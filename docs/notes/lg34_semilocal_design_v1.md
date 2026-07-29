# 【LG-3】【LG-4】半局所 Kummer — 帰属訂正・NORM-U/MARK-U の判定・橋 $B_{\rm FC}^{\rm sl}$ の設計図

**状態札: candidate(裁定前・未 commit・単系統・Sol 監査前)**
起草: Claude(数学者レイヤー・Opus 5)/ 2026-07-30
設問: 司令塔文献配達(`docs/notes/litgate_semilocal_kummer_v1.md`)の §3 新規性警報 +【LG-3】【LG-4】

**本稿は `docs/notes/surj_d4_t1_v1.md` の正誤表を兼ねる**(versioned 規律により v1 は上書きしない — §0 が erratum of record)。

**依拠**
- 配達覚書 `docs/notes/litgate_semilocal_kummer_v1.md`(司令塔翻訳)
- 原著(**読んだ範囲を申告**): `papers/delivered/arxiv_2506.11310.pdf`(O'Dorney, *Étale algebras and the Kummer theory of finite Galois modules*)— **Abstract・§1 Introduction・§2.1(Prop 2.1・Example 2.2)・§3(Prop 3.1/3.2)の 4 頁のみ精読**。§4–6 未読。他 5 本(1301.4429 / 0809.0017 / 1507.07208 / 2408.13108 / 1504.02814)は**未読**(覚書の要旨のみ使用・出所は覚書に帰属)。Jacobson–Vélez 1990 は**未入手・未読**(書誌のみ)。
- 自前: `docs/notes/surj_d4_t1_v1.md`(補題 SURJ-Split・W-OBS・TAIL-OBS)/ `docs/notes/surj_s4_v1.md`(補題 Φ-univ・補題 F0)/ BFC v2.15 §5–§8 / 梯子証明書 4 通(`search/certs/a13_ladder_W_E_A1{0,1,2,3}_*_20260730.json`)

> ## 封印遵守
> 封印量非接触。$K^{(5)}$ 非接触。$u$ の値には触れない(本稿は**定義の well-defined 性**と**設計図**のみ)。凍結済み予言(i10_1 の 11 欄・41b8698)には非接触。

---

## 0. 新規性突合(義務事項)— 層 II の帰属訂正

### 0.1 突合の結果: **警報は正しい。層 II の辞書は古典である。**

O'Dorney 2506.11310 の **Abstract** 逐語(精読済):

> "for finite Galois modules $M$, an element of $H^1(K,M)$ can be described by a finite amount of data over $K$. For the important case $i=1$, the appropriate object is an étale algebra over $K$ … whose Galois group is a subgroup of the semidirect product **$\mathrm{Hol}\,M=M\rtimes\mathrm{Aut}\,M$ (often called the holomorph of $M$)**, equipped with a little bit of combinatorial data.
> Although the correspondence between $H^1$ and field extensions **is in widespread use**, it includes some combinatorial and Galois-theoretic details that seem never to have been written down."

さらに **Prop 2.1**(精読済)は逐語で

> "$K$-Galois module structures on $M$ are in natural bijection with pairs consisting of (a) a finite Galois extension $L/K$, and (b) an embedding $\mathrm{Gal}(L/K)\hookrightarrow\mathrm{Aut}\,M$."

**⟹ 著者自身が「widespread use(周知)」と明言している。** 私が `surj_d4_t1_v1.md` §2.3 で「②の正確な形」として書いた内容 —
$$\text{$\mathrm{Ih}$ 全射}\iff c:G_{K_0}\to\mathbf Z/9\ \text{が}\ \chi\text{-同変な満位数指標}\iff \mathrm{ord}([u]_9)=9,\quad\text{固定体}=K_0(u^{1/9})$$
— は、**$M=\mu_9$ に特殊化したこの古典辞書そのもの**である。$\mathrm{Hol}(\mathbf Z/9)$ への全射性が radical 拡大 $x^9-u$ の Galois 群の満性に対応する部分は **Jacobson–Vélez 1990**(*The Galois group of $x^n-a$*・holomorph の部分群としての明示)の射程でもある(**未読・覚書の書誌に依拠**)。

### 0.2 正誤表(erratum of record)

| 対象 | v1 の書き方 | **訂正後の帰属** |
|---|---|---|
| `surj_d4_t1_v1.md` §2.3「②の正確な形」 | 自前の導出として提示(新規とは書いていないが、**引用もしていない**) | **古典**。O'Dorney 2506.11310 Abstract/§2.1(+ Jacobson–Vélez 1990)を引用すること。$H^1(K,M)\leftrightarrow\mathrm{Hol}(M)$ 部分群つきエタール代数の辞書 |
| 同 §2.4「像の可能性は 3 つ」 | 自前 | **古典**(O'Dorney Prop 2.1 の直接の系: $\mathrm{Gal}(L/K)\hookrightarrow\mathrm{Aut}\,M$ の像の分類)。$\mathbf Z/9$ の部分群が $1,C_3,C_9$ の 3 つという初等事実 |
| 同 §3 補題 3.1($u\in\mathbf Q^\times$ 非 3 乗 ⟹ 満位数) | 自前 | **初等かつ古典的**(アーベル拡大の部分体は正規、の標準論法)。t63 §5(c) の再利用としてのみ自前 |
| 同 §6.1 の層の表「層 II」 | 「**✅ 形は届く**」を成果として提示 | **「古典辞書がそのまま使える」に書き換え**。到達したのは我々ではなく古典理論であり、我々がしたのは**入力を古典辞書に載る形に整えたこと**だけ |
| 同 §7.1 補題 SURJ-Split | 「新規性: 窓データを一切使わないことの明示」 | **維持(訂正不要)**。$\tilde\chi\circ\mathrm{Ih}_N=\chi_{2\nu}$ は **GT 側の言明**(Ihara 写像と GT-shadow の合成則についての主張)であり、古典 Kummer 理論とは別の層。**ただし「①が閉じる」の内容の半分(円分の全射性)は完全に古典**であることを明記する |
| `surj_s4_v1.md` §4 定理 SURJ-S4 | $R^{\rm cyc}_{\rm formal}$(W3-13)を引用済 | **訂正不要**(自前定理の引用として正しい)。ただし「1 ビット帰着」の**形**が古典辞書と同型であることを註記すると読者に親切 |

> ### ★ 正味の自前寄与(訂正後の確定リスト)
> 1. **補題 SURJ-Split (b)(d)(e)**: $\tilde\chi\circ\mathrm{Ih}_N=\chi_{2\nu}$ の**窓非依存性**と、そこからの分解。**GT 固有**。
> 2. **命題 W-OBS / 系 W-OBS-fam / 命題 TAIL-OBS**: (W4) が空であることの厳密証明。**GT 固有**。
> 3. **補題 Φ-univ / 補題 F0**(`surj_s4_v1.md`): 【GAP-06a】の紙上閉鎖と命題 K5-1 の族外一般化。**GT 固有**。
> 4. **S4 の (W3)(W4)(W5)(W5$^{\mathbb Q}$)(6′) の紙上証明**と 1 ビット帰着。**窓固有**。
> 5. **【SD-c】$a=+1$ の実測**。**窓固有**。
> 6. **本稿 §1–§2**(下記)。
>
> **「$u$ を cusp 主係数として同定する」ことだけが古典に無い部分**であり、それは橋 $B_{\rm FC}$(自前)の仕事である。**古典辞書は「$u$ が何かを知っていれば答えが出る」と言うだけで、$u$ が幾何のどこから来るかは言わない。** ここが本プロジェクトの立ち位置である。

### 0.3 ★ 逆に得たもの — エタール代数の言葉は【LG-3】の正しい言語である

O'Dorney §3(精読済)の枠組み(**エタール代数 $L/K$ $\leftrightarrow$ $G_K$-集合**、Prop 3.1;**基底変換との両立**、Prop 3.2)は、覚書 §2 の型 A(cusp 集合を有限エタール代数 $E$ と読む)と**同じ言語**である。すなわち文献配達は「層 II を古い」と告げると同時に、**【LG-3】を書くための語彙を供給している**。以下 §1 はその語彙で書く。

---

## 1.【LG-3】NORM-U と MARK-U を $W\text{-}E\text{-}A10\text{-}9t1$ で書き下す

### 1.1 設定(半局所の幾何データ)

窓: $P\cong A_{10}$、$\bar x=X$ は $\{1,\dots,9\}$ 上の 9-巡回で $10$ を固定、$M_{\rm win}:=\mathrm{ord}(X)=9$、$N_{\rm ord}=9$、$K=\mathbf Q(\zeta_{18})=\mathbf Q(\zeta_9)$。

TAIL-OBS より $[P:H]=9$ なる $H$ は存在しない。**そこで窓を自然な次数 10 の被覆に取る**:
$$H:=\mathrm{Stab}_P(10)\cong A_9,\qquad [P:H]=10 .$$
* $N_P(H)=H$: $A_9$ は $A_{10}$ の極大部分群で、$N_{A_{10}}(A_9)\supsetneq A_9$ なら指数 1 となり単純性に反する ⟹ **(W3) は成立** ✓
* $\langle X\rangle$ の $P/H$(10 点)上の軌道: $X$ の巡回型は $(9,1)$ ⟹ **軌道 2 個、長さ 9 と 1** ⟹ (W4) は不成立(既知)。

**cusp**: 補題 B-5b(幾何点 $\leftrightarrow$ 慣性軌道)より $\lambda^{-1}(0)$ の幾何点は $\langle x\rangle$-軌道と 1:1、軌道長 $=$ 分岐指数。よって
$$\lambda^{-1}(0)=\{P_0,\ P_1\},\qquad e_{P_0}=9,\quad e_{P_1}=1 .$$

> ### 補題 SL-1(t=1 の cusp は個別に $K$-有理)
> $G_K$ は $\lambda^{-1}(0)$ の幾何点を分岐指数を保って置換する。$e_{P_0}=9\ne1=e_{P_1}$ ゆえ **$G_K$ は 2 点を混ぜられない**。したがって $P_0,P_1$ はそれぞれ $G_K$-固定、すなわち $\kappa(P_0)=\kappa(P_1)=K$。
> $$\boxed{\ E:=\kappa(P_0)\times\kappa(P_1)=K\times K\quad(\text{分裂エタール代数}).\ }$$

**⟹ t=1 ではエタール代数が分裂する。** O'Dorney §3 の言葉では、$G_K$-集合 $\mathrm{Coord}(E)$ が 2 つの自明軌道に分かれる場合であり、**最も退化した場合**である。

### 1.2 局所類の型付け(ここが判定の要)

分岐指数 $e_P$ の点 $P$ で $\lambda=u_P\,s_P^{e_P}\bigl(1+O(s_P)\bigr)$。uniformizer の取り替え $s_P\mapsto a\,s_P(1+O(s_P))$($a\in\kappa(P)^\times$)で
$$u_P\ \longmapsto\ u_P\,a^{-e_P}.$$

> ### 補題 SL-2(局所類の well-defined な住処)
> $[u_P]$ が well-defined なのは **$\kappa(P)^\times/\kappa(P)^{\times e_P}$ の中でだけ**である。とくに $e_P=1$ なら $\kappa(P)^\times/\kappa(P)^{\times1}=1$ で、**$u_P$ は情報を一切持たない**(任意の値に取り替えられる)。

**t=1 での帰結**:
$$[u_{P_0}]\in K^\times/K^{\times9}\ \ (\text{9 次の情報を持つ}),\qquad [u_{P_1}]\in K^\times/K^{\times1}=1\ \ (\textbf{情報ゼロ}).$$

### 1.3 NORM-U の判定

覚書の候補定義:
$$\textbf{NORM-U}:\qquad [u]_K:=N_{E/K}\bigl([u]_E\bigr)\in K^\times/K^{\times M}.$$

**(a) 一様指数 $M=9$ で読む場合 — ill-defined。**
$[u]_E:=([u_{P_0}]_9,[u_{P_1}]_9)\in(K^\times/K^{\times9})^2$ と**書ける**が、第 2 成分は補題 SL-2 より uniformizer の取り替えで $u_{P_1}\mapsto u_{P_1}a^{-1}$、$a\in K^\times$ 任意。$K^\times\to K^\times/K^{\times9}$ は全射なので $[u_{P_1}]_9$ は**任意の値を取りうる**。$E=K\times K$ でノルムは積 $N(\alpha,\beta)=\alpha\beta$ だから
$$N_{E/K}([u]_E)=[u_{P_0}u_{P_1}]_9\ \text{は}\ K^\times/K^{\times9}\ \textbf{全体を動く}.$$
$$\boxed{\ \textbf{一様指数版 NORM-U は well-defined でない(情報ゼロ)。}\ }$$

**(b) 局所指数で正しく型付けした場合 — degenerate だが well-defined。**
正しい住処は
$$[u]_E\in\prod_{P\mid0}\kappa(P)^\times/\kappa(P)^{\times e_P}=\bigl(K^\times/K^{\times9}\bigr)\times\{1\}.$$
$e_P$ が点ごとに違うので「$E^\times/E^{\times M}$」という一様な書き方が**そもそも型として誤り**である。第 2 成分が自明群なのでノルム(積)は第 1 成分の恒等写像に退化し
$$\boxed{\ \textbf{NORM-U}^{\rm typed}=[u_{P_0}]_9\in K^\times/K^{\times9}\quad(\text{well-defined}).\ }$$

### 1.4 MARK-U の判定

覚書の候補定義: canonical 生成対(LID-1)が指す cusp の局所 $u$。

**t=1 では marking が不要である**: $e_{P_0}=9\ne e_{P_1}=1$ なので、**「分岐している方」という群論的条件だけで $P_0$ が一意に決まる**(規約の選択が入らない)。したがって
$$\boxed{\ \textbf{MARK-U}=[u_{P_0}]_9\quad(\text{well-defined・LID-1 を呼ばずに正準}).\ }$$

### 1.5 判定(委嘱の問いへの回答)

> ### 命題 LG3(t=1 での三型の一致)
> 窓 $W\text{-}E\text{-}A10\text{-}9t1$(および一般に $\bar x$ の型が $(\ell,1)$ で $\ell>1$ の窓)において
> $$\textbf{NORM-U}^{\rm typed}\ =\ \textbf{MARK-U}\ =\ [u_{P_0}]_\ell\ \in\ K^\times/K^{\times\ell},$$
> であり、型 C(束ねない = 「cusp ごとの類の族」)も同じ情報を与える(族 $=\bigl([u_{P_0}]_9,\ 1\bigr)$ で第 2 成分は自明)。**三型は一致し、いずれも well-defined。**

**帰結 1(良い知らせ)**: **t=1 では定義の選択問題が起きない。** どの型が「正しい」かを決めずに橋の修理へ進んでよい(覚書の「型 C が正なら LG-4 は空振り」という懸念は、**t=1 に関しては解消**する)。

**帰結 2(悪い知らせ・設計上重要)**: **t=1 は三型の判別窓にならない。** 覚書 §2 の「NORM-U との一致/不一致自体が測定項目になる」という期待は、t=1 では**恒真**であって測定にならない。

> ### 系 LG3′(判別窓の条件)
> 三型が分岐するには、**分岐指数が等しい cusp 点が 2 つ以上**必要である($G_K$ がそれらを混ぜられ、$\kappa(P)$ が $K$ の真の拡大になりうる)。$\bar x$ の巡回型で言えば
> $$\boxed{\ \text{判別窓の必要条件}:\ \bar x\ \text{の巡回型に長さ}\ \ell>1\ \text{の巡回が \textbf{2 本以上}}\ }$$
> 最小候補は $\bar x=(\ell,\ell,1^t)$。**これは発案 I10-1 の判別窓 $(\ell,\ell,\ell,1^t)$ と同じ族**であり、**1 本の設計で I10-1(奇部の 3 vs 81)と LG-3(NORM/MARK/型 C)の両方を判別できる**可能性がある(設計の相乗り候補・§3【LG-a】)。

---

## 2.【LG-4】橋 $B_{\rm FC}^{\rm sl}$(半局所版)の要修理箇所リスト

BFC §4 の四段に沿って、**t=1 を主対象**に「そのまま通る/要修理」を判定する。**証明は書かない(委嘱どおり設計図まで)。**

### 2.1 段 I($B_{\rm FC}$-I・定理 B-3「型は無料」)

**使っている核**: 命題 B-1(**正則**可換部分群は自己中心化)⟹ $\rho_\Lambda(\mathrm{Ih}(\gamma))\in C_{\mathrm{Sym}(\Lambda)}(\tau(\mu_M))=\tau(\mu_M)$ ⟹ 一意の $c$。

**半局所での状況**: $\Lambda\cong P/H$(補題 B-2 (B2-bij)・(W3) のみ使用 ✓ **(W4) 不要**)。$\tau(\zeta_M)$ は $X$ による左移動で、巡回型 $(9,1^t)$。$S_{9+t}$ における巡回型 $(9,1^t)$ の元の中心化群の位数は $9\cdot t!$、すなわち
$$\boxed{\ C_{\mathrm{Sym}(\Lambda)}\bigl(\tau(\mu_9)\bigr)\ \cong\ \langle X\rangle\times S_t\ \cong\ C_9\times S_t .\ }$$

> ### ★ 修理 R-I(および $t$ の役割の正体)
> * **$t=1$**: $S_1=1$ ゆえ $C(\tau(\mu_9))=\tau(\mu_9)$ — **命題 B-1 の結論がそのまま成り立つ**(正則でないのに自己中心化)。⟹ **段 I は無修理で通る。** 修理は「命題 B-1(正則性)」を「巡回型 $(\ell,1^t)$ の中心化群の直接計算」に**差し替える**だけ。
> * **$t\ge2$**: 中心化群が $S_t$ の分だけ太る ⟹ $c$ の一意性が壊れ、$\rho_\Lambda(\mathrm{Ih}(\gamma))$ は**対** $\bigl(c(\gamma),\ \sigma(\gamma)\bigr)\in\mu_9\times S_t$ を与える。$\sigma:G_K\to S_t$ が「**不分岐 cusp 点の Galois 置換**」である。

> ### ★★ 観察 SL-3(measured 値との一致・candidate)
> 梯子 4 窓の実測 $\ker\tilde\chi$ を $C_9\times S_t$ と並べる(証明書 4 通から転記):
>
> | 窓 | $t$ | 実測 $\ker\tilde\chi$ | $\lvert\ker\rvert$ | $C_9\times\mathrm{Syl}_2(S_t)$ | $\lvert C_9\times S_t\rvert=9\cdot t!$ |
> |---|---|---|---|---|---|
> | A10-9t1 | 1 | $C_9$ | 9 | $C_9\times1=C_9$ ✓ | 9 |
> | A11-9t2 | 2 | $C_{18}$ | 18 | $C_9\times C_2$ ✓ | 18 |
> | A12-9t3 | 3 | $C_{18}$ | 18 | $C_9\times C_2$ ✓ | 54 |
> | A13-9t4 | 4 | $C_9\times D_8$ | 72 | $C_9\times D_8$ ✓ | 216 |
>
> $$\boxed{\ \ker\tilde\chi\ \cong\ \langle X\rangle\times\mathrm{Syl}_2(S_t)\ =\ \bigl(\text{段 I の中心化群}\bigr)\ \text{の 2-部分側への制限}\ \ (4/4\ \text{一致}).\ }$$
> **⟹ 測定済の「$\mathrm{GTSh}=\mathrm{Hol}\times\mathrm{Syl}_2(S_t)$」の $\mathrm{Syl}_2(S_t)$ 因子は、半局所幾何では「不分岐 cusp 点の置換」として現れる。** `surj_d4_t1_v1.md` §6.2 で作業仮説として置いた「2-群因子の算術的正体 = 不分岐 cusp 点の Galois 置換」に、**4 点の定量的裏づけ**がついた。
> **⚠ 未解明の核心が 1 つ残る**: なぜ $S_t$ **全部**でなく $\mathrm{Syl}_2(S_t)$ **だけ**か($t=3$ で $54\to18$、$t=4$ で $216\to72$)。これは発案 I10-1 の「刈り込みの処方」の問いと**同一の問い**である(§3【LG-b】)。
> **⚠ 札**: 観察 SL-3 は **candidate**(4 点一致の観測+段 I の中心化群計算という機構候補)。$\mathrm{Syl}_2$ への刈り込みの証明はない。

### 2.2 段 II-a($B_{\rm FC}$-II-a・定理 B-4「剛性 descent」)

**前件**(BFC §6.2): (TB1)–(TB3)+**(W1)(W2)(W3)(W5)**+(CAL)。**(W4) を含まない**(`surj_s4_v1.md` §3 (S1) で証明本文を走査済 — (TB4) も現れない)。

$$\boxed{\ \textbf{段 II-a は無修理で通る。}\ }$$

必要なのは (W3)(=$N_P(H)=H$ ✓ §1.1)・(W5)($\Lambda$ が $\Phi(\mathfrak F_0)$-安定)・(W1)・(W2)。
* **(W5)**: 補題 F0(`surj_s4_v1.md` §3.3)の前件は t=1 窓でも成立(【SD-c】で $C_{S_{10}}(X)=\langle X\rangle$・$\Phi|_{\mathfrak F_0}$ 全単射を実測)⟹ $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X\rangle)\subseteq\mathrm{Inn}(P)$ ⟹ $\Lambda$ は共役類ゆえ安定 ✓ **(W5) 成立**。
* **(W1)**: ⚠ **未確立**(【SD-a】= 本キャンペーンで isolated は独立検証されていない・既出 GAP-4)。**段 II-a の唯一の穴。**
* **(W2)**: 群論半は実測、算術半は補題 SURJ-Split (b) で窓非依存 ✓。

### 2.3 段 II-c($B_{\rm FC}$-II-c・補題 B-5「局所 Kummer」)— **修理の本体**

| 部品 | 現行の主張 | 半局所版の判定 |
|---|---|---|
| **B-5a**(繊維の分解) | $\mathcal O(\cdots)\cong\prod_{P\mid0}\kappa(P)((s_P))$ | ✅ **無修理**。**もともと積で書かれている**(BFC §7 補題 B-5a) |
| **B-5b**(幾何点 $\leftrightarrow$ 慣性軌道) | 幾何点 $\leftrightarrow$ $\langle x\rangle$-軌道、軌道長 $=$ 分岐指数 | ✅ **無修理**。一般の繊維で述べられている |
| **B-5(i)** | 「$\lambda^{-1}(0)$ はただ 1 点・$K$-有理・$e=M$」 | ❌ **要全面書換**。→ **補題 SL-1**:「$\lambda^{-1}(0)$ の点は軌道長で層別され、**軌道長が相異なる層の点は個別に $K$-有理**」。t=1 では 2 点とも $K$-有理 |
| **B-5(ii)** | 単一の $[u]_M$ が uniformizer・モデル非依存 | ⚠ **型の修理**。→ **補題 SL-2**:$[u_P]$ の住処は $\kappa(P)^\times/\kappa(P)^{\times e_P}$。**$e_P=1$ の点は情報ゼロ**。t=1 では $[u_{P_0}]_9$ のみが実体(命題 LG3) |
| **B-5(iii)/(7.1)** | $\mathcal O\cong K((\beta))[T]/(T^M-u^{-1}\beta)$、$\mathrm{Fib}$ が $\mu_M$-torsor | ⚠ **分解して書換**。→ $\mathrm{Fib}=\mathrm{Fib}_{P_0}\sqcup\mathrm{Fib}_{P_1}$ で、**$\mathrm{Fib}_{P_0}$ は $\mu_9$-torsor(類 $[u_{P_0}^{-1}]_9$)**、$\mathrm{Fib}_{P_1}$ は $e=1$ ゆえ $\kappa(P_1)((s_1))=K((\beta))$ で**1 点・$G_K$-固定** |
| **(7.2)** | $\gamma\cdot p=m(\kappa_{u^{-1}}(\gamma))p$ | ✅ **$\mathrm{Fib}_{P_0}$ 上でそのまま**。$\mathrm{Fib}_{P_1}$ 上は自明作用 |
| **補題 B-5$^{\rm u}$** | (i)(ii-loc)(iii)(7.1)(7.2) は $(\mathrm{TB4}^{\rm u})$ で足りる | ✅ **論法は保存される**(使うのは $\mathrm{im}(I_0)=\overline{\langle x\rangle}$ と後合成作用のみ・分岐の一様性を使わない) |

$$\boxed{\ \textbf{段 II-c の修理 = 補題 B-5(i)(ii)(iii) の 3 項の書換え。B-5a・B-5b・(7.2)・B-5}^{\rm u}\ \textbf{は無修理。}\ }$$

### 2.4 段 II-b($B_{\rm FC}$-II-b・補題 B-6「torsor 比較・$b_{\rm op}=1$」)

**現行**: $c_\Lambda:\mathrm{Fib}\xrightarrow{\sim}\Lambda$ が $\mu_M$-同変、$c_\Lambda m(\xi)c_\Lambda^{-1}=\tau(\xi)$。

**半局所(t=1)**: $\mathrm{Fib}$ も $\Lambda$ も $9+1$ に分解し、$G_K$-同変同型 $c_\Lambda$ は**分岐指数を保つので層を保つ**($\mathrm{Fib}_{P_0}\to$ 9-軌道、$\mathrm{Fib}_{P_1}\to$ 固定点)。$m(\xi)$ は $\mathrm{Fib}_{P_0}$ 上で自由・$\mathrm{Fib}_{P_1}$ 上で自明、$\tau(\xi)$ は 9-軌道上で自由・固定点上で自明 — **形が一致**。

$$\boxed{\ \textbf{段 II-b は「9-軌道への制限」を 1 行挟むだけで通る見込み。}\ (Z_{2M}\text{-link}) \textbf{ の要否は不変}.\ }$$

⚠ **$t\ge2$ では別**: $\mathrm{Fib}_{\rm 不分岐}$ が $t$ 点になり $c_\Lambda$ の制限に $S_t$ の自由度が入る ⟹ 段 I の $\sigma$ と連動して「$b$ の $S_t$-成分」という新しい比較量が生じる。

### 2.5 修理リスト(要約)

| 段 | 判定 | 要る仕事 |
|---|---|---|
| **I** | ⚠ 差し替え(t=1 は結論不変) | 命題 B-1 を「巡回型 $(\ell,1^t)$ の中心化群 $=C_\ell\times S_t$」の直接計算に差し替え。**$t=1$ なら $c$ の一意性は保たれる** |
| **II-a** | ✅ 無修理 | なし((W4) を使っていない)。**穴は (W1) = 【SD-a】のみ** |
| **II-c** | ❌ **本体** | 補題 B-5 の **(i)(ii)(iii) を書換**(SL-1・SL-2・Fib の層分解)。(iii) は「分岐点の層に制限した $\mu_{e}$-torsor」へ |
| **II-b** | ✅ ほぼ無修理 | 「9-軌道への制限」1 行 |
| **合成(定理 B-7)** | ⚠ | $c=\kappa_{u_{P_0}^{-1}}$ を**分岐 cusp の類**として述べ直す |

> ### ★ 見積りの訂正(自認)
> `surj_d4_t1_v1.md` §6.2 で私は半局所化を「**キャンペーン級**」と評価した。**t=1 に限れば過大評価だった。** 上の表のとおり **t=1 では補題 B-5 の 3 項の書換えが実体**であり、他は無修理か 1 行。**「補題の一般化」で足りる。** キャンペーン級なのは **$t\ge2$**(段 I の $\sigma$ と段 II-b の $S_t$-成分が新しい比較量を生む)である。
> ⟹ **壁窓 $W\text{-}E\text{-}A10\text{-}9t1$ の層 III は、想定より近い。** ただし (W1)(=【SD-a】)が土台として未確立である点は変わらない。

---

## 3. FINDING と未閉鎖

| # | 種別 | 内容 |
|---|---|---|
| **LG-1** | **帰属訂正(義務)** | 層 II(Hol 値 ⟺ 捻れ Kummer)は**古典**。O'Dorney 2506.11310 Abstract/§2.1 が「widespread use」と明言。**引用へ切替**(§0.2 の正誤表が erratum of record)。正味の自前寄与は §0.2 の 6 項 |
| **LG-2** | **★【LG-3】回答** | **t=1 では NORM-U$^{\rm typed}$ = MARK-U = 型 C = $[u_{P_0}]_9$**。三型一致・すべて well-defined。**ただし一様指数版 NORM-U は ill-defined**($e=1$ 点の $u$ が任意)— 覚書の定義は**型付けの修理が要る** |
| **LG-3** | **設計上の負** | **t=1 は三型の判別窓にならない**(恒真)。判別には**長さ $>1$ の巡回が 2 本以上**要る(系 LG3′)。最小候補 $\bar x=(\ell,\ell,1^t)$ は **発案 I10-1 の判別窓と同族** ⟹ 相乗り設計の候補 |
| **LG-4** | **★【LG-4】回答** | 修理は **補題 B-5(i)(ii)(iii) の 3 項に集中**。段 II-a は無修理(**(W4) を使っていない**)、段 II-b はほぼ無修理、段 I は t=1 なら結論不変 |
| **LG-5** | **★ 見積りの訂正(自認)** | 「キャンペーン級」は **t=1 に対しては過大評価**。補題書換えで足りる。キャンペーン級は $t\ge2$ |
| **LG-6** | **★ 観察 SL-3(candidate)** | $\ker\tilde\chi\cong\langle X\rangle\times\mathrm{Syl}_2(S_t)$ が梯子 **4/4** で一致し、段 I の中心化群 $C_{\mathrm{Sym}(\Lambda)}(\tau(\mu_9))=C_9\times S_t$ の 2-部分と対応。**「2-群因子 = 不分岐 cusp 点の Galois 置換」仮説に定量的裏づけ**。未解明 = なぜ $S_t$ 全部でなく $\mathrm{Syl}_2$ か |
| **LG-7** | **読解の申告** | O'Dorney は **4 頁のみ精読**(Abstract・§1・§2.1・§3)。他 5 本**未読**・Jacobson–Vélez **未入手未読**。§2 の設計は**自前の幾何計算**であり、原著の定理を引用してはいない(覚書の型 A/B/C の枠組みだけを借りた) |

### 未閉鎖・次の一手

* 【LG-a】**判別窓の設計(相乗り)**: $\bar x=(\ell,\ell,1^t)$ 型で ①NORM-U vs MARK-U vs 型 C ②I10-1 の奇部(3 vs 81)を**同時に**判別する窓を設計。$\ell=3$・小さい $t$ から。**設計チェックリスト関数の拡張で機械枚挙可能**(I10-1 の記述による)。
* 【LG-b】**$\mathrm{Syl}_2$ 刈り込みの機構**(LG-6 の未解明部)。「なぜ $S_t$ の奇部が GT に見えないか」。**I10-1 の『刈り込みの処方』と同一の問い**であり、半局所側から攻める新しい入口。
* 【LG-c】**(W1)/【SD-a】が依然として土台の穴**。$B_{\rm FC}^{\rm sl}$ をどれだけ修理しても、壁窓が isolated でなければ $\mathrm{Ih}_N$ の像の議論が立たない。**修理の前にここを閉じるべき**(優先順位の提案)。
* 【LG-d】**補題 B-5 の書換え本体**(段 II-c)は本稿の射程外(設計図まで)。着手するなら **t=1 限定**で、SL-1/SL-2 を正式な補題として起草するのが最小の一歩。
* 【LG-e】本稿は**紙上・単系統・Sol 監査前**。**Lean 検証ではない。** 観察 SL-3 の数値は既存証明書からの転記(私の新規測定ではない)。封印量非接触・$K^{(5)}$ 非接触。

> ### 【文献要請】— 本稿からは無し(既存要請は充足された)
> `surj_d4_t1_v1.md` の要請(非全分岐 cusp での半局所 Kummer 不変量)は、**t=1 に関しては本稿 §1–§2 で自前に解決した**(エタール代数が分裂し、局所指数の型付けだけで一意に決まる)。**$t\ge2$ の判別窓(【LG-a】)で新しい困難が出たら改めて要請する。**
