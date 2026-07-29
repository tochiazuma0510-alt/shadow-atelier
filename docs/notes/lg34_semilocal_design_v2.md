# 【LG-3】【LG-4】半局所 Kummer — weighted norm・判別条件の二分・$B_{\rm FC}^{\rm sl}$ 設計図 **v2**

**状態札: candidate(裁定前・単系統・Sol 監査前)。§2 の $B_{\rm FC}^{\rm sl}$ は `design NOTE`(定理として提出しない)**
起草: Claude(数学者レイヤー・Opus 5)/ 2026-07-30
**v1 → v2 の根拠**: 裁定 227 / **P86-6**(便 86 F86-4.1.4 の blocker 3 件 + 修理指示 4 件)。v1(`lg34_semilocal_design_v1.md`・SHA `643ba30a…f973db`)は**上書きせず保存**。

**v1 → v2 差分一覧**

| # | P86-6 項 / blocker | v1 | v2 |
|---|---|---|---|
| **A** | 項 1 / **B86-LG1** | `NORM-U^typed` を「局所指数で型付けしたノルム」と呼んだが、実体は**第 2 成分を捨てる射影**で、体ノルムから誘導されていなかった(**LG-3 = FAIL**) | **Sol 供給の weighted norm $N^{\rm wt}=\prod_P N_{\kappa(P)/K}(u_P)^{M/e_P}$ を正式採用**し、**体ノルムと冪写像の合成として誘導されること**と well-defined 性を §1.3 で証明 |
| **B** | 項 2 / **B86-LG2** | LG3′ の必要条件を「同じ長さの巡回 2 本」一本で書いた(**強すぎ**) | **二分**: ①三型の**情報差**の必要条件 = 分岐 cusp($e_P>1$)が 2 つ以上 ②**Galois mixing** の必要条件 = **同一** index の cusp が 2 つ以上(§1.6) |
| **C** | 項 3 / **B86-LG3** | SL-1 を「index が異なる層の点は個別に $K$-有理」と一般形で書いた(**一般には偽**) | **SL-1 を「各 index 層は $G_K$-安定・層が singleton ならその点は $K$-有理」へ訂正**(§1.1) |
| **D** | 項 4 | 段 II-b(補題 B-6)を「1 行挟むだけで通る**見込み**」と書き、修理表で ✅ 扱い | **B-6 は `design NOTE` に降格**(§2.4)。$t=1$ 限定の **B-5$^{\rm sl}$ は完全な statement + 証明**を §2.3 に置く。**(W1) は独立前件のまま明示** |
| **E** | — | — | §0 の帰属訂正は**維持**(v1 の erratum of record を継承・§0) |

**依拠**: v1 と同一 + `sol/sol_reply_86_math13.md` §4.1(F86-4.1.4・B86-LG1/2/3・P86-6)。原著読解範囲は v1 と同一(**O'Dorney 2506.11310 は Abstract・§1・§2.1・§3 の 4 頁のみ精読、他 5 本未読、Jacobson–Vélez 未入手**)。

> ## 封印遵守
> 封印量非接触。$K^{(5)}$ 非接触。$u$ の値には触れない(本稿は**定義の well-defined 性**と**設計図**のみ)。凍結済み予言(i10_1 の 11 欄・41b8698)非接触。

---

## 0. 新規性突合(v1 §0 を継承・erratum of record)

**層 II(Hol 値 ⟺ 捻れ Kummer 指標)の辞書は古典である。** O'Dorney 2506.11310 Abstract 逐語(精読済): *"the appropriate object is an étale algebra over $K$ … whose Galois group is a subgroup of the semidirect product $\mathrm{Hol}\,M=M\rtimes\mathrm{Aut}\,M$ … Although the correspondence between $H^1$ and field extensions **is in widespread use** …"*。Prop 2.1 は「$K$-Galois module 構造 ⟺($L/K$, $\mathrm{Gal}(L/K)\hookrightarrow\mathrm{Aut}\,M$)」。

⟹ `surj_d4_t1_v1.md` §2.3・§2.4・§3・§6.1 の該当箇所は**引用に切り替える**(v1 §0.2 の正誤表がその of record)。

> **正味の自前寄与(不変)**: ①補題 SURJ-Split (b)(d)(e)(GT 固有)②W-OBS / TAIL-OBS ③補題 Φ-univ / 補題 F0 ④S4 の前件と 1 ビット帰着 ⑤【SD-c】$a=+1$ の実測 ⑥本稿 §1–§2。
> **「$u$ を cusp 主係数として同定する」ことだけが古典に無い部分**であり、それは橋 $B_{\rm FC}$(自前)の仕事。

**★ 得たもの**: O'Dorney §3 のエタール代数 ⟺ $G_K$-集合の枠組(Prop 3.1/3.2)は、**§1 を書くための正しい語彙**である。以下はその語彙で書く。

---

## 1.【LG-3】v2 — weighted norm による修理

### 1.1 幾何データと SL-1【訂正 — B86-LG3】

窓 $(P,H)$、$M:=\mathrm{ord}(X)$、$K$ を基礎体とする。$\lambda^{-1}(0)$ の幾何点は $\langle x\rangle$ の $P/H$ 上の軌道と 1:1 で、軌道長 $=$ 分岐指数(BFC 補題 B-5b)。**各 $e_P$ は $M$ を割る**(軌道長は $\mathrm{ord}(X)$ の約数)。

> ### 補題 SL-1(v2 訂正形)
> $e>0$ に対し **index 層** $\Sigma_e:=\{P\in\lambda^{-1}(0)\ :\ e_P=e\}$ と置く。
> **(a)** $G_K$ は分岐指数を保つので、**各 $\Sigma_e$ は $G_K$-安定**である。
> **(b)** $\lvert\Sigma_e\rvert=1$ ならその点 $P$ は **$K$-有理**($\kappa(P)=K$)。
> **(c)** 一般には $\Sigma_e$ 上の $G_K$-作用は非自明でありうる。$\Sigma_e$ が単一軌道なら $\kappa(P)$ は $K$ の $\lvert\Sigma_e\rvert$ 次拡大、一般には $\Sigma_e$ の軌道分解に応じて $\prod$ の各因子が定まる。

> ⚠ **v1 の誤り(自認)**: v1 は「**index が異なる層の点は個別に $K$-有理**」と一般形で書いた。**これは偽**である。正しくは (a)+(b) であり、**個別の有理性は層が singleton のときだけ**。$t=1$ の $(e_0,e_1)=(9,1)$ は**両層とも singleton** なので v1 の結論(2 点とも $K$-有理)自体は正しい。**一般形の言明が強すぎた。**

**O'Dorney の語彙で**: cusp 集合は有限エタール $K$-代数 $E:=\prod_{P\mid0}\kappa(P)$ であり、$\mathrm{Coord}(E)$ は $G_K$-集合 $\lambda^{-1}(0)(\bar K)$。SL-1 (a) は「$G_K$-集合が index でグレード付けされる」ことに他ならない。

### 1.2 局所類の住処(v1 §1.2 を維持)

> ### 補題 SL-2
> $\lambda=u_P\,s_P^{e_P}(1+O(s_P))$ で、uniformizer の取り替え $s_P\mapsto a\,s_P(1+O(s_P))$($a\in\kappa(P)^\times$)により $u_P\mapsto u_P\,a^{-e_P}$。したがって $[u_P]$ が well-defined なのは
> $$[u_P]_{e_P}\in\kappa(P)^\times/\kappa(P)^{\times e_P}$$
> の中だけである。とくに $e_P=1$ なら剰余群は自明で、**$u_P$ は情報を持たない**。

### 1.3 ★ weighted norm — 正式定義と well-defined 性【P86-6 項 1】

> ### 定義 $N^{\rm wt}$(Sol 便 86 B86-LG1 供給・本稿で正式採用)
> $e_P\mid M$ を用いて
> $$\boxed{\ N^{\rm wt}\bigl(([u_P]_{e_P})_{P\mid0}\bigr)\ :=\ \prod_{P\mid0}N_{\kappa(P)/K}\bigl(u_P\bigr)^{M/e_P}\ \pmod{K^{\times M}}\ \in\ K^\times/K^{\times M}.\ }$$

> ### 補題 SL-3(well-defined 性 — **体ノルムから誘導される**)
> $N^{\rm wt}$ は、各 $P$ について**二つの標準写像の合成**である:
> $$\kappa(P)^\times/\kappa(P)^{\times e_P}\ \xrightarrow{\ (\ \cdot\ )^{M/e_P}\ }\ \kappa(P)^\times/\kappa(P)^{\times M}\ \xrightarrow{\ N_{\kappa(P)/K}\ }\ K^\times/K^{\times M},$$
> したがって群準同型として well-defined であり、その積 $\prod_P$ も well-defined。とくに uniformizer の取り替えに対し不変。

**証明.**
**(1) 冪写像**: $u'=u\,c^{e_P}$($c\in\kappa(P)^\times$)なら $u'^{M/e_P}=u^{M/e_P}c^{M}\equiv u^{M/e_P}\pmod{\kappa(P)^{\times M}}$。よって $(\ \cdot\ )^{M/e_P}$ は $\kappa(P)^\times/\kappa(P)^{\times e_P}\to\kappa(P)^\times/\kappa(P)^{\times M}$ を誘導する($M/e_P\in\mathbf Z$ は $e_P\mid M$ による)。
**(2) ノルム**: $N_{\kappa(P)/K}(c^M)=N_{\kappa(P)/K}(c)^M\in K^{\times M}$ ゆえ、体ノルムは $\kappa(P)^\times/\kappa(P)^{\times M}\to K^\times/K^{\times M}$ を誘導する。
**(3) 直接確認(uniformizer 不変性)**: $u_P\mapsto u_Pa^{-e_P}$ のとき
$$N_{\kappa(P)/K}\bigl(u_Pa^{-e_P}\bigr)^{M/e_P}=N(u_P)^{M/e_P}\cdot N(a)^{-e_P\cdot M/e_P}=N(u_P)^{M/e_P}\cdot N(a)^{-M},$$
第 2 因子は $K^{\times M}$ に属す。$\blacksquare$

> **★ B86-LG1 への回答**: v1 の `NORM-U^typed` は**射影**であってノルム誘導ではなかった(Sol の指摘は正しい)。$N^{\rm wt}$ は上の (1)(2) のとおり **$\kappa(P)/K$ の体ノルム(= Kummer 類の corestriction)と冪写像の合成**であり、「norm から誘導される」という語法が正当化される。**型の修理を数式そのものに反映した**(便 86 ★教材 3)。
> **⚠ 用語**: v1 の `NORM-U^typed` という名称は**撤回**する。以後 $N^{\rm wt}$ と書く。「分岐点だけを見る」量を指したいときは **`RAMIFIED-PROJ-U`**(= MARK-U の別名)と呼び分ける(P86-6 項 1 の指示に従う)。

### 1.4 $t=1$ での計算

$(e_{P_0},e_{P_1})=(\ell,1)$、両層 singleton ゆえ $\kappa(P_0)=\kappa(P_1)=K$(補題 SL-1 (b))、$M=\ell$。

$$N^{\rm wt}=\underbrace{N_{K/K}(u_0)^{\ell/\ell}}_{=\ [u_0]_\ell}\cdot\underbrace{N_{K/K}(u_1)^{\ell/1}}_{=\ [u_1^{\ell}]_\ell\ =\ 1}\ =\ \boxed{\ [u_0]_\ell\ }$$

**第 2 成分は $\ell$ 乗になって自動的に消える** — v1 が「射影」で手作業に捨てたものが、weighted norm では**式そのものが捨てる**。$W\text{-}E\text{-}A10\text{-}9t1$ では $\ell=M=9$ で $N^{\rm wt}=[u_0]_9$。

### 1.5 三型の比較($t=1$)

| 定義 | $t=1$ での値 | well-defined? |
|---|---|---|
| $N^{\rm wt}$(§1.3) | $[u_0]_9$ | ✅(補題 SL-3) |
| **MARK-U** = `RAMIFIED-PROJ-U` | $[u_0]_9$ | ✅(marking は**不要** — $e_0=9\ne1=e_1$ で分岐側が群論的に一意) |
| **型 C**(束ねない) | $\bigl([u_0]_9,\ 1\bigr)$ | ✅(第 2 成分は自明群) |

> ### 命題 LG3(v2 形)
> $\bar x$ の型が $(\ell,1)$($\ell>1$)の窓では
> $$N^{\rm wt}\ =\ \textbf{MARK-U}\ =\ \text{型 C の非自明成分}\ =\ [u_0]_\ell\in K^\times/K^{\times\ell},$$
> **三型は一致し、いずれも well-defined。** ⟹ **$t=1$ では定義の選択問題が起きない**(修理の前に型を決める必要がない)。

### 1.6 ★ 判別条件の二分【P86-6 項 2 / B86-LG2】

v1 の LG3′(「同じ長さの巡回が 2 本」)は**必要条件として強すぎた**。Sol の指摘どおり、$e_1\ne e_2$ でも $e_1,e_2>1$ なら型 C は 2 成分をもち、$N^{\rm wt}$ は両方を混ぜ、MARK は一方だけを選ぶ。正しくは**二つの別の条件**である。

> ### 系 LG3′(v2・二分形)
> **(I) 三型の情報差が出る必要条件**:
> $$\boxed{\ \#\{P:\ e_P>1\}\ \ge\ 2\ }$$
> ($e_P=1$ の点は補題 SL-2 より寄与ゼロ。分岐 cusp が 1 つだけなら §1.5 の計算がそのまま走り三型一致。)
> **(II) $G_K$ が cusp を相互に混ぜる必要条件**:
> $$\boxed{\ \exists e>1:\ \lvert\Sigma_e\rvert\ \ge\ 2\ }$$
> (補題 SL-1 (a) より $G_K$ は index 層をまたげない。$\kappa(P)\supsetneq K$ が起きるのはこの場合に限る。)
> **(I) と (II) は独立**: $(e)=(2,3,1^t)$ は (I) を満たし (II) を満たさない($N^{\rm wt}$ は 2 成分を混ぜるが全点 $K$-有理)。$(\ell,\ell,1^t)$ は両方を満たす。

**設計への含意**:
* **最小の (I)-判別窓**は $\bar x=(e_1,e_2,1^t)$($e_1\ne e_2$、ともに $>1$)。**$\kappa(P)=K$ のまま**なので幾何が軽く、$N^{\rm wt}$ vs MARK の差だけを純粋に見られる。**v1 が「$(\ell,\ell,1^t)$ が必要」と書いたのは誤り** — こちらの方が安い。
* **(II)-判別窓**は $(\ell,\ell,1^t)$ で、これは**発案 I10-1 の判別窓と同族**(相乗り候補・§3【LG-a】)。
* **両方を一度に見たいなら** $(\ell,\ell,e_3,1^t)$ 型。

---

## 2.【LG-4】v2 — $B_{\rm FC}^{\rm sl}$ の設計図(**design NOTE**)

> ### 札の明示【P86-6 項 4】
> **本節は定理として提出しない。** 便 86 F86-4.1.4 のとおり、B-6 の torsor comparison が「9 軌道への制限 1 行」で閉じることは**未証明**であり、**(W1) も未閉鎖**である。§2.3 の B-5$^{\rm sl}$($t=1$ 限定)だけは statement + 証明を書くが、**(W1) を独立前件として明示的に外に置く**。

### 2.1 段 I(定理 B-3)— 中心化群の直接計算へ差し替え

$\Lambda\cong P/H$((W3) から命題 B-2 (B2-bij)・**(W4) 不要**)。$\tau(\zeta_M)$ は $X$ による左移動で巡回型 $(\ell,1^t)$。$S_{\ell+t}$ における巡回型 $(\ell,1^t)$ の元の中心化群の位数は $\ell\cdot t!$ ゆえ
$$C_{\mathrm{Sym}(\Lambda)}\bigl(\tau(\mu_\ell)\bigr)\ \cong\ \langle X\rangle\times S_t .$$
* **$t=1$**: $S_1=1$ ⟹ 中心化群 $=\tau(\mu_\ell)$ ⟹ **命題 B-1 の結論(自己中心化)が正則性なしに成立**、$c$ の一意性は保たれる。
* **$t\ge2$**: $\rho_\Lambda(\mathrm{Ih}(\gamma))$ は対 $\bigl(c(\gamma),\sigma(\gamma)\bigr)\in\mu_\ell\times S_t$ を与える。$\sigma:G_K\to S_t$ が**不分岐 cusp 点の Galois 置換**。

> ### 観察 SL-4(v1 の観察 SL-3 を改称・**candidate**)
> 梯子 4 窓の実測 $\ker\tilde\chi$(証明書からの転記):
>
> | 窓 | $t$ | 実測 $\ker\tilde\chi$ | $\lvert\ker\rvert$ | $\langle X\rangle\times\mathrm{Syl}_2(S_t)$ | $\lvert\langle X\rangle\times S_t\rvert=9\cdot t!$ |
> |---|---|---|---|---|---|
> | A10-9t1 | 1 | $C_9$ | 9 | $C_9$ ✓ | 9 |
> | A11-9t2 | 2 | $C_{18}$ | 18 | $C_9\times C_2$ ✓ | 18 |
> | A12-9t3 | 3 | $C_{18}$ | 18 | $C_9\times C_2$ ✓ | 54 |
> | A13-9t4 | 4 | $C_9\times D_8$ | 72 | $C_9\times D_8$ ✓ | 216 |
>
> $\ker\tilde\chi\cong\langle X\rangle\times\mathrm{Syl}_2(S_t)$ が **4/4 一致**し、段 I の中心化群 $\langle X\rangle\times S_t$ の **2-部分**に対応する。
> **⟹「2-群因子 = 不分岐 cusp 点の Galois 置換」仮説に定量的裏づけ。** 未解明 = **なぜ $S_t$ 全部でなく $\mathrm{Syl}_2$ か**($t=3$ で $54\to18$、$t=4$ で $216\to72$)。これは発案 I10-1 の「刈り込みの処方」と同一の問い。
> **札: candidate**(4 点一致の観測 + 中心化群計算という機構候補。刈り込みの証明はない)。

### 2.2 段 II-a(定理 B-4)— 無修理

前件は (TB1)–(TB3)+(W1)(W2)(W3)(W5)+(CAL) で **(W4) を含まない**(`surj_s4_v1.md` §3 (S1) で BFC §6.2 の証明本文を走査済 — (TB4) も現れない)。$t=1$ 窓で (W3) ✓・(W5) ✓(補題 F0 の前件を【SD-c】証明書が満たす)・(W2) ✓。
$$\boxed{\ \textbf{穴は (W1) のみ — 【SD-a】により UNKNOWN。独立前件として外に置く。}\ }$$

### 2.3 段 II-c(補題 B-5)— $t=1$ 限定の完全 statement【P86-6 項 4】

> ### 補題 B-5$^{\rm sl}$($t=1$ 半局所版)
> **前件**: (TB1)(TB2)(TB3)(TB4$^{\rm u}$)、$K$-モデル $W_0\to U_K$ が与えられている、$\bar x$ の $P/H$ 上の巡回型が $(\ell,1)$、$M=\mathrm{ord}(X)=\ell$。**((W1) は本補題の前件ではない — モデルの存在は段 II-a が供給する。)**
> **(i)** $\lambda^{-1}(0)=\{P_0,P_1\}$、$e_{P_0}=\ell$、$e_{P_1}=1$、**両点とも $K$-有理**。
> **(ii)** $P_0$ の任意の $K$-有理 uniformizer $s_0$ について $\lambda=u_0\,s_0^{\ell}(1+O(s_0))$、$u_0\in K^\times$、**$[u_0]_\ell$ は $s_0$ に依らない**。$P_1$ では $\lambda$ 自身が uniformizer で、$[u_1]_1=1$ は情報を持たない。
> **(iii)** $K((\beta))$-代数として
> $$\mathcal O\bigl(W_0\times_U\mathrm{Spec}\,K((\beta))\bigr)\ \cong\ K((\beta))[T]/\bigl(T^{\ell}-u_0^{-1}\beta\bigr)\ \times\ K((\beta)).$$
> **(iv)** ゆえに $\mathrm{Fib}_{\vec{01}}(W_0)=\mathrm{Fib}_{P_0}\sqcup\mathrm{Fib}_{P_1}$ で
> $$\mathrm{Fib}_{P_0}=\bigl\{\xi\,(u_0^{-1})^{1/\ell}\beta^{1/\ell}:\xi\in\mu_\ell\bigr\}\ (\mu_\ell\text{-torsor,\ 類}\ [u_0^{-1}]_\ell),\qquad \lvert\mathrm{Fib}_{P_1}\rvert=1\ (G_K\text{-固定}),$$
> $$\gamma\cdot p=m\bigl(\kappa_{u_0^{-1}}(\gamma)\bigr)p\quad(p\in\mathrm{Fib}_{P_0}),\qquad \gamma\cdot p=p\quad(p\in\mathrm{Fib}_{P_1}).$$
> **(v)** $N^{\rm wt}=[u_0]_\ell$(§1.4)。

**証明.**
**(i)** 補題 B-5b より幾何点は $\langle x\rangle$-軌道と 1:1、軌道長 $=$ 分岐指数 ⟹ 2 点、指数 $\ell,1$。$\Sigma_\ell=\{P_0\}$・$\Sigma_1=\{P_1\}$ はともに singleton ゆえ補題 SL-1 (b) より $K$-有理。
**(ii)** $P_0$ は滑らかな $K$-有理点ゆえ $K$-有理 uniformizer が取れ、$v_{P_0}(\lambda)=e_{P_0}=\ell$ から $\lambda=u_0s_0^\ell+\cdots$。uniformizer 不変性は補題 SL-2($u_0\mapsto u_0a^{-\ell}$)。$P_1$ は $v_{P_1}(\lambda)=1$ ゆえ $\lambda$ 自身が uniformizer。
**(iii)** 補題 B-5a(**もともと積の形**)より $\mathcal O(\cdots)\cong\kappa(P_0)((s_0))\times\kappa(P_1)((s_1))=K((s_0))\times K((s_1))$。$P_0$ 側は BFC §7 (iii) の計算がそのまま走る($h:=u_0^{-1}\lambda s_0^{-\ell}\in K[[s_0]]$、$h(0)=1$、$\ell\in K^\times$ ゆえ $h^{1/\ell}$ が一意に存在、$\tilde s_0:=s_0h^{1/\ell}$ が $\tilde s_0^{\ell}=u_0^{-1}\beta$ を満たし、$T^\ell-u_0^{-1}\beta$ は $K((\beta))$ 上 Eisenstein で既約)。$P_1$ 側は $e=1$ ゆえ $K((s_1))=K((\lambda))=K((\beta))$(不分岐次数 1)。
**(iv)** (iii) の第 1 因子の根の集合が $\mathrm{Fib}_{P_0}$、第 2 因子が 1 点。$\gamma\in G_K$ は (TB2) より $\beta^{1/\ell}$ を固定し係数に作用するので BFC (7.2) の計算がそのまま。第 2 因子は $K((\beta))$ 自身なので $G_K$-固定。
**(v)** §1.4。$\blacksquare$

> **⟹ 修理の実体**: BFC 補題 B-5 の **(i)(ii)(iii) の 3 項の書換え**。B-5a・B-5b・(7.2) の計算・補題 B-5$^{\rm u}$(TB4$^{\rm u}$ で足りること)は**無修理で保存される**。

### 2.4 段 II-b(補題 B-6)— **design NOTE のまま**【P86-6 項 4 / 便 86】

**設計の見通し(定理主張ではない)**: $c_\Lambda:\mathrm{Fib}\to\Lambda$ は $G_K$-同変かつ $\hat F_2$-同変で、分岐指数を保つので層 $\mathrm{Fib}_{P_0}\to$($\ell$-軌道)、$\mathrm{Fib}_{P_1}\to$(固定点)を保つはずである。$m(\xi)$ は $\mathrm{Fib}_{P_0}$ 上自由・$\mathrm{Fib}_{P_1}$ 上自明、$\tau(\xi)$ は $\ell$-軌道上自由・固定点上自明で**形が一致する**。

> ⚠ **これは証明ではない。** 便 86 F86-4.1.4 の指摘どおり、
> 1. $c_\Lambda$ が層を保つことの証明(同変性から従うはずだが未記述)、
> 2. 制限後に $c_\Lambda\,m(\xi)\,c_\Lambda^{-1}=\tau(\xi)$ が成り立つことの証明、
> 3. $(Z_{2M}$-link$)$ の役割が半局所化で変わらないことの確認、
>
> のいずれも書いていない。**さらに (W1) が未閉鎖**である。したがって本節は **`design NOTE`** であり、$B_{\rm FC}^{\rm sl}$ を定理として提出しない。
> **$t\ge2$ ではさらに**: $\mathrm{Fib}_{\rm 不分岐}$ が $t$ 点になり $c_\Lambda$ の制限に $S_t$ の自由度が入る ⟹ 段 I の $\sigma$ と連動して「$b$ の $S_t$-成分」という**新しい比較量**が生じる。

### 2.5 修理リスト(v2)

| 段 | 判定($t=1$) | 要る仕事 | 札 |
|---|---|---|---|
| **I** | 結論不変 | 命題 B-1(正則性)を巡回型 $(\ell,1^t)$ の中心化群計算に差し替え | 紙(§2.1) |
| **II-a** | 無修理 | なし。**穴は (W1) のみ** | (W1) は UNKNOWN |
| **II-c** | **本体** | 補題 B-5 の (i)(ii)(iii) を書換 | **§2.3 に完全 statement + 証明** |
| **II-b** | 未証明 | $c_\Lambda$ の層保存 + 制限後の (8.1) | **design NOTE** |
| **合成 B-7** | 未 | $c=\kappa_{u_0^{-1}}$ として述べ直す | design NOTE |

> ### 見積り(v1 の自認を維持)
> `surj_d4_t1_v1.md` §6.2 の「キャンペーン級」は **$t=1$ に対しては過大評価**だった。$t=1$ の実体は補題 B-5 の 3 項の書換えで、**§2.3 で実際に書けた**。キャンペーン級なのは **$t\ge2$**(段 I の $\sigma$ と段 II-b の $S_t$-成分)。
> **ただし** $t=1$ でも **(W1) と段 II-b が未閉鎖**なので、**壁窓の層 III は依然として開いている**。

---

## 3. FINDING と未閉鎖(v2)

| # | 種別 | 内容 |
|---|---|---|
| **LG-1** | 帰属訂正(継続) | 層 II は古典(O'Dorney / Jacobson–Vélez)。v1 §0.2 の正誤表が of record |
| **LG-2** | **修理完了(v2)** | **B86-LG1 解消**: $N^{\rm wt}=\prod_PN_{\kappa(P)/K}(u_P)^{M/e_P}$ を正式採用し、**冪写像 ∘ 体ノルムの合成**として well-defined 性を証明(補題 SL-3)。v1 の `NORM-U^typed`(射影)は**撤回・改称** |
| **LG-3** | **修理完了(v2)** | **B86-LG2 解消**: LG3′ を **(I) 情報差 = 分岐 cusp ≥2** と **(II) Galois mixing = 同 index cusp ≥2** に二分。**最小の (I)-判別窓は $(e_1,e_2,1^t)$($e_1\ne e_2$)で、v1 の $(\ell,\ell,1^t)$ より安い** |
| **LG-4** | **修理完了(v2)** | **B86-LG3 解消**: SL-1 を「各 index 層は $G_K$-安定・singleton なら有理」へ訂正。v1 の一般形は偽 |
| **LG-5** | **$t=1$ の B-5$^{\rm sl}$** | statement + 証明を §2.3 に。**(W1) は独立前件として外出し** |
| **LG-6** | **札の降格(v2)** | 段 II-b(B-6)は **design NOTE**。$B_{\rm FC}^{\rm sl}$ を定理として提出しない |
| **LG-7** | 観察 SL-4(candidate) | $\ker\tilde\chi\cong\langle X\rangle\times\mathrm{Syl}_2(S_t)$ が 4/4 一致・段 I の中心化群の 2-部分に対応。未解明 = $\mathrm{Syl}_2$ 刈り込みの機構 |
| **LG-8** | 読解の申告(継続) | O'Dorney **4 頁のみ精読**、他 5 本**未読**、Jacobson–Vélez **未入手未読**。§1–§2 は**自前の幾何計算**で、原著の定理を引用してはいない(型 A/B/C の枠組だけを覚書から借りた) |

### 未閉鎖・次の一手

* 【LG-a】**判別窓の設計**: **(I)-判別**には $(e_1,e_2,1^t)$($e_1\ne e_2>1$)が最小・最安。**(II)-判別**には $(\ell,\ell,1^t)$ で、これは**発案 I10-1 の判別窓と同族**(相乗り候補)。設計チェックリスト関数の拡張で機械枚挙可能。
* 【LG-b】**$\mathrm{Syl}_2$ 刈り込みの機構**(LG-7)。「なぜ $S_t$ の奇部が GT に見えないか」= I10-1 の刈り込みの処方と同一の問い。半局所側からの新しい入口。
* 【LG-c】**(W1)/【SD-a】が土台の穴**(最優先)。$B_{\rm FC}^{\rm sl}$ をどれだけ修理しても、壁窓が isolated でなければ $\mathrm{Ih}_N$ の像の議論が立たない。
* 【LG-d】**段 II-b の証明**($c_\Lambda$ の層保存 + 制限後の (8.1))。これが書ければ $t=1$ の $B_{\rm FC}^{\rm sl}$ が定理候補になる。
* 【LG-e】本稿は**紙上・単系統・Sol 監査前**。**Lean 検証ではない。** 観察 SL-4 の数値は既存証明書からの転記。封印量非接触・$K^{(5)}$ 非接触。

> ### 【文献要請】— 本稿からは無し
> $t=1$ の半局所 Kummer 不変量は §1(weighted norm)+ §2.3(B-5$^{\rm sl}$)で閉じた。**$t\ge2$ の判別窓(【LG-a】)と段 II-b(【LG-d】)で新しい困難が出たら改めて要請する。**
