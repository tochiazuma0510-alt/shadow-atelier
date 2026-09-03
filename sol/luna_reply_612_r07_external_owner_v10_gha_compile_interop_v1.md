# Luna reply 612 - external-owner v10 strict compile/interop GHA wrapper

## Result

Task612 の指定どおり、監査済み v10 三ファイルを変更せず、有限な
compiler/wire-interop gate 用 workflow を追加した。

- runner は `ubuntu-latest`、Python 3.13、job timeout は 15 分。
- matrix、shard、package install、production input、rank-8059 adapter はない。
- branch は `sol/r07-explicit-lift-20260825` に限定し、push は
  `[fire-external-owner-v10-interop]` marker を job gate で要求する。
  `workflow_dispatch` も許可した。
- 実行前に C worker、Python owner、checker の三つの SHA-256 を exact
  match で認証する。
- 実行コマンドは
  `python -B search/check_d972_external_owner_gf3_worker_v10.py` の一つだけ。
  stdout/stderr 全体を一つの raw log に保存する。
- checker の exit code を別に保存したうえで、最終非空行を JSON として
  parse し、整形済み `report.json` を先に書いてから Task610 の numbered
  gate 1--9 を全て assert する。したがって checker の exit zero だけでは
  workflow は通らない。
- raw log、parsed JSON、checker exit を一つの artifact に `always()` で
  upload する。認証以前の失敗でも空の artifact にならないよう、三ファイル
  には正直な `NOT_RUN` 初期値を置き、checker 実行時に上書きする。

## Exact gate coverage

Inline assertion は次を exact 値で閉じる。

1. compiler が `NONE` でないこと、production/test-only の strict compile
   command、strict warning flags、60 秒内部 timeout を完了して checker が
   report へ到達したこと、failpoint define の production 不在/test 一回。
2. version 10、wire 88、record 56、rank 4095、rank-8059 out-of-scope、
   `production=false`、`verified=false`。
3. static/dense PASS、16 offers、3 accepted、ID5 coefficient-one witness。
4. 五 stream の exact SHA-256。
5. compiled campaign の exact STATS/CLOSED/EOF/exit-zero、cancellation、
   five-stream whole-byte image、cursor/finalize。
6. 三 cap、87 partial headers、malformed/noncanonical、test-only allocation
   FATAL、89-byte/89-fragment request。
7. 81-entry table、fragmented response、stall/short poison cleanup、reuse reject。
8. hard-kill の committed 4、provisional IDs `[5,6]`、physical offsets 7、
   suffix resume、clean controls 4 と四つの exact rejection names。
9. report 全体に `NOT_RUN_NO_COMPILER` がなく、terminal
   `interoperability=PASS` であること。

## Frozen source receipt

| file | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_external_owner_gf3_worker_v10.c` | 22,449 | 763 | `8938bcdad693553266aeb08cfe023548fcb8d5965683157e60df564ea16681bd` |
| `search/d972_external_owner_gf3_worker_v10.py` | 38,121 | 1,026 | `3b6441063348987d101a9dc8ac019b2dcc85dee983f77342b821db710c00a16c` |
| `search/check_d972_external_owner_gf3_worker_v10.py` | 44,071 | 1,256 | `34016ce93096cfdc1e28735468a624016c6e53be6b39a1002adc1f07b9d44f63` |

## New workflow receipt

| file | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `.github/workflows/d972-r07-external-owner-v10-interop-v1.yml` | 11,903 | 244 | `f3b045809a0440502a1b12d5420e176627041c57e19e4d52a1ab180b60a93c22` |

## Local no-compiler sanity

```text
PyYAML safe_load: PASS
workflow steps: 7
inline Python compile(): PASS
inline Python source bytes: 7003
source hash pins: exact frozen values
GHA dispatch: NOT_RUN
strict compile/interop: NOT_RUN
```

No compiler、GHA、production calculation、git operation はこの実装便では
実行していない。run ID と head SHA は発火後に root reply へ記録する。

```text
TASK612_WORKFLOW_IMPLEMENTATION: COMPLETE
READY_FOR_ROOT_COMMIT_AND_ONE_BOUNDED_GHA_CAMPAIGN: YES
PRODUCTION: false
verified: false
```
