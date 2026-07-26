// Wake a shadow-atelier Codex session non-interactively.
// Usage: node wake_codex.mjs [--role sol|sol2|luna] [--queue-retry N] [reason...]
// - Resumes ONLY by the role's pinned session id (no --last fallback:
//   this machine runs Codex for multiple ateliers and --last could
//   resume a foreign session).
// - Appends full turn output to the role's activity log.
//
// ── 仕様(2026-07-26 ツール総点検で v2 化: SKIP → キュー運用) ─────────────
// ガード(main レーン sol/luna のみ・sol2 は並走レーンとして対象外):
//   (a) codex.exe 稼働中かつ main ログ 45 分以内に更新 → 稼働中と判断
//   (b) main ログ 45 分無音でも sol2 ログが 45 分以内 → ゾンビ kill を拒否
//       (taskkill /IM は並走レーンを巻き添えにするため)
//   (c) 両ログ 45 分無音 → ゾンビと判断し kill して続行(従来どおり)
// v2 変更: (a)(b) は起床要求を「弾く」のでなく ops/bin/wake_queue.jsonl へ
//   enqueue する(ENQUEUED・exit 2)。排出は ops/bin/wake_queue_drain.mjs
//   (本スクリプトの turn 終了フック/turn_monitor.ps1/手動 の 3 経路)。
//   多重発火・空キュー・retry 上限の仕様は wake_queue_drain.mjs ヘッダが正本。
// 観測性: ガード判定・enqueue・turn 終了は ops/wake_dispatch.log にも記録する
//   (launch_wake.ps1 の Hidden 起動で console 出力が消失し、SKIP がどこにも
//   残らなかった問題への恒久対処 — 2026-07-26 総点検の発見)。
// exit code: 0=起床実行 / 2=enqueue・dup・drop(起床せず) / 1,3=引数・ピン異常。
// ────────────────────────────────────────────────────────────────────────
import { execSync, spawn } from 'node:child_process';
import fs from 'node:fs';

const REPO = 'C:/Users/81905/Desktop/shadow-atelier';
const LOG = `${REPO}/ops/codex_activity.log`;
const QUEUE = `${REPO}/ops/bin/wake_queue.jsonl`;
const DISPATCH = `${REPO}/ops/wake_dispatch.log`;
const MAX_QUEUE_RETRY = 10;
const dlog = (msg) => {
  try { fs.appendFileSync(DISPATCH, `${new Date().toISOString()} [wake] ${msg}\n`); } catch { /* never block a wake */ }
  console.log(msg);
};
let argv = process.argv.slice(2);
let role = 'sol', effort = '', queueRetry = 0;
while (argv[0] === '--role' || argv[0] === '--effort' || argv[0] === '--queue-retry') {
  if (argv[0] === '--role') { role = (argv[1] || 'sol').toLowerCase(); argv = argv.slice(2); }
  else if (argv[0] === '--effort') { effort = (argv[1] || '').toLowerCase(); argv = argv.slice(2); }
  else { queueRetry = parseInt(argv[1] || '0', 10) || 0; argv = argv.slice(2); }
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

// enqueue this wake request instead of dropping it (v2: SKIP -> ENQUEUED).
// The message payload (if any) stays in ops/inbox_codex either way - the queue
// only carries the wake trigger, so QUEUE-DROPPED loses no content.
function enqueueSelf(why) {
  if (queueRetry >= MAX_QUEUE_RETRY) {
    dlog(`QUEUE-DROPPED(${role}): retry limit ${MAX_QUEUE_RETRY} reached (${why}) - auto-wake abandoned; message (if any) remains in ops/inbox_codex`);
    process.exit(2);
  }
  let entries = [];
  if (fs.existsSync(QUEUE)) {
    entries = fs.readFileSync(QUEUE, 'utf8').split(/\r?\n/).filter(Boolean)
      .map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
  }
  if (entries.some((x) => x.role === role && x.reason === reason)) {
    dlog(`QUEUE-DUP(${role}): identical entry already queued (len=${entries.length}) - not added (${why})`);
    process.exit(2);
  }
  const entry = { ts: new Date().toISOString(), role, effort, reason, retries: queueRetry, why };
  fs.appendFileSync(QUEUE, JSON.stringify(entry) + '\n');
  dlog(`ENQUEUED(${role}): ${why} - queue len=${entries.length + 1}; auto-fires on next turn-end drain`);
  process.exit(2);
}

if (role !== 'sol2') {
  const tasklist = execSync('tasklist', { encoding: 'utf8' });
  if (/^codex\.exe/im.test(tasklist)) {
    const silentMin = fs.existsSync(LOG) ? (Date.now() - fs.statSync(LOG).mtimeMs) / 60000 : Infinity;
    if (silentMin < 45) {
      enqueueSelf('main lane busy (codex.exe running, log active)');
    }
    const SOL2_LOG = `${REPO}/ops/codex_activity_sol2.log`;
    const sol2SilentMin = fs.existsSync(SOL2_LOG) ? (Date.now() - fs.statSync(SOL2_LOG).mtimeMs) / 60000 : Infinity;
    if (sol2SilentMin < 45) {
      enqueueSelf('sol2 lane active - zombie-kill refused (taskkill would hit the parallel lane)');
    }
    dlog(`ZOMBIE-DETECTED(${role}): codex.exe present but log silent ${Math.round(silentMin)}min - killing and proceeding`);
    try { execSync('taskkill /IM codex.exe /F', { stdio: 'pipe' }); } catch { /* already gone */ }
  }
} else {
  dlog('PARALLEL-LANE(sol2): skipping running-guard by design (do not taskkill - main lane may be live)');
}

if (!fs.existsSync(ID_FILE)) {
  dlog(`NO-PINNED-SESSION(${role}): refusing to wake (no --last fallback on a multi-atelier machine). Use launch_new.mjs first.`);
  process.exit(3);
}
const sid = fs.readFileSync(ID_FILE, 'utf8').trim().split(/\r?\n/)[0];
const quoted = '"' + reason.replace(/"/g, '\\"') + '"';
// 注意: `codex exec resume` は --sandbox フラグ非対応(new 専用)。sandbox は元セッション設定を
// 継承するため -c のみ渡す(2026-07-19 実測: --sandbox 付きは exit 2 で起床失敗)。
const cmd = `codex exec resume ${sid}${MODEL_FLAGS} -c approval_policy="never" ${quoted}`;

if (!fs.existsSync(ROLE_LOG)) fs.writeFileSync(ROLE_LOG, '﻿');
fs.appendFileSync(ROLE_LOG, `\n===== WAKE(${role}) ${new Date().toISOString()} =====\nreason: ${reason}\ntarget: ${sid}\n`);
dlog(`WAKE-START(${role}) target=${sid}${queueRetry > 0 ? ` (from queue, retry=${queueRetry})` : ''}`);

const ws = fs.createWriteStream(ROLE_LOG, { flags: 'a' });
// stdin は必ず閉じる(launch_new.mjs と同じ理由 — EOF 待ちブロック防止)
const child = spawn(cmd, { cwd: REPO, shell: true, stdio: ['ignore', 'pipe', 'pipe'] });
child.stdout.setEncoding('utf8');
child.stderr.setEncoding('utf8');
child.stdout.on('data', (c) => ws.write(c));
child.stderr.on('data', (c) => ws.write(c));
const code = await new Promise((res) => child.on('close', res));
ws.end(`\n----- turn end (exit ${code}) ${new Date().toISOString()} -----\n`);
dlog(`WAKE-DONE(${role}) exit=${code}`);
// turn-end hook: fire the next queued wake request, if any (fire-and-forget;
// drain holds its own lock and re-evaluates the guards - see wake_queue_drain.mjs).
try {
  if (fs.existsSync(QUEUE) && fs.statSync(QUEUE).size > 0) {
    const d = spawn(process.execPath, [`${REPO}/ops/bin/wake_queue_drain.mjs`, '--from', `turn-end(${role})`],
      { cwd: REPO, detached: true, stdio: 'ignore' });
    d.unref();
    dlog(`DRAIN-HOOK(${role}): queue non-empty - drain spawned`);
  }
} catch (err) { dlog(`DRAIN-HOOK-ERROR(${role}): ${err.message}`); }
