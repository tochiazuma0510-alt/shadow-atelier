// Start a BRAND-NEW Codex (Sol) session for shadow-atelier and pin its
// session id, so follow-up wakes use `codex exec resume <pinned-id>`.
// Session policy (ES7-aligned): one NEW session per Sol kickoff (便);
// context travels via files (kickoff references prior replies). wake_codex
// is for follow-ups WITHIN the current 便 only.
// Usage: node launch_new.mjs [--renew] [--role sol|luna] "<instruction...>"
// - Roles (subscription discipline): sol = math audits only (config default
//   gpt-6-astra / max (2026-09-05 Astra switch; was gpt-5.6-sol)). luna = implementation & bulk computation
//   (-m gpt-5.6-luna, effort high). Each role has its OWN pin file.
// - Without --renew: refuses if that role's session id is already pinned.
// - With --renew: archives the current pin to codex_session_id_history.txt
//   and starts a fresh session (use at the start of each new 便).
// - Refuses if codex.exe is already running (do not spawn a second brain).
import { execSync, spawn } from 'node:child_process';
import fs from 'node:fs';

const REPO = 'C:/Users/81905/Desktop/shadow-atelier';
const LOG = `${REPO}/ops/codex_activity.log`;
const HIST_FILE = `${REPO}/ops/bin/codex_session_id_history.txt`;
let argv = process.argv.slice(2);
let renew = false, role = 'sol', effort = '';
while (argv[0] === '--renew' || argv[0] === '--role' || argv[0] === '--effort') {
  if (argv[0] === '--renew') { renew = true; argv = argv.slice(1); }
  else if (argv[0] === '--role') { role = (argv[1] || 'sol').toLowerCase(); argv = argv.slice(2); }
  else { effort = (argv[1] || '').toLowerCase(); argv = argv.slice(2); }
}
if (!['sol', 'sol2', 'luna'].includes(role)) { console.log('BAD-ROLE'); process.exit(1); }
// sol2 (2026-07-26): second PARALLEL sol-model lane. Own pin + own log; skips
// the codex-already-running guard BY DESIGN (parallel lanes are intentional).
// 推論設定の強制(2026-07-18 ユーザー指示「推論設定を必ず遵守」):
// - Sol = gpt-6-astra / max (2026-09-05 Astra switch; was gpt-5.6-sol) 固定(effort 指定は拒否 — 数学監査を安売りしない)
// - Luna = gpt-5.6-luna / effort は medium|high|xhigh(既定 high、Lean shard は xhigh、定型は medium)
let MODEL_FLAGS;
if (role === 'sol' || role === 'sol2') {
  if (effort) { console.log('SOL-EFFORT-IS-PINNED-MAX: --effort is not allowed for sol'); process.exit(1); }
  MODEL_FLAGS = ' -m gpt-6-astra -c model_reasoning_effort="max"';
} else {
  if (!effort) effort = 'high';
  if (!['medium', 'high', 'xhigh'].includes(effort)) { console.log('BAD-EFFORT(luna): medium|high|xhigh'); process.exit(1); }
  MODEL_FLAGS = ` -m gpt-5.6-luna -c model_reasoning_effort="${effort}"`;
}
const ID_FILE = role === 'sol'
  ? `${REPO}/ops/bin/codex_session_id.txt`
  : role === 'sol2'
    ? `${REPO}/ops/bin/codex_session_id_sol2.txt`
    : `${REPO}/ops/bin/codex_session_id_luna.txt`;
const ROLE_LOG = role === 'sol2' ? `${REPO}/ops/codex_activity_sol2.log` : LOG;
const instr = argv.join(' ');
if (!instr) { console.log('NO-INSTRUCTION'); process.exit(1); }
if (fs.existsSync(ID_FILE)) {
  if (!renew) { console.log('ALREADY-PINNED: use wake_codex.mjs for follow-ups, or --renew for a new 便'); process.exit(3); }
  const old = fs.readFileSync(ID_FILE, 'utf8').trim();
  fs.appendFileSync(HIST_FILE, `${new Date().toISOString()} ${role} ${old}\n`);
  fs.unlinkSync(ID_FILE);
  console.log(`RENEWED: archived ${role} ${old}`);
}

if (role !== 'sol2') {
  const tasklist = execSync('tasklist', { encoding: 'utf8' });
  if (/^codex\.exe/im.test(tasklist)) { console.log('CODEX-ALREADY-RUNNING: aborting first launch'); process.exit(2); }
} else {
  console.log('PARALLEL-LANE(sol2): skipping running-guard by design');
}

const quoted = '"' + instr.replace(/"/g, '\\"') + '"';
const cmd = `codex exec${MODEL_FLAGS} -c approval_policy="never" --sandbox workspace-write ${quoted}`;

if (!fs.existsSync(ROLE_LOG)) fs.writeFileSync(ROLE_LOG, '﻿');
fs.appendFileSync(ROLE_LOG, `\n===== NEW-SESSION(${role}) ${new Date().toISOString()} =====\ninstr: ${instr}\n`);

const ws = fs.createWriteStream(ROLE_LOG, { flags: 'a' });
// stdin は必ず閉じる: パイプのまま開いていると codex exec が
// "Reading additional input from stdin..." で EOF 待ちブロックする(2026-07-18 実測)
const child = spawn(cmd, { cwd: REPO, shell: true, stdio: ['ignore', 'pipe', 'pipe'] });
let buf = '';
let pinned = false;
const tryPin = (chunk) => {
  if (pinned) return;
  buf += chunk;
  const m = buf.match(/session id:\s*([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/i)
        || buf.match(/\b([0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12})\b/i);
  if (m) { fs.writeFileSync(ID_FILE, m[1] + '\n'); pinned = true; console.log(`PINNED ${m[1]}`); }
};
child.stdout.setEncoding('utf8');
child.stderr.setEncoding('utf8');
child.stdout.on('data', (c) => { ws.write(c); tryPin(c); });
child.stderr.on('data', (c) => { ws.write(c); tryPin(c); });
const code = await new Promise((res) => child.on('close', res));
ws.end(`\n----- turn end (exit ${code}) ${new Date().toISOString()} -----\n`);
console.log(`LAUNCH-DONE exit=${code} pinned=${pinned}`);
