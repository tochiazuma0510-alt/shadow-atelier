# E1 正典文書 v1 — 中間峰 $\mathrm{GT}^{\rm odd}_{\rm Dih}$(P2)の定義・構造・同値・忠実実現

**状態札: candidate / 研究内部文書**(論文ではない。論文起草は研究者発意事項 — 2026-07-30 確認)
起草: 数学者(Opus 5)/ 2026-07-31 ・ 委嘱 = 地図 P2 行「E1 正典統合の起草」(帯 0/帯 3 の空白欄)
記法: 正典 arXiv **2401.06870**(GTSh の定義正本)/ arXiv **2405.11725**(dihedral 予想 Conj 5.1・$K^{(n)}$ 族・Thm 4.3/4.4/4.6)準拠。工房内の定義正本は `docs/week1-定義ノート.md`。
**封印量・$K^{(5)}$ 非接触。新しい数学は主張しない**(統合と正典化のみ。証明の再構成は既存部品の逐語化であり、出所を各所に併記した)。

---

## 0. この文書の位置づけ

### 0.1 先行文書との差分(**重要 — 二つの E1 がある**)

| 文書 | 射程 | 状態 |
|---|---|---|
| `docs/notes/e1_canonical_v1.md`(2026-07-30・**裁定 226 で検収済**) | 4 点セットの **statement 統合** + 窓族統一表(dihedral/D4/E/PSL)+ 語彙の橋 $\mathrm{Aff}=\mathrm{Hol}$。**「証明の再掲はしない」と明記**(同 §0) | 受理済 |
| **本文書**(`E1_gt_odd_dih_canonical_v1.md`) | 中間峰 $\mathrm{GT}^{\rm odd}_{\rm Dih}$ **単体の正典文書** — 定義から始めて **構造定理・同値定理に完全な証明を付ける**。窓族統一表は扱わない(先行文書に委ねる)。q=7 前線との依存図・格付け表・Lean 化候補を追加 | **本稿** |

地図(第 2.1 版)の帯 0/帯 3 空白欄「E1 正典統合の起草」は、**先行文書が statement 統合までで止まっている**ことを指す。本稿はその欄の残り(証明つき正典化)を埋める。両者は競合せず、先行文書 §3–§4(語彙の橋・窓族統一表)は本稿の射程外である。

### 0.2 本稿が扱う対象

> **中間峰 P2** = dihedral 予想(2405 Conj 5.1)の **odd 側だけを取り出した井原問題**。
> 主張の核は「**有限段の族の全射性**(odd Conj 5.1)と**一本の副有限群への全射性**($\mathrm{Ih}^{\rm odd}$ 全射)が同値」であり、その両辺が計算可能な形($\mathrm{Aff}(\widehat{\mathbb Z}^{\rm odd})\times C_2$)で書けること。

### 0.3 射程外(明示)

- 混合位数($\alpha\ge2$)・2 冪側は本稿の対象外(ただし §5.6 で odd 側との接続点に触れ、未接続を【E1-GAP-3】として名指す)。
- 壁キャンペーン(D4 族・E 族・PSL 窓)は無関係。先行文書 §3–§4 を見よ。
- **正典の定理(Thm 4.3・4.4・4.6・Conj 5.1)は引用する。再証明はしない。**

---

## 1. 定義(正典記法)

以下すべて `docs/week1-定義ノート.md` §1–§3(画像照合済)から引く。式番号は工房の定義ノートの採番(2401 §3 準拠)。

### 1.1 土台

$$B_3=\langle\sigma_1,\sigma_2\mid\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2\rangle,\qquad PB_3=\ker(B_3\to S_3),$$
$$x:=\sigma_1^2,\quad y:=\sigma_2^2,\quad z:=y^{-1}x^{-1},\quad c:=(\sigma_1\sigma_2\sigma_1)^2\ (\text{中心}),\qquad PB_3\cong F_2\times\langle c\rangle,\ \ F_2=\langle x,y\rangle .$$

$\mathrm{NFI}_{PB_3}(B_3):=\{N\trianglelefteq B_3\mid N\le PB_3,\ [B_3:N]<\infty\}$。$N$ に対し
$$N_{\rm ord}:=\mathrm{lcm}\bigl(\mathrm{ord}(xN),\mathrm{ord}(yN),\mathrm{ord}(cN)\bigr)\tag{3.1}$$
$$N_{F_2}:=N\cap F_2 .\tag{3.2}$$

### 1.2 GT-shadow と groupoid $\mathrm{GTSh}$

**GT-pair**(Def 3.1): hexagon 関係 (3.3)(3.4) を $B_3/N$ で満たす $[m,f]=(m+N_{\rm ord}\mathbb Z,\ fN_{F_2})$。
**charming**: $\gcd(2m+1,N_{\rm ord})=1$ かつ $fN_{F_2}\in[F_2/N_{F_2},\,F_2/N_{F_2}]$。
**GT-shadow**(Def 3.7): charming GT-pair であって $T_{m,f}$ が全射なもの。ここで
$$T_{m,f}:B_3\to B_3/N,\qquad \sigma_1\mapsto\sigma_1^{2m+1}N,\quad\sigma_2\mapsto f^{-1}\sigma_2^{2m+1}fN .$$
$\mathrm{GT}(N):=\{\text{target }N\text{ の GT-shadow 全体}\}$、$\mathrm{GTSh}(K,N):=\{[m,f]\in\mathrm{GT}(N)\mid\ker T_{m,f}=K\}$。

**合成**(Thm 3.10・(3.53)):
$$[m_1,f_1]\circ[m_2,f_2]=\bigl[\,2m_1m_2+m_1+m_2,\ f_1E_{m_1,f_1}(f_2)\,\bigr],\qquad E_{m,f}(x)=x^{2m+1},\ E_{m,f}(y)=f^{-1}y^{2m+1}f .$$
**乗法性**(3.49): $\bigl(2m_1+1\bigr)\bigl(2m_2+1\bigr)=2(2m_1m_2+m_1+m_2)+1$。単位元 $[0,1]$。

**settled**: $\ker T_{m,f}=N$。**isolated**: $N$ を target とする全 shadow が settled。
$$\textbf{isolated}\ \Longrightarrow\ \mathrm{GT}(N)=\mathrm{GTSh}(N,N)\ \text{は (3.53) を積とする\textbf{有限群}}\quad(\text{Prop 3.14}).$$

**reduction**(3.60): $N\le H$ のとき $R_{N,H}:\mathrm{GT}(N)\to\mathrm{GT}(H)$、$[m,f]\mapsto(m+H_{\rm ord}\mathbb Z,\ fH_{F_2})$。両者 isolated なら群準同型。
**Main Line 関手** $\mathrm{ML}:N\mapsto\mathrm{GT}(N)$(isolated poset 上)。2401 Thm 5.2: $\widehat{GT}_{\rm gen}\cong\varprojlim\mathrm{ML}$。

### 1.3 Ihara 側

$\chi:G_{\mathbb Q}\to\widehat{\mathbb Z}^\times$ を円分指標とし(2405 (1.5)・画像照合 `docs/notes/照合_Ih定義_P1.md`)
$$\mathrm{Ih}(g):=\Bigl(\tfrac{\chi(g)-1}{2},\ f_g\Bigr)\in\widehat{\mathbb Z}\times\widehat F_2,\qquad \mathrm{Ih}:G_{\mathbb Q}\hookrightarrow\widehat{GT}\subseteq\widehat{GT}_{\rm gen},$$
$$\mathrm{Ih}_N:=\mathcal{PR}_N\circ\mathrm{Ih}:G_{\mathbb Q}\longrightarrow\mathrm{GT}(N)\tag{1.11}$$
$$\mathrm{GT}_{\rm arith}(N):=\mathrm{Ih}_N(G_{\mathbb Q}) .\tag{1.12}$$
shadow が **arithmetical** $:\iff$ $\mathrm{GT}_{\rm arith}(N)$ に属する。**genuine** $:\iff$ $\mathcal{PR}_N(\widehat{GT}_{\rm gen})$ に属する。arithmetical $\Rightarrow$ genuine。

> **⚠ 型の注意(2405 Remark 1.4・画像照合済)**: $N$ が isolated でないとき $\mathrm{GT}(N)$ に自然な群構造がなく、**$\mathrm{Ih}_N$ は群準同型ではない**。「$\mathrm{Ih}_N$ は準同型」と書いてよいのは isolated のときだけ。

### 1.4 dihedral poset

$D_n=\langle r,s\mid r^n,s^2,srs^{-1}r\rangle$(位数 $2n$)、$n\ge3$。
$$\psi_n:PB_3\to D_n^3,\qquad x\mapsto(r,s,s),\quad y\mapsto(rs,r,rs),\quad c\mapsto(1,1,1)\tag{3.1$_{2405}$}$$
$$K^{(n)}:=\ker\psi_n\in\mathrm{NFI}_{PB_3}(B_3)\ (\text{Prop 3.1}),\qquad G_n:=\mathrm{Im}\,\psi_n\cong PB_3/K^{(n)}\cong F_2/K^{(n)}_{F_2},$$
$$\mathrm{Dih}:=\{K^{(n)}\mid n\ge3\},\qquad K^{(n)}_{\rm ord}=\mathrm{lcm}(n,2) .$$
$X:=\psi_n(x)$、$Y:=\psi_n(y)$。**Prop 3.4**: $n$ 奇 $\Rightarrow K^{(n)}=K^{(2n)}$。**Prop 3.5**: $K^{(q)}\subseteq K^{(n)}\iff n\mid\mathrm{lcm}(q,2)$。

**正典 Thm 4.3**(較正ゲートの正解): $\mathcal X_n:=\{m\in\{0,\dots,K^{(n)}_{\rm ord}-1\}\mid\gcd(2m+1,K^{(n)}_{\rm ord})=1\}$、
$$\varkappa(m):=\begin{cases}m+1&(m\ \text{奇})\\-m&(m\ \text{偶})\end{cases}\tag{4.9}$$
$$\mathrm{GT}(K^{(n)})=\bigl\{(m,\ (r^{2k},r^{-2k},r^{\varkappa(m)}))\ \big|\ m\in\mathcal X_n,\ k\in\mathbb Z\bigr\}\quad(\textbf{4}\mid n\ \text{のときのみ追加条件}\ k\equiv\varkappa(m)/2\ (2))\tag{4.12}$$
**かつ $K^{(n)}$ は $\mathrm{GTSh}$ の isolated object**(Lemma 4.2 / Thm 4.3 末尾)。

**正典 Thm 4.4**: $K^{(q)}\le K^{(n)}$ のとき $R_{K^{(q)},K^{(n)}}$ は**全射**。
**正典 Thm 4.6**($n=2^\alpha n_0$、$n_0$ 奇):
$$\mathrm{GT}(K^{(n)})\cong\begin{cases}\mathrm{Aff}(\mathbb Z/n_0\mathbb Z)\times\mathcal Z_2&(\alpha\le1)\\ \mathrm{Aff}(\mathbb Z/n_0\mathbb Z)\times\widetilde H_\alpha&(\alpha\ge2)\end{cases}\qquad
\lvert\mathrm{GT}(K^{(n)})\rvert=\begin{cases}2n_0\varphi(n_0)&(\alpha\le1)\\ n_0\varphi(n_0)2^{2\alpha-2}&(\alpha\ge2)\end{cases}\tag{4.23}$$
**正典 Conj 5.1**(dihedral 予想・p.23 画像照合済): $\mathrm{Dih}$ の全対象 $K$ で全 GT-shadow が arithmetical、すなわち $\mathrm{Ih}_K:G_{\mathbb Q}\to\mathrm{GTSh}(K,K)$ が全射。**証明済みは $n=2^\alpha$($\alpha\ge2$)のみ**(Thm 5.3)。

### 1.5 **odd 窓族**(本稿の対象の定義)

> ### 定義 E1-D1(odd 窓族)
> $$\boxed{\ \mathrm{Dih}^{\rm odd}:=\{K^{(n)}\mid n\ \text{奇},\ n\ge3\}\ \subseteq\ \mathrm{Dih}\ }$$

> ### 補題 E1-D2(正規化代表と順序)
> 1. $\mathrm{Dih}^{\rm odd}$ は $\mathrm{Dih}$ のうち $\alpha\le1$ の対象全体に一致する($n=2^\alpha n_0$、$\alpha\le1$ $\Rightarrow$ $K^{(n)}=K^{(n_0)}$、$n_0$ 奇 $\ge3$)。
> 2. $n\mapsto K^{(n)}$ は $\{n\ \text{奇}\ge3\}$ から $\mathrm{Dih}^{\rm odd}$ への**全単射**。
> 3. 奇 $q,n\ge3$ に対し $K^{(q)}\subseteq K^{(n)}\iff n\mid q$。ゆえに $\mathrm{Dih}^{\rm odd}$ 上の poset 順序は**整除順序そのもの**であり、$\mathrm{lcm}$ で**有向**である。

**証明.** (1) $\alpha=0$ は自明。$\alpha=1$ なら $n=2n_0$ で $n\ge3$ より $n_0\ge3$($n_0=1$ なら $n=2<3$ で対象外)、Prop 3.4 より $K^{(2n_0)}=K^{(n_0)}$。逆に $\alpha\ge2$ の対象は $K^{(n)}_{\rm ord}=n$ が $4$ で割れるので、$K^{(m)}_{\rm ord}=2m$($m$ 奇)と一致しえない。
(3) Prop 3.5 で $q$ 奇なら $\mathrm{lcm}(q,2)=2q$ ゆえ $K^{(q)}\subseteq K^{(n)}\iff n\mid 2q$。$n$ 奇と $\gcd(n,2)=1$ から $n\mid2q\iff n\mid q$。
(2) (3) と反対称性: $K^{(q)}=K^{(n)}\iff n\mid q$ かつ $q\mid n\iff q=n$。有向性は $\mathrm{lcm}(q,n)$ が奇 $\ge3$ であることから。∎

> ### 定義 E1-D3($\mathrm{GT}^{\rm odd}_{\rm Dih}$ と $\mathrm{Ih}^{\rm odd}$)
> $$\boxed{\ \mathrm{GT}^{\rm odd}_{\rm Dih}:=\varprojlim_{n\ \text{奇}\ \ge3}\mathrm{GT}(K^{(n)})=\varprojlim\bigl(\mathrm{ML}\big|_{\mathrm{Dih}^{\rm odd}}\bigr)\ }$$
> (遷移写像 $=$ reduction $R_{K^{(n)},K^{(d)}}$、$d\mid n$)。さらに
> $$\mathrm{Ih}^{\rm odd}:=\bigl(\mathrm{Ih}_{K^{(n)}}\bigr)_{n}\ :\ G_{\mathbb Q}\longrightarrow\mathrm{GT}^{\rm odd}_{\rm Dih}.$$

> **記法規約**(誤読事故を受けた規約・Sol 同調済・先行文書 §6): 正式表記は **`GT^odd` ではなく `GT^odd_Dih`**(dihedral 窓族由来の限定子を保持)。引用元の原文(便 75 等)には `GT^odd` 表記が残る。

**$\mathrm{Ih}^{\rm odd}$ の well-defined 性**は §3.1 の補題 E1-3a/3b で示す(自明ではない — isolated 性と reduction 整合の両方を使う)。

---

## 2. 構造定理 — $\mathrm{GT}^{\rm odd}_{\rm Dih}\cong\mathrm{Aff}(\widehat{\mathbb Z}^{\rm odd})\times C_2$

$\mathrm{Aff}(R):=R\rtimes R^\times$($(k_1,u_1)(k_2,u_2)=(k_1+u_1k_2,\ u_1u_2)$)、$\widehat{\mathbb Z}^{\rm odd}:=\prod_{p\ne2}\mathbb Z_p$。

### 2.1 有限段の自然座標

> ### 命題 E1-S1(自然座標・**便 75 §F6.2(b) の逐語化**)
> $n\ge3$ を奇数とする。$\mathrm{GT}(K^{(n)})$ の元 $[m,f]$ を Thm 4.3 (4.12) の座標 $(m,k)$ で表し
> $$u:=2m+1\bmod n,\qquad \varepsilon:=m\bmod2$$
> と置く。このとき
> $$\Theta_n:\ \mathrm{GT}(K^{(n)})\ \xrightarrow{\ \sim\ }\ \mathrm{Aff}(\mathbb Z/n\mathbb Z)\times C_2,\qquad [m,f]\longmapsto(k,\ u,\ \varepsilon)$$
> は**群同型**であり、外部 $C_2$ 成分は $\chi_4([m,f])=2m+1\bmod4$ に対応する。とくに $\lvert\mathrm{GT}(K^{(n)})\rvert=2n\varphi(n)$。

**証明.** $n$ 奇より $K^{(n)}_{\rm ord}=\mathrm{lcm}(n,2)=2n$、また $4\nmid n$ なので (4.12) の追加条件は発動しない。

**(a) 座標の忠実性.** (4.12) より shadow は $(m,k)$、$m\in\mathcal X_n\subseteq\mathbb Z/2n$、$f$ の $G_n$ での値は $(r^{2k},r^{-2k},r^{\varkappa(m)})$。$\mathrm{ord}(r)=n$ と $n$ 奇($2\in(\mathbb Z/n)^\times$)より $r^{2k}$ は $k\bmod n$ で決まり、逆に $k$ を復元する。よって $k\in\mathbb Z/n$ が well-defined。第 3 成分 $r^{\varkappa(m)}$ は $m$ の関数なので独立自由度ではない。

**(b) $m\leftrightarrow(u,\varepsilon)$.** $2$ は $\bmod\ n$ で可逆だから $m\mapsto 2m+1\bmod n$ は $\mathbb Z/n\to\mathbb Z/n$ の全単射。$n$ 奇ゆえ CRT で $\mathbb Z/2n\cong\mathbb Z/n\times\mathbb Z/2$、$m\mapsto(m\bmod n,\ m\bmod2)\mapsto(u,\varepsilon)$ は全単射。

**(c) charming 条件.** $\gcd(2m+1,2n)=1$。$2m+1$ は奇だから $\gcd(2m+1,2)=1$、よって条件は $\gcd(2m+1,n)=1$、すなわち $u\in(\mathbb Z/n)^\times$ と同値。ゆえに $\mathcal X_n\xrightarrow{\sim}(\mathbb Z/n)^\times\times\mathbb Z/2$、$\lvert\mathcal X_n\rvert=2\varphi(n)=\varphi(4n)$。(a)(b)(c) より $\Theta_n$ は集合として全単射で $\lvert\mathrm{GT}(K^{(n)})\rvert=n\cdot2\varphi(n)=2n\varphi(n)$。

**(d) 積.** $[m_1,f_1]\circ[m_2,f_2]$ の第一成分は $m=2m_1m_2+m_1+m_2$ である。
* $u$: (3.49)$=$(4.19) の**整数恒等式** $2m+1=(2m_1+1)(2m_2+1)$ を $\bmod\ n$ で読んで $u=u_1u_2$。
* $\varepsilon$: $2m_1m_2$ は偶だから $m\equiv m_1+m_2\ (2)$、すなわち $\varepsilon=\varepsilon_1+\varepsilon_2$。
* $k$: (4.18) が $\psi_n\bigl(f_1E_{m_1,f_1}(f_2)\bigr)=\bigl(r^{2(k_1+u_1k_2)},\ r^{-2(k_1+u_1k_2)},\ r^{\varkappa(m_1)+\varkappa(m_2)-2\varkappa(m_1)\varkappa(m_2)}\bigr)$、$u_1=2m_1+1$ を与える。第 3 成分は (4.20) により $r^{\varkappa(m)}$ に一致する(第 3 成分が $m$ の関数として整合することの正典側の保証)。ゆえに $k=k_1+u_1k_2\bmod n$。

したがって
$$(k_1,u_1,\varepsilon_1)\cdot(k_2,u_2,\varepsilon_2)=(k_1+u_1k_2,\ u_1u_2,\ \varepsilon_1+\varepsilon_2)$$
であり、これは $\mathrm{Aff}(\mathbb Z/n)\times C_2$ の積そのもの。単位元 $[0,1]\mapsto(0,1,0)$。∎

> **$\chi_4$ との対応**(便 75 F6.1(b)): $2m+1\equiv(-1)^m\ (\bmod\ 4)$ なので $\varepsilon=m\bmod2$ は $\chi_4([m,f])=2m+1\bmod4$ と同じ情報。$K^{(n)}_{\rm ord}=2n$ が偶数であることが $m\bmod2$ の well-defined 性を保証する(奇 $n$ でのみ成立)。

> **正典 Thm 4.6 との関係**: (4.23) の $\alpha\le1$ 分岐($n_0=n$)は $\mathrm{Aff}(\mathbb Z/n)\times\mathcal Z_2$ を主張する。命題 E1-S1 はその同型を**自然に**($\bmod$ の取り方だけで)構成したものである。**正典の同型は非自然な直積分解の選択を含む**(便 75 F7.3 が指摘し、有限段 API をこの座標にすることを提案)。以下で逆極限を取るには自然性が要る。

> **⚠ Thm 4.6 の再証明ではない**: 命題 E1-S1 は (4.12)(4.18)(4.19)(4.20) を**入力として**使う。これらは正典の定理であり、本稿は引用する。

> ### 命題 E1-S2(遷移写像の成分性 — **自然性**)
> 奇 $d\mid n$($d\ge3$)に対し、$\Theta$ による同一視の下で
> $$R_{K^{(n)},K^{(d)}}\ :\ (k,u,\varepsilon)\ \longmapsto\ (k\bmod d,\ u\bmod d,\ \varepsilon)$$
> すなわち遷移写像は**成分ごとの還元**であり、$C_2$ 成分を捻らない。

**証明.** (3.60) より $R([m,f])=(m\bmod K^{(d)}_{\rm ord},\ fK^{(d)}_{F_2})=(m\bmod 2d,\ \cdot)$。
* $u$: $2m+1\bmod d$ は $u=2m+1\bmod n$ の $\bmod\ d$ 還元($d\mid n$)。
* $\varepsilon$: $2\mid 2d$ なので $m\bmod2$ は $m\bmod2d$ から復元でき、値は不変。
* $k$: $f$ の $G_d$ での値は $G_n$ での値の像であり、$A_n=(\mathbb Z/n)^3\twoheadrightarrow(\mathbb Z/d)^3$ の下で $r^{2k}\mapsto r_d^{2k}$、すなわち $k\mapsto k\bmod d$。∎

> **系 E1-S2′(reduction 全射性の座標的再導出)**: $d\mid n$ 奇に対し $\mathbb Z/n\twoheadrightarrow\mathbb Z/d$ と $(\mathbb Z/n)^\times\twoheadrightarrow(\mathbb Z/d)^\times$ はともに全射だから、$R_{K^{(n)},K^{(d)}}$ は全射。これは**正典 Thm 4.4 の odd 部分の独立再導出**である(正典の証明は CRT による lift 構成; 本系は座標の成分性から直ちに出る)。

### 2.2 逆極限

> ### 補題 E1-S3(分裂系の極限)
> 有向 poset $I$ 上の有限群の逆系 $\{A_i\rtimes Q_i\}$ で、遷移写像が $A$-部分と $Q$-部分をそれぞれ保つ(すなわち分裂を保つ)ならば
> $$\varprojlim(A_i\rtimes Q_i)=\bigl(\varprojlim A_i\bigr)\rtimes\bigl(\varprojlim Q_i\bigr).$$

**証明.** 逆極限は台集合の上で計算され、$\prod A_i\rtimes\prod Q_i$ の中の整合列全体は $(\varprojlim A_i)\rtimes(\varprojlim Q_i)$ に一致する(分裂を保つので $A$-成分と $Q$-成分が独立に整合条件を満たす)。積の式も成分ごと。∎

> ### 補題 E1-S4(単数群の極限)
> 有限可換環の逆系 $\{R_i\}$(遷移は環準同型)に対し $\varprojlim(R_i^\times)=(\varprojlim R_i)^\times$。

**証明.** $(\varprojlim R_i)^\times\subseteq\varprojlim(R_i^\times)$ は明らか。逆に各成分が単元なら逆元の族は(逆元の一意性より)整合し、極限の元の逆元を与える。∎

> ### 定理 E1-2(構造定理)
> $$\boxed{\ \mathrm{GT}^{\rm odd}_{\rm Dih}\ \cong\ \mathrm{Aff}\bigl(\widehat{\mathbb Z}^{\rm odd}\bigr)\times C_2\ ,\qquad \widehat{\mathbb Z}^{\rm odd}=\prod_{p\ne2}\mathbb Z_p .}$$

**証明.** 補題 E1-D2(3) より添字系は $\{n\ \text{奇}\ge3\}$ を整除順序で有向にしたもの。命題 E1-S1・E1-S2 より逆系 $\{\mathrm{GT}(K^{(n)})\}$ は逆系 $\{\mathrm{Aff}(\mathbb Z/n)\times C_2\}$(遷移 $=$ 成分還元・$C_2$ は恒等)と**自然に同型**である。逆極限は有限積と可換だから
$$\mathrm{GT}^{\rm odd}_{\rm Dih}\cong\Bigl(\varprojlim_n\mathrm{Aff}(\mathbb Z/n)\Bigr)\times\Bigl(\varprojlim_n C_2\Bigr).$$
第 2 因子: 遷移が恒等の定数系ゆえ $C_2$(便 75 F6.2(c))。
第 1 因子: 遷移は分裂 $\mathbb Z/n\rtimes(\mathbb Z/n)^\times$ を保つので補題 E1-S3 が適用でき、補題 E1-S4 と
$$\varprojlim_{n\ \text{奇}}\mathbb Z/n\mathbb Z=\prod_{p\ne2}\mathbb Z_p=\widehat{\mathbb Z}^{\rm odd}$$
(奇数全体は整除順序で $\prod_{p\ne2}p^{k}$ を cofinal に含む)より
$$\varprojlim_n\mathrm{Aff}(\mathbb Z/n)=\widehat{\mathbb Z}^{\rm odd}\rtimes(\widehat{\mathbb Z}^{\rm odd})^\times=\mathrm{Aff}(\widehat{\mathbb Z}^{\rm odd}).\qquad\blacksquare$$

> **出所**: 結論式・$C_2$ の定数系論法は **便 75 §F6.2(b)(c)**(裁定 111 で受理)。補題 E1-S3/S4 と補題 E1-D2 は本稿が明示化した初等段(便 75 は「従って」で通している箇所)。**新しい定理ではなく、既存主張の前件を全部書き出したもの。**

> **系 E1-2a(位数の系列)**: $\lvert\mathrm{GT}(K^{(n)})\rvert=2n\varphi(n)$($n$ 奇)。$n=3,5,7,9,11,15,21,25$ で $12,40,84,108,220,240,504,1000$。**正典 Thm 4.6 と一致**(定義ノート §3・C-4 の cross-checked 証明書 17 通)。

> **検算(証明とは独立・整数演算のみ)**: `scratchpad/e1_coord_check.py`(本稿起草時に実行)で $n=3,5,7,9,11,15,21,25$ の 8 点について ①$\Theta_n$ の全単射性 ②積が $\mathrm{Aff}\times C_2$ の積になること(全 shadow 対) ③(4.20) の $\varkappa$ 恒等式 ④命題 E1-S2 の成分性(全約数対)を確認、**8/8 ALL PASS**。**これは証明の cross-check であって証明ではない**(単系統・スクラッチ)。

---

## 3. 同値定理 — odd Conj 5.1 $\iff$ $\mathrm{Ih}^{\rm odd}$ 全射

### 3.1 $\mathrm{Ih}^{\rm odd}$ の well-defined 性

> ### 補題 E1-3a($\mathrm{Ih}_{K^{(n)}}$ は群準同型)
> $n$ 奇 $\ge3$。$K^{(n)}$ は isolated(**E1-1** $=$ 正典 Lemma 4.2/Thm 4.3)だから $\mathrm{GT}(K^{(n)})=\mathrm{GTSh}(K^{(n)},K^{(n)})$ は有限群であり、$\mathrm{Ih}_{K^{(n)}}:G_{\mathbb Q}\to\mathrm{GT}(K^{(n)})$ は**連続群準同型**である。

**証明.** 群であることは Prop 3.14。準同型性は 2405 Remark 1.4 の対偶(isolated なら準同型)。連続性: $\mathrm{Ih}$ は連続、$\mathcal{PR}_{K^{(n)}}$ は $\widehat{\mathbb Z}\times\widehat F_2\to\mathbb Z/2n\times F_2/K^{(n)}_{F_2}$ の還元で連続、合成は連続。有限離散な終域ゆえ $\ker$ は開。∎

> **⚠ E1-1 の効き所(1)**: isolated 性がないと $\mathrm{Ih}_{K^{(n)}}$ は準同型ですらなく、**「全射」を群論の言葉で扱う土台が消える**。E1-1 は 4 点セットの「一つ目」ではなく**土台**である。

> ### 補題 E1-3b(reduction 整合)
> 奇 $d\mid n$($d\ge3$)に対し $R_{K^{(n)},K^{(d)}}\circ\mathrm{Ih}_{K^{(n)}}=\mathrm{Ih}_{K^{(d)}}$。

**証明.** $\mathrm{Ih}_{K^{(n)}}=\mathcal{PR}_{K^{(n)}}\circ\mathrm{Ih}$、$\mathcal{PR}_N(\hat m,\hat f)=(\hat m\bmod N_{\rm ord},\ \hat fN_{F_2})$、$R_{N,H}([m,f])=(m\bmod H_{\rm ord},\ fH_{F_2})$。$K^{(d)}_{\rm ord}=2d\mid2n=K^{(n)}_{\rm ord}$ と $K^{(n)}_{F_2}\subseteq K^{(d)}_{F_2}$(補題 E1-D2(3))より $R_{K^{(n)},K^{(d)}}\circ\mathcal{PR}_{K^{(n)}}=\mathcal{PR}_{K^{(d)}}$。∎

> **系 E1-3c**: $\mathrm{Ih}^{\rm odd}=(\mathrm{Ih}_{K^{(n)}})_n:G_{\mathbb Q}\to\mathrm{GT}^{\rm odd}_{\rm Dih}$ は well-defined な**連続群準同型**である。

> ### 補題 E1-3d(射影の全射性)
> 各 $n$ 奇 $\ge3$ に対し $\mathrm{pr}_n:\mathrm{GT}^{\rm odd}_{\rm Dih}\to\mathrm{GT}(K^{(n)})$ は全射。

**証明.** 遷移写像は全射(正典 Thm 4.4;odd 部分は系 E1-S2′ で独立再導出済)。有向 poset 上の有限群(空でないコンパクト空間)の逆系で遷移が全射なら、逆極限の射影は全射である(標準)。∎

### 3.2 主定理

> ### 定理 E1-3(同値定理)
> 次は同値である。
> **(i) [odd Conjecture 5.1]** すべての奇 $n\ge3$ で、target $K^{(n)}$ の全 GT-shadow が arithmetical。すなわち $\mathrm{Ih}_{K^{(n)}}:G_{\mathbb Q}\to\mathrm{GT}(K^{(n)})=\mathrm{GTSh}(K^{(n)},K^{(n)})$ が**全射**。
> **(ii)** $\mathrm{Ih}^{\rm odd}:G_{\mathbb Q}\to\mathrm{GT}^{\rm odd}_{\rm Dih}$ が**全射**。
> $$\boxed{\ \text{odd Conjecture 5.1}\iff \mathrm{Ih}^{\rm odd}\ \text{が全射}\ }$$

**証明.**

**(ii) $\Rightarrow$ (i).** 補題 E1-3b より $\mathrm{Ih}_{K^{(n)}}=\mathrm{pr}_n\circ\mathrm{Ih}^{\rm odd}$。補題 E1-3d より $\mathrm{pr}_n$ は全射。よって
$$\mathrm{GT}_{\rm arith}(K^{(n)})=\mathrm{pr}_n\bigl(\mathrm{Im}\,\mathrm{Ih}^{\rm odd}\bigr)=\mathrm{pr}_n\bigl(\mathrm{GT}^{\rm odd}_{\rm Dih}\bigr)=\mathrm{GT}(K^{(n)}).$$

**(i) $\Rightarrow$ (ii).** $A:=\mathrm{Im}\,\mathrm{Ih}^{\rm odd}\le\mathrm{GT}^{\rm odd}_{\rm Dih}$ と置く。

*(a) $A$ は閉.* $G_{\mathbb Q}$ は副有限ゆえコンパクト、$\mathrm{Ih}^{\rm odd}$ は連続(系 E1-3c)、よって $A$ はコンパクト。$\mathrm{GT}^{\rm odd}_{\rm Dih}$ は有限離散群の逆極限ゆえ Hausdorff、したがって $A$ は閉。

*(b) $A$ は稠密.* $g\in\mathrm{GT}^{\rm odd}_{\rm Dih}$ とその基本開近傍
$$U=\{h\mid \mathrm{pr}_{n_i}(h)=\mathrm{pr}_{n_i}(g),\ i=1,\dots,r\}$$
を取る(逆極限位相の基本開集合は**有限個の段しか指定しない**)。$N:=\mathrm{lcm}(n_1,\dots,n_r)$ は奇 $\ge3$ で各 $n_i\mid N$。(i) より $\mathrm{Ih}_{K^{(N)}}$ は全射だから、$\gamma\in G_{\mathbb Q}$ を $\mathrm{Ih}_{K^{(N)}}(\gamma)=\mathrm{pr}_N(g)$ に取れる。補題 E1-3b より各 $i$ で
$$\mathrm{pr}_{n_i}\bigl(\mathrm{Ih}^{\rm odd}(\gamma)\bigr)=R_{K^{(N)},K^{(n_i)}}\bigl(\mathrm{Ih}_{K^{(N)}}(\gamma)\bigr)=R_{K^{(N)},K^{(n_i)}}\bigl(\mathrm{pr}_N(g)\bigr)=\mathrm{pr}_{n_i}(g),$$
すなわち $\mathrm{Ih}^{\rm odd}(\gamma)\in U\cap A$。

*(c)* 閉かつ稠密 $\Rightarrow$ $A=\mathrm{GT}^{\rm odd}_{\rm Dih}$。$\blacksquare$

> ### ⚠ 前件の明記(**便 75 §F6.2(d) 原文**)
> 「ここで必要なのは**全有限段の arithmetic surjectivity** であり、**遷移写像の全射性だけから Galois 像の全射性が出るわけではない**。」
> 実際 (b) は「lcm 段の $\mathrm{Ih}_{K^{(N)}}$ が全射」を各回使う。遷移が全射なだけでは、$A$ の像が各段で真部分群にとどまる可能性を排除できない。

> ### 系 E1-3e(有限段への帰着の限界)
> (i) は**全奇数 $n$** についての量化である。「全奇素数冪 $n=p^e$ で全射」からは (i) は従わない — 合成には entanglement の制御が要る(【E1-GAP-2】§5.6)。

> ### 注(genuine 側との差)
> 定理 E1-3 は **arithmetical**(Galois 側)についての言明である。**genuine** 側、すなわち $\mathcal{PR}^{\rm odd}:\widehat{GT}_{\rm gen}\to\mathrm{GT}^{\rm odd}_{\rm Dih}$ の全射性は別の主張であり、本稿の射程外(【E1-GAP-4】)。arithmetical $\Rightarrow$ genuine より (ii) $\Rightarrow$ $\mathcal{PR}^{\rm odd}$ 全射は従うが、逆は不明。

---

## 4. 4 点セット(裁定 226 の statement 群)

裁定 226 で統合が受理され、`provenance/CLAIMS.md` §「GT^odd_Dih 4 点セット」に遡及登録された 4 主張。本節はその**正典化された statement** を置き、§2–§3 で証明した 2 本(E1-2/E1-3)については証明の所在を指す。

> ### 【E1-1】isolated(**正典の定理**)
> すべての $n\ge3$ で $K^{(n)}$ は $\mathrm{GTSh}$ の isolated object(2405 Lemma 4.2 / Thm 4.3 末尾・画像照合済)。ゆえに
> $$\mathrm{GT}(K^{(n)})=\mathrm{GTSh}(K^{(n)},K^{(n)})\ \text{は有限群}.$$
> **状態: 正典の定理**(工房の主張ではない)。
> **⚠ Sol 注記**(定義ノート §3): $\mathrm{GTSh}(K,K)=\mathrm{GT}(K)$ と書けるのは Thm 4.3 が $K\in\mathrm{Dih}$ の isolated 性を証明しているからであり、**一般の $N$ に安易に一般化してはならない**。

> ### 【E1-2】構造 — 本稿 §2(定理 E1-2)
> 有限段: $\mathrm{GT}(K^{(n)})\cong\mathrm{Aff}(\mathbb Z/n)\times C_2$(**自然座標**・命題 E1-S1)。
> 極限: $\mathrm{GT}^{\rm odd}_{\rm Dih}\cong\mathrm{Aff}(\widehat{\mathbb Z}^{\rm odd})\times C_2$。

> ### 【E1-3】同値 — 本稿 §3(定理 E1-3)
> odd Conjecture 5.1 $\iff$ $\mathrm{Ih}^{\rm odd}$ 全射。

> ### 【E1-4】忠実実現(**framed 対象上**・型修理済)
> **(a) 有限段(命題 Φ-fam)**: $n$ 奇 $\ge3$、$G_n=A\rtimes Q$($A\cong(\mathbb Z/n)^3$、$Q\cong C_2^2$;ODD-H 補題 A)。$[m,f]\in\mathrm{GT}(K^{(n)})$ に対し $u:=2m+1$、$F:=\psi_n(f)$ とし
> $$\Phi_{m,f}:G_n\to G_n,\qquad X\mapsto X^{u},\quad Y\mapsto F^{-1}Y^{u}F$$
> と置く。このとき $\Phi_{m,f}\in\mathrm{Aut}(G_n)$ であり、
> $$\Phi_n:\mathrm{GT}(K^{(n)})\longrightarrow\mathrm{Aut}(G_n),\qquad[m,f]\mapsto\Phi_{m,f}$$
> は**共変**な($\Phi_{g_1\circ g_2}=\Phi_{g_1}\circ\Phi_{g_2}$)**単射**群準同型で $\ker\Phi_n=\{[0,1]\}$。
> **(b) 極限**: $\Phi^{\rm odd}:\mathrm{GT}^{\rm odd}_{\rm Dih}\hookrightarrow\mathrm{Aut}_{\rm cont}(G^{\rm odd})$、$G^{\rm odd}=\varprojlim G_n=(\widehat{\mathbb Z}^{\rm odd})^3\rtimes Q$。
> **(c) 対象の型(便 77 F77-3.6・裁定 138 で採択)**: 結論を「marked dessin の自己同型」と幾何語で書くのは不正確。正しくは
> $$\text{$G^{\rm odd}$ と、その compatible ordered generating-pair(framing)の \textbf{torsor} 上の忠実な連続作用}$$
> であり、codomain も抽象 $\mathrm{Aut}$ でなく $\mathrm{Aut}_{\rm cont}$ と書く。

**(a) の証明**(`docs/notes/phifam_v1.md` §2–§3 の逐語化・便 77 F77-3.1〜3.3 の修理反映)。

*自己同型性.* $[m,f]$ が GT-shadow なら $T_{m,f}$ は全射(Def 3.7)。**さらに $K^{(n)}$ が isolated(E1-1)だから $\ker T^{F_2}_{m,f}=K^{(n)}_{F_2}$**、よって $T^{F_2}_{m,f}$ は有限群 $G_n=F_2/K^{(n)}_{F_2}$ の**自己**全射準同型に降り、有限性から単射、すなわち自己同型。
> **⚠ E1-1 の効き所(2)・便 77 F77-3.3 の訂正**: `phifam_v1.md` 旧 FINDING Φ3 の「$\mathrm{Aut}$ 性に isolated 不要」は**誤りとして撤回済**(裁定 138)。Def 3.7 が与えるのは $F_2\to F_2/K^{(n)}_{F_2}$ の全射であって、その核は一般には別の source $K'$ でありうる。$G_n$ の**自己**写像へ降ろすのに settled 性が要る。正しい依存順は
> $$\text{Thm 4.3 (settled)}\Longrightarrow T:G_n\twoheadrightarrow G_n\Longrightarrow T\in\mathrm{Aut}(G_n).$$

*共変性.* $y$ 上で
$$T_1(T_2(y))=T_1(f_2^{-1}y^{u_2}f_2)=E_1(f_2)^{-1}\bigl(f_1^{-1}y^{u_1}f_1\bigr)^{u_2}E_1(f_2)=\bigl(f_1E_1(f_2)\bigr)^{-1}y^{u_1u_2}\bigl(f_1E_1(f_2)\bigr),$$
$x$ 上で $T_1(T_2(x))=x^{u_1u_2}$。(3.49) より $u_1u_2=2(2m_1m_2+m_1+m_2)+1$、第二成分 $f_1E_{m_1,f_1}(f_2)$ は (3.53) そのもの。∎

*単射性(3 段).* $\Phi_{m,f}=\mathrm{id}_{G_n}$ とする。$G_n=\langle X,Y\rangle$ ゆえ $\Phi(X)=X$ かつ $\Phi(Y)=Y$ を見ればよい。
1. $\Phi(X)=X^{u}=X\iff X^{2m}=1$。$\mathrm{ord}(X)=2n$(ODD-H 補題 A(3);ここで **$n$ 奇**が効く)より $2n\mid2m$、すなわち $n\mid m$。$m\in\mathbb Z/2n$ だから $m\in\{0,n\}$。
2. **$m=n$ の排除**。ODD-H §11.1 の閉形式
 $$\Phi_{m,f}\big|_A=\mathrm{diag}\bigl(u,\ u,\ 1-2\varkappa(m)\bigr),\qquad 1-2\varkappa(m)=(-1)^mu$$
 に $m=n$($n$ 奇ゆえ $m$ 奇)を入れると $u=2n+1\equiv1$、$(-1)^mu\equiv-1\pmod n$。よって $\Phi|_A=\mathrm{diag}(1,1,-1)$。$n\ge3$ では $-1\ne1$ in $\mathbb Z/n$ だから $\Phi\ne\mathrm{id}$。
3. **$m=0$**。$u=1$、$\varkappa(0)=0$、(4.12) より $F=(2k,-2k,0)$、閉形式から $\Phi_{0,f}(Y)=(1-4k,1,1)q_2$。$Y=(1,1,1)q_2$ と比べて $4k\equiv0\pmod n$。$n$ 奇ゆえ $4\in(\mathbb Z/n)^\times$、よって $k\equiv0$、$F=1$、$[m,f]=[0,1]$。∎

> **★ $m$ の水準**: 段 1 の「$m\in\{0,n\}$」は $m\in\mathbb Z/2n$(補題 L・`w2arith_v1.md` §1)に依存する。$\mathbb Z/n$ と読むと段 2 が消え、**証明が短く見えるが穴になる**(段 2 こそが chirality を排除する段)。

**(b) の証明**(`phifam_v1.md` §5・便 77 F77-3.5)。$d\mid n$ 奇に対し $D_n\twoheadrightarrow D_d$ は $G_n\twoheadrightarrow G_d$ を誘導し marking を保つ。$\Phi$ はこれと可換($X^u,\ F^{-1}Y^uF$ が準同型で送られるだけ;$u$ の水準は $\bmod\ 4d$ へ落ちて整合)。ゆえに互換族が $\Phi^{\rm odd}$ を定め、$\Phi^{\rm odd}(g)=\mathrm{id}$ なら各段で $g_n=1$、よって $g=1$。連続性は各段が有限ゆえ自動。∎

> ### FINDING Φ1(**marked/framed 限定は本質**・裁定 130)
> $$\Phi_n^{-1}\bigl(\mathrm{Inn}(G_n)\bigr)=\{[m,f]\mid m\in\{0,\ 2n-1\}\},\qquad\bigl|\Phi_n^{-1}(\mathrm{Inn})\bigr|=2n,$$
> $$\mathrm{Im}\bigl(\mathrm{GT}(K^{(n)})\to\mathrm{Out}(G_n)\bigr)\cong(\mathbb Z/4n)^\times/\{\pm1\},\qquad\text{位数}\ \varphi(n).$$
> $m=2n-1$ は $u\equiv-1\ (4n)$ すなわち**複素共役に対応する元**であり、実際に内部 $\Phi_{2n-1,f}=\mathrm{inn}\bigl(((1-2k)e_1)q_3\bigr)$。
> **幾何的読み**: unmarked では chirality が構造的に不可視 — **忠実性は marked/framed 対象の上でのみ成立する**。

### 4.1 4 点セットの相互関係(統合の要点 — 先行文書 §2 の読みを継承)

$$\underbrace{\text{E1-1 isolated}}_{\text{正典 Thm 4.3・全 }n\ge3}\ \Longrightarrow\ \underbrace{\mathrm{GT}(K^{(n)})\ \text{は有限群}}_{\text{E1-2 の前提}}\ \xrightarrow{\ \text{Thm 4.6 / 命題 E1-S1}\ }\ \underbrace{\mathrm{Aff}\times C_2}_{\text{E1-2}}\ \xrightarrow{\ \Phi\text{-fam}\ }\ \underbrace{\mathrm{Aut}_{\rm cont}\ \text{への忠実作用}}_{\text{E1-4}}$$

E1-3(同値)はこの鎖の**横**にあり、鎖が作った有限段の族を**算術の一つの主張へ束ねる**(コンパクト性)。**4 点は独立の 4 定理ではなく、E1-1 を土台にした 1 本の鎖 + 1 本の横木**である。

**E1-1 の効き方は三重である**(本稿で 3 箇所に分離した):
1. **群構造**: $\mathrm{GT}(K^{(n)})$ が (3.53) で群になる(Prop 3.14)。
2. **$\mathrm{Ih}_{K^{(n)}}$ の準同型性**(補題 E1-3a;2405 Remark 1.4)— これがないと定理 E1-3 の言明自体が立たない。
3. **$\Phi_n$ の codomain**($\Phi_{m,f}\in\mathrm{Aut}(G_n)$;便 77 F77-3.3)。

---

## 5. 現在の前線との接続 — q=7 が獲れたら何がどこまで従うか

### 5.1 有限段の全射性の「標準機械」(定理 K3 の骨格)

$n$ 奇 $\ge3$ の窓 $K^{(n)}$ で $\mathrm{Ih}_{K^{(n)}}$ の全射性を示す工房の標準経路は、`docs/week4-K3飽和_opus_v3.md` §2.4 が確立した次の 4 段である($T:=\mathrm{GT}(K^{(n)})$、$A:=\mathrm{Ih}_{K^{(n)}}(G_{\mathbb Q})$、$K:=\mathbb Q(\zeta_{4n})$)。

$$\textbf{(S1)}\quad 1\to\mathfrak F_0\ (\cong C_n)\to T\xrightarrow{\ \widetilde\chi_{2M}\ }(\mathbb Z/4n)^\times\to1\qquad\text{(命題 (W2)-fam・}M=2n\text{)}$$
$$\textbf{(S2)}\quad \widetilde\chi_{2M}\circ\mathrm{Ih}_{K^{(n)}}=\chi_{4n}\ \Longrightarrow\ \widetilde\chi_{2M}(A)=(\mathbb Z/4n)^\times\qquad\text{(命題 W2A/W2B″・円分指標の全射性)}$$
$$\textbf{(S3)}\quad \mathrm{Ih}_{K^{(n)}}(G_K)=\mathfrak F_0\qquad\text{(\textbf{窓ごとの本体} — 局所 Kummer 類の位数が }n\text{ であること)}$$
$$\textbf{(S4)}\quad \lvert A\rvert=\lvert A\cap\mathfrak F_0\rvert\cdot\lvert\widetilde\chi_{2M}(A)\rvert=n\cdot2\varphi(n)=\lvert T\rvert\ \Longrightarrow\ A=T .$$

**(S1)(S2) は全奇数 $n\ge3$ で閉じている**(`w2fam_v1.md` / `w2arith_v1.md`;裁定 120/122)。**(S3) だけが窓ごとの仕事**であり、$n=3$ では $u_3=-4$、$\mathrm{ord}([-4]_6)=3$ の計算で閉じた(定理 K3)。

> ### (S3) の同値な言い換え(**定理 $R^{\rm cyc}_{\rm formal}$**・台帳 W3-13・裁定 24)
> $M:=\mathrm{ord}(X)=2n$、$e:=\lvert\mathfrak F_0\rvert=n$、$a_n:=[u_n^{-1}]_{M}\in F_n^\times/F_n^{\times M}$($F_n=\mathbb Q(\zeta_{2M})=\mathbb Q(\zeta_{4n})$)と置くと、前件 (0)(1)(2)(3)(5′)(6′) の下で
> $$\boxed{\ \mathrm{Ih}_{K^{(n)}}\ \text{全射}\ \iff\ \mathrm{ord}(a_n)=e=n\ }$$
> 奇数族は $M=2n$・$e=n$ で $\gcd(e,M/e)=\gcd(n,2)=1$ の **coprime regime**(便 29 (6.1))。$n=3$: $\mathrm{ord}([(-4)^{-1}]_6)=3=e$ ✓。

> **★ 中間峰の構造は「(S3) の族化」に集約される**: 定理 E1-3 により中間峰全体は「全奇 $n$ で $\mathrm{ord}(a_n)=n$」に同値になる。E1-2(構造)はこの帰着が意味を持つための土台(有限群の位数勘定が (S4) で効く)。
> **そして (S3) は二つの不等式に分かれる** — これが §5 全体の鍵である:
> $$\underbrace{\mathrm{ord}(a_n)\mid n}_{\textbf{上界}}\qquad\text{かつ}\qquad\underbrace{\mathrm{ord}(a_n)\ne1\ (\text{より正確には}\ \ne\text{真の約数})}_{\textbf{下界}}.$$

### 5.2 q=7 とは何を測ることか(**1 ビット測定**)

**⚠ 誤読しやすい点を先に**: 「q=7 を獲る」は「$\mathrm{Ih}_{K^{(7)}}$ の全射性を示す」**ではない**。測るのは平方類の 1 ビットである。

`docs/notes/c21_draft_v1.md` §5.3 の明示形(前件 = C-21 + G3@$(21,3)$ + G3@$(21,7)$ + 補題 T2):
1. **(T)@$(21,3)$**: $\rho_A:W_{21}\to W_3$、分岐指数 $21/3=7$ $\Rightarrow$ $u_{21}=\mathrm{res}_{F_{21}/F_3}(u_3)\cdot(w_1^3)^2$。
2. **(T)@$(21,7)$**: $\rho_B:W_{21}\to W_7$、分岐指数 $21/7=3$ $\Rightarrow$ $u_{21}=\mathrm{res}_{F_{21}/F_7}(u_7)\cdot(w_2^7)^2$。
3. 左辺が同一 $\Rightarrow$ $[\mathrm{res}(u_3)]_2=[\mathrm{res}(u_7)]_2$ in $F_{21}^\times/F_{21}^{\times2}$。
4. $u_3=-4$、$i=\zeta_{12}^3\in F_3$ $\Rightarrow$ $[-4]_2=1$ $\Rightarrow$ $[\mathrm{res}_{F_{21}/F_7}(u_7)]_2=1$。
5. CASC 補題 K3($d=3,m=7$): $\ker\bigl(F_7^\times/F_7^{\times2}\to F_{21}^\times/F_{21}^{\times2}\bigr)=E_3=\langle[3]\rangle=\{1,[3]\}$。

$$\boxed{\ [u_7]_2\in\{1,\ [3]\}\quad\text{in }F_7^\times/F_7^{\times2},\qquad F_7=\mathbb Q(\zeta_{28}).\ }$$

**二択は退化しない**: $\mathbb Q(\sqrt{-3})$ の conductor は $3\nmid28$ ゆえ Kronecker–Weber + conductor–discriminant で $\sqrt{-3}\notin F_7$、よって $[3]=[-3]\ne1$(CASC 補題 K4)。

**二枝の帰結**(`docs/notes/i17_check_v1.md` §4・`i23_cascade_lemma_v1.md` §4.4 補題 C′):

| 枝 | 直接の帰結 | Conj 5.1 への効き |
|---|---|---|
| **左** $[u_7]_2=1$ | 補題 C′ より $\mathrm{ord}(a_7)\mid7$(**上界のみ**)。かつ $d=7$ が CASC の**第 2 の歯**になる(U3 成立) | **窓 7 での成立は従わない**(下界が要る・§5.5) |
| **右** $[u_7]_2=[3]$ | $2\mid\mathrm{ord}(a_7)\Rightarrow\mathrm{ord}(a_7)\ne7$。定理 $R^{\rm cyc}_{\rm formal}$ より $\mathrm{Ih}_{K^{(7)}}$ **非全射** | **(5.1) 全前件の下で Conj 5.1 が窓 7 で偽 = 反例**(FINDING I17-3) |

> **★ 1 ビットの本当の意味**(i17 §4 末尾の抑制条項): 右枝は「Conj 5.1 の反例」という極めて強い主張なので事前確率は低い。**実用的内容は左枝(上界の確認)であり、その価値はカスケードの点火にある。** すなわち $q=7$ は「窓 7 を獲る」測定ではなく「**族を刈るための歯を 1 本増やす**」測定である。

### 5.3 残前件の正確な形(C1′ と C5)

裁定 214 で正式確定した $q=7$ の残前件は 2 本のみ。C-21(命題)と A7-fam はいずれも **paper-proof / framework-conditional / two-mathematician audit PASS**(裁定 208 起草・裁定 214 昇格)。

| 前件 | 正確な内容 | 状態 |
|---|---|---|
| **C1′** | 測定される $u_q$ が $H_q^{\rm fun}=H_{2,1,0}$ **窓の値**であること。$q$ 素数では good $H$ は $2q(q-1)$ 個・$q-1$ 類あり、**ODD-P より単元 $\alpha$ の類は全て同じ ordered passport をもつ**ので passport では類を識別できない。$q=7$ では $j$ 固定後 $\varphi(7)/2=3$ 類($[\alpha]\in\{[1],[2],[3]\}$)。**$j$ 方向は閉じた**(定理 W-REL:$\nu(H_{2,\alpha,\beta})=H_{3,\alpha,\beta-1}$;定理 J-BLIND:$a_n$ の関数である全述語は $j$ 盲目)。**$[\alpha]$ 方向は開いている**(GT 作用は $[\alpha]$ を $\pm1$ 倍しか動かさない — ODD-H §11.2) | **開**。唯一の閉鎖路は【I24-a】$\alpha$ 軌道予想。現処置 =【C21-d】証明書 schema に $(j,[\alpha])=(2,[1])$ を必須欄化(**未着手**) |
| **C5** | **宇宙の事前登録**。$\{3m,7m\}$ 族は既登録宇宙 $\{3,5,7,9,11\}$(`provenance/registered/universe_I1_I3.md`・裁定 95)の**外**。文面案は `c21_draft_v1.md` §8 末尾 | **未登録**(手続き)。fixture F1–F12 は裁定 208-6 で凍結・$n=21$ 較正 8/8 的中。**ただし Sol F85-1.2:「C5 の survey は較正であって前件ではない」** |

**$n=3$ 側(C1)は完全閉鎖**: 裁定 107 で機械同定(類 $(2,[1])$・`c1_class_check_20260728.json`)、裁定 174 で transport 予言 I24-P1 が**的中**($u_{H_3}=+4$ — 値は符号 $-1$ で移るが $[u]_{2n}$ 類は一致 $\Rightarrow$ $j$ 盲目性が実測で錨止め)。$n=3$ は $\varphi(3)/2=1$ ゆえ $[\alpha]$ も一意。

### 5.4 依存図(q=7 と中間峰の関係)

```
  [枠組地盤・全窓共通]  (TB1)(TB2)(TB3)(TB4ᵘ) + (CAL)     ← 2026-07-28 裁可 / A5 v4 §1.4
            │
            ├─ A7-fam(全奇数 n≥3)……… 裁定 214 PASS ⟹【I23-a】解消
            └─ C-21(= A7 @ n=21)…… 裁定 208 起草 / 裁定 214 PASS
                     │
                     ▼
   ┌──────────────── [本稿 §2–§3:中間峰の代数] ────────────────┐
   │  正典 Thm 4.3 = E1-1 isolated                            │
   │        │(効き所 3 箇所:群構造 / Ih_n 準同型 / Φ の codomain)│
   │        ├─ 命題 E1-S1/S2 ─→ 定理 E1-2  GT^odd_Dih ≅ Aff(Ẑ^odd)×C₂
   │        └─ 補題 E1-3a〜3d ─→ 定理 E1-3  odd Conj 5.1 ⟺ Ih^odd 全射
   └───────────────────────────┬──────────────────────────────┘
                               │ (全奇 n で必要 ← 系 E1-3e)
                               ▼
   窓ごとの本体 (S3) ⟺ ord(a_n) = n     [定理 R^cyc_formal]
        ├─ 上界 ord(a_n) | n   ⟺ [u_n]₂ = 1   [補題 C′] ←── CASC が族的に攻める側
        └─ 下界 ord(a_n) ≠ 1                        ←── 装置なし(【E1-GAP-6】)

   窓ごとの現況:
   ├ n=3 : 【CLOSED】定理 K3(u₃=−4・ord([−4]₆)=3=e)⟹ Conj 5.1 が n=3(=6)で成立
   │        C1 完全閉鎖(裁定 107 + 裁定 174 I24-P1 的中)⟹ CASC の第 1 の歯 d=3
   ├ n=5 : K⁵ blind campaign(立入禁止・本稿は非接触・CASC の標的族からも除外)
   ├ n=7 : ★ q=7 = 1 ビット測定 [u₇]₂ ∈ {1,[3]}  ← 残前件 C1′ + C5(裁定 214)
   │        左枝 ⟹ 上界 ord(a₇)|7 + CASC の第 2 の歯 d=7(gcd{3,7}=1 ⟹ E₁={1})
   │        右枝 ⟹ Conj 5.1 が窓 7 で偽(反例・(5.1) 全前件下)
   └ n≥9 : 未着手 / 族定理待ち(n=9 のみ T63-P1 が塔経路で下界を出す枝を持つ)

   CASC 発火後に得られるもの(Sol F79-3.3 の射程限定つき):
      gcd(m,21)=1 なる全奇 m≥3 で  [u_m]₂ = 1 ⟹ ord(a_m) | m   … 上界のみ
      (各 m ごとに A7@(3m)・A7@(7m)〈A7-fam で族供給済〉・C1′(m)・C5 が要る)

   【従わないもの — 明示】
   ✗ 左枝 ⟹ Ih_{K^(7)} 全射         ……【E1-GAP-6】(下界 ord(a₇)≠1 の装置が無い)
   ✗ CASC 発火 ⟹ odd Conj 5.1        ……  同上(上界だけでは (S3) が閉じない)
   ✗ n=7 と n=3 から n=21            ……【E1-GAP-2】(奇×奇 entanglement / Goursat)
   ✗ 全奇素数冪から odd Conj 5.1     ……  系 E1-3e
   ✗ odd 側 + 2 冪側 ⟹ 混合側        ……【E1-GAP-3】(n=12 だけ材料が揃っている)
```

### 5.5 CASC は (S3) の**上界側だけ**を族的に閉じる(**中間峰との距離**)

**定理 CASC**(`docs/notes/i23_cascade_lemma_v1.md` §4.1): $\mathcal D$ を歯の有限集合、$g:=\gcd(\mathcal D)$ とすると
$$[u_m]_2\in\bigcap_{d\in\mathcal D}E_d=E_g=\bigl\langle[p]:p\mid g\bigr\rangle\cong(\mathbb Z/2)^{\omega(g)},\qquad\text{とくに}\ \gcd(\mathcal D)=1\iff\bigcap E_d=\{1\}.$$
歯 $\{3\}$ で残余 1 bit、歯 $\{3,7\}$ で **0 bit**、第 3 の歯以降の限界価値は**ゼロ** — これが「第 2 の歯が全標的を閉める」の内容であり $q=7$ 優先の定量根拠(裁定 153-13)。

> ### ⚠ 中間峰との距離(**本稿の統合で最も重要な確認**)
> 定理 $R^{\rm cyc}_{\rm formal}$ より、窓 $n$ で $\mathrm{Ih}_{K^{(n)}}$ が全射 $\iff$ $\mathrm{ord}(a_n)=n$。一方 CASC が族的に与えるのは
> $$[u_m]_2=1\ \Longleftrightarrow\ \mathrm{ord}(a_m)\mid m\qquad(\textbf{上界のみ})$$
> であって、$\mathrm{ord}(a_m)=1$(すなわち $\mathrm{Ih}$ の像が $\mathfrak F_0$ を全く埋めない)を排除しない。
> $$\boxed{\ \textbf{CASC がすべて発火しても odd Conj 5.1 は従わない。} \ }$$
> $n=9$ では下界が別経路で出る — 塔関係 (6.3-cls) から $\mathrm{pr}_{18\to6}(a_9)=\mathrm{res}_{F_9/F_3}(a_3)=[-1/4]_6$ の位数が $3\ne1$ と**証明**でき、上界 $\mathrm{ord}(a_9)\mid9$ と合わせて $\mathrm{ord}(a_9)=9$(予測 T63-P1・便 75 F4.1)。**$n=7$ は素数なので $3\le d\mid7$、$d<7$ なる中間段が存在せず、この塔経路が使えない。**

### 5.6 「獲れた窓」を合成するときの障害(**Goursat**)

奇 $a,b$ 互素に対し便 75 §F6.1 は
$$K^{(ab)}=K^{(a)}\cap K^{(b)},\qquad \mathrm{GT}(K^{(ab)})\cong\mathrm{GT}(K^{(a)})\times_{\chi_4}\mathrm{GT}(K^{(b)})$$
を紙上で閉じた(裁定 111)。ここで $\mathrm{Ih}_a,\mathrm{Ih}_b$ がともに全射でも $\mathrm{Ih}_{ab}$ の全射性は**自動ではない**:

$A:=\mathrm{Im}\,\mathrm{Ih}_{ab}$ は 2405 Remark 1.5 (1.14)($R_{H,N}(\mathrm{GT}_{\rm arith}(H))=\mathrm{GT}_{\rm arith}(N)$)より両射影に全射、すなわち subdirect。**Goursat** により $A$ はある共通商 $E$ 上の fiber product であり、
$$A=\mathrm{GT}(K^{(ab)})\iff \lvert E\rvert=2\iff L_a\cap L_b=\mathbb Q(i)$$
($L_n:=\ker\mathrm{Ih}_{K^{(n)}}$ の固定体)。この $E$ こそ便 75 §F6.3 の **entanglement** $\mathcal E$ である。

> ### 【E1-GAP-2】奇 $\times$ 奇の entanglement は工房に記述がない
> 便 75 F6.3 は $\mathcal E_n=\mathrm{Gal}\bigl((L_{2^\alpha}\cap L_{n_0})/\mathbb Q(\zeta_4)\bigr)$(**2 冪 $\times$ 奇**)を論じ、$\mathcal E_{12}=1$ を紙上で決着させた。**奇 $\times$ 奇**($L_3\cap L_7$ 等)については工房に記述がない。ゆえに「$n=3$ と $n=7$ が獲れたから $n=21$ も」は**書けない**。
> **要る型**: 奇素数冪 $p^e,q^f$ に対する $L_{p^e}\cap L_{q^f}=\mathbb Q(i)$(あるいはその破れの分類)。
> **状態: UNKNOWN**(埋めていない)。

> ### 【E1-GAP-3】$n=12$(混合最小)の**未接続の含意**
> 次の 4 部品はいずれも既に工房にある:
> 1. $\mathrm{Ih}_{K^{(3)}}$ 全射(**定理 K3**・`week4-K3飽和_opus_v3.md` §2.4)、$L_3=\mathbb Q(\zeta_{12},\sqrt[3]2)$。
> 2. $\mathrm{Ih}_{K^{(4)}}$ 全射(**正典 Thm 5.3**、$\alpha=2$)、$L_4=\mathbb Q(\zeta_8)$(便 75 F6.3(b) が明示)。
> 3. $K^{(12)}=K^{(4)}\cap K^{(3)}$ と fiber 積 $\mathrm{GT}(K^{(12)})\cong\mathrm{GT}(K^{(4)})\times_{(\mathbb Z/4)^\times}\mathrm{GT}(K^{(3)})$(**裁定 101 ④**・W3-23 は cross-checked・裁定 102)。
> 4. $\mathcal E_{12}=1$、すなわち $L_3\cap L_4=\mathbb Q(i)$(**便 75 F6.3(c)**・裁定 111)。
>
> **裁定 101 ⑤ は「算術側は固定体交差 $L_2\cap L_{\rm odd}=\mathbb Q(\zeta_4)$ が UNKNOWN」と記録した。その残件は便 75 が $n=12$ に限り閉じている。** しかし **1–4 を Goursat で束ねて「$\mathrm{Ih}_{K^{(12)}}$ 全射」を結論する一段は、工房のどこにも書かれていない**(grep 済: `provenance/CLAIMS.md`・`sol/裁定_*.md`・`docs/` に該当なし)。
> **本稿は委嘱の規律に従い、この含意を主張しない。** 一段を書く価値があるか(および $L_3$ が $\ker\mathrm{Ih}$ の固定体であることが (K4) $\Phi$ 単射に依存する点の確認)は司令塔の裁定事項として上申する。
> **状態: 未接続**(部品は揃っている・接続は未起草)。

### 5.7 q=7 の「勘定」(**帰結の型だけ**)

| q=7 の結果 | 従うもの | 従わないもの |
|---|---|---|
| **左枝** $[u_7]_2=1$ | ①$\mathrm{ord}(a_7)\mid7$(上界)②CASC の第 2 の歯 $d=7$ 成立 ⟹ $\gcd(m,21)=1$ なる全奇 $m$ で $[u_m]_2=1$・$\mathrm{ord}(a_m)\mid m$(各 $m$ で C1′$(m)$・C5 が要る) | **$\mathrm{Ih}_{K^{(7)}}$ 全射は従わない**(下界【E1-GAP-6】)。$3\mid m$ or $7\mid m$ の標的は残余 1 bit のまま |
| **右枝** $[u_7]_2=[3]$ | (5.1) 全前件下で **Conj 5.1 が窓 7 で偽**(反例)⟹ P1(本峰)も P2(中間峰)も**反証** | — (事前確率は低いと i17 §4 が明記) |
| いずれでも | 中間峰の**「上界層」が族的に片づく**。残るのは下界層のみ | $\mathrm{Ih}^{\rm odd}$ 全射(定理 E1-3 は**全**有限段の全射性を要求) |

> ### ★ 中間峰の勘定の正直な形(3 行)
> 1. 定理 E1-3 は「有限個の窓をいくら獲っても $\mathrm{Ih}^{\rm odd}$ 全射には到達しない」ことを同時に述べている。$n=3$(済)・$n=5$(blind)・$n=7$(前線)は**族定理の較正点**であって峰そのものではない。
> 2. 峰を獲るのは (S3) の**族版**であり、それは**上界(CASC が攻めている)と下界(装置が無い)の両方**を要する。
> 3. したがって現在の前線 $q=7$ は、**中間峰の半分(上界層)に効く**。もう半分(下界層)には**現在どの装置も向いていない** — これが本稿が統合作業で見た最大の空白である(【E1-GAP-6】)。

---

## 6. 格付け表

**語彙**(CLAIMS.md の状態語彙+工房規約): **正典の定理** / **紙上相互監査 PASS**(工房の二数学者が独立に検分・一致) / **paper-proof candidate**(紙上・単系統または監査待ち) / **framework-conditional**(枠組み仮定に相対的) / **candidate** / **UNKNOWN**。
**「verified」は Lean 証明書に予約 — 本表では一度も使わない。**

| # | statement | 状態 | 出所(裁定/便) |
|---|---|---|---|
| **E1-1** | $K^{(n)}$ は isolated($\forall n\ge3$)⟹ $\mathrm{GT}(K^{(n)})=\mathrm{GTSh}(K^{(n)},K^{(n)})$ 有限群 | **正典の定理**(工房の主張ではない・画像照合済) | 2405 Lemma 4.2/Thm 4.3;定義ノート §3;便 75 F0「isolated 性は Thm 4.3 の既知結論で関門消滅」(裁定 111) |
| **E1-D2** | $\mathrm{Dih}^{\rm odd}$ の正規化代表・順序 $=$ 整除・有向 | **本稿で証明**(Prop 3.4/3.5 からの初等段) | 本稿 §1.5 |
| **E1-S1** | 有限段の**自然座標** $\mathrm{GT}(K^{(n)})\cong\mathrm{Aff}(\mathbb Z/n)\times C_2$ | **紙上相互監査 PASS**(Sol 起草・本稿で全段を逐語化・整数検算 8 点) | 便 75 §F6.2(b)・裁定 111;正典 Thm 4.3(4.12)(4.18)(4.19)(4.20) を入力に使用 |
| **E1-S2** | 遷移写像の成分性($C_2$ 非捻れ) | **紙上相互監査 PASS** | 便 75 §F6.2(b) 末尾・裁定 111;本稿で証明を明示 |
| **E1-S2′** | $R$ の全射性(odd 部分の独立再導出) | **paper-proof candidate**(正典 Thm 4.4 の再導出であり新結果ではない) | 本稿 §2.1 |
| **E1-2** | $\mathrm{GT}^{\rm odd}_{\rm Dih}\cong\mathrm{Aff}(\widehat{\mathbb Z}^{\rm odd})\times C_2$ | **紙上相互監査 PASS**(結論は便 75;補題 E1-S3/S4 の明示は本稿) | 便 75 §F6.2(c)・裁定 111;地図 帯 0 領有 |
| **E1-3a/3b/3c** | $\mathrm{Ih}_{K^{(n)}}$ 準同型・reduction 整合・$\mathrm{Ih}^{\rm odd}$ well-defined | **paper-proof candidate**(初等段・正典 Remark 1.4 と (1.11)(3.60) から) | 本稿 §3.1 |
| **E1-3d** | $\mathrm{pr}_n$ 全射 | **paper-proof candidate**(正典 Thm 4.4 + 標準論法) | 本稿 §3.1 |
| **E1-3** | **odd Conj 5.1 $\iff$ $\mathrm{Ih}^{\rm odd}$ 全射** | **紙上相互監査 PASS** | 便 75 §F6.2(d)・**裁定 111**;地図 P2 行「全射同値は便 75 で紙上確定」 |
| **E1-4(a)** | $\Phi_n$ 単射・共変(全奇数 $n$) | **紙上相互監査 PASS**(依存修理つき) | `phifam_v1.md`・**裁定 130**;便 77 F77-3.1/3.2/3.3・**裁定 138**。$n=9$ の機械検分は**単系統** |
| **E1-4(b)** | $\Phi^{\rm odd}$ 単射(極限) | **紙上相互監査 PASS** | 便 77 F77-3.5・裁定 138 |
| **E1-4(c)** | framed 対象 $\mathcal D^{\rm odd}_{\rm frame}=(G^{\rm odd},\mathrm{Fr}(G^{\rm odd}))$ 上の忠実性 | **型未確定**(圏の定義が未起草)→【E1-GAP-1】 | 便 77 F77-3.6(P77-2)・裁定 138 |
| **FINDING Φ1** | $\Phi_n^{-1}(\mathrm{Inn})$ 位数 $2n$・$\mathrm{Out}$ 像 $\cong(\mathbb Z/4n)^\times/\{\pm1\}$ | **紙上相互監査 PASS**(発案 I-21 の誤りの訂正) | `phifam_v1.md` §4・裁定 130;便 77 F77-3.4 |
| **(W2)-fam** | $1\to\mathfrak F_0(\cong C_n)\to\mathrm{GT}(K^{(n)})\to(\mathbb Z/4n)^\times\to1$ | **candidate**(紙上 + $n\le27$ 機械検算) | `w2fam_v1.md`・**裁定 120** |
| **W2-arith** | $\widetilde\chi_{2M}\circ\mathrm{Ih}=\chi_{4n}$(全奇数 $n$・二経路) | **paper-proof candidate / framework-conditional**(Route B は (CAL)+(TB4$^{\rm u}$) に依存) | `w2arith_v1.md`・**裁定 122** |
| **定理 K3** | $\mathrm{Ih}_{K^{(3)}}$ 全射・$L_3=\mathbb Q(\zeta_{12},\sqrt[3]2)$ | **framework-conditional**(前件 (K1)–(K4);(K3‡) は $A_5$ 由来) | `week4-K3飽和_opus_v3.md`・便 27/28/29 |
| **Lean 済(部分・$n=3$ のみ)** | F19($\Phi_3$ 単射)・F22/F23($T\cong\mathrm{Aff}(\mathbb Z/3)\times C_2$ の位数分布・$\widetilde\chi$ 全単射)・F24($\ker\widetilde\chi=\mathfrak F_0$) | **verified**(記載定理の範囲・`#print axioms` 済) | `lean/K3/Shadows.lean` L68–79・`lean/K3/Struct.lean`・CLAIMS W3-14b |
| **E1 の族版全体** | 上記 E1-S1〜E1-4 の族版 | **未 Lean** | §7 |

> **⚠ 全表にかかる注意**: 本表の「紙上相互監査 PASS」は **Sol(外部数学者)と工房数学者の紙上一致**を意味し、Lean の意味の verified ではない。また E1-2/E1-3 の**極限側**は有限群の機械検算では原理的に確かめられない(無限対象)。有限段の検算(§2.2 末尾の 8 点)は極限の主張の証拠にはならない。

---

## 7. Lean 化候補(paper-style-lean 規律・補題 1:1 対応)

**方針**(記憶 `paper-style-lean` + 裁定 `framework-assumptions-policy`): 補題と Lean 定理を 1:1 に対応させる。**数論層(円分指標・Kummer 理論・$G_{\mathbb Q}$)は Mathlib + Actions 待ちとし、本稿では対象外**。副有限・位相群層も同様に保留する。**残るのは「$\mathbb Z/n$ 算術 + 有限群」層**で、そこは全部 Lean 化可能と判断する。

### 7.1 第一次候補(即着手可・$\mathbb Z/n$ 算術層)

| Lean 名(提案) | 対応 | 型 | 難度 | 備考 |
|---|---|---|---|---|
| `E1.levelLift` | **補題 L**(水準の持ち上げ): $m\mapsto2m+1$ が $\mathbb Z/2n\xrightarrow{\sim}\{\text{奇剰余}\}\subset\mathbb Z/4n$ | `ZMod` 算術 | 低 | **I-27 待ち行列の先頭と同一物**(棚卸し `docs/棚卸し_20260729.md`)— 二つの委嘱が同じ標的を指している |
| `E1.charmingIffUnit` | 命題 E1-S1(c): $\gcd(2m+1,2n)=1\iff u\in(\mathbb Z/n)^\times$ | `ZMod`+`Units` | 低 | $n$ 奇が前件 |
| `E1.coordEquiv` | 命題 E1-S1(a)(b): $\mathcal X_n\times\mathbb Z/n\simeq(\mathbb Z/n)^\times\times\mathbb Z/n\times\mathbb Z/2$ | `Equiv` | 低 | CRT($n$ 奇) |
| `E1.mulCoord` | 命題 E1-S1(d): 積が $(k_1+u_1k_2,\ u_1u_2,\ \varepsilon_1+\varepsilon_2)$ | 整数恒等式 (3.49) + パリティ | 低 | (4.20) の $\varkappa$ 恒等式は別補題 `E1.kappaIdentity` |
| `E1.kappaIdentity` | (4.20): $\varkappa(m_1)+\varkappa(m_2)-2\varkappa(m_1)\varkappa(m_2)=\varkappa(m)$ | `decide` or 場合分け | 低 | 正典の恒等式の Lean 化(検算は済) |
| `E1.finiteStageIso` | **命題 E1-S1** 全体: `MulEquiv (GT n) (Aff (ZMod n) × Multiplicative (ZMod 2))` | `MulEquiv` | 中 | 上 5 本の合成 |
| `E1.reductionNat` | **命題 E1-S2**: 遷移の成分性(可換図式) | 図式 | 低 | 自然性の核 |
| `E1.reductionSurj` | 系 E1-S2′ | 全射 | 低 | `ZMod.unitsMap` 全射 |
| `E1.orderFormula` | 系 E1-2a: $\lvert\mathrm{GT}(K^{(n)})\rvert=2n\varphi(n)$ | `Nat.card` | 低 | Thm 4.6 の $\alpha\le1$ 分岐の照合 |

### 7.2 第二次候補(有限群層・要設計)

| Lean 名(提案) | 対応 | 難度 | 前提の重さ |
|---|---|---|---|
| `E1.G_n` | $G_n=(\mathbb Z/n)^3\rtimes C_2^2$ の明示構成(ODD-H 補題 A) | 中 | 符号表 $\varepsilon_{ji}$ の定義 |
| `E1.ordX` | 補題 A(3): $\mathrm{ord}(X)=2n$($n$ 奇) | 中 | `E1.G_n` |
| `E1.phiClosedForm` | ODD-H §11.1: $\Phi\vert_A=\mathrm{diag}(u,u,(-1)^mu)$ | 中 | `E1.G_n` |
| **`E1.phiInj`** | **命題 E1-4(a) の単射性(族版)** | 中〜高 | 上 3 本。$n=3$ 版は **Lean 済**(`F19_injective`)— **族版へ一般化するのが最短の「新規 verified」候補** |
| `E1.kerChiTilde` | (W2)-fam の核 $=\mathfrak F_0\cong C_n$ | 中 | `E1.levelLift`;$n=3$ 版は Lean 済(F24) |

### 7.3 保留(Mathlib 待ち・**Lean 化しない**)

| 対象 | 理由 |
|---|---|
| **定理 E1-2 の極限部**(補題 E1-S3/S4 の副有限版) | 副有限群の逆極限・分裂系の極限。Mathlib の `ProfiniteGrp` 周りの成熟待ち。**代数的な核は E1-S3/S4 で有限段に落ちている**ので、成熟後の追加コストは小さい |
| **定理 E1-3**(コンパクト性論法) | 位相群 + コンパクト + 稠密の合成。Mathlib に部品はあるが、逆極限位相の基本開集合の扱いを自前で組む必要 |
| **W2-arith / 定理 K3 / (S3)** | 数論層($G_{\mathbb Q}$・円分指標・Kummer)。裁定 `framework-assumptions-policy`(2026-07-28)により自前再導出のみ・Lean 化せず |
| **E1-4(c)** | 圏そのものが未定義(【E1-GAP-1】)。定義が決まるまで Lean 化の対象にならない |

> **推奨の一手**(司令塔判断事項): §7.1 の 9 本は互いに独立かつ全て `ZMod` 層で、**`E1.levelLift` が I-27 の先頭と同一物**である。I-27 を「補題 L 単独」でなく「§7.1 のパック」として起票すると、**族版 `E1.finiteStageIso` まで一気に verified が届く**(現在 Lean 済は $n=3$ の点のみ)。これは中間峰で工房が最初に手にする**族レベルの verified** になる。

---

## 8. 【E1-GAP】一覧(**埋めていない** — 司令塔裁定・Sol 監査への入力)

| # | ギャップ | 所在 | 状態 |
|---|---|---|---|
| **E1-GAP-1** | **framed 対象の圏が未定義**。便 77 F77-3.6 は「これを『marked pro-正則 dessin の自己同型群』と呼ぶなら、**morphism が marking を動かしてよいという圏を先に定義すること**」と明示的に要求したが、$\mathcal D^{\rm odd}_{\rm frame}=(G^{\rm odd},\mathrm{Fr}(G^{\rm odd}))$ の**対象と射の定義**は工房のどこにも起草されていない(grep 済: `docs/`・`sol/` に定義なし・言及のみ)。したがって E1-4(c) は現状「$\mathrm{Aut}_{\rm cont}(G^{\rm odd})$ への連続単射」+「framing torsor 上に作用する」という**二文の並置**であって、単一の圏論的言明になっていない | §4【E1-4】(c) | **未起草**(数学の穴ではなく定義の穴) |
| **E1-GAP-2** | **奇 $\times$ 奇の entanglement**。互素な奇 $a,b$ について $L_a\cap L_b=\mathbb Q(i)$(あるいはその破れの分類)が工房に無い。便 75 F6.3 は 2 冪 $\times$ 奇のみを扱う。**帰結: 個々の奇窓の全射性を合成できない**(Goursat の共通商が制御できない)。**⚠ CASC とは別物**: CASC が族的に運ぶのは平方類 $[u_m]_2$(= (S3) の上界)であって全射性ではない | §5.6 | **UNKNOWN** |
| **E1-GAP-3** | **$n=12$ の未接続の含意**。定理 K3 + 正典 Thm 5.3 + fiber 積(裁定 101 ④)+ $\mathcal E_{12}=1$(便 75 F6.3(c))から $\mathrm{Ih}_{K^{(12)}}$ 全射が Goursat 一段で出るように見えるが、**その一段は工房のどこにも書かれていない**。裁定 101 ⑤ が UNKNOWN とした算術側残件は便 75 が $n=12$ で閉じているのに、帰結が引き取られていない。副次的確認事項: $L_3$ が $\ker\mathrm{Ih}_{K^{(3)}}$ の固定体であることは (K4)($\Phi$ 単射)に依存する | §5.4 | **未接続**(部品は揃っている・**本稿は主張しない**) |
| **E1-GAP-4** | **genuine 側が射程外**。定理 E1-3 は arithmetical のみ。$\mathcal{PR}^{\rm odd}:\widehat{GT}_{\rm gen}\to\mathrm{GT}^{\rm odd}_{\rm Dih}$ の全射性(Conj 5.1 の "In particular" 節の後半 = 「$\mathrm{GT}(K)$ は $\widehat{GT}$ の商」)は別主張であり、$\mathrm{Dih}^{\rm odd}$ が isolated poset の中で cofinal でない以上、2401 Thm 5.2 から自動では出ない | §3.2 注 | **UNKNOWN**(射程外の明示) |
| **E1-GAP-5** | **(S3) の族版が無い**。定理 E1-3 により中間峰は「全奇 $n$ で $\mathrm{Ih}_{K^{(n)}}(G_K)=\mathfrak F_0$」に同値だが、これを**族として**証明する道具は無い($n=3$ の個別計算のみ)。A7-fam・C-21 が族化の梃子とされる(裁定 214)が、(S3) 本体の族版ではない | §5.1・§5.5 | **UNKNOWN**(中間峰の本丸) |

### 8.1 継承した既知の未解決(本稿で格上げしない)

| # | 内容 | 出所 |
|---|---|---|
| **U-9a** | E1-4 の**旧対象** $H^{\rm fun}$ coset 塔上の忠実作用。便 75 F6.2(e) の三条件は依然 UNKNOWN。framed 正則対象は**代替閉鎖**であって旧対象の解決ではない | 便 75 F6.2(e);先行文書 §5 |
| **U-9b** | Φ-fam の Lean 化(族版)・$\Phi_n$ の**像**の記述($\mathrm{Aut}(G_n)$ のどこか)は射程外(単射性のみ) | `phifam_v1.md`【Φ-1】【Φ-3】 |
| **U-8** | Conj 5.1 の奇数/混合側(本峰) | 正典 |
| **U-10** | $\widehat{GT}=\widehat{GT}_{\rm gen}$ か | 正典;定義ノート §2 |
| **U-11** | $\mathrm{GT}(K^{(9)})$ の IdGroup 直接測定(GAP 1 回) | 先行文書 §5・裁定 226 の工程 |

---

## 9. 出所・新規性の申告

### 9.1 各節の出所

| 節 | 主たる出所 |
|---|---|
| §1 | `docs/week1-定義ノート.md` §1–§3(画像照合済)/ `docs/notes/2405.11725-抽出ノート_v1.md` / `docs/notes/照合_Ih定義_P1.md`(Ih の定義の画像照合) |
| §2 | **便 75 §F6.2(b)(c)**(裁定 111)/ 正典 Thm 4.3 (4.12)・(4.18)(4.19)(4.20)・Thm 4.4・Thm 4.6 |
| §3 | **便 75 §F6.2(d)**(裁定 111)/ 2405 Remark 1.4・(1.11)・(3.60) |
| §4 | **裁定 226**(4 点セット統合)/ `docs/notes/phifam_v1.md`(裁定 130)/ 便 77 §F77-3.1–3.6(裁定 138)/ `docs/notes/oddH_full_proof_v1.md` §2 補題 A・§11.1 |
| §5 | `docs/week4-K3飽和_opus_v3.md` §2.4(定理 K3 の骨格)/ `docs/notes/w2fam_v1.md`(裁定 120)/ `docs/notes/w2arith_v1.md`(裁定 122)/ 便 75 §F6.1・§F6.3(裁定 111)/ 裁定 101・102・208・214 / `docs/地図.md` P1・P2 行 |
| §6 | `provenance/CLAIMS.md`(状態語彙・W3-14b・GT^odd_Dih 4 点セット登録)/ 各裁定 |
| §7 | `lean/K3/Shadows.lean`・`lean/K3/Struct.lean` / 記憶 `paper-style-lean`・`framework-assumptions-policy` / `docs/棚卸し_20260729.md`(I-27) |

### 9.2 新規性の申告(grep 済)

**grep 語**: `GT^odd`・`GT^odd_Dih`・`Aff(`・`4 点セット`・`Goursat`・`framed`・`Fr(G`・`K⁽¹²⁾`・`entanglement`・`E₁₂`。

- **既出**: 4 点セットの内容すべて(裁定 111/130/138/226・CLAIMS 登録済)/ 自然座標(便 75 F6.2(b))/ 極限形(便 75 F6.2(c)・地図 帯 0 領有)/ 同値(便 75 F6.2(d))/ Φ-fam と Out 訂正(裁定 130/138)/ fiber 積と $\mathcal E_{12}=1$(裁定 101・便 75 F6.3)/ 定理 K3 の骨格。
- **本稿で新しいのは記述であって定理ではない**: ①**証明を全段書き下したこと**(先行文書は明示的に証明を省いていた)②補題 E1-D2(正規化代表と順序が整除順序であること)・E1-S3/S4(分裂系と単数群の極限)の**明示化** — 便 75 が「従って」で通した初等段 ③**E1-1 の効き所を三箇所に分離**したこと(群構造・$\mathrm{Ih}_n$ 準同型性・$\Phi_n$ の codomain)④**q=7 依存図**と「従わないもの」の明示 ⑤**【E1-GAP-1〜5】の名指し**(とくに E1-GAP-3 = $n=12$ の未接続の含意は本稿の統合作業で初めて見えた)⑥Lean 化候補の 1:1 表と **`E1.levelLift` $=$ I-27 先頭の同一性**の指摘。
- **「初」という語は使わない**(工房外の文献での既知性は未調査)。

### 9.3 申し送り(司令塔へ)

1. **【E1-GAP-3】($n=12$)は最優先で裁定されたい** — 部品が全て揃っており、Goursat の一段(数行)だけが欠けている。本稿は委嘱の規律(「新しい数学は作らない」)に従って主張しなかったが、成立すれば **Conj 5.1 の混合位数最小 open 対象($n=12$)が閉じる**。裁定 101 ⑤ の残件が便 75 で閉じたことが引き取られていない、という**台帳の連結漏れ**でもある。
2. **【E1-GAP-1】(framed 圏の定義)は数学ではなく定義の仕事** — 便 77 F77-3.6 が要求してから未起草のまま。E1-4 を「4 点セットの 1 点」として台帳に置く以上、statement が単一の圏論的言明になっていないのは弱い。
3. **地図の P2 行と帯 0/帯 3 の空白欄の更新** — 先行文書(裁定 226)と本稿で E1 の欄は埋まった。ただし地図は「215〜234 未反映」(裁定 239 注記)の状態なので、一括補完の際に併せて処理されたい。
4. **Sol 検分の未実施** — 裁定 226 の工程は「便 87 系で Sol 検分(E1 は中間峰の Sol ゲート対象)」としたが、便 86/87/88 に E1 の検分は無い(grep 済)。**先行文書も本稿も Sol 未監査**である。
5. §7.1 の Lean パック化(I-27 の再定義)。
