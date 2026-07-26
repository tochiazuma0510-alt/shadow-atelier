// crosscheck/check-kummer-cov3.mjs
// 便 34 P6-C3 (Sol 便 34 blocker 4 / F4.5) 第三 covariance の独立照合器。
//
// manifest §較正三層 3: tau -> tau∘[d'] (mu_M の生成元の取り替え zeta_M ->
// zeta_M^{d'}) と Kummer character の逆冪 kappa -> d'^{-1}*kappa を同時に
// 施しても、(5') 相当の等式 sigma(e)/e = zeta_M^{kappa(sigma)} が(取り替え
// た生成元の下で)引き続き成り立つことを、search/kummer-decide.g
// (KummerCovariance3Check, GaloisCyc ベース)とは**別の実装**で確認する。
//
// 独立性: 本ファイルは GAP の GaloisCyc / AlgebraicExtension を一切使わない。
// witness の座標(basis 1,a,...,a^{deg-1} 表現)と体の次数だけを証明書から
// 読み、円分多項式 Phi_n(T) を独立に計算し(crosscheck/cyclo-ring-lib.mjs)、
// Galois 自己同型 sigma_d: a -> a^d の作用を「a を a^d の環演算べき乗に
// 置き換えて多項式を評価し直す」ことで純粋な Q[T]/(Phi_n) の環演算として
// 再構成する(GAP の GaloisCyc は import しない)。
//
// 入力: search/kummer-decide-k3-driver.g が書いた *-kummer-cov3.json。
// 使い方: node crosscheck/check-kummer-cov3.mjs <cov3 cert JSON>

import { readFileSync } from 'node:fs';
import { Q, polyMulMod, polyPowMod, polyAdd, polyMul, cyclotomicPolynomialAscending } from './cyclo-ring-lib.mjs';

function parseRatMaybeNumber(x) {
  if (typeof x === 'number') { if (!Number.isInteger(x)) throw new Error('non-integer'); return new Q(BigInt(x)); }
  const s = String(x).trim();
  if (s.includes('/')) { const [a, b] = s.split('/'); return new Q(BigInt(a), BigInt(b)); }
  return new Q(BigInt(s));
}

function gcd(a, b) { a = a < 0 ? -a : a; b = b < 0 ? -b : b; while (b) { [a, b] = [b, a % b]; } return a; }

// sigma_d(elt): elt = sum_i coeffs[i] * a^i と表されているとき、
// a -> a^d を代入して mod Phi_n(T) で reduce する。
// これは「aToD := a^d mod Phi_n」を先に計算し、elt(a) を Horner 法で
// aToD に代入することと同値(ring hom の定義そのまま)。
function applyGaloisSubstitution(coeffs, d, n, modPoly) {
  const aVec = [Q0(), new Q(1n)]; // a の係数表現 [0,1,0,...]
  const aToD = polyPowMod(aVec, d, modPoly);
  // Horner: elt = c0 + a*(c1 + a*(c2 + ...)) だが、ここでは a -> aToD なので
  // elt(aToD) = c0 + aToD*(c1 + aToD*(c2 + ...))
  let acc = [new Q(0n)];
  for (let i = coeffs.length - 1; i >= 0; i--) {
    acc = polyMulMod(acc, aToD, modPoly);
    acc = polyAddConst(acc, coeffs[i]);
  }
  return acc;
}
function Q0() { return new Q(0n); }
function polyAddConst(a, c) {
  const r = a.slice();
  r[0] = (r[0] ?? new Q(0n)).add(c);
  return r;
}

function polyEq(a, b) {
  const n = Math.max(a.length, b.length);
  for (let i = 0; i < n; i++) {
    const ai = a[i] ?? new Q(0n), bi = b[i] ?? new Q(0n);
    if (!ai.eq(bi)) return false;
  }
  return true;
}

//////////////////// 実行 ////////////////////
const certPath = process.argv[2];
if (!certPath) {
  console.error('usage: node check-kummer-cov3.mjs <kummer-cov3 cert JSON>');
  process.exit(2);
}
const cert = JSON.parse(readFileSync(certPath, 'utf8'));
const n = cert.field_n;
const M = cert.M;
const w = parseRatMaybeNumber(cert.w);
const ord = cert.ord;
const witnessCoeffs = cert.witness_coeffs_basis_powers_of_root.map((s) => parseRatMaybeNumber(s));

const modPoly = cyclotomicPolynomialAscending(n);

// witness の再検算: e^M = w^ord
const wPowOrd = (() => { let r = new Q(1n); for (let i = 0; i < ord; i++) r = r.mul(w); return r; })();
const eM = polyPowMod(witnessCoeffs, M, modPoly);
const eMok = eM.length === 1 && eM[0].eq(wPowOrd);
if (!eMok) {
  console.log(JSON.stringify({ schema: 'check-kummer-cov3/v1', certPath, result: 'MISMATCH',
    reason: `witness^M != w^ord independently: got ${eM.map(String)}, expected ${wPowOrd.toString()}` }, null, 2));
  process.exit(1);
}

// zeta_M の環内表現: zeta_M = a^{n/M} (n/M は整数、M|n を要求)
if (n % M !== 0) {
  console.log(JSON.stringify({ schema: 'check-kummer-cov3/v1', certPath, result: 'UNKNOWN',
    reason: `M=${M} does not divide n=${n} -- out of scope for this checker` }, null, 2));
  process.exit(0);
}
const aVec = [new Q(0n), new Q(1n)];
const zetaM = polyPowMod(aVec, n / M, modPoly);
function zetaMPow(k) { return polyPowMod(zetaM, ((k % M) + M) % M, modPoly); }

const galoisUnits = [];
for (let d = 1; d < n; d++) if (gcd(d, n) === 1) galoisUnits.push(d);

// kappa(d): sigma_d(e) = e * zeta_M^{kappa(d)} を満たす一意な kappa(d)
const eNative = witnessCoeffs;
const kappaTable = {};
for (const d of galoisUnits) {
  const sigE = applyGaloisSubstitution(eNative, d, n, modPoly);
  let found = null;
  for (let k = 0; k < M; k++) {
    const rhs = polyMulMod(eNative, zetaMPow(k), modPoly);
    if (polyEq(sigE, rhs)) { found = k; break; }
  }
  if (found === null) {
    console.log(JSON.stringify({ schema: 'check-kummer-cov3/v1', certPath, result: 'MISMATCH',
      reason: `sigma_${d}(e) is not e * zeta_M^k for any k (independent recompute failed)` }, null, 2));
    process.exit(1);
  }
  kappaTable[d] = found;
}

// GAP の kappa_table_wrt_zetaM と突合(独立算出値が一致するか)
const gapKappaTable = cert.kappa_table_wrt_zetaM;
const kappaMismatches = [];
for (const d of galoisUnits) {
  const gapVal = gapKappaTable[String(d)];
  if (gapVal === undefined || Number(gapVal) !== kappaTable[d]) {
    kappaMismatches.push({ d, independent: kappaTable[d], gap: gapVal });
  }
}
if (kappaMismatches.length > 0) {
  console.log(JSON.stringify({ schema: 'check-kummer-cov3/v1', certPath, result: 'MISMATCH',
    reason: 'kappa table mismatch between independent recompute and GAP certificate', kappaMismatches }, null, 2));
  process.exit(1);
}

// 第三 covariance 本体: tau -> tau∘[d'] (zeta_M -> zeta_M^{d'}) と
// kappa -> d'^{-1}*kappa の同時変換で不変であることを独立に検算する。
const unitsModM = [];
for (let x = 1; x < M; x++) if (gcd(x, M) === 1) unitsModM.push(x);

const reparamResults = [];
for (const dprime of unitsModM) {
  let dprimeInv = null;
  for (let x = 0; x < M; x++) if ((x * dprime) % M === 1) { dprimeInv = x; break; }
  const zetaMPrime = zetaMPow(dprime); // 新生成元 zeta_M^{d'}
  for (const d of galoisUnits) {
    const sigE = applyGaloisSubstitution(eNative, d, n, modPoly);
    let kNew = null;
    for (let k = 0; k < M; k++) {
      const zMPk = polyPowMod(zetaMPrime, k, modPoly);
      const rhs = polyMulMod(eNative, zMPk, modPoly);
      if (polyEq(sigE, rhs)) { kNew = k; break; }
    }
    const expectedKNew = (dprimeInv * kappaTable[d]) % M;
    reparamResults.push({ d, dprime, kNew, expectedKNew, match: kNew === expectedKNew });
  }
}
const allMatch = reparamResults.every((r) => r.match);

const report = {
  schema: 'check-kummer-cov3/v1',
  certPath,
  field_n: n,
  M,
  w: cert.w,
  ord,
  independent_kappa_table: kappaTable,
  gap_kappa_table: gapKappaTable,
  kappa_table_match: true,
  reparam_results: reparamResults,
  independent_all_match: allMatch,
  gap_all_match: cert.all_match,
  result: (allMatch === cert.all_match && allMatch === true) ? 'MATCH' : 'MISMATCH',
};
if (report.result !== 'MATCH') {
  report.reason = `independent_all_match=${allMatch} vs cert.all_match=${cert.all_match}`;
}
console.log(JSON.stringify(report, null, 2));
if (report.result !== 'MATCH') process.exit(1);
