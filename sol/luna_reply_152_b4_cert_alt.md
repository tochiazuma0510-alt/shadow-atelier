# B4 local norm の別 certificate lane（v1）

## 判定

現時点の global B4-B の決着は `UNKNOWN` のままです。KBMAG の `ReducedForm` と
`roof_bits` は、rewrite rule が元の 158 relator から導かれたことを記録
しないため、それだけでは B4-B の証明にも B4-A の証明にもなりません。
今回、unlogged normal form を「目標語」として利用しつつ、最終的には元の
F6/158-relator presentation で独立再生するための versioned checker を追加
しました。なお、bundle が将来通っても、それは固定した
`U=F6/<158 relators>` における972本の local norm identity に限られます。
PB4 の typed refinement/survival/cofinality bridge を含む global B4-B terminal
ではありません。GHA で proof bundleもまだ生成されていないので、local
terminalすら宣言していません。

変更ファイルは次の2つだけです。

- `crosscheck/check_d972_b4_kbmag_vankampen_extract_v1.py`
- `sol/luna_reply_152_b4_cert_alt.md`

親側の commit/push/dispatch、workflow、ローカル GAP/KBMAG は実行していません。

## 既存資産の棚卸し

| 資産 | 役割 | この別経路での扱い |
|---|---|---|
| `search/check_d972_b4_rewrite_cert_v1.py:2-24,205-308` | `cancel`、元 relator の cyclic conjugate の `delete/insert`、各 step の `after` を再計算する直接 checker | primitive proof の意味論の正本。cert が無いと UNKNOWN のままなので、新 checker に同じ操作を producer 非共有で再実装した |
| `search/d972_b4_norm_van_kampen_v1.py:2-9,116-214` | GAP/KBMAG に依存しない Dehn-style trace producer | 直接証明の資産。486 unique の候補に留まり、unlogged KBMAG rule の provenance は補わない |
| `search/d972_b4_norm_tietze_trace_v2.py:2-15,273-378` | raw RS 161 generators/5056 relators、明示的 Tietze、dense relabel | dense KBMAG 入力を作る前段。単独では proof ではない |
| `crosscheck/check_d972_b4_norm_tietze_dense_v1.py:2-17,475-638` | v2 trace と map、final relators/norms を独立再生 | `terminal_claim` は `NONE; KBMAG/AutomaticStructure replay still required`。今回の checker はこの final norm を F6 に戻した後の proof bundleを受ける |
| `search/d972_b4_norm_tietze_kbmag_consumer_v2.g:118-213` | dense presentation を KBMAG に渡し、972 `ReducedForm` を読む | `:184-213` は bits と candidate status のみ。rule/van Kampen traceを出さないため、今回の checkerへの入力としては不十分 |
| `search/d972_b4_kbmag_v2.g:144-208` | raw KBMAG lane | `:168` の `ReducedForm` と `:193-206` の `roof_bits` だけで、`:208` に `QUIT`。Read-safeな証明出力ではない |
| `search/check_d972_b4_kbmag_v2.py:131-218` | 972 norm/receipt の独立 input gate | `:201-203` の `global_b_status=UNKNOWN`。KBMAG の非算術性や rule provenanceを証明しない |

v2 Tietze の basis pin は以下です（別 lane と同じ canonical input に固定する）。

- raw RS: 161 generators / 5056 relators
- `RS_WORDS_SHA256 = 29c65a6cf9d0308e25ca462c752d7b540a6856e7d99d5d1d016919240b575c0e`
- `NORM_RS_SHA256 = f7134e15e92c80a5ceeede38e94314539815a665ba7d279443208de1696041f8`
- original relators: `12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e`
- normalized 972 rows: `283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930`
- F6 roof norms: `ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e`
- canonical word artifact raw bytes: `564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9`

## 実装した bundle 契約

新 checker の schema は `d972-b4-kbmag-vankampen-bundle/v1` です。producer は
次の3層を一つの artifact に固定して渡します。

1. `normal_form_source`

   - `normal_form_basis: "F6"`
   - 972 個の signed F6 `normal_forms`
   - `normal_forms_sha256` と `all_empty`
   - KBMAG receipt の `artifact_sha256` と `kbmag_status`

   `normal_forms` は KBMAG の output を F6 basis に戻した目標語です。checker
   は source digest、972 行、`all_empty` の整合性を再計算し、端末候補として
   は現行 consumer の `ALL_972_EMPTY_CANDIDATE_NEEDS_REPLAY` だけを受けます。
   出力 receipt は source artifact SHA と bundle raw-byte SHA も記録します。

2. `rules`

   各 rule は `id`, `lhs`, `rhs`, `proof_steps` を持ちます。`lhs`/`rhs` は
   元の6-generator basisで、`proof_steps` は各 step の完全な `after` を含む
   次の primitive だけです。

   - `cancel`: 隣接する逆元対を削除
   - `delete_relator`: 158 relator の cyclic conjugate（または inverse）が
     現在位置に一致することを検査して削除
   - `insert_relator`: 同じ token を挿入

   全 step の word を checker 自身が free-reduce して `after` と比較し、
   `lhs` から `rhs` まで到達することを確認します。従って KBMAG が生成した
   opaque rule や forged `after` は通りません。

3. `rows`

   `index=1..972` の全行を要求し、各行について canonical F6 norm から開始し、
   `rule_steps` の位置・lhs一致・置換後 `after` を順番に再生します。終点が
   `normal_form_source.normal_forms[index-1]` と一致すること、全 index が揃う
   ことを必須にしました。`final` が付く場合も同じ終点と比較します。

この構成では、rule proofが元の presentation 内の等式、row traceがその有限
個の合成です。`u ~= v` を158 relatorのnormal closureでの等式とすると、
free reductionは群要素を変えず、`cancel` は逆元対の削除、relator の cyclic
conjugate（または inverse）の insertion/deletion は `~=` を保ちます。従って
primitive proofとrow traceへの帰納法で、972 行すべての終点が空語なら、KBMAG
の完備性や confluent normal formを仮定せずに、固定U内の local van Kampen /
rewrite certificate が得られます。逆に rule ledger、source、row のどれかが
欠ければ fail-closedで UNKNOWN です。

checkerの成功 status は `LOCAL_972_NORMS_REPLAY_CERTIFIED`、global status は
常に `GLOBAL_SURVIVAL_UNKNOWN` です。これは PB4 の全 refinement を自動的に
encodeしたり、cofinal な towerで identity が生き残ることを示したりしません。

## GHA の最短分割案

1. canonical source → v2 Tietze producer → `crosscheck/check_d972_b4_norm_tietze_dense_v1.py`
   で、161/5056、34 primitive step、dense map、972 final words を独立照合する。
2. `search/d972_b4_norm_tietze_kbmag_consumer_v2.g` の <=127-generator lane を
   実行する。現行版の `roof_bits` だけでは足りないので、versioned producer
   出力に `final_norm_words`（dense basis）と、v2 trace の snapshot 済み
   `new_to_old` map digestを追加する。
3. dense wordを signed F6 wordへ戻す変換を、GAP側の共有 helperでなく独立
   Python側で行う。具体的には final dense → stable RS generator の
   `new_to_old` snapshot → v2 `pair_words`（各RS generatorの元F6 word）を
   合成する。event mapは後続 in-place mutationを参照しない snapshotでなければ
   ならない（既に検出された `new_to_old` mismatchを再発させない）。
4. KBMAG ruleを取得できる場合は、各 `lhs -> rhs` に元158 relatorからの
   primitive proof DAGを添付する。KBMAG 1.5.11 の unlogged ruleに provenance
   が無い場合は、ruleごとに独立 van Kampen finderを走らせて proof_stepsを
   生成する。どちらも無い状態で bitsだけをBに昇格してはならない。
5. 本 checkerを artifactに対して実行する。`LOCAL_972_NORMS_REPLAY_CERTIFIED`
   になるのは972 rows、全 rule proof、全 normal formが空、かつ KBMAG status が
   上記の empty candidate の全条件を満たす場合だけ。それでも `global_b_status`
   は `GLOBAL_SURVIVAL_UNKNOWN` のままである。それ以外（非空 normal form、
   KBMAG未完、rule欠品、partial ledger）は `UNKNOWN` であり、Aへの反転も行わない。

つまり現在の consumerを少し拡張するだけで、重いKBMAGを再計算せずに済む
「計算 → output extraction → 独立 van Kampen replay」の分割になります。ただし
rule provenanceを出せないKBMAG実行の `roof_bits` 単独には、どれだけ全行が true
でも証明力はありません。

## 検査結果

ローカルで実行したのは軽量な Python の構文検査と toy fixture だけです。

```text
python -m py_compile crosscheck/check_d972_b4_kbmag_vankampen_extract_v1.py
python crosscheck/check_d972_b4_kbmag_vankampen_extract_v1.py --selftest
SELFTEST_PASS schema=d972-b4-kbmag-vankampen-bundle/v1
```

selftest は、正しい relator deletion の通過に加えて、primitive `after` 改竄、
row application `after` 改竄、index欠番、nonempty normal form の terminal昇格を
拒否します。972 canonical inputへの完全実行、GAP、KBMAG、SAT、workflow dispatch
はこの便では行っていません。従って本便の成果は「B4-Bを確定した」ではなく、
unlogged KBMAG outputを固定Uの local norm certificateへ昇格させるための
独立・再生可能な最小証明路線とcheckerの実装です。global B4-Bへ進むには、
この local receiptとは別に、PB4 typed refinement、survival/cofinality、及び
その shadowからglobal B4-B/Ihara conclusionへ至る数学的 bridgeを明示的に
証明する必要があります。
