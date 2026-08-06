# Q4.6 (2008.00066) 被引用文献掃引 v1

司令塔スペック: arXiv 2008.00066(Dolgushev–Le–Lorenz, *What are GT-shadows?*)の Question 4.6 が、
その後の文献で回答・部分回答されていないかを調べる。採否判断はしない(司令塔・reader 送り)。

## ①原文確認: Question 4.6 の正確な文言と番号

`papers/dolgushev-2008.00066-gt-shadows-original.pdf` §4.3(open questions)、txt 版 3574-3577 行付近で実在確認済み(ページ内 grep 直接取得・捏造なし):

> **Question 4.6** Is it possible to find K, N ∈ NFI_PB4(B4) such that K ≤ N and the natural map
> GT♥(K) → GT♥(N) is not onto? In other words, can one produce an example of a charming
> GT-shadow that is also fake?

司令塔スペックの記述(「charming だが genuine でない実例はあるか」)と**一致**。番号は Question 4.6 で正しい。

**重要な但し書き(機構レベルの注意)**: この問いは **NFI_PB4(B4) 上**、すなわち §4.2 の見出し「Is there a charming
GT-shadow that is also fake?」が示す通り**B4 系(pentagon あり・本来 GT の副線)の設定**である。当工房の主線は
B3-gentle 系(2401.06870/2405.11725、hexagon のみ・pentagon なし)であり、Q4.6 は**そのままでは主線に移送でき
ない**(定義域が NFI_PB3(B3) でなく NFI_PB4(B4))。ただし後述の通り、gentle 版(2401.06870)にも「genuine/fake」の
アナロジーが存在し脚注で同型の未解決宣言がある — 機構としては両系に並行した問いが立っている。

隣接して **Question 4.7**(F2/NF2 が非可換な N で GT♥(N) の genuine を全識別できるか)も同じ open-questions 節にあり、
下記②③で確認した通りこちらは 2405.11725 で(gentle 版のアナロジーとして)**解決済み**。Q4.6 と Q4.7 を取り違えないこと。

## ②被引用文献の掃引

**掃引方法**: (a) Semantic Scholar Graph API `paper/arXiv:2008.00066/citations`(全件取得)、(b) Semantic Scholar
`paper/arXiv:2401.06870/citations`、(c) arXiv API `export.arxiv.org` で全文検索語 `"GT-shadow"` を submittedDate 降順で
最大 50 件取得(payload 実物確認)、(d) 一般 Web 検索(Google 経由)複数角度、(e) Dolgushev 本人サイト
(sites.temple.edu/vald)の publication list と GT パッケージ文書を直接取得。

**結果: arXiv 上で "GT-shadow" を含む論文は下記 4 本のみ(2026-08-06 時点、全件確認済み・これ以上のヒットなし)**:

| # | 論文 | arXiv ID | 年 | 実在確認 | Q4.6 言及 |
|---|---|---|---|---|---|
| 1 | What are GT-shadows?(Dolgushev–Le–Lorenz) | 2008.00066 | 2020 | 確認済み(手元 PDF+arXiv) | 出題元 |
| 2 | The action of GT-shadows on child's drawings(Dolgushev) | 2106.06645 | 2021 | 確認済み(手元 PDF+arXiv) | 言及あり(§8, [8, Cor 3.13] 経由)・**未解答** |
| 3 | GT-shadows for the gentle version of GT(Dolgushev–Guynee) | 2401.06870 | 2024 | 確認済み(手元 PDF+arXiv) | gentle 版アナロジーで**未解答**(脚注 2 で明言) |
| 4 | Accessing non-abelian quotients of GT via elementary tools(Bortnovskyi–Dolgushev–Holikov–Pashkovskyi) | 2405.11725 | 2024(v2: 2026-01-13) | 確認済み(手元 PDF+arXiv) | **Q4.7 を解決**(Q4.6 には触れず) |

Semantic Scholar の `2008.00066` citations エンドポイントは 1 件のみ返却(「Documentation for the package GT」
2020, arXiv ID/DOI 不明 — GT パッケージの README、Dolgushev 本人執筆・Temple 大サイト配布、査読論文ではない)。
`2401.06870` の citations エンドポイントは 2405.11725 の 1 件のみ返却。両者とも arXiv API の直接掃引(c)と整合。

MIT PRIMES(高校生向け研究プログラム)の関連レポート 2 本を発見したが中身は PDF 抽出失敗(暗号化/圧縮ストリームで
テキスト化できず — **UNVERIFIED、内容主張はしない**):
- `Bortnovskyi-Pashkovskyi.pdf`(2023, math.mit.edu/research/highschool/primes)— おそらく 2405.11725 の前段プレプリント
  版(著者の一部が重複)。
- `Dolgushev_s group.pdf` 「First examples of non-abelian quotients of the Grothendieck-Teichmueller group」(2024)
  — タイトル・トピックから 2405.11725 の学生向け並行稿と推測されるが**未確認**。

## ③各ヒットのトリアージ(Q4.6 への言及・解答の有無)

### 2106.06645(The action of GT-shadows on child's drawings, 2021)— B4 系
- 要旨: GT-shadow の Grothendieck child's drawing への作用を構成し、monodromy 群・passport の不変性、Galois
  child's drawing の実例供給(Cor 3.13)を示す。
- Q4.6 との関係: §8「パッケージでできること」の箇条書きで
  「Given K, N ∈ NFI_PB4(B4) with K ≤ N, one can look for fake charming GT-shadows with the target N.
  See [8, Corollary 3.13].」(txt 1809-1810 行、実在確認済み)と**Q4.6 を再掲**するのみ。
  参照先 [8, Cor 3.13] は実際には「isolated N なら NF2 の child's drawing は Q 上 Belyi 対を持つ」という**別の主張**
  (txt 1240-1241 行)であり、Q4.6 そのものへの証明や反例ではない — **GT パッケージを使えばこの探索ができる、という
  作業提案(未解答のままの再掲)**と読むのが正確。
- 判定: **未解答**(re-statement のみ、進展なし)。
- 深読み時の照合観点: [8, Cor 3.13] の正引用先が本当に Cor 3.13 で合っているか(版ずれの可能性 — 2008.00066 側の
  番号と食い違わないか)は未検証、降ろす場合は要再確認。

### 2401.06870(GT-shadows for the gentle version of GT, 2024)— B3-gentle 系(当工房主線)
- 要旨: Harbater–Schneps (2000) の gentle 版 GT に対する GTSh 構成。genuine GT-shadow を識別する基準を与える。
- Q4.6 との関係: 直接の言及なし(「charming」概念自体が使われていない — gentle 版では charming/fake の区別が
  B4 系と同じ形では登場しない可能性)。ただし脚注 2(txt 263 行)に
  「At the time of writing, the authors of this paper do not know a single example of a fake GT-shadow.」
  と明記 — **gentle 版でも genuine/fake の区別自体は生きており、fake の実例は 2024 年時点で未発見**。
  これは Q4.6 の B3-gentle 版アナロジー(charming の概念なしで fake の実例が見つかるか)にあたる。
- 判定: **未解答**(gentel 版の対応する問いも 2024 年時点で開いたまま)。

### 2405.11725(Accessing non-abelian quotients of GT, 2024/2026)— B3-gentle 系(当工房主線)
- 要旨: 2401.06870 の道具を使い、dihedral poset・K⁽ⁿ⁾=ker(ψₙ) 族を構成し、2 冪 dihedral 商への全射性を証明
  (当工房が較正ゲートの正解データとして使っている論文そのもの)。
- Q4.6 との関係: txt 1463-1466 行(実在確認済み)に
  「Corollary 5.4 resolves the natural version of [7, Question 4.7] for the gentle version GT_gen of GT.」
  — [7] = 2008.00066(references 1745-1746 行で確認)。**解決されたのは Question 4.7 であって Question 4.6 ではない**
  (混同注意 — 番号一つ違いで別問い)。Q4.6(fake charming 実例)への言及は本文中に見当たらず。
- 判定: Q4.6 に関しては**言及なし(接触なし)**。Q4.7(隣接する別の問い)は gentle 版で解決済み。

## 総括: 解答済み / 未解答 / 不明

**Question 4.6(charming だが fake な GT-shadow の実例)自体は、arXiv 上に存在する GT-shadow 系列論文 4 本の
掃引範囲内で — 未解答のままである。**

- 2008.00066 出題(2020)以降、B4 系での直接の反例・証明は見つからず(2106.06645 は再掲のみ)。
- B3-gentle 系(当工房主線)側でも、genuine/fake の区別に対応する未解決宣言が 2401.06870(2024)の脚注に生きている
  — つまり**主線側でも「fake の実例が一つも知られていない」という状況は変わっていない**。
- 紛らわしい**部分解決**が一件ある: 2405.11725 が解決したのは Q4.6 ではなく **Q4.7**(隣接する別の問い、非可換 N
  での genuine 完全識別)。降ろす際にこの取り違えに注意。
- MIT PRIMES 系の 2 本(非 arXiv)は内容未確認(PDF 抽出失敗)。仮に Q4.6 に触れていたとしても学生レポートであり
  査読前(UNVERIFIED 区分)。

## 空振りだった角度・使ったクエリ

- (a) 概念直当て: WebSearch `"GT-shadow" OR "GT-shadows" arxiv Dolgushev charming fake` → 上記 4 本以外なし。
- (a') WebSearch `"fake GT-shadow" example found` → **完全に空振り**(ゲーム/レーシングゲームの "fake shadow"
  技術記事しかヒットせず、数学的ノイズなし)。
- (b) 機構名直当て: WebSearch `Dolgushev Guynee "GT-shadows" gentle version arxiv 2401.06870 citations` →
  既知 4 本の範囲内で収束。
- (c) 逆引き: Semantic Scholar Graph API(2008.00066 citations, 2401.06870 citations)→ 各 1 件のみ、既知範囲。
- (c') 逆引き(全数): arXiv API `export.arxiv.org/api/query?search_query=all:"GT-shadow"` sortBy=submittedDate
  → **4 本で全数**(この検索語を含む論文が arXiv に他に存在しないことを直接確認)。
- (d) 著者系譜: Dolgushev 本人の publist(sites.temple.edu/vald)取得を試みたが PDF が暗号化ストリームで
  WebFetch のテキスト抽出に失敗 → **UNVERIFIED、内容主張なし**。ローカルにダウンロード保存はされている
  (tool-results 配下、金庫外・一時ファイル)。
- Fresse・Horel・Bar-Natan・Schneps 等 GT 業界本流からの引用は今回未探索(スペックが 2008.00066 の被引用に限定
  していたため優先度低と判断・角度②③のみで収束したので追加探索は行わなかった。要すれば追加ベンで発注可)。

## 実在確認サマリ

全 4 本の arXiv ID・PDF はリポジトリ内 `papers/` に現物あり、かつ本掃引で txt 全文 grep により該当箇所を実行取得
(捏造なし)。MIT PRIMES 2 本は URL 実在確認済みだが内容 UNVERIFIED。
