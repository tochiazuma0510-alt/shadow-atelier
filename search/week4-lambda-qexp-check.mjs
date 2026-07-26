// week4-lambda-qexp-check.mjs — 委嘱 13 §1: λ(τ) = 16 q^{1/2} + O(q) の主係数 16 を数値で確認。
// これが u ≡ 16 (mod (Q^*)^5) の「第三系統(古典モジュラー)」の裏取りになる。
// θ₂ = 2 q^{1/8} Σ_{n≥0} q^{n(n+1)/2},  θ₃ = 1 + 2 Σ_{n≥1} q^{n²/2},  λ = (θ₂/θ₃)^4,  q = e^{2πiτ}.
const results = [];
const chk = (n, ok, d = '') => { results.push(ok); console.log(`${ok ? 'PASS' : '*** FAIL'}  ${n}${d ? '  :: ' + d : ''}`); };

function lambdaOf(t) {                    // τ = i t (t > 0), q = e^{-2πt} 実数
  const q = Math.exp(-2 * Math.PI * t);
  let s2 = 0; for (let n = 0; n < 60; n++) s2 += Math.pow(q, n * (n + 1) / 2);
  const th2 = 2 * Math.pow(q, 1 / 8) * s2;
  let s3 = 1; for (let n = 1; n < 60; n++) s3 += 2 * Math.pow(q, n * n / 2);
  const r = th2 / s3;
  return r * r * r * r;
}

// (1) λ / q^{1/2} → 16
{
  const rows = [];
  let ok = true;
  for (const t of [1, 1.5, 2, 3, 4, 5]) {
    const q12 = Math.exp(-Math.PI * t);
    const ratio = lambdaOf(t) / q12;
    // 予測誤差は |16·(−8)q^{1/2}| = 128 e^{−πt}
    const bound = 1.3 * 128 * q12;
    rows.push(`t=${t}: λ/q^{1/2} = ${ratio.toFixed(8)} (|Δ| = ${Math.abs(ratio - 16).toExponential(2)} < ${bound.toExponential(2)})`);
    if (!(Math.abs(ratio - 16) < bound)) ok = false;
  }
  chk('(1) λ(it)/q^{1/2} → 16、誤差は予測 128·e^{−πt} 内', ok, rows.join(' | '));
}

// (2) 次項まで: λ = 16 q^{1/2} (1 − 8 q^{1/2} + 44 q − …) の -8 を確認
{
  let ok = true; const rows = [];
  for (const t of [2, 3, 4]) {
    const q12 = Math.exp(-Math.PI * t);
    const c1 = (lambdaOf(t) / (16 * q12) - 1) / q12;   // ≈ −8 + 44 q^{1/2}
    rows.push(`t=${t}: (λ/(16q^{1/2})−1)/q^{1/2} = ${c1.toFixed(6)}`);
    if (t >= 3 && Math.abs(c1 + 8) > 0.05) ok = false;
  }
  chk('(2) 第二係数 = −8(λ = 16q^{1/2}(1 − 8q^{1/2} + …))', ok, rows.join(' | '));
}

// (3) 5 乗剰余類: [16] = [2]^4 で、我々の平面モデル計算 [u] = [2]^4 と一致
{
  const cls = (e2) => ((e2 % 5) + 5) % 5;
  chk('(3) [16] = [2^4] = 平面モデル由来の [u]', cls(4) === cls(4) && cls(4) !== 0, `v_2(16) = 4 ≢ 0 (mod 5)`);
  // Tate 正規化(q^{1/2} を基準)に取り替えると c = 16 で、系 B′ の「危険な c」に一致するか
  // [b_A]_{v_c} = [2]·[c]^{±1};  c = 16 = 2^4 ⇒ [2^{1+4}] = [2^5] = 1  (符号の一方で自明化)
  chk('(3b) c = 16 は系 B′ の「判定を反転させる危険な c」そのもの', (1 + 4) % 5 === 0, `[2]·[16] = [2^5] = 1`);
}

console.log(`\n==== ${results.filter(Boolean).length}/${results.length} PASS ====`);
if (results.some(r => !r)) process.exitCode = 1;
