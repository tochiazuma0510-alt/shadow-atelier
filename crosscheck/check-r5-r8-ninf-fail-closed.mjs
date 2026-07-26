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

import { loadModel, loadModelNinf, extractPathB_Ninf } from './u-extract-pathB-lib.mjs';

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

console.log(`\n=== ${pass}/${pass + fail} PASS ===`);
if (fail > 0) process.exitCode = 1;
