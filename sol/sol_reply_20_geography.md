# 最初の層の指名: **level 16 双子セル**

最初に撃つべき対象は、単独の窓ではなく
\[
\boxed{
 \mathcal C_{16}:=\pi^{-1}\bar\Gamma(16)
 \quad\text{対}\quad
 K^{(8)}
}
\]
の二窓比較である。ここで
\(\pi:B_3\to PSL_2(\mathbb Z)\) は中心商である。
両者は

- \(c=1\),
- exact geometric level \(16\),
- \(|P|=|\Gamma(2)/N|=256\),
- passport \((8,8,8)\),
- \([PSL_2(\mathbb Z):N]=1536\)

まで一致する。一方、
\(\mathcal C_{16}\) は主合同窓であり、
\(K^{(8)}\) は非合同であることを F8 で紙上証明する。
しかも \(K^{(8)}\) の算術飽和は 2405.11725 Thm 5.3 で既知だが、
\(\mathcal C_{16}\) の算術像は未決である。

従ってこの一対は、

1. 商の位数・passport・level だけでは窓を分類できないこと、
2. 合同性と算術飽和を同一視できないこと、
3. 統一 normalizer 則が marking の差を本当に読むか、
4. A5 の torsor 法が 2-primary 層へ移植できるか

を同時に検査する最小の強い反証セルである。
較正アンカーは
\[
\mathcal C_8=K^{(4)},\qquad
\mathcal C_{10}=N_A
\]
とする。

## 追加・修正した軸

現行 4 軸は、次の 6 座標と 1 整合条件に組み替えるのがよい。

1. **(A0) 中心・拡大座標（新規）**:
   \(\bar c\) の位数、中心消去商、中心拡大類。
2. **(A1) 完全 marked quotient 座標（A の修正）**:
   \(Q_N=PB_3/N\) と \((\bar x,\bar y,\bar c)\)、
   および \(B_3/PB_3\cong S_3\) の輸送作用。
3. **(B′) modular geography（B の強化）**:
   exact level、合同閉包、非合同 defect、素数冪局所像。
4. **(C′) deformation/extension 座標（C の強化）**:
   graded module だけでなく、交換子 pairing・\(H^2\) の拡大類・
   実際の obstruction map。
5. **(E) poset incidence 座標（新規）**:
   refinement、intersection/join、reduction image、gluing defect。
6. **(F) arithmetic descent 座標（新規）**:
   arithmetic orbit、安定窓での stabilizer image、
   定義体・moduli 体、rigidification torsor の \(H^1\)-類。
7. **(D′) GTSh-equivariance（D の格下げ・精密化）**:
   独立の数値軸ではなく、上記全座標が満たすべき
   **GTSh 群oid上の関手性**。

特に、一般の \(N\in NFI_{PB_3}(B_3)\) では \(c\notin N\) があり得る。
従って regular dessin の辞書だけを最上位軸に置く現行 (A)(B) は
全宇宙を覆っていない。

## 追加・修正した圧縮法則

- **G0（正確な orbit count）**:
  admissible generating triples の個数を \(|\operatorname{Aut}P|\) で割る。
  passport の Frobenius 計数だけでは generation と
  \(B_3\)-normality を数えていない。
- **G1′（normalizer 則）**:
  位数等式でなく、canonical map
  \(\Phi_N:GT(N)\to N_{\operatorname{Aut}(Q_N)}
  (\langle w_N\rangle)\) の核と余核を別々に事前登録する。
- **G2′（settled 率）**:
  \(2/\varphi(e)\) を一般則にせず、
  cyclotomic unit 群の Nielsen class stabilizer の比として述べる。
- **G3′（E23 型）**:
  各中央層の \(M^\sigma\) と
  \(\widehat H^0(\langle\theta\rangle,M)\) が零なら障害写像が零、
  という条件付き層帰納にする。
- **G4′（A5 テンプレ）**:
  scalar \(u\) でなく rigidification torsor の
  \([b]\in H^1(G_{\mathbb Q},M)\) を基本量にする。
  Kummer 数は \(M\cong\mu_p\) の一次元特例。
- **G5（CRT/gluing 則・新規）**:
  coprime な二窓の intersection に対する
  \(GT\to GT\times GT\) の像を fiber product と比較し、
  gluing index を記録する。

以下、根拠を順に述べる。

---

## F1. 現行 (A) は、狭い意味では完全、広い意味では不足

\(c\in N\) と仮定し
\[
\bar N\triangleleft\Gamma(2)\cong F_2,\qquad
P=\Gamma(2)/\bar N
\]
とする。このとき、全射
\[
F_2\twoheadrightarrow P,\qquad x\mapsto X,\quad y\mapsto Y
\]
の \(\operatorname{Aut}(P)\)-軌道は kernel を一意に決める。
実際、二つの全射が同じ kernel をもつことと、
商 \(P\) の自己同型によって移り合うことは同値である。
従って
\[
\bigl(P,\operatorname{Aut}(P)\cdot(X,Y)\bigr)
\tag{1.1}
\]
は既に完全不変量であり、
\[
(\operatorname{ord}X,\operatorname{ord}Y,
 \operatorname{ord}(XY)^{-1})
\]
という passport は (1.1) から導かれる粗い索引である。

これは現行 (A) の二重性を示す。

- 「実際の generating triple の Aut 軌道」まで持てば完全だが、
  その列挙自体が atlas の本作業である。
- passport まで粗くすると、同じセルに多数の kernel が入り、
  分類力は大きく落ちる。

さらに \(N\triangleleft B_3\) であるためには、
単に \(X,Y,Z\) が \(P\) を生成するだけでは足りない。
\(B_3/PB_3\cong S_3\) が与える Nielsen 変換が
商 \(P\) の自己同型として降りる、という
**\(B_3\)-admissibility** を課す必要がある。

従って正確な個数公式は
\[
\#\{\text{windows with quotient }P\}
=
\frac{
 \#\{\text{\(B_3\)-admissible generating triples of the given type}\}
}{
 |\operatorname{Aut}(P)|
}.
\tag{1.2}
\]
Aut 作用は generating pair を点ごとに固定する自己同型が恒等写像なので
自由である。Frobenius の指標公式は分子の「積が 1」の部分を数えるが、
generation と \(B_3\)-admissibility は別途差し引く必要がある。

---

## F2. 欠けている第一軸は中心拡大である

一般の窓では \(c\) が生きる。まず
\[
Q_N:=PB_3/N,\qquad
C_N:=\langle\bar c\rangle,\qquad
P_N:=Q_N/C_N
\]
を置くべきである。すると
\[
1\longrightarrow C_N
\longrightarrow Q_N
\longrightarrow P_N
\longrightarrow1
\tag{2.1}
\]
は cyclic central extension である。

完全な identity coordinate は
\[
\mathfrak M(N)=
\bigl(Q_N;\bar x,\bar y,\bar c;
       \text{\(S_3\)-transport}\bigr)/
\operatorname{Aut}(Q_N).
\tag{2.2}
\]
圧縮座標としては少なくとも

- \(e_c=\operatorname{ord}(\bar c)\),
- 中心消去商 \(P_N\),
- (2.1) の拡大類、
- \([\bar x,\bar y]\) と \(\bar c\) の gluing、
- \(\theta,\tau\) が \(C_N\) に及ぼす作用

を記録する。

\(c\notin N\) なら \(N\) 自身は
\(PSL_2(\mathbb Z)\) の部分群ではない。
modular geography を付けられるのは
\[
N^{\mathrm{mod}}
:=
N\langle c\rangle/\langle c\rangle
\le PSL_2(\mathbb Z)
\tag{2.3}
\]
だけである。(2.3) と中心データを併記して初めて元の窓へ戻れる。

従って M5 型の \(c\ne1\) 窓を含む全 NFI atlas では、
(A0) は任意でなく必須である。

---

## F3. (B) は二値でなく「level・closure・local image」に分解する

\(c\in N\) とし、対応する正規部分群を
\[
H\triangleleft PSL_2(\mathbb Z),\qquad H\le\bar\Gamma(2)
\]
とする。記録すべき量は次である。

1. **geometric level**
   \[
   \ell(H):=\operatorname{ord}_{PSL_2(\mathbb Z)/H}(T).
   \tag{3.1}
   \]
   正規部分群なので全 cusp width は同じ \(\ell(H)\)。
2. **congruence closure**
   \[
   H^{\mathrm{cong}}
   :=
   \bigcap_{\substack{C\supseteq H\\C\text{ congruence}}}C.
   \tag{3.2}
   \]
3. **congruence defect**
   \[
   d_{\mathrm{cong}}(H):=[H^{\mathrm{cong}}:H].
   \tag{3.3}
   \]
4. 各 \(p^a\mid\ell(H)\) における局所像と、
   CRT の中央符号を含む gluing data。

合同／非合同は (3.3) が \(1\) か否かという末端の一ビットにすぎない。
非合同窓同士でも closure と defect は大きく異なり得る。

また、level だけで「層別悉皆」にはならない。
\((2,3,\ell)\) triangle group は \(\ell\ge7\) で多数の有限商をもち、
固定 level でも quotient order は無制限になり得る。
従って atlas の有限な宇宙は
\[
(e_c,\ell,|P|)\quad\text{の同時 bound}
\tag{3.4}
\]
で事前登録し、その内部を passport と Aut 軌道で分けるべきである。

---

## F4. (C) は表現だけでなく extension class まで必要

E23 で使った

- \(\det(1-\sigma|_M)\),
- \(M^\sigma\),
- \(M^\theta/(1+\theta)M\),
- induced lattice 性

は非常に良い層不変量である。ただし、これらは
「一つの窓の静的分類軸」ではなく、選んだ tower
\[
N_{r+1}\le N_r
\]
の kernel
\[
M_r=\ker(Q_{N_{r+1}}\to Q_{N_r})
\]
に付く deformation data である。

同じ graded \(S_3\)-module をもつ二つの拡大でも、

- \(H^2(Q_{N_r},M_r)\) の extension class,
- commutator pairing
  \(\beta:\bar Q\wedge\bar Q\to M_r\),
- section cocycle,
- 実際の obstruction map

が異なれば shadow の持上げは異なる。

従って (C′) の一層分は
\[
\mathfrak D_r=
\bigl(
 M_r,\sigma,\theta,\tau;
 [\xi_r]\in H^2;
 \beta_r;
 \omega_r
\bigr)
\tag{4.1}
\]
とするのが安全である。
E23 の \((G2)(G3)\) は (4.1) の一部を零化して
\(\omega_r\equiv0\) を導く定理であって、
module character だけから一般に \(\omega_r\) を復元できるわけではない。

---

## F5. 新規 (E): poset incidence は genuine/fake 判定の load-bearing 軸

窓 \(N\) 単体の不変量をどれだけ精密にしても、
genuine/fake の定義が要求する
\[
R_{K,N}:GT(K)\longrightarrow GT(N),
\qquad K\le N
\tag{5.1}
\]
の像は読めない。

従って各 vertex に加えて、各 refinement edge に

- quotient map \(Q_K\twoheadrightarrow Q_N\),
- \(\operatorname{im}R_{K,N}\),
- fiber cardinality と torsor 構造、
- 二方向 refinement の fiber-product image,
- intersection \(K_1\cap K_2\) における gluing index

を置く必要がある。

特に
\[
GT(K_1\cap K_2)
\longrightarrow
GT(K_1)\times_{GT(N)}GT(K_2)
\tag{5.2}
\]
の余核は、個々の一辺が全射でも残り得る二方向 obstruction を測る。
これは Week 3 の \(J=L\cap M_5\) で既に較正された構図である。

従って「窓の地理学」の基本対象は点の表でなく、
**vertex labels と edge labels をもつ有限部分 poset** でなければならない。

---

## F6. 新規 (F): 幾何型と算術型を分離する

同じ \(\overline{\mathbb Q}\)-dessin 型でも、
Galois descent と rigidification torsor は別データである。
一般の窓では、まず arithmetic groupoid orbit
\[
\mathcal O_{\mathrm{arith}}(N)
\tag{6.1}
\]
と stabilizer を記録する。
\(N\) が \(G_{\mathbb Q}\)-安定な場合（特に isolated の場合）に限り、
\[
A_N:=\operatorname{im}
\bigl(G_{\mathbb Q}\to GT(N)\bigr)
\tag{6.2}
\]
を群として書ける。その計算に使う有限 \(P_N\)-集合 \(\Lambda\) ごとの
\[
[b_{N,\Lambda}]
\in H^1(G_{\mathbb Q},M_\Lambda)
\tag{6.3}
\]
は、対応する cover と rigidification が
\(G_{\mathbb Q}\)-stable に降下した後で置く。

A5 では \(M_\Lambda\cong\mathbb F_5\) が一次元で、
(6.3) が Kummer 類 \([2]\) に落ちた。
一般には

- torsor が cyclic でない、
- affine module が高次元、
- deck automorphism が非自明、
- moduli 体と定義体が異なる

ことがあるため、一つの数 \(u\) へ押し込めてはならない。

従って現行法則 4 は

> 「\(u\) を族上の関数にする」

ではなく

> 「rigidification torsor の cohomology class
> \([b]\) を族上で自然にする。
> cyclic 一次元セルでのみ Kummer representative \(u\) を選ぶ」

へ修正する。

---

## F7. (D) の正確な定式化 — invariant でなく群oid関手

GTSh は、一つの群が全窓へ作用するというより、
窓を objects、shadows を arrows とする groupoid として扱うのが正確である。
shadow
\[
\alpha=[m,f]:K\longrightarrow N
\]
は marked quotient の同型
\[
T_\alpha:Q_K\xrightarrow{\sim}Q_N
\tag{7.1}
\]
を誘導する。

従って「GTSh 作用で保たれる不変量」は、次の形で定義すべきである。

> **定義候補（equivariant classification functor）.**
> 構造の圏 \(\mathsf{Str}\) への関手
> \[
> \mathcal I:\mathsf{GTSh}\longrightarrow\mathsf{Str}
> \tag{7.2}
> \]
> であって、
> \(\mathcal I(N)\) は (A0)–(F) の chosen data、
> \(\mathcal I(\alpha)\) は (7.1) が誘導する transport とする。
> 恒等 shadow には恒等写像、合成には写像の合成を割り当てる。

数値量 \(i(N)\) が invariant であるとは、
各 arrow \(K\to N\) に対して
\[
i(K)=i(N)
\tag{7.3}
\]
であること、module や torsor のような共変量では
literal equality でなく指定された transport isomorphism があることをいう。

さらに refinement \(K\le N\) を含む atlas では、
quotient map と shadow transport の正方形が可換であることを要求する。
すなわち \(\mathcal I\) は vertex だけでなく arrow category 上で自然である。

**isolated の正確な読み**は
\[
\pi_0(\mathsf{GTSh})\text{ における }N\text{ の連結成分が }\{N\}
\tag{7.4}
\]
である。「固定点」は (7.4) の略記としてのみ使うべきで、
一つの粗い数値 invariant が同じ値を保つことから isolated は従わない。

事前登録宇宙 \(\mathcal U\) 上で
\[
\{M\in\mathcal U:\mathcal I(M)\cong\mathcal I(N)\}=\{N\}
\tag{7.5}
\]
まで示せれば、equivariance から \(N\) の \(\mathcal U\)-内 isolated 性が従う。
逆に isolated でも、別成分の窓が同じ粗い invariant をもつことはあり得る。

軸間の依存関係をまとめると、

\[
\begin{array}{c}
\text{(A0)+(A1): identity data}\\
\downarrow\\
\text{passport, genus, deck automorphism}
\end{array}
\qquad
\begin{array}{c}
\text{(A0) で中心消去}\\
\downarrow\\
\text{(B′): modular data}
\end{array}
\tag{7.6}
\]
であり、(C′) は (E) で tower/edge を選んだ後に初めて定義される。
(F) は幾何的 identity data だけから形式的には決まらない arithmetic data、
(D′) はこれら全てに課す自然性条件である。

---

## F8. \(K^{(n)}\) の合同性 — **\(K^{(4)}\) だけが合同**

以下は本便で新しく得た紙上命題である。
証明を全て書くが、二人目の独立監査前なので状態札は
**single-system paper candidate** とする。

> **命題 K-cong.**
> \(n\ge3\) とする。中心商で
> \(K^{(n)}\) に対応する部分群を
> \(\bar K_n\triangleleft PSL_2(\mathbb Z)\) と書く。
> このとき
> \[
> \boxed{
> \bar K_n\text{ が合同部分群}
> \iff n=4,
> \qquad
> \bar K_4=\bar\Gamma(8).
> }
> \tag{8.1}
> \]

### 8.1 exact level

標準写像を
\[
\sigma_1\longmapsto
T=\begin{pmatrix}1&1\\0&1\end{pmatrix},
\qquad
\sigma_2\longmapsto
U=\begin{pmatrix}1&0\\-1&1\end{pmatrix}
\tag{8.2}
\]
と取る。すると
\[
x=x_{12}\longmapsto X=T^2,\qquad
y=x_{23}\longmapsto Y=U^2.
\]
\(G_n=\Gamma(2)/\bar K_n\) における \(x\) の位数は
\[
e_n=\operatorname{lcm}(n,2).
\]
\(T\) の像は \(PSL_2(\mathbb F_2)\cong S_3\) で transposition だから
偶数位数をもち、その二乗の位数が \(e_n\) である。従って
\[
\ell_n=\operatorname{ord}(T)=2e_n
=
\begin{cases}
4n,&n\text{ odd},\\
2n,&n\text{ even}.
\end{cases}
\tag{8.3}
\]
これが \(\bar K_n\) の geometric level である。

### 8.2 odd prime を含む \(n\) は指数だけで非合同

既知の位数公式から
\[
[PSL_2(\mathbb Z):\bar K_n]
=6|G_n|
=
\begin{cases}
24n^3,&n\text{ odd},\\
3n^3,&n\text{ even}.
\end{cases}
\tag{8.4}
\]
一方、\(L\ge3\) では
\[
|PSL_2(\mathbb Z/L)|
=\frac{L^3}{2}\prod_{p\mid L}(1-p^{-2}).
\tag{8.5}
\]

\(n\) が奇数なら \(L=4n\) なので
\[
|PSL_2(\mathbb Z/4n)|
=24n^3\prod_{p\mid n}(1-p^{-2})
<24n^3.
\tag{8.6}
\]
\(n\) が偶数で odd prime divisor をもつなら \(L=2n\) なので
\[
|PSL_2(\mathbb Z/2n)|
=3n^3\prod_{\substack{p\mid n\\p\text{ odd}}}(1-p^{-2})
<3n^3.
\tag{8.7}
\]

Wohlfahrt の level 定理により、level \(L\) の合同部分群なら
\(\bar\Gamma(L)\) を含む。従ってその指数は
\(|PSL_2(\mathbb Z/L)|\) 以下でなければならない。
(8.6)(8.7) はこれに反する。

よって odd prime を含む全 \(n\) は非合同である。
特に doubling
\(K^{(q)}=K^{(2q)}\)（\(q\) odd）とも整合する。

### 8.3 \(n=2^\alpha\) では指数が同じになる

\(n=2^\alpha\) なら積の odd-prime 因子がなく、
\[
[PSL_2(\mathbb Z):\bar K_n]
=|PSL_2(\mathbb Z/2n)|.
\tag{8.8}
\]
従って、もし \(\bar K_n\) が合同なら
\[
\bar K_n=\bar\Gamma(2n)
\tag{8.9}
\]
でなければならない。

### 8.4 \(n\ge8\) を一語で分離する word

\(G_n\le D_n^3\) の標準生成元は
\[
x=(r,s,s),\qquad y=(rs,r,rs).
\]
従って
\[
y^2=(1,r^2,1),\qquad
x^{-1}y^2x=(1,r^{-2},1)=y^{-2}.
\]
ゆえに
\[
w:=x^{-1}y^2xy^2\in\bar K_n
\qquad(\text{全 }n).
\tag{8.10}
\]

ところが (8.2) の行列では
\[
X=\begin{pmatrix}1&2\\0&1\end{pmatrix},
\qquad
Y=\begin{pmatrix}1&0\\-2&1\end{pmatrix}
\]
なので、直接乗算により
\[
X^{-1}Y^2XY^2
=
\begin{pmatrix}
-55&16\\
24&-7
\end{pmatrix}.
\tag{8.11}
\]
\(w-I\) の四成分の最大公約数は \(8\)、
\(w+I\) の四成分の最大公約数は \(2\) である。
従って
\[
w\notin\bar\Gamma(2n)\qquad(2n\ge16).
\tag{8.12}
\]
(8.9) と矛盾するので、全 \(n=2^\alpha\ge8\) は非合同である。

### 8.5 \(n=4\) は \(\bar\Gamma(8)\)

\[
H:=\bar\Gamma(2)/\bar\Gamma(8),\qquad
J:=\bar\Gamma(4)/\bar\Gamma(8)
\]
と置く。mod \(8\) の一次近似から
\[
J\cong\mathfrak{sl}_2(\mathbb F_2)\cong C_2^3,
\qquad
H/J\cong C_2^2.
\tag{8.13}
\]
さらに \([\bar\Gamma(2),\bar\Gamma(4)]
\subseteq\bar\Gamma(8)\) なので \(J\) は中心である。

\(Z=(XY)^{-1}\) とすると
\[
\frac{X^2-I}{4}=E_{12},\qquad
\frac{Y^2-I}{4}=-E_{21},\qquad
\frac{Z^2-I}{4}
=
\begin{pmatrix}-1&1\\-1&1\end{pmatrix}.
\tag{8.14}
\]
これらは \(\mathfrak{sl}_2(\mathbb F_2)\) の基底をなす。
従って \(X^2,Y^2,Z^2\) は中心 involution 三つを独立に生成し、
\(|H|=8\cdot4=32\)。

一方 \(G_4\) でも
\[
\langle x^2,y^2,z^2\rangle
=\langle r^2\rangle^3\cong C_2^3
\]
は中心で、商は \(C_2^2\)、\(|G_4|=32\)。
「\(x^2,y^2,z^2\) が中心 involution」という presentation は
各語を
\[
(x^2)^a(y^2)^b(z^2)^c x^\epsilon y^\delta
\]
へ直すので位数高々 \(32\) であり、\(G_4\) と \(H\) は双方その
32 個を実現する。従って marked quotient は同型で、
\[
\bar K_4=\bar\Gamma(8).
\tag{8.15}
\]

(8.6)–(8.15) で (8.1) が従う。

---

## F9. T-6 検分 — 群論部分 PASS、算術モデルの語に限定を付す

### 9.1 「強近似」は初等行列二つで置き換えられる

\(\bar\Gamma(2)\) の標準放物生成元を
\[
X=
\begin{pmatrix}1&2\\0&1\end{pmatrix},
\qquad
Y=
\begin{pmatrix}1&0\\-2&1\end{pmatrix}
\]
とする。mod \(5\) で
\[
X^3=E_{12}(1),\qquad
Y^2=E_{21}(1).
\tag{9.1}
\]
二つの elementary matrix は \(SL_2(\mathbb F_5)\) を生成するから
\[
\bar\Gamma(2)\twoheadrightarrow PSL_2(\mathbb F_5)\cong A_5
\tag{9.2}
\]
は全射である。従って full strong approximation を引用する必要はない。

\(X,Y\) は非自明 unipotent なので projective order \(5\)。
\(XY\) は trace \(-2\) で \(-XY\) が非自明 unipotent だから、
\(Z=(XY)^{-1}\) も projective order \(5\) である。
よって (9.2) は \((5,5,5)\) marking を与える。

### 9.2 kernel は \(\bar\Gamma(10)\)

(9.2) の kernel は
\[
\bar\Gamma(2)\cap\bar\Gamma(5)=\bar\Gamma(10).
\tag{9.3}
\]
符号にも問題はない。mod \(2\) では \(-I=I\) なので、
mod \(5\) で \(I\) または \(-I\) となる行列は、
CRT により mod \(10\) でも同じ global sign の \(\pm I\) となる。

### 9.3 「S5 軌道一意 ⇒ kernel 一意」の正確な言明

\[
\operatorname{Sur}_{555}(F_2,A_5)
\]
を、\(X,Y,Z=(XY)^{-1}\) が全て位数 \(5\) である全射の集合とする。
\(\operatorname{Aut}(A_5)=S_5\) は postcomposition で作用する。

二つの全射 \(\varphi_1,\varphi_2\) について
\[
\ker\varphi_1=\ker\varphi_2
\iff
\exists\alpha\in\operatorname{Aut}(A_5):
\varphi_2=\alpha\circ\varphi_1.
\tag{9.4}
\]
従って kernel の集合は
\[
\operatorname{Aut}(A_5)\backslash
\operatorname{Sur}_{555}(F_2,A_5)
\tag{9.5}
\]
そのものである。

W3-3b／A5 v4 の二系統計数は (9.5) が一元集合であることを示している。
(9.2) はその集合の一元を与えるので、実際の \(N_A\) marking と
postcomposition で移り、
\[
\boxed{
\bar N_A=\bar\Gamma(10),\qquad
N_A=\pi^{-1}\bar\Gamma(10).
}
\tag{9.6}
\]
ここで (9.6) はまず離散群
\(F_2\cong\bar\Gamma(2)\) の有限指数 kernel の等式である。
\(\widehat F_2\) を使う A5 v4 の記法では双方の profinite closure を取り、
有限指数性により同じ profinite kernel を得る。
また「S5 軌道」は degree-5 dessin の偶然の relabelling でなく、
まさに \(\operatorname{Aut}(A_5)\)-orbit だから kernel を保つ、
という一文が T-6 の ③ に必要な厳密化である。

### 9.4 指数・CRT・genus

CRT により
\[
PSL_2(\mathbb Z/10)
\cong SL_2(\mathbb F_2)\times PSL_2(\mathbb F_5)
\cong S_3\times A_5.
\tag{9.7}
\]
従って
\[
[PSL_2(\mathbb Z):\bar\Gamma(10)]=360,\qquad
[\bar\Gamma(2):\bar\Gamma(10)]=60.
\]

\(X(10)\to X(2)\) は degree \(60\)、三分岐点の inertia は全て \(5\)。
Riemann–Hurwitz から
\[
2g(X(10))-2
=60(-2)+3\cdot60(1-1/5)=24,
\]
すなわち
\[
g(X(10))=13.
\tag{9.8}
\]
また \(A_4<A_5\) の quotient は degree \(5\) で、
三つの branch cycle は 5-cycle だから
\[
2g(W)-2=5(-2)+3(5-1)=2,
\qquad g(W)=2.
\tag{9.9}
\]
従って複素解析的な Belyi cover として
\[
\boxed{W_{\mathbb C}\cong X(10)_{\mathbb C}/A_4}
\tag{9.10}
\]
は正しい。

### 9.5 必要な限定

「Galois 曲線 \(=X(10)\)」は、まず
**複素曲線／dessin としての同定**と書くべきである。
classical full-level modular curveの標準算術モデルは
level structure と cyclotomic descent の規約を伴う。
A5 v4 の一意な \(\mathbb Q\)-dessin model と、その標準 modular model を
\(\mathbb Q\) 上で literally 同一視するなら、
その descent datum の一致を一段明記する必要がある。

安全な現時点の文言は

> regular dessin の幾何曲線は \(X(10)_{\mathbb C}\)。
> degree-5 quotient の一意な \(\mathbb Q\)-form が A5 v4 の \(W_0\)。

である。

同様に
\[
L=\mathbb Q(\zeta_5,\sqrt[5]{2})
\]
は \(X(10)\) の function field の部分体という意味ではない。
これは接繊維の rigidification に対する
\[
G_{\mathbb Q}\to F_{20}\le\operatorname{Aut}(A_5)
\]
が切り出す number field である。
「\(X(10)\) の数論の断片」は比喩としてはよいが、
本文ではこの意味を添えるべきである。

以上により T-6 は

- (9.6) の群論的同定: **PASS**,
- \(X(10)\), \(X(10)/A_4\) の幾何同定: **PASS**,
- 標準 modular \(\mathbb Q\)-model との literal equality:
  **descent datum の明記を条件とする**

と裁定する。

---

## F10. 最初の層と次の 10 窓

\[
\mathcal C_L:=\pi^{-1}\bar\Gamma(L)
\qquad(L\text{ even},\ L\ge4)
\tag{10.1}
\]
と置く。主合同窓では
\[
|P_L|
=\frac{|PSL_2(\mathbb Z/L)|}{6},
\qquad
\text{passport}=(L/2,L/2,L/2).
\tag{10.2}
\]

最初の実験は F8 の level-16 双子セルとする。
その前後を含む次の law-validation panel は以下の 10 窓がよい。

| 順 | 窓 | level | \(|P|\) | passport | 地理 | 主目的 |
|---:|---|---:|---:|---|---|---|
| 1 | \(\mathcal C_4\) | 4 | 4 | \((2,2,2)\) | congruence | 最小 abelian control |
| 2 | \(\mathcal C_6\) | 6 | 12 | \((3,3,3)\) | congruence、\(P\cong A_4\) | solvable nonabelian control |
| 3 | \(\mathcal C_{12}\) | 12 | 96 | \((6,6,6)\) | congruence | 最初の mixed CRT |
| 4 | \(K^{(3)}=K^{(6)}\) | 12 | 108 | \((6,6,6)\) | noncongruence | 同 level/passport 比較・Conj 5.1 最小 open |
| 5 | \(\mathcal C_{14}\) | 14 | 168 | \((7,7,7)\) | congruence、\(P\cong PSL_2(7)\) | A5 の次の simple prime-level |
| 6 | \(\mathcal C_{16}\) | 16 | 256 | \((8,8,8)\) | congruence | **第一標的** |
| 7 | \(K^{(8)}\) | 16 | 256 | \((8,8,8)\) | noncongruence | **第一標的・既知 saturated control** |
| 8 | \(\mathcal C_{18}\) | 18 | 324 | \((9,9,9)\) | congruence、\(P\cong PSL_2(\mathbb Z/9)\) | odd prime-power 初段 |
| 9 | \(\mathcal C_{20}\) | 20 | 480 | \((10,10,10)\) | congruence | \(2^2\)-\(5\) mixed CRT |
| 10 | \(K^{(5)}=K^{(10)}\) | 20 | 500 | \((10,10,10)\) | noncongruence | level-20 paired contrast |

既知アンカー
\[
\mathcal C_8=K^{(4)},\qquad
\mathcal C_{10}=N_A
\tag{10.3}
\]
は各バッチの先頭で再実行するが、「次の 10 窓」には数えていない。

この順序は \(|P|\) 順そのものではない。
先に同 level/passport の congruence/noncongruence pair を置き、
分類軸の分離力を検査する。
その後
\[
6,10,14\quad(\text{prime-level }PSL_2\text{ 系}),
\qquad
12,20\quad(\text{mixed CRT 系}),
\qquad
16,18\quad(\text{prime-power 系})
\]
を比較できるようにしてある。

---

## F11. 圧縮法則の反証可能な形

### G0. orbit-count law（定理形）

固定した有限群 \(P\) と passport \(\mathbf e\) に対し、
\[
a(P,\mathbf e)
:=
\frac{
\#\operatorname{Gen}^{B_3}_{\mathbf e}(P)
}{
|\operatorname{Aut}(P)|
}
\tag{11.1}
\]
を窓数とする。
ここで分子は product-one、generation、\(B_3\)-admissibility を
全て満たす ordered triple の集合である。
passport の class multiplication coefficient だけを
\(a(P,\mathbf e)\) と呼ばない。

### G1′. marked normalizer law

各 family でまず canonical map
\[
\Phi_N:GT(N)\longrightarrow
N_{\operatorname{Aut}(Q_N)}
(\langle w_N\rangle)
\tag{11.2}
\]
を定義し、
\[
\ker\Phi_N,\qquad
\operatorname{coker}\Phi_N
\tag{11.3}
\]
を別々に測る。

事前登録する法則は

> split-inner 条件、marking rigidity、全 normalizer 元の charming lift、
> kernel-free の四条件が成立する family では \(\Phi_N\) は同型。

である。一つでも非自明な (11.3) が出れば反証。
単なる位数一致は hidden kernel と missing image の相殺を見逃すので不可。

### G2′. stabilizer law for settled rate

cyclotomic exponent 群 \(U_e\) が marking/Nielsen class \(\nu_N\) に作用し、
各 exponent fiber が一様であるときに限り
\[
\frac{\#\mathrm{settled}}{\#GTSh(N,N)}
=
\frac{|\operatorname{Stab}_{U_e}(\nu_N)|}{|U_e|}.
\tag{11.4}
\]
case A は stabilizer \(=U_e\)、
既存 case B は stabilizer \(=\{\pm1\}\) なので
\(2/\varphi(e)\) が出る。
新 family で stabilizer が別部分群なら、率もそれに従って変わる。

### G3′. central-layer vanishing law

中央拡大
\[
1\to M\to\widetilde Q\to Q\to1
\]
の線型解に対し、E23+ の恒等式は defects を
\[
d_N\in M^\sigma,\qquad d_\theta\in M^\theta
\]
へ入れる。従って
\[
M^\sigma=0,\qquad
M^\theta=(1+\theta)M
\tag{11.5}
\]
なら obstruction map は恒等零。
全中央列で (11.5) が成立すれば層帰納で持ち上がる。

反証対象は「(11.5) が破れたら必ず非零障害」ではない。
破れは obstruction の居場所を作るだけなので、
実際の \(\omega\) を別に計算する。

### G4′. torsor-cohomology law

有限 \(P\)-集合 \(\Lambda=P/H\) と rigidification を選び、
その affine translation class
\[
[b_{N,H}]\in H^1(G_{\mathbb Q},M_{N,H})
\tag{11.6}
\]
を基本量にする。
\(M_{N,H}\cong\mathbb F_p(1)\) のときだけ
\[
[b_{N,H}]\leftrightarrow
[u]\in\mathbb Q^\times/(\mathbb Q^\times)^p
\]
と書く。

族化の反証条件は、

- \(H\) の選択が Aut-natural でない、
- deck automorphism により descent が捻れる、
- \(\Phi_N\) が非単射、
- actual Galois action と Ih action が一致しない、
- \(M\) が一次元でない

のいずれかである。これらを通る前に scalar \(u\) を比較しない。

### G5. CRT/gluing law

coprime な局所窓 \(N_1,N_2\) と共通粗窓 \(N\) に対し
\[
GT(N_1\cap N_2)
\longrightarrow
GT(N_1)\times_{GT(N)}GT(N_2)
\tag{11.7}
\]
を作り、
\[
\delta_{\mathrm{glue}}
:=
\left[
GT(N_1)\times_{GT(N)}GT(N_2):
\operatorname{im}(11.7)
\right]
\tag{11.8}
\]
を記録する。

候補法則は

> quotient 側に非自明な common quotient がなく、
> central extension class が独立で、
> charming 条件が因子ごとに分離するとき
> \(\delta_{\mathrm{glue}}=1\)。

である。CRT による有限群の直積分解だけから
\(GT\) の直積を結論しない。
\(\mathcal C_{12},\mathcal C_{20}\) が最初の反証試験になる。

### 棄却する法則

\[
\text{congruence}\iff\text{arithmetically saturated}
\tag{11.9}
\]
という形は事前登録しない。
\(N_A=\mathcal C_{10}\) は congruence かつ saturated、
\(K^{(8)}\) は F8 により noncongruence だが Thm 5.3 により saturated。
従って合同性は arithmetic image の説明変数にはなり得ても、
必要十分条件ではない。

---

## F12. 状態札

| 項目 | 判定 |
|---|---|
| 現行 4 軸 | **大幅修正して採用** |
| 中心拡大軸 (A0) | **必須追加** |
| poset incidence 軸 (E) | **必須追加** |
| arithmetic descent 軸 (F) | **必須追加** |
| (D) | 数値軸から **GTSh-groupoid functoriality** へ変更 |
| 最初の層 | **level 16: \(\mathcal C_{16}\) vs \(K^{(8)}\)** |
| T-6 の \(N_A=\pi^{-1}\bar\Gamma(10)\) | **紙上監査 PASS** |
| \(X(10)\), \(X(10)/A_4\) | **幾何的同定 PASS**。算術モデルの文言は §9.5 の限定つき |
| \(K^{(n)}\) 合同性分類 | **本便新規 paper candidate**: \(n=4\) のみ合同 |
| 機械照合・Lean verified | 本便ではなし |

---

## ★ 教材

1. **完全不変量と役に立つ分類軸は同じではない。**
   marked generating pair の Aut 軌道は kernel を完全に決めるが、
   それを得ること自体が全列挙である。level、module、torsor は
   完全性を捨てて法則を見せる座標である。
2. **dessin は中心を殺した世界だけを見る。**
   \(c\ne1\) の窓を含めるなら、中心拡大類を atlas の入口に置く必要がある。
3. **同じ level・位数・passport でも合同性は違い得る。**
   \(\mathcal C_{16}\) と \(K^{(8)}\) が最小の鮮明な教材である。
4. **「作用で不変」は数値の等号だけではない。**
   module、extension、torsor は GTSh arrow に沿って transport される。
   正しい器は groupoid functor である。
5. **CRT は quotient を分解しても shadow の持上げを自動分解しない。**
   gluing obstruction は edge/fiber-product 上にあり、vertex 表からは見えない。
6. **合同 modular curve と算術飽和は別の方向の情報である。**
   congruence は kernel の地理、saturation は Galois image の大きさを測る。

---

## 考察と提案

P182【schema】`docs/窓の地理学_v2.md` では各 vertex の必須欄を
\[
(Q;\bar x,\bar y,\bar c),\ e_c,\ P,\ passport,\ \ell,\
H^{\rm cong},\ d_{\rm cong},\ \operatorname{Aut},\
\mathcal O_{\rm arith}
\]
とし、\(G_{\mathbb Q}\)-stable な vertex でのみ
\(\operatorname{im}Ih\le GT(N)\) を追加する。
各 edge には quotient map・reduction image・fiber・gluing index を置く。

P183【第一撃】既知アンカー
\(\mathcal C_8=K^{(4)}\) と \(\mathcal C_{10}=N_A\) を通した後、
\(\mathcal C_{16}\) と \(K^{(8)}\) を同一 manifest の blind pair として撃つ。
観測前に normalizer map、settled 率、arithmetic orbit
（安定なら stabilizer image）の予測を別々に封印する。

P184【10 窓】F10 の 10 窓を law-validation panel v1 として事前登録する。
level 12・16・20 は必ず congruence/noncongruence の対で読む。

P185【K-cong】F8 の命題 K-cong を Opus に独立再計算させる。
特に (8.11) の一語 witness と \(n=4\) の
\(\mathfrak{sl}_2(\mathbb F_2)\) presentation を別経路で検査する。

P186【T-6 本文化】T-6 は
\[
N_A=\pi^{-1}\bar\Gamma(10),\quad
X(10)_{\mathbb C},\quad
W_{\mathbb C}=X(10)_{\mathbb C}/A_4
\]
を正式命題化し、\(\mathbb Q\)-model については descent datum を分離する。

P187【D の定義】isolated を「固定点」とだけ書かず、
GTSh connected component が singleton であることを主定義に戻す。
各分類量には arrow transport を一つずつ指定する。

P188【法則札】G1′–G5 は全て、適用 family・前件・falsifier を
manifest に書いてから計算する。既存 7+1 窓との一致だけで
適用 family を無限定に広げない。

W141【中心】\(c\notin N\) の窓を regular dessin と同一視しない。
modular subgroup が見るのは中心消去像 (2.3) だけである。

W142【完全性】\(P+\operatorname{Aut}(P)\)-orbit of marking は
既に完全不変量。passport を別の独立軸と数えない。

W143【群oid】GTSh を一つの大域群作用と略記するとき、
partial arrows と connected-component の情報を落とさない。

W144【level】level bound 単独は有限宇宙を与えない。
必ず quotient order または index bound を併記する。

W145【算術モデル】\(X(10)_{\mathbb C}\) の同定と、
標準 modular \(\mathbb Q\)-model の同定を同じ一行にしない。

W146【体】\(L=\mathbb Q(\zeta_5,\sqrt[5]2)\) を
\(\mathbb Q(X(10))\) の部分体と書かない。
これは rigidified tangent fiber の Galois 表現が切り出す数体である。

W147【合同性】congruence/noncongruence から
genuine/fake または saturated/non-saturated を推論しない。

W148【同じ粗データ】order・level・passport が全部一致しても
marked kernel は一致しない。
\(\mathcal C_{16}\) と \(K^{(8)}\) を恒久回帰標本にする。

---

## 監査範囲外の申告

- GAP、node、Python、Lean は実行していない。
- 全有限群 \(|P|\le B\) の新規悉皆列挙はしていない。
  F10 は紙上で選んだ事前登録候補 panel である。
- \(K^{(n)}\) の合同性命題は本便の新規紙上証明であり、
  helper 非共有の第二系統も文献照合もまだない。
- \(\mathcal C_{16}\) の GT-shadow 全列挙・isolated 性・算術像は
  いずれも未計算で UNKNOWN。
- \(X(10)\) の標準算術モデルと A5 v4 の
  \(\mathbb Q\)-dessin model の descent datum は照合していない。
- A5 v4 の算術飽和定理、裁定 16、定理 E23、裁定 17 は
  確定済み入力として用い、再監査していない。
- 過去返信・正本文書・対話帳は編集していない。
  本便で新規作成した成果物は
  `sol/sol_reply_20_geography.md` のみである。
