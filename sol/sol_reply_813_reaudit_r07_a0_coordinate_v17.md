# Sol(max) Task813 — hostile release re-audit of A0 v17 coordinate repair

## 裁定概要

狭い再監査は合格である。v16 の到達 failure は、checker v8 の実
`IndependentAllSeven.specs` 11 record が `coordinate` を持たないまま、
fail-closed な `occurrence_prefix_contract` が最初の record の
`spec['coordinate']` を読んだことによる `KeyError('coordinate')` だった。
v9 は同じ実 constructor が必ず通る `build_actual_specs` 内で全 11 record に
`(0,1,2,3,0,4,5,6,7,8,9)` を束縛し、完全 tuple を `TEN` と照合する。
その field は `coordinates` と `occurrence_data` の双方が直接読む。late default、
missing-field 受理、label からの事後推定はない。

Producer は byte-level で凍結されたままであり、checker の算術、parent/source、
bucket、dimension、claim flag に拡張変更はない。v17 は producer と checker を
一回ずつ直列に保ち、producer marker 後の完全 payload を先に明示的な
`unchecked-candidate` artifact として確定させる。後続 checker の失敗はその完了済み
artifact を抑止せず、producer または producer-marker gate の失敗時には artifact
upload は実行されない。新しい数学的結果は本監査では主張しない。

## 1. 指定入力と凍結 evidence

Task813 §1 の九ファイルおよび retained v16 の `producer.log` / `checker.log` を、
先頭から末尾まで読んだ。retained log receipt は次のとおりである。

| file | bytes | LF | CR | SHA-256 |
|---|---:|---:|---:|---|
| `producer.log` | 7,173 | 83 | 0 | `ce1019b3a8e4f47ca07b33f406283916632b5ed628c6aba60b88d07b6ee33701` |
| `checker.log` | 49 | 1 | 0 | `1ed864644a4cd818ad893524948a384e20d7ef55876aaadd3bb9a55305c55e63` |

Producer log は `L=21608, U=13043, G=21287`、23/23 reached-seed base canary、
`endpoint_precision2_aggregation_complete elapsed_seconds=889` まで到達している。
Checker log の全内容は厳密に次である。

```text
{"error": "'coordinate'", "status": "NOT_READY"}
```

これは run/attempt `33836732706/1`、job `100910685815`、head
`f72d9173ce2b90b6ce8ad137d4d82ff7b059fe53` について Task808 と root receipt が
記録した failure と一致する。

## 2. 旧 failure の静的 call trace と実座標修理

旧 v8 の到達順は次である。

1. `validate_payload` が `build_checker_light` を呼ぶ。
2. `build_checker_light` が `IndependentAllSeven(runtime)` を構成する。
3. v8 `__init__` は hexagon 6 record と pentagon 5 record を `self.specs` に
   append するが、各 dict に `coordinate` key はない。
4. 直後の `occurrence_prefix_gate` は `block/base_factor/sign` のみを使うため通る。
   後続の reached endpoint と atom signature も、v8 `coordinates` 内の別の固定 tuple
   を zip していたため通る。
5. `validate_payload` の `prefix_table=occurrence_prefix_contract(model)` が最初の
   actual record で `spec['coordinate']` を読む。ここが最初の例外である。
6. `main` が `str(KeyError('coordinate')) == "'coordinate'"` を JSON 化し、retained
   checker log の `NOT_READY` になる。checker の base canary と 21,287 aggregation
   には到達していない。

v9 では `IndependentAllSeven.__init__` が actual `raw_specs` を
`build_actual_specs(self, raw_specs)` へ一度渡す。helper は長さ 11 を要求し、既存の
base substitution/factor 構成と同じ loop 内で `coordinate=TEN[ordinal-1]` を必須 key
として追加し、返却前に全 tuple が `TEN` と等しいことを要求する。その後にのみ
`occurrence_prefix_gate` と `occurrence_prefix` の付加が行われる。

静的追跡に加えて、production producer/checker replay を行わず、実
`SevenSources -> build_checker_light -> IndependentAllSeven` constructor だけを通す
bounded call を行った。actual record の全配置は次のとおり一致した。

| ordinal | label | block | sign | coordinate |
|---:|---|---:|---:|---:|
| 1 | `H1_fxy` | 1 | 1 | 0 |
| 2 | `H1_fxz` | 1 | -1 | 1 |
| 3 | `H1_fyz` | 1 | 1 | 2 |
| 4 | `H2_fux` | 2 | -1 | 3 |
| 5 | `H2_fxy` | 2 | -1 | 0 |
| 6 | `H2_fuy` | 2 | 1 | 4 |
| 7 | `P_b1` | 3 | 1 | 5 |
| 8 | `P_b2` | 3 | 1 | 6 |
| 9 | `P_b3` | 3 | 1 | 7 |
| 10 | `P_b5_inverse` | 3 | -1 | 8 |
| 11 | `P_b4_inverse` | 3 | -1 | 9 |

したがって actual block/label/order/sign まで含む tuple は厳密に
`OCCURRENCE_LAYOUT`、coordinate tuple は厳密に `TEN` である。同じ actual model に
対して `occurrence_prefix_contract`、`coordinates(())`、`occurrence_data((), {})` を
通し、後二者がそれぞれ `spec['coordinate']` を読むことも確認した。ordinal 10 の
actual record copy を `8 -> 1` に変えた場合、最初の拒否は厳密に
`checker_prefix_layout` だった。

同梱 regression も手書き済み coordinate dict を直接 contract に渡す旧 fixture では
ない。production と同じ `build_actual_specs` を通してから
`occurrence_prefix_contract` を通し、正例を受理し、同じ ordinal 10 変異を exact reason
付きで拒否する。fixture の raw data は小さいが、load-bearing production helper を
迂回していない。

## 3. Producer/checker 差分境界と bounded checks

Producer v9 は厳密に 70,945 bytes / SHA-256
`1422bec44e1367c0ea22043cb7b5e844ba8e7df69e3da763bd08e372d5dc8046`
で、Task802 の凍結 receipt と一致する。

Checker v8 -> v9 の機械的 line-sequence 比較は 11 change blocks、66 additions、
22 deletionsだった。AST 比較では top-level definition/class は 149 -> 150、追加は
`build_actual_specs` 一個だけである。body が変わった既存 top-level 定義は
`fixture_rejects`、`selftest`、`IndependentAllSeven`、`main` のみだった。
`IndependentAllSeven` 内で変わった method は `__init__`、`coordinates`、
`occurrence_data` の三つだけで、`occurrence_column`、`direct_column`、pentagon、
word/arithmetic helpers は同一である。残る text change は checker marker と verdict
schema の v9 化および bounded receipt の一項追加だけである。

特に `validate_payload` の body は AST-level で同一であり、production
`validate_direct_canary(..., base_receipt)` は five-key `base_receipt` を最終引数へ渡す
v8 repair のままである。既存 55 mutations の削除はなく、coordinate mutation 一件を
加えた実行値は 56 である。

Repository 外の pycache prefix を用い、許可された checker v9 の `py_compile` と
`--selftest` のみを実行した。ともに exit 0 で、主要 receipt は次だった。

```text
fixture=PASS
mutation_count=56
actual_coordinate_mutation_rejections=1
positive_direct_canary=1
base_canary_direct_calls=2
base_canary_completion=2
actor_atom_generic_evaluations=4
full_prefix_generic_comparisons=0
```

上記 actual-constructor positive/mutation call も bounded であり、producer arithmetic、
production-size checker replay、GHA は実行していない。

## 4. v17 workflow の hostile audit

v16 -> v17 の全差分を照合した。version/path、checker bytes/SHA/marker、fire token、
artifact 名の正直な v17 化に加え、旧 combined production step を次の直列 step に分けた
ものだけである。

1. `Produce fresh rho2 candidate` が凍結 producer v9 を一回だけ実行する。
2. 同じ step 内で producer exit を `set -euo pipefail` と `timeout` で受け、
   `manifest.json` の固定 `PRODUCER_MARKER` を照合する。
3. 成功時だけ `Upload unchecked rho2 candidate` が
   `${{ runner.temp }}/task640-payload/` 全体を upload する。
4. その upload 完了後、`Independently check fresh rho2 candidate` が download/copy を
   挟まず、同一 local directory を checker v9 へ一回渡す。
5. checker exit と固定 `CHECKER_MARKER` の双方を通った場合だけ、payload と
   `task640-verdict.json` を accepted-side artifact に upload する。
6. logs step は `${{ always() }}` である。

Unchecked artifact 名は厳密に
`task640-fresh-rho2-v17-unchecked-candidate-${{ github.run_id }}-${{ github.run_attempt }}`。
内容指定は producer payload directory 一個だけで verdict を含まない。producer が
原子的に完成させる 7 receipt files と `manifest.json` を directory ごと含み、manifest
自身も candidate marker、`cross_checked:false`、`verified:false`、全 terminal claim
false を持つ。artifact 名にも内容にも accepted/cross-checked verdict はない。この名を
download または数学的結果として consume する step は存在しない。

Workflow は top-level job `fresh-endpoint` 一個のまま、parent は Task625
`33734643746/1`, job `100582244001`, head
`b401d724bbdbef8cf67e96def22fc51c014ab546`、Task554 source run
`33677346616`、Task595 candidate run `33707397894` のままである。source/proof pins、
permissions、job timeout 120 分、producer/checker 各 45 分 process cap、各 production
step の `ulimit -v 8388608`、7-GiB internal RSS cap、durable/path/trie/state/record caps、
claim flags、90-day retention は維持されている。

## 5. 追加 work と memory envelope

新しい production-side Python work は、既存 11-record constructor loop を helper に
移した上で各小 dict に一つの小整数 field を足し、11 要素 tuple equality を一回行う
ことだけである。constructor、`coordinates`、`occurrence_data` のいずれにも第二の
record collection、大きな copy、追加 group evaluation はない。

Successful production path の generic `direct_column((), relator)` は producer/checker
各 23 回、合計 46 回のまま。四 actor atom evaluation も各側 4 回のまま。precision-two
aggregation は producer/checker 各 21,287 actions のままで、`G` loop に generic
`direct_column` はない。checker の `validate_payload` と `independent_replay` は不変で
あり、v17 step split は producer/checker のどちらも再実行しない。

新規 workflow work は既に disk 上に完成した payload の upload 一回だけである。
checker 成功時には同じ payload が unchecked artifact と従来の accepted artifact に
それぞれ一回転送されるが、local payload directory は一個であり、二つの live Python
object へ複製するコードはない。checker failure 時の追加転送は unchecked artifact
一回だけである。新規 production fixture、23-call duplication、21,287 aggregation の
再走、dense closure、full-history、G-size generic replay はない。

## 6. Exact receipts、pins、failure ordering

| file | bytes | LF | CR | BOM | SHA-256 |
|---|---:|---:|---:|---|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py` | 70,945 | 1,272 | 0 | none | `1422bec44e1367c0ea22043cb7b5e844ba8e7df69e3da763bd08e372d5dc8046` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v9.py` | 113,012 | 1,969 | 0 | none | `7b2beb39dbdc65494f85fa4451ed69d99a22685d11f1d4fef6e671322d24098d` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v17.yml` | 13,818 | 213 | 0 | none | `94ff396ed41ff5a6231d5b2fbe79648da921c02f809199542a7195080c7d5c75` |

Workflow 内の repository-local SHA checks は 19/19、明示 byte checks は 8/8 が現物と
一致した。全 8 `uses:` は 40-hex commit SHA 固定で、新しい unchecked upload も既存
upload と同じ固定 `actions/upload-artifact` SHA を使う。主要な release pins は次である。

```text
workflow path  .github/workflows/d972-r07-a0-fresh-precision2-endpoint-v17.yml
producer path  search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py
checker path   search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v9.py
producer mark  R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CANDIDATE
checker mark   R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CHECKER_PASS
fire token     [fire-fresh-precision2-endpoint-v17]
unchecked      task640-fresh-rho2-v17-unchecked-candidate-${{ github.run_id }}-${{ github.run_attempt }}
accepted       task640-fresh-rho2-v17-${{ github.run_id }}-${{ github.run_attempt }}
logs           task640-fresh-rho2-v17-logs-${{ github.run_id }}-${{ github.run_attempt }}
```

Control-flow 上、producer process または producer marker grep が失敗すれば producer
step は failure となり、直後の `${{ success() }}` unchecked upload は skip される。
逆にその upload step が完了した後の checker failure は、既に確定した artifact を
遡って削除・抑止しない。Accepted upload は checker process と checker marker grep
の後にある `${{ success() }}` のため実行されず、logs upload だけは常に試行される。

## 7. Terminal

```text
VERDICT=PASS_A0_COORDINATE_V17
SAFE_TO_DISPATCH_GHA=yes
FRESH_RHO2/A0/COMMON/COMPATIBLE_LIFT/FAKE/IHARA=NOT_CLAIMED
verified=false
```
