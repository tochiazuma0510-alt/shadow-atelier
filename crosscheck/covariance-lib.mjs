// crosscheck/covariance-lib.mjs -- covariance の共通ライブラリ(裁定 38/便 37
// F5 修理: 便 36 F4.2 の sealed envelope が使う computeAEff 等を export し、
// 較正 checker (crosscheck/check-covariance-envelope.mjs) と橋段 driver
// (crosscheck/covariance-bridge-in.mjs)の**両方**が同じ関数を呼ぶようにする
// (Sol 便 37 F5.2 (3) 「actual bridge が import する共通 library として固定
// する」の実体化)。
//
// 身分: 本ファイルは Rule 1 SS7.2/SS7.3 の型レベル規約(d-reparametrization
// covariance・restriction map (Z/10)^x -> (Z/5)^x)を実装するだけであり、
// K5 の実 b_sq/b_ns 値をハードコードしない(引数として受け取る)。

export function gcd(a, b) { while (b) { [a, b] = [b, a % b]; } return a; }
export function unitsMod(n) {
  const r = [];
  for (let x = 1; x < n; x++) if (gcd(x, n) === 1) r.push(x);
  return r;
}
export function invMod(x, n) {
  for (let y = 1; y < n; y++) if ((x * y) % n === 1) return y;
  throw new Error(`invMod: ${x} has no inverse mod ${n}`);
}
export function mulMod(x, y, n) { return ((x * y) % n + n) % n; }

// restriction map [.]: (Z/10)^x -> (Z/5)^x (Rule 1 SS7.2: "(Z/10)^x ->
// (Z/5)^x は全単射ゆえ lift の曖昧さはない"): reduce mod 5.
export function restrict10to5(b) { return ((b % 5) + 5) % 5; }

// a_eff = [b_ns]^{-1} a [b_sq] (mod 5). a は Rule 1 SS7.2 (1.11) の formal
// invariant(K5 sq/ns fixture の rho0_and_j.a_sealed から読む -- 再導出しない)。
export function computeAEff(bSq, bNs, a) {
  const bSq5 = restrict10to5(bSq);
  const bNs5 = restrict10to5(bNs);
  const bNs5Inv = invMod(bNs5, 5);
  return mulMod(mulMod(bNs5Inv, a, 5), bSq5, 5);
}

// SS7.3 acceptance rule: b_sq = b_ns => a_eff = a.
export function acceptanceRuleHolds(b, a) {
  return computeAEff(b, b, a) === a;
}
