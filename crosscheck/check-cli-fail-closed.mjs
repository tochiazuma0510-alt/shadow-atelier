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
// ============================================================================
// 裁定42/便41 F4.2-F4.3 対応(本ファイルの主眼): 保存 harness 自体の false
// green を根絶する。
//
// Sol が管理下 Windows セッションで実測した症状: この環境では nested な
// node 子プロセスの spawnSync が EPERM 等で失敗し、旧版は
//   - 6 件すべてが envFail (spawnSync 使用不能) として扱われる
//   - pass=0, fail=0 のまま "=== 0/0 PASS ===" と表示
//   - 末尾が `if (fail > 0) process.exitCode = 1;` だけなので exit 0
// という「何も測っていないのに green に見える」状態になっていた。
//
// 本版の修理:
//   1. spawnSync が使えない(EPERM 等で envFail 判定になる)場合、
//      各ケースについて**その場で in-process fallback** に自動切替する。
//      u-compare.mjs / u-compare-ninf.mjs は便41 対応で純関数
//      runCliCore(argv) を export するようになった(副作用なし・
//      readFileSync + compareMain/compareNinf 呼び出し + report/exitCode を
//      返すだけ)。fallback はこの runCliCore を子プロセスを介さず直接呼ぶ
//      ことで、"non-JSON arg1 は INTEGRITY_STOP になる" 等の判定ロジックを
//      実際に exercise する。fallback したケースは [FALLBACK:in-process] と
//      明記し、実行数・PASS/FAIL に正しく算入する(見なかったことにしない)。
//   2. ただし fallback は「OS プロセスとして実際に node が起動し、
//      process.exit/console.log の薄い CLI wrapper が正しく機能するか」
//      という**真に CLI プロセス固有の挙動**までは検査できない
//      (in-process 呼び出しは同一プロセス内の関数呼び出しであり、実際の
//      exit code や stdout バイト列を OS 経由で観測していない)。この
//      残差は各グループにつき一件、明示的な [ENV_LIMIT] として SKIP 扱いに
//      し、PASS には数えない(黙って PASS に混ぜない)。
//   3. 実行ケース数(spawn 実測 + in-process fallback で確定した判定数)が
//      期待値(このファイルが定義する 12 件)と厳密に一致することを assert
//      する。0 件はもちろん、11 件・13 件でも非零 exit + 構造化
//      {"status":"ENV_FAIL"} を stdout に出す(0 件実行のまま exit 0 という
//      false green を再発させない)。
//
// 実行: node crosscheck/check-cli-fail-closed.mjs
//   (PowerShell fallback: powershell -File crosscheck/check-cli-fail-closed.ps1)

import { spawnSync } from 'node:child_process';
import { writeFileSync, readFileSync, mkdtempSync, rmSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { tmpdir } from 'node:os';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const NODE = process.execPath;

// このファイルが定義する「較正が実際に何かを測った」とみなすケース総数。
// F5.1(裁定42 再申請要件 1): 「期待検査数が厳密に 12」を assert する。
const EXPECTED_CASES = 12;

let pass = 0, fail = 0;
let fellBack = 0; // このうち in-process fallback で判定した件数(内訳表示用)
let envLimit = 0; // 真の CLI プロセス挙動固有で in-process では検査不能だった件数(SKIP・PASSに数えない)
function report(name, ok, extra = '') {
  if (ok) { pass++; console.log(`[PASS] ${name}${extra ? '  ' + extra : ''}`); }
  else { fail++; console.log(`[FAIL] ${name}${extra ? '  ' + extra : ''}`); }
}
function reportFallback(name, ok, extra = '') {
  fellBack++;
  if (ok) { pass++; console.log(`[PASS][FALLBACK:in-process] ${name}${extra ? '  ' + extra : ''}`); }
  else { fail++; console.log(`[FAIL][FALLBACK:in-process] ${name}${extra ? '  ' + extra : ''}`); }
}
function reportEnvLimit(name, reason) {
  envLimit++;
  console.log(`[ENV_LIMIT] ${name} -- 真の CLI プロセス挙動(OS exit code / stdout バイト列)は in-process fallback では検査できない: ${reason} (SKIP。PASS には数えない)`);
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

// 裁定42/便41 F4.2 対応: spawnSync が使えない環境向けの in-process fallback。
// u-compare.mjs / u-compare-ninf.mjs の副作用なし runCliCore(argv) を直接
// import して呼ぶ(子プロセスを立てない)。戻り値の形は safeRun() の非
// envFail ケースと揃えてある({ envFail:false, status, stdout, stderr }) の
// で、以降の判定コードを spawn/fallback で共有できる。
const coreModules = {
  'u-compare-ninf.mjs': await import(pathToFileURL(join(ROOT, 'crosscheck', 'u-compare-ninf.mjs')).href),
  'u-compare.mjs': await import(pathToFileURL(join(ROOT, 'crosscheck', 'u-compare.mjs')).href),
};
function fallbackRun(script, args) {
  const mod = coreModules[script];
  const r = mod.runCliCore(args);
  return { envFail: false, status: r.exitCode, stdout: r.stdout, stderr: r.stderr };
}
// spawn を試み、envFail なら in-process fallback に自動切替する。戻り値に
// usedFallback を付与して呼び出し側が表示を分けられるようにする。
// spawn・fallback が両方とも使えない(fallback 自体が例外を投げる)場合は
// crashed:true を返し、呼び出し側はこのケースを pass にも fail にも数え
// ない(=executed が EXPECTED_CASES 未満になり、末尾の厳密一致 assert が
// 機械的に ENV_FAIL を発報する。crash を握り潰して 0/0 green にしない)。
function runWithFallback(script, args) {
  const spawned = safeRun(script, args);
  if (!spawned.envFail) return { ...spawned, usedFallback: false };
  try {
    const fb = fallbackRun(script, args);
    return { ...fb, usedFallback: true, spawnEnvFailReason: spawned.reason };
  } catch (e) {
    return { crashed: true, spawnEnvFailReason: spawned.reason, fallbackError: e && e.stack ? e.stack : String(e) };
  }
}
// 呼び出し元は spawn/fallback どちらの経路でも同じ report()/reportFallback()
// で結果を記録できるよう、r.usedFallback を見て振り分けるヘルパー。
// r.crashed の場合はこのケースの assertion 自体を実行不能として扱い、
// pass/fail どちらにも数えない(executed カウントを意図的に減らす)。
function reportEither(name, r, ok, extra = '') {
  if (r.crashed) {
    console.log(`[ENV_FAIL] ${name} -- spawnSync envFail (${r.spawnEnvFailReason}) かつ in-process fallback も例外で失敗: ${r.fallbackError} (このケースは pass/fail いずれにも数えない -- 実行不能)`);
    return;
  }
  if (r.usedFallback) reportFallback(`${name} (spawnSync envFail: ${r.spawnEnvFailReason})`, ok, extra);
  else report(name, ok, extra);
}

for (const [label, script, argsWithBad] of [
  ['u-compare-ninf.mjs (N_infty)', 'u-compare-ninf.mjs', [nonJsonFile, validNinfB, validNinfBundle]],
  ['u-compare.mjs (main)', 'u-compare.mjs', [nonJsonFile, validMainB, validMainBundle]],
]) {
  const r = runWithFallback(script, argsWithBad);
  reportEither(
    `裁定40 F1.3: ${label} -- 非 JSON な第一引数は非零 exit する`,
    r, r.status !== 0, `exit=${r.status} stdout.length=${r.stdout?.length}`
  );
  reportEither(
    `裁定40 F1.3: ${label} -- 非 JSON な第一引数で stdout は空(無出力・exit 0 の fail-open が再現しない)`,
    r, r.stdout?.length === 0, `stdout=${JSON.stringify(r.stdout)}`
  );
  reportEither(
    `裁定40 F1.3: ${label} -- 非 JSON な第一引数で stderr に INTEGRITY_STOP メッセージが出る`,
    r, !!r.stderr?.includes('INTEGRITY_STOP'), `stderr(先頭200字)=${JSON.stringify(r.stderr?.slice(0, 200))}`
  );
  if (r.usedFallback) {
    reportEnvLimit(`裁定40 F1.3: ${label} -- 実 OS プロセスとしての exit code/stdout(spawnSync 経路)`,
      'in-process fallback は runCliCore の戻り値を直接検査しており、実際の子プロセス起動・process.exit・OS stdout 捕捉は exercise していない');
  }
}

// ---- malformed rational (裁定41/便40 F2.2 修理: 正当な pathA raw を clone
// し、狙った 1 field だけを malformed rational に書き換えたもの -- 旧版の
// `{id:'x',...}` は正当 pathB と id が食い違い、実際の停止理由が
// `id mismatch` であって parser gate に到達していなかった。本版は stdout の
// JSON report を実際に parse し、到達した停止理由が strict rational parser
// であることを assert する。両 checker(main/N_infty)で確認する。----
{
  const r = runWithFallback('u-compare-ninf.mjs', [badRationalNinfFile, validNinfB, validNinfBundle]);
  reportEither(
    '裁定41 F2.2: u-compare-ninf.mjs -- malformed rational chat="not-a-number"(clone された正当 raw の 1 field だけ改変)は非零 exit する',
    r, r.status !== 0, `exit=${r.status}`
  );
  let reachedParserGate = false;
  try {
    const parsed = JSON.parse(r.stdout);
    reachedParserGate = parsed.result === 'INTEGRITY_STOP' && /strict rational parser/.test(parsed.reason || '');
  } catch { /* stdout not JSON -- reachedParserGate stays false, reported as FAIL below */ }
  reportEither(
    '裁定41 F2.2: u-compare-ninf.mjs -- 停止理由が strict rational parser gate であることを assert(id mismatch 等の無関係な理由で止まっていない)',
    r, reachedParserGate, `stdout(先頭300字)=${JSON.stringify(r.stdout?.slice(0, 300))}`
  );
}
{
  const r = runWithFallback('u-compare.mjs', [badRationalMainFile, validMainB, validMainBundle]);
  reportEither(
    '裁定41 F2.2: u-compare.mjs -- malformed rational u_pathA="1/0"(clone された正当 raw の 1 field だけ改変)は非零 exit する',
    r, r.status !== 0, `exit=${r.status}`
  );
  let reachedParserGate = false;
  try {
    const parsed = JSON.parse(r.stdout);
    reachedParserGate = parsed.result === 'INTEGRITY_STOP' && /strict rational parser/.test(parsed.reason || '');
  } catch { /* stdout not JSON -- reachedParserGate stays false, reported as FAIL below */ }
  reportEither(
    '裁定41 F2.2: u-compare.mjs -- 停止理由が strict rational parser gate であることを assert(id mismatch 等の無関係な理由で止まっていない)',
    r, reachedParserGate, `stdout(先頭300字)=${JSON.stringify(r.stdout?.slice(0, 300))}`
  );
}

// ---- sanity: unmodified valid CLI invocation still exits 0 with ACCEPT (proves
// the above failures are caused by the malformed input, not a general CLI break) ----
{
  const r = runWithFallback('u-compare-ninf.mjs', [validNinfA, validNinfB, validNinfBundle]);
  reportEither(
    'sanity: u-compare-ninf.mjs -- 正当な入力では exit 0 かつ stdout に ACCEPT が出る(CLI 自体は無傷)',
    r, r.status === 0 && !!r.stdout?.includes('"result": "ACCEPT"'), `exit=${r.status}`
  );
}
{
  const r = runWithFallback('u-compare.mjs', [validMainA, validMainB, validMainBundle]);
  reportEither(
    'sanity: u-compare.mjs -- 正当な入力では exit 0 かつ stdout に ACCEPT が出る(CLI 自体は無傷)',
    r, r.status === 0 && !!r.stdout?.includes('"result": "ACCEPT"'), `exit=${r.status}`
  );
}

rmSync(tmpDir, { recursive: true, force: true });

const executed = pass + fail;
console.log(`\n=== ${pass}/${executed} PASS ===${fellBack > 0 ? ` (うち ${fellBack} 件は in-process fallback で実行)` : ''}${envLimit > 0 ? ` (${envLimit} 件は ENV_LIMIT/SKIP -- 別枠。PASSに含めない)` : ''}`);

// 裁定42/便41 F5.1 対応: 「実行ケース数 > 0」だけでなく「期待検査数と厳密に
// 一致」まで assert する(0 件はもちろん、11 件・13 件でも false green
// ではないことを機械的に保証する)。
if (executed !== EXPECTED_CASES) {
  console.log(JSON.stringify({
    status: 'ENV_FAIL',
    reason: `executed case count (${executed}) does not equal expected (${EXPECTED_CASES}) -- this harness measured nothing or an unexpected subset, and must not be reported as a passing calibration`,
    executed, expected: EXPECTED_CASES, pass, fail, fellBack, envLimit,
  }));
  process.exitCode = 1;
} else if (fail > 0) {
  process.exitCode = 1;
}
