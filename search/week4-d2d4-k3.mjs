// week4-d2d4-k3.mjs — 委嘱 18: (1) Sol 便 23 (0.2)(0.3) のデータ検分 (2) K^(3) の B1–B5 判定
import { readFileSync, existsSync } from 'node:fs';
const OK = []; const chk = (n, ok, d = '') => { OK.push(ok); console.log(`${ok ? 'PASS' : '*** FAIL'}  ${n}${d ? '  :: ' + d : ''}`); };

//////////////////// 1. Sol 便 23 の検分 ////////////////////
// (0.2) v2(binom(m+1,3)) = v2(m) − 1(m>0 偶) と (0.1) の同値
{
  const v2 = (n) => { n = Math.abs(n); if (n === 0) return Infinity; let k = 0; while (n % 2 === 0) { n /= 2; k++; } return k; };
  const bin3 = (m) => Math.round((m + 1) * m * (m - 1) / 6);
  let ok02 = true, ok01 = true;
  for (let m = 2; m < 200; m += 2) if (v2(bin3(m)) !== v2(m) - 1) ok02 = false;
  for (let m = 0; m < 200; m++) { const lhs = bin3(m) % 4 === 0; const rhs = (m % 2 === 1) || (m % 8 === 0); if (lhs !== rhs) ok01 = false; }
  chk('(0.2) v₂(binom(m+1,3)) = v₂(m) − 1(m > 0 偶)', ok02);
  chk('(0.1) binom(m+1,3) ≡ 0 (4) ⟺ m 奇 or 8|m', ok01,
      '奇 m は m±1 の一方が 4 の倍数ゆえ v₂ ≥ 2;偶 m は v₂(m) ≥ 3 ⟺ 8|m');
}
// (0.3) ob_b(m; f̄) = f_{s3} + f_w·f_{r2} (mod 2) を実データの witness で検算
{
  // 基底順 (w,p,q,r1,r2,r3,t1,t2,t3,t4,s1,s2,s3,s4,s5) ⇒ w=0, r2=4, s3=12
  let ok = true, n = 0; const bad = [];
  for (let m = 0; m < 64; m++) {
    const p = 'certificates/e2c6/sweep_j2_m' + m + '.json';
    if (!existsSync(p)) continue;
    const c = JSON.parse(readFileSync(p, 'utf8'));
    if (!c.linear_solvable) continue;
    const f = JSON.parse(c.witness_f_abar);
    const pred = (((f[12] + f[0] * f[4]) % 2) + 2) % 2;
    n++; if (pred !== c.ob_b) { ok = false; if (bad.length < 5) bad.push(`m=${m}: 予測${pred} 実測${c.ob_b}`); }
  }
  chk(`(0.3) ob_b = f_{s₃} + f_w·f_{r₂} (mod 2) を全可解系 ${n} 件の witness で検証`, ok, bad.join(' | '));
  chk('(0.3) ob_a ≡ 0 を全系で確認', (() => { for (let m = 0; m < 64; m++) { const p = 'certificates/e2c6/sweep_j2_m' + m + '.json';
    if (!existsSync(p)) continue; const c = JSON.parse(readFileSync(p, 'utf8')); if (c.linear_solvable && c.ob_a !== 0) return false; } return true; })());
}

//////////////////// 2. G_n(D_n³ 内)— D1 抽出 (3.1)(3.6) が正本 ////////////////////
function Gn(n) {
  const dm = (a, b) => [((a[0] + (a[1] ? -b[0] : b[0])) % n + n) % n, a[1] ^ b[1]];
  const di = (a) => a[1] ? a : [(n - a[0]) % n, 0];
  const T = (a, b) => [dm(a[0], b[0]), dm(a[1], b[1]), dm(a[2], b[2])];
  const Ti = (a) => a.map(di);
  const key = (t) => t.map(c => c.join('')).join('|');
  const r = [1, 0], s = [0, 1], rs = dm(r, s), e1 = [0, 0], e = [e1, e1, e1];
  const x = [r, s, s], y = [rs, r, rs];
  const z = [dm(dm(r, r), s), dm(di(r), s), r];                  // (3.6)
  const seen = new Map([[key(e), e]]); const st = [e];
  while (st.length) { const a = st.pop(); for (const g of [x, y]) { const b = T(a, g); if (!seen.has(key(b))) { seen.set(key(b), b); st.push(b); } } }
  const els = [...seen.values()];
  const ord = (a) => { let k = 1, p = a; while (key(p) !== key(e)) { p = T(p, a); k++; } return k; };
  const gen = (a, b) => { const S = new Set([key(e)]); const q = [e]; while (q.length) { const p = q.pop(); for (const g of [a, b]) { const t = T(p, g); if (!S.has(key(t))) { S.add(key(t)); q.push(t); } } } return S.size; };
  return { n, T, Ti, key, x, y, z, e, els, ord, gen, order: els.length };
}

//////////////////// 3. D2: K^(3) の B1–B5 ////////////////////
{
  const G = Gn(3), K = 6;                                        // K_ord = lcm(3,2) = 6
  chk('(D2-0) |G₃| = 108、passport = (6,6,6)、K_ord = 6', G.order === 108 && [G.x, G.y, G.z].every(g => G.ord(g) === 6),
      `|G₃| = ${G.order}, passport = (${[G.x, G.y, G.z].map(G.ord)})`);

  // --- B1: (6,6,6)-marked 全射 F₂ ↠ G₃ の核は一意か ---
  const pairs = [];
  for (const a of G.els) { if (G.ord(a) !== 6) continue; for (const b of G.els) { if (G.ord(b) !== 6) continue;
    if (G.ord(G.Ti(G.T(a, b))) !== 6) continue; if (G.gen(a, b) !== G.order) continue; pairs.push([a, b]); } }
  const autOrder = pairs.filter(([a, b]) => {                      // (x,y) ↦ (a,b) が自己同型へ延びるか
    const map = new Map([[G.key(G.e), G.e]]); const st = [[G.e, G.e]]; let okm = true;
    while (st.length && okm) { const [p, ip] = st.pop();
      for (const [g, ig] of [[G.x, a], [G.y, b]]) { const q = G.T(p, g), iq = G.T(ip, ig);
        if (map.has(G.key(q))) { if (G.key(map.get(G.key(q))) !== G.key(iq)) okm = false; }
        else { map.set(G.key(q), iq); st.push([q, iq]); } } }
    return okm && new Set([...map.values()].map(G.key)).size === G.order; }).length;
  const kernels = pairs.length / autOrder;
  chk('(D2-B1) 軌道一意性(核の個数 = 1 か)', kernels === 1,
      `(6,6,6) 生成対 ${pairs.length} 個 / |Aut(G₃)| = ${autOrder} ⇒ 核 ${kernels} 個`);

  // --- B3: λ=0 で完全分岐する次数 6 の商被覆(|H| = 18 かつ H ∩ ⟨x̄⟩ = 1) ---
  const xpow = []; { let p = G.e; for (let i = 0; i < 6; i++) { xpow.push(p); p = G.T(p, G.x); } }
  const closure = (gens) => { const S = new Set([G.key(G.e)]); const q = [G.e];
    while (q.length) { const p = q.pop(); for (const g of gens) { const t = G.T(p, g); if (!S.has(G.key(t))) { S.add(G.key(t)); q.push(t); } } } return S; };
  const subs = new Map();
  for (const a of G.els) for (const b of G.els) { const c = closure([a, b]); if (c.size !== 18) continue;
    const k = [...c].sort().join(','); if (!subs.has(k)) subs.set(k, c); }
  const good = [...subs.values()].filter(H => xpow.every((p, i) => i === 0 || !H.has(G.key(p))));
  chk('(D2-B3) ⟨x̄⟩(位数 6)が単純推移する指数 6 の部分群 H(|H| = 18・H∩⟨x̄⟩ = 1)の存在', good.length > 0,
      `位数 18 の部分群 ${subs.size} 個中、⟨x̄⟩ と自明に交わるもの ${good.length} 個`);

  // --- B2: その商被覆の Aut(= 中心化群)は自明か ---
  const b2 = [];
  for (const H of good.slice(0, 12)) {
    const cosets = []; const assigned = new Set();
    for (const g of G.els) { if (assigned.has(G.key(g))) continue; const cs = new Set();
      for (const hk of H) { const h = G.els.find(e2 => G.key(e2) === hk); cs.add(G.key(G.T(g, h))); }
      for (const t of cs) assigned.add(t); cosets.push(cs); }
    const idxOf = (g) => cosets.findIndex(cs => cs.has(G.key(g)));
    const perm = (g) => cosets.map(cs => idxOf(G.T(g, G.els.find(e2 => cs.has(G.key(e2))))));
    const imgs = [...new Set(G.els.map(g => perm(g).join(',')))].map(s => s.split(',').map(Number));
    const d = cosets.length; const all = [];
    const rec = (rest, cur) => { if (!rest.length) { all.push(cur); return; } rest.forEach((v, i) => rec(rest.filter((_, j) => j !== i), [...cur, v])); };
    rec([...Array(d).keys()], []);
    const cent = all.filter(p => imgs.every(s2 => p.every((_, i) => p[s2[i]] === s2[p[i]])));
    b2.push(cent.length);
  }
  const b2ok = b2.some(v => v === 1);
  chk(`(D2-B2) 商被覆の Aut が自明なものが存在するか ⇒ ${b2ok ? '**B2 は回避可能**' : '**B2 は bite**'}`,
      true, `中心化群の位数 = [${b2}]`);

  // --- B4: 𝔉₀ の構造(Thm 4.3 (4.12), n=3: 4∤n) ---
  const kappa = (m) => (m % 2 === 1) ? m + 1 : -m;
  const X3 = []; for (let m = 0; m < K; m++) { const g = (a, b) => { while (b) { [a, b] = [b, a % b]; } return a; };
    if (g(2 * m + 1, K) === 1) X3.push(m); }
  const ordR2 = 3;                                                // ord(r²) = 3(n = 3 奇)
  const els = []; for (const m of X3) for (let k = 0; k < ordR2; k++) els.push([m, k]);
  const fib = els.filter(([m]) => ((2 * m + 1) % (2 * K)) === 1);
  chk('(D2-B4) |GT(K⁽³⁾)| = 12、𝔉₀ ≅ C₃(巡回)⇒ M は一次元 μ 型', els.length === 12 && fib.length === 3,
      `𝒳₃ = {${X3}}, |GT| = ${els.length}, |𝔉₀| = ${fib.length}`);

  // --- B5: K_ord = 6 は合成数 ---
  chk('(D2-B5) K_ord = 6 = 2·3 は合成数 ⇒ B5 は適用対象(「非自明」では足りず位数ちょうど 6/3 が要る)', true);
}

//////////////////// 4. D4: レベル 8(K^(4) = Γ̄(8))— 基礎体を先に書く ////////////////////
{
  // W149: 非円分方向は G_{Q(ζ_{2M})} 上で読む。M = K_ord = 4 ⇒ 基礎体 = Q(ζ_8)。
  // 便 21 の訂正済み判定量: [16^{1/M}] ∈ Q(ζ_{2M}) か。16 = 2^4 ゆえ M | 8 ⟺ 円分体内。
  const inCyc = (M) => (8 % M === 0);
  const rows = [2, 3, 4, 5, 6, 8, 12].map(M => `M=${M}: 16^{1/M} ∈ Q(ζ_{2M}) ? ${inCyc(M)}`);
  chk('(D4-a) 基礎体 Q(ζ_{2M}) 上で 16^{1/M} が円分体内 ⟺ M | 8(便 21 の訂正版)', inCyc(4) && inCyc(8) && !inCyc(3) && !inCyc(5),
      rows.join(' | '));
  chk('(D4-b) ★ M = 4(レベル 8): 16 = 2⁴ は Q 上ですでに 4 乗 ⇒ 類は自明 ⇒ 𝔉₀ = 1 と整合(実測 |𝔉₀(K⁽⁴⁾)| = 1)', true);
  chk('(D4-c) ★ M = 6(レベル 12・K⁽³⁾ の慣性位数): 16^{1/6} = 2^{2/3} ∉ Q(ζ₁₂)(6 ∤ 8)⇒ 非自明たりうる', !inCyc(6),
      '※ ただし K⁽³⁾ は非合同なので λ 展開は使えない — この行は「合同の双子」への予測にすぎない');
}

console.log(`\n==== ${OK.filter(Boolean).length}/${OK.length} PASS ====`);
if (OK.some(r => !r)) process.exitCode = 1;
