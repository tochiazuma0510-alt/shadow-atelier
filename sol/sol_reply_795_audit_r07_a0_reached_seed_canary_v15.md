# Sol Task795 hostile audit: A0 reached-seed canary v15

## 結論と第一到達 blocker

v512 の数学的縮約、producer v9 の `S`-schedule、両側に残した full
precision-two `G`-schedule、および v15 の fail-closed workflow は、静的には
委嘱どおりである。しかし checker v7 の production reached path には一つの
決定的な wiring defect があるため、現候補は dispatch 不可である。

`check_d972_r07_a0_fresh_precision2_endpoint_signature_v7.py:846--848` は
`validate_direct_canary(..., base_receipt)` の最終引数に、5-key の
`base_receipt` ではなく、atom/prefix/order 等を加えた 12-key の
`direct_canary` を渡す。同関数は lines 625--629 で payload から抽出した
5-key `base` と最終引数を exact equality で比較するので、正しい payload
でも常に

```text
checker_canary_base_rows
```

で停止する。外部の bounded reached test でも、現 production 引数形は
`REJECT:checker_canary_base_rows`、同じ値へ正しい `base_receipt` を渡した形は
`ACCEPT` となった。停止位置は checker の `bucket_terms` 構築と
`independent_replay` より前である。したがって checker 側の 21,287 回
precision-two aggregation はコード上は保存されていても、現 v7 では live
到達不能である。selftest が full `validate_direct_canary` の正常系を一度も
呼ばないため、この defect を検出できず PASS している。

## 1. 全文照合と exact receipts

指定順に全ファイルを最初から最後まで読んだ。全行は LF-only、CR/NUL は
0 だった。

| file | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `proof_r07_all_path_direct_canary_induction_v509.md` | 6,220 | 161 | `bee19b30ad8e3ced8905795566540626141d6623c1e8bcaf05e5389c0d0aff95` |
| `sol_task_789_audit_r07_all_path_direct_canary_induction_v509.txt` | 3,285 | 57 | `c4e0522c6a3aa15e9bd7cf35c62c76484aeeadcc3b6f87aadb78c845e4f7d349` |
| `sol_reply_789_audit_r07_all_path_direct_canary_induction_v509.md` | 16,116 | 378 | `a862524927f04547390114f7fa2425e9760d184a30c2c236c2ecf01fe5d71d61` |
| `proof_r07_all_path_direct_canary_induction_repair_v512.md` | 6,151 | 154 | `33997289c63c66392849ebdc81f4668172272f72057d54e383e50523059b2011` |
| `luna_task_791_r07_a0_reached_seed_canary_v9_v7_v15.md` | 6,656 | 148 | `ad8d553a4ab0245a8cfc955529fe091843d1fece5fa9eee4bc216f6bc1382929` |
| `luna_reply_791_r07_a0_reached_seed_canary_v9_v7_v15.md` | 8,739 | 176 | `8fa3851e61cdae7862910a9c78d57496609288a823abb23cb284fe4be7a02713` |
| producer v8 | 59,749 | 1,037 | `9acb4edcbbfcb4b1e8815918ee39215298d8c97811e99467bb713d9b41a2875c` |
| checker v6 | 98,228 | 1,654 | `8b3bcc7120dec651debb0d4af775c5f2429ea30481c336139252e44e5db73652` |
| workflow v14 | 12,320 | 187 | `6ce08d351d8db84448bcb4657ecbc13ba39dea7c0ddd7882b1a35265b486ada2` |
| producer v9 | 70,945 | 1,272 | `1422bec44e1367c0ea22043cb7b5e844ba8e7df69e3da763bd08e372d5dc8046` |
| checker v7 | 109,876 | 1,894 | `0599759e2c2311e771439cf7bce10fd3fb0ce99f498e60a62827aa12a1a460c4` |
| workflow v15 | 13,249 | 198 | `6710ae309ef24409e01f4e28bf2d219342b75c2ff6b49d7b6125c4014caf4f84` |

Task791 reply と v15 内の新規 bytes/SHA pins は全てこの実測値に一致した。

## 2. pins、AST/call graph、drift

ローカルに存在する pin を個別に再ハッシュした結果は次のとおりである。

- producer/checker の `PAPER_PINS`: 各 24/24 一致。
- pinned v12f の `SOURCE_PINS`: 28/28、bytes と SHA の双方が一致。
- checker の `SEVEN_PINS`: 6/6、bytes と SHA の双方が一致。
- prebuild、v12f、paper words の直接 pin: 3/3 一致。
- checker に残る inherited `PREBUILD_PINS` table: 5/5 一致。この table は
  production authentication からは呼ばれない inherited dead table である。
- workflow の repository-local checks: SHA 19/19、size 8/8 一致。Task601
  verdict の runtime 2 checks は production parent を download しないという
  委嘱に従い未実行であり、v14 との literal comparison のみ行った。

Top-level assignment AST は、producer では marker、新規 canary/prefix
constants と runtime profile の `profile/direct_replay` 以外が v8 と同一、
checker でも対応する versioned fields 以外が v6 と同一だった。
`EXPECTED_FILES`、Task601/Task554/Task595 identity、arithmetic/word pins、
dimensions、caps、target、packing、false claim flags に drift はない。

Top-level function/class AST は producer が旧 44 nodes 中 39 unchanged、
`replay_bucket_direct` を削除し、canary 用 9 helpers を追加、`evaluate` と
bounded fixtures のみを変更した。checker は旧 137 nodes 中 130 unchanged、
旧 bucket-direct helper を削除して 11 helpers を追加し、
`independent_replay` は progress/count return のみ、arithmetic body は同じで
ある。問題の最終引数取り違えは、新規変更された `validate_payload` 内に
限局する。

workflow v15 は v14 から workflow/path/fire token、v9/v7 bytes/SHA/markers、
v512/Task789 pins、artifact names だけを変更している。既存 env key の変更は
producer/checker SHA の二つだけ、追加は markers と v512/Task789 receipts の
六つ、削除は 0。permissions、runner、job timeout は同一だった。

## 3. producer の数学的 reached path

producer は `prior + replaced` から cancellation より先に sorted raw seed set
を取り、actual v14 parent では `S=23` となる。その各 seed に対する production
`direct_column((), relators[s-1])` call site は
`replay_reached_seed_base` 内の一か所だけであり、bucket loop 内にはない。
base row は完全な sparse dict を canonical sort してから `nnz` と SHA-256
だけを残す。

v512 と code を独立に展開した十一 slot は以下で一致した。

| slot | type / label / sign | actual left prefix |
|---:|---|---|
| 1 | E3 `H1_fxy +` | `G_yz G_xz^-1 G_xy = 1` |
| 2 | E3 `H1_fxz -` | `G_yz` |
| 3 | E3 `H1_fyz +` | `G_yz` |
| 4 | E3 `H2_fux -` | `G_uy G_xy^-1` |
| 5 | E3 `H2_fxy -` | `G_uy` |
| 6 | E3 `H2_fuy +` | `G_uy` |
| 7 | E4 `P_b1 +` | `G4^-1 G2^-1 G0 G3 G1 = 1` |
| 8 | E4 `P_b2 +` | `G4^-1 G2^-1 G0 G3` |
| 9 | E4 `P_b3 +` | `G4^-1 G2^-1 G0` |
| 10 | E4 `P_b5_inverse -` | `G4^-1` |
| 11 | E4 `P_b4_inverse -` | `1` |

Coordinate orderは `(0,1,2,3,0,4,5,6,7,8,9)`、signs は
`(+,-,+,-,-,+,+,+,+,-,-)` である。reverse-index prefix scan は positive
factor の場合だけその factor を occurrence prefix に含める。負符号は seed
relation の inversion に一度だけ入れ、その後に外側の符号乗算をしないため、
v512 の unsigned derivative convention と一致し、double sign はない。

Trie recurrence は各 slot で `quotient.mul(left,right)`、すなわち厳密に
`parent * atom` である。atoms は `(-2,-1,1,2)` を各一回評価し、負 atom と
正 atom の inverse equality を両型で検査する。非可換 `(1,2)` direct anchor
も独立評価される。係数 2 は producer の bucket accumulation と checker の
`add_full` で mod 3 scalar として保持される。

producer の一回の base `direct_column` は、pinned owner の
`occurrence_column` が六つの E3 relation endpoint を全て検査し、さらに
`EndpointMinimalJointEvaluator` が original conjugate を E3 と全 31 registered
E4 contexts で identity 検査する。したがって v512 の stronger base guard は
十一-slot endpoint だけから誤って推論されず、base call の live path で成立
する。

## 4. exact source、trie、bucket、precision two

次の必須経路は削除・sample・縮退されていない。

- Task601 manifest/files/root/verdict と source-ancestry digest を exact
  authentication し、literal leaves header を ancestry digest に結ぶ。
- raw roster を mod-three cancellation 前に取り、その後に exact
  `(seed, freely-reduced path)` keys を canonicalize する。
- 四 atoms から全 11-slot typed prefix trie を作り、全 path receipt を出す。
- key を `(seed, full 11-slot signature)` とする全 nonzero buckets を保持する。
  seed を representative に置換せず、equal physical row を equal word とも
  扱わない。
- producer は 44 seed precision-two cache の後、各 bucket representative と
  coefficient 1/2 に `act_precision2` と `aggregate_precision2` を一回ずつ適用
  する。checker の独立 arithmetic も同じ全 bucket を `act/aggregate/add_full`
  する。completion counters は total と exact equality で閉じる。
- lower/auxiliary 32,260、top 48,384、packing、target、receipts と全 false flags
  は predecessor のままである。

Actual immutable parent の値 `L=21,608, U=13,043, G=21,287, S=23` は Task788
の既存 result による。本監査は production を再実行していない。producer の
21,287 aggregation は live reachable だが、checker の同じ loop は F1 により
現在は到達不能である。

## 5. certificate、independence、live mutations

Manifest schema は v9、checker verdict schema は v7、direct canary schema は
`d972.r07.a0.reached-seed-direct-canary.v1` に分離されている。receipt は sorted
roster、各 seed の `(seed, nnz, canonical_sparse_row_sha256)`、completion、四
typed atoms、二 inverse equalities、noncommuting anchor、十一 labels/signs/
prefix bytes、zero-initialized rolling row digest、EOF を含む。

checker は producer/import/shared helper を使わず、local quotient/group/Fox/
precision-two arithmetic と `IndependentAllSeven` で roster、rows、atoms、
prefix/order、buckets、target を再構成する。F1 を一行修正すれば、producer
digest を信頼せず canonical rows から再計算した base receipt と exact compare
する経路になる。

現 production 引数 defect を隔離するため最終引数だけ正しい base receipt に
した同じ live validators に、全 mutation を逐次投入した結果は次のとおり。

| mutation | result / exact reason |
|---|---|
| slot 10 sign `- -> +` | reject / `checker_prefix_table_contract` |
| slot 10 prefix -> identity | reject / `checker_prefix_table_contract` |
| E4 slot -> E3 | reject / `checker_canary_atoms` |
| `parent*atom -> atom*parent` receipt | reject / `checker_canary_order` |
| pentagon factor order | reject / `pentagon_factor_order` |
| missing seed | reject / `checker_base_canary_eof` |
| duplicate seed | reject / `checker_base_canary_eof` |
| base-row digest change with rolling digest resealed | reject / `checker_canary_base_rows` |
| atom bytes change | reject / `checker_canary_atoms` |
| EOF false | reject / `checker_base_canary_eof` |
| truncated/missing EOF | reject / `checker_canary_shape` |
| 21,286/21,287 aggregation completion | reject / `checker_precision2_aggregation_incomplete` |

全 case を first rejection 後も続行した。validators 自体に false acceptance は
見つからず、F1 は caller の引数一個に限定される。

## 6. slow path / memory audit

旧 `replay_bucket_direct` definition と production call は両側から完全に消えて
いる。`direct_column` の唯一の production call site は sorted reached-seed loop
内であり、G loop 内には `direct_column`、generic Fox replay、context rebuild
のいずれもない。

Actual-parent static schedule は次のとおり。

| side | `direct_column` | bounded coordinate evaluations outside G | precision-two bucket actions |
|---|---:|---:|---:|
| producer | 23 | 23 endpoint + 4 atoms + 1 order anchor = 28 | 21,287 |
| checker | 23 | 23 endpoint + 4 atoms + 1 order anchor + 23 internal endpoint checks = 51 | 21,287 structurally; current live completion 0 because F1 precedes it |

ここで「generic calls」は v14 blocker と同じ complete `direct_column` 単位で
あり、auxiliary coordinate evaluations は全て `O(S)+O(1)`、G 非依存である。
全 31 contexts は producer runtime で一度だけ構築され、base rows は digest
後に保持されない。新しい dense per-bucket retained copy、parallelism、parent
replay、archive DOM はない。precision-two action が作る inherited transient
dense arrays と exact path/bucket receipts は必須計算であり、今回の canary が
追加した不要 owner ではない。

したがって 21,287 generic 再導入または別の不要 slow/memory-heavy path は
ない。ただし現 checker は intended 23 expensive base callsを終えた後に F1
で必ず捨てるので、修正前 dispatch は計算資源の浪費にもなる。

## 7. workflow と claim boundary

PyYAML 6.0.3 `BaseLoader` で v15 を local parse し、top keys、
`workflow_dispatch/push`、単一 job を確認した。全七 action uses は 40-hex commit
pin である。event SHA checkout、read-only permissions、immutable parent API
checks/downloads、Python 3.13 / NumPy 2.5.1、serial BLAS、8 GiB virtual-memory
limit、外部 timeouts、producer marker gate、独立 checker launch、checker marker
後だけの residual upload、always log upload は fail-closed である。push は
`[fire-fresh-precision2-endpoint-v15]` が無ければ production job に入らない。

F1 により checker exit 1、marker gate failure、residual upload skip となるので
偽 PASS は出ない。一方で有効な run も成功不能なので dispatch-safe ではない。
明示的 `UNKNOWN_RESOURCE:*` は `UNKNOWN_RESOURCE`、外部 timeout と inherited
meter stop も nonzero/`NOT_READY` であり、どの経路も NONMEMBER または A0 に
昇格しない。selftests は `fixture=PASS` だけを出し、fresh rho2/A0 manifest を
生成しない。

## 8. bounded external checks

repository 外の temporary pycache を用い、全 command は逐次終了した。

| command | exit | elapsed s | peak RSS bytes |
|---|---:|---:|---:|
| `python -X pycache_prefix=%TEMP%/task795-pycache-* -m py_compile <v9> <v7>` | 0 | 0.600665 | 27,631,616 |
| `python -B <v9> --selftest` | 0 | 0.259218 | 33,878,016 |
| `python -B <v7> --selftest` | 0 | 0.277381 | 37,720,064 |

producer は `fixture=PASS`, `direct_schedule=S`, base calls/completion `2/2`,
atoms `4`, full-prefix generic comparisons `0`。checker も `fixture=PASS`,
base `2/2`, `precision2_schedule=G`, mutation count `55` だった。この PASS が F1
を覆えない理由は、checker selftest が full canary validator 正常系を呼ばない
ためである。追加で AST/call counts、structural diff、pin hashes、上記 mutation
script、YAML parse を実行し、production parent、GHA、fresh rho2 は実行して
いない。残存 child process はない。

## 9. 最小有限修理

1. checker successor の production call で
   `inverse_equalities,direct_canary` を
   `inverse_equalities,base_receipt` に直す。validator 本体または数学を変更する
   必要はない。
2. checker の bounded selftest に、base-only receipt を最終引数として full
   `validate_direct_canary` 正常系を最低一回通す regression を加える。これで
   今回の 5-key/12-key wiring mismatch を直接捕捉する。既存 mutation farm の
   拡大や production-size fixture は不要である。
3. versioned checker/workflow successor を作り、新 bytes/SHA/schema/marker を
   pin し直して同じ bounded checks と hostile re-audit を通す。producer v9 の
   arithmetic/loop 修理は不要。修理前の v15 は dispatch しない。

```text
SAFE_TO_DISPATCH_GHA=no
ACTUAL_GENERIC_DIRECT_CALLS_PRODUCER=23
ACTUAL_GENERIC_DIRECT_CALLS_CHECKER=23_THEN_DETERMINISTIC_ABORT
RETAINED_PRECISION2_BUCKETS_PRODUCER=21287
RETAINED_PRECISION2_BUCKETS_CHECKER=21287_STRUCTURAL_0_CURRENTLY_REACHABLE
UNNECESSARY_GENERIC_21287_OR_MEMORY_HEAVY_PATH_REMAINS=no
A0: 0/1 ACTUAL
FRESH_RHO2=NOT_PRODUCED
COMMON_COMPATIBLE_LIFT_FAKE_IHARA=NOT_PROMOTED
verified=false
```

`VERDICT=FAIL_A0_REACHED_SEED_CANARY_V15`
