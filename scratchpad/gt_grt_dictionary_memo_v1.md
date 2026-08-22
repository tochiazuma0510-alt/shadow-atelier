# GT ↔ grt 翻訳メモ v1 — pro-unipotent 側と有限 GTSh 側の辞書・Soulé 輸入の可否・graded 簿記

`DIR: 反例側(graded 影・unipotent 版井原の反証)+正側(タスク B = Im(Ih_N) 下界)/ FRAME: Lie-graded(grt)× B₃-gentle/B₄-proper の辞書`

**状態札**: `mixed — §2 は定理(自前証明)/ §3.2 は定理(自前証明)/ ★§3.3 は新結果(paper-proof + GAP 単系統・独立照合前)/ §2.6・§4 は candidate / 封印非接触 / 窓の候補値(48 元の f 値)非接触`

> ## ⚠ 訂正バナー(2026-08-22・Sol 便 156 = 条件付き受理 → 5 条件執行済)
> **本文 §2〜§3 は初版のまま残置(versioned 規律)。読む前に必ず **§8** を見ること。** 訂正は 7 箇所に **⚠訂正 C1〜C5-g** のマーカーを埋め込み、逐語の正本は **§8** に置いた。とくに:
> **C1** $X_3$ は開曲線 $U_3=E\setminus S$($\hat\pi_1(E)$ ではない)・ℚ 上の deck 群は $\mu_3$ / **C2** 重み完全列は localization sequence・**分裂主張は削除**(C3-LIFT に不要)/ **C3** T-ARITH の「全 $K$」→「**全細分 $K\le N$**」/ **C4** (S7) は全 reduction fibre の死亡証明書へ強化 / **C5** A5 の格境界(D3(iv) 分離・D4 の $e=0$ 文・**𝔤𝔯𝔱^hex → 斉次 hexagon 解空間**・294/42 は retrospective agreement・$\mathrm{nilvis}_p$・**972 は保留**)。
> **§7.7 の (S1)(S3)(S7) は §8.7 の改訂版が正本**(旧逐語は参照専用)。

- 起草: 影工房 数学者(Claude / Opus 5)・2026-08-22
- 委嘱: 司令塔(転進判断の入力)。配達文献 4 本(金庫 `intel/grt_papers/`)= §1.3。
- 正典: `docs/week1-定義ノート.md` / 2401.06870 / 2405.11725。工房既在: `docs/notes/c83_closure_index_v1.md`・`scratchpad/c83_inn_lift_lemma_v1.md`・`docs/notes/bhunt_l1_bridge_v1.md`・`docs/notes/b4_direct_adjudication_feasibility_v1_2.md`・`docs/notes/b_type_synthesis_design_v1_addendum_l4b_grt12.md`。
- **novelty 規律**: §3 の Soulé 輸入は **工房初ではない** — `bhunt_l1_bridge_v1.md`(2026-08-06・補題 BH-BRIDGE)が NW(7) 窓で既に実行済み。本メモの新規部分は §3.2(不可の定理)と §3.3(83 窓の新機構)に限る。

---

## §0 裁定サマリ(三行 + 一枚)

| タスク | 裁定 | 一言 |
|---|---|---|
| **A(辞書)** | **定理 5 本で確立**(D1〜D5) | pro-ℓ 側から見える窓は poset の**極小部分**(F₂/N_{F₂} が冪零 ℓ 群のものだけ)。V=N/K_p は確かに gr の 1 層で、T-DEF は grt の線型化 hexagon の相対版。**gr が忘れるのは拡大類 e ∈ H²(Q,V)**(= KER-π の主役)。**𝒯(fake torus)= 𝔤𝔯𝔱^hex の重み 1 の直線 K(X−Y)** — pentagon が Remark 6.3 で殺す方向そのもの(**一次資料で確認**)。 |
| **B(Soulé 輸入)** | ★**83 窓へは構造的に不可(定理 NILP-VOID)。ただし別機構で目的そのものは達成した(★§3.3)** | Soulé/grt 系の情報は **G の最大 pro-ℓ 商**までしか降りず、83 窓ではそれが G^ab=C₃、charming で 0 ⟹ **情報量ちょうど 0**(証明つき・GAP で前提を機械確認)。**しかし** 83 窓の非冪零性そのものを使う別経路(C₃-被覆 = 楕円曲線 E: Y²=X³+16、E[2] の 2 分体 ℚ(ζ₃,∛2))で **Im(Ih_N) ∩ ker χ_vir ⊇ C₃** を得た。**下界が 4 → 12 へ・22 候補のうち 4 個(両窓で各 2)が算術的として脱落**。 |
| **C(graded 簿記)** | **見取り図+予言式**(§4) | Frattini 塔(3^98 で死ぬ)を **Zassenhaus 塔**へ置換し、層次元を **Witt 公式**で数える。**𝔽_ℓ 窓の shadow 数の閉じた予言式**を得た — **BIT-252 の実測 294/42 を独立に的中**(§2.5.3)。 |

> ★**本メモの最重要行**: 83 線の「再開条件 = c∉N に効く算術機構」は **誤診である**。Soulé 系が効かない理由は c∉N ではなく **F₂/N_{F₂} が非冪零**であること(定理 NILP-VOID)。そして非冪零性は障害ではなく **資源**だった — 中間の C₃ 層を経由すれば楕円曲線の 2 分体が算術入力を供給する(§3.3)。

---

## §1 記法・入力・引用/自前の分離

### 1.1 記法(正典どおり)
B₃=⟨σ₁,σ₂⟩、x=σ₁², y=σ₂², z=(xy)^{-1}, Δ=σ₁σ₂σ₁, c=Δ²。PB₃=F₂×⟨c⟩、F₂=⟨x,y⟩。
N ∈ NFI_{PB₃}(B₃)、Q=B₃/N、**G := F₂/N_{F₂}**、N_ord=(3.1)、Λ_N=ab(N_{F₂})⊆ℤ²。
Ih(g)=((χ(g)−1)/2, f_g)(2405 (1.5))、Ih_N=PR_N∘Ih(同 (1.11))、GT^arith(N)=Im(Ih_N)、χ_vir([m,f])=2m+1。

### 1.2 正典から引く事実(逐語 pin つき・自前導出はしない)
- **(P1)** g∈G_ℚ の作用: x↦x^{χ(g)}, y↦f_g^{-1}y^{χ(g)}f_g、**f_g ∈ 𝐅̂₂′**(Ihara ICM (2.3.1)(2.3.2) 逐語 = `bhunt_l1_bridge_v1.md` §1.1)。
- **(P2)** χ_vir,N ∘ Ih_N = P̂_{N_ord} ∘ χ、χ 全射(2405 (1.13)・§1.3)。
- **(P3)** arithmetical ⟹ genuine ⟹ charming(2405 §1.3.1)。
- **(P4)** settled(ker T_{m,f}=N)。isolated 窓では全 shadow が settled で GT(N) は群(2401 Prop 3.8/3.14)。
- **(P5)** 2405 **Thm 5.3** の証明が使う算術入力は **χ の全射性と複素共役の 2 つだけ**(本起草者が `papers/txt/2405…txt` 行 1310–1420 を通読して確認)。⟹ **正典が供給する下界は「円分部分のみ」**。これが工房の [11,1] 錨と同一の技術であり、それ以上は正典にない。

### 1.3 配達文献(candidate 情報・§/式番号つきで引用)
| 記号 | 出所 | 本メモでの用途 |
|---|---|---|
| **[W]** | Willwacher, arXiv **1009.1654** §6.1(式 (27)(28)(29)・Def 6.1・Thm 6.2・**Remark 6.3**) | **grt₁ の定義の正**。§2.5 の 𝔤𝔯𝔱^hex はこの (28)(29) から pentagon (27) を落として定義 |
| **[NW]** | Naef–Willwacher, arXiv **2508.08081**(Thm 1・Conj 2・**Cor 7**・式 (3)) | **Deligne–Drinfeld 予想は weight ≤ 29 で検証済**(Cor 7 逐語: "Conjecture 2 holds in all weights up to and including weight 29")。Conj 2 = free ⊆ grt₁ ⊆ ds ⊆ kv₂ が **weight ≤ 29 で全て同型**。⟹ **dim 𝔤𝔯𝔱_w(w≤29)= 自由 Lie 値(奇重み ≥3 に生成元 1 本)** = §4 の表 |
| **[Wi2]** | Willwacher, arXiv **2508.13724**(GC₂ の 11-loop) | 「大規模厳密計算が中心予想を殺す」の現行例。本メモでは型のみ言及(§4 注) |
| **[Br]** | Brown, arXiv **1102.1312** | σ_{2n+1} 生成のモチーフ側正典(§3.1 で「Galois の足跡」の出所として名指す) |

> **[NW] Cor 7 の正確な意味(司令塔の要求)**: 「weight 29 まで」= 式 (1) の 4 つの Lie 代数(free / grt₁ / ds / kv₂)の**重み次数付き成分**が W ≤ 29 で一致することの検証。係数体は ℚ(実装は有限体 rank 計算)。深さ方向は Figure 1 の (W,D) 表の範囲。**「dim 𝔤𝔯𝔱₁₆ は 4 か 5 か未決着」という工房の L-4c 文献要請は、これで解決 = 5**(自由 Lie 値・§4 の表)。

### 1.4 本メモが自前で証明するもの
定理 **D1**(pro-ℓ 窓族)/ 定理 **D2**(情報の行き先)/ 定理 **D3**(V = gr の 1 層)/ 定理 **D4**(gr が忘れるもの)/ 命題 **D5**(𝔤𝔯𝔱^hex 重み 1 = 𝒯)/ ★定理 **NILP-VOID** / ★定理 **C3-LIFT**(83 窓の算術下界)。

---

## §2 タスク A — 辞書(定理つき)

### 2.1 定理 D1(pro-ℓ 窓族は NFI の中に実在し、逆極限が pro-ℓ 側を復元する)

> **定理 D1.** ℓ を素数、k ≥ 2、j ≥ 1 とし
> $$\mathbf N(\ell,k,j) := \gamma_k(PB_3)\cdot PB_3^{\,\ell^j}.$$
> **(0)** $\mathbf N(\ell,k,j) \in \mathrm{NFI}_{PB_3}(B_3)$。
> **(1)** $\mathbf N(\ell,k,j) = \bigl(\gamma_k(F_2)F_2^{\ell^j}\bigr)\times\langle c^{\ell^j}\rangle$、したがって
> $$G = F_2/\mathbf N_{F_2} = F_2/\gamma_k(F_2)F_2^{\ell^j}\quad(\text{階数 2 の自由冪零 }\ell\text{ 群}),\qquad N_{\rm ord}=\ell^{j'}\ (\text{ℓ 冪}),\qquad c\notin \mathbf N .$$
> **(2)** $\varprojlim_{k,j}\bigl(\mathbb Z/N_{\rm ord}\times F_2/\mathbf N_{F_2}\bigr) = \mathbb Z_\ell\times F_2^{(\ell)}$。すなわちこの部分族の上での shadow 座標 $(m,f)$ の逆極限が **pro-ℓ 側の座標 $(\lambda, q_\ell(f))$ をちょうど復元する**。
> **(3)(反対側)** $N \supseteq \mathbf N(\ell,k,j)$ なる $N\in\mathrm{NFI}$ は、**$F_2/N_{F_2}$ が冪零 ℓ 群であるものに限る**。したがって $\{\mathbf N(\ell,k,j)\}$ の上側集合は NFI の中で **cofinal ではない**。

**証明.** (0) $\gamma_k(PB_3)$ と $PB_3^{\ell^j}$ は $PB_3$ の characteristic 部分群、$PB_3\trianglelefteq B_3$ ゆえ両者とも $B_3$ で正規、積も正規。$PB_3$ は有限生成で $PB_3/\gamma_kPB_3^{\ell^j}$ は有限生成冪零・有限指数冪 ⟹ 有限。⊆ PB₃ は自明。
(1) $PB_3=F_2\times\langle c\rangle$ で $c$ 中心ゆえ $\gamma_k(PB_3)=\gamma_k(F_2)$。$PB_3^{\ell^j}$ は $(uc^n)^{\ell^j}=u^{\ell^j}c^{n\ell^j}$ たちで生成されるから $\gamma_k(F_2)PB_3^{\ell^j}=\bigl(\gamma_k(F_2)F_2^{\ell^j}\bigr)\times\langle c^{\ell^j}\rangle$(直積分解が保たれる)。ゆえに $\mathbf N\cap F_2=\gamma_k(F_2)F_2^{\ell^j}$。$c^{\ell^j}\in\mathbf N$ かつ $c\notin\mathbf N$($j\ge1$)。
(2) $\varprojlim_k F_2/\gamma_kF_2^{\ell^j}\ (j\to\infty) = F_2^{(\ell)}$ は pro-ℓ 完備化の定義。$N_{\rm ord}$ は $\bar x,\bar y,\bar c$ の位数の lcm でいずれも ℓ 冪。
(3) $N\supseteq\mathbf N$ ⟺ $N_{F_2}\supseteq\gamma_kF_2^{\ell^j}$ ⟺ $G$ が自由冪零 ℓ 群の商 ⟺ $G$ が冪零 ℓ 群。83 窓($|G|=192$、非冪零 — §3.2 で機械確認)も 972 窓($G$ が $PSL(2,8)$ 因子を持つ)もこれを満たさない。∎

> **辞書の第一行(移るもの/移らないもの)**
> | 対象 | pro-ℓ GT 側 | 有限窓側 | 移るか |
> |---|---|---|---|
> | hexagon (3.3)(3.4) | (I)(II)(Ihara) | mod N の同式 | **移る**(方程式が同型) |
> | 群法則 (3.53) | GT の合成 | 同 | **移る** |
> | χ_vir | $\lambda\in\mathbb Z_\ell^\times$ | $2m+1 \bmod N_{\rm ord}$ | **移る** |
> | charming | $f\in[F_2^{(\ell)},F_2^{(\ell)}]$ | $f\in[G,G]$ | **移る** |
> | pentagon | grt では (27) | gentle にはない | **移らない**(§2.5) |
> | **poset の位置** | $\mathcal P_\ell$(冪零 ℓ 群窓のみ) | NFI 全体 | **移らない — $\mathcal P_\ell$ は cofinal でない**(D1(3)) |

### 2.2 定理 D2(pro-ℓ 情報の行き先はちょうど最大 ℓ 商)

> **定理 D2.** $\pi:\hat F_2\twoheadrightarrow G$ を窓の射影、$q_\ell:\hat F_2\to F_2^{(\ell)}$ を pro-ℓ 完備化とする。$\hat f\in\hat F_2$ について「$q_\ell(\hat f)$ を知ることから決まる $\pi(\hat f)$ の情報」は、**ちょうど $\pi(\hat f)$ の $G/O^\ell(G)$(= G の最大 ℓ 商)における像**である。全素数を併せた場合(pro-冪零完備化)は **$G/\gamma_\infty(G)$(= G の最大冪零商)における像**。
> さらに: **$\ell\nmid |G^{\rm ab}|$ ならば $G/O^\ell(G)=1$**、そして **$(G/O^\ell(G))^{\rm ab}=(G^{\rm ab})_\ell$**。

**証明.** $\pi(\ker q_\ell)$ は $G$ の正規部分群で、$G/\pi(\ker q_\ell)$ は pro-ℓ 群 $F_2^{(\ell)}$ の商ゆえ ℓ 群。逆に $G$ の任意の ℓ 群商は $\hat F_2$ の pro-ℓ 商を経由するので $\ker q_\ell$ を殺す。ゆえに $\pi(\ker q_\ell)=O^\ell(G)$。冪零版も同様($\hat F_2$ の pro-冪零完備化 $=\prod_\ell F_2^{(\ell)}$)。最後の 2 文: ℓ 群 $H$ で $H^{\rm ab}=1$ なら $H=1$(Burnside 基底定理)、かつ $(G/O^\ell(G))^{\rm ab}$ は $G^{\rm ab}$ の最大 ℓ 商。∎

### 2.3 定理 D3(V=N/K_p は gr の 1 層・T-DEF は線型化 hexagon)

$K_p:=[N,N]N^p$、$V:=N/K_p=H_1(N;\mathbb F_p)$($\mathbb F_p[Q]$-加群)。

> **定理 D3.**
> **(i)** $K_p=\Phi_p(N)$(mod-p Frattini)であり、$V$ は $N$ の **mod-p 下中心(Zassenhaus)フィルトレーションの第 1 層** $D_1(N)/D_2(N)$ に一致する。$\bigoplus_i D_i(N)/D_{i+1}(N)$ は $\mathbb F_p$ 上の次数付き制限 Lie 代数で $Q$ が作用する。
> **(ii)** shadow $[m,f]\in GT(N)$ の $GT(K_p)$ への持ち上げ全体は、空でなければ、T-DEF の線型解空間 $\bar x^\nu U_0 \cap ab^{-1}((\nu,-\nu)+\Lambda_{K_p})$ 上の**アフィン**な集合である(逐語 = `c83_inn_lift_lemma_v1.md` §2.6)。
> **(iii)** $U_0=\ker(1-\bar\sigma_1+\bar\sigma_1\bar\sigma_2)\cap\ker(1-\bar\sigma_2+\bar\sigma_2\bar\sigma_1)$ が含意する $\bar\Delta v=-v$ は、**[W] (29) $\psi(X,Y)+\psi(Y,X)=0$ の群論的相対版そのもの**である($\mathrm{Ad}(\Delta)$ は $x\leftrightarrow y$ = θ、(1.13))。同様に $\mathrm{Ad}(\delta)=\mathrm{Ad}(\sigma_1\sigma_2)$ は τ($x\to y\to z\to x$)で、簡約 hexagon (3.11) の線型化が **[W] (28) $\psi(X,Y)+\psi(Y,Z)+\psi(Z,X)=0$($Z=-X-Y$)**にあたる。
> **(iv)(★橋の正確な位置)** $N=\mathbf N(\ell,k,j)$(定理 D1)かつ $p=\ell$ のとき、$V$ の中の重み $k$ 成分は自由 Lie 代数の次数 $k$ 部分 $\mathrm{Lie}_k\otimes\mathbb F_\ell$ で、$Q$ は $S_3$ 作用と円分捻りで作用する。この場合 **$U_0$ は $\mathfrak{grt}^{\rm hex}_k\otimes\mathbb F_\ell$ に一致する**(§2.5.3 の数値一致がその証拠)。一般の窓では $V$ は非冪零被覆群の $H_1$ であり、**重み次数も grt 解釈も存在しない**。

> **⚠訂正 C5-a(便 156・§8.5)**: **(iv) は定理 D3 から分離する**。(i)(ii)(iii) のみが定理で、**(iv) は【GAP-DICT-1】candidate**(根拠は数値一致のみ・構成的証明なし)。以後 (iv) を「定理 D3 の一部」として引用しない。

**証明.** (i) 定義から $[N,N]N^p=\Phi_p(N)$、$D_1=N$、$D_2=[N,N]N^p$。(ii) は `c83_inn_lift_lemma_v1.md` 定理 T-DEF そのもの(本メモは再証明しない・引用)。(iii) は (1.13) と導出 1((3.3) 節の $\delta x\delta^{-1}=y$)から作用素の同定が従う(同ノート §2.6 の系「$\bar\Delta v=-v$」が加法記法で (29) である)。(iv) の一致は §2.5.3 の 2 系統一致による **candidate**(構成的証明は与えていない — 【GAP-DICT-1】)。∎

### 2.4 定理 D4(gr が忘れるもの = 拡大類)

> **定理 D4.** 1 → V → B₃/K_p → Q → 1 の拡大類を $e\in H^2(Q,V)$ とする。次数付きデータ $(V,\ Q\text{-作用},\ U_0)$ は **$e$ を忘れる**。持ち上げの障害はこの $e$ から作られる類であり、実際 **KER-π**(`c83_inn_lift_lemma_v1.md` §3)が $\ker(\pi^*)=\mathrm{End}_{\mathbb F_p[Q]}(V)\cdot e$ を与える。⟹ **同型な $(V,Q)$ をもつ 2 つの窓が、異なる $e$ ゆえに異なる survival 挙動をもち得る。**
> ゆえに「grt の影で有限窓を語る」対応は **影であって同値ではない**。~~同値になるのは拡大が分裂($e=0$)する場合に限る。~~
> **⚠訂正 C5-b(便 156・§8.5)**: 取り消し線部は**過大**。$e=0$ は**この一つの障害を消すだけ**で、grt と有限窓の全情報の同値は与えない。正 =「$e$ を忘れることで持ち上げ障害の情報が失われる」まで。

**証明.** $(V,Q)$ は $e$ の情報を含まない(同じ $(V,Q)$ に対し $H^2(Q,V)$ は一般に非零で、異なる類が異なる群 $B_3/K_p$ を与える)。障害の記述は KER-π。∎

> **系(規律)**: 「$\mathfrak{grt}$ で次元が合ったから有限窓でも合う」は **禁句**。合うのは $V$ の線型部分までで、貼り合わせは別勘定。§2.5.3 の 294/42 一致は「合った」という**測定**であって、この系の反例ではない(その窓では $e$ の寄与が見えていないだけ)。

### 2.5 ~~𝔤𝔯𝔱^hex — hexagon だけを課した Lie 代数~~ → **斉次 hexagon 解空間 $\mathcal H$**(便 156 改称)

> **⚠訂正 C5-c(便 156・§8.5)**: **「Lie 代数」と断言しない**。Ihara bracket での閉性は【GAP-HEX-1】未解決ゆえ、本節の対象は **斉次 hexagon 解空間 $\mathcal H_w:=\{\psi\in\mathrm{Lie}_w(X,Y):\text{(28)}\wedge\text{(29)}\}$** と呼ぶ(次元計算に bracket 閉性は不要)。以下の記号 $\mathfrak{grt}^{\rm hex}_w$ は $\mathcal H_w$ と読み替えること。
> **⚠訂正 C5-d(便 156・§8.5)**: §2.5.2 の次元表は **candidate**。2 大素数一致は有理 rank の**下界**を与えるにとどまる(mod-p rank ≤ 有理 rank)。厳密化には fraction-free 有理消去 or SNF 証明書が要る。

#### 2.5.1 定義(可能・[W] の定義から pentagon を落とすだけ)

[W] §6.1 の grt₁ は $\psi\in\hat{\mathrm{Lie}}(X,Y)$ で (27)(pentagon)・(28)(hexagon)・(29)(反対称)を満たすもの。そこで

$$\boxed{\ \mathfrak{grt}^{\rm hex} := \{\psi \in \hat{\mathrm{Lie}}(X,Y)\ :\ \text{(28)}\wedge\text{(29)}\}\ \supseteq\ \mathfrak{grt}_1,\qquad \mathfrak{grt}^{\rm hex}_{\rm gen}:=\mathfrak{grt}^{\rm hex}\cap \hat{\mathrm{Lie}}^{\ge2} }$$

- (28)(29) は重み次数について斉次なので $\mathfrak{grt}^{\rm hex}=\bigoplus_w \mathfrak{grt}^{\rm hex}_w$。**次元は純粋な線型代数で計算できる**(§2.5.2)。
- **Ihara bracket で閉じるか**は本メモでは未証明 —【GAP-HEX-1】(candidate。grt₁ が閉じる標準証明は 3 条件を個別に保存する形で進むので、(28)(29) だけでも閉じる見込みは高い)。次元表は Lie 構造に依らないので以下の結論には影響しない。
- **charming の線型化**: [W] **Remark 6.3** 逐語「It also follows from (24) that Φ contains no terms linear in X, Y」— すなわち **pentagon が重み 1 項を殺す**。gentle 側の charming($\hat f\in[\hat F_2,\hat F_2]$)はまさにこの帰結だけを残したもの ⟹ **$\mathfrak{grt}^{\rm hex}_{\rm gen}$ が gentle の Lie 影**。

#### 2.5.2 ★次元表(本メモで新規計算・2 素数一致)

自前実装(Dynkin 冪等元で $\mathrm{Lie}_w\subseteq A_w$ を張り、(28)(29) を非可換代入で線型方程式化、$p=2^{31}-1$ と $998244353$ の 2 素数で rank)。

| $w$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\dim \mathrm{Lie}_w$ | 2 | 1 | 2 | 3 | 6 | 9 | 18 | 30 | 56 | 99 | 186 | 335 |
| **$\dim\mathfrak{grt}^{\rm hex}_w$** | **1** | 0 | 1 | **1** | **2** | **3** | **6** | **10** | **19** | **33** | **62** | **112** |
| $\dim\mathfrak{grt}_w$([NW] Cor 7 で $w\le29$ 確定) | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 2 | 2 |
| **超過** | 1 | 0 | 0 | **1** | 1 | 3 | 5 | 9 | 18 | 32 | 60 | 110 |

手検算 2 点(独立): $w=1$: $\psi=aX+bY$、(29) ⟹ $a+b=0$、(28) は恒真 ⟹ **1 次元 = $K(X-Y)$** ✓。$w=2$: $\psi=a[X,Y]$、(29) 恒真、(28) ⟹ $3a[X,Y]=0$ ⟹ $a=0$ ✓(★**標数 3 では消えない** — mod 3 計算の注意点)。$w=3$: 1 次元 = 工房の **D3-BLIND(hexagon 深さ 3 ⟺ $a=b$)** と一致 ✓。

> **読み(candidate)**: **gentle 緩和は無害な記帳の便宜ではない。** graded/unipotent 水準では hexagon-only は grt より**指数的に大きい**($\dim\mathfrak{grt}^{\rm hex}_w\approx\dim\mathrm{Lie}_w/3$ 対 多項式増大)。最初の超過は重み 1(= 𝒯)、pentagon 由来の charming を課した後の最初の超過は **重み 4**(1 対 0)。
> ⟹ **「$\widehat{GT}=\widehat{GT}_{\rm gen}$?」の pro-unipotent 版は NO 側に強く傾く**(ただし profinite 版の証明ではない —【GAP-HEX-2】: $\widehat{GT}_{\rm gen}$ の associated graded が $\mathfrak{grt}^{\rm hex}$ を**満たす**ことは (28)(29) の線型化から出るが、**等号**(解が全部実現される)は未証明)。

#### 2.5.3 ★2 系統一致 — 工房の BIT-252 実測を graded 表が的中させる

NW(7) 窓(`b4_direct_adjudication_feasibility_v1_2.md` §1.1): $N_{F_2}=\gamma_5(F_2)F_2^{7}$、$P=F_2/N_{F_2}$($7^8$)、$N_{\rm ord}=7$、$|\mathcal X|=6$。本走測定 = **hexagon 294・PENT_W 42・hexagon-only 252**。

- $294/6 = 49 = 7^{2}$、$42/6 = 7 = 7^{1}$。
- 本メモの表の重み 2,3,4 の和: $\mathfrak{grt}^{\rm hex}$: $0+1+1 = \mathbf{2}$;$\mathfrak{grt}$: $0+1+0 = \mathbf{1}$。
- $$\boxed{\ 294/6 = 7^{\,\dim\mathfrak{grt}^{\rm hex}_{2}+\dim\mathfrak{grt}^{\rm hex}_{3}+\dim\mathfrak{grt}^{\rm hex}_{4}} = 7^2,\qquad 42/6 = 7^{\,\dim\mathfrak{grt}_{2}+\dim\mathfrak{grt}_{3}+\dim\mathfrak{grt}_{4}} = 7^1\ }$$

~~**二つの完全に独立な系統(工房の GAP 悉皆 vs 本メモの char-0 線型代数)が一致した。**これは §2.3(iv) の橋の強い実証であり、同時に **BIT-252 の数値の独立裏取り**でもある(工房側は「実測」、こちらは「予測」— 時系列は工房が先なので予言とは呼ばない)。~~

> **⚠訂正 C5-e(便 156・§8.5)**: 正しい語は **retrospective numerical agreement(事後的な数値一致)**。**D3(iv) が未証明である以上、「独立裏取り」「独立再現」「BIT-252 を証明した」「橋の実証」とは書かない。** 最大文 = 「**既知の GAP 値と、独立な graded 会計とが一致した**」。§0 の表 C 欄の「独立に的中」も同じく **retrospective agreement** へ読み替える。

> **予言 P-GRT-1(事前登録可・未測定)**: 窓 $F_2/\gamma_{6}F_2^{\ell}$(重み ≤5)について
> $$|GT(\mathbf N)| / |\mathcal X| = \ell^{\,0+1+1+2}=\ell^4,\qquad |\mathrm{PENT}_W| / |\mathcal X| = \ell^{\,0+1+0+1}=\ell^2 .$$
> ℓ=7 なら 2401 と 49。**外れたら** (a) mod ℓ で次元が落ちた(= SYN-0 型の段差)か (b) 橋 §2.3(iv) が偽。どちらも情報。

### 2.6 𝒯(fake torus)と BIT-252 の gentle-fake — 位置づけ【candidate】

> **命題 D5(証明つき部分).** $\mathcal T=\{(1,\hat y^\nu\hat x^{-\nu})\}$ の元の Lie 対数の最低次項は $\nu(Y-X)$ で、これはちょうど $\mathfrak{grt}^{\rm hex}_1=K(X-Y)$ を張る。すなわち **𝒯 = 𝔤𝔯𝔱^hex の重み 1 の直線の群水準の化身**であり、[W] Remark 6.3 により **pentagon がまさにこの方向を殺す**。工房の既在定理 $\mathcal T\cap\widehat{GT}_{\rm gen}=\{1\}$ はこの「重み 1 の超過は charming で消える」の profinite 版である。

**証明.** $ab(y^\nu x^{-\nu})=(-\nu,\nu)$、重み 1 の Lie 部分は $\nu(Y-X)$。(29): $\nu(Y-X)+\nu(X-Y)=0$ ✓。(28): $Z=-X-Y$ で $\nu[(Y-X)+(Z-Y)+(X-Z)]=0$ ✓。$\dim\mathfrak{grt}^{\rm hex}_1=1$(§2.5.2)ゆえ張る。∎

**系(T-DEAD の概念的読解)**: T-DEAD(「$\Lambda_{K_n}=n\Lambda_N$ ゆえ $\nu\not\equiv0$ の $[0,f_\nu]$ は $K\le K_3$ 上で厳密族機構が必ず死ぬ」)は、**「重み 1 成分は窓を深くすると必ず可視化されて charming に引っかかる」**の定量版に他ならない。⟹ T-DEAD は grt 側の Remark 6.3 の有限版。

**BIT-252 の gentle-fake【candidate】**: 252 = 294 − 42 は $\ell^2-\ell^1$ ではなく差集合の元数だが、上の指数一致から **252 個はちょうど「$\mathfrak{grt}^{\rm hex}$ の重み ≤4 の余剰方向(重み 4 の 1 次元)が生む層」に対応する**と読める。すなわち **BIT-252 の gentle-fake は「𝔤𝔯𝔱^hex ⊋ 𝔤𝔯𝔱 の重み 4 の超過」の群水準の痕跡**。⟹ 𝒯(重み 1 の超過・charming で死ぬ)と BIT-252(重み 4 の超過・charming を通り pentagon で死ぬ)は **同じ現象の別の重み**。見込み評価 = **高**(数値が指数まで合っているため)。証明は要求されていないので candidate 札のまま。

---

## §3 タスク B — Soulé/σ 元の有限水準輸入

### 3.0 先行実績の申告(novelty grep)

**工房は既に Soulé 輸入を 1 回成功させている**: `docs/notes/bhunt_l1_bridge_v1.md`(2026-08-06)= 補題 **BH-BRIDGE**。舞台は **NW(7) 窓**($N_{F_2}=\gamma_5F_2^7$、$P$ は $7^8$ の 7 群)。鎖は
Ihara ICM §6.2(ii)(Soulé–Deligne 円分元 $\kappa^{(l)}_m$)→ §6.3(Anderson–Coleman–IKY の明示公式)→ 補題 BR-3(**$f_\sigma\equiv-\frac{\kappa^*_3(\sigma)}{2}\mathfrak h_3 \bmod \gamma_4$**)→ $p=7$ で単元性 → Kurihara 1992 で $c(1)$ が $H^1(\mathbb Z[1/p],\mathbb Z_p(3))$ を生成 → **$\mathrm{Ih}_{\mathbf N}(G_{\mathbb Q(\mu_7)})\ne1$**。残余ギャップ =【BR-GAP-1】(正規化 1 段)。
本メモはこれを**繰り返さない**。本メモの寄与は「なぜ 83 窓では同じ手が原理的に使えないか」(§3.2)と「代わりに何が使えるか」(§3.3)。

### 3.1 定義経路と mod p での計算可能性(整理・自前知識)

σ_{2n+1}(Soulé 元)は $G_\mathbb{Q}$ の元ではなく、**pro-ℓ 側の次数付き Lie 代数 $\mathfrak g^\ell$ の元**である。到達経路は 3 本で、どれも pro-ℓ を経由する:

| 経路 | 対象 | mod p での計算可能性 |
|---|---|---|
| **(a) 円分/Kummer** | $\varepsilon_{m,n}=\prod_a(\zeta_n^a-1)^{\langle a^{m-1}\rangle}$ の Kummer 類 ⟹ 1-cocycle $\kappa^{(\ell)}_m: G_\mathbb{Q}\to\mathbb Z_\ell(m)$(ICM §6.2(ii)) | **計算可能**。値は円単数の ℓ 進 Kummer 類。$\kappa_m$ の **mod ℓ 全射性** ⟺ Deligne–Soulé 円分元が $H^1(\mathbb Z[1/\ell],\mathbb Z_\ell(m))\cong\mathbb Z_\ell$ を生成 ⟺ $H^2(\mathbb Z[1/\ell],\mathbb Z_\ell(m))=0$(Kurihara Prop 5.1+Rem 5.2)⟺ **ℓ が重み $m$ で「非正則でない」**(Bernoulli 分子条件・素数ごとに 3 行で判定可) |
| **(b) Jacobi/Gauss 和** | Anderson–Ihara 理論(Coleman, "Anderson–Ihara theory: Gauss sums and circular units" = **2405 の参考文献 [4]**) | 同上。metabelian 商まで一挙に決まる |
| **(c) K 理論/モチーフ** | $K_{2m-1}(\mathbb Z)\otimes\mathbb Z_\ell\to H^1$(Soulé)、$\mathfrak g^\ell\cong$ free(σ₃,σ₅,…)の予想([Br]) | 非消滅は定理、生成の完全性は Deligne–Ihara 予想(未解決) |

**明示公式(ICM §6.3・[$A_3,C_3$,IKY])** は $f_\sigma$ の **$\hat F_2''$ を法とした像(metabelian 部分)を全重み一挙に**与える:
$$\psi^{\rm ab}_\sigma(\xi,\eta)=\exp\Bigl\{\sum_{m\ge3,\ \rm odd}\frac{\kappa^*_m(\sigma)}{m!}\bigl((X+Y)^m-X^m-Y^m\bigr)\Bigr\}\times(\text{偶数重み・}\chi\text{ 依存の因子}).$$
⟹ **「$F_2/N_{F_2}$ が metabelian な ℓ 群」である窓では、$\mathrm{Ih}_N$ の $f$ 座標は $(\chi,\kappa_3,\kappa_5,\dots)$ で完全に決まる**。これが Soulé 輸入の射程の正確な形。

### 3.2 ★定理 NILP-VOID — 83 窓へは不可(構造的・計算困難ではない)

> ### 定理 NILP-VOID
> $N\in\mathrm{NFI}_{PB_3}(B_3)$、$G=F_2/N_{F_2}$ とする。$\mathcal I$ を、$g\in G_\mathbb{Q}$ の不変量で **$q_\ell(f_g)$($\ell$ は任意の素数の集合)と $\chi(g)$ だけの関数**であるもの全体とする(Soulé 指標 $\kappa_m$ 全体・ℓ 進 Magnus 展開の全係数・$\mathrm{Out}(\pi_1^{(\ell)})$ における像・$\mathfrak{grt}$/$\mathfrak g^\ell$ の全次数付きデータ はすべてここに入る)。このとき $\mathcal I$ から決まる $\mathrm{Ih}_N(g)$ の情報は
> $$\Bigl(\chi(g)\bmod N_{\rm ord}\ ,\ \ f_g\ \text{の}\ G/\gamma_\infty(G)\ \text{における像}\Bigr)$$
> に尽きる。さらに **$f_g\in\hat F_2'$**(P1)ゆえ第 2 成分は $G^{\rm ab}$ の中で常に $0$ である。したがって:
> $$\boxed{\ \gamma_2(G)=\gamma_3(G)\ \Bigl(\iff G\text{ の最大冪零商}=G^{\rm ab}\Bigr)\ \Longrightarrow\ \mathcal I\ \text{から得られる }\mathrm{Im}(\mathrm{Ih}_N)\ \text{の下界は }|(\mathbb Z/N_{\rm ord})^\times|\ \text{を超えない}.\ }$$
> すなわち **Soulé/grt 系の情報量はちょうど 0**(2405 Thm 5.3 が χ の全射性だけから既に出す量と同一)。**細かい窓 $K\le N$ を経由しても回避できない**(同じ議論が $K$ に対しても働き、$R_{K,N}$ で押し出しても $G$ の中の値は決まらない)。

**証明.** 定理 D2 より $\mathcal I$ が決めるのは $f_g$ の $G/O^\ell(G)$(全素数併せて $G/\gamma_\infty(G)$)における像のみ。$\gamma_2=\gamma_3$ なら $\gamma_\infty=\gamma_2$ で $G/\gamma_\infty=G^{\rm ab}$。$f_g\in\hat F_2'$ ゆえ $G^{\rm ab}$ での像は $0$。よって $f$ 座標は完全に未定のまま残り、下界は $\chi_{vir}$ 由来の分だけになる。∎

**83 窓での前提の機械確認**(本メモの GAP スクリプト `scratchpad/math_c3cover_test_v2.g`・両窓):

| 窓 | \|G\| | ord(x,y,z,c) | G^ab | IsNilpotent | 下中心列の位数 | \|P\|=\|[G,G]\| |
|---|---|---|---|---|---|---|
| [1152,154161] | 192 | (12,12,12,2) | C₃ | **false** | **[192, 64]**(γ₂=γ₃ で停止) | 64 |
| [1152,154163] | 192 | (6,6,12,4) | C₃ | **false** | **[192, 64]** | 64 |

⟹ **両窓で $\gamma_2(G)=\gamma_3(G)$、最大冪零商 $=G^{\rm ab}=C_3$、最大 pro-ℓ 商は $\ell\ne3$ で自明・$\ell=3$ で $C_3$。**
⟹ **83 窓での Soulé 輸入は不可(理由: 構造的に情報量 0。「計算が重い」ではない)。**

### 3.2.1 972 窓についての一言

972 系の窓は $F_2/N_{F_2}\cong G_9\times PSL(2,8)$ 型(地図 §PH2-VOID)。$PSL(2,8)$ は単純ゆえ $ab=1$、$G_9\le D_9^3$ ゆえ $G_9^{\rm ab}$ は位数 ≤4 の 2 群。したがって **$G^{\rm ab}$ は 2 群で、最大 pro-ℓ 商は $\ell$ 奇で自明・$\ell=2$ で $G^{\rm ab}$ に等しい**(位数 ≤4 の群は可換)。⟹ ~~**同じ理由で Soulé 輸入は不可**~~。工房の既在観測「$G_l^{\rm ab}$ に 3-part なし」はこの定理の特殊例である。

> **⚠訂正 C5-f(便 156 §6.3・§8.5)— 972 は保留**: 「$G^{\rm ab}$ が小さい 2 群」だけからは **最大 2-商が可換とは結論できない**(位数 ≤4 の abelianization をもつ 2 群が非可換でありうる)。**972 への NILP-VOID 適用は、その対象で $\gamma_2=\gamma_3$ または最大冪零商を直接 pin するまで保留**。本メモが主張するのは **83 両窓のみ**(そこでは $\gamma_2=\gamma_3$ が二系統実測済)。

### 3.3 ★★新結果 — 83 窓の算術下界(Soulé 抜き・非冪零性を資源に使う)

**着想**: NILP-VOID が言うのは「冪零方向に情報がない」であって「算術がない」ではない。$G$ は $P\rtimes C_3$($P$ = 位数 64 の 2 群)で、**中間の $C_3$ 被覆を経由すれば「2 群だが冪零でない」構造が使える**。

#### 3.3.1 幾何の同定(自前・初等)

$G^{\rm ab}=C_3$ かつ $\Lambda_N=\{(a,b):3\mid a+b\}$ ⟹ 射影 $F_2\twoheadrightarrow C_3$ は $x\mapsto1,\ y\mapsto1$(ゆえに $z\mapsto1$)。$R:=\ker(F_2\to C_3)$ は階数 4 の自由群で、対応する被覆は $\mathbb P^1\setminus\{0,1,\infty\}$ の **3 点で完全分岐する巡回 3 次被覆**
$$X_3:\ w^3=t(1-t).$$
Riemann–Hurwitz: $2g-2=3(-2)+3\cdot2=0$ ⟹ **$g=1$**。滑化とモデル変換($u=2t-1$、$Y=4u$、$X=-4w$)は $\mathbb Q$ 上で
$$\boxed{\ E:\ Y^2=X^3+16\quad(\cong y^2+y=x^3,\ \text{27a3}),\qquad j=0,\ \mathrm{CM}\ \text{by}\ \mathbb Z[\zeta_3].\ }$$
**2 分体**: $Y=0,\ X^3=-16$ ⟹ $\boxed{\mathbb Q(E[2])=\mathbb Q(\zeta_3,\sqrt[3]{2}),\ \mathrm{Gal}\cong S_3}$。

$R$ は $G_\mathbb{Q}$-安定($G_\mathbb{Q}$ は $F_2^{\rm ab}$ にスカラー $\chi$ で作用するので mod 3 の線型条件を保つ)⟹ **$X_3$ は $\mathbb Q$ 上定義**され、$H_1(X_3;\mathbb F_2)=R/\Phi(R)$(4 次元)は $G_\mathbb{Q}$-加群、重み完全列
$$0\to W_{\mathbb F_2}\ (\dim 2,\ \text{尖点類 }x^3,y^3,z^3;\ \text{Galois 自明})\to H_1(X_3;\mathbb F_2)\to E[2]\to 0 .$$
~~($W'$ は $H_1$(コンパクト)が自由ゆえ飽和・分裂するので mod 2 でも完全。)~~

> **⚠訂正 C1(便 156 §2.1–2.2・§8.1)— 開曲線とコンパクト曲線の分離**: 上の $X_3$ は **開曲線** $U_3:=E\setminus S$、$S=\{O,T,-T\}$、$T=(0,4)$ を指す(座標変換 $u=2t-1,\ X=-4w,\ Y=4u$)。正しい同一視は $\widehat R\cong\hat\pi_1(U_3,\bar{\mathbb Q})$ であり、**$\hat\pi_1(E)$ と書いてはならない**($R$ の階数 4 がその証左)。接ベクトル基点は「基底側の標準 tangential base point とその上の幾何的 lift を一つ選んで得られる同型」であり、**lift の選択を変えても $G_\mathbb{Q}$-加群の同型型は不変**(deck 変換による同型の差のみ)。さらに **ℚ 上の deck 群は定数群 $C_3$ ではなく $\mu_3$**($\bar{\mathbb Q}$ 上で $C_3$)ゆえ、**「ℚ 上の $C_3$-Galois cover」という語は使わない** — Galois は deck 生成元を $\chi \bmod 3$ で捻る。
> **⚠訂正 C2(便 156 §2.3・§8.2)— 完全列の書き方と分裂主張の削除**: 上の完全列は **localization sequence** として書く:
> $$0\to W\to H_1(U_3;\mathbb F_2)\to H_1(E;\mathbb F_2)\to0,\qquad W\cong\widetilde H_0(S;\mathbb F_2)(1)\ (\dim 2).$$
> $W$ が自明 $G_\mathbb{Q}$-加群である理由は「3 尖点が各点 ℚ-rational」かつ「$\mathbb F_2(1)$ が自明」であること。**取り消し線部の「コンパクト部分が自由ゆえ飽和・分裂」は $G_\mathbb{Q}$-同変分裂の理由にならないので削除する。C3-LIFT に分裂は不要**(必要なのは同変完全列と商 $H_1(U_3)/W\cong E[2]$ だけ)。分裂を残す場合のみ「尖点差 $T,-T$ が有理 3-torsion($3T=O$・接線公式より $2T=-T$)で、2 が有理 $C_3$ 上可逆ゆえ mod-2 Kummer 類が消える」に差し替える。

#### 3.3.2 ★決定的計算(GAP・両窓)

`scratchpad/math_c3cover_test_v2.g`:

| 窓 | \|P\| | \|Φ(P)\| | **d(P)** | $W=\langle x^3,y^3,z^3\rangle^G$ | **W ⊆ Φ(P)?** | Ad(x̄) の P/Φ(P) 上の位数 | 固定部分空間 |
|---|---|---|---|---|---|---|---|
| [1152,154161] | 64 | 16 | **2** | 位数 4 | **true**(x³,y³,z³ 各々も) | **3** | **1(自由作用)** |
| [1152,154163] | 64 | 16 | **2** | 位数 4 | **true**(同) | **3** | **1(自由作用)** |

#### 3.3.3 ★定理 C3-LIFT

> ### 定理 C3-LIFT(両窓 [1152,154161] / [1152,154163])
> **(i)** $P/\Phi(P)\ \cong\ E[2]$ **as $G_\mathbb{Q}$-加群**($E:Y^2=X^3+16$)。
> **(ii)** $\rho_N:G_\mathbb{Q}\to\mathrm{Aut}(G)$($g\mapsto[\bar x\mapsto\bar x^{\chi},\ \bar y\mapsto\bar f_g^{-1}\bar y^{\chi}\bar f_g]$)の像は $\mathrm{Gal}(\mathbb Q(\zeta_3,\sqrt[3]2)/\mathbb Q)\cong S_3$ の上へ落ちる。
> **(iii)** $$\boxed{\ \mathrm{Im}(\mathrm{Ih}_N)\ \cap\ \ker\chi_{\rm vir}\ \supseteq\ C_3\ \ (\text{位数}\ \ge 3),\qquad |\mathrm{Im}(\mathrm{Ih}_N)|\ \ge\ 4\cdot 3=12 .}$$
> (従来の下界は $|(\mathbb Z/12)^\times|=4$。$|\ker\chi_{\rm vir}|=12$、$|GT(N)|=48$。)
> **(iv)** ゆえに **22 候補(= 両窓の $\ker\chi_{\rm vir}$ の非単位元 11×2)のうち少なくとも 4 個(各窓 2 個)は算術的**であり、非算術証人の候補から**脱落**する。

**証明.**
**(i)** 窓は isolated で全 shadow が settled ⟹ $\ker T^{F_2}_{m_g,f_g}=N_{F_2}$。Galois 作用 $\phi_g\in\mathrm{Aut}(\hat F_2)$ は $T^{F_2}=\mathrm{pr}\circ\phi_g$ を満たすから $\phi_g(\hat N_{F_2})=\hat N_{F_2}$ ⟹ $\rho_N$ が well-defined で、$R$ も $G_\mathbb{Q}$-安定。よって $R/\Phi(R)=H_1(X_3;\mathbb F_2)\twoheadrightarrow P/\Phi(P)=R/N_{F_2}\Phi(R)$ は $G_\mathbb{Q}$-同変。GAP 測定より $x^3,y^3,z^3\in\Phi(P)$、すなわち核 $M\supseteq W_{\mathbb F_2}$。$\dim(H_1/W_{\mathbb F_2})=2=\dim(P/\Phi(P))$($d(P)=2$)ゆえ $M=W_{\mathbb F_2}$ で $P/\Phi(P)\cong H_1/W_{\mathbb F_2}\cong E[2]$。∎
**(ii)** (i) より。
**(iii)** $\mathbb Q(\zeta_3,\sqrt[3]2)$ の可換部分体は $\mathbb Q,\mathbb Q(\zeta_3)$ のみ ⟹ 任意の $M$ について $\mathbb Q(\zeta_M)\cap\mathbb Q(\zeta_3,\sqrt[3]2)\subseteq\mathbb Q(\zeta_3)$ ⟹ $\mathrm{Gal}(\mathbb Q(\zeta_{24},\sqrt[3]2)/\mathbb Q(\zeta_{24}))\cong C_3$。$\chi(g)\equiv1\ (\mathrm{mod}\ 24)$ なる $g$ を取ると $m_g\equiv0\ (\mathrm{mod}\ 12=N_{\rm ord})$、$\bar x^{\chi}=\bar x$、$\bar y^{\chi}=\bar y$ ゆえ $\rho_N(g):\bar y\mapsto\bar f_g^{-1}\bar y\bar f_g$。$g$ が $\sqrt[3]2$ を動かせば (i) より $\rho_N(g)$ は $P/\Phi(P)$ 上非自明 ⟹ $\bar f_g\ne1$ ⟹ $\mathrm{Ih}_N(g)=[0,\bar f_g]\ne[0,1]$。この $C_3$ の 3 元は $P/\Phi(P)$ 上で相異なる作用を与えるので、対応する 3 shadow も相異なる。$\mathrm{Ih}_N$ は群準同型(isolated)で $\ker\chi_{\rm vir}$ は部分群だから交わりは部分群、位数 ≥3。$\chi_{vir}$ の像は (P2) より $(\mathbb Z/12)^\times$ 全体(位数 4)。∎
**(iv)** (iii) の 3 元のうち 2 元は非単位。両窓で成立。∎

#### 3.3.4 格・残余ギャップ・確認事項

- **格**: **paper-proof candidate(単系統)**。紙の連鎖は自己完結だが、載荷している機械入力(GAP の $d(P)=2$・$W\subseteq\Phi(P)$・$\mathrm{Ad}(\bar x)$ 自由)は **本メモ 1 系統のみ**。**独立照合器が要る**(著者分離・別実装で $P/\Phi(P)$ と $x^3,y^3,z^3$ の所属を再計算)。
- 【**GAP-C3-1**】 $R$ と $\hat\pi_1(X_{3,\bar{\mathbb Q}})$ の同一視、および「$G_\mathbb{Q}$ の $R^{\rm ab}$ 上の作用 = $X_3$ の étale $H_1$ 上の算術作用」— 標準だが **Sol 監査を請う**(接点/tangential base point の扱い)。
- 【**GAP-C3-2**】(★次の一手) **得られた $C_3$ は 𝒯(fake torus)の像 3 元と一致するか?** 一致するなら **DICHOTOMY-83 が genuine 側で決着**し、**GAP-INN-1 の主張(𝒯 3 元の永久生存)は算術経由で真**となる(T-DEAD と無矛盾 — T-DEAD は「厳密族機構では証明できない」であって「偽」ではない。算術は族機構が原理的に届かない場所を埋める)。一致しないなら **45/42 問題に直接食い込む非内部の算術元**が出る。**どちらでも大きい。**
  - 判別手続き(設計): $\ker\chi_{\rm vir}$ の 12 元それぞれについて $T_{m,f}$ の $P/\Phi(P)$ 上の作用を計算し、非自明作用を与える元を列挙する。それが内部 3 元だけなら (a) 側で確定。
- **陽性対照**: 複素共役 $[11,1]$($\chi_{\rm vir}=-1$)は $\bar f=1$ で $\rho_N$ が $\bar x\mapsto\bar x^{-1},\bar y\mapsto\bar y^{-1}$ ⟹ $E[2]$ 上自明(mod 2 で $-1=1$)。本定理の $C_3$ と独立 ✓(整合)。
- **陰性対照(canary)**: もし $\mathrm{Ad}(\bar x)$ が $P/\Phi(P)$ 上自明だったら (i) の CM 構造と矛盾し全体が崩れる。**測定は「位数 3・固定点なし」= $\mathbb F_4$ 構造で、CM by $\zeta_3$ の予測どおり** ✓。

### 3.4 タスク B の裁定(4 項目)

1. **定義経路と mod p 計算可能性** = §3.1(整理済・(a)(b) は計算可能、可否は Bernoulli 分子/$H^2$ 消滅条件で素数ごとに判定)。
2. **難所の判定** = **不可(83 窓)・不可(972 窓)** — 定理 NILP-VOID。理由は $c\notin N$ ではなく **$F_2/N_{F_2}$ の最大冪零商が可換**であること。**再開条件の再診断が必要**(§3.5)。
3. **具体的計算計画** = Soulé 経路については **83 窓向けには存在しない**。代わりに (α) **新レーン PL-ℓ**(§3.5)と (β) **§3.3 の C3-LIFT がすでに目的(Im ⊋ 円分部分)を達成**。
4. **文献要請** = §5.2。

### 3.5 再開条件の再診断と 2 本のレーン

> **旧**: 「c∉N の対象に適用できる算術機構」。**新(本メモの提案)**: 窓ごとに次の 2 値を先に測れ。
> $$\mathrm{nilvis}(N):=\dim\bigl(\gamma_2(G)/\gamma_3(G)\bigr)\quad(\text{Soulé/grt 系が効く条件} = \mathrm{nilvis}>0),$$
> $$\mathrm{solvis}(N):=\text{「}G\text{ の可解フィルトレーションの各層に対応する被覆の算術」の有無}\quad(\text{83 窓ではこれが }E[2]).$$
> **⚠訂正 C5-g(便 156 §6.3・§8.5)**: $\mathrm{nilvis}(N):=\dim(\gamma_2/\gamma_3)$ は **係数体なしには未定義**。正しくは $$\mathrm{nilvis}_p(N):=\dim_{\mathbb F_p}\bigl((\gamma_2(G)/\gamma_3(G))\otimes\mathbb F_p\bigr)\quad(\text{素数ごとのベクトル})$$ または単に **$\gamma_2(G)/\gamma_3(G)$ の群同型型**を記録する。83 両窓では $\gamma_2=\gamma_3$ ゆえ全 $p$ で $\mathrm{nilvis}_p=0$。また **$\mathrm{solvis}$ は数値不変量ではなく「レーン選択ラベル」**である(格を明記して用いる)。
>
> 83 窓は $\mathrm{nilvis}_p\equiv0$(Soulé 不可)だが $\mathrm{solvis}$ は非空(楕円曲線が出る)。**c∉N は両方に無関係**(NW(7) の $\mathbf N$ は $c\in N$、その ℚ-変種 $\mathbf N_0=\mathcal V(PB_3)$ は $c\notin N$、どちらでも BH-BRIDGE は動く)。

**レーン PL-ℓ(新設提案・Soulé が効く窓)**: $\mathbf N(\ell,k,j)$(定理 D1)。ここでは (a) 明示公式(§3.1)が $f_\sigma$ の metabelian 部分を全重み与え、(b) 各重み $m$ での mod ℓ 全射性が $H^2(\mathbb Z[1/\ell],\mathbb Z_\ell(m))=0$(⟸ Bernoulli 分子条件)で判定でき、(c) 出力は
$$|\mathrm{Im}(\mathrm{Ih}_{\mathbf N})|\ \ge\ \varphi(\ell^{j'})\cdot \ell^{\#\{m\ \text{odd},\ 3\le m\le k-1,\ H^2=0\}}$$
という **重み複数本にわたる初の算術下界**。$k=5,\ell=7$(NW(7) の 1 段深い窓)が最小の新規標的。**BH-BRIDGE は $k=5$ の重み 3 の 1 本だけを使った特殊例**である。

**レーン EC-83(§3.3 の続き)**: (1)【GAP-C3-2】の判別、(2) $E[2]$ より深く — $E[4]$/$T_2E$ と $P$ の深い層の対応(Galois 像 = $\mathbb Q(E[4])$ 等)で下界をさらに上げる、(3) 同じ機構を他の $c\notin N$ 窓へ(判定は $\mathrm{solvis}$)。
**★ここで金庫の elliptic GT intel(Ishii 2312.04196・Enriquez 1003.1012・Lochak–Nakamura–Schneps 2602.12462)が初めて正しい標的を得る**: 83 窓の算術は **CM 楕円曲線 $E$(27a3)から 3 点を抜いた曲線の pro-2 基本群への Galois 作用**であり、これはまさに elliptic associator / elliptic GT の管轄である。降ろし検問の 3 問への回答: ①c∉N 適用可否 = **無関係**(条件は $\mathrm{solvis}$)②下から評価する手続き = **§3.3 の型(被覆の分体を測る)**③B₃-gentle への翻訳 = **$R=\ker(F_2\to C_3)$ 経由で完了済み**。

---

## §4 タスク C — graded 簿記(見取り図・10 行)

1. **問題**: 工房の塔 $K^{(i+1)}=[K^{(i)},K^{(i)}](K^{(i)})^p$(Frattini 塔)は層が爆発する($[N:K_3]=3^{98}$、第 2 段は $3^{98}$ 次元で到達不能)。
2. **処方**: 塔を **Zassenhaus(mod-p 次元部分群)塔** $D_i(N)$ に置換する。層 $\mathcal L_i=D_i/D_{i+1}$ は次数付き制限 Lie 代数を成し、**1 段ごとの線型代数のサイズが多項式**になる。
3. **簿記式(自由部分)**: 階数 $d$ の自由群で $\dim_{\mathbb F_p}\mathcal L_n=\sum_{p^j\mid n} W(n/p^j,d)$、$W(m,d)=\frac1m\sum_{e\mid m}\mu(e)d^{m/e}$(Witt)。$d=2$ で $[2,1,2,3,6,9,18,30,56,\dots]$、$p=7$ なら $[2,1,2,3,6,9,\mathbf{20},30,56]$、$p=3$ なら $[2,1,\mathbf{4},3,6,\mathbf{10},18,30,\mathbf{60}]$(本メモで機械計算)。
4. **窓の大きさの検算**: NW(7) は $|P|=7^{2+1+2+3}=7^8$ ✓(実測 `size_P=5764801` と一致)。
5. **同変版**: 一般の窓では $\mathcal L_n$ は $\mathbb F_p[Q]$-加群なので、簿記は **表現環 $R(Q)$ 上の生成関数**(同変 Witt/necklace 公式)で行う。工房の予想 P-83-5($V\cong\mathbb F_p[Q/H]\oplus\mathbb F_p^2$)はその第 1 層の正規形の推測にあたる。
6. **grt 側の対応表(w≤29 確定・[NW] Cor 7)**: $\dim\mathfrak{grt}_w = [0,0,1,0,1,0,1,1,1,1,2,2,3,3,4,5,7,8,11,13,17,21,28,34,45,56,73,92,120]$(w=1..29、本メモで生成関数から再計算・**L-4c の宿題「$\dim\mathfrak{grt}_{16}$ は 4 か 5 か」= 5 で解決**)。
7. **shadow 数の予言式**(§2.5.3): $\ell$ 群窓 $F_2/\gamma_{k+1}F_2^\ell$ で 1 つの $m$ あたり charming hexagon 数 $=\ell^{\sum_{w=2}^{k}\dim\mathfrak{grt}^{\rm hex}_w}$、PENT 通過数 $=\ell^{\sum_{w=2}^{k}\dim\mathfrak{grt}_w}$。**NW(7) の 294/42 で的中**。
8. **段差の意味**: mod ℓ で $\dim$ が落ちる重み(ℓ=691/w=12 等)がちょうど工房の **SYN-0** の標的。予言式の破れ = 段差の検出器。
9. **972 の B 線(関係加群会計)について**: **この graded 世界の自然な対象である** — Crowell–Fox 完全列 $0\to H_1(K;\mathbb F_3)\to\mathbb F_3[J]^2\to\mathbb F_3[J]\to\mathbb F_3\to0$ は $\mathcal L_1$ の $\mathbb F_p[Q]$-表示そのもの(`t60_relmodule_answer_v1.md`)。ただし **モスボールの理由(CV-9: T56(iv) と別述語)は解消していない** — 復帰させるなら「(iv) の証拠」としてではなく「**$\mathcal L_1$ の同変簿記の計器**」として札を貼り替えること(INC-04 の再演防止)。
10. **注**([Wi2] の型): 大規模厳密計算が中心予想の強形を殺す例は現行(Willwacher 2508.13724 の GC₂ 11-loop)。**工房の予言式 P-GRT-1 も同じ型の反証可能性を持つ** — 外れたら橋 §2.3(iv) が偽と分かる。

---

## §5 未決・要請・同期

### 5.1 本メモが残す GAP
| 札 | 内容 | 重み |
|---|---|---|
| 【GAP-DICT-1】 | 定理 D3(iv)($U_0 = \mathfrak{grt}^{\rm hex}_k\otimes\mathbb F_\ell$)の構成的証明。現状は数値一致(294/42)による candidate | 中 |
| 【GAP-HEX-1】 | $\mathfrak{grt}^{\rm hex}$ が Ihara bracket で閉じるか | 低(次元表に影響なし) |
| 【GAP-HEX-2】 | $\mathrm{gr}(\widehat{GT}_{\rm gen})=\mathfrak{grt}^{\rm hex}$ の等号(⊆ は自明・⊇ が未証明) | 中 |
| 【**GAP-C3-1**】 | §3.3 の幾何的同一視($R\leftrightarrow\hat\pi_1(X_3)$・作用の一致)の Sol 監査 | **高(定理 C3-LIFT の載荷)** |
| 【**GAP-C3-2**】 | 得られた $C_3$ は 𝒯 の像か否か | **高(DICHOTOMY-83 の決着に直結)** |
| 【GAP-C3-3】 | GAP 測定($d(P)=2$・$W\subseteq\Phi(P)$)の独立照合(著者分離) | **高(cross-checked の前件)** |

### 5.2 文献要請(取りに行っていない・名指しのみ)
- 【**文献要請 S-1**】 **Ihara ICM §6.3 の明示公式 [$A_3,C_3$, IKY] の原典**(Anderson;Coleman "Anderson–Ihara theory: Gauss sums and circular units"(= **2405 参考文献 [4]**・在庫外);Ihara–Kaneko–Yukinari)。**欲しい形**: $\psi^{\rm ab}_\sigma$ の公式の正確な言明と正規化(【BR-GAP-1】の解消 = 「$[\kappa^{(p)}_3]$ と Deligne–Soulé $c(1)$ が $\mathbb Z_p^\times$ 倍で一致」の逐語)。**なぜ必要か**: レーン PL-ℓ の重み ≥5 を動かすには公式の全重み版が要る。
- 【**文献要請 S-2**】 **$H^2(\mathbb Z[1/\ell],\mathbb Z_\ell(m))=0$ の判定条件の現行形**(岩澤主予想以後)。**欲しい形**: 「奇数 $m\ge3$ と素数 $\ell$ に対し $H^2=0$ ⟺ $\ell\nmid$(明示された Bernoulli 数/p 進 L 値の分子)」の逐語と、小さい $(\ell,m)$ の表。**なぜ必要か**: レーン PL-ℓ の各重みの発火条件そのもの。
- 【**文献要請 E-1**】(金庫在庫の降ろし検問用) **穴あき CM 楕円曲線の pro-2 基本群への Galois 作用**: (a) $\mathbb Q(E[2^n])$ と $\mathrm{Out}(\pi_1^{(2)}(E\setminus S))$ の像の関係(Nakamura 型)、(b) elliptic Soulé 元(Eisenstein 由来)の非消滅。**対象定理の型**: 「$E$ が CM・$S$ が 3 点のとき、$\mathrm{Im}(G_\mathbb{Q}\to\mathrm{Out}\,\pi_1^{(2)})$ の重み $\le w$ 部分の下界」。**なぜ必要か**: §3.3 のレーン EC-83 を $E[2]$ より深く進めるため。
- 【文献要請 L-4c】= **解決**([NW] Cor 7 により $\dim\mathfrak{grt}_{16}=5$)。台帳から落とせる。

### 5.3 同期の要請(司令塔へ)
1. `docs/notes/c83_closure_index_v1.md` §7 の **再開条件を「c∉N に効く算術機構」から「$\mathrm{nilvis}/\mathrm{solvis}$ による窓判定」へ改訂**(§3.5)。
2. **C-15 (C6)「Im(Ih_N)⊇C₂」を、定理 C3-LIFT の検収後に「⊇ C₂ × C₃(位数 ≥12)」へ更新**(検収前は本メモを candidate として参照)。
3. **22 候補のうち 4 個の脱落**(§3.3.3(iv))を残問 ① の母数に反映(検収後)。
4. `b_type_synthesis_design_v1_addendum_l4b_grt12.md` の **第 2 番地(w=16)の「4 or 5 未決着」を [NW] Cor 7 で確定(=5)**。
5. 予言 **P-GRT-1**(§2.5.3)の事前登録。

---

## §6 機械検算(本メモで走らせたもの・すべて再現手順つき)

| スクリプト | 内容 | 出力 |
|---|---|---|
| `scratchpad/math_c3cover_test_v2.g`(GAP・工房リポジトリ収蔵) | 両 83 窓の $G$・$G^{\rm ab}$・下中心列・$P$・$\Phi(P)$・$d(P)$・$x^3,y^3,z^3\in\Phi(P)$・$\mathrm{Ad}(\bar x)$ の $P/\Phi(P)$ 上の位数と固定空間 | 表 §3.2/§3.3.2。入力は既在 `search/iso_census83_deep15_data.g` のみ(窓の shadow 値には非接触) |
| (session scratchpad) `grthex.py` | $\mathfrak{grt}^{\rm hex}_w$($w\le12$)を Dynkin 冪等元+非可換代入で 2 素数 rank | §2.5.2 の表(2 素数一致) |
| (session scratchpad) `gr_check2.py` | Witt 数・$\dim\mathfrak{grt}_w$($w\le29$、自由性仮定+[NW] Cor 7)・mod-p Zassenhaus 層次元 | §4 の 3/6 行 |

**自己申告**: (a) GAP は本メモ 1 系統(独立照合器なし)。(b) $\mathfrak{grt}^{\rm hex}$ の次元は 2 素数一致だが char-0 の rank と厳密に等しいことは未証明(大素数ゆえ実用上安全・**candidate**)。(c) 配達文献 4 本は **精読していない** — [W] §6.1(定義)・[NW] Abstract/Cor 6,7/式 (3)・[Wi2] Abstract・[Br] タイトルのみ。範囲外の内容は引いていない。

---

# §7 追記(2026-08-22)— 独立照合(cert `koubou83_c3lift_indepcheck_v1_20260822`)を受けた設計者裁定

**状態札**: `§7.2/§7.4 = 定理(自前証明・前件は登録済み二系統事実)/ §7.3 = artifact 裁定(証明済み定理と矛盾するため確定)/ §7.1 = 旧設計の撤回`
入力: `search/certs/koubou83_c3lift_indepcheck_v1_20260822.json`(implementer・著者分離・本メモのスクリプト未開封・3 レコードともバイト同一・elapsed 1024 ms)。

## 7.0 一行

> **§3.3.4 の判別基準(「非自明作用が内部 3 元だけなら確定」)は撤回する — 解像度が足りず、実測はそれを裏づけた。しかし実測の副産物 `m-distribution = {0:6, 6:6}` により、別の(正しい)経路で GAP-C3-2 は決着する**: 位数 6 の群の Sylow 3 部分群は一意ゆえ、**𝒯 の像は必ず Im(Ih_N) に含まれる**(定理 T-ARITH)。

## 7.1 (i) 意図した解像度と、その撤回

**答**: 意図した解像度は確かに $P/\Phi(P)$(層 1)である。**しかし §3.3.4 に書いた判定基準は誤っていた**。あの基準は暗に「shadow ↦ $P/\Phi(P)$ 上の作用」が 𝒯 像を分離するほど細かい、と仮定していた。実測はそうでないことを示した:

$$\Theta:\ \ker\chi_{\rm vir}\ \longrightarrow\ \mathrm{Aut}(P/\Phi(P))\cong GL_2(\mathbb F_2),\qquad |\ker\chi_{\rm vir}|=12,\quad \mathrm{Im}\,\Theta=C_3=\langle \mathrm{Ad}(\bar x)\rangle,\quad \text{各繊維 }4\ \text{元}.$$

⟹ **層 1 では 12 元が 3 つの箱に 4 個ずつ入るだけで、𝒯 像(3 元)を他から切り出せない。したがって「internal 一致で確定」とは書けない。** §3.3.4 の当該判定文は **撤回**(設計者の基準が測定で否定されたのだから、基準を先に撤回する)。

## 7.2 定理 RES-1(解像度定理 — 実測の本当の内容)

> **定理 RES-1.** (a)〔実測・単系統(implementer)〕$\Theta(\ker\chi_{\rm vir})=C_3$、外部作用 0、各繊維 4 元。
> (b)〔定理 C3-LIFT〕$A:=\mathrm{Im}(\mathrm{Ih}_N)\cap\ker\chi_{\rm vir}$ に対し $\Theta(A)=C_3$。
> ⟹ $$\boxed{\ \Theta(A)=\Theta(\ker\chi_{\rm vir})\ :\ \textbf{層 1 の不変量は算術部分によって既に飽和している}.\ }$$
> **系**: 下界 $|A|\ge3$ の改善も、$A$ と $\ker\chi_{\rm vir}$ の区別も、**$\ker\Theta$(位数 4)の上で非自明な不変量**を必要とする。すなわち **$\Phi(P)$ より深い層の算術情報**($\mathbb Q(E[4])$ / $X_3$ の pro-2 $\pi_1$ の $H_1$ より下)なしには一歩も進まない。

**これが実測の正しい読みである** — 「予言の確認」ではなく「**この計器の分解能の上限を測った**」。

## 7.3 (ii) Φ(P) 分のずれ — ゲージか実質か

**三分して答える。**

**(a) 水準 N では「ゲージ」は存在しない(裁定: 元水準の一致検査は正しい)。**
shadow は $(m+N_{\rm ord}\mathbb Z,\ f N_{F_2})$ であり、**$f$ は $G=F_2/N_{F_2}$ の元として完全に確定している**。補正 $w$ の自由度が生じるのは**深い窓 $K$ への持ち上げ**($f_K\in f\cdot N_{F_2}/K_{F_2}$)のときだけで、それは T-DEF の $V=N/K_p$ に住む。**$\Phi(P)$ は $G$ の部分群であって $N/K_p$ ではない — 水準が違う。** ゆえに:
- 「元水準の完全一致」は **過剰に厳しい検査ではなく、唯一正しい検査**である。
- 「ずれを $U_0$ の元として読めるか」= **読めない**(別の群・別の水準)。生存 witness が $f_0\cdot w$ 形だったのは水準 $K$ の話で、ここへ持ち込むと **水準取り違え**になる。
- 一方 $G/\Phi(P)$(位数 $12=3\times4$)は **「$C_3$ 層 ⊕ $E[2]$ 層」に見える最大商**であり、`matched_nu_modphi` の一致はまさに **RES-1 の言い換え**であって shadow の一致ではない。

**(b) ただし当該実測の `matched_nu = None` / `t_pair_valid = False` は artifact である(裁定: 証明済み定理と矛盾するため確定)。**
`t_pair_valid = False` が非単位 11 元すべてに付いている。ところが **補題 U′(証明済み・`c83_inn_lift_lemma_v1.md` §2.2)は「$(0,f_\nu)$ は hexagon (3.3)(3.4) を $B_3$ の恒等式として満たす」を主張する** — したがって任意の $K$、とくに $N$ で GT-pair である。**`t_pair_valid=False` は定理に反する ⟹ 構成側の誤り。** さらに登録済みの独立実測(`inner == {[0,f_ν]}` が **True**・窓 154161・`c83_inn2_innerness_v1.py`)とも矛盾する。
**診断(最有力・一行で検査可能)**: **規約 W-1 違反**。paper 語 $y^\nu x^{-\nu}$ は GAP では `x^-nu * y^nu` である。`y^nu * x^-nu` と書くと差は交換子 $[\bar y^\nu,\bar x^{-\nu}]\in[G,G]=P$ になり、**それが $\Phi(P)$ に落ちれば「mod $\Phi(P)$ は一致・元では不一致」という観測された症状がちょうど出る**(補題 W1 の ι+逆元の二重捻れ)。
⟹ **発注 M0**: `f_nu` 構成を `x^-nu * y^nu` に直して再走し、(i) `t_pair_valid` が 12/12 True になるか (ii) `matched_nu` が $\nu\in\{0,1,2\}$ で当たるか (iii) 誤形との差がちょうど $[\bar y^\nu,\bar x^{-\nu}]$ か、を確認する。**この 3 点が揃うまで「元水準では恒等のみ一致」は報告に書かない**(§7.4 はこの再走に依存しないので走行はブロックしない)。

**(c) 実質の所在**: 本当に実質的なずれがあるとすれば、それは **$P$ の 2 進フィルトレーションの第 2 層**($\Phi(P)$・位数 16)に住む。これは T-DEF の変形ではなく **水準 N の窓自身の深部**であり、次の算術入力($\mathbb Q(E[4])$ 系)がまさに作用する場所である。

## 7.4 ★定理 T-ARITH — GAP-C3-2 の決着(層 1 を使わない経路)

実測が返した **$m$-分布 $\{0:6,\ 6:6\}$**(3 レコード一致)は、登録済み C-15 (C1)(「$\ker\chi_{\rm vir}=12$、**m=6 層 6 元**」・二系統)と一致する。これを使う。

> **補題 M($m$ 層は指数 2 の部分群).** $\mu:\ker\chi_{\rm vir}\to\{0,6\}$、$[m,f]\mapsto m \bmod 12$ は群準同型である。
> **証明.** (3.53) の第 1 成分 $2m_1m_2+m_1+m_2$ に $m_i\in\{0,6\}$ を代入すると $0,\ 6,\ 6,\ 84\equiv0 \pmod{12}$。∎
> ⟹ C-15 (C1) より $\mu$ は全射、よって **$H_0:=\ker\mu=\{[0,f]\in\ker\chi_{\rm vir}\}$ は位数 6 の部分群**。

> ### ★定理 T-ARITH
> 窓 $N\in\{[1152,154161],[1152,154163]\}$ について
> $$\boxed{\ R_N(\mathcal T)\ =\ \{[0,f_0],[0,f_1],[0,f_2]\}\ \subseteq\ \mathrm{Im}(\mathrm{Ih}_N).\ }$$
> すなわち **𝒯(fake torus)の像 3 元は算術的**であり、したがって **genuine**、したがって **2401 Cor 5.4 により ~~全ての $K\in\mathrm{NFI}_{PB_3}(B_3)$~~ → 【訂正 C3(便 156)】全ての細分 $K\le N$ へ survive する**(NFI 内の $N$ と無関係な $K$ を含意しない)。
>
> **証明.** ① $|H_0|=6$(補題 M + C-15 (C1))。② 位数 6 の群の Sylow 3 部分群は一意($n_3\mid 2$ かつ $n_3\equiv1 \bmod 3$ ⟹ $n_3=1$)。③ $R_N(\mathcal T)$ は $H_0$ の位数 3 の部分群である: 補題 U′ より $[0,f_\nu]\in GT(N)$、$m=0$ ゆえ $\chi_{\rm vir}=1$、周期 $e=3$(系 T-EX2・実測)、非自明性は登録済み実測(inner $=3$ 元)。よって ② より $R_N(\mathcal T)$ は $H_0$ の**唯一の**位数 3 部分群。④ $A_0:=\mathrm{Im}(\mathrm{Ih}_N)\cap H_0$ は部分群($\mathrm{Ih}_N$ は isolated 窓で準同型・$H_0$ は部分群)。定理 C3-LIFT の 3 元は $\chi\equiv1\ (\mathrm{mod}\ 24)$ ゆえ $m\equiv0\ (\mathrm{mod}\ 12)$ で $A_0$ に属し、$\Theta$ 像が相異なるので $3\mid|A_0|$。⑤ よって $A_0$ は $H_0$ の位数 3 の部分群を含み、②よりそれは $R_N(\mathcal T)$。∎
>
> **格**: **paper-proof(条件つき)**。前件 = (C1) **【GAP-C3-1】**(§3.3.1 の幾何同一視の Sol 監査)、(C2) 登録済み二系統事実(|GT(N)|=48・$\ker\chi_{\rm vir}$=12・m=6 層 6 元・inner=3(m=0 層))、(C3) 補題 U′・系 T-EX2(証明済み)。
> **★重要**: 本証明は **どの元が 𝒯 像かを知る必要がない** ⟹ §7.3(b) の係争(`matched_nu`)に **依存しない**。

**帰結(すべて上記条件つき・格上げ禁止)**
1. **DICHOTOMY-83 は genuine 側**(事前登録済みの「genuine + 新現象(fake torus 像と ĜT_gen 像の合致)」分岐に着地)。$\mathcal T\cap\widehat{GT}_{\rm gen}=\{1\}$ と矛盾しない — profinite で交わらなくても**像**は一致しうる、というのがまさにこの分岐の内容。
2. **【GAP-INN-1】の主張は真**(𝒯 3 元は全 $K$ で生存)。ただし **T-DEAD とも矛盾しない**: T-DEAD は「厳密族機構では証明できない」であり、実際 **証明を与えたのは算術**である(族機構が原理的に届かない場所を算術が埋めた)。**C-83-INN は「主張は復帰・旧 4 行証明は依然 NOGO-1 で無効」**という形になる。
3. **22 候補のうち 4 個(各窓 2 個 = order-3 候補)が算術的として脱落**。残る主戦場は $\ker\Theta$ 側と $m=6$ 層。
4. **K₃ witness の構造との整合**: 算術代表 $f_g$ は厳密に $[\hat F_2,\hat F_2]$ に入るので全水準で charming、一方 $f_1=yx^{-1}$ は入らない。登録済み実測 **abg(f″)=(0,0,0) が 24/24 厳密**は「算術代表が持つべき形」であり **後づけで整合する**(根拠には数えない・整合の記録)。

## 7.5 (iii) 作用パターンの読み

**答: C3-LIFT の予言の「確認」ではない。ただし無情報でもない — 反証機会が実在して通過した。**
- $\Theta$ のパターン(4+4+4・external 0)は $GT(N)$ の**純群論的**事実で、算術を一切使わずに出る。算術的かどうかは GAP では原理的に見えない ⟹ **予言の確認とは呼べない**(格上げ禁止)。
- しかし **反証機会は実在した**: もし 12 元すべてが $P/\Phi(P)$ 上自明に作用していたら、C3-LIFT(算術元が非自明作用を持つ)は **即座に反証**された。通過したので **consistency check PASS**。
- **external 0** は $\Theta(\ker\chi_{\rm vir})=C_3$ を与え、C3-LIFT と合わさって「層 1 は算術で飽和」= RES-1 を出す。これが実測の主産物。
- **傾いたか**: 層 1 の作用実測**によっては傾かない**。着地させたのは **$m$ 分布 $\{0:6,6:6\}$ という副産物**であり、経路は §7.4 の Sylow 論法である。**作用の一致と元の一致は最後まで峻別した**(§7.4 は元の一致を一切使わない)。

## 7.6 (iv) §3.3.4 改訂版 — 判別の正しい粒度と発注

**粒度の再定義(層の梯子)**

| 層 | 対象 | 見える算術 | 分解能 |
|---|---|---|---|
| $L_0$ | $G/P=C_3$ | 円分($\chi$)のみ | charming で 0 — 情報なし |
| $L_1$ | $P/\Phi(P)\cong E[2]$ | $\mathbb Q(\zeta_3,\sqrt[3]2)$ | **C3-LIFT が住む層。繊維 4($m=0$ に限れば 2)— 元の分離は不可能(RES-1)** |
| $L_2$ | $\Phi(P)$(位数 16) | $\mathbb Q(E[4])$ / pro-2 $\pi_1$ の $H_1$ 以下 | **未着手 — $|A|>3$ と $m=6$ 層の判定はここでしか出ない** |

**発注(優先順)**
- **M0(即・数分)**: §7.3(b) の規約再走(`x^-nu * y^nu`)。合格条件 = `t_pair_valid` 12/12 True ∧ `matched_nu ∈ {0,1,2}` ∧ 誤形との差 $=[\bar y^\nu,\bar x^{-\nu}]$。**不合格なら補題 U′ か census のどちらかが壊れている = 全面点検**(強力な健全性検査)。
- **M1(即)**: $H_0$($m=0$ 層・位数 6)の同型型($C_6$ か $S_3$ か)と $\ker\Theta\cap H_0$(位数 2)の生成元。§7.4 の ①② を独立に再確認する。
- **M2(小)**: 12 元それぞれの **$G$ 全体(位数 192)上の**誘導自己同型を計算し、$\mathrm{Ad}(\bar x^\nu)$ と一致するものを列挙(full-$G$ 分解能)。𝒯 像がちょうど 3 元なら §7.4 ③ の独立確認になる。
- **M3(本命・レーン EC-83)**: $L_2$ の算術。$\mathbb Q(E[4])$($E$ = 27a3・CM)と $\Phi(P)$ の Galois 加群構造の対応。**【文献要請 E-1】がここに効く。**

**★falsifier canary(新設・強力)**: 定理 T-ARITH は「$[0,f_1]$ は全 $K$ で survive する」を**予言する**。したがって **survival lane(park 中)で $[0,f_\nu]$($\nu\not\equiv0$)の死亡証明書が 1 枚でも出れば、T-ARITH は反証され、ひいては C3-LIFT か【GAP-C3-1】が偽**と分かる。⟹ **park 中の lane が C3-LIFT の反証器に転用できる**(片側判定・登録推奨)。逆に死が出ないことは(有限深度ゆえ)何も証明しない — 非対称は従来どおり。

## 7.7 便 156 に載せる言明(逐語・Sol 監査用)

> **(S1)** 定理 **C3-LIFT**(§3.3.3): 83 両窓で $P/\Phi(P)\cong E[2]$($E:Y^2=X^3+16\cong$ 27a3、$\mathbb Q(E[2])=\mathbb Q(\zeta_3,\sqrt[3]2)$)、ゆえに $\mathrm{Im}(\mathrm{Ih}_N)\cap\ker\chi_{\rm vir}\supseteq C_3$、$|\mathrm{Im}(\mathrm{Ih}_N)|\ge12$(従来 4)。**格 = paper-proof candidate。監査点 =【GAP-C3-1】**($R$ と $\hat\pi_1(X_3)$ の同一視・接ベクトル基点・$G_\mathbb{Q}$ 作用の一致)。機械入力は **二系統**(数学者 × implementer・著者分離・9/9 一致)。
> **(S2)** 定理 **RES-1**(§7.2): 層 1 は算術部分で飽和 ⟹ さらなる下界改善は $L_2$ を要する。
> **(S3)** 定理 **T-ARITH**(§7.4): $R_N(\mathcal T)\subseteq\mathrm{Im}(\mathrm{Ih}_N)$ ⟹ 𝒯 3 元は genuine で全 $K$ 生存。**(S1) 相対**。⟹ DICHOTOMY-83 は genuine 側・**GAP-INN-1 の主張は真(証明機構は算術・T-DEAD と両立)**・22 候補から 4 個脱落。
> **(S4)** 定理 **NILP-VOID**(§3.2): Soulé/grt 系は 83・972 窓で情報量ちょうど 0(前件 $\gamma_2=\gamma_3$ は二系統実測)。**再開条件は「c∉N」から「$\mathrm{nilvis}/\mathrm{solvis}$」へ改訂を要する。**
> **(S5)** 係争 1 件: cert の `matched_nu=None` / `t_pair_valid=False` は **補題 U′ と矛盾するため artifact と裁定**(規約 W-1 疑い・発注 M0)。**(S3) はこの係争に依存しない。**

## 7.8 追記(同日)— 発注 M0 の実測結果と (S1)–(S5) の改訂

**cert**: `search/certs/koubou83_c3lift_indepcheck_v1_1_20260822.json`(v1 残置)。**診断は的中**(v1 :210 が paper 順 `y^nu*x^-nu` を GAP へ直書き = 規約 W-1 違反)。

1. **`t_pair_valid = 3/12`・一致 3 元 = {ν=0(恒等), ν=2, ν=1} で $\Theta$ 像がちょうど $C_3$・3 レコード同一。** ⟹ **補題 U′ との矛盾は解消**(非単位元も元水準で完全一致)。**§7.4 の前件 ③(「$R_N(\mathcal T)$ は $H_0$ の位数 3 の部分群」)は、登録済み実測に加えて本 cert で直接測定された(二系統)。**
2. **ν とクラスの反転(ν=2↔Ad(x̄)、ν=1↔Ad(x̄)²)は誤りではなく予期される符号**である。補題 U′ は $T_{0,f_\nu}$ が $\bar y\mapsto\bar x^{\nu}\bar y\bar x^{-\nu}$ を与えるが、GAP の共役規約は `u^x` $=\bar x^{-1}u\bar x$ ゆえ cert の "Ad(x̄)" は本メモの $\mathrm{Ad}(\bar x^{-1})$ にあたる。⟹ **反転はむしろ整合の証拠**(規約 pin: 以後 cert に `ad_convention = GAP(u^x = x^-1 u x)` を明記)。
3. **内訳 3+3 は補題 M の絵と完全に整合**: $H_0$(位数 6)$=R_N(\mathcal T)$(唯一の Sylow 3・3 元)$\sqcup$ 非自明剰余類(3 元)。v1 の $m=0$ 層の作用分布 $\{1:2,\ 3:4\}$ とも整合($\mathcal T$ 像が 1+1+1 を供給し、残り 3 元が 1+1+1)。⟹ **implementer の解釈(「$\ker\chi_{\rm vir}\supsetneq\mathcal T$ 像・C3-LIFT は ⊇ しか主張しない・想定内」)は正しい。**
4. ★**残問の縮約(新)**: $A:=\mathrm{Im}(\mathrm{Ih}_N)\cap\ker\chi_{\rm vir}$ は $R_N(\mathcal T)$ を含む部分群ゆえ $|A|\in\{3,6,12\}$。とくに **$m=0$ 部分は厳密に 1 ビット**: $A_0\in\{R_N(\mathcal T),\ H_0\}$ で、判定は **$\ker(\Theta|_{H_0})$(位数 2)の生成元 1 個の算術性**に帰着する。⟹ **11 元(窓あたり)の問題が「1 元の算術性 + $m=6$ 層の有無」に縮約された。** この 1 元こそ $L_2$($\Phi(P)$・$\mathbb Q(E[4])$)で測るべき標的である(発注 M3 の照準)。
5. **格の更新**: (S3) T-ARITH の前件 ③ は **cross-checked**(登録 `inn2.py` × 本 cert・著者分離)。**(S1) C3-LIFT の格・条件は不変**(【GAP-C3-1】相対)。**(S5) は「係争」から「解決・診断的中」へ改訂** — 実測は (S5) を支持した。

> **(S5′)〔改訂〕** v1 の `matched_nu=None` / `t_pair_valid=False` は **規約 W-1 違反による artifact と確定**(数学者診断 → M0 再走で解消)。W-1 準拠の v1_1 では **𝒯 像 3 元が元水準で完全一致・$t\_pair\_valid$ 3/12**。**新規約 pin: cert に `ad_convention` を明記**。INC 追記候補(内部捕獲・定理との矛盾で検出した型)。
> **(S6)〔新〕** **残問は 1 ビット + $m$=6 層**: $|A|\in\{3,6,12\}$、$m=0$ 部は $\ker(\Theta|_{H_0})$ 生成元 1 個の算術性で決まる。
> **(S7)〔新〕** **falsifier canary**(§7.6): $[0,f_\nu]$($\nu\not\equiv0$)の死亡証明書 1 枚で T-ARITH は反証 ⟹ park 中の survival lane が C3-LIFT の片側反証器になる。**この canary の妥当性の可否を Sol に問う。**

---

# §8 Sol 便 156(AUDIT_156_VERDICT = 条件付き)5 条件の執行 — versioned 訂正の正本

出典: `sol/sol_reply_156_c3lift.md`(監査固定点 `9f6ad83f18fe4d5f1352fea411e3b5bb720ff13a`・全文読了)。
**規律**: 本文 §2〜§7 は 1 バイトも削除せず、訂正マーカー(⚠訂正 C1〜C5-g)と取り消し線のみを挿入した。**逐語の正本は本 §8。**
**Sol の総合判定**: 「C3-LIFT の幾何鎖は、2 つの修正を入れれば通る。この修正形では【GAP-C3-1】(a)〜(c) に未解決の数学的欠落は残らない。従って C3-LIFT を前件とする T-ARITH と残問縮約の論理も通る。」 ⟹ **【GAP-C3-1】は解消**(格は candidate のまま・verified ではない)。

## 8.1 条件 1 — $X_3$ の開/コンパクト分離(執行済・マーカー C1)

> **正本**: $U:=\mathbb P^1_\mathbb{Q}\setminus\{0,1,\infty\}$、$q:\hat\pi_1(U_{\bar{\mathbb Q}})\cong\hat F_2\to\mathbb Z/3$、$q(x)=q(y)=q(z)=1$。被覆 $w^3=t(1-t)$ は $U$ 上有限 étale 3 次。$\ker q=\widehat R$($R=\ker(F_2\to C_3)$ の閉包・有限指数ゆえ閉包との齟齬なし)。
> 座標変換 $u=2t-1,\ X=-4w,\ Y=4u$ により滑らかな完備化は $E:Y^2=X^3+16$、除いた 3 点は $S=\{O,\ T,\ -T\}$、$T=(0,4)$。よって
> $$\boxed{\ \widehat R\ \cong\ \hat\pi_1(U_3,\bar{\mathbb Q}),\qquad U_3:=E\setminus S\ }$$
> であり、**$\hat\pi_1(E)$ と書くのは誤り**($R$ の階数が 4 であることがその証左)。本メモの $X_3$ は以後すべて $U_3$ を指す。
> **接ベクトル基点**: 基底側の標準 tangential base point と、その上の幾何的 lift/path を **一つ選んで得られる同型**として述べる。lift の変更は deck 変換による同型を変えるだけで、**$G_\mathbb{Q}$-加群の同型型は不変**。「基点を無視した文字どおりの等号」とは書かない。
> **deck 群**: ℚ 上の deck 群は定数群 $C_3$ ではなく **$\mu_3$**($\bar{\mathbb Q}$ 上で $C_3$)。Galois は deck 生成元を $\chi\bmod3$ で捻る。⟹ **「ℚ 上の $C_3$-Galois cover」という語は使わない。**
> **$\widehat R$ の安定性(Sol §2.2 の形)**: Ihara 作用 $\varphi_g$ に対し $q\circ\varphi_g=(\chi(g)\bmod3)\,q$($f_g\in\hat F_2'$ ゆえ共役項が消える)。$\chi(g)\bmod3$ は単元ゆえ $\ker q=\widehat R$ は安定。これが descent datum を与え、式 $w^3=t(1-t)$ 自体が ℚ 上にあるので **ℚ-構造は循環論法なしに明示されている**。

## 8.2 条件 2 — 重み完全列と分裂主張の削除(執行済・マーカー C2)

> **正本**: $O,T,-T$ はすべて ℚ-rational で、接線公式から $2T=-T$、ゆえに $3T=O$。開曲線の étale homology には $G_\mathbb{Q}$-同変な **localization sequence**
> $$0\ \to\ W\ \to\ H_1(U_3;\mathbb F_2)\ \to\ H_1(E;\mathbb F_2)\ \to\ 0$$
> があり、$W\cong\widetilde H_0(S;\mathbb F_2)(1)$ は **2 次元**($x^3,y^3,z^3$ の cusp inertia class が張り関係は 1 本)、3 尖点が点ごとに ℚ-rational かつ $\mathbb F_2(1)$ が自明ゆえ **$W$ は自明 $G_\mathbb{Q}$-加群**、$H_1(E;\mathbb F_2)\cong E[2]$ は同変。
> **分裂は主張しない(削除)。** 旧稿の「コンパクト部分が自由だから飽和・分裂」は**ベクトル空間としての分裂しか与えず、$G_\mathbb{Q}$-同変分裂の理由にならない**。**C3-LIFT に必要なのは同変完全列と商 $H_1(U_3)/W\cong E[2]$ だけ**である。
> (残す場合の代替理由のみ記録: generalized Jacobian / 1-motive の拡大類は尖点差 $T,-T$ の mod-2 Kummer 類であり、$T=2(-T),\ -T=2T$ と 2 が有理 $C_3$ 上可逆ゆえ両類が消える。以下では使わない。)
> **$P/\Phi(P)\cong E[2]$ の導出(Sol §2.3 の形)**: isolated/settled 性から $N_{F_2}$ は Ihara 作用で安定し、自然な全射 $H_1(U_3;\mathbb F_2)=R/\Phi(R)\twoheadrightarrow P/\Phi(P)$ は $G_\mathbb{Q}$-同変。独立測定は $d(P)=2$ と $x^3,y^3,z^3\in\Phi(P)$ を返すので **核は 2 次元の $W$ を含み、両辺の次元から核はちょうど $W$**。ゆえに $P/\Phi(P)\cong H_1(U_3;\mathbb F_2)/W\cong E[2]$ が $G_\mathbb{Q}$-加群として従う。∎

## 8.3 条件 3 — T-ARITH の射程(執行済・マーカー C3)

> **正本**: 「$R_N(\mathcal T)\subseteq\mathrm{Im}(\mathrm{Ih}_N)$ ⟹ 3 元は arithmetical ⟹ genuine ⟹ **全ての細分 $K\le N$ へ survive する**」。
> **禁句**: 「全ての $K\in\mathrm{NFI}_{PB_3}(B_3)$」— $N$ と比較不能な $K$ を含意してしまう。

## 8.4 条件 4 — (S7) 片側反証器の強化(執行済・§8.7 に逐語)

Sol §4 の 5 点を必須要件として組み込む(逐語は §8.7 の (S7′))。あわせて **A4 の規約 2 件を次版 checker/cert への発注として登録**:
- **発注 A4-1(W-1 fail-closed assert・必須ゲート)**: paper-aware product helper を通し、$\nu=1$ の補題 U′ $f_1^{-1}\sigma_2f_1=x\sigma_2x^{-1}$($f_1=yx^{-1}$、GAP では `x^-1*y`)を **$B_3$ または規約感度をもつ固定非可換 fixture 上で assert**。同 fixture で旧誤形 `y*x^-1` が不一致になる **陰性 canary** も必須。**可換商・単生成元・空語のみの fixture は W-1 に盲ゆえ不可。**
- **発注 A4-2(`ad_convention` pin)**: cert に `paper_ad_x(u)=x*u*x^-1` / `gap_power_convention: u^x = x^-1*u*x` / 実装がどちらを `Ad(x)` とラベルしているか / ν と action class の対応表と非中心 fixture 上の assert 結果 / `word_convention_id`・`action_convention_id`・checker source SHA を **機械生成**で入れる。⟹ v1_1 の `ν=2↔matches_adx`, `ν=1↔matches_adx2` が **バグでなく raw GAP conjugation label と paper $\mathrm{Ad}$ の符号差**だと cert 単体で判読できる。
- **発注 A4-3(stale comment 訂正)**: `koubou83_c3lift_check_v1_1.g` の :193–195「ker χ は m=0 のみ」・:233「m=0 so u=1」は、直後の正しい実装 `m∈{0,6}` と矛盾する stale comment。**v1_1 は上書きせず次版で訂正**。

## 8.5 条件 5 — A5 の格境界同期(執行済・マーカー C5-a〜C5-g)

| 札 | 旧 | **新(正本)** |
|---|---|---|
| **C5-a** | 定理 D3 (iv)(「$U_0=\mathfrak{grt}^{\rm hex}_k\otimes\mathbb F_\ell$」)を定理の一部として提示 | **定理 D3 から分離。(i)(ii)(iii) のみ定理、(iv) は【GAP-DICT-1】candidate**(根拠は数値一致のみ) |
| **C5-b** | 「同値になるのは拡大が分裂($e=0$)する場合に限る」 | **削除(過大)**。$e=0$ は**この一つの障害を消すだけ**で全情報の同値を与えない |
| **C5-c** | $\mathfrak{grt}^{\rm hex}$ を「Lie 代数」と呼ぶ | **「斉次 hexagon 解空間 $\mathcal H_w$」に改称**(Ihara bracket 閉性 =【GAP-HEX-1】未証明。次元計算に閉性は不要) |
| **C5-d** | 次元表(w≤12)の格が曖昧 | **candidate**。2 大素数一致は **有理 rank の下界**にとどまる(mod-p rank ≤ 有理 rank)。厳密化には fraction-free 有理消去・非零 minor と kernel basis の両証明・または SNF 証明書 |
| **C5-e** | 294/42 一致を「独立裏取り/橋の実証」 | **retrospective numerical agreement**。「独立再現」「BIT-252 を証明」とは書かない。最大文 =「既知の GAP 値と独立な graded 会計との一致」 |
| **C5-f** | 972 へ NILP-VOID を一行拡張 | **保留**。$G^{\rm ab}$ が小さい 2 群というだけでは最大 2-商が可換とは限らない。**別 pin($\gamma_2=\gamma_3$ or 最大冪零商の直接計算)まで 83 両窓のみ主張** |
| **C5-g** | $\mathrm{nilvis}(N)=\dim(\gamma_2/\gamma_3)$ | **$\mathrm{nilvis}_p(N):=\dim_{\mathbb F_p}((\gamma_2/\gamma_3)\otimes\mathbb F_p)$ のベクトル、または $\gamma_2/\gamma_3$ の群同型型**。$\mathrm{solvis}$ は数値不変量でなく **レーン選択ラベル**(格を明記) |

**P-GRT-1 の凍結宇宙(条件 5 の一部・執行)**: 事前登録は採用。ただし **最初の凍結宇宙は ℓ=7・重み ≤5・一窓に限定**する。digest 化する対象 = window presentation・$\mathcal X$・charming/PENT の述語版・row universe・**char-0 / mod-7 rank canary**。**全素数への無条件適用はしない**(本メモ自身が重み 2・標数 3 の段差を指摘している)。**一般版は mod-ℓ rank を入力とする次版に分ける。** 外れた場合の分岐は既登録どおり(mod-ℓ 段差 / 有限窓 bridge・非線形 lifting の破れ)で、**結果を見て予言本文を上書きしない**。

**[NW] 引用範囲の確認**: 「weight ≤29 で Conj. 2 の 4 Lie 代数が一致」に限定した読みで整合。その引用を前件に自由 Lie 生成関数から $\dim\mathfrak{grt}_{16}=5$ を得るのも整合。**ただし論文全体の独立精読ではない**(§6 の自己申告どおり)。

## 8.6 便 156 の付随事項(記録)

- **park の限定解除(Sol §7)**: 再開してよいのは **EC-83 の $E[4]$ / punctured CM elliptic pro-2 レーン**と **(S7) の完全 fibre falsifier** のみ。**解除しないもの** = 18 候補の全算術性・$\mathrm{Im}(\mathrm{Ih}_N)=GT(N)$・83 線全体の genuine/fake 判定・深度線完結。
- **C-15/地図へ反映する最大文(Sol §7 逐語)**: 「A1 の修正文に相対して C3-LIFT/T-ARITH の paper chain が Sol 監査を通過。三 torus image は算術的という candidate 結論を持ち、全体は UNKNOWN。verified ではない。」
- **digest 不一致 1 件(Sol §8)**: 現作業木 `docs/状態.md` は便記載の prefix と不一致(C3 検証ブロックの**途中挿入**による)。固定 commit の blob は正しく数学入力は復元可能。**次 freeze で append-only か full digest 更新のどちらかに統一すること**(司令塔案件)。
- **監査範囲外(Sol §9)**: M1/M2/M3 未発注・P-GRT-1 は登録のみ・C-15/地図反映は条件執行後・972 A 型 v3 は対象外・Lean 未着手。

## 8.7 ★改訂逐語 — (S1)(S3)(S7)(便 156 後の正本)

> ### (S1′) 定理 C3-LIFT【改訂】
> 窓 $N\in\{[1152,154161],[1152,154163]\}$。$U:=\mathbb P^1_\mathbb{Q}\setminus\{0,1,\infty\}$、$q:\hat F_2\to\mathbb Z/3$($x,y,z\mapsto1$)、$\widehat R:=\ker q$。被覆 $w^3=t(1-t)$ の滑らかな完備化は $E:Y^2=X^3+16$($\cong$ 27a3・$j=0$・CM by $\mathbb Z[\zeta_3]$)、除去点は $S=\{O,T,-T\}$、$T=(0,4)$、$U_3:=E\setminus S$。標準 tangential base point とその lift を一つ選ぶと $\widehat R\cong\hat\pi_1(U_3,\bar{\mathbb Q})$(**lift の選択変更に対し同型**)。ℚ 上の deck 群は $\mu_3$。$q\circ\varphi_g=(\chi(g)\bmod3)q$ より $\widehat R$ は $G_\mathbb{Q}$-安定で、$w^3=t(1-t)$ が ℚ 上にあるので ℚ-構造は明示的。
> $G_\mathbb{Q}$-同変 localization sequence $0\to W\to H_1(U_3;\mathbb F_2)\to H_1(E;\mathbb F_2)\to0$($W\cong\widetilde H_0(S;\mathbb F_2)(1)$・2 次元・3 尖点 ℚ-rational かつ $\mathbb F_2(1)$ 自明ゆえ **自明加群**;**分裂は主張しない**)。settled/isolated から $N_{F_2}$ は安定で全射 $H_1(U_3;\mathbb F_2)\twoheadrightarrow P/\Phi(P)$ は同変。二系統測定 $d(P)=2$・$x^3,y^3,z^3\in\Phi(P)$ より核は $W$ を含み、次元勘定で核 $=W$。ゆえに
> $$\boxed{\ P/\Phi(P)\ \cong\ E[2]\quad(G_\mathbb{Q}\text{-加群として}),\qquad \mathbb Q(E[2])=\mathbb Q(\zeta_3,\sqrt[3]2),\ \mathrm{Gal}\cong S_3.\ }$$
> 最大可換部分体が $\mathbb Q(\zeta_3)$ ゆえ $\mathbb Q(E[2])\cap\mathbb Q(\zeta_{24})=\mathbb Q(\zeta_3)$、$G_{\mathbb Q(\zeta_{24})}$ の $E[2]$ 像に $C_3$ が残る。この部分では $\chi\equiv1\ (24)$ ゆえ $m\equiv0\ (12)$。よって
> $$\boxed{\ \mathrm{Im}(\mathrm{Ih}_N)\cap\ker\chi_{\rm vir}\supseteq C_3,\qquad |\mathrm{Im}(\mathrm{Ih}_N)|\ \ge\ 12\ \ (\text{従来 }4).\ }$$
> **格 = paper-proof candidate**(verified でない・cross-checked とも書かない)。**【GAP-C3-1】は便 156 §2 で解消**(「この修正形では (a)〜(c) に未解決の数学的欠落は残らない」)。機械入力は **二系統**(数学者 × implementer・著者分離・9/9 一致)。各窓で非単位 2 元・計 4 元が候補除外集合から落ちる会計も Sol が確認済。

> ### (S3′) 定理 T-ARITH【改訂】
> 補題 M(($3.53$) の第一成分 $2m_1m_2+m_1+m_2$ で $\{0,6\}$ が $C_2$ をなす ⟹ $\mu:\ker\chi_{\rm vir}\to C_2$ は準同型)と、**凍結有限前件**である登録済み C-15 (C1)(|H|=12・m=6 層 6 元・二系統測定;C3-LIFT/T-ARITH の結論を使わないので**循環しない**)から $|H_0|=6$。位数 6 の群の Sylow 3 部分群は一意。補題 U′・周期 $e=3$・非自明性測定から $R_N(\mathcal T)$ は $H_0$ の位数 3 の部分群、ゆえに**唯一の Sylow 3**。C3-LIFT の算術 3 元は $m=0$ ゆえ $A_0:=\mathrm{Im}(\mathrm{Ih}_N)\cap H_0$ に属し $E[2]$ 上相異なるので $3\mid|A_0|$。よって
> $$\boxed{\ R_N(\mathcal T)\subseteq\mathrm{Im}(\mathrm{Ih}_N)\ }$$
> arithmetical ⟹ genuine ⟹ **全ての細分 $K\le N$ へ survive**(「全 NFI の無関係な $K$」ではない)。**この Sylow 論法はどの shadow がどの $\nu$ かを使わないので v1 の W-1 artifact に依存しない。**
> **格 = candidate**。相対する前件 = (S1′) の修正文・C-15 (C1) の凍結有限前件・isolated 性。
> **帰結**: DICHOTOMY-83 は genuine 側の分岐に着地(𝒯∩ĜT_gen={1} と矛盾しない)/【GAP-INN-1】の主張は真だが**証明機構は算術**で T-DEAD と両立(T-DEAD は「厳密族機構では証明できない」)/ 22 候補から 4 元脱落。

> ### (S7′) 片側反証器【改訂・強化 5 点】
> $[0,f_\nu]$($\nu\not\equiv0$)の**真正な死亡証明書**が 1 枚出れば T-ARITH は反証される。ただし次を**すべて**満たすもののみ死亡証明書と認める。
> 1. 対象を $K\le N$ と reduction map $R_{K,N}$ で pin し、死亡対象が同じ $[0,f_\nu]\in GT(N)$ であることを **canonical key** で確認する。
> 2. 「strict representative $f_\nu$ が $K$ で charming でない」「T-EX の厳密族 witness が失敗」は**死亡証明書ではない**(**T-DEAD がまさにその失敗を予言している**)。**$R_{K,N}^{-1}([0,f_\nu])$ の全 fibre に lift がないこと**を証明しなければならない。
> 3. 有界探索の不発・solver UNKNOWN・未尽の coset は反証に使わない。**CLAIM-COVER-1 の exact multiset coverage・legal/charming/direct gate・破壊対照・陽性対照**を要求する。
> 4. 真の死亡証明書が出た場合、論理的には C3-LIFT/A1 だけでなく **C-15 (C1)・$R_N(\mathcal T)$ の同定・reduction 実装を含む前件の連言のどれか**を反証する。**原因を C3-LIFT に一意帰属させない。**
> 5. **有限深度で死亡が出ないことは支持証拠へ格上げしない。**
> この形なら、park 中の既存計器を正側定理の高感度 falsifier に転用する設計として有効(Sol §4 = 登録可)。
