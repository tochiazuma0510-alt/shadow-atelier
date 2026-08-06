# Brown 1301.3053 Prop 6.4・σ̃ の整構造・深さ propagation の正典範囲 逐語 v1

- **依頼**: 裁定 708・文献要請 C-1(高優先)。P-C-4「A₁₂@691=1」予言の可否判断材料 — 合同 {σ̃₃,σ̃₉}−3{σ̃₅,σ̃₇} ≡ 0 mod 691 の正典保証深さの精密化。**解釈判断は書かない**(UNKNOWN は UNKNOWN と明記)。
- **対象 PDF**: `papers/brown-2013-1301.3053-depth-graded-motivic-mzv.pdf`(arXiv:1301.3053v2, 2020-01-10)
- **読了頁申告**: 本タスクで画像照合(150dpi)= **pp.3, 12, 18, 24**(+ 前タスクで照合済みの p.25 を再引用)。テキスト全文走査(pdftotext, 全 34 頁)で "691" "144" "propagat" "depth five/six" "integral" "lattice" "[20]" の全出現を確認。
- 前ノート `docs/scout/brown_eq14_verbatim_v1.md` は不改変。

---

## 1. Proposition 6.4 の主張文全文(§6.4, p.18 — 画像照合済み・逐語)

### 1.1 前文(p.18)

> "**6.4. Parity relations.** The following result is well-known, and was first proved by Tsumura [35], and subsequently in ([21], theorem 7). We repeat the proof for convenience. It has subsequently been extended to multiple polylogarithms by Panzer [28]."

### 1.2 主張文(p.18・逐語)

> "**Proposition 6.4.** *The components of ls in weight N and depth r vanish unless N ≡ r mod 2. Equivalently, ρ(ls) consists of polynomials of even degree only.*"

### 1.3 内容の整理(論文記載の事実のみ)

| 項目 | 内容 | 出典 |
|---|---|---|
| なにを主張するか | **消滅(vanishing)の主張**: ls(linearized double shuffle の解空間)の weight N・depth r 成分は N ≢ r (mod 2) なら 0。同値な言い換え: 多項式表現 ρ(ls) は偶数次多項式のみ | Prop 6.4, p.18 |
| どの空間で | **ls**(ℚ 上の bigraded ベクトル空間・§5 で定義・linearized double shuffle 解) | p.18 |
| 「propagate」への言及 | **Prop 6.4 自身には合同・propagation の言明は一切ない**。純粋にパリティによる消滅命題 | p.18(全文照合) |
| 仮定 | f が ρ(dg_r^m) の像に入ること…と証明冒頭にあるが(下記)、主張自体は ls の成分についての無条件の言明。証明は linearized stuffle 関係式 (6.9)(6.12) のみ使用 | p.18 |
| 出典系譜 | Tsumura [35] が初証明・[21](Ihara–Kaneko–Zagier)theorem 7・Panzer [28] が multiple polylog へ拡張 | p.18 |

証明冒頭(p.18・逐語): "Proof. Let f ∈ ℚ[y₀,…,y_r] be in the image of ρ(dg_r^m). In particular it satisfies the linearized stuffle relations, (6.9) and (6.12). Following [21], consider the relation …"(以下パリティ計算。結び: "((−1)^{deg f} − 1) f(y₀,y₂,y₁,y₃,…,y_r) = 0 . Therefore, in the case when deg f is odd, the polynomial f must vanish. □")

### 1.4 対をなす命題(§4.4, p.12 — 画像照合済み・逐語)

> "**4.4. Depth-parity.** The following proposition is a consequence of Tsumura's result on double shuffle equations (proposition 6.4).
>
> **Proposition 4.3.** *The depth-graded motivic Lie algebra dg^m vanishes in bidegrees with different parity. More precisely, it vanishes in weight N and depth r if N ≢ r (mod 2).*
>
> Equivalently, if n₁ + … + n_r ≢ r (mod 2), and n₁ + … + n_r > 2 then
>
> (4.4)  ζ^m_𝔇(n₁, …, n_r) ≡ 0 (mod products) ."

さらに(p.12): "**Proposition 4.4.** *The differentials d^r vanish if r is odd.*"(depth スペクトル系列 §4.5 の奇数次微分の消滅・証明は Prop 4.3 のパリティによる)。

### 1.5 Prop 6.4 が (8.8) 合同の文脈でどう使われているか(p.25 — 前タスクで画像照合済み・逐語再掲)

> "Using the depth-parity proposition 6.4, one can show that the corresponding congruence
>
> {σ̃₃, σ̃₉} − 3{σ̃₅, σ̃₇} ≡ 0  mod 691 ,
>
> propagates to depth five also."

- **導出の詳細(なぜ prop 6.4 から深さ 5 への propagation が出るか)は論文に書かれていない**("one can show that" のみ)= 過程 UNKNOWN。
- 導出値(パリティの直接適用・根拠 = Prop 6.4 の主張文): weight N = 12, depth r = 5 は 12 ≢ 5 (mod 2) なので ls(および Prop 4.3 により dg^m)の bidegree (12,5) 成分は 0。weight 12, depth 6 は 12 ≡ 6 (mod 2) なので **Prop 6.4 は bidegree (12,6) の消滅を強制しない**(これはパリティ計算の事実であり、深さ 6 の合同の成否については何も言わない)。

---

## 2. σ̃(canonical lift)の整構造/格子

### 2.1 σ̃ の一般定義 = 任意の lift(§8.4, p.24 — 画像照合済み・逐語)

> "The map d can be computed explicitly as follows. **Choose a lift σ̃_{2n+1} of every generator σ_{2n+1} ∈ dg₁^m to g^m**, and decompose it according to the 𝔇-degree:
>
> σ̃_{2n+1} = σ^{(1)}_{2n+1} + σ^{(2)}_{2n+1} + σ^{(3)}_{2n+1} + … ,"

続き(p.25 冒頭 — 画像照合済み・逐語): "where σ^{(i)}_{2n+1} is of 𝔇-degree i, and σ^{(1)}_{2n+1} = σ_{2n+1}."

(注意: pdftotext ではチルダが脱落する。p.24 の画像で σ̃(チルダ)を確認済み。)

### 2.2 Examples 8.5 の σ̃ = Drinfeld associator による canonical な特定 lift(p.25 — 画像照合済み・逐語)

> "**Examples 8.5.** The elements σ̃₃, σ̃₅, σ̃₇, σ̃₉ **defined by the coefficients of ζ(3), ζ(5), ζ(7), and ζ(9) in weights 3,5,7,9 in Drinfeld's associator** are canonical, and we have (8.8) …"

- これが合同式に現れる σ̃ の**定義の全文**。これ以上の正規化・明示式は当該箇所にない。
- 補助(p.3 脚注 1 — 画像照合済み・逐語): "in fact, one can define canonical generators σ_{2n+1} to be the coefficient of ζ^m(3, 2, …, 2), with n−1 twos, in a motivic Drinfeld associator Φ^m = Σ_w ζ^m(w)w. However, this definition is not explicit and most of the coefficients of σ_{2n+1} defined in this way are not known explicitly."
- Φ の係数規約(§2, p.9 付近・テキスト照合): "Here, we use the convention from [4]: the coefficient of the word e_{a₁} … e_{a_n} in Φ, for a_i ∈ {0,1}, is the iterated integral …"
- 関連(p.25 末尾・前タスク照合済み): weight 3 の canonical lift は [7](Brown, Zeta elements in depth 3)で σ^{(3)}_{2i+1} を構成 — "we showed in [7] how to construct canonical elements σ^{(3)}_{2i+1} modulo depths ≥ 5, which enables one to write down the differential d explicitly."

### 2.3 「≡ 0 mod 691 がどの ℤ-格子上の言明か」

- **論文はこの合同の基礎となる ℤ-構造(格子)を定義していない = UNKNOWN**。根拠となる走査結果:
  - "lattice" は全文に出現ゼロ(grep)。
  - "integral" の実質的出現は Example 8.4(p.24・画像照合済み)の "**Choose integral generators:** f₁₂ = [x₁⁸, x₂²] − 3[x₁⁶, x₂⁴] …"(period polynomial 空間 S の整生成元の選択)のみ。
  - 写像 e の整性(p.25・逐語): "the differential d is related to our map e (**which is defined over Z**) up to a non-trivial isomorphism of the space of period polynomials."
  - ē₁₂ の明示係数(p.24・画像照合済み・逐語): "ē₁₂ = x₃⁷x₄ − 116 x₁³x₂²x₃²x₄ − 57 x₁²x₂⁵x₄ + … (118 terms in total)"(表示されている係数はすべて整数。全 118 項の整性の明示的主張は**なし** = UNKNOWN)。
  - 合同の意味の参照先として指定されているのは Ihara [20] p.258 の 'key example' のみ(§4 参照)。
- **144 の由来と 691 との互いに素性**: (8.8) の係数は 691/144(p.25・画像照合済み)。144 は論文中この一箇所のみに出現(grep)。導出値: 144 = 2⁴·3²、691 は素数、ゆえに **691 ∤ 144**(gcd(691,144)=1)。したがって「mod 691」で係数 691/144 は well-defined に 0(この最後の一文の「well-defined」の基礎構造は上記のとおり論文未定義 = UNKNOWN、算術事実のみ記録)。
- σ̃ 自身の係数(Drinfeld associator の係数 = MZV の実数値/その ℚ-線形結合)の分母・整性について論文は**何も述べていない** = UNKNOWN。

---

## 3. 深さ 6 以上について

**記述なし。** 根拠(全文走査):

- 合同の propagation に関する言明は p.25 の一文 "propagates to depth five also" が**唯一**(grep "propagat" の全出現 = この 1 箇所)。
- "depth six" / 深さ 6 への言及は合同の文脈に存在しない。
- 他の "depth ≥ 5" 言及はすべて別トピック:
  - §1.4.3(p.6・テキスト照合): "nor can we presently rule out the existence of relations of the form {e_f, σ_{2n+1}} ∈ Lie₅ ls₁ which can only occur in depth ≥ 5 and weight ≥ 15. Relations which are quadratic in the e_f could first occur in weight 28 and depth 8."(e_f が絡む未排除の関係式の話であり、(8.8) 合同の話ではない)
  - (8.8) の "mod depth ≥ 5"・p.25 の 𝔞 = {g^m, g^m} + 𝔇⁵g^m(等式の打ち切り深さの指定)。
- したがって **合同 ≡ 0 mod 691 の正典保証は: 深さ 4 まで = (8.8) の言明・深さ 5 = Prop 6.4 経由の propagation("one can show" のみ・導出過程は紙面にない)・深さ 6 以上 = 論文に記述なし**。

---

## 4. Ihara [20] p.258 'key example' を引く箇所の前後関係(精密化)

[20] = Y. Ihara: "Some arithmetic aspects of Galois actions on the pro-p fundamental group of P¹∖{0,1,∞}", Proc. Symp. Pure Math. 70 (2002), 247–273(References p.34)。本文中の [20] 引用は**全 3 箇所**(grep 確認):

1. **p.3(§1.2・画像照合済み)**: "…the outer action of the absolute Galois group Gal(ℚ̄/ℚ) on the pro-ℓ completion of the fundamental group of X which was first studied extensively by Deligne, Drinfeld, Ihara [10, 13, 20]."(歴史的文脈・key example とは無関係)
2. **p.25(Examples 8.5 内・画像照合済み・逐語)** — 位置: 合同式の直後・weight 16/18/20 の d 計算の直前:
   > "…propagates to depth five also. **Compare with the 'key example' of [20], page 258, and the ensuing discussion.** Thereafter, one checks that d(2σ₃∧σ₁₃ − …) ≡ (3617/720)e₁₆ (mod 𝔞) …"
   - 'key example' の**内容自体は Brown の紙面に転記されていない**(参照指示のみ)= [20] p.258 の中身は本 PDF からは UNKNOWN(papers/ に [20] は未収蔵)。
3. **p.25(§8.4 末尾・画像照合済み・逐語)**:
   > "If the elements e_f can be shown to be motivic, then they provide in particular an answer to the question raised by Ihara in ([20], end of §4 page 259). The appearance of the numerators of Bernoulli numbers is related to **conjecture 2 in [20]** and has been studied from the Galois-theoretic side by Sharifi [31] and McCallum and Sharifi [27]."

---

## 出典一覧(頁 = 論文印刷頁・v2)

- Prop 6.4 + 前文 + 証明: p.18(画像照合)
- Prop 4.3・(4.4)・Prop 4.4(§4.4–4.5): p.12(画像照合)
- σ̃ 一般 lift の定義・integral generators f₁₂…f₂₀・ē₁₂ の係数・ζ_𝔇(4,3,3,2) ≡ −116 ζ_𝔇(1,1,8,2): p.24(画像照合)
- σ^{(i)} の続き・Examples 8.5・(8.8)・mod 691 合同・propagation 文・'key example' 引用・e defined over Z・[7] の canonical σ^{(3)}: p.25(前タスクで画像照合)
- σ_{2n+1} 非 canonical 性・脚注 1(Φ^m 係数による canonical 定義)・[10,13,20] 引用: p.3(画像照合)
- {e_f, σ_{2n+1}} ∈ Lie₅ls₁ の未排除・weight 28/depth 8: p.6(テキスト照合)
- Φ の係数規約([4] 由来): §2(テキスト照合)
- References([20][21][28][35][27][31]): pp.33–34(テキスト照合)
