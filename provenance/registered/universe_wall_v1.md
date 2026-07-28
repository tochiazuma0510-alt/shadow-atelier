# 宇宙の事前登録: 壁キャンペーン v1.1(draft/candidate — falsifier 前哨反映済・Sol 便 78 ゲート待ち)

状態: **draft**(前哨監査 FAIL 5/NOTE 3 を全採用して v1 から改訂・Sol ゲート PASS で registered に昇格)。登録後の変更禁止 — 拡張は新 band の追加登録で行う。

## 目的(先に固定)

非 metabelian または非可解な GT(N) の存否を、事前固定した窓宇宙の中で悉皆判定する。動機は FINDING I-26(現 atlas 14 対象は全て metabelian)と層 A 必要条件群(裁定記録)。**全窓 metabelian という負の結果は一級の成果**(壁絶対性定理 (B1) の実験的裏付け)であり、探索の成否を TIER 到達の有無で定義しない。

## 宇宙の定義

- 母群: B₃ = ⟨a, b | aba = bab⟩(自由群 F(a,b) の剰余・この表示を固定)。
- 窓: N ⊴ B₃ かつ [B₃:N] ≤ 上限 かつ N ≤ PB₃。PB₃ 判定は標準全射 β: B₃ → S₃(a ↦ (1,2), b ↦ (2,3))の核との包含で行う。**根拠(NOTE-1)**: PB₃ = ker β は B₃ の非可換商 S₃ を与える指数 6 正規部分群として一意(probe 実測: 指数 6 の正規部分群 2 本中 S₃ 商は 1 本のみ — wall_probe_20260728.json)。別の全射 β′ を選んでも核は不変。
- 列挙器: GAP 4.16.0 + lins 0.9(`LowIndexNormalSubgroupsSearch` → `ComputedNormalSubgroups`・Firth/Holt)。
- **band W-A(ローカル参照帯)**: 指数 ≤ 192。probe 実測(search/certs/wall_probe_20260728.json): 正規部分群 319 本・うち PB₃ 内 66 本・壁時計 12.5 秒。
- **band W-B(CI 帯)**: 指数上限は煙試験+スケーリング実測(shard 1 本の実測時間)を根拠に **W-B 登録追記で数値固定してから**掃引する(本 v1.1 では W-A のみ発効)。CI 環境 = Actions/setup-gap(GAP 4.16.0 公式 tarball・sha256 検証・LEDGER 2026-07-28 記帳)。
- 計数規約: 宇宙の要素は**部分群**(同型商の重複はそのまま数える — 本数 ≠ 同型類数)。isolated 性は**判定して記録する属性**であり、宇宙の資格要件ではない。

## 窓ごとの判定パイプライン(規約)

1. **不変量**(全窓で記録): 指数・B₃/N の StructureDescription・N_ord = lcm(ord x, ord y, ord c)・**c ∈ N か**・**|Z(PB₃/N)|**(C2F 核予言子・裁定 147)・ord(σ₁ mod N)(命題候補「= 2·N_ord」の検証データを兼ねる)。
2. **ker χ̃ の枚挙**(c = 1 層)— 三つの規約(FAIL-1/FAIL-3 対応):
   - **(2a) 評価方式の分岐**: c ∈ N の窓は簡約 hexagon の商内評価・**c ∉ N の窓は語レベル評価(prepend 方式・week3-battery-common.g の既存分岐)**を用いる(commit 9fcb893 の教訓の明文化)。両方式とも構成に失敗した窓は UNKNOWN。
   - **(2b) 水準の規約**: ker χ̃ の元は **shadow(GT-pair)水準**で数え、合成は (3.53) で行う。**Φ の商群上の像で数えない**(C2F: Φ_on_PB₃/N は位数 2 の中心核を落とし、非可換核が可換な像に潰れる偽 TIER-0 を起こしうる — 裁定 147)。
   - **(2c) C2F 暫定札**: |Z(PB₃/N)| ≠ 1 の窓の TIER 判定は、full hexagon(B₃/N 内 (3.3)(3.4))の独立再検証(裁定 147 の二経路方式)と付き合わせるまで **PROVISIONAL** 札を付す。
3. **理論フィルタ**(層 A 必要条件 — **一方向**であることを明記): GT(N) 非 metabelian ⟹ ker χ̃ 非可換(対偶: [GT,GT] ⊆ ker χ̃ は Im χ̃ 可換から・ker 可換 ⟹ [GT,GT] 可換)。逆は主張しない(FAIL-2: ker χ̃ = [GT,GT] の等号は未証明)。
   - TIER-0 = ker χ̃ 可換 → **METABELIAN-CONFIRMED**(この含意は定理・その窓の探索終了)
   - **TIER-1** = ker χ̃ 非可換 = **必要条件通過・精査対象**(発見の主張ではない — 「metabelian パターンの破れ」を言えるのは段 4 の GT(N) 本体の導来列計算後のみ)
   - **TIER-2 候補** = さらに |ker χ̃| が非可換単純群位数(60, 168, 360, 504, 660, 1092, 2448, …— band 上限までのリストを実装時に事前生成し証明書に同梱)で割り切れる
4. **TIER-1 以上の窓のみ** GT(N) 全体の枚挙・導来列・可解性判定(full hexagon の独立再検証つき — 二経路方式)。非 metabelian の**主張はこの段の本体導来列でのみ**行う。
5. 打ち切り(cap 超過)は **UNKNOWN** として窓単位で記録(失敗でない)。**shard cap(600 秒)超過時は当該 shard 内の未完了窓のみ UNKNOWN とし、完了済み窓の判定は保持する**(NOTE-2)。

## 実行と証明書

- 実行環境: ローカル(gap.ps1・-o 2g・600 秒 cap/shard)と GitHub Actions(setup-gap・-o 8g・cap は shard 実測で固定)。**両環境とも GAP 4.16.0 + lins 0.9 に固定**。
- 証明書 schema **wall-cert/v1**: 窓 ID(指数+生成元語の正規形 hash)・不変量・ker χ̃ データ(方式 2a のどちらを使ったか併記)・TIER 判定(PROVISIONAL 札含む)・壁時計・GAP 版・実行環境(local | actions run ID)・打ち切り情報。shard 単位で JSON を artifact 回収。
- 照合: 独立レーン(python)が証明書の**抽出集合**(全 TIER-1/TIER-2 窓+TIER-0 の無作為抽出 ≥ 10%・**RNG シード = 20260728 に固定**(FAIL-5))について不変量と ker χ̃ 可換性を再計算して突合。二系統一致 = cross-checked(verified は Lean のみ)。
- 較正ゲート(常備三分+合成・FAIL-4 対応):
  - positive = K⁽³⁾(ker = C₃ 可換 → TIER-0 に落ちること)
  - adversarial = N_Q(C2F 核あり窓 — (2b)(2c) が核を落とさないこと)+ **c ∉ N 窓 1 本**(M_A5 系 — (2a) の語レベル分岐が発火すること)
  - **合成 TIER-1 fixture**: 判定コードに既知の非可換有限群(例 S₃)を ker χ̃ として直接注入し、**TIER-1 分岐(IsAbelian 否定側)が実際に発火する**ことを掃引前に確認(「全窓 TIER-0 潰れ」型の系統誤り検出)。
  - 較正 4 点のいずれかが失敗した状態での掃引結果は無効。
- 実装上の既知注意: index = 1 の FactorGroup 不具合(GAP 4.16.0 + lins 0.9)は自明群への特殊分岐で回避(probe 報告どおり)。

## 報告規約(NOTE-3)

宣言・報告時は必ず **全窓数・METABELIAN-CONFIRMED 数・TIER-1 数・TIER-2 数・UNKNOWN 数・UNKNOWN 率(%)・PROVISIONAL 数**を併記する。UNKNOWN が残る限り「全窓 metabelian」とは書かず「判定済み窓のうち」と書く。

## 撤退・停止

- 本キャンペーンは主線(dihedral 予想)の**従**: 主線のゲート便・測定が優先され、資源競合時は本キャンペーンを停止する。
- W-A で TIER-1 がゼロでも W-B へ拡張してよい(負の結果の band 拡張は登録追記のみで可)。判定規約の変更は不可(新キャンペーンとして登録し直す)。

## 改訂履歴

- v1 → v1.1: falsifier 前哨監査(FAIL 5/NOTE 3)を全採用。FAIL-1 (2a) 分岐・FAIL-2 TIER-1 文言弱化・FAIL-3 (2b)(2c) 水準規約・FAIL-4 合成 fixture・FAIL-5 シード固定・NOTE-1 β 一意性根拠・NOTE-2 shard cap 意味論・NOTE-3 報告規約。
