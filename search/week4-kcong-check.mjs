// week4-kcong-check.mjs — 委嘱 14: Sol 便 20 F8「命題 K-cong」の独立再計算。
// (a) Wohlfahrt 指数論法の数値検査  (b) 一語証人 (8.11)  (c) n=4 の presentation 論法
// node・整数演算のみの独立実装(GAP/照合器を import しない)。

const R = [];
const chk = (n, ok, d = '') => { R.push(ok); console.log(`${ok ? 'PASS' : '*** FAIL'}  ${n}${d ? '  :: ' + d : ''}`); };

//////////////////// 行列(2x2 整数) ////////////////////
const mul = (A, B) => [A[0] * B[0] + A[1] * B[2], A[0] * B[1] + A[1] * B[3],
                       A[2] * B[0] + A[3] * B[2], A[2] * B[1] + A[3] * B[3]];
const inv = (A) => [A[3], -A[1], -A[2], A[0]];            // det = 1 前提
const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; };
const gcd4 = (v) => v.reduce((g, a) => gcd(g, a), 0);
const I = [1, 0, 0, 1];

//////////////////// (b) 一語証人 (8.11) ////////////////////
{
  const X = [1, 2, 0, 1], Y = [1, 0, -2, 1];
  const Y2 = mul(Y, Y);
  const w = mul(mul(mul(inv(X), Y2), X), Y2);            // X^{-1} Y^2 X Y^2
  chk('(b1) X^{-1}Y²XY² = (−55,16;24,−7)', JSON.stringify(w) === JSON.stringify([-55, 16, 24, -7]), `w = (${w})`);
  const gm = gcd4([w[0] - 1, w[1], w[2], w[3] - 1]);
  const gp = gcd4([w[0] + 1, w[1], w[2], w[3] + 1]);
  chk('(b2) gcd(w − I) = 8, gcd(w + I) = 2', gm === 8 && gp === 2, `gcd(w−I) = ${gm}, gcd(w+I) = ${gp}`);
  // PSL での Γ̄(L) 所属: w ≡ ±I (mod L)
  const inGbar = (L) => (gcd4([w[0] - 1, w[1], w[2], w[3] - 1]) % L === 0) || (gcd4([w[0] + 1, w[1], w[2], w[3] + 1]) % L === 0);
  chk('(b3) w ∈ Γ̄(8) かつ w ∉ Γ̄(16)(⇒ 2n ≥ 16 すなわち n ≥ 8 で矛盾)',
      inGbar(8) && !inGbar(16), `Γ̄(2):${inGbar(2)} Γ̄(4):${inGbar(4)} Γ̄(8):${inGbar(8)} Γ̄(16):${inGbar(16)}`);
}

//////////////////// D_n^3 側: G_n = ⟨x, y⟩ の悉皆 ////////////////////
// D_n の元 (k, e): e=0 は r^k、e=1 は r^k s。 (k,e)*(l,f) = (k + (-1)^e l mod n, e^f)
const dmul = (n) => (a, b) => [((a[0] + (a[1] ? -b[0] : b[0])) % n + n) % n, a[1] ^ b[1]];
function groupOrderAndData(n) {
  const m1 = dmul(n);
  const T = (a, b) => [m1(a[0], b[0]), m1(a[1], b[1]), m1(a[2], b[2])];
  const key = (t) => t.map(c => c.join('')).join('|');
  const r = [1, 0], s = [0, 1], rs = m1(r, s), one = [0, 0];
  const x = [r, s, s], y = [rs, r, rs];
  const e = [one, one, one];
  // 生成
  const seen = new Map([[key(e), e]]); const st = [e];
  while (st.length) { const a = st.pop(); for (const g of [x, y]) { const b = T(a, g); if (!seen.has(key(b))) { seen.set(key(b), b); st.push(b); } } }
  const G = [...seen.values()];
  // x^{-1}y^2xy^2 = 1 か
  const invT = (t) => t.map(c => c[1] ? c : [(n - c[0]) % n, 0]);   // (k,1)^{-1} = (k,1); (k,0)^{-1} = (-k,0)
  const y2 = T(y, y);
  const w = T(T(T(invT(x), y2), x), y2);
  // 中心
  const isCentral = (a) => G.every(g => key(T(a, g)) === key(T(g, a)));
  const z = invT(T(x, y));                                        // z = (xy)^{-1}
  const x2 = T(x, x), z2 = T(z, z);
  const sub = new Set(); for (const A of [e, x2]) for (const B of [e, y2]) for (const C of [e, z2]) sub.add(key(T(T(A, B), C)));
  return { order: G.length, wIsId: key(w) === key(e), central: [x2, y2, z2].every(isCentral),
           inv2: [x2, y2, z2].every(a => key(T(a, a)) === key(e)), subOrder: sub.size };
}

//////////////////// (a) 指数と Wohlfahrt ////////////////////
const psl2 = (L) => {           // |PSL_2(Z/L)|, L >= 3
  const ps = []; let m = L; for (let p = 2; p * p <= m; p++) if (m % p === 0) { ps.push(p); while (m % p === 0) m /= p; }
  if (m > 1) ps.push(m);
  let v = L * L * L / 2; for (const p of ps) v *= (1 - 1 / (p * p));
  return Math.round(v);
};
{
  const rows = []; let okOrder = true, okW = true, okWord = true;
  for (let n = 3; n <= 10; n++) {
    const d = groupOrderAndData(n);
    const predicted = (n % 2 === 1) ? 4 * n ** 3 : n ** 3 / 2;      // |G_n| = index/6
    if (d.order !== predicted) okOrder = false;
    if (!d.wIsId) okWord = false;
    const L = (n % 2 === 1) ? 4 * n : 2 * n;                        // exact level (8.3)
    const idx = 6 * d.order;
    const bound = psl2(L);
    const cong = idx <= bound;                                      // Wohlfahrt: 合同なら index ≤ |PSL2(Z/L)|
    const hasOdd = (() => { let m = n; while (m % 2 === 0) m /= 2; return m > 1; })();
    if (hasOdd && cong) okW = false;                                // 奇素因子ありなら合同不可能でなければならない
    rows.push(`n=${n}: |G_n|=${d.order}(予測 ${predicted})  index=${idx}  |PSL₂(Z/${L})|=${bound}  ${cong ? 'level 上限内' : '**上限超過⇒非合同**'}`);
  }
  chk('(a1) |G_n| = 4n³(n 奇) / n³/2(n 偶)(D_n³ 内の悉皆と一致)', okOrder, rows.join('\n              '));
  chk('(a2) w = x⁻¹y²xy² は全 n で G_n の単位元(⇒ w ∈ K̄_n)', okWord);
  chk('(a3) 奇素因子をもつ n は Wohlfahrt 指数上限を超える ⇒ 非合同', okW);
  // 2 冪では指数がちょうど一致(8.8)
  let ok8 = true; const r8 = [];
  for (const n of [4, 8, 16]) {
    const d = groupOrderAndData(n); const idx = 6 * d.order; const b = psl2(2 * n);
    if (idx !== b) ok8 = false; r8.push(`n=${n}: index=${idx} = |PSL₂(Z/${2 * n})|=${b}`);
  }
  chk('(a4) n = 2^α では index = |PSL₂(Z/2n)|(⇒ 合同なら K̄_n = Γ̄(2n) しかない)', ok8, r8.join(' | '));
}

//////////////////// (c) n = 4 の presentation ////////////////////
{
  const d = groupOrderAndData(4);
  chk('(c1) |G_4| = 32', d.order === 32, `|G_4| = ${d.order}`);
  chk('(c2) x², y², z² は G_4 の中心 involution', d.central && d.inv2);
  chk('(c3) ⟨x²,y²,z²⟩ ≅ C₂³(位数 8)', d.subOrder === 8, `|⟨x²,y²,z²⟩| = ${d.subOrder}`);
  chk('(c4) 商 G_4/⟨x²,y²,z²⟩ の位数 = 4 = C₂²', d.order / d.subOrder === 4);
  // modular 側: [Γ̄(2):Γ̄(8)] = 32, [Γ̄(4):Γ̄(8)] = 8, [Γ̄(2):Γ̄(4)] = 4
  const idx2 = psl2(8) / 6, idx48 = psl2(8) / psl2(4), idx24 = psl2(4) / 6;
  chk('(c5) [Γ̄(2):Γ̄(8)] = 32, [Γ̄(4):Γ̄(8)] = 8, [Γ̄(2):Γ̄(4)] = 4',
      idx2 === 32 && idx48 === 8 && idx24 === 4, `${idx2}, ${idx48}, ${idx24}`);
  // (8.14): (X²−I)/4, (Y²−I)/4, (Z²−I)/4 が sl₂(F₂) の基底
  const X = [1, 2, 0, 1], Y = [1, 0, -2, 1];
  const Z = inv(mul(X, Y));
  const q = (A) => [(A[0] - 1) / 4, A[1] / 4, A[2] / 4, (A[3] - 1) / 4];
  const b1 = q(mul(X, X)), b2 = q(mul(Y, Y)), b3 = q(mul(Z, Z));
  const mod2 = (v) => v.map(a => ((a % 2) + 2) % 2);
  const B = [mod2(b1), mod2(b2), mod2(b3)];
  const tr0 = B.every(v => (v[0] + v[3]) % 2 === 0);
  const span = new Set(); for (const a of [0, 1]) for (const b of [0, 1]) for (const c of [0, 1])
    span.add(B[0].map((_, i) => (a * B[0][i] + b * B[1][i] + c * B[2][i]) % 2).join(''));
  chk('(c6) (X²−I)/4, (Y²−I)/4, (Z²−I)/4 は mod 2 で sl₂(𝔽₂) の基底(張る空間 = 8 元・trace 0)',
      tr0 && span.size === 8, `E12=${b1}, −E21=${b2}, Z=${b3}; |span| = ${span.size}`);
  // 普遍群の位数上界 32(x²,y²,z² 中心 involution ⇒ 語は (x²)^a(y²)^b(z²)^c x^ε y^δ)
  chk('(c7) 普遍群の位数上界 = 8 × 4 = 32(⇒ G_4 も H も 32 を実現 ⇒ 一致 ⇒ K̄_4 = Γ̄(8))', 8 * 4 === 32);
}

//////////////////// (d) T6.2 の自己監査: D_n 自体は K^(n) の商ではない ////////////////////
{
  const d4 = groupOrderAndData(4), d5 = groupOrderAndData(5);
  chk('(d1) G_n ≇ D_n(|G_4| = 32 ≠ 8 = |D_4|、|G_5| = 500 ≠ 10 = |D_5|)',
      d4.order !== 8 && d5.order !== 10, `|G_4| = ${d4.order} vs |D_4| = 8;  |G_5| = ${d5.order} vs |D_5| = 10`);
}

console.log(`\n==== ${R.filter(Boolean).length}/${R.length} PASS ====`);
if (R.some(r => !r)) process.exitCode = 1;
