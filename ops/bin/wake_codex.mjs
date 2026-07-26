// Wake a shadow-atelier Codex session non-interactively.
// Usage: node wake_codex.mjs [--role sol|luna] [reason...]
// - Resumes ONLY by the role's pinned session id (no --last fallback:
//   this machine runs Codex for multiple ateliers and --last could
//   resume a foreign session).
// - Skips if codex.exe is running with an active log (zombie guard: 45 min
//   silence => kill and proceed). Ported from atelier_lean/ES7/ops (proven).
// - Appends full turn output to ops/codex_activity.log.
import { execSync, spawn } from 'node:child_process';
import fs from 'node:fs';

const REPO = 'C:/Users/81905/Desktop/shadow-atelier';
const LOG = `${REPO}/ops/codex_activity.log`;
let argv = process.argv.slice(2);
let role = 'sol', effort = '';
while (argv[0] === '--role' || argv[0] === '--effort') {
  if (argv[0] === '--role') { role = (argv[1] || 'sol').toLowerCase(); argv = argv.slice(2); }
  else { effort = (argv[1] || '').toLowerCase(); argv = argv.slice(2); }
}
if (!['sol', 'sol2', 'luna'].includes(role)) { console.log('BAD-ROLE'); process.exit(1); }
// 推論設定を resume にも明示(config 既定 sol/max が Luna セッションへ漏れる事故の防止)
let MODEL_FLAGS;
if (role === 'sol' || role === 'sol2') {
  if (effort) { console.log('SOL-EFFORT-IS-PINNED-MAX'); process.exit(1); }
  MODEL_FLAGS = ' -m gpt-5.6-sol -c model_reasoning_effort="max"';
} else {
  if (!effort) effort = 'high';
  if (!['medium', 'high', 'xhigh'].includes(effort)) { console.log('BAD-EFFORT(luna)'); process.exit(1); }
  MODEL_FLAGS = ` -m gpt-5.6-luna -c model_reasoning_effort="${effort}"`;
}
const ID_FILE = role === 'sol'
  ? `${REPO}/ops/bin/codex_session_id.txt`
  : role === 'sol2'
    ? `${REPO}/ops/bin/codex_session_id_sol2.txt`
    : `${REPO}/ops/bin/codex_session_id_luna.txt`;
const ROLE_LOG = role === 'sol2' ? `${REPO}/ops/codex_activity_sol2.log` : LOG;
const reason = argv.join(' ')
  || 'ops: new message in ops/inbox_codex. Read it and resume work. (external wake from commander)';

if (role !== 'sol2') {
  const tasklist = execSync('tasklist', { encoding: 'utf8' });
  if (/^codex\.exe/im.test(tasklist)) {
    const silentMin = fs.existsSync(LOG) ? (Date.now() - fs.statSync(LOG).mtimeMs) / 60000 : Infinity;
    if (silentMin < 45) {
      console.log('SKIP-WAKE: codex.exe running and log active - message stays in inbox_codex');
      process.exit(2);
    }
    const SOL2_LOG = `${REPO}/ops/codex_activity_sol2.log`;
    const sol2SilentMin = fs.existsSync(SOL2_LOG) ? (Date.now() - fs.statSync(SOL2_LOG).mtimeMs) / 60000 : Infinity;
    if (sol2SilentMin < 45) {
      console.log('SKIP-WAKE: sol2 lane active - refusing zombie-kill (would kill the parallel lane). Message stays in inbox_codex');
      process.exit(2);
    }
    console.log(`ZOMBIE-DETECTED: codex.exe present but log silent ${Math.round(silentMin)}min - killing and proceeding`);
    try { execSync('taskkill /IM codex.exe /F', { stdio: 'pipe' }); } catch { /* already gone */ }
  }
} else {
  console.log('PARALLEL-LANE(sol2): skipping running-guard by design (do not taskkill - main lane may be live)');
}

if (!fs.existsSync(ID_FILE)) {
  console.log(`NO-PINNED-SESSION(${role}): refusing to wake (no --last fallback on a multi-atelier machine). Use launch_new.mjs first.`);
  process.exit(3);
}
const sid = fs.readFileSync(ID_FILE, 'utf8').trim().split(/\r?\n/)[0];
const quoted = '"' + reason.replace(/"/g, '\\"') + '"';
// 注意: `codex exec resume` は --sandbox フラグ非対応(new 専用)。sandbox は元セッション設定を
// 継承するため -c のみ渡す(2026-07-19 実測: --sandbox 付きは exit 2 で起床失敗)。
const cmd = `codex exec resume ${sid}${MODEL_FLAGS} -c approval_policy="never" ${quoted}`;

if (!fs.existsSync(ROLE_LOG)) fs.writeFileSync(ROLE_LOG, '﻿');
fs.appendFileSync(ROLE_LOG, `\n===== WAKE(${role}) ${new Date().toISOString()} =====\nreason: ${reason}\ntarget: ${sid}\n`);

const ws = fs.createWriteStream(ROLE_LOG, { flags: 'a' });
// stdin は必ず閉じる(launch_new.mjs と同じ理由 — EOF 待ちブロック防止)
const child = spawn(cmd, { cwd: REPO, shell: true, stdio: ['ignore', 'pipe', 'pipe'] });
child.stdout.setEncoding('utf8');
child.stderr.setEncoding('utf8');
child.stdout.on('data', (c) => ws.write(c));
child.stderr.on('data', (c) => ws.write(c));
const code = await new Promise((res) => child.on('close', res));
ws.end(`\n----- turn end (exit ${code}) ${new Date().toISOString()} -----\n`);
console.log(`WAKE-DONE exit=${code}`);
