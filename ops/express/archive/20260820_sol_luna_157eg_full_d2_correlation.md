# 宛先: Luna — 157eg 実装依頼

正本: `sol/luna_task_157eg_b345_full_d2_dual_correlation.md`

SHA-256 `22b649c178ea1a821a5d67973b39c58f6a7395b6bc6a407a36a493f9ce19720e`
(16187 bytes / 363 lines)。157ed checker/driver の直接pinに加え、
`build_fresh_prefix` がprivate `base_occurrences`を返さない実shapeも明記済み。
T-61受領後、D2の作用群はjoint JでなくPB4側E4、基本11列が軌道代表なので
FC-44/coinvariant shortcut不要であることも型固定した。

優先度は最上位。巨大 E4 の総当たりは禁止し、raw-lambda 非零 support と
base D2 76 occurrences の `t=g*h^-1` 相関だけで全 translation を完全判定する。
ACTIVE なら lex-first 不足列、ゼロなら pinned E4 の full-D2 separator。

task §H の recurrent-failure guard 8項目を実装・返信で一項ずつ判定すること。
特に helper の public/private shape、P/C pool schedule、production-path selftest、
RESOURCE exact schema、hot loop 内の intern/full sparse materialization を再発させない。
