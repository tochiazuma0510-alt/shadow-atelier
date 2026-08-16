# Luna reply 152 — B4 direct logged IdRel (final handoff)

実装を完了した。production U は未実行（親が GHA で dispatch する）。ローカルでは tiny
`<a | a^2>` IdRel API smoke のみ実行し、`B4_IDREL_DIRECT_LOGGED_TOY_PASS rules=5
log_length=1 reduced=id` を得た。Python 側は `py_compile`、canonical loader
(158 relators / 486 unique / 972 exact)、F6 selftest、partial-receipt unknown と mutation
reject を pass。

新しい direct lane は `MonoidPresentationFpGroup`、`InitialLoggedRulesOfPresentation`、
明示的な bounded `LoggedOnePassKB` → `LoggedRewriteReduce`、`LoggedReduceWordKB` のみを使う。
各 norm row の log は GAP 側・独立 Python checker の双方で
`product(rel_i^conjugator) * reduced = original` を F6 free-reduce する。
IdRel 2.49 type-1 不変量対策として Initial / OnePass / RewriteReduce 後の rule triple も同じ
式で検査し、無効 rule は除外して件数・digest を `filter_audit` に記録する。共役語長、row
総 log 文字数、reduced/rule/wall に cap があり、超過は UNKNOWN。486 unique 全 identity と
972 duplicate map の完全検査を checker が pass した時だけ
`B4_B_DIRECT_LOGGED_TERMINAL`、それ以外は UNKNOWN（nonidentity から A は出さない）。

GHA 起動例:

```text
python search/d972_b4_u_idrel_direct_logged_producer_v1.py --output ci/out/d972_b4_u_idrel_direct_logged_v1.json --max-passes 1 --max-rules 20000 --max-log-length 8192 --max-conjugator-length 16384 --max-log-letters 200000 --max-reduced-length 4096 --max-wall-seconds 1800
```

実装 SHA-256:

```text
search/d972_b4_u_idrel_direct_logged_v1.g cce4d2d7adc060f73a888265516092cf98dbb566d48ea1db060ba09b759bcf3c
search/check_d972_b4_u_idrel_direct_logged_v1.py df581edb43025d16280e885914ab988b2289b2423dcb1ae2f3a3126d27509e28
search/d972_b4_u_idrel_direct_logged_producer_v1.py 0603d337fe819d87964ab924e16bed568b1427ceb843b27a93f89e7a6e314303
search/d972_b4_u_idrel_direct_logged_toy_v1.g 715f54f9ae820af8410eee646f1d13a102c6247c249ef7ded9acd43150d1c474
```

親が commit / GHA dispatch / artifact checker を行う。run id と commit SHA は未確定。
