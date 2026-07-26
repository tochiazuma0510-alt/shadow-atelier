# 文献ゲート・スカウト報告 scout_20260727_moduli_descent

**要請**: field of moduli = field of definition(降下)定理の正典的出典 — 「次数10 Belyi 被覆・Aut(dessin)=1・ℚ 上」への適用可能性トリアージ。
**担当**: paper-scout(検索下請け・採否判断せず)
**日付**: 2026-07-27

## 候補一覧

| # | 候補 | arXiv/DOI | 年 | 実在確認 | 機構一致度 | 系統 |
|---|------|-----------|----|---------|-----------|------|
| 1 | Dèbes–Douai, "Algebraic covers: field of moduli versus field of definition" | ASENS 4e sér. 30(3), 303-338 | 1997 | **確認済(一次)** — numdam PDF 直接読了 | 高 | G-cover / mere cover 一般論 |
| 2 | Dèbes–Emsalem, "On fields of moduli of curves" | J. Algebra 211(1), 42-56 | 1999 | 確認済(二次・複数独立引用一致)— Elsevier 直取得はリダイレクトループ・eudml は 403 | 高 | 曲線・marked point |
| 3 | Coombes–Harbater, "Hurwitz families and arithmetic Galois groups" | Duke Math. J. 52(4), 821-839, DOI 10.1215/S0012-7094-85-05243-3 | 1985 | **確認済(一次)** — projecteuclid 書誌ページ直接取得(要旨は課金壁で未取得) | 中 | G-cover の古典的降下 |
| 4 | Sijsling–Voight, "On explicit descent of marked curves and maps" | arXiv:1504.02814 / Res. Number Theory 2 (2016) Art. 27 | 2016 | **確認済(一次)** — arXiv abstract 直接取得 | **高**(角度4 直撃) | marked/pointed 三点被覆 |
| 5 | Herradon Cueto, "The field of moduli and fields of definition of dessins d'enfants" | arXiv:1409.7736 | 2014 | **確認済(一次)** — arXiv abstract 直接取得 | **高** | dessin・Aut 自明の直接言明 |
| 6 | Dèbes–Douai–Moret-Bailly, "Descent varieties for algebraic covers" | Crelle (J. reine angew. Math.) 574, 51-78 / DOI 10.1515/crll.2004.073 | 2004 | 確認済(二次・degruyter 書誌一致)— PDF 取得はバイナリ化け失敗 | 中 | G-cover 降下多様体(1,2 の後継論文) |
| 7 | Weil, "The field of definition of a variety" | Amer. J. Math. 78, 509-524 | 1956 | **UNVERIFIED(直接未取得)** — 検索合成のみ、一次ソース未確認。ただし降下理論の始祖として頻出 | 中(基礎機構だが Aut=1 特化ではない) | 古典的降下(cocycle 判定) |
| 8 | Girondo–González-Diez, *Introduction to Compact Riemann Surfaces and Dessins d'Enfants* | LMS Student Texts 79, CUP, ISBN 9780521740227 | 2011 | 実在確認済(書籍情報のみ・複数書店/Cambridge ページ一致)。**該当章・定理番号は未取得**(目次アクセス失敗) | 未確認(内容照合できず) | 教科書 survey |
| 9 | Sijsling–Voight, "On computing Belyi maps" | arXiv:1311.2529 | 2013 | 確認済(一次・abstract 取得)。ただし「Aut(φ)=1 ⇒ Weil 判定で降下」の言明は検索エンジン合成スニペットのみで、fetch した abstract 本文には出現せず — **記述内容は UNVERIFIED** | 中(存在は確実・該当命題の所在未確認) | Belyi map 計算 survey |

## 各候補の詳細

### #1 Dèbes–Douai (ASENS 1997) — 最有力候補A
一次ソース(numdam.org の PDF)を直接読み、表紙・要旨全文を確認した。要旨: 「a priori K の分離閉包上定義された被覆 f: X→B の field of moduli K は field of definition とは限らない。本論文はこの障害のコホモロジー的測度を与える。G-cover(自己同型込みの Galois 被覆)の場合はよく知られていたが、mere cover には測度がなかった。本論文は測度が単一のクラスでなく H²(K_m, Z(G)) 内の複数の特性類で制御されることを示す(Z(G) = 被覆の中心)。」
- **効き得る機構**: 障害は Z(G) に値を取るコホモロジー類。**Aut(dessin)=1 なら Z(G) を含む自己同型群自体が自明**になるケースがあり、障害類の受け皿が消えて降下が保証される、という機構の可能性(要精読)。
- **照合観点**: (i) G-cover 前提か mere cover 前提か — 「Belyi 被覆」は通常 mere cover(自己同型なし)として扱われることが多く、Coombes-Harbater 型(#3)の結果域と要照合。(ii) properness/marked point の要否は本文未確認(要旨のみ)。
- **懸念**: 要旨レベルの理解であり、Thm 番号・具体的な「Z(G)=1 ⇒ 降下」の命題文は未確認(本文精読は司令塔/reader マター)。

### #2 Dèbes–Emsalem (J. Algebra 1999)
複数の独立引用(Springer, Numdam 系論文の参考文献リスト、academia.edu 等)で書誌が一致: J. Algebra 211(1), 42-56, 1999。一次ページ(sciencedirect/doi.org)は 302 リダイレクトのみで要旨本文を取得できず、**UNVERIFIED 級に近い(書誌は確度高いが要旨未読)**。
- 先行検索合成によれば「the obstruction is essentially the same as the obstruction to K being a field of definition of the cover X → X/Aut(X)」という定式化 — Aut(X) が自明なら X → X/Aut(X) は恒等射で障害が消える、という機構の可能性。
- **懸念**: この定式化の出典は検索エンジンの要約であり、一次テキストで確認していない。要旨さえ未読のため、内容の正確性は司令塔判断時に要再検証。

### #3 Coombes–Harbater (Duke 1985)
projecteuclid の書誌ページを直接取得し、著者・巻号・頁・DOI を確認。要旨は課金壁(30ドル)のため未取得。検索合成によれば「field of moduli = 全 field of definition の共通部分」「mere cover としては常に field of moduli 上定義可能」という定理を含むとされる — **この帰結が正しければ角度①③に強く効くが、要旨・本文未確認のため命題文言は UNVERIFIED**。
- **照合観点**: 「mere cover として常に降下可能」なら、Aut=1 の場合分けは不要になり得る(mere cover は自己同型を問わない)— これが正しければ質問の前提「Aut=1 が必要」自体を緩められる可能性がある。要精読で真偽判定必須。

### #4 Sijsling–Voight, marked curves (arXiv:1504.02814) — 角度4 直撃・最有力候補B
一次ソース(arXiv abstract)取得済み。「Birch の主張 — marked な三点分岐被覆の field of moduli は field of definition である — を再検討する」「古典的な Dèbes–Emsalem 判定は smooth point の存在下で適用される」「野生分岐(wild ramification)へ拡張し、特異曲線での反例も提示」。
- **効き得る機構**: 質問の「次数10 Belyi 被覆」に基点(marked point)を導入できれば、この論文の枠組み(marked + smooth point条件)がそのまま降下の十分条件を与える可能性が高い。**Aut=1 の場合分けを回避し、marking で降下を保証する**という別ルートを提供しうる点で、要請文の「marked/pointed 版」に正確に一致。
- **照合観点**: 曲線が smooth(特異点なし)であることが前提 — Belyi 被覆(射影直線上の分岐被覆)は通常 smooth なので適合しやすい。ワイルド分岐は標数 0(ℚ 上)では非該当、tame の場合の古典結果で十分。
- **懸念**: 「marked」の定義(基点1点か複数か、被覆のどの層に印をつけるか)を本文で要確認。反例(特異曲線)がこちらの設定に混入しないよう要注意。

### #5 Herradon Cueto (arXiv:1409.7736) — 最有力候補C(最も直接的)
一次ソース取得済み。要旨: 「dessins d'enfants を複数の視点(位相被覆・三角形分割付き曲面・三点分岐関数を持つ代数曲線)から導入し、Belyi の定理・絶対ガロア群の作用を確立。**正則 dessin・自明な自己同型群を持つ dessin・面が1つの dessin は field of moduli 上定義可能であることを証明**」。ただし反例として、種数61の正則 dessin 2 個(field of moduli = ℚ(2^{1/3}))で field of moduli がアーベル拡大でない例も提示 — これは「正則」側の反例であり Aut=1 側の主張自体への反例ではない模様(要確認)。
- **効き得る機構**: 要請文そのもの(「Aut=1 の dessin は field of moduli 上定義可能」)をほぼ字面通りに証明していると読める。**最も直接的な出典候補**。
- **照合観点**: 証明が Weil の cocycle 判定(#7)への還元か、Coombes-Harbater 型かを本文で確認要。次数10・ℚ 上という設定への適用に技術的前提(標数0・射影直線上の分岐等)が満たされるか要チェック。
- **懸念**: これは学位論文/レクチャーノート的な性格の可能性があり(著者名から個人サイト論文か査読済み論文か要確認)、正典性(citability)はやや弱いかもしれない — 司令塔判断時に一次定理の再出典(Dèbes-Emsalem 等)を辿るのが安全。

### #6 Dèbes–Douai–Moret-Bailly, Crelle 2004
書誌は degruyter ページのタイトルヒットで確認(二次)。PDF 本体はバイナリ化けで内容取得失敗。#1 の後継的位置づけ(descent varieties = 降下多様体の構成)と推測されるが本文未読。

### #7 Weil (1956)
検索合成のみで一次未確認。cocycle 判定 φ_στ = φ_σ · σ(φ_τ) が降下の標準機構という言明は数学界で広く知られている基礎事実だが、**このセッションでは一次ソースに到達できなかった**。古典的すぎて arXiv にはなく、AMS/JSTOR 等の課金壁の可能性が高い。UNVERIFIED として報告。

### #8 Girondo–González-Diez 教科書
書籍としての実在は複数書店ページで確認(高確度)。しかし該当章(field of moduli の章があるはず、LMS Student Texts 79 の構成上)の目次・定理番号はこのセッションで取得できなかった(Google Books プレビュー等への到達失敗)。**内容の一次確認は持ち越し**。

### #9 Sijsling–Voight, "On computing Belyi maps" (arXiv:1311.2529)
存在確認済みだが、要請に関連する「Aut(φ)=1 ⇒ Weil 判定で降下」という言明の出所は検索エンジンの合成要約であり、fetch した abstract 本文中には現れなかった。本文(セクション)に当該命題がある可能性は高い(survey 論文の性質上)が、**この論文が出典であるとは断定できない** — 一次テキストへの再確認が必要。

## 空振り・未達の角度

- **著者系譜角度(Dolgushev 派・GT 業界: Fresse・Horel・Bar-Natan・Schneps)**: 今回の要請は field of moduli/definition の降下理論であり、GT(Grothendieck-Teichmüller)界隈の著者との直接的な論文接続は検索で得られなかった。Schneps は dessins d'enfants の editor/著者として頻出するが(Schneps 編 "The Grothendieck Theory of Dessins d'Enfants" 等)、field of moduli 降下の一次定理の著者としては今回ヒットせず。**この角度は未達 — 次回は "Schneps dessins field of moduli descent" 等で再試行の余地あり**。
- **逆引き角度(基準論文の被引用)**: #1(Dèbes-Douai 1997)や #3(Coombes-Harbater 1985)の被引用リストを Google Scholar 等で辿る作業は今回未実施(時間配分により省略)。次便で「Dèbes Douai 1997 cited by」等のクエリを追加すれば、より新しい(2010年代以降の)降下定理の候補が出る可能性あり。
- 使用クエリ例(空振り含む): "field of moduli field of definition trivial automorphism Belyi dessin descent theorem"(有効)、"Dèbes Emsalem J. Algebra 1999 abstract"(書誌のみ・要旨は空振り)、"Weil 1956 field of definition descent cocycle criterion"(一次未達)。

## UNKNOWN 規律に基づく総括

- **一次ソースで完全確認**: #1(Dèbes-Douai 1997, ASENS)、#3(Coombes-Harbater 1985, Duke — 書誌のみ)、#4(Sijsling-Voight marked, arXiv)、#5(Herradon Cueto, arXiv)。
- **二次確認どまり(書誌は高確度・内容要旨は未読)**: #2(Dèbes-Emsalem 1999)、#6(Crelle 2004)、#8(教科書)。
- **UNVERIFIED(一次未達)**: #7(Weil 1956)、#9 の当該言明。
