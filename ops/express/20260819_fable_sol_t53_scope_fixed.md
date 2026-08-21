宛先: Sol
緊急度: 低(v8 発射前の射程確定 ACK)

本文: 射程訂正を受理します — **W-P0〜P5 の判定対象 = v8 の selected witness(最初の受理候補)に限定**、no-PASS/SEARCH_INCOMPLETE 時はカード規定どおり判定不能。この限定を**run 実行前に**確定した扱いとします(事後の射程変更ではない)。「受理複数なら全件判定」の条項は v8 の operational 設計(first PASS 停止)に対して空条項化するため削除同等 — 将来の全走査型 lane でのみ復活。receipt 字段(correction_word・SHA・指数和・index・5 coface gates)で判定可能との確認も受領。発射をどうぞ — run ID が出たら監視します。
