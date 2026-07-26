# Sol 返信 — 第 15 便: \(A_5\) 窓の算術飽和と rigidity 路線

## 冒頭判定

**総合判定は (c) 部分的。**

| 問い | 裁定 |
|---|---|
| \(A_5\) の \((5,5,5)\) rigidity | **PASS**。\(5A^3\)、\(5B^3\) はそれぞれ生成する inner rigid orbit を一つ持つ |
| \(5A/5B\) の有理性 | **\(\mathbf Q(\sqrt5)\) の壁が実在**。inner marking では二成分、outer/absolute dessin では両者が一つに合流する |
| 「5 個の分解を通常 dessin の 5 個の moduli 点として追う」路線 | **(b) 不能**。5 個は \(C_{A_5}(v)=C_5\) の同時共役で一つの dessin 同型類に潰れる |
| rooted / tangentially framed dessin への修正 | **(a) 実行可能性が高い**。5 点は \(\mu _5\)-torsor として残り、問題は一つの Kummer 類へ落ちる |
| 明示算術 | passport \((2^2 1,3 1^2,5)\) の \(\mathbf Q\)-Belyi 多項式から、自然な無限遠 tangential torsor の候補 \(\lambda^5=-16/27\) を紙上で得た |
| \(\operatorname{Ih}_{N_A}\) の全射性 | **未確定 / UNKNOWN**。上の tangential torsor と shadow の \(C_5\) 座標を、inner lift まで保って同定する比較補題がまだ無い |

★ 核心は、**rigidity が弱いことではなく、通常の dessin 同型類が強く割りすぎていること**である。\(C_5\) は \(A_5\) の inner automorphism なので、unrooted dessin へ移した瞬間に消える。一方、接方向を固定した framed dessin なら、その同じ \(C_5\) が局所 Kummer torsor として現れる。従って本路線は捨てるべきではないが、「ordinary moduli field を計算すれば全射性が出る」という原案のままでは成立しない。

---

## F1. 算術問題は affine cocycle 一個に等価

既知の cross-checked な同型を
\[
\Phi:\operatorname{GTSh}(N_A,N_A)
 \xrightarrow{\sim}
N_{S_5}(\langle X\rangle)
\cong \operatorname{AGL}_1(\mathbf F_5)
=\mathbf F_5\rtimes\mathbf F_5^\times
\]
とする。5 文字を \(\mathbf F_5\) と同一視し、\(X:a\mapsto a+1\) と取る。

\[
\rho_A:=\Phi\circ\operatorname{Ih}_{N_A}:G_{\mathbf Q}
\longrightarrow \operatorname{AGL}_1(\mathbf F_5)
\]
は
\[
\rho_A(\gamma)(a)=\chi _5(\gamma)a+b_\gamma
\tag{1.1}
\]
と一意に書ける。ここで線形部は \(u=2m+1\bmod5\)、すなわち mod \(5\) 円分指標であり、
\[
b_{\gamma\delta}
=b_\gamma+\chi _5(\gamma)b_\delta
\tag{1.2}
\]
である。

従って \(b\) は
\[
[b_A]\in H^1(G_{\mathbf Q},\mathbf F_5(1))
\cong H^1(G_{\mathbf Q},\mu _5)
\cong \mathbf Q^\times/(\mathbf Q^\times)^5
\tag{1.3}
\]
を定める。affine 原点の変更は coboundary、\(\mathbf F_5\) 座標の倍率変更は \([b_A]\) の非零冪を取るだけなので、**零か非零かは marking に依らない**。

\(\chi _5:G_{\mathbf Q}\twoheadrightarrow\mathbf F_5^\times\cong C_4\) は全射である。従って
\[
\operatorname{im}\rho_A=
\begin{cases}
\text{\(C_4\) の一つの complement},&[b_A]=0,\\
F_{20},&[b_A]\ne0.
\end{cases}
\tag{1.4}
\]
実際 \(K=\mathbf Q(\zeta _5)\) 上では線形部が消え、
\[
\rho_A(G_K)\le \mathbf F_5.
\]
\(\mathbf F_5\) は素数位数なので、ここに非自明な元が一つあれば像は \(C_5\) 全体である。また
\[
H^1(C_4,\mathbf F_5(1))=0
\]
（位数 4 と 5 が互いに素）なので、inflation–restriction により \([b_A]\ne0\) なら \(G_K\) への制限も非零である。逆に制限が零なら像は一つの complement であり、全 complement は translation 共役だから \([b_A]=0\) である。

従って主問題は正確に
\[
\boxed{\quad
\operatorname{Ih}_{N_A}\text{ が全射}
\iff [b_A]\ne0
\iff \rho_A(G_{\mathbf Q(\zeta _5)})=C_5.
\quad}
\tag{1.5}
\]

円分 \(C_4\) は「見込み」より一段強く、比較規約を固定すれば形式的に覆われる。未解決部分は Kummer 類 \([b_A]\) 一個だけである。

---

## F2. \(A_5\) の 5-cycle 類と \(\mathbf Q(\sqrt5)\) の壁

\(A_5\) の非自明共役類を
\[
2A,\quad 3A,\quad 5A,\quad 5B
\]
と書く。5-cycle \(v\) を一つ固定すると、一つの Sylow-\(5\) 群内で
\[
5A\cap\langle v\rangle=\{v,v^{-1}\},\qquad
5B\cap\langle v\rangle=\{v^2,v^{-2}\}
\tag{2.1}
\]
となるようにラベルできる。

従って power map \(v\mapsto v^u\) に関して

- \(u\equiv\pm1\pmod5\) は \(5A\) を保つ。
- \(u\equiv\pm2\pmod5\) は \(5A\leftrightarrow5B\) を交換する。

一つの類の stabilizer は
\[
\{\pm1\}<(\mathbf Z/5)^\times,
\]
その固定体は
\[
\mathbf Q(\zeta _5)^{\{\pm1\}}=\mathbf Q(\sqrt5).
\tag{2.2}
\]
よって \(5A\)、\(5B\) は個別には \(\mathbf Q\)-rational class ではなく、\(\mathbf Q(\sqrt5)\)-rational である。これは既知の
\[
\operatorname{GTSh}(N_A)\longrightarrow
\operatorname{Out}(A_5)\cong C_2
\]
が Legendre 記号
\[
u\longmapsto\left(\frac{u}{5}\right)
\]
になることと完全に整合する。

ただし、この二次情報は \(F_{20}\twoheadrightarrow C_2\) までしか見ない。translation kernel \(C_5\) は inner なので、\(\mathbf Q(\sqrt5)\) の壁を越えただけでは主問題は解けない。

---

## F3. 対称 \((5,5,5)\) triple は geometrically rigid

\(C=5A\) とし、固定した \(z\in C\) に対して
\[
x,y\in C,\qquad xyz=1
\tag{3.1}
\]
を満たす ordered pair の数を数える。

\(A_5\) の既約指標の \(5A\) 上の値は
\[
1,\quad \varphi,\quad \varphi',\quad -1,\quad 0,
\qquad
\varphi=\frac{1+\sqrt5}{2},\quad
\varphi'=\frac{1-\sqrt5}{2},
\]
次数は \(1,3,3,4,5\) である。従って class multiplication formula より
\[
\begin{aligned}
n_C(z)
&=\frac{|C|^2}{|A_5|}
\left(
1+\frac{\varphi^3+(\varphi')^3}{3}-\frac14
\right)\\
&=\frac{12^2}{60}
\left(1+\frac43-\frac14\right)
=5.
\end{aligned}
\tag{3.2}
\]

全 triple 数は \(12\cdot5=60\)。また、これらは全て \(A_5\) を生成する。実際、5-cycle を含む proper maximal subgroup は \(D_{10}\) であり、その order-\(5\) 元は一つの \(\langle z\rangle\) に入る。しかし (2.1) の指数 \(\{1,-1\}\) の二つを足しても、積条件に必要な指数 \(-1\) にはならない。従って \(5A^3\) triple は \(D_{10}\) 内には無い。

生成 triple の同時共役 stabilizer は
\[
C_{A_5}(\langle x,y,z\rangle)=Z(A_5)=1.
\]
従って一軌道の大きさは 60 であり、全 60 triple が一つの inner orbit をなす。

\[
\boxed{\operatorname{Ni}^{\mathrm{in}}(A_5;5A,5A,5A)
\text{ は一点。}}
\tag{3.3}
\]

同じ計算により \(5B^3\) も一点である。よって両者はそれぞれ geometrically rigid である。

---

## F4. inner rigidity と absolute descent を分ける

F2–F3 から、ordered branch points を固定した inner/G-marked 問題には

\[
\mathcal H_{5A^3}^{\mathrm{in}},\qquad
\mathcal H_{5B^3}^{\mathrm{in}}
\]
という二つの零次元幾何成分があり、各々の field of moduli は \(\mathbf Q(\sqrt5)\) である。非平方の円分 exponent は両成分を交換する。

一方、
\[
\operatorname{Aut}(A_5)=S_5
\]
の odd element が \(5A\leftrightarrow5B\) を交換する。従って Aut\((A_5)\)-orbit、すなわち unmarked regular dessin としては二成分が一つに合流し、absolute field of moduli は \(\mathbf Q\) になる。

ここで区別すべき三段は次である。

| 対象 | 見える体 |
|---|---|
| exact 5-cycle generator \(v\) | \(\mathbf Q(\zeta _5)\) |
| \(A_5\)-inner marking、class \(5A\) | \(\mathbf Q(\sqrt5)\) |
| Aut\((A_5)\) まで割った unmarked dessin | \(\mathbf Q\) |

従って rational rigidity が直接与えるのは、marked cover の \(\mathbf Q(\sqrt5)\) 上の降下と、weak/Aut-rational な unmarked object の \(\mathbf Q\) 上の降下である。**この表のどの段にも degree \(5\) の体はまだ現れない。**

---

## F5. \((2,3,5)\) triple の 5 分解も global には rigid

固定 \(v\in5A\) に対して
\[
\mathcal D(v):=
\{(q,r):q\in2A,\ r\in3A,\ qrv=1\}
\tag{5.1}
\]
とする。積の左右や \(v^{-1}\) の規約を変えても以下の結論は変わらない。

class multiplication formula では、非自明指標の積
\[
\chi(2A)\chi(3A)\chi(5A)
\]
は全て零になるため、
\[
|\mathcal D(v)|
=\frac{|2A||3A|}{|A_5|}
=\frac{15\cdot20}{60}
=5.
\tag{5.2}
\]

\(2,3,5\) の三位数を同時に含む proper subgroup は無いので、5 triple は全て \(A_5\) を生成する。また
\[
C_{A_5}(v)=\langle v\rangle\cong C_5
\]
が
\[
(q,r)\longmapsto
(v^jqv^{-j},\,v^jrv^{-j})
\tag{5.3}
\]
で自由推移的に作用する。

しかし \(v\) を \(5A\) 全体に動かすと triple の総数は再び
\[
12\cdot5=60.
\]
生成性から同時共役 stabilizer は自明なので、これは **一つの inner Nielsen orbit** である。

\[
\boxed{\text{fixed-\(v\) では 5 点だが、同時共役で割ると一つの dessin。}}
\tag{5.4}
\]

ここが本監査の決定点である。5 個は五つの普通の dessin ではなく、**一つの dessin の五つの frame** である。

---

## F6. 次数・種数・Hurwitz 次元

関係する曲線を混同しないため、Riemann–Hurwitz を分けて記す。

| triple / 表現 | degree | branch cycle の cycle 数 | genus |
|---|---:|---:|---:|
| \((5,5,5)\)、regular \(A_5\) | 60 | \(12,12,12\) | 13 |
| \((5,5,5)\)、自然な 5 点表現 | 5 | \(1,1,1\) | 2 |
| \((2,3,5)\)、regular \(A_5\) | 60 | \(30,20,12\) | 0 |
| \((2,3,5)\)、自然な 5 点表現 | 5 | \(3,3,1\) | 0 |

例えば regular \((5,5,5)\) では
\[
2-2g=12+12+12-60=-24,
\]
従って \(g=13\)。自然な \((2,3,5)\) dessin では
\[
2-2g=3+3+1-5=2,
\]
従って \(g=0\)。

branch point は \(0,1,\infty\) の三点に固定され、F3 と F5 の Nielsen class は rigid なので、対応 Hurwitz space は **零次元**である。従って「5 分解の moduli 曲線の genus」を求める対象は無い。genus を持つのは上表の covering curve であり、5 分解を保つ修正版は有限 étale torsor である。

---

## F7. ordinary dessin 路線が \(C_5\) を失う正確な場所

child's drawing の定義は transitive homomorphism
\[
\psi:F_2\to S_d
\]
の \(S_d\)-同時共役類 \([\psi]\) である。

[GT-shadows and child's drawings, Theorem 3.1](../papers/2106.06645-gt-shadows-childs-drawings.pdf) は
\[
\psi^{(m,f)}(x)=\psi(x^{2m+1}),\qquad
\psi^{(m,f)}(y)=\psi(f^{-1}y^{2m+1}f)
\tag{7.1}
\]
を与えるが、cofunctor の値は最終的に
\[
[\psi^{(m,f)}]
\]
である。従って inner conjugation は全て不可視になる。

同じ現象は [Guillot, *The Grothendieck–Teichmüller group of a finite group*](../papers/delivered/guillot_1407.3112.pdf) の枠組みでも明示的である。

- generating pair は regular dessin では Aut\((G)\) まで割られる。
- \(G\)-dessin / inner Nielsen class でも simultaneous \(G\)-conjugacy まで割られる。
- Guillot, Theorem 5.2 では
  \[
  GT_1(PSL_2(\mathbf F_4))=GT_1(A_5)=1.
  \]
- 従って通常の \(A_5\)-monodromy dessin の moduli field は abelian である。

これは \(GTSh(N_A)\cong F_{20}\) と矛盾しない。Guillot 側は dessin の isomorphism class、こちらは一つの marking の inner lift を見ている。むしろ、
\[
C_5\le\operatorname{Inn}(A_5)
\]
が ordinary dessin quotient で消えることを正確に診断している。

従って非可換な \(F_{20}\)-extension を **ordinary \(A_5\) dessin の moduli field** として探す計画は停止すべきである。関連する \(F_{20}\) 型の dessin 体が一般に存在することは、例えば [Daire–Kato–Uchino](https://arxiv.org/abs/2109.14945) の
\(\mathbf Q(\zeta _p,\sqrt[p]{q})\) 型の構成から分かるが、それは本 \(A_5\) unrooted dessin がその体を持つという主張ではない。

---

## F8. 正しい置換先は framed \(\mu _5\)-torsor

通常の同型類を取る前に、次を保持する。

1. exact inertia generator \(v\)。
2. \(v\) の上の tangential lift、またはそれと同値な distinguished root/sheet。
3. その frame を動かす simultaneous inner conjugationを同型として割らない。

この framed object の幾何点は \(\mathcal D(v)\) の 5 点であり、\(\langle v\rangle\) が自由推移的に作用する。exact \(v\) が固定される
\[
K=\mathbf Q(\zeta _5)
\]
上では constant \(C_5\)-torsor、\(\mathbf Q\) 上では cyclotomic twisting を持つ \(\mu _5\)-torsor と読むのが正しい。

F1 の Kummer 類を \(a_A\in\mathbf Q^\times/(\mathbf Q^\times)^5\) で表すなら、比較補題の成立後には framed moduli object は
\[
\mathcal T_A\simeq
\operatorname{Spec}\mathbf Q[t]/(t^5-a_A)
\tag{8.1}
\]
と書ける。\(a_A\ne1\) in \(\mathbf Q^\times/(\mathbf Q^\times)^5\) なら
\[
E=\mathbf Q(\sqrt[5]{a_A}),\qquad [E:\mathbf Q]=5,
\tag{8.2}
\]
その Galois closure は
\[
L=\mathbf Q(\zeta _5,\sqrt[5]{a_A}),\qquad
\operatorname{Gal}(L/\mathbf Q)\cong F_{20}.
\tag{8.3}
\]
さらに
\[
[L:\mathbf Q(\zeta _5)]=5,\qquad
L^{C_5}=\mathbf Q(\zeta _5),\qquad
L^{D_{10}}=\mathbf Q(\sqrt5).
\tag{8.4}
\]

(8.2) の次数 5 は、素数次数の binomial に対する既約性判定、すなわち \(a_A\notin(\mathbf Q^\times)^5\) なら \(T^5-a_A\) が既約であることによる。

よって「5 個の moduli 体」の正確な予想は、

- unframed dessin: 一点、absolute field of moduli は \(\mathbf Q\)。
- inner class: \(\mathbf Q(\sqrt5)\)。
- 一つの frame: 非 Galois な degree-\(5\) 体 \(E\)。
- 全 frame の正規閉包: degree \(20\) の \(F_{20}\)-extension \(L\)。
- exact \(v\) を固定した後: \(L/\mathbf Q(\zeta _5)\) が cyclic degree \(5\)。

である。

また
\[
G_{\mathbf Q(\zeta _5)}
\text{ が }\mathcal D(v)\text{ 上推移的}
\iff [L:\mathbf Q(\zeta _5)]=5
\iff [b_A]\ne0.
\tag{8.5}
\]
これが課題文の「\(C_5\) 推移性 \(\Longleftrightarrow\) Galois orbit」の、quotient を取り違えない正確な形である。

---

## F9. degree \(5\), genus \(0\) の明示 Belyi 候補

passport
\[
(2^2 1,\ 3 1^2,\ 5)
\]
を持つ \((2,3,5)\) dessin には、次の \(\mathbf Q\)-model がある。

\[
\boxed{
B(z)=
\frac{(3-4z)(2z^2+2z+3)^2}{27}
=
1-\frac{4z^3(4z^2+5z+10)}{27}.
}
\tag{9.1}
\]

この二つの因数分解から直ちに、

- \(B^{-1}(0)\) の ramification partition は \(2,2,1\)。
- \(B^{-1}(1)\) は \(3,1,1\)。
- \(B^{-1}(\infty)\) は \(5\)。

と分かる。全 branch permutation は偶置換で、transitive monodromy は位数 \(2,3,5\) の元を含むので \(A_5\) である。

無限遠で
\[
s=\frac1z,\qquad T=\frac1{B(z)}
\]
と置くと、\(B\) の leading coefficient が
\[
c=-\frac{16}{27}
\]
なので
\[
T=-\frac{27}{16}s^5+O(s^6).
\tag{9.2}
\]
unit target tangent を持ち上げる五つの leading direction \(\lambda\) は
\[
\boxed{\lambda^5=-\frac{16}{27}}
\tag{9.3}
\]
を満たす。

\[
v_2(-16/27)=4\not\equiv0\pmod5
\]
なので \(-16/27\) は \(\mathbf Q\) の fifth power ではない。従ってこの自然な tangential fiber は非自明な \(\mu _5\)-torsor であり、その splitting field は
\[
\mathbf Q\!\left(\zeta _5,\sqrt[5]{-16/27}\right)
\]
という \(F_{20}\)-extension になる。

これは機械探索ではなく、(9.1) の二つの因数分解と無限遠の leading term だけによる紙計算である。

---

## F10. \(-16/27\) を直ちに \(a_A\) と宣言してはいけない

F9 は非常に強い攻略候補だが、現時点で証明したのは

> 明示 \((2,3,5)\) Belyi map の、選んだ無限遠 tangential basepoint の lift torsor

が非自明ということだけである。未証明なのは

\[
\{\text{その五つの接方向}\}
\stackrel{?}{\cong}
\{\text{shadow の fixed-\(v\) 五分解}\}
\tag{10.1}
\]
の **\(G_{\mathbf Q}\)-equivariant な同定**である。

幾何的には両辺とも \(C_5\)-torsor なので、\(\overline{\mathbf Q}\) 上の全単射だけなら自動的に作れる。しかし二つの torsor は
\[
H^1(G_{\mathbf Q},\mu _5)
\]
の異なる twist であり得る。従って「どちらも 5 点」「どちらも \(C_5\) が自由推移的」だけでは算術同定にならない。

また、本工房の標準 tangential basepoint、\(x,y\) の向き、\((q,r,v)\) の積規約、cofunctor による逆向き作用を固定しないと、得られる radicand は逆元や非零冪に変わる。逆元・非零冪なら非自明性は保たれるが、別の basepoint twist を未計算のまま足すことは許されない。

従って現時点の正しい状態札は
\[
\boxed{
a_A\stackrel{?}{=}
\left[-\frac{16}{27}\right]^{e},
\quad e\in\mathbf F_5^\times,
\qquad\text{comparison 未証明。}
}
\tag{10.2}
\]

である。ここを証明できれば、\(v_2(-16/27)=4\) が直ちに全射性を閉じる。

---

## F11. 必要な比較補題の設計図

以下を **Framed Comparison Lemma \(FC(A_5)\)** として独立に起案すべきである。

### FC-0. data と規約

\[
U=\mathbf P^1_{\mathbf Q}\setminus\{0,1,\infty\}
\]
の標準 tangential basepoint \(\vec b\)、幾何生成元 \(x,y\)、および
\[
\rho_0:\widehat F_2\twoheadrightarrow A_5,\qquad
x\mapsto X,\quad y\mapsto Y,\quad\ker\rho_0=N_A
\tag{11.1}
\]
を固定する。

さらに、

- \(w=X^3\) など、既存 marking と fixed-\(v\) の正確な対応。
- 一つの factorization \((q_0,r_0,w)\)。
- (9.1) の幾何 monodromy triple と \((q_0,r_0,w)\) の明示同定。
- \(\vec b\) から order-\(5\) branch への étale path と tangential lift。

を data に含める。ここを「共役まで」で済ませてはいけない。

### FC-1. Ihara pair の exact formula

\(\gamma\in G_{\mathbf Q}\) に対して
\[
u_\gamma=\chi(\gamma)\bmod10,\qquad
m_\gamma=\frac{u_\gamma-1}{2}\bmod5
\]
とし、Ihara pair を本工房と同じ規約で
\[
x\longmapsto x^{u_\gamma},\qquad
y\longmapsto f_\gamma^{-1}y^{u_\gamma}f_\gamma
\tag{11.2}
\]
と書く。

その reduction が
\[
\beta_\gamma(X)=X^{u_\gamma},\qquad
\beta_\gamma(Y)=\bar f_\gamma^{-1}Y^{u_\gamma}\bar f_\gamma
\tag{11.3}
\]
を満たす actual automorphism
\(\beta_\gamma\in\operatorname{Aut}(A_5)=S_5\)
であることを示す。

### FC-2. shadow と actual automorphism の一致

既知の \(\Phi\) に対して
\[
\boxed{
\Phi(\operatorname{Ih}_{N_A}(\gamma))=\beta_\gamma
}
\tag{11.4}
\]
を **Out\((A_5)\) でなく Aut\((A_5)\) 内の等式**として証明する。

右作用・左作用または cofunctor のため逆元が入るなら、(11.4) を最初からその規約で書き直す。最終的に「同じ outer class」しか示さない命題では \(C_5\) は全く見えない。

### FC-3. modular factorization への word-level functor

shadow の hexagon から得る \((q,r,v_m)\) と、Belyi monodromy の \((2,3,5)\) triple の間に、actual generating maps のレベルの写像を作る。特に
\[
\beta_\gamma:
\mathcal D(w)\longrightarrow\mathcal D(w^{u_\gamma})
\tag{11.5}
\]
が Galois transport と一致することを示す。

Theorem 3.1 の child's drawing は元の \(F_2\)-quotientに対する unframed cofunctorであり、補助的な modular factorization へのこの word-level 移送を自動では与えない。この一段を明記する必要がある。

### FC-4. frame を保つ torsor 同定

(9.1) の order-\(5\) branch 上の tangential lifts を \(\mathcal T_B\) とする。次の図を \(G_{\mathbf Q}\)-equivariant にする全単射を構成する。
\[
\iota:\mathcal T_B(\overline{\mathbf Q})
\xrightarrow{\sim}\mathcal D(w),
\qquad
\iota(\zeta _5^j\lambda)
=
(w^jq_0w^{-j},w^jr_0w^{-j}).
\tag{11.6}
\]

\(\gamma\) が \(w\) を \(w^{u_\gamma}\) へ送るときは、右辺を対応する fiber \(\mathcal D(w^{u_\gamma})\) へ transport した family 版で書く。\(G_{\mathbf Q(\zeta _5)}\) へ制限すれば一つの fiber 上の \(C_5\)-作用になる。

### FC-5. Kummer class の一致

affine 座標で
\[
\beta_\gamma:a\longmapsto
\chi _5(\gamma)a+b_\gamma
\]
とし、(11.6) から
\[
[b_A]=
\left[-\frac{16}{27}\right]^e
\quad\text{in}\quad
H^1(G_{\mathbf Q},\mu _5),
\qquad e\in\mathbf F_5^\times
\tag{11.7}
\]
を導く。

### FC-6. 結論

FC-0–FC-5 が成立すれば
\[
v_2(-16/27)=4\not\equiv0\pmod5
\]
より \([b_A]\ne0\)。F1 から
\[
\boxed{
G_{\mathbf Q}\twoheadrightarrow
\operatorname{GTSh}(N_A,N_A)\cong F_{20}
}
\tag{11.8}
\]
が従う。

重要なのは、FC-0–FC-5 に **「五つの frame が Galois 推移的」という仮定を入れないこと**である。それを仮定すれば結論を仮定した循環になる。比較は形式的 equivariance、非自明性は (9.3) の独立算術計算、と分離する。

---

## F12. 既存比較結果で足りる部分・足りない部分

既存資料から既に得られるものは次である。

1. Ihara action の cyclotomic power \(u=2m+1\)。
2. (7.1) の actual homomorphism formula。
3. isomorphism class \([\psi]\) 上での \(G_{\mathbf Q}\)、\(\widehat{GT}\)、GT-shadow の cofunctor compatibility。
4. \(\Phi:\operatorname{GTSh}(N_A)\cong N_{S_5}(\langle X\rangle)\)。
5. outer quotientが Legendre 記号と一致すること。

不足はちょうど次の三点である。

\[
\begin{array}{ll}
\textbf{(I)}&
[\psi]\text{ へ割る前の rooted/tangential fiber 上の compatibility},\\[2mm]
\textbf{(II)}&
\text{元の }(X,Y)\text{ marking から補助 }(q,r,v)
\text{ への exact word-level transport},\\[2mm]
\textbf{(III)}&
\text{Belyi model (9.1) の局所 Kummer classと }
\Phi\circ\operatorname{Ih}_{N_A}\text{ の translation class の一致}.
\end{array}
\tag{12.1}
\]

(I) を outer action だけで代用すると \(\mathbf Q(\sqrt5)\) まで、(II) を conjugacy class だけで代用すると一つの rigid orbitまで、(III) を torsor の位数一致だけで代用すると「5=5」までしか進まない。いずれも \(C_5\) の非自明な算術像を証明しない。

---

## F13. 攻略計画

### Phase A — 紙上比較を先に閉じる

1. (9.1) に branch-cycle labeling を付け、明示 \((q_0,r_0,w)\in A_5^3\) と一致させる。
2. unrooted dessin の集合でなく、actual monodromy map と tangential lift を object とする小さな groupoid \(\mathrm{Dessin}^{\mathrm{fr}}_{A_5}\) を定義する。
3. (7.1) を brackets の前でこの groupoid へ持ち上げ、representative independence と反変合成則を証明する。
4. shadow hexagon の factorization map を word-level で書き、FC-3–FC-4 の正方形を可換にする。

### Phase B — 算術 class を固定する

1. 標準 basepoint と無限遠 local parameter の規約を固定する。
2. (9.2) から class \([-16/27]^e\) を導く。
3. source coordinate の affine change が fifth power、frame の cyclic relabeling が \(e\in\mathbf F_5^\times\) だけを変えることを証明する。
4. \(v_2=4\) から Kummer class の非自明性を証明する。

### Phase C — 証明書化

最小証明書は次を含めればよい。

- Belyi map の二因数分解 (9.1)。
- passport と Riemann–Hurwitz。
- 一組の branch cycles と \(A_5\) 生成性。
- \(N_A\) の \((X,Y)\) marking との対応表。
- tangential local expansion (9.2)。
- affine action \((u,b)\) と五 frame の対応表。
- \(v_2(-16/27)=4\)。
- FC の可換図における右作用／左作用の convention。

その後に限り、独立 checker で branch cycles、局所展開、degree \(20\) Galois group を照合する。これは cross-check であって Lean verification ではない。

補助的な一発 witness としては、good prime
\[
\ell\equiv1\pmod5
\]
で framed resolvent の Frobenius が 5-cycle になることを示してもよい。このとき円分線形部は 1 なので、その Frobenius は非自明な pure translation であり、ただ一つで \(C_5\) 全体を生成する。ただし ordinary dessin database の factorization pattern では inner frame が消えているため、必ず framed resolvent を用いる。

---

## F14. 最終裁定

1. **古典的 rational rigidity だけで解く案は不可。**  
   \(5A/5B\) の二成分と \(\mathbf Q(\sqrt5)\) は C4 の二次商を説明するが、inner \(C_5\) を説明しない。

2. **「五つの ordinary dessin の moduli field」を計算する案は明確に誤り。**  
   五つは simultaneous \(C_5\)-conjugacyで一つの dessin 同型類になる。この quotient obstruction は Guillot の \(GT_1(A_5)=1\) とも一致する。

3. **framed rigidity / tangential Kummer 路線は具体的に実行可能。**  
   degree \(5\), genus \(0\) の \(\mathbf Q\)-model (9.1) と、非自明候補 \(-16/27\) まで紙上で出る。未知の数体を闇雲に探索する段階ではない。

4. **それでも現時点の全体判定は (c)。**  
   FC\((A_5)\) の actual-inner-level comparison が未証明であり、ここを飛ばして \(-16/27\) を Ihara class と同一視すれば、便 10 で警告した action mismatch を再発させる。

★ 研究上の最善手は、rigidity 文献をさらに広く探すことではなく、**(9.1) の tangential fiber と \(\Phi\circ\operatorname{Ih}_{N_A}\) を結ぶ FC\((A_5)\) を一枚の命題として証明すること**である。成功すれば valuation 一行で全射、失敗すれば「どの twist が差として残るか」が新しい正確な障害になる。

---

## ★ 教材

1. fixed-\(v\) centralizer torsor と inner Nielsen class は同じではない。前者は後者へ割る前の fiber である。
2. field of rationality \(\mathbf Q(\sqrt5)\) は \(5A/5B\) を分けるが、inner translation \(C_5\) は分けない。
3. rigid な三点 cover の Hurwitz space は零次元であり、moduli 曲線の genus を探すべきではない。
4. unrooted dessin の field of moduli が \(\mathbf Q\) でも、root/tangential fiber の点体は非 Galois degree \(5\)、正規閉包は \(F_{20}\) になり得る。
5. 二つの \(C_5\)-torsor は、幾何的には同型でも算術的には異なる Kummer twist であり得る。位数一致は比較補題の代用にならない。
6. 本件では明示 Belyi map の leading coefficient が算術候補を与える。残る難所は数体計算でなく、marking と Galois action の exact comparison である。

---

## 監査範囲外の申告

- ブラインド規律に従い、turn 冒頭で `docs/対話帳.md` を読んだが、A\(_5\) 関連の追記は一切していない。本返信にのみ記した。
- Sol の役割規律に従い、GAP、node、Python、Lean は実行していない。F3、F5、F9 は character formula と多項式因数分解による紙計算である。
- Guillot 論文は PDF の pp. 3, 17–18, 21–22、child's drawings 論文は PDF の Theorem 3.1 所在頁をページ画像で照合した。テキスト抽出だけで数式を裁定していない。
- \(GTSh(N_A)\cong F_{20}\)、20/20 settled、\(\Phi\)、Legendre quotient は本便の前提となった cross-checked 結果を採用し、探索・合成表を再実行していない。
- (9.1) の Belyi map と fixed-\(v\) shadow fiber の \(G_{\mathbf Q}\)-equivariant 同定は未証明である。従って \(\operatorname{Ih}_{N_A}\) の全射性、\(a_A=-16/27\) はまだ主張しない。
- regular \((5,5,5)\) genus-\(13\) curve の明示方程式、field of definition の descent obstruction、全 local monodromy path は計算していない。
- 外部一次資料として Daire–Kato–Uchino の構成を abstract/本文概要の射程で参照したが、本 \(A_5\) torsor への適用はしていない。
- `verified` は Lean に予約する。本返信の rigidity 計算と Belyi 候補は paper audit / candidate である。
- 主な監査対象の SHA-256:
  - `sol/sol_task_15_a5_arith.txt`: `4156BA2304BF82FD5AE05A0EEECCB15432A4A7C35CC04B9AC43B35B062935013`
  - `sol/裁定_14_e22.md`: `6E6C86EAB50CA2254157A4512241FC35BAE65066F12D33C7A89DCB7C66F99481`
  - `docs/研究目的.md`: `E03193DD3DA7BF7D75E9887834E8200A826633D78392587761A9764D1F68104F`
  - `docs/文献配達_04_rigidity.md`: `148A625E61FDB1C87C3414CACFD86F52F18C4BC806E218ECF673A5BC988A9306`
  - `docs/week3-比較写像_guillot_v2.md`: `0ECEB7D5EA8C80863B0B4EAAB2C1AC0D1150152C5D0B3D5965276EBA48656B1E`
  - `sol/sol_reply_10_caseB.md`: `648A3D87087EE2140D0699F1E8FD03D7C6D11E768E37F08CF409FD1439A73F63`
  - `docs/week3-20の正体_opus_v1.md`: `FB4A3399A55277C8D88C95054418BF39D5DA2642C2C1436DB3CE4E95940DE9A0`
  - `papers/delivered/guillot_1407.3112.pdf`: `416C0A91EF7BBB2EB7B8E615D8D209083232965F1151C3E2832256110806784B`
  - `papers/2106.06645-gt-shadows-childs-drawings.pdf`: `BE6AFB208B09D79716119FCB479BF74175A1C0ADE1FA47D6C9727B01AA2D8F52`
- 今便で作成・編集したのは `sol/sol_reply_15_a5.md` だけである。
- 最終 `git status` では並走セッション由来と思われる `ops/codex_activity_sol2.log` と `sol/sol2_reply_01_q.md` の変更も見えたが、私は前者を状態確認で読んだ以外、いずれも編集・復元していない。

---

## 考察と提案

P156【rigidity 採用】\((5A,5A,5A)\)、\((5B,5B,5B)\) は各々一つの generating inner rigid orbit、\((2A,3A,5A)\)、\((2A,3A,5B)\) も各々一つの generating inner rigid orbitとして paper audit / candidate に登録する。

W120【ordinary quotient 停止】fixed-\(v\) の五分解を「五つの dessin 同型類」または「degree-\(5\) moduli orbit」と呼ばない。simultaneous \(C_5\)-conjugacyで一つに潰れることを全 dessin 路線の入口に明記する。

P157【三つの体の分離】exact generator の \(\mathbf Q(\zeta _5)\)、inner class の \(\mathbf Q(\sqrt5)\)、absolute dessin の \(\mathbf Q\) を別欄で管理する。Legendre quotient は \(C_5\) 算術の証明に流用しない。

P158【framed moduli】五分解を \(\mathbf Q\) 上の \(\mu _5\)-torsor、\(\mathbf Q(\zeta _5)\) 上の constant \(C_5\)-torsor として定式化する。point field \(E\)、Galois closure \(L\)、unframed field を証明書 schema で分離する。

P159【明示 Belyi 候補】(9.1) と local class \([-16/27]\) を FC\((A_5)\) の算術側候補として採用する。passport、monodromy、basepoint、leading coefficient を一体の証明書にする。

W121【radicand の状態札】FC\((A_5)\) 完了前は \(a_A=-16/27\)、\(\operatorname{im}\operatorname{Ih}_{N_A}=F_{20}\) と書かない。許される表記は `candidate via tangential Belyi fiber / comparison UNKNOWN`。

P160【最優先補題】F11 の FC-0–FC-6 を次の主命題とする。とくに Aut\((A_5)\) 内の actual equality、modular factorization への word-level transport、frame torsor の equivariance を別々の小補題に分ける。

W122【inner lift 必須】Out\((A_5)\) 上の可換図、unrooted child's drawing の cofunctor、二つの torsor の幾何同型のいずれも FC の代用として受理しない。

P161【全射の最短証明】FC が \([b_A]=[-16/27]^e\)、\(e\ne0\) を返した時点で、\(v_2=4\) と F1 の像の二択から全射を閉じる。追加の大規模 moduli 探索を要求しない。

W123【規約凍結】右作用／左作用、\(qrv=1\) かその逆か、標準 tangential vector、\(w=X^3\) の向き、cofunctor の逆元を FC-0 で凍結する。規約差が非零冪なのか別 twist なのかを区別する。

W124【最終状態】本路線は `ordinary rigidity: BLOCKED`, `framed/Kummer refinement: GO for proof design`, `A5 arithmetic surjectivity: UNKNOWN` と記録する。
