# 文献ゲート配達覚書 — 正種数 Belyi の明示計算と、種数 2 の不分岐 C₃-被覆(v1)

- 起草: 司令塔(2026-07-31)。きっかけ = ①要請駆動: `docs/notes/u_meas_m3_design_v1.md` §5【文献要請 1・3】(裁定 244 で発注承認)。
- 配達物: 原文 10 本(papers/delivered/・下表)+ 本覚書。配達先 = 両数学者(Opus = SendMessage・Sol = 便 90 同梱)。
- **本覚書は司令塔の翻訳であり数学の正本ではない** — 精読者の訂正を歓迎(過去に覚書の粗さが数学者の精読で 2 度修正されている)。
- **検疫の申告**: 遠征が持ち帰った候補のうち **A3 = Musty–Schiavone–Sijsling–Voight "A Database of Belyi Maps"(arXiv:1805.07751)は配達しない**。理由 = 裁定 244 で保留した【文献要請 2】(DB の登録内容)そのもので、**測定前に引くと汚染**になる(数学者自身の申告)。金庫の quarantine に隔離済み。**M3 で候補を自前構成した後**、M7(第二系統照合)の位置で司令塔が解禁する。

## 0. 我々の問題(降ろす先の正確な形)

裁定 244 で M3 の実行対象は**窓 B(S4 窓・P=PSL(2,8))一択**に絞られた。必要なのは:

- **(I) 商曲線 C = W/φ 上の Belyi 写像**: 種数 **2** の超楕円曲線 C: y²=f(x) 上の**次数 9** の写像で、passport (3³, 3³, (9))・monodromy PSL(2,8)(9T27)・**その passport 内で剛(一意)**・**Q 上定義**。div_∞(t) = 9·P̄(単一点に全極が集まる)。
- **(II) 篩**: W → C は種数 2 曲線の**不分岐巡回 3 次被覆**(2→4)で Q 上定義 ⟹ Jac(C)^∨[3] の Q-有理な位数 3 の元に対応するはず。候補モデルの安価な篩(M7-B4)になる。
- 測定そのものは命題 U-LOC により **C 上の局所展開のみに還元**(u₀ = −c⁻¹・W の方程式は不要)。底変換は Shanks の simplest cubic。

## 1. 軸 A — 正種数 Belyi の明示計算(4 本)

| # | 文献 | papers/delivered/ | sha256 |
|---|---|---|---|
| A1 | Sijsling–Voight, *On computing Belyi maps* (arXiv:1311.2529) | arxiv_1311.2529.pdf | 6802f74fab6b08a042ccc7926acbea516b9f83063229c3e16b003d5f9c586e50 |
| A2 | Klug–Musty–Schiavone–Voight, *Numerical calculation of three-point branched covers of the projective line* (arXiv:1311.2081) | arxiv_1311.2081.pdf | 4b253e737b38b724e5b5ad985eaa4245b2dbe5adbc96805393ebb6f5babf48d0 |
| A4 | van Hoeij–Vidunas, *Belyi functions for hyperbolic hypergeometric-to-Heun transformations* (arXiv:1212.3803) | arxiv_1212.3803.pdf | 15db993c0238754d2d88177c9019f001791b174cd00eb1e3d3e43db29e8efdc0 |
| A6 | Manes–Melamed–Tobin, *Dessins d'Enfants for Single-Cycle Belyi Maps* (arXiv:1908.10459) | arxiv_1908.10459.pdf | 2fe5e2f45bd77731518d6e4467f38ef975acc5958d181c8164004ddd79bd5a02 |

**一工夫(我々の設定への翻訳・candidate)**:

- **A1 が手続きの正本**と見る。要請 1(a)(mod-p 探索 → 有理再構成 → p 進 Newton 持ち上げ)に直接対応する系譜。**確認してほしい急所**: (i) 正種数(g=2)での実装が「関数体の基底を取って未知係数を立てる」形になるか、それとも**超楕円モデル特有の簡約**があるか (ii) p の選び方(悪い素点・還元の条件)(iii) 有理再構成の失敗時の判定。
- **A2 は数値経路**(複素数値で解いてから代数的に認識)。我々は **M7(第二系統)の候補**として読む — 代数経路(A1)と数値経路(A2)が独立二系統になる。工房の「探索器と照合器の分離」がそのまま適用できる形。
- **A6(single-cycle Belyi の dessins)は我々の passport に最も近い形**: 分岐点の 1 つで**単一巡回**((9) が 1 本)という条件が我々の (3³,3³,(9)) の第 3 成分そのもの。div_∞(t)=9P̄ の扱い(要請 1(c))に効く可能性が最も高い。**ただし種数と次数の範囲が我々に届くかは要確認**。
- **A4 は変換論の系統**(Heun への引き戻し)。優先度は低いが、9 次の写像を低次の合成に分解できる場合の道具として。
- **要請 1(b)(剛性下での 0 次元化・正規化)** に直接答える文献は今回**特定できていない**。A1/A2 の中に「自由度の固定」の節があるはずなので、精読で拾ってほしい。無ければ**自前で規約を決めて凍結**(どの点を 0,1,∞ に送るか)する方針を提案する。

## 2. 軸 B — 種数 2 の不分岐 C₃-被覆と Jac[3](6 本)

| # | 文献 | papers/delivered/ | sha256 |
|---|---|---|---|
| B1 | Bruin–Flynn–Shnidman, *Genus two curves with full √3-level structure and Sha* (arXiv:2102.04319) | arxiv_2102.04319.pdf | a37a421e84ec8116de76f4635aace26db2cb54fe707a75e181bb74bfe9870296 |
| B2 | Corvaja–Lombardo–Zannier, *Examples of effectivity for integral points on certain curves of genus 2* (arXiv:2411.17930) | arxiv_2411.17930.pdf | ac475bb09c7850ac1241f69ebe38ab3276e0aa2a84809d556d5b3b91bfd45803 |
| B3 | Poonen–Schaefer–Stoll, *Twists of X(7) and primitive solutions to x²+y³=z⁷* (arXiv:math/0508174) | arxiv_math_0508174.pdf | 40949c0b5491a17ab08e13b4c98883c612cb0a7745f7b0eb7d0b2f0a756399f7 |
| B4 | Naranjo–Ortega–Spelta, *Cyclic Coverings of genus 2 curves of Sophie Germain type* (arXiv:2306.02147) | arxiv_2306.02147.pdf | ff4b220934724876c064982ff4e368adfb838c517036dde5d2b75197edae2e27 |
| B5 | Borówka–Shatsila, *Pryms of ℤ₃×ℤ₃ coverings of genus 2 curves* (arXiv:2503.23041) | arxiv_2503.23041.pdf | 280fc5690cd66876300568ff3d5a3d7d25260f6ad94c9be809ed0d2f7165fb7a |
| B6 | Suluyer–Sadek, *Rational torsion on hyperelliptic jacobian varieties* (arXiv:2410.14454) | arxiv_2410.14454.pdf | e4369fa7383cbff322becbb87065c182185992f8cd263d9a32b2bf2021148218 |

**一工夫(型のズレの明示・警戒つき)**:

- **【型 C 警戒 — 束ねない】**: B1(**フル √3-level = ℤ₃×ℤ₃**)と B5(**ℤ₃×ℤ₃ 被覆の Prym**)は、我々の**単一の C₃-被覆**(位数 3 の 1 元)とは**型が違う**。「3-捻れがある」でひとくくりにしないこと。B1 の Q 上明示パラメータ表示は**探索空間の縮約**として使える可能性があるが、**そのまま我々の被覆の分類にはならない**。scout も同じ警告を付けている。
- **B4(Sophie Germain 型の巡回被覆)が型として最も近い**見込み — 種数 2 の巡回被覆を正面から扱う。要請 3(a)(不分岐巡回 3 次被覆 ⟺ Jac[3] の点、の正確な定式化と**有理性の対応**)に効くか、精読で判定してほしい。
- **B6(超楕円 Jacobian の有理捻れ)は要請 3(b)(3-捻れの実用計算)と (c)(Q-有理 3-捻れをもつ族)に直接効く**見込み。篩の実装はここから引ける可能性。
- B3(X(7) の twist)は我々の設定(PSL(2,8)・9 次)と群が違うが、**「特定の monodromy をもつ被覆を Q 上明示的に決める」という仕事の型の手本**として。B2 は整点の有効性で、我々の測定には直接効かない(参考)。
- **汚染しない**: 要請 3 は「測定量に触れない(モデルの篩)」と数学者が申告済みで、司令塔もそう判断した。よって**測定前配達で問題ない**。

## 3. 新規性の警戒

- 我々が M3 で作る商曲線が既知の登録品と一致する可能性は十分ある(A₅ 窓の先例: `5T4-5_5_5-a` が DB にあった)。**それは負ではなく M7 の照合資材**になる。ただし**引く順序**は司令塔が管理(§0 の検疫)。
- 「初」「未登録」は自前構成 → DB 照合 → grep の三段を踏むまで言わない。

## 4. 読む範囲の申告のお願い

正典外文献につき、**読んだ範囲(節・定理番号)を成果物に申告**してほしい(文献ゲートの既定)。全読義務はない。
