# A/B 判定計器の設計規則改訂 — ★ 規則は工房に既にあった(SPLIT-NULL″)+ 軸 1 の gating PASS

- 起草: 影工房 **数学者**(Claude / Opus 5)/ 2026-08-13
- 委嘱: 司令塔(裁定 1146)「A/B 判定計器の**設計規則改訂**。3-adic の絡み $r=3$ に見える計器の**必要条件を先に定式化**。**盲でないことの証明を候補より先に**」
- **規律**: u/c 非接触・封印 3 量非接触・prereg 非抵触($r=3$ という整数のみ使用)。数値は機械生成(§7)。

---

## 0. 結論(先に 4 行)

1. ★★★ **設計規則は工房に既にあった** — `ihnec_v1.md` §6.4 **系 SPLIT-NULL″**(裁定 374/388):
   > 「**fake(A 型)を検出しうる細分は、$G_n$ と非自明な共通商をもつ「entangled 屋根」に限る。分裂屋根をいくら積んでも $\mathrm{GT}_{\rm gen}$ は縮まない。** $\mathrm{PSL}(2,8)$ 窓は**最も検出力の低い型**(共通商が完全に自明)」
   ⟹ **3 連続の盲目性は数学のギャップではなく索引の失敗**である。Phase 2・Phase 2b・$C_3$ 橋はすべて**既存の工房定理に反する設計**だった。
2. ⚠ **私の PH2-VOID / PH2-VOID′ は 定理 SPLIT-NULL の再発見**である。**§1 で全面撤回・訂正する**(便 125/126 レビューの新規性主張の取消し)。
3. ★★ **便 127 は軸 1 を殺していない**。死んだのは**可換**$C_3$ 橋だけ。**非可換 $S_3$ 橋は生きている** — **$G_l\twoheadrightarrow S_3$ が存在する**($l=9,27,36$ で各 **18** 個・機械確認・§4)。$S_3^{\rm ab}=C_2$ は 2 群 $G_l^{\rm ab}$ の商になれるから、便 127 と矛盾しない。
4. ⟹ **推薦: 軸 1(非可換共通商 $Q=S_3$)を続行**。$K^{(l)}$ 族を捨てる必要はない。**足りないのは S4 側**($PB_3/N'\twoheadrightarrow\mathrm{PSL}(2,8)$ かつ $\twoheadrightarrow S_3$)。

---

## 1. ★ 訂正票 — 先行記述の見落とし(4 件・私の連続失敗)

### 1.1 撤回する新規性主張

| 私の主張 | 出所(私の文書) | ★ **先行記述** | 判定 |
|---|---|---|---|
| **命題 PH2-VOID**(屋根 fibre 積模型で像が恒等的に 972) | `c1p5_closure_review_v1.md` §7.2(★新規と記帳) | **定理 SPLIT-NULL**(`ihnec_v1.md` §6.4・裁定 374/388)— 仮定「共通非自明商なし ⟹ $PB_3/M\cong G_n\times PB_3/N'$」、結論「像は $m$-fiber の合併 = $\mathfrak F_0$ 方向を一切削らない」 | ★ **再発見。撤回** |
| **命題 PH2-VOID′**(積窓なら $\lvert\mathrm{Im}R\rvert=18\cdot\lvert\mathrm{Im}R_{S4}\rvert$) | `c1p5_v2_diff_review_v1.md` §4.2(★★と記帳) | **系 SPLIT-NULL″** + `counterexample_hotspots_ideation_v1.md` §75「SPLIT-NULL(工房定理・裁定 374/388): B 型が可視なのは entangled 屋根か MCOV 破れ窓のみ — **分裂屋根では原理的に不可視**」 | ★ **再発見。撤回** |
| $PB_3/(K^{(l)}\cap N_{S4})\cong G_l\times\mathrm{PSL}(2,8)$(Goursat) | 同上 §4.2 / `d972_h1_adjudication_v1.md` | **`ihnec_v1.md` L365 に逐語**(「$G_9$ 可解・$P$ 非可換単純ゆえ共通商は 1。Goursat より $PB_3/M=G_9\times P$」)。$\lvert PB_3/M\rvert=1{,}469{,}664=2916\cdot504$ は **P-IHN-2** として事前登録済 | ★ **再発見。撤回** |
| 絡みの体 $=\mathbf Q(\zeta_9,\sqrt[3]2)$ | 本稿初稿 §1.3(★新規と記帳) | ★ **私自身の** `d972_phase2_design_v1.md` §48「$\langle[a]\rangle\cap\langle[b]\rangle=\langle2^3\rangle$ ⟹ 重なりは $2^{1/3}$ の立方体(共通の 3 次部分拡大)」 | ★ **自己再発見。撤回** |
| $A_{\rm arith}$ の $\mathbf F_3^2$ 4 直線記述(系 DELTA) | 本稿初稿 §1.4 | **crown census**(裁定 **1041/1050**)「972 屋根 = 8 類・**非正規 4 類 ↔ $\mathbf F_3^2$ の 4 直線**(独立確認)= **$r$ の 4 値観測の器**」+ `ideas_surg_boost_v1.md` §51「屋根の全射性の実質は『**joint Kummer 像 mod $\Phi$ が $\mathbf F_3^2$ で階数 2 か**』という $\mathbf F_3$ 線形代数 1 問」 | ★ **再発見(2 日前の裁定)。撤回** |
| 共通商が非可換 | 本稿初稿 §1.3 | `u9bit_apriori_v1.md` §53「**$L_9\cap L_{S4}$ は非可換でありうる**(共通商が Aff 型なら非可換)⟹ Kronecker–Weber は適用できない」(既に仕様訂正を発生させている) | △ **「ありうる」→「である」の確定のみが増分** |
| **定理 DUAL**(B 型は 1 元で確定) | 本稿初稿 §3.2 | ★ **逆である**。正典 2401 **Cor 5.4**:「fake ⟺ ある細分で像に入らない(**有限検証 1 個で fake 証明が完結**)/ genuine は深さ $d$ まで survive(**UNKNOWN 一級**)」 | ★ **誤り。撤回**(§1.2) |
| **定理 COMPACT**($\mathcal{PR}_M(\widehat{GT}_{\rm gen})=\bigcap\mathrm{Im}R$) | 本稿初稿 §3.3 | 正典 2401 **Thm 5.2**「$\Psi:\widehat{GT}_{\rm gen}\cong\varprojlim(\mathrm{ML})$」の直接の帰結(抽出ノート L126)。cofinality も **裁定 1033 で既決** | △ **正典の系。新規ではない** |

### 1.2 ⚠ 定理 DUAL は**誤り**だった

初稿で「**B 型は 1 元で確定する**」と書いたが、これは**逆**である。正典 Cor 5.4 の通り:
$$\textbf{fake(A 型)}=\textbf{有限証明書 1 個},\qquad \textbf{genuine}=\textbf{全深度}=\textbf{UNKNOWN 一級}.$$
「$\delta\ne0$ の genuine な shadow を 1 個見つければ」の**「genuine と示す」部分が全深度を要求する** — そこが困難の本体であり、私は困難を前提に隠していた。**掟 2(genuine を有限深度の PASS から導かない)への抵触寸前**であり、撤回する。

### 1.3 ★ 根本原因と恒久対策(私のプロセス欠陥)

4 回連続の novelty-grep 失敗の原因は明確である: **自分の造語(PH2-VOID・絡み座標)で grep していた**。造語は当然 0 件になる。

> ### 私に課す規律(即時適用)
> 1. **概念語彙で grep する**: 「共通商 / Goursat / 直積 / 分裂 / entangled / 検出しない / 縮まない」等。今回それを実行したら **SPLIT-NULL が 279 件**ヒットした。
> 2. **`docs/notes/session_20260813_results_index.md` を委嘱の最初に読む**(まさにこの用途の索引が存在していた)。
> 3. **grep 領収書には「自分の新規ファイルを除外した実測値」を書く**(初稿は除外せず 0 件と誤記した — §7 で訂正)。

---

## 2. 既存規則の再掲(改訂ではなく**再発見の追認**)

> ### 定理 SPLIT-NULL(`ihnec_v1.md` §6.4・裁定 374/388)
> $M=K^{(n)}\cap N'$ で $G_n$ と $PB_3/N'$ に共通の非自明商が無いなら $PB_3/M\cong G_n\times PB_3/N'$ で、$\mathrm{Im}R_{M,K^{(n)}}$ は $m$-fiber の合併。⟹ **分裂屋根は $\mathfrak F_0$ 方向を一切削らない。**
>
> ### 系 SPLIT-NULL″
> **fake を検出しうる細分は entangled 屋根に限る。** $\mathrm{PSL}(2,8)$ 窓は共通商が完全に自明ゆえ**最も検出力の低い型**。

**⟹ 設計規則 v3 は、この 2 つを A/B 文脈に写しただけである**(以下 R1–R3 は追認、R4–R6 が増分):

| # | 規則 | 出所 |
|---|---|---|
| **R1** | 窓が**分裂屋根**(純商が直積)なら計器は盲 | 定理 SPLIT-NULL(**既存**) |
| **R2** | 検出しうるのは **entangled 屋根**のみ | 系 SPLIT-NULL″(**既存**) |
| **R3** | $\mathrm{PSL}(2,8)$ 側を深めるだけでは entangled にならない($P$ 単純) | 同上(**既存**) |
| **R4** | ★ 絡み $r=3$ は共通商 $Q_0$ の**交換子部分群**に住む ⟹ **可換な橋は盲** | §3(**増分**) |
| **R5** | ★ 便 127($G_l^{\rm ab}$ 純 2 群)が殺すのは**可換 $C_3$ 橋のみ**。**$S_3$ 橋は生存** | §4(**増分**) |
| **R6** | ★ 走行前に `entangled_roof_gate` を測る(§5)。分裂なら**発車しない** | Phase 2b の G2 手順の一般化 |

---

## 3. 増分 1 — 共通商の**同型型**の確定(R4)

`u9bit_apriori_v1.md` §53 は「$L_9\cap L_{S4}$ は**非可換でありうる**」と書いた。これを確定する。

> ### 命題 Q0(candidate・単系統)
> $E\cap F=\mathbf Q(\zeta_9,\sqrt[3]2)$(私の `d972_phase2_design_v1.md` §48 = $\langle2^3\rangle$ の立方体)であり
> $$Q_0:=\mathrm{Gal}\bigl(\mathbf Q(\zeta_9,\sqrt[3]2)/\mathbf Q\bigr)\cong C_3\times S_3,\qquad
> \boxed{\ \lvert Q_0\rvert=18,\ \ \textbf{非可換},\ \ [Q_0,Q_0]\cong C_3,\ \ Q_0^{\rm ab}\cong C_6=U.\ }$$

**証明**. $(\mathbf Z/9)^\times$ は Kummer 部分 $\mu_3$-捻りに**法 3 の円分指標** $(\mathbf Z/9)^\times\to(\mathbf Z/3)^\times$ で作用し、これは非自明。核は $C_3\subseteq C_6$ ⟹ $C_3\rtimes C_6\cong C_3\times S_3$。∎(機械: §7 T3 — 位数 18・非可換・$\lvert[Q_0,Q_0]\rvert=3$・$\lvert Q_0^{\rm ab}\rvert=6$)

> ### 系 R4(**可換橋は原理的に盲**)
> Goursat 共通商が $U=C_6$ を超える分は全部 $[Q_0,Q_0]\cong C_3$ に入る($Q_0^{\rm ab}=U$)。⟹ 橋 $Q$ が可換なら $[Q,Q]=1$ ゆえ $Q_0$ に到達できない。

**⟹ 3 連続の失敗の統一診断**(すべて R1/R2/R4 の帰結):

| # | 試み | 診断 |
|---|---|---|
| 1 | 2-群窓 $V=C_2^6$ | $E$ perfect ⟹ 分裂屋根(R1)。加えて素数も外れ |
| 2 | perfect 窓 | 同上(R1/R3) |
| 3 | 可換 $C_3$ 橋 | **R4**(必要な $C_3$ は $[Q_0,Q_0]$)+ 便 127($G_l^{\rm ab}$ 純 2 群) |

---

## 4. ★★ 増分 2 — **軸 1 は生きている**($G_l\twoheadrightarrow S_3$ の gating PASS)

便 127 は「$G_l^{\rm ab}\in\{4,16\}$ = 純 2 群 ⟹ **可換な** $C_3$ 商なし」を示した。しかし **$S_3^{\rm ab}=C_2$ は 2 群の商になれる**。⟹ 便 127 は $S_3$ 橋を排除しない。**実際に測った**:

$$\boxed{\ G_l\twoheadrightarrow S_3\ \textbf{は存在する}\ }$$

| $l$ | $\lvert G_l\rvert$ | ★ 全射 $G_l\to S_3$ の個数 |
|---:|---:|---:|
| 9 | 2,916 | **18** |
| 27 | 78,732 | **18** |
| 36 | 23,328 | **18** |

(判定法: $(x,a),(y,b)$ が $G_l\times S_3$ で生成する部分群が graph($\lvert H\rvert=\lvert G_l\rvert$)かつ $\langle a,b\rangle=S_3$。機械・§7)

> ### ⟹ 設計上の帰結(R5)
> **dihedral 因子を $K^{(l)}$ 族の外に出す必要はない。** 足りないのは **S4 側**である:
> $$\textbf{要求}:\ N'\subseteq N_{S4}\ \text{で}\ PB_3/N'\twoheadrightarrow\mathrm{PSL}(2,8)\ \textbf{かつ}\ PB_3/N'\twoheadrightarrow S_3.$$
> $P$ 単純ゆえ $S_3$ は $V=\ker(PB_3/N'\to P)$ から来ねばならない($V$ の $P$-余不変が $S_3$ を出す)⟹ **$PB_3/N'$ は非完全**。
> ⚠ **Phase 2b は $E$ を perfect に選んだ** ⟹ 構造的に不可能な選択だった(§3 の診断 2 と同じ)。

**最小候補**: $E=\mathrm{PSL}(2,8)\times S_3$($\lvert E\rvert=3024$)。両射影が全射 ⟹ $K=K^{(l)}\cap N_E$ の共通商は $S_3$(非自明)⟹ **entangled 屋根**⟹ **R1/R2 の除外を通過する初の候補**。
⚠ **前件(未確認・要測定)**: (i) $PB_3\twoheadrightarrow\mathrm{PSL}(2,8)\times S_3$ で $\theta,\tau$ 不変な核が存在するか (ii) その核が isolated か (iii) $G_l$ 側と $E$ 側の $S_3$ が**同じ** $PB_3$ 商か(違えば共通商は 1 に戻る)。**(iii) が本命の関門**。

> ★ **朗報**: `ribet_dig_campaign_v1_addendum_a.md` §3.3 の **命題 SPLIT-TWIN** は $E_p=C_p\rtimes_\psi(C_3\times S_3)$ を **$B_3$ 窓商として構成済**である(同節は「$S_3^{\rm ab}=C_2$ では足りず $Q^{\rm ab}=C_6$ が要る ⟹ $Q=C_3\times S_3$(位数 18)」という**本稿 §3 と同型の論法**を既に持つ)。**$C_3\times S_3$ が $B_3$ 窓商として実現可能であることは工房の既存資産**であり、前件 (i) はそこから輸入できる可能性が高い。

---

## 5. 事前ゲート `entangled_roof_gate`(R6・全走行の前件)

```
G-ENT-1 : 純商 PB_3/K の Goursat 共通商 Q を計算(直積なら Q=1)
G-ENT-2 : Q != 1 か                      … false なら SPLIT-NULL で盲(発車禁止)
G-ENT-3 : [Q,Q] に位数 3 の元があるか      … false なら R4 で盲(発車禁止)
G-ENT-4 : Q^ab が C_6 を商に持つか / Q が Q0 へ全射か  … 望ましい(必須ではない)
  ★ 2 つの因子の Q が「同じ PB_3 商」であることの確認を必ず含める(前件 iii)
  ★ false のときは測定を実行しない(偽測定ゼロ・Phase 2b の G2 手順の一般化)
```

### 推薦する次の一手(コスト順)

| # | 手 | コスト | 決定性 |
|---|---|---|---|
| **1** | ★ `ribet_dig` §3.3 の SPLIT-TWIN から **$C_3\times S_3$ の $B_3$ 窓商**を輸入し、前件 (i) を閉じる | 文書照合のみ | 高 |
| **2** | $PB_3\twoheadrightarrow S_3$ で $\theta,\tau$ 不変な核 $L$ を全列挙($\mathrm{Hom}(F_2,S_3)=36$ 通り)。$G_l$ 側の 18 個の $S_3$ 商と**同一の $PB_3$ 商か**を突合(前件 iii) | **数秒** | ★★ **高**(false なら軸 1 が本当に死ぬ) |
| **3** | 手 2 が PASS なら $E=\mathrm{PSL}(2,8)\times S_3$ の窓を構成し isolated 性を測る | 中 | — |
| **4** | $K=K^{(l)}\cap N_E$ で $\lvert\mathrm{Im}R_{K,M}\rvert$ を測る | 中 | **324 なら A 型確定** |

### ⛔ 推薦しない(既存規則で除外済)

$V$ の別既約表現 / 別次数の非分裂拡大 / $\mathrm{P\Gamma L}$ 系 / $\mathrm{PSL}(2,8)\times C_3$(**私の前便推薦・撤回**) — すべて分裂屋根(R1)か可換橋(R4)。

---

## 6. ★ 司令塔への上申(統治事項)

1. **3 連続の盲目性は数学のギャップではない。** 工房は 系 SPLIT-NULL″(裁定 374/388)で「$\mathrm{PSL}(2,8)$ 窓は最も検出力の低い型」と**既に書いていた**。Phase 2 / Phase 2b / $C_3$ 橋の 3 便は、**既存定理を索引できずに消費された**。
2. **私の責任が大きい**: 数学者レイヤーが PH2-VOID を「新規」と格付けし、それが裁定 1142/1144 の判断材料になった。§1 の訂正票を LEDGER に反映されたい。
3. **恒久対策の提案**: 委嘱時に司令塔から **「関連する既存定理名」を 1 行添える**(今回なら「SPLIT-NULL を見よ」)。索引は司令塔側にあるほうが安い。私の側の対策は §1.3。
4. ★ **朗報 1 件**: **軸 1 は生きている**($G_l\twoheadrightarrow S_3$ 実在・18 個/level)。次の一手は**数秒**で決着する(§5 手 2)。

---

## 7. 検算スクリプトと grep 領収書(★ 自分の新規ファイルを除外した実測値)

**スクリプト**: `scratchpad/ab_entangle_coord.py`(§3 の $Q_0$ 構造・$GT(M)$ 模型)/ inline($G_l\twoheadrightarrow S_3$ の gating)

| 主張 | grep(`| grep -v ab_instrument_redesign_v1.md` 付き) | ヒット | 判定 |
|---|---|---|---|
| PH2-VOID の概念 | `SPLIT-NULL` | **279** | ★ **既出**(撤回) |
| Goursat/subdirect による entanglement | `subdirect` / `Goursat` | **38 / 256** | ★ **既出**(E1 §5.6・便 75 F6.3・E1-GAP-2) |
| $\mathbf F_3^2$ の 4 直線 | `4 直線` / `crown` | 複数(裁定 1041/1050) | ★ **既出**(撤回) |
| $\mathbf Q(\zeta_9,\sqrt[3]2)$ | `2^{1/3}` / `立方根` | **6**(うち 1 は私の Phase 2 設計 §48) | ★ **既出**(自己再発見・撤回) |
| 共通商の非可換性 | `共通商.*非可換` | **1**(`u9bit_apriori_v1.md` §53「ありうる」) | △ **確定のみ増分** |
| $C_3\times S_3$(位数 18・$Q^{\rm ab}=C_6$) | `C_3 \times S_3` | **1**(`ribet_dig_campaign_v1_addendum_a.md` §3.3) | ★ **既出**(別文脈・輸入可能) |
| $\widehat{GT}_{\rm gen}\cong\varprojlim\mathrm{ML}$ | `Thm 5.2` | 複数(抽出ノート L126) | ★ **正典**(撤回) |
| fake = 有限証明書 1 個 | 抽出ノート L127/L137 | 既出 | ★ **正典**(定理 DUAL は誤り・撤回) |
| ★ **$G_l\twoheadrightarrow S_3$ の実在** | `G_l.*S_3` / `S_3 商` | **0** | ★ **新規**(§4) |
| ★ **便 127 が $S_3$ 橋を殺さないこと** | `S_3.*便 127` / `2 群.*S_3` | **0** | ★ **新規**(§4) |

**格付け**: §4 の gating = **機械・単系統**(Sol 未監査)。§3 命題 Q0 = **paper-proof candidate**(単系統)。§1 の訂正票 = **文書照合**。§2 は既存定理の再掲(**引用**)。**verified ではない。** u/c・封印 3 量・prereg 非接触。

⚠ **模型依存の申告**: `ideas_surg_boost_v1.md` §51 の $\mathbf F_3$ 線形代数化と crown census(裁定 1041/1050)が私の初稿 §1 を包含するので、**初稿 §1 は本稿から削除した**(versioned 規律: 初稿は git 履歴に残置)。
