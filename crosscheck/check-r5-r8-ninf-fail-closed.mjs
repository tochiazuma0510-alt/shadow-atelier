#!/usr/bin/env node
// crosscheck/check-r5-r8-ninf-fail-closed.mjs -- R-5/R-8 の fail-closed 挙動の
// adversarial 自己確認(便 36 F3.2/F6-1,3 の裏付け)。
//
// 目的: 「較正で ACCEPT が出ること」だけでなく「壊れた入力を正しく検出して
// 止まること」も実行して確認する(CLAUDE.md「落ちたケースを見捨てない」・
// 便 36 F1.2「0 解を corruption 扱いしない」の裏側 -- 本物の入力破損は
// 握りつぶさないことの確認)。ここでの各ケースは**意図的に壊した入力**であり、
// throw/エラーが出ることが PASS 条件である(通常の PASS/FAIL 表記と逆になる
// ケースがあるので注意)。
//
// 実行: node crosscheck/check-r5-r8-ninf-fail-closed.mjs

import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadModel, loadModelNinf, extractPathB_Ninf } from './u-extract-pathB-lib.mjs';
import { compareMain } from './u-compare.mjs';
import { compareNinf } from './u-compare-ninf.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

let pass = 0, fail = 0;
function expectThrow(name, fn) {
  try {
    fn();
    console.log(`[FAIL] ${name}: expected a throw, but call succeeded`);
    fail++;
  } catch (e) {
    console.log(`[PASS] ${name}: threw as expected -- ${e.message}`);
    pass++;
  }
}
function expectOk(name, fn) {
  try {
    fn();
    console.log(`[PASS] ${name}: succeeded as expected`);
    pass++;
  } catch (e) {
    console.log(`[FAIL] ${name}: expected success, but threw -- ${e.message}`);
    fail++;
  }
}

// ---- baseline valid M=3 model (chat=1) ----
const validRaw = {
  id: 'toy-ninf-M3',
  branch: 'N_infty',
  M: 3,
  f_coeffs_ascending: ['0', '2', '1', '2', '2', '0', '1'],
  A_coeffs_ascending: ['1', '1', '0', '1'],
  B_coeffs_ascending: ['1'],
  series_length: 20,
  expected_model_digest: '9e5563726c0fbd544ad13e569ed368baaac1ade58d1be1617548e6570cacfe1d',
};

expectOk('R-5 baseline: valid chat=1 model succeeds', () => {
  extractPathB_Ninf(loadModelNinf(validRaw));
});

// ---- (N∞-4): old toy fixture with chat=2 (f constant term -1 instead of 0) ----
expectThrow('R-5 (N∞-4): chat=2 model must be rejected', () => {
  const bad = { ...validRaw, f_coeffs_ascending: ['-1', '2', '1', '2', '2', '0', '1'] };
  extractPathB_Ninf(loadModelNinf(bad));
});

// ---- (N∞-1): wrong deg A ----
expectThrow('R-5 (N∞-1): deg A != M must be rejected', () => {
  const bad = { ...validRaw, A_coeffs_ascending: ['1', '1', '0', '1', '0'] }; // deg 4 != M=3
  extractPathB_Ninf(loadModelNinf(bad));
});

// ---- (N∞-2): b_{M-3} != a_M ----
expectThrow('R-5 (N∞-2): b_{M-3} != a_M must be rejected', () => {
  const bad = { ...validRaw, B_coeffs_ascending: ['2'] }; // b_0=2 != a_3=1
  extractPathB_Ninf(loadModelNinf(bad));
});

// ---- gcd(f,f') not a unit (f has a repeated root: use f=(x-1)^2*(...)) ----
expectThrow('R-5: non-squarefree f must be rejected', () => {
  // f = (x^3-1)^2 = x^6-2x^3+1: monic degree 6, repeated roots at every cube
  // root of unity, so gcd(f,f') has degree 3 (not a unit). A,B unchanged from
  // the valid model (this case is meant to trip the gcd check, not N∞-1/2).
  const bad = { ...validRaw, f_coeffs_ascending: ['1', '0', '0', '-2', '0', '0', '1'] };
  extractPathB_Ninf(loadModelNinf(bad));
});

// ---- I-l: expected_model_digest mismatch must be rejected ----
expectThrow('R-7/I-l: wrong expected_model_digest must be rejected', () => {
  const bad = { ...validRaw, expected_model_digest: '0'.repeat(64) };
  extractPathB_Ninf(loadModelNinf(bad));
});

// ---- I-m: loadModelNinf requires branch === 'N_infty' ----
expectThrow("I-m: loadModelNinf rejects branch != 'N_infty'", () => {
  loadModelNinf({ ...validRaw, branch: 'Weierstrass' });
});
// ---- R-8(便37 F3): loadModelNinf rejects P0_type != 'nonWeierstrass' if given ----
expectThrow("R-8/I-m(便37 F3): loadModelNinf rejects P0_type='Weierstrass' for branch=N_infty (Lemma R1-M0 3.)", () => {
  loadModelNinf({ ...validRaw, P0_type: 'Weierstrass' });
});
expectOk("R-8(便37 F3): loadModelNinf accepts explicit P0_type='nonWeierstrass' for branch=N_infty", () => {
  loadModelNinf({ ...validRaw, P0_type: 'nonWeierstrass' });
});

// ---- R-8/I-m(便 37 F3/裁定 38 修理): loadModel (main, non-Ninf) must not
// fall back to a default on an unknown label, and must keep the global
// `branch` ({W,N_aff,N_infty}) separate from the local `P0_type`
// ({Weierstrass,nonWeierstrass}) ----
const validMainRaw = {
  id: 'dummy', M: 6, branch: 'N_aff', P0_type: 'nonWeierstrass', x0: '0', y0: '1',
  f_coeffs_ascending: ['1', '0', '0', '0', '0', '0', '1'],
  A_coeffs_ascending: ['1'], B_coeffs_ascending: ['1'],
};
expectOk('R-8 baseline: loadModel accepts valid branch=N_aff/P0_type=nonWeierstrass', () => {
  loadModel(validMainRaw);
});
expectOk('R-8 baseline: loadModel accepts valid branch=W/P0_type=nonWeierstrass', () => {
  loadModel({ ...validMainRaw, branch: 'W' });
});
expectThrow('R-8/I-m: loadModel must reject unknown branch label (no silent fallback)', () => {
  loadModel({ ...validMainRaw, branch: 'bogusLabel' });
});
expectThrow('R-8/I-m: loadModel must reject missing branch label (no silent fallback)', () => {
  const { branch, ...rest } = validMainRaw;
  loadModel(rest);
});
expectThrow("R-8/I-m: loadModel must reject branch='N_infty' (wrong loader for that schema)", () => {
  loadModel({ ...validMainRaw, branch: 'N_infty' });
});
expectThrow('R-8/I-m: loadModel must reject unknown P0_type label (no silent fallback)', () => {
  loadModel({ ...validMainRaw, P0_type: 'bogusP0Type' });
});
expectThrow('R-8/I-m: loadModel must reject missing P0_type label (no silent fallback)', () => {
  const { P0_type, ...rest } = validMainRaw;
  loadModel(rest);
});
// 便 37 F3 の核心: branch と P0_type は別軸であり、branch='W' は
// P0_type='nonWeierstrass' を要求する(S5-W 補題 / Rule 1 SS4.1「v1.2 の
// 絞り込み」)。混同していれば branch='W' + P0_type='Weierstrass' が
// 素通りしてしまう -- これを fail-closed に拒否できることを確認する。
expectThrow("R-8/I-m(便37 F3): branch='W' with P0_type='Weierstrass' must be rejected (S5-W consistency; only N_aff may have P0 Weierstrass)", () => {
  loadModel({ ...validMainRaw, branch: 'W', P0_type: 'Weierstrass' });
});
expectOk("R-8(便37 F3): branch='N_aff' with P0_type='Weierstrass' is the only branch allowed to have P0 Weierstrass", () => {
  loadModel({ ...validMainRaw, branch: 'N_aff', P0_type: 'Weierstrass' });
});

// ============================================================================
// 裁定 39/便 38 F2(R-8 schema gate の fail-closed 化): 第三 checker
// (crosscheck/u-compare.mjs / u-compare-ninf.mjs)自体への 5 攻撃。
//
// 便 38 F2.3 が実証したとおり、上の 18 件は crosscheck/u-extract-pathB-lib.mjs
// の loadModel/loadModelNinf(ローダー)の branch/P0_type 分岐だけを検査して
// おり、第三 checker(u-compare.mjs/u-compare-ninf.mjs)の schema 欠落・方向
// 交換・(N∞) の P0_type 欠落・禁止 field 混入・必須 field 欠落は一件も
// 試していなかった(旧第三 checker はこれら 5 攻撃すべてを ACCEPT していた)。
// 本節は保存済みの正当な raw/bundle 証明書(K3 main-path・prod-ninf-M10)を
// 出発点に、便 38 F2.3 と同じ 5 攻撃を実際に compareMain()/compareNinf() へ
// in-process で投入し、INTEGRITY_STOP になることを確認する。
// ============================================================================

function expectStop(name, report) {
  if (report && report.result === 'INTEGRITY_STOP') {
    console.log(`[PASS] ${name}: rejected as expected -- ${report.reason}`);
    pass++;
  } else {
    console.log(`[FAIL] ${name}: expected INTEGRITY_STOP, got ${report ? report.result : report}`);
    fail++;
  }
}
function expectAccept(name, report) {
  if (report && report.result === 'ACCEPT') {
    console.log(`[PASS] ${name}: accepted as expected`);
    pass++;
  } else {
    console.log(`[FAIL] ${name}: expected ACCEPT, got ${report ? report.result + ' -- ' + report.reason : report}`);
    fail++;
  }
}

// ---- fixtures: K3 main-path (schema u-pathA/v3 / u-pathB/v3) ----
const k3A = JSON.parse(readFileSync(join(ROOT, 'certificates/k5pipeline/K3-regression-u-pathA.json'), 'utf8'));
const k3B = JSON.parse(readFileSync(join(ROOT, 'certificates/k5pipeline/K3-regression-u-pathB.json'), 'utf8'));
const k3Bundle = JSON.parse(readFileSync(join(ROOT, 'certificates/k5fixture/K3-regression-model.json'), 'utf8'));

// baseline sanity: unmodified fixtures still ACCEPT (proves the 5 attacks
// below are the *cause* of rejection, not some unrelated fixture drift).
expectAccept('baseline: unmodified K3 main-path raw ACCEPTs', compareMain(k3A, k3B, k3Bundle));

// ---- attack 1: schema field missing (K3 pathA) ----
{
  const { schema, ...badA } = k3A;
  expectStop('攻撃1(main): K3 pathA.schema 欠落は拒否される', compareMain(badA, k3B, k3Bundle));
}

// ---- attack 2: schema names swapped between pathA/pathB (K3) ----
{
  const swappedA = { ...k3A, schema: 'u-pathB/v3' };
  const swappedB = { ...k3B, schema: 'u-pathA/v3' };
  expectStop('攻撃2(main): K3 pathA/pathB の schema 名交換は拒否される', compareMain(swappedA, swappedB, k3Bundle));
}

// ---- fixtures: production (N_infty) (schema u-pathA-ninf/v2 / u-pathB-ninf/v2) ----
const ninfA = JSON.parse(readFileSync(join(ROOT, 'certificates/k5pipeline/prod-ninf-M10-pathA.json'), 'utf8'));
const ninfB = JSON.parse(readFileSync(join(ROOT, 'certificates/k5pipeline/prod-ninf-M10-pathB.json'), 'utf8'));
const ninfBundle = JSON.parse(readFileSync(join(ROOT, 'certificates/k5pipeline/prod-ninf-M10-bundle.json'), 'utf8'));

expectAccept('baseline: unmodified production (N_infty) raw ACCEPTs', compareNinf(ninfA, ninfB, ninfBundle));

// ---- attack 1 (N_infty variant): schema and P0_type both missing ----
{
  const { schema: sA, P0_type: pA, ...badA } = ninfA;
  const { schema: sB, P0_type: pB, ...badB } = ninfB;
  expectStop('攻撃1(N_infty): schema と P0_type の同時欠落は拒否される', compareNinf(badA, badB, ninfBundle));
}

// ---- attack 2 (N_infty variant): schema names swapped between pathA/pathB ----
{
  const swappedA = { ...ninfA, schema: 'u-pathB-ninf/v3' };
  const swappedB = { ...ninfB, schema: 'u-pathA-ninf/v3' };
  expectStop('攻撃2(N_infty): production raw の pathA/pathB schema 名交換は拒否される', compareNinf(swappedA, swappedB, ninfBundle));
}

// ---- attack 3: (N_infty) P0_type missing alone (schema kept intact) ----
{
  const { P0_type, ...badA } = ninfA;
  const { P0_type: p2, ...badB } = ninfB;
  expectStop('攻撃3: production (N_infty) raw の P0_type 欠落は拒否される', compareNinf(badA, badB, ninfBundle));
}

// ---- attack 4: forbidden fields x0/y0 injected into an (N_infty) raw ----
{
  const badA = { ...ninfA, x0: '0', y0: '1' };
  const badB = { ...ninfB, x0: '0', y0: '1' };
  expectStop('攻撃4: production (N_infty) raw への禁止 field x0/y0 混入は拒否される', compareNinf(badA, badB, ninfBundle));
}

// ---- attack 5: required fields a_M/b_Mm3 removed from an (N_infty) raw ----
{
  const { a_M, b_Mm3, ...badA } = ninfA;
  const { a_M: a2, b_Mm3: b2, ...badB } = ninfB;
  expectStop('攻撃5: production (N_infty) raw の必須 field a_M/b_Mm3 欠落は拒否される', compareNinf(badA, badB, ninfBundle));
}

// ---- combined attack (便38 F2.3 悪意入力 5.そのもの): x0/y0 混入 と
// a_M/b_Mm3 欠落を同時に行う ----
{
  const badA = { ...ninfA, x0: '0', y0: '1' };
  delete badA.a_M; delete badA.b_Mm3;
  const badB = { ...ninfB, x0: '0', y0: '1' };
  delete badB.a_M; delete badB.b_Mm3;
  expectStop('便38 F2.3 攻撃5(結合形): x0/y0 混入 + a_M/b_Mm3 欠落の同時攻撃は拒否される', compareNinf(badA, badB, ninfBundle));
}

// ---- extra: independently-recomputed a_M/b_Mm3 must match the declared
// value (not just "field present") -- a forged a_M that disagrees with the
// coefficient list must also be rejected ----
{
  const badA = { ...ninfA, a_M: String(BigInt(ninfA.a_M) + 1n) };
  expectStop('裁定39 F2 追加: a_M の明示値が係数列からの再抽出値と食い違えば拒否される', compareNinf(badA, ninfB, ninfBundle));
}

// ============================================================================
// 裁定40/便39 F1.2: chat の実値矛盾 raw への直接攻撃(Sol 便39 の攻撃そのもの)。
//
// 便39 F1.2 の指摘: 旧 checker は chat_equals_1===true という自己申告
// boolean flag だけを見ており、raw.chat の実値・pathA/pathB 相互一致・
// pathB.N_lambda_coeffs_ascending の値を一度も検査していなかった。Sol は
// 保存済み production raw の chat="2"(かつ B.N_lambda_coeffs_ascending=["2"])
// へ書き換え、chat_equals_1・A/B/f・u・全 digest はそのままにして
// compareNinf() へ直接投入すると ACCEPT することを実証した。この攻撃を
// そのまま再現し、裁定40対応版が INTEGRITY_STOP にすることを確認する。
// ============================================================================
{
  const badA = { ...ninfA, chat: '2' }; // chat_equals_1 は据え置き(true のまま) -- Sol の攻撃どおり
  const badB = { ...ninfB, chat: '2', N_lambda_coeffs_ascending: ['2'] }; // chat_equals_1/N_lambda_is_nonzero_constant も据え置き
  expectStop(
    '裁定40 F1.2 攻撃(Sol 便39 の矛盾 raw 攻撃そのもの): chat="2"(+N_lambda=["2"])は chat_equals_1=true のままでも拒否される',
    compareNinf(badA, badB, ninfBundle)
  );
}
// ---- variant: only pathB's declared chat/N_lambda are corrupted (pathA left alone) ----
{
  const badB2 = { ...ninfB, chat: '2', N_lambda_coeffs_ascending: ['2'] };
  expectStop(
    '裁定40 F1.2 攻撃 variant: pathB.chat="2"(+N_lambda=["2"])のみの矛盾 raw も拒否される(pathA は無傷)',
    compareNinf(ninfA, badB2, ninfBundle)
  );
}
// ---- variant: N_lambda_coeffs_ascending corrupted while chat stays "1" (declared chat and
// declared N(lambda) polynomial disagree with each other) ----
{
  const badB3 = { ...ninfB, N_lambda_coeffs_ascending: ['2'] };
  expectStop(
    '裁定40 F1.2 攻撃 variant: chat="1" のまま N_lambda_coeffs_ascending=["2"] にすると拒否される(宣言値同士の内部矛盾)',
    compareNinf(ninfA, badB3, ninfBundle)
  );
}

// ============================================================================
// 裁定41/便40 F1.2: strict rational parser の adversarial 較正(Sol 便40
// F1.2 の指摘そのもの)。旧 parseRat は分母 0 を拒否せず、交差積等値判定
// (a.n*b.d===b.n*a.d)の下で "0/0" が任意の有理数と等しいと判定され、
// "1/0" 同士も等しいと判定されていた -- u の exact equality という第三
// checker の核心を無効化する攻撃。ここでは正しい保存 raw/bundle の他の
// フィールド・digest は一切変えず、攻撃対象の 1-2 field だけを書き換える。
// ============================================================================

// ---- attack: (N_infty) both chat="0/0" (declared N_lambda=[1] left intact) ----
{
  const badA = { ...ninfA, chat: '0/0' };
  const badB = { ...ninfB, chat: '0/0' };
  expectStop(
    '裁定41 F1.2 攻撃: production (N_infty) 両 chat="0/0" は拒否される(旧交差積判定では 0/0 は任意の値と等値になり得た)',
    compareNinf(badA, badB, ninfBundle)
  );
}

// ---- attack: (N_infty) both a_M=b_Mm3="0/0" ----
{
  const badA = { ...ninfA, a_M: '0/0', b_Mm3: '0/0' };
  const badB = { ...ninfB, a_M: '0/0', b_Mm3: '0/0' };
  expectStop(
    '裁定41 F1.2 攻撃: production (N_infty) 両 a_M=b_Mm3="0/0" は拒否される',
    compareNinf(badA, badB, ninfBundle)
  );
}

// ---- attack: (N_infty) u_pathA_ninf=u_pathB_ninf="1/0" (the core u-equality attack) ----
{
  const badA = { ...ninfA, u_pathA_ninf: '1/0' };
  const badB = { ...ninfB, u_pathB_ninf: '1/0' };
  expectStop(
    '裁定41 F1.2 攻撃: production (N_infty) 両 u="1/0" は拒否される(旧版は 1/0 == 1/0 を ACCEPT した)',
    compareNinf(badA, badB, ninfBundle)
  );
}

// ---- attack: main (K3) u_pathA=u_pathB="1/0" (the core u-equality attack, main branch) ----
{
  const badA = { ...k3A, u_pathA: '1/0' };
  const badB = { ...k3B, u_pathB: '1/0' };
  expectStop(
    '裁定41 F1.2 攻撃: main (K3) 両 u="1/0" は拒否される(第三 checker の核心である u exact equality を無効化する攻撃)',
    compareMain(badA, badB, k3Bundle)
  );
}

// ---- attack: "1/2/3" (two or more '/') must be rejected as a grammar violation,
// independent of which field carries it ----
{
  const badA = { ...ninfA, chat: '1/2/3' };
  expectStop(
    '裁定41 F1.2 攻撃: (N_infty) chat="1/2/3"(二本以上の "/")は全文 grammar 違反として拒否される',
    compareNinf(badA, ninfB, ninfBundle)
  );
}
{
  const badA = { ...k3A, x0: '1/2/3' };
  expectStop(
    '裁定41 F1.2 攻撃: main x0="1/2/3"(二本以上の "/")は全文 grammar 違反として拒否される',
    compareMain(badA, k3B, k3Bundle)
  );
}

// ============================================================================
// 司令塔独自攻撃(裁定41続報): parseRat の trim() 除去。旧版は正規表現の
// 前に String(s).trim() を呼んでおり、先頭/末尾空白が黙って正規化されて
// ACCEPT されていた("全文 grammar" の趣旨に反する)。trim を廃止し、
// 入力文字列そのままが ^[+-]?\d+(/[+-]?\d+)?$ に一致しなければ拒否する。
// ============================================================================
{
  const badA = { ...ninfA, chat: ' 1' };
  expectStop(
    '司令塔独自攻撃: (N_infty) chat=" 1"(先頭空白)は拒否される',
    compareNinf(badA, ninfB, ninfBundle)
  );
}
{
  const badA = { ...ninfA, chat: '1 ' };
  expectStop(
    '司令塔独自攻撃: (N_infty) chat="1 "(末尾空白)は拒否される',
    compareNinf(badA, ninfB, ninfBundle)
  );
}
{
  const badA = { ...ninfA, chat: '1/ 2' };
  expectStop(
    '司令塔独自攻撃: (N_infty) chat="1/ 2"(分子/分母間の空白)は拒否される',
    compareNinf(badA, ninfB, ninfBundle)
  );
}
{
  const badA = { ...k3A, x0: ' 1' };
  expectStop(
    '司令塔独自攻撃: main x0=" 1"(先頭空白)は拒否される',
    compareMain(badA, k3B, k3Bundle)
  );
}

console.log(`\n=== ${pass}/${pass + fail} PASS ===`);
if (fail > 0) process.exitCode = 1;
