#!/usr/bin/env node
// docs/scout/hall6.mjs
// ============================================================================
//  A^(6) = gamma_2(F_2)/gamma_7   (class 2, rank 21) の独立検算スクリプト
//
//  モデル: 次数 7 打ち切り Magnus 埋め込み
//      R := Z<xi,eta> / (deg >= 7),   x |-> 1+xi,  y |-> 1+eta
//  自由群では次元部分群が下中心列に一致する(Magnus/Witt)ので、この写像は
//  F_2/gamma_7 上で単射であり P^(6) の厳密モデルを与える。
//
//  外部依存なし・BigInt 整数演算のみ。   実行: node docs/scout/hall6.mjs
//
//  規約: [u,v] = u^{-1} v^{-1} u v,   u^v = v^{-1} u v,   昇順 section
//  Hall 基底(昇順):
//     w; p,q; r1,r2,r3; t1,t2,t3,t4; t5,t6; s1..s5; u1..u4
//  C = [A,A] = <t5,t6,u1,u2,u3,u4> (rank 6),   Abar = A/C (rank 15)
// ============================================================================

import fs from 'node:fs';

let PASS = 0, FAIL = 0;
const FAILMSG = [], ALLCHK = [];
function chk(cond, name) { ALLCHK.push((cond ? "pass" : "FAIL") + " | " + name);
  if (cond) PASS++; else { FAIL++; FAILMSG.push(name); console.log("  *** FAIL: " + name); } }
function head(s) { console.log("\n=== " + s + " ==="); }

// ---------------------------------------------------------------- 0. algebra
const DEG = 6;
const NIDX = (1 << (DEG + 1)) - 1;                 // 127 words of length 0..6
const LEN = new Int8Array(NIDX), VAL = new Int32Array(NIDX), OFF = [];
{
  for (let L = 0; L <= DEG; L++) OFF[L] = (1 << L) - 1;
  let k = 0;
  for (let L = 0; L <= DEG; L++) for (let v = 0; v < (1 << L); v++) { LEN[k] = L; VAL[k] = v; k++; }
}
const CAT = new Int16Array(NIDX * NIDX).fill(-1);
for (let i = 0; i < NIDX; i++) for (let j = 0; j < NIDX; j++) {
  const L = LEN[i] + LEN[j];
  if (L <= DEG) CAT[i * NIDX + j] = OFF[L] + (VAL[i] << LEN[j]) + VAL[j];
}
const zero = () => new Array(NIDX).fill(0n);
function one() { const a = zero(); a[0] = 1n; return a; }
function mul(a, b) {
  const r = zero();
  for (let i = 0; i < NIDX; i++) {
    const ai = a[i]; if (ai === 0n) continue;
    const base = i * NIDX, lim = (1 << (DEG - LEN[i] + 1)) - 1;
    for (let j = 0; j < lim; j++) { const bj = b[j]; if (bj === 0n) continue; r[CAT[base + j]] += ai * bj; }
  }
  return r;
}
const eq = (a, b) => { for (let i = 0; i < NIDX; i++) if (a[i] !== b[i]) return false; return true; };
const isOne = (a) => { if (a[0] !== 1n) return false; for (let i = 1; i < NIDX; i++) if (a[i] !== 0n) return false; return true; };
function binom(n, k) { if (k < 0) return 0n; n = BigInt(n); let num = 1n, den = 1n;
  for (let i = 0; i < k; i++) { num *= (n - BigInt(i)); den *= BigInt(i + 1); } return num / den; }
// unipotent power  (1+N)^n = sum_{k<=6} C(n,k) N^k  (all n in Z; N^7 = 0)
function upow(g, n) {
  if (g[0] !== 1n) throw new Error("upow: not unipotent");
  const N = g.slice(); N[0] = 0n;
  const res = one(); let Nk = one();
  for (let k = 1; k <= DEG; k++) { Nk = mul(Nk, N); const c = binom(n, k);
    if (c !== 0n) for (let i = 0; i < NIDX; i++) if (Nk[i] !== 0n) res[i] += c * Nk[i]; }
  return res;
}
const inv = (g) => upow(g, -1);
const comm = (a, b) => mul(mul(inv(a), inv(b)), mul(a, b));
const conj = (a, g) => mul(mul(inv(g), a), g);
// algebra substitution xi |-> imX,  eta |-> imY   (both without constant term)
function substR(imX, imY) {
  const W = new Array(NIDX); W[0] = one();
  for (let L = 1; L <= DEG; L++) for (let v = 0; v < (1 << L); v++) {
    const i = OFF[L] + v, first = (v >> (L - 1)) & 1, rest = OFF[L - 1] + (v & ((1 << (L - 1)) - 1));
    W[i] = mul(first ? imY : imX, W[rest]);
  }
  return (a) => { const r = zero();
    for (let i = 0; i < NIDX; i++) { const ai = a[i]; if (ai === 0n) continue;
      const Wi = W[i]; for (let k = 0; k < NIDX; k++) if (Wi[k] !== 0n) r[k] += ai * Wi[k]; }
    return r; };
}
const XI = zero(); XI[OFF[1] + 0] = 1n;
const ETA = zero(); ETA[OFF[1] + 1] = 1n;
const X = one(); X[OFF[1] + 0] = 1n;
const Y = one(); Y[OFF[1] + 1] = 1n;
const Z = inv(mul(X, Y));                              // z = (xy)^{-1}
const Zm1 = (() => { const a = Z.slice(); a[0] = 0n; return a; })();
const thetaR = substR(ETA, XI);                        // theta: x<->y
const tauR   = substR(ETA, Zm1);                       // tau:  x->y, y->z
const tauInvR= substR(Zm1, XI);                        // tau^{-1}: x->z, y->x

// ---------------------------------------------------------------- 1. basis
const NAMES = ['w','p','q','r1','r2','r3','t1','t2','t3','t4','t5','t6','s1','s2','s3','s4','s5','u1','u2','u3','u4'];
const WT    = [ 2,  3,  3,  4,   4,   4,   5,   5,   5,   5,   5,   5,   6,   6,   6,   6,   6,   6,   6,   6,   6 ];
const N21 = 21, IDX = {}; NAMES.forEach((n, i) => IDX[n] = i);
const ABAR = [0,1,2,3,4,5,6,7,8,9,12,13,14,15,16];     // 15 non-C indices (ascending)
const CIDX = [10,11,17,18,19,20];                      // t5,t6,u1,u2,u3,u4
function buildBasis(gx, gy) {
  const w  = comm(gx, gy);
  const p  = comm(w, gx),  q  = comm(w, gy);
  const r1 = comm(p, gx),  r2 = comm(p, gy), r3 = comm(q, gy);
  const t1 = comm(r1, gx), t2 = comm(r1, gy), t3 = comm(r2, gy), t4 = comm(r3, gy);
  const t5 = comm(w, p),   t6 = comm(w, q);
  const s1 = comm(t1, gx), s2 = comm(t1, gy), s3 = comm(t2, gy), s4 = comm(t3, gy), s5 = comm(t4, gy);
  const u1 = comm(w, r1),  u2 = comm(w, r2),  u3 = comm(w, r3),  u4 = comm(p, q);
  return [w,p,q,r1,r2,r3,t1,t2,t3,t4,t5,t6,s1,s2,s3,s4,s5,u1,u2,u3,u4];
}
const B = buildBasis(X, Y);

// ------------------------------------------------- 2. exact rational solver
function fgcd(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { const t = a % b; a = b; b = t; } return a; }
function fr(n, d) { if (d < 0n) { n = -n; d = -d; } if (n === 0n) return [0n, 1n]; const g = fgcd(n, d); return [n / g, d / g]; }
const fsub = (a, b) => fr(a[0]*b[1] - b[0]*a[1], a[1]*b[1]);
const fmul = (a, b) => fr(a[0]*b[0], a[1]*b[1]);
const fdiv = (a, b) => fr(a[0]*b[1], a[1]*b[0]);
function solveInt(M, v) {
  const rows = M.length, cols = M[0].length, A = [];
  for (let i = 0; i < rows; i++) { const row = []; for (let j = 0; j < cols; j++) row.push([M[i][j], 1n]); row.push([v[i], 1n]); A.push(row); }
  const piv = []; let r = 0;
  for (let c = 0; c < cols && r < rows; c++) {
    let pr = -1; for (let i = r; i < rows; i++) if (A[i][c][0] !== 0n) { pr = i; break; }
    if (pr < 0) continue;
    [A[r], A[pr]] = [A[pr], A[r]];
    const pv = A[r][c];
    for (let j = c; j <= cols; j++) A[r][j] = fdiv(A[r][j], pv);
    for (let i = 0; i < rows; i++) { if (i === r) continue; const f = A[i][c]; if (f[0] === 0n) continue;
      for (let j = c; j <= cols; j++) A[i][j] = fsub(A[i][j], fmul(f, A[r][j])); }
    piv.push(c); r++;
  }
  if (piv.length !== cols) throw new Error("solveInt: rank deficient");
  for (let i = r; i < rows; i++) if (A[i][cols][0] !== 0n) throw new Error("solveInt: inconsistent");
  const out = new Array(cols).fill(0n);
  for (let i = 0; i < piv.length; i++) { const f = A[i][cols]; if (f[1] !== 1n) throw new Error("solveInt: non-integral"); out[piv[i]] = f[0]; }
  return out;
}
const degPart = (a, d) => a.slice(OFF[d], OFF[d] + (1 << d));
const WIDX = {}; for (let d = 2; d <= 6; d++) WIDX[d] = [];
for (let i = 0; i < N21; i++) WIDX[WT[i]].push(i);
const BLEAD = {};
for (let d = 2; d <= 6; d++) { const cols = WIDX[d].map(i => degPart(B[i], d)); const M = [];
  for (let r = 0; r < (1 << d); r++) M.push(cols.map(c => c[r])); BLEAD[d] = M; }
function Hall(a) { let acc = one(); for (let i = 0; i < N21; i++) if (a[i] !== 0n) acc = mul(acc, upow(B[i], a[i])); return acc; }
function hallCoords(g) {
  const a = new Array(N21).fill(0n); let cur = g;
  for (let d = 2; d <= 6; d++) {
    for (let dd = 1; dd < d; dd++) for (const c of degPart(cur, dd)) if (c !== 0n) throw new Error("hallCoords: residue at deg " + dd);
    const c = solveInt(BLEAD[d], degPart(cur, d));
    WIDX[d].forEach((i, k) => a[i] = c[k]);
    let strip = one(); for (const i of WIDX[d]) if (a[i] !== 0n) strip = mul(strip, upow(B[i], a[i]));
    cur = mul(inv(strip), cur);
  }
  if (!isOne(cur)) throw new Error("hallCoords: residue after deg 6");
  return a;
}
function fmt(a) { const t = []; for (let i = 0; i < N21; i++) if (a[i] !== 0n)
    t.push((a[i] === 1n ? "" : a[i] === -1n ? "-" : a[i] + "*") + NAMES[i]);
  return t.length ? t.join(" + ").replace(/\+ -/g, "- ") : "0"; }
const fmtC = (a) => { const t = []; for (const i of CIDX) if (a[i] !== 0n)
    t.push((a[i] === 1n ? "" : a[i] === -1n ? "-" : a[i] + "*") + NAMES[i]);
  return t.length ? t.join(" + ").replace(/\+ -/g, "- ") : "0"; };
const vec = (a) => "[" + a.join(",") + "]";

// ---------------------------------------------------- 3. coordinate algebra
function kappa(a, b) { const k = new Array(N21).fill(0n);
  k[IDX.t5] = a[IDX.p]*b[IDX.w];  k[IDX.t6] = a[IDX.q]*b[IDX.w];
  k[IDX.u1] = a[IDX.r1]*b[IDX.w]; k[IDX.u2] = a[IDX.r2]*b[IDX.w];
  k[IDX.u3] = a[IDX.r3]*b[IDX.w]; k[IDX.u4] = a[IDX.q]*b[IDX.p];
  return k; }
const delta = (a) => kappa(a, a);
function cmul(a, b) { const k = kappa(a, b), r = new Array(N21); for (let i = 0; i < N21; i++) r[i] = a[i] + b[i] - k[i]; return r; }
function cpow(a, n) { n = BigInt(n); const d = delta(a), c = binom(n, 2), r = new Array(N21);
  for (let i = 0; i < N21; i++) r[i] = n * a[i] - c * d[i]; return r; }
const cinv = (a) => cpow(a, -1n);
function beta(u, v) { const b = new Array(N21).fill(0n);
  b[IDX.t5] = u[IDX.w]*v[IDX.p]  - u[IDX.p] *v[IDX.w];
  b[IDX.t6] = u[IDX.w]*v[IDX.q]  - u[IDX.q] *v[IDX.w];
  b[IDX.u1] = u[IDX.w]*v[IDX.r1] - u[IDX.r1]*v[IDX.w];
  b[IDX.u2] = u[IDX.w]*v[IDX.r2] - u[IDX.r2]*v[IDX.w];
  b[IDX.u3] = u[IDX.w]*v[IDX.r3] - u[IDX.r3]*v[IDX.w];
  b[IDX.u4] = u[IDX.p]*v[IDX.q]  - u[IDX.q] *v[IDX.p];
  return b; }
function applyTab(tab, a) { let acc = new Array(N21).fill(0n); for (let i = 0; i < N21; i++) acc = cmul(acc, cpow(tab[i], a[i])); return acc; }
const compTab = (f, g) => g.map(row => applyTab(f, row));    // table of  f o g
function secCoords(ab) { const a = new Array(N21).fill(0n); for (const i of ABAR) a[i] = ab[i]; return a; }
const Cpart = (a) => CIDX.map(i => a[i]);

let _seed = 20260726n;
function rnd(lo, hi) { _seed = (_seed * 6364136223846793005n + 1442695040888963407n) & ((1n << 64n) - 1n);
  return BigInt(lo) + ((_seed >> 17n) % BigInt(hi - lo + 1)); }
function rndVec(lo, hi, onlyAbar) { const a = new Array(N21).fill(0n);
  for (const i of (onlyAbar ? ABAR : [...Array(N21).keys()])) a[i] = rnd(lo, hi); return a; }

// ============================================================================
head("0. モデル健全性");
{
  chk(NIDX === 127, "R の次元 = 1+2+4+8+16+32+64 = 127");
  let ok = true;
  for (let i = 0; i < N21; i++) { const a = hallCoords(B[i]); for (let j = 0; j < N21; j++) if (a[j] !== (i === j ? 1n : 0n)) ok = false; }
  chk(ok, "21 基底の Hall 座標が単位ベクトル");
  const ranks = { 2:1, 3:2, 4:3, 5:6, 6:9 }; let rok = true;
  for (let d = 2; d <= 6; d++) if (WIDX[d].length !== ranks[d]) rok = false;
  chk(rok, "重み別階数 (1,2,3,6,9) = 自由 Lie 環 L_d の階数、総和 21");
  let rt = true;
  for (let n = 0; n < 40; n++) { const a = rndVec(-6, 6, false), a2 = hallCoords(Hall(a));
    for (let i = 0; i < N21; i++) if (a[i] !== a2[i]) rt = false; }
  chk(rt, "Hall 正規形の存在と一意性(往復 40 例)");
  chk(eq(tauR(tauR(tauR(X))), X) && eq(tauR(tauR(tauR(Y))), Y), "tau^3 = id");
  chk(eq(tauR(X), Y) && eq(tauR(Y), Z) && eq(tauR(Z), X), "tau: x->y->z->x");
  chk(eq(tauInvR(tauR(X)), X) && eq(tauInvR(tauR(Y)), Y), "tau^{-1} o tau = id");
  chk(eq(thetaR(thetaR(X)), X) && eq(thetaR(X), Y), "theta^2 = id on generators");
}

// ============================================================================
head("1. Hall–Witt と P^(6) 内の交換子表(委嘱項目 1)");
{
  const pool = [X, Y, Z, mul(X,Y), inv(X), inv(Y), B[0], B[1], mul(X, B[2]), mul(B[1], inv(Y))];
  let ok = true;
  for (const a of pool) for (const b of pool) for (const c of pool) {
    const T = mul(mul(comm(comm(a,b), conj(c,a)), comm(comm(c,a), conj(b,c))), comm(comm(b,c), conj(a,b)));
    if (!isOne(T)) ok = false; }
  chk(ok, "Hall 恒等式 [[a,b],c^a][[c,a],b^c][[b,c],a^b] = 1 が P^(6) で成立(1000 組)");
}
const COMM = [];
for (let i = 0; i < N21; i++) COMM.push([hallCoords(comm(B[i], X)), hallCoords(comm(B[i], Y))]);
{
  console.log("  基底元 | [.,x]                              | [.,y]");
  for (let i = 0; i < N21; i++) console.log("  " + NAMES[i].padEnd(6) + " | " + fmt(COMM[i][0]).padEnd(34) + " | " + fmt(COMM[i][1]));
  const mk = (o) => { const a = new Array(N21).fill(0n); for (const [n, c] of Object.entries(o)) a[IDX[n]] = BigInt(c); return a; };
  const HAND = {           // §2 の手計算(Hall–Witt / Jacobi)結果
    'w,x': mk({p:1}),  'w,y': mk({q:1}),
    'p,x': mk({r1:1}), 'p,y': mk({r2:1}),
    'q,x': mk({r2:1, t5:1, t6:1, u2:1, u4:-1}), 'q,y': mk({r3:1}),
    'r1,x': mk({t1:1}), 'r1,y': mk({t2:1}),
    'r2,x': mk({t2:1, t5:1, u1:1, u2:1}), 'r2,y': mk({t3:1}),
    'r3,x': mk({t3:1, t6:1, u2:2, u3:2, u4:-1}), 'r3,y': mk({t4:1}),
    't1,x': mk({s1:1}), 't1,y': mk({s2:1}),
    't2,x': mk({s2:1, u1:1}), 't2,y': mk({s3:1}),
    't3,x': mk({s3:1, u2:2, u4:-1}), 't3,y': mk({s4:1}),
    't4,x': mk({s4:1, u3:2}), 't4,y': mk({s5:1}),
    't5,x': mk({u1:1}), 't5,y': mk({u2:1, u4:-1}),
    't6,x': mk({u2:1, u4:1}), 't6,y': mk({u3:1}),
  };
  let ok = true, cells = 0; const bad = [];
  for (const [key, exp] of Object.entries(HAND)) {
    const [nm, gen] = key.split(","); const got = COMM[IDX[nm]][gen === 'x' ? 0 : 1];
    for (let i = 0; i < N21; i++) { cells++; if (got[i] !== exp[i]) { ok = false; bad.push(key + "/" + NAMES[i] + ": got " + got[i] + " exp " + exp[i]); } } }
  chk(ok, "§2 の手計算(Hall–Witt 導出)と機械計算が全 " + cells + " セル一致" + (bad.length ? "  -- " + bad.slice(0,8).join(" ; ") : ""));
  let cen = true; for (const i of [12,13,14,15,16,17,18,19,20]) if (!isOne(comm(B[i], X)) || !isOne(comm(B[i], Y))) cen = false;
  chk(cen, "重み 6 の 9 基底は P^(6) の中心(gamma_7 = 1)");
}

// ============================================================================
head("2. A の交換子表・collection 公式(委嘱項目 1)");
{
  const nz = [];
  for (let i = 0; i < N21; i++) for (let j = 0; j < N21; j++) { const c = comm(B[i], B[j]);
    if (!isOne(c)) nz.push("[" + NAMES[i] + "," + NAMES[j] + "]=" + fmt(hallCoords(c))); }
  console.log("  非自明な交換子: " + nz.join("  "));
  chk(nz.length === 12, "A 内の非自明な基底対交換子は 12 個 = 6 対 x 2 向き");
  let c2 = true;
  for (let n = 0; n < 30; n++) if (!isOne(comm(comm(Hall(rndVec(-4,4,false)), Hall(rndVec(-4,4,false))), Hall(rndVec(-4,4,false))))) c2 = false;
  chk(c2, "A は class 2 ( [[A,A],A] = 1 )");
  let cz = true;
  for (const i of CIDX) for (let n = 0; n < 10; n++) if (!isOne(comm(B[i], Hall(rndVec(-5,5,false))))) cz = false;
  chk(cz, "C = <t5,t6,u1..u4> は A の中心に含まれる(rank 6)");
  let bok = true;
  for (let n = 0; n < 100; n++) { const a = rndVec(-5,5,true), b = rndVec(-5,5,true);
    const got = hallCoords(comm(Hall(a), Hall(b))), exp = beta(a, b);
    for (let i = 0; i < N21; i++) if (got[i] !== exp[i]) bok = false; }
  chk(bok, "beta の明示形 (2.1') が実測と一致(100 対)");
  let pok = true;
  for (let n = 0; n < 200; n++) { const a = rndVec(-7,7,false), b = rndVec(-7,7,false);
    if (!eq(mul(Hall(a), Hall(b)), Hall(cmul(a,b)))) pok = false; }
  chk(pok, "積公式 (2.2') H(a)H(b) = H(a+b-kappa(a,b))(200 対)");
  let qok = true;
  for (let n = 0; n < 60; n++) { const a = rndVec(-5,5,false), e = rnd(-9, 9);
    if (!eq(upow(Hall(a), e), Hall(cpow(a, e)))) qok = false; }
  chk(qok, "冪公式 (2.3') H(a)^n = H(na - C(n,2)delta(a))(60 例・負の n 含む)");
  let iok = true;
  for (let n = 0; n < 40; n++) { const a = rndVec(-6,6,false); if (!eq(inv(Hall(a)), Hall(cinv(a)))) iok = false; }
  chk(iok, "逆元公式 (2.4')(40 例)");
  const cs = (u, v) => { const k = kappa(u, v), r = new Array(N21); for (let i = 0; i < N21; i++) r[i] = -k[i]; return r; };
  let sok = true;
  for (let n = 0; n < 120; n++) { const u = rndVec(-6,6,true), v = rndVec(-6,6,true);
    const uv = new Array(N21).fill(0n); for (let i = 0; i < N21; i++) uv[i] = u[i] + v[i];
    const got = hallCoords(mul(mul(Hall(secCoords(u)), Hall(secCoords(v))), inv(Hall(secCoords(uv))))), exp = cs(u, v);
    for (let i = 0; i < N21; i++) if (got[i] !== exp[i]) sok = false; }
  chk(sok, "section cocycle (2.5') c_s(u,v) = -kappa(u,v)(120 対)");
  const e_ = (n) => { const a = new Array(N21).fill(0n); a[IDX[n]] = 1n; return a; };
  chk(fmtC(cs(e_('w'), e_('p'))) === "0",   "c_s(w,p) = 0");
  chk(fmtC(cs(e_('p'), e_('w'))) === "-t5", "c_s(p,w) = -t5");
  chk(fmtC(cs(e_('q'), e_('p'))) === "-u4", "c_s(q,p) = -u4   [class-6 新規]");
  chk(fmtC(cs(e_('r2'), e_('w'))) === "-u2","c_s(r2,w) = -u2  [class-6 新規]");
  // 反対称部が beta
  let abk = true;
  for (let n = 0; n < 60; n++) { const u = rndVec(-5,5,true), v = rndVec(-5,5,true);
    const l = cs(u,v), r = cs(v,u), b = beta(u,v);
    for (const c of CIDX) if (l[c] - r[c] !== b[c]) abk = false; }
  chk(abk, "c_s(u,v) - c_s(v,u) = beta(u,v)(60 対)");
}

// ============================================================================
head("3. theta の full 作用表(委嘱項目 2a)");
const TH = buildBasis(Y, X).map(hallCoords);
{
  for (let i = 0; i < N21; i++) console.log("  theta(" + NAMES[i].padEnd(3) + ") = " + fmt(TH[i]));
  let ok = true;
  for (let n = 0; n < 60; n++) { const a = rndVec(-6,6,false);
    const lhs = hallCoords(thetaR(Hall(a))), rhs = applyTab(TH, a);
    for (let i = 0; i < N21; i++) if (lhs[i] !== rhs[i]) ok = false; }
  chk(ok, "座標作用 applyTab(TH,·) = theta の実作用(60 例)");
  let t2 = true;
  for (let n = 0; n < 60; n++) { const a = rndVec(-6,6,false), b = applyTab(TH, applyTab(TH, a));
    for (let i = 0; i < N21; i++) if (a[i] !== b[i]) t2 = false; }
  chk(t2, "** 自己検査 (i) **  theta^2 = id on A(座標合成・60 例)");
  const I2 = compTab(TH, TH); let t2b = true;
  for (let i = 0; i < N21; i++) for (let j = 0; j < N21; j++) if (I2[i][j] !== (i === j ? 1n : 0n)) t2b = false;
  chk(t2b, "** 自己検査 (i') ** theta^2(g_k) = g_k(全 21 基底・表の合成)");
}

// ============================================================================
head("4. sigma_m の full 作用表(委嘱項目 2b)");
const SIGCACHE = {};
function sigmaG(g, m) { return conj(tauR(g), upow(Y, m)); }
function sigTab(m) { if (!(m in SIGCACHE)) SIGCACHE[m] = B.map(g => hallCoords(sigmaG(g, m))); return SIGCACHE[m]; }
let SIGPOLY;
{
  let cok = true;
  for (const g of [X, Y]) for (const m of [0,1,2,3,5,8,13,-4,-7]) for (let n = 0; n < 8; n++) {
    const h = Hall(rndVec(-4,4,false)); let acc = h, c = h;
    for (let k = 1; k <= 4; k++) { c = comm(c, g); acc = mul(acc, upow(c, binom(m, k))); }
    if (!eq(conj(h, upow(g, m)), acc)) cok = false; }
  chk(cok, "collection 公式 (4.1') h^{g^m} = h [h,g]^C(m,1) [h,g,g]^C(m,2) [h,g,g,g]^C(m,3) [h,g,g,g,g]^C(m,4)(g=x,y・m 9 種)");
  const MS = []; for (let m = 0; m <= 10; m++) MS.push(sigTab(m));
  SIGPOLY = []; let deg4 = true;
  for (let i = 0; i < N21; i++) { const row = [];
    for (let j = 0; j < N21; j++) { let d = MS.map(T => T[i][j]); const co = [];
      for (let k = 0; k <= 10; k++) { co.push(d[0]); const nd = []; for (let t = 0; t + 1 < d.length; t++) nd.push(d[t+1] - d[t]); d = nd; }
      for (let k = 5; k <= 10; k++) if (co[k] !== 0n) deg4 = false;
      row.push(co.slice(0, 5)); } SIGPOLY.push(row); }
  chk(deg4, "sigma_m の全 441 座標成分が C(m,0..4) の整係数結合(5 階以上の差分 = 0)");
  const ev = (co, m) => { let s = 0n; for (let k = 0; k < co.length; k++) s += co[k] * binom(m, k); return s; };
  let xok = true;
  for (const m of [11,13,20,33,64,-1,-5,-12,-30]) { const T = sigTab(m);
    for (let i = 0; i < N21; i++) for (let j = 0; j < N21; j++) if (ev(SIGPOLY[i][j], m) !== T[i][j]) xok = false; }
  chk(xok, "sigma_m の m 多項式の外挿検査(m = 11,13,20,33,64,-1,-5,-12,-30)");
  const bn = ["", "m", "C(m,2)", "C(m,3)", "C(m,4)"];
  for (let i = 0; i < N21; i++) { const terms = [];
    for (let j = 0; j < N21; j++) { const co = SIGPOLY[i][j], parts = [];
      for (let k = 0; k < 5; k++) if (co[k] !== 0n) parts.push(k === 0 ? co[k].toString() : (co[k] === 1n ? "" : co[k] === -1n ? "-" : co[k] + "*") + bn[k]);
      if (parts.length) terms.push((parts.length > 1 || parts[0].startsWith("-") || /[+]/.test(parts[0]) ? "(" + parts.join("+").replace(/\+-/g, "-") + ")" : parts[0]) + NAMES[j]); }
    console.log("  sigma(" + NAMES[i].padEnd(3) + ") = " + (terms.join(" + ") || "0")); }
  let aok = true;
  for (const m of [0,1,2,3,5,7,11,-3]) { const T = sigTab(m);
    for (let n = 0; n < 6; n++) { const a = rndVec(-5,5,false);
      const lhs = hallCoords(sigmaG(Hall(a), m)), rhs = applyTab(T, a);
      for (let i = 0; i < N21; i++) if (lhs[i] !== rhs[i]) aok = false; } }
  chk(aok, "座標作用 applyTab(sigTab(m),·) = sigma_m の実作用(8 個の m x 6 例)");
  // m 依存の局在(観測)
  let loc = true;
  for (let i = 0; i < N21; i++) for (const c of [IDX.t5, IDX.t6]) for (let k = 1; k < 5; k++) if (SIGPOLY[i][c][k] !== 0n) loc = false;
  chk(loc, "観測 4.2': sigma の **t5,t6 成分は m に依らない**(class-5 の観測がそのまま生き残る)");
  let degC = 0, degA = 0;
  for (let i = 0; i < N21; i++) { for (const c of CIDX) for (let k = 0; k < 5; k++) if (SIGPOLY[i][c][k] !== 0n) degC = Math.max(degC, k);
    for (const c of ABAR) for (let k = 0; k < 5; k++) if (SIGPOLY[i][c][k] !== 0n) degA = Math.max(degA, k); }
  chk(degC === 1, "観測 4.3': sigma の C 成分は m の高々 1 次(実測最高次 = " + degC + ")、Abar 成分は " + degA + " 次");
  const mdep = [];
  for (let i = 0; i < N21; i++) for (const c of CIDX) { let d = 0; for (let k = 1; k < 5; k++) if (SIGPOLY[i][c][k] !== 0n) d = k;
    if (d) mdep.push("sigma(" + NAMES[i] + ")_" + NAMES[c]); }
  console.log("  m 依存をもつ C 成分: " + mdep.join(", "));
  // theta|_C, sigma|_C の 6x6 行列(基底 t5,t6,u1,u2,u3,u4)
  console.log("  theta|_C(列 = 像・基底 t5,t6,u1,u2,u3,u4):");
  for (const i of CIDX) console.log("    theta(" + NAMES[i].padEnd(2) + ") = " + fmtC(TH[i]));
  console.log("  sigma|_C(m 多項式):");
  for (const i of CIDX) { const parts = [];
    for (const j of CIDX) { const co = SIGPOLY[i][j], ps = [];
      for (let k = 0; k < 5; k++) if (co[k] !== 0n) ps.push(k === 0 ? co[k].toString() : (co[k] === 1n ? "" : co[k] === -1n ? "-" : co[k] + "*") + bn[k]);
      if (ps.length) parts.push("(" + ps.join("+").replace(/\+-/g, "-") + ")" + NAMES[j]); }
    console.log("    sigma(" + NAMES[i].padEnd(2) + ") = " + (parts.join(" + ") || "0")); }
  let cstab = true;
  for (const i of CIDX) { for (const j of ABAR) if (TH[i][j] !== 0n || SIGPOLY[i][j].some(c => c !== 0n)) cstab = false; }
  chk(cstab, "C = [A,A] は theta・sigma_m 不変(C-stable)");
}

// ============================================================================
head("5. E_m の明示式(委嘱項目 3)");
const EMCACHE = {};
const Em = (m) => mul(mul(upow(X, m), upow(Z, m)), upow(Y, m));
const emc = (m) => { if (!(m in EMCACHE)) EMCACHE[m] = hallCoords(Em(m)); return EMCACHE[m]; };
let EPOLY;
{
  let inA = true;
  for (const m of [0,1,2,3,5,7,11,17,23,63,-4]) for (const c of degPart(Em(m), 1)) if (c !== 0n) inA = false;
  chk(inA, "E_m = x^m z^m y^m in gamma_2(次数 1 部分が消える)");
  const MS = []; for (let m = 0; m <= 18; m++) MS.push(emc(m));
  EPOLY = []; let degOK = true, maxdeg = 0;
  for (let j = 0; j < N21; j++) { let d = MS.map(v => v[j]); const co = [];
    for (let k = 0; k <= 18; k++) { co.push(d[0]); const nd = []; for (let t = 0; t + 1 < d.length; t++) nd.push(d[t+1] - d[t]); d = nd; }
    for (let k = 0; k <= 18; k++) if (co[k] !== 0n) maxdeg = Math.max(maxdeg, k);
    for (let k = 10; k <= 18; k++) if (co[k] !== 0n) degOK = false;
    EPOLY.push(co.slice(0, 10)); }
  chk(degOK, "E_m の全 21 座標が C(m,0..9) の整係数結合(実際の最高次 = " + maxdeg + ")");
  const ev = (co, m) => { let s = 0n; for (let k = 0; k < co.length; k++) s += co[k] * binom(m, k); return s; };
  let xok = true;
  for (const m of [19,20,23,33,63,100,-1,-3,-8,-20]) { const v = emc(m);
    for (let j = 0; j < N21; j++) if (ev(EPOLY[j], m) !== v[j]) xok = false; }
  chk(xok, "E_m の閉形の外挿検査(m = 19,20,23,33,63,100,-1,-3,-8,-20)");
  const DICT = [['w',0,0],['p',1,0],['q',0,1],['r1',2,0],['r2',1,1],['r3',0,2],
                ['t1',3,0],['t2',2,1],['t3',1,2],['t4',0,3],
                ['s1',4,0],['s2',3,1],['s3',2,2],['s4',1,3],['s5',0,4]];
  let bok = true, bcells = 0;
  for (const m of [0,1,2,3,4,5,6,9,17,31,63,100,-3,-8,-20]) { const v = emc(m);
    for (const [n, a, b] of DICT) { bcells++;
      const exp = (a % 2 === 0 ? -1n : 1n) * binom(m + 1 + a, a + b + 2);
      if (v[IDX[n]] !== exp) bok = false; } }
  chk(bok, "(5.1') Ebar_m = sum_{a+b<=4} (-1)^{a+1} C(m+1+a, a+b+2) S^a T^b(" + bcells + " セル)");
  console.log("  Ebar_m(Abar 座標・C(m,k) 基底の係数 k=0..9):");
  for (const i of ABAR) console.log("    " + NAMES[i].padEnd(3) + ": " + vec(EPOLY[i]));
  console.log("  epsilon_m(C 座標・C(m,k) 基底の係数 k=0..9):");
  for (const i of CIDX) console.log("    " + NAMES[i].padEnd(3) + ": " + vec(EPOLY[i]));
  console.log("  E_m の 21 座標(m = 0..6):");
  for (let m = 0; m <= 6; m++) console.log("    m=" + m + ": " + vec(emc(m)));
  console.log("  epsilon_m の数値(m = 0..10)  [t5,t6,u1,u2,u3,u4]:");
  for (let m = 0; m <= 10; m++) console.log("    m=" + String(m).padStart(2) + ": " + vec(Cpart(emc(m))));
  // (5.2') epsilon_m の明示閉形(二項基底・整係数)
  const EPS = { t5: [0,1,7,17,17,6,0], t6: [0,0,-1,-4,-6,-3,0], u1: [0,-1,-10,-34,-52,-37,-10],
                u2: [0,0,1,7,17,17,6],  u3: [0,0,0,-1,-4,-6,-3], u4: [0,0,0,3,10,11,4] };
  let eok = true, ecells = 0;
  for (const m of [0,1,2,3,4,5,6,7,9,13,17,31,63,100,-1,-3,-8,-20]) { const v = emc(m);
    for (const [n, co] of Object.entries(EPS)) { ecells++;
      let s = 0n; for (let k = 0; k < co.length; k++) s += BigInt(co[k]) * binom(m, k);
      if (v[IDX[n]] !== s) eok = false; } }
  chk(eok, "(5.2') epsilon_m の閉形(二項基底・整係数・" + ecells + " セル)");
  // 二項基底の一段シフト関係(観測)
  const shift = (co) => [0, ...co];
  const sameArr = (a, b) => { const n = Math.max(a.length, b.length);
    for (let i = 0; i < n; i++) if (BigInt(a[i] || 0) !== BigInt(b[i] || 0)) return false; return true; };
  chk(sameArr(EPS.u2, shift(EPS.t5)) && sameArr(EPS.u3, shift(EPS.t6)),
      "観測 5.3': (eps_m)_{u2} = sum_{j<m}(eps_j)_{t5}、(eps_m)_{u3} = sum_{j<m}(eps_j)_{t6}(二項基底の一段シフト)");
}

// ============================================================================
head("6. 自己検査 (ii): sigma_m(E_m) = E_m ・ sigma_m^3 = Inn(E_m)");
{
  let s0 = true;
  for (let m = -6; m <= 12; m++) if (!eq(sigmaG(Em(m), m), Em(m))) s0 = false;
  chk(s0, "** (ii-a) ** sigma_m(E_m) = E_m を P^(6) の群積で厳密確認(m = -6..12)");
  let s1 = true;
  for (const m of [0,1,2,3,5,7,11,17,-3,-9]) { const e = emc(m), se = applyTab(sigTab(m), e);
    for (let i = 0; i < N21; i++) if (se[i] !== e[i]) s1 = false; }
  chk(s1, "** (ii-a') ** sigma_m(E_m) = E_m(作用表の座標計算・m 10 種)");
  let s3 = true;
  for (const m of [0,1,2,3,5,7,11,-4]) { const T = sigTab(m), e = emc(m);
    for (let n = 0; n < 8; n++) { const a = rndVec(-5,5,false);
      const lhs = applyTab(T, applyTab(T, applyTab(T, a))), bb = beta(a, e);
      for (let i = 0; i < N21; i++) if (lhs[i] !== a[i] + bb[i]) s3 = false; } }
  chk(s3, "** (ii-b) ** sigma_m^3 = Inn_A(E_m):  a -> a + beta(a, Ebar_m)(m 8 種 x 8 例)");
  let s3b = true;
  for (const m of [0,1,2,3,5,7,17,-4]) { const T = sigTab(m), e = emc(m), T3 = compTab(T, compTab(T, T));
    for (let i = 0; i < N21; i++) { const ei = new Array(N21).fill(0n); ei[i] = 1n; const bb = beta(ei, e);
      for (let j = 0; j < N21; j++) if (T3[i][j] !== (i === j ? 1n : 0n) + bb[j]) s3b = false; } }
  chk(s3b, "** (ii-b') ** sigma_m^3(g_k) = E_m^{-1} g_k E_m(全 21 基底 x m 8 種)");
  let s3g = true;
  for (const m of [0,1,2,3,5,-3]) for (let i = 0; i < N21; i++)
    if (!eq(sigmaG(sigmaG(sigmaG(B[i], m), m), m), conj(B[i], Em(m)))) s3g = false;
  chk(s3g, "** (ii-b'') ** sigma_m^3 = Inn(E_m) を群積で直接確認(m 6 種 x 21 基底)");
  // 命題 E1: theta sigma theta = iota_{x^u} sigma^{-1},  u = 2m+1
  let e1 = true;
  for (const m of [0,1,2,3,5,7,-2,-5]) { const u = 2*m + 1, xu = upow(X, u);
    const sigInv = (g) => tauInvR(conj(g, upow(Y, -m)));
    for (let i = 0; i < N21; i++) { const lhs = thetaR(sigmaG(thetaR(B[i]), m)), rhs = conj(sigInv(B[i]), xu);
      if (!eq(lhs, rhs)) e1 = false; } }
  chk(e1, "命題 E1  theta sigma_m theta = iota_{x^u} sigma_m^{-1}(u = 2m+1・全 21 基底 x m 8 種)");
}

// ============================================================================
head("7. section の欠損 d_theta, d_sigma, epsilon_m(委嘱項目 4)");
{
  console.log("  d_theta(e_k):");
  for (const k of ABAR) { const a = new Array(N21).fill(0n); a[k] = 1n; console.log("    " + NAMES[k].padEnd(3) + " : " + fmtC(applyTab(TH, a))); }
  console.log("  d_sigma(e_k)(m 多項式・二項基底):");
  { const bn2 = ["", "m", "C(m,2)", "C(m,3)", "C(m,4)"];
    for (const k of ABAR) { const parts = [];
      for (const c of CIDX) { const co = SIGPOLY[k][c], ps = [];
        for (let t = 0; t < 5; t++) if (co[t] !== 0n) ps.push(t === 0 ? co[t].toString() : (co[t] === 1n ? "" : co[t] === -1n ? "-" : co[t] + "*") + bn2[t]);
        if (ps.length) parts.push("(" + ps.join("+").replace(/\+-/g, "-") + ")" + NAMES[c]); }
      console.log("    " + NAMES[k].padEnd(3) + " : " + (parts.join(" + ") || "0")); } }
  function dClosed(tab, ab) {   // (6.1') 一般形
    const out = new Array(N21).fill(0n);
    for (const k of ABAR) { const ek = new Array(N21).fill(0n); ek[k] = 1n; const dk = applyTab(tab, ek);
      for (const c of CIDX) out[c] += ab[k] * dk[c]; }
    for (const k of ABAR) { const d = delta(tab[k]), c2 = binom(ab[k], 2);
      for (const c of CIDX) out[c] -= c2 * d[c]; }
    for (let x = 0; x < ABAR.length; x++) for (let y = x + 1; y < ABAR.length; y++) {
      const j = ABAR[x], k = ABAR[y], kk = kappa(tab[j], tab[k]);
      for (const c of CIDX) out[c] -= ab[j] * ab[k] * kk[c]; }
    return out; }
  let ok1 = true;
  for (let n = 0; n < 120; n++) { const a = rndVec(-7,7,true), got = applyTab(TH, secCoords(a)), exp = dClosed(TH, a);
    for (const c of CIDX) if (got[c] !== exp[c]) ok1 = false; }
  chk(ok1, "(6.1') 一般 collection 閉形 [theta](120 例)");
  let ok2 = true;
  for (const m of [0,1,2,3,5,7,11,17,-4]) { const T = sigTab(m);
    for (let n = 0; n < 25; n++) { const a = rndVec(-7,7,true), got = applyTab(T, secCoords(a)), exp = dClosed(T, a);
      for (const c of CIDX) if (got[c] !== exp[c]) ok2 = false; } }
  chk(ok2, "(6.1') 一般 collection 閉形 [sigma_m](9 個の m x 25 例)");
  function dShort(tab, ab) {   // (6.2') 簡約形
    const out = new Array(N21).fill(0n);
    for (const k of ABAR) { const ek = new Array(N21).fill(0n); ek[k] = 1n; const dk = applyTab(tab, ek);
      for (const c of CIDX) out[c] += ab[k] * dk[c]; }
    const W = tab[IDX.w], P = tab[IDX.p], Q = tab[IDX.q], dW = delta(W), c2w = binom(ab[IDX.w], 2);
    for (const c of CIDX) out[c] -= c2w * dW[c];
    out[IDX.u4] -= binom(ab[IDX.p], 2) * P[IDX.q] * P[IDX.p];
    out[IDX.u4] -= binom(ab[IDX.q], 2) * Q[IDX.q] * Q[IDX.p];
    out[IDX.u4] -= ab[IDX.w]*ab[IDX.p]*W[IDX.q]*P[IDX.p] + ab[IDX.w]*ab[IDX.q]*W[IDX.q]*Q[IDX.p] + ab[IDX.p]*ab[IDX.q]*P[IDX.q]*Q[IDX.p];
    return out; }
  let ok3 = true;
  for (let n = 0; n < 200; n++) { const a = rndVec(-8,8,true), got = applyTab(TH, secCoords(a)), exp = dShort(TH, a);
    for (const c of CIDX) if (got[c] !== exp[c]) ok3 = false; }
  chk(ok3, "(6.2') 簡約閉形 [theta](200 例)");
  let ok4 = true;
  for (const m of [0,1,2,3,5,7,11,17,63,-4]) { const T = sigTab(m);
    for (let n = 0; n < 40; n++) { const a = rndVec(-8,8,true), got = applyTab(T, secCoords(a)), exp = dShort(T, a);
      for (const c of CIDX) if (got[c] !== exp[c]) ok4 = false; } }
  chk(ok4, "(6.2') 簡約閉形 [sigma_m](10 個の m x 40 例)");
  // 明示式 d_theta
  const dThE = {}; for (const k of ABAR) { const ek = new Array(N21).fill(0n); ek[k] = 1n; dThE[k] = applyTab(TH, ek); }
  const dTheta = (a) => { const o = new Array(N21).fill(0n);
    for (const k of ABAR) for (const c of CIDX) o[c] += a[k] * dThE[k][c];
    o[IDX.u4] -= a[IDX.p] * a[IDX.q]; return o; };
  let ok5 = true;
  for (let n = 0; n < 300; n++) { const a = rndVec(-9,9,true), got = applyTab(TH, secCoords(a)), exp = dTheta(a);
    for (const c of CIDX) if (got[c] !== exp[c]) ok5 = false; }
  chk(ok5, "(6.3') d_theta = 線型 - a_p a_q u4(300 例)  ** class-6 で新規の二次項 **");
  // 明示式 d_sigma
  let ok6 = true;
  for (const m of [0,1,2,3,5,7,11,17,63,-4,-11]) { const T = sigTab(m);
    const dS = {}; for (const k of ABAR) { const ek = new Array(N21).fill(0n); ek[k] = 1n; dS[k] = applyTab(T, ek); }
    for (let n = 0; n < 40; n++) { const a = rndVec(-9,9,true), o = new Array(N21).fill(0n);
      for (const k of ABAR) for (const c of CIDX) o[c] += a[k] * dS[k][c];
      const c2 = binom(a[IDX.w], 2), M = BigInt(m);
      o[IDX.t5] += c2;  o[IDX.t6] -= c2 * M;  o[IDX.u1] -= c2;  o[IDX.u2] += c2 * M;  o[IDX.u3] -= c2 * binom(M, 2);
      o[IDX.u4] += c2 * M - binom(a[IDX.q], 2) + M * a[IDX.w] * a[IDX.q] + a[IDX.p] * a[IDX.q];
      const got = applyTab(T, secCoords(a));
      for (const c of CIDX) if (got[c] !== o[c]) ok6 = false; } }
  chk(ok6, "(6.4') d_sigma の明示式(11 個の m x 40 例)");
  // ---- 本文 §6.3'/§6.4' に書き下す明示式そのものを検査(ハードコード) ----
  const A_ = (a, n) => a[IDX[n]];
  function dThetaLit(a) { const o = new Array(N21).fill(0n);
    o[IDX.t5] = -(A_(a,'q') + A_(a,'r2') + A_(a,'t3'));
    o[IDX.t6] = -(A_(a,'p') + A_(a,'r2') + A_(a,'t2'));
    o[IDX.u1] = -(A_(a,'r3') + 2n*A_(a,'t3') + 2n*A_(a,'s4'));
    o[IDX.u2] = -(2n*A_(a,'r2') + 2n*A_(a,'t2') + 2n*A_(a,'t3') + 3n*A_(a,'s3'));
    o[IDX.u3] = -(A_(a,'r1') + 2n*A_(a,'t2') + 2n*A_(a,'s2'));
    o[IDX.u4] = A_(a,'t2') - A_(a,'t3') - A_(a,'p')*A_(a,'q');
    return o; }
  function dSigmaLit(a, m) { const M = BigInt(m), c2 = binom(A_(a,'w'), 2), o = new Array(N21).fill(0n);
    o[IDX.t5] = -A_(a,'q') + A_(a,'r2') - 3n*A_(a,'r3') + A_(a,'t3') - 2n*A_(a,'t4') + c2;
    o[IDX.t6] = -A_(a,'r3') - A_(a,'t2') + A_(a,'t3') - A_(a,'t4') - M*c2;
    o[IDX.u1] = 2n*A_(a,'q') - 2n*A_(a,'r2') + 9n*A_(a,'r3') - 4n*A_(a,'t3') + 12n*A_(a,'t4')
              - 2n*A_(a,'s4') + 5n*A_(a,'s5') - c2;
    o[IDX.u2] = (1n-M)*A_(a,'q') + (M-1n)*A_(a,'r2') + (9n-3n*M)*A_(a,'r3') + 3n*A_(a,'t2')
              + (M-7n)*A_(a,'t3') + (17n-2n*M)*A_(a,'t4') + 3n*A_(a,'s3') - 6n*A_(a,'s4') + 9n*A_(a,'s5') + M*c2;
    o[IDX.u3] = (2n-M)*A_(a,'r3') - M*A_(a,'t2') + (M-2n)*A_(a,'t3') + (5n-M)*A_(a,'t4')
              - 2n*A_(a,'s2') + 3n*A_(a,'s3') - 3n*A_(a,'s4') + 3n*A_(a,'s5') - binom(M,2)*c2;
    o[IDX.u4] = M*A_(a,'w') + A_(a,'p') + (M-3n)*A_(a,'q') + (2n-M)*A_(a,'r2') + (3n*M-6n)*A_(a,'r3')
              + (3n-M)*A_(a,'t3') + (2n*M-8n)*A_(a,'t4') + 2n*A_(a,'s4') - 4n*A_(a,'s5')
              + M*c2 - binom(A_(a,'q'), 2) + M*A_(a,'w')*A_(a,'q') + A_(a,'p')*A_(a,'q');
    return o; }
  let okL1 = true;
  for (let n = 0; n < 300; n++) { const a = rndVec(-9,9,true), got = applyTab(TH, secCoords(a)), exp = dThetaLit(a);
    for (const c of CIDX) if (got[c] !== exp[c]) okL1 = false; }
  chk(okL1, "** 本文 (6.3') の逐語式 ** d_theta の 6 成分明示式(300 例)");
  let okL2 = true;
  for (const m of [0,1,2,3,5,7,11,17,63,-4,-11]) for (let n = 0; n < 40; n++) {
    const a = rndVec(-9,9,true), got = applyTab(sigTab(m), secCoords(a)), exp = dSigmaLit(a, m);
    for (const c of CIDX) if (got[c] !== exp[c]) okL2 = false; }
  chk(okL2, "** 本文 (6.4') の逐語式 ** d_sigma の 6 成分明示式(11 個の m x 40 例)");
  // d_{sigma^2} の合成公式
  let ok7 = true;
  for (const m of [0,1,2,3,5,7,-4]) { const T = sigTab(m), T2 = compTab(T, T), sC = {};
    for (const c of CIDX) { const ec = new Array(N21).fill(0n); ec[c] = 1n; sC[c] = applyTab(T, ec); }
    for (let n = 0; n < 25; n++) { const a = rndVec(-6,6,true);
      const d1 = applyTab(T, secCoords(a)), sa = d1.slice(); // sigma(s a) coords
      const sbar = new Array(N21).fill(0n); for (const i of ABAR) sbar[i] = d1[i];
      const d2 = applyTab(T, secCoords(sbar));
      const got = applyTab(T2, secCoords(a));
      const o = new Array(N21).fill(0n);
      for (const c of CIDX) o[c] += d2[c];
      for (const c of CIDX) { const img = sC[c]; for (const cc of CIDX) o[cc] += d1[c] * img[cc]; }
      for (const c of CIDX) if (got[c] !== o[c]) ok7 = false; } }
  chk(ok7, "(6.5') d_{sigma^2}(a) = d_sigma(sigmabar a) + sigma|_C(d_sigma(a))(m 7 種 x 25 例)");
}

// ============================================================================
head("8. 自己検査 (iii): weight <= 5 制限 = docs/week4-E2作用表_v1.md と全セル一致");
{
  const N12 = 12, I5 = { w:0,p:1,q:2,r1:3,r2:4,r3:5,t1:6,t2:7,t3:8,t4:9,t5:10,t6:11 };
  const v5 = (o) => { const a = new Array(N12).fill(0n); for (const [k, c] of Object.entries(o)) a[I5[k]] = BigInt(c); return a; };
  const C5 = {   // §2.1
    'w,x': v5({p:1}),  'w,y': v5({q:1}),
    'p,x': v5({r1:1}), 'p,y': v5({r2:1}),
    'q,x': v5({r2:1,t5:1,t6:1}), 'q,y': v5({r3:1}),
    'r1,x': v5({t1:1}), 'r1,y': v5({t2:1}),
    'r2,x': v5({t2:1,t5:1}), 'r2,y': v5({t3:1}),
    'r3,x': v5({t3:1,t6:1}), 'r3,y': v5({t4:1}),
    't1,x': v5({}), 't1,y': v5({}), 't2,x': v5({}), 't2,y': v5({}), 't3,x': v5({}), 't3,y': v5({}),
    't4,x': v5({}), 't4,y': v5({}), 't5,x': v5({}), 't5,y': v5({}), 't6,x': v5({}), 't6,y': v5({}),
  };
  const T5 = {   // §3.2
    w: v5({w:-1}), p: v5({q:-1,t6:-1}), q: v5({p:-1,t5:-1}),
    r1: v5({r3:-1}), r2: v5({r2:-1,t5:-1,t6:-1}), r3: v5({r1:-1}),
    t1: v5({t4:-1}), t2: v5({t3:-1,t6:-1}), t3: v5({t2:-1,t5:-1}), t4: v5({t1:-1}),
    t5: v5({t6:1}), t6: v5({t5:1}),
  };
  const S5 = (m) => { const c2 = binom(m,2), c3 = binom(m,3), M = BigInt(m); const o = {};
    o.w  = v5({w:1,p:-1,r1:1,t1:-1}); o.w[I5.q] = M; o.w[I5.r2] = -M; o.w[I5.r3] = c2; o.w[I5.t2] = M; o.w[I5.t3] = -c2; o.w[I5.t4] = c3;
    o.p  = v5({q:1,r2:-1,t2:1});      o.p[I5.r3] = M; o.p[I5.t3] = -M; o.p[I5.t4] = c2;
    o.q  = v5({p:-1,q:-1,r1:2,t1:-3,t5:-1}); o.q[I5.r2] = 2n-M; o.q[I5.r3] = 1n-M; o.q[I5.t2] = 2n*M-3n; o.q[I5.t3] = 2n*M-2n-c2; o.q[I5.t4] = M-1n-c2;
    o.r1 = v5({r3:1,t3:-1});          o.r1[I5.t4] = M;
    o.r2 = v5({r2:-1,r3:-1,t2:2,t5:1}); o.r2[I5.t3] = 2n-M; o.r2[I5.t4] = 1n-M;
    o.r3 = v5({r1:1,r2:2,r3:1,t1:-3,t5:-3,t6:-1}); o.r3[I5.t2] = M-6n; o.r3[I5.t3] = 2n*M-5n; o.r3[I5.t4] = M-2n;
    o.t1 = v5({t4:1}); o.t2 = v5({t3:-1,t4:-1,t6:-1}); o.t3 = v5({t2:1,t3:2,t4:1,t5:1,t6:1});
    o.t4 = v5({t1:-1,t2:-3,t3:-3,t4:-1,t5:-2,t6:-1}); o.t5 = v5({t6:1}); o.t6 = v5({t5:-1,t6:-1});
    return o; };
  const dTh5 = (a) => ({ t5: -(a[I5.q] + a[I5.r2] + a[I5.t3]), t6: -(a[I5.p] + a[I5.r2] + a[I5.t2]) });
  const dSg5 = (a, m) => ({ t5: -a[I5.q] + a[I5.r2] - 3n*a[I5.r3] + a[I5.t3] - 2n*a[I5.t4] + binom(a[I5.w],2),
                            t6: -a[I5.r3] - a[I5.t2] + a[I5.t3] - a[I5.t4] - BigInt(m)*binom(a[I5.w],2) });
  const E5 = (m) => { const a = new Array(N12).fill(0n);
    a[I5.w] = -binom(m+1,2); a[I5.p] = binom(m+2,3); a[I5.q] = -binom(m+1,3);
    a[I5.r1] = -binom(m+3,4); a[I5.r2] = binom(m+2,4); a[I5.r3] = -binom(m+1,4);
    a[I5.t1] = binom(m+4,5); a[I5.t2] = -binom(m+3,5); a[I5.t3] = binom(m+2,5); a[I5.t4] = -binom(m+1,5);
    a[I5.t5] = binom(m,1) + 7n*binom(m,2) + 17n*binom(m,3) + 17n*binom(m,4) + 6n*binom(m,5);
    a[I5.t6] = -(binom(m,2) + 4n*binom(m,3) + 6n*binom(m,4) + 3n*binom(m,5));
    return a; };
  const proj = (a) => a.slice(0, 12);
  let cells = 0; const bad = [];
  const cmp = (got, exp, tag) => { for (let i = 0; i < 12; i++) { cells++; if (got[i] !== exp[i]) bad.push(tag + "/" + NAMES[i] + " got=" + got[i] + " exp=" + exp[i]); } };
  for (const [key, exp] of Object.entries(C5)) { const [nm, gen] = key.split(",");
    cmp(proj(COMM[IDX[nm]][gen === 'x' ? 0 : 1]), exp, "comm[" + key + "]"); }
  const cA = cells;
  for (const [nm, exp] of Object.entries(T5)) cmp(proj(TH[IDX[nm]]), exp, "theta[" + nm + "]");
  const cB = cells - cA;
  for (const m of [0,1,2,3,4,5,7,11,17,63]) { const S = S5(m), T = sigTab(m);
    for (const nm of Object.keys(S)) cmp(proj(T[IDX[nm]]), S[nm], "sigma[m=" + m + "][" + nm + "]"); }
  const cC = cells - cA - cB;
  for (const m of [0,1,2,3,4,5,6,9,17,31,63]) cmp(proj(emc(m)), E5(m), "E_" + m);
  const cD = cells - cA - cB - cC;
  let dcells = 0;
  for (let n = 0; n < 100; n++) { const a = rndVec(-6,6,true), got = applyTab(TH, secCoords(a)), e = dTh5(proj(a)); dcells += 2;
    if (got[IDX.t5] !== e.t5) bad.push("d_theta/t5"); if (got[IDX.t6] !== e.t6) bad.push("d_theta/t6"); }
  for (const m of [0,1,2,3,5,7,11,17,63]) { const T = sigTab(m);
    for (let n = 0; n < 20; n++) { const a = rndVec(-6,6,true), got = applyTab(T, secCoords(a)), e = dSg5(proj(a), m); dcells += 2;
      if (got[IDX.t5] !== e.t5) bad.push("d_sigma[m=" + m + "]/t5"); if (got[IDX.t6] !== e.t6) bad.push("d_sigma[m=" + m + "]/t6"); } }
  console.log("  照合セル数: 交換子 " + cA + " / theta " + cB + " / sigma " + cC + " / E_m " + cD + " / d_* " + dcells + "  = 合計 " + (cells + dcells));
  chk(bad.length === 0, "** 自己検査 (iii) ** class-5 正本(week4-E2作用表_v1.md)と全 " + (cells + dcells) + " セル一致"
      + (bad.length ? "  -- 不一致 " + bad.length + " 件: " + bad.slice(0,8).join(" ; ") : ""));
}

// ============================================================================
head("9. 第二系統: certificates/e19 の GAP ダンプとの照合");
{
  // スクリプト位置(docs/scout/)から見たリポジトリ直下の certificates/e19/
  const path = decodeURIComponent(new URL("../../certificates/e19/", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
  const MS = [0,1,2,3,5,7,11,17,23,63];
  let ok6 = true, okE6 = true, c6 = 0, cE = 0; const miss6 = [];
  for (const m of MS) {
    let txt; try { txt = fs.readFileSync(path + "gap_system_c6_m" + m + ".txt", "utf8"); } catch (e) { miss6.push(m); continue; }
    const rows = txt.match(/M=([^\n]*)/)[1].trim().split(";").map(r => r.split(",").map(s => BigInt(s.trim())));
    const b = txt.match(/b=([^\n]*)/)[1].trim().split(",").map(s => BigInt(s.trim()));
    const T = sigTab(m), S2 = compTab(T, T), e = emc(m);
    for (let r = 0; r < 15; r++) for (let c = 0; c < 15; c++) { c6++;
      const i = ABAR[r], j = ABAR[c];
      if (rows[r][c] !== (i === j ? 1n : 0n) + TH[j][i]) ok6 = false;
      c6++;
      if (rows[15 + r][c] !== (i === j ? 1n : 0n) + T[j][i] + S2[j][i]) ok6 = false; }
    for (let c = 0; c < 15; c++) { cE += 2; if (b[c] !== 0n) okE6 = false; if (b[15 + c] !== -e[ABAR[c]]) okE6 = false; }
  }
  chk(miss6.length === 0, "E19 c6 ダンプ 10 件が存在(m = " + MS.join(",") + ")");
  chk(ok6, "** 第二系統 ** E19 c6 の 30x15 行列 M(=(1+thetabar) と Nbar)の全 " + c6 + " 成分一致");
  chk(okE6, "** 第二系統 ** E19 c6 の b(=(0, -Ebar_m))の全 " + cE + " 成分一致");
  let ok5 = true, c5 = 0; const miss5 = [];
  for (const m of MS) {
    let txt; try { txt = fs.readFileSync(path + "gap_system_c5_m" + m + ".txt", "utf8"); } catch (e) { miss5.push(m); continue; }
    const rows = txt.match(/M=([^\n]*)/)[1].trim().split(";").map(r => r.split(",").map(s => BigInt(s.trim())));
    const b = txt.match(/b=([^\n]*)/)[1].trim().split(",").map(s => BigInt(s.trim()));
    const T = sigTab(m), S2 = compTab(T, T), e = emc(m);
    for (let r = 0; r < 10; r++) for (let c = 0; c < 10; c++) { c5 += 2;
      if (rows[r][c] !== (r === c ? 1n : 0n) + TH[c][r]) ok5 = false;
      if (rows[10 + r][c] !== (r === c ? 1n : 0n) + T[c][r] + S2[c][r]) ok5 = false; }
    for (let c = 0; c < 10; c++) { c5++; if (b[10 + c] !== -e[c]) ok5 = false; }
  }
  chk(ok5 && miss5.length === 0, "** 第二系統 ** E19 c5 ダンプ(class-5 射影)の全 " + c5 + " 成分一致");
}

// ============================================================================
head("10. 補足: mod 2^j 還元での代表元非依存性");
{
  let ok = true;
  for (let j = 2; j <= 6; j++) { const M = 1n << BigInt(j), Mc = 1n << BigInt(j - 1);
    for (const m of [0,1,5,13,63]) { const T = sigTab(m);
      for (let n = 0; n < 20; n++) { const a = rndVec(0, (1 << j) - 1, true), a2 = a.slice();
        a2[ABAR[Number(rnd(0, 14))]] += M * rnd(-3, 3);
        const g1 = applyTab(T, secCoords(a)), g2 = applyTab(T, secCoords(a2));
        const h1 = applyTab(TH, secCoords(a)), h2 = applyTab(TH, secCoords(a2));
        for (const c of CIDX) { if (((g1[c] - g2[c]) % Mc + Mc) % Mc !== 0n) ok = false;
                                if (((h1[c] - h2[c]) % Mc + Mc) % Mc !== 0n) ok = false; } } } }
  chk(ok, "補題 7.1' 代表元非依存(Abar mod 2^j, C mod 2^{j-1}; j = 2..6 x m 5 種 x 20 例)");
  let dep = false;
  for (let j = 2; j <= 4; j++) { const M = 1n << BigInt(j);
    for (let n = 0; n < 40; n++) { const a = rndVec(0, (1 << j) - 1, true), a2 = a.slice(); a2[IDX.w] += M;
      const g1 = applyTab(sigTab(1), secCoords(a)), g2 = applyTab(sigTab(1), secCoords(a2));
      for (const c of CIDX) if (((g1[c] - g2[c]) % M + M) % M !== 0n) dep = true; } }
  chk(dep, "対照: C を mod 2^j で読むと代表元依存(素朴な有限化は不可)");
}

// ============================================================================
head("11. 実装引き継ぎダンプ(Abar 15x15 行列)");
{
  console.log("  thetabar (15x15, 行 = 像の座標 i, 列 = 入力の座標 j):");
  for (const i of ABAR) console.log("    " + NAMES[i].padEnd(3) + ": " + vec(ABAR.map(j => TH[j][i])));
  console.log("  sigmabar (15x15, C(m,k) 係数ベクトル k=0..4):");
  for (const i of ABAR) console.log("    " + NAMES[i].padEnd(3) + ": " + ABAR.map(j => "[" + SIGPOLY[j][i].join(",") + "]").join(" "));
  // (1 + sigma + sigma^2)|_C  --- 作用表からの一行帰結(本稿は解釈しない)
  console.log("  (1+sigma+sigma^2)|_C  (m 別):");
  for (const m of [0,1,2,3,5,7]) { const T = sigTab(m), T2 = compTab(T, T); const out = [];
    for (const c of CIDX) { const o = new Array(N21).fill(0n);
      for (const cc of CIDX) o[cc] = (c === cc ? 1n : 0n) + T[c][cc] + T2[c][cc];
      out.push(NAMES[c] + "->" + fmtC(o)); }
    console.log("    m=" + m + ": " + out.join(", ")); }
  // 本文 §9.4 に書く一般 m の式そのものを検査
  { let ok = true;
    for (const m of [0,1,2,3,4,5,7,11,17,63,-2,-9]) { const M = BigInt(m), T = sigTab(m), T2 = compTab(T, T);
      const N = {}; for (const c of CIDX) { const o = new Array(N21).fill(0n);
        for (const cc of CIDX) o[cc] = (c === cc ? 1n : 0n) + T[c][cc] + T2[c][cc]; N[c] = o; }
      const E = {};
      E[IDX.t5] = { u1: M+2n, u2: M+2n, u3: M+2n, u4: M-1n };
      E[IDX.t6] = { u1: 1n-M, u2: 1n-M, u3: 1n-M, u4: M+2n };
      E[IDX.u1] = { u1: 2n, u2: 2n, u3: 2n, u4: 0n };
      E[IDX.u2] = { u1: -1n, u2: -1n, u3: -1n, u4: 0n };
      E[IDX.u3] = { u1: 2n, u2: 2n, u3: 2n, u4: 0n };
      E[IDX.u4] = { u1: 0n, u2: 0n, u3: 0n, u4: 3n };
      for (const c of CIDX) { for (const cc of CIDX) {
        const want = (cc === IDX.t5 || cc === IDX.t6) ? 0n : E[c][NAMES[cc]];
        if (N[c][cc] !== want) ok = false; } } }
    chk(ok, "§9.4 の一般 m 式: (1+sigma+sigma^2)|_C の 36 成分(m 12 種)"); }
}

// ============================================================================
head("12. Abar 層の加群記述(閉形)");
// Abar = Z[s^{+-1},t^{+-1}]-加群として w が自由生成(自由メタベリアン、rank 1)。
// S := s-1 (= 作用 [.,x]),  T := t-1 (= 作用 [.,y])。単項式 S^a T^b <-> Hall 基底。
{
  const MAXD = 6;                       // 割り算のために deg <= 6 まで持つ(表示は deg <= 4)
  const MON = [], MI = {};
  for (let d = 0; d <= MAXD; d++) for (let a = d; a >= 0; a--) { const b = d - a; MI[a+","+b] = MON.length; MON.push([a,b]); }
  const NM = MON.length;
  const NAME_OF = {'0,0':'w','1,0':'p','0,1':'q','2,0':'r1','1,1':'r2','0,2':'r3',
                   '3,0':'t1','2,1':'t2','1,2':'t3','0,3':'t4',
                   '4,0':'s1','3,1':'s2','2,2':'s3','1,3':'s4','0,4':'s5'};
  const pz = () => new Array(NM).fill(0n);
  const p1 = () => { const p = pz(); p[MI["0,0"]] = 1n; return p; };
  const padd = (A, B) => { const r = pz(); for (let i = 0; i < NM; i++) r[i] = A[i] + B[i]; return r; };
  const pscal = (c, A) => { const r = pz(); for (let i = 0; i < NM; i++) r[i] = c * A[i]; return r; };
  function pmul(A, B) { const r = pz();
    for (let i = 0; i < NM; i++) { if (A[i] === 0n) continue; const [a1,b1] = MON[i];
      for (let j = 0; j < NM; j++) { if (B[j] === 0n) continue; const [a2,b2] = MON[j];
        if (a1+a2+b1+b2 <= MAXD) r[MI[(a1+a2)+","+(b1+b2)]] += A[i]*B[j]; } }
    return r; }
  const Sp = (() => { const p = pz(); p[MI["1,0"]] = 1n; return p; })();
  const Tp = (() => { const p = pz(); p[MI["0,1"]] = 1n; return p; })();
  const sp = padd(p1(), Sp), tp = padd(p1(), Tp);
  function nilInv(u) { const N = u.slice(); N[MI["0,0"]] -= 1n; let r = p1(), Nk = p1();
    for (let k = 1; k <= MAXD; k++) { Nk = pmul(Nk, N); r = padd(r, pscal(k % 2 ? -1n : 1n, Nk)); } return r; }
  const ppow = (u, n) => { const base = n >= 0 ? u : nilInv(u); let r = p1();
    for (let k = 0; k < Math.abs(n); k++) r = pmul(r, base); return r; };
  function psubst(A, imS, imT) { let r = pz();
    for (let i = 0; i < NM; i++) { if (A[i] === 0n) continue; const [a,b] = MON[i];
      r = padd(r, pscal(A[i], pmul(ppow(imS, a), ppow(imT, b)))); } return r; }
  const toVec = (A) => { const v = new Array(N21).fill(0n);
    for (const key of Object.keys(NAME_OF)) v[IDX[NAME_OF[key]]] = A[MI[key]]; return v; };
  const monVec = (i) => { const A = pz(); A[i] = 1n; return A; };
  const AB15 = Object.keys(NAME_OF);
  // (3.3')  thetabar(lambda . w) = -lambda(t,s) . w
  { let ok = true;
    for (const key of AB15) { const A = monVec(MI[key]), exp = toVec(pscal(-1n, psubst(A, Tp, Sp))), k = IDX[NAME_OF[key]];
      for (const j of ABAR) if (TH[k][j] !== exp[j]) ok = false; }
    chk(ok, "(3.3') thetabar(lambda . w) = -lambda(t,s) . w   (15 基底)"); }
  // (4.4')  sigmabar_m(lambda . w) = lambda(t, s^{-1}t^{-1}) . s^{-1}t^m . w
  { let ok = true;
    const imS = Tp, imT = padd(pmul(nilInv(sp), nilInv(tp)), pscal(-1n, p1()));
    for (const m of [0,1,2,3,5,7,11,-3,-7]) { const Tm = sigTab(m), mult = pmul(nilInv(sp), ppow(tp, m));
      for (const key of AB15) { const A = monVec(MI[key]), exp = toVec(pmul(psubst(A, imS, imT), mult)), k = IDX[NAME_OF[key]];
        for (const j of ABAR) if (Tm[k][j] !== exp[j]) ok = false; } }
    chk(ok, "(4.4') sigmabar_m(lambda . w) = lambda(t, s^{-1}t^{-1}) . s^{-1}t^m . w   (15 基底 x m 9 種)"); }
  // (5.4')  Ebar_m = (1-s)^{-1}( [m]_t - s^{-m}[m]_{st} ) . w
  { const brk = (u, n) => { if (n >= 0) { let r = pz(); for (let k = 0; k < n; k++) r = padd(r, ppow(u, k)); return r; }
      let r = pz(); for (let k = 0; k < -n; k++) r = padd(r, ppow(u, k));
      return pscal(-1n, pmul(ppow(u, n), r)); };          // [n]_u = (1-u^n)/(1-u)
    let ok = true, div = true;
    for (const m of [0,1,2,3,4,5,6,9,17,31,63,-1,-3,-8,-20]) {
      const num = padd(brk(tp, m), pscal(-1n, pmul(ppow(sp, -m), brk(pmul(sp, tp), m))));
      // 1-s = -S。num は S で割り切れるはず。quo = num / S、答は -quo。
      const quo = pz();
      for (let i = 0; i < NM; i++) { if (num[i] === 0n) continue; const [a,b] = MON[i];
        if (a === 0) { div = false; continue; } quo[MI[(a-1)+","+b]] += num[i]; }
      const exp = toVec(pscal(-1n, quo)), v = emc(m);
      for (const j of ABAR) if (v[j] !== exp[j]) ok = false; }
    chk(div, "(5.4') の分子 [m]_t - s^{-m}[m]_{st} が (1-s) で割り切れる");
    chk(ok, "(5.4') Ebar_m = (1-s)^{-1}( [m]_t - s^{-m}[m]_{st} ) . w   (m 15 種)"); }
}

head("検査一覧");
ALLCHK.forEach((s, i) => console.log("  " + String(i + 1).padStart(2) + ". " + s));

console.log("\n============================================");
console.log("pass = " + PASS + "   FAIL = " + FAIL);
if (FAIL) { console.log("failed: " + FAILMSG.join(" | ")); process.exit(1); }
process.exit(0);
