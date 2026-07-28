# 等号問題 $\ker\widetilde\chi=[\operatorname{GT}(N),\operatorname{GT}(N)]$ — 一般判定条件・dihedral 族での定理・**atlas 内の反例** **v2**

**状態札: candidate(裁定前・未 commit)**
起草: Claude(数学者レイヤー・Opus 5)/ v1 = 2026-07-29 / **v2 = 2026-07-29(便 79 検収・裁定 170 の修理波)/ v2.1 = 2026-07-29(裁定 173 追補: §11 $\chi$-退化窓・予想 KE-P の反証)**
設問: 司令塔委嘱(便 79 検分材料)/ `docs/notes/w2fam_v1.md`(dihedral 族での等号)の一般化
**v2 の依拠(追加)**: `sol/sol_reply_79_math6.md` **F79-2.1 / F79-2.2 / F79-2.3 / F79-2.5 / F79-2.6 / P79-A / P79-B**、`search/certs/derived_census_v2_20260729.json`(census v2)。
正典・依拠(v1 から継承):
- `docs/week1-定義ノート.md` §3(GT-pair Def 3.1・charming・合成 (3.53)・(3.49)・逆元 (3.54)・$\chi_{\rm vir}$・$N_{\rm ord}$ (3.1))、§(isolated の定義: 2401 Def 3.13 直後・Prop 3.14)
- 正典 arXiv **2405.11725**: §1.3 Ihara 準同型・$\operatorname{Ih}(g)=((\chi(g)-1)/2,f_g)$・図式 (1.10)(1.13)・**Remark 1.3**(全射性の唯一の証明経路)・**Remark 1.4**(非 isolated では $\operatorname{Ih}_N$ は準同型でない)・**Thm 4.6** (4.23)(4.24)・Cor 5.4
- 正典 arXiv **2401.06870**: Def 3.13(isolated)・**Thm 4.3**($K^{(n)}$ は isolated)・Thm 5.2
- `docs/notes/w2fam_v1.md` / `docs/notes/oddH_full_proof_v1.md` §11.1 / `provenance/registered/universe_wall_v1.md`
- 外部文献なし。群論的入力は **有限アーベル群の Schur 乗数 $H_2(A)=\Lambda^2A$**、**LHS 5 項完全列**、**Maschke** のみ(すべて標準)。

> ## 封印遵守
> **$u$・封印 3 量($u_9/a_9$ の値・$c$ の平方類・$\hat c_\mu$)に一切触れていない。** 本稿は純粋に有限群論であり、算術的入力は「円分指標 $\chi:G_{\mathbf Q}\to\widehat{\mathbf Z}^\times$ が全射」ただ一つ(§2 (AR))。
> ## C2F 遵守
> **$\Phi$ の商群上の像で数えていない。** 全ての測定は **shadow(GT-pair)水準の合成表**((3.53) で構成)を入力とし、スクリプトは「表が (3.53) の第一成分 $2m_1m_2+m_1+m_2$ を再現するか」を fail-closed assert で検査してから測っている(裁定 147・宇宙登録 v1.1 (2b))。§6.3 で新たに使う census v2 の `group_order` / `derived_length_of_group` も **(3.53) 合成表の正則表現から**得られており、$\Phi$ 像ではない(証明書の `schema_note` に明記)。

---

## 0. v2 errata — v1 からの変更一覧(この節が本改訂の要旨)

| # | 箇所 | v1 の記述 | v2 の処置 | 根拠 |
|---|---|---|---|---|
| **E1** | **T-A(4)(5)** | 「$\widetilde\chi_{2M}$ は**全ての** $N$ で全射」「$|\mathfrak F_0|=|\operatorname{GT}(N)|/\varphi(2N_{\rm ord})$」 | **型ゲートを挿入**。全射は **isolated $N$**(または独立な全射証明書のある窓)に限定。**普遍形は $|\mathfrak F_0|\cdot|Q_N|=|G_N|$**($Q_N:=\operatorname{Im}\widetilde\chi$) | **F79-2.1**。非 isolated $N$ では $\operatorname{PR}_N\circ\operatorname{Ih}$ の source が $N$ とは限らず、$\operatorname{Ih}_N(g)$ が isotropy 群 $GTSh(N,N)$ の元である保証がない(2401 Thm 5.2 証明冒頭 / 2405 Remark 1.4) |
| **E2** | **T-B** | $Q=(\mathbf Z/2M)^\times$ | $Q_N=\operatorname{Im}\widetilde\chi$ へ差し替え(証明は逐語同じ) | F79-2.2(この形で PASS) |
| **E3** | **T-G の系** | 「**反例は $|\mathfrak F_0|$ 非素数の窓にしか存在しない**」 | **削除**。補題 P は残すが、系は**偽**。$G=C_p\times Q\to Q$ が反例 | **F79-2.5** |
| **E4** | **§7.5 priority 0** | 「$|\mathfrak F_0|$ が素数または 1 の窓は反例になりえない ⟹ まずこれで篩う」 | **削除**。素数核の窓は**除外**ではなく**最安の反例候補**(可換なら必ず反例)。優先度表を組み直した(§7.5 v2) | F79-2.5 |
| **E5** | **§6 atlas 決着表** | $N_3$ = **UNKNOWN** | **$N_3$ は等号成立**($|\mathfrak F_0|=2$ 素数 + census v2 で**本体**の導来長 2 = 非可換 + 補題 P)。$M_3$ は UNKNOWN 継続 | **F79-2.6**・census v2 |
| **E6** | **§5.2** | 「$Q$-固定な一次元部分群があるから $Q$-自明な商がある」 | **Maschke の一行を挿入**($|Q|=4$ と標数 3 が互いに素 ⟹ $\mathbf F_3[Q]$-加群は半単純 ⟹ 固定直線は $Q$-安定補空間をもつ ⟹ $Q$-同変な全射 $\mathfrak F_0^{\rm ab}\twoheadrightarrow\langle g_1\rangle$) | **F79-2.3** |
| **E7** | **§5.2 の呼称** | 「独立な **a priori** 証明(実測に依存しない)」 | 「**理論機構+有限データの組合せ**による証明」へ改称。重み 2 の生存機構は理論的だが、$\mathfrak F_0^{\rm ab}\cong C_3^2$ の具体構造と中心方向の同定には登録証明書を使っている | F79-2.3 |
| **E8** | **§7.3 TIER-1.5** | 名称 TIER-1.5 | **`KERNEL-DL3` / `KERNEL-NONMETABELIAN` を正式名として併記**(意味を直接表す) | F79-2.6 |
| **E9** | **§7.4 掃引 assert** | `|ker_chi| * phi_2Nord == |GT|` を無条件 fail-closed | **二段に分離**。普遍 assert は `|ker_chi| * chi_image_order == |G_N|`、`chi_image_order == phi(2*N_ord)` は `is_isolated` または `chi_surjectivity_cert` のある窓でのみ発火 | F79-2.1・**P79-A** |
| **E10** | **新設 §3.2** | — | 補題 P の正しい読み(「非可換性の一ビット判定器」)+ **予想 KE-P**(可換 GT ⟹ $\widetilde\chi$ 単射)の提示と atlas 3 窓の支持。これが立てば E3 で失った篩が限定版で復活する | F79-2.5 の「追加定理が将来立てば限定版は救える」への応答 |

**v1 は `docs/notes/kerchi_equality_v1.md` としてそのまま残す**(上書きしていない)。v1 を引用している下流文書は、上表の 10 点について本稿を正本とすること。

---

## 1. 結論(要旨・v2)

**問いへの答は NO(一般には成り立たない)。** 判定条件は完全に付き、既存の主線は無傷である。

| # | 主張 | 状態(v2) |
|---|---|---|
| **T-A** | $\widetilde\chi_{2M}:\operatorname{GT}(N)\to(\mathbf Z/2M)^\times$、$[m,f]\mapsto2m+1$ は**任意の $N$ で** well-defined な準同型で $\ker=\mathfrak F_0$。**普遍個数等式** $|\mathfrak F_0|\cdot|Q_N|=|\operatorname{GT}(N)|$。**全射($Q_N=(\mathbf Z/2M)^\times$)は isolated $N$ で (AR) の下**、一般には**証明書が要る** | **証明**(1,2,3,5 は純群論・4′ は (AR)+isolated)。**25 窓で実測一致・不一致ゼロ**(= その 25 窓の regression) |
| **T-B** | **判定条件(完全)**: $\ker\widetilde\chi/[\operatorname{GT},\operatorname{GT}]\cong\operatorname{coker}\bigl(\Lambda^2Q_N\xrightarrow{\rm tg}(\mathfrak F_0^{\rm ab})_{Q_N}\bigr)$ | **証明**(LHS 5 項完全列) |
| **T-C** | **dihedral 族では等号が成立 — 全ての $n\ge3$** | **証明**($K^{(n)}$ は **isolated**(正典 Thm 4.3)なので T-A(4′) が使える)。**16 証明書で cross-checked** |
| **T-D** | **等号は一般には偽。反例は登録 atlas の中にある: $L=K^{(3)}\cap N_0$** — 指数 3 | **実測(cross-checked 証明書・$\widetilde\chi$ の全射も実測)+ 理論機構と有限データを組み合わせた証明**(§5.2) |
| **T-E** | 反例の**機構**: $\Phi_{m,f}$ は abelianization に重み $u$、$\gamma_2/\gamma_3$ に**重み $u^2$** で作用。$u^2\equiv1$ となる層($e\mid24$)は GT-不変 | **証明**(§5.3 命題 W2) |
| **T-F** | **壁ソルバーへの帰結**: TIER-0 無傷 / TIER-1 の昇格は窓ごとの等号証明書が要る / **`KERNEL-DL3` は等号不要で非 metabelian を確定** | §7 |
| **T-G** | **補題 P**: $|\mathfrak F_0|$ が素数なら「等号 $\iff\operatorname{GT}(N)$ 非可換」。**~~反例は非素数核の窓にしかない~~(削除・E3)**。正しい読みは「**非可換性の一ビット判定器**」 | 補題は**証明**。**系は撤回**(F79-2.5) |

---

## 2. 一般設定と T-A(v2)

$N\in\mathrm{NFI}_{PB_3}(B_3)$、$M:=N_{\rm ord}=\operatorname{lcm}(\operatorname{ord}(xN),\operatorname{ord}(yN),\operatorname{ord}(cN))$(定義ノート (3.1))。GT-pair は $[m,f]$、$m\in\mathbf Z/M$。$G_N:=\operatorname{GTSh}(N,N)$(**任意の $N$ で群**)、合成は (3.53)。$N$ が isolated のときに限り $G_N=\operatorname{GT}(N)$ と書いてよい(2401 Def 3.13 直後)。

$$\widetilde\chi_{2M}:\ G_N\longrightarrow(\mathbf Z/2M)^\times,\qquad [m,f]\longmapsto 2m+1\ (\mathrm{mod}\ 2M).$$

> ### 定理 T-A(v2)
> 任意の $N\in\mathrm{NFI}_{PB_3}(B_3)$ について:
> 1. $\widetilde\chi_{2M}$ は **well-defined** であり、$2M$ は well-defined になる**最細の水準**である。
> 2. 値は単元で、$\widetilde\chi_{2M}$ は**群準同型**である。
> 3. $\ker\widetilde\chi_{2M}=\mathfrak F_0:=\{[0,f]\in G_N\}$。
> 4. **(4′ 型ゲートつき全射)** $N$ が **isolated** で **(AR)** が成り立つなら $\widetilde\chi_{2M}$ は**全射**。
>    **(4″)** 一般の $N$ については $Q_N:=\operatorname{Im}\widetilde\chi_{2M}\le(\mathbf Z/2M)^\times$ を定義するにとどまる。
> 5. **(普遍・無条件)** $\boxed{\ |\mathfrak F_0|\cdot|Q_N|=|G_N|\ }$、および $|G_N^{\rm ab}|\ge|Q_N|$。**等号 $\ker\widetilde\chi=[G_N,G_N]\iff|G_N^{\rm ab}|=|Q_N|$**。
>    **(5″)** $N$ が isolated(または独立な全射証明書つき)なら $|\mathfrak F_0|=|G_N|/\varphi(2N_{\rm ord})$、$|G_N^{\rm ab}|\ge\varphi(2N_{\rm ord})$。

**証明.**
(1) $m$ は $\mathbf Z/M$ の類。$m\mapsto m+M$ で $2m+1\mapsto(2m+1)+2M$ ✓。$4M$ を法にすると $2M\not\equiv0$ で壊れる ✓。
(2) charming より $\gcd(2m+1,M)=1$。$2m+1$ は奇数だから $2$ の任意冪と互いに素、ゆえに $\gcd(2m+1,2M)=1$。準同型性は (3.53) の第一成分と**整数の恒等式** (3.49)
$$2(2m_1m_2+m_1+m_2)+1=(2m_1+1)(2m_2+1)$$
から。恒等式は $\mathbf Z$ で厳密なので法を取る順序の誤差は出ない。単位元 $[0,1]\mapsto1$。
(3) $2m+1\equiv1\ (2M)\iff2m\equiv0\ (2M)\iff m\equiv0\ (M)\iff m=0$ in $\mathbf Z/M$。
(4′) **(AR)** = 「$\operatorname{Ih}_N=\mathrm{PR}_N\circ\operatorname{Ih}$ が存在し $\operatorname{Ih}(g)=((\chi(g)-1)/2,\,f_g)$」(2405 §1.3・図式 (1.10)(1.13))。**$N$ が isolated なら** $N^{(\hat m,\hat f)}=N$(2401 Thm 5.2 証明冒頭)ゆえ $\operatorname{PR}_N$ の像は isotropy 群 $GTSh(N,N)=G_N$ に入り、$\operatorname{Ih}_N:G_{\mathbf Q}\to G_N$ は群準同型である(2405 Remark 1.4 の対偶)。$\chi(g)\in\widehat{\mathbf Z}^\times$ は奇なので $(\chi(g)-1)/2\in\widehat{\mathbf Z}$ が定義でき、
$$\widetilde\chi_{2M}(\operatorname{Ih}_N(g))=2\cdot\tfrac{\chi(g)-1}{2}+1=\chi(g)\ \ (\mathrm{mod}\ 2M).$$
$\chi$ は全射(Kronecker–Weber)ゆえ $\chi\bmod2M$ は $(\mathbf Z/2M)^\times$ へ全射。よって $\widetilde\chi_{2M}$ も全射。
(4″)(5) 準同型の第一同型定理。$[G_N,G_N]\subseteq\mathfrak F_0$($Q_N$ が可換だから)より $G_N^{\rm ab}\twoheadrightarrow Q_N$、その核は $\mathfrak F_0/[G_N,G_N]$。$\blacksquare$

> **⚠ 註 0(v2 の型ゲート・F79-2.1)**: v1 の T-A(4) は「任意の $N$」と書いていた。**これは誤り**である。射影された shadow は target $N$ をもつが、source は一般に別の $N^{(g)}$ であり、$GTSh(N,N)$ の元とは限らない。25 窓の実測一致は**その 25 窓の有力な regression** であって普遍定理ではない。
> **註 1(算術的入力はここだけ)**: 正典 Remark 1.3 は「$\chi_{\rm vir,N}$ の全射性はこれ以外の証明を知らない」と明言する。(4′) はその**水準 $2M$ 版**である。(1)(2)(3)(5) は純群論・**無条件**。
> **註 2(実測)**: (4′)(5″) は §6 で **25 窓**で確認され不一致ゼロ。ただし 25 窓のうち isolated が正典で保証されているのは $K^{(n)}$ 族(Thm 4.3)であり、**$L,M_5,N_Q,M_Q,N_2,N_3,M_3,N_A,M_{A_5}$ の isolated 性は本稿では未確認**。それらの窓での全射性は「窓ごとの実測証明書」として扱う。
> **註 3(掃引への即効・v2 で二段化)**: (5) は**無条件の** fail-closed assert `|ker_chi| * chi_image_order == |G_N|` を与える。**$\varphi(2N_{\rm ord})$ との比較は別 assert** とし、`is_isolated` または `chi_surjectivity_cert` のある窓でのみ発火させる(§7.4・P79-A)。

**記号**: 以下 $Q:=Q_N=\operatorname{Im}\widetilde\chi$、$\mathfrak F_0=\ker\widetilde\chi$、$G:=G_N$。**$[G,G]\subseteq\mathfrak F_0$ は $Q$ が可換であることから自明**。問題は逆包含。

---

## 3. T-B — 完全な判定条件

> ### 定理 T-B(判定条件・v2)
> $1\to\mathfrak F_0\to G\xrightarrow{\widetilde\chi}Q\to1$($Q=\operatorname{Im}\widetilde\chi$)に対し、**自然な同型**
> $$\boxed{\ \ker\widetilde\chi\big/[G,G]\ \cong\ \operatorname{coker}\Bigl(H_2(Q;\mathbf Z)\xrightarrow{\ \mathrm{tg}\ }\bigl(\mathfrak F_0^{\rm ab}\bigr)_Q\Bigr),\qquad H_2(Q;\mathbf Z)=\Lambda^2Q\ }$$
> がある($(\ \cdot\ )_Q$ = 共役作用に関する余不変量)。とくに:
> * **(B1)** $(\mathfrak F_0^{\rm ab})_Q=0\ \Longrightarrow$ **等号成立**。
> * **(B2)** $Q$ が**巡回**なら $\Lambda^2Q=0$ ゆえ **等号成立 $\iff(\mathfrak F_0^{\rm ab})_Q=0$**。
> * **(B3)** $\mathfrak F_0^{\rm ab}$ が **$Q$-自明な商 $V\ne0$** をもち $\gcd(|V|,|\Lambda^2Q|)=1$ なら **等号は破れ**、$\ker\widetilde\chi/[G,G]\twoheadrightarrow V$。

**証明.** LHS 5 項完全列
$$H_2(G)\to H_2(Q)\xrightarrow{\ \mathrm{tg}\ }H_0\bigl(Q,H_1(\mathfrak F_0)\bigr)\to H_1(G)\to H_1(Q)\to0$$
で $H_1(\ \cdot\ )=(\ \cdot\ )^{\rm ab}$、$H_0(Q,\mathfrak F_0^{\rm ab})=(\mathfrak F_0^{\rm ab})_Q$。末尾 3 項から $\ker(G^{\rm ab}\to Q)\cong\operatorname{coker}(\mathrm{tg})$。$\widetilde\chi$ は $Q$ へ全射(定義)で $[G,G]\subseteq\mathfrak F_0$ だから $\ker(G^{\rm ab}\to Q)=\mathfrak F_0/[G,G]$。$Q$ は有限アーベルなので $H_2(Q;\mathbf Z)\cong\Lambda^2Q$。
(B1) 余不変量が $0$ なら coker も $0$。(B2) 巡回群は $\Lambda^2=0$。(B3) 合成 $\Lambda^2Q\to(\mathfrak F_0^{\rm ab})_Q\twoheadrightarrow V_Q=V$ は位数互いに素な有限群の間の準同型ゆえ $0$、よって $\operatorname{coker}(\mathrm{tg})\twoheadrightarrow V\ne0$。$\blacksquare$

> **註(なぜ余不変量だけでは足りないか)**: 実測(§6)で **K8・K16 は $(\mathfrak F_0)_Q\cong\mathbf Z/2\ne0$ なのに等号が成立**する。そこでは $\Lambda^2Q=\mathbf Z/2$ からの transgression がちょうど余不変量を潰している。**「余不変量 $\ne0$ ⟹ 反例」は誤り**であり、T-B の coker まで見る必要がある — 本稿の技術的核心。

**$\Lambda^2Q$ の前処理**: 全射証明書のある窓では $Q=(\mathbf Z/2M)^\times$ が $M$ だけで決まるので $\Lambda^2Q$ は $N_{\rm ord}$ の算術関数として先に表にできる。**全射が未確定の窓ではこの前処理は使えない**(実像 $Q_N$ を測ってからでないと $\Lambda^2Q_N$ が決まらない)— v2 で追加した制限。

### 3.1 素数位数の核 — 補題 P(**射程を訂正**)

> **補題 P.** $|\mathfrak F_0|$ が**素数** $p$ なら
> $$\ker\widetilde\chi=[G,G]\ \iff\ G\ \text{が非可換}.$$
> **証明.** $[G,G]$ は素数位数群 $\mathfrak F_0$ の部分群だから $1$ か $\mathfrak F_0$。$G$ 可換 $\iff[G,G]=1$。$\blacksquare$
> **系 P0.** $|\mathfrak F_0|=1$ なら等号は**無条件に**成立。

> ### ⛔ v1 の系は撤回(E3・F79-2.5)
> v1 は補題 P から「**反例は $|\mathfrak F_0|$ が非素数の窓にしか存在しない**」を導いていた。**これは偽である。** 任意の可換群 $Q$ と素数 $p$ に対し
> $$G=C_p\times Q\ \longrightarrow\ Q\quad(\text{射影})$$
> は核 $C_p$(素数位数)をもつが $[G,G]=1$ で等号は破れる。**素数核は除外篩ではない。**
> **正しい読み**: 補題 P は等号問題を「**$G$ が可換か**」という**一ビット**へ還元する判定器である。そのビットが「非可換」なら等号成立、「可換」なら**反例**。素数核の窓は**除外先ではなく、最安の反例候補**である(合成表なしで $|\mathfrak F_0|$ が出る上に、可換性は導来列 1 本で決まる)。

### 3.2 【新設】予想 KE-P — 失った篩を限定版で取り戻す道

F79-2.5 は「GT isotropy 群に限って『可換なら核は自明』とする追加定理が将来立てば限定版は救える」と書いた。その定理の候補を明示しておく。

> ### ⛔ 予想 KE-P(素形)は **v2.1 で反証された** — §11 を先に読むこと
> 以下の素形は **`W-A-B3idx126-s2/s3` により偽**である。生き残るのは §11 の**全射ゲート版 KE-P$'$** のみ。素形を篩に使ってはならない。

> ### 予想 KE-P(素形・**反証済み**・§11)
> ~~$G_N=GTSh(N,N)$ が**可換**ならば $\widetilde\chi_{2M}$ は**単射**、すなわち $\mathfrak F_0=1$。~~
> ~~同値に: $G_N$ が可換なら $G_N\cong Q_N\le(\mathbf Z/2M)^\times$。~~

**支持データ(atlas 内で可換な窓は 3 つ、すべて $\mathfrak F_0=1$)**:

| 窓 | $|G_N|$ | $N_{\rm ord}$ | 導来長(census v2) | $|\mathfrak F_0|$ |
|---|---|---|---|---|
| K4 | 4 | 4 | — | **1** |
| $N_Q$ | 4 | 4 | 1(可換) | **1** |
| $N_2$ | 4 | 4 | 1(可換) | **1** |

**もし KE-P が真なら**: 素数核 $|\mathfrak F_0|=p>1$ の窓は自動的に非可換、よって補題 P より**等号成立**。すなわち v1 の priority 0 の篩が**「GT 窓に限る」という限定つきで復活する**。**現状は予想であり、篩として使ってはならない**(3 標本は根拠として薄い)。
**反証の形**: 可換な $G_N$ で $\mathfrak F_0\ne1$ の窓を 1 つ見つければ KE-P は死ぬ。そしてその窓は**同時に等号の反例**であり、L より安価な 2 例目になる(§7.5 v2 の priority 1)。

---

## 4. T-C — dihedral 族では等号が成立(全 $n$)

> ### 定理 T-C
> 全ての $n\ge3$ について $\ker\widetilde\chi_{2M}=[\operatorname{GT}(K^{(n)}),\operatorname{GT}(K^{(n)})]$、同値に
> $$\bigl|\operatorname{GT}(K^{(n)})^{\rm ab}\bigr|=\varphi(2N_{\rm ord}).$$

**前提の確認(v2 で明示)**: $K^{(n)}$ は **isolated**(正典 2401 **Thm 4.3**・定義ノート §該当行)。したがって T-A(4′)(5″) がこの族では**適用できる** — E1 の型ゲートは dihedral 主線を傷つけない。

**証明.** $n=n_0\cdot2^\alpha$($n_0$ 奇)。T-A(5″) より、示すべきは $|[G,G]|=|G|/\varphi(2M)$ である($[G,G]\subseteq\mathfrak F_0$ は既知なので**位数の一致で十分**)。正典 Thm 4.6 (4.23) を使う。

**(i) $\alpha=0$($n$ 奇)**: $M=\operatorname{lcm}(n,2)=2n_0$、$2M=4n_0$、$\varphi(2M)=2\varphi(n_0)$。$G\cong\operatorname{Aff}(\mathbf Z/n_0)\times\mathcal Z_2$、$|G|=2n_0\varphi(n_0)$。$n_0$ 奇ゆえ $-1\in(\mathbf Z/n_0)^\times$ で $u-1=-2$ は可逆、よって $[\operatorname{Aff}(\mathbf Z/n_0),\operatorname{Aff}(\mathbf Z/n_0)]=$ 並進部 $\cong\mathbf Z/n_0$、$\mathcal Z_2$ は可換直積因子。$|[G,G]|=n_0=|G|/\varphi(2M)$ ✓。

**(ii) $\alpha=1$($n=2n_0$)**: $M=2n_0$、$\varphi(2M)=\varphi(4n_0)=2\varphi(n_0)$。Thm 4.6 は $\alpha<2$ で同じ $\operatorname{Aff}(\mathbf Z/n_0)\times\mathcal Z_2$ を与えるので (i) と同一計算 ✓。

**(iii) $\alpha\ge2$**: $M=n=n_02^\alpha$、$2M=n_02^{\alpha+1}$、$\varphi(2M)=\varphi(n_0)2^\alpha$。$G\cong\operatorname{Aff}(\mathbf Z/n_0)\times\widetilde H_\alpha$、
$$\widetilde H_\alpha=\bigl\{(\bar k,(-1)^a\bar5^{\,b})\in\mathbf Z/2^{\alpha-1}\rtimes(\mathbf Z/2^{\alpha+1})^\times\ \bigm|\ k\equiv b\ (2)\bigr\},\quad|\widetilde H_\alpha|=2^{2\alpha-2}\ \ \text{(4.24)}.$$
$\operatorname{Aff}(\mathbf Z/m)$ 内の交換子は直接計算で $[(k_1,u_1),(k_2,u_2)]=((1-u_2)k_1+(u_1-1)k_2,\ 1)$。$\widetilde H_\alpha$ では $u$ は奇数だから $u-1$ は偶数、よって $[\widetilde H_\alpha,\widetilde H_\alpha]\subseteq2\,\mathbf Z/2^{\alpha-1}$。逆に $g_1=(0,-1)$、$g_2=(k,u)$($b\equiv k\ (2)$ と取れる)で $[g_1,g_2]=(-2k,1)$、$k$ を動かせば $2\,\mathbf Z/2^{\alpha-1}$ 全体。ゆえに $|[\widetilde H_\alpha,\widetilde H_\alpha]|=2^{\alpha-2}$。
したがって $|[G,G]|=n_0\cdot2^{\alpha-2}=|G|/\varphi(2M)$ ✓。$\blacksquare$

> **註($\alpha\ge2$ では transgression が実際に働く)**: (iii) で $\mathfrak F_0=2\,\mathbf Z/2^{\alpha-1}$、$Q\ni u$ の作用は $u$ 倍。$u-1$ は常に偶数なので $(\mathfrak F_0)_Q\cong\mathbf Z/2\ne0$($\alpha\ge3$)。それでも等号が立つのは $\Lambda^2Q\cong\mathbf Z/2$ から transgression が全射だからである。**(iii) の直接計算はこの transgression を「手で」実行したものにあたる。** 実測 K8・K16 の $|(\mathfrak F_0)_Q|=2$ がこれに対応する。

---

## 5. T-D — 反例($L=K^{(3)}\cap N_0$)

### 5.1 実測

**対象**: `certificates/L01.v1.json`(atlas 登録窓 $L$)。$PB_3/L\cong G_3\times H_3$($H_3$ = 位数 27 の Heisenberg 群、$X=(1,0,0)$、$Y=(0,1,0)$)、$c\in L$、$[B_3:L]=17496$、$N_{\rm ord}=6$。

| 量 | 値 |
|---|---|
| $|G_L|$ | **36** |
| $Q_L=\operatorname{Im}\widetilde\chi$ | **実測 $\{1,5,7,11\}=(\mathbf Z/12)^\times$**($\cong(\mathbf Z/2)^2$、位数 4)— **この窓の全射は実測証明書**(isolated 性には依拠しない) |
| $|\mathfrak F_0|=36/4$ | **9**(T-A(5) の普遍形と一致 ✓)。構造 $\cong C_3\times C_3$ |
| $|[G_L,G_L]|$ | **3** |
| $\ker\widetilde\chi/[G_L,G_L]$ | $\cong\mathbf Z/3$ — **等号は破れている** |
| $(\mathfrak F_0)_Q$ | $\cong\mathbf Z/3$(実測) |
| $\Lambda^2Q$ | $\cong\mathbf Z/2$ |
| $|G_L^{\rm ab}|$ | **12** $\ne|Q_L|=4$ |

> **v2 の型注記**: v1 は $|\mathfrak F_0|=36/\varphi(12)$ と書いたが、正しくは $36/|Q_L|$ であり、**$|Q_L|=\varphi(12)$ は実測**である($L$ の isolated 性は未確認)。数値は変わらない。

**根拠の質**: 合成表 `L01.v1.json` の 1296 エントリは **GAP 4.16.0(`search/week3-L-explorer.g`)で生成 → node の独立レーンが全件再計算**(`crosscheck/verdicts/L01.v1.verdict.json` item `7_composition_table`: `ok:true, checked:1296, fails:[]`)。すなわち **cross-checked**(二系統一致)。**verified(Lean)ではない。** 測定スクリプトはさらに ①単位元の一意性 ②結合律 ③Latin 方陣性 ④**(3.53) 第一成分の再現** ⑤$\widetilde\chi$ の準同型性、を fail-closed assert してから測っている。$L\triangleleft B_3$ と指数 17496 は `search/certs/ke_a_normality_20260729.json`(**GAP 一レーン**)。

**測定スクリプト**: `search/kerchi-abelianization-check.py`(sha256 `bbcc5bf058069dff9154a067a4fee27880c50e4585744a6cafe24a0f52f9ea26`)。**Sol が便 79 監査で再実行し 18 窓の全行と L01 を再現している**(F79-2.3)。

### 5.2 **理論機構と有限データを組み合わせた証明**(v1 の「a priori 証明」を改称・E7)

$Q$-加群としての $\mathfrak F_0\cong\mathbf F_3^2$ は、基底 $(g_1,g_2)$ で対角化される(**この基底の存在と $g_1,g_2$ の同定は登録証明書からの有限データ**):

| $u\in Q$ | $g_1$ | $g_2$ |
|---|---|---|
| $1,7$ | $+1$ | $+1$ |
| $5,11$ | $+1$ | $-1$ |

すなわち $\mathfrak F_0\cong\mathbf 1\oplus\chi_3$。$g_1$ は shadow $[0,[x^2,y^2]]$(証明書 index 6)、$g_2$ は index 8。

**$g_1$ が $Q$-自明であることの理論的証明**: $H_3$ は class 2 で $[X,Y]$ が中心を生成し位数 3。$\Phi_{m,f}$ は $X\mapsto X^{u}$、$Y\mapsto f^{-1}Y^{u}f$($u=2m+1$)を誘導するので、class 2 ゆえ
$$[X,Y]\ \longmapsto\ [X^{u},Y^{u}]=[X,Y]^{u^2}.$$
$u\in(\mathbf Z/12)^\times$ に対し $u\equiv\pm1\ (3)$、よって $u^2\equiv1\ (3)$。**中心方向は $\Phi$ 不変**、したがって $g_1$ は $Q$-自明。

> ### **【E6】Maschke の一行(F79-2.3 の補修)**
> 「$Q$-自明な直線 $\langle g_1\rangle$ がある」から「**$Q$-自明な商がある**」へ渡るには半単純性が要る。
> $|Q|=4$ と係数標数 $3$ は互いに素なので、**Maschke の定理**により $\mathbf F_3[Q]$-加群はすべて半単純である。したがって固定直線 $\langle g_1\rangle\le\mathfrak F_0^{\rm ab}$ は **$Q$-安定な補空間**をもち、$Q$-同変な全射
> $$\mathfrak F_0^{\rm ab}\ \twoheadrightarrow\ \langle g_1\rangle\cong C_3$$
> が存在する。これで T-B(B3) を $V=\langle g_1\rangle$ に適用できる。

$\gcd(|V|,|\Lambda^2Q|)=\gcd(3,2)=1$ より **T-B(B3) から等号は破れ、$\ker\widetilde\chi/[G,G]\twoheadrightarrow\mathbf Z/3$**。実測の指数 3 と一致する。$\blacksquare$

> **⚠ 呼称の訂正(E7)**: v1 はこれを「実測に依存しない a priori 証明」と呼んだ。**それは強すぎる。** 重み 2 の生存機構(下記 W2)は理論的だが、$\mathfrak F_0^{\rm ab}$ の具体的な $C_3^2$ 構造・中心方向の同定・$Q$ の作用表には**登録証明書の有限データ**を使っている。**「理論機構+有限データの組合せによる証明」**と呼ぶのが正確である。

### 5.3 機構の一般化 — 重み 1 と重み 2

> ### 命題 W2(重み)
> $\pi:PB_3/N\twoheadrightarrow H$ を $\Phi$-安定な商、$H$ は冪零度 2、$H'=\langle[\bar X,\bar Y]\rangle\cong\mathbf Z/e$ を中心とする($e\mid2M$)。$\Phi_{m,f}$ は $H^{\rm ab}$ 上で**重み 1**(スカラー $u$)、$H'\cong\gamma_2/\gamma_3$ 方向で**重み 2**(スカラー $u^2$)で作用する。とくに
> $$u^2\equiv1\ (\mathrm{mod}\ e)\ \ \text{が全ての}\ u\in(\mathbf Z/2M)^\times\ \text{で成立}\iff e\mid24$$
> であり、そのとき $H'$ 方向は **GT-自明**である。

**証明.** class 2 で $[X^a,Y^b]=[X,Y]^{ab}$。$\Phi$ は $\bar X\mapsto\bar X^u$、$\bar Y\mapsto$($\bar Y^u$ の共役)で、中心への共役は自明だから $[\bar X,\bar Y]\mapsto[\bar X,\bar Y]^{u^2}$。後半: $(\mathbf Z/e)^\times$ の指数が $\le2$ $\iff e\mid24$($e\in\{1,2,3,4,6,8,12,24\}$)。$\blacksquare$

> **反例の作り方(処方)**: **$\mathfrak F_0$ に「重み 2 の層」を持ち込む** — $K^{(n)}$ 型の窓と**冪零(Heisenberg 型)窓の交叉**をとる。$L=K^{(3)}\cap N_0$ がその型で、重み 1 の $C_3$($G_3$ 由来 = $[\operatorname{GT},\operatorname{GT}]$)と重み 2 の $C_3$($H_3$ 中心由来 = 余不変量として生存)が同居する。

---

## 6. 測定表(atlas 横断)

**入力**: `certificates/*.json` のうち shadow 水準 composition table をもつ 18 窓。**$\Phi$ 像は不使用。**
$\operatorname{Im}\widetilde\chi$ 欄の「✓」は $Q_N=(\mathbf Z/2N_{\rm ord})^\times$ の**実測**(理論的保証ではない)。

| 窓 | $|G_N|$ | $N_{\rm ord}$ | $\varphi(2N)$ | $|\ker\widetilde\chi|$ | $\operatorname{Im}\widetilde\chi$ 全射(実測) | $|[G,G]|$ | **EQUAL** | $|(\mathfrak F_0)_Q|$ |
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

**全 18 窓**: $\widetilde\chi$ 全射 18/18(**実測**)・普遍個数等式 $|\ker|\cdot|Q_N|=|G_N|$ 18/18 ✓・$[G,G]\subseteq\ker$ 18/18 ✓・**等号 17/18(唯一の反例 L01)**。

**battery 7 窓**(composition table 未収録・shadow 一覧のみ)での T-A(5) の追加確認:

| 窓 | 定義 | $|G_N|$ | $N_{\rm ord}$ | $\varphi(2N)$ | $|\ker\widetilde\chi|$(実測 $m=0$ の個数) | 個数等式 |
|---|---|---|---|---|---|---|
| $N_Q$ | $\pi^{-1}(\ker(F_2\twoheadrightarrow Q_8))$ | 4 | 4 | 4 | 1 | ✓ |
| $M_Q$ | $K^{(3)}\cap N_Q$ | 24 | 12 | 8 | 3 | ✓ |
| $N_2$ | $\pi^{-1}(F_2^4\gamma_3)$ | 4 | 4 | 4 | 1 | ✓ |
| $N_3$ | $\pi^{-1}(F_2^4\gamma_4)$ | 8 | 4 | 4 | 2 | ✓ |
| $M_3$ | $K^{(3)}\cap N_3$ | 48 | 12 | 8 | 6 | ✓ |
| $N_A$ | $\pi^{-1}(\ker(F_2\twoheadrightarrow A_5))$ | 20 | 5 | 4 | 5 | ✓ |
| $M_{A_5}$ | $N_A\cap N_5$ | 20 | 5 | 4 | 5 | ✓ |

**合計 25 窓で個数等式の不一致ゼロ。**(**これは 25 窓の regression であって普遍定理ではない** — E1)

### 6.3 【E5】$N_3$ の決着 — census v2 による

> **$N_3$: 等号成立。**
> - $|\mathfrak F_0|=|G_{N_3}|/|Q|=8/4=2$ — **素数**。
> - `search/certs/derived_census_v2_20260729.json` の $N_3$ 行: `group_order = 8`、**`derived_length_of_group = 2`**、`derived_length_of_image = 1`、`phi_image_order = 4`。
> - `derived_length_of_group` は **(3.53) shadow 合成表の正則表現**から `DerivedSubgroup` で計算されており(証明書 `schema_note`)、**$\Phi$ 像ではない**(C2F 遵守)。導来長 2 は $[G,G]\ne1$、すなわち **$G_{N_3}$ は非可換**。
> - **補題 P** より等号成立。$\blacksquare$

> **⚠ 根拠の質**: census v2 は**同一 GAP スクリプト由来の一レーン artifact** である(F79-4.3)。したがって $N_3$ の等号は「**単系統 GAP による導来長 1 ビット + 紙上の補題 P**」であり、**cross-checked ではない**。二系統化は `derived_length_of_group` を node レーンで再計算すれば足りる(合成表は既に手元にある)。
> **v1 の見通しとの対照**: v1 は「$\Phi$ 像(位数 4)は可換なのでこの方向からは決まらない — shadow 水準で 1 ビット測るだけで決着」と書いた。census v2 が測ったのは**まさにその 1 ビット**であり、`derived_length_of_image = 1`(像は可換)と `derived_length_of_group = 2`(本体は非可換)の**分離**が答えになっている。**$\Phi$ 像の可換性から本体の可換性を読んだら誤答していた** — C2F の罠が実際に効く実例。

**atlas 14 対象の決着(v2)**:

| 判定 | 窓 | 根拠 |
|---|---|---|
| **等号成立** | $K^{(3)},K^{(5)},K^{(7)},K^{(9)},K^{(11)}$ | T-C(証明・isolated)+ 合成表実測 |
| | $M_5$ | 合成表実測 |
| | $N_Q,N_2$ | $|\mathfrak F_0|=1$(系 P0・無条件) |
| | $N_A,M_{A_5}$ | $|\mathfrak F_0|=5$ 素数 + census の導来長 2(非可換)→ **補題 P** |
| | $M_Q$ | $|\mathfrak F_0|=3$ 素数 + census の `derived_length_of_group = 2`(非可換)→ **補題 P** |
| | **$N_3$** ← **v2 で新規決着** | $|\mathfrak F_0|=2$ 素数 + census v2 の `derived_length_of_group = 2` → **補題 P**(§6.3) |
| **等号不成立** | **$L$** | T-D(実測 + §5.2 の証明) |
| **UNKNOWN** | **$M_3$** のみ | $|\mathfrak F_0|=6$(非素数)・合成表未収録 |

> **註($M_Q$ の根拠の差し替え)**: v1 は $M_Q$ の非可換性を「$\Phi$ 像(位数 12)が非可換 ⟹ 元の群も非可換」という**一方向**の使い方で得ていた(C2F の罠にはかからない)。v2 では census v2 の `derived_length_of_group = 2`(本体・(3.53) 由来)が直接使えるので、そちらを正本にする。**$N_A,M_{A_5}$ も同様**。

**残る UNKNOWN の見通し**:
* **$M_3$**: $|\mathfrak F_0|=6$(非素数 — 反例の資格がある窓)。$Q=(\mathbf Z/24)^\times\cong(\mathbf Z/2)^3$、$|\Lambda^2Q|=8$。3-部分は $M_Q$ と同型の議論で潰れる見込み、2-部分は transgression 勝負。**$\mathfrak F_0$ の 2-部分が生き残れば 2 例目の反例**。census v2 の `derived_length_of_group = 2` は「非可換」しか言わないので**補題 P の射程外**(核が非素数)。決着には **shadow 水準の合成表**が要る。

---

## 7. 壁ソルバーへの帰結

### 7.1 無傷なもの

$[G,G]\subseteq\ker\widetilde\chi$ は**無条件の定理**なので
$$\textbf{TIER-0}:\quad \ker\widetilde\chi\ \text{可換}\ \Longrightarrow\ [G,G]\ \text{可換}\ \Longrightarrow\ G_N\ \text{metabelian}$$
は**そのまま有効**。v1.1 の記述に変更不要。

### 7.2 訂正 — FAIL-2 の文言

v1.1 は「逆は主張しない(**FAIL-2**: 等号は**未証明**)」と書く。これは
> **未証明ではなく、一般には偽である。反例 $L$ は登録 atlas の中にある**(T-D)。**dihedral 族($K^{(n)}$ 全 $n$)では定理**(T-C)。

に改めるべきである。**TIER-1 から「非 metabelian」への昇格は、その窓での等号を別途証明しない限り不正。**

### 7.3 `KERNEL-DL3`(= 旧 TIER-1.5・等号を要さない非 metabelian 判定)

> **命題 `KERNEL-DL3` / `KERNEL-NONMETABELIAN`(旧 TIER-1.5).** $\ker\widetilde\chi$ の**導来長が 3 以上**($\mathfrak F_0''\ne1$)なら $G_N''\ne1$、すなわち $G_N$ は **非 metabelian**。**等号を一切要さない。**
> **証明.** $\mathfrak F_0\le G_N$ ゆえ $\mathfrak F_0''\le G_N''$。$\blacksquare$

**名称は意味を直接表す `KERNEL-DL3` を正式名とし、`TIER-1.5` は旧称として残す**(E8・F79-2.6)。

### 7.4 等号証明書(窓ごと)+ P79-A character registry

**普遍形**(無条件):
$$\boxed{\ \ker\widetilde\chi=[G,G]\iff\bigl|G_N^{\rm ab}\bigr|=|Q_N|\ }$$
$\varphi(2N_{\rm ord})$ 版は **isolated または全射証明書のある窓に限る**。証明書 schema `wall-cert/v1` に足す欄(P79-A を採用):

```text
canonical_character_modulus = N_ord
refined_character_modulus   = 2*N_ord
chi_image_order                       # = |Q_N|(実測)
chi_surjective_status = PROVED | CROSS_CHECKED_WINDOW | UNKNOWN
chi_surjective_evidence_digest
is_isolated = TRUE | FALSE | UNKNOWN
abelianization_order                  # = |G_N^ab|
kerchi_equals_derived                 # abelianization_order == chi_image_order / UNKNOWN
```

**fail-closed assert(二段・E9)**:

```text
[普遍・常時]      ker_chi_order * chi_image_order == group_order
[gate つき]       chi_image_order == phi(2*N_ord)
                    ← is_isolated == TRUE  または  chi_surjective_status != UNKNOWN のときだけ発火
```

普遍 assert は **$\Phi$ 潰れ型の系統誤りを掃引の内部から検出する**(C2F 検出器)。**$\varphi$ 版を無条件で焚くと、非 isolated 窓で偽の FAIL を出しうる。**

**安い前段(補題 P・射程を訂正)**: $|\mathfrak F_0|=|G_N|/|Q_N|$ が
* **$1$** なら等号成立(系 P0・無条件)。
* **素数**なら「$G_N$ 可換か」の**一ビット**で決着(**両側に転ぶ**: 非可換 ⟹ 成立、可換 ⟹ **反例**)。導来列 1 本で足りる。
* **非素数**なら T-B の coker(余不変量+transgression)を計算する。

### 7.5 反例の探し場所(**v2 で組み直し**)

| 優先度 | 探し場所 | 根拠 |
|---|---|---|
| **1** | **$|\mathfrak F_0|$ が素数($>1$)で $G_N$ が可換な窓** — 見つかれば**即・反例**、しかも最安(合成表不要・導来列 1 本) | 補題 P。**v1 はここを「除外」していた(E4 の誤り)。予想 KE-P が真ならこの箱は空だが、未証明** |
| **2** | **$N_{\rm ord}$ が奇素数冪または $M\in\{1,2\}$ の窓** — $Q_N$ が巡回なら $\Lambda^2Q_N=0$、ゆえに **$(\mathfrak F_0)_{Q_N}\ne0$ なら必ず反例** | T-B(B2)。**$Q_N$ の巡回性は実像で判定する**(全射未確定でも使える — むしろ非全射なら $Q_N$ が巡回になりやすい) |
| **3** | **$K^{(n)}$ と冪零窓(Heisenberg・$\gamma_3,\gamma_4$ 型)の交叉窓** — 重み 2 の層が入る | T-E(W2)。$L$ がこの型。**$M_3$ が未決着の同型候補** |
| **4** | **$|\Lambda^2Q_N|$ と $|(\mathfrak F_0)_{Q_N}|$ が互いに素**になる窓(一般形) | T-B(B3) |

実務: 各窓で **(a) $|\mathfrak F_0|=|G_N|/|Q_N|$、(b) $Q_N$ の構造(巡回か)と $|\Lambda^2Q_N|$、(c) $|\mathfrak F_0|$ が素数なら導来列 1 本**、を並べる。(a)(b) は掃引が既に持つ量から無料。

---

## 8. 自己監査(v2)

| # | リスク | 判定 |
|---|---|---|
| R-1 | $L$ が本当に $\mathrm{NFI}_{PB_3}(B_3)$ の窓か | △ `ke_a_normality_20260729.json` が $L\triangleleft B_3$・指数 17496 を閉じるが **GAP 一レーン**。**これが偽なら T-D は消える**(T-A/T-B/T-C は無傷) |
| R-2 | 合成表の向き(左右) | ○ **結論に無関係**($\ker\widetilde\chi$ も $[G,G]$ も $G$ と $G^{\rm op}$ で同一) |
| R-3 | 合成表が「本当に GT-shadow の群」か | ○ 群公理 3 種 + **(3.53) 第一成分の再現**を fail-closed assert + node 独立レーン検収 |
| **R-4** | **T-A(4′) が (AR) と isolated 性に依存** | △ **v2 で型ゲート化**。25 窓の全射は**実測証明書**として扱い、族的主張は isolated 窓に限る |
| **R-4b** | **25 窓のうち isolated が正典で保証されるのは $K^{(n)}$ 族だけ** | △ **明示**。$L,M_5,N_Q,M_Q,N_2,N_3,M_3,N_A,M_{A_5}$ の isolated 性は**未確認**。→【KE-g】 |
| R-5 | T-C が Thm 4.6 (4.23)(4.24) の**引用**に依存 | △ 明示。16 窓の独立実測が背理検査になっている |
| R-6 | $H_2(Q)=\Lambda^2Q$ の適用範囲 | ○ 有限アーベル群で標準。$Q_N\le(\mathbf Z/2M)^\times$ は有限アーベル ✓ |
| R-7 | 「余不変量 $\ne0$ ⟹ 反例」と早合点する危険 | ○ **本稿自身が反証**(K8/K16) |
| R-8 | T-D を「dihedral 予想に影響」と読む危険 | ○ **影響しない**。$L$ は dihedral 塔の窓ではない。影響するのは壁キャンペーンの推論規則のみ |
| **R-9** | **補題 P を除外篩として使う誤り**(v1 の E3/E4) | ○ **v2 で撤回・§3.1 に警告を常設**。★教材「素数核は反例除外器ではない」 |
| R-10 | $e\mid24$ 判定で $e\mid2M$ を暗黙に使う | ○ W2 の仮定に明記($L$ では $e=3\mid12$ ✓) |
| **R-11** | **census v2 の一レーン性**($N_3$ 決着の根拠) | △ **明示**。単系統 GAP。node 再計算で二系統化可能(【KE-h】) |
| **R-12** | **予想 KE-P を篩として使う危険** | ○ **予想と明記**。3 標本のみ。使用禁止を §3.2 に明記 |

---

## 9. 未閉鎖項・次の一手(v2)

* 【KE-a】**$L$ の $B_3$-正規性の二系統化**(現在 GAP 一レーン)。T-D の唯一の外部依存。
* 【KE-b′】**$M_3$ の決着**(v1 の KE-b から $N_3$ が落ちた): $M_3$ の **shadow 水準合成表**の生成。$|\mathfrak F_0|=6$ で**反例の資格がある**唯一の未決着窓。
* 【KE-c】**$\Lambda^2Q_N$ の前処理表** — ただし **$Q_N$ は実像**なので、全射未確定の窓では $N_{\rm ord}$ からの表引きではなく測定が要る(v1 からの訂正)。
* 【KE-d】**W2 の逆**: $\mathfrak F_0$ の「重み分解」を一般に計算する装置。→ 下記【文献要請】。
* 【KE-e】**I-26 への接続**: T-A(5″)+T-C は「$\operatorname{GT}(K^{(n)})^{\rm ab}\cong(\mathbf Z/2M)^\times$」を全 $n$ で確定させる。**ただし $L$ で $G^{\rm ab}$ が $Q_L$ より真に大きい**ので、「アーベル化は円分で尽きる」は **dihedral 族に固有**。
* 【KE-f】本稿は紙上(paper-proof candidate)+ 既存 cross-checked 証明書の再解析。**Lean 検証ではない。**
* 【KE-g・新設】**atlas 各窓の isolated 性の判定**。T-A(4′) の gate を実際に開けるかは窓ごとに決まる。`is_isolated` 欄を UNKNOWN のまま運用してよいが、**$\varphi$ 版 assert を焚くには要る**。
* 【KE-h・新設】**census v2 の `derived_length_of_group` の node 二系統化**($N_3$/$M_Q$/$N_A$/$M_{A_5}$ の等号判定の根拠を cross-checked に上げる)。
* 【KE-i・新設】**予想 KE-P の証明または反証**。真なら §7.5 priority 1 の箱が空になり、v1 の篩が「GT 窓限定」で復活する。偽なら**その witness がそのまま 2 例目の反例**。

> ### 【文献要請】(v1 から継続)
> **困難**: 等号の成否は「$\mathfrak F_0$ の各層に $\Phi_{m,f}$ が重み $u^{w}$ のどれで作用するか」で決まる(§5.3)。重み 1 の層は $[G,G]$ に吸収され、重み 2 以上で $u^{w}\equiv1$ となる層が余不変量として残る。現状これを**窓ごとに手で読む**しかない。
> **欲しい結果の型**: 「自由群 $F_2$ の**降中心列 $\gamma_k/\gamma_{k+1}$**に対し、$x\mapsto x^u,\ y\mapsto y^u$(と共役)から誘導される作用が **$u^k$ 倍**であること、およびその**有限冪零商での定式化**(Magnus 埋め込み・Fox 微分・$\mathbf F_p$ 係数リー環の重み分解)」。より一般に $\widehat{\mathrm{GT}}$ の**深さフィルトレーション**と円分指標の重みの対応。
> **当て**: Ihara・Deligne–Terasoma・Hain–Matsumoto の mixed Tate / weight filtration on $\pi_1$ 系、あるいは Magnus 展開と自由リー環の標準教科書。
> **使い道**: 窓の nilpotency データから**等号の成否を計算で予言**でき、§7.5 の「探し場所」が「探し当て」に変わる。

---

## 10. v1 の履歴(撤回・訂正された主張の記録)

**この節は v1 で述べ、v2 で撤回・訂正した主張を明示的に記録する**(下流文書が v1 を引いている場合の照合用)。

| v1 の主張 | v2 の判定 | 差し替え先 |
|---|---|---|
| T-A(4)「任意の $N$ で $\widetilde\chi_{2M}$ は全射」 | **撤回**(型エラー) | T-A(4′)(4″)・§2 註 0 |
| T-A(5) 「$|\mathfrak F_0|=|\operatorname{GT}(N)|/\varphi(2N_{\rm ord})$」を無条件 | **限定**(isolated / 証明書つきの窓のみ) | T-A(5)(普遍形)・(5″) |
| T-G 系「反例は $|\mathfrak F_0|$ 非素数の窓にしか存在しない」 | **偽**(反例 $C_p\times Q$) | §3.1 の警告・§7.5 v2 priority 1 |
| §7.5 priority 0「素数または 1 の核は反例探索から除外」 | **削除** | §7.5 v2(素数核は**最安の反例候補**) |
| §5.2「独立な a priori 証明(実測に依存しない)」 | **改称** | §5.2「理論機構+有限データの組合せ」 |
| §5.2 「$Q$-固定な直線があるから $Q$-自明な商がある」 | **証明にギャップ**(半単純性が要る) | §5.2【E6】Maschke の一行 |
| §6「$N_3$ は UNKNOWN」 | **stale**(census v2 で決着) | §6.3(等号成立) |
| §7.3 の名称「TIER-1.5」 | **改称**(旧称として残す) | §7.3 `KERNEL-DL3` |
| §3 「$\Lambda^2Q$ は $N_{\rm ord}$ の算術関数として先に表にできる」 | **限定**($Q_N$ が実像のため、全射未確定の窓では不可) | §3 末尾・【KE-c】 |

**変更していないもの(v1 のまま有効)**: T-A(1)(2)(3)、T-B の同型と (B1)(B2)(B3)、T-C の全証明、T-D の実測値と反例性、T-E(命題 W2)、§7.1 TIER-0、§7.2 FAIL-2 の訂正文言、K8/K16 の「余不変量だけでは足りない」註。

---

# 11. 【v2.1 追補】$\chi$-退化窓 — 予想 KE-P の反証・TYPE-0 の新設・機構

**追補: 2026-07-29(裁定 173・司令塔追補検分)。入力 = `search/certs/wall_miner_v5_20260729.json`(v5 一発走り・GAP 一レーン)。**

### 11.0 データ(証明書からの機械転写)

| 欄 | `W-A-B3idx6-s1` | **`W-A-B3idx126-s2`** | **`W-A-B3idx126-s3`** |
|---|---|---|---|
| `abs_Bq` / `abs_PN` | 6 / 1 | 126 / **21** | 126 / **21** |
| `N_ord` | 1 | **3** | **3** |
| `c_in_N` | true | true | true |
| `charming_count` / `shadow_total` | 1 / 1 | 2 / 6 | 2 / 6 |
| `settled_total_evaluated` / `settled_fail_count` | 1 / 0 | **12 / 6** | **12 / 6** |
| `settled_fail_witnesses` | — | **全 6 件が $m=2$**(先頭は $f=()$) | **全 6 件が $m=2$** |
| `isotropy_order` / `ker_size` | 1 / 1 | **6 / 6** | **6 / 6** |
| `chi_image_order` / `phi_2Nord` | 1 / 1 | **1 / 2** | **1 / 2** |
| `ta_predicted_ker` / `ta_assert_holds` | 1 / true | **3 / true** | **3 / true** |
| `chi_surjective_assert` | true | **false** | **false** |
| `derived_series_orders` / `derived_length` | [1] / 0 | **[6,1] / 1**(可換) | **[6,1] / 1**(可換) |

$M=N_{\rm ord}=3$、$2M=6$、charming は $\gcd(2m+1,3)=1$ すなわち $m\in\{0,2\}$(✓ `charming_count = 2`)。

> **★ E9(二段 assert)の実地検証**: この窓で `ta_predicted_ker = |G|/\varphi(2N_{\rm ord}) = 6/2 = 3` は**実測 `ker_size = 6` と食い違う**。にもかかわらず `ta_assert_holds = true` — v5 miner が焚いているのが**普遍形** $|\ker|\cdot|Q_N|=6\cdot1=6=|G_N|$ だからである。**v1 のまま $\varphi$ 版を無条件 assert していれば、この窓で偽の FAIL が出て掃引が止まっていた。** E1/E9 の型ゲートは机上の慎重さではなく、**実際に発火する分岐**だった。

### 11.1 ① 予想 KE-P は**反証された**(射程外ではない)

$G_N$ は可換(`derived_length = 1`)で $|G_N|=6$、$\mathfrak F_0=\ker\widetilde\chi=G_N$ は位数 6 $\ne1$。**§3.2 に書いた素形の KE-P はこれで偽である。** 「射程外」で逃げない — **私が書いた命題がそのまま反証された**。

正しい修理は**全射ゲート**であり、isolated ではなく $\widetilde\chi$ の全射性を前件に置く:

> ### 予想 KE-P$'$(全射ゲート版・candidate・未証明)
> $G_N=GTSh(N,N)$ が**可換**かつ **$\widetilde\chi_{2M}$ が全射**($Q_N=(\mathbf Z/2M)^\times$)ならば $\mathfrak F_0=1$、同値に $|G_N|=\varphi(2N_{\rm ord})$。

* **反例は KE-P$'$ に触れない**: `idx126-s2/s3` は `chi_surjective_assert = false`(むしろ $Q_N=1$ で最大に非全射)。したがって**前件を満たさない**。
* **篩としての用途は保たれる**: 全射証明書のある窓で $|\mathfrak F_0|=|G_N|/\varphi(2M)$ が素数 $p>1$ なら、KE-P$'$ から $G_N$ は非可換、補題 P より**等号成立**。§7.5 の priority 1 の箱が(全射窓に限って)空になる、という v1 の狙いはそのまま残る。**依然として未証明であり、篩に使ってはならない。**
* **isolated ゲートでも同じ**: T-A(4′) より isolated + (AR) ⟹ 全射なので、KE-P$'$ は isolated 窓を含む。**より弱い前件(全射)で書くほうが射程が広い。**

### 11.2 **副産物 — $\chi$-退化は非 isolated の無料の証明書**

> **命題 NI(non-isolation detector).** (AR) の下で、$\varphi(2N_{\rm ord})>1$ かつ $\operatorname{Im}\widetilde\chi_{2M}\ne(\mathbf Z/2M)^\times$ なる $N$ は **isolated ではない**。
> **証明.** $N$ が isolated なら T-A(4′) より $\widetilde\chi$ は全射。対偶。$\blacksquare$

`idx126-s2/s3` は $\varphi(6)=2>1$ かつ $Q_N=1$ ゆえ **非 isolated が確定**する(【KE-g】への最初の実弾)。逆に `idx6-s1` は $\varphi(2)=1$ なので**何も言えない**(全射は自明に成立)— **$\varphi(2N_{\rm ord})>1$ の但し書きは load-bearing**。
掃引 schema に `not_isolated_certified = (phi_2Nord > 1) and (chi_image_order != phi_2Nord)` を足すことを提案する(既存 2 欄からの導出・追加計算ゼロ)。

### 11.3 ② 分類 — TYPE-0(自明型)を新設し、反例の勘定から分ける

**採用可**。ただし「数えない」ではなく「**別の型として数える**」。根拠は T-B が $Q_N=1$ でこの窓を**計算なしに予言してしまう**ことである:

$$Q_N=1\ \Longrightarrow\ \Lambda^2Q_N=0,\quad (\mathfrak F_0^{\rm ab})_{Q_N}=G_N^{\rm ab}
\ \Longrightarrow\ \ker\widetilde\chi/[G_N,G_N]\ \cong\ G_N^{\rm ab}.$$

したがって:

> ### 分類(v2.1)
> * **TYPE-0($\chi$-退化型)**: $Q_N=\operatorname{Im}\widetilde\chi=1$。このとき $\ker\widetilde\chi=G_N$ で
>   $$\text{等号}\iff G_N=[G_N,G_N]\iff G_N\ \text{は完全群}.$$
>   $G_N$ が可解(観測範囲では常に)なら **$G_N=1$ のとき等号成立・$G_N\ne1$ のとき等号破れ**、という**自明な二分**になる。
>   - `idx6-s1`: $G_N=1$ ⟹ **等号成立**(自明)。
>   - `idx126-s2/s3`: $G_N\cong C_6\ne1$ ⟹ **等号破れ(TYPE-0)**。
> * **TYPE-L(実質型)**: $Q_N\ne1$ で破れる。$L01$ がこれ($Q_L=(\mathbf Z/12)^\times$ 全射で破れ)。**T-B の coker を実際に計算しないと判定できない**のはこちらだけ。

**分ける理由(3 つ)**:
1. **数学的内容が違う**: 等号問題の内容は「円分指標の核が交換子群と一致するか」であり、$Q_N=1$ では指標が何も見ていない。残る主張「$G_N$ が完全群か」は**算術的内容ゼロ**の純群論。
2. **命題 NI により TYPE-0($\varphi(2N_{\rm ord})>1$)は非 isolated** — $GTSh(N,N)$ は $\operatorname{Ih}$ の受け皿ですらない。壁キャンペーンの推論規則(TIER 昇格)は Ihara 像の話なので、**この窓に適用する意味がない**。
3. **反例の希少性の統計を汚す**: 「25 窓中 1 例」という L の希少性は TYPE-L の中での希少性である。TYPE-0 を同じ箱に入れると混ざる。

**schema への反映**(既存欄から導出・追加計算ゼロ):

```text
chi_degenerate      = (chi_image_order == 1)
equality_type       = TYPE_0_TRIVIAL   if chi_degenerate
                    | TYPE_L_SUBSTANTIVE if (!chi_degenerate && !kerchi_equals_derived)
                    | EQUAL              otherwise
```
**TIER 昇格・反例カウント・§7.5 の探索優先度は `equality_type == TYPE_L_SUBSTANTIVE` にゲートする。**

### 11.4 ③ 機構 — $u$-twist が商へ降りない($T_{m,1}$ の非降下)

**(a) $G_N$ の実体**: 位数 6 の可換群は $C_6$ のみ(`derived_series_orders = [6,1]` が可換を確定)。$C_2\times C_3=C_6$ なので**同じもの**。すなわち $G_N=\mathfrak F_0\cong C_6$、$[G_N,G_N]=1$。

**(b) なぜ $\widetilde\chi$ が完全に潰れるか — 証明書が直接示す**: `settled_total_evaluated = 12` は charming 2 層($m=0,2$)$\times$ 6 個。`settled_fail_witnesses` の**6 件すべてが $m=2$**。すなわち

$$\boxed{\ \text{full hexagon を通る候補は $m=0$ と $m=2$ に 6 個ずつあるが、$m=2$ の層は\textbf{全滅}(source kernel $\ne N$)}\ }$$

isotropy 群に残るのは $m=0$ の 6 個だけ ⟹ $Q_N=1$。**これは F79-2.1 が警告した「source が $N$ とは限らない」現象が、$m\ne0$ 層に集中して起きた実例**である。

**(c) 一段だけ掘る — 非降下の群論的な理由(証明つき)**: 失敗 witness の先頭が $(m,f)=(2,\ ())$、すなわち **$f$ 補正なしの純 twist** であることが効く。

> **補題 $\chi$-DEG.** $A:=PB_3/N$、$u:=2m+1$ とする。**$A$ が可換で $\gcd(u,|A|)=1$ ならば $(m,1)$ は settled**(source kernel $=N$)。
> **証明.** $T_{m,1}$ は $x\mapsto x^u$、$y\mapsto y^u$ で決まる自由群の自己準同型なので、語 $w(x,y)$ に対し $P_N(T_{m,1}(w))=w(\bar x^{\,u},\bar y^{\,u})$。$A$ が可換なら右辺 $=\bigl(w(\bar x,\bar y)\bigr)^u$、すなわち $P_N\circ T_{m,1}=(\ \cdot\ )^u\circ P_N$。$\gcd(u,|A|)=1$ なら $u$ 乗写像は $A$ の自己同型だから $\ker(P_N\circ T_{m,1})=\ker P_N=N$。$\blacksquare$
> **対偶(この窓への適用)**: $|A|=21$、$u=2\cdot2+1=5$、$\gcd(5,21)=1$。しかし $(2,1)$ は settled に**失敗している**。ゆえに
> $$\boxed{\ PB_3/N\ \text{は\textbf{非可換}(位数 21 = $C_7\rtimes C_3$ 型)}\ }$$
> が**証明書から従う**(証明書は $|PB_3/N|=21$ しか報告していないが、settled 失敗が構造を決める)。実際 `settled_fail_witnesses` の $f$ は 7-サイクル(`(4,5,8,6,7,9,10)` 等)で、7-部分が動いていることと整合する。

**(d) 分類の言葉(これで十分と判断)**:

> **「隠れ素数型 $\chi$-退化」**: $N_{\rm ord}=3$ は $PB_3/N$ の位数 $21=3\cdot7$ の **$3$-部分しか見ていない**。細分指標が住む水準 $2N_{\rm ord}=6$ は $7$ と互いに素なので、**$7$-部分は $\widetilde\chi$ から完全に不可視**である。一方 $u$-twist($u\ne1$)は $7$-部分に非可換的に作用し、$N$ を保たない。結果として「指標が見ない場所が、指標の定義域そのものを削る」— **$m\ne0$ 層が settled で全滅し、$\widetilde\chi$ が潰れる。**
> **予測(未検証・安価)**: この機構が正しいなら、**$\gcd$ が $1$ でない大きな素因子を $|PB_3/N|$ に持ち、かつその素因子が $2N_{\rm ord}$ を割らない窓**が $\chi$-退化の候補である。掃引は $|PB_3/N|$ と $N_{\rm ord}$ を既に全窓で持つので、**追加計算ゼロで候補を先に列挙できる**。→【KE-j】

### 11.5 v2.1 の未閉鎖項

* 【KE-i′】(KE-i を差し替え)**予想 KE-P$'$(全射ゲート版)の証明または反証**。素形は死んだ。
* 【KE-j・新設】$\chi$-退化の予測($|PB_3/N|$ の「隠れ素因子」)を掃引で先読み検査(追加計算ゼロ)。
* 【KE-k・新設】`not_isolated_certified` 欄と `equality_type` 欄の schema 追加(いずれも既存欄からの導出)。
* **根拠の質**: 本節の入力 `wall_miner_v5_20260729.json` は **GAP 一レーン・v5 の一発走り**。補題 $\chi$-DEG は紙上証明だが、それが適用する事実(`settled` 失敗)は単系統。**「$PB_3/N$ は非可換」は単系統証明書に依存する導出**である。二系統化は $PB_3/N$(位数 21)の可換性を node で 1 行測れば足りる。
