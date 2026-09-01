# Luna reply: Task482 v3

Status: `TASK482_R07_RANK99_DURABLE_DISCOVERY_V3_PASS`

Task482 の指定された4成果物だけを作成しました。v2 は変更していません。

- `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v3.py`
- `crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v3.py`
- `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v3.g`
- 本返信ファイル

実装ゲート:

- 固定 rank-ladder v3 の `v3.tau_free_adjoint(P,m,args)` を prefix replay、batch replay、実 candidate generation で使用。bound v2 helper の3引数呼出しはありません。
- checker は replay 前に durable checkpoint と base/appended batches、chronological records、accepted sources/count、batch/round/rank、profile、segments、C99 identity、rolling prefix を完全一致束縛します。
- segment 検証は appended rows を一度だけ時系列走査し、rolling prefix digest と ledger digest、compact READY-core seal を再計算します。旧 cumulative ancestor I/O/deep-copy はありません。segment の `prior_state_seal` はこの compact READY-core 式で producer/checker 同期です。
- v427 の soft boundary は batch owner 内で `flush_rows(...)` に戻り、0 rows は直前の last-closed、1--16 rows は通常の `close_batch`/single update/atomic write、hard close failure は直前 seal に rollback します。soft branch と通常 branch は同じ flush helper を通ります。
- v426 driver は `UNKNOWN_RESOURCE` で sealed receipt/checkpoint と fresh `RESOURCE_CANDIDATE` marker のみ認証して checker を skip。`COMMON_CANDIDATE` の場合だけ checker を一回実行し PASS 後に COMPLETE を出します。
- limit margin は search soft/internal hard/external wall = `14040 < 14220 < 14400`、RSS/hard RSS/VM = `4200000000 < 4500000000 < 5120000000`。旧 `4687500`/`4800000000` equal envelope はありません。

Bounded gates:

- producer fixture: PASS（1/15 rows、zero fallback、hard rollback、zero/17 reject、same early-close resume equality、two-segment row mutation、identity/prior seal mutation、実 `replay_prefix` v3 ABI、single update）。
- checker self-test: PASS（16-row、variable 1/15、zero/17、flat chain、top-level durable mutation before replay、one-input-read、identity/prior seal、unsafe paths）。
- producer fixture/pin-check、checker self-test/pin-check、Python AST、driver static process/RSS/timeout gate、GAP `ReadAsFunction` parse: PASS。
- symlink fixture は Windows の symlink 作成権限で `symlink_platform_limited=true`。production/checker の symlink escape rejection は exact path gate を保持し、他の temporary fixture は repo 外で実行しました。
- production、GHA、git、authority replay、bytecode cache は実行していません。persistent Omega/cache/framework は追加していません。

Live pins:

```text
producer 100066 90bd58dce838eb518da7b32d8eaec210223efdee6a35d5f98d404e57517615a1
checker  66854 70540c60f0685539d21ca5a23c10cdacb840c4317b93b88fa57fb89fc7398c35
driver    8488 8ee2253e244f45e27307d72f7cbacf613211c10381858340e29c7b52fc7ee616
binding   71d8f66576cccf2f91e8641e1a0f0f3d00d104502a6f3d428356db9df2de8aa6
```

Later COMMON-only artifact driver is not separately needed: the v3 driver already performs the final full-prefix checker branch when a COMMON candidate is emitted; a resource candidate remains a producer-authenticated candidate for the next owner.
