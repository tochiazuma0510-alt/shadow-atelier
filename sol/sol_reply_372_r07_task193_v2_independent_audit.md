# Sol reply 372 — task193 v2 independent audit

## 判定

**REJECT** — 最初の load-bearing defect で停止した。

## F1 — adapter v3 は終了済み A0-v18 に版固定され、現行 GHA の正入力を物理的に受け取れない

adapter producer/checker はともに A0 の source identity を v18 の二本へ
hard-pin している。

- `search/d972_r07_history_free_task193_compat_adapter_v3.py:33-38`
- `crosscheck/check_d972_r07_history_free_task193_compat_adapter_v3.py:34-39`

さらに accepted 経路は、A0 checker を v18 の byte identity で load するだけでなく、
A0 verdict の `producer_pin` が **v18 producer の path/bytes/SHA-256 と完全一致**
することを要求する（producer `:156-166,204-210`、checker
`:159-169,205-211`）。これは健全な fail-closed pin だが、現在の production
campaign には接続できない。

物理事実は `sol/audit_r07_full_proof_reaudit_and_forward_direction_v220.md`
Delta 211 (`:8246-8286`) に固定されている。v18 run `33247540982` は
`UNKNOWN_RESOURCE`（RSS 5.7 GB frontier）で終了し、その後 UNKNOWN checker が
`TypeError: unhashable type: 'list'` で crash、completion sentinel も artifact upload
もなく **artifact 0** である。したがって v18 の accepted receipt/verdict は
`ci/in` へ解決できない。adapter driver 自身も
`search/d972_r07_history_free_task193_compat_adapter_gha_driver_v3.g:2,6-7,44-56`
で A0-v18 の二入力を外部供給されることを前提にしており、それを生成・取得する
経路を持たない。

一方、修理中の live successor は A0-v20 である。v20 が positive receipt/verdict
を生成しても、その verdict は v20 producer を pin するため、adapter v3 の上記
`producer_pin == A0_PRODUCER_PIN(v18)` gate で必ず `UNKNOWN_INPUT:A0 verdict
envelope` になる。ファイル名だけを `ci/in` に置き換えても通らない。

従って現時点の入力集合は

```text
v18 accepted physical artifact: EMPTY (terminal run, artifact 0)
v20 accepted artifact: adapter-v3 source identity gate rejects it
task193-v2 accepted production path: physically unreachable
```

であり、監査点 (5) の「実 GHA 入力を物理的に解決可能」を満たさない。これは
数学的な accepted replay の誤受理ではなく、live pipeline を空にする版固定欠陥
である。

## 最小 successor 条件

A0-v20 producer/checker が静的受理され byte identity が凍結した後、wildcard や
複数版許容へ弱めず、次の **exact-pin successor** を一組作るのが最小である。

1. adapter-v4 producer/checker で A0 producer/checker の path/bytes/SHA-256 を
   v20 の二本へ差し替え、専用 schema/terminal/source provenance も v4 に上げる。
2. compiler successor は adapter-v4 producer/checker の exact identities のみを
   pin する。対応する二 driver も同じ pin と terminal に上げる。
3. GHA は v20 の producer receipt と **v20 independent-checker verdict** を同じ
   run/artifact から `ci/in` に取得し、その物理 identities を adapter に渡す。
   UNKNOWN artifact は task193 accepted 入力に昇格させない。

v20 の identities が未確定な現在、仮 SHA や v18/v20 の OR-gate を入れてはならない。
この F1 で停止したため、direct sparse row 以降、compiler の H1/H2/P 符号・endpoint、
v1 shim、および過大 claim は本便では未裁定であり、successor に対して監査点 (1)
から全面再監査を要する。

```text
first defect: stale exact source pin leaves no physically resolvable accepted A0 input
safe behavior on wrong version: fail closed
live task193-v2 acceptance: unreachable
overall: REJECT
```
