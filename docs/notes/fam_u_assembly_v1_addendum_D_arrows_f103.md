# FAM-U 総組立【v2 追記 D】— **距離図の矢印 (d) を (d1)/(d2) へ分割**(便 103 F103-5 の適用)

**状態札: `additive erratum(適用版)/ candidate / 主言明・domain・最短鎖・格は動かない / Lean 検証ではない`**

> ## 適用の申告
> - **適用対象**: `docs/notes/fam_u_assembly_v1.md`(SHA-256 `fe3abe0a98e98589112bf8fa067b941f9e745c228b1726a8d0ad25bed3b67114`)の **§V.5(距離の図 — v1 §7 を置換した節)**。
> - ★ **CV-10 additive erratum 方式**: host の **v1 / v2 / 追記 A / 追記 B は 1 バイトも書き換えない**。**追記 C(適用版)**(`fam_u_assembly_v1_addendum_C_applied_f103.md`)にも触れない。抵触する箇所は**本追記 D が優先**する。
> - ★ **effective source = 便 103 `F103-5` PASS**(`sol/sol_reply_103_math30.md` §5・SHA-256 `cc516a0ec69f6df39f82e0cdca0d8899f10bdba90ea6e79fdc9d8956e97b5d06`)。
> - **上流の起草**: `docs/notes/s3_family_draft_v1_addendum_a_f102.md`(SHA-256 `0e3d292213f2a7411519408c415a31dea305cf928ec7a1a921a3d16195734da5`)§2–§3。本追記 D はその **§3(距離図の書き換え案)を適用形に固めたもの**である。
> - **本追記 D は新しい数学を主張しない。** 変えるのは**矢印の分割・格の帰属・依存の discharge の記帳**だけである。
> - 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05

---

## D.0 判定(先に 5 行)

| # | 問い | 判定 |
|---|---|---|
| **①** | 何を置換するか | ★ **§V.5.1 の矢印表の (d) 行**と **§V.5 の図**。**(a)(b)(c-2)(c-n) の 4 行は不変** |
| **②** | 分割形は | ★★ **(d1)** $\mathrm{ord}(a_n)=n\Rightarrow\mathrm{Ih}_{K^{(n)}}(G_{F_n})=\mathfrak F_0$ /**(d2)** 像形 $\Rightarrow$ SURJ。加えて旧 (d) 後段を **(e)**(E1-3)として独立させる |
| **③** | (d1) の格 | ★ **`theorem-framework-relative [TB: canonical-source-pinned/v2]`**(**F103-4 の (5′) 条件付き PASS を継承**)+ **【MATCH-one】が満たされない限り UNKNOWN に止まる**。⚠ **無条件定理としない**(F103-5 逐語) |
| **④** | (d2) の格 | ★ **既在補題で閉**(補題 SURJ-Split (e) 族適用・裁定 227)。**窓非依存・枠組み層なし** |
| **⑤** | (6′) の扱い | ★ **前件に書かず、依存表で discharge を明記**(F103-5 の指示)— **単元 $\alpha$ に対する定理 SIXP-fam が供給**。§D.2.2 |

---

## D.1 何が誤りだったか(**旧 §V.5.1 (d) 行の撤回**)

§V.5.1 は

> | **(d)** | $\mathrm{ord}(a_n)=n$ ⟹ SURJ ⟹ odd Conj 5.1 | ★ **未証明**((S3) 族版)+ **E1-3** |

と、**二段(場合により三段)を一つの矢印に畳んでいた**(F103-5 / F102-5.3)。畳んだことの実害は 2 つ:

1. **格の混在** — 前半は枠組み相対、後半は枠組み非依存であるのに、1 本の「未証明」で塗られていた。
2. **未知の所在が見えない** — 前半に残る未知は **(5′)** と **【MATCH-one】** の 2 点だけであり、後半には未知が無い。畳むとこの局在が消える。

⚠ **同時に、上流の起草(追補 A の前身)が「(d) は丸ごと既在補題で閉じている」と書いたのも過剰であった**(F102-5.3 で不承認)。**正しいのは「二矢印に分け、(d2) だけが既在で閉じる」である。**

---

## D.2 ★ §V.5.1 矢印表の置換(**(d) 行 → (d1)/(d2)/(e) の 3 行**)

| 矢印 | 内容 | 格・条件 | pin |
|---|---|---|---|
| (a) | 裸の class/order: $\mathrm{ord}([u_n]_{2n})=n$ | 最短鎖 (S0)–(S5)+(S\*)。M2(theorem)+ 初等 | **不変**(§V.2.2・F96-1.3) |
| (b) | B-5 による torsor 解釈 | BFC/B-5/TB 相対(層 3) | **不変**(W96-1.1 層 3;供給は**追記 C** §C.1) |
| (c-2) | 2-part の輸送(B-LIMIT-0/0a) | FAITH-free。ただし BFC/B-4c/B-5/TB の橋に相対的 | **不変**(F96-1.6) |
| (c-n) | $n$-part の輸送(B-LIMIT-1) | FAITH 条件付き ⟹ **循環** | **不変**(F96-1.6)。⚠ **$n$-part の橋としては使えない** |
| ★ **(d1)** | $\mathrm{ord}(a_n)=n\ \Longrightarrow\ \mathrm{Ih}_{K^{(n)}}(G_{F_n})=\mathfrak F_0$ | ★ **`theorem-framework-relative [TB: canonical-source-pinned/v2]`**。経路 = $R^{\rm cyc}_{\rm formal}$ 証明 2 + **【MATCH-one】** + **同一 matched window 上の $(5')@\alpha$**。**依存が満たされなければ UNKNOWN に止める** | **F103-5**(PASS)・**F103-4**((5′) 条件付き PASS)・W3-13 / 裁定 24・`s3_family_completion_v1.md` §11–§13 |
| ★ **(d2)** | $\mathrm{Ih}_{K^{(n)}}(G_{F_n})=\mathfrak F_0\ \Longrightarrow\ \mathrm{Ih}_{K^{(n)}}$ 全射 | ★ **既在補題で閉**(窓非依存・**枠組み層なし**) | **補題 SURJ-Split (e)**(`surj_d4_t1_v1.md` §2.1)・**F86-4.1.1**・裁定 **227**;`s3_family_draft_v1.md` §3.2 定理 SURJ-fam;**F103-5** |
| ★ **(e)** | 全奇 $n$ で SURJ $\Rightarrow$ odd Conj 5.1 | **紙上相互監査 PASS** | **定理 E1-3**・裁定 **111**(旧 (d) の後段を独立させた) |

### D.2.1 ★ (d1) の格の内訳(**無条件定理としない** — F103-5 逐語)

> F103-5: 「**ただし `(d1)` の格は §4 の TB 条件を継承し、無条件定理とはしない。**」

| 成分 | 状態(便 103 時点) |
|---|---|
| **$R^{\rm cyc}_{\rm formal}$ 証明 2** | **paper-proof**(W3-13・裁定 24)。$\lvert\mathrm{Ih}_N(G_K)\rvert=\mathrm{ord}([u^{-1}]_M)$ |
| **(3)(6′)** | ★ **discharge 済**(§D.2.2)— 単元 $\alpha$ で **SIXP-fam / Λ-REG**(F102-5.1 PASS) |
| **(5′)** | ★ **`theorem-framework-relative [TB: canonical-source-pinned/v2]` として条件付き PASS**(**F103-4**)。条件 = 2 件の文言修理(RD6′ の分離・不要な Hensel/valuation 説明の削除)。⚠ **`canonical-source-relative` / `verified` とは書かない** |
| **【MATCH-one】** | ⚠ **開**。$\exists\alpha\in(\mathbf Z/n)^\times$ で「$(5')@\alpha$」と「手元の類 $=[u_{n,\alpha}]_{2n}$」が**同一の $\alpha$**。**満たされなければ (d1) は UNKNOWN に止まる**(F103-5 逐語) |

$$\boxed{\ \textbf{(d1) は「無条件」でも「UNKNOWN 一色」でもない — }\texttt{framework-relative}\ \textbf{条件つきで、【MATCH-one】が gate である。}\ }$$

### D.2.2 ★ (6′) の discharge の明記(**F103-5 の指示の履行**)

> F103-5: 「`(6′)` は前件に明記されていないが、unit alpha に対する SIXP-fam が供給するので、**依存表にその discharge を明記すればよい**。」

| $R^{\rm cyc}_{\rm formal}$ の前件 | (d1) での扱い | discharge 元 |
|---|---|---|
| **(0)** isolated / $\mathrm{Ih}$ の typing | 前件(A1) | 正典 Thm 4.3・Remark 1.4 |
| **(1)** 完全列 + $\widetilde\chi\circ\mathrm{Ih}=\chi_{4n}$ | 前件(A2+A3) | (W2)-fam(裁定 120)/ W2-arith Route A(裁定 122) |
| **(2)** $\mathfrak F_0\cong C_e$、$e\mid M$ | 前件(A2) | (W2)-fam($e=n\mid2n$) |
| **(3)** $\mathrm{ord}(X)=\lvert\Lambda\rvert=M$・$\langle X\rangle$ 単純推移 | ★ **discharge**(前件に書かない) | **補題 Λ-REG**(`s3_family_completion_v1.md` §3)— ODD-H (1.3)+補題 C(2)。**全 $\alpha\ne0$** |
| **(5′)** 比較出力 | ★ **前件**(【MATCH-one】の $\alpha$ で) | **F103-4**(条件付き PASS・上表) |
| **(6′)** (R6-act):$\rho_0$ 忠実 + $\rho_0(\mathfrak F_0)=\tau(\mu_M[e])$ | ★ **discharge**(前件に書かない) | **定理 SIXP-fam**(同 §5)— **F102-5.1 PASS**。**単元 $\alpha$** で紙の証明 |

⚠ **射程遮断(F102-5.1 逐語)**: 「**$\alpha\ne0$ は SIXP の作用論的範囲であって、非単元を ASM の正例へ戻す根拠ではない**」。⟹ **(d1) の量化は $\alpha\in(\mathbf Z/n)^\times$(単元)に限る**。追記 C §C.4 の【ASM-α】と同じ遮断が掛かる。

---

## D.3 ★ §V.5 の図の置換

$$
\underbrace{\operatorname{ord}([u_n]_{2n})=n}_{\textbf{(a) 本組立}}
\ \xrightarrow[\text{BFC/B-5/TB 相対}]{\textbf{(b) torsor 解釈}}\
\underbrace{\text{窓の局所 Kummer torsor 類}}_{\text{層 3}}
\ \xrightarrow[\substack{\textbf{(c-2) FAITH-free・橋相対}\\ \textbf{(c-n) FAITH 条件付き = 循環}}]{}\
\operatorname{ord}(a_n)=n
$$
$$
\operatorname{ord}(a_n)=n
\ \xrightarrow[\substack{R^{\rm cyc}\ +\ \textbf{MATCH-one}\ +\ (5')@\alpha\\ \texttt{framework-relative}\ \textbf{[TB: canonical-source-pinned/v2]}}]{\textbf{(d1)}}\
\operatorname{Ih}_{K^{(n)}}(G_{F_n})=\mathfrak F_0
\ \xrightarrow[\substack{\text{補題 SURJ-Split (e) の族適用}\\ \textbf{既在で閉・窓非依存・枠組み層なし}}]{\textbf{(d2)}}\
\mathrm{Ih}_{K^{(n)}}\ \text{全射}
\ \xrightarrow[\textbf{(e) E1-3}]{\text{全奇 }n}\
\text{odd Conj 5.1}
$$

---

## D.4 ★ §V.5.2(依存監査と禁止事項)への追加

**§V.5.2 の既存 4 項はすべて維持**(B-LIMIT-2′ の bounded 性・F96-1.6 の結論再投入禁止・`UNKNOWN BL-2`・矢印跨ぎ禁止)。本追記が**足すのは 3 項**である。

> **5.** ★ **「(d) が閉じた」という要約は禁止。** (d) は 2 本ある。**閉じているのは (d2) だけ**であり、(d1) は `framework-relative` 条件つき+**【MATCH-one】が gate** である。
> **6.** ★ **(d2) が既在補題で閉じていることを、(d1) や始点ノードの格の軽減に流用してはならない。** 始点「**全奇 $n$ で $\mathrm{ord}(a_n)=n$**」は **【E1-GAP-5】【E1-GAP-6】の格を保つ**(F102-5.3 末)。下界層の入力は $n=3$・$n=9$ の 2 例のままである。
> **7.** ★ **(c-n) を (d1) の代用にしてはならない。** (c-n) は FAITH 条件付きで**循環**(F96-1.6)。$\mathrm{ord}(a_n)=n$ から像形へ渡る経路は **(d1)(= $R^{\rm cyc}$ 経由)のみ**である。

---

## D.5 動かないもの(**明示**)

| # | 不変 |
|---|---|
| 1 | **§1 の主言明(組立文)** — 逐語形も動かさない |
| 2 | **domain**(追記 B = 全奇数 $n\ge3$) |
| 3 | **最短鎖 (S0)–(S5)+(S\*)** と追記 A の DAG |
| 4 | **P97-1.1(裁定 366)の 4 札**と campaign status `candidate`(唯一の理由も不変) |
| 5 | **§V.5.1 の (a)(b)(c-2)(c-n) の 4 行** |
| 6 | **追記 C(適用版)の層 3 表** — 本追記 D は層 4 側の矢印にしか触れない |
| 7 | **$K^{(5)}$**:本追記は $n=5$ の値・窓データ・機械計算に触れない |

---

## D.6 【v2 正位置ポインタ】への追加行(**司令塔が挿入する 1 行・文面**)

> ★★★★ **さらに【v2 追記 D】を末尾に追加**(v1/v2/追記 A/追記 B/追記 C いずれも不改変・effective source = `docs/notes/fam_u_assembly_v1_addendum_D_arrows_f103.md`・**便 103 F103-5 PASS**)。**§V.5.1 の矢印 (d) 行は §D.2 の (d1)/(d2)/(e) 3 行が置換**し、**§V.5 の図は §D.3 が置換**、**§V.5.2 に §D.4 の禁止 3 項が加わる**。**旧 (d) 行と旧図を単独で引用しないこと。**★ **主言明・domain・最短鎖・格は 1 つも動かない**(§D.5)。

---

## D.7 FINDING(本追記の分)

| # | 格 | 内容 |
|---|---|---|
| **ASM-D1** | ★★ **矢印の分割(本追記の主成果)** | 旧 (d) は二段(+E1-3)を畳んでいた。**(d1)**(framework-relative・MATCH-one が gate)と **(d2)**(既在補題で閉・窓非依存)へ分割し、**(e)**(E1-3)を独立させた |
| **ASM-D2** | ★ **未知の局在** | (d1) に残るのは **(5′)**(F103-4 で `theorem-framework-relative [TB: canonical-source-pinned/v2]` 条件付き PASS)と **【MATCH-one】**(開)の 2 点のみ。**(3)(6′) は Λ-REG / SIXP-fam で discharge 済**(§D.2.2) |
| **ASM-D3** | ★ **格の非混同** | (d2) が閉じたことは (d1) の格にも始点ノード(【E1-GAP-5/6】)の格にも**波及しない**。§D.4 の禁止 5–7 で明文化 |
| **ASM-D4** | ⚠ **量化の遮断** | (d1) の $\alpha$ 量化は**単元 $(\mathbf Z/n)^\times$ に限る**(F102-5.1 の射程遮断)。追記 C §C.4【ASM-α】と同じ壁 |

---

## D.8 本追記が主張しないこと

1. 「矢印 (d) が閉じた」— **主張しない**((d2) のみ)。
2. 「$\mathrm{Ih}_{K^{(n)}}$ が全射」— **主張しない**(始点が未供給)。
3. 「(S3) の族版が得られた」— **主張しない**(【E1-GAP-5】は不変)。
4. 「(5′) が無条件」「枠組み仮定が消えた」— **主張しない**(`canonical-source-relative` / `verified` とは書かない — F103-4 逐語)。
5. `cross-checked` / `verified` — **付さない**。
