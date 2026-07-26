# 総合判定: **E23 PASS** ／ 転進先: **weight 6・class 6**

定理 E23 の中心結論
\[
\omega\equiv0\quad\text{on }\mathcal L
\]
は正しい。(b) の二つの交換子補正の符号も正しく相殺する。
しかも、交換子座標を一切使わない中央拡大の恒等式で独立に証明できる。
従って【GAP-E23a】は **紙上相互監査 PASS** として閉じてよい。

転進先も紙で一意に決まる。自由 Lie 環の第二導来
\(D=L''\) について
\[
D_5\cong V,\qquad
D_6\cong\mathbf1\oplus\mathrm{sgn}\oplus V
\]
（\(V\) は \(S_3\) の標準表現）である。従って

- \([A,A]\) が \(\sigma\)-固定成分を初めて獲得するのは
  **weight 6**。
- 対象は
  \[
  P^{(6)}=F_2/\gamma_7,\qquad
  A^{(6)}=\gamma_2/\gamma_7.
  \]
- 同じ weight 6 で \(C=[A,A]\) の
  \(\langle\theta\rangle\)-induced 性も初めて破れる。
- \(A^{(6)}\) はなお class \(2\) なので、E22′ の現行枠組みを
  変更せずそのまま撃てる。

したがって「闇雲に次の class」ではなく、
**weight-6 中心層の二つの \(\sigma\)-固定方向だけを狙う class-6 掃引**
が唯一の最小転進である。

監査対象
`docs/命題_E23中心障害消滅_v1.md`
は全 173 行、SHA-256
`BBFB9FFF57662FB66466129250C0D4FBCFEF4D1FBB5EB53D6F36D294D7824919`
で固定した。

---

## F1. 符号監査 — (b) の相殺は正しい

交換子規約は
\[
[u,v]=u^{-1}v^{-1}uv,\qquad
uv=vu[u,v],\qquad
u^v=v^{-1}uv=u[u,v].
\]
\(g=s\bar f\),
\[
q_N=E_m\,\sigma^2(g)\sigma(g)g,\qquad
y=\sigma^2(g)\sigma(g)
\]
と置く。作用表の規約どおり
\[
\sigma^3(g)=E_m^{-1}gE_m
=g[g,E_m]
=g\,\beta(\bar f,\bar E_m).
\]
従って
\[
\begin{aligned}
\sigma(q_N)
 &=E_m\,\sigma^3(g)\sigma^2(g)\sigma(g)\\
 &=E_m\,g\,\beta(\bar f,\bar E_m)\,y\\
 &=E_m\,y\,g\,
   \beta(\bar f,\bar E_m)\,[g,y]\\
 &=q_N\,
   \beta(\bar f,\bar E_m)\,
   \beta(\bar f,\bar\sigma^2\bar f+\bar\sigma\bar f).
\end{aligned}
\]
ここで \(\bar f\in\mathcal L\) なら
\[
\bar\sigma^2\bar f+\bar\sigma\bar f
=-\bar E_m-\bar f.
\]
よって交代性から
\[
\beta(\bar f,-\bar E_m-\bar f)
=-\beta(\bar f,\bar E_m),
\]
二項は正確に逆符号で消える。従って
\[
\sigma(q_N)=q_N.
\]

重要なのは、内自己同型の向きが
\[
\operatorname{Inn}(E_m)(g)=E_m^{-1}gE_m
\]
であること、また \(g y=y g[g,y]\) を使うことの二点である。
配達された full-\(A\) 表と
`docs/notes/一致確認_E2作用表.md`
はいずれもこの規約で一致している。符号反転はない。

第一座標も
\[
\theta(q_\theta)
=g\theta(g)
=\theta(g)g\,[g,\theta(g)]
\]
であり、
\(\bar\theta\bar f=-\bar f\) と
\(\beta(\bar f,-\bar f)=0\) から
\[
\theta(q_\theta)=q_\theta.
\]
従って E23 の (a)(b) はともに **PASS**。

---

## F2. より短い独立証明 — 中央欠損は自動的に固定される

上の符号計算には、さらに強い座標自由な証明がある。

> **中央欠損補題 E23+。**
> \(1\to M\to G\to\bar G\to1\) を
> \(\sigma,\theta\)-安定な中央拡大とする。
> \[
> \theta^2=1,\qquad
> \sigma^3=\operatorname{Inn}(E),\qquad
> \sigma(E)=E
> \]
> とし、\(\bar g\in\bar G\) が二つの方程式を満たすとする。
> 任意の lift \(g\in G\) の欠損
> \[
> d_\theta:=\theta(g)g,\qquad
> d_N:=E\sigma^2(g)\sigma(g)g
> \]
> は \(M\) に入り、
> \[
> d_\theta\in M^\theta,\qquad d_N\in M^\sigma.
> \]

実際、\(d_\theta\in M\subset Z(G)\) と
\(\theta(g)=d_\theta g^{-1}\) から
\[
\theta(d_\theta)
=g\theta(g)
=g d_\theta g^{-1}
=d_\theta.
\]
同様に \(y=\sigma^2(g)\sigma(g)\) と置けば
\[
\begin{aligned}
\sigma(d_N)
 &=E(E^{-1}gE)y
  =gEy,\\
d_N&=Eyg
\quad\Longrightarrow\quad
Ey=d_Ng^{-1},
\end{aligned}
\]
ゆえに
\[
\sigma(d_N)=g d_Ng^{-1}=d_N.
\]

これは E23(b) の二つの \(\beta\)-項の相殺を、群の積だけで再証明している。
したがって相殺は Hall section、cocycle、class-2 座標の偶然ではない。
正確な標語は

> **線型段の解が欠損を中央核へ入れ、群恒等式がそれを固定部分へ入れ、
> (G2)(G3) が最後に殺す**

である。「線型方程式だけが無条件に二次障害を殺す」わけではない。

さらに
\[
M^\sigma=1,\qquad M^\theta=(1+\theta)M
\tag{2.1}
\]
なら \(d_N=1\)。また
\((1+\theta)z=d_\theta^{-1}\) となる \(z\in M\) を選べる。
\(M\) 上の \(\sigma\)-norm の像は
\[
\operatorname{im}(1+\sigma+\sigma^2)\subseteq M^\sigma=1
\]
なので、\(gz\) は norm 方程式を壊さず \(\theta\)-方程式も満たす。
これで E23 全体が従う。

この証明は Opus の証明から独立であり、符号事故を構造的に排除する。

---

## F3. (G2)(G3) の使用箇所

使用箇所は次の二箇所だけである。

1. **(G2)** \(C^\sigma=0\) により
   \[
   q_N\in C^\sigma\quad\Longrightarrow\quad q_N=0
   \]
   （乗法記法なら \(q_N=1\)）。
2. **(G3)** \(C^\theta=(1+\theta)C\) により
   \[
   q_\theta\in C^\theta
   \quad\Longrightarrow\quad
   q_\theta\in(1+\theta)C.
   \]

ここで E23 本文の最終段には一つ修文が要る。本文は別途
「系 E22.6 の \(\mathcal N_C=0\) の下で」と書くが、
\(\mathcal N_C=0\) は既に (G2) から従う。実際
\[
(\sigma-1)(1+\sigma+\sigma^2)=\sigma^3-1=0
\quad\text{on }C,
\]
従って
\[
\operatorname{im}\mathcal N_C\subseteq C^\sigma=0.
\]
よって
\[
\operatorname{im}\Lambda
=(1+\theta)C\times\{0\}
\]
は E22.6 を追加仮定せず得られる。

従って §4 の L4

> \(\mathcal N_C\ne0\) の対象では再検討が要る

は、E23 の仮定 (G2) の下では起こり得ない。L4 は削除するか、
「(G2) を落とす一般化では再検討が要る」と直すべきである。
これは定理の欠陥ではなく、依存関係をさらに短くする修正である。

---

## F4. 普遍 class-5 の全 \(j\)・全 \(m\)

class-5 の中心基底 \((t_5,t_6)\) では
\[
\sigma_C=
\begin{pmatrix}0&-1\\1&-1\end{pmatrix},
\qquad
\theta_C=
\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]
従って
\[
\det(1-\sigma_C)=3
\]
は任意の \(2\) 冪係数上で単元であり、(G2) が成立する。
また \(\theta\) は二基底を交換するので、任意の
\(R=\mathbb Z/2^e\) に対し
\[
C\cong R[C_2],\qquad
C^\theta=(1+\theta)C.
\]
従って (G3) も成立する。

ただし E23 §3 と検算スクリプトの \(j\) は、掃引宇宙の \(j\) と
一つずれている。正本の verbal 商では
\[
\bar A_j\cong(\mathbb Z/2^j)^{10},\qquad
C_j\cong(\mathbb Z/2^{j-1})^2.
\]
従って E23 §3 の
\[
\mathbb Z/2^j[C_2],\qquad
|C^\theta|=2^j
\]
は、実際の \(A_j\) については
\[
\mathbb Z/2^{j-1}[C_2],\qquad
|C_j^\theta|=2^{j-1}
\]
へ直すこと。\(j=1\) は \(C_1=0\) の可換 control である。

`week4-e2-vanish-check.mjs` は generic な係数環
\(\mathbb Z/2^e\), \(e=1,\dots,8\) を正しく検査している。
したがって数値自体は無傷だが、スクリプトの \(e\) を
掃引の \(j\) と同名にしない方がよい。

\(m\) への非依存も正しい。
\(a=y^m\) と置けば
\[
\sigma_m=\operatorname{Inn}(a)\tau,\qquad
E_m=\tau^2(a)\tau(a)a.
\]
共役自己同型の合成を三回展開すると群語として
\[
\sigma_m^3=\operatorname{Inn}(E_m),\qquad
\sigma_m(E_m)=E_m
\]
となる。後者は
\[
\tau(E_m)=a\tau^2(a)\tau(a),\qquad
a^{-1}\tau(E_m)a=E_m
\]
の一行でも確認できる。従って両式は全 \(m\in\mathbb Z\) で成立し、
中心上では inner 部分が消える。
従って E23.3 の
\[
\forall j\ge1,\ \forall m\in\mathbb Z:\quad\omega=0
\]
は上の添字修正後に **PASS**。

なお「(G2)(G3) はどちらも 2 群だから」という説明は弱めるべきである。

- (G2) は正確には **\(3\) が可逆**だからであり、任意の \(p\ne3\) に効く。
- (G3) は **この \(C_2\)-lattice が induced** だからであり、
  係数素数が \(2\) であること自体からは出ない。

class 6 では同じ \(2\) 冪係数でも (G3) が破れるので、この区別は
転進設計に実際に効く。

---

## F5. 系 E23.1・E23.2

E23.1 は直ちに正しい。
\(\omega\) が \(\mathcal L\) 上恒等的に零なら
\[
F(\bar k)
=\omega(\bar f_0+\bar k)-\omega(\bar f_0)=0.
\]
従って implementer の「定数」は厳密に \(0\) である。

E23.2 も正しい。\(K\subseteq\ker\bar{\mathcal N}\) で、weight-2 の
\(w\)-成分上では \(\bar{\mathcal N}=3\) だから
\[
3k_w=0.
\]
\(\bar A_j\) は \(2\) 群なので \(k_w=0\)。
一方
\[
\beta(u,v)
=(u_wv_p-u_pv_w)t_5+(u_wv_q-u_qv_w)t_6
\]
は一方の \(w\)-座標を必ず要する。従って
\[
\beta|_{K\times K}=0.
\]
full-\(A\) の交換子表は二独立導出が一致済みなので、この入力も
現在は単系統のままではない。ただし E23 本体は E23.2 に依存しない。

「障害群 \(\mathrm{Ob}\) が零」ではなく
「実際の障害元 \(\omega\) が恒等的に零」という語彙の区別も正しい。

---

## F6. 最小転進層の表現論的決定

\(L=\bigoplus L_n\) を rank \(2\) 自由 Lie 環、
\[
D:=L''=[L',L']
\]
とする。普遍 class-\(c\) 対象の
\([A,A]\) の weight-\(n\) 部分は \(D_n\) である。
自由 metabelian Lie 環の weight-\(n\) 部分を \(M_n\) とすれば
\[
0\longrightarrow D_n\longrightarrow L_n\longrightarrow M_n
\longrightarrow0.
\]
\[
\chi_{L_n}(g)
=\frac1n\sum_{d\mid n}\mu(d)
 \chi_V(g^d)^{\,n/d},
\qquad
M_n\otimes\mathbb Q
\cong\operatorname{Sym}^{n-2}(V)\otimes\mathrm{sgn}.
\tag{6.1}
\]
\(S_3\) の共役類を \((1,\sigma,\theta)\)
（\(\sigma\) は位数 \(3\)、\(\theta\) は対合）順に書く。
(6.1) から次を得る。

| weight \(n\) | \(\chi_{L_n}\) | \(\chi_{M_n}\) | \(\chi_{D_n}\) | \(D_n\otimes\mathbb Q\) |
|---|---|---|---|---|
| \(n<5\) | — | — | \(0\) | \(0\) |
| \(5\) | \((6,0,0)\) | \((4,1,0)\) | \((2,-1,0)\) | \(V\) |
| \(6\) | \((9,0,-1)\) | \((5,-1,-1)\) | \((4,1,0)\) | \(\mathbf1\oplus\mathrm{sgn}\oplus V\) |

位数 \(3\) の元 \(\sigma\) は \(\mathbf1\) と \(\mathrm{sgn}\) の双方で
恒等に作用し、\(V\) には固定ベクトルを持たない。従って
\[
D_5^\sigma=0,\qquad \dim_{\mathbb Q}D_6^\sigma=2.
\]
これで **weight 6 が最小**と決まる。

注意すべき点は、自由 Lie 環 \(L_5\) 自体には自明成分があるが、
metabelian 部分 \(M_5\) にも同じ成分があり、差
\(D_5=L''_5\) では消えることである。
「自由 Lie 環の自明成分の初出」と「中心
\([A,A]\) の \(\sigma\)-固定成分の初出」を混同してはならない。

---

## F7. weight 6 の整数基底と二つの固定方向

weight \(2,3,4\) の既存基底を
\[
w;\qquad p,q;\qquad r_1,r_2,r_3
\]
とし、
\[
\begin{aligned}
u_1&=[w,r_1],&
u_2&=[w,r_2],&
u_3&=[w,r_3],&
u_4&=[p,q].
\end{aligned}
\tag{7.1}
\]
と置く。weight 6 では
\[
D_6=[L_2,L_4]+[L_3,L_3]
\]
であり、
\[
\operatorname{rank}D_6
=\dim L_6-\dim M_6=9-5=4.
\]
(7.1) の四元は \(D_6\) を生成するので整数基底である。

既監査の graded 作用
\[
\begin{aligned}
&\sigma(w)=w,\quad
\sigma(p)=q,\quad\sigma(q)=-p-q,\\
&\sigma(r_1)=r_3,\quad
\sigma(r_2)=-r_2-r_3,\quad
\sigma(r_3)=r_1+2r_2+r_3
\end{aligned}
\]
から
\[
\begin{array}{c|cccc}
 &u_1&u_2&u_3&u_4\\ \hline
\sigma&
u_3&-u_2-u_3&u_1+2u_2+u_3&u_4
\end{array}
\tag{7.2}
\]
を得る。また
\[
\theta(w)=-w,\quad
\theta(p)=-q,\quad\theta(q)=-p,\quad
\theta(r_1)=-r_3,\quad
\theta(r_2)=-r_2,\quad
\theta(r_3)=-r_1
\]
より
\[
\begin{array}{c|cccc}
 &u_1&u_2&u_3&u_4\\ \hline
\theta&
u_3&u_2&u_1&-u_4.
\end{array}
\tag{7.3}
\]

ここで元の作用表にある高 weight 補正は問題にならない。
\(u_i\) は最大 weight \(6\) にあり、補正を (7.1) の交換子へ入れると
weight \(\ge7\) となって \(\gamma_7\) で消える。従って
(7.2)(7.3) は associated graded だけでなく
\(F_2/\gamma_7\) の \(D_6\) 上で厳密である。

従って
\[
a:=u_4=[p,q],\qquad
b:=u_1+u_2+u_3
\tag{7.4}
\]
は
\[
\sigma(a)=a,\quad\theta(a)=-a,\qquad
\sigma(b)=b,\quad\theta(b)=b.
\]
これが転進先で追うべき二本の中心方向である。

---

## F8. (G3) も class 6 で初めて破れる

weight 5 の \(D_5\) は基底 \(t_5,t_6\) を \(\theta\) が交換する
induced module だった。

weight 6 では (7.3) により
\[
D_6|_{\langle\theta\rangle}
\cong
\underbrace{\langle u_1,u_3\rangle}_{\text{regular/induced}}
\oplus
\underbrace{\langle u_2\rangle}_{\theta=+1}
\oplus
\underbrace{\langle u_4\rangle}_{\theta=-1}.
\]
\(R=\mathbb Z/2^e\), \(e\ge1\) とする。
\(u_2\in D_6^\theta\) だが、\((1+\theta)z\) の \(u_2\)-係数は常に
\(2z_{u_2}\) なので
\[
u_2\notin(1+\theta)D_6.
\]
また \(\theta=-1\) の \(u_4\) 方向にも位数 \(2\) の固定元が残り、
\((1+\theta)u_4=0\) である。
従って
\[
D_6^\theta\ne(1+\theta)D_6.
\]

total center では weight-5 から weight-6 への上三角補正があり得るが、
この結論も変わらない。短完全列
\[
0\longrightarrow D_6\longrightarrow C^{(6)}
\longrightarrow D_5\longrightarrow0
\]
で \(D_5|_{\langle\theta\rangle}\) は induced、従って Tate
コホモロジーが全次数で零である。長完全列から
\[
\widehat H^0(\langle\theta\rangle,C^{(6)})
\cong
\widehat H^0(\langle\theta\rangle,D_6)\ne0.
\]
よって weight-5 由来の補正が (G3) の破れを修復することはない。

つまり **(G2) と (G3) は同じ最小 weight 6 で同時に破れる。**
class 6 は二条件のどちらを狙っても同じ一意な転進先になる。

---

## F9. class 6 はまだ E22′ の射程内

\(A^{(6)}=\gamma_2/\gamma_7\) とする。
rank \(2\) 自由群では
\[
[\gamma_2,\gamma_2]\subseteq\gamma_5
\]
（weight 4 の候補 \([L_2,L_2]\) は零）なので
\[
[[A^{(6)},A^{(6)}],A^{(6)}]
\subseteq\gamma_7/\gamma_7=1.
\]
従って \(A^{(6)}\) は class \(2\) で、
\[
C^{(6)}=[A^{(6)},A^{(6)}]
=D_5\oplus D_6
\]
は中心、階数 \(2+4=6\) である。

また
\[
\operatorname{rank}\bar A^{(6)}
=\sum_{n=2}^6(n-1)=15,
\qquad
\operatorname{rank}A^{(6)}=15+6=21.
\]
従って class-6 転進では

- \(\bar A_j\cong(\mathbb Z/2^j)^{15}\)。
- \(C_j\cong(\mathbb Z/2^{j-1})^6\)。
- E22′ の同じ二欠損 \(q_\theta,q_N\) と同じ \(\Lambda\)。

をそのまま使える。class(A)\(\ge3\) 用の新理論を待つ必要はない。
class(A)\(\ge3\) が初めて現れるのは次の
\(F_2/\gamma_8\) 側である。

---

## F10. 転進掃引を二方向へ縮約する

\(R=\mathbb Z/2^e\), \(e=j-1\ge1\) とする。
weight 5 と weight 6 の標準表現成分には \(\sigma\)-固定点がない。
従って
\[
(C_j^\sigma)^\theta
\]
へ寄与できるのは (7.4) の二方向だけである。
weight filtration 上で作用が上三角になる可能性はあるが、
\(3\) は \(R\) 上可逆なので \(C_3=\langle\sigma\rangle\) の
不変部分関手は完全である。従って weight-5 の標準成分から
隠れた固定 lift が増えることもない。
2-primary 上では \(3^{-1}\) が存在し、
\[
C_j^\sigma=Ra\oplus Rb,\qquad
\theta(a)=-a,\quad\theta(b)=b.
\]
従って潜在障害群は
\[
\boxed{
(C_j^\sigma)^\theta
\cong R[2]\,a\oplus R\,b
\cong\mathbb Z/2\oplus\mathbb Z/2^e.
}
\tag{10.1}
\]

具体的には norm 欠損が中心補正 \(z_+=-3^{-1}q_N\) を強制し、
残る障害は
\[
\operatorname{ob}
=(q_\theta)_+
-3^{-1}(1+\theta)q_N
\in(C_j^\sigma)^\theta.
\tag{10.2}
\]
従って次の掃引は、全 \(6\) 中心座標を盲目的に走査するのでなく、

1. \(a=[p,q]\) 方向の位数 \(2\) 座標。
2. \(b=[w,r_1]+[w,r_2]+[w,r_3]\) 方向の
   \(\mathbb Z/2^{j-1}\) 座標。

だけを最終 target として登録すべきである。

最小 falsification gate は \(j=2\)
（\(C_2\) は mod \(2\)、(10.1) は \((\mathbb Z/2)^2\)）である。
まず class-6 full-action 表を二系統化し、既存の \(m=0,\dots,63\)
窓でこの二ビットを掃く。ここが全零なら初めて \(j\) を上げる、
という段階設計が最小である。
この有限 \(m\) 窓の通過から全 \(m\) を推論してはならない。

ただし、この普遍 congruence 商で非零障害が出ても、
有限許容 \(PB_3/N\) への実現と charming 性なしには E15 の反例ではない。
既存の実現ギャップは維持する。

---

## F11. class(A)\(\ge3\) への射程

「線型段を解いた事実自身が二次段を殺す」という表現は、
次の形なら class(A)\(\ge3\) に一般化できる。

nilpotent \(A\) の \(\sigma,\theta\)-安定な中心列を一段ずつ取り、
\[
1\to M_r\to A/\Gamma_{r+1}\to A/\Gamma_r\to1
\]
で解を持ち上げる。商で既に二方程式を満たす lift \(g\) の欠損は、
F2 の中央欠損補題により自動的に
\[
d_{\theta,r}\in M_r^\theta,\qquad
d_{N,r}\in M_r^\sigma
\]
へ入る。各段で
\[
M_r^\sigma=0,\qquad
M_r^\theta=(1+\theta)M_r
\tag{11.1}
\]
なら、その段の lift 障害は零である。従って全中心層で (11.1) が
成立すれば、最初の可換段の解は \(A\) まで逐次的に持ち上がる。

これは E23 を一段の class-2 定理から
**central-layer induction lemma** へ一般化するものである。
class-3 以上でも Hall の高次二次式を一度に書く必要はない。

ただし「最初の線型解だけで無条件に全高次障害が消える」わけではない。
各中心層で (11.1) を検査する必要があり、どこかで
\(M_r^\sigma\ne0\) または Tate \(\hat H^0\ne0\) なら障害元を実計算する。
従って【GAP-E18】は、**全層が (11.1) を満たす対象については閉じる**が、
一般には残る。

なお今回の最小転進 class 6 は F9 のとおりまだ class \(2\) なので、
この新しい帰納枠組みを最初の掃引へ持ち込む必要はない。

---

## F12. 状態札

| 主張 | 裁定 |
|---|---|
| 定理 E23 | **paper mutual-audit PASS** |
| (b) の相殺符号 | **PASS**。交換子計算と中央欠損補題の二経路 |
| 系 E23.1 \(F|_K=0\) | **PASS** |
| 系 E23.2 \(\pi B=0\) | **PASS** |
| 系 E23.3 全 \(j\)・全 \(m\) | **PASS**。ただし \(C_j\) の添字を \(2^{j-1}\) へ修正 |
| weight/class の最小性 | **紙上 PASS**: weight 6 / class 6 |
| (G3) の最初の破れ | **紙上 PASS**: 同じ weight 6 |
| class(A)\(\ge3\) 一般化 | **命題候補 E23+**。中央一段の補題は証明済み、全層版は条件 (11.1) つき |
| Lean verified | なし |

作用表 608 セルと 384 系・409 証明書の機械状態は開示どおり採用した。
本返信が追加するのは紙上の定理監査と表現論的な転進決定であり、
それらを `cross-checked` や `verified` とは呼ばない。

---

## ★ 教材

1. **符号に敏感な相殺は、可能なら共役恒等式へ持ち上げる。**
   二つの \(\beta\)-項が消える本当の理由は、欠損が中央に入った瞬間
   \(\sigma(d_N)=g d_Ng^{-1}=d_N\) となることだった。
2. **自由 Lie 環全体の自明成分と、第二導来の自明成分は別物。**
   weight 5 の自明成分は metabelian 商へ流れ、\([A,A]\) には残らない。
3. **「次の class」を撃つのでなく、壊れる表現を先に特定する。**
   今回は weight 6 の
   \(\mathbf1\oplus\mathrm{sgn}\) が class 6 を一意に指定した。
4. **induced 性は素数の性質ではなく lattice の性質。**
   class 5 で成立し、同じ 2-primary の class 6 で破れる。
5. **高 nilpotency class は一括 BCH でなく中央層ごとに扱える。**
   欠損固定性は各中央拡大で同じ二行から出る。

---

## 考察と提案

P178【E23+】F2 の中央欠損補題を、E23 の主証明へ格上げする。
現行の \(\beta\)-相殺は規約照合用の補助証明として残す。

P179【転進】次の数学対象を
\[
P^{(6)}=F_2/\gamma_7,\qquad A^{(6)}=\gamma_2/\gamma_7
\]
に固定し、中心 target を (7.4) の \(a,b\) 二方向へ縮約する。

P180【最小 gate】class-6 作用表の二系統一致後、
まず \(j=2\)・既存 \(m=0,\dots,63\) の二ビット掃引を行う。
全零の場合だけ高い \(j\) へ進む。

P181【一般化】class 7 以降へ進む前に、F11 の
central-layer induction lemma を正式命題化し、各 graded kernel の
(G2)(G3) 表を事前登録する。

W137【添字】verbal 商の中心は mod \(2^{j-1}\)。
generic な係数指数 \(e\) と掃引添字 \(j\) を同名にしない。

W138【固定成分】\(L_n\) の自明成分をそのまま
\(L''_n=[A,A]_n\) の自明成分と読まない。

W139【素数説明】(G2) は \(p\ne3\)、(G3) は induced lattice。
両者を一括して「2 群だから」と書かない。

W140【障害語彙】障害群が非零でも、実際の障害写像が恒等零になり得る。
常に「群」と「元／写像」を分ける。

---

## 監査範囲外の申告

- GAP、node、Python、Lean は実行していない。
  `search/week4-e2-vanish-check.mjs` はコードを静的に読んだだけである。
- 384 系と 409 証明書の全件再検算はしていない。
  作用表 608 セル一致と証明書 ALL PASS は委嘱の開示として採用した。
- class-6 の full Hall 作用表、有限 PC presentation、実掃引は作成していない。
  本便で決定したのは対象・中心基底・最小 target までである。
- class-6 congruence 商の有限許容対象への実現性と charming 性は
  依然として射程外である。
- A5 戦線の新規 v4 には触れていない。
- 過去返信ファイルは編集していない。本便で編集した成果物は
  `sol/sol_reply_19_e23.md` のみである。
