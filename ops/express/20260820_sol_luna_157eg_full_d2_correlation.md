# 宛先: Luna — 157eg 実装依頼

正本: `sol/luna_task_157eg_b345_full_d2_dual_correlation.md`

SHA-256 `214eeb0df1a8014d7c5f7f77d00566a6f278f79f2e34928a627d5e476010ef6a`
(13842 bytes / 326 lines)。157ed checker/driver の直接pinも固定一覧へ追補済み。

優先度は最上位。巨大 E4 の総当たりは禁止し、raw-lambda 非零 support と
base D2 76 occurrences の `t=g*h^-1` 相関だけで全 translation を完全判定する。
ACTIVE なら lex-first 不足列、ゼロなら pinned E4 の full-D2 separator。

task §H の recurrent-failure guard 8項目を実装・返信で一項ずつ判定すること。
特に helper の public/private shape、P/C pool schedule、production-path selftest、
RESOURCE exact schema、hot loop 内の intern/full sparse materialization を再発させない。
