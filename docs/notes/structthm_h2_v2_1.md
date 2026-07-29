# 構造定理 v2.1 — 局所修理 2 件(裁定 227・P86-1)

作成: 数学者(Opus 5)・2026-07-30
**本ノートは `docs/notes/structthm_h2_v2.md` の局所修理であり、v2 を上書きしない。**
**v2.1 が正本**(v2 の §2 本体・§3 H2′・§4〜§9 は**変更なし・凍結扱い**。本文書で触れるのは系 STR-1.4c と tail-8 帰結の 2 箇所のみ)。
入力: Sol 便 86(`sol/sol_reply_86_math13.md` §F86-1.1・P86-1)。

---

## 0. 判定と修理範囲

> **STR-1 v2 = 条件付き PASS**(F86-1.1)。TFAE の証明核(1〜7)は Sol が再導出し追認。(a) → (a$_{\rm int}$) の retype も**証明と一致**と確認された。
> ただし **v2 をそのまま定理 freeze することは認めない** — 局所修理 2 件が先。

| # | v2 の記述 | 判定 | v2.1 での処置 |
|---|---|---|---|
| **R-1** | 系 STR-1.4c: $\mathrm{dl}(A\rtimes Q)\le2$ から $\mathrm{dl}(G)=\max(\mathrm{dl}(S),2)$ へ飛んでいる | **修理** | 必要なのは $\mathrm{dl}(A\rtimes Q)=\mathbf 2$(等号)。**基本形を STR-1(4) とし、非可換 full-Hol($N>2$)のときだけ 2 に特殊化**する形へ(§1) |
| **R-2** | 尾部帰結「$\mathrm{dl}(G)=3\iff t\ge8$」 | **修理**($t\ge16$ で偽) | $\mathrm{dl}(\mathrm{Syl}_2(S_t))=\lfloor\log_2t\rfloor$ に基づき **$\mathrm{dl}(G)\ge3\iff t\ge8$**、**$\mathrm{dl}(G)=3\iff 8\le t\le15$** へ(§2) |

**この 2 件は TFAE を壊さない**(Sol 明記)。**R-1・R-2 はいずれも私(起草者)の責**である。

---

## 1. 【R-1】系 STR-1.4c の修理

### 1.1 何が誤っていたか

v2 の系は前件を「$A\rtimes Q\cong\mathrm{Hol}(C_N)$($A=C_N$ 巡回、$Q\le\mathrm{Aut}(C_N)$)」と書き、$\mathrm{Hol}(C_N)'\le C_N$ から $\mathrm{dl}(A\rtimes Q)\le2$ を出して $\max(\mathrm{dl}(S),2)$ に飛んでいた。**$\le2$ では足りず $=2$ が要る。**

**反例(Sol)**: $\mathrm{Hol}(C_2)=C_2$ は $\mathrm{dl}=1$。
**もう一つの穴**: 括弧内の「$Q\le\mathrm{Aut}(C_N)$」だけでは**非自明作用が保証されない**($Q=1$ なら $A\rtimes Q=C_N$ でアーベル、$\mathrm{dl}=1$)。

### 1.2 修理後の形(基本形 + 特殊化)

> **基本形(= STR-1(4)・変更なし)**: (a$_{\rm int}$) の下で
> $$\mathrm{Syl}_2(G)\cong S\times\mathrm{Syl}_2(Q),\qquad \mathrm{dl}(G)=\max\bigl(\mathrm{dl}(S),\ \mathrm{dl}(A\rtimes Q)\bigr).$$
> **これを常に基本形として書き、$2$ への特殊化は別立ての系にする。**

> ### 系 STR-1.4c(v2.1・修理版)
> (a$_{\rm int}$) に加えて **$\mathrm{dl}(A\rtimes Q)=2$** が成り立つとき、
> $$\mathrm{dl}(G)=\max\bigl(\mathrm{dl}(S),\,2\bigr).$$
> **前件 $\mathrm{dl}(A\rtimes Q)=2$ の十分条件(いずれも同値な言い換え)**:
> - **(c1)** $Q$ がアーベルで、かつ **$Q$ の $A$ 上の作用が非自明**($[A,Q]\ne1$)。
> - **(c2)** $A\rtimes Q\cong\mathrm{Hol}(C_N)$(**full** holomorph)かつ **$N>2$**。
>
> **証明**: (c1) $Q$ アーベルより $(A\rtimes Q)'\le A$、$A$ アーベルゆえ $(A\rtimes Q)''=1$、よって $\mathrm{dl}\le2$。等号は $A\rtimes Q$ が非可換であること、すなわち $[A,Q]\ne1$ と同値。
> (c2) $\mathrm{Hol}(C_N)=C_N\rtimes\mathrm{Aut}(C_N)$ で $\mathrm{Aut}(C_N)$ はアーベル、かつ定義から $A$ 上**忠実**に作用する。$N>2$ なら $\mathrm{Aut}(C_N)\ne1$ ゆえ作用は非自明で (c1) を満たす。$N\le2$ では $\mathrm{Aut}(C_N)=1$ で $\mathrm{Hol}(C_N)=C_N$、$\mathrm{dl}\le1$。$\square$

### 1.3 三窓への適用(値は不変)

| 窓 | $N$ | $A\rtimes Q$ | (c2) の $N>2$ | $\mathrm{dl}(A\rtimes Q)$ | $\mathrm{dl}(S)$ | $\mathrm{dl}(G)$ |
|---|---|---|---|---|---|---|
| W-D-A16-11a | 11 | $\mathrm{Hol}(\mathbb Z/11)$ | ✔ | 2 | 2($D_8$) | **2** |
| W-D-A18-13a | 13 | $\mathrm{Hol}(\mathbb Z/13)$ | ✔ | 2 | 2 | **2** |
| W-D-A20-15a | 15 | $\mathrm{Hol}(\mathbb Z/15)$ | ✔ | 2 | 2 | **2** |

実測 `derived_length_G = 2`(三窓)と一致。**修理は三窓の適用値を反転させない**(Sol も同旨: 「三つの実窓では $N=11,13,15$ かつ full Hol が非可換なので適用値は正しい」)。

> **⚠ 再利用時の注意(新設)**: 梯子の $t=1$ 窓のように $S=1$ の窓では $\mathrm{dl}(G)=\mathrm{dl}(A\rtimes Q)$ となり、**$S$ 側からは何も出ない**。また $Q$ が非アーベルな窓では (c1) が使えず、$\mathrm{dl}(A\rtimes Q)$ を**独立に測る**必要がある(基本形へ戻る)。

---

## 2. 【R-2】tail-8 帰結の修理

### 2.1 $\mathrm{dl}(\mathrm{Syl}_2(S_t))$ の閉じた形

> **補題**: $\mathrm{dl}(\mathrm{Syl}_2(S_t))=\lfloor\log_2 t\rfloor$($t\ge1$;$t=1$ で $0$)。
> **証明**: $t=\sum_i 2^{a_i}$(二進展開)に対し $\mathrm{Syl}_2(S_t)\cong\prod_i\mathrm{Syl}_2(S_{2^{a_i}})$、かつ $\mathrm{Syl}_2(S_{2^a})\cong C_2\wr\cdots\wr C_2$($a$ 重)で $\mathrm{dl}=a$。直積の導来長は $\max$ ゆえ $\max_i a_i=\lfloor\log_2t\rfloor$。$\square$

| $t$ | 1 | 2–3 | 4–7 | **8–15** | 16–31 |
|---|---|---|---|---|---|
| $\mathrm{Syl}_2(S_t)$ | $1$ | $C_2$ | $D_8$ / $D_8\times C_2$ | $C_2\wr C_2\wr C_2$ 型 | — |
| $\mathrm{dl}(S)=\lfloor\log_2t\rfloor$ | 0 | 1 | 2 | **3** | 4 |
| $\mathrm{dl}(G)=\max(\mathrm{dl}(S),2)$ | 2 | 2 | 2 | **3** | **4** |

(最下行は §1 の前件 $\mathrm{dl}(A\rtimes Q)=2$ の下での値。)

### 2.2 修理後の主張

> **v2 の誤り**: 「$\mathrm{dl}(G)=3\iff t\ge8$」は **$t\ge16$ で偽**($\mathrm{dl}(S)=4$ 以上になるため)。
>
> **修理後(正しい形)**: $\mathrm{dl}(A\rtimes Q)=2$ の下で
> $$\boxed{\ \mathrm{dl}(G)\ge3\ \iff\ t\ge8\ }\qquad\text{かつ}\qquad\boxed{\ \mathrm{dl}(G)=3\ \iff\ 8\le t\le15\ }$$
> $t\ge16$ では $\mathrm{dl}(G)=\lfloor\log_2t\rfloor\ge4$。

### 2.3 尾部 8 プログラムへの影響(読みの更新)

- **プログラムの標的は無傷**。KERNEL-DL3 経路が要求するのは「**metabelian を破る**」= $\mathrm{dl}\ge3$ であり、修理後の**左の boxed がまさにその形**。$t\ge8$ が閾値であることは変わらない。
- **裁定 206 の「dl 跳躍点 $t=8$」の読みを精密化**: 跳躍は 1 回ではなく、$\lfloor\log_2t\rfloor$ の**各 2 冪ごと**に起きる($t=2,4,8,16,\dots$)。$t=8$ は「**$\ge3$ に入る最初の点**」であって「$=3$ になる点」ではない。$=3$ は $8\le t\le15$ という**帯**である。
- **証明書への含意**: dl の観測値を報告するとき、$t\ge16$ の窓では「$\mathrm{dl}=3$」を期待値として凍結してはならない。**期待値は $\max(\lfloor\log_2t\rfloor,2)$** と書く。
- **v2 §2.3 の警告は維持**: $A\rtimes Q$ が Hol 型でない窓では $\mathrm{dl}(A\rtimes Q)$ が独立に 3 以上になりうる($D_8\times S_4$ 型の汚染)ので、**dl-3 の観測を自動的に「$S$ 由来」と読んではならない**。§1 の前件($\mathrm{dl}(A\rtimes Q)=2$)を測ってから読むこと。

---

## 3. 変更していないもの(凍結扱い)

以下は `docs/notes/structthm_h2_v2.md` のまま**一字も変えていない**。再監査は本文書の §1・§2 だけを見ればよい。

- §2 定理 STR-1 v2 の (H1)(H2)(H3)・(1)(2)・TFAE (a$_{\rm int}$)(b)(c)(d)・(5)(6) と、その証明(F86-1.1 の 1〜7 で Sol 追認済)
- §2.1 (a$_{\rm int}$) と (a$_{\rm abs}$) の区別
- §3 H2′ パッケージ(H2′-exist / H2′-uniq / Cyclic criterion・「$Q\ne1\Rightarrow A^Q=0$」は偽・非アーベル $A$ への移植不可)— **F86-1.2 で全て PASS**
- §4 $H^2$ の計算と判定 STR-3(必然ではない)
- §5 実測 STR-2(三窓の $D_8\times\mathrm{Hol}$・GAP 単系統)
- §6 裁定 205 の推論の訂正($D_8\circ C_4$ 反例)
- §7 残るギャップ・§8 定理 candidate・§9 出所

**唯一の差し替え**: §2 の (4) は「基本形」として維持し、**$\max(\mathrm{dl}(S),2)$ への特殊化は §1 の系 STR-1.4c(v2.1)を参照**すること。v2 §2.3 の系 STR-1.4c 本文は本文書 §1.2 で置き換わる。

---

## 4. 出所

- 修理指示: `sol/sol_reply_86_math13.md` §F86-1.1(本体・残る局所修理 1/2)・P86-1 / 裁定 227
- 修理対象: `docs/notes/structthm_h2_v2.md` §2(4)・§2.3
- 実測値(§1.3): `search/certs/a{16,18,20}_kernel_structure_20260729.json`(`derived_length_G = 2`)・`docs/notes/structthm_h2_v2.md` §5
- 格付け: §1.2 の系(c1)(c2)と §2.1 の補題は**証明済**(初等・自己完結)。§1.3 の表は実測。§2.3 は読みの更新であって新主張ではない。
