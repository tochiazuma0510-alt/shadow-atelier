#!/usr/bin/env node
// crosscheck/check-v2.mjs -- independent 照合器 for gtsh-cert/v2 certificates (Week3 較正
// バッテリー workorder 1, stages 1a/1b/2a/2b). Reads ONLY the certificate JSON files under
// certificates/ -- no import of search/*.g, no import of check.mjs (kept separate on purpose:
// gtsh-cert/v2 is a different schema from gtsh-cert/v1, and the objects here (Q8, the K^(3)/N_Q
// fiber product, the p=2 verbal-restricted towers P2/P3) are independently re-derived below from
// their own group-theoretic definitions, not from the GAP explorer's code or intermediate state).
//
// Design source (spec projection only): search/manifest_spec_v1.md, docs/wp2-transversal-model.md,
// docs/week1-定義ノート.md.
'use strict';

import { readFileSync, readdirSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const CERT_DIR = join(ROOT, 'certificates');
const VERDICT_DIR = join(ROOT, 'crosscheck', 'verdicts');

function mod(a, n) { return ((a % n) + n) % n; }
function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; }
function lcm(a, b) { return Math.abs(a * b) / gcd(a, b); }

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value !== null && typeof value === 'object') {
    const out = {};
    for (const k of Object.keys(value).sort()) out[k] = canonicalize(value[k]);
    return out;
  }
  return value;
}
function canonicalJson(value) { return JSON.stringify(canonicalize(value)); }
function sha256hex(s) { return createHash('sha256').update(s, 'utf8').digest('hex'); }

// ---------- Q8 (own independent construction, quaternion algebra directly) ----------
// element = {s: +-1, u: 0..3} (0=1,1=i,2=j,3=k). Multiplication table derived directly from
// i^2=j^2=k^2=-1, ij=k, ji=-k, jk=i, kj=-i, ki=j, ik=-j (standard quaternion relations).
const Q8_UNIT_TABLE = [
  [[1, 0], [1, 1], [1, 2], [1, 3]],
  [[1, 1], [-1, 0], [1, 3], [-1, 2]],
  [[1, 2], [-1, 3], [-1, 0], [1, 1]],
  [[1, 3], [1, 2], [-1, 1], [-1, 0]],
];
function makeQ8() {
  const id = { s: 1, u: 0 };
  const mul = (g, h) => {
    const [tsign, tu] = Q8_UNIT_TABLE[g.u][h.u];
    return { s: g.s * h.s * tsign, u: tu };
  };
  const inv = (g) => {
    // for quaternion units, g^-1 = conjugate-ish: 1^-1=1, (-1)^-1=-1, i^-1=-i, j^-1=-j, k^-1=-k
    if (g.u === 0) return { s: g.s, u: 0 };
    return { s: -g.s, u: g.u };
  };
  const key = (g) => `${g.s},${g.u}`;
  const eq = (g, h) => key(g) === key(h);
  const elements = () => {
    const out = [];
    for (let u = 0; u < 4; u++) for (const s of [1, -1]) out.push({ s, u });
    return out;
  };
  const pow = (g, k) => {
    if (k === 0) return id;
    let base = k < 0 ? inv(g) : g, exponent = Math.abs(k), res = id;
    while (exponent > 0) { if (exponent % 2 === 1) res = mul(res, base); base = mul(base, base); exponent = Math.floor(exponent / 2); }
    return res;
  };
  const label = (g) => {
    const names = ['1', 'i', 'j', 'k'];
    if (g.u === 0) return g.s === 1 ? '1' : '-1';
    return (g.s === 1 ? '' : '-') + names[g.u];
  };
  return { id, mul, inv, key, eq, elements, pow, label };
}

// ---------- word evaluation ----------
function evalWord(G, phi, tokens) {
  let res = G.id;
  for (const [gen, p] of tokens) res = G.mul(res, G.pow(phi[gen], p));
  return res;
}

// ---------- subgroup closure (BFS) ----------
function subgroupClosure(G, gens) {
  const genList = [];
  for (const g of gens) { genList.push(g); genList.push(G.inv(g)); }
  const seen = new Map();
  seen.set(G.key(G.id), G.id);
  const frontier = [G.id];
  while (frontier.length) {
    const elem = frontier.pop();
    for (const g of genList) {
      const cand = G.mul(elem, g);
      const k = G.key(cand);
      if (!seen.has(k)) { seen.set(k, cand); frontier.push(cand); }
    }
  }
  return seen;
}
function commutator(G, g, h) { return G.mul(G.mul(G.inv(g), G.inv(h)), G.mul(g, h)); }
function derivedSubgroup(G, genMap, X, Y) {
  const c0 = commutator(G, X, Y);
  const conjugates = [];
  for (const g of genMap.values()) conjugates.push(G.mul(G.mul(g, c0), G.inv(g)));
  return subgroupClosure(G, conjugates);
}

// word BFS: assign a shortest x/y-word to every element reachable from id via x,y,x^-1,y^-1.
// NATURAL convention (see evalWordLeftAccum comment above): word list [w1,...,wk] represents the
// F2 element w1*w2*...*wk read left to right, so extending a word by appending a new letter at the
// END must correspond to RIGHT-multiplying the current element by that letter (cur*g), not
// left-multiplying (that would be the GAP-script-specific reversed convention we deliberately do
// not reuse here).
function bfsWords(G, X, Y) {
  const invX = G.inv(X), invY = G.inv(Y);
  const gens = [['x', 1, X], ['x', -1, invX], ['y', 1, Y], ['y', -1, invY]];
  const wordOf = new Map();
  wordOf.set(G.key(G.id), []);
  const queue = [G.id];
  let qi = 0;
  while (qi < queue.length) {
    const cur = queue[qi++];
    const curWord = wordOf.get(G.key(cur));
    for (const [sym, pow, gelt] of gens) {
      const nv = G.mul(cur, gelt); // right-multiply: append g naturally extends the word
      const k = G.key(nv);
      if (!wordOf.has(k)) { wordOf.set(k, curWord.concat([[sym, pow]])); queue.push(nv); }
    }
  }
  return { wordOf, elements: queue };
}

// Natural left-to-right homomorphism evaluation: a word list [w1,w2,...,wk] represents the F2
// element w1*w2*...*wk (standard free-group concatenation, read left to right), and phi is a
// genuine group homomorphism, so phi(w1...wk) = phi(w1)*phi(w2)*...*phi(wk) using Q's OWN
// multiplication in matching order -- no reversal. (IMPORTANT, found during independent
// verification: this is deliberately NOT copied from search/week3-{L,M5}-explorer.g's
// EvalWordInQ, which accumulates via "val := g^pow * val" (prepend). That prepend convention is
// only correct there because it is the exact inverse of how those scripts' own BFSWords stores
// words (BFSWords appends the new letter while GAP-multiplying by *prepending* the generator on
// the left) -- a GAP-internal representation artifact of building group elements via LEFT REGULAR
// PERMUTATION representations under GAP's right-action permutation-composition convention. That
// artifact is not part of the mathematical definition (theta/tau are automorphisms of the abstract
// free group F2, and (xy)^-1 = y^-1 x^-1 by ordinary algebra) and reusing it here would silently
// import a GAP-script convention into the independent checker, defeating the point of
// crosscheck/ (CLAUDE.md rule 2: "同じ helper を共有したら独立の照合にならない"). Verified by hand
// for f=1,m=1 in Q8: natural evaluation gives (3.11) product = -1 (FAIL), matching the certificate's
// own claimed h11_fail for that candidate; the prepend convention gave the opposite (wrongly PASS)
// when tried first -- see report to commander.
function evalWordLeftAccum(G, X, Y, word) {
  let val = G.id;
  for (const [sym, p] of word) {
    const g = sym === 'x' ? X : Y;
    val = G.mul(val, G.pow(g, p));
  }
  return val;
}

// ---------- reduced-hexagon enumeration (quotient shortcut; valid since c_in_N=true for 1a/1b/2a/2b) ----------
function enumerateReducedHexagon(G, X, Y, charmingSet) {
  const genMap = subgroupClosure(G, [X, Y]);
  const D = derivedSubgroup(G, genMap, X, Y);
  const zElt = G.inv(G.mul(X, Y)); // z = (xy)^-1
  const theta = (w) => w.map(([sym, p]) => (sym === 'x' ? ['y', p] : ['x', p]));
  const tau = (w) => w.flatMap(([sym, p]) => {
    if (sym === 'x') return [[p === 1 ? 'y' : 'y', p === 1 ? 1 : -1]];
    // y -> z = (xy)^-1 = y^-1 x^-1 ; y^-1 -> z^-1 = x y
    return p === 1 ? [['y', -1], ['x', -1]] : [['x', 1], ['y', 1]];
  });
  const { wordOf, elements } = bfsWords(G, X, Y);
  const dWords = [];
  for (const elt of elements) {
    if (D.has(G.key(elt))) dWords.push({ elt, word: wordOf.get(G.key(elt)) });
  }
  let h10Fail = 0, h11Fail = 0, genFail = 0;
  const shadows = [];
  const genDetail = [];
  for (const cand of dWords) {
    const f = cand.elt;
    for (const m of charmingSet) {
      const u = 2 * m + 1;
      const thetaF = evalWordLeftAccum(G, X, Y, theta(cand.word));
      const hex310 = G.eq(G.mul(f, thetaF), G.id);
      if (!hex310) { h10Fail++; genDetail.push({ m, f_word: cand.word, pass: false, stage: 'h10_fail' }); continue; }
      const yWordM = Array.from({ length: m }, () => ['y', 1]);
      const ymfWord = yWordM.concat(cand.word);
      const ymf = evalWordLeftAccum(G, X, Y, ymfWord);
      const tauWord1 = tau(ymfWord);
      const tauymf = evalWordLeftAccum(G, X, Y, tauWord1);
      const tauWord2 = tau(tauWord1);
      const tau2ymf = evalWordLeftAccum(G, X, Y, tauWord2);
      const hex311 = G.eq(G.mul(G.mul(tau2ymf, tauymf), ymf), G.id);
      if (!hex311) { h11Fail++; genDetail.push({ m, f_word: cand.word, pass: false, stage: 'h11_fail' }); continue; }
      const genA = G.pow(X, u);
      const invF = G.inv(f);
      const genB = G.mul(G.mul(invF, G.pow(Y, u)), f);
      const gen = subgroupClosure(G, [genA, genB]);
      const surj = gen.size === genMap.size;
      if (!surj) { genFail++; genDetail.push({ m, f_word: cand.word, pass: false, stage: 'generation_fail' }); }
      else { shadows.push({ m, f, word: cand.word }); genDetail.push({ m, f_word: cand.word, pass: true, stage: 'pass' }); }
    }
  }
  return {
    candidate_total: dWords.length * charmingSet.length,
    h10_fail: h10Fail, h11_fail: h11Fail, generation_fail: genFail,
    shadow_total: shadows.length, shadows, generation_detail: genDetail,
    G_size: genMap.size, derived_size: D.size,
  };
}

// ---------- per-certificate checks ----------
function wordKey(word) { return JSON.stringify(word); }

function checkTargetHash(cert) {
  if (!cert.target_definition) return { ok: false, reason: 'no target_definition' };
  const canon = canonicalJson(cert.target_definition);
  const expected = sha256hex(canon);
  return { ok: cert.target_hash === expected, expected, claimed: cert.target_hash, canonical: canon };
}

function checkHexagonFreeCertificate(cert, observed) {
  const c = cert.hexagon_free_certificate || {};
  const sumOk = (c.candidate_total - c.h10_fail - c.h11_fail - c.generation_fail) === c.shadow_total;
  const checks = {
    candidate_total: c.candidate_total === observed.candidate_total,
    h10_fail: c.h10_fail === observed.h10_fail,
    h11_fail: c.h11_fail === observed.h11_fail,
    generation_fail: c.generation_fail === observed.generation_fail,
    shadow_total: c.shadow_total === observed.shadow_total,
    sum_identity: sumOk,
  };
  return { ok: Object.values(checks).every(Boolean), checks, claimed: c, observed: {
    candidate_total: observed.candidate_total, h10_fail: observed.h10_fail, h11_fail: observed.h11_fail,
    generation_fail: observed.generation_fail, shadow_total: observed.shadow_total } };
}

// Recompute each claimed candidate DIRECTLY from its f_word (independent evaluation), rather than
// matching against our own BFS's word choice -- different BFS traversal orders can assign a
// different (but equally valid, same-element) shortest word to the same group element, so matching
// by literal word string is not a legitimate independence check. Evaluating the claimed word in our
// own group model and re-deriving pass/fail from scratch is the correct cross-check.
function checkGenerationDetailByEval(cert, G, X, Y, D) {
  const zElt = G.inv(G.mul(X, Y));
  const theta = (w) => w.map(([sym, p]) => (sym === 'x' ? ['y', p] : ['x', p]));
  const tau = (w) => w.flatMap(([sym, p]) => {
    if (sym === 'x') return [['y', p]];
    return p === 1 ? [['y', -1], ['x', -1]] : [['x', 1], ['y', 1]];
  });
  const genMap = subgroupClosure(G, [X, Y]);
  const claimed = cert.generation_detail || [];
  let mismatches = 0, notInDerived = 0;
  const details = [];
  for (const gd of claimed) {
    const f = evalWordLeftAccum(G, X, Y, gd.f_word);
    if (!D.has(G.key(f))) { notInDerived++; continue; }
    const m = gd.m, u = 2 * m + 1;
    const thetaF = evalWordLeftAccum(G, X, Y, theta(gd.f_word));
    const hex310 = G.eq(G.mul(f, thetaF), G.id);
    let pass = false, stage = 'h10_fail';
    if (hex310) {
      const yWordM = Array.from({ length: m }, () => ['y', 1]);
      const ymfWord = yWordM.concat(gd.f_word);
      const ymf = evalWordLeftAccum(G, X, Y, ymfWord);
      const tauWord1 = tau(ymfWord);
      const tauymf = evalWordLeftAccum(G, X, Y, tauWord1);
      const tauWord2 = tau(tauWord1);
      const tau2ymf = evalWordLeftAccum(G, X, Y, tauWord2);
      const hex311 = G.eq(G.mul(G.mul(tau2ymf, tauymf), ymf), G.id);
      if (hex311) {
        const genA = G.pow(X, u);
        const invF = G.inv(f);
        const genB = G.mul(G.mul(invF, G.pow(Y, u)), f);
        const gen = subgroupClosure(G, [genA, genB]);
        if (gen.size === genMap.size) { pass = true; stage = 'pass'; } else stage = 'generation_fail';
      } else stage = 'h11_fail';
    }
    if (pass !== gd.pass || stage !== gd.stage) mismatches++;
    details.push({ m, claimed_pass: gd.pass, recomputed_pass: pass, claimed_stage: gd.stage, recomputed_stage: stage });
  }
  const passCountClaimed = cert.generation_pass_count;
  const passCountRecomputed = details.filter((d) => d.recomputed_pass).length;
  return {
    ok: mismatches === 0 && notInDerived === 0 && claimed.length > 0 && passCountClaimed === passCountRecomputed,
    mismatches, not_in_derived_subgroup: notInDerived, count: claimed.length,
    generation_pass_count_claimed: passCountClaimed, generation_pass_count_recomputed: passCountRecomputed,
    details,
  };
}

function checkUniverse1a(cert) {
  const u = cert.universe || {};
  const Q = makeQ8();
  const X = { s: 1, u: 1 }; // i
  const Y = { s: 1, u: 2 }; // j
  const genMap = subgroupClosure(Q, [X, Y]);
  const D = derivedSubgroup(Q, genMap, X, Y);
  const nOrd = lcm(4, lcm(4, 1)); // ord(i)=4, ord(j)=4, ord(c)=ord(1)=1
  const expectedCharming = [0, 1, 2, 3].filter((m) => gcd(2 * m + 1, nOrd) === 1);
  const checks = {
    pb3_index: u.pb3_index === genMap.size && genMap.size === 8,
    b3_points: u.b3_points === 6 * genMap.size,
    n_ord: u.n_ord === nOrd,
    derived_order: u.derived_order === D.size,
    charming_set: JSON.stringify((u.charming_set || []).slice().sort()) === JSON.stringify(expectedCharming.slice().sort()),
    candidate_total: u.candidate_total === expectedCharming.length * D.size,
  };
  return { ok: Object.values(checks).every(Boolean), checks, observed: { pb3_index: genMap.size, b3_points: 6 * genMap.size, n_ord: nOrd, derived_order: D.size, charming_set: expectedCharming, candidate_total: expectedCharming.length * D.size } };
}

function checkStage1a(cert) {
  const hashRes = checkTargetHash(cert);
  const uniRes = checkUniverse1a(cert);
  const Q = makeQ8();
  const X = { s: 1, u: 1 }, Y = { s: 1, u: 2 };
  const charmingSet = (cert.universe && cert.universe.charming_set) || [0, 1, 2, 3];
  const observed = enumerateReducedHexagon(Q, X, Y, charmingSet);
  const hexRes = checkHexagonFreeCertificate(cert, observed);
  const genMap = subgroupClosure(Q, [X, Y]);
  const D = derivedSubgroup(Q, genMap, X, Y);
  const genRes = checkGenerationDetailByEval(cert, Q, X, Y, D);
  const kernelClaim = cert.kernel_certificate || {};
  const kernelOk = kernelClaim.kernel_scope === 'PB3' && kernelClaim.pb3_kernel_index === 8 && kernelClaim.b3_kernel_index === 48;
  const cInNOk = cert.c_in_N === true;
  const evalModeOk = cert.evaluation_mode === 'quotient_ok';
  const shadowSumOk = observed.candidate_total - observed.h10_fail - observed.h11_fail - observed.generation_fail === observed.shadow_total;
  const ok = hashRes.ok && uniRes.ok && hexRes.ok && genRes.ok && kernelOk && cInNOk && evalModeOk && shadowSumOk;
  return { ok, target_hash: hashRes, universe: uniRes, hexagon_free_certificate: hexRes, generation_detail: genRes, kernel_certificate: { ok: kernelOk, claimed: kernelClaim }, c_in_N: cInNOk, evaluation_mode: evalModeOk, shadow_sum_identity: shadowSumOk, observed_shadow_total: observed.shadow_total };
}

// ---------- P2 = F2/F2^4 gamma_3(F2), order 32 (Heisenberg-style cocycle group, own independent
// derivation from manifest_spec_v1.md fixture U-F4's explicit relations -- X^4=Y^4=(XY)^4=1,
// [X,Y] central order 2, class 2, |P2|=32 -- hand-verified against all four relations before use,
// same method as the GAP explorer used (independently re-derived here, not copied). ----------
function makeHeis(nMod, cMod) {
  const id = { a: 0, b: 0, e: 0 };
  const mul = (g, h) => ({ a: mod(g.a + h.a, nMod), b: mod(g.b + h.b, nMod), e: mod(g.e + h.e + g.a * h.b, cMod) });
  const inv = (g) => ({ a: mod(-g.a, nMod), b: mod(-g.b, nMod), e: mod(-g.e + g.a * g.b, cMod) });
  const key = (g) => `${mod(g.a, nMod)},${mod(g.b, nMod)},${mod(g.e, cMod)}`;
  const eq = (g, h) => key(g) === key(h);
  const elements = () => { const out = []; for (let a = 0; a < nMod; a++) for (let b = 0; b < nMod; b++) for (let e = 0; e < cMod; e++) out.push({ a, b, e }); return out; };
  const pow = (g, k) => {
    if (k === 0) return id;
    let base = k < 0 ? inv(g) : g, exponent = Math.abs(k), res = id;
    while (exponent > 0) { if (exponent % 2 === 1) res = mul(res, base); base = mul(base, base); exponent = Math.floor(exponent / 2); }
    return res;
  };
  return { id, mul, inv, key, eq, elements, pow };
}

function checkUniverseSimple(cert, G, X, Y, nOrdExpected, expectedOrder) {
  const u = cert.universe || {};
  const genMap = subgroupClosure(G, [X, Y]);
  const D = derivedSubgroup(G, genMap, X, Y);
  const expectedCharming = Array.from({ length: nOrdExpected }, (_, m) => m).filter((m) => gcd(2 * m + 1, nOrdExpected) === 1);
  const checks = {
    pb3_index: u.pb3_index === genMap.size && genMap.size === expectedOrder,
    b3_points: u.b3_points === 6 * genMap.size,
    n_ord: u.n_ord === nOrdExpected,
    derived_order: u.derived_order === D.size,
    charming_set: JSON.stringify((u.charming_set || []).slice().sort((a, b) => a - b)) === JSON.stringify(expectedCharming),
    candidate_total: u.candidate_total === expectedCharming.length * D.size,
  };
  return { ok: Object.values(checks).every(Boolean), checks, genMap, D, observed: { pb3_index: genMap.size, b3_points: 6 * genMap.size, n_ord: nOrdExpected, derived_order: D.size, charming_set: expectedCharming, candidate_total: expectedCharming.length * D.size } };
}

function selfCheckP3(P3, X, Y) {
  const log = [];
  let ok = true;
  const genMap = subgroupClosure(P3, [X, Y]);
  const sizeOk = genMap.size === 128;
  log.push(`|<X,Y>| = ${genMap.size} (expect 128): ${sizeOk}`); if (!sizeOk) ok = false;
  const x4 = P3.eq(P3.pow(X, 4), P3.id), y4 = P3.eq(P3.pow(Y, 4), P3.id);
  log.push(`X^4=1: ${x4}, Y^4=1: ${y4}`); if (!x4 || !y4) ok = false;
  // exponent 4: every element to the 4th power is identity
  let expOk = true;
  for (const e of genMap.values()) if (!P3.eq(P3.pow(e, 4), P3.id)) expOk = false;
  log.push(`exponent 4 (all 128 elements): ${expOk}`); if (!expOk) ok = false;
  const w = commutator(P3, X, Y);
  const p = commutator(P3, w, X), q = commutator(P3, w, Y);
  const wOk = !P3.eq(w, P3.id) && P3.eq(P3.pow(w, 2), P3.id);
  const pOk = !P3.eq(p, P3.id) && P3.eq(P3.pow(p, 2), P3.id);
  const qOk = !P3.eq(q, P3.id) && P3.eq(P3.pow(q, 2), P3.id);
  log.push(`ord(w)=2: ${wOk}, ord(p)=2: ${pOk}, ord(q)=2: ${qOk}`); if (!wOk || !pOk || !qOk) ok = false;
  const g3 = subgroupClosure(P3, [p, q]);
  const g3Ok = g3.size === 4;
  log.push(`|<p,q>| = ${g3.size} (expect 4): ${g3Ok}`); if (!g3Ok) ok = false;
  const central = [X, Y, w].every((g) => P3.eq(P3.mul(p, g), P3.mul(g, p)) && P3.eq(P3.mul(q, g), P3.mul(g, q)));
  log.push(`p,q central: ${central}`); if (!central) ok = false;
  return { ok, log };
}

function checkStage2b(cert) {
  const hashRes = checkTargetHash(cert);
  const P3 = makeP3Group();
  const X = { a: 1, b: 0, e: 0, f: 0, q: 0 }, Y = { a: 0, b: 1, e: 0, f: 0, q: 0 };
  const selfCheck = selfCheckP3(P3, X, Y);
  const uniRes = checkUniverseSimple(cert, P3, X, Y, 4, 128);
  const charmingSet = (cert.universe && cert.universe.charming_set) || [0, 1, 2, 3];
  const observed = enumerateReducedHexagon(P3, X, Y, charmingSet);
  const hexRes = checkHexagonFreeCertificate(cert, observed);
  const genRes = checkGenerationDetailByEval(cert, P3, X, Y, uniRes.D);
  const kernelClaim = cert.kernel_certificate || {};
  const kernelOk = kernelClaim.kernel_scope === 'PB3' && kernelClaim.pb3_kernel_index === 128 && kernelClaim.b3_kernel_index === 768;
  const cInNOk = cert.c_in_N === true;
  const evalModeOk = cert.evaluation_mode === 'quotient_ok';
  const shadowSumOk = observed.candidate_total - observed.h10_fail - observed.h11_fail - observed.generation_fail === observed.shadow_total;
  // R4: N3 -> N2, marked factor map X->X, Y->Y: evaluate f_word directly in P2
  const P2 = makeHeis(4, 2);
  const Xp2 = { a: 1, b: 0, e: 0 }, Yp2 = { a: 0, b: 1, e: 0 };
  const n2Observed = enumerateReducedHexagon(P2, Xp2, Yp2, [0, 1, 2, 3]);
  const claimedR4 = (cert.reductions || []).find((r) => r.target === 'N2');
  let r4Res = { ok: false, reason: 'no R4 in cert.reductions' };
  if (claimedR4) {
    const seen = new Set();
    for (const sh of observed.shadows) {
      const fp2 = evalWordLeftAccum(P2, Xp2, Yp2, sh.word);
      const newm = mod(sh.m, 4);
      const idx = n2Observed.shadows.findIndex((s) => s.m === newm && P2.eq(s.f, fp2));
      if (idx >= 0) seen.add(idx);
    }
    const surjective = seen.size === n2Observed.shadows.length;
    r4Res = { ok: claimedR4.surjective === surjective && claimedR4.image_size === seen.size, claimed: { surjective: claimedR4.surjective, image_size: claimedR4.image_size }, recomputed: { surjective, image_size: seen.size, target_count: n2Observed.shadows.length } };
  }
  // R5: N3 -> N_Q, marked factor map X->i, Y->j: evaluate f_word directly in Q8
  const Q8 = makeQ8();
  const i8 = { s: 1, u: 1 }, j8 = { s: 1, u: 2 };
  const nqObserved = enumerateReducedHexagon(Q8, i8, j8, [0, 1, 2, 3]);
  const claimedR5 = (cert.reductions || []).find((r) => r.target === 'N_Q');
  let r5Res = { ok: false, reason: 'no R5 in cert.reductions' };
  if (claimedR5) {
    const seen = new Set();
    for (const sh of observed.shadows) {
      const fq8 = evalWordLeftAccum(Q8, i8, j8, sh.word);
      const newm = mod(sh.m, 4);
      const idx = nqObserved.shadows.findIndex((s) => s.m === newm && Q8.eq(s.f, fq8));
      if (idx >= 0) seen.add(idx);
    }
    const surjective = seen.size === nqObserved.shadows.length;
    r5Res = { ok: claimedR5.surjective === surjective && claimedR5.image_size === seen.size, claimed: { surjective: claimedR5.surjective, image_size: claimedR5.image_size }, recomputed: { surjective, image_size: seen.size, target_count: nqObserved.shadows.length } };
  }
  // U-F7 (司令塔裁定 2026-07-26): D_4^(2)=F2^4.gamma_2^2.gamma_4; agreement <=> exponent([P3,P3])<=2
  const derivedExpOk2b = [...uniRes.D.values()].every((g) => P3.eq(P3.pow(g, 2), P3.id));
  const uf7Status = cert.uf7_status === 'PASS' && derivedExpOk2b;
  const ok = hashRes.ok && selfCheck.ok && uniRes.ok && hexRes.ok && genRes.ok && kernelOk && cInNOk && evalModeOk && shadowSumOk && r4Res.ok && r5Res.ok && uf7Status;
  return { ok, target_hash: hashRes, p3_self_check: selfCheck, universe: uniRes, hexagon_free_certificate: hexRes, generation_detail: genRes, kernel_certificate: { ok: kernelOk, claimed: kernelClaim }, c_in_N: cInNOk, evaluation_mode: evalModeOk, shadow_sum_identity: shadowSumOk, reduction_R4_to_N2: r4Res, reduction_R5_to_N_Q: r5Res, uf7_derived_subgroup_exponent_le2: derivedExpOk2b, uf7_status_acknowledged: uf7Status, observed_shadow_total: observed.shadow_total };
}

function checkStage2a(cert) {
  const hashRes = checkTargetHash(cert);
  const P2 = makeHeis(4, 2);
  const X = { a: 1, b: 0, e: 0 }, Y = { a: 0, b: 1, e: 0 };
  const uniRes = checkUniverseSimple(cert, P2, X, Y, 4, 32);
  const charmingSet = (cert.universe && cert.universe.charming_set) || [0, 1, 2, 3];
  const observed = enumerateReducedHexagon(P2, X, Y, charmingSet);
  const hexRes = checkHexagonFreeCertificate(cert, observed);
  const genRes = checkGenerationDetailByEval(cert, P2, X, Y, uniRes.D);
  const kernelClaim = cert.kernel_certificate || {};
  const kernelOk = kernelClaim.kernel_scope === 'PB3' && kernelClaim.pb3_kernel_index === 32 && kernelClaim.b3_kernel_index === 192;
  const cInNOk = cert.c_in_N === true;
  const evalModeOk = cert.evaluation_mode === 'quotient_ok';
  const shadowSumOk = observed.candidate_total - observed.h10_fail - observed.h11_fail - observed.generation_fail === observed.shadow_total;
  // U-F6 (P2->Q8 leg): X->i, Y->j must respect relations (X^4=1 -> i^4=1, etc.) -- check by evaluating
  // the defining relators of P2 directly in Q8 under the generator map.
  const Q8 = makeQ8();
  const i8 = { s: 1, u: 1 }, j8 = { s: 1, u: 2 };
  const relatorsHold = Q8.eq(Q8.pow(i8, 4), Q8.id) && Q8.eq(Q8.pow(j8, 4), Q8.id) && Q8.eq(Q8.pow(Q8.mul(i8, j8), 4), Q8.id)
    && Q8.eq(commutator(Q8, i8, j8), Q8.mul(Q8.mul(Q8.inv(i8), Q8.inv(j8)), Q8.mul(i8, j8))); // sanity (always true), real check below
  const q8CommOrder2 = (() => { const c = commutator(Q8, i8, j8); return !Q8.eq(c, Q8.id) && Q8.eq(Q8.pow(c, 2), Q8.id); })();
  const uf6Ok = relatorsHold && q8CommOrder2;
  const uf6Claimed = (cert.uf6_check && cert.uf6_check.p2_to_q8_leg) === true;
  // R3: N2 -> N_Q, via the marked factor map (evaluate the SAME f_word directly in Q8)
  const nqObserved = enumerateReducedHexagon(Q8, i8, j8, [0, 1, 2, 3]);
  const claimed = (cert.reductions || []).find((r) => r.target === 'N_Q');
  let r3Res = { ok: false, reason: 'no R3 in cert.reductions' };
  if (claimed) {
    const seen = new Set();
    for (const sh of observed.shadows) {
      const fq8 = evalWordLeftAccum(Q8, i8, j8, sh.word);
      const newm = mod(sh.m, 4);
      const idx = nqObserved.shadows.findIndex((s) => s.m === newm && Q8.eq(s.f, fq8));
      if (idx >= 0) seen.add(idx);
    }
    const surjective = seen.size === nqObserved.shadows.length;
    r3Res = { ok: claimed.surjective === surjective && claimed.image_size === seen.size, claimed: { surjective: claimed.surjective, image_size: claimed.image_size }, recomputed: { surjective, image_size: seen.size, target_count: nqObserved.shadows.length } };
  }
  // U-F7 (司令塔裁定 2026-07-26): D_3^(2)=F2^4.gamma_2^2.gamma_3; agreement <=> exponent([P2,P2])<=2
  const derivedExpOk2a = [...uniRes.D.values()].every((g) => P2.eq(P2.pow(g, 2), P2.id));
  const uf7Status = cert.uf7_status === 'PASS' && derivedExpOk2a;
  const ok = hashRes.ok && uniRes.ok && hexRes.ok && genRes.ok && kernelOk && cInNOk && evalModeOk && shadowSumOk && uf6Ok && uf6Claimed && r3Res.ok && uf7Status;
  return { ok, target_hash: hashRes, universe: uniRes, hexagon_free_certificate: hexRes, generation_detail: genRes, kernel_certificate: { ok: kernelOk, claimed: kernelClaim }, c_in_N: cInNOk, evaluation_mode: evalModeOk, shadow_sum_identity: shadowSumOk, uf6_p2_to_q8: { ok: uf6Ok, claimed_matches: uf6Claimed }, uf7_derived_subgroup_exponent_le2: derivedExpOk2a, uf7_status_acknowledged: uf7Status, reduction_R3_to_N_Q: r3Res, observed_shadow_total: observed.shadow_total };
}

// ---------- P3 = F2/F2^4 gamma_4(F2), order 128, class 3 (own independent construction via direct
// word rewriting -- NOT copied from GAP's fp-group/IsomorphismPcGroup construction, which is
// opaque to me anyway; internal Pc collector data is not exposed to me from GAP). ----------
// Canonical form: X^a Y^b w^e p^f q^g (a,b mod 4; e,f,g mod 2), w=[X,Y], p=[w,X], q=[w,Y].
// IMPORTANT (found + fixed during independent verification): a first attempt used a hand-derived
// closed-form collection FORMULA (binomial-coefficient correction terms) that looked right on 3
// small hand-checked cases but FAILED associativity when checked exhaustively over all 128^3
// triples (393216 of 2097152 failed) -- a real bug caught by testing, not shipped. Replaced with a
// direct simulation of the defining relations themselves via bubble-sort-style word rewriting
// (each adjacent-letter swap literally applies one defining relation: YX=XYw, wX=Xwp, wY=Ywq, and
// p/q commute with everything since they are central) -- this is mechanically tied to the actual
// relations rather than a guessed closed form, and IS verified associative over all 128^3 triples,
// with w/p/q coming out "pure" (no cross-contamination) and BFS-closure from X,Y covering exactly
// 128 elements, before being adopted.
const P3_RANK = { X: 1, Y: 2, w: 3, p: 4, q: 5 };
function p3Normalize(tokens) {
  const arr = tokens.slice();
  let i = 0;
  while (i < arr.length - 1) {
    if (P3_RANK[arr[i]] > P3_RANK[arr[i + 1]]) {
      const l = arr[i], r = arr[i + 1];
      let emit = null;
      if (l === 'Y' && r === 'X') emit = 'w';
      else if (l === 'w' && r === 'X') emit = 'p';
      else if (l === 'w' && r === 'Y') emit = 'q';
      if (emit) arr.splice(i, 2, r, l, emit); else arr.splice(i, 2, r, l);
      i = i > 0 ? i - 1 : 0;
    } else { i++; }
  }
  const c = { X: 0, Y: 0, w: 0, p: 0, q: 0 };
  for (const t of arr) c[t]++;
  return { a: mod(c.X, 4), b: mod(c.Y, 4), e: mod(c.w, 2), f: mod(c.p, 2), q: mod(c.q, 2) };
}
function p3WordOf(g) {
  const out = [];
  for (let i = 0; i < g.a; i++) out.push('X');
  for (let i = 0; i < g.b; i++) out.push('Y');
  for (let i = 0; i < g.e; i++) out.push('w');
  for (let i = 0; i < g.f; i++) out.push('p');
  for (let i = 0; i < g.q; i++) out.push('q');
  return out;
}
function makeP3Group() {
  const id = { a: 0, b: 0, e: 0, f: 0, q: 0 };
  const mul = (g, h) => p3Normalize(p3WordOf(g).concat(p3WordOf(h)));
  const key = (g) => `${mod(g.a, 4)},${mod(g.b, 4)},${mod(g.e, 2)},${mod(g.f, 2)},${mod(g.q, 2)}`;
  const eq = (g, h) => key(g) === key(h);
  const elements = () => { const out = []; for (let a = 0; a < 4; a++) for (let b = 0; b < 4; b++) for (let e = 0; e < 2; e++) for (let f = 0; f < 2; f++) for (let q = 0; q < 2; q++) out.push({ a, b, e, f, q }); return out; };
  function invByBruteForce(g) {
    for (let a = 0; a < 4; a++) for (let b = 0; b < 4; b++) for (let e = 0; e < 2; e++) for (let f = 0; f < 2; f++) for (let q = 0; q < 2; q++) {
      const cand = { a, b, e, f, q };
      if (eq(mul(g, cand), id)) return cand;
    }
    throw new Error('makeP3Group: no inverse found (construction bug)');
  }
  const inv = (g) => invByBruteForce(g);
  const pow = (g, k) => {
    if (k === 0) return id;
    let base = k < 0 ? inv(g) : g, exponent = Math.abs(k), res = id;
    while (exponent > 0) { if (exponent % 2 === 1) res = mul(res, base); base = mul(base, base); exponent = Math.floor(exponent / 2); }
    return res;
  };
  return { id, mul, inv, key, eq, elements, pow };
}

// ---------- D_n and G3 = Im(psi_3) <= D3^3 (own independent construction, standard semidirect
// product Z_n rtimes Z_2 -- no ambiguity risk here unlike the F2-word evaluation order question
// above: this is a well-known, unambiguous formula, not a representation-specific convention) ----------
function makeDn(n) {
  const id = { a: 0, e: 0 };
  const mul = (g, h) => ({ a: mod(g.a + (g.e === 0 ? 1 : -1) * h.a, n), e: (g.e + h.e) % 2 });
  const inv = (g) => (g.e === 0 ? { a: mod(-g.a, n), e: 0 } : { a: mod(g.a, n), e: 1 });
  const key = (g) => `${mod(g.a, n)},${g.e}`;
  const eq = (g, h) => key(g) === key(h);
  const elements = () => { const out = []; for (let a = 0; a < n; a++) for (let e = 0; e < 2; e++) out.push({ a, e }); return out; };
  const pow = (g, k) => {
    if (k === 0) return id;
    let base = k < 0 ? inv(g) : g, exponent = Math.abs(k), res = id;
    while (exponent > 0) { if (exponent % 2 === 1) res = mul(res, base); base = mul(base, base); exponent = Math.floor(exponent / 2); }
    return res;
  };
  return { n, id, mul, inv, key, eq, elements, pow };
}

function cartesianProduct(arrays) {
  let result = [[]];
  for (const arr of arrays) {
    const next = [];
    for (const prefix of result) for (const item of arr) next.push(prefix.concat([item]));
    result = next;
  }
  return result;
}
function makeProduct(groups) {
  const id = groups.map((g) => g.id);
  const mul = (xs, ys) => xs.map((x, i) => groups[i].mul(x, ys[i]));
  const inv = (xs) => xs.map((x, i) => groups[i].inv(x));
  const key = (xs) => xs.map((x, i) => groups[i].key(x)).join('|');
  const eq = (xs, ys) => key(xs) === key(ys);
  const pow = (xs, k) => xs.map((x, i) => groups[i].pow(x, k));
  const elements = groups.every((g) => typeof g.elements === 'function')
    ? () => cartesianProduct(groups.map((g) => g.elements()))
    : undefined;
  return { id, mul, inv, key, eq, pow, elements };
}

// G3 = Im(psi_3) <= D3^3, X=(r,s,s), Y=(rs,r,rs) (2405.11725 (3.1), n=3). |G3| expected 108.
function buildG3() {
  const D3 = makeDn(3);
  const r = { a: 1, e: 0 }, s = { a: 0, e: 1 };
  const rs = D3.mul(r, s);
  const Triple = makeProduct([D3, D3, D3]);
  const X = [r, s, s], Y = [rs, r, rs];
  const G3Map = subgroupClosure(Triple, [X, Y]);
  return { D3, Triple, X, Y, G3Map, r, s };
}

function tripleToAE(elt, r, s, D3) {
  for (let a = 0; a < 3; a++) if (D3.eq(D3.pow(r, a), elt)) return [a, 0];
  for (let a = 0; a < 3; a++) if (D3.eq(D3.mul(s, D3.pow(r, a)), elt)) return [a, 1];
  throw new Error('tripleToAE: no match');
}

// fiber product Q_M = G3 x_{C2^2} Q8 <= (D3^3) x Q8, built exactly like the GAP script:
// ambient direct product on disjoint factors, generators X=(G3.X,Q8.i), Y=(G3.Y,Q8.j); the
// fiber-product order (216, not 108*8=864) falls out of BFS closure automatically.
function buildQM() {
  const G3 = buildG3();
  const Q8 = makeQ8();
  const i8 = { s: 1, u: 1 }, j8 = { s: 1, u: 2 };
  const ambient = makeProduct([G3.Triple, Q8]);
  const X = [G3.X, i8], Y = [G3.Y, j8];
  const QMap = subgroupClosure(ambient, [X, Y]);
  const Triple = { id: ambient.id, mul: ambient.mul, inv: ambient.inv, key: ambient.key, eq: ambient.eq, pow: ambient.pow, elements: () => [...QMap.values()] };
  return { G3, Q8, Triple, X, Y, QMap };
}

// ---------- stage 1b checker ----------
function checkUniverse1b(cert, QM, nOrd, D) {
  const u = cert.universe || {};
  const expectedCharming = Array.from({ length: nOrd }, (_, m) => m).filter((m) => gcd(2 * m + 1, nOrd) === 1);
  const checks = {
    pb3_index: u.pb3_index === QM.QMap.size && QM.QMap.size === 216,
    b3_points: u.b3_points === 6 * QM.QMap.size,
    n_ord: u.n_ord === nOrd,
    derived_order: u.derived_order === D.size,
    charming_set: JSON.stringify((u.charming_set || []).slice().sort((a, b) => a - b)) === JSON.stringify(expectedCharming),
    candidate_total: u.candidate_total === expectedCharming.length * D.size,
  };
  return { ok: Object.values(checks).every(Boolean), checks, observed: { pb3_index: QM.QMap.size, b3_points: 6 * QM.QMap.size, n_ord: nOrd, derived_order: D.size, charming_set: expectedCharming, candidate_total: expectedCharming.length * D.size } };
}

function checkReductionR1(cert, QM, observed) {
  const k3Path = join(CERT_DIR, 'K3.v1.json');
  if (!existsSync(k3Path)) return { ok: false, reason: 'K3.v1.json not found' };
  const k3 = JSON.parse(readFileSync(k3Path, 'utf8'));
  const k3Shadows = k3.shadows; // [{m, f_triple, ...}]
  const claimed = (cert.reductions || []).find((r) => r.target === 'K3');
  if (!claimed) return { ok: false, reason: 'no R1 (target=K3) in cert.reductions' };
  const seen = new Set();
  const images = [];
  for (const sh of observed.shadows) {
    const g3elt = sh.f[0]; // ambient element is [G3triple, Q8elt]; f[0] is G3-Triple part
    const triple = g3elt.map((d) => tripleToAE(d, QM.G3.r, QM.G3.s, QM.G3.D3));
    const newm = mod(sh.m, 6);
    let idx = -1;
    for (let t = 0; t < k3Shadows.length; t++) {
      const ks = k3Shadows[t];
      if (ks.m === newm && JSON.stringify(ks.f_triple) === JSON.stringify(triple)) { idx = t; break; }
    }
    images.push(idx);
    if (idx >= 0) seen.add(idx);
  }
  const surjective = seen.size === k3Shadows.length;
  const imageSize = seen.size;
  const claimedOk = claimed.surjective === surjective && claimed.image_size === imageSize;
  return { ok: claimedOk, claimed: { surjective: claimed.surjective, image_size: claimed.image_size }, recomputed: { surjective, image_size: imageSize, target_count: k3Shadows.length } };
}

function checkReductionR2(cert, QM, observed, nqObserved) {
  const claimed = (cert.reductions || []).find((r) => r.target === 'N_Q');
  if (!claimed) return { ok: false, reason: 'no R2 (target=N_Q) in cert.reductions' };
  const Q8 = QM.Q8;
  const seen = new Set();
  const images = [];
  for (const sh of observed.shadows) {
    const q8elt = sh.f[1]; // ambient element [G3triple, Q8elt]; f[1] is Q8 part
    const newm = mod(sh.m, 4);
    let idx = -1;
    for (let t = 0; t < nqObserved.shadows.length; t++) {
      if (nqObserved.shadows[t].m === newm && Q8.eq(nqObserved.shadows[t].f, q8elt)) { idx = t; break; }
    }
    images.push(idx);
    if (idx >= 0) seen.add(idx);
  }
  const surjective = seen.size === nqObserved.shadows.length;
  const imageSize = seen.size;
  const claimedOk = claimed.surjective === surjective && claimed.image_size === imageSize;
  return { ok: claimedOk, claimed: { surjective: claimed.surjective, image_size: claimed.image_size }, recomputed: { surjective, image_size: imageSize, target_count: nqObserved.shadows.length } };
}

function checkStage1b(cert) {
  const hashRes = checkTargetHash(cert);
  const QM = buildQM();
  const X = QM.X, Y = QM.Y;
  const Triple = QM.Triple;
  const nOrd = lcm(6, 4); // ord(x)=lcm(ord in G3=6, ord in Q8=4)... use observed order via charming set instead
  const genMap = subgroupClosure(Triple, [X, Y]);
  const D = derivedSubgroup(Triple, genMap, X, Y);
  const uniRes = checkUniverse1b(cert, QM, nOrd, D);
  const charmingSet = (cert.universe && cert.universe.charming_set) || [0, 2, 3, 5, 6, 8, 9, 11];
  const observed = enumerateReducedHexagon(Triple, X, Y, charmingSet);
  const hexRes = checkHexagonFreeCertificate(cert, observed);
  const genRes = checkGenerationDetailByEval(cert, Triple, X, Y, D);
  const kernelClaim = cert.kernel_certificate || {};
  const kernelOk = kernelClaim.kernel_scope === 'PB3' && kernelClaim.pb3_kernel_index === 216 && kernelClaim.b3_kernel_index === 1296;
  const cInNOk = cert.c_in_N === true;
  const evalModeOk = cert.evaluation_mode === 'quotient_ok';
  const shadowSumOk = observed.candidate_total - observed.h10_fail - observed.h11_fail - observed.generation_fail === observed.shadow_total;
  // R2 needs N_Q's own shadow set, recomputed independently here too
  const Q8 = QM.Q8;
  const i8 = { s: 1, u: 1 }, j8 = { s: 1, u: 2 };
  const nqObserved = enumerateReducedHexagon(Q8, i8, j8, [0, 1, 2, 3]);
  const r1Res = checkReductionR1(cert, QM, observed);
  const r2Res = checkReductionR2(cert, QM, observed, nqObserved);
  const ok = hashRes.ok && uniRes.ok && hexRes.ok && genRes.ok && kernelOk && cInNOk && evalModeOk && shadowSumOk && r1Res.ok && r2Res.ok;
  return { ok, target_hash: hashRes, universe: uniRes, hexagon_free_certificate: hexRes, generation_detail: genRes, kernel_certificate: { ok: kernelOk, claimed: kernelClaim }, c_in_N: cInNOk, evaluation_mode: evalModeOk, shadow_sum_identity: shadowSumOk, reduction_R1_to_K3: r1Res, reduction_R2_to_N_Q: r2Res, observed_shadow_total: observed.shadow_total };
}

// ---------- permutations on {1..n} (own independent implementation, array-based 1-indexed) ----------
function makeSymGroupHelpers(n) {
  const id = Array.from({ length: n }, (_, i) => i + 1);
  const mul = (p, q) => p.map((_, i) => q[p[i] - 1]); // apply p then q (matches GAP's p*q convention, empirically verified in stage 1a/A1 debugging)
  const inv = (p) => { const r = new Array(n); p.forEach((v, i) => { r[v - 1] = i + 1; }); return r; };
  const key = (p) => p.join(',');
  const eq = (p, q) => key(p) === key(q);
  const pow = (p, k) => { if (k === 0) return id; let base = k < 0 ? inv(p) : p, exponent = Math.abs(k), res = id; while (exponent > 0) { if (exponent % 2 === 1) res = mul(res, base); base = mul(base, base); exponent = Math.floor(exponent / 2); } return res; };
  return { id, mul, inv, key, eq, pow, n };
}
function cyclesToPerm(n, cycles) {
  const p = Array.from({ length: n }, (_, i) => i + 1);
  for (const cyc of cycles) {
    for (let i = 0; i < cyc.length; i++) { const a = cyc[i], b = cyc[(i + 1) % cyc.length]; p[a - 1] = b; }
  }
  return p;
}

function checkStageA1(cert) {
  const hashRes = checkTargetHash(cert);
  const S5 = makeSymGroupHelpers(5);
  // generators taken verbatim from the spec-disclosed marking block (same data GAP used; using
  // given spec literals is not "importing GAP code" -- it is using spec data, same as K3.v1.json).
  const t = cyclesToPerm(5, [[1, 2, 3]]);
  const a = cyclesToPerm(5, [[1, 4, 5]]);
  const X = cyclesToPerm(5, [[1, 3, 2, 4, 5]]);
  const Y = cyclesToPerm(5, [[1, 3, 4, 5, 2]]);
  const Z = cyclesToPerm(5, [[1, 4, 5, 3, 2]]);
  const s = cyclesToPerm(5, [[1, 4], [3, 5]]);
  // A-F1 self-check (reversed-product convention, same finding as GAP script)
  const ord = (g) => { let k = 1, cur = g; while (!S5.eq(cur, S5.id)) { cur = S5.mul(cur, g); k++; } return k; };
  const f1a = ord(X) === 5 && ord(Y) === 5 && ord(Z) === 5;
  const f1b = S5.eq(S5.mul(S5.mul(Z, Y), X), S5.id);
  const f1c = ord(s) === 2;
  const f1d = S5.eq(S5.mul(S5.mul(s, X), S5.inv(s)), Y);
  const f1e = ord(t) === 3;
  const tinv = S5.inv(t);
  const f1f = S5.eq(S5.mul(S5.mul(tinv, X), t), Y) && S5.eq(S5.mul(S5.mul(tinv, Y), t), Z) && S5.eq(S5.mul(S5.mul(tinv, Z), t), X);
  const f1g = S5.eq(S5.mul(tinv, a), X);
  const selfCheckOk = f1a && f1b && f1c && f1d && f1e && f1f && f1g;
  const genMap = subgroupClosure(S5, [X, Y]);
  const uniRes = checkUniverseSimple(cert, S5, X, Y, 5, 60);
  const derivedIsFull = uniRes.D.size === 60; // A5 perfect
  const charmingSet = (cert.universe && cert.universe.charming_set) || [0, 1, 3, 4];
  const observed = enumerateReducedHexagon(S5, X, Y, charmingSet);
  const hexRes = checkHexagonFreeCertificate(cert, observed);
  const genRes = checkGenerationDetailByEval(cert, S5, X, Y, uniRes.D);
  const kernelClaim = cert.kernel_certificate || {};
  const kernelOk = kernelClaim.kernel_scope === 'PB3' && kernelClaim.pb3_kernel_index === 60 && kernelClaim.b3_kernel_index === 360;
  const cInNOk = cert.c_in_N === true;
  const evalModeOk = cert.evaluation_mode === 'quotient_ok';
  const shadowSumOk = observed.candidate_total - observed.h10_fail - observed.h11_fail - observed.generation_fail === observed.shadow_total;
  const layerBlocked = cert.layer_id === 'BLOCKED';
  const ok = hashRes.ok && selfCheckOk && genMap.size === 60 && uniRes.ok && derivedIsFull && hexRes.ok && genRes.ok && kernelOk && cInNOk && evalModeOk && shadowSumOk && layerBlocked;
  return { ok, target_hash: hashRes, a5_self_check: { f1a, f1b, f1c, f1d, f1e, f1f, f1g, ok: selfCheckOk }, generated_order: genMap.size, universe: uniRes, derived_is_full_A5: derivedIsFull, hexagon_free_certificate: hexRes, generation_detail: genRes, kernel_certificate: { ok: kernelOk, claimed: kernelClaim }, c_in_N: cInNOk, evaluation_mode: evalModeOk, shadow_sum_identity: shadowSumOk, layer_id_blocked_acknowledged: layerBlocked, observed_shadow_total: observed.shadow_total };
}

// ---------- driver ----------
function loadCert(id) {
  const path = join(CERT_DIR, `${id}.v2.json`);
  return JSON.parse(readFileSync(path, 'utf8'));
}

function main() {
  if (!existsSync(VERDICT_DIR)) mkdirSync(VERDICT_DIR, { recursive: true });
  const results = {};
  const stageIds = process.argv.slice(2).length ? process.argv.slice(2) : ['1a'];
  for (const id of stageIds) {
    const certPath = join(CERT_DIR, `${id}.v2.json`);
    if (!existsSync(certPath)) { results[id] = { ok: false, reason: 'certificate not found', path: certPath }; continue; }
    const cert = loadCert(id);
    let verdict;
    if (id === '1a') verdict = checkStage1a(cert);
    else if (id === '1b') verdict = checkStage1b(cert);
    else if (id === '2a') verdict = checkStage2a(cert);
    else if (id === '2b') verdict = checkStage2b(cert);
    else if (id === 'A1') verdict = checkStageA1(cert);
    else verdict = { ok: false, reason: `stage ${id} checker not implemented yet in check-v2.mjs` };
    results[id] = verdict;
    writeFileSync(join(VERDICT_DIR, `${id}.v2.verdict.json`), JSON.stringify(verdict, null, 2));
    console.log(`stage ${id}: ${verdict.ok ? 'PASS' : 'FAIL'}`);
    console.log(JSON.stringify(verdict, null, 2));
  }
  const allOk = Object.values(results).every((r) => r.ok);
  console.log(`\ncheck-v2.mjs overall: ${allOk ? 'all_pass' : 'FAIL'}`);
}

main();
