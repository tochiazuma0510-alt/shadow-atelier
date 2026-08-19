# Luna reply 157ea — explicit T-53 strong-word inertness certificate v1

## 結論

更新後の正本 task
`sol/luna_task_157ea_b345_strong_wform_inertness.md`
（SHA-256
`1b403d5f545cf11b2ab397c1bc9c4e1a57f29207e2e3dee423f42e60b81f0665`、
14,464 bytes）を全文再読し、指定された4ファイルだけで single-word
diagnostic lane を実装した。

この便は、明示語

```text
s = y^-18 x^-18 y^18 x^18
```

について、5本の coface の `Phi_3(H4)` membership と、target 6 の
`D(r_s)-D(r_0)` membership の計6問だけを、fresh v7 prefix に対して判定する。
4096 dictionary、onto/inverse、PB5、ANUPQ、A5 layer は構築しない。

## Frozen files

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_b345_strong_wform_inertness_v1.py` | 51,391 | `d41123a8c4803f6ac67387ac9bbf1a32f797b90d6233605a5511713f215244be` |
| `search/check_d972_b345_strong_wform_inertness_v1.py` | 38,531 | `a8345c6c27fea24147dc7c310bbda48ea5bc08b7a0a720ded961af13a5b961e8` |
| `search/d972_b345_strong_wform_inertness_gha_driver_v1.g` | 10,322 | `54bc3f0132adf8b3b5b112721d3c790009c8a48e9aac8bb11860e5a85db69b18` |

driver は上記 producer/checker SHA と、task に指定された q3
producer/checker/driver および q3 artifact SHA を hard-pin する。placeholder は
0件である。この reply 自身の SHA/bytes は自己参照を避け、外側の完了報告で固定する。

## 実装した exact contract

1. `f0`、`xi=x^18`、`eta=y^18`、
   `s=[eta,xi]=eta^-1 xi^-1 eta xi`、`fs=f0*s` を signed F2 word として再構成する。
   literal word、長さ `20/72/92`、指定 digest、自由簡約、指数和 `(0,0)` をすべて
   hard gate にした。
2. F2 の埋込みは全経路で `x -> PB3 gen1=A12`,
   `y -> PB3 gen3=A23` に固定した。PB3 gen2=A13 を y とする mutation は checker が
   reject する。`xi,eta,s` の E3 identity と、5 coface 後の E4 identity は digest
   ではなく実 element equality で再生する。
3. PB4 presentation、11 relators、left Fox convention を fresh に再構成し、
   32768 BFS translations の後に v7 の32 directed roundsを再生する。
   stable rounds projection、translations、columns、blocker history の4 SHA、
   `32975` translation blocks、`362725` columns、`362709` pivots、
   `16` dependent columns、および candidate-1 target-6 blocker
   `0cd653ee...e00903` を hard gate にした。旧 receipt/basis/pool/proof は入力にしない。
4. ordered targets は `d_0(s),...,d_4(s),delta` の6本だけである。
   `r0` と `rs` を同一の literal target-6 formula/coface/orientation から別々に構成し、
   `delta=rs*r0^-1`、`E4(r0)=E4(rs)=E4(delta)=1`、
   `D(delta)=D(rs)-D(r0)` を直接照合する。
5. 各 target は provenance-free reduction を先に行い、zero の場合だけ同じ target を
   provenance 付きで再生成・再 solve する。positive bit は packed proof serialization と
   root equality が完了した後にだけ立つ。ResourceStop 中の未評価/仮 positive は `null`
   として false と区別する。6問は同じ immutable basis を共有し、basis を6回再構築しない。
6. positive proof は base-relator index、左 translation の canonical E4 bytes、section
   word、F3 coefficient、backward-only packed DAG、root/array SHA を lossless に持つ。
   checker は新 producer を import せず、各 translated relator column と packed proof root
   を frozen checker-side machinery から独立再生する。
7. terminal は次の4種だけである。

```text
B345_T53_STRONG_S_EXACT_TYPED_INERT
B345_T53_STRONG_S_PREFIX_INCOMPLETE
B345_T53_STRONG_S_UNKNOWN_RESOURCE
B345_T53_STRONG_S_UNKNOWN_INPUT
```

`PREFIX_INCOMPLETE` の zero bit は registered prefix で未証明という意味だけで、
nonmembership には変換しない。RESOURCE/INPUT を含む全 nonpositive terminal は
`unknown_not_obstruction` と exact single-word scope を保持する。

## Freeze STOP repair

最初の freeze 後の hostile audit で見つかった RESOURCE receipt の2点を、通常完走・
positive predicateを変えず修理した。

1. `classify_results(..., complete=False)` は `len(results)<=6` を hard gate し、
   evaluated prefix の typed bit の後ろを `null` で埋め、常に長さ6の
   `membership_bits` を返す。空 prefix は `[null,null,null,null,null,null]`、一般 prefix
   も recorded rows と null suffix の exact concatenationである。producer/checker と
   RESOURCE selftest を同じ契約へ揃えた。
2. wall/RSS 以外の structural `ResourceStop` は monitor 自身が `hit_reason` を設定しない。
   catch時に未設定なら例外の exact reason を束縛し、既設定の soft wall/RSS reason なら
   例外 reasonとの一致を hard gateする。これにより top-level `reason` と
   `resource_guards.hit_reason` は全 ResourceStop で一致する。

## Independent checker と mutation gates

checker は q3 SHA/schema/formula、E3/E4、cofaces、PB4/Fox、fresh prefix、6 gradients、
blockers、proof DAG、terminal/claim keysets を独立に構成する。少なくとも次の drift を
fail closed にするコードを入れた。

- wrong `y -> PB3 gen2`、commutator orientation、exponent、coface order
- target-6 formula/coface、negative-letter Fox order、delta product order、subtraction sign
- quotient identity、missing-pivot component/value、stable-prefix hash
- proof coefficient/leaf/section/root/typed payload と positive-without-complete-proof
- missing bit の negative relabel、claim leakage booleans

checker が利用する frozen v7 proof validator の terminal set は selftest の間だけ
4-token v7 fixture に差し替え、`try/finally` で必ず元の v10 terminal set に復元する。
production entry ではこの fixture injection は到達不能である。

## Combined lightweight selftest

最初の許可 run では新 producer selftest は PASS し、新 checker は共有している frozen
v7 selftest の terminal fixture set だけで停止した。これは新 production predicate の失敗では
なく、v10 module 上で v7 fixture を単独起動した際の fixture-only terminal drift だった。

最初に明示許可された corrective run は上記 `try/finally` 修理後に PASS した。その後の
freeze STOP は fixed-width RESOURCE ledger と structural resource reason の receipt-only
不整合だった。両修理後に追加で明示許可された corrective combined selftest を exactly
once 実行し、PASSした。以後の Python/GAP 実行はしていない。最終 marker は次のとおり。

```text
D972_B345_T53_STRONG_S_PRODUCER_SELFTEST_PASS six_positive=1 partial=1 resource=1 input=1 wrong_y=1 resource_reason=1
D972_B345_RELFRAT3_PIVOT_SURGERY_V7_CHECKER_SELFTEST_PASS left_orientation=1 wrong_orientations=3 dedup=1 rollback=1 smaller_pivot_incomplete=1 sparse_oracle=1 terminals=4 acceptance=33 diagnostics=17 expression_mutation=1 source_anchors=6 probe_rollback=1
B345_T53_STRONG_S_INERTNESS_CHECKER_SELFTEST_PASS shared_terminal_core=4 wrong_y=1 word_mutations=6 fox=2 gradient=1 blocker=2 prefix=1 proof_core=v7 claim_mutations=6
```

selftest は production q3、full 32768+207 prefix、GAP を実行していない。

## Static/transport audit

- producer/checker の task SHA は更新後の `1b403d...f0665` で一致する。
- q3 3 source SHA、q3 artifact SHA、v7 producer/checker、v9 producer、v10 checker/driver
  の frozen pins を再走査した。
- driver の producer/checker pins は上表の最終 SHA と一致し、placeholder は0件である。
- driver は ASCII-only、same-job q3 child は1回、q3 checker PASS marker はexactly one、
  producer/checker は `python3 -u` + `bash -o pipefail` + live `tee` である。
- output/log/sentinel を開始前に固定パスで削除し、4 terminal の exactly-one gate、checker
  PASS の exactly-one gate、artifact SHA 出力を持つ。
- 300-minute producer soft deadline、4.5-GiB RSS guard、330-minute job contract を保持した。
- local production GAP、full producer/checker、GHA、Git、workflow edit は行っていない。

## Claim boundary

まだ production run は行っていないため、6本の actual membership bit について結果を主張しない。
将来 `EXACT_TYPED_INERT` が cross-check されても、それが述べるのはこの一つの `s` が5本の
coface preimage に入り、二つの明示 target-6 residual がこの fixed quotientで同じ class を持つ
ことだけである。W-FORM universality、full H3 coverage、nonmembership、finite obstruction、
B4-A、B4-B、cofinality/uniform iteration は一切主張しない。

B345_T53_STRONG_S_INERTNESS_V1_READY_FOR_GHA
