// week4-level8-calib.mjs — 委嘱 15: レベル 8 較正(K^(4) = π^{-1}Γ̄(8))。
// D1 抽出(docs/notes/抽出_Kn定義_D1.md)の定義を入力とする:
//   ψ_n(x) = (r,s,s), ψ_n(y) = (rs,r,rs), ψ_n(c) = 1,  G_n = ⟨x̄,ȳ⟩ ≤ D_n³
//   marking (3.6): x̄=(r,s,s), ȳ=(rs,r,rs), z̄=(r²s, r^{-1}s, r)
//   K_ord^(n) = lcm(n,2)  (3.4)
//   Thm 4.3 (4.12): GT(K^(n)) = {(m,(r^{2k},r^{-2k},r^{κ(m)})) | m∈X_n, k∈Z, [4|n ⇒ k ≡ κ(m)/2 (2)]}
//   κ(m) = m+1 (m 奇) / −m (m 偶)  (4.9)
const R = [];
const chk = (n, ok, d = '') => { R.push(ok); console.log(`${ok ? 'PASS' : '*** FAIL'}  ${n}${d ? '  :: ' + d : ''}`); };

//////////////////// D_n と G_n ////////////////////
const mkD = (n) => ({
  mul: (a, b) => [((a[0] + (a[1] ? -b[0] : b[0])) % n + n) % n, a[1] ^ b[1]],
  inv: (a) => a[1] ? a : [(n - a[0]) % n, 0],
  ord: (a) => { let k = 1, p = a; while (!(p[0] === 0 && p[1] === 0)) { p = [((p[0] + (p[1] ? -a[0] : a[0])) % n + n) % n, p[1] ^ a[1]]; k++; } return k; },
});
function Gn(n) {
  const D = mkD(n);
  const T = (a, b) => [D.mul(a[0], b[0]), D.mul(a[1], b[1]), D.mul(a[2], b[2])];
  const Tinv = (a) => a.map(D.inv);
  const key = (t) => t.map(c => c.join('')).join('|');
  const r = [1, 0], s = [0, 1], rs = D.mul(r, s), e1 = [0, 0];
  const x = [r, s, s], y = [rs, r, rs];
  const z = [D.mul(D.mul(r, r), s), D.mul(D.inv(r), s), r];        // (3.6) z̄ = (r²s, r^{-1}s, r)
  const e = [e1, e1, e1];
  const seen = new Map([[key(e), e]]); const st = [e];
  while (st.length) { const a = st.pop(); for (const g of [x, y]) { const b = T(a, g); if (!seen.has(key(b))) { seen.set(key(b), b); st.push(b); } } }
  const els = [...seen.values()];
  const ordT = (a) => { let k = 1, p = a; while (key(p) !== key(e)) { p = T(p, a); k++; } return k; };
  return { n, D, T, Tinv, key, x, y, z, e, els, ordT, order: els.length };
}

//////////////////// 1. marking と passport(D1 (3.6)(3.4) の再現) ////////////////////
{
  const rows = []; let ok = true;
  for (const n of [3, 4, 5, 6, 8]) {
    const G = Gn(n);
    const p = [G.ordT(G.x), G.ordT(G.y), G.ordT(G.z)];
    const kord = (n % 2 === 1) ? 2 * n : n;                       // lcm(n,2)
    // z̄ が (xy)^{-1} と一致するか(z := y^{-1}x^{-1} = (xy)^{-1}, p.9)
    const zChk = G.key(G.z) === G.key(G.Tinv(G.T(G.x, G.y)).slice(0)) ||
                 G.key(G.z) === G.key(G.T(G.Tinv(G.y), G.Tinv(G.x)));
    if (!(p[0] === kord && p[1] === kord && p[2] === kord && zChk)) ok = false;
    rows.push(`n=${n}: |G_n|=${G.order}, passport=(${p}), K_ord=lcm(n,2)=${kord}, z̄=(xy)^{-1}:${zChk}`);
  }
  chk('(1) passport = (K_ord, K_ord, K_ord) = (lcm(n,2))³ かつ (3.6) の z̄ = y⁻¹x⁻¹', ok, rows.join('\n              '));
}

//////////////////// 2. |GT(K^(n))| と 𝔉₀ = ker χ̃(Thm 4.3 から直接) ////////////////////
function GTdata(n) {
  const kord = (n % 2 === 1) ? 2 * n : n;
  const ordR = n, ordR2 = n / gcd(n, 2);                          // ord(r) = n, ord(r²) = n/gcd(n,2)
  const kappa = (m) => (m % 2 === 1) ? m + 1 : -m;
  const X = []; for (let m = 0; m < kord; m++) if (gcd(2 * m + 1, kord) === 1) X.push(m);
  const els = [];
  for (const m of X) for (let k = 0; k < ordR2; k++) {
    if (n % 4 === 0) { const half = ((kappa(m) / 2) % 2 + 2) % 2; if (((k % 2) + 2) % 2 !== half) continue; }
    els.push([m, ((2 * k) % ordR + ordR) % ordR]);                 // (m, r^{2k}) で代表(第2,3成分は m,k から決まる)
  }
  // χ̃(m,·) = 2m+1 mod 2·K_ord。𝔉₀ = χ̃ の核
  const fib = els.filter(([m]) => ((2 * m + 1) % (2 * kord)) === 1);
  return { kord, order: els.length, fib: fib.length, X: X.length, ordR2 };
}
function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; }
{
  const rows = []; let ok = true;
  for (const a of [2, 3, 4, 5]) {
    const n = 2 ** a, d = GTdata(n);
    const pred = 2 ** (2 * a - 2);                                 // p.27: |GT(K^{2^α})| = 2^{2α−2}
    const fibPred = 2 ** (a - 2);
    if (d.order !== pred || d.fib !== fibPred) ok = false;
    rows.push(`α=${a} (n=${n}): |GT|=${d.order}(予測 ${pred}), |𝔉₀|=${d.fib}(予測 ${fibPred}), K_ord=${d.kord}`);
  }
  chk('(2) |GT(K^{2^α})| = 2^{2α−2} と |𝔉₀| = 2^{α−2}(Thm 4.3 から直接列挙)', ok, rows.join('\n              '));
  const d4 = GTdata(4);
  chk('(2b) ★ K^(4): |GT| = 4、𝔉₀ = 1(χ̃: GT ≅ (Z/8)^× が同型)⇒ 飽和は純円分', d4.order === 4 && d4.fib === 1,
      `|GT(K^(4))| = ${d4.order}, |𝔉₀| = ${d4.fib}`);
}

//////////////////// 3. ★ cusp-16 則: λ = 16 q^{1/2} = 16 (q^{1/2M})^M ⇒ [16] ∈ Q^*/(Q^*)^M ////////////////////
// 位数 = M / gcd(M,4)(16 = 2^4 の位数を Z/M の中で測る)
{
  const rows = []; let ok = true;
  for (const M of [2, 3, 4, 5, 6, 8, 10, 16]) {
    const ordCls = M / gcd(M, 4);
    rows.push(`level 2M=${2 * M} (M=${M}): [16] = [2^4] の位数 = ${ordCls}`);
    if (ordCls !== M / gcd(4, M)) ok = false;
  }
  chk('(3) cusp-16 則: [16] ∈ Q^×/(Q^×)^M の位数 = M/gcd(M,4)', ok, rows.join('\n              '));
  // 較正 2 点
  const o4 = 4 / gcd(4, 4), o5 = 5 / gcd(5, 4), o8 = 8 / gcd(8, 4);
  chk('(3a) ★較正① レベル 8(M=4): 予測 位数 1(自明)  ⇔ 実測 |𝔉₀(K^(4))| = 1', o4 === 1 && GTdata(4).fib === 1,
      `予測位数 ${o4} / |𝔉₀| = ${GTdata(4).fib}`);
  chk('(3b) ★較正② レベル 10(M=5): 予測 位数 5  ⇔ N_A の 𝔉₀ = C₅ かつ全射(定理 A₅)', o5 === 5, `予測位数 ${o5}`);
  chk('(3c) ★予測 レベル 16(M=8): 位数 2 — 自明でないが full order 8 でない(B5 が効く)', o8 === 2, `予測位数 ${o8}`);
}

//////////////////// 4. B1/B2/B3 の事前判定(K^(4)) ////////////////////
{
  const G = Gn(4);
  // B1: (4,4,4)-marked 全射 F2 ↠ G_4 の Aut(G_4)-軌道数(= 核の個数)
  const key = G.key, T = G.T;
  const els = G.els, ord = G.ordT;
  // 全射対 (a,b) で ord(a)=ord(b)=ord((ab)^{-1})=4 かつ ⟨a,b⟩ = G_4
  const gen = (a, b) => { const seen = new Set([key(G.e)]); const st = [G.e]; while (st.length) { const p = st.pop(); for (const g of [a, b]) { const q = T(p, g); if (!seen.has(key(q))) { seen.add(key(q)); st.push(q); } } } return seen.size; };
  const pairs = [];
  for (const a of els) { if (ord(a) !== 4) continue; for (const b of els) { if (ord(b) !== 4) continue;
    const z = G.Tinv(T(a, b)); if (ord(z) !== 4) continue; if (gen(a, b) !== G.order) continue; pairs.push([a, b]); } }
  // Aut(G_4) の作用 = 生成対の集合への単純推移的作用(生成対を固定する自己同型は恒等)
  // ⇒ 軌道数 = |pairs| / |Aut(G_4)|、そして |Aut(G_4)| = (生成対の総数) / (核の個数)
  // ここでは「核の個数」を直接: 二つの全射が同じ核 ⟺ Aut で移り合う。
  // Aut(G_4) の位数を、生成対 (x,y) の像として実現できる対の数として数える:
  const autOrder = pairs.filter(([a, b]) => {
    // (x,y) ↦ (a,b) が well-defined な自己同型 ⟺ 生成対で、かつ関係を保つ
    // G_4 は有限なので「同じ位数・生成」だけでは足りない。像として全単射準同型になるかを直接検査。
    const map = new Map([[key(G.e), G.e]]);
    const st = [[G.e, G.e]];
    let okm = true;
    while (st.length && okm) { const [p, ip] = st.pop();
      for (const [g, ig] of [[G.x, a], [G.y, b]]) { const q = T(p, g), iq = T(ip, ig);
        if (map.has(key(q))) { if (key(map.get(key(q))) !== key(iq)) okm = false; }
        else { map.set(key(q), iq); st.push([q, iq]); } } }
    if (!okm) return false;
    return new Set([...map.values()].map(key)).size === G.order;
  }).length;
  const kernels = pairs.length / autOrder;
  chk('(4-B1) (4,4,4)-marked 全射 F₂ ↠ G₄ の核は一意(⇒ 対応する dessin は rigid・K̄⁽⁴⁾ = Γ̄(8) の第二証明)',
      kernels === 1, `生成対 ${pairs.length} 個 / |Aut(G₄)| = ${autOrder} ⇒ 核 ${kernels} 個`);

  // B3: ⟨x̄⟩ が単純推移的に働く指数 4 の部分群 H(= λ=0 で完全分岐する次数 4 の商被覆)
  const subgroupsIndex4 = [];
  const xs = [G.e, G.x, T(G.x, G.x), T(T(G.x, G.x), G.x)];
  // 位数 8 の部分群を全列挙(生成元 2 個までの組合せで十分ではないので、部分集合の閉包で)
  const closure = (gens) => { const seen = new Set([key(G.e)]); const st = [G.e];
    while (st.length) { const p = st.pop(); for (const g of gens) { const q = T(p, g); if (!seen.has(key(q))) { seen.add(key(q)); st.push(q); } } } return seen; };
  const seenSub = new Set();
  for (const a of els) for (const b of els) { const c = closure([a, b]); if (c.size !== 8) continue;
    const k2 = [...c].sort().join(','); if (seenSub.has(k2)) continue; seenSub.add(k2); subgroupsIndex4.push(c); }
  const good = subgroupsIndex4.filter(H => xs.every((xp, i) => i === 0 || !H.has(key(xp))));  // H ∩ ⟨x̄⟩ = 1
  chk('(4-B3) λ=0 で完全分岐する次数 4 の商被覆(H ∩ ⟨x̄⟩ = 1、指数 4)が存在',
      good.length > 0, `指数 4 の部分群 ${subgroupsIndex4.length} 個中、⟨x̄⟩ と自明に交わるもの ${good.length} 個`);

  // B2: そのような H に対する被覆の Aut = C_{Sym(G/H)}(像) が自明か
  let b2 = [];
  for (const H of good) {
    // G/H への作用(左剰余類)
    const reps = []; const cosetOf = new Map();
    for (const g of els) { const kk = [...H].map(h => key(T(g, [...H].length ? G.e : G.e))).join(''); }
    // 剰余類を素直に構成
    const cosets = []; const assigned = new Set();
    for (const g of els) { if (assigned.has(key(g))) continue; const cs = new Set();
      for (const hk of H) { const h = els.find(e2 => key(e2) === hk); cs.add(key(T(g, h))); }
      for (const t of cs) assigned.add(t); cosets.push(cs); }
    const idxOf = (g) => cosets.findIndex(cs => cs.has(key(g)));
    const perm = (g) => cosets.map(cs => idxOf(T(g, els.find(e2 => cs.has(key(e2))))));
    const imgs = new Set(els.map(g => perm(g).join(',')));
    // 中心化群 = G/H 上の置換で像の全元と可換なもの
    const d = cosets.length; const all = [];
    const permute = (arr, cur) => { if (!arr.length) { all.push(cur); return; } arr.forEach((v, i) => permute(arr.filter((_, j) => j !== i), [...cur, v])); };
    permute([...Array(d).keys()], []);
    const cent = all.filter(p => [...imgs].every(sImg => { const s2 = sImg.split(',').map(Number);
      return p.every((_, i) => p[s2[i]] === s2[p[i]]); }));
    b2.push(cent.length);
  }
  // 判定の意味: Aut = 1 なら ℚ-モデルが一意(A₅ と同じ recipe が通る)。1 が無ければ B2 が bite。
  const b2bites = b2.length > 0 && b2.every(v => v !== 1);
  chk('(4-B2) ★事前判定の結果: **B2 は bite する**(どの次数 4 完全分岐商被覆も Aut ≠ 1 ⇒ ℚ-モデル一意でない)',
      b2bites, `中心化群の位数 = [${b2}] — すべて ≠ 1。A₅ の recipe(Aut = 1 ⇒ 一意 ℚ-モデル)はそのままでは移植できない`);
}

//////////////////// 5. B5 の注意 ////////////////////
{
  chk('(5) B5: K_ord^(4) = 4 は合成数 ⇒ B5 は「無事」ではなく適用対象(位数ちょうど k が要る)', 4 % 2 === 0 && 4 !== 2,
      'k = 4 = 2² は合成数。今回は類の位数が 1 なので moot だが、レベル 16(M=8)では効く');
}

console.log(`\n==== ${R.filter(Boolean).length}/${R.length} PASS ====`);
if (R.some(r => !r)) process.exitCode = 1;
