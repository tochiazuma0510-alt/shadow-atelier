// a5_u_extract.mjs -- 委嘱 12: LMFDB 5T4-5_5_5-a の平面モデルから主係数 u を抽出する検算
// 独立実装(node・BigInt 有理数のみ)。GAP/照合器を import しない。
// 平面モデル: F(x,t) = x^5 t^3 + (-5x+2) t^2 + (-5x+6) t + 4   [LMFDB plane_model]

//////////////////// BigInt 有理数 ////////////////////
function gcdB(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { [a, b] = [b, a % b]; } return a; }
class Q {
  constructor(n, d = 1n) {
    if (typeof n === 'number') n = BigInt(n);
    if (typeof d === 'number') d = BigInt(d);
    if (d === 0n) throw new Error('div0');
    if (d < 0n) { n = -n; d = -d; }
    const g = gcdB(n, d) || 1n;
    this.n = n / g; this.d = d / g;
  }
  add(o) { return new Q(this.n * o.d + o.n * this.d, this.d * o.d); }
  sub(o) { return new Q(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { return new Q(this.n * o.n, this.d * o.d); }
  div(o) { return new Q(this.n * o.d, this.d * o.n); }
  neg() { return new Q(-this.n, this.d); }
  isZero() { return this.n === 0n; }
  eq(o) { return this.n * o.d === o.n * this.d; }
  toString() { return this.d === 1n ? `${this.n}` : `${this.n}/${this.d}`; }
}
const q = (n, d = 1) => new Q(n, d);
const Q0 = q(0), Q1 = q(1);

//////////////////// 切断冪級数(ℚ[[s]]/s^PREC) ////////////////////
const PREC = 26;
const zero = () => Array.from({ length: PREC }, () => Q0);
const cst = (c) => { const a = zero(); a[0] = c; return a; };
const S = () => { const a = zero(); a[1] = Q1; return a; };
function sAdd(a, b) { return a.map((c, i) => c.add(b[i])); }
function sSub(a, b) { return a.map((c, i) => c.sub(b[i])); }
function sMul(a, b) {
  const r = zero();
  for (let i = 0; i < PREC; i++) { if (a[i].isZero()) continue; for (let j = 0; i + j < PREC; j++) { if (b[j].isZero()) continue; r[i + j] = r[i + j].add(a[i].mul(b[j])); } }
  return r;
}
function sInv(a) { // a[0] != 0
  const r = zero(); r[0] = Q1.div(a[0]);
  for (let n = 1; n < PREC; n++) { let acc = Q0; for (let k = 1; k <= n; k++) acc = acc.add(a[k].mul(r[n - k])); r[n] = acc.neg().div(a[0]); }
  return r;
}
function sDiv(a, b) { return sMul(a, sInv(b)); }
function sShift(a, k) { const r = zero(); for (let i = 0; i + k < PREC; i++) r[i + k] = a[i]; return r; }
function sUnshift(a, k) { const r = zero(); for (let i = 0; i < k; i++) if (!a[i].isZero()) throw new Error('unshift'); for (let i = k; i < PREC; i++) r[i - k] = a[i]; return r; }
function sStr(a, m = 8) { return a.slice(0, m).map((c, i) => `${c}·s^${i}`).join(' + '); }
function lead(a) { for (let i = 0; i < PREC; i++) if (!a[i].isZero()) return [i, a[i]]; return [Infinity, Q0]; }

const results = [];
const chk = (name, ok, detail = '') => { results.push([name, ok, detail]); console.log(`${ok ? 'PASS' : '*** FAIL'}  ${name}${detail ? '  :: ' + detail : ''}`); };

//////////////////// 0. 平面モデルの展開形の同定 ////////////////////
// 主張: x^5 t^3 + (-5x+2)t^2 + (-5x+6)t + 4  ==  t^3 x^5 - 5 t(t+1) x + 2(t+1)(t+2)
function F_lmfdb(x, t) {
  return t.mul(t).mul(t).mul(x.mul(x).mul(x).mul(x).mul(x))
    .add(x.mul(q(-5)).add(q(2)).mul(t).mul(t))
    .add(x.mul(q(-5)).add(q(6)).mul(t))
    .add(q(4));
}
function F_mine(x, t) {
  const t3 = t.mul(t).mul(t), x5 = x.mul(x).mul(x).mul(x).mul(x);
  return t3.mul(x5).sub(q(5).mul(t).mul(t.add(Q1)).mul(x)).add(q(2).mul(t.add(Q1)).mul(t.add(q(2))));
}
{
  let ok = true;
  for (let a = -6; a <= 6; a++) for (let b = -6; b <= 6; b++) {
    const x = q(a, 3), t = q(b, 5);
    if (!F_lmfdb(x, t).eq(F_mine(x, t))) ok = false;
  }
  chk('T0 平面モデル = t^3x^5 - 5t(t+1)x + 2(t+1)(t+2)', ok, '169 点で一致');
}

//////////////////// 1. 判別式: disc = 50000 (t+1)^4 (t^2-4t-4)^2 / t^12 = 5·(有理関数)^2 ////////////////////
// monic 化: x^5 + P x + Q,  P = -5(t+1)/t^2, Q = 2(t+1)(t+2)/t^3
// disc(x^5+Px+Q) = 256 P^5 + 3125 Q^4
{
  let ok = true, sample = '';
  for (let b = 1; b <= 12; b++) {
    const t = q(b, 7);
    const P = q(-5).mul(t.add(Q1)).div(t.mul(t));
    const Qc = q(2).mul(t.add(Q1)).mul(t.add(q(2))).div(t.mul(t).mul(t));
    const disc = q(256).mul(P.mul(P).mul(P).mul(P).mul(P)).add(q(3125).mul(Qc.mul(Qc).mul(Qc).mul(Qc)));
    const t1 = t.add(Q1), tt = t.mul(t).sub(q(4).mul(t)).sub(q(4));
    let t12 = Q1; for (let i = 0; i < 12; i++) t12 = t12.mul(t);
    const rhs = q(50000).mul(t1.mul(t1).mul(t1).mul(t1)).mul(tt.mul(tt)).div(t12);
    if (!disc.eq(rhs)) ok = false;
    // disc = 5 * (100 (t+1)^2 (t^2-4t-4) / t^6)^2
    let t6 = Q1; for (let i = 0; i < 6; i++) t6 = t6.mul(t);
    const r = q(100).mul(t1.mul(t1)).mul(tt).div(t6);
    if (!disc.eq(q(5).mul(r).mul(r))) ok = false;
    if (b === 1) sample = `t=1/7: disc=${disc}`;
  }
  chk('T1 disc = 50000(t+1)^4(t^2-4t-4)^2/t^12 = 5·(平方)  [幾何 monodromy ⊆ A5, 算術 = S5, √5 の壁]', ok, sample);
}

//////////////////// 2. 恒等式 (t+1)(5xt-2t-4) = x^5 t^3  on F=0 ////////////////////
// これが h := 4/(x^5t^3) の計算の核。F(x,t)=0 から x^5t^3 = 5xt(t+1) - 2(t+1)(t+2) = (t+1)(5xt-2t-4)
{
  let ok = true;
  for (let a = -6; a <= 6; a++) for (let b = -6; b <= 6; b++) {
    const x = q(a, 3), t = q(b, 5);
    const lhs = t.add(Q1).mul(q(5).mul(x).mul(t).sub(q(2).mul(t)).sub(q(4)));
    const rhs = t.mul(t).mul(t).mul(x.mul(x).mul(x).mul(x).mul(x));
    // x^5t^3 - (t+1)(5xt-2t-4) = F(x,t)  (恒等式)
    if (!rhs.sub(lhs).eq(F_mine(x, t))) ok = false;
  }
  chk('T2 恒等式  x^5t^3 - (t+1)(5xt-2t-4) = F(x,t)   ⇒ F=0 上で x^5t^3 = (t+1)(5xt-2t-4)', ok);
}

//////////////////// 3. 主関係式 H(s,t): t(1-5s^2(t+1))^2 = 4 s^5 (t+1)^2 (t+2)^2 ////////////////////
// s := 1/(x^2 t) と置いたときの t と s の関係(x を消去)。
// 導出: F=0 ⇔ x^5t^3 - 5xt(t+1) = -2(t+1)(t+2) ⇒ 両辺 2 乗 ⇒ x^2t^2(x^4t^2-5(t+1))^2 = 4(t+1)^2(t+2)^2
//       これを s = 1/(x^2 t) で書き直すと H(s,t)=0。
{
  let ok = true;
  for (let a = -7; a <= 7; a++) for (let b = -7; b <= 7; b++) {
    if (a === 0 || b === 0) continue;
    const x = q(a, 3), t = q(b, 5);
    const A = t.mul(t).mul(t).mul(x.mul(x).mul(x).mul(x).mul(x)).sub(q(5).mul(x).mul(t).mul(t.add(Q1))); // x^5t^3-5xt(t+1)
    const B = q(2).mul(t.add(Q1)).mul(t.add(q(2)));
    // A^2 - B^2 = (A-B)(A+B) = (A-B)·F
    if (!A.mul(A).sub(B.mul(B)).eq(A.sub(B).mul(F_mine(x, t)))) ok = false;
    // s 版: t(1-5s^2(t+1))^2 - 4s^5(t+1)^2(t+2)^2 = (A^2-B^2)/(x^10 t^5)
    const s = Q1.div(x.mul(x).mul(t));
    const H = t.mul(Q1.sub(q(5).mul(s).mul(s).mul(t.add(Q1))).mul(Q1.sub(q(5).mul(s).mul(s).mul(t.add(Q1)))))
      .sub(q(4).mul(s.mul(s).mul(s).mul(s).mul(s)).mul(t.add(Q1).mul(t.add(Q1))).mul(t.add(q(2)).mul(t.add(q(2)))));
    let x10 = Q1; for (let i = 0; i < 10; i++) x10 = x10.mul(x);
    let t5 = Q1; for (let i = 0; i < 5; i++) t5 = t5.mul(t);
    if (!H.mul(x10).mul(t5).eq(A.mul(A).sub(B.mul(B)))) ok = false;
  }
  chk('T3 H(s,t) := t(1-5s^2(t+1))^2 - 4s^5(t+1)^2(t+2)^2 は F=0 上で消える(s=1/(x^2t))', ok);
}

//////////////////// 4. P0 での冪級数: t = 16 s^5 + ... ////////////////////
// H(s,t)=0 を t = 4s^5(t+1)^2(t+2)^2 / (1-5s^2(t+1))^2 で反復
{
  const s = S();
  let t = zero();
  for (let it = 0; it < 12; it++) {
    const t1 = sAdd(t, cst(Q1)), t2 = sAdd(t, cst(q(2)));
    const num = sMul(sShift(cst(q(4)), 5), sMul(sMul(t1, t1), sMul(t2, t2)));
    const den = (() => { const d = sSub(cst(Q1), sMul(sMul(s, s), sMul(cst(q(5)), t1))); return sMul(d, d); })();
    t = sDiv(num, den);
  }
  // 検算: H(s,t) ≡ 0
  const t1 = sAdd(t, cst(Q1)), t2 = sAdd(t, cst(q(2)));
  const d = sSub(cst(Q1), sMul(sMul(s, s), sMul(cst(q(5)), t1)));
  const H = sSub(sMul(t, sMul(d, d)), sMul(sShift(cst(q(4)), 5), sMul(sMul(t1, t1), sMul(t2, t2))));
  const Hok = H.every(c => c.isZero());
  const [ord, lc] = lead(t);
  chk('T4a 冪級数解 t(s) が H=0 を満たす', Hok);
  chk('T4b ord_s(t) = 5 かつ 主係数 = 16', ord === 5 && lc.eq(q(16)), `t = ${sStr(t, 11)}`);
  // β = -t なので u0(β) = -16
  chk('T4c β = -t = -16 s^5 + O(s^6)  ⇒ u0 = -16', ord === 5 && lc.neg().eq(q(-16)));
  // z := 2s とすると z^5 = 32 s^5 = 2t·(単数, 定数項 1)
  const z5 = sShift(cst(q(32)), 5);
  const unit = sDiv(sUnshift(z5, 5), sUnshift(sMul(cst(q(2)), t), 5));
  chk('T4d z:=2s ⇒ z^5/(2t) は定数項 1 の単数(⇒ その 5 乗根が ℚ[[s]] に存在 ⇒ z\' = z·単数^{-1/5} で z\'^5 = 2t)',
    unit[0].eq(Q1), `z^5/(2t) = ${sStr(unit, 6)}`);
}

//////////////////// 5. 他の二つの全分岐点(S3 対称性の内部整合) ////////////////////
// P1: t=-1, x が局所助変数。 τ := t+1 = (1-τ)^3 x^5 / (5(1-τ)x + 2(1+τ))
{
  const x = S();
  let tau = zero();
  for (let it = 0; it < 12; it++) {
    const om = sSub(cst(Q1), tau), op = sAdd(cst(Q1), tau);
    const num = sMul(sMul(sMul(om, om), om), sShift(cst(Q1), 5));
    const den = sAdd(sMul(cst(q(5)), sMul(om, x)), sMul(cst(q(2)), op));
    tau = sDiv(num, den);
  }
  const [o1, l1] = lead(tau);
  chk('T5a P1 (t=-1): 1-β = t+1 = (1/2) x^5 + ...  ⇒ u1 = 1/2', o1 === 5 && l1.eq(q(1, 2)), `t+1 = ${sStr(tau, 9)}`);

  // P∞: σ := 1/t,  σ = x^5 / (5(1+σ)x - 2(1+σ)(1+2σ))
  let sig = zero();
  for (let it = 0; it < 12; it++) {
    const op = sAdd(cst(Q1), sig), op2 = sAdd(cst(Q1), sMul(cst(q(2)), sig));
    const den = sSub(sMul(cst(q(5)), sMul(op, x)), sMul(cst(q(2)), sMul(op, op2)));
    sig = sDiv(sShift(cst(Q1), 5), den);
  }
  const [o2, l2] = lead(sig);
  chk('T5b P∞ (t=∞): 1/β = -1/t = (1/2) x^5 + ...  ⇒ u∞ = 1/2', o2 === 5 && l2.neg().eq(q(1, 2)), `1/t = ${sStr(sig, 9)}`);
}

//////////////////// 5b. 数値的独立確認(Durand-Kerner・冪級数を使わない経路) ////////////////////
{
  const cadd = (a, b) => [a[0] + b[0], a[1] + b[1]];
  const csub = (a, b) => [a[0] - b[0], a[1] - b[1]];
  const cmul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
  const cdiv = (a, b) => { const d = b[0] * b[0] + b[1] * b[1]; return [(a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d]; };
  const cabs = (a) => Math.hypot(a[0], a[1]);
  let ok = true; const rows = [];
  for (const t of [1e-4, 1e-6, 1e-8, 1e-10]) {
    // monic: x^5 + P x + Q, P = -5(t+1)/t^2, Q = 2(t+1)(t+2)/t^3
    const P = -5 * (t + 1) / (t * t), Qc = 2 * (t + 1) * (t + 2) / (t * t * t);
    const f = (z) => { let z5 = [1, 0]; for (let i = 0; i < 5; i++) z5 = cmul(z5, z); return cadd(cadd(z5, cmul([P, 0], z)), [Qc, 0]); };
    // 初期値: |x| ~ |Q|^{1/5}
    const R = Math.pow(Math.abs(Qc), 0.2);
    let r = [0, 1, 2, 3, 4].map(k => [R * Math.cos(0.4 + 2 * Math.PI * k / 5), R * Math.sin(0.4 + 2 * Math.PI * k / 5)]);
    for (let it = 0; it < 800; it++) {
      const nr = r.map((zi, i) => { let den = [1, 0]; r.forEach((zj, j) => { if (i !== j) den = cmul(den, csub(zi, zj)); }); return csub(zi, cdiv(f(zi), den)); });
      r = nr;
    }
    // s_i = 1/(x_i^2 t) が s_i^5 = (t/16)(1+O(s^2)) を満たすか(予測誤差 ~ 10 s^2 = 10 (t/16)^{2/5})
    let worst = 0;
    for (const z of r) {
      const s = cdiv([1, 0], cmul(cmul(z, z), [t, 0]));
      let s5 = [1, 0]; for (let i = 0; i < 5; i++) s5 = cmul(s5, s);
      worst = Math.max(worst, cabs(csub(s5, [t / 16, 0])) / Math.abs(t / 16));
    }
    const bound = 20 * Math.pow(Math.abs(t) / 16, 0.4);
    if (!(worst < bound)) ok = false;
    rows.push(`t=${t.toExponential(0)}: |16s^5/t-1| = ${worst.toExponential(2)} (< ${bound.toExponential(2)})`);
  }
  chk('T5c 数値(Durand-Kerner・冪級数非依存): 全 5 根で 16 s^5/t → 1、誤差は予測 O(t^{2/5}) 内', ok, rows.join(' | '));
}

//////////////////// 6. 5 乗剰余類の突合 ////////////////////
// v_p(u) mod 5 で比較(-1 = (-1)^5 は 5 乗なので符号は無関係)
function fifthClass(n, d) { // 有理数 n/d の (2,3,5,...) 指数を mod 5 で
  const e = {};
  for (const [v, sg] of [[n, 1], [d, -1]]) {
    let m = Math.abs(v);
    for (const p of [2, 3, 5, 7, 11, 13]) { let k = 0; while (m % p === 0) { m /= p; k++; } if (k) e[p] = ((e[p] || 0) + sg * k % 5 + 5) % 5; }
    if (m !== 1) e['rest' + m] = ((e['rest' + m] || 0) + sg + 5) % 5;
  }
  for (const k of Object.keys(e)) if (e[k] === 0) delete e[k];
  return JSON.stringify(e);
}
{
  const c0 = fifthClass(-16, 1), c1 = fifthClass(1, 2), cinf = fifthClass(1, 2);
  chk('T6a [u0]=[-16], [u1]=[1/2], [u∞]=[1/2] は ℚ*/(ℚ*)^5 で一致(S3 対称性)', c0 === c1 && c1 === cinf, `class = ${c0}  (= [2]^4)`);
  chk('T6b [u] ≠ 1 : v_2(16) = 4 ≢ 0 mod 5', c0 !== '{}');
  // Sol の候補 -16/27 との比較
  const cs = fifthClass(-16, 27);
  chk('T6c Sol 候補 [-16/27] と [u]=[−16] は別クラス(e ∈ F5^* の冪でも移らない)',
    cs !== c0 && ![1, 2, 3, 4].some(e => {
      // [-16]^e の類
      const ee = {}; ee['2'] = (4 * e) % 5; for (const k of Object.keys(ee)) if (ee[k] === 0) delete ee[k];
      return JSON.stringify(ee) === cs;
    }), `[-16/27] = ${cs} vs [-16]^e = {2:4e}`);
}

//////////////////// 7. 幾何 monodromy ≠ C5 (特殊化の Galois 群 ⊄ F20) ////////////////////
// t=1 で x^5 - 10x + 12。F20 の cycle type は 1^5, 5, 2^2 1, 4 1 のみ。
// mod p の因数分解型に 3 次因子が現れれば Galois 群 ⊄ F20 ⇒ 幾何 monodromy = A5。
// x^5 + c1 x + c0 の 𝔽_p 上の根の個数(重根の場合は null)
function rootCountModP(coeffs, p) {
  const mod = (a) => ((a % p) + p) % p;
  const val = (x) => { let x5 = 1; for (let i = 0; i < 5; i++) x5 = mod(x5 * x); return mod(x5 + coeffs[1] * x + coeffs[0]); };
  const dval = (x) => { let x4 = 1; for (let i = 0; i < 4; i++) x4 = mod(x4 * x); return mod(5 * x4 + coeffs[1]); };
  let roots = 0;
  for (let x = 0; x < p; x++) if (val(x) === 0) { if (dval(x) === 0) return null; roots++; }
  return roots;
}
{
  // x^5 - 10x + 12  (t=1)
  const c = [12, -10]; // c0, c1
  // 5 次の Galois 群が F20 に含まれるなら、任意の p で「根の数」は 0,1,5 のいずれか
  // (F20 の元の不動点数: id=5, 5-cycle=0, (2,2,1)=1, (4,1)=1) ⇒ 根の数 ∈ {0,1,5}
  // A5/S5 では 3-cycle 型 (3,1,1) が現れ、根の数 = 2 になりうる。
  // disc = 39200000 = 2^8·5^5·7^2 ⇒ 分岐素数 {2,5,7} を除く
  const bad = [];
  for (const p of [3, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103]) {
    const r = rootCountModP(c, p);
    if (r !== null && ![0, 1, 5].includes(r)) bad.push([p, r]);
  }
  chk('T7 特殊化 t=1 の x^5-10x+12: 根の数が {0,1,5} 外の素数が存在 ⇒ Galois 群 ⊄ F20 ⇒ 幾何 monodromy = A5',
    bad.length > 0, `例: ${bad.slice(0, 5).map(([p, r]) => `p=${p}: ${r} 根`).join(', ')}`);
}

//////////////////// 8. LMFDB の monodromy 三つ組の独立確認 ////////////////////
{
  const perm = (cyc) => { const a = [0, 1, 2, 3, 4, 5]; for (let i = 0; i < cyc.length; i++) a[cyc[i]] = cyc[(i + 1) % cyc.length]; return a; };
  const comp = (f, g) => { const r = [0]; for (let i = 1; i <= 5; i++) r[i] = f[g[i]]; return r; }; // (f∘g)(i)=f(g(i))
  const id = [0, 1, 2, 3, 4, 5];
  const eq = (f, g) => f.every((v, i) => v === g[i]);
  const s0 = perm([1, 2, 3, 4, 5]), s1 = perm([1, 3, 4, 2, 5]), si = perm([1, 2, 5, 3, 4]);
  chk('T8a triples_cyc の積 σ0σ1σ∞ = id', eq(comp(comp(s0, s1), si), id));
  // 生成群の位数
  const key = (f) => f.slice(1).join('');
  const seen = new Map([[key(id), id]]); const stack = [id];
  while (stack.length) { const a = stack.pop(); for (const g of [s0, s1, si]) { const b = comp(a, g); if (!seen.has(key(b))) { seen.set(key(b), b); stack.push(b); } } }
  chk('T8b ⟨σ0,σ1,σ∞⟩ の位数 = 60 (= A5)', seen.size === 60, `|G| = ${seen.size}`);
  // sign
  const sign = (f) => { let s = 1; const v = [...f]; for (let i = 1; i <= 5; i++) for (let j = i + 1; j <= 5; j++) if (v[i] > v[j]) s = -s; return s; };
  chk('T8c 全生成元が偶置換', [s0, s1, si].every(g => sign(g) === 1));
}

//////////////////// 9. 較正ゲート: 巡回 μ5-被覆 w^5 = c·t(1-t)^b ////////////////////
// 予測: 0⃗1 上の接繊維の Kummer 類 = [c]^{-1}。c=1 なら自明、c=2 なら [2]^{-1}(非自明)。
// 機構: w が P0 の局所助変数、t = w^5 · c^{-1} (1-t)^{-b} = c^{-1} w^5 (1+O(w^5)) ⇒ u = c^{-1}
{
  const tests = [[1, 1], [2, 1], [1, 3], [16, 2]];
  let ok = true, det = [];
  for (const [c, b] of tests) {
    // w^5 = c t (1-t)^b を t について解く: t = w^5/(c (1-t)^b)
    const w = S(); let t = zero();
    for (let it = 0; it < 10; it++) {
      let omb = cst(Q1); const om = sSub(cst(Q1), t);
      for (let i = 0; i < b; i++) omb = sMul(omb, om);
      t = sDiv(sShift(cst(Q1), 5), sMul(cst(q(c)), omb));
    }
    const [o, l] = lead(t);
    const good = o === 5 && l.eq(Q1.div(q(c)));
    if (!good) ok = false;
    det.push(`c=${c},b=${b}: u=${l} (期待 1/${c})`);
  }
  chk('T9 較正ゲート: 巡回 μ5-被覆 w^5 = c·t(1-t)^b の接繊維主係数 = 1/c(捻れ c を正しく検出)', ok, det.join(' | '));
}

//////////////////// 総括 ////////////////////
const nfail = results.filter(r => !r[1]).length;
console.log(`\n==== ${results.length - nfail}/${results.length} PASS ====`);
if (nfail) process.exitCode = 1;
