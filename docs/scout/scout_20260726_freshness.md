# 鮮度スイープ 2026-07-26 — 主要未解決リストへの外部進展の有無

**任務**: URGENT 鮮度スイープ。2405.11725・2401.06870 の被引用・関連著者の新着・キーワード全文検索により、我々の主張(K⁽³⁾ 飽和・A₅ 飽和・|GT(M5)|=48・E23 等)への先行/衝突の有無を確定する。**採否・数学的評価はしない**(字面照合のみ)。

---

## 冒頭表

| # | 候補 | arXiv ID / URL | 年 | 実在確認 | 関連度 | 系 |
|---|---|---|---|---|---|---|
| 1 | 2405.11725 **v2**(改題: "Accessing non-abelian quotients of the Grothendieck-Teichmueller group via elementary tools") | arXiv:2405.11725 | v1: 2024-05-20 / **v2: 2026-01-13** | 確認済み(abs ページ直接取得) | **最高**(我々の基準論文そのものの改訂版) | B₃-gentle(主線) |
| 2 | Glenn C. Ma, "The action of GT-shadows on child's drawings" | Journal of Algebra 662 (2025) 514-527 / arXiv:2106.06645 の出版版 | 2025(掲載)/ 元 preprint 2021 | 確認済み(ScienceDirect + arXiv abs) | 低(B₄ 系・dessins 作用・dihedral 主張なし) | **B₄ 系**(副線・同名別物) |
| 3 | N. Combe, "Proving the Grothendieck–Teichmüller Conjecture for Profinite Spaces & The Galois Grothendieck Path Integral" | arXiv:2503.13006 | v1 2025-03-17 / v2 2025-07-02 | 確認済み(abs ページ直接取得) | **低〜要注意**(GT 全射性を全称的に主張・GT-shadows/dihedral/GTSh への言及なし・独自用語「Cubic Matrioshka」で標準的先行研究との接続薄い) | 別系統(profinite spaces・非標準) |
| 4 | (ノイズ)Simone Tagliente, 4-manifolds with infinite dihedral π₁ | arXiv:2603.17013 | 2026 | 確認済み | 無関係(キーワード「dihedral」のみ一致・4 次元トポロジー) | 無関係 |
| 5 | (ノイズ)Huang–Xie, arc-transitive inner-automorphic Cayley graphs on dihedral groups | arXiv:2604.04366 | 2026 | 確認済み | 無関係(グラフ理論) | 無関係 |

候補 2・4・5 は空振り側(記録のため掲載)。**新規の脅威候補は実質ゼロ件**。

---

## 詳細

### 候補 1: 2405.11725 v2(最重要チェック対象)

- **確認方法**: `https://arxiv.org/abs/2405.11725v1` と `v2` を直接取得し、abstract を逐語比較。
- **結果**: **v1 と v2 の abstract は一字一句同一**。変更点はタイトルのみ("First examples of non-abelian quotients..." → "Accessing non-abelian quotients... via elementary tools")。journal-ref フィールドなし(まだ正式出版情報は反映されていない、または雑誌側の要望でタイトル変更のみ行った改訂と推測されるが、**これは司令塔の解釈であり本報告の主張ではない**)。
- **Conjecture 5.1 の現状**(abstract 内の文言そのまま): "we conjecture that the natural homomorphism from G_Q to the finite group GTSh(K,K) is surjective for every object K of the dihedral poset" — **依然として conjecture のまま**。証明済みは 2 冪の場合(Thm 5.3)のみで変化なし。
- **K⁽³⁾ / 奇数 n への言及**: v2 本文(HTML)を精査したが、**K⁽³⁾ の明示的計算・奇数 n の証明は見当たらない**。Prop 3.4-3.6 で K⁽ⁿ⁾=K⁽²ⁿ⁾(奇数 n)という構造的事実のみ。
- **GAP 計算・|GTSh(K,K)|=48 等の言及**: **なし**。A₅ や位数 48 への言及も見当たらない。
- **字面照合(我々の主張との衝突可能性)**: **衝突なし**。我々の K⁽³⁾ 飽和・|GT(M5)|=48・A₅ 飽和の主張と同一の定理を述べている箇所は確認できなかった。ただし **v2 が 2026-01-13 に改訂された事実自体は司令塔に急ぎ共有すべき**(本文全体の詳細差分までは今回未検証 — abstract 比較のみ。念のため full diff は要請があれば追跡可能)。

### 候補 2: Glenn Ma (2025, Journal of Algebra)

- 2401.06870/2405.11725 系列とは別に、B₄ 系副線(2106.06645 の正式出版)。dessins d'enfants への作用の記述論文で、dihedral 全射性やケント射性の主張なし。**先行/衝突なし**。

### 候補 3: Combe 2503.13006(要注意フラグのみ)

- GT 予想(GT ≅ Gal(Q̄/Q))の「profinite spaces での証明」を主張する論文。**GT-shadows・GTSh・dihedral poset への言及は確認できず**、我々の B₃-gentle 系との接続点なし。独自概念("Cubic Matrioshka" アルゴリズム、path integral)を用いており、標準的な GT 文献(Dolgushev 系譜・Fresse・Horel 等)との相互引用も検索上確認できなかった。**採否判断はしないが、司令塔への申し送り: 出所の異例さ(全称的主張・非標準用語・査読情報なし)に留意**。

---

## 空振りだった角度・使用クエリ

1. **被引用検索(角度 a)**: `"2405.11725" cited by 2025 2026 dihedral` / `"2401.06870" GT-shadow cited by 2025` — Semantic Scholar 直接ページ取得は失敗(JS 読み込み待ちページのみ返却)。Google 経由の間接情報のみ(Glenn Ma 論文がヒット、上記候補 2)。**INSPIRE-HEP 経由の被引用検索は未実施**(このサービスは数学よりHEP寄りで today のクエリでは有効なヒットなし・時間の都合で優先度を下げた)。
2. **著者系譜追跡(角度 c)**: `Bortnovskyi Pashkovskyi Holikov arxiv 2025 2026` / `Guynee Dolgushev arxiv 2025 2026` / Google Scholar プロフィール(`scholar.google.com/citations?user=wMx0U6wAAAAJ`)・Temple 大 publist.pdf 取得 — **Google Scholar ページはロード不完全**(2017 年までの表示のみ確認、JS 依存の制約)、publist.pdf は ECONNRESET で取得失敗。新規共著論文の存在は確認も否定もできず(**UNKNOWN**)。ただし Temple 大セミナー掲示(2026-03-18 Haifa 大学)では 2405.11725 を基にした講演のみで新論文の言及なし。
3. **キーワード全文検索(角度 a/d)**: `"GT-shadows" arXiv 2025 2026` / `"fake GT-shadow" OR "pentagon independent"` — 新規論文ヒットなし。既知の 4 本(2008.00066・2106.06645・2401.06870・2405.11725)以外の GT-shadows 論文は arXiv 上に検出されず。
4. **「dihedral」×「Grothendieck-Teichmuller」全般(角度 a)**: 上記候補 4・5 のようなノイズ(無関係分野での「dihedral」キーワード一致)のみ。MathOverflow 検索も既知論文の再掲のみで新規質問ヒットなし。

---

## 最終報告(司令塔向け要約)

- **先行/衝突: なし**(確認できた範囲で)。
- **ヒット数**: 実在確認済み候補 5 件(うち直接関連 1 件 [2405.11725 v2]・B₄ 系副線 1 件 [Ma 2025]・要注意フラグ 1 件 [Combe 2503.13006]・無関係ノイズ 2 件)。
- **最重要フラグ**: **2405.11725 に 2026-01-13 付の v2 改訂あり**(abstract 同一・タイトル変更のみ確認・full diff 未実施)。Conjecture 5.1 は依然未解決、K⁽³⁾・奇数 n の新規証明やGAP計算の追加は確認されず。我々の C-1..C-5(K⁽³⁾ 飽和・A₅ 飽和・|GT(M5)|=48)と字面上重複する主張は見つからなかった。
- **UNKNOWN 事項**: Dolgushev 系譜著者陣の 2025-2026 年新規投稿の有無は Google Scholar/publist.pdf 取得失敗により完全には確定できず。必要なら再スイープを推奨。
