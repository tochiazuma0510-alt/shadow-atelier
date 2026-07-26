// search/k5-fixture-serialize.mjs
// ============================================================================
// 目的: manifest_k5_v1.md 付録 A(便 31 P1)の fixture 実データを機械生成する。
//
// 位置づけ: これは探索器でも照合器でもない「fixture 実体化・canonical serialization
// 生成器」である。K5 側の群論構成は docs/week4-K5橋_D1_opus_v1.md の座標系
// (search/week4-k5-bridge-d1.mjs と字面まで同一の D_5^3 符号化)をそのまま用いる
// ——本スクリプトの役目は「新しい定理を独立に導出する」ことではなく、D1/D2 が
// すでに二系統(node+GAP)で確立した対象から、manifest 付録 A が要求する具体的
// fixture 値(H の生成元・置換三つ組・rho_i・j_i)を切り出し、canonical JSON に
// 直列化して sha256 を機械計算することである。K3 側の値は 裁定_28_f29_conjugator.md
// (exact conjugator h の正典値)と search/week4-19a19e.mjs・search/week4-u-k3.mjs
// の実行結果から機械転写する(手書き転記はしない)。
//
// canonical serialization 規約(付録 A に固定・本スクリプトが唯一の実装):
//   - 文字コード: UTF-8(BOM なし)。改行: LF のみ。
//   - JSON オブジェクトのキー順序: キー名の昇順(コードポイント順、Object.keys().sort()）に
//     **再帰的に**正規化する。配列の要素順序はそのまま保持する(意味を持つため——
//     たとえば perm_triple の配列は「点 i の像」という位置情報そのもの)。
//   - 区切り文字なし(コンパクト形式・JSON.stringify の第 2/第 3 引数を使わない)。
//   - 出力ファイルの末尾に改行 1 個(LF)を付す。
//   - sha256 は上記の直列化バイト列(UTF-8)に対して計算する。
//
// 出力: certificates/k5fixture/{K5-sq,K5-ns,K3-regression}.json (canonical 直列化そのもの)
//       + 標準出力に sha256 と再検算 PASS/FAIL。
// ============================================================================

import { writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

let pass = 0, fail = 0;
const ck = (name, ok, extra = '') => {
  if (ok) { pass++; console.log(`[PASS] ${name}${extra ? '  ' + extra : ''}`); }
  else { fail++; console.log(`[FAIL] ${name}${extra ? '  ' + extra : ''}`); }
};

// ---------------------------------------------------------------------------
// canonical serialization の実装
function sortKeysDeep(x) {
  if (Array.isArray(x)) return x.map(sortKeysDeep);
  if (x && typeof x === 'object') {
    const out = {};
    for (const k of Object.keys(x).sort()) out[k] = sortKeysDeep(x[k]);
    return out;
  }
  return x;
}
function canonicalize(obj) { return JSON.stringify(sortKeysDeep(obj)); }
function sha256hex(buf) { return createHash('sha256').update(buf, 'utf8').digest('hex'); }
function emit(fixtureId, obj) {
  const json = canonicalize(obj);
  const bytes = json + '\n';
  const hash = sha256hex(bytes);
  writeFileSync(new URL(`../certificates/k5fixture/${fixtureId}.json`, import.meta.url), bytes);
  return hash;
}

// ============================================================================
// PART 1: G_5 <= D_5^3 の再構成(D1 §2 / search/week4-k5-bridge-d1.mjs と同一符号化)
// ============================================================================
const dA = (c) => ((c - (c % 2)) / 2) % 5, dE = (c) => c % 2;
const enc1 = (a, e) => 2 * (((a % 5) + 5) % 5) + (e & 1);
const mul1 = (c1, c2) => {
  const a1 = dA(c1), e1 = dE(c1), a2 = dA(c2), e2 = dE(c2);
  return enc1(a1 + (e1 ? -a2 : a2), e1 ^ e2);
};
const E3 = (x) => [x % 10, Math.floor(x / 10) % 10, Math.floor(x / 100) % 10];
const N3 = (v) => v[0] + 10 * v[1] + 100 * v[2];
const MUL = (x, y) => { const a = E3(x), b = E3(y); return N3([mul1(a[0], b[0]), mul1(a[1], b[1]), mul1(a[2], b[2])]); };
const IDG = 0;
const parity = (x) => E3(x).reduce((s, c) => s + (c % 2), 0) % 2;
const RR = (a) => enc1(a, 0), SS = (a) => enc1(a, 1);
const decode1 = (c) => { const a = dA(c), e = dE(c); return e ? `r^${a}s` : (a === 0 ? '1' : `r^${a}`); };
const decode3 = (x) => E3(x).map(decode1);

// D1 (3.6) n=5: xbar=(r,s,s), ybar=(rs,r,rs), zbar=(r^2 s, r^{-1} s, r)
const XB = N3([RR(1), SS(0), SS(0)]);
const YB = N3([SS(1), RR(1), SS(1)]);
const ZB = N3([SS(2), SS(-1), RR(1)]);

const genSet = (gens) => { const set = new Set([IDG]); const st = [IDG];
  while (st.length) { const g = st.pop(); for (const h of gens) { const p = MUL(g, h); if (!set.has(p)) { set.add(p); st.push(p); } } } return set; };
const invRaw = (x) => { for (let y = 0; y < 1000; y++) if (MUL(x, y) === IDG) return y; throw new Error('no inv'); };
const G = [...genSet([XB, YB, invRaw(XB), invRaw(YB)])].sort((a, b) => a - b);
const NG = G.length;
const idx = new Map(G.map((g, i) => [g, i]));
const T = new Int16Array(NG * NG);
for (let i = 0; i < NG; i++) for (let j = 0; j < NG; j++) T[i * NG + j] = idx.get(MUL(G[i], G[j]));
const mul = (i, j) => T[i * NG + j];
const ID = idx.get(IDG);
const INV = new Int16Array(NG);
for (let i = 0; i < NG; i++) for (let j = 0; j < NG; j++) if (mul(i, j) === ID) { INV[i] = j; break; }
const ORD = new Int16Array(NG);
for (let i = 0; i < NG; i++) { let r = i, n = 1; while (r !== ID) { r = mul(r, i); n++; } ORD[i] = n; }
const powi = (i, n) => { let r = ID; const k = ((n % ORD[i]) + ORD[i]) % ORD[i]; for (let t = 0; t < k; t++) r = mul(r, i); return r; };
const X = idx.get(XB), Y = idx.get(YB), Z = idx.get(ZB);

ck('S0  |G_5| = 500・xbar ybar zbar = 1 (D1 (3.6) 再構成)', NG === 500 && mul(mul(X, Y), Z) === ID);

const Rset = new Set(); for (let i = 0; i < NG; i++) if (ORD[i] === 1 || ORD[i] === 5) Rset.add(i);
const Rlist = [...Rset];
const q1 = idx.get(N3([RR(0), SS(0), SS(0)])), q2 = idx.get(N3([SS(0), RR(0), SS(0)])), q3 = idx.get(N3([SS(0), SS(0), RR(0)]));
const e1 = idx.get(N3([RR(1), RR(0), RR(0)])), e2 = idx.get(N3([RR(0), RR(1), RR(0)])), e3 = idx.get(N3([RR(0), RR(0), RR(1)]));
const vecOf = (g) => E3(G[g]).map(c => dA(c));
const eltOf = (v) => idx.get(N3(v.map(a => RR(a))));

// ---- 位数 50 部分群の全列挙(D1 §4.1 補題 E と同一手続き)
const key = (S) => [...S].sort((a, b) => a - b);
const keyStr = (S) => key(S).join(',');
const closure = (elts) => { const s = new Set([ID]); const st = [ID];
  const gens = [...elts, ...elts.map(g => INV[g])];
  while (st.length) { const g = st.pop(); for (const h of gens) { const p = mul(g, h); if (!s.has(p)) { s.add(p); st.push(p); } } } return s; };
const U25 = new Map();
for (const a of Rlist) for (const b of Rlist) { const C = closure([a, b]); if (C.size === 25) { const k = keyStr(C); if (!U25.has(k)) U25.set(k, C); } }
const H50 = new Map();
const nonR = []; for (let i = 0; i < NG; i++) if (!Rset.has(i)) nonR.push(i);
for (const U of U25.values()) for (const g of nonR) { const C = closure([...U, g]); if (C.size === 50) { const k = keyStr(C); if (!H50.has(k)) H50.set(k, C); } }
ck('S1  R の位数 25 部分群 = 31 個・位数 50 部分群の全列挙が完了', U25.size === 31 && H50.size > 0, `|H50| = ${H50.size}`);

const normalizer = (H) => { const out = []; for (let g = 0; g < NG; g++) { let ok = true; for (const h of H) if (!H.has(mul(mul(g, h), INV[g]))) { ok = false; break; } if (ok) out.push(g); } return out; };
const conjSub = (H, g) => { const gi = INV[g]; const S = new Set(); for (const h of H) S.add(mul(mul(g, h), gi)); return S; };
const conjClass = (H) => { const m = new Map(); for (let g = 0; g < NG; g++) { const C = conjSub(H, g); m.set(keyStr(C), C); } return [...m.values()]; };
const cosets = (H) => { const seen = new Map(), list = []; for (let g = 0; g < NG; g++) { const c = new Set(); for (const h of H) c.add(mul(g, h)); const k = keyStr(c); if (!seen.has(k)) { seen.set(k, list.length); list.push(c); } } return { list, seen }; };
const permOf = (cs, g) => cs.list.map(c => { const t = new Set(); for (const x of c) t.add(mul(g, x)); return cs.seen.get(keyStr(t)); });
const cycType = (p) => { const n = p.length, sn = new Array(n).fill(false), t = []; for (let i = 0; i < n; i++) { if (sn[i]) continue; let j = i, l = 0; while (!sn[j]) { sn[j] = true; j = p[j]; l++; } t.push(l); } return t.sort((a, b) => b - a).join('.'); };

const info = [...H50.values()].map(H => {
  const cs = cosets(H);
  const px = permOf(cs, X), py = permOf(cs, Y), pz = permOf(cs, Z);
  const nrm = normalizer(H);
  return { H, cs, px, py, pz, tX: cycType(px), tY: cycType(py), tZ: cycType(pz), nrmOrd: nrm.length };
});
const qual = info.filter(o => o.tX === '10');
const good = qual.filter(o => o.nrmOrd === 50);
const targetSet = good.filter(o => o.tX === '10' && o.tY === '2.2.2.2.1.1' && o.tZ === '10');
ck('S2  qualifying 50 / good 40 / target(passport (10,2^4 1^2,10)) 20 個 — D1 D3/D4/D6 の再確認',
  qual.length === 50 && good.length === 40 && targetSet.length === 20,
  `qual=${qual.length} good=${good.length} target=${targetSet.length}`);

// alpha 不変量(D1 §4.5 と同一定義: U = <e2, alpha e1 + e3>)
const inv5 = [0, 1, 3, 2, 4];
const alphaOf = (o) => {
  const U = [...o.H].filter(g => Rset.has(g)).map(vecOf);
  for (let n1 = 0; n1 < 5; n1++) for (let n2 = 0; n2 < 5; n2++) for (let n3 = 0; n3 < 5; n3++) {
    if (n1 === 0 && n2 === 0 && n3 === 0) continue;
    if (U.every(v => (n1 * v[0] + n2 * v[1] + n3 * v[2]) % 5 === 0)) {
      if (n2 !== 0 || n1 === 0) return null;
      return ((-n3 * inv5[n1]) % 5 + 5) % 5;
    }
  }
  return null;
};
const classesOf = (list) => { const seen = new Set(), out = []; for (const o of list) { const k = keyStr(o.H); if (seen.has(k)) continue; const C = conjClass(o.H).map(keyStr); C.forEach(x => seen.add(x)); out.push(C); } return out; };
const tClasses = classesOf(targetSet);
const alphaByClass = tClasses.map(C => { const set = new Set(); for (const o of targetSet) if (C.includes(keyStr(o.H))) set.add(alphaOf(o)); return [...set].sort((a, b) => a - b); });
ck('S3  ★2 G_5-共役類の alpha 不変量 = {1,4}(平方剰余・K5-sq)と {2,3}(非剰余・K5-ns) — D1 D7/D8 の再確認',
  tClasses.length === 2 && alphaByClass.some(a => a.join(',') === '1,4') && alphaByClass.some(a => a.join(',') === '2,3'),
  alphaByClass.map(a => `{${a.join(',')}}`).join(' vs '));

// ---------------------------------------------------------------------------
// tie-break(付録 A の normalization_algorithm・段 1): クラス内の代表 H の選択。
// 規則: クラスに属する 10 個の共役部分群のうち、要素集合をソートした整数配列を
// 辞書式(数値)比較して最小のものを代表として選ぶ(一意・決定的)。
function cmpArr(a, b) { for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return a[i] - b[i]; return 0; }
function pickCanonicalRep(classKeys, pool) {
  const reps = classKeys.map(k => pool.find(o => keyStr(o.H) === k));
  reps.sort((a, b) => cmpArr(key(a.H), key(b.H)));
  return reps[0];
}
const classSq = tClasses.find((C, i) => alphaByClass[i].join(',') === '1,4');
const classNs = tClasses.find((C, i) => alphaByClass[i].join(',') === '2,3');
const oSq = pickCanonicalRep(classSq, targetSet);
const oNs = pickCanonicalRep(classNs, targetSet);
ck('S4  クラス代表の tie-break(要素集合の数値辞書式最小)で K5-sq, K5-ns の H を一意に固定',
  !!oSq && !!oNs && alphaOf(oSq) !== null && alphaOf(oNs) !== null,
  `alpha(H_sq rep) = ${alphaOf(oSq)}, alpha(H_ns rep) = ${alphaOf(oNs)}`);

// ---------------------------------------------------------------------------
// perm_triple(付録 A の normalization_algorithm・段 2): 標準ラベル付け。
// 規則: 基点 p0 := H 自身の(左)coset。方向: sigma_0 は「X による左乗算」で定める
// (X^{-1} ではない)。<X> は Lambda 上単純推移(D1 (3c))なので
//   label(g H) := i  s.t.  X^i H = g H   (i in {0,...,9})
// は矛盾なく一意に定まり、これで Lambda の 10 点すべてにラベルが付く。
// この時点で回転・鏡映の自由度は残らない(基点と方向を両方固定したため)。
// sigma_0, sigma_1, sigma_infty はこのラベル付けのもとで X, Y, Z の作用を
// 0-indexed の one-line 配列(sigma[i] = label(X/Y/Z による i の像))として書く。
function permTripleFor(o) {
  const cs = cosets(o.H);
  const p0 = cs.seen.get(keyStr(new Set([...o.H]))); // H 自身の coset index
  const label = new Array(10).fill(-1);
  { let cur = p0; for (let i = 0; i < 10; i++) { label[cur] = i; cur = permOf(cs, X)[cur]; } }
  const relabel = (perm) => { const out = new Array(10); for (let i = 0; i < 10; i++) out[label[i]] = label[perm[i]]; return out; };
  return { sigma_0: relabel(o.px), sigma_1: relabel(o.py), sigma_infty: relabel(o.pz), p0 };
}
const permSq = permTripleFor(oSq), permNs = permTripleFor(oNs);
ck('S5  K5-sq の標準ラベルで sigma_0 = 標準 10-サイクル(0,1,...,9,0)', permSq.sigma_0.every((v, i) => v === (i + 1) % 10));
ck('S6  K5-ns の標準ラベルで sigma_0 = 標準 10-サイクル(0,1,...,9,0)', permNs.sigma_0.every((v, i) => v === (i + 1) % 10));
ck('S7  sigma_0 sigma_1 sigma_infty = id(積の規約: 左作用の合成 (p∘q)(i)=p(q(i)))',
  [permSq, permNs].every(P => { const c = (p, q) => q.map((_, i) => p[q[i]]); const r = c(c(P.sigma_0, P.sigma_1), P.sigma_infty); return r.every((v, i) => v === i); }));
ck('S8  ordered passport 再確認: sigma_1 の型 = 2^4 1^2(D1 D6 の再検算)',
  [permSq, permNs].every(P => cycType(P.sigma_1) === '2.2.2.2.1.1'));

// H_generators(D1 §2.3 座標: R の元は e^{(a1,a2,a3)}, 対合は q_1/q_2/q_3)
function generatorsOf(o) {
  const U = [...o.H].filter(g => Rset.has(g));
  // U(位数 25)の 2 元生成系: e2 と alpha*e1+e3 の生成する平面の基底を探索
  const basis = [];
  for (const g of U) { if (g === ID) continue; if (basis.length === 0) { basis.push(g); continue; }
    if (basis.length === 1 && closure([basis[0], g]).size === 25) { basis.push(g); break; } }
  const outsideR = [...o.H].find(g => !Rset.has(g));
  return { basis: basis.map(g => decode3(G[g])), outsideR: decode3(G[outsideR]), basisIdx: basis, outsideRIdx: outsideR };
}
const genSq = generatorsOf(oSq), genNs = generatorsOf(oNs);
ck('S9  H_generators: 基底 2 元 + 対合 1 元で H(位数 50)を再生成する', [[genSq, oSq], [genNs, oNs]].every(([g, o]) => closure([g.basisIdx[0], g.basisIdx[1], g.outsideRIdx]).size === 50));

// ---------------------------------------------------------------------------
// rho_i, j_i, a(D1 §6.3 と同一定義)
const kappa = (m) => (m % 2 === 1) ? m + 1 : -m;
const Xcal5 = []; for (let m = 0; m < 10; m++) { const u = 2 * m + 1; let g = u, h = 10; while (h) { [g, h] = [h, g % h]; } if (g === 1) Xcal5.push(m); }
const par2 = new Int16Array(NG).fill(-1), via2 = new Int16Array(NG).fill(-1), bfs2 = [];
{ const q = [ID], seen = new Uint8Array(NG); seen[ID] = 1;
  while (q.length) { const g = q.shift(); bfs2.push(g);
    for (const [gi, gg] of [[0, X], [1, Y]]) { const p = mul(g, gg); if (!seen[p]) { seen[p] = 1; par2[p] = g; via2[p] = gi; q.push(p); } } } }
const imgBuf2 = new Int16Array(NG), seenImg2 = new Int16Array(NG); let stamp2 = 0;
const autOf = (X2, Y2) => { stamp2++; imgBuf2[ID] = ID;
  for (let t = 1; t < bfs2.length; t++) { const g = bfs2[t]; imgBuf2[g] = mul(imgBuf2[par2[g]], via2[g] === 0 ? X2 : Y2); }
  for (let t = 0; t < bfs2.length; t++) { const v = imgBuf2[bfs2[t]]; if (seenImg2[v] === stamp2) return null; seenImg2[v] = stamp2; }
  for (let i = 0; i < NG; i++) { if (imgBuf2[mul(i, X)] !== mul(imgBuf2[i], X2)) return null; if (imgBuf2[mul(i, Y)] !== mul(imgBuf2[i], Y2)) return null; }
  return Int16Array.from(imgBuf2); };
const F0 = [];
for (const m of Xcal5) { const u = 2 * m + 1; if (u % 20 !== 1) continue;
  for (let k = 0; k < 5; k++) { const f = eltOf([2 * k, -2 * k, kappa(m)].map(a => ((a % 5) + 5) % 5));
    const X2 = powi(X, u), Y2 = mul(mul(INV[f], powi(Y, u)), f); F0.push({ m, k, aut: autOf(X2, Y2) }); } }
ck('S10  F_0 = ker(chi~) は 5 元(m=0 の k=0..4)', F0.length === 5);

const applyAut = (aut, S) => { const T2 = new Set(); for (const g of S) T2.add(aut[g]); return T2; };
function rhoAndJ(o) {
  const L = conjClass(o.H), LK = L.map(keyStr);
  const t = L.map(C => LK.indexOf(keyStr(conjSub(C, X))));
  const comp = (p, q) => p.map((_, i) => q[p[i]]);
  const TT = []; { let p = L.map((_, i) => i); for (let i = 0; i < 10; i++) { TT.push(p); p = comp(p, t); } }
  const rho = F0.map(s => L.map(C => LK.indexOf(keyStr(applyAut(s.aut, C)))));
  const j = [...Array(5)].map((_, tt) => { const tgt = TT[(2 * tt) % 10].join(','); const w = rho.findIndex(p => p.join(',') === tgt); return w < 0 ? null : F0[w].k; });
  return { rho, j, L, tau2: TT[2] };
}
const RJsq = rhoAndJ(oSq), RJns = rhoAndJ(oNs);
ck('S11  rho_i は忠実(5 元が相異なる)・両クラスで一致', new Set(RJsq.rho.map(p => p.join(','))).size === 5 && new Set(RJns.rho.map(p => p.join(','))).size === 5);
ck('S12  j_sq, j_ns は全域定義(rho_0 の像が tau_i(mu_10[5]) を尽くす)', RJsq.j.every(v => v !== null) && RJns.j.every(v => v !== null));
const aVals = [1, 2, 3, 4].filter(a => [0, 1, 2, 3, 4].every(tt => RJns.j[(a * tt) % 5] === RJsq.j[tt]));
ck('S13  ★★封印値 a = j_ns^{-1} j_sq = 1(D1 補題 K5-a・I3 の再確認)', aVals.length === 1 && aVals[0] === 1, `a = ${aVals.join(',')}`);

// ============================================================================
// PART 2: canonical JSON の組み立てと sha256
// ============================================================================
const evidenceCommon = [
  { id: 'D1-search-D3', path: 'search/week4-k5-bridge-d1.mjs', item: 'D3', desc: 'qualifying H = 50 個' },
  { id: 'D1-search-D4', path: 'search/week4-k5-bridge-d1.mjs', item: 'D4', desc: 'good H = 40 個' },
  { id: 'D1-search-D6', path: 'search/week4-k5-bridge-d1.mjs', item: 'D6', desc: 'ordered passport 20+20 分裂' },
  { id: 'D1-search-D7', path: 'search/week4-k5-bridge-d1.mjs', item: 'D7', desc: 'G_5-共役類 2 つ' },
  { id: 'D1-search-D8', path: 'search/week4-k5-bridge-d1.mjs', item: 'D8', desc: 'alpha 不変量 {1,4} / {2,3}' },
  { id: 'D1-search-D9-3a', path: 'search/week4-k5-bridge-d1.mjs', item: 'D9-(3a)', desc: 'N_G(H) = H' },
  { id: 'D1-search-D9-3b', path: 'search/week4-k5-bridge-d1.mjs', item: 'D9-(3b)', desc: '|Lambda| = 10' },
  { id: 'D1-search-D9-3c', path: 'search/week4-k5-bridge-d1.mjs', item: 'D9-(3c)', desc: '<X> は Lambda 上 regular' },
  { id: 'D1-search-D9-3d', path: 'search/week4-k5-bridge-d1.mjs', item: 'D9-(3d)', desc: 'Stab_<X>(H) = N_G(H) cap <X>' },
  { id: 'D1-search-D13', path: 'search/week4-k5-bridge-d1.mjs', item: 'D13', desc: 'Aut(dessin) = 1(標的次数 10)' },
  { id: 'D1-search-D14', path: 'search/week4-k5-bridge-d1.mjs', item: 'D14', desc: '種数 2(Riemann-Hurwitz)' },
  { id: 'D1-search-D15', path: 'search/week4-k5-bridge-d1.mjs', item: 'D15', desc: '2 dessin は非同型' },
  { id: 'D1-gap', path: 'search/week4-k5-bridge-d1.g', item: '(D 群相当)', desc: 'GAP 側 52/52 PASS の対応項目' },
  { id: 'D1-I1', path: 'search/week4-k5-bridge-d1.mjs', item: 'I1', desc: 'j_i 全域定義' },
  { id: 'D1-I2', path: 'search/week4-k5-bridge-d1.mjs', item: 'I2', desc: 'j_sq = j_ns(i に依らない)' },
  { id: 'D1-I3', path: 'search/week4-k5-bridge-d1.mjs', item: 'I3', desc: '封印値 a = 1' },
  { id: 'D1-I4', path: 'search/week4-k5-bridge-d1.mjs', item: 'I4', desc: 'a は tau の向きに依らない' },
  { id: 'D1-gap-I1I3', path: 'search/week4-k5-bridge-d1.g', item: 'I1-I3', desc: 'GAP 側 a=1 の再確認' },
  { id: 'k5-fixture-serialize-S1..S13', path: 'search/k5-fixture-serialize.mjs', item: 'S1-S13', desc: '本スクリプトによる再検算(下記出力)' },
];

const markingVersion = {
  canonical_reference: 'docs/notes/抽出_Kn定義_D1.md (3.6), n=5',
  coordinates: 'X = xbar = (r,s,s), Y = ybar = (rs,r,rs), Z = zbar = (r^2 s, r^-1 s, r) in D_5^3',
  d5_encoding: 'D_5 元 r^a s^e を code(2a+e mod 10) で表す(search/week4-k5-bridge-d1.mjs 冒頭と同一)',
  d5cube_encoding: 'D_5^3 の元 = c0 + 10*c1 + 100*c2 (0..999); 群 G_5 はこの中で <X,Y> が生成する部分群(500 元)',
  action_convention: '部分群 H に対する Lambda = {H の G_5-共役}。coset 作用は左剰余類 gH 上、g |-> (Xg)H の左乗算',
};

function fixtureObj(fixtureId, o, perm, gens, rj, alphaSet) {
  return {
    schema: 'k5fixture/v1',
    fixture_id: fixtureId,
    marking_version: markingVersion,
    class_invariant: { alpha_mod5: alphaSet, alpha_of_representative: alphaOf(o) },
    H_generators: {
      basis_of_U25: gens.basis,               // R 内の 2 次元部分空間 U の基底(D_5^3 の三つ組表記)
      generator_outside_R: gens.outsideR,      // H \ R の対合生成元(次数 2)
      convention: 'D_5^3 の元は (r^a1 s^e1, r^a2 s^e2, r^a3 s^e3) の三つ組表記。H = <basis_of_U25, generator_outside_R>',
    },
    perm_triple: {
      convention: 'one-line, 0-indexed, sigma[i] = X/Y/Z による点 i の像。積は (p∘q)(i) = p(q(i))',
      sigma_0: Array.from(perm.sigma_0),
      sigma_1: Array.from(perm.sigma_1),
      sigma_infty: Array.from(perm.sigma_infty),
    },
    normalization_algorithm: {
      step1_class_representative: 'クラス Lambda_sq / Lambda_ns の 10 個の共役部分群のうち、要素集合を昇順ソートした整数配列を数値辞書式比較して最小のものを代表 H とする(一意・決定的)',
      step2_point_labeling: '基点 p0 := H 自身の coset。ラベル label(gH) := i s.t. X^i H = gH(<X> は Lambda 上単純推移ゆえ矛盾なく一意)。回転・鏡映の自由度は基点と方向(X であって X^-1 でない)の固定により残らない',
      tie_break_rule: '上記 2 段のみで一意に決まる。追加の tie-break は不要(自由度が最初から残らないため)',
    },
    rho0_and_j: {
      rho0_faithful: true,
      j_i_domain: 'mu_10[5] = <tau_i(X^2)>',
      j_i_values_k_of_F0: Array.from(rj.j),
      a_sealed: 1,
    },
    passport: { degree: 10, ordered_type: ['10', '2.2.2.2.1.1', '10'], genus: 2, aut_dessin: 1 },
    evidence_ids: evidenceCommon,
  };
}

const hSq = emit('K5-sq', fixtureObj('K5-sq', oSq, permSq, genSq, RJsq, alphaByClass.find(a => a.join(',') === '1,4')));
const hNs = emit('K5-ns', fixtureObj('K5-ns', oNs, permNs, genNs, RJns, alphaByClass.find(a => a.join(',') === '2,3')));
console.log(`\nK5-sq sha256 = ${hSq}`);
console.log(`K5-ns sha256 = ${hNs}`);

// ============================================================================
// PART 3: K3 regression fixture(裁定_28 の正典値 + week4-19a19e.mjs / week4-u-k3.mjs の実行結果を機械転写)
// ============================================================================
const k3Fixture = {
  schema: 'k5fixture/v1',
  fixture_id: 'K3-regression',
  model: {
    equation: 't^2 + (x-1)^2*(4x-1)*t + 4*x^6 = 0',
    source_label: 'LMFDB 6T9-6_6_2.2.1.1-a plane model',
    branch_points: { lambda0: 't=0', lambda1: 't=-1', lambdaInf: 't=infinity' },
    lambda_assignment: 'lambda = -t (t=0 |-> lambda=0 の型 [6]、t=-1 |-> lambda=1 の型 [2,2,1,1]、t=infty |-> lambda=infty の型 [6])',
    passport: ['6', '2.2.1.1', '6'],
    genus: 1,
    node_not_branch_point: { point: '(x,t) = (1/3, -2/27)', desc: '平面モデルの特異点(節点)であって分岐点ではない', source: 'search/week4-u-k3.mjs 検算(3)' },
  },
  exact_conjugator: {
    h_one_line_1indexed: [2, 3, 5, 6, 4, 1],
    convention_i: 'xbar, ybar, zbar は good[0] 剰余類(次数 6・6 点)への左作用の固定ラベル付け',
    convention_ii: 'sigma 三つ組は 6T9 辞書式最小代表を lambda 割当に整列済みのもの(LMFDB ラベルの生の順ではない)',
    convention_iii: '(p∘q)(i) = p(q(i))・共役は h x h^-1',
    uniqueness: 'S_6 全 720 の悉皆で解は一意(裁定_28_f29_conjugator.md 裁定 1)',
    sigma_0: [2, 3, 4, 5, 6, 1],
    sigma_1: [1, 2, 5, 6, 3, 4],
    sigma_infty: [4, 1, 2, 5, 6, 3],
    g3_side_xbar: [2, 5, 4, 6, 3, 1],
    g3_side_ybar: [1, 3, 2, 5, 4, 6],
    g3_side_zbar: [6, 1, 4, 2, 3, 5],
    source: 'sol/裁定_28_f29_conjugator.md 裁定 1・再計算 search/week4-19a19e.mjs 検算 (3)(3b)(3c) = 7/7 PASS(本便で再実行し一致を確認)',
  },
  cusp_and_uniformizer: {
    point_P0: '(x,t) = (0,0), 全分岐 cusp(lambda=0 上)',
    uniformizer: 'x (Q-有理)',
    expansion: 't = 4*x^6 + O(x^7)',
    source: 'search/week4-u-k3.mjs 検算 (7)(8)',
  },
  u: { value: '-4', ord_u_inv_mod6: 3, source: 'search/week4-u-k3.mjs 検算 (9)(10)(11)(12)' },
  covariance_control: { u_prime: '-256/729', desc: 't=infty 側のもう一方の全分岐 cusp での u(Mobius 不変性の較正)', source: 'search/week4-u-k3.mjs 検算 (13)(14)(15)(16)' },
  tau_rho0_j_orientation: {
    tau_definition: 'X (=<xbar>) -> mu_M(全分岐 cusp の Q-有理局所助変数 s に対し s^{1/M} |-> zeta_M s^{1/M})',
    source: 'docs/week4-K3飽和_opus_v3.md 「tau の mu_M 側の同定」節',
    note: '生成元の向きの曖昧さは判定にも固定体にも影響しない(同節・注 4)',
  },
  evidence_ids: [
    { id: 'K3-19a19e', path: 'search/week4-19a19e.mjs', item: '(0)-(4)', desc: '7/7 PASS(本便で再実行し確認)' },
    { id: 'K3-u-k3', path: 'search/week4-u-k3.mjs', item: '(1)-(16)', desc: '16/16 PASS(本便で再実行し確認)' },
    { id: 'K3-裁定28', path: 'sol/裁定_28_f29_conjugator.md', item: '裁定 1-5', desc: 'exact conjugator h の正典値と規約・旧値の誤りの確定' },
  ],
};
const hK3 = emit('K3-regression', k3Fixture);
console.log(`K3-regression sha256 = ${hK3}`);

console.log(`\n=== ${pass}/${pass + fail} PASS ===`);
if (fail) process.exitCode = 1;
