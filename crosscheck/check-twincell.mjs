#!/usr/bin/env node
// crosscheck/check-twincell.mjs -- 独立照合器 for the level-16 twin-cell enumerator
// (search/twincell-enum.g / docs/manifest_twincell_v1.md).
//
// ── ツール仕様ヘッダ ─────────────────────────────────────────────────────
// 入力: certificates/twincell/*.json のみ(証明書ファイル)。search/twincell-enum.g や
//   search/week3-battery-common.g・search/gaplib_common.g は import しない(CLAUDE.md 鉄則2:
//   探索器と照合器の分離)。matrix-mod-L 演算・D4^3 埋め込み・reduced-hexagon 列挙・
//   marked-factor-map 全単射照合は、すべてこのファイル内で一から再実装する(check-v2.mjs /
//   check-psl.mjs と同じ「毎照合器が独立に再導出する」という工房の慣行 -- helper の使い回しは
//   探索器/照合器間だけでなく照合器どうしでも避ける)。
// モード/触れてよいデータ範囲: 証明書の claimed 値の再計算のみ。GAP 側の中間状態には触れない。
// 出力スキーマ: crosscheck/verdicts/<window_id>.twincell.verdict.json(ok/errors/observed)。
// 検査する不変量: universe(pb3_index/n_ord/charming_set/derived_order/candidate_total)・
//   hexagon_free_certificate(candidate_total/h10_fail/h11_fail/generation_fail/shadow_total)・
//   generation_detail の再評価一致・較正①(marked factor map 全単射, matrix-mod-8 <-> D4^3)・
//   較正②(marked factor map 全単射, matrix-mod-10 <-> A5 permutation, + A5-CONV 適合テスト)・
//   較正③(K^(8) の既知値 |GT|=16, Thm 4.3/5.3 alpha=3 -- 標的窓の証明書が存在する場合のみ)・
//   (自己テスト)証明書の数値を故意に壊した clone が FAIL することの確認。
//
// 【読み方の注意・falsifier 監査 §5a 軽微指摘への対応】「window <id>: PASS/FAIL」という行は
// **その証明書単体の自己無矛盾性**(claimed 値 = 独立再計算値)を意味するだけであり、
// 「その窓が較正に合格した」という意味ではない。負例 fixture の証明書は、正直に作られていれば
// 自己無矛盾なので self-consistency は PASS になる(=正しい振る舞い) -- 負例としての合否は
// 別行の「NEGATIVE FIXTURE ... correctly_rejected」で報告される。
'use strict';
import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const CERT_DIR = join(ROOT, 'certificates', 'twincell');
const VERDICT_DIR = join(ROOT, 'crosscheck', 'verdicts');

function mod(a, n) { return ((a % n) + n) % n; }
function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; }

// ================= matrix-mod-L group (own from-scratch construction) =================
// element = [a,b,c,d] (row-major [[a,b],[c,d]] mod L), canonicalized under m ~ -m (mod +-1).
function matMulL(m, n, L) {
  const [a, b, c, d] = m, [e, f, g, h] = n;
  return [mod(a * e + b * g, L), mod(a * f + b * h, L), mod(c * e + d * g, L), mod(c * f + d * h, L)];
}
function matNegL(m, L) { return m.map((x) => mod(-x, L)); }
function matKeyInt(m, L) { return ((m[0] * L + m[1]) * L + m[2]) * L + m[3]; }
// 罠(発見・修理 2026-07-26 事後デルタ対応中, GAP 側 search/twincell-enum.g と同じ修理):
// 正準化は「まず全エントリを mod L 還元してから」比較しないと、生の(未還元の)整数リテラル
// (例: -2)と、他所で既に還元済みの同じ抽象元(例: L-2)とで異なる代表元が選ばれてしまう
// (整数キーは還元前後で値が違うため)。kernel_certificate.generator_images を証明書の文字列
// から parse した値と、この照合器が独自に構築した X/Y とを比較する際、両者が同じ正準化規約を
// 使っていないと偽の不一致が出る -- 入力を必ず mod L 還元してから比較することで解消する
// (入力が既に還元済みでも冪等なので無害)。
function matCanonL(m, L) { const mr = m.map((x) => mod(x, L)); const neg = matNegL(mr, L); return matKeyInt(mr, L) <= matKeyInt(neg, L) ? mr : neg; }

function makeMatGroup(L) {
  const id = matCanonL([1, 0, 0, 1], L);
  const X = matCanonL([1, 2, 0, 1], L);
  const Y = matCanonL([1, 0, -2, 1], L);
  const mul = (g, h) => matCanonL(matMulL(g, h, L), L);
  const key = (g) => String(matKeyInt(g, L));
  const eq = (g, h) => key(g) === key(h);
  const inv = (g) => matCanonL([g[3], mod(-g[1], L), mod(-g[2], L), g[0]], L);
  const pow = (g, k) => {
    if (k === 0) return id;
    let base = k < 0 ? inv(g) : g, e = Math.abs(k), res = id;
    while (e > 0) { if (e % 2 === 1) res = mul(res, base); base = mul(base, base); e = Math.floor(e / 2); }
    return res;
  };
  return { id, X, Y, mul, inv, key, eq, pow, L };
}

function matStrToArr(s) {
  const nums = s.match(/-?\d+/g).map(Number);
  return nums; // [a,b,c,d]
}

// ================= kernel_certificate.generator_images parsers (司令塔続報「事後デルタ」要求1
// への対応: 数値の重複+文章だけの kernel_certificate をやめ、N を定義する psi: F2->>Q の
// 生成元像そのものを machine-parseable な文字列で持たせ、この照合器が独自に構築した (G,X,Y) と
// 突き合わせて独立に再検証する。フォーマットは窓の構成方式(matrix / D_n^3-triple / A5-perm)
// ごとに異なるので、window_id で分岐してパースする。) =================
function parseGeneratorImageMatrix(str, L) { return matCanonL(matStrToArr(str), L); }
function parseGeneratorImageDnTriple(str, n) {
  const arr = JSON.parse(str); // "[[a1,e1],[a2,e2],[a3,e3]]" -- valid JSON already
  return arr.map(([a, e]) => ({ a: mod(a, n), e: mod(e, 2) }));
}
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

// ================= D_n and D_n^3 embedding G_n = <x,y> <= D_n^3 (own from-scratch construction,
// mirrors D1 (3.6): x=(r,s,s), y=(rs,r,rs). Independent of search/week3-battery-common.g's MakeGn
// (separate code, not imported). ) =================
function makeDn(n) {
  const id = { a: 0, e: 0 };
  const mul = (g, h) => ({ a: mod(g.a + (g.e === 0 ? 1 : -1) * h.a, n), e: (g.e + h.e) % 2 });
  const inv = (g) => (g.e === 0 ? { a: mod(-g.a, n), e: 0 } : { a: mod(g.a, n), e: 1 });
  const key = (g) => `${mod(g.a, n)},${g.e}`;
  const eq = (g, h) => key(g) === key(h);
  const pow = (g, k) => {
    if (k === 0) return id;
    let base = k < 0 ? inv(g) : g, e = Math.abs(k), res = id;
    while (e > 0) { if (e % 2 === 1) res = mul(res, base); base = mul(base, base); e = Math.floor(e / 2); }
    return res;
  };
  return { n, id, mul, inv, key, eq, pow };
}
function makeTripleGroup(D) {
  const id = [D.id, D.id, D.id];
  const mul = (g, h) => [D.mul(g[0], h[0]), D.mul(g[1], h[1]), D.mul(g[2], h[2])];
  const inv = (g) => g.map(D.inv);
  const key = (g) => g.map(D.key).join('|');
  const eq = (g, h) => key(g) === key(h);
  const pow = (g, k) => {
    if (k === 0) return id;
    let base = k < 0 ? inv(g) : g, e = Math.abs(k), res = id;
    while (e > 0) { if (e % 2 === 1) res = mul(res, base); base = mul(base, base); e = Math.floor(e / 2); }
    return res;
  };
  return { id, mul, inv, key, eq, pow };
}
function makeGn(n) {
  const D = makeDn(n);
  const T = makeTripleGroup(D);
  const r = { a: 1, e: 0 }, s = { a: 0, e: 1 };
  const rs = D.mul(r, s);
  const X = [r, s, s], Y = [rs, r, rs];
  return { T, X, Y, D, n };
}

// ================= generic BFS closure / derived subgroup (own implementation) =================
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
function derivedSubgroup(G, genMap) {
  const gensArr = [...genMap.values()];
  const c0 = commutator(G, gensArr.find(() => true), gensArr.find(() => true)); // placeholder, replaced below
  return derivedSubgroupFromXY(G, genMap);
}
function derivedSubgroupFromXY(G, genMap, X, Y) {
  const c0 = commutator(G, X, Y);
  const conjugates = [];
  for (const g of genMap.values()) conjugates.push(G.mul(G.mul(g, c0), G.inv(g)));
  return subgroupClosure(G, conjugates);
}

// prepend-convention BFS word assignment + evaluation (matches GAP's BFSWords/EvalWordInQ, the
// convention this whole codebase uses for the quotient-shortcut EnumerateReducedHexagon pipeline
// -- verified against crosscheck/check-psl.mjs's bfsWords/evalWordPrepend, independently reimplemented
// here rather than imported).
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
    for (const [sym, p, gelt] of gens) {
      const nv = G.mul(gelt, cur); // prepend
      const k = G.key(nv);
      if (!wordOf.has(k)) { wordOf.set(k, curWord.concat([[sym, p]])); queue.push(nv); }
    }
  }
  return { wordOf, elements: queue };
}
function evalWordPrepend(G, X, Y, word) {
  let val = G.id;
  for (const [sym, p] of word) { const g = sym === 'x' ? X : Y; val = G.mul(G.pow(g, p), val); }
  return val;
}
function thetaWord(w) { return w.map(([s, p]) => (s === 'x' ? ['y', p] : ['x', p])); }
function tauWord(w) { return w.flatMap(([s, p]) => (s === 'x' ? [['y', p]] : (p === 1 ? [['y', -1], ['x', -1]] : [['x', 1], ['y', 1]]))); }

function enumerateReducedHexagon(G, X, Y, charmingSet) {
  const genMap = subgroupClosure(G, [X, Y]);
  const D = derivedSubgroupFromXY(G, genMap, X, Y);
  const { wordOf, elements } = bfsWords(G, X, Y);
  const dWords = [];
  for (const elt of elements) if (D.has(G.key(elt))) dWords.push({ elt, word: wordOf.get(G.key(elt)) });
  let h10Fail = 0, h11Fail = 0, genFail = 0;
  const shadows = [];
  const genDetail = [];
  for (const cand of dWords) {
    const f = cand.elt;
    for (const m of charmingSet) {
      const u = 2 * m + 1;
      const th = thetaWord(cand.word);
      const hex310 = G.eq(evalWordPrepend(G, X, Y, cand.word.concat(th)), G.id);
      if (!hex310) { h10Fail++; genDetail.push({ m, f_word: cand.word, pass: false, stage: 'h10_fail' }); continue; }
      const yWordM = Array.from({ length: m }, () => ['y', 1]);
      const ymfWord = yWordM.concat(cand.word);
      const tau1 = tauWord(ymfWord), tau2 = tauWord(tau1);
      const hex311 = G.eq(evalWordPrepend(G, X, Y, tau2.concat(tau1, ymfWord)), G.id);
      if (!hex311) { h11Fail++; genDetail.push({ m, f_word: cand.word, pass: false, stage: 'h11_fail' }); continue; }
      const genA = G.pow(X, u);
      const genB = G.mul(G.mul(f, G.pow(Y, u)), G.inv(f)); // reversed, matches AbstractProd genB
      const gen = subgroupClosure(G, [genA, genB]);
      if (gen.size === genMap.size) { shadows.push({ m, f, word: cand.word }); genDetail.push({ m, f_word: cand.word, pass: true, stage: 'pass' }); }
      else { genFail++; genDetail.push({ m, f_word: cand.word, pass: false, stage: 'generation_fail' }); }
    }
  }
  return {
    candidate_total: dWords.length * charmingSet.length, h10_fail: h10Fail, h11_fail: h11Fail,
    generation_fail: genFail, shadow_total: shadows.length, shadows, generation_detail: genDetail,
    G_size: genMap.size, derived_size: D.size,
  };
}

// ================= A5 permutation construction (own from-scratch reimplementation of the marking
// verbatim from certificates/A1.v2.json / week3-battery-A1.g: X=(1,3,2,4,5), Y=(1,3,4,5,2) --
// this is spec-disclosed known marking data, not an import of search/ code) =================
function permMul(p, q) { return p.map((_, i) => q[p[i]]); }
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
function cyclesToPerm(n, cycles) {
  const perm = permId(n);
  for (const cyc of cycles) {
    const idx = cyc.map((x) => x - 1);
    for (let i = 0; i < idx.length; i++) perm[idx[i]] = idx[(i + 1) % idx.length];
  }
  return perm;
}
function makePermWrapper(n) {
  return { id: permId(n), mul: permMul, inv: permInv, key: (p) => p.join(','), eq: permEq, pow: permPow };
}
function makeA5Construction() {
  const G = makePermWrapper(5);
  const X = cyclesToPerm(5, [[1, 3, 2, 4, 5]]);
  const Y = cyclesToPerm(5, [[1, 3, 4, 5, 2]]);
  return { G, X, Y };
}

// ================= per-construction group builders keyed by window_id =================
function groupForWindow(windowId) {
  if (windowId.startsWith('C8_matrix_mod8_Ybar_signflip')) {
    const g = makeMatGroup(8);
    g.Y = matCanonL([1, 0, 2, 1], 8); // sign-flip variant (BONUS, not a fixture)
    return { G: g, X: g.X, Y: g.Y };
  }
  if (windowId.startsWith('C8_matrix_WRONG_LEVEL6')) { const g = makeMatGroup(6); return { G: g, X: g.X, Y: g.Y }; }
  if (windowId.startsWith('C8_matrix') || windowId === 'C8_matrix_mod8') { const g = makeMatGroup(8); return { G: g, X: g.X, Y: g.Y }; }
  if (windowId === 'C10_A5_permutation') { return makeA5Construction(); }
  if (windowId.startsWith('C10_matrix')) { const g = makeMatGroup(10); return { G: g, X: g.X, Y: g.Y }; }
  if (windowId.startsWith('C16_matrix')) { const g = makeMatGroup(16); return { G: g, X: g.X, Y: g.Y }; }
  if (windowId === 'C8_D4cubed') { const gn = makeGn(4); return { G: gn.T, X: gn.X, Y: gn.Y }; }
  if (windowId === 'K8_MakeGn8') { const gn = makeGn(8); return { G: gn.T, X: gn.X, Y: gn.Y }; }
  return null;
}

// ================= A5-CONV 適合テスト(twincell 固有・falsifier 監査 §4 軽微指摘への対応)
// docs/week1-定義ノート.md §1.5.4 の判定式 ev(y x^-1) = (1 2 4) を、C10 matrix-mod-10 構成の
// 要素を実際に BFS で得た語に変換し、その同じ語を A5 permutation 構成側で評価する(較正②の
// marked bijection と同じ「語の転送」による、GAP 側 twincell-enum.g の手続きに正確に対応)。=================
function checkA5ConvViaBijection(matRes, a5Res) {
  const word = [['y', 1], ['x', -1]];
  const fMat = evalWordPrepend(matRes.G, matRes.X, matRes.Y, word);
  const { wordOf } = bfsWords(matRes.G, matRes.X, matRes.Y);
  const w = wordOf.get(matRes.G.key(fMat));
  if (w === undefined) return { ok: false, reason: 'f (y x^-1 in matrix group) not found via BFS -- should be unreachable' };
  const img = evalWordPrepend(a5Res.G, a5Res.X, a5Res.Y, w);
  const target = cyclesToPerm(5, [[1, 2, 4]]);
  return { ok: a5Res.G.eq(img, target), observed: img, target };
}

// ================= per-certificate check =================
function checkCert(cert, opts = {}) {
  const errors = [];
  const windowId = cert.window_id;
  const built = groupForWindow(windowId);
  if (!built) { errors.push(`unknown window_id: ${windowId} (checker not extended for this construction)`); return { ok: false, errors }; }
  const { G, X, Y } = built;

  const genMap = subgroupClosure(G, [X, Y]);
  const pb3Index = genMap.size;
  if (!opts.skipUniverse && pb3Index !== cert.universe.pb3_index) errors.push(`pb3_index observed=${pb3Index} claimed=${cert.universe.pb3_index}`);
  const b3Points = 6 * pb3Index;
  if (!opts.skipUniverse && b3Points !== cert.universe.b3_points) errors.push(`b3_points observed=${b3Points} claimed=${cert.universe.b3_points}`);

  const ordX = orderOf(G, X), ordY = orderOf(G, Y);
  const nOrd = lcm(ordX, ordY);
  if (!opts.skipUniverse && nOrd !== cert.universe.n_ord) errors.push(`n_ord observed=${nOrd} claimed=${cert.universe.n_ord}`);
  const charmingSet = Array.from({ length: nOrd }, (_, m) => m).filter((m) => gcd(2 * m + 1, nOrd) === 1);
  if (!opts.skipUniverse && JSON.stringify(charmingSet) !== JSON.stringify(cert.universe.charming_set)) errors.push('charming_set mismatch');

  const derivedMap = derivedSubgroupFromXY(G, genMap, X, Y);
  const derivedOrder = derivedMap.size;
  if (!opts.skipUniverse && derivedOrder !== cert.universe.derived_order) errors.push(`derived_order observed=${derivedOrder} claimed=${cert.universe.derived_order}`);
  const candidateTotal = charmingSet.length * derivedOrder;
  if (!opts.skipUniverse && candidateTotal !== cert.universe.candidate_total) errors.push(`candidate_total observed=${candidateTotal} claimed=${cert.universe.candidate_total}`);

  const observed = enumerateReducedHexagon(G, X, Y, charmingSet);
  const claimedHex = cert.hexagon_free_certificate || {};
  const hexOk = claimedHex.candidate_total === observed.candidate_total && claimedHex.h10_fail === observed.h10_fail
    && claimedHex.h11_fail === observed.h11_fail && claimedHex.generation_fail === observed.generation_fail
    && claimedHex.shadow_total === observed.shadow_total;
  if (!hexOk) errors.push(`hexagon_free_certificate mismatch: observed=${JSON.stringify({ candidate_total: observed.candidate_total, h10_fail: observed.h10_fail, h11_fail: observed.h11_fail, generation_fail: observed.generation_fail, shadow_total: observed.shadow_total })} claimed=${JSON.stringify(claimedHex)}`);

  const sumOk = (claimedHex.candidate_total - claimedHex.h10_fail - claimedHex.h11_fail - claimedHex.generation_fail) === claimedHex.shadow_total;
  if (!sumOk) errors.push('shadow_sum_identity fails on claimed values');

  // recompute each claimed generation_detail entry from its own f_word (independent, not just
  // trusting our own BFS's word choice for the same element)
  let genMismatches = 0;
  for (const gd of (cert.generation_detail || [])) {
    const f = evalWordPrepend(G, X, Y, gd.f_word);
    const m = gd.m, u = 2 * m + 1;
    const th = thetaWord(gd.f_word);
    const hex310 = G.eq(evalWordPrepend(G, X, Y, gd.f_word.concat(th)), G.id);
    let pass = false, stage = 'h10_fail';
    if (hex310) {
      const yWordM = Array.from({ length: m }, () => ['y', 1]);
      const ymfWord = yWordM.concat(gd.f_word);
      const tau1 = tauWord(ymfWord), tau2 = tauWord(tau1);
      const hex311 = G.eq(evalWordPrepend(G, X, Y, tau2.concat(tau1, ymfWord)), G.id);
      if (hex311) {
        const genA = G.pow(X, u);
        const genB = G.mul(G.mul(f, G.pow(Y, u)), G.inv(f));
        const gen = subgroupClosure(G, [genA, genB]);
        if (gen.size === genMap.size) { pass = true; stage = 'pass'; } else stage = 'generation_fail';
      } else stage = 'h11_fail';
    }
    if (pass !== gd.pass || stage !== gd.stage) genMismatches++;
  }
  if (genMismatches > 0) errors.push(`${genMismatches} generation_detail mismatches on independent re-evaluation`);

  // ---- settled/isolated (only checked when the certificate actually claims settled_detail --
  // calibration windows C8/C10 don't compute this, target windows C16/K8 do per the fire
  // instructions). settled: the induced map x->x^u, y->f^-1 y^u f is a genuine AUTOMORPHISM of G
  // (own re-derivation, not reusing GAP's GroupHomomorphismByImages result).
  //
  // 【要修正→強化(falsifier 監査「事後デルタ」問い1)】旧実装は BFS 全域木の代表語だけを
  // targetX/targetY で再評価し、その像集合の濃度が |G| と一致するかだけを見ていた -- これは
  // 「代表語ベースの関数としての単射性」でしかなく、全域木に含まれない辺(非木辺・Cayley
  // グラフの関係式)が targetX/targetY の下でも保存されるかを一度も検査していなかった
  // (falsifier が独立に書いた第三スクリプトが手本として示した弱点)。
  // 強化版: 全要素 g in G と全生成元方向 gen in {x,+1},{x,-1},{y,+1},{y,-1} について
  // F(g*gen) == F(g)*targetGen(このgen方向のtarget像)を悉皆検査する(|G|×4 回、G=256でも軽量)。
  // これは真の群準同型としての well-definedness を保証する完全なチェックであり(F が生成元との
  // 積演算をどの経路でも一貫して尊重することを直接確認するので、単なる代表語の単射性より強い)、
  // かつ image-size による全単射性チェックも維持する(両方が真のとき初めて settled=true)。
  let settledObserved = null;
  if (Array.isArray(cert.settled_detail)) {
    const { wordOf, elements } = bfsWords(G, X, Y);
    const invX = G.inv(X), invY = G.inv(Y);
    let settledCount = 0;
    const detail = [];
    for (const sd of cert.settled_detail) {
      const m = sd.m, u = 2 * m + 1;
      const f = evalWordPrepend(G, X, Y, sd.f_word);
      const targetX = G.pow(X, u);
      const targetY = G.mul(G.mul(f, G.pow(Y, u)), G.inv(f));
      const invTX = G.inv(targetX), invTY = G.inv(targetY);
      const gens = [['x', 1, X, targetX], ['x', -1, invX, invTX], ['y', 1, Y, targetY], ['y', -1, invY, invTY]];
      const Fcache = new Map();
      const Fof = (g) => {
        const k = G.key(g);
        if (Fcache.has(k)) return Fcache.get(k);
        const val = evalWordPrepend(G, targetX, targetY, wordOf.get(k));
        Fcache.set(k, val);
        return val;
      };
      const imageSet = new Set();
      for (const elt of elements) imageSet.add(G.key(Fof(elt)));
      const bijective = imageSet.size === elements.length;
      let relationViolations = 0;
      for (const g of elements) {
        const Fg = Fof(g);
        for (const [, , gelt, targetGelt] of gens) {
          const h = G.mul(g, gelt); // g * gen, using the ORIGINAL generators' multiplication (Cayley graph edge)
          const Fh = Fof(h);
          const rhs = G.mul(Fg, targetGelt); // F(g) * targetGen (what a genuine homomorphism must give)
          if (!G.eq(Fh, rhs)) relationViolations++;
        }
      }
      const isSettled = bijective && relationViolations === 0;
      if (isSettled) settledCount++;
      if (isSettled !== sd.settled) errors.push(`settled mismatch for m=${m}: claimed=${sd.settled} observed=${isSettled} (bijective=${bijective}, cayley_relation_violations=${relationViolations})`);
      detail.push({ m, settled: isSettled, bijective, relation_violations: relationViolations });
    }
    const isolatedObserved = detail.length > 0 && settledCount === detail.length;
    settledObserved = { settled_count: settledCount, total: detail.length, isolated: isolatedObserved, method: 'full Cayley-graph relation check (all |G|x4 edges), not just BFS spanning-tree representatives', detail };
    if (cert.settled_count !== settledCount) errors.push(`settled_count claimed=${cert.settled_count} observed=${settledCount}`);
    if (cert.settled_total !== detail.length) errors.push(`settled_total claimed=${cert.settled_total} observed=${detail.length}`);
    if (cert.isolated !== isolatedObserved) errors.push(`isolated claimed=${cert.isolated} observed=${isolatedObserved}`);
  }

  // ---- kernel_certificate (falsifier 監査「事後デルタ」重大指摘への対応): 数値の重複+文章では
  // なく、実際に N を定義する generator_images を独立に parse し、この照合器が独自に構築した
  // (G,X,Y) と一致するかを直接検証する。加えて claimed generation_verified/pb3_kernel_index/
  // b3_kernel_index も独立再計算して突き合わせる -- kernel_certificate という名のフィールドを
  // 実際に読み検査する、初めてのロジック(旧実装では node 側は当フィールドを一切参照していなかった)。
  let kernelCertObserved = null;
  if (cert.kernel_certificate) {
    const kc = cert.kernel_certificate;
    let parsedX = null, parsedY = null, parseErr = null;
    try {
      if (windowId.startsWith('C8_matrix') || windowId.startsWith('C10_matrix') || windowId.startsWith('C16_matrix')) {
        parsedX = parseGeneratorImageMatrix(kc.generator_images.x, G.L);
        parsedY = parseGeneratorImageMatrix(kc.generator_images.y, G.L);
      } else if (windowId === 'C8_D4cubed') {
        parsedX = parseGeneratorImageDnTriple(kc.generator_images.x, 4);
        parsedY = parseGeneratorImageDnTriple(kc.generator_images.y, 4);
      } else if (windowId === 'K8_MakeGn8') {
        parsedX = parseGeneratorImageDnTriple(kc.generator_images.x, 8);
        parsedY = parseGeneratorImageDnTriple(kc.generator_images.y, 8);
      } else if (windowId === 'C10_A5_permutation') {
        parsedX = parseGapPermString(kc.generator_images.x, 5);
        parsedY = parseGapPermString(kc.generator_images.y, 5);
      } else {
        parseErr = `no generator_images parser registered for window_id ${windowId}`;
      }
    } catch (e) { parseErr = String(e); }
    if (parseErr) {
      errors.push(`kernel_certificate.generator_images parse failed: ${parseErr}`);
    } else {
      const imagesMatchIndependentBuild = G.eq(parsedX, X) && G.eq(parsedY, Y);
      if (!imagesMatchIndependentBuild) errors.push('kernel_certificate.generator_images do NOT match this checker\'s independently-built generators');
      const genMapFromCert = subgroupClosure(G, [parsedX, parsedY]);
      const generationVerifiedObserved = genMapFromCert.size === pb3Index;
      if (!generationVerifiedObserved) errors.push(`kernel_certificate generators only generate a subgroup of size ${genMapFromCert.size}, not the full claimed pb3_index=${pb3Index}`);
      if (kc.verification && kc.verification.generation_verified !== generationVerifiedObserved) errors.push(`kernel_certificate.verification.generation_verified claimed=${kc.verification.generation_verified} observed=${generationVerifiedObserved}`);
      if (kc.pb3_kernel_index !== pb3Index) errors.push(`kernel_certificate.pb3_kernel_index claimed=${kc.pb3_kernel_index} observed=${pb3Index}`);
      if (kc.b3_kernel_index !== 6 * pb3Index) errors.push(`kernel_certificate.b3_kernel_index claimed=${kc.b3_kernel_index} observed=${6 * pb3Index}`);
      kernelCertObserved = { generator_images_match: imagesMatchIndependentBuild, generation_verified: generationVerifiedObserved, pb3_kernel_index: pb3Index, b3_kernel_index: 6 * pb3Index };
    }
  } else {
    errors.push('kernel_certificate field missing');
  }

  const ok = errors.length === 0;
  return { ok, errors, observed: { pb3_index: pb3Index, b3_points: b3Points, n_ord: nOrd, charming_set: charmingSet, derived_order: derivedOrder, candidate_total: candidateTotal, hexagon_free_certificate: { candidate_total: observed.candidate_total, h10_fail: observed.h10_fail, h11_fail: observed.h11_fail, generation_fail: observed.generation_fail, shadow_total: observed.shadow_total }, settled: settledObserved, kernel_certificate: kernelCertObserved }, G, X, Y, genMap, shadows: observed.shadows };
}

function orderOf(G, g) { let k = 1, p = g; while (!G.eq(p, G.id)) { p = G.mul(p, g); k++; } return k; }
function lcm(a, b) { return Math.abs(a * b) / gcd(a, b); }

// ================= calibration 1: marked factor map bijection (own re-derivation, NOT reusing
// GAP's GroupHomomorphismByImages result -- build the map by evaluating the SAME word in BOTH
// groups and checking it is injective+surjective+shadow-preserving) =================
function checkMarkedBijection(res1, res2) {
  // build BFS word list of G1 (from res1.genMap via bfsWords already done inside enumerateReducedHexagon,
  // but we need the word for EVERY element of G1, not just derived-subgroup ones)
  const { wordOf, elements } = bfsWords(res1.G, res1.X, res1.Y);
  const imageSet = new Map();
  let injective = true;
  for (const elt of elements) {
    const word = wordOf.get(res1.G.key(elt));
    const img = evalWordPrepend(res2.G, res2.X, res2.Y, word);
    const k = res2.G.key(img);
    if (imageSet.has(k)) injective = false;
    imageSet.set(k, true);
  }
  const genMap2 = subgroupClosure(res2.G, [res2.X, res2.Y]);
  const surjective = imageSet.size === genMap2.size;
  const sizesMatch = res1.genMap.size === genMap2.size;
  // shadow-preservation: for each shadow (m,f) of G1, phi(f) (evaluated via its word) should be a
  // shadow (m, phi(f)) actually present in G2's own shadow list.
  let shadowMatched = 0;
  const g2ShadowKeys = new Set(res2.shadows.map((s) => `${s.m}|${res2.G.key(s.f)}`));
  for (const sh of res1.shadows) {
    const img = evalWordPrepend(res2.G, res2.X, res2.Y, sh.word);
    if (g2ShadowKeys.has(`${sh.m}|${res2.G.key(img)}`)) shadowMatched++;
  }
  const shadowsOk = shadowMatched === res1.shadows.length && res1.shadows.length === res2.shadows.length;
  const ok = sizesMatch && injective && surjective && shadowsOk;
  return { ok, sizesMatch, injective, surjective, shadowMatched, shadow1_count: res1.shadows.length, shadow2_count: res2.shadows.length };
}

// ================= negative-fixture self-test (F5/F6 style 偽陽性検出器): corrupt a KNOWN-GOOD
// certificate's shadow_total and confirm checkCert correctly reports FAIL =================
function selfTestCorruption(goodCert) {
  const corrupted = JSON.parse(JSON.stringify(goodCert));
  corrupted.hexagon_free_certificate.shadow_total = corrupted.hexagon_free_certificate.shadow_total + 1;
  const verdict = checkCert(corrupted);
  return { ok: verdict.ok === false, note: 'corrupted shadow_total must be REJECTED', verdict_ok: verdict.ok };
}

function main() {
  if (!existsSync(VERDICT_DIR)) mkdirSync(VERDICT_DIR, { recursive: true });
  if (!existsSync(CERT_DIR)) { console.log(`no certificate dir: ${CERT_DIR}`); process.exitCode = 1; return; }

  const files = {
    C8_matrix_mod8: 'C8.matrix.v1.json',
    C8_D4cubed: 'C8.d4cubed.v1.json',
    C10_matrix_mod10: 'C10.matrix.v1.json',
    C10_A5_permutation: 'C10.a5permutation.v1.json',
    C8_matrix_WRONG_LEVEL6_fixture: 'C8.matrix.v1.WRONG_LEVEL6_fixture.json',
    C8_matrix_mod8_Ybar_signflip_BONUS: 'C8.matrix.v1.Ybar_signflip_BONUS.json',
    C16_matrix_mod16: 'C16.matrix.v1.json',       // target window -- may not exist while FIRE-locked
    K8_MakeGn8: 'K8.dncubed.v1.json',             // target window -- may not exist while FIRE-locked
  };

  const certs = {};
  const results = {};
  for (const [id, fname] of Object.entries(files)) {
    const p = join(CERT_DIR, fname);
    if (!existsSync(p)) { console.log(`[skip] ${id}: certificate not found (${fname}) -- expected while FIRE-locked for target windows`); continue; }
    const cert = JSON.parse(readFileSync(p, 'utf8'));
    certs[id] = cert;
    const verdict = checkCert(cert);
    results[id] = verdict;
    writeFileSync(join(VERDICT_DIR, `${id}.twincell.verdict.json`), JSON.stringify(verdict, null, 2));
    console.log(`window ${id} [self-consistency of this certificate]: ${verdict.ok ? 'PASS' : 'FAIL'}${verdict.errors.length ? '  -- ' + verdict.errors.join('; ') : ''}`);
  }

  // ---- Calibration 1: C8 marked factor map bijection (matrix-mod-8 <-> D4^3) ----
  let calib1 = { ok: false, reason: 'missing certs' };
  if (results.C8_matrix_mod8 && results.C8_D4cubed) {
    calib1 = checkMarkedBijection(results.C8_matrix_mod8.observed ? results.C8_matrix_mod8 : results.C8_matrix_mod8, results.C8_D4cubed);
    // (observed group/shadows are attached on the verdict object itself, see checkCert return)
    calib1 = checkMarkedBijection(results.C8_matrix_mod8, results.C8_D4cubed);
  }
  const calib1KnownValue = results.C8_matrix_mod8 && results.C8_D4cubed
    && results.C8_matrix_mod8.observed.hexagon_free_certificate.shadow_total === 4
    && results.C8_D4cubed.observed.hexagon_free_certificate.shadow_total === 4;
  console.log(`\n[${calib1.ok ? 'PASS' : 'FAIL'}] CALIBRATION 1 (marked factor map bijection, C8 matrix-mod-8 <-> D4^3): ${JSON.stringify(calib1)}`);
  console.log(`[${calib1KnownValue ? 'PASS' : 'FAIL'}] CALIBRATION 1 known value (|GT|=4 both sides)`);

  // ---- Calibration 2: C10 known value |GT|=20 + marked factor map bijection vs A5 permutation
  // construction (falsifier 監査 §2 要修正への対応 -- 数値一致だけで済ませない) + A5-CONV
  // (falsifier 軽微指摘6への対応 -- twincell 固有の構成に対する専用実行) ----
  const calib2KnownValue = results.C10_matrix_mod10 && results.C10_matrix_mod10.observed.hexagon_free_certificate.shadow_total === 20;
  console.log(`[${calib2KnownValue ? 'PASS' : 'FAIL'}] CALIBRATION 2 known value (C10 matrix-mod-10 |GT|=20)`);
  let calib2Bij = { ok: false, reason: 'missing certs' };
  let a5ConvResult = { ok: false, reason: 'missing certs' };
  if (results.C10_matrix_mod10 && results.C10_A5_permutation) {
    calib2Bij = checkMarkedBijection(results.C10_matrix_mod10, results.C10_A5_permutation);
    a5ConvResult = checkA5ConvViaBijection(results.C10_matrix_mod10, results.C10_A5_permutation);
  }
  console.log(`[${calib2Bij.ok ? 'PASS' : 'FAIL'}] CALIBRATION 2 (marked factor map bijection, C10 matrix-mod-10 <-> A5 permutation): ${JSON.stringify(calib2Bij)}`);
  console.log(`[${a5ConvResult.ok ? 'PASS' : 'FAIL'}] A5-CONV (twincell 固有, transported via C10-matrix<->A5 word bijection): observed=${a5ConvResult.observed} target=${a5ConvResult.target}`);
  const calib2Ok = calib2KnownValue && calib2Bij.ok && a5ConvResult.ok;
  console.log(`[${calib2Ok ? 'PASS' : 'FAIL'}] CALIBRATION 2 overall`);

  // ---- Calibration 3: K^(8) known value |GT|=16 (Thm 4.3/5.3, alpha=3) -- only if the target
  // window certificate exists (i.e. FIRE unlocked and the main sweep has run). While locked, this
  // reports status=LOCKED (not a silent skip, not a false PASS) -- falsifier 監査 §3b 重大指摘 ----
  let calib3 = { status: 'LOCKED', known_value_ok: null };
  if (results.K8_MakeGn8) {
    const observedShadowTotal = results.K8_MakeGn8.observed.hexagon_free_certificate.shadow_total;
    calib3 = { status: 'RAN', known_value_ok: observedShadowTotal === 16, observed_shadow_total: observedShadowTotal, expected: 16 };
    console.log(`[${calib3.known_value_ok ? 'PASS' : 'FAIL'}] CALIBRATION 3 (K^(8) known value |GT|=16, Thm 4.3/5.3 alpha=3): observed=${observedShadowTotal}`);
  } else {
    console.log('[LOCKED] CALIBRATION 3 (K^(8) known value |GT|=16) -- target window certificate not found, NOT a PASS');
  }

  // ---- Negative fixture (mistaken level L=6): must NOT match known value / must NOT biject with D4^3 ----
  let negFixtureOk = null;
  if (results.C8_matrix_WRONG_LEVEL6_fixture && results.C8_D4cubed) {
    const calibBad = checkMarkedBijection(results.C8_matrix_WRONG_LEVEL6_fixture, results.C8_D4cubed);
    negFixtureOk = (!calibBad.ok) || (results.C8_matrix_WRONG_LEVEL6_fixture.observed.hexagon_free_certificate.shadow_total !== 4);
    console.log(`[${negFixtureOk ? 'PASS' : 'FAIL'}] NEGATIVE FIXTURE (wrong level L=6) correctly rejected: bijection_ok=${calibBad.ok}, shadow_total=${results.C8_matrix_WRONG_LEVEL6_fixture.observed.hexagon_free_certificate.shadow_total}`);
  }

  // ---- Self-test: corrupted-certificate detector (F5/F6 style 偽陽性検出器) ----
  let selfTest = null;
  if (certs.C8_matrix_mod8) {
    selfTest = selfTestCorruption(certs.C8_matrix_mod8);
    console.log(`[${selfTest.ok ? 'PASS' : 'FAIL'}] SELF-TEST: corrupted certificate (shadow_total+1) is correctly REJECTED by this checker`);
  }

  const perCertOk = Object.values(results).every((r) => r.ok);
  const calib3Blocking = calib3.status === 'RAN' ? calib3.known_value_ok : true; // LOCKED does not fail the gate, a RAN mismatch does
  const allOk = perCertOk && calib1.ok && calib1KnownValue && calib2Ok && calib3Blocking
    && (negFixtureOk === null || negFixtureOk) && (selfTest === null || selfTest.ok);
  writeFileSync(join(VERDICT_DIR, 'twincell.calibration.verdict.json'), JSON.stringify({
    per_cert_ok: perCertOk, calibration_1: { ...calib1, known_value_ok: calib1KnownValue },
    calibration_2: { known_value_ok: calib2KnownValue, bijection: calib2Bij, a5_conv: a5ConvResult, ok: calib2Ok },
    calibration_3: calib3,
    negative_fixture: { ok: negFixtureOk }, self_test_corruption: selfTest, all_ok: allOk,
  }, null, 2));
  console.log(`\ncheck-twincell.mjs overall: ${allOk ? 'all_pass' : 'FAIL'}`);
  if (!allOk) process.exitCode = 1;
}

main();
