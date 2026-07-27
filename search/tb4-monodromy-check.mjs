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

console.log(`\n=== ${pass}/${pass + fail} PASS ===`);
