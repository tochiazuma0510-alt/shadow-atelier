# 【K9-P1-RECON】P1 鎖(FAM-U-ASM)との同一対象判読 — **測定装置の相続は不可**

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5・後任)/ **委嘱**: 裁定 904(委嘱文の実体 = `docs/状態.md` 行 24)
**格**: candidate(紙・単系統・**Sol 未監査**)。⚠ **委嘱文は独立ファイルとして届いていない**(§0.1)。
**判読対象**: `docs/notes/fam_u_assembly_v1.md`(P1 鎖)/ `docs/notes/u9bit_spec_v1.md` §1.2 / R1 第一波 `r1_k9_bridge_v1.md`

> ### ★★ 判定(先に 3 行)
> | 提案された同一視 | 判定 |
> |---|---|
> | **(3)** U-11 の $\Theta_9\cong\mathrm{Aff}(\mathbf Z/9)\times C_2$ ↔ K9-COORD | ★ **同一**(しかも正典内在で再導出済 ⟹ U-11 の確認)。**型側の言明ゆえ無害** |
> | **(1)** 私の $a$ ↔ $u_9$ | ⚠ ★ **NAME-COLLIDE: 工房内に $u$ が二つある**。u9bit の $u_9$ とは**同一だが定義域が違う**($u_9$ は $d_9=9$ を暗黙前件にもつ)/ FAM-U の $u_n$ とは**別対象**(窓側) |
> | **(2)** $d_9$ ↔ $\operatorname{ord}([u_9^{-1}]_{18})$ | ✘ ★★ **別対象**。両者は FAM-U の矢印 **(b)+(c-n)** で隔てられ、**(c-n) は FAM-U 自身が「循環」と裁定済**(F96-1.6・Sol 承認)|
> $$\boxed{\ \Longrightarrow\ \textbf{P1 測定装置の相続は}\textbf{不可}\textbf{。相続すれば }\textbf{B116-1 の再犯}\ (\textbf{標的群型 → 実算術像の密輸})\ }$$

## §0.1 ⚠ 手続き上の申告

委嘱【K9-P1-RECON】は**独立ファイルとして `ops/express/` にも `docs/` にも存在しない**。実体は `docs/状態.md` 行 24 の 1 文と司令塔メッセージの要約のみ。本判読は**その 2 つを一次入力**として行った。⟹ **委嘱文に私の知らない条件が付いていた場合、本判読はその分だけ射程外**。

---

## §1 判読 (3) — U-11 の $\Theta_9$ 同型: **同一・確認**

| | U-11(ihnec 戦役) | K9-COORD(R1 第一波) |
|---|---|---|
| 主張 | $\Theta_9\cong\mathrm{Aff}(\mathbf Z/9)\times C_2$、位数 108 | 同左 |
| 出所 | ihnec 戦役(工房) | ★ **正典内在**: Prop 3.4 + **Prop 4.5 (4.15)** + CRT + **Thm 4.6 (4.23)** $\alpha<2$ 枝 |

$$\boxed{\ \textbf{同一対象・二系統で一致} \Longrightarrow\ \textbf{U-11 は正典から独立に確認された}\ }$$
⚠ ただし **これは (1) marked target の言明**(TYPE-IMAGE$^\rho$ の第 1 対象)であって、**(3) embedded image については何も言わない**。**B116-1 はまさにここを踏んだ** — 本判読でも型を跨がない。

---

## §2 判読 (1) — ★ 工房内に **$u$ が二つ**ある(NAME-COLLIDE)

| 記号 | 定義 | 型(TYPE-IMAGE$^\rho$) | 定義域 |
|---|---|---|---|
| **私の $a$**(K9-KUMMER) | translation コサイクル $t\in Z^1(G_\mathbf Q,\mu_9)$ の Kummer 類・$L_{9,\mathrm{Aff}}=\mathbf Q(\zeta_9,\sqrt[9]{a})$ | ★ **(4) kernel field / (3) image 側** | ★ **無条件**($d_9\in\{1,3,9\}$ のどれでも定義される) |
| **u9bit の $u_9$**(`u9bit_spec_v1.md` §1.2) | 「$L_9$ に含まれる**次数 9** Kummer 層の生成データ」 | 同上(算術側) | ⚠ ★ 原文の括弧「**$u$ が 9 乗類として自明でなく、かつ Kummer 層が完全に立つとき**」= **$d_9=9$ を暗黙前件にもつ** |
| **FAM-U の $u_n$**(`fam_u_assembly_v1.md`) | $\operatorname{ord}([u_n]_{2n})=n$ の $u_n$。**B-5$_{\rm loc}$**: 「局所 Kummer torsor 類 $=[u^{-1}]_M$」「**層 2 の数値を『窓の torsor 類』として読む**」 | ★★ **(1) marked target 側(窓・模型)** | 枠組み(TB1–TB4・BFC)相対 |

> ### ★ 判定
> - **$a$ vs u9bit の $u_9$**: **同一対象だが $u_9$ の定義が $d_9=9$ を前件にもつ** ⟹ $$\boxed{\ u_9\ \textbf{を使って }d_9\ \textbf{を測ることは}\textbf{定義上の循環}\ }$$ **$a$ が無条件版**であり、以後 $d_9$ 関連では **$a$ を正本**とすべき。
> - **$a$ vs FAM-U の $u_n$**: ★ **別対象**(算術像側 vs 窓側)。同名だが source/target/基礎体が違う ⟹ **NAME-COLLIDE 規約の 6 点照合が必須**。

---

## §3 判読 (2) — ★★ $d_9$ と $\operatorname{ord}([u_9]_{18})$ は**循環の矢印で隔てられている**

### 3.1 FAM-U 自身の距離の図(**§V.5.1 逐語**)

$$\underbrace{\operatorname{ord}([u_n]_{2n})=n}_{\textbf{(a) 本組立}}\xrightarrow[\text{BFC/B-5/TB 相対}]{\textbf{(b)}}\underbrace{\text{窓の局所 Kummer torsor 類}}_{\text{層 3}}\xrightarrow[\substack{\textbf{(c-2) FAITH-free・橋相対}\\ \textbf{(c-n) FAITH 条件付き}}]{}\operatorname{ord}(a_n)=n\xrightarrow[\text{未証明}]{\textbf{(d)}}\mathrm{Ih}_{K^{(n)}}\ \text{全射}$$

**(c-n) の格(逐語)**:
> **$n$-part の輸送**: FAITH 下で $\operatorname{ord}([u_n]_n)=\lvert\mathrm{Ih}_N(G_F)\rvert$(B-LIMIT-1)。★ **さらに (FAITH) 条件付き ⟹ 循環**(経路 B で $n$-part を出すことは Ihara 全射性を示すことと同値)

**橋 B-1(逐語)**:
> ★ **$[u_n]$ から $\mathrm{Ih}$ の像へ渡る唯一の橋**。ここが未検分である限り、$\operatorname{ord}([u_n]_{2n})=n$ は $\operatorname{ord}(a_n)=n$ を**含意しない**

### 3.2 私の $d_9$ はこの図のどこにいるか

$d_9=\lvert A_9\cap\mathbf Z/9\rvert$ = **算術像 $\mathrm{Ih}_{K^{(9)}}(G_\mathbf Q)$ の translation 部分の位数** ⟹ **図の右端側**($n$-part = (c-n) の標的そのもの)。
一方 $\operatorname{ord}([u_9]_{18})$ は **左端 (a)**。

$$\boxed{\ \Longrightarrow\ \textbf{提案された同一視 }d_9\leftrightarrow\operatorname{ord}([u_9^{-1}]_{18})\ \textbf{は矢印 (b)(c-n) を}\textbf{跨ぐ}\ }$$
FAM-U §V.5.1 は明示的に「**第 2 の矢印(枠組み)と第 3 の矢印(未証明)を跨いで SURJ を語ってはならない**」と書いている。⟹ **相続は禁止事項に直接抵触**。

### 3.3 ★★ 正の副産物 — 私の K9-CYC(b) は **(c-n) の循環を FAITH 抜きで確定させる**

FAM-U (c-n): 「**FAITH 下で** $n$-part を出すことは Ihara 全射性を示すことと**同値**」= **条件付きの循環宣言**。
私の **K9-CYC(b)**($\chi$ 全射 + Prop 4.5 + (1.13) のみ使用): $$\boxed{\ d_9=9\iff\mathrm{Ih}_{K^{(9)}}\ \textbf{全射}\qquad(\textbf{無条件・}n=9)\ }$$

> ★ **⟹ 循環は FAITH の副作用ではなく構造的である**。(c-n) の格を「FAITH 条件付きの循環」から **「$n=9$ では無条件の同値」**へ**強めた**。
> ⟹ **経路 B で $d_9$ を出そうとする試みは、$n=9$ において確定的に閉じている**(条件を外しても抜け道はない)。これは**負の情報だが一級**である。

### 3.4 【RECON-GAP-1】— $a_n$ と私の $a$ の同一性は**未判読**

FAM-U の矢印 (d) は「$\operatorname{ord}(a_n)=n\Rightarrow$ SURJ」(**未証明**)。私の K9-CYC(b) は $n=9$ で **双方向の同値**を与える。
⟹ ★ **もし FAM-U の $a_n$ が私の $a$ と同一なら、矢印 (d) は $n=9$ で無条件に閉じる**(新規結果)。
⚠ **しかし $a_n$ の定義を `fam_u_assembly_v1.md` / `fam_u_v1.md` 内で特定できなかった**(grep 不発)⟹ **UNKNOWN**。**同一と仮定して (d) を閉じたと言ってはならない。** 判読には `fam_u_v1.md` 本体と M2 三部作が要る。

---

## §4 帰結 — 裁定 907 の「二枝」は**一枝に collapse する**

司令塔は「RECON 未了の場合 / 肯定の場合」の二枝を持たせよと指示した。**判読の結果 RECON は否定**である。

$$\boxed{\ \textbf{枝「RECON 肯定 ⟹ P1 測定装置を相続」は}\textbf{閉じた}\ \Longrightarrow\ d_9\ge3\ \textbf{見積りは}\textbf{単枝}\ }$$

⚠ **残る唯一の分岐**は【RECON-GAP-1】($a_n\overset?=a$)だが、これは**測定装置の相続ではなく矢印 (d) の帰属**の話であり、$d_9$ の**下界を出す力はもたない**(同一でも (d) は $d_9$ の値を与えず、同値を与えるだけ)。⟹ **見積りには影響しない**。

---

## §5 帰属・依存申告

- **P1 鎖の距離の図・(c-n) の循環宣言・橋 B-1 の未検分性** = `fam_u_assembly_v1.md`(便 95/96・Sol F96-1.6)。
- **委嘱** = 司令塔(裁定 904)。⚠ **委嘱文の実体は `docs/状態.md` 行 24 のみ**(§0.1)。
- **本ノートの新規部分**: ① **$u$ の三重 NAME-COLLIDE の摘出**(私の $a$ / u9bit の $u_9$ / FAM-U の $u_n$)② **u9bit の $u_9$ が $d_9=9$ を暗黙前件にもつ**ことの摘出(⟹ $u_9$ で $d_9$ を測るのは定義上の循環)③ **$d_9$ が図の右端に居ることの同定**と相続不可の結論 ④ ★ **K9-CYC(b) が (c-n) の循環を FAITH 抜きで確定させる**という格上げ ⑤ **【RECON-GAP-1】**の起票。
- **未実施**: `fam_u_v1.md` 本体・M2 三部作の精読(⟹ $a_n$ の定義未特定)。**Sol 未監査**。⟹ **verified ではない**。
