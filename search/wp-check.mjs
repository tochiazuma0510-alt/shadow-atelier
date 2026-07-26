// 検算用(手計算の機械確認): weighted-primitive 正規化 wp の
//   (1) denominator clearing 非依存性  wp(sigma . A) = wp(A)
//   (2) 冪等性 wp(wp(A)) = wp(A)
//   (3) 有限性(安定化群 = {±1})
// 純整数演算(BigInt 有理数)。入力は無作為な有理係数ベクトル(曲線データではない)。

function gcdB(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { [a, b] = [b, a % b]; } return a; }
class Q { // 有理数 num/den, den>0, 既約
  constructor(n, d = 1n) {
    if (d === 0n) throw new Error('div0');
    if (d < 0n) { n = -n; d = -d; }
    const g = gcdB(n, d) || 1n; this.n = n / g; this.d = d / g;
  }
  static of(n, d = 1n) { return new Q(BigInt(n), BigInt(d)); }
  mul(o) { return new Q(this.n * o.n, this.d * o.d); }
  div(o) { return new Q(this.n * o.d, this.d * o.n); }
  pow(k) { // k >= 0
    let r = Q.of(1), b = this; let e = BigInt(k);
    while (e > 0n) { if (e & 1n) r = r.mul(b); b = b.mul(b); e >>= 1n; }
    return r;
  }
  isZero() { return this.n === 0n; }
  isInt() { return this.d === 1n; }
  toString() { return this.d === 1n ? `${this.n}` : `${this.n}/${this.d}`; }
  eq(o) { return this.n === o.n && this.d === o.d; }
}

// v_p(q)
function vp(q, p) {
  if (q.isZero()) return null;
  let v = 0, n = q.n < 0n ? -q.n : q.n, d = q.d, P = BigInt(p);
  while (n % P === 0n) { n /= P; v++; }
  while (d % P === 0n) { d /= P; v--; }
  return v;
}
// 現れうる素数(分子・分母の素因子)
function primesOf(vec) {
  const s = new Set();
  const fac = (m) => { m = m < 0n ? -m : m; for (let p = 2n; p * p <= m; p++) { while (m % p === 0n) { s.add(Number(p)); m /= p; } } if (m > 1n) s.add(Number(m)); };
  for (const q of vec) { if (q.isZero()) continue; fac(q.n); fac(q.d); }
  return [...s].sort((a, b) => a - b);
}
function floorDiv(a, b) { return Math.floor(a / b); } // b>0

// weighted-primitive normalization: A_j |-> A_j / tau_+^{w_j}
function wp(A, w) {
  const ps = primesOf(A);
  // tau_+ を素数冪の積として構成
  let tau = Q.of(1);
  for (const p of ps) {
    let k = null;
    for (let j = 0; j < A.length; j++) {
      if (A[j].isZero()) continue;            // 零係数は min から除外
      const t = floorDiv(vp(A[j], p), w[j]);
      k = (k === null) ? t : Math.min(k, t);
    }
    if (k === null) throw new Error('all-zero vector');
    const P = Q.of(p);
    tau = tau.mul(k >= 0 ? P.pow(k) : Q.of(1).div(P.pow(-k)));
  }
  return A.map((a, j) => a.isZero() ? a : a.div(tau.pow(w[j])));
}
// M2 作用: A_j |-> A_j / sigma^{w_j}
function act(A, w, sigma) { return A.map((a, j) => a.isZero() ? a : a.div(sigma.pow(w[j]))); }
// 注: sigma^{w_j} は w_j>=0 なので pow で足りる

function isIntVec(A) { return A.every(a => a.isZero() || a.isInt()); }
function kappa(A, w, p) {
  let k = null;
  for (let j = 0; j < A.length; j++) { if (A[j].isZero()) continue; const t = floorDiv(vp(A[j], p), w[j]); k = (k === null) ? t : Math.min(k, t); }
  return k;
}
function isWP(A, w) { return primesOf(A).every(p => kappa(A, w, p) === 0) && isIntVec(A); }
function eqVec(A, B) { return A.length === B.length && A.every((a, i) => a.eq(B[i])); }

// ---- 試験 ----
const branches = [
  { name: '(W) w_j = 2(5-j), j=0..4', w: [10, 8, 6, 4, 2] },
  { name: '(N) w_j = 6-j,   j=0..5', w: [6, 5, 4, 3, 2, 1] },
];
// 決定的な擬似乱数
let seed = 20260727n;
function rnd(m) { seed = (seed * 6364136223846793005n + 1442695040888963407n) & ((1n << 64n) - 1n); return Number((seed >> 33n) % BigInt(m)); }

let pass = 0, fail = 0;
for (const br of branches) {
  const w = br.w, n = w.length;
  for (let trial = 0; trial < 400; trial++) {
    // 無作為有理係数(小さな素数を意図的に含める)・一部を零に
    const A = [];
    for (let j = 0; j < n; j++) {
      if (rnd(5) === 0) { A.push(Q.of(0)); continue; }
      const num = BigInt((rnd(2) ? 1 : -1) * (1 + rnd(30))) * (2n ** BigInt(rnd(12))) * (3n ** BigInt(rnd(7))) * (5n ** BigInt(rnd(5)));
      const den = (2n ** BigInt(rnd(9))) * (3n ** BigInt(rnd(5))) * BigInt(1 + rnd(7));
      A.push(new Q(num, den));
    }
    if (A.every(a => a.isZero())) continue;

    const W0 = wp(A, w);
    // (1) 非依存性: 任意の sigma > 0 で act した後に wp を取っても同じ
    for (let s = 0; s < 6; s++) {
      const sig = new Q(BigInt(1 + rnd(20)) * (2n ** BigInt(rnd(6))) * (5n ** BigInt(rnd(4))), BigInt(1 + rnd(15)) * (3n ** BigInt(rnd(5))));
      const W1 = wp(act(A, w, sig), w);
      if (eqVec(W0, W1)) pass++; else { fail++; console.log('FAIL indep', br.name, A.map(String).join(','), 'sigma=', sig.toString()); }
    }
    // (1') 具体的な過剰 clearing: sigma = 1/lcm(分母) でも整数化される
    let L = 1n; for (const a of A) if (!a.isZero()) L = L / gcdB(L, a.d) * a.d;
    const cleared = act(A, w, new Q(1n, L));
    if (isIntVec(cleared)) pass++; else { fail++; console.log('FAIL clearing', br.name, A.map(String).join(',')); }
    if (eqVec(wp(cleared, w), W0)) pass++; else { fail++; console.log('FAIL clearing-wp', br.name); }

    // (2) 整数性 + weighted primitive + 冪等
    if (isWP(W0, w)) pass++; else { fail++; console.log('FAIL isWP', br.name, W0.map(String).join(',')); }
    if (eqVec(wp(W0, w), W0)) pass++; else { fail++; console.log('FAIL idem', br.name); }

    // (3) 有限性: sigma != ±1 なら「整数かつ weighted primitive」を保てない
    for (let s = 0; s < 4; s++) {
      let sig = new Q(BigInt(1 + rnd(9)), BigInt(1 + rnd(9)));
      if (sig.n === sig.d) continue;             // sigma = 1 は除く
      const B = act(W0, w, sig);
      const stillOK = isIntVec(B) && isWP(B, w);
      if (!stillOK) pass++; else { fail++; console.log('FAIL stab', br.name, 'sigma=', sig.toString()); }
    }
    // sigma = -1 は必ず保つ(符号単元)
    const Bm = act(W0, w, Q.of(-1));
    if (isIntVec(Bm) && isWP(Bm, w)) pass++; else { fail++; console.log('FAIL sign-unit', br.name); }
  }
}
console.log(`pass=${pass} fail=${fail}`);

// 枝ごとの符号作用の確認: (W) は tau=-1 で係数不変 / (N) は t=-1 で B_j |-> (-1)^j B_j
{
  const w = [10, 8, 6, 4, 2];
  const A = [Q.of(3), Q.of(-5), Q.of(7), Q.of(2), Q.of(-11)];
  console.log('(W) tau=-1 :', act(A, w, Q.of(-1)).map(String).join(','), ' (元:', A.map(String).join(','), ')');
}
{
  const w = [6, 5, 4, 3, 2, 1];
  const B = [Q.of(3), Q.of(-5), Q.of(7), Q.of(2), Q.of(-11), Q.of(4)];
  console.log('(N) t=-1   :', act(B, w, Q.of(-1)).map(String).join(','), ' (元:', B.map(String).join(','), ')');
}
