# Sol task 370 — pre-A0 A3/v3 complete finite repair

## 0. Static completion and execution boundary

Task369 が REJECT した F1/F2/F5/F6/F7 だけを versioned v3 owner で修理した。F3 の exact v303-only projection / single producer closure / independent checker verifier と、F4 の wrapper 重複なし境界は変更していない。数学的主張、探索宇宙、A0、cofinal lift、fake、Ihara へは広げていない。

この便で使用したのは read-only PowerShell の全文・byte・SHA-256 検査と、指定 owner への text patch、P0 末尾に patcher が付けた単一 LF の bounded final-byte normalization だけである。Python、Node、GAP、GHA、workflow、git、network、candidate program、syntax compilation は実行していない。従って以下は source-static implementation/freeze 報告であり、runtime/RSS/mutation result/closure result ではない。

| frozen machine owner | bytes | physical SHA-256 |
|---|---:|---|
| `ci/in/d972_r07_pre_a0_single_target_a3_v3.prereg.v1.json` | 16,417 | `2660c8e1dce475d19f4d8a40f43626df401d3ca299f34b0f1dd067db896d2ce6` |
| `search/d972_r07_pre_a0_single_target_a3_v3.py` | 95,172 | `436e7c06acff9cf2087277a12067371518c2ce033effaf85bff6b04585c0f9cf` |
| `crosscheck/check_d972_r07_pre_a0_single_target_a3_v3.py` | 106,148 | `eaaa9d602da22921991f25229eed559c50a920a30c3c56495b0954b40af03485` |
| `search/d972_r07_pre_a0_single_target_a3_gha_driver_v3.g` | 20,110 | `63126f5c0c1c2278656a5a2a77fab4d1562af0566e9bca54a85b090cbcc3783e` |

第五の指定 output は本返信 `sol/sol_reply_370_r07_pre_a0_a3_v3_complete_finite_repair.md` である。自己参照を避けるため、その post-write physical identity は親 session への handoff で報告する。

GAP driver は全 20,110 bytes が ASCII、BOM なし、CR 0 である。driver 15--22 行は上の P0 と両 Python owner の exact bytes/SHA を pin する。

## 1. F1 — canonical P0 and complete acyclic authority graph

P0 の read-only ordinal check は次の全条件に一致した。

- physical length = canonical compact-ASCII length = 16,417;
- physical SHA-256 = `2660c8e1dce475d19f4d8a40f43626df401d3ca299f34b0f1dd067db896d2ce6`;
- top-level `self_digest_sha256` を除く canonical body の SHA-256 = declared/pinned self seal = `0539e586fd6001ff65965e990461f390fc8868bb6fbbd0ec2a9cd4464f91df0e`;
- BOM = none, CR = 0, LF = 0, non-ASCII byte = 0;
- first/last byte = `0x7b` / `0x7d`; terminator は `}` で、末尾改行はない。

`authority.g760_ancestry` は key-as-path ではなく、2 個の通常の `{path,bytes,sha256}` record に正規化した。producer 478--517 行と checker 432--471 行の recursive collector は通常 record の literal path/bytes/full SHA shape、path alias、重複、inventory の exact path roster/count/sum、current-v3 cycle を拒否する。producer 578--600 行と checker 533--555 行は collector が返す全 owner を物理 read/hash し、全 dynamic `SOURCE_PINS` が P0 graph に存在することも要求する。driver 155--183 行の generated collector は同じ 23-owner inventory を再構成した後、各 owner を `lstat`、regular/non-symlink、byte count、full physical SHA まで照合する。

完全な authority inventory は 23 unique owners、33,121,619 bytes である。read-only physical inspection では全 23 件が一致した。

| authority owner | bytes | SHA-256 |
|---|---:|---|
| `ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json` | 231,570 | `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json` | 2,722 | `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt` | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json` | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.json` | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt` | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` |
| `crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py` | 35,463 | `e49e4ee24b56e35f8c8120bad7579865e497d94f57b2af51664d562f50ffaa44` |
| `crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py` | 157,253 | `001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1` |
| `crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py` | 34,200 | `028e615bd71276c22cea2180b8ff59e53d8e9ee745c84a1912c862f217f2bb95` |
| `search/check_d972_b345_joint_kernel_qstar_closure_v1.py` | 47,661 | `9e721634d1f16be806e315eec263ec272bc023587f862703c094b7dd37c0111f` |
| `search/check_d972_b345_seedspan_triple4_v1.py` | 574,347 | `ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981` |
| `search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py` | 33,409 | `f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f` |
| `search/d972_b345_joint_kernel_qstar_closure_v1.py` | 67,945 | `06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc` |
| `search/d972_b345_seedspan_triple4_v1.py` | 535,219 | `fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29` |
| `search/d972_r07_760_l3_target6_v1.py` | 53,284 | `7048e73a02e76df5d49fd359c52d5be70ae99d70aa95ebe74b28c4a18f130fde` |
| `search/d972_r07_actual_two_word_endpoint_specializer_v2.py` | 40,556 | `a1532740a7343bd8166c17947f6bd95203a4abdaaafd8e0d9607d3cdf202e6fb` |
| `search/d972_r07_all_seven_extension_section_census_v1.py` | 66,109 | `878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b` |
| `search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g` | 20,541 | `6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068` |
| `search/d972_r07_seven_context_roof_presentation_v1.py` | 137,169 | `6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c` |
| `search/d972_r07_typed_single_seed_endpoint_consumer_gha_driver_v2.g` | 5,387 | `38352fd53e2aa2534e6b4d61c5a613c38fd65c4a6843fa5cb6dd2a04918cfe7d` |
| `search/d972_r07_typed_single_seed_endpoint_consumer_v2.py` | 47,135 | `755ba97e55266bcdb51796cc1a89a562efa782db48475d0e3479e82e325cde8e` |
| `sol/proof_r07_a18_area_invisibility_single_a3_target_v302.md` | 7,340 | `ba508bbe96f34967ebe456c51285ecbe774861a864c369699bbf1dce2b9fc6c3` |
| `sol/proof_r07_pre_a0_computational_base_equivalence_v303.md` | 6,739 | `9868aa26d630138da9b8b963b0f3968e8c2ee698ba4461d596a2b6f155d25cf2` |

依存方向は `23 immutable authorities -> canonical P0 -> producer/checker -> driver` のみである。P0 inventory に P0 自身、current v3 Python、current v3 driver はなく、両 Python は同一 exact P0 を pin し、driver は P0 と両最終 Python identity を pin するため、graph は acyclic である。

## 2. F2 — accepted evaluator is actually exercised

producer は authenticated source bytes を loader に再読させず `compile(raw)` / `exec` し、accepted task198 producer の live `v188_consumer_action_abi()` registry を取得する（producer 1201--1207 行）。q3 arithmetic、31 contexts/46 uses、26 correction words、243-state Gamma、59,049-state fine deletion、projection、必要な 2-state Q0 section support を producer 1107--1176 行で組み立てる。

producer の ordinary direct call sites は 1219--1227 行である。

| operation | direct arguments/use | exact direct calls | accepted transitive calls |
|---|---|---:|---:|
| `roof_eval` | `g760`, `[1]`, `[2]` | 3 | 6 |
| `roof_multiply` | `x,y` | 1 | 4 |
| `roof_inverse` | `x`, `eval(g760)` | 2 | 3 |
| `roof_source_section` | state ids `(2,2)` | 1 | 1 |
| `roof_action` | actor `[1]`, value `eval([2])` | 1 | 1 |
| `roof_section_cocycle` | `[1]`, `[2]`, `[1,2]` | 1 | 1 |

checker は producer summary を evaluator input にしない。独立 task198 checker functions `checker_eval/multiply/inverse/source_section/action/section_cocycle` を checker 1395--1402 行で直接束ね、checker arithmetic orientation と independent joint group、checker-private Q0 section data を 1309--1368 行で再構成する。direct call sites は checker 1416--1424 行、direct roster は同じ 9 calls、accepted checker-side transitive roster は eval 8 / multiply 4 / inverse 3 / source-section 1 / action 1 / cocycle 1 である。

両側は full ten-coordinate values を `direct_values` に保持し、11 occurrence ごとに ordinal/name/ten-index/sign/orientation/width/value を `occurrence_values` に保持する。E3 は 40-byte、E4 は 154-byte width を要求し、factor sign と direct/inverse orientation を各行で一致させる。checker verdict は checker が再構成した full direct values、exact call counts、その digest を保持し、producer digest だけを比較する設計ではない。値そのものは candidate 未実行のため本返信では観測値として主張しない。

## 3. F5 — baseline-first mutation routes

producer 1631--1756 行、checker 1573--1690 行は mutation catch の前に ledger、g760、computational-base reference、projection/consumer seal、central identities、area equality、全 false flags の untouched ordinary baseline を通す。各 mutant は独立 deepcopy owner を実際に変え、before/after digest の不一致を要求する。`MutationAccepted` と wrong reason は narrow expected catch の外で hard failure になる。

| preregistered mutation | extant changed owner | ordinary route | exact first reason |
|---|---|---|---|
| `task198_raw_manifest_binding` | authenticated manifest raw + resealed manifest owner | full `authenticate_task198` manifest/member/attestation/verdict/evaluator-metadata route | `task198 raw/manifest binding` |
| `task198_ledger_sign` | independently built 11-row ledger | `validate_ledger_owner` | `task198 ledger sign` |
| `task198_prefix` | independently built 11-row ledger | `validate_ledger_owner` | `task198 ledger prefix` |
| `g760_letter_digest` | independently reconstructed g760 word | `validate_g760_owner` | `g760 digest` |
| `computational_base_mode` | ordinary base reference | `validate_base_owner` | `computational-base mode` |
| `forbidden_task192_binding` | ordinary base reference | `validate_base_owner` | `task192 binding` |
| `H1_central_row` | P0 H1 row owner clone | actual `central_replay` constructor | `H1_central_row` |
| `H2_central_row` | P0 H2 row owner clone | actual `central_replay` constructor | `H2_central_row` |
| `P_central_row` | P0 P row owner clone | actual `central_replay` constructor | `P_central_row` |
| `projected_area_target` | independently built task226 ABI `bar_epsilon_1.H1` | actual `target_from_fox` closure-input constructor | `projected area target` |
| `ABI_seal_target` | valid consumer ABI, genuinely resealed after mutation | true `validate_projection` seal/derived-only consumer route | `ABI seal/target` |
| `forbidden_conclusion_flag` | complete false-flag owner | `validate_false_flags` | `forbidden conclusion flag` |

raw-manifest mutation は manifest raw の extant `receipt.sha256` を変え、manifest self seal と cloned P0 expected manifest seal を再計算してから full task198 authority validator に戻る。raw/manifest binding check はその full route の末尾なので、parallel copied-fixture equality で先に落とす構造ではない。central と projected target も copied summary comparator ではなく ordinary constructors に戻る。

## 4. Retained F3/F4 clauses

projection は v303-only allowlist `schema/modulus/ten_to_eleven/occurrences/bar_epsilon_1/u0` のままで、full task226 package、`B_a`、PB-chain fields、literals、task192 ancestry を closure input に入れない。`rword_f/rword_g` は frozen task227 が presence だけ読む exact compatibility marker `V303_OMITTED_NOT_CONSUMED` のままである。

producer の load-bearing call は `t227.closure(consumer, closure_budget, structural=None)` の一回だけ（2024 行）、checker の load-bearing call は checker owner の `verify_gate(...)` の一回だけ（2094--2095 行）である。486 ideal rows、729 translates、occurrence/block rank/echelon/ancestry、MEMBER replay または NONMEMBER dual evidence を complete gate に保持する。read-only call-site scan は producer closure 1、checker verifier 1 のみである。

frozen task227 verifier 内の既知 span comparisons 12 は frozen dependency cost として明示し、wrapper reverse comparisons は 0 のままである。wrapper 側に reverse span pass を追加していない。`closure_actions` と `occurrence_support` は CAPS/acceptance から除去し、実 work のない counter を成功条件にしていない。

## 5. F6 — source-derived caps and ordering

| bounded quantity | source formula | exact bound/cap |
|---|---|---:|
| unique authority owners | 23 records | 33,121,619 bytes |
| authority including P0 | `16,417 + 33,121,619` | 33,138,036 < 40,000,000 |
| producer authenticated import sources | sum of six sources | 894,133 bytes |
| producer input | `16,417 + 33,121,619 + 2*894,133` | 34,926,302 < 60,000,000 |
| checker authenticated import sources | sum of seven sources | 1,450,252 bytes |
| checker input before receipt | `16,417 + 33,121,619 + 2*1,450,252` | 36,038,540 |
| checker input with maximum receipt | `36,038,540 + 19,000,000` | 55,038,540 < 60,000,000 |
| producer normal serialized payload | preregistered maximum | 19,000,000; `serialized_bytes` cap 20,000,000 |
| producer normal fixed-point transient | `3*19,000,000 + 65,536` | 57,065,536 bytes |
| emergency transient after failed normal attempt | `3*65,536 + 65,536` | additional 262,144 bytes |
| cumulative serialization peak cap | `57,065,536 + 262,144` | 57,327,680 bytes |
| checker verdict transient | `3*1,000,000 + 65,536` | 3,065,536 bytes |
| checker private Q0 | `5*1,469,664` | 7,348,320 bytes; construction peak 14,696,640 |
| hard address-space limit | Linux `RLIMIT_AS` | 4,294,967,296 bytes |
| wall | internal/external/serial/workflow | `1800 < 2100`; `2*2100=4200 < 21600` seconds |

全 23 authority owner は最初の physical read を authority/input に事前 reserve してから読む。producer 1760--1788 行と checker 1691--1719 行の dynamic loader は authority で既に pin 済みの source を explicit pre-read し、その authenticated bytes を `compile(raw)` / `exec` するため module loader の隠れた source read はない。その後の physical post-read も read 前に input reserve/charge する。従って式の `2*source bytes` は import pre-read + post-read であり、exec read は 0 である。

Linux `RLIMIT_AS` は complete authority/import/build/call より前に hard limit として設定する。authority authentication、task198 authority route、raw mutation、各 import、evaluator build/calls、task226 builds、closure/verifier、sealing/publication は 1,800-second `WallDeadline` の内側である。既存 ITIMER_REAL は経過時間を差し引いた remaining 値で復元し、既存 timer がその間に失効した場合は `ResourceStop` で fail closed する。driver の各 external timeout は 2,100 seconds、二 route は serial 4,200 seconds で 6-hour envelope 内である。

fixed-point sealing は old encoded bytes、new JSON text、new encoded bytes の同時生存を 3N として charge し、streaming chunk 65,536 を加える。RSS sample は hard interrupt の証拠とは称さず、RLIMIT_AS が hard ceiling、sample は boundary telemetry と明記する。

## 6. F7 — bound publication and accepting-only driver

両 Python writer は output を `ci/out` の direct child に限定する（producer 1835--1848、checker 1793--1806）。publication は resolved repo root fd から `ci`、`out` を `O_DIRECTORY|O_NOFOLLOW` の `openat` chain で開き、以後はその bound `out` fd に対して次を行う。

1. `O_CREAT|O_EXCL|O_NOFOLLOW` の dirfd-relative temp creation;
2. complete write、file fsync;
3. source/destination とも同じ bound dirfd の `renameat2(..., RENAME_NOREPLACE)`;
4. bound directory fsync;
5. failure rollback の `unlink(..., dir_fd=directory)` と directory fsync。

pathname は publication では basename にしか使わない。stale final/temp は writer 開始前と no-overwrite rename で拒否する。UNKNOWN や publication failure は accepting process status にならない。

driver は checker 実行後、verdict の pre-validation physical digest `vsha` を validator に渡し、validator 自身が読んだ `vraw` に `sha(vraw)==vsha` を要求する（driver 145--159）。validation 後に physical `vsha2` を再計算して `vsha` と一致させる（205--206）。receipt も checker 後と最終直前に rehash する。terminal mismatch、UNKNOWN、status、canonical/seal、false flags、P0、23 physical owners、projection、rank、mutation、resource telemetry の不一致はいずれも sentinel より前に停止する。

accepted sentinel は全照合後だけ、repo-root/`ci`/`out` の no-follow dirfd chain 上で `O_CREAT|O_EXCL|O_NOFOLLOW` により作る（207--232）。exact `D363_V3_ACCEPTED` を write、file/directory fsync し、write/fsync 失敗時は同じ bound fd から sentinel を unlink して directory fsync してから failure を返す。stale sentinel は driver 冒頭で拒否され、no-overwrite なので置換もしない。

## 7. Conclusion boundary

8 個の `false_conclusion_flags` は P0、receipt top/result/gate、verdict、driver acceptance の全層で完全な false を要求する。特に `actual_a3_numerator=false` は欠落不可である。本便は code/P0/driver の静的 owner freeze のみであり、MEMBER/NONMEMBER、rank、direct evaluator values、mutation outcomes、RSS、GHA terminal は未観測である。fresh independent STATIC PASS が得られるまで GHA は禁止し、actual A3 numerator は 0/3 のまま、A0/cofinal/fake/Ihara へ何も運ばない。

A3/V3 VERSIONED OWNERS:                 COMPLETE
TASK369 F1 AUTHORITY GRAPH:              REPAIRED
TASK369 F2 EVALUATOR EXERCISE:           REPAIRED
TASK369 F3 PROJECTION / CLOSURE:         RETAINED
TASK369 F4 DUPLICATE WORK BOUNDARY:      RETAINED
TASK369 F5 MUTATION ORDINARY ROUTES:     REPAIRED
TASK369 F6 CAPS / PERFORMANCE:           REPAIRED
TASK369 F7 BOUND PUBLICATION:            REPAIRED
LOCAL CANDIDATE EXECUTION:               NONE
PRE-A0 A3/V3 GHA:                        FORBIDDEN PENDING INDEPENDENT AUDIT
ACTUAL A3 NUMERATOR:                     remains 0/3
A0 / COFINAL LIFT / FAKE / IHARA:        NONE

TASK370_R07_PRE_A0_A3_V3_COMPLETE_FINITE_REPAIR
