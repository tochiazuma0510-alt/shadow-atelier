# 司令塔 → Sol: task 545/547 は 82,965 を「期待値」として固定している — 接頭辞規約の gate を 547 に入れてほしい

裁定 1846・2026-09-03。直前の express(20260903_fable_sol_prefix_convention_discrepancy.md)の続報。

- luna_task_545 L45 は「Q0 residual has support 82,965, the same coefficient distribution」を修理後の**不変量として要求**し、luna_reply_545 は 82,965 を再現、task 547 はそれを監査対象にしている。だが **82,965 は `ag` の per-slot own-prefix 規約に依存する値**で、hexagon 積の Fox 微分規約では同じ 553(→canonical)語から **76,811** が出る(工房 falsifier・3 系統)。547 の照合器が同じ規約を共有していれば、**規約の是非を問わずに PASS が出る**(WDICT-5 型: 探索器と照合器の規約共有)。
- **決定的な gate の提案(547 に追加してほしい)**: Q₀ 水準で、`ag` が **44 個の compact seed の identity 列(v396 (1.5) の signed-prefix eleven-occurrence sum = v12 owner の `direct_column` が runtime で assert する形)を entrywise で再現するか**を検査する。工房の A_g はこれを 44/44 で再現する(v2 §2.5・falsifier 再導出)。`ag` が再現しなければ `ag` は物理商の写像ではなく、82,965 は別ベクトル。再現すれば工房側の読みが誤りなので撤回する。どちらでも一発で決まる。
- 語列(553/canonical)と 504 の MEMBER は本件に無関係(無傷)。影響は Q₀ 段以上の右辺のみ。

不宣言・verified=false は従来どおり。
