# 影工房 第 7 便返信 — T2・E2・Guillot 比較写像・実装ゲート監査

## 結論

### (a) 定理 T2

- **T2(i)–(iv) 本体は合格**する。照合ノートが原文画像で固定した
  \[
  c=\Delta^2,\quad \delta^3=\Delta^2,\quad
  B_3\cong\langle\Delta,\delta\mid\Delta^2=\delta^3\rangle
  \]
  と共役作用の向きにずれはない。二つの hexagon を
  \[
  (\bar\Delta f)^2=1,\qquad
  (\bar\delta^{-1}\bar Y^m f)^3=1
  \]
  と読む辞書も正しい。
- **系 T2-A は要修正**である。三角群の関係は
  \(\operatorname{ord}(b^{-1}a)\mid2k\) しか保証しない。\(N_{\rm ord}=k\) と一対一にするには
  \[
  \boxed{\operatorname{ord}_Q(b^{-1}a)=2k}
  \]
  をデータへ追加し、marked quotient の同型を法として述べる必要がある。
- 系 T2-B の torsion 分解は合格する。ただし \(\langle g,r\rangle=Q\) と shadow の生成性の関係は本文自身が「同値に近い」としか述べていないので、実装では従来の
  \[
  \langle X^u,f^{-1}Y^u f\rangle=P
  \]
  を正本判定として残す。

### (b) E2 攻撃

- **E1 は合格**する:
  \[
  \theta\tau\theta=\iota_X\tau^{-1},\qquad
  \theta\sigma\theta^{-1}=\iota_{X^u}\sigma^{-1}.
  \]
- **E2 は現文の必要十分形では不合格**である。掲載計算が証明するのは、指定された自然な候補
  \[
  \sigma_A=\sigma^{-1}\theta
  \]
  に対する同変性が \(X^u\in C_P(A)\) と同値、という主張である。「何らかの \(\sigma_A\in\operatorname{Aut}(A)\) が存在するなら必ず中心化」という必要性は証明されていない。捻れ作用は一般に faithful でない。
- charming な \(u\) では \(X^u\in C_P(A)\iff X\in C_P(A)\)。さらに \(\theta(X)=Y\) なので、許容対象ではこれは
  \[
  A=P'\le Z(P)
  \]
  すなわち **class \(\le2\)** と正確に同値である。「class 3 にはほぼ届かない」ではなく「この条件のままでは class 3 に全く届かない」。
- E3 は上の限定版 E2 のもとで合格する。E4 の Frobenius 指標和、E5、E6 も合格する。
- **\(N(v_m)=0\) は即 fake witness ではない。** 正しくは「その N、その \(m\) で同時 hexagon 解がない」、すなわち \(m\notin\mathfrak M(N)\) を証明する片側フィルタである。fake を確定するには、粗い対象 K の具体的 shadow と、許される **全 m-lift** の欠落、reduction 像、H3 の仮定または直接列挙が要る。

### (c) Guillot 比較写像

- genus 対象
  \[
  N^{(G)}=\pi^{-1}(N_G)
  \]
  の許容性は合格する。Q8、P2、P3 が genus 対象であること、今回の marked \(A_5\) 対象が genus 外であることにも不一致はない。
- settled shadow から induced automorphism \(\alpha_{m,f}\) を作る G1、Guillot 条件 (1) を満たす G2′、Out 内 \(\theta,\delta\)-可換性を与える G3 は合格する。G2 の準同型性は groupoid の引用を待たず、(3.53) から紙上で向きを確定できる。
- Q8 で四 shadow が全て inner automorphism に落ち、\(\Phi=0\)、かつ \(GT(Q_8)=1\) という結論は合格する。ただし Guillot の \(\delta\) は Out(Q8) で **位数 2** の転置であり、位数 3 ではない。\(\theta,\delta\) という二つの転置が \(S_3\) を生成するので結論は変わらない。
- 命題 A5-Q
  \[
  B_3/N_A\cong A_5\times S_3
  \]
  と 360 点 fixture は合格する。S3 座標のラベルは標準 braid 射影と同時共役の関係にあることを明記すべきである。

### (d) 実装ゲート

**現行文面のままは NO-GO。下記の局所修正後は GO** と裁定する。

止める項目は次の四つである。

1. T2-A に exact-order 条件と marked-isomorphism 規約を追加する。
2. E2 を「canonical \(\sigma_A=\sigma^{-1}\theta\) に対する同値」へ弱める。
3. `N(v_m)=0` / `intersection_size=0` の出力名を `m_missing` とし、単独で `fake_witness=true` を出さない。
4. A1 の `settled[m]` を、既知の正確な \((m,f)\) ごとの `known_solutions[i].settled=true` へ変更する。

七段、合計 25200 B3 点、順序
\[
1a\to1b\to2a\to2b\to A1\to A2\to3
\]
と W35 cap は妥当であり、上の修正のために対象や順序を組み直す必要はない。

---

## 個別所見

### F1【軽微】T2 の trefoil 土台は閉じてよい

照合ノートの D1–D3 は正しい。

\[
\sigma_1=\delta^{-1}\Delta,\qquad
\sigma_2=\Delta^{-1}\delta^2.
\]

v3 が用いる \(\sigma_2=\Delta\delta^{-1}\) も

\[
\Delta\delta^{-1}
=\Delta^{-1}\Delta^2\delta^{-1}
=\Delta^{-1}\delta^2
\]

なので同じ元である。braid 関係から \(\delta^3=\Delta^2=c\) が出て、二つの表示は互いに逆写像を持つ。ページ画像照合済みの B3 表示を土台にした導出として【GAP-E10】は閉鎖可能である。

### F2【提案】T2(iii) の二同値は採用してよい

\(\bar\Delta^2=1\) より

\[
(\bar\Delta f)^2
=\bar\Delta f\bar\Delta f
=\theta(f)f,
\]

従って最初の同値は正しい。

\(h=\bar Y^m f\) と置き、\(\bar\delta^{-1}w=\tau^{-1}(w)\bar\delta^{-1}\) を三回用いれば

\[
(\bar\delta^{-1}h)^3
=\tau^{-1}(h)\tau^{-2}(h)\tau^{-3}(h)
=\tau^2(h)\tau(h)h.
\]

これは簡約 hexagon (3.11) そのものであり、\(E_m\mathcal N_m(f)=1\) への変形とも一致する。積の順序・逆元のずれはない。

### F3【要修正】T2-A には exact order が必要

現行の三角群 quotient は

\[
(b^{-1}a)^{2k}=1
\]

しか課さないので、実際の \(\operatorname{ord}(b^{-1}a)\) が \(2d\)、\(d\mid k\) である対象も混入する。その逆構成で得る N は \(N_{\rm ord}=d\) であって k ではない。

正しい形は次である。

> \(c\in N\)、\(N_{\rm ord}=k\) なる許容 N と、
> \[
> \varphi:\Delta(2,3,2k)\twoheadrightarrow Q,\qquad
> \epsilon:Q\twoheadrightarrow S_3
> \]
> で \(\epsilon\varphi\) が標準 modular 射影、かつ
> \[
> \operatorname{ord}_Q(\varphi(b^{-1}a))=2k
> \]
> を満たす **marked quotient の同型類**とは一対一に対応する。

この修正を入れれば掃引宇宙の書き換えは有効である。

### F4【軽微】S3 marking は同時共役を明記せよ

標準規約 \(\sigma_1\mapsto(12),\sigma_2\mapsto(23)\) なら

\[
\Delta\mapsto(13),\qquad\delta\mapsto(123).
\]

文書の \(a\mapsto(12),b\mapsto(123)\) では

\[
b^{-1}a\mapsto(23),\qquad ab^{-1}\mapsto(13),
\]

となり、標準 pair の同時共役である。PB3 の核は同じなので数学は壊れないが、「標準射に等しい」と「標準射と同時共役」は schema で区別する。A5-Q でも同じ一行を添えるべきである。

### F5【軽微】T2-B の torsion 判定と生成判定を混ぜない

\[
g=\bar\Delta f,\qquad
r=\bar\delta^{-1}\bar Y^m f,\qquad
v_m=\bar\delta^{-1}\bar Y^m\bar\Delta^{-1}
\]

なら \(r=v_mg\)。従って

\[
m\in\mathfrak M(N)
\iff
v_m\in T_3(T_2\cap\bar\Delta A)
\]

は正しい。

一方、\(\langle g,r\rangle=Q\) と shadow の全射性との厳密な同値は本文では証明されていない。証明書では torsion test を h10/h11、生成性を従来の marked generators test として独立に走らせる。`generation_pass` は boolean ではなく、複数解がある場合に備え `generation_pass_count` または候補ごとの欄とする。

### F6【提案】E1 は紙上補題として採用

自由群生成元上で

\[
\theta\tau\theta(X)=Z^X,\qquad
\theta\tau\theta(Y)=X
\]

であり、これは \(\iota_X\tau^{-1}\) と一致する。

\[
\sigma=\iota_{Y^m}\tau,\qquad
\sigma^{-1}=\iota_{X^{-m}}\tau^{-1}
\]

を代入すると

\[
\theta\sigma\theta
=\iota_{X^{m+1}}\tau^{-1}
=\iota_{X^{2m+1}}\sigma^{-1}.
\]

右共役 \(\iota_g(w)=g^{-1}wg\) の合成順にも問題はない。E1 は【GAP-E2】のずれを正確に同定している。

### F7【重大】E2 の「ある \(\sigma_A\) が存在 iff」は証明されていない

捻れ作用を

\[
\lambda(a)(f)=\sigma(a)^{-1}fa
\]

と書く。掲載計算から、\(c=\sigma^{-1}\theta(a)\) に対して

\[
\rho(\lambda(a)f)
=\sigma(c)^{-1}\rho(f)X^{-u}cX^u.
\]

従って

\[
\rho\lambda(a)=\lambda(\sigma^{-1}\theta(a))\rho
\quad(\forall a)
\]

と
\[
X^u\in C_P(A)
\]
は同値である。ここまでは正しい。

しかし \(\lambda\) は一般に faithful ではない。実際

\[
\ker\lambda
=Z(A)\cap\operatorname{Fix}(\sigma).
\]

従って別の \(\sigma_A\) が同じ置換作用を与える可能性を排除できず、「何らかの \(\sigma_A\in\operatorname{Aut}(A)\) が存在するなら中心化」という必要性は掲載証明から出ない。

命題名を次へ直せばよい。

> **E2′.** canonical candidate \(\sigma_A=\sigma^{-1}\theta\) によって \(\rho\) が同変であることと \(X^u\in C_P(A)\) は同値。このとき \(\sigma_A^2=1\)。

一般の存在必要条件は UNKNOWN として残す。

### F8【要修正】中心化条件は class 2 と正確に同値

charming より \(\gcd(u,k)=1\)。\(uv\equiv1\pmod k\) を取れば

\[
X=(X^u)^v.
\]

従って \(X^u\) が A を中心化すれば X も中心化する。\(\theta(A)=A\)、\(\theta(X)=Y\) より Y も A を中心化する。X,Y が P を生成するので

\[
X^u\in C_P(A)
\iff
A=P'\le Z(P)
\iff
\operatorname{class}(P)\le2.
\]

よって Glauberman のこの route は class 3 に「ほぼ」届かないのではなく、この仮定のままでは**厳密に届かない**。E3 は H6 の別証明として位置づけるのが正しい。

### F9【軽微】E3 は限定版 E2 の下で合格

A が可換なら \(\sigma^3=1\)、ノルムは

\[
\mathcal N=1+\sigma+\sigma^2.
\]

\(\theta\sigma\theta=\sigma^{-1}\) の下で \(\mathcal N\theta=\theta\mathcal N\)。\(\rho(f)=-\theta(f)\) と加法表記すれば

\[
\mathcal N(f)=-E_m
\Longrightarrow
\mathcal N(\rho f)=\theta(E_m).
\]

\(\theta(E_m)=-E_m\) なら \(\rho\) は \(\mathcal S_m\) を保つ。A は仮定から既に可換なので、可解性に Feit–Thompson を持ち出す必要はない。coprime Glauberman により \(\rho\)-固定点が存在し、これは \(\theta(f)=f^{-1}\) と同値である。

### F10【提案】E4 の Frobenius 公式は正しい

\[
z_2=\sum_{g^2=1}g,\qquad z_3=\sum_{r^3=1}r
\]

は中心元で、既約表現 \(\chi\) 上の scalar は

\[
\frac{S_2(\chi)}{\chi(1)},\qquad
\frac{S_3(\chi)}{\chi(1)}.
\]

中心元の係数復元を \(z_3z_2\) に適用すると

\[
N(w)
=\frac1{|Q|}
\sum_{\chi\in\operatorname{Irr}(Q)}
\frac{S_2(\chi)S_3(\chi)}{\chi(1)}
\overline{\chi(w)}.
\]

係数 \(\chi(1)\) の過不足はない。S3 の照合値 \(N(1)=1,N((12))=3\) も一致する。

### F11【重大】\(N(v_m)=0\) のラベルは `m_missing` であって fake ではない

\[
n_m\le N(v_m)
\]

なので

\[
N(v_m)=0\Longrightarrow n_m=0
\Longrightarrow m\notin\mathfrak M(N)
\]

は正しい。しかし fake は**粗い対象の既存 shadow**が指定した細分へ持ち上がらないという相対概念である。

一般の \(M=K\cap N\) では、一つの \(m\in\mathcal X_N\) が欠けても、同じ \(m_0\bmod K_{\rm ord}\) を持つ別の
\[
m'\in\mathcal X_M\cap\mathfrak M(N)
\]
が存在すれば K-shadow は持ち上がる。従って fake の証明には次が必要である。

1. 粗い K の具体的 shadow \([m_0,f_K]\)。
2. \(m_0\) の許容される全 lift \(m'\) に対する欠落。
3. H3 の仮定または fiber product の直接解析。
4. W34 の完全 reduction 像。

実装は `frobenius_zero=true`、`m_missing=true` までは自動出力してよいが、`fake_witness=true` は上の四項が揃った別 certificate に限る。

### F12【軽微】E5・E6 は合格

全 factorization を H=Q/A の layer で分割した和が N(v) なので、\(\Lambda_H(\bar v)\) が一点ならその唯一の layer が \(n_m=N(v_m)\) となる。E5 は正しい。

P=A が完全なら H=S3。ここで \(\bar v_m\) は奇置換である。\(r\in A_3\) の三通りを選ぶと

\[
g=r^{-1}\bar v_m
\]

は必ず転置になり、逆に全解がこの形なので \(|\Lambda_H|=3\)。E6 に不一致はない。

### F13【提案】成層数には既に正確な行列値 Fourier 公式がある

\[
C:=\bar\Delta A,\qquad
z_{2,C}:=\sum_{\substack{g\in C\\g^2=1}}g
\]

と置けば、欲しい数は単に

\[
n_m=[v_m](z_3z_{2,C})
\]

である。\(z_{2,C}\) は一般に中心でないが、Wedderburn Fourier 反転により

\[
\boxed{
n_m=
\frac1{|Q|}
\sum_{\chi\in\operatorname{Irr}(Q)}
S_3(\chi)\,
\operatorname{Tr}\!\left(
\rho_\chi(z_{2,C})\rho_\chi(v_m^{-1})
\right)}
\]

が得られる。これは scalar character table だけの公式ではないが、正確で有限・実装可能である。文献要請 4 は「この行列値式を spherical/relative character の scalar 式へ落とす既知理論があるか」と絞るとよい。

### F14【提案】genus 対象の許容性と G4 は採用

\(N_G\) を定義する kernel の族は Aut(F2) で置換されるので、その交わりは characteristic。従って \(N^{(G)}\) は常に許容で c を含む。

- Aut(G) が ordered generating pairs に推移的なら、全 epimorphism の kernel は同一。
- G が rank-2 relative free なら、任意の epimorphism は有限 G の surjective endomorphismを経て automorphism になるので kernel は verbal subgroup。
- Q8 は生成対 24 個、Aut(Q8) も 24 で単純推移。
- P2/P3 は relative free。
- A5 には元の位数型が異なる生成対軌道があり、今回の \((5,5,5)\) kernel は全 kernel の交わりではない。

従って G4 の三対象と A5 除外は正しい。ただし「genus 対象である最小の三つ」という最小性は証明していないので、「今回比較する三つ」と書く。

### F15【提案】G1・G3・G2′ は合格、G2 の向きも紙で閉じる

settled なら

\[
\ker(T|_{F_2})=\bar N
\]

なので \(\alpha_{m,f}\) は P の自己同型へ降りる。m と f の代表独立性も正しい。

G3 は

\[
\alpha\circ\operatorname{Ad}(\bar q)
=\operatorname{Ad}(T(q))\circ\alpha
\]

から、T(q) と q の S3-coset が同じことを使えば、Out(P) で \([\alpha]\) が \(\theta,\delta_{\rm Guillot}\) と可換する。正しい。

G2′ も、配達 02 の「ある k が \(|P|\) と素」という存在量化の下で正しい。\(e=\operatorname{ord}(X)\) とし、k を

\[
k\equiv u\pmod e,\qquad k\not\equiv0\pmod p\quad(p\mid|P|,\ p\nmid e)
\]

となるよう CRT で選べばよい。

準同型性は (3.53) から直接閉じる。二元を \((m_i,f_i)\)、対応する自己同型を \(\alpha_i\) とすると

\[
\alpha_1\alpha_2(Y)
=\bigl(f_1\alpha_1(f_2)\bigr)^{-1}
Y^{u_1u_2}
\bigl(f_1\alpha_1(f_2)\bigr),
\]

これは積の f 成分 \(f_1E_{m_1,f_1}(f_2)\) と一致する。従って文書の積規約では

\[
\alpha_{\xi_1\circ\xi_2}=\alpha_{\xi_1}\circ\alpha_{\xi_2}.
\]

【GAP-G1】は原文の向き確認ではなく、この一行を本文へ入れて閉じられる。

### F16【軽微】Q8 の \(\delta\) の位数だけ訂正

Out(Q8) は三つの軸

\[
\{\pm i\},\{\pm j\},\{\pm k\}
\]

の置換として S3 である。\(\theta\) は i,j 軸を交換する転置。Guillot の

\[
\delta:i\mapsto-k,\quad j\mapsto j
\]

は i,k 軸を交換する**別の転置**で、Out で位数 2 である。この二転置が S3 全体を生成するため

\[
C_{\operatorname{Out}(Q_8)}(\langle\bar\theta,\bar\delta\rangle)
=Z(S_3)=1.
\]

従って \(GT(Q_8)=1\) は正しい。

四 shadow の \(\alpha\) は id または
\[
i\mapsto-i,\quad j\mapsto-j=\operatorname{Ad}(k),
\]
なので全て inner。従って
\[
\Phi:GT(N_Q)\ (4\text{ 元})\longrightarrow GT(Q_8)=1
\]
は零写像である。数値 fixture は合格する。

### F17【軽微】A5-Q の direct product は合格

\[
\bar\Delta=(s,\zeta),\qquad
\bar\delta=(t,\rho)
\]

で \(s^2=t^3=1\)、\(\zeta^2=\rho^3=1\) なので trefoil 表示から準同型ができる。

\[
(\bar\delta^{-1}\bar\Delta)^2=(X,1),\qquad
(\bar\Delta\bar\delta^{-1})^2=(Y,1)
\]

だから PB3 の像は \(A_5\times1\)。S3 座標も全射なので全像は \(A_5\times S_3\)。S3 座標が標準 braid 射影と同時共役であるため、kernel は PB3 内で、その PB3 との交わりは正確に \(N_A\)。従って

\[
B_3/N_A\cong A_5\times S_3,\qquad |B_3:N_A|=360
\]

が閉じる。

### F18【提案】25200 点・順序・cap は合格

\[
48+1296+192+768+20736+360+1800=25200
\]

で不一致はない。軽い既知較正から始め、A1/A2 を最大の M3 より前に置く順序は合理的である。各段 10 分、集約 30 分、2GB、二乗 Cayley 表禁止も 8GB 環境に適合する。

ただし「最終表」は v2 §3.3 への参照を残さず、七段を一つの canonical manifest にまとめるべきである。各段について少なくとも次を同じ場所に固定する。

- target hash と marked generator images
- PB3 index / B3 points / ord / charming set
- derived order / candidate total
- c の生死と evaluation mode
- expected relation count / generation count / GT count または UNKNOWN
- reduction target / expected image / fiber / kernel
- isolated status と根拠
- cap と撤退条件

### F19【要修正】A1 の `settled[m]` は量化が曖昧

一つの m に未知の f が複数あり得る。従って

```text
settled[m] = true
```

は「その m の全 shadow が settled」と誤読され、isolated UNKNOWN と衝突する。

正しい schema は例えば

```text
known_solutions[i] = {
  m: ...,
  f_canonical: ...,
  solution_hash: ...,
  hexagon: true,
  generation: true,
  settled: true,
  automorphism_witness: ...
}
known_solution_count = 4
gt_count = UNKNOWN
isolated = UNKNOWN
```

である。`gt_count_lower_bound` は JSON 文字列 `">=4"` でなく、`known_solution_count: 4` から導出するか、`{"relation":"ge","value":4}` と canonical に表す。

### F20【軽微】A2 から A1 への全射は正しいが根拠を強めよ

現文の「A1 の既知四解が持ち上がる」だけでは未知の A1-shadow を覆わない。しかし結論は一般に証明できる。

任意の A1-shadow \([m,f_A]\) を取る。A5 は完全なので f は \([F_2,F_2]\) の語で代表でき、その C5 成分は 1 である。N5 側の hexagon は可換商なので自動。生成部分群は A5 と C5 の両射影へ全射し、両群に共通商がないので A5×C5 全体である。従って全 A1-shadow が一意に A2 へ持ち上がる。

逆向きの reduction は明らかなので、集合として

\[
GT(A2)\xrightarrow{\sim}GT(A1)
\]

である。両対象の isolated 性が未知な間は、これを群同型とは呼ばない。封印 payload には

```text
R_to_NA.set_surjective = true
R_to_NA.set_bijective = true
R_to_NA.group_homomorphism = UNKNOWN
gt_count_A2_equals_gt_count_A1 = true
```

と書ける。

---

## 実装ゲートの修正チェックリスト

| # | 修正 | 現裁定 |
|---|---|---|
| G-01 | T2-A に `exact_order_binv_a = 2*k` | **必須** |
| G-02 | marked S3 map を固定し、同時共役なら schema に記録 | **必須** |
| G-03 | E2 を canonical-equivariance 版へ弱める | **必須** |
| G-04 | `frobenius_zero` / `m_missing` と `fake_witness` を分離 | **必須** |
| G-05 | `generation_pass` を count または candidate 別にする | **必須** |
| G-06 | `settled[m]` を exact \((m,f)\) witness 別へ変更 | **必須** |
| G-07 | 七段の universe/expectation を一つの manifest に統合 | **実装発注前に必須** |
| G-08 | A2→A1 の根拠を F20 の全 shadow 論法へ差し替え | **必須** |
| G-09 | Q8 の Guillot \(\delta\) を order 2 と修文 | 比較ノート修正 |

**G-01〜G-08 が反映された差分を falsifier が確認した時点で GO。** 数学対象、25200 点、実装順、cap 自体には再設計を要する問題はない。

---

## ★ 教材

1. **presentation の関係と exact order は別物**: \((b^{-1}a)^{2k}=1\) から order \(2k\) は出ない。
2. **自然な同変写像の必要十分性と、任意の同変写像の存在必要十分性は別物**: 非 faithful な作用では特に分ける。
3. **障害の検出と fake witness は別物**: \(m\)-欠損は、粗い shadow と全 lift の量化を加えて初めて fake になる。
4. **settled は \((m,f)\) の性質**: m だけを key にすると未知の別 f へ量化が広がる。
5. **outer の元の位数は生成元の記号から推測しない**: B3 の \(\delta\) は 3-torsion、Guillot の \(\delta=\tau\theta\) は reflection である。

---

## 監査範囲外の申告

- Sol の役割規律に従い、GAP、node、Python、Lean の計算・実装は行っていない。25200 点と各 fixture は紙上式を突合した。
- T2 の土台には、指定されたページ画像照合ノートを証拠として用いた。PDF を再レンダリングしていない。
- 外部検索は行っていない。文献配達 02 の翻訳を供与文献として用いた。
- Guillot 条件 (1) の原文英語の量化子は未照合である。G2′ は配達 02 の「存在する k」という翻訳を前提に合格とした。
- hunter の「A5 が位数最小」「次点 PSL(2,8)」という悉皆数値は再計算していない。
- A1 の全 shadow 数と isolated 性は UNKNOWN のままである。
- A5 の四 automorphism witness は文書の明示置換との整合を紙上確認したが、全 Aut(A5) を列挙していない。
- 今便に Lean verified の主張はない。

---

## 考察と提案

P69【T2-A】掃引宇宙を `exact_order(b^-1*a)=2*k` 付き marked triangle quotient の同型類として定義し直す。

W51【order】triangle relation が与える「位数が割る」を「位数が等しい」と読まない。

P70【T2-B】torsion factorization count と marked-generator generation count を別 certificate にする。

P71【土台閉鎖】照合ノートを根拠に【GAP-E10/G2 同根項目】を閉じ、導出式 D1–D3 を正本ノートへ参照する。

W52【生成性】\(\langle g,r\rangle=Q\) を実装の正本判定に昇格するのは、従来の shadow 生成条件との同値証明後に限る。

P72【E1】\(\theta\sigma\theta=\iota_{X^u}\sigma^{-1}\) を E2 障害の紙上補題として CLAIMS に載せる。

W53【E2】「canonical action の同変性」と「何らかの action automorphism の存在」を区別し、後者は UNKNOWN に戻す。

P73【class 2】\(X^u\in C_P(A)\iff P'\le Z(P)\) を系として明記し、Glauberman route の射程を正確に閉じる。

P74【相対指標式】F13 の \(z_{2,\Delta A}\) を用いた行列値 Fourier 公式を文献要請 4 の基準式にする。

W54【fake 語彙】`m_missing` を fake と呼ばない。fake certificate は粗い shadow、全 lift、reduction 像を必須にする。

P75【E6】完全群では三 layer を明示し、A5 のどの layer が指定 \(\bar\Delta\) かを certificate に残す。

P76【genus】Q8/P2/P3 を「今回の genus 比較三対象」と呼び、未証明の最小性は言わない。

P77【比較準同型】G2 は (3.53) の一行計算で向きを固定し、数値較正に論理決着を委ねない。

W55【delta 記号】B3 の \(\delta_B=\sigma_1\sigma_2\) と Guillot の \(d_G=\tau\theta\) を別記号にし、order 3/2 の混同を防ぐ。

P78【Q8】\(\Phi:4\to1\) を比較配管の第一較正として採用し、情報量ゼロであることも併記する。

P79【A5-Q】S3 marking の同時共役を schema に固定した上で、360 点 fixture を採用する。

P80【manifest】七段の対象定義・全 fixture・期待値・UNKNOWN・cap を一つの canonical manifest へ統合する。

W56【ゲート】現行 workorder は G-01〜G-08 反映まで dispatch しない。

P81【封印】A1 は m でなく exact known solution を key にして settled witness を封印する。

P82【A2】A2→A1 は既知四解でなく全 A1-shadow に対する集合全単射として紙上補題化する。

W57【群語彙】A1/A2 が isolated と確定するまで GT(A1), GT(A2) の集合全単射を群同型と呼ばない。

P83【cap】各段 10 分・集約 30 分・2GB・BFS/Int32Array の四条件を manifest の機械可読欄にする。

P84【falsifier】各段の fixture mismatch で即停止し、後段の既知値を使った補正を禁止する。

W58【集約 cap】七段それぞれが 10 分以内でも、合計 30 分を超えた時点で残りを UNKNOWN に倒す。

P85【文献要請4】relative Frobenius の探索語を「非中心 group-algebra element の Fourier inversion / Hecke centralizer algebra / prescribed quotient coset」に絞る。

P86【文献要請5】全 torsion 集合の積が群を覆う結果と、指定 coset layer が正である結果を区別して配達してもらう。

W59【状態札】行列値公式が紙で書けても scalar character-table formula や漸近正値性が得られたとは記帳しない。

P87【Lean 候補】T2(iii) の二 torsion 恒等式、E1、A5-Q の生成元等式を有限代数の初弾候補にする。

P88【条件付き GO】G-01〜G-08 の修文を falsifier が再読して PASS したら、対象・順序を変えず implementer へ渡す。

W60【状態】T2/E1/E4/G1/G3/Q8/A5-Q は今便の紙上相互監査段階であり、Lean までは verified と呼ばない。
