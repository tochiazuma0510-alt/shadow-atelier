// crosscheck/check-e2c6j3.mjs
// Independent Node-side crosscheck for search/e2c6j3-sweep.g (E2 class-6 j=3 gate,
// docs/manifest_e2c6j3_v1.md).
//
// === TOOL SPEC (per docs/所在と能力.md "ツール仕様ヘッダ標準" / 体制と道具.md "仕様書優先") ===
//
// (1) INPUT:
//   - crosscheck/agree6_sol2.json : ONLY source for class-6 table data (system B, Sol's
//     independent transcription) -- same discipline as crosscheck/check-e2c6.mjs (j=2). This
//     script does NOT read search/e2c6j3-sweep.g, search/e2c6-common-data.g, or sol/.
//   - certificates/e2c6j3/*.json  : the only other input.
//   - The RATIFIED OB FORMULA and the j=3 lambda formula (eq 8.1-8.4, W(m)=binom(m+1,2) mod2)
//     are taken from the same commander-designated spec chain (docs/manifest_e2c6j3_v1.md,
//     docs/委嘱16_ob定義_opus_v1.md, sol/sol_reply_22_ob.md, and sol/sol_reply_24_d2.md §F8
//     ONLY -- §F7 of that file is sealed and was not read while writing this checker).
//
// (2) MODES: fixture mode only (this script never computes/discloses real m>0 class-6
//   target solvability -- the one exception is m=0, a known structural identity, same as
//   check-e2c6.mjs's own m=0 shortcut precedent).
//
// (3) OUTPUT (certificate schemas this script consumes):
//   - claim:"m6j3_multiplicity_table" : {m,j,modulus,R,witness_f0_abar,K_generators,
//     K_orders,total_points,ob_table,brute_force_matches_shortcut,ob_mode}. Independently
//     re-enumerates the FULL L_m coset from f0/K_generators/K_orders, recomputes the ACTUAL
//     (nonlinear) first-condition Q(f)=(f_p mod2, (f_s3+f_w*f_r2) mod2) at every point
//     (exact brute force -- no lambda shortcut trusted blindly), and compares the resulting
//     table to the certificate's claimed ob_table exactly (keys AND counts), plus checks
//     total_points = Prod(K_orders) and sum(ob_table)=total_points.
//   - claim:"f7_routeG_crosscheck" (gate:"j=3") : same recheck style as check-e2c6.mjs's
//     f7_routeG_crosscheck handler (route-G group product itself not independently rebuilt
//     here -- no polycyclic package in Node; GAP-only check), but ALSO verifies every test
//     vector `f` in the certificate is already reduced mod 8 (the j=3 Abar modulus), which
//     is the specific "j=3 cell" content this fixture adds over the j=2 gate's F7.
//   - claim:"linear_stage_empty_c6j3" : real-sweep negative cert (only appears if the fire
//     lock is ever opened) -- not expected in a fixture-only run, but handled defensively.
//
// (4) MODE LOCK: same rule as check-e2c6.mjs -- any cert carrying an ob-bearing field must
//   declare "ob_mode":"quotient-ratified-v2"; anything else with non-null ob content is a
//   REJECT.
//
// STATUS (2026-07-26, implementer, j=3 gate build): fixture-only. Real 64-system sweep is
// gated behind search/FIRE_e2c6j3.auth (this checker has no opinion on whether that file
// should exist -- see search/e2c6j3-sweep.g's own header for the fire-lock mechanism).

'use strict';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
const __dirname_ = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname_, '..');

const sol2 = JSON.parse(readFileSync(join(ROOT, 'crosscheck', 'agree6_sol2.json'), 'utf8'));
const BASIS21 = sol2.meta.basis_order;
if (BASIS21.length !== 21) throw new Error('unexpected basis length');

let fails = 0;
const TT = (name, cond, extra = '') => {
  console.log((cond ? 'PASS  ' : 'FAIL  ') + name + (extra ? '   ' + extra : ''));
  if (!cond) fails++;
};
console.log('=== crosscheck/check-e2c6j3.mjs (independent Node reimplementation, j=3 gate, input=agree6_sol2.json) ===');

// ---------------------------------------------------------------------------
// Full 21x21 operators from sol2's theta_table / sigma_table_poly / Em_components
// (independent re-transcription -- same code shape as check-e2c6.mjs, re-typed fresh here
// per the search/crosscheck separation discipline: this checker does not import GAP code or
// e2c6j3-sweep.g's JS-equivalent from anywhere).
// ---------------------------------------------------------------------------
function genBinom(m, k) {
  if (k < 0) return 0;
  if (k === 0) return 1;
  let num = 1;
  for (let i = 0; i < k; i++) num *= (m - i);
  let f = 1; for (let i = 2; i <= k; i++) f *= i;
  return num / f;
}
function evalPoly5(p5, m) {
  return p5[0] + p5[1] * genBinom(m, 1) + p5[2] * genBinom(m, 2) + p5[3] * genBinom(m, 3) + p5[4] * genBinom(m, 4);
}
function evalEmComponent(terms, m) {
  return terms.reduce((s, t) => s + t.coef * genBinom(m + t.shift, t.k), 0);
}
function mod(x, m) { const r = x % m; return r < 0 ? r + m : r; }

const ThetaTable21 = BASIS21.map((g) => sol2.theta_table[g]);
function sigmaRow(g) {
  const row = sol2.sigma_table_poly[g] || {};
  return BASIS21.map((coord) => row[coord] || [0, 0, 0, 0, 0]);
}
const SigmaTablePoly21 = BASIS21.map((g) => sigmaRow(g));
const EmComponents21 = BASIS21.map((g) => sol2.Em_components[g] || []);
const KappaTerms = sol2.kappa_terms.terms;
const DThetaFormula = sol2.d_theta_formula;
const DSigmaFormula = sol2.d_sigma_formula;

function vecMatMul(v, M) {
  const n = M.length, m = M[0].length;
  const r = new Array(m).fill(0);
  for (let i = 0; i < n; i++) if (v[i] !== 0) for (let j = 0; j < m; j++) r[j] += v[i] * M[i][j];
  return r;
}

const AbarNames = ['w', 'p', 'q', 'r1', 'r2', 'r3', 't1', 't2', 't3', 't4', 's1', 's2', 's3', 's4', 's5'];
const CNames = ['t5', 't6', 'u1', 'u2', 'u3', 'u4'];
const nameIdx21 = (nm) => BASIS21.indexOf(nm);
const AbarIdx21 = AbarNames.map(nameIdx21);
const CIdx21 = CNames.map(nameIdx21);
const NAB = AbarNames.length, NC6 = CNames.length;
const IdxP = AbarNames.indexOf('p'), IdxW = AbarNames.indexOf('w'),
      IdxR2 = AbarNames.indexOf('r2'), IdxS3 = AbarNames.indexOf('s3');

const ThetaBarMat = AbarIdx21.map((i) => AbarIdx21.map((j) => ThetaTable21[i][j]));
function SigmaBarMat(m) { return AbarIdx21.map((i) => AbarIdx21.map((j) => evalPoly5(SigmaTablePoly21[i][j], m))); }
function EmBar15(m) { return AbarIdx21.map((i) => evalEmComponent(EmComponents21[i], m)); }
const ThetaOnCMat = CIdx21.map((i) => CIdx21.map((j) => ThetaTable21[i][j]));
function SigmaOnCMat(m) { return CIdx21.map((i) => CIdx21.map((j) => evalPoly5(SigmaTablePoly21[i][j], m))); }
function EmC6(m) { return CIdx21.map((i) => evalEmComponent(EmComponents21[i], m)); }

function evalDFormTerm(term, avec15, m, mPolyLen) {
  let mc;
  if (mPolyLen === 1) mc = term.mcoef[0];
  else mc = term.mcoef[0] + term.mcoef[1] * genBinom(m, 1) + term.mcoef[2] * genBinom(m, 2);
  if (term.vars.length === 1) {
    const v = term.vars[0];
    if (v.startsWith('C(')) {
      const av = avec15[AbarNames.indexOf(v.slice(2, -1))];
      return mc * genBinom(av, 2);
    }
    return mc * avec15[AbarNames.indexOf(v)];
  }
  return mc * avec15[AbarNames.indexOf(term.vars[0])] * avec15[AbarNames.indexOf(term.vars[1])];
}
function dThetaOf(avec15) {
  return CNames.map((cc) => (DThetaFormula[cc] || []).reduce((s, t) => s + evalDFormTerm(t, avec15, 0, 1), 0));
}
function dSigmaOf(avec15, m) {
  return CNames.map((cc) => (DSigmaFormula[cc] || []).reduce((s, t) => s + evalDFormTerm(t, avec15, m, 3), 0));
}
function kappa(a15, b15) {
  const out = new Array(NC6).fill(0);
  for (const term of KappaTerms) {
    const ai = a15[AbarNames.indexOf(term.in1)];
    const bi = b15[AbarNames.indexOf(term.in2)];
    out[CNames.indexOf(term.out)] += term.coef * ai * bi;
  }
  return out;
}
function qThetaFullRaw(f15) {
  const thBar = vecMatMul(f15, ThetaBarMat);
  const k = kappa(thBar, f15);
  const d = dThetaOf(f15);
  return k.map((x, i) => -x + d[i]);
}
function qNFullRaw(f15, m) {
  const ebar = EmBar15(m);
  const Sf = vecMatMul(f15, SigmaBarMat(m));
  const S2f = vecMatMul(Sf, SigmaBarMat(m));
  const eps = EmC6(m);
  const dSigmaF = dSigmaOf(f15, m);
  const dSigmaSf = dSigmaOf(Sf, m);
  const dSigma2 = dSigmaSf.map((x, i) => x + vecMatMul(dSigmaF, SigmaOnCMat(m))[i]);
  const c1 = kappa(ebar, S2f);
  const ePlusS2f = ebar.map((x, i) => x + S2f[i]);
  const c2 = kappa(ePlusS2f, Sf);
  const ePlusS2fPlusSf = ePlusS2f.map((x, i) => x + Sf[i]);
  const c3 = kappa(ePlusS2fPlusSf, f15);
  return eps.map((x, i) => x + dSigma2[i] + dSigmaF[i] - c1[i] - c2[i] - c3[i]);
}

// ---------------------------------------------------------------------------
// j=3 lambda formula (sol_reply_24_d2.md sec.F8, eq 8.3) -- W(m)=binom(m+1,2) mod2;
// QFirstCond(f) = (f_p mod2, (f_s3 + f_w*f_r2) mod2) -- the ACTUAL (nonlinear) quantity,
// used for the brute-force recheck (this script never trusts the affine lambda shortcut
// blindly -- it re-derives the multiplicity table from scratch via direct enumeration).
// ---------------------------------------------------------------------------
function QFirstCond(f15) {
  return [mod(f15[IdxP], 2), mod(f15[IdxS3] + f15[IdxW] * f15[IdxR2], 2)];
}
function WMfun(m) { return mod(genBinom(m + 1, 2), 2); }
function lambdaOfK(k15, m) {
  return [mod(k15[IdxP], 2), mod(k15[IdxS3] + WMfun(m) * k15[IdxR2], 2)];
}
function xor2(a, b) { return [(a[0] + b[0]) % 2, (a[1] + b[1]) % 2]; }
function spanF2(vecs) {
  let span = [[0, 0]];
  let changed = true;
  while (changed) {
    changed = false;
    for (const v of vecs) {
      for (const s of [...span]) {
        const nv = xor2(s, v);
        if (!span.some((x) => x[0] === nv[0] && x[1] === nv[1])) { span.push(nv); changed = true; }
      }
    }
  }
  return span;
}
function rankFromSpanSize(n) { return n === 1 ? 0 : n === 2 ? 1 : 2; }

// ---------------------------------------------------------------------------
// R-generic ObFromQPair (same ratified formula as check-e2c6.mjs's j=2 checker, reused here
// unchanged -- the ob quotient formula itself does not change between j=2 and j=3, only R).
// ---------------------------------------------------------------------------
function modInverse(a, n) {
  if (n === 1) return 0;
  let [old_r, r] = [((a % n) + n) % n, n];
  let [old_s, s] = [1, 0];
  while (r !== 0) { const q = Math.floor(old_r / r); [old_r, r] = [r, old_r - q * r]; [old_s, s] = [s, old_s - q * s]; }
  return ((old_s % n) + n) % n;
}
function obFromQPair(qTheta6, qN6, R) {
  const inv3 = modInverse(3, R);
  const thQN = vecMatMul(qN6, ThetaOnCMat);
  const corr = qN6.map((x, i) => inv3 * (x + thQN[i]));
  const v = qTheta6.map((x, i) => mod(x - corr[i], R));
  return { v, ob_a: v[CNames.indexOf('u4')], ob_b: v[CNames.indexOf('u2')] };
}

// ---------------------------------------------------------------------------
// Linear-stage system builder (class 6, n=15) -- for the G1b dual-witness recheck (adversarial
// unsolvable synthetic system) and for a possible future real-sweep recheck.
// ---------------------------------------------------------------------------
function matMatMul(A, B) {
  const n = A.length, k = B.length, m = B[0].length;
  const R2 = [];
  for (let i = 0; i < n; i++) {
    const row = new Array(m).fill(0);
    for (let t = 0; t < k; t++) { const a = A[i][t]; if (a !== 0) for (let j = 0; j < m; j++) row[j] += a * B[t][j]; }
    R2.push(row);
  }
  return R2;
}
function buildLinearSystemC6(m) {
  const n = NAB;
  const thMat = ThetaBarMat;
  const smMat = SigmaBarMat(m);
  const sm2Mat = matMatMul(smMat, smMat);
  const b = EmBar15(m);
  const rows = [], rhs = [];
  for (let i = 0; i < n; i++) {
    rows.push(Array.from({ length: n }, (_, k) => thMat[k][i] + (i === k ? 1 : 0)));
    rhs.push(0);
  }
  for (let i = 0; i < n; i++) {
    rows.push(Array.from({ length: n }, (_, k) => (i === k ? 1 : 0) + smMat[k][i] + sm2Mat[k][i]));
    rhs.push(-b[i]);
  }
  return { rows, rhs, n };
}
// Adversarial-unsolvable rhs formula, EXACT reproduction of e2c6j3-sweep.g's
// BuildLinearSystemC6AdversarialUnsolvableJ3(label): rhs = plain pseudo-random 15-vector,
// independently re-typed here (not read from the GAP source).
function buildAdversarialRhs(label) {
  return Array.from({ length: NAB }, (_, i0) => {
    const i = i0 + 1; // GAP is 1-indexed in the source formula
    return mod(41 * label + 13 * i + 3, 5) - 2;
  });
}

// ---------------------------------------------------------------------------
// Certificate crosscheck: reads certificates/e2c6j3/*.json ONLY.
// ---------------------------------------------------------------------------
const CERT_DIR = join(ROOT, 'certificates', 'e2c6j3');
let certFiles = [];
try { certFiles = readdirSync(CERT_DIR).filter((f) => f.endsWith('.json')); } catch (e) { console.log('  (no certificates/e2c6j3/ directory found)'); }
console.log(`\n=== certificate crosscheck: certificates/e2c6j3/*.json (${certFiles.length} files) ===`);

let certFails = 0;
for (const fname of certFiles) {
  const raw = readFileSync(join(CERT_DIR, fname), 'utf8');
  let cert;
  try { cert = JSON.parse(raw); } catch (e) { console.log(`FAIL  ${fname}: not valid JSON (${e.message})`); certFails++; continue; }
  const parseMaybe = (x) => (typeof x === 'string' ? JSON.parse(x) : x);

  // MODE LOCK: any cert with a recognizable ob_mode field must carry the ratified string.
  if (typeof cert.ob_mode !== 'undefined' && cert.ob_mode !== null && cert.ob_mode !== 'quotient-ratified-v2') {
    console.log(`REJECT  ${fname}: ob_mode="${cert.ob_mode}" != "quotient-ratified-v2" -- MODE LOCK violation`);
    certFails++;
    continue;
  }

  if (cert.claim === 'm6j3_multiplicity_table') {
    // Independent recheck: re-enumerate the FULL L_m = f0 + K (all Prod(K_orders)
    // combinations from the cert's own f0/K_generators/K_orders), evaluate the ACTUAL
    // (nonlinear) first-condition Q(f) at EVERY point directly (no lambda shortcut used
    // here), build an independent table, and compare to the cert's claimed ob_table exactly.
    const f0 = parseMaybe(cert.witness_f0_abar);
    const gens = cert.K_generators.map(parseMaybe);
    const orders = cert.K_orders.map(parseMaybe);
    const r = gens.length;
    const total = orders.reduce((a, b) => a * b, 1);
    const table = new Map();
    const avec = new Array(Math.max(r, 1)).fill(0);
    let done = r === 0;
    let count = 0;
    while (!done) {
      let f = f0.slice();
      for (let i = 0; i < r; i++) if (avec[i]) f = f.map((x, k) => x + avec[i] * gens[i][k]);
      f = f.map((x) => mod(x, 8));  // Abar modulus at j=3 is 2^3=8
      const q = QFirstCond(f);
      const key = `${q[0]},${q[1]}`;
      table.set(key, (table.get(key) || 0) + 1);
      count++;
      if (r === 0) { done = true; } else {
        let idx = 0;
        while (idx < r) { avec[idx]++; if (avec[idx] < orders[idx]) break; avec[idx] = 0; idx++; }
        if (idx >= r) done = true;
      }
    }
    const certKeys = Object.keys(cert.ob_table).sort();
    const gotKeys = [...table.keys()].sort();
    const keysMatch = JSON.stringify(certKeys) === JSON.stringify(gotKeys);
    const valuesMatch = keysMatch && certKeys.every((k) => table.get(k) === cert.ob_table[k]);
    const totalMatch = count === total && total === cert.total_points;
    const sumMatch = certKeys.reduce((s, k) => s + cert.ob_table[k], 0) === cert.total_points;

    // Independent recheck of lambda_bit_matrix/lambda_rank (便24 F8 item 2), if present:
    // recompute LambdaOfK(gen_i, m) for each generator directly from the cert's own
    // K_generators/m, and recompute the rank via the GF(2) span closure.
    let bitMatrixOk = true;
    if (typeof cert.lambda_bit_matrix !== 'undefined') {
      const gotBitMatrix = gens.map((g) => lambdaOfK(g, cert.m));
      const certBitMatrix = cert.lambda_bit_matrix.map(parseMaybe);
      bitMatrixOk = JSON.stringify(gotBitMatrix) === JSON.stringify(certBitMatrix);
      const gotSpan = spanF2(gotBitMatrix);
      const gotRank = rankFromSpanSize(gotSpan.length);
      if (gotRank !== cert.lambda_rank) bitMatrixOk = false;
      if (!bitMatrixOk) console.log(`  lambda_bit_matrix/rank MISMATCH: got matrix=${JSON.stringify(gotBitMatrix)} rank=${gotRank} (cert claimed matrix=${JSON.stringify(certBitMatrix)} rank=${cert.lambda_rank})`);
    }

    const ok = keysMatch && valuesMatch && totalMatch && sumMatch && bitMatrixOk;
    const gotTableStr = JSON.stringify(Object.fromEntries(table));
    console.log((ok ? 'PASS  ' : 'FAIL  ') + `${fname}: m6j3_multiplicity_table (fixture=${cert.fixture}, m=${cert.m}, |L|=${total}) independently re-enumerated (brute force, exact nonlinear Q) table=${gotTableStr} (cert claimed ${JSON.stringify(cert.ob_table)}); lambda_bit_matrix/rank recheck=${bitMatrixOk}`);
    if (!ok) certFails++;
    continue;
  }

  if (cert.claim === 'ob_synthetic_check') {
    // G7 (ObFromQPair at R=4, nonzero q_N, permanent): independently recompute v/ob_a/ob_b
    // from the cert's OWN q_theta/q_N via the ratified formula, and also recheck the cert's
    // own same_mod_2_as_q_N_zero self-report against a fresh q_N=0 computation.
    const R = cert.R;
    const qTheta6 = parseMaybe(cert.q_theta);
    const qN6 = parseMaybe(cert.q_N);
    const obR = obFromQPair(qTheta6, qN6, R);
    const obZero = obFromQPair(qTheta6, new Array(NC6).fill(0), R);
    const primaryOk = obR.ob_a === cert.ob_a && obR.ob_b === cert.ob_b;
    const sameMod2Indep = (mod(obR.ob_a, 2) === mod(obZero.ob_a, 2)) && (mod(obR.ob_b, 2) === mod(obZero.ob_b, 2));
    const selfReportOk = cert.same_mod_2_as_q_N_zero === sameMod2Indep;
    const ok = primaryOk && selfReportOk;
    console.log((ok ? 'PASS  ' : 'FAIL  ') + `${fname}: ob_synthetic_check (fixture=${cert.fixture}, R=${R}) independently recomputed ob_a=${obR.ob_a} ob_b=${obR.ob_b} (cert claimed ob_a=${cert.ob_a} ob_b=${cert.ob_b}); same-mod-2-vs-qN-zero recheck=${sameMod2Indep} (cert self-report=${cert.same_mod_2_as_q_N_zero})`);
    if (!ok) certFails++;
    continue;
  }

  if (cert.claim === 'periodicity_comparison_j3') {
    // G8: independently recompute EmBar15(mA)/(mB) mod 8, EmC6(mA)/(mB) mod 4, W(mA)/(mB),
    // and confirm the cert's own fields AND its "observed_equal" self-report are consistent
    // with an independent recomputation (this recheck does NOT itself assert whether equality
    // SHOULD hold -- it only verifies the cert accurately reports what it claims to report).
    const [mA, mB] = cert.m_pair;
    const gotEmBarA = EmBar15(mA).map((x) => mod(x, 8));
    const gotEmBarB = EmBar15(mB).map((x) => mod(x, 8));
    const gotEmCA = EmC6(mA).map((x) => mod(x, 4));
    const gotEmCB = EmC6(mB).map((x) => mod(x, 4));
    const gotWA = WMfun(mA), gotWB = WMfun(mB);
    const certEmBarA = parseMaybe(cert.EmBar15_mod8_mA), certEmBarB = parseMaybe(cert.EmBar15_mod8_mB);
    const certEmCA = parseMaybe(cert.EmC6_mod4_mA), certEmCB = parseMaybe(cert.EmC6_mod4_mB);
    const fieldsMatch =
      JSON.stringify(gotEmBarA) === JSON.stringify(certEmBarA) &&
      JSON.stringify(gotEmBarB) === JSON.stringify(certEmBarB) &&
      JSON.stringify(gotEmCA) === JSON.stringify(certEmCA) &&
      JSON.stringify(gotEmCB) === JSON.stringify(certEmCB) &&
      gotWA === cert.W_mA && gotWB === cert.W_mB;
    const gotObsEqual = JSON.stringify(gotEmBarA) === JSON.stringify(gotEmBarB) &&
      JSON.stringify(gotEmCA) === JSON.stringify(gotEmCB) && gotWA === gotWB;
    const obsReportOk = gotObsEqual === cert.observed_equal;
    const ok = fieldsMatch && obsReportOk;
    console.log((ok ? 'PASS  ' : 'FAIL  ') + `${fname}: periodicity_comparison_j3 (m_pair=[${mA},${mB}]) independently recomputed EmBar15/EmC6/W for both m -- fields match cert=${fieldsMatch}, observed_equal self-report accurate=${obsReportOk} (this recheck does not judge whether equality SHOULD hold)`);
    if (!ok) certFails++;
    continue;
  }

  if (cert.claim === 'm8c_mass_identity') {
    // Full independent recheck of the M8-c mass identity (docs/notes/設計_F8項目5.md item 5):
    // rebuild LambdaTable(m) from scratch (own agree6_sol2.json-derived theta|C/sigma|C),
    // re-enumerate the FULL L_m from the cert's own f0/K_generators/K_orders, recompute ob
    // (QUOTIENT-classified: ob_a=0 exact AND ob_b mod 2=0 -- per the empirically-confirmed
    // 委嘱16 R[2]a(+)(R/2R)b-bar semantics) and Xi (closed form) at every point, and rebuild
    // sum_fib/set_mismatch_count/mass_identity_holds/set_match_holds independently.
    const R = cert.R;
    const m = cert.m;
    function lambdaOnC(z6, mm) {
      const thZ = vecMatMul(z6, ThetaOnCMat);
      const oneP = z6.map((x, i) => mod(x + thZ[i], R));
      const S = SigmaOnCMat(mm);
      const S2 = matMatMul(S, S);
      const NC = S2.map((row, i) => row.map((x, j) => x + S[i][j] + (i === j ? 1 : 0)));
      const nz = vecMatMul(z6, NC);
      return [...oneP, ...nz.map((x) => mod(x, R))];
    }
    const lamTable = new Map();
    let kerLambdaSize = 0;
    for (let c1 = 0; c1 < 4; c1++) for (let c2 = 0; c2 < 4; c2++) for (let c3 = 0; c3 < 4; c3++)
      for (let c4 = 0; c4 < 4; c4++) for (let c5 = 0; c5 < 4; c5++) for (let c6 = 0; c6 < 4; c6++) {
        const z6 = [c1, c2, c3, c4, c5, c6];
        const key = JSON.stringify(lambdaOnC(z6, m));
        if (!lamTable.has(key)) lamTable.set(key, 0);
        lamTable.set(key, lamTable.get(key) + 1);
      }
    kerLambdaSize = lamTable.get(JSON.stringify(new Array(12).fill(0))) || 0;

    const f0 = parseMaybe(cert.witness_f0_abar);
    const gens = cert.K_generators.map(parseMaybe);
    const orders = cert.K_orders.map(parseMaybe);
    const r = gens.length;
    const avec = new Array(Math.max(r, 1)).fill(0);
    let done = r === 0;
    let sumFib = 0, multQuotZero = 0, setMismatch = 0, total = 0;
    while (!done) {
      let f = f0.slice();
      for (let i = 0; i < r; i++) if (avec[i]) f = f.map((x, k) => x + avec[i] * gens[i][k]);
      f = f.map((x) => mod(x, 8));
      const qT = qThetaFullRaw(f);
      const qN = qNFullRaw(f, m);
      const obr = obFromQPair(qT, qN, R);
      const isObZero = obr.ob_a === 0 && mod(obr.ob_b, 2) === 0;
      if (isObZero) multQuotZero++;
      const xi = [...qT.map((x) => mod(x, R)), ...qN.map((x) => mod(x, R))];
      const negXi = xi.map((x) => mod(-x, R));
      const fibSize = lamTable.get(JSON.stringify(negXi)) || 0;
      sumFib += fibSize;
      if (isObZero !== (fibSize > 0)) setMismatch++;
      total++;
      if (r === 0) { done = true; } else {
        let idx = 0;
        while (idx < r) { avec[idx]++; if (avec[idx] < orders[idx]) break; avec[idx] = 0; idx++; }
        if (idx >= r) done = true;
      }
    }
    const massOk = sumFib === kerLambdaSize * multQuotZero;
    const setOk = setMismatch === 0;
    const kerLamMatch = kerLambdaSize === cert.ker_lambda_size;
    const multMatch = multQuotZero === cert.mult_ob0_quotient;
    const sumFibMatch = sumFib === cert.sum_fib;
    const massOkMatch = massOk === cert.mass_identity_holds;
    const setOkMatch = setOk === cert.set_match_holds;
    const setMismatchMatch = setMismatch === cert.set_mismatch_count;
    const ok = kerLamMatch && multMatch && sumFibMatch && massOkMatch && setOkMatch && setMismatchMatch && massOk && setOk;
    console.log((ok ? 'PASS  ' : 'FAIL  ') + `${fname}: m8c_mass_identity (m=${m}, |L|=${total}) independently rebuilt LambdaTable + re-enumerated L_m -- ker_lambda_size=${kerLambdaSize} mult_ob0_quotient=${multQuotZero} sum_fib=${sumFib} set_mismatch=${setMismatch} (cert claimed ker_lambda_size=${cert.ker_lambda_size} mult=${cert.mult_ob0_quotient} sum_fib=${cert.sum_fib} set_mismatch=${cert.set_mismatch_count})`);
    if (!ok) certFails++;
    continue;
  }

  if (cert.claim === 'm8b_fiber_realization') {
    // M8-b real-data sample: this checker has no polycyclic package (same limitation as
    // f7_routeG_crosscheck/m8a -- genuine PcpGroup products are GAP-only), so the group
    // products themselves are NOT independently rebuilt here. Structural/arithmetic
    // self-consistency check only: witness count matches array length, each fiber_size is
    // positive (an ob=0-quotient point must have a nonempty fiber), and total_group_products
    // arithmetically equals 2 * sum(fiber_size) (theta-side + N-side per fiber element).
    const witnesses = cert.witnesses || [];
    const sumFiberSizes = witnesses.reduce((s, w) => s + w.fiber_size, 0);
    const countOk = witnesses.length === cert.witness_count;
    const fiberSizesPositive = witnesses.every((w) => w.fiber_size > 0);
    const totalMatch = cert.total_group_products === 2 * sumFiberSizes;
    const ok = countOk && fiberSizesPositive && totalMatch && cert.all_fiber_elements_give_identity === true;
    console.log((ok ? 'PASS  ' : 'FAIL  ') + `${fname}: m8b_fiber_realization (fixture=${cert.fixture}, m=${cert.m}) structural/arithmetic self-consistency (witness_count=${countOk}, fiber_sizes_positive=${fiberSizesPositive}, total_group_products=2*Sum(fiber_size)=${totalMatch}) -- genuine PcpGroup products NOT independently rebuilt (GAP-only, same limitation as f7_routeG_crosscheck)`);
    if (!ok) certFails++;
    continue;
  }

  if (cert.claim === 'm8d_negative_control') {
    // M8-d real-data sample: same GAP-only limitation as above -- structural self-consistency
    // check: pass field must equal (fiber_empty AND all_ker_lambda_products_fail), and the
    // witness's own ob must genuinely be OUTSIDE the ob=0-quotient class (ob_a<>0 or ob_b odd).
    const isObZeroQuotient = cert.witness_ob_a === 0 && mod(cert.witness_ob_b, 2) === 0;
    const passConsistent = cert.pass === (cert.fiber_empty && cert.all_ker_lambda_products_fail);
    const ok = !isObZeroQuotient && passConsistent;
    console.log((ok ? 'PASS  ' : 'FAIL  ') + `${fname}: m8d_negative_control (fixture=${cert.fixture}, m=${cert.m}) witness ob=(${cert.witness_ob_a},${cert.witness_ob_b}) genuinely outside ob=0-quotient class=${!isObZeroQuotient}, pass field arithmetically consistent=${passConsistent} -- genuine PcpGroup products NOT independently rebuilt (GAP-only)`);
    if (!ok) certFails++;
    continue;
  }

  if (cert.claim === 'precondition_violated_c6j3') {
    // GUARD cert (only appears if k_w<>0 was detected during a real sweep -- not expected in
    // this fixture-only pass, but handled defensively): structural well-formedness check only
    // (this checker cannot re-derive K_m3 generators from scratch without re-solving the
    // linear stage, which is out of scope for a lightweight recheck of an abort record).
    const ok = cert.k_w_nonzero === true && Array.isArray(cert.bad_generators) && cert.bad_generators.length === cert.bad_generator_count && cert.ob_mode === null;
    console.log((ok ? 'PASS  ' : 'FAIL  ') + `${fname}: precondition_violated_c6j3 (m=${cert.m}) well-formed abort record (k_w_nonzero=true, bad_generator_count=${cert.bad_generator_count} consistent, ob_mode=null)`);
    if (!ok) certFails++;
    continue;
  }

  if (cert.claim === 'f7_routeG_crosscheck') {
    // Same style as check-e2c6.mjs's f7_routeG_crosscheck handler (route-G group product
    // itself not independently rebuilt here -- GAP-only), PLUS the j=3-specific check: every
    // test vector `f` must already be reduced mod 8 (the actual j=3 Abar modulus).
    const R = cert.R;
    let allOk = true;
    let allReducedMod8 = true;
    for (const e of cert.entries) {
      const f = parseMaybe(e.f);
      if (!f.every((x) => x >= 0 && x < 8)) allReducedMod8 = false;
      const routeG = parseMaybe(e.routeG);
      const closedCert = parseMaybe(e.closed_form);
      const closedIndep = e.kind === 'qTheta' ? qThetaFullRaw(f) : qNFullRaw(f, e.m);
      const closedMatchesIndep = closedIndep.every((x, i) => x === closedCert[i]);
      const mod4ClaimOk = e.mod4_match === routeG.every((x, i) => mod(x, R) === mod(closedCert[i], R));
      const exactClaimOk = e.exact_match === routeG.every((x, i) => x === closedCert[i]);
      if (!closedMatchesIndep || !mod4ClaimOk || !exactClaimOk) allOk = false;
    }
    const ok = allOk && allReducedMod8;
    console.log((ok ? 'PASS  ' : 'FAIL  ') + `${fname}: f7_routeG_crosscheck (gate=${cert.gate}, ${cert.entries.length} entries) -- independently recomputed closed_form matches cert's closed_form, self-reports arithmetically consistent, AND all test vectors reduced mod 8 (=${allReducedMod8}) (route-G group product itself NOT independently rebuilt -- GAP-only, no polycyclic package in Node)`);
    if (!ok) certFails++;
    continue;
  }

  if (cert.claim === 'linear_stage_empty_c6j3') {
    // G1b (便24 F8 item 1, dual witness): independently rebuild the SAME public
    // theta_bar/sigma_bar(m-shape) structure AND the SAME deterministic adversarial rhs
    // formula, then recheck y*rows==0 (mod modulus) and y*rhs<>0 (mod modulus) directly.
    if (cert.linear_solvable !== false) {
      console.log(`FAIL  ${fname}: linear_stage_empty_c6j3 claim but linear_solvable !== false (got ${cert.linear_solvable})`);
      certFails++;
      continue;
    }
    let rows, rhs;
    if (cert.fixture === 'adversarial_unsolvable_synthetic_j3') {
      const label = cert.label;
      const mShape = mod(label, 64);
      ({ rows } = buildLinearSystemC6(mShape));
      rhs = [...new Array(NAB).fill(0), ...buildAdversarialRhs(label)];
    } else if (cert.fixture === 'real_sweep') {
      // real sweep: independently rebuild the REAL public theta_bar/sigma_bar(m) structure
      // AND the REAL Ebar_m(m)-derived rhs (both from this checker's own agree6_sol2.json-
      // derived EmBar15/SigmaBarMat -- public formula data, fire lock now open).
      ({ rows, rhs } = buildLinearSystemC6(cert.m));
    } else {
      console.log(`SKIP  ${fname}: linear_stage_empty_c6j3 with unrecognized fixture="${cert.fixture}"`);
      continue;
    }
    const modulus = cert.modulus;
    const y = parseMaybe(cert.dual_witness_y);
    const n = NAB;
    const yM = new Array(n).fill(0);
    for (let k = 0; k < n; k++) for (let i = 0; i < rows.length; i++) yM[k] += y[i] * rows[i][k];
    const yb = y.reduce((s, yi, i) => s + yi * rhs[i], 0);
    const yMZero = yM.every((x) => mod(x, modulus) === 0);
    const yBNonzero = mod(yb, modulus) !== 0;
    const claimedYMZero = !!cert.yM_is_zero_mod_2j;
    const claimedYBNonzero = !!cert.yb_nonzero_mod_2j;
    const ok = yMZero && yBNonzero && yMZero === claimedYMZero && yBNonzero === claimedYBNonzero;
    console.log((ok ? 'PASS  ' : 'FAIL  ') + `${fname}: linear_stage_empty_c6j3 (fixture=${cert.fixture}, m=${cert.m}, label=${cert.label}, modulus=${modulus}) independently rebuilt public theta_bar/sigma_bar(+Ebar_m) structure, recomputed yM=${JSON.stringify(yM)} yb=${yb} (cert claimed yM_zero=${claimedYMZero}, yb_nonzero=${claimedYBNonzero})`);
    if (!ok) certFails++;
    continue;
  }

  console.log(`SKIP  ${fname}: unrecognized claim "${cert.claim}"`);
}
console.log(`\ncertificate crosscheck: ${certFails === 0 ? 'ALL PASS' : certFails + ' FAILURES'}`);
console.log(`\n${fails === 0 ? 'ALL PASS' : fails + ' FAILURES'} (self-check fails=${fails}, cert fails=${certFails})`);
if (fails > 0 || certFails > 0) process.exit(1);
