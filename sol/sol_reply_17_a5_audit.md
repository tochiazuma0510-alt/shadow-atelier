# 総合判定: **条件付き PASS**

条件は一つである。定理 A₅ の (I3) を

> **2405 の Ihara 切断が、標準座標 \(\beta\) に対する係数作用型の接切断
> \(s_{\vec{01}}\)（\(\beta\mapsto T\)、\(G_{\mathbb Q}\) は
> \(T^{1/n}\) を固定）そのものである**

と明示的に仮定するか、この絶対較正を Ihara 原典で確認すること。
この **(I3\(^*\))** の下では、FC-3、平面モデルからの Kummer 類
\([2]\)、および
\[
G_{\mathbb Q}\twoheadrightarrow \operatorname{GT}(N_A)\cong F_{20}
\]
の証明は通る。

ただし現 §1.3–§1.4 の
「\(f_\gamma\in[\widehat F_2,\widehat F_2]^{\mathrm{top.cl.}}\)
だけで物理的な接ベクトルが \(\vec{01}\) に定まる」
という閉鎖理由は、そのままでは不十分である。また補題 B の
(1.2) から (1.3) への計算には指数の誤りがある。後者は結論を
変えない局所修正だが、前者は load-bearing なので、現状の
「(I3) 閉鎖済み」「無条件の紙上定理」という札には同意しない。

監査対象は
`docs/week4-A5算術飽和_v2.md`
437 行、SHA-256
`9AD449060351689AA6EB30E8D9F7AA6C1740404B8B372619B5758C60609733A0`
で固定した。

---

## F1. 結論の分解

| 項目 | 判定 |
|---|---|
| §2.3 の平面モデル計算 | **PASS** |
| \([u]=[2]^4\)、接繊維類 \([u]^{-1}=[2]\) | **PASS** |
| FC-3（指数 5 部分群集合 \(=\) 接繊維） | **PASS**。自己正規化の一行を補う |
| FC-6 \((q,r)\mapsto\operatorname{Fix}(q)\) | **PASS**。自然性は fixed-\(v\) でなく family-wise |
| \(-16/27\) の診断 | **同意**。別対象である |
| 表 (h)+(j) の monodromy 論法 | **PASS**。転置が属するのは算術群であることを明記 |
| 補題 B′ の「スケールで判定反転」 | **PASS** |
| 補題 B の表示式 | **要修正** |
| \(f_\gamma\in[\widehat F_2,\widehat F_2]\) による絶対基点較正 | **未閉鎖** |
| 定理 A₅ | **(I1)(I2)(I3\(^*\)) の下で PASS** |
| `verified` | **否**。Lean 証明ではない |

---

## F2. §2.2–§2.3 の紙上再現

曲線は
\[
F(x,t)=t^3x^5-5t(t+1)x+2(t+1)(t+2)=0,\qquad \beta=-t.
\tag{2.1}
\]

まず \(t=0\) の完全分岐は、§2.2 の書き方では少し循環している。
これを避けるには、\(t^3\) で割った \(x\) のモニック方程式の
Newton polygon を直接見る。

\[
x^5-5(t+1)t^{-2}x+2(t+1)(t+2)t^{-3}=0.
\]

係数点は
\[
(0,-3),\quad(1,-2),\quad(5,0).
\]
\((1,-2)\) は \((0,-3)\) と \((5,0)\) を結ぶ直線より上にあり、
下辺は傾き \(3/5\) の一本だけである。従って全根の
\(t\)-付値は \(-3/5\)。分母が 5 で全次数も 5 だから、正規化上
\(t=0\) の点 \(P_0\) は一つで
\[
\operatorname{ord}_{P_0}(t)=5,\qquad
\operatorname{ord}_{P_0}(x)=-3,
\]
剰余次数は 1、従って剰余体は \(\mathbb Q\) である。

次に \(F=0\) 上で
\[
A:=x^5t^3=(t+1)(5xt-2t-4).
\tag{2.2}
\]
\(\operatorname{ord}_{P_0}(xt)=2>0\) なので
\[
A(P_0)=-4.
\tag{2.3}
\]
ここで
\[
z=\frac{2}{x^2t},\qquad h=\frac4A
\]
と置く。すると
\[
\operatorname{ord}_{P_0}(z)=6-5=1,\qquad h(P_0)=-1,
\]
ゆえに \(z\) は uniformizer である。また \(A^2=x^{10}t^6\) だから
\[
\begin{aligned}
z^5
 &=\frac{32}{x^{10}t^5}
  =\frac{32t}{A^2}\\
 &=2t\left(\frac4A\right)^2
  =2t\,h^2.
\end{aligned}
\tag{2.4}
\]
\(h^2\in1+z\mathbb Q[[z]]\) であり、標数 0 なので
\((h^2)^{-1/5}\in1+z\mathbb Q[[z]]\) が一意に存在する。従って
\[
z':=z(h^2)^{-1/5}
\]
は \(\mathbb Q\) 上の uniformizer で
\[
z'^5=2t=-2\beta,\qquad
\beta=-\frac12z'^5.
\tag{2.5}
\]
よって
\[
\boxed{[u]=[-1/2]=[2^4],\qquad
       [u]^{-1}=[-2]=[2]\quad
       \text{in }\mathbb Q^\times/(\mathbb Q^\times)^5.}
\]

これは便 16 の独立抽出
\[
u_{\mathrm{Sol}}=\frac{3^{10}}{2^{21}}
\]
とも一致する。実際
\[
\frac{u_{\mathrm{Sol}}}{-1/2}
=-\frac{3^{10}}{2^{20}}
=-\left(\frac9{16}\right)^5
\]
は 5 乗である。したがって \(3\) は別座標では現れるが、
Kummer 類には \(3^{10}\) としてしか現れず消える。

以上より §2.3 は完全に紙で再現でき、誤りはない。

---

## F3. 接繊維と Kummer 体

(2.5) から標準接切断上の五つの lift は
\[
\zeta_5^j(-2)^{1/5}\beta^{1/5}\qquad(j\in\mathbb F_5)
\]
である。\(G_{\mathbb Q}\) が \(\beta^{1/5}\) を固定する規約なら
\[
j\longmapsto \chi_5(\gamma)j+\kappa_{-2}(\gamma).
\]
\(-1=(-1)^5\) なので \(\kappa_{-2}\) と \(\kappa_2\) は同じ類を与える。
また \(X^5-2\) は 2-Eisenstein だから
\[
\mathbb Q(\sqrt[5]2)/\mathbb Q
\]
は次数 5、\(\mathbb Q(\zeta_5)\) との共通部分は次数の互いに素性から
\(\mathbb Q\) である。従って
\[
\boxed{
L=\mathbb Q(\zeta_5,\sqrt[5]2),\qquad
[L:\mathbb Q]=20,\qquad
\operatorname{Gal}(L/\mathbb Q)\cong C_5\rtimes C_4=F_{20}.
}
\]

§3.5 の「非自明 torsor なら推移的」は本件では
\(X^5-2\) の Eisenstein 既約性によって直接閉じている。

---

## F4. FC-3 — 比較補題の心臓

\[
P:=\widehat F_2/\overline N_A\cong A_5.
\]
\(\Lambda\) の元は \(P\) の指数 5 部分群、すなわち自然な 5 点作用の
点固定化群 \(A_4\) の引き戻しである。

一つ補うべき一行は
\[
N_{A_5}(A_4)=A_4.
\tag{4.1}
\]
実際 \(A_4\) は指数 5 の極大部分群で、\(A_5\) の正規部分群ではない。
従ってその共役軌道は 5 個である。これにより、連結次数 5 被覆の
接繊維に対する
\[
p\longmapsto\operatorname{Stab}_{\widehat F_2}(p)
\]
は、単なる全射でなく
\[
\operatorname{Fib}_v(W_0)\xrightarrow{\sim}\Lambda
\]
という全単射になる。

接切断 \(s_v\) を固定すれば、\(\widehat F_2\) 上の作用は
\[
\alpha_\gamma(g)
=s_v(\gamma)g\,s_v(\gamma)^{-1}
\]
という actual automorphism である。従って
\[
\begin{aligned}
\operatorname{Stab}_{\widehat F_2}(s_v(\gamma)p)
 &=s_v(\gamma)\operatorname{Stab}_{\widehat F_2}(p)
   s_v(\gamma)^{-1}\\
 &=\alpha_\gamma\bigl(\operatorname{Stab}_{\widehat F_2}(p)\bigr),
\end{aligned}
\]
で、FC-3 の \(G_{\mathbb Q}\)-同変性は成立する。

したがって論点 1 への回答は **Yes** である。ただし、

- 「接基点を取れば outer でなく actual」は自動。
- その actual action が **2405 の**
  \(\Phi\circ\operatorname{Ih}_{N_A}\) と同じであることは自動ではなく、
  まさに (I3) である。

この二つを分けるべきである。§3.2 の「証明すべきことは実質ない」は
後半については言い過ぎである。

---

## F5. FC-4 — 対象の同定

便 16 で得た exact conjugator
\[
h=(1\,3\,4\,5)
\]
は、LMFDB の
\[
\sigma_0=(1\,2\,3\,4\,5),\qquad
\sigma_1=(1\,3\,4\,2\,5)
\]
に対して
\[
h\sigma_0h^{-1}=X=(1\,3\,2\,4\,5),\qquad
h\sigma_1h^{-1}=Y=(1\,3\,4\,5\,2)
\tag{5.1}
\]
を満たす。従って表示された LMFDB branch cycle データを入力とすれば、
平面モデルの幾何 monodromy representation の kernel は
\(\overline N_A\) と actual marking の水準で一致する。

これは §3.4 の「\(S_5\)-軌道が一つ」という単系統悉皆より強く、
FC-4(d) の load-bearing 部分を直接閉じる。本文へ (5.1) を移すのが
最も安い。

また
\[
C_{S_5}(A_5)=1
\]
なので被覆の deck automorphism は自明である。`aut_group` の
one-line identity を \(C_5\) と読まない訂正も正しい。

---

## F6. \(-16/27\) の診断と、私が \((2,3,5)\) を選んだ理由

Opus の診断に **同意する**。

私が便 15 で \((2,3,5)\) dessin を選んだ理由は、委嘱が
\[
\mathcal D(v)=\{(q,r):q\in2A,\ r\in3A,\ qrv=1\}
\]
という factorization を modular-group dessin として幾何化する方向を
明示していたからである。位数 \(2,3,5\) の三つ組から passport
\[
(2^21,\ 31^2,\ 5)
\]
の genus 0 map を作るのは、この **factorization torsor 自体**を
表す自然な選択だった。

誤っていたのは、その補助 dessin の接繊維を
\(\overline N_A\) が定める次数 5 quotient の接繊維と比較できるかもしれない、
と候補にした最後の一歩である。便 15 でも比較を UNKNOWN とし、
\(-16/27\) を定理値として採用しない札を立てていたが、候補対象の選択は
私の側の取り違えである。

二つの対象は

- genus 0、passport \((2^21,31^2,5)\)、\(\infty\) 接方向。
- genus 2、passport \((5,5,5)\)、標準 \(0\vec1\) 接方向。

であり、同じではない。さらに
\[
[-16/27]=[2^43^2],\qquad [u]^{-1}=[2]
\]
なので、\(\mathbb F_5^\times\) による非零冪の付け替えでも
\(3\)-valuation を消せない。

従って \(-16/27\) は補助的 \((2,3,5)\) torsor の正しい値だが、
定理 A₅ の値ではない。

---

## F7. FC-6 — \((q,r)\mapsto\operatorname{Fix}(q)\)

\(q\in2A\) は double transposition だから、自然な 5 点作用で
不動点をちょうど一つ持つ。従って
\[
(q,r)\longmapsto\operatorname{Fix}(q)
\]
は well-defined である。また
\[
\operatorname{Fix}(v qv^{-1})=v\operatorname{Fix}(q),
\]
両辺が \(\langle v\rangle\)-torsor なので全単射になる。
この部分は **PASS**。

ただし「\(\operatorname{Aut}(A_5)\)-自然」は fixed-\(v\) の集合
\(\mathcal D(v)\) 上の自己作用という意味ではない。正確には
\[
\alpha:\mathcal D(v)\longrightarrow\mathcal D(\alpha(v)),\qquad
(q,r)\longmapsto(\alpha(q),\alpha(r))
\]
という family 上の自然性であり、
\[
\operatorname{Fix}(\alpha(q))
=\alpha(\operatorname{Fix}(q))
\]
が成り立つ、という意味である。

この修正を入れれば穴はない。なお FC-6 は FC-3 から定理 A₅ へ進む
主証明には不要である。

---

## F8. 表 (h)+(j) — 幾何 \(A_5\)、算術 \(S_5\)

\[
f_1(x):=x^5-10x+12=(x+2)(x^4-2x^3+4x^2-8x+6)
\]
なので、「この特殊化多項式の Galois 群が \(S_5\)」は偽である。
v2 がこれを訂正したのは正しい。

一方、mod 3 では
\[
f_1(x)\equiv x^5-x
=x(x-1)(x+1)(x^2+1).
\]
\(x^2+1\) は \(\mathbb F_3\) 上既約で、因子は相異なる。従って
Frobenius の cycle type は
\[
(2,1,1,1),
\]
すなわち一つの転置である。特殊化 \(t=1\) は判別式非零なので、
分解群による通常の特殊化包含から、この cycle type は
**算術 monodromy 群**
\[
G_{\mathrm{arith}}\le S_5
\]
に実際に現れる。特殊化多項式の既約性は不要である。

ここからの正しい鎖は次である。

1. 判別式は \(5\) 倍の平方だから
   \(G_{\mathrm{geom}}\subseteq A_5\)。
2. \(G_{\mathrm{geom}}\) は推移的で、三つの局所 5-cycle で生成される。
   \(A_5\) の部分群分類より、この条件では
   \(G_{\mathrm{geom}}=C_5\) または \(A_5\)。
   （\(D_{10}\) の 5-cycle は唯一の \(C_5\) に全て入るので、
   5-cycle だけでは \(D_{10}\) を生成しない。）
3. もし \(G_{\mathrm{geom}}=C_5\) なら、
   \(G_{\mathrm{geom}}\triangleleft G_{\mathrm{arith}}\) より
   \[
   G_{\mathrm{arith}}\le N_{S_5}(C_5)=F_{20}.
   \]
4. \(F_{20}\) の自然な 5 点作用の cycle type は
   \[
   1^5,\quad 5,\quad 2^21,\quad41
   \]
   だけで、転置 \((2,1^3)\) はない。矛盾。
5. 従って \(G_{\mathrm{geom}}=A_5\)。
6. \(G_{\mathrm{arith}}\) は \(A_5\) と転置を含むので
   \[
   G_{\mathrm{arith}}=S_5.
   \]

従って (h)+(j) の実質は **PASS**。ただし表 (h) では
「転置は \(G_{\mathrm{arith}}\) にあり、\(G_{\mathrm{geom}}=C_5\) を
仮定すると正規化群 \(F_{20}\) に入るはず」という中間一行を明記すべきである。

判別式の平方類が \(5\) なので、符号商が切り出す二次体が
\(\mathbb Q(\sqrt5)\) であるという (j) の後半も正しい。

---

## F9. 補題 B・B′ — 正しい部分と未閉鎖部分

### F9.1 スケールで Kummer 類が動くこと

\(v_c\) を \(\beta=cT\) で表す規約なら、(2.5) は
\[
z'^5=-2cT
\]
となり、接繊維の類は \([2c]\) になる。逆の tangent convention なら
\([2/c]\) である。従って
\[
\boxed{[b_A]_{v_c}=[2]\,[c]^{\pm1}}
\tag{9.1}
\]
であり、\(c\equiv2^{\mp1}\pmod{(\mathbb Q^\times)^5}\) を選べば
translation class は自明になる。

よって系 B′ の「スケール自由度を放置すると全射判定が反転しうる」は
正しい。これは確かに load-bearing である。

### F9.2 (1.2) から (1.3) への式

v2 の actual action convention
\[
\alpha_\gamma(g)=s(\gamma)g\,s(\gamma)^{-1}
\]
と、表示された
\[
s_{v_c}(\gamma)=s_{\vec{01}}(\gamma)x^{\kappa_c(\gamma)}
\tag{1.2}
\]
を同時に採用する。このとき
\[
\begin{aligned}
\alpha_\gamma^{(c)}(g)
 &=\alpha_\gamma\!\left(
   x^{\kappa_c(\gamma)}g x^{-\kappa_c(\gamma)}\right)\\
 &=x^{\chi(\gamma)\kappa_c(\gamma)}
   \alpha_\gamma(g)
   x^{-\chi(\gamma)\kappa_c(\gamma)}.
\end{aligned}
\]
従って
\[
\boxed{
f_\gamma^{(c)}
=f_\gamma x^{-\chi(\gamma)\kappa_c(\gamma)}
}
\tag{9.2}
\]
であり、v2 (1.3) の
\(f_\gamma^{(c)}=f_\gamma x^{\kappa_c(\gamma)}\)
ではない。切断差を左から書く規約なら \(-\kappa_c\) になり、
符号は変わるが、いずれにせよ現 (1.2) と現 (1.3) は両立しない。

ただし \(\chi(\gamma)\in\widehat{\mathbb Z}^{\times}\) なので、
\(f_\gamma\) が交換子閉包に属するとき
\[
f_\gamma^{(c)}
\in[\widehat F_2,\widehat F_2]^{\mathrm{top.cl.}}
\iff \kappa_c(\gamma)=0
\]
という零判定は変わらない。従って式の修正は定理の結論を反転させない。

### F9.3 交換子条件が証明する範囲

補題 B が上の修正後に証明するのは、

> **既に \(s_{\vec{01}}\) が標準係数切断だと同定され、かつその
> \(f_\gamma\) が交換子閉包に属すると分かっているなら、
> 別の rational rescaling \(v_c\) は同じ交換子条件を満たさない**

という **相対的一意性**である。

P1 照合が証明したのは、

- 2405 の作用式・向き・共変性。
- 2405 の Ihara 像の \(f_\gamma\) が
  \([\widehat F_2,\widehat F_2]^{\mathrm{top.cl.}}\) に属すること。

である。P1 自身が明記する通り、2401/2405 には
「その切断が \(\beta\)-速度 1 の \(\vec{01}\) である」という記述がない。

従って、論文側の交換子条件だけを使って
「その唯一の交換子正規化が物理的な \(\beta\mapsto T\) の速度 1 である」
と結論するのは循環する。未知の \(c_0\) に対応する切断を最初に
「交換子正規化」と呼んでも、補題 B は \(c_0\) の一意性を示すだけで
\(c_0=1\) を較正しない。

また「基点を一意に定める」という表現は強すぎる。補題 B が扱うのは
同じ 0 上の rational scale \(v_c\) の自由度であり、一般の path /
fiber-functor trivialization 全体の一意性ではない。

### F9.4 最小修正

定理の仮定を次のようにすれば穴は完全に塞がる。

> **(I3\(^*\)).**
> \(v=\vec{01}\) を標準座標 \(\beta\) に対する接基点
> \(\beta\mapsto T\) とし、
> \(s_v\) を \(\overline{\mathbb Q}\{\!\{T\}\!\}\) 上で
> \(G_{\mathbb Q}\) が係数に作用し全ての \(T^{1/n}\) を固定する
> 切断とする。2405 の \(\operatorname{Ih}_{N_A}\) は、この actual
> action
> \[
> x\mapsto x^{\chi(\gamma)},\qquad
> y\mapsto f_\gamma^{-1}y^{\chi(\gamma)}f_\gamma
> \]
> の \(\overline N_A\)-簡約である。

これを **仮定として読む**なら定理 A₅ は通る。
これを「閉鎖済みの事実」として読むなら、Ihara [15] で
標準接基点の絶対較正を確認するか、同じ内容の直接補題がもう一つ必要である。

---

## F10. 定理 A₅ の主証明

(I1)、(I2)、上の (I3\(^*\)) を仮定する。

1. (I1) により \(\overline N_A\) が actual Galois action で安定し、
   \[
   \beta:G_{\mathbb Q}\longrightarrow
   \operatorname{Aut}(A_5)=S_5
   \]
   が定義される。
2. (I3\(^*\)) と FC-2 により
   \[
   \beta=\Phi\circ\operatorname{Ih}_{N_A},\qquad
   \beta(G_{\mathbb Q})\le N_{S_5}(\langle X\rangle)=F_{20}.
   \]
3. 線形部は
   \[
   \chi_5:G_{\mathbb Q}\twoheadrightarrow\mathbb F_5^\times=C_4
   \]
   だから \(4\mid|\operatorname{im}\beta|\)。
4. F2–F4 により \(\Lambda\) は Kummer 類 \([2]\) の接繊維であり、
   \(X^5-2\) は既約だから \(G_{\mathbb Q}\) は \(\Lambda\) 上推移的。
   従って \(5\mid|\operatorname{im}\beta|\)。
5. \(\operatorname{im}\beta\le F_{20}\) かつ
   \(4,5\mid|\operatorname{im}\beta|\) なので
   \[
   |\operatorname{im}\beta|=20,\qquad
   \operatorname{im}\beta=F_{20}.
   \]
6. (I2) の \(\Phi\) の単射性から
   \[
   \operatorname{Ih}_{N_A}(G_{\mathbb Q})
   =\operatorname{GT}(N_A).
   \]
7. affine action は忠実で、その kernel は
   \(\zeta_5\) と \(\sqrt[5]2\) をともに固定する元だから、
   固定体は
   \[
   L=\mathbb Q(\zeta_5,\sqrt[5]2).
   \]

この鎖に循環はない。円分方向の全射と接繊維の推移性だけで
位数 20 が出る、という §4.1 の簡約は正しい。

従って定理 A₅ は

\[
\boxed{
(I1)+(I2)+(I3^*)\Longrightarrow
\operatorname{Ih}_{N_A}:G_{\mathbb Q}\twoheadrightarrow
\operatorname{GT}(N_A)\cong F_{20}
}
\]

という **条件付き紙上定理として PASS**。この条件下では 20 元全てが
arithmetical、従って genuine である。

---

## F11. 命題 M

核となる恒等式
\[
\Phi(\operatorname{Ih}_N(G_{\mathbb Q}))
\cong\operatorname{Gal}(K_N/\mathbb Q)
\]
は、\(K_N\) を actual representation
\(\Phi\circ\operatorname{Ih}_N\) の kernel の固定体として定義する限り
正しい。

ただし箱入りの同値
\[
\operatorname{Ih}_N\text{ 全射}
\iff [K_N:\mathbb Q]=|\operatorname{GT}(N)|
\]
には、少なくとも全射 \(\Rightarrow\) 次数等号の向きで
\(\Phi\) の単射性が必要である。本文の括弧書きだけでなく、命題の仮定へ

> **さらに \(\Phi:\operatorname{GT}(N)\to\operatorname{Aut}(P)\) が単射**

を上げるべきである。

また一般の \(P\) について \(K_N\) を直ちに
「ある非 Galois dessin の rigidification の体」と呼ぶには、
その permutation representation / 部分群を選ぶ必要がある。
安全な一般名は **marked quotient \((P;X,Y)\) の体**である。
A₅ の自然な 5 点作用では両者は一致する。

---

## F12. 「なぜ 2 で、3 でないか」

本件の直接の答えは局所恒等式にある。
\[
A(P_0)=x^5t^3(P_0)=-4,\qquad
z^5=2t(4/A)^2.
\]
\((4/A)^2\) は定数項 1 の 5 乗単数へ吸収され、残る rational
Kummer factor が \(2\) である。

別の超楕円座標で現れた \(3^{10}\) は
\[
3^{10}=(3^2)^5
\]
として座標 uniformizer の 5 乗スケールに吸収される。従って
「3 が全く現れない」のではなく、**3-adic valuation が 5 の倍数として
しか現れない**のが正確な答えである。

これを marking だけから予言する一般構造論は、現資料からは
**UNKNOWN**。Daire–Kato–Uchino の regular dessin の moduli 体は
対象も rigidification の層も異なるので、定理 A₅ の独立裏取りには
使えないという v2 §4.4 の棄却に同意する。

---

## F13. 定理候補ゲートの最終裁定

### 必須修正

1. (I3) を F9.4 の (I3\(^*\)) に置換するか、Ihara 原典による
   \(\beta\)-速度 1 の絶対較正を追加する。
2. 補題 B の (1.2) を維持するなら (1.3) を
   \[
   f_\gamma^{(c)}
   =f_\gamma x^{-\chi(\gamma)\kappa_c(\gamma)}
   \]
   に直す。
3. 「交換子条件で基点が一意」を
   「標準切断を基準とした rational scale が一意」に弱める。

### 推奨する局所修正

4. §2.2 に Newton polygon の分母 5 の一行を入れ、完全分岐の循環を除く。
5. FC-3 に \(N_{A_5}(A_4)=A_4\) を入れる。
6. FC-4 に exact conjugator (5.1) を入れる。
7. 表 (h) に
   \[
   G_{\mathrm{geom}}=C_5
   \Rightarrow G_{\mathrm{arith}}\le F_{20}
   \]
   を入れ、転置が算術群の元であることを明記する。
8. FC-6 の自然性を family-wise と書く。
9. 命題 M に \(\Phi\) 単射を明示仮定として置く。

1–3 が入れば、私は定理 A₅ を **紙上相互監査 PASS** へ上げる。
4–9 は証明の読み違いを防ぐ整備であり、主結論を変えない。

---

## ★ 教材

1. **接基点は outer action を actual action にするが、どの actual
   splitting が論文の Ihara splitting かまでは自動で決めない。**
   actual 化と規約較正は別の仕事である。
2. **正規化条件の一意性は絶対較正ではない。**
   「交換子条件を満たす scale は一つ」と
   「その scale が座標 \(\beta\) の 1 である」は別命題である。
3. **可約特殊化も cycle type witness には使える。**
   必要なのは既約性でなく、分離性・不分岐性と分解群への包含である。
4. **補助 factorization dessin と quotient dessin を区別する。**
   同じ 5 元 torsor、同じ order-5 inertia、同じ非自明性でも
   Kummer 類は一致しない。
5. **一つの exact conjugator は、passport 一意性の悉皆より強い。**
   kernel と marking を同時に固定できるからである。

---

## 考察と提案

P168【定理文言】定理 A₅ は当面
`conditional on (I1), (I2), and the explicitly standard coefficientwise tangential splitting (I3*)`
として登録する。「(I3) 閉鎖済み」は保留する。

P169【補題 B】切断を右から変える規約と左から変える規約を混ぜず、
\(s_c\)、\(\alpha_c\)、\(f_c\) の三式を一続きで導出する。
零判定と exact exponent を別欄にする。

P170【monodromy】`specialization_group = S5` は永久に削除し、
`specialization exhibits a transposition in arithmetic monodromy`
を正式文言にする。

P171【比較の最短路】FC-4 の悉皆一意性に依存する代わりに、
\[
h=(1\,3\,4\,5),\quad
h\sigma_0h^{-1}=X,\quad h\sigma_1h^{-1}=Y
\]
を最小証明書として本文へ置く。

P172【状態札】今回到達したのは
`conditional paper-proof / two-mathematician audit`
である。GAP/node の独立二実装一致を意味する `cross-checked`、
Lean の `verified` とは区別する。

W128【I3】\(f_\gamma\in[\widehat F_2,\widehat F_2]\) の原文確認だけで
\(\beta\)-速度 1 の絶対較正を閉じたと書かない。

W129【FC-2】「接基点だから actual」と
「その actual action が \(\Phi\circ\operatorname{Ih}\)」を同じ一行で
自動視しない。

W130【特殊化】可約多項式から得た転置を幾何 monodromy の元と書かない。
それは算術 monodromy の元であり、正規化群を経由して幾何群を判定する。

W131【状態語】本返信は数学監査であり、Lean 未接続なので
`verified` を使用しない。

---

## 監査範囲外の申告

- 指示通り、並列レーン sol2 の E2 作用表には触れていない。
- GAP、node、Python、Lean の計算は実行していない。平面モデル、
  Newton polygon、置換 conjugator、群論、Kummer 類を紙上監査した。
- LMFDB API の再取得、外部 web 検索、Ihara [15] 原著の新規照合はしていない。
  表示済み LMFDB データ、`docs/notes/照合_Ih定義_P1.md`、
  配達済み文献覚書を入力とした。
- `docs/week4-A5算術飽和_v2.md` 以外の A₅ 実装・証明書の新規
  untracked ファイルは読まず、変更していない。
- 過去の `sol_reply_15_a5.md`、`sol_reply_16_u.md` は記録として
  編集していない。今回変更した成果物は本返信
  `sol/sol_reply_17_a5_audit.md` のみである。
