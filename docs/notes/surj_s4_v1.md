# S4 = PSL(2,8) 窓($k=9$)での SURJ 押し込み — 族機械の非 dihedral 初適用

**状態札: candidate(裁定前・未 commit・単系統・Sol 監査前)**
起草: Claude(数学者レイヤー・Opus 5)/ 2026-07-30
設問: 司令塔委嘱(裁定 217)。`docs/notes/surj_d4_t1_v1.md` SD-5(転送先の同定)の続編。同梱 2 点【SD-a】【SD-c】を §6・§7 に。

**依拠(正典・repo 内のみ・外部文献ゼロ)**
- S4 の窓データ: `docs/week3-PSL封印計算_opus_v1.md` §5.4(封印 JSON)・§4.1(case A の正規化群)/ `docs/week4-E2作戦_v1.md`(isolated 表)/ 台帳 **W3-6**(封印予測 7/7・二系統)・**W3-7**(七窓統一定理)
- `docs/week4-BFC攻略_opus_v2.md`(BFC v2.15)§3 (W1)–(W5)・§6 定理 B-4・§7 補題 B-5/B-5$^{\rm u}$・§8 補題 B-6・§9 定理 B-7
- `docs/week4-K3飽和_opus_v3.md` §5.2.2 = **定理 $R^{\rm cyc}_{\rm formal}$**(W3-13)/ `docs/week4-A5算術飽和_v4.md`(定理 A₅ = W3-8・§1.4 = (CAL)・§3.5 = $u$ 抽出の実例)
- `docs/notes/phifam_v1.md` §2(**Φ の共変性 — 本稿で窓非依存に持ち上げる**)/ `docs/notes/surj_d4_t1_v1.md` §2(補題 SURJ-Split)§5.2
- `search/kerchi-judge.g`(**§6【SD-a】の一次資料**)/ `docs/notes/wcp5d_resolution_v1.md` GAP-4
- 正典 arXiv 2405.11725 (1.5)・`docs/week1-定義ノート.md` §2 (3.49)(3.53)・§3(settled/isolated の定義)

> ## 封印遵守
> **$u_{S4}$ の値には触れていない**(§5 は測定**計画**まで)。$K^{(5)}$ 非接触。使用した公開値は $A_5$ の $u^{-1}=-2$ と $K^{(3)}$ の $u=-4$ のみで、いずれも**先例の形**を示すためにしか使わない。

---

## 0. 判定(先に 8 行)

$$\boxed{\ \textbf{前件は揃う。1 ビット帰着は成立する。ただし procedural gap 1 件(}(Z_{18}\text{-link})\textbf{)と検分要請 1 件(isolated の意味論)つき。}\ }$$

1. **(W1)–(W5)+(CAL) はすべて S4 で成立**(§3)。うち **(W3)(W4)(W5)(W5$^{\mathbb Q}$) と $\mathfrak F_0\cong C_9$ は本稿で紙上証明**、(W2) 算術半は窓非依存(SURJ-Split)、(CAL) は窓非依存、**(W1) のみ測定依存**。
2. **★ 副産物**: $\mathfrak F_0\cong C_9$ と $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X\rangle)$ を、**命題 K5-1 の非 dihedral 版**として紙上で得た(§3.3 補題 F0)。論法は $K^{(n)}$ 族の座標を一切使わない。
3. **(6′) も成立**($\rho_0$ 忠実・$\rho_0(\mathfrak F_0)=\tau(\mu_M[e])$、$M=e=9$)(§3.7)。
4. ⟹ **$R^{\rm cyc}_{\rm formal}$ の帰結が書き下せる**:
 $$\boxed{\ \mathrm{Ih}_{S4}\ \text{全射}\iff\mathrm{ord}\bigl([u^{-1}]_9\bigr)=9\iff u^{-1}\notin K^{\times3},\qquad K=\mathbf Q(\zeta_{18})=\mathbf Q(\zeta_9),}$$
 固定体は $K\bigl((u^{-1})^{1/9}\bigr)$(9 次巡回)。**1 ビット帰着は成立**(§4)。
5. **★ procedural gap**: **$(Z_{18}$-link$)$ が per-window で未供給**(`Z-norm-seal/v1` の window inventory に S4 の行が無い)。橋 B-7 の $b_{\rm op}=1$ はこれに相対的なので、**現状 S4 は $K^{(3)}/A_5$ と同じ `pending` 身分**(§3.8)。数学ではなく手続き。
6. **★【SD-a】= NO(重大)**: 壁窓証明書の `settled_fail_count = 0` は **isolated を意味しない**。judge の実装ではこれは **$T_{m,f}$ が well-defined な準同型か**の検査(裁定 169 の KJ-1 修理)であり、judge のソース自身が「**genuine isolated-ness は本キャンペーンでどこでも独立検証されていない**」と明記している(既出 GAP: `wcp5d_resolution_v1.md` **GAP-4**)。⟹ **壁窓の (W1) は未確立**(§6)。
7. **★【SD-c】= 測定完了・$a=+1$**: t=1 壁窓で $\Phi|_{\mathfrak F_0}:\mathfrak F_0\to\mathrm{inn}(\langle X\rangle)$ が**全単射**であることを GAP で実測($j$-値が $\mathbf Z/9$ を尽くす)。⟹ 捻れ指数 **$a=+1$**、すなわち核方向の指標は**真に Kummer 型**(§7)。付随して $\lvert\mathfrak F_0\rvert=9$ を**judge とは別実装で独立再現**。
8. **測定計画**(委嘱 2 後半): 次数 9・$0$ 上全分岐の dessin の Belyi 写像から $[u]_9$ を読む。$A_5$ v4 §3.5 の手順が**そのまま骨格になる**(§5)。

---

## 1. 窓データ(転記)

`docs/week3-PSL封印計算_opus_v1.md` §5.4(封印 JSON・段 S4)より:

| 項目 | 値 |
|---|---|
| 群 | $\mathrm{PSL}(2,8)$、$q=8$、$\lvert P\rvert=504$ |
| marking | $S=\begin{pmatrix}1&0\\1&1\end{pmatrix}$、$T=\begin{pmatrix}4&3\\1&5\end{pmatrix}$、$\det T=1$、trace 三つ組 $[0,1,2]$、$w=T^{-1}S$、$\mathrm{ord}(w)=9$($\mathbf F_8$ の整数符号 $x=2,\ x+1=3,\ x^2=4,\ x^2+1=5$) |
| case | `A_split_inner`、`three_divides_k: true` |
| $N_{\rm ord}$ | **9** |
| charming set | $\{0,2,3,5,6,8\}$(6 個) |
| $[\mathrm{PB}_3:N]$ | 504、$B_3$ 点数 3024、対象数 1 |
| $c\in N$ | **true** |
| `gt_count` | **54**、`shadow_total` 54、`settled_count` 54、`isolated` **true** |
| `n_m_uniform` | **9** |
| `phi_image` | $N_{\mathrm{P\Gamma L}(2,8)}(\langle X\rangle)=\mathrm{Hol}(\mathbf Z/9)$、`phi_bijective: true` |
| staged counts | $2640+330+54=3024$ ✓(排他・悉皆) |

**水準の勘定**(`surj_d4_t1_v1.md` §1 と同一・検算済): $M:=\mathrm{ord}(X)=9$、$2M=2N_{\rm ord}=18$、$\varphi(18)=6$、$K:=\mathbf Q(\zeta_{2M})=\mathbf Q(\zeta_{18})=\mathbf Q(\zeta_9)$、$[K:\mathbf Q]=6$、$e:=\lvert\mathfrak F_0\rvert=54/6=9$。**$M=e=9$。**

$\{2m+1\bmod18:m\in\{0,2,3,5,6,8\}\}=\{1,5,7,11,13,17\}=(\mathbf Z/18)^\times$ ✓ — **$\tilde\chi$ は charming 層と $(\mathbf Z/18)^\times$ の間の全単射**。

---

## 2. 一般の道具 — Φ の共変性を窓非依存に持ち上げる

以後くり返し使うので先に置く。

> ### 補題 Φ-univ(窓非依存)
> 任意の charming target $N$ と $[m_i,f_i]\in\mathrm{GT}(N)$ について、$\Phi_{m,f}\in\mathrm{End}(P)$ を
> $$\Phi_{m,f}(X)=X^{u}\ (u=2m+1),\qquad \Phi_{m,f}(Y)=F^{-1}Y^{u}F\quad(F=f\ \text{の}\ P\ \text{での値})$$
> で定めると **$\Phi$ は共変な準同型**である: $\Phi_{[m_1,f_1]\circ[m_2,f_2]}=\Phi_{[m_1,f_1]}\circ\Phi_{[m_2,f_2]}$。

**証明.** `phifam_v1.md` §2 の計算を逐語に読む:
$$T_1(T_2(y))=T_1(f_2^{-1}y^{u_2}f_2)=E_1(f_2)^{-1}\bigl(f_1^{-1}y^{u_1}f_1\bigr)^{u_2}E_1(f_2)=\bigl(f_1E_1(f_2)\bigr)^{-1}y^{u_1u_2}\bigl(f_1E_1(f_2)\bigr),$$
$x$ 上で $T_1(T_2(x))=x^{u_1u_2}$。(3.49) より $u_1u_2=2(2m_1m_2+m_1+m_2)+1$、第二成分 $f_1E_{m_1,f_1}(f_2)$ は合成則 (3.53) そのもの。$\blacksquare$

> **★ 射程の申告**: `phifam_v1.md` は「$n\ge3$ 奇・$G_n=A\rtimes Q$(ODD-H 座標)」という枠で書かれているが、**§2 の共変性の証明は座標も $n$ の奇偶も一切使っていない**($E_{m,f}$ の定義・(3.53)・(3.49) のみ)。したがって**任意の窓へ持ち上がる**。これは本稿の寄与(**§8-S4-2**)であり、`phifam` の再証明ではない。
> **⚠ これは §5.4 の【GAP-06a】(「(3.53) の合成法則が $\Phi$ と両立することは $A_5$ でしか確認していない」)を紙で閉じる。** 実装確認を待つ必要はない。

---

## 3. 前件の逐項確認(委嘱 1)

### 3.1 (W3) — $N_P(H)=H$

> **補題 W3-S4.** $P=\mathrm{PSL}(2,8)$、$H:=$ Borel(点安定化群、位数 56)とすると $N_P(H)=H$。

**証明.** $\lvert P\rvert=504=8\cdot9\cdot7$、$\mathbf P^1(\mathbf F_8)$ は 9 点で $P$ は可移、点安定化群は $B=\mathbf F_8\rtimes C_7$(位数 56)。$B$ は $\mathrm{Syl}_2(P)$($=\mathbf F_8$、位数 8)の正規化群である。$N_P(B)\supsetneq B$ とすると $N_P(B)$ の位数は 56 の真の倍数で 504 の約数、すなわち 168 か 504。$[P:N_P(B)]\in\{1,3\}$ だが、$P$ 単純で $\lvert P\rvert>3!$ ゆえ指数 3 の部分群は存在しない(剰余類作用が $P\hookrightarrow S_3$ を与え矛盾)。指数 1 なら $B\trianglelefteq P$ で単純性に反する。$\blacksquare$

### 3.2 (W4) — 全分岐・$[P:H]=M$

> **補題 W4-S4.** $[P:H]=9=M$ であり、$\langle X\rangle$($X$ は位数 9)は $P/H$ 上**単純推移的**。

**証明.** $[P:H]=504/56=9=M$ ✓。$\lvert P\rvert=8\cdot9\cdot7$ より位数 9 の巡回部分群は $q+1=9$ の**非分裂トーラス**である。非分裂トーラスの非単位元は $\mathbf P^1(\mathbf F_8)$ 上に固定点をもたない(固有値が $\mathbf F_8$ に無い)。位数 3 の元についても同様: $\mathbf F_8^\times$ は位数 7 で 3 乗根 $\ne1$ を含まず、1 の原始 3 乗根は $\mathbf F_4\setminus\mathbf F_2$ にあり $\mathbf F_4\cap\mathbf F_8=\mathbf F_2$ ゆえ固有値は $\mathbf F_8$ に無い。よって $\langle X\rangle$ は 9 点上**自由**に作用し、軌道長 9 $=$ 点の個数 ⟹ **単純推移** ✓。$\blacksquare$

> **★ ここが壁窓との分水嶺である。** `surj_d4_t1_v1.md` 命題 TAIL-OBS: 壁窓は $P\cong A_n$・$M=9<n$ で指数 $M$ の部分群が**存在しない**。S4 は $P=\mathrm{PSL}(2,8)$・$M=9=\lvert\mathbf P^1(\mathbf F_8)\rvert$ で**ちょうど存在する**。

### 3.3 $\mathfrak F_0\cong C_9$ と $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X\rangle)$ — 命題 K5-1 の非 dihedral 版

これは (W2) の内容の一部であり、(6′) と (W5) の土台でもある。

> ### 補題 F0(窓非依存の形)
> $\Phi$ が単射で、$C_{\mathrm{Aut}(P)}(X)=\langle X\rangle$ かつ $\lvert\mathfrak F_0\rvert=\lvert\langle X\rangle\rvert$ ならば
> $$\Phi\bigl(\mathfrak F_0\bigr)=\mathrm{inn}\bigl(\langle X\rangle\bigr)\ \cong\ \langle X\rangle,\qquad\text{とくに }\mathfrak F_0\ \text{は巡回}.$$

**証明.** $[0,f]\in\mathfrak F_0$ は $u=2\cdot0+1=1$ ゆえ $\Phi_{0,f}(X)=X^1=X$、すなわち $\Phi_{0,f}\in C_{\mathrm{Aut}(P)}(X)=\langle X\rangle$(ここで $\langle X\rangle\le\mathrm{Inn}(P)$ と同一視 — $C_{\mathrm{Aut}(P)}(X)=\langle X\rangle$ の右辺は $\mathrm{inn}(\langle X\rangle)$ の意味)。補題 Φ-univ より $\Phi$ は準同型なので $\Phi(\mathfrak F_0)\le\mathrm{inn}(\langle X\rangle)$ は部分群。$\Phi$ 単射と位数一致から等号、かつ $\mathfrak F_0\cong\mathrm{inn}(\langle X\rangle)\cong\langle X\rangle$。$\blacksquare$

**S4 への適用**: $C_{\mathrm{Aut}(P)}(X)=\langle X\rangle$(位数 9)は `週3-PSL封印計算` §4.1 が「各窓で $\lvert N_{\mathrm{Aut}(G)}(\langle X\rangle)\rvert=k\varphi(k)$、$C_{\mathrm{Aut}(G)}(X)=\langle X\rangle$(位数 $k$)、$N/C\twoheadrightarrow(\mathbf Z/k)^\times$ 全射」として §7 で確認済と記す。$\Phi$ 単射は `phi_bijective: true`。$\lvert\mathfrak F_0\rvert=$ `n_m_uniform` $=9=\lvert\langle X\rangle\rvert$ ✓。

$$\Longrightarrow\ \boxed{\ \mathfrak F_0\cong C_9,\qquad \Phi(\mathfrak F_0)=\mathrm{inn}(\langle X\rangle)\subseteq\mathrm{Inn}(P).\ }$$

> **★ これは命題 K5-1($\Phi_{0,k}=\mathrm{inn}(X^{-2k})$・W3-15①・$K^{(n)}$ 族限定)の、族の外での初の対応物である。** しかも補題 F0 の証明は $K^{(n)}$ の座標を使わない。**$C_{\mathrm{Aut}(P)}(X)=\langle X\rangle$ と $\lvert\mathfrak F_0\rvert=\mathrm{ord}(X)$ の 2 条件だけが本質**であることが分かった(§8-S4-3)。

### 3.4 (W2) — 完全列と算術半

**群論半**: $\tilde\chi:\mathrm{GT}(N)\to(\mathbf Z/18)^\times$ は補題 SURJ-Split (a)(窓非依存)より well-defined な準同型。charming 層と $(\mathbf Z/18)^\times$ の全単射(§1)より**全射**、核は $m=0$ 層 $=\mathfrak F_0$、位数 9(`n_m_uniform`)。§3.3 より $\mathfrak F_0\cong C_9$。
$$\boxed{\ 1\to\mathfrak F_0\ (\cong C_9)\to\mathrm{GT}(N)\xrightarrow{\ \tilde\chi\ }(\mathbf Z/18)^\times\to1\ \text{完全}\ }$$
位数勘定 $9\cdot6=54=$ `gt_count` ✓。

**算術半** $\tilde\chi\circ\mathrm{Ih}_N=\chi_{18}$: **補題 SURJ-Split (b)**(`surj_d4_t1_v1.md` §2.1)より**窓非依存に成立**。正典 (1.5) と水準補題だけを使い、$K^{(n)}$ 族に固有の入力はゼロ。✅

### 3.5 (W1) — isolated

`isolated: true`(封印 JSON)。`week4-E2作戦_v1.md` の isolated 表の S4 行の justification は逐語「全 54 shadow が settled(6 層 × 各 9)ゆえ $\mathrm{GT}(N)=\mathrm{GTSh}(N,N)$;case A の正規化群 $\mathrm{Hol}(C_9)$(位数 54)と一致」。これは定義ノート §3 の **isolated の定義そのもの**(全 shadow が settled ⟹ $\mathrm{GT}(N)=\mathrm{GTSh}(N,N)$)に一致する。

isolated ⟹ (W1) は `c2c4_closure_v1.md` §1.2 補題 W1-a(**窓非依存**: $\ker(T_{m_\gamma,f_\gamma})=(\alpha^{\rm Ih}_\gamma)^{-1}(\bar N)$ と settled から $\alpha^{\rm Ih}_\gamma(\bar N)=\bar N$)+ (CAL) で $\alpha^{\rm std}_\gamma(\bar N)=\bar N$。✅

> **⚠ ここだけ測定依存である**(**$K^{(n)}$ 族との最大の差**)。族側では isolated は正典 **Thm 4.3**(「For every $n\ge3$ … $K^{(n)}$ is an isolated object」)という**定理**だった。S4 では **GAP 実測**(W3-6 で二系統・封印 7/7 一致)である。
> **⚠⚠ さらに §6【SD-a】の教訓を適用せよ**: 別実装(kerchi-judge)では `settled` という語が**別の意味**(well-definedness)に使われていた。**PSL 実装の `settled_count` が定義ノートの settled($\ker T_{m,f}=N$)であることを、PSL スクリプトのソースで確認すること**を検分要請とする(§9【S4-a】)。上の justification 文は正しい読みを示唆するが、**私はソースを読んでいない**。

### 3.6 (W5) と (W5$^{\mathbb Q}$)

> **補題 W5-S4.** $\Lambda:=\{H\ \text{の}\ P\text{-共役}\}$ は $\Phi(\mathfrak F_0)$-安定であり、さらに $\Phi(\mathrm{GT}(N))$-安定でもある。

**証明.** **(W5)**: §3.3 より $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X\rangle)\subseteq\mathrm{Inn}(P)$。$\Lambda$ は部分群の $P$-共役類**全体**なので $\mathrm{Inn}(P)$-安定 ✓(Sol 便 73 (1.13)(1.14) の論法と同型 — そこでも「内部自己同型は全ての $P$-共役類を保つ」)。
**(W5$^{\mathbb Q}$)**: $\Lambda$ は $\mathrm{Aut}(P)$-安定であることを示せば十分。$H'\le P$ が指数 9 なら、$H'\le K\le P$ に対し $[P:K]\in\{1,3,9\}$ で 3 は単純性から不可、ゆえに $H'$ は**極大**。位数 56 の極大部分群は Borel($=\mathrm{Syl}_2$ の正規化群)に限る。Borel は Sylow 2-部分群と 1:1 対応し、Sylow の定理より**単一の $P$-共役類**をなす。ゆえに「指数 9 の部分群」という**群論的性質だけで $\Lambda$ が特徴づけられる**ので、任意の $\sigma\in\mathrm{Aut}(P)$ は $\Lambda$ を保つ ✓。$\blacksquare$

> **★ (W5$^{\mathbb Q}$) まで出たので、定理 B-4(b) により $\mathbf Q$-モデルが取れる**(橋には $K$-モデルで足りるので必須ではないが、$A_5$/$K^{(3)}$ と同じ強さ)。

### 3.7 (6′)$R^{\rm cyc}_{\rm formal}$ 側の前件

(6′) は 2 節からなる(BFC §3 の対応表): 第 1 節「$\Lambda$ が $\Phi(\mathfrak F_0)$-安定」$=$ **(W5)** ✅(§3.6)。第 2 節「$\rho_0$ 忠実」:

> **補題 6′-S4.** $\rho_0:\mathfrak F_0\to\mathrm{Sym}(\Lambda)$ は忠実で、$\rho_0(\mathfrak F_0)=\tau(\mu_M[e])$。

**証明.** (W4) と命題 B-2 (B2-bij)((W3) から $P/H\xrightarrow{\sim}\Lambda$、$gH\mapsto gHg^{-1}$)より $\Lambda\cong P/H$(9 点)で、$\tau(\zeta_M)$ は左移動 $L_X$ に対応する。§3.3 より $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X\rangle)$、その $\Lambda$ 上の作用は $\mathrm{inn}(X^j):H'\mapsto X^jH'X^{-j}$、すなわち $P/H$ の左移動 $L_{X^j}$。$\langle X\rangle$ は $P/H$ 上**単純推移**(補題 W4-S4)なので $L_{X^j}=\mathrm{id}\iff j\equiv0$ ⟹ **忠実** ✓。像は $\{L_{X^j}\}=\tau(\mu_9)$ で、$e=M=9$ ゆえ $\mu_M[e]=\mu_9[9]=\mu_9$ ⟹ $\rho_0(\mathfrak F_0)=\tau(\mu_M[e])$ ✓。$\blacksquare$

**盲点定理(K5-2)のチェック**: $\ker(\Phi|_{\mathfrak F_0})=1$(§3.3)ゆえ **SCHEMA-OUT ではない** ✅。

### 3.8 枠組前件と procedural gap

| 前件 | S4 での status |
|---|---|
| (CAL) | ✅ **窓非依存に証明済**($A_5$ v4 §1.4・`c2c4_closure_v1.md` I5) |
| (TB1)(TB2)(TB3) | retained framework(2026-07-28 裁可) |
| exact (TB4) | `Z-norm-seal/v1` が **global** に供給(W3-21) |
| **$(Z_{18}$-link$)$** | ⚠ **per-window・S4 は inventory に行が無い**(W3-21: 「$K^{(5)}$ 供給済・$K^{(3)}/A_5$ は pending」— S4 は**未登録**)。⟹ 補題 B-6($b_{\rm op}=1$)は S4 では **not_assessed** |
| A3 | 未閉(別線・全窓共通) |

> **⚠ これは数学ではなく手続きである。** $(Z_{18}$-link$)$ は「$\zeta_{18}^{\rm TB2}=\zeta_{18}^{\rm Rule1}$」という命名規約の一致条項で、S4 の window inventory 行を立てて migration/compatibility certificate を書けば供給される。**$K^{(3)}/A_5$ も同じ `pending` なので、S4 が特に劣るわけではない**(定理 A₅(W3-8)・定理 K3(W3-11)はこの条項の確立前に成立しており、W3-21 で遡及的に相対化された)。

### 3.9 前件表(まとめ)

| # | S4 | 供給 | 型 |
|---|---|---|---|
| (W1) | ✅ | isolated 実測(W3-6 二系統)+ 補題 W1-a + (CAL) | **測定依存**(要検分【S4-a】) |
| (W2) 群 | ✅ | §3.4(SURJ-Split (a) + charming 全単射 + §3.3) | **紙** |
| (W2) 算術 | ✅ | 補題 SURJ-Split (b) | **紙・窓非依存** |
| (W3) | ✅ | 補題 W3-S4 | **紙** |
| (W4) | ✅ | 補題 W4-S4 | **紙** |
| (W5) | ✅ | 補題 W5-S4 | **紙** |
| (W5$^{\mathbb Q}$) | ✅ | 補題 W5-S4 | **紙**(ボーナス) |
| (6′) | ✅ | (W5) + 補題 6′-S4 | **紙** |
| (CAL) | ✅ | $A_5$ v4 §1.4 | 紙・窓非依存 |
| $(Z_{18}$-link$)$ | ⚠ | 未登録 | **手続き** |

$$\boxed{\ \textbf{数学の前件は全て揃った。紙で閉じていないのは (W1) の測定依存性と }(Z_{18}\text{-link})\textbf{ の手続きだけ。}\ }$$

---

## 4. 1 ビット帰着(委嘱 2 前半)

前件が揃ったので $B_{\rm FC}$(定理 B-7)が (5′) を与え、$R^{\rm cyc}_{\rm formal}$(W3-13)が次を与える。

> ### 定理 SURJ-S4(条件付き・candidate)
> **前件**: (TB1)(TB2)(TB3)(TB4)+$(Z_{18}$-link$)$+(CAL)+(W1)(W2)(W3)(W4)(W5)+(6′)(すべて §3 で確認、$(Z_{18}$-link$)$ のみ手続き未了)。
> $K=\mathbf Q(\zeta_{18})=\mathbf Q(\zeta_9)$、$M=e=9$、$u\in K^\times$ を窓 $(P,H)=(\mathrm{PSL}(2,8),\text{Borel})$ の cusp 主係数(補題 B-5 (ii) で well-defined)とすると
> $$\boxed{\ \mathrm{Ih}_{S4}:G_{\mathbf Q}\longrightarrow\mathrm{GTSh}(N,N)\cong\mathrm{Hol}(\mathbf Z/9)\ \text{が全射}\iff\mathrm{ord}\bigl([u^{-1}]_9\bigr)=9\ }$$
> であり、全射性によらず**固定体は $K\bigl((u^{-1})^{1/9}\bigr)$**。

**位数条件の初等化**: $\mathrm{ord}([u^{-1}]_9)\in\{1,3,9\}$ で
$$\mathrm{ord}\bigl([u^{-1}]_9\bigr)=9\iff u^{-1}\notin K^{\times3}.$$
さらに §3 の `surj_d4_t1_v1.md` 補題 3.1 と同じ論法で:

> **系 4.1.** $u^{-1}\in\mathbf Q^\times$ が有理数の 3 乗でなければ $\mathrm{ord}([u^{-1}]_9)=9$、すなわち **$\mathrm{Ih}_{S4}$ は全射**。
> **証明.** $u^{-1}=y^3$($y\in K$)なら $\mathbf Q(y)\subseteq K=\mathbf Q(\zeta_9)$ はアーベル拡大の部分体ゆえ $\mathbf Q$ 上正規。$[\mathbf Q(y):\mathbf Q]=3$ なので共役 $\zeta_3y$ を含み $\zeta_3\in\mathbf Q(y)$、しかし $2\nmid3$ で矛盾。$\blacksquare$

**先例との整合**: $A_5$ 窓($M=e=5$)では $u^{-1}=-2\in\mathbf Q^\times$ で 5 乗でない ⟹ 全射・固定体 $\mathbf Q(\zeta_5,\sqrt[5]2)$(W3-8)。$K^{(3)}$ では $u=-4$(W3-11)。**先例 2 件とも $u^{\pm1}\in\mathbf Q^\times$** なので、系 4.1 が発火する可能性は高い — ただし**これは予想であって証明ではない**(§9【S4-c】で凍結を提案)。

$$\boxed{\ \textbf{1 ビット帰着 = 成立。委嘱 2 の目標は達成された。}\ }$$

---

## 5. $u_{S4}$ の測定計画(委嘱 2 後半)

**測定自体は別工程。** ここでは「何を計算するか」を仕様として書く。$A_5$ v4 §3.5 の手順が骨格になる。

### 5.1 段取り

| 段 | 内容 | 出力 | 備考 |
|---|---|---|---|
| **M0** | 窓の再構成: 封印 JSON の $S,T$($\mathbf F_8$ 行列・整数符号)から $P=\mathrm{PSL}(2,8)$、$X,Y$、$H=$ Borel を GAP で構成 | 生成元と $H$ の明示 | canonical-id fail-closed(封印 JSON の値と突合) |
| **M1** | $P/H$(9 点)上の $X,Y,Z=(XY)^{-1}$ の**巡回型** | **ordered passport** | $0$ 上は $(9)$ が**先験的に確定**(補題 W4-S4)。$1,\infty$ 上は要計算 |
| **M2** | Riemann–Hurwitz で種数 | $g$ | $2g-2=-2\cdot9+\sum_{P\in\{0,1,\infty\}}(9-\#\text{cycles})$。$g=0$ なら M3 は有理関数の連立代数方程式 |
| **M3** | passport に対応する Belyi 写像 $\lambda$ を**定義体上で**構成 | $\lambda\in K(t)$ or $K(W)$ | dessin の個数(= 該当 passport の Hurwitz 数)が 1 なら定義体は $\mathbf Q$、複数なら軌道ごと。**M1 の passport で軌道が一意かを先に確認** |
| **M4** | $\lambda^{-1}(0)$ の唯一点 $P_0$ を同定し、**$K$-有理 uniformizer $s$** を取る | $P_0,s$ | 補題 B-5(i) が $P_0$ の $K$-有理性と $e=9$ を保証(前件済) |
| **M5** | $\lambda=u\,s^{9}\bigl(1+O(s)\bigr)$ を展開して $u$ を読む | $u\in K^\times$ | (ii-loc)(ii-win) で $[u]_9$ は well-defined(前件済) |
| **M6** | **判定**: $u^{-1}\in K^{\times3}$ か | 1 ビット | $u^{-1}\in\mathbf Q^\times$ なら系 4.1 で有理 3 乗判定に落ちる(初等) |
| **M7** | 独立照合: 第二系統($u$ の別経路 or 別モデル)で $[u]_9$ を再計算 | cross-check | $K^{(5)}$ campaign の「$u$ 二経路」規律を踏襲 |

### 5.2 事前登録すべき事項(凍結)

* **M1 の passport** は M3 より前に凍結する(passport を見てから dessin を選ぶ余地を残さない)。
* **M6 の判定則**を先に固定: 「$\mathrm{ord}([u^{-1}]_9)=9$ ⟹ 全射」「$=3$ or $1$ ⟹ **非全射**(= S4 窓に fake shadow が存在)」。
* $u$ の**値**は封印対象にしない(S4 は blind campaign の外)。ただし**測定前に本稿の系 4.1 を凍結**しておけば、「先例どおり $u^{-1}\in\mathbf Q^\times$ 非 3 乗 ⟹ 全射」という**予言先行**の形になる(§9【S4-c】)。

### 5.3 期待コスト

$P$ は位数 504、dessin は次数 9。**A₅ 窓(次数 5)の 1 段上でしかない。** M0–M2 は GAP で秒。M3 が本体(次数 9 の Belyi 写像)だが、$g=0$ なら 1 変数有理関数の係数連立で、既存の $A_5$ の手順が流用できる見込み。**$K^{(5)}$ 級の重さにはならない。**

---

## 6.【SD-a】`settled_fail_count = 0` は isolated を意味するか — **NO**

**一次資料**: `search/kerchi-judge.g`(v1.3)。

### 6.1 判定

$$\boxed{\ \textbf{NO。judge の }\texttt{settled}\textbf{ は「}T_{m,f}\textbf{ が well-defined な準同型か」であって「}\ker T_{m,f}=N\textbf{」ではない。}\ }$$

**根拠(ソース逐語)**:
* KJ-1 修理(裁定 169)のコメント: 「the three original (F2) conditions … do NOT by themselves guarantee that $T_{m,f}$ … is an **actual well-defined homomorphism** … The fix: … additionally require `GroupHomomorphismByImages(Bq, Bq, [s1,s2], [s1^u, f^-1*s2^u*f]) <> fail` … **Candidates failing this are dropped and counted in the new `settled_fail_count` output field**」。
* 出力仕様: 「`settled_all_pass=true` and `settled_fail_count=0` together mean "shadow_total/shadow_total settled", i.e. **every hexagon-candidate that passed the three original (F2) conditions was ALSO well-defined**」。

**⟹ 語の衝突**: 定義ノート §3 の **settled**($\ker(T_{m,f})=N$)と、judge の **settled**(well-definedness)は**別物**である。

### 6.2 さらに強い自認がソースにある

`kerchi-judge.g` の `chi_surjective_assert` 直前のコメント(逐語):

> 「Only "fires" … for `c_in_N` windows, which is the readily-available **proxy** this campaign has used throughout for "isolated 相当" — **genuine isolated-ness ($\ker(T_{m,f})=N$ for every shadow) has never been independently verified anywhere in this campaign** (see `docs/notes/wcp5d_resolution_v1.md` GAP-4 …), so this is a **DELIBERATE, documented simplification, not a claim that `c_in_N` literally implies isolated**.」

### 6.3 帰結

1. **壁窓(梯子 13 窓を含む)の (W1) は未確立。** `settled_fail_count = 0` からも `c_in_N = true` からも isolated は出ない。
2. **$\mathrm{Ih}_N$ の定義の健全性**(像が $\mathrm{GTSh}(N,N)$ に入ること)が壁窓では未保証。⟹ `surj_d4_t1_v1.md` の補題 SURJ-Split を壁窓へ適用する際の前提「$N$ が isolated」は**仮定であって既知ではない**。同稿【SD-a】の懸念は**的中**した。
3. **既出の GAP である**(私の発見ではない): `wcp5d_resolution_v1.md` **GAP-4** に既に記帳されている。novelty 主張はしない。本稿の寄与は「**その既知 GAP が壁窓の (W1)・したがって genuine 議論の土台に直撃する**」という接続の指摘のみ。
4. **S4(PSL 側)は別実装**であり、`isolated: true` の justification は定義ノートの正しい読みを示唆する(§3.5)。ただし**ソース未読**につき検分要請【S4-a】。

---

## 7.【SD-c】t=1 壁窓の捻れ指数 $a$ — **測定完了・$a=+1$**

### 7.1 何を測ればよいか(測定の縮約)

`surj_d4_t1_v1.md` §2.3 の $a\in\{\pm1\}$ は、次のように**1 つの構造的事実に縮約**できる。

> **補題 7.1.** $\Phi|_{\mathfrak F_0}:\mathfrak F_0\to\mathrm{inn}(\langle X\rangle)$ が全単射ならば、$\tilde\chi$-値 $u$ の shadow による $\mathfrak F_0$ 上の共役作用は、同一視 $\mathfrak F_0\cong\langle X\rangle\cong\mathbf Z/9$ の下で **$u$ 倍**である。すなわち $a=+1$(Kummer 捻れ)。
> **証明.** 補題 Φ-univ より $\Phi$ は準同型。自己同型の一般恒等式 $\sigma\,\mathrm{inn}(h)\,\sigma^{-1}=\mathrm{inn}(\sigma(h))$ と $\Phi_{m,f}(X)=X^{u}$ から
> $$\Phi_{m,f}\ \mathrm{inn}(X^j)\ \Phi_{m,f}^{-1}=\mathrm{inn}\bigl(\Phi_{m,f}(X^j)\bigr)=\mathrm{inn}(X^{ju}).$$
> $\Phi$ 単射なので $\mathrm{GTSh}$ 側の共役も同じ規則に従う。$(\mathbf Z/18)^\times\to(\mathbf Z/9)^\times$ は標準還元だから捻れは $+1$。$\blacksquare$

### 7.2 GAP 実測(本稿で実施)

`.\gap.ps1`(GAP 4.16.0・`-o 2g`)で、driver spec の $s_1,s_2$ から窓を再構成し、$m=0$ 層を**悉皆走査**(全 1814400 元)した。

**窓 assert(judge とは独立に再現)**
```
|Bq| = 10886400  (= 6*|A10|)          ✓
|PN| = 1814400   (= |A10|)            ✓
ord(x) = 9   ord(y) = 9   c = id      ✓
N_ord = 9                             ✓
```
**$\mathrm{Aut}(P)$ 側**
```
|C_{S10}(X)|   = 9   (= |<X>|)        ✓
|N_{S10}(<X>)| = 54   IdGroup = [54,6]
  → 測定済 GTSh の IdGroup [54,6] と一致
```
**$m=0$ 層**
```
scanned = 1814400   |F_0| = 9        ← 証明書の ker_size = 9 を別実装で独立再現
j-values = [0, 8, 6, 5, 1, 7, 3, 2, 4]
all in inn(<X>) ? = true
distinct j count = 9   (= Z/9 全体)   ← Phi|_{F_0} は全単射
```

$$\boxed{\ \Phi|_{\mathfrak F_0}:\mathfrak F_0\xrightarrow{\ \sim\ }\mathrm{inn}(\langle X\rangle)\ \text{は全単射}\ \Longrightarrow\ \boxed{a=+1}\ }$$

### 7.3 帰結

* `surj_d4_t1_v1.md` §2.3 の二択が解消: **核方向の指標 $c:G_{\mathbf Q(\zeta_9)}\to\mathbf Z/9$ は真の Kummer 類**である($\mu_9\subset\mathbf Q(\zeta_9)$ ゆえ $H^1(G_{K_0},\mu_9)\cong K_0^\times/K_0^{\times9}$)。⟹ **層 II の記述は完全に確定**(残るのは層 III = $u$ の同定のみ)。
* **副産物**: 壁窓でも $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X\rangle)$・$\mathfrak F_0\cong C_9$ が成立(補題 F0 の仮定が $A_{10}$ 窓でも満たされる: $C_{S_{10}}(X)=\langle X\rangle$ を実測)。**命題 K5-1 型の現象は dihedral 族・PSL・壁の 3 系統で共通**。
* **⚠ 射程**: この測定は $\mathrm{Ih}$ の像について**何も言わない**。$a$ は $\mathrm{GTSh}$ の内部構造の量である。
* **⚠ 単系統**: 私の使い捨てスクリプト 1 本(scratchpad・未 commit)。判定に用いた $\lvert\mathfrak F_0\rvert=9$ は kerchi-judge の値と一致した(実質二系統)が、$j$-値表は単系統。

---

## 8. FINDING

| # | 種別 | 内容 |
|---|---|---|
| **S4-1** | **成立(委嘱 1・2)** | S4 で **(W1)–(W5)+(W5$^{\mathbb Q}$)+(6′)+(CAL) が揃う**。うち **(W2)群/(W3)(W4)(W5)(W5$^{\mathbb Q}$)(6′) は本稿で紙上証明**。⟹ **1 ビット帰着が成立**(定理 SURJ-S4) |
| **S4-2** | **窓非依存化(道具)** | **補題 Φ-univ**: $\Phi$ の共変性は `phifam` §2 の証明が座標を使わないので**全窓へ持ち上がる**。⟹ **【GAP-06a】を紙で閉じる**(実装確認待ち不要) |
| **S4-3** | **★ 命題 K5-1 の族外一般化** | **補題 F0**: 「$\Phi$ 単射 + $C_{\mathrm{Aut}(P)}(X)=\langle X\rangle$ + $\lvert\mathfrak F_0\rvert=\mathrm{ord}(X)$」だけから $\mathfrak F_0\cong C_{\mathrm{ord}(X)}$ かつ $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X\rangle)$。**dihedral 族の座標を使わない初の形**。S4・壁窓 t=1 の両方で前件充足を確認 |
| **S4-4** | **分水嶺の明示** | S4 で (W4) が成立するのは $M=9=\lvert\mathbf P^1(\mathbf F_8)\rvert$ だから。壁窓は $M=9<n$ で不成立(TAIL-OBS)。**「$M\ge$ 最小忠実置換次数」が橋の適用可否の境界** |
| **S4-5** | **★【SD-a】= NO** | judge の `settled_fail_count` は **well-definedness** の検査で isolated ではない。judge ソース自身が「genuine isolated-ness は本キャンペーンでどこでも独立検証されていない」と明記(既出 **GAP-4**)。⟹ **壁窓の (W1) は未確立・$\mathrm{Ih}_N$ の健全性が未保証** |
| **S4-6** | **★【SD-c】= $a=+1$** | GAP 実測で $\Phi|_{\mathfrak F_0}$ 全単射 ⟹ 捻れ $+1$ ⟹ 核方向は**真の Kummer 類**。`surj_d4_t1_v1.md` の未測定 1 ビットを閉じた。$\lvert\mathfrak F_0\rvert=9$ を別実装で独立再現 |
| **S4-7** | **procedural gap** | $(Z_{18}$-link$)$ が S4 の window inventory に無い。**$K^{(3)}/A_5$ と同格の `pending`** であって S4 固有の弱点ではない |
| **S4-8** | **要検分** | S4 の `isolated: true` の `settled` が定義ノートの settled かを PSL スクリプトのソースで確認(【SD-a】の教訓の水平展開) |

---

## 9. 未閉鎖項・次の一手

* 【S4-a】**最優先**: PSL 実装(段 S1–S7 を出したスクリプト)の `settled_count` の意味論確認。定義ノートの settled($\ker T_{m,f}=N$)なら (W1) は閉じ、**S4 の前件は $(Z_{18}$-link$)$ を除いて全閉**。違えば (W1) は壁窓と同じ身分に落ちる。**§6 と同型の調査で 30 分。**
* 【S4-b】$(Z_{18}$-link$)$ の window inventory 行の起票(手続き・司令塔案件)。$K^{(3)}/A_5$ の `pending` 解消と**同じ便でまとめて**処理するのが効率的。
* 【S4-c】**予言先行の凍結**: 測定前に「$u^{-1}\in\mathbf Q^\times$ かつ有理 3 乗でない ⟹ $\mathrm{Ih}_{S4}$ 全射」(系 4.1)と、$A_5$/$K^{(3)}$ の先例からの予想「**全射**」を凍結。的中判定が M6 で自動的に付く。
* 【S4-d】測定発注(§5 の M0–M7)。**M1(passport)を M3 の前に凍結**すること。
* 【S4-e】**壁窓側への波及**: 【SD-a】により壁窓の (W1) が未確立と判明した以上、**壁キャンペーンの GTSh 主張群が「$\mathrm{GTSh}(N,N)$ の計算」として何を意味するか**を司令塔が整理する必要がある(isolated でなければ $\mathrm{GT}(N)\ne\mathrm{GTSh}(N,N)$ で、判定は $\mathrm{GTSh}(N,N)$ 側にしか及ばない)。**本稿の射程外だが、影響は広い。**
* 【S4-f】本稿は**紙上(paper-proof candidate)・単系統・Sol 監査前**。**Lean 検証ではない。** §7 の GAP は使い捨て(scratchpad・未 commit)。$u_{S4}$ の値には触れていない。$K^{(5)}$ 非接触。

> ### 【文献要請】— 本稿からは無し
> S4 の前件は正典と既存資産で閉じた。`surj_d4_t1_v1.md` の要請(非全分岐 cusp での半局所 Kummer 不変量)は**壁窓側の話として有効なまま**であり、本稿はそれを増やさない。
