#!/usr/bin/env node
// crosscheck/check-cli-fail-closed.mjs -- 裁定40/便39 F1.3 の CLI wrapper
// fail-open 修理を実際に CLI 経由で叩く adversarial 較正。
//
// 背景(Sol 便39 F1.3): 旧 u-compare.mjs / u-compare-ninf.mjs の末尾は
//   try {
//     const { pathToFileURL } = await import('node:url');
//     if (direct) runCli();
//   } catch { /* ignore */ }
// という形で、direct-run 判定だけでなく runCli() 本体の JSON.parse/BigInt/
// I-O/型例外までも同じ catch で握り潰していた。実測では、非 JSON の第一
// 引数を与えると**無出力・exit 0** となり、fail-closed の建前(異常入力は
// 必ず検出して止まる)に反していた。
//
// 修理後(本ファイルが検査する現行版): direct-run 判定(pathToFileURL/
// import.meta.url の比較)は try で囲まず、runCli() 本体だけを
// runCliGuarded() の try/catch で囲み、例外は stderr に INTEGRITY_STOP
// メッセージを出して非零 exit する。
//
// 実測上の注意(便38 F1.2 の教訓・裁定41/便40 F2.2 で harness 自体を修理):
// この管理下 Windows セッションでは、ある node プロセスが nested に子 node
// プロセスを spawn すると stdout 捕捉が EPERM で拒まれることがあった
// (check-r7-bundle-attack.mjs の旧版で遭遇)。本ファイル自体は「node
// crosscheck/check-cli-fail-closed.mjs」として**トップレベルから直接実行
// される**ことを想定しており(ネストではない)、内部で spawn する子
// process は一段のみである。
//
// **裁定41/便40 F2.2 の指摘・修理**: 旧版は `spawnSync` が stdout を
// 生成しない(`r.error` が立つ・`r.stdout` が `undefined`)場合に
// `r.stdout.length` を無条件参照して `TypeError` で crash していた
// (Sol が管理下 Windows セッションで実測)。本版は `safeRun()` でこれを
// 明示的に検出し、**calibration の PASS には数えず**、`[ENV_FAIL]` として
// 別枠報告する(黙って PASS 扱いにしない・crash もしない)。また
// `bad-rational.json` fixture は旧版では `id` が正当 pathB と不一致で
// あり、実際の停止理由が `id mismatch` であって有理数 parse にすら
// 到達していなかった(Sol の指摘)。本版は**正当な raw 全体を clone**し、
// 攻撃対象の 1 field だけを malformed rational へ書き換え、到達した停止
// 理由が strict rational parser であることを assert する。
// もし spawnSync の EPERM がこの環境で再発した場合は、
// `crosscheck/check-cli-fail-closed.ps1`(本便で新設した PowerShell 版
// 外側 harness・同じ攻撃を `node` 直接呼び出し + `$LASTEXITCODE` で判定)
// を使うこと。
//
// 実行: node crosscheck/check-cli-fail-closed.mjs
//   (PowerShell fallback: powershell -File crosscheck/check-cli-fail-closed.ps1)

import { spawnSync } from 'node:child_process';
import { writeFileSync, readFileSync, mkdtempSync, rmSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const NODE = process.execPath;

let pass = 0, fail = 0, envFail = 0;
function report(name, ok, extra = '') {
  if (ok) { pass++; console.log(`[PASS] ${name}${extra ? '  ' + extra : ''}`); }
  else { fail++; console.log(`[FAIL] ${name}${extra ? '  ' + extra : ''}`); }
}
// 裁定41/便40 F2.2: spawnSync 自体の失敗(EPERM 等)は calibration PASS/FAIL
// に混ぜず、明示的な環境 FAIL として報告する(crash もしない・黙って
// PASS にもしない)。
function reportEnvFail(name, reason) {
  envFail++;
  console.log(`[ENV_FAIL] ${name} -- spawnSync did not produce usable output in this environment: ${reason} (この個別ケースは calibration PASS に数えない。crosscheck/check-cli-fail-closed.ps1 で代替実行すること)`);
}

const tmpDir = mkdtempSync(join(tmpdir(), 'k5-cli-fail-closed-'));
const nonJsonFile = join(tmpDir, 'non-json.txt');
writeFileSync(nonJsonFile, '便39 委嘱文の抜粋 -- これは JSON ではない {{{ 非構造化テキスト', 'utf8');

const validNinfA = join(ROOT, 'certificates/k5pipeline/toy-ninf-M3-pathA.json');
const validNinfB = join(ROOT, 'certificates/k5pipeline/toy-ninf-M3-pathB.json');
const validNinfBundle = join(ROOT, 'certificates/k5pipeline/toy-ninf-M3-bundle.json');
const validMainA = join(ROOT, 'certificates/k5pipeline/K3-regression-u-pathA.json');
const validMainB = join(ROOT, 'certificates/k5pipeline/K3-regression-u-pathB.json');
const validMainBundle = join(ROOT, 'certificates/k5fixture/K3-regression-model.json');

// 裁定41/便40 F2.2: 正当 pathA raw 全体を clone し、狙った 1 field だけを
// malformed rational へ書き換える(id/M/schema/その他フィールドはすべて
// 正当なまま保つ -- 実際に strict rational parser gate へ到達させるため)。
const badRationalNinfFile = join(tmpDir, 'bad-rational-ninf.json');
{
  const cloned = JSON.parse(readFileSync(validNinfA, 'utf8'));
  cloned.chat = 'not-a-number';
  writeFileSync(badRationalNinfFile, JSON.stringify(cloned), 'utf8');
}
const badRationalMainFile = join(tmpDir, 'bad-rational-main.json');
{
  const cloned = JSON.parse(readFileSync(validMainA, 'utf8'));
  cloned.u_pathA = '1/0';
  writeFileSync(badRationalMainFile, JSON.stringify(cloned), 'utf8');
}

function run(script, args) {
  return spawnSync(NODE, [join(ROOT, 'crosscheck', script), ...args], { encoding: 'utf8', cwd: ROOT });
}
// 裁定41/便40 F2.2: r.error(spawn 自体の失敗)・r.stdout/r.stderr が
// string でない(この管理下 Windows セッションで観測された EPERM 相当の
// 症状)を明示的に検出し、以降の r.stdout.length 等の無条件参照で crash
// しないようにする。呼び出し側は戻り値の `envFail` を見て分岐すること。
function safeRun(script, args) {
  const r = run(script, args);
  if (r.error || typeof r.stdout !== 'string' || typeof r.stderr !== 'string') {
    return { envFail: true, raw: r, reason: r.error ? String(r.error) : `stdout/stderr not captured as string (status=${r.status})` };
  }
  return { envFail: false, status: r.status, stdout: r.stdout, stderr: r.stderr };
}

for (const [label, script, argsWithBad] of [
  ['u-compare-ninf.mjs (N_infty)', 'u-compare-ninf.mjs', [nonJsonFile, validNinfB, validNinfBundle]],
  ['u-compare.mjs (main)', 'u-compare.mjs', [nonJsonFile, validMainB, validMainBundle]],
]) {
  const r = safeRun(script, argsWithBad);
  if (r.envFail) { reportEnvFail(`裁定40 F1.3: ${label} -- 非 JSON な第一引数`, r.reason); continue; }
  report(
    `裁定40 F1.3: ${label} -- 非 JSON な第一引数は非零 exit する`,
    r.status !== 0,
    `exit=${r.status} stdout.length=${r.stdout.length}`
  );
  report(
    `裁定40 F1.3: ${label} -- 非 JSON な第一引数で stdout は空(無出力・exit 0 の fail-open が再現しない)`,
    r.stdout.length === 0,
    `stdout=${JSON.stringify(r.stdout)}`
  );
  report(
    `裁定40 F1.3: ${label} -- 非 JSON な第一引数で stderr に INTEGRITY_STOP メッセージが出る`,
    r.stderr.includes('INTEGRITY_STOP'),
    `stderr(先頭200字)=${JSON.stringify(r.stderr.slice(0, 200))}`
  );
}

// ---- malformed rational (裁定41/便40 F2.2 修理: 正当な pathA raw を clone
// し、狙った 1 field だけを malformed rational に書き換えたもの -- 旧版の
// `{id:'x',...}` は正当 pathB と id が食い違い、実際の停止理由が
// `id mismatch` であって parser gate に到達していなかった。本版は stdout の
// JSON report を実際に parse し、到達した停止理由が strict rational parser
// であることを assert する)。両 checker(main/N_infty)で確認する。----
{
  const r = safeRun('u-compare-ninf.mjs', [badRationalNinfFile, validNinfB, validNinfBundle]);
  if (r.envFail) {
    reportEnvFail('裁定41 F2.2: u-compare-ninf.mjs -- malformed rational (chat)', r.reason);
  } else {
    report(
      '裁定41 F2.2: u-compare-ninf.mjs -- malformed rational chat="not-a-number"(clone された正当 raw の 1 field だけ改変)は非零 exit する',
      r.status !== 0,
      `exit=${r.status}`
    );
    let reachedParserGate = false;
    try {
      const parsed = JSON.parse(r.stdout);
      reachedParserGate = parsed.result === 'INTEGRITY_STOP' && /strict rational parser/.test(parsed.reason || '');
    } catch { /* stdout not JSON -- reachedParserGate stays false, reported as FAIL below */ }
    report(
      '裁定41 F2.2: u-compare-ninf.mjs -- 停止理由が strict rational parser gate であることを assert(id mismatch 等の無関係な理由で止まっていない)',
      reachedParserGate,
      `stdout(先頭300字)=${JSON.stringify(r.stdout.slice(0, 300))}`
    );
  }
}
{
  const r = safeRun('u-compare.mjs', [badRationalMainFile, validMainB, validMainBundle]);
  if (r.envFail) {
    reportEnvFail('裁定41 F2.2: u-compare.mjs -- malformed rational (u_pathA="1/0")', r.reason);
  } else {
    report(
      '裁定41 F2.2: u-compare.mjs -- malformed rational u_pathA="1/0"(clone された正当 raw の 1 field だけ改変)は非零 exit する',
      r.status !== 0,
      `exit=${r.status}`
    );
    let reachedParserGate = false;
    try {
      const parsed = JSON.parse(r.stdout);
      reachedParserGate = parsed.result === 'INTEGRITY_STOP' && /strict rational parser/.test(parsed.reason || '');
    } catch { /* stdout not JSON -- reachedParserGate stays false, reported as FAIL below */ }
    report(
      '裁定41 F2.2: u-compare.mjs -- 停止理由が strict rational parser gate であることを assert(id mismatch 等の無関係な理由で止まっていない)',
      reachedParserGate,
      `stdout(先頭300字)=${JSON.stringify(r.stdout.slice(0, 300))}`
    );
  }
}

// ---- sanity: unmodified valid CLI invocation still exits 0 with ACCEPT (proves
// the above failures are caused by the malformed input, not a general CLI break) ----
{
  const r = safeRun('u-compare-ninf.mjs', [validNinfA, validNinfB, validNinfBundle]);
  if (r.envFail) {
    reportEnvFail('sanity: u-compare-ninf.mjs -- 正当な入力', r.reason);
  } else {
    report(
      'sanity: u-compare-ninf.mjs -- 正当な入力では exit 0 かつ stdout に ACCEPT が出る(CLI 自体は無傷)',
      r.status === 0 && r.stdout.includes('"result": "ACCEPT"'),
      `exit=${r.status}`
    );
  }
}
{
  const r = safeRun('u-compare.mjs', [validMainA, validMainB, validMainBundle]);
  if (r.envFail) {
    reportEnvFail('sanity: u-compare.mjs -- 正当な入力', r.reason);
  } else {
    report(
      'sanity: u-compare.mjs -- 正当な入力では exit 0 かつ stdout に ACCEPT が出る(CLI 自体は無傷)',
      r.status === 0 && r.stdout.includes('"result": "ACCEPT"'),
      `exit=${r.status}`
    );
  }
}

rmSync(tmpDir, { recursive: true, force: true });

console.log(`\n=== ${pass}/${pass + fail} PASS ===${envFail > 0 ? ` (${envFail} 件は ENV_FAIL -- calibration PASS/FAIL に含めない。crosscheck/check-cli-fail-closed.ps1 で代替実行すること)` : ''}`);
if (fail > 0) process.exitCode = 1;
