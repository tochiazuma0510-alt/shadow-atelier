// search/certs/fixtures-lanea.mjs
//
// Lane A (searcher v2 + verifier A) fixtures — decision-lane candidates and
// divisor_equality_certificate scenarios, with EXPECTED outcomes for
// search/ninfty-selftest-lanea.mjs.
//
// All numeric (a,p,f6,C) tuples below satisfy the Pell relation a^2-f6*p^2=C
// EXACTLY by construction: a(x) = p(x)^2 * m1(x) + s0  (p monic quadratic,
// m1 monic linear, s0 a nonzero integer constant), C = s0^2,
// f6(x) = p(x)^2 * m1(x)^2 + 2*s0*m1(x). This identity holds for ANY choice
// of (b,c,k,s0) where p=x^2+bx+c, m1=x+k — it was NOT reverse-engineered by
// perturbing a known solution; it is an algebraic family. The specific
// (b,c,k,s0) tuples used here were found by brute-force search over small
// integers for the ones that ALSO satisfy T-1 (rootpart(a)=[2,2,1]) or its
// negation, as documented per fixture below.
//
// FIXTURE-DESIGN NOTE (superseded by 裁定 113): a genuine Pell-consistent
// (a,p,f6,C) example with a TRIPLE root (reject code [7] "triple-root-of-a")
// was NOT found within the earlier constructive family search up to
// |b|,|c|,|k|,|s0| <= 7. docs/notes/e5_interpretation_v1.md Sec.4 explains why
// (the "branch I" triple-root family a=x^5+5g*x^3, p=x^2+3g,
// f6=x^6+4g*x^4-8g^2*x^2+12g^3 has minimal integer height 12 at |g|=1, outside
// that search box) and supplies a closed form. `negTripleRootCandidate` below
// uses g=2 (per commander instruction, avoiding the g=1 / C=-108 sealed-adjacent
// value) as a full end-to-end candidate-level REJECT[7] fixture, in addition
// to the isolated `t1IsolatedTripleRoot` unit test kept for regression.
//
// CORRECTION NOTE: the commander's dispatch message gave f6 = x^6+16x^4-32x^2+96
// for g=2, but independent recomputation here (a^2 mod p^2 with a=x^5+10x^3,
// p=x^2+6) gives quotient f6 = x^6+8x^4-32x^2+96 with remainder C=-3456 (the
// x^4 coefficient is 8, matching the note's own formula 4g|_{g=2}=8, not 16;
// the C=-3456 value matches). Using the dispatched 16x^4 value would break the
// Pell identity and make the fixture hit REJECT[5] (pell-violation) instead of
// [7], defeating its purpose -- flagged here rather than silently "fixed".
// The corrected, verified value is used below.

export const positive1 = {
  label: 'positive-1 (b=-3,c=1,k=1,s0=-4)',
  candidate: {
    a: ['-3', '-5', '5', '5', '-5', '1'],
    p: ['1', '-3', '1'],
    f6: ['-7', '-12', '0', '10', '0', '-4', '1'],
    orientation_declared_ok: true,
  },
  expect: { verdict: 'ACCEPT', primary_reason_code: 'accepted' },
};

export const positive2 = {
  label: 'positive-2 (b=-1,c=-1,k=-3,s0=4)',
  candidate: {
    a: ['1', '-5', '5', '5', '-5', '1'],
    p: ['-1', '-1', '1'],
    f6: ['-15', '20', '-20', '-10', '20', '-8', '1'],
    orientation_declared_ok: true,
  },
  expect: { verdict: 'ACCEPT', primary_reason_code: 'accepted' },
};

export const negDegreeMismatch = {
  label: 'neg-degree-mismatch [1] (a truncated to degree 4)',
  candidate: {
    a: ['-3', '-5', '5', '5', '-5'], // degree 4, was positive1.a with leading term dropped
    p: ['1', '-3', '1'],
    f6: ['-7', '-12', '0', '10', '0', '-4', '1'],
    orientation_declared_ok: true,
  },
  expect: { verdict: 'REJECT', primary_reason_code: 'precondition/degree-mismatch' },
};

export const negF6NotMonic = {
  label: 'neg-f6-not-monic [2] (positive1.f6 scaled by 2)',
  candidate: {
    a: ['-3', '-5', '5', '5', '-5', '1'],
    p: ['1', '-3', '1'],
    f6: ['-14', '-24', '0', '20', '0', '-8', '2'],
    orientation_declared_ok: true,
  },
  expect: { verdict: 'REJECT', primary_reason_code: 'precondition/f6-not-monic' },
};

export const negCurveNotSquarefree = {
  label: 'neg-curve-not-squarefree [3] (f6=(x-1)^2(x-2)(x-3)(x-4)(x-5))',
  candidate: {
    a: ['-3', '-5', '5', '5', '-5', '1'],
    p: ['1', '-3', '1'],
    f6: ['120', '-394', '499', '-310', '100', '-16', '1'],
    orientation_declared_ok: true,
  },
  expect: { verdict: 'REJECT', primary_reason_code: 'precondition/curve-not-squarefree' },
};

export const negLeadingCoeffMismatch = {
  label: 'neg-leading-coeff-mismatch [4] (a5=2, p2=1)',
  candidate: {
    a: ['-3', '-5', '5', '5', '-5', '2'],
    p: ['1', '-3', '1'],
    f6: ['-7', '-12', '0', '10', '0', '-4', '1'],
    orientation_declared_ok: true,
  },
  expect: { verdict: 'REJECT', primary_reason_code: 'precondition/leading-coeff-mismatch' },
};

export const negPellViolation = {
  label: 'neg-pell-violation [5] (positive1.f6 constant term perturbed by +1)',
  candidate: {
    a: ['-3', '-5', '5', '5', '-5', '1'],
    p: ['1', '-3', '1'],
    f6: ['-6', '-12', '0', '10', '0', '-4', '1'],
    orientation_declared_ok: true,
  },
  expect: { verdict: 'REJECT', primary_reason_code: 'precondition/pell-violation' },
};

export const negDivisorOrientation = {
  // 2026-08-01 (docs/notes/lanea_native_semantics_v1.md §8 C-1..C-5, cert
  // search/certs/ep_nf_20260801.json e5_c1_c5): E-5 is now DERIVED once
  // E-1..E-4 hold, on BOTH lanes -- an attested orientation flag that
  // contradicts the derived value is no longer treated as a candidate
  // defect (REJECT[6]) but as an input-inconsistency (INTEGRITY_STOP,
  // 'divisor-orientation-attestation-mismatch' [27]), the same C-3 pattern
  // already used for E-6 (gcd(a,p)!=1 after exact E-4 PASS). This fixture's
  // `expect` was stale after that migration (ninfty-selftest-lanea.mjs was
  // not in the C-1..C-5 batch's own regression list) -- updated here to the
  // now-correct verdict, found + fixed during the 2026-08-01 EP re-activation
  // full-suite regression pass.
  label: 'neg-divisor-orientation [27] (declared flag false disagrees with derived E-5=true, C-3/裁定 113)',
  candidate: {
    a: ['-3', '-5', '5', '5', '-5', '1'],
    p: ['1', '-3', '1'],
    f6: ['-7', '-12', '0', '10', '0', '-4', '1'],
    orientation_declared_ok: false,
  },
  expect: { verdict: 'INTEGRITY_STOP', primary_reason_code: 'divisor-orientation-attestation-mismatch' },
};

export const positive3OmittedOrientationFlag = {
  label: 'positive-3 (same as positive-1, orientation_declared_ok OMITTED -- derived E-5 accepted, 裁定 113)',
  candidate: {
    a: ['-3', '-5', '5', '5', '-5', '1'],
    p: ['1', '-3', '1'],
    f6: ['-7', '-12', '0', '10', '0', '-4', '1'],
    // orientation_declared_ok intentionally absent: this is exactly the case
    // 裁定 113 / e5_interpretation_v1.md Sec.3.2 says must NOT be REJECT[6].
  },
  expect: { verdict: 'ACCEPT', primary_reason_code: 'accepted' },
};

export const negTripleRootCandidate = {
  label: 'neg-triple-root-of-a [7] (branch I, g=2: a=x^5+10x^3, p=x^2+6, f6=x^6+8x^4-32x^2+96, C=-3456)',
  candidate: {
    a: ['0', '0', '0', '10', '0', '1'],
    p: ['6', '0', '1'],
    f6: ['96', '0', '-32', '0', '8', '0', '1'],
    orientation_declared_ok: true,
  },
  expect: { verdict: 'REJECT', primary_reason_code: 'triple-root-of-a' },
};

export const negAPartitionMismatch = {
  label: 'neg-a-partition-mismatch [8] (b=-4,c=-4,k=-4,s0=-4; gcd(a,a") has degree 0)',
  candidate: {
    a: ['-68', '-112', '0', '40', '-12', '1'],
    p: ['-4', '-4', '1'],
    f6: ['288', '376', '-112', '-160', '88', '-16', '1'],
    orientation_declared_ok: true,
  },
  expect: { verdict: 'REJECT', primary_reason_code: 'a-partition-mismatch' },
};

// ISOLATED T-1 unit test for code [7] -- see FIXTURE-DESIGN NOTE above.
export const t1IsolatedTripleRoot = {
  label: 't1-isolated-triple-root [7] ((x-1)^3(x-2)(x-3), checkT1 only, NOT a full candidate)',
  aCoeffs: ['-6', '23', '-34', '24', '-8', '1'],
  expect: { ok: false, code: 'triple-root-of-a' },
};

export const decisionLaneFixtures = [
  positive1, positive2, positive3OmittedOrientationFlag, negDegreeMismatch, negF6NotMonic,
  negCurveNotSquarefree, negLeadingCoeffMismatch, negPellViolation, negDivisorOrientation,
  negTripleRootCandidate, negAPartitionMismatch,
];
