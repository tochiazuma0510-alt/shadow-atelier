# 論文検索報告: 接基点における慣性群の正準同一視(TB4)

**検索スペック**: (TB4) 「Gal(Ω/ℚ̄((β))) ≅ ℤ̂(1) で、(ζ_n) が定める生成元が π₁(P¹∖{0,1,∞}) のループ x に対応する」型の正確な言明と証明の正典出典。
**採否判断はしない**(司令塔の専権)。数学者への直接配達はしていない。

## 冒頭表

| 候補 | ID/書誌 | 年 | 実在確認 | 機構一致度 | 系統 |
|---|---|---|---|---|---|
| ① Deligne, "Le groupe fondamental de la droite projective moins trois points" | Galois Groups over Q, MSRI Publ. 16 (1989), pp.79-297; Springer chapter DOI 10.1007/978-1-4613-9649-9_3 | 1989 | **書誌のみ確認**(DOI 解決を確認・全文はログイン壁で未取得) | 高(定義の正本と目される)| B₃-gentle 系の外側(基礎文献・系統区分の対象外) |
| ② Hoshi–Matsumoto–Nakayama, "Tangential morphisms via log arithmetic geometry" | arXiv 2606.07993v1 | 2026 | **実在確認済み**(abstract + HTML 全文取得) | 中(用語の系譜確認に有効・TB4 の具体言明は未搭載) | 同上 |

候補は 2 件のみ(スペック指定どおり最有力 1–2 件)。他の関連候補(Hain–Matsumoto arXiv 1512.03975、Levine arXiv math/0509463、Schneps arXiv 1506.09050 等)は実在確認まで行ったが、TB4 の中心言明への一致度が低い(特殊文脈での再掲に留まる可能性が高く、深読み優先度は①②に劣る)ため、表には載せず「その他の実在確認済み候補」として下部に記載。

---

## ① Deligne (1989), §15 周辺

**書誌**: P. Deligne, "Le groupe fondamental de la droite projective moins trois points", in *Galois Groups over Q* (Y. Ihara, K. Ribet, J-P. Serre 編), MSRI Publications 16, Springer, 1989, pp. 79–297.

**実在確認の状況**: Springer の DOI (`10.1007/978-1-4613-9649-9_3`) は解決し、認証ページへリダイレクトされた(章として実在することの間接確認)。MSRI/SLMath の旧 PDF ホスト(`slmath.org/publications/books/Book16/files/deligne.pdf`)はサイト刷新後 SPA シェルへリダイレクトされ、本文取得は失敗。archive.org の候補 ID も 404。**節番号(§15)・命題/定理番号は本報告では live 確認できていない** — これは司令塔・数学者の記憶/二次文献に基づく通説であり、**本検索係としては UNVERIFIED** として扱う。

**なぜ TB4 に効き得るか(機構ベース、通説に基づく暫定メモ)**: この論文は接基点(point tangentiel)の定義そのものの出典であり、P¹∖{0,1,∞} の 0, 1, ∞ における接基点 01→, 10→ 等の局所モノドロミー(慣性)を、形式ローラン級数体上の絶対 Galois 群 Gal(k̄((t))/k̄((t))) ≅ ℤ̂(1) の言葉で正確に記述する一次資料と目される。TB4 が要求する「(ζ_n) が定める生成元とループ x の対応」の**向きの正規化**(どちらの回転方向、どの冪根系の整合的選択か)は、この論文の局所理論の節が定義した規約に遡ることになるはずで、他のどの二次文献も最終的にはここへ帰着させて引用する。

**深読み時の照合観点**:
- 接基点の定義箇所(通説では §10 前後から始まる「points tangentiels」関連節、§15 はその一部)を実際に開いて、慣性生成元の向き(ζ_n = exp(2πi/n) か exp(-2πi/n) か)の規約を確認すること。
- Ω = k̄((t)) 上の絶対 Galois 群の同一視で、t¹ᐟⁿ ↦ ζ_n t¹ᐟⁿ の形の作用がどちらの生成元にどう対応するかの式番号を特定すること。
- (TB4) 側の β の意味(どの局所座標か、01→ か 10→ かで符号が反転しうる)との整合を要確認。

**懸念**: 未入手のため、通説的な節番号(§15)は司令塔側の記述をそのまま踏襲しているだけで、本検索係が独立に検証した事実ではない。次段階で PDF 現物(大学図書館経由・ResearchGate・第二著者経由の私家版等)への直接アクセスが必要。

---

## ② Hoshi–Matsumoto–Nakayama, arXiv 2606.07993 (2026)

**書誌**: Y. Hoshi, M. Matsumoto, C. Nakayama, "Tangential morphisms via log arithmetic geometry", arXiv:2606.07993v1 (2026年6月投稿)。

**実在確認**: arXiv abstract ページおよび HTML 全文を直接取得して確認済み(捏造なし)。

**要旨の要約**: 接的射(tangential morphisms)— Deligne の接基点の高次元一般化として第二著者(松本)が導入した概念 — を log 幾何の言葉で再定式化する論文。本文 Remark 1 (§2) に「第二著者は Deligne 本人から、これが tangential base point という用語の由来だと聞いた」という直接の系譜証言がある。

**なぜ TB4 に効き得るか(機構ベース)**: TB4 の核心言明そのもの(慣性 ≅ ℤ̂(1)・ζ_n との対応)はこの論文の主眼ではなく確認できなかった(HTML 全文検索でも「inertia」「Ẑ(1)」「ζ_n」「canonical generator」の直接記述は見つからず)。したがって**一次資料としては効かない**。ただし、Deligne の原論文と現代的定式化との**用語・概念系譜の橋渡し**として、①の節番号特定作業で行き詰まった場合の参考文献リスト(著者らが引く SGA1 等の一次資料)を辿る入口になる。

**深読み時の照合観点**: 参考文献 [1]-[8] の中に Deligne 1989 への直接引用があるかどうか(取得した範囲では確認できず「なし」の可能性が高い)を再確認し、あれば書誌情報(巻・章・節番号)を抽出すること。

**懸念**: TB4 の具体的言明(ℤ̂(1) 同一視・ζ_n 対応)への一致度は「中」ではなく実質「低〜中」。系譜確認以上の価値は薄い。

---

## その他の実在確認済み候補(表外・優先度低)

いずれも arXiv API(`export.arxiv.org`)経由で実在確認済みだが、TB4 中心言明との一致は文脈依存(混合 Tate 動機・楕円 MZV 等の特殊化された前置きでの再掲にとどまる可能性が高く、深読み優先度は①②に劣ると判断):

- Hain–Matsumoto, "Universal Mixed Elliptic Motives", arXiv:1512.03975v4 (2015) — M_{1,1} の尖点における接基点 d/dq の文脈。
- Levine, "Motivic Tubular Neighborhoods", arXiv:math/0509463v3 (2005) — 混合 Tate 動機のための接基点構成の動機的類似物。
- Schneps, "Elliptic multiple zeta values, Grothendieck-Teichmüller and mould theory", arXiv:1506.09050v5 (2015) — 楕円版 double shuffle Lie 代数、tangential-base-point section との整合性。

これらは Ihara–Nakamura–Schneps 系譜(著者系譜角度③)の実在確認例ではあるが、いずれも TB4 が要求する「P¹∖{0,1,∞} 上の 0/1/∞ における古典的接基点の慣性生成元の正規化」そのものを主題にしていない(楕円曲線版・動機的類似物・高次元一般化)。

---

## 空振りだった角度とクエリ(負の結果・UNKNOWN 規律)

- **WebSearch(汎用検索)は本セッション予算を使い切っており(200/200 使用済み、他セッションとの共有と思われる)、途中から一切実行不可能になった**。角度②(Nakamura・Schneps 系解説、Szamuely 教科書の節特定)はこの制約のため未完了。Szamuely, *Galois Groups and Fundamental Groups* (Cambridge, 2009) の該当章・節番号は**一切検証できていない**(UNVERIFIED — 通説記憶のみで、本報告には未掲載)。
- arXiv API (`export.arxiv.org/api/query`) による直接クエリ試行(実行結果 0 件):
  - `abs:"tangential base point" AND abs:"inertia"` → 0 件
  - `abs:"tangential base point" AND abs:"canonical generator"` → 0 件
  - `abs:"inertia" AND abs:"pi_1" AND abs:"roots of unity"` → 0 件
  - `au:Nakamura_H AND abs:"tangential"` → 0 件(著者名インデックスの表記揺れの可能性大 — Nakamura が実際にこの主題の論文を持つことは間違いないが、arXiv API の author-id 検索と一致しなかった)
  - `ti:"tangential base points"`(タイトル限定) → 0 件
  - `abs:"tangential base point" AND abs:"Kummer"` → 1 件(Shiraishi 2307.09414、TB4 とは低一致)
- Deligne 論文原文の直接取得試行(失敗):
  - MSRI/SLMath 旧 URL → SPA シェルへリダイレクト、本文取得不可
  - Springer DOI → 認証壁
  - archive.org 候補 ID → 404
  - jussieu.fr(Schneps 個人ページ旧ドメイン)→ DNS 解決不可(ドメイン移転済み、後継 URL `webusers.imj-prg.fr` も接続拒否)

## 総括(検索係としての推奨)

①(Deligne 1989 原論文)は書誌としては実在するが、**節番号(§15)・命題番号を含む本文内容は本検索では未検証**。次段階で必要なのは Web 検索ではなく**現物 PDF の直接入手**(大学リポジトリ・ResearchGate・図書館経由)。②は用語の系譜確認以上の価値が薄い。**Szamuely 教科書・Ihara ICM 講演等、角度②で予定していた現代的解説の実在確認は WebSearch 予算切れのため未達 — 次便で再試行が必要**。
