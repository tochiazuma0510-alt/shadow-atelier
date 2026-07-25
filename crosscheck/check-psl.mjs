#!/usr/bin/env node
// crosscheck/check-psl.mjs -- independent 照合器 for PSL/PGL window S1 (workorder 4).
//
// P115 compliance: this file builds PGL(2,q) from EXPLICIT 2x2 matrices over GF(q) acting on the
// projective line P^1(GF(q)) directly -- it does NOT read any character table (CTblLib or
// otherwise). This is a genuinely independent second data source from the GAP explorer's own
// (also matrix-based, but separately coded) construction in search/week3-psl-common.g.
'use strict';
import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const CERT_DIR = join(ROOT, 'certificates');
const VERDICT_DIR = join(ROOT, 'crosscheck', 'verdicts');

function mod(a, n) { return ((a % n) + n) % n; }
function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; }

// ---------- GF(q) prime field arithmetic (own independent implementation) ----------
function gfInv(a, q) {
  a = mod(a, q);
  for (let b = 1; b < q; b++) if (mod(a * b, q) === 1) return b;
  throw new Error(`gfInv: no inverse for ${a} mod ${q}`);
}
function isSquareInGF(q, x) {
  x = mod(x, q);
  if (x === 0) return true;
  for (let e = 1; e < q; e++) if (mod(e * e, q) === x) return true;
  return false;
}

// ---------- 2x2 matrices over GF(q) ----------
function mat(q, a, b, c, d) { return [mod(a, q), mod(b, q), mod(c, q), mod(d, q)]; }
function detMat(q, M) { return mod(M[0] * M[3] - M[1] * M[2], q); }
function canonicalize(q, M) {
  let first = 0;
  for (const x of M) if (x !== 0) { first = x; break; }
  const inv = gfInv(first, q);
  return M.map((x) => mod(x * inv, q));
}
function matKey(M) { return M.join(','); }

// projective line P^1(GF(q)): q+1 points, index 0..q (0=infinity, 1+x = [x:1] for x in 0..q-1)
function matToPerm(q, M) {
  const [a, b, c, d] = M;
  const n = q + 1;
  const perm = new Array(n);
  // point 0: infinity [1:0] -> [a:c]
  perm[0] = c === 0 ? 0 : 1 + mod(a * gfInv(c, q), q);
  for (let x = 0; x < q; x++) {
    const num = mod(a * x + b, q), den = mod(c * x + d, q);
    perm[1 + x] = den === 0 ? 0 : 1 + mod(num * gfInv(den, q), q);
  }
  return perm;
}
function permMul(p, q_) { return p.map((_, i) => q_[p[i]]); } // apply p then q_ (matches GAP convention verified in earlier stages)
function permInv(p) { const r = new Array(p.length); p.forEach((v, i) => { r[v] = i; }); return r; }
function permId(n) { return Array.from({ length: n }, (_, i) => i); }
function permEq(a, b) { return a.length === b.length && a.every((x, i) => x === b[i]); }
function permPow(p, k) {
  const n = p.length;
  if (k === 0) return permId(n);
  let base = k < 0 ? permInv(p) : p, e = Math.abs(k), res = permId(n);
  while (e > 0) { if (e % 2 === 1) res = permMul(res, base); base = permMul(base, base); e = Math.floor(e / 2); }
  return res;
}
function permOrder(p) { let k = 1, cur = p.slice(); const id = permId(p.length); while (!permEq(cur, id)) { cur = permMul(cur, p); k++; } return k; }

function buildPGLElements(q) {
  const seen = new Map();
  const out = [];
  for (let a = 0; a < q; a++) for (let b = 0; b < q; b++) for (let c = 0; c < q; c++) for (let d = 0; d < q; d++) {
    const M = mat(q, a, b, c, d);
    if (detMat(q, M) === 0) continue;
    const canon = canonicalize(q, M);
    const key = matKey(canon);
    if (!seen.has(key)) { seen.set(key, true); out.push({ mat: canon, perm: matToPerm(q, canon) }); }
  }
  return out;
}

// subgroup closure via BFS (own generic implementation, permutation form)
function subgroupClosure(gens, n) {
  const genList = [...gens, ...gens.map(permInv)];
  const seen = new Map();
  const id = permId(n);
  seen.set(id.join(','), id);
  const frontier = [id];
  while (frontier.length) {
    const e = frontier.pop();
    for (const g of genList) {
      const cand = permMul(e, g);
      const k = cand.join(',');
      if (!seen.has(k)) { seen.set(k, cand); frontier.push(cand); }
    }
  }
  return seen;
}

function classCoefficient(elemList, target) {
  const t3 = elemList.filter((x) => permOrder(x) === 3);
  const t2 = elemList.filter((x) => permOrder(x) === 2);
  let count = 0;
  for (const r of t3) for (const g of t2) if (permEq(permMul(g, r), target)) count++; // paper rg -> GAP g*r
  return count;
}

function matFromStr(s) {
  // parses "[[a,b],[c,d]]" -> [a,b,c,d]
  const nums = s.match(/-?\d+/g).map(Number);
  return nums;
}

// ---------- GF(8) = F2[x]/(x^3+x+1), own bit-based arithmetic (independent JS reimplementation of
// search/week3-psl-common.g's GF8* functions -- same algorithm, separate code, per the P115/helper-
// non-sharing rule between search/ and crosscheck/) ----------
function bitOf(n, i) { return (n >> i) & 1; }
function xorInt(a, b) { return a ^ b; }
function gf8CarrylessMul(a, b) { let r = 0; for (let i = 0; i <= 2; i++) if (bitOf(b, i)) r ^= (a << i); return r; }
function gf8Reduce(p) { let r = p; for (const i of [4, 3]) if (bitOf(r, i)) r ^= (11 << (i - 3)); return r; }
function gf8Mul(a, b) { return gf8Reduce(gf8CarrylessMul(a, b)); }
function gf8Add(a, b) { return a ^ b; }
function gf8Inv(a) { for (let b = 1; b < 8; b++) if (gf8Mul(a, b) === 1) return b; throw new Error('gf8Inv: not found'); }
function matToPermGF8(M) {
  const [a, b, c, d] = M;
  const perm = new Array(9);
  perm[0] = c === 0 ? 0 : 1 + gf8Mul(a, gf8Inv(c));
  for (let x = 0; x < 8; x++) {
    const num = gf8Add(gf8Mul(a, x), b), den = gf8Add(gf8Mul(c, x), d);
    perm[1 + x] = den === 0 ? 0 : 1 + gf8Mul(num, gf8Inv(den));
  }
  return perm;
}
function gf8CanonicalizeMat(M) {
  let first = 0;
  for (const x of M) if (x !== 0) { first = x; break; }
  const inv = gf8Inv(first);
  return M.map((x) => gf8Mul(x, inv));
}
function gf8DetMat(M) { return gf8Add(gf8Mul(M[0], M[3]), gf8Mul(M[1], M[2])); } // sub = add in char 2
function buildPGLElementsGF8() {
  const seen = new Map(); const out = [];
  for (let a = 0; a < 8; a++) for (let b = 0; b < 8; b++) for (let c = 0; c < 8; c++) for (let d = 0; d < 8; d++) {
    const M = [a, b, c, d];
    if (gf8DetMat(M) === 0) continue;
    const canon = gf8CanonicalizeMat(M);
    const key = canon.join(',');
    if (!seen.has(key)) { seen.set(key, true); out.push({ mat: canon, perm: matToPermGF8(canon) }); }
  }
  return out;
}
function frobPermGF8() {
  const perm = [0];
  for (let x = 0; x < 8; x++) perm.push(1 + gf8Mul(x, x));
  return perm;
}

function parseQ(cert) {
  const mtch = /\(2,\s*(\d+)\)/.exec(cert.ambient_group);
  return mtch ? parseInt(mtch[1], 10) : null;
}

function checkPSLWindow(cert) {
  const q = parseQ(cert);
  if (q === 8) return checkPSLWindowGF8(cert);
  return checkPSLWindowPrime(cert, q);
}

function checkPSLWindowPrime(cert, q) {
  const errors = [];
  const Smat = matFromStr(cert.marking.S);
  const Tmat = matFromStr(cert.marking.T);
  const Sperm = matToPerm(q, Smat);
  const Tperm = matToPerm(q, Tmat);
  return checkPSLWindowCore(cert, q, q + 1, Sperm, Tperm, () => buildPGLElements(q),
    (M) => detMat(q, M), (x) => isSquareInGF(q, x), Smat);
}

function checkPSLWindowGF8(cert) {
  const Smat = matFromStr(cert.marking.S);
  const Tmat = matFromStr(cert.marking.T);
  const Sperm = matToPermGF8(Smat);
  const Tperm = matToPermGF8(Tmat);
  const buildAut = () => {
    const pgl = buildPGLElementsGF8();
    const frob = frobPermGF8();
    const gens = [...pgl.map((e) => e.perm), frob];
    const map = subgroupClosure(gens, 9);
    return [...map.values()].map((p) => ({ mat: p, perm: p }));
  };
  return checkPSLWindowCore(cert, 8, 9, Sperm, Tperm, buildAut, null, null, Smat);
}

// core logic shared by prime-field and GF(8) windows (own independent implementation throughout;
// P115: matrix-direct enumeration, no character tables read anywhere in this file)
function checkPSLWindowCore(cert, q, n, Sperm, Tperm, buildAutList, detFn, isSquareFn, Smat) {
  const errors = [];
  const ordS = permOrder(Sperm), ordT = permOrder(Tperm);
  if (ordS !== 2) errors.push('ord(S) != 2');
  if (ordT !== 3) errors.push('ord(T) != 3');
  let sIsInner = null;
  if (detFn && isSquareFn) {
    const detS = detFn(Smat);
    sIsInner = isSquareFn(detS);
    const expectInner = cert.case === 'A_split_inner';
    if (sIsInner !== expectInner) errors.push(`det(S) square=${sIsInner}, case=${cert.case} mismatch`);
  }
  const wPerm = permMul(Sperm, permInv(Tperm)); // paper T^-1 S -> GAP S*T^-1
  const eOrd = permOrder(wPerm);
  const Xperm = permMul(wPerm, wPerm);
  const kOrd = permOrder(Xperm);
  if (eOrd !== cert.marking.ord_w) errors.push(`ord(w) = ${eOrd} != claimed ${cert.marking.ord_w}`);
  if (kOrd !== cert.marking.ord_X) errors.push(`ord(X) = ${kOrd} != claimed ${cert.marking.ord_X}`);
  const Yperm = permMul(permMul(permInv(Sperm), Xperm), Sperm); // paper S X S^-1 -> GAP S^-1 X S
  const XYZid = (() => {
    const Zperm = permMul(permMul(permPow(Tperm, -2), Xperm), permPow(Tperm, 2));
    return permEq(permMul(permMul(Zperm, Yperm), Xperm), permId(n)); // paper XYZ=1 -> GAP Z*Y*X=1 (3-term reversal, D7)
  })();
  if (!XYZid) errors.push('XYZ != 1');

  const ghatMap = subgroupClosure([Sperm, Tperm], n);
  const gMap = subgroupClosure([Xperm, Yperm], n);
  if (ghatMap.size !== cert.generation_checks.gen_ambient) errors.push(`|<S,T>| = ${ghatMap.size} != claimed ${cert.generation_checks.gen_ambient}`);
  if (gMap.size !== cert.generation_checks.gen_derived) errors.push(`|<X,Y>| = ${gMap.size} != claimed ${cert.generation_checks.gen_derived}`);

  const b3Points = 6 * gMap.size;
  if (b3Points !== cert.universe.b3_points) errors.push(`b3_points = ${b3Points} != claimed ${cert.universe.b3_points}`);

  const nOrd = kOrd;
  const charmingSet = Array.from({ length: nOrd }, (_, m) => m).filter((m) => gcd(2 * m + 1, nOrd) === 1);
  if (JSON.stringify(charmingSet) !== JSON.stringify(cert.universe.charming_set)) errors.push('charming_set mismatch');

  const candidateTotal = charmingSet.length * gMap.size;
  if (candidateTotal !== cert.universe.candidate_total) errors.push(`candidate_total = ${candidateTotal} != claimed ${cert.universe.candidate_total}`);

  const pglElts = buildAutList();

  // hexagon_free_certificate cross-check (reduced hexagon via theta/tau homomorphism shortcut,
  // matching GAP's EnumerateReducedHexagon logic -- own independent word/BFS implementation)
  function bfsWords(X, Y, n) {
    const invX = permInv(X), invY = permInv(Y);
    const gens = [['x', 1, X], ['x', -1, invX], ['y', 1, Y], ['y', -1, invY]];
    const wordOf = new Map();
    const id = permId(n);
    wordOf.set(id.join(','), []);
    const queue = [id];
    let qi = 0;
    while (qi < queue.length) {
      const cur = queue[qi++];
      const curWord = wordOf.get(cur.join(','));
      for (const [sym, p, gelt] of gens) {
        const nv = permMul(gelt, cur); // prepend, matches GAP's BFSWords
        const k = nv.join(',');
        if (!wordOf.has(k)) { wordOf.set(k, curWord.concat([[sym, p]])); queue.push(nv); }
      }
    }
    return { wordOf, elements: queue };
  }
  function evalWordPrepend(word, X, Y, n) {
    let val = permId(n);
    for (const [sym, p] of word) { const g = sym === 'x' ? X : Y; val = permMul(permPow(g, p), val); }
    return val;
  }
  function thetaWord(w) { return w.map(([s, p]) => (s === 'x' ? ['y', p] : ['x', p])); }
  function tauWord(w) { return w.flatMap(([s, p]) => (s === 'x' ? [['y', p]] : (p === 1 ? [['y', -1], ['x', -1]] : [['x', 1], ['y', 1]]))); }

  const { wordOf, elements } = bfsWords(Xperm, Yperm, n);
  // derived subgroup = G (perfect), so ALL 168 elements are candidates
  let h10Fail = 0, h11Fail = 0, genFail = 0, shadowTotal = 0;
  const shadows = [];
  for (const elt of elements) {
    const word = wordOf.get(elt.join(','));
    for (const m of charmingSet) {
      const u = 2 * m + 1;
      const th = thetaWord(word);
      const hex310 = permEq(evalWordPrepend(word.concat(th), Xperm, Yperm, n), permId(n));
      if (!hex310) { h10Fail++; continue; }
      const yWordM = Array.from({ length: m }, () => ['y', 1]);
      const ymfWord = yWordM.concat(word);
      const tau1 = tauWord(ymfWord);
      const tau2 = tauWord(tau1);
      const hex311 = permEq(evalWordPrepend(tau2.concat(tau1, ymfWord), Xperm, Yperm, n), permId(n));
      if (!hex311) { h11Fail++; continue; }
      const u_ = u;
      const genA = permPow(Xperm, u_);
      const genB = permMul(permMul(elt, permPow(Yperm, u_)), permInv(elt)); // reversed, matches AbstractProd genB
      const gen = subgroupClosure([genA, genB], n);
      if (gen.size === gMap.size) { shadowTotal++; shadows.push({ m, f: elt, word }); } else genFail++;
    }
  }
  const candTot = charmingSet.length * elements.length;
  const claimedHex = cert.hexagon_free_certificate;
  const hexOk = claimedHex.candidate_total === candTot && claimedHex.h10_fail === h10Fail && claimedHex.h11_fail === h11Fail && claimedHex.generation_fail === genFail && claimedHex.shadow_total === shadowTotal;
  if (!hexOk) errors.push(`hexagon_free_certificate mismatch: observed cand=${candTot} h10=${h10Fail} h11=${h11Fail} genfail=${genFail} shadow=${shadowTotal}, claimed=${JSON.stringify(claimedHex)}`);

  // settled witness re-verification (independent search over the SAME PGL(2,7) list)
  function witnessToPerm(str) {
    if (q === 8) return parseGapPermString(str, n); // PGammaL witnesses are printed as GAP perms
    return matToPerm(q, matFromStr(str));
  }
  let witnessMismatches = 0;
  for (const sd of (cert.settled_detail || [])) {
    const f = evalWordPrepend(sd.f_word, Xperm, Yperm, n);
    const m = sd.m, u = 2 * m + 1;
    const targetX = permPow(Xperm, u);
    const targetY = permMul(permMul(f, permPow(Yperm, u)), permInv(f));
    if (sd.settled) {
      const h = witnessToPerm(sd.automorphism_witness);
      const ok = permEq(permMul(permMul(permInv(h), Xperm), h), targetX) && permEq(permMul(permMul(permInv(h), Yperm), h), targetY);
      if (!ok) witnessMismatches++;
    } else {
      let found = false;
      for (const e of pglElts) {
        const h = e.perm;
        if (permEq(permMul(permMul(permInv(h), Xperm), h), targetX) && permEq(permMul(permMul(permInv(h), Yperm), h), targetY)) { found = true; break; }
      }
      if (found) witnessMismatches++;
    }
  }
  if (witnessMismatches > 0) errors.push(`${witnessMismatches} settled-witness mismatches`);
  const settledCountObserved = (cert.settled_detail || []).filter((sd) => sd.settled).length;
  if (cert.settled_count !== settledCountObserved) errors.push('settled_count mismatch');

  const ok = errors.length === 0;
  return { ok, errors, observed: { ord_S: ordS, ord_T: ordT, ord_w: eOrd, ord_X: kOrd, s_is_inner: sIsInner, ghat_size: ghatMap.size, g_size: gMap.size, b3_points: b3Points, candidate_total: candidateTotal, aut_size: pglElts.length, hexagon_free_certificate_observed: { candidate_total: candTot, h10_fail: h10Fail, h11_fail: h11Fail, generation_fail: genFail, shadow_total: shadowTotal }, settled_count_observed: settledCountObserved } };
}

// parses a 1-indexed GAP permutation print string (e.g. "(1,4)(2,7,3)" or "()") into a 0-indexed
// permutation array of length n (own independent parser, mirrors the one used for A1 in check-v2.mjs
// but generalized to n points).
function parseGapPermString(s, n) {
  const perm = Array.from({ length: n }, (_, i) => i);
  if (s === '()') return perm;
  const re = /\(([^)]+)\)/g;
  let match;
  while ((match = re.exec(s))) {
    const cyc = match[1].split(',').map((x) => parseInt(x.trim(), 10) - 1);
    for (let i = 0; i < cyc.length; i++) perm[cyc[i]] = cyc[(i + 1) % cyc.length];
  }
  return perm;
}

function checkPU_F12() {
  // PU-F12 (W78 control, PSL(2,11)) -- checked once here (not per-window; excluded window, not
  // part of any S1-S7 certificate's own claims, so verified against the S1 cert's recorded value).
  const q11 = 11;
  const pgl11 = buildPGLElements(q11);
  const psl11 = pgl11.filter((e) => isSquareInGF(q11, detMat(q11, e.mat))).map((e) => e.perm);
  if (psl11.length !== 660) return { ok: false, reason: `PSL(2,11) size = ${psl11.length} != 660` };
  const v5 = psl11.find((x) => permOrder(x) === 5);
  const cc = classCoefficient(psl11, v5);
  return { ok: cc === 10, class_coefficient_observed: cc };
}

function main() {
  if (!existsSync(VERDICT_DIR)) mkdirSync(VERDICT_DIR, { recursive: true });
  const ids = process.argv.slice(2).length ? process.argv.slice(2) : ['S1'];
  const results = {};
  for (const id of ids) {
    const certPath = join(CERT_DIR, `${id}.v2.json`);
    if (!existsSync(certPath)) { console.log(`certificate not found: ${certPath}`); results[id] = { ok: false }; continue; }
    const cert = JSON.parse(readFileSync(certPath, 'utf8'));
    let verdict = checkPSLWindow(cert);
    if (id === 'S1') {
      const puf12 = checkPU_F12();
      verdict = { ...verdict, ok: verdict.ok && puf12.ok, pu_f12_control_recheck: puf12 };
    }
    results[id] = verdict;
    writeFileSync(join(VERDICT_DIR, `${id}.psl.verdict.json`), JSON.stringify(verdict, null, 2));
    console.log(`window ${id}: ${verdict.ok ? 'PASS' : 'FAIL'}`);
    console.log(JSON.stringify(verdict, null, 2));
  }
  const allOk = Object.values(results).every((r) => r.ok);
  console.log(`\ncheck-psl.mjs overall: ${allOk ? 'all_pass' : 'FAIL'}`);
}

main();
