# 追補 E-A(**裁定 394 採択札 A** = FAKE-KILL$^{B_4}$ の一頁再演)

**位置づけ**: `docs/notes/ihnec_v1.md` への**追補 E の第 2 部**(erratum 方式)。**v1 本文・追補 A/B/C/D は 1 バイトも改変していない** — 置換関係は §E-A.6 / §E-A.8.1 に明記する。
**起草**: 数学者(Opus 5)/ 2026-08-01。**委嘱** = 発案係第 18 便・裁定 394 採択札 A(**IHNEC-GAP-3 への回答**)。**Sol 未監査。**
**正典**: arXiv **2008.00066** "What are GT-shadows?"(54 頁 v2)。覚書 = `docs/scout/覚書_upb4_2008_v1.md`(配達 2026-08-01)。
**記号規約(覚書 §一工夫の混同防止に従う)**: 本追補の B₄ 側の対象にはすべて **上付き $^{B_4}$** を付し、主線 $B_3$-gentle の $K^{(n)}$ 族と**物理的に分離**する。**2405 Remark 1.2 の「同名別物」宣言を全編で遵守。**
**封印遵守**: $K^{(5)}$ 非接触($B_4$ 側には $K^{(n)}$ 族が存在しないので接触の機会自体が無い)。

---

## E-A.0 先に一枚 — **何が出たか(結論を先に)**

発案係の札 A は「$B_4$ 塔の極限は最初から $\widehat{GT}$(2008 Thm 3.8)ゆえ **U-10 が前件から消える**」という着想であった。検査の結果:

| 検査項目 | 結果 |
|---|---|
| **Thm 3.8 の $\widehat{GT}$ は pentagon つきの Drinfeld $\widehat{GT}$ か** | ★ **YES で確定**(3 系統の根拠・§E-A.2.1)⟹ **U-10 は前件から消える。札 A の着想は正しい** |
| **前件表に U-10 は現れるか** | ★ **現れない**(§E-A.4.2 の除外欄)。**ただし代わりに (TRUNC$^{B_4}$) が暗黙の前件として現れる**(§E-A.2.2)— 交換は「未解決予想 ⟶ 記述の穴」であって**等価ではない(真の前進)** |
| **(COR54)$^{B_4}$ の所在** | ★ **条文あり = 2008 Corollary 3.13 (p.38)**。**ただし証明本文が無い**(「Prop 3.3 と Thm 3.8 の直接の帰結」の一言のみ)⟹ **§E-A.5 で自前補完(補題 SURV$^{B_4}$)** |
| ★★ **FAKE-KILL$^{B_4}$ の新規性** | **新結果ではない。正典が既に述べている** — 2008 **Remark B.3 + 脚注 15**(p.52)が逐語で同じ含意を書いている(§E-A.4.3)。⟹ **本追補の寄与は定理ではなく前件表と $B_3$ 版との差分管理** |
| **発案係の懸念 A-1(groupoid 型ずれ)** | **実在する**が、**集合水準の FAKE-KILL$^{B_4}$ には無害**。群・極限を使う補題 SURV$^{B_4}$ 側では isolated 制限で処理(橋補題 BRIDGE$^{B_4}$・§E-A.3) |
| **発案係の懸念 A-2(算術側装置の $B_3$ 取り残し)** | ★ **実在し、かつ本追補で解消できない**。$B_4$ 側に算術のフックは 1 本だけある(Remark 2.17 の cyclotomic character)が、**窓の族も明示式も無い** ⟹ 【IHNEC-GAP-6】(§E-A.7) |
| ★ **副産物(B₃ 側への配当)** | **2008 が $B_4$ 側で明記していた観察を $B_3$ 側へ移すと、ihnec の (INT) 依存が外れる**(§E-A.6)。⟹ **ML-ODD の格が「補題 INT に相対的」から解放される** |

> ★ **本追補の核心を一行で**: 札 A の着想「U-10 が消える」は**正しい**。しかし **FAKE-KILL$^{B_4}$ 自体は正典の脚注に既にある**ので、これは**決着でも新定理でもなく、前件の付け替え(bookkeeping)**である。**そして付け替えた先には工房の装置が一つも無い**(§E-A.7)。**最大の実収穫は、$B_4$ 論文を読んだことで $B_3$ 側の依存が 1 本外れたこと**(§E-A.6)である。

---

## E-A.1 記法($^{B_4}$ 物理分離)

| 記号 | 意味 | 2008 での出所 |
|---|---|---|
| $\mathrm{NFI}_{PB_4}(B_4)$ | $PB_4$ に含まれる $B_4$ の有限指数正規部分群のなす poset | p.4 §1.2 |
| $\mathrm{GT}^{B_4}(N)$ | target $N$ の GT-shadow 全体 | **Def 2.9** (p.17) |
| $\mathrm{GT}^{\heartsuit,B_4}(N)$ | うち **charming** なもの | p.28 |
| $I^{B_4}:=\mathrm{NFI}^{\rm isolated}_{PB_4}(B_4)$ | isolated 対象のなす部分 poset | **Def 3.2** (p.29) |
| $\mathrm{ML}^{B_4}(N)$ | isolated $N$ に対する有限群 $=\mathrm{GT}^{\heartsuit,B_4}(N)$ | **Prop 3.7** (p.31) |
| $\mathrm{ML}^{B_4}_{K,N}$ | $K\le N$(共に isolated)の遷移 $=P_{K,N}\circ T_{m,f}$ | **(3.8)** (p.31) |
| $\iota_{K,N}$ | $K\le N$ の**自然写像** $\mathrm{GT}^{\heartsuit,B_4}(K)\to\mathrm{GT}^{\heartsuit,B_4}(N)$(isolated 不要) | **(3.24)** (p.38) |
| $\mathcal{PR}^{B_4}_N$ | $\widehat{GT}\to\mathrm{GT}^{\heartsuit,B_4}(N)$、$\hat T\mapsto T_N:=\widehat P_N\circ\hat T\circ I$ | **(2.31)** (p.16) |
| $\mathrm{Ih}$ | $G_{\mathbb Q}\to\widehat{GT}$(Belyi により単射) | **(1.1)** (p.2) |
| $\mathrm{Ih}^{B_4}_N$ | $:=\mathcal{PR}^{B_4}_N\circ\mathrm{Ih}$(**本追補の記号**) | 本追補 §E-A.3 |
| $\mathrm{GT}^{B_4}_{\rm arith}(N)$ | $:=\mathrm{Ih}^{B_4}_N(G_{\mathbb Q})$(**本追補の記号**) | 本追補 §E-A.3 |
| $\mathrm{GT}^{B_4}_{\rm gen}(N)$ | $:=\mathcal{PR}^{B_4}_N(\widehat{GT})=\{$genuine な shadow$\}$ | **Def 2.19** (p.25) |

> ### ⚠ 主線との**同名別物**警告(全編にかかる)
> - $\mathrm{GT}^{B_4}(N)$ と主線の $\mathrm{GT}(N)$ は**別物**(前者は pentagon を課す・後者は hexagon のみ)。
> - **settled / isolated の語は両系で同じだが所属 poset が違う**($\mathrm{NFI}_{PB_4}(B_4)$ vs $\mathrm{NFI}_{PB_3}(B_3)$)。
> - $B_4$ 側に **$K^{(n)}$ 族に相当するものは存在しない**(2008 に dihedral 予想は無い・§E-A.7)。**「$K^{(n)}$ の $B_4$ 版」と書いてはならない。**

---

## E-A.2 逐語 pin 表(2008.00066)

**出所**: reader 逐語抽出(150dpi ページ画像照合)。**★ 印の 4 本は本追補起草者が原文テキストで独立に再確認した**(行番号を併記)。

### E-A.2.1 ★ 最重要 pin — **Thm 3.8 の $\widehat{GT}$ は pentagon つきか**

| 札 | 逐語 | 出所 |
|---|---|---|
| **(LIM$^{B_4}$)** ★ | "*The (profinite version) $\widehat{GT}$ of the Grothendieck-Teichmueller group is isomorphic to $\lim(\mathrm{ML})$.*" | **Theorem 3.8** p.33(txt L2555) |
| **(GT-DEF)** | "*By definition, $\widehat{GT}$ is the group $\mathrm{Aut}(\widehat{\mathrm{PaB}})$ of (continuous) automorphisms of the profinite completion $\widehat{\mathrm{PaB}}$ of $\mathrm{PaB}$.*" | p.3 |
| **(PENT$^{B_4}$)** | **Def 2.6** (p.13): GT-pair は hexagon 2 本 **(2.18)(2.19)** に加え **pentagon (2.20)** を満たす対 | p.13 |
| **(RMK13)** ★ | **Remark 1.3**: "*Recall [15] that, omitting the pentagon relation from the definition of $\widehat{GT}$, we get the coarse version $\widehat{GT}_0$ … $\widehat{GT}_0$ is the group of continuous automorphisms of the truncated operad $\widehat{\mathrm{PaB}}^{\le3}$ and $\widehat{GT}$ is a subgroup of $\widehat{GT}_0$.*" | p.5 |

$$\boxed{\ \textbf{判定: Thm 3.8 の }\widehat{GT}\textbf{ は pentagon つきの Drinfeld }\widehat{GT}\textbf{ で確定。}\ }$$
**根拠 3 系統**: ① (GT-DEF) が $\mathrm{Aut}(\widehat{\mathrm{PaB}})$(全 arity)② (PENT$^{B_4}$) が pentagon を課す ③ **(RMK13) が pentagon を落とした粗版を $\widehat{GT}_0$ と別名で呼び、$\widehat{GT}\subsetneq\widehat{GT}_0$ と明示的に対比している** — ③ が決定的である(著者自身が両者を区別している)。

⟹ **札 A の着想の根拠は確定した。$B_4$ 塔の極限は「gentle 版」ではなく「本物」である。**

### E-A.2.2 ★ しかし暗黙の同定が 1 つある — **(TRUNC$^{B_4}$)**

Thm 3.8 の証明(§3.2 pp.33–38)が実際に構成しているのは **$\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})$** の元である(全射性の段: "*defines a morphism of truncated operads in groupoids $\hat T:\widetilde{\mathrm{PaB}}^{\le4}\to\widetilde{\mathrm{PaB}}^{\le4}$*"、および Prop 2.18 (p.25) が "*automorphism $\hat T$ of $\widehat{\mathrm{PaB}}^{\le4}$*")。一方 (GT-DEF) は $\mathrm{Aut}(\widehat{\mathrm{PaB}})$(非切断)。

> ### 前件 (TRUNC$^{B_4}$)
> $$\mathrm{Aut}(\widehat{\mathrm{PaB}})\ \cong\ \mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4}).$$
> **格: ★ 暗黙の前件**。2008 に**番号つき補題は存在しない**(reader の全文検索 + 起草者の照合の範囲で)。導出経路は **Theorem A.1** (p.48・"*any relation on $\alpha$ and $\beta$ in $\mathrm{PaB}$ is a consequence of (A.13), (A.14) and (A.15)*" = pentagon 1 + hexagon 2)+ p.3 の "*$\beta$ and $\alpha$ … are topological generators of $\widehat{\mathrm{PaB}}$, every $\hat T\in\widehat{GT}$ is uniquely determined by its values*" と目されるが、**起草者はこの導出を自分で検証していない**。

> ### ★ U-10 との比較(**交換の正直な会計**)
> | | $B_3$-gentle 系(v1 追補 A.2) | $B_4$ 系(本追補) |
> |---|---|---|
> | 欠けている同定 | **U-10**: $\widehat{GT}=\widehat{GT}_{\rm gen}$ | **(TRUNC$^{B_4}$)**: $\mathrm{Aut}(\widehat{\mathrm{PaB}})\cong\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})$ |
> | 格 | ★ **未解決の予想**(正典・定義ノート §8.1) | **記述の穴**(番号つき補題が無いだけ。Thm A.1 から導出可能と目される) |
> | 難度 | 研究レベルの未解決問題 | pin 作業(reader 案件) |
>
> ⟹ **交換は等価ではなく、真の前進である。ただし「前件が完全に消えた」と書いてはならない。**

### E-A.2.3 その他の pin

| 札 | 逐語 | 出所 |
|---|---|---|
| **(SET$^{B_4}$)** | **Def 3.2** (p.29): "*A charming GT-shadow $[(m,f)]$ is called **settled** if its source coincides with $N$, i.e. $\ker(T_{m,f})=N$. An element $N$ … is called **isolated** if every GT-shadow in $\mathrm{GT}^\heartsuit(N)$ is settled.*" | p.29 |
| **(GRP$^{B_4}$)** | Def 3.2 直後: "*$N$ is isolated if and only if the groupoid $\mathrm{GTSh}^\heartsuit_{\rm conn}(N)$ has exactly one object. In this case, $\mathrm{GT}^\heartsuit(N)$ is the group of automorphisms of the object $N$ …*" | p.29 |
| **(SRC$^{B_4}$)** | **Prop 2.11** (p.18): source $N_s:=\ker(T^{PB_4}_{m,f})\trianglelefteq PB_4$。**Prop 2.22 (2.65)**: $\mathrm{Hom}_{\mathrm{GTSh}^\heartsuit}(\widetilde N,N)=\{[(m,f)]\in\mathrm{GT}^\heartsuit(N)\mid\widetilde N=\ker(T^{PB_4}_{m,f})\}$ | pp.18, 28 |
| **(GEN$^{B_4}$)** | **Def 2.19** (p.25): "*A GT-shadow $[(m,f)]\in\mathrm{GT}(N)$ is called **genuine** if it comes from an automorphism of $\widehat{\mathrm{PaB}}$. Otherwise, $[(m,f)]$ is called **fake**.*" 図式版 = **(1.7)** (p.5) | p.25 |
| **(CHM$^{B_4}$)** | **Prop 2.20** (p.26): "*Every genuine GT-shadow is charming.*" | p.26 |
| **(PR$^{B_4}$)** | **(2.31)** (p.16): $T_N:=\widehat P_N\circ\hat T\circ I$。成分形($\mathrm{Cor}$ 2.21 の証明中 p.27): $(\hat m,\hat f)\mapsto(\widehat P_{K_{\rm ord}}(\hat m),\ \widehat P_{K_{F_2}}(\hat f))$ | p.16, 27 |
| **(COF$^{B_4}$)** ★ | **Corollary 3.5** (p.30・txt L2396): "*The subposet $\mathrm{NFI}^{\rm isolated}_{PB_4}(B_4)$ of $\mathrm{NFI}_{PB_4}(B_4)$ is cofinal.*" **かつ直後の地の文**: "*Although, Corollary 3.5 implies that the poset $\mathrm{NFI}^{\rm isolated}_{PB_4}(B_4)$ is **directed** (it is a cofinal subposet of a directed poset), it is still useful to know that …*" | p.30 |
| **(INT$^{B_4}$)** ★ | **Proposition 3.6** (p.30・txt L2406): "*For every $N^{(1)},N^{(2)}\in\mathrm{NFI}^{\rm isolated}_{PB_4}(B_4)$, $N^{(1)}\cap N^{(2)}$ is also an isolated element of $\mathrm{NFI}_{PB_4}(B_4)$.*" **★ 証明あり**(pp.30–31) | p.30 |
| **(HOM$^{B_4}$)** | **Prop 3.7** (p.31): $N\mapsto\mathrm{ML}(N)$ は $I^{B_4}\to\mathbf{FinGrp}$ の関手。$\mathrm{ML}_{K,N}(T_{m,f}):=P_{K,N}\circ T_{m,f}$ **(3.8)**。群準同型であることの証明は Prop 3.7 の証明本体(pp.31–33) | p.31 |
| **(NAT$^{B_4}$)** ★ | **(3.24)** (p.38・txt L3016): "*if $K\le N$, then we have a natural map $\mathrm{GT}^\heartsuit(K)\to\mathrm{GT}^\heartsuit(N)$. It makes sense to consider this map even if neither $K$ nor $N$ are isolated.*"(同じ対 $(m,f)$ が両方を代表する) | p.38 |
| **(SURV-DEF)** ★ | **Def 3.12** (p.38): "*$[(m,f)]\in\mathrm{GT}^\heartsuit(N)$ **survives into** $K$ if $[(m,f)]$ belongs to the image of the map (3.24).*" | p.38 |
| **(COR313)** ★ | **Corollary 3.13** (p.38・txt L3028): "*Let $N\in\mathrm{NFI}_{PB_4}(B_4)$ and $[(m,f)]\in\mathrm{GT}^\heartsuit(N)$. The GT-shadow $[(m,f)]$ is genuine if and only if $[(m,f)]$ survives into $K$ for every $K\in\mathrm{NFI}_{PB_4}(B_4)$ such that $K\le N$.*" **★ 証明本文なし**(前置き "*The following statement is a straightforward consequence of Proposition 3.3 and Theorem 3.8*" + $\square$ のみ) | p.38 |
| **(CYC$^{B_4}$)** | **Remark 2.17** (p.24): $g\in G_{\mathbb Q}$ から誘導される $[(m,f)]\in\mathrm{GT}(N)$ に対し $\mathrm{Ch}_{\rm cyclot}(m,f)(x_{12}N_{PB_2})=x_{12}^{\chi(g)_{N_{\rm ord}}}N_{PB_2}$ **(2.57)**($\chi$ は円分指標) | p.24 |
| **(IHARA)** | p.2: "*one can produce a natural group homomorphism $G_{\mathbb Q}\to\widehat{GT}$ **(1.1)** and, due to Belyi's theorem, this homomorphism is injective. … **the famous question on surjectivity of (1.1) posed by Ihara at his ICM address is still open.***" | p.2 |

---

## E-A.3 補題 BRIDGE$^{B_4}$ — **groupoid 型ずれの処理**(発案係の懸念 A-1)

> ### 懸念の実体
> 2008 の $\mathrm{GTSh}^\heartsuit$ は **groupoid で対象が動く**。$[(m,f)]:\widetilde N\to N$ で $\widetilde N=\ker T^{PB_4}_{m,f}$(**(SRC$^{B_4}$)**)。したがって $\mathrm{GT}^{\heartsuit,B_4}(N)$ は**一般には群ではない**(**(GRP$^{B_4}$)** より、群になるのは $N$ が isolated のときだけ)。主線 2401 の $\mathrm{GT}(N)$ を「$N$ の自己同型群」と読む習慣を持ち込むと事故になる。

> ### 補題 BRIDGE$^{B_4}$(**型の整理** — 3 点)
> **(1) 四層**: 任意の $N\in\mathrm{NFI}_{PB_4}(B_4)$ に対し
> $$\mathrm{GT}^{B_4}_{\rm arith}(N)\ \subseteq\ \mathrm{GT}^{B_4}_{\rm gen}(N)\ \subseteq\ \mathrm{GT}^{\heartsuit,B_4}(N)\ \subseteq\ \mathrm{GT}^{B_4}(N).\tag{1.A$^{B_4}$}$$
> 第 2 の包含は **(CHM$^{B_4}$)**(genuine $\Rightarrow$ charming)。**主線 (1.A) が三層なのに対し $B_4$ 側は四層** — charming の層が明示に挟まるのが差である。
> **(2) $\mathcal{PR}^{B_4}_N$ は isolated 性なしに well-defined な集合写像**: $\hat T\in\widehat{GT}$ に対し $T_N:=\widehat P_N\circ\hat T\circ I$ は **(PR$^{B_4}$)** で GT-shadow を定め、**(GEN$^{B_4}$)** より genuine、**(CHM$^{B_4}$)** より charming。ゆえに $T_N\in\mathrm{GT}^{\heartsuit,B_4}(N)$。**群準同型になるのは $N$ が isolated のとき**(Thm 3.8 の証明中の (3.19) の $N$ 成分)。
> **(3) 使い分けの規約**:
> - **集合水準の主張**(系 FAKE-KILL$^{B_4}$)⟹ **isolated 制限は不要**。
> - **群・関手・逆極限を使う主張**(補題 SURV$^{B_4}$ の $(\Leftarrow)$ 方向、ML-ODD$^{B_4}$)⟹ **添字を $I^{B_4}$ に制限する**。**(COF$^{B_4}$)** により制限しても射程は失われない。

**証明.** (1) 第 1 の包含は $\mathrm{Ih}(G_{\mathbb Q})\subseteq\widehat{GT}$ から。第 2 は (CHM$^{B_4}$)。第 3 は定義。(2)(3) は上記のとおり。$\blacksquare$

> ### 定義 $\mathrm{Ih}^{B_4}_N$(**本追補の記号**)
> $$\mathrm{Ih}^{B_4}_N:=\mathcal{PR}^{B_4}_N\circ\mathrm{Ih}\ :\ G_{\mathbb Q}\longrightarrow\mathrm{GT}^{\heartsuit,B_4}(N),\qquad \mathrm{GT}^{B_4}_{\rm arith}(N):=\mathrm{Ih}^{B_4}_N(G_{\mathbb Q}).$$
> これは主線 (1.11) $\mathrm{Ih}_N=\mathcal{PR}_N\circ\mathrm{Ih}$ の $B_4$ 版であり、**新しい写像を作ってはいない** — 正典の (1.1) と (2.31) を合成しただけである(v1 補題 IH-FACT の★注と同じ構造)。$N$ が isolated なら群準同型。

---

## E-A.4 系 FAKE-KILL$^{B_4}$ と前件表

### E-A.4.1 系

> ### 系 FAKE-KILL$^{B_4}$(**点ごとの最小形**)
> **任意の**窓 $N\in\mathrm{NFI}_{PB_4}(B_4)$(isolated でなくてよい)に **非算術証人**
> $$g\ \in\ \mathrm{GT}^{B_4}_{\rm gen}(N)\ \setminus\ \mathrm{GT}^{B_4}_{\rm arith}(N)$$
> が **1 つでも**存在すれば、
> $$\boxed{\ \textbf{(IH-S) は偽 — すなわち井原予想の全射部 }G_{\mathbb Q}\to\widehat{GT}\textbf{ が偽。}\ }$$
> **前件は (IH-S) の否定を導くための最小形であり、U-10 を含まない。**

**証明.** $g$ が genuine ⟹ **(GEN$^{B_4}$)** より $g=\mathcal{PR}^{B_4}_N(\hat T)$ なる $\hat T\in\widehat{GT}$ が存在する。もし (IH-S) が真なら $\hat T=\mathrm{Ih}(\gamma)$ なる $\gamma\in G_{\mathbb Q}$ があり
$$g=\mathcal{PR}^{B_4}_N(\mathrm{Ih}(\gamma))=\mathrm{Ih}^{B_4}_N(\gamma)\in\mathrm{GT}^{B_4}_{\rm arith}(N),$$
これは $g$ が非算術であることに反する。$\blacksquare$

> ### ★ $B_3$ 版との唯一の差(**これが札 A の全内容**)
> v1 追補 A.2 の系 FAKE-KILL($B_3$-gentle)は、**genuine の定義が $\widehat{GT}_{\rm gen}$(gentle 版)に対してなされている**ため、$\hat\sigma\in\widehat{GT}_{\rm gen}$ から $\hat\sigma\in\widehat{GT}$ へ渡るのに **U-10** を要した。
> $B_4$ 版では **(GEN$^{B_4}$)** が最初から $\widehat{GT}=\mathrm{Aut}(\widehat{\mathrm{PaB}})$(pentagon つき・§E-A.2.1)に対して定義されているので、**その一段が消える**。
> $$\text{FAKE-KILL}^{B_3}:\ \widehat{GT}_{\rm gen}\ \overset{\textbf{U-10}}{\dashrightarrow}\ \widehat{GT}\ \overset{\text{(IH-S)}}{\dashrightarrow}\ G_{\mathbb Q}\qquad\text{vs}\qquad\text{FAKE-KILL}^{B_4}:\ \widehat{GT}\ \overset{\text{(IH-S)}}{\dashrightarrow}\ G_{\mathbb Q}$$

> ### 系 FAKE-KILL$^{B_4}$ の対偶(**実質的な内容**)
> $$\textbf{(IH-S)}\ \Longrightarrow\ \forall N\in\mathrm{NFI}_{PB_4}(B_4):\ \mathrm{GT}^{B_4}_{\rm arith}(N)=\mathrm{GT}^{B_4}_{\rm gen}(N).$$
> **U-10 なしで**「井原予想は全 $B_4$ 窓で算術と genuine の一致を強制する」が言える。

### E-A.4.2 ★ 前件表(**U-10 の不在を明示**・FAM-U-ASM 方式)

**最短鎖**(FAKE-KILL$^{B_4}$ の導出に**実際に使う段だけ**):

| 段 | 内容 | 使う前件 |
|---|---|---|
| **(B0)** | 定義: $\mathrm{Ih}$ (1.1)、$\mathcal{PR}^{B_4}_N$ (2.31)、$\mathrm{Ih}^{B_4}_N:=\mathcal{PR}^{B_4}_N\circ\mathrm{Ih}$ | 正典の定義のみ |
| **(B1)** | $\mathcal{PR}^{B_4}_N$ の像が $\mathrm{GT}^{\heartsuit,B_4}(N)$ に入る | **(PR$^{B_4}$)**・**(CHM$^{B_4}$)** |
| **(B2)** | genuine $=\mathcal{PR}^{B_4}_N$ の像(定義そのもの) | **(GEN$^{B_4}$)** |
| **(B3)** | (IH-S) $\Rightarrow$ $\mathrm{GT}^{B_4}_{\rm gen}(N)=\mathrm{GT}^{B_4}_{\rm arith}(N)$ | **(IH-S)** のみ |
| **(B4)** | 対偶 $\Rightarrow$ **FAKE-KILL$^{B_4}$** | — |

**鎖は 4 段**($B_3$ 版の (A0)–(A7) が 8 段だったのに対し半分)。

**前件表**:

| 札 | 言明 | 格 | 出所 | **落とすと壊れるもの** |
|---|---|---|---|---|
| **(IH-S)** | $\mathrm{Ih}:G_{\mathbb Q}\twoheadrightarrow\widehat{GT}$ | ★ **UNKNOWN**(P6) | 2008 (1.1) p.2 | 前提そのもの |
| **(GEN$^{B_4}$)** | genuine $=$ $\widehat{GT}$ の元からの射影 | **正典の定義** | Def 2.19 p.25 / (1.7) p.5 | (B2) が消え、証人が何を意味するか定まらない |
| **(PR$^{B_4}$)** | $T_N:=\widehat P_N\circ\hat T\circ I$ が GT-shadow | **正典の定義+命題** | (2.31) p.16 | (B1) が消える |
| **(CHM$^{B_4}$)** | genuine $\Rightarrow$ charming | **正典の定理** | Prop 2.20 p.26 | 四層 (1.A$^{B_4}$) の第 2 包含が消える。**FAKE-KILL$^{B_4}$ 本体は $\mathrm{GT}^{B_4}(N)$ 水準で述べれば生き残る**(格下げであって破綻ではない) |
| **(TRUNC$^{B_4}$)** | $\mathrm{Aut}(\widehat{\mathrm{PaB}})\cong\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})$ | ★ **暗黙**(番号つき補題なし・Thm A.1 から導出可と目される) | §E-A.2.2 | **(LIM$^{B_4}$) の読みが揺れる**(Thm 3.8 が切断版の話になる)⟹ **補題 SURV$^{B_4}$ が壊れる**。**FAKE-KILL$^{B_4}$ 本体は無傷**((GEN$^{B_4}$) だけで閉じるため) |

### ★ 除外欄(= 前件では**ない**もの・混ぜないこと)

| 除外するもの | 理由 |
|---|---|
| ★★ **(U-10)**($\widehat{GT}=\widehat{GT}_{\rm gen}$) | ★ **$B_4$ 系では前件でない**。2008 の $\widehat{GT}$ は最初から pentagon つきの Drinfeld $\widehat{GT}$ である(**(GT-DEF)+(PENT$^{B_4}$)+(RMK13)** の 3 系統・§E-A.2.1)。**gentle 版との同定が要らない** ⟹ **これが札 A の全内容** |
| **(LIM$^{B_4}$)** Thm 3.8 | **FAKE-KILL$^{B_4}$ 本体では不要**(集合水準の一行)。**補題 SURV$^{B_4}$(§E-A.5)でのみ要る** |
| **(INT$^{B_4}$) / (COF$^{B_4}$) / (HOM$^{B_4}$)** | 同上。**群構造も isolated 性も FAKE-KILL$^{B_4}$ には不要** |
| **(COR313)** | 同上。証人の genuine 性を**別途**確立する必要があるが、その手段は前件表の外(§E-A.7) |
| **$K^{(n)}$ 族・odd Conj 5.1・E1-3・ML-ODD** | **すべて $B_3$ 側の話であり $B_4$ 側に対応物が無い**。混ぜないこと |

### E-A.4.3 ★★ **新規性の訂正 — 正典が既に述べている**

> **2008 Remark B.3(p.52・txt L4317-4319、起草者が原文で確認)逐語**:
> "*Note that, in the Abelian setting, every charming GT-shadow comes from an element of $G_{\mathbb Q}$. The authors do not know whether there is a genuine GT-shadow (in the non-Abelian setting) that does not come from an element of $G_{\mathbb Q}$. **Of course, if such a GT-shadow exists then the homomorphism (1.1) is not onto**$^{15}$.*"
> **脚注 15**(txt L4324): "*Some mathematicians believe that, in modern mathematics, there are no tools for tackling this question.*"

$$\boxed{\ \textbf{系 FAKE-KILL}^{B_4}\textbf{ は正典が既に述べている。新結果ではない。}\ }$$

- 「genuine GT-shadow that does not come from an element of $G_{\mathbb Q}$」= 本追補の**非算術証人**(v1 追補 A.1 の用語)。
- 「then the homomorphism (1.1) is not onto」= **(IH-S) が偽**。
- 著者は "**Of course**" と書いており、自明な含意として扱っている。⟹ **工房の系 FAKE-KILL($B_3$ 版)も、U-10 の一段を除けば正典が自明としている論法である。**

**⟹ 本追補が新しく置くもの(申告)**:
1. **前件表**(§E-A.4.2)— 正典は含意を 1 文で書くだけで、**何が前件で何が前件でないかの表を持たない**。とくに **U-10 の不在**と **(TRUNC$^{B_4}$) の暗黙性**を同じ表に並べたのは本追補である。
2. **$B_3$ 版との差分管理**(§E-A.4.1 の★枠・§E-A.7 の交換表)— 2008 は 2401 より前の論文なので、gentle 版との比較は**原理的に正典に無い**。
3. **(COR313) の自前証明**(§E-A.5)。
4. **$B_3$ 側への配当**(§E-A.6)。

---

## E-A.5 (COR54)$^{B_4}$ — **条文はあるが証明本文が無い** ⟹ 自前補完

### E-A.5.1 所在の確定

**2401 Cor 5.4 の $B_4$ 対応物は存在する** = **2008 Corollary 3.13**(§E-A.2.3 に逐語)。**2401 版との差分 3 点**:

| # | 差分 | 影響 |
|---|---|---|
| 1 | 前提が $[(m,f)]\in\mathrm{GT}^{\heartsuit,B_4}(N)$(**charming に限定**) | 非 charming なら **(CHM$^{B_4}$)** の対偶で自動的に fake。⟹ **射程の損失なし** |
| 2 | $K$ の走る範囲は $\mathrm{NFI}_{PB_4}(B_4)$ 全体($K\le N$)・**isolated 制限なし** | 2401 Cor 5.4 と**同じ形**(追補 B.1 の逐語照合と一致) |
| 3 | ★ **証明本文が無い**("*a straightforward consequence of Proposition 3.3 and Theorem 3.8*" + $\square$) | ⟹ **自前補完が要る**(委嘱の指示どおり) |

> ### ★ 「証明未掲載」の 3 例目
> 工房がこの研究計画で当たった「主柱の条文に証明本文が無い」事例:
> 1. **2401 Prop 3.15**(isolated $\cap$ isolated)— 「読者演習」明記(追補 B.1)
> 2. **2405 Thm 4.4 の奇 $q$ 分岐**(reduction 全射性)— 読者演習分岐を経由(追補 E-F §E-F.2.2)
> 3. **2008 Cor 3.13**(genuine $\iff$ 全細分 survive)— 本節
> (加えて **2405 Prop 4.1 の偶 $m$ 分岐**・追補 E-F §E-F.3.1。)
> ⟹ **司令塔への申し送り**: これは偶然ではなく系統的である。**正典から条文を引くときは「証明本文の有無」を pin 項目に加えることを規約化すべき**(§E-A.8.4)。

### E-A.5.2 補助補題(遷移写像と自然写像の一致)

> ### 補題 RED-CMP$^{B_4}$
> $K\le N$ が共に isolated のとき、$\mathrm{ML}^{B_4}_{K,N}:\mathrm{ML}^{B_4}(K)\to\mathrm{ML}^{B_4}(N)$ は自然写像 $\iota_{K,N}$ **(3.24)** に一致する。

**証明(pin による).** **(HOM$^{B_4}$) (3.8)** は $\mathrm{ML}_{K,N}(T_{m,f}):=P_{K,N}\circ T_{m,f}$。正典 **Prop 3.6 の証明中の一文**(p.30・起草者が原文で確認・txt L2418-2422)が、まさにこの合成を対 $(m,f)$ で読み替えている:

> "*Since $K\le N^{(1)}$ and $K\le N^{(2)}$, **the pair $(m,f)$ also represents a GT-shadow in $\mathrm{GT}^\heartsuit(N^{(1)})$** and a GT-shadow in $\mathrm{GT}^\heartsuit(N^{(2)})$. Moreover, **the compositions $P_{K,N^{(1)}}\circ T^{PB_4}_{m,f}$ and $P_{K,N^{(2)}}\circ T^{PB_4}_{m,f}$ are the homomorphisms $PB_4\to PB_4/N^{(1)}$ and $PB_4\to PB_4/N^{(2)}$ corresponding to these GT-shadows** …*"

すなわち「$P_{K,N}\circ T_{m,f}$ が定める shadow」$=$「同じ対 $(m,f)$ が target $N$ で定める shadow」$=$ **(NAT$^{B_4}$) (3.24)** の像。$\blacksquare$

⚠ **格の申告**: 2008 は (3.8) と (3.24) を**明示的に同一視する番号つき主張を持たない**。上の pin は **Prop 3.6 の証明中の地の文**である。⟹ **paper-proof candidate(pin は地の文)**。

### E-A.5.3 補題 SURV$^{B_4}$(= 2008 Cor 3.13 の自前証明)

> ### 補題 SURV$^{B_4}$
> $N\in\mathrm{NFI}_{PB_4}(B_4)$、$[(m,f)]\in\mathrm{GT}^{\heartsuit,B_4}(N)$ とする。次は同値。
> **(a)** $[(m,f)]$ は genuine。
> **(b)** すべての $K\in\mathrm{NFI}_{PB_4}(B_4)$($K\le N$)に対し $[(m,f)]$ は $K$ へ survive する。

**証明.**

**(a) $\Rightarrow$ (b).** $[(m,f)]=T_N=\widehat P_N\circ\hat T\circ I$ なる $\hat T\in\widehat{GT}$ を取る。$K\le N$ とする。$T_K:=\widehat P_K\circ\hat T\circ I$ は genuine な GT-shadow(target $K$)であり、**(CHM$^{B_4}$)** より $T_K\in\mathrm{GT}^{\heartsuit,B_4}(K)$。射影の分解 $\widehat P_N=P_{K,N}\circ\widehat P_K$ より
$$T_N=P_{K,N}\circ\widehat P_K\circ\hat T\circ I=P_{K,N}\circ T_K .$$
**補題 RED-CMP$^{B_4}$** により右辺は $\iota_{K,N}(T_K)$。ゆえに $[(m,f)]=T_N\in\mathrm{Im}\,\iota_{K,N}$、すなわち $K$ へ survive する。

**(b) $\Rightarrow$ (a).**

*(段 1) isolated への還元.* $K\in\mathrm{NFI}_{PB_4}(B_4)$、$K\le N$ を任意に取る。**(COF$^{B_4}$)** より isolated $K'\le K$ が存在する($K'\le N$ でもある)。**(3.24)** は対 $(m,f)$ を保つので $\iota_{K,N}=\iota_{K',N}$ の分解 $\iota_{K,N}\circ\iota_{K',K}=\iota_{K',N}$ が成り立つ。ゆえに **$K'$ へ survive すれば $K$ へも survive する**。⟹ 仮定 (b) を **isolated な $K\le N$** に限っても同値。

*(段 2) 添字集合.* $I^{B_4}_N:=\{K\in I^{B_4}\mid K\le N\}$ と置く。
- **有向**: $K_1,K_2\in I^{B_4}_N$ に対し $K_1\cap K_2$ は **(INT$^{B_4}$)**(Prop 3.6・**証明つき**)より isolated で $\le N$。(**(COF$^{B_4}$)** の地の文の論法でも同じ結論。)
- **$I^{B_4}$ の中で共終**: 任意の $K'\in I^{B_4}$ に対し $K'\cap N\in\mathrm{NFI}_{PB_4}(B_4)$、**(COF$^{B_4}$)** より isolated $K''\le K'\cap N$ が取れる。$K''\in I^{B_4}_N$ かつ $K''\le K'$。
⟹ 共終部分 poset 上の極限は一致するので、**(LIM$^{B_4}$)** と合わせて
$$\varprojlim_{I^{B_4}_N}\mathrm{ML}^{B_4}\ =\ \varprojlim_{I^{B_4}}\mathrm{ML}^{B_4}\ \cong\ \widehat{GT}.$$

*(段 3) 逆部分系.* $K\in I^{B_4}_N$ に対し
$$Y_K:=\{\,h\in\mathrm{ML}^{B_4}(K)\ \mid\ \iota_{K,N}(h)=[(m,f)]\,\}.$$
- **$Y_K\ne\emptyset$**: 段 1 の形の仮定 (b)。
- **有限**: $\mathrm{ML}^{B_4}(K)$ は有限群(**(GRP$^{B_4}$)**・Prop 3.7)。
- **逆系をなす**: $K'\le K$($\in I^{B_4}_N$)で $h\in Y_{K'}$ なら、**補題 RED-CMP$^{B_4}$** より $\mathrm{ML}^{B_4}_{K',K}(h)=\iota_{K',K}(h)$、ゆえに $\iota_{K,N}(\mathrm{ML}^{B_4}_{K',K}(h))=\iota_{K',N}(h)=[(m,f)]$、すなわち $\mathrm{ML}^{B_4}_{K',K}(h)\in Y_K$。

*(段 4) コンパクト性.* 有向 poset 上の空でない有限集合の逆系は極限が空でない(v1 補題 ML-3 $=$ (CPT)・Bourbaki)。ゆえに $\sigma\in\varprojlim_{I^{B_4}_N}Y\ne\emptyset$ を取る。段 2 より $\sigma\in\varprojlim\mathrm{ML}^{B_4}\cong\widehat{GT}$、対応する $\hat T\in\widehat{GT}$ を取る。

*(段 5) 結論.* 任意の $K\in I^{B_4}_N$ で $\sigma_K=T_K$(Thm 3.8 の同型 (3.19) は $\hat T\mapsto\{T_K\}$ で与えられる)。$\sigma_K\in Y_K$ だから
$$T_N=P_{K,N}\circ T_K=\iota_{K,N}(T_K)=[(m,f)].$$
すなわち $[(m,f)]$ は $\hat T$ から来る = genuine。$\blacksquare$

> ### ★ 依存の向きの確認(**非循環**)
> 使ったのは **(GEN$^{B_4}$)・(CHM$^{B_4}$)・(PR$^{B_4}$)・(NAT$^{B_4}$)・(SURV-DEF)・(COF$^{B_4}$)・(INT$^{B_4}$)・(HOM$^{B_4}$)・(LIM$^{B_4}$)・(CPT)・補題 RED-CMP$^{B_4}$** のみ。**(COR313) 自身を一切使っていない。** また **(LIM$^{B_4}$) の証明**(§3.2)は Prop 3.3 / 3.9 / Cor 3.10 / Prop 3.11 に依り、**(COR313) を使わない** ⟹ 循環なし。
> 正典の前置き「Prop 3.3 と Thm 3.8 の直接の帰結」とも整合する(本証明は Prop 3.3 を **(COF$^{B_4}$)** = Cor 3.5 の形で使っている)。⟹ **本補完は正典の主張の忠実な展開であり、別ルートではない。**

> ### ★ 構造の申告(**新規性の正直な形**)
> 上の証明は **v1 §4.3 定理 ML-ODD の (iii)$\Rightarrow$(i) の論法の逐語移植**である($Y_N$ の構成・逆部分系・コンパクト性・極限の元を $\widehat{GT}$ の元と読む段)。**新しい論法は一つも無い。** 委嘱が求めた「一頁再演」はこの意味で成立した — **工房の ML 機構は $B_4$ 系にそのまま乗る**。

### E-A.5.4 ML-ODD$^{B_4}$ の型(**述べるだけ・証明しない**)

> ### 系 ML-ODD$^{B_4}$ の型
> 補題 SURV$^{B_4}$ と補題 BRIDGE$^{B_4}$ より、**$B_4$ 側でも v1 §4.3 と同じ形の同値**が書ける:
> $$\bigl[\mathrm{GT}^{\heartsuit,B_4}(N)\ \text{の全 shadow が genuine}\bigr]\iff\bigl[\forall K\le N:\ \iota_{K,N}\ \text{が全射}\bigr].$$
> ⚠ **ただし $B_4$ 側には $\mathrm{Dih}^{\rm odd}$ に相当する窓の族が無い**ので、v1 の (i)$\iff$(ii)$\iff$(iii)(**族に沿った束ね**)に相当する部分は**書けない**。⟹ **ML-ODD$^{B_4}$ は「点ごと版」しか存在しない。** これは 2008 §4.2 の実測(24 組で $\iota$ が onto)と Question 4.6 が置かれている水準そのものである。

---

## E-A.6 ★ **$B_4$ 側読解の $B_3$ 側への配当**(本追補の最大の実収穫)

### E-A.6.1 発見

**(COF$^{B_4}$)** の直後の**地の文**(§E-A.2.3 に逐語)が次を明記している:

> "*Corollary 3.5 implies that the poset $\mathrm{NFI}^{\rm isolated}_{PB_4}(B_4)$ is **directed** (**it is a cofinal subposet of a directed poset**), it is still useful to know that the intersection of two isolated elements … is an isolated element*"

$$\Longrightarrow\ \boxed{\ \textbf{共終性だけで有向性が出る。交叉閉性(Prop 3.6 / Prop 3.15)は有向性には要らない。}\ }$$

**これを $B_3$ 側へ移す**:

> ### 補題 DIR-FROM-COF($B_3$-gentle 系)
> $I:=\mathrm{NFI}^{\rm isolated}_{PB_3}(B_3)$ は **(COF)**(追補 B.1 の pin = 2401 Prop 3.14 の系)だけから refinement 順序で**有向**である。**(INT) $=$ 補題 INT を使わない。**
>
> **証明.** ① $\mathrm{NFI}_{PB_3}(B_3)$ は有向: $N,H$ に対し $N\cap H$ は $B_3$ の有限指数正規部分群で $\subseteq PB_3$、ゆえ $\mathrm{NFI}_{PB_3}(B_3)$ の元で $N,H$ 両方を細分する。② **(COF)** より、$N,K\in I$ に対し $M:=N\cap K\in\mathrm{NFI}$ に $\widetilde N\in I$、$\widetilde N\subseteq M$ が取れる。$\widetilde N\subseteq N$ かつ $\widetilde N\subseteq K$。∎

### E-A.6.2 ihnec への波及(**追補 B.3 の「重さの差」の訂正**)

追補 B.3 は次の 2 行を書いていた:
- 「**(INT) が落ちると ML-ODD (iii)$\Rightarrow$(i) は全崩壊**(補題 ML-3 の有向性が消える)」
- 「**(COF) が落ちても定理は生き残る** — (ii) の量化を $\mathrm{NFI}$ 全体に戻せばよい」

**この 2 行は、それぞれ他方が存在しないかのように書かれていた。** 正しい形:

| 落ちるもの | ML-ODD への影響 |
|---|---|
| **(INT) のみ** | ★ **無傷** — **(COF)** が有向性を供給する(補題 DIR-FROM-COF) |
| **(COF) のみ** | **無傷** — **(INT)** が有向性を供給し、(ii) の量化を $\mathrm{NFI}$ 全体に戻せばよい |
| **両方** | 崩壊 |

$$\Longrightarrow\ \boxed{\ \textbf{ML-ODD は「(INT) }\vee\textbf{ (COF)」という}\textbf{選言}\textbf{に相対的である。}\ }$$

**格への影響**(追補 B.6 / D.6 の留保の緩和):

| 対象 | 追補 B.6 / D.6 | ★ 本追補後 |
|---|---|---|
| **ML-ODD** | 「格は **補題 INT(工房の紙上証明)に相対的**」 | ★ **その留保は解除できる**。**(COF) $=$ 2401 Prop 3.14 の系は証明つきの正典**(追補 B.1 で確認)であり、これだけで ML-ODD の有向性要求は満たされる。⟹ ML-ODD は**証明つきの正典条文のみに乗る** |
| **命題 ROOF(3)**($M=K^{(9)}\cap N_{\rm S4}$ の isolated 性) | (INT) 依存 | **変わらず (INT) 依存**(具体的な交叉の isolated 性は共終性では代替できない)⟹ **補題 INT は依然必要** |

⚠ **この訂正は追補 C(R4a)・追補 D の結論に波及しない**(ROOF(3) 側の依存は不変であり、R4a は証明書からの再導出で群構造を仮定していない)。**凍結物 P-IHN-1〜7 と検算 digest は不変。**

### E-A.6.3 ★ 補題 INT の新規性の訂正(**正典 grep で判明**)

2008 **Prop 3.6 の証明**(p.30–31・起草者が原文で確認・txt L2412-2436)の構造:

| 段 | 2008 Prop 3.6 の証明 | ihnec 追補 B.2 補題 INT の証明 |
|---|---|---|
| 段 1 | $P_{K,N^{(i)}}\circ T^{PB_4}_{m,f}$ が $N^{(i)}$ 側 shadow の $T$ 写像 $\Rightarrow$ $N^{(i)}$ isolated $\Rightarrow$ settled $\Rightarrow$ $K_s\le N^{(i)}$ ($i=1,2$) $\Rightarrow$ $K_s\le K$ | $\pi_N\circ T^M_{m,f}=T^N_{R_{M,N}([m,f])}$ $\Rightarrow$ $N$ isolated $\Rightarrow$ settled $\Rightarrow$ $K\subseteq N$(同様に $H$)$\Rightarrow$ $K\subseteq M$ |
| 段 2 | "*both subgroups have the same (finite) index in $PB_4$*" $\Rightarrow$ $K_s=K$ | $T^M_{m,f}$ 全射 $+$ 準同型定理 $\Rightarrow$ $[B_3:K]=[B_3:M]$ $\Rightarrow$ $K=M$ |

$$\Longrightarrow\ \boxed{\ \textbf{補題 INT は 2008 Prop 3.6 の証明の }B_3\textbf{-gentle 系への移植であり、独立発見ではない。}\ }$$

**格の訂正**(追補 D.6 の表への追記):

| # | 追補 D.6 | ★ 本追補後 |
|---|---|---|
| **補題 INT**(追補 B.2) | 「工房の自前証明 / 紙上相互監査 PASS(F98-3.4)」 | ★ **「2008 Prop 3.6(証明つき正典)の $B_3$-gentle 系への移植」**。**紙上相互監査 PASS は不変**。ただし **「工房が独立に考案した」とは書かない**(2401 が読者演習にした証明が、同著者の先行論文 2008 に載っていた) |

> ⚠ **これは補題 INT の価値を下げるものではない**: 2401 Prop 3.15 の言明に証明が無い以上、$B_3$-gentle 系での補完は必要であり、$B_4$ 版から $B_3$ 版への移送は自明ではない($PB_4$ vs $PB_3$・charming の扱い)。**訂正するのは新規性の申告だけである。**

---

## E-A.7 発案係の懸念 A-2 の検査 — **算術側装置の非対称**

### E-A.7.1 検査結果

| 問い | 結果 |
|---|---|
| $B_4$ 側に算術のフックはあるか | ★ **1 本だけある** — **(CYC$^{B_4}$) Remark 2.17 (2.57)**: $g\in G_{\mathbb Q}$ 由来の shadow は $\mathrm{Ch}_{\rm cyclot}$ が円分指標で決まる。**工房の $\widetilde\chi$ / $\chi_4$ 装置の $B_4$ 対応物**である |
| $B_4$ 側に窓の**族**はあるか | ★ **無い**。2008 に **dihedral 予想は存在しない**(Question 4.4–4.7 という open question の形のみ)。$K^{(n)}$ 族に相当する明示族も、$\mathrm{GT}^{B_4}(N)$ の明示式(2405 Thm 4.3 相当)も**無い** |
| 工房の $R^{\rm cyc}_{\rm formal}$($\mathrm{ord}(a_n)\ne n$)は移せるか | ★ **移せない**。この装置は $K^{(n)}$ の座標 $\Theta_n$ と $\mathrm{Aff}(\mathbb Z/n)\times C_2$ 構造に全面依存しており、$B_4$ 側にその土台が無い |
| $B_4$ 窓と $B_3$ 窓を結ぶ条文はあるか | ★ **無い**(起草者の照合範囲)。**(RMK13)** は $\widehat{GT}\subseteq\widehat{GT}_0=\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le3})$ を与えるが、**$\widehat{GT}_0$ と 2401 の $\widehat{GT}_{\rm gen}$ が同じかは UNKNOWN**(2008 は 2401 より前の論文・reader も同判定) |
| 2008 側の実測状況 | §4.2 (p.42): 24 組 $(N^{(i)},N^{(j)})$ で $\iota$ が onto を確認、"*we did not find a single example of a charming GT-shadow that is also fake*"。**Question 4.6** (p.43) で fake の存在自体が未解決と明記 |

### E-A.7.2 交換の会計(**札 A の正味**)

| | **FAKE-KILL($B_3$-gentle・v1 追補 A.2)** | **FAKE-KILL$^{B_4}$(本追補)** |
|---|---|---|
| 前件 | (U-10) $\wedge$ 非算術証人 @ $B_3$ 窓 | ★ **U-10 不要** $\wedge$ 非算術証人 @ $B_4$ 窓 |
| 暗黙の前件 | なし | **(TRUNC$^{B_4}$)**(FAKE-KILL 本体には効かない・§E-A.4.2) |
| genuine 側の装置 | (COR54)(証明つき正典)+ ML-ODD(工房)+ $K^{(n)}$ 明示式(Thm 4.3) | (COR313)(**証明なし** ⟹ 本追補 §E-A.5 で補完)+ **明示式なし** |
| 非算術性の装置 | ★ **$R^{\rm cyc}_{\rm formal}$($\mathrm{ord}(a_n)\ne n$)**・$\Theta_n$ 座標・証明書群 | ★ **(CYC$^{B_4}$) の 1 本のみ**・窓の族も証明書も無い |
| 工房の計算基盤 | GAP 証明書・窓 8 枚以上・$\mathrm{Dih}^{\rm odd}$ 塔 | ★ **ゼロ** |
| 正典での既述 | — | ★ **2008 Remark B.3 + 脚注 15 が既述** |

> ### 【IHNEC-GAP-6】(**新規・本追補が開く**)
> **FAKE-KILL$^{B_4}$ を発火させる装置が、工房にも正典にも無い。** 要るのは 2 つ:
> **(a)** ある $B_4$ 窓 $N$ で **genuine 性**を確立する(= 補題 SURV$^{B_4}$ の点ごと版を通す — **有限深度では出ない**、v1 §A.4 の壁と同じ)。
> **(b)** 同じ窓で **非算術性**を測る(= $\mathrm{GT}^{B_4}_{\rm arith}(N)\subsetneq$ を示す)。**(CYC$^{B_4}$) が唯一の足がかり**だが、円分指標が決めるのは $m$ 成分だけであり、$f$ 成分の障害を測る装置が無い。
> **状態: UNKNOWN(未着手)。**
>
> ### 【文献要請 IHNEC-L2】
> **困難**: $B_4$ 系($\mathrm{PaB}^{\le4}$・pentagon つき)の有限窓 $N\in\mathrm{NFI}_{PB_4}(B_4)$ で、$\mathrm{GT}^{\heartsuit,B_4}(N)$ の**明示的な記述**(生成元・位数・座標)を与える例が欲しい。とくに **$B_3$-gentle 系の $K^{(n)}$ 族(2405 Thm 4.3 の (4.12))に相当する、$B_4$ 窓の明示族**。
> **欲しい結果の型**: 「$N$ を明示に構成し、$\mathrm{GT}^{\heartsuit,B_4}(N)$ を有限群として同定した」型の結果。Dolgushev らの Python パッケージ GT(Temple 大)は 2008 §4 の実測基盤なので、**そこに窓の明示データがあれば代替になりうる**(第三者クロスチェック資源としても)。
> **なぜ要るか**: これが無い限り FAKE-KILL$^{B_4}$ は**発火装置のない撃鉄**である(【IHNEC-GAP-6】)。

### E-A.7.3 ★ 正直な結論(**IHNEC-GAP-3 への回答として**)

**IHNEC-GAP-3** は「U-10 を迂回して $\widehat{GT}$ 版だけを直接攻める経路があるか」であった。回答:

$$\boxed{\ \textbf{ある。}B_4\textbf{ 系へ移れば U-10 は前件から消える。しかし移った先に工房の装置は一つも無い。}\ }$$

- **論理的には**: 迂回路は存在し、前件は 4 段に減る(§E-A.4.2)。**IHNEC-GAP-3 は「経路の存在」については閉じた。**
- **実効的には**: 迂回路は【IHNEC-GAP-6】に突き当たる。**「U-10 という未解決予想」が「$B_4$ 側の計算基盤の不在」に置き換わった**だけであり、**どちらが安いかは現時点で不明**。
- ⟹ **IHNEC-GAP-3 の状態を「未検討」から「経路確定・実効性 UNKNOWN(【IHNEC-GAP-6】へ委譲)」へ更新する。**

---

## E-A.8 格付け・erratum・新規性・申し送り

### E-A.8.1 格付け

| # | statement | 状態 | 出所 |
|---|---|---|---|
| **BRIDGE$^{B_4}$** | 四層 (1.A$^{B_4}$) と型の使い分け | **paper-proof candidate**(定義の整理・Sol 未監査) | §E-A.3 |
| **FAKE-KILL$^{B_4}$** | 非算術証人 1 個 ⟹ $\neg$(IH-S)・**U-10 不要** | ★ **正典が既述**(2008 Remark B.3 + fn.15)。**工房の寄与は前件表のみ** | §E-A.4 |
| **前件表 / 除外欄(U-10 不在)** | — | **paper-proof candidate**(**本追補の実質**) | §E-A.4.2 |
| **RED-CMP$^{B_4}$** | (3.8) $=$ (3.24) | **paper-proof candidate**(pin は Prop 3.6 の証明中の**地の文**) | §E-A.5.2 |
| **SURV$^{B_4}$**(= 2008 Cor 3.13) | genuine $\iff$ 全細分 survive | ★ **paper-proof candidate**(**正典に証明本文が無い条文の補完**・非循環確認済・**v1 ML-ODD (iii)$\Rightarrow$(i) の逐語移植**・Sol 未監査) | §E-A.5.3 |
| **ML-ODD$^{B_4}$ の型** | 点ごと版のみ存在 | **観察**(族が無いので束ねられない) | §E-A.5.4 |
| **DIR-FROM-COF** | (COF) だけで $I$ は有向 | ★ **paper-proof candidate**(**2008 p.30 の地の文の $B_3$ 側への移植**) | §E-A.6.1 |
| **(TRUNC$^{B_4}$)** | $\mathrm{Aut}(\widehat{\mathrm{PaB}})\cong\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})$ | ★ **暗黙の前件・要 pin** | §E-A.2.2 |
| **(IH-S)** | — | **UNKNOWN**(P6) | 2008 (1.1) |

### E-A.8.2 erratum(**v1 本文・追補 B/D への訂正**)

**v1 本文・追補 A/B/C/D は不改変。** 以下の読み替えを行う。

| 対象 | 差替前 | ★ 差替後 |
|---|---|---|
| **追補 B.3 の「重さの差」2 行** | 「(INT) が落ちると全崩壊 / (COF) が落ちても生き残る」 | ★ **§E-A.6.2 の 3 行表に置換**。**ML-ODD は「(INT) $\vee$ (COF)」に相対的** |
| **追補 B.6 / D.6 の ML-ODD の格** | 「補題 INT(工房の紙上証明)に相対的」 | ★ **その留保は解除**。(COF) $=$ 証明つきの正典条文だけで有向性が出る(補題 DIR-FROM-COF)。**命題 ROOF(3) の (INT) 依存は不変** |
| **追補 D.6 の 補題 INT 行** | 「工房の自前証明 / 紙上相互監査 PASS」 | ★ **「2008 Prop 3.6(証明つき正典)の $B_3$-gentle 系への移植」**。PASS は不変・**新規性の申告のみ訂正**(§E-A.6.3) |
| **v1 §8 GAP 表 IHNEC-GAP-3** | 「未検討」 | ★ **「経路確定($B_4$ 系で U-10 が消える)・実効性 UNKNOWN」**。後段は【IHNEC-GAP-6】へ委譲 |
| **v1 §8 GAP 表** | — | **追加**: 【IHNEC-GAP-6】(§E-A.7.2)・【文献要請 IHNEC-L2】 |

> **凍結物は不変**: **P-IHN-1〜7**・検算 digest(`edf6181376…d49309`・`f8be65ae…c88820b`)は改訂なし。本追補は $B_3$ 側の実測に一切波及しない(§E-A.6.2 の ⚠ 枠)。

### E-A.8.3 新規性の申告(**grep 済**)

**grep 語**: `FAKE-KILL`・`B4`・`B_4`・`PB4`・`2008.00066`・`Thm 3.8`・`Cor 3.13`・`GTSh^♡`・`charming`・`cofinal`・`共終`・`有向`・`TRUNC`・`Aut(PaB`。

- **既出(工房内)**: 覚書 `docs/scout/覚書_upb4_2008_v1.md`(Thm 3.8・Prop 3.3・§2.5-2.6 charming・Remark 1.3)/ `docs/notes/gtpi_pb4_*`(PB₄ 窓の設計線)/ v1 追補 A.2 の FAKE-KILL($B_3$ 版)。
- **既出(正典)**: ★★ **FAKE-KILL$^{B_4}$ そのもの**(2008 Remark B.3 + 脚注 15)/ **有向性が共終性から出るという観察**(2008 p.30 地の文)/ **補題 INT の証明**(2008 Prop 3.6)。
- **本追補で新しいもの**: ① **前件表と除外欄**(U-10 の不在と (TRUNC$^{B_4}$) の暗黙性を同じ表に置く — 2008 は 2401 より前なので gentle 版との比較は原理的に正典に無い)② **補題 SURV$^{B_4}$**(2008 Cor 3.13 の証明本文の補完)③ **補題 DIR-FROM-COF と追補 B.3 の訂正**(**$B_3$ 側の格が上がる**)④ **補題 INT の新規性の訂正**(正典 grep の結果)⑤ **交換の会計表**(§E-A.7.2)と【IHNEC-GAP-6】。
- **「初」という語は使わない。** ★ **とくに「FAKE-KILL$^{B_4}$ は新しい」と書いてはならない**(§E-A.4.3)。

### E-A.8.4 Sol 監査の依頼(**優先順位つき**)

1. ★★ **§E-A.2.1 の判定の独立確認**(最優先)— 「2008 Thm 3.8 の $\widehat{GT}$ は pentagon つきの Drinfeld $\widehat{GT}$」。ここが崩れると札 A 全体が消える。とくに **(RMK13) の $\widehat{GT}_0$ との対比**の読みを見てほしい。
2. ★ **§E-A.6.1–6.2 の $B_3$ 側への配当** — 「共終部分 poset が有向」から $I$ の有向性を出す論法に穴が無いか。**ここが正しければ ML-ODD の格が一段上がる**ので、実利が最も大きい。
3. **補題 SURV$^{B_4}$** の段 1(isolated への還元)と段 2(共終性 ⟹ 極限の一致)。とくに **$I^{B_4}_N$ が $I^{B_4}$ で共終であること**の論法。
4. **補題 RED-CMP$^{B_4}$** — (3.8) と (3.24) の一致を **Prop 3.6 の証明中の地の文**で pin するのは十分か。番号つき条文を要求すべきか。
5. **(TRUNC$^{B_4}$)** — $\mathrm{Aut}(\widehat{\mathrm{PaB}})\cong\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})$ を Thm A.1 から導けるか(Sol が原文を持っているなら)。**導ければ前件表から★印が 1 つ消える。**

### E-A.8.5 申し送り(司令塔へ)

1. ★★ **札 A の結論を「決着」「新定理」として台帳・地図に登録しないこと**。正典が既述である(§E-A.4.3)。登録するなら **「前件表 $=$ U-10 不在の確定」+「IHNEC-GAP-3 の状態更新」** の形で。
2. ★ **§E-A.6 の配当は $B_3$ 主線に直接効く**ので、**Sol 監査の 2 位に置いた**。PASS すれば追補 B.6 / D.6 の留保が外れ、**ML-ODD が「証明つきの正典条文のみに乗る」**ことになる(補題 INT は ROOF(3) 用に残る)。
3. **規約提案(§E-A.5.1 の★枠)**: 正典から条文を引く際、pin 項目に **「証明本文の有無」** を必須欄として加えることを規約台帳に提案する。**4 例が出た**(2401 Prop 3.15 / 2405 Thm 4.4 奇分岐 / 2405 Prop 4.1 偶 $m$ 分岐 / 2008 Cor 3.13)— **系統的である。**
4. **(TRUNC$^{B_4}$) の pin を reader へ発注**するか(Thm A.1 p.48 + p.3 の生成元の議論から導出できるかの逐語確認)。**軽い案件**。
5. **【文献要請 IHNEC-L2】**(§E-A.7.2)— $B_4$ 窓の明示族。**Dolgushev の Python パッケージ GT に窓データがあれば代替になる**ので、文献より先に**そちらの棚卸し**が安いかもしれない(工房は `provenance/LEDGER.md` にパッケージ GT を入手済と記帳している)。
6. **reader からの副次報告**(本追補では使わなかったが記録): ① 2008 Def 3.2 の $\ker(T^{B_4}_{m,f})$ は他の全箇所が $PB_4$ なので**著者のタイポと推定** ② Introduction p.5 の "GT(N) is a group" は §3 の正式定義では $\mathrm{GT}^\heartsuit(N)$ であり**書き落としと推定** ③ ページ番号つき再抽出テキストが scratchpad にある(既存 `papers/txt/2008...txt` は form-feed が除去されておりページ復元不可)— **ページ引用を伴う $B_4$ 作業では再抽出版が要る**ので、`papers/txt/` の再生成を検討されたい。
