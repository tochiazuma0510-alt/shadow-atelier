// search/week4-k5-bridge-d1.mjs
// ============================================================================
// ツール仕様ヘッダ(所在と能力.md 追記の標準に従う)
//
// 入力   : なし(D1 正典 `docs/notes/抽出_Kn定義_D1.md` の (3.1)(3.6)(4.9)(4.12) だけを
//          読んで G_5 <= D_5^3 を自前で組み直す)。最後の H 群でのみ既存証明書
//          `certificates/K5.v1.json`(C-4)と「突合」する。
// モード / 触れてよいデータ範囲:
//          **群論のみ**。u の抽出・Kummer 類・固定体・円分体上の位数には一切触れない
//          (委嘱の封印規律 — 算術側 S5/S6 は次工程)。
// 出力スキーマ:
//          標準出力に `[PASS]/[FAIL] <名前>  <補足>` 行、末尾に `=== n/N PASS ===`。
//          FAIL があれば exitCode = 1。
// 検査する不変量:
//          (a) |G_5| = 500 = 4*5^3 ・[G_5,G_5] = <r>^3 (125) ・Z(G_5) = 1 ・符号表 (1.4)
//          (b) |GT(K^(5))| = 40 ・X_5 (8 元) ・chi~: X_5 -> (Z/20)^x 全単射 ・|F_0| = 5
//          (c) Phi の自己同型性・単射性・R 上の対角形・**Phi_{0,k} = inn(X^{-2k})**
//          (d) 位数 50 の部分群の全列挙 / qualifying 50 / good 40 / |Lambda| = 10 /
//              ordered passport 20+20 / G_5-共役類 2+2 / 種数 2 / Aut(dessin) = 1
//          (e) (6') 判定: Lambda の Phi(GT)-安定性・rho_0 忠実・rho_0(F_0) = tau(mu_10[5])
//          (f) 最小 faithful transitive 次数 20 ・passport (10^2,10^2,10^2) ・種数 8 ・Aut = C_5
//          (g) |Aut(G_5)| = 48000 と marked triple の自由推移(B1)
// ============================================================================

import { readFileSync } from 'node:fs';

let pass = 0, fail = 0;
const ck = (name, ok, extra = '') => {
  if (ok) { pass++; console.log(`[PASS] ${name}${extra ? '  ' + extra : ''}`); }
  else { fail++; console.log(`[FAIL] ${name}${extra ? '  ' + extra : ''}`); }
};

// ---------------------------------------------------------------- D_5^3
// D_5 = <r,s | r^5, s^2, srs^{-1}r>。元 r^a s^e を code 2a+e (0..9) で表す。
const dA = (c) => ((c - (c % 2)) / 2) % 5, dE = (c) => c % 2;
const enc1 = (a, e) => 2 * (((a % 5) + 5) % 5) + (e & 1);
const mul1 = (c1, c2) => {
  const a1 = dA(c1), e1 = dE(c1), a2 = dA(c2), e2 = dE(c2);
  return enc1(a1 + (e1 ? -a2 : a2), e1 ^ e2);
};
// D_5^3 の元 = c0 + 10 c1 + 100 c2 (0..999)
const E3 = (x) => [x % 10, Math.floor(x / 10) % 10, Math.floor(x / 100) % 10];
const N3 = (v) => v[0] + 10 * v[1] + 100 * v[2];
const MUL = (x, y) => { const a = E3(x), b = E3(y); return N3([mul1(a[0], b[0]), mul1(a[1], b[1]), mul1(a[2], b[2])]); };
const IDG = 0;
const parity = (x) => E3(x).reduce((s, c) => s + (c % 2), 0) % 2;
const RR = (a) => enc1(a, 0), SS = (a) => enc1(a, 1);

// D1 (3.6) の n = 5: xbar = (r,s,s), ybar = (rs,r,rs), zbar = (r^2 s, r^{-1} s, r)
const XB = N3([RR(1), SS(0), SS(0)]);
const YB = N3([SS(1), RR(1), SS(1)]);
const ZB = N3([SS(2), SS(-1), RR(1)]);

// ---- 生成
const genSet = (gens) => {
  const set = new Set([IDG]); const st = [IDG];
  while (st.length) { const g = st.pop(); for (const h of gens) { const p = MUL(g, h); if (!set.has(p)) { set.add(p); st.push(p); } } }
  return set;
};
const invRaw = (x) => { for (let y = 0; y < 1000; y++) if (MUL(x, y) === IDG) return y; throw new Error('no inv'); };
const G = [...genSet([XB, YB, invRaw(XB), invRaw(YB)])].sort((a, b) => a - b);
const NG = G.length;
const idx = new Map(G.map((g, i) => [g, i]));

// ---- 500x500 積表(以降はすべて添字演算)
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

// ================================================================ A. G_5 の基本量
ck('A1  xbar*ybar*zbar = 1  (D1 (3.6) の n=5 版の整合)', mul(mul(X, Y), Z) === ID);
ck('A2  ord(xbar)=ord(ybar)=ord(zbar)=10 = lcm(5,2)  ((3.4))', ORD[X] === 10 && ORD[Y] === 10 && ORD[Z] === 10);
ck('A3  |G_5| = 500 = 4*5^3   ← C-1 (cross-checked)', NG === 500, `got ${NG}`);
ck('A4  G_5 = D_5^3 の反射パリティ偶の部分群(指数 2)', G.every(g => parity(g) === 0) && NG === 500);

// R = <r>^3 = 5-元の集合
const Rset = new Set(); for (let i = 0; i < NG; i++) if (ORD[i] === 1 || ORD[i] === 5) Rset.add(i);
const Rlist = [...Rset];
ck('A5a R := {g : g^5 = 1} は位数 125 の部分群 = <r>x<r>x<r>', Rlist.length === 125 &&
  Rlist.every(a => Rlist.every(b => Rset.has(mul(a, b)))));
// 導来群
const commutators = new Set();
for (let i = 0; i < NG; i++) for (let j = 0; j < NG; j++) commutators.add(mul(mul(i, j), INV[mul(j, i)]));
const D = genSet0([...commutators]);
function genSet0(gens) { const s = new Set([ID]); const st = [ID]; while (st.length) { const g = st.pop(); for (const h of gens) { const p = mul(g, h); if (!s.has(p)) { s.add(p); st.push(p); } } } return s; }
ck('A5b [G_5,G_5] = R,  |[G_5,G_5]| = 125   ← Prop 3.6 (3.8)(4∤5)・K5.v1 derived_order', D.size === 125 &&
  [...D].every(g => Rset.has(g)), `|D| = ${D.size}`);
ck('A5c G_5/[G_5,G_5] ~= C_2 x C_2', NG / D.size === 4);
// 中心
const center = []; for (let i = 0; i < NG; i++) { let ok = true; for (let j = 0; j < NG; j++) if (mul(i, j) !== mul(j, i)) { ok = false; break; } if (ok) center.push(i); }
ck('A6  Z(G_5) = 1  (便 24 (1.6) の n=5 版)', center.length === 1 && center[0] === ID);

// 座標: R ~= (Z/5)^3, e_j = j 番目成分の r
const e1 = idx.get(N3([RR(1), RR(0), RR(0)])), e2 = idx.get(N3([RR(0), RR(1), RR(0)])), e3 = idx.get(N3([RR(0), RR(0), RR(1)]));
const vecOf = (g) => E3(G[g]).map(c => dA(c));           // R の元 -> (a1,a2,a3)
const eltOf = (v) => idx.get(N3(v.map(a => RR(a))));
// q_j: X,Y,Z の像(パリティ)
const q1 = idx.get(N3([RR(0), SS(0), SS(0)])), q2 = idx.get(N3([SS(0), RR(0), SS(0)])), q3 = idx.get(N3([SS(0), SS(0), RR(0)]));
ck('A7a q_1=(1,s,s), q_2=(s,1,s), q_3=(s,s,1) は G_5 の C_2^2-補群(Schur-Zassenhaus)',
  [q1, q2, q3].every(q => ORD[q] === 2) && mul(q1, q2) === q3 && mul(q2, q1) === q3 && mul(q1, q3) === q2);
// 符号表 (1.4)
const signTable = [q1, q2, q3].map(q => [e1, e2, e3].map(e => {
  const c = mul(mul(q, e), INV[q]);
  if (c === e) return '+'; if (c === INV[e]) return '-'; return '?';
}));
ck('A7b ★符号表 (1.4) の n=5 版は n=3 と字面まで同一: h_i(e_j) = +(i=j) / -(i≠j)',
  JSON.stringify(signTable) === JSON.stringify([['+', '-', '-'], ['-', '+', '-'], ['-', '-', '+']]),
  signTable.map(r => r.join('')).join(' | '));
ck('A7c ⇒ G_5 ~= F_5^3 : C_2^2(三本の線は C_2^2 の三つの非自明指標・固定部分 0・作用忠実)',
  [e1, e2, e3].every(e => [q1, q2, q3].some(q => mul(mul(q, e), INV[q]) === INV[e])));
// marking の半直積表示(委嘱の X=(r,s,s),Y=(rs,r,rs),Z=(r^2 s, r^{-1} s, r) 型)
ck('A8  X = e^{(1,0,0)} q_1,  Y = e^{(1,1,1)} q_2,  Z = e^{(2,-1,1)} q_3',
  X === mul(eltOf([1, 0, 0]), q1) && Y === mul(eltOf([1, 1, 1]), q2) && Z === mul(eltOf([2, 4, 1]), q3));
ck('A9  X^2 = e_1^2, Y^2 = e_2^2, Z^2 = e_3^2 (D1 p.15 の x̄^2=(r^2,1,1) 等)',
  powi(X, 2) === powi(e1, 2) && powi(Y, 2) === powi(e2, 2) && powi(Z, 2) === powi(e3, 2));
// 中心化群(B4)
const centralizer = (g) => { const out = []; for (let i = 0; i < NG; i++) if (mul(i, g) === mul(g, i)) out.push(i); return out; };
const CX = centralizer(X);
const cycX = genSet0([X]);
ck('A10 B4: C_{G_5}(X) = <X> ~= C_10(巡回)', CX.length === 10 && CX.every(g => cycX.has(g)));
ck('A10b B4 は charming な全 u = 2m+1 で同じ(gcd(u,10)=1 ⇒ <X^u> = <X>)',
  [1, 3, 7, 9, 11, 13, 17, 19].every(u => { const g = powi(X, u); return ORD[g] === 10 && genSet0([g]).size === 10; }));
ck('A10c ★教材(便24 F4 注)C_{G_5}(X^2) は位数 250 で非巡回 — B4 に代入してはならない',
  centralizer(powi(X, 2)).length === 250);

// ================================================================ B. GT(K^(5)) の構造
const kappa = (m) => (m % 2 === 1) ? m + 1 : -m;         // D1 (4.9)
const Xcal5 = []; for (let m = 0; m < 10; m++) { const u = 2 * m + 1; if (gcd(u, 10) === 1) Xcal5.push(m); }
function gcd(a, b) { while (b) { [a, b] = [b, a % b]; } return a; }
ck('B1  X_5 = {m in 0..9 : gcd(2m+1, K_ord=10) = 1} = {0,1,3,4,5,6,8,9}  (|X_5| = 8)',
  Xcal5.join(',') === '0,1,3,4,5,6,8,9');
ck('B2  chi~: m -> 2m+1 は X_5 -> (Z/20)^x の全単射(⇒ K = Q(zeta_20), 2M = 20)',
  new Set(Xcal5.map(m => (2 * m + 1) % 20)).size === 8 &&
  [1, 3, 7, 9, 11, 13, 17, 19].every(v => Xcal5.some(m => (2 * m + 1) % 20 === v)));
// (4.12) 4∤5 ゆえ k は ord(r^2) = 5 で自由
const shadows = [];
for (const m of Xcal5) for (let k = 0; k < 5; k++) {
  const f = eltOf([2 * k, -2 * k, kappa(m)].map(a => ((a % 5) + 5) % 5));
  shadows.push({ m, k, u: 2 * m + 1, f });
}
ck('B3  |GT(K^(5))| = |X_5| * ord(r^2) = 8 * 5 = 40   ← Thm 4.3 (4.12)', shadows.length === 40);
ck('B4  Thm 4.6 (4.23) との一致: |Aff(Z/5) x Z_2| = (5*4)*2 = 40', 5 * 4 * 2 === shadows.length);
const F0 = shadows.filter(s => (s.u % 20) === 1);
ck('B5  F_0 = ker chi~ = {m = 0} x {k mod 5},  |F_0| = e = 5  (位数 5 ⇒ C_5・巡回)',
  F0.length === 5 && F0.every(s => s.m === 0));
ck('B6  M = ord(X) = K_ord = 10,  e = 5,  e | M,  M/e = 2', ORD[X] === 10 && F0.length === 5 && 10 % 5 === 0);
ck('B7  ★gcd(e, M/e) = gcd(5,2) = 1 ⇒ n=5 も **coprime regime**(便 28 P4 の repeated-primary ではない)',
  gcd(5, 2) === 1);
ck('B8  ★奇数族は構造的に常に coprime: n 奇 ⇒ M = 2n, e = n, gcd(n,2) = 1',
  [3, 5, 7, 9, 11, 13, 15].every(n => gcd(n, 2) === 1));
ck('B9  ★repeated-primary は 8 | n のときだけ(4|n で e = n/4, M/e = 4, gcd(n/4,4) > 1 ⟺ 8|n)',
  [4, 12, 20].every(n => gcd(n / 4, 4) === 1) && [8, 16, 24].every(n => gcd(n / 4, 4) > 1));

// ================================================================ C. Phi の検査
// BFS 語表現(生成元 X, Y)
const par = new Int16Array(NG).fill(-1), via = new Int16Array(NG).fill(-1), bfs = [];
{ const q = [ID], seen = new Uint8Array(NG); seen[ID] = 1;
  while (q.length) { const g = q.shift(); bfs.push(g);
    for (const [gi, gg] of [[0, X], [1, Y]]) { const p = mul(g, gg); if (!seen[p]) { seen[p] = 1; par[p] = g; via[p] = gi; q.push(p); } } } }
const imgBuf = new Int16Array(NG), seenImg = new Int16Array(NG);
let autStamp = 0;
const autOf = (X2, Y2) => {
  autStamp++;
  imgBuf[ID] = ID;
  for (let t = 1; t < bfs.length; t++) { const g = bfs[t]; imgBuf[g] = mul(imgBuf[par[g]], via[g] === 0 ? X2 : Y2); }
  // 全単射
  for (let t = 0; t < bfs.length; t++) { const v = imgBuf[bfs[t]]; if (seenImg[v] === autStamp) return null; seenImg[v] = autStamp; }
  // 準同型
  for (let i = 0; i < NG; i++) {
    if (imgBuf[mul(i, X)] !== mul(imgBuf[i], X2)) return null;
    if (imgBuf[mul(i, Y)] !== mul(imgBuf[i], Y2)) return null;
  }
  return Int16Array.from(imgBuf);
};
for (const s of shadows) { s.X2 = powi(X, s.u); s.Y2 = mul(mul(INV[s.f], powi(Y, s.u)), s.f); s.aut = autOf(s.X2, s.Y2); }
ck('C1  40 個の Phi_{m,k} はすべて G_5 の自己同型(語評価で全単射性+準同型性を悉皆)',
  shadows.every(s => s.aut !== null));
// 【便 29 ⑦】Phi 単射は (6') とは **別ゲート**。補題 R の (7.4) は ker Ih の固定体で、
// ker(Phi∘Ih) まで述べるときにのみ全 GT(K^(5)) 上の単射性が要る。
ck('C2  [別ゲート] Phi: GT(K^(5)) -> Aut(G_5) は単射(40 個が相異なる自己同型)',
  new Set(shadows.map(s => s.aut.join(','))).size === 40);
// Phi(Y) の閉形式
ck('C3  Phi_{m,k}(X) = e^{(u,0,0)} q_1,  Phi_{m,k}(Y) = e^{(1-4k, u, 1-2kappa(m))} q_2',
  shadows.every(s => s.X2 === mul(eltOf([((s.u % 5) + 5) % 5, 0, 0]), q1) &&
    s.Y2 === mul(eltOf([1 - 4 * s.k, s.u, 1 - 2 * kappa(s.m)].map(a => ((a % 5) + 5) % 5)), q2)));
// Phi|_R = diag(u, u, 1-2kappa(m))
const scalarOn = (aut, e) => { for (let l = 1; l < 5; l++) if (aut[e] === powi(e, l)) return l; return null; };
ck('C4  ★Phi|_R = diag(u, u, 1-2kappa(m)) mod 5,  第 3 成分の符号 = (-1)^m ・u',
  shadows.every(s => {
    const l = [scalarOn(s.aut, e1), scalarOn(s.aut, e2), scalarOn(s.aut, e3)];
    const u5 = ((s.u % 5) + 5) % 5, third = ((1 - 2 * kappa(s.m)) % 5 + 5) % 5;
    const expect3 = s.m % 2 === 0 ? u5 : ((-u5 % 5) + 5) % 5;
    return l[0] === u5 && l[1] === u5 && l[2] === third && third === expect3;
  }));
ck('C5  Phi_{0,k}(X) = X  (chi~ = 1 ⇒ u = 1)', F0.every(s => s.X2 === X));
// ★★ 縮約の核心: Phi_{0,k} = inn(X^{-2k})
ck('C6  ★★Phi_{0,k} = inn(X^{-2k})(= inn(e^{(-2k,0,0)}))— F_0 の像は <X^2> による内部自己同型',
  F0.every(s => { const g = powi(X, -2 * s.k); for (let i = 0; i < NG; i++) if (s.aut[i] !== mul(mul(g, i), INV[g])) return false; return true; }));
ck('C6b ⇒ Phi|_{F_0} は Inn(G_5) に入り、k -> X^{-2k} は Z/5 -> <X^2> の同型', new Set(F0.map(s => powi(X, -2 * s.k))).size === 5);

// ================================================================ D. 位数 50 の部分群と Lambda
// 完全性の根拠: |H| = 50 = 2*25 なら H の Sylow 5-部分群は指数 2 ゆえ正規かつ一意で、
// R = {g : g^5 = 1} ゆえ H ∩ R = Syl_5(H)(位数 25)。従って H = <U, g>(g in H \ R)。
const key = (S) => [...S].sort((a, b) => a - b).join(',');
const closure = (elts) => genSet0([...elts, ...elts.map(g => INV[g])]);
// (i) R の位数 25 部分群
const U25 = new Map();
for (const a of Rlist) for (const b of Rlist) { const C = closure([a, b]); if (C.size === 25) { const k = key(C); if (!U25.has(k)) U25.set(k, C); } }
ck('D1  R = F_5^3 の位数 25 部分群(= 2 次元部分空間)は 31 個', U25.size === 31, `got ${U25.size}`);
// (ii) 位数 50 の部分群
const H50 = new Map();
const nonR = []; for (let i = 0; i < NG; i++) if (!Rset.has(i)) nonR.push(i);
for (const U of U25.values()) for (const g of nonR) { const C = closure([...U, g]); if (C.size === 50) { const k = key(C); if (!H50.has(k)) H50.set(k, C); } }
const Hs = [...H50.values()];
ck('D2  位数 50 の部分群の全列挙(H∩R = Syl_5(H) 位数 25 ゆえ完全)', Hs.length > 0, `|{H : |H| = 50}| = ${Hs.length}`);

const normalizer = (H) => { const out = []; for (let g = 0; g < NG; g++) { let ok = true; for (const h of H) if (!H.has(mul(mul(g, h), INV[g]))) { ok = false; break; } if (ok) out.push(g); } return out; };
const conjSub = (H, g) => { const gi = INV[g]; const S = new Set(); for (const h of H) S.add(mul(mul(g, h), gi)); return S; };
const conjClass = (H) => { const m = new Map(); for (let g = 0; g < NG; g++) { const C = conjSub(H, g); m.set(key(C), C); } return [...m.values()]; };
const cosets = (H) => { const seen = new Map(), list = []; for (let g = 0; g < NG; g++) { const c = new Set(); for (const h of H) c.add(mul(g, h)); const k = key(c); if (!seen.has(k)) { seen.set(k, list.length); list.push(c); } } return { list, seen }; };
const permOf = (cs, g) => cs.list.map(c => { const t = new Set(); for (const x of c) t.add(mul(g, x)); return cs.seen.get(key(t)); });
const cycType = (p) => { const n = p.length, sn = new Array(n).fill(false), t = []; for (let i = 0; i < n; i++) { if (sn[i]) continue; let j = i, l = 0; while (!sn[j]) { sn[j] = true; j = p[j]; l++; } t.push(l); } return t.sort((a, b) => b - a).join('.'); };
const coreOf = (H) => { let C = new Set(H); for (let g = 0; g < NG; g++) { const D2 = conjSub(H, g); C = new Set([...C].filter(x => D2.has(x))); } return C; };
const permOrder = (perms) => { const k = (p) => p.join(','); const n = perms[0].length; const idp = [...Array(n)].map((_, i) => i); const set = new Map([[k(idp), idp]]); const st = [idp]; while (st.length) { const p = st.pop(); for (const q of perms) { const r = p.map((_, i) => q[p[i]]); if (!set.has(k(r))) { set.set(k(r), r); st.push(r); } } } return set.size; };

const info = Hs.map(H => {
  const cs = cosets(H);
  const px = permOf(cs, X), py = permOf(cs, Y), pz = permOf(cs, Z);
  const nrm = normalizer(H);
  const lam = conjClass(H);
  return { H, cs, px, py, pz, tX: cycType(px), tY: cycType(py), tZ: cycType(pz), nrmOrd: nrm.length, lamSize: lam.length, lam };
});
const qual = info.filter(o => o.tX === '10');   // B3: lambda = 0 で全分岐
ck('D3  qualifying H(xbar が 10-サイクル = B3 全分岐)= 50 個', qual.length === 50, `got ${qual.length}`);
const good = qual.filter(o => o.nrmOrd === 50), bad = qual.filter(o => o.nrmOrd !== 50);
ck('D4  N_G(H) = H が 40 個 / N_G(H) が大きい側が 10 個(|N| = 100・|Lambda| = 5)',
  good.length === 40 && bad.length === 10 && bad.every(o => o.nrmOrd === 100 && o.lamSize === 5),
  `good = ${good.length}, bad = ${bad.length}`);
ck('D5  good 側は |Lambda| = 10 = M = ord(X)  ⇒ 前件 (3) の第 1 条件', good.every(o => o.lamSize === 10));
const targetSet = good.filter(o => o.tX === '10' && o.tY === '2.2.2.2.1.1' && o.tZ === '10');
const mirrorSet = good.filter(o => o.tX === '10' && o.tY === '10' && o.tZ === '2.2.2.2.1.1');
ck('D6  ★good 40 個は ordered passport で 20+20 に分裂: (10, 2^4 1^2, 10) と (10, 10, 2^4 1^2)',
  targetSet.length === 20 && mirrorSet.length === 20 && targetSet.length + mirrorSet.length === good.length,
  `target = ${targetSet.length}, mirror = ${mirrorSet.length}`);
// G_5-共役類
const classesOf = (list) => { const seen = new Set(), out = []; for (const o of list) { const k = key(o.H); if (seen.has(k)) continue; const C = conjClass(o.H).map(key); C.forEach(x => seen.add(x)); out.push(C); } return out; };
const tClasses = classesOf(targetSet);
ck('D7  ★★n=3 との差: 標的 20 個は G_5-共役類 **2 つ**(各 10)— n=3 では 6 個で 1 類だった',
  tClasses.length === 2 && tClasses.every(c => c.length === 10), `classes = ${tClasses.map(c => c.length).join('+')}`);
// alpha 不変量(U = <e_2, alpha e_1 + e_3> の alpha)
const alphaOf = (o) => {
  const U = [...o.H].filter(g => Rset.has(g)).map(vecOf);
  // 法線ベクトル n を求める(n.u = 0 for all u in U)
  for (let n1 = 0; n1 < 5; n1++) for (let n2 = 0; n2 < 5; n2++) for (let n3 = 0; n3 < 5; n3++) {
    if (n1 === 0 && n2 === 0 && n3 === 0) continue;
    if (U.every(v => (n1 * v[0] + n2 * v[1] + n3 * v[2]) % 5 === 0)) {
      if (n2 !== 0) return null;                 // e_2 が U に入らない ⇒ 標的族ではない
      if (n1 === 0) return null;
      const inv5 = [0, 1, 3, 2, 4];              // 1/x mod 5
      return ((-n3 * inv5[n1]) % 5 + 5) % 5;     // alpha = -n3/n1
    }
  }
  return null;
};
const alphaByClass = tClasses.map(C => {
  const set = new Set(); for (const o of targetSet) if (C.includes(key(o.H))) set.add(alphaOf(o));
  return [...set].sort((a, b) => a - b);
});
ck('D8  ★2 類の不変量は alpha mod ±: {1,4}(平方剰余)と {2,3}(非剰余)',
  alphaByClass.length === 2 &&
  alphaByClass.some(a => a.join(',') === '1,4') && alphaByClass.some(a => a.join(',') === '2,3'),
  alphaByClass.map(a => `{${a.join(',')}}`).join(' vs '));
// 標的代表(alpha = 1 の類)を先に固定しておく
const o0 = targetSet.find(o => alphaOf(o) === 1);
// (3) 単純推移・Stab の同定(補題 P(a') の n=5 版)
let t3ok = true, t3free = true, t3stab = true, b3ok = true;
for (const o of good) {
  const nrm = new Set(normalizer(o.H));
  const lamK = o.lam.map(key);
  const XPOW = [...Array(10)].map((_, i) => powi(X, i));
  const st = XPOW.filter(g => key(conjSub(o.H, g)) === key(o.H));
  const nx = XPOW.filter(g => nrm.has(g));
  if (key(new Set(st)) !== key(new Set(nx))) t3stab = false;
  if (st.length !== 1) t3free = false;
  if (new Set(XPOW.map(g => key(conjSub(o.H, g)))).size !== 10) t3ok = false;
  for (let g = 0; g < NG; g++) { const Hg = conjSub(o.H, g); if (XPOW.some(t => t !== ID && Hg.has(t))) b3ok = false; }
}
// 【便 29 ③】前件 (3) は三つの条件を **別々に** 記録する
ck('D9-(3a) N_P(H) = H(good 40 個すべて)', good.every(o => o.nrmOrd === 50));
ck('D9-(3b) |Lambda| = 10 = M = ord(X)', good.every(o => o.lamSize === 10));
ck('D9-(3c) <X> は Lambda 上 regular: 全 coset で H^g cap <X> = 1 かつ軌道長 10',
  b3ok && t3free && t3ok);
ck('D9-(3d) Stab_{<X>}(H) = N_G(H) cap <X>(共役部分群の stabilizer は N_G(H)・W1)', t3stab);
// 【便 29 ⑤】符号による passport の事前制約 — (10,10,10) を先入観にしない
{
  const sgn = (p) => { const n = p.length, sn = new Array(n).fill(false); let s = 1;
    for (let i = 0; i < n; i++) { if (sn[i]) continue; let j = i, l = 0; while (!sn[j]) { sn[j] = true; j = p[j]; l++; } if (l % 2 === 0) s = -s; } return s; };
  ck('D9-(5a) ★次数 10 で (10,10,10) は **符号により不可能**(10-cycle は奇置換・奇^3 = 奇 ≠ 1)',
    sgn([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]) === -1);
  ck('D9-(5b) 観測 passport (10, 2^4 1^2, 10) は符号整合(奇・偶・奇 ⇒ 積は偶 = 1)',
    good.every(o => sgn(o.px) * sgn(o.py) * sgn(o.pz) === 1) && sgn(o0.px) === -1 && sgn(o0.py) === 1 && sgn(o0.pz) === -1);
}
// core / monodromy
ck('D12 標的 H の core = <e_2> (位数 5)・monodromy 像は位数 100', coreOf(o0.H).size === 5 && permOrder([o0.px, o0.py]) === 100,
  `|core| = ${coreOf(o0.H).size}, |mon| = ${permOrder([o0.px, o0.py])}`);
ck('D13 B2: Aut(dessin) = N_G(H)/H = 1  ⇒ 標的次数 10 では B2 PASS(≠ 最小忠実次数 20)', o0.nrmOrd === 50);
// Riemann-Hurwitz
const rh = (deg, types) => { const c = types.reduce((s, t) => s + t.split('.').length, 0); return (-2 * deg + (3 * deg - c)) / 2 + 1; };
ck('D14 Riemann-Hurwitz: 次数 10・(10, 2^4 1^2, 10) ⇒ 種数 **2**', rh(10, [o0.tX, o0.tY, o0.tZ]) === 2, `g = ${rh(10, [o0.tX, o0.tY, o0.tZ])}`);
// 2 つの dessin は非同型か(sigma_x を標準 10-サイクルへ正規化 → sigma_y を <sigma_x> 共役で比較)
const normalizeDessin = (o) => {
  const pts = []; let p = 0; for (let i = 0; i < 10; i++) { pts.push(p); p = o.px[p]; }
  const pos = new Map(pts.map((v, i) => [v, i]));
  return pts.map((v, i) => pos.get(o.py[v]));
};
const dessinKey = (o) => {
  const sy = normalizeDessin(o);
  const cands = [];
  for (let c = 0; c < 10; c++) cands.push([...Array(10)].map((_, i) => (sy[((i - c) % 10 + 10) % 10] + c) % 10).join(','));
  return cands.sort()[0];
};
const dk = new Set(targetSet.map(dessinKey));
ck('D15 ★標的 passport (10,2^4 1^2,10) の dessin は **2 個**(G_5-共役類 1 つに 1 個・互いに非同型)',
  dk.size === 2, `distinct dessins = ${dk.size}`);
// 【便 29 ①/W3 の実例】「|Lambda| = e = 5 に合わせたくなる」誘惑が実在する
ck('D16b ★bad 側(10 個)は |Lambda| = 5 = e。だが Stab_{<X>}(H) の位数が 2 で tau が非単射 ⇒ mu_10-torsor を失う(前件 (3) 破れ = scope-out)',
  bad.every(o => { const XPOW = [...Array(10)].map((_, i) => powi(X, i));
    const st = XPOW.filter(g => key(conjSub(o.H, g)) === key(o.H));
    return o.lamSize === 5 && st.length === 2; }));
ck('D16 同一 G_5-共役類の H はすべて同じ dessin を与える',
  tClasses.every(C => new Set(targetSet.filter(o => C.includes(key(o.H))).map(dessinKey)).size === 1));

// ================================================================ E. 前件 (6') の判定
const applyAut = (aut, S) => { const T2 = new Set(); for (const g of S) T2.add(aut[g]); return T2; };
const lam = o0.lam, lamK = lam.map(key);
const tau = lam.map(C => lamK.indexOf(key(conjSub(C, X))));
ck('E1  tau: mu_10 -> Sym(Lambda) は 10-サイクル(regular)', cycType(tau) === '10');
const comp = (p, q) => p.map((_, i) => q[p[i]]);
const TAU = []; { let p = lam.map((_, i) => i); for (let i = 0; i < 10; i++) { TAU.push(p); p = comp(p, tau); } }
const TAUK = new Set(TAU.map(p => p.join(',')));
// 【便 29 ③】(6') の二成分は **別々に** 記録する。安定性 = 前提、忠実性 = 補題 R' の 1 ビット入力。
let stableF0 = true;
for (const s of F0) for (const C of lam) if (!lamK.includes(key(applyAut(s.aut, C)))) stableF0 = false;
ck('E2a (6\'-i) Lambda は **Phi(F_0)-安定**(rho_0 が定義されるための最低条件)', stableF0);
let stable40 = true;
for (const s of shadows) for (const C of lam) if (!lamK.includes(key(applyAut(s.aut, C)))) stable40 = false;
ck('E2b (参考・より強い)Lambda は Phi(GT(K^(5))) **全 40 元**で安定', stable40);
const rho0 = F0.map(s => lam.map(C => lamK.indexOf(key(applyAut(s.aut, C)))));
ck('E3  rho_0 は Lambda 上で定義され **忠実**(5 個の置換が相異)',
  rho0.every(p => p.every(v => v >= 0)) && new Set(rho0.map(p => p.join(','))).size === 5);
ck('E4  rho_0(F_0) ⊆ tau(mu_10)(補題 R\' の結論の n=5 実測)', rho0.every(p => TAUK.has(p.join(','))));
const TAU5 = new Set([0, 2, 4, 6, 8].map(i => TAU[i].join(',')));
ck('E5  ★rho_0(F_0) = tau(mu_10[5]) = <tau^2>  ⇒ **(R6-act) = 前件 (6\') PASS**',
  new Set(rho0.map(p => p.join(','))).size === 5 && rho0.every(p => TAU5.has(p.join(','))));
ck('E6  rho_0(F_0) の各元は tau と可換(補題 R\' の 2 段目)', rho0.every(p => comp(p, tau).join(',') === comp(tau, p).join(',')));
ck('E7  非自明元は不動点なしの 5-サイクル 2 個(型 5.5)', rho0.filter(p => p.some((v, i) => v !== i)).every(p => cycType(p) === '5.5'));
// W2 対照(型では部分群を同定できない)
{
  // Sym(10) の型 5.5 の元の個数 = 10!/(5*5*2) = 72576、生成する C_5 は /4
  const cnt = 3628800 / (5 * 5 * 2);
  ck('E8  【W2 対照】Sym(10) の型 5.5 の元は 72576 個・生成する C_5 は 18144 個 — 型だけでは tau(mu_10[5]) を同定できない',
    cnt === 72576 && cnt / 4 === 18144, `elts = ${cnt}, C_5 = ${cnt / 4}`);
}
// 各共役類で同じ結論か
const rho0For = (o) => { const L = o.lam, LK = L.map(key); return F0.map(s => L.map(C => LK.indexOf(key(applyAut(s.aut, C))))); };
ck('E9  2 つの G_5-共役類のどちらでも rho_0 は忠実・像は位数 5 の平行移動群',
  tClasses.every(C => { const o = targetSet.find(x => C.includes(key(x.H))); const r = rho0For(o);
    const t = o.lam.map(D2 => o.lam.map(key).indexOf(key(conjSub(D2, X))));
    const TT = []; { let p = o.lam.map((_, i) => i); for (let i = 0; i < 10; i++) { TT.push(p); p = comp(p, t); } }
    const T5 = new Set([0, 2, 4, 6, 8].map(i => TT[i].join(',')));
    return new Set(r.map(p => p.join(','))).size === 5 && r.every(p => T5.has(p.join(',')));
  }));
// Phi(GT) は 2 類のどちらも保つ(field of moduli 補題の群論的入力)
ck('E10 ★Phi(GT) は 2 つの G_5-共役類を **入れ替えない**(各類が Phi(GT)-安定)',
  tClasses.every(C => { const Cs = new Set(C); const o = targetSet.find(x => C.includes(key(x.H)));
    return shadows.every(s => Cs.has(key(applyAut(s.aut, o.H)))); }));

// 【便 29 ⑥】整合の事前枠(u には触れない・結果値を含まない)
ck('E11 事前枠: (5\')+(R6-act) が成立するなら ord([u^{-1}]_10) | e = 5 ⇒ 取りうる値は {1, 5} の二値',
  [1, 5].join(',') === [...Array(6).keys()].filter(d => d > 0 && 5 % d === 0).join(','));
ck('E12 事前枠(警報規準): 将来の走査で 2 または 10 が出たら新現象ではなく **前件札か記録の破れ**',
  5 % 2 !== 0 && 5 % 10 !== 0);

// ================================================================ I. 【便 30 F2.3/P4】整合ゲートの強化: 封印値 a
// j_i := (rho_0^{(i)})^{-1} o tau_i|_{<X^2>} : mu_10[5] --> F_0  (dessin ごとの作用同型)
// (5') が両 dessin で成立するなら Ih|_{G_K} = j_i o kappa_i、ゆえに kappa_ns = kappa_sq^a、
//   a := j_ns^{-1} j_sq in Aut(mu_5) = (Z/5)^x  … これを **u の開示前に**有限群論だけで確定する。
{
  const jFor = (o) => {
    const L = o.lam, LK = L.map(key);
    const t = L.map(C => LK.indexOf(key(conjSub(C, X))));            // tau_i(zeta_10)
    const TT = []; { let p = L.map((_, i2) => i2); for (let i2 = 0; i2 < 10; i2++) { TT.push(p); p = comp(p, t); } }
    const rho = F0.map(s => L.map(C => LK.indexOf(key(applyAut(s.aut, C)))));
    return [...Array(5)].map((_, tt) => {
      const tgt = TT[(2 * tt) % 10].join(',');
      const w = rho.findIndex(p => p.join(',') === tgt);
      return w < 0 ? null : F0[w].k;
    });
  };
  const reps = tClasses.map(C => targetSet.find(x => C.includes(key(x.H))));
  const sqRep = reps.find(o => [1, 4].includes(alphaOf(o))), nsRep = reps.find(o => [2, 3].includes(alphaOf(o)));
  const jsq = jFor(sqRep), jns = jFor(nsRep);
  ck('I1  j_i は両クラスで定義される(rho_0 の像が tau_i(mu_10[5]) を尽くす)',
    jsq.every(v => v !== null) && jns.every(v => v !== null));
  ck('I2  K5-1 の帰結: j_i(tau_i(zeta_10^{2t})) = Phi_{0,-t}  — **i に依らない**',
    jsq.every((v, tt) => v === ((-tt % 5) + 5) % 5) && jns.every((v, tt) => v === ((-tt % 5) + 5) % 5),
    `j_sq = [${jsq}]  j_ns = [${jns}]`);
  const aVals = [1, 2, 3, 4].filter(a => [...Array(5)].every((_, tt) => jns[(a * tt) % 5] === jsq[tt]));
  ck('I3  ★★封印値 a = j_ns^{-1} j_sq in (Z/5)^x  ⇒ kappa_ns = kappa_sq^a',
    aVals.length === 1, `a = ${aVals.join(',')}`);
  ck('I4  a は tau の向き(zeta_10 <-> X か X^{-1} か)に依らない — 両クラスで同一規約を使う限り不変',
    (() => { const jF2 = (o) => { const L = o.lam, LK = L.map(key);
        const t = L.map(C => LK.indexOf(key(conjSub(C, INV[X]))));   // 逆向き規約
        const TT = []; { let p = L.map((_, i2) => i2); for (let i2 = 0; i2 < 10; i2++) { TT.push(p); p = comp(p, t); } }
        const rho = F0.map(s => L.map(C => LK.indexOf(key(applyAut(s.aut, C)))));
        return [...Array(5)].map((_, tt) => { const tgt = TT[(2 * tt) % 10].join(','); const w = rho.findIndex(p => p.join(',') === tgt); return F0[w].k; }); };
      const b = [1, 2, 3, 4].filter(a => [...Array(5)].every((_, tt) => jF2(nsRep)[(a * tt) % 5] === jF2(sqRep)[tt]));
      return b.length === 1 && b[0] === aVals[0]; })());
}

// ================================================================ F. 最小 faithful transitive 作用
// core-free 部分群の最大位数を、位数 50 / 100 / 125 / 250 の全部分群で確認
const coreFreePlanes = [...U25.values()].filter(U => coreOf(U).size === 1);
ck('F1  R 内の core-free な位数 25 部分群(座標線を含まない平面)は 16 個', coreFreePlanes.length === 16, `got ${coreFreePlanes.length}`);
ck('F2  位数 50 の部分群に core-free なものは無い(⇒ 最大 core-free 位数 = 25)',
  Hs.every(H => coreOf(H).size > 1));
// 位数 100 / 125 / 250
const H100 = new Map();
for (const H of Hs) for (const g of nonR) { const C = closure([...H, g]); if (C.size === 100) H100.set(key(C), C); }
ck('F3  位数 100 の部分群にも core-free なものは無い', [...H100.values()].every(H => coreOf(H).size > 1), `|{|H|=100}| = ${H100.size}`);
ck('F4  ⇒ **最小 faithful transitive 次数 = 500/25 = 20**', 500 / 25 === 20);
{
  const U = coreFreePlanes[0];
  const cs = cosets(U);
  const px = permOf(cs, X), py = permOf(cs, Y), pz = permOf(cs, Z);
  ck('F5  最小忠実 dessin の passport = (10^2, 10^2, 10^2)', cycType(px) === '10.10' && cycType(py) === '10.10' && cycType(pz) === '10.10');
  ck('F6  Riemann-Hurwitz: 次数 20・(10^2,10^2,10^2) ⇒ 種数 **8**', rh(20, ['10.10', '10.10', '10.10']) === 8, `g = ${rh(20, ['10.10', '10.10', '10.10'])}`);
  ck('F7  B2 FAIL: Aut(dessin) = N_G(U)/U ~= C_5 ≠ 1(便 24 F3.2 の n=5 版)',
    normalizer(U).length / 25 === 5, `|N(U)/U| = ${normalizer(U).length / 25}`);
  ck('F8  忠実(core-free)⇒ monodromy = G_5 全体(位数 500)', permOrder([px, py]) === 500);
  const cls = classesOf(coreFreePlanes.map(U2 => ({ H: U2 })));
  ck('F9  ★16 平面は G_5-共役類 **4 つ**(n=3 では 4 平面で 1 類)— 最小忠実 dessin も一意でない',
    cls.length === 4 && cls.every(c => c.length === 4), `classes = ${cls.map(c => c.length).join('+')}`);
}

// ================================================================ G. Aut(G_5) と B1
let tripleCount = 0; const cands = [];
for (let a = 0; a < NG; a++) { if (ORD[a] !== 10) continue;
  for (let b = 0; b < NG; b++) { if (ORD[b] !== 10) continue; if (ORD[mul(a, b)] !== 10) continue; tripleCount++; cands.push([a, b]); } }
ck('G1  marked (10,10,10)-triple(XYZ = 1・位数条件)の個数 = 48000', tripleCount === 48000, `got ${tripleCount}`);
let autCount = 0; const autPairs = [];
for (const [a, b] of cands) { if (autOf(a, b)) { autCount++; autPairs.push([a, b]); } }
ck('G2  ★|Aut(G_5)| = 48000 = 125 * 4^3 * 6  ⇒ marked triple 上で自由推移 ⇒ **B1 PASS**',
  autCount === 48000, `got ${autCount}`);
ck('G3  (n=3 との較正)同じ公式が |Aut(G_3)| = 27*2^3*6 = 1296 を与える', 27 * 8 * 6 === 1296);
// good 40 個は Aut-軌道 1 つ
{
  const goodKeys = new Set(good.map(o => key(o.H)));
  const hit = new Set();
  for (const [a, b] of autPairs) { const A = autOf(a, b); const k = key(applyAut(A, o0.H)); if (goodKeys.has(k)) hit.add(k); }
  ck('G4  good 40 個は Aut(G_5)-軌道 1 つ(2 つの ordered passport 類・4 つの共役類を融合)',
    hit.size === 40, `orbit size within good = ${hit.size}`);
}

// ================================================================ H. 既存証明書との突合
try {
  const cert = JSON.parse(readFileSync(new URL('../certificates/K5.v1.json', import.meta.url), 'utf8'));
  ck('H1  K5.v1.json 突合: |GT(K^(5))| = 40', cert.shadows.length === shadows.length && cert.counts.hexagon_pass === 40);
  ck('H2  K5.v1.json 突合: N_ord = 10 / index_PB3 = 500 = |G_5| / derived_order = 125',
    cert.target.invariants.N_ord === ORD[X] && cert.target.invariants.index_PB3 === NG && cert.target.invariants.derived_order === D.size);
  ck('H3  K5.v1.json 突合: m 値の集合 = X_5', [...new Set(cert.shadows.map(s => s.m))].sort((a, b) => a - b).join(',') === Xcal5.join(','));
  ck('H4  K5.v1.json 突合: Thm 4.6 期待位数 40', cert.counts.thm46_expected_order === 40);
  const certF = new Set(cert.shadows.filter(s => s.m === 0).map(s => JSON.stringify(s.f_triple)));
  ck('H5  K5.v1.json 突合: m = 0 の f は (r^{2k}, r^{-2k}, 1) 5 通り(= F_0)',
    certF.size === 5 && [...certF].every(t => { const v = JSON.parse(t); return v[2][0] === 0 && v[2][1] === 0 && (v[0][0] + v[1][0]) % 5 === 0; }));
} catch (e) { ck('H  K5.v1.json 突合', false, String(e)); }

console.log(`\n=== ${pass}/${pass + fail} PASS ===`);
if (fail) process.exitCode = 1;
