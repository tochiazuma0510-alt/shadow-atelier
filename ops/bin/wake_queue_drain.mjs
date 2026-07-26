// ops/bin/wake_queue_drain.mjs — wake 要求キューの排出(dequeue)スクリプト。
// 2026-07-26 ツール総点検で新設(司令塔発注・事例1「起床要求を弾くのでなく enqueue し、
// codex 終了時に自動発火する」)。常駐プロセスは持たない(8GB RAM 制約)— 終了フック方式。
//
// ── 仕様 ────────────────────────────────────────────────────────────────
// 入力:   ops/bin/wake_queue.jsonl(1 行 1 エントリの JSON:
//         {ts, role, effort, reason, retries, why})。wake_codex.mjs がガードで
//         起床を見送った時に追記する(SKIP → ENQUEUED)。
// 呼び元: ①wake_codex.mjs の turn 終了フック(キュー非空時のみ detached 起動)
//         ②turn_monitor.ps1 の正常完了パス ③手動 `node ops/bin/wake_queue_drain.mjs`。
// 動作:   先頭から FIFO で「今すぐ起床可能」な最初の 1 件だけを取り出し、
//         detached の `node wake_codex.mjs --role .. --queue-retry N+1 <reason>` を発火。
//         起床可能の判定(wake_codex のガードの事前評価):
//           - role=sol2: 常に可(並走レーンはガード対象外 — wake_codex と同じ設計)
//           - それ以外: codex.exe 不在、または両活動ログ 45 分無音(ゾンビ経路は
//             wake_codex 側が kill 判断する — 本スクリプトは kill しない)。
// 多重発火の防止(仕様ヘッダ明記事項):
//   1) ロックファイル ops/bin/wake_queue.lock(O_EXCL 作成)— 同時 drain は 1 本のみ。
//      120 秒超の stale ロックは奪取。process.exit を使わず必ず解放(exit ハンドラ)。
//   2) 1 回の drain で発火は最大 1 件(発火された wake が次の turn 終了で再 drain)。
//   3) 発火された wake_codex は自身のガードを再評価する — レースで先客がいれば
//      retries+1 で再 enqueue(上限 10 回で QUEUE-DROPPED・メッセージ本体は
//      ops/inbox_codex に残るため喪失しない)。
// 空キューの扱い(仕様ヘッダ明記事項): ファイル不在 or 0 バイト or 全行破損 →
//   DRAIN-EMPTY を記録して何もしない(破損行は捨てて記録)。空になったら
//   キューファイル自体を削除する。
// 出力:   判定と発火の全行を ops/wake_dispatch.log に追記(+stdout)。Hidden 起動でも
//         事後検証可能(2026-07-26 発見: ガード判定の console 出力が Start-Process
//         -WindowStyle Hidden で消失していた問題への恒久対処)。
// フラグ: --dry-run 判定のみ(キュー変更・発火なし)。--from <label> 呼び元の記録。
// 非対象: launch_new.mjs は変更しない(new 便の turn 終了は turn_monitor 経由で drain)。
// ────────────────────────────────────────────────────────────────────────
import { execSync, spawn } from 'node:child_process';
import fs from 'node:fs';

const REPO = 'C:/Users/81905/Desktop/shadow-atelier';
const QUEUE = `${REPO}/ops/bin/wake_queue.jsonl`;
const QLOCK = `${REPO}/ops/bin/wake_queue.lock`;
const DISPATCH = `${REPO}/ops/wake_dispatch.log`;
const MAIN_LOG = `${REPO}/ops/codex_activity.log`;
const SOL2_LOG = `${REPO}/ops/codex_activity_sol2.log`;
const SILENCE_MIN = 45;      // wake_codex.mjs のゾンビガードと同一の閾値
const LOCK_STALE_SEC = 120;

const argv = process.argv.slice(2);
const dryRun = argv.includes('--dry-run');
const fromIdx = argv.indexOf('--from');
const from = fromIdx >= 0 ? (argv[fromIdx + 1] || 'unknown') : 'manual';

const dlog = (msg) => {
  try { fs.appendFileSync(DISPATCH, `${new Date().toISOString()} [drain] ${msg}\n`); } catch { /* dispatch log must never break a drain */ }
  console.log(msg);
};
const silentMin = (p) => (fs.existsSync(p) ? (Date.now() - fs.statSync(p).mtimeMs) / 60000 : Infinity);

// --- lock (multi-fire protection) ---
let locked = false;
function acquireLock() {
  for (let attempt = 0; attempt < 2; attempt++) {
    try { fs.writeFileSync(QLOCK, `${process.pid} ${new Date().toISOString()}\n`, { flag: 'wx' }); locked = true; return true; }
    catch {
      try {
        const age = (Date.now() - fs.statSync(QLOCK).mtimeMs) / 1000;
        if (age > LOCK_STALE_SEC) { fs.unlinkSync(QLOCK); continue; }  // stale takeover
        return false;
      } catch { continue; }  // lock vanished between attempts - retry once
    }
  }
  return false;
}
process.on('exit', () => { if (locked) { try { fs.unlinkSync(QLOCK); } catch { /* already gone */ } } });

// --- empty queue: nothing to do ---
if (!fs.existsSync(QUEUE) || fs.statSync(QUEUE).size === 0) {
  dlog(`DRAIN-EMPTY (from=${from})`);
  process.exit(0);
}
if (!dryRun && !acquireLock()) {
  dlog(`DRAIN-BUSY: another drain holds the lock (from=${from}) - exiting`);
  process.exit(0);
}

const raw = fs.readFileSync(QUEUE, 'utf8').split(/\r?\n/).filter(Boolean);
const entries = [];
let corrupt = 0;
for (const l of raw) { try { entries.push(JSON.parse(l)); } catch { corrupt++; } }
if (corrupt > 0) dlog(`DRAIN-WARN: ${corrupt} corrupt queue line(s) dropped`);
if (entries.length === 0) {
  if (!dryRun) { try { fs.unlinkSync(QUEUE); } catch { /* ignore */ } }
  dlog(`DRAIN-EMPTY (all lines corrupt, from=${from})`);
  process.exit(0);
}

const codexRunning = /^codex\.exe/im.test(execSync('tasklist', { encoding: 'utf8' }));
const mainSilent = silentMin(MAIN_LOG);
const sol2Silent = silentMin(SOL2_LOG);
const eligible = (e) =>
  e.role === 'sol2'
    ? true
    : (!codexRunning || (mainSilent >= SILENCE_MIN && sol2Silent >= SILENCE_MIN));

const idx = entries.findIndex(eligible);
if (idx < 0) {
  dlog(`DRAIN-DEFERRED: head=${entries[0].role} len=${entries.length} codexRunning=${codexRunning} `
    + `mainSilent=${Math.round(mainSilent)}m sol2Silent=${Math.round(sol2Silent)}m (from=${from}) - retry on next turn end`);
  process.exit(0);
}
const e = entries[idx];
if (dryRun) {
  dlog(`DRAIN-DRYRUN: would fire role=${e.role} retries=${e.retries || 0} reason=${String(e.reason).slice(0, 80)} (from=${from})`);
  process.exit(0);
}
entries.splice(idx, 1);
if (entries.length === 0) fs.unlinkSync(QUEUE);
else fs.writeFileSync(QUEUE, entries.map((x) => JSON.stringify(x)).join('\n') + '\n');

const args = [`${REPO}/ops/bin/wake_codex.mjs`, '--role', e.role];
if (e.effort) args.push('--effort', e.effort);
args.push('--queue-retry', String((e.retries || 0) + 1));
args.push(String(e.reason));
const child = spawn(process.execPath, args, { cwd: REPO, detached: true, stdio: 'ignore' });
child.unref();
dlog(`DEQUEUE-FIRED(${e.role}): retries=${(e.retries || 0) + 1} queue_left=${entries.length} `
  + `reason=${String(e.reason).slice(0, 80)} (from=${from})`);
