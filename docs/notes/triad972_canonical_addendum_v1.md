# TRIAD-972 canonical addendum v1 — fields, degrees, and interpretation types

日付: 2026-08-13。返書 124 §1 の式 (1)–(5) を theorem pin 用に独立化し、同 §3/§5/§6 の小修理を併記する。

## 1. 型の固定

\[
K:=\mathbf Q(\zeta_9),\qquad
E:=L_{9,\mathrm{Aff}}=K(\sqrt[9]{a_{\rm mod9}}),\qquad
F:=L_{S4}=K(\sqrt[9]{b_{\rm mod9}}),
\]

\[
L_{9,\mathrm{full}}:=E(i)
=\mathbf Q(\zeta_{36},\sqrt[9]{a_{\rm mod9}}),\qquad
d_9:=[E:K],\quad d_{S4}:=[F:K].
\]

ここで \(a_{\rm mod9}\) は法 9 へ降下した rational Kummer class であり、法 18 の \(a_{9,\rm mod18}\) とは別記号である。算術像は \(A_{\rm arith}\)、DICHOTOMY の分類語は A 型と書き、裸の \(A\) を共有しない。

RES-INJ-9 の適用範囲では

\[
r:=\left|\langle[a_{\rm mod9}]\rangle
\cap\langle[b_{\rm mod9}]\rangle\right|
\]

を \(\mathbf Q^\times/(\mathbf Q^\times)^9\) と \(K^\times/(K^\times)^9\) のどちらでも同じ整数として読む。

## 2. 定理 CAN-972

### 仮定

1. \(M=K^{(9)}\cap N_{S4}\) について ROOF の fibre product
   \[
   GT(M)\cong GT(K^{(9)})\times_U GT(N_{S4}),\qquad |U|=6
   \]
   があり、両因子の位数は \(108,54\) である。
2. 算術射 \(\rho_M,\rho_9,\rho_{S4}\) は
   \[
   \rho_i=R_i\circ\rho_M
   \]
   を満たし、\(R=(R_9,R_{S4})\) は単射である。
3. \(\ker\rho_9,\ker\rho_{S4}\) の固定体はそれぞれ
   \(L_{9,\mathrm{full}},F\) である。
4. \(E/K,F/K\) は上記の Kummer 拡大で、RES-INJ-9 が二つの cyclic subgroup の交叉を rational classes へ戻す。

### 結論

\(K\) は \(\mu_9\) を含むから Kummer 理論により

\[
[EF:K]
=|\langle[a_{\rm mod9}],[b_{\rm mod9}]\rangle|
=\frac{d_9d_{S4}}r.
\tag{1}
\]

ROOF の位数公式から

\[
|X_{\rm shadow}|:=|GT(M)|
=\frac{108\cdot54}{6}
=972.
\tag{2}
\]

自然性と \(R\) の単射性から

\[
\ker\rho_M=\ker\rho_9\cap\ker\rho_{S4},\qquad
A_{\rm arith}:=\operatorname{im}\rho_M
\cong\operatorname{Gal}(L_{9,\mathrm{full}}F/\mathbf Q),
\]

従って

\[
|A_{\rm arith}|
=[L_{9,\mathrm{full}}F:\mathbf Q].
\tag{3}
\]

\([EF:K]\) は 3 冪であり \([K(i):K]=2\) なので \(K(i)\cap EF=K\)。よって

\[
\boxed{
|A_{\rm arith}|
=[L_{9,\mathrm{full}}F:\mathbf Q]
=6[L_{9,\mathrm{full}}F:K]
=12[EF:K]
=\frac{12d_9d_{S4}}r.
}
\tag{4}
\]

従って集合差の計数は

\[
\boxed{
|X_{\rm shadow}\setminus A_{\rm arith}|
=972-\frac{12d_9d_{S4}}r.
}
\tag{5}
\]

係数 12 は

\[
[K:\mathbf Q]\,[K(i):K]=6\cdot2
\]

である。従って係数 12 を使う次数式は必ず

\[
12[L_{9,\mathrm{Aff}}L_{S4}:K]
\]

と書く。\(L_{9,\mathrm{full}}\) を使うなら係数は 6 である。

## 3. B3 小修理 4 件

### 3.1 D9-VAL の第二証明

\(a_{\rm mod9}=2^7\) の位数 9 は 2-adic valuation で直接出る。補助的な ramification 証明を使うなら「唯一の三次部分体」を仮定しない。もし交叉が三次なら \(x^9-2\) の Eisenstein 性から 2 はその交叉で分岐するが、\(K=\mathbf Q(\zeta_9)\) とその部分体では 2 は不分岐であり矛盾する。

### 3.2 GAUGE-18 の labels

同じ \(F\)-有理 cusp の二つの \(F\)-有理 parameter は

\[
s'=c_1s(1+O(s)),\qquad u_9'=u_9c_1^{-18}.
\]

従って法 18、さらに法 9 の class は不変である。「残る gauge は Belyi scaling だけ」は \(P_0,P_\infty\) と target の \(0,1,\infty\) labels を固定した場合に限って用いる。

### 3.3 cyclotomic ambient

\(\zeta_{12}\notin\mathbf Q(\zeta_3)\)。\(\zeta_{12}\) を単数表で使う場合の ambient field は \(F_9=\mathbf Q(\zeta_{36})\) と明記する。

### 3.4 rational 18th-power classes の符号

\[
\mathbf Q^\times/(\mathbf Q^\times)^{18}
\cong\mathbf Z/2\oplus\bigoplus_p\mathbf Z/18.
\]

法 18 の表では符号の \(\mathbf Z/2\) を残す。法 9 では \(-1=(-1)^9\) なので符号成分は消える。

## 4. B5 二行分記 template

各測定量は次の二行を一組として記帳する。

> raw: 使用した宣言模型・cert・再現 command と、そこから得た class/vector/order。測定格だけを書く。
>
> interpretation: raw object を \(L_{9,\mathrm{Aff}}\), \(L_{S4}\), \(r\), \(A_{\rm arith}\) のいずれとして読むか。必要な model/dessin/framework 前件を列挙し、その格を別に書く。

raw の格から interpretation の格を自動的に上げない。

## 5. S-3 と NAME-COLLIDE の固定文

P8 v3.2 の S-3 は「\(a_9\) 側」でなく

> 法 9 へ降下した \([a_{\rm mod9}]\) 側

と書く。法 18 の対象は \([a_{9,\rm mod18}]\) とする。

また namespace の無い S3 ラベルを廃し、少なくとも

- E1-S3: dihedral inverse-system splitting lemma
- FAM-V2-S3: family statement in §V.2.1
- P8-v3.2-S-3: prereg schema item

のように namespace を付ける。

## 6. 射程

本 addendum は式の型と条件を pin する文書である。個々の model binding、P1/P2、C1′/P5′、および算術像の全射性をこの文書単独からは導かない。
