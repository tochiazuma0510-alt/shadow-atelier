# c83_closure_index_v1 — 83 窓線(④ χ 扉)索引(2026-08-22・**Sol 便 154 差し戻し反映 = v4 限定文言**)

> **⚠ 監査注記**: 同日の Sol 便 154(sol/sol_reply_154_daily.md)= **差し戻し(STOP 4 = F1〜F4)**。本索引は限定文言へ同期済み。正本 = CLAIMS C-15(v4)。

## §0 三行
1. **どこまで到達したか**: isolated 2 窓で **full-48 単段生存が二素数とも cross-checked**(便 155・WO-155-1): p=3 = v2 producer(核不変性で厳尽)×独立照合器 96/96・p=2 = v3(PIN-AB-1 準拠・**初の実検査** — v1/v2 は単位 2 倍バグ INC-13 で mod-2 検査が恒真化)×同 96/96。照合器 = Luna 実装・著者分離・producer 非開封・全ゲート 192/192・対照 P-A2-1/2 的中(verdict a144249b…・commit d7a3ff09・射程 pin は CLAIMS C-15)。K₃ 深部 24 行 cross-check(維持理由 = 法 3 冪で単位誤差不可視)・障害類 = p=3 の 26/26 ゼロも維持。**登録済み有限探針からは fake 証明書 0(全体判定 = UNKNOWN-DEPTH/UNKNOWN-STRUCTURAL — 便 155 後も不変)**。
2. **何が残ったか**: 非内部元の生存機構(主要残問)・**GAP-INN-1 = C-83-INN の marked-form lift 補題(F4・conditional のまま)**・transgression 実 rank(End 次元読解は撤回)・GAP-83-3・TORUS-GAP-1。〔K₆ fibre-product = proved 昇格・F1 再走帰結 = 解決 — 便 155 反映〕
3. **再開条件**: **c∉N の対象に適用できる算術機構**の入手(金庫 intel/: Ishii 2312.04196・Enriquez 1003.1012・Lochak–Nakamura–Schneps 2602.12462)。lane の現状 = **park**(登録済み経路の使い切りによる休止・非存在定理ではない)。

## §1 正本の主張
**C-15(v4)= CLAIMS 正本**(2026-08-22・便 154 差し戻し反映)。v3 逐語 = `scratchpad/c83_final_v3_draft.md`(**撤回バナー付き封存・引用禁止**)。格 = K₃ 24 行のみ cross-checked(格付け条件 2 = 共通モード注記+C6-elt data-pin 依拠)・p=2 full-48 は単一系統 candidate・verified 未。

## §2 閉じたもの
### 2.1 深度線(cert と sha)
| cert | 内容 | sha256[:16] |
|---|---|---|
| koubou83_survival_v3_1_20260822.json | K(p=2)最終形・4 代表+witness | (git 収蔵・freeze e138fcea) |
| koubou83_survival_k3_v1_1_20260822.json | K₃(p=3)26 行・バグ史・対照・m 簿記 | 486d7490c34700d2 |
| koubou83_k3_witness_export_v1_20260822.json | witness 生値(f/w/k/f″/witness_m) | 884e9c2199188eab |
| crosscheck/verdicts/koubou83_survival_k3_crosscheck_v2 | 独立照合 v2(破壊対照つき 24/24) | (v2・supersedes v1) |
| koubou83_survival_k5_v1_20260822.json | K₅(p=5)全生存(単系統・情報量 UNKNOWN) | 81ba289e5fc8f5b9 相当 |
| koubou83_h2_obstruction_v1_20260822.json | dim H²=23/11(3 経路)・障害類 = **p=3 の 26/26(非自明 24+対照 2)ゼロ**(「48/48・両素数」は F2 で撤回済 — cert 実母数どおり) | d54401ed798016e4 |
| koubou83_closure_v1_20260822.json | A-1 撤回・A-2′・A-3・A-4・COMP-1・end_ring_dims — **⚠ hard-coded 集計の単一系統 candidate(manifest なし・A-2′「48/48」は F1 で無効・erratum 追記済・cross-checked 根拠に使わない)** | (erratum 追記で sha 更新) |
| koubou83_charming_sweep_v1_20260822.json | p=2 charming 掃引 24 行・位数ラベル | efc6066798e536d3 |
### 2.2 経路の閉鎖 3 本
K₆ 等 squarefree 合成細分 = CRT で K₂∧K₃ に分解(定理・走行禁止)/3 塔第 2 段 = [N:K₃]=3^98 で到達不能/Guillot 比較写像 Φ = c∉N で定義域外(week3-比較写像_guillot_v2.md §2.1 補題 G0・§4 — 検疫解除は不要かつ無益)。
### 2.3 機構の排除 3 本
𝒯(fake torus)由来 = W-2 全 FALSE で排除(片側)/𝒯 以外の離散族 = 半径 R(m∈[−12,12]・音節≤4・指数±3・77700 悉皆)まで不在/charming = CH-0 で恒久無力。

## §3 定理群(数学者検分後の最終格・逐語 = scratchpad/c83_inn_lift_lemma_v1.md)
**維持**: 補題 U/U′(hexagon が B₃ の恒等式)/𝒯≅ℤ̂ 閉部分群 ∧ 𝒯∩ĜT_gen={1}/補題 MIRROR。**proved(新規・数学者)**: **KER-π**(仮定 5 点明示・自己完結初等証明・transgression=−φ_*e・Lean 向き)/**K₆ fibre-product compatibility**(無条件 ⟹「K₆ は新情報なし」は定理)/**T-EX**(1 段族 lift)/**T-DEAD**(補題 LAT: Λ_{K_n}=nΛ_N ⟹ 厳密族機構は K≤K₃ cofinal で必ず死 = この路線で永久生存は原理的に証明不能)/**T-DEF**(1 段変形の線型判定)/**A2-TAUT**(p≠3 では cond3 恒真)/**命題 NOGO-1**(T_{m,f} は hexagon 情報を落とす — C-83-INN 4 行証明の反例)。**降格確定(F4)**: C-83-INN — 𝒯 3 元の永久生存は撤回・欠落 =【GAP-INN-1】。**射程限定で受理(Sol §2)**: CH-0(witness 独立検算で非障害を再確認・abg(f″)=(0,0,0) 24/24)/P5-0/2 進塔 futility。**End 次元読解の撤回は確定**(24>23・12>11)。**副産物**: 窓 154163 は inner=6 元で「inner=𝒯 像」は偽・GT(N)→Aut(Q) 非単射。
規約(本日新設・正本は裁定簿): FRED-1・ARB-1(+2)・TAU-1(1〜7)・MAT-1・CHAR-1・ESC-1・SEMA-1・INFO-1・CANARY-1/2・STRUCT-1・LEG-1・PRED-WELLPOSED-1・EVID-1・WITNESS-NORM-1。

## §4 残問(優先順)
1. **45/42 元の生存機構**(非内部・非整数・非族の三重に説明不能 — 「23 次元障害空間で全員の障害類がなぜ 0 か」)
2. dim End_{F_p[Q]}(V) = 24/12(p 非依存・実測)。**K_ord との一致は p=2 限定で p=3(K₃_ord=36)で破れる ⟹ 偶然と判定・追跡せず**(裁定 1498)。**「dim ker π*≤24/12 は小さい ⟹ 障害消失は安くない」の読解は撤回(Sol §2 — dim だけでは像が H² 全体の可能性すら排除できない)。中立な残問 = transgression φ↦φ_*e の実 rank/像次元の測定**。次の初手 = **予想 P-83-5**(V ≅ F_p[Q/H]⊕F_p²・|H|=12/24・#(H\Q/H)=16/4 — 検査は秒・当たれば残問①が加群論の問題に書き直せる)
3. GAP-83-3(p∤|GT(N)| ⟹ 自動生存、は未証明 — Ω は捻れ 1-コサイクルで素の加法性は ill-posed)
4. TORUS-GAP-1(整数 hexagon 対の λ=±1 限定 — 半径 R 有界悉皆のみ)

## §5 予言簿
P-83-1(order6 死)= 反証/P-83-2(order3 死)= 反証/P-83-3 W-1 = VOID(charming の言い換え・設計ミス)・W-2 = 的中(片側・全 FALSE)/P-83-4(p=5 全生存)= 的中(情報量 UNKNOWN)。C-83 v1(障害消失 ⟺ integral)→ v2(片側のみ定理)へ改訂。**「登録が直感に勝った」実例**(C-83 スケッチ vs P-83-3)を含む — 事前登録制度の価値の実証。

## §6 計器の在庫(再開時にそのまま使える)
producer(GAP): B の scratchpad スクリプト群(koubou83_*.g — K/K₃/K₅ 装置・差分定義 A・γ-canary・COMP-1)/checker(Python): crosscheck/check_koubou83_survival_v3.py・check_koubou83_survival_k3.py(v2・係数追跡・破壊対照)・check_koubou83_tref_v1.py/数学者検算(セッション scratchpad): arith.py(COMP-1 参照・48 元列挙・[11,1])・h2spec.py・close.py(内部性悉皆)・integral.py・mirror.py 等。常設対照: **C-83-ARITH-PC**([11,1] は理論が生存を保証 — 死んだら計器バグ)・NC-1(f₄ 素通し charming=false)・PC-1(真の交換子)・破壊対照(witness 削除 = 判別子)。

## §7 handover 導線
- **再開条件**: c∉N 対象に効く算術機構。金庫の elliptic GT 3 本の降ろし検問(司令塔義務): ①c∉N 適用可否(定義域明示)②Im(Ih_N) を下から評価する手続き ③B₃-gentle への翻訳。
- **再開初手**: [11,1] を陽性対照に Im(Ih_N)∩ker χ_vir(位数 12)を下から詰める — 22 候補はちょうどこの全射性の障害集合。
- **再開しない場合**: C-15(v4)の park 記録で総括 — 「**登録済み有限探針(3 素数)からは fake 証明書 0**」という限定つき負結果+定理群(格付き)+規約 15 本+incident table が成果。「完結/非存在/深度線閉鎖」とは書かない(F3)。
- 経緯の正本: 裁定簿(セッション scratchpad/pending_ruling1206.md 1433〜1497)→ LEDGER 転記後はそちら。Sol 報告 = 便 154。
