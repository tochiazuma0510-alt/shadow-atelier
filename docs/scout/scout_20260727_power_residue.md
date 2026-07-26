# 論文検索 — 文献要請2(円分体 K=ℚ(ζ₂₀) における n 乗剰余の exact 判定・正当性証明つき)

検索スペック: 数体での n 乗剰余判定アルゴリズム(正当性証明つき)と「v_𝔭(v) ≢ 0 (mod n)」型 obstruction の標準的提示法。K=ℚ(ζ₂₀)・n=10 への適用可能性トリアージ。

**採否判断はしていない**。降ろす判断・機構翻訳は司令塔の専権。

## 候補一覧

| # | 候補 | 識別子 | 年 | 実在確認 | 機構一致度 | 系統 |
|---|------|--------|----|---------|-----------|------|
| 1 | Cohen, *Advanced Topics in Computational Number Theory* (GTM 193) §10.2 + §5.2 | ISBN 978-0-387-98727-9(arXiv なし・書籍) | 2000 | **確認済**(生 PDF 直接読み・目次+本文抜粋を実際に読了) | **高** | 円分体 Kummer 理論本流 |
| 2 | Roblot, "Polynomial Factorization Algorithms over Number Fields" | J. Symbolic Computation 11 (2002) 1–14 | 2002 | **確認済**(生 PDF 直接読み) | 高 | 一般数体・因数分解経由 |
| 3 | Trager, "Algebraic Factoring and Rational Function Integration" | DOI 10.1145/800205.806338(SYMSAC '76) | 1976 | **確認済**(CrossRef API で書誌照合。本文は 403 で未読 — 内容は Roblot 論文中の引用経由で間接確認) | 中 | 一般代数体・古典アルゴリズム |
| 4 | Guàrdia–Montes–Nart, "Higher Newton polygons in the computation of discriminants and prime ideal decomposition in number fields" | arXiv:0807.4065 | 2008 | **確認済**(arXiv 抄録ページ取得) | 中 | 一般数体・イデアル分解/valuation 計算 |
| 5 | Guàrdia–Montes–Nart, "A new computational approach to ideal theory in number fields" | arXiv:1005.1156 | 2010 | **確認済**(arXiv 抄録ページ取得) | 中 | 一般数体・イデアル演算(+Ideals パッケージの理論的基盤) |
| 6 | Cohen, *A Course in Computational Algebraic Number Theory* (GTM 138) | ISBN 3-540-55640-0(書籍・[Coh0] として上記全論文から参照) | 1993(1996 訂正版) | **未読**(候補 1・2 内で頻繁に [Coh0] として参照される定番だが、今回は該当章を直接開いていない) — **UNVERIFIED(詳細レベル)** | 低〜中(背景知識としては必須だが本要請の核心 = Kummer 側の正当性証明は GTM 193 の方が詳しい) | 一般数体・基礎アルゴリズム集 |

## 各候補の詳細

### 1. Cohen, *Advanced Topics in Computational Number Theory*(GTM 193)— 最有力

**要旨**: Cohen の第一の教科書(GTM 138, [Coh0])の続編。相対拡大・類体論の計算アルゴリズムを扱う。第5章「Kummer 理論による定義多項式の計算」と付録A §10.2「Kummer Theory」が本要請の核心。

**該当章・定理番号(実際に本文を読んで確認)**:
- **定理 10.2.9(Hecke の定理)**: K を数体、ℓ を素数、ζ_ℓ∈K、L=K(ℓ√α)(α∈K*\K*^ℓ)とする。素イデアル 𝔭 の L/K における分解型を、**v_𝔭(α) mod ℓ** と合同式 x^ℓ≡α (mod 𝔭^k) の可解性で完全に判定する定理。まさに「v_𝔭(v)≢0 (mod n)」型 obstruction の標準的定式化そのもの。3ケース(ℓ∤v_𝔭(α)/ ℓ|v_𝔭(α)かつ𝔭∤ℓ/ ℓ|v_𝔭(α)かつ𝔭|ℓ)に分けて完全証明(pp.498–504、証明は Newton-Hensel 反復・補題10.2.10–10.2.11を使い切って構成的)。
- **命題10.2.13・アルゴリズム10.2.14「Algorithm for ℓth Powers」(p.504–506)**: x^ℓ≡α (mod 𝔭^k) の可解性を判定する明示アルゴリズム。**正当性証明は命題10.2.13の証明そのもの**(step-by-step の帰納法、Frobenius/完全体 𝒪_K/𝔭 の性質を使用)。「アルゴリズムの妥当性の証明はほぼ自明」と明記(演習17に詳細は譲るが骨子は本文に完備)。
- **アルゴリズム10.2.15**(k≤e(𝔭/ℓ) の場合の HNF ベース高速版、正当性証明つき、p.507)。
- **§5.2「Kummer Theory Using Hecke's Theorem When ζ_ℓ∈K」**: 定理5.2.2(円分体で ζ_ℓ∈K のときの巡回拡大の**十条件**による完全特徴づけ、証明つき)。§5.2.2「Virtual Units and the ℓ-Selmer Group」(定義5.2.4・命題5.2.3/5.2.5/5.2.8)— n 乗剰余判定を類群・単数群のℓ-階数計算に還元する標準的機構(まさに v_𝔭(v) mod n obstruction を Selmer 群の言葉で整理したもの)。

**K=ℚ(ζ₂₀)・n=10 への適用可能性(一次トリアージ)**:
- n=10=2·5 と素因数分解し、ℓ=2 と ℓ=5 それぞれに Hecke の定理を独立適用 → CRT で合成、という自然な二段構成が可能(要請文に既にある「CRT 分解済み」と完全に整合)。
- ζ_5∈K は自明(5|20 なので K⊇ℚ(ζ_5))。ζ_2=-1∈K も自明。**両方の ℓ で「ζ_ℓ∈K」の仮定(定理10.2.9・§5.2 双方の前提条件)が満たされる** — この本の主定理がそのまま適用できる理想的な状況。
- 懸念: 本書は一般の数体 K・一般のイデアル 𝔭 を扱っており、K=ℚ(ζ₂₀) 固有の構造(円分体としての単数・類数の特殊性)は使っていない。円分体特有の高速化(Gauss和・円分単位)は別途要る可能性。

### 2. Roblot, "Polynomial Factorization Algorithms over Number Fields"

**要旨**: 素イデアル法での多項式の法 𝔭 での分解(Berlekamp 法の一般化)+ Hensel 持ち上げ + Mignotte 型評価による数体上への因数分解の2段構成アルゴリズム。T^n−a の既約性判定はこの一般アルゴリズムの特殊ケースとして得られる。

**該当定理・アルゴリズム番号**:
- 定理3.2(Berlekamp、法𝔭での既約成分判定の必要十分条件)、命題3.3(ランダム化・確率1/2以上の分解、証明つき)、アルゴリズム3.4。
- 定理4.1(Hensel持ち上げの一意性・存在、証明つき)、定理4.2/系4.4(Mignotte型 T₂-ノルム評価、完全証明つき、これが「十分な指数 e まで持ち上げれば真の分解が一意に復元される」という**正当性の核**)。
- **アルゴリズム4.6**が数体上の完全分解アルゴリズム(全ステップに証明背景あり)。

**K=ℚ(ζ₂₀)・n=10 への適用可能性**: T^10−v の既約性判定に直接使える一般アルゴリズム。ただし v_𝔭(v) mod n の**構造(素イデアルでの直接の合同式判定)を経由しない**、より重い「法𝔭での分解 → Hensel 持ち上げ → 有理係数復元」という別ルートであり、Cohen の Hecke 定理ルートよりも計算コストは重いと想定される。正当性証明は非常に明快で移送しやすい。

### 3. Trager (1976), "Algebraic Factoring and Rational Function Integration"

**要旨**: 数体上の多項式因数分解の古典的手法(ノルム写像による次数低減+終結式計算)。Roblot論文冒頭でも "Trager 1976" として直接の先行研究に挙げられている。

**懸念**: 本文取得は ACM DOI ページで403(認証拒否)のため**未読** — 内容は Roblot論文の引用・要約経由の間接情報のみ。定理番号・正当性証明の具体的箇所は今回未確認。書誌自体は CrossRef API で実在確認済み(捏造ではない)。深読みする場合は大学図書館経由等でのフルテキスト入手が必要。

### 4. Guàrdia–Montes–Nart, arXiv:0807.4065

**要旨**: 高次 Newton 多角形を用いた判別式計算・素イデアル分解アルゴリズム(Montes アルゴリズムの精密化)。𝔭-adic valuation の計算そのものがこの手法の主要な出力の一つ。

**K=ℚ(ζ₂₀)・n=10 への適用可能性**: v_𝔭(v) の計算部分(obstruction の「左辺」を出す道具)として使える可能性。ただし n 乗剰余判定という「使い道」自体はこの論文の主題ではなく、素イデアル分解・valuation計算という土台部分の提供にとどまる。正当性証明の所在(定理番号)は抄録取得のみでは確認できておらず、深読み時に本文確認が必要。

### 5. Guàrdia–Montes–Nart, arXiv:1005.1156

**要旨**: 上記の続編。イデアルの基本演算(積・商・CRT・valuation)を、極大整数環 𝒪_K の構成を経由せず Montes 表現で直接行う手法。Magma の "+Ideals" パッケージの理論的基盤。

**K=ℚ(ζ₂₀)・n=10 への適用可能性**: 候補4と同様、v_𝔭 計算の効率化という基盤技術。circular に n 乗剰余判定を「library 実装の裏付け」として支える文献であり、**要請が明示的に避けたい「ライブラリマニュアル」寄りに近い**点は留意(ただし本論文自体は理論論文であり、マニュアルではない)。

### 6. Cohen, GTM 138(未深読・UNVERIFIED 扱い)

候補1・2の両方から繰り返し [Coh0] として参照される定番書(3.4節=有限体上の多項式分解、3.5節=有理数体上への持ち上げ、6.2.9=素イデアルの計算、4.8節=𝔭-adic 表現)。本要請の核心である Kummer 理論・n乗剰余判定の**証明つき**記述は GTM 138 ではなく GTM 193(候補1)に格上げ・詳細化されている、というのが候補1の序文(Preface)自身の証言("Chapter 5 ... Kummer theory"は GTM193 の新規内容)。したがって深追いの優先度は候補1より低いと考えられるが、実装時の基礎アルゴリズム(HNF・法𝔭計算等)の参照先として名前だけ記録。

## 空振り・未走査だった角度

- **Belabas の因数分解論文個別**: WebSearch のセッション予算(200/200)を使い切ったため、"Belabas 数体 多項式分解" の直接検索は実行できず。候補2(Roblot)・候補1(Cohen 本人の謝辞に Belabas の名あり、GTM193第8章担当)経由の間接情報のみ。
- **Pohst–Zassenhaus の教科書個別章**の直接確認(角度1後半): 未実施。候補2の定理4.1証明中に "proved in a more general case in (Pohst and Zassenhaus 1989)" という言及はあり、実在は間接確認できるが書誌未取得。
- **証明書化(certified computation)の専用文献**(角度3): Guàrdia–Montes–Nart 2論文(候補4・5)以外に専用の "certificate" 型論文は発見できず。primality proving 分野の「立方体証明書」がヒットしたのみで畑違い(角度3は総じて空振り気味)。
- 使用クエリ例: `Cohen "Course in Computational Algebraic Number Theory" n-th power residue test algorithm chapter` / `Trager algorithm irreducibility x^n - a number field factorization algebraic` / `certified valuation computation prime ideal number field certificate algorithm` / `computing Kummer extensions cyclotomic field power residue symbol algorithm PARI` / `Cohen "Kummer extension" algorithm "n-th power" ideal valuation number field GTM 138`。
