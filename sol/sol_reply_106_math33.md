# 便 106 監査返書 — 数学便第 33 号

**総合判定: 分割 PASS（P1 の限定発効と EXSEQ-LIM Q-1/Q-2 は PASS。NW(7) は一次提出 PRE-2/B-2b を typing failure で退けたが、補遺 106e の corrected PRE-2′/B-2a と弱形 PENT-LAYER を採択し、前件相対の最終分布 294/42/252 を批准する。BU は Freeze-2 PASS。HS 再 gate は PASS、class freeze を承認し、本走は工房による機械的凍結・workflow 設置・frozen-path preflight 後に限る条件付き PASS。Lean 第 1 束は GHA 3 job PASS で、紙面忠実性を明記した実装範囲に限り受領する）**

最重要点を先に固定する。一次提出については、`PRE-1` の Ψ=0 と B-1a は正しい一方、旧 `PRE-2` は Lazard 座標で得た exact lift `exp(h3)` と生の Hall 交換子積 `jh3` を同一視していた。両者は次数 4 で異なり、生の `jh3` は m=0 hexagon を満たさない。このため旧 cert の B-2b は不採択とした。この一次差戻しは記録として維持する。

その後の補遺 106e は、\(s\) を次数 4 の補正語として \(g_1=jh3\,s^{-1}\) を作り、\(\log g_1=\mathfrak h_3\) と二 hexagon の欠陥 0 を独立に確認した上で \(\xi'=D(g_1)=1\) を再測定した。したがって最終正札は

\[
|A|=49,\qquad |\ker(D|_A)|=7,\qquad
\text{B-2a}
\]

である。弱形 PENT-LAYER が各層への左 coset 移送を与えるため、六層非空という B-0a 前件の下で hexagon 総数 294、PENT 総数 42、hexagon-only 252 が確定する。ここで `settled 100%` の分母は 705,894 全候補ではなく、hexagon-pass/GT-shadow 294 件である。

対話帳は T-28 まで読了した。本便の全番号節を末尾まで読み、指定された 5 artifact の SHA-256 は実 bytes から 5/5 一致、一次 PRE cert が pin する script/log/input の SHA-256 も 5/5 一致した。IF-FIRST 票 commit `89349a8f31f0b7adf961bbae908fbf6aa09708f7` は当該文書 1 ファイルだけの commit であり、PRE 束 commit `43bcae15db2e265482f989ead6b5d6edd2e596ba` に 12 分先行する。従って事前性・単独 commit 規律は PASS である。補遺 106e、ならびに作業中に還流した裁定 562 の候補非接触 HS 登録 preflight も追加監査対象へ含めた。

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

### F106-2.5　一次提出だけから批准できた分布（補遺前の記録）

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

### F106-2.6　補遺 106e / PENT-LAYER 弱形: PASS

nw7_predictions_addendum_pentlayer_v1.md（SHA-256
89627ea1a108be41e64ca8867e612782b8dce898cdf88f245e594e5aeeec71ac）の設計判断を採る。すなわち、票に必要なのは \(H_W\) 全体の部分群性ではなく、固定した genuine/PENT 基点 \(f_0\) に対する左掛け閉性である。

1. SUB-W は verbal subgroup の一般次数版であり、\(A\subset\gamma_3(P)\) を含む必要な降下を与える。
2. \(h'\in A\) に対し \(E_{0,h'}\) が \(\gamma_2(P)/\gamma_5(P)\) 上恒等となるので、LEFT-TRIV の \(E_{0,h'}(f_0)=f_0\) は類 4 で exact である。
3. 従って \(\operatorname{hex}(m_0)=A f_0\)、かつ \(D(h'f_0)=D(h')D(f_0)\)。\(f_0\) が PENT なら

   \[
   \operatorname{pent}(m_0)=\ker(D|_A)f_0
   \]

   となり、全非空層で同じ個数が出る。

よって Q-2 への回答は **可**。弱形 PENT-LAYER で層間一様移送の要求を満たす。\(H_W\) の部分群性そのもの、ならびに PL-GAP-1 は **UNKNOWN / 非律速**として残す。CONJ-Φ により EXQ-GAP-2 は graded 水準では CLOSED だが、filtered off-diagonal の PL-GAP-2 までは閉じない。

### F106-2.7　corrected PRE-2′ / B-2a: PASS（計器 NOTE つき）

superseding cert nw7_pre12_v2_20260805.json の SHA-256 は
671171a4da7ab59eccce06da18e8a4cd5c6f7785848e63172c1a9ae0414d978d。旧 cert を上書きせず、raw jh3 の値を diagnostic として保存した版である。根拠束は次と byte 一致した。

| artifact | SHA-256 |
|---|---|
| Python honest BCH checker | ff893452ef956a2d093bd63b59eae3f9c94213aeadc713ececb5bb8c6067f151 |
| Python log | a065f65f791f1ec6736a48348ffb90cce298efcff1385ae8dbf37a0e4c9be952 |
| GAP remeasurement script | 601c6f683b73253221662442bfcd5ec55a9bf3b9f4b1fbd77b6949019dcd207e |
| GAP log | 348acf183952136bd10cbfb23b22bff69c6035470b4c6e006690a72e7329d584 |

親側でも Python checker を PYTHONDONTWRITEBYTECODE=1 で再走し、raw 補正係数 \((1,1,1)\)、raw 第二 hexagon 欠陥 \((3,3,3)\)、corrected \(g_1\) の次数 4 成分と欠陥がともに \((0,0,0)\) であることを再現した。GAP log は \(\eta\ne1\)、\(\xi'=D(g_1)=1\)、rank 1、比例 scalar \(k=0\) を記録する。

全ゼロは異常な偶然ではない。PENT-HOM と PENT-LAYER により

\[
D(g_1^a h_4^t)=D(g_1)^aD(h_4)^t=\eta^t,
\]

なので、各層で \(t=0\) の 7 元がちょうど PENT を満たす。従って B-2a は構造的にも整合する。B-0a の六層前件相対で最終表は次である。

| 量 | 最終裁定 |
|---|---:|
| nonempty layers | 6 |
| hexagon / layer | 49 |
| hexagon total | **294** |
| PENT / layer | **7** |
| PENT total | **42** |
| hexagon-only | **252** |
| settled | **294/294 hexagon-pass shadows** |

ただし計器上の非 blocking NOTE が二件ある。

- addendum が恒久要件にした \(g_1\theta(g_1)=1\) と \(\tau^2(g_1)\tau(g_1)g_1=1\) の exact A-membership 前検査は、現 GAP remeasurement script 内にはまだ実装されていない。本件では paper/Lazard と独立 Python 計算が所属を確立するので数学裁定は採択するが、将来の主 wrapper は不一致時 TYPING_FAILURE/STOP を出すこと。
- GAP script の xi_raw-xi_prime == s という表示 sanity は偽であり、正しい関係は \(D(s)=\xi_{raw}\xi'^{-1}\) である。branch 判定には使われず \(\xi'\) の値を変えないが、次の cert では削除または正しい \(D(s)\) 比較へ直すこと。

以上は Python+GAP の同一提出束による **candidate** であり、cross-checked や Lean verified へは上げない。705,894 候補接触は 0、封印量への接触も 0 である。

## F106-3. HS 再 gate 実装束

**判定: PASS（登録 fixture 較正まで。main/unregistered sweep と本走 dispatch は 0）。**

六点 envelope で Luna 106-HS へ委嘱した後、親側の byte/digest、JSON 算術、range cover、ordered-PCGS material、negative fixture の独立再導出に加え、別 agent の敵対監査を通した。F105-2.3 の五点は次のとおり閉じた。

1. **P/S/V wrapper と実 cert。** 三 wrapper は production predicate を呼ぶ runnable path となり、S/V は 13 件、P は 8 件、p=5 control は 5 件の登録 fixture を GAP 4.16.0 上で実行した。current-source v4 aggregate は `overall_pass=true`、S/V/P の UNKNOWN は 0、比較 8/8 true である。
2. **CF/CONV-P 主経路。** V は CF と baseline の (N/N_0) を全登録行で比較し、P は CONV-P と native (Q) 元を element/verdict の双方で比較する。p=5 control も 5/5 一致した。source path/digest は class component に束縛した。
3. **semantic join。** checker は GAP helper を共有せず、flat pair index と ((m,e_1,\ldots,e_6))、P の f-index と六 pair key を manifest の radix から再導出する。人工 join fixture は 15/15、binding matrix v2 は positive 11 と mutant 60 の計 71/71 expectation match であり、改竄は STOP へ落ちる。
4. **versioned prereg / Appendix C。** exact partition は S が 705,894 件を 192 shard（末尾 `[702498,705893]`）、V が 705,894 件を 14 shard（末尾 `[702000,705893]`）、P が 117,649 件を 32 shard（末尾 `[114018,117648]`）に分ける。各 lane は `max-parallel=20`、GAP hard timeout 60 分、job timeout 90 分、欠落・重複・range/receipt/digest 不一致を STOP とする。
5. **候補非接触容量測定。** deliberately invalid な synthetic row 20,000/lane だけを serialize/gzip し、predicate/group 呼出しは 0。線形外挿は raw 344,837,077 B、gzip 17,468,550 B。各 lane cap は 680 MiB、和 2,139,095,040 B は class cap 2 GiB = 2,147,483,648 B 以下、per-shard raw cap は 20 MiB、retention は 30 日である。これは速度・実圧縮率の観測ではない。

current v4 calibration の主証跡は次である。

| artifact | SHA-256 / 値 |
|---|---|
| source provenance commit | `a9a653e9a82f4dd93ca9eabec085a03af931b26e` |
| v4 aggregate | `4dc9464d7e8be153ced72bd19887f5e7f5fad13cd1f714bb54cad410e98db60e` |
| lane S cert / basis FP | `11813961c83d8db77905b54ab0e5eac61b6de935d9f84151371517a2a8c81eea` / `ff2e40c93bf3b547f34dabb0ab7ee6ea1fa2e46dd67bcca43c59fec5158726d3` |
| lane V cert / basis FP | `64215fb4f67955bf035702586968f22456a53b32f6f238b4846d00c53762b7fb` / `eaf54f528795c7831ab4a1b52d4c5e7578f0e93633c2332bfd9428b4b0503889` |
| lane P cert / basis FP | `d786797d563e6b955fd5b77bfa41b69b670e067fd7f7507d8179c9e8a0edfdc9` / `ff2e40c93bf3b547f34dabb0ab7ee6ea1fa2e46dd67bcca43c59fec5158726d3` |

ordered-PCGS material は単なる自己関係ではなく、PQ source path/SHA、ambient `Pcgs(P)` relative orders、named x/y ambient coordinates、六 D-generator ambient coordinates、theta/tau action rows、V の S→V bridge を持つ。rank-2/class-4 の (D=[P,P]) は可換なので、15 commutator rows が全て 0 なのは正しい構造値である。S/P の core fingerprint は一致し、V の bridge も六 unit vector で逐点一致する。

監査履歴は上書きしない。v2 は「交換子行は非自明でなければならない」という誤 guard で FAIL、v3 は条件分岐内の `QUIT;` が GAP 4.16 で callable でなく FAIL であり、いずれも不採択の immutable 記録である。v4 は三 wrapper の当該箇所だけを `QuitGap(0);` に直し、BASIS_ONLY material 書出し直後、candidate constructor/range より前に停止する。

ここで `candidate_universe_contact=0` は synthetic capacity と main/unregistered sweep についての札である。登録 fixture は既知の宇宙元を意図的に評価したため、文字どおりの集合論的「全候補接触 0」とは書かない。本走・未登録 sweep・較正 shard・探索 workflow dispatch は全て 0 である。

## F106-4. BOTTOM-UP freeze blocker 修理束

**判定: PASS / Freeze-2 発効。**

六点 envelope で委嘱した Luna 106-BU 束を親側で差分監査し、self-test を独立再走した。FREEZE-2 の宇宙は次の exact 17 行へ一意化された。

~~~text
layer = V-cen/S3-inflated
p=2: dim in {2,3,4}
p=3: dim = 2
window_order <= 8000
strata = 3 + 3 + 6 + 5 = 17
~~~

p=2 dim 0/1、p=3 dim 0/1/3/4 は cap から暗黙除外せず DIMENSION_OUT_OF_SCOPE/STOP、許容 dimension の order cap 超過は ORDER_CAP_EXCEEDED/STOP とする。traversed/accepted/rejected を分離し、個々の traversal witness を持たせたため、共役類単位の lift 潰しによる分母 alias も防いでいる。

M-ISO-8 erratum も正しい。real と mutant はともに UNKNOWN(NONSHADOW_IN_DATUM) で verdict は不感、kill は witness detail の false/true 比較だけである。過去の IF-FIRST 事前性を遡及生成しないという会計も正直である。

checker self-test は次を再現した。

- positive 1/1 PASS。
- mutant 14/14 が指定 STOP、15/15 expectation match。
- freeze ID、authority、stage unlock、dispatch scope、S3.6 lock の 5 authorization mutant も全て AUTHORIZATION_BINDING_MISMATCH/STOP。
- 実行は schema fixture のみで、探索・候補・kill・EMPTY は 0。

ここに opaque freeze ID

~~~text
W6-BU-FREEZE2-EXACT17-F106
~~~

を発行する。主 digest は次である。

| artifact | SHA-256 |
|---|---|
| authorized manifest | 2818c0aceb2948750df84f3df5c6a63df12c477bf73681690cb06e7c00a82376 |
| checker | ef44d52c0eeda48a3fd5290b1185bedc39a30121006be9b91051d50ec27246b4 |
| fixture receipt | 36dcfea73ae5a078d52592455d86f0ed38089fddf3a6990d94b81b93cb5de26f |
| positive fixture | 9299c3c4e8a17177334d7eae847a6a3576d0b06ba95521ae45ed3b942e6acb04 |
| 15-fixture aggregate | d6644b65a2bc5aeee3a0280a86bb979a0fe6a1b2c8572841b0b91536d1cd6511 |

状態遷移は **S1–S3.5 = 将来の workshop-only dispatch に限り eligible、S3.6–S9 = LOCKED**。本便ではいずれも実行していない。この freeze は W-5、ISO route 2、kill/EMPTY、候補不存在を昇格させない。

## F106-5. Standing class manifest と小 gate

**class freeze 判定: PASS。main-run authorization: 条件付き PASS（工房専権）。**

小 gate の対象を次の一個へ固定する。

~~~text
class_id = HS-NW7-CLASS-v3-draft-2c5c1559812c5d9b
draft manifest = search/certs/hsp7_class_manifest_v3_draft_20260805.json
draft SHA-256 = 48364db7d82aa8000096058f07c321a2003ada6655d84cd4544548428d37e31b
component bundle = 2c5c1559812c5d9b8dccd9f0ca5b74a7d288fc18508c3872dea3f2c3798c02d7
status = READY_FOR_SOL_FREEZE_REVIEW
authorization = all false
~~~

class ID に歴史的文字列 `draft` が入るが、shard manifests がこの exact ID を pin しているので rename しない。F105-4 の五要件は、(1) 45 component の source-map/digest、(2) exact universe・semantic-key bijection・range、(3) STOP/UNKNOWN・timeout・join 規則、(4) exposure/negative registration/cap/retention、(5) preflight schema と current-source v4 class calibration receipt、の全てが単一 bundle に束縛されている。static audit は 35/35、binding matrix は 71/71、親の current-draft `--preflight-only` 再走も S/V/P 全て candidate evaluation 0 で PASS した。

従って監査上の freeze approval ID として

~~~text
HS-NW7-FREEZE1-2c5c1559812c5d9b-F106
~~~

を発行する。ただし、これは現在の draft bytes を直接 dispatchable に変える札ではない。main run の発効には工房が次の機械条件を逐語的に履行することを要する。条件をそのまま履行する限り再度の数学監査は不要である。

1. exact draft/components を保持した新しい versioned frozen manifest を作り、status を `FROZEN_AUTHORIZED`、`main_run=true`、`workflow_dispatch=true` とする。`calibration_shard=false`、`claim_grade_promotion=false` は維持する。
2. frozen file の新しい SHA-256 を計算する。上記 draft SHA を流用しない。
3. exact template を `.github/workflows/hsp7-mainrun-class-v3.yml` へ設置し、承認済み二 sentinel だけを frozen path/new SHA に置換する。normalized digest `41b29577479b51a4b9b3b06ffb4d62465afb2e256fab96c42714518dec6615cd` を維持し、`class_lock_checks` を通す。
4. 全参照 component/manifest/cert と frozen workflow を一緒に commit する。設置・探索 dispatch は工房だけが行う。
5. dispatch 前に frozen path/SHA に対する fresh `--preflight-only` receipt を S/V/P で採り、candidate evaluation 0 と manifest binding を確認する。現在見える draft-path receipt を最終 receipt として流用しない。

source/schema/range/cap/output/STOP 規則または normalized workflow digest の変更、登録 range 外、封印隣接量、S9、claim-grade promotion は再 gate とする。本走 shard cert を freeze の前件に置くのは循環なので要求しない。run receipt には GAP 4.16.0 と ANUPQ 3.3.3、および resolved action revision を記録する。`install-pkg@v1` が暗号学的 dependency pin でない点は、pre-shard fingerprint mismatch が STOP するため NOTE に留める。

## F106-6. Lean 親子方式・GitHub broker

### F106-6.1　plain Lean 第 1 束: local PASS（GHA は F106-6.4）

実装順 hygiene → H → A → E は守られた。親側の再走でも、bare lake build を使わず

~~~text
lake build P1
lake env lean P1/AxiomCheck.lean
~~~

がともに exit 0、最終 marker は

~~~text
P1_AXIOM_AUDIT_PASS|modules=8|theorems=180|manifest=P1/AXIOMS.manifest.json
~~~

となった。静的 scan でも実 axiom/sorry/admit/:True no-op は 0。warning は unused simp/section variable の linter だけである。

AxiomCheck は ShadowAxioms を含む current 8 module を import・列挙し、全 P1-owned declaration を走査する。未使用 project axiom、definition に潜む sorryAx、許可外 axiom、旧 T2 名の復活を fail-closed に止める。180 theorem row は名前順・重複なしで、各 metadata-free type digest と exact sorted axiom set を持つ。許可集合の和は Classical.choice / propext / Quot.sound、project axiom declaration は空である。

主要 receipt は次である。

| artifact | SHA-256 |
|---|---|
| AxiomCheck.lean | f605fd82efd1540abc8a38c9d22384369a06e08f73a3339070fad4209203cfa3 |
| AXIOMS.manifest.json | 049e8452c8d56acbbbf9656e2c9554da7e8d1380fe7c0c1cd97427fd49c4d6dd |
| AxiomAudit.receipt.md | 6e385656f78d5406d93f90be3d94e3fca54bd913e3713835218ec03bc9cfd3c0 |
| PAPER_STATEMENT_MAP.md | 27005fb3cf3a6f513ee3c54f418bef62880bcffcbd7f71997426193b9b53cb56 |
| BlockH.lean | a3f21551e74049f3a60a9cde95d3152b6046102532eda8856a75368902232bde |
| BlockA.lean | 427152999e23d10b4da1200743261679b00d047eda1907b4ae141a5dfc3a8733 |
| BlockE.lean | d7cb27e4aecf51501805b48eb900fb27d181897fecdda03c950edac0727dd241 |

### F106-6.2　paper fidelity の裁定

- **Block H: PASS（抽象 theorem island）。** \(m\) は faithful regular action、比較側 \(\tau\) は faithful action のみで、紙の LH-1 より強い regularity を \(\tau\) に仮定しない。generator 上の conjugacy から唯一の automorphism を作り、explicit \(C_M=\mathrm{Fin}\,M\) では唯一の \(b\in(\mathbf Z/M\mathbf Z)^\times\) へ typed adapter で接続する。character fitting は 0。
- **Block A foundations: PASS（指定範囲）。** \(G_n=\{x\in E_n:\operatorname{par}(x)=0\}\) を実 subtype とし、積・単位・逆・群則、\(X_g\in G_n\)、実 subtype 上の \(xpowGn\) と \(\operatorname{ord}(X_g)=2n\) を閉じた。cardinality は \(G_n\simeq(\mathrm{Fin}\,n)^3\times\mathrm{Bool}^2\) の constructive witness と算術式であり、literal Fintype.card theorem ではない。Lambda は real conjugacy-class type と existence/uniqueness statement までで、index/normalizer 前件と proof は OPEN。
- **Block E: PASS（算術核だけ）。** chiTilde_welldefined、chiTilde_isUnit、整数 (3.49) と mod consequence は閉じた。GT-shadow composition、Ihara decomposition、cyclotomic surjectivity、SURJ-Split 全体は OPEN。

従って「P1 全紙面 verified」ではない。LA-2〜LA-5/7/9、full INN automorphism、Lambda-REG proof、LE-1(b)〜LE-4、Bridge B は未閉鎖である。local build は candidate、判定正本は GHA である。

### F106-6.3　T2 一枚表の PDF 画像監査

Luna の表を原 PDF のページ画像で照合した。

| 候補 | 画像裁定 |
|---|---|
| 2405.11725 Thm 4.3 / (4.12) | printed/PDF p.18。\(n\ge3\)、二つの \(4\mid n\) 分岐、\(\mathcal X_n\)、\(\varkappa\)、isolated 結論を確認。PASS。 |
| Ihara (1.5) | printed/PDF p.4。\(g\mapsto((\chi(g)-1)/2,f_g)\) と \(\widehat{GT}\)、さらに \(\widehat{GT}_{gen}\) への包含を確認。PASS。 |
| 2401.06870 Thm 3.10 / (3.53) | **printed/PDF p.18**。初稿表の p.17 は前命題末尾なので訂正済。三 object、共通 \(N_{\rm ord}\)、\(m_{12}=2m_1m_2+m_1+m_2\)、\(f_1E_{m_1,f_1}(f_2)\) を確認。PASS。 |

これは locator と最弱 conclusion の requirements sheet の批准である。implicit quotient equality、GTSh object index、Ih の具体 domain/codomain を Lean type として一意化する作業はまだ OPEN なので、四つの T2 declaration を import 経路へ戻す認可ではない。現 ShadowAxioms の comment-only quarantine を維持する。

### F106-6.4　workflow proposal と broker 状態

工房の便 106f は proposal を二条件つきで承認した。(i) push/pull_request の path filter を `lean/**`, `lean-arith/**`, workflow 自身へ限定、(ii) raw axiom scan は `ShadowAxioms.lean` だけを除外し、typed axiom policy は AxiomCheck manifest で fail-closed に担う、である。両条件を反映した proposal SHA-256 は

~~~text
d61796aadad70af56957669667958ba56a209ef1b81e865cf820a7ead64cce23
~~~

で、`.github/workflows/lean.yml` はその bytes と一致する。作業 branch `sol/task106-math33-20260806` の Lean/workflow commit は `120b21c121e41d81651e896101c83cfd2bb6854f`。最初の push は token の workflow permission 不足で reject されたが、研究者による権限修復後に同じ非 force-push 経路で成功し、credential をファイル・返信・ログへ書いていない。

手動 `workflow_dispatch` run `31021842884`（head `120b21c...`）は三 job 全て success である。自動 push run `31021839716` も三 job success で一致した。手動 run の証跡は次のとおり。

| job/artifact | 結果 |
|---|---|
| existing Lean targets / artifact 8936979725 | Marking+K3、15 jobs success。log SHA `ef423ec8895cd796233739c22bd09a6434dd0c96d291febf2d4d006f73b3e87a` |
| lean-arith / artifact 8936979634 | 2053 jobs success。log SHA `09d5fba6881aaf3309f863adac80f9e69c1379764668af4cf1667ba128641667` |
| P1 axiom manifest / artifact 8936943790 | P1 11 jobs success、8 modules/180 theorems。build log SHA `503cfaeef5f3cabc9d5152c5de30d5570f8276a14b5fc97b14fa0cff303a6dbd`、audit log SHA `4b692aa681b724acacf9c7a3681e2c6412e4301e9274a2e67a51b80f65b598a5` |

GHA artifact の `AXIOMS.manifest.json` SHA は local の `049e8452c8d56acbbbf9656e2c9554da7e8d1380fe7c0c1cd97427fd49c4d6dd` と一致した。sorry/native fallback はなく、K3 の表示 axiom は propext/Quot.sound、P1 全体の許可集合は §6.1 の三公理である。従って GHA を判定正本として、実装済み theorem island は各 manifest の公理集合に相対して verified と呼べる。ただし §6.2 の paper-fidelity 境界を越えて P1 全紙面を verified とはしない。

## F106-7. 共有・最終状態遷移

本便での状態遷移をまとめる。

- P1: 限定 FAM-U-ASM 発効への異議なし。ただし「campaign が candidate である唯一の理由」という旧 bundle の過大記帳は F106-1.1 の erratum を正本とする。
- NW(7): 旧 PRE-2/B-2b は typing failure の不採択記録。corrected PRE-2′ は B-2a、B-0a 前件相対の予言は hexagon/PENT/hexagon-only = **294/42/252**、採点分母は 294。
- BU: `W6-BU-FREEZE2-EXACT17-F106` 発効。S1–S3.5 は将来の workshop-only dispatch に限り eligible、S3.6–S9 は LOCKED。
- HS: `HS-NW7-FREEZE1-2c5c1559812c5d9b-F106` の class-freeze 監査 PASS。本走は F106-5 の工房側五条件を満たした後だけ条件付き認可。Sol broker は探索 workflow を設置・dispatch していない。
- Lean: approved workflow を branch へ push し、manual run `31021842884` と push run `31021839716` はともに三 job PASS。master merge は工房検収事項である。

Git broker は作業 branch

~~~text
sol/task106-math33-20260806
~~~

だけを用い、force-push と master 直 push は 0。Lean/workflow commit は `120b21c121e41d81651e896101c83cfd2bb6854f`、HS source commit は `71e9e2d03ff3c0ee8ff4c01a1cdb72e5d2af2f7b`、GAP 4.16 callable-exit 修理の superseding commit は `a9a653e9a82f4dd93ca9eabec085a03af931b26e` である。残る versioned docs/certs、BU 束、Luna envelopes/replies と本返書の artifact commit は、この返書末尾の final provenance 行へ記帳する。

本走、未登録 sweep、掘削、kill、d 測定、BU stage、HS calibration shard、S9 は実行していない。登録 fixture calibration と synthetic candidate-0 preflight/capacity だけを実行した。封印三量は非接触、探索統計は exploration-heuristic のままである。

**Final provenance:** 実装・監査 artifact commit = `b33d95802e28f59bef51ec195c37acc9bec3e8ce`（branch `sol/task106-math33-20260806` へ non-force push 済み）。本返書自身はこの SHA を記帳する後続 reply-only commit に置く。

## F106e. 補遺 106e 再配達の全節再検収

**再検収判定: PASS（F106-2.6/2.7 の裁定と最終分布に変更なし）。** `ops/inbox_codex/sol_task_106e_supplement.txt` は 26 行を末尾まで再読し、SHA-256 `b758ca7a8c719853b44fc5bcda58994ee77b5cac0b20ee4254c0604a9fb4c6e5` を得た。以下、番号節 1〜4 の順に再回答する。

### F106e-1. PRE-2′ 再測定: PASS / B-2a

raw \(jh3\) の次数 4 成分 \((1,1,1)\) と第二 hexagon 欠陥 \((3,3,3)\)、補正 \(g_1=r s^{-1}\) の次数 4 成分・欠陥 \((0,0,0)\)、\(\eta\ne1\)、\(\xi'=D(g_1)=1\)、比例 scalar \(k=0\) は F106-2.7 の再現結果どおりである。全ゼロは

\[
D(g_1^a h_4^t)=D(g_1)^aD(h_4)^t=\eta^t
\]

から構造的に説明され、異常値ではない。従って \(\ker(D|_A)\) は位数 7、B-2a を維持する。

superseding cert の SHA と、それが pin する Python script/log・GAP script/input/log の実 bytes を再照合した。cert 自身を含めて 6/6 の SHA は一致した。ただし cert の `input_artifact` 値は

~~~text
search/probe/hsp7_cond4_laneP/PQ_OUTPUT_Q_laneP.g (pre-existing, not regenerated, not modified)
~~~

と注釈まで同じ JSON string に入っているため、汎用 path resolver ではそのまま解決できない。正しい path `search/probe/hsp7_cond4_laneP/PQ_OUTPUT_Q_laneP.g` の実 SHA は宣言値 `bfb71c2167d2936fa135f0aa6345f23843cf4239984d5fb6155ce0753620ab8b` と一致する。これは数学結果を変えない provenance NOTE だが、次版では path と note を別 field にし、path field を機械可読な exact path にせよ。

また `TYPING_FAILURE/STOP` は仕様化されたが、現 GAP script は \(g_1\) と \(h_4\) の二 exact A-membership 等式をまだ実装していない。この点は F106-2.7 の非 blocking NOTE を維持し、将来 wrapper の恒久条件とする。

### F106e-2. PENT-LAYER の設計判断: 可 / PASS

Q-2 への回答は再度 **可**。層別個数に必要なのは \(H_W\) 全体の部分群性ではなく、PENT 基点 \(f_0\) に \(A\cap H_W=\ker(D|_A)\) を左から掛ける閉性で足りる。SUB-W、LEFT-TRIV、COSET-EXP により

\[
\operatorname{pent}(m_0)=\ker(D|_A)f_0
\]

が exact に従うため、全非空層の個数は一様である。\(H_W\) の部分群性と PL-GAP-1 は UNKNOWN / 非律速のまま、D-5 の lift 存在形は持ち込まない。CONJ-Φ による EXQ-GAP-2 の CLOSED は graded 水準に限り、filtered 非対角成分 PL-GAP-2 は OPEN とする。

### F106e-3. 分布充填: PASS

B-0a の六層非空前件の下で、最終表は次で固定する。

| 量 | 値 |
|---|---:|
| hexagon / layer | 49 |
| hexagon total | 294 |
| PENT / layer | **7** |
| PENT total | **42** |
| hexagon-only | **252** |
| settled | **294/294 hexagon-pass shadows** |

`settled 100%` の分母は 294 であり、705,894 の全 candidate pair ではない。

### F106e-4. 規律・履歴: PASS（commit 表現 NOTE）

705,894 candidate pair の評価、本走、封印量への接触は 0。旧票・旧 script・旧 cert は不改変で、v2 は superseding artifact として追加されている。履歴上、PENT-LAYER addendum は単独 commit `5bcddfbcfd2e775bbdb756adc4daf2c404738d62`。一方、v2 cert・二 script・二 log は裁定 ledger と同じ commit `e7853b3ccc06628f574e990374a62e248217f3c1` の 6-file bundle である。従って後者を「単独ファイル commit」とは呼ばず、「一個の versioned release bundle」と記帳する。実 bytes と cert の pin は一致しており、事前分岐 B-2a/B-2b の登録性は変わらない。

\(\mathfrak h_3/h_3\) 区別の ledger 追記は再発防止として妥当だが、補遺 §4 の「追加予定」は 106e 束自身の証拠ではない。後続版での物理化・検収とは分け、106e の裁定根拠には数えない。

## F106f. Lean workflow 承認便の全節再検収

**再検収判定: PASS（承認範囲と修正条件 2 件は履行済み。注記の path-filter 解釈には訂正 NOTE がある）。**

監査対象便は `ops/inbox_codex/sol_task_106f_workflow_approval.txt`（14 行、SHA-256 `024660cc0ab87861f09816a66ba2081559b01af9f3f3a853d3d0534d2497e504`）。第 1 行から第 14 行まで再読した。

### F106f-1. 承認範囲: PASS

条件反映後の proposal と `.github/workflows/lean.yml` は byte-identical（各 5,681 bytes、SHA-256 `d61796aadad70af56957669667958ba56a209ef1b81e865cf820a7ead64cce23`）。適用 commit は `120b21c121e41d81651e896101c83cfd2bb6854f`、push・dispatch 対象はいずれも作業ブランチ `sol/task106-math33-20260806` である。force-push は行わず、2026-08-06 再検収時点で当該 commit は master `8ef08bde7de00c26f83baba09d1273f1dc3e28be` に未包含であり、「master merge は工房検収後」を維持している。

### F106f-2. 修正条件 1 — path filter: 字面 PASS / 意味論 NOTE

`on.push.paths` と `on.pull_request.paths` はともに、指定どおり次の 3 path のみに限定され、`workflow_dispatch` も維持されている。

- `lean/**`
- `lean-arith/**`
- `.github/workflows/lean.yml`

ただし便 106f §注記第 2 項の「`lean-arith/` package が未作成の間は path filter により mathlib job は発火しない」は GitHub Actions の意味論としては成立しない。`on.<event>.paths` は個別 job ではなく workflow run 全体の起動条件であり、現 workflow の `mathlib-cache-targeted` job に package 存在・変更有無を判定する job-level `if` はない。実際、commit `120b21c...` は `lean-arith/**` を変更していないが、`.github/workflows/lean.yml` / `lean/**` の変更により push run が起動し、三 job 全てが走った。また当該 package 自体は既に commit `3e538d3ca4254762c5b723e40f799398966e55bb` から存在するため、「未作成期間」の同一ブランチ実証も今回の履歴にはない。

これは条件 1 の literal 適合を覆さない設計 NOTE である。将来「package 不在または非変更なら mathlib job だけを抑止」を要件にするなら、changed-path/package-existence を判定する job-level `if`、または workflow の分離が必要である。

### F106f-3. 修正条件 2 — axiom allowlist 分担: PASS

axiom scan は `rg -n '^\s*axiom\b' P1 -g '*.lean' -g '!ShadowAxioms.lean'` で、除外は `ShadowAxioms.lean` のみである。typed axiom の許可境界は `AxiomCheck.lean` の theorem ごとの exact manifest が担う。あわせて、

- `sorry` / `admit` の source scan、
- no-op `True` placeholder の source scan、
- build log 中の `uses 'sorry'` / `sorryAx` / `ofReduceBool` / `ofReduceNat` scan

を維持し、今回の source と実 run log はいずれも clean であった。なおこれは P1 の exact axiom inventory と現 build の証跡であり、今後追加される任意 target 全体について `native_decide` 構文を source-level に一律禁止する checker まで実装済み、とは過大主張しない。

### F106f-4. 注記の初回実 run 検収: PASS

manual dispatch run `31021842884`（attempt 1、head `120b21c...`）は completed/success。job と artifact は次のとおり。

| job | job ID | 結果 | artifact ID |
|---|---:|---|---:|
| `existing-lean-targets`（`lake build Marking K3` を明示実行） | `92360265823` | success | `8936979725` |
| `p1-plain-targeted` | `92360265868` | success | `8936943790` |
| `mathlib-cache-targeted` | `92360266210` | success | `8936979634` |

同 head の push run `31021839716` も completed/success で、三 job 全て success。従って Marking+K3 の明示 build、P1、lean-arith の初回 branch 実挙動は取得済みである。この PASS は branch CI と承認便 106f の適用ゲートに限り、master merge、P1 全体の紙上定理化、または将来 target の包括的 soundness 承認を意味しない。
