# 総合判定: **条件付き PASS**

数学的な心臓については、

- **補題 C: PASS**
- **補題 D: PASS**（下記 F5 の文献入力＋初等補足を含む）
- **系 E: PASS**
- **(I3‡) から (I3*) への含意: PASS**
- **系 B′ の反転危険の除去: PASS**

である。

条件は二つで、いずれも本文への局所追記で閉じられる。

1. 補題 D が使う
   \[
   C_{\widehat F_2}(x)=\overline{\langle x\rangle}
   \tag{D0}
   \]
   を、配達済み Zalesskii–Zapata, arXiv:1711.01500,
   Proposition 4.7（p.14）と Lemma 4.2（pp.11–12）から導く
   F5 の短い補足ごと本文へ入れること。Proposition 4.7 が直接いうのは
   **meta-procyclic projective** までであり、これを単に
   “procyclic” と読み替えてはならない。
2. v3 に残った旧版の循環文言を除くこと。とくに §1.1 規約 A、
   §1.2 規約 B、§3.7 (f2) は、補題 C+D で**証明するはずの比較を先に
   仮定している**。

この二点を直せば、v3 は **紙上相互監査 PASS** に達する。
差戻しを要する数学的反例は見つからなかった。

監査対象は
`docs/week4-A5算術飽和_v3.md`
全 580 行、SHA-256
`6462BEA3B3510723295CB8F6482949D77CE4C543DB55287D76D6C3285A595DC8`
で固定した。

---

## F1. 補題 C の両端の不動点

記号を
\[
U=\mathbf P^1_{\mathbb Q}\setminus\{0,1,\infty\},\qquad
s_1=1-\beta
\]
とする。使う被覆は
\[
C_n:\ w^n=\beta,\qquad
D_n:\ u^n=1-\beta=s_1.
\]

### \(C_n\)

- \(0\vec1\) 側では
  \[
  v_0=\beta^{1/n}
  \]
  が標準係数作用で固定される。
- \(1\vec0\) 側では
  \[
  v_1=(1-s_1)^{1/n}
  =\sum_{k\ge0}\binom{1/n}{k}(-s_1)^k
  \in\mathbb Q[[s_1]]
  \]
  が定数項 1 の一意な根で、係数が全て有理数だから固定される。

とくに委嘱が指定した \(1\vec0\) 側の同定は正しい。

### \(D_n\)

- \(0\vec1\) 側では
  \[
  v_0'=(1-\beta)^{1/n}\in\mathbb Q[[\beta]]
  \]
  が固定される。
- \(1\vec0\) 側では
  \[
  v_1'=s_1^{1/n}
  \]
  が標準係数作用で固定される。

従って、両被覆の両端に必要な Galois 不動点が存在する。

---

## F2. 正実分枝の輸送は副有限化後も正しい

\(\overline{\mathbb Q}\hookrightarrow\mathbb C\) を一つ固定する。
実区間 \(0<\beta<1\) 上では
\[
\beta^{1/n}>0,\qquad(1-\beta)^{1/n}>0
\]
という正実分枝はそれぞれ一意であり、区間上で零にも極にもならない。
従って、\(1\vec0\) から \(0\vec1\) への実経路 \(p\) に沿う解析接続は
\[
p\cdot v_1=v_0,\qquad p\cdot v_1'=v_0'
\tag{2.1}
\]
を与える。

これは単なる解析的比喩ではない。Riemann existence により、\(p\) は
各有限エタール被覆の幾何繊維間の compatible transport を与え、その
逆極限が副有限 étale path である。補題 C が必要とするのは
\(C_n,D_n\) という各有限被覆上の (2.1) だけなので、有限段で確認した
正実分枝の輸送は副有限化後にもそのまま残る。

接端点については、小さい正の実半径上の分枝を
\(\beta\)-または \(s_1\)-Puiseux 展開へ送る極限として読めばよい。
新しい解析仮定は要らず、§1.1 の tangential fiber framework の範囲内で
ある。

従って委嘱 1(b) も **PASS**。外部出典を付けるならこれは
【GAP-C3】の tangential fiber framework の裏取りであり、絶対較正の
新しい数論入力ではない。

---

## F3. \(g_\sigma\) のアーベル化

\[
p:1\vec0\longrightarrow0\vec1,\qquad
g_\sigma=\sigma(p)p^{-1}\in\pi_1(U_{\overline{\mathbb Q}},0\vec1)
\]
とする。経路の積は v3 と同じ規約で読む。

\(v_0,v_1\) はそれぞれ Galois 不動で、\(p\cdot v_1=v_0\) だから
\[
\begin{aligned}
g_\sigma\cdot v_0
 &=\sigma(p)p^{-1}\cdot v_0\\
 &=\sigma(p)\cdot v_1\\
 &=\sigma(p)\cdot\sigma(v_1)\\
 &=\sigma(p\cdot v_1)
 =\sigma(v_0)=v_0.
\end{aligned}
\tag{3.1}
\]
\(C_n\) の幾何 deck 群は \(\mu_n\simeq\mathbb Z/n\) で、幾何ループの
繊維作用は
\[
\psi_{C_n}:\widehat F_2\longrightarrow\mathbb Z/n,
\qquad x\mapsto1,\ y\mapsto0
\]
による自由な平行移動である。一点を固定する (3.1) から
\[
\psi_{C_n}(g_\sigma)=0.
\]
従って \(g_\sigma\) の \(x\)-成分は \(0\bmod n\)。
\(D_n\) では同様に \(y\)-成分が \(0\bmod n\) になる。

これは全 \(n\ge2\) で成立するので
\[
\psi(g_\sigma)=0
\quad\text{in}\quad
\widehat F_2^{\mathrm{ab}}=\widehat{\mathbb Z}^2.
\]
よって
\[
\boxed{
g_\sigma\in
[\widehat F_2,\widehat F_2]^{\mathrm{top.cl.}}.
}
\]

この段には「\(\mu_n\) が \(\mathbb Q\) 上 constant でない」という障害は
ない。ここで作用させている \(g_\sigma\) は幾何基本群の元であり、
\(\overline{\mathbb Q}\) 上の cyclic deck action を見ているからである。

以上により補題 C は **完全に PASS**。

---

## F4. \(g_\sigma\) と Ihara の \(f_\sigma\)

\(x_1\) を \(1\vec0\) における 1 周りの正向き慣性とし、
\[
y=p x_1p^{-1}
\]
と置く。標準係数切断では
\[
\sigma(x_1)=x_1^{\chi(\sigma)}.
\]
また \(\sigma(p)=g_\sigma p\) だから
\[
\sigma(y)
=g_\sigma y^{\chi(\sigma)}g_\sigma^{-1}.
\]
Ihara の表示
\[
\sigma(y)=f_\sigma^{-1}y^{\chi(\sigma)}f_\sigma
\]
と比べれば
\[
f_\sigma=g_\sigma^{-1}
\]
である。左右作用規約を逆にしても逆元が入るだけで、交換子閉包への
所属は不変である。

従って補題 C は、標準係数切断の actual action が条件 (ii) を
満たすことを、絶対座標 \(\beta\) から直接証明している。便 17 の
循環はここで本当に解消された。

---

## F5. 補題 D の中心化群入力

補題 D が必要とする純群論入力を分離すると次である。

> **(D0)** 自由生成元 \(x\) に対し
> \[
> C_{\widehat F_2}(x)
> =\overline{\langle x\rangle}
> \cong\widehat{\mathbb Z},
> \]
> 同様に
> \(C_{\widehat F_2}(y)=\overline{\langle y\rangle}\)。

離散自由群の中心化群定理を無言で completion へ移すことはできない。
しかし監査中に届いた次の資料で、基底元に必要な形は閉じる。

> P. Zalesskii–T. Zapata,
> *Profinite extensions of centralizers and the profinite completion of
> limit groups*, arXiv:1711.01500,
> **Lemma 4.2, pp.11–12; Proposition 4.7, p.14**。
>
> 配達 PDF:
> `papers/delivered/zalesskii_zapata_1711.01500_profinite_extensions_centralizers.pdf`
> SHA-256:
> `6F42E953267170B7C48629D2D8BEE4427ADD24F437FAF49B6629B9DC424CB21B`。

ページ画像で照合した Proposition 4.7 の \(n=0\) の証明は、
自由副有限群 \(F\)（同論文の class \(\mathcal Z_0\)）と
\(\overline{\langle g\rangle}\cong\widehat{\mathbb Z}\) に対して
\(C_F(g)\) が **meta-procyclic projective** であることを与える。
Lemma 4.2 の用語では
\[
C_F(g)\cong\mathbb Z_\pi\rtimes\mathbb Z_\rho,
\qquad
\mathbb Z_\pi:=\prod_{p\in\pi}\mathbb Z_p
\tag{5.1}
\]
（\(\pi,\rho\) は互いに交わらない素数集合）である。これは
“procyclic” より弱いので、ここで一段の補足が要る。

いま \(g=x\) とし \(C=C_{\widehat F_2}(x)\),
\(K=\overline{\langle x\rangle}\cong\widehat{\mathbb Z}\) と置く。
\(K\subset Z(C)\) である。各素数 \(p\) に対し
\(K_p\cong\mathbb Z_p\) は非自明だから、(5.1) では
\(\pi\cup\rho\) が全素数集合になる。

\(p\in\pi\) なら、商 \(\mathbb Z_\rho\) は非自明な pro-\(p\)
部分群を持たないので、\(K_p\) は正規因子
\((\mathbb Z_\pi)_p\cong\mathbb Z_p\) の非零閉部分群であり、
従って \(p^m\mathbb Z_p\) の形の開部分群である。一方
\(K\subset Z(C)\) なので、\(\mathbb Z_\rho\) の共役作用は
\(K_p\) を各点固定する。\(\mathbb Z_p\) の自己同型は単元倍であり、
非零開部分群を各点固定するものは恒等写像だけである。よって
\(\mathbb Z_\rho\) は各 \(p\)-成分へ自明に作用し、
\[
C\cong\mathbb Z_\pi\times\mathbb Z_\rho
\cong\widehat{\mathbb Z}
\tag{5.2}
\]
は procyclic である。

最後に \(z\) を \(C\) の位相的生成元、\(x=z^a\) と書くと、
アーベル化で
\[
(1,0)=a\,\psi(z)
\quad\text{in }\widehat{\mathbb Z}^2.
\]
第一成分だけで \(a\in\widehat{\mathbb Z}^{\times}\) が従う。
従って \(x\) 自身が \(C\) を位相的に生成し、
\[
C_{\widehat F_2}(x)=K.
\]
\(y\) にも同じ議論が適用できる。さらに
\(\chi\in\widehat{\mathbb Z}^{\times}\) なので
\(\overline{\langle x^\chi\rangle}=\overline{\langle x\rangle}\)、
従って \(C(x^\chi)=C(x)\) である。

これで (D0) は **紙上 PASS**。新着資料の
“meta-procyclic” は反例ではなく、基底元の場合に上の中心性と
全素数成分を使って procyclic へ強める必要がある、という警告だった。

なお v3 の

> 「自由副有限群では非自明元の中心化群は、それを含む極大
> procyclic 部分群」

という一般文は、この配達資料だけからは出ない。補題 D に必要な
「基底元 \(x,y\)」へ主張を絞り、Proposition 4.7 と上の補足を
記すべきである。P1 追補が画像照合した Schneps p.4 §I.3 の
「\(f\in\widehat F_2'\) なる一意持ち上げ」も、補題 D の結論への
独立な文献支持になっている。

---

## F6. 補題 D の正規化計算

F5 で (D0) を確立した。残りの正規化計算も正しい。

まず canonical outer class \(\rho(\gamma)\) は 0 と 1 の慣性共役類を
それぞれ \(\chi(\gamma)\) 乗へ送る。従って、任意の lift を内共役で
調整すれば
\[
\alpha(x)=x^{\chi(\gamma)}
\tag{6.1}
\]
を満たす lift が少なくとも一つ存在し、その lift について
\[
\alpha(y)=f^{-1}y^{\chi(\gamma)}f
\tag{6.2}
\]
となる \(f\) も存在する。この**存在の一行**を v3 補題 D の冒頭に
足すべきである。

\(\widehat F_2\) の中心は自明である。実際、中心元は (D0) により
\(\overline{\langle x\rangle}\cap\overline{\langle y\rangle}\) に入り、
この交わりはアーベル化で自明である。従って同じ outer class の
lift は内共役の torsor である。(D0) と
\(\chi(\gamma)\in\widehat{\mathbb Z}^{\times}\) から
\[
C_{\widehat F_2}(x^{\chi(\gamma)})
=\overline{\langle x\rangle}.
\]
従って (6.1) を満たす lift は
\[
\operatorname{Ad}(x^a)\circ\alpha,
\qquad a\in\widehat{\mathbb Z},
\]
で尽くされる。

この lift に対する (6.2) の conjugator は
\[
f x^{-a}.
\]
同じ automorphism を表す conjugator の自由度は左から
\[
C_{\widehat F_2}(y^{\chi(\gamma)})
=\overline{\langle y\rangle}
\]
を掛けることだけなので、全候補は
\[
y^b f x^{-a},
\qquad a,b\in\widehat{\mathbb Z}.
\]
\(\psi(f)=(r,s)\) と書けば
\[
\psi(y^bfx^{-a})=(r-a,s+b).
\]
これが \((0,0)\) になるのは
\[
(a,b)=(r,-s)
\]
の一組だけである。よって正規化 lift は存在し、かつ一意。

以上から、補題 D は存在・一意性とも **紙上 PASS**。ただし v3 本文には
F5 の文献入力と補足、および本節冒頭の「存在の一行」を追記すること。

---

## F7. 系 E

標準係数切断 \(s_{0\vec1}\) の action は、

1. 局所慣性の係数作用から
   \[
   \alpha_{s_{0\vec1}}(x)=x^{\chi(\gamma)};
   \]
2. 補題 C から、その \(y\)-conjugator が
   \(\widehat F_2'\) に属する。

従って補題 D の一意正規化 lift の条件を満たす。よって
\[
\boxed{
\alpha_{s_{0\vec1}}=\alpha^{\mathrm{norm}}.
}
\]

この含意に穴はない。補題 D の一意性は各 \(\gamma\) ごとの主張だが、
標準 action も canonical outer representation も準同型なので、比較に
十分である。なお正規化条件は合成で保存され、一意性から
\(\gamma\mapsto\alpha^{\mathrm{norm}}_\gamma\) 自体も準同型になる。

系 E は **PASS**。

---

## F8. (I3‡) の強さ

v3 の (I3‡) は

1. \(\alpha^{\mathrm{Ih}}\) が canonical outer Galois action
   \(\rho\) の lift。
2. \(\alpha^{\mathrm{Ih}}(x)=x^{\chi}\)。
3. \(y\)-conjugator \(f_\gamma\in\widehat F_2'\)。

という三点である。

### 1 は落とせない

補題 D は「**同じ outer class の中で**正規化 lift が一意」という
定理である。outer class の一致を落とせば、条件 2,3 を満たす別の
Aut\((\widehat F_2)\)-値作用を排除できない。従って、抽象的な比較仮定
として 1 は不可欠である。

### ただし本件では 1 は既に原文から出る

P1 が画像照合した 2405 p.4 の文は、

> Ihara constructed a **splitting of (1.4)** that gives us an action
> of \(G_{\mathbb Q}\) on \(\widehat F_2\)

と述べる。群拡大
\[
1\to\widehat F_2\to\pi_1(U_{\mathbb Q})\to G_{\mathbb Q}\to1
\]
の任意の splitting が共役作用で与える Aut-action は、その
Out-class が canonical outer action \(\rho\) になる。これは splitting
の定義そのものである。

従って (I3‡)-1 は「残る未検証仮定」ではなく、上の原文から従う
**source-closed fact** として扱える。2 は同じページの表示式、3 は
Ih の像が \(\widehat{GT}_{\mathrm{gen}}\) に入ることとその定義から既に
閉じている。

したがって定理文では (I3‡) を仮定に残しても安全だが、より正確には

> **補題 I3‡（原文から）**: \(\alpha^{\mathrm{Ih}}\) は
> \(\rho\) の \(\widehat F_2'\)-正規化 lift である。

へ格上げできる。定理 A₅ の未閉鎖仮定として数える必要はない。

### 「(I3*) より真に弱い」について

補題 C+D を証明した後は
\[
(I3‡)\iff(I3*)
\]
である。従って **真に弱い**という表現は正しくない。
基点・速度を明示しない、より intrinsic な**同値条件**になった、
というのが正確である。

形式上は 2,3 を (I3‡) の仮定から外し、既に照合済みの事実として
前置きできる。しかし outer-class の一致そのものをさらに弱めることは
この比較路線ではできない。

---

## F9. 系 B′ の反転危険

\(s_c\) を rational rescaling とし、v3 の右積規約で
\[
f_\gamma^{(c)}
=f_\gamma x^{-\chi(\gamma)\kappa_c(\gamma)}.
\]
標準 \(s_{0\vec1}\) は補題 C により
\(f_\gamma\in\widehat F_2'\)。もし \(s_c\) も canonical outer action の
正規化 lift なら、補題 D の一意性から \(s_c=s_{0\vec1}\) の action。
同じことをアーベル化で読めば
\[
\chi(\gamma)\kappa_c(\gamma)=0
\quad\text{for all }\gamma,
\]
従って \(\kappa_c=0\)、\(c=1\) である。

したがって
\[
[b_A]_{v_c}=[2][c]^{\pm1}
\]
を自明にする危険な \(c\) は、paper Ihara action と同じ正規化 lift には
なれない。系 B′ の反転危険は **完全に除去された**。

---

## F10. 便 17 の反映検収

数学的な反映は概ね意図どおりである。

### 正しく反映されたもの

- 補題 B の指数
  \[
  f_\gamma^{(c)}
  =f_\gamma x^{-\chi(\gamma)\kappa_c(\gamma)}
  \]
  は正しい。
- 補題 B は相対一意性だけへ弱められた。
- Newton polygon の循環は除かれた。
- \(N_{A_5}(A_4)=A_4\) が FC-3 に追加された。
- exact conjugator \(h=(1\,3\,4\,5)\) が本文へ入った。
- 特殊化の転置は \(G_{\mathrm{arith}}\) の元である、と訂正された。
- FC-2a / FC-2b の分離は正しい。
- 命題 M は \(\Phi\) 単射を仮定へ上げ、一般名も
  “marked quotient の体”へ直された。
- \(u_{\mathrm{Sol}}/(-1/2)=(-9/16)^5\) と
  \(3\)-valuation の説明は正しい。

### まだ残っている旧版文言

1. **§1.1 規約 A（v3 49–51 行）**は、標準係数切断の action と
   2405 の Ihara action が同一だと最初に仮定している。これは系 E で
   後から証明する FC-2b そのものである。
2. **§1.2 規約 B（58 行）**も
   \(\Phi\circ\operatorname{Ih}_{N_A}=\beta_\gamma\) を規約として先取り
   している。
3. **§3.7 (f2) と直後（423–425 行）**は、交換子条件だけで
   スケール問題が閉じるという v2 の説明と
   【GAP-C1′】を残している。正しくは補題 C+D+(I3‡) と
   【GAP-C1″】である。
4. FC-6 の注は family-wise へ直ったが、補題の statement
   （403 行）自体にはまだ「Aut\((A_5)\)-自然」とだけある。
   statement 側を「族 \(\{\mathcal D(v)\}_v\) 上で自然」と直すべき。
5. §1.4 の見出しに `(I3**)` と `(I3‡)` が混在し、
   `1.4.4` も二度現れる。
6. 式番号 `(3.2)` が
   \[
   N_{A_5}(A_4)=A_4
   \]
   と affine action の二箇所で重複し、定理証明 6 の参照が曖昧。

最小修正は、冒頭を

- \(\alpha^{\mathrm{std}}\): 標準係数切断が定める幾何 action。
- \(\alpha^{\mathrm{Ih}}\): 2405 の表示式が定める action。

として**別々に定義**し、系 E+(I3‡) の後で初めて
\[
\alpha^{\mathrm{std}}=\alpha^{\mathrm{Ih}}
\]
と書くことである。規約 B もこの等式の帰結へ移す。

これらは補題 C+D の数学を壊さないが、「直接証明で循環を除いた」
という v3 の売りを本文の論理順でも実現するために必要である。

---

## F11. 定理 A₅ の状態

F5 の (D0) 証明を v3 へ取り込み、F10 の旧文言を整理すれば、

\[
\alpha^{\mathrm{Ih}}
=\alpha^{\mathrm{norm}}
=\alpha_{s_{0\vec1}}.
\]
従って FC-2b が閉じ、便 17 で監査済みの
FC-3、FC-4、FC-5 と合わせて
\[
\boxed{
\operatorname{Ih}_{N_A}:
G_{\mathbb Q}\twoheadrightarrow
\operatorname{GT}(N_A)\cong F_{20}
}
\]
および固定体
\[
\boxed{
\mathbb Q(\zeta_5,\sqrt[5]2)
}
\]
が従う。

補題 C は paper-specific な数値計算ではなく、標準実経路と二つの
Kummer 被覆だけから出る一般的な絶対較正補題である。ここは今後の
窓でも再利用できる。

現時点の正式札は

> **`conditional paper-proof / two-mathematician audit`**
> — 条件は F5 の文献＋補足の本文化と、循環文言の整理。

条件解除後は

> **`paper-proof / two-mathematician audit PASS`**

へ上げてよい。これは `cross-checked` や `verified` を意味しない。

---

## ★ 教材

1. **絶対較正は一つの被覆ではなく、アーベル化の二座標を検出する
   二つの被覆で閉じる。** \(w^n=\beta\) が \(x\)、\(u^n=1-\beta\)
   が \(y\) を検出する。
2. **解析接続を副有限群の中で直接操作する必要はない。**
   各有限被覆で分枝輸送を確認し、compatible transport の逆極限を
   取ればよい。
3. **正規化 lift の一意性は、outer class を固定して初めて意味を持つ。**
   \(x\)-式と交換子条件だけでは、異なる outer action 同士を比較できない。
4. **引用の結論を一語でも強めない。** “meta-procyclic” は
   “procyclic” ではない。本件では、中心に
   \(\widehat{\mathbb Z}\) を含むことが半直積作用を消し、さらに
   基底元のアーベル化が真の根を排除して、初めて
   \(C_{\widehat F_2}(x)=\overline{\langle x\rangle}\) になる。
5. **仮定を intrinsic に書き換えても、証明後に元の条件と同値なら
   「真に弱い」とは言わない。**
6. **循環を数学で直した後は、規約節に残った先取り等式も消す。**
   証明本体だけでなく文書の依存順も監査対象である。

---

## 考察と提案

P173【補題 C】補題 C を
「標準実経路の Galois path cocycle は
\(\widehat F_2'\) に入る」という独立一般補題として採用する。
証明状態は **紙上相互監査 PASS**。

P174【補題 D0】次の版へ
\[
C_{\widehat F_2}(x)
=\overline{\langle x\rangle}
\]
の根拠として Zalesskii–Zapata Lemma 4.2 + Proposition 4.7 と
F5 の初等補足を本文へ移す。Proposition 4.7 の結論を
meta-procyclic から procyclic へ無言で強めないこと。

P175【I3‡】(I3‡) を「残る仮定」でなく、2405 p.4 の splitting 文から
従う **補題 I3‡** へ移す。(i)(ii) も既に source-closed なので、
定理の仮定リストから外せる。

P176【v3 清掃】F10 の六箇所を直し、
\(\alpha^{\mathrm{std}}\) と \(\alpha^{\mathrm{Ih}}\) を系 E まで分離する。

P177【状態更新】P174/P176 完了後、定理 A₅ を
`paper-proof / two-mathematician audit PASS`
へ上げる。数値・実装の `cross-checked`、Lean の `verified` には
上げない。

W132【中心化群】自由副有限群の中心化群を、離散自由群の記憶だけで
引用なしに使わない。“meta-procyclic” と “procyclic” も区別し、
基底元で後者へ強める補足を明記する。

W133【I3 の強さ】補題 C+D の後は (I3‡) と (I3*) は同値。
「真に弱い」でなく「基点を含まない intrinsic な同値条件」と書く。

W134【規約循環】比較等式を規約 A/B で仮定してから系 E で証明しない。

W135【状態語】補題 C の紙上 PASS は機械的 `cross-checked` でも
Lean `verified` でもない。

W136【式番号】二つの `(3.2)` と二つの `1.4.4` を次版で分離する。

---

## 監査範囲外の申告

- 並列レーンの E2 作用表・証明書には触れていない。
- GAP、node、Python、Lean は実行していない。
  `search/week4-a5-audit17-check.mjs` の 11 項目も再実行していない。
- 外部 web 検索はしていない。監査中に配達された
  Zalesskii–Zapata arXiv:1711.01500 の PDF について、
  pp.5, 11–12, 14 をページ画像で照合した。Herfort–Ribes 1985
  本文は未入手のままなので、その命題番号は推測していない。
- Tangential fiber framework の一次資料全体、Deligne §15 の新規監査は
  本便の範囲外。【GAP-C3】を維持した。
- v3 の既監査部分については便 17 の結論を採用し、新規補題 C/D、
  系 E、(I3‡)、および便 17 修正の反映箇所を監査した。
- 過去返信 `sol_reply_17_a5_audit.md` は編集していない。本便で私が
  編集した成果物は `sol/sol_reply_18_lemmaCD.md` のみである。
