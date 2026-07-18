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
let role = 'sol';
if (argv[0] === '--role') { role = (argv[1] || 'sol').toLowerCase(); argv = argv.slice(2); }
if (!['sol', 'luna'].includes(role)) { console.log('BAD-ROLE'); process.exit(1); }
const ID_FILE = role === 'sol'
  ? `${REPO}/ops/bin/codex_session_id.txt`
  : `${REPO}/ops/bin/codex_session_id_luna.txt`;
const reason = argv.join(' ')
  || 'ops: new message in ops/inbox_codex. Read it and resume work. (external wake from commander)';

const tasklist = execSync('tasklist', { encoding: 'utf8' });
if (/^codex\.exe/im.test(tasklist)) {
  const silentMin = fs.existsSync(LOG) ? (Date.now() - fs.statSync(LOG).mtimeMs) / 60000 : Infinity;
  if (silentMin < 45) {
    console.log('SKIP-WAKE: codex.exe running and log active - message stays in inbox_codex');
    process.exit(2);
  }
  console.log(`ZOMBIE-DETECTED: codex.exe present but log silent ${Math.round(silentMin)}min - killing and proceeding`);
  try { execSync('taskkill /IM codex.exe /F', { stdio: 'pipe' }); } catch { /* already gone */ }
}

if (!fs.existsSync(ID_FILE)) {
  console.log(`NO-PINNED-SESSION(${role}): refusing to wake (no --last fallback on a multi-atelier machine). Use launch_new.mjs first.`);
  process.exit(3);
}
const sid = fs.readFileSync(ID_FILE, 'utf8').trim().split(/\r?\n/)[0];
const quoted = '"' + reason.replace(/"/g, '\\"') + '"';
const cmd = `codex exec resume ${sid} -c approval_policy="never" --sandbox workspace-write ${quoted}`;

if (!fs.existsSync(LOG)) fs.writeFileSync(LOG, '﻿');
fs.appendFileSync(LOG, `\n===== WAKE(${role}) ${new Date().toISOString()} =====\nreason: ${reason}\ntarget: ${sid}\n`);

const ws = fs.createWriteStream(LOG, { flags: 'a' });
// stdin は必ず閉じる(launch_new.mjs と同じ理由 — EOF 待ちブロック防止)
const child = spawn(cmd, { cwd: REPO, shell: true, stdio: ['ignore', 'pipe', 'pipe'] });
child.stdout.setEncoding('utf8');
child.stderr.setEncoding('utf8');
child.stdout.on('data', (c) => ws.write(c));
child.stderr.on('data', (c) => ws.write(c));
const code = await new Promise((res) => child.on('close', res));
ws.end(`\n----- turn end (exit ${code}) ${new Date().toISOString()} -----\n`);
console.log(`WAKE-DONE exit=${code}`);
