#!/usr/bin/env node
// crosscheck/check-kummer-rational-parser-fail-closed.mjs -- 司令塔追加委嘱
// (裁定41対応中・Sol 便40 F1.2 の水準を crosscheck/check-kummer.mjs /
// crosscheck/check-kummer-cov3.mjs へ横展開)の adversarial 較正。
//
// 背景: check-kummer.mjs / check-kummer-cov3.mjs の `parseRatMaybeNumber` は
// u-compare.mjs / u-compare-ninf.mjs の旧 parseRat と同じ穴を持っていた
// (`str.split('/')` のみで分母 0 を拒否せず、"1/2/3" のような二本以上の
// '/' も黙って先頭 2 要素だけを読んでいた)。両ファイルを同じ strict
// grammar(全文一致・分母 0 拒否・d>0 invariant・malformed は structured
// INTEGRITY_STOP)へ硬化したので、ここでその拒否と、既存の正当較正
// (MATCH)が無傷であることを両方確認する。
//
// この checker は check-kummer.mjs/check-kummer-cov3.mjs を子プロセスとして
// 実際に CLI 経由で叩く(check-cli-fail-closed.mjs と同じ方針: import した
// pure function ではなく実 CLI 出力を検査する)。
//
// ============================================================================
// 裁定42/便41 F4.2 対応: 保存 harness の false green 根絶。
//
// Sol の管理下環境での実測: この管理下 Windows セッションでは子 node の
// spawnSync が EPERM となり、旧版は 0/11, exit 1 だった(exit 自体は非零
// だったので「静かな green」ではなかったが、「0 件実行のまま止まった」
// ことが構造化されておらず、単なる「11 件 FAIL」に見えて false negative の
// 印象を与えていた -- 実際は「何も測れていない」のであって「不一致だった」
// のではない)。
//
// 本版は check-cli-fail-closed.mjs と同じ修理を適用する:
//   1. 裁定42/便41 で check-kummer.mjs / check-kummer-cov3.mjs が
//      export するようになった副作用なし runCliCore(argv) を、spawnSync が
//      envFail になった場合に in-process で直接呼ぶ(fallback したことを
//      [FALLBACK:in-process] と明記)。
//   2. spawn・fallback の両方が失敗した(=真に 0 件実行)ケースは pass/fail
//      いずれにも数えず、末尾で「実行ケース数 == 期待件数(9)」の厳密一致を
//      assert して構造化 ENV_FAIL + 非零 exit にする(0/0 や不完全な件数の
//      まま green を返さない)。
//   3. 実 OS プロセスとしての exit code/stdout 捕捉そのもの(fallback では
//      exercise できない)は ENV_LIMIT として明示 SKIP する(PASS に混ぜない)。
//
// 実行: node crosscheck/check-kummer-rational-parser-fail-closed.mjs

import { spawnSync } from 'node:child_process';
import { writeFileSync, readFileSync, mkdtempSync, rmSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { tmpdir } from 'node:os';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const NODE = process.execPath;

// このファイルが定義する期待実行ケース数(下記のブロック数を数えたもの:
// sanity 3 + attack 6(w=0/0 x2, w=1/0 x2, witness 1/2/3 x2)
// + 司令塔独自攻撃 2 = 11)。裁定42/便41 再申請要件 1 の「期待検査数の厳密
// 一致 assert」を、check-cli-fail-closed.mjs と同水準でここにも適用する。
const EXPECTED_CASES = 11;

let pass = 0, fail = 0;
let fellBack = 0;
let envLimit = 0;
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
  console.log(`[ENV_LIMIT] ${name} -- 真の CLI プロセス挙動は in-process fallback では検査できない: ${reason} (SKIP。PASS には数えない)`);
}

function run(script, args) {
  return spawnSync(NODE, [join(ROOT, 'crosscheck', script), ...args], { encoding: 'utf8', cwd: ROOT });
}
function safeRun(script, args) {
  const r = run(script, args);
  if (r.error || typeof r.stdout !== 'string' || typeof r.stderr !== 'string') {
    return { envFail: true, raw: r, reason: r.error ? String(r.error) : `stdout/stderr not captured as string (status=${r.status})` };
  }
  return { envFail: false, status: r.status, stdout: r.stdout, stderr: r.stderr };
}

// 裁定42/便41 対応: check-kummer.mjs / check-kummer-cov3.mjs の副作用なし
// runCliCore(argv) を in-process fallback 用に import する。
const coreModules = {
  'check-kummer.mjs': await import(pathToFileURL(join(ROOT, 'crosscheck', 'check-kummer.mjs')).href),
  'check-kummer-cov3.mjs': await import(pathToFileURL(join(ROOT, 'crosscheck', 'check-kummer-cov3.mjs')).href),
};
function fallbackRun(script, args) {
  const mod = coreModules[script];
  const r = mod.runCliCore(args);
  return { envFail: false, status: r.exitCode, stdout: r.stdout, stderr: r.stderr };
}
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
function reportEither(name, r, ok, extra = '') {
  if (r.crashed) {
    console.log(`[ENV_FAIL] ${name} -- spawnSync envFail (${r.spawnEnvFailReason}) かつ in-process fallback も例外で失敗: ${r.fallbackError} (このケースは pass/fail いずれにも数えない -- 実行不能)`);
    return;
  }
  if (r.usedFallback) reportFallback(`${name} (spawnSync envFail: ${r.spawnEnvFailReason})`, ok, extra);
  else report(name, ok, extra);
}
function noteEnvLimitIfFellBack(name, r) {
  if (r.usedFallback) {
    reportEnvLimit(`${name} -- 実 OS プロセスとしての exit code/stdout(spawnSync 経路)`,
      'in-process fallback は runCliCore の戻り値を直接検査しており、実際の子プロセス起動・process.exit・OS stdout 捕捉は exercise していない');
  }
}

const tmpDir = mkdtempSync(join(tmpdir(), 'k5-kummer-parser-fail-closed-'));

const validKummerU = join(ROOT, 'certificates/k5pipeline/K3-regression-kummer-u.json');
const validKummerUinv = join(ROOT, 'certificates/k5pipeline/K3-regression-kummer-uinv.json');
const validCov3 = join(ROOT, 'certificates/k5pipeline/retracted/K3-regression-kummer-cov3.v1.json');

function cloneAndMutate(srcFile, mutateFn, outName) {
  const obj = JSON.parse(readFileSync(srcFile, 'utf8'));
  mutateFn(obj);
  const outFile = join(tmpDir, outName);
  writeFileSync(outFile, JSON.stringify(obj), 'utf8');
  return outFile;
}

// ---- sanity: existing valid calibrations still MATCH (proves the attacks
// below are caused by the malformed input, not a general regression) ----
{
  const r = runWithFallback('check-kummer.mjs', [validKummerU]);
  reportEither('sanity: check-kummer.mjs on K3-regression-kummer-u.json still MATCH', r, r.status === 0 && !!r.stdout?.includes('"result": "MATCH"'), `exit=${r.status}`);
  noteEnvLimitIfFellBack('sanity: check-kummer.mjs on K3-regression-kummer-u.json', r);
}
{
  const r = runWithFallback('check-kummer.mjs', [validKummerUinv]);
  reportEither('sanity: check-kummer.mjs on K3-regression-kummer-uinv.json still MATCH', r, r.status === 0 && !!r.stdout?.includes('"result": "MATCH"'), `exit=${r.status}`);
  noteEnvLimitIfFellBack('sanity: check-kummer.mjs on K3-regression-kummer-uinv.json', r);
}
{
  const r = runWithFallback('check-kummer-cov3.mjs', [validCov3]);
  reportEither('sanity: check-kummer-cov3.mjs on retracted/K3-regression-kummer-cov3.v1.json still MATCH', r, r.status === 0 && !!r.stdout?.includes('"result": "MATCH"'), `exit=${r.status}`);
  noteEnvLimitIfFellBack('sanity: check-kummer-cov3.mjs on retracted/K3-regression-kummer-cov3.v1.json', r);
}

// ---- attack: w="0/0" ----
{
  const f = cloneAndMutate(validKummerU, (o) => { o.w = '0/0'; }, 'kummer-w-00.json');
  const r = runWithFallback('check-kummer.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  reportEither('攻撃: check-kummer.mjs w="0/0" は strict rational parser gate で拒否される', r, r.status !== 0 && stopped, `exit=${r.status}`);
  noteEnvLimitIfFellBack('攻撃: check-kummer.mjs w="0/0"', r);
}
{
  const f = cloneAndMutate(validCov3, (o) => { o.w = '0/0'; }, 'cov3-w-00.json');
  const r = runWithFallback('check-kummer-cov3.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  reportEither('攻撃: check-kummer-cov3.mjs w="0/0" は strict rational parser gate で拒否される', r, r.status !== 0 && stopped, `exit=${r.status}`);
  noteEnvLimitIfFellBack('攻撃: check-kummer-cov3.mjs w="0/0"', r);
}

// ---- attack: w="1/0" ----
{
  const f = cloneAndMutate(validKummerU, (o) => { o.w = '1/0'; }, 'kummer-w-10.json');
  const r = runWithFallback('check-kummer.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  reportEither('攻撃: check-kummer.mjs w="1/0" は strict rational parser gate で拒否される', r, r.status !== 0 && stopped, `exit=${r.status}`);
  noteEnvLimitIfFellBack('攻撃: check-kummer.mjs w="1/0"', r);
}
{
  const f = cloneAndMutate(validCov3, (o) => { o.w = '1/0'; }, 'cov3-w-10.json');
  const r = runWithFallback('check-kummer-cov3.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  reportEither('攻撃: check-kummer-cov3.mjs w="1/0" は strict rational parser gate で拒否される', r, r.status !== 0 && stopped, `exit=${r.status}`);
  noteEnvLimitIfFellBack('攻撃: check-kummer-cov3.mjs w="1/0"', r);
}

// ---- attack: witness coefficient = "1/2/3" (two or more '/') ----
{
  const f = cloneAndMutate(validKummerU, (o) => { o.witness_coeffs_basis_powers_of_root = ['0', '1/2/3', '0', '-2']; }, 'kummer-witness-123.json');
  const r = runWithFallback('check-kummer.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  reportEither('攻撃: check-kummer.mjs witness_coeffs 中の "1/2/3"(二本以上の "/")は全文 grammar 違反として拒否される', r, r.status !== 0 && stopped, `exit=${r.status}`);
  noteEnvLimitIfFellBack('攻撃: check-kummer.mjs witness_coeffs "1/2/3"', r);
}
{
  const f = cloneAndMutate(validCov3, (o) => { o.witness_coeffs_basis_powers_of_root = ['0', '1/2/3', '0', '-2']; }, 'cov3-witness-123.json');
  const r = runWithFallback('check-kummer-cov3.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  reportEither('攻撃: check-kummer-cov3.mjs witness_coeffs 中の "1/2/3"(二本以上の "/")は全文 grammar 違反として拒否される', r, r.status !== 0 && stopped, `exit=${r.status}`);
  noteEnvLimitIfFellBack('攻撃: check-kummer-cov3.mjs witness_coeffs "1/2/3"', r);
}

// ============================================================================
// 司令塔独自攻撃(裁定41続報): trim() 除去攻撃を check-kummer 系にも横展開。
// ============================================================================
{
  const f = cloneAndMutate(validKummerU, (o) => { o.w = ' -4'; }, 'kummer-w-leadingspace.json');
  const r = runWithFallback('check-kummer.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  reportEither('司令塔独自攻撃: check-kummer.mjs w=" -4"(先頭空白)は拒否される', r, r.status !== 0 && stopped, `exit=${r.status}`);
  noteEnvLimitIfFellBack('司令塔独自攻撃: check-kummer.mjs w=" -4"', r);
}
{
  const f = cloneAndMutate(validCov3, (o) => { o.w = '-4 '; }, 'cov3-w-trailingspace.json');
  const r = runWithFallback('check-kummer-cov3.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  reportEither('司令塔独自攻撃: check-kummer-cov3.mjs w="-4 "(末尾空白)は拒否される', r, r.status !== 0 && stopped, `exit=${r.status}`);
  noteEnvLimitIfFellBack('司令塔独自攻撃: check-kummer-cov3.mjs w="-4 "', r);
}

rmSync(tmpDir, { recursive: true, force: true });

const executed = pass + fail;
console.log(`\n=== ${pass}/${executed} PASS ===${fellBack > 0 ? ` (うち ${fellBack} 件は in-process fallback で実行)` : ''}${envLimit > 0 ? ` (${envLimit} 件は ENV_LIMIT/SKIP -- 別枠。PASSに含めない)` : ''}`);

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
