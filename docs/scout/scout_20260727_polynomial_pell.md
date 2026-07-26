# 論文検索: 多項式 Pell 方程式(deg f=6・genus 2・torsion 位数 5) — 2026-07-27

司令塔発・S5 設計 v1.2 §7 論点 5 の要請。困難: **a² − f₆·p² = ĉ**(deg f₆=6・genus 2 超楕円曲線 y²=f₆(x))の解と、Jacobian の因子類 [P₀−P_∞] の位数(特に **5**)の対応の正典的出典を探す。

**採否・数学的評価は行わない。機構ベースの照合観点提示まで。司令塔への引き渡し専用(数学者への直接配達は禁止)。**

## 候補一覧

| # | 候補 | 出典 | 年 | 実在確認 | 機構一致度 | 備考 |
|---|------|------|----|----|----|----|
| 1 | Kollár, "Pell surfaces" | arXiv:1906.08818 [math.AG] | 2019 | **確認済**(arXiv abs 取得) | 高 | Abel 1826 の帰着を明示的に述べる一次サーベイ級 |
| 2 | Daowsud–Schmidt, "Continued fractions for rational torsion" | arXiv:1708.05511(J. Number Theory 189 (2018) 115–130) | 2017/2018 | **確認済**(arXiv abs 取得・journal ref 記載) | 高(機構)/中(位数不一致) | genus 2・関数体連分数で torsion 位数 **11** の族を構成。手法は移送可能、対象位数は 5 でない |
| 3 | Leprévost, "Torsion sur des familles de courbes de genre g" | Manuscripta Math.(DOI: 10.1007/bf02567087) | 1992 | **確認済(書誌のみ)**— Crossref で著者・誌名・DOI 確認。要旨本文は未取得(paywall) | 高(推定) | genus g 一般の torsion 族構成の基礎論文。genus 2・位数 5 が含まれるか本文未確認 — **要追加確認** |
| 4 | Leprévost, "Jacobiennes de certaines courbes de genre 2: torsion et simplicité" | J. Théorie des Nombres de Bordeaux 7(1) (1995), 283–306(DOI: 10.5802/jtnb.144) | 1995 | **確認済(書誌のみ)**— journal ページで題名・巻号・頁確認。本文/要旨未取得(bot 制限) | 高(推定) | genus 2 特化・torsion + simplicité。参考文献に「order 15,17,19,21」の姉妹論文の存在を確認 — 本論文が **位数 5,7,9,11,13** 系列の該当編である可能性が高いが**未確認(UNVERIFIED)** |
| 5 | Leprévost, "Famille de courbes hyperelliptiques de genre g munies d'une classe de diviseurs rationnels d'ordre 2g²+4g+1" | Sém. Théorie des Nombres Paris 1991–92, Progress in Math.(DOI: 10.1007/978-1-4757-4273-2_7) | 1993 | **確認済(書誌のみ)** | 中 | genus g 一般公式・g=2 で位数 17(=2·4+4·2+1)。**位数 5 には該当しない**(公式不一致) |
| 6 | Adams–Razar, "Multiples of Points on Elliptic Curves and Continued Fractions" | Proc. London Math. Soc. (DOI: 10.1112/plms/s3-41.3.481) | 1980 | **確認済(書誌のみ)** | 中(機構の原型・genus 1) | 連分数 ⟺ torsion の対応を elliptic curve(genus 1)で確立した古典。Abel–Pell の現代的定式化の先駆けとしてスペック角度①の起点 |
| 7 | Dubickas–Steuding, "The polynomial Pell equation" | Elemente der Mathematik 59 (2004)(DOI: 10.1007/s00017-004-0214-7) | 2004 | **確認済(書誌のみ)** | 中〜高(推定) | 多項式 Pell 方程式の解説論文。Abel の定理の現代的整理を含む可能性が高いが本文未確認 |
| 8 | Avanzi–Zannier, "Genus one curves defined by separated variable polynomials and a polynomial Pell equation" | Acta Arithmetica(DOI: 10.4064/aa99-3-2) | 2001 | **確認済(書誌のみ)** | 低〜中 | genus 1 の類似構造。手法の隣接参考(deg f₆=6・genus 2 には直接該当しない) |
| 9 | Suluyer–Sadek, "Quadratic torsion orders on Jacobian varieties" | arXiv:2410.14455 | 2024 | **確認済**(arXiv abs 取得) | 低〜中(方法論) | genus g 一般公式 N=4g²+2g-2, 4g²+2g-4, 2g²+7g+1 の torsion 族構成。g=2 代入では 16,18,23 — **位数 5 に非該当**。構成技法(1パラメータ族)は参考になりうる |
| 10 | Suluyer–Sadek, "Rational torsion on hyperelliptic jacobian varieties" | arXiv:2410.14454 | 2024 | **確認済**(arXiv abs 取得) | 低 | Flynn 予想(torsion 位数 N∈[3g,4g+1])の証明・g=2 では [6,9] — **位数 5 は範囲外**(Flynn 予想の境界外の例外ケースという整理軸としては有用) |

## 各候補の詳細

### 候補 1: Kollár, "Pell surfaces" (arXiv:1906.06870 ではなく **1906.08818**)
- 要旨: x²−g(u)y²=1 型の多項式 Pell 方程式を研究。Pell 曲面上のアフィン直線(=多項式解)の記述を試み、**偶数次数 g では完全な結果**、奇数次数は未解決と明記。
- なぜ効き得るか: Abel 1826 の枠組み(解の存在 ⟺ Jacobian(y²=g(u)) 上のある torsion 点)を現代語で要約しており、**a²−f₆p²=ĉ の deg f₆=6(偶数次数)ケースの一般論の入口**として直接使える。deg 6 は偶数なので「結果が rather complete」な側に該当する可能性が高い。
- 照合観点: (i) この論文の「偶数次数で完全」の主張が deg 6・genus 2 の場合に具体的に何を保証するか(存在条件のみか、明示多項式まで与えるか)を本文で確認。(ii) torsion 点の位数と解の次数(deg a, deg p)の対応公式の有無。
- 懸念: 曲面上の「アフィン直線」問題として抽象化されており、**位数 5 という具体的数値には言及がない**可能性(要旨レベルでは不明)。深読み必須。

### 候補 2: Daowsud–Schmidt, "Continued fractions for rational torsion"
- 要旨: 関数体上の連分数を使い、指定の torsion 位数を持つ genus 2 曲線の新しい族を構成する手法を提示。具体例として **genus 2・torsion 位数 11** の無限族を実演。
- なぜ効き得るか: **手法(連分数構成法)がそのまま位数 5 のケースに転用できる可能性が高い**— 本質的に「連分数展開の周期が torsion 位数を決める」という機構は位数に依存しない一般法のはず。位数 11 用に調整されたパラメータを 5 用に置き換える再導出が期待できる。
- 照合観点: 本文の構成アルゴリズムが位数に依存しないパラメトリックな手順か、位数 11 に特化した aد hoc 構成かを確認。deg f₆=6 の設定と一致するか(genus 2 なので deg f は 5 or 6 のはず)。
- 懸念: 位数がスペックの要求(5)と異なる ⟹ **直接引用不可・手法の移送のみ**。

### 候補 3・4・5: Leprévost 三部作(1992, 1993, 1995)
- Leprévost は 1990 年代に genus g(特に genus 2)の超楕円曲線で Jacobian が特定位数の有理因子類を持つ族を系列的に構成した(位数 5,7,9,11,13,15,17,19,21 …の各論文が存在する形跡)。
- なぜ効き得るか: **この系列のどれかが「genus 2・位数 5」を厳密に扱っている可能性が最も高い一次資料群**。フランス語の古典論文で arXiv 未収録・paywall のため、書誌(著者・誌名・DOI)は Crossref で確認できたが**本文・要旨は今回未取得**。
- 照合観点: 1995 年の JTNB 論文(候補4)の参考文献リストに「位数 15,17,19,21」の姉妹論文が確認できたことから、**「位数 5,7,9,11,13」を扱う対の論文が別に存在する可能性が高い**(表題末尾の位数リストのみが違う姉妹論文シリーズと推定)。次回検索での優先探索対象。
- 懸念: **UNVERIFIED**(本文未確認)。位数 5 が実際にこのシリーズのどの論文に含まれるか、今回の検索では確定できなかった。**捏造回避のため、位数 5 を含むと断定はしていない** — あくまで書誌が実在する 3 論文の提示。

### 候補 6: Adams–Razar (1980)
- 連分数 ⟺ 楕円曲線 torsion の対応を確立した古典(genus 1)。Abel–Pell 理論の現代的定式化の起点としてスペック角度①が名指しした系譜に一致。
- 照合観点: genus 2 への一般化の際の類似定理の形(torsion 位数と連分数周期の関係式)の直接移植可能性。

### 候補 7・8: Dubickas–Steuding (2004)・Avanzi–Zannier (2001)
- 多項式 Pell 方程式の一般論(角度①)。Avanzi–Zannier は genus 1 の類似構造。両者とも書誌確認のみで本文未確認。

### 候補 9・10: Suluyer–Sadek 二部作 (2024, arXiv)
- 最新(2024)の genus g 一般 torsion 族構成・Flynn 予想証明。g=2 に代入すると位数 5 は当該公式・当該範囲に該当しないことを確認済み。**直接の解ではないが、「なぜ位数 5 が genus 2 で特異/困難なケースなのか」を照らす背景資料**として有用(Flynn 予想の境界 [3g,4g+1]=[6,9] の外側にあることの意味づけに使える)。

## 空振りだった角度とクエリ

- `abs:"polynomial Pell equation" AND abs:"genus 2"` → 0 件
- `abs:"5-torsion" AND abs:"genus 2" AND abs:"Jacobian"` → 0 件
- `abs:"torsion" AND abs:"genus 2" AND abs:"order 5"` → 0 件
- `abs:"Pell" AND abs:"torsion" AND abs:"genus two"` → 0 件
- zbMATH 検索(`zbmath.org/?q=...`) → **403 Forbidden**(bot 制限・未確認のまま断念)
- Semantic Scholar API → **429 Too Many Requests**(レート制限・未確認のまま断念)
- van der Poorten の "Pell's equation for polynomials" 系論文(スペック角度①で名指し)→ **今回未発見**。arXiv/Crossref の検索クエリでは該当なし。氏の個人サイト・豪州系レポジトリでの追加検索が必要(次便の宿題)。
- WebSearch(汎用検索)ツール自体が**セッション予算切れ(200/200 使用済み)**で今回使用不可 — 全検索は arXiv API(export.arxiv.org)・Crossref API・個別 abs ページ直接取得に限定された。この制約により、**Google Scholar 経由の被引用探索(角度④の一部)は未実施**。次便では別セッションでの WebSearch 併用を推奨。

## 総括

候補 10 件。実在確認: arXiv 由来 4 件(#1,2,9,10)は abs ページ直接取得で確認、書誌由来 6 件(#3,4,5,6,7,8)は Crossref で著者・誌名・DOI を確認したが本文未取得(未確認要旨部分は本報告に含めていない)。

**最有力候補**:
1. **候補 1(Kollár, arXiv:1906.08818)** — deg f₆=6 が偶数次数のケースに該当し「結果が比較的完全」と明記。Abel 1826 の枠組みへの現代的入口として深読み優先度最高。
2. **候補 4(Leprévost 1995, JTNB, DOI:10.5802/jtnb.144)** — genus 2 特化・torsion 構成の一次資料。位数 5 を含むかは未確認だが、姉妹論文シリーズ(位数 15,17,19,21 論文の存在を確認済み)から推定して、位数 5,7,9,11,13 系列の対応編を持つ可能性が最も高い一次資料。**次便で本文入手(有料 or 図書館経由)を優先課題として提案**。
