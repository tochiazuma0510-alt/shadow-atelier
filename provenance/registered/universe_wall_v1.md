# 宇宙の事前登録: 壁キャンペーン v1(draft/candidate — Sol 便 78 ゲート待ち)

状態: **draft**(falsifier 前哨 → Sol ゲート PASS で registered に昇格)。登録後の変更禁止 — 拡張は新 band の追加登録で行う。

## 目的(先に固定)

非 metabelian または非可解な GT(N) の存否を、事前固定した窓宇宙の中で悉皆判定する。動機は FINDING I-26(現 atlas 14 対象は全て metabelian)と層 A 必要条件群(裁定記録)。**全窓 metabelian という負の結果は一級の成果**(壁絶対性定理 (B1) の実験的裏付け)であり、探索の成否を TIER 到達の有無で定義しない。

## 宇宙の定義

- 母群: B₃ = ⟨a, b | aba = bab⟩(自由群 F(a,b) の剰余・この表示を固定)。
- 窓: N ⊴ B₃ かつ [B₃:N] ≤ 上限 かつ N ≤ PB₃。PB₃ 判定は標準全射 β: B₃ → S₃(a ↦ (1,2), b ↦ (2,3))の核との包含で行う(この一本に固定)。
- 列挙器: GAP 4.16.0 + lins 0.9(`LowIndexNormalSubgroupsSearch` → `ComputedNormalSubgroups`・Firth/Holt)。
- **band W-A(ローカル参照帯)**: 指数 ≤ 192。probe 実測(search/certs/wall_probe_20260728.json): 正規部分群 319 本・うち PB₃ 内 66 本・壁時計 12.5 秒。
- **band W-B(CI 帯)**: 指数上限は煙試験+スケーリング実測(shard 1 本の実測時間)を根拠に **W-B 登録追記で数値固定してから**掃引する(本 v1 では W-A のみ発効)。
- 計数規約: 宇宙の要素は**部分群**(同型商の重複はそのまま数える — 本数 ≠ 同型類数)。isolated 性は**判定して記録する属性**であり、宇宙の資格要件ではない。

## 窓ごとの判定パイプライン(規約)

1. **不変量**(全窓で記録): 指数・B₃/N の StructureDescription・N_ord = lcm(ord x, ord y, ord c)・c ∈ N か・**|Z(PB₃/N)|**(C2F 核予言子・裁定 147)・ord(σ₁ mod N)(命題候補「= 2·N_ord」の検証データを兼ねる)。
2. **ker χ̃ の枚挙**(c = 1 層のみ・簡約 hexagon): 位数と可換性を判定。
3. **理論フィルタ**(層 A・裁定記録の必要条件):
   - TIER-0 = ker χ̃ 可換 → **METABELIAN-CONFIRMED**(その窓の探索終了)
   - **TIER-1** = ker χ̃ 非可換(metabelian パターンの破れ — それ自体が発見)
   - **TIER-2 候補** = さらに |ker χ̃| が非可換単純群位数(60, 168, 360, 504, 660, 1092, 2448, …— band 上限までのリストを実装時に事前生成し証明書に同梱)で割り切れる
4. **TIER 到達窓のみ** GT(N) 全体の枚挙・導来列・可解性判定(full hexagon の独立再検証つき — C2F probe の二経路方式)。
5. 打ち切り(cap 超過)は **UNKNOWN** として窓単位で記録(失敗でない)。

## 実行と証明書

- 実行環境: ローカル(gap.ps1・-o 2g・600 秒 cap/shard)と GitHub Actions(setup-gap で 4.16.0 公式 tarball・sha256 検証・-o 8g・cap は shard 実測で固定)。**両環境とも GAP 4.16.0 に固定**。
- 証明書 schema **wall-cert/v1**: 窓 ID(指数+生成元語の正規形 hash)・不変量・ker χ̃ データ・TIER 判定・壁時計・GAP 版・実行環境(local | actions run ID)・打ち切り情報。shard 単位で JSON を artifact 回収。
- 照合: 独立レーン(python)が証明書の**抽出集合**(全 TIER-1/TIER-2 窓+TIER-0 の無作為抽出 ≥ 10%)について不変量と ker χ̃ 可換性を再計算して突合。二系統一致 = cross-checked(verified は Lean のみ)。
- 既知例ゲート(常備三分): positive = K⁽³⁾(ker = C₃ 可換・METABELIAN 側に落ちること)・negative = 該当なしの初期状態を明記・adversarial = N_Q(C2F 核あり窓 — 核の存在がパイプラインを誤らせないこと)。
- 実装上の既知注意: index = 1 の FactorGroup 不具合(GAP 4.16.0 + lins 0.9)は自明群への特殊分岐で回避(probe 報告どおり)。

## 撤退・停止

- 本キャンペーンは主線(dihedral 予想)の**従**: 主線のゲート便・測定が優先され、資源競合時は本キャンペーンを停止する。
- W-A で TIER-1 がゼロでも W-B へ拡張してよい(負の結果の band 拡張は登録追記のみで可)。判定規約の変更は不可(新キャンペーンとして登録し直す)。
