// week4-ob-c6-derive.mjs — 委嘱 16: class-6 障害式 ob の独立導出(並列ブラインド)
// 入力: crosscheck/agree6_claude.json の theta_table / sigma_table_poly の C-ブロックのみ。
// 基底 (t5,t6,u1,u2,u3,u4)。j = 2 ⇒ R = Z/2(W137 の添字規約で C_j = (Z/2^{j-1})^6)。
import { readFileSync } from 'node:fs';
const J = JSON.parse(readFileSync(new URL('../crosscheck/agree6_claude.json', import.meta.url), 'utf8'));
const OK = [];
const chk = (n, ok, d = '') => { OK.push(ok); console.log(`${ok ? 'PASS' : '*** FAIL'}  ${n}${d ? '  :: ' + d : ''}`); };

const B = ['t5', 't6', 'u1', 'u2', 'u3', 'u4'];
const idx = Object.fromEntries(B.map((k, i) => [k, i]));
const A_ = 5, B_ = 3;                    // a = u4 は成分 5、b の代表 u2 は成分 3

const thetaMat = () => { const M = Array.from({ length: 6 }, () => Array(6).fill(0));
  for (let c = 0; c < 6; c++) { const row = J.theta_table[B[c]]; B.forEach((k, r) => { M[r][c] = row[J.meta.basis_order.indexOf(k)]; }); } return M; };
const sigmaMat = (m) => { const M = Array.from({ length: 6 }, () => Array(6).fill(0));
  for (let c = 0; c < 6; c++) for (const [k, co] of Object.entries(J.sigma_table_poly[B[c]])) {
    if (!(k in idx)) continue; let v = 0, mm = 1; for (const cc of co) { v += cc * mm; mm *= m; } M[idx[k]][c] = v; } return M; };
const mmulZ = (X, Y) => X.map((r, i) => Y[0].map((_, j) => r.reduce((s, _, k) => s + X[i][k] * Y[k][j], 0)));
const ap2 = (M, v) => Array.from({ length: 6 }, (_, i) => M[i].reduce((s, a, k) => s ^ ((((a % 2) + 2) % 2) & v[k]), 0) & 1);
const ALL = []; for (let k = 0; k < 64; k++) ALL.push(Array.from({ length: 6 }, (_, i) => (k >> i) & 1));
const dimF2 = (set) => { const bas = []; for (const s of set) { let x = Array.isArray(s) ? s.slice() : s.split('').map(Number);
    for (const b of bas) { const p = b.findIndex(t => t === 1); if (x[p] === 1) x = x.map((t, i) => t ^ b[i]); }
    if (x.some(t => t === 1)) bas.push(x); } return bas.length; };
const T = thetaMat();

//////////////////// 0. C が σ,θ で閉じる ////////////////////
{ let closed = true;
  for (const c of B) { for (const k of Object.keys(J.sigma_table_poly[c])) if (k !== '_comment' && !(k in idx)) closed = false;
    J.meta.basis_order.forEach((k, i) => { if (J.theta_table[c][i] !== 0 && !(k in idx)) closed = false; }); }
  chk('(0) C = ⟨t5,t6,u1,u2,u3,u4⟩ は σ,θ で閉じる', closed); }

//////////////////// 1. σ³ = 1、C^σ = Ra⊕Rb、θ(a) = −a・θ(b) = b ////////////////////
{ let ok3 = true, okFix = true;
  for (const m of [0, 1, 2, 3, 7, 63]) { const S = sigmaMat(m), S3 = mmulZ(mmulZ(S, S), S);
    if (!S3.every((r, i) => r.every((v, j) => v === (i === j ? 1 : 0)))) ok3 = false;
    for (const v of [[0,0,0,0,0,1], [0,0,1,1,1,0]]) {
      const w = v.map((_, i) => S[i].reduce((s, c, k) => s + c * v[k], 0));
      if (JSON.stringify(w) !== JSON.stringify(v)) okFix = false; } }
  chk('(1a) σ|_C の位数は 3(σ³ = Inn(E_m) は中心上恒等)', ok3);
  chk('(1b) a = u₄, b = u₁+u₂+u₃ は σ-不変(全 m・Z 上)⇒ C^σ = Ra⊕Rb', okFix);
  const th = (v) => v.map((_, i) => T[i].reduce((s, c, k) => s + c * v[k], 0));
  chk('(1c) θ(a) = −a、θ(b) = +b', JSON.stringify(th([0,0,0,0,0,1])) === JSON.stringify([0,0,0,0,0,-1])
      && JSON.stringify(th([0,0,1,1,1,0])) === JSON.stringify([0,0,1,1,1,0])); }

//////////////////// 2. ★ θ は 𝒩_C と可換でない ⇒ Maschke 分解は θ-同変でない ////////////////////
{ let anyNonComm = false, kerNotStable = false;
  for (const m of [0, 1, 2, 3]) { const S = sigmaMat(m), S2 = mmulZ(S, S);
    const NC = S.map((r, i) => r.map((v, j) => (i === j ? 1 : 0) + v + S2[i][j]));
    if (JSON.stringify(mmulZ(T, NC)) !== JSON.stringify(mmulZ(NC, T))) anyNonComm = true;
    const ker = ALL.filter(v => ap2(NC, v).every(t => t === 0));
    const set = new Set(ker.map(v => v.join('')));
    if (!ker.every(v => set.has(ap2(T, v).join('')))) kerNotStable = true; }
  chk('(2) ★ θ𝒩_C ≠ 𝒩_Cθ、かつ C₋ = ker 𝒩_C は θ-安定でない(class 5 と決定的に違う)', anyNonComm && kerNotStable); }

//////////////////// 3. ★ 正しい障害群と (a,b) 座標 ////////////////////
{ const rows = []; let okDim = true, okCrit = true, okIso = true, okImg = true;
  for (const m of [0, 1]) {                       // Z/2 上 σ は m mod 2 のみに依存
    const S = sigmaMat(m), S2 = mmulZ(S, S);
    const NC = S.map((r, i) => r.map((v, j) => (i === j ? 1 : 0) + v + S2[i][j]));
    const IpT = T.map((r, i) => r.map((v, j) => (i === j ? 1 : 0) + v));
    const Cm = ALL.filter(v => ap2(NC, v).every(t => t === 0));                    // C₋ = ker 𝒩_C
    const Cth = ALL.filter(v => JSON.stringify(ap2(T, v)) === JSON.stringify(v));  // C^θ
    const img = [...new Set(Cm.map(v => ap2(IpT, v).join('')))].map(s => s.split('').map(Number));
    const dTh = dimF2(Cth), dIm = dimF2(img);
    if (!(dTh === 4 && dIm === 2 && dTh - dIm === 2)) okDim = false;
    // ★ 判定: v ∈ C^θ に対し [v] = 0 in C^θ/(1+θ)C₋  ⟺  (v_{u2}, v_{u4}) = (0,0)
    const imgSet = new Set(img.map(v => v.join('')));
    for (const v of Cth) { const inImg = imgSet.has(v.join('')); if (inImg !== (v[B_] === 0 && v[A_] === 0)) okCrit = false; }
    // ★ (C^σ)^θ → C^θ/(1+θ)C₋ が同型(a ↦ [u₄]、b ↦ [u₂])
    const a = [0,0,0,0,0,1], b = [0,0,1,1,1,0];
    if (!(a[B_] === 0 && a[A_] === 1 && b[B_] === 1 && b[A_] === 0)) okIso = false;
    // ★ e = 3⁻¹𝒩_C は (1+θ)C₋ を殺さない ⇒ 平均化射影 (A) は商へ落ちない
    const survive = img.filter(v => ap2(NC, v).some(t => t === 1));
    if (survive.length === 0) okImg = false;
    rows.push(`m≡${m}: dim C^θ=${dTh}, dim(1+θ)C₋=${dIm}, dim Ob=${dTh - dIm}; (1+θ)C₋ = {${img.map(v => v.join('')).sort().join(', ')}}; e が殺さない元 = ${survive.map(v => v.join('')).join(',')}`); }
  chk('(3a) dim C^θ = 4、dim (1+θ)C₋ = 2 ⇒ 障害群 Ob = C^θ/(1+θ)C₋ は 2 次元(= manifest の 2 ビットと一致)', okDim, rows.join('\n              '));
  chk('(3b) ★ 判定式: v ∈ C^θ について [v] = 0 ⟺ (v の u₂ 係数, v の u₄ 係数) = (0,0)', okCrit);
  chk('(3c) ★ (C^σ)^θ ≅ C^θ/(1+θ)C₋ は同型で a = u₄ ↦ [u₄]、b = u₁+u₂+u₃ ↦ [u₂](ラベルは整合)', okIso);
  chk('(3d) ★★ e = 3⁻¹𝒩_C は (1+θ)C₋ を殺さない(t₅+t₆ ∈ (1+θ)C₋ だが e(t₅+t₆) = a+b ≠ 0)⇒ **平均化射影 (A) は障害群へ落ちない**', okImg); }

//////////////////// 4. ★★ 偽陽性 fixture: 可解なのに manifest 式が ob ≠ 0 を返す ////////////////////
{ const rows = []; let found = false;
  for (const m of [0, 1]) {
    const S = sigmaMat(m), S2 = mmulZ(S, S);
    const NC = S.map((r, i) => r.map((v, j) => (i === j ? 1 : 0) + v + S2[i][j]));
    const IpT = T.map((r, i) => r.map((v, j) => (i === j ? 1 : 0) + v));
    const Cm = ALL.filter(v => ap2(NC, v).every(t => t === 0));
    for (const zm of Cm) {
      const qth = ap2(IpT, zm);                       // q_θ = (1+θ)z₋、q_N = 0 ⇒ z = z₋ が両式を解く(可解)
      if (qth.every(t => t === 0)) continue;
      const manifest = ap2(NC, qth);                  // (A): ob = e(q_θ) − 3⁻¹(1+θ)q_N、q_N = 0 なので e(q_θ)
      const correct = [qth[B_], qth[A_]];             // 正しい ob = (u₂ 係数, u₄ 係数)
      if (manifest.some(t => t === 1) && correct.every(t => t === 0)) { found = true;
        rows.push(`m≡${m}: z₋=(${zm}) ⇒ q_θ=(1+θ)z₋=(${qth}), q_N=0 ⇒ **可解**(z = z₋)。しかし (A) の ob = e(q_θ) = (${manifest}) ≠ 0 ⇒ 偽 fake。正しい ob = (${correct}) = 0 ✓`);
        break; } } }
  chk('(4) ★★ 可解系で manifest 式 (A) が ob ≠ 0 を返す反例が存在(偽陽性生成器)', found, rows.join('\n              ')); }

console.log(`\n==== ${OK.filter(Boolean).length}/${OK.length} PASS ====`);
if (OK.some(r => !r)) process.exitCode = 1;
