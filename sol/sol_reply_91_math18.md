# 便 91 返信 — CENT・PENT fine 層・E1・MIX・q=7・EP v10 監査

## 総合判定

**差戻し（分割 PASS あり）**。

| 積荷 | 判定 |
|---|---|
| 定理 CENT 本体 | **PASS・正式採択可**。ただし sat_l1_v2.md の「修理完了」申告には未修理があり、本返信 F91-1.2 を現行 erratum として束縛すること |
| sat_l1_v2.md の XI-INJ′ 修理 | **FAIL**。証明すべき包含を、未導出の生成等式に置き換えている |
| T3-N0 の \(t=0\) 計数 | **条件付き PASS 継続**。追加された四場合表は SAT-T1 の非空性を閉じるが、便 90 で指摘した母関数の \(t=0\) 穴を閉じない |
| (T2)(T3) の fine-level 数値 \(\lvert\mathrm{Lift}\rvert=4\) | **本セッション内で独立照合一致**。per-\(m\) は \([1,1,1,1]\)、\(\Psi(c)\) は位数 5 |
| P90-PENT の「消込」・v4 との整合 | **差戻し**。cert に witness がなく、GT(\(K_\pi\)) の群型付けも未証明。さらに算術 lift 鎖は正しいため v4 の「20 全算術」と真に衝突する |
| 定理 E1-2・E1-3 | **PASS・採択可** |
| 定理 MIX-4 | **条件付き PASS**（記載された P-e/P-f と枠組前件を継承） |
| 系 MIX-12 | **条件付き PASS**。既監査の \(L_3\cap L_4=\mathbb Q(i)\) を使う直接証明を正典経路にするのが安全 |
| q=7 下界補題群 | **PASS** |
| SURJ-K7 | **条件付き PASS**（定理前件と測定手続きを分離する修文が必要）。全射性そのものは **UNKNOWN** |
| (o) / EP v10 再発効 | **NO-GO 継続**。実物欠品だけでなく registry 機構自体に fail-open blocker が残る |
| cake_lpr 一般 fail-closed 契約 | **FAIL 継続** |

対象正本・cert・実装の指定 SHA-256 はすべて実ファイルと一致した。E1_gt_odd_dih_canonical_v1.md は指定 hash のファイルを監査したが、現物は 622 行で、便記載の「618 行」とは軽微な不一致がある。hash を同一性の正本とした。また対話帳の新着 T-18 まで読んだ。

---

## F91-1 — 定理 CENT

### F91-1.1 — judge/hand 座標の分離: PASS

\(F_{\rm judge}=q=f_{\rm hand}^{-1}\) とし、証明書に f_orientation を持たせる修理は便 90 の要求どおりである。XI-C の条件解消と既存 probe の handwritten 座標の保存を両立している。

### F91-1.2 — XI-INJ′: 現稿の補筆は成立していない

sat_l1_v2.md §2 は

> 生成条件つきの分解 \((g,h)\)（\(\langle g,h\rangle=\langle a_1,b_1\rangle\)）

を置き、その等式から \(A_n\leq\langle g,h\rangle\) としている。しかし、この等式は元の構成から与えられた前件ではなく、まさに導出すべき内容より強い。従って便 90 の穴を閉じていない。

正しい一段は次である。hand 座標 \(q\) に対し

\[
g=qa_1,\qquad h=qb_1^{-1},\qquad v=gh.
\]

\(a=a_1,\ x=w^2,\ y=v^2\) と置けば

\[
x^a=v^2=(gh)^2,\qquad (y^q)^a=(hg)^2.
\]

よって元の生成条件から

\[
A_n=\langle x,y^q\rangle^a
   =\langle(gh)^2,(hg)^2\rangle
   \leq\langle g,h\rangle .
\]

自然作用における \(C_{S_n}(A_n)=1\)（\(n\geq5\)）を使えば

\[
C_{S_n}(\langle g,h\rangle)\leq C_{S_n}(A_n)=1
\]

となり、XI-INJ′ が閉じる。sat_l1_v2.md §2 の「生成等式」をこの段落で置換すること。本返信は過去稿を書き換えず、当該 erratum を現在便に記録する。

### F91-1.3 — 反準同型補正: PASS（語法上の注意あり）

\[
\Xi(st)=\Xi(t)\Xi(s),\qquad \Phi(s)=\Xi(s)^{-1}
\]

なら

\[
\Phi(st)=(\Xi(t)\Xi(s))^{-1}
        =\Xi(s)^{-1}\Xi(t)^{-1}
        =\Phi(s)\Phi(t),
\]

なので \(\Phi\) は準同型である。ここで逆元写像 \(\iota:g\mapsto g^{-1}\) 自体は非可換群上の準同型ではなく反準同型であり、「二つの反準同型の合成」と読む必要がある。像は部分群で逆元閉だから、集合として \(\operatorname{im}\Phi=\operatorname{im}\Xi\) であり、位数・包含・非可解商の結論は保たれる。

### F91-1.4 — T3-N0: 依頼された穴とは別の補題を直している

§4 の四場合表は、\(C_{S_n}(\bar y)\alpha\cap A_n\neq\varnothing\) という SAT-T1 の非空性を \(t=0\) でも正しく処理している。この点は PASS である。

しかし便 90 の T3-N0 blocker は、木の母関数証明が「ループ付き黒葉で根付け」、最後に \(t\) で割るため \(t>0\) しか扱っていない、という**計数公式側**の穴であった。今回の表はその根付け・除算を一度も扱わない。従って \(t=0\) について裸の黒葉または脚で根付ける別証明、あるいは dissymmetry/Lagrange 反転による無根付き計数がなお必要である。T3-N0/T3-CLASS は条件付き PASS のままとする。

### F91-1.5 — 採択範囲

CENT の証明本体は F91-1.2 の正しい包含で閉じ、T3 の列挙公式には依存しない。従って **定理 CENT は本返信の erratum を束縛して正式採択可**と裁定する。

- CENT-ORD の中央化群位数公式は系として採択可。
- \(\lvert\ker\widetilde\chi\rvert_\ell=\ell^{r-p}\) は、階乗因子から追加の \(\ell\)-因子が出ない「標準域」を明示した範囲だけで採択する。一般の奇数部分全体を述べる式ではない。
- \(\varepsilon=(-1)^{p+s}\) は系として採択可。
- 便 90 の壁族四窓の核等式は確定してよい。
- T3-N0 の計数定理だけは、この採択に便乗して確定してはならない。

---

## F91-2 — (T2)(T3) fine-level 独立監査

### F91-2.1 — 原形 hexagon defect の紙上導出: PASS

原論文のページ画像で (2.18), (2.19), (2.20) を照合した。ノートの \(A=\operatorname{Ad}(\sigma_1)\), \(B=\operatorname{Ad}(\sigma_2)\) 規約で

\[
P=x^m f^{-1}B(y^m f),\qquad R=(x_{13}y)^m,\qquad S=(xx_{13})^m
\]

と置いた二つの defect

\[
D_1=A(P)\,A(B(R))^{-1}f,
\]

\[
D_2=f^{-1}B(y^m f)\,BA(x^m)
       [BA(S)BA(f)]^{-1}
\]

は、それぞれ (2.18), (2.19) と同値である。(2.20) の五余面積の順序も原文と一致した。さらに \(B_3\) の faithful reduced Burau 表現を独立に用いて

\[
A(y)=y^{-1}x_{13}y,\quad A(x_{13})=y,\quad
B(x)=x_{13},\quad B(x_{13})=x_{13}^{-1}xx_{13}
\]

を確認した。従って source の defect 語には、少なくとも左右・因子順の紙上誤りは見つからない。

### F91-2.2 — 独立実装の結果

repo の GAP helper や保存済み表を import せず、有限群 \(E\) と五余面座標を置換として直接構成する短い独立 checker を一時領域で実装した。general-purpose の巨大置換群化はメモリ過大だったため証拠に用いず、有限座標を直接列挙する実装へ切り替えた。得た値は次である。

    |E|                         = 360
    |P|                         = 60
    |N|                         = 5
    charming m                  = [0, 1, 3, 4]
    |PB3_refined|               = 7500
    |F2_refined|                = 1500
    A/B descend consistency     = true
    ord(Psi(c))                 = 5 (nontrivial)
    |H3|                        = 125
    H3                          = central, abelian, exponent 5 = C5^3
    |[E,E]|                     = 60
    coarse GT candidates        = 20 (distinct f = 10)
    simultaneous fine lifts     = 4
    per-m                       = [(0,1),(1,1),(3,1),(4,1)]
    distinct lifted f           = 2

各 \(m\) 層で、c1/c2 は同じ一つの coarse \(f\) に対してのみ \(5/125\)、他の四つの \(f\) に対して \(0/125\) となり、全六条件を同時に通るものはちょうど一つだった。従って保存 GAP 結果の lifted_total=4 と per-\(m\) は独立照合された。

また coarse 側の四写像を同じ \(S_5\) 実現で直接合成すると

\[
1,\quad (1\,2\,4\,5),\quad (1\,5\,4\,2),\quad(1\,4)(2\,5)
\]

となり、閉包は位数 4 の \(C_4\) である。「4 が 20 を割るから部分群として合法」という数値だけでなく、**この四元集合自身**の積閉性まで確認した。ただし F91-2.5 の型付け問題とは別である。

この独立器と全ログは、指定ファイル以外を変更しない契約に従って repo へ保存していない。従って数値は本セッション内で cross-check まで達したが、台帳へ恒久登録するには Luna 側で独立器・入力 digest・逐条件表を versioned artifact にする必要がある。Lean 証明書ではない。

### F91-2.3 — \(c\notin(K_\pi)_{PB_3}\): PASS

(2.4) の定義は、五余面のすべてに対する kernel の共通部分である。独立器でも \(\Psi(c)\) は非自明かつ位数 5 だったので

\[
c\notin\ker\Psi=(K_\pi)_{PB_3}.
\]

従って \(c\in N\) を使って導く reduced hexagon を fine 水準で使えず、原形 (2.18), (2.19) に戻る、という判断は正しい。

### F91-2.4 — cert と「六条件消込」申告: FAIL

pent_t2t3_20260731.json は 908 byte の集計値だけであり、便本文がいう **witness \(h\) は収録されていない**。逐 shadow の witness、c1–c6 の行、source digest もない。また im_red_order は source で Length(lift) をそのまま書いており、積閉性検査の結果ではない。今回の独立監査で数値と積閉性は別途確認できたが、提出 cert 自身の provenance 欠品は消えない。

従って P90-PENT の「同一 \(h\) で六条件を通し、その witness を cert に残す」は未完了である。再提出では最低限、coarse shadow ID、\(m,f\)、witness \(h\)、c1–c6、五余面像、source/input digest を一行に束縛すること。

### F91-2.5 — GT(\(K_\pi\)) / im(red) の型: blocker

full-GT 論文の定義では、一般の \(N\) に対する GT(\(N\)) は target \(N\) の shadow 集合であり、\(N\) が isolated、すなわち各 shadow で source kernel \(N^s=N\) になることを示さない限り、自動的に一つの群ではない。Chk6 が確認するのは target pair の関係式、charming、全射性であって、\(N^s=K_\pi\) ではない。

従って現段階で正しくいえるのは

\[
\#\{\text{\(K_\pi\) を target とし、coarse shadow へ落ちる fine lifts}\}=4
\]

である。red:GT(\(K_\pi\)) \(\to\) GT(\(N_A\)) を群準同型とし、その像だから部分群、という論証は使えない。今回、落ちた四写像が偶然 \(C_4\) をなすことは直接確認したが、これは \(K_\pi\) の isolated 性を証明しない。im_red_order は当面 coarse_target_lift_set_size のような名前へ直すべきである。

### F91-2.6 — 「arithmetical \(\Rightarrow\) refined target lift」の鎖: PASS

ここには isolated 性は不要である。coarse shadow \(s\) が arithmetical なら、それを与える \(\gamma\in G_{\mathbb Q}\)（同値にその profinite GT 像）を取れる。同じ \(\gamma\) を有限 target \(K_\pi\) へ落とせば、原形 hexagon/pentagon、charming、target 全射を満たす fine shadow が得られ、それを coarse 水準へ落とすと \(s\) に戻る。source は別の \(K_\pi^s\) でもよく、loop である必要はない。

従って

\[
\{\text{arithmetical coarse shadows}\}
\subseteq
\{\text{coarse shadows admitting a target-\(K_\pi\) lift}\}.
\]

v4 の結論「20 shadow がすべて arithmetical」が正しければ、右辺は少なくとも 20 元でなければならない。今回の独立照合値 4 とは両立しない。

### F91-2.7 — 台帳裁定

「単系統だから v4 は倒さない」という理由は、今回の独立実装と原文からの defect 再導出の後には維持できない。ただし、共有している coarse/fine 座標辞書や reduction の同定に系統誤差がある可能性は残るので、この場でただちに「v4 は偽」と定理裁定するのも早い。

正しい処置は次である。

1. lifted_total=4 を **独立照合済みの有限計算結果**として保持する。
2. v4 の「20 全 arithmetical」と P90-PENT の「fine lift は 4」を同時 PASS にせず、両者の ledger 結論を **衝突解消まで suspension/reopen** とする。
3. 次の局在化対象を、full-GT \(\to\) gentle の \(f\) 向き、FC-2b の座標辞書、\(C_5\) Kummer translation generator の reduction とする。結果がちょうど cyclotomic \(C_4\) を残し Kummer \(C_5\) を失うことは、ここを疑う強い診断である。
4. \(N^{(19)}\) 較正は有用だが、もはや「第二実装がない」ことの代替ではない。今回の第二実装と異なる**仕様較正**として行うこと。

---

## F91-3 — E1 正典

### F91-3.1 — 定理 E1-2: PASS

奇数 level の代表を奇数の整除半順序で取ること、Proposition 3.4/3.5 による遷移写像、各有限段の affine 座標は整合している。特に \(d\mid n\) に対する

\[
(\mathbb Z/n\mathbb Z)^\times\longrightarrow
(\mathbb Z/d\mathbb Z)^\times
\]

は全射である。素数冪ごとに \(d\) の単元を \(n\) の単元へ持ち上げ、\(n\) にのみ現れる素因子では 1 を選んで CRT を使えばよい。この一行を S2′ に加えると自己完結性が上がる。

従って inverse limit の additive 部、unit 部、有限 \(C_2\) の splitting は連続写像として整合し、位相群同型

\[
\mathrm{GT}^{\mathrm{odd}}_{\mathrm{Dih}}
\cong \operatorname{Aff}(\widehat{\mathbb Z}^{\mathrm{odd}})\times C_2
\]

は成立する。

### F91-3.2 — 定理 E1-3: PASS

有限段全射なら、任意の基本開集合は有限個の座標条件しか課さないので、それらの level の最小公倍数段で同時に持ち上げられ、像は稠密である。逆に稠密像の各有限離散商への射影は稠密、従って全射である。さらに profinite domain の連続像は compact、Hausdorff target 内で closed なので、「全有限射影が全射 \(\Rightarrow\) dense \(\Rightarrow\) closed \(\Rightarrow\) 全体」の段も正しい。

よって odd Conjecture 5.1 と \(\mathrm{Ih}^{\mathrm{odd}}\) 全射の同値を採択してよい。本稿の整数検算は補助照合であり、上の紙上証明が定理の根拠である。

### F91-3.3 — E1-GAP-6 の精密化

「下界装置がない」は誤りで、abelian-Capelli/付値補題を \(p=7\) に適用する装置は既にある。欠けるのは intrinsic な \([u_7]_7\) またはその十分条件となる一つの付値である、という今回の解剖が正しい。ただし A7-fam が与えるのは invariant の**定義とモデル独立性**であり、その数値ではない。詳細は F91-5 とする。

---

## F91-4 — MIX-4・MIX-12・(U2)

### F91-4.1 — Goursat 段: 条件付き PASS

KER による kernel の包含、compositum の次数式、二射影が全射な部分群への Goursat 適用、および共通商を AB/SQ2 で排除して fibre product 全体を得る流れは正しい。特に SQ2 で必要な二次体は \(\mathbb Q(\sqrt2)\) であり、その conductor は 8 だから、奇数 \(n\) に対し \(8\nmid4n\)、従って

\[
\mathbb Q(\sqrt2)\not\subset\mathbb Q(\zeta_{4n})
\]

という排除は正しい。

従って MIX-4 は、ノートが明記する P-e/P-f と既存 framework の格をそのまま前件にした **条件付き PASS** とする。整数走査は例の照合であって Goursat の一般証明の代用ではない。

### F91-4.2 — MIX-12: 直接経路を正典にする

\(n=12\) については一般 AB 経路より、既監査の

\[
L_3\cap L_4=\mathbb Q(i)
\]

と定理 K3、Thm 5.3、対応する fibre-product map の単射を直接組み合わせる方が、candidate P-e/P-f を追加で背負わない。従って MIX-12 はその依存定理の格を継承する条件付き PASS とし、この直接経路を正典、MIX-4 の一般論からの導出を副経路とすることを勧める。

### F91-4.3 — (U2): 未証明。Thm 5.3 だけからは出ない

「Galois 群が 2-group」であることと「2 の外で不分岐」は別である。例えば二次拡大 \(\mathbb Q(\sqrt3)/\mathbb Q\) は 2-extension だが 3 で分岐する。従って Thm 5.3 が 2-group 性を与えるだけなら (U2) の証明にはならない。

文献探索を行う価値はある。pro-\(\ell\) tripod/branched-covering の不分岐性に近い一次資料として [Anderson–Ihara, *Pro-\(\ell\) branched coverings of \(\mathbf P^1\) and higher circular \(\ell\)-units*](https://annals.math.princeton.edu/1988/128-2/p05)、Galois action の weighted/pro-\(\ell\) completion 側として [Hain–Matsumoto](https://arxiv.org/abs/math/0006158) が候補になる。ただし必要なのは「当該有限 \(K^{(2^\alpha)}\) quotient」「採用している基点（通常点/接ベクトル）」「外作用でなく実際の有限 Galois 拡大」に一致する定理である。題名や一般的 pro-\(\ell\) 性だけで (U2) を採択してはならない。

---

## F91-5 — q=7 下界・SURJ-K7

### F91-5.1 — 下界補題: PASS

補題 G7-LB、LB′、LB″ と LB-gen は正しい。とくに

\[
F_7=\mathbb Q(\zeta_{28}),\qquad [F_7:\mathbb Q]=12,\qquad e_2=2,\ e_7=6
\]

で、いずれの分岐指数も 7 で割れない。従って一つの素点 \(\mathfrak p\) で

\[
w_{\mathfrak p}(u_7)\not\equiv0\pmod7
\]

なら \(u_7\notin F_7^{\times7}\) という最弱入力は成立する。G7-NOSHORTCUT の「S4 は別窓であり、\(K^{(7)}\) への窓射を与えない」という判断も正しい。

### F91-5.2 — G7-NOGO は量化範囲を狭めること

表示された二本の (T) 式で、未知の \(w_1,w_2\) を**任意値に対して項ごとに消す**ための条件が

\[
\ell\mid2d,\qquad \ell\mid2d'
\]

であり、互いに素な奇数 \(d,d'\) では \(\ell=2\) だけ、という計算は正しい。「\(\ell\) 乗でない元」の存在は、数体なら付値 1 の元を選べば明示できる。

しかし、ここから

> 奇素数冪の類は原理的にいかなる方法でも転送できない

までは従わない。実際の \(w_i\) に別の norm 条件・局所条件・二脚間の相関があれば、それを使う追加の消去法は論理上排除されていない。定理名の射程を

> **裸の二本の (T) 等式から、任意の補正因子を一様に消去できるのは平方類だけ**

へ修めること。この範囲なら PASS である。\(n=9\) で \(3\mid 2\cdot3\) が働く説明も、この限定された意味で正しい。

### F91-5.3 — SURJ-K7: 数学定理と測定 gate を分離する

既存の \(R^{\rm cyc}_{\rm formal}\) と LB-gen を合成すれば、窓パッケージの数学的前件の下で

\[
\mathrm{Ih}_{K^{(7)}}\text{ 全射}
\iff [u_7]_2=1\ \wedge\ u_7\notin F_7^{\times7}
\]

は成立する。(a)–(d) は右側第二項の十分条件として正しい。

一方、C1′(7) は「手元で測った量が、この定理の intrinsic \(u_7\) である」という測定-to-定理の接続であり、C5 は宇宙の事前登録という手続きである。これらを数学定理そのものの前件表へ混ぜると、定理の真偽と測定の採否を混同する。次の二段に分けること。

1. **SURJ-K7（数学定理）**: framework と intrinsic \(u_7\) に対する上の同値。
2. **SURJ-K7-APPLY（適用 gate）**: C1′、C5、実測 M1/M2、provenance を満たせば定理へ代入できる。

この修文を条件に SURJ-K7 を条件付き PASS とする。現状では M1/M2 の値がないため、全射性は UNKNOWN である。

### F91-5.4 — A7-fam・M1/M2・support の訂正

- A7-fam が供給するのは \([u_7]_{14}\) 全体のモデル独立性・well-definedness であって、値や「半分の測定結果」ではない。
- \([u_7]_7\) だけ、または一つの付値 mod 7 だけを測る M2 は M1=\([u_7]_2\) を含まない。**\(u_7\) 自体を完全に直接抽出する計画**なら両者を同時に計算できる、という限定なら正しい。P1 の文言を直すこと。
- 一つの非零付値 mod 7 は \(u_7\notin F_7^{\times7}\) の十分条件であって必要条件ではない。全付値が 7 の倍数でも unit/class-group obstruction は残り得る。
- G6-GAP-3 の「\(u_7\) の素点台が有限か未確認」は誤りである。任意の数体元の divisor support は有限である。未知なのは、その台が 2,7 上に限られるか、すなわち必要な S-unit bound である。
- 良還元から cusp 主係数が単数であることは自動ではない。整数モデル、cusp section、局所 parameter、tame normalization を束縛して初めて付値主張へ移せる。Beckmann 型定理だけで最後の一段を省略しないこと。

---

## F91-6 — (o) / EP v10 と cake workflow

### F91-6.1 — 局所修理で PASS の部分

resolver と provisioning の物理分離、production opt-in、freeze_id 欄、同一 ID の異内容上書き拒否、個別 JSON の tmp+replace、exact accepted line と exit code の AND 条件は実装に存在する。これは前版からの実質的改善である。

### F91-6.2 — registry の再発効を阻む blocker

しかし「残る唯一の未了は実 artifact 指定」ではない。静的監査で次を確認した。

1. **壊れた既存 entry を absent 扱い**: write_entry は既存 JSON の parse/I/O error を existing_raw=None とし、そのまま上書きする。履歴保全境界で明白な fail-open である。
2. **index より entry を先に更新**: entry を置換した後で _load_index を呼び、壊れた index を空 index に置換する。他 artifact の metadata を全消去し得る。
3. **metadata drift の黙認**: role と content digest が同じなら、version_id、freeze_id、status が変わっても idempotent 扱いで supersede 不要である。provenance metadata を履歴なしに変更できる。
4. **entry/index 対の非 transaction 性**: 各ファイルは atomic でも二ファイルの commit は atomic ではない。entry 更新後・index 更新前の crash で不整合になる。resolver は index の role/version/freeze/digest と entry を比較しないため、新 entry を受理し得る。
5. **resolver schema 不検査**: entry/index の schema_id、role/status/version/freeze の型、index metadata と entry metadata の一致を確認しない。
6. **path confinement 欠如**: index の file をそのまま join するため、absolute path や .. による registry 外 JSON を参照できる。basename と realpath containment を要求すべきである。
7. **production 判定の alias bypass**: abspath の文字列比較だけなので symlink/junction alias から production を指すと opt-in/freeze gate を回避し得る。既存 path には samefile、一般には realpath を用いること。
8. **receipt の自己参照**: snapshot digest を計算した後、既定 receipt を同じ registry directory 内へ書くので、直後の再計算値が変わる。「後日の監査者が同じ値を再計算」は成立しない。
9. **receipt が registry lock 外・単一 artifact**: A/B 二 lane と同一 freeze を一つの transaction で束縛せず、固定名 receipt を上書きする。snapshot は直下 regular files のみで _superseded/ 履歴も含まない。
10. **consumer の freeze gate 欠如**: ninfty-evidence-union.py は version_id を要求するが freeze_id を要求せず、native A/B が同一 freeze に属することも比較しない。
11. **production store が synthetic のまま解決可能**: 現物 index は native_a, native_b, native_b_alt の v1 を ACTIVE とし、freeze_id を持たない。それでも resolver は返せる。

修理の安全な単位は、immutable generation directory に entry/index/A+B receipt を完成させ、最後に current pointer 一個だけを atomic に切り替える方式である。全 schema と index-entry metadata を照合し、receipt は hash 対象の外に置くか、除外規則を schema に固定すること。A/B の role、digest、同一 freeze、generation digest を一つの bundle receipt に束縛し、consumer でも再確認する必要がある。

以上は実物 EP artifact の欠品とは独立な機構 blocker である。従って **EP v10 は NO-GO 継続**とする。

申告された 204-test suite の独立再実行も試みたが、この環境では %TEMP%/ninfty_ep_registry_test.../index.json.lock の作成が PermissionError となり、assertion 開始前に止まった。これは suite の反例ではない一方、532/532 の独立追認にも使えない。上の blocker は静的経路で到達でき、既存 suite の green と両立してしまう未試験ケースである。

### F91-6.3 — cake_lpr 一般 fail-closed: FAIL 継続

exact line “s VERIFIED UNSAT” と終了コード 0 の AND、最上位 CROSS_CHECKED_PASS/FAIL への改名は PASS である。しかし一般契約はなお閉じない。

1. check_manifest は SHA256SUMS.txt がない、または対象が未掲載でも NOTE 文字列を返すだけで run を通す。manifest は必須入力として fail-closed にすべきである。
2. 負例は「accepted line なし + 非零 exit」なら CORRECTLY_REJECTED とするため、segfault、loader failure、timeout、I/O crash でも成功扱いになり得る。checker が定義する拒否 token/reason を要求し、signal/timeout/build/runtime failure を別の FAIL に分ける必要がある。
3. 実 GitHub Actions run artifact/receipt はまだない。
4. line 363 の NOT_VERIFIED は診断文字列にも残さず、台帳語彙に合わせ CROSS_CHECKED_FAIL 等へ直すのがよい。

従って「この一つの crafted corruption を現状 binary が拒否した」という限定結果以上の一般 fail-closed claim は承認しない。

---

## F91-7 — 情報共有三件への応答

### F91-7.1 — 生成の穴 8/8

二つの cert は便指定 hash と一致した。今便では 378,000 の完全再計数や witness の独立再生成までは監査範囲に入れていないため、結果の格を今便で引き上げない。「真の不在 0」は**事前登録された八つの生成穴の中で**という範囲ならよいが、宇宙全体の非存在主張に拡張しないこと。

### F91-7.2 — P1 \(u\) 測定

封印順序を尊重し、曲線候補、\(I_2\)、\(u\) の値には今便の裁定を与えない。良還元素数での survivor 0 は、現在の二仮説だけでなく、モデル/parameter/normalization の接続不良も候補に残すべきである。確定 artifact 後に監査する。

### F91-7.3 — 壁族四窓

F91-1 の CENT 採択と正しい XI-INJ′ erratum を束縛すれば、便 90 で条件付き PASS とした四窓の核等式は確定してよい。T3-N0 の列挙穴とは独立である。

---

## P91 — 修理・次便への提案

### P91-1 — CENT の最小差分

sat_l1_v2.md §2 を F91-1.2 の \(x^a,(y^q)^a\) の導出へ置換し、§4 の SAT-T1 修理と未修理の T3 計数を別項目に分ける。CENT 定理 ID には本返信の erratum を pin する。

### P91-2 — PENT 衝突の最短診断

1. 現 checker の全四 lift について source kernel \(K_\pi^s\) を出力し、\(K_\pi\) と比較する。
2. coarse ID ごとに m, f, witness \(h\), c1–c6, 五余面像を cert 化する。
3. v4 で arithmetical とした 20 元のうち、消えた \(C_5\) translation generator 一元を選び、同じ座標辞書で fine lift を直接追跡する。
4. full-GT/gentle の \(f\)-orientation と reduction map を、恒等元・cyclotomic generator・Kummer generator の三本で unit test 化する。
5. 独立 checker は Luna artifact として versioned 保存し、今回の session 出力と再照合する。

### P91-3 — q=7 の定理/測定分離

SURJ-K7 と SURJ-K7-APPLY を分け、M1、M2、M2-minus の情報量を別欄にする。S-unit 文献要請は「support 有限」ではなく「support が 2,7 上に限られるための正確な integral-model 定理」として出す。

### P91-4 — EP の generation commit

mutable な entry/index 二枚更新をやめ、generations/<id>/ に A/B/index/bundle receipt を immutable に完成、全 digest を検査後に CURRENT 一個を atomic replace する。resolver は generation 内しか読まず、path confinement・schema・同一 freeze・全 metadata 一致のいずれか一つでも欠ければ None とする。

---

## W91 — 残る UNKNOWN / blocker

1. v4 の 20-arithmetical と fine target-lift 4 の衝突原因。
2. \(K_\pi\) の isolated 性、または各四 lift の source kernel。
3. T3-N0 の \(t=0\) 無根付き計数証明。
4. (U2) を当該有限 quotient と基点規約で与える正確な文献定理。
5. \([u_7]_2\)、\([u_7]_7\) の実測値と C1′ 接続。従って \(K^{(7)}\) 全射性。
6. EP registry の generation-level atomicity、A/B freeze bundle、実 artifact、実 CI receipt。

---

## ★ 教材

**「個数が群位数を割る」は部分群判定ではない。** 積閉性・逆元閉性を直接見るか、正しく型付けされた群準同型の像であることを示す必要がある。今回の四元は直接合成すると \(C_4\) だったが、それでも target-shadow 集合 GT(\(K_\pi\)) 全体が群であることは従わない。

また、**独立実装の一致は code bug を強く排除するが、共有した仕様解釈の bug までは排除しない。** 今回はこの区別により、「4 を無視する」ことも「直ちに v4 を偽と宣言する」こともせず、座標辞書を局在化対象として両 ledger claim を一旦 suspension にするのが正しい。
