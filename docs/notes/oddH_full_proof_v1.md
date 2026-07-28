# 命題 ODD-H — 独立監査と完全証明(v1)

**状態札: candidate(裁定前・未 commit)**
起草: Claude 第二インスタンス(数学者・独立監査役)/ 2026-07-28
監査対象: `sol/sol_reply_73_math.md` §Q1(命題 ODD-H・式 (1.1)–(1.11))
正典: `docs/week1-定義ノート.md` §3(2405.11725 (3.1) の $\psi_n$・$G_n$・$|G_n|=4n^3$(n 奇))
照合データ: `search/certs/i1_survey_20260728.json`(**証明はこの数値に依存しない**。§7 で事後照合のみ)

**状態札の内訳(混同禁止)**

| 内容 | 札 |
|---|---|
| §2 補題 A・§4 補題 B–I(命題 ODD-H の完全証明) | **紙上証明**(paper-proof candidate)。Lean の意味の verified ではない |
| §5 判別子の well-defined 性 | **紙上証明** |
| §6 命題 ODD-P(ordered passport の閉形式) | **紙上証明 + 二系統の数値一致**(§7) |
| §7 の個数表 | **cross-checked**(GAP 単系統だった JSON を、独立実装が全項再現) |
| §8 FINDING F1–F9 | **監査所見**(裁定前) |

---

## 1. 監査結論の要旨

1. **命題 ODD-H の結論はすべて正しい**。個数 $2n(n-1)$、自己正規化前 $2n^2$、共役類 $n-1$、各類サイズ $2n$、判別子 $(j,[\alpha])$、$\alpha\ne0$ 判定 — 全部が成立する。§4 に完全証明を置いた。
2. ただし **スケッチには実質的な欠落が 3 か所**ある。最も重いのは **(F2) 「$H$ の $Q$-像が $\langle q_2\rangle$ か $\langle q_3\rangle$」の無証明** — これは悉皆性(exhaustiveness)の要であり、「$q_1\notin H$」からは従わない。次に **(F4) 逆向き(各 $H_{j,\alpha,\beta}$ が実際に述語を満たすこと)と単射性の未証明** — これなしには (1.7)(1.8) は上界にすぎない。**(F1) (1.1) の分解そのものが正典からの導出でなく引用**。いずれも埋められる(埋めた)。
3. **新しい実質的発見(F8)**: **Sol の Q1.5 は $n=9$ で誤り**。ordered passport の残り一成分の型は $2n$ ではなく $(2n/d)^d$($d:=\gcd(\alpha,n)$)である(命題 ODD-P・§6)。したがって「$K^{(3)}/K^{(5)}$ と同じ ordered passport $(2n,2^{n-1}1^2,2n)$」を課すと $\alpha$ は**単元に限られ**、残る類は $(n-1)/2$ ではなく $\boldsymbol{\varphi(n)/2}$。$n=9$ では 4 ではなく **3**。Sol の結論(「単数形の正典 $\Lambda_n$ は $n\ge5$ で未定義」)自体は無傷だが、**$\alpha$ が非単元の窓は $K^{(3)}/K^{(5)}$ と同じ幾何型ではない**という下流に効く事実が落ちている。
4. **★教材 73-1 の位置づけの修正**: 「答えは $\varphi(n)$ でなく $n-1$」は**3 述語に対しては正しい**。だが passport を窓仕様に含めるなら $\varphi(n)$ 側が正しい。**二つの述語集合を区別せよ**、が正しい教訓である(どちらか一方が誤りなのではない)。
5. 判別子 $(j,[\alpha])$ は **marking を固定して初めて** well-defined($\alpha$ は固有線の生成元の取り方に依存し、独立な単元倍で $\alpha\mapsto u\alpha$)。marking $X,Y,Z$ から $X^2,Y^2,Z^2$ を取れば一様な 2 倍なので $\alpha$ は不変 — この一行がスケッチにない(F7)。$\operatorname{Aut}(G_n)$-軌道では $\alpha$ は $\gcd(\alpha,n)$ にまで潰れる($\tau(n)-1$ 軌道)。
6. **$n=9$ で $\alpha=3,6$ も good** は正しい(§4 補題 H は $\alpha$ の可逆性を一切使わない)。ただし上記 3 の意味で「$K^{(3)}/K^{(5)}$ と同型の検出器」ではない。
7. **(追補 §11・裁定 105 の追加設問)** $\Phi(\mathrm{GT}(K^{(9)}))$ の類への作用について、**Sol の (1.13)(1.14) と線形部論法は正しい**。$\Phi|_A=\operatorname{diag}(u,u,\pm u)$ は 108/108 で成立し、**全 108 shadow が類 $(2,[1])$ を保つ**。GAP 実測の $18/108$ は `search/k9-package.g` L221 の**共役方向の反転(規約 W-4 違反)**であり、その値($18$ 件・生き残り $m\in\{0,17\}$・落ちる対 $m+m'=17$)は独立実装で**完全に再現・説明**された(F10)。GT-軌道は全て 1 点なので「GT-軌道単位の detector 選択」は動機ごと消える(F13)。ODD-H 本体への影響はない。

---

## 2. 記法と設定(正典からの導出)

正典 §3 のとおり $D_n=\langle r,s\mid r^n,s^2,srs^{-1}r\rangle$、
$$\psi_n:PB_3\to D_n^3,\qquad x\mapsto(r,s,s),\quad y\mapsto(rs,r,rs),\quad c\mapsto(1,1,1),$$
$$G_n:=\operatorname{Im}\psi_n\;\cong\;PB_3/K^{(n)}\;\cong\;F_2/K^{(n)}_{F_2}.$$
$X:=\psi_n(x)=(r,s,s)$、$Y:=\psi_n(y)=(rs,r,rs)$、$Z:=\psi_n(z)=(XY)^{-1}$($xyz=1$)。
以下 $n\ge3$ は奇数。Sol の $P_n$ は本稿の $G_n$ である(以後 $G_n$ で統一)。

> **補題 A(構造補題).** $n$ を奇数とする。$a_1:=(r,1,1),\,a_2:=(1,r,1),\,a_3:=(1,1,r)$、
> $q_1:=(1,s,s),\,q_2:=(s,1,s),\,q_3:=(s,s,1)$ と置く。このとき
> 1. $A:=\langle a_1,a_2,a_3\rangle=\langle r\rangle^3\le G_n$ かつ $Q:=\{1,q_1,q_2,q_3\}\le G_n$、$Q\cong C_2^2$、
>    $$G_n=A\rtimes Q,\qquad |G_n|=4n^3 .$$
> 2. $q_j a_i q_j^{-1}=a_i^{\varepsilon_{ji}}$、$\varepsilon_{ji}=+1\iff i=j$(**Sol の (1.1) の符号表**)。
> 3. $X=a_1q_1$、$Y=a_1a_2a_3\,q_2$、$XY=a_1^{2}a_2^{-1}a_3^{-1}q_3$、
>    $\operatorname{ord}(X)=2n$、$\langle X\rangle=\langle a_1\rangle\times\langle q_1\rangle$ は位数 $2n$ の巡回群。
> 4. $A=[G_n,G_n]$。とくに $A$ は $G_n$ の**特性**部分群。

**証明.** $D_n$ 内で $(r^as)^2=1$ に注意する。
(1) $X^2=(r^2,1,1)$、$Y^2=(1,r^2,1)$、$XY=(r^2s,\;r^{-1}s,\;r^{-1})$ ゆえ $(XY)^2=(1,1,r^{-2})$。**$n$ が奇数なので $\langle r^2\rangle=\langle r\rangle$**(正典 p.15 の $J_n=\langle r^2\rangle^3$ と同じ点)、よって $a_1,a_2,a_3\in G_n$、すなわち $A\le G_n$。
反射パリティ $\pi_0:D_n^3\twoheadrightarrow C_2^3$(核 $=A$)は $X\mapsto(0,1,1)$、$Y\mapsto(1,0,1)$ を送るから $\pi_0(G_n)$ は偶パリティ部分群 $E\cong C_2^2$。$A=\ker\pi_0\le G_n$ ゆえ $G_n/A\cong E$、$|G_n|=4n^3$。
$q_1=a_1^{-1}X\in G_n$、$q_2=(a_1a_2a_3)^{-1}Y\in G_n$、$q_3=q_1q_2$。直接計算で $q_j^2=1$、$q_1q_2=q_2q_1=q_3$ ゆえ $Q\cong C_2^2$。$A\cap Q=1$ かつ $|A||Q|=|G_n|$ より $G_n=A\rtimes Q$。
(2) $srs^{-1}=r^{-1}$ と座標ごとの計算。例えば $q_1a_2q_1^{-1}=(1,srs,1)=(1,r^{-1},1)=a_2^{-1}$。
(3) 上の計算そのもの。$a_1$ と $q_1$ は可換で位数 $n,2$、$\gcd(n,2)=1$ ゆえ $\langle X\rangle=\langle a_1q_1\rangle\ni X^2=a_1^2$、$n$ 奇より $\langle a_1\rangle\le\langle X\rangle$、よって $\langle X\rangle=\langle a_1\rangle\times\langle q_1\rangle\cong C_{2n}$。
(4) $G_n/A\cong C_2^2$ は可換ゆえ $[G_n,G_n]\le A$。逆に $[a,q_1]=a^{-1}q_1aq_1^{-1}$ を走らせると $(q_1-1)A=\langle a_2^{-2},a_3^{-2}\rangle=\langle a_2,a_3\rangle$($n$ 奇)、同様に $(q_2-1)A=\langle a_1,a_3\rangle$。両者で $A$ を生成する。∎

**加法記法.** 以後 $A\cong(\mathbf Z/n)^3=\bigoplus_i(\mathbf Z/n)e_i$($e_i\leftrightarrow a_i$)と書く。$Q\cong C_2^2$ の非自明指標は 3 個 $\chi_1,\chi_2,\chi_3$($\chi_i$ の核は $\langle q_i\rangle$)で、補題 A(2) は
$$A^{\chi_i}=\langle e_i\rangle\qquad(i=1,2,3)$$
すなわち **3 本の座標線が 3 つの相異なる非自明指標をちょうど 1 回ずつ担う**、と言い換えられる。$q\in Q\setminus\{1\}$ に対し $A^{q,\pm}:=\ker(q\mp1)$ と書けば $A^{q_j,+}=\langle e_j\rangle$、$A^{q_j,-}=\bigoplus_{i\ne j}\langle e_i\rangle$。

> **補題 B(半単純分解).** $2\in(\mathbf Z/n)^\times$ とする。$q\in Q\setminus\{1\}$ で安定な部分群 $V\le A$ は
> $V=(V\cap A^{q,+})\oplus(V\cap A^{q,-})$ と分解する。

**証明.** $v\in V$ に対し $v=\tfrac12(v+qv)+\tfrac12(v-qv)$。$V$ は $q$-安定で $2$ が可逆だから両項とも $V$ に属し、それぞれ $A^{q,+},A^{q,-}$ に入る。和が直和なのは $A=A^{q,+}\oplus A^{q,-}$ から。∎

**記号.** $\pi:G_n\twoheadrightarrow Q$ を射影($\ker\pi=A$)とする。$j\in\{2,3\}$ に対し $j':=5-j$(すなわち $2'=3,\,3'=2$)。

---

## 3. 命題 ODD-H(監査版ステートメント)

> **命題 ODD-H.** $n\ge3$ を奇数、$G_n=A\rtimes Q$ を補題 A のとおりとする。部分群 $H\le G_n$ に対する三述語を
> $$(\mathrm{P1})\;[G_n:H]=2n,\qquad(\mathrm{P2})\;N_{G_n}(H)=H,\qquad(\mathrm{P3})\;\langle X\rangle\ \text{は}\ G_n/H\ \text{上推移的}$$
> と置く。$j\in\{2,3\}$、$\alpha,\beta\in\mathbf Z/n$ に対し
> $$H_{j,\alpha,\beta}:=\bigl\langle\,a_j,\;a_1^{\alpha}a_{j'},\;a_1^{\beta}q_j\,\bigr\rangle \tag{1.2}$$
> と定める(Sol の (1.2) と逐語一致)。このとき:
> 1. **(悉皆性と一意性)** $H$ が (P1)(P3) を満たす $\iff$ $H=H_{j,\alpha,\beta}$ なる $(j,\alpha,\beta)$ が存在する。しかもその $(j,\alpha,\beta)$ は一意。とくに (P1)(P3) を満たす部分群はちょうど $\boldsymbol{2n^2}$ 個。 (1.8)
> 2. **(正規化群)** $N_{G_n}(H_{j,\alpha,\beta})\cap A=U_{j,\alpha}:=\langle e_j,\ \alpha e_1+e_{j'}\rangle$ であり、
>    $$N_{G_n}(H_{j,\alpha,\beta})=H_{j,\alpha,\beta}\iff\alpha\ne0. \tag{1.3}$$
>    $\alpha=0$ のときは $N=\langle H,q_1\rangle$、$[N:H]=2$。
> 3. **(個数)** 三述語すべてを満たす部分群はちょうど $\boldsymbol{2n(n-1)}$ 個。 (1.7)
> 4. **(共役)** $H_{j,\alpha,\beta}\sim_{G_n}H_{j',\alpha',\beta'}\iff j=j'$ かつ $\alpha'=\pm\alpha$。 (1.9)
>    三述語を満たす部分群の $G_n$-共役類はちょうど $\boldsymbol{n-1}$ 個、各類のサイズは $\boldsymbol{2n}$。 (1.10)
>    完全不変量は
>    $$(j,[\alpha]),\qquad[\alpha]\in\bigl((\mathbf Z/n)\setminus\{0\}\bigr)/\{\pm1\}. \tag{1.11}$$
> 5. **(三述語の共役不変性)** (P1)(P2)(P3) はいずれも $H\mapsto gHg^{-1}$ で不変。とくに (P3) は共役類を割らない。

Sol のステートメントとの差分は **1 の「$\Longleftarrow$」と一意性を明示したこと**、および **5 を独立の項目として立てたこと**の 2 点である(F4・F5 参照)。

---

## 4. 証明

以下 $H\le G_n$ は (P1) を満たすとし、$U:=H\cap A$、$Q_H:=\pi(H)$ と置く。

### 補題 C(基本の数え上げと共役不変性)

> 1. $|H|=2n^2$、$|U|=n^2$、$|Q_H|=2$。
> 2. (P1) の下で:(P3) $\iff\langle X\rangle\cap H=1\iff\langle X\rangle$ は $H$ の左剰余類の完全代表系(単純推移)。
> 3. (P1)(P3) の下で $U\cap\langle e_1\rangle=0$、したがって $A=U\oplus\langle e_1\rangle$。
> 4. (P1)(P2)(P3) はそれぞれ共役不変。

**証明.** (1) $|H|=|G_n|/2n=2n^2$。$H/U\cong Q_H$ より $|H|=|U|\cdot|Q_H|$。$|U|$ は $|A|=n^3$ を割るので**奇数**、一方 $|Q_H|\in\{1,2,4\}$。$2n^2$ の $2$-指数は $1$($n$ 奇)だから $|Q_H|=2$、$|U|=n^2$。
(2) $\operatorname{ord}(X)=2n=[G_n:H]$(補題 A(3))。基点 $H$ の $\langle X\rangle$-軌道の長さは $|\langle X\rangle|/|\langle X\rangle\cap H|=2n/|\langle X\rangle\cap H|$。これが $2n$ に等しい $\iff\langle X\rangle\cap H=1$。位数が一致するので推移的なら単純推移、すなわち完全代表系。
(3) $\langle e_1\rangle=\langle a_1\rangle\le\langle X\rangle$(補題 A(3))ゆえ $U\cap\langle e_1\rangle\le\langle X\rangle\cap H=1$。位数を数えて $|U\oplus\langle e_1\rangle|=n^2\cdot n=n^3=|A|$。
(4) (P1) は自明、(P2) は $N(gHg^{-1})=gN(H)g^{-1}$。(P3): 写像 $G_n/H\to G_n/gHg^{-1},\ kH\mapsto kg^{-1}(gHg^{-1})$ は well-defined な $G_n$-集合同型である($khg^{-1}=kg^{-1}(ghg^{-1})$、および $p\cdot kH\mapsto pkg^{-1}(gHg^{-1})$)。したがって任意の部分群が一方に推移的 $\iff$ 他方に推移的。∎

> **註(F5).** (4) の (P3) の部分は **$G$-集合同型だけで従い、(1.3) とも $\langle X\rangle$ の特別な性質とも無関係**である。Sol は「各類が all-or-nothing であることも (1.3) から従う」と書くが、正しい根拠はこれ。**同じ誤りが `search/family-window-survey.g` の実装註(および証明書 JSON の `implementation_note`)にも焼き込まれている**:「条件(3)は $X_n$ を固定するため共役不変ではない — 共役類内で一部だけ通ることがある」は**偽**。実装は保守的(個体ごとに検査)なので観測結果は無害だが、証明書に偽の数学的主張が残っている。

### 補題 D($Q$-像の決定 — 悉皆性の核心)

> (P1)(P3) の下で $Q_H\ne\langle q_1\rangle$。すなわち $Q_H=\langle q_2\rangle$ または $\langle q_3\rangle$。

**証明.** $Q_H=\langle q_1\rangle$ と仮定する。$h\in H$、$\pi(h)=q_1$ を取り $h=a\,q_1$($a\in A$)と書く。補題 C(3) より $a=u+te_1$($u\in U$、$t\in\mathbf Z/n$ が一意)。$u\in U\le H$ だから
$$(te_1)q_1=u^{-1}h\in H .$$
その平方は
$$\bigl((te_1)q_1\bigr)^2=te_1+q_1(te_1)=\bigl(1+\chi_1(q_1)\bigr)te_1=2te_1 ,$$
これは $H\cap\langle e_1\rangle\le\langle X\rangle\cap H=1$ に属す。**$n$ が奇数なので $t=0$**。ゆえに $q_1\in H\cap\langle X\rangle=1$、矛盾。∎

> **註.** 非対称性の出どころは $\chi_1(q_1)=+1$、$\chi_1(q_2)=\chi_1(q_3)=-1$ の一点である。$j\in\{2,3\}$ では上の平方が $0$ になり情報を与えない — だから $\langle q_2\rangle,\langle q_3\rangle$ は残る。**「$q_1\notin H$」からはこの補題は従わない**($a\notin U$ なる $aq_1\in H$ の可能性が残るため)。ここが Sol のスケッチの最大の欠落(F2)。

### 補題 E($U$ の決定)

> (P1)(P3) と $Q_H=\langle q_j\rangle$($j\in\{2,3\}$)の下で、
> $$U=\langle e_j\rangle\oplus\langle \alpha e_1+e_{j'}\rangle=U_{j,\alpha}$$
> なる $\alpha\in\mathbf Z/n$ がただ一つ存在する。 (1.5)

**証明.** $A\trianglelefteq G_n$ ゆえ $H$ は $U=H\cap A$ を正規化し、$h\in H$ の $A$ への共役作用は $\pi(h)$ の作用に一致する。よって **$U$ は $q_j$-安定**。補題 B より $U=U^+\oplus U^-$、$U^+\le A^{q_j,+}=\langle e_j\rangle$、$U^-\le A^{q_j,-}=\langle e_1,e_{j'}\rangle$。
$|U^+|\le n$。また $U^-\cap\langle e_1\rangle\le U\cap\langle e_1\rangle=0$(補題 C(3))だから、射影 $p_{j'}:\langle e_1,e_{j'}\rangle\to\langle e_{j'}\rangle$ は $U^-$ 上単射、$|U^-|\le n$。$|U^+||U^-|=n^2$ より両方ちょうど $n$。ゆえに $U^+=\langle e_j\rangle$、かつ $p_{j'}(U^-)=\langle e_{j'}\rangle$ で $p_{j'}|_{U^-}$ は同型 — すなわち $U^-$ は準同型 $\langle e_{j'}\rangle\to\langle e_1\rangle$ のグラフ、$U^-=\langle\alpha e_1+e_{j'}\rangle$。一意性は $\alpha e_1+e_{j'}$ が $U^-$ の元のうち $e_{j'}$-成分 $1$ をもつ唯一の元であることから。∎

### 補題 F(剰余類の決定)

> 補題 E の状況で、$\beta\in\mathbf Z/n$ がただ一つ存在して
> $$H=U_{j,\alpha}\ \sqcup\ U_{j,\alpha}\cdot(\beta e_1)q_j=H_{j,\alpha,\beta}.$$

**証明.** $|H/U|=2$。$h\in H\setminus U$ を取り $h=aq_j$ と書くと、$Uh=\{(u+a)q_j: u\in U\}$ ゆえ $a$ は $U$ を法として一意。補題 C(3) の $A=U\oplus\langle e_1\rangle$ により $a\equiv\beta e_1\pmod U$ なる $\beta$ が一意に定まる。$H=U\sqcup U(\beta e_1)q_j$ は生成系の形 (1.2) に一致する。∎

**補題 D+E+F で「$\Longrightarrow$」(悉皆性)が閉じた。**

### 補題 G(逆向き:存在・部分群性・一意性)

> 任意の $j\in\{2,3\}$、$\alpha,\beta\in\mathbf Z/n$ に対し (1.2) の $H_{j,\alpha,\beta}$ は位数 $2n^2$ の部分群で、(P1)(P3) を満たす。写像 $(j,\alpha,\beta)\mapsto H_{j,\alpha,\beta}$ は単射。**したがって (P1)(P3) を満たす部分群はちょうど $2n^2$ 個**(1.8)。

**証明.** $U:=U_{j,\alpha}$ は $A$ の部分群で、$\alpha e_1+e_{j'}$ の $e_{j'}$-成分が $1$ ゆえ位数 $n$、$\langle e_j\rangle$ との和は直和、$|U|=n^2$。$U$ は $q_j$-安定($q_je_j=e_j$、$q_j(\alpha e_1+e_{j'})=-(\alpha e_1+e_{j'})$)。$h:=(\beta e_1)q_j$ について
$$h^2=\beta e_1+q_j(\beta e_1)=\bigl(1+\chi_1(q_j)\bigr)\beta e_1=0\qquad(j\in\{2,3\}\Rightarrow\chi_1(q_j)=-1),$$
すなわち **$h$ は対合**。$h$ は $U$ を正規化するので $H=U\rtimes\langle h\rangle$ は位数 $2n^2$ の部分群、$[G_n:H]=2n$(P1)。
(P3): $\langle X\rangle=\langle e_1\rangle\sqcup\langle e_1\rangle q_1$ の元の $Q$-成分は $1$ か $q_1$、$H$ の元の $Q$-成分は $1$ か $q_j\ne q_1$。よって $\langle X\rangle\cap H\subseteq\langle e_1\rangle\cap U$。$se_j+t(\alpha e_1+e_{j'})\in\langle e_1\rangle$ は $e_j$-成分から $s=0$、$e_{j'}$-成分から $t=0$ を強いるので $\langle e_1\rangle\cap U=0$。補題 C(2) より (P3)。
単射性: $H$ から $Q_H=\langle q_j\rangle$ すなわち $j$ が定まり、$U=H\cap A$ から補題 E の一意性で $\alpha$ が定まり、$A=U\oplus\langle e_1\rangle$ から $\beta$ が定まる。∎

> **註(F4).** Sol のスケッチ 3 の「(1.5) により $(w,q_2)^2\in U$ は自動」は、必要な主張を述べていない。$(wq_2)^2\in A\cap H=U$ は $H$ が部分群であることから自明で (1.5) を使わない。**逆向きで実際に必要なのは「$(\beta e_1)q_j$ が対合であること」**であり、その根拠は $\chi_1(q_j)=-1$($\alpha$ とは無関係)である。

### 補題 H(正規化群 — (1.3))

> $H=H_{j,\alpha,\beta}$、$U=U_{j,\alpha}$、$N:=N_{G_n}(H)$ とする。
> 1. $N\cap A=U$($\alpha$ の値によらず)。
> 2. $q\in Q$ が $U$ を保つ $\iff$ $q\in\langle q_j\rangle$ または $\alpha=0$。
> 3. ゆえに $N=H\iff\alpha\ne0$。$\alpha=0$ のとき $N=\langle H,q_1\rangle$、$|N|=4n^2$、$[N:H]=2$。

**証明.** (1) $b\in A$ は($A$ 可換ゆえ)$U$ を保つ。$h=(\beta e_1)q_j$ に対し
$$bhb^{-1}=\bigl((1-q_j)b+\beta e_1\bigr)q_j ,$$
これが $H$ に入る $\iff(1-q_j)b\in U$。$b=x_1e_1+x_2e_2+x_3e_3$ とすると $q_j$ は $e_j$ を固定し他を反転するので
$$(1-q_j)b=2\bigl(x_1e_1+x_{j'}e_{j'}\bigr).$$
$U$ の元で $e_j$-成分が $0$ のものは $\langle\alpha e_1+e_{j'}\rangle$ に限るから、条件は $\exists t:\ 2x_{j'}=t,\ 2x_1=\alpha t$、すなわち $2(x_1-\alpha x_{j'})=0$、**$n$ 奇より** $x_1=\alpha x_{j'}$。他方 $U=\{b: x_1=\alpha x_{j'}\}$(成分表示 $\{(\alpha t,\,s,\,t)\}$ 型)であるから、条件はちょうど $b\in U$。
(2) $g\in N$ は $U=H\cap A$ を保つので $\pi(g)$ が $U$ を保つ。$q_j$ は保つ。$q_1$(したがって $q_{j'}=q_1q_j$)については $q_1e_j=-e_j\in U$ は良いが
$$q_1(\alpha e_1+e_{j'})=\alpha e_1-e_{j'}\in U\iff \alpha e_1-e_{j'}\in\langle\alpha e_1+e_{j'}\rangle\iff \exists t:\ t=-1,\ t\alpha=\alpha\iff 2\alpha=0\iff\alpha=0$$
(**$n$ 奇**)。
(3) $\alpha\ne0$ なら $\pi(N)=\langle q_j\rangle$、$|N|=|N\cap A|\cdot2=2n^2=|H|$、ゆえに $N=H$。$\alpha=0$ なら $q_1$ は $U=\langle e_j,e_{j'}\rangle$ を保ち、さらに
$$q_1hq_1^{-1}=q_1(\beta e_1)q_jq_1=(\beta e_1)q_j=h\qquad(q_1e_1=e_1,\ Q\ \text{可換})$$
すなわち $q_1$ は $h$ を中心化するので $H$ を正規化する。$q_1\notin H$ だから $N\supsetneq H$、$\pi(N)=Q$ より $|N|=4n^2$。∎

> **註.** (2)(3) のどこにも **$\alpha$ の可逆性は使われない**。効くのは $\alpha\ne0$ だけ。これが「$n=9$ で $\alpha=3,6$ も good」の正体である(§5.3)。

### 補題 I(共役 — (1.9)(1.10))

> $n$ を奇数とする。
> 1. $b\in A$ に対し $bH_{j,\alpha,\beta}b^{-1}=H_{j,\alpha,\;\beta+2(x_1-\alpha x_{j'})}$。$b$ が $A$ を走ると第 3 添字は $\mathbf Z/n$ 全体を走る。
> 2. $q_1H_{j,\alpha,\beta}q_1^{-1}=H_{j,-\alpha,\beta}$。
> 3. $H_{j,\alpha,\beta}$ の $G_n$-共役類は $\{H_{j,\pm\alpha,\gamma}:\gamma\in\mathbf Z/n\}$。よって (1.9) が成立し、$\alpha\ne0$ の類は大きさ $2n$、$\alpha=0$ の類は大きさ $n$。三述語を満たす部分群の類は $2\cdot\frac{n-1}{2}=n-1$ 個。 (1.10)

**証明.** (1) $bUb^{-1}=U$、$bhb^{-1}=((1-q_j)b+\beta e_1)q_j$、$(1-q_j)b=2(x_1e_1+x_{j'}e_{j'})=2x_{j'}(\alpha e_1+e_{j'})+2(x_1-\alpha x_{j'})e_1$ の第 1 項は $U$ に入るので、$A=U\oplus\langle e_1\rangle$ における $\langle e_1\rangle$-成分は $\beta+2(x_1-\alpha x_{j'})$。$2$ が可逆かつ $x_1$ が自由なのでこれは全射。
(2) $q_1Uq_1^{-1}=\langle -e_j,\ \alpha e_1-e_{j'}\rangle=\langle e_j,\ (-\alpha)e_1+e_{j'}\rangle=U_{j,-\alpha}$、$q_1hq_1^{-1}=h$(補題 H(3) の計算)。
(3) $\pi(gHg^{-1})=\pi(g)Q_H\pi(g)^{-1}=Q_H$($Q$ 可換)ゆえ $j$ は不変。$G_n=A\cdot\langle q_1,q_j\rangle$ で、$q_j=(-\beta e_1)\cdot h$($h\in H$)だから $q_j$ による共役は $A$ の元による共役と $H$ を保つ共役の合成 — したがって共役軌道は (1) と (2) で生成される。$n$ 奇かつ $\alpha\ne0$ なら $\alpha\ne-\alpha$ なので軌道の大きさは $2n$、$\alpha=0$ なら $n$。検算: $|G_n|/|N|=4n^3/2n^2=2n$、$4n^3/4n^2=n$(補題 H)。∎

### 系(個数 — (1.7)(1.8))

$$\#\{H:\mathrm{P1},\mathrm{P3}\}=2\cdot n\cdot n=2n^2,\qquad
\#\{H:\mathrm{P1},\mathrm{P2},\mathrm{P3}\}=2\cdot(n-1)\cdot n=2n(n-1),$$
$$\#\{H:\mathrm{P1},\mathrm{P3},\ \lnot\mathrm{P2}\}=2n\quad(\alpha=0\ \text{の層}\ \text{— 2 類・各 }n),\qquad
\#\text{共役類}(\text{三述語})=n-1 .$$
**$K^{(3)}$: $18=12+6$、$K^{(5)}$: $50=40+10$** はこの $2n^2=2n(n-1)+2n$ の $n=3,5$ での実現である。∎

---

## 5. 判別子 $(j,[\alpha])$ の well-defined 性

### 5.1 何が $(j,\alpha)$ を決めるか

$A=[G_n,G_n]$ は特性(補題 A(4))。$\bar q_1:=\pi(X)$、$\bar q_2:=\pi(Y)$、$\bar q_3:=\bar q_1\bar q_2$ は **marking $(X,Y)$ から決まる** $G_n/A\cong C_2^2$ の 3 元。$\chi_i$ をその核が $\langle\bar q_i\rangle$ である指標、$A^{\chi_i}$ を対応する固有線とすると:

* $j(H):=2$ if $\pi(H)=\langle\bar q_2\rangle$、$:=3$ if $\pi(H)=\langle\bar q_3\rangle$ — **marking のみから決まる**。
* $\alpha(H)$: $U=H\cap A$ の $q_j$ に関する $(-1)$-固有部分 $U^-\le A^{\chi_1}\oplus A^{\chi_{j'}}$ は、**$A^{\chi_1}$ と $A^{\chi_{j'}}$ の生成元を選んで初めて**「傾き」として数値化される。

> **【要注意・F7】** 生成元を $e_1\mapsto ue_1$、$e_{j'}\mapsto we_{j'}$($u,w\in(\mathbf Z/n)^\times$)と取り替えると
> $$\alpha\ \longmapsto\ \alpha\,w\,u^{-1}.$$
> したがって **$\alpha$ は「固有線の生成元の組」を固定して初めて意味をもつ**。$\pm1$ だけの曖昧さで済むのは、その組を固定したときである。

### 5.2 marking が生成元を与える

補題 A(3) の計算から
$$X^2=2e_1,\qquad Y^2=2e_2,\qquad Z^2=2e_3$$
($(XY)^2=-2e_3$ ゆえ $Z^2=((XY)^{-1})^2=2e_3$)。**$2$ が可逆**なのでこれらは各固有線の生成元であり、しかも **3 本とも同じ単元 $2$ 倍**。$u=w=2$ のとき $\alpha\mapsto\alpha\cdot2\cdot2^{-1}=\alpha$ だから:

> **系.** marking $(X,Y,Z)$ に付随する正準生成元 $(X^2,Y^2,Z^2)$ を用いれば $\alpha$ は一意に定まる。補題 I によりその $G_n$-共役不変な形は $[\alpha]\in((\mathbf Z/n)\setminus\{0\})/\{\pm1\}$ であり、$(j,[\alpha])$ は三述語を満たす部分群の $G_n$-共役類の**完全不変量**である。 (1.11)

### 5.3 $n=9$ の $\alpha=3,6$

補題 H は $\alpha$ の可逆性をどこにも使わない($\alpha\ne0$ のみ)。$n=9$ で $\alpha=3$:$U_{2,3}=\langle e_2,\,3e_1+e_3\rangle$ の位数は $81=n^2$($3e_1+e_3$ の位数は $e_3$-成分から $9$)、$q_1$ が $U$ を保つ条件 $2\alpha=0$ は $6\ne0$ より不成立、よって $N=H$ — **good**。$[3]=\{3,-3\}=\{3,6\}$ は 1 つの類。したがって
$$\bigl((\mathbf Z/9)\setminus\{0\}\bigr)/\{\pm1\}=\{[1],[2],[3],[4]\}\ (4\ \text{個}),\qquad
\text{類数}=2\times4=8=n-1 .$$
**$(\mathbf Z/n)^\times/\{\pm1\}$ と狭めると 6 になり、実測 8 と合わない** — Sol の指摘は正しい。

### 5.4 $\operatorname{Aut}(G_n)$-軌道は別物(Q1.4 の警告の中身)

対角写像 $e_i\mapsto u_ie_i$($u_i\in(\mathbf Z/n)^\times$)は $Q$ の作用($\pm1$ 倍)と可換なので $G_n$ の自己同型。座標置換 $S_3$($D_n^3$ の 3 因子の置換)は $A,Q$ を保つのでやはり自己同型で、互換 $(2\,3)$ は $H_{2,\alpha,\beta}\mapsto H_{3,\alpha,\beta}$ を与える。よって
$$\operatorname{Aut}(G_n)\ \text{の作用で}\quad \alpha\mapsto u\alpha\ (u\in(\mathbf Z/n)^\times),\qquad j=2\leftrightarrow3$$
が可能で、**$\operatorname{Aut}(G_n)$-軌道の完全不変量は $d:=\gcd(\alpha,n)$**、軌道数は $\tau(n)-1$($d\mid n$, $d<n$)。$n=3$ では 1 軌道 — これは既存記録(対話帳 T-11「良い 12 個が $\operatorname{Aut}(G_3)$ の一軌道、$G_3$-共役では $6+6$ の二類」)と一致する。**「marking を固定した $G_n$-共役類($n-1$ 個)」と「$\operatorname{Aut}$-軌道($\tau(n)-1$ 個)」を同一視しない**という Sol の Q1.4 の警告は、群論的にはこの $\gcd$ への潰れのことである。

---

## 6. 命題 ODD-P(ordered passport の閉形式)— 新規

> **命題 ODD-P.** $n$ 奇、$H=H_{j,\alpha,\beta}$、$d:=\gcd(\alpha,n)$($\gcd(0,n)=n$)とする。$G_n/H$($2n$ 点)上の置換の型は
> $$j=2:\quad\bigl(\bar X,\bar Y,\bar Z\bigr)\ \text{の型}=\Bigl(\,2n\ ,\ 2^{\,n-1}1^2\ ,\ (2n/d)^{\,d}\,\Bigr),$$
> $$j=3:\quad\bigl(\bar X,\bar Y,\bar Z\bigr)\ \text{の型}=\Bigl(\,2n\ ,\ (2n/d)^{\,d}\ ,\ 2^{\,n-1}1^2\,\Bigr).$$
> とくに **ordered passport が $K^{(3)},K^{(5)}$ と同じ $(2n,\,2^{n-1}1^2,\,2n)$ になるのは $j=2$ かつ $\alpha\in(\mathbf Z/n)^\times$ のときに限る**。$j=2$ でこの passport をもつ類は $\varphi(n)/2$ 個。

**証明.** (P3) より $\langle X\rangle=\{te_1,\ (te_1)q_1: t\in\mathbf Z/n\}$ は $H$ の左剰余類の完全代表系。剰余類を $R(t,\varepsilon)$($\varepsilon\in\{0,1\}$、$R(t,0)=te_1H$、$R(t,1)=(te_1)q_1H$)と書く。

**($\bar X$)** $\langle X\rangle$ は単純推移なので $X$ は正則、型は $2n$($1$ 個の $2n$-サイクル)。

**($j=2$ の $\bar Y$)** $H$ の $Q$-成分は $\{1,q_2\}$。$\pi(Y)=q_2$ ゆえ $\varepsilon$ は保存される。$\varepsilon=0$:
$$Y\cdot(te_1)=\bigl((1,1,1)+q_2(te_1)\bigr)q_2=(1-t,\,1,\,1)q_2 ,$$
これが $R(t',0)$ に入る条件は $(1-t-t',1,1)\in\beta e_1+U=\{(\alpha s+\beta,\,w,\,s)\}$、すなわち $s=1$、$1-t-t'=\alpha+\beta$、つまり
$$t'=(1-\alpha-\beta)-t .$$
同様に $\varepsilon=1$ では $t'=(1+\alpha-\beta)-t$。いずれも $\mathbf Z/n$ 上の**鏡映**で、$n$ 奇より不動点 1・二輪 $(n-1)/2$。両ブロック合わせて型 $2^{\,n-1}1^2$($\alpha$ に依らない)。

**($j=2$ の $\bar Z$)** $\pi(XY)=q_3\notin\{1,q_2\}$ ゆえ $XY$ は 2 ブロックを入れ替える。$(XY)^2=-2e_3$(補題 A(3))。$e_3$ のブロック $\varepsilon=0$ 上の作用は
$$e_3\cdot(te_1)=(t,0,1),\qquad (t-t',0,1)\in U=\{(\alpha s,w,s)\}\iff s=1,\ t'=t-\alpha ,$$
すなわち $t\mapsto t-\alpha$。よって $(XY)^2$ は $t\mapsto t+2\alpha$、その軌道長は $n/\gcd(2\alpha,n)=n/d$($n$ 奇)。ブロックを入れ替える置換 $\sigma$ で $\sigma^2$ の各サイクル長が $\ell$ なら $\sigma$ のサイクル長は $2\ell$ だから、$XY$(したがって $Z=(XY)^{-1}$)の型は $(2n/d)^{d}$。

**($j=3$)** 同様。$\pi(Y)=q_2\notin\{1,q_3\}$ ゆえ $Y$ はブロックを入れ替え、$Y^2=2e_2$、$e_2$ のブロック上の作用は $t\mapsto t-\alpha$ で型 $(2n/d)^d$。$\pi(XY)=q_3$ はブロックを保存し、$XY\cdot(te_1)=(2-t,-1,-1)q_3$ から $t'=(2+\alpha-\beta)-t$(鏡映)、型 $2^{\,n-1}1^2$。∎

**帰結(F8).** Sol の Q1.5「ordered passport を $K^{(3)}/K^{(5)}$ と同じ $(2n,2^{n-1}1^2,2n)$ に取れば $j=2$ 側を選ぶ。**しかし $j=2$ としても $[\alpha]$ が $(n-1)/2$ 個残る**」— 後半は誤り。残るのは $\alpha\in(\mathbf Z/n)^\times$ の $\varphi(n)/2$ 個である。

| $n$ | 三述語の類数 $n-1$ | passport 込みの類数 $\varphi(n)$ | $j$ 固定後 $\varphi(n)/2$ | Sol の $(n-1)/2$ |
|---|---|---|---|---|
| 3 | 2 | 2 | **1**(passport で一意に決まる) | 1 |
| 5 | 4 | 4 | 2 | 2 |
| 7 | 6 | 6 | 3 | 3 |
| **9** | **8** | **6** | **3** | **4 ← 誤り** |
| 11 | 10 | 10 | 5 | 5 |
| 15 | 14 | 8 | **4** | 7 ← 誤り |
| 21 | 20 | 12 | **6** | 10 ← 誤り |
| 25 | 24 | 20 | **10** | 12 ← 誤り |

Sol の**結論**(「追加規約なしの単数形『正典 $\Lambda_n$』は $n\ge5$ で未定義」)は $\varphi(n)/2\ge2$($n\ge5$)ゆえ**無傷**。$n=3$ では passport が類を一意に決める(既存記録 T-11 と整合)。ただし下流に効くのは次の一点である:

> **$\alpha$ が非単元の good 窓は、$K^{(3)}/K^{(5)}$ と同じ幾何型(ordered passport)を**もたない**。第 3(または第 2)の印付き点での分岐指数が $2n$ でなく $2n/d$ に落ちる。**「$e=n$ の全分岐 regular detector」等、passport / 分岐構造を前件にする下流の条項は、非単元 $\alpha$ の窓を自動的には含まない。** Sol の Q6.1 の提案 $H_n^{\mathrm{fun}}=H_{2,1,0}$ は $\alpha=1$(単元)なので安全側。

---

## 7. 観測データとの照合(事後・二系統)

**独立実装**(node・GAP 非依存・`SubgroupsSolvableGroup` 不使用)で次を行った。共有前提は正典 §3 の $\psi_n$ の生成元像のみ。

* $D_n^3$ の中で $\langle(r,s,s),(rs,r,rs)\rangle$ を直接閉包生成し、$|G_n|=4n^3$、$a_i,q_j$ の所属、符号表、$X=a_1q_1$、$Y=a_1a_2a_3q_2$、$\operatorname{ord}(X)=2n$、模型 $A\rtimes Q$ との同型を検証(すべて PASS)。
* **位数 $2n^2$ の部分群を悉皆列挙**(補題 C(1) の「$|H\cap A|=n^2$、$|\pi(H)|=2$」を使い、$A$ の位数 $n^2$ 部分群を双対格子から全列挙 → $q$-安定性 → 剰余類)。列挙された各 $H$ の部分群性を積閉包で再確認。
* 各 $H$ について (P2)(P3) を独立実装で判定。

| $n$ | $\vert G_n\vert$ | $2n^2$ | 実測 P1&P3 | $2n(n-1)$ | 実測 P1&P2&P3 | 類数 $n-1$ | 実測 | JSON `passing_H_count` | JSON `qualifying_..._count` | JSON `self_norm_total` | 実測(P3 なし) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 108 | 18 | **18** | 12 | **12** | 2 | **2** | 12 ✓ | 2 ✓ | 18 | **18** ✓ |
| 5 | 500 | 50 | **50** | 40 | **40** | 4 | **4** | 40 ✓ | 4 ✓ | 60 | **60** ✓ |
| 7 | 1372 | 98 | **98** | 84 | **84** | 6 | **6** | 84 ✓ | 6 ✓ | 126 | **126** ✓ |
| 9 | 2916 | 162 | **162** | 144 | **144** | 8 | **8** | 144 ✓ | 8 ✓ | 270 | **270** ✓ |
| 11 | 5324 | 242 | **242** | 220 | **220** | 10 | **10** | 220 ✓ | 10 ✓ | 330 | **330** ✓ |

さらに全 $n$ で「各類サイズ $=2n$」「各類で $j$ 一定・$\alpha$ は $\{\pm\alpha\}$」「$\{P1,P3\}=$ (1.2) の族(集合として一致)」「$N=H\iff\alpha\ne0$」が PASS。
**自己正規化クラス数**も JSON と一致(3, 6, 9, 15, 15)。

**逆向きと (1.3) と命題 ODD-P の合成数 $n$ での追試**(悉皆列挙はせず (1.2) の族のみ):$n=3,5,9,13,15,21,25$ で「部分群性・$|H|=2n^2$・(P3)・$(\mathrm{P2}\iff\alpha\ne0$)」「passport $=(2n/d)^d$, $d=\gcd(\alpha,n)$」がすべて PASS。

> **状態札**: この照合により、JSON の 5 項目(`pn_size` / `target_H_order` / `passing_H_count` / `qualifying_conjugacy_class_count` / `self_normalizing_conjugate_total` / `self_normalizing_rep_class_count`)は **単系統 OBSERVED → cross-checked** に上げてよい。**verified(Lean)ではない。** 命題 ODD-P の閉形式は**紙上証明済み**で、数値はその確認。

---

## 8. FINDING 一覧

| # | 種別 | 箇所 | 内容 | 影響 |
|---|---|---|---|---|
| **F1** | **GAP(埋めた)** | (1.1) | $G_n=A_n\rtimes Q$・符号表・$X=a_1q_1$ が正典からの**導出でなく引用**。とくに「$X$ の $A$-成分が、$X$ の $Q$-成分の $+1$-固有線に載る」という組み合わせが load-bearing($\operatorname{ord}(X)=2n$ と補題 D の非対称性の**両方**がここに乗る)。$A\le G_n$ には $n$ 奇($\langle r^2\rangle=\langle r\rangle$)が要る | 補題 A で閉じた |
| **F2** | **GAP(実質・悉皆性の核心)** | スケッチ 1 | 「したがって $H$ の $Q$-像は $\langle q_2\rangle$ または $\langle q_3\rangle$」が**無証明**。$q_1\notin H$ からは従わない($a\notin U$ なる $aq_1\in H$ が原理的に残る)。正しい論法は $A=U\oplus\langle e_1\rangle$ → $(te_1)q_1\in H$ → 平方 $2te_1=0$ → $t=0$ → $q_1\in H$ の矛盾 | **これが落ちると (1.2) の悉皆性が立たない**。補題 D で閉じた |
| **F3** | GAP(明示化) | スケッチ 2 | 「$U$ が $q_2$-安定」の根拠($U=H\cap A$ が $H$-正規、$h$ の $A$ への作用 $=\pi(h)$)が書かれていない。半単純分解も補題の形になっていない | 補題 B/E で閉じた |
| **F4** | **GAP(逆向き未証明)** | (1.7)(1.8) | スケッチは「$\Rightarrow$」のみ。個数主張には (a) 各 $H_{j,\alpha,\beta}$ が実際に述語を満たすこと、(b) パラメータ付けの単射性が要る。さらに「(1.5) により $(w,q_2)^2\in U$ は自動」は**必要な主張を述べていない**(自明な事実の言い換え)。実際に要るのは **$(\beta e_1)q_j$ が対合**($\chi_1(q_j)=-1$ ゆえ・$\alpha$ 無関係) | (1.7)(1.8) は補題 G なしでは**上界にすぎない**。補題 G で閉じた |
| **F5** | **誤帰属 + 実装註の誤り** | (1.3) 直後 / GAP script | 「各類が all-or-nothing であることも (1.3) から従う」— 正しい根拠は $G_n/H\cong G_n/gHg^{-1}$ という **$G$-集合同型**で (1.3) と無関係。**同型の誤りが `search/family-window-survey.g` の実装註と証明書 JSON の `implementation_note` にある**:「条件(3)は $X_n$ を固定するため共役不変ではない」は**偽**((P1) の下で (P3)$\iff\langle X\rangle\cap H=1$ で共役不変) | 観測結果は無害(実装は保守的)。**証明書に偽の数学的主張が焼き込まれている** — 次版で訂正推奨 |
| **F6** | **数値の衝突(読み手の罠)** | (1.8) の「$n=3$ で $18=12+6$」 | この $18$ は $2n^2$(**P1&P3** を満たす総数)。JSON の `self_normalizing_conjugate_total`$=18$($n=3$)は **P1&P2**(P3 抜き)の総数で**別の集合**。$n=3$ でのみ両者が偶然 $18$、しかも**両方が $12+6$ に割れる**(前者 $=12$ good $+\,6$($\alpha=0$)、後者 $=12$ good $+\,6$(非推移))。$n=5$ では $50$ 対 $60$ で分岐 | 引用時は必ず述語の組を明記。$n=3$ だけを見て一般則を読むと取り違える |
| **F7** | 精密化要 | (1.11) | $\alpha$ は $A^{\chi_1}$ と $A^{\chi_{j'}}$ の**生成元の選択**に依存($e_1\mapsto ue_1$, $e_{j'}\mapsto we_{j'}$ で $\alpha\mapsto\alpha wu^{-1}$)。$\pm1$ の商で済むのは marking 由来の正準生成元 $X^2,Y^2,Z^2$(一様に $2$ 倍)を採るとき。この一行がない | (1.11) の well-defined 性の前提。$\operatorname{Aut}$ 軌道では $\gcd(\alpha,n)$ に潰れる(§5.4)— Q1.4 の警告の群論的中身 |
| **F8** | **誤り(新規発見)** | Q1.5 | 「$j=2$ としても $[\alpha]$ が $(n-1)/2$ 個残る」は **$n=9$(および $n=15,21,25,\dots$)で誤り**。ordered passport の残り一成分は $(2n/d)^d$, $d=\gcd(\alpha,n)$(命題 ODD-P)なので、$K^{(3)}/K^{(5)}$ 型 passport を課すと $\alpha$ は**単元に限られ**、残るのは $\varphi(n)/2$ 個。$n=9$: 4 でなく **3** | Sol の**結論**(単数形 $\Lambda_n$ は $n\ge5$ で未定義)は無傷。だが**非単元 $\alpha$ の窓は $K^{(3)}/K^{(5)}$ と同じ幾何型でない**。passport / 分岐指数を前件にする下流条項(「$e=n$ の全分岐 regular detector」等)は非単元 $\alpha$ を自動的には含まない。**Q1.6 の「任意の一類について (W3)(W4)(W5) が成立する」は再検討を要する** |
| **F9** | 射程の限定 | Q1.6 | 本命題は**有限群 $G_n$ の部分群論**であり、GT-shadow・genuine・arithmetical には何も言わない。(W3)(W4)(W5) の内容は本文にないので、「任意の一類について成立」は本命題からは従わない | 【要確認】(W3)(W4)(W5) の定義を明示のうえ、F8 の $d>1$ 層で個別に検査すべき |

**監査範囲外(触れていない)**: (1.12)($\vert\operatorname{Aut}(G_n)\vert=6n^3\varphi(n)^3$)は (1.1)–(1.11) の範囲外なので監査していない。ただし §5.4 で $((\mathbf Z/n)^\times)^3\rtimes S_3$ が実際に $\operatorname{Aut}(G_n)$ に埋まることは示した(位数 $6\varphi(n)^3$)。$n=3$ の値 $1296$ は既存記録(T-10)と一致する。Q2–Q6 全体、および $u$・平方類・$\widehat c_\mu$ には一切触れていない。

---

## 9. 「$2\in(\mathbf Z/n)^\times$」の使用箇所(task 1 の要請)

| # | 箇所 | 使い方 | $n$ が偶数なら |
|---|---|---|---|
| 1 | 補題 A(1) | $\langle r^2\rangle=\langle r\rangle$ ⇒ $A\le G_n$、$\vert G_n\vert=4n^3$ | 破綻($\vert G_n\vert=4(n/2)^3$・正典 p.15 の別分岐) |
| 2 | 補題 A(3) | $\operatorname{ord}(a_1q_1)=\operatorname{lcm}(n,2)=2n$ | 破綻 |
| 3 | 補題 A(4) | $(q_1-1)A=\langle 2e_2,2e_3\rangle=\langle e_2,e_3\rangle$ ⇒ $A=[G_n,G_n]$ | 破綻(指数 2 の像しか出ない) |
| 4 | 補題 B | 固有空間分解 $v=\frac12(v+qv)+\frac12(v-qv)$(**Sol の (1.5) の根拠**) | 破綻($\mathbf Z/n[C_2]$ が半単純でない) |
| 5 | 補題 C(1) | $\vert H\vert=2n^2$ の $2$-指数が $1$ ⇒ $\vert\pi(H)\vert=2$、$\vert U\vert=n^2$ | 破綻 |
| 6 | **補題 D** | $2te_1=0\Rightarrow t=0$(**$Q$-像から $\langle q_1\rangle$ を排除する唯一の道具**) | 破綻 |
| 7 | 補題 H(1) | $2(x_1-\alpha x_{j'})=0\Rightarrow x_1=\alpha x_{j'}$(**Sol の (1.6)**) | 破綻 |
| 8 | 補題 H(2) | $2\alpha=0\Rightarrow\alpha=0$(自己正規化判定の心臓) | 破綻 |
| 9 | 補題 I(1) | $\beta\mapsto\beta+2(\cdot)$ が全射 | 破綻 |
| 10 | 補題 I(3) | $\alpha\ne0\Rightarrow\alpha\ne-\alpha$ ⇒ 類サイズ $2n$・類数 $n-1$ | 破綻(類構造が変わる) |
| 11 | §5.2 | $X^2=2e_1$ 等が生成元 ⇒ marking から正準生成元 | 破綻 |
| 12 | 命題 ODD-P | $\gcd(2\alpha,n)=\gcd(\alpha,n)$、鏡映の不動点が 1 個 | 破綻 |

$\chi_1(q_j)=-1$($j\in\{2,3\}$)による「$(\beta e_1)q_j$ が対合」(補題 G)は**符号から来るのであって $n$ の奇偶からではない** — この 1 点だけが偶数でも生き残る。

---

## 10. 未閉鎖項

* 【ODD-H-1】本稿は**紙上証明**であり Lean 検証はしていない。有限群の等式 checker への写像は自然(整数行列 $(\mathbf Z/n)^3\rtimes C_2^2$ と部分群の有限検査)なので、Lean 化候補として登録する価値がある。
* 【ODD-H-2】§7 の合成数 $n$($15,21,25$)は **(1.2) の族の検査のみ**で悉皆列挙ではない(悉皆性は §4 の証明が担う。数値による悉皆確認は $n\le11$ のみ)。
* 【ODD-H-3】F8/F9: (W3)(W4)(W5) の内容が本稿からは参照できないため、$d=\gcd(\alpha,n)>1$ の層で (W3)(W4)(W5) が成立するかは **UNKNOWN**。Q1.6 の「任意の一類について成立」は、この確認まで candidate に留めるべき。
* 【ODD-H-4】F5 の実装註の訂正(証明書 JSON の `implementation_note`)は上書きせず次版で。

---

## 11. 追補(裁定 105 の追加設問)— $\Phi(\mathrm{GT}(K^{(9)}))$ の類への作用

**結論を先に: Sol の (1.13)(1.14) と Q1.5 末尾の線形部論法は正しい。$\mathrm{GT}(K^{(9)})$ の 108 shadow は $\boldsymbol{108/108}$ で類 $(2,[1])$ を保つ。GAP 実測の $18/108$ は `search/k9-package.g` の 1 行の実装バグ(規約 W-4 違反)であり、その値は完全に再現・説明できる。**

### 11.1 $\Phi_{m,f}$ の $A$ への誘導作用(設問 1)

$u:=2m+1$、$f$ の $G_n$ での値を $F=(F_1,F_2,F_3)\in A$(Thm 4.3 では $F=(2k,-2k,\varkappa(m))$)とする。$\Phi=\Phi_{m,f}$ は $X\mapsto X^u$、$Y\mapsto F^{-1}Y^uF$。補題 A(3) の座標で:

$$X^u=(ue_1)q_1,\qquad Y^u=(1,u,1)q_2,\qquad F^{-1}Y^uF=(1-2F_1,\;u,\;1-2F_3)\,q_2 .$$

$X^2=2e_1,\;Y^2=2e_2,\;Z^2=2e_3$ の像を取って($2$ が可逆):

$$\boxed{\ \Phi|_A=\operatorname{diag}\bigl(u,\;u,\;1-2\varkappa(m)\bigr),\qquad 1-2\varkappa(m)=\begin{cases}+u&(m\ \text{偶})\\-u&(m\ \text{奇})\end{cases}\ }$$

すなわち **$\operatorname{diag}(u,u,\pm u)$ — Sol の主張どおり**。さらに $\Phi(q_1)=q_1$、$\Phi(q_2)=\bigl((1-u-4k)e_1\bigr)q_2$ ゆえ **$\Phi$ が $G_n/A$ に誘導する写像は恒等**、したがって $\Phi$ は 3 本の指標線を**各々保つ**。

**実測(独立実装・n=9・全 108 件)**: 固有値は 12 個の $m$ すべてで上式と一致($m=3$: $(7,7,2)=(7,7,-7)$、$m=9$: $(1,1,8)=(1,1,-1)$、…)。**破れている箇所はない。**

### 11.2 正しい変換則(設問 2)

$\delta:=+1$($m$ 偶)$/-1$($m$ 奇)、$c:=1-u-4k$ と置くと

$$\boxed{\ \Phi_{m,f}\bigl(H_{2,\alpha,\beta}\bigr)=H_{2,\;\delta\alpha,\;\beta u+c},\qquad
\Phi_{m,f}\bigl(H_{3,\alpha,\beta}\bigr)=H_{3,\;\alpha,\;\ast}\ }$$

($j=2$ 側は $\langle\alpha e_1+e_3\rangle\mapsto\langle\alpha ue_1+\delta ue_3\rangle=\langle\delta\alpha e_1+e_3\rangle$;$j=3$ 側は $\langle\alpha e_1+e_2\rangle\mapsto\langle u(\alpha e_1+e_2)\rangle$ で $\alpha$ が**そのまま**保たれる)。
**実測**: $n=9$ の全 shadow × 全 good 部分群 $108\times(2\cdot8\cdot9)=15552$ 対で上式が **PASS**。

$\delta=\pm1$ だから **$[\alpha]$ は常に保たれる**。$\alpha\mapsto u\alpha$ 型ではない。

> **構造的な理由**: $\operatorname{Aut}(G_n)$ の対角部は $(u_1,u_2,u_3)\in((\mathbf Z/n)^\times)^3$ を自由に取れる(§5.4)が、**$\Phi(\mathrm{GT}(K^{(n)}))$ の対角部は $(u,u,\pm u)$ に制限される** — 第 1 座標と第 3 座標の比が $\pm1$ に固定されるので、$\alpha$ を単元倍する余地が構造的に存在しない。$[\alpha]$ が GT-不変なのはこのためである。

### 11.3 GT-軌道構造(設問 3)

$j$ も $[\alpha]$ も保たれるので、**$\mathrm{GT}(K^{(n)})$ が $(j,[\alpha])$-類の集合に誘導する作用は自明**:

$$\text{GT-軌道は全て 1 点、軌道数}=n-1 .$$

したがって **Sol の (1.14)「(W5) は $n-1$ 類を一つも削らない・全類 PASS」は確認された**。$H^{\mathrm{fun}}=H_{2,1,0}$ の GT-軌道は自分の類 $(2,[1])$ ただ一つである。
**帰結(設計)**: 「canonical detector を GT-軌道単位で選ぶ」という設計変更は**成り立たない**(その動機だったデータがバグ由来)。類の選択問題は依然として未解決で、現時点の候補は (i) Sol Q6.1 の reduction-functorial な $\alpha=1$、(ii) 本稿 §6 の **ordered passport による $\alpha$ 単元への絞り込み**($n-1\to\varphi(n)$)の 2 つ。

### 11.4 実装バグの特定(設問 1 の「破れ」の正体)

`search/k9-package.g` 221 行:

```gap
PhiHom := GroupHomomorphismByImages(P9.G, P9.G, [P9.X, P9.Y], [P9.X^u, f^-1 * P9.Y^u * f]);
```

**規約 W-4** により paper 語 $f^{-1}y^uf$ の GAP 実装は `AbstractProd([f^-1, Y^u, f])` $=$ `f * Y^u * f^-1` でなければならない。同スクリプトは $X,Y$ の構成では `AbstractProd` を使い、**その罠を 66–74 行のコメントで自ら詳細に記録している**にもかかわらず、221 行だけ生の GAP 順で書いている — 定義ノート §1.5.1 が「最悪」と名指しする **「判定式を GAP 順・語を paper 順」の混在**そのもの。

**この 1 行だけで観測値が完全に再現される**(独立実装で確認):

| | 規約 A(paper・正) | 規約 B(反転 = 221 行が計算したもの) |
|---|---|---|
| $\Phi|_A$ の第 3 固有値 | $1-2\varkappa=\pm u$(常に単元) | $1+2\varkappa=\;2-u$($m$ 偶)$/\;u+2$($m$ 奇)— **単元とは限らない** |
| 自己同型か | **108/108** | **54/108 のみ**($m=3,14$ で固有値 $0$、$m=2$ で $6$、$m=8,9,15$ で非単元) |
| $\Phi(H^{\mathrm{fun}})$ が類 $(2,[1])$ に留まる | **108/108** | **18/108** |
| 留まる $m$ | 全部 | $\{0,17\}$ のみ |

規約 B での生き残り条件は $u\equiv\pm(1+2\varkappa)$、すなわち「$m$ 偶かつ $u\equiv1$」または「$m$ 奇かつ $u\equiv-1$」$\pmod 9$ — $\mathcal X_9$ の中でこれを満たすのは $m=0,17$ の 2 個、$2\times9=18$ 件。**実測 `w5_bonus_fail = 90` と完全一致**。落ちる $m$ の集合 $\{2,15\},\{3,14\},\{5,12\},\{6,11\},\{8,9\}$ も一致する。

> **$m+m'=17$ の対称性について**: $m+m'=17\iff u'\equiv-u\pmod{36}$ で、対の一方は偶・他方は奇。規約 B の生き残り条件は対の内部で高々一方しか満たせないため、$(0,17)$ 以外の対が全滅する。**この対称性はバグの失敗パターンの副産物であって、類の変換則の痕跡ではない**(正しい規約では対の両方が留まる)。

**なぜ silent だったか**: `GroupHomomorphismByImages` は**非単射な自己準同型**でも `fail` を返さない。規約 B の 54 件はまさに非単射自己準同型で、スクリプトは `PhiHom = fail` しか検査していないため素通りし、`Image(PhiHom, H9)` が位数の小さい部分群になって「非共役」と報告された。

**修理仕様(実装者向け)**
1. 221 行を `AbstractProd([f^-1, P9.Y^u, f])` に置換(または `f * P9.Y^u * f^-1`)。
2. **`IsBijective(PhiHom)` を fail-closed の assert に追加**。Thm 4.3 が $K^{(n)}$ の isolated 性を主張する以上、$T_{m,f}$ は自己同型でなければならない — 非単射が出たら実装の誤りである。
3. **回帰 fixture**: 「$\Phi|_A=\operatorname{diag}(u,u,\pm u)$」を各 shadow で assert(規約が反転すると第 3 成分が非単元になるので、この 1 行が同型の罠を全部捕まえる)。
4. lint 規則の提案: **paper 由来の式を GAP で書くときは必ず `AbstractProd` を通す**(生の `*` で 3 項以上の積を書いたら警報)。

### 11.5 副産物 — GT($K^{(9)}$) 較正の cross-check

上記の検証のため、簡約 hexagon (3.10)(3.11) を**独立実装で再列挙**した(paper 積・$f\in[G_9,G_9]=A$ の 729 個 × charming 12 個)。結果:

| 量 | 独立実装(node) | `k9_package_20260728.json` |
|---|---|---|
| candidate_total | $12\times729=8748$ | 8748 ✓ |
| (3.10) fail | **7776** | 7776 ✓ |
| (3.11) fail | **864** | 864 ✓ |
| generation fail | **0** | 0 ✓ |
| $\vert\mathrm{GT}(K^{(9)})\vert$ | **108** | 108 ✓ |
| Thm 4.3 の形 $(t,-t,\varkappa(m))$ との一致 | **108/108** | (未記録) |

さらに $m$ ごとの内訳 9 件ずつも一致。**したがって cert の `task1_gt_k9_calibration` は cross-checked に上げてよい**(hexagon 層は正しい規約で実装されている — バグは 221 行に局在)。参考: 反転規約で hexagon を回すと shadow 総数は $81\ne108$ になり、較正ゲートが落ちる。
また `task2` の ordered passport 実測 $\bigl([[18,1]],[[1,2],[2,8]],[[18,1]]\bigr)$ は本稿 **命題 ODD-P の $j=2,\ d=\gcd(1,9)=1$ の場合の予測と逐語一致**する(独立の裏づけ)。

### 11.6 ODD-H 本体への影響(設問 4)

**なし。** §2–§6 の議論は有限群 $G_n$ の部分群論のみを用い、$\Phi$・GT-shadow・$m$・$f$ はどこにも現れない。分類・個数・共役類・判別子・passport のいずれも $\Phi$ 非依存である。逆に §11 は §4 の分類((1.2) のパラメータ表示)を**使って** $\Phi$ の作用則を閉じた形で書いた — 依存の向きは一方向。

### 11.7 追加 FINDING

| # | 種別 | 内容 |
|---|---|---|
| **F10** | **実装バグ(確定)** | `search/k9-package.g` L221 の共役方向が規約 W-4 違反。観測値 `w5_bonus_fail=90` は完全にこれで説明される。**Sol の (1.13)(1.14) は正しく、実装が誤り。** 修理仕様は §11.4 |
| **F11** | **監査手続きの穴** | `GroupHomomorphismByImages ≠ fail` を「自己同型が構成できた」と読んだ。**非単射自己準同型が 54 件、無警報で通過**。`IsBijective` の assert 追加を必須とする |
| **F12** | 良い知らせ | GT($K^{(9)}$) 較正(hexagon 層)は独立実装と全項一致 — **cross-checked へ昇格可**。ordered passport 実測も命題 ODD-P と逐語一致 |
| **F13** | 設計 | 「GT-軌道単位で canonical detector を選ぶ」路線は**動機が消滅**(GT-軌道は全て 1 点)。類の選択は依然未解決。現存候補は Q6.1 の $\alpha=1$ と本稿 §6 の passport 絞り込み($n-1\to\varphi(n)$)のみ |
