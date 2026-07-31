# 追補 — T3 系を **重み付き計数定理**として書き直す(W92-3 の採択条件)

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-07-31
- 位置づけ: `docs/notes/t3_quasi_purecycle_rigidity_v1.md`(本体)+ 同 `_addendum_t0.md`(第 1 追補)への **第 2 追補**。**erratum 方式 — 本体も第 1 追補も書き換えない**。
- 委嘱: 司令塔(次波 1)「T3 の計数定理を『重み付き個数 Σ 1/|Aut D|』の定理として書き直し、無重み化(Nielsen 数 N との一致)に Aut=1 条件を明記。generation/Jordan 域では Aut 自明ゆえ T3-WALL がそのまま定理であることの証明一段も」
- 入力正本: `sol/sol_reply_92_math19.md` **F92-2.3 / W92-3**。
- 検算: `scratchpad/t3_weighted_check.py`(SHA-256 `6614ad39…1d482cd`・Python 3.13 + sympy 1.14.0・GAP も指標表も使わない独立実装)

---

## 0. W92-3 の要求と、本追補の応答(先出し)

> **W92-3(Sol)**: 「一般に得た量は $\sum_D 1/\lvert\mathrm{Aut}\,D\rvert$ であり、無重みの Nielsen class 数 $N$ とは限らない。従って T3-CLASS を全範囲で『連結被覆の個数』と読むなら未採択である。自己同型が自明になる generation/Jordan 範囲では両者が一致するため、T3-WALL はその範囲で定理として採択してよい。『T3 系完全採択』は、全域を weighted theorem と書き、無重み化に `Aut=1` を付けることを条件とする。」

**指摘は全面的に正しい。** 本体は $N$ という 1 つの記号を **3 つの別の量**に使っていた。本追補はそれを分離し、各主張を正しい量で述べ直す。

| # | 本追補の結論 | 格 |
|---|---|---|
| **①** | 記号の分離: $\mathcal N^{\mathrm w}$(重み付き・推移)/ $\mathcal N^{\mathrm{tr}}$(無重み・推移)/ $N^{\mathrm{gen}}$(無重み・生成)の 3 量を定義。本体の「$N$」は文脈により 3 つを指していた | **修文** |
| **②** | **定理 T3-N0″**: 閉形が計算するのは $\mathcal N^{\mathrm w}$ **のみ**。$\mathcal N^{\mathrm w}=\mathcal N^{\mathrm{tr}}$ には $\mathrm{Aut}=1$ が、$\mathcal N^{\mathrm{tr}}=N^{\mathrm{gen}}$ には「推移 ⟹ 生成」が要る。**2 つの別々のギャップ** | **定理**(修文のみ・内容は第 1 追補と同一) |
| **③** | **定理 T3-CLASS″**: 分類は $\mathcal N^{\mathrm w}=1$ の分類である。$N^{\mathrm{gen}}=1$ の分類ではない | **定理**(修文)+ 悉皆 W1 |
| **④** | **補題 J-AUT**(新): Jordan 安全域 (J) では $\mathrm{Aut}(M)=1$ が**全推移対象**で成立し、かつ**推移 ⟹ 生成**。ゆえに (J) では $\mathcal N^{\mathrm w}=\mathcal N^{\mathrm{tr}}=N^{\mathrm{gen}}$ が**同時に**閉じる | **定理**(4 行・2 経路) |
| **⑤** | **⟹ 系 T3-WALL は (J) 域の定理としてそのまま生存**(W92-3 が許した通り)。証明鎖は「T3-N0″ → T3-CLASS″ → 補題 J-AUT → T3-WALL」 | **定理** |
| **⑥** | **反例(数値・新規)**: $\mathcal N^{\mathrm w}=1$ でも $N^{\mathrm{gen}}=0$ が起こる。$(\ell,t,n)=(7,2,9)$: $\mathcal N^{\mathrm w}=1$ だが唯一の類は $\mathrm{PSL}(2,8)$(位数 504)で $A_9$ を生成せず **$N^{\mathrm{gen}}=0$**。$(\ell,t,n)=(9,3,12)$: $\mathcal N^{\mathrm w}=1/3$、$\mathrm{Aut}=C_3$、$N^{\mathrm{gen}}=0$ | **悉皆機械(本追補の独立器)** |
| **⑦** | **本体の要修正箇所 2 件を名指し**: §0 の ⑥ 行と §2.3 の表の「$N$(実測)」列。後者は $1/3,\ 1/2$ という**非整数を「$N$」と書いていた** — 定義上あり得ない値で、混同の物証 | **修文指定** |
| **⑧** | **$m=1$ 層は T3-N0′ の射程外**(補題 A2 が $m\ge2$ 前件)。ところが T3-CLASS の 3 型のうち $\{1,1,0\}$ は $m=1$。5 個の passport を明示列挙し直接計数で埋めた(いずれも $n\le6$、(J) 域外) | **穴の名指し + 閉鎖**(有限確認) |

> **一行で**: 閉形が数えているのは**重み付きの推移類**であって、窓の個数ではない。両者の間には**重み**と**生成**の 2 枚の壁がある。Jordan 安全域では 2 枚とも同じ補題で一度に落ちるので、**壁の一意性(T3-WALL)は無傷**。

---

## 1. 三つの量の分離(記号の正本)

本体 §1 の設定($n=\ell+t$、$v$ 型 $(\ell,1^t)$、$g$ 型 $2^k1^{f_2}$、$h$ 型 $3^j1^{f_3}$、$C:=C_{S_n}(v)$、$\lvert C\rvert=\ell\cdot t!$)の下で:

$$\mathcal F^{\mathrm{tr}}(v):=\{(g,h)\ :\ g^2=h^3=1,\ g^{-1}h=v,\ \text{型指定},\ \langle g,h\rangle\ \text{推移}\},$$
$$\mathcal F^{\mathrm{gen}}(v):=\{(g,h)\in\mathcal F^{\mathrm{tr}}(v)\ :\ \langle g,h\rangle\supseteq A_n\}\subseteq\mathcal F^{\mathrm{tr}}(v).$$

$C$ は同時共役で両方に作用する。$(g,h)$ に対応する hypermap を $M$、その自己同型群を
$$\mathrm{Aut}(M)\ :=\ C_{\mathrm{Sym}([n])}(\langle g,h\rangle)$$
とおく($=$ dart 上の写像自己同型群。本体 補題 T3-3)。$v=g^{-1}h\in\langle g,h\rangle$ ゆえ $\mathrm{Aut}(M)\le C_{S_n}(v)=C$ であり、**$C$-作用の $(g,h)$ における固定化群はちょうど $\mathrm{Aut}(M)$** である。

> ### 定義(三つの量)
> $$\boxed{\ \mathcal N^{\mathrm w}:=\sum_{M\ \text{推移}}\frac1{\lvert\mathrm{Aut}(M)\rvert}=\frac{\lvert\mathcal F^{\mathrm{tr}}(v)\rvert}{\lvert C\rvert},\qquad
> \mathcal N^{\mathrm{tr}}:=\#\{M\ \text{推移}\},\qquad
> N^{\mathrm{gen}}:=\#\{M\ \text{生成}\}\ }$$
> ($M$ は $C$-軌道 $=$ 同型類を走る。$\mathcal N^{\mathrm w}$ の第 2 等号は軌道公式 $\lvert\mathcal F^{\mathrm{tr}}\rvert=\sum_M\lvert C\rvert/\lvert\mathrm{Aut}(M)\rvert$。)

**一般に $\mathcal N^{\mathrm w}\in\mathbb Q_{>0}$、$\mathcal N^{\mathrm{tr}},N^{\mathrm{gen}}\in\mathbb Z_{\ge0}$、かつ**
$$N^{\mathrm{gen}}\ \le\ \mathcal N^{\mathrm{tr}},\qquad \mathcal N^{\mathrm w}\le\mathcal N^{\mathrm{tr}}\quad(\text{等号}\iff\text{全}M\ \text{で}\ \mathrm{Aut}(M)=1).$$
**$\mathcal N^{\mathrm w}$ と $N^{\mathrm{gen}}$ の間には一般に大小関係すらない**(⑥ の例では $\mathcal N^{\mathrm w}=1>0=N^{\mathrm{gen}}$;逆に $\mathrm{Aut}$ が大きい非生成類が多ければ $\mathcal N^{\mathrm w}<N^{\mathrm{gen}}$ も原理的に起こりうる)。

**本体の「$N$」の実際の意味**(棚卸し):

| 本体の箇所 | 書かれている記号 | 実際に計算・測定されている量 |
|---|---|---|
| §1 の定義式 $N:=\#(\mathcal F(v)/C)$($\mathcal F$ は生成条件つき) | $N$ | $N^{\mathrm{gen}}$ |
| §2.2 定理 T3-N0 の左辺 $\sum_M1/\lvert\mathrm{Aut}\rvert$ | — | $\mathcal N^{\mathrm w}$(正しく書かれている) |
| **§2.3 の表の「$N$(実測)」列** | $N$ | **$\mathcal N^{\mathrm w}$**($1/3,1/2$ という非整数値が物証) |
| §3 定理 T3-CLASS の左辺 | $\sum_M1/\lvert\mathrm{Aut}\rvert$ | $\mathcal N^{\mathrm w}$(正しい) |
| **§0 の ⑥ 行「種数 0 で $N=1$ $\iff$ …」** | $N$ | **$\mathcal N^{\mathrm w}$**(誤記) |
| §4 の表の「$N$(本稿)」列 | $N$ | $\mathcal N^{\mathrm w}$ |
| 系 T3-WALL | $N$ | (J) 域なので三者一致(§3 で証明) |

---

## 2. 定理 T3-N0″ — 閉形が計算する量の正確な言明

> ### 定理 T3-N0″【定理・種数 0・$t\ge0$・$m\ge2$】(第 1 追補 T3-N0′ の**修文のみ**;証明は不変)
> 種数 0、$m:=t+f_2+f_3-1\ \ge2$ のとき
> $$\boxed{\ \mathcal N^{\mathrm w}\ =\ \sum_{M\ \text{推移}}\frac1{\lvert\mathrm{Aut}(M)\rvert}\ =\ \mathrm{Cat}(m-1)\cdot\frac{m!}{t!\,f_2!\,f_3!}\ }$$
> **左辺は「推移な地図の重み付き個数」であり、連結被覆の個数でも、窓を与える生成系の個数でもない。**
>
> **証明.** 第 1 追補 §3(補題 A1・A1′・A2 + $R=sW-2\lambda(u+z)-\lambda^2$ の次数計算)そのまま。本追補は 1 文字も変えない。∎

> ### 系 T3-N0″-a(**無重み化の条件**)
> $$\mathcal N^{\mathrm w}=\mathcal N^{\mathrm{tr}}\iff \mathrm{Aut}(M)=1\ \ \text{が全推移類 }M\ \text{で成立}.$$
> 十分条件は 2 つ(独立):
> - **(A-arith)** 本体 補題 T3-3: $\lvert\mathrm{Aut}(M)\rvert\mid\gcd(\ell,t)$。ゆえに **$\ell$ 素数かつ $0<t<\ell$ なら $\mathrm{Aut}=1$**($t=0$ では $\gcd(\ell,0)=\ell$ で情報が落ちる — 第 1 追補 §3 の注)。
> - **(A-gen)** $\langle g,h\rangle\supseteq A_n$($n\ge4$)なら $\mathrm{Aut}(M)=C_{S_n}(\langle g,h\rangle)\le C_{S_n}(A_n)=1$。**生成する類は必ず $\mathrm{Aut}=1$**。

> ### 系 T3-N0″-b(**生成化の条件**)
> $$\mathcal N^{\mathrm{tr}}=N^{\mathrm{gen}}\iff \text{全推移類が }A_n\ \text{を生成}.$$
> 十分条件: **補題 J**(本体 §1・古典 Jordan)— $\ell$ 素数、$\ell>n/2$、$\ell\le n-3$。

**⟹ 閉形 $\Rightarrow$ 窓の個数、には壁が 2 枚ある**(重み・生成)。W92-3 が指したのは 1 枚目だが、2 枚目も同格に効く(§4 の反例 (a) はまさに 2 枚目だけが破れる例)。

---

## 3. 補題 J-AUT と系 T3-WALL の完全な証明鎖

> ### 補題 J-AUT【定理・4 行】
> Jordan 安全域 (J)($\ell$ 素数、$n/2<\ell\le n-3$、すなわち $3\le t<\ell$)では
> $$\mathcal N^{\mathrm w}\ =\ \mathcal N^{\mathrm{tr}}\ =\ N^{\mathrm{gen}}.$$
> **証明.**
> (i) (J) は $t\ge3>0$ と $t=n-\ell<\ell$ を含む。$\ell$ は素数で $0<t<\ell$ だから $\gcd(\ell,t)=1$。本体 補題 T3-3 より $\lvert\mathrm{Aut}(M)\rvert\mid\gcd(\ell,t)=1$、よって**全推移類で $\mathrm{Aut}(M)=1$** — 系 T3-N0″-a により $\mathcal N^{\mathrm w}=\mathcal N^{\mathrm{tr}}$。
> (ii) 補題 J(古典 Jordan;本体 §1 で証明済)より (J) では推移 $\Rightarrow\langle g,h\rangle\supseteq A_n$、すなわち $\mathcal F^{\mathrm{tr}}=\mathcal F^{\mathrm{gen}}$ — 系 T3-N0″-b により $\mathcal N^{\mathrm{tr}}=N^{\mathrm{gen}}$。∎
>
> **注(冗長性の指摘)**: (ii) が成り立てば (A-gen) からも $\mathrm{Aut}=1$ が出るので、(J) では (i) は独立第 2 経路である。**2 経路が同じ結論を与える**ことは、この一段が壊れにくいことの証拠になる(片方は $\ell$ の素数性、他方は Jordan の分類定理に依存し、依存先が交わらない)。

> ### 定理 T3-CLASS″【定理・種数 0・$m\ge2$】(本体 §3 の**修文**)
> 種数 0、$m\ge2$ で
> $$\mathcal N^{\mathrm w}=1\iff \{t,f_2,f_3\}\in\bigl\{\{2,1,0\},\{5,0,0\}\bigr\}\ (\text{多重集合}).$$
> **証明.** 本体 §3 と同じ($\mathrm{Cat}(m-1)m!=t!f_2!f_3!$、$t+f_2+f_3=m+1$、右辺 $\le(m+1)!$ から $\mathrm{Cat}(m-1)\le m+1$、これが破れる最初の $m$ は $5$ — 悉皆 W1 で確認)。$m\le4$ の 4 通りを潰すと $m=2$: $\{2,1,0\}$、$m=3$: 解なし、$m=4$: $\{5,0,0\}$。$m=1$ の $\{1,1,0\}$ は**本定理の前件外**(§5 で別扱い)。∎
> **★ 本体 §0 ⑥ の「$N=1$」は「$\mathcal N^{\mathrm w}=1$」と読むこと。** $\mathcal N^{\mathrm w}=1$ は $N^{\mathrm{gen}}=1$ を**含意しない**(§4 (a))。

> ### 系 T3-WALL″(壁窓の一意性)【定理・W92-3 の採択条件を充たす形】
> Jordan 安全域 (J) の種数 0 窓で
> $$N^{\mathrm{gen}}=1\ \Longleftrightarrow\ (n,\ell,t,k,j)=(24,19,5,12,8)$$
> ただ 1 個。
> **証明(4 段・依存を明示).**
> 1. (J) ⟹ 補題 J-AUT ⟹ $N^{\mathrm{gen}}=\mathcal N^{\mathrm w}$。**ここで初めて無重み量が閉形で計算できる。**
> 2. (J) は $t\ge3$。定理 T3-CLASS″ の 2 型のうち $t\ge3$ を許すのは $\{5,0,0\}$、すなわち $t=5$、$f_2=f_3=0$ のみ($\{2,1,0\}$ は最大成分 2 < 3)。$m=1$ 型 $\{1,1,0\}$ も最大成分 1 < 3 で (J) では起こらない — **§5 の $m=1$ 穴は T3-WALL に影響しない**。
> 3. $f_2=0\Rightarrow k=n/2$、$f_3=0\Rightarrow j=n/3$。種数 0 の $k+2j=n+t-1$ に代入して $\tfrac n2+\tfrac{2n}3=n+4$、$n=24$、$\ell=n-t=19$、$(k,j)=(12,8)$。
> 4. 逆向きの検証: $19$ は素数、$19>12=n/2$、$19\le21=n-3$ で (J) を満たす ✓。$\mathcal N^{\mathrm w}=\mathrm{Cat}(3)\cdot4!/5!=5\cdot24/120=1$ ✓。∎
> **⟹ W92-3 が「その範囲で定理として採択してよい」と述べた通り、系 T3-WALL は (J) 域の定理である。上の 1. が、W92-3 の要求する `Aut=1` 条件の明示的な履行にあたる。**

**P-WALL-2 への含意**: 壁 $n=24$ の窓が**ただ 1 つ**であるという主張は $N^{\mathrm{gen}}$ の主張であり、上の鎖で閉じている。壁の非可解性主張は元々下限だけで立っており(本体 §6)、**本追補で何も失われない**。

---

## 4. 三量が実際に食い違う実例(悉皆機械・新規)

`scratchpad/t3_weighted_check.py`(sympy・GAP と指標表を使わない独立実装)。$v$ を型 $(\ell,1^t)$ に固定 → 型 $2^k1^{f_2}$ の対合 $g$ を悉皆 → $h:=gv$ が $h^3=1$ かつ型 $3^j1^{f_3}$ のものを収集 → 推移性で絞り $\lvert\mathcal F^{\mathrm{tr}}\rvert$、$\lvert\langle g,h\rangle\rvert\ge n!/2$ で絞り $\lvert\mathcal F^{\mathrm{gen}}\rvert$。

| $\ell$ | $t$ | $n$ | $(k,j)$ | $f_2$ | $f_3$ | $m$ | $\lvert\mathcal F^{\mathrm{tr}}\rvert$ | $\lvert C\rvert$ | $\mathcal N^{\mathrm w}$ | 閉形 | $\lvert\langle g,h\rangle\rvert$ | $N^{\mathrm{gen}}$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **7** | **2** | 9 | (4,3) | 1 | 0 | 2 | 14 | 14 | **1** | 1 ✓ | **504** $=\lvert\mathrm{PSL}(2,8)\rvert$ | **0** |
| 9 | 1 | 10 | (4,3) | 2 | 1 | 3 | 54 | 9 | **6** | 6 ✓ | $1814400=10!/2$ | **6** |
| **9** | **3** | 12 | (6,4) | 0 | 0 | 2 | 18 | 54 | **1/3** | 1/3 ✓ | **324** | **0** |
| 3 | 1 | 4 | (2,1) | 0 | 1 | **1** | 3 | 3 | **1** | 1 ✓ | $12=4!/2$ | **1** |

- **(a) $(\ell,t)=(7,2)$**: $\mathcal N^{\mathrm w}=\mathcal N^{\mathrm{tr}}=1$(重みの壁は無い)だが**生成の壁で $N^{\mathrm{gen}}=0$**。$\mathcal N^{\mathrm w}=1$ から「窓が 1 個ある」は**言えない**ことの実物。本体 §3 の「$N=1$ と『窓が存在する』は独立」という注意の、機械による確認でもある。
- **(b) $(\ell,t)=(9,1)$**: 較正行。本体 §2.3 の $T_{\rm trans}=54,\lvert C\rvert=9$ と**逐語一致**。ここでは $\mathcal N^{\mathrm w}=\mathcal N^{\mathrm{tr}}=N^{\mathrm{gen}}=6$(三者一致)。
- **(c) $(\ell,t)=(9,3)$**: $\mathcal N^{\mathrm w}=1/3$。軌道は 1 本($18=54/3$)で固定化群の位数 3 ⟹ $\mathrm{Aut}=C_3$ ⟹ $\mathcal N^{\mathrm{tr}}=1$、しかし群位数 324 で非生成 ⟹ $N^{\mathrm{gen}}=0$。**重みと生成の壁が両方立っている**唯一の行。本体 §3 の「$\ell=9,t=3$ は $\mathrm{Aut}=C_3$ ⟹ 生成窓なし」を機械で確認。
- **(d) $(\ell,t)=(3,1)$**: $m=1$ 行(§5)。

**格**: 単系統(本追補の独立器)。ただし (b) 行は本体 §2.3 の 3 実装(完全指標表・自前 MN・直接列挙)と一致し、(c) 行は本体 §3 の記述と一致する。**Lean verified ではない。**

---

## 5. $m=1$ 層 — T3-N0′/N0″ の射程外(名指しの穴と、その閉鎖)

**穴**: 第 1 追補の補題 A2 は「3 価黒頂点が 1 個以上」$\iff m\ge2$ を前件にもつ。ところが本体 §3 の分類が挙げる 3 型のうち $\{1,1,0\}$ は $t+f_2+f_3=2$、すなわち **$m=1$** であり、**定理 T3-N0′ の証明はこの型を覆っていない**。本体 §2.2 も退化 $(t,f_2,f_3)=(1,1,0)$ を明示除外していたので、**本体の分類定理は自分の計数定理が扱わない型を答に含めていた**。

**閉鎖**: $m=1$ の passport は有限個であり、悉皆で確認できる($m+1=2$ 枚の葉・3 価黒 0 個 ⟹ 木は「1 辺」または「黒–白–黒 の道」の 2 形)。

| $(t,f_2,f_3)$ | 木の形 | $j$ | $n$ | $\ell$ | $\mathrm{Aut}$ | $\mathcal N^{\mathrm w}$ | 閉形 $\mathrm{Cat}(0)\cdot1!/(t!f_2!f_3!)$ |
|---|---|---|---|---|---|---|---|
| $(1,1,0)$ | 1 辺(ループ黒葉 + 脚) | 1 | **3** | 2 | 1 | 1 | 1 ✓ |
| $(1,0,1)$ | 道(ループ黒葉 + 裸黒葉) | 1 | **4** | 3 | 1 | **1**(機械確認 §4(d)) | 1 ✓ |
| $(0,1,1)$ | 1 辺(裸黒葉 + 脚) | 0 | **1** | 1 | 1 | 1 | 1 ✓ |
| $(2,0,0)$ | 道(ループ黒葉 2 枚) | 2 | **6** | 4 | $C_2$(2 葉の交換) | 1/2 | 1/2 ✓ |
| $(0,0,2)$ | 道(裸黒葉 2 枚) | 0 | **2** | 2 | $C_2$ | 1/2 | 1/2 ✓ |

- **閉形は $m=1$ でも正しい**(5 通り全一致)。ただし証明は補題 A2 経由ではなく**直接列挙**である。
- **$n\ge4$ を満たすのは $(1,0,1)$($n=4$)のみ**で、これは §4(d) で群論的に $\mathcal N^{\mathrm w}=1$、$\lvert\langle g,h\rangle\rvert=12=\lvert A_4\rvert$、$N^{\mathrm{gen}}=1$ と確認した。
- **(J) 域($t\ge3$)には $m=1$ 型は 1 つも入らない**(上表の $t\le2$)。**⟹ 系 T3-WALL″ は本穴と無関係**(§3 証明の段 2 で明示)。

> **修文指定**: 本体 §0 ⑥ と §3 の T3-CLASS の主張文には「$m\ge2$;$m=1$ 型 $\{1,1,0\}$ は本追補 §5 の直接列挙による」を添えること。

---

## 6. 本体・第 1 追補への修文指定(erratum の一覧)

| 箇所 | 現行 | 修文後 |
|---|---|---|
| 本体 §0 表 ⑤ | 「$\ell$ 奇素数・$t<\ell$ なら $\mathrm{Aut}=1$ でこれが $N$ そのもの」 | 「$\ell$ 奇素数かつ **$0<t<\ell$** なら $\mathrm{Aut}=1$ でこれが $\mathcal N^{\mathrm{tr}}$。さらに $N^{\mathrm{gen}}$ と一致するには『推移⟹生成』が要る(補題 J)」 |
| 本体 §0 表 ⑥ | 「種数 0 で **$N=1$** $\iff$ …」 | 「種数 0 で **$\mathcal N^{\mathrm w}=1$** $\iff$ …($m\ge2$)」 |
| 本体 §2.3 の表の列見出し | 「$N$(実測)」 | 「$\mathcal N^{\mathrm w}=T_{\rm trans}/\lvert C\rvert$(実測)」— **$1/3,1/2$ の行はこれで整合** |
| 本体 §2.3 の $n=36$ 行の注 | 「$N=6$ を先に紙で予言」 | 「$\mathcal N^{\mathrm w}=6$ を先に紙で予言」($n=36$ は $\ell=29$ 素数・$t=7<29$ ゆえ (J) 域で三量一致 — **予言の内容は不変**) |
| 本体 §3 定理 T3-CLASS | 「$N=1$ の完全分類」 | 「$\mathcal N^{\mathrm w}=1$ の完全分類($m\ge2$)」 |
| 本体 §3 系 T3-WALL | (そのまま) | **本追補 §3 の系 T3-WALL″ を正本とする**(証明鎖に補題 J-AUT を挿入) |
| 本体 §0 表 ⑧ | 「$n=36$ で **$N=6$**」 | 「$n=36$ で $\mathcal N^{\mathrm w}=6$」(= $N^{\mathrm{gen}}=6$、(J) 域ゆえ) |
| 本体 §11 格付け表 | 「定理 T3-N0($N$ の閉評価)」 | 「定理 T3-N0″($\mathcal N^{\mathrm w}$ の閉評価)」 |

**変わらないもの**: 定理 CENT・XI-C・XI-INJ は T3 の計数に**非依存**(F91-1.5・本体 §12)。本追補も CENT の格に何も足さない・引かない。

---

## 7. 外部向けの述べ方(本体 §7 の修文)

> 種数 0・3 分岐点・分岐データ $(2^k1^{f_2},3^j1^{f_3},(\ell,1^t))$ の**推移な被覆の同型類の、自己同型群の位数の逆数で重みづけた個数**は
> $$\mathrm{Cat}(m-1)\cdot\frac{m!}{t!\,f_2!\,f_3!},\qquad m=t+f_2+f_3-1\ (\ge2)$$
> **で与えられる。$\ell$ が素数で $0<t<\ell$ のときは自己同型が自明になり、これは同型類の個数そのものである。さらに $\ell>n/2$ かつ $\ell\le n-3$ ならば全ての類が $A_n$ または $S_n$ を単系群にもち、重み付き個数が 1 になる剛な例は $(2^{12},3^8,(19,1^5))$、$n=24$、ただ 1 つである。**

**新規性は依然として主張しない**(本体 §7 の衝突候補 4 件と【文献要請 (1)】は生きている)。**重み付き計数であることは、平面木・cacti の古典的枚挙(Goulden–Jackson / Tutte)と同じ土俵に乗ることをむしろ強めるので、既知の再発見である蓋然性は上がる。**

---

## 8. Sol への申し送り(監査点)

1. **補題 J-AUT の (i)**: 本体 補題 T3-3 の「$\lvert\mathrm{Aut}\rvert$ が $t$ を割る」段は $t>0$ を要する(大面が唯一 ⟹ $\lvert\mathrm{Aut}\rvert\mid\ell$、次数 1 の面に自由作用 ⟹ $\lvert\mathrm{Aut}\rvert\mid t$)。(J) は $t\ge3$ なので使えるが、**$t=0$ 域では (i) が空振り**し (A-gen) しか残らない。この非対称を疑ってほしい。
2. **$\mathcal N^{\mathrm w}$ の軌道公式**($\mathrm{Stab}_C(g,h)=C_{S_n}(\langle g,h\rangle)$)— $v\in\langle g,h\rangle$ を使う 1 行。ここが本追補の全体の土台。
3. **$m=1$ 層の直接列挙**(§5)— 木の形が 2 種しかないこと、$(2,0,0)$ と $(0,0,2)$ の $\mathrm{Aut}=C_2$ の同定。$(0,0,2)$ は $n=2$ で $h=1$ という極端な退化なので、そもそも族の定義域に入れるべきかの判断も仰ぎたい。
4. **§4(a) の $\mathrm{PSL}(2,8)$ 行**: $\mathcal N^{\mathrm w}=1$ かつ $N^{\mathrm{gen}}=0$ という、W92-3 の懸念の 2 枚目の壁の実物。この行を本体 §2.3 の表に**恒久の負例**として常備することを提案する。
5. **T3-CLASS″ の $m=3$ 「解なし」**: $12$ が $\{24,6,4,2\}$ に現れないという 1 行の場合分け。悉皆 W1($m\le40$)が独立に支持している。

---

## 9. 格付け表(本追補の分)

| 主張 | 格 |
|---|---|
| 三量の分離と $\mathcal N^{\mathrm w}=\lvert\mathcal F^{\mathrm{tr}}\rvert/\lvert C\rvert$(軌道公式) | **proof** |
| 定理 T3-N0″($\mathcal N^{\mathrm w}$ の閉評価・$m\ge2$) | **定理**(第 1 追補の証明・修文のみ) |
| 系 T3-N0″-a / -b(無重み化・生成化の条件) | **proof**(初等) |
| **補題 J-AUT**((J) で三量一致・2 独立経路) | **定理**(4 行) |
| 定理 T3-CLASS″($\mathcal N^{\mathrm w}=1$ の分類・$m\ge2$) | **定理** + 悉皆 W1($m\le40$) |
| **系 T3-WALL″**(P-WALL-2 の一意性・$N^{\mathrm{gen}}$ 水準) | **定理**(証明鎖 4 段・W92-3 の採択条件を充足) |
| $m=1$ 層の閉形(5 passport) | **有限直接列挙**(+ $n=4$ 行は群論悉皆) |
| $\mathcal N^{\mathrm w}=1\not\Rightarrow N^{\mathrm{gen}}=1$($\mathrm{PSL}(2,8)$ 行) | **悉皆機械**(単系統・独立器) |
| 本体の 8 箇所の修文指定 | **erratum** |
| 種数 $\ge1$ の閉形【GAP-T3a】 | **UNKNOWN のまま**(【文献要請 (2)】生存) |
| 外部新規性 | **主張しない**(本追補で蓋然性はむしろ下がった) |
