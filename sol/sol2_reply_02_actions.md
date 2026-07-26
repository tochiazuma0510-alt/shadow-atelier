# sol2 便 02 — \(A=\gamma _2(F_2)/\gamma _6(F_2)\) の full-\(A\) 作用表

## 自己検査結果（冒頭）

**全項 PASS（紙上 collection + 整数係数の次数 5 Magnus 展開による独立照合）。**

| 項目 | 結果 |
|---|---|
| \(\mathcal N_C=1+\sigma_C+\sigma_C^2=0\) | PASS |
| \(\operatorname{im}\Lambda=\langle(t_5+t_6,0)\rangle\) | PASS |
| canonical section で \(c_s(w,p)=0\) | PASS |
| canonical section で \(c_s(p,w)=-t_5\) | PASS |
| \(\theta^2=1\)（全 12 基底） | PASS |
| \(\sigma_m(E_m)=E_m\)、\(\sigma_m^3=\operatorname{Inn}(E_m)\) | PASS（多項式恒等式。数値では \(m=-3,\ldots,10\)、全 12 基底も直接照合） |
| E19 の \(c=5,\ m=1,2,5\) の \(b\)-ベクトル | PASS（本稿の \(-\bar E_m\) と 10 座標すべて一致） |

以下は定義と導出のみであり、掃引の可解性に関する結論は含めない。

---

## 0. 規約と導出法

交換子と共役の規約を
\[
[u,v]=u^{-1}v^{-1}uv,\qquad u^v=v^{-1}uv=u[u,v]
\]
とする。\(z=(xy)^{-1}\) とし、
\[
\theta:(x,y)\longmapsto(y,x),\qquad
\tau:(x,y,z)\longmapsto(y,z,x),
\]
\[
\sigma_m(g)=y^{-m}\tau(g)y^m=(\tau g)^{y^m},\qquad
E_m=x^mz^my^m
\tag{0.1}
\]
を用いた。

Hall 基底と順序は
\[
\begin{aligned}
&w=[x,y];\quad p=[w,x],\ q=[w,y];\\
&r_1=[p,x],\ r_2=[p,y],\ r_3=[q,y];\\
&t_1=[r_1,x],\ t_2=[r_1,y],\ t_3=[r_2,y],\ t_4=[r_3,y],
\quad t_5=[w,p],\ t_6=[w,q].
\end{aligned}
\tag{0.2}
\]

以下で
\[
[a_1,\ldots,a_{12}]
:=w^{a_1}p^{a_2}q^{a_3}r_1^{a_4}r_2^{a_5}r_3^{a_6}
t_1^{a_7}t_2^{a_8}t_3^{a_9}t_4^{a_{10}}t_5^{a_{11}}t_6^{a_{12}}
\tag{0.3}
\]
と書く（右辺で隣接する因子は昇順の群積である）。

独立導出には Magnus 写像
\[
x\mapsto1+X,\qquad y\mapsto1+Y
\]
を \(\mathbb Z\langle X,Y\rangle/(\text{次数}\ge6)\) へ入れ、逆元を有限幾何級数で展開する方法を用いた。自由群では次数 \(6\) の dimension subgroup が \(\gamma _6\) なので、この打切りは \(F_2/\gamma _6\) 上で厳密である。各重み \(2,3,4,5\) の斉次成分を (0.2) の Lie leading term で解き、その重みの Hall 積を左から除去して次の重みへ進んだ。

---

## 1. Hall 積表

### 1.1 \(A\) 内の全交換子対

\(A=\gamma _2/\gamma _6\) は class \(2\) であり、12 基底の全対について非自明なのは
\[
[w,p]=t_5,\qquad [w,q]=t_6
\tag{1.1}
\]
だけである。すなわち、対角はすべて \(1\)、上の二対以外の \(i<j\) はすべて \(1\)、下三角は
\[
[p,w]=t_5^{-1},\qquad[q,w]=t_6^{-1}
\tag{1.2}
\]
および残りすべて \(1\) である。これで 12 基底の全 \(12^2\) 対を尽くす。

従って collection の非自明な交換則は
\[
p^a w^b=w^b p^a t_5^{-ab},\qquad
q^a w^b=w^b q^a t_6^{-ab}
\tag{1.3}
\]
だけである。

### 1.2 全座標の積・逆元・冪

\(a=(a_1,\ldots,a_{12})\)、\(b=(b_1,\ldots,b_{12})\) に対し、
\[
\boxed{
[a]\,[b]=
[a_1+b_1,\ldots,a_{10}+b_{10},
a_{11}+b_{11}-a_2b_1,\,
a_{12}+b_{12}-a_3b_1].
}
\tag{1.4}
\]
従って
\[
[a]^{-1}=
[-a_1,\ldots,-a_{10},-a_{11}-a_1a_2,-a_{12}-a_1a_3],
\tag{1.5}
\]
\[
[a]^n=
[na_1,\ldots,na_{10},
na_{11}-\tbinom n2a_1a_2,\,
na_{12}-\tbinom n2a_1a_3].
\tag{1.6}
\]
ここで \(\binom n2=n(n-1)/2\) とし、負の \(n\) にも同じ式を用いる。

### 1.3 \(x,y\) による collection 表

full-\(A\) 作用の導出に使う外部共役の完全表は次である。空欄はなく、最後の行は \(i=1,\ldots,6\) の全てを表す。

| \(g\) | \([g,x]\) | \([g,y]\) |
|---|---|---|
| \(w\) | \(p\) | \(q\) |
| \(p\) | \(r_1\) | \(r_2\) |
| \(q\) | \(r_2t_5t_6\) | \(r_3\) |
| \(r_1\) | \(t_1\) | \(t_2\) |
| \(r_2\) | \(t_2t_5\) | \(t_3\) |
| \(r_3\) | \(t_3t_6\) | \(t_4\) |
| \(t_i\) | \(1\) | \(1\) |

特に class \(4\) へ射影すると \([q,x]=r_2\) となり、既存の Jacobi 表と一致する。重み \(5\) の \(t_5,t_6\) 補正が full-\(A\) で新たに残る部分である。

### 1.4 canonical section cocycle

\(\bar A=A/C\)、\(C=\langle t_5,t_6\rangle\) とし、昇順 section
\[
s(a)=w^{a_w}p^{a_p}q^{a_q}r_1^{a_{r_1}}r_2^{a_{r_2}}r_3^{a_{r_3}}
t_1^{a_{t_1}}t_2^{a_{t_2}}t_3^{a_{t_3}}t_4^{a_{t_4}}
\tag{1.7}
\]
を取る。(1.4) から
\[
\boxed{c_s(a,b)=(-a_pb_w)\,t_5+(-a_qb_w)\,t_6.}
\tag{1.8}
\]

---

## 2. \(\theta\) と \(\sigma_m\) の full-\(A\) 作用表

\(c_2=\binom m2,\ c_3=\binom m3\) と略記する。各右辺は (0.2) の昇順に collection 済みである。

### 2.1 \(\theta\)

\[
\begin{array}{c|l}
g&\theta(g)\\ \hline
w&w^{-1}\\
p&q^{-1}t_6^{-1}\\
q&p^{-1}t_5^{-1}\\
r_1&r_3^{-1}\\
r_2&r_2^{-1}t_5^{-1}t_6^{-1}\\
r_3&r_1^{-1}\\
t_1&t_4^{-1}\\
t_2&t_3^{-1}t_6^{-1}\\
t_3&t_2^{-1}t_5^{-1}\\
t_4&t_1^{-1}\\
t_5&t_6\\
t_6&t_5
\end{array}
\tag{2.1}
\]

導出は \(\theta(x)=y,\theta(y)=x\) を (0.2) へ代入し、§1.3 で collection するだけである。例えば
\[
\theta(r_2)=[\theta(p),x]=[q^{-1}t_6^{-1},x]
=r_2^{-1}t_5^{-1}t_6^{-1}.
\]

### 2.2 \(\sigma_m\)

\[
\begin{array}{c|l}
g&\sigma_m(g)\\ \hline
w&
w\,p^{-1}q^m r_1r_2^{-m}r_3^{c_2}
t_1^{-1}t_2^m t_3^{-c_2}t_4^{c_3}\\
p&
q\,r_2^{-1}r_3^m t_2t_3^{-m}t_4^{c_2}\\
q&
p^{-1}q^{-1}r_1^2r_2^{\,2-m}r_3^{\,1-m}
t_1^{-3}t_2^{\,2m-3}t_3^{-2+2m-c_2}t_4^{-1+m-c_2}t_5^{-1}\\
r_1&
r_3t_3^{-1}t_4^m\\
r_2&
r_2^{-1}r_3^{-1}t_2^2t_3^{\,2-m}t_4^{\,1-m}t_5\\
r_3&
r_1r_2^2r_3t_1^{-3}t_2^{\,m-6}t_3^{\,2m-5}t_4^{\,m-2}t_5^{-3}t_6^{-1}\\
t_1&t_4\\
t_2&t_3^{-1}t_4^{-1}t_6^{-1}\\
t_3&t_2t_3^2t_4t_5t_6\\
t_4&t_1^{-1}t_2^{-3}t_3^{-3}t_4^{-1}t_5^{-2}t_6^{-1}\\
t_5&t_6\\
t_6&t_5^{-1}t_6^{-1}
\end{array}
\tag{2.2}
\]

\(\tau\) の full-\(A\) 表は (2.2) の \(m=0\) である。導出は二段で行った。

1. \(\tau(x)=y,\tau(y)=z=(xy)^{-1}\) を各 Hall 語へ代入し、§1 の積則で昇順へ collection する。
2. \(\sigma_m(g)=\tau(g)^{y^m}\) と
   \[
   G_{m+1}=G_m^y=G_m[G_m,y]
   \]
   を用い、§1.3 の表を反復する。重み \(5\) は中心なので三回差分で止まり、
   \(\binom m2,\binom m3\) が現れる。Pascal 恒等式により (2.2) を整数 \(m\) について帰納できる。

(2.2) を重み \(4\) までへ射影すると
\[
\begin{aligned}
\sigma_m(w)&=w-p+mq+r_1-mr_2+\binom m2r_3,\\
\sigma_m(p)&=q-r_2+mr_3,\\
\sigma_m(q)&=-p-q+2r_1+(2-m)r_2+(1-m)r_3,
\end{aligned}
\]
となり、既存の class-4 表と一致する。

---

## 3. \(E_m\) の明示 Hall 座標

一般化二項係数
\[
\binom mk=\frac{m(m-1)\cdots(m-k+1)}{k!}
\]
を整数 \(m\) 全体で用いる。次の二つの整数値多項式を置く:
\[
\begin{aligned}
e_5(m)
&=\binom m1+7\binom m2+17\binom m3+17\binom m4+6\binom m5\\
&=\frac{m(m+1)(m+2)(6m^2+7m+7)}{120},\\
e_6(m)
&=-\binom m2-4\binom m3-6\binom m4-3\binom m5\\
&=-\frac{m(m-1)(m+1)(3m^2+8)}{120}.
\end{aligned}
\tag{3.1}
\]

すると \(E_m=x^m((xy)^{-1})^my^m\) の昇順 Hall 正規形は
\[
\boxed{\begin{aligned}
E_m={}&
w^{-\binom{m+1}{2}}
p^{ \binom{m+2}{3}}
q^{-\binom{m+1}{3}}
r_1^{-\binom{m+3}{4}}
r_2^{ \binom{m+2}{4}}
r_3^{-\binom{m+1}{4}}\\
&\cdot
t_1^{ \binom{m+4}{5}}
t_2^{-\binom{m+3}{5}}
t_3^{ \binom{m+2}{5}}
t_4^{-\binom{m+1}{5}}
t_5^{e_5(m)}t_6^{e_6(m)}.
\end{aligned}}
\tag{3.2}
\]

導出では (0.1) の三因子を次数 \(5\) Magnus 環で冪乗・乗算し、重み順に Hall 成分を除去した。各座標は次数 \(\le5\) の整数値多項式となる。\(t_5,t_6\) 座標の Newton 差分係数
\((f(0),\Delta f(0),\ldots,\Delta^5f(0))\) はそれぞれ
\[
(0,1,7,17,17,6),\qquad(0,0,-1,-4,-6,-3)
\]
なので (3.1) を得る。

較正点は次の通り（セミコロンの後が \(t_5,t_6\)）:
\[
\begin{array}{c|c}
m&E_m\text{ の 12 座標}\\ \hline
1&(-1,1,0,-1,0,0,1,0,0,0;\ 1,0)\\
2&(-3,4,-1,-5,1,0,6,-1,0,0;\ 9,-1)\\
5&(-15,35,-20,-70,35,-15,126,-56,21,-6;\ 336,-83).
\end{array}
\tag{3.3}
\]
`certificates/e19/gap_system_c5_m1.txt`, `m2.txt`, `m5.txt` の \(b\) の後半 10 座標は、(3.3) の最初の 10 座標の負号とすべて一致した。

---

## 4. Section 欠損 \(d_\theta,d_\sigma,\varepsilon_m\)

### 4.1 一般式

\[
a=(a_w,a_p,a_q,a_{r_1},a_{r_2},a_{r_3},
a_{t_1},a_{t_2},a_{t_3},a_{t_4})\in\bar A
\]
とし、section は (1.7) とする。作用 \(\gamma\) の \(i\) 番目の基底像を
\[
\gamma(b_i)=s(v_i^\gamma)\,h_i^\gamma,\qquad
v_i^\gamma\in\bar A,\quad h_i^\gamma\in C
\]
と書く。(1.4)–(1.6) から
\[
\boxed{\begin{aligned}
d_\gamma(a)
&:=s(\bar\gamma a)^{-1}\gamma(s(a))\\
&=\sum_i a_i h_i^\gamma
-\sum_i\binom{a_i}{2}v_{i,w}^\gamma
  (v_{i,p}^\gamma t_5+v_{i,q}^\gamma t_6)\\
&\quad-\sum_{i<j}a_ia_jv_{j,w}^\gamma
  (v_{i,p}^\gamma t_5+v_{i,q}^\gamma t_6).
\end{aligned}}
\tag{4.1}
\]
従って作用表の基底像だけから一般の section 欠損が再構成できる。

### 4.2 展開済みの \(d_\theta,d_{\sigma_m}\)

(2.1) を (4.1) へ代入すると
\[
\boxed{
d_\theta(a)=
(-a_q-a_{r_2}-a_{t_3})t_5
+(-a_p-a_{r_2}-a_{t_2})t_6.
}
\tag{4.2}
\]

(2.2) では \(w\)-成分を持つ基底像は \(\sigma_m(w)\) だけであり、その
\((w,p,q)\)-成分は \((1,-1,m)\) である。従って唯一の冪補正は
\(\binom{a_w}{2}(t_5-mt_6)\) であり、
\[
\boxed{\begin{aligned}
d_{\sigma_m}(a)
={}&\left(
\binom{a_w}{2}-a_q+a_{r_2}-3a_{r_3}+a_{t_3}-2a_{t_4}
\right)t_5\\
&+\left(
-m\binom{a_w}{2}-a_{r_3}-a_{t_2}+a_{t_3}-a_{t_4}
\right)t_6.
\end{aligned}}
\tag{4.3}
\]

基底上の線型部分は、(4.2)–(4.3) で対応する座標を \(1\)、残りを \(0\) とすれば得られる。非線型部分は \(w^{a_w}\) の像の自己 collection だけである。

### 4.3 \(\varepsilon_m\)

\(e=\bar E_m\) とし、
\[
\varepsilon_m:=s(e)^{-1}E_m\in C
\]
と定める。(3.2) から直ちに
\[
\boxed{\varepsilon_m=e_5(m)t_5+e_6(m)t_6.}
\tag{4.4}
\]

有限 verbal 冪商 \(A_j=A/\mho_j(A)\) では、入力の \(a_i\) を
\(0\le a_i<2^j\) に取り、(1.8)、(4.2)–(4.4) の中心係数を
\(2^{j-1}\) で落とせばよい。各基底元の \(2^j\) 乗そのものが
\(\mho_j(A)\) で消えるため、商座標を代表元区間へ戻す際の追加中心項はない。

### 4.4 sol2 便 01 の \(q\) 式への接続

\(T=\bar\theta,\ S=\bar\sigma_m\) とする。加法的な \(C\) 座標では
\[
q_\theta(a)=d_\theta(a)+c_s(Ta,a).
\tag{4.5}
\]
また
\[
d_{\sigma^2}(a)=\sigma_Cd_\sigma(a)+d_\sigma(Sa)
\tag{4.6}
\]
であり、
\[
\boxed{\begin{aligned}
q_N(a)={}&\varepsilon_m+d_{\sigma^2}(a)+d_\sigma(a)\\
&+c_s(e,S^2a)+c_s(e+S^2a,Sa)
+c_s(e+S^2a+Sa,a).
\end{aligned}}
\tag{4.7}
\]
(1.8)、(2.1)–(2.2)、(3.1)、(4.2)–(4.4) により、(4.5)–(4.7) の全項が明示された。

---

## 5. 指定自己検査の展開

(2.2) の最後の二行から、基底 \((t_5,t_6)\) において
\[
\sigma_C=
\begin{pmatrix}0&-1\\1&-1\end{pmatrix},\qquad
\theta_C=
\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]
従って
\[
\sigma_C^2=
\begin{pmatrix}-1&1\\-1&0\end{pmatrix},\qquad
I+\sigma_C+\sigma_C^2=0.
\]
また
\[
(1+\theta_C)(at_5+bt_6)=(a+b)(t_5+t_6),
\]
ゆえに
\[
\operatorname{im}\Lambda
=\{((1+\theta_C)z,0):z\in C\}
=\langle(t_5+t_6,0)\rangle.
\]
最後に (1.8) へ \((a,b)=(w,p)\)、\((p,w)\) を代入して
\[
c_s(w,p)=0,\qquad c_s(p,w)=-t_5.
\]

## 監査範囲外申告

読取禁止指定の `docs/week4-E2作用表_v1.md`、`sol/sol_task_16*`、
`sol/sol_reply_16*`、`docs/対話帳.md` は一切読んでいない。相方の導出結果との
答え合わせも行っていない。有限 PC presentation の構築、384 系の走査、
route N/G の二系統照合、Lean 証明書化は本便の範囲外である。
