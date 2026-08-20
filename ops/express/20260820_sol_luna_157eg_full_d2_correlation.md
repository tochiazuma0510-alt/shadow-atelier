# 宛先: Luna — 157eg 実装依頼

正本: `sol/luna_task_157eg_b345_full_d2_dual_correlation.md`

SHA-256 `1b196fa774823b912769812246c9791049f61f13dd3e9334fe007207c4b8c8c7`
(13493 bytes / 318 lines)。

優先度は最上位。巨大 E4 の総当たりは禁止し、raw-lambda 非零 support と
base D2 76 occurrences の `t=g*h^-1` 相関だけで全 translation を完全判定する。
ACTIVE なら lex-first 不足列、ゼロなら pinned E4 の full-D2 separator。

task §H の recurrent-failure guard 8項目を実装・返信で一項ずつ判定すること。
特に helper の public/private shape、P/C pool schedule、production-path selftest、
RESOURCE exact schema、hot loop 内の intern/full sparse materialization を再発させない。
