# 便 98 返信 — GTPI / D / FAKE–IH / 壁 / 計数 / EP

**総合判定: 条件付き PASS。**  最優先の **(A′) c3 pentagon は PASS**、**補題 INT は PASS**、定理 D/D+ の紙上部分も PASS とする。一方、`ihnec_v1.md` の **系 SPLIT-NULL″（「fake を検出しうるのは entangled 屋根だけ」）は現前件からは従わず FAIL**。定理 SPLIT-NULL 本体の「像は $m$-fiber の合併」は、下記の一行を明記すれば PASS である。GTPI 二部作は定理候補として条件付き PASS だが、`CLOSURE` の存在段と $PB_4$-settled は依然として有限計算に論理依存するので、「紙が probe 全体を spot-check に降格した」とは分類しない。

## 0. 監査範囲と provenance

### F98-0.1 — 指定物の同一性: PASS

便 98 に列挙された 18 個の SHA-256 は、手元の 18 artifact と **18/18 byte 一致**した。さらに原論文をテキスト抽出だけでなく PDF ページ画像で照合した。

- 2008.00066: PDF p.13 の (2.18)–(2.20)、pp.48–49 の (A.16)/(A.18)。
- 2401.06870: PDF pp.20–21 の Prop. 3.12、(3.59)/(3.60)、Prop. 3.14/3.15、p.28 の Cor. 5.4。
- 対話帳 T-22/T-23/T-24、LEDGER 裁定 344–383（と発送記録 384）も読んだ。

本返信の「PASS」は紙上監査または artifact の検収を意味する。Lean 証明ではなく、工房規約上の **verified（検証済み）ではない**。

## 1. GTPI 二部作

### F98-1.1 — (A′) `c3 = Pent` の正典忠実性: PASS

$R=\mathrm{Rev}$ を語反転反準同型とする。コードの 5 成分を正確に型付けすると、単に $v_i=\phi_i(f)$ ではなく

\[
\begin{aligned}
v_1&=R(\phi_{123}(f)),&v_2&=R(\phi_{234}(f)),\\
v_3&=R(\phi_{12,3,4}(f)),&v_4&=R(\phi_{1,23,4}(f)),\\
v_5&=R(\phi_{1,2,34}(f)).
\end{aligned}
\]

ここで code の `cof[3..5]` に現れる積順序が (A.18) の逆順なのは、`PsiAt(w,i)=MappedWord(Rev(w),cof[i])` が $R\circ\phi_i$ を実装するためである。原文 (2.20)

\[
\phi_{234}(f)\phi_{1,23,4}(f)\phi_{123}(f)
=\phi_{1,2,34}(f)\phi_{12,3,4}(f)
\]

に $R$ を施すと積順序が反転し、

\[
v_1v_4v_2=v_3v_5,
\]

すなわち code の `Pent` と逐語一致する。これは 400/400 の鏡像不変性とは独立な、原文式からの導出である。従って **c3 の canonical-fidelity は閉鎖**してよい。

`Aut1`/`Aut2` はそれぞれ (A.6) の共役作用を自由語へ移したものであり、`D1`/`D2` も (2.18)/(2.19) を同じ $R$ 規約で移した形と整合した。今回名指しされた最後の穴は c3 であり、そこに新しい逆転はない。

### F98-1.2 — (G) $T^{PB_4}$ の共役向き: PASS

正典は

\[
\phi(f)^{-1}a\phi(f).
\]

$R$ は反準同型なので

\[
R\!\left(\phi(f)^{-1}a\phi(f)\right)
=R(\phi(f))\,R(a)\,R(\phi(f))^{-1}.
\]

従って Rev 側の正しい向きは code の **`v*(.)*v^-1`** であり、`v^-1*(.)*v` は正典と Rev を混ぜた向きである。20/20 対 4/20 はこの導出の補助的な識別実験であって、採択根拠そのものではない。

### F98-1.3 — (H) WD-4: NOTE（定理 blocker ではないが検出器は未閉鎖）

現 WD-4 は識別力を持たない。`cofcMix` を同じ `cofMix` から作り、

\[
y^{-1}(y\,x_{13}\,x)x^{-1}=x_{13}
\]

を検査しているだけなので、混成した表の内部でも恒真になる。$B_4$ 表現検査 20/20 対 4/20 は $T$ の共役向きを識別するが、**5 coface の source-map packing 自体を直接検査する WD の代用品ではない**。

### P98-1.1 — 【GAP-WD-1】の修理仕様

次の二経路を分けるべきである。

1. **正典経路**: (A.2) から $A_{ij}$ を独立に構成し、(A.18) の 15 個の生成元像を literal table として実装する。期待値を `cof`/`cofc` から生成しない。
2. **probe 経路**: 現 `PsiAt` をそのまま使う。
3. 非回文語、例えば $w_*=xy^2x^{-1}c[x,y]$ を含む固定 discriminator 集合で、全 5 成分について
   \[
   \Psi_i(w)=\pi\bigl(R(\phi_i(w))\bigr)
   \]
   を比較する。
4. fwd 生成元 × rev 行順、または $X_{13}/X_{24}$ の一方だけを反転した mutation が **必ず FAIL** することを同じ suite で要求する。

これなら「同じ表から恒等式の両辺を作る」循環を断ち、直接の混成検出器になる。

### F98-1.4 — (I) $c$-項の射程: 限定つき PASS

この窓では $\Psi(c)$ は位数 5 で、成分 3,4,5 の $c$-項は実際に非自明である。従って「全 $c$-項が空虚」は誤り。一方、成分 1,2、すなわち $\phi_{123},\phi_{234}$ 経路では $c$ の像が恒等元であり、その二経路の非自明 $c$-挙動は未較正である。

これは **この $N_0$ に対する正しさの欠陥ではない**（正典像も局所的に恒等元になる）が、coface evaluator を他窓へ再利用できるという一般的主張には使えない。一般 evaluator の較正には、少なくとも $\pi\phi_{123}(c)$ または $\pi\phi_{234}(c)$ が非自明な新窓が必要である。

### F98-1.5 — GTPI / $GTPI^{PB_4}$ の総合格: 条件付き PASS

- $\mathrm{GT}(K_\pi)\cong\mathrm{GT}(N_A)\cong F_{20}$ の有限定理候補は、UNIV/DICT/SHAPE の紙と有限悉皆の組合せとして整合する。
- ただし `gtpi_v1.md` の CLOSURE 段 3 は **`red(\mathcal G)=\mathcal S` の exhaustive scan**を使っている。UNIV は各 coarse fiber の精 lift の「高々一意」を与えるが、20 coarse 元すべてに lift が存在することまでは紙だけで与えない。従って probe は全体として spot-check ではなく、存在・全射性に不可欠な有限証明書である。
- $N_0\in\mathrm{NFI}_{PB_4}(B_4)$、$N_{PB_3}(N_0)=K_\pi$、20/20 settled、$N^\sharp=N_0$ の鎖は数理的に整合し、**LEVEL CAVEAT は定理候補の意味論として解除してよい**。ただし settled 部分は現状 GAP 単系統なので、格は「紙 + 単系統有限計算」であり cross-checked ではない。
- H は QA の未閉鎖、I は移植射程の NOTE であり、この固定窓の定理を倒さない。

## 2. 定理 D と二裁定

### F98-2.1 — 定理 D / D+: PASS

中核は正しい。T-1 を仮定すると GAUSS により $A=Q^2\ell$、$Q,\ell\in\mathbb Z[x]$。BARY から

\[
4A_4=5(P_1+Q_1),\qquad 5\mid A_4.
\]

$B\le4$ では $A_4=0$ となり、$d=-2b$、$c\equiv4b^2\pmod5$ を用いた三場合分けはいずれも箱と矛盾する。depressed は使っておらず、定理 D はその意味でゲージ非依存である。

depressed を加えた D+ では $A_4=P_1=-5b$、$d=-7b$ が従い、$B\le24$ の場合分けも正しい。最後の $b=\pm1,c=-1$ を Pell 合同で排除する段も有効である。

系 D′ の 372/372 は、$(a,p)\mapsto(a,-p)$ が T-1 を保存して E-3 だけを反転し、priority が `[4]` を `[8]` より先に表示するための会計像である。この等分を独立な数学的陰性証拠として数えないという降格も正しい。

ただし「最小 $B=25$ でちょうど 2 点」「非 depressed $B=5$ でちょうど 6 点」の**完全個数**は有限列挙に依存する。紙が与えるのは下界・パラメータ化と提示点の確認であり、個数の格は machine result のまま。

### F98-2.2 — D-1（旧 stage2 hit 8 件）: `[7] REJECT`

8 件は $\operatorname{rootpart}(a)=[3,1,1]$ で、spec v19 の T-1 を満たさない。従って現 decision lane では全件 `[7] triple-root-of-a` により REJECT。これは「候補 8 件」ではなく、旧 searcher stage2 と spec decision lane が別対象を選んだことの回帰 fixture である。救済・候補数への算入・positive control 化を認めない。

### F98-2.3 — D-2（depressed の意味論）: 技術的選択、現 Rule 1 内では規範的

depressed は対象の幾何学から強制される条件ではなく、$x$-平行移動自由度を使い切る **座標 gauge の選択**である。ただし Rule 1 がその gauge を canonical producer の一部として採択している間は、現 campaign 内で任意に外せる filter ではない。

また「gauge-free $B=5$」という呼び方は厳密には避けるべきである。係数箱 $\|a\|,\|p\|\le B$ 自体が平行移動・再尺度で変わるため、depressed を外した箱も座標依存である。正確には **non-depressed integral-coordinate lane** である。

### P98-2.1 — $B=5$ 六点の扱い

六点は事前登録外・audit lane 未走なので、現時点では **新 campaign の seed/fixture** に限る。受理するなら、旧 spec を黙って広げず、次のいずれかを versioned に事前登録すること。

- depressed canonical representative と rational/integral height の変換を含む新しい高さ規約、または
- non-depressed integral-coordinate lane を別宇宙として固定し、平行移動 orbit の重複規則を明記する。

いずれの場合も六点を positive control や candidate と先に呼んではならず、E-5 と audit lane を初めから通す。

## 3. FAKE-VOID / IH-NEC / INT

### F98-3.1 — FV-EQ / FV-COST / FV-SUB: PASS（用語修文つき）

FV-EQ の閉部分群論法は正しい。副有限群の閉部分群は全有限商像から復元され、$G_{\mathbb Q}$ の像はコンパクト性により閉である。INT が下記のとおり閉じるので、isolated cofinal 系を用いる鎖にも新しい穴はない。FV-SUB は arithmetical $\Rightarrow$ genuine $\Rightarrow$ 全細分 survive という容易な向きだけを使い、個々の VOID を独立証拠から降格する会計も正しい。

FV-SOLV はあくまで operational conjecture、FV-WALL は予想にせず観測帯、FV-N∞ は D/D+ 以外 UNKNOWN、という三層の格を維持すること。Thm B.2 移送が成立する窓を「独立プローブ」に数えないという留保も必要である。

### F98-3.2 — 正式用語: 旧三種の `*-fake` は公開語として不採用

T-23/裁定 374 に従い、以後の定理文・台帳では次だけを用いる。

\[
\begin{array}{ll}
\textbf{fake}&=\mathrm{GT}\setminus\mathrm{GT}_{\rm gen},\\
\textbf{非算術証人}&=\mathrm{GT}_{\rm gen}\setminus\mathrm{GT}_{\rm arith},\\
\textbf{非算術 shadow}&=\mathrm{GT}\setminus\mathrm{GT}_{\rm arith}
=\text{fake}\sqcup\text{非算術証人}.
\end{array}
\]

`pentagon-fake` / `arith-fake` の細分は数学的 filtration の内部メモとしては読めるが、正式な「fake」の二義を再導入する。必要なら「pentagon 障害層」「算術障害層」と呼び、上の三語を上書きしないこと。

### F98-3.3 — IH-FACT / IH-NEC / FAKE-KILL: PASS

- IH-FACT は各有限段の定義を逆極限へ束ねた等式で正しい。
- IH-NEC の含意と対偶は正しい。名称に反して odd Conj. 5.1 から IH-S が従うとは述べておらず、必要条件としての方向も明示されている。
- FAKE-KILL は **非算術証人**を使うとき、前件 U-10 のみで正しい。fake は P1/P2 を殺しうるが、この結論には使えないという差分も正しい。

### F98-3.4 — ★ 補題 INT: PASS

段 1 の代表元取り替えに穴はない。実は 2401 Prop. 3.12(c) の可換図 (3.59) が、まさに

\[
\pi_N\circ T^M_{m,f}=T^N_{R_{M,N}[m,f]}
\]

を既に述べている。自前確認も次で閉じる。

- $m'=m+kN_{\rm ord}$ なら指数差は $2kN_{\rm ord}$。$\operatorname{ord}(xN),\operatorname{ord}(yN)\mid N_{\rm ord}$ なので $\sigma_i^{2m'+1}N=\sigma_i^{2m+1}N$。
- $f'=fh$、$h\in N_{F_2}=N\cap F_2$ なら $hN=1$ であり、$f'^{-1}\sigma_2^{2m+1}f'N=f^{-1}\sigma_2^{2m+1}fN$。

従って $K=\ker T^M_{m,f}\subseteq N\cap H=M$。一方 $T^M_{m,f}$ は全射なので
$[B_3:K]=[B_3:M]$、ゆえに $K=M$。Prop. 3.14/5.1/5.2/Cor. 5.4 を使っておらず非循環である。

改善点は依存表だけである。「Def. 3.7/3.13/(3.1)/(3.60) のみ」と書くより、**Prop. 3.12(c)/(3.59) を直接引用**するのが最短かつ安全である。Prop. 3.15 の言明は原文にあるが証明は reader exercise、工房の INT がその欠落を埋める。

### F98-3.5 — 定理 ML-ODD: PASS（決定手続きではない）

ML-1 の交叉/lcm、ML-3 の有限集合逆系の非空性、$Y_N$ の構成はいずれも正しい。有限個の整合条件には共通 refinement を取り、その一点から写せるので finite-intersection property が成立する。(iii)$\Rightarrow$(i) の逆極限構成にも量化漏れはない。$N=K^{(n)}$ では $n\in D(N)$ なので $Y_N=\{y_n\}$ となる。

ただし「有限問題族」は **各問題が有限**という意味であり、$N$ の族自体は無限。停留深さの有効上界がないため、IHNEC-GAP-1 はそのまま UNKNOWN である。

### F98-3.6 — 定理 SPLIT-NULL 本体: 修文条件つき PASS

Goursat 段に次の一行を明記すればよい。任意の $T_{m,f}$ は $f\in PB_3$、$u=2m+1$ 奇数だから $B_3/PB_3\cong S_3$ 上で恒等写像を誘導する。従って image を記述する共通商 $E$ には自然な全射 $E\twoheadrightarrow S_3$ があり、その核 $E_0$ は二つの pure quotient の共通商である。仮定より $E_0=1$、従って $E\cong S_3$ で image は全 fiber product になる。

これで主公式「$\operatorname{Im}R_{M,K^{(n)}}$ は $m$-fiber の合併」は成立する。

### F98-3.7 — ★ 系 SPLIT-NULL″ の無条件形: FAIL

主公式から分かるのは **同じ $m$-fiber の内部（$\mathfrak F_0$ 方向）を部分的に削らない**ことだけである。もし $\mathfrak m(N')$ が compatible な $m$ を欠けば、分裂屋根はその $m$-fiber **全体**を削り、その元は fake の有限 witness になる。pure quotient に共通商がないという仮定だけでは、$\mathfrak m(N')$ の全 $m$-被覆は従わない。

従って次の文は現状では過大である。

- 「fake を検出しうる細分は entangled 屋根に限る」
- 「分裂屋根をいくら積んでも genuine image は縮まない」

また「非算術証人は分裂屋根で不可視」という言い方は、非算術証人が genuine である以上 **全ての屋根へ survive するという定義上の事実**で、split 特有の結論ではない。

### P98-3.1 — SPLIT-NULL の正しい強形

次を追加前件にする。

\[
\forall m\in\mathcal X_n\ \exists\widetilde m\pmod {M_{\rm ord}}:
\widetilde m\equiv m\pmod{2n},\quad
\widetilde m\bmod N'_{\rm ord}\in\mathfrak m(N').
\tag{MCOV}
\]

(MCOV) の下では全 $m$-fiber が現れ、reduction は全射、従ってその split roof は fake を検出しない。framework-conditional な S2 は (MCOV) を与える一経路であり、$n=9,N_{S4}$ では 6 個の $m$-像の直接測定が (MCOV) を与える。従って R4a の 108/108・54/54 にはこの欠陥は波及しない。一般の `SPLIT-NULL″` だけを (MCOV) なしで撤回・差替すること。

### F98-3.8 — R4a / U-11: 有限主張は整合、証拠格は単系統

$|\mathrm{GT}(M)|=972$、二 reduction の 108/108・54/54 全射は、上の修理済み split-roof 論法と直接の $m$-coverage に整合する。$\Theta_9$ が 108 元を全単射で座標化し、11,664 対すべてで $\mathrm{Aff}(\mathbb Z/9)\times C_2$ の積に一致するなら、有限群の明示同型という結論は正しい。ただし元の列挙は GAP 単系統で、R4b も未了であるため、U-11 の記帳は「有限 exhaustive candidate / single lane」とし、cross-checked や verified へ上げない。

## 4. 壁、SURV、カナリア、CV-13

### F98-4.1 — 壁族分類: PASS

非可解壁は $n=24,28,36,37$ の 4 窓。$n=40,45$ は同じ $C_\ell\times S_t$ 型でも有限群が可解であり、可解帯へ置く。旧「6 壁」は撤回済みの語法として扱う。

### F98-4.2 — m=0 の 2280 悉皆等号: PASS（GAP 単系統）

列挙の完全性は紙上でも説明できる。$A_{24}$ の自己同型は $S_{24}$ の共役で与えられるので、$x\mapsto x^u$ の全共役元は一つの解 $\alpha_0$ と $\operatorname{Stab}(x)$ の積で尽くされる。固定した target に対する
$f^{-1}y^uf=\text{target}$ の解は $C_{A_{24}}(y^u)f_0$ という左 coset で尽くされる。従って `stab_size*cyu_size` の予算 assert と全 scan は候補生成を尽くす。

m=0 で新候補集合と既知 SURV 集合が literal Set equality、双方 2280 であるため、向きつき完全性アンカーは強い。ただし証拠格は GAP 単系統である。

### F98-4.3 — settled 2280/2280: PASS、ただし cert の説明を補う

`SettledReport` 単体は `GroupHomomorphismByImages` が `fail` でないことしか見ておらず、kernel を直接測っていない。しかし直前の candidate filter が

\[
\langle x^u,f^{-1}y^uf\rangle=P_N
\]

を要求しているので、得られた $B_q\to B_q$ の image は pure subgroup $P_N$ を含む。また $u$ は奇数、$f$ は pure なので $B_q/P_N\cong S_3$ 上では恒等、従って image は $B_q$ 全体。有限群の全射自己準同型は自己同型で、kernel は自明となる。よって settled 結論は正しい。

この依存を cert/report に明記し、将来 `SettledReport` を別 pipeline から単独利用して「hom exists = settled」と誤読させないこと。

### F98-4.4 — m=18 カナリア: 存在 PASS、構造欄は sample NOTE

m=18 の候補 2280 と settled 2280/2280 は全件測定であり、複素共役層の非空性は PASS。算術的意味づけを保留した格も正しい。

一方 `per_candidate_sample_cap=20`、`per_candidate_sample_truncated=true` である。従って shadow order 2/4/6、conjugator、$S_5$ 内部作用の各主張は **20/2280 sample** に限る。「2280 全件で確認」と書いてはならない。

$C_{19}$ 作用の反転は、distinguished generator が $x\mapsto x^{u}$、$u=37\equiv-1\pmod{19}$ であることから紙上では全候補に従いうる。ただし cert の `c19_action_r=18` 欄自身が測ったのは 20 件のみである。「紙の一般帰結」と「machine sample」を分けて記帳すること。

### F98-4.5 — CV-13: 条件付き承認

`YImg` を一箇所に置き、生成直後に受理式を assert する規約は、局所的な向き混用を確実に止めるので採択してよい。ただし generator と receiver が同じ誤った `YImg` を共有すれば一様鏡像は通る。従って CV-13 は **internal orientation consistency gate** であって canonical-fidelity gate ではない。m=0 の既知集合等号のような外部 anchor、または独立 source-map route を必ず併置すること。

## 5. W98-ALG — 全指標表を作らない厳密計数

### F98-5.1 — 現状の計数結果の格

収穫は 1/13 セルのみであり、

\[
T_{\rm trans}(37,1^2)=3{,}296{,}573{,}904,\qquad
T_{\rm all}(37,1^2)=10{,}643{,}405{,}866
\]

が較正点。残る 12 セルは UNKNOWN。GHA job success や `gap_exit_code=0` を完走と読まず、`DRIVER_DONE` と cert を必要条件にした fail-closed 修理は正しい。

### W98-5.1 — 採択案: long-hook localized Frobenius/Jacobi–Trudi 法

固定した $w_\rho\in S_n$ に対し

\[
T_{\rm all}(\rho)=\#\{(g,h):g^2=h^3=1,\ gh=w_\rho\}.
\]

$\lambda\vdash n$、既約指標 $\chi^\lambda$、次数 $f^\lambda$ とし

\[
A_2(\lambda)=\sum_{g^2=1}\chi^\lambda(g),\qquad
A_3(\lambda)=\sum_{h^3=1}\chi^\lambda(h).
\]

中心関数の畳込みから

\[
\boxed{
T_{\rm all}(\rho)=\frac1{n!}\sum_{\lambda\vdash n}
\frac{A_2(\lambda)A_3(\lambda)\chi^\lambda(\rho)}{f^\lambda}}
\tag{ALG-1}
\]

である。ここで全 character table は不要。Frobenius characteristic により

\[
\frac{A_2(\lambda)}{n!}=s_\lambda\big|_{p_1=p_2=1,p_{r\ne1,2}=0},\quad
\frac{A_3(\lambda)}{n!}=s_\lambda\big|_{p_1=p_3=1,p_{r\ne1,3}=0}.
\]

完全対称函数の必要列は

\[
h_k^{(2)}=[z^k]e^{z+z^2/2},\qquad
h_k^{(3)}=[z^k]e^{z+z^3/3},
\]

すなわち $kh_k^{(2)}=h_{k-1}^{(2)}+h_{k-2}^{(2)}$、
$kh_k^{(3)}=h_{k-1}^{(3)}+h_{k-3}^{(3)}$。Jacobi–Trudi

\[
s_\lambda=\det(h_{\lambda_i-i+j})
\]

を exact rational / fraction-free determinant で評価すれば $A_2,A_3$ が得られる。次数 $f^\lambda$ は hook-length formula でよい。

本件の $\rho=(\ell,1^a)$、$a\le8$ では MN 則がさらに局所化する。

\[
\boxed{
\chi^\lambda(\ell,1^a)=
\sum_{\substack{\mu\vdash a\\\lambda/\mu\text{ が長さ }\ell\text{ の rim hook}}}
(-1)^{\mathrm{ht}(\lambda/\mu)}f^\mu}
\tag{ALG-2}
\]

従って $p(n)$ 個の各 $\lambda$ について必要なのは、最大 22 個の $\mu\vdash a$ に対する border-strip 判定だけである。非零の $\lambda$ だけで Jacobi–Trudi を行う。安全な初版は partitions を一個ずつ stream し、メモリ $O(n^2)$ とする。高速版では $\mu\vdash a$ へ長さ $\ell$ の rim hook を加えて非零 $\lambda$ だけを直接生成する。

推移性は一般 Bell 分割を使う必要がない。$w=(\ell,1^t)$ の $\ell$-cycle を含まない orbit では $w=1$、$gh=1$、$g^2=h^3=1$ なので $g=h=1$ となり、各点は singleton orbit である。従って

\[
T_{\rm all}(\ell,1^t)=\sum_{a=0}^t{t\choose a}T_{\rm trans}(\ell,1^a),
\]

二項反転で

\[
\boxed{T_{\rm trans}(\ell,1^t)=
\sum_{a=0}^t(-1)^{t-a}{t\choose a}T_{\rm all}(\ell,1^a).}
\tag{ALG-3}
\]

これは既存 `t3_a_chars.g` の数学を一般 driver へ戻すもので、Bell 数列挙も消す。13 セルは $\ell=37,41$ ごとに $a=0,\ldots,8$ の値を一度ずつ計算して再利用できる。

### P98-5.1 — 実装・検収ゲート

上の案を第一選択として **GO** とする。条件は次のとおり。

1. `CharacterTable("Symmetric",n)` と ctbllib の全表構築を dependency closure から禁止する。
2. 初版 route A は全 partition streaming、route B は rim-hook 直接生成とし、同じ partition generator/helper を共有しない。
3. 各 $T_{\rm all}$ の整数性・非負性、(ALG-1) の分母消去、(ALG-3) の非負性を fail-closed assert にする。
4. 小 $n$ の直接悉皆、$(23,1^3)$ の $T_{\rm trans}=173{,}880$、$(25,1^5)$ の 378,000、そして今回の $(37,1^2)$ の **両方の値**を較正にする。単に $>0$ だけでは normalization bug を捕まえない。
5. cert には formula ID、各 $a$ の $T_{\rm all}$、寄与した partition 数、contribution stream digest、script digest、完走 marker を残す。

Burnside/character-free 路線については、(ALG-3) が推移性部分の完全な組合せ的解答である。$T_{\rm all}$ 自体を $h=gw$、$g^2=(gw)^3=1$ の map/constellation DP に落とす第二路線は独立 checker として有望だが、現時点で state bound と完全性証明が無い。これを待って主線を止める必要はない。まず (ALG-1)–(ALG-3) を着地させ、12 セル再走はその検収後に行う。

## 6. EP の二検問

### F98-6.1 — era composition 修理: PASS

現 source では `_compose_full(..., era_ok)` が最初に `era_ok is not True` を判定し、route の PASS/FAIL/ABSENT/CONFLICT/INTEGRITY_STOP に関係なく `INTEGRITY_STOP` を返す。数学的 route composition は `integrity_gate.route_composition_status` に別保存され、report schema も v2 へ上がっている。suite は 5 base status × era の両辺と、newer/missing/stale era mutation を public entry point で通している。

receipt `run30693842443` の SHA-256 は指定値と一致し、記載 commit `c2c64e58…` はローカルに存在する。現在の三つの該当 source はその commit から差分がなく、receipt だけが後続収蔵で加わっている。従って **便 97 の masking defect は履行済み**と裁定する。

ただし receipt が直接束縛するのは `suites_status=0` と各 gate 欄であり、「899 checks」という手集計値は receipt 本文に含まれない。899 を引用する場合は suite log の別 provenance を添えること。EP 自体は receipt が明記する通り `uncalibrated/UNKNOWN`。

### F98-6.2 — W6-KEY draft の設計: 条件付き PASS

最小多項式の primitive normalization、固定複素埋込みに相対的な exact root rank、float fallback 禁止、二 receiver の判別式 route / Sturm route 分離は妥当である。token 一致を image equality と混同せず、`IMAGE-MU` を UNKNOWN に残している点も正しい。

### P98-6.1 — W6-P1 lane A per-point producer 改造: **認可 GO**

現 genuine fixture では有限 ramification points を紙上で点ごとに分けられる。

\[
x\in\{-2,-4\},\qquad 125y^2+16=0,\qquad
p(x)=\frac45,\qquad \mu=p(x)y,qquad3125\mu^2+256=0.
\]

各 $x$ について $y$ の root rank $k=0,1$ を持つ二点があり、正の有理数 $4/5$ を掛けるので branch value の rank も同じ $k$ になる。従って lane A は少なくとも次の 4 record を独立に出す。

\[
(-2,y_0)\mapsto b_0,\quad(-2,y_1)\mapsto b_1,\quad
(-4,y_0)\mapsto b_0,\quad(-4,y_1)\mapsto b_1,
\]

各 multiplicity は 1、受領側集計は $b_0,b_1$ に各 2 となる。`ramification_point_id` は branch token で代用せず、**$x$ の値と $y$-root rank の両方**を含めること。`exact_image_witness` は $125y^2+16=0$、$\mu=(4/5)y$、$3125\mu^2+256=0$ の exact reduction を持たせる。lane B の token/NF を producer 入力にしてはならない。

この 4 点だけで COVERAGE 全体を宣言してはならず、既存の二無限遠 ramification point とその像・係数も同じ point-map に残す。receiver が全 support の一回被覆を再計算して初めて COVERAGE PASS とする。

### P98-6.2 — SPEC-V20 / contract-manifest v15: 改版着手を認可

**spec v20・verifier contract v15・dependency manifest v15 の versioned trio を起こすことを認可する。** これは draft/implementation authorization であり、freeze・W-6 closure・EP 発効の認可ではない。必須条件:

- `mb/ninfty-w6-branch-key/v1` と `...point-map/v1`、R1′/R2′ を新しい exact era plane として matrix に登録する。
- frozen R1/R2 core の byte を変更せず、新 payload を v18 と偽装しない。
- KEY/COVERAGE/IMAGE/AGGREGATE/INDEPENDENCE を別欄にし、`IMAGE-MU=UNKNOWN` の間は overall W-6 を PASS にしない。
- schema/provenance 不正は MALFORMED/INTEGRITY_STOP、exact 判定不能は UNKNOWN、well-formed な divisor 不一致だけを FAIL とする。
- R3-NF は忘却像の列のままで、W-6 の代替にしない。
- trio digest と payload-era receipt を新たに束縛し、v19/v14/v14 の旧 plane を黙って書換えない。

### F98-6.3 — positive control: `NotAuthorised` / UNKNOWN 維持

harness の先行実装や green suite は calibration ではない。full-path positive control 本走の認可は本便からは出さない。W-6 producer 改造・v20/v15 改版と positive-control event を同一の「EP 再発効」に束ねないこと。

## 7. 情報共有・台帳

### F98-7.1 — CV-11 の `digest` キー: v1.3 と整合、PASS

P97-1.2(2) の `digest` 禁止は、本文どおり **CV-10 の `effective_source_chain/effective_source` 範囲**に限定される。CV-11 `seal_recoverability[].digest` は明示的に範囲外であり、現 v1.3 は自己矛盾していない。既存 CV-11 を遡及的に `sha256` へ改名しない。

将来用語を統一するなら v1.4 の versioned schema change と fixture 更新で行うべきで、v1.3 の黙示的読み替えは禁止する。

### F98-7.2 — 最終仕分け

- **PASS**: GTPI A′/G、定理 D/D+ の紙上核、FV-EQ/FV-SUB、IH-FACT/IH-NEC/FAKE-KILL、補題 INT、ML-ODD、壁分類、2280 列挙と settled の現在の論理、era 修理。
- **条件付き PASS / NOTE**: GTPI 二部作の計算依存と単系統格、GAP-WD-1、$c$-path の移植射程、SPLIT-NULL 本体の $S_3$ 一行、カナリア構造 sample、CV-13、W6-KEY draft。
- **FAIL（修理対象は一件）**: (MCOV) なしの SPLIT-NULL″ / 「entangled 屋根だけが fake を検出する」という無条件結論。
- **認可**: W98-ALG の実装設計、lane A per-point producer 改造、spec v20 / contract-manifest v15 の versioned draft/implementation。
- **未認可・UNKNOWN 維持**: 残 12 計数セルの旧 backend 再走、W-6 closure、EP 発効、positive-control 本走、$B=5$ 六点の candidate/positive-control 化。
