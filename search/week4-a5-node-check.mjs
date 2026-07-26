// a5_node_check.mjs -- 平面モデル F の余分な判別式零点 t^2-4t-4=0 が「節点(node)」であり
// 分岐点ではないことを確認する。これが通れば分岐点は {0,-1,∞} のちょうど 3 点、RH で g=2。
// 体 K = Q(√2) 上で計算(t0 = 2+2√2 は t^2 = 4t+4 の根)。

function gcdB(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { [a, b] = [b, a % b]; } return a; }
class Q { constructor(n, d = 1n) { if (typeof n === 'number') n = BigInt(n); if (typeof d === 'number') d = BigInt(d); if (d < 0n) { n = -n; d = -d; } const g = gcdB(n, d) || 1n; this.n = n / g; this.d = d / g; }
  add(o) { return new Q(this.n * o.d + o.n * this.d, this.d * o.d); } sub(o) { return new Q(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { return new Q(this.n * o.n, this.d * o.d); } div(o) { return new Q(this.n * o.d, this.d * o.n); }
  isZero() { return this.n === 0n; } toString() { return this.d === 1n ? `${this.n}` : `${this.n}/${this.d}`; } }
const q = (n, d = 1) => new Q(n, d);
// K = Q(√2): [a,b] = a + b√2
const K = {
  add: (u, v) => [u[0].add(v[0]), u[1].add(v[1])],
  sub: (u, v) => [u[0].sub(v[0]), u[1].sub(v[1])],
  mul: (u, v) => [u[0].mul(v[0]).add(q(2).mul(u[1]).mul(v[1])), u[0].mul(v[1]).add(u[1].mul(v[0]))],
  inv: (u) => { const n = u[0].mul(u[0]).sub(q(2).mul(u[1]).mul(u[1])); return [u[0].div(n), u[1].div(n).mul(q(-1))]; },
  div: (u, v) => K.mul(u, K.inv(v)),
  isZero: (u) => u[0].isZero() && u[1].isZero(),
  of: (a, b = 0) => [q(a), q(b)],
  str: (u) => `${u[0]} + ${u[1]}√2`,
};
const t0 = K.of(2, 2);                 // t0 = 2 + 2√2,  t0^2 = 4t0 + 4
console.log('t0^2 - 4t0 - 4 =', K.str(K.sub(K.sub(K.mul(t0, t0), K.mul(K.of(4), t0)), K.of(4))));

// F(x,t) = t^3 x^5 - 5 t(t+1) x + 2(t+1)(t+2)
const P = (x, t) => {
  const t1 = K.add(t, K.of(1)), t2 = K.add(t, K.of(2));
  const t3 = K.mul(K.mul(t, t), t);
  let x5 = K.of(1); for (let i = 0; i < 5; i++) x5 = K.mul(x5, x);
  return K.sub(K.mul(t3, x5), K.mul(K.mul(K.of(5), K.mul(t, t1)), x)).map ? K.add(K.sub(K.mul(t3, x5), K.mul(K.mul(K.of(5), K.mul(t, t1)), x)), K.mul(K.of(2), K.mul(t1, t2))) : null;
};
// 偏微分(記号で書き下し)
const Fx = (x, t) => { const t1 = K.add(t, K.of(1)); let x4 = K.of(1); for (let i = 0; i < 4; i++) x4 = K.mul(x4, x);
  return K.sub(K.mul(K.mul(K.of(5), K.mul(K.mul(t, t), t)), x4), K.mul(K.of(5), K.mul(t, t1))); };
const Fxx = (x, t) => { let x3 = K.of(1); for (let i = 0; i < 3; i++) x3 = K.mul(x3, x);
  return K.mul(K.mul(K.of(20), K.mul(K.mul(t, t), t)), x3); };
const Ft = (x, t) => { let x5 = K.of(1); for (let i = 0; i < 5; i++) x5 = K.mul(x5, x);
  // d/dt [t^3 x^5 - 5(t^2+t)x + 2(t^2+3t+2)] = 3t^2 x^5 - 5(2t+1)x + 2(2t+3)
  return K.add(K.sub(K.mul(K.mul(K.of(3), K.mul(t, t)), x5), K.mul(K.mul(K.of(5), K.add(K.mul(K.of(2), t), K.of(1))), x)), K.mul(K.of(2), K.add(K.mul(K.of(2), t), K.of(3)))); };
const Fxt = (x, t) => { let x4 = K.of(1); for (let i = 0; i < 4; i++) x4 = K.mul(x4, x);
  return K.sub(K.mul(K.mul(K.of(15), K.mul(t, t)), x4), K.mul(K.of(5), K.add(K.mul(K.of(2), t), K.of(1)))); };
const Ftt = (x, t) => { let x5 = K.of(1); for (let i = 0; i < 5; i++) x5 = K.mul(x5, x);
  return K.add(K.mul(K.mul(K.of(6), t), x5), K.of(-10 + 4)); };  // 6t x^5 - 10x*0 ... : d^2/dt^2 = 6t x^5 - 10 x' ... 下で再計算

// Ftt を正しく: F = t^3x^5 - 5(t^2+t)x + 2t^2+6t+4  ⇒ F_tt = 6t x^5 - 10 x + 4
const Ftt2 = (x, t) => { let x5 = K.of(1); for (let i = 0; i < 5; i++) x5 = K.mul(x5, x);
  return K.add(K.sub(K.mul(K.mul(K.of(6), t), x5), K.mul(K.of(10), x)), K.of(4)); };

// F(·,t0) と F_x(·,t0) の共通根 x0 を求める。
// F_x = 0 ⇒ x^4 = (t0+1)/t0^2  … x0 は 4 次方程式の根だが、F=0 も満たすものを探す。
// 実際には resultant を使わず、F と F_x の gcd を K[x] で計算する。
function polyFromF(t) { // F(x,t) の係数(昇冪, 次数 5)
  const t1 = K.add(t, K.of(1)), t2 = K.add(t, K.of(2));
  return [K.mul(K.of(2), K.mul(t1, t2)), K.mul(K.of(-5), K.mul(t, t1)), K.of(0), K.of(0), K.of(0), K.mul(K.mul(t, t), t)];
}
function polyFromFx(t) { const t1 = K.add(t, K.of(1));
  return [K.mul(K.of(-5), K.mul(t, t1)), K.of(0), K.of(0), K.of(0), K.mul(K.of(5), K.mul(K.mul(t, t), t))]; }
const deg = (a) => { let d = a.length - 1; while (d >= 0 && K.isZero(a[d])) d--; return d; };
function polyRem(a, b) { a = a.map(z => [z[0], z[1]]); const db = deg(b); const lb = b[db];
  let da = deg(a);
  while (da >= db && da >= 0) { const c = K.div(a[da], lb); for (let i = 0; i <= db; i++) a[da - db + i] = K.sub(a[da - db + i], K.mul(c, b[i])); da = deg(a); }
  return a.slice(0, Math.max(da + 1, 1)); }
function polyGcd(a, b) { while (deg(b) > 0 || (deg(b) === 0 && !K.isZero(b[0]))) { const r = polyRem(a, b); a = b; b = r; } return a; }

const g = polyGcd(polyFromF(t0), polyFromFx(t0));
console.log('gcd(F, F_x) の次数 =', deg(g), '係数:', g.map(K.str).join(' , '));
if (deg(g) !== 1) { console.log('*** 期待は 1 次(重根 1 個)'); process.exitCode = 1; }
const x0 = K.div(K.mul(K.of(-1), g[0]), g[1]);
console.log('重根 x0 =', K.str(x0));

const vF = polyRem(polyFromF(t0), [K.mul(K.of(-1), x0), K.of(1)]);
console.log('F(x0,t0) =', K.str(vF[0] || K.of(0)));
console.log('F_x(x0,t0) =', K.str(Fx(x0, t0)));
console.log('F_t(x0,t0) =', K.str(Ft(x0, t0)));
const A = Fxx(x0, t0), B = Fxt(x0, t0), C = Ftt2(x0, t0);
const disc2 = K.sub(K.mul(B, B), K.mul(A, C));
console.log('二次形式: a=F_xx =', K.str(A), ', b=F_xt =', K.str(B), ', c=F_tt =', K.str(C));
console.log('判別 b^2-ac =', K.str(disc2));

const isNode = K.isZero(Ft(x0, t0)) && !K.isZero(A) && !K.isZero(disc2);
console.log(isNode
  ? 'PASS  (x0,t0) は F の node(F=F_x=F_t=0, b^2-ac≠0, a≠0)⇒ 写像 t は両枝で不分岐 ⇒ 余分な分岐なし'
  : '*** FAIL 節点判定に失敗');
if (!isNode) process.exitCode = 1;
