// Start a BRAND-NEW Codex (Sol) session for shadow-atelier and pin its
// session id, so follow-up wakes use `codex exec resume <pinned-id>`.
// Session policy (ES7-aligned): one NEW session per Sol kickoff (便);
// context travels via files (kickoff references prior replies). wake_codex
// is for follow-ups WITHIN the current 便 only.
// Usage: node launch_new.mjs [--renew] [--role sol|luna] "<instruction...>"
// - Roles (subscription discipline): sol = math audits only (config default
//   gpt-5.6-sol / max). luna = implementation & bulk computation
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
let renew = false, role = 'sol';
while (argv[0] === '--renew' || argv[0] === '--role') {
  if (argv[0] === '--renew') { renew = true; argv = argv.slice(1); }
  else { role = (argv[1] || 'sol').toLowerCase(); argv = argv.slice(2); }
}
if (!['sol', 'luna'].includes(role)) { console.log('BAD-ROLE'); process.exit(1); }
const ID_FILE = role === 'sol'
  ? `${REPO}/ops/bin/codex_session_id.txt`
  : `${REPO}/ops/bin/codex_session_id_luna.txt`;
const MODEL_FLAGS = role === 'luna' ? ' -m gpt-5.6-luna -c model_reasoning_effort="high"' : '';
const instr = argv.join(' ');
if (!instr) { console.log('NO-INSTRUCTION'); process.exit(1); }
if (fs.existsSync(ID_FILE)) {
  if (!renew) { console.log('ALREADY-PINNED: use wake_codex.mjs for follow-ups, or --renew for a new 便'); process.exit(3); }
  const old = fs.readFileSync(ID_FILE, 'utf8').trim();
  fs.appendFileSync(HIST_FILE, `${new Date().toISOString()} ${role} ${old}\n`);
  fs.unlinkSync(ID_FILE);
  console.log(`RENEWED: archived ${role} ${old}`);
}

const tasklist = execSync('tasklist', { encoding: 'utf8' });
if (/^codex\.exe/im.test(tasklist)) { console.log('CODEX-ALREADY-RUNNING: aborting first launch'); process.exit(2); }

const quoted = '"' + instr.replace(/"/g, '\\"') + '"';
const cmd = `codex exec${MODEL_FLAGS} -c approval_policy="never" --sandbox workspace-write ${quoted}`;

if (!fs.existsSync(LOG)) fs.writeFileSync(LOG, '﻿');
fs.appendFileSync(LOG, `\n===== NEW-SESSION(${role}) ${new Date().toISOString()} =====\ninstr: ${instr}\n`);

const ws = fs.createWriteStream(LOG, { flags: 'a' });
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
