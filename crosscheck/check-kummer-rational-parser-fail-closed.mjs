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
// pure function ではなく実 CLI 出力を検査する。これらのファイルはトップ
// レベルの直書きスクリプトであり、compareMain/compareNinf のような export
// された純関数を持たないため)。
//
// 実行: node crosscheck/check-kummer-rational-parser-fail-closed.mjs

import { spawnSync } from 'node:child_process';
import { writeFileSync, readFileSync, mkdtempSync, rmSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const NODE = process.execPath;

let pass = 0, fail = 0;
function report(name, ok, extra = '') {
  if (ok) { pass++; console.log(`[PASS] ${name}${extra ? '  ' + extra : ''}`); }
  else { fail++; console.log(`[FAIL] ${name}${extra ? '  ' + extra : ''}`); }
}

function run(script, args) {
  return spawnSync(NODE, [join(ROOT, 'crosscheck', script), ...args], { encoding: 'utf8', cwd: ROOT });
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
  const r = run('check-kummer.mjs', [validKummerU]);
  report('sanity: check-kummer.mjs on K3-regression-kummer-u.json still MATCH', r.status === 0 && r.stdout.includes('"result": "MATCH"'), `exit=${r.status}`);
}
{
  const r = run('check-kummer.mjs', [validKummerUinv]);
  report('sanity: check-kummer.mjs on K3-regression-kummer-uinv.json still MATCH', r.status === 0 && r.stdout.includes('"result": "MATCH"'), `exit=${r.status}`);
}
{
  const r = run('check-kummer-cov3.mjs', [validCov3]);
  report('sanity: check-kummer-cov3.mjs on retracted/K3-regression-kummer-cov3.v1.json still MATCH', r.status === 0 && r.stdout.includes('"result": "MATCH"'), `exit=${r.status}`);
}

// ---- attack: w="0/0" ----
{
  const f = cloneAndMutate(validKummerU, (o) => { o.w = '0/0'; }, 'kummer-w-00.json');
  const r = run('check-kummer.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  report('攻撃: check-kummer.mjs w="0/0" は strict rational parser gate で拒否される', r.status !== 0 && stopped, `exit=${r.status}`);
}
{
  const f = cloneAndMutate(validCov3, (o) => { o.w = '0/0'; }, 'cov3-w-00.json');
  const r = run('check-kummer-cov3.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  report('攻撃: check-kummer-cov3.mjs w="0/0" は strict rational parser gate で拒否される', r.status !== 0 && stopped, `exit=${r.status}`);
}

// ---- attack: w="1/0" ----
{
  const f = cloneAndMutate(validKummerU, (o) => { o.w = '1/0'; }, 'kummer-w-10.json');
  const r = run('check-kummer.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  report('攻撃: check-kummer.mjs w="1/0" は strict rational parser gate で拒否される', r.status !== 0 && stopped, `exit=${r.status}`);
}
{
  const f = cloneAndMutate(validCov3, (o) => { o.w = '1/0'; }, 'cov3-w-10.json');
  const r = run('check-kummer-cov3.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  report('攻撃: check-kummer-cov3.mjs w="1/0" は strict rational parser gate で拒否される', r.status !== 0 && stopped, `exit=${r.status}`);
}

// ---- attack: witness coefficient = "1/2/3" (two or more '/') ----
{
  const f = cloneAndMutate(validKummerU, (o) => { o.witness_coeffs_basis_powers_of_root = ['0', '1/2/3', '0', '-2']; }, 'kummer-witness-123.json');
  const r = run('check-kummer.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  report('攻撃: check-kummer.mjs witness_coeffs 中の "1/2/3"(二本以上の "/")は全文 grammar 違反として拒否される', r.status !== 0 && stopped, `exit=${r.status}`);
}
{
  const f = cloneAndMutate(validCov3, (o) => { o.witness_coeffs_basis_powers_of_root = ['0', '1/2/3', '0', '-2']; }, 'cov3-witness-123.json');
  const r = run('check-kummer-cov3.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  report('攻撃: check-kummer-cov3.mjs witness_coeffs 中の "1/2/3"(二本以上の "/")は全文 grammar 違反として拒否される', r.status !== 0 && stopped, `exit=${r.status}`);
}

// ============================================================================
// 司令塔独自攻撃(裁定41続報): trim() 除去攻撃を check-kummer 系にも横展開。
// ============================================================================
{
  const f = cloneAndMutate(validKummerU, (o) => { o.w = ' -4'; }, 'kummer-w-leadingspace.json');
  const r = run('check-kummer.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  report('司令塔独自攻撃: check-kummer.mjs w=" -4"(先頭空白)は拒否される', r.status !== 0 && stopped, `exit=${r.status}`);
}
{
  const f = cloneAndMutate(validCov3, (o) => { o.w = '-4 '; }, 'cov3-w-trailingspace.json');
  const r = run('check-kummer-cov3.mjs', [f]);
  let stopped = false;
  try { const p = JSON.parse(r.stdout); stopped = p.result === 'INTEGRITY_STOP' && /strict rational parser/.test(p.reason || ''); } catch {}
  report('司令塔独自攻撃: check-kummer-cov3.mjs w="-4 "(末尾空白)は拒否される', r.status !== 0 && stopped, `exit=${r.status}`);
}

rmSync(tmpDir, { recursive: true, force: true });

console.log(`\n=== ${pass}/${pass + fail} PASS ===`);
if (fail > 0) process.exitCode = 1;
