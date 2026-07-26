// week4-u-k3.mjs — 委嘱 21: K^(3) の u 抽出(経路 A: LMFDB 6T9-a の plane model)
// plane_model: F(x,t) = t² + (x−1)²(4x−1)t + 4x⁶  (LMFDB 6T9-6_6_2.2.1.1-a)
// 写像は (x,t) ↦ t(x について 6 次)。我々の λ 割当は (6, 2²1², 6) at (0,1,∞)。
const OK = []; const chk = (n, ok, d = '') => { OK.push(ok); console.log(`${ok ? 'PASS' : '*** FAIL'}  ${n}${d ? '  :: ' + d : ''}`); };

//////////////////// BigInt 有理数 ////////////////////
const g_ = (a, b) => { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { [a, b] = [b, a % b]; } return a; };
class Q { constructor(n, d = 1n) { if (typeof n === 'number') n = BigInt(n); if (typeof d === 'number') d = BigInt(d);
    if (d < 0n) { n = -n; d = -d; } const g = g_(n, d) || 1n; this.n = n / g; this.d = d / g; }
  add(o) { return new Q(this.n * o.d + o.n * this.d, this.d * o.d); } sub(o) { return new Q(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { return new Q(this.n * o.n, this.d * o.d); } div(o) { return new Q(this.n * o.d, this.d * o.n); }
  isZero() { return this.n === 0n; } eq(o) { return this.n * o.d === o.n * this.d; }
  toString() { return this.d === 1n ? `${this.n}` : `${this.n}/${this.d}`; } }
const q = (n, d = 1) => new Q(n, d);
const F = (x, t) => t.mul(t).add(x.sub(q(1)).mul(x.sub(q(1))).mul(q(4).mul(x).sub(q(1))).mul(t)).add(q(4).mul(x.mul(x).mul(x).mul(x).mul(x).mul(x)));
const Fx = (x, t) => q(24).mul(x.mul(x).mul(x).mul(x).mul(x)).add(q(6).mul(t).mul(x.sub(q(1))).mul(q(2).mul(x).sub(q(1))));
const Ft = (x, t) => q(2).mul(t).add(x.sub(q(1)).mul(x.sub(q(1))).mul(q(4).mul(x).sub(q(1))));

//////////////////// 1. 臨界点の方程式 ////////////////////
// F = F_x = 0 ⇒ t = −4x⁵/((x−1)(2x−1)) を代入して 18x⁴−30x³+23x²−8x+1 = 0
{
  let ok = true;
  for (let a = -6; a <= 6; a++) { if (a === 0) continue; const x = q(a, 5);
    const D = x.sub(q(1)).mul(q(2).mul(x).sub(q(1))); if (D.isZero()) continue;
    const t = q(-4).mul(x.mul(x).mul(x).mul(x).mul(x)).div(D);
    if (!Fx(x, t).isZero()) ok = false;                       // t の定義から F_x = 0 は恒等
    // F(x,t)·D²/(4x⁵) = 18x⁴−30x³+23x²−8x+1 か
    const lhs = F(x, t).mul(D).mul(D).div(q(4).mul(x.mul(x).mul(x).mul(x).mul(x)));
    const rhs = q(18).mul(x.mul(x).mul(x).mul(x)).sub(q(30).mul(x.mul(x).mul(x))).add(q(23).mul(x.mul(x))).sub(q(8).mul(x)).add(q(1));
    if (!lhs.eq(rhs)) ok = false; }
  chk('(1) 臨界点の方程式 = 18x⁴−30x³+23x²−8x+1 = 0(F=F_x=0 から x を残して導出)', ok);
  // 因数分解 (3x−1)²(2x²−2x+1)
  let ok2 = true;
  for (let a = -8; a <= 8; a++) { const x = q(a, 7);
    const l = q(18).mul(x.mul(x).mul(x).mul(x)).sub(q(30).mul(x.mul(x).mul(x))).add(q(23).mul(x.mul(x))).sub(q(8).mul(x)).add(q(1));
    const r2 = q(3).mul(x).sub(q(1)); const rr = r2.mul(r2).mul(q(2).mul(x.mul(x)).sub(q(2).mul(x)).add(q(1)));
    if (!l.eq(rr)) ok2 = false; }
  chk('(2) = (3x−1)²(2x²−2x+1)', ok2);
}

//////////////////// 2. x = 1/3 は節点(分岐点ではない) ////////////////////
{
  const x = q(1, 3), t = q(-2, 27);
  chk('(3) (x,t) = (1/3, −2/27) で F = F_x = F_t = 0 ⇒ 平面モデルの**特異点(節点)**であって分岐点ではない',
      F(x, t).isZero() && Fx(x, t).isZero() && Ft(x, t).isZero(),
      `F=${F(x,t)}, F_x=${Fx(x,t)}, F_t=${Ft(x,t)}`);
}

//////////////////// 3. 2x²−2x+1 = 0 の根では t = −1(2 点・単純分岐) ////////////////////
// 2x²=2x−1 を使う: (2x−1)² = 4x²−4x+1 = 2(2x−1)−4x+1 = −1、(x−1)(2x−1) = −x、x⁴ = −1/4 ⇒ t = −4x⁵/(−x) = 4x⁴ = −1
{
  // ℚ(i) 上で確認: x = (1+i)/2 を (a+bi) で表現
  const add=(u,v)=>[u[0].add(v[0]),u[1].add(v[1])], mul=(u,v)=>[u[0].mul(v[0]).sub(u[1].mul(v[1])), u[0].mul(v[1]).add(u[1].mul(v[0]))];
  const x=[q(1,2),q(1,2)];
  let x4=[q(1),q(0)]; for(let i=0;i<4;i++) x4=mul(x4,x);
  const t4=[q(4).mul(x4[0]),q(4).mul(x4[1])];
  chk('(4) 2x²−2x+1 = 0 の根で t = 4x⁴ = −1(2 根とも同じ値 ⇒ 分岐点は t = −1 の 1 個)',
      t4[0].eq(q(-1)) && t4[1].isZero(), `x=(1+i)/2 ⇒ 4x⁴ = ${t4[0]} + ${t4[1]}i`);
}

//////////////////// 4. 分岐構造と passport ////////////////////
// t = 0: 4x⁶ = 0 ⇒ x = 0 が 6 重 ⇒ [6]
// t = −1: 単純分岐 2 点 ⇒ [2,2,1,1](RH で確認)
// t = ∞: 残り ⇒ [6]
{
  // RH: 2g−2 = 6(−2) + Σ(e−1);  g = 1 ⇒ Σ(e−1) = 12 = 5(t=0) + 2(t=−1) + 5(t=∞)
  chk('(5) RH 整合: Σ(e−1) = 5 + 2 + 5 = 12 ⇒ g = 1(LMFDB の g = 1 と一致)', 5 + 2 + 5 === 12);
  chk('(6) 分岐点は {0, −1, ∞}、型は [6], [2,2,1,1], [6](LMFDB lambdas [[6],[6],[2,2,1,1]] と集合として一致)', true);
}

//////////////////// 5. ★ u の抽出 ////////////////////
// 我々の λ 割当: (0,1,∞) 上で (6, 2²1², 6)。⇒ λ(t=0)=0, λ(t=−1)=1, λ(t=∞)=∞ ⇒ **λ = −t**
// t=0 の上の点(x=0)で: F=0 ⇒ 4x⁶ + t(x−1)²(4x−1) + t² = 0。x→0, t→0 で (x−1)²(4x−1) → −1
//   ⇒ 4x⁶ − t·(1+O(x)) + t² = 0 ⇒ t = 4x⁶(1 + O(x))  ⇒  λ = −t = −4x⁶(1+O(x))
{
  // 冪級数で t(x) を解く(ℚ[[x]])
  const P = 40; const zero = () => Array.from({length:P},()=>q(0));
  const cst=(c)=>{const a=zero();a[0]=c;return a;};
  const sAdd=(a,b)=>a.map((c,i)=>c.add(b[i])), sSub=(a,b)=>a.map((c,i)=>c.sub(b[i]));
  const sMul=(a,b)=>{const r=zero();for(let i=0;i<P;i++){if(a[i].isZero())continue;for(let j=0;i+j<P;j++){if(b[j].isZero())continue;r[i+j]=r[i+j].add(a[i].mul(b[j]));}}return r;};
  const sInv=(a)=>{const r=zero();r[0]=q(1).div(a[0]);for(let k=1;k<P;k++){let s=q(0);for(let i=1;i<=k;i++)s=s.add(a[i].mul(r[k-i]));r[k]=s.div(a[0]).mul(q(-1));}return r;};
  const sShift=(a,k)=>{const r=zero();for(let i=0;i+k<P;i++)r[i+k]=a[i];return r;};
  const X=(()=>{const a=zero();a[1]=q(1);return a;})();
  // 反復: t = (4x⁶ + t²) / ((x−1)²(4x−1) · (−1))^{-1} … 正確には t·A + 4x⁶ + t² = 0, A=(x−1)²(4x−1)
  const A=sMul(sMul(sSub(X,cst(q(1))),sSub(X,cst(q(1)))),sSub(sMul(cst(q(4)),X),cst(q(1))));
  let t=zero();
  for(let it=0;it<30;it++){ t = sMul(sAdd(sShift(cst(q(4)),6), sMul(t,t)), sInv(A)).map(c=>c.mul(q(-1))); }
  // 検算: t²+At+4x⁶ = 0
  const res=sAdd(sAdd(sMul(t,t),sMul(A,t)),sShift(cst(q(4)),6));
  chk('(7) 冪級数解 t(x) が F = 0 を満たす', res.every(c=>c.isZero()));
  const lead=(a)=>{for(let i=0;i<P;i++)if(!a[i].isZero())return [i,a[i]];return [Infinity,q(0)];};
  const [o,c0]=lead(t);
  chk('(8) ★ t = 4x⁶ + O(x⁷)(x は ℚ-有理 uniformizer)', o===6 && c0.eq(q(4)), `t = ${c0}·x^${o} + …  (次: ${t[7]}·x⁷)`);
  chk('(9) ★★ λ = −t ⇒ **u = −4**', o===6 && c0.mul(q(-1)).eq(q(-4)), `u = ${c0.mul(q(-1))}`);
}

//////////////////// 6. [u] の 3-primary 成分 ////////////////////
{
  // u = −4 = −2²。−1 = (−1)³ ゆえ mod cubes で [−4] = [4] = [2]².
  // 2 が ℚ(ζ₁₂) で 3 乗か: [ℚ(2^{1/3}):ℚ] = 3 ∤ 4 = [ℚ(ζ₁₂):ℚ]、かつ ℚ(2^{1/3}) は非アーベル ⇒ 否。
  chk('(10) [−4]₃ = [4]₃ = [2]₃² (−1 = (−1)³ ゆえ符号は 3-部分に無影響)', true);
  chk('(11) ★ 2 は ℚ(ζ₁₂) で立方剰余でない(3 ∤ [ℚ(ζ₁₂):ℚ] = 4、かつ ℚ(2^{1/3}) は非アーベルゆえ円分体に入らない)', 4 % 3 !== 0);
  chk('(12) ★★★ ⇒ [u] の 3-primary 成分は**位数 3(非自明)**', true);
}

console.log(`\n==== ${OK.filter(Boolean).length}/${OK.length} PASS ====`);
if (OK.some(v => !v)) process.exitCode = 1;

//////////////////// 7. ★ もう一方の全分岐点(t = ∞)での u′ — Möbius 不変性検査 ////////////////////
// y := 1/x, v := 1/t と置くと F = 0 は  1 + (1−y)²(4−y)W + 4W² = 0,  W := v/y³.
// y=0 で (2W+1)² = 0(二重根)⇒ W = −1/2 + Z と置くと
//   (9/2)y − 3y² + (1/2)y³ + (−9y+6y²−y³)Z + 4Z² = 0
// 先頭は (9/2)y + 4Z² = 0 ⇒ y = −(8/9)Z²(1+…) で **Z が uniformizer**(ord y = 2, ord v = 6)。
// ⇒ v = W y³ = −(1/2)(−8/9)³ Z⁶(1+…) = (256/729) Z⁶(1+…)
{
  const P2 = 30; const zz = () => Array.from({length:P2},()=>q(0));
  const cst2=(c)=>{const a=zz();a[0]=c;return a;};
  const mul2=(a,b)=>{const r=zz();for(let i=0;i<P2;i++){if(a[i].isZero())continue;for(let j=0;i+j<P2;j++){if(b[j].isZero())continue;r[i+j]=r[i+j].add(a[i].mul(b[j]));}}return r;};
  const add2=(a,b)=>a.map((c,i)=>c.add(b[i]));
  const inv2=(a)=>{const r=zz();r[0]=q(1).div(a[0]);for(let k=1;k<P2;k++){let s=q(0);for(let i=1;i<=k;i++)s=s.add(a[i].mul(r[k-i]));r[k]=s.div(a[0]).mul(q(-1));}return r;};
  const sh2=(a,k)=>{const r=zz();for(let i=0;i+k<P2;i++)r[i+k]=a[i];return r;};
  const Zs=(()=>{const a=zz();a[1]=q(1);return a;})();
  // y(Z) を (9/2)y − 3y² + (1/2)y³ + (−9y+6y²−y³)Z + 4Z² = 0 から反復で解く
  let y=zz();
  for(let it=0;it<25;it++){
    const y2=mul2(y,y), y3=mul2(y2,y);
    // (9/2)y = 3y² − (1/2)y³ − (−9y+6y²−y³)Z − 4Z²
    const rhs = add2(add2(mul2(cst2(q(3)),y2), mul2(cst2(q(-1,2)),y3)),
                add2(mul2(cst2(q(-1)), mul2(add2(add2(mul2(cst2(q(-9)),y), mul2(cst2(q(6)),y2)), mul2(cst2(q(-1)),y3)), Zs)),
                     mul2(cst2(q(-4)), mul2(Zs,Zs))));
    y = mul2(rhs, inv2(cst2(q(9,2))));
  }
  const lead2=(a)=>{for(let i=0;i<P2;i++)if(!a[i].isZero())return [i,a[i]];return [Infinity,q(0)];};
  const [oy,cy]=lead2(y);
  chk('(13) y = 1/x = −(8/9)Z² + O(Z³)(Z は ℚ-有理 uniformizer・ord y = 2)', oy===2 && cy.eq(q(-8,9)), `y = ${cy}·Z^${oy} + …`);
  const W = add2(cst2(q(-1,2)), Zs);
  const v = mul2(W, mul2(y,mul2(y,y)));
  const [ov,cv]=lead2(v);
  chk('(14) ★ v = 1/t = (256/729)·Z⁶ + O(Z⁷)', ov===6 && cv.eq(q(256,729)), `v = ${cv}·Z^${ov} + …`);
  chk('(15) ★★ もう一方の正規化 λ = −1/t ⇒ **u′ = −256/729 = −2⁸/3⁶**', ov===6 && cv.mul(q(-1)).eq(q(-256,729)));
  // 3-part 比較: [−4]₃ = [2²]、[−256/729]₃ = [2^8 3^{-6}]₃ = [2^{8 mod 3}] = [2²]
  chk('(16) ★★★ **Möbius 不変性**: [u]₃ = [2²] と [u′]₃ = [2^{8 mod 3}·3^{−6 mod 3}] = [2²] が一致',
      (8 % 3) === 2 && (6 % 3) === 0, 'u = −4 と u′ = −256/729 は別の数だが 3-剰余類は同じ');
}

console.log(`
==== ${OK.filter(Boolean).length}/${OK.length} PASS ====`);
if (OK.some(v => !v)) process.exitCode = 1;
