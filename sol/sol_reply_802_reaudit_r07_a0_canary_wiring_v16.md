# Sol(max) Task802 — hostile narrow re-audit of A0 canary wiring v16

## 裁定概要

狭い release audit は合格である。Task795 の唯一の到達 blocker だった
checker production call の最終引数は、twelve-key `direct_canary` から、同じ
run で独立再構成した five-key `base_receipt` へ正しく交換された。v8 の
positive fixture は full receipt と base receipt を別 object・別 key set として
完全な `validate_direct_canary` 経路へ渡して受理され、同じ twelve-key object
を両役へ渡す hostile check は `checker_canary_base_rows` で拒否された。

Producer v9 は Task795 監査時と同一 bytes/SHA である。Checker の数学・算術、
owner/source universe、target、schedule、caps、precision-two aggregation、claim
flags に変更はない。実際の immutable parent に対する generic `direct_column`
は producer/checker 各 23 回であり、四つの typed atom 評価を別に保持する。
`G=21,287` は generic direct 評価へ戻っておらず、precision-two aggregation
として両側に全件残る。GHA/production は実行しておらず、その結果も主張しない。

## 1. 全指定入力の byte receipt

全十ファイルを UTF-8 bytes のまま最初から最後まで読んだ。いずれも LF-only、
CRLF なしである。

| file | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `sol/luna_task_800_r07_a0_canary_wiring_repair_v16.md` | 2,583 | 60 | `6e5f38aa55a97b3b26d05817cd883d96ddebff5ef6ba3fbe5acc013961bb0ed8` |
| `sol/luna_reply_800_r07_a0_canary_wiring_repair_v16.md` | 3,732 | 50 | `fad2b60d50aa8f1870be4554906466954df17293471b051139b45b5c1c32a5d9` |
| `sol/sol_reply_795_audit_r07_a0_reached_seed_canary_v15.md` | 16,063 | 275 | `fc5cc176eb4b1da22b28b8881ca3bc5f4718b65356c76fc270cfdc08ee4804c6` |
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py` | 70,945 | 1,272 | `1422bec44e1367c0ea22043cb7b5e844ba8e7df69e3da763bd08e372d5dc8046` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v7.py` | 109,876 | 1,894 | `0599759e2c2311e771439cf7bce10fd3fb0ce99f498e60a62827aa12a1a460c4` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v8.py` | 111,387 | 1,925 | `1e8e82191bb8d82189a194010228ed180ebc0607732a6bb338ab13abf16d86fc` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v15.yml` | 13,249 | 198 | `6710ae309ef24409e01f4e28bf2d219342b75c2ff6b49d7b6125c4014caf4f84` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v16.yml` | 13,249 | 198 | `996854c74cefbfc873bfa09ed74881c4163bebf32bc5880310f069748831e2f5` |
| `sol/proof_r07_all_path_direct_canary_induction_repair_v512.md` | 6,151 | 154 | `33997289c63c66392849ebdc81f4668172272f72057d54e383e50523059b2011` |
| `sol/sol_reply_789_audit_r07_all_path_direct_canary_induction_v509.md` | 16,116 | 378 | `a862524927f04547390114f7fa2425e9760d184a30c2c236c2ecf01fe5d71d61` |

## 2. Exact checker v7 -> v8 diff

機械的 unified diff は 6 hunks、36 additions、5 deletions で、全体は次のとおり。

```diff
--- search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v7.py
+++ search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v8.py
@@ -13,7 +13,7 @@
 TASK601_MANIFEST_SHA='381f961fc808076c5c0adbc98e32c19742565087bffbcd5f99772533e05d5c22'
 DECISION_BODY='62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d'; DECISION_HEAD='07de7a817e8c5ae2e7346402a290c32631d05b0cc621d03702faa6cb43a948c0'; BASIS_SHA='b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d'; REMAINDER_SHA='564cbfafc869a8c6eb761a392caa5e792b546bf577af7fe808177b2fdf13cbb0'
 PREPARE_SHA='1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865'
-MARKER='R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V7_CHECKER_PASS'
+MARKER='R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V8_CHECKER_PASS'
 RHO2_MARKER='R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CANDIDATE'
 DIRECT_REPLAY_LABEL='reached-seed-base-plus-four-actor-v1'
 DIRECT_CANARY_SCHEMA='d972.r07.a0.reached-seed-direct-canary.v1'
@@ -751,6 +751,36 @@
     validate_precision2_completion(2,2)
     reject(lambda:validate_precision2_completion(1,2))
     reject(lambda:validate_direct_completion(0,1))
+    # Positive wiring regression: the complete 12-key canary is checked
+    # against the distinct five-key base receipt passed as the final argument.
+    positive_rows = [{'seed': 1, 'nnz': 0,
+                      'canonical_sparse_row_sha256': 'a' * 64}]
+    positive_base = {
+        'reached_seeds': [1], 'base_rows': positive_rows,
+        'completed_count': 1,
+        'rolling_sha256': rolling_base_rows(positive_rows), 'eof': True,
+    }
+    positive_atoms = {
+        letter: tuple([('E3', b'e3')] * 6 + [('E4', b'e4')] * 5)
+        for letter in ATOM_LETTERS
+    }
+    positive_full = dict(positive_base)
+    positive_full.update({
+        'schema': DIRECT_CANARY_SCHEMA, 'label': DIRECT_REPLAY_LABEL,
+        'atom_signatures': [
+            {'letter': letter,
+             'signature': public_typed_signature(positive_atoms[letter])}
+            for letter in ATOM_LETTERS],
+        'inverse_equalities': [], 'order_anchor': {}, 'prefix_table': {},
+        'generic_direct_scope':
+            '31-context joint direct_column at empty path per reached seed; '
+            'all-path propagation by conjugacy',
+    })
+    if set(positive_full) == set(positive_base):
+        fail('fixture_positive_receipt_not_distinct')
+    validate_direct_canary(positive_full, [1], positive_atoms, None,
+                           {}, {}, [], positive_base)
+    positive_direct_canary = 1
     factors=[[1],[2],[3],[4],[5]]; correct_pentagon=pentagon_factor_word(factors,cinv,lambda *rows:list(cpp(rows)))
     reversed_factor=[list(row) for row in factors]; reversed_factor[1]=list(cinv(reversed_factor[1])); reversed_pentagon=pentagon_factor_word(reversed_factor,cinv,lambda *rows:list(cpp(rows)))
     reject(lambda:pentagon_factor_gate(reversed_pentagon,factors,cinv,lambda *rows:list(cpp(rows))))
@@ -766,7 +796,8 @@
     roundtrip_blobs={'target_dense':target,'lower_dense':lower.tobytes(),'rho2_dense':bad_top.tobytes(),'rho2_packed':bad_packed}
     reject(lambda:dense_result_gate(roundtrip_blobs,target,lower,bad_top,bad_packed,module))
     return {'count':len(cases),'base_canary_direct_calls':len(calls),
-            'base_canary_completion':base['completed_count']}
+            'base_canary_completion':base['completed_count'],
+            'positive_direct_canary':positive_direct_canary}
 def validate_payload(payload,task601,roots,leaves):
     started=time.monotonic()
     raw=(payload/'manifest.json').read_bytes(); manifest=json.loads(raw)
@@ -845,7 +876,7 @@
         'generic_direct_scope':'31-context joint direct_column at empty path per reached seed; all-path propagation by conjugacy'})
     validate_direct_canary(manifest.get('direct_canary'),reached,
                            atom_signatures,model,prefix_table,order_anchor,
-                           inverse_equalities,direct_canary)
+                           inverse_equalities,base_receipt)
     print('A0_PROGRESS side=checker phase=endpoint_reached_seed_base_canary_complete S='+str(base_receipt['completed_count']),flush=True)
     bucket_terms=[[seed,list(path),coefficient] for (seed,_signature),(coefficient,path) in buckets.items()]
     print('A0_PROGRESS side=checker phase=endpoint_precision2_aggregation_start G='+str(len(bucket_terms)),flush=True)
@@ -891,7 +922,7 @@
     try: parse_literal_leaves(good,'33'*32)
     except RuntimeError: mutations+=1
     else: fail('fixture_ancestry_binding_mutation')
-    print(json.dumps({'fixture':'PASS','actor_multiplication':'PASS','inverse_action':'PASS','coefficient_2':'PASS','occurrence_components':11,'endpoint_ceiling':484,'rho2_bytes':PACKED,'mutation_count':mutations,'direct_schedule':'S','direct_replay_label':DIRECT_REPLAY_LABEL,'actor_atom_generic_evaluations':4,'full_prefix_generic_comparisons':0,'base_canary_direct_calls':fixture_counts['base_canary_direct_calls'],'base_canary_completion':fixture_counts['base_canary_completion'],'E4_split_buckets':2,'precision2_schedule':'G'},sort_keys=True))
+    print(json.dumps({'fixture':'PASS','actor_multiplication':'PASS','inverse_action':'PASS','coefficient_2':'PASS','occurrence_components':11,'endpoint_ceiling':484,'rho2_bytes':PACKED,'mutation_count':mutations,'direct_schedule':'S','direct_replay_label':DIRECT_REPLAY_LABEL,'actor_atom_generic_evaluations':4,'full_prefix_generic_comparisons':0,'base_canary_direct_calls':fixture_counts['base_canary_direct_calls'],'base_canary_completion':fixture_counts['base_canary_completion'],'positive_direct_canary':fixture_counts['positive_direct_canary'],'E4_split_buckets':2,'precision2_schedule':'G'},sort_keys=True))
 """Independent checker for Task565's grade-two module prebuild.
 
 This file does not import the producer.  It implements its own canonical
@@ -1886,7 +1917,7 @@
         authenticate_paper_pins(); auth_source_state(a.state); _manifest,_loaded,_roots,_leaves=auth_task601(a.task601); auth_candidate(a.candidate,_roots); manifest,_blobs=validate_payload(a.payload,a.task601,_roots,_leaves)
         if manifest.get('source_ancestry_sha256') != EXPECTED_FILES['source_ancestry'][2] or manifest.get('roots_sha256') != sha(_loaded['roots']): fail('consumer_parent_receipt_sha')
         if manifest.get('dimensions') != {'lower':LOWER,'top':TOP,'packed_rho2':PACKED}: fail('consumer_dimensions')
-        verdict={'schema':'d972.r07.a0.fresh-precision2-endpoint-signature.v7.checker','marker':MARKER,'payload_manifest_sha256':sha((a.payload/'manifest.json').read_bytes()),'rho2_sha256':sha(_blobs['rho2_packed']),'lower_coordinates_checked':LOWER,'top_coordinates_checked':TOP,'cross_checked':False,'verified':False}
+        verdict={'schema':'d972.r07.a0.fresh-precision2-endpoint-signature.v8.checker','marker':MARKER,'payload_manifest_sha256':sha((a.payload/'manifest.json').read_bytes()),'rho2_sha256':sha(_blobs['rho2_packed']),'lower_coordinates_checked':LOWER,'top_coordinates_checked':TOP,'cross_checked':False,'verified':False}
         a.out.write_bytes(canon(verdict)); print(MARKER); return 0
     except Exception as exc:
         error=str(exc); status='UNKNOWN_RESOURCE' if error.startswith('UNKNOWN_RESOURCE:') else 'NOT_READY'
```

AST 比較では top-level definition/class 147 個の名前・順序は一致し、body が
変わったものは厳密に `fixture_rejects`, `validate_payload`, `selftest`, `main`
だけだった。`validate_direct_canary` call は v7 の production 一個
(`direct_canary`) から、v8 の bounded positive 一個 (`positive_base`) と
production 一個 (`base_receipt`) になった。算術関数・owner class・source pin
には差分がない。

`validate_direct_canary` は full object の exact twelve-key shape/header を検査し、
そこから five-key base を再構成して `validate_base_receipt` を通した後、最終引数
との exact equality、四 atom、inverse、order、prefix の各 equality を順に検査する。
Positive fixture の objects は identity も key set も異なる。追加の hostile local
call では distinct pair が受理され、`positive_full` 自身を最終引数にも渡した場合は
厳密に次を得た。

```text
DISTINCT_BASE_ACCEPTED
SAME_OBJECT_REJECTED=checker_canary_base_rows
```

したがって「同じ object を full/base 両役に使って偶然通る」経路はない。

## 3. Exact workflow v15 -> v16 diff

機械的 unified diff は 8 hunks、13 additions、13 deletions で、全体は次のとおり。

```diff
--- .github/workflows/d972-r07-a0-fresh-precision2-endpoint-v15.yml
+++ .github/workflows/d972-r07-a0-fresh-precision2-endpoint-v16.yml
@@ -1,10 +1,10 @@
-name: d972-r07-a0-fresh-precision2-endpoint-v15
+name: d972-r07-a0-fresh-precision2-endpoint-v16
 on:
   workflow_dispatch:
   push:
     branches: [sol/r07-explicit-lift-20260825]
     paths:
-      - .github/workflows/d972-r07-a0-fresh-precision2-endpoint-v15.yml
+      - .github/workflows/d972-r07-a0-fresh-precision2-endpoint-v16.yml
 permissions:
   contents: read
   actions: read
@@ -29,9 +29,9 @@
   TASK625_WORKFLOW: "d972-r07-a0-grade1-selected-slp-staged-v3"
   SOURCE_RUN: "33677346616"
   PRODUCER_SHA256: "1422bec44e1367c0ea22043cb7b5e844ba8e7df69e3da763bd08e372d5dc8046"
-  CHECKER_SHA256: "0599759e2c2311e771439cf7bce10fd3fb0ce99f498e60a62827aa12a1a460c4"
+  CHECKER_SHA256: "1e8e82191bb8d82189a194010228ed180ebc0607732a6bb338ab13abf16d86fc"
   PRODUCER_MARKER: "R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CANDIDATE"
-  CHECKER_MARKER: "R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V7_CHECKER_PASS"
+  CHECKER_MARKER: "R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V8_CHECKER_PASS"
   V512_BYTES: "6151"
   V512_SHA256: "33997289c63c66392849ebdc81f4668172272f72057d54e383e50523059b2011"
   TASK789_AUDIT_BYTES: "16116"
@@ -50,7 +50,7 @@
   TASK737_AUDIT_SHA256: "13e6d021c197cec3ca0213ab0f57fe711b982ecc11a4e9d3ca54984d3bd8cb49"
 jobs:
   fresh-endpoint:
-    if: ${{ github.event_name == 'workflow_dispatch' || contains(github.event.head_commit.message, '[fire-fresh-precision2-endpoint-v15]') }}
+    if: ${{ github.event_name == 'workflow_dispatch' || contains(github.event.head_commit.message, '[fire-fresh-precision2-endpoint-v16]') }}
     runs-on: ubuntu-24.04
     timeout-minutes: 120
     steps:
@@ -63,14 +63,14 @@
         uses: actions/setup-python@8d9ed9ac5c53483de85588cdf95a591a75ab9f55
         with:
           python-version: "3.13"
-      - name: Authenticate v15 and pinned arithmetic source
+      - name: Authenticate v16 and pinned arithmetic source
         shell: bash
         run: |
           set -euo pipefail
           test "$(stat -c '%s' search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py)" = "70945"
           test "$(sha256sum search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py | awk '{print $1}')" = "$PRODUCER_SHA256"
-          test "$(stat -c '%s' search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v7.py)" = "109876"
-          test "$(sha256sum search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v7.py | awk '{print $1}')" = "$CHECKER_SHA256"
+          test "$(stat -c '%s' search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v8.py)" = "111387"
+          test "$(sha256sum search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v8.py | awk '{print $1}')" = "$CHECKER_SHA256"
           test "$(stat -c '%s' sol/proof_r07_all_path_direct_canary_induction_repair_v512.md)" = "$V512_BYTES"
           test "$(sha256sum sol/proof_r07_all_path_direct_canary_induction_repair_v512.md | awk '{print $1}')" = "$V512_SHA256"
           test "$(stat -c '%s' sol/sol_reply_789_audit_r07_all_path_direct_canary_induction_v509.md)" = "$TASK789_AUDIT_BYTES"
@@ -101,9 +101,9 @@
         run: |
           set -euo pipefail
           python -m pip install --disable-pip-version-check --no-cache-dir "numpy==2.5.1"
-          python -B -m py_compile search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v7.py
+          python -B -m py_compile search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v8.py
           python -B search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py --selftest
-          python -B search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v7.py --selftest
+          python -B search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v8.py --selftest
       - name: Authenticate exact accepted Task625 run
         shell: bash
         env:
@@ -173,7 +173,7 @@
             --task601 "$RUNNER_TEMP/task625/task625-payload" --out "$RUNNER_TEMP/task640-payload" \
             2>&1 | tee "$RUNNER_TEMP/task640-logs/producer.log"
           grep -Fq "$PRODUCER_MARKER" "$RUNNER_TEMP/task640-payload/manifest.json"
-          timeout --signal=TERM --kill-after=60s 45m python -B -u search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v7.py \
+          timeout --signal=TERM --kill-after=60s 45m python -B -u search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v8.py \
             --state "$RUNNER_TEMP/task554-state" --candidate "$RUNNER_TEMP/task595-candidate" \
             --task601 "$RUNNER_TEMP/task625/task625-payload" --payload "$RUNNER_TEMP/task640-payload" \
             --out "$RUNNER_TEMP/task640-verdict.json" 2>&1 | tee "$RUNNER_TEMP/task640-logs/checker.log"
@@ -182,7 +182,7 @@
         if: ${{ success() }}
         uses: actions/upload-artifact@65462800fd760344b1a7b4382951275a0abb4808
         with:
-          name: task640-fresh-rho2-v15-${{ github.run_id }}-${{ github.run_attempt }}
+          name: task640-fresh-rho2-v16-${{ github.run_id }}-${{ github.run_attempt }}
           path: |
             ${{ runner.temp }}/task640-payload/
             ${{ runner.temp }}/task640-verdict.json
@@ -192,7 +192,7 @@
         if: ${{ always() }}
         uses: actions/upload-artifact@65462800fd760344b1a7b4382951275a0abb4808
         with:
-          name: task640-fresh-rho2-v15-logs-${{ github.run_id }}-${{ github.run_attempt }}
+          name: task640-fresh-rho2-v16-logs-${{ github.run_id }}-${{ github.run_attempt }}
           path: ${{ runner.temp }}/task640-logs/
           if-no-files-found: warn
           retention-days: 90
```

これは Luna の報告どおりの機械的 successor である。Producer path/SHA、全 parent
pins、limits、permissions、実行順序は不変であり、checker の path/bytes/SHA/marker
だけを v8 に合わせている。

## 4. Bounded checks と mutation/completion coverage

Repository 外の pycache を使った `py_compile`、producer v9 `--selftest`、checker
v8 `--selftest` はすべて exit 0。主要 receipt は次のとおり。

```text
producer: fixture=PASS
producer: direct_schedule=S
producer: actor_atom_generic_evaluations=4
producer: full_prefix_generic_comparisons=0
producer: build_heavy_trap_called=false
producer: generic_builders_called=false

checker: fixture=PASS
checker: positive_direct_canary=1
checker: base_canary_direct_calls=2
checker: base_canary_completion=2
checker: mutation_count=55
checker: direct_schedule=S
checker: precision2_schedule=G
checker: actor_atom_generic_evaluations=4
checker: full_prefix_generic_comparisons=0
```

55 件は単なる固定値ではなく、各 `reject(...)` が `RuntimeError` を捕捉した件数に、
leaf EOF/extra/header/ancestry-binding の四拒否を加えた実行結果である。Task795 が
要求した base-row digest、completion count、EOF、slot sign/prefix/type、
`parent*atom` reversal/type、bucket representative/first-six-only、pentagon order、
dense receipt、claim flag 等の既存変異は維持された。特に
`validate_precision2_completion(1,2)` と `validate_direct_completion(0,1)` は拒否され、
同じ predicate が production の `21,286/21,287` 未完了を fail-close する。

さらに Task795 の release-critical mutation を v8 validator に個別投入した bounded
再現結果は次のとおりで、全件が指定された最初の gate で拒否された。

| mutation | exact rejection |
|---|---|
| missing reached seed | `checker_base_canary_eof` |
| duplicate reached seed | `checker_base_canary_eof` |
| base-row digest mutation + rolling digest reseal | `checker_canary_base_rows` |
| atom bytes mutation | `checker_canary_atoms` |
| E4 slot -> E3 | `checker_canary_atoms` |
| `parent*atom` receipt -> reversed order | `checker_canary_order` |
| slot 10 sign `- -> +` | `checker_prefix_table_contract` |
| slot 10 prefix -> different bytes | `checker_prefix_table_contract` |
| EOF false | `checker_base_canary_eof` |
| missing EOF/key truncation | `checker_canary_shape` |
| pentagon factor order | `pentagon_factor_order` |
| aggregation `21,286/21,287` | `checker_precision2_aggregation_incomplete` |
| direct completion `22/23` | `checker_direct_bucket_incomplete` |

これらは tiny synthetic fixtures のみであり、production input、GHA、全 21,287
件の local replay は実行していない。Fixture の `PASS` は fresh rho2 や A0 の
結果ではない。

## 5. Correctness と performance/scope

Task795 が監査した producer receipt は 70,945 bytes / SHA-256
`1422bec44e1367c0ea22043cb7b5e844ba8e7df69e3da763bd08e372d5dc8046`
であり、現 v9 と完全一致する。したがって producer の arithmetic、owner/source、
target、schedule、caps、aggregation、flags は byte-level で不変である。Checker
側も上記 exact diff に列挙した箇所以外は同一で、独立実装のまま producer を
import しない。

Actual immutable parent の `L=21,608, U=13,043, G=21,287, S=23` と不変 pins
の下で、successful production path の静的 count は次のとおり。

| side | generic `direct_column((), relator)` | four typed atoms | other typed `coordinates` | precision-two aggregate actions |
|---|---:|---:|---:|---:|
| producer | 23 | 4 | reached endpoints 23 + order anchor 1 | 21,287 |
| independent checker | 23 | 4 | reached endpoints 23 + order anchor 1 + the 23 internal direct-column endpoint evaluations | 21,287 |

両側とも production から `replay_reached_seed_base` を一度だけ呼び、その内部で
sorted reached seeds を一周して一 seed 一 generic call と completion gate を行う。
`G` loop 内に `direct_column` はない。Producer は `for ... in buckets.items()` の
全 action を数え `aggregation_done == aggregation_total` を要求し、checker は
全 `bucket_terms` を `independent_replay` が一周した後
`validate_precision2_completion(aggregation_done, len(bucket_terms))` を要求する。
v8 の修理により honest checker はこの loop に到達できる。

新しい positive fixture は `--selftest` branch のみにあり、workflow でも
`Run bounded serial fixtures` という別 step で明示実行される。Production step
の producer/checker command に `--selftest` はない。Runtime profile の
`generic_joint_closure`, `generic_roster`, `base_fox_rows`, `pb3_boundary_rows`,
`pb4_boundary_rows`, `generic_target`, `generic_runtime_model` はすべて `False` の
まま、light owner、exact prefix trie と sparse bucket replay を使う。Dense closure、
full-history copy、G-size generic replay、二重 base replay、その他新規の
slow/memory-heavy path は認められない。

## 6. Workflow authentication と release envelope

v16 authentication step にある repository-local SHA checks は 19/19、明示 byte
checks は 8/8 が現 bytes と一致した。主要な exact parent pins は次のとおり。

| item | exact pin |
|---|---|
| Task625 run | run `33734643746`, attempt `1`, head `b401d724bbdbef8cf67e96def22fc51c014ab546`, workflow `d972-r07-a0-grade1-selected-slp-staged-v3` |
| Task625 job | id `100582244001`, name `selected-slp`, conclusion `success` |
| Task625 artifact | id `9885925239`, name `task625-grade1-selected-slp-staged-v3-33734643746-1`, 50,793,121 bytes, digest `sha256:ac3121f3bc1a7e2a6c267f20352e953b7343f9085015dd74e4a67e4b90129a75`, not expired, matching run/head |
| Task625 verdict | 1,120 bytes, SHA-256 `a650aa8d5d78f52145fff5ba7769ad2036cfd16e90e3caaf367b4517e07d2740`, marker `R07_GRADE1_SELECTED_SLP_V2_CHECKER_PASS` |
| Task554 source | run `33677346616`, attempt `1` |
| Task595 candidate | run `33707397894`, attempt `1` |
| Task601 producer/checker | `ce036c4a1a92d16a78cb8da8c16dee282a6a981889f821e6df82eaecdd8fba0a` / `8c3dd039368f63d62ef79694a196f73d0b626134df39673c5e48c98c7c8787f9` |
| decision/body/head | `62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d` / `07de7a817e8c5ae2e7346402a290c32631d05b0cc621d03702faa6cb43a948c0` |
| basis/remainder/prepare | `b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d` / `564cbfafc869a8c6eb761a392caa5e792b546bf577af7fe808177b2fdf13cbb0` / `1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865` |

Workflow は top-level job `fresh-endpoint` 一個だけで、producer の完了後に checker
を直列実行する。Job timeout は 120 分、両 production process はそれぞれ
`timeout --signal=TERM --kill-after=60s 45m`、virtual-memory ulimit は 8 GiB、
内部 RSS cap は 7 GiB である。全 7 `uses:` は 40-hex commit SHA に固定される。
Result artifact は checker marker grep を含む全先行 step 成功時だけ
`${{ success() }}` で upload され、logs は `${{ always() }}` で upload される。
外部 artifact の現存性・metadata は dispatch 後に API gate が再確認して
fail-close する。本 audit はその API/GHA を実行したという主張ではない。

```text
VERDICT=PASS_A0_CANARY_WIRING_V16
SAFE_TO_DISPATCH_GHA=yes
ACTUAL_GENERIC_DIRECT_CALLS_PRODUCER=23
ACTUAL_GENERIC_DIRECT_CALLS_CHECKER=23
ACTUAL_GENERIC_DIRECT_CALLS_COMBINED=46
FOUR_TYPED_ATOM_EVALUATIONS_PER_SIDE=4
FULL_PRECISION2_BUCKETS_PRODUCER=21287
FULL_PRECISION2_BUCKETS_CHECKER=21287
ALL_21287_AGGREGATION_BUCKETS_REMAIN=yes
UNNECESSARY_GENERIC_21287_OR_MEMORY_HEAVY_PATH_REMAINS=no
FRESH_RHO2=NOT_CLAIMED
A0=NOT_CLAIMED
COMMON=NOT_CLAIMED
FAKE=NOT_CLAIMED
IHARA=NOT_CLAIMED
verified=false
```
