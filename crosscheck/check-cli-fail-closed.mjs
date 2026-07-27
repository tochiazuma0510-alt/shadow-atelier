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
// 実測上の注意(便38 F1.2 の教訓): この管理下 Windows セッションでは、
// ある node プロセスが nested に子 node プロセスを spawn すると stdout
// 捕捉が EPERM で拒まれることがあった(check-r7-bundle-attack.mjs の旧版で
// 遭遇)。本ファイル自体は「node crosscheck/check-cli-fail-closed.mjs」として
// **トップレベルから直接実行される**ことを想定しており(ネストではない)、
// 内部で spawn する子 process は一段のみである。もし将来 EPERM が再発したら、
// このファイルではなく PowerShell/bash から直接 `node u-compare*.mjs <args>`
// を叩いて $LASTEXITCODE を確認すること(このファイルのコメントに記録)。
//
// 実行: node crosscheck/check-cli-fail-closed.mjs

import { spawnSync } from 'node:child_process';
import { writeFileSync, unlinkSync, mkdtempSync, rmSync } from 'node:fs';
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

const tmpDir = mkdtempSync(join(tmpdir(), 'k5-cli-fail-closed-'));
const nonJsonFile = join(tmpDir, 'non-json.txt');
const badRationalFile = join(tmpDir, 'bad-rational.json');
writeFileSync(nonJsonFile, '便39 委嘱文の抜粋 -- これは JSON ではない {{{ 非構造化テキスト', 'utf8');
// valid JSON, but a field that later BigInt()-parsing chokes on (not a valid rational string)
writeFileSync(badRationalFile, JSON.stringify({ id: 'x', branch: 'N_infty', M: 3, chat: 'not-a-number' }), 'utf8');

const validNinfA = join(ROOT, 'certificates/k5pipeline/toy-ninf-M3-pathA.json');
const validNinfB = join(ROOT, 'certificates/k5pipeline/toy-ninf-M3-pathB.json');
const validNinfBundle = join(ROOT, 'certificates/k5pipeline/toy-ninf-M3-bundle.json');
const validMainA = join(ROOT, 'certificates/k5pipeline/K3-regression-u-pathA.json');
const validMainB = join(ROOT, 'certificates/k5pipeline/K3-regression-u-pathB.json');
const validMainBundle = join(ROOT, 'certificates/k5fixture/K3-regression-model.json');

function run(script, args) {
  return spawnSync(NODE, [join(ROOT, 'crosscheck', script), ...args], { encoding: 'utf8', cwd: ROOT });
}

for (const [label, script, argsWithBad] of [
  ['u-compare-ninf.mjs (N_infty)', 'u-compare-ninf.mjs', [nonJsonFile, validNinfB, validNinfBundle]],
  ['u-compare.mjs (main)', 'u-compare.mjs', [nonJsonFile, validMainB, validMainBundle]],
]) {
  const r = run(script, argsWithBad);
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

// ---- malformed rational (valid JSON, but chat field is not a valid rational
// string once compareNinf's parseRat/BigInt tries to parse it) ----
{
  const r = run('u-compare-ninf.mjs', [badRationalFile, validNinfB, validNinfBundle]);
  report(
    '裁定40 F1.3: u-compare-ninf.mjs -- 不正な有理数値(BigInt 変換不能)を含む JSON も非零 exit する',
    r.status !== 0,
    `exit=${r.status}`
  );
}

// ---- sanity: unmodified valid CLI invocation still exits 0 with ACCEPT (proves
// the above failures are caused by the malformed input, not a general CLI break) ----
{
  const r = run('u-compare-ninf.mjs', [validNinfA, validNinfB, validNinfBundle]);
  report(
    'sanity: u-compare-ninf.mjs -- 正当な入力では exit 0 かつ stdout に ACCEPT が出る(CLI 自体は無傷)',
    r.status === 0 && r.stdout.includes('"result": "ACCEPT"'),
    `exit=${r.status}`
  );
}
{
  const r = run('u-compare.mjs', [validMainA, validMainB, validMainBundle]);
  report(
    'sanity: u-compare.mjs -- 正当な入力では exit 0 かつ stdout に ACCEPT が出る(CLI 自体は無傷)',
    r.status === 0 && r.stdout.includes('"result": "ACCEPT"'),
    `exit=${r.status}`
  );
}

rmSync(tmpDir, { recursive: true, force: true });

console.log(`\n=== ${pass}/${pass + fail} PASS ===`);
if (fail > 0) process.exitCode = 1;
