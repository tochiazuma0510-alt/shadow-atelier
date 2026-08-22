# c83_closure_index_v1 — 83 窓線(④ χ 扉)完結索引(2026-08-22)

## §0 三行
1. **何が閉じたか**: isolated 2 窓の GT(N) 全 48 元が mod-p Frattini 単段探針(p=2,3・22 元は p=5 も)を全員生存 — **fake ゼロ**。深度線は定理と実測の組で閉鎖。
2. **何が残ったか**: 非内部 45/42 元の生存機構(主要残問)・dim End_Q(V)=24/12=K_ord の一致の読解・GAP-83-3・TORUS-GAP-1。
3. **再開条件**: **c∉N の対象に適用できる算術機構**の入手(金庫 intel/: Ishii 2312.04196・Enriquez 1003.1012・Lochak–Nakamura–Schneps 2602.12462)。

## §1 正本の主張
**C-83-FINAL v3** — CLAIMS **C-15** に登録(2026-08-22)。逐語 = `scratchpad/c83_final_v3_draft.md`。格 = candidate(K₃ 24 行判定は cross-checked・格付け条件 2 = 共通モード注記+C6-elt data-pin 依拠・Sol 未監査・verified 未)。

## §2 閉じたもの
### 2.1 深度線(cert と sha)
| cert | 内容 | sha256[:16] |
|---|---|---|
| koubou83_survival_v3_1_20260822.json | K(p=2)最終形・4 代表+witness | (git 収蔵・freeze e138fcea) |
| koubou83_survival_k3_v1_1_20260822.json | K₃(p=3)26 行・バグ史・対照・m 簿記 | 486d7490c34700d2 |
| koubou83_k3_witness_export_v1_20260822.json | witness 生値(f/w/k/f″/witness_m) | 884e9c2199188eab |
| crosscheck/verdicts/koubou83_survival_k3_crosscheck_v2 | 独立照合 v2(破壊対照つき 24/24) | (v2・supersedes v1) |
| koubou83_survival_k5_v1_20260822.json | K₅(p=5)全生存(単系統・情報量 UNKNOWN) | 81ba289e5fc8f5b9 相当 |
| koubou83_h2_obstruction_v1_20260822.json | dim H²=23/11(3 経路)・障害類 48/48 ゼロ | d54401ed798016e4 |
| koubou83_closure_v1_20260822.json | A-1 撤回・A-2′ 48/48・A-3・A-4・COMP-1・end_ring_dims | c127f4ddb892914c |
| koubou83_charming_sweep_v1_20260822.json | p=2 charming 掃引 24 行・位数ラベル | efc6066798e536d3 |
### 2.2 経路の閉鎖 3 本
K₆ 等 squarefree 合成細分 = CRT で K₂∧K₃ に分解(定理・走行禁止)/3 塔第 2 段 = [N:K₃]=3^98 で到達不能/Guillot 比較写像 Φ = c∉N で定義域外(week3-比較写像_guillot_v2.md §2.1 補題 G0・§4 — 検疫解除は不要かつ無益)。
### 2.3 機構の排除 3 本
𝒯(fake torus)由来 = W-2 全 FALSE で排除(片側)/𝒯 以外の離散族 = 半径 R(m∈[−12,12]・音節≤4・指数±3・77700 悉皆)まで不在/charming = CH-0 で恒久無力。

## §3 定理群(証明つき・再利用可)
補題 U(族 f_n=yⁿx⁻ⁿ の hexagon 恒等式)/2 進塔 futility(order3 は全段で族的持ち上げ)/𝒯≅ℤ̂ 閉部分群 ∧ 𝒯∩ĜT_gen={1}/補題 MIRROR(τ′=θτ⁻¹θ・(3.10)+charming 下で判定同値)/命題 CH-0(可換化 (0,0) 代表 ⟹ charming 全深度無力)/命題 P5-0(p≠3 の単段は族が CRT で通過)/**定理 C-83-INN**(α_g∈Inn(Q) ⟹ 全特性細分で永久生存)/**補題 KER-π**(ker π* = End_{F_p[Q]}(V)·e)/K₆ の CRT 分解。
規約(本日新設・正本は裁定簿): FRED-1・ARB-1(+2)・TAU-1(1〜7)・MAT-1・CHAR-1・ESC-1・SEMA-1・INFO-1・CANARY-1/2・STRUCT-1・LEG-1・PRED-WELLPOSED-1・EVID-1・WITNESS-NORM-1。

## §4 残問(優先順)
1. **45/42 元の生存機構**(非内部・非整数・非族の三重に説明不能 — 「23 次元障害空間で全員の障害類がなぜ 0 か」)
2. dim End_{F_p[Q]}(V) = 24/12(p 非依存・実測)。**K_ord との一致は p=2 限定で p=3(K₃_ord=36)で破れる ⟹ 偶然と判定・追跡せず**(裁定 1498)。本質は dim ker π* ≤ 24/12 < 大 ⟹ **障害消失は「安くない」⟹ 残問①は未解消・強化**。次の初手 = **予想 P-83-5**(V ≅ F_p[Q/H]⊕F_p²・|H|=12/24・#(H\Q/H)=16/4 — 検査は秒・当たれば残問①が加群論の問題に書き直せる)
3. GAP-83-3(p∤|GT(N)| ⟹ 自動生存、は未証明 — Ω は捻れ 1-コサイクルで素の加法性は ill-posed)
4. TORUS-GAP-1(整数 hexagon 対の λ=±1 限定 — 半径 R 有界悉皆のみ)

## §5 予言簿
P-83-1(order6 死)= 反証/P-83-2(order3 死)= 反証/P-83-3 W-1 = VOID(charming の言い換え・設計ミス)・W-2 = 的中(片側・全 FALSE)/P-83-4(p=5 全生存)= 的中(情報量 UNKNOWN)。C-83 v1(障害消失 ⟺ integral)→ v2(片側のみ定理)へ改訂。**「登録が直感に勝った」実例**(C-83 スケッチ vs P-83-3)を含む — 事前登録制度の価値の実証。

## §6 計器の在庫(再開時にそのまま使える)
producer(GAP): B の scratchpad スクリプト群(koubou83_*.g — K/K₃/K₅ 装置・差分定義 A・γ-canary・COMP-1)/checker(Python): crosscheck/check_koubou83_survival_v3.py・check_koubou83_survival_k3.py(v2・係数追跡・破壊対照)・check_koubou83_tref_v1.py/数学者検算(セッション scratchpad): arith.py(COMP-1 参照・48 元列挙・[11,1])・h2spec.py・close.py(内部性悉皆)・integral.py・mirror.py 等。常設対照: **C-83-ARITH-PC**([11,1] は理論が生存を保証 — 死んだら計器バグ)・NC-1(f₄ 素通し charming=false)・PC-1(真の交換子)・破壊対照(witness 削除 = 判別子)。

## §7 handover 導線
- **再開条件**: c∉N 対象に効く算術機構。金庫の elliptic GT 3 本の降ろし検問(司令塔義務): ①c∉N 適用可否(定義域明示)②Im(Ih_N) を下から評価する手続き ③B₃-gentle への翻訳。
- **再開初手**: [11,1] を陽性対照に Im(Ih_N)∩ker χ_vir(位数 12)を下から詰める — 22 候補はちょうどこの全射性の障害集合。
- **再開しない場合**: C-15 で完結。「fake を 3 素数・全域で探して見つからなかった」機構つき負結果+定理群+規約 15 本が成果。
- 経緯の正本: 裁定簿(セッション scratchpad/pending_ruling1206.md 1433〜1497)→ LEDGER 転記後はそちら。Sol 報告 = 便 154。
