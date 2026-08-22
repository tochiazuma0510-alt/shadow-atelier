# Sol 便 156 返書 — C3-LIFT / T-ARITH 監査

日付: 2026-08-22  
監査固定点: `9f6ad83f18fe4d5f1352fea411e3b5bb720ff13a`  
総合裁定: **条件付き**

結論を先に述べる。C3-LIFT の幾何鎖は、次の二つの修正を入れれば通る。

1. `R=ker(F₂→C₃)` が対応するのはコンパクト楕円曲線 `E` の基本群ではなく、三尖点を除いた開曲線
   `U₃=E\{O,(0,4),(0,-4)}` の幾何基本群である。memo の `X₃` はこの `U₃` を指す、と明記しなければならない。
2. 重み完全列の `G_ℚ`-同変分裂は「コンパクト部分が自由・飽和」という理由からは出ない。分裂を残すなら、二つの尖点差が有理 3-torsion であり、2 がその群上で可逆なので mod-2 Kummer 類が消える、という理由に差し替える。ただし C3-LIFT に必要なのは同変な完全列と商 `H₁(U₃)/W≅E[2]` だけで、分裂自体は不要である。

この修正形では【GAP-C3-1】(a)〜(c) に未解決の数学的欠落は残らない。従って C3-LIFT を前件とする T-ARITH と残問縮約の論理も通る。ただし便の明示規律どおり、本便では積荷を `candidate` から格上げせず、`verified` とも書かない。park は「EC-83 算術レーンを再開してよい」という限定で解除可とするが、83 窓全体の genuine/fake 判定は依然 UNKNOWN である。

## 0. 指定資料の読了

指定順を守り、次を全文読了・照合した。

1. `scratchpad/gt_grt_dictionary_memo_v1.md` 全文。特に §3、§7.7 の (S1)〜(S5′)、§7.8、ならびに A5 対象の §2・§4。
2. `search/certs/koubou83_c3lift_indepcheck_v1_1_20260822.json` と、誤規約を保存した v1。
3. `docs/状態.md` の該当末尾ブロックと `docs/notes/c83_closure_index_v1.md` 全文。
4. 指定絶対パスの `pending_ruling1206.md`、裁定 1543〜1562。
5. NW Cor 7 と Willwacher §6.1 は、本便の指定どおり memo に固定された引用範囲だけを用いた。

対話帳の新着 T-62〜T-66 も確認し、`cross-checked` と `verified`、有限探針と全深度、83 線と 972 線を混同していない。

## 1. 積荷 (S1)〜(S7) の裁定

| 項目 | 裁定 | 射程 |
|---|---|---|
| (S1) C3-LIFT | **修正文で GO、現行逐語は条件付き** | §2 の開曲線・基点・同変完全列の修正が必須。結論 `P/Φ(P)≅E[2]`、算術核に位数 3、像位数 ≥12 はその後通る。 |
| (S2) RES-1 | **(S1) 相対で GO** | `Θ(ker χ_vir)=C₃` は有限群測定、`Θ(A)=C₃` は C3-LIFT。層 1 の飽和を超えて `A` 全体を決めない。 |
| (S3) T-ARITH | **(S1) 相対で GO** | 補題 M、`|H₀|=6`、Sylow 3 一意性の鎖は正しい。結論の「全 K」は厳密には **全細分 `K≤N`**。 |
| (S4) NILP-VOID | **83 窓について GO** | `γ₂(G)=γ₃(G)` と `f_g∈F̂₂′` から pro-nilpotent 情報が円分下界を増やさない。972 への一行拡張は別途 `γ₂=γ₃` 等を pin し、`G^ab` だけから最大 2-商が可換とは結論しない。 |
| (S5′) W-1 artifact | **測定記述を受理** | v1_1 は各 12 行中 `t_pair_valid=3`、対応 ν は `0,2,1`。三 DEEP15 record で同じ multiset。v1 の 1/12 からの修復は W-1 診断と一致する。 |
| (S6) 残問縮約 | **GO** | `A⊇R_N(𝒯)` なら `|A|∈{3,6,12}`。`A₀` は `R_N(𝒯)` または `H₀` の二択で、`ker(Θ|H₀)` の非単位生成元 1 個が判定ビットになる。 |
| (S7) 片側反証器 | **強化形で登録可** | strict representative の失敗や有界探索の失敗では不可。全 reduction fibre を尽くした真正の死亡証明書だけを反証器とする。 |

## 2. A1 —【GAP-C3-1】三分割監査

### 2.1 (a) `R` と幾何基本群、接ベクトル基点

`U:=P¹_ℚ\{0,1,∞}` とし、幾何基本群の標準生成元を `x,y`、`z=(xy)^{-1}` とする。被覆

`w³=t(1-t)`

は `U` 上で有限 étale 3 次である。幾何モノドロミー

`q: π̂₁(U_{Q̄})≅F̂₂ → ℤ/3`, `q(x)=q(y)=q(z)=1`

の核は、有限指数部分群 `R=ker(F₂→C₃)` の閉包、すなわち `R̂` である。有限指数部分群なので、`R̂` と `F̂₂` 内の閉包の間に問題はない。

ここで重要な修正は、`R` が階数 4 の自由群であることからも分かるように、対応先はコンパクト種数 1 曲線の基本群ではないことである。座標変換

`u=2t-1`, `X=-4w`, `Y=4u`

により滑らかな完備化は

`E: Y²=X³+16`

となり、除いた三点は

`S={O,T,-T}`, `T=(0,4)`

である。従って正しい同一視は

`R̂ ≅ π̂₁(U₃,Q̄)`, `U₃:=E\S`

である。memo で `X₃` を affine/open curve の意味に固定するなら同じ内容だが、`π̂₁(E)` と書くのは誤りである。

接ベクトル基点については、基底側の標準 tangential base point と、その上の幾何的 lift/path を一つ選べばよい。lift の変更は deck transformation による同型を変えるだけで、以下の `G_ℚ`-加群の同型型を変えない。従って「基点を無視した文字どおりの等号」ではなく、「lift を選んだ同型、選択変更に対して同型」という形にする。

### 2.2 (b) `R` の安定性と ℚ-構造

Ihara 作用を `φ_g` と書くと

`φ_g(x)=x^{χ(g)}`, `φ_g(y)=f_g^{-1}y^{χ(g)}f_g`, `f_g∈F̂₂′`

である。従って `q` の上では共役項が消え、

`q∘φ_g = (χ(g) mod 3) q`

が成り立つ。`χ(g) mod 3` は単元なので `ker q=R̂` は安定である。これは cover の descent datum を与える。また式 `w³=t(1-t)` 自体が ℚ 上にあるので、ℚ-構造は循環論法なしに明示されている。

ただし ℚ 上の deck group は定数群 `C₃` ではなく `μ₃` であり、`Q̄` 上で `C₃` になる。Galois が deck generator を `χ mod 3` で動かすことが、上の式と同じ内容である。「ℚ 上の C₃-Galois cover」という語はこの捻れを隠すため避ける。

### 2.3 (c) 重み完全列、同変性、分裂

三点 `O,T,-T` はすべて ℚ-rational で、接線公式から `2T=-T`、従って `3T=O` である。開曲線の étale homology には `G_ℚ`-同変な完全列

`0 → W → H₁(U₃;F₂) → H₁(E;F₂) → 0`

があり、

- `W≅\widetilde H₀(S;F₂)(1)` は二次元、`x³,y³,z³` の cusp inertia class が張り、関係は一つ。
- 三尖点は点ごとに ℚ-rational、かつ `F₂(1)` は自明なので `W` は自明 `G_ℚ`-加群。
- `H₁(E;F₂)≅E[2]` は `G_ℚ`-同変。

である。

この完全列の存在と同変性だけで C3-LIFT には十分である。「コンパクト部分が自由だから分裂」という現行理由は、ベクトル空間としての分裂しか与えず、`G_ℚ`-同変分裂の理由にはならない。分裂まで主張するなら、generalized Jacobian/1-motive の拡大類が尖点差 `T,-T` の mod-2 Kummer 類であり、`T=2(-T)`, `-T=2T` と 2 が有理 `C₃` 上で可逆であるため両類が消える、と補う。これは非標準な `G_ℚ`-同変分裂を与えるが、以下では使わない。

`P=[G,G]=R/N_{F₂}` とする。isolated/settled 性から `N_{F₂}` は Ihara 作用で安定し、自然な全射

`H₁(U₃;F₂)=R/Φ(R) → P/Φ(P)`

は `G_ℚ`-同変である。独立測定は `d(P)=2` と `x³,y³,z³∈Φ(P)` を返す。従って核は二次元の `W` を含み、両辺の次元から核はちょうど `W`。ゆえに

`P/Φ(P) ≅ H₁(U₃;F₂)/W ≅ E[2]`

が `G_ℚ`-加群として従う。

### 2.4 C3-LIFT の残りの鎖

`E[2]` の x 座標は `X³=-16` を満たすので

`Q(E[2])=Q(ζ₃,∛2)`、Galois 群は `S₃` である。その最大可換部分体は `Q(ζ₃)`。従って

`Q(E[2])∩Q(ζ₂₄)=Q(ζ₃)`

であり、`G_{Q(ζ₂₄)}` の `E[2]` 像には `C₃` が残る。この部分では `χ≡1 mod 24` なので `m≡0 mod 12`。非自明な `E[2]` 作用は非自明な Ihara shadow を与える。よって

`A₀:=Im(Ih_N)∩H₀`

の位数は 3 で割れ、`Im(Ih_N)∩ker χ_vir` は位数 3 の部分群を含む。`χ_vir` 像の位数は 4 なので `|Im(Ih_N)|≥12`。各窓で非単位 2 元、計 4 元が算術的候補除外集合から落ちる、という会計も正しい。

**A1 裁定**: 数学的には GO。ただし §2.1 の open/compact 区別と §2.3 の分裂理由を memo に versioned 訂正するまで、現行逐語の無条件採用はしない。

## 3. A2 — T-ARITH、RES-1、残問縮約

### 3.1 補題 M と C-15(C1) の使用

`H:=ker χ_vir` では `m∈{0,6}`。群法 (3.53) の第一成分

`m₁⋆m₂=2m₁m₂+m₁+m₂ mod 12`

を代入すると `{0,6}` は `C₂` となり、`μ:H→C₂` は準同型である。登録済み C-15(C1) の `|H|=12` と m=6 層 6 元は二系統有限測定であり、ここでは凍結された有限前件として使ってよい。これは C3-LIFT や T-ARITH の結論を使っていないため循環しない。`μ` は全射、従って `H₀=ker μ` は位数 6。

位数 6 の群の Sylow 3 部分群は一意である。補題 U′、周期 `e=3`、非自明性測定から `R_N(𝒯)` は `H₀` の位数 3 の部分群であり、それが唯一の Sylow 3 である。

C3-LIFT の算術三元は `χ≡1 mod 24` から `m=0`、従って `A₀` に入り、`E[2]` 上で相異なるので `3∣|A₀|`。ゆえに `A₀` は唯一の Sylow 3、すなわち `R_N(𝒯)` を含む。この Sylow 論法はどの shadow がどの ν かを使わないため、v1 の W-1 artifact に依存しない。

従って、A1 の修正形を前件に

`R_N(𝒯)⊆Im(Ih_N)`

が従う。arithmetical ⇒ genuine と Cor 5.4 により、三元は **全ての細分 `K≤N`** へ生存する。「全 NFI の無関係な K」という意味にはしない。

### 3.2 RES-1

cert は `Θ(H)` の作用次数を `1:4, 3:8`、external action 0 と返すので `Θ(H)=C₃`、各 fibre 4。C3-LIFT は `Θ(A)=C₃` を与える。従って

`Θ(A)=Θ(H)`

であり、層 1 は算術部分で飽和する。この等式は `A=H` を意味せず、次の情報には `ker Θ` を見る L₂/`Q(E[4])` レーンが必要、という RES-1 の読みは正しい。

### 3.3 残問の縮約

`A⊆H`, `R_N(𝒯)⊆A` より Lagrange から `|A|∈{3,6,12}`。さらに `A₀` は `H₀` 内で唯一の `C₃` を含むので、`A₀=R_N(𝒯)` または `A₀=H₀`。v1_1 の作用測定から `|ker(Θ|H₀)|=2` であり、その非単位生成元が算術的なら後者、そうでなければ前者である。従って m=0 部は一ビット、m=6 層は「算術元が一つでもあるか」のもう一ビットに縮約される。

**A2 裁定**: GO。ただし全結論は A1 の修正文、C-15(C1) の凍結有限前件、isolated 性に相対し、本便では candidate 格を維持する。

## 4. A3 — (S7) 片側反証器

登録は認めるが、次の強化を必須とする。

1. 対象を `K≤N` と reduction map `R_{K,N}` で pin し、死亡対象が同じ `[0,f_ν]∈GT(N)` であることを canonical key で確認する。
2. 「strict representative `f_ν` が K で charming でない」「T-EX の厳密族 witness が失敗」は死亡証明書ではない。T-DEAD がまさにその失敗を予言している。`R_{K,N}^{-1}([0,f_ν])` の **全 fibre**に lift がないことを証明しなければならない。
3. 有界探索の不発、solver UNKNOWN、未尽の coset は反証に使わない。CLAIM-COVER-1 の exact multiset coverage、legal/charming/direct gate、破壊・陽性対照を要求する。
4. 真の死亡証明書が出れば T-ARITH の結論と矛盾する。ただし論理的には C3-LIFT/A1 だけでなく、C-15(C1)、`R_N(𝒯)` の同定、reduction 実装を含む前件の連言のどれかを反証する。原因を C3-LIFT に一意帰属させない。
5. 有限深度で死亡が出ないことは支持証拠へ格上げしない。

この形なら、park 中の既存計器を正側定理の高感度 falsifier に転用する設計として有効である。

## 5. A4 — 規約諮問

### 5.1 W-1 assert の義務化

**採用。** コメントや語順文字列の pin だけでは不足し、非可換 fixture 上の意味論 assert を mandatory gate にする。

最低限、paper-aware product helper を通して `ν=1` の補題 U′

`f₁^{-1}σ₂f₁ = xσ₂x^{-1}`, `f₁=yx^{-1}`

を B₃ または規約感度を持つ固定非可換 fixture で assert する。GAP 側の `f₁` は `x^{-1}*y` である。同時に旧誤形 `y*x^{-1}` が同じ fixture で不一致になる陰性 canary を要求する。可換商、単生成元、空語だけの fixture は W-1 に盲なので不可。

現行 v1_1 は構成行を正しく直しているが、fail-closed assert はまだない。また source :193〜195 の「ker χ は m=0 のみ」と :233 の「m=0 so u=1」は、直後の正しい実装 `m∈{0,6}` と矛盾する stale comment である。v1_1 を上書きせず、次版で assert とコメント修正を入れる。

### 5.2 `ad_convention` pin

**採用。** cert には少なくとも次を機械生成して入れる。

- `paper_ad_x(u) = x*u*x^-1`
- `gap_power_convention: u^x = x^-1*u*x`
- 実装が raw GAP 積 `x*u*x^-1 = u^(x^-1)` のどちらを `Ad(x)` とラベルしているか
- ν と action class の対応表、および非中心 fixture 上の assert 結果
- `word_convention_id`, `action_convention_id`, checker source SHA

これにより v1_1 の `ν=2↔matches_adx`, `ν=1↔matches_adx2` はバグでなく、raw GAP conjugation label と paper `Ad` の符号差だと cert 単体で判読できる。

## 6. A5 — grt 辞書と P-GRT-1

### 6.1 D1〜D5

| 項目 | 裁定 |
|---|---|
| D1 | `N(ℓ,k,j)=γ_k(PB₃)PB₃^{ℓ^j}` の NFI 性、直積分解、有限冪零 ℓ-商、当該部分族が非 cofinal、はいずれも証明が通る。inverse limit の座標同定はこの部分族に限る。 |
| D2 | pro-ℓ 情報が有限 G の最大 ℓ-商まで、全 ℓ で最大冪零商までしか見ない、という普遍性は正しい。 |
| D3 | (i)〜(iii) は受理。**(iv) の `U₀=grt_hex` 同定は数値一致だけなので定理 D3 から分離し、GAP-DICT-1 candidate とする。** |
| D4 | 拡大類 `e` を graded module data が忘れ、KER-π が obstruction に載る、という核心は正しい。ただし「`e=0` なら grt と有限窓の対応が同値になる」は過大。`e=0` はこの一つの障害を消すだけで、全情報の同値を与えない。 |
| D5 | `log f_ν` の最低次が `ν(Y-X)` で hexagon-only 重み 1 を張ることは正しい。「𝒯 はその群水準の化身」はこの associated-graded の意味に限定する。 |

### 6.2 `grt_hex`、次元表、NW(7)

Ihara bracket で閉じることが未証明なら、現時点では `𝔤𝔯𝔱^hex` を「Lie 代数」と断言せず、**斉次 hexagon solution space** と呼ぶ。重み別次元の線型計算自体には bracket closure は不要である。

二つの大素数で同じ rank が出たことは強い sanity check だが、char-0 rank の証明ではない。整数行列では mod-p rank は有理 rankを超えないため、二素数一致は有理 rank の下界を与えるにとどまる。厳密化には fraction-free 有理消去、非零 minor と kernel basis の両証明、または SNF 証明書が要る。従って w≤12 表は candidate のまま。

NW Cor 7 の引用範囲を「weight≤29 で Conj. 2 の四 Lie algebra が一致」に限定する読みはよい。その引用を前件に、自由 Lie 生成関数から `dim grt₁₆=5` を得ることも整合する。ただし本便は論文全体の独立精読ではなく、指定された memo 内引用の監査である。

`294/6=7²`, `42/6=7` と重み 2〜4 の指数が合うことは、bridge candidate の **retrospective numerical agreement** である。既知の GAP 値を独立に cross-check した、または BIT-252 を証明した、とは書かない。D3(iv) が未証明である以上、「独立再現」より「独立な graded 会計との一致」が最大文である。

### 6.3 NILP-VOID と再開指標

83 両窓では `γ₂=γ₃` が二系統測定されているため、NILP-VOID の適用は通る。`nilvis(N):=dim(γ₂/γ₃)` は係数体なしには未定義なので、

`nilvis_p(N):=dim_{F_p}((γ₂/γ₃)⊗F_p)`

のベクトル、または単に `γ₂/γ₃` の群同型型を記録する形へ直す。`solvis` は現段階では数値不変量でなくレーン選択ラベルであり、その格を明記する。

972 については `G^ab` が小さい 2 群というだけでは最大 2-商が可換とは限らない。972 に NILP-VOID を適用するなら、その対象での `γ₂=γ₃`、または最大冪零商の直接計算を別に pin する。本便では 83 結論だけを採用する。

### 6.4 P-GRT-1

事前登録そのものは採用する。ただし最初の凍結宇宙は **ℓ=7、重み≤5 の一窓**に限定し、window presentation、`𝒳`、charming/PENT の述語版、row universe、char-0/mod-7 rank canary を digest 化する。memo 自身が重み 2 で標数 3 の段差を指摘しているため、全素数に同じ char-0 指数式を無条件適用しない。一般版は mod-ℓ rank を入力にした次版として分ける。

P-GRT-1 が外れた場合の分岐は、既登録どおり「mod-ℓ 段差」または「有限窓 bridge/非線形 lifting の破れ」でよい。既知の結果を見て予言本文を上書きしない。

## 7. park 解除と正本更新の条件

park は次の限定で解除してよい。

- 再開対象: EC-83 の `E[4]` / punctured CM elliptic pro-2 レーン、ならびに S7 の完全 fibre falsifier。
- 解除しないもの: 18 候補の全算術性、`Im(Ih_N)=GT(N)`、83 線の全体 genuine/fake 判定、深度線完結。
- C-15/地図へ反映する最大文: 「A1 の修正文に相対して C3-LIFT/T-ARITH の paper chain が Sol 監査を通過。三 torus image は算術的という candidate 結論を持ち、全体は UNKNOWN。verified ではない。」

正本更新前の条件は次の五点である。

1. `X₃` を `U₃=E\S` とコンパクト `E` に分離し、tangential basepoint の選択依存を記す。
2. 重み完全列の同変性を localization sequence で書き、分裂理由を 3-torsion/Kummer に差し替えるか、不要な分裂主張を削る。
3. T-ARITH の「全 K」を「全細分 `K≤N`」へ修正する。
4. S7 を全 reduction fibre の死亡証明書へ強化し、W-1 assert と `ad_convention` pin を次版 checker/cert に入れる。
5. A5 の格境界(D3(iv)、D4 の `e=0` 文、`grt_hex` 名称、294/42 の語、P-GRT-1 の ℓ-scope)を同期する。

## 8. digest と来歴

便 §4 の再計算結果:

| path | 結果 |
|---|---|
| `scratchpad/gt_grt_dictionary_memo_v1.md` | 61277 bytes / `205e6e6eacf87944` — 一致 |
| `...c3lift_indepcheck_v1_1...json` | 11807 / `d169cecd6d65b8f7` — 一致 |
| `...c3lift_indepcheck_v1...json` | 11009 / `de739dab576fc9f8` — 一致 |
| `scratchpad/koubou83_c3lift_check_v1_1.g` | 24599 / `07f682df0ce70b1f` — 一致 |
| `docs/notes/c83_closure_index_v1.md` | 9674 / `f97a9d2cbb3790ab` — 一致 |
| 指定裁定簿 | 414788 / `e6481bb0969ccff3` — 一致 |
| `docs/状態.md` @ pinned commit `9f6ad83f…` | 30488 / `a86576db0ad75950` — 一致 |
| 現作業木 `docs/状態.md` | 31433 / `23070bc043ffad6c`。先頭 30488 bytes は `a2f26ef48dd85dfa` で、便記載 prefix と不一致 |

最後の不一致は、現作業木で grt ブロックの一文変更と C3 検証ブロックの**途中挿入**が行われたためである。内容は裁定 1557〜1562 と整合するが、「追記型なら prefix 一致」という配達規律には適合しない。固定 commit の blob は正しいので本監査の数学入力は復元可能だが、次 freeze では append-only か full digest 更新のどちらかに統一する。

v1/v1_1 の機械比較では、task1 structural record は label を除き三 record で同一、task2 は row 順を除く multiset が同一。各 record は `m={0:6,6:6}`、action order `{1:4,3:8}`、external 0、v1 の valid 1 から v1_1 の valid 3 (`ν=0,2,1`)へ変化した。これは S5′ の数値と一致する。

## 9. 監査範囲外と規律

便 §3 の五項は格上げしていない。

1. M1/M2/M3 は未発注・未測定。
2. P-GRT-1 は登録のみ。
3. C-15/地図への T-ARITH 反映は本返書条件の執行後。
4. 972 A 型 v3 は本便の裁定対象外。
5. Lean は未着手。

`cross-checked` と `verified` を分離し、UNKNOWN を負の証拠にせず、P-GRT-1 を後知恵で変更していない。数値は cert/digest の機械再計算から転記した。

AUDIT_156_VERDICT: 条件付き
