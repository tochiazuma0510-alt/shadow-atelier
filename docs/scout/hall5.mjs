// hall5.mjs -- P^(5) = F_2/gamma_6 の厳密モデル(Magnus 埋め込み)による作用表の検算
// 数学者(Opus 5)2026-07-26。docs/week4-E2作用表_v1.md の全表の独立再計算。
// モデル: 自由結合環 Z<xi,eta>/(deg>=6)。Magnus 埋め込み x=1+xi, y=1+eta は
// 自由群に対して D_n(Z)=gamma_n(Magnus)なので F/gamma_6 上単射。
// 整数演算のみ(BigInt)。外部依存なし。

// ---------- 切断自由結合環 ----------
const DEG = 5;                       // deg > DEG は切り捨て
const zero = () => new Map();
const one  = () => new Map([["", 1n]]);
function addTo(m, w, c) { if (c === 0n) return; const v = (m.get(w) || 0n) + c; if (v === 0n) m.delete(w); else m.set(w, v); }
function add(a, b) { const r = new Map(a); for (const [w, c] of b) addTo(r, w, c); return r; }
function neg(a) { const r = new Map(); for (const [w, c] of a) r.set(w, -c); return r; }
function mul(a, b) {
  const r = new Map();
  for (const [u, cu] of a) for (const [v, cv] of b) { if (u.length + v.length > DEG) continue; addTo(r, u + v, cu * cv); }
  return r;
}
function eq(a, b) { if (a.size !== b.size) return false; for (const [w, c] of a) if ((b.get(w) || 0n) !== c) return false; return true; }
function inv(u) {                    // u = 1 + n, n に定数項なし
  const n = new Map(u); n.delete("");
  if ((u.get("") || 0n) !== 1n) throw new Error("not a unit with constant 1");
  let r = one(), pw = one();
  for (let k = 1; k <= DEG; k++) { pw = mul(pw, neg(n)); r = add(r, pw); }
  return r;
}
const conj = (a, g) => mul(mul(inv(g), a), g);              // a^g = g^-1 a g
const comm = (a, b) => mul(mul(inv(a), inv(b)), mul(a, b)); // [a,b] = a^-1 b^-1 a b
function pow(a, n) {                 // n は BigInt 可(負も)。二進冪
  let e = (typeof n === "bigint") ? n : BigInt(n);
  let base = e < 0n ? inv(a) : a; if (e < 0n) e = -e;
  let r = one();
  while (e > 0n) { if (e & 1n) r = mul(r, base); base = mul(base, base); e >>= 1n; }
  return r;
}
function homo(a, d) { const r = new Map(); for (const [w, c] of a) if (w.length === d) r.set(w, c); return r; }

// ---------- 有理数(小さな線型ソルバ用) ----------
function bgcd(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { [a, b] = [b, a % b]; } return a; }
const Fr = (n, d = 1n) => { if (d < 0n) { n = -n; d = -d; } const g = bgcd(n, d) || 1n; return [n / g, d / g]; };
const fadd = (x, y) => Fr(x[0] * y[1] + y[0] * x[1], x[1] * y[1]);
const fmul = (x, y) => Fr(x[0] * y[0], x[1] * y[1]);
const fsub = (x, y) => fadd(x, [-y[0], y[1]]);
const fdiv = (x, y) => Fr(x[0] * y[1], x[1] * y[0]);

// 列ベクトル cols[k] (Map word->BigInt) の一次結合で target を表す整数係数を返す
function solveInt(cols, target, words) {
  const n = words.length, k = cols.length;
  const M = [];
  for (let i = 0; i < n; i++) {
    const row = [];
    for (let j = 0; j < k; j++) row.push(Fr(cols[j].get(words[i]) || 0n));
    row.push(Fr(target.get(words[i]) || 0n));
    M.push(row);
  }
  let r = 0; const piv = [];
  for (let c = 0; c < k && r < n; c++) {
    let s = -1; for (let i = r; i < n; i++) if (M[i][c][0] !== 0n) { s = i; break; }
    if (s < 0) continue;
    [M[r], M[s]] = [M[s], M[r]];
    const pv = M[r][c];
    for (let j = c; j <= k; j++) M[r][j] = fdiv(M[r][j], pv);
    for (let i = 0; i < n; i++) if (i !== r && M[i][c][0] !== 0n) {
      const f = M[i][c];
      for (let j = c; j <= k; j++) M[i][j] = fsub(M[i][j], fmul(f, M[r][j]));
    }
    piv.push(c); r++;
  }
  for (let i = r; i < n; i++) if (M[i][k][0] !== 0n) throw new Error("inconsistent system");
  const sol = new Array(k).fill(0n);
  for (let i = 0; i < piv.length; i++) {
    const v = M[i][k];
    if (v[1] !== 1n) throw new Error("non-integral solution " + v);
    sol[piv[i]] = v[0];
  }
  if (piv.length < k) throw new Error("columns not independent");
  return sol;
}

// ---------- Hall 基底(X,Y の関数として) ----------
// 順序(正本): w; p,q; r1,r2,r3; t1,t2,t3,t4; t5,t6
const NAMES = ["w", "p", "q", "r1", "r2", "r3", "t1", "t2", "t3", "t4", "t5", "t6"];
const WT    = [ 2,   3,   3,    4,    4,    4,    5,    5,    5,    5,    5,    5 ];
function hallBasis(X, Y) {
  const w = comm(X, Y), p = comm(w, X), q = comm(w, Y);
  const r1 = comm(p, X), r2 = comm(p, Y), r3 = comm(q, Y);
  const t1 = comm(r1, X), t2 = comm(r1, Y), t3 = comm(r2, Y), t4 = comm(r3, Y);
  const t5 = comm(w, p), t6 = comm(w, q);
  return [w, p, q, r1, r2, r3, t1, t2, t3, t4, t5, t6];
}
const xi = new Map([["0", 1n]]), eta = new Map([["1", 1n]]);
const X0 = add(one(), xi), Y0 = add(one(), eta);
const Z0 = inv(mul(X0, Y0));                        // z = (xy)^{-1}
const B = hallBasis(X0, Y0);                        // 正本の基底

// 各重みの単項式リスト
const wordsOf = d => { const out = []; for (let i = 0; i < (1 << d); i++) { let s = ""; for (let j = d - 1; j >= 0; j--) s += ((i >> j) & 1); out.push(s); } return out; };
const LEAD = B.map((g, i) => homo(g, WT[i]));

// ---------- Hall 座標 ----------
function hall(g) {
  const a = new Array(12).fill(0n);
  let h = g;
  for (let d = 2; d <= 5; d++) {
    const idx = []; for (let i = 0; i < 12; i++) if (WT[i] === d) idx.push(i);
    const Hd = homo(h, d);
    const sol = solveInt(idx.map(i => LEAD[i]), Hd, wordsOf(d));
    let pre = one();
    for (let j = 0; j < idx.length; j++) { a[idx[j]] = sol[j]; pre = mul(pre, pow(B[idx[j]], sol[j])); }
    h = mul(inv(pre), h);
  }
  if (!eq(h, one())) throw new Error("hall normal form residue != 1");
  return a;
}
const s = a => { let r = one(); for (let i = 0; i < 12; i++) r = mul(r, pow(B[i], a[i])); return r; };

// ---------- 写像 ----------
const theta_img = hallBasis(Y0, X0);                 // theta: x<->y
const tau_img   = hallBasis(Y0, Z0);                 // tau : x->y->z->x
const sigma_img = m => tau_img.map(g => conj(g, pow(Y0, m)));   // sigma_m = iota_{Y^m} o tau
const Em = m => mul(mul(pow(X0, m), pow(Z0, m)), pow(Y0, m));   // E_m = x^m z^m y^m

// ---------- 多項式補間(m 依存) ----------
function interp(vals) {              // vals[k] = f(k) (BigInt), k=0..N。差分法で整数係数の二項展開
  const d = vals.map(v => [v]); const co = [vals[0]];
  let cur = vals.slice();
  for (let k = 1; k < vals.length; k++) { const nx = []; for (let i = 0; i + 1 < cur.length; i++) nx.push(cur[i + 1] - cur[i]); cur = nx; co.push(cur[0]); }
  while (co.length && co[co.length - 1] === 0n) co.pop();
  return co;                          // f(m) = sum co[k] * binom(m,k)
}
const evalNewton = (co, m) => { let r = 0n, b = 1n; for (let k = 0; k < co.length; k++) { r += co[k] * b; b = b * (BigInt(m) - BigInt(k)) / BigInt(k + 1); } return r; };
// binom(m,k) 基底 -> 単項式 m^j 基底(有理係数)
function newtonToMono(co) {
  let out = [Fr(0n)];
  for (let k = 0; k < co.length; k++) {
    // binom(m,k) = (1/k!) prod_{i=0}^{k-1}(m-i)
    let poly = [Fr(1n)]; let fact = 1n;
    for (let i = 0; i < k; i++) { fact *= BigInt(i + 1); const np = new Array(poly.length + 1).fill(null).map(() => Fr(0n)); for (let j = 0; j < poly.length; j++) { np[j + 1] = fadd(np[j + 1], poly[j]); np[j] = fadd(np[j], fmul(Fr(-BigInt(i)), poly[j])); } poly = np; }
    poly = poly.map(c => fdiv(c, Fr(fact)));
    while (out.length < poly.length) out.push(Fr(0n));
    for (let j = 0; j < poly.length; j++) out[j] = fadd(out[j], fmul(Fr(co[k]), poly[j]));
  }
  while (out.length > 1 && out[out.length - 1][0] === 0n) out.pop();
  return out;
}
function polyStr(mono) {
  const t = [];
  for (let j = mono.length - 1; j >= 0; j--) {
    const [n, d] = mono[j]; if (n === 0n) continue;
    let c = d === 1n ? `${n}` : `${n}/${d}`;
    if (j === 0) t.push(c); else { if (c === "1") c = ""; else if (c === "-1") c = "-"; t.push(`${c}${c && !c.endsWith("/") && c !== "-" ? "*" : ""}m${j > 1 ? "^" + j : ""}`); }
  }
  return t.length ? t.join(" + ").replace(/\+ -/g, "- ") : "0";
}

// ---------- 出力ユーティリティ ----------
const vec = a => "[" + a.map(String).join(",") + "]";
let FAILS = 0;
function check(name, cond, extra = "") { if (!cond) { FAILS++; console.log(`FAIL  ${name} ${extra}`); } else console.log(`pass  ${name}`); }

console.log("=== 0. モデルの健全性 ===");
check("hall(w)=e_w", vec(hall(B[0])) === vec([1n, 0n, 0n, 0n, 0n, 0n, 0n, 0n, 0n, 0n, 0n, 0n]));
for (let i = 0; i < 12; i++) { const a = new Array(12).fill(0n); a[i] = 1n; check(`hall(${NAMES[i]})=e_${NAMES[i]}`, vec(hall(B[i])) === vec(a)); }

console.log("\n=== 1. P 内の交換子表(基底 x 生成元) ===");
for (let i = 0; i < 12; i++) {
  const cx = hall(comm(B[i], X0)), cy = hall(comm(B[i], Y0));
  console.log(`[${NAMES[i]},x] = ${vec(cx)}   [${NAMES[i]},y] = ${vec(cy)}`);
}
console.log("\n--- A 内の交換子表(全 12x12 対・非自明のみ) ---");
for (let i = 0; i < 12; i++) for (let j = 0; j < 12; j++) {
  const c = hall(comm(B[i], B[j]));
  if (c.some(v => v !== 0n)) console.log(`[${NAMES[i]},${NAMES[j]}] = ${vec(c)}`);
}

console.log("\n=== 2. collection 公式の検査 ===");
// H(a)H(b) = H(a+b - a_p b_w e5 - a_q b_w e6)
{
  let ok = true;
  const rnd = () => BigInt(Math.floor(Math.random() * 9) - 4);
  for (let trial = 0; trial < 200; trial++) {
    const a = Array.from({ length: 12 }, rnd), b = Array.from({ length: 12 }, rnd);
    const lhs = hall(mul(s(a), s(b)));
    const rhs = a.map((v, i) => v + b[i]); rhs[10] -= a[1] * b[0]; rhs[11] -= a[2] * b[0];
    if (vec(lhs) !== vec(rhs)) { ok = false; console.log("  counterexample", vec(a), vec(b), vec(lhs), vec(rhs)); break; }
  }
  check("積公式 H(a)H(b)=H(a+b-(a_p b_w)t5-(a_q b_w)t6) (200 ランダム)", ok);
  // 冪公式
  let ok2 = true;
  for (let trial = 0; trial < 60; trial++) {
    const a = Array.from({ length: 12 }, rnd); const n = BigInt(Math.floor(Math.random() * 11) - 5);
    const lhs = hall(pow(s(a), n));
    const bn = n * (n - 1n) / 2n;
    const rhs = a.map(v => n * v); rhs[10] -= bn * a[1] * a[0]; rhs[11] -= bn * a[2] * a[0];
    if (vec(lhs) !== vec(rhs)) { ok2 = false; console.log("  cf", vec(a), n, vec(lhs), vec(rhs)); break; }
  }
  check("冪公式 H(a)^n=H(na-C(n,2)(a_p a_w, a_q a_w))", ok2);
  // c_s の指定値
  const ew = new Array(12).fill(0n); ew[0] = 1n; const ep = new Array(12).fill(0n); ep[1] = 1n;
  const cwp = hall(mul(mul(s(ew), s(ep)), inv(s(ew.map((v, i) => v + ep[i])))));
  const cpw = hall(mul(mul(s(ep), s(ew)), inv(s(ep.map((v, i) => v + ew[i])))));
  check("c_s(w,p)=0", vec(cwp) === vec(new Array(12).fill(0n)), vec(cwp));
  const m1 = new Array(12).fill(0n); m1[10] = -1n;
  check("c_s(p,w)=-t5", vec(cpw) === vec(m1), vec(cpw));
}

console.log("\n=== 3. theta の full-A 作用表 ===");
const TH = theta_img.map(hall);
for (let i = 0; i < 12; i++) console.log(`theta(${NAMES[i]}) = ${vec(TH[i])}`);
check("theta^2 = id", hallBasis(X0, Y0).every((g, i) => eq(g, B[i])) &&
  (() => { // theta を Hall 座標上で二回適用
    const apply = a => { let r = one(); for (let i = 0; i < 12; i++) r = mul(r, pow(theta_img[i], a[i])); return hall(r); };
    for (let i = 0; i < 12; i++) { const e = new Array(12).fill(0n); e[i] = 1n; if (vec(apply(TH[i])) !== vec(e)) return false; } return true;
  })());

console.log("\n=== 4. sigma_m の full-A 作用表(m 多項式) ===");
const MS = 12;                                   // m = 0..MS で補間
const SG = [];
for (let m = 0; m <= MS; m++) SG.push(sigma_img(m).map(hall));
const sigmaPoly = [];                            // sigmaPoly[i][j] = sigma(e_i) の j 座標(newton 係数)
for (let i = 0; i < 12; i++) {
  const row = [];
  for (let j = 0; j < 12; j++) row.push(interp(SG.map(t => t[i][j])));
  sigmaPoly.push(row);
}
for (let i = 0; i < 12; i++) {
  const parts = [];
  for (let j = 0; j < 12; j++) { const pstr = polyStr(newtonToMono(sigmaPoly[i][j])); if (pstr !== "0") parts.push(`(${pstr})*${NAMES[j]}`); }
  console.log(`sigma(${NAMES[i]}) = ${parts.join(" + ") || "0"}`);
}
{ // 補間の外挿検査
  let ok = true;
  for (const m of [13, 20, 33, -1, -5, -12]) {
    const act = sigma_img(m).map(hall);
    for (let i = 0; i < 12; i++) for (let j = 0; j < 12; j++)
      if (evalNewton(sigmaPoly[i][j], m) !== act[i][j]) { ok = false; console.log(`  mismatch m=${m} ${NAMES[i]}->${NAMES[j]}`); }
  }
  check("sigma 多項式の外挿(m=13,20,33,-1,-5,-12)", ok);
}

console.log("\n=== 5. E_m の Hall 座標(m 多項式) ===");
const EH = []; for (let m = 0; m <= MS; m++) EH.push(hall(Em(m)));
const EPoly = []; for (let j = 0; j < 12; j++) EPoly.push(interp(EH.map(t => t[j])));
for (let j = 0; j < 12; j++) console.log(`E_m[${NAMES[j]}] = ${polyStr(newtonToMono(EPoly[j]))}`);
{
  let ok = true;
  for (const m of [13, 20, 33, -1, -5, -12]) { const a = hall(Em(m)); for (let j = 0; j < 12; j++) if (evalNewton(EPoly[j], m) !== a[j]) { ok = false; console.log(`  mismatch m=${m} ${NAMES[j]}`); } }
  check("E_m 多項式の外挿", ok);
  // sigma(E_m) = E_m :  tau(E_m) = tau(x^m z^m y^m) = y^m x^m z^m
  let ok2 = true;
  for (let m = 0; m <= 10; m++) {
    const tauE = mul(mul(pow(Y0, m), pow(X0, m)), pow(Z0, m));
    if (!eq(conj(tauE, pow(Y0, m)), Em(m))) { ok2 = false; console.log(`  sigma(E_m)!=E_m at m=${m}`); }
  }
  check("sigma(E_m)=E_m (m=0..10, P^(5) 内で厳密)", ok2);
  // 二項係数閉形:  Ebar_m の S^a T^b 係数 = (-1)^{d+b+1} C(m+1+a, d+2)
  const AB = [[0, 0], [1, 0], [0, 1], [2, 0], [1, 1], [0, 2], [3, 0], [2, 1], [1, 2], [0, 3]];
  const binom = (m, k) => { let r = 1n, M = BigInt(m); for (let i = 0; i < k; i++) r = r * (M - BigInt(i)) / BigInt(i + 1); return r; };
  let ok3 = true;
  for (const m of [0, 1, 2, 3, 4, 7, 13, 40, 63]) {
    const e = hall(Em(m));
    for (let j = 0; j < 10; j++) {
      const [a, b] = AB[j], d = a + b;
      const pred = ((d + b + 1) % 2 === 0 ? 1n : -1n) * binom(m + 1 + a, d + 2);
      if (pred !== e[j]) { ok3 = false; console.log(`  binom closed form mismatch m=${m} ${NAMES[j]}: ${pred} vs ${e[j]}`); }
    }
    // eps_m の閉形
    const p5 = BigInt(m) * BigInt(m + 1) * BigInt(m + 2) * (6n * BigInt(m) * BigInt(m) + 7n * BigInt(m) + 7n) / 120n;
    const p6 = -BigInt(m - 1) * BigInt(m) * BigInt(m + 1) * (3n * BigInt(m) * BigInt(m) + 8n) / 120n;
    if (p5 !== e[10] || p6 !== e[11]) { ok3 = false; console.log(`  eps closed form mismatch m=${m}: ${p5},${p6} vs ${e[10]},${e[11]}`); }
  }
  check("Ebar_m の二項閉形と eps_m の因数分解形", ok3);
  console.log("  E_m の 12 座標(m=0..6):");
  for (let m = 0; m <= 6; m++) console.log(`    m=${m}: ${vec(hall(Em(m)))}`);
}

console.log("\n=== 6. 欠損 d_theta, d_sigma, eps_m(基底上) ===");
// d_phi(e_k) = phi(e_k) の C 成分(Abar 成分は phi-bar(e_k))
const dTheta = TH.map(a => [a[10], a[11]]);
for (let i = 0; i < 10; i++) console.log(`d_theta(${NAMES[i]}) = ${dTheta[i][0]}*t5 + ${dTheta[i][1]}*t6`);
console.log("(参考) d_theta(t5),d_theta(t6) =", vec(dTheta[10]), vec(dTheta[11]));
for (let i = 0; i < 10; i++) {
  const c5 = polyStr(newtonToMono(sigmaPoly[i][10])), c6 = polyStr(newtonToMono(sigmaPoly[i][11]));
  console.log(`d_sigma(${NAMES[i]}) = (${c5})*t5 + (${c6})*t6`);
}
console.log(`eps_m = (${polyStr(newtonToMono(EPoly[10]))})*t5 + (${polyStr(newtonToMono(EPoly[11]))})*t6`);

console.log("\n=== 7. 二次閉形の検査 ===");
// d_phi(a) = sum a_k d_phi(e_k) - sum C(a_k,2) delta(phi_bar e_k) - sum_{j<k} a_j a_k kappa(phi_bar e_j, phi_bar e_k)
function closedForm(imgs, a) {           // imgs[k] = phi(e_k) の 12 座標(k=0..9 のみ使用)
  let c5 = 0n, c6 = 0n;
  for (let k = 0; k < 10; k++) {
    c5 += a[k] * imgs[k][10]; c6 += a[k] * imgs[k][11];
    const b2 = a[k] * (a[k] - 1n) / 2n;
    c5 -= b2 * imgs[k][1] * imgs[k][0]; c6 -= b2 * imgs[k][2] * imgs[k][0];
  }
  for (let j = 0; j < 10; j++) for (let k = j + 1; k < 10; k++) {
    c5 -= a[j] * a[k] * imgs[j][1] * imgs[k][0];
    c6 -= a[j] * a[k] * imgs[j][2] * imgs[k][0];
  }
  return [c5, c6];
}
{
  const rnd = () => BigInt(Math.floor(Math.random() * 9) - 4);
  const applyPhi = (imgs, a) => { let r = one(); for (let k = 0; k < 10; k++) r = mul(r, pow(imgsG[k], a[k])); return hall(r); };
  let imgsG = theta_img;
  let ok = true;
  for (let trial = 0; trial < 120; trial++) {
    const a = Array.from({ length: 10 }, rnd).concat([0n, 0n]);
    const lhs = applyPhi(theta_img, a);                       // theta(s(a)) の Hall 座標
    const abar = lhs.slice(0, 10);
    const d = closedForm(TH, a);
    // s(abar) の C 成分は 0 なので d_theta(a) = lhs の C 成分
    if (lhs[10] !== d[0] || lhs[11] !== d[1]) { ok = false; console.log("  theta closed-form mismatch", vec(a), vec(lhs), d.map(String)); break; }
  }
  check("d_theta の二次閉形(120 ランダム)", ok);

  let ok2 = true;
  for (const m of [0, 1, 2, 3, 5, 7, 11, 17]) {
    const si = sigma_img(m); const SH = si.map(hall); imgsG = si;
    for (let trial = 0; trial < 25; trial++) {
      const a = Array.from({ length: 10 }, rnd).concat([0n, 0n]);
      const lhs = applyPhi(si, a);
      const d = closedForm(SH, a);
      if (lhs[10] !== d[0] || lhs[11] !== d[1]) { ok2 = false; console.log(`  sigma closed-form mismatch m=${m}`, vec(a)); break; }
    }
    if (!ok2) break;
  }
  check("d_sigma の二次閉形(m=0,1,2,3,5,7,11,17 x 25 ランダム)", ok2);
}

console.log("\n=== 8. cocycle 式 (2)(3)(4) の検査 ===");
// q_theta(f) = c_s(theta_bar f, f) + d_theta(f) ;  q_N(f) = eps + d_sigma2 + d_sigma + 3 つの c_s
function csC(a, b) { return [-a[1] * b[0], -a[2] * b[0]]; }
{
  const thBar = i => TH[i].slice(0, 10);
  // L に入る f を作るのは面倒なので、恒等式そのものを一般の f で検査する
  // q_theta(f) := theta(s f) * s f。一般には Abar 成分 (1+theta)f が残るので、
  // C 成分だけを取り出して比較する(Hall 座標の t5,t6 欄)。
  const rnd = () => BigInt(Math.floor(Math.random() * 9) - 4);
  const applyBar = (M, a) => { const r = new Array(10).fill(0n); for (let k = 0; k < 10; k++) for (let j = 0; j < 10; j++) r[j] += a[k] * M[k][j]; return r; };
  const THbar = TH.map(v => v.slice(0, 10));
  let ok = true;
  for (let trial = 0; trial < 120; trial++) {
    const a = Array.from({ length: 10 }, rnd).concat([0n, 0n]);
    let thsa = one(); for (let k = 0; k < 10; k++) thsa = mul(thsa, pow(theta_img[k], a[k]));
    const prod = hall(mul(thsa, s(a)));                 // theta(s a) * s a
    const ta = applyBar(THbar, a.slice(0, 10));
    // 予測: Abar 成分 = ta + a、C 成分 = c_s(ta, a) + d_theta(a)
    const d = closedForm(TH, a); const c = csC(ta, a);
    const pred5 = c[0] + d[0], pred6 = c[1] + d[1];
    for (let j = 0; j < 10; j++) if (prod[j] !== ta[j] + a[j]) { ok = false; }
    if (prod[10] !== pred5 || prod[11] !== pred6) { ok = false; console.log("  q_theta mismatch", vec(a), vec(prod), pred5, pred6); break; }
  }
  check("q_theta = c_s(theta f, f) + d_theta(f) (一般 f・120 ランダム)", ok);

  let ok2 = true;
  for (const m of [0, 1, 2, 3, 5, 7]) {
    const si = sigma_img(m), SH = si.map(hall), SBar = SH.map(v => v.slice(0, 10));
    const eH = hall(Em(m)); const ebar = eH.slice(0, 10), eps = [eH[10], eH[11]];
    const sigC = z => [-z[1], z[0] - z[1]];              // sigma|_C: t5->t6, t6->-t5-t6
    for (let trial = 0; trial < 25; trial++) {
      const a = Array.from({ length: 10 }, rnd).concat([0n, 0n]);
      // 実際の値
      let s1 = one(); for (let k = 0; k < 10; k++) s1 = mul(s1, pow(si[k], a[k]));       // sigma(s a)
      const s1h = hall(s1);
      let s2 = one(); for (let k = 0; k < 12; k++) s2 = mul(s2, pow(si[k], s1h[k]));     // sigma^2(s a)
      const actual = hall(mul(mul(mul(Em(m), s2), s1), s(a)));
      // 予測
      const Sa = applyBar(SBar, a.slice(0, 10));
      const S2a = applyBar(SBar, Sa);
      const dS = closedForm(SH, a);
      const dS_Sa = closedForm(SH, Sa.concat([0n, 0n]));
      const dS2 = [dS_Sa[0] + sigC(dS)[0], dS_Sa[1] + sigC(dS)[1]];
      const c1 = csC(ebar, S2a);
      const u1 = ebar.map((v, i) => v + S2a[i]);
      const c2 = csC(u1, Sa);
      const u2 = u1.map((v, i) => v + Sa[i]);
      const c3 = csC(u2, a.slice(0, 10));
      const pred = [eps[0] + dS2[0] + dS[0] + c1[0] + c2[0] + c3[0],
                    eps[1] + dS2[1] + dS[1] + c1[1] + c2[1] + c3[1]];
      const predBar = u2.map((v, i) => v + a[i]);
      for (let j = 0; j < 10; j++) if (actual[j] !== predBar[j]) { ok2 = false; console.log("  qN Abar mismatch", m, vec(a)); }
      if (actual[10] !== pred[0] || actual[11] !== pred[1]) { ok2 = false; console.log("  qN C mismatch", m, vec(a), vec(actual), pred.map(String)); break; }
    }
    if (!ok2) break;
  }
  check("q_N = eps_m + d_sigma2 + d_sigma + 3 c_s (一般 f・m=0,1,2,3,5,7)", ok2);
}

console.log("\n=== 9. 構造事実の再現 ===");
{
  const sigC = z => [-z[1], z[0] - z[1]], thC = z => [z[1], z[0]];
  // sigma|_C, theta|_C を実測から
  const s5 = sigma_img(0).map(hall); // sigma(t5), sigma(t6)
  console.log("sigma(t5) =", vec(s5[10].slice(10)), " sigma(t6) =", vec(s5[11].slice(10)));
  console.log("theta(t5) =", vec(TH[10].slice(10)), " theta(t6) =", vec(TH[11].slice(10)));
  let okN = true;
  for (const m of [0, 1, 2, 3, 7, 13]) {
    const si = sigma_img(m).map(hall);
    for (const i of [10, 11]) {
      const z = [si[i][10], si[i][11]];
      const z2 = [si[10][10] * z[0] + si[11][10] * z[1], si[10][11] * z[0] + si[11][11] * z[1]];
      if (z2[0] + z[0] + (i === 10 ? 1n : 0n) !== 0n || z2[1] + z[1] + (i === 11 ? 1n : 0n) !== 0n) okN = false;
    }
  }
  check("N_C = 1+sigma+sigma^2 = 0 on C (m=0,1,2,3,7,13)", okN);
  // im Lambda = <(t5+t6, 0)>
  const L = [];
  for (const z of [[1n, 0n], [0n, 1n]]) L.push([[z[0] + thC(z)[0], z[1] + thC(z)[1]], [0n, 0n]]);
  console.log("Lambda(t5) =", JSON.stringify(L[0].map(v => v.map(String))), " Lambda(t6) =", JSON.stringify(L[1].map(v => v.map(String))));
  check("im Lambda = <(t5+t6,0)>", L[0][0][0] === 1n && L[0][0][1] === 1n && L[1][0][0] === 1n && L[1][0][1] === 1n && L[0][1].every(v => v === 0n));
}

console.log("\n=== 10. E19 c=5 ダンプとの b 整合 ===");
{
  const fs = await import("node:fs");
  const dir = "C:/Users/81905/Desktop/shadow-atelier/certificates/e19/";
  let ok = true, tested = 0;
  for (const m of [0, 1, 2, 3, 5, 7, 11, 17, 23, 63]) {
    const f = dir + `gap_system_c5_m${m}.txt`;
    if (!fs.existsSync(f)) { console.log(`  (skip m=${m}: no dump)`); continue; }
    const txt = fs.readFileSync(f, "utf8");
    const bline = txt.split("\n").find(l => l.startsWith("b="));
    const b = bline.slice(2).trim().split(",").map(v => BigInt(v));
    const e = hall(Em(m)).slice(0, 10);
    const pred = e.map(v => -v);                     // b の後半 = -Ebar_m
    const got = b.slice(10);
    tested++;
    if (vec(pred) !== vec(got)) { ok = false; console.log(`  m=${m}  mine(-Ebar)=${vec(pred)}  dump=${vec(got)}`); }
    else console.log(`  m=${m}  -Ebar_m = ${vec(got)}  OK`);
  }
  check(`E19 c=5 b ベクトル整合(${tested} 件)`, ok);
  // N-block(列 1 = kappa_m)の照合
  let ok2 = true;
  for (const m of [0, 1, 3, 7]) {
    const f = dir + `gap_system_c5_m${m}.txt`;
    if (!fs.existsSync(f)) continue;
    const txt = fs.readFileSync(f, "utf8");
    const Mline = txt.split("\n").find(l => l.startsWith("M="));
    const rows = Mline.slice(2).trim().split(";").map(r => r.split(",").map(v => BigInt(v)));
    // kappa_m = N(w) = M の行 11..20 の第 1 列
    const kap = rows.slice(10).map(r => r[0]);
    // 自前: N(w) = sigma^2(w)+sigma(w)+w の Abar 成分
    const si = sigma_img(m), SH = si.map(hall), SBar = SH.map(v => v.slice(0, 10));
    const applyBar = a => { const r = new Array(10).fill(0n); for (let k = 0; k < 10; k++) for (let j = 0; j < 10; j++) r[j] += a[k] * SBar[k][j]; return r; };
    const e1 = new Array(10).fill(0n); e1[0] = 1n;
    const S1 = applyBar(e1), S2 = applyBar(S1);
    const N = e1.map((v, i) => v + S1[i] + S2[i]);
    if (vec(N) !== vec(kap)) { ok2 = false; console.log(`  kappa mismatch m=${m}: mine=${vec(N)} dump=${vec(kap)}`); }
    else console.log(`  m=${m}  kappa_m = ${vec(N)}  OK`);
  }
  check("E19 c=5 N ブロック第 1 列(kappa_m)整合", ok2);
}

console.log("\n=== 11. 欠損の明示閉形(文書 §4 の式) ===");
{
  const rnd = () => BigInt(Math.floor(Math.random() * 13) - 6);
  // d_theta(a) = -(a_q + a_r2 + a_t3) t5 - (a_p + a_r2 + a_t2) t6   (線型・m 非依存)
  let ok = true;
  for (let trial = 0; trial < 300; trial++) {
    const a = Array.from({ length: 10 }, rnd).concat([0n, 0n]);
    let g = one(); for (let k = 0; k < 10; k++) g = mul(g, pow(theta_img[k], a[k]));
    const h = hall(g);
    const p5 = -(a[2] + a[4] + a[8]), p6 = -(a[1] + a[4] + a[7]);
    if (h[10] !== p5 || h[11] !== p6) { ok = false; console.log("  d_theta explicit mismatch", vec(a), h[10], h[11], p5, p6); break; }
  }
  check("d_theta(a) = -(a_q+a_r2+a_t3)t5 - (a_p+a_r2+a_t2)t6  (線型・300 ランダム)", ok);
  // d_sigma(a) = [-a_q+a_r2-3a_r3+a_t3-2a_t4 + C(a_w,2)] t5 + [-a_r3-a_t2+a_t3-a_t4 - m C(a_w,2)] t6
  let ok2 = true;
  for (const m of [0, 1, 2, 3, 5, 7, 11, 17, 63]) {
    const si = sigma_img(m);
    for (let trial = 0; trial < 40; trial++) {
      const a = Array.from({ length: 10 }, rnd).concat([0n, 0n]);
      let g = one(); for (let k = 0; k < 10; k++) g = mul(g, pow(si[k], a[k]));
      const h = hall(g);
      const b2 = a[0] * (a[0] - 1n) / 2n;
      const p5 = -a[2] + a[4] - 3n * a[5] + a[8] - 2n * a[9] + b2;
      const p6 = -a[5] - a[7] + a[8] - a[9] - BigInt(m) * b2;
      if (h[10] !== p5 || h[11] !== p6) { ok2 = false; console.log(`  d_sigma explicit mismatch m=${m}`, vec(a), h[10], h[11], p5, p6); break; }
    }
    if (!ok2) break;
  }
  check("d_sigma(a) の明示閉形(9 個の m x 40 ランダム)", ok2);
}

console.log("\n=== 12. 大域整合(sigma^3 = Inn(E_m)・命題 E1) ===");
{
  // A 上の写像を Hall 座標で合成するためのヘルパ
  const applyMap = (imgs, a) => { let r = one(); for (let k = 0; k < 12; k++) r = mul(r, pow(imgs[k], a[k])); return hall(r); };
  let ok = true, ok2 = true;
  for (const m of [0, 1, 2, 3, 5, 7]) {
    const si = sigma_img(m), SH = si.map(hall);
    const E = Em(m);
    for (let i = 0; i < 12; i++) {
      const e = new Array(12).fill(0n); e[i] = 1n;
      const s3 = applyMap(si, applyMap(si, SH[i]));
      const innR = hall(conj(B[i], E));       // E^{-1} b E
      if (vec(s3) !== vec(innR)) { ok = false; console.log(`  sigma^3 != Inn(E_m) at m=${m}, ${NAMES[i]}: ${vec(s3)} vs ${vec(innR)}`); break; }
    }
    // 命題 E1: theta sigma theta = iota_{X^u} sigma^{-1},  u = 2m+1
    const u = 2 * m + 1;
    // sigma^{-1} を Hall 座標で: sigma の 12x12 行列(下三角ではないので直接解く)
    const invSigma = (() => {
      // sigma は A の自己同型。基底像の行列(下三角ブロック)を反転する
      const Mx = SH; // Mx[k] = sigma(e_k) の座標
      // 逐次解法: 重み順に解く
      return a => {
        let target = a.slice(), res = new Array(12).fill(0n);
        for (let k = 0; k < 12; k++) {
          // 重み昇順に、先頭非零座標から決める
          const lead = Mx[k].findIndex(v => v !== 0n);
        }
        // 汎用: 12x12 整数線型系を有理ソルバで解く
        const cols = Mx.map(v => new Map(v.map((c, j) => [String(j), c]).filter(([, c]) => c !== 0n)));
        const tgt = new Map(a.map((c, j) => [String(j), c]).filter(([, c]) => c !== 0n));
        return solveInt(cols, tgt, Array.from({ length: 12 }, (_, j) => String(j)));
      };
    })();
    for (let i = 0; i < 12; i++) {
      const lhs = applyMap(theta_img, applyMap(si, TH[i]));         // theta(sigma(theta(e_i)))
      const rhs = hall(conj(s(invSigma(new Array(12).fill(0n).map((_, j) => j === i ? 1n : 0n))), pow(X0, u)));
      if (vec(lhs) !== vec(rhs)) { ok2 = false; console.log(`  E1 mismatch m=${m}, ${NAMES[i]}: ${vec(lhs)} vs ${vec(rhs)}`); break; }
    }
    if (!ok || !ok2) break;
  }
  check("sigma^3 = Inn_A(E_m)  (m=0,1,2,3,5,7・全 12 基底)", ok);
  check("命題 E1: theta sigma theta = iota_{X^u} sigma^{-1}, u=2m+1  (全 12 基底)", ok2);
}

console.log("\n=== 13. E19 c=5 行列 M 全体との照合 ===");
{
  const fs = await import("node:fs");
  const dir = "C:/Users/81905/Desktop/shadow-atelier/certificates/e19/";
  let ok = true, tested = 0;
  for (const m of [0, 1, 2, 3, 5, 7, 11, 17, 23, 63]) {
    const f = dir + `gap_system_c5_m${m}.txt`;
    if (!fs.existsSync(f)) continue;
    const txt = fs.readFileSync(f, "utf8");
    const rows = txt.split("\n").find(l => l.startsWith("M=")).slice(2).trim().split(";").map(r => r.split(",").map(v => BigInt(v)));
    const THbar = TH.map(v => v.slice(0, 10));
    const SBar = sigma_img(m).map(hall).map(v => v.slice(0, 10));
    const app = (M, a) => { const r = new Array(10).fill(0n); for (let k = 0; k < 10; k++) for (let j = 0; j < 10; j++) r[j] += a[k] * M[k][j]; return r; };
    for (let k = 0; k < 10; k++) {
      const e = new Array(10).fill(0n); e[k] = 1n;
      const th = app(THbar, e).map((v, i) => v + e[i]);            // (1+thetabar) e_k
      const S1 = app(SBar, e), S2 = app(SBar, S1);
      const N = e.map((v, i) => v + S1[i] + S2[i]);                // Nbar e_k
      for (let j = 0; j < 10; j++) {
        if (rows[j][k] !== th[j]) { ok = false; console.log(`  (1+theta) mismatch m=${m} row${j} col${k}: ${rows[j][k]} vs ${th[j]}`); }
        if (rows[10 + j][k] !== N[j]) { ok = false; console.log(`  N mismatch m=${m} row${j} col${k}: ${rows[10 + j][k]} vs ${N[j]}`); }
      }
    }
    tested++;
  }
  check(`E19 c=5 の 20x10 行列 M 全成分一致(${tested} 個の m)`, ok);
}

console.log("\n=== 14. 文書掲載用の行列ダンプ ===");
{
  console.log("thetabar (10x10, 行 = 像の座標, 列 = 入力基底):");
  for (let j = 0; j < 10; j++) console.log("  " + Array.from({ length: 10 }, (_, k) => String(TH[k][j])).join(","));
  for (const m of [0, 1, 2]) {
    const SB = sigma_img(m).map(hall);
    console.log(`sigmabar (m=${m}):`);
    for (let j = 0; j < 10; j++) console.log("  " + Array.from({ length: 10 }, (_, k) => String(SB[k][j])).join(","));
  }
}

console.log("\n=== 15. 有限商 A_j への降下(代表元非依存性) ===");
{
  // 主張: Abar 座標を mod 2^j、C 座標を mod 2^{j-1} で読むと、c_s / d_theta / d_sigma は
  // 代表元の取り方に依らない。鍵は  C(a+2^j,2) - C(a,2) = 2^j a + 2^{j-1}(2^j-1) ≡ 0 (mod 2^{j-1})。
  let ok = true;
  const rnd = () => BigInt(Math.floor(Math.random() * 13) - 6);
  for (let j = 1; j <= 6; j++) {
    const Mj = 1n << BigInt(j), Cj = 1n << BigInt(j - 1);
    for (const m of [0, 1, 5, 13, 63]) {
      for (let trial = 0; trial < 30; trial++) {
        const a = Array.from({ length: 10 }, rnd);
        const k = Math.floor(Math.random() * 10);
        const a2 = a.slice(); a2[k] += Mj * BigInt(Math.floor(Math.random() * 5) - 2);
        const dth = v => [-(v[2] + v[4] + v[8]), -(v[1] + v[4] + v[7])];
        const b2 = v => v[0] * (v[0] - 1n) / 2n;
        const dsg = v => [-v[2] + v[4] - 3n * v[5] + v[8] - 2n * v[9] + b2(v),
                          -v[5] - v[7] + v[8] - v[9] - BigInt(m) * b2(v)];
        const md = (u, v) => ((u - v) % Cj + Cj) % Cj === 0n;
        if (!md(dth(a)[0], dth(a2)[0]) || !md(dth(a)[1], dth(a2)[1])) { ok = false; console.log(`  d_theta not well-defined j=${j}`); }
        if (!md(dsg(a)[0], dsg(a2)[0]) || !md(dsg(a)[1], dsg(a2)[1])) { ok = false; console.log(`  d_sigma not well-defined j=${j} m=${m} k=${k}`, vec(a), vec(a2)); }
        // c_s も
        const b = Array.from({ length: 10 }, rnd);
        const cs = (u, v) => [-u[1] * v[0], -u[2] * v[0]];
        if (!md(cs(a, b)[0], cs(a2, b)[0]) || !md(cs(a, b)[1], cs(a2, b)[1])) { ok = false; console.log(`  c_s not well-defined j=${j}`); }
      }
    }
  }
  check("c_s / d_theta / d_sigma は A_j(Abar mod 2^j, C mod 2^{j-1})で代表元非依存", ok);
  // 反例側: C を mod 2^j で読むと壊れる(v3 §1.1 の再現)
  let broken = false;
  for (let j = 2; j <= 4; j++) {
    const Mj = 1n << BigInt(j);
    const b2 = v => v * (v - 1n) / 2n;
    for (let a = 0n; a < 8n; a++) if ((b2(a + Mj) - b2(a)) % Mj !== 0n) broken = true;
  }
  check("(対照) C を mod 2^j で読むと C(a,2) 項が代表元依存になる", broken);
}

console.log("\n=== 16. Hall-Witt 恒等式(文書の導出で使う形) ===");
{
  // [[a,b],c^a] [[c,a],b^c] [[b,c],a^b] = 1
  let ok = true;
  const rnd = () => { let g = one(); for (let i = 0; i < 3; i++) g = mul(g, pow(Math.random() < 0.5 ? X0 : Y0, BigInt(Math.floor(Math.random() * 5) - 2))); return g; };
  for (let t = 0; t < 40; t++) {
    const a = rnd(), b = rnd(), c = rnd();
    const L = mul(mul(comm(comm(a, b), conj(c, a)), comm(comm(c, a), conj(b, c))), comm(comm(b, c), conj(a, b)));
    if (!eq(L, one())) { ok = false; break; }
  }
  check("[[a,b],c^a][[c,a],b^c][[b,c],a^b] = 1 (P^(5) 内・40 ランダム)", ok);
  console.log("  導出の帰結: [q,x] = r2 t5 t6,  [r2,x] = t2 t5,  [r3,x] = t3 t6");
  const chk = (g, exp) => vec(hall(g)) === vec(exp);
  const E = i => { const v = new Array(12).fill(0n); for (const [k, c] of i) v[k] = c; return v; };
  check("[q,x] = r2+t5+t6", chk(comm(B[2], X0), E([[4, 1n], [10, 1n], [11, 1n]])));
  check("[r2,x] = t2+t5", chk(comm(B[4], X0), E([[7, 1n], [10, 1n]])));
  check("[r3,x] = t3+t6", chk(comm(B[5], X0), E([[8, 1n], [11, 1n]])));
}

console.log("\n=== 17. q_theta の明示閉形 ===");
{
  // q_theta(f) = (f_w f_q - f_q - f_r2 - f_t3) t5 + (f_w f_p - f_p - f_r2 - f_t2) t6
  // (f が L に入るとき。一般の f では Abar 成分 (1+thetabar)f が残るが C 成分は同じ式)
  let ok = true;
  const rnd = () => BigInt(Math.floor(Math.random() * 13) - 6);
  for (let t = 0; t < 200; t++) {
    const a = Array.from({ length: 10 }, rnd).concat([0n, 0n]);
    let g = one(); for (let k = 0; k < 10; k++) g = mul(g, pow(theta_img[k], a[k]));
    const prod = hall(mul(g, s(a)));
    const p5 = a[0] * a[2] - a[2] - a[4] - a[8];
    const p6 = a[0] * a[1] - a[1] - a[4] - a[7];
    if (prod[10] !== p5 || prod[11] !== p6) { ok = false; console.log("  mismatch", vec(a), prod[10], prod[11], p5, p6); break; }
  }
  check("q_theta = (f_w f_q - f_q - f_r2 - f_t3)t5 + (f_w f_p - f_p - f_r2 - f_t2)t6", ok);
  // 旧実装(誤り)の式との差
  console.log("  誤実装 c_s^code(a,b)=(a_w b_p, a_w b_q) は q_theta = -f_w f_p t5 - f_w f_q t6 を与える");
  console.log("  差 = (f_w f_q + f_w f_p - f_q - f_r2 - f_t3) t5 + (f_w f_p + f_w f_q - f_p - f_r2 - f_t2) t6 (非零)");
}

console.log("\n=== 18. 二項基底での閉形(文書掲載形) ===");
{
  const bn = (m, k) => { let r = 1n, M = BigInt(m); for (let i = 0; i < k; i++) r = r * (M - BigInt(i)) / BigInt(i + 1); return r; };
  let ok = true;
  for (const m of [0, 1, 2, 3, 4, 5, 9, 17, 31, 63, -3, -8]) {
    const e = hall(Em(m));
    const p5 = bn(m, 1) + 7n * bn(m, 2) + 17n * bn(m, 3) + 17n * bn(m, 4) + 6n * bn(m, 5);
    const p6 = -(bn(m, 2) + 4n * bn(m, 3) + 6n * bn(m, 4) + 3n * bn(m, 5));
    if (p5 !== e[10] || p6 !== e[11]) { ok = false; console.log(`  eps binom mismatch m=${m}: ${p5},${p6} vs ${e[10]},${e[11]}`); }
    // Ebar_m の (-1)^{a+1} C(m+1+a, a+b+2) 形
    const AB = [[0, 0], [1, 0], [0, 1], [2, 0], [1, 1], [0, 2], [3, 0], [2, 1], [1, 2], [0, 3]];
    for (let j = 0; j < 10; j++) { const [a, b] = AB[j]; const pr = (a % 2 === 1 ? 1n : -1n) * bn(m + 1 + a, a + b + 2); if (pr !== e[j]) { ok = false; console.log(`  Ebar binom mismatch m=${m} ${NAMES[j]}`); } }
  }
  check("eps_m = [C(m,1)+7C(m,2)+17C(m,3)+17C(m,4)+6C(m,5)]t5 - [C(m,2)+4C(m,3)+6C(m,4)+3C(m,5)]t6", ok);
  check("Ebar_m の S^aT^b 係数 = (-1)^{a+1} C(m+1+a, a+b+2)", ok);
}

console.log("\n=== 19. Ad(y^m) の collection 公式 ===");
{
  // h in A に対し  h^{y^m} = h [h,y]^{C(m,1)} [h,y,y]^{C(m,2)} [h,y,y,y]^{C(m,3)}(左から順)
  const bn = (m, k) => { let r = 1n, M = BigInt(m); for (let i = 0; i < k; i++) r = r * (M - BigInt(i)) / BigInt(i + 1); return r; };
  let ok = true;
  const rnd = () => BigInt(Math.floor(Math.random() * 7) - 3);
  for (const m of [0, 1, 2, 3, 5, 8, 13, -4]) {
    for (let t = 0; t < 20; t++) {
      const a = Array.from({ length: 12 }, rnd);
      const h = s(a);
      const lhs = hall(conj(h, pow(Y0, m)));
      let ad = h, rhs = h;
      for (let k = 1; k <= 3; k++) { ad = comm(ad, Y0); rhs = mul(rhs, pow(ad, bn(m, k))); }
      if (vec(lhs) !== vec(hall(rhs))) { ok = false; console.log(`  Ad(y^m) mismatch m=${m}`, vec(a)); break; }
    }
    if (!ok) break;
  }
  check("h^{y^m} = h [h,y]^{C(m,1)} [h,y,y]^{C(m,2)} [h,y,y,y]^{C(m,3)}  (h in A)", ok);
  // 同じ形が x でも成立するか(theta 対称)
  let ok2 = true;
  for (const m of [1, 3, 7]) for (let t = 0; t < 15; t++) {
    const a = Array.from({ length: 12 }, rnd); const h = s(a);
    const lhs = hall(conj(h, pow(X0, m)));
    let ad = h, rhs = h;
    for (let k = 1; k <= 3; k++) { ad = comm(ad, X0); rhs = mul(rhs, pow(ad, bn(m, k))); }
    if (vec(lhs) !== vec(hall(rhs))) { ok2 = false; break; }
  }
  check("同形が x でも成立(h^{x^m})", ok2);
}

console.log(`\n=== 集計: FAILS = ${FAILS} ===`);
if (FAILS > 0) process.exit(1);
