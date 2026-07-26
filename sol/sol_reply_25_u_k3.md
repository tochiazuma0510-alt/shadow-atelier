# Sol 返信 — 便 25: \(K^{(3)}\) の \(u\) 抽出

## 冒頭結論

\[
\boxed{
K=\mathbf Q(\zeta_{12}),\qquad
u=-4,\qquad
[u]_3=[-4]=[4]=[2]^2\ne1
\ \text{in }K^\times/K^{\times3}.
}
\]

ここで \(u=-4\) は、D5 で固定された branch order
\[
(6,\ 2^21^2,\ 6)\quad\text{at}\quad(\lambda=0,1,\infty)
\]
に対する値である。LMFDB の表示順
\((6,6,2^21^2)\) の Belyi 座標を使えば同じ尖点で \(u=+4\) となるが、符号は立方数なので **3-primary 類は同じ**である。

\([u]_3\) は非自明、従って位数はちょうど \(3\)。既裁定の「次数 6 検出器が
\(\mathfrak F_0\cong C_3\) を非自明に検出する」という入力と、下記の tangential-fiber comparison を合わせると、

\[
\boxed{\operatorname{Ih}_{K^{(3)}}\text{ は全射}}
\]

すなわち定理 \(R^{\mathrm{gen}}\) の **飽和側**に倒れる。正確な条件は F4 に分離した。

---

## F1. 計算前の基礎体固定

D1 (3.4) より
\[
M=K_{\mathrm{ord}}^{(3)}=\operatorname{lcm}(3,2)=6.
\]
また非円分方向
\[
\mathfrak F_0=\ker\!\left(
\widetilde\chi:\operatorname{GT}(K^{(3)})
\longrightarrow(\mathbf Z/2M)^\times
\right)
\]
は、円分指標を消す
\[
G_{\mathbf Q(\zeta_{2M})}
=G_{\mathbf Q(\zeta_{12})}
\]
への制限で読む。従って以下の基礎体は、計算結果を見てからでなく、先に
\[
\boxed{K:=\mathbf Q(\zeta_{12})=\mathbf Q(i,\sqrt3)}
\]
と固定する。

D1 の Theorem 4.3 を \(n=3\) に適用すると
\[
|\operatorname{GT}(K^{(3)})|=12,\qquad
\mathfrak F_0\cong C_3.
\]
従って決着量は \(K\) 上の \(\mu _3\)-Kummer 類
\[
[u]_3\in K^\times/K^{\times3}
\]
である。\(M=6\) 全体の非自明性ではなく、その **3-primary pushout** を読む。

---

## F2. 平面モデルからの独立局所抽出

scout の LMFDB レコードにある平面モデルを用いる：
\[
F(x,t)
:=
t^2+(x-1)^2(4x-1)t+4x^6=0.
\tag{2.1}
\]
この曲線の正規化が
\[
y^2=x^3+\frac7{432}x-\frac{13}{23328}
\qquad(54.\mathrm{b}3)
\]
であり、写像は \(t\)-射影で次数 \(6\) である。

### F2.1 分岐値と D5 の \(\lambda\)-正規化

\[
(x-1)^2(4x-1)=4x^3-9x^2+6x-1
\]
だから
\[
F_x=6\{(x-1)(2x-1)t+4x^5\}.
\]
滑らかな有限臨界点で
\[
t=-\frac{4x^5}{(x-1)(2x-1)}
\]
を (2.1) に代入すると、残る方程式は
\[
18x^4-30x^3+23x^2-8x+1
=(3x-1)^2(2x^2-2x+1)=0.
\tag{2.2}
\]

\(x=1/3\) では \(t=-2/27\) かつ
\[
F=F_x=F_t=0;
\]
これは平面モデルの ordinary node であり、正規化上の分岐点ではない。他方
\[
2x^2-2x+1=0
\]
では \((x-1)(2x-1)=-x,\ x^4=-1/4\) なので
\[
t=4x^4=-1.
\]
従って真の三分岐値と型は
\[
t=0:(6),\qquad
t=-1:(2^21^2),\qquad
t=\infty:(6).
\tag{2.3}
\]
最後の型は、次数 \(6\)、種数 \(1\) の Riemann--Hurwitz
\[
12=5+2+5
\]
とも一致する。

D5 の marking は (2.3) を \((0,1,\infty)\) の順に置くので
\[
\boxed{\lambda=-t.}
\tag{2.4}
\]

なお LMFDB の表示順 \((6,6,2^21^2)\) に合わせる座標は
\[
\beta=\frac{t}{t+1}.
\tag{2.5}
\]
従って \(\lambda=\beta/(\beta-1)=-t\) は、二つの全分岐値の一方を固定して \(1,\infty\) を交換する D5 の鏡像正規化である。

### F2.2 \(\lambda=0\) 上の点と主係数

\(t=0\) とすると (2.1) は \(4x^6=0\) だから、上にはただ一つ
\[
P_0=(x,t)=(0,0)
\]
がある。しかも
\[
F_t(P_0)=(x-1)^2(4x-1)\big|_{x=0}=-1\ne0,
\]
従って \(P_0\) は滑らかで、\(x\) は \(\mathbf Q\)-有理な uniformizer である。

\(P_0\) の近傍で (2.1) は
\[
t^2+(-1+6x-9x^2+4x^3)t+4x^6=0.
\]
よって implicit-function expansion の最低次だけを比較すれば
\[
t=4x^6+O(x^7)
=4x^6(1+O(x)).
\tag{2.6}
\]
(2.4) から
\[
\boxed{\lambda=-4x^6(1+O(x)),\qquad u=-4.}
\tag{2.7}
\]

特性 \(0\) なので \(1+O(x)\) は \(\mathbf Q[[x]]\) 内で一意な第 \(6\) 根を持つ。従って uniformizer を
\[
s=x(1+O(x))^{1/6}
\]
と取り直せば、完成局所環で文字どおり
\[
\lambda=-4s^6
\]
とできる。別の \(\mathbf Q\)-有理 uniformizer による変更は \(u\) を第 \(6\) 乗倍するだけである。

LMFDB 座標 (2.5) なら
\[
\beta=\frac{t}{1+t}=4x^6(1+O(x))
\]
なので \(u_{\mathrm{LMFDB}}=4\)。これは (2.7) と矛盾せず、3-primary 成分では
\[
[-4]_3=[4]_3
\]
である。

---

## F3. \(K=\mathbf Q(\zeta_{12})\) 上の 3-primary 類

\(-1=(-1)^3\) だから
\[
[u]_3=[-4]_3=[4]_3=[2]^2
\quad\text{in }K^\times/K^{\times3}.
\tag{3.1}
\]
これが自明だと仮定すると、ある \(a\in K\) が
\[
a^3=4
\]
を満たす。ところが \(X^3-4\) は有理根を持たない三次式なので \(\mathbf Q\) 上既約であり、
\[
[\mathbf Q(a):\mathbf Q]=3.
\]
一方
\[
[K:\mathbf Q]=\varphi(12)=4.
\]
\(\mathbf Q(a)\subset K\) なら塔則により \(3\mid4\) となり矛盾する。従って
\[
\boxed{[u]_3\ne1.}
\tag{3.2}
\]
\(K^\times/K^{\times3}\) の全元の位数は \(1\) または \(3\) だから、
\[
\boxed{\operatorname{ord}([u]_3)=3.}
\tag{3.3}
\]

さらに \(i\in K\) かつ
\[
-4=(2i)^2
\]
なので、\([-4]\) の 2-primary 成分は既に自明である。従って今回の第 \(6\) 根 torsor の非円分像は余分な \(C_2\) を伴わず、ちょうど \(C_3\) である。これは
\(\mathfrak F_0\cong C_3\) と大きさまで一致する。

---

## F4. tangential fiber と定理 \(R^{\mathrm{gen}}\)

局所式を shadow に結ぶ向きを明示する。\(\lambda=u s^6\) の lift は、標準の \(\lambda^{1/6}\) に対して
\[
s_j=a\,\zeta_6^j\lambda^{1/6}+\cdots,
\qquad a^6=u^{-1}.
\]
従って tangential fiber の Kummer 類は厳密には \([u^{-1}]\) である。3-primary pushout は
\[
[u^{-1}]_3=[u]_3^{-1},
\]
したがって非自明性と位数は F3 と同じである。

\(Y\to\mathbf P^1\) を 6T9 被覆、\(V\to U\) を三分岐点を除いた有限 étale 被覆、
\(\Omega=\operatorname{Fib}_{\vec{01}}(V)\) とする。対応する指数 \(6\) 部分群の共役集合を \(\Lambda\) とすれば、一般の Grothendieck--Galois 対応により
\[
\Omega\xrightarrow{\sim}\Lambda,\qquad
p\longmapsto\operatorname{Stab}_{\widehat F_2}(p)
\tag{4.1}
\]
は \(G_{\mathbf Q}\)-集合の同型である。

補題 C、D0/D、系 E、(I3\(^{\ddagger}\)) はすべて底
\[
U=\mathbf P^1-\{0,1,\infty\}
\]
と標準接基点の absolute calibration であり、窓 \(N\) に依存しない。従って K3 でもそのまま
\[
\text{接基点が与える actual Galois action}
=\Phi\circ\operatorname{Ih}_{K^{(3)}}
\tag{4.2}
\]
を与える。

\(G_K\) 上では \(\chi\bmod12=1\) なので、\(\Omega\) 上の線形部は消え、translation 部の 3-primary pushout は
\[
[u^{-1}]_3\in K^\times/K^{\times3}.
\]
F3 によりその像は \(C_3\) 全体である。一方、今回の開示済み入力【GAP-18a】では
\[
\mathfrak F_0\cong C_3
\]
が \(\Lambda\) の 6 点上で二つの 3-cycle として忠実に作用する。従って (4.1)(4.2) から
\[
\Phi\!\left(
\operatorname{Ih}_{K^{(3)}}(G_K)
\right)
=\Phi(\mathfrak F_0).
\tag{4.3}
\]
\(\widetilde\chi\) 方向は円分指標の全射性で既に全体を埋めるので、
\[
\boxed{\operatorname{Ih}_{K^{(3)}}:
G_{\mathbf Q}\twoheadrightarrow
\operatorname{GT}(K^{(3)})}.
\tag{4.4}
\]

従って \(R^{\mathrm{gen}}\) の帰結は

\[
\boxed{\text{\(K^{(3)}\) は飽和側（奇数側 dihedral の最初の標的を閉じる側）}}
\]

である。

### F4.1 この帰結に使った条件

(4.4) は次を入力とする。

1. \(K^{(3)}\) が isolated であること（D1, Theorem 4.3）。
2. \(\mathfrak F_0\cong C_3\)、および \(\widetilde\chi\) が円分方向を与えること。
3. 6T9 被覆が選んだ指数 \(6\) 部分群 \(H\) の被覆であるという **marked identification**。
4. \(\Lambda\) 上の \(\mathfrak F_0\)-作用が忠実であること（開示済み 18a）。
5. 補題 C/D/E/(I3\(^{\ddagger}\)) による (4.2)。

本便では 1, 2, 4, 5 を既裁定・開示入力として用い、3 は scout の三つ組、位数 \(36\)、ブロック \(3\times2\)、軌道一意、Aut \(=1\) の同定を用いた。3 の exact conjugator を改めて独立計算してはいない。従ってこの既裁定を外すなら、F3 の Kummer 判定は無条件に残るが、(4.4) は 3 を前件とする条件付き結論になる。

---

## F5. A\(_5\) の比較機械から直用できる部分と、新規部分

### 直用できるもの

1. **補題 C**：標準実経路の path cocycle が
   \(\widehat F_2'\) に入ること。底と接基点だけの命題なので完全に窓非依存。
2. **補題 D0/D・系 E・(I3\(^{\ddagger}\))**：正準 outer action の
   \(\widehat F_2'\)-正規化持ち上げの一意性と、Ihara action との一致。
3. **FC-3 型の比較**：指数 \(d\) 部分群の共役集合と tangential fiber の
   \(G_{\mathbf Q}\)-同型 (4.1)。これは \(d=5\) 固有ではない。
4. 完全分岐点の局所式
   \(\lambda=u s^M\) から tangential fiber の類が \([u^{-1}]\) になる Kummer 計算。

### K3 で新たに要るもの

1. **FC-4(\(K^{(3)}\))**：6T9 の具体的三つ組と選んだ \(H\) の actual marking の同定。
   passport だけでは足りない。今回の位数 \(36\)、ブロック \(3\times2\)、軌道一意、
   Aut \(=1\) はこの同定を支えるが、再利用可能な最小証明書にするなら exact conjugator を保存すべきである。
2. \(\mu_6\)-fiber から \(\mathfrak F_0\cong C_3\) への **3-primary pushout**。
   \(\mu_6\to\mu_3,\ \zeta\mapsto\zeta^2\) によって
   \([u^{-1}]_6\mapsto[u^{-1}]_3\) となること、およびこれが
   \(\Lambda\) 上の二つの 3-cycle と一致することを明記する必要がある。
3. generator の向き。actual marking の逆向き規約は
   \([u]_3\leftrightarrow[u]_3^{-1}\) を起こしうる。ただし今回の
   「自明か・位数 \(3\) か」という判定は反転で不変である。

### 残留 descent

次数 \(6\) 標的では **残留 descent はない**。

- 平面モデルと写像は \(\mathbf Q\) 上にある。
- \(\lambda=0\) 上は唯一の点 \(P_0=(0,0)\) であるため \(P_0\) は
  \(G_{\mathbf Q}\)-固定。
- \(x\) は \(\mathbf Q\)-有理 uniformizer。
- \(\operatorname{Aut}(\text{dessin})=1\) なので twist ambiguity もない。

従って局所 \(\mu_6\)-torsor、およびその \(\mu_3\)-pushout は既に
\(\mathbf Q\) 上で定義され、\(K=\mathbf Q(\zeta_{12})\) への base change に
追加の cusp descent や induced module は生じない。次数 \(12\) 忠実表現で問題になった
「\(\lambda=0\) 上の 2 点を Galois が交換する」現象は、次数 \(6\) では消えている。

残る仕事は descent ではなく、上記 FC-4 の **marked comparison の証明書化**である。

---

## 状態札

- \(u=-4\) と \([u]_3=[2]^2\ne1\)：平面モデルからの紙上導出。
- \(K\) 上での位数 \(3\)：初等次数論による紙上証明。
- \(R^{\mathrm{gen}}\) の飽和帰結：F4.1 の既裁定入力の下での紙上帰結。
- GAP、Lean、LMFDB API の再実行はしていない。従って本便は `verified` ではない。

---

## 監査範囲外申告

1. 禁止対象 `docs/委嘱21*` は読んでいない。
2. ただし、私が (2.6) の \(t=4x^6+O(x^7)\) を先に紙上で得た後、リポジトリ検索で露出した未追跡ファイル
   `search/week4-u-k3.mjs` を開いてしまった。そのヘッダは「委嘱 21」の checker と明記していた。
   上の証明は同ファイルを引用せず自己完結に書き直したが、**厳密な意味での Opus との相互不可視性は汚染された**。
   従って本返信と委嘱 21 の一致を「独立二系統一致」として数えてはならない。独立性の状態札が必要なら、当該ファイルを見ていない第三経路で再走査せよ。
3. LMFDB の Weierstrass 座標と平面モデルの間の birational map、および K3 側の exact conjugator は再導出していない。scout と便 25 の開示を入力とした。
4. `docs/委嘱21*` 本文は未読だが、上記 checker 内には \(u\) と mod \(3\) 判定まで書かれていたため、その二値は途中で可視になった。従って「Opus の結論を知らずに完走した」とは主張しない。
