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
