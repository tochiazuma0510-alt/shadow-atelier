# Mathlib4 網羅度調査 v1(裁定 531 発火)

**状態札: `survey(読み取り専用調査・単系統)/ 公理台帳・着工可否の変更は司令塔裁定に留保 / lean/ 非接触 / 封印非接触`**

- 起草: 影工房 調査係 / **2026-08-05**
- 委嘱: **裁定 531**(docs/状態.md 施策 9)「Mathlib 網羅度調査: 公理 T2×6+T1×2 の討ち取り可能性+橋 B[エタール π₁]の待ちの精密化」— 【LP1-GAP-1】(Mathlib API 存否の版 pin つき実地調査)への回答。
- 需要側正本: `docs/notes/lean_p1_allocation_plan_v1.md`(49 補題・ブロック A〜H・公理 T2×6+T1×2)/ `docs/notes/lean_axiom_policy_v1.md`(v1.6 まで)。
- **版 pin**: mathlib4_docs ビルド commit **`503b1a2818938506db0e99d814816c83e9c054a9`**(本調査で取得した全 docs 頁の source link が同一値・2026-08-05 取得)。宣言存否の名前検索は Loogle(Mathlib master 追随・2026-08-05 照会)。
- ⚠ **鮮度注意: Mathlib は高速に動く**。本稿の「あり/なし」はすべて上記 commit・照会日に相対化した主張である(公理方針 v1.6-2)。着工時には toolchain/commit を pin して**再判定必須**。

---

## 0. 先に結論(7 行)

| # | 発見 | 重み |
|---|---|---|
| **①** | ★★ **`T1_cyclotomic_ram2` は討ち取れる**。`IsCyclotomicExtension.Rat.ramificationIdxIn_eq`(n=p^(k+1)·m, p∤m ⟹ e=p^k(p−1))に p=2, k=1, m=n(奇)を代入して e(𝔭/2)=2 が**そのまま出る**。⟹ **実質 T1 公理は 2 本 → 1 本(`T1_kummer_duality` のみ)へ削減可能**(台帳変更は司令塔裁定) | ★★ |
| **②** | `T1_kummer_duality` は**公理のまま正**(副有限 Kummer 双対は不在)。ただし部品(有限巡回 Kummer 理論・Hilbert 90・連続コホモロジー枠)は着地済みで、最弱形の再設計余地あり | ★ |
| **③** | T2 6 本は**全て公理のまま正**(論文固有・原理的に Mathlib に来ない)。ただし `T2_composition` の整数恒等式 (3.49) は Lean で証明可能な部品 — 公理を (3.53) 部分へ縮小できる | ★ |
| **④** | ★★ **橋 B の「待ち」の実態が変わった**: 抽象 Galois 圏理論(SGA1 V Th 4.1 級の圏同値・pro 表現可能性・π₁ の特徴付け)は **Mathlib で完成済み**。欠けているのは**スキーム側のみ**(有限エタール射・FiniteEtale(X) 圏・π₁^ét・SGA1 IX 完全列・接基点)。さらに**アフィン(環)版の有限エタール圏+繊維関手は既にある**(`CommAlgCat.FiniteEtale`) | ★★ |
| **⑤** | 着工可ブロック A・E・H の「M」見込み(【LP1-GAP-1】)は**全て裏取りできた**: `autEquivPow`(円分ガロア群)・`Finite.injective_iff_bijective`・`ZMod.AddAutEquivUnits`(Aut(C_M) の加法版)ほか §6.1 の X-1〜X-7 相当も標準供給圏内 | ★ |
| **⑥** | ブロック F(E1-3)が要求した「副有限群・逆極限 API の監査」への回答: **ProfiniteGrp 圏・射影極限・profinite 完備化(普遍性=随伴つき)まで存在**。格上げ判断は司令塔 | ★ |
| **⑦** | 不在確定(名前検索+ファイル一覧の範囲): braid 群(B₃/B₄/PB₃)・Reidemeister–Schreier・名前つき Ẑ(本体)・inflation-restriction・Nielsen–Schreier 階数公式 | — |

---

## 1. 13 項目突合表(概観)

判定: **あり** / **部分的** / **なし**。根拠列の [L#]=Loogle 照会・[D#]=docs 頁・[G#]=GitHub は §5 の URL 台帳を指す。

| # | 項目 | 判定 | 主な供給(モジュール / 主宣言) | 欠け | 根拠 |
|---|---|---|---|---|---|
| 1 | 自由群・Nielsen–Schreier・部分群の階数 | **部分的** | `FreeGroup`・`IsFreeGroup`・`FreeGroupBasis`(GroupTheory.FreeGroup.*)/ **`subgroupIsFreeOfIsFree : IsFreeGroup H`**(GroupTheory.FreeGroup.NielsenSchreier) | ★ **階数公式なし**(rank−1=[G:H](rank−1) は docs に言及なし・FreeGroupBasis に card/rank 系 0 件)。代替: Schreier 補題 `Subgroup.rank_le_index_mul_rank`(Group.rank=最小生成数・自由階数ではない) | [L19][L29][L32][L33][D7] |
| 2 | PresentedGroup・von Dyck | **あり** | `PresentedGroup rels = FreeGroup α ⧸ normalClosure rels`・**`PresentedGroup.toGroup`(関係を満たす写像の持ち上げ = von Dyck)**・`toGroup.unique`・`ext`・`closure_range_of`(GroupTheory.PresentedGroup) | — | [L12][D11] |
| 3 | braid 群(B₃/B₄・表示・PB₃・中心) | **なし** | —("braid" 473 件は全て BraidedCategory 圏論+`CoxeterSystem.braidWord`/`wordProd_braidWord_eq` = Coxeter 系の braid 関係式) | ★ B_n という群・Artin 表示・純 braid 群・中心: 全て不在。**外部参考**: H. Fechtner「Braids in Lean」(2024-12・braid monoid/group)[E3]。工房の B₃ は項目 2 で自作するのが現実線 | [L1][L2][L28] |
| 4 | 半直積・wreath 積 | **あり/部分的** | `SemidirectProduct`(`N ⋊[φ] G`・`lift`・`map`・88 件)+ `GroupExtension` 接続(`Splitting.semidirectProductMulEquiv`)/ wreath は `RegularWreathProduct`・`IteratedWreathProduct`・`Sylow.mulEquivIteratedWreathProduct` | wreath は**正則版のみ** — 一般の置換 wreath 積(任意の H-集合上)は不在 | [L13][L3] |
| 5 | profinite 群(圏・射影極限・位相群) | **あり** | `ProfiniteGrp` 圏(of/ofFiniteGrp/**ofClosedSubgroup**/位相群 instance)+ `ProfiniteGrp.limit`・`limitCone`・`instHasLimit`(Topology.Algebra.Category.ProfiniteGrp.Basic・100 件)。付: `InfiniteGalois`(Gal(K/k) ≅ lim 有限 Gal・profiniteGalGrp — FieldTheory.Galois.Profinite・PR #16993) | — | [L4][D3][G6] |
| 6 | 群の profinite 完備化 | **あり** | **`ProfiniteGrp.profiniteCompletion : GrpCat ⥤ ProfiniteGrp`**(関手)+ `eta`(単位)+ `lift`/`lift_eta`/`lift_unique`/`homEquiv`/**`adjunction`(忘却関手への左随伴 = 普遍性)**+ `denseRange`+`etaFn_injective_iff_residuallyFinite`(ProfiniteGrp.Completion・AddGrp 版併設) | — | [L5][D12] |
| 7 | Ẑ・Ẑ^× | **なし(本体)** | 部品: `PadicInt`(ℤ_p)・profiniteCompletion(ℤ に適用すれば**位相群**としての Ẑ は合成可能)・`cyclotomicCharacter`(ℤ_[p]ˣ 値) | ★ 名前つき Ẑ(環構造・Ẑ≅∏ℤ_p・Ẑˣ・Ẑˣ→(ℤ/M)ˣ 全射)は不在("ZHat" 0 件)。**外部参考**: FLT project の blueprint に ℤ̂(compatible collections 定義)の節あり [E1][E2] — **実装ファイルの現行ツリー所在は未確認**(リポジトリ FLT/ 直下に該当名なし [G5]) | [L6][G5][E2] |
| 8 | 円分指標・絶対ガロア群・Krull 位相 | **あり** | **`modularCyclotomicCharacter : (L ≃+* L) →* (ZMod n)ˣ`**(仮定 `Nat.card (rootsOfUnity n L) = n`)・**`cyclotomicCharacter L p : (L ≃+* L) →* ℤ_[p]ˣ`**+`.continuous`・`IsPrimitiveRoot.autToPow_eq_modularCyclotomicCharacter`(NumberTheory.Cyclotomic.CyclotomicCharacter)/ **`Field.absoluteGaloisGroup K` = Gal(AlgebraicClosure K/K)**+Krull 位相群 instance+位相的アーベル化(FieldTheory.AbsoluteGaloisGroup)/ `krullTopology`(t2・totallySeparated・有限次で離散)/ 円分ガロア群 **`IsCyclotomicExtension.autEquivPow : (L ≃ₐ[K] L) ≃* (ZMod n)ˣ`** | Ẑˣ 値の大域円分指標としての一本化のみ不在(項目 7 に還元)。**工房需要の χ_{2ν}(mod 2ν)レベルは完全供給** | [L7][L8][L14][L24][D1][D2] |
| 9 | Galois 圏・fiber functor・圏論的 π₁ | **あり** | `CategoryTheory.Galois.*` 11 ファイル: `PreGaloisCategory`・`FiberFunctor`(Basic)・GaloisObjects・Decomposition・Prorepresentability・Full・EssSurj・**Equivalence: `functorToContAction : C ⥤ ContAction FintypeCat (Aut F)` が `IsEquivalence`(= SGA1 V Th 4.1 級の主同値)**・Topology(Aut F の位相)・**`IsFundamentalGroup`(位相群 π が「この圏の π₁」である公理的特徴付け+`Aut F` 自身の instance)** | — | [L9][L22][L23][G2][D6] |
| 10 | スキームのエタール π₁・有限エタール射・SGA1 IX | **なし** | あるもの: `AlgebraicGeometry.IsEtale`(Morphisms/Etale.lean)・IsFinite・IsSmooth・FormallyUnramified・WeaklyEtale・QuasiFinite ほか(Morphisms/ 38 ファイル) | ★★ 有限エタール**射**の合成述語("IsFiniteEtale" 0 件)・スキーム上の FiniteEtale(X) 圏・π₁^ét("fundamentalGroup" 113 件に AlgebraicGeometry ゼロ)・SGA1 IX 型完全列・接基点: 全て不在。**追跡 issue #16890(open・2025-03 更新)がエタール site+étale fundamental group をロードマップ化** | [L17][L25][L31][G1][G4] |
| 11 | 群コホモロジー(H¹/H²・inf-res) | **部分的** | `groupCohomology`(一般次数)+ LowDegree(**H0/H1/H2**・cocycles₁/₂・H1Iso/H2Iso)+ **LongExactSequence**+**Shapiro**+**Hilbert90**(`groupCohomology.H1ofAutOnUnitsUnique`: H¹(Aut_K(L), Lˣ)=1)+FiniteCyclic+Functoriality(RepresentationTheory.Homological.GroupCohomology.*)。**連続コホモロジー着地済み**: `continuousCohomology`(ContCohomology: Basic/Functoriality/LowDegree・31 件・H⁰≅不変量まで) | ★ **inflation-restriction 不在**(名前検索 0+ファイル一覧に無し)。連続版の H¹/H² 明示記述も未着 | [L15][L20][L21][L34][G3][D8] |
| 12 | Reidemeister–Schreier(部分群の表示) | **なし** | 部品: `Quiver.SchreierGraph`(被覆・"Schreier" 24 件は全てこれ)・Nielsen–Schreier(groupoid 経由)・Schreier 補題 `Subgroup.rank_le_index_mul_rank`(GroupTheory.Schreier) | ★ 部分群の**表示**(生成元+関係式)を返す機構は不在。外部形式化も検索で見当たらず(非存在の証明ではない) | [L11][L33] |
| 13 | エタール代数・有限エタール代数の圏 | **あり** | **`Algebra.Etale`**(= FormallyEtale+有限表示・RingTheory.Etale.Basic)+`Algebra.IsEtaleAt`・standard étale 局所構造 / **`CommAlgCat.FiniteEtale R`(有限エタール R-代数の圏)**+**fiber functor `FiniteEtale.fiber`(幾何点 Ω: S ↦ (S →ₐ[R] Ω) : FintypeCat)**+**`equivOfIsSepClosed : (FiniteEtale Ω)ᵒᵖ ≌ FintypeCat`(分離閉体上の反同値)**(RingTheory.Etale.Finite) | `FiniteEtale` への **PreGaloisCategory インスタンスは未接続**(当該モジュールに無し・他所でも未検出)— §3.3(b) の焦点 | [L36][L10][D4][D10] |

---

## 2. 公理 8 本(T2×6+T1×2)への判定

> 判定語: **公理のまま正** / **縮小可**(公理は残るが範囲を狭められる)/ **討ち取れる**(公理 → M+接続補題へ変換可能)。台帳(`lean/AXIOMS.md` 初版案)の変更は**司令塔裁定**を経る(方針 v1 §4)。

### 2.1 T2(論文固有・6 本)

| 公理 | 判定 | 説明 |
|---|---|---|
| `T2_thm43_explicit` | **公理のまま正** | 2405 Thm 4.3 (4.12) は論文固有 — Mathlib に来ることは原理的にない |
| `T2_thm43_isolated` | **公理のまま正** | 同上 |
| `T2_15_Ih` | **公理のまま正** | 2405 (1.5)。★ sanity instance の材料: 右辺の χ(mod 2ν)は `modularCyclotomicCharacter` [D1] で Mathlib の `(ZMod n)ˣ` に型接続できる — 言明を Mathlib 語彙で書くと LE-2/LE-3 との継ぎ目が消える |
| `T2_composition` | **公理のまま正・★縮小可** | (3.53) 合成則は 2401 固有で公理。しかし**同梱の整数恒等式 (3.49) は Lean で証明できる部品**であり、公理から切り離して形式化補題にすれば公理境界が縮む(v1.6-1「最弱形」の適用) |
| `T2_GTodd_def` | **公理のまま正(選択肢増)** | 定義的性質。★ `ProfiniteGrp.profiniteCompletion`+`ProfiniteGrp.limit` [D12] の着地により、GT^odd_Dih と pr_n の系を**公理でなく Lean 定義として内製**する道が現実化した(ψₙ を定義にするのと同型の判断)。採否は司令塔 |
| `T2_thm46_order` | **公理のまま正** | 較正専用(主鎖不要)は割り付け表 §4.1 のとおり |

### 2.2 T1(実質 2 本)

| 公理 | 判定 | 説明 |
|---|---|---|
| `T1_kummer_duality` | **公理のまま正(現時点)** | 副有限 Kummer 双対 Hom_cont(G_K, μ_M) ≅ K^×/K^{×M} は不在。"Kummer" 8 件は `KummerExtension`(有限巡回 Kummer 理論: `autEquivZmod`・`isCyclic_tfae` [D9])と KummerDedekind のみ。**部分短縮材料**: ①Hilbert 90 = `groupCohomology.H1ofAutOnUnitsUnique` [D8] ②連続コホモロジー枠 `continuousCohomology` [L34](ただし低次は H⁰ まで)③有限レベル巡回対応 [D9]。⟹ 公理の**最弱形を「必要な有限レベルの対応」に狭める再設計余地**あり(LH-2/LH-6 の実使用形を見て司令塔判断) |
| `T1_cyclotomic_ram2` | ★★ **討ち取れる** | **`IsCyclotomicExtension.Rat.ramificationIdxIn_eq (n) (hn : n = p^(k+1) * m) (hm : ¬p ∣ m) [IsCyclotomicExtension {n} ℚ K] : (Ideal.span {↑p}).ramificationIdxIn (𝓞 K) = p^k * (p-1)`**(NumberTheory.NumberField.Cyclotomic.Ideal [D5][L27])。4n = 2^(1+1)·n(n 奇)に p=2, k=1, m=n を代入して **e = 2¹·(2−1) = 2**。LC-9 への接続は `ramificationIdxIn`(Galois 拡大での素点一様値)を個別素点へ降ろす `Ideal.ramificationIdxIn_eq_ramificationIdx`(NumberTheory.RamificationInertia.Galois)で 1 行級。⟹ **公理 → M+接続補題 1 本** |

$$\Longrightarrow\quad\textbf{実質 T1 公理は }2\text{ 本}\to\boxed{1\text{ 本}}\ (\texttt{T1\_kummer\_duality})\text{ へ削減可能(裁定待ち)}$$

### 2.3 参考: 割り付け表が「取込済/要確認」とした T1 3 本の裏取り

| 公理 | 割り付け表の主張 | 本調査の裏取り(版 pin 503b1a28) |
|---|---|---|
| `T1_cyclotomic_galois` | 取込済 ⟹ M | ✔ **確認**: `IsCyclotomicExtension.autEquivPow : (L ≃ₐ[K] L) ≃* (ZMod n)ˣ`(NumberTheory.Cyclotomic.Gal)[L24] |
| `T1_finite_inj_bij` | 取込済 ⟹ M | ✔ **確認**: `Finite.injective_iff_bijective`(Mathlib.Data.Fintype.Card)[L30] |
| `T1_autCyclic` | 要確認 | **部分的(討ち取り見込み)**: `ZMod.AddAutEquivUnits (n) : AddAut (ZMod n) ≃+ Additive (ZMod n)ˣ`(Mathlib.Data.ZMod.Aut)[L18]。一般巡回群 C_M の MulAut 版は直接ないが、`zmodEquivZPowers` 級の同型で転送する**糊補題 1 本**で足りる見込み — 公理にせず工房補題で書ける |

### 2.4 付記: ブロック F(E1-3)の「Mathlib 副有限 API 監査」への回答

LF-1/LF-2 の保留理由「Mathlib の逆極限・副有限群 API の監査が要る」に対し: **API は存在する** — `ProfiniteGrp` 圏+`limit`(射影極限)[L4]・`profiniteCompletion`(普遍性=随伴)[D12]・`ofClosedSubgroup`・`ContinuousMulEquiv` 系・`InfiniteGalois`(Gal ≅ lim)[D3]。E1-3 の pr_n(逆極限からの射影)と全射性の議論はこの語彙で書ける見込み。**着工可否の格上げは司令塔判断**(本稿は存在確認まで)。

---

## 3. 橋 B(エタール π₁ 依存ブロック)の「待ち」の精密化

### 3.1 正確に何が欠けているか(LB 対応つき)

| # | 欠け | 対応 LB | 状態(版 pin 503b1a28) |
|---|---|---|---|
| B-i | スキームの**有限エタール射**(finite+étale の合成述語)と **FiniteEtale(X) 圏** | LB-2/3/9 | 不在("IsFiniteEtale" 0 件 [L31]。`IsEtale`・`IsFinite` は個別に存在 [L25][G4]) |
| B-ii | FiniteEtale(X) が **Galois 圏**である証明+幾何点の **fiber functor Fib_x̄**(スキーム版) | LB-2/3/9 | 不在(LB-9 の「Fib の型がない」は正確なまま) |
| B-iii | **π₁^ét(X, x̄) の定義** | LB-2〜11 | 不在("fundamentalGroup" に AlgebraicGeometry ゼロ [L17]) |
| B-iv | **SGA1 IX 6.1 型の homotopy 完全列**・基底変換(EXSEQ 系) | LB-4/5/6 | 不在 |
| B-v | **接基点**(tangential base point・01→)と π₁(P¹−{0,1,∞}) ≅ F̂₂(TB3)・Riemann existence 系 | LB-7 | 不在 |
| B-vi | **慣性の比較**(TB4ᵘ) | LB-8 | 不在(ただし**数体・環レベル**の分解群・慣性群・e/f は RamificationInertia.Galois/HilbertTheory にあり [L26] — 部品) |
| B-vii | 上流の動き | — | **追跡 issue #16890「smooth morphisms of schemes and étale fundamental group」が open**(2024-09 起票・2025-03 更新)でエタール site+π₁ を明示ロードマップ化 [G1]。進行順の観測: Galois 圏(着地済)→ 環版 FiniteEtale(着地済)→ スキーム版(未)。着地時期の予測は本稿ではしない |

### 3.2 既にある側(待ちを短縮する在庫)

1. ★★ **抽象 Galois 圏理論は完成**: `PreGaloisCategory`+`FiberFunctor`+pro 表現可能性+**`functorToContAction : C ⥤ ContAction FintypeCat (Aut F)` の圏同値**(= SGA1 V Th 4.1 級)[D6]+**`IsFundamentalGroup`**(π₁ の公理的特徴付け)[L23]。⟹ **割り付け表 §9 確認事項 2(「TB1 の下に置く SGA1 V Th 4.1 級の T1 公理の可否」)は前提が変わった**: 抽象段は公理でなく **M(Mathlib 供給)** にできる。司法問題として残るのは具体段(B-i/B-ii)のみ。
2. ★ **アフィン(環)版は繊維関手まで既にある**: `CommAlgCat.FiniteEtale R` 圏+`FiniteEtale.fiber`(幾何点 Ω での繊維関手)+分離閉上の反同値 `equivOfIsSepClosed` [D4]。
3. 体側の型は立つ: `Field.absoluteGaloisGroup`(Krull 位相群)[D2]・`InfiniteGalois`(profinite 性)[D3]・`IsGaloisGroup`(**環拡大のガロア群**への一般化・105 件・PR #30791)[L35][G7]。
4. 群論側: `profiniteCompletion`(普遍性つき)[D12] — **F̂₂ を `profiniteCompletion(FreeGroup (Fin 2))` として定義する**ことは今日の Mathlib で書ける(TB3 の**主張**= π₁ との同型は依然 B-v)。
5. 数論側の慣性・分岐の部品: RamificationInertia 系(e/f・塔の乗法性・Galois 一様値・Frobenius 系)[L26][L27]。

### 3.3 代替定式化の材料(**判断は司令塔に留保** — 列挙のみ)

- **(a) 抽象パラメータ化**: 橋 (5′) の幾何入力を「Galois 圏 C+fiber functor F+Aut F」の抽象データに置き、TB1 を「具体圏(U_ℚ̄ の有限エタール被覆)がこのデータを与える」という 1 点に集約する書き方。圏同値の段は M [D6] で賄われ、公理候補は具体段だけに縮む。⚠ ただしその 1 点の公理化は v1.3(TB1 は形式化補題)と正面衝突するため、**採るなら方針の司法判断が要る**。
- **(b) アフィン内製ルート**: U = P¹−{0,1,∞} は**アフィン**(Spec ℚ[t, 1/t, 1/(t−1)])。ゆえにスキーム版を待たず、`CommAlgCat.FiniteEtale A`(既在 [D4])に **PreGaloisCategory インスタンスを与える工房補題群**+既在の `FiniteEtale.fiber` で「π₁^ét(U) := Aut Fib」を Mathlib の枠内で**定義**できる可能性がある。Mathlib 不在部分はこのインスタンス証明(繊維関手の exactness 検証一式)に局在する。⚠ 規模は小さくない(実質「アフィンスキームのエタール π₁」の内製)— 着工判断の材料としてのみ列挙。
- **(c) TB3 の右辺の先行定義**: F̂₂ = `profiniteCompletion(FreeGroup (Fin 2))` を定義として先に固定し、TB3 の言明を「π₁ 側との同型」だけに最弱化する(公理・補題の言明整備が橋の完成を待たずに進む)。
- **(d) EXSEQ-LIM の極限段の先行形式化**: 骨子の群論部分(逆極限の完全性・stab 系)は `ProfiniteGrp.limit` API で幾何と独立に書ける可能性(LB-6 の紙債務 2 件の解消が先なのは不変)。
- **(e) 環版ガロア群の活用**: `IsGaloisGroup`(RingTheory)[L35] は「環拡大+群作用+固定環」の語彙で Galois 被覆を記述する — (b) の被覆記述・LB-9 の CRT/完備化段との接続部品。
- **(f) 現状維持(待ち)**: issue #16890 の進行を監視し、スキーム版 π₁ の着地まで B は保留のまま(割り付け表 §7 の判定を維持)。

> **本稿の判定**: 3.1 の欠けにより、**割り付け表の結論「ブロック B は着工不可」は版 pin 503b1a28 でも不変**。変わったのは待ちの**内訳** — 「エタール π₁ の基盤が丸ごとない」ではなく「**抽象層は完成・アフィン層は圏+繊維関手まで済み・スキーム層と接基点だけがない**」。(a)〜(f) の選択は司令塔裁定。

---

## 4. 調査方法と限界(UNKNOWN 規律)

1. **方法**: ①Loogle 名前検索(Mathlib master・2026-08-05 照会・JSON エンドポイント)②mathlib4_docs 頁の精読(全頁 source link の commit `503b1a2818938506db0e99d814816c83e9c054a9` を確認)③GitHub API(ディレクトリ一覧・issue/PR 検索)④一般 Web 検索(外部プロジェクト)。コード実行なし・lean/ 非接触。
2. **「なし」判定の限界**: 名前検索は「その部分文字列を名前に含む宣言がない」ことの確認であり、**別名での存在を排除しない**。本稿の「なし」は {名前検索 0 件+関連モジュールのファイル一覧+追跡 issue} の三角測量による。負の探索結果は非存在の証明ではない。
3. **未確認 2 点(正直申告)**: ①FLT project の Ẑ 実装ファイルの現行ツリー所在(blueprint に定義節はある [E2] が、FLT/ 直下一覧 [G5] に該当名なし — 下位ディレクトリは未走査)②`CommAlgCat.FiniteEtale` への PreGaloisCategory 接続が他モジュールに存在する可能性(検索範囲では無しだが悉皆ではない)。
4. **鮮度**: 本稿の全判定は 2026-08-05・commit 503b1a28 に相対化される。**Mathlib は高速に動く**(例: 連続コホモロジー・環版ガロア群・円分分岐公式はいずれも比較的新しい着地)。着工時 pin での再判定を必須とする(v1.6-2)。

---

## 5. URL 台帳(全確認 URL)

### 5.1 Loogle 照会(Mathlib master・2026-08-05)

| # | 照会 | 結果要点 |
|---|---|---|
| L1 | https://loogle.lean-lang.org/json?q=%22braid%22 | 473 件・全て BraidedCategory 圏論(braid 群なし) |
| L2 | https://loogle.lean-lang.org/json?q=%22BraidGroup%22 | **0 件** |
| L3 | https://loogle.lean-lang.org/json?q=%22wreath%22 | 44 件・RegularWreathProduct/Iterated のみ |
| L4 | https://loogle.lean-lang.org/json?q=%22ProfiniteGrp%22 | 100 件・圏+limit 一式 |
| L5 | https://loogle.lean-lang.org/json?q=%22ProfiniteCompletion%22 | 32 件・lift/lift_unique/adjunction |
| L6 | https://loogle.lean-lang.org/json?q=%22ZHat%22 | **0 件** |
| L7 | https://loogle.lean-lang.org/json?q=%22cyclotomicCharacter%22 | 26 件(modular+p 進) |
| L8 | https://loogle.lean-lang.org/json?q=%22absoluteGaloisGroup%22 | 6 件 |
| L9 | https://loogle.lean-lang.org/json?q=%22PreGaloisCategory%22 | 241 件 |
| L10 | https://loogle.lean-lang.org/json?q=%22FiniteEtale%22 | 30 件・全て RingTheory.Etale.Finite |
| L11 | https://loogle.lean-lang.org/json?q=%22Schreier%22 | 24 件・全て Quiver.SchreierGraph |
| L12 | https://loogle.lean-lang.org/json?q=%22PresentedGroup%22 | 31 件・toGroup/unique あり |
| L13 | https://loogle.lean-lang.org/json?q=%22SemidirectProduct%22 | 88 件 |
| L14 | https://loogle.lean-lang.org/json?q=%22krullTopology%22 | 7 件 |
| L15 | https://loogle.lean-lang.org/json?q=%22groupCohomology%22 | 395 件・H0/H1/H2 系 |
| L17 | https://loogle.lean-lang.org/json?q=%22fundamentalGroup%22 | 113 件・**AlgebraicGeometry ゼロ** |
| L18 | https://loogle.lean-lang.org/json?q=%22AutEquivUnits%22 | 3 件(ZMod.AddAutEquivUnits) |
| L19 | https://loogle.lean-lang.org/json?q=%22IsFreeGroup%22 | 45 件 |
| L20 | https://loogle.lean-lang.org/json?q=%22nflation%22 | 1 件(BourbakiWitt のみ = **inf-res 不在**) |
| L21 | https://loogle.lean-lang.org/json?q=%22ilbert90%22 | Hilbert90 モジュール確認 |
| L22 | https://loogle.lean-lang.org/json?q=%22functorToAction%22 | 14 件・full+faithful |
| L23 | https://loogle.lean-lang.org/json?q=%22IsFundamentalGroup%22 | 8 件 |
| L24 | https://loogle.lean-lang.org/json?q=%22autEquivPow%22 | 3 件(Cyclotomic.Gal) |
| L25 | https://loogle.lean-lang.org/json?q=%22IsEtale%22 | 6 件(うち AlgebraicGeometry 1) |
| L26 | https://loogle.lean-lang.org/json?q=%22ramificationIdx%22 | 126 件・塔乗法性・円分明示公式 |
| L27 | https://loogle.lean-lang.org/json?q=%22ramificationIdxIn%22 | 12 件・**Rat.ramificationIdxIn_eq の型取得** |
| L28 | https://loogle.lean-lang.org/json?q=%22Coxeter%22 | 207 件・braidWord は Coxeter 系 |
| L29 | https://loogle.lean-lang.org/json?q=%22ubgroupIsFree%22 | 1 件(subgroupIsFreeOfIsFree) |
| L30 | https://loogle.lean-lang.org/json?q=Finite.injective_iff_bijective | 存在確認(Data.Fintype.Card) |
| L31 | https://loogle.lean-lang.org/json?q=%22IsFiniteEtale%22 | **0 件** |
| L32 | https://loogle.lean-lang.org/json?q=%22FreeGroupBasis%22 | 21 件・card/rank 系 0 |
| L33 | https://loogle.lean-lang.org/json?q=Subgroup.rank_le_index_mul_rank | 存在確認(GroupTheory.Schreier) |
| L34 | https://loogle.lean-lang.org/json?q=%22ontinuousCohomology%22 | 31 件(ContCohomology 3 モジュール) |
| L35 | https://loogle.lean-lang.org/json?q=%22IsGaloisGroup%22 | 105 件(RingTheory+FieldTheory) |
| L36 | https://loogle.lean-lang.org/json?q=%22Algebra.Etale%22 | 28 件(RingTheory.Etale.Basic) |

### 5.2 mathlib4_docs(全頁 commit 503b1a28 確認済み)

| # | URL |
|---|---|
| D1 | https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/Cyclotomic/CyclotomicCharacter.html |
| D2 | https://leanprover-community.github.io/mathlib4_docs/Mathlib/FieldTheory/AbsoluteGaloisGroup.html |
| D3 | https://leanprover-community.github.io/mathlib4_docs/Mathlib/FieldTheory/Galois/Profinite.html |
| D4 | https://leanprover-community.github.io/mathlib4_docs/Mathlib/RingTheory/Etale/Finite.html |
| D5 | https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/NumberField/Cyclotomic/Ideal.html |
| D6 | https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/Galois/Equivalence.html |
| D7 | https://leanprover-community.github.io/mathlib4_docs/Mathlib/GroupTheory/FreeGroup/NielsenSchreier.html |
| D8 | https://leanprover-community.github.io/mathlib4_docs/Mathlib/RepresentationTheory/Homological/GroupCohomology/Hilbert90.html |
| D9 | https://leanprover-community.github.io/mathlib4_docs/Mathlib/FieldTheory/KummerExtension.html |
| D10 | https://leanprover-community.github.io/mathlib4_docs/Mathlib/RingTheory/Etale/Basic.html |
| D11 | https://leanprover-community.github.io/mathlib4_docs/Mathlib/GroupTheory/PresentedGroup.html |
| D12 | https://leanprover-community.github.io/mathlib4_docs/Mathlib/Topology/Algebra/Category/ProfiniteGrp/Completion.html |

### 5.3 GitHub・外部

| # | URL | 用途 |
|---|---|---|
| G1 | https://github.com/leanprover-community/mathlib4/issues/16890 | エタール site+π₁ の追跡 issue(open) |
| G2 | https://api.github.com/repos/leanprover-community/mathlib4/contents/Mathlib/CategoryTheory/Galois | Galois/ 11 ファイル一覧 |
| G3 | https://api.github.com/repos/leanprover-community/mathlib4/contents/Mathlib/RepresentationTheory/Homological/GroupCohomology | inf-res ファイル不在の確認 |
| G4 | https://api.github.com/repos/leanprover-community/mathlib4/contents/Mathlib/AlgebraicGeometry/Morphisms | Morphisms/ 38 ファイル一覧 |
| G5 | https://api.github.com/repos/ImperialCollegeLondon/FLT/contents/FLT | FLT 直下一覧(ZHat 該当名なし) |
| G6 | https://github.com/leanprover-community/mathlib4/pull/16993 | Galois group is profinite(merged) |
| G7 | https://github.com/leanprover-community/mathlib4/pull/30791 | IsGaloisGroup の環への一般化(merged) |
| E1 | https://github.com/ImperialCollegeLondon/FLT | FLT project(外部) |
| E2 | https://imperialcollegelondon.github.io/FLT/blueprint.pdf | FLT blueprint(ℤ̂ の定義節・検索結果由来) |
| E3 | https://www.hannahfechtner.com/finallyyy.pdf | 「Braids in Lean」(2024-12・外部・検索結果由来) |

---

## 6. 出所

| 節 | 出所 |
|---|---|
| 需要側 | `docs/notes/lean_p1_allocation_plan_v1.md`(§4 公理台帳・§7 着工可否・【LP1-GAP-1】)/ `docs/notes/lean_axiom_policy_v1.md`(v1.3/v1.4/v1.6)/ `docs/状態.md` 施策 9(裁定 531) |
| 供給側 | §5 の URL 台帳(Loogle 36 照会・docs 12 頁・GitHub 7 点・外部 3 点) |
