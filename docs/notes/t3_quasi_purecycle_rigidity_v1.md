# 標的 T3 — 準 pure-cycle 剛性:$N$ の閉評価、適用範囲、そして **予想 CENT の定理化** v1

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-07-31
- 委嘱: 司令塔「標的 T3(ideas_014)— 族 $(2^k1^*,3^j1^*,(\ell,1^t))$ で $N=1$ を紙で証明せよ。適用範囲の明示・外部定理としての位置づけ・系として CENT の $\subseteq$ 方向」
- 入力正本: `docs/notes/sat_l1_v1.md`(§6.2 の $N$ の定義・§10.6.2 の計数機構)/ `docs/notes/litgate_rigidity_hurwitz_v1.md` / `docs/notes/hexagon_orientation_ruling_v1.md` / `search/kerchi-judge.g`(受理条件の実物・**146–215 行を直接読解**)
- 配達済み原著 `papers/delivered/arxiv_math_0609118.pdf`(Liu–Osserman)は **abstract と §1 の限界表明のみ**を覚書経由で参照。**本文は未読**(範囲申告)。
- 向き規約: 本稿の $(g,h)$ は $f$ を経由しない量($g^2=h^3=1$、$g^{-1}h=v$)なので **hexagon の向き規約に非依存**。$f$ を扱う §5–§6 では judge 規約(`hexagon_orientation_ruling_v1.md`)に統一した。

---

## 0. 結論(先出し)

| # | 主張 | 格 |
|---|---|---|
| **①** | **委嘱の前提を訂正**: 「剛性 $N=1$ ⟺ CENT の $\subseteq$」は**偽**。judge の **settled 節**(裁定169)が $m=0$ 層をさらに刈るため、$N\gg1$ の窓でも CENT は成立する。実測: $n=10$ 窓 hexagon $90\to$ 生成 $54\to$ **settled 9** $=\lvert C(w)\rvert$(このとき $N=6$) | **反証(proof + 悉皆機械)** |
| **②** | **定理 XI-C(settled の正体)**: $m=0$ の settled 節 $\iff$ $\exists\alpha\in S_n$ で $w^\alpha=w$ かつ $v^\alpha=v^{f}$。すなわち **$\Xi(\ker\widetilde\chi)\subseteq C_{S_n}(w)$**(全窓・$\varepsilon$ 不問)。$\mathrm{Aut}(E)$ の構造から従う | **定理**(紙・$\varepsilon=0/1$ 両方)+ 3 窓機械 |
| **③** | **定理 XI-INJ($\Xi$ 単射)**: $c\in C_{S_n}(v)$、$(cg)^2=1$、$g^2=1$、$h^3=1$、$C_{S_n}(\langle g,h\rangle)=1$ $\Rightarrow c=1$。**5 行**。$\Xi$ は $\ker\widetilde\chi$ 上単射 | **定理**(初等・完結)+ 4 窓悉皆 |
| **④** | **⟹ 予想 CENT は定理になった**: $\ker\widetilde\chi\cong C_{S_n}(w)$(② で $\subseteq$、③ で単射、SURV+ で $\supseteq$)。**剛性も飽和も一切不要**。$p,s$ の制限もなし(定理 CENT-0 の真の一般化) | **定理**(証明鎖 3 段)+ 3 窓で全段機械確認 |
| **⑤** | **定理 T3-N0($N$ の閉評価・種数 0)**: $m:=t+f_2+f_3-1=j-t+1$ とおくと $$\sum_M\frac1{\lvert\mathrm{Aut}M\rvert}=\mathrm{Cat}(m-1)\cdot\frac{m!}{t!\,f_2!\,f_3!}$$ $\ell$ 奇素数・$t<\ell$ なら $\mathrm{Aut}=1$ でこれが $N$ そのもの | **定理**(平面木との全単射)+ **75 行の独立計数と完全一致・不一致 0** |
| **⑥** | **分類**: 種数 0 で $N=1$ $\iff$ 多重集合 $\{t,f_2,f_3\}\in\{\{1,1,0\},\{2,1,0\},\{5,0,0\}\}$。完全リスト | **定理**(有限個の場合分け) |
| **⑦** | **系(壁の一意性)**: Jordan 安全域($\ell$ 素数・$n/2<\ell\le n-3$、すなわち $3\le t<\ell$)の種数 0 窓で $N=1$ となるのは **$n=24,\ \ell=19,\ t=5,\ (k,j)=(12,8)$ の 1 個だけ**。= **P-WALL-2**。$n\le34$ 掃引でも唯一 | **定理**(⑥ から 3 行)+ 掃引一致 |
| **⑧** | **反例(委嘱の予期どおり一級)**: 同族の $n=36$($\ell=29,t=7$、不動点なし種数 0)で **$N=6$**。$N=1$ は $t$ について**有界**であり、族全体には広がらない | **予言先行 → 機械的中**(木モデルで先に 6 と予言し、MN 指標計算が $T_{\rm trans}=876960=6\cdot\lvert C\rvert$ を返した) |
| **⑨** | 種数 $\ge1$ の $N$ の閉形は **UNKNOWN**(1 面地図 = unicellular map の枚挙が要る)。実測では Jordan 安全域の種数 1 窓はすべて $N\ge 10$ | **UNKNOWN + 実測**・【文献要請】§8 |
| **⑩** | 外部位置づけ: ⑤⑥ は Liu–Osserman(pure-cycle・種数 0・既約性)の **pure-cycle を落とした版**の完全計数。ただし **種数 0 の「1 本の長巡回 + 不動点」passport は古典的な平面木計数の圏内**であり、**新規性は主張しない(要 scout)** | **格付けのみ** |

> **一行で**: 「$N=1$ を証明せよ」は**やってみたら $N=1$ はほぼ成り立たない**(閉形で完全に判った)。ところが同じ解剖の途中で、**CENT が $N$ とは無関係に、settled 節と 5 行の補題だけで定理になる**ことが判った。$N$ の閉形は外向き(Hurwitz 側)の成果として独立に残る。

---

## 1. 設定と記号

$n=\ell+t$、$w_0=v$ を型 $(\ell,1^t)$ の元($\Delta:=\mathrm{Fix}(v)$、$\lvert\Delta\rvert=t$)。
$$\mathcal F(v):=\{(g,h)\ :\ g^2=1,\ h^3=1,\ g^{-1}h=v,\ \langle g,h\rangle\supseteq A_n\}$$
$g$ の型 $2^k1^{f_2}$($f_2=n-2k$)、$h$ の型 $3^j1^{f_3}$($f_3=n-3j$)。$C:=C_{S_n}(v)=\langle v\rangle\times\mathrm{Sym}(\Delta)$、$\lvert C\rvert=\ell\cdot t!$。
$$N:=\#\bigl(\mathcal F(v)/C\ \text{(同時共役)}\bigr)\qquad(\text{sat\_l1\_v1 §6.2 の }N).$$

**種数**: Riemann–Hurwitz から $2\gamma-2=-2n+k+2j+(\ell-1)$、すなわち
$$\boxed{\ k+2j=n+t-1+2\gamma\ }\qquad(\gamma=\text{種数}\ \ge0).$$
$\ell$ 奇 $\Rightarrow v$ 偶 $\Rightarrow k$ 偶(本族は常に $\varepsilon=0$)。

**Jordan 安全域**(以下この条件を (J) と呼ぶ):
> **補題 J**【proof・古典】 $\ell$ 素数、$\ell>n/2$、$\ell\le n-3$(すなわち $3\le t<\ell$)なら、$\langle g,h\rangle$ 推移 $\Rightarrow\langle g,h\rangle\supseteq A_n$。
> **証明.** $\ell>n/2$ ⟹ ブロック長 $b\ge2$ なら $b\le n/2<\ell$ でブロック数 $m=n/b$;$\ell$-巡回の誘導置換は位数 $1$ か $\ell$。位数 1 ならその台($\ell$ 点)が 1 ブロックに入り $\ell\le b$ で矛盾、位数 $\ell$ なら $m\ge\ell>n/2\ge b\cdot m/2$ で矛盾。ゆえに原始的。原始 + 素数長 $\ell\le n-3$ の巡回 ⟹ Jordan の定理で $A_n$ を含む。∎
> (sat_l1_v1 §10.6.5 の 3 段と同じ。$t\ge3$ が Jordan の $\ell\le n-3$ に対応する。)

---

## 2. 定理 T3-N0 — 種数 0 での $N$ の閉評価

### 2.1 地図への翻訳

$(g,h)$ に **hypermap(bipartite map)** $M$ を対応させる: 黒頂点 $=h$ の巡回(次数 3 が $j$ 個・次数 1 が $f_3$ 個)、白頂点 $=g$ の巡回(次数 2 が $k$ 個・次数 1 が $f_2$ 個)、辺(dart)$=[n]$、面 $=v$ の巡回。Euler 標数は上の種数式と一致する。

> ### 補題 T3-1(次数 1 の面 = ループ)【proof】
> $M$ の次数 1 の面は、**3 価黒頂点に付いたループ辺**(残り 1 本が「柄」)に他ならない。
> **証明.** 面が dart $d$ 1 個 $\iff v(d)=d\iff h(g(d))=d$。$g(d)=d$ なら $h(d)=d$ で $\{d\}$ が $\langle g,h\rangle$ 軌道になり推移性に反する。よって $g(d)=d'\ne d$ かつ $h(d')=d$、すなわち $h$ の 3-巡回 $(d',d,e)$ と $g$ の 2-巡回 $(d,d')$ — これがループ。∎

> ### 補題 T3-2(ループを外すと 1 面地図)【proof】
> $t$ 本のループを取り除いた $M'$ は連結・面数 1・同種数。種数 0 なら **$M'$ は平面木**。
> **証明.** ループ辺は橋でないので連結性は不変。各ループの次数 1 の面は隣の(唯一の)大面と併合されるので $F'=F-t=1$。$V'=V-t$($次数2$ の白が消える)、$E'=n-2t$ で $V'-E'+F'=V-E+F$。$\gamma=0$ なら $V'=E'+1$。∎
> 逆に、平面木 $T$(黒次数 $\in\{1,3\}$・白次数 $\in\{1,2\}$)と黒葉の $t$-部分集合 $S$ から $M$ が同型を除き一意に復元される(ループの 2 dart の入れ替えは同型)。

> ### 補題 T3-3($\mathrm{Aut}$ の消滅)【proof】
> $\mathrm{Aut}(M)=C_{\mathrm{Sym}(darts)}(\langle g,h\rangle)$ は dart 上自由に働く。大面(次数 $\ell$)は唯一なので保たれ $\lvert\mathrm{Aut}\rvert\mid\ell$;次数 1 の面を固定すればその dart を固定して恒等になるので $t$ 個の面に自由に働き $\lvert\mathrm{Aut}\rvert\mid t$。よって $\lvert\mathrm{Aut}(M)\rvert\mid\gcd(\ell,t)$。
> **$\ell$ 素数・$0<t<\ell$ なら $\mathrm{Aut}(M)=1$。**∎
> 一般には $\lvert\mathcal F(v)\rvert=\lvert C\rvert\cdot\sum_M 1/\lvert\mathrm{Aut}(M)\rvert$(標識付け数え上げ)であり、$\mathrm{Aut}=1$ のとき $N=\#\{M\}$。

### 2.2 母関数と閉形

平面木を「ループ付き黒葉」で根付ける。根から先に垂れる部分木の母関数を $Y$、$u$=ループ付き黒葉、$z$=裸の黒葉($h$ の不動点)、$\lambda$=脚($g$ の不動点)とすると、3 価黒頂点では入辺以外の 2 スロットが**線形順序**になるので
$$\boxed{\ Y=u+z+(\lambda+Y)^2\ }$$
$W:=\lambda+Y$ とおくと $W=s+W^2$($s=u+z+\lambda$)、ゆえに $W=\sum_{i\ge1}\mathrm{Cat}(i-1)s^i$。根付き対象の母関数は $u\,Y=u\,W-u\lambda$ だから、$m:=t+f_2+f_3-1$ として

> ### 定理 T3-N0【定理・種数 0】
> $(n\ge4$、種数 0、退化 $(t,f_3,f_2)=(1,0,1)$ を除く$)$
> $$\boxed{\ \sum_{M}\frac1{\lvert\mathrm{Aut}(M)\rvert}\;=\;\mathrm{Cat}(m-1)\cdot\frac{m!}{t!\,f_2!\,f_3!},\qquad m=t+f_2+f_3-1=j-t+1\ }$$
> $\ell$ 奇素数かつ $0<t<\ell$ なら左辺 $=N$(補題 T3-3)。
> $\mathrm{Cat}(i)=\frac1{i+1}\binom{2i}{i}$。

**読み**: $\mathrm{Cat}(m-1)$ = 内部節点 $m-1$ 個の平面二分木、$m!/(t!f_2!f_3!)$ = その $m$ 枚の(左右順序のついた)葉を「ループ付き黒葉 $t$・脚 $f_2$・裸黒葉 $f_3$」に塗り分ける方法。**$m-1=j-t$ は「ループを外した木の 3 価黒頂点の個数」**。

### 2.3 検算(2 系統・不一致 0)

| 系統 | 内容 | 結果 |
|---|---|---|
| **完全指標表**(`t3_a_chars.g`) | $S_m$($m\le22$)の class multiplication coefficient から $T_{\rm all}$、巡回の集合分割 Möbius(本族では**二項反転**に退化・§2.4)で $T_{\rm trans}$ | 種数 0 の全行で定理 T3-N0 と一致 |
| **自前 MN**(`t3_b_mn.g`, `t3_c_sweep.g`) | $\ell$-weight 1 の $\lambda$ のみに落とした Frobenius 和(完全指標表を作らずに $n\le36$) | **種数 0 行 52/52 一致・不一致 0** |
| **直接列挙**(`t3_d_brute.g`) | 指標を使わず対合を悉皆列挙し $C(v)$-軌道を明示計算 | $n=10,13,16$ で $T_{\rm all},T_{\rm trans},N$ が上の 2 系統と一致 |

**代表値**(すべて 3 系統一致):

| $\ell$ | $t$ | $n$ | $(k,j)$ | $f_2$ | $f_3$ | $m$ | $T_{\rm trans}$ | $\lvert C\rvert$ | $N$(実測) | 定理 T3-N0 |
|---|---|---|---|---|---|---|---|---|---|---|
| 9 | 1 | 10 | (4,3) | 2 | 1 | 3 | 54 | 9 | **6** | $\mathrm{Cat}(2)\cdot3!/(1!2!1!)=6$ ✓ |
| 7 | 0 | 7 | (2,2) | 3 | 1 | 3 | 14 | 7 | **2** | $2\cdot6/(0!3!1!)=2$ ✓ |
| 13 | 3 | 16 | (8,5) | 0 | 1 | 3 | 156 | 78 | **2** | ✓ |
| 17 | 3 | 20 | (10,6) | 0 | 2 | 4 | 1020 | 102 | **10** | ✓ |
| 19 | 3 | 22 | (10,7) | 2 | 1 | 5 | 15960 | 114 | **140** | ✓ |
| **9** | **3** | **12** | (6,4) | 0 | 0 | 2 | 18 | 54 | **1/3** | $\mathrm{Cat}(1)\cdot2!/3!=1/3$ ✓(唯一の木が $\mathrm{Aut}=C_3$) |
| **14** | **4** | **18** | (9,6) | 0 | 0 | 3 | 168 | 336 | **1/2** | $2\cdot6/4!=1/2$ ✓($\mathrm{Aut}=C_2$) |
| **19** | **5** | **24** | (12,8) | 0 | 0 | 4 | **2280** | **2280** | **1** | $5\cdot24/5!=1$ ✓ **= P-WALL-2** |
| **29** | **7** | **36** | (18,12) | 0 | 0 | 6 | **876960** | 146160 | **6** | $42\cdot720/7!=6$ ✓ **予言先行** |

> **予言先行の記録**: $n=36$ の行は、木モデルから **$N=6$・$T_{\rm trans}=6\cdot29\cdot5040=876960$ を先に紙で予言**し、その後 MN 指標計算(`t3_b_mn.g` [3])が **876960 をそのまま返した**。この 1 点で定理 T3-N0 は「11 窓に合わせた式」ではないことが確定する。

### 2.4 なぜ Möbius が二項反転に退化するか【proof】

$\langle g,h\rangle$ の軌道は $v$ の巡回の合併。$v$ の不動点だけからなる軌道 $O$ 上では $g\vert_O h\vert_O=1$ かつ $g^2=h^3=1$ ⟹ $h=g$、$h^3=g=1$ ⟹ $\lvert O\rvert=1$。よって非主軌道はすべて 1 点で、型 $(k,j)$ も保たれる:
$$T_{\rm all}^{(k,j)}(\ell,1^t)=\sum_{a=0}^t\binom ta\,T_{\rm trans}^{(k,j)}(\ell,1^a)\ \Longrightarrow\ T_{\rm trans}^{(k,j)}(\ell,1^t)=\sum_{a=0}^t(-1)^{t-a}\binom ta\,T_{\rm all}^{(k,j)}(\ell,1^a).$$
(sat_l1_v1 §10.6.2 の一般 Möbius の、本族での退化形。配達覚書 §2 の Hall 格子はやはり不要。)

---

## 3. $N=1$ の完全分類と適用範囲(委嘱 2)

> ### 定理 T3-CLASS【定理・種数 0】
> 種数 0 で $\displaystyle\sum_M\frac1{\lvert\mathrm{Aut}\rvert}=1$ となるのは
> $$\{t,f_2,f_3\}\in\bigl\{\ \{1,1,0\},\ \{2,1,0\},\ \{5,0,0\}\ \bigr\}$$
> の場合に**限る**(多重集合として)。
> **証明.** 条件は $\mathrm{Cat}(m-1)\,m!=t!f_2!f_3!$、ただし $t+f_2+f_3=m+1$。右辺の最大値は $(m+1)!$(1 つに集中)なので $\mathrm{Cat}(m-1)\le m+1$、すなわち $m\le4$($\mathrm{Cat}=1,1,2,5,14,\dots$ vs $m+1=2,3,4,5,6$)。
> - $m=1$: $t!f_2!f_3!=1$、和 $2$ ⟹ $\{1,1,0\}$。
> - $m=2$: $=2$、和 $3$ ⟹ $\{2,1,0\}$($\{3,0,0\}=6$、$\{1,1,1\}=1$ は不可)。
> - $m=3$: $=12$、和 $4$ ⟹ 候補値は $24,6,4,2$ のみで $12$ は出ない。**解なし**。
> - $m=4$: $=120$、和 $5$ ⟹ $\{5,0,0\}$ のみ($24,12,6,4$ は不可)。∎

> ### 系 T3-WALL(壁窓の一意性)【定理】
> Jordan 安全域 (J)($\ell$ 素数・$n/2<\ell\le n-3$、すなわち $3\le t<\ell$)の種数 0 窓で $N=1$ となるのは
> $$\boxed{\ n=24,\quad \ell=19,\quad t=5,\quad (k,j)=(12,8)\quad(\text{$g,h$ とも不動点なし})\ }$$
> **ただ 1 個**。すなわち **P-WALL-2**。
> **証明.** (J) は $t\ge3$。定理 T3-CLASS の 3 型のうち $t\ge3$ を許すのは $\{5,0,0\}$ で $t=5,\ f_2=f_3=0$ のみ。$f_2=0\Rightarrow k=n/2$、$f_3=0\Rightarrow j=n/3$、種数 0 ⟹ $\tfrac n2+\tfrac{2n}3=n+4$ ⟹ $n=24$、$\ell=19$。$19$ は素数、$19>12$、$19\le21$ で (J) を満たす ✓。∎
> **掃引での追認**: $\ell\in\{5,7,11,13,17,19,23,29\}$、$t\le8$、$n\le34$、種数 $\ge0$ の全 (J) 行で $N=1$ は **$[19,5,24,12,8,\gamma{=}0]$ の 1 行のみ**(`t3_c_sweep.g`)。

**$t$ の上限**(委嘱 2 への直接回答):
- **$N=1$ の意味での上限は $t\le5$**。$t\ge6$ では常に $N>1$($\mathrm{Cat}$ が階乗を追い越す)。
- **不動点なし種数 0 の族では $t=n/6+1$ が強制**され($\ell=5n/6-1$)、$\ell$ 奇 ⟹ $n\equiv0\ (12)$。よって許される $t$ は $3,5,7,9,\dots$ で、$t=3$($\ell=9$、$\gcd=3$ ⟹ $\mathrm{Aut}=C_3$ ⟹ **生成窓が存在しない**)、$t=5$($\ell=19$ ⟹ $N=1$)、$t=7$($\ell=29$ ⟹ **$N=6$**)。
- **$\ell>n/2$ の必要性**: 原始性の自動化に使う(補題 J)。落とすと「推移だが $A_n$ でない」($n{=}12$ の $2^5{:}S_5$ 型)が復活し、$N$ は生成分の勘定でなくなる。**$\ell$ 素数**は補題 J と補題 T3-3($\mathrm{Aut}=1$、$N$ が整数)の両方に効く。
- **生成条件(Jordan)との相互作用**: (J) の外では $N$ は「推移類の個数」で、生成分はその部分集合。$\ell=9,t=1$ 窓が典型($N_{\rm trans}=6$、うち $A_{10}$ 生成 $6$、非推移 $9$)。逆に $\ell=7,t=2,n=9$ は $N=1$ だが**唯一の類が $\mathrm{PSL}(2,8)$**(位数 504)で生成しない — **$N=1$ と「窓が存在する」は独立**。

**種数 $\ge1$**(委嘱 2 の残り): 補題 T3-2 は種数 $\gamma$ でも成立し $M'$ は **1 面地図(unicellular map)**。その prescribed-degree 枚挙の閉形は本稿では出せていない(**UNKNOWN**)。実測(`t3_c_sweep.g`)では (J) 域の種数 1 窓はすべて $N\ge10$($n=32,\ell=29,t=3$: $N=4620$;$n=33,\ell=29,t=4$: $N=2310$;$n=32,(16,10)$: $N=4620$)。**種数 $\ge1$ で $N=1$ の (J) 窓は掃引範囲に存在しない。**

---

## 4. ★ 委嘱前提の訂正 — $N$ は $\lvert\ker\widetilde\chi\rvert$ を支配しない

`sat_l1_v1` §6.2 は $\ker\widetilde\chi\leftrightarrow\mathcal F(v)$(生成条件 $\langle g,h\rangle=\langle a_1,b_1\rangle$)という全単射を置き、そこから $\lvert\ker\rvert=\lvert C(v)\rvert\cdot N$ を導いた。**この対応は正しくない。** judge(`search/kerchi-judge.g` 200–215 行)の受理条件は 4 つある:

1. $f\in[P,P]$、2. hexagon(3.10)、3. hexagon(3.11)、4. 生成 $\langle\bar x^u,(\bar y^u)^f\rangle=P$、
5. **settled 節**(裁定169): $s_1\mapsto s_1^u,\ s_2\mapsto s_2^{u,f}$ が $B_q=E$ の自己準同型に延びること。

**この 5 が (F2) の 1–4 から従わない**(judge のコメント自身がそう述べている)。実測(`t3_f_settled.g`, `t3_g_xiinj.g`):

| 窓 | $v$ 型 | hexagon | +生成 | **+settled $=\lvert\ker\widetilde\chi\rvert$** | $\lvert C_{S_n}(w)\rvert$ | $N$(本稿) |
|---|---|---|---|---|---|---|
| $n=10$、$\varepsilon=0$ | $(9,1)$ | 90 | 54 | **9** | 9 | 6 |
| $n=10$、$\varepsilon=1$ | $(10)$ | **65** | **50** | **10** | 10 | — |
| $n=13$、$\varepsilon=0$ | $(11,1^2)$ | 418 | 132 | **22** | 22 | 6 |

$n=10$、$v=(10)$ の行の $65$ と $50$ は `hexagon_orientation_ruling_v1.md` §1.3 の悉皆値($A_{10}$ 全 $1.8\times10^6$ 元走査)と**完全一致**、$10$ は `sat_l1_v1` §6.1 の実測 $\lvert\ker\rvert=10$ と一致 — **三系統が同じ窓で噛み合う**。

> **⟹ $N=1$ は CENT の十分条件にすぎず、必要条件ではない。** 委嘱文の「【GAP-C1】(剛性 $N=1$・CENT の $\subseteq$ 方向)」という同一視は**訂正を要する**。$N\gg1$ の窓($n=10$ で $N=6$)でも CENT はぴたりと成立している。

---

## 5. 定理 XI-C — settled 節の正体は「$\Xi$ が $C_{S_n}(w)$ に入る」

$m=0$ では $u=2m+1=1$ なので settled 節は「$T:\ s_1\mapsto s_1,\ s_2\mapsto s_2^{\,f}$ が $E=\langle a,b\rangle$ の自己準同型」。生成条件と有限性からこれは**自己同型**である。

> ### 補題 AUT-E【proof】
> $n\ge5$、$n\ne6$ とする。
> $\varepsilon=0$: $E=A_n\times S_3$。$A_n$、$S_3$ はともに直既約・中心自明・互いに非同型なので $\mathrm{Aut}(E)=\mathrm{Aut}(A_n)\times\mathrm{Aut}(S_3)=S_n\times S_3$(共役作用)。
> $\varepsilon=1$: $E=S_n\times_{C_2}S_3=\{(\sigma,\tau):\mathrm{sgn}\,\sigma=\mathrm{sgn}\,\tau\}$。極小正規部分群は $A_n\times1$(非可換単純)と $1\times A_3$(位数 3)で、同型型が違うから任意の $\varphi\in\mathrm{Aut}(E)$ は両方を保つ。$E/(1\times A_3)\cong S_n$、$E/(A_n\times1)\cong S_3$ で、2 つの核の交わりは自明だから $E\hookrightarrow S_n\times S_3$ とこの 2 商への $\varphi$ の作用が $\varphi$ を決める。$\mathrm{Aut}(S_n)=S_n$、$\mathrm{Aut}(S_3)=S_3$(内部)ゆえ $\varphi=(\mathrm{conj}\,\alpha)\times(\mathrm{conj}\,\beta)\vert_E$。∎

$\sigma_1\leftrightarrow(w,\tau_1)$、$\sigma_2\leftrightarrow(v,\tau_2)$、$f\in P=A_n$ は $(f,1)$。よって:

> ### 定理 XI-C【定理】
> $m=0$ の候補 $f$ について
> $$\text{settled}\ \wedge\ \text{生成}\iff \exists\alpha\in S_n:\ \ w^{\alpha}=w\ \ \wedge\ \ v^{\alpha}=v^{\,f}.$$
> このとき $\alpha$ は一意($C_{S_n}(\langle v,w\rangle)=C_{S_n}(\langle a_1,b_1\rangle)=1$、$a_1=wvw$・$b_1=wv$ による)で、$\Xi(f)=\alpha$。したがって
> $$\boxed{\ \Xi(\ker\widetilde\chi)\subseteq C_{S_n}(w)\ }\qquad(\text{全窓・}\varepsilon\text{ 不問}).$$

**これは `sat_l1_v1` 定理 SURV+ の上界 $\Xi(\ker)\subseteq C_{S_n}(\bar x)=C_{S_n}(w^2)$ を強める**(一般に $C(w)\subsetneq C(w^2)$;$n=10$、$w=(10)$ で $10<50$)。定理 CENT-0 は $p=s=0$ でしか両端を閉じられなかったが、**定理 XI-C は $p,s$ を問わず上界を $C(w)$ に落とす**。

**機械確認**(`t3_h_cent.g`・3 窓・$\varepsilon=0$ と $\varepsilon=1$ の両方): 全 shadow で (b) $w^{\Xi(f)}=w$ ✓、**(c) $v^{\Xi(f)}=v^{f}$**(★ 二乗でなく $v$ のレベル)✓、(e) $\Xi$ 像 $=C_{S_n}(w)$ ちょうど ✓。

---

## 6. 定理 XI-INJ — $\Xi$ 単射(5 行)、そして **CENT の定理化**

> ### 定理 XI-INJ【定理・初等・完結】
> $g,h\in S_n$、$g^2=1$、$h^3=1$、$v:=g^{-1}h$、$C_{S_n}(\langle g,h\rangle)=1$ とする。
> $$c\in C_{S_n}(v)\ \wedge\ (cg)^2=1\ \Longrightarrow\ c=1 .$$
> **証明.** $(cg)^2=1$ と $g^2=1$ から $gcg=c^{-1}$、すなわち $c^{\,g}=c^{-1}$、書き換えて $cg=gc^{-1}$。
> $c\in C(v)$、$v=g^{-1}h=gh$ より $c\,gh=gh\,c$;左辺 $=gc^{-1}h$ だから $c^{-1}h=hc$、すなわち $c^{\,h}=c^{-1}$。
> $h^3=1$ より $c=c^{\,h^3}$。ところが $c^{\,h}=c^{-1}$、$c^{\,h^2}=(c^{-1})^{h}=c$、$c^{\,h^3}=c^{-1}$。ゆえに $c=c^{-1}$、$c^2=1$。
> すると $c^{\,g}=c^{-1}=c$、$c^{\,h}=c^{-1}=c$ で $c\in C_{S_n}(\langle g,h\rangle)=1$。∎
> **機械検算**(`t3_g_xiinj.g`): $n=9,10,12$ の 4 種の $v$ について全生成解 × 全 $c\in C(v)$ を悉皆 — **反例 0 件**。

> ### 系 XI-INJ′【定理】
> $\Xi$ は $\ker\widetilde\chi\vert_{m=0}$ 上**単射**。
> **証明.** $\Xi(f)=\Xi(f')=\alpha$ とすると定理 XI-C の (c) より $v^{f}=v^{\alpha}=v^{f'}$、ゆえに $c:=f'f^{-1}\in C_{S_n}(v)$。$g:=fa_1$、$g':=f'a_1=cg$ はともに対合(定理 RED)だから定理 XI-INJ で $c=1$。∎
> (**注**: $\Xi$ の定義だけからは $c\in C(\bar y)=C(v^2)$ しか出ず、$p$ または $s$ が正のとき $C(v^2)\supsetneq C(v)$ で議論が止まる。**$c\in C(v)$ を与えるのが定理 XI-C の (c)**、つまり settled 節が $\bar y$ ではなく $\sigma_2$ のレベルで効くことが要である。)

> ### **定理 CENT**【定理・証明鎖 3 段】
> 命題 0.3 型窓($n\ge5$、$n\ne6$)において
> $$\boxed{\ \ker\widetilde\chi\ \xrightarrow[\ \sim\ ]{\ \Xi\ }\ C_{S_n}(w),\qquad w=b_1^{-1}a_1\ }$$
> **証明.** ① $\Xi(\ker)\subseteq C_{S_n}(w)$(定理 XI-C)。② $\Xi$ 単射(系 XI-INJ′)。③ $C_{S_n}(w)\subseteq\Xi(\ker)$(定理 SURV+、`sat_l1_v1` §10.5.1・$\Xi(f_z)=z^{a_1}$)。$\Xi$ は自己同型の合成に対応するので群準同型、よって群同型。∎
> **⟹ 予想 CENT(`sat_l1_v1` §6・11 窓 machine-measured)は candidate から定理へ。剛性($N$)も飽和も $p=s=0$ の仮定も不要。**

**帰結の棚卸し**(いずれも定理 CENT の直接の系):
- **定理 CENT-ORD**(閉じた位数公式・奇部 $\ell^{\,r-p}$)は candidate から**定理**へ。$\varepsilon=(-1)^{p+s}$ も同様。
- **PRUNE 律の棄却**は「実データによる反証」から「定理による反証」へ格上げ。
- **P-WALL-2 の $\ker\widetilde\chi=C_{19}\times S_5$、W-CENT-B の $162$ は下限でなく等号**。壁の主張($\mathrm{GTSh}$ 非可解)は元々下限だけで立っていたので**無傷のまま強化**。
- **【GAP-C1】は解消**。ただし解消の経路は「剛性 $N=1$」ではなく「settled 節 + $\Xi$ 単射」。**剛性は不要だった。**
- `pruning_law_v2` §5 の **(I) $\Xi$ 単射(未証明・9 窓 measured)は証明済み**に更新すべき。

**格の注意**: 本定理の唯一の外部依存は **judge の受理条件 5 本が Dolgushev の GT-shadow の定義と一致していること**(工房の定義ノートと裁定169 に依る)。定義側の再確認は Sol 監査に回す(§9 の監査点 A)。

---

## 7. 外部定理としての位置づけ(委嘱 3)

**Liu–Osserman(2008, Amer. J. Math. 130)**は genus 0 の **pure-cycle** Hurwitz 空間の既約性(braid 軌道 1 本)を与え、原著は「pure-cycle か genus 0 のどちらかを落とすと多成分例に当たる」と限界を明示している(覚書 §1.1・abstract/§1 のみ参照・本文未読)。

我々の三つ組 $(2^k1^{f_2},\,3^j1^{f_3},\,(\ell,1^t))$ は **第 3 類だけが pure-cycle** で全体は pure-cycle でない。分岐点が 3 個なので **braid 力学は消え**(3 点付き球面の純写像類群は自明)、Nielsen 類 = $C_{S_n}(w_0)$-共役軌道であり、$N$ = その個数。この設定で本稿が得たのは:

> **述べ方(外部向け)**: 種数 0・3 分岐点・分岐データ $(2^k1^{f_2},3^j1^{f_3},(\ell,1^t))$ の**連結被覆の同型類の個数は閉じた式**
> $$\mathrm{Cat}(m-1)\cdot\frac{m!}{t!\,f_2!\,f_3!},\qquad m=t+f_2+f_3-1$$
> **で与えられ、それが 1(= Hurwitz 空間が既約 = 剛)になるのは $\{t,f_2,f_3\}\in\{\{1,1,0\},\{2,1,0\},\{5,0,0\}\}$ のときに限る。**
> 特に $\ell>n/2$ が素数で $3\le t$ なら被覆は自動的に $A_n$/$S_n$-被覆で、**剛な例は $(2^{12},3^8,(19,1^5))$、$n=24$、ただ 1 つ**。

**新規性は断定しない。要 scout。** 具体的な衝突候補を名指ししておく:
1. **平面木・cacti の枚挙**: 「1 本の長巡回 + 不動点」という passport は種数 0 で**平面木の枚挙そのもの**であり、Goulden–Jackson / Tutte / Lagrange 反転の古典圏内。定理 T3-N0 の式は**既知の再発見である可能性が高い**(発案係の見立て「Murnaghan–Nakayama で指標和が閉じる」より、木の全単射の方が短かった)。
2. **Fried の 3-cycle 系**(genus-0 problem・Nielsen 類の連結性)。
3. **Magaard–Völklein の genus-0 生成系分類**($A_n/S_n$ の genus-0 系の分類)— 我々の族はその中に**完全に入っている可能性**がある。
4. **逆 Galois 論の rigid triple カタログ**($A_n$/$S_n$ の剛 3 つ組)— $(2^{12},3^8,(19,1^5))$ が既出かどうかは要確認。$C(w_0)=C_{19}\times S_5\ne1$ なので**古典的な意味の rigid(中心化群自明)ではない** — 我々の $N=1$ は「$C(w_0)$-軌道 1 本」であって "rigidity" の標準定義とは**別物**。この差は覚書 §4 の警戒どおりで、外部に述べるときは必ず区別する。

**【文献要請】(1)**: 上の 4 点、特に「3 分岐点・種数 0・$(2^*,3^*,(\ell,1^t))$ passport の Nielsen 類個数」が既知かどうか。**欲しい結果の型**: (a) prescribed-degree 平面木の枚挙公式の標準出典、(b) $A_n/S_n$ の genus-0 三つ組の分類定理で本族を覆うもの、(c) 「軌道数 1」の既知例カタログ。

---

## 8. 残ギャップ・【文献要請】

### 8.1 名指しの未解決

- **【GAP-T3a】種数 $\ge1$ の $N$ の閉形**。補題 T3-2 で「1 面地図(unicellular map)+ ループ」まで還元済み。あとは prescribed vertex degree の unicellular map の枚挙。
  > **【文献要請】(2)**: **困難** — 頂点次数が $\{1,3\}$(黒)・$\{1,2\}$(白)で指定された**種数 $\gamma$ の 1 面 bipartite map** の(根付き)個数の閉形または漸化式。**欲しい結果の型**: Lehman–Walsh / Goupil–Schaeffer / Chapuy 型の公式、あるいは種数展開($\gamma$ ごとに Catalan の多項式補正)。**正典外なので自分では漁っていない**(文献ゲート遵守)。
- **【GAP-T3b】$t\le2$ / $\ell$ 非素数域**での「$N$ の値」と「生成分の値」の乖離。(J) の外では $N$ は推移類の勘定。実測は §3 に一部あるが体系的でない。
- **【GAP-T3c】$m\ne0$ 層**: 本稿は $m=0$ のみ。定理 XI-C の $u=2m+1$ 版($s_1\mapsto s_1^u$)がどう変わるかは未検討 — `sat_l1_v1` §9.1【GAP-M】と合流する。

### 8.2 定理 CENT の適用限界(正直な申告)

- **$n=6$ を除く**($\mathrm{Aut}(A_6)\ne S_6$ で補題 AUT-E が壊れる)。
- **$P=\langle\bar x,\bar y\rangle=A_n$ の窓に限る**(命題 0.3 型窓では成立)。$P$ が $A_n$ でない一般の $K$ では補題 AUT-E を書き直す必要がある。
- **judge の受理条件 5 本が定義と一致していること**に依存(§6 末尾)。

---

## 9. 検算一覧(GAP 4.16.0・`gap.ps1`・-o 2g)

| スクリプト | SHA-256 | 内容 | 結果 |
|---|---|---|---|
| `search/probe/wac_v1/t3_a_chars.g` | `bb79823c…124ee5` | 完全指標表($S_5$–$S_{22}$)の class multiplication coefficient + 二項反転で $N$ 表 | 種数 0 全行で定理 T3-N0 と一致 |
| `search/probe/wac_v1/t3_b_mn.g` | `2a7b4ced…a007c4` | 自前 Murnaghan–Nakayama($\ell$-weight 1 に制限)で $n\le36$ | 較正 6 件一致・壁 2280 再現・**$n{=}36$ 予言 876960 的中** |
| `search/probe/wac_v1/t3_c_sweep.g` | `73933e4a…4fd02e` | $\ell\in\{5,7,11,13,17,19,23,29\}$、$t\le8$、$n\le34$ の系統掃引 | **種数 0 行 52/52 一致・不一致 0**;(J) 域で $N=1$ は $[19,5,24,12,8]$ のみ |
| `search/probe/wac_v1/t3_d_brute.g` | `8b74e3bd…9a6dad` | 指標を使わない直接列挙(対合悉皆・$C(v)$-軌道明示)+ P-WALL-2 witness の地図復元 | $n=10,13,16$ で一致;**壁の witness が「3 価 3 個の道 + 葉 5 個 + ループ 5 本」= 予言の唯一の木** |
| `search/probe/wac_v1/t3_e_ker.g` | `1bd01e85…19e5f2` | 全射条件 $\langle v^2,gv^2g\rangle=A_n$ の効き目 | 生成分では常に成立(= これは刈らない) |
| `search/probe/wac_v1/t3_f_settled.g` | `d8ae1219…7ce5ec` | judge 実物の 5 条件で $\ker$ を測る | $n{=}10$: 90→54→**9**;$n{=}13$: 418→132→**22** |
| `search/probe/wac_v1/t3_g_xiinj.g` | `9151cdfc…aeb1a8` | 定理 XI-INJ の悉皆検算 + $\varepsilon{=}1$ 窓($v=(10)$) | 反例 **0 件**;$\varepsilon{=}1$ 窓で 65→50→**10** = 工房実測 |
| `search/probe/wac_v1/t3_h_cent.g` | `e878413d…96b512` | 定理 CENT の証明鎖 (a)–(e) の最終検算(3 窓) | 全項目 true・$\Xi$ 像 $=C(w)$ ちょうど |

**単系統(GAP のみ)。cross-checked ではない。Lean verified でもない。** ただし §2.3 の $N$ 表は**完全指標表・自前 MN・直接列挙の 3 実装**が一致しており、§4 の $65/50/10$ は**工房の既存悉皆値**(orientation ruling §1.3・sat_l1_v1 §6.1)と独立に一致する。登録宇宙の掃引ではなく、台帳請求権は発生していない。

---

## 10. Sol への申し送り(相互裏取り用・監査の優先順)

- **監査点 A(最優先)**: **定理 XI-C**。judge の settled 節を「$\mathrm{Aut}(E)$ の元による共役」と読み替えた §5 の 1 段が本稿の要。補題 AUT-E($\varepsilon=1$ の $S_n\times_{C_2}S_3$)を疑ってほしい。ここが崩れると定理 CENT が candidate に戻る。
- **監査点 B**: **定理 XI-INJ**(§6)は 5 行。$c\in C(v)$ が $C(v^2)$ でなく $C(v)$ であること(定理 XI-C (c) 由来)が唯一の外部依存。
- **監査点 C**: 定理 T3-N0 の母関数 $Y=u+z+(\lambda+Y)^2$ — 3 価頂点で「入辺が巡回順序を線形化する」という 1 点だけが幾何的仮定。$n=36$ の予言的中がこの式の非自明な証拠。
- **申し送り**: `sat_l1_v1` §6.2 の $\mathcal F(v)$ 定義(生成条件を $\langle g,h\rangle=\langle a_1,b_1\rangle$ と書いた)は **settled 節を落としているので $\ker$ との全単射にならない**。同ノートの $N$ の役割は「Nielsen 類の勘定」に限定して読み直すべき。

---

## 11. 格付け表

| 主張 | 格 |
|---|---|
| 補題 J(推移 ⟹ 原始 ⟹ $A_n$) | **proof**(古典 Jordan) |
| 補題 T3-1(次数 1 面 = ループ)/ T3-2(1 面地図への還元)/ T3-3($\mathrm{Aut}\mid\gcd(\ell,t)$) | **proof** |
| **定理 T3-N0**($N$ の閉評価・種数 0) | **定理**(全単射 + Lagrange)+ **3 実装 75 行一致・不一致 0**・$n{=}36$ 予言的中 |
| **定理 T3-CLASS**($N=1$ の完全分類) | **定理**(有限場合分け) |
| **系 T3-WALL**(P-WALL-2 の一意性) | **定理**(+ $n\le34$ 掃引で追認) |
| $n=36$ で $N=6$(族は $N=1$ に広がらない) | **反例・予言先行 + 機械** |
| §4 の訂正($N$ は $\lvert\ker\rvert$ を支配しない) | **反証(proof + 悉皆機械)** |
| 補題 AUT-E($\mathrm{Aut}(E)$ の決定) | **proof**($\varepsilon=0$ は古典・$\varepsilon=1$ は本稿 3 行) |
| **定理 XI-C**($\Xi(\ker)\subseteq C_{S_n}(w)$・全窓) | **定理**(補題 AUT-E 依存)+ 3 窓機械 |
| **定理 XI-INJ / 系 XI-INJ′**($\Xi$ 単射) | **定理**(5 行・完結)+ 4 窓悉皆 |
| **定理 CENT**($\ker\widetilde\chi\cong C_{S_n}(w)$) | **定理**(XI-C + XI-INJ + SURV+)。**candidate → 定理**;唯一の外部依存は judge 受理条件 = 定義の一致 |
| 系: CENT-ORD・$\varepsilon=(-1)^{p+s}$ | **candidate → 定理**(定理 CENT の系) |
| 系: PRUNE 律の棄却 | **実データ反証 → 定理による反証** |
| 種数 $\ge1$ の $N$ の閉形 | **UNKNOWN**【文献要請 (2)】 |
| 外部新規性(Liu–Osserman 拡張として初か) | **主張しない・要 scout**(衝突候補 4 件を §7 に名指し) |

---

## 12. 追補ポインタ(2026-07-31・追記のみ・本文は不変)

- **【T3-N0 の $t=0$ 穴】**(Sol 便 90 blocker → 便 91 **F91-1.4** で再掲): §2.2 の母関数証明は「ループ付き黒葉で根付け、最後に $t$ で割る」形なので **$t>0$ しか扱っていない**。
  → **閉鎖済**: `docs/notes/t3_quasi_purecycle_rigidity_v1_addendum_t0.md`(**定理 T3-N0′** = 任意の葉で根付けて $m+1$ で割る一様版。$t=0$ を含む $m\ge2$ の全域で同じ閉形。記号計算 155 件 + 群論ブルート $t=0$ 6 行で不一致 0)。
  旧証明は撤回ではなく**特別な根付けとして吸収**($t\ge1$ で 116 件一致)。
- 本追補は **定理 CENT の格に何も足さない**(CENT は T3 の計数公式に非依存・F91-1.5)。
- **【重み付き修文】**(Sol 便 92 **W92-3** の採択条件・2026-07-31 追記): 本体は「$N$」の 1 記号を **3 つの別の量**(重み付き推移計数 $\mathcal N^{\mathrm w}$ / 無重み推移計数 $\mathcal N^{\mathrm{tr}}$ / 生成計数 $N^{\mathrm{gen}}$)に使っていた。分離・修文・(J) 域での三者一致の証明(**補題 J-AUT**)・$m=1$ 層の穴の閉鎖は
  → `docs/notes/t3_quasi_purecycle_rigidity_v1_addendum_weighted.md`(**系 T3-WALL は無傷**)。
  とくに **§2.3 の表の「$N$(実測)」列は $\mathcal N^{\mathrm w}=T_{\rm trans}/\lvert C\rvert$ と読むこと**($1/3,1/2$ という非整数値がその証拠)。**§0 の ⑥ の「$N=1$」も $\mathcal N^{\mathrm w}=1$ と読む。**
