# A0 と「cofinal な両立 lift」— 二つの塔の分離・有限厳密性定理・König 境界(候補 paper note v2.2)

Author: Fable(数学者・Claude 側)/ 2026-09-05
Status: candidate paper note.  **v2.2 = v2.1(sha16 `ef6cc8dcb6594eb1`, 不変・保存)に Sol(Astra)返書 162 §2 の条件付き受理に応える narrowing を反映した改版**(差分 = §10 D5–D14).
Sol 162 §2 の判定: 定理 A の物理商訂正・完全下位 fibre・定理 B の根なし/根付き区別・P と ν の同時扱いは **重要として保持**; §5.2 の 2 命題は数学的排除として使う前に **狭めよ**.
本版は **定理 A・定理 B・命題 C とその証明を一切変更していない**(Sol の保持判定に従う).  変更は §5.2/§5.3/§0/§8/§10 の主張の射程と, §5.4(Sol 経路との対応表)・注 1.3・注 B.3 の新設のみ.
v2.1 = v2(sha16 `1c46f8ba47045a70`)に falsifier の新規 GAP(`fal_a0cl_nu_pent_check_v1.g`: pent(g760)=1 in e4・ν 正規化語の Δ での位数 9)を反映した小改版(差分 = §10 D1–D4).
v2 = v1(sha16 `87e6d2cdef64b6fe`)に工房 falsifier 前哨(裁定 2002)の要修正 2 点・軽微 7 点を反映し, 追補 `a0_cofinal_lift_theorem_v1_addendum_furusho.md`(sha16 `d10998f65fb7086e`)を §5.2 に統合したもの.
`verified=false`(Lean なし).  MEMBER / NONMEMBER / COMMON / fake / Ihara の宣言なし.  GHA・production・git 不使用.
機械計算 = **v2.2 では新規計算なし**(§9 の出力・sha16 は v2.1 のまま; 再実行もしていない).  数値・群計算はすべて既存 provenance の引用.

```text
VERDICT (3 行, v2.2):
 (1) A0 本体は cofinal 定理を必要としない.  A0 は次元 |Δ|+1 = 357,128,353 の一つの有限線形所属問題(v405 (4.2) / v1 §1)であり,
     特性商の塔 504→2,016→54,432→Q₀→… は「その一問題の商による必要条件の有限列」.  物理商 Ẑ = Z̄/D̃₀(v403 (1.6)–(1.9))の上で
     頂上(H ブロック = e3 水準, さらに P ブロックと ν)を**完全 fibre**で MEMBER 決定すれば A0 = 1(定理 A).  逆極限・コンパクト性・
     分離性(LERF)は A0 のどこにも入らない.
 (2) Sol の boundary の「COFINAL / SOURCE-KERNEL SURJECTIVITY: NOT PROVED」は二種ある: T1 の note(v465/v466/609)では
     「下位解の**自動 lift(全射性)**は未証明」の意味で閉鎖条件ではない(完全 fibre で実決定すれば閉じる); T2(v145/v395/v396/v169;
     v460 の「核 ⊊ Ω₀ の refinement」は T1 の rung 5–6 と T2 の両方)では cofinal lift が真の未証明定理(逐語 §2).
 (3) T2 では: 各段の完全解集合が全て非空 ⟺ 逆極限非空(König; v169 Thm 4.1 の根なし版)が自動.  足りないのは「全段非空」で,
     rung 1 の群は |E_{3,1}| = |e3|·3^{39,680,930} で計算不能(命題 C).  ゆえに T2 を閉じる定理は (c) rung-0 で有限回 replay により
     検査可能な恒等式(v191 (2.2): 源群 𝒢 上の普遍 Fox 加群での等式 / v174 (2.1))を前提にする形か, (d) 全 edge の核を有限に覆う形(§5.4)の
     いずれかになり, 前者の存在定理(U3)も後者の実 cover も未証明.
     候補型 (b)(pentagon ⟹ hexagon の欠陥恒等式)は群水準の塔相対 Furusho 性を要する.  **v2.2 で三分割**(§5.2 (i′)): 一様形(全 admissible f で
     `E_P = 0` が H 欠陥**全体**を零に強制する恒等式族)は在庫 (2) の有限反例により**翻訳前提つきで射程内で反証**, 副有限形は Furusho Q14 = **open**,
     **点固有形は未排除 = UNKNOWN**.  (a) 層再帰は降格.  **工房が現在明示している経路は (c) 登録契約型と (d) 一様 cover 型(v526/v537/v539 → v504, §5.4)の 2 つ**であり,
     v2.1 の「(c) が唯一可能な経路」は**撤回**する — それは数学的排除ではなく research-status の記述だった(Sol 162 §1 Q3/§2).
一文 gap: 「T1 を物理商上で完全 fibre により頂上まで登れば A0 = 1 は決まる — 足りないのは選択した filtration での残り 19 grade 決定
     (正準不変量ではない)+ P ブロック(商形で未設計・規模 UNKNOWN)+ ν(**P ブロックと同時に解く** — v460 の正規化語 c_x, c_y は H 塔では Fox 不可視だが P ブロックでは自動零ではない, §6 (vi))+ 直接 replay.  A0 = 1 から証人へは測定不能な無限塔 T2 の
     全段非空性(しかも得られるのは **lane 証人**まで — 注 B.3)が要り, それは v191 (2.2)/v174 (2.1) 型の有限検査可能恒等式の存在(U3), **または** (d) 全 edge の核 cover(v526/v537)の
     いずれかに還元されたまま(いずれも未証明).」
```

研究者向け要約(日本語): 「有限の塔を登り切っても A0 は cofinal 定理がないと閉じない」という読みは, Sol の boundary の「cofinal」が二つの意味で
使われていることから来ている.  T1(A0 内部の有限塔)の note では「下の段の解が自動的に上へ持ち上がる保証(全射性)は未証明」という意味で,
これは閉鎖条件ではない — 各段で「全ての下位解の差」を含む完全な fibre で判定すれば, 頂上で MEMBER なら A0 = 1 が決まる(定理 A).  ただし v1 の
定理 A は境界 D̃₀ を filtration に含めない場合に誤り(falsifier の反例 §3 注 A.3)で, v2 では v403 の物理商(境界を 0 にした空間)上で述べ直した.
D̃₀ は P ブロック内なので H ブロック側の結論と段の勘定は無傷.  本当に開いているのは A0 の上の無限塔 T2 で, (i) 各段が非空なら極限も非空は自動,
(ii) 各段の非空性を無限に確かめることは不可能(rung 1 の群の位数が 3 の 4 千万乗), (iii) だから「rung 0 で有限回の replay で検査できる一つの恒等式が
全段を同時に降ろす」型の定理(Sol の v174/v191)が出口の一つ — その恒等式の存在(U3)が律速.  **もう一つの登録済み出口**は「各 edge の核を有限の語つき列で覆えば下の段の解が自動で上がる」型(Sol の v526/v537/v539 → v504; §5.4)で, こちらは A0 = 1 を出発点として使えるが全 edge の cover が未証明.  候補として挙げた「pentagon が hexagon を
決める」型は, **全 f 一様な形**については DLL の有限反例(35 窓中 24 で不成立)により射程内で反証されるが, **点固有の形は排除されていない**(副有限版 = Furusho Q14 は未解決のままで, 有限反例からは偽と結論できない).  本稿はいずれも証明しない.  v2.2 はこの三分割と「(c) が唯一」の撤回, 「全段非空 ⟺ 証人」の lane 限定を行った版である.

---

## 0. 記号(正典逐語 → 略記; v460/v459 の記号に合わせる)

- `F = F(x,y)`, `Θ: F ↠ Δ` joint roof, **`Ω = ker(F → Δ)`**, **`Ω₀ = ker(F → Q₀)`**, `Ω ⊆ Ω₀`(v460 §1 逐語; `[Ω₀ : Ω] = |Γ| = 243`).
  `|Δ| = 357,128,352 = 2⁵·3¹³·7`, 座標核 `(9,9,9,9,9,1,1,1,3,3)`(v1 P1, task176 cross-checked).  `M := H_1(Ω;F_3) = Ω/Ω'Ω³`, `dim M = |Δ|+1`(v1 (1.1)).
- `P_3 = PB3 = ⟨a,b,c | 2 relators⟩ = ⟨a,c⟩ × ⟨z⟩`(`z = abc` 中心), `P_4 = PB4`.  pinned marked quotients `E_3 = e3`, `E_4 = e4`(v145 (1.1)).
  `e3 = Q_0 × pc3`(v1 P6; GAP: `|e3| = 119,042,784 = |Q_0|·81`, 直積そのもの), `|Q_0| = 1,469,664`, `|pc3| = 81`; `AC := ⟨a,c⟩` の像(指数 3), `e3 = AC × ⟨z3⟩`(§9).
- 11 occurrence: 6 PB3 slot(H1: fyz,fxz,fxy / H2: fuy,fxy,fux)+ 5 PB4 slot(v2 addendum §2.3, v405 §1).
- 物理空間 `Z̄ = Y_3^{(1)} ⊕ Y_3^{(2)} ⊕ Y_4^{cen} ⊕ k²`(v405 (3.3)), 残余境界 `D̃_0 = (0,0,D_0,0)`(v405 (4.1)), **物理商 `Ẑ := Z̄/D̃_0 = Y_3^{(1)} ⊕ Y_3^{(2)} ⊕ Ȳ_4 ⊕ k²`**
  (v403 (1.6) `Ȳ_4 = (k[H_0]^5/D_0) ⊕ k[H_4]/(NI_{H_0})`, (1.8) `Q = Q_3 ⊕ Q_3 ⊕ Q_4 ⊕ id_{k²}`, Thm 1.1 (1.9) `ker Q = D`).  `k = F_3`.
- 標的 `T = −Fox(hex_1(g760)) ⊕ −Fox(hex_2(g760)) ⊕ −Fox(pent(g760)) ⊕ (0,0)`(v1 P3).  `Φ := Q_ph L̂_g Ĵ : M → Z̄`, `C := Φ(M)`(v1 §1); `Â := (Z̄ → Ẑ) ∘ Φ`, `t̂ := −T̄ mod D̃_0`.
- 正規化指数 `ν : Ω → k²`(v399; `ε/18 mod 3`, `Ω` の指数格子は `18Z²`, errata §5.1).
- Relative Frattini: `Φ_3(K) = K³[K,K]`, `K_{r,n+1} = Φ_3(K_{r,n})`, `E_{r,n} = P_r/K_{r,n}`, `K_{r,0} = ker(P_r → E_r)`(v145 (1.2)–(1.3)).
- T2 の joint kernel: **`Ω⁽ⁿ⁾ := ∩_{slots} σ_o^{−1}(K_{r,n})`, `Ω⁽⁰⁾ = Ω`**(v1 の `Ω_n`, `Ω_0` を改名; v460 の `Ω_0` との衝突回避).

## 1. A0 の正確な主張(pin)

### 1.1 逐語

- **v405 (4.2)**: 「The exact A0 equation is now `−T̄ ∈ L̄_g(W̄) + D̃_0`」, `W̄ = span_k{ρ̄(a) Ĵ_g(r_i)‾ : i=1..44, a ∈ F(x,y)}`(v405 (2.1)),
  `D̃_0 = (0,0,D_0,0)`(v405 (4.1)).  **v405 Theorem 4.1 (COMPLETE FINITE A0 SELECTOR)**: 「decides the A0 equation (4.2) after finitely many strict rank rises」.
- **v403 Theorem 1.1 (1.9)**: 「`ker Q = D`」— 物理商 `Q = Q_3 ⊕ Q_3 ⊕ Q_4 ⊕ id_{k²}` の核が完全境界 `D`.  §2: 「A producer need not materialize the quotient by `D_0`」(lazy 六 family 形は等価).
- **v1 §1**: 「the A0 equation v405 (4.2) is `−T̄ ∈ D̃_0 + C`」, `C = Φ(M)`, `dim M = |Δ|+1`.
- **v145 Theorem 2.2**: `f^{(1)} = g760 c_0` について「both hexagon relation words of `f^{(1)}` lie in `K_{3,1} = Φ_3(K_{3,0})`, and its printed-order pentagon relation word lies in `K_{4,1} = Φ_3(K_{4,0})`」; 「Thus task179 is the first universal elementary-abelian relative lift above the pinned `E_3/E_4` window」.
- **v145 Lemma 2.1 (2.3)–(2.4)**: `K/K³[K,K] ≅ ker D_1/im D_2`(`F_3[E]`-加群同型), `∇w ∈ im D_2 ⟺ w ∈ Φ_3(K)`.  適用前提: `w` の値が `K` に入ること.
- **v220 §20 表**: 「A0 | task192 actual exact word | positive terminal + independent acceptance: 0/1」.

### 1.2 A0 = relative Frattini 塔の rung 0 → 1 の一つの有限線形問題

Lemma 2.1 の適用前提(値が `K_{r,0}` に入る)は H ブロックでは機械確認済み: **`hex_1(g760) = hex_2(g760) = 1` in `e3`**(falsifier 検査 `scratchpad/fal_a0cl_e3check_v1.g`, 本稿で再実行:
「FAL hex1(g760)=1 in e3: true hex2(g760)=1 in e3: true」, §9).  P ブロックも機械確認済み(単一実装): **`pent(g760) = 1` in `e4`**(falsifier 検査 `scratchpad/fal_a0cl_nu_pent_check_v1.g`: 5 slot 規約すべて true, 各 occurrence 値 `f_j` は位数 9; v2 の UNKNOWN を v2.1 で更新, §9).  その下で

```text
A0 = 1  ⟺  ∃ c ∈ Ω :  hex_b(g760·c) ∈ Φ_3(K_{3,0}) (b=1,2),  pent(g760·c) ∈ Φ_3(K_{4,0}),  ν(c) = 0
        ⟺  ∃ [c] ∈ M :  Φ([c]) ≡ −T̄ (mod D̃_0)      (v405 (4.2))
        ⟺  ∃ [c] ∈ M :  Â([c]) = t̂   in  Ẑ = Z̄/D̃_0  (v403 (1.9) で境界を 0 に).
```

右辺は有限次元 `F_3`-空間 `M`(dim 3.57×10⁸)上の線形所属.  `c ↦ Fox(hex_b(g760 c)) − Fox(hex_b(g760))` は `[c] ∈ M` の線形関数(v1 P4, v396 (1.5)); Fox 行は `ker D_1` に入り
`im D_2` で割った類が `H_1(K_{3,0};F_3)` の元 = 「`Φ_3(K_{3,0})` に落ちるか」の唯一の障害(Lemma 2.1).  **A0 は群 `Δ`(有限)・加群 `M`・標的空間 `Ẑ`(有限次元)だけで完結し, 無限対象を
含まない.**  v405 Thm 4.1 はその有限決定手続きである.

### 1.3 二つの塔(本稿の中心的区別)

```text
T1 (A0 の内部・有限):  Ẑ の商への射影 π_{Q'} で得る必要条件の列.  H ブロック側の標的群 e3 の特性商の塔:
      P=PSL(2,8) (504)  ←  Q_1 = Q_0/(1×G9') (2,016)  ←  Q_2 = Q_0/(1×(G9')³) (54,432)  ←  Q_0 (1,469,664)
                        ←  e3/Φ(pc3) (39,680,928)      ←  e3 (119,042,784)  [頂上 = A0 の H ブロック]
      (v2 addendum §3.5 / v441 §6 に GAP の 2 段を追加: pc3 は exponent 3, class 2, Φ(pc3)=pc3' 位数 3, Frattini 列 81→3→1)
      P ブロック側の塔: 物理商 Ȳ_4(v403 (1.6))の上で設計されるべきもの — 未設計(§6 (P1)–(P3)).   ν: 座標 1 本(§6 (vi), v460).
      各段 Q' で「MEMBER」= π_{Q'}(t̂) ∈ π_{Q'}(Â(M))  (chord/kernel 形 = closure 形, errata R2).
      各段は厳密な必要条件: NONMEMBER at Q' ⟹ A0 = 0.   頂上を完全 fibre で MEMBER ⟺ A0 = 1  (定理 A).
      T1 の boundary 行「SURJECTIVITY / COFINAL LIFT: NOT PROVED」(v465/v466/609)= 下位解の自動 lift 未証明 = 閉鎖条件ではない.

T2 (A0 の上・無限):   relative Frattini 塔 (v145 (1.3)).  rung n の問題 = 「f^{(n)} = g760 c_0 ⋯ c_{n−1} の hexagon/pentagon を
      K_{r,n+1} = Φ_3(K_{r,n}) に落とす c_n ∈ Ω⁽ⁿ⁾」.  rung 0 = A0.  rung n ≥ 1 の群は計算不能な大きさ(命題 C).
      「cofinal」(v145/v396/v460)「compatible lift」(v395/v169)「source-kernel surjectivity」(v395 (3.4))の真の未証明定理はここ(§2).
```

**注 1.3(段の名指しと NAME-COLLIDE — D11; Sol 162 §0 の前提訂正).**  本稿の「rung N」= 塔の N 番目の商を**標的とする段**(地図の「N 段」と同じ target 名の規約):

```text
rung 1 = 段[504 = PSL(2,8)]                 rung 2 = 段[2,016]      (edge 504 → 2,016)
rung 3 = 段[54,432] (edge 2,016 → 54,432)   ← **現在の precision-two / grade 作業はここ**
rung 4 = 段[Q_0 = 1,469,664] (edge 54,432 → Q_0)   rung 5 = 段[e3/Φ(pc3)]   rung 6 = 段[e3]  ← H ブロック頂上
```

すなわち**現行作業は `2,016 → 54,432` の段であって `54,432 → Q₀`(= rung 4, 未着手)ではない**(Sol 162 §0 1. の前提訂正; 地図 9/3 追記も同じ訂正済).  本稿の他の箇所の「rung N」はこの表で読む.
**NAME-COLLIDE(「rung」)**: Sol の "first rung" は **T2 の relative Frattini rung 1**(= A0 全体 = 本稿 T1 の全段)を指し, 本稿 T1 の rung 1..6 とは別の数え方である(v145 (1.3) の `K_{r,n}`).
Sol 162 §5 の「first-rung grades 1/6」は「T2 rung 1 の内部(= 本稿 T1 rung 3)の grade 1/6」の意味.

図式(T1 の各段 MEMBER が A0 のどの必要条件か; 物理商上):

```text
  M ──Â──▶ Ẑ = Y_3^{H1} ⊕ Y_3^{H2} ⊕ Ȳ_4 ⊕ k²                 A0: t̂ ∈ Â(M)
  │            │ π_{e3→Q'} (H ブロック; κ_* 型, v1 (3.1))         必要条件 (Q'): π_{Q'}(t̂) ∈ π_{Q'}(Â(M))
  │            ▼
  │        Y-bar_3^{H1}(Q') ⊕ Y-bar_3^{H2}(Q') ⊕ k²          Q' = P, Q_1, Q_2, Q_0, e3/Φ(pc3), e3
  │  (v1 定理 B/C は Q'=Q_0 で seed 1,2 が 0 になる/T が V0 像の外, の主張; v2 addendum §4.1: P ブロックは π で落とす)
  └─ 頂上 Q' = e3 で H ブロック MEMBER ⟹ 解集合 c_H + ker Â_H 上で P ブロック方程式(有限, Ȳ_4 上)⟹ A0.
```

## 2. 「cofinal」「compatible lift」「source-kernel surjectivity」の逐語と帰属

| 語 | 正典逐語 | 帰属(v2 で訂正) |
|---|---|---|
| cofinal(T2) | v145 status: 「proves that the resulting relative Frattini tower is cofinal on the marked pro-3 lane」; v396 §7: 「this **finite A0 closure** does not prove that every cofinal rung has a nonempty accepted set. It is a faster finite base-word constructor, not the missing inverse-limit homotopy」 | T2 の rung ≥ 1 |
| cofinal(T1+T2) | v460 §1: 「`Ω = ker(F→Δ)`, `Ω_0 = ker(F→Q_0)`, `Ω ⊆ Ω_0`」; §4: 「does not … prove compatibility for **refinements whose kernel is smaller than `Omega_0`**. In particular it is not by itself the inverse-limit homotopy requested for all cofinal refinements」, 「REFINEMENTS BELOW Omega_0 / COFINAL LIFT: OPEN」 | 核 ⊊ Ω₀ の refinement = **T1 の rung 5–6(rung 6: `σ_o^{−1}(K_{3,0}) = ker(F→AC)`, `F` の `e3` 像は `AC`(指数 3); rung 5: `ker(F→AC/Φ(pc3))`, `Φ(pc3) ≤ AC`(§9 FAL 行); いずれも ⊊ Ω₀)と T2 の両方**.  T1 部分は有限段の未実行, T2 部分が真の定理 |
| compatible (cofinal) lift | v395 Thm 4.1(「Fix the registered cofinal tower」の下): 「`c_∞ = (c_n)` is one coherent correction in the inverse limit」(前提: 全 edge で (3.4)); v169 Thm 4.1: 「If `𝒮_n ≠ ∅` for every `n`, then `lim← 𝒮_n ≠ ∅`」+「compactness removes the **compatibility-choice** problem, not the **nonemptiness** problem」; v220 §1.1: 「全ての有限 GT-shadow へ整合的に降りる一つの profinite GT element を構成する」 | T2 全段の解の整合族 = profinite 元 |
| source-kernel surjectivity(抽象) | v395 (2.4) `K^D_n = ker r^D_n`, `K^L_n = ker r^L_n`; (3.4) `B_{n+1}(K^D_n) = K^L_n` = UNIVERSAL ONE-STEP CRITERION(「provided `r^D_n` is onto on the legal source」); Cor 3.2: 「Every lower solution and every compatible fine target lift across this edge can be lifted if and only if (3.4)」 | 任意の edge(T1 でも T2 でも)での**自動 lift**(全ての下位解が持ち上がる)の判定条件; 十分条件であって閉鎖条件ではない |
| source-kernel surjectivity(T1 の note) | v465(rung 3 grade-one SLP の note; status「the positive handoff after a grade-one MEMBER decision」)Prop 2.2(§2): 「(2.3) proves membership in the registered physical fibre. It does **not** by itself prove membership in a source relative kernel such as `K^D_n = ker r^D_n`. That stronger typing requires a separate direct source-reduction replay」, boundary 「COFINAL SUCCESSOR SURJECTIVITY: NOT PROVED」; v466 §5: 「The source-kernel assertion required by a later v395 edge remains a distinct direct source-reduction replay」; reply 609 boundary: 「SOURCE-KERNEL SURJECTIVITY / COFINAL LIFT: NOT PROVED」 | **T1 の edge**(rung 3 の grade 遷移と後続 rung).  意味 = 「選択 SLP を v395 の再帰(3.3)の `K^D_n` の元として使う typing は別 replay が要り, 下位解の自動 lift は未証明」.  **閉鎖条件ではない**: 完全 fibre(定理 A (ii) の `K_d`)で実決定すれば, 自動 lift の有無に関わらず各段は閉じる |
| 「6 grade MEMBER ⟹ 54,432 で等式」の境界 | v479 §6: 「Six accepted MEMBER updates with direct replays imply equality at order 54,432 because `I^7 = 0` … It does not imply the second rung or any cofinal lifting theorem」 | T1 の rung 3 完成 = T1 内の一段; 「second rung」= 次段 |

**定式(v2).**  T1 では boundary 行は「自動 lift(全射性)は未証明」の意味であって閉鎖条件ではない(完全 fibre で実決定すれば閉じる).  T2 では cofinal lift が真の未証明定理である.
v1 §2 の「いずれも T2 の語」は過大で, 上表のとおり訂正する.

## 3. 定理 A(A0 の有限厳密性 — 物理商上・T1 に逆極限は入らない)

**設定.**  `W := Ẑ = Z̄/D̃_0`(有限次元; v403 Thm 1.1 により境界は 0), `A := Â : M → W`(線形), 標的 `t := t̂`.  A0 ⟺ `t ∈ A(M)`.
`W ⊇ F^0 ⊋ F^1 ⊋ ⋯ ⊋ F^m = 0` を `W` の任意の減少フィルトレーション(部分空間の列)とし, `C_d : M → W/F^d`, `t_d := t mod F^d`, `S_d := {m ∈ M : C_d(m) = t_d}`.

**定理 A.**
(i) `S_{d+1} ⊆ S_d`(有限集合の降下列); `S_m` = A0 の解集合.  **A0 = 1 ⟺ `S_m ≠ ∅`**; **`S_d = ∅` for some `d` ⟹ A0 = 0**.
(ii) (v441 Cor 2.2 の一般形) `S_d ≠ ∅` とし `c ∈ S_d` を任意に取る.  `D_d := ker C_d = A^{−1}(F^d)`(下位解の差の空間: `S_d = c + D_d`), `K_d := A(D_d) mod F^{d+1} ⊆ F^d/F^{d+1}`,
`ρ_d := (t − A(c)) mod F^{d+1} ∈ F^d/F^{d+1}`.  このとき **`S_{d+1} ≠ ∅ ⟺ ρ_d ∈ K_d`**; 条件は `c` の取り方に依らない.
(iii) (ブロック逐次) `F^1 = 0 ⊕ 0 ⊕ Ȳ_4 ⊕ k²`(H ブロックを先に見る), その下に `Ȳ_4`・ν のフィルトレーションを続けても (i)(ii) はそのまま成り立つ.  「H ブロックを頂上まで解く →
その解集合 `c_H + ker Â_H` 上で P ブロック(`Ȳ_4` 上)と ν を解く」は厳密.  法的像を「商での閉包」として計算するために必要なのは, 商 `W/F^d` への射影が occurrence-separated module 上の
4 actor の半線形作用と可換なこと; ブロック射影は tag ごとの作用 `ρ̄_o(a)`(v405 (1.6))と可換で, ν の作用は自明(v405 §1)なので満たす.
(iv) 特性商の塔は (i) の特別な場合: `Q'' → Q'` が `e3` の商で, その核が occurrence の誘導する **`AC = Δ/K` の自己同型**(5 座標写像の合成 `φ_{o'} ∘ φ_o^{−1}`; `e3` の自己同型ではない)に保たれるなら `π_{Q'} = ρ'_* ∘ π_{Q''}` が線形に誘導され(v2 addendum §4.1 の可換図式
`A_g^{Q'} ∘ ρ_* = ρ_* ∘ A_g^{Q''}`; H ブロックについて), `F^d := ker(π_{Q'})` 型の部分空間列が得られる; 各段の中の grade 分解(v441 (1.6)–(1.7))は `F^d = I^d W` によるその細分.
したがって塔の各段 MEMBER は A0 の必要条件であり, **頂上 `Q' = e3`(H ブロック)+ P ブロック(`Ȳ_4` 上)+ ν の完全 fibre MEMBER が A0 = 1 と同値**.
(v) コンパクト性・逆極限・部分加群の副有限閉包・LERF 型の分離性は一切使われない: `M`, `W` が有限次元だから.

*証明.* (i) `C_{d+1}(m) = t_{d+1}` なら mod `F^d` に落として `C_d(m) = t_d`.  `F^m = 0` で `S_m` は A0 の解集合そのもの.
(ii) `S_d = c + D_d`(`A(c) ≡ t mod F^d` かつ `A(δ) ∈ F^d` ⟺ `A(c+δ) ≡ t mod F^d`).  `S_{d+1} ≠ ∅ ⟺ ∃δ ∈ D_d : A(c+δ) ≡ t mod F^{d+1} ⟺ (t − A(c)) mod F^{d+1} ∈ A(D_d) mod F^{d+1}`;
左辺は `F^d/F^{d+1}` の元(`c ∈ S_d`), 右辺は `K_d`.  `c' = c + δ'`(`δ' ∈ D_d`)に替えると `ρ'_d = ρ_d − A(δ') mod F^{d+1}` は `K_d` を法として不変.
(iii) 任意の減少フィルトレーションで (i)(ii) は成り立つ(部分空間列以外の仮定を使っていない). (iv)(v) 明白. ∎

**注 A.3(境界を filtration に含めない定式は誤り — v1 定理 A (ii)(iii) の訂正).**  境界 `D̃_0 ≠ 0` を残した空間 `Z̄` 上で `S_d := {m : Φ(m) ≡ −T̄ mod (D̃_0 + F^d)}` と定めると
`S_d = c + ker C_d` は**偽**である.  falsifier の反例(`F_3`, node 実証): `W = F_3²`, `A(M) = ⟨e_1⟩`, `D̃_0 = ⟨e_1+e_2⟩`, `F^1 = ⟨e_2⟩`, `t = e_2`.  真は MEMBER(`e_2 = 2e_1 + (e_1+e_2)`)だが
v1 の判定は `K_1 = 0`, `ρ_1 = e_2 ∉ K_1` で「`S_2 = ∅`」を返す.  境界を残す場合の正しい下位解差空間と fibre は

```text
D_d = A^{−1}(D̃_0 + F^d),     K_d = ( (A(M) ∩ (D̃_0 + F^d)) + D̃_0 + F^{d+1} ) ∩ F^d / F^{d+1}
```

(反例では `K_1 = ⟨e_2⟩ ∋ ρ_1` で MEMBER に戻る).  v441 Cor 2.2 は元々 boundary quotient 後の物理加群 `W`(v441 §1: 「the physical module after the fixed signed aggregation and boundary
quotient」)で述べられており, 本 v2 もそれに合わせて `W = Ẑ`(`D̃_0 = 0`)で述べた.  `D̃_0 = (0,0,D_0,0)` は P ブロック内なので, **H ブロックの結論・系 A.1 の勘定・T1 rung 1–6 は無傷**;
P ブロックの塔は物理商 `Ȳ_4`(v403 (1.6))の上で設計する(lazy 六 family 形 v403 §2 は等価だが, filtration の厳密性の言明は商の上で行う).

**系 A.1(残り工程の勘定, H ブロック; 選択した filtration に対する決定回数).**  現状(地図 2026-09-03 追記; 段名は注 1.3): rung 1(段[504]), rung 2(段[2,016])MEMBER(cross-checked), **rung 3(段[54,432] = edge `2,016 → 54,432` = 現在の precision-two 作業)= grade 1/6**(限定つき cross-checked).
残り: rung 3 の grade 2–6(5)+ rung 4 `Q_0`(`V = (G9')³ ≅ C_3³`, 6)+ rung 5 `e3/Φ(pc3)`(`V = pc3/Φ(pc3) ≅ C_3³`, `Q_0` の共役作用は自明(直積), 6)+ rung 6 `e3`(`V = Φ(pc3) = pc3' ≅ C_3` 中心,
`k[u]/(u³)`, 正 grade 2)= **19 grade 決定**.  **注(f)**: 19 は「`1×pc3` の Frattini 列」という選択した filtration に対する決定回数であり正準不変量ではない — 例えば `C_3³` 層を `C_3 ⊕ C_3²` に
切れば `Q_0` の上は `2+4+2`, 屋根側(Δ 水準)の別列ならまた別の勘定になる; 不変なのは有限性と厳密性(定理 A)だけ.  その後 P ブロック(商形で未設計・§6)と ν(P ブロックと同時, §6 (vi))・直接 replay.
数値根拠(§9): `pc3` order 81, `AbelianInvariants = [3,3,3]`, exponent 3, class 2, Frattini 列 `[81, 3, 1]`; `ker(e3 → Q_0) = 1×pc3`.  occurrence 自己同型による保存: `ker(Δ → e3)` は 5 座標で
一致(errata R6)し `ker(Δ → e3 → Q_0) = Γ` も 5 座標で一致(v1 Lemma 3.1)ので, 誘導されるのは **`AC = Δ/K` の自己同型**(`e3` の自己同型ではない).  filtration `I^d`(`I` = `1×pc3` の augmentation ideal の生成する `k[e3]` の両側イデアル)の actor 安定性は `I` が両側イデアルであること(乗法部分)と, `1×pc3` が `e3 = Q_0 × pc3` で特性的であること(`Hom(pc3, Z(Q_0)) = 0`; 工房 falsifier 再検査の根拠, 本稿では未再計算)から従い, その Frattini 列も特性的ゆえ保たれる(紙).  各段の実 extension データは**未実体化**.

**注 A.2(NONMEMBER 側の非対称).**  MEMBER は部分 span(routed span・targeted CEGAR)で証明してよい.  NONMEMBER は `K_d` を完全な `D_d` で計算した上でのみ有効(v441 §3 末尾,
v479 §5「TARGETED MEMBER = COMPLETE PRESENTATION: FORBIDDEN」).  `D_d` は下位の**全**解の差であって「選んだ下位解の fibre」ではない — これが §2 の「自動 lift 未証明 ≠ 閉鎖条件」の内容.

## 4. 定理 B(T2: König 境界・dead branch・計算不能性)

**設定(v2: 根なし版・ν gate 込み).**  `ν : Ω → k²` は準同型(`ε` は加法的, 像は `18Z²`).  `G_n := Ω/(Ω⁽ⁿ⁺¹⁾ ∩ ker ν)`(有限群: `Ω⁽ⁿ⁺¹⁾` は `Ω` で有限指数, `ker ν` は指数 ≤ 9),
`S_n := {c̄ ∈ G_n : hex_b(g760 c) ∈ K_{3,n+1} (b=1,2), pent(g760 c) ∈ K_{4,n+1}, ν(c) = 0}`.  各条件は `G_n` の類上 well-defined(`hex_b(g760 c) mod K_{3,n+1}` は `c mod σ_o^{−1}(K_{3,n+1}) ⊇ Ω⁽ⁿ⁺¹⁾` にのみ依存;
`ν(c)` は `c mod ker ν` にのみ依存).  制限 `r_n : G_{n+1} → G_n` は well-defined(`Ω⁽ⁿ⁺²⁾ ∩ ker ν ⊆ Ω⁽ⁿ⁺¹⁾ ∩ ker ν`)で `S_{n+1}` を `S_n` に写す(`K_{r,n+2} ⊆ K_{r,n+1}`).
他の登録 side gate(v169 §4 条件 4: marking, formation, onto, settlement)は本稿の射程外で, 同じ可換性を各々確かめる必要がある.
証人(v220 §1.1 の pro-3 lane 部分)= `lim← S_n` の元.

**注 B.0(v169 との差).**  v169 Thm 4.1 の `𝒮_n` は条件 1–5 つき, 特に条件 5 「reduce to the fixed earlier partial word」を含む**根付き**版(固定した部分語の fibre 内の解集合).  本稿の `S_n` は
根なし(全解集合).  この差が (ii) の dead-branch の内容そのもの: 根付き版の全段非空は「固定した枝が生きる」を意味し, 根なし版の全段非空は「どこかの枝が生きる」を意味する.

**定理 B.**
(i) (König; v169 Thm 4.1 の根なし版) `lim← S_n ≠ ∅ ⟺ ∀n: S_n ≠ ∅`.  遷移写像は関手的に存在し, 「両立性」は自動.
(ii) (Mittag-Leffler 型の精密化) `S_n^∞ := ∩_{m ≥ n} r_{n,m}(S_m)` とおくと `S_n^∞ = im(lim← S → S_n)` であり, **証人 ⟺ `S_0^∞ ≠ ∅`**.  A0 = 1 で得た `c_0 ∈ S_0` が `S_0^∞` に入る保証はない:
「`c_0` を固定した fibre(= v169 の根付き `𝒮_n`)で rung n が NONMEMBER」は証人問題の NONMEMBER ではない(dead branch).
(iii) (一様 lift) 全 edge で v395 (3.4) が成り立てば `r_n` は全射, よって `S_n^∞ = S_n` かつ **証人 ⟺ A0 = 1**.  (3.4) は各 edge で有限 rank test だが edge は無限個.
(iv) (class-specific の必要十分) 固定した `c ∈ S_n` の fibre `r_n^{−1}(c)` は `(Ω⁽ⁿ⁺¹⁾ ∩ ker ν)/(Ω⁽ⁿ⁺²⁾ ∩ ker ν)` のアフィン部分空間で, 非空 ⟺ `ρ_{n+1}(c) ∈ im B_{n+1}(f)`, `f = g760 c`,
`B_{n+1}(f) : (Ω⁽ⁿ⁺¹⁾ ∩ ker ν)/(Ω⁽ⁿ⁺²⁾ ∩ ker ν) → ⊕_r H_1(K_{r,n+1};F_3)`, `[δ] ↦ Σ_o ε_o P_o(f)·[σ_o(δ)]`(定義域を ν gate 側に制限; `σ_o^{−1}(K_{r,n+2}) ⊇ Ω⁽ⁿ⁺²⁾ ⊇ Ω⁽ⁿ⁺²⁾ ∩ ker ν` ゆえ well-defined).  これは rung `n+1` における「A0 と同形の有限線形所属」.

*証明.* (i) 有限集合の逆系: `S_n ≠ ∅` 全てなら各深さに頂点をもつ有限分岐木に König.  逆は明白.  (ii) 有限集合の逆系では `im(lim← S → S_n) = ∩_m r_{n,m}(S_m)`(各 `m` で像は有限降下列で安定し,
安定部分系に König).  (iii) v395 Cor 3.2.  (iv) Fox 積公式: `σ_o(δ) ∈ K_{r,n+1}` かつ `K_{r,n+1}/K_{r,n+2}` はアーベルなので `hex_b(fδ) ≡ hex_b(f)·Π_o (P_o σ_o(δ) P_o^{−1})^{ε_o}` mod `K_{r,n+2}` の類は
`[hex_b(f)] + Σ_o ε_o P_o·[σ_o(δ)]`; `[σ_o(δ)]` は `δ mod Φ_3(Ω⁽ⁿ⁺¹⁾)` にのみ依存. ∎

**注 B.3(「全段非空 ⟺ 証人」の射程 — v2.2 で追加・D10; Sol 162 §2 末).**  定理 B (i)(ii) の右辺は `lim← S_n` の元であり, `S_n` は §4 の定義 = **登録済み pro-3 lane** の相対 Frattini 条件 + ν gate
だけを課した集合である.  ゆえに定理 B が与えるのは「**lane 証人**」(= v220 §1.1 の証人の pro-3 lane 部分)であって, **無条件の証人ではない**.  完全な証人にはさらに
(α) v169 §4 条件 4 の side gate(marking, formation, onto, settlement)— 各段で restriction と可換であることを確かめれば `S_n` の定義に追加でき, König 論法はそのまま通る(各自確認が要る・本稿の射程外)—
と, (β) v220 §16 規則 8 の B(mixed-prime)・C(perfect-core)gate が要る.  (β) は 3 冪商の逆系では**原理的に見えない**(注 B.2 (T-iii) の玩具例 `F = Z`, 条件「`c ≡ 1 (mod 2)`」)ので `S_n` に追加できず,
T2 を閉じても別途要る.  したがって §10 claim boundary の該当行は「**lane 限定**」と読むこと(v2.1 の無条件の「⟺ WITNESS」は本版で限定した).  定理 B の主張と証明そのものは不変.

**命題 C(rung 1 は計算不能; v2 で exact).**  `P_3 = ⟨a,c⟩ × ⟨z⟩`(`z = abc` 中心; `⟨a,c⟩ ↠ P_3/⟨z⟩ ≅ F_2` は 2 生成群から自由群への全射ゆえ同型, `⟨a,c⟩ ∩ ⟨z⟩ = 1`).  GAP(§9):
`e3 = AC × ⟨z3⟩`(`AC` = `⟨a,c⟩` の像, 指数 3, `|AC| = 39,680,928 = |Δ|/9`; `z3` 中心・位数 3・`z3 ∉ AC`), 5 つの E3 occurrence の像は全て `AC`.  `P_3 → e3` は積写像 `(⟨a,c⟩ → AC) × (⟨z⟩ → ⟨z3⟩)` なので
`K_{3,0} = K_A × ⟨z³⟩`, `K_A = ker(⟨a,c⟩ → AC)` は自由群 `⟨a,c⟩` の指数 `39,680,928` の部分群で Schreier 階数 `39,680,929`, `⟨z³⟩ ≅ Z`.  よって

```text
dim_F3 H_1(K_{3,0};F_3) = 39,680,929 + 1 = 39,680,930  (exact),     |E_{3,1}| = |e3| · 3^{39,680,930} = 1.19×10⁸ · 3^{39,680,930}.
```

rung 1 の標的空間 `H_1(K_{3,1};F_3)` は次元 ≈ `|E_{3,1}|`.  **T2 の rung ≥ 1 は有限だが計算の対象にならず, 「全段 MEMBER」は測定可能な命題ではない.**
(Sol の v213/v216 の exponent-9・pro-Heisenberg 射影は rung n の**商への射影**(必要条件)であって rung そのものではない — v220 §8, §16 規則 5.)

**系 B.1(依頼された定理の位置づけ; v2.2 の限定は §5.2/§5.4 と注 B.3 を併読).**  「条件 (i)–(k) の下で cofinal な有限段の両立 MEMBER 系は A0 の解を与える」は:
- T1 に対しては定理 A(条件 = §6 の有限 gate; 「両立」は自動; 頂上の完全 fibre MEMBER = A0).
- T2 に対しては定理 B (i)(ii)(条件 = 全段の完全解集合が非空; 「両立」は自動)— しかしその前提は命題 C により**測定できない**.  ゆえに T2 を閉じる定理は「rung-0 で有限回の replay により
  検査可能な条件 ⟹ 全段非空」の形でなければならず, 登録済みの候補は v174 Thm 2.1(`β − Ba = μβ`, `μ ∈ 𝔧` ⟹ `q_∞ = Σ μ^r a`, `B q_∞ = β`)と v191 Thm 2.1(word-pair `M` と boundary chain `q` の
  **源群 `𝒢` 上の普遍 Fox 加群での等式** `ẽ − M d̃ = D̃_2 q` ⟹ 全 matched relative pro-3 quotient で `e_n = μ_n d_n`; `q` の存在 ⟺ 三 endpoint 零, v194/v198).  両者は**十分**条件
  (v220 §14「v191 は sufficient theorem であり, 必要条件とは証明していない」).  その等式の存在(U3)が本当の open(§5).

**注 B.2(依頼の「最小反例モデル」について).**  「有限段で全て MEMBER なのに極限で失敗する玩具例」は, 完全(根なし)な有限解集合と自然な制限写像の逆系では**存在しない**(定理 B (i)).
現実に起こり得る失敗は次の 3 型で, それぞれ玩具例を与える:
- (T-i) dead branch(根付き版と根なし版の差): `S_0 = {a, b}`, `S_1 = {a', b'}`(`a' ↦ a, b' ↦ b`), `S_2 = {b''}`(`b'' ↦ b'`).  全段非空・極限非空(`b` 枝)だが `a` を固定した探索は rung 2 で
  「NONMEMBER」を返す.  対策 = 定理 A (ii)/v441 Cor 2.2 のように**全下位解の差** `D_d` で fibre を作る(T1 では実装済み), T2 では v195–v196 の same-μ repair だけでなく rung-0 解の
  取り替え(`S_0` の別点)を許す設計(§8 Q4).
- (T-ii) 規約漂流: 段ごとに異なる chain map で「MEMBER」を出せば, それは異なる問題の解で, 遷移写像が存在しない(逆系でない).  実例 = 接頭辞規約の逸脱(裁定 1847/1850: own-prefix `ag` は
  2,016 段まで不可視・54,432 段から可視).  対策 = 44 identity 列 gate を各段の標準検査に(既に express 済).
- (T-iii) 非 cofinal: pro-3 lane の逆極限は「核 ⊆ Ω で `Ω/N` が 3 群」の商しか見ない.  玩具: `F = Z`, 条件「`c ≡ 1 (mod 2)`」は 3 冪商で不可視.  R07 では v220 の B(mixed-prime)・C(perfect-core)
  gate がこれに当たり, T2 を閉じても Ihara には B, C が別途要る(v220 §16 規則 8).

## 5. 一様 lift 定理の形 — 障害の同定と, 要る定理(§5.2 は追補 (b′) を統合; §5.4 = Sol 経路との対応表・v2.2 新設)

### 5.1 障害はどこに住むか

定理 B (iv) により, edge `n → n+1` の障害は `coker(B_{n+1}(f))` における残差 `ρ_{n+1}(f)` の類(class-specific), あるいは「`f` を `S_n` 内で動かしたときの最良値」= `ρ_{n+1} mod (im B_{n+1} + 下位解差の像)`
(定理 A (ii) の `K_d` と同形).  rung 0 の次元簿記(§9 の測定と正典値):

```text
source  dim M = |Δ|+1 = 357,128,353
H 標的  dim H_1(K_{3,0};F_3) = 39,680,930  (×2 ブロック)   — source ≫ H 標的: H 部分だけなら全射は次元的には排除されない
P 標的  dim H_1(K_{4,0};F_3): UNKNOWN(PB4 の指数 |Δ| の部分群; χ(PB4)=0 なので指数比例の公式は無い; 測定可)
既知の非全射性: rung 1 (504) で dim A_g^G(K_G) = 405 (v2 addendum §4.2) < 2·(|G|+2) = 1,012
  (標的の H_1 部分: ker(P_3 → G) = K_A^G × ⟨z⟩ (z ↦ 1), rank K_A^G = 1+|G| = 505, ⟨z⟩ ≅ Z が 1 を足して 506 = |G|+2 per block).
```

つまり rung 0 でも `B_0` は全射でなく, A0 は本物の制約である.  同じことが各 `n` で起こるので, 「全 `n` で残差が像に入る」には**残差側の構造**が要る.

### 5.2 要る定理の形と候補型の再評価(追補 (b′) 統合; 在庫 = 裁定 2002 の文献ゲート回答・4 点在庫検査 = 在庫内・新規遠征なし; **v2.2 で D5–D8 の限定・撤回**)

**在庫(逐語 pin).**  (1) LEDGER L1414(裁定 378): 「型 (i) = **Furusho Question 14(Ann. Math. 2010 末尾)として名前つき未解決問題で実在**(副有限版 pentagon⇒hexagon・被引用 84 件走査で追随ゼロ)」;
覚書 FV-L1: 「λ²=24c₂(f)+1 の平方根存在を仮定に置いた形 … 射程は Lie/pro-unipotent/pro-ℓ/pro-nilpotent のみ — 副有限は本人が明示的に未解決と宣言」, 「副有限でも pentagon ⇒ 2-cycle 関係 (I) は成立
(Furusho 指摘)— 未解決は (II) hexagon のみ」.  (2) LEDGER L668: 「**Furusho property(pentagon ⟹ hexagon)の profinite 版は一般には偽**(C1 §4.3・35 例で機械判定・強 11/弱 13)」; 原文 2008.00066 §4.3
(papers/txt 行 3502–3540; 本稿の読解範囲はこの節のみ): Property 4.2(strong: 「For every f N_{F_2} ∈ F_2/N_{F_2} satisfying pentagon relation (2.20) modulo N, there exists m ∈ Z such that 2m+1 represents
a unit in Z/N_ord Z and the pair (m,f) satisfies hexagon relations (2.18), (2.19)」)を満たすのは 35 元中 11(残り 24 は不成立), Property 4.3(weak: charming `f`)は 13(残り 22 不成立); N^(19): pentagon 解
216 中 hexagon を持つのは 36; N^(34): 4096 中 243.  (3) LEDGER L1422(裁定 380 訂正①): 「Furusho Q14 = pentagon⇒hexagon であり、層 (b) が要るのは **converse(hexagon+charming⇒pentagon)** … 正しい家 =
**HS Main Theorem の M₀,₄/M₀,₅ 水準差・HS Prop 7 の置換持ち上げ特徴づけ**」.  (4) LEDGER L1561(裁定 408): 「c₂ 有限版は well-defined に定義できた(定義 D1 …)が、**分離能力は厳密にゼロと否定で確定**」;
c2q_finite_def_v1 R3: 「C2-Q の答は『hexagon だけ』= 分離能力ゼロ」.  (5) LEDGER L2605(裁定 655): dim 𝔤𝔯𝔱₁₂ = 2(本稿では不使用).
NAME-COLLIDE: 本稿の候補型「(b)」と在庫 (3) の「層 (b)」(FAKE-VOID 戦役)は別物.

**在庫 (2) の読みの訂正(D7; Sol 162 §2 末「finite-shadow failures must not be called profinite counterexamples without compatible lifts」).**  L668 の文言「Furusho property の **profinite 版**は一般には偽」は,
引用元の計算(2008.00066 §4.3 の 35 元・有限商 `N^{(19)}`, `N^{(34)}`)からは**従わない** — 有限 shadow の失敗は compatible lift なしに副有限反例と呼べないからである.  正しい読みは
「**有限商水準で一般には偽**(35 元中 24 で Property 4.2 不成立・weak 版は 22/35 不成立)」であり, **副有限版の真偽は在庫 (1)(Furusho Q14)= open のまま**.  この訂正は在庫 (1) と (2) の見かけの緊張
(本人が open と宣言している命題を他方が「偽」と記す)を解消する.  本稿の用途(下記 (N1a) = **一様**恒等式の反証)には有限反例で十分なので, (N1a) の根拠は失われない.

**同名別物ゲート.**  R07 の証人条件は 2 hexagon + 1 pentagon の**三本同時**(v1 P3, v145 Thm 2.2)= 2008.00066 の本来系.  B₃-gentle 系(2401: pentagon なし)では候補型 (b) は空.  以下は本来系.

**(i) 候補型 (b) は群水準を要する(補題 (b′.1)).**  edge `n → n+1` で欠陥類 `E_{H_b}(f) := [hex_b(f)] ∈ H_1(K_{3,n};F_3)`, `E_P(f) := [pent(f)] ∈ H_1(K_{4,n};F_3)`.  候補型 (b) の内容は
「(b-lin) `E_P(f) ∈ (指定部分空間) ⟹ E_H(f) ∈ im B_H` for all admissible f」, 最小形 `E_P(f) = 0 ⟹ E_{H_1}(f) = E_{H_2}(f) = 0`.  v145 Lemma 2.1 (2.4) により `E_{H_b}(f) = 0 ⟺ hex_b(f) ∈ K_{3,n+1}`,
`E_P(f) = 0 ⟺ pent(f) ∈ K_{4,n+1}`, ゆえに最小形は群水準の「(b-grp_n) `f` が `E_{3,n}, E_{4,n}` で三関係を満たし `pent(f)` が `E_{4,n+1}` で成り立つ ⟹ `hex_b(f)` が `E_{3,n+1}` で成り立つ」と同値
= DLL Property 4.2 の塔相対・`m` 固定版.  Fox 線形化は未知数(補正)についての線形化であって欠陥類は群水準の障害と一対一 — **最小形についての要求は弱まらない**(D12: これは最小形 `E_P = 0 ⟹ E_{H_1} = E_{H_2} = 0` についての結論であって, 一般の (b-lin) 型についての結論ではない).

**(i′) 撤回と限定(D5; Sol 162 §2 第 1 点).**  v2.1 の「より弱い Fox 水準の syzygy `λ(E_{H_1},E_{H_2},E_P) = 0` も, 全商で成り立つには語水準の恒等式が要り, それがあれば任意の有限商で
pentagon ⟹ hexagon が従って在庫 (2) と矛盾する ⟹ **形式的 P–H syzygy は存在しない**」を **撤回する**.  誤りは初等的で, **syzygy であること自体からは含意は出ない**: 例えば
`λ = E_{H_1} − E_{H_2}`(関係 `H1 − H2 = 0`)は非自明な線形恒等式だが `E_P = 0` かつ `E_{H_1} = E_{H_2} ≠ 0` を許す(Sol の反例).  含意を導くには **H 欠陥全体を零に強制するだけの独立な恒等式**が要る.
内部反証も立つ: R07 には実際に欠陥加群上の非自明な線形構造 (S1)(return involution θ の冪等分解 `e_± = (1±θ)/2`, v169 (5.1)–(5.3))が在り, かつ在庫 (2) の有限反例も成立している —
v2.1 の推論を認めると両者が矛盾するので, **推論の方が誤っている**(θ-odd 部が v75 の相対 dihedral 原像で処理できても θ-even 部の membership v169 (5.2) が残る = 含意は出ない).  正しい限定形:

```text
(N1a) [射程内で反証]  「`E_P = 0` を代入したとき H 欠陥**全体**を零に強制するだけの独立な恒等式族」(H-forcing syzygy)で,
      全 admissible f・全登録商で**一様に**成り立つものは存在しない.  根拠 = 在庫 (2)(DLL Property 4.2 が 35 元中 24 で
      不成立; `∃m` 版の反例は固定 `m` 版の反例を含意する ⟹ R07 の固定 `m` 設定にも効く).
      **翻訳前提(未証明)**: DLL の商族 `N` と f の族が R07 の登録相対 Frattini 商族 `K_{r,n}` と比較可能であること
      ⟹ (N1a) 自体が条件つきの主張である(§8 Q8).
(N1b) [未排除]        H 欠陥全体を強制しない**より弱い** P–H syzygy 一般は, 上の反例では排除されない(Sol 162 §2).
(N1c) [未排除]        点固有(class-specific / pointed at (m, g760) または選んだ `c_0`)の P–H 恒等式は, **別の点での反例
      では排除されない**.  ゆえに「pointed 形の (b)」は生存しており, その生存の仕方は (c) の pointed 性と同じ層に属する
      (§8 Q6: 両者を別経路として数えるべきか, (c) が (b-pt) を吸収するか).
```

R07 で実在する Fox 水準の恒等式は (S1) return involution θ による hex_1/hex_2 の対称性(v169 §5, v399), (S2) Fox 基本公式の cycle 条件, (S3) 正規化指数 ν(v399/v460)で, いずれも M₀,₄ 水準.

**(ii) 群水準 ⟹ 一様形は閉塞, U3 生存経路の再評価(v2.2 で三分割・D13).**  (α) 有限水準: 在庫 (2)(24/35・22/35 不成立; 失敗窓の割合 36/216, 243/4096).  (β) 副有限: 在庫 (1)(Q14 未解決; しかも `∃m` 形で R07 の固定 `m` を与えない).
(γ) 翻訳機構の不在: char 0・pro-unipotent・lower central・𝔤𝔯𝔱 の証明(`m` を `c₂` から決める, `λ² = 24c₂+1`)vs char 3・relative Frattini・非冪零 roof; `c₂` の**登録済み**有限版(定義 D1)は在庫 (4) により分離能力ゼロ(**ただし D1 についてのみ** — D6; (γ) の残り三根拠 char 0 vs char 3・pro-unipotent vs 相対 Frattini・冪零 vs 非冪零 roof は独立に立つ).
副次: 在庫 (1) の「pentagon ⇒ 2-cycle (I) は副有限でも成立」は hexagon 本体 (II) ではなく (b) を救わない((S1) の裏づけにはなる).

| 経路 | 内容 | 評価(v2.2; 表は D8 で三分割+(d) 追加) |
|---|---|---|
| (b-univ) 一様 syzygy 型 | (b-grp_n) を**全 admissible f・全 edge**で | **射程内で反証**((N1a); 翻訳前提つき).  加えて群水準 Furusho 性が必要で (α)(β)(γ) の機構ゼロ.  v1 §5.2(b) の【文献要請】は**撤回**(v2 のまま) |
| (b-pf) 副有限 syzygy 型 | pentagon ⟹ hexagon を副有限で | **open**(= Furusho Q14, 在庫 (1)).  有限反例からは偽と結論できない(D7).  真なら (b) は復活するが Q14 級の未解決問題 |
| (b-pt) 点固有 syzygy 型 | 点 (m, g760)・選んだ `c_0` に固有の P–H 恒等式 | **未排除 = UNKNOWN**((N1c)).  証明機構は依然ゼロだが, **反例による排除もされていない**.  実質的に (c) と同じ pointed 層(§8 Q6) |
| (a) 層再帰 | `H_1(Ω⁽ⁿ⁺¹⁾)_{V_n} ≅ H_2(V_n;F_3) ≅ Λ²V_n ⊕ V_n`(五項完全列, `Ω⁽ⁿ⁾` 自由; 標的側は `coker(H_2(K_{r,n}) → H_2(V_{r,n}))`)— edge n+1 の障害の共変射影は edge n の線形写像の `Λ²⊕id` で決まる | **降格(保留・候補未満)**: 計算縮約としては死亡(edge 1 の共変部分だけで次元 ~ `d_0²/2 ≈ 8×10¹⁴`, `d_0 = 39,680,930`)・「共変障害が構造的に消える」機構なし |
| (c) 登録契約型 | v174 (2.1) `β − Ba = μβ`, `μ ∈ 𝔧` ⟹ Neumann 級数; v191 (2.2) 源群 `𝒢` 上の普遍 Fox 加群での等式 `ẽ − M d̃ = D̃_2 q` ⟹ 全 matched refinement で `e_n = μ_n d_n`; `q` の存在 ⟺ 三 endpoint 零(v194/v198; universal cover 単連結 ⟹ `ker D_1 = im D_2`) | **生存**(工房が現在明示している 2 経路の一つ; v2.1 の「唯一の生存経路」は**撤回** = D8).  仮説は rung-0 で有限回の replay により検査可能, 三ブロックを対角的に同時に扱うので (b-univ) の反証に触れない(v191 §2).  十分条件のみ・**必要性は未証明**(Sol 162 §1 Q3 逐語: 「No necessity theorem is supplied by these notes」)・成否は A0 後の計算(A5–A8 = 0/3) |
| (d) 一様 cover 型 | 各 edge で `q̃'(ker r^U) = ker r^E`(v526 (0.1)/(4.2), 非集約 owner)または `B'(ker rX) = ker rL`(v537 (2.2), 完全物理 owner)を**有限の語つき column cover** で証明 ⟹ 一つの coarse 解から閉形式 selector で整合族(v526 Thm 4.1 / v537 §4)⟹ v539 (1.1)–(1.3) の型 bridge で v504 Thm 6.1 の初期前件 | **生存・条件つき**(§5.4).  本稿 定理 B (iii)(= v395 (3.4))と**同型の条件を別 owner で**述べ, さらに「有限 cover で証明する手段」と「target family の構成法」を与えたもの.  未証明の前件 = 実 cover(A4/P1 gate)・**完全な** first-rung A0 MEMBER・physical-jet saturation |

(c) についての注意: (1) pointed(distinguished defect `β` に限定)— 在庫 (2) の失敗窓でも pentagon 解の一部は hexagon を持つので「一般には偽」は「点 (m, g760) では偽」を意味しない; 点固有の恒等式を
要求するのは一般機構が無い世界で唯一整合的な形(**v2.2: (N1c) がこれを裏づける** — 点固有の恒等式は別の点での反例では排除されない).  (2) 仮説は rung-0 解 `c_0` の取り方に依存する(v191 Thm 3.1 は pointed ancestry から `M` を compile)— 定理 B (ii) の dead-branch 論点はここで効き,
`c_0` を `S_0 = c_0 + ker` 内で取り替える経路(§8 Q4)と v195–v196 の same-μ repair torsor が唯一の自由度.

**(iii) 在庫 (3)(4) との整合(一段; v2.2 で D6 の限定).**  (S1)–(S3) は M₀,₄ 水準(PB3/F₂)で pentagon を含まず, converse(家 = HS M₀,₄/M₀,₅ 水準差・Prop 7)を与えも否定もしない = 「型 (ii) 分離不変量は存在せず」
(L1414)と整合.
**限定(D6; Sol 162 §2 第 2 点).**  v2.1 は「(S1)–(S3) から作れる不変量は hexagon 側の線形化データのみ = `c₂^fin`(定義 D1)と**同じ入力に依存する**ので R3(分離能力ゼロ)により pentagon の
持ち上げを判定できない」と書いたが, これは **UNKNOWN へ格下げする**.  在庫 (4) が確定させたのは「**登録済みの特定の**有限 c₂(定義 D1)の分離能力が零」であって, 「(S1)–(S3) から構成できる
**あらゆる**不変量の分離能力が零」ではない — 後者を言うには「S1–S3 構成可能な不変量はすべて `c₂^fin` を経由する」という**因数分解定理**が要り, 本稿も在庫もそれを供給しない.
**同じ入力に依存することは同じ分離能力を意味しない**(同じデータの細かい関数が分離することはあり得る).  ゆえに「(S1)–(S3) 由来の別の不変量が pentagon の持ち上げを判定する」可能性は
**排除されていない**(反証されたのではなく未証明 = UNKNOWN).  これは (γ) の裏づけを一つ弱めるが, (γ) の残り三根拠は独立に立つ((ii) の (γ) 参照).
帰結(この設計上の結論は D5/D6 の限定でも変わらない): H を P に従属させる (b) の**一様形**も, その逆(converse・M₀,₅ 水準・open)も使えない; 三ブロックは**同時**に(定理 A (iii) の逐次は
線形代数の順序であって含意ではない)扱う現行設計が正しい.

### 5.3 本稿の結論(定理の成否)

- 定理 A: **成立**(物理商上の有限線形代数; v1 の境界込み定式は注 A.3 で訂正).  A0 に cofinal 定理は不要.
- 定理 B: **成立**(König/Mittag-Leffler; 根なし版).  「全段 MEMBER ⟹ 極限」は自動だが前提が測定不能(命題 C).  得られるのは **lane 証人**まで(注 B.3・D10).
- 「cofinal 両立 lift」定理(T2 全段非空 ⟸ 有限条件): **本稿では閉じない**.  障害 = 各 edge の `coker B_{n+1}` における残差類(§5.1).  閉じる定理の型として**現在明示されている**のは
  (c) 登録契約型(pointed contraction)と (d) 一様 cover 型(v526/v537/v539 → v504, §5.4)の 2 つ; (a) は降格, (b) は**一様形のみ射程内で反証**で pointed 形は未排除.
  v2.1 の「閉じる定理の型は (c) のみ生存」は **撤回**(D8)— それは数学的排除ではなく research-status の記述だった.

### 5.4 Sol 経路(v526 / v537 / v539 → v504)との対応表(v2.2 新設・D9)

Sol 162 §3 の比較を本稿の記号に翻訳して並べる.  **目的は自分の経路の位置を正しく置くこと**であって優劣の宣言ではない — Sol の逐語判定は
「工房の contraction 経路は**実欠陥を指しており** target coverage は弱くてよい」「v537 は full kernel cover ゆえ全 compatible physical fibre の持ち上げを保証し以後の membership 探索を消すが,
その all-edge cover の証明は難しい」「**どちらの定式も相手の欠けた証明書を無償では供給しない**」「v526 の非集約 target と v537 の物理 target は追加の target-kernel lifting 比較なしには
**強弱を順序づけられない**」「**有限 A0 は出発点であって cofinal lift 定理の全体ではない**」である.

| # | 経路 | 前件(仮説) | 結論 | 未証明の前件 / 位置 |
|---|---|---|---|---|
| 定理 B (i)(ii) | 本稿 König / Mittag-Leffler(根なし) | 各段 `S_n ≠ ∅`(全段・完全解集合) | `lim← S_n ≠ ∅` = **lane 証人**(注 B.3).  両立性は**自動** | 前件が**測定不能**(命題 C: `|E_{3,1}| = |e3|·3^{39,680,930}`).  lifting 仮説は不要 = 前件が強い代わりに追加の cover を要求しない |
| 定理 B (iii) | 本稿 = v395 (3.4) 一様 lift | 全 edge で `B_{n+1}(K^D_n) = K^L_n` | `r_n` 全射 ⟹ `S_n^∞ = S_n` ⟹ lane 証人 ⟺ A0 = 1 | 各 edge で有限 rank test だが **edge は無限個**.  owner は v395 の抽象 source/target で, **証明手段を与えていない**(抽象形どまり) |
| (c) | 工房 contraction(v174 pointed Neumann / v191 universal word-pair) | rung-0 で有限回 replay 可能な恒等式 `β − Ba = μβ`(`μ ∈ 𝔧`)/ `ẽ − M d̃ = D̃_2 q`(`q` の存在 ⟺ 三 endpoint 零, v194/v198) | 全 matched relative pro-3 refinement で `e_n = μ_n d_n` ⟹ pointed な全段解 | **U3 = 恒等式の存在が未証明**; **必要性も未証明**(Sol 162 §1 Q3); `c_0` 依存(dead branch・定理 B (ii)); 検査は A0 = 1 の**後**(A5–A8 = 0/3) |
| (d1) v526 | 非集約 owner の相対像等式 | 全 edge で `q̃_{n+1}(ker r^U_{n+1,n}) = ker r^E_{n+1,n}`((0.1)/(4.2))+ **外から与える compatible target family** `(ρ_n)`((4.1))+ `r^U` 全射 | Thm 1.1 = 相対像等式 **⟺** 全 compatible fibre の持ち上げ(必要十分).  Thm 4.1 = 一つの coarse 解 `u_0` から閉形式 selector (2.5) で `lim← U_n` の整合族(以後 membership 探索なし) | 実 R07 の relative-kernel basis cover = **OPEN(A4/P1 gate)**; **target family を仮定に置く**点が構成上の弱み(v537 が除去) |
| (d2) v537 | 完全物理 owner の核 cover | 全 edge で `B'(ker rX) = ker rL`((2.2))+ 固定 literal word `w0` の**関手的** full physical residual `z_n = Φ_n(w0)`((1.2)(1.3)= target family を仮定しない)+ word-bearing columns (3.1) | Thm 2.1 = 物理 fibre lifting(必要十分).  §4 = **完全な** first-rung coarse member + cover ⟹ cofinal physical member | 実 A4 物理 basis columns・固定語 reduction receipt・physical-jet saturation・**完全な coarse A0 MEMBER** すべて OPEN.  Sol 逐語「Grade two alone is not a full initial member」 |
| (d3) v539 | 型 bridge | v537 の `X_n`/`B_n` と v504 の完成源 `P_n`/`B^504_{n,w0}` を結ぶ生成子水準の三恒等式 (1.1)–(1.3) | `B^504_{w0}(p) = Φ^504(w0)`((2.5))= v504 Thm 6.1 の初期完成源前件 | **型精度の改善のみ**で実 cover の証明ではない; その後も v504 の compactness / strictness / separation / physical-jet saturation / side / Cauchy / continuity が要る |

**読み(v2.2 の自己評価 — 自分の経路を過大評価しないための 5 点).**

1. **同型性**: 本稿 定理 B (iii) の条件(v395 (3.4))と v526 (4.2)・v537 (2.2) は **同じ形の条件(「下位解の差の空間の像 = 標的核」)を異なる owner で述べたもの**である.
   v526/v537 が付け加えたのは (α) その条件を**有限の語つき column cover で証明する手段**(v526 Prop 3.1 / v537 §3・Cor 3.1)と, (β) v537 における **target family の構成法**
   (固定語 `w0` の関手的残差 — v526 の「外から与える `(ρ_n)`」という弱みの除去).  したがって**一様 lift 経路について本稿は抽象形しか持っておらず, 具体化は Sol 側が先行している**.
2. **強弱(工房 (c) の位置)**: (c) は**実欠陥 `β` を指す pointed 経路**なので target coverage の要求が弱い(全 relative target-kernel ベクトルを覆う必要がない).  しかしこれは「得」ではない —
   **要求が弱い代わりに供給も無い**: 恒等式の存在(U3)も必要性も未証明で, 検査は A0 = 1 の後にしか始められない.  逆に (d2) は cover さえ取れれば以後の探索を消すが, その cover の証明が難しい.
   Sol の逐語どおり **両者は互いの欠けた証明書を無償では供給しない**.
3. **順序づけ不能**: (d1) と (d2) の強弱は, 非集約 target と物理 target の間の **target-kernel lifting 比較**という別の補題なしには決まらない(Sol 162 §3).  本稿はその比較を持たない(§8 Q7).
4. **共通点**: どの経路でも **有限 A0(定理 A)は出発点**であって cofinal lift 定理の全体ではない.  この一点は全経路が一致しており, **A0 の優先順位は v2.2 でも変わらない**(Sol 162 §2 末).
5. **本稿の寄与の位置**: 定理 A(有限性・完全 fibre)と 定理 B (i)(ii)(根なし König と dead branch)は, どの経路にも共通に効く**土台**である — 特に (d) の「一つの coarse member」の意味を
   「**全下位解の差** `D_d` で作った完全 fibre の一点」に固定するのが 定理 A (ii), その一点が極限まで生きる保証がないと言うのが 定理 B (ii)(Sol 162 §1 Q4 の「`S_0 = c_0 + ker(B_0)` を
   語つきで保持せよ」と同じ内容).  **一様 lift 定理そのものは本稿の寄与ではない.**


## 6. A0 を閉じるための有限検査条件(定理 A の条件 (i)–(xi))と追加測定仕様

```text
(i)   塔の各段 Q'' → Q' の核 V が初等アーベル 3 群で, 5 つの E3 occurrence 自己同型(P ブロックでは 5 つの PB4 occurrence 写像)に保たれる [実行 gate; v441 §7 gate 1]
(ii)  各段の extension データ: transversal・核値 cocycle・V 上の商作用・I^d の occurrence 保存・切り詰め代入 (v441 §7 gate 2–3)
(iii) 44 seed の identity 列 = hexagon/pentagon 語の直接 Fox 列と entrywise 一致(44/44)を各段の標準検査に(規約 canary; T-ii 対策)
(iv)  法的像の完全性: MEMBER は部分 span でよいが, NONMEMBER には完全 presentation 𝒫_d(v444 (2.2)–(2.3), v479 二分岐)が必須; fibre は全下位解差 D_d = ker C_d から(定理 A (ii))
(v)   残差は composed root C_d(v465 (4.1))の直接評価から新規に計算(v479 (4.1)); lower/auxiliary 座標の dense 零検査; 判定は K_d を法として
(vi)  ν: 最終 root の指数対を整数で 0 に(v399/v460; 3 で割る前に整数検査).  頂上まで一様: v460 (1.1) の r_x, r_y の像は 5 occurrence すべてで e3 内の位数 3(1×pc3 内; §9 FAL 行)ゆえ
      Fox(r⁹) = 3(1+r̄+r̄²)Fox(r) = 0 in F_3[e3] — c_x = r_x⁹, c_y = r_y⁹ は rung 5–6 でも H ブロックに Fox 不可視で ν(c_x)=e_x, ν(c_y)=e_y(v460 (1.2)).
      **P ブロックでは自動零ではない**(falsifier 検査 `fal_a0cl_nu_pent_check_v1.g`): r_x, r_y は Δ で位数 9(r_x³, r_y³ ∉ Ω; E4 座標像の位数 coord 6–8: 9/9, coord 9: 9/3, coord 10: 3/9; E3 座標は 3/3).
      ゆえに pentagon slot では s := σ_o(r_x) の像が位数 9 で, Fox(σ_o(c_x)) = (1+s+…+s⁸)·Fox(σ_o(r_x)) = (s−1)⁸·Fox(σ_o(r_x))(char 3: s⁹−1 = (s−1)⁹), F_3[C_9] で (s−1)⁸ ≠ 0 —
      D_4 を法とした零性は**未測定(測定可)**.  v460 §4「does not solve the physical pentagon residual」と整合.  結論: **ν は P ブロックと同時に解く(または Ȳ_4 での c_x, c_y の像を測る)必要があり, 「ν/直接 replay」は free step ではない**
(vii) H ブロック頂上 = e3 の 2 段(rung 5: V = pc3/Φ(pc3) ≅ C_3³, rung 6: V = Φ(pc3) ≅ C_3 中心)の extension データ実体化 — 本稿 GAP で構造のみ確定
(viii) P ブロック: 物理商 Ȳ_4(v403 (1.6))の上で設計.  (P1) 標的群の同定(e4 の 5 座標 context 像; §9: 座標 6–8 の像は位数 |Δ|(核 1, abinv [2,2,9,9] = Δ^{ab}), 座標 9–10 は位数
      119,042,784(核 C_3); 座標 6 像の Q4-粗部分は位数 |Δ|/3, pc4-細核は C_3; ambient e4 = Q4 × pc4, |Q4| = 5.8×10²³, |pc4| = 3¹⁰, |e4| ≈ 3.4×10²⁸; pc4: exponent 3・class 2・
      Frattini 列 [3¹⁰, 3⁴, 1]), (P2) 5 つの pentagon 代入に保たれる特性列(Δ 側の候補: Γ は exponent 9・class 2・abinv [9,9]・Frattini 列 [243, 27, 1] ⟹ V = Γ/Φ(Γ) ≅ C_3², V = Φ(Γ) ≅ C_3³;
      3 座標の像が e4 の同一部分群かは未確認), (P3) 初等アーベル細分 — **未設計・規模 UNKNOWN**; pent(g760) = 1 in e4 は成立(単一実装, §1.2)
(ix)  ブロック順序: H → P → ν(定理 A (iii))または joint; H 解集合の fibre(ker Â_H)を occurrence closure から「lower-零行」として取る(v441 §3)
(x)   直接 replay(A0 = 1 の受理条件): 最終語 C(SLP)で hex_b(g760 C) の Fox 行 ∈ im D_2 over F_3[e3](v145 (2.4) ⟺ ∈ Φ_3(K_{3,0})), pent 同様 over F_3[e4], ν(C) = 0 整数, ρ_* で全下位段 MEMBER と整合
(xi)  NONMEMBER 証明書: 完全 fibre を消す dual + 残差との非零 pairing(v441 §7); 有限 cap は UNKNOWN_RESOURCE(v465 §5)
```

追加測定(既存 GHA 機構への要求・仕様のみ): (M1) rung 5/6 の extension データ生成(v442 の G9 twisting と同じ型で pc3 について; `Q_0` の共役作用は直積ゆえ自明, occurrence 自己同型の `V_5 = C_3³` 上の
3×3 行列 5 本と `V_6 = C_3` 上のスカラー 5 本), (M2) rung 3 grade 2–6 → rung 4 → 5 → 6 の decision-first(v474/642)+ fresh ρ(v479)の反復, 各段で (iii)(v), (M3) P ブロックの (P1)–(P3) の GAP 測定
(標的群・特性列・`dim H_1(K_{4,0};F_3)`・`pent(g760) = 1` in e4), (M4) 最終 (x) の replay checker(task192 terminal の型).

## 7. A0 以降への接続(一段だけ)

A0 = 1 が取れたときに渡す物(v220 §14 の依存鎖の最初の矢印): **形** = 一つの literal source word `c_0 ∈ Ω`(SLP root `C = Compose(…)`, v465 (4.1); 平坦展開不要), ν = 0 の整数証明, 11 occurrence の
endpoint receipt, `f^{(1)} = g760 c_0` が `E_{3,1}, E_{4,1}` で関係を満たすことの直接 replay(v145 Thm 2.2 の受理条件).  **両立系全体ではない** — rung 0 の一点と, 定理 B (ii)/§5.2 (c) 注 (2) に従い `S_0` の
他の点へ戻れるよう解集合 `c_0 + ker` の生成データ.  **次段**: A2 二入力 specializer(v221)→ v216 / v188 → v214 pointed `μ_1` → v191 `M` → v198 三 endpoint → v197 `q` → v174 relative pro-3 lift(T2)
→ B(mixed-prime)・C(perfect-core)→ 証人.  FAKE/IHARA の語は本稿で用いない(用語改定 20260823).

## 8. Sol への問い(v2 = 回答済み / v2.2 の新規 Q6–Q8)

**回答状況(Sol 162 §1 — Q1–Q5 は本版で閉じる).**  Q1 = **受理**(物理商による定義訂正つき; 完全 fibre MEMBER + 正規化座標条件 + 一回の literal 直接 replay で有限 A0 は閉じ, cofinal/全 edge 全射性は
その有限終端の追加条件ではない.  v220 Δ526 に明文化済).  Q2 = **構造は既知だが実体化されていない**(`C_3³`, `C_3` の 2 因子は述べられた群入力の下で従うが, marked extension データと 5 occurrence 作用の
receipt ではない; P 標的は v403 (1.6) + 先行する v401/v402 の owner 定義, **5 座標像の位数だけでは共通 occurrence 安定部分群を同定しない**; H の正規化子から P 側の不可視性は自動的には従わず
v2.1 の位数 9 警告は保持).  Q3 = v174 は pointed contraction, v191 はより強い有限 replay 可能な構成, v194/v198 はその特定構成の endpoint gate — **必要性定理は無い**(ゆえに (c) 唯一性は撤回 = D8).
Q4 = **`S_0 = c_0 + ker(B_0)` を語つきで保持せよ**(次 edge の恒等式が `c_0` で失敗しても `S_0` の別点は否定されない; v195/v196 は base point 取り替えの完全実装ではない).  Q5 = 群入力の下で
`|E_{3,1}| = 119,042,784·3^{39,680,930}` は**式として従う**(新規 GAP ではない); 明示列挙は実務上排除されるが「後段の有用な商・記号表現・圧縮計算が不可能」は言えない.  以下は v2.2 の新しい問い.

**(v2 の問い — 上の回答で閉じる; 原文は保存する.)**

- **Q1(裁定 2002 の express 文に置換)**: T1 の各段で boundary 行「SURJECTIVITY / COFINAL LIFT: NOT PROVED」は「下位解の自動 lift 未証明」の意味であり, 頂上(H ブロック = e3, P ブロック = `Ȳ_4`, ν)を
  完全 fibre で MEMBER 決定すれば A0 = 1 と受理する — 同意するか.  同意なら v220 に明文化を請う.
- **Q2** H ブロック頂上 = `e3` の 2 段(`V = pc3/Φ(pc3) ≅ C_3³`, `V = Φ(pc3) ≅ C_3`)と P ブロック(`Ȳ_4` 上)の塔は既存 note で設計済みか(v442/v443 の G9 twisting の pc3/pc4 版).  P ブロックの標的群の同定
  (§6 (P1))の正本は v401–v403 のどれか.
- **Q3** T2 の登録路線は v174(pointed Neumann)と v191(universal word-pair)のどちらが主か.  いずれかの**必要性**(証人が存在すれば恒等式も存在する)を示す note はあるか.  なければ U3 の存在定理の
  候補証明方針についての見解を請う(候補型 (b) は §5.2 で閉塞と判定 — **v2.2 で「一様形のみ射程内で反証・副有限形は open・pointed 形は未排除」に限定**, D5/D8).
- **Q4** v174/v191 の恒等式が A0 で得た `c_0` に対して失敗した場合, `S_0 = c_0 + ker` の別点へ retreat する経路は設計に含まれるか(v195–v196 は same-μ repair であって `c_0` の取り替えではないと読んだ).
- **Q5** 命題 C の値 `|E_{3,1}| = |e3|·3^{39,680,930}`(rung 1 = `P_3/Φ_3(ker(P_3 → e3))`)は登録塔の定義と一致するか.  一致するなら「rung ≥ 1 は射影と定理でのみ扱う」を v220 §16 の規則として明文化することを提案する.

**Q6(v2.2 新規・(b-pt) と (c) の層).**  (N1c) により「点固有の P–H 恒等式」は反例で排除されていない.  v191 の universal word-pair 恒等式は `E_P` と `E_H` を**対角的に同時に**扱う(v191 §2)ので,
pointed 形の (b) は (c) の特別な場合として吸収されるのか, それとも独立な候補として登録すべきか.  吸収されるなら §5.2 の表から (b-pt) 行を落として (c) に注記する.
**Q7(v2.2 新規・owner の選択).**  本稿 定理 B (iii)(v395 (3.4))・v526 (4.2)・v537 (2.2) は**同型の条件を異なる owner で**述べている.  R07 の登録塔について, どの owner の条件を「主」として
証明に行くのが最短か.  Sol 162 §3 は「v526 と v537 は追加の **target-kernel lifting 比較**なしには順序づけ不能」と述べるが, **その比較自体を一つの補題として立てる**価値はあるか
(= 非集約核と物理核の間の像の比較; 立つなら (d1)/(d2) の一方に資源を集中できる).
**Q8(v2.2 新規・(N1a) の翻訳前提).**  (N1a) の「DLL の商族 `N` と f の族が R07 の登録相対 Frattini 商族 `K_{r,n}` と比較可能」を厳密にする note は在庫にあるか.  無ければ (b-univ) の「射程内で反証」も
**条件つきのまま**据え置き, claim boundary もそう記す(本版はそうしている).

## 9. 検算 artifacts(scratchpad/, sha16 = SHA-256 先頭 16 hex)

- `a0_cofinal_layers_v1.g` `a63ffbf51b62ca69` / 出力 `a0_cofinal_layers_v1_output.txt` `f2c198a8664cad28`(自作): pc3/pc4 の構造, `|Q_0|`, `|Q4|`, `|e3|`, `⟨a,c⟩`-像の指数と `z3` の所属, `ker(e3 → Q_0)`, 階数下界.
- `a0_cofinal_layers_v2.g` `5f648fda768fa734` / 出力 `a0_cofinal_layers_v2_output.txt` `ee6147ba6e1a9192`(自作): v2 prelude(joint 群)で `Γ` の Frattini 列・E4 座標像・粗/細分解.
- `fal_a0cl_nu_pent_check_v1.g`(**falsifier 作**, v2.1 で追加; joint 群を読む; 本稿で再実行, 出力は末尾 FAL2 行): `pent(g760) = 1` in e4(5 slot 規約 true・occurrence 値の位数 9), `Θ(r_x), Θ(r_y)` の Δ での位数 9, 10 座標での像の位数.
- `fal_a0cl_e3check_v1.g`(**falsifier 作**; 本稿は再実行のみ = 同一実装の第二執行であって第二系統ではない): `hex_b(g760) = 1` in e3, `e3 = AC × ⟨z3⟩`, occurrence 像 = AC, v460 の r_x/r_y の像の位数,
  `dim H_1(K_{3,0};F_3)` exact.

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
FAL hex1(g760)=1 in e3: true  hex2(g760)=1 in e3: true
FAL hex1 order 1 hex2 order 1 (coarse Q0 parts trivial: true true)
FAL z3 central true order 3 z3 in AC false AC meet <z3> order 1 => e3 = AC x <z3>: true
FAL |K3|=81 |Phi(K3)|=3 Phi(K3) <= AC: true z3 in Phi(K3): false |AC meet K3|=27 AC meet K3 abinv [ 3, 3 ] exponent 3
FAL occurrence fxy/fxz/fyz/fux/fuy image order 39680928 equals AC: true (5/5)
FAL v460 r_x/r_y image in e3 via fxy/fxz/fyz/fux/fuy: orders 3 3 in K3(=1xpc3): true true (5/5)
FAL rank K_A = 1 + |AC| = 39680929  => dim H_1(K_{3,0};F_3) = rank K_A + 1 = 39680930
FAL2 Theta(r_x) in Gamma true order 9  Theta(r_y) in Gamma true order 9
FAL2 r_x^3 in Omega (cube trivial in Delta): false  r_y^3 in Omega: false
FAL2 coord 1 r_x,r_y image orders: 3 3
FAL2 coord 2 r_x,r_y image orders: 3 3
FAL2 coord 3 r_x,r_y image orders: 3 3
FAL2 coord 4 r_x,r_y image orders: 3 3
FAL2 coord 5 r_x,r_y image orders: 3 3
FAL2 coord 6 r_x,r_y image orders: 9 9
FAL2 coord 7 r_x,r_y image orders: 9 9
FAL2 coord 8 r_x,r_y image orders: 9 9
FAL2 coord 9 r_x,r_y image orders: 9 3
FAL2 coord 10 r_x,r_y image orders: 3 9
FAL2 pent(g760) in e4: f5f4=f1f2f3 true ; f5f4=f3f2f1 true ; f4f5=f1f2f3 true ; f4f5=f3f2f1 true   (4 slot conventions, wrapped line joined)
FAL2 each occurrence value order: [ 9, 9, 9, 9, 9 ]
```

整合: 座標核 (9,9,9,9,9,1,1,1,3,3) = v1 P1(task176); E3 像 39,680,928 = v220 Δ76 の context-image order; `Δ^{ab} = [2,2,9,9]` = errata §5.1; `|Φ(Γ)| = 27`, `Γ/Φ(Γ) ≅ F_3²` = v2 addendum P10.
新規: pc3/pc4/Γ の Frattini 列, `e3 = AC × ⟨z3⟩`, `dim H_1(K_{3,0};F_3) = 39,680,930`, E4 像の粗/細分解, r_x/r_y の e3 像.

## 10. Claim boundary と各版の変更点(v1 → v2 → v2.1 → v2.2)

```text
A0 = FINITE LINEAR MEMBERSHIP (dim 357,128,353) ON THE PHYSICAL QUOTIENT Ẑ, NO INVERSE LIMIT:  PAPER (定理 A; v405 (4.2)/v403 (1.9)/v1 §1/v145 Lemma 2.1)
T1 TOP COMPLETE-FIBRE MEMBER <=> A0 = 1; ANY RUNG NONMEMBER => A0 = 0:                          PAPER (定理 A (i)(iv))
H-BLOCK TOWER ABOVE Q0: TWO RUNGS (C_3^3, C_3); 19 GRADE DECISIONS FOR THE CHOSEN FILTRATION:     PAPER + GAP (系 A.1; not a canonical invariant; extension data NOT MATERIALIZED)
P-BLOCK TOWER (ON Ȳ_4 = v403 (1.6)):                                                            NOT DESIGNED; SIZE UNKNOWN (e4 level, |e4| ≈ 3.4×10^28); pent(g760)=1 in e4 HOLDS (single implementation)
NU NORMALIZER c_x,c_y (v460 (1.1)):                                                               FOX-INVISIBLE IN H BLOCK UP TO e3; NOT AUTOMATICALLY ZERO IN P BLOCK (r_x,r_y order 9 in Delta; image mod D_4 UNMEASURED) => NU SOLVED JOINTLY WITH P, NOT A FREE STEP
T1 BOUNDARY LINES "SURJECTIVITY / COFINAL: NOT PROVED" (v465/v466/609):                          = AUTOMATIC LIFT UNPROVED, NOT A CLOSURE CONDITION
T2: ALL RUNGS NONEMPTY (UNROOTED) <=> LANE WITNESS ONLY (registered pro-3 lane + nu gate);   [v2.2 NARROWED, D10]
  COMPATIBILITY AUTOMATIC; SIDE GATES (marking/formation/onto/settlement) NOT IMPOSED; B/C INVISIBLE TO THE 3-ADIC SYSTEM:              PAPER (定理 B = v169 Thm 4.1 unrooted + Mittag-Leffler; 注 B.3).  NOT AN UNQUALIFIED WITNESS
T2 RUNG 1 SIZE = |e3|*3^39,680,930:                                                               PAPER + GAP (命題 C, exact)
UNIFORM LIFT THEOREM / U3 EXISTENCE:                                                              NOT PROVED
  (b) UNIFORM FORM (H-forcing syzygy, all admissible f):  REFUTED WITHIN SCOPE (stock (2)); TRANSLATION PREMISE UNPROVED   (N1a)
  (b) PROFINITE FORM:                                     OPEN (= Furusho Q14, stock (1)); finite counterexamples do NOT settle it  (D7)
  (b) POINTED / CLASS-SPECIFIC FORM:                      UNKNOWN, NOT EXCLUDED                                            (N1c)
  (a) LAYER RECURSION: DEMOTED;  (c) CONTRACTION: SURVIVING;  (d) UNIFORM COVER (v526/v537/v539 -> v504): SURVIVING, CONDITIONAL  (5.4)
"FORMAL P-H SYZYGIES DO NOT EXIST" (v2.1):                                                        WITHDRAWN (D5)
"EVERY S1-S3 INVARIANT HAS ZERO SEPARATING POWER" (v2.1):                                         WITHDRAWN -> UNKNOWN (D6; needs a factorization theorem through c2)
"(c) IS THE SOLE POSSIBLE ROUTE" (v2.1):                                                          WITHDRAWN (D8; research status, not a mathematical exclusion)
CURRENT PRECISION-TWO WORK = RUNG 3 = EDGE 2,016 -> 54,432 (NOT 54,432 -> Q_0):                    注 1.3 (D11; Sol 162 §0)
NEW LITERATURE REQUEST:                                                                           NONE (v1 §5.2(b) request WITHDRAWN)
A0 MEMBER / NONMEMBER / COMMON / COMPATIBLE LIFT / FAKE / IHARA:                                  NOT DECLARED
verified:                                                                                         false
```

**v1 → v2 の変更点(裁定 2002 の要修正 2 点・軽微 7 点・追補統合).**
- C1(要修正 1): 定理 A を物理商 `Ẑ = Z̄/D̃_0`(v403 (1.6)–(1.9))上で述べ `D̃_0 = 0` に; v1 の「`S_d = c + D_d`」は境界を filtration に含めない定式では偽(falsifier 反例, 注 A.3 に記録); 境界込みの正しい
  `D_d = A^{−1}(D̃_0+F^d)`, `K_d = ((A(M)∩(D̃_0+F^d)) + D̃_0 + F^{d+1}) ∩ F^d / F^{d+1}` を併記.  H ブロック・19 grade・rung 1–6 は無傷; P ブロック塔は商形で設計と明記.
- C2(要修正 2): §2/§4 の帰属を訂正 — v465/v466/609 の boundary 行は T1 の edge(自動 lift 未証明 ≠ 閉鎖条件); v460 の `Ω_0 = ker(F→Q_0)` を採用し v1 の `Ω_0 := Ω` を `Ω⁽⁰⁾ = Ω` に改名; v460 §4 の
  「核 ⊊ Ω₀」は T1 rung 5–6 と T2 の両方と明記.  Q1 を裁定 2002 の express 文に置換.
- C3(軽微 a): 定理 B (i) を「v169 Thm 4.1 の**根なし版**」と明記(v169 の `𝒮_n` は条件 5「reduce to the fixed earlier partial word」つきの根付き版; 差 = (ii) dead branch); `S_n` を `Ω/(Ω⁽ⁿ⁺¹⁾ ∩ ker ν)` 上で定義し
  `r_n` の well-definedness と ν gate の可換性を記述.
- C4(軽微 b): 命題 C を exact に(`e3 = AC × ⟨z3⟩` ⟹ `K_{3,0} = K_A × ⟨z³⟩` ⟹ `dim H_1 = 39,680,930`); §5.1 の 504 水準の標的次元を `2(|G|+2) = 1,012` に訂正(v1: 1,010).
- C5(軽微 c): ν の rung 5–6 延長(§6 (vi)): r_x, r_y は 5 occurrence で e3 内の位数 3 ⟹ `Fox(r⁹) = 0` ⟹ c_x, c_y は頂上でも Fox 不可視.
- C6(軽微 d): 「rung-0 の有限恒等式」を「v191 (2.2) = 源群 𝒢 上の普遍 Fox 加群での等式・有限回の replay で検査可」に表現修正.
- C7(軽微 e): §1.2 に Lemma 2.1 の適用前提 `hex_1(g760) = hex_2(g760) = 1` in e3(falsifier 検査・再実行)を引用; pentagon の e4 での自明性は未検査と明記.
- C8(軽微 f): 「19」は選択した filtration に対する決定回数で正準不変量ではないと注記(`C_3⊕C_3²` 切りで `Q_0` の上 2+4+2 など).
- C9(軽微 g): P ブロック塔 = 未設計・規模 UNKNOWN(e4 水準・`|e4| ≈ 3.4×10²⁸`)を claim boundary に明示.
- C10: 追補 §5.2(b′) を §5.2 に統合((b) 閉塞・(a) 降格・(c) 生存・文献要請撤回・NAME-COLLIDE 注記); §9 に falsifier 検査の再実行出力を追加.

**v2 → v2.1 の変更点(司令塔小発注; falsifier 新規 GAP `fal_a0cl_nu_pent_check_v1.g` の反映).**
- D1(必須・§6 (vi)/§0/§3 系 A.1/§10): (a) `pent(g760) = 1` in e4 成立(5 slot 規約 true・各 `f_j` 位数 9; 単一実装)— §1.2/§6 (viii)/claim boundary の UNKNOWN を更新.  (b) v460 (1.1) の r_x, r_y は Δ で位数 9(r_x³, r_y³ ∉ Ω; E4 座標像 coord 6–8: 9/9, coord 9: 9/3, coord 10: 3/9; E3: 3/3)⟹ H 塔では c_x, c_y は Fox 不可視だが P ブロックでは `Fox(σ_o(c_x)) = (s−1)⁸·Fox(σ_o(r_x))`(s 位数 9, `(s−1)⁸ ≠ 0` in F_3[C_9])で自動零ではない(D_4 を法とした零性は未測定・測定可; v460 §4 と整合)⟹ **ν は P ブロックと同時に解く — 「ν/直接 replay」は free step ではない**(一文 gap・§6・claim boundary に反映).
- D2(軽微・§2 表): 「`ker(F→e3)`」→ `σ_o^{−1}(K_{3,0}) = ker(F→AC)`(F の e3 像は AC・指数 3; rung 5 は `ker(F→AC/Φ(pc3))`; ⊊ Ω₀ は不変); 「v465 §2.2」→「v465 Prop 2.2(§2)」.
- D3(軽微・定理 B (iv)): `B_{n+1}(f)` の定義域を `(Ω⁽ⁿ⁺¹⁾ ∩ ker ν)/(Ω⁽ⁿ⁺²⁾ ∩ ker ν)` に制限し well-definedness を明記.
- D4(軽微・定理 A (iv)/系 A.1): 「誘導される e3 の自己同型」→「`AC = Δ/K` の自己同型」; filtration の actor 安定性は `I` が `k[e3]` の両側イデアルであることから, `1×pc3` の特性性は `Hom(pc3, Z(Q_0)) = 0` から(falsifier 再検査の根拠・本稿未再計算).

**v2.1 → v2.2 の変更点(Sol(Astra)返書 162 §2 の条件付き受理に応える narrowing).  定理 A・定理 B・命題 C とその証明は不変; 新規計算なし.**
- **D5(必須・撤回・§5.2 (i′)/§0/要約/§10)**: 「**形式的 P–H syzygy は存在しない**」を **撤回**.  syzygy であること自体からは pentagon ⟹ hexagon は出ない(Sol の反例: 関係 `H1 − H2 = 0` は
  `P = 0` かつ `H1 = H2 ≠ 0` を許す).  内部反証も立つ — R07 には実在の線形構造 (S1)(θ の冪等分解 v169 (5.1)–(5.3))が在り, かつ在庫 (2) も成立しているので, v2.1 の推論を認めると矛盾する.
  限定形 **(N1a)**(一様 H-forcing syzygy = 翻訳前提つきで射程内で反証)/ **(N1b)**(より弱い P–H syzygy は未排除)/ **(N1c)**(点固有恒等式は別の点の反例では排除されない)に置換.
- **D6(必須・限定・§5.2 (iii)/(ii)(γ)/§10)**: 「(S1)–(S3) から作れる不変量は分離能力ゼロ」を **UNKNOWN へ格下げ**.  確定しているのは登録済み定義 D1 の `c₂^fin` についてのみ(在庫 (4) R3)で,
  全 S1–S3 構成可能不変量へ一般化するには「`c₂^fin` を経由する**因数分解定理**」が要る(未供給).  同じ入力に依存することは同じ分離能力を意味しない.
- **D7(必須・在庫の読み・§5.2 在庫)**: L668 の「Furusho property の **profinite 版**は一般には偽」は有限 shadow の反例からは従わない(compatible lift 不在)⟹ 「**有限商水準で**一般には偽」と読み替え,
  副有限版は在庫 (1)(Q14)= **open** のままとする.  在庫 (1) と (2) の見かけの緊張が解消.  (N1a) の根拠には有限反例で足りるので影響なし.
- **D8(必須・撤回・§5.2 表/§5.3/§0/§10)**: 「(c) が唯一の生存経路」を **撤回**(research-status の記述であって数学的排除ではない; Sol 162 §1 Q3「No necessity theorem is supplied」).
  §5.2 の表を **(b-univ)/(b-pf)/(b-pt)** に三分割し, **(d) 一様 cover 型**(v526/v537/v539 → v504)を経路として追加.
- **D9(必須・新設・§5.4)**: 「**Sol 経路との対応表**」を新設 — 定理 B (i)(ii) / 定理 B (iii) / (c) / (d1) v526 / (d2) v537 / (d3) v539 の**前件・結論・未証明部分**を並べ, 自己評価 5 点
  (同型性・強弱・順序づけ不能・共通点・本稿の寄与の位置)を明記.  特に「本稿の一様 lift 経路は抽象形どまりで具体化は Sol 側が先行」「(c) は要求が弱い代わりに供給も無い」を明記.
- **D10(必須・限定・§4 注 B.3/§0/§5.3/§10)**: 「全段非空 ⟺ 証人」を **lane 限定**に.  定理 B が与えるのは `lim← S_n` の元 = **lane 証人**(登録 pro-3 lane + ν gate のみ)であって無条件の証人ではない.
  side gate(marking/formation/onto/settlement)は各段で restriction と可換なら `S_n` に追加でき König はそのまま通る(未確認・射程外); B(mixed-prime)/C(perfect-core)は 3 冪逆系では**原理的に見えない**((T-iii)).
- **D11(軽微・§1.3 注 1.3/系 A.1/§10)**: 段の名指しの辞書を追加 — **現行 precision-two 作業 = rung 3 = edge `2,016 → 54,432`**(`54,432 → Q₀` = rung 4 は未着手; Sol 162 §0 1. の前提訂正).
  **NAME-COLLIDE「rung」**を登録: Sol の "first rung" = T2 relative Frattini rung 1 = A0 全体(本稿 T1 の rung 1..6 とは別の数え方).
- **D12(軽微・§5.2 (i))**: 「要求は弱まらない」を「**最小形についての**要求は弱まらない」に限定(一般の (b-lin) 型についての結論ではない).
- **D13(軽微・§5.2 (ii) 見出し・(γ))**: 「群水準 ⟹ 閉塞」を「群水準 ⟹ **一様形は**閉塞」に; (γ) の根拠から c₂ 由来の一項を D6 により降格し, 残り三根拠(char 0 vs char 3・pro-unipotent vs
  相対 Frattini・冪零 vs 非冪零 roof)は独立に立つと明記.
- **D14(軽微・§8)**: Q1–Q5 に Sol 162 §1 の回答を記録して閉じ, 新規 **Q6**(pointed (b) と (c) の層の関係 — v191 が (b-pt) を吸収するか)・**Q7**(owner の選択 = v395 (3.4)/v526 (4.2)/v537 (2.2) の
  どれを主に行くか; 非集約核と物理核の比較補題を立てる価値)・**Q8**((N1a) の翻訳前提を厳密にする note の在庫)を追加.

**v2.2 が変えなかったもの(Sol の保持判定).**  定理 A(物理商 `Ẑ` 上の有限厳密性・完全下位 fibre `D_d`)/ 注 A.3(境界込み定式の訂正)/ 系 A.1 の 19 grade 勘定と注(f)/ 注 A.2(NONMEMBER の非対称)/
定理 B (i)–(iv) とその証明 / 注 B.0(根なし vs 根付き)/ 注 B.2(3 つの失敗型)/ 命題 C / §6 の有限検査条件 (i)–(xi)(特に (vi) = **ν は P ブロックと同時**)/ §7 / §9 の機械出力と sha16.

`R07_A0_COFINAL_LIFT_TWO_TOWERS_FABLE_V2_2`
