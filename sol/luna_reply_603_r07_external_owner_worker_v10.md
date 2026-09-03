# Luna reply 603 — bounded external-owner worker v10 repair

## Result

Task603 の指定どおり、v9 を凍結したまま次の v10 三ファイルを追加した。
変更は Task600 の F1--F4 に限定し、proof、v220、workflow、git、GHA、production
には触れていない。

- C kernel は packed subtraction table を厳密に
  `SUB[coefficient][left][right]` として構成する。特に
  `SUB[1][1][1]=0` である。packed-byte elimination、scale-two table、
  first-trit table、monotone byte cursor、pivot/companion semantics は維持した。
- rank/offer/byte cap のいずれでも session-owned `LEDGER` を解放せず、
  unchanged-counter `UNKNOWN_RESOURCE` の直後に `continue` する。
  ledger は service cleanup で一度だけ解放する。`write_full` は残量を
  完送する loop にし、strict-warning 対象の compact conditionals を分離した。
- owner は `read1` による唯一の lifetime pipe reader を持つ。
  checker だけが指定する optional deadline は、一つの response の header/body
  に同じ absolute deadline として適用され、production default は `None` である。
  poison は terminal で、kill、reap、stdin/stdout close、durable-stream close、
  reader join を終えてから制御を返す。partial durable transaction も poison し、
  `finalize` は成功・失敗を一つの cleanup path で閉じる。
- committed replay は present な四／五 stream を一度だけ開き、transcript、
  offsets、basis、companion、leads の declared prefix を lockstep で消費する。
  canonical packed bytes、declared EOF、normalized first lead、lead/ID binding を
  同じ pass で検査する。live/resume の first-lead は 81-entry packed-byte table
  を使う。
- checker は supplied campaign の exact bytes を decode する独立 dense pass から、
  transcript、offsets、basis、companion、leads の五つの完全期待像を構成して
  whole-byte 比較する。88-byte header と `88+pn+cn` frame を別々に検査する。
  coefficient-one cancellation、literal STATS/CLOSED/EOF、三 cap、四 isolated
  mutations と各 clean-resume control、1--87 byte partial headers、terminal
  malformed/noncanonical、compile-time test-only allocation FATAL、fragmented
  request/response、stalled/short response、offer 4 manifest と physical provisional
  offer/offset 5--6 の各 gate を実装した。allocation failpoint define は normal
  production compile command に含まれない。

`MAX_RANK=4095` は維持した。rank 8059 の grade-one adapter は追加していない。

## Local bounded evidence

実行した command と結果は次のとおり。

```text
$env:PYTHONPYCACHEPREFIX = Join-Path $env:TEMP 'shadow-atelier-task603-pyc'
python -m py_compile search/d972_external_owner_gf3_worker_v10.py search/check_d972_external_owner_gf3_worker_v10.py
=> exit 0

python -B search/check_d972_external_owner_gf3_worker_v10.py
=> exit 0
=> static_source=PASS
=> dense_reference=PASS; offers=16; accepted_reference=3
=> dense_coefficient_one_witness=ID5_DEPENDENT_AFTER_C1_C1
=> packed_first_table_81=PASS
=> fragmented_response=PASS
=> stalled_response=DEADLINE_POISON_REAP_CLOSE_JOIN
=> short_response=EOF_POISON_REAP_CLOSE_JOIN
=> poison_reuse=REJECTED
=> compiler=NONE
```

独立した `%TEMP%` state harness でも、期待五 stream の lockstep replay と、
四 mutant の固有拒否理由を直接通した。

```text
OWNER_LOCKSTEP_AND_FOUR_MUTATION_REASONS: PASS
future_pair       -> future_pivot
lead_id_swap      -> lead_binding
offset_interval   -> record_offset_binding
record_basis_lead -> basis_binding
```

この host では `cc`、`gcc`、`clang`、`cl`（加えて `zig`、`tcc）を検出できなかった。
したがって strict C compile、compiled interop、raw-wire、cap、durable resume、
hard-kill、compiled mutation、CLOSED/exit-0 gates はすべて正直に
`NOT_RUN_NO_COMPILER` である。checker はそれらを省略・弱化せず、compiler が
ある host で有限 timeout 付きに実行する。

独立 dense expected-stream SHA-256 は次のとおり。

```text
basis.bin      29cb9adc78f3170a94efdf7d017a6e171929186d761281b99005473f4790ac12
companion.bin  351ea4ae333c69e88e860823d5bbc4df2e165020fc47f755d318b3a6ddab9f7a
transcript.bin e668ea9177aca442e3adf6be177246d5581fbea0737912ea52172dc473f1c1ab
offsets.bin    5d9363ec924b847008bdd68a724b3bd7a1980c2439938219d2b898513a5e3d30
leads.bin      0c63c9bdd21f44653a6c359796aafab772898febbadb5413a0f22738d6c39a30
```

## Receipt

読んだ委嘱／監査と生成物の exact receipt は以下である。

| file | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `sol/luna_task_603_r07_external_owner_worker_v10.md` | 2,613 | 46 | `eb682db3406dbb9058e38ffa5662930187dc99d56c95387a0aeb27dfb2613def` |
| `sol/sol_reply_600_audit_r07_external_owner_worker_v9.md` | 12,345 | 224 | `345b0cec56f692802108727c472a36dc43d1f3da794c87d5d75232251f01ae55` |
| `search/d972_external_owner_gf3_worker_v10.c` | 22,449 | 763 | `8938bcdad693553266aeb08cfe023548fcb8d5965683157e60df564ea16681bd` |
| `search/d972_external_owner_gf3_worker_v10.py` | 38,121 | 1,026 | `3b6441063348987d101a9dc8ac019b2dcc85dee983f77342b821db710c00a16c` |
| `search/check_d972_external_owner_gf3_worker_v10.py` | 44,071 | 1,256 | `34016ce93096cfdc1e28735468a624016c6e53be6b39a1002adc1f07b9d44f63` |

## Readiness

```text
TASK603_V10_IMPLEMENTATION: COMPLETE
LOCAL_STATIC_DENSE_AND_OWNER_TRANSPORT: PASS
STRICT_COMPILE_AND_INTEROP: NOT_RUN_NO_COMPILER
READY_FOR_FRESH_SOL_STATIC_AUDIT: YES
READY_FOR_PRODUCTION: NO
PRODUCTION: false
verified: false
```
