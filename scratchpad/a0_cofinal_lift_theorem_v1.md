# A0 と「cofinal な両立 lift」— 二つの塔の分離・有限厳密性定理・König 境界(候補 paper note v1)

Author: Fable(数学者・Claude 側)/ 2026-09-03
Status: candidate paper note.  `verified=false`(Lean なし).  MEMBER / NONMEMBER / COMMON / fake / Ihara の宣言なし.
GHA・production・git 不使用.  機械計算は scratchpad の小 GAP 検算 2 本のみ(§9).
宛先: 司令塔(裁定 1980 の発注「cofinal 両立 lift の定理 or 有限条件への還元 or 障害の同定」)・Sol(監査).

```text
VERDICT (3 行):
 (1) A0 本体は cofinal 定理を必要としない.  A0 は次元 |Δ|+1 = 357,128,353 の一つの有限線形所属問題
     (v405 (4.2) / v1 §1) であり, 特性商の塔 504→2,016→54,432→Q₀→… は「その一問題の商による必要条件の有限列」.
     頂上(H ブロックは e3 = Q₀×pc3 の水準, さらに P ブロックと ν)で MEMBER ⟺ A0 = 1 (定理 A).
     逆極限・コンパクト性・分離性(LERF)は A0 のどこにも入らない.
 (2) Sol の全 note の「COFINAL / SOURCE-KERNEL SURJECTIVITY: NOT PROVED」は A0 の上の別の塔 —
     relative Frattini 塔 K_{r,n+1} = Φ₃(K_{r,n}) (v145) の rung n ≥ 1 = 「Ω₀ より小さい核をもつ refinement」(v460 §4)
     — についての行であり, A0 (= rung 0→1) の閉鎖条件ではない(逐語 §2).
 (3) その塔(T2)では: 各段の完全解集合 S_n が全て非空 ⟺ 逆極限非空(König, v169 Thm 4.1 = 自動).  足りないのは
     「全段非空」そのものであり, かつ rung 1 の群は |E_{3,1}| ≥ 3^{39,680,929} で計算不能(命題 C).  ゆえに
     「cofinal な有限段の両立 MEMBER 系」は測定可能な前提ではなく, T2 を閉じる定理は必然的に rung-0 データだけを
     前提にする形(登録済み: v174 pointed Neumann / v191 universal word-pair)でなければならない.  その存在定理
     (v220 の U3)は本稿でも閉じない — 障害の型と必要な定理の形を §5 に同定した.
一文 gap: 「T1(A0 内の有限塔)を頂上まで登れば A0 = 1 は決まる — 足りないのは頂上までの残り 19 grade 決定 + P ブロック
     + ν/直接 replay だけ.  一方 A0 = 1 から証人へは, 測定不能な無限塔 T2 の全段非空性が要り, それは rung-0 の
     有限恒等式(v191 (2.2) / v174 (2.1))の存在という未証明の定理(U3)に還元されたまま.」
```

研究者向け要約(日本語): 「有限の塔を登り切っても A0 は cofinal 定理がないと閉じない」という読みは, Sol の claim boundary の
「cofinal」が指す対象(A0 の上に続く無限塔)と, A0 の内部の有限塔(504→…→Q₀→e3)を同一視したことから来ている.  A0 は
Δ(位数 3.57×10⁸)の relation module 上の一つの有限線形問題で, 塔はその商による必要条件を安い順に並べたもの.  頂上で
MEMBER なら A0 = 1 で, 逆極限も分離性も要らない(定理 A).  本当に開いているのは A0 の**上**の無限塔で, そこは
(i) 各段が非空なら極限も非空(König)は自動だが, (ii) 各段の非空性を無限に確かめることは原理的に不可能(rung 1 の群の
位数が 3 の 4 千万乗以上), だから (iii) Sol の路線どおり「rung 0 で成り立つ一つの有限恒等式が全段を同時に降ろす」型の
定理が唯一の出口 — その恒等式の存在(U3)が本当の律速.  本稿はそれを証明しない.  何が障害で, どんな定理の形が
要るかを同定し(§5), A0 を閉じるための有限検査条件(§6)と, 閉じたとき次段へ渡す物(§7)を書いた.

---

## 0. 記号(正典逐語 → 略記)

- `F = F(x,y)`, `Θ: F ↠ Δ` joint roof, `Ω = ker Θ = ⟨⟨r_1..r_44⟩⟩_F`, `|Δ| = 357,128,352 = 2⁵·3¹³·7`, 座標核 `(9,9,9,9,9,1,1,1,3,3)`
  (v1 P1, task176 cross-checked).  `M := H_1(Ω;F_3) = Ω/Ω'Ω³`, `dim M = |Δ|+1 = 357,128,353`(v1 (1.1)).
- `P_3 = PB3 = ⟨a,b,c | 2 relators⟩`, `P_4 = PB4`.  pinned marked quotients `E_3 = e3`, `E_4 = e4`(v145 (1.1)).
  `e3 = Q_0 × pc3`(v1 P6; 本稿 GAP: `|e3| = 119,042,784 = |Q_0|·81`, 直積そのもの), `|Q_0| = 1,469,664`, `|pc3| = 81`.
- 11 occurrence: 6 PB3 slot(H1: fyz,fxz,fxy / H2: fuy,fxy,fux)+ 5 PB4 slot(v2 §2.3, v405 §1).
- 物理空間 `Z̄ = Y_3^{(1)} ⊕ Y_3^{(2)} ⊕ Y_4^{cen} ⊕ k²`(v405 (3.3)), `Y_3 = k[e3]³/D_3`(v401), `k = F_3`.
- 標的 `T = −Fox(hex_1(g760)) ⊕ −Fox(hex_2(g760)) ⊕ −Fox(pent(g760)) ⊕ (0,0)`(v1 P3), `g760 = W2(W3⁻¹W2)⁸y³⁶x⁻¹⁰⁸`.
- `Φ := Q_ph L̂_g Ĵ : M → Z̄`(線形), `C := Φ(M)`(v1 §1).  正規化指数 `ν : M → k²`(v399).
- Relative Frattini: `Φ_3(K) = K³[K,K]`, `K_{r,n+1} = Φ_3(K_{r,n})`, `E_{r,n} = P_r/K_{r,n}`, `K_{r,0} = ker(P_r → E_r)`(v145 (1.2)–(1.3)).

## 1. A0 の正確な主張(pin)

### 1.1 逐語

- **v405 (4.2)**(A0 方程式): 「The exact A0 equation is now `−T̄ ∈ L̄_g(W̄) + D̃_0`」, `W̄ = span_k{ρ̄(a) Ĵ_g(r_i)‾ : i=1..44, a ∈ F(x,y)} ≤ Ū`
  (v405 (2.1)), `Ū = ⊕_{o∈𝒪} C_o ⊕ k²`(11 tagged occurrence + ν, v405 (1.1)), `D̃_0 = (0,0,D_0,0)`(六 action 行, v405 (4.1)).
  **v405 Theorem 4.1 (COMPLETE FINITE A0 SELECTOR)**: 「decides the A0 equation (4.2) after finitely many strict rank rises」.
- **v1 §1**: 「the A0 equation v405 (4.2) is `−T̄ ∈ D̃_0 + C`」, `C = Φ(M)`, `dim M = |Δ|+1`(Schreier).
- **v145 Theorem 2.2 (WHAT A TASK179 COMMON WORD SETTLES)**: 受理された COMMON_WORD `f^{(1)} = g760 c_0` について
  「both hexagon relation words of `f^{(1)}` lie in `K_{3,1} = Φ_3(K_{3,0})`, and its printed-order pentagon relation word lies in
  `K_{4,1} = Φ_3(K_{4,0})`」, i.e. `f^{(1)}` は `E_{3,1} = P_3/K_{3,1}`, `E_{4,1} = P_4/K_{4,1}`(v145 (2.7))で hexagon/pentagon を満たす.
  「Thus task179 is the first universal elementary-abelian relative lift above the pinned `E_3/E_4` window」.
- **v145 Lemma 2.1 (2.3)–(2.4)**: `K/K³[K,K] ≅ ker D_1/im D_2`(`F_3[E]`-加群同型), `∇w ∈ im D_2 ⟺ w ∈ Φ_3(K)`.
- **v220 §20 表**: 「A0 | task192 actual exact word | positive terminal + independent acceptance: 0/1」.

### 1.2 A0 = relative Frattini 塔の rung 0 → 1 の一つの有限線形問題

v145 Lemma 2.1 を `E = e3`(H1, H2 ブロック)と `E = e4`(P ブロック)に適用すると, A0 の意味は正確に

```text
A0 = 1  ⟺  ∃ c ∈ Ω :  hex_b(g760·c) ∈ Φ_3(K_{3,0}) (b=1,2),  pent(g760·c) ∈ Φ_3(K_{4,0}),  ν(c) = 0
        ⟺  ∃ [c] ∈ M :  Φ([c]) ≡ −T̄ (mod D̃_0)                                   (v405 (4.2), Fox 線形化)
```

右辺は **有限次元 `F_3`-空間 `M`(dim 3.57×10⁸)上の線形所属** である.  Fox 積公式により `c ↦ Fox(hex_b(g760 c)) − Fox(hex_b(g760))` は
`[c] ∈ M` の線形関数(v1 P4, v396 (1.5)); `hex_b(g760 c)` は `e3` で 1 なので Fox 行は `ker D_1` に入り, `im D_2 = D_3` で割った類が
`H_1(K_{3,0};F_3)` の元 = 「`Φ_3(K_{3,0})` に落ちるか」の唯一の障害(Lemma 2.1).  したがって **A0 は群 `Δ`(有限)・加群 `M`(有限次元)・
標的空間 `Z̄`(有限次元)だけで完結し, 無限対象を一切含まない**.  v405 Thm 4.1 はまさにその有限決定手続きである.

### 1.3 二つの塔(本稿の中心的区別)

```text
T1 (A0 の内部・有限):  Z̄ の商への射影 π_{Q'} で得る必要条件の列.  H ブロック側の標的群 e3 の特性商の塔:
      P=PSL(2,8) (504)  ←  Q_1 = Q_0/(1×G9') (2,016)  ←  Q_2 = Q_0/(1×(G9')³) (54,432)  ←  Q_0 (1,469,664)
                        ←  e3/Φ(pc3) (39,680,928)      ←  e3 (119,042,784)  [頂上 = A0 の H ブロック]
      (v2 addendum §3.5 / v441 §6 に本稿 GAP の 2 段を追加: pc3 は exponent 3, class 2, Φ(pc3)=pc3' 位数 3, Frattini 列 81→3→1)
      P ブロック側の塔: 未設計(§6 (P1)–(P3)).   ν: 座標 1 本(v460 で塔一様に処理済).
      各段 Q' で「MEMBER」= π_{Q'}(T) ∈ π_{Q'}(C + D̃_0)  (chord/kernel 形 = closure 形, errata R2).
      各段は厳密な必要条件: NONMEMBER at Q' ⟹ A0 = 0.   頂上 MEMBER ⟺ A0 = 1  (定理 A).

T2 (A0 の上・無限):   relative Frattini 塔 (v145 (1.3)).  rung n の問題 = 「f^{(n)} = g760 c_0 ⋯ c_{n−1} の hexagon/pentagon を
      K_{r,n+1} = Φ_3(K_{r,n}) に落とす c_n ∈ Ω_n」.  rung 0 = A0.  rung n の群 E_{r,n} は n ≥ 1 で計算不能な大きさ(命題 C).
      「cofinal」「compatible lift」「source-kernel surjectivity」は全てここの語(§2).
```

図式(T1 の各段 MEMBER が A0 のどの必要条件か):

```text
  M ──Φ──▶ Z̄ = Y_3^{H1} ⊕ Y_3^{H2} ⊕ Y_4^{cen} ⊕ k²        A0: −T̄ ∈ Φ(M) + D̃_0
  │            │ π_{e3→Q'} (H ブロック; κ_* 型, v1 (3.1))         必要条件 (Q'): π_{Q'}(−T̄) ∈ π_{Q'}(Φ(M)) + 0
  │            ▼
  │        Y-bar_3^{H1}(Q') ⊕ Y-bar_3^{H2}(Q') ⊕ k²          Q' = P, Q_1, Q_2, Q_0, e3/Φ(pc3), e3
  │  (v1 定理 B/C は Q'=Q_0 で seed 1,2 が 0 になる/T が V0 像の外, の主張; v2 §4.1: P ブロックは π で落とす)
  └─ 頂上 Q' = e3 で H ブロック MEMBER ⟹ 解集合 c_H + (ker Φ_H ∩ ker ν) 上で P ブロック方程式(有限)⟹ A0.
```

## 2. 「cofinal」「compatible lift」「source-kernel surjectivity」の逐語

| 語 | 正典逐語 | 指す対象 |
|---|---|---|
| cofinal | v145 status: 「proves that the resulting relative Frattini tower is cofinal on the marked pro-3 lane」; v396 §7: 「this finite A0 closure does not prove that **every cofinal rung** has a nonempty accepted set. It is a faster finite base-word constructor, not the missing inverse-limit homotopy」; v460 §4: 「does not … prove compatibility for **refinements whose kernel is smaller than `Omega_0`**. In particular it is not by itself the inverse-limit homotopy requested for all cofinal refinements」, claim 行「REFINEMENTS BELOW Omega_0 / COFINAL LIFT: OPEN」 | T2 の rung n ≥ 1(核 ⊊ Ω₀ の refinement) |
| compatible (cofinal) lift | v395 Thm 4.1: 「`c_∞ = (c_n)` is one coherent correction in the inverse limit」(前提: 全 edge で (3.4)); v169 Thm 4.1: 「If `𝒮_n ≠ ∅` for every `n`, then `lim← 𝒮_n ≠ ∅`」+「compactness removes the **compatibility-choice** problem, not the **nonemptiness** problem」; v220 §1.1: 「全ての有限 GT-shadow へ整合的に降りる一つの profinite GT element を構成する」 | T2 全段の解の整合族 = profinite 元 |
| source-kernel surjectivity | v395 (2.4) `K^D_n = ker r^D_n`, `K^L_n = ker r^L_n`; (3.4) 「`B_{n+1}(K^D_n) = K^L_n`」= UNIVERSAL ONE-STEP CRITERION(「provided `r^D_n` is onto on the legal source」); 「The equality in (3.4), not mere endpoint surjectivity of `B_{n+1}`, is the precise content of the proposed relative-dihedral successor theorem」; v465 §2.2: 「(2.3) proves membership in the registered physical fibre. It does **not** by itself prove membership in a source relative kernel such as `K^D_n = ker r^D_n`. That stronger typing requires a separate direct source-reduction replay」; v466 §5: 「The source-kernel assertion required by **a later v395 edge** remains a distinct direct source-reduction replay」 | v395 の再帰的 selector(Thm 4.1)が要る**十分**条件; 各 edge の有限 rank test |
| 「6 grade MEMBER ⟹ 54,432 で等式」の境界 | v479 §6: 「Six accepted MEMBER updates with direct replays imply equality at order 54,432 because `I^7 = 0` … It does not imply the second rung or any cofinal lifting theorem」 | T1 の rung 3 の完成 = T1 内の一段 |

読み: Sol の boundary は一貫して「A0(T1)の有限閉鎖」と「T2 の inverse-limit homotopy」を分けている.  「A0 本体が cofinal 定理を要する」
とは書かれていない(v396 §7 は反対に「finite A0 closure」と呼ぶ).

## 3. 定理 A(A0 の有限厳密性 — T1 に逆極限は入らない)

**設定.** `W := Z̄`(有限次元), `A := Φ : M → W`(線形), 標的 `t := −T̄`, 境界 `D̃_0 ≤ W`.  A0 ⟺ `t ∈ A(M) + D̃_0`.
`W ⊇ F^0 ⊋ F^1 ⊋ ⋯ ⊋ F^m = 0` を `W` の任意の減少フィルトレーション(部分空間の列)とし, `C_d : M → W/F^d`, `t_d := t mod F^d`,
`S_d := {m ∈ M : C_d(m) ≡ t_d mod (D̃_0 + F^d)/F^d}`(精度 `d` の解集合)とおく.

**定理 A.**
(i) `S_{d+1} ⊆ S_d`(有限集合の降下列); `S_m` = A0 の解集合.  特に **A0 = 1 ⟺ `S_m ≠ ∅`**, **`S_d = ∅` for some `d` ⟹ A0 = 0**.
(ii) (v441 Cor 2.2 の一般形) `S_d ≠ ∅` とし `c ∈ S_d` を任意に取る.  `D_d := ker C_d`(下位解の差の空間), `K_d := (A(D_d) + D̃_0 + F^{d+1}) ∩ F^d / F^{d+1}`,
`ρ_d := (t − A(c)) mod F^{d+1} ∈ F^d/F^{d+1}`.  このとき `S_{d+1} ≠ ∅ ⟺ ρ_d ∈ K_d`.  条件は `c` の取り方に依らない.
(iii) (ブロック逐次) フィルトレーションを `F^1 = 0⊕0⊕Y_4^{cen}⊕k²`(H ブロックを先に見る), その下に P ブロック・ν のフィルトレーションを続けても (i)(ii) は
そのまま成り立つ.  すなわち「H ブロックを頂上まで解く → その解集合 `c_H + (ker Φ_H)` 上で P ブロックと ν を解く」は厳密.
(iv) 特性商の塔は (i) の特別な場合: `Q' ← Q''` が `e3` の特性商で occurrence 自己同型に保たれるなら, `π_{Q'} = π_{Q''}` を経由する射影が誘導され
(v2 §4.1 の可換図式 `A_g^{Q'} ∘ ρ_* = ρ_* ∘ A_g^{Q''}` と同型), `F^d := ker(π_{Q'})` 型の部分空間列が得られる; 各段の中の grade 分解(v441 (1.6)–(1.7))は
`F^d = I^d W` によるその細分.  したがって **塔の各段 MEMBER は A0 の必要条件であり, 頂上 `Q' = e3`(H ブロック)+ P ブロック + ν の MEMBER が A0 = 1 と同値**.
(v) コンパクト性・逆極限・部分加群の副有限閉包・LERF 型の分離性は一切使われない: `M`, `W` が有限次元だから.

*証明.* (i) `C_{d+1}(m) ≡ t_{d+1}` なら mod `F^d` に落として `C_d(m) ≡ t_d`.  `F^m = 0` で `S_m` は A0 の解集合そのもの.
(ii) `S_d = c + D_d`(アフィン).  `S_{d+1} ≠ ∅ ⟺ ∃δ ∈ D_d, ∃b ∈ D̃_0 : A(c+δ) + b ≡ t mod F^{d+1}`.  `A(c) ≡ t mod (D̃_0 + F^d)` なので
`t − A(c) − b_0 ∈ F^d` なる `b_0 ∈ D̃_0` があり, 条件は `ρ_d := (t − A(c) − b_0) mod F^{d+1} ∈ (A(D_d) + D̃_0) mod F^{d+1}` かつ左辺が `F^d/F^{d+1}` の元,
すなわち `ρ_d ∈ K_d`.  `c' = c + δ'`(`δ' ∈ D_d`)に替えると `ρ'_d = ρ_d − A(δ')` は `K_d` を法として不変.
(iii) 任意の減少フィルトレーションで (i)(ii) は成り立つ(部分空間列以外の仮定を使っていない).  法的像 `A(D_d)` を「商での閉包」として計算するために
必要なのは, 商 `W/F^d` への射影が occurrence-separated module 上の 4 actor の半線形作用と可換なこと; ブロック射影(H のみ・ν のみ)は tag ごとに定義された
作用 `ρ̄_o(a)`(v405 (1.6))と可換であり, ν の作用は自明(v405 §1)なので満たす.
(iv) 特性性から 5 個の occurrence 自己同型 `ψ_o` は `Q''→Q'` を保ち(v2 §3.5 の議論), 前置詞・Jacobian・class map は押し出される(v2 §4.1).  よって
`π_{Q'} = ρ'_* ∘ π_{Q''}` が線形に誘導され, その核は `W` の部分空間.  各段の内部で `1 → V → Q'' → Q' → 1`(`V` 初等アーベル)なら `I^d W` の列で細分できる
(v441 §1).  (v) 明白. ∎

**系 A.1(残り工程の勘定, H ブロック).**  現状(地図 2026-09-03 追記): rung 1,2 MEMBER(cross-checked), rung 3 = grade 1/6(限定つき cross-checked).
残り: rung 3 の grade 2–6(5)+ rung 4 `Q_0`(`V = (G9')³ ≅ C_3³`, 6)+ rung 5 `e3/Φ(pc3)`(`V = pc3/Φ(pc3) ≅ C_3³`, `Q_0` の共役作用は自明(直積), 6)
+ rung 6 `e3`(`V = Φ(pc3) = pc3' ≅ C_3` 中心, `k[u]/(u³)`, 正 grade 2)= **19 grade 決定**.  その後 P ブロック(塔未設計・§6)と ν・直接 replay.
数値根拠: 本稿 GAP(§9): `pc3` order 81, `AbelianInvariants = [3,3,3]`, exponent 3, class 2, Frattini 列 `[81, 3, 1]`; `ker(e3 → Q_0) = 1×pc3`.
occurrence 自己同型による保存: `ker(Δ → e3)` は 5 座標で一致(errata R6)し `ker(Δ → e3 → Q_0) = Γ` も 5 座標で一致(v1 Lemma 3.1)ので, 誘導される
`e3` の自己同型は `1×pc3` を保つ; Frattini 列は特性的ゆえその自己同型に保たれる(紙).  各段の実 extension データ(transversal・cocycle・`V` 上の作用)は
**未実体化**(v441 §7 の gate 2–3 に相当).

**注 A.2(NONMEMBER 側の非対称).**  MEMBER は部分 span(routed span・targeted CEGAR)で証明してよい(解は解).  NONMEMBER は `K_d` を完全な `D_d` で
計算した上でのみ有効(v441 §3 末尾, v479 §5「TARGETED MEMBER = COMPLETE PRESENTATION: FORBIDDEN」).  定理 A (ii) の `D_d = ker C_d` は下位の
**全**解の差であることに注意 — 「選んだ下位解の fibre だけ」では `K_d` を小さく見積もる.

## 4. 定理 B(T2: König 境界・dead branch・計算不能性)

**設定.** rung `n` の解集合 `S_n := {c ∈ Ω_0/Ω_{n+1} : hex_b(g760 c) ∈ K_{3,n+1} (b=1,2), pent(g760 c) ∈ K_{4,n+1}, (登録 side gate)}`, ただし
`Ω_n := ∩_{slots} σ_o^{−1}(K_{r,n})`(joint kernel; `Ω_0 = Ω`).  `S_n` は有限.  制限 `r_n : S_{n+1} → S_n`(mod `Ω_{n+1}`)は well-defined
(`K_{r,n+2} ⊆ K_{r,n+1}`).  証人(v220 §1.1 の pro-3 lane 部分)= `lim← S_n` の元.

**定理 B.**
(i) (König; v169 Thm 4.1 の再掲) `lim← S_n ≠ ∅ ⟺ ∀n: S_n ≠ ∅`.  遷移写像は関手的に存在し, 「両立性」は自動.
(ii) (Mittag-Leffler 型の精密化) `S_n^∞ := ∩_{m ≥ n} r_{n,m}(S_m)`(eventually liftable な rung-n 解)とおくと `S_n^∞ = im(lim← S → S_n)`(有限集合の逆系では
像の交わり = 極限の像)であり, **証人 ⟺ `S_0^∞ ≠ ∅`**.  A0 = 1 で得た語 `c_0 ∈ S_0` が `S_0^∞` に入る保証はない: 「`c_0` を固定した fibre で rung n が
NONMEMBER」は証人問題の NONMEMBER ではない(dead branch).
(iii) (一様 lift) 全 edge で v395 (3.4) が成り立てば `r_n` は全射, よって `S_n^∞ = S_n` かつ **証人 ⟺ A0 = 1**.  (3.4) は各 edge で有限 rank test だが edge は無限個.
(iv) (class-specific の必要十分) 固定した `c ∈ S_n` の fibre `r_n^{−1}(c)` は `Ω_{n+1}/Ω_{n+2}` のアフィン部分空間で, 非空 ⟺ `ρ_{n+1}(c) ∈ im B_{n+1}(f)`,
`f = g760 c`, `B_{n+1}(f)([δ]) = Σ_o ε_o P_o(f)·[σ_o(δ)] ∈ ⊕_r H_1(K_{r,n+1};F_3)`.  これは rung `n+1` における「A0 と同形の有限線形所属」.

*証明.* (i) 有限集合の逆系: `S_n ≠ ∅` 全てなら, 各 `n` に頂点 `S_n`, 辺 `r_n` の有限分岐木は各深さに頂点をもち König で無限枝.  逆は明白.
(ii) 有限集合の逆系では `im(lim← S → S_n) = ∩_m r_{n,m}(S_m)`(標準; 各 `m` で `r_{n,m}(S_m)` は有限降下列で安定し, 安定値の元は各 `S_m` に
原像をもつので König を安定部分系に適用).  (iii) (3.4) は v395 Cor 3.2 により「every lower solution … can be lifted」と同値.  (iv) Fox 積公式:
`σ_o(δ) ∈ K_{r,n+1}` かつ `K_{r,n+1}/K_{r,n+2}` はアーベルなので `hex_b(f δ) ≡ hex_b(f)·Π_o (P_o σ_o(δ) P_o^{−1})^{ε_o}` mod `K_{r,n+2}` の類は
`[hex_b(f)] + Σ_o ε_o P_o·[σ_o(δ)]`; `[σ_o(δ)]` は `δ mod Φ_3(Ω_{n+1})` にのみ依存(`σ_o(Φ_3(Ω_{n+1})) ⊆ Φ_3(K_{r,n+1})`). ∎

**命題 C(rung 1 は計算不能).**  `P_3 = ⟨a,c⟩ × ⟨z⟩`(`z = abc` 中心; 2 生成自由部分群 `⟨a,c⟩` は `P_3/⟨z⟩ ≅ F_2` に同型に写る).  本稿 GAP: `e3` の中で
`⟨a,c⟩` の像は指数 3(`z3 ∉ ⟨a,c⟩`-像, `z3` は中心・位数 3), 位数 `39,680,928 = |Δ|/9`(= 5 つの E3 occurrence の context-image order, v220 Δ76 と一致).
よって `K_{3,0} ∩ ⟨a,c⟩` は自由群 `⟨a,c⟩` の指数 `39,680,928` の部分群で Schreier 階数 `39,680,929`, したがって

```text
dim_F3 H_1(K_{3,0};F_3) ≥ 39,680,929,     |E_{3,1}| = |e3| · 3^{dim H_1(K_{3,0};F_3)} ≥ 1.19×10⁸ · 3^{39,680,929}.
```

rung 1 の標的空間 `H_1(K_{3,1};F_3)` は次元 ≈ `|E_{3,1}|`.  **T2 の rung ≥ 1 は有限だが計算の対象にならず, 「全段 MEMBER」は測定可能な命題ではない.**
(Sol の v213/v216 の exponent-9・pro-Heisenberg 射影は rung n の**商への射影**(必要条件)であって rung そのものではない — v220 §8, §16 規則 5.)

**系 B.1(依頼された定理の位置づけ).**  「条件 (i)–(k) の下で cofinal な有限段の両立 MEMBER 系は A0 の解を与える」は:
- T1 に対しては定理 A(条件 = §6 の有限 gate; 「両立」は自動; 頂上 MEMBER = A0).
- T2 に対しては定理 B (i)(ii)(条件 = 全段の完全解集合が非空; 「両立」は自動)— しかしその前提は命題 C により**測定できない**.  ゆえに T2 を閉じる
  定理は「rung-0 で検査可能な有限条件 ⟹ 全段非空」の形でなければならず, 登録済みの候補は v174 Thm 2.1(`β − Ba = μβ`, `μ ∈ 𝔧` ⟹ `q_∞ = Σ μ^r a`,
  `B q_∞ = β`)と v191 Thm 2.1(word-pair `M` と boundary chain `q` の literal 等式 `ẽ − M d̃ = D̃_2 q` ⟹ 全 matched relative pro-3 quotient で `e_n = μ_n d_n`).
  両者は**十分**条件(v220 §14「v191 は sufficient theorem であり, 必要条件とは証明していない」).  その有限恒等式の存在(U3)が本当の open.

**注 B.2(依頼の「最小反例モデル」について).**  「有限段で全て MEMBER なのに極限で失敗する玩具例」は, 完全な有限解集合と自然な制限写像の逆系では
**存在しない**(定理 B (i)).  現実に起こり得る失敗は次の 3 型で, それぞれ玩具例を与える:
- (T-i) dead branch: `S_0 = {a, b}`, `S_1 = {a', b'}`(`a' ↦ a, b' ↦ b`), `S_2 = {b''}`(`b'' ↦ b'`).  全段非空・極限非空(`b` 枝)だが `a` を固定した
  探索は rung 2 で「NONMEMBER」を返す.  対策 = 定理 A (ii)/v441 Cor 2.2 のように**全下位解の差** `D_d` で fibre を作る(T1 では実装済み), T2 では
  v195–v196 の same-μ repair だけでなく rung-0 解の取り替え(`S_0` の別点)を許す設計(§8 Q4).
- (T-ii) 規約漂流: 段ごとに異なる chain map で「MEMBER」を出せば, それは異なる問題の解で, 遷移写像が存在しない(逆系でない).  実例 = 接頭辞規約の
  逸脱(裁定 1847/1850: own-prefix `ag` は 2,016 段まで不可視・54,432 段から可視).  対策 = 44 identity 列 gate(直接 Fox 列との entrywise 一致)を各段の
  標準検査に(既に express 済).
- (T-iii) 非 cofinal: pro-3 lane の逆極限は「核 ⊆ Ω₀ で `Ω₀/N` が 3 群」の商しか見ない.  玩具: `F = Z`, 条件「`c ≡ 1 (mod 2)`」は 3 冪商で不可視.
  R07 では v220 の B(mixed-prime)・C(perfect-core)gate がこれに当たり, T2 を閉じても Ihara には B, C が別途要る(v220 §16 規則 8).

## 5. 一様 lift 定理の形 — 障害の同定と, 要る定理

### 5.1 障害はどこに住むか

定理 B (iv) により, edge `n → n+1` の障害は `coker(B_{n+1}(f))` における残差 `ρ_{n+1}(f)` の類(class-specific), あるいは「`f` を `S_n` 内で動かしたときの
最良値」= `ρ_{n+1} mod (im B_{n+1} + 下位解差の像)`(定理 A (ii) の `K_d` と同形).  rung 0 の次元簿記(本稿の測定と正典値):

```text
source  dim M = |Δ|+1 = 357,128,353
H 標的  dim H_1(K_{3,0};F_3) ≥ 39,680,929  (×2 ブロック)   — source ≫ H 標的: H 部分だけなら全射は次元的には排除されない
P 標的  dim H_1(K_{4,0};F_3): UNKNOWN(PB4 の指数 |Δ| の部分群; χ(PB4)=0 なので指数比例の公式は無い; 測定可)
既知の非全射性: rung 1 (504) で dim A_g^G(K_G) = 405 < 2·(|G|+1) = 1,010 (v2 §4.2) — 標的の H_1 部分に対しても全射ではない.
```

つまり rung 0 でも `B_0` は全射でなく, A0 は本物の制約である.  同じことが各 `n` で起こるので, 「全 `n` で残差が像に入る」には**残差側の構造**(残差が
標的空間の任意の元ではないこと)が要る.

### 5.2 要る定理の形(推測を含む・明示)

(a) **一様 (3.4) 型**: 「`n ≥ n_0` で `B_{n+1}(K^D_n) = K^L_n`」.  各 edge は有限 rank test(v395 Cor 3.2)だが命題 C により `n ≥ 1` は測れない.  成立させ得る
構造は relation module の層再帰: `1 → Ω_{n+1} → Ω_n → V_n → 1`(`V_n = Ω_n/Ω_{n+1}`)の 5 項完全列(`F_3` 係数, `Ω_n` 自由)から
`H_1(Ω_{n+1})_{V_n} ≅ H_2(V_n;F_3) ≅ Λ²V_n ⊕ V_n`(奇素数の初等アーベル群), 標的側も同形の列(ただし `H_2(K_{r,n}) ≠ 0` の補正).  rung `n+1` の
`B_{n+1}` の `V_n`-共変部分は rung `n` の線形写像 `V_n → V_{r,n}`(= `B_n` の型)から `Λ²⊕id` で関手的に決まる — **推測**: この再帰で「共変部分の全射性/
残差の消滅」が `n = 0,1` から決まる形の定理が書ける可能性がある.  本稿では証明しない(【GAP-U1】).
(b) **残差の構造(syzygy)型**: 2 hexagon + 1 pentagon の線形化された欠陥 `(E_{H1}(f), E_{H2}(f), E_P(f))` が満たす恒等式(関係の間の関係).  pro-unipotent
設定では Furusho の「pentagon ⟹ hexagons」(associator)が知られる型の結果であり, もし B₄-proper/profinite 設定で線形化水準の含意
`E_P(f) ∈ (指定部分空間) ⟹ E_{H}(f) ∈ im B_H` があれば, H ブロックの塔登りは P ブロックに従属し, 一様性の証明対象が 1 ブロックに減る.
**【文献要請】**: (困難) relative pro-3 塔の各段で hexagon/pentagon 欠陥が満たす線形恒等式が要る.  (欲しい結果の型) (1) profinite/pro-ℓ GT に
おける pentagon ⟹ hexagon 型の含意(Furusho 2010 の profinite 版の有無, 条件), (2) GT 定義関係の「syzygy」— Fox 線形化水準で欠陥ベクトル
`(E_{H1},E_{H2},E_P)` が張る部分空間を制限する恒等式.  正典外につき自分では漁らない.
(c) **契約型(登録済み)**: v174 (2.1) `β − Ba = μβ`(`μ ∈ 𝔧`)/ v191 (2.2).  これは (a)(b) を経由せず, 「1 つの有限恒等式が全段の残差を `𝔧`-倍に縮める」ことで
(iii) の代わりに Neumann 級数で `lim←` の元を直接作る.  必要なのは rung-0 の有限データ `(a, μ)` または `(M, q)` の存在(U3)で, 現在 0/3(v220 表 A5–A8).

### 5.3 本稿の結論(定理の成否)

- 定理 A: **成立**(有限線形代数).  A0 に cofinal 定理は不要.
- 定理 B: **成立**(König/Mittag-Leffler).  「全段 MEMBER ⟹ 極限」は自動だが前提が測定不能(命題 C).
- 「cofinal 両立 lift」定理(T2 全段非空 ⟸ 有限条件): **本稿では閉じない**.  障害 = 各 edge の `coker B_{n+1}` における残差類(§5.1); 閉じる定理の型は
  §5.2 (a)(b)(c) のいずれか.  (c) が登録路線, (b) は文献要請, (a) は推測段階.

## 6. A0 を閉じるための有限検査条件(定理 A の条件 (i)–(k))と追加測定仕様

```text
(i)   塔の各段 Q'' → Q' の核 V が初等アーベル 3 群で, 5 つの E3 occurrence 自己同型(および P ブロックでは 5 つの PB4 occurrence 写像)に保たれる
      [GAP: ψ_o(V) = V; e3 側は v1 Lemma 3.1 + R6 + Frattini 列の特性性で紙で閉じるが, 実行 gate としても束縛(v441 §7 gate 1)]
(ii)  各段の extension データ: transversal・核値 cocycle・V 上の商作用・I^d の occurrence 保存・切り詰め代入 u_i ↦ Π(1+u_j)^{m_ji} − 1 (v441 §7 gate 2–3)
(iii) 44 seed の identity 列 = hexagon/pentagon 語の直接 Fox 列と entrywise 一致(44/44)を各段の標準検査に(規約 canary; T-ii 対策)
(iv)  法的像の完全性: MEMBER 判定に用いる span は部分でよいが, NONMEMBER 判定には完全 presentation 𝒫_d(44 seed reduction + 4r transition +
      queue exhaustion, v444 (2.2)–(2.3), v479 witness/presentation 二分岐)が必須
(v)   残差は composed root C_d(v465 (4.1))の直接評価から新規に計算(v479 (4.1)); lower/auxiliary 座標の dense 零検査; 「選んだ下位解」依存の
      残差を「K_d を法として」判定(定理 A (ii) — K_d は全下位解差の像)
(vi)  ν: 最終 root の指数対を整数で 0 に(v399/v460; 3 で割る前に整数検査, v441 §7 gate 7)
(vii) H ブロック頂上 = e3(rung 5: V = pc3/Φ(pc3) ≅ C_3³, rung 6: V = Φ(pc3) ≅ C_3 中心)の extension データ実体化 — 本稿 GAP で構造のみ確定
(viii) P ブロック: (P1) 標的群の同定(e4 の 5 座標 context 像; 本稿 GAP v2: 座標 6–8 の像は位数 |Δ| = 357,128,352(核 1, abinv [2,2,9,9] = Δ^{ab}),
      座標 9–10 は位数 119,042,784(核 C_3); 座標 6 像の Q4-粗部分は位数 |Δ|/3 = 119,042,784 で pc4-細核は C_3; ambient e4 = Q4 × pc4, |Q4| = 5.8×10²³,
      |pc4| = 3¹⁰, pc4: exponent 3・class 2・Frattini 列 [3¹⁰, 3⁴, 1]), (P2) 5 つの pentagon 代入に保たれる特性列(Δ 側の候補: Δ → Q_0 の核 Γ は
      exponent 9・class 2・abinv [9,9]・Frattini 列 [243, 27, 1] ⟹ 2 段 V = Γ/Φ(Γ) ≅ C_3², V = Φ(Γ) ≅ C_3³ に細分できる; ただし 3 座標の像が e4 の
      同一部分群かは未確認), (P3) 初等アーベル細分 — 未設計(法的像・境界 D_cen/D_0 込みのサイズ UNKNOWN)
(ix)  ブロック順序: H → P → ν(定理 A (iii))または joint; H 解集合の fibre(ker Φ_H)を occurrence closure から「lower-零行」として取る(v441 §3)
(x)   直接 replay(A0 = 1 の受理条件): 最終語 C(SLP)で hex_b(g760 C) の Fox 行 ∈ im D_2 over F_3[e3](v145 (2.4) ⟺ ∈ Φ_3(K_{3,0})), pent 同様 over F_3[e4],
      ν(C) = 0 整数, ρ_* で全下位段 MEMBER と整合
(xi)  NONMEMBER 証明書: 完全 fibre を消す dual + 残差との非零 pairing(v441 §7); 有限 cap は UNKNOWN_RESOURCE(v465 §5)
```

追加測定(既存 GHA 機構への要求・仕様のみ): (M1) rung 5/6 の extension データ生成(v442 の G9 twisting と同じ型で pc3 について; 作用は `Q_0` 直積ゆえ
共役は自明, occurrence 自己同型の `V_5 = C_3³` 上の 3×3 行列 5 本と `V_6 = C_3` 上のスカラー 5 本を測る), (M2) rung 3 grade 2–6 → rung 4 → 5 → 6 の
decision-first(v474/642)+ fresh ρ(v479)の反復, 各段で (iii)(v), (M3) P ブロックの (P1)–(P3) の GAP 測定(標的群の位数・特性列・`H_1(K_{4,0};F_3)` の次元),
(M4) 最終 (x) の replay checker(task192 terminal の型).

## 7. A0 以降への接続(一段だけ)

A0 = 1 が取れたときに渡す物(v220 §14 の依存鎖の最初の矢印):
- **形**: 一つの literal source word `c_0 ∈ Ω`(SLP root `C = Compose(…)`, v465 (4.1); 平坦展開不要), その ν = 0 の整数証明, 11 occurrence の endpoint
  receipt, そして `f^{(1)} = g760 c_0` が `E_{3,1}, E_{4,1}` で関係を満たすことの直接 replay(v145 Thm 2.2 の受理条件).  **両立系全体ではない** — rung 0 の
  一点(と, 定理 B (ii) に従い `S_0` の他の点へ戻れるよう, 解集合の記述 `c_0 + ker` の生成データ)を渡す.
- **次段**: A2 二入力 specializer(v221)→ v216 one-seed pre-gate / v188 actual `K` → v214 pointed `μ_1` → v191 `M` → v198 三 endpoint → (零なら)v197 `q` →
  v174 relative pro-3 lift(T2)→ B(mixed-prime)・C(perfect-core)→ 証人.  本稿の含意: v174/v191 の恒等式が `c_0` で失敗した場合, v195–v196 の same-μ
  repair に加えて `S_0` 内の別解への retreat が理論上は必要になり得る(定理 B (ii)); 設計に「rung-0 解の取り替え」経路があるかは §8 Q4.
- FAKE/IHARA の語は本稿で用いない(用語改定 20260823 に従い, 証人型/fake 型の判定は B₄ 層の別 gate).

## 8. Sol への問い

- **Q1** claim boundary の「COFINAL / SOURCE-KERNEL SURJECTIVITY: NOT PROVED」は relative Frattini 塔の rung ≥ 1(核 ⊊ Ω₀)のみを指し, T1 のどの段
  (Q₀ → e3 の 2 段, P ブロック含む)にも掛からない — この読み(定理 A)に同意するか.  同意なら「A0 = 1 は T1 頂上の MEMBER と同値」を A0 の受理条件として
  明文化してよいか.
- **Q2** H ブロック頂上 = `e3` の 2 段(`V = pc3/Φ(pc3) ≅ C_3³`, `V = Φ(pc3) ≅ C_3`)と P ブロックの塔は既存 note で設計済みか(v442/v443 の G9 twisting の
  pc3/pc4 版).  P ブロックの標的群の同定(§6 (P1))は v401–v403 のどれが正本か.
- **Q3** T2 の登録路線は v174(pointed Neumann, `μ ∈ 𝔧`)と v191(universal word-pair)のどちらが主か.  いずれかの**必要性**(証人が存在すれば恒等式も
  存在する)を示す note はあるか.  なければ「U3 の存在定理」の候補証明方針(§5.2 (a) 層再帰 / (b) syzygy)についての見解を請う.
- **Q4** v174/v191 の恒等式が A0 で得た `c_0` に対して失敗した場合, `S_0 = c_0 + ker` の別点へ retreat する経路は設計に含まれるか(v195–v196 は same-μ
  repair であって `c_0` の取り替えではないと読んだ).
- **Q5** 命題 C の下界 `|E_{3,1}| ≥ |e3|·3^{39,680,929}`(rung 1 = `P_3/Φ_3(ker(P_3 → e3))`)は登録塔の定義と一致するか.  一致するなら「rung ≥ 1 は射影と
  定理でのみ扱う」を v220 §16 の規則として明文化することを提案する.

## 9. 検算 artifacts(scratchpad/, sha16 = SHA-256 先頭 16 hex; 本文末に転記)

- `a0_cofinal_layers_v1.g` / `a0_cofinal_layers_v1_output.txt`: pc3/pc4 の構造(位数・abinv・exponent・class・Frattini 列), `|Q_0|`, `|Q4|`, `|e3|`,
  `⟨a,c⟩`-像の指数と `z3` の所属, `ker(e3 → Q_0)` の構造, `K_{3,0} ∩ ⟨a,c⟩` の階数下界.  入力 = 凍結 `fuda1_a0_rmax_data.g` のみ(joint 群は不要, 数十秒).
- `a0_cofinal_layers_v2.g` / `a0_cofinal_layers_v2_output.txt`: v2 prelude(joint 群)を読み, `Γ` の Frattini 列・E4 座標像の位数と核・E4 像の粗/細分解.
  (P ブロック塔設計 (P1)–(P3) の入力データ.)

機械出力(逐語, 折返し結合):

```text
LAYERS pc3 order 81 abinv [ 3, 3, 3 ] exponent 3 class 2 center 9 frattini_series [ 81, 3, 1 ] lower_central [ 81, 3, 1 ]
LAYERS pc4 order 59049 abinv [ 3, 3, 3, 3, 3, 3 ] exponent 3 class 2 center 243 frattini_series [ 59049, 81, 1 ] lower_central [ 59049, 81, 1 ]
LAYERS Q0 order 1469664 Q4 order 583152628325845597028352
LAYERS e3 order 119042784 index_of_<a,c>_image 3 z3_in_<a,c> false z3_order 3 z3_central true
LAYERS ker(e3->Q0) order 81 abinv [ 3, 3, 3 ] frattini_series [ 81, 3, 1 ]
LAYERS rank_lower_bound_N0capF(a,c) 39680929
LAYERS2 Gamma order 243 abinv [ 9, 9 ] exponent 9 class 2 frattini [ 243, 27, 1 ]
LAYERS2 coord 1..5 image_order 39680928 kernel_order 9 ; coord 6..8 image_order 357128352 kernel_order 1 ; coord 9..10 image_order 119042784 kernel_order 3
LAYERS2 E4coord6 image order 357128352 abinv [ 2, 2, 9, 9 ]
LAYERS2 E4coord6 coarse(Q4) image order 119042784 fine kernel order 3 fine kernel abinv [ 3 ] fine kernel frattini [ 3, 1 ]
```

整合: 座標核 (9,9,9,9,9,1,1,1,3,3) = v1 P1(task176); E3 像 39,680,928 = v220 Δ76 の context-image order; `Δ^{ab} = [2,2,9,9]` = errata §5.1;
`|Φ(Γ)| = 27`, `Γ/Φ(Γ) ≅ F_3²` = v2 P10.  新規(本稿): pc3/pc4/Γ の Frattini 列, `⟨a,c⟩`-像の指数 3, 階数下界 39,680,929, E4 像の粗/細分解.

## 10. Claim boundary

```text
A0 = FINITE LINEAR MEMBERSHIP (dim 357,128,353), NO INVERSE LIMIT:     PAPER (定理 A; v405 (4.2)/v1 §1/v145 Lemma 2.1 から)
T1 TOP MEMBER <=> A0 = 1; ANY RUNG NONMEMBER => A0 = 0:                  PAPER (定理 A (i)(iv))
H-BLOCK TOWER ABOVE Q0: TWO RUNGS (C_3^3, C_3), 19 GRADE DECISIONS LEFT:  PAPER + GAP (系 A.1; extension data NOT MATERIALIZED)
P-BLOCK TOWER:                                                            NOT DESIGNED (sizes UNKNOWN)
T2: ALL RUNGS NONEMPTY <=> WITNESS (pro-3 lane); COMPATIBILITY AUTOMATIC:  PAPER (定理 B = v169 Thm 4.1 + Mittag-Leffler)
T2 RUNG 1 SIZE >= |e3|*3^39,680,929:                                       PAPER + GAP (命題 C)
UNIFORM LIFT THEOREM / U3 EXISTENCE:                                       NOT PROVED (障害同定のみ; 【GAP-U1】; 【文献要請】 §5.2 (b))
A0 MEMBER / NONMEMBER / COMMON / COMPATIBLE LIFT / FAKE / IHARA:           NOT DECLARED
verified:                                                                  false
```

`R07_A0_COFINAL_LIFT_TWO_TOWERS_FABLE_V1`

## 11. Artifact sha16(SHA-256 先頭 16 hex)

```text
a0_cofinal_layers_v1.g                 a63ffbf51b62ca69
a0_cofinal_layers_v1_output.txt        f2c198a8664cad28
a0_cofinal_layers_v2.g                 5f648fda768fa734
a0_cofinal_layers_v2_output.txt        ee6147ba6e1a9192
```
