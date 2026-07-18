// First launch: start a BRAND-NEW Codex (Sol) session for shadow-atelier and
// pin its session id, so all later wakes use `codex exec resume <pinned-id>`.
// Usage: node launch_new.mjs "<instruction...>"
// - Refuses if a session id is already pinned (use wake_codex.mjs instead).
// - Refuses if codex.exe is already running (do not spawn a second brain).
// - Streams the whole turn to ops/codex_activity.log and scans the stream for
//   "session id: <uuid>" to write ops/bin/codex_session_id.txt.
import { execSync, spawn } from 'node:child_process';
import fs from 'node:fs';

const REPO = 'C:/Users/81905/Desktop/shadow-atelier';
const LOG = `${REPO}/ops/codex_activity.log`;
const ID_FILE = `${REPO}/ops/bin/codex_session_id.txt`;
const instr = process.argv.slice(2).join(' ');
if (!instr) { console.log('NO-INSTRUCTION'); process.exit(1); }
if (fs.existsSync(ID_FILE)) { console.log('ALREADY-PINNED: use wake_codex.mjs'); process.exit(3); }

const tasklist = execSync('tasklist', { encoding: 'utf8' });
if (/^codex\.exe/im.test(tasklist)) { console.log('CODEX-ALREADY-RUNNING: aborting first launch'); process.exit(2); }

const quoted = '"' + instr.replace(/"/g, '\\"') + '"';
const cmd = `codex exec -c approval_policy="never" --sandbox workspace-write ${quoted}`;

if (!fs.existsSync(LOG)) fs.writeFileSync(LOG, '﻿');
fs.appendFileSync(LOG, `\n===== NEW-SESSION ${new Date().toISOString()} =====\ninstr: ${instr}\n`);

const ws = fs.createWriteStream(LOG, { flags: 'a' });
const child = spawn(cmd, { cwd: REPO, shell: true });
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
