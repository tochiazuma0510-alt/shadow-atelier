# 補題 **BH-BRIDGE** — 文献 BH-L1(Kurihara 1992)から当窓 $\mathbf N$ の算術像へ(**翻訳補題 v1**)

**状態札: `candidate(paper-proof candidate・単系統・Sol 未監査 / 新規窓計算ゼロ / 機械は付録 A の Fox 微分検算(整数演算・窓非接触・cert bhbridge_foxcheck_20260806 = 30/30 PASS)のみ / 封印 3 量非接触 / novelty 主張なし / 残余ギャップ【BR-GAP-1】1 個を明記)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-06
- 委嘱: 司令塔(**裁定 576**)+ **裁定 578 の前提訂正を反映**(§0.2)
- 目的: 事前登録票 `docs/notes/bhunt_prereg_iffirst_v1.md` の **定理 BH-4 の前件**
  $$\mathrm{Ih}_{\mathbf N}\bigl(G_{\mathbb Q(\mu_7)}\bigr)\ne 1$$
  を、供給された外部文献(Kurihara 1992)と正典から導く。

### 入力正本(すべて既在または本便で降ろされた文献)

| 記号 | 出所 | 状態 |
|---|---|---|
| **[KUR]** | Kurihara, *Some remarks on conjectures about cyclotomic fields and $K$-groups of $\mathbf Z$*, Compositio Math. **81** (1992) 223–236(numdam) | 司令塔配達(裁定 578)。`papers/kurihara-1992-compositio-cyclotomic-Kgroups.pdf`(gitignored)/ SHA-256 `70ee5919eae904197bf5949e9a8af2b45a805d31e2976241217be329360becca`(当方が numdam から独立に取得した実体と**バイト同一**を確認 — 重複は削除した) |
| **[J0J2]** | `search/certs/bhunt_j0j2_20260806.json`(裁定 575・**(J0)–(J2) 既走 cert**) | 既在。**本ノートの導出に先行する測定**(§8.2 で時系列を申告) |
| **[FOX]** | `search/certs/bhbridge_foxcheck_20260806.json`(本ノートの検算 cert・30/30 PASS) | 本ノートで生成(付録 A) |
| **[ICM]** | Ihara, *Braids, Galois Groups, and Some Arithmetic Functions*, ICM Kyoto 1990 | 既在 `papers/ihara-ICM1990-vol1-braids-galois-arithmetic.ocr.pdf`。**頁対応: 印字頁 = PDF 頁 − 88**(読解ノート `reading_ihara_icm1990_tb3_v1.md` で確定済) |
| **[2405]** | arXiv 2405.11725(正典)§1.1・§1.3・§1.3.1 | `papers/txt/2405.11725-….txt` |
| **[HS7]** | `docs/notes/hs_prop7_translation_v1.md` §1.4(逐語辞書)・§2.2(定理 D3-BLIND)・§8.7.3(定義 NW(7)) | 既在 |
| **[PRE]** | `docs/notes/bhunt_prereg_iffirst_v1.md`(IF-FIRST 事前登録票 v1) | 既在・**本ノートは 1 バイトも改変しない** |
| **[C2]** | `search/certs/hsp7_cond2_p7_20260804.json`(発火条件 2 cert) | 既在 |

---

## 0. 先に 6 行 — 本ノートの拘束と、委嘱前提の訂正

| # | 拘束 |
|---|---|
| **0-1** | **紙のみ。** GAP も pc 群も起動していない。機械は付録 A の python(Fox 微分・整数/Laurent 演算・窓非接触)だけ。 |
| **0-2** | **42 個の candidate key の値に一切触れていない。** 本ノートは窓の値を 1 個も読んでいない。 |
| **0-3** | **封印 3 量非接触**($n=5$ 系・$\mathrm{Im}\,R$・$d_N$・genuine 層の $u$ 値・PSL 量)。本ノートで使う「$u$」は $[\mathrm{PRE}]$ §4.3 の公開の窓座標 $u=2m+1=\chi_{\rm vir}$ のみ。 |
| **0-4** | 結論はすべて **framework-relative**。`cross-checked` も `verified` も付かない。 |
| **0-5** | **novelty 主張なし**(grep 済: `BH-BRIDGE`・`Kurihara`・`Soulé`・「円分元」は repo に既出なし = repo 内では新規語だが、**数学の内容は [KUR] と [ICM] の既知定理の合成**であり、新規性は主張しない)。 |
| **0-6** | [PRE] の IF-FIRST 凍結を保全。本ノートは [PRE] を改版せず、**§8 に「(J1′) への反証可能な予言」を新規登録**する形で追記する(別ファイル・単独コミット)。 |

### 0.1 一行の結論(先に)

> $$\boxed{\ \textbf{BH-BRIDGE は通る。ただし残余ギャップ 1 個(正規化の一段・}\textbf{【BR-GAP-1】}\textbf{)を明記したうえで。}\ }$$
> $$\boxed{\ \textbf{BH-1 の二値 + 本補題}\ \Longrightarrow\ \mathrm{GT}^{\rm arith}(\mathbf N)=H_W,\quad \lvert\mathrm{GT}^{\rm arith}(\mathbf N)\rvert=42\ \Longrightarrow\ \textbf{BH-α(B 型候補ゼロ)確定候補}.\ }$$
> 発効は **Sol 監査後(便 109)**。
>
> さらに、既走の (J1′) 測定([J0J2])が **$\Phi\vert_L=-1=u_0^3$** を出しており、これは本補題が名指しする $\mathrm{gr}_3$ 直線(= Tate 捻り 3)と一致する(§8.2.2 整合 (ii))。**測定が導出に先行しているので予言とは呼ばない**が、$\mathrm{gr}_4$ 側($u_0^4\equiv4$)を排除する識別力のある一致である。

### 0.2 ★ 委嘱前提の訂正(裁定 578 と独立に、原典で同一結論)

委嘱文は「Kurihara の設定は **B₄ 系**(pentagon あり・当工房の副線)」としたが、**これは誤りである**。原典 [KUR] 印字 231 §4 (2) 逐語:

> "(2) *Galois representation arising from* $\pi_1^{\rm pro\text-p}(\mathbf P^1\backslash\{0,1,\infty\})$. … Let $p$ be an odd prime. Put $X=\mathbf P^1\backslash\{0,1,\infty\}$. Then, $G_{\mathbf Q}$ acts on $\pi_1(X)$ and on its pro-$p$ completion $\pi_1^{\rm pro\text-p}(X)\simeq\mathscr F$ by conjugation where $\mathscr F$ is the free pro-$p$ group of rank 2." — [KUR] 印字 231

⟹ Kurihara の舞台は **$\mathbb P^1\setminus\{0,1,\infty\}$ の pro-$p$ 基本群 = 当工房の主線と同じ $F_2$** である。**B₄→B₃ の大工事は不要**であり、本ノートは**そのような工事を一行も含まない**。

> ★ **では真の翻訳ギャップはどこにあったか。** 委嘱が案じた「同名別物」は解消するが、代わりに**別の落とし穴**が現れる。それは
> $$\textbf{Kurihara の }\Phi(3)/\Phi(4)\ \textbf{が }\mathrm{gr}_3(\mathscr F)\otimes\mathbb Z_p\ \textbf{の中で飽和(saturated)かどうか}$$
> である(§7.1)。飽和でなければ **mod 7 で像が消え、当窓の結論は BH-α から BH-β へ反転する**。[KUR] はこれを述べていない。**本ノートの技術的中心は、この落とし穴を通らない迂回路を正典 [ICM] §6 の中に作ったこと**である(§4)。

---

## 1. 二つの設営を並べる(**辞書を先に固定する**)

### 1.1 Kurihara / Ihara 側(pro-$p$ 側)

- $X=\mathbb P^1\setminus\{0,1,\infty\}$、$\mathscr F:=\pi_1^{\text{pro-}p}(X)$ = 階数 2 の自由 pro-$p$ 群([KUR] 印字 231・上記逐語)。
- $G_{\mathbb Q}$ の作用は [ICM] 印字 106 (PDF 194) の **(2.3.1)(2.3.2)** で座標化される(読解ノート §3.5 で 400 dpi 照合済):
  > $f_\sigma=p^{-1}\circ\sigma(p)\in\hat\pi_1(X(\mathbb C),\vec{01})$ … (2.3.1)
  > $x\longrightarrow x^{\chi(\sigma)},\quad y\longrightarrow f_\sigma^{-1}\,y^{\chi(\sigma)}\,f_\sigma$ … (2.3.2)
  > "It follows easily that $f_\sigma\in\hat F_2'$, and that (2.3.2) with this requirement characterizes $f_\sigma$."
- **フィルトレーション**([KUR] 印字 231): $\Phi=Br\,d_2^{(p)}\subseteq\mathrm{Out}\,\mathscr F$([Ih Annals 1986] p.46)、$(\Phi(m))_{m\ge1}$ は $\mathscr F$ の**下中心列で定義**される。$\varphi:G_{\mathbb Q}\to\Phi$。
- **不分岐性**([ICM] 印字 112 = PDF 200 §5.2 逐語): 対応する体の塔 $\mathbb Q^{(l)}(\infty)$ は "a pro-$l$ (non-abelian) extension over $\mathbb Q(\mu_{l^\infty})$ **unramified outside $l$**"。

### 1.2 当工房側(B₃-gentle・有限窓)

- [2405] §1.1(txt 81–83 行)逐語: $PB_3=\langle x_{12},x_{23}\rangle\times\langle c\rangle$、$x_{12}:=\sigma_1^2$、$x_{23}:=\sigma_2^2$、$c:=(\sigma_1\sigma_2\sigma_1)^2$、"We identify the free group $F_2$ on two generators with the subgroup $\langle x_{12},x_{23}\rangle$ of $PB_3$"。
- [2405] §1.3 の **(1.5)**: $\mathrm{Ih}(g):=\bigl((\chi(g)-1)/2,\ f_g\bigr)$、ここで $f_g$ は
  $$g(x)=x^{\chi(g)},\qquad g(y)=f_g^{-1}y^{\chi(g)}f_g$$
  で与えられる元(逐語・[2405] §1.3)。**(1.6)** で $G_{\mathbb Q}\hookrightarrow\widehat{GT}$、**(1.11)(1.12)** で $\mathrm{Ih}_{\mathbf N}:=\mathrm{PR}_{\mathbf N}\circ\mathrm{Ih}$、$\mathrm{GT}^{\rm arith}(\mathbf N):=\mathrm{Ih}_{\mathbf N}(G_{\mathbb Q})$。**(1.3)**: $\mathrm{PR}_{\mathbf N}(\hat m,\hat f)=[\widehat P_{N_{\rm ord}}(\hat m),\ \widehat P_{N_{F_2}}(\hat f)]$。
- 窓(定義 **NW(7)**・[HS7] §8.7.3):
  $$\mathbf N=\mathcal V(F_2)\times\langle c\rangle,\quad N_{F_2}=\mathcal V(F_2)=\gamma_5(F_2)F_2^{\,7},\quad P=F_2/N_{F_2},\quad N_{\rm ord}=7 .$$
- 測定([C2] cert 逐語欄): `size_P = 5764801` $=7^8$、`lcs_layer_dims_F7 = [2,1,2,3]`、`dim_gamma4_P_F7 = 3`、`derived_subgroup_size = 117649` $=7^6$。

### 1.3 ★ 一致するもの・しないもの(**罠の精算表**)

| 対象 | Kurihara/Ihara 側 | 当工房側 | 判定 |
|---|---|---|---|
| **自由群** | $\mathscr F=\pi_1^{\text{pro-}p}(\mathbb P^1\!\setminus\!\{0,1,\infty\})$、階数 2 | $F_2=\langle x_{12},x_{23}\rangle\subset PB_3$ | ★ **同一**(§2 補題 BR-1)。委嘱が案じた B₄ の混入はない |
| **$G_{\mathbb Q}$ 作用の座標** | (2.3.2) の $(\chi,f_\sigma)$ | (1.5) の $(\chi,f_g)$ | ★ **同一の式**(§2) |
| **hexagon** | (3.1.1)(I)(II)([ICM] 印字 106) | (3.10)(3.11) | ★ **逐語辞書済**([HS7] §1.4) |
| **窓の圏** | $\Phi\subseteq\mathrm{Out}\,\mathscr F$ の合同フィルトレーション(**副有限**) | $\mathrm{NFI}_{PB_3}(B_3)$ の**有限**窓 $\mathbf N$ | ⚠ **別物**。橋は「$\mathrm{gr}_3$ を経由して有限化する」形でしか架からない(§5) |
| **pentagon** | Kurihara は使わない | $\mathrm{PENT}_W$ は別途 | 交差しない(本補題は hexagon 側だけを使う) |
| **$\Phi(3)/\Phi(4)$ の格子** | $\cong\mathbb Z_p$(位数のみ言明) | — | ★ **飽和性は未言明** ⟹ §7.1 の落とし穴。**本補題はここを通らない** |

---

## 2. 段 I — $f_\sigma$ と $f_g$ は**同一の元**である

> ### 補題 BR-1(同一性)
> $F_2=\langle x_{12},x_{23}\rangle$ と $\pi_1(X(\mathbb C),\vec{01})=\langle x,y\rangle$ の正典の同一視の下で、
> $$f_g\ (\text{[2405] (1.5)})\ =\ f_\sigma\ (\text{[ICM] (2.3.1)})\qquad(g=\sigma\in G_{\mathbb Q}).$$
>
> **証明.** [ICM] 印字 106 逐語より、$f_\sigma$ は「$f\in\hat F_2'$ かつ (2.3.2) が成り立つ」という条件で**一意に特徴づけられる**。[2405] §1.3 は $f_g$ について**文字通り同じ式** $g(x)=x^{\chi(g)},\ g(y)=f_g^{-1}y^{\chi(g)}f_g$ を述べ、かつ $f_g\in\widehat{F_2}$ を $\widehat{GT}$ の第 2 座標(charming = 交換子部分群の元)として扱う。同じ作用・同じ生成対・同じ特徴づけゆえ両者は一致する。∎

> ### ★ 規約ずれの排除(**$S_3$ のうち何が残るか**)
> 生成対の同一視に $S_3=\langle\theta,\tau\rangle$ 分のずれが残る可能性を潰す。
> - **$\tau$ 型のずれは式の形が排除する。** もし当工房の $x$ が Ihara の $y$(または $z$)なら、当工房側の「$g(x)=x^{\chi}$」は Ihara 側で「$g(y)=y^\chi$」を意味するが、Ihara の (2.3.2) は $g(y)=f_\sigma^{-1}y^\chi f_\sigma$ であり、両立には $f_\sigma$ が $y^\chi$ と可換($\Rightarrow f_\sigma=1$)を要する。$f_\sigma\ne1$ となる $\sigma$ が存在する(Belyi による単射性・[2405] (1.6))ので矛盾。⟹ **排除**。
> - **$\theta$ 型($x\leftrightarrow y$)のずれは無害。** $\theta$ は $\mathrm{gr}_3$ 上 $u_1\mapsto-u_2,\ u_2\mapsto-u_1$(付録 A (4) で機械確認)ゆえ $\mathfrak h_3=u_1+u_2\mapsto-\mathfrak h_3$。**直線 $\mathbb Z\mathfrak h_3$ は保たれる**ので、本補題が使う「非消滅」に影響しない。
> - 残るのは inner 型の微調整のみ ⟹ **【BR-GAP-2】**(§7.2)。

---

## 3. 段 II — 深さ 3 の座標と $\mathfrak h_3$ 直線

$\mathrm{gr}_3(F_2)\cong\mathbb Z^2$、基底
$$u_1:=[[x,y],x],\qquad u_2:=[[x,y],y]\qquad([a,b]:=aba^{-1}b^{-1}),$$
$$\mathfrak h_3:=u_1+u_2 .$$
([HS7] §2.2 と同一の基底・同一の記号。付録 A で $\theta(u_1)\equiv-u_2$, $\theta(u_2)\equiv-u_1$ を機械確認し、[HS7] の $\theta$ 作用と一致することを確かめた。)

> ### 補題 BR-2(飽和性)
> $\mathbb Z\mathfrak h_3$ は $\mathrm{gr}_3(F_2)=\mathbb Z u_1\oplus\mathbb Z u_2$ の中で**飽和**(= 直和因子)である。
>
> **証明.** $\mathfrak h_3=(1,1)$ は原始ベクトル($\gcd(1,1)=1$)。$\mathbb Z^2/\mathbb Z(1,1)\cong\mathbb Z$ は捩れなし。∎(付録 A (5))

> ### 系 BR-2′(深さ 3 の hexagon 軌跡)
> [HS7] **定理 D3-BLIND (b)**: hexagon (3.10) は深さ 3 で $a=b$ と同値。ゆえに hexagon を満たす $f$ の深さ 3 成分は $\mathbb Z_p\mathfrak h_3$ に**ちょうど**乗る(飽和した 1 本の直線)。
> ⚠ ただし **本補題は D3-BLIND を前件として使わない** — §4 の公式から $a=b$ が独立に落ちてくるからである(§4 の ★ 参照)。D3-BLIND は**照合用**に置く。

---

## 4. 段 III(★ **本ノートの技術的中心**)— $f_\sigma$ の深さ 3 係数を **Soulé–Deligne 円分元で書く**

以下 $p$ は奇素数、$\sigma\in G_{\mathbb Q(\mu_{p^\infty})}$、すなわち **$\chi^{(p)}(\sigma)=1$**(円分指標の $p$ 成分が $1$)とする。すべて pro-$p$ 成分で考える($\mathscr F=F_2^{(p)}$、係数 $\mathbb Z_p$)。

### 4.1 [ICM] §6 から引く 4 つの式(逐語 pin)

**(i)** [ICM] 印字 114(PDF 202)§6.1:
> $\mathscr A=\widehat{\mathbb Z}\ll\xi,\eta\gg$(非可換巾級数環)、$F_2^{\rm nil}\hookrightarrow\mathscr A^\times$ via $x\to1+\xi,\ y\to1+\eta$;
> $\mathscr A=\widehat{\mathbb Z}\cdot1\oplus\mathscr A\cdot\xi\oplus\mathscr A\cdot\eta$ … (6.1.1);
> $(f_\sigma^{\rm nil})^{-1}=1+A_1\xi+A_2\eta$;  Put $\psi_\sigma(\xi,\eta)=1+A_1\xi$;  $f_\sigma^{\rm nil}=\psi_\sigma(\eta,\xi)\cdot\psi_\sigma(\xi,\eta)^{-1}$;
> $\psi^{\rm ab}_\sigma$ は $\xi,\eta$ を可換化して得られる $\mathscr A^{\rm ab}=\widehat{\mathbb Z}[[\xi,\eta]]$ の元。

**(ii)** [ICM] 印字 115(PDF 203)§6.2 (ii)(**Soulé–Deligne 円分元**):
> $\kappa^{(l)}_m:G_{\mathbb Q}\longrightarrow\mathbb Z_l$($m\ge1$, odd)、1-cocycle 関係
> $$\kappa^{(l)}_m(\sigma\tau)=\kappa^{(l)}_m(\sigma)+\chi^{(l)}(\sigma)^m\kappa^{(l)}_m(\tau)\qquad(6.2.1)$$
> [Construction] $\varepsilon_{m,n}=\prod_a(\zeta_n^a-1)^{\langle a^{m-1}\rangle}$($0<a<l^n$, $(a,l)=1$、$\langle a^{m-1}\rangle$ = $a^{m-1}\bmod l^n$ の最小正代表)、
> $$\sigma\bigl((\varepsilon_{m,n})^{1/l^n}\bigr)=(\sigma(\varepsilon_{m,n}))^{1/l^n}\cdot\zeta_n^{\chi^{(l)}(\sigma)^{1-m}\kappa^{(l)}_m(\sigma)} .$$
> "Moreover, by Soulé $[\mathrm{So}_{1,2}]$, these 1-cocycles $\kappa^{(l)}_m$ do not vanish at least if $l>2$."

**(iii)** [ICM] 印字 115–116(PDF 203–204)§6.3(**Anderson–Coleman–Deligne–Ihara–Kaneko–Yukinari の明示公式**):
> $\kappa^*_m(\sigma)=\bigl((l^{m-1}-1)^{-1}\kappa^{(l)}_m(\sigma)\bigr)_l$;
> **Theorem [$A_3,C_3$, IKY].**
> $$\psi^{\rm ab}_\sigma(\xi,\eta)=\exp\Bigl\{\sum_{m\ge3,\,odd}\frac{\kappa^*_m(\sigma)}{m!}\bigl((X+Y)^m-X^m-Y^m\bigr)\Bigr\}\times\exp\Bigl\{-\frac12\sum_{m\ge2,\,even}\frac{b_m(1-\chi(\sigma)^m)}{m!}\bigl((X+Y)^m-X^m-Y^m\bigr)\Bigr\},$$
> $X=\log(1+\xi)$, $Y=\log(1+\eta)$, $\log\bigl((1-e^{-t})/t\bigr)=\sum_{m\ge1}(b_m/m!)t^m$。

**(iv)** [ICM] 印字 116(PDF 204)§6.4:
> $\mathscr F=\widehat{F_2}$、$\mathscr F'^{\rm ab}=\mathscr F'/\mathscr F''$ は完備群環 $\widehat{\mathbb Z}[[\mathscr F^{\rm ab}]]$ 上**階数 1 の自由加群**で、生成元は $(x,y)=xyx^{-1}y^{-1}$ の類 $\theta'$;
> $$\sigma(\theta')=B'_\sigma\cdot\theta'\quad(6.4.1),\qquad B'_\sigma=\Bigl(\frac{\underline x^{\chi(\sigma)}-1}{\underline x-1}\cdot\frac{\underline y^{\chi(\sigma)}-1}{\underline y-1}\Bigr)B_\sigma\quad(6.4.2),$$
> $$\mathrm{pr}:\widehat{\mathbb Z}[[\mathscr F^{\rm ab}]]\to\widehat{\mathbb Z}[[\xi,\eta]]\ \ (\underline x\mapsto1+\xi,\ \underline y\mapsto1+\eta)\quad(6.4.3),\qquad \mathrm{pr}(B_\sigma)=\psi^{\rm ab}_\sigma\quad(6.4.4).$$

### 4.2 補題 BR-3(**深さ 3 の係数公式**)

> ### 補題 BR-3
> $p$ を奇素数、$\sigma\in G_{\mathbb Q(\mu_{p^\infty})}$ とする。$p$ 成分において
> $$\boxed{\ f_\sigma\ \equiv\ -\frac{\kappa^*_3(\sigma)}{2}\,\mathfrak h_3\ \pmod{\gamma_4(\mathscr F)},\qquad \kappa^*_3(\sigma)=(p^2-1)^{-1}\kappa^{(p)}_3(\sigma).\ }$$
> とくに $f_\sigma\in\gamma_3(\mathscr F)$ であり(深さ 2 成分は消える)、深さ 3 成分は $u_1,u_2$ の係数が**等しい**。

**証明.** 4 段。

**(a) 深さ 2 の消滅と $B'_\sigma=B_\sigma$。** $\chi^{(p)}(\sigma)=1$ ゆえ (6.4.2) の補正因子は $p$ 成分で $1$、したがって $B'_\sigma=B_\sigma$ で $\mathrm{pr}(B'_\sigma)=\psi^{\rm ab}_\sigma$((6.4.4))。また (iii) の第 2 因子は $1-\chi(\sigma)^m$ の $p$ 成分が $0$ ゆえ $p$ 進的に $1$、第 1 因子は $m\ge3$ から始まる。ゆえに
$$\psi^{\rm ab}_\sigma\equiv1+\frac{\kappa^*_3(\sigma)}{3!}\bigl((X+Y)^3-X^3-Y^3\bigr)=1+\frac{\kappa^*_3(\sigma)}{2}\,XY(X+Y)\pmod{\deg\ge4},$$
$X\equiv\xi,\ Y\equiv\eta\pmod{\deg\ge2}$ より
$$\boxed{\ \psi^{\rm ab}_\sigma\equiv1+\frac{\kappa^*_3(\sigma)}{2}\bigl(\xi^2\eta+\xi\eta^2\bigr)\pmod{\deg\ge4}.\ }\tag{4.1}$$
とくに **$\psi^{\rm ab}_\sigma$ は次数 2 の項を持たない**。

**(b) $\sigma$ の $\mathscr F'/\mathscr F''$ 上の作用を $f_\sigma$ で書く。** $\chi^{(p)}(\sigma)=1$ ゆえ (2.3.2) は $\sigma(x)=x,\ \sigma(y)=f^{-1}yf$($f:=f_\sigma$)。$c:=y^{-1}f^{-1}yf\in\mathscr F'$ と置くと $f^{-1}yf=yc$ で、自由群の恒等式
$$[x,\,yc]=[x,y]\cdot y\,[x,c]\,y^{-1}$$
が成り立つ(直接展開)。$\mathscr F'/\mathscr F''$ の加法記法($\underline g$ の共役作用)で $\theta_c=(1-\underline y^{-1})\theta_f$、$\theta_{[x,c]}=(\underline x-1)\theta_c$ ゆえ
$$\sigma(\theta')=\theta'+\underline y(\underline x-1)(1-\underline y^{-1})\theta_f=\theta'+(\underline x-1)(\underline y-1)\,\theta_f .$$
$\theta_f=h\cdot\theta'$($h\in\widehat{\mathbb Z}[[\mathscr F^{\rm ab}]]$)と書けば
$$\boxed{\ B'_\sigma=1+(\underline x-1)(\underline y-1)\,h\ }\tag{4.2}$$
> ★ この (4.2) が**本証明の要**である。**付録 A (3) が 7 通りの $f$(斉次・非斉次・逆元込み)で Fox 微分により機械確認した。**

**(c) $h$ の 1 次項を深さ 3 係数で書く。** $\mathscr F'/\mathscr F''$ の $\widehat{\mathbb Z}[[\mathscr F^{\rm ab}]]$-座標 $h$ について
$$h(\theta')=1,\qquad h(u_1)=-(\underline x-1),\qquad h(u_2)=-(\underline y-1)$$
(付録 A (1)(2)・Fox 微分で厳密計算)。$h$ は $\mathscr F'/\mathscr F''$ 上加法的(付録 A (8))、$\gamma_4$ の元は $\mathrm{pr}\,h$ の $(\xi,\eta)$-次数 $\ge2$(付録 A (7)(8))。ゆえに $f\equiv a\,u_1+b\,u_2\pmod{\gamma_4}$、深さ 2 成分を $c_2$ とすると
$$\mathrm{pr}(h)\ \equiv\ c_2-(a\xi+b\eta)\pmod{(\xi,\eta)^2},$$
$$\mathrm{pr}(B'_\sigma)\ \equiv\ 1+c_2\,\xi\eta-a\,\xi^2\eta-b\,\xi\eta^2\pmod{\deg\ge4}.\tag{4.3}$$

**(d) 係数比較。** (4.1) と (4.3) を $\mathrm{pr}(B'_\sigma)=\psi^{\rm ab}_\sigma$ で突き合わせる。次数 2:$c_2=0$(⟹ $f_\sigma\in\gamma_3$)。次数 3:
$$-a=\frac{\kappa^*_3(\sigma)}{2},\qquad -b=\frac{\kappa^*_3(\sigma)}{2}\quad\Longrightarrow\quad a=b=-\frac{\kappa^*_3(\sigma)}{2}. \qquad\blacksquare$$

> ### ★ 二つの副産物(**独立の裏取り**)
> 1. **$a=b$ が公式の対称性から落ちてくる。** (4.1) の $\xi^2\eta+\xi\eta^2$ は $\xi\leftrightarrow\eta$ 対称であり、これがそのまま $a=b$ を与える。これは [HS7] **定理 D3-BLIND (b)**(hexagon 深さ 3 $\iff a=b$)の**完全に独立な再導出**である(一方は $K(0,5)$/hexagon の線型代数、他方は Anderson–Coleman–IKY の明示公式)。**規約の整合が取れていることの強い証拠**。
> 2. **$c_2=0$ も同時に落ちる。** [HS7] の C2-FIN($c_2=m(m+1)/6$、$m\equiv0$)を引かずに済む。

### 4.3 $p=7$ での単元性

$\kappa^*_3=(p^2-1)^{-1}\kappa^{(p)}_3$、係数 $-1/2$。$p=7$ で
$$2\equiv2,\qquad p^2-1=48\equiv6,\qquad 2(p^2-1)=96\equiv5\pmod 7$$
すべて $\ne0$(付録 A (6))。ゆえに
$$\boxed{\ a_\sigma:=-\frac{\kappa^*_3(\sigma)}{2}\in\mathbb Z_7^\times\iff\kappa^{(7)}_3(\sigma)\in\mathbb Z_7^\times .\ }\tag{4.4}$$

---

## 5. 段 IV — 窓 $\mathbf N$ への還元(**副有限 → 有限**)

> ### 補題 BR-4(窓への降下)
> $\sigma\in G_{\mathbb Q(\mu_7)}$ とする。
> **(1)** $m_\sigma:=(\chi(\sigma)-1)/2\equiv0\pmod 7$、ゆえに $\mathrm{Ih}_{\mathbf N}(\sigma)=[0,\ \bar f_\sigma]\in A=\ker\chi_{\rm vir}$。
> **(2)** さらに $\sigma\in G_{\mathbb Q(\mu_{7^\infty})}$ で $\kappa^{(7)}_3(\sigma)\in\mathbb Z_7^\times$ ならば $\bar f_\sigma\ne1$ in $P$、すなわち $\mathrm{Ih}_{\mathbf N}(\sigma)\ne1$。
>
> **証明.**
> **(1)** $\chi(\sigma)\equiv1\pmod 7$、$2\in(\mathbb Z/7)^\times$ ゆえ $m_\sigma\equiv0$。[2405] (1.13) の可換性 $\chi_{\rm vir,\mathbf N}\circ\mathrm{Ih}_{\mathbf N}=\widehat P_7\circ\chi$ から $\chi_{\rm vir}(\mathrm{Ih}_{\mathbf N}(\sigma))=1$、すなわち像は $A$ に入る([PRE] §2.8 定理 BH-4 の第 1 段と同一)。
> **(2)** $P=F_2/\gamma_5(F_2)F_2^{\,7}$ は有限 $7$ 群ゆえ $\widehat{F_2}\to P$ は pro-$7$ 完備化 $\mathscr F=F_2^{(7)}$ を経由する。$\gamma_4(\mathscr F)\to\gamma_4(P)$ ゆえ、$f_\sigma\bmod\gamma_4(\mathscr F)\in\mathrm{gr}_3(F_2)\otimes\mathbb Z_7$ の像は $\gamma_3(P)/\gamma_4(P)$ の中で定まる。[C2] cert の測定 `lcs_layer_dims_F7 = [2,1,2,3]`(と `size_P = 7^8`)より
> $$\gamma_3(P)/\gamma_4(P)\ \cong\ \mathrm{gr}_3(F_2)\otimes\mathbb F_7\quad(\dim=2),$$
> したがってこの写像は **mod 7 還元そのもの**である。補題 BR-3 と (4.4) より $f_\sigma\equiv a_\sigma\mathfrak h_3$、$a_\sigma\in\mathbb Z_7^\times$ ゆえ mod 7 で $\ne0$。∎

---

## 6. 算術入力 — [KUR] の鎖(**逐語 pin つき・4 段**)

### 6.1 逐語

**(K1)** [KUR] 印字 230 **COROLLARY 3.8**:
> "For an odd prime $p$, we have $A^{[p-3]}=0$, $A^{[3]}\simeq\mathbf Z_p/L(0,\omega^{-3})\mathbf Z_p$, and $H^2(\mathbf Z[1/p],\mathbf Z_p(k))\simeq\mathbf Z_p/N_k\mathbf Z_p$ for $k\equiv p-3\ (\mathrm{mod}\ p-1)$ and $k>0$."
> "In fact, by [11], $K_4(\mathbf Z)=0$ modulo 2 and 3-torsions. Now, we may assume $p\ne3$ because 3 is a regular prime."
> ⟹ **$A^{[p-3]}=0$ は全奇素数 $p$ で無条件**([11] = Lee–Szczarba)。

**(K2)** [KUR] 印字 226 **COROLLARY 1.5**:
> "For $r\ge2$, $A^{[1-r]}$ is cyclic (resp. zero) if and only if $H^2(\mathbf Z[1/p],\mathbf Z_p(r))$ is cyclic (resp. zero)."

**(K3)** [KUR] 印字 233 §5(c(1) の定義 (4) の直後):
> "Let $C$ be the subgroup of $H^1(\mathbf Z[1/p],\mathbf Z_p(r))$ (topologically) generated by $c(1)$. … Notice that $H^1(\mathbf Z[1/p],\mathbf Z_p(r))$ is a free $\mathbf Z_p$-module of rank 1. In fact, by [16] its rank is equal to 1. Further, since $r$ is odd, $H^0(\mathbf Z[1/p],\mathbf Z/p(r))=0$. This implies $H^1(\mathbf Z[1/p],\mathbf Z_p(r))$ is torsion free. Therefore, $H^1(\mathbf Z[1/p],\mathbf Z_p(r))\simeq\mathbf Z_p$, and $c(1)\ne0$ implies that $C$ is a subgroup of finite index."

**(K4)** [KUR] 印字 233 **PROPOSITION 5.1** + **REMARK 5.2**:
> "For an odd number $r\ge3$, $H^2(\mathbf Z[1/p],\mathbf Z_p(r))$ is finite, and we have $\#H^2(\mathbf Z[1/p],\mathbf Z_p(r))\le\#(H^1(\mathbf Z[1/p],\mathbf Z_p(r))/C)$."
> "(The above inequality is really an equality.)"

**(K5)** [KUR] 印字 231 **REMARK 4.3**(参照用・§7.1 で使う):
> "The above homomorphism $\mathrm{gr}^3\varphi:G_{\mathbf Q(\mu_{p^\infty})}\to\Phi(3)/\Phi(4)$ is unramified outside $p$, and $\Phi(3)/\Phi(4)$ is isomorphic to $\mathbf Z_p(3)$ as a $G_\infty=\mathrm{Gal}(\mathbf Q(\mu_{p^\infty})/\mathbf Q)$-module. … We know that $\mathrm{gr}^3\varphi$ in $H^1(\mathbf Z[1/p],\mathbf Z_p(3))$ coincides with the cyclotomic element of Deligne–Soulé $c(1)$ in Section 5 (4) modulo $\mathbf Z_p^\times$ ([8] Th. B, [3] Th. C). Hence, the surjectivity of $\mathrm{gr}^3\varphi$ corresponds to the fact that the cyclotomic element generates $H^1(\mathbf Z[1/p],\mathbf Z_p(3))$. The latter is also deduced from Proposition 5.1 below and $H^2(\mathbf Z[1/p],\mathbf Z_p(3))=0$."

### 6.2 補題 BR-5(**円分元が $H^1$ を生成する** — [KUR] だけで閉じる)

> ### 補題 BR-5
> 任意の奇素数 $p$ に対し、Deligne–Soulé 円分元 $c(1)$ は $H^1(\mathbb Z[1/p],\mathbb Z_p(3))\cong\mathbb Z_p$ を**生成する**。
>
> **証明.** (K1) より $A^{[p-3]}=0$。$-2\equiv p-3\pmod{p-1}$ ゆえ $A^{[1-3]}=A^{[-2]}=A^{[p-3]}=0$、(K2) を $r=3$ で適用して $H^2(\mathbb Z[1/p],\mathbb Z_p(3))=0$。(K3) より $H^1(\mathbb Z[1/p],\mathbb Z_p(3))\cong\mathbb Z_p$(自由階数 1)。(K4) を $r=3$ で適用して $\#\bigl(H^1/C\bigr)\le\#H^2=1$、すなわち $C=H^1$。∎
>
> ⟹ **$c(1)$ は $p$ で割れない** ⟹ $c(1)$ を $G_{\mathbb Q(\mu_{p^\infty})}\to\mathbb Z_p(3)$ の準同型と見て **全射**。
> (実際、もし像が $p^k\mathbb Z_p$($k\ge1$)なら $c(1)/p^k$ も同じ条件を満たす $H^1$ の元となり $c(1)$ は生成元でない。)

> ★ **独立の傍証(根拠に数えない・出所ラベル)**: $p=7$ では $h(\mathbb Q(\mu_7))=1$ が古典的に知られ、$A=0$ ゆえ $A^{[4]}=0$ は自明に成り立つ。これは (K1) の $p=7$ instance の**整合確認**であって、補題 BR-5 の載荷根拠ではない(載荷は (K1)–(K4))。

### 6.3 補題 BR-6(**正規化** — $\kappa^{(p)}_3$ と $c(1)$)★ **本ノート唯一の残余ギャップ**

> ### 補題 BR-6(【BR-GAP-1】)
> $H^1(\mathbb Z[1/p],\mathbb Z_p(3))$ において
> $$[\kappa^{(p)}_3]\ =\ (\text{unit in }\mathbb Z_p^\times)\cdot[c(1)] .$$
>
> **証明のスケッチ(単系統・自前)。** 両者は同じ「捻れ円分単数の Kummer 類」である。
> - [KUR] §5 (4)(印字 233):$c(1)=\varprojlim_n\mathrm{Cor}_{\mathbb Z[1/p,\mu_{p^n}]/\mathbb Z[1/p]}\bigl[(1-\zeta_{p^n})\otimes\zeta_{p^n}^{\otimes(r-1)}\bigr]$。
> - $\Delta_n=\mathrm{Gal}(\mathbb Q(\mu_{p^n})/\mathbb Q)$、$\tau_a(\zeta)=\zeta^a$。$\mathrm{Cor}=\sum_{a}\tau_a^{-1}$ を Kummer 類に適用すると、$\zeta^{\otimes(r-1)}$ の捻れが $a^{r-1}$ を生み、$b=a^{-1}$ の置換で
> $$\mathrm{Cor}\bigl[(1-\zeta)\otimes\zeta^{\otimes(r-1)}\bigr]=\Bigl[\prod_b(1-\zeta^{b})^{b^{\,r-1}}\Bigr]\otimes\zeta^{\otimes(r-1)} .$$
> - [ICM] §6.2 (ii) の $\varepsilon_{r,n}=\prod_a(\zeta^a_n-1)^{\langle a^{r-1}\rangle}$ は、$\langle a^{r-1}\rangle\equiv a^{r-1}\pmod{p^n}$(Kummer 類は $p^n$ 乗を法とするので指数は mod $p^n$ でよい)、および $(\zeta^a-1)=(-1)(1-\zeta^a)$ で $-1$ が $\mathbb Q(\mu_{p^n})^\times$ の $p^n$ 乗($p$ 奇)であることから、**同じ Kummer 類を与える**。
> - $\kappa^{(p)}_3$ の定義にある $\chi^{1-m}$ 因子は (6.2.1) の cocycle 条件を $\mathbb Z_p(m)$ 係数に合わせるためのもので、$m=3$ で $\mathbb Z_p(3)$ 係数の 1-cocycle を与える(§4.1 (ii))。ゆえに両者は $H^1(\mathbb Z[1/p],\mathbb Z_p(3))$ の同じ元を $\pm1$ の差で与える。∎(スケッチ)
>
> ⚠ **格: paper-proof candidate(単系統・自前・Sol 未監査)。** corestriction の向き($\sum\tau_a$ か $\sum\tau_a^{-1}$ か)と $\langle\cdot\rangle$ の最小正代表の扱いの 2 点が**逐語の確認を要する**。
>
> ★ **独立の支え**: [KUR] **Remark 4.3**((K5))が「$\mathrm{gr}^3\varphi$ は $c(1)$ と $\mathbb Z_p^\times$ を除いて一致する」を **[8] Th. B(Ihara–Kaneko–Yukinari)・[3] Th. C(Coleman)** で主張している。この 2 本はまさに [ICM] §6.3 の Theorem $[A_3,C_3,\mathrm{IKY}]$ の出所であり、**補題 BR-3 と [KUR] Rem 4.3 は同じ定理の二つの読み**である。

---

## 7. ★★ 定理 **BH-BRIDGE**

> ### 定理 BH-BRIDGE
> **前件**: (α) [2405] §1.3 の Ihara 埋め込み(1.5)(1.6)(1.11)–(1.13);(β) [ICM] §6.1/6.3/6.4 の 4 式(§4.1);(γ) [KUR] Cor 3.8 / Cor 1.5 / §5 / Prop 5.1(§6.1);(δ) 補題 BR-6(**【BR-GAP-1】**);(ε) [C2] cert の測定 $\lvert P\rvert=7^8$・LCS $[2,1,2,3]$;(ζ) 補題 BR-1 の規約整合(**【BR-GAP-2】**)。
>
> **主張**: $$\boxed{\ \exists\,\sigma\in G_{\mathbb Q(\mu_{7^\infty})}\subseteq G_{\mathbb Q(\mu_7)}:\quad \mathrm{Ih}_{\mathbf N}(\sigma)\ne1,\qquad\text{すなわち}\quad \mathrm{Ih}_{\mathbf N}\bigl(G_{\mathbb Q(\mu_7)}\bigr)\ne1 .\ }$$
> さらに像の $\mathrm{gr}_3$ 成分は $\mathbb F_7\mathfrak h_3$ の**非零**元である。
>
> **証明.** 補題 BR-5 より $c(1):G_{\mathbb Q(\mu_{7^\infty})}\to\mathbb Z_7(3)$ は全射。補題 BR-6 より $\kappa^{(7)}_3$ も全射。ゆえに $\kappa^{(7)}_3(\sigma)\in\mathbb Z_7^\times$ なる $\sigma\in G_{\mathbb Q(\mu_{7^\infty})}$ が存在する。補題 BR-1 で $f_\sigma$ は正典の $f_g$ と同一、補題 BR-3 と (4.4) より $f_\sigma\equiv a_\sigma\mathfrak h_3\pmod{\gamma_4}$ で $a_\sigma\in\mathbb Z_7^\times$。補題 BR-4 (2) より $\bar f_\sigma\ne1$ in $P$、$\mathbb Q(\mu_7)\subseteq\mathbb Q(\mu_{7^\infty})$ ゆえ $\sigma\in G_{\mathbb Q(\mu_7)}$。∎

### 7.1 ★ **通らなかった道**(Sol への申し送り・**ここが最大の学び**)

[KUR] **Prop 4.2**(「$\mathrm{gr}^3\varphi:G_{\mathbb Q(\mu_{p^\infty})}\to\Phi(3)/\Phi(4)\simeq\mathbb Z_p$ は全射」)を**逐語のまま**使う経路は、**閉じない**。理由:

- $\Phi(3)/\Phi(4)$ は $\mathrm{gr}_3(\mathscr F)\otimes\mathbb Z_p\cong\mathbb Z_p^2$ に単射に入るが、**その像が飽和(= $\mathbb Z_p$-直和因子)であることを [KUR] は述べていない**。
- もし $\Phi(3)/\Phi(4)=p^k\,\mathbb Z_p\mathfrak h_3$($k\ge1$)なら、$\mathrm{gr}^3\varphi$ が「$\Phi(3)/\Phi(4)$ の上に全射」でも、$\mathrm{gr}_3\otimes\mathbb F_7$ への像は**ゼロ**になる。
- さらに Prop 4.2 は「像 $=\Phi(3)/\Phi(4)$」を主張するので、$\Phi(3)/\Phi(4)$ の格子を決めるのは**まさに Galois 像自身**であり、Prop 4.2 単独では循環する。
- $\Phi=Br\,d_2^{(p)}$ の定義は [Ih Annals 1986] p.46 にあり、**当工房は未取得**。

⟹ **本ノートは Prop 4.2 を使わず、[ICM] §6.3 の明示公式(補題 BR-3)で $\mathrm{gr}_3$ の座標を直接押さえ、[KUR] の $H^1$ 側の言明(Cor 3.8 → Cor 1.5 → Prop 5.1)だけを算術入力にした。** これにより $\Phi$ の格子問題を完全に迂回している。

### 7.2 【GAP】と前件表

| 札 | 内容 | 状態・影響 |
|---|---|---|
| ★ **【BR-GAP-1】** | 補題 BR-6($\kappa^{(p)}_3\sim c(1)$ mod $\mathbb Z_p^\times$)。**本ノート唯一の真の残余** | **paper-proof candidate**(自前スケッチ・単系統)。[KUR] Rem 4.3 が同値な主張を [8]/[3] で述べているのが支え。**逐語確認 2 点**(corestriction の向き・$\langle a^{m-1}\rangle$)が残る ⟹ **【文献要請 BH-L2】**(§9.2) |
| **【BR-GAP-2】** | 補題 BR-1 の生成対同一視。$\tau$ 型は式の形で排除、$\theta$ 型は $\mathbb Z\mathfrak h_3$ を保つので無害。残るは inner 型微調整 | **軽微**(結論の非消滅に影響しない・§2) |
| **【BR-GAP-3】** | [C2] cert の $\lvert P\rvert=7^8$・LCS $[2,1,2,3]$ は**単系統**(CV-9 判読未経由) | 測定依存。補題 BR-4 (2) の前件 |
| **【BR-GAP-4】** | [ICM] §6.3 の Theorem 本体は**引用**であり本ノートは再証明しない([$A_3$, $C_3$, IKY]) | 正典内の公刊定理。**再導出の予定なし** |
| — | $\Phi=Br\,d_2^{(p)}$ の定義(p.46)・Th.6 | **不要になった**(§7.1) |

> ★ **重要な会計**: 委嘱が想定した「B₄→B₃ 翻訳」は**存在しない**(裁定 578)。実際に必要だったのは「**副有限フィルトレーション $\Phi(m)$ を経由せず、$\mathrm{gr}_3$ の明示係数で有限窓へ降ろす**」という別種の翻訳であり、その道具は**正典 [ICM] §6 に既にあった**。

> ★ **[PRE] 側の GAP の現況**(参考): [PRE] §7.2 の【BH-GAP-2】($L$ の $\Phi$-不変性)と【PL-GAP-1】($H_W$ の部分群性)は **[J0J2] の測定で CLOSED**(§8.2.2)。【BH-GAP-1】((J3) の 1 ビット)を埋めるのが本ノートである。【BH-GAP-3】($H_W\setminus\mathfrak G_{\rm ar}$ の内訳)は原理的 UNKNOWN のまま — 本ノートは触れない。

### 7.3 格付け

| 対象 | 格 |
|---|---|
| 補題 **BR-1 / BR-2 / BR-2′** | **paper-proof**(引用+初等) |
| 補題 **BR-3**(深さ 3 係数公式) | ★ **paper-proof candidate**(自前・[ICM] の 4 式からの導出・**付録 A で機械検算**・Sol 未監査) |
| 補題 **BR-4** | **paper-proof candidate**(measurement-relative: [C2]) |
| 補題 **BR-5** | ★ **paper-proof**([KUR] の 4 定理の合成のみ・自前の新段なし) |
| 補題 **BR-6** | ⚠ **paper-proof candidate(スケッチ)** = **【BR-GAP-1】** |
| **定理 BH-BRIDGE** | ★ **paper-proof candidate**(前件 = §7.2 の表・**【BR-GAP-1】相対**) |
| `cross-checked` / `verified` | ✗ どちらも付かない |
| novelty | **主張しない**(§0-5) |

---

## 8. 帰結と ★ 新規予言(**IF-FIRST 登録候補**)

### 8.1 [PRE] への接続(一行の帰結)

定理 BH-BRIDGE は [PRE] §2.8 **定理 BH-4** の前件をちょうど満たす:
$$\mathrm{Ih}_{\mathbf N}(G_{\mathbb Q(\mu_7)})\ne1\ \overset{\text{BH-4}}{\Longrightarrow}\ \mathfrak G_{\rm ar}\cap A=L\ \overset{\text{SUP-4}}{\Longrightarrow}\ L=L_3\ \overset{\text{BH-1}}{\Longrightarrow}\ \mathfrak G_{\rm ar}=H_W .$$

> $$\boxed{\ \textbf{BH-1 の二値 + BH-BRIDGE}\ \Longrightarrow\ \mathrm{GT}^{\rm arith}(\mathbf N)=H_W,\ \lvert\mathrm{GT}^{\rm arith}(\mathbf N)\rvert=42\ \Longrightarrow\ \mathcal B=\emptyset\ =\ \textbf{BH-α(非算術証人ゼロ)確定候補}.\ }$$
> **発効は Sol 監査後(便 109)。** [PRE] §6.5 の「的中しても言えないこと」5 項はすべてそのまま生きる(とくに「42 個が genuine」は**言えない**)。

### 8.2 ★ 既走 (J1′) 測定との整合(**予言ではない — 時系列を正直に**)

#### 8.2.1 時系列の申告(**最重要・格付けの根拠**)

> $$\boxed{\ \textbf{(J1′) の測定は本ノートの導出に}\textbf{先行}\textbf{する。裁定 575 で既走(cert [J0J2])。}\ }$$
> ゆえに以下は **IF-FIRST 予言ではなく、「独立に立てた導出が既存の測定と合った」という整合の記帳**である。**事前登録とは呼ばない。**
> (起草者は本委嘱の作業中に「(J1′) は $\Phi(L)=L$ を出すはず」という予想を立てたが、司令塔から既走 cert の存在を知らされた。**予想の格上げはしない。**)

#### 8.2.2 測定値と、本補題との 3 点の整合

[J0J2] cert の該当欄(**構造欄のみ参照・key 値は読んでいない**):

| cert 欄 | 値 |
|---|---|
| `J1prime_Phi.m0` | $1$(⟹ 生成層 $u_0=2m_0+1=3$、$(\mathbb Z/7)^\times$ の生成元) |
| `J1prime_Phi.phi_invariant_Phi_L_equals_L` | `true` |
| `J1prime_Phi.phi_images` | $\Phi$ は $L$ 上 **$-1$ 倍**(例: $e$-ベクトル $[0,1,1,6,6,6]\mapsto[0,6,6,1,1,1]$) |
| `BH5_branch.phi_invariant` | `true`(⟹ 系 **BH-5** は**発火しない**) |

**整合 (i) — 系 BH-5 が発火しないこと。** [PRE] 系 BH-5 は「$L$ が $\Phi$-不変でない $\Rightarrow\ \mathfrak G_{\rm ar}=\mathcal C$(位数 6)」という**片側検出器**である。測定は $\Phi(L)=L$ を出したので **BH-5 は発火せず**、$\lvert\mathfrak G_{\rm ar}\rvert\in\{6,42\}$ の 1 ビットはそのまま残った。定理 BH-BRIDGE と**矛盾しない**(もし $\Phi(L)\ne L$ が出ていたら正面衝突していた)。

**整合 (ii) ★★ — $-1$ 作用が $\mathrm{gr}_3$ を名指しする(本ノートで最も強い裏取り)。**
[PRE] 補題 SUP-4 は $\Phi$ が $L_3$(gr₃ 側)に $u^3$、$L_4$(gr₄ 側)に $u^4$ で作用すると言う。$u_0=3$ で
$$u_0^{\,3}=27\equiv 6\equiv-1,\qquad u_0^{\,4}=81\equiv 4\not\equiv-1\pmod 7$$
(付録 A (12) で機械確認)。**測定された $-1$ は $u^3$ に一致し $u^4$ には一致しない** ⟹ **$L=L_3$ が実測で確定**する。
一方、算術側は完全に独立に同じことを言っている: [KUR] Remark 4.3 逐語「$\Phi(3)/\Phi(4)$ **is isomorphic to $\mathbf Z_p(3)$** as a $G_\infty$-module」 — すなわち Galois の $\mathrm{gr}_3$ 直線は **Tate 捻り 3**。窓側の $\chi_{\rm vir}=u$ と $\chi$ は (1.13) で同一視されるから、**「Tate 捻り 3」= 「窓の $u^3$ 作用」= 「測定された $-1$」**。
> ⟹ 本補題が「窓の $A$ の中で $\mathrm{gr}_3$ 成分を名指ししている」ことが、**窓側の実測から裏取りされた**。これは §2 の規約整合(補題 BR-1)と §4 の座標(補題 BR-3)が正しい対象を指していることの、$[\mathrm{ICM}]$ とも $[\mathrm{KUR}]$ とも独立な第 3 の証拠である。

**整合 (iii) — 【BH-GAP-2】は測定で CLOSED。** [PRE] §7.2 の【BH-GAP-2】($L$ の $\Phi$-不変性が未測定)は [J0J2] で閉じている。したがって**残っていた唯一の未決は (J3) の 1 ビットのみ**であり、定理 BH-BRIDGE がそれを埋める。

#### 8.2.3 反証の所在(**過大評価の防止**)

本補題が誤りであるとすれば、破れ得るのは次の順序である:

1. ★ **【BR-GAP-1】(補題 BR-6 の正規化)** — $\kappa^{(7)}_3$ と $c(1)$ が $7^k$($k\ge1$)ずれていれば、$a_\sigma\in7\mathbb Z_7$ となり像は窓で消え、**結論は BH-β(B 型候補 36 個)へ反転する**。⟹ §9.2 の【文献要請 BH-L2】が指すのはここ。
2. **【BR-GAP-2】** — 生成対同一視の inner 型微調整(§2 で $\tau$ 型は排除・$\theta$ 型は無害と論じた)。
3. **【BR-GAP-3】** — [C2] cert の $\lvert P\rvert=7^8$・LCS $[2,1,2,3]$(単系統)。

⚠ **どの場合も「古典算術の言明を覆した」とは読まない。** [PRE] §6.2 の警報規律(BH-γ 着地時は翻訳の忠実性を先に疑う)を、本補題の側にもそのまま適用する。

---

## 9. Sol への監査点 と 【文献要請】

### 9.1 監査点(4 点)

> **R-1 ★★ 補題 BR-3 の (b)(c)(d)**(§4.2)。とくに **(4.2) $B'_\sigma=1+(\underline x-1)(\underline y-1)h$** の導出(自由群の恒等式 $[x,yc]=[x,y]\cdot y[x,c]y^{-1}$ と $\theta_c=(1-\underline y^{-1})\theta_f$、$\theta_{[x,c]}=(\underline x-1)\theta_c$)。**ここが本補題の全体を支えている。** 付録 A (3) が 7 例で機械確認しているが、**一般の $f$ に対する紙の証明**を認めるか。
>
> **R-2 ★★ 【BR-GAP-1】= 補題 BR-6**(§6.3)。$\kappa^{(p)}_3$([ICM] §6.2 (ii))と $c(1)$([KUR] §5 (4))が $\mathbb Z_p^\times$ 倍で一致することの証明スケッチ(corestriction ↔ 捻れ積)。**逐語確認が要る 2 点**(corestriction の向き・$\langle a^{m-1}\rangle$ の最小正代表)を含めて判定を請う。**ここが唯一の残余。**
>
> **R-3 ★ §7.1 の「通らなかった道」**。[KUR] Prop 4.2 を逐語で使うと $\Phi(3)/\Phi(4)$ の飽和性が要る、という診断は正しいか。もし Sol が「Prop 4.2 の $\simeq\mathbb Z_p$ は飽和を含意する」と読むなら、その根拠を示してほしい(そうなら【BR-GAP-1】は第 2 経路で閉じる)。
>
> **R-4 ★ 補題 BR-1 の規約排除**(§2)。「$\tau$ 型のずれは式の形が排除する」($f_\sigma$ が $y^\chi$ と可換になる矛盾)という論法に穴はないか。また $\theta$ 型が $\mathbb Z\mathfrak h_3$ を保つ(ゆえに無害)という会計を認めるか。
>
> ★ **教材メモ(Sol への共有)**: 補題 BR-3 は **$a=b$(= [HS7] 定理 D3-BLIND (b))を独立に再導出する**。一方は $K(0,5)$ 側の線型代数、他方は Anderson–Coleman–IKY の明示公式。**別系統の二つが同じ 1 次元性を出した**ことは、規約(生成対・$\theta$・bracket)が両側で整合していることの実質的な裏取りである。

### 9.2 【文献要請 **BH-L2**】(**小さい・限定的**)

- **具体的な技術的困難**: 【BR-GAP-1】= 補題 BR-6。Ihara [ICM] §6.2 (ii) の $\kappa^{(p)}_m$ と Kurihara §5 (4) の Deligne–Soulé 円分元 $c(1)$ が、$H^1(\mathbb Z[1/p],\mathbb Z_p(m))$ で **$\mathbb Z_p^\times$ 倍を除いて**一致すること。**「非零倍」では足りない — 単元倍でなければ mod 7 で結論が反転する。**
- **欲しい結果の型**: 「Soulé 円分元の二つの標準的構成(円分単数の捻れ積による Kummer 類 / corestriction による構成)が $H^1(\mathbb Z[1/p],\mathbb Z_p(r))$ で $\mathbb Z_p^\times$ を除いて一致する」を明示する一節。または **Ihara–Kaneko–Yukinari [IKY] Th. B / Coleman Th. C の正規化つきの言明**。
- ★ **本命候補は司令塔が既に特定済み(裁定 578 の②)**:
  **C1 = H. Ichimura, K. Sakaguchi, "The Non-Vanishing of a Certain Kummer Character $\chi_m$ (after C. Soulé), and Some Related Topics", Adv. Stud. Pure Math. 12 (1987) 53–64**(DOI `10.2969/aspm/01210053`・Project Euclid Open Access)。
  遠征係の OCR 読解によれば §3-1 Prop 1 (i)(iii)(Coleman–Ihara の $L$ 値等式)と §3-3 Prop 4 + Cor が【BR-GAP-1】の**第三の支え**になる。
  ⚠ **取得は環境で詰まっている**(Project Euclid が Imperva/Incapsula の bot 保護を返す。curl 4 経路・WebFetch とも `200 text/html` の 1 KB チャレンジ頁)。**速達 `ops/express/20260806-060000_math_c1_projecteuclid_blocked.md` を起票済み**(ブラウザ経由での配達を依頼)。
- **不要なもの**: pentagon 側・dihedral 側・$\Phi=Br\,d_2^{(p)}$ の定義(§7.1 で不要になった)。
- **代替(= 現状)**: C1 なしでも **定理 BH-BRIDGE は【BR-GAP-1】相対で成立**しており、[PRE] の分岐 BH-α を条件つきで指す。**C1 が入れば §6.3 の格が単系統 → 二系統に上がる**が、便 109 の発送を待たせる必要はない。**発効判定は司令塔・Sol の裁定に委ねる。**

> ### 補足: 司令塔が同時配達した入口資料
> `papers/ghate-vandiver-via-Ktheory-survey.pdf`(Vandiver 予想と $K$ 理論の解説)。本ノートは**これを載荷根拠に使っていない**([KUR] の逐語だけで §6.2 が閉じるため)。$A^{[p-3]}=0$ の背景理解用として記録に留める。

---

## 10. 規律申告

- ★ **新規の窓計算ゼロ。** GAP も pc 群も起動していない。機械は付録 A の python(Fox 微分・整数/Laurent 演算)のみで、**42 個の candidate key の値は 1 個も読んでいない**。cert から参照したのは次の**構造欄・公開層指標のみ**: [C2] の `size_P`・`lcs_layer_dims_F7`;[J0J2] の `J1prime_Phi.m0`(= 1、公開の層 index)・`phi_invariant_Phi_L_equals_L`・`BH5_branch.phi_invariant`、および $\Phi$ が $L$ 上 $-1$ 倍であるという**作用の形**。
- **検算は cert 化した**([FOX]・30/30 PASS・schema `bhbridge-foxcheck/v1`)。本文の数値はすべて cert からの機械コピーで、**手写しゼロ**。
- **文献取得の記録(正直な申告)**: 司令塔の裁定 578 ②の明示指示により **C1(Ichimura–Sakaguchi ASPM 12・DOI `10.2969/aspm/01210053`)の取得を 4 経路試み、すべて bot 保護で失敗**(§9.2)。それ以外の**自発的な文献検索はゼロ**。[KUR] は司令塔配達分、[ICM]・[2405] は既在の正典。
- **封印 3 量非接触**($n=5$ 系・$\mathrm{Im}\,R$・$d_N$・genuine 層の $u$ 値・PSL 量・$\varepsilon$ bits)。本ノートの $\kappa$・$\kappa^*$・$c(1)$・$C$ はすべて数論側の記号で、封印語彙との衝突はない(grep 済)。**$\mathfrak h_3$ は Lie 元、$h$ は $\mathscr F'/\mathscr F''$ の座標**で、群元 $h_4$(DUM-FIN)とは別物 — 規約台帳 §1.3.10 の分離を遵守。
- **文献**: [KUR] は**司令塔が文献ゲートで降ろした 1 本**であり、自分では検索していない(numdam から取得のみ)。[ICM] は既在の正典。**新しい外部文献の探索はゼロ。**【文献要請 BH-L2】を起票した。
- **既存文書は 1 バイトも改変していない**([PRE] の IF-FIRST 凍結を保全。§8.2 の予言は本ノート(新規ファイル)に登録)。
- 数値・検算結果は**すべて機械生成**(付録 A の出力を転記・手写しゼロ)。原文引用は**すべて 220–300 dpi の頁画像で照合**(OCR テキストは補助のみ)。

---

## 付録 A. 独立検算(`scratchpad/bhbridge_check.py`・**窓非接触**・整数/Laurent 演算のみ)

**方法**: 自由群 $F_2=\langle x,y\rangle$ 上の **Fox 微分**を $\mathbb Z[\mathscr F^{\rm ab}]=\mathbb Z[X^{\pm1},Y^{\pm1}]$ に値を取って厳密計算する。$w\in\mathscr F'$ に対し Fox 対は $(\partial w/\partial x,\partial w/\partial y)=(-(Y-1)h,\ (X-1)h)$ の形で、この $h$ が $\mathscr F'/\mathscr F''=\mathbb Z[\mathscr F^{\rm ab}]\theta'$ における座標である($h(\theta')=1$)。両式(割り切れと syzygy)を毎回 assert している。

> ### ★ cert 化(**手写し禁止規律の遵守**)
> 本検算は **cert [FOX] = `search/certs/bhbridge_foxcheck_20260806.json`**(schema `bhbridge-foxcheck/v1`)として機械記録した。
> - cert SHA-256 = `1e3c4ac0294cb96c3fe2fadb907c622049ffed2990d9f1d738ebc5e749ccde71`
> - script `scratchpad/bhbridge_check.py` SHA-256 = `c2773a64696636054772273ceb2bb28b244e438e53b56a9a5dbca3f691afa299`
> - **判定行 30 / PASS 30 / FAIL 0**(`results.all_pass = true`)
> - cert の `stdout` 欄は下記出力の**機械生成コピー**であり、以下の転記は cert から取った(手写しゼロ)。
> - cert は `discipline` 欄で `window_contact:false`・`candidate_keys_read:0`・`sealed_quantities_contacted:false`・`gap_invoked:false` を自己申告している。

```
=== BH-BRIDGE independent check (exact integer/Laurent arithmetic) ===
(1) h([x,y])            = {(0, 0): 1}  expect {(0,0):1} : True
(2) h([[x,y],x])        = {(1, 0): -1, (0, 0): 1}  expect -(X-1)      : True
    h([[x,y],y])        = {(0, 1): -1, (0, 0): 1}  expect -(Y-1)      : True
(3) f=[[x,y],x]            h([x,f^-1yf]) == 1+(X-1)(Y-1)h(f) : True
(3) f=[[x,y],y]            h([x,f^-1yf]) == 1+(X-1)(Y-1)h(f) : True
(3) f=[[x,y],x]*[[x,y],y]  h([x,f^-1yf]) == 1+(X-1)(Y-1)h(f) : True
(3) f=[x,y]                h([x,f^-1yf]) == 1+(X-1)(Y-1)h(f) : True
(3) f=[[x,y],x]^-1         h([x,f^-1yf]) == 1+(X-1)(Y-1)h(f) : True
(3) f=[x,y]*[[x,y],y]^2    h([x,f^-1yf]) == 1+(X-1)(Y-1)h(f) : True
(3) f=[[[x,y],x],y]        h([x,f^-1yf]) == 1+(X-1)(Y-1)h(f) : True
(3) KEY IDENTITY all cases: True
(4) h(theta(u1)) = {(0, 1): 1, (0, 0): -1}  expect +(Y-1) (= class -u2): True
    h(theta(u2)) = {(1, 0): 1, (0, 0): -1}  expect +(X-1) (= class -u1): True
(5) gcd of coords of h_3=(1,1): 1 -> primitive: True
(6) 2 (from (X+Y)^3-X^3-Y^3 = 3XY(X+Y), /3!)       mod 7 = 2  unit: True
(6) p^2-1 = 48 (Ihara kappa* normaliser)           mod 7 = 6  unit: True
(6) 2*(p^2-1) = 96                                 mod 7 = 5  unit: True
--- xi,eta coordinates ---
(7) pr h(u1) = {(1, 0): -1}  expect -xi  : True
    pr h(u2) = {(0, 1): -1}  expect -eta : True
(8) gamma_4 words: xi-order of pr h(v_i) = [2, 2, 2]  all >=2 : True
(9) Hall  h([[[x,y],y],x]) == h([[[x,y],x],y]) : True
--- end-to-end degree-3 coefficient ---
(10) f=u1^1 u2^0 : deg2={} deg3={(2, 1): -1} expect {(2, 1): -1} : True
(10) f=u1^0 u2^1 : deg2={} deg3={(1, 2): -1} expect {(1, 2): -1} : True
(10) f=u1^1 u2^1 : deg2={} deg3={(2, 1): -1, (1, 2): -1} expect {(2, 1): -1, (1, 2): -1} : True
(10) f=u1^2 u2^3 : deg2={} deg3={(2, 1): -2, (1, 2): -3} expect {(2, 1): -2, (1, 2): -3} : True
(10) f=u1^-1 u2^4 : deg2={} deg3={(2, 1): 1, (1, 2): -4} expect {(2, 1): 1, (1, 2): -4} : True
(10) END-TO-END all cases: True
(11) => matching 1+xi*eta*pr(h_f) with psi^ab = 1 + (k*_3/2)(xi^2 eta + xi eta^2)
     gives  a = b = -k*_3(sigma)/2 .  (a=b falls out, independent re-derivation of D3-BLIND(b))
--- consistency with measured Phi|_L = -1 (cert bhunt_j0j2_20260806) ---
(12) u0=3 : u0^3 mod 7 = 6 , u0^4 mod 7 = 4 , -1 mod 7 = 6
     measured -1 equals u0^3 (gr_3 line) : True
     measured -1 differs from u0^4 (gr_4 line) : True
     => L = L_3 ; the Galois gr_3 line carries Tate twist 3, matching KUR Rem 4.3 (Phi(3)/Phi(4) = Z_p(3)) : True
```

**各行の対応**

| 行 | 検証した命題 |
|---|---|
| (1)(2)(7) | 補題 BR-3 (c) の座標:$h(\theta')=1$、$h(u_1)=-(X-1)\mapsto-\xi$、$h(u_2)=-(Y-1)\mapsto-\eta$ |
| **(3)** | ★ **補題 BR-3 (b) の恒等式 (4.2)** — 7 例(斉次・非斉次・逆元・$\gamma_4$ 元)すべて PASS |
| (4) | $\theta$ の $\mathrm{gr}_3$ 作用($u_1\mapsto-u_2$, $u_2\mapsto-u_1$)= [HS7] D3-BLIND (b) の入力と一致 |
| (5) | 補題 BR-2(飽和性) |
| (6) | §4.3 の $p=7$ 単元性($2$, $48$, $96$ がすべて $7$ の単元) |
| (8)(9) | $\gamma_4$ 元は $\mathrm{pr}\,h$ の次数 $\ge2$(深さ 3 の読み取りを乱さない)/ Hall 関係 |
| **(10)** | ★ **端から端まで**: $f=u_1^au_2^b$ に対し $\mathrm{pr}(B'_\sigma)$ の次数 2 が空・次数 3 が $-a\xi^2\eta-b\xi\eta^2$ |
| (11) | (4.1) との係数比較 ⟹ $a=b=-\kappa^*_3(\sigma)/2$ |
| **(12)** | ★ §8.2.2 整合 (ii):$u_0^3\equiv-1$、$u_0^4\equiv4$ ⟹ 実測の $\Phi\vert_L=-1$ は $\mathrm{gr}_3$ を名指しする(cert [J0J2] の公開層指標 $u_0=3$ のみ参照・key 値は読んでいない) |

⚠ **検算の限界(正直な申告)**: これは **1 系統の python** であり `cross-checked` ではない。また (3)(10) は**有限個の $f$ での確認**であって、一般の $f$ に対する証明は §4.2 (b)(c) の紙(手計算)である。

---

## 付録 B. 使用した逐語引用の一覧(頁 pin)

| # | 出所 | 頁 | 内容 |
|---|---|---|---|
| B-1 | [KUR] | 印字 230 | COROLLARY 3.8(+ "we may assume $p\ne3$ because 3 is a regular prime") |
| B-2 | [KUR] | 印字 226 | COROLLARY 1.5 |
| B-3 | [KUR] | 印字 231 | §4 (2) 冒頭($X=\mathbb P^1\setminus\{0,1,\infty\}$・$\mathscr F$ = 階数 2 自由 pro-$p$ 群)★ 委嘱前提の訂正根拠 |
| B-4 | [KUR] | 印字 231 | フィルトレーション($\Phi(m)$ は $\mathscr F$ の下中心列で定義・$\Phi(1)=\Phi(2)=\Phi(3)$)/ PROPOSITION 4.2 / REMARK 4.3 |
| B-5 | [KUR] | 印字 233 | §5 (4)($c(\eta)$ の定義)/ $H^1\cong\mathbb Z_p$ の段 / PROPOSITION 5.1 / REMARK 5.2 |
| B-6 | [ICM] | 印字 106(PDF 194) | (2.3.1)(2.3.2)+特徴づけ+複素共役 |
| B-7 | [ICM] | 印字 112(PDF 200) | §5.2("unramified outside $l$") |
| B-8 | [ICM] | 印字 114(PDF 202) | §6.1($\mathscr A$・(6.1.1)・$\psi_\sigma$ の定義・$f^{\rm nil}_\sigma=\psi_\sigma(\eta,\xi)\psi_\sigma(\xi,\eta)^{-1}$・$\psi^{\rm ab}$) |
| B-9 | [ICM] | 印字 115(PDF 203) | §6.2 (ii)(κ の定義と構成・(6.2.1))/ §6.3(κ\* と Theorem $[A_3,C_3,\mathrm{IKY}]$) |
| B-10 | [ICM] | 印字 116(PDF 204) | $b_m$ の定義 / §6.4((6.4.1)–(6.4.4)) |
| B-11 | [2405] | §1.1 / §1.3 / §1.3.1 | $PB_3=\langle x_{12},x_{23}\rangle\times\langle c\rangle$ / (1.3)(1.5)(1.6)(1.7) / (1.9)–(1.13) |

**画像照合記録**: [KUR] は PDF 頁 5, 9, 10, 11, 12(= 印字 226, 230, 231, 232, 233)を 220 dpi で、[ICM] は PDF 頁 202, 203, 204(= 印字 114, 115, 116)を 300 dpi で描画して照合した(`scratchpad/bhbridge_img/`)。[ICM] の頁対応(印字 = PDF − 88)は既在の読解ノートで確定済み。
