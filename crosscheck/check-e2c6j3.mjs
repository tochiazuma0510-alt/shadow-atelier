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
    const ok = keysMatch && valuesMatch && totalMatch && sumMatch;
    const gotTableStr = JSON.stringify(Object.fromEntries(table));
    console.log((ok ? 'PASS  ' : 'FAIL  ') + `${fname}: m6j3_multiplicity_table (fixture=${cert.fixture}, m=${cert.m}, |L|=${total}) independently re-enumerated (brute force, exact nonlinear Q) table=${gotTableStr} (cert claimed ${JSON.stringify(cert.ob_table)})`);
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
    console.log(`SKIP  ${fname}: linear_stage_empty_c6j3 (negative real-sweep cert; only appears if fire lock is open -- no independent recheck implemented in this fixture-only pass)`);
    continue;
  }

  console.log(`SKIP  ${fname}: unrecognized claim "${cert.claim}"`);
}
console.log(`\ncertificate crosscheck: ${certFails === 0 ? 'ALL PASS' : certFails + ' FAILURES'}`);
console.log(`\n${fails === 0 ? 'ALL PASS' : fails + ' FAILURES'} (self-check fails=${fails}, cert fails=${certFails})`);
if (fails > 0 || certFails > 0) process.exit(1);
