// TB4 導出の数値サニティチェック(証明ではない・浮動小数点)
// 目的: 反時計回りループ γ0 に沿う解析接続が、繊維の標識を j -> j+1 (= ζ_n 倍) にすることの機械確認。
// 入力: 一般的な玩具データのみ。K^(5) の個別モデル候補・係数・数値近似・database には一切接触しない。

const C = {
  add: (a, b) => [a[0] + b[0], a[1] + b[1]],
  sub: (a, b) => [a[0] - b[0], a[1] - b[1]],
  mul: (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]],
  div: (a, b) => { const d = b[0] * b[0] + b[1] * b[1]; return [(a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d]; },
  abs: (a) => Math.hypot(a[0], a[1]),
  exp2pi: (t) => [Math.cos(2 * Math.PI * t), Math.sin(2 * Math.PI * t)],
  pow: (a, k) => { let r = [1, 0]; for (let i = 0; i < k; i++) r = C.mul(r, a); return r; },
};

let pass = 0, fail = 0;
const chk = (name, cond, extra = '') => { if (cond) { pass++; console.log(`  PASS  ${name} ${extra}`); } else { fail++; console.log(`  FAIL  ${name} ${extra}`); } };

// ---- 検査 1: Kummer 被覆 C_n : w^n = β。反時計回り一周での標識の動き ----
// 繊維の標識: j <-> ζ_n^j * δ^{1/n}  (ζ_n = e^{2πi/n}, δ^{1/n} > 0)
function kummerMonodromy(n, delta, steps) {
  const res = [];
  for (let j = 0; j < n; j++) {
    // 出発点 = 標識 j
    let w = C.mul(C.exp2pi(j / n), [Math.pow(delta, 1 / n), 0]);
    for (let k = 1; k <= steps; k++) {
      const beta = C.mul([delta, 0], C.exp2pi(k / steps));
      // w^n = beta の n 根のうち直前の w に最も近いものを選ぶ(連続分岐追跡)
      const r = Math.pow(C.abs(beta), 1 / n);
      const th = Math.atan2(beta[1], beta[0]) / (2 * Math.PI);
      let best = null, bd = Infinity;
      for (let m = 0; m < n; m++) {
        const cand = C.mul([r, 0], C.exp2pi((th + m) / n));
        const d = C.abs(C.sub(cand, w));
        if (d < bd) { bd = d; best = cand; }
      }
      w = best;
    }
    // 終点の標識を読む
    const ratio = C.div(w, [Math.pow(delta, 1 / n), 0]);
    let lab = Math.round(Math.atan2(ratio[1], ratio[0]) / (2 * Math.PI) * n);
    lab = ((lab % n) + n) % n;
    res.push(lab);
  }
  return res;
}

console.log('検査 1: Kummer 被覆 w^n = β の反時計回りモノドロミー(期待: j -> j+1 mod n)');
for (const n of [2, 3, 5, 6, 10, 12, 20]) {
  const perm = kummerMonodromy(n, 0.3, 4000);
  const want = [...Array(n).keys()].map((j) => (j + 1) % n);
  chk(`n=${n}`, JSON.stringify(perm) === JSON.stringify(want), `perm=[${perm}]`);
}

// ---- 検査 2: 局所 Kummer 形 λ = u s^M (1 + c1 s + c2 s^2) ----
// 補題 B-5(iii)/B-6 の第 1 段の状況。β = λ を反時計回りに回したとき
// 正規化座標 s~ = s * h^{1/M} が ζ_M 倍されるか(⇔ s(1)/s(0) = ζ_M)を見る。
function localKummerMonodromy(M, u, c1, c2, delta, steps) {
  const lam = (s) => C.mul([u, 0], C.mul(C.pow(s, M), C.add([1, 0], C.add(C.mul([c1, 0], s), C.mul([c2, 0], C.pow(s, 2))))));
  const dlam = (s) => {
    // d/ds [ u (s^M + c1 s^{M+1} + c2 s^{M+2}) ]
    const t1 = C.mul([M, 0], C.pow(s, M - 1));
    const t2 = C.mul([c1 * (M + 1), 0], C.pow(s, M));
    const t3 = C.mul([c2 * (M + 2), 0], C.pow(s, M + 1));
    return C.mul([u, 0], C.add(t1, C.add(t2, t3)));
  };
  // 正規化 uniformizer s~ := s * h(s)^{1/M}(補題 B-5(iii) の T)。|s| 小ゆえ h は 1 の近傍で主枝で可。
  const hfun = (s) => C.add([1, 0], C.add(C.mul([c1, 0], s), C.mul([c2, 0], C.pow(s, 2))));
  const norm = (s) => {
    const h = hfun(s);
    const lr = Math.log(C.abs(h)) / M, la = Math.atan2(h[1], h[0]) / (2 * Math.PI * M);
    return C.mul(s, C.mul([Math.exp(lr), 0], C.exp2pi(la)));
  };
  const ratios = [];
  for (let j = 0; j < M; j++) {
    // 出発点: s^M ≈ δ/u の M 根のひとつ。Newton で精密化。
    let s = C.mul(C.exp2pi(j / M), [Math.pow(delta / Math.abs(u), 1 / M), 0]);
    if (u < 0) s = C.mul(s, C.exp2pi(1 / (2 * M))); // (1/u)^{1/M} の位相
    const s0start = s;
    for (let it = 0; it < 60; it++) s = C.sub(s, C.div(C.sub(lam(s), [delta, 0]), dlam(s)));
    const s0 = s;
    for (let k = 1; k <= steps; k++) {
      const beta = C.mul([delta, 0], C.exp2pi(k / steps));
      for (let it = 0; it < 60; it++) {
        const step = C.div(C.sub(lam(s), beta), dlam(s));
        s = C.sub(s, step);
        if (C.abs(step) < 1e-15) break;
      }
    }
    ratios.push([C.div(s, s0), C.div(norm(s), norm(s0))]);
    void s0start;
  }
  return ratios;
}

console.log('\n検査 2: 局所 Kummer λ = u s^M (1 + c1 s + c2 s^2) の反時計回りモノドロミー');
console.log('        正規化 uniformizer s~ = s h(s)^{1/M} が ζ_M 倍されるか(補題 B-5(iii) の T)');
for (const [M, u, c1, c2] of [[5, 1, 0, 0], [5, 3, 2, -1], [6, -1, 1, 1], [10, 3, 2, -1], [10, -7, -3, 5]]) {
  const rs = localKummerMonodromy(M, u, c1, c2, 1e-14, 3000);
  const zeta = C.exp2pi(1 / M);
  const okN = rs.every((r) => C.abs(C.sub(r[1], zeta)) < 1e-9);   // 正規化座標: 厳密に ζ_M のはず
  chk(`M=${M}, u=${u}, c=(${c1},${c2}) [s~]`, okN, `s~1/s~0 - ζ_M = ${C.abs(C.sub(rs[0][1], zeta)).toExponential(2)}`);
  // 生の s は正規化前なので O(|s|) の偏差が出る(= 正規化が不可欠であることの確認・PASS/FAIL 対象外)
  console.log(`  note  生 s の偏差 = ${C.abs(C.sub(rs[0][0], zeta)).toExponential(2)}  (|s| ≈ ${C.abs(rs[0][0]).toExponential(1)} 倍の主要項誤差; c1=0 なら 0)`);
}

// ---- 検査 3: 逆向き(時計回り)なら ζ_M^{-1} になること(= 符号の敏感性の確認) ----
console.log('\n検査 3: 時計回りにすると ζ_M^{-1}(= ε の符号が向きに敏感であることの確認)');
function kummerMonodromyCW(n, delta, steps) {
  let w = [Math.pow(delta, 1 / n), 0];
  for (let k = 1; k <= steps; k++) {
    const beta = C.mul([delta, 0], C.exp2pi(-k / steps));
    const r = Math.pow(C.abs(beta), 1 / n);
    const th = Math.atan2(beta[1], beta[0]) / (2 * Math.PI);
    let best = null, bd = Infinity;
    for (let m = 0; m < n; m++) {
      const cand = C.mul([r, 0], C.exp2pi((th + m) / n));
      const d = C.abs(C.sub(cand, w));
      if (d < bd) { bd = d; best = cand; }
    }
    w = best;
  }
  const ratio = C.div(w, [Math.pow(delta, 1 / n), 0]);
  let lab = Math.round(Math.atan2(ratio[1], ratio[0]) / (2 * Math.PI) * n);
  lab = ((lab % n) + n) % n;
  return lab;
}
for (const n of [5, 10, 20]) {
  const lab = kummerMonodromyCW(n, 0.3, 4000);
  chk(`n=${n} 時計回り`, lab === n - 1, `0 -> ${lab}(期待 ${n - 1})`);
}

// ---- 検査 4: root-object ずれ(便 48 F7.2 の countermodel)の独立再現・整数演算のみ ----
// (TB2) の系を canonical の t 乗に取ると、(*) は ε ≡ t^{-1} (mod 20)。
// 主張: b := ε^{-1} mod 10 は t mod 10 に等しい。とくに t≡3 (20) で ε≡7, b=3(Sol の値)。
console.log('\n検査 4: root-object ずれ t の countermodel(整数演算・便 48 F7.2 の独立再現)');
const inv = (a, m) => { for (let k = 1; k < m; k++) if ((a * k) % m === 1) return k; return null; };
const units20 = [1, 3, 7, 9, 11, 13, 17, 19];
const rows = [];
for (const t of units20) {
  const eps20 = inv(t, 20);              // ε ≡ t^{-1} (mod 20)
  const eps10 = eps20 % 10;
  const b = inv(eps10, 10);              // b := ε^{-1} mod 10  (BFC (2.1))
  rows.push([t, eps20, b]);
  chk(`t=${t}`, b === t % 10, `ε≡${eps20} (20), b=${b}, t mod 10 = ${t % 10}`);
}
chk('Sol の値 t=3 -> ε≡7, b=3', rows.find((r) => r[0] === 3)[1] === 7 && rows.find((r) => r[0] === 3)[2] === 3);
chk('t≡11 (20) は b=1 を与える(単一 M の観測では exact が戻らない例)', rows.find((r) => r[0] === 11)[2] === 1);

// ---- 検査 5: TB4-b-dictionary/v1 の invariant(裁定 55 + 便 49 F4.1/F10.1)----
// 【便 49 F4.1 blocker 修理】t の型を 2M と M に分ける:
//   t_2M ∈ (Z/2M)^×  : ζ_{2M}^TB2 = (ζ_{2M}^Rule1)^{t_2M}    ← (Z_{2M}-link) ⟺ t_2M = 1
//   t̄_M := t_2M mod M ∈ (Z/M)^×
//   b_cmp := ε^{-1} mod M          (BFC (2.1) 側)
//   b_op  := (t̄_M·ε)^{-1} mod M    (BFC (8.1) 側)
const M2 = 20, M = 10;
console.log('\n検査 5: TB4-b-dictionary/v1 invariant(便 49 F10.1・整数演算)');
{
  // (a) b_op = b_cmp · t̄_M^{-1} (mod M) — ε, t_2M 任意の 64 対(TB4-3 を仮定しない)
  let ok = true, n = 0;
  for (const t2 of units20) for (const e of units20) {
    const tb = t2 % M;
    const bcmp = inv(e % M, M);
    const bop = inv((tb * e) % M, M);
    if (bop !== (bcmp * inv(tb, M)) % M) ok = false;
    n++;
  }
  chk('(a) b_op = b_cmp · t̄_M^{-1} (mod M)(ε・t_2M 任意)', ok, `${n} 対検査`);

  // (b) TB4-3(ε ≡ t_2M^{-1} mod 2M)を入れると b_cmp ≡ t̄_M、b_op ≡ 1(全 t_2M)
  let okB = true; const tbl = [];
  for (const t2 of units20) {
    const e = inv(t2, M2), tb = t2 % M;
    const bcmp = inv(e % M, M), bop = inv((tb * e) % M, M);
    tbl.push(`t_20=${t2}: t̄=${tb}, b_cmp=${bcmp}, b_op=${bop}`);
    if (bcmp !== tb || bop !== 1) okB = false;
  }
  chk('(b) TB4-3 下で b_cmp ≡ t̄_M かつ b_op ≡ 1(全 t_2M)', okB, tbl[1] + ' / ' + tbl[4]);

  // (c) Z2M_link_pass => root_twist_2M = 1
  const Z2Mlink = (t2) => t2 === 1;
  chk('(c) Z2M_link ⟹ t_2M = 1', units20.every((t2) => !Z2Mlink(t2) || t2 === 1));

  // (d)(d′) ★ negative regression fixture `NF-root-link/K5`(便 50 F4.2 / T-15 の full-tuple 形)
  // 普遍含意「t_20=11 => b=1」ではない。ε は TB4-3 (ε ≡ t_20^{-1} mod 20) で束縛される。
  // 全自由変数: (M, t_20, t̄_10, ε, b_cmp, b_op, Z20-link)
  {
    const t20 = 11;
    const eps = inv(t20, M2);                  // ← TB4-3 の束縛(普遍含意ではない)
    const tb = t20 % M;
    const bcmp = inv(eps % M, M);
    const bop = inv((tb * eps) % M, M);
    const link = Z2Mlink(t20);
    const tuple = [M, t20, tb, eps, bcmp, bop, link];
    chk('(d) NF-root-link/K5 = (M,t_20,t̄_10,ε,b_cmp,b_op,link) = (10,11,1,11,1,1,false)',
        JSON.stringify(tuple) === JSON.stringify([10, 11, 1, 11, 1, 1, false]),
        `実測 = (${tuple.join(',')})`);
    chk("(d′) 同 fixture で b_cmp = b_op = 1 かつ link = false(どちらの b でも link は戻らない)",
        bcmp === 1 && bop === 1 && link === false);
  }
  // 核の完全一致検査(便 51 F4: ラベル過大の解消 — units を列挙して集合比較する)
  const gcd = (a, b) => (b ? gcd(b, a % b) : a);
  const units = (n) => [...Array(n).keys()].filter((u) => gcd(u, n) === 1);
  const kernelOf = (n2, n1) => units(n2).filter((u) => u % n1 === 1);   // ker((Z/n2)^× -> (Z/n1)^×)

  // (e) NF-root-link/K3: level 12 の equality を level 6 の指数から復元しない(型警告)
  {
    const ker = kernelOf(12, 6);
    chk('(e) ker((Z/12)^× → (Z/6)^×) = {1,7}(units 列挙による完全一致)',
        JSON.stringify(ker) === JSON.stringify([1, 7]), `実測 ker = {${ker}}`);
    const t12 = 7;
    chk('(e′) NF-root-link/K3 = (M,t_12,t̄_6) = (6,7,1) かつ t_12 ∈ ker∖{1}',
        t12 % 6 === 1 && t12 !== 1 && ker.includes(t12));
  }
  // (f) K5 側の核も同じ形式で検査(§3.5.1 の反例 t_20=11 の出所)
  {
    const ker = kernelOf(20, 10);
    chk('(f) ker((Z/20)^× → (Z/10)^×) = {1,11}(units 列挙による完全一致)',
        JSON.stringify(ker) === JSON.stringify([1, 11]), `実測 ker = {${ker}}`);
    chk('(f′) 反例 t_20=11 はこの核の非自明元である', ker.includes(11) && 11 !== 1);
  }
}

// ---- 検査 6: regression suite を二分割(便 49 F4.5 / F10.2)----
// finite operational orientation suite : paths 1,2,3,4,6,7,8 → 期待 6 detected / 1 root-link blind
// profinite root-normalization suite   : path 5 → 期待 finite b measurement out-of-scope
console.log('\n検査 6: single-axis regression set の二分割(便 49 F4.5 の数え直し)');
{
  // 各 path が b_op に与える効果。9 = 検出、1 = 不可視、null = 有限測定の射程外
  const paths = {
    1: { suite: 'finite', b_op: 9 },  // C1 反転
    2: { suite: 'finite', b_op: 9 },  // C2 反転
    3: { suite: 'finite', b_op: 9 },  // C5 時計回り
    4: { suite: 'finite', b_op: 9 },  // C4 埋め込み反転
    5: { suite: 'profinite', b_op: null }, // C7: n∤20 の root ⇒ M|20 の測定宇宙に入らない
    6: { suite: 'finite', b_op: 9 },  // C3 反転
    7: { suite: 'finite', b_op: 9 },  // A3 反転
    8: { suite: 'finite', b_op: 1 },  // root-object ずれ ⇒ blind((Z20-link) 担当)
  };
  const fin = Object.entries(paths).filter(([, v]) => v.suite === 'finite');
  const det = fin.filter(([, v]) => v.b_op === 9).length;
  const blind = fin.filter(([, v]) => v.b_op === 1).length;
  const oos = Object.entries(paths).filter(([, v]) => v.suite === 'profinite').length;
  chk('finite suite: 7 paths / 6 detected / 1 root-link blind', fin.length === 7 && det === 6 && blind === 1,
      `detected=${det}, blind=${blind}`);
  chk('profinite suite: path 5 は out-of-scope(1 本)', oos === 1);
  chk('母数 8 での数え: 6/8 可視・2/8 不可視(「7/8」は偽)', det === 6 && (blind + oos) === 2);
}

console.log(`\n=== ${pass}/${pass + fail} PASS ===`);
