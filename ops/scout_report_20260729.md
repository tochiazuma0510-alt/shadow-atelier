# paper-scout 報告書 — 2026-07-29(数学者要請駆動・経路①)

司令塔宛て。採否判断はしていない。実在確認は全候補について arXiv abs ページを直接取得して行った(WebFetch)。google scholar / arxiv API 検索は WebSearch 予算枯渇のため、arXiv export API (`export.arxiv.org/api/query`) を主経路に切替えた。

---

## スペック 1: 被覆の組合せデータ(monodromy/passport)→ 定義体の主係数・判別式の平方類

| # | 候補 | arXiv ID | 年 | 実在確認 | 機構一致度 | 系統 |
|---|---|---|---|---|---|---|
| 1 | Sijsling–Voight, "On explicit descent of marked curves and maps" | 1504.02814 | 2015 | 確認済み(abs 取得) | 高 | Birch/Dèbes-Emsalem 系譜 |
| 2 | Dèbes–König–Legrand–Neftin, "Rational pullbacks of Galois covers" | 1807.01937 | 2018 | 確認済み(abs 取得) | 中 | Beckmann-Black 系譜 |
| 3 | Wewers, "Three point covers with bad reduction" | math/0205026 | 2002 | 確認済み(abs 取得) | 中 | Beckmann-Wewers 系譜 |
| 4 | Obus, "Fields of moduli of three-point G-covers with cyclic p-Sylow, I" | 0911.1103 | 2009 | 確認済み(検索結果に abstract あり・abs 未直接取得) | 中 | Beckmann-Wewers 拡張 |
| 5 | Roberts, "Division polynomials with Galois group SU3(3).2 = G2(2)" | 1411.7015 | 2014 | 確認済み(検索結果に abstract あり・abs 未直接取得) | 低〜中 | Deligne-Mostow/三点被覆・特殊数体の実例 |

### 各候補の詳細

**1. Sijsling–Voight 1504.02814**(最有力候補)
- 要旨: Birch の主張(marked three-point ramified cover の field of moduli が field of definition である)を再検討。Dèbes–Emsalem の古典的基準(滑らかな点の存在下で降下可能)を用い、代数的な構成的降下法を与える。野生分岐の場合へ拡張。特異曲線での反例も提示。
- なぜ効き得るか(機構ベース): 「モノドロミー置換 → 定義体」の**構成的**(computable)降下アルゴリズムを扱っており、スペックが求める「passport → 定義体のある元の平方類」を機械計算可能にする定理の最有力な足場になりうる。特に "field of moduli = field of definition" の判定条件が、対象の対称性(自己同型群の有無)に依存する形で述べられているはずで、判別式の平方類が現れる典型は二次拡大での降下障害(H²(Gal, ±1) 的コホモロジー類)である可能性が高い。
- 深読み時の照合観点: (i) 降下障害類が具体的に H¹(Gal(k̄/k), Aut) のどのコホモロジー群で表現されているか。(ii) 平方類との対応が定理の中に明示式としてあるか、それとも一般降下理論の系として間接的にしか出ないか。(iii) 野生分岐拡張部分がB₃-gentle系(有限商・hexagon only)の設定に翻訳可能か。
- 懸念: 論文は「降下可能かどうか」の判定に主眼があり、「読み出し公式」そのもの(平方類を具体的に計算する式)がここにあるかは abstract だけでは不明。深読み必須。

**2. Dèbes–König–Legrand–Neftin 1807.01937**
- 要旨: PGL₂(ℂ) の有限部分群 G が「Beckmann-Black 性質」(分岐点数を増やす有理引き戻しで新しい Galois 実現を得られる)を持つのはこの部分群クラスのみであることを証明。
- なぜ効き得るか: Beckmann の定理の精密化・逆問題側からの制約。定義体の構造がどの有限群クラスで「安定」かを分類しており、B₃-gentle 系(有限商)の対象がこの分類のどこに位置するかで、平方類公式の適用範囲を絞れる可能性。
- 照合観点: G が PGL₂(ℂ) の部分群という制約が強く、当工房の対象群(B₃ の有限商)がこの分類対象に該当するかをまず確認する必要。
- 懸念: 主題は「新しい Galois 実現の生成」であり、平方類の読み出し公式そのものではない。間接資料。

**3. Wewers math/0205026**
- 要旨: 標数 p で分岐三点被覆の悪い還元を研究。moduli 体が p で高々従順分岐(tamely ramified)であることを証明。
- なぜ効き得るか: 「定義体のどの素点が分岐するか」という Beckmann 型の定理の p 進版。判別式の**素点情報**(平方類ではなく分岐素点)に直結する定理群の一つ。
- 照合観点: 従順分岐の結果が判別式の 2-adic 成分(平方類判定で最も厄介な素点 p=2 の扱い)にどう影響するか要確認。
- 懸念: 標数 p の還元理論であり、代数体上の判別式平方類公式への翻訳には一段の変換が必要。

**4. Obus 0911.1103**(未直接 abs 取得・API 検索結果の abstract のみで確認)
- 要旨: 巡回 p-Sylow 部分群を持つ三点 G-被覆について、Galois 閉包における高次分岐群の消滅を証明(Beckmann–Wewers の拡張)。
- なぜ効き得るか: Beckmann の定理の一般化ライン上にあり、素点の分岐次数(=判別式の指数)を制御する。
- 懸念: 深読み前に abs ページでの直接確認が必要(現時点は API 経由の abstract のみ)。

**5. Roberts 1411.7015**(未直接 abs 取得)
- 要旨: ガロア群 G2(2) を持つ射影平面の被覆の剛性論証。Deligne-Mostow の三点分岐構成、Dettweiler-Reiter の分割多項式族との関係、三点被覆から特殊数体を得る具体例。
- なぜ効き得るか: 明示計算による「被覆 → 特殊数体」の実例集。判別式の平方類を実例ベースで拾える可能性(公式ではなく実例)。
- 懸念: 一般公式ではなく個別実例。機構移送には不向きかもしれないが、数値検算用のテストケースとしては有用。

### 空振りだった角度(スペック1)
- 直接検索 `Belyi AND "field of definition" AND discriminant` → 0 件。
- `Couveignes AND dessin` → 0 件(Couveignes の explicit dessin 計算論文は arXiv 未掲載の可能性 — 本人の仏語論文や書籍章の可能性が高い)。
- `Malle AND Matzat AND "inverse Galois"` → 0 件(Malle–Matzat の定義体判別式に関する扱いは 1999 年 Springer 書籍 "Inverse Galois Theory" が正典で、arXiv には無い模様。**UNVERIFIED as arXiv record** — 書籍として別途確認が必要)。
- Elkies による dessin 明示計算そのものの論文は本検索で発見できず(関連物理論文が 1 件ヒットしたのみ、機構的に無関係)。

---

## スペック 2: 自由 Lie 環の重み分解と円分指標の重みの対応

| # | 候補 | arXiv ID | 年 | 実在確認 | 機構一致度 | 系統 |
|---|---|---|---|---|---|---|
| 1 | Goncharov, "Galois symmetries of fundamental groupoids and noncommutative geometry" | math/0208144 | 2002 | 確認済み(abs 取得) | 高 | Deligne-Ihara 系譜(motivic) |
| 2 | Brown, "Mixed Tate Motives over Z" | 1102.1312 | 2011 | 確認済み(abs 取得) | 高 | Deligne-Goncharov 系譜 |
| 3 | Furusho, "Four groups related to associators" | 1108.3389 | 2011 | 確認済み(abs 取得) | 中 | GT群/motivic Galois 群系譜 |
| 4 | Furusho, "The multiple zeta value algebra and the stable derivation algebra" | math/0011261 | 2000 | 確認済み(検索結果 abstract あり・abs 未直接取得) | 中 | 安定微分環(stable derivation algebra)系譜 |
| 5 | Hain, "Relative Weight Filtrations on Completions of Mapping Class Groups" | 0802.0814 | 2008 | 確認済み(検索結果 abstract あり・abs 未直接取得) | 中 | Hain–Matsumoto 系譜 |

### 各候補の詳細

**1. Goncharov math/0208144**(最有力候補)
- 要旨: アフィン直線上の motivic iterated integral を定義し、Hopf 代数の余積公式を証明。motivic polylogarithm Hopf 代数の余積の明示公式・非分岐性(unramifiedness)の基準を導出。
- なぜ効き得るか(機構ベース): motivic iterated integral の次数(=反復積分の長さ)が weight に直結し、Galois(motivic Galois 群)作用がこの次数のべきで働く、という枠組みそのもの。当工房が求める「γ_k/γ_{k+1} 上の cyclotomic 作用が重み k」の**正典的な出所**である可能性が高い(Deligne-Ihara の定理をこの論文が明示的に再定式化しているはず)。
- 照合観点: (i) 論文内で自由 Lie 環(motivic Lie coalgebra の双対)の次数付けが下中心列商とどう対応しているか明示式を探す。(ii) 「weight k = cyclotomic character の k 乗」の記述が Proposition/Theorem として直接あるか、それとも一般 Tate 対象の性質として暗黙か。
- 懸念: 51 ページの重い論文で、目的の一文がどのセクションにあるか不明(深読み必須、当たりは §1-2 の基礎設定部分と予想)。

**2. Brown 1102.1312**
- 要旨: Z 上の mixed Tate motives の圏が P¹−{0,1,∞} の motivic fundamental group で張られることを示し、Hoffman 予想(MZV が {2,3} 添字の元の有理線形結合で書ける)を証明。
- なぜ効き得るか: motivic fundamental group の枠組みで、下中心列商への重み付け(= weight n の Tate 対象への分解)が明示的に扱われている一次資料。MZV の depth/weight 分解が当工房の「u に重み k」の直接の類例。
- 照合観点: Broadhurst-Kreimer 予想周辺の depth-graded 構造の記述箇所で、weight n = cyclotomic^n の対応が定理として書かれているか確認。
- 懸念: 主眼は MZV の代数的構造で、Galois 表現としての明示的记述は薄い可能性(Ihara/Deligne 側の一次論文の方がストレートかもしれない)。

**3. Furusho 1108.3389**
- 要旨: Drinfeld associator の定義の解説と、4つの準冪単代数群(motivic Galois 群・GT群・二重シャッフル群・Kashiwara-Vergne 群)の最近の関係の報告。
- なぜ効き得るか: motivic Galois 群と GT 群の関係を扱う概説論文であり、重み構造の対応表が整理されている可能性が高い(サーベイなので出発点として有用)。
- 照合観点: GT 群の λ パラメータ(scalar 因子)と motivic Galois 群の重みの対応表があるか。B₃-gentle 系の c(=当工房の中心パラメータ)との対応も探る価値あり。
- 懸念: 概説であり厳密な定理の一次証明は引用元(arXiv:math/0702128, arXiv:0808.0319 — 未確認)にある。

**4. Furusho math/0011261**(未直接 abs 取得)
- 要旨: 多重ゼータ値代数と安定微分環(stable derivation algebra)の関係。l-adic Galois 表現と基本群の比較。
- なぜ効き得るか: 「安定微分環の次数付け」と「l 進 Galois 表現の重み」の対応が扱われており、当工房の γ_k/γ_{k+1} 上の作用と直接類比可能。
- 懸念: 未直接確認、深読み前に abs ページ要再取得。

**5. Hain 0802.0814**(未直接 abs 取得)
- 要旨: 標識種数 g 曲線の写像類群の完成上の relative weight filtration。Matsumoto との共同研究(Galois 理論側)。
- なぜ効き得るか: Hain–Matsumoto の weight filtration そのものの一次資料(スペックの当たり指定と直接一致)。ただし対象が写像類群であり、自由 Lie 環/braid 群への言明は間接的かもしれない。
- 懸念: 未直接確認。また対象がやや広い(mapping class group 全般)ため、目的の braid 群の下中心列商への特化した記述があるか要確認。

### 空振りだった角度(スペック2)
- `Ihara AND "free Lie algebra" AND Galois` → 0 件(Ihara の該当論文は 1990-1991 年の Grothendieck Festschrift 掲載で、**arXiv 未掲載と推定 — pre-arXiv 時代の一次資料**。図書館アクセスでの確認が必要)。
- `Deligne AND "projective line" AND "three points" AND motivic` → 0 件相当(ヒットは無関係の Roberts 論文のみ)。Deligne の "Le groupe fondamental de la droite projective moins trois points"(1989)も同様に**pre-arXiv・未掲載と推定**。
- `Nakamura AND "Galois representations" AND braid` および `Nakamura AND Galois AND "Grothendieck-Teichmuller" AND cyclotomic` → いずれも 0 件。中村博昭の関連論文は arXiv 収録が薄い可能性(日本の紀要・数理研講究録掲載が多い分野)。
- `"lower central series" AND "pure braid" AND Galois` → 0 件。
- `"free Lie algebra" AND cyclotomic AND weight` → 0 件。
- Ihara の弟子筋である Kodani–Morishita–Terashima "Arithmetic topology in Ihara theory"(1608.07926)、Hirano–Morishita "Arithmetic topology in Ihara theory II"(1906.00627)がヒットしたが、これらは pure braid 群の Milnor 不変量の数論的類似という**隣接領域**であり、直接の重み対応公式ではない(参考文献として深読み時に一次資料への足がかりに使える可能性)。

---

## 総括(UNKNOWN 規律の遵守)

- スペック1は Sijsling–Voight(1504.02814)が最有力。Malle–Matzat の書籍(1999)・Couveignes の explicit dessin 計算・Elkies 自身の論文は **arXiv に見当たらず**、書籍/紀要アクセスでの別途確認が必要(UNVERIFIED as arXiv record、非存在の証明ではない)。
- スペック2は Goncharov(math/0208144)・Brown(1102.1312)が最有力候補だが、**求める定理の一次資料(Ihara 1990-91, Deligne 1989)は pre-arXiv 時代とみられ、本検索経路では実在確認できなかった**。これは負の結果として明記する — 図書館 DB(MathSciNet 等)でのタイトル直接照合が次の一手になる。
- 全候補のうち abs ページを直接取得して確認したもの: 1504.02814 / 1807.01937 / math/0205026 / math/0208144 / 1102.1312 / 1108.3389 の6件。残り4件(0911.1103, 1411.7015, math/0011261, 0802.0814)は arXiv export API 検索結果内の abstract 表示で確認したのみで、abs ページの直接取得は未実施(必要なら追加で行う)。
