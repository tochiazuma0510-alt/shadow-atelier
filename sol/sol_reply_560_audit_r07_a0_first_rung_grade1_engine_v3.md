# Sol Reply 560 — A0 first-grade engine v3 差分限定 release 監査

役割は Sol(max)、判定対象は Task558 が列挙した R1--R4 の修復だけである。
実 first-grade 計算、prepare/block/merge、並列 Python、git/GHA、追加の数学設計は
行っていない。結論は **R1--R4 はすべて閉じており、v3 を production graph に
release してよい**、である。これは production membership の判定ではない。

## 1. 凍結入力と受領確認

指定された文書と v2/v3 producer/checker を全体として順に読み、次を再計算した。

| file | bytes | SHA-256 |
|---|---:|---|
| `sol/sol_task_560_audit_r07_a0_first_rung_grade1_engine_v3.md` | 4,102 | `971a0b1064df27173cc14441f33cb07e8d3dd123a2ad5005bdc8294f8728c66f` |
| `sol/sol_reply_558_audit_r07_a0_first_rung_grade1_engine_v2.md` | 22,080 | `b61962bf557c4790fc1d36dde49805527e245933300348c76970c5e7fc49cf6f` |
| `sol/luna_task_559_r07_a0_first_rung_grade1_release_repair_v3.md` | 6,615 | `0733be2dc26388fbee0855a2a2746251a7e0db851ff50b9924e1114406b56e4d` |
| `sol/luna_reply_559_r07_a0_first_rung_grade1_release_repair_v3.md` | 7,931 | `8ccb6304243e3045e2edb1cde5ce196b90ab7a4a8a4579c9c4f0da95d20ae976` |
| `search/d972_r07_a0_first_rung_grade1_v2.py` | 114,922 | `df3aea9f49f5f76cd52f10923a38f75072eb2fc9cd4808578259ee48c4129ee4` |
| `search/check_d972_r07_a0_first_rung_grade1_v2.py` | 55,010 | `a11824ff42602698219ccd130e1a03d1fd4dcdc76a3cbece4a9ed816e0ac050d` |
| `search/d972_r07_a0_first_rung_grade1_v3.py` | 138,202 | `bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff` |
| `search/check_d972_r07_a0_first_rung_grade1_v3.py` | 69,193 | `67f56ee92aea7e17ce88303657ca519ee9539269eef44e6e5550da63d6a4a012` |

v2 の二つの receipt は Task558 と一致する。v3 checker の
`PRODUCER_SHA256` は producer v3 の上記 digest と完全一致する。監査開始時と
bounded checks 終了時の双方で
`search/certs/d972_r07_a0_first_rung_grade1_v3.json` は存在しなかった。

## 2. R1--R4 差分監査

### R1 — PASS: NONMEMBER roster は全量を algebra 前に閉じる

checker の `validate_nonmember_block_roster` は、各 block について
`origin_count == len(prepare["defect_origins"])`、origin reductions の完全な
`origin_count` 本、actor transitions の `rank x 4` 本、DAG の `rank` 本を先に
要求する。`validate_expression` は参照 pivot と F3 coefficient を bool ではない
plain integer に限定し、それぞれ `0 <= pivot < rank` と `{1,2}` を要求する。
DAG reduction はさらに `pivot` より前、defect origin は全 origin 範囲内、actor
parent は現在 pivot より前でなければならない。

この gate は `validate_block_state_file` を介して四 block 全部に適用され、
NONMEMBER branch の `verify_nonmember` でも packet/transition algebra より前に
再度到達する。その後の checker は全 packet origin の containment、全 pivot の
四 actor transition、各 coupled defect の physical aggregate に対する dual
annihilation、および全 old-lift zero-lower connection を従来どおり直接確認する。
したがって origin list の prefix だけを検査して terminal に進む経路はない。

fixture の一-origin block から `origin_reductions` だけを空にした canary は
`origin_reduction_count` で拒否され、公開出力も
`"truncated_origin_reduction":"REJECTED"` となった。

### R2 — PASS: state/blob の current binding と bounded authentication

producer の prepare/block/merge validators は、現時点で再読した全 18 input
receipt とその canonical digest、phase/fixture、parent、固定 dimensions、各 roster
cardinality、queue/attempt receipt、DAG/roster digest、terminal 種別を phase ごとに
fail closed で照合する。block は character と packet SHA に、merge は ordered な
四つの exact block body digest に結ばれる。既存 provisional merge も finalizer を
呼ぶ前に同じ ordered list に一致しなければならない。

blob validator は receipt の完全な key set、basename/hash suffix、rows、width、
encoding、計算された byte count と stat size を確認し、1 MiB 固定 chunk で SHA-256
を取る。認証 cache は path/size/digest/mtime/inode に結ばれ、stat の前後一致も
要求する。新規 block/merge の実消費では `read_blob(..., retain=True)` が同じ
authenticated stream の chunks を保持する。completed prepare/block/merge resume は
各 phase に relevant な residual、old lower/lift、packet、block basis、physical basis
（MEMBER なら degree-2 residual も）を認証してから返る。checker 側も同じ exact
receipt 条件を 1 MiB streaming で検査し、packet は mmap-backed のまま各 row を
読む。SHA scan を row loop 内で反復する経路はない。

### R3 — PASS: final HEAD 後の deterministic certificate recovery

`build_terminal_certificate` は authenticated final merge と exact prepare/block
chain から公開 object 全体を一意に組み立て、fixture または `MEMBER/NONMEMBER` の
provisional terminal を拒否する。`install_or_validate_terminal_certificate` は欠品時
には canonical bytes を atomic install し、既存時にはその bytes が再構成した完全
な canonical expected object と一致することを要求する。runtime は final merge body
に封じた `elapsed_seconds` を再利用するので recovery bytes は変わらない。

finalizer が final merge body/HEAD を先に seal して certificate install に進むため、
その間で crash しても、次の `--merge` は prepare、四 block、final merge と relevant
blob を認証した後、final terminal branch から同じ install 関数を再実行する。既存
provisional terminal は finalizer に戻され、直接 publish されない。checker も
certificate の canonical encoding を要求し、独自 `expected_certificate` と object
全体を equality 比較してから MEMBER/NONMEMBER terminal algebra に進む。fixture の
二回 install は同一 object/bytes と sealed runtime `12.5` を再現した。

### R4 — PASS: packet ingestion と lower replay の既存 gates

block の初期 packet-origin loop は actor queue と同じ block seconds/RSS caps の内側に
入り、256 attempts または 30 秒ごとに RSS 付き `block-ingest` progress を出し、各
attempt で resource gate、loop 完了直後にも completion check を通る。

prepare caps は seed evaluation と raw/canonical lower replay より前に初期化される。
`replay_lower_terms` は 256 terms または 30 秒ごとの progress/resource gate と終了時
completion check を持ち、raw と canonical の両 replay に同じ caps が渡る。terminal
MEMBER の zero-lower update replay にも merge caps が渡る。precision-one replay は
同じ progress cadence に加え各 term で resource gate を通る。したがって Task558 が
指摘した「ingestion 完了まで cap が届かない」経路と lower replay の未完了 gate は
閉じた。

## 3. regression と bounded checks

v2/v3 の top-level blocks を比較した。producer の affine multiplication/action、
Fourier transport/projector、direct target、paired closure、packed-echelon pivot policy、
physical lower-first merge、literal DAG expansion、degree-2 continuation の各数学関数は
変更されていない。共通 block の変更は blob/state I/O、validators、phase dispatch、
cap plumbing、certificate finalization と fixture に局在する。checker でも direct/
induced accumulation、independent physical aggregation、old-connection reconstruction は
変更されず、`verify_nonmember` の algebra 本体には事前 roster gate と bounded data
lifetime だけが加わった。packet mmap と block ごとの dense buffer 解放により、新たな
回避可能な全 packet 展開や loop 内 full-file rescan もない。有限 row universe、pivot
選択、ancestry の符号/scale、MEMBER direct replay、NONMEMBER dual criteria は不変である。

許可された Python commands だけを直列実行し、bytecode cache は
`%TEMP%\task560_pycache` に置いた。

1. `python -B -m py_compile search/d972_r07_a0_first_rung_grade1_v3.py search/check_d972_r07_a0_first_rung_grade1_v3.py`
   — exit 0、stdout/stderr なし、outer wall `0.6286124 s`。
2. `python -B -u search/d972_r07_a0_first_rung_grade1_v3.py --fixture`
   — exit 0、outer wall `2.0429084 s`、内部 `elapsed_seconds=0.5462718000053428`。

```json
{"block_ranks": [1, 1, 1, 1], "certificate_recovery": "PASS", "elapsed_seconds": 0.5462718000053428, "fixture": "PASS", "merge_sha256": "767dbeb79e6e7c0e9efcce3e09e407d52adc452219a00d9887e2c3c99b024a58", "nonmonotone_leads": [5, 3], "packet_projector_ancestry": "PASS", "physical_rank": 4, "semantic_mutations_rejected": 3, "state_validators": "PASS", "terminal": "FIXTURE_MEMBER", "v443_actor_accumulation": "PASS"}
```

3. `python -B -u search/check_d972_r07_a0_first_rung_grade1_v3.py --fixture`
   — exit 0、outer wall `1.5616926 s`。

```json
{"canonical_terms": 2622, "fixture": "PASS", "mutations_rejected": 3, "pinned_inputs": 18, "projectors": 16, "raw_terms": 3936, "truncated_origin_reduction": "REJECTED", "v443_actor_accumulation": "PASS"}
```

これらは seconds-scale の reached-path 補助であり、production rank、runtime、terminal
を計算してはいない。R1--R4 の release 判定は上記の static load-bearing call sites に
基づく。追加 repair、optimization、test campaign は要求しない。

## 4. release 判定と claim boundary

凍結 v3 の R1--R4 はすべて閉じ、受理済み数学の regression はない。この exact
producer/checker pair に限り production GHA release を許可する。first-grade membership
およびその先の算術 claim は未計算・未宣言であり、Lean verification もない。

FIRST_GRADE_ENGINE_V3_PASS
GHA_RELEASE: ALLOWED
FIRST-GRADE MEMBERSHIP: NOT COMPUTED
ORDER-54,432 / FULL-Q0 / A0 / COMMON / COMPATIBLE LIFT / FAKE / IHARA: NOT DECLARED
verified=false
