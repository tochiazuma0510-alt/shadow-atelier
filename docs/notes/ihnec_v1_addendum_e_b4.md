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

---
---

# E-A.9 ★ 補題 TRUNC$^{B_4}$ —— **(TRUNC$^{B_4}$) を番号つき補題で塞ぐ**(裁定 399 委嘱・erratum 追記)

**位置づけ**: 上記 §E-A.2.2 で「★ 暗黙の前件」として顕在化させた **(TRUNC$^{B_4}$)** を、番号つき補題として証明する。**erratum 方式** — §E-A.0〜E-A.8 は 1 バイトも改変せず、置換関係は §E-A.9.7 の表に書く。
**起草**: 数学者(Opus 5)/ 2026-08-01。**委嘱** = 裁定 399。**Sol 未監査。**
**正典**: arXiv **2008.00066** v2(54 頁)。**本節の頁番号はすべて起草者が `pdftotext -f p -l p` で頁指定抽出して確認した**(§E-A.8.5-6③ の懸念は解消 — `papers/txt/` の再生成は不要であった。**erratum-6**)。
**封印遵守**: $K^{(5)}$ 非接触。

---

## E-A.9.0 一枚(結論を先に)

| 問い | 結果 |
|---|---|
| (TRUNC$^{B_4}$) は証明できるか | ★ **できる**(§E-A.9.4)。$\mathrm{res}:\mathrm{Aut}(\widehat{\mathrm{PaB}})\to\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})$ は**群同型** |
| 何が効いているか | ★ **生成元が arity $\le3$・全関係式が arity $\le4$** に住むという**表示論法**。正典 **Theorem A.1** (p.48) が untruncated 版の表示、**p.12–13 の地の文**が **truncated 版の表示**を明記している(★ 起草者はこの 2 本目を §E-A.2.2 執筆時に見落としていた) |
| 単射半分 | **(TOPGEN)** p.3 の逐語がほぼそのまま。**易** |
| 全射半分 | **Theorem A.1 の表示 ⟹ 離散射 $\Phi:\mathrm{PaB}\to\widehat{\mathrm{PaB}}$ ⟹ 連続延長**の 3 段。**本節の実質** |
| ★ Thm 3.8 の証明のどの行がどちらの Aut に住むか | **単射性の段(p.37–38)= 切詰め上でしか id を示していない**(単射半分を要する)/ **全射性の段 (3.22)(p.38)= $\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})$ の元しか作っていない**(全射半分を要する)。§E-A.9.5 に逐行表 |
| ★★ **第 2 の暗黙段はあったか** | ★ **あったが正典が既に塞いでいた** — $\widehat{\mathrm{PaB}}^{\le4}\cong\widetilde{\mathrm{PaB}}^{\le4}(=\varprojlim_{K\,\rm isolated})$ は **Corollary 3.10 (p.35–36)・証明本文あり**。⟹ **§E-A.2.2 の「暗黙の同定が 1 つある」は正しかった**(1 つで尽きていた) |
| ★★ **前件表から (TRUNC$^{B_4}$) を除去できるか** | ★ **できる**(§E-A.9.6)。**FAKE-KILL$^{B_4}$ の前件は (IH-S)/(GEN$^{B_4}$)/(PR$^{B_4}$)/(CHM$^{B_4}$) の 4 つだけ**になる。理由は二重(①もともと荷重を担っていなかった ②本節で証明された) |
| 残る穴 | **2 本**(§E-A.9.7)。いずれも「未証明の同定」ではなく**外部文献への依存**へ移った: 【GAP-TRUNC-1】表示の普遍性の圏論的包装・【GAP-TRUNC-2】**Theorem A.1 自身に 2008 は証明本文をもたない**(外部引用 [9, Thm 6.2.4] $=$ Fresse) |

> ★ **一行で**: (TRUNC$^{B_4}$) は**塞がった**。ただし塞ぎ方は「工房の自前証明が Theorem A.1 に載る」形であり、**Theorem A.1 は 2008 では証明本文をもたない外部引用**である。⟹ 依存は「**記述の穴 ⟶ 確立した外部定理**」へ移った。これは正しい方向の移動だが、**「前件が消えた」ではなく「前件の格が上がった」と書く**。

---

## E-A.9.1 規約 —— 委嘱の注意点 ①「整合」の正確な定義

### 規約 (OBJ) — **対象上恒等**

本節を通じ、$\mathrm{Aut}(-)$ は「**対象上恒等な連続自己同型**」を意味する。正典の根拠は p.3 **脚注 2**:

> "*We tacitly assume that our automorphisms act as identity on objects.*"

これは「our automorphisms」という一般形なので**全編にかかる**読みが自然であり、実際 **Prop 2.18** (p.25) は同じ語法で $\widehat{\mathrm{PaB}}^{\le4}$ 側の自己同型を扱う。⟹ **両辺に同じ規約を課す**。

> ⚠ **この規約は無害ではない**(委嘱への回答の一部): $\mathrm{PaB}$ の**対象の operad** $\Omega$($\Omega(n)=$ 各記号がちょうど 1 回現れる自由マグマの語)は、**arity 2 の自由 $S_2$-集合 1 個の上の自由 operad** である($|\Omega(n)|=\mathrm{Cat}(n-1)\cdot n!$; $n=2,3$ で $2,12$ — 正典 p.3 の「$\mathrm{PaB}(3)$ は 12 個の対象」と一致)。
> **検算(機械)**: 括弧つき語を直接列挙し $n=1..5$ で $|\Omega(n)|=1,2,12,120,1680=\mathrm{Cat}(n-1)\cdot n!$ を確認(scratchpad `omega_count.py`・起草者実行)。$n=3$ の $12$ が正典 p.3 の逐語と一致することが自由性の傍証。ゆえに $\mathrm{Aut}_{\rm operad}(\Omega)\cong S_2$(生成元 $(12)\mapsto(21)$ の反転)であり、**対象上の非自明な自己同型は原理的に存在しうる**。両辺で規約を揃えないと補題は形を変える。
> **規約を落とした場合の可否は本節の射程外(UNKNOWN)。**

### 規約 (TR) — **切詰め operad と「整合」**

正典 p.7 **(1.9)** の定義(逐語): $q$-truncated operad in groupoids $=$ 次を満たす groupoid の族 $\{G(n)\}_{1\le n\le q}$:
- 各 $1\le n\le q$ で $G(n)$ に $S_n$ 作用;
- $1\le i\le n$ かつ $n,m,n+m-1\le q$ なる**すべての** $(i,n,m)$ に対し関手 $\circ_i:G(n)\times G(m)\to G(n+m-1)$;
- **arity がすべて $\le q$ の場合の** operad 公理(§1.4 p.7: 結合律は "on the nose")。

⟹ **$\widehat{\mathrm{PaB}}^{\le4}$ の「整合する自己同型」の定義(5 条件)**:

| # | 条件 |
|---|---|
| (i) | 各 arity $n\le4$ で $\widehat{\mathrm{PaB}}(n)$ の**関手**(合成と**恒等射**を保つ) |
| (ii) | $S_n$ 同変($n\le4$) |
| (iii) | $n,m,n+m-1\le4$ なる**全**組で $\circ_i$ と可換 |
| (iv) | **対象上恒等**(規約 (OBJ)) |
| (v) | **連続** |

> ### ★ 切詰めが忘れるもの / 忘れないもの(**これが補題の全内容**)
> | | 中身 |
> |---|---|
> | **忘れる** | arity $\ge5$ の射・$n+m-1\ge5$ となる挿入(例 $\circ_i:G(3)\times G(3)\to G(5)$) |
> | **忘れない** | $\beta\in\mathrm{PaB}(2)$・$\alpha\in\mathrm{PaB}(3)$(**生成元**)/ pentagon **(2.13)** $\in$ arity 4 / hexagon **(2.14)(2.15)** $\in$ arity 3 / それらを組む挿入 $(3,2)\to4$, $(2,3)\to4$, $(2,2)\to3$ |
>
> **生成元も全関係式も切詰めの中に住む** — これが (TRUNC$^{B_4}$) が成り立つ理由のすべてである。

---

## E-A.9.2 pin 表(★ **裁定 399 採択の「証明本文の有無」欄つき**)

**出所**: すべて起草者が `pdftotext -f p -l p` で頁指定抽出して原文照合(2026-08-01)。

| 札 | 逐語 / 内容 | 頁 | ★ **証明本文** |
|---|---|---|---|
| **(GT-DEF)** | "*By definition, $\widehat{GT}$ is the group $\mathrm{Aut}(\widehat{\mathrm{PaB}})$ of (continuous) automorphisms$^2$ of the profinite completion $\widehat{\mathrm{PaB}}$ of $\mathrm{PaB}$.*" $+$ **脚注 2** "*We tacitly assume that our automorphisms act as identity on objects.*" | p.3 | **定義**(該当なし) |
| **(TOPGEN)** | "*Since the morphisms $\beta$ and $\alpha$ from (1.2) are topological generators of $\widehat{\mathrm{PaB}}$, every $\hat T\in\widehat{GT}$ is uniquely determined by its values $\hat T(\beta)\in\mathrm{Hom}_{\widehat{\mathrm{PaB}}}((1,2),(2,1))$, $\hat T(\alpha)\in\mathrm{Hom}_{\widehat{\mathrm{PaB}}}((1,2)3,1(2,3))$.*" **(1.3)** | p.3 | ★ **なし**(地の文の宣言) |
| **(A1)** **Theorem A.1** | "*As the operad in the category of groupoids, $\mathrm{PaB}$ is generated by morphisms $\alpha$ and $\beta$ shown in figure A.3. Moreover, any relation on $\alpha$ and $\beta$ in $\mathrm{PaB}$ is a consequence of (A.13), (A.14) and (A.15).*" | p.48 | ★★ **なし — 外部引用**。直前の地の文 "*It is known [9, Theorem 6.2.4] that$^{13}$*"、**脚注 13** "*A very similar statement is proved in [1]. See Claim 2.6 in loc. cit. … Theorem A.1 can be thought of as a version of MacLane's coherence theorem for braided monoidal categories.*" |
| **(A1$^{\le4}$)** ★★ | "*Since the groupoid $\mathrm{PaB}(0)$ is empty, **Theorem A.1 implies that the truncated operad $\mathrm{PaB}^{\le4}$ is generated by morphisms $\alpha$ and $\beta$** shown in figure 2.1.*" $+$ "*Moreover **any relation on $\alpha$ and $\beta$ in $\mathrm{PaB}^{\le4}$ is a consequence of the pentagon relation** (2.13) **and the hexagon relations** (2.14),(2.15)*" | **p.12–13** | ★ **なし**(Thm A.1 からの 1 行演繹・地の文)。**しかし言明は明示的に切詰め版である** |
| **(TROP)** | $q$-truncated operad の定義 **(1.9)**;"*For every operad $\mathcal O$ and every integer $q\ge1$, the disjoint union $\mathcal O^{\le q}$ is clearly a $q$-truncated operad.*" | p.7 | **定義** |
| **(CPL)** | **A.5**: 連結・対象有限・$\mathrm{Aut}(a)$ 剰余有限な groupoid $G$ に対し compatible equivalence relation(3 条件)の**有向 poset** 上の極限として $\widehat G$ を定義。"*the quotient $G/\!\sim$ is naturally a finite groupoid (**with the same set of objects**)*";"*compatible equivalence relations on $G$ are in bijection with finite index normal subgroups $N$ of $G$*";★ "*Thus "putting hats" over $\mathrm{PaB}(n)$ **for every $n\ge0$** gives us an operad $\widehat{\mathrm{PaB}}$ in the category of topological groupoids.*" | p.49 | **一部なし**(双射・関手性・対称モノイダル性は **[5] へ外部引用**) |
| **(DENSE)** | "*Since $I(\mathrm{PaB}^{\le4})$ is dense in $\widehat{\mathrm{PaB}}^{\le4}$ …*"(p.17)/ "*Since the image $I(\mathrm{PaB}^{\le4})$ of $\mathrm{PaB}^{\le4}$ in $\widetilde{\mathrm{PaB}}^{\le4}$ is dense … and the target … is Hausdorff*"(p.36) | p.17, 36 | **使用のみ**(自明) |
| **(RMK13)** | **Remark 1.3**: "*It is not hard to show that $\widehat{GT}_0$ is the group of continuous automorphisms of the truncated operad $\widehat{\mathrm{PaB}}^{\le3}$ and $\widehat{GT}$ is a subgroup of $\widehat{GT}_0$.*" | p.5 | ★ **なし**("It is not hard to show") |
| **(COR310)** ★★ | **Corollary 3.10**: 標準射 $\Lambda:\widehat{\mathrm{PaB}}^{\le4}\to\widetilde{\mathrm{PaB}}^{\le4}$($\widetilde{\mathrm{PaB}}^{\le4}:=\varprojlim_{K\in\mathrm{NFI}^{\rm isolated}_{PB_4}(B_4)}\mathrm{PaB}^{\le4}/\!\sim_K$、定義 (3.13)(3.14))は**位相 groupoid における切詰め operad の同型** | p.35–36 | ★ **あり**(単射・全射・連続性を Prop 3.9 経由で;直後 "*we can safely replace $\widehat{\mathrm{PaB}}^{\le4}$ by $\widetilde{\mathrm{PaB}}^{\le4}$*") |
| **(PROP39)** | **Prop 3.9** A) $\forall N\in\mathrm{NFI}(PB_3)\ \exists K$ isolated: $K_{PB_3}\le N$;B) 同 $PB_2$ | p.33–34 | ★ **あり** |

> ### ★ 規約提案の増強(§E-A.8.5-3 の補強)
> **(A1) は「証明本文なし」の 5 例目**だが、**種が違う** — 1〜4 例目は**読者演習/分岐の書き落とし**(同著者が自分で埋める気だった)であるのに対し、(A1) は **他書への引用**([9, Thm 6.2.4] $=$ Fresse)である。
> ⟹ **「証明本文の有無」欄は 2 値でなく 3 値にすべき**: **あり / 読者演習(著者が省略) / 外部引用(他書)**。後 2 者はリスクの型が違う(前者は工房が埋められる・後者は文献入手が要る)。

---

## E-A.9.3 補題の言明

> ### 補題 TRUNC$^{B_4}$
> 規約 **(OBJ)**・**(TR)** の下で、arity $\le4$ への制限写像
> $$\mathrm{res}:\ \mathrm{Aut}(\widehat{\mathrm{PaB}})\longrightarrow\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4}),\qquad \mathrm{res}(\hat T):=\bigl(\hat T|_{\widehat{\mathrm{PaB}}(n)}\bigr)_{1\le n\le4}$$
> は**群同型**である。逆写像は
> $$\mathrm{res}^{-1}(\hat U)\ =\ \bigl(\alpha\mapsto\hat U(\alpha),\ \beta\mapsto\hat U(\beta)\ \text{で一意に定まる連続自己同型}\bigr).$$
> とくに
> $$\boxed{\ \widehat{GT}\ =\ \mathrm{Aut}(\widehat{\mathrm{PaB}})\ \cong\ \mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})\ }$$
> すなわち **(TRUNC$^{B_4}$) は成り立つ。**

**補助補題 6 本**(証明は §E-A.9.4):

| 札 | 内容 | 難度 |
|---|---|---|
| **(TR-0)** | $\mathrm{res}$ は well-defined な群準同型 | **定義的**(arity 保存) |
| **(TR-1)** | $\widehat{\mathrm{PaB}}$(resp. $\widehat{\mathrm{PaB}}^{\le4}$)の連続 operad 自己射で $\alpha,\beta$ 上一致する 2 つは一致 | **易**((A1)/(A1$^{\le4}$) $+$ (DENSE)) |
| **(TR-2)** | $\hat U\in\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})$ に対し $(\beta',\alpha'):=(\hat U(\beta),\hat U(\alpha))$ は $\widehat{\mathrm{PaB}}$ の中で pentagon $+$ hexagon $\times2$ を満たす | **易**(規約 (TR) の (i)(ii)(iii)(iv)) |
| **(TR-3)** | $\exists!$ 対象上恒等な operad-in-groupoids 射 $\Phi:\mathrm{PaB}\to\widehat{\mathrm{PaB}}$、$\Phi(\beta)=\beta'$, $\Phi(\alpha)=\alpha'$ | ★ **本節の実質**((A1) を**表示**として読む) |
| **(TR-4)** | $\Phi$ は一意な**連続** operad 射 $\widehat\Phi:\widehat{\mathrm{PaB}}\to\widehat{\mathrm{PaB}}$ に延びる | ★ **本節の実質**((CPL) の定義から自前) |
| **(TR-5)** | $\mathrm{res}(\widehat\Phi)=\hat U$ かつ $\widehat\Phi\in\mathrm{Aut}(\widehat{\mathrm{PaB}})$ | **易** |

---

## E-A.9.4 証明

### (TR-0) $\mathrm{res}$ は well-defined な群準同型

operad の射は arity を保つので、$\hat T\in\mathrm{Aut}(\widehat{\mathrm{PaB}})$ は各 $\widehat{\mathrm{PaB}}(n)$ を保つ。規約 (TR) の (i)(ii)(iii)(v) は $\widehat{\mathrm{PaB}}$ 側の条件を $n\le4$ に制限したものであり、(iv) は規約 (OBJ)。$\mathrm{res}(\hat T)^{-1}=\mathrm{res}(\hat T^{-1})$、$\mathrm{res}(\hat T_1\circ\hat T_2)=\mathrm{res}(\hat T_1)\circ\mathrm{res}(\hat T_2)$。$\blacksquare$

> ### ★ (TR-0) の正典での使われ方(**前件会計に効く**)
> 正典 **(2.31)** (p.16) は $T_N:=\widehat P_N\circ\hat T\circ I$ と書くが、$\widehat P_N:\widehat{\mathrm{PaB}}^{\le4}\to\mathrm{PaB}^{\le4}/\!\sim_N$ **(2.30)** かつ $I:\mathrm{PaB}^{\le4}\to\widehat{\mathrm{PaB}}^{\le4}$ **(2.32)** であるのに対し、$\hat T$ は**非切断**の $\widehat{\mathrm{PaB}}$ の自己同型である。この合成が意味をもつのは **(TR-0)** による。
> ⟹ **(PR$^{B_4}$) は (TR-0) を暗黙に使っている。しかし (TR-0) は定義的(arity 保存)なので前件を増やさない。**(Remark 1.1 p.3 が Prop 2.18($\widehat{\mathrm{PaB}}^{\le4}$ の自己同型についての命題)を $\hat T\in\mathrm{Aut}(\widehat{\mathrm{PaB}})$ に適用しているのも同じ (TR-0) の使用である。)

### (TR-1) 一意性

$A,B$ を $\widehat{\mathrm{PaB}}$ の連続 operad 自己射(対象上恒等)で $A(\alpha)=B(\alpha)$, $A(\beta)=B(\beta)$ とする。
$$E:=\{\gamma\in\widehat{\mathrm{PaB}}\ \mid\ A(\gamma)=B(\gamma)\}.$$
- $E$ は**部分 operad**: 合成・逆($A,B$ は関手ゆえ逆を保つ)・恒等射・挿入 $\circ_i$・$S_n$ 作用で閉じる。
- $E$ は**各 arity で閉集合**: $A,B$ は連続、$\widehat{\mathrm{PaB}}(n)$ は副有限(有限離散 groupoid の逆極限)ゆえ Hausdorff、2 つの連続写像の等化子は閉。
- $\alpha,\beta\in E$ と **(A1)**(生成)より $E\supseteq\mathrm{PaB}$。
- **(DENSE)** より $\mathrm{PaB}$ は $\widehat{\mathrm{PaB}}$ で稠密(各有限商へ全射ゆえ;正典は $\le4$ で明記、一般 $n$ も同一論法)。$E$ は閉ゆえ $E=\widehat{\mathrm{PaB}}$。$\blacksquare$

$\widehat{\mathrm{PaB}}^{\le4}$ 版も同じ論法(**(A1$^{\le4}$)** を使う)。
> ★ **(TOPGEN)** (p.3) はこの主張の正典側の逐語版である。**すなわち (TRUNC$^{B_4}$) の単射半分は、正典が地の文で述べている。**

### (TR-2) 関係式の輸送

$\hat U\in\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})$、$\beta':=\hat U(\beta)\in\widehat{\mathrm{PaB}}(2)$、$\alpha':=\hat U(\alpha)\in\widehat{\mathrm{PaB}}(3)$。

**pentagon (2.13)**(向きの pin は `docs/notes/reading_2008_x13_c_v1.md` §5;**本論法は向きに依存しない**):
$$(\mathrm{id}_{12}\circ_2\alpha)\cdot(\alpha\circ_2\mathrm{id}_{12})\cdot(\mathrm{id}_{12}\circ_1\alpha)\ =\ (\alpha\circ_3\mathrm{id}_{12})\cdot(\alpha\circ_1\mathrm{id}_{12})\qquad\text{in }\widehat{\mathrm{PaB}}(4).$$
両辺に $\hat U$ を施す。使うのは:
- **(i)** $\hat U(\gamma\cdot\delta)=\hat U(\gamma)\cdot\hat U(\delta)$、および $\hat U(\mathrm{id}_{12})=\mathrm{id}_{\hat U_{\rm obj}((12))}=\mathrm{id}_{(12)}$ — ★ **ここで (iv) 対象上恒等を使う**(規約 (OBJ) が効く唯一の箇所);
- **(iii)** $\hat U(\gamma\circ_i\delta)=\hat U(\gamma)\circ_i\hat U(\delta)$ — 使う組は $(n,m)=(3,2)$ と $(2,3)$ でいずれも $n+m-1=4\le4$ ゆえ**切詰めに残っている**。

⟹ $\alpha$ を $\alpha'$ に置換した同じ等式が $\widehat{\mathrm{PaB}}(4)$ で成り立つ。
**hexagon (2.14)(2.15)** は arity 3 の等式で、$\beta\circ_1\mathrm{id}_{12}$($2+2-1=3\le4$)・$\theta(\alpha)$($\theta\in S_3$)・$\mathrm{id}_{12}\circ_i\beta$ を含むが、いずれも切詰めに残っており、**(ii)** $S_3$ 同変性から $\hat U(\theta(\gamma))=\theta(\hat U(\gamma))$。⟹ 同様に $(\beta',\alpha')$ で成り立つ。$\blacksquare$

### (TR-3) 表示 $\Rightarrow$ 離散射

**(A1) を表示として読む。** 対象の operad $\Omega$(§E-A.9.1)を固定し、$\Omega$ 上の operad-in-groupoids(射は対象上恒等)の圏で、
$$\beta\in F(2)\bigl((12),(21)\bigr),\qquad \alpha\in F(3)\bigl(((12)3),(1(23))\bigr)$$
を生成射とする**自由対象** $F$ をとり、**(A.13)(A.14)(A.15)** が生成する operad 合同 $R$ で割った $F/R$ を作る。標準射 $F/R\to\mathrm{PaB}$ について:
- **(A1) 前半(生成)** $\iff$ 全射;
- **(A1) 後半**("*any relation on $\alpha$ and $\beta$ in $\mathrm{PaB}$ is a consequence of (A.13),(A.14),(A.15)*")$\iff$ 単射。

$\Rightarrow F/R\cong\mathrm{PaB}$。ゆえに $\mathrm{PaB}$ は次の普遍性をもつ:

> **(UP)** 対象 operad が $\Omega$ である任意の operad-in-groupoids $Q$ と、**(A.13)(A.14)(A.15) を満たす**任意の対
> $$(b,a)\in Q(2)\bigl((12),(21)\bigr)\times Q(3)\bigl(((12)3),(1(23))\bigr)$$
> に対し、対象上恒等な operad 射 $\Phi:\mathrm{PaB}\to Q$ で $\Phi(\beta)=b$, $\Phi(\alpha)=a$ なるものが**ただ一つ**存在する。

$Q:=\widehat{\mathrm{PaB}}$(対象集合は $\mathrm{PaB}$ と同じ — **(CPL)** の "*with the same set of objects*")、$(b,a):=(\beta',\alpha')$(**(TR-2)** で関係式を確認済)を代入して主張を得る。$\blacksquare$

> ### ★ ここが要点(**離散の表示で足りる理由**)
> **表示は離散の $\mathrm{PaB}$ のものでよい。標的が副有限であることは邪魔にならない** — 必要なのは「$\beta',\alpha'$ が**標的の中で**関係式を満たす」ことだけであり、それは (TR-2) で確認済だからである。**副有限版の表示定理は要らない。**

> ### 【前提 (FREE-OP)】(⟹ §E-A.9.7 の【GAP-TRUNC-1】)
> 「$\Omega$ 上の operad-in-groupoids の自由対象 $F$ の存在」と「operad 合同による商」。2008 は p.7 で "*We will freely use the language of operads [6, Section 3], [9, Chapter 1], [21], [22], [27]*" と述べるのみで、この構成を明示しない。**標準的な圏論的事実だが正典に逐語がない。**

### (TR-4) 連続延長

各 $n\ge1$ を固定。$\mathrm{PaB}(n)$ は連結・対象有限・$\mathrm{Aut}(\tau)=PB_n$ 剰余有限ゆえ **(CPL)** の枠内。$\Phi_n:\mathrm{PaB}(n)\to\widehat{\mathrm{PaB}}(n)$ は対象上恒等な関手。

**段 1(有限商への降下).** $\mathrm{PaB}(n)$ 上の compatible equivalence relation $\sim$ を任意にとり、標準射影を $q_\sim:\widehat{\mathrm{PaB}}(n)\to\mathrm{PaB}(n)/\!\sim$ とする。合成
$$\psi_\sim:=q_\sim\circ\Phi_n:\ \mathrm{PaB}(n)\longrightarrow\mathrm{PaB}(n)/\!\sim$$
は**有限 groupoid への対象上恒等な関手**。その「核」
$$\gamma_1\sim'\gamma_2\ :\Longleftrightarrow\ \psi_\sim(\gamma_1)=\psi_\sim(\gamma_2)$$
は **(CPL)** の 3 条件を満たす: ① source/target 保存($\psi_\sim$ は対象上恒等な関手)② 合成両側との整合($\psi_\sim$ は関手)③ **有限**($\mathrm{PaB}(n)/\!\sim'$ は射の集合として $\mathrm{PaB}(n)/\!\sim$ に単射に入る)。
⟹ $\sim'$ は $\widehat{\mathrm{PaB}}(n)$ の添字であり、$\psi_\sim$ は $\mathrm{PaB}(n)\to\mathrm{PaB}(n)/\!\sim'\xrightarrow{\ \bar\psi_\sim\ }\mathrm{PaB}(n)/\!\sim$ と分解する。**連続関手** $(\widehat\Phi_n)_\sim:=\bar\psi_\sim\circ\mathrm{pr}_{\sim'}:\widehat{\mathrm{PaB}}(n)\to\mathrm{PaB}(n)/\!\sim$ を得る。

**段 2(錐の整合と極限).** $\sim_1\le\sim_2$ のとき $P_{\sim_1,\sim_2}\circ(\widehat\Phi_n)_{\sim_1}=(\widehat\Phi_n)_{\sim_2}$: 両辺を $\iota_n:\mathrm{PaB}(n)\hookrightarrow\widehat{\mathrm{PaB}}(n)$ と合成すると共に $q_{\sim_2}\circ\Phi_n$ に等しく、両辺は連続・標的は有限離散(Hausdorff)・$\iota_n$ の像は稠密ゆえ一致。⟹ 錐は整合し、$\widehat{\mathrm{PaB}}(n)=\varprojlim_\sim\mathrm{PaB}(n)/\!\sim$ の普遍性から連続関手
$$\widehat\Phi_n:\widehat{\mathrm{PaB}}(n)\to\widehat{\mathrm{PaB}}(n),\qquad \widehat\Phi_n\circ\iota_n=\Phi_n$$
を得る(関手性は有限関手の極限として自動)。

**段 3(operad 構造との整合).** 各 $\circ_i$ について、2 つの連続写像
$$\widehat\Phi\circ\circ_i,\qquad \circ_i\circ(\widehat\Phi\times\widehat\Phi)\ :\ \widehat{\mathrm{PaB}}(n)\times\widehat{\mathrm{PaB}}(m)\to\widehat{\mathrm{PaB}}(n+m-1)$$
は稠密部分集合 $\iota(\mathrm{PaB}(n))\times\iota(\mathrm{PaB}(m))$ 上で一致し($\Phi$ が operad 射)、標的は Hausdorff ゆえ一致。$S_n$ 作用も同様。⟹ $\widehat\Phi$ は連続 operad 射。一意性も稠密性 $+$ Hausdorff。$\blacksquare$

> ### ★ 委嘱の注意点 ②(**副有限完備化と切詰めの可換性**)への回答
> $$\boxed{\ \textbf{可換性は「順序交換」の問題ですらない — 完備化が }\textbf{arity ごと}\textbf{に定義されているから。}\ }$$
> **(CPL)** (p.49) の逐語: "*Thus "putting hats" over $\mathrm{PaB}(n)$ **for every $n\ge0$** gives us an operad $\widehat{\mathrm{PaB}}$*"。完備化の極限は**各 arity の groupoid 上の compatible equivalence relation の poset**上でとられており、$\mathrm{NFI}_{PB_4}(B_4)$ とは無関係である。ゆえに
> $$(\widehat{\mathrm{PaB}})^{\le4}=\widehat{\mathrm{PaB}}(1)\sqcup\cdots\sqcup\widehat{\mathrm{PaB}}(4)=\widehat{(\mathrm{PaB}^{\le4})}$$
> は**構成上の恒等式**であり、有限性の議論すら不要。⟹ **懸念 ② は空振り(良い意味で)。**
>
> ⚠ **ただし紛らわしい別物が 1 つある**: Thm 3.8 の証明が使う $\widetilde{\mathrm{PaB}}^{\le4}:=\varprojlim_{K\in\mathrm{NFI}^{\rm isolated}_{PB_4}(B_4)}\mathrm{PaB}^{\le4}/\!\sim_K$ **(3.13)** は、**添字が $\mathrm{NFI}^{\rm isolated}$ に絞られた別の極限**である。$\widehat{\mathrm{PaB}}^{\le4}\cong\widetilde{\mathrm{PaB}}^{\le4}$ は**共終性を要する非自明な主張**だが、★ **正典 Corollary 3.10 (p.35–36) に証明本文がある**(§E-A.9.5)。

### (TR-5) 復元と可逆性

$\mathrm{res}(\widehat\Phi)$ と $\hat U$ はともに $\widehat{\mathrm{PaB}}^{\le4}$ の連続 operad 自己射で $\alpha,\beta$ 上一致 ⟹ **(TR-1)** の切詰め版より一致。
可逆性: $\hat U^{-1}\in\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})$ に (TR-2)–(TR-4) を適用して $\widehat\Psi$ を得る。$\widehat\Psi\circ\widehat\Phi$ は $\widehat{\mathrm{PaB}}$ の連続 operad 自己射で
$$\mathrm{res}(\widehat\Psi\circ\widehat\Phi)=\mathrm{res}(\widehat\Psi)\circ\mathrm{res}(\widehat\Phi)=\hat U^{-1}\circ\hat U=\mathrm{id},$$
とくに $\alpha,\beta$ を固定するので **(TR-1)** より $\widehat\Psi\circ\widehat\Phi=\mathrm{id}_{\widehat{\mathrm{PaB}}}$。同様に $\widehat\Phi\circ\widehat\Psi=\mathrm{id}$。⟹ $\widehat\Phi\in\mathrm{Aut}(\widehat{\mathrm{PaB}})$ かつ $\mathrm{res}(\widehat\Phi)=\hat U$。$\blacksquare$

**(TR-0)–(TR-5) を合わせて補題 TRUNC$^{B_4}$ が従う。** $\blacksquare$

### ★ 系 TRUNC-PAIR(**Drinfeld 的対記述が定理になる**)

> $\widehat{GT}=\mathrm{Aut}(\widehat{\mathrm{PaB}})$ は、**pentagon (2.20) と hexagon (2.18)(2.19) の副有限版を満たす対 $(\hat m,\hat f)\in\widehat{\mathbb Z}\times\widehat{PB_3}$** の集合に単射に写り、像は「可逆なもの」全体に一致する。
> **証明骨子**: 単射性 $=$ (TR-1);対 $\mapsto$ 自己射は **(A1$^{\le4}$)**(切詰め版の表示)$+$ (TR-4) の完備化論法;可逆性の条件は (TR-5) と同じ議論。$\square$

⚠ **格の申告**: 正典 p.3 は "*the underlying set of $\widehat{GT}$ can be identified with the subset of pairs $(\hat m,\hat f)$ satisfying **some relations and technical conditions***" と書き、Remark 1.1 は "*the "invertibility condition"*" と呼ぶだけで**明示していない**。⟹ **本系の「可逆性条件」の明示形は本節の射程外(UNKNOWN)**。系は「関係式を満たす対 $\Rightarrow$ 連続**自己準同型**」までを主張し、自己**同型**であることは別途要る、という形で使うこと。

---

## E-A.9.5 ★ Thm 3.8 の証明との逐行突合(**委嘱の注意点 ③**)

**「証明のどの行がどちらの Aut に住むか」の全表**(頁は起草者が頁指定抽出で確認):

| 段 | 頁 | 逐語の要点 | **どちらの Aut に住むか** | **(TRUNC) のどの半分を使うか** |
|---|---|---|---|---|
| **(3.19) の定義** $\hat T\mapsto\{T_K\}$ | p.36 | $T_K=\widehat P_K\circ\hat T\circ I$ | 源は $\mathrm{Aut}(\widehat{\mathrm{PaB}})$(定義どおり)・合成は切詰め上 | **(TR-0)** のみ(**定義的**) |
| **群準同型性 (3.20)** | p.37 | $\widehat P_K\circ\hat T=T_K^{\rm isom}\circ\widehat P_K$ の操作 | 切詰め上の等式 | **(TR-0)** のみ |
| ★ **単射性の段** | p.37–38 | "*we conclude that $\hat T$ is the identity map $\mathrm{id}:\widehat{\mathrm{PaB}}^{\le4}\to\widehat{\mathrm{PaB}}^{\le4}$. **Thus the injectivity of (3.19) is established.***" | ★ **結論は切詰め上でしか id を言っていない**(稠密性 $+$ Hausdorff の議論は $I(\mathrm{PaB}^{\le4})$ 上) | ★★ **(TRUNC) の単射半分**($=$ **(TR-1)**)。これが無いと (3.19) の単射性は「$\mathrm{res}(\hat T)=\mathrm{id}$」までしか言えない |
| ★ **全射性の段 (3.22)** | p.38 | "*the formula $\hat T(\gamma)(K):=T_K^{\rm isom}(\gamma(K))$ **defines a morphism of truncated operads in groupoids** $\hat T:\widetilde{\mathrm{PaB}}^{\le4}\to\widetilde{\mathrm{PaB}}^{\le4}$*" $+$ 連続性 $+$ 逆射の構成 $+$ "*The proof of surjectivity of (3.19) is complete.*" | ★ **構成物は $\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})$ の元**(Cor 3.10 で $\widetilde{}\cong\widehat{}$)。$\mathrm{Aut}(\widehat{\mathrm{PaB}})$ の元は**一度も作られていない** | ★★ **(TRUNC) の全射半分**($=$ **(TR-2)–(TR-5)**)。これが無いと (3.19) の全射性は成立しない |
| $\widehat{\mathrm{PaB}}^{\le4}\cong\widetilde{\mathrm{PaB}}^{\le4}$ | p.35–36 | **Corollary 3.10** | — | ★ **(TRUNC) とは別件・証明本文あり ⟹ 穴ではない** |

$$\boxed{\ \textbf{Thm 3.8 の証明は、単射性・全射性の}\textbf{両方}\textbf{で (TRUNC}^{B_4}\textbf{) を暗黙に使っている。}\ }$$

> ### ★ §E-A.2.2 の主張の検収(**自己監査**)
> §E-A.2.2 は「Thm 3.8 の証明が実際に構成しているのは $\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})$ の元である」と書いた。**この観察は正しい**(上表の全射性の段)。**さらに単射性の段も同じ穴に落ちている**ことが本節で判明した(§E-A.2.2 は全射性の段しか挙げていなかった)。⟹ **erratum-1**(§E-A.9.7)。

> ### ★ 副次観察(**正典の引用の綻び・数学の穴ではない**)
> **Cor 3.10 の証明**(p.36)は "*due to **Proposition 3.9**, the image of $\hat\gamma_2^{-1}\cdot\hat\gamma_1$ in $PB_n/N$ is the identity element for every $N\in\mathrm{NFI}(PB_n)$*" と書くが、**Prop 3.9 は A) $PB_3$・B) $PB_2$ の 2 本しかない**(p.33–34)。$n=4$ の場合は引用されていない。
> **2 行で埋まる**: $M\in\mathrm{NFI}(PB_4)$ に対し $B_4$ における正規核 $M_0:=\bigcap_{b\in B_4}bMb^{-1}$ をとる。$[B_4:PB_4]=4!<\infty$ かつ $[PB_4:M]<\infty$ ゆえ $[B_4:M]<\infty$、有限指数部分群の正規核は有限指数で $B_4$ 正規、$M_0\le M\le PB_4$。⟹ $M_0\in\mathrm{NFI}_{PB_4}(B_4)$。**(COF$^{B_4}$) Cor 3.5** より isolated $K\le M_0\le M$。∎
> ⟹ **引用の綻びであって穴ではない。**(参考: 同種の $n=4$ 補完は **Prop 2.5**(p.12)にも要る — こちらは "*Stronger versions … are proved in Subsection 3.1*" とだけ書かれている。)

---

## E-A.9.6 ★★ 前件表の更新(**委嘱の判定**)

### 判定

$$\boxed{\ \textbf{(TRUNC}^{B_4}\textbf{) は前件表から除去できる。FAKE-KILL}^{B_4}\textbf{ の前件は 4 つになる。}\ }$$

**理由は二重で、格が違う** — 混ぜないこと:

| # | 理由 | 効き方 |
|---|---|---|
| **(a)** | ★ **もともと FAKE-KILL$^{B_4}$ の荷重を担っていなかった** | 最短鎖 **(B0)–(B4)**(§E-A.4.2)は (TRUNC) を使わない。(PR$^{B_4}$) が使うのは **(TR-0)**(arity 保存 $=$ 定義的)だけ。⟹ §E-A.4.2 の「落とすと壊れるもの」欄が既に "*FAKE-KILL$^{B_4}$ 本体は無傷*" と書いていたのは**正しかった**。表に**行があったこと自体**が、周辺結果((LIM$^{B_4}$)/SURV$^{B_4}$)の前件との混載だった |
| **(b)** | ★ **本節で証明された** | 格が「★ **暗黙の前件**(番号つき補題なし)」から「**工房の証明つき補題**(Sol 未監査)」へ移る。⟹ **SURV$^{B_4}$ / (LIM$^{B_4}$) 側の依存も「未証明の同定」ではなくなる** |

### ★ 更新後の前件表(**FAKE-KILL$^{B_4}$**)

| 札 | 言明 | 格 | 出所 | 落とすと壊れるもの |
|---|---|---|---|---|
| **(IH-S)** | $\mathrm{Ih}:G_{\mathbb Q}\twoheadrightarrow\widehat{GT}$ | ★ **UNKNOWN**(P6) | 2008 (1.1) p.2 | 前提そのもの |
| **(GEN$^{B_4}$)** | genuine $=$ $\widehat{GT}$ の元からの射影 | **正典の定義** | Def 2.19 p.25 / (1.7) p.5 | (B2) が消える |
| **(PR$^{B_4}$)** | $T_N:=\widehat P_N\circ\hat T\circ I$ が GT-shadow | **正典の定義+命題** | (2.31) p.16 | (B1) が消える |
| **(CHM$^{B_4}$)** | genuine $\Rightarrow$ charming | **正典の定理** | Prop 2.20 p.26 | 四層 (1.A$^{B_4}$) の第 2 包含が消える(格下げであって破綻ではない) |

**以上 4 つで閉じる。**

### ★ 除外欄への追加(**(TRUNC$^{B_4}$) の移動先**)

| 除外するもの | 理由 |
|---|---|
| ★ **(TRUNC$^{B_4}$)** | ① **FAKE-KILL$^{B_4}$ の最短鎖では使わない**(使うのは定義的な (TR-0) のみ)② **補題 TRUNC$^{B_4}$(§E-A.9)で証明済**(工房の自前証明・Sol 未監査・**Theorem A.1 に相対的**)。⟹ 前件ではなく**補題**として §E-A.9 に置く |

### ⚠ 会計の正直さ(**「消えた」と書かないこと**)

補題 TRUNC$^{B_4}$ は **(A1) $=$ Theorem A.1 に相対的**であり、**Theorem A.1 は 2008 に証明本文をもたない**(外部引用 [9, Thm 6.2.4] $=$ Fresse・§E-A.9.2)。すなわち:

$$\text{U-10(未解決予想)}\ \longrightarrow\ \text{(TRUNC}^{B_4}\text{)(記述の穴)}\ \longrightarrow\ \text{Theorem A.1(確立した外部定理)}$$

**2 段とも正しい方向の移動**だが、**「前件が完全に消えた」ではなく「前件の格が 2 段上がった」と書く**。§E-A.2.2 の「交換の正直な会計」の続きである。

---

## E-A.9.7 残る穴・格付け・erratum・申し送り

### 残る穴

> ### 【GAP-TRUNC-1】(FREE-OP)— **圏論的包装**
> 「$\Omega$ 上の operad-in-groupoids の**自由対象**の存在」と「**operad 合同**による商」。これが無いと (A1) を **(UP)** の形に読み替える段(TR-3)が浮く。
> **状態**: **標準的な圏論的事実だが正典に逐語がない**。2008 は p.7 で operad の言語を [6],[9],[21],[22],[27] へ丸投げしている。
> **リスク評価**: **低**。(A1) の言明("生成される"$+$"任意の関係は 3 本の帰結")は**表示の定義そのもの**であり、(UP) はその定義的展開である。ただし**工房が自分で確認していない**ので【GAP】として立てる。

> ### 【GAP-TRUNC-2】(A1 の外部性)— **正典に証明本文が無い**
> **Theorem A.1 自体**が 2008 では "*It is known [9, Theorem 6.2.4] that*" の引用であり、証明本文がない(脚注 13 が [1] Claim 2.6 と MacLane coherence に言及するのみ)。**工房は [9](Fresse)を保持していない。**
> **リスク評価**: **低**(braided monoidal category の MacLane coherence として広く知られた定理)。ただし**格の申告**として: 補題 TRUNC$^{B_4}$ は「**正典 $+$ 未入手の外部定理**」に乗る。

> ### 【文献要請 IHNEC-L3】
> **困難**: 補題 TRUNC$^{B_4}$ の (TR-3) が、$\mathrm{PaB}$ の**表示の普遍性**に乗っている。工房は正典 (A1) の言明しか持たず、その原典を持たない。
> **欲しい結果の型**: **Fresse, "Homotopy of Operads and Grothendieck–Teichmüller Groups", Theorem 6.2.4** の**正確な言明**。とくに (i) 「生成される $+$ 関係は 3 本の帰結」の形か、**(ii) 普遍性(universal property)の形で述べられているか**。(ii) なら【GAP-TRUNC-1】も同時に閉じる。
> **代替**: 2008 の脚注 13 が挙げる **[1] の Claim 2.6**("A very similar statement is proved in [1]")でも可。
> **なぜ要るか**: これが降りれば **(TRUNC$^{B_4}$) の格が「工房の自前証明(外部定理に相対的)」から「正典 $+$ 入手済文献の定理」へ**上がり、前件会計が閉じる。**軽い案件**(定理 1 本の言明照合)。

> ### 【穴ではなかったもの(記録)】
> - $\widehat{\mathrm{PaB}}^{\le4}\cong\widetilde{\mathrm{PaB}}^{\le4}$ ⟹ **Cor 3.10・証明本文あり**。
> - 完備化と切詰めの可換性 ⟹ **(CPL) が arity ごとの定義なので恒等式**(§E-A.9.4 の枠)。
> - Cor 3.10 / Prop 2.5 の $n=4$ 引用の綻び ⟹ **正規核 $+$ Cor 3.5 で 2 行**(§E-A.9.5)。

### 格付け

| # | statement | 状態 | 出所 |
|---|---|---|---|
| **TRUNC$^{B_4}$** | $\mathrm{res}:\mathrm{Aut}(\widehat{\mathrm{PaB}})\xrightarrow{\ \sim\ }\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})$ | ★ **paper-proof candidate**(工房の自前証明・**Sol 未監査**・**Theorem A.1(未入手外部定理)に相対的**) | §E-A.9.3–4 |
| **(TR-0)** | $\mathrm{res}$ の well-defined 性 | **定義的**(arity 保存) | §E-A.9.4 |
| **(TR-1)** | 一意性 | **paper-proof**((TOPGEN) の逐語がほぼ同内容) | §E-A.9.4 |
| **TRUNC-PAIR** | 対 $(\hat m,\hat f)$ 記述 | **paper-proof candidate**(可逆性条件の明示形は **UNKNOWN**) | §E-A.9.4 |
| **Thm 3.8 逐行突合表** | 単射性・全射性の**両段**が (TRUNC) を使う | **観察**(原文照合済) | §E-A.9.5 |
| **規約 (OBJ) の必要性** | $\mathrm{Aut}_{\rm operad}(\Omega)\cong S_2$ ゆえ両辺同規約が要る | **観察** | §E-A.9.1 |
| **$n=4$ 引用の綻び** | Cor 3.10 / Prop 2.5 | **観察**(2 行で補完) | §E-A.9.5 |

### erratum(**§E-A.0–E-A.8 への訂正**・本文は不改変)

| # | 対象 | 差替前 | ★ 差替後 |
|---|---|---|---|
| **erratum-1** | §E-A.2.2 の記述(Thm 3.8 のどこで切詰めが出るか) | 「**全射性の段**が $\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le4})$ の元を構成している」 | ★ **単射性の段も同じ**(結論の逐語が $\widehat{\mathrm{PaB}}^{\le4}$ 上の id)。**両段が (TRUNC) を使う**(§E-A.9.5 の逐行表) |
| **erratum-2** | §E-A.2.2 の (TRUNC$^{B_4}$) の格 | 「★ **暗黙の前件**(番号つき補題なし)・**起草者はこの導出を自分で検証していない**」 | ★ **補題 TRUNC$^{B_4}$(§E-A.9)として証明済**。格は **paper-proof candidate**(Sol 未監査・Theorem A.1 に相対的) |
| **erratum-3** | §E-A.2.2 の導出経路の見立て | 「**Theorem A.1** $+$ p.3 の生成元の議論**と目される**」 | ★ **見立ては正しかったが不完全**。実際に効くのは ① **(A1) Thm A.1**(全射半分)② **(TOPGEN)** p.3(単射半分)③ ★ **(A1$^{\le4}$) p.12–13 の切詰め版表示**(§E-A.2.2 執筆時に**見落としていた** — 正典が切詰め版の生成と関係式を明示している)④ **(CPL)** A.5 の arity ごと完備化 |
| **erratum-4** | §E-A.4.2 の前件表 | **(TRUNC$^{B_4}$)** の行あり(5 札) | ★ **行を除外欄へ移す**。前件は **(IH-S)/(GEN$^{B_4}$)/(PR$^{B_4}$)/(CHM$^{B_4}$) の 4 札**(§E-A.9.6) |
| **erratum-5** | §E-A.8.1 の格付け表 | (TRUNC$^{B_4}$)「★ 暗黙の前件・要 pin」 | ★ 「**paper-proof candidate**(§E-A.9)」 |
| **erratum-6** | §E-A.8.5-6③ の申し送り | 「`papers/txt/` の再生成を検討されたい(頁復元不可)」 | ★ **不要**。`pdftotext -f p -l p papers/2008.00066-*.pdf -` で**頁指定抽出が直接できる**(本節の全 pin はこれで照合した)。⟹ **頁引用を伴う $B_4$ 作業に障害はない** |
| **erratum-7** | §E-A.8.4-5 / §E-A.8.5-4 の Sol 監査依頼・reader 発注 | 「(TRUNC$^{B_4}$) を Thm A.1 から導けるか(Sol へ)」「reader へ pin 発注(軽い案件)」 | ★ **本節が代替した**。**reader 発注は不要**(起草者が原文照合済)。**Sol への依頼は「導けるか」から「§E-A.9.4 の証明の監査」へ変更**(§E-A.9.8) |

> **凍結物は不変**: **P-IHN-1〜7**・検算 digest(`edf6181376…d49309`・`f8be65ae…c88820b`)は改訂なし。本節は $B_3$ 側の実測に一切波及しない。

### 新規性の申告(**grep 済**)

**grep 語**: `TRUNC`・`Aut(PaB`・`PaB^{\le4}`・`切詰`・`truncat`・`Theorem A.1`・`表示`・`presentation`・`free operad`・`自由 operad`。
- **工房内既出**: 追補 E-A §E-A.2.2(**前件としての顕在化のみ・証明なし**)/ `provenance/LEDGER.md` L1525(同)。**他になし。**
- **正典内既出**: ★ **(RMK13)** (p.5) が **$\le3$ 版の類似命題**($\widehat{GT}_0=\mathrm{Aut}(\widehat{\mathrm{PaB}}^{\le3})$)を "*It is not hard to show*" と述べる。**$\le4$ 版 $=$ 本補題そのものは述べていない。** **(TOPGEN)** (p.3) が単射半分の実質。**(A1$^{\le4}$)** (p.12–13) が切詰め版の表示。
- **本節が新しく置くもの**: ① **$\le4$ 版の言明化と証明**(とくに全射半分 $=$ 表示から連続延長を作る (TR-3)(TR-4))② **Thm 3.8 の逐行突合表**(**単射性の段も同じ穴**という発見)③ **規約 (OBJ) の必要性の指摘**($\mathrm{Aut}_{\rm operad}(\Omega)\cong S_2$)④ **前件表の 4 札化**⑤ **「証明本文の有無」欄の 3 値化提案**(あり/読者演習/**外部引用**)。
- ★ **「初」とは書かない。** 本補題は **Fresse/Drinfeld 以来の標準論法の書き下し**であり、正典自身が $\le3$ 版を "not hard to show" と扱っている。**新定理ではなく、前件会計を閉じるための番号つけである。**

### Sol 監査の依頼(優先順位つき・§E-A.8.4 を差し替える)

1. ★★ **(TR-3) の表示の読み**(最優先)— Theorem A.1 の言明を **(UP)**(普遍性)として読んでよいか。**Sol が Fresse [9, Thm 6.2.4] の原文を持っているなら、その言明の形を教えてほしい**(【文献要請 IHNEC-L3】)。ここが崩れると全射半分が消える。
2. ★ **(TR-4) の完備化論法** — 段 1 の「$\psi_\sim$ の核 $\sim'$ が compatible equivalence relation になる」の 3 条件確認、および段 3 の稠密性 $+$ Hausdorff による operad 整合性の議論。
3. **(TR-2) の関係式輸送** — とくに $\hat U(\mathrm{id}_{12})=\mathrm{id}_{(12)}$ に規約 (OBJ) を使う点。**規約 (OBJ) を落とすと何が起きるか**(本節は UNKNOWN と申告)。
4. **§E-A.9.5 の逐行突合表** — 「Thm 3.8 の**単射性の段も** (TRUNC) を使う」という読みに異論はないか。
5. **系 TRUNC-PAIR の可逆性条件** — 正典が "technical conditions" / "invertibility condition" としか書かない部分の明示形を Sol が知っているか。

### 申し送り(司令塔へ)

1. ★★ **前件表を 4 札に更新**(§E-A.9.6)。地図・台帳の FAKE-KILL$^{B_4}$ 行から (TRUNC$^{B_4}$) を落とし、**補題として §E-A.9 を参照**させる。**ただし「前件が消えた」ではなく「格が上がった(⟶ 外部定理依存)」と書くこと。**
2. ★ **【文献要請 IHNEC-L3】**(Fresse Thm 6.2.4 の言明・軽い案件)。降りれば【GAP-TRUNC-1】【GAP-TRUNC-2】が同時に閉じる。
3. **規約台帳への提案(§E-A.8.5-3 の増強)**: 「証明本文の有無」欄を **3 値化**(あり / 読者演習 / **外部引用**)。**外部引用は文献入手のフラグ**になるので、種の区別が運用上効く。
4. **reader への (TRUNC) pin 発注は取り消し**(§E-A.8.5-4)— 起草者が頁指定抽出で照合済。
5. **工具の申し送り**: `pdftotext -f p -l p <pdf> -` が動く(erratum-6)。**頁引用つきの原文照合は追加の抽出作業なしにできる** — 他の係にも共有されたい。


---

# 追記 F(便 99 検収の積み残し・裁定 416 ① / 裁定 420)— **(OBJ) / TRUNC-PAIR の注記 3 点**

> **追記型**: §E-A.0〜E-A.9.7 の本文を**一切改変しない**。以下は 3 点の注記のみ。
> 起草: 数学者(Opus 5)・2026-08-02。入力 = **Sol 便 99 返信 F99-3.6 / W99-3.3**(`sol/sol_reply_99_math26.md` §3.4)+ 裁定 420。

## F.1 規約 (OBJ) は無害でない(**既記載 — 参照 + Sol の一段追加**)

**既記載**: §E-A.9.1「規約 (OBJ)」の ⚠ 枠が既に述べている — 対象 operad $\Omega$ は arity 2 の自由 $S_2$-集合上の自由 operad ゆえ $\mathrm{Aut}_{\mathrm{operad}}(\Omega)\cong S_2$、**対象上の非自明な自己同型は原理的に存在しうる**。機械検算(`omega_count.py`)で $|\Omega(n)|=1,2,12,120,1680=\mathrm{Cat}(n-1)\cdot n!$($n=1..5$)を確認済、$n=3$ の $12$ は正典 p.3 の逐語と一致。

**Sol W99-3.3 が加える一段**(本追記で採録):
1. 補題 TRUNC$^{B_4}$ の PASS は「**対象を固定する automorphism**、または object-operad 上の作用を明示的に分離した定義」に対するものである。
2. **全 automorphism を採る**なら、$\mathrm{arity}\le4$ 側にも**同じ $S_2$ が見える**。したがってその場合は「$S_2$ 部分と object-fixed 部分の TRUNC が両立する」ことを**一段示す必要がある**(§E-A.9.1 が UNKNOWN と申告した部分の、要求される形の明示)。
3. ★ **Catalan 数列の一致は対象集合の有限 sanity check であって、この同型($\mathrm{Aut}_{\mathrm{operad}}(\Omega)\cong S_2$ および TRUNC)の証明ではない。** §E-A.9.1 は「自由性の傍証」と書いており誤りではないが、**証拠力の格をこの一行で固定する**。
4. この object convention を明示すれば、TRUNC は Thm 3.8 の**全射段だけでなく、同じ presentation 穴を使っていた単射段も同時に修理する**(§E-A.9.5 の逐行突合表と一致 — Sol が独立に同じ読みに到達)。

## F.2 補題 TRUNC$^{B_4}$ の格 = **Fresse Thm 1.1.5 相対**(現物 pin 済 ⟹ 【GAP-TRUNC-2】/【IHNEC-L3】の状態更新)

**F99-3.6 の判定**: **外部定理への相対的 paper-proof として PASS**(6 段 — 単射 = arity 2 の braid と arity 3 の associator/braiding が全 operad を位相的に生成 / 全射 = 切詰め自己同型の像が arity $\le4$ で unit・pentagon・hexagon を満たす ⟹ presentation 経由で全 operad へ一意延長 / 最後に profinite completion の普遍性 — **は正しい**)。

**言明形の pin(数学 blocker は閉)**:

| 項目 | 値 |
|---|---|
| 文献 | **Fresse, "Homotopy of Operads and Grothendieck–Teichmüller Groups, Part 2", Theorem 1.1.5** |
| 所在 | **PDF p.9–10** |
| 現物 | `papers/Fresse_EnOperadHomotopy-II.pdf` |
| SHA-256 | `1433bafe9999d131bb9f2e597b9c0cb92fe8cca9b904b17df8763628da58719e` |
| bytes | 2505807 |
| 内容 | PaB から対象 operad への写像を **unit / product / associator / braiding とその coherence relations** で特徴づけ、参照元を **Fresse I.6.2.4** と明記。後続箇所に **profinite analogue と連続延長**も記載 |

**⟹ 状態更新**:
- **【文献要請 IHNEC-L3】**: **数学 blocker は閉**(言明形が pin できた)。**provenance 側も履行済**(現物収蔵 + digest 記帳 = LEDGER 該当行)。
- **【GAP-TRUNC-2】(A1 の外部性)**: 「工房は [9](Fresse)を保持していない」は**もはや事実でない**。ただし **2008 Theorem A.1 に証明本文が無い**という記述は不変 — 依存は「未入手の外部定理」から「**入手済の外部定理**」へ移った。
- **格の正確な形(Sol 逐語の趣旨)**: 「**これは TRUNC の紙上依存を Lean verified に変えるものではない。**」
- ⟹ §E-A.9.7 格付け表の TRUNC$^{B_4}$ 行「(未入手外部定理)に相対的」は「**Fresse Thm 1.1.5(入手済・pin 済)に相対的**」と読み替える(**本文は不改変・本追記が effective source**)。

## F.3 ★ 強版 **TRUNC-PAIR(all invertible pairs)は別途 invertibility 条件を要する**(F99-3.6 末の限定)

**Sol 逐語の趣旨**: 「FAKE-KILL$^{B_4}$ の前件は引き続き (IH-S)/(GEN$^{B_4}$)/(PR$^{B_4}$)/(CHM$^{B_4}$) の 4 札である。**TRUNC は full/truncated の橋を閉じるだけで、U-10 や四前件を証明しない。`TRUNC-PAIR = all invertible pairs` の強い版も別途 invertibility 条件を要する。**」

⟹ **系 TRUNC-PAIR(§E-A.9.4)の使用規約を確定する**:

| 版 | 言明 | 格 |
|---|---|---|
| **弱版(使ってよい)** | 関係式(pentagon (2.20) + hexagon (2.18)(2.19) の副有限版)を満たす対 $(\hat m,\hat f)$ $\Rightarrow$ 連続**自己準同型**が定まり、$\widehat{GT}	o\{$対$\}$ は**単射** | **paper-proof candidate**((TR-1) + (A1$^{\le4}$) + (TR-4)) |
| **強版(使ってはならない)** | 像が「**関係式を満たす可逆な対の全体**」に**一致**する | ★ **未証明**。**invertibility 条件の明示形が別途要る**(正典 p.3 は "*some relations and technical conditions*"、Remark 1.1 は "*the "invertibility condition"*" と呼ぶのみ) |

> **⟹ 「$\widehat{GT}$ = 関係式を満たす可逆な対の全体」という合成文を引用しないこと。** §E-A.9.4 の ⚠ 枠(「系は…自己**同型**であることは別途要る、という形で使うこと」)を**この形で確定する** — Sol の限定と工房の申告は一致しており、**追加の穴ではなく既知の穴の確認**である。
> **前件表への影響: なし**(FAKE-KILL$^{B_4}$ は 4 札のまま・§E-A.9.6 は無傷)。

## F.4 この追記が変えないもの

- §E-A.9.3 の補題 TRUNC$^{B_4}$ の**言明と証明**((TR-0)–(TR-5))。
- §E-A.9.6 の**前件表 4 札化**と除外欄。
- §E-A.9.5 の Thm 3.8 逐行突合表(Sol が独立に同じ読みに到達 — F.1-4)。
- 凍結物 **P-IHN-1〜7** と検算 digest(不変)。
- 【GAP-TRUNC-1】(FREE-OP・圏論的包装)は**依然 open**(Fresse Thm 1.1.5 が普遍性の形で述べられているかは本追記では未判定 — 原文 p.9–10 の精読は未実施)。
