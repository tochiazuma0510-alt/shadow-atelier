# 影工房 便 24 返信 — \(K^{(3)}\) 橋 D2 と委嘱 17 の相互監査

## 冒頭判定 — B1–B5

ここで **PASS はテンプレの安全側の前件が成立し、当該の「破れ」が
起きないこと**、FAIL は破れが実在することを表す。
B2・B3 は permutation representation に依存するので、D3 が予定する
**最小忠実推移作用**を正本として判定した。この作用は紙上で一意に
次数 \(12\) と決まり、passport は
\((6^2,6^2,6^2)\)、種数は \(4\) である。

| 条件 | 判定 | \(K^{(3)}\) での根拠 |
|---|---|---|
| **B1** relevant Nielsen/Aut orbit の一意性 | **PASS** | \((6,6,6)\)-生成 triple は \(\operatorname{Aut}(G_3)\)-軌道一つ。最小 core-free 部分群も一軌道。三点 Hurwitz 空間が 0 次元というだけでなく、v3 の意味で一意 |
| **B2** \(\operatorname{Aut}(\text{dessin})=1\) | **FAIL** | 最小次数 \(12\) の作用 \(G_3/U\) では \(\operatorname{Aut}(\text{dessin})=N_{G_3}(U)/U\cong C_3\) |
| **B3** \(\lambda=0\) 上の全分岐 | **PASS** | \(\bar x\) は \(6^2\) 型。各 stabilizer と \(\langle\bar x\rangle\) の交わりは自明 |
| **B4** 関連中心化群が巡回 | **PASS** | charming \(m\) 全てで \(C_{G_3}(\bar\sigma _1^{\,2m+1})=\langle\bar x\rangle\cong C_6\)。非可換 \(H^1\) ルートは発火しない |
| **B5** \(k=N_{\rm ord}\) が素数 | **FAIL** | \(k=6\)。非自明性だけでは足りず、class の位数が正確に \(6\) であることが必要 |

従って D2 の総合判定は

\[
\boxed{\text{B1, B3, B4 は通過、B2 と B5 が破れる。}}
\tag{0.1}
\]

dihedral 橋の新しい難所は、予想された「非巡回中心化群」ではなく、
**残留 \(C_3\)-automorphism による descent と、\(2\)-成分・\(3\)-成分を
同時に最大化する合成数 \(k=6\) の算術**である。

---

## F1. \(G_3\) の紙上構造

D1 の正本 (3.1)(3.6) に従い

\[
\begin{aligned}
X&=(r,s,s),\\
Y&=(rs,r,rs),\\
Z&=(r^2s,r^{-1}s,r)
\end{aligned}
\qquad(r^3=s^2=1,\ srs=r^{-1})
\tag{1.1}
\]

と置く。\(n=3\) では \(r^{-1}=r^2\) であり、

\[
e_1:=X^2=(r^2,1,1),\quad
e_2:=Y^2=(1,r^2,1),\quad
e_3:=Z^2=(1,1,r^2).
\tag{1.2}
\]

従って

\[
R:=\langle e_1,e_2,e_3\rangle
\cong C_3^3,\qquad
G_3/R\cong C_2^2 .
\tag{1.3}
\]

これは D1 の \(|G_3|=4\cdot3^3=108\) および
\([G_3,G_3]=R\) と一致する。商の三つの非零元を
\(h_1=\bar X,h_2=\bar Y,h_3=\bar Z\) とすると、共役作用は

\[
\begin{array}{c|ccc}
 &e_1&e_2&e_3\\ \hline
h_1&+&-&-\\
h_2&-&+&-\\
h_3&-&-&+
\end{array}
\tag{1.4}
\]

である。すなわち

\[
\boxed{
G_3\cong \mathbb F_3^3\rtimes C_2^2,
}
\tag{1.5}
\]

ここで \(\mathbb F_3^3\) は \(C_2^2\) の三つの非自明一次元指標の
直和である。特に固定部分は零で、作用は faithful だから

\[
Z(G_3)=1.
\tag{1.6}
\]

以下の B1–B4 は全てこの一枚の符号表から出る。

---

## F2. B1 — relevant orbit は一つ

三つの位数 \(6\) の元 \(A,B,C\) が \(ABC=1\) を満たすとする。
位数 \(6\) の元は \(R\) へは入らない。商 \(C_2^2\) で
\(\bar A+\bar B+\bar C=0\) だから、三つの像は相異なる三非零元である。
商の自己同型で

\[
\bar A=h_1,\qquad\bar B=h_2,\qquad\bar C=h_3
\tag{2.1}
\]

としてよい。

Hall \(3\)-部分群 \(R\) の補群を一つ固定し、

\[
A=(a,h_1),\qquad B=(b,h_2)
\tag{2.2}
\]

と書く。位数 \(6\) 条件は

\[
a_1\ne0,\qquad b_2\ne0,\qquad
(b_3-a_3)\ne0
\tag{2.3}
\]

である。最後の量は \(C=(AB)^{-1}\) の \(h_3\)-固定線上の成分である。
\(R\) による同時共役で off-diagonal 成分を消し、三本の character line
の独立な scaling \(e_i\mapsto\pm e_i\) で (2.3) の三非零値を
全て \(1\) にできる。さらに \(S_3=\operatorname{Aut}(C_2^2)\) が
三本の character line を同時に置換する。

従って、ordered generating \((6,6,6)\)-triple は
\(\operatorname{Aut}(G_3)\) の一軌道である。しかも (2.3) から
\(A^2,B^2,C^2\) がそれぞれ \(e_1,e_2,e_3\) を生成するため、
位数条件を満たす triple は自動的に \(G_3\) 全体を生成する。

これは単なる「三点なので次元 \(0\)」ではなく、地理学 v3 が B1 に
要求する **Nielsen/Aut orbit の一意性**である。よって B1 は PASS。

---

## F3. 最小 faithful dessin、B2 と B3

### F3.1 最小次数は \(12\)

推移作用 \(G_3/S\) が忠実である条件は \(S\) が core-free であること。
\(U:=S\cap R\)、\(L:=SR/R\le C_2^2\) とする。

- \(L=C_2^2\) なら \(U\) は三 character line の直和なので、
  core-free 性から \(U=0\)、従って \(|S|\le4\)。
- \(|L|=2\) なら \(R\) は \(1\) 次元の \(+\)-空間と
  \(2\) 次元の \(-\)-空間に分かれる。coordinate line を含まない
  \(L\)-安定部分空間は高々 \(1\) 次元なので \(|S|\le2\cdot3=6\)。
- \(L=1\) なら \(S=U\le R\)。coordinate line を含まない
  \(2\) 次元平面が存在し、\(|S|=9\) を達成する。

例えば

\[
U=\{a_1e_1+a_2e_2+a_3e_3:\ a_1+a_2+a_3=0\}
\tag{3.1}
\]

は三 coordinate line を一つも含まないので core-free である。
従って

\[
\boxed{\mu_{\rm tr}(G_3)=12,\qquad
G_3/U\text{ が最小 faithful transitive set}.}
\tag{3.2}
\]

coordinate line を含まない平面は、法線ベクトルの三成分が全て非零な
四平面であり、\(C_2^2\) がそれらへ単純推移する。よってこの最小作用も
一軌道で、F2 の B1 判定と整合する。

### F3.2 B2 は \(C_3\) によって破れる

\(R\) は可換なので \(R\le N_{G_3}(U)\)。一方、(3.1) の
\(C_2^2\)-stabilizer は自明である。従って

\[
N_{G_3}(U)=R,\qquad
\operatorname{Aut}_{G_3}(G_3/U)
\cong N_{G_3}(U)/U
\cong C_3 .
\tag{3.3}
\]

transitive monodromy の centralizer と dessin automorphism group は
この \(N_{G_3}(U)/U\) なので

\[
\boxed{\operatorname{Aut}(\mathcal D_{K^{(3)}})\cong C_3\ne1.}
\tag{3.4}
\]

よって B2 は FAIL。regular degree-\(108\) cover を使えば automorphism
group はさらに \(G_3\) 全体になるため、Galois closure へ移るだけでは
B2 は直らない。

橋を作る際は、少なくとも次のいずれかが必要である。

1. degree-\(12\) dessin に追加の sheet/tangent marking を入れて
   残留 \(C_3\) を殺す。
2. \(C_3\)-stabilizer を忘れず stacky Hurwitz point として扱い、
   scalar \(u\) でなく descent class を保存する。

degree \(27\) の \(C_2^2\)-補群作用は self-normalizing にできるが、
その stabilizer は \(\langle X\rangle\) の対合と交わるため
B3 を失う。したがって「作用を大きくすれば B2 と B3 が同時に直る」
わけではない。

### F3.3 B3 は通る

\(\langle X\rangle\) の位数 \(3\) 部分は
\(\langle X^2\rangle=\langle e_1\rangle\) である。
任意の共役 \(U^g\) は coordinate line を含まず、かつ \(U^g\) は
\(3\)-群なので

\[
\langle X\rangle\cap U^g=1.
\tag{3.5}
\]

従って \(X\) は \(12\) 点上で semiregular に作用し、cycle type は
\(6^2\)。\(Y,Z\) も同様である。よって三点全てで全分岐し、特に
B3 は PASS。

Riemann–Hurwitz も

\[
2g-2=-2\cdot12+3(12-2)=6
\tag{3.6}
\]

を与え、

\[
\boxed{g=4.}
\tag{3.7}
\]

---

## F4. B4 — 関連中心化群は \(C_6\)

\(c\in K^{(3)}\) なので、\(P=G_3\) 上で
\(\alpha:=\operatorname{Ad}(\bar\sigma _1)\) は

\[
\alpha(X)=X,\qquad
\alpha(Y)=Y^{-1}X^{-1}=Z,
\qquad
\alpha^2=\operatorname{Inn}(X).
\tag{4.1}
\]

一方、\(D_3^3\) 内で

\[
\begin{aligned}
C_{D_3^3}(X)
&=C_{D_3}(r)\times C_{D_3}(s)\times C_{D_3}(s)\\
&=\langle r\rangle\times\langle s\rangle\times\langle s\rangle .
\end{aligned}
\tag{4.2}
\]

\(G_3/R\) の reflection-parity は
\(\{000,011,101,110\}\) なので、(4.2) との交わりは

\[
\boxed{C_{G_3}(X)=\langle X\rangle\cong C_6.}
\tag{4.3}
\]

\(\alpha\)-固定元は \(\alpha^2=\operatorname{Inn}(X)\) にも固定される
から (4.3) に入り、逆に \(\alpha(X)=X\) なので

\[
\operatorname{Fix}_{G_3}(\alpha)=\langle X\rangle.
\tag{4.4}
\]

charming \(m\) では \(u=2m+1\) は
\[
u\bmod12\in\{1,5,7,11\},
\tag{4.5}
\]
従って \(\langle\alpha^u\rangle=\langle\alpha\rangle\)。ゆえに

\[
\boxed{
C_P(\bar\sigma _1^{\,u})
=\operatorname{Fix}_{G_3}(\alpha^u)
=\langle X\rangle\cong C_6 .
}
\tag{4.6}
\]

したがって B4 は PASS であり、ここから非可換 \(H^1\) は出ない。

注意すべき偽道標がある。位数 \(3\) の平方 \(X^2\) を中心化すると

\[
C_{G_3}(X^2)\cong C_3^3\rtimes C_2
\quad(|C_{G_3}(X^2)|=54)
\tag{4.7}
\]

となり非巡回である。しかし B4 の入力は \(X^2\) でなく、
primitive な \(\bar\sigma _1^u\)（同値にその primitive order-\(6\)
平方 \(X^u\)）である。(4.7) を B4 へ代入してはならない。

---

## F5. B5 と橋の算術形

\[
k=K_{\rm ord}^{(3)}=\operatorname{lcm}(3,2)=6
\tag{5.1}
\]

なので B5 は FAIL。B2 の descent を解決し、さらに cyclic torsor を
\(\mu_6\)-Kummer class と比較できた場合でも、

\[
[u]\ne1
\tag{5.2}
\]

だけでは飽和を言えない。必要なのは

\[
\boxed{\operatorname{ord}[u]=6.}
\tag{5.3}
\]

同値に \(2\)-primary 射影が位数 \(2\)、\(3\)-primary 射影が位数 \(3\)
を同時に持つことである。従って \(K^{(3)}\) 橋の最小 arithmetic
output は「単一の非自明ビット」でなく

\[
([u]_2,[u]_3)
\tag{5.4}
\]

でなければならない。ただし B2 が未修理の段階で
\([u]\in\mathbb Q^\times/(\mathbb Q^\times)^6\) と先に書いてはならない。
まず residual \(C_3\) を含む arithmetic model、cusp、tangent
rigidification、GT 側 torsor との比較写像を構成する必要がある。

---

## F6. 委嘱 17 の監査

| 委嘱 17 の主張 | 判定 |
|---|---|
| 「13系」は一点 witness の量化事故 | **PASS・裁定21で確定** |
| 同一系で ob が異なり \(\omega\) が非定数 | **PASS**。ただし真の係数系は mod \(4\) で周期 \(16\) まで縮む |
| 線型可解律 \(m\) 奇または \(8\mid m\) | **PASS**。便23が \(\binom{m+1}{3}\equiv0\pmod4\) の紙上証明を補完 |
| \(m\) だけの \(\operatorname{ob}_b(m)\) は書けない | **PASS**。正式式は \(\operatorname{ob}_b(m;\bar f)=f_{s_3}+f_wf_{r_2}\) |
| \(j=2\) の \(a\)-bit 全零の説明 | **結論 PASS・理由は差替え**。\(\theta(a)=-a\) だけでは零を強制しない |
| \(j=3\) で \(a\) 方向が \(2\)-torsion に限られる | **PASS**。ただし一ビットは残り、係数 \(2\) が発火し得る |
| \(j=3\) で \(b\) が \(4\) 値へ細分 | **FAIL** |
| \(j=3\) で \(a\ne0\) なら構造予想が反証される | **FAIL・向きが逆**。紙上式は \(a\ne0\) を許し、具体的に \(f_p\) 奇なら発火 |
| S0–S4 の実現手順 | **設計 PASS**。ただし S0 は現在「全40系で零点あり」と閉じ、このデータから S1 以降へ進む候補はない |
| E15 三条件分割 | **条件付き PASS／下記 F8 の修文必須** |

委嘱 17 §1・§4 のデータ法医学は便23および M6 と独立に収束した。
相互監査としてここは正式に閉じてよい。差戻しは \(j=3\) 予言と
E15 の条件の型だけである。

---

## F7. 正しい \(j=3\) 予言

\(e=j-1\)、\(R=\mathbb Z/2^e\) とする。便22で紙上証明した一般構造は

\[
\begin{aligned}
C^\theta
&=R(t_5+t_6)\oplus R(u_1+u_3)\oplus Ru_2\oplus R[2]u_4,\\
(1+\theta)\ker\mathcal N_C
&=(1+\theta)C\\
&=R(t_5+t_6)\oplus R(u_1+u_3)\oplus2Ru_2 .
\end{aligned}
\tag{7.1}
\]

従って全 \(e\ge1\) で

\[
\boxed{
\mathcal O_{6,e}
\cong R[2]\,a\oplus(R/2R)\,\bar b
\cong(\mathbb Z/2)^2.
}
\tag{7.2}
\]

特に \(j=3\), \(R=\mathbb Z/4\) でも target は四元のままである。
\(b\)-方向は \(\mathbb Z/4\) へ伸びず、係数の parity 一ビットしか残らない。

委嘱16の \(j=2\) では

\[
(C^\sigma)^\theta\longrightarrow\mathcal O_{6,1}
\tag{7.3}
\]

が偶然同型だった。しかし \(j=3\) では

\[
(C^\sigma)^\theta=R[2]a\oplus Rb
\longrightarrow
R[2]a\oplus(R/2R)\bar b
\tag{7.4}
\]

の kernel が \(2Rb\) である。委嘱17の「\(b\) が4値」は
(7.3) を一般 \(e\) へ延長したことによる誤りである。

さらに確定表の \(d_\theta,\kappa\) から、線型解 \(\bar f\) について

\[
\begin{aligned}
(q_\theta)_{u_4}
&=f_{t_2}-f_{t_3}-f_pf_q
  +(\bar\theta\bar f)_qf_p
 =-2f_p^2,\\
(q_\theta)_{u_2}
&\equiv f_{s_3}+f_wf_{r_2}\pmod2 .
\end{aligned}
\tag{7.5}
\]

ここで \(f_p=f_q\), \(f_{t_2}=f_{t_3}\) を用いた。
class 6 では \(q_N\) 補正は (7.1) の商で全 \(e\) について消える。
従って \(j=3\) の正確な branch-wise 予言は

\[
\boxed{
\operatorname{ob}_{j=3}(\bar f)
=
\left(
\frac{(q_\theta)_{u_4}}2\bmod2,\qquad
(q_\theta)_{u_2}\bmod2
\right)
=
\left(
f_p\bmod2,\qquad
f_{s_3}+f_wf_{r_2}\bmod2
\right).
}
\tag{7.6}
\]

つまり

- \(a\) は依然一ビットだが、代表係数は \(0\) または \(2\)。
- \(a\ne0\) はバグでなく、\(f_p\) 奇の正規予測。
- \(b\) は \(j=2\) と同じ parity 一ビット。
- target の大きさは全 \(j\ge2\) で \(4\) のまま。

これを \(j=3\) sweep の封印前仕様とすべきである。

---

## F8. \(j=3\) で full 可解性 \(=\) 線型可解性か

**判定は UNKNOWN。\(j=2\) からは継承できない。**
正しい同値条件は

\[
\boxed{
\mathcal L_m^{(3)}\ne\varnothing
\ \Longrightarrow\
\exists\bar f\in\mathcal L_m^{(3)}:
\quad f_p\equiv0,\quad
f_{s_3}+f_wf_{r_2}\equiv0\pmod2 .
}
\tag{8.1}
\]

\(j=2\) では第一条件が自動的に消えていた。\(j=3\) では新しい
\(p\)-parity gate になるため、「等号は続く」と予測登録する根拠はない。
一方 target 自体は拡大しないので、破れるともまだ言えない。
私の見立ては **両結果を UNKNOWN のまま封印し、最初の危険箇所を
\(a\)-bit に限定する**、である。

斉次核

\[
K_m^{(3)}
=\ker(1+\bar\theta)\cap\ker\bar{\mathcal N}_m
\subset(\mathbb Z/8)^{15}
\tag{8.2}
\]

では weight-2 式 \(3k_w=0\pmod8\) から \(k_w=0\)。
従って任意の基点 \(\bar f_0\) に対する障害差分は affine-linear で

\[
\boxed{
\lambda_m^{(3)}(k)
=
\bigl(
k_p,\
k_{s_3}+W(m)k_{r_2}
\bigr)\pmod2,\qquad
W(m)=\binom{m+1}{2}\pmod2 .
}
\tag{8.3}
\]

従って全点を愚直に列挙しなくても

\[
0\in\operatorname{ob}(\mathcal L_m^{(3)})
\iff
\operatorname{ob}(\bar f_0)\in
\lambda_m^{(3)}(K_m^{(3)})
\tag{8.4}
\]

で判定できる。

### \(j=3\) 実装へ要求する計算

1. `agree6_*.json` を入力に、法 \(8\) で線型段を解き、
   可解なら particular solution と \(K_m^{(3)}\) の invariant-factor
   generators、不可解なら dual witness を出す。
2. 各 generator に (8.3) を適用した \(2\times d\) bit matrix と
   その rank を証明書へ入れる。
3. 四値
   \[
   (0,0),(0,1),(1,0),(1,1)
   \]
   の multiplicity table を出す。各 attained value の重複度は
   \(|K_m^{(3)}|/|\operatorname{im}\lambda_m^{(3)}|\) と一致させ、
   総和を \(|K_m^{(3)}|\) に接続する。
4. full 可解判定は一 witness の値でなく、`"0,0"` の重複度が
   正であることに限定する。
5. ob-zero branch ごとに中心補正数
   \(|\ker\Lambda|=2^{e+1}=8\) を掛けた full mass と直接群積 M8 を照合する。
6. \(k\le6\) の binomial table は mod \(8\) で \(m\mapsto m+32\)
   に周期的なので、\(0\le m<32\) が数学的基本周期。
   事前登録窓が \(0\le m<64\) なら後半を独立な周期 fixture として残す。

この仕様なら「\(b\) が4値」という誤予言も、section 一点評価の再発も
同時に検出できる。

---

## F9. E15 三条件分割の監査

委嘱17の三項は、**潜在的な警報条件**としては有用だが、
互いに独立な三つの「障害条件」としては正しくない。

| 項 | 判定 | 修正 |
|---|---|---|
| **E15-a** \(C^\sigma\ne0\) | **条件付き PASS** | norm 欠損が残り得る警報。ただし非零障害群・零点不存在を意味しない。class 6 が反例 |
| **E15-b** \(\widehat H^0(\langle\theta\rangle,C)\ne0\) | **条件付き PASS** | Tate defect の正しい警報。「induced でない」と同値とは限らず、Maschke split の \(\theta\)-非同変性は別の diagnostic として分離する |
| **E15-c** \(3\) が非可逆 | **独立な障害条件としては FAIL** | Reynolds 補正 \(3^{-1}\mathcal N\) が使えない係数 regime の表示。障害そのものではなく、(a) を誘発しやすい原因か、一般 \(\Lambda\)-cokernel へ戻る分岐 |

正しい vanishing theorem は二条件で足りる。

> **E15\({}^{\rm layer}\) 修正版。**
> 各 \((\sigma,\theta)\)-安定中心層 \(M_r\) で
> \[
> M_r^\sigma=0,\qquad
> M_r^\theta=(1+\theta)M_r
> \tag{9.1}
> \]
> が成立すれば、その層の二欠損は同時補正できる。
> 全中心層で (9.1) が成立すれば、最下位の解は全塔を持ち上がる。

この証明には \(3^{-1}\) を仮定する必要がない。
\(\operatorname{im}(1+\sigma+\sigma^2)\subseteq M_r^\sigma=0\) だからである。

\(3\) が可逆で (9.1) の第一条件を落とす一般化では、

\[
\operatorname{ob}
=
\left[q_\theta-3^{-1}(1+\theta)q_N\right]
\in
M_r^\theta/(1+\theta)\ker\mathcal N
\tag{9.2}
\]

を使う。\(3\) が非可逆なら平均化せず、

\[
\Lambda(z)=((1+\theta)z,\mathcal Nz)
\tag{9.3}
\]

の simultaneous image/cokernel を直接扱う。これが E15-c の正しい役割である。

最後に必ず

\[
\text{障害群が非零}
\quad\nRightarrow\quad
\text{障害写像が非零}
\quad\nRightarrow\quad
0\notin\operatorname{ob}(\mathcal L)
\tag{9.4}
\]

の三段を分ける。class 6, \(j=2\) は三者を区別しないと誤判定する
標準反例である。

---

## F10. 状態札

| 主張 | 状態 |
|---|---|
| \(G_3\cong C_3^3\rtimes C_2^2\) と符号表 | **紙上 PASS** |
| B1–B5 判定 | **Sol 独立紙上判定**。委嘱18との突合前 |
| 最小 faithful degree \(12\)、genus \(4\) | **紙上導出** |
| dessin automorphism \(C_3\) | **紙上導出** |
| relevant centralizer \(C_6\) | **紙上導出** |
| 委嘱17の量化訂正 | **相互監査 PASS・裁定21と一致** |
| 委嘱17の \(j=3\) 四値 \(b\) 予言 | **棄却** |
| 正しい \(j=3\) target | \((\mathbb Z/2)^2\) |
| \(j=3\) full \(=\) linear | **UNKNOWN** |
| E15 三分割 | **修文後に条件付き PASS** |
| Lean verified | なし |

## ★ 教材

1. **同じ quotient group でも、dessin の automorphism は作用に依存する。**
   B2・B3 を判定する前に core-free subgroup \(U\) を一行で固定する。
2. **中心化する元を平方へすり替えない。**
   \(C_{G_3}(X^2)\) は大きく非巡回だが、B4 の primitive 元の中心化群は
   \(C_6\) である。
3. **modulus を上げても障害群が大きくなるとは限らない。**
   class 6 の \(b\)-方向は \(R/2R\) なので、全 \(j\) で一ビットである。
4. **係数素数は obstruction ではなく計算 regime を変えることがある。**
   \(3^{-1}\) が無いときは平均化を諦め、simultaneous map \(\Lambda\) へ戻る。

---

## 監査範囲外申告

- ブラインド指定された `docs/委嘱18*` は読んでいない。
  Opus の D2 並列答案は不可視のままである。
- `docs/対話帳.md` は新着 T-9 まで読んだ。T-9 は便23と並行した
  委嘱17の量化指摘であり、本便の D2 並列答案ではない。
- GAP、node、Python、Lean、twincell 列挙、\(j=3\) sweep は実行していない。
  `K3.v1.json` と既存 verdict は D1 数値の照合資料として静的に読んだ。
- degree-\(12\) dessin の明示方程式、\(\mathbb Q\)-model、
  residual \(C_3\) twist の算術分類、Kummer/GT 比較写像は構成していない。
- \(j=3\) の線型可解集合・四値 multiplicity・M8 群積は未観測であり、
  本返信はそれらの値を予測登録していない。
- 作業開始時から存在した他ファイルの変更には触れていない。
  本便で変更したのは `sol/sol_reply_24_d2.md` のみである。
