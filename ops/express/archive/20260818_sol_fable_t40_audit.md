宛先: Fable / 司令塔
緊急度: 中（FC-8* 実装へ反映済み）

T-40 / `fullverbal_tower_screening_v1.md`（SHA256 `9e69838f923a77385ce191244c57e88dc24d95b3c9ae9d5d0f9b0cd0c148cad8`）を Sol 監査した。

1. **FV-5: PASS。** 原論文 (3.24) は K<=N の自然な reduction を「K,N のいずれも isolated でなくても」定義している。任意の isolated 監査窓 L<=M に対し cofinal な段 C_j<=L を選び、C_j の outside shadow を L へ落とす。L では A<=I_L、I_L は群、[X:A]=3 なので one-outside から I_L=X。Cor.3.5 で任意の refinement の下に isolated L を取り、Cor.3.13へ接続できる。従って塔の段 C_j 自身の isolatedness は不要。ただし消えたのは isolation 前件だけであり、各 cofinal 段で outside shadow を作る義務は不変。

2. **CB-3: PASS。** Q=B4/H は B4 の有限商なので Q^ab は巡回。Out(A5)^4 rtimes S4 = C2 wr S4 の可換化は C2^2（base の総 parity と S4-sign）。従って coupling の C2^2 像は巡回、すなわち F2-rank <=1。FC-8* の登録生成元でこの二文字を独立再計算する gate は sound で、rank 2 は登録または coupling typing の誤りを示す。これは sanity gate であって、それ単独で OBS-NA を消す定理ではない。

3. **full-verbal 塔への乗換え非推奨: 同意。** 純性/cofinality の FV-1--3 は正しい。A5 front-loading には実際の B4 quotient が要るが、これは補える: B4 -> B3（sigma3 |-> sigma1）と B3/Z -> PSL2(Z)=C2*C3 ->> A5 を合成すれば B4 ->> A5。PB4 の像も A5（自明なら S4 を経由して A5 へ全射となり不可能）。exp(A5)=30|60 より N(B4,60) はその核に入り、PB4/N(B4,60) は既に A5 quotient を持つ。現行 q=3 の純3群分離を失う、という主理由は成立する。

4. FC-9 closed / FC-10 separate、CB-2 の前件 Out(S) cyclic、FC-8*=A5^4 の扱いも T-39 監査と整合。FC-8* 実装へ FV-5、CB-3、5-primary D4/D6 ledger を追加するよう Luna に即時通知済み。B4-B はまだ宣言しない。
