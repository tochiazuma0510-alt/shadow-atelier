// week4-e2-vanish-check.mjs — 定理 E23(中心持ち上げ障害の恒等消滅)の仮定 (G2)(G3) の検算
// 普遍 class-5 対象 P^(5) = F_2/γ_6、C = [A,A] = ⟨t5,t6⟩、基底 (t5,t6) で
//   σ|_C = [[0,-1],[1,-1]]  (σ(t5)=t6, σ(t6)=-t5-t6)      … 命題 E22 §5.2
//   θ|_C = [[0, 1],[1, 0]]  (θ(t5)=t6, θ(t6)=t5)
// を Z/2^j (j=1..6) 上で確認する。GAP/照合器を import しない独立実装。

const results = [];
const chk = (n, ok, d = '') => { results.push(ok); console.log(`${ok ? 'PASS' : '*** FAIL'}  ${n}${d ? '  :: ' + d : ''}`); };

const mmul = (A, B, M) => A.map(r => B[0].map((_, j) => r.reduce((s, a, k) => (s + a * B[k][j]) % M, 0) % M));
const madd = (A, B, M) => A.map((r, i) => r.map((a, j) => ((a + B[i][j]) % M + M) % M));
const mid = (n) => Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => +(i === j)));
const mscale = (A, c, M) => A.map(r => r.map(a => ((a * c) % M + M) % M));
// Z/M 上の写像 A: (Z/M)^2 -> (Z/M)^2 の核 / 像を全数で
const kernel = (A, M) => { const K = []; for (let a = 0; a < M; a++) for (let b = 0; b < M; b++) { const x = [a, b]; const y = A.map(r => ((r[0] * a + r[1] * b) % M + M) % M); if (y[0] === 0 && y[1] === 0) K.push(x); } return K; };
const image = (A, M) => { const S = new Set(); for (let a = 0; a < M; a++) for (let b = 0; b < M; b++) { const y = A.map(r => ((r[0] * a + r[1] * b) % M + M) % M); S.add(y.join(',')); } return S; };

const sigma = [[0, -1], [1, -1]];
const theta = [[0, 1], [1, 0]];

for (let j = 1; j <= 8; j++) {
  const M = 2 ** j;
  const S = sigma.map(r => r.map(a => ((a % M) + M) % M));
  const T = theta.map(r => r.map(a => ((a % M) + M) % M));
  const I = mid(2);

  // 基本性質
  const S3 = mmul(mmul(S, S, M), S, M);
  const T2 = mmul(T, T, M);
  const N  = madd(madd(I, S, M), mmul(S, S, M), M);
  const ok0 = JSON.stringify(S3) === JSON.stringify(I) && JSON.stringify(T2) === JSON.stringify(I)
           && N.every(r => r.every(a => a % M === 0));
  chk(`j=${j}: σ³ = θ² = 1, N_C = 1+σ+σ² = 0 on C`, ok0);

  // (G2) C^σ = 0  ⟺ 1−σ が可逆(det = 3 が奇数)
  const ImS = madd(I, mscale(S, -1, M), M);            // 1 − σ
  const detImS = ((ImS[0][0] * ImS[1][1] - ImS[0][1] * ImS[1][0]) % M + M) % M;
  const kerImS = kernel(ImS, M);
  chk(`j=${j}: (G2) C^σ = 0(det(1−σ) = 3 は奇数ゆえ可逆)`, kerImS.length === 1 && detImS % 2 === 1,
      `det(1−σ) ≡ ${detImS} (mod ${M}), |C^σ| = ${kerImS.length}`);

  // (G3) C^θ = im(1+θ)  ⟺ Ĥ^0(⟨θ⟩, C) = 0(C ≅ Z/2^j[C_2] は induced)
  const IpT = madd(I, T, M);                            // 1 + θ
  const kerImT = kernel(madd(I, mscale(T, -1, M), M), M);   // C^θ = ker(1 − θ)
  const imIpT = image(IpT, M);
  const fixSet = new Set(kerImT.map(x => x.join(',')));
  const eq = fixSet.size === imIpT.size && [...fixSet].every(s => imIpT.has(s));
  chk(`j=${j}: (G3) C^θ = im(1+θ)|_C(= ⟨t5+t6⟩・Tate Ĥ⁰ = 0)`, eq,
      `|C^θ| = ${fixSet.size}, |im(1+θ)| = ${imIpT.size}, 期待 ${M}`);

  // im Λ = {((1+θ)z, N_C z)} = ⟨(t5+t6, 0)⟩、|Ob| = M^4 / M = M^3
  chk(`j=${j}: im Λ = ⟨(t5+t6, 0)⟩、|Ob| = ${M ** 3}`, imIpT.size === M);
}

// (σ−1)^{-1}(t5+t6) の明示値(F₂ ≡ 0 の内訳の検算・整数で)
// (σ−1)(t5+2t6) = −3(t5+t6) を確認
{
  const apply = (A, v) => [A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1]];
  const SmI = [[0 - 1, -1], [1, -1 - 1]];              // σ − 1(整数)
  const v = apply(SmI, [1, 2]);
  chk('(σ−1)(t5+2t6) = −3(t5+t6)', v[0] === -3 && v[1] === -3, `= ${v[0]}t5 + ${v[1]}t6`);
  chk('σ(t5+t6) = −t5', JSON.stringify(apply(sigma, [1, 1])) === JSON.stringify([-1, 0]));
  chk('(2+σ)(t5+t6) = t5 + 2t6', JSON.stringify(apply([[2, -1], [1, 1]], [1, 1])) === JSON.stringify([1, 2]));
}

console.log(`\n==== ${results.filter(Boolean).length}/${results.length} PASS ====`);
if (results.some(r => !r)) process.exitCode = 1;
