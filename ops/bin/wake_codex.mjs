// Wake the shadow-atelier Codex (Sol) session non-interactively.
// Usage: node wake_codex.mjs [reason...]
// - Resumes ONLY by pinned session id (ops/bin/codex_session_id.txt).
//   NO --last fallback: this machine runs Codex for multiple ateliers
//   (atelier_lean/ES7 etc.) and --last could resume a foreign session.
// - Skips if codex.exe is running with an active log (zombie guard: 45 min
//   silence => kill and proceed). Ported from atelier_lean/ES7/ops (proven).
// - Appends full turn output to ops/codex_activity.log.
import { execSync, spawn } from 'node:child_process';
import fs from 'node:fs';

const REPO = 'C:/Users/81905/Desktop/shadow-atelier';
const LOG = `${REPO}/ops/codex_activity.log`;
const ID_FILE = `${REPO}/ops/bin/codex_session_id.txt`;
const reason = process.argv.slice(2).join(' ')
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
  console.log('NO-PINNED-SESSION: refusing to wake (no --last fallback on a multi-atelier machine). Use launch_new.mjs first.');
  process.exit(3);
}
const sid = fs.readFileSync(ID_FILE, 'utf8').trim().split(/\r?\n/)[0];
const quoted = '"' + reason.replace(/"/g, '\\"') + '"';
const cmd = `codex exec resume ${sid} -c approval_policy="never" --sandbox workspace-write ${quoted}`;

if (!fs.existsSync(LOG)) fs.writeFileSync(LOG, '﻿');
fs.appendFileSync(LOG, `\n===== WAKE ${new Date().toISOString()} =====\nreason: ${reason}\ntarget: ${sid}\n`);

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
