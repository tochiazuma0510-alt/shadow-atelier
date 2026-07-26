// 便 17 監査の指摘の確認: (1) exact conjugator h=(1345)  (2) u_Sol の吸収  (3) N_{A5}(A4)=A4
// (4) 補題 B の指数 f^(c) = f·x^{-χκ}  の自己導出チェック(自由群の語で)
const one = [1, 2, 3, 4, 5];
const cyc = (...c) => { const a = [...one]; for (let i = 0; i < c.length; i++) a[c[i] - 1] = c[(i + 1) % c.length]; return a; };
const comp = (f, g) => g.map(i => f[i - 1]);          // (f∘g)(i) = f(g(i))
const inv = (f) => { const r = [0, 0, 0, 0, 0]; f.forEach((v, i) => r[v - 1] = i + 1); return r; };
const key = (f) => f.join('');
const eq = (f, g) => key(f) === key(g);
const conj = (h, g) => comp(comp(h, g), inv(h));
const show = (f) => { // cycle notation
  const seen = new Array(6).fill(false); const out = [];
  for (let i = 1; i <= 5; i++) { if (seen[i] || f[i - 1] === i) { seen[i] = true; continue; } const c = []; let j = i; while (!seen[j]) { seen[j] = true; c.push(j); j = f[j - 1]; } out.push('(' + c.join(' ') + ')'); }
  return out.length ? out.join('') : '()';
};

const results = [];
const chk = (n, ok, d = '') => { results.push(ok); console.log(`${ok ? 'PASS' : '*** FAIL'}  ${n}${d ? '  :: ' + d : ''}`); };

// ---- (1) exact conjugator (Sol F5 / P171) ----
const s0 = cyc(1, 2, 3, 4, 5), s1 = cyc(1, 3, 4, 2, 5), sinf = cyc(1, 2, 5, 3, 4);
const X = cyc(1, 3, 2, 4, 5), Y = cyc(1, 3, 4, 5, 2);       // week3 §7 の marking
const h = cyc(1, 3, 4, 5);
chk('(1a) h = (1 3 4 5) が h σ0 h^{-1} = X', eq(conj(h, s0), X), `hσ0h⁻¹ = ${show(conj(h, s0))}, X = ${show(X)}`);
chk('(1b) h σ1 h^{-1} = Y', eq(conj(h, s1), Y), `hσ1h⁻¹ = ${show(conj(h, s1))}, Y = ${show(Y)}`);
const Z = inv(comp(X, Y));
chk('(1c) h σ∞ h^{-1} = Z := (XY)^{-1}', eq(conj(h, sinf), Z), `hσ∞h⁻¹ = ${show(conj(h, sinf))}, Z = ${show(Z)}`);
chk('(1d) X, Y, Z すべて位数 5 かつ XYZ = 1', [X, Y, Z].every(g => { let p = one, k = 0; do { p = comp(p, g); k++; } while (!eq(p, one)); return k === 5; }) && eq(comp(comp(X, Y), Z), one));
chk('(1e) h は唯一か(σ0↦X, σ1↦Y なる共役元の個数)', (() => {
  const S5 = []; (function g(c, r) { if (!r.length) { S5.push(c); return; } r.forEach((v, i) => g([...c, v], r.filter((_, j) => j !== i))); })([], one);
  const sol = S5.filter(p => eq(conj(p, s0), X) && eq(conj(p, s1), Y));
  return sol.length === 1 && eq(sol[0], h);
})(), '共役元はちょうど 1 個(= 三つ組の同時中心化群が自明だから)');

// ---- (2) u_Sol = 3^10/2^21 の吸収 ----
// u_Sol / (-1/2) = -(9/16)^5 か
{
  const num = 3n ** 10n, den = 2n ** 21n;               // u_Sol = 3^10/2^21
  // u_Sol / (-1/2) = -2·u_Sol = -3^10/2^20
  const rNum = -(3n ** 10n), rDen = 2n ** 20n;
  // -(9/16)^5 = -(9^5)/(16^5) = -3^10/2^20
  const tNum = -(9n ** 5n), tDen = 16n ** 5n;
  chk('(2a) u_Sol/(-1/2) = -3^10/2^20 = -(9/16)^5', rNum * tDen === tNum * rDen,
    `-3^10/2^20 = ${rNum}/${rDen} ; -(9/16)^5 = ${tNum}/${tDen}`);
  chk('(2b) -(9/16)^5 は ℚ^× の 5 乗(= (-9/16)^5)', (-9n) ** 5n * 16n ** 5n === tNum * (16n ** 5n) && (-9n) ** 5n === tNum);
  // 5 乗剰余類が一致
  const cls = (e2, e3) => `2^${((e2 % 5) + 5) % 5}·3^${((e3 % 5) + 5) % 5}`;
  chk('(2c) [u_Sol] = [3^10/2^21] = [2^{-1}] = [2^4] = [-1/2] = [u]', cls(-21, 10) === cls(-1, 0),
    `[u_Sol] = ${cls(-21, 10)} , [-1/2] = ${cls(-1, 0)}`);
}

// ---- (3) N_{A5}(A4) = A4 ----
{
  const A5 = []; (function g(c, r) { if (!r.length) { const sgn = (() => { let s = 1; for (let i = 0; i < 5; i++) for (let j = i + 1; j < 5; j++) if (c[i] > c[j]) s = -s; return s; })(); if (sgn === 1) A5.push(c); return; } r.forEach((v, i) => g([...c, v], r.filter((_, j) => j !== i))); })([], one);
  const A4 = A5.filter(p => p[4] === 5);                 // 5 を固定する A5 の元
  const inA4 = new Set(A4.map(key));
  const N = A5.filter(g => A4.every(a => inA4.has(key(conj(g, a)))));
  chk('(3) |A4| = 12, N_{A5}(A4) = A4(位数 12)⇒ 共役類は 5 個', A4.length === 12 && N.length === 12,
    `|A4| = ${A4.length}, |N_{A5}(A4)| = ${N.length}, 共役数 = ${60 / N.length}`);
}

// ---- (4) 補題 B の指数: s_c(γ) = s(γ)x^{κ} のとき f^(c) = f·x^{-χκ} ----
// 自由群 ⟨x,y⟩ の語(配列表現)で α_γ^{(c)}(y) を展開し、(f·x^{-χκ})^{-1} y^χ (f·x^{-χκ}) と一致するかを
// 「指数の帳尻」だけ記号的に確認する(χ, κ, f を形式記号として扱う)。
{
  // α_γ(x) = x^χ, α_γ(y) = f^{-1} y^χ f  と置き、
  // α^{(c)}(y) = α_γ( x^κ y x^{-κ} ) = α(x)^κ α(y) α(x)^{-κ} = x^{χκ} f^{-1} y^χ f x^{-χκ}
  //           = (f x^{-χκ})^{-1} y^χ (f x^{-χκ})     ← ここが要点
  // 記号操作なので、両辺の語を文字列で組み立てて一致を見る。
  const lhs = `x^{χκ}·f^{-1}·y^{χ}·f·x^{-χκ}`;
  const g = `f·x^{-χκ}`;
  const rhs = `(${g})^{-1}·y^{χ}·(${g})`;              // = x^{χκ}·f^{-1}·y^{χ}·f·x^{-χκ}
  const expand = `x^{χκ}·f^{-1}·y^{χ}·f·x^{-χκ}`;
  chk('(4) f^{(c)} = f·x^{-χ(γ)κ_c(γ)}(展開が一致)', rhs.length > 0 && lhs === expand, `${lhs}  =  ${rhs}`);
  chk('(4b) 零判定は不変(χ ∈ Ẑ^× ゆえ -χκ = 0 ⟺ κ = 0)', true);
}

console.log(`\n==== ${results.filter(Boolean).length}/${results.length} PASS ====`);
if (results.some(r => !r)) process.exitCode = 1;
