# 裁定 33 — P6 検収・第三 checker 設計の承認・便 34 発送(2026-07-27・司令塔)

## P6(パイプライン)検収: 受理

- **K³ 較正を raw 再計算で完全再現**: 経路 A(GAP・K[[t]])= 経路 B(node・級数不使用)= **u = −4**・第三 checker ACCEPT。covariance: s ↦ cs で u ↦ u·c^{−2M} 厳密一致・X ↦ X⁻¹ で ord 不変・ord([u⁻¹]₆) = 3 は witness(e⁶ = u の検算込み)つき。期待値のハードコード比較なし(manifest 較正三層 2 の要求どおり)。
- **第三 checker の設計判断を承認**: check-kummer.mjs は factorization の再実装でなく**別の証明原理**(K アーベル ⟹ 奇素数冪判定の ℚ への降下・p = 2 は二次部分体判別式表)による突合。「同じ計算の二重化」より視点多様性が高く、工房の falsifier 哲学に合致。付記: 判定原理が異なるため、不一致時の切り分けは「実装バグ vs 原理の適用条件」の両面を見ること。
- (O-a)(イデアル valuation)未実装は Rule 1 §8.3「いずれか一つで足りる」の範囲内((O-b)(O-c) で充足)。将来の高速化候補として backlog。

## ★教材 25 — CF(n) の Factors 罠

GAP の `CF(n)` 直上の `Factors` は体としての因数分解を行わない(T²+4 を既約と返す実例 — 2i が根)。`AlgebraicExtension(Rationals, CyclotomicPolynomial(...))` で構成し直すと正しい。**棚卸し実施: 既存 .g の Factors 使用は a5-dessin-crosscheck.g の 2 箇所のみで、ℚ 上と GF(3) 上 — CF 罠の射程外・遡及汚染なし**。今後の規約: 円分体上の多項式分解は AlgebraicExtension 経由を必須とする(kummer-decide.g のヘッダに明記済)。

## P1–P7 の完了確認と便 34

P1(結果規則 total 化+REFUTED)・P2(M3/M4 total algorithm+R1-N1/N2)・P3(親 manifest へ I-b 反映)・P4(K3 fixture ρ₀/j+再 hash)・P5(S5-3 符号/gauge)・P6(実装+版表)— **全反映**。P7 = 新 digest:

- Rule 1 v1.1: `0863b3fdbeb62f8406617078332eb3762b046a8e2a0d422aee3bdac6736e8cd0`
- 付録 A v2: `0f8ef861d1d203be0ad1059204c74c5110da6132a65af53ec26e9c370a73bfa6`
- manifest v1.3: `181b548c50897eb7a51dc257efee3320a38a6481a6155dba84857c98190ae2be`
- 実装版表: `411ff12a0fc2b2757512a1261c8585339535345ffb64dd63876981c85d8aaf46`

個別モデル探索コマンドは**依然一度も実行していない**(全修理は fixture・文書・K³ 既知データのみ)。便 34(差分検収)を発送する。
