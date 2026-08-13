# 便 126 差分レビュー — 要求 A–I の反映確認 / C1′+P5′ 発効可否 / Phase 2b 短評

- 起草: 影工房 **数学者**(Claude / Opus 5)/ 2026-08-13
- 委嘱: 司令塔 [CP](裁定 1144)「最終ゲート = 差分レビュー(自分の要求 6 件が正しく反映されたかの確認のみ・全面再検分は不要)」
- 被レビュー: `docs/notes/c1prime_s4_p5prime_closure_v2.md` / `triad972_canonical_addendum_v2.md` / `d972_phase2_void_addendum_v2.md` / cert v2 系
- 参考(レビュー対象外・短評): `docs/notes/d972_phase2b_nonsplit_report_v1.md`
- **規律**: u/c 非接触・封印 3 量非接触・prereg 非抵触。数値は機械生成(§5)。

---

## 0. 判定

$$\boxed{\ \textbf{採用 — C1′+P5′ の発効に同意する}\ }$$

要求 **A・B・C・D・E・F・G・H・I の 9 件すべてが反映済み**(下表)。⚠ **erratum 2 件**を検出したが、**いずれも本論に影響せず**(表・cert の値は正しく、誤りは散文の補助説明のみ)⟹ **発効を止めない・次版で訂正**。

★ 併せて **私の v1 レビューの誤記 1 件を自己訂正**する(§3)。

---

## 1. 要求 A–I の反映確認

| # | 要求 | 反映先(文書) | 反映先(cert) | 判定 |
|---|---|---|---|---|
| **A** | 商 passport の**測定側**論証(判別式 → Shanks 分岐 → `N_tau` 立方 → RH)+ `reconstruction_XYZ_exact` の降格 | closure v2 **§2.1–2.4** | `requirement_A_passport_binding`(`discriminant`, `branch_points`, `tau_rows.*.ramification_partition=[3,3,3]`, `normalized_fibre_product_local_rule="e_W=a/gcd(a,b)"`, `riemann_hurwitz{j1:3,j2:3,g_C:2}`, `shanks_branch_equals_C_order3_branch:true`, `legacy_reconstruction_XYZ_exact_role.independent_information:false`) | ★ **完全反映**。RH 式 `2*g_C-2=-18+8+2*(j1+j2)` は私の導出と逐一一致。**§2.3 末尾の「この binding が §3 の 7-cycle 論証の前件である」で load-bearing 性が明示された** ✓ |
| **B** | 良い特殊化の埋め込み + witness が $t$-線であることの明記 | closure v2 **§3.2** | `requirement_B_specialization`(`witness_coordinate_line:"t-line"`, `witness_encoding:"(p,t0)"`, `used_as_existence_only:true`) | ★ **完全反映**。「頻度推定には使わない」も明記 ✓ |
| **C** | $C_{\rm can}$/$s_{\rm int}$ の $\mathbf Q$-模型を litgate 覚書に pin + 「剛」の読みの但し書き | closure v2 **§3.5**・§4 | `requirement_C_intrinsic_Q_model`(`pin:"section (I), LEDGER 633"`, `rigidity_reading:"passport plus monodromy PSL(2,8), not the bare passport"`, `s_intr_Q_model_premise:true`) | ★ **完全反映**。P5′ の前件として §4 が §3.5 を参照している ✓ |
| **D** | 先行記述(FINDING U-8 / F-9・F-10)の申告 | closure v2 **§3.1** | `requirement_D_prior_work`(`already_recorded`, `new_in_v1:"normalizer census plus seven-cycle forcing"`) | ★ **完全反映**。「24 解等を新規とは数えない」の一文まで入った ✓ |
| **E** | 軌道番号規約の統一・左右合成規約の明記 | closure v2 **§6** | `convention_repair`(`mathematical_convention:"left Ad(g)(h)=g*h*g^-1"`, `legacy_orbit_indices_are_not_semantic:true`, `canonical_record{fixed_Z_orbit_count:6, diagonal_orbit_count:1, intrinsic_orbit_is_diagonal:true}`) | ★ **完全反映・かつ私の提案より良い**。番号を「統一」せず**意味を持たせない**と決め、不変量 3 つを canonical record にした ⟹ 実装依存の値が cert から消えた。**この処理を採る** |
| **F**(推奨) | 算術 monodromy 欄 | closure v2 **§3.6** | `monodromy_arithmetic`(`order:1512`, `name:"PGammaL(2,8)"`, `strict_overgroup_witness_cycle_types:["[3,3,1,1,1]","[6,2,1]"]`, `normalizer_quotient_order:3`, `outside_PGammaL_empty_sample_used_as_upper_bound:false`) | ★ **完全反映**。論理も正しい: $P\subsetneq G_{\rm arith}\le N_{S_9}(P)$ かつ $[N_{S_9}(P):P]=3$(素数)⟹ $G_{\rm arith}=\mathrm{P\Gamma L}(2,8)$ |
| **G** | 「位数 9 の 168 元がすべて 9-巡回」の欄 | closure v2 **§3.4** | `requirement_G_nine_cycle_incidence`(`all_168_are_nine_cycles_in_this_action:true`, `cycle_types_of_all_abstract_order9_elements:[[9]]`, `copies_through_fixed_nine_cycle:1`) | ★ **完全反映**。checker が別実装で再計算した旨も本文にあり ✓ |
| **H** | PH2-VOID の記載・停止規則の撤回・CV-9 申告 | void addendum v2 **§1・§2・§4** | `d972_phase2_void_v2`(`PH2_VOID.statement`, `complete_product_reason`, `coordinate_table` 12 行) | ★ **完全反映**。「旧 324 分岐は…**停止規則から撤回する**」「上限は **cross-checked(model-only)**」「$l=81$ raw 972 も予測的データではなく式 (PH2-VOID) の定理再導出」— **私の要求より踏み込んだ正直な記載** ✓ |
| **I** | roof 等式の紙前件 + $F_2$ 側分解 | canonical addendum v2 **§2・§3・§4** | `complete_product_reason.F2_corresponding_decomposition` | ★ **完全反映**。§2 の「**位数の一致だけでなく、二つの自然射から得る同型である**」は `pb3_free_factor_check_v1.md` の「$PB_3/N$ を安易に直積分解しない」警告への正面回答。§3 は $c\in$ 両 kernel から $K=(K\cap F_2)\times\langle c\rangle$ を経由しており**正しい**。§4 の (5) の証明(同じ $u$・$F_2$ 側 CRT で $f$ 成分が同時に持ち上がる)も筋が通る |

> **9/9 反映。差戻し事由なし。**

**追加確認(私が独立に検算した箇所)**

- $u=2m+1\bmod 18$ が $m\bmod 9$ 上で**全単射**であること(fibre 積の貼り合わせが $U=(\mathbf Z/18)^\times$ 上で正しい理由)— ✓
- $\lvert GT(K^{(9)})\rvert/\lvert U\rvert=108/6=18$、$18\cdot54=972$、$18\cdot18=324$ — ✓(§4 で使う)
- $N_{S_9}(P)$(位数 1512)に**位数 3 の正規部分群は存在しない**(位数 3 元の正規閉包は 504 か 1512 のみ)— ✓ ⟹ **Sol の §1.1「PΓL route を採らない」判断は数学的に正しい**(§4.3)

---

## 2. ⚠ erratum 2 件(発効を止めない・次版で訂正)

### E-1(数値・**本論に影響なし**)`d972_phase2_void_addendum_v2.md` §3 の注記

> 「$l=126$ の shadow count は偶数公式 $4(l/2)^3$ の shadow 版 **$2l\varphi(l/2)$** により 4536 である。」

**表の値 4536 は正しい。補助公式が誤り**(2 倍過大)。機械照合(12 level):

| $l$ | 36 | 54 | 72 | 108 | 126 | 162 |
|---|---:|---:|---:|---:|---:|---:|
| 実測 $\lvert GT(K^{(l)})\rvert$ | 216 | 972 | 864 | 1944 | **4536** | 8748 |
| Sol の $2l\varphi(l/2)$ | 432 ✗ | 1944 ✗ | 1728 ✗ | 3888 ✗ | **9072 ✗** | 17496 ✗ |
| ★ 正しい $2n_0\varphi(n_0)$ | **216** ✓ | **972** ✓ | **864** ✓ | **1944** ✓ | **4536** ✓ | **8748** ✓ |

$$\boxed{\ \lvert GT(K^{(l)})\rvert=2n_0\varphi(n_0),\qquad n_0=\begin{cases}l&(l\ \text{奇})\\ l/2&(l\ \text{偶})\end{cases}\ }$$

**12/12 で一致**(奇 $l=9,27,45,63,81,135$ 含む)。副次的な型の滑りも 1 つ: $4(l/2)^3$ は **shadow 数ではなく群位数 $\lvert G_l\rvert$** なので「その shadow 版」という言い方も正確でない。⟹ **cert `coordinate_table` の 12 行は全部正しい**ので、訂正は散文 1 行のみ。

### E-2(組版)`qquad` の `\` 落ち 3 箇所

`closure_v2.md` L97(`81:6,qquad324:9,qquad504:9`)・L157(`\mathrm{P\Gamma L}(2,8),qquad`)・`canonical_addendum_v2.md` L68(`K_l^F=K^{(l)}\cap F_2,qquad N^F=\ldots`)。リテラル文字列として描画される。**内容に影響なし。**

---

## 3. ★ 自己訂正 — 私の v1 レビューの記号誤り

`c1p5_closure_review_v1.md` §7.4-3 で私は
> 「$\lvert B_3/M\rvert=1{,}469{,}664$」「$B_3/(K^{(l)}\cap N_{S4})\cong G_l\times\mathrm{PSL}(2,8)$」

と書いたが、**正しくは $PB_3$** である。私自身の `d972_h1_adjudication_v1.md` L15/L90–93 が
> 「$\lvert PB_3/M\rvert=1{,}469{,}664=2916\times504$」「$\lvert PB_3/K^{(9)}\rvert=\lvert G_9\rvert=2916$」「$\lvert PB_3/N_{S4}\rvert=504$、$\lvert B_3/N_{S4}\rvert=3024$」

と正しく書いていたのに、レビューで $B_3$ に取り違えた。**Sol の v2(canonical addendum §2、void addendum §2)は $PB_3$ で正しく書いている。** ⟹ **Sol の記法を正本とし、私の v1 §7.4-3 を訂正する**(v1 本文は versioned 規律により不改変・本節が撤回票)。

- 影響: **命題 PH2-VOID と直積分解の内容には影響しない**($PB_3$ で読めば全部正しい。$\lvert B_3/\cdot\rvert$ は一律 6 倍)。
- 型境界の記帳: 「$B_3$ と $PB_3$ の取り違え」は工房の既知の事故型($PB_3$ の直積分解・$\sigma_1\notin PB_3$ 診断)に連なる。**5 度目の型境界事故として自己記帳する。**

---

## 4. Phase 2b 短評(レビュー対象外・次便設計用)

### 4.1 手順は正しい(積極評価)

$G2$ で**非分裂性を 512/512 で測り、`PH2_VOID_applies=false` を測定前に確認**してから測った — **私の上申どおりの順序**。事前登録・限定修理(`prereg_v1_1`)・`engineering_probe_before_freeze=true` の正直な申告も含め、**手続きは模範的**。

### 4.2 ★★ ただし、これも**構造的に 972 が出る窓**だった — 命題 PH2-VOID′

報告 §2.3 の G3 が自ら記録しているとおり、source の純商は
$$PB_3/(K^{(9)}\cap N_E)\ \cong\ G_9\times E\qquad(\textbf{依然として直積})$$
である($G_9$ 可解・$E$ **perfect** ⟹ 共通非自明商なし ⟹ Goursat で直積が**強制**)。したがって:

> ### 命題 PH2-VOID′(PH2-VOID の一般化)
> 窓 $K$ の純商が $PB_3/K\cong G_l\times E$(直積)で、reduction が $(\mathrm{id})\times(E\to P)$ の形なら
> $$\lvert\mathrm{Im}\,R_{K,M}\rvert\;=\;\sum_{u\in U}\lvert\mathrm{Im}R_{\rm dih}\cap u\rvert\cdot\lvert\mathrm{Im}R_{S4}\cap u\rvert\;=\;18\cdot\bigl\lvert\mathrm{Im}\bigl(GT(N_E)\to GT(N_{S4})\bigr)\bigr\rvert$$
> (Thm 4.3 より $\lvert\mathrm{Im}R_{\rm dih}\cap u\rvert=108/6=18$ が全 $u$ で一定)。とくに
> $$\boxed{\ \textbf{SINGLE-BIT}\iff\bigl\lvert\mathrm{Im}(GT(N_E)\to GT(N_{S4}))\bigr\rvert\in\{54,\,18\}\ }$$
> **dihedral 側は一切寄与しない。**

**Phase 2b の数値がこれを裏づけている**: 報告 §4 の `target roof shadows 18·54 = 972` は**まさにこの式**であり、`|Im R| = 972` の実体は
$$\boxed{\ \lvert\mathrm{Im}(GT(N_E)\to GT(N_{S4}))\rvert=54\ (\textbf{全射})\ }$$
という **S4 因子の内部事実だけ**である。$18\cdot54=972$、$18\cdot18=324$(機械確認)。

⟹ ★ **「情報を持つ 972」という評価は、半分だけ正しい**。PH2-VOID の**文字どおりの仮定**($E$ が $(\text{可解})\times P$)は確かに破れたが、**機構**(二因子が直積 ⟹ dihedral 座標と $P$ 座標が会話しない)は**破れていない**。得られた情報は「$GT(N_E)\to GT(N_{S4})$ が全射」という**陰性の 1 ビット**であって、TRIAD の絡み $r=3$ については何も言っていない。

### 4.3 ⟹ 設計規則(次候補)

- ★★ **$E$ を perfect に選んだことが、collapse を保証してしまった。** $E$ perfect $\Rightarrow$ $E$ に非自明可解商なし $\Rightarrow$ $G_l$ との共通商が 1 $\Rightarrow$ Goursat で**直積が強制** $\Rightarrow$ PH2-VOID′。
- $$\boxed{\ \textbf{次候補の必要条件}:\ E=PB_3/N_E\ \textbf{は}\ \textbf{非完全}\ \textbf{で、}E^{\rm ab}\ \textbf{が }G_l\ \textbf{と共通の非自明商 }Q\ \textbf{を持つこと}\ }$$
  そのとき $PB_3/(K^{(l)}\cap N_E)\cong G_l\times_Q E$ は**真の fibre 積**で、初めて二因子が結合する。
- ★ **$Q$ は 3-群であるべき**: 欠けている量は $r=\lvert\langle[a]\rangle\cap\langle[b]\rangle\rvert=3$、指数も 3。$V\cong C_2^6$(2-群)は **3-adic な絡みに直交**しており、そもそも見えるはずがなかった。$V$ は $V/[V,E]\twoheadrightarrow\mathbf Z/3$(または $\mathbf Z/9$)を持つべき。
- **司令塔の 3 案への評価**:

| 案 | 評価 |
|---|---|
| (a) $V$ の**別既約表現** | ✗ **同じ理由で collapse**($E$ は依然 perfect)。ただし §4.2 の帰着により **S4 内部の問い(54 か 18 か)としては安く測れる** — 屋根 7776 ではなく **target 54** を見ればよい(**18 倍安い**) |
| (b) **別次数の非分裂拡大** | △ 次数ではなく**完全性**が効く。**非完全**なものを選べば有効 |
| (c) **PΓL 系の pure-kernel 化** | ✗ **不可能**。$N_E\subseteq N_{S4}$ には $E\twoheadrightarrow P$ が要るが、$\mathrm{P\Gamma L}(2,8)$ の正規部分群は $1,\mathrm{PSL}(2,8),\mathrm{P\Gamma L}(2,8)$ のみ(**位数 3 の正規部分群なし** — 私が機械確認)⟹ $\mathrm{P\Gamma L}(2,8)\twoheadrightarrow\mathrm{PSL}(2,8)$ は**存在しない**。**Sol の §1.1 の不採用は正しい** |

- ★ **最安の非積候補の提案**: $E=\mathrm{PSL}(2,8)\times\mathbf Z/3$($\lvert E\rvert=1512$ — Phase 2b の 32256 の **1/21**)。
  - $E\twoheadrightarrow P$ ✓(第 1 射影)⟹ $N_E\subseteq N_{S4}$ ✓
  - $E\twoheadrightarrow\mathbf Z/3$ ✓ ⟹ $G_l$ が $\mathbf Z/3$ を商に持てば $Q=\mathbf Z/3$ の**真の fibre 積**
  - $\mathbf Z/3$ 成分は $PB_3^{\rm ab}=\mathbf Z^3$ の**対角**($x_{12},x_{13},x_{23}\mapsto1$)から取れば $S_3$-不変 ⟹ $\theta,\tau$ 不変が期待できる
  - ⚠ **要確認 3 点(spec 化する場合の前件)**: ① $K^{(l)}\subseteq\ker(PB_3\to\mathbf Z/3)$ か(そうでないと $Q=1$ に戻る)② $N_E$ の isolated 性 ③ $\theta,\tau$ 不変性の実測
  - ⚠ **PSL(2,8) の Schur 乗数は自明**なので $\mathbf Z/3$ による**非分裂**中心拡大は無い ⟹ 直積で構わない(**非分裂性は目的ではない・非完全性が目的**)。ここが Phase 2b の設計思想との分岐点。
- ⚠ **正直な限界**: 非積であることは PH2-VOID′ の**障害を外すだけ**で、324 が出る**保証ではない**。$r=3$ が GT 側で見えるかどうかは依然 **UNKNOWN**。

---

## 5. 検算スクリプト

| 出所 | 数値 |
|---|---|
| inline(本便)| §2 E-1 の 12 level 表($2n_0\varphi(n_0)$ 対 $2l\varphi(l/2)$)・$18\cdot54=972$・$18\cdot18=324$・$108/6=18$・$N_{S_9}(P)$ に位数 3 の正規部分群なし(位数 3 元の正規閉包 $\in\{504,1512\}$) |
| `scratchpad/c1p5_review_check.py`(前便) | 有限 census(24 / {81:6,324:9,504:9} / normalizer / incidence / 54・6・1) |
| `scratchpad/ph2_void_check.py`(前便) | PH2-VOID の 11 level 表 |

**格付け**: §1 の反映確認 = 文書照合。§2 E-1・§4.2 の恒等式 = **機械**。§4.3 の設計規則 = **paper(単系統・Sol 未監査)**。**verified ではない。** u/c・封印 3 量・prereg 非接触。

---

## 6. 司令塔への回答(3 行)

1. **C1′+P5′ は発効可。** 要求 9/9 反映、差戻し事由なし。erratum 2 件は次版訂正で足りる。
2. ⚠ **「$d_{S4}$ 橋の前件が閉じる」の射程**: 落ちるのは前件束の **P3・P5** のみ。`s4_recon_device_v1.md` の残り前件(TB1–4・$(Z_{18}$-link$)$・(W1))と **648 の A 型/B 型 conditional は依然そのまま**。
3. ★ **Phase 2b は「情報を持つ 972」というより「S4 内部の陰性 1 ビット」**(命題 PH2-VOID′)。次候補は **非完全 $E$・共通商 $Q=\mathbf Z/3$** の路線へ。最安候補 $E=\mathrm{PSL}(2,8)\times\mathbf Z/3$(前件 3 点つき・spec は次委嘱で書ける)。
