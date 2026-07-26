# Sol 返信 — 第 16 便: \(u\) の独立抽出と framed comparison

## 冒頭結論

\[
\boxed{
u=\frac{59049}{2097152}
=\frac{3^{10}}{2^{21}}
=\left(\frac9{16}\right)^5\frac12
\equiv \frac12
\pmod{(\mathbf Q^\times)^5}.
}
\tag{0.1}
\]

従って
\[
\boxed{u\notin(\mathbf Q^\times)^5.}
\tag{0.2}
\]

LMFDB の表示モデルと branch-cycle data を入力として採用する限り、比較は actual \(S_5\)-action のレベルで閉じる。標準の正向き inertia と
\[
X:a\longmapsto a+1
\]
の規約では
\[
\boxed{
b_\gamma=\kappa_2(\gamma)
=-\kappa_u(\gamma)
\quad\text{up to an affine-origin coboundary},
}
\tag{0.3}
\]
ここで
\[
\frac{\gamma(\sqrt[5]{2})}{\sqrt[5]{2}}
=\zeta _5^{\,\kappa_2(\gamma)},\qquad
\frac{\gamma(\sqrt[5]{u})}{\sqrt[5]{u}}
=\zeta _5^{\,\kappa_u(\gamma)}.
\]

従って affine cocycle の Kummer class は
\[
[b_A]=[2]=[u^{-1}]
\quad\text{in}\quad
H^1(G_{\mathbf Q},\mu _5)
\cong\mathbf Q^\times/(\mathbf Q^\times)^5.
\tag{0.4}
\]
切り出される体は
\[
\boxed{
E=\mathbf Q(\sqrt[5]{2}),\qquad
L=\mathbf Q(\zeta _5,\sqrt[5]{2}),\qquad
\operatorname{Gal}(L/\mathbf Q)\cong F_{20}.
}
\tag{0.5}
\]

したがって定理 R は非 5 乗側へ倒れ、
\[
\boxed{
\operatorname{Ih}_{N_A}:G_{\mathbf Q}
\twoheadrightarrow
\operatorname{GTSh}(N_A,N_A)\cong F_{20}.
}
\tag{0.6}
\]

ただし状態札は、**LMFDB の曲線・写像・branch cycles を入力とする paper proof / candidate** である。LMFDB 式そのものの独立 algebraic checker と Opus 側の並列値との突合前に `cross-checked`、Lean 証明書なしに `verified` とはしない。

★ 便 15 の \(\lambda^5=-16/27\) は、補助的な genus-\(0\) \((2,3,5)\) dessin の接方向であり、本件の genus-\(2\) \((5,5,5)\) dessin の \(u\) ではない。両者は passport も genus も異なり、Kummer 類も一致しない。便 15 の「framed/Kummer が正解」という構造判定は維持するが、FC-4 の対象は \((2,3,5)\) から \((5,5,5)\) へ訂正する。

---

## F1. LMFDB model と完全分岐点

LMFDB `5T4-5_5_5-a` の hyperelliptic model を
\[
C:\quad
y^2=x^6+A x^4+B x^2+C_0
\tag{1.1}
\]
と書く。ただし
\[
A=\frac{567}{512},\qquad
B=\frac{111537}{1048576},\qquad
C_0=\frac{531441}{33554432}.
\tag{1.2}
\]

Belyi map は
\[
\beta=
\frac{(x^2+a)y+N(x)}{D(x)},
\qquad
a=\frac{243}{1024},
\tag{1.3}
\]
ただし
\[
\begin{aligned}
N(x)
&=x^5+\frac{405}{512}x^3
+\frac{32805}{1048576}x
+\frac{59049}{2097152},\\
D(x)
&=x^5-\frac{45}{32}x^4
+\frac{405}{512}x^3
-\frac{3645}{16384}x^2\\
&\hspace{22mm}
+\frac{32805}{1048576}x
-\frac{59049}{33554432}.
\end{aligned}
\tag{1.4}
\]

even sextic model の無限遠点は
\[
P_\pm=[1:\pm1:0]\in C(\mathbf Q)
\]
である。局所助変数を
\[
s=\frac1x,\qquad \eta=\frac{y}{x^3}
\tag{1.5}
\]
と取ると、
\[
\eta^2=1+A s^2+B s^4+C_0s^6.
\]

\(P_-\) は \(\eta=-1\) の枝である。F2 で
\[
\beta(P_-)=0,\qquad \operatorname{ord}_{P_-}(\beta)=5
\]
を直接示す。従って \(P_-\) が target \(0\) の唯一の原像であり、source model 上の「無限遠接点」である。

target の branch point を \(\infty\) と呼ぶ規約を使いたければ、Belyi map を \(\beta_\infty=1/\beta\) とする。このとき \(\infty\) の標準局所座標
\[
T=\frac1{\beta_\infty}=\beta
\]
を使うので、以下の主係数 \(u\) は変わらない。

---

## F2. \(u\) の紙上抽出

\(P_-\) の枝では
\[
\eta=
-1-\frac A2s^2
-\left(\frac B2-\frac{A^2}{8}\right)s^4
+O(s^6).
\tag{2.1}
\]

\(N(x)\) の三係数を
\[
n_2=\frac{405}{512},\qquad
n_4=\frac{32805}{1048576},\qquad
n_5=\frac{59049}{2097152}
\]
と書く。分子を \(s^5\) 倍すると
\[
\begin{aligned}
s^5\bigl((x^2+a)y+N(x)\bigr)
&=(1+as^2)\eta
+1+n_2s^2+n_4s^4+n_5s^5.
\end{aligned}
\tag{2.2}
\]

ここで二つの exact cancellation
\[
a+\frac A2
=\frac{243+567}{1024}
=\frac{405}{512}
=n_2
\tag{2.3}
\]
および
\[
\frac B2-\frac{A^2}{8}+\frac{aA}{2}
=\frac{32805}{1048576}
=n_4
\tag{2.4}
\]
が成立する。実際 (2.4) を共通分母 \(2^{21}\) で書けば、分子は
\[
111537-321489+275562=65610
\]
である。

従って (2.2) は
\[
s^5\bigl((x^2+a)y+N(x)\bigr)
=n_5s^5+O(s^6).
\tag{2.5}
\]
一方、
\[
s^5D(x)=1-\frac{45}{32}s+O(s^2)
\tag{2.6}
\]
なので分母の主係数は 1。よって
\[
\boxed{
\beta=
\frac{59049}{2097152}s^5+O(s^6).
}
\tag{2.7}
\]

\(P_+\) では \(\eta=+1\) なので \(\beta(P_+)=2\)。従って上の cancellation は確かに \(P_-\) だけで起こっている。

最後に
\[
\frac{59049}{2097152}
=\frac{3^{10}}{2^{21}}
=\left(\frac9{16}\right)^5\frac12
\]
より、(0.1) を得る。

---

## F3. \(u\) は 5 乗数でない

最短の判定は 2-adic valuation である。
\[
v_2(u)=-21\not\equiv0\pmod5.
\tag{3.1}
\]
有理数の 5 乗なら全素数 valuation が 5 の倍数なので、
\[
u\notin(\mathbf Q^\times)^5.
\]

また
\[
\sqrt[5]{u}=\frac9{16}\,\frac1{\sqrt[5]{2}}
\tag{3.2}
\]
である。従って
\[
\mathbf Q(\sqrt[5]{u})
=\mathbf Q(\sqrt[5]{2}).
\tag{3.3}
\]

\(T^5-2\) は 2 で Eisenstein だから、この体は次数 5。さらに
\(\mathbf Q(\zeta _5)\) は次数 4 なので両者の共通部分は \(\mathbf Q\)、正規閉包
\[
L=\mathbf Q(\zeta _5,\sqrt[5]{2})
\]
は次数 20 で、その Galois 群は
\[
C_5\rtimes\mathbf F_5^\times=F_{20}.
\]

---

## F4. LMFDB branch cycles と \(N_A\) marking の exact 一致

LMFDB の branch cycles を
\[
\begin{aligned}
\sigma _0&=(1\,2\,3\,4\,5),\\
\sigma _1&=(1\,3\,4\,2\,5),\\
\sigma _\infty&=(1\,2\,5\,3\,4)
\end{aligned}
\tag{4.1}
\]
とする。本工房の marking は
\[
X=(1\,3\,2\,4\,5),\qquad
Y=(1\,3\,4\,5\,2).
\tag{4.2}
\]

ここで
\[
h=(1\,3\,4\,5)\in S_5
\tag{4.3}
\]
と置けば、cycle の各文字を \(h\) で移すだけで
\[
\boxed{
h\sigma _0h^{-1}=X,\qquad
h\sigma _1h^{-1}=Y.
}
\tag{4.4}
\]
\(\sigma _0\sigma _1\sigma _\infty=1\) の規約では第三成分も自動的に
\((XY)^{-1}\) へ移る。

従って、この degree-\(5\) monodromy representation
\[
\psi:\widehat F_2\longrightarrow A_5\hookrightarrow S_5
\]
は、(4.3) により relabel した後
\[
\psi(x)=X,\qquad\psi(y)=Y
\]
となり、
\[
\ker\psi=\bar N_A:=N_A\cap F_2.
\tag{4.5}
\]

これは passport の一意性だけに頼った「共役まで」の主張ではなく、比較補題で使える actual marking である。\(h\) が odd permutation であることは、\(5A/5B\) の outer twist を吸収しているだけで、kernel の同定を妨げない。

---

## F5. framed comparison lemma — actual \(S_5\)-action で閉じる

\[
U=\mathbf P^1_{\mathbf Q}\setminus\{0,1,\infty\}
\]
とし、標準 tangential basepoint \(0\vec1\) を取る。LMFDB cover の制限
\[
V\longrightarrow U
\]
は degree 5 finite étale cover であり、その tangential fiber を \(\Omega\) とする。

標準 tangential section による arithmetic monodromy を
\[
\rho_\beta:G_{\mathbf Q}\longrightarrow S(\Omega)\cong S_5
\tag{5.1}
\]
と書く。幾何 monodromy \(\psi(\widehat F_2)=A_5\) に対して、fiber functor の自然性は
\[
\rho_\beta(\gamma)\,
\psi(g)\,
\rho_\beta(\gamma)^{-1}
=
\psi(\gamma\cdot g)
\qquad(g\in\widehat F_2)
\tag{5.2}
\]
を与える。

Ihara の規約
\[
\gamma(x)=x^{\chi(\gamma)},\qquad
\gamma(y)=f_\gamma^{-1}y^{\chi(\gamma)}f_\gamma
\tag{5.3}
\]
と (4.5) を (5.2) に代入すると、
\[
\begin{aligned}
\rho_\beta(\gamma)X\rho_\beta(\gamma)^{-1}
&=X^{\chi(\gamma)},\\
\rho_\beta(\gamma)Y\rho_\beta(\gamma)^{-1}
&=\bar f_\gamma^{-1}Y^{\chi(\gamma)}\bar f_\gamma.
\end{aligned}
\tag{5.4}
\]

右辺は \(\Phi(\operatorname{Ih}_{N_A}(\gamma))\) を定義する式と逐語的に同じである。さらに
\[
C_{S_5}(A_5)=1
\tag{5.5}
\]
なので、同じ automorphism of \(A_5\) を誘導する二つの sheet permutation は一致する。従って
\[
\boxed{
\rho_\beta
=\Phi\circ\operatorname{Ih}_{N_A}
}
\tag{5.6}
\]
が、Out\((A_5)\) でなく actual \(S_5\) の等式として成立する。

これは便 15 で求めた inner lift を埋める比較補題である。鍵は ordinary dessin の同型類でなく、**正しい \((5,5,5)\) cover の tangential fiber**を使ったことである。transitivity は (5.6) の証明に仮定していない。

右作用を採る流儀では (5.2)–(5.6) の全 permutation が逆になる。その場合も Kummer class は非零冪へ変わるだけで、全射判定と切り出す体は同じである。

---

## F6. \(b_\gamma\) と Kummer cocycle の exact 符号

\[
\alpha^5=u,\qquad
\theta^5=2,\qquad
\alpha=\frac9{16}\theta^{-1}
\tag{6.1}
\]
と取る。\(t=\beta\) とし、\(t^{1/5}\) を標準 tangential basepoint の Puiseux parameter とする。

(2.7) の五つの lift は、leading term で
\[
s_j=
\zeta _5^j\alpha^{-1}t^{1/5}
+O(t^{2/5}),
\qquad j\in\mathbf F_5
\tag{6.2}
\]
と書ける。正向き inertia は
\[
j\longmapsto j+1
\tag{6.3}
\]
なので、この \(j\) が F1 の affine coordinate
\(X:j\mapsto j+1\) である。

Kummer cocycle を
\[
\frac{\gamma(\theta)}{\theta}
=\zeta _5^{\kappa _2(\gamma)}
\tag{6.4}
\]
と定義する。標準 tangential action は formal parameter \(t^{1/5}\) を固定し、係数へ作用するので、
\[
\begin{aligned}
\gamma\!\left(\zeta _5^j\alpha^{-1}\right)
&=
\zeta _5^{\chi _5(\gamma)j}
\frac{\gamma(\alpha^{-1})}{\alpha^{-1}}
\alpha^{-1}\\
&=
\zeta _5^{\chi _5(\gamma)j+\kappa _2(\gamma)}
\alpha^{-1}.
\end{aligned}
\tag{6.5}
\]
従って
\[
\boxed{
\rho_\beta(\gamma)(j)
=\chi _5(\gamma)j+\kappa _2(\gamma).
}
\tag{6.6}
\]

\(\kappa _u\) を
\[
\gamma(\alpha)/\alpha=\zeta _5^{\kappa _u(\gamma)}
\]
で定義すれば、(6.1) から
\[
\kappa _u=-\kappa _2.
\]
従って
\[
\boxed{
b_\gamma=\kappa _2(\gamma)=-\kappa _u(\gamma).
}
\tag{6.7}
\]

sheet \(j=0\) の選択を変えると
\[
b_\gamma\longmapsto
b_\gamma+(1-\chi _5(\gamma))c
\qquad(c\in\mathbf F_5)
\tag{6.8}
\]
となる。これは coboundary である。従って本工房で既に固定された affine origin が (6.2) と異なっていても、
\[
\boxed{[b_A]=[2]=[u^{-1}]}
\tag{6.9}
\]
は不変である。

ここで Opus 定理 R の「主係数 \(u\)」と、標準 Kummer torsor
\(w^5=a\) の class \(a\) には逆元が入る。実際 lift の係数は
\[
w^5=u^{-1}.
\]
非自明性と生成する field は同じだが、\(b_\gamma\) との exact 比較では (6.7) の符号を落としてはいけない。

---

## F7. 定理 R の帰結

F6 より
\[
\rho_\beta(G_{\mathbf Q(\zeta _5)})
\]
は \(T^5-2\) の Kummer extension の \(C_5\) を与える。これは非自明なので、位数が素数 5 であることから kernel direction 全体である。

一方、線形部は
\[
\chi _5:G_{\mathbf Q}\twoheadrightarrow\mathbf F_5^\times=C_4
\]
である。従って
\[
|\operatorname{im}\rho_\beta|=5\cdot4=20
\]
かつ
\[
\operatorname{im}\rho_\beta
=\operatorname{AGL}_1(\mathbf F_5)=F_{20}.
\]
F5 の比較から
\[
\operatorname{im}\operatorname{Ih}_{N_A}
=\operatorname{GTSh}(N_A,N_A).
\]

よって定理 R は **(α) 非 5 乗側**へ倒れる。少なくとも本窓では、

- 20 shadow は全て arithmetical。
- 従って全て genuine。
- 算術像が切り出す finite extension は
  \[
  \mathbf Q(\zeta _5,\sqrt[5]{2})/\mathbf Q.
  \]

となる。

---

## F8. 便 15 の \(-16/27\) との関係

便 15 の genus-\(0\) map は
\[
B(z)=
\frac{(3-4z)(2z^2+2z+3)^2}{27}
\]
で、passport は
\[
(2^2 1,\ 3 1^2,\ 5).
\]
無限遠で
\[
T=\frac1{B(z)}
=-\frac{27}{16}s^5+O(s^6),
\qquad s=\frac1z.
\tag{8.1}
\]

従って定理 R と同じ「主係数」規約なら
\[
u_{235}=-\frac{27}{16}.
\tag{8.2}
\]
便 15 で報告した
\[
\lambda_{235}^5=-\frac{16}{27}
\tag{8.3}
\]
は、その逆元
\[
\lambda_{235}^5=u_{235}^{-1}
\]
であり、lift direction の Kummer class であった。

今回の \((5,5,5)\) dessin では
\[
u_{555}\equiv\frac12,\qquad
\lambda_{555}^5=u_{555}^{-1}\equiv2.
\tag{8.4}
\]
従って lift class を同じ規約で比較すると
\[
\frac{[\lambda_{555}^5]}{[\lambda_{235}^5]}
=
\left[-\frac{2^{17}}{3^7}\right]
=
[2^2 3^3]
\ne1
\quad\text{in }\mathbf Q^\times/(\mathbf Q^\times)^5.
\tag{8.5}
\]

また principal coefficient 同士でも
\[
\frac{[u_{555}]}{[u_{235}]}
=[2^3 3^2]\ne1.
\tag{8.6}
\]

この不一致は座標変換の失敗ではない。二つの dessin は

| | 便 15 の補助 dessin | 本件の dessin |
|---|---:|---:|
| passport | \((2^2 1,3 1^2,5)\) | \((5,5,5)\) |
| genus | 0 | 2 |
| 役割 | \((q,r,v)\) factorization の modular 座標 | \(N_A\) の degree-\(5\) quotient |

であり、別対象である。source genus も branch cycle partitions も Belyi coordinate change では変わらないため、同一 passport への変換ではない。

従って便 15 FC-4 の
\[
\{\text{genus-0 \((2,3,5)\) map の接方向}\}
\stackrel?=\{\text{\(N_A\) shadow frame}\}
\]
は撤回する。正しい左辺は genus-\(2\) \((5,5,5)\) cover の
\(0\vec1\)-fiber である。数値差を「未知の twist」で救う必要もない。

---

## F9. 開示資料に対する二つの errata

### F9.1 trivial torsor の étale algebra

Opus 定理 R は \(u\) が 5 乗のとき
\[
E=\mathbf Q^5
\]
と書いているが、\(\mu _5\) は \(\mathbf Q\) 上 constant ではない。正しくは
\[
\mathbf Q[w]/(w^5-1)
\cong
\mathbf Q\times\mathbf Q(\zeta _5).
\tag{9.1}
\]
\(\mathbf Q(\zeta _5)\) へ base change して初めて五つの点へ split する。この修正は
\[
u\text{ 非 5 乗}\iff\text{5 点作用が推移的}
\]
および本便の全射結論には影響しない。

### F9.2 `aut_group` の解釈

hunter 覚書は LMFDB の
`aut_group = [(1,2,3,4,5)]`
を「被覆の自己同型群が \(C_5\)」と解釈している。しかし connected degree-\(5\) cover の dessin automorphism group は
\[
C_{S_5}(\langle\sigma _0,\sigma _1\rangle)
=C_{S_5}(A_5)=1.
\tag{9.2}
\]
従って「Belyi cover と可換する order-\(5\) automorphism」という解釈は不可能である。表示は one-line identity か別 schema の値として再確認すべきであり、少なくとも \(C_5\) deck group の根拠には使えない。

(9.2) の自明性は F5 では好都合であり、Galois action と shadow automorphism の間に余分な centralizer ambiguity が無い理由になる。

---

## F10. 条件と状態札

本便の論理依存を分離する。

| 入力 | 状態 | 本便での扱い |
|---|---|---|
| \(N_A\) isolated、\(GTSh(N_A)\cong F_{20}\)、\(\Phi\) | 裁定 15 により二系統確定 | 採用 |
| LMFDB curve/map/branch cycles | hunter が API 実取得した一つの外部データ源 | 入力として採用、独立再計算なし |
| \(P_-\) の主係数 \(u\) | 本便の独立紙計算 | (2.1)–(2.7) |
| LMFDB triple と \((X,Y)\) marking | 本便の明示 conjugator | (4.3)–(4.5) |
| framed comparison | fiber functor の自然性と trivial centralizer による紙証明 | F5–F6 |
| \(u\) の非 5 乗 | valuation / Eisenstein | F3 |

従って、**課題が指定した「LMFDB の明示データから計算せよ」という宇宙内では、全射判定は無条件に YES** である。プロジェクト全体の状態札としては、

> `A5 arithmetic surjectivity: paper proof PASS conditional on the displayed LMFDB record; independent algebraic certificate pending`

とするのが正確である。

独立 checker が最低限確認すべきなのは、

1. (1.1) 上で (1.3) が well-defined な degree-\(5\) Belyi map であること。
2. \(\operatorname{div}(\beta)=5P_0-5P_\infty\) と \(\operatorname{div}(1-\beta)=5P_1-5P_\infty\)。
3. branch cycles (4.1) と monodromy \(A_5\)。
4. \(P_-= [1:-1:0]\) で (2.7)。
5. conjugator (4.3)。

である。これが LMFDB helper を共有しない系統で通れば、数値・幾何入力は `cross-checked` に上げられる。Lean へはまず rational cancellation (2.3)–(2.4)、class identity (0.1)、conjugator (4.4) を小さな証明書として切り出すのがよい。

---

## ★ 教材

1. Kummer class を読む前に、「主係数 \(u\)」と「lift coefficient \(\lambda^5=u^{-1}\)」を分ける。非自明性は同じでも affine cocycle の符号が逆になる。
2. 同じ \(A_5\) monodromy、同じ order-\(5\) inertia でも、\((2,3,5)\) と \((5,5,5)\) の tangential torsor は同じとは限らない。本件では実際に class が異なる。
3. exact branch-cycle conjugator と \(C_{S_5}(A_5)=1\) がそろえば、Galois fiber action と \(\Phi\circ\operatorname{Ih}\) は outer class でなく actual permutation として一致する。
4. \(u\equiv1/2\) は、affine translation cocycle が \(2\) の Kummer cocycleになることを意味する。切り出す体は最も単純な Frobenius 型 extension \(\mathbf Q(\zeta _5,\sqrt[5]{2})\) である。
5. \(\mu _5\)-torsor が trivial でも五点が \(\mathbf Q\)-rationalになるわけではない。cyclotomic \(C_4\) は残る。

---

## 監査範囲外の申告

- turn 冒頭で `docs/対話帳.md` の新着 T-2 と `docs/所在と能力.md` を読んだ。T-2 は E19 の単系統数値更新であり、本 A\(_5\) 便では再計算・正式裁定していない。
- Sol の役割規律に従い、GAP、node、Python、Lean は実行していない。\(u\) は LMFDB 表示式の Laurent/Puiseux 展開を紙上で行って抽出した。
- LMFDB API を本便で再取得していない。`docs/scout/hunt_20260726_belyi555.md` に開示された curve、map、plane model、branch cycles を入力とした。
- plane model
  \[
  x^5t^3+(-5x+2)t^2+(-5x+6)t+4
  \]
  からの第二抽出はしていない。LMFDB hyperelliptic model と plane model の birational change も範囲外である。
- \(\beta-1\) と pole divisor の全因数分解、curve の smoothness、全 branch locus、LMFDB record の独立再構成はしていない。
- Nakamura/Deligne の接基点原典は本便ではページ画像照合していない。F5–F6 は Puiseux fiber による直接証明であり、出典の権威に依存させていない。
- Opus 委嘱 12 の並列計算結果は未開示であり、本数値計算では参照していない。
- `verified` は Lean に予約する。本便の新規結果は paper proof / candidate である。
- 過去の `sol_reply_15_a5.md` は記録として変更せず、数値候補と FC-4 の訂正は現在便 F8 に記した。
- 主な入力の SHA-256:
  - `sol/sol_task_16_u_extraction.txt`: `5ECA1206ED63B0C964D2ED82A69C7C813B8649532D03D16A7A2A1D2068278C03`
  - `sol/裁定_15_a5_q.md`: `34568F7CDEF883AD93EF959E05D2F9A8F619BB3E849D614BAAD4F38D8296FE7E`
  - `docs/scout/hunt_20260726_belyi555.md`: `918996C85340FC5669A847C2B045033E8F3EF7077063DDA58C3E7DCA8432BE4B`
  - `docs/week4-A5算術飽和_opus_v1.md`: `CF8BD2B424630529D67B0EE319D65B7EB71EED125851C8CD461466B7DBFF9DDA`
  - `docs/week1-定義ノート.md`: `24DB1372FD191659F1F0149CB669870DFF470DB1F779D3E5F83DBA4171501C6C`
  - `sol/sol_reply_15_a5.md`: `7D6CDFCA9E169C3FA1550A1B160906BA797FDD13FDF7666561410F8E62314C19`
- 今便で作成した主成果物は `sol/sol_reply_16_u.md`。恒久例外に従い、`docs/対話帳.md` へ T-2 の状態札だけを答える T-3 を追記した。既存 T-1/T-2 は編集していない。
- 最終 `git status` には並走作業と思われる `ops/codex_activity_sol2.log` と `docs/scout/hall5.mjs` も見えたが、私は両者を読まず、編集・復元していない。

---

## 考察と提案

P162【\(u\) の採用】LMFDB model に対する主係数
\[
u=3^{10}/2^{21}\equiv1/2
\]
を paper proof / candidate として採用する。独立 algebraic checker が同じ局所展開を再現するまで `cross-checked` としない。

P163【比較補題】F5 の
\[
\rho_\beta=\Phi\circ\operatorname{Ih}_{N_A}
\]
を framed comparison の正式命題とする。仮定は exact marking (4.4)、標準 tangential section、\(C_{S_5}(A_5)=1\) であり、transitivity を仮定しない。

P164【Kummer cocycle】正向き inertia \(X:j\mapsto j+1\) の規約で
\[
b_\gamma=\kappa_2(\gamma)=-\kappa_u(\gamma)
\]
を採用する。affine origin の差は (6.8) の coboundary として証明書に保存する。

P165【算術飽和】LMFDB record の algebraic correctness を入力とする paper theorem として
\[
G_{\mathbf Q}\twoheadrightarrow GTSh(N_A,N_A)\cong F_{20}
\]
および切出体
\[
\mathbf Q(\zeta _5,\sqrt[5]{2})
\]
を登録する。

W125【状態札】P165 は現時点で `conditional on displayed LMFDB data / paper proof PASS`。DB 非共有の divisor・branch-cycle checker と Opus 並列値の突合前に cross-checked としない。

W126【便 15 erratum】\(-16/27\) は genus-\(0\) \((2,3,5)\) auxiliary dessin の lift class であり、\(N_A\) の arithmetic \(u\) ではない。FC-4 の対象を genus-\(2\) \((5,5,5)\) tangential fiber へ置換する。

P166【最小証明書】F10 の五項目を一つの exact certificate にする。とくに局所展開は浮動小数でなく (2.3)–(2.6) の有理数恒等式を保存する。

W127【inverse convention】`leading_u`、`lift_kummer = leading_u^{-1}`、`affine_b_class` の三欄を分ける。本件では
\[
[u]=[1/2],\qquad [u^{-1}]=[b_A]=[2].
\]

W128【trivial torsor erratum】定理 R の trivial case は \(E=\mathbf Q^5\) でなく
\[
E=\mathbf Q\times\mathbf Q(\zeta _5)
\]
と修正する。base change to \(\mathbf Q(\zeta _5)\) 後にのみ五点へ split する。

W129【aut_group erratum】LMFDB `aut_group` 表示から \(C_5\) deck group を読まない。dessin automorphism は \(C_{S_5}(A_5)=1\) である。

P167【Lean 初弾】(0.1)、(2.3)、(2.4)、(4.4) を exact rational/permutation lemma として Lean 初弾候補にする。全 Belyi map verification はその後段とする。

W130【最終判定】`u non-fifth: PASS`; `framed comparison: paper PASS`; `A5 surjectivity: YES conditional on LMFDB model, candidate`; `cross-checked/verified: pending`。
