// crosscheck/check-e2c6.mjs
// Independent Node-side crosscheck for search/e2c6-sweep.g (E2 class-6 two-direction sweep,
// docs/manifest_e2c6_sweep_v2.md).
//
// === TOOL SPEC (first of its kind, per 体制と道具.md "仕様書優先", 2026-07-26 researcher ruling) ===
//
// (1) INPUT (files and roles):
//   - crosscheck/agree6_sol2.json    : ONLY source for class-6 table data (theta_table,
//     sigma_table_poly, Em_components, kappa_terms, d_theta_formula, d_sigma_formula). This is
//     system B (Sol's independent transcription) -- NOT agree6_claude.json (system A, used by
//     the GAP side) -- input-level system separation is the whole point of having two files.
//   - certificates/e2c6/*.json       : the only other input. Certificates written by
//     search/e2c6-sweep.g. This script does NOT read e2c6-sweep.g's source, hall6.mjs, or sol/.
//   - The RATIFIED OB FORMULA (as opposed to the class-6 table data) is taken from the same
//     commander-designated spec docs as the GAP side: docs/manifest_e2c6_sweep_v2.md,
//     docs/委嘱16_ob定義_opus_v1.md, sol/sol_reply_22_ob.md.
//
// (2) MODES (what data each mode may touch):
//   - fixture mode (the only mode this script runs): rechecks certificates whose "fixture"
//     field names a SYNTHETIC system (rhs=0, or a hand-built (q_theta,q_N) pair) or the
//     class-5 CONTROL system (independent Magnus-embedding reimplementation, dim 10). This
//     mode NEVER computes or discloses real E_m(m)-based class-6 target solvability/ob for
//     m>0 -- the one exception is m=0, where Ebar_15(0)=EmC6(0)=0 is a known STRUCTURAL
//     identity (not a "finding" about the real 64-system sweep), used only inside
//     e2c6-sweep.g's own M2 self-check (this script does not need to re-derive that).
//   - real-sweep mode: NOT implemented on the Node side. If a certificate ever appears with
//     claim "e2c6_real_sweep", this script rechecks it the same way as any other ob-bearing
//     certificate (same ratified formula, same mode-lock gate below) -- it does not
//     distinguish "is this real data" from "is this fixture data" when RECHECKING math, only
//     when deciding whether to print an extra disclosure warning (see FIRE LOCK note below).
//
// (3) OUTPUT (certificate schema this script consumes):
//   - claim:"linear_stage_kernel_c6"  : {modulus,m,j,K_generators,K_orders,ob_a:null,
//     ob_b:null,ob_mode:"PENDING",fixture}. Pure kernel cert, no ob content expected.
//   - claim:"ob_synthetic_check"      : {fixture,R,basis_order_C6,q_theta,q_N,v,ob_a,ob_b,
//     ob_mode,formula}. ob_a/ob_b non-null -- MODE LOCK applies (see below).
//   - claim:"e2c6_real_sweep"         : {m,j,linear_solvable,witness_f_abar,q_theta,q_N,
//     ob_a,ob_b,ob_mode}. Only ever appears once the fire lock is opened; same mode lock.
//   - Ratified ob_mode string: "quotient-ratified-v2" (裁定20). Any OTHER string paired with
//     non-null ob_a/ob_b is a contract violation (see MODE LOCK).
//
// (4) INVARIANTS checked at runtime (M-series, 委嘱16 sec.5 / manifest v2 F4):
//   - M2: (1-sigma)q_N = 0 mod R          -- checked GAP-side only (needs real Em(0)=0 shortcut)
//   - M3: (1-theta)q_theta = 0 mod R      -- checked GAP-side only (m-independent, safe)
//   - M5: (1+theta)ker(N_C) has zero u4/u2 mod R -- checked GAP-side only
//   - This script's own invariants: (a) K-generators satisfy the homogeneous kernel equations
//     mod `modulus` for their declared fixture system; (b) kernel enumeration is bijective
//     (|distinct| = Prod(K_orders)); (c) for ob-bearing certs, v/ob_a/ob_b are independently
//     recomputed from the certificate's own (q_theta,q_N) via the ratified formula and must
//     match: MODE LOCK -- ob_a/ob_b non-null with ob_mode != "quotient-ratified-v2" is REJECT.
//
// (5) FIRE LOCK (specified here for completeness; this script does not enforce it -- that is
//     search/e2c6-sweep.g's job): the real-universe sweep (real m=0..63, claim
//     "e2c6_real_sweep") only runs when search/FIRE_e2c6.auth exists and contains the SHA-256
//     of docs/manifest_e2c6_sweep_v2.md. This checker has no opinion on whether that file
//     should exist -- it only rechecks whatever certificates are actually present.
//
// STATUS (2026-07-26, second pass): ob layer RATIFIED (裁定20). MODE LOCK enforced below --
// any ob-bearing certificate not carrying "ob_mode":"quotient-ratified-v2" is REJECTed.

'use strict';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
const __dirname_ = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname_, '..');

const sol2 = JSON.parse(readFileSync(join(ROOT, 'crosscheck', 'agree6_sol2.json'), 'utf8'));
const BASIS21 = sol2.meta.basis_order; // 21 names, independently transcribed by Sol
if (BASIS21.length !== 21) throw new Error('unexpected basis length');

let fails = 0;
const TT = (name, cond, extra = '') => {
  console.log((cond ? 'PASS  ' : 'FAIL  ') + name + (extra ? '   ' + extra : ''));
  if (!cond) fails++;
};
console.log('=== crosscheck/check-e2c6.mjs (independent Node reimplementation, input=agree6_sol2.json) ===');

// ---------------------------------------------------------------------------
// Full 21x21 operators from sol2's theta_table / sigma_table_poly / Em_components
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
function matMatMul(A, B) {
  const n = A.length, k = B.length, m = B[0].length;
  const R = [];
  for (let i = 0; i < n; i++) {
    const row = new Array(m).fill(0);
    for (let t = 0; t < k; t++) { const a = A[i][t]; if (a !== 0) for (let j = 0; j < m; j++) row[j] += a * B[t][j]; }
    R.push(row);
  }
  return R;
}

// ---------------------------------------------------------------------------
// SELF-CHECK 1: theta^2 = id on all 21 generators
// ---------------------------------------------------------------------------
function ek21(i) { const v = new Array(21).fill(0); v[i] = 1; return v; }
let thetaSqOk = true;
for (let k = 0; k < 21; k++) {
  const t1 = vecMatMul(ek21(k), ThetaTable21);
  const t2 = vecMatMul(t1, ThetaTable21);
  if (!t2.every((x, i) => x === ek21(k)[i])) thetaSqOk = false;
}
TT('theta^2 = id on all 21 BASIS21 generators (agree6_sol2.json transcription self-check)', thetaSqOk);

// ---------------------------------------------------------------------------
// Abar (15) / C (6) index split
// ---------------------------------------------------------------------------
const AbarNames = ['w', 'p', 'q', 'r1', 'r2', 'r3', 't1', 't2', 't3', 't4', 's1', 's2', 's3', 's4', 's5'];
const CNames = ['t5', 't6', 'u1', 'u2', 'u3', 'u4'];
const nameIdx21 = (nm) => BASIS21.indexOf(nm);
const AbarIdx21 = AbarNames.map(nameIdx21);
const CIdx21 = CNames.map(nameIdx21);
const NAB = AbarNames.length, NC6 = CNames.length;

const ThetaBarMat = AbarIdx21.map((i) => AbarIdx21.map((j) => ThetaTable21[i][j]));
function SigmaBarMat(m) { return AbarIdx21.map((i) => AbarIdx21.map((j) => evalPoly5(SigmaTablePoly21[i][j], m))); }
function EmBar15(m) { return AbarIdx21.map((i) => evalEmComponent(EmComponents21[i], m)); }

// ---------------------------------------------------------------------------
// SELF-CHECK 2: d_theta_formula / d_sigma_formula linear (single-generator) readout matches
// theta_table / sigma_table_poly's own C-columns.
// ---------------------------------------------------------------------------
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
function ekAbar(i) { const v = new Array(NAB).fill(0); v[i] = 1; return v; }

// ---------------------------------------------------------------------------
// RATIFIED OB LAYER (裁定20): ob = [q_theta - 3^{-1}(1+theta)q_N] in C^theta/(1+theta)K.
// j=2 readout (R=2): ob_a = v's u4-coefficient, ob_b = v's u2-coefficient.
// ---------------------------------------------------------------------------
const ThetaOnCMat = CIdx21.map((i) => CIdx21.map((j) => ThetaTable21[i][j]));
function SigmaOnCMat(m) { return CIdx21.map((i) => CIdx21.map((j) => evalPoly5(SigmaTablePoly21[i][j], m))); }
function EmC6(m) { return CIdx21.map((i) => evalEmComponent(EmComponents21[i], m)); }
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
  return k.map((x, i) => x + d[i]);
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
  return eps.map((x, i) => x + dSigma2[i] + dSigmaF[i] + c1[i] + c2[i] + c3[i]);
}
function modInverse(a, n) {
  if (n === 1) return 0;
  // extended Euclid
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

let dThetaOk = true, dSigmaOk = true;
for (let g = 0; g < NAB; g++) {
  const got = dThetaOf(ekAbar(g));
  const want = CIdx21.map((ci) => ThetaTable21[AbarIdx21[g]][ci]);
  if (!got.every((x, i) => x === want[i])) { dThetaOk = false; console.log(`  MISMATCH d_theta(${AbarNames[g]}): got=${got} want=${want}`); }
  for (const mtest of [0, 7]) {
    const got2 = dSigmaOf(ekAbar(g), mtest);
    const want2 = CIdx21.map((ci) => evalPoly5(SigmaTablePoly21[AbarIdx21[g]][ci], mtest));
    if (!got2.every((x, i) => x === want2[i])) { dSigmaOk = false; console.log(`  MISMATCH d_sigma(${AbarNames[g]},m=${mtest}): got=${got2} want=${want2}`); }
  }
}
TT('d_theta_formula(e_g) matches theta_table own C-columns (all 15 Abar generators)', dThetaOk);
TT('d_sigma_formula(e_g,m) matches sigma_table_poly own C-columns (m=0,7; all 15 Abar generators)', dSigmaOk);

// ---------------------------------------------------------------------------
// Linear-stage system builder (class 6, n=15), for certificate rechecking only (this
// checker does NOT run its own SNF/solve -- it verifies GAP's certificate claims directly,
// same discipline as crosscheck/check-e2-action.mjs's certificate-crosscheck section).
// ---------------------------------------------------------------------------
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

// ---------------------------------------------------------------------------
// Class-5 CONTROL model (independent JS reimplementation of the classical truncated Magnus
// embedding, degree 3, dim 10 -- generic combinatorics, not read from any GAP file).
// ---------------------------------------------------------------------------
const DG5 = 3;
const BASIS5 = [];
const IDX5 = new Map();
for (let d = 0; d <= DG5; d++) for (let a = d; a >= 0; a--) { const b = d - a; IDX5.set(`${a},${b}`, BASIS5.length); BASIS5.push([a, b]); }
const NN5 = BASIS5.length; // 10
function zeroP5() { return new Array(NN5).fill(0); }
function constP5(c) { const v = zeroP5(); if (c !== 0) v[IDX5.get('0,0')] = c; return v; }
function sgen5() { const v = zeroP5(); v[IDX5.get('1,0')] = 1; return v; }
function tgen5() { const v = zeroP5(); v[IDX5.get('0,1')] = 1; return v; }
function padd5(u, v) { return u.map((x, i) => x + v[i]); }
function psub5(u, v) { return u.map((x, i) => x - v[i]); }
function pmul5(u, v) {
  const r = zeroP5();
  for (let i = 0; i < NN5; i++) if (u[i] !== 0) {
    const [a1, b1] = BASIS5[i];
    for (let j = 0; j < NN5; j++) if (v[j] !== 0) {
      const [a2, b2] = BASIS5[j];
      if (a1 + a2 + b1 + b2 <= DG5) { const idx = IDX5.get(`${a1 + a2},${b1 + b2}`); r[idx] += u[i] * v[j]; }
    }
  }
  return r;
}
function ppow5(u, k) { let r = constP5(1), b = u.slice(); let n = k; while (n > 0) { if (n & 1) r = pmul5(r, b); b = pmul5(b, b); n >>= 1; } return r; }
function pinvUnit5(u) { const x = psub5(u, constP5(1)); let r = constP5(1), t = constP5(1); for (let i = 1; i <= DG5; i++) { t = pmul5(t, x); r = i % 2 ? psub5(r, t) : padd5(r, t); } return r; }
function sunit5() { return padd5(constP5(1), sgen5()); }
function tunit5() { return padd5(constP5(1), tgen5()); }
function psubst5(f, U, V) {
  let r = zeroP5();
  const Up = [constP5(1)], Vp = [constP5(1)];
  for (let i = 1; i <= DG5; i++) { Up.push(pmul5(Up[i - 1], U)); Vp.push(pmul5(Vp[i - 1], V)); }
  for (let i = 0; i < NN5; i++) if (f[i] !== 0) {
    const [a, b] = BASIS5[i];
    if (a + b <= DG5) r = padd5(r, pmul5(Up[a], Vp[b]).map((x) => x * f[i]));
  }
  return r;
}
function thetaP5(f) { return psubst5(f, tgen5(), sgen5()).map((x) => -x); }
function tauP5(f) {
  const invs = pinvUnit5(sunit5()), invt = pinvUnit5(tunit5());
  const rho = psub5(pmul5(invs, invt), constP5(1));
  return pmul5(psubst5(f, tgen5(), rho), invs);
}
function sigmaP5(f, m) { return pmul5(ppow5(tunit5(), m), tauP5(f)); }
function emP5(m) {
  if (m === 0) return zeroP5();
  const s = sunit5(), t = tunit5(), st = pmul5(s, t);
  const AA = (u, n) => { let r = zeroP5(), p = constP5(1); for (let i = 0; i < n; i++) { r = padd5(r, p); p = pmul5(p, u); } return r; };
  let c = zeroP5();
  for (let k = 2; k <= m; k++) c = padd5(pmul5(t, AA(st, k - 1)), pmul5(t, c));
  const invsm = ppow5(pinvUnit5(s), m);
  return psub5(c, pmul5(invsm, pmul5(AA(s, m), AA(st, m))));
}
function matOf5(op) { const M = []; for (let i = 0; i < NN5; i++) { const e = zeroP5(); e[i] = 1; M.push(op(e)); } return M; }
function buildLinearSystemC5(m) {
  const n = NN5;
  const thMat = matOf5(thetaP5);
  const smMat = matOf5((x) => sigmaP5(x, m));
  const sm2Mat = matMatMul(smMat, smMat);
  const b = emP5(m);
  const rows = [], rhs = [];
  for (let i = 0; i < n; i++) { rows.push(Array.from({ length: n }, (_, k) => thMat[k][i] + (i === k ? 1 : 0))); rhs.push(0); }
  for (let i = 0; i < n; i++) { rows.push(Array.from({ length: n }, (_, k) => (i === k ? 1 : 0) + smMat[k][i] + sm2Mat[k][i])); rhs.push(-b[i]); }
  return { rows, rhs, n };
}

function mod(x, m) { const r = x % m; return r < 0 ? r + m : r; }

// ---------------------------------------------------------------------------
// Certificate crosscheck: reads certificates/e2c6/*.json ONLY (not e2c6-sweep.g's source).
// ---------------------------------------------------------------------------
const CERT_DIR = join(ROOT, 'certificates', 'e2c6');
let certFiles = [];
try { certFiles = readdirSync(CERT_DIR).filter((f) => f.endsWith('.json')); } catch (e) { console.log('  (no certificates/e2c6/ directory found)'); }
console.log(`\n=== certificate crosscheck: certificates/e2c6/*.json (${certFiles.length} files) ===`);

let certFails = 0;
for (const fname of certFiles) {
  const raw = readFileSync(join(CERT_DIR, fname), 'utf8');
  let cert;
  try { cert = JSON.parse(raw); } catch (e) { console.log(`FAIL  ${fname}: not valid JSON (${e.message})`); certFails++; continue; }
  const parseMaybe = (x) => (typeof x === 'string' ? JSON.parse(x) : x);

  // MODE LOCK (applies to every claim type): any certificate carrying a non-null ob_a or
  // ob_b MUST declare "ob_mode":"quotient-ratified-v2" -- the one ratified string (裁定20).
  // Anything else (e.g. "PENDING" with non-null values, an old "A"/"B" label, a typo) is a
  // REJECT, full stop, regardless of what the numeric values happen to be.
  const obANonNull = typeof cert.ob_a !== 'undefined' && cert.ob_a !== null;
  const obBNonNull = typeof cert.ob_b !== 'undefined' && cert.ob_b !== null;
  if ((obANonNull || obBNonNull) && cert.ob_mode !== 'quotient-ratified-v2') {
    console.log(`REJECT  ${fname}: ob_a/ob_b non-null (ob_a=${cert.ob_a}, ob_b=${cert.ob_b}) but ob_mode="${cert.ob_mode}" != "quotient-ratified-v2" -- MODE LOCK violation`);
    certFails++;
    continue;
  }

  if (cert.claim === 'ob_synthetic_check') {
    // Independent recheck: recompute v/ob_a/ob_b from the certificate's OWN q_theta/q_N
    // (given directly in the cert -- these are synthetic/hand-built pairs for F1/F2, not
    // derived from any Abar witness) using the ratified formula, and compare.
    const R = cert.R;
    const qTheta6 = parseMaybe(cert.q_theta);
    const qN6 = parseMaybe(cert.q_N);
    const obR = obFromQPair(qTheta6, qN6, R);
    const ok = obR.ob_a === cert.ob_a && obR.ob_b === cert.ob_b;
    console.log((ok ? 'PASS  ' : 'FAIL  ') + `${fname}: ob_synthetic_check (fixture=${cert.fixture}, R=${R}) independently recomputed ob_a=${obR.ob_a} ob_b=${obR.ob_b} (cert claimed ob_a=${cert.ob_a} ob_b=${cert.ob_b})`);
    if (!ok) certFails++;
    continue;
  }

  if (cert.claim === 'e2c6_real_sweep') {
    // Same recheck, but q_theta/q_N are given directly in the cert too (per e2c6-sweep.g's
    // RunRealSweepC6 schema) -- no need to recompute them from witness_f_abar independently
    // (that would require this file's own Abar(15)/C(6) machinery applied to the witness,
    // which is exactly what qThetaFullRaw/qNFullRaw below already do if ever needed).
    // HARDENED (2026-07-26 commander): explicit check that linear_solvable === true (strict),
    // not just "truthy" -- catches a missing/undefined field rather than silently passing.
    if (cert.linear_solvable !== true) {
      console.log(`FAIL  ${fname}: e2c6_real_sweep claim but linear_solvable !== true (got ${cert.linear_solvable})`);
      certFails++;
      continue;
    }
    const R = 2 ** (cert.j - 1);
    const qTheta6 = parseMaybe(cert.q_theta);
    const qN6 = parseMaybe(cert.q_N);
    const obR = obFromQPair(qTheta6, qN6, R);
    const fAbar = parseMaybe(cert.witness_f_abar);
    const qThetaIndep = qThetaFullRaw(fAbar);
    const qNIndep = qNFullRaw(fAbar, cert.m);
    const qOk = qThetaIndep.every((x, i) => mod(x, R) === mod(qTheta6[i], R)) && qNIndep.every((x, i) => mod(x, R) === mod(qN6[i], R));
    const ok = qOk && obR.ob_a === cert.ob_a && obR.ob_b === cert.ob_b;
    console.log((ok ? 'PASS  ' : 'FAIL  ') + `${fname}: e2c6_real_sweep (m=${cert.m}, j=${cert.j}) independently rebuilt q_theta/q_N from witness_f_abar AND recomputed ob_a=${obR.ob_a} ob_b=${obR.ob_b} (cert claimed ob_a=${cert.ob_a} ob_b=${cert.ob_b})`);
    if (!ok) certFails++;
    continue;
  }

  if (cert.claim === 'linear_stage_empty_c6') {
    // Negative certificate (linear stage unsolvable at this m): independently rebuild the
    // REAL system (real Em_bar(m), now that the fire lock has authorized real-sweep
    // disclosure) and recheck the dual witness y: y*rows === 0 (mod modulus) and
    // y*rhs !== 0 (mod modulus).
    // HARDENED (2026-07-26 commander): explicit strict check linear_solvable === false --
    // the underlying bug (field missing entirely, so `cert.linear_solvable === false` was
    // ALWAYS false for old certs, i.e. this check would have wrongly FAILED every legitimate
    // unsolvable cert once added naively) is fixed at the SOURCE (e2c6-sweep.g now always
    // writes the field); this checker requires it be present and exactly false.
    if (cert.linear_solvable !== false) {
      console.log(`FAIL  ${fname}: linear_stage_empty_c6 claim but linear_solvable !== false (got ${cert.linear_solvable})`);
      certFails++;
      continue;
    }
    const modulus = cert.modulus;
    const y = parseMaybe(cert.dual_witness_y);
    let rows, rhs, n;
    if (cert.fixture === 'real_sweep') {
      ({ rows, rhs, n } = buildLinearSystemC6(cert.m));
    } else {
      console.log(`SKIP  ${fname}: linear_stage_empty_c6 with unrecognized fixture "${cert.fixture}"`);
      continue;
    }
    const yM = new Array(n).fill(0);
    for (let k = 0; k < n; k++) for (let i = 0; i < rows.length; i++) yM[k] += y[i] * rows[i][k];
    const yb = y.reduce((s, yi, i) => s + yi * rhs[i], 0);
    const yMZero = yM.every((x) => mod(x, modulus) === 0);
    const yBNonzero = mod(yb, modulus) !== 0;
    const claimedYMZero = !!(cert.yM_is_zero ?? cert.yM_is_zero_mod_2j);
    const claimedYBNonzero = !!cert.yb_nonzero_mod_2j;
    const ok = yMZero && yBNonzero && yMZero === claimedYMZero && yBNonzero === claimedYBNonzero;
    console.log((ok ? 'PASS  ' : 'FAIL  ') + `${fname}: linear_stage_empty_c6 (fixture=${cert.fixture}, m=${cert.m}, modulus=${modulus}) independently recomputed yM=${JSON.stringify(yM)} yb=${yb} (cert claimed yM_zero=${claimedYMZero}, yb_nonzero=${claimedYBNonzero})`);
    if (!ok) certFails++;
    continue;
  }

  if (cert.claim !== 'linear_stage_kernel_c6') {
    console.log(`SKIP  ${fname}: unrecognized claim "${cert.claim}"`);
    continue;
  }

  const modulus = cert.modulus, j = cert.j, m = cert.m;
  const gens = cert.K_generators.map(parseMaybe);
  const orders = cert.K_orders.map(parseMaybe);

  let rows, rhs, n;
  if (cert.fixture === 'fixture_ii_class5_control') {
    ({ rows, rhs, n } = buildLinearSystemC5(m));
  } else if (cert.fixture === 'fixture_iii_mass_check_synthetic_rhs0') {
    ({ rows, rhs, n } = buildLinearSystemC6(m));
    rhs = new Array(2 * n).fill(0); // synthetic: rhs overwritten to 0, per e2c6-sweep.g's own labeling
  } else if (cert.fixture === 'fixture_F5_pseudorandom_rhs') {
    // F5: cert.m is the PRNG SEED, not the sigma_bar shape parameter (m mod 64 is). The
    // K-generator recheck (M*e === 0 mod modulus) and mass-check bijectivity are both
    // rhs-independent, so rhs is irrelevant here regardless -- only the real theta_bar/
    // sigma_bar STRUCTURE (public table data) at m%64 is needed to rebuild `rows`.
    ({ rows, n } = buildLinearSystemC6(((m % 64) + 64) % 64));
    rhs = new Array(2 * n).fill(0); // placeholder; unused by the kernel/bijectivity checks below
  } else {
    console.log(`SKIP  ${fname}: unrecognized fixture label "${cert.fixture}"`);
    continue;
  }

  // recheck each generator: K-generators are elements of ker(M mod modulus), i.e. the
  // HOMOGENEOUS system M*e === 0 (mod modulus) for BOTH blocks -- rhs is irrelevant here
  // (rhs only enters when extracting a particular solution f0, not the kernel itself).
  let genOk = true;
  gens.forEach((e, idx) => {
    for (let r = 0; r < rows.length; r++) {
      const val = e.reduce((s, x, k) => s + x * rows[r][k], 0);
      if (mod(val, modulus) !== 0) { genOk = false; }
    }
    const nE = e.map((x) => orders[idx] * x);
    if (!nE.every((x) => mod(x, modulus) === 0)) genOk = false;
  });
  console.log((genOk ? 'PASS  ' : 'FAIL  ') + `${fname}: linear_stage_kernel_c6 (fixture=${cert.fixture}, m=${m}, j=${j}, ${gens.length} generators) independently rechecked against agree6_sol2.json`);
  if (!genOk) certFails++;

  // mass-check bijectivity recheck (for fixture iii certs, and also informative for ii)
  const ns = orders;
  const totalCombos = ns.reduce((a, b) => a * b, 1);
  if (totalCombos <= 200000) {
    const seen = new Set();
    let allDistinct = true;
    const avec = new Array(gens.length).fill(0);
    let done = gens.length === 0;
    let count = 0;
    while (!done) {
      let f = new Array(n).fill(0); // f0 is not stored in the cert (only kernel gens); the
      // bijectivity check here is therefore on the KERNEL itself (avec -> sum a_i*e_i mod
      // modulus), i.e. verifying the kernel's own generating set has no redundancy -- a
      // slightly different (but equally informative) mass check than e2c6-sweep.g's own
      // (which mass-checked the full coset f0+K against the ORIGINAL system). Both are
      // legitimate cross-checks of the same underlying claim (|K|=Prod(n_i), no collisions).
      for (let i = 0; i < gens.length; i++) if (avec[i]) f = f.map((x, k) => x + avec[i] * gens[i][k]);
      f = f.map((x) => mod(x, modulus));
      const key = JSON.stringify(f);
      if (seen.has(key)) allDistinct = false; else seen.add(key);
      count++;
      let idx = 0;
      while (idx < gens.length) { avec[idx]++; if (avec[idx] < ns[idx]) break; avec[idx] = 0; idx++; }
      if (idx >= gens.length) done = true;
    }
    const ok = allDistinct && seen.size === totalCombos;
    console.log((ok ? 'PASS  ' : 'FAIL  ') + `  mass-check (kernel-only bijectivity): |K|=${totalCombos}  distinct=${seen.size}`);
    if (!ok) certFails++;
  }
}
console.log(`\ncertificate crosscheck: ${certFails === 0 ? 'ALL PASS' : certFails + ' FAILURES'}`);

console.log(`\n${fails === 0 ? 'ALL PASS' : fails + ' FAILURES'} (self-check fails=${fails}, cert fails=${certFails})`);
if (fails > 0 || certFails > 0) process.exit(1);
