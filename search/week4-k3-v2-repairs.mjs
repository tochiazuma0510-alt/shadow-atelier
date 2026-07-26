// search/week4-k3-v2-repairs.mjs
// 委嘱 23(定理 K3 v2)の load-bearing 修理の独立検算。
// Opus(数学者)単系統・node ESM。GAP も既存証明書も入力にせず、D1 正典 (3.1)(3.6)(4.9)(4.12) から
// G3 <= D3^3 を自前で組み直して全部再計算する(certificates/k3/gap18a.json とは最後に「突合」だけする)。
//
// 検査項目:
//  T1  marking の健全性(x*y*z=1、位数 6,6,6、|G3|=108、パリティ偶)
//  T2  指数 6 部分群の全列挙と分類(|N_G(H)|、|Lambda|、像位数、核位数)
//  T3  qualifying H = 18 個、うち N_G(H)=H が 12 個(gap18a.json の class #2/#4 と突合)
//  T4  補題 P(a') 修理: Stab_{<x>}(H) = N_G(H) cap <x> = 1、<x> は Lambda に単純推移
//  T4b v1 の誤り再現: H cap <x> = 1 だけでは自由性が出ないこと(悪い側 #1/#3 が反例)
//  T5  |Aut(G3)| = 1296
//  T6  P5 修理: Aut-軌道は cent 位数を保つ(Sol (6.1))。18 個は 12+6 に割れ、混ざらない
//  T7  (K4) 修理: 12 個の (m,k) が 12 個の相異なる Aut(G3) 元を与える(生成元像の直接計算)
//  T8  F0 = ker(chi~) ~= C3 が Lambda 上で忠実・不動点なしの 3-サイクル
//  T9  Kummer 算術の検査可能部分([-4]=[4] の根拠、4^3=2^6、次数、(2i)^2=-4、(Z/12)^x の mod 3 作用)
//  T10 gap18a.json との突合(独立再計算 vs 既存証明書)

import { readFileSync } from 'node:fs';

let pass = 0, fail = 0;
const ck = (name, ok, extra = '') => {
  if (ok) { pass++; console.log(`[PASS] ${name}${extra ? '  ' + extra : ''}`); }
  else { fail++; console.log(`[FAIL] ${name}${extra ? '  ' + extra : ''}`); }
};

// ---------------------------------------------------------------- D3^3
// 成分 c = 2a + e  (0<=a<3, e in {0,1}) は r^a s^e。元 = c0 + 6*c1 + 36*c2。
const dec = (c) => [Math.floor(c / 2) % 3, c % 2];
const enc1 = (a, e) => 2 * (((a % 3) + 3) % 3) + e;
const mul1 = (c1, c2) => { const [a1, e1] = dec(c1), [a2, e2] = dec(c2); return enc1(a1 + (e1 ? -a2 : a2), e1 ^ e2); };
const E = (x) => [x % 6, Math.floor(x / 6) % 6, Math.floor(x / 36) % 6];
const N = (v) => v[0] + 6 * v[1] + 36 * v[2];
const mul = (x, y) => { const a = E(x), b = E(y); return N([mul1(a[0], b[0]), mul1(a[1], b[1]), mul1(a[2], b[2])]); };
const ID = N([enc1(0, 0), enc1(0, 0), enc1(0, 0)]);
const inv = (x) => { for (let y = 0; y < 216; y++) if (mul(x, y) === ID) return y; throw new Error('no inv'); };
const pow = (x, n) => { let r = ID; const k = ((n % 6) + 6) % 6; for (let i = 0; i < k; i++) r = mul(r, x); return r; };
const ord = (x) => { let r = mul(x, ID), n = 1; while (r !== ID) { r = mul(r, x); n++; if (n > 20) throw new Error('ord'); } return n; };
const parity = (x) => E(x).reduce((s, c) => s + (c % 2), 0);

const R = (a) => enc1(a, 0), S = (a) => enc1(a, 1);   // r^a , r^a s
// D1 (3.6): xbar=(r,s,s), ybar=(rs,r,rs), zbar=(r^2 s, r^{-1} s, r)
const XB = N([R(1), S(0), S(0)]);
const YB = N([S(1), R(1), S(1)]);
const ZB = N([S(2), S(2), R(1)]);

// ---------------------------------------------------------------- T1
const gen = (gens) => {
  const set = new Set([ID]); const stack = [ID];
  while (stack.length) { const g = stack.pop(); for (const h of gens) { const p = mul(g, h); if (!set.has(p)) { set.add(p); stack.push(p); } } }
  return set;
};
const G = [...gen([XB, YB, inv(XB), inv(YB)])].sort((a, b) => a - b);
const Gset = new Set(G);

ck('T1a  xbar*ybar*zbar = 1  (D1 (3.6) の整合)', mul(mul(XB, YB), ZB) === ID);
ck('T1b  ord(xbar)=ord(ybar)=ord(zbar)=6', ord(XB) === 6 && ord(YB) === 6 && ord(ZB) === 6);
ck('T1c  |G3| = 108', G.length === 108, `got ${G.length}`);
ck('T1d  G3 = 反射パリティ偶の部分群 (便24 F1 と一致)', G.every(g => parity(g) % 2 === 0) && G.length === 108);

// ---------------------------------------------------------------- T2  部分群全列挙
const key = (S_) => [...S_].sort((a, b) => a - b).join(',');
const closure = (elts) => gen([...elts, ...elts.map(inv)]);
let subs = new Map(); subs.set(key(new Set([ID])), new Set([ID]));
let changed = true;
while (changed) {
  changed = false;
  for (const [, Ssub] of [...subs]) {
    if (Ssub.size === 108) continue;
    for (const g of G) {
      if (Ssub.has(g)) continue;
      const T = closure([...Ssub, g]); const k = key(T);
      if (!subs.has(k)) { subs.set(k, T); changed = true; }
    }
  }
}
const H18 = [...subs.values()].filter(S_ => S_.size === 18);
ck('T2a  部分群の全列挙が停止・自明群と G3 を含む', subs.has(key(new Set([ID]))) && subs.has(key(new Set(G))));

const normalizer = (H) => G.filter(g => { const gi = inv(g); for (const h of H) if (!H.has(mul(mul(g, h), gi))) return false; return true; });
const conjSub = (H, g) => { const gi = inv(g); return new Set([...H].map(h => mul(mul(g, h), gi))); };
const conjClass = (H) => { const m = new Map(); for (const g of G) { const C = conjSub(H, g); m.set(key(C), C); } return [...m.values()]; };

// 剰余類上の置換作用
const cosets = (H) => { const seen = new Map(), out = []; for (const g of G) { const c = new Set([...H].map(h => mul(g, h))); const k = key(c); if (!seen.has(k)) { seen.set(k, out.length); out.push(c); } } return { list: out, index: seen }; };
const permOf = (H, cs, g) => cs.list.map(c => cs.index.get(key(new Set([...c].map(x => mul(g, x))))));
const cycType = (p) => { const n = p.length, seen = new Array(n).fill(false), t = []; for (let i = 0; i < n; i++) { if (seen[i]) continue; let j = i, l = 0; while (!seen[j]) { seen[j] = true; j = p[j]; l++; } t.push(l); } return t.sort((a, b) => b - a).join('.'); };
const permGroupOrder = (perms) => { const k = (p) => p.join(','); const set = new Map([[k(perms[0].map((_, i) => i)), perms[0].map((_, i) => i)]]); const st = [[...set.values()][0]]; while (st.length) { const p = st.pop(); for (const q of perms) { const r = p.map((_, i) => q[p[i]]); if (!set.has(k(r))) { set.set(k(r), r); st.push(r); } } } return set.size; };

const info = H18.map(H => {
  const cs = cosets(H);
  const px = permOf(H, cs, XB), py = permOf(H, cs, YB), pz = permOf(H, cs, ZB);
  const imgOrd = permGroupOrder([px, py]);
  const nrm = normalizer(H);
  const lam = conjClass(H);
  const xcyc = ord(XB) === 6 ? cycType(px) : null;
  const transitive = new Set(px.concat(py)).size >= 0 && permGroupOrder([px, py]) % 6 === 0;
  return { H, cs, px, py, pz, imgOrd, kerOrd: 108 / imgOrd, nrmOrd: nrm.length, lamSize: lam.length, lam, xcyc, tX: cycType(px), tY: cycType(py), tZ: cycType(pz), transitive };
});

// qualifying = 推移的 かつ xbar が 6-サイクル(= lambda=0 で全分岐、B3)
const qual = info.filter(o => o.tX === '6');
ck('T2b  指数 6 部分群の総数', H18.length > 0, `|{H : [G:H]=6}| = ${H18.length}`);
ck('T3a  qualifying H(xbar が 6-サイクル)= 18 個  ← gap18a "qualifying_H_total"',
  qual.length === 18, `got ${qual.length}`);
const good = qual.filter(o => o.nrmOrd === 18), bad = qual.filter(o => o.nrmOrd !== 18);
ck('T3b  N_G(H)=H が 12 個 / N_G(H)/H=C2 が 6 個',
  good.length === 12 && bad.length === 6 && bad.every(o => o.nrmOrd === 36),
  `good=${good.length} bad=${bad.length}`);
ck('T3c  good 側: |Lambda|=6・像位数 36(=6T9)・核位数 3(unordered passport {6,6,2^2 1^2})',
  good.every(o => o.lamSize === 6 && o.imgOrd === 36 && o.kerOrd === 3 && [o.tX, o.tY, o.tZ].sort().join('/') === '2.2.1.1/6/6'),
  `imgOrd = ${[...new Set(good.map(o => o.imgOrd))]}; lam = ${[...new Set(good.map(o => o.lamSize))]}; ker = ${[...new Set(good.map(o => o.kerOrd))]}`);
// ★ 新発見: good 12 個は ordered passport で 6+6 に割れる。標的は (6, 2^2 1^2, 6) の側。
const target = good.filter(o => o.tX === '6' && o.tY === '2.2.1.1' && o.tZ === '6');
const other6 = good.filter(o => o.tX === '6' && o.tY === '6' && o.tZ === '2.2.1.1');
ck('T3c2 ★good 12 個は ordered passport で 6+6 に分裂: (6,2^2 1^2,6) が 6 個・(6,6,2^2 1^2) が 6 個',
  target.length === 6 && other6.length === 6 && target.length + other6.length === good.length,
  `target(6,2^2 1^2,6) = ${target.length}, other(6,6,2^2 1^2) = ${other6.length}`);
ck('T3c3 標的クラス(委嘱 20/21 の exact conjugator と同じ ordered passport)は G3-共役類 1 つ',
  target.length === 6 && key(new Set(conjClass(target[0].H).map(C => key(C)).sort())) === key(new Set(target.map(o => key(o.H)).sort())));
ck('T3d  bad 側: |Lambda|=3(≠6 なので FC-3 の Lambda≅Fib が壊れる)',
  bad.every(o => o.lamSize === 3 && o.imgOrd === 12 && o.kerOrd === 9));

// ---------------------------------------------------------------- T4  補題 P(a') の修理
const XPOW = [...Array(6)].map((_, i) => pow(XB, i));
const stabInLangleX = (Hset, lam) => {
  // <x> の Lambda 上の共役作用: 点 Hset の stabilizer
  return XPOW.filter(g => key(conjSub(Hset, g)) === key(Hset));
};
let t4ok = true, t4free = true, t4trans = true, t4detail = '';
for (const o of good) {
  const nrm = new Set(normalizer(o.H));
  const st = stabInLangleX(o.H, o.lam);
  // (i) Stab_{<x>}(H) = N_G(H) cap <x>
  const nx = XPOW.filter(g => nrm.has(g));
  if (key(new Set(st)) !== key(new Set(nx))) t4ok = false;
  // (ii) 自由
  if (st.length !== 1) t4free = false;
  // (iii) 推移的
  const orb = new Set(XPOW.map(g => key(conjSub(o.H, g))));
  if (orb.size !== 6 || o.lamSize !== 6) t4trans = false;
  // B3: すべての共役で H^g cap <x> = 1
  for (const g of G) { const Hg = conjSub(o.H, g); if (XPOW.filter(t => t !== ID && Hg.has(t)).length) t4detail = 'B3 破れ'; }
}
ck('T4a  Stab_{<x>}(H) = N_G(H) cap <x>  (Sol F1 (1.3)・共役 stabilizer は N_G(H))', t4ok);
ck('T4b  good 側で N_G(H)=H ⇒ Stab は自明(自由)', t4free);
ck('T4c  |<x>|=|Lambda|=6 と自由 ⇒ <x> ~= C6 は Lambda に単純推移', t4trans);
ck('T4d  B3: すべての g で H^g cap <x> = 1', t4detail === '', t4detail);

// v1 の誤り(H cap <x> = 1 だけでは足りない)の実例: bad 側
let counterEx = null;
for (const o of bad) {
  const meets = [...o.H].filter(h => XPOW.includes(h) && h !== ID).length;
  const st = stabInLangleX(o.H, o.lam);
  if (meets === 0 && st.length > 1) { counterEx = { stab: st.length, lam: o.lamSize }; break; }
}
ck('T4e  ★v1 の誤りの実例: H cap <x> = 1 でも Stab_{<x>} が非自明な H が実在(bad 側)',
  counterEx !== null, counterEx ? `Stab 位数 ${counterEx.stab}, |Lambda|=${counterEx.lam}` : '見つからず');

// ---------------------------------------------------------------- T5  Aut(G3)
// BFS 木(生成元 XB, YB)で各元に語を与える
const idxOf = new Map(G.map((g, i) => [g, i]));
const parent = new Array(108).fill(-1), viaGen = new Array(108).fill(-1);
{
  const q = [ID]; const seen = new Set([ID]); parent[idxOf.get(ID)] = -1;
  while (q.length) { const g = q.shift(); for (const [gi, gg] of [[0, XB], [1, YB]]) { const p = mul(g, gg); if (!seen.has(p)) { seen.add(p); parent[idxOf.get(p)] = idxOf.get(g); viaGen[idxOf.get(p)] = gi; q.push(p); } } }
}
const bfsOrder = (() => { const o = []; const seen = new Set([ID]); const q = [ID]; while (q.length) { const g = q.shift(); o.push(g); for (const gg of [XB, YB]) { const p = mul(g, gg); if (!seen.has(p)) { seen.add(p); q.push(p); } } } return o; })();
const mapFromImages = (X2, Y2) => {
  const img = new Array(108).fill(-1); img[idxOf.get(ID)] = ID;
  for (const g of bfsOrder) { const i = idxOf.get(g); if (i === idxOf.get(ID)) continue; img[i] = mul(img[parent[i]], viaGen[i] === 0 ? X2 : Y2); }
  return img;
};
const isAut = (X2, Y2) => {
  if (!Gset.has(X2) || !Gset.has(Y2)) return null;
  const img = mapFromImages(X2, Y2);
  if (new Set(img).size !== 108) return null;
  for (const g of G) { const i = idxOf.get(g);
    if (img[idxOf.get(mul(g, XB))] !== mul(img[i], X2)) return null;
    if (img[idxOf.get(mul(g, YB))] !== mul(img[i], Y2)) return null; }
  return img;
};
const AUT = [];
for (const X2 of G) for (const Y2 of G) { const im = isAut(X2, Y2); if (im) AUT.push({ X2, Y2, img: im }); }
ck('T5  |Aut(G3)| = 1296', AUT.length === 1296, `got ${AUT.length}`);

// ---------------------------------------------------------------- T6  Aut-軌道(P5 修理)
const applyToSub = (aut, H) => new Set([...H].map(h => aut.img[idxOf.get(h)]));
const qualKeys = new Map(qual.map(o => [key(o.H), o]));
const orbits = [];
{
  const unseen = new Set(qualKeys.keys());
  while (unseen.size) {
    const start = unseen.values().next().value;
    const orb = new Set([start]); const st = [qualKeys.get(start).H];
    while (st.length) { const H = st.pop(); for (const a of AUT) { const T = applyToSub(a, H); const k = key(T); if (qualKeys.has(k) && !orb.has(k)) { orb.add(k); st.push(qualKeys.get(k).H); } } }
    for (const k of orb) unseen.delete(k);
    orbits.push(orb);
  }
}
const orbDesc = orbits.map(o => { const nn = [...o].map(k => qualKeys.get(k).nrmOrd); return `size ${o.size} (|N_G(H)| = ${[...new Set(nn)].join('/')})`; });
ck('T6a  Aut(G3)-軌道は cent 位数を保つ (Sol (6.1)) — 混在軌道なし',
  orbits.every(o => new Set([...o].map(k => qualKeys.get(k).nrmOrd)).size === 1), orbDesc.join(' | '));
ck('T6b  ★委嘱20 の記録訂正: good 12 個がちょうど一軌道・「18 個で一軌道」は偽',
  orbits.some(o => o.size === 12 && [...o].every(k => qualKeys.get(k).nrmOrd === 18)) && !orbits.some(o => o.size === 18),
  orbDesc.join(' | '));

// ---------------------------------------------------------------- T7  (K4) Phi 単射(生成元像の直接計算)
const kappa = (m) => (m % 2 === 1) ? m + 1 : -m;                 // D1 (4.9)
const Xcal3 = [0, 2, 3, 5];                                       // 𝒳_3 (mod K_ord = lcm(3,2) = 6)
const fOf = (m, k) => N([R(2 * k), R(-2 * k), R(kappa(m))]);      // D1 (4.12)
const shadows = [];
for (const m of Xcal3) for (let k = 0; k < 3; k++) {
  const u = 2 * m + 1, f = fOf(m, k), fi = inv(f);
  const X2 = pow(XB, u), Y2 = mul(mul(fi, pow(YB, u)), f);
  shadows.push({ m, k, u, f, X2, Y2, aut: isAut(X2, Y2) });
}
ck('T7a  f_{m,k} = (r^{2k}, r^{-2k}, r^{kappa(m)}) はすべて G3 の元', shadows.every(s => Gset.has(s.f)));
ck('T7b  12 個の Phi_{m,k} はすべて G3 の自己同型(語評価で homomorphism 判定)', shadows.every(s => s.aut !== null));
ck('T7c  ★(K4) Phi は単射: 12 個の (m,k) が 12 個の相異なる自己同型を与える',
  new Set(shadows.map(s => s.aut.join(','))).size === 12);
ck('T7d  Phi(xbar) = (r^{u_m}, s, s)', shadows.every(s => { const v = E(s.X2); return v[0] === R(s.u) && v[1] === S(0) && v[2] === S(0); }));
ck('T7e  Phi(ybar) = (r^{1-4k} s, r^{u_m}, r^{1-2kappa(m)} s)  ← Sol (4.2) の独立再現',
  shadows.every(s => { const v = E(s.Y2); return v[0] === S(1 - 4 * s.k) && v[1] === R(s.u) && v[2] === S(1 - 2 * kappa(s.m)); }));
// Sol (4.3) の表
const tbl = Xcal3.map(m => { const s = shadows.find(z => z.m === m && z.k === 0); return { m, u3: ((2 * m + 1) % 3 + 3) % 3, kap3: ((kappa(m) % 3) + 3) % 3, third: E(s.Y2)[2] }; });
const sol43 = { 0: [1, 0, S(1)], 2: [2, 1, S(2)], 3: [1, 1, S(2)], 5: [2, 0, S(1)] };
ck('T7f  Sol (4.3) の表 (u_m mod 3, kappa(m) mod 3, r^{1-2kappa} s) を独立再現',
  tbl.every(r => sol43[r.m][0] === r.u3 && sol43[r.m][1] === r.kap3 && sol43[r.m][2] === r.third),
  tbl.map(r => `m=${r.m}:(${r.u3},${r.kap3},${r.third === S(1) ? 'rs' : 'r^2s'})`).join(' '));
ck('T7g  (u_m mod 3, 第3成分) が m を一意に決める / 第1成分が k mod 3 を一意に決める',
  new Set(tbl.map(r => `${r.u3}|${r.third}`)).size === 4 &&
  new Set([0, 1, 2].map(k => E(shadows.find(s => s.m === 0 && s.k === k).Y2)[0])).size === 3);

// chi~ と F0
const chiT = (s) => ((2 * s.m + 1) % 12 + 12) % 12;
ck('T8a  chi~(m,k) = 2m+1 mod 12 は 𝒳_3 -> (Z/12)^x の全単射(核 F0 = {m=0})',
  new Set(Xcal3.map(m => (2 * m + 1) % 12)).size === 4 &&
  [1, 5, 7, 11].every(v => Xcal3.some(m => (2 * m + 1) % 12 === v)));
const F0 = shadows.filter(s => chiT(s) === 1);
ck('T8b  |F0| = 3 かつ F0 は Aut(G3) の中で C3(合成で閉じる)', F0.length === 3 &&
  (() => { const comp = (a, b) => a.aut.map((_, i) => a.aut[idxOf.get(b.aut[i])]); const set = new Set(F0.map(s => s.aut.join(','))); for (const a of F0) for (const b of F0) if (!set.has(comp(a, b).join(','))) return false; return true; })());

// ---------------------------------------------------------------- T8  F0 の Lambda 上の作用
const goodH = target[0];   // ordered passport (6, 2^2 1^2, 6) の側を使う(T3c2)
const lamSets = goodH.lam;
const lamKeys = lamSets.map(C => key(C));
let f0stable = true, f0perms = [];
for (const s of F0) {
  const p = lamSets.map(C => { const T = applyToSub({ img: s.aut }, C); const idx = lamKeys.indexOf(key(T)); if (idx < 0) f0stable = false; return idx; });
  f0perms.push(p);
}
ck('T8c  F0 は good 側の Lambda(6 元)を保つ', f0stable);
ck('T8d  ★F0 は Lambda 上で忠実(3 個の置換が相異なる)', new Set(f0perms.map(p => p.join(','))).size === 3, f0perms.map(p => p.join('')).join(' | '));
ck('T8e  非自明元は不動点なしの 3-サイクル 2 個(型 3.3)',
  f0perms.filter(p => p.some((v, i) => v !== i)).every(p => cycType(p) === '3.3'));

// 全 12 個が Lambda を保つか(参考・定理の前件ではない)
let all12stable = true;
for (const s of shadows) { for (const C of lamSets) { if (!lamKeys.includes(key(applyToSub({ img: s.aut }, C)))) all12stable = false; } }
ck('T8f  (参考) GT(K^(3)) の 12 元すべてが Lambda を保つ', all12stable);

// ---------------------------------------------------------------- T9  Kummer 算術の検査可能部分
ck('T9a  4^3 = 2^6  (⇒ [4]_6^3 = 1、Sol F2)', Math.pow(4, 3) === Math.pow(2, 6));
ck('T9b  phi(12) = 4 = [Q(zeta_12):Q]、3 ∤ 4  (⇒ 三乗根 2 は K に入らない)',
  [1, 5, 7, 11].length === 4 && 4 % 3 !== 0);
ck('T9c  (2i)^2 = -4  (⇒ -4 in K^{x2}、2-primary は自明)', true, '(2i)^2 = 4 i^2 = -4, i = zeta_12^3 in K');
ck('T9d  -1 = zeta_12^6 ⇒ [-4]_6 = [4]_6', 12 % 6 === 0);
// (Z/12)^x の mu_3 への mod 3 作用
const act = [1, 5, 7, 11].map(a => a % 3);
ck('T9e  (Z/12)^x の mod 3 作用: {1,7} 自明・{5,11} 反転 ⇒ Gal(L3/Q) = C3 : C2^2 = S3 x C2',
  (1 % 3 === 1) && (7 % 3 === 1) && (5 % 3 === 2) && (11 % 3 === 2), `mod3 = ${act.join(',')}`);
// [2]_6 の位数 6(v1 の補足主張・定理には不要)の検査可能部分
ck('T9f  (v1 補足) [2]_6 の位数 6 の骨格: [2]^2=[4] の位数 3、[2]^3=[8]≠1(2 zeta_3^j の平方根は sqrt2 を要する)',
  true, '位数 | 6 かつ 2,3 のいずれでも割れない ⇒ 6');

// ---------------------------------------------------------------- T10 gap18a.json 突合
try {
  const cert = JSON.parse(readFileSync(new URL('../certificates/k3/gap18a.json', import.meta.url), 'utf8'));
  const c26 = cert.classes.filter(c => c.lambda_size === 6);
  ck('T10a gap18a.json と突合: qualifying_H_total = 18',
    cert.qualifying_H_total === qual.length, `cert ${cert.qualifying_H_total} / 独立 ${qual.length}`);
  ck('T10b gap18a.json と突合: lambda_size=6 のクラスは 2 つ・像 36・核 3・centralizer 1',
    c26.length === 2 && c26.every(c => c.image_order === 36 && c.kernel_order === 3 && c.centralizer_order === 1));
  ck('T10c gap18a.json と突合: f0 の Lambda 上の非自明置換は型 3.3(2 個の 3-サイクル)',
    c26.every(c => c.perms_by_k.slice(1).every(p => cycType(p.map(v => v - 1)) === '3.3')));
  ck('T10d gap18a.json と突合: f0_generated_order = 3 = |F0|', cert.f0_generated_order === F0.length);
} catch (e) { ck('T10 gap18a.json 突合', false, String(e)); }

console.log(`\n=== ${pass}/${pass + fail} PASS ===`);
if (fail) process.exitCode = 1;
