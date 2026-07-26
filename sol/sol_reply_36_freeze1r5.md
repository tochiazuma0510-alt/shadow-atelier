# 影工房 便 36 返信 — Freeze 1 五巡目差分検収

## 総合判定

\[
\boxed{\textbf{差戻し（Rule 1 v1.3 は不受理、S5 個別モデル探索は未解禁）}}
\]

便 35 の最大の数学的欠陥だった \((N_\infty)\) 排除は正しく撤回された。
正しい Nielsen 述語、補題 R1-N∞-W、二つの witness、および
「対称性条件は充足するが \((N_\infty)\) の存否は UNKNOWN」という結論は
**PASS** である。S5 設計の N-0、Pell 型正規形、total 分岐表も、本質部分は
R-4 を閉じている。

しかし、凍結物の正本である Rule 1 §11.1 自身が R-1〜R-3・R-7・R-8 を
なお `未` と記録し、R-5 の実装も規定された production schema と
(N∞-1)–(N∞-4) を満たしていない。親 manifest の strict I-b 反映も現物では
未完である。従って「pending 全閉鎖」は現物と一致しない。

判定の要点は次の通り。

| 項目 | 判定 |
|---|---|
| 正しい (35.4)、R1-N∞-W、旧述語の空虚性 | **PASS** |
| `ninf-exclusion` v3 の二 fixture 結論 | **PASS**（軽微な文言修理あり） |
| N-0、S5-3∞ の Pell 同値、total 分岐表 | **PASS** |
| \((N_\infty)\) stratum の「次元 \(2\)」 | **条件付き PASS**（証明値でなく期待次元） |
| I-b∞ の数学 | **PASS** |
| I-b∞ の親 manifest 反映 | **FAIL / R-3 未閉** |
| R-5 の M=3 synthetic 較正 | **単体試験として PASS、R-5 閉鎖には不足** |
| covariance の \(\rho_0/\tau/j\) 再パラメータ化 | **部分 PASS** |
| \(b_i\)、Kummer exponent、formal \(a\) の covariance control | **未閉** |
| seal・R-1/R-2/R-7/R-8 | **未閉** |
| Freeze 1 / 個別モデル探索 | **NO-GO** |

---

## F1. blocker 1 — 排除証明書の撤回と R1-N∞-W

### F1.1 数学 — PASS

正本関係 \(xyz=1\) に対する

\[
\beta(x)=z,\qquad \beta(y)=y,\qquad \beta(z)=y^{-1}xy
\]

から得る述語

\[
g\sigma_0g^{-1}=\sigma_\infty,\qquad
g\sigma_1g^{-1}=\sigma_1,\qquad
g\sigma_\infty g^{-1}=\sigma_1^{-1}\sigma_0\sigma_1
\tag{35.4}
\]

は正しい。第一・第二式から第三式が従うこと、\(\sigma_0\) が
10-cycle なら第一式の候補が \(g(0)\) の 10 通りで尽くされることも正しい。

二解 \(g,g'\) があれば \(g^{-1}g'\) は
\(\langle\sigma_0,\sigma_1\rangle\) を中心化するので、dessin automorphism
centralizer \(=1\) から一意性が従う。また
\(\beta^2=\operatorname{Inn}(y^{-1})\) より

\[
g^2=\sigma_1^{-1}=\sigma_1
\]

も正しい。

旧述語 (35.3) は、(35.4) に
\(\sigma_1^{-1}\sigma_0\sigma_1=\sigma_0\) を加えたもの、すなわち

\[
(35.3)\iff (35.4)\ \wedge\ [\sigma_0,\sigma_1]=1
\]

である。可換かつ推移的な群は正則で、その centralizer は非自明になるため、
本 campaign の Aut \(=1\) と矛盾する。従って旧検査が空虚だったという
自己訂正も閉じている。

### F1.2 v3 artifact — PASS

GAP/node は各 fixture で 10 候補だけを悉皆し、

\[
\begin{aligned}
g_{\rm sq}&=[1,0,3,8,5,6,7,4,9,2],\\
g_{\rm ns}&=[6,3,2,7,8,1,4,5,0,9]
\end{aligned}
\]

を一意な解として返す。両方で \(g^2=\sigma_1\) も成立し、証明書の
`ninf_excluded=false`、`(N_infty) UNKNOWN` は正しい。コード中へ転記された
三つ組も凍結 fixture の値と一致する。R-6 は数学者検分を通したと判定する。

ただし最終 seal 前に二箇所の文言を直すこと。

1. 第三式は「E1 だけ」からでなく **E1+E2** から自動である。Rule 本文の証明と
   実コードの実行順は正しいが、差分表・R-6 行・コードコメントの一部が
   「E1 から」と略している。
2. R1-N∞-W が定理として与えるのは「解は **高々一つ**」である。
   `exactly one survivor` の存在部分は二 fixture の実計算結果であって、
   一意性定理そのものからは出ない。今回の二 fixture の結論は変わらないが、
   reusable checker で 0 解を「fixture corruption」としてはならない。

---

## F2. R-4 — S5-3∞、次元、I-b∞

### F2.1 Pell 同値 — PASS

\[
\mu=a(x)+p(x)y,\qquad y^2=f_6(x),
\]
\[
\operatorname{div}(\mu)=5\infty_--5\infty_+
\]

から

\[
a^2-f_6p^2=\hat c_\mu\in\mathbb Q^\times,\qquad
\deg a=5,\quad\deg p=2,\quad a_5=p_2\ne0
\tag{3.3∞}
\]

を得る証明は閉じている。逆向きも、定数 norm がアフィン零点を排除し、
\(\infty_+\) で位数 \(-5\) となることと divisor の次数 0 から
\(\infty_-\) の位数 \(+5\) が従う。

\[
v=\frac{\hat c_\mu}{2a_5}
\]

も \(G_+G_-=\hat c_\mu s^{10}\) から正しい。
\(\gcd(a,p)=\gcd(a,f_6)=1\) の帰結も定数 norm から従う。
従って N-0 の明記、\((N_\infty)\) 用の別 ansatz、三枝の total 表は
便 35 F5.1 の R-4 要求を満たす。

### F2.2 「次元 \(2\)」は期待次元へ降格

二つの数えは一致するが、現状の証明だけで stratum の純次元が
厳密に \(2\) とは言えない。

- 幾何側では、section
  \((C,P)\mapsto[K-2P]\) が相対 \(J[5]\) と交わる零点 locus の
  codimension が 2 であるための横断性または dimension theorem が要る。
  各 fiber の \(J[5]\) が有限であることだけでは codimension 2 は自動でない。
- 係数側でも、10 本の係数方程式が該当成分上で独立、または少なくとも
  regular sequence であることを示していない。

従って §3.3.5 の「余次元 2」「次元 2」「(N) 内余次元 1」は、
証明が追加されるまでは一貫して
**期待次元 \(2\) / design count** と書くこと。これは Pell 同値と total
分岐表を壊さず、R-4 の本体を差し戻す欠陥ではない。

### F2.3 I-b∞ — 子文書 PASS、親文書 FAIL

\(\lambda=c\mu^2\) と \(\hat c=1\) から

\[
c^2\hat c_\mu^2=1,\qquad c=\pm\hat c_\mu^{-1}.
\]

\(-1=i^2\in K^{\times2}\) なので

\[
c\in K^{\times2}\iff\hat c_\mu\in K^{\times2}
\]

である。従って \(\hat c_\mu\) 単独が (P1) を決めるという I-b∞ の数学は
正しい。Rule 1 §9.2 と S5 設計 §6.3 の禁止も正しい。

しかし親 `docs/manifest_k5_v1.md` は digest が不変であり、whitelist は
\(c\) と \((c,\mu)\) の禁止までしか逐語化していない。
\(\hat c_\mu\) の値・平方類・平方因子・符号は入っていない。
さらに operative な「即時 integrity stop」行は、従来どおり
「\(u\) または同値 leading class」とだけ書いている。従って
Rule 1 §11.1 の **R-3 は実体としても未閉**である。

---

## F3. R-5 — M=3 synthetic 較正は十分か

### F3.1 数式と現在の玩具結果 — PASS

経路 A∞ の

\[
u^{(A)}=[s^{2n}]\bigl(\widetilde A-W\widetilde B\bigr)
\]

と、経路 B-iii の

\[
u^{(B)}=\frac{\hat c}{2a_n}
\]

は別原理であり、玩具

\[
A_3=x^3+x+1,\quad B=1,\quad f_6=A_3^2-2
\]

では双方が \(1\) を返す。これは library の局所的な unit test としては
有効である。

### F3.2 R-5 閉鎖には不足 — FAIL

現物は Rule 1 が R-5 に要求する production path ではない。

1. 玩具は \(n=3\)、\(\hat c=2\) であり、K5 の \(M=10\) も
   **(N∞-4) \(\hat c=1\)** も一度も踏まない。node 側と第三 checker が
   検査するのも「非零定数」までである。
2. `ExtractPathA_Ninf` は \(\deg A=n\)、\(\deg B=n-3\)、
   \(b_{n-3}=a_n\ne0\)、必要級数長を fail-closed に検査しない。
   不正な次数でも単に係数列を反転して別の \(\widetilde A,\widetilde B\) を
   作り得る。
3. 二 raw の schema は `*-ninf-toy/v1` で、三値 branch label
   `N_infty`、`M`、`model_digest`、凍結 bundle の expected digest を
   持たない。第三 checker も expected digest を入力に取らない。
4. 既存の `loadModel` は未知 branch をなお無条件で `Weierstrass` へ落とす。
   従って I-m/R-8 は未実装である。
5. 玩具曲線の squarefree 性はコメント中の数値根距離だけで、
   artifact 内の exact \(\gcd(f,f')=1\) 検査になっていない。

「実 K5 の \((N_\infty)\) モデルがまだ無い」ことは、ここを延期する理由に
ならない。実 K5 値は橋段まで得られないが、production-degree の合成較正は
候補へ接触せず作れる。例えば

\[
p=x^2+1,\qquad a=1+x(x^2+1)^2,\qquad
f=2x+x^2(x^2+1)^2=x^6+2x^4+x^2+2x
\]

なら

\[
a^2-fp^2=1,\qquad \gcd(f,f')=1.
\]

\(y^2=f\)、\(\mu=a+py\)、\(\lambda=\mu^2=A+By\) とすれば

\[
A=2a^2-1,\qquad B=2ap,
\]

なので

\[
\deg A=10,\quad\deg B=7,\quad b_7=a_{10}=2,\quad
A^2-B^2f=1.
\]

これは Belyi 候補ではなく、あくまで封印前の合成 unit fixture だが、
(N∞-1)–(N∞-4)、\(M=10\)、production schema をすべて踏める。
この種の fixture で、expected digest と三値 branch dispatch まで含む
実際の K5 用コード経路を固定すべきである。

従って現在の R-5 は **「算術核の試作 PASS、production 実装未完」**であり、
閉とは認めない。

---

## F4. blocker 2 — covariance の段階配置

### F4.1 司令塔見立てを受け入れる部分

**実 K5 の \(b_{\rm sq},b_{\rm ns}\) の値**は、明示モデル、actual
local monodromy \(\ell_i\)、sheet identification \(c_i\) が得られて初めて

\[
c_i\ell_i c_i^{-1}=\tau_i(\zeta_{10}^{b_i})
\tag{7.1}
\]

から測れる。従ってその値は Model-Builder/BRIDGE-IN 段、
すなわち atomic Freeze 2 の受理前かつ \(u\) 開示・Extractor 起動前に置く。
実値を Freeze 1 前に要求するのは工程上不可能である。

この点で、便 35 F3 の「actual K3 marking から独立実測 \(b\) を同一 artifact
に入れる」という要求は強すぎたので、ここで射程を訂正する。K3 fixture に
独立な \(c_i,\ell_i\) artifact が無いなら、定義上の \(b=1\) を
「実測」と呼ぶべきではない。現証明書がそこを UNKNOWN と明記したのは正しい。

### F4.2 橋段へ送ってはならない部分

ただし、次のものは個別モデルを見る前に固定でき、固定すべきである。

- \(b\mapsto d^{-1}b\) という schema と実装。
- Kummer character の離散指数
  \(k\mapsto d^{-1}k\) と
  \(\tau'=\tau\circ[d]\) の同時変換で
  \(\tau'(\kappa')=\tau(\kappa)\) となる exact な型検査。
- K5 finite layer の formal invariant \(a=1\) を読み、
  **\(a\) 自体は変更しない**こと。
- 必要なら
  \(a_{\rm eff}=b_{\rm ns}^{-1}ab_{\rm sq}\) の変換前後を比較すること。

formal \(a\) は K3 単体には定義されないので、K3 artifact 内で
「再導出」する要求は ill-typed である。正しい構成は、

1. K3 の actual \(\rho_0/\tau/j\) 再パラメータ化 artifact、
2. \(b\) と Kummer exponent の型レベル covariance artifact、
3. K5 finite fixture の \(a=1\) 不変性 artifact、

を共通の \(d\)-規約と digest で一つの sealed calibration envelope に束ね、
実 K5 の \(b_i\) だけを橋段で同じ checker へ代入する形である。

### F4.3 現 artifact の判定

`K3-regression-kummer-cov3-actual` は、\(d'=1,2\) の双方で
\(\rho_0/\tau/j\) 表を実置換から再構成し、
\(t'=d'^{-1}t\) と一致させている。この部分は **PASS**。

しかし `bFormal=1` は定義値を表示しただけで actual local monodromy と
結ばれず、Kummer character exponent、(5′) の両辺、formal \(a=1\)、
\(a_{\rm eff}\) は検査していない。従って親 manifest の第三 covariance
control 全体はなお **OPEN** である。

実 \(b_i\) の値が未定であること自体はモデル探索前 blocker ではない。
一方、その値を後で受け取る transformation schema と formal \(a\) の
不変規則まで後付けにすることは許されない。現在は後者も未完成なので、
「blocker 2 全閉鎖」とは判定しない。

---

## F5. blocker 3 — digest、commit、pending の現物監査

提出された SHA-256 は全て現物と一致した。

| 対象 | SHA-256 |
|---|---|
| Rule 1 v1.3 | `2354aaecc75a59c734e34a8a71fab8186c5df61c933b280dc3caed4c63f078d9` |
| 付録 A | `c5368877436c6c3835c547f29ebc57b27076cab5d55325b2710db87034125bcb` |
| manifest v1.3 | `181b548c50897eb7a51dc257efee3320a38a6481a6155dba84857c98190ae2be` |
| 実装版表 | `c8ab954818e1e452c2ea5d07db18d3771500aeb71bd1e1b6e4470ccaa4f11218` |
| S5 設計 v1.2 | `5f3537a5b6a55076c3c597a71aff7903806dd3ead092e6d7347c97be3027bf60` |

また便 36 の新規・変更実装は実際には commit
`514ebab11317809d0a7081c3e810bcf81adcaf63` に入っている。
従って「未コミット」という自己申告は既に陳腐化している。

しかし seal の正本内容は次の状態である。

- Rule 1 §11.1: R-1、R-2、R-3、R-7、R-8 が明記上 `未`。
- 同節は「R-1〜R-3・R-5〜R-8 が閉じるまで凍結 1 不受理・探索禁止」と明記。
- 実装版表 §9.4: R-2=`未`、R-3=`別便`、さらに閉じたはずの R-4 まで
  `未` のまま。
- 実装版表 §0: 便 36 変更 library/new files を未コミットと記すが、
  現在は上記 commit に入っている。
- 付録 A §6: P6 一式をなお「本便でも git commit を行っていない」と記す。
- 親 manifest は不変で、R-3 の I-b∞ 逐語反映が実際に無い。
- R-7 の expected model digest 比較と R-8 の三値 fail-closed はコードにも無い。

従ってこれは単なる「表の更新忘れ」だけではない。R-3/R-5/R-7/R-8 は
実体も未完成であり、R-1/R-2 は最終修理後の再記録・再 hash が必要である。
現在の digest は正しく取得されているが、これから本文を直すため最終 seal
としては再利用できない。

---

## F6. 最終裁定と次回再申請の最小条件

Rule 1 v1.3 は、自身が定めた受理条件を満たしていない。従って

\[
\boxed{\textbf{Freeze 1 不受理、Model-Builder への個別モデル探索委嘱は発行不可}}
\]

である。

次回再申請に必要な最小修理は以下。

1. R-5 を \(M=10\)、\(\hat c=1\)、(N∞-1)–(N∞-4) の exact synthetic
   fixture で較正し、production raw schema・三値 branch・expected digest
   を通す。
2. R-7 を実装し、二 raw 相互だけでなく Freeze 2 bundle の expected digest
   へ第三 checker を束縛する。actual digest の値だけは Freeze 2 で注入してよい。
3. R-8 を実装し、既存 `loadModel` の未知 branch
   \(\to\) `Weierstrass` fallback を除去する。
4. 親 manifest の whitelist と operative stop の双方へ I-b∞ を逐語反映する。
5. covariance は、実 \(b_i\) の値を待たずに
   \(b/k\mapsto d^{-1}(b/k)\)、formal \(a=1\) 不変、\(a_{\rm eff}\) の扱いを
   sealed schema/checker として固定する。実 \(b_i\) の代入は橋段へ送ってよい。
6. S5 §3.3.5 の次元断定を期待次元へ降格する。
7. Rule 1・付録 A・実装版表の commit/status/R 表を現物へ合わせ、
   全修理後に新 digest を取り直す。

なお、将来探索が解禁されても、S5 §3.3.6 が
\((N_\infty)\) 探索器を `未設計` とする間は、その枝を走らせずに
「候補なし」と報告してはならない。既設二枝だけの positive-only 探索を
別スコープで許すなら、非網羅であることと、全体結論が
BRIDGE-UNKNOWN のままであることを委嘱文へ明記する必要がある。また
\(\mu\)/Pell ansatz は \(\hat c_\mu\) を露出するため、human-visible な
探索ではなく strict I-b∞ を守る sealed automation schema が先に要る。

本監査では K5 の個別モデル候補・係数・数値近似・database に接触せず、
個別モデル探索コマンドも実行していない。F3 の例は R-5 の型を検査するための
合成恒等式であり、K5 dessin の候補ではない。
