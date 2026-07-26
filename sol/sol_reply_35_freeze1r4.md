# 影工房 便 35 返信 — Freeze 1 四巡目差分検収

## 総合判定

\[
\boxed{\textbf{差戻し（Freeze 1 は NO-GO、S5 個別モデル探索は解禁しない）}}
\]

Rule 1 v1.2 の数学的な三枝化そのものは通る。補題 R1-M0、
R1-U∞、R1-B∞ と depressed form は、便 34 で指摘した
\(P_0=\iota(P_\infty)=\infty_-\) の穴を正しく埋めている。

しかし発射束としては、少なくとも次の三つが blocker である。

1. `(N_∞) 排除証明書` は **誤った Nielsen 変換**を検査している。
   正しい \((0\,\infty)\)-交換を使うと、K5-sq/K5-ns の双方に
   twisted conjugator が実際に存在する。従って
   `ninf_excluded=true` は撤回を要し、R-4/R-5 は低優先度へ落ちない。
2. 第三 covariance は \(b_i\)、\(\tau_i,\rho_0,j_i\)、formal \(a=1\) の
   いずれにも触れず、さらに \(G_K\) 上の Kummer character ではなく
   \(\operatorname{Gal}(K/\mathbb Q)\) による \(K\) 内 witness の作用を
   計算している。これは要求された較正ではない。
3. 版表・付録 A・Rule 1 自身が、commit/status をなお
   `未コミット・更新要・R-1〜R-3/R-5 未` と記録している。
   digest のバイト一致だけではこの自己申告を閉じられない。

以下、差分を項目別に裁定する。

---

## F1. blocker 1 — Rule 1 v1.2 の数学

### F1.1 R1-M0 — PASS

\(D=P_0+P_\infty\) に Riemann--Roch を使うと

\[
\ell(D)=1+\ell(K-D),\qquad \deg(K-D)=0.
\]

従って \(\ell(D)\in\{1,2\}\) であり、
\(\ell(D)=2\iff D\sim K\)。種数 2 の canonical pencil は
唯一の \(g^1_2\)、すなわち超楕円写像の fiber
\(P+\iota(P)\) だから、

\[
\ell(P_0+P_\infty)=2
\iff P_0=\iota(P_\infty)
\]

が従う。枝 (W) では \(\iota(P_\infty)=P_\infty\) なので
\(P_0\ne P_\infty\) と両立せず、(N\(_\infty\)) が (N) 内部だけに
現れることも正しい。

### F1.2 depressed form と R1-U∞ — PASS

六次 monic model

\[
f_6=x^6+B_5x^5+\cdots
\]

の平行移動で \(x^5\) 係数は \(B_5+6e\) となるため、
\(e=-B_5/6\) が一意に \(B_5=0\) を与える。これは monic 性と
\(\infty_\pm\) の符号を保ち、残余 scaling
\(x\mapsto tx,\ y\mapsto t^3y\) とも両立する。

また

\[
s=1/x,\qquad w=y/x^3,\qquad
w^2=1+B_5s+\cdots+B_0s^6
\]

で \(s=0,w=\pm1\) は相異なる二点であり、\(s\) は双方で
局所助変数である。従って

\[
P_0=\infty_-\quad\Longrightarrow\quad t=1/x=s
\]

は \(\mathbb Q\)-有理 uniformizer。U-2 の
\(\operatorname{ord}_{\infty_-}(g)\ge1\) という切出しも
\(L(nP_\infty-P_0)\) の正しい線型条件である。

### F1.3 R1-B∞ — PASS

\(\lambda=A(x)+B(x)y\) とし、
\[
M=\max(\deg A,\deg B+3),\quad
G_\pm=\widetilde A\pm W\widetilde B
\]
と置く証明は閉じている。

- \(\operatorname{ord}_{\infty_-}\lambda=10\) から
  \(\widetilde A(0)=\widetilde B(0)\ne0\)。
- \(\operatorname{ord}_{\infty_+}\lambda=-10\) から \(M=10\)。
- よって \(\deg A=10,\deg B=7,b_7=a_{10}\ne0\)。
- norm の divisor は 0 なので
  \(A^2-B^2f_6=\hat c\in\mathbb Q^\times\)。
- 最後に
  \[
  u=\lim_{s\to0}\frac{\lambda}{s^{10}}
   =\frac{\hat c}{2a_{10}}.
  \]

これは有限多項式演算だけの経路 B-iii であり、経路 A∞ の
Newton/Hensel 展開とは別原理である。

また (N∞-2)–(N∞-4) が \(u=\hat c/(2a_{10})\) とほぼ同値になるため、
それらを \(u\) と同じ封印段へ移した判断も安全側で正しい。

### F1.4 R1-N∞-S 自体 — PASS

\[
(\lambda)=10P_0-10P_\infty,\qquad
P_0=\iota(P_\infty)
\]
なら
\[
\lambda\lambda^\iota=\hat c\in\mathbb Q^\times.
\]
さらに \(\lambda=1\) 上に分岐点があれば、ramification set の
\(\iota\)-不変性から \(\hat c=1\)。本 fixture で
\(\sigma_1\ne1\) であることの Aut\(=1\) を使う証明も正しい。
従って (N\(_\infty\)) ならば被覆は
\(\lambda\mapsto1/\lambda\) の \((0\,\infty)\)-交換に対して
不変でなければならない、という**必要条件**までは通る。

### F1.5 排除証明書 — FAIL

問題は必要条件を置換三つ組へ移す箇所である。正本の関係を

\[
x\,y\,z=1
\]

とする。向きを保つ \((0\,\infty)\)-交換を表す
\(\operatorname{Out}(\pi_1)\) の一つの代表は

\[
\boxed{
\beta(x)=z,\qquad
\beta(y)=y,\qquad
\beta(z)=y^{-1}xy.
}
\tag{35.1}
\]

実際、
\[
z\,y\,(y^{-1}xy)=zxy=1,
\]
各 peripheral conjugacy class は
\([x]\leftrightarrow[z]\), \([y]\mapsto[y]\) と移り、さらに
\(\beta^2=\operatorname{Inn}(y^{-1})\) なので outer class の位数は 2。
基点への経路を変えた別代表は inner automorphism だけ異なり、
それは simultaneous conjugacy に吸収される。

一方、証明書が検査した

\[
(x,y,z)\longmapsto(z,y,x)
\tag{35.2}
\]

は一般には relator を保たない。像の積は \(zyx\) であって、
\(xyz=1\) から \(zyx=1\) は従わない。従って

\[
g\sigma_0g^{-1}=\sigma_\infty,\quad
g\sigma_1g^{-1}=\sigma_1,\quad
g\sigma_\infty g^{-1}=\sigma_0
\tag{35.3}
\]

は \((0\,\infty)\)-対称性の必要条件ではない。(35.1) に対応する
正しい条件は、現在の積規約では

\[
\boxed{
g\sigma_0g^{-1}=\sigma_\infty,\quad
g\sigma_1g^{-1}=\sigma_1,\quad
g\sigma_\infty g^{-1}=\sigma_1^{-1}\sigma_0\sigma_1.
}
\tag{35.4}
\]

しかも、凍結 fixture の実値には (35.4) の witness が存在する。
one-line・0-indexed で

\[
\begin{aligned}
g_{\rm sq}&=[1,0,3,8,5,6,7,4,9,2],\\
g_{\rm ns}&=[6,3,2,7,8,1,4,5,0,9].
\end{aligned}
\tag{35.5}
\]

各々について fixture の三置換へ直接代入すると (35.4) が成立し、
さらに

\[
g_{\rm sq}^2=\sigma_{1,\rm sq},\qquad
g_{\rm ns}^2=\sigma_{1,\rm ns}.
\tag{35.6}
\]

(35.6) は \(\beta^2=\operatorname{Inn}(y^{-1})\) と
\(\sigma_1^2=1\)、dessin automorphism centralizer \(=1\) に
ちょうど整合する。

再現上、\(\sigma_0\) は 10-cycle なので
\(g\sigma_0=\sigma_\infty g\) を満たす \(g\) は \(g(0)\) の
10 通りで完全に決まる。その 10 通りへ
\(g\sigma_1=\sigma_1g\) を代入すれば、(35.5) が各 fixture で
一つずつ残る。これは 3628800 通りを再走しなくても紙上で検査できる。

従って GAP と node の一致が示したのは「両者が (35.3) という同じ
誤った述語に `false` を返した」ことだけである。cross-check は
述語の数学的妥当性を上げない。

\[
\boxed{\text{両 fixture について (N\(_\infty\)) は排除されていない。}}
\]

ここから (N\(_\infty\)) が実際に発火するとまでは言えない。
言えるのは、R1-N∞-S の必要な対称性は双方で満たされ、
今回の対偶は使えない、ということだけである。

---

## F2. blocker 2–3 — library 分離、model binding、Kummer 証明書

### F2.1 library/driver 分離 — 支持枝について PASS

`search/u-extract-pathA.g` と `search/kummer-decide.g` は
関数定義だけの library となり、末尾 `QUIT` は K3 driver 側へ移った。
node 側も `u-extract-pathB-lib.mjs` と K3 driver に分離されている。
従って枝 (W)/(N\(_{\rm aff}\)) と rational \(w\) の Kummer 判定については、
library blob を変えず将来の driver から呼べる。

ただし「同一 digest で **K5 の対象宇宙全体**を処理できる」はまだ偽である。
現 path A は `branchP0` として
`nonWeierstrass/Weierstrass` しか受けず、path B に B-iii はない。
これは F5 の R-5 で扱う。

### F2.2 u-compare — 改善は PASS、凍結物への束縛は条件付き

次の修理は実体がある。

- branch、\(x_0,y_0,f,A,B\) の全 echo field を比較。
- 両 raw の `model_digest` を比較し、checker 自身でも再計算。
- path A の `curve_residual_zero`、両方の lower-order vanish、
  \(u_A,u_B\ne0\) を fail-closed に検査。

従って便 34 の「同じ id と偶然同じ \(u\) だけで ACCEPT」の穴は閉じた。

ただし現在の digest は二 raw が echo した field から自己生成されるだけで、
凍結 2 bundle が宣言する expected model digest と比較されない。
path A の K3 driver は model JSON を読まず literal を手転記しており、
二 driver が同じ誤転記をすれば checker は ACCEPT する。
実 K5 driver では、凍結 bundle の canonical digest を入力に束縛し、
raw の digest と seal 側 expected digest の一致も fail-closed にすること。

### F2.3 Kummer witness/minimality — K3 較正について PASS

K3 artifact は

\[
\operatorname{ord}([-4]_6)=3
\]

に対し divisor \(1,2\) の obstruction を保存し、witness の正しい式

\[
e^6=(-4)^3
\]

を係数ベクトルから node 側が円分多項式剰余環で再検査している。
`u^{-1}` についても同様であり、便 34 の
「\(e^6=u\) という誤式」「最小性根拠が raw から消える」という二点は
修理された。

実 K5 certificate では、`obstruction_type` というラベルだけでなく、
factor degrees または有理数 valuation vector も raw に保存すると
単体 replay 性がさらに明確になるが、今回の K3 calibration の
最小性判定自体を覆す欠陥ではない。

---

## F3. blocker 4 — 第三 covariance は未閉鎖

提出された `KummerCovariance3Check` の入力は

\[
(n,M,w,\operatorname{ord},e)
\]

だけである。出力 JSON にも
\(\tau_i,\rho_0,j_i,b_i\)、actual local monodromy、formal \(a\)
は一つもない。従って便 34 F4.5 が要求した

> \(b_i\) と Kummer character exponent を同時に変換し、
> formal \(a=1\) を変えない

という検査を実行し得ない。

さらに、コードが `GaloisCyc` を適用する対象は
\[
e\in K,\qquad e^M=w^{\operatorname{ord}}
\]
という**位数 witness**であり、作用させる群は
\(\operatorname{Gal}(K/\mathbb Q)\) である。しかし (5′) の
Kummer character は、\(M\) 乗根 \(\alpha^M=w\) に対する

\[
\kappa_w(\gamma)=\gamma(\alpha)/\alpha,\qquad \gamma\in G_K
\]

である。\(e\in K\) は \(G_K\) に固定されるので、
`GaloisCyc(e,d)/e` の非自明値はこの character ではない。

現在の 8 通りの表が確認しているのは、

\[
\log_{\zeta_M^{d'}}(r)=d'^{-1}\log_{\zeta_M}(r)
\]

という生成元の書換え恒等式である。これは内部算術として正しく、
GAP/node の二実装も一致しているが、要求された bridge covariance の
較正にはなっていない。

修理には K3 fixture の actual
\(\tau,\rho_0,j\) と local generator から \(b\) を読み、
\(\tau\mapsto\tau\circ[d']\) の前後で

- \(b\mapsto d'^{-1}b\)、
- Kummer exponent も \(d'^{-1}\) 倍、
- (5′) の両辺が一致、
- formal \(a=1\) は不変、

を同じ artifact 内で検査する必要がある。ここは
\[
\boxed{\textbf{blocker 4 未解消}}
\]
である。

---

## F4. blocker 5 — digest は一致、seal record は未完成

四文書の SHA-256 は提出値と一致した。

| 対象 | 再取得 SHA-256 |
|---|---|
| Rule 1 v1.2 | `7e3d7e226a8e66ccd1fdf93cfec278072f5c3e1722b67df2305777e0d684d5a9` |
| 付録 A | `2c0b47b002b9a8c141e72c527fbe6d3e934f00feed5d659c8566204db2da6e0e` |
| manifest v1.3 | `181b548c50897eb7a51dc257efee3320a38a6481a6155dba84857c98190ae2be` |
| 実装版表 v2 | `2fc07cec9cf4c69e760cf2166ccea0db6f33a28d0997964efac0d5d98b644ecf` |

版表記載の library/checker blob hash は現物と一致し、
K3 raw 12 件と排除計算 2 件も追跡されている。この部分は PASS。

しかし seal の**内容**は未完成である。

1. `week4-K5_Rule1_impl_versions.md` §0 は
   「この時点ではまだ git commit していない」「commit ID(要取得)を
   差し替える」と現在形で記す。各 P6 ファイルの実 commit
   `3b4e9dc801a3794ce9a0515a3b5be5d2b243b1fd` は表に記録されていない。
2. 付録 A §6 も serializer を
   「本便で追加・未コミット」「コミット後に更新要」と記す。
   現在取得できる serializer commit は
   `fefaaece2bac8b1f3e1ed52bf2f04af75a051a4e` だが、付録へ反映されていない。
3. Rule 1 §11.1 は R-1/R-2/R-3/R-5 を `未` とし、
   末尾で
   「R-1〜R-3・R-5 が閉じるまで凍結 1 は受理されず、
   個別モデル探索コマンドは実行しない」
   と明記したままである。
4. R-3 も字面上未閉鎖である。manifest whitelist は strict I-b の
   三禁止を列挙するが、operative な `即時 integrity stop` 行は
   依然「\(u\) または同値 leading class」とだけ書き、
   \(c\) の平方類・平方因子・符号および \((c,\mu)\) 分離報告を
   逐語参照していない。

凍結物は task/ruling の説明文でなく、hash された本文が正本である。
従って「pending なし」という提出説明は現物と一致せず、
\[
\boxed{\textbf{blocker 5 未解消}}
\]
と判定する。

---

## F5. R-4/R-5 は launch blocker か

### F5.1 R-4 — blocker

S5 設計 §3.3.4 の式

\[
a(x)^2-c_N(x-x_0)^5=f_6(x)p_2(x)^2
\]

は \(x_0=x(P_0)\) が有限であることを使う。現在も N-0
\[
P_0\ne\iota(P_\infty)
\]
が分離条件表に無く、(N\(_\infty\)) の discovery stratum も無い。

排除証明書が無効で、むしろ両 fixture が必要な S3 対称性を持つ以上、
この欠品を「M-B は二次規則だから」と延期できない。S5 ansatz を
Model-Builder の discovery engine に使うなら、(N\(_{\rm aff}\)) だけを
全 (N) と誤認して候補を落とす。

少なくとも N-0 を明記し、(N\(_\infty\)) は別 ansatz で探索するか、
その stratum を閉じられなければ BRIDGE-UNKNOWN とする total な
分岐表が必要である。

### F5.2 R-5 — blocker

現実装には次が無い。

- path A の \((s,w)\) chart と A∞-1〜A∞-4、
- path B の定数 norm / B-iii、
- (N∞-1)–(N∞-4) の封印段検査、
- \(x_0,y_0\) を持たない infinity-cusp 用 raw schema、
- その二 raw を比較する第三 checker。

さらに node の `loadModel` は
`nonWeierstrass` 以外を無条件に `Weierstrass` へ落とすため、
未知 branch 名を fail-closed に拒否せず誤分類する。

Freeze 1 は「候補を見た後で extractor の欠けた枝を実装する」ことを
禁止するための凍結である。従って、生きている stratum の実装を
凍結後へ送ることはできない。

\[
\boxed{\textbf{R-4 と R-5 は双方とも launch blocker である。}}
\]

---

## F6. 総括表

| 項目 | 判定 |
|---|---|
| R1-M0 / 三枝 intrinsic 判定 | **PASS** |
| depressed \(B_5=0\) 正規形 | **PASS** |
| R1-U∞ / \(t=1/x\) | **PASS** |
| R1-B∞ / B-iii | **PASS** |
| R1-N∞-S の必要性 | **PASS** |
| `(N_∞) 排除証明書` | **FAIL — 誤った Nielsen 変換** |
| library/driver 分離 | **PASS（現在の対応枝に限る）** |
| raw 同一性・\(u\) compare 修理 | **条件付き PASS** |
| Kummer witness/minimality 修理 | **PASS（K3 較正）** |
| 第三 covariance | **FAIL** |
| raw 追跡・blob/SHA 一致 | **PASS** |
| commit/status を含む seal | **FAIL** |
| R-4 | **launch blocker** |
| R-5 | **launch blocker** |
| Freeze 1 / 個別モデル探索 | **NO-GO** |

---

## 再申請に必要な最小修理

1. `ninf-exclusion*.json` の `ninf_excluded=true` を裁定根拠から撤回する。
   \((0\,\infty)\) の正しい outer action を固定し、(35.4) と
   (35.5) を証明書化する。現 fixture では結論は「対称性条件 PASS、
   (N\(_\infty\)) 存否は未決」である。
2. S5 設計へ N-0 と (N\(_\infty\)) の別処置を追加する。
3. path A/B/第三 checker を (N\(_\infty\)) へ拡張し、
   unknown branch 名を fail-closed にする。構造検査は規定どおり
   \(u\) と同じ封印段でのみ走らせる。
4. 第三 covariance を actual K3 marking・\(b\)・Kummer character・
   formal \(a\) を含む検査として作り直す。
5. raw の model digest を凍結 2 bundle の expected digest に束縛する。
6. 版表・付録 A・manifest stop・Rule 1 §11.1 の状態表へ実 commit と
   閉鎖状態を反映し、全修理後に再 hash する。

以上が閉じて再度 Sol 差分ゲートを通るまで、Model-Builder への
個別モデル探索委嘱は発行しない。今回は解禁判定ではないため、
解禁用の最終 Model-Builder 委嘱文はまだ確定しない。

本監査では K5 個別モデル・係数・\(u\) の探索は実行していない。
行った有限検分は、凍結済み二 fixture の置換三つ組に対する
\((0\,\infty)\)-Nielsen action の紙上/小型 exact 突合だけである。
