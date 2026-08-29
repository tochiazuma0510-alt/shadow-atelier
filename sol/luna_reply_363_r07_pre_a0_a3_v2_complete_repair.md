# Luna reply 363 - R07 pre-A0 A3 v2 complete repair

## 0. 結論と作業境界

Task363 の五つの指定 owner を完成・凍結した。v1 の数学的に正しい
g760/task226/v302/task227 部分は再利用し、task361 の F1--F7 は一つの
v2 repair にまとめて閉じた。task227 の静的 field-read trace で
`rword_g`/`rword_f` は値を一度も読まず presence だけを要求することを
確認したため、v303 が決めない値を流用せず、明示的な
`V303_OMITTED_NOT_CONSUMED` compatibility marker を minimal consumer
ABI にだけ置いた。したがって BLOCKED 条件は生じていない。

Python、Node、GAP、GHA、workflow、network、git、candidate program は一切
実行していない。v1、task198、task226、task227、proof、workflow、v220
その他の非指定 path は変更していない。candidate-free PowerShell 使用は
byte inspection/SHA-256/ordinal canonical cross-check と、次の bounded
final-byte normalization に限定した。P0 の意味内容は `apply_patch` で編集し、text patcher が付ける最後の
LF だけは、対象絶対 path・変更前 13,749 bytes・末尾 `0x7d 0x0a` を
確認した上で 1 byte の bounded final-byte normalization を行った。

## 1. 凍結した四 owner

| owner | bytes | physical SHA-256 |
|---|---:|---|
| `ci/in/d972_r07_pre_a0_single_target_a3_v2.prereg.v1.json` | 13,748 | `4a7f966d803dfdf7977dc73ab2db9b7f54d0d932ec2a10e410e034b5b6b151af` |
| `search/d972_r07_pre_a0_single_target_a3_v2.py` | 76,763 | `01578037cfabc73fdb7cb29d7725a41f903b05aab0f689d259fc89f56489daa6` |
| `crosscheck/check_d972_r07_pre_a0_single_target_a3_v2.py` | 84,273 | `3d77b6e6ca577bd762512b99a1ba2be647d994c4632b66ca2478259fea06f403` |
| `search/d972_r07_pre_a0_single_target_a3_gha_driver_v2.g` | 15,917 | `05ecedcf238fc55f758302a6210de0e32cf52c5d6304d3ad472007aba99c99b6` |

P0 self seal は
`f633498efef1e8fb2adf02a474dcca05b87de83fe5655e1e805f8e10f1f916a4`。
独立の ordinal-key compact-ASCII encoder で次を静的照合した。

- raw bytes = 再構成 canonical bytes: true;
- canonical length = physical length = 13,748;
- BOM = none, CR = 0, LF = 0, non-ASCII byte = 0;
- first/last byte = `0x7b`/`0x7d`;
- top-level `self_digest_sha256` だけを除いた body SHA-256 =
  declared self seal。

両 Python owner の exact P0 path/bytes/physical SHA/self seal は producer
30--33 行、checker 30--33 行にある。canonical-input predicate は producer
445--453 行、checker 373--381 行で、凍結 raw と
`json.dumps(sort_keys=True,separators=(",",":"),ensure_ascii=True)` の
完全一致を要求する。driver の acyclic pin table は 15--21 行、64-hex
shape と物理 byte/SHA 比較は 25--51 行である。Section 3 の明示 graph
どおり driver は P0 と両 Python の三 upstream owner を pin し、graph
leaf である driver 自身の physical identity はこの返信で凍結した。

## 2. Authority/import graph

依存 graph は次の一方向だけで、P0 は新 v2 program/driver を pin しない。

```text
accepted task198:
  receipt + acceptance manifest + producer/checker attestations
  + checker verdict + producer/checker/driver source owners
g760 ancestry (2 owners) + v302 + v303
task226 producer/checker
task227 producer/checker/driver + accepted SELFTEST metadata
                         |
                         v
                    canonical P0
                    /          \
       producer P0 pin          checker P0 pin
       task226 producer         task226 checker
       task227 producer         task227 checker
                    \          /
                     final Python hashes
                             |
                             v
                serial accepting-only GAP driver
```

P0 authority の全 `{path,bytes,sha256}` は再帰的に一意化して物理照合する
(producer 498--519 行、checker 427--447 行)。dynamic import は producer
側が pinned task226 producer と task227 producer の二つだけ
(1432--1458, 1621--1622 行)、checker 側が pinned task226 checker と
task227 checker の二つだけ (1304--1324, 1565--1566 行)。import 前後で
同じ source bytes/SHA を再照合する。checker は producer helper を
import しない。

driver は final Python SHA を full 64 hex で直接 pin し、receipt の
physical SHA を producer 終了直後に取得して
`--receipt-sha256 "$rsha"` として checker に渡し (134--135 行)、
checker 後と最終 acceptance 直前に再 hash する (145--146,
191--192 行)。

## 3. task198 full authority と evaluator ABI

両側の full authentication は producer 575--728 行、checker
526--669 行にある。31,017,244-byte receipt は stat/reserve 後に一度だけ
read/parse し、manifest とともに bounded streaming canonical encoder
で retained raw と chunk 比較する (producer 353--417, 586--591 行;
checker 280--344, 537--542 行)。二つの self seal も seal-stripped
stream で照合する。

次の semantic edge をすべて exact equality で閉じた。

- `accepted_receipt_basename` と physical receipt basename;
- producer/checker の run, head, artifact_id, zip SHA,
  terminal-line SHA、および member の basename/bytes/SHA;
- producer/checker attestation の basename/bytes/SHA と literal line;
- checker verdict の basename/bytes/SHA/schema/receipt terminal/
  `accepted=true`/`independent=true`;
- manifest receipt/member/attestation/verdict/source-owner links;
- manifest/receipt self seals と task198 acceptance run/head/zip/terminals。

根拠箇所は producer 604--692 行、checker 554--634 行。特に member と
attestation の cross-link は producer 627--638 行、checker 576--587 行。

P0 の evaluator contract digest は
`4fc38881ffee293f0820d3639230dd44a2af9b9ed126dfb21dc5831290ff08b8`。
literal eleven-row bridge ledger は producer 694--703 行/checker
636--645 行で local literal と accepted receipt と P0 の三者一致を取る。
contract は次を exact に含む。

- schema `d972-r07-v188-roof-consumer-action-abi/v1`;
- module `search/d972_r07_seven_context_roof_presentation_v1.py`;
- registry `v188_consumer_action_abi`, runtime constructor
  `load_runtime`;
- widths `[40,40,40,40,40,154,154,154,154,154]`;
- coordinate-ledger digest
  `9f9c081e9653d6e141e4d6d231e2d6db9526850b7ccd33c0859d13825f3fa83c`;
- relator-row digest
  `e00880c01bc96ba8f0549311f4955662668d74001ecf5c06097646dad4268950`;
- `roof_action(runtime,actor_word,value)`,
  `roof_eval(runtime,word)`, `roof_inverse(runtime,value)`,
  `roof_multiply(runtime,left,right)`,
  `roof_section_cocycle(runtime,left_section_word,right_section_word,
  product_section_word)`,
  `roof_source_section(runtime,gamma_state_id,q0_state_id)`;
- strict signed-F2/source-state/ten-hex-coordinate encodings and
  left-then-right multiplication, conjugation action, section-cocycle
  conventions。

accepted evaluator object の exact keyset/core と canary types は producer
704--725 行/checker 646--666 行で照合し、全六 callable binding と
ordinary g760 target/central reconstruction を producer 964--999 行、
checker 1131--1165 行で exercise trace に結ぶ。raw map は producer
1616--1618 行で result 構築前に解放し、checker は 1762--1764 行で
production receipt を読む前に解放する。したがって checker では
task198 raw と新 receipt DOM は overlap しない。

## 4. v303-only projection と task227 consumer ABI

task226 full package は closure input にせず、producer 932--961,
1226--1255 行、checker 865--887, 1098--1128 行の
`BASE_REFERENCE_ONLY` record に限定した。ここには computational base
`f=g760,a=[]`, zero `B_a`, `rword_f`, PB-chain diagnostics を
`transfer_evidence=false` として隔離する。

explicit `projected_a3_interface_v2` の allowlist construction は
producer 1074--1223 行、checker 952--1095 行。top-level trace は:

```text
schema, projection_mode, mode, correction_word_constructed,
task192_consumed, f_role, projection_only, modulus, ten_to_eleven,
authenticated_ledger, group_field_coordinate_codecs,
actor_orbit_convention, occurrences, combined_w, combined_u0,
target_blocks, target_role, full_package_fields_excluded,
self_digest_sha256
```

各 occurrence は次の extant field だけを持つ。

```text
ordinal, block, block_index, block_slot, occurrence, type, ten_index,
context_id, role, factor_sign, orientation, fox_prefix_occurrences,
combined_block, q_degree, key_width, p_o, q_o(x), q_o(y), xi_o, w_o,
translated, u0, ancestry
```

したがって十一 occurrence の separate H1/H2/P typing、全 q-map、
`p/xi/w/u0`、combined `w/u0`、target、actor/orbit convention、
F3/Q3/Q4/sparse codecs、v303 mode が明示される。interface には
`literals`, `rword_f`, `B_a`, exact PB-chain field,
`task192_ancestry` その他 full-package field はない。

この interface だけから consumer ABI
`{schema,modulus,occurrences,bar_epsilon_1,u0,ten_to_eleven,
self_digest_sha256}` を作る (producer 1118--1138、checker
996--1013 行)。consumer occurrence は task227 が実際に読む
`ordinal,combined_block,q_degree,key_width,factor_sign,p_o,q_o(x),
q_o(y),xi_o,w_o,translated,u0,fox_prefix_occurrences,orientation,
ancestry` と、presence-only marker 二つだけである。full ABI の
`rword_f` 値は転送しない。

各 seal は旧 `self_digest_sha256` を pop し、body を canonical hash、
seal 挿入後ただちに untouched baseline を照合する (producer
1082--1098, 1140--1168 行; checker 960--975, 1016--1044 行)。
runtime seal trace は四つを別所有する。

```text
projected_interface_body_sha256
projected_interface_sealed_sha256
task227_consumer_abi_body_sha256
task227_consumer_abi_sealed_sha256
```

`ABI_seal_target` mutation はこの baseline PASS 後にだけ実行される。

## 5. closure と独立 checker

producer の load-bearing call は
`t227.closure(consumer, closure_budget, structural=None)` の一回だけ
(1646--1656 行)。closure 前に full task226 package を解放し、consumer
以外を渡さない。frozen `encode_gate` の complete gate を保持するため、
occurrence basis/ancestry、block basis/echelon/remainder、rank、
canonical 486 rows、729 translates、`c_i/lambda/kappa`、四 replay
rows、quotient remainder、および MEMBER replay または NONMEMBER dual
pairings は Boolean summary に縮退しない (1660--1692 行)。

checker の唯一の expensive verifier call は
`task227 checker.verify_gate(gate, consumer, internal, "production")`
(1662--1673 行)。wrapper 自身に逆向き span call はない。凍結 verifier
内部には `compare_sparse_spans` が正確に 12 call あり、verdict は
`frozen_internal_span_comparison_calls=12`,
`wrapper_reversed_span_calls=0` と正直に記録する (1540--1546 行)。
bounded call 後、type/rank と exact 486/729 を数える
(1676--1691 行)。

checker は producer top/result/gate の完全な false flags を要求し、
`actual_a3_numerator=false` も欠落不可 (44--46, 1599--1661 行)。
さらに P0、全 authority identities、projection/consumer seal trace、
central/target/evaluator/area/mutation、ranks/terminal/resource telemetry
を独立再構成し、producer result 全体との exact equality と bounded
streaming digest を取る (1693--1741 行)。verdict は receipt
bytes/SHA/self seal、P0、authority digest、projection/consumer digests、
central digest、ranks、terminal、mutation digest、および
`independently_reconstructed_result_sha256` を束縛する
(1502--1548 行)。

## 6. baseline と exact mutation matrix

両側は実際の authority snapshot、ledger、g760、base reference、
central replay、area targets、explicit interface、consumer ABI、false
flags から同じ ordinary cheap validator fixture を独立構成する。
untouched full baseline PASS は producer 1359--1366 行、checker
1259--1266 行で mutation より先。expected reason は catch の外で
P0 から読む (producer 1408--1421、checker 1285--1295 行)。

| mutation | extant owner | exact expected first reason |
|---|---|---|
| `task198_raw_manifest_binding` | authority manifest/member | `task198 raw/manifest binding` |
| `task198_ledger_sign` | literal ledger | `task198 ledger sign` |
| `task198_prefix` | literal ledger | `task198 ledger prefix` |
| `g760_letter_digest` | g760 | `g760 digest` |
| `computational_base_mode` | base reference | `computational-base mode` |
| `forbidden_task192_binding` | base reference | `task192 binding` |
| `H1_central_row` | central replay H1 | `H1_central_row` |
| `H2_central_row` | central replay H2 | `H2_central_row` |
| `P_central_row` | central replay P | `P_central_row` |
| `projected_area_target` | actual area row | `projected area target` |
| `ABI_seal_target` | valid consumer ABI | `ABI seal/target` |
| `forbidden_conclusion_flag` | false flags | `forbidden conclusion flag` |

`MutationAccepted` と wrong reason は narrow `NarrowReject` catch の外へ
出る。checker は producer record を信用せず自分の 12 件を実行する。

## 7. caps、accounting、performance

P0 と両 wrapper の共通 hard envelope は
`wall_seconds=1800`, `rss_bytes=4,294,967,296`,
`serialized_bytes=20,000,000`, `input_bytes=60,000,000`,
`authority_bytes=40,000,000`。完全な cap map は producer 46--56 行、
checker 47--57 行。Linux `signal.setitimer` は各 expensive region の
残り process wall を interrupt し、finally で cancel/restore する
(producer 288--317、checker 218--246 行)。dynamic import 前に
`resource.RLIMIT_AS` hard ceiling と Linux `renameat2` availability
を要求する (producer 320--340、checker 249--268 行)。RSS sampling は
boundary evidence であり in-call interrupt とは称していない。

exact byte formulas は次のとおり。

- unique P0 authority files: 31,512,075 bytes;
- producer input worst static reads:
  `13,748 + 31,512,075 + 2*(40,556+47,135)
   = 31,701,205 < 60,000,000`;
- checker before production receipt:
  `13,748 + 31,512,075 + 2*(35,463+34,200)
   = 31,665,149`;
- checker with maximal accepted production receipt:
  `31,665,149 + 19,000,000 = 50,665,149 < 60,000,000`;
- producer output reservation:
  `19,000,000 + 65,536 emergency = 19,065,536 < 20,000,000`;
- checker output reservation:
  `1,000,000 + 65,536 emergency = 1,065,536 < 20,000,000`。

19 MB producer maximum は accepted five-case task227 receipt
4,636,766 bytes の約 4.1 倍で、2 GB wrapper allowance ではない。
producer は gate materialization 前に reserve (1662--1664 行)、
checker は verdict construction 前に reserve (1774--1776 行)。
fixed-point serializer は repeated pass を論理 output として重複加算せず、
sealed `resource_meter.used.serialized_bytes` と final raw length を
一致させる (producer 1466--1495、checker 1373--1402 行)。

frozen task227 の production resource canary に現れる 2,000,000,000 は
凍結 engine の inner schema を verifier が要求する値であり、v2 wrapper
output cap ではない。q-multiplication に対する frozen
`actor_operations`/`orbit_actions` 二重 callback は producer
`ClosureBudget` が actor 一回だけを charge し、orbit 側を alias event
として記録する (268--285 行)。checker の opaque verifier は
`independent_verify_calls=1` のみを call 前 reserve/call 後 consume
する。486/729/ranks は call 後の reconstructed object から数える。

accepted SELFTEST は五 case 493 秒、単純一 case 比は約 99 秒である。
base/authority/serialization margin を含む nominal estimate を各 side
300 秒、internal hard wall を各 1,800 秒、external timeout を各
2,100 秒とした。serial external maximum は 4,200 秒で、setup margin
を足しても six-hour=21,600 秒より厳密に小さい。driver の frozen estimate
と二 timeout は 80, 83--84, 134--135 行。

## 8. failure-atomic publication と terminal state machine

producer 1498--1584 行、checker 1405--1492 行は同じ安全 state machine
を別実装する。

```text
fresh final + no stale temp
  -> emergency reserve already held
  -> normal maximum reserve
  -> complete fixed-point serialization in memory
  -> exclusive same-directory temp (O_EXCL/O_NOFOLLOW)
  -> full write -> fsync(temp)
  -> renameat2(RENAME_NOREPLACE)
  -> fsync(directory)
  -> exactly one terminal print
```

rename 前の failure は temp を best-effort cleanup し final を absent に
保つ。rename 後 fsync failure は final unlink + directory fsync rollback
を試みる。normal reservation を解放後、small pre-reserved emergency
UNKNOWN が同じ atomic route を使える。stale final/temp は overwrite
せず distinct nonaccepting failure。MemoryError/wall/allocation は
`UNKNOWN_RESOURCE`、input/auth/schema は `UNKNOWN_INPUT`。UNKNOWN
receipt/verdict は self-sealed だが exit nonzero である
(producer 1710--1755、checker 1744--1818 行)。

## 9. serial accepting-only driver

driver は開始前に final/log/shell/sentinel と Python atomic temp alias を
拒否する (53--64, 81--82 行)。producer/checker を各 2,100 秒で直列実行
し、各 log に exact-one recognized full-line terminal と exact-one
terminal prefix を要求する (83--94, 134--143 行)。UNKNOWN、timeout、
missing/malformed terminal は `D363_DRIVER_UNKNOWN` を出して exit 41、
accepted sentinel を作らない (79, 90--94, 141--143 行)。

accepted route でも次が全部必要である。

- producer/checker process exit 0 と同じ accepted terminal;
- receipt/verdict regular, non-symlink, nonempty, cap 内;
- compact canonical raw と top/nested self seals;
- P0 と全 authority identity の physical cross-binding;
- projection/consumer body+sealed digests;
- complete false flags、central/mutation/rank/terminal/result digest;
- exact receipt SHA injection と checker 後/最終直前の二 rehash;
- verdict `accepted=true`, `independent=true`,
  verifier count 1、inner span count 12、wrapper reverse count 0。

この後だけ shell が fresh sentinel を作り、GAP がそれを exact read-back
して一行の `D363_DRIVER_ACCEPTED` を出す (195--201 行)。UNKNOWN/
mismatch route に PASS/ACCEPTED sentinel はない。

## 10. frontier

本便は static implementation/freeze だけであり、actual closure result は
まだ存在しない。従って MEMBER/NONMEMBER のどちらも未観測、A3 numerator
は 0/3 のまま、A0/common/pointed/exact-PB/cofinal/fake/Ihara へ結論を
運ばない。P0 と source hashes を変えず、独立 Sol(max) static PASS 後に
親 session が fresh GHA を dispatch するまで `UNEXECUTED` である。

```text
V1 TASK359:                           STATIC REJECT / SUPERSEDED
V2 CANONICAL P0 + FULL PINS:          PASS
TASK198 FULL AUTHORITY/EVALUATOR ABI: IMPLEMENTED
SUFFICIENT V303-ONLY PROJECTION:      IMPLEMENTED
ONE ACTUAL 486/729 CLOSURE ROUTE:     IMPLEMENTED
INDEPENDENT BOUNDED MEMBER/CHECKER:   IMPLEMENTED
BASELINE + GLUE MUTATIONS:            IMPLEMENTED
FAILURE-ATOMIC PUBLICATION:           IMPLEMENTED
SERIAL ACCEPTING-ONLY DRIVER:         IMPLEMENTED
EXECUTION / GHA:                      UNEXECUTED
ACTUAL A3 NUMERATOR:                  remains 0/3 pending accepted run
A0 COMMON / POINTED / EXACT PB:       OPEN
COFINAL LIFT / FAKE / IHARA:          NONE
```

`TASK363_R07_PRE_A0_A3_V2_COMPLETE_REPAIR`
