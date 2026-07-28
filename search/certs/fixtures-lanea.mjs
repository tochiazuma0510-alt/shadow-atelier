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
// FIXTURE-DESIGN NOTE (reported to commander, not silently decided): a
// genuine Pell-consistent (a,p,f6,C) example with a TRIPLE root or a
// non-squarefree gcd(a,a') (reject code [7] "triple-root-of-a") was NOT found
// within this constructive family up to |b|,|c|,|k|,|s0| <= 7. Code [7] is
// therefore tested in ISOLATION against the `checkT1` sub-routine only
// (fixture `t1IsolatedTripleRoot` below), using a synthetic a(x) with a known
// triple root, WITHOUT an accompanying Pell-consistent (p,f6,C) triple. This
// is flagged as a scope gap, not asserted as a full end-to-end REJECT[7]
// candidate test.

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
  label: 'neg-divisor-orientation [6] (declared flag false; see searcher file KNOWN GAP)',
  candidate: {
    a: ['-3', '-5', '5', '5', '-5', '1'],
    p: ['1', '-3', '1'],
    f6: ['-7', '-12', '0', '10', '0', '-4', '1'],
    orientation_declared_ok: false,
  },
  expect: { verdict: 'REJECT', primary_reason_code: 'precondition/divisor-orientation' },
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
  positive1, positive2, negDegreeMismatch, negF6NotMonic, negCurveNotSquarefree,
  negLeadingCoeffMismatch, negPellViolation, negDivisorOrientation, negAPartitionMismatch,
];
