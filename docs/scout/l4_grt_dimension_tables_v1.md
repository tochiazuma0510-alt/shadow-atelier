# 文献検索報告 — L-4+L-6統合: grt₁次元表 & Ihara–Takao関係明示形

**検索スペック元**: 裁定640/646(文献要請L-4「stable derivation algebra/grt₁の重み別次元表」+L-6「Ihara–Takao関係の明示係数・Brown freeness定理・depth-graded次元表」)
**検索日**: 2026-08-06(セッション日付ラベル)
**検索係**: paper-scout
**採否判断**: なし(本報告書は候補提示のみ。降ろし判断・機構翻訳は司令塔の専権)

---

## 候補表

| # | 候補 | arXiv/DOI/所在 | 年 | 実在確認 | 機構一致度 | 系 |
|---|------|----------------|----|---------|-----------|-----|
| 1 | L. Schneps, "Grothendieck-Teichmüller Lie theory and multiple zeta values" (MIT講義ノート Lecture 2A) | webusers.imj-prg.fr/~leila.schneps/MIT2A.pdf(講義ノート・非arXiv) | 2012 | **確認済**(全11頁を直接取得・精読) | **高** | GT一般(grt理論・B₄系隣接だが対象は次数構造そのもので系依存性は薄い) |
| 2 | H. Ihara, H. Takao, 関係式定理(Theorem 4, 上記講義ノートp.7に引用) | 原論文は未直接確認(下記#7参照)。**係数は#1経由で確認済** | (原論文は1990年代) | **原論文はUNVERIFIED**・係数自体は#1で実在確認 | **高** | GT一般 |
| 3 | L. Schneps, 期間多項式定理(Theorem 5, S,2006) | 同上#1内(p.8) | 2006 | **確認済**(#1に included) | **高** | GT一般 |
| 4 | F. Brown, "Mixed Tate motives over Z" | arXiv **1102.1312**(Annals of Math 175(2), 2012, 949-976) | 2012 | **確認済**(arXiv abstractページ取得) | **高**(freeness定理の主結果は同定・§本文の正確な言明は未読解=深読み要) | GT一般/motivic |
| 5 | F. Brown, "Depth-graded motivic multiple zeta values" | arXiv **1301.3053**(Compositio Math) | 2013 | **確認済**(arXiv abstractページ取得) | **高**(Broadhurst-Kreimer予想を明示的に扱う) | GT一般/motivic |
| 6 | F. Brown, "Anatomy of an associator" | arXiv **1709.02765** | 2017 | **確認済**(arXiv abstractページ取得) | 中(重み≤13の関係式表を圧縮する手法論文・次元表そのものではない可能性) | GT一般/motivic |
| 7 | H. Tsunogai, "On ranks of the stable derivation algebra and Deligne's problem" | Proc. Japan Acad. 73(2)(1997), 29-31(projecteuclid.org/euclid.pja/1195510120) | 1997 | **確認済**(メタデータのみ・本文は購読制のため未読)| 高(想定=次元/rank表そのもの) | GT一般 |
| 8 | H. Furusho, "Multiple zeta values and Grothendieck-Teichmüller groups" | kurims.kyoto-u.ac.jp preprint RIMS1357.pdf | 2002 | **確認済**(全体構成・冒頭8頁精読) | 低〜中(GRT/GTの定義的サーベイが中心・**読んだ範囲(§0-2.1導入部)には次元表なし**。§5.2「stable derivation algebraの標準自由基底の候補への余談」に何か載る可能性あるが未読) | GT一般 |
| 9 | J. Li, "The depth structure of motivic multiple zeta values" | arXiv **1710.06135** | 2017-2018 | **確認済**(arXiv abstract) | 中(depth構造の完全列・次元表明示は abstract からは不明) | GT一般/motivic |
| 10 | J. Li, "Depth-graded motivic Lie algebra" | arXiv **1801.02145** | 2018 | **確認済**(arXiv abstract) | 中(Tasaka予想⇒Brown行列予想の含意・次元表は abstract からは不明) | GT一般/motivic |
| 11 | B. Enriquez, P. Lochak, "Homology of depth-graded motivic Lie algebras and koszulity" | arXiv **1407.4060** | 2014 | **確認済**(arXiv abstract) | 高(Broadhurst-Kreimer予想のHilbert級数を明示的に扱う・**depth-graded次元表の理論的裏付けとして有望**) | GT一般/motivic |
| 12 | N. Arbesfeld, B. Enriquez, "On a lower central series filtration of grt₁" | arXiv **1406.0675** | 2014 | **確認済**(arXiv abstract) | 中(depth-graded構造・下中心列によるgrt₁の分解) | GT一般 |
| 13 | B. C. Ward, "Lie graph homology model for grt₁" | arXiv **2206.03433** | 2022-2023 | **確認済**(arXiv abstract) | 低(depth 2 mod depth 3の関係式の構造論・次元表なしと abstract で明言) | GT一般 |

---

## 各候補の詳細

### #1 Schneps講義ノート(MIT2A.pdf)— 最有力候補
3-4行要約: GT/grt理論の講義ノート。grt の定義(relations I/II/III)・Furushoの単一関係定理・**Theorem 4(Ihara-Takao)**「偶数 n≥12 に対し depth<4 の項を持たない線形結合 Σaᵢ{f₂ᵢ₊₁,f_{n-2i-1}} の空間の次元 = dim S_k(SL₂(Z))(重み k のカスプ形式空間の次元)= [(n-4)/4]-[(n-2)/6]」の明示式。**重み12の Ihara の等式を原文のまま確認**:
> 2{f₃,f₉} - 27{f₅,f₇} ≡ 0 mod 691
正規化後(Theorem 5, Schneps 2006):
> {f₃,f₉} - 3{f₅,f₇} は depth<4 の項を持たない
重み16の類例も明示:
> 2{f₃,f₁₃} - 7{f₅,f₁₁} + 11{f₇,f₉} ≡ 0 mod 3617
また **dim grt₁₁=2, dim grt₁₃=3**、weight 3,5,7,9 は1次元・weight 4,6は0、との明言あり。

なぜスペックの困難に効き得るか: L-4(次元表)とL-6(明示係数)の**両方を一枚で満たす**一次資料級の内容。特に「重み12で自由Lieからの次元差」を dim S_k(SL₂(Z)) という**具体式**で与えており、B₃-gentle系のhexagon-only構造で次数勘定を行う際の比較対象として直接使える可能性が高い。

深読み時の照合観点: (a) この Theorem 4/5 の証明(Ihara-Takaoの原論文、Schneps 2006原論文)への遡及が必要 — 講義ノートは要約のみで完全証明はなし。(b) 「depth<4の項を持たない」という条件が本工房の hexagon-only(pentagon-free)構造の depth 概念と同一かは要確認(GT側のdepth概念とB₃側の深さ概念の対応は未検証)。

懸念: **講義ノート(非査読・非arXiv)**であり、原論文(Ihara-Takao, Schneps 2006)への直接照合が必須。数値そのもの(691, 3617)は Ramanujan合同として独立検証可能(691はB₁₂の分子・3617はB₁₆の分子)。

### #4-6, #9-13 Brown系・depth-graded系
3-4行要約: Brown の2012 Annals論文(mixed Tate motives over Z の圏論的スパン性・Hoffman予想証明)を起点に、depth-graded構造・Broadhurst-Kreimer予想への複数のフォローアップ(Brown自身・Li・Enriquez-Lochak・Arbesfeld-Enriquez)。

なぜスペックの困難に効き得るか: freeness定理の**正確な言明**(何が自由で・どのgradingで)を求める L-6-3 に対し、#4(原論文)+#11(Homology/koszulity — Hilbert級数の理論的基礎)が本命。depth-graded次元表(L-6-4)は #5, #9, #10, #12 のいずれかの本文に載っている可能性が高いが、**abstractだけでは次元表の有無を断定できない**(すべて「深読み要」)。

深読み時の照合観点: Brown 1102.1312 本文 §の freeness定理のステートメント番号・grading の正確な定義(motivic weight か Lie algebra の内的次数か)を確認。depth-graded次元表がある場合、weight 12 の行を抽出し Schneps講義ノートの Ihara-Takao 係数(691, mod 3617)との整合を取る。

懸念: Li の2論文(#9, #10)は単著・査読状況不明(投稿版のみ arXiv 確認)。Ward(#13)は abstract 上「次元表なし」と自己申告的に読めるため優先度低。

### #7 Tsunogai 1997
3-4行要約: タイトルから「stable derivation algebraのrank(次元)とDeligneの問題」を扱う短報(Proc. Japan Acad. 3頁)。**L-4の直球候補**だが、本文は購読制で未読(メタデータのみ確認)。

なぜスペックの困難に効き得るか: タイトルが検索スペックの「重み別次元表」にほぼ字義通り一致。3頁の短報のため、次元表(weight ≤ 12など)がコンパクトに載っている可能性が高い。

懸念: **arXivになし**(1997年当時のarXiv math範囲外の可能性)・本文未確認につき機構一致度は「想定」であり実見していない。深読み時は projecteuclid での購読アクセス or 図書館経由の入手が必要。

### #8 Furusho survey(RIMS1357.pdf)
3-4行要約: GRT(Drinfeld's graded Grothendieck-Teichmüller群)とMZVの関係を扱う2002年サーベイ。冒頭8頁(Introduction・§1)を精読したが、**この範囲には次元表なし**。目次に「§5.2 stable derivation algebraの標準自由基底の候補への余談」(p.29)があり、ここに次元関連の記述がある可能性は残るが未確認。

懸念: 優先度は#1, #7より低い。深読みの価値は§5.2次第。

---

## 空振りだった角度・使ったクエリ

- **角度(c)著者系譜直接**: Dolgushev派(Dolgushev自身の論文)からの直接ヒットなし。GT業界の Fresse・Horel・Bar-Natan・Schneps のうち、Bar-Natan の "On associators and the GT group I"(math.toronto.edu掲載PDF)がヒットしたが、次元表・Ihara-Takao係数の存在は未確認(検索結果に出ただけで深追いせず)。
  - クエリ: `arxiv "Anatomy of an associator" Brown Dupont dimension table grt weight 12`(Dupont共著という誤前提で検索・実際は単著と判明)
- **角度(d)逆引き**: Ihara-Takao原論文(1990年代)そのものへの arXiv 到達は不可(存在確認は projecteuclid の Tsunogai論文経由の間接証拠のみ)。原論文の正確な書誌(タイトル・掲載誌)は今回未確定 — 次回検索で優先課題。
  - クエリ: `Ihara Takao "Some relations among Soule's elements" arxiv OR journal` → ヒットなし(タイトル推測が誤りの可能性)
  - クエリ: `Ihara Takao "Galois-Teichmuller theory and arithmetic geometry" relations stable derivation algebra weight 12 16` → Ihara関連論文は同アンソロジー内に別題("Comparison of some quotients...")で存在するが、Ihara-Takao共著関係式論文そのものは未特定
- **角度(b)機構直当て・depth-graded次元表**: Broadhurst-Kreimer予想の**元論文**(D. Broadhurst, D. Kreimer 自身の物理系論文、1990年代)は今回未検索 — 次回の宿題。
- **重み12の depth-graded 次元の具体的な数値**(motivic Lie algebra の weight-12行そのもの)は、どの候補の abstract にも明示されておらず、**本文深読みなしには未確認(UNKNOWN)**。

---

## 総括(検索係としての申し送り)

最も確度が高いのは **#1 Schneps講義ノート**(原文で係数・次元を直接確認済み)。これは非査読の講義資料のため、司令塔が降ろす際は #2(Ihara-Takao原論文の書誌特定)と #3(Schneps 2006原論文)への遡及確認を検討されたい。次点で **#7 Tsunogai 1997短報**(タイトル一致度最高だが本文未読)と **#4 Brown 2012 + #11 Enriquez-Lochak 2014**(freeness定理とHilbert級数の理論的支柱)。depth-graded次元表そのもの(weight 12の行)はどの候補でも実見未確認 — 深読み(reader委嘱)が必要。
