# Luna reply 354 - R07 A0/v12a auditable SELFTEST bootstrap

## 結論

task354 の二版プロトコルに従う v12a を実装した。v12a の唯一の入口は
SELFTEST_BOOTSTRAP であり、R/V は決定的な candidate artifact に限る。
PRODUCTION/RESUME、acceptance、A0 COMMON、separator、negative、lift、fake、
Ihara の主張は全て不許可である。P0 は最終 producer/checker/fixture と全
frozen authority を固定し、未実行 R/V の物理値だけを
TO_BE_GENERATED_BY_AUDITED_V12A_SELFTEST として事前登録する。

この便では指示どおり Python、Node、GAP、GHA、workflow、git、network、
candidate を一切実行していない。行った照合は read-only PowerShell による
bytes/SHA、ASCII/LF、P0 self seal、P0/source/frozen roster の静的照合だけで
ある。従って runtime と RSS は UNEXECUTED であり、Sol(max) の新しい静的
再監査が次の gate である。

## 最終 machine identities

| file | bytes | SHA-256 |
|---|---:|---|
| ci/in/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12a.manifest.v1.json | 10,058 | f127bac60d4fb41d984fcfdc57f77a32cc88e32905207009e6758ec913d1d52d |
| search/d972_r07_history_free_positive_fast_resume_v12a.py | 304,762 | 0e938caeb83b4e65440495b0f50952135d4bfca4309aef38f16c00f50d2905cf |
| crosscheck/check_d972_r07_history_free_positive_fast_resume_v12a.py | 237,150 | b3d95ae7bb7c82878121a5a386e934b425259ef5ea00e80f31d7202d827750a0 |
| search/d972_r07_history_free_positive_fast_resume_gha_driver_v12a.g | 24,621 | 816dfb705d38692393cce28675f90e6759065ebb47714ee8ef4c744a54807610 |
| search/certs/d972_r07_history_free_positive_fast_resume_selftest_v12a_20260829.json | 22,094 | 6a87bf608bf0a392ff77d3aacbe813a0cc01f54d67bd5d346fb75ee1e7000ffc |

P0 は sorted ASCII canonical JSON + exactly one LF である。P0 の
self_digest_sha256 は
7c81a9167612300579dac8bb7dd1b5b3f4a48bf08963f00cdc498edc8ecfedf2
で、同 field を除いた canonical object から静的に再計算して一致した。
P0 の 3 source rows は上表の最終 identity と一致する。P0 の frozen roster
は SOURCE_PINS 28 owner + raw checkpoint + checkpoint archive の 30 owner。
現存する 29 owner は全て bytes/SHA が一致し、未展開 raw は
86,368,039 bytes /
c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab
として sole-member archive に固定される。archive 自身も 5,001,811 bytes /
f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566
に一致した。raw canonical self seal は委嘱で PASS とされた
29bb74f3bd8048913a0365bc4c599f3731d32ba56967f3a238c7468b7fcfd123
を変更していない。

## 非循環 authority / import / process graph

    28 physical SOURCE_PINS + checkpoint archive + raw-member identity
                             |
    final producer ----------+----> P0 <---- final checker + final fixture
       |                              |
       | validates P0 schema/path     | exact sources/frozen rows
       | (no hard-coded P0 SHA)       |
       +---- raw + frozen owners + P0 ----> producer-local baseline/mutations
                                                 |
                                                 v
                                  deterministic candidate R
                                                 |
                      physical bytes/SHA/self/semantic + P0/frozen binding
                                                 |
                                                 v
                         independently written checker replay/mutations
                                                 |
                                                 v
                                  deterministic candidate V
                                                 |
                                                 v
                       driver artifact gate -> neutral last sentinel

P0 の全 graph/constructor/prospective field は manifest line 1 にある。edge は
sources/frozen -> P0、P0/raw/frozen -> R、physical R/P0/checker/frozen -> V、
P0/sources/frozen と candidate R/V -> driver artifact gate の順である。
producer/checker は P0 path と semantic/source roster を読むが P0 physical SHA
を source 内に hard-code しない（producer 5489-5561, 5606-5627、checker
3328-3384, 4317-4341）。R/V は driver SHA を含まない。driver だけが全4
ファイル確定後の P0 physical SHA を固定する（driver 33-68）。従って
cryptographic cycle と実行後 manifest rewrite はない。

Producer import graph は SOURCE_PINS roster と一回の immutable byte snapshot
registry（producer 117-178, 321-399）から frozen group/codec/Fox primitives
だけを load し、v10 producer/checker/main/mutation/search object を import
しない。checker は別に書いた Sources と composite validators
（checker 67-127, 325-405）を用い、v12a producer を import せず bytes と
P0 row としてのみ認証する。

Process 順は次のとおり。

1. driver が explicit bound mode と 32 pre-existing physical pin を確認し、
   prefix stale scan を行う（driver 25-105）。
2. no-follow archive FD、sole exact member、raw bytes/SHA、fixed .tmp、
   no-replace link、file/directory fsync で raw を展開する
   （driver 116-166）。
3. producer は P0/raw/frozen を一回認証し、light/triangular を構築してから
   W2/W4 process/fault owner を pre-heavy で完了し、その後だけ heavy owner と
   全 mutation suite を構築して R を exclusive publish する
   （producer 5606-5697、process suite 4586-4689）。
4. checker は P0 と physical R を独立 open し、pre-heavy checker process
   suite、task176/Q0/Gamma/K0、全 checker mutation suites を順に再構築して V
   を exclusive publish する（checker 4317-4469）。
5. driver は exact-one producer/checker full line と suffix byte equality を
   調べ、R/V canonical/self/semantic/source/frozen/physical-R binding を
   producer/checker import なしで照合し、neutral sentinel を最後に
   no-replace + fsync publish する（driver 167-284）。

Producer/checker の owned log 名は各 executable の stale gate 通過までは
.tmp capture に保ち、両 executable 終了後に no-replace publish する
（driver 109-114, 167-189）。従って log redirection 自身が ordinary stale
gate を先回りしない。

## task352/task353 finite repair trace

### 1. Triangular、meter、fixture、suite reachability

- Producer は 2,896 列を raw/ancestry として一回 parse し、P=A*C を row ごとに
  作り、禁止対象を chronological seen_pivots に限定する
  (1313, 1374-1383)。Checker も全 future roster ではなく独立
  seen_pivots を用いる (2755-2766)。
- reader は meter を明示引数に持つ (1047-1095, 2881-2966)。fresh meter の
  wall/RSS/counter policy は producer 401-480、checker 130-166。
  sparse_operations は inject/reduce/backsolve/annihilation/P-row で実際に
  charge される (1211, 1226, 1257, 1281, 1297, 1369)。
- current fixture pin は producer 142-143 / checker 112-113 と上表の
  physical identity。producer suite dispatch は 5402, 5434-5447, 5657、
  checker の独立 dispatch は 4368, 4395-4405 で全て main から reachable。

### 2. q3 の三 gate

- Producer の literal grammar / 0-based conversion / multiplication gate は
  validate_q3_literal_owner (907-940): 各 row は literal 1..36 (924)、
  変換は value-1 (926)、積は right[left[i]] として記録 (936)。
- Checker は physical literal rows を 1..36 として読む (565-573)、独立
  q0_perm_mul (841-846) で right[left[i]] を行い、selected replay
  (849-904) と chronological Q0 edge (2238-2246) の両方に使う。

### 3. Projected Gamma と full diagnostic

- Projected state は 5*40 + 5*154 = 970 bytes。Full JointGroup diagnostic
  は 40 + 31*154 = 4,814 bytes で別 codec
  jointgroup-E3-plus-31-E4/v1、非 load-bearing
  (producer 2212-2226, 2754-2767, 3736-3744;
  checker 1108-1122, 2829-2837)。
- selected owner は projected SHA と full factor widths/codec/SHA を別 field
  で持ち、producer/checker が別々に再構成する
  (producer 3298-3306, 3407-3420; checker 2559-2576)。

### 4. K0、A、kernel

- 定数は N=1,469,664、table=2^22、uint32。Producer open-address cache は
  StableProducerK0Index (2054-2198)、checker は別実装
  K0CoordinateStore (2009-2129)。hash は deterministic SHA-256 prefix。
- 一 coordinate payload は E3
  N*40 + 2^22*4 = 75,563,776 bytes、E4
  N*154 + 2^22*4 = 243,105,472 bytes。最大同時一-coordinate checker
  store は 256 MiB 未満 (2017-2028)。producer ten-store raw payload と
  全 index 上限は public formula (2251-2271) に固定。
- coarse key hit 後に retained 40/154-byte full state equality を要求する。
  miss または coarse/full mismatch は None で skip し、candidate-zero へ
  落とさない (producer 2099-2115, 2288-2316; checker
  2059-2074, 2335-2356)。accepted singleton-bucket statistics/digest と
  task176 physical receipt は producer 2117-2140, 3484-3523、checker
  2088-2111, 2302-2332 で exact equality。
- Gamma/A は exact first-gid table/order/literal SHA を比較する
  (producer 3238-3250, 3501-3523; checker 2170-2199, 2317-2332)。
- trivial kernel order 1 は generator 空 roster を受理し、非trivial時だけ
  generator 非空を要求する (producer 2341-2372; checker 2363-2375)。
  kernel は parent state × generator state の incremental BFS と direct word
  replayを各 edge で照合し、canonical state blobs/words/parents/generator
  indices、cursor state/wordを一致させる
  (producer 3525-3595; checker 2376-2436)。selftest selection は
  authenticated identity state cursor 0 を明示選択し、missing cursor/word は
  hard stop (3600-3621)。

### 5. Heavy identity

Producer は task176 physical blobs、receipt/manifest/crosscheck/recovery-v1/v2、
task176 checker/reply、Q0/Gamma/code ownersから OwnerPre を stream decode
して seal する (3820-4112)。actual selected Q0/Gamma/K0/kernel/dual/code
statement を加えた H は producer_final_heavy_identity (3777-3813)。
Checker は別 decoder/constructorで OwnerPre を作る (600-743)。selected
statement と H を独立再構成し、receipt の copied 64-hex shapeではなく object
equality + SHA equalityを要求する (2873-2940)。

### 6. DAG、carrier、phase/accounting

- DAG literal inner list は canonical typed bytesで再帰的 JSON
  normalizationされ、opcode/reference/orderを検査する
  (producer 201-319; checker 281-306)。Expansion は recursive call
  stackではなく bounded iterative post-order (224-264)。
- raw carrier/archive/manifest/recovery-v2 は P0 と driver の外部 pin。
  raw は一回 read/parse (1047-1095, 5629-5640)。
- light/heavy completion は phase ownerで分離され、early heavy call、
  fabricated digest、stale progress、zero->negative の actual mutationと
  light checkpoint/heavy transition positive gateを持つ
  (producer 5216-5374; checker 4108-4302)。
- IPC/history counter は additive、physical gauge は max として合成し、
  fresh invocation counterと host telemetryを分離する
  (producer 4562-4583, 4648-4688; checker 1852-1900)。

V12a は production/resume checkpointを作らず、unbound checkpointを
ordinary envelopeで拒む。R/V final publicationは bounded canonical write、
file fsync、no-replace link、directory fsync (2801-2876, 3387-3437)。
従って v12a に retire 対象の production checkpoint は存在せず、partial
candidate を mathematical terminal に昇格させない。

### 7. Bounded expansion、caps、typed stop

Producer cap は wall 10,800 s、RSS 5.7 GB、boundary pairs 8,000,000、
frame 32 MiB、candidate 512 MiB、checkpoint/DAG serialization 4 GB、
formal entries 2,000,000、sparse operations 12,000,000
(64-74, 401-480)。Checker cap は wall 7,200 s、artifact 3,600 s、
RSS 5.7 GB、allocation 4 GB、frame 32 MiB、candidate 512 MiB
(35-42, 130-166)。Input/resource/protocol failures do not emit a candidate
R/V or any mathematical claim。

### 8. Process/IPC/performance ownership

- Persistent light workers are forked before heavy construction
  (1617-2032, 4586-4689, 5657-5659); checker process suiteも heavy decode前
  (1852-1900, 4362-4377)。
- Parent sends bounded worker slices incrementally。Worker accumulator merge後、
  winnerだけに contributor requestを送り、selected contributor rows/digests
  を返す。parentの二回目 full contributor scanはない
  (producer 1800-1924; checker independent reconstruction 1524-1613)。
- STOP frame bytes/countも cumulative accountingに含まれる
  (producer 1984-2008, 4562-4583; checker 1773-1825)。
- Q0 duplicate edge は既知 prior の時点で ten-coordinate multiplicationを
  skip (2432-2481)。L bitset/proof は family/coordinate cacheを共有
  (2704-2743, 2775-2780)。selected coordinate K0 table は一回 build後に
  mutation群を通し、phase endで release (2274-2287, 5451-5464)。
- indexed symbol/DAGと O(1) meter countersを用い、telemetryは R/V の
  load-bearing fieldから除外する。

### 9. 全 physical mutation roster と reachability

Fixture roster と exact owner/validator/stage/first-reason contract は fixture
38-141, 142-234。各 mutation は cloneした actual baseline owner/transport
を変更し、reseal指定に従い、通常 validatorへ投入し、first rejection と
event traceを contractと比較する。Producer entry/call は
3078, 4454, 4790, 4921, 5005, 5216, 5402, 5434-5447。Checker の別実装と
main call は 3032, 3547, 3633, 3798, 3932, 4108, 4395-4405。

- process/fault 13 (fixture 38-51、producer 4586-4689、checker
  1852-1900): empty_support, one_support, short_support,
  typed_present_shape_filter, f3_cancellation, active, zero,
  three_serial_duals, deadline_timeout, blocked_pipe, worker_death,
  partial_result, bounded_cleanup。
- triangular/raw 8 (fixture 53-61; producer 3078-3139; checker
  3547-3630): future_ancestry_index, zero_diagonal,
  changed_raw_sparse_entry, changed_ancestry_coefficient,
  duplicate_pivot, wrong_pivot, hidden_smaller_pivot, skipped_P_equation。
- boundary/process 13 (fixture 63-76; producer 4790-4918; checker
  3633-3795): wrong_typed_support, missing_interval, overlapping_interval,
  wrong_t_orientation, changed_accumulator, changed_winner, changed_scalar,
  cross_epoch_frame, blocked_send, partial_worker, dead_worker,
  surviving_process, counter_reset。
- heavy/checkpoint 4 + positive phase gates 2 (fixture 78-87; producer
  5216-5374; checker 4108-4302): heavy_call_before_heavy_digest,
  fabricated_heavy_digest, stale_correction_progress, zero_promoted_to_negative;
  light_resource_checkpoint, heavy_transition。
- selected-correction 30 (fixture 88-118; producer 4454-4512; checker
  3032-3086): selected_q0_roster_state, selected_q0_parent,
  selected_q0_letter, selected_marked_generator, selected_gamma_state,
  selected_gamma_parent, selected_gamma_record, selected_qid, selected_gid,
  selected_cursor_quotient, selected_cursor_remainder, selected_schedule_kind,
  selected_k0_fibre_nonleast, selected_kernel_order,
  selected_heavy_input_identity, selected_section_word,
  selected_coefficient_two_inverse_word, recovery_v1_substitution,
  recovery_v2_corrected_field, recovery_v2_self_seal,
  q0_parent_letter_roster, q3_marked_permutation, one_coordinate_mark,
  gamma_parent_record_word, gamma_projected_970_byte_state,
  gamma_full_vs_projected_substitution, k0_coarse_key_full_blob_least_base,
  kernel_generator_order_cursor_word, product_order, heavy_identity_final_row。
- positive 7 (fixture 120-127; producer 4921-5002; checker 3798-3929):
  omitted_selected_row, changed_selected_row, changed_selected_coefficient,
  wrong_coefficient_two_word, copied_sparse_equality_boolean, changed_target,
  changed_boundary_preimage。
- physical/terminal 11 (fixture 129-141; producer 5005-5213; checker
  3932-4105): symlink_candidate, hardlink_candidate, toctou_substitution,
  unbound_checkpoint, positive_claim_on_resource_exit, separator_flip,
  cofinal_flip, fake_flip, ihara_flip, terminal_reseal, stale_output。

Checker verdict は producer ledgerを採用せず、独自 ledgerを
producer_ledgers_replayed:false, checker_independent_ledger:true,
actual_owner_validators:true, all_fixture_cases:true, executed:true
として構成する (4411-4429)。

## 決定的 R/V constructor

R body は producer 5661-5697。P0/source/frozen、triangular certificate、
light/heavy seal、actual selected H、全 producer mutation ledger、false claimsを
含む。まず semantic_digest = SHA256(canonical(body))、次に
self_digest = SHA256(canonical(body+semantic_digest)) を付け、bounded
exclusive publishする。

V body は checker 4430-4469。physical R の bytes/SHA/self/semantic、
checker-local P0/source/frozen、independent H、derived summary、全 checker
mutation ledger、resource limits/counters、false claimsを含み、R と同じ順の
semantic/self seal規則で exclusive publishする。P0 line 1 の
constructors.R/V.deterministic_field_set はこの top-level field setを事前登録
し、host time/PID/inode/mtime/RSS samples/random/unordered iterationを除外する。

Driver の import-independent artifact gate は canonical+one-LF、self/semantic、
constructor exact field set、candidate envelope、false claims、P0 physical/source/
frozen、raw、V->physical R、H bindingを確認する (192-263)。producer/checker
terminal はそれぞれ
V12A_PRODUCER_TERMINAL V12A_SELFTEST_BOOTSTRAP_ARTIFACT と
V12A_CHECKER_TERMINAL V12A_SELFTEST_BOOTSTRAP_ARTIFACT
(5697, 4469)。driver は各 prefix/full lineを exact-one とし suffixを
byte compareする (174-185)。

## Driver envelope

Mode は外部で D972_R07_A0_V12A_MODE が明示 bindされ、値が
SELFTEST_BOOTSTRAP でなければ shell生成前に停止する (25-31)。
Producer/checker/artifact/outer timeout はそれぞれ
10,800/7,200/3,600/21,600 s (167-173, 190-191, 285)。worker count は固定4。
sleep/retry/poll/pool、workflow edit、driver self pin、R/V hash予測はない。
sentinel は V12A_SELFTEST_BOOTSTRAP_ARTIFACT_READY であり、禁止語
PASS/COMMON/ACCEPTED/A0_COMPLETEを含まない。sentinel は全 gate 後の最後の
writeで、file fsync/no-replace link/directory fsyncを行う (264-284)。

## 未実行値

- Producer measured runtime: UNEXECUTED
- Producer measured RSS: UNEXECUTED
- Checker measured runtime: UNEXECUTED
- Checker measured RSS/allocation: UNEXECUTED
- GHA run id / commit SHA: NONE（workflow/git/networkを実行していない）
- Candidate R bytes/SHA/self/semantic:
  TO_BE_GENERATED_BY_AUDITED_V12A_SELFTEST
- Candidate V bytes/SHA/self/semantic:
  TO_BE_GENERATED_BY_AUDITED_V12A_SELFTEST

V12A BOOTSTRAP MANIFEST:         COMPLETE
IMPLEMENTATION:                  IMPLEMENTED
SELFTEST BOOTSTRAP / GHA:        UNEXECUTED
PRODUCTION / RESUME:             FORBIDDEN UNTIL V12B
FROZEN INPUTS:                   PASS
DETERMINISTIC R/V CONSTRUCTORS:  STATICALLY REACHABLE
SOL(MAX) REAUDIT REQUIRED:       YES
ACTUAL A0 COMMON + CHECKER:      0/1
SEPARATOR / NEGATIVE CLAIM:      FORBIDDEN
LIFT / FAKE / IHARA:             NONE

TASK354_R07_A0_V12A_AUDITABLE_SELFTEST_BOOTSTRAP
