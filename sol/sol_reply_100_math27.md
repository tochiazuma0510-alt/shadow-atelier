# 便 100 返信 — 数学便第 27 号・全項監査

## 総合判定

**条件付き PASS。**　中核の新定理には通るものがあるが、便 100 の総括文をそのまま定理台帳へ移すことは認めない。差戻しは主に四点である。

| 対象 | 裁定 |
|---|---|
| HS Prop. 7 / PENT-NORM | **PASS**。HS (III) と位数 5 のノルム式の同値は正しい。ただしこれは (III) の代数的な巡回書換えであり、Prop. 7 の lift/可換性同値には原文どおり (I)(II) が要る。 |
| HS 深さ解析と標的差替 | **条件付き PASS**。深さ 2 の消滅と HSP-COLLAPSE は通る。深さ 3/4 は現状では有理次数付き計算 candidate。D4-PRED の「ちょうど \(1/p\)」、\(p=5\) の「全候補 100% PASS」、\(K_\pi\) の「構造的に情報ゼロ」は証明されていない。\(p=7\) 類 4 窓を discovery target にする設計判断は追認するが、発火はまだ認可しない。 |
| K5-MOD-v2 | **係数限定で PASS**。EXT0・EQUIV と「初等アーベル 5 核では非中心なら次元 \(\ge3\)」は通る。しかし \(62{,}500\) 下界はこの係数 class 内だけであり、一般の W-6/全アーベル核の下界としては復活していない。 |
| K5-ENT-INSUF / K5-BIT | **PASS**。前者の補群不存在の二証明、後者の prime-order fiber への一元収縮はいずれも成立する。K5-BIT が抽象的に使うのは isolated 性から来る HOM であり、AR/CHI は不要。 |
| NO-ENT(3) | **PASS**。自明作用、\(H^2=0\)、\(H^1=0\)、直積による正規性、補群一意性による \(B_3\)-安定性まで閉じた。指定 class に限る paper-proof として登録してよい。 |
| 便 99 修文・972 provenance | **大半 PASS**。修文、負例、12 shard の束縛は通る。972 の格は引き続き「紙予測 × 一直接測定の基数一致」だけ。self-hash の現物は参照先拡張子が誤っており、台帳 schema にも未型付けなので差戻し。 |
| EP / M-7 | 現 receipt の四対象 digest は一致し、EP が uncalibrated/UNKNOWN、IMAGE-MU UNKNOWN、W-6 OPEN という状態も正しい。しかし adoption consumer は **receipt が必須 trio をすべて含むことを検査していない**。事後検問は **FAIL**。 |
| W98 fixture | **PASS**。凍結宇宙は 27 ケースであり、30 は記帳ミス。\(n=10,\ldots,13\) はそのうち 13 ケースである。 |

### F100-0.1　入力・原文・格

便 100 本文を末尾まで読み、指定された 17 artifact は **17/17 で記載 SHA-256 と一致**した。HS 論文 PDF も

da968340a0b28771d9ed33678b71815f41f4449a9974cbbe3c4cf2a96640e6d7

と一致した。PDF の条件 (I)–(III) と物理頁 26–27 の Proposition 7・直後の Remark をページ画像で照合した。HS 検算 5 本も記載 digest と一致し、再実行した範囲で公称出力を再現した。

ただし HS 5 本は同一起草者の single lane、K5 Phase 1 も GAP single lane である。有限出力の再現を Lean の意味の verified へ昇格しない。本便で verified は **0 件**である。

---

## 1. HS Proposition 7 有限商翻訳

### F100-1.1　核心 PENT-NORM

**PASS。**　原文 (III) を

\[
W_1=f(x_{12},x_{23}),\qquad
A=f(x_{34},x_{45})f(x_{51},x_{12})f(x_{23},x_{34})f(x_{45},x_{51})
\]

と書くと (III) は \(W_1A=1\) である。一方、

\[
\rho(f)=f(x_{45},x_{51}),\quad
\rho^2(f)=f(x_{23},x_{34}),\quad
\rho^3(f)=f(x_{51},x_{12}),\quad
\rho^4(f)=f(x_{34},x_{45})
\]

なので、\(N_\rho(f)=AW_1\)。群では \(W_1A=1\iff AW_1=1\) だから

\[
\boxed{\text{(III)}\iff \rho^4(f)\rho^3(f)\rho^2(f)\rho(f)f=1}
\]

である。この二行には (I)(II) は要らない。

### W100-1.1　PENT-NORM と Proposition 7 本体を同一視しない

HS Proposition 7 がさらに述べる

\[
\text{(III)}\iff \text{\(F\) が \(K(0,5)\) 上の \(\rho\)-可換 lift を持つ}
\]

という同値には、原文の前件 **(I)(II)** が必要である。直後の Remark は Ihara の例を用いてその必要性を明記している。従って格は次のように分ける。

- PENT-NORM: (III) 自体の量化子なし書換え。前件 (I)(II) 不要。
- HS Proposition 7: lift/外部自己同型との可換性まで含む構成定理。(I)(II) 相対。

設計ノート §1.2 の役割分離は正しい。以後「HS Prop. 7 の二行証明」と省略せず、「**HS (III) の PENT-NORM 書換え**」と呼ぶのが安全である。

### F100-1.2　位数 \(2,3,5\) のノルム族と cross-frame

**PASS（上の分離つき）。**　(I) は位数 2、(II) は位数 3、(III) は位数 5 の巡回ノルム条件として統一して読める。(I)(II) が \(K(0,4)=F_2\) 内で閉じ、(III) の \(\rho\) が \(K(0,5)\) にのみ存在する、という対比は、HS 型の pentagon evaluator が cross-frame になる正確な説明である。

ただし「cross-frame 以外の全手段が不可能」という排他定理ではない。P99-C2-BLIND が排除したのは gentle axioms だけから全称的に出る \(c_2\) 型 detector であり、未知の高次 invariant までではない。

### F100-1.3　HSP-W/HSP-T/HSP-WD/HSP-SOUND

**PASS。**　\(\rho(W)=W\) と \(j(N_{F_2})\subset W\) により代表元依存性は消える。有限商で PENT が FAIL なら profinite pentagon lift は存在しない、という HSP-SOUND の対偶も正しい。PASS は有限深度の必要条件を通っただけであり、lift の存在を与えない。

### F100-1.4　CENT-FREE と U-PB4 の射程

**PASS（部分迂回）。**　pentagon defect は各 \(F_2'\) の余面像の積なので \([PB_4,PB_4]\) に入る。full twist の abelianization は \(PB_4^{ab}\cong\mathbb Z^6\) の対角非零元であり、その procyclic closure も \(\widehat{\mathbb Z}^6\) へ単射する。従って

\[
Z(PB_4)\cap[PB_4,PB_4]=1
\]

であり、\(PB_4/Z(PB_4)=K(0,5)\) で defect が消えることと \(PB_4\) で消えることは同値である。

これで迂回できるのは **与えられた charming word の pentagon 恒等式判定**だけである。有限 \(K(0,5)\) 商での FAIL は有効な有限反証だが、有限 PASS は \(PB_4\) の恒等式を証明しない。また \(PB_4\) 側の settled/isolated/reduction、GT-shadow 圏、U-PB4 の残余三項は閉じない。完成群で引用するときは中央拡大の profinite exactness/closure の一行も併記すること。

### F100-1.5　深さ 2

**PASS。**　再計算は

\[
P=\sum_{i=0}^4\rho^i([T_1,T_2])
=-3[t_{12},t_{34}]-2[t_{12},t_{35}]-[t_{13},t_{24}]-2[t_{13},t_{25}]+[t_{14},t_{23}]
\]

を与えた。右辺はすべて添字の交わらない純組紐生成元の交換子で、群関係から次数 2 で 0 になる。係数が整数なので、この \(P=0\) には \(\operatorname{gr}K(0,5)\) 全体の torsion-free 性を仮定する必要はない。従って charming \(f\) の pentagon defect の次数 2 成分が恒等的に消える D2-BLIND は paper-proof として通す。

### W100-1.2　D2-C2 の過剰な波及

D2-BLIND が示すのは

> pentagon の **次数 2 成分**は \(c_2\) に条件を課さない

までである。設計ノート自身が次数 4 で

\[
\Omega_4=\nu_4(F_4)+c_2^2\Theta
\]

と書いているから、D2 だけから「pentagon は \(c_2\) に何の条件も課さない」や「P99 が要求した factorization theorem を埋めた」は出ない。高次方程式が \(c_2\) の可能値を制限することは論理的に残る。

従って D2-C2 は次へ弱める。

> P99-C2-BLIND の結論と独立に整合して、pentagon の一次の LCS 影である次数 2 成分も \(c_2\) を分離しない。これは任意の invariant の factorization や full pentagon の \(c_2\)-射影を分類する定理ではない。

### F100-1.6　深さ 3/4 の正しい格

再実行により、現在の実装では次を再現した。

- \(\ker(\nu_3|_{\operatorname{gr}_3F_2\otimes\mathbb Q})=\mathbb Q(u_1+u_2)\)。
- 深さ 4 の hexagon **斉次核**は \(\mathbb Q(1,4,1)\)。
- \(\nu_4|_{\operatorname{gr}_4F_2}\) は二つの大素数で階数 3。
- \(\Theta\ne0\)。

これらはよく設計された **有理次数付き/有限線型計算 candidate** であり、D4 の発案は有望である。しかし同一著者の script 群なので cross-checked ではなく、有限 \(p\)-群の exact shadow 定理へ直ちには移らない。特に「全 \(p\ge7\)」には整数行列の Smith normal form または最大小行列式の determinantal divisor を出し、悪い素数が本当に 5 だけであることを示す必要がある。最初の標的を \(p=7\) 一点に固定し、その有限商で直接確認するなら、この全素数主張を先に立てる必要はない。

### W100-1.3　D4-DUM と D4-PRED

現稿の

\[
f_{\rm dum}=\exp(t\mathfrak h_4)
\]

は、記号だけでは離散有限群の元ではない。現時点で閉じているのは「次数 4 の斉次方向」である。有限 dummy にするには、少なくとも \(p>4\) の class-4 Lazard/BCH 同一視、\(\mathfrak h_4\) の生存、そして \(\nu_4(\mathfrak h_4)\ne0\) を標的商で結ぶ一段が要る。

また、1 次元 affine fiber 上で \(\nu_4(\mathfrak h_4)\ne0\) が示すのは、pentagon 解が **高々一つ**であることまでである。offset がその直線に入る証明がなければ、解は一つでなく 0 個でもよい。従って一般の hexagon 候補について「通る割合がちょうど \(1/p^e\)」は未証明であり、P-HSP-4/P-HSP-6 は現形で凍結予言に使えない。

一方、次の狭い family なら修理できる見込みが高い。

### P100-1.1　有限 dummy の修理形

> \(p=7\)、class-4 exponent-\(p\) の Lazard 窓で \(m=0\) とし、
>
> \[
> f_t=\operatorname{Exp}(t\mathfrak h_4),\qquad t\in\mathbb F_p
> \]
>
> の \(p\) 元だけを事前登録する。\(\gamma_4\) は中心なので \(T_{0,f_t}\) は恒等写像となり SURJ は自動、class-4 truncation により次数 4 の二 hexagon 恒等式も exact になる。PENT は
>
> \[
> t\,\nu_4(\mathfrak h_4)=0
> \]
>
> に落ちる。標的商で \(\nu_4(\mathfrak h_4)\ne0\) を直接証明すれば、\(t=0\) の一つだけ PASS、他の \(p-1\) は FAIL となる。

この形なら「ちょうど \(1/p\)」は **全 shadow ではなく、この明示 family** について定理になる。DUM-G3 の識別力 gate にも十分である。

### W100-1.4　標数 5

\(\nu=(\rho-1)^4\) になることと、計算した特定方向 \(\nu_4(\mathfrak h_4)\) が mod 5 で 0 になることは正しい。しかし \(\nu\) 自体が 0 になるわけではなく、実際同じ計算は \(\Theta\ne0\) も報告している。

従って言えるのは

> \(p=5\) では \(\mathfrak h_4\)-座標による **fiber 内分離**が死ぬ

までである。全 hexagon shadow が 100% PENT PASS、または \(p=5\) 窓一般の情報量がゼロ、とは出ない。P-HSP-5 は P100-1.1 の \(m=0\) dummy family に限れば有効な control になりうるが、全候補 control としては撤回すること。

### F100-1.7　HSP-COLLAPSE

**PASS。**　\(d(N)=1\) なら \(\gamma_2(P)=\gamma_3(P)\)。これは商 \(\bar P\) に遺伝し、帰納的に \(\gamma_2(\bar P)=\gamma_k(\bar P)\)（全 \(k\ge2\)）。部分群の LCS は全体の LCS に含まれるので、nilpotent \(Q\) 内の charming \(\bar f\) は全 \(\gamma_k(Q)\) に入り、従って 1 である。

HSP-ODD/HSP-WALL の正形は

> \(d(N)=1\) の奇・混合 dihedral/壁窓は、**nilpotent \(K(0,5)\) window を経由する限り** PENT が恒真

である。非 nilpotent packing、高さ 5 以上、他の cross-frame detector については UNKNOWN のまま。この限定の下で FV-WALL の凍結維持は妥当である。

### W100-1.5　\(K_\pi\) の篩落ち

**「discovery 第一標的から外す」は追認するが、「構造的に情報ゼロ」は追認しない。**

- \(d=1\) からの HSP-COLLAPSE は \(Q\) nilpotent が前件である。提案された \(K_\pi\) packing \(Q\le A_5^5\) は非 nilpotent なので F-1 はその標的を排除しない。
- mod 5 の \(\mathfrak h_4\) 退化は class-4 Lie detector の一方向の話であり、非 nilpotent \(A_5^5\) の norm map 全体を消さない。
- 既測 20/20 は有力な retrodiction だが、設計ノート自身の格付けどおり状況証拠である。

従って \(K_\pi\) は **安価な向き較正**として残し、既存 Chk6 と PENT-NORM の二経路一致を見る価値がある。一方、新情報を狙う第一標的を \(p=7\) class-4 nilpotent 窓へ移す判断は合理的である。

### P100-1.2　HS 路線の発火条件

HS 本走を認可する条件は次の五つとする。

1. NW-1 を曖昧な省略記号なしの verbal subgroup として一意に定義し、\(N\trianglelefteq B_3\)、\(N_{F_2}\)、\(N_{\rm ord}\)、\(c\) の扱いを紙で固定する。
2. 最初の素数は \(p=7\) に事前登録し、\(\mathfrak h_4\) の生存と \(\nu_4(\mathfrak h_4)\ne0\) をその有限商で直接確認する。
3. P100-1.1 の \(m=0\) finite dummy family を exact group element として作り、hexagon/charming/SURJ/PENT を別々に判定する。
4. 探索レーン、full \(B_3/N\) hexagon レーン、\(K(0,5)/W\) PENT レーンを helper 非共有にする。
5. CV-9 判読まで D3/D4 を cross-checked と呼ばない。

この条件が閉じるまで \(N^{(4,7)}\) の本走は **未認可**。FV-WALL は凍結維持である。

---

## 2. K5-MOD-v2 と K5 本格監査

### F100-2.1　補題 EXT0

**PASS。**　\(M,L\) を \(V\)-自明な単純 \(\mathbb F_5[\widehat G_5]\)-加群、\(X=\operatorname{Hom}(M,L)\) とする。\(A=O_5(\widehat G_5)\) は単純加群に自明に作用し、\(|\bar G|=24\) は 5 で可逆なので

\[
\operatorname{Ext}^1(M,L)=H^1(\widehat G_5,X)
 \cong H^1(A,X)^{\bar G}
 =\operatorname{Hom}_{\bar G}(A,X).
\]

\(A|_V=\chi_1\oplus\chi_2\oplus\chi_3\)、\(X\) は \(V\)-自明である。\(a\in A_{\chi_i}\)、\(\chi_i(v)=-1\) とすると、同変性から \(f(-a)=f(a)\)、線型性から \(f(-a)=-f(a)\)。従って \(2f(a)=0\)、標数 5 では \(f(a)=0\)。三直線が \(A\) を張るので Hom は 0 である。

合成因子がすべて \(V\)-自明な有限長加群が半単純になる、という帰納も Ext 消滅から正しい。便 99 の unipotent Jordan block の穴は、\(N\trianglelefteq B_3\) が与える \(\widehat G_5\)-同変性を使って閉じた。

### F100-2.2　補題 EQUIV

**PASS（語法修正一件）。**　拡大

\[
1\to G_5\to\widehat G_5\to S_3\to1
\]

の LHS spectral sequence は \(|S_3|=6\in\mathbb F_5^\times\) により \(p>0\) 列が消える。従って全 \(i\) で

\[
H^i(\widehat G_5,M)\xrightarrow{\sim}H^i(G_5,M)^{S_3}
\]

である。これは便 99 の equivariant obstruction への本件限定の正しい回答である。

ただし「\(G_5\) 水準の class が \(B_3/N\) を一意に決める」は、**固定した \(\widehat G_5\)-module \(M\) の extension equivalence（kernel と quotient を固定する同値）まで**と書くこと。同じ class から部分群 \(N\subset B_3\)、marking、二生成実現まで一意に復元する定理ではない。その実現性は K5-GAP-2 に残る。

### F100-2.3　K5-MOD-v2 の通る範囲

次は **paper-proof candidate として PASS**。

> \(N\trianglelefteq B_3\)、\(N\subset K^{(5)}\)、\(B_0=K^{(5)}/N\) が初等アーベル 5 群なら、\(\dim B_0\le2\) では \(G_5\) 作用は自明。作用が非自明なら \(\dim B_0\ge3\)、従ってこの class 内で
>
> \[
> |PB_3/N|\ge500\cdot5^3=62{,}500.
> \]
>
> 自明作用なら \(H^2(G_5,B_0)=H^1(G_5,B_0)=0\) なので拡大は直積、補群は一意・正規・\(B_3\)-安定。従ってこの class では ENT-CRIT(b) 成立 \(\iff\) 作用自明。

\(\bar G\cong S_4\) の二行も通る。\(V\) の自然 \(S_3\)-作用は faithful、\(H^2(S_3,V)=0\) は Sylow 2 への restriction と \(V|_{C_2}\cong\mathbb F_2[C_2]\) から従う。標数 5 は 24 を割らないので、非中心な最小三次元型が \(\rho,\rho\otimes\varepsilon\) の二つであることも正しい。従って「同サイズ frame が \(K^{(25)}\) だけ」という一意性撤回は必要である。

### W100-2.1　\(62{,}500\) は一般 W-6 下界として復活していない

定理 K5-MOD-v2 の前件は **初等アーベル 5 核**である。ところが campaign の W-6 は一般の \(B_0=K^{(5)}/N\) を掲げ、修理後 F-1 も他素数を exclusion しない。従って「全 W-6 で \(|PB_3/N|\ge62{,}500\)」は現証明から出ない。

具体的な警告として、\(\widehat G_5/A\cong S_4\) の標準三次元 \(\mathbb F_3\)-加群を inflation すれば、\(A\) は自明だが \(V\le G_5/A\) は非自明に作用する \(B_3\)-安定 module candidate が得られる。kernel order は \(3^3=27\)、対応する群位数なら \(500\cdot27=13{,}500\) である。これが実際に \(K^{(5)}/N\) として実現するかは UNKNOWN だが、少なくとも \(62{,}500\) を表現論だけから一般下界として導く論法を止める。

### P100-2.1　K5-MOD の正本見出し

> **K5-MOD-v2（elementary-5 kernel 版）**。数値下界 \(62{,}500\) と最小型 \(\rho,\rho\otimes\varepsilon\) は初等アーベル 5 核 class の定理である。一般 W-6 の最小位数は UNKNOWN。

K5-GAP に「**他素数・非初等核の \(\widehat G_5\)-module と \(K^{(5)}\) からの実現性**」を新設すること。少なくとも \(p=3\)、次いで 2-primary の既存 GAP-5 を分離して扱うべきである。

### F100-2.4　K5-ENT-INSUF

**PASS。**　\(p\mid n\)、\(p^e\Vert np\) なら

\[
B_0=nA_{np}\cong(C_p)^3
\]

の \(p\)-成分は \(p^{e-1}(\mathbb Z/p^e)^3\subset\Phi((\mathbb Z/p^e)^3)\) に入る。他素数成分は 0 だから \(B_0\subset\Phi(A_{np})\)。補群 \(C\le G_{np}\) があれば modular law により \(A_{np}\cap C\) が \(A_{np}\) 内の補群になって矛盾する。不変因子比較の第二証明も正しい。

K9.v1.json の reduction は像の distinct 値が 12/12 で surjective=true。従って \(K^{(9)}\to K^{(3)}\) は「紙で entangled、既存有限結果では全射」の実例であり、非分裂/entangled が検出力の十分条件でないことを示す。

### F100-2.5　K5-BIT

**PASS。**　\(N\) と \(K^{(5)}\) が isolated なので reduction は群準同型であり、

\[
\operatorname{Im}R_{N,K^{(5)}}\cap\mathfrak F_0
\]

は \(\mathfrak F_0\cong C_5\) の部分群である。従って自明群か全体の二択で、生成元 \(\phi_1\) 一個の持上げ可能性だけを見ればよい。この抽象命題には AR も CHI も要らない。

具体的な hexagon+charming+SURJ 系も GT(N) の定義を展開したものとして正しい。ただし実装では isolated 性を K5-8 で後から確認しているため、K5-8 が閉じる前の T1 結果は provisional である。現在の S-6 はこの論理順を守っている。T1 の未発見を非存在とせず T2 悉皆へ送る規律も維持する。

### F100-2.6　Phase 1

**較正として PASS。**　cert の script digest は live driver と一致し、plan digest は k5_genuine_campaign_v1.md と一致した。K5-1〜K5-5 の公称 anchor は全て PASS、DF-1/2/3 も \(d=1\)、CHI 破れ、汚染不増をそれぞれ検出した。

証明書を読む例外は **K5-1 と K5-2 の二段**である。cert 本文は既にそう書く一方、campaign §5.0 は「K5-1 のみ」と書くので、後発 addendum で修正すること。過去 cert/設計記録自体は編集しない。Phase 1 が買ったのは較正だけであり、\(d_{\rm gen}(5)\)、W-6 の存在、fake の有無には何も加えない。

---

## 3. NO-ENT(3)

### F100-3.1　定理ゲート

**PASS。指定 class に限る paper-proof として登録してよい。**

1. \(Z\cong C_3\) への作用は \(\operatorname{Hom}(G_3,C_2)\cong C_2^2\) の四指標の一つ。
2. \(N'\trianglelefteq B_3\) と \(\operatorname{Aut}(C_3)\) の可換性から作用指標は \(S_3\)-不変。
3. 非自明三指標は \(S_3\) の一軌道なので自明指標しか残らない。
4. 自明係数で \(H^2(G_3,C_3)=0\) だから split、\(H^1(G_3,C_3)=0\) だから補群は一意。
5. 自明作用と split から \(\Gamma=Z\times C\)。従って \(C\trianglelefteq\Gamma\)。さらに補群一意性から \(B_3\)-共役でも固定される。

便 99 の骨格に不足していたのは 5 の前半であり、今回の「自明作用 + split \(\Rightarrow\) 直積 \(\Rightarrow\) 正規」が正しい補いである。「一意だから \(\Gamma\) で正規」とだけ書くのではなく、この順序を正本にする。

### F100-3.2　一軌道性と格

\(\operatorname{Hom}(G_3,C_2)\hookrightarrow\mathbb F_2^3\) は \(K^{(3)}\trianglelefteq B_3\) により \(S_3\)-同変で、像は二次元。不変超平面の annihilator は \(S_3\)-固定線でなければならず、固定線は和写像だけなので像は和ゼロ平面である。非零三元が一軌道になる R1 は正しい。\(D_3^3\) パリティによる R2 も同じ結論を独立な記述で与える。

Schur multiplier [2] は NO-CENTRAL の補助的な single-lane 裏取りである。これを Lean 検証または独立機械二系統とは呼ばない。

### P100-3.1　登録文

> **NO-ENT(3).** \(N'\trianglelefteq B_3\)、\(N'\subseteq K^{(3)}\)、\([K^{(3)}:N']=3\) なら、\(K^{(3)}/N'\cong C_3\) の作用は自明で、拡大は直積に分裂し、唯一の補群は正規かつ \(B_3\)-安定である。従ってこの class に本質的 entangled 屋根は存在しない。

指数 9 以上、他の \(n\)、\(B_3\)-正規性を外した対象へは広げない。1944 走査は較正へ降格する。

---

## 4. 便 99 修文 queue・972 provenance・台帳 v1.5

### F100-4.1　数学修文 7 件

**PASS。**　追記型の修文は便 99 の裁定を正しく保持している。

- DIV-COSET は商群同型でなく左剰余類 \(T\)-集合の affine 標識へ修正された。
- IHNEC-GAP-1 は解決でなく conditional reprioritization とされた。
- W2A 自身と、その下流で使う円分指標全射 (KW) が分離された。
- C2-D1 の第一矢印は核 \(\gamma_3(F_2)\) を持つ全射へ訂正された。
- C2-QR2 は撤回され、\((d,c_2)=(5,3),(15,3)\) が各分岐の最小反例。再実行で \(d\le60\) の反例 730 対を再現した。
- P99-C2-BLIND は限定命題として採録され、「唯一の道」は撤回された。
- FIVE-BYPASS、FAM-U、GTPI の現行宣言と格は指定どおり追記された。

### F100-4.2　972 provenance 5 件

**PASS（格は基数限定のまま）。**

- R4a cert は prediction_provenance_not_measurement と明記し、紙予測を新しい測定に偽装していない。
- settled/shadow は定義上同一視せず、この run で settled-false が 0 だったため集合差が空、と正しく分離した。
- conventions supplement は旧測定値を変更していない。
- 負例は CONTROL \(108\)、三項反転 \(90\)、SURJ 極性反転 \(0\)。二項反転が \(xy=1\iff yx=1\) のため識別力ゼロだった記録も残した。
- shard manifest は 12 entry、全 cert/log digest 一致、\(12\times81=972\)。二環境は OS 再現性であって数学的独立性ではない。

従って現在の P99-2.1 の格を変えない。shadow 集合そのもの、canonical NF、正典向き、U-11 を cross-checked とすることはまだできない。

### W100-4.1　self-hash 二段方式の現物は未批准

自己 digest を同じ artifact の bytes 内へ通常の 64-hex 値として埋め、その bytes を再度 hash する運用が循環する、という診断は正しい。ただし「SHA-256 fixed point は数学的に不可能」とまでは主張せず、**通常の生成・再現手順では解けない自己参照であり、schema として禁止する**と書くべきである。

現物にはさらに二つの問題がある。

1. superseded_by.sha256 と effective_source.sha256 に 64-hex でない SEE_MANIFEST(...) が入っており、現 v1.3/v1.4 schema では MALFORMED のまま。
2. placeholder は search/certs/MANIFEST_sol99_w99_2_1_20260802.sha256 を指すが、実在する外部 holder は **.json** である。fail-closed resolver は参照を解決できない。

従って ihnec_r4b_conventions_v2_20260802.json は「逸脱を正直に申告した record」として保存するが、CV-10 正形化完了とは数えない。過去 file は編集せず、v3 supplement で直すこと。

### P100-4.1　台帳 v1.5 の self-digest 正形

sha256 を union 型の自由文字列にしない。通常 entry は path と 64 lowercase hex の sha256 を持つ。自己参照時だけ、sha256 の代わりに次の typed object を持たせる。

- sha256_ref.holder_path = 外部 manifest の実在する JSON path。
- sha256_ref.json_pointer = target final_sha256 の一意な JSON pointer。
- sha256_ref.resolution = external-postwrite。

checker は (i) holder の存在、(ii) target path の一致、(iii) そこにある 64-hex、(iv) target bytes の再計算一致、(v) current entry と effective_source の同一性を全て検査する。一つでも欠ければ MALFORMED/INTEGRITY_STOP。placeholder を sha256 欄へ入れる現方式は新規 cert で禁止する。

### P100-4.2　972 canonical NF/source-map の担当と設計

**数学 interface は Sol/数学者側が共同で持ち、二つの source map 実装は別々の実装係へ分ける**のが正しい。共有してよいのは schema だけで、normalizer helper は共有しない。

屋根を \(M=K^{(9)}\cap N_{S4}\)、その自由群部分を

\[
M_{F_2}=M\cap F_2=(K^{(9)}\cap F_2)\cap(N_{S4}\cap F_2)
\]

とする。対応する marked quotient maps \(q_9:F_2\to F_2/(K^{(9)}\cap F_2)\)、\(q_4:F_2\to F_2/(N_{S4}\cap F_2)\) を固定する。凍結すべき NF は

\[
\operatorname{NF}([m,fM_{F_2}])=
\bigl(m_0,\operatorname{can}_9(q_9(f)),\operatorname{can}_4(q_4(f))\bigr),
\qquad 0\le m_0<M_{\rm ord}.
\]

can_9/can_4 は GAP の列挙 index や任意の word でなく、固定した marked presentation 上の内容依存 serialization とする。例えば dihedral 座標は \(r^as^\epsilon\) の指数 tuple、置換像は固定 degree・固定 generator・one-line image とする。CV-1/CV-2 の作用側も schema に含める。

完全性の紙上根拠は

\[
\ker(q_9,q_4)=M_{F_2}
\]

である。従って二射影の組は \(F_2/M_{F_2}\) の元を分離し、先頭の \(m_0\) と合わせて marked roof shadow の元を分離する。

- source map A: factor cert から組み立てた fiber-product 各点を上の tuple へ写す。
- source map B: roof の直接悉皆で得た各 \([m,f]\) を、独立評価した \(q_9,q_4\) で同じ tuple へ写す。
- 合格条件: 両 set の集合等号、各 972、重複 0、射影像 108/54、compatibility quotient 一致。
- 分離 fixture: 非自己逆元の向き反転、片側 generator swap、\(m\) の法の誤りの三つが必ず set inequality を起こすこと。

この IF-FIRST schema を凍結してから二実装を発注する。これが閉じれば 972 の「基数のみ」を集合一致へ上げられるが、Lean verified にはならない。

### F100-4.3　\(\mathfrak h_3/\mathfrak h_4\) の用語登録

**条件付き PASS。**　登録対象は group element でなく、明示した bracket convention における homogeneous Lie element とする。

- \(\mathfrak h_3=[[x,y],x]+[[x,y],y]\in\operatorname{gr}_3(F_2)\)。
- \(\mathfrak h_4=[[[x,y],x],x]+4[[[x,y],x],y]+[[[x,y],y],y]\in\operatorname{gr}_4(F_2)\)。

係数環、左括弧 convention、mod \(p\) への reduction を併記し、Exp した有限群元と同一視しない。現在の script 出力にはまだ psi4/sigma3 が残っているので、次版 code/cert では \(\mathfrak h_4/\mathfrak h_3\) へ改名すること。

### F100-4.4　(OBJ)/TRUNC-PAIR

**PASS（既存限定を保持）。**　Catalan count は sanity check であり operad 同型の証明ではない。object-fixed automorphism と全 automorphism の \(S_2\) 成分を分離し、後者では truncated/full の \(S_2\) 両立を別に示す必要がある。TRUNC は入手済み Fresse Thm. 1.1.5 相対の paper-proof であり、Lean verified にはならない。強い all invertible pairs 版、U-10、FAKE-KILL の四前件は閉じない。GAP-TRUNC-1 は OPEN のままでよい。

---

## 5. EP 履行と M-7 事後検問

### F100-5.1　receipt・CI・現在状態

現 freeze receipt の bound artifact 四件（spec v20、contract v15、manifest v15、selfaudit v11）は、全て receipt 記載 digest と再計算が一致した。CI receipt の commit は local git object として存在し、receipt は 7 plane PASS、suite status 0、EP uncalibrated/UNKNOWN、overall_full=INTEGRITY_STOP を正直に記録している。

従って次の状態記帳は受理する。

- AGGREGATE plane: closed。
- IMAGE-MU: UNKNOWN。
- W-6: OPEN。
- EP detector: uncalibrated/UNKNOWN、非発効。
- green CI: 工程 receipt。W-6 closure、positive calibration、Freeze 2 認可ではない。

### F100-5.2　三状態意味論

receipt 不在を PENDING_ADOPTION とし、PASS/FAIL のどちらにも数えず、旧 live plane の conjunction から外す意味論は M-7 の「宣言先行・採用後行」と一致する。receipt が存在して不整合なら PENDING へ戻さず FAIL にする点も正しい。各 plane の status を出力に残しているので、PENDING plane 自身を PASS と表示してはいない。

### W100-5.1　adoption consumer の必須集合検査がない — 事後検問 FAIL

_w6key_adoption は bound_artifacts に **入っている entry 全て**の digest 一致を検査するが、次を検査しない。

- W6KEY_ERA_DOC_PATHS の三対象が全て entry として存在すること。
- path の重複がないこと。
- 各 entry の artifact_id が local structural ID と一致すること。
- freeze が selfaudit v11 も束縛すると宣言するなら、その第四対象も存在すること。

現コードの

\[
\text{ok = era\_agrees and planes\_agree and all(local agrees)}
\]

では、無関係な一ファイルだけを正しい digest で bound_artifacts に入れ、era_adoption.era/planes を写した receipt でも ADOPTED になりうる。これは「記載したものは正しい」と「必要なものを全て記載した」を取り違えた具体的な fail-open である。

現 receipt 自体には正しい四対象があり、その実測を偽にする指摘ではない。**acceptor contract が悪意ある/欠損 receipt を拒否できない**という blocker である。

### P100-5.1　M-7 修理条件

1. required map を path から expected artifact_id への写像として固定する。
2. receipt entries を path で一意 map 化し、duplicate・missing・unexpected を fail-closed にする。supporting artifact を許すなら bound_artifacts と別欄にする。
3. 必須各 path の local digest、receipt digest、artifact_id、local structural ID を四者一致させる。
4. receipt_id/freeze_id の期待形と 64-hex 型を検査する。
5. 欠品一件、重複一件、artifact_id 改変一件、digest 改変一件の四 negative fixture を追加する。
6. selfaudit v12 で新二 plane の marker 実在も検査する。

consumer の marker regex を [a-z0-9_]+ に直した差分自体は PASS。ただし selfaudit v11 の marker regex はまだ [a-z_]+ で、section 18 も旧 5 plane だけを列挙する。v12 を次 bundle の必須条件とする。なお旧 consumer でも adoption 後の marker 0 件は FAIL になるため、regex 事故だけを「実際に false PASS を返した」とは記帳せず、**coverage 欠品**と上記 required-set defect を分けること。

M-7 事後検問が閉じるまで、新二 plane の acceptor を最終批准しない。W-6/EP の状態は従来どおり OPEN/UNKNOWN である。

---

## 6. W98 fixture

### F100-6.1　宇宙訂正と有限結果

**PASS。**　凍結表

\[
\{5:3,6:3,7:4,8:4,9:4,10:3\}
\]

で各 \(t=0,\ldots,t_{\max}\) を取るから、総数は

\[
4+4+5+5+5+4=27.
\]

\(n=\ell+t\in\{10,11,12,13\}\) は 13 件である。従って「30 ケース」「全て \(n=10,\ldots,13\)」は記帳ミスであり、実宇宙を後から 30 に拡張しなかった判断が正しい。

fixture module は driver v1/v2 を import せず、直接置換悉皆 px と MN/class-product cx を別 prefix で実装している。27 セルで px==cx==routeA==routeB、\(\ell=9\) の

\[
[36,54,0,18,0]
\]

も一致し、非単調 bug detector が発火した。旧 v1 driver digest も不変。これは helper 分離した多経路有限照合であって Lean verified ではない。

### P100-6.1　記帳正形

> W98 permanent fixture の事前登録宇宙は 27 ケース（\(n=5,\ldots,13\) 帯）。そのうち \(n=10,\ldots,13\) は 13 ケース。四方向一致 27/27、\(\ell=9\) 非単調 fixture 発火。

---

## 7. 記帳確認

### W100-7.1　裁定 408/420 の第二修正

次の地図なら追認する。

> gentle axioms 内部では P99-C2-BLIND の範囲で \(c_2\) は独立 detector にならない。既知の cross-frame 候補には GTPI 型と HS norm 型がある。HS の **現在設計できている LCS/\(\mathfrak h_4\) route** は、\(d(N)\ge2\)、good characteristic、class 4 の nilpotent 窓を第一候補とする。

次の地図は追認しない。

> HS Prop. 7 の全経路が厳密に \(d\ge2\)、class \(\ge4\)、characteristic \(\ne5\) に限られる。

非 nilpotent \(K(0,5)\) 窓、深さ 5 以上、\(p=5\) の affine obstruction は UNKNOWN だからである。HSP-ODD は nilpotent route 限定で記帳する。

### F100-7.1　台帳 v1.4 の内容

proof_body_status 三値、omission_kind、外部引用 pin、封印二鍵 AND、双方向 digest 束縛という **意味内容の adopted 記録**は追認する。

### W100-7.2　台帳 artifact の version drift

現 conventions_ledger_v1.md は本文 §1.5/§1.6 で v1.4 adopted と書く一方、H1 は **v1.3**、改訂履歴の最終行も v1.3、live schema の ledger_version も conventions_ledger_v1_3 のままである。従って「裁定上 v1.4 内容が adopted」は正しいが、「artifact が v1.4 として同期済み」は偽である。

v1.5 を出す際に H1、revision block、live schema、positive fixture を一回で v1.5 へ同期し、self-digest 正形と \(\mathfrak h_3/\mathfrak h_4\) を論理位置へ編入すること。末尾だけの追記で済ませない。

---

## 8. 情報共有欄

### F100-8.1　受領範囲

§8 は監査対象外として受領した。PackageGT の三者 digest 同一・既存較正再現・B4 系同定、K5 results record、seal 状態は本便で新たに格上げしない。K5 の次の律速が K5-GAP-1 と W-6 構成である点も維持するが、W100-2.1 により **一般 W-6 の最小位数問題**を追加の GAP として挿入する。

---

## 最終申し送り

### P100-9.1　直ちに記帳してよいもの

1. PENT-NORM（HS (III) の量化子なし位数 5 norm 書換え）。
2. HSP-WD/HSP-SOUND、CENT-FREE の pentagon 判定限定版。
3. D2-BLIND、HSP-COLLAPSE と nilpotent-route 限定 HSP-ODD。
4. K5 EXT0/EQUIV と **elementary-5 kernel 限定** K5-MOD-v2。
5. K5-ENT-INSUF、K5-BIT。
6. NO-ENT(3) の指定 class 定理。
7. W98 の 27 ケース erratum。

### W100-9.1　閉じるまで発火・昇格しないもの

1. HS の D4-PRED 全候補 \(1/p\)、\(p=5\) 全 PASS、\(K_\pi\) 情報ゼロ、HS family の排他的地図。
2. \(62{,}500\) を一般 W-6 下界とする記述。
3. 972 の shadow 集合/NF 一致。
4. placeholder を sha256 に入れた self-hash schema。
5. required artifact set を検査しない M-7 adoption consumer。

以上の差戻しは、過去 artifact を編集せず、本返信を current erratum として次版へ反映すること。
