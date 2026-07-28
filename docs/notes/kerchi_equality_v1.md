# 等号問題 $\ker\widetilde\chi=[\operatorname{GT}(N),\operatorname{GT}(N)]$ — 一般判定条件・dihedral 族での定理・**atlas 内の反例**

**状態札: candidate(裁定前・未 commit)**
起草: Claude(数学者レイヤー・Opus 5)/ 2026-07-29
設問: 司令塔委嘱(便 79 検分材料)/ `docs/notes/w2fam_v1.md`(dihedral 族での等号)の一般化
正典・依拠:
- `docs/week1-定義ノート.md` §3(GT-pair Def 3.1・charming・合成 (3.53)・(3.49)・逆元 (3.54)・$\chi_{\rm vir}$・$N_{\rm ord}$ (3.1))
- 正典 arXiv **2405.11725**: §1.3 Ihara 準同型 $\operatorname{Ih}_N=\mathrm{PR}_N\circ\operatorname{Ih}$、$\operatorname{Ih}(g)=((\chi(g)-1)/2,f_g)$、図式 (1.10)(1.13)、Remark 1.3(全射性の唯一の証明経路)、**Thm 4.6** (4.23)(4.24)($\operatorname{GT}(K^{(n)})\cong\operatorname{Aff}(\mathbf Z/n_0)\times\mathcal Z_2$ / $\times\widetilde H_\alpha$)、Cor 5.4
- `docs/notes/w2fam_v1.md`(命題 (W2)-fam・§3.4 別証)/ `docs/notes/oddH_full_proof_v1.md` §11.1($\Phi|_A=\operatorname{diag}(u,u,1-2\varkappa(m))$)
- `provenance/registered/universe_wall_v1.md`(v1.1 draft・FAIL-2 の文言)
- 外部文献なし。群論的入力は **有限アーベル群の Schur 乗数 $H_2(A)=\Lambda^2A$** と **LHS 5 項完全列**のみ(標準)。

> ## 封印遵守
> **$u$・封印 3 量($u_9/a_9$ の値・$c$ の平方類・$\hat c_\mu$)に一切触れていない。** 本稿は純粋に有限群論であり、算術的入力は「円分指標 $\chi:G_{\mathbf Q}\to\widehat{\mathbf Z}^\times$ が全射」ただ一つ(§2 (AR))。
> ## C2F 遵守
> **$\Phi$ の商群上の像で数えていない。** 全ての測定は **shadow(GT-pair)水準の合成表**((3.53) で構成)を入力とし、スクリプトは「表が (3.53) の第一成分 $2m_1m_2+m_1+m_2$ を再現するか」を fail-closed assert で検査してから測っている(裁定 147・宇宙登録 v1.1 (2b))。

---

## 1. 結論(要旨)

**問いへの答は NO(一般には成り立たない)。** ただし正確な判定条件が付き、既存の主線は無傷である。

| # | 主張 | 状態 |
|---|---|---|
| **T-A** | **$\widetilde\chi_{2M}$ は全ての $N\in\mathrm{NFI}_{PB_3}(B_3)$ で well-defined な全射準同型**で $\ker\widetilde\chi_{2M}=\mathfrak F_0$。ゆえに**無料の個数等式** $\;|\ker\widetilde\chi_{2M}|=|\operatorname{GT}(N)|/\varphi(2N_{\rm ord})$ | **証明**(算術的入力 1 個)。**25 窓で実測一致・不一致ゼロ** |
| **T-B** | **判定条件(完全)**: $\displaystyle\ker\widetilde\chi/[\operatorname{GT},\operatorname{GT}]\ \cong\ \operatorname{coker}\Bigl(\Lambda^2\bigl((\mathbf Z/2M)^\times\bigr)\xrightarrow{\ \mathrm{tg}\ }(\mathfrak F_0^{\rm ab})_{(\mathbf Z/2M)^\times}\Bigr)$ | **証明**(LHS 5 項完全列) |
| **T-C** | **dihedral 族では等号が成立 — 全ての $n\ge3$**(奇・$\alpha=1$・$\alpha\ge2$・混合を含む)。(W2)-fam(奇のみ)の完全な一般化 | **証明**。**16 証明書で cross-checked**(K3–K36) |
| **T-D** | **等号は一般には偽。反例は既に登録 atlas の中にある: $L=K^{(3)}\cap N_0$** — $\ker\widetilde\chi\cong C_3\times C_3$、$[\operatorname{GT},\operatorname{GT}]\cong C_3$、**指数 3** | **実測(shadow 水準・cross-checked 証明書)+ 独立な a priori 証明**(§5.2) |
| **T-E** | 反例の**機構**: $\Phi_{m,f}$ は $F_2^{\rm ab}$ に重み $u$、交換子層 $\gamma_2/\gamma_3$ に**重み $u^2$** で作用する。$u^2\equiv1$ となる指数($e\mid24$)の交換子層は **GT-不変**になり、$\mathfrak F_0$ に $Q$-自明な直和因子を生む | **証明**(§5.3 Prop W/W2) |
| **T-F** | **壁ソルバーへの帰結**: TIER-0(自由・無傷)/ TIER-1 の昇格は**窓ごとの等号証明書**が要る / **新設 TIER-1.5 は等号不要で非 metabelian を確定する** | §7 |
| **T-G** | **補題 P(最安の篩)**: $|\mathfrak F_0|$ が素数なら「等号 $\iff\operatorname{GT}(N)$ 非可換」。**反例は $|\mathfrak F_0|$ 非素数の窓にしか存在しない**。合成表不要 — $N_{\rm ord}$ と $|\operatorname{GT}|$ だけで篩える | **証明**。18 窓中 11 窓を一撃で決定。atlas の $M_Q,N_A,M_{A_5}$ もこれで確定 |

---

## 2. 一般設定と T-A

$N\in\mathrm{NFI}_{PB_3}(B_3)$、$M:=N_{\rm ord}=\operatorname{lcm}(\operatorname{ord}(xN),\operatorname{ord}(yN),\operatorname{ord}(cN))$(定義ノート (3.1))。GT-pair は $[m,f]$、$m\in\mathbf Z/M$(Def 3.1)。$\operatorname{GT}(N):=\operatorname{GTSh}(N,N)$、合成は (3.53)。

$$\widetilde\chi_{2M}:\ \operatorname{GT}(N)\longrightarrow(\mathbf Z/2M)^\times,\qquad [m,f]\longmapsto 2m+1\ (\mathrm{mod}\ 2M).$$

> ### 定理 T-A
> 任意の $N\in\mathrm{NFI}_{PB_3}(B_3)$ について:
> 1. $\widetilde\chi_{2M}$ は **well-defined** であり、$2M$ は well-defined になる**最細の水準**である。
> 2. 値は単元で、$\widetilde\chi_{2M}$ は**群準同型**である。
> 3. $\ker\widetilde\chi_{2M}=\mathfrak F_0:=\{[0,f]\in\operatorname{GT}(N)\}$。
> 4. **(AR) の下で** $\widetilde\chi_{2M}$ は**全射**である。
> 5. ゆえに $\boxed{\ |\mathfrak F_0|=|\operatorname{GT}(N)|\big/\varphi(2N_{\rm ord})\ }$、および $|\operatorname{GT}(N)^{\rm ab}|\ge\varphi(2N_{\rm ord})$、等号は $\ker\widetilde\chi=[\operatorname{GT},\operatorname{GT}]$ と同値。

**証明.**
(1) $m$ は $\mathbf Z/M$ の類。$m\mapsto m+M$ で $2m+1\mapsto(2m+1)+2M$ ✓。$4M$ を法にすると $2M\not\equiv0$ で壊れる ✓(w2fam §3.1 の議論は $M=2n$ に依存しない)。
(2) charming より $\gcd(2m+1,M)=1$。$2m+1$ は奇数だから $2$ の任意冪と互いに素、ゆえに $\gcd(2m+1,2M)=1$。準同型性は (3.53) の第一成分と**整数の恒等式** (3.49)
$$2(2m_1m_2+m_1+m_2)+1=(2m_1+1)(2m_2+1)$$
から。恒等式は $\mathbf Z$ で厳密なので法を取る順序の誤差は出ない。単位元 $[0,1]\mapsto1$。
(3) $2m+1\equiv1\ (2M)\iff2m\equiv0\ (2M)\iff m\equiv0\ (M)\iff m=0$ in $\mathbf Z/M$。
(4) **(AR)** = 「$\operatorname{Ih}_N=\mathrm{PR}_N\circ\operatorname{Ih}:G_{\mathbf Q}\to\operatorname{GT}(N)$ が存在し $\operatorname{Ih}(g)=((\chi(g)-1)/2,\,f_g)$」(2405 §1.3・図式 (1.10)(1.13))。$\chi(g)\in\widehat{\mathbf Z}^\times$ は奇なので $(\chi(g)-1)/2\in\widehat{\mathbf Z}$ が定義でき、
$$\widetilde\chi_{2M}(\operatorname{Ih}_N(g))=2\cdot\tfrac{\chi(g)-1}{2}+1=\chi(g)\ \ (\mathrm{mod}\ 2M).$$
$\chi$ は全射(Kronecker–Weber)ゆえ $\chi\bmod2M$ は $(\mathbf Z/2M)^\times$ へ全射。よって $\widetilde\chi_{2M}$ も全射。$\blacksquare$

> **註 1(算術的入力はここだけ)**: 正典 Remark 1.3 は「$\chi_{\rm vir,N}$ の全射性はこれ以外の証明を知らない」と明言する。本稿の (4) はその**水準 $2M$ 版**である。(1)(2)(3)(5) は純群論。
> **註 2(実測)**: (4)(5) は §6 で **25 窓**(composition table をもつ 18 窓 + battery 7 窓)で確認され、**不一致ゼロ**。したがって (AR) を仮定に置くことに実務上の危険はない。
> **註 3(掃引への即効)**: (5) は壁キャンペーンに **無料の fail-closed assert** を与える。列挙した $|\ker\widetilde\chi|$ が $|\operatorname{GT}(N)|/\varphi(2N_{\rm ord})$ と食い違えば、その窓の列挙は壊れている(C2F 型の $\Phi$ 潰れを含む系統誤りの検出器)。**$N_{\rm ord}$ は掃引が既に全窓で記録する量**(v1.1 パイプライン 1)なので追加コストはゼロ。

**記号**: 以下 $Q:=(\mathbf Z/2M)^\times=\operatorname{Im}\widetilde\chi$、$\mathfrak F_0=\ker\widetilde\chi$、$G:=\operatorname{GT}(N)$。**$[G,G]\subseteq\mathfrak F_0$ は $Q$ が可換であることから自明**(委嘱文のとおり)。問題は逆包含。

---

## 3. T-B — 完全な判定条件

> ### 定理 T-B(判定条件)
> $1\to\mathfrak F_0\to G\xrightarrow{\widetilde\chi}Q\to1$ に対し、**自然な同型**
> $$\boxed{\ \ker\widetilde\chi\big/[G,G]\ \cong\ \operatorname{coker}\Bigl(H_2(Q;\mathbf Z)\xrightarrow{\ \mathrm{tg}\ }\bigl(\mathfrak F_0^{\rm ab}\bigr)_Q\Bigr),\qquad H_2(Q;\mathbf Z)=\Lambda^2Q\ }$$
> がある($(\ \cdot\ )_Q$ = 共役作用に関する余不変量 $=\mathfrak F_0^{\rm ab}/\langle\,gxg^{-1}x^{-1}\,\rangle$)。とくに:
> * **(B1)** $(\mathfrak F_0^{\rm ab})_Q=0\ \Longrightarrow$ **等号成立**。
> * **(B2)** $Q$ が**巡回**なら $\Lambda^2Q=0$ ゆえ **等号成立 $\iff(\mathfrak F_0^{\rm ab})_Q=0$**。
> * **(B3)** $\mathfrak F_0^{\rm ab}$ が **$Q$-自明な商 $V\ne0$** をもち $\gcd(|V|,|\Lambda^2Q|)=1$ なら **等号は破れ**、$\ker\widetilde\chi/[G,G]\twoheadrightarrow V$。

**証明.** 群のホモロジーの Lyndon–Hochschild–Serre 5 項完全列
$$H_2(G)\to H_2(Q)\xrightarrow{\ \mathrm{tg}\ }H_0\bigl(Q,H_1(\mathfrak F_0)\bigr)\to H_1(G)\to H_1(Q)\to0$$
において $H_1(\ \cdot\ )=(\ \cdot\ )^{\rm ab}$、$H_0(Q,\mathfrak F_0^{\rm ab})=(\mathfrak F_0^{\rm ab})_Q$。末尾 3 項から
$$\ker\bigl(G^{\rm ab}\to Q\bigr)\cong\operatorname{coker}(\mathrm{tg}).$$
一方 $\widetilde\chi$ は全射で $[G,G]\subseteq\mathfrak F_0$ だから $\ker(G^{\rm ab}\to Q)=\mathfrak F_0[G,G]/[G,G]=\mathfrak F_0/[G,G]$。$Q$ は有限アーベルなので $H_2(Q;\mathbf Z)\cong\Lambda^2Q$(有限アーベル群の Schur 乗数)。
(B1) 余不変量が $0$ なら coker も $0$。(B2) 巡回群は $\Lambda^2=0$。(B3) 合成 $\Lambda^2Q\to(\mathfrak F_0^{\rm ab})_Q\twoheadrightarrow V_Q=V$ は位数互いに素な有限群の間の準同型ゆえ $0$、よって $\operatorname{coker}(\mathrm{tg})\twoheadrightarrow V\ne0$。$\blacksquare$

> **註(なぜ余不変量だけでは足りないか)**: 実測(§6)で **K8・K16 は $(\mathfrak F_0)_Q\cong\mathbf Z/2\ne0$ なのに等号が成立**する。そこでは $\Lambda^2Q=\mathbf Z/2$ からの transgression がちょうど余不変量を潰している。**「余不変量 $\ne0$ ⟹ 反例」は誤り**であり、T-B の coker まで見る必要がある — これが本稿の技術的な核心。

$Q=(\mathbf Z/2M)^\times$ は $M$ だけで決まるので、**$\Lambda^2Q$ は窓に依らず $N_{\rm ord}$ の算術関数として先に表にできる**(掃引の前処理として有用)。

### 3.1 素数位数の核 — 最安の判定

> **補題 P.** $|\mathfrak F_0|=|\operatorname{GT}(N)|/\varphi(2N_{\rm ord})$ が**素数**なら
> $$\ker\widetilde\chi=[\operatorname{GT},\operatorname{GT}]\ \iff\ \operatorname{GT}(N)\ \text{が非可換}.$$
> **証明.** $[\operatorname{GT},\operatorname{GT}]$ は素数位数群 $\mathfrak F_0$ の部分群だから $1$ か $\mathfrak F_0$。$\blacksquare$
> **系.** $|\mathfrak F_0|=1$ なら等号は自明に成立。

これは **$N_{\rm ord}$ と $|\operatorname{GT}(N)|$ と可換性の 3 つだけ**で判定でき、合成表を必要としない。§6 の 18 窓のうち **11 窓(K3,K5,K6,K7,K8,K10,K11,K12,K13,K14,M01)がこれ一本で決まる**。反例 $L$ は $|\mathfrak F_0|=9$(非素数)で、補題 P の射程外である — **反例は $|\mathfrak F_0|$ が非素数の窓にしか存在しえない**。

---

## 4. T-C — dihedral 族では等号が成立(全 $n$)

> ### 定理 T-C
> 全ての $n\ge3$ について $\ker\widetilde\chi_{2M}=[\operatorname{GT}(K^{(n)}),\operatorname{GT}(K^{(n)})]$、同値に
> $$\bigl|\operatorname{GT}(K^{(n)})^{\rm ab}\bigr|=\varphi(2N_{\rm ord}).$$

**証明.** $n=n_0\cdot2^\alpha$($n_0$ 奇)。T-A(5) より、示すべきは $|[G,G]|=|G|/\varphi(2M)$ である($[G,G]\subseteq\mathfrak F_0$ は既知なので**位数の一致で十分**)。正典 Thm 4.6 (4.23) を使う。

**(i) $\alpha=0$($n$ 奇)**: $M=\operatorname{lcm}(n,2)=2n_0$、$2M=4n_0$、$\varphi(2M)=2\varphi(n_0)$。$G\cong\operatorname{Aff}(\mathbf Z/n_0)\times\mathcal Z_2$、$|G|=2n_0\varphi(n_0)$。$n_0$ 奇ゆえ $-1\in(\mathbf Z/n_0)^\times$ で $u-1=-2$ は可逆、よって $[\operatorname{Aff}(\mathbf Z/n_0),\operatorname{Aff}(\mathbf Z/n_0)]=$ 並進部 $\cong\mathbf Z/n_0$、$\mathcal Z_2$ は可換直積因子。$|[G,G]|=n_0=|G|/\varphi(2M)$ ✓(= w2fam §3.4 別証)。

**(ii) $\alpha=1$($n=2n_0$)**: $M=\operatorname{lcm}(n,2)=2n_0$、$\varphi(2M)=\varphi(4n_0)=2\varphi(n_0)$。Thm 4.6 は $\alpha<2$ で同じ $\operatorname{Aff}(\mathbf Z/n_0)\times\mathcal Z_2$ を与えるので (i) と同一計算 ✓。

**(iii) $\alpha\ge2$**: $M=n=n_02^\alpha$、$2M=n_02^{\alpha+1}$、$\varphi(2M)=\varphi(n_0)2^\alpha$。$G\cong\operatorname{Aff}(\mathbf Z/n_0)\times\widetilde H_\alpha$、
$$\widetilde H_\alpha=\bigl\{(\bar k,(-1)^a\bar5^{\,b})\in\mathbf Z/2^{\alpha-1}\rtimes(\mathbf Z/2^{\alpha+1})^\times\ \bigm|\ k\equiv b\ (2)\bigr\},\quad|\widetilde H_\alpha|=2^{2\alpha-2}\ \ \text{(4.24)}.$$
$\operatorname{Aff}(\mathbf Z/m)$ 内の交換子は直接計算で
$$[(k_1,u_1),(k_2,u_2)]=\bigl((1-u_2)k_1+(u_1-1)k_2,\ 1\bigr)$$
(第 2 成分が可換なので交換子は必ず並進)。$\widetilde H_\alpha$ では $u$ は奇数だから $u-1$ は偶数、よって $[\widetilde H_\alpha,\widetilde H_\alpha]\subseteq2\,\mathbf Z/2^{\alpha-1}$。逆に $g_1=(0,-1)\in\widetilde H_\alpha$($b=0,k=0$、$k\equiv b$ ✓)と $g_2=(k,u)$($任意の k$ に対し $b\equiv k\ (2)$ を選べる)で
$$[g_1,g_2]=\bigl((1-u)\cdot0+(-1-1)k,\ 1\bigr)=(-2k,1),$$
$k$ を動かせば $2\,\mathbf Z/2^{\alpha-1}$ 全体を得る。ゆえに $[\widetilde H_\alpha,\widetilde H_\alpha]=2\,\mathbf Z/2^{\alpha-1}$、位数 $2^{\alpha-2}$。
したがって $|[G,G]|=n_0\cdot2^{\alpha-2}=|G|/\varphi(2M)$ ✓。$\blacksquare$

> **註($\alpha\ge2$ では transgression が実際に働く)**: (iii) で $\mathfrak F_0=2\,\mathbf Z/2^{\alpha-1}$、$Q\ni u$ の作用は $u$ 倍。$u-1$ は常に偶数なので $[Q,\mathfrak F_0]\subseteq4\mathbf Z$、すなわち $(\mathfrak F_0)_Q\cong\mathbf Z/2\ne0$($\alpha\ge3$)。それでも等号が立つのは、$Q=(\mathbf Z/2^{\alpha+1})^\times\cong\mathbf Z/2\times\mathbf Z/2^{\alpha-1}$ の $\Lambda^2Q\cong\mathbf Z/2$ から transgression が全射だからである。**上の (iii) の直接計算はこの transgression を「手で」実行したものにあたる。** 実測 K8・K16 の $|(\mathfrak F_0)_Q|=2$ がこれに対応する(§6)。

---

## 5. T-D — 反例($L=K^{(3)}\cap N_0$)

### 5.1 実測

**対象**: `certificates/L01.v1.json`(atlas 登録窓 $L$)。$PB_3/L\cong G_3\times H_3$($H_3$ = 位数 27 の Heisenberg 群、$X=(1,0,0)$、$Y=(0,1,0)$)、$c\in L$、$[B_3:L]=17496$、$N_{\rm ord}=6$。

| 量 | 値 |
|---|---|
| $|\operatorname{GT}(L)|$ | **36** |
| $Q=(\mathbf Z/12)^\times$ | $\cong(\mathbf Z/2)^2$、位数 4、$\widetilde\chi$ は**全射**(実測 $\operatorname{Im}=\{1,5,7,11\}$) |
| $|\mathfrak F_0|=36/\varphi(12)$ | **9**(T-A(5) と一致 ✓)。構造 $\cong C_3\times C_3$(全元の位数 $\in\{1,3\}$・可換) |
| $|[\operatorname{GT}(L),\operatorname{GT}(L)]|$ | **3** |
| $\ker\widetilde\chi/[\operatorname{GT},\operatorname{GT}]$ | $\cong\mathbf Z/3$ — **等号は破れている** |
| $(\mathfrak F_0)_Q$ | $\cong\mathbf Z/3$(実測) |
| $\Lambda^2Q=\Lambda^2((\mathbf Z/2)^2)$ | $\cong\mathbf Z/2$ |
| $|\operatorname{GT}(L)^{\rm ab}|$ | **12** $\ne\varphi(2N_{\rm ord})=4$ |

**根拠の質**: 合成表 `L01.v1.json` の 1296 エントリは **GAP 4.16.0(`search/week3-L-explorer.g`)で生成 → node の独立レーンが全件再計算**(`crosscheck/verdicts/L01.v1.verdict.json` item `7_composition_table`: `ok:true, checked:1296, fails:[]`)。すなわち **cross-checked**(二系統一致)。**verified(Lean)ではない。** 本稿の測定スクリプトはさらに ①単位元の一意性 ②結合律 1296³ 全件 ③Latin 方陣性 ④**(3.53) 第一成分 $2m_1m_2+m_1+m_2$ の再現** ⑤$\widetilde\chi$ の準同型性、を fail-closed assert してから測っている。

**測定スクリプト**: `search/kerchi-abelianization-check.py`(sha256 `bbcc5bf058069dff9154a067a4fee27880c50e4585744a6cafe24a0f52f9ea26`)。標準ライブラリのみ・GAP 不要・再実行は `python search/kerchi-abelianization-check.py`。

### 5.2 独立な a priori 証明(実測に依存しない)

$Q$-加群としての $\mathfrak F_0\cong\mathbf F_3^2$ の分解を実測(スクリプト)で読むと、基底 $(g_1,g_2)$ で対角:

| $u\in Q$ | $g_1$ への作用 | $g_2$ への作用 |
|---|---|---|
| $1,7$ | $+1$ | $+1$ |
| $5,11$ | $+1$ | $-1$ |

すなわち $\mathfrak F_0\cong\mathbf 1\oplus\chi_3$、$\chi_3(u)=(u\bmod3)\in\{\pm1\}$。$g_1$ は shadow $[0,\ [x^2,y^2]\,]$(証明書 index 6・$f$-word $=x^2y^2x^{-2}y^{-2}$)、$g_2$ は index 8。

**$g_1$ が $Q$-自明であることの証明(実測不要)**: $H_3$ は class 2 で $[X,Y]$ が中心を生成し位数 3。$\Phi_{m,f}$ は $X\mapsto X^{u}$、$Y\mapsto f^{-1}Y^{u}f$($u=2m+1$)を誘導するので、class 2 ゆえ
$$[X,Y]\ \longmapsto\ [X^{u},Y^{u}]=[X,Y]^{u^2}.$$
$u\in(\mathbf Z/12)^\times$ に対し $u\equiv\pm1\ (3)$、よって $u^2\equiv1\ (3)$。**中心方向は $\Phi$ 不変**、したがって $g_1$ は $Q$-自明。よって $V:=\langle g_1\rangle\cong\mathbf Z/3$ は $\mathfrak F_0^{\rm ab}$ の $Q$-自明な商であり、$\gcd(3,|\Lambda^2Q|)=\gcd(3,2)=1$。**T-B(B3) より等号は破れ、$\ker\widetilde\chi/[\operatorname{GT},\operatorname{GT}]\twoheadrightarrow\mathbf Z/3$。** 実測の指数 3 と一致する。$\blacksquare$

### 5.3 機構の一般化 — 重み 1 と重み 2

> ### 命題 W2(重み)
> $\pi:PB_3/N\twoheadrightarrow H$ を $\Phi$-安定な商($\ker\pi$ が全 $\Phi_{m,f}$ で不変)、$H$ は冪零度 2、$H'=\langle[\bar X,\bar Y]\rangle\cong\mathbf Z/e$ を中心とする。$e\mid 2M$ とすると $\Phi_{m,f}$ は
> * $H^{\rm ab}$ 上で **重み 1**(スカラー $u$)、
> * $H'\cong\gamma_2/\gamma_3$ 方向で **重み 2**(スカラー $u^2$)
>
> で作用する。とくに
> $$u^2\equiv1\ (\mathrm{mod}\ e)\ \ \text{が全ての}\ u\in(\mathbf Z/2M)^\times\ \text{で成立}\iff e\mid24$$
> であり、そのとき $H'$ 方向は **GT-自明**である。

**証明.** class 2 で $[X^a,Y^b]=[X,Y]^{ab}$。$\Phi$ は $\bar X\mapsto\bar X^u$、$\bar Y\mapsto$($\bar Y^u$ の共役)で、中心への共役は自明だから $[\bar X,\bar Y]\mapsto[\bar X,\bar Y]^{u^2}$。後半: $(\mathbf Z/e)^\times$ の指数が $\le2$ $\iff e\mid24$(初等・$e\in\{1,2,3,4,6,8,12,24\}$)。$\blacksquare$

> **反例の作り方(処方)**: **$\mathfrak F_0$ に「重み 2 の層」を持ち込む**。具体的には $K^{(n)}$ 型の窓と **冪零(Heisenberg 型)窓の交叉**をとる。$L=K^{(3)}\cap N_0$ がまさにそれで、重み 1 の $C_3$($G_3$ 由来 = $[\operatorname{GT},\operatorname{GT}]$ になる)と重み 2 の $C_3$($H_3$ 中心由来 = 余不変量として生き残る)が同居している。

---

## 6. 測定表(atlas 横断)

**入力**: `certificates/*.json` のうち shadow 水準 composition table をもつ 18 窓。**$\Phi$ 像は不使用。**
`| EQUAL |` は $\ker\widetilde\chi=[\operatorname{GT},\operatorname{GT}]$ の成否。

| 窓 | $|\operatorname{GT}|$ | $N_{\rm ord}$ | $\varphi(2N)$ | $|\ker\widetilde\chi|$ | $\operatorname{Im}\widetilde\chi$ 全射 | $|[\operatorname{GT},\operatorname{GT}]|$ | **EQUAL** | $|(\mathfrak F_0)_Q|$ |
|---|---|---|---|---|---|---|---|---|
| K3 | 12 | 6 | 4 | 3 | ✓ | 3 | ✅ | 1 |
| K4 | 4 | 4 | 4 | 1 | ✓ | 1 | ✅ | 1 |
| K5 | 40 | 10 | 8 | 5 | ✓ | 5 | ✅ | 1 |
| K6 | 12 | 6 | 4 | 3 | ✓ | 3 | ✅ | 1 |
| K7 | 84 | 14 | 12 | 7 | ✓ | 7 | ✅ | 1 |
| **K8** | 16 | 8 | 8 | 2 | ✓ | 2 | ✅ | **2** |
| K9 | 108 | 18 | 12 | 9 | ✓ | 9 | ✅ | 1 |
| K10 | 40 | 10 | 8 | 5 | ✓ | 5 | ✅ | 1 |
| K11 | 220 | 22 | 20 | 11 | ✓ | 11 | ✅ | 1 |
| K12 | 24 | 12 | 8 | 3 | ✓ | 3 | ✅ | 1 |
| K13 | 312 | 26 | 24 | 13 | ✓ | 13 | ✅ | 1 |
| K14 | 84 | 14 | 12 | 7 | ✓ | 7 | ✅ | 1 |
| K15 | 240 | 30 | 16 | 15 | ✓ | 15 | ✅ | 1 |
| **K16** | 64 | 16 | 16 | 4 | ✓ | 4 | ✅ | **2** |
| K18 | 108 | 18 | 12 | 9 | ✓ | 9 | ✅ | 1 |
| K36 | 216 | 36 | 24 | 9 | ✓ | 9 | ✅ | 1 |
| **L01** | **36** | **6** | **4** | **9** | ✓ | **3** | ❌ **FAIL** | **3** |
| M01($M_5$) | 48 | 30 | 16 | 3 | ✓ | 3 | ✅ | 1 |

**全 18 窓**: $\widetilde\chi$ 全射 18/18 ✓・個数等式 $|\ker|\cdot\varphi(2N)=|\operatorname{GT}|$ 18/18 ✓・$[\operatorname{GT},\operatorname{GT}]\subseteq\ker$ 18/18 ✓・**等号 17/18(唯一の反例 L01)**。
**K4/K8/K16** は 2 冪(T-C(iii))、**K6/K10/K14/K18** は $\alpha=1$(T-C(ii))、**K12/K36** は混合 $\alpha=2$、残りは奇 — **T-C の三分岐がすべて実測で裏取りされている**。

**battery 7 窓**(composition table 未収録・shadow 一覧のみ)での T-A(5) の追加確認:

| 窓 | 定義 | $|\operatorname{GT}|$ | $N_{\rm ord}$($m$ 値集合から確定) | $\varphi(2N)$ | $|\ker\widetilde\chi|$(実測 $m=0$ の個数) | 個数等式 |
|---|---|---|---|---|---|---|
| $N_Q$ | $\pi^{-1}(\ker(F_2\twoheadrightarrow Q_8))$ | 4 | 4 | 4 | 1 | ✓ |
| $M_Q$ | $K^{(3)}\cap N_Q$ | 24 | 12 | 8 | 3 | ✓ |
| $N_2$ | $\pi^{-1}(F_2^4\gamma_3)$ | 4 | 4 | 4 | 1 | ✓ |
| $N_3$ | $\pi^{-1}(F_2^4\gamma_4)$ | 8 | 4 | 4 | 2 | ✓ |
| $M_3$ | $K^{(3)}\cap N_3$ | 48 | 12 | 8 | 6 | ✓ |
| $N_A$ | $\pi^{-1}(\ker(F_2\twoheadrightarrow A_5))$ | 20 | 5 | 4 | 5 | ✓ |
| $M_{A_5}$ | $N_A\cap N_5$ | 20 | 5 | 4 | 5 | ✓ |

**合計 25 窓で個数等式の不一致ゼロ。**

**atlas 14 対象の決着**:

| 判定 | 窓 | 根拠 |
|---|---|---|
| **等号成立** | $K^{(3)},K^{(5)},K^{(7)},K^{(9)},K^{(11)}$ | T-C(証明)+ 合成表実測 |
| | $M_5$ | 合成表実測 |
| | $N_Q,N_2$ | $|\mathfrak F_0|=1$(補題 P 系) |
| | $N_A,M_{A_5}$ | $|\mathfrak F_0|=5$ 素数 + I-26 census の導来長 2(非可換)→ **補題 P** |
| | $M_Q$ | $|\mathfrak F_0|=3$ 素数 + $\Phi$ 像(位数 12)が非可換 ⟹ $\operatorname{GT}(M_Q)$ 非可換 → **補題 P** |
| **等号不成立** | **$L$** | T-D(実測 + a priori 証明) |
| **UNKNOWN** | $N_3$、$M_3$ | 合成表未収録・補題 P が届かない |

> **註**: $M_Q$・$N_A$・$M_{A_5}$ は補題 P で**合成表なしに確定した**(非可換性は I-26 census の $\Phi$ 像から従う — $\Phi$ 像が非可換なら元の群も非可換、という**一方向だけ**の使い方なので C2F の罠にかからない)。

**UNKNOWN 2 件の見通し**:
* **$N_3$**: $\mathfrak F_0\cong C_2$(素数位数)。補題 P より **等号 $\iff\operatorname{GT}(N_3)$(位数 8)が非可換**。ただし $\Phi$ 像(位数 4)は可換なので、この方向からは決まらない — **shadow 水準で 1 ビット測るだけ**で決着。$\ker\Phi$ は位数 2 の正規部分群 $=$ 中心なので $\operatorname{GT}(N_3)$ は class $\le2$、$C_2\times C_4$ か $D_4/Q_8$ かの二択。
* **$M_3$**: $|\mathfrak F_0|=6$(非素数 — 反例の資格がある窓)。$Q=(\mathbf Z/24)^\times\cong(\mathbf Z/2)^3$、$\Lambda^2Q$ の位数 8。3-部分は $M_Q$ と同型の議論で潰れる見込み、2-部分は $N_3$ と同じ transgression 勝負。**$\mathfrak F_0$ の 2-部分が生き残れば 2 例目の反例**。

---

## 7. 壁ソルバーへの帰結(委嘱の「帰結の明記」)

現行 `provenance/registered/universe_wall_v1.md` v1.1 の「理論フィルタ」節を、次のとおり**強化かつ訂正**できる。

### 7.1 無傷なもの(自由な向き)

$[\operatorname{GT},\operatorname{GT}]\subseteq\ker\widetilde\chi$ は**無条件の定理**なので:
$$\textbf{TIER-0}:\quad \ker\widetilde\chi\ \text{可換}\ \Longrightarrow\ [\operatorname{GT},\operatorname{GT}]\ \text{可換}\ \Longrightarrow\ \operatorname{GT}(N)\ \text{metabelian}$$
は**そのまま有効**。v1.1 の記述に変更不要。

### 7.2 訂正 — FAIL-2 の文言

v1.1 は「逆は主張しない(**FAIL-2**: $\ker\widetilde\chi=[\operatorname{GT},\operatorname{GT}]$ の等号は**未証明**)」と書く。これは:
> **未証明ではなく、一般には偽である。反例 $L$ は登録 atlas の中にある**(T-D)。**dihedral 族($K^{(n)}$ 全 $n$)では定理**(T-C)。

に改めるべきである。**TIER-1 から「非 metabelian」への昇格は、その窓での等号を別途証明しない限り不正**である(委嘱文の「等号が立つクラスでは…昇格」は正しいが、**クラスの同定が必須**)。

### 7.3 新設提案 — TIER-1.5(等号を要さない非 metabelian 判定)

$\mathfrak F_0\le\operatorname{GT}(N)$ から $[\mathfrak F_0,\mathfrak F_0]\subseteq[\operatorname{GT},\operatorname{GT}]$。ゆえに:

> **命題 TIER-1.5.** $\ker\widetilde\chi$ の**導来長が 3 以上**(同値: $[\mathfrak F_0,\mathfrak F_0]$ が非可換)なら $[\operatorname{GT},\operatorname{GT}]$ は非可換、すなわち $\operatorname{GT}(N)$ は **非 metabelian**。**等号を一切要さない。**

これは現行 TIER-1(「$\ker$ 非可換 = 必要条件通過」止まり)と TIER-2 の間を埋め、**負の結果しか出ない可能性のある掃引に、等号仮定なしの陽性判定路を与える**。実装コストは $\ker\widetilde\chi$ の導来列を取るだけ(既に列挙している部分群)。

### 7.4 等号証明書(窓ごと・安価)

T-A(5) より
$$\boxed{\ \ker\widetilde\chi=[\operatorname{GT},\operatorname{GT}]\iff \bigl|\operatorname{GT}(N)^{\rm ab}\bigr|=\varphi(2N_{\rm ord})\ }$$
なので、等号は **$|\operatorname{GT}^{\rm ab}|$ を 1 個計算するだけ**で確定する(合成表があれば $O(|\operatorname{GT}|^2)$)。掃引の証明書 schema `wall-cert/v1` に次の 3 欄を追加することを提案する:

1. `abelianization_order`($=|\operatorname{GT}(N)^{\rm ab}|$)
2. `phi_2Nord`($=\varphi(2N_{\rm ord})$ — 既記録の $N_{\rm ord}$ から無料)
3. `kerchi_equals_derived`(上 2 者の一致 / `UNKNOWN`)

**さらに安い前段**: 補題 P(§3.1)により、$|\mathfrak F_0|=|\operatorname{GT}|/\varphi(2N_{\rm ord})$ が**素数または 1** の窓は `abelianization_order` を計算せずに決着する(非可換性は TIER-0 判定の副産物)。合成表を要するのは $|\mathfrak F_0|$ が非素数の窓だけ。

さらに **fail-closed assert として T-A(5)** — `|ker_chi| * phi_2Nord == |GT|` — を入れること(§2 註 3)。**$\Phi$ 潰れ型の系統誤りを掃引の内部から検出する**。

### 7.5 反例の探し場所(委嘱の主要設問への回答)

T-B/W2 から、**等号が破れる窓の同定はほぼ機械的**になる:

| 優先度 | 探し場所 | 根拠 |
|---|---|---|
| **0(除外)** | **$|\mathfrak F_0|=|\operatorname{GT}|/\varphi(2N_{\rm ord})$ が素数または 1 の窓は反例になりえない**(非可換なら等号成立・可換なら $\operatorname{GT}$ 自体が可換で $\mathfrak F_0=1$)。**まずこれで篩う** | 補題 P。$N_{\rm ord}$ と $|\operatorname{GT}|$ だけで判定・合成表不要 |
| **1** | **$N_{\rm ord}$ が奇素数冪($M\in\{p^k\}$)または $M\in\{1,2\}$ の窓** — このとき $Q=(\mathbf Z/2M)^\times$ は**巡回**で $\Lambda^2Q=0$。ゆえに **$(\mathfrak F_0)_Q\ne0$ なら必ず反例**(T-B(B2))。判定は余不変量 1 個 | T-B(B2)。$N_{\rm ord}$ は掃引が全窓で既に記録 |
| **2** | **$|\mathfrak F_0|$ が偶数で $\mathfrak F_0$ に位数 2 の $Q$-自明成分がある窓**($\mathbf Z/2$ への作用は常に自明) | $N_3$ 型。$\Lambda^2Q$ の 2-部分との綱引きになる |
| **3** | **$K^{(n)}$ と冪零窓(Heisenberg・$\gamma_3,\gamma_4$ 型)の交叉窓** — 重み 2 の層が入る | T-E(W2)。$L$ がこの型 |
| **4** | **$\Lambda^2Q$ の位数と $|(\mathfrak F_0)_Q|$ が互いに素**になる窓(一般形) | T-B(B3) |

実務: 掃引の各窓で **(a) $|\mathfrak F_0|=|\operatorname{GT}|/\varphi(2N_{\rm ord})$(無料)、(b) $\Lambda^2((\mathbf Z/2N_{\rm ord})^\times)$ の位数($N_{\rm ord}$ の表引き)** を並べるだけで、優先度 1・4 の候補が抽出できる。

---

## 8. 自己監査(falsifier 前)

| # | リスク | 判定 |
|---|---|---|
| R-1 | **$L$ が本当に $\mathrm{NFI}_{PB_3}(B_3)$ の窓か**($B_3$-正規性・$L\le PB_3$) | △ **atlas 登録を継承した仮定**。証明書は $[B_3:L]=17496$、$c\in L$、`crosscheck` 検収済だが、$B_3$-正規性の独立再検証は本稿では行っていない。**これが偽なら T-D は消える**(T-B/T-C/T-A は無傷)。→ 【KE-a】 |
| R-2 | 合成表の向き(左右)を取り違えていないか | ○ **結論に無関係**。$\ker\widetilde\chi$ も $[G,G]$ も $G$ と $G^{\rm op}$ で同一($x\mapsto x^{-1}$ が同型)。加えて (3.53) の第一成分は可換なので第一成分からは向きが決まらない — 意図的に向き非依存な量だけを測った |
| R-3 | 合成表が「本当に GT-shadow の群」か(表が偽物なら全部無意味) | ○ 群公理 3 種 + **(3.53) 第一成分の再現**を fail-closed assert。加えて node 独立レーンの検収済(§5.1) |
| R-4 | T-A(4) が (AR)(Ihara 準同型の存在と形)に依存 | △ **依存を明示**。ただし 25 窓で全射性を独立実測しており、(AR) が偽でも実測範囲では T-A(5) は成立している。**族的主張としては (AR) 必須** |
| R-5 | T-C が Thm 4.6 (4.23)(4.24) の**引用**に依存(再証明していない) | △ **明示**。ただし K3–K36 の 16 窓で $|\operatorname{GT}^{\rm ab}|=\varphi(2N_{\rm ord})$ を独立実測しており、引用が壊れていれば実測が破れるはず |
| R-6 | $H_2(Q)=\Lambda^2Q$ の適用範囲 | ○ 有限アーベル群で標準。$Q=(\mathbf Z/2M)^\times$ は有限アーベル ✓ |
| R-7 | 「$\mathfrak F_0$ の余不変量 $\ne0$ ⟹ 反例」と早合点する危険 | ○ **本稿自身が反証**(K8/K16)。T-B の coker を必ず見ること — §3 註で明記 |
| R-8 | T-D を「dihedral 予想に影響」と読む危険 | ○ **影響しない**。$L$ は dihedral 塔の窓ではない($K^{(n)}$ 族は T-C で等号成立)。影響するのは**壁キャンペーンの推論規則のみ** |
| R-9 | UNKNOWN 3 件($M_Q,N_3,M_3$)の「予測」を結果と混同 | ○ **予測と明記**。決着には合成表(shadow 水準)が要る |
| R-10 | $e\mid24$ 判定で $e\mid2M$ を暗黙に使う | ○ W2 の仮定に明記($L$ では $e=3\mid12$ ✓) |

---

## 9. 未閉鎖項・次の一手

* 【KE-a】**$L$ の $B_3$-正規性の独立確認**(T-D の唯一の外部依存)。GAP で $\langle L^{B_3}\rangle=L$ を直接検査すれば数秒。**最優先**。
* 【KE-b】**UNKNOWN 2 件の決着**: $N_3$・$M_3$ の **shadow 水準合成表**の生成(既存 battery スクリプトの (3.53) 合成部を証明書に書き出すだけ)。とくに **$N_3$ は「位数 8 の群が可換か」の 1 ビット**で決まる — 最安。$M_3$ は $|\mathfrak F_0|=6$ で**反例の資格がある**ので優先度が高い。
* 【KE-c】**$\Lambda^2((\mathbf Z/2M)^\times)$ の表**($M\le$ band 上限)を掃引の前処理として生成 → 優先度 1・4 の候補窓の自動抽出。
* 【KE-d】**W2 の逆**: $\mathfrak F_0$ の「重み分解」を一般に計算する装置があれば、等号は**窓を見る前に**判定できる。→ 下記【文献要請】。
* 【KE-e】**I-26(metabelian の壁)への接続**: T-A(5)+T-C は「$\operatorname{GT}(K^{(n)})^{\rm ab}\cong(\mathbf Z/2M)^\times$」を全 $n$ で確定させるので、I-26 の「経由定理」($\operatorname{Ih}$ は二段可解商を経由)の第一段が族的に閉じる。**ただし $L$ で $\operatorname{GT}^{\rm ab}$ が $(\mathbf Z/2M)^\times$ より真に大きい**ので、「アーベル化は円分で尽きる」という描像は **dihedral 族に固有**である — I-26 の物語はこの限定つきで書くべき。
* 【KE-f】本稿は紙上(paper-proof candidate)+ 既存 cross-checked 証明書の再解析。**Lean 検証ではない**。

> ### 【文献要請】
> **困難**: 等号の成否は「$\mathfrak F_0$ の各層に $\Phi_{m,f}$ が重み $u^{w}$ のどれで作用するか」で決まる(§5.3)。重み 1 の層は $[\operatorname{GT},\operatorname{GT}]$ に吸収され、重み 2(以上)で $u^{w}\equiv1$ となる層が余不変量として残る。現状これを**窓ごとに手で読む**しかない。
> **欲しい結果の型**: 「自由群 $F_2$ の**降中心列 $\gamma_k/\gamma_{k+1}$(自由リー環の重み $k$ 部分)**に対し、生成元のスカラー倍 $x\mapsto x^u,\ y\mapsto y^u$(と共役)から誘導される作用が **$u^k$ 倍**であること、およびその**有限冪零商での定式化**(Magnus 埋め込み・Fox 微分・$\mathbf F_p$ 係数リー環の重み分解)」。より一般に、$\widehat{\mathrm{GT}}$ の**深さ(depth)フィルトレーション**と円分指標の重みの対応。
> **当て**: Ihara・Deligne–Terasoma・Hain–Matsumoto の「mixed Tate / weight filtration on $\pi_1$」系、あるいは Magnus 展開と自由リー環の標準教科書。**GT 文献のど真ん中にありそうだが、我々の正典 2 本(2401/2405)は有限 shadow の代数しか扱っていないため未装備**である。
> **使い道**: 窓の nilpotency データ(掃引が既に持つ)から**等号の成否を計算で予言**できるようになり、§7.5 の「探し場所」が「探し当て」に変わる。
