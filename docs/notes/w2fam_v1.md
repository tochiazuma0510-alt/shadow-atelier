# 命題 (W2)-fam — 全奇数 $n$ での完全列 $1\to\mathfrak F_0\to\operatorname{GT}(K^{(n)})\to(\mathbf Z/4n)^\times\to1$

**状態札: candidate(裁定前・未 commit)**
起草: Claude 第二インスタンス(数学者)/ 2026-07-28
設問: 裁定 118(n=9 前件 **C3-I6/I7** の閉鎖)
正典: `docs/week1-定義ノート.md` §2(合成則 (3.53)・(3.49)・charming)・§3(Thm 4.3 (4.12)・Thm 4.6・$K_{\rm ord}=\operatorname{lcm}(n,2)$)
併用: `docs/notes/oddH_full_proof_v1.md` §2 補題 A・§11(座標と $\Phi_{m,f}$ の作用)
機械証拠: `search/certs/i6i7_check_20260728.json`(§5 で照合)。**証明はこの数値に依存しない。**

---

## 1. ステートメント

$n\ge3$ を奇数、$M:=K^{(n)}_{\rm ord}=\operatorname{lcm}(n,2)=2n$ と置く。

> **命題 (W2)-fam.** 写像
> $$\widetilde\chi_{2M}:\ \operatorname{GT}(K^{(n)})\longrightarrow(\mathbf Z/4n)^\times,\qquad [m,f]\longmapsto 2m+1\ \ (\mathrm{mod}\ 4n)$$
> は **well-defined な群準同型**であり、**全射**で、
> $$\ker\widetilde\chi_{2M}=\mathfrak F_0=\{[0,f]\in\operatorname{GT}(K^{(n)})\}\;\cong\;C_n .$$
> すなわち完全列
> $$\boxed{\ 1\longrightarrow \mathfrak F_0\ (\cong C_n)\longrightarrow\operatorname{GT}(K^{(n)})\xrightarrow{\ \widetilde\chi_{2M}\ }(\mathbf Z/4n)^\times\longrightarrow1\ }\tag{W2-fam}$$
> が全奇数 $n\ge3$ で成立する。位数は $n\cdot\varphi(4n)=n\cdot2\varphi(n)=|\operatorname{GT}(K^{(n)})|$(Thm 4.6・$\alpha=0$)。
> さらに Thm 4.6 の同一視 $\operatorname{GT}(K^{(n)})\cong\operatorname{Aff}(\mathbf Z/n)\times\mathcal Z_2$ の下で $\ker\widetilde\chi_{2M}$ は**並進部** $C_n$ に一致し、$\widetilde\chi_{2M}$ は自然な射影 $\operatorname{Aff}(\mathbf Z/n)\times\mathcal Z_2\twoheadrightarrow(\mathbf Z/n)^\times\times\mathcal Z_2\cong(\mathbf Z/4n)^\times$ である。

**水準の警告(裁定 118 の罠)**: **$4n=2M$ が正しい水準**であり、$2n=M$ に落とすと $m$ と $m+n$ が併合されて核が $2n$ になり、$|\mathfrak F_0|=e=n$ と**因子 $2$ の偽不一致**が出る(§4)。正典が $\chi_{\rm vir}([m,f])=2m+1\bmod N_{\rm ord}$ と書く量は、この粗い方(水準 $M$)である — 誤りではなく、**(W2) が要求する不変量より粗い**。

---

## 2. 記号

正典 §3 より($n$ 奇):
$$\mathcal X_n=\{m\in\{0,\dots,M-1\}\mid\gcd(2m+1,M)=1\},\qquad
\varkappa(m)=\begin{cases}m+1&(m\ \text{奇})\\-m&(m\ \text{偶})\end{cases}$$
$$\operatorname{GT}(K^{(n)})=\bigl\{[m,f]\ \big|\ m\in\mathcal X_n,\ f\mapsto(r^{2k},r^{-2k},r^{\varkappa(m)}),\ k\in\mathbf Z\bigr\}\tag{4.12}$$
$K^{(n)}$ は isolated(Thm 4.3)ゆえ $\operatorname{GT}(K^{(n)})$ は (3.53) を積とする**有限群**である。GT-pair の定義(Def 3.1)より $m$ は $\mathbf Z/N_{\rm ord}=\mathbf Z/M=\mathbf Z/2n$ の類である。
$G_n$ の座標 $A\rtimes Q$、$a_i,q_j,X,Y$ は ODD-H §2 補題 A のものを用いる($f$ の値 $F=(2k,-2k,\varkappa(m))\in A$)。

---

## 3. 証明

### 3.1 well-defined(および水準 $2M$ が最良であること)

$m$ は $\mathbf Z/2n$ の類だから、代表を $m\mapsto m+2n$ と取り替えると
$$2(m+2n)+1=(2m+1)+4n\equiv 2m+1\pmod{4n}.$$
よって $2m+1\bmod4n$ は代表の取り方によらない。$8n$ を法にすると $4n\not\equiv0$ なので**壊れる** — すなわち **$4n=2M$ は $m\mapsto2m+1$ が well-defined な最細の水準**である。
値が単位であること: charming より $\gcd(2m+1,2n)=1$。$2m+1$ は奇数だから $\gcd(2m+1,4)=1$、また $\gcd(2m+1,n)\mid\gcd(2m+1,2n)=1$。ゆえに $\gcd(2m+1,4n)=1$、すなわち $2m+1\in(\mathbf Z/4n)^\times$。$\square$

### 3.2 準同型性(素朴な値割当てでなく合成則から)

合成則 (3.53) は
$$[m_1,f_1]\circ[m_2,f_2]=[\,2m_1m_2+m_1+m_2,\ f_1E_{m_1,f_1}(f_2)\,].$$
第一成分だけを見ればよく、**整数の恒等式**
$$2\bigl(2m_1m_2+m_1+m_2\bigr)+1=4m_1m_2+2m_1+2m_2+1=(2m_1+1)(2m_2+1)\tag{3.49}$$
が成り立つ。両辺を $\bmod\ 4n$ で読めば
$$\widetilde\chi_{2M}\bigl([m_1,f_1]\circ[m_2,f_2]\bigr)=\widetilde\chi_{2M}([m_1,f_1])\cdot\widetilde\chi_{2M}([m_2,f_2]).$$
恒等式は**整数として厳密**なので、法を取る順序による誤差は生じない(ここが「素朴な値割当て」との違い:$u=2m+1$ が乗法的であることは合成則の第一成分の形 $2m_1m_2+m_1+m_2$ そのものに由来する)。単位元 $[0,1]$ は $1$ に写る。$\square$

### 3.3 全射性

写像 $\mathcal X_n\to(\mathbf Z/4n)^\times,\ m\mapsto2m+1$ は**全単射**である。
* 単射: $2m+1\equiv2m'+1\ (4n)\Rightarrow 2(m-m')\equiv0\ (4n)\Rightarrow m\equiv m'\ (2n)$、$\mathcal X_n\subseteq\{0,\dots,2n-1\}$ ゆえ $m=m'$。
* 全射: $v\in(\mathbf Z/4n)^\times$ は奇数だから $v\equiv2m+1\ (4n)$ なる $m\in\{0,\dots,2n-1\}$ が一意に存在。$\gcd(v,4n)=1$ から $\gcd(2m+1,2n)=1$、すなわち $m\in\mathcal X_n$。

したがって $\widetilde\chi_{2M}$ は全射で、$|\mathcal X_n|=\varphi(4n)=2\varphi(n)$。$\square$

> **系(較正)**: (4.12) の $k$ は $r^{2k}$($r$ の位数 $n$、$n$ 奇ゆえ $2$ 可逆)で決まるので $k\in\mathbf Z/n$、各 $m$ の繊維はちょうど $n$ 点。ゆえに
> $$|\operatorname{GT}(K^{(n)})|=|\mathcal X_n|\cdot n=2\varphi(n)\,n$$
> で Thm 4.6($\alpha=0$)と一致する。**繊維 $=n$ は核の位数 $n$ と同じ数であり、これが (W2-fam) の位数勘定である。**

### 3.4 核

3.3 の単射性より
$$\widetilde\chi_{2M}([m,f])=1\iff 2m+1\equiv1\ (4n)\iff 2m\equiv0\ (4n)\iff m\equiv0\ (2n)\iff m=0\ \text{in}\ \mathbf Z/2n .$$
よって $\ker\widetilde\chi_{2M}=\{[0,f]\}$、$\varkappa(0)=0$ ゆえ
$$\ker\widetilde\chi_{2M}=\bigl\{[0,f_k]\ \big|\ f_k\mapsto(r^{2k},r^{-2k},1),\ k\in\mathbf Z/n\bigr\},\qquad |\ker|=n .$$

**群構造が $C_n$ であること(明示)**: (3.53) で $m_1=0$ のとき $E_{0,f_1}$ は $x\mapsto x,\ y\mapsto f_1^{-1}yf_1$ が定める $G_n$ の自己同型 $\Phi_{0,f_1}$ を誘導する。ODD-H §11.1 の閉形式
$$\Phi_{m,f}\big|_A=\operatorname{diag}\bigl(u,\,u,\,1-2\varkappa(m)\bigr),\qquad u=2m+1$$
に $m=0$($u=1$, $\varkappa(0)=0$)を入れると $\Phi_{0,f_1}\big|_A=\operatorname{diag}(1,1,1)=\mathrm{id}_A$。$f_2$ の値 $F_2$ は $A$ に属すから $E_{0,f_1}(f_2)$ の値は $F_2$ のまま。ゆえに
$$[0,f_{k_1}]\circ[0,f_{k_2}]=[0,\,f_{k_1}f_{k_2}]\quad\text{(値は }A\text{ 内の積)},$$
すなわち $\ker\widetilde\chi_{2M}\cong\bigl\langle(2,-2,0)\bigr\rangle=\bigl\langle(1,-1,0)\bigr\rangle\le A\cong(\mathbf Z/n)^3$($2$ 可逆)、これは位数 $n$ の巡回群 $C_n$。$\square$

**別証(座標非依存)**: $\operatorname{GT}(K^{(n)})/\ker\cong(\mathbf Z/4n)^\times$ は可換だから $\ker\supseteq[\operatorname{GT},\operatorname{GT}]$。Thm 4.6 で $\operatorname{GT}(K^{(n)})\cong\operatorname{Aff}(\mathbf Z/n)\times\mathcal Z_2$、$n>1$ 奇では $\{u-1:u\in(\mathbf Z/n)^\times\}\ni-2\in(\mathbf Z/n)^\times$ ゆえ $[\operatorname{Aff}(\mathbf Z/n),\operatorname{Aff}(\mathbf Z/n)]=\mathbf Z/n$(並進部)。よって $[\operatorname{GT},\operatorname{GT}]=$ 並進部 $\cong C_n$、位数がともに $n$ だから
$$\ker\widetilde\chi_{2M}=[\operatorname{GT}(K^{(n)}),\operatorname{GT}(K^{(n)})]=\text{並進部}\cong C_n. \qquad\square$$
(これが設問 ④「$\operatorname{Aff}(\mathbf Z/n)\times C_2$ 座標では $\ker=$ 並進部 $C_n$」の内容である。付随して $\widetilde\chi_{2M}$ は**アーベル化そのもの**: $\operatorname{GT}(K^{(n)})^{\rm ab}\cong(\mathbf Z/4n)^\times$。)

### 3.5 $\mathfrak F_0$ との同一視

命題 K5-1(W3-15①)は $\Phi_{0,k}=\operatorname{inn}(X^{-2k})$、Sol 便 73 (1.13) は $\Phi(\mathfrak F_0)=\operatorname{inn}(\langle X^2\rangle)$ と述べる。上の $\ker$ の元 $[0,f_k]$($F_k=(2k,-2k,0)$)について、ODD-H §11.1 の式で $u=1,\ F_1=2k,\ F_3=0$ とすると
$$\Phi_{0,f_k}(X)=X,\qquad \Phi_{0,f_k}(Y)=(1-4k,\,1,\,1)\,q_2,$$
他方 $X^2=a_1^2$ ゆえ
$$\operatorname{inn}(a_1^{-2k})(X)=X,\qquad \operatorname{inn}(a_1^{-2k})(Y)=(-2k)+(1,1,1)+q_2(2k,0,0)\ \text{付き}\ q_2=(1-4k,\,1,\,1)q_2 .$$
**両者は一致する**。$Z(G_n)=1$($A$ の三本の線がいずれも非自明指標を担うので $A^Q=0$、$q\ne1$ の元は $A$ 上非自明)だから $\operatorname{inn}$ は単射で $\operatorname{inn}(\langle X^2\rangle)\cong\langle a_1\rangle\cong C_n$。よって
$$\ker\widetilde\chi_{2M}\;=\;\{[0,f_k]\}_{k\in\mathbf Z/n}\;\xrightarrow{\ \sim\ }\;\operatorname{inn}(\langle X^2\rangle)\;=\;\Phi(\mathfrak F_0),\qquad k\mapsto\operatorname{inn}(a_1^{-2k}),$$
すなわち **$\ker\widetilde\chi_{2M}=\mathfrak F_0$ であり $e:=|\mathfrak F_0|=n$、$\mathfrak F_0\cong C_n$**(= I7 の主張)。$\square$

---

## 4. 水準の罠 — なぜ $\bmod\ 2n$ だと因子 $2$ が出るか

$n$ 奇のとき CRT で
$$(\mathbf Z/4n)^\times\cong(\mathbf Z/4)^\times\times(\mathbf Z/n)^\times,\qquad
(\mathbf Z/2n)^\times\cong(\mathbf Z/2)^\times\times(\mathbf Z/n)^\times\cong(\mathbf Z/n)^\times .$$
還元 $(\mathbf Z/4n)^\times\to(\mathbf Z/2n)^\times$ は全射で、核は $\{1,\,1+2n\}$(位数 $2$)— **消えるのはちょうど $(\mathbf Z/4)^\times=C_2$ 因子**である。粗い版
$$\chi_M:[m,f]\mapsto 2m+1\ (\mathrm{mod}\ 2n)$$
は $\widetilde\chi_{2M}$ とこの還元の合成だから:

* 像は $(\mathbf Z/2n)^\times$、位数 $\varphi(n)$($2\varphi(n)$ の**半分**)。
* 核は位数 $2n$($n$ の**二倍**)。併合される対はちょうど $\{m,\,m+n\}$($2(m+n)+1=(2m+1)+2n$)。$\gcd(2m+1,2n)=\gcd(2m+1+2n,2n)$ なので $\mathcal X_n$ は $m\mapsto m+n$ で安定 — 対は必ず両方 charming で、必ず併合される。
* $n$ が奇数ゆえ $m$ と $m+n$ は**パリティが異なる**。ODD-H §11.1 の $\Phi\big|_A=\operatorname{diag}(u,u,\delta u)$、$\delta=(-1)^m$ と、$2m+1\equiv(-1)^m\pmod 4$ を見比べると:

$$\boxed{\ \widetilde\chi_{2M}\ \text{の}\ (\mathbf Z/4)^\times\ \text{成分}\;=\;\delta=(-1)^m\;=\;\text{Thm 4.6 の}\ \mathcal Z_2\ \text{因子}\ }$$

すなわち **$\bmod\ 2n$ に落とすことは、Thm 4.6 の $\mathcal Z_2$(= $\Phi$ の第 3 固有値の符号 = chirality)をちょうど捨てること**である。因子 $2$ の不一致はこの一点から生じる。

**I6/I7 の「同時不成立」の解消**: `docs/notes/i8_bridge_n9_v1.md` が指摘した $9\times6=54\ne108$ は、商を $(\mathbf Z/18)^\times$($\varphi(18)=6$)と取ったための矛盾である。正しくは
$$n\cdot\varphi(4n)=9\cdot\varphi(36)=9\cdot12=108=|\operatorname{GT}(K^{(9)})| \quad\checkmark$$
で、$\mathfrak F_0\cong C_9$($e=9$)と $|GT|=108$ は**両立する**。動かすべきは I6 の商の水準であって、I3′ でも I7 でもない。

---

## 5. 機械証拠との照合(§3 の証明に依存しない事後確認)

`search/certs/i6i7_check_20260728.json` は $\chi_M$(**$\bmod\ 2n$** — 粗い方)を測っている。§4 の予測は「像の位数 $=\varphi(n)$・全繊維 $=2n$」。

| $n$ | 実測 `chi_image_order` | 予測 $\varphi(n)$ | 実測 `chi_kernel_mult_at_1`(全繊維) | 予測 $2n$ | 実測 `charming_set` の大きさ | 予測 $\varphi(4n)$ | $\vert$GT$\vert$ | $n\cdot\varphi(4n)$ |
|---|---|---|---|---|---|---|---|---|
| 3 | 2 | **2** ✓ | 6 | **6** ✓ | 4 | **4** ✓ | 12 | **12** ✓ |
| 5 | 4 | **4** ✓ | 10 | **10** ✓ | 8 | **8** ✓ | 40 | **40** ✓ |
| 7 | 6 | **6** ✓ | 14 | **14** ✓ | 12 | **12** ✓ | 84 | **84** ✓ |
| 9 | 6 | **6** ✓ | 18 | **18** ✓ | 12 | **12** ✓ | 108 | **108** ✓ |
| 11 | 10 | **10** ✓ | 22 | **22** ✓ | 20 | **20** ✓ | 220 | **220** ✓ |

**5 点すべてで一致。** 証明書の `i7_match:false`(全 5 点)は「$\mathfrak F_0\cong C_n$ が偽」ではなく、**水準 $M$ の量を水準 $2M$ の予測と突き合わせた型の不一致**であり、$\widetilde\chi_{2M}$ で測り直せば繊維は $2n\to n$ になって $e=n$ と一致する。とくに `chi_value_multiplicities` が全値で等しい($\chi_M$ が群準同型であることの観測的痕跡)ことも (W2-fam) の系である。

> **再測定の仕様(implementer 向け・1 行)**: `i6i7-check.g` の $\chi$ を `(2*m+1) mod (4*n)` に変更するだけでよい。期待値は **像 $=(\mathbf Z/4n)^\times$(位数 $2\varphi(n)$)・全繊維 $=n$・`i7_match` が全 5 点で true**。追加の fail-closed assert として「$m\mapsto2m+1\bmod4n$ が $\mathcal X_n$ 上単射」を入れると水準の取り違えが再発しない。

---

## 6. 未閉鎖項

* 【W2-1】本稿は **(W2) の群論部分のみ**を閉じた。(W2) のもう半分、すなわち **$\widetilde\chi_{2M}\circ\operatorname{Ih}_{K^{(n)}}=\chi_{4n}$(円分指標との比較)は算術側**であり、本稿の射程外(GAP でも計算できない)。C3 の残りはここ。
* 【W2-2】本稿は $[m,f]$ の第一成分のみを使う。第二成分 $f$ に関する主張(Thm 4.3 の $\varkappa$ の形の正しさ等)は正典の引用であり再証明していない(ただし §3.5 の $\Phi_{0,f_k}=\operatorname{inn}(X^{-2k})$ 一致は独立に確認した)。
* 【W2-3】$n$ が偶数の場合は**射程外**($M=\operatorname{lcm}(n,2)=n$ となり水準・CRT・$\varkappa$ の分岐がすべて変わる。Thm 4.6 も $\alpha\ge2$ で別形)。「全奇数」は本質的な限定である。
* 【W2-4】紙上証明(paper-proof candidate)。Lean 検証ではない。
