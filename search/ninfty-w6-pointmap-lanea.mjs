// search/ninfty-w6-pointmap-lanea.mjs
//
// LANE A per-point W-6 point-map PRODUCER.
//
// AUTHORISATION: Sol 便98 P98-6.1 ("W6-P1 lane A per-point producer 改造:
// 認可 GO").  What P98-6.1 authorises is exactly this file: a producer that
// separates the FINITE ramification points of the genuine fixture ONE BY ONE
// and emits a `mb/ninfty-w6-point-map/v1` record for each.  It authorises
// nothing else.  In particular Sol 便98 P98-6.2/F98-6.3 keep refusing:
//   * W-6 closure          (IMAGE-MU is still UNKNOWN on the receiver side)
//   * EP re-activation
//   * the positive-control full run
// so this module declares `W6_CLOSED = false` and stamps every output
// `artifact_class: "diagnostic_construction"` (便95 F95-2.3 terminology:
// a diagnostic construction is buildable pre-gate and is NOT a minted /
// published artifact; publication is the registry's business, not this
// file's).
//
// ERA (spec v20 sec.5.3.4 / P98-6.2 item 1): this file belongs to the NEW
// plane `w6_point_map_producer`, era ERA_W6KEY -- NOT to `native_payload_
// schema` (ERA_FROZEN).  Its payload must never be presented to the frozen
// R1/R2 core as a v18 native payload (P98-6.2 item 2).
//   [ep-era-declaration] plane=w6_point_map_producer predicate_spec_id=mb/ninfty-stage2-predicate/v20 verifier_contract_id=mb/ninfty-verifier-contract/v15 dependency_manifest_schema_id=mb/dependency-manifest/v15
//
// INDEPENDENCE (schema doc H-1/H-3/H-4', spec v20 W6-P6): this module reads
// ONLY lane A's own module (search/ninfty-searcher-v2.mjs: its exact rational
// arithmetic and its own gcd-derived loci) plus the SHARED MATHEMATICAL
// SCHEMA document.  It never reads the other lane's producer, its normal
// form, its tokens, or its symbolic string encoding, and it never imports a
// receiver route.  The key is re-derived here from the curve data by this
// file's own code; agreement with the other lane, if it happens, is the
// schema doing the work.
//
// WHAT IT COMPUTES (P98-6.1, verbatim geometry).  For an ACCEPTed candidate
// (curve y^2 = f6(x), map mu = a(x) + p(x) y, Pell a^2 - f6 p^2 = C):
//
//   * finite ramification support = the roots of d = gcd(a, a') (lane A
//     already builds this locus in buildSearcherNative as `a-pair-locus`).
//     T-1 gives rootpart(a) = [2,2,1], so d is squarefree of degree 2 and
//     each root x0 is a DOUBLE root of a.
//   * over each such x0 the curve has the two points (x0, y) with
//     y^2 = f6(x0) =: F0.  THESE ARE THE POINTS.  P-1 of the schema doc is
//     explicit that the x-locus alone is only the support and must not be
//     "assigned to the two roots" of the branch polynomial; the point is
//     made here from the curve relation.
//   * mu(x0, y) = a(x0) + p(x0) y, so with s := p(x0)^2 F0 the image b
//     satisfies (b - a(x0))^2 = s.  That is the exact reduction chain
//     recorded per record as `exact_reduction`.
//   * ramification index e = 2 at each of these points (partition [2,2,1]),
//     so m_r = e - 1 = 1; and at the two points over x = infinity e = 5,
//     m_r = 4, with mu(inf_-) = 0 and mu(inf_+) = infinity by (Or) under the
//     E-3 branch a5 = +p2.  Total 4*1 + 2*4 = 12 = deg R_mu = 2g-2+2deg(mu),
//     asserted below, fail-closed.
//
// FAIL-CLOSED (schema doc O-2/O-3): anything this route cannot decide
// EXACTLY within the v1 universe (coefficient field Q, target P^1_mu) is
// reported as UNKNOWN with the reason recorded, and NO records are emitted
// for it.  There is no float arithmetic anywhere in this file and no
// approximate root finding: the only numbers are exact rationals from lane
// A's own Frac.
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  Frac, F0, F1,
  polyFromInts, polyDeg, polyGCD, polyDerivative, polyMonic, polyMul, polySub,
  polyToCoeffStrings, polyLeading,
  evaluateDecisionLane,
} from './ninfty-searcher-v2.mjs';

const THIS_DIR = dirname(fileURLToPath(import.meta.url));
const REPO = join(THIS_DIR, '..');

export const BRANCH_KEY_SCHEMA_ID = 'mb/ninfty-w6-branch-key/v1';
export const POINT_MAP_SCHEMA_ID = 'mb/ninfty-w6-point-map/v1';
export const IMAGE_WITNESS_SCHEMA_ID = 'mb/ninfty-w6-image-witness/v1';
export const TARGET_COORDINATE_ID = 'aqp1';
export const TARGET_MAP_ID = 'mu';
export const DEFINITION_DOC = 'docs/mb_ninfty_w6_branch_key_v1.md';

// This producer does not close W-6 and may not be read as closing it.
export const W6_CLOSED = false;

function schemaDefinitionDigest() {
  try {
    return createHash('sha256').update(readFileSync(join(REPO, 'docs', 'mb_ninfty_w6_branch_key_v1.md'))).digest('hex');
  } catch {
    return null;
  }
}

// --------------------------------------------------------------------------
// exact rational helpers (lane A's own Frac; no float anywhere)
// --------------------------------------------------------------------------

function evalPoly(poly, x) {
  const d = polyDeg(poly);
  if (d < 0) return F0;
  let out = poly[d];
  for (let i = d - 1; i >= 0; i--) out = out.mul(x).add(poly[i]);
  return out;
}

function fracParts(f) {
  // lane A's Frac keeps n/d in lowest terms with a positive denominator.
  return { num: f.n, den: f.d };
}

function bigAbs(n) { return n < 0n ? -n : n; }

function bigGcd(x, y) {
  x = bigAbs(x); y = bigAbs(y);
  while (y) { const t = x % y; x = y; y = t; }
  return x;
}

function bigIsqrt(n) {
  if (n < 0n) return null;
  if (n < 2n) return n;
  let lo = 0n, hi = 1n;
  while (hi * hi <= n) hi <<= 1n;
  while (lo + 1n < hi) {
    const mid = (lo + hi) >> 1n;
    if (mid * mid <= n) lo = mid; else hi = mid;
  }
  return lo;
}

/** exact rational square root, or null when the rational is not a square. */
function exactRationalSqrt(f) {
  const { num, den } = fracParts(f);
  if (num < 0n) return null;
  const rn = bigIsqrt(num), rd = bigIsqrt(den);
  if (rn === null || rn * rn !== num || rd * rd !== den) return null;
  return new Frac(rn, rd);
}

/**
 * K-2 normalisation, coded here from the schema's words (integer coefficient
 * list, low to high, content 1, positive leading coefficient).  `coeffs` are
 * exact rationals, low to high.
 */
function primitiveIntegerForm(coeffs) {
  let den = 1n;
  for (const c of coeffs) {
    const { den: d } = fracParts(c);
    den = (den / bigGcd(den, d)) * d;
  }
  const ints = coeffs.map((c) => {
    const { num, den: d } = fracParts(c);
    return (num * den) / d;
  });
  let g = 0n;
  for (const v of ints) g = bigGcd(g, v);
  let out = g === 0n ? ints : ints.map((v) => v / g);
  while (out.length > 1 && out[out.length - 1] === 0n) out = out.slice(0, -1);
  if (out[out.length - 1] < 0n) out = out.map((v) => -v);
  return out;
}

function tokenFinite(intCoeffs, rank) {
  return `${TARGET_COORDINATE_ID}|${TARGET_MAP_ID}|F|${intCoeffs.map((v) => v.toString()).join(',')}|${rank}`;
}

const TOKEN_INFINITY = `${TARGET_COORDINATE_ID}|${TARGET_MAP_ID}|I`;

/**
 * The exact image datum of b = re + sign*sqrt(s), together with its token.
 * `s` is an exact rational.  Returns {ok, datum, token, minimal_polynomial}
 * or {ok:false, reason} when v1 cannot decide it exactly.
 *
 * Rank rule, re-derived here from K-3 (lexicographic Re then Im):
 *   s < 0 : conjugate pair, equal real parts -> the NEGATIVE imaginary part
 *           ranks 0, i.e. rank = (sign < 0 ? 0 : 1).
 *   s > 0 non-square : two distinct reals -> the SMALLER ranks 0, and the
 *           smaller one is again the minus sign.  Same formula.
 *   s a rational square (incl. 0) : b is RATIONAL, degree 1, rank 0.
 */
function imageDatumFor(re, s, sign) {
  if (sign !== 1 && sign !== -1) return { ok: false, reason: `sign must be +-1, got ${sign}` };
  const root = exactRationalSqrt(s);
  if (root !== null) {
    // b = re + sign*root is rational: degree-1 minimal polynomial.
    const b = sign < 0 ? re.sub(root) : re.add(root);
    const coeffs = primitiveIntegerForm([b.neg(), F1]);
    return {
      ok: true,
      datum: { kind: 'rational', value: b.toString() },
      token: tokenFinite(coeffs, 0),
      minimal_polynomial: coeffs.map((v) => v.toString()),
      rank: 0,
    };
  }
  // (T - re)^2 = s  ->  T^2 - 2 re T + (re^2 - s), irreducible over Q because
  // s is not a rational square.
  const coeffs = primitiveIntegerForm([re.mul(re).sub(s), F0.sub(re.add(re)), F1]);
  const rank = sign < 0 ? 0 : 1;
  const negative = fracParts(s).num < 0n;
  const datum = negative
    ? { kind: 'quadratic_imaginary', real_part: re.toString(), imag_sq: F0.sub(s).toString(), sign }
    : { kind: 'quadratic_real', real_part: re.toString(), radicand: s.toString(), sign };
  return { ok: true, datum, token: tokenFinite(coeffs, rank), minimal_polynomial: coeffs.map((v) => v.toString()), rank };
}

/** rational roots of a monic squarefree quadratic, exactly; null when it is
 *  irreducible over Q (then the x-support itself is not Q-rational and the
 *  v1 universe does not cover it -> UNKNOWN, never a guessed split). */
function rationalRootsOfMonicQuadratic(d) {
  if (polyDeg(d) !== 2) return null;
  const [c0, c1] = [d[0], d[1]];
  const disc = c1.mul(c1).sub(c0.add(c0).add(c0).add(c0)); // c1^2 - 4 c0
  const r = exactRationalSqrt(disc);
  if (r === null) return null;
  const two = new Frac(2n);
  const x1 = F0.sub(c1).sub(r).div(two);
  const x2 = F0.sub(c1).add(r).div(two);
  return [x1, x2];
}

/** canonical, grammar-safe rendering of an exact rational for use inside a
 *  ramification_point_id ("-2", "-7/3"). */
function rationalId(f) { return f.toString(); }

// --------------------------------------------------------------------------
// the producer
// --------------------------------------------------------------------------

/**
 * Build the lane-A per-point W-6 point map for one candidate.
 *
 * NOTE ON WHAT IS *NOT* HERE (W6-C4): no producer-side aggregate is emitted.
 * The receiver re-sums the per-point multiplicities itself; shipping a
 * self-declared divisor would invite exactly the "trust the producer's
 * aggregate" defect W97-3.1 named.
 */
export function buildW6PointMapLaneA(candidate, options = {}) {
  const sourceArtifactId = options.source_artifact_id || null;
  const base = {
    producer: 'lane_a',
    producer_module: 'search/ninfty-w6-pointmap-lanea.mjs',
    point_map_schema_id: POINT_MAP_SCHEMA_ID,
    artifact_class: 'diagnostic_construction',
    registry_pinned: false,
    w6_closed: W6_CLOSED,
    frame: {
      branch_key_schema_id: BRANCH_KEY_SCHEMA_ID,
      point_map_schema_id: POINT_MAP_SCHEMA_ID,
      target_coordinate_id: TARGET_COORDINATE_ID,
      branch_key_definition_digest: schemaDefinitionDigest(),
    },
    declared_support: [],
    records: [],
    unresolved: [],
    note: 'diagnostic construction, not a published artifact; W-6 is OPEN (IMAGE-MU is UNKNOWN on both receiver routes).',
  };

  const decision = evaluateDecisionLane(candidate);
  if (decision.verdict === 'REJECT') {
    return { ...base, status: 'ABSENT', decision_verdict: decision.verdict,
      primary_reason_code: decision.primary_reason_code,
      reason: 'the decision lane REJECTed this candidate -- no divisor-shaped data exists, so no ramification point may be named.' };
  }
  if (decision.verdict === 'INTEGRITY_STOP') {
    return { ...base, status: 'INTEGRITY_STOP', decision_verdict: decision.verdict,
      primary_reason_code: decision.primary_reason_code,
      reason: 'a theorem-forced identity broke after the prerequisites held; the input is internally inconsistent.' };
  }

  const a = polyFromInts(candidate.a);
  const p = polyFromInts(candidate.p);
  const f6 = polyFromInts(candidate.f6);
  const d = polyMonic(polyGCD(a, polyDerivative(a)));
  const pell = polySub(polyMul(a, a), polyMul(f6, polyMul(p, p)));

  // E-3's literal branch (a5 = +p2) is what fixes the orientation
  // mu(inf_-) = 0, mu(inf_+) = infinity.  ACCEPT already implies it; assert
  // rather than assume, because the orientation is what names the two
  // infinite records below.
  if (!polyLeading(a).eq(polyLeading(p))) {
    return { ...base, status: 'UNKNOWN',
      reason: 'a5 != p2: the E-3 branch that fixes the (Or) orientation does not hold, so the two points at infinity cannot be named. Fail-closed.' };
  }

  const roots = polyDeg(d) === 2 ? rationalRootsOfMonicQuadratic(d) : null;
  if (roots === null) {
    return { ...base, status: 'UNKNOWN',
      reason: `the finite ramification locus d = gcd(a,a') = [${polyToCoeffStrings(d).join(',')}] does not split into Q-rational points in the v1 universe (coefficient field Q, sec.1 of the schema doc). Separating its points needs an x-side algebraic extension, which v1 does not cover; no record is emitted and nothing is guessed.` };
  }
  if (roots[0].eq(roots[1])) {
    return { ...base, status: 'UNKNOWN', reason: 'd is not squarefree; T-1 should have excluded this.' };
  }

  const records = [];
  const support = [];
  const unresolved = [];

  for (const x0 of roots) {
    const aAt = evalPoly(a, x0);
    const pAt = evalPoly(p, x0);
    const f6At = evalPoly(f6, x0);
    // sanity, exact: x0 is a double root of a, and the fibre is not a
    // Weierstrass point (f6(x0) = 0 would force C = a(x0)^2 - 0 = 0).
    if (!aAt.eq(F0)) {
      unresolved.push({ x: rationalId(x0), reason: `a(x0) = ${aAt.toString()} != 0: x0 is not a double root of a, contradicting T-1's rootpart [2,2,1].` });
      continue;
    }
    if (f6At.eq(F0)) {
      unresolved.push({ x: rationalId(x0), reason: 'f6(x0) = 0: the fibre degenerates to a Weierstrass point, which the Pell constant C != 0 forbids.' });
      continue;
    }
    const s = pAt.mul(pAt).mul(f6At);           // (mu - a(x0))^2 at this point
    const pSign = fracParts(pAt).num < 0n ? -1 : (fracParts(pAt).num === 0n ? 0 : 1);
    if (pSign === 0) {
      unresolved.push({ x: rationalId(x0), reason: 'p(x0) = 0: mu collapses on the fibre and the two points share one image; v1 does not encode that degenerate case.' });
      continue;
    }
    // the fibre's own minimal polynomial: y^2 - f6(x0)
    const fibreMinPoly = primitiveIntegerForm([F0.sub(f6At), F0, F1]);
    for (const yRank of [0, 1]) {
      const ySign = yRank === 0 ? -1 : 1;        // K-3 applied to y's own minimal polynomial
      const bSign = pSign * ySign;
      const img = imageDatumFor(aAt, s, bSign);
      if (!img.ok) {
        unresolved.push({ x: rationalId(x0), y_root_rank: yRank, reason: img.reason });
        continue;
      }
      // P98-6.1, verbatim: the ramification_point_id carries BOTH the value
      // of x AND the y-root rank; it is never the branch token in disguise.
      const pointId = `aff|x=${rationalId(x0)}|yrank=${yRank}`;
      support.push(pointId);
      records.push({
        ramification_point_id: pointId,
        branch_value: img.token,
        multiplicity: 1,                         // e = 2 at a [2,2,1] fibre point => m_r = e - 1 = 1
        ramification_index: 2,
        source_locus_ref: {
          artifact_id: sourceArtifactId || 'lane-a-diagnostic-locus',
          json_pointer: '/ramification_divisor_on_C_ref/components/0',
          digest: createHash('sha256').update(JSON.stringify({
            locus_type: 'a-pair-locus', ideal_generator: polyToCoeffStrings(d),
          })).digest('hex'),
          ref_status: sourceArtifactId ? 'registry_pinned_claimed' : 'LEGACY_UNVERIFIED_REF',
        },
        exact_image_witness: {
          schema_id: IMAGE_WITNESS_SCHEMA_ID,
          datum: img.datum,
          // The exact reduction chain P98-6.1 requires:
          //   fibre relation      y^2 - f6(x0) = 0
          //   map evaluation      mu = a(x0) + p(x0) y
          //   image relation      minimal polynomial of mu
          exact_reduction: {
            fibre_relation: { variable: 'y', minimal_polynomial_low_to_high: fibreMinPoly.map((v) => v.toString()) },
            map_evaluation: { form: 'mu = a(x0) + p(x0)*y', x: rationalId(x0), a_at_x: aAt.toString(), p_at_x: pAt.toString() },
            image_relation: { variable: 'mu', minimal_polynomial_low_to_high: img.minimal_polynomial, root_rank: img.rank },
            square_relation: { statement: '(mu - a(x0))^2 = p(x0)^2 * f6(x0)', value: s.toString() },
          },
        },
      });
    }
  }

  // The two points at infinity.  (Or): div(mu) = 5 P_0 - 5 P_inf with, under
  // the E-3 branch a5 = +p2, P_0 = inf_- and P_inf = inf_+.  e = 5 there, so
  // m_r = 4 at each.
  for (const [pointId, img] of [
    ['inf_minus', { token: (() => { const c = primitiveIntegerForm([F0, F1]); return tokenFinite(c, 0); })(), datum: { kind: 'rational', value: '0' }, minimal_polynomial: ['0', '1'], rank: 0 }],
    ['inf_plus', { token: TOKEN_INFINITY, datum: { kind: 'infinity' }, minimal_polynomial: null, rank: null }],
  ]) {
    support.push(pointId);
    records.push({
      ramification_point_id: pointId,
      branch_value: img.token,
      multiplicity: 4,                            // e = 5 => m_r = 4
      ramification_index: 5,
      source_locus_ref: {
        artifact_id: sourceArtifactId || 'lane-a-diagnostic-locus',
        json_pointer: '/ram_infinite',
        digest: createHash('sha256').update(JSON.stringify({ locus_type: 'infinity', point: pointId })).digest('hex'),
        ref_status: sourceArtifactId ? 'registry_pinned_claimed' : 'LEGACY_UNVERIFIED_REF',
      },
      exact_image_witness: {
        schema_id: IMAGE_WITNESS_SCHEMA_ID,
        datum: img.datum,
        exact_reduction: {
          orientation: '(Or) div(mu) = 5 P_0 - 5 P_inf, E-3 branch a5 = +p2 => P_0 = inf_-, P_inf = inf_+',
          image_relation: img.minimal_polynomial
            ? { variable: 'mu', minimal_polynomial_low_to_high: img.minimal_polynomial, root_rank: img.rank }
            : { variable: 'mu', at_infinity: true },
        },
      },
    });
  }

  // deg R_mu = 2g - 2 + 2 deg(mu) = 12 for g = 2, deg mu = 5.  A point map
  // whose multiplicities do not add up to 12 has lost or invented a point;
  // that is a provenance defect, and the honest report is UNKNOWN, not a
  // partial map presented as complete.
  const total = records.reduce((acc, r) => acc + r.multiplicity, 0);
  const status = unresolved.length ? 'UNKNOWN' : (total === 12 ? 'PRESENT' : 'UNKNOWN');

  return {
    ...base,
    status,
    decision_verdict: decision.verdict,
    declared_support: support,
    records,
    unresolved,
    ramification_degree_check: { total_multiplicity: total, required: 12, ok: total === 12 },
    pell_constant: polyDeg(pell) === 0 ? pell[0].toString() : null,
    finite_ramification_locus: polyToCoeffStrings(d),
    ...(status === 'UNKNOWN' && unresolved.length
      ? { reason: 'at least one ramification point could not be resolved exactly in the v1 universe; see unresolved[].' }
      : {}),
    ...(status === 'UNKNOWN' && !unresolved.length
      ? { reason: `the per-point multiplicities sum to ${total}, not the required deg R_mu = 12.` }
      : {}),
  };
}

// --------------------------------------------------------------------------
// CLI:  node search/ninfty-w6-pointmap-lanea.mjs <candidate.json> [artifact_id]
// --------------------------------------------------------------------------
const invokedDirectly = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (invokedDirectly) {
  const path = process.argv[2];
  if (!path) {
    process.stderr.write('usage: node search/ninfty-w6-pointmap-lanea.mjs <candidate.json> [source_artifact_id]\n');
    process.exit(2);
  }
  const candidate = JSON.parse(readFileSync(path, 'utf8'));
  const out = buildW6PointMapLaneA(candidate, { source_artifact_id: process.argv[3] || null });
  process.stdout.write(JSON.stringify(out, null, 2) + '\n');
}
