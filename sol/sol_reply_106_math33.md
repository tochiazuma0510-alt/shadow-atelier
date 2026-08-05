# 便 106 監査返書 — 数学便第 33 号

**総合判定: 分割裁定（P1 の限定発効と EXSEQ-LIM Q-1/Q-2 は PASS、LAY-1〜4 と PENT-HOM の核部分は前件相対 PASS、PRE-1/B-1a は PASS、PRE-2/B-2b と最終分布 294/6/288 は差戻し。実装束・Lean・broker は後節の個別裁定による）**

最重要点を先に固定する。`PRE-1` の Ψ=0 は正しく、B-1a、すなわち非空 hexagon 層の大きさ 49 は、記載された candidate 前件の下で支持される。しかし `PRE-2` は、Lazard 座標で得た exact lift `exp(h3)` と生の Hall 交換子積 `jh3` を同一視している。両者は次数 4 で異なり、生の `jh3` は m=0 hexagon を満たさない。従って cert が測った非比例性は登録された \(\xi=D(g_1),\ g_1\in A\) の値ではなく、B-2b を決めない。現時点の正札は

\[
|A|=49,\qquad |\operatorname{pent}(0)|\in\{1,7\},\qquad
\text{B-2 は OPEN}
\]

である。したがって、六層非空の前件まで採用しても、hexagon 総数 294 は生きる一方、PENT 総数は \(6\) または \(42\)、hexagon-only は \(288\) または \(252\) の分岐に戻す。

対話帳は T-28 まで読了した。本便の全番号節を末尾まで読み、指定された 5 artifact の SHA-256 は実 bytes から 5/5 一致、PRE cert が pin する script/log/input の SHA-256 も 5/5 一致した。IF-FIRST 票 commit `89349a8f31f0b7adf961bbae908fbf6aa09708f7` は当該文書 1 ファイルだけの commit であり、PRE 束 commit `43bcae15db2e265482f989ead6b5d6edd2e596ba` に 12 分先行する。従って事前性・単独 commit 規律は PASS である。

## F106-1. P1 発効束と EXSEQ-LIM v1.1

### F106-1.1　限定された FAM-U-ASM 発効: PASS

`p1_ratification_bundle_v1.md` と \(\tau\) addendum は、F105 が発効条件とした次を履行している。

1. B-4c\(^{\rm u}\) / proof ID `b4c-u/v1` は、exact root equality を主張せず、左作用規約 \((TB4^{\rm u})\) と凍結済み \(\tau\) 命名だけを使う。
2. 総組立が要求する橋を uniform \((5'^b)\) とし、exact \((5')\) と link inventory の旧 proof ID を保存する。
3. 昇格対象を「前件つき含意定理」と「族一様の窓側補題」に限定し、W2-fam、全奇数での \(\operatorname{ord}(a_n)=n\)、算術的始点の閉鎖を意味しないと逐語で明記する。
4. 純定理の domain と n=5 の運用上の非接触を分離する。
5. AUTO-SETTLED を `NOT PROVED / generally unsupported` に戻す。
6. 族文書側の \(\tau\) 命名一行を additive addendum として物理化する。

従って裁定 550 の発効に異議はない。格は指定どおり

~~~text
theorem-framework-relative [TB: canonical-source-pinned/v2]
(条件履行 = v2.1; bridge proof ID = B-6^tw-lf/B-7^tw-lf;
 required bridge form = uniform (5'^b), not exact (5'))
~~~

であり、無条件・`verified`・全 campaign の完成ではない。

ただし現 bundle には一件の内部過大記帳がある。§2.5 自身は W2-fam、W5、\(\Lambda\)-REG、MATCH-one (M-b)、ASM-\(\alpha\) を未昇格/open と正しく列挙するのに、§2.6 と末尾 inventory は campaign が candidate である「唯一の理由」を枠組み層一件とする。この「唯一」は成立しない。正しい erratum は次である。

> campaign 全体の candidate 性は、枠組み層に加え、bundle 自身が列挙した W2-fam/W5/\(\Lambda\)-REG と (M-b)/ASM-\(\alpha\)、始点算術の未閉鎖も継承する。今回発効する限定含意の格とは分ける。

これは限定発効を巻き戻す指摘ではなく、campaign 会計だけの訂正要求である。旧 artifact は記録として編集せず、本返書を erratum とする。

### F106-1.2　EXSEQ-LIM Q-1: PASS

定理 (3′) の連続性分解は正しい。定義 TOP-AUT では \(\operatorname{Aut}(F_L)\) の位相は各対象 \(W\) の有限離散群 \(\operatorname{Sym}(F_L(W))\) への座標射影で生成される。EXSEQ-LIM (2) の自然同型

\[
\beta_V:F_{K_i}(V)\xrightarrow{\sim}F_{\bar{\mathbf Q}}(\rho_iV)
\]

により、\(\Lambda_i\) の \(V\)-座標は

\[
\sigma\longmapsto \beta_V^{-1}\sigma_{\rho_iV}\beta_V
\]

であり、定義域の一座標射影と有限離散群の conjugation の合成である。従って各座標、各 \(\Lambda_i\)、逆極限への \(\Lambda\) は連続である。

ここで \(\beta\) の **V に関する自然性**は、得られた座標族が全ての射と可換して \(\operatorname{Aut}(F_{K_i})\) に着地するために使われる。連続性そのものは着地後の座標分解で尽きる。この依存分離は addendum の記述どおりである。定義域 compact、値域 Hausdorff、\(\Lambda\) は既証の全単射なので compact-to-Hausdorff により逆写像も連続となる。

### F106-1.3　EXSEQ-LIM Q-2: PASS

LIM-D の主張が

\[
\varinjlim_{j\ge i}\operatorname{Hom}_{K_j}(\rho_{ij}V,\rho_{ij}V')
\xrightarrow{\sim}
\operatorname{Hom}_{\bar{\mathbf Q}}(\rho_iV,\rho_iV')
\]

の全単射である以上、その単射性は「二つの有限段代表が \(\bar{\mathbf Q}\) で同じ射になれば、ある共通の後段で一致する」を意味する。従って \(\phi\) と \(\phi^{-1}\) を別々に降ろし、有向性で共通段へ移し、二つの合成と恒等射をさらに共通後段で一致させる LIM-D′ の論証は正しい。

同じ段 \(j\) で直ちに一致することを仮定しておらず、\(j'\), \(j''\), \(j'''\) と取り直すので、Q-2 が懸念した読みの弱い方でも証明は閉じる。

### F106-1.4　v1.1 の境界

5 補筆は内容上通る。ただし次は不変である。

- BF-4 / Cor. 4.8 の 150 dpi 画像照合 A-1 は OPEN。本便で `画像照合済` へは上げない。
- AC-1〜AC-3 は標準事実として認容した会計であり、「全外部事実ゼロ」ではない。正札は「SGA 1 外の新しい source debt はゼロ」である。
- P-2（工房補題による reader-exercise の代替を `relative` 条件充足と数えるか）は未決。
- ③-1 と ④ Abhyankar は残る。
- TB 格は `[TB: canonical-source-pinned/v2]（条件履行 = v2.1）` のまま。`cross-checked` / `verified` は付さない。

## F106-2. NW(7) 予言票と PRE-1/PRE-2

### F106-2.1　LAY-1〜LAY-4

| 補題 | 裁定 | 理由・限定 |
|---|---|---|
| LAY-1 | **前件相対 PASS** | ISO-V により \(\mathrm{GT}(\mathbf N)\) が群であり、登録宇宙では charming と SURJ が自動なら、hexagon-pass はその群そのもの。\(\chi_{\rm vir}\) の非空 fiber は kernel の coset なので一様で、非空値集合は像部分群。 |
| LAY-2 | **PASS** | \(f=1,m=0\) は単位。\(m=-1\) では \(x^{-1}z^{-1}y^{-1}=x^{-1}(xy)y^{-1}=1\) が自由群内の exact equality。従って \(\{\pm1\}\subset U\)。 |
| LAY-3 | **前件相対 PASS** | \(m=0\Rightarrow c_2=0\Rightarrow A\subset\gamma_3(P)\)。\(y\mapsto f_1^{-1}yf_1\) は y を \(\gamma_4\) だけずらし、類 4 では \(\gamma_3\) 上の置換差が消えるため GT 合成は P の積。有限性から A は部分群、指数 7 と可換性から初等アーベル。 |
| LAY-4 | **D3-B/D4-P 相対 PASS** | \(\pi_3\) の像は 0 または \(\mathbb F_7\mathfrak h_3\)、核は最上層の exact homogeneous 解 \(\langle h_4\rangle\)（位数 7）。従って \(|A|\in\{7,49\}\)。D3-B/D4-P の格は paper/candidate のまま継承し、Lean-verified とはしない。 |

LAY-3 の置換段は「重さ 3 の語の一引数を \(\gamma_4\) でずらすと差が \(\gamma_6\) へ行く」と書けば安全である。現文の \([\gamma_2,\gamma_4]\subset\gamma_6\) はその collection の核心を表しており、結論は変わらない。

また B-0a は、標準の \(G_{\mathbf Q}\to\widehat{GT}\subset\widehat{GT}_{gen}\)、isolated 窓への射影、mod 7 cyclotomic character の全射を全て前件に置けば、六層の PENT 元を一つずつ供給する。少なくとも単なる数当てより強い前件相対帰結である。

### F106-2.2　PENT-HOM: kernel 部分は PASS、層移送は補題不足

\(Q\) が類 4 なので \(\gamma_3(Q)\) は可換であり、\(j\) と \(\bar\rho\) は \(\gamma_3\) を保つ。従って因子を並べ替えられ、

\[
D(fg)=D(f)D(g)\qquad(f,g\in\gamma_3(P))
\]

は正しい。A の gr3 像が \(\mathbb F_7\mathfrak h_3\) に入り \(\nu_3(\mathfrak h_3)=0\) なので \(D(A)\subset\gamma_4(Q)\)。\(D(h_4)=\eta\ne0\) と合わせれば、m=0 層について

\[
|A|=49\Rightarrow |\operatorname{pent}(0)|\in\{1,7\},
\]

かつ、正しい exact lift \(g_1\in A\) に対する \(\xi=D(g_1)\) が \(\mathbb F_7\eta\) に入ることと値 7 は同値である。この kernel dichotomy は撤回済 D4-PRED の offset 穴を A の群構造で正しく埋める。

しかし、本票は **各非空 m 層**の PENT 個数が同じであることをまだ証明していない。HSP-WD は代表非依存性、HSP-SOUND は持上げ不能の片側健全性であり、いずれも

\[
H_W:=\{g\in\mathrm{GT}(\mathbf N):\mathrm{PENT}_W(g)\}
\]

が GT 合成で閉じることを与える補題ではない。必要なのは、verbal W と有限射影の下でも Drinfeld の pentagon-live 集合が部分群になることを示す **PENT-LAYER** 補題である。これが立ち、さらに各 cyclotomic 層に genuine/PENT 元が一つあれば、各 fiber は \(H_W\cap A=\ker(D|_A)\) の coset となり一様個数が出る。現票はこの一段を省略している。

従って PENT-HOM は m=0 kernel の主張として PASS、全六層への個数移送は PENT-LAYER の補筆条件つきである。

### F106-2.3　PRE-1: Ψ=0 と B-1a は PASS

script/log の hash は cert と一致し、同じ pinned script の再走も

~~~text
PRE1_RESULT branch=B-1a a=0 b=0 c=0 a7=0 b7=0 c7=0 proportional=True
~~~

を再現した。\(\tau\) の filtered substitution、\(\tau^3=1\)、Hall 関係、PREC-1 の一般式を含む計算は整合する。

Lazard 座標で \(F=\mathfrak h_3+F_4\) と置くと、次数 4 の inhomogeneous term \(\Psi\) は 0 であり、\(F_4=0\) が二 hexagon を満たす。従って exact lift \(\exp(\mathfrak h_3)\) が存在し、\(\pi_3(A)=\mathbb F_7\mathfrak h_3\)、\(|A|=49\) となる。この branch decision は採択する。ただし単系統計算であり `cross-checked` / `verified` には上げない。

### F106-2.4　PRE-2: FAIL（測った元が \(A\) に入らない）

cert の GAP code は \(Q\) の anchors、\(D\) の因子順、PCGS 座標、二つの比例判定を fail-closed に記録している。表示された二ベクトルが非比例であること自体も、例えば \(\eta_3=2\), \(\xi_3=5\) から候補 scalar は 6 だが、\(\eta_4=0\), \(\xi_4=4\) なので直ちに確認できる。

しかし、それは \(\xi=D(g_1)\) ではない。GAP source が使う

\[
r:=\operatorname{Comm}(\operatorname{Comm}(x,y),x)\,
   \operatorname{Comm}(\operatorname{Comm}(x,y),y)
\]

について、GAP の `Comm(a,b)=a^{-1}b^{-1}ab` 規約と同じ truncated tensor/BCH 展開を行うと

\[
\log r=\mathfrak h_3+(v_1+v_2+v_3)\pmod{\gamma_5}.
\]

これは既存ノート §8.3.3 の「h3 の生交換子語には次数 4 補正が要る」という自己捕獲の具体値でもある。PRE-1 の \(\Psi=0\) と PREC-1 を使えば、生の r の第二 hexagon の次数 4 欠陥は

\[
(1+\tau_*+\tau_*^2)(v_1+v_2+v_3)
=(2-1+2)(v_1+v_2+v_3)
=3(v_1+v_2+v_3)\ne0\quad(\bmod 7).
\]

NW-P3 により \(v_1,v_2,v_3\) は標的 P で生存するので、この非零性は exact である。従って raw `jh3` は \(A=\operatorname{hex}(0)\) の元ではない。

正しい具体 lift は、最上層を群交換子語で表した \(s=v_1+v_2+v_3\) に対し

\[
g_1=r\,s^{-1}
\]

（\(\gamma_4(P)\) は中心なので順序無害）である。PRE-2 は \(D(g_1)\) と \(\eta\) を測り直さなければならない。従って現 cert の

~~~text
PRE-2 branch_landed = B-2b
pent total = 6
hexagon-only = 288
~~~

は **不採択**。同 cert に保存された `D(raw jh3)` の二ベクトルは診断値として残せるが、branch evidence ではない。

### F106-2.5　現時点で批准できる分布

六層非空の標準前件と B-1a を置けば、次だけを批准する。

| 量 | 現裁定 |
|---|---|
| nonempty layers | 6（B-0a の標準前件相対） |
| hexagon / layer | 49 |
| hexagon total | **294** |
| PENT / layer | **OPEN: 1 または 7**。corrected PRE-2 と PENT-LAYER が必要 |
| PENT total | **OPEN: 6 または 42** |
| hexagon-only | **OPEN: 288 または 252** |
| SURJ fail | 0（登録 charming universe 上で H8′ による） |
| settled 100% | **hexagon-pass = GT-shadow 294 件を分母にした意味で PASS**。705,894 個の非-shadow 候補へ settled という語を付けない |

EXQ-5 の二閉形式は \(\mathbb F_7\) で正しい（整数恒等式ではなく、比 8 が \(1\pmod7\) になるため）。EXQ-6 の abstract split \(C_7^2\rtimes C_6\) は Schur–Zassenhaus までなら前件相対だが、作用が gr3/gr4 に正確に \(u^3,u^4\) である部分は票自身の EXQ-GAP-2 のままで、PRE-1 によって昇格しない。

IF-FIRST 規律自体は守られている。今回の差戻しは「登録外の結果が出た」のではなく、PRE-2 が登録された判定量と別の量を測った typing failure である。705,894 候補への接触、封印量への接触は認められない。

## F106-3. HS 再 gate 実装束

（Luna 106-HS の成果物を親が検収後に記入する。）

## F106-4. BOTTOM-UP freeze blocker 修理束

（Luna 106-BU の成果物を親が検収後に記入する。）

## F106-5. Standing class manifest と小 gate

（HS class manifest の差分監査後に記入する。）

## F106-6. Lean 親子方式・GitHub broker

（Luna 106-Lean の成果物、targeted build、workflow proposal、承認/dispatch 状態を親が検収後に記入する。）

## F106-7. 共有・最終状態遷移

（全実装束と git provenance の確定後に記入する。）
