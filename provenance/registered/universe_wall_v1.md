# 宇宙の事前登録: 壁キャンペーン v1.2(draft/candidate — Sol 便 78 共同設計を反映・falsifier 再前哨 → 便 79 で go 請求)

状態: **draft**。v1.1 への Sol 便 78 の裁定(F78-3.7 FAIL = 型違反ほか)と発案札 A/B・(a)〜(f) を反映。登録後の変更禁止 — 拡張は新 band の追加登録で行う。

## 目的(先に固定)

非 metabelian または非可解な GT 型対象の**明示座標**を、事前固定した窓宇宙の中で探す。**冒頭定理(candidate・二層検証中)= W-Exist**: 枠組み仮定(Ihara 埋込+isolated Main Line 逆極限)の下、非可解 GT(N) を持つ有限 isolated 窓は存在する(ker χ̃ も非可解)。よって本キャンペーンは存在を賭けた探索でなく、**存在が保証された座標の明示化**である(ただし指数の定量上界は理論から出ない)。全窓 metabelian の band 結果は「低い帯の現象」の悉皆記録として一級の成果。

## 宇宙の定義

- 母群: B₃ = ⟨a, b | aba = bab⟩(表示固定)。PB₃ = ker(β: B₃ → S₃)(a ↦ (1,2), b ↦ (2,3)・この定義で十分 — 一意性補助主張には依存しない)。
- 窓: N ⊴ B₃・[B₃:N] ≤ 上限・N ≤ PB₃。列挙器: GAP 4.16.0 + lins 0.9。
- **band W-A(ローカル参照帯)**: 指数 ≤ 192(probe 実測 319 本・PB₃ 内 66 本)。**理論消去: 指数 < 48 は (W3) により可解確定**(計算不要・記録のみ)。
- **band W-C(標的族・Sol 発案 D1)**: congruence 族 N_p = ker(B₃ → S₃ × SL₂(𝔽_p))(標準表現 mod 2p・CRT)、p ∈ {5, 7, 11, 13}。指数 6p(p²−1) = 720/2016/7920/13104。**c ∉ N_p(c ↦ −I)につき語レベル hexagon 分岐の本番適用**。settled/isolation・Θ 忠実性は窓ごと判定。
- band W-B(CI 一般帯): 上限は W-A/W-C の実測 shard 時間を根拠に追加登録で固定してから。
- 計数規約: 宇宙の要素は部分群(本数 ≠ 同型類数)。isolated 性は属性として記録。
- **対称簡約(Sol (e))**: ι: σᵢ ↦ σᵢ⁻¹(Out(B₃) ≅ C₂)による orbit(大きさ 1 or 2)。raw universe の計数は保持し、**canonical subgroup hash の小さい方のみ計算代表**とする。証明書に partner・transport 自己同型・transport 後の source-kernel 一致・χ 可換図式 digest を記録。報告は raw_window_count と symmetry_orbit_count を併記。無言の宇宙縮小は禁止。

## 群対象の型(v1.2 の根本修理・Sol 札 B)

- 各窓の群対象は **G_N := GTSh(N,N)(isotropy group)**。手順: ①charming pair+full hexagon を列挙 ②各 pair の **source kernel K = ker T_{m,f} を証明書化** ③K = N のもののみで G_N を構成 ④合成・χ̃・導来列・可解性は **G_N 上でのみ**計算。
- source 同定が cap 内で完了しない窓は UNKNOWN。isolated なら GT(N) = GTSh(N,N) を別欄で記録(settled count と isolated status は別報告)。
- 証明書必須欄: source_kernel_id/digest・settled ∈ {true,false,UNKNOWN}・isotropy_order。

## 窓ごとの判定パイプライン

1. **不変量**: 指数・StructureDescription(参考欄 — 主張には使わない)・N_ord・c ∈ N か・|Z(A)|(A = PB₃/N)・**S₃-module としての Z(A) と |Z¹(S₃, Z(A))|**・ord(σ₁ mod N)(定理 F78-2.2: c ∈ N 窓では = 2N_ord — 検算欄)。
2. **Stage 0 理論 sieve(hexagon 評価前・Sol (a)(f))**:
   - (W2) 候補数床: c_m(N)·|[P_N,P_N]| < 60 ⟹ SOLVABLE 確定(即決)。
   - Θ_N: G_N → Aut_π(E) の kernel order/status(**Θ 単射を一般定理として仮定しない**)。
   - H_N(power-form 生成部分群)の構成と IsSolvable(H_N)・非可換組成因子。
   - **nilpotent/class-2 判定(Sol A3)**: A nilpotent + ker Θ 可解 ⟹ SOLVABLE。A class-2 + Θ 忠実 ⟹ METABELIAN。該当窓は理論確定(extraspecial 族は較正族へ)。
   - inversion orbit ID。
3. **ker χ̃ の枚挙**(G_N の c = 1 層・v1.1 の (2a)(2b)(2c) 維持: c ∈ N は簡約 hexagon/c ∉ N は語レベル・shadow 水準 (3.53) 合成・|Z(A)| ≠ 1 窓は PROVISIONAL 札)。
4. **札(Sol (f)・一方向必要条件の明記)**:
   - **KERNEL-NONABELIAN**: ker χ̃ 非可換(候補札のみ — 発見主張ではない)
   - **CHI-AB-CERTIFIED**: ker χ̃ = [G_N, G_N] を当該窓で機械証明(G_N^ab → Im χ̃ の核自明)
   - **NONMETABELIAN**: G_N″ ≠ 1 の**具体 witness**(交換子の交換子の非自明例)保持
   - **NONSOLVABLE**: 導来列が非自明 perfect core で停止した exact orders 保持
   - **SIMPLE-ORDER-FILTER**(別欄): |G_N| の非可換単純群位数(60, 168, …)可除性
   - 主張は witness と exact order で支える(StructureDescription では主張しない)。
5. 打ち切り = UNKNOWN(窓単位・shard cap 超過は未完了窓のみ)。

## 実行と証明書

- 実行環境: ローカル(gap.ps1・-o 2g・600 秒 cap/shard)+ GitHub Actions(setup-gap 4.16.0・-o 8g)。両環境 GAP 4.16.0 + lins 0.9 固定。
- 証明書 wall-cert/**v2**: v1 欄+source_kernel 欄群+Stage 0 採点 7 欄+orbit 欄+札(PROVISIONAL 含む)。
- **照合 lane の独立性(Sol (f))**: python lane は GAP helper/table を共有しない。入力は multiplication table・x, y, c・source-kernel generator images の **exact blob(digest つき)**とし、cocycle 則・合成・導来 witness を別実装で再評価。抽出 = 全 KERNEL-NONABELIAN 以上+SOLVABLE 確定の無作為 ≥ 10%(シード 20260728)。
- 較正: positive = K⁽³⁾(SOLVABLE 側)・adversarial = N_Q(C2F 核)+ c ∉ N 窓(語レベル分岐)・**合成 KERNEL-NONABELIAN fixture**(注入テスト)・**nilpotent 較正 = extraspecial 族**(A3 の理論確定と機械判定の一致確認)。較正失敗時の掃引結果は無効。
- index = 1 の FactorGroup 不具合回避(既知)。

## 報告規約

全窓数(raw/orbit 両建て)・SOLVABLE(理論確定と計算確定を区別)・各札の数・UNKNOWN 数と率・PROVISIONAL 数を必ず併記。UNKNOWN が残る限り悉皆主張をしない。

## 撤退・停止

主線(dihedral 予想)優先・資源競合時は本キャンペーン停止。band 拡張は追記のみ可・判定規約の変更は新登録。**掃引 go は Sol 便 79 の v1.2 承認後**(F78-3.7)。

## 改訂履歴

- v1 → v1.1: falsifier 前哨(FAIL 5/NOTE 3)全採用。
- v1.1 → v1.2: Sol 便 78(裁定 152)反映 — W-Exist 目的再定義・**isotropy 型修理(G_N = GTSh(N,N)・source kernel 証明書)**・Stage 0 理論 sieve 7 欄・札の四分離+witness 主義・ι-orbit 簡約・W-C congruence 帯・lane 独立性強化・extraspecial の較正族降格。
