# Task 377 — pre-A0 A3/v4 bounded repair

## 0. Source-static completion boundary

task374 の五つの load-bearing REJECT group だけを、versioned v4 owner で一括修理した。候補、Python、Node、GAP、GHA、workflow、git、network、syntax compilation は一度も実行していない。本返信の `REPAIRED` / `RETAINED` は source-static implementation closure の意味だけであり、runtime terminal、mutation observation、RSS 又は数学的 A3 numerator の観測ではない。fresh independent Sol(max) static code/performance audit が終わるまで GHA は禁止である。

## 1. Versioned owners and one-way seal graph

| frozen machine owner | bytes | physical SHA-256 |
|---|---:|---|
| `ci/in/d972_r07_pre_a0_single_target_a3_v4.prereg.v1.json` | 16,417 | `14ea6de8efac73e71854f6566a9202eb89164ab6b7b5940954e87b3af21ee8ae` |
| `search/d972_r07_pre_a0_single_target_a3_v4.py` | 104,369 | `171e73dab2bd27f638021ceea43d8fb96ec4623a13d45873f364114e4290badd` |
| `crosscheck/check_d972_r07_pre_a0_single_target_a3_v4.py` | 115,675 | `eb07e34164f27b6676b97c722fb0fb2ef87b1e971baaab3d18c26770f17b7804` |
| `search/d972_r07_pre_a0_single_target_a3_gha_driver_v4.g` | 20,111 | `78ee39b6f8926c267cb24d6b15bdc3a961906cdb8ddf9de8f7668222a5113f91` |

第五の指定 owner は本返信 `sol/sol_reply_377_r07_pre_a0_a3_v4_bounded_repair.md` である。physical SHA を本文へ埋めることは自己参照になるため、従来の task370 と同じく post-write exact bytes/SHA-256 を親 session への handoff で報告する。

P0 は compact canonical ASCII、BOM/CR/LF なし、16,417 bytes である。top-level `self_digest_sha256` を除く canonical body は 16,329 bytes、その SHA-256 と宣言 self seal はともに `f1991fa0c232e1d7ea95a211498b4d1741c2104b22271fb90ec1a7ee3af98be7`。schema は exact `d972-r07-pre-a0-single-target-a3/v4/prereg/v1`。両 Python owner はこの P0 の path/bytes/physical SHA/self seal を pin し、driver 15--22 行は P0 と final producer/checker bytes/SHA を pin する。P0 authority から current v4 machine owner への逆辺はなく、graph は `23 immutable authorities -> canonical P0 -> v4 producer/checker -> v4 driver` の一方向である。

read-only PowerShell による P0 recursive ordinary-owner reconstruction は 23 unique paths / 33,121,619 bytes であり、宣言 inventory と全 physical bytes/SHA-256 が一致した。alias、duplicate、missing/extra owner はない。

## 2. F1 — checker evaluator budget API

checker 1433--1444 行の `EvaluatorBudget.check` は、実装済みの `Meter.check` を直接呼ぶ。不存在だった `Meter.check_wall` reference は checker 全文で 0 件である。catch roster は広げていない。したがって frozen task176 が最初の `sid=0` で行う budget check は同じ elapsed meter に到達し、`AttributeError` で ordinary checker route が切れる静的欠陥を除いた。

task198 callable ABI は不変である。六 entry points は `eval/multiply/inverse/source_section/action/section_cocycle`、semantics は `left_then_right`、`actor*value*actor_inverse`、`s_left*s_right*s_product_inverse`。producer direct calls はそれぞれ `3/1/2/1/1/1`（合計 9）、accepted producer transitive calls は `6/4/3/1/1/1`。checker direct callsも `3/1/2/1/1/1`、checker-local reconstructed transitive calls は `8/4/3/1/1/1` である。checker は producer summary を callable evidence に使わず、checker arithmetic、checker joint owner、checker-private Q0 と task198 checker entry pointsから再構成する。

各 roof value は hash-only でなく十個の typed coordinate blobsを保持し、width roster は exact `[40,40,40,40,40,154,154,154,154,154]`。eleven occurrence bindings は ten-index `[0,1,2,3,0,4,5,6,7,8,9]`、sign `[1,-1,1,-1,-1,1,1,1,1,-1,-1]`、orientation `[direct,inverse,direct,inverse,inverse,direct,direct,direct,direct,inverse,inverse]`。ordinal/name は `H1_fxy,H1_fxz,H1_fyz,H2_fux,H2_fxy,H2_fuy,P_b1,P_b2,P_b3,P_b5_inverse,P_b4_inverse` で、full value、width、sign、orientation、ordinal/name/ten-index を producer receipt と independently rebuilt checker verdict の両側に保持し、exact equality と digest を要求する。これは source schema の保持であり、未実行 candidate value の観測主張ではない。

## 3. F2 — one full receipt authentication, small ordinary mutation

producer 657--757 / checker 635--734 行は、recursive `MappingProxyType` + tuple の compact immutable authenticated snapshot と、その producer/checker-local ordinary `validate_task198_binding_snapshot` を独立実装した。snapshot は exact accepted-receipt raw digest/body seal、manifest physical digest/self seal、member、producer/checker attestations、checker verdict、source identities、run/head/artifact/zip acceptance links、および downstream の decoded 11-row ledger/evaluator contract/canariesを保持する。

baseline authority route は producer 760--967 / checker 737--932 行で 31,017,244-byte task198 receipt を各 process 一回だけ JSON parseし、一回の full canonical raw comparisonと一回の body-seal traversalを行う。raw SHA-256 は authority `read_bytes` の一回を `pins[receipt_path]` から再利用し、`authenticate_task198` 内の whole-raw rehash は 0。receipt DOM は snapshot生成後に削除される。

producer 970--1003 / checker 935--969 行の `task198_raw_manifest_binding` は extant 2,722-byte manifest owner の `receipt.sha256` を変え、manifest body sealを再計算し、before/after physical raw SHA inequalityを要求する。その後 baseline と同じ ordinary small-owner validatorへ戻る。validator は canonical/keyset/schemaの後、snapshot の exact receipt binding を manifest seal/digestより先に照合するため、preregistered exact first reason `task198 raw/manifest binding` に到達する。mutation route は receipt rawをindexせず、receipt JSON parse、31-MB canonical traversal、body-seal traversal、whole-raw SHAを一切繰り返さない。detached test-only predicateではない。

small manifest/verdict/attestationの再照合は意図的に ordinary authority routeへ残したが、31-MB ownerの二重処理はない。mutation後は retained raw mapを clear し、31-MB bytesも downstreamへ持ち越さない。

## 4. F3 — immutable baselines and owner-local copy-on-write

producer 1724--1936 / checker 1666--1875 行で `mutation_fixture` は rows、g760、base、central、areas、full task226 ABI、interface、consumer を借用 immutable baseline referenceとして保持するだけで、`deepcopy(reference)` も `deepcopy(p0)` も両全文で 0 件である。全 case は次の局所 replacement だけを作る。

| mutation owner | v4 copy-on-write allocation |
|---|---|
| ledger sign/prefix | 11-reference list + row 0 dict（prefix は新しい小 list） |
| g760 letter | 760-reference list |
| base mode/task192 | base top dict |
| H1/H2/P central | three-reference central top dict + one block dict + its row-reference list + one changed row vector; P0 全体は複製しない |
| projected-area target | task226 の `bar_epsilon_1` top block map と borrowed `literals.relation_words_g` だけ |
| ABI seal target | consumer top dict + `bar_epsilon_1` block map; interface と残り nested owners は借用し、mutant top sealだけ再生成 |
| forbidden flag | eight-flag dict |

untouched baseline は mutation 前に ledger/g760/base/projection seals/central identities/area equality/all-false flagsを ordinary validatorsで通す。raw manifest 1件と上の11件の計12件は、各 real changed owner の before/after digest inequality、ordinary validator、exact first-reason equalityを要求する。`MutationAccepted` は hard status 4、unexpected又は wrong first reason は fail closed。checker central routeは actual checker-local `central rows/sum:H1|H2|P` だけを narrow catchし、それぞれ preregistered `H1_central_row|H2_central_row|P_central_row` に写す。全層で `actual_a3_numerator` を含む8 flagsは falseのままである。

## 5. F4 — one elapsed-adjusted signal envelope

producer 2275--2283 行では Linux hard limitsを先にinstallし、2277行の単一 outer `WallDeadline("complete v4 producer route")` が output preflight、P0/authority、snapshot/mutation、imports、evaluator build/calls、task226 base/area builds、projection/sealing、fixture/COW/all12 validators、task227 closure、receipt sealing、atomic publicationを包含する。checker 2381--2429 行も同様に、2384行の単一 outer checker deadlineが checker-local evaluator reconstruction、projection/mutations、production receipt check、一回の `verify_gate`、verdict sealing/publicationまでを包含する。emergency publicationも producer 2305--2312 / checker 2451--2459 行の独立 internal deadline内であり、残時間がなければ非受理で停止する。

inner deadlinesは既存の詳細 phase attributionを保持する。producer 324--362 / checker 279--317 行の `WallDeadline.__exit__` は prior timerから実 elapsedを差し引いて復元し、prior timerがその間に失効した場合は `ResourceStop`。platformは Linux `RLIMIT_AS`, `SIGALRM`, `ITIMER_REAL`, `renameat2` を必須とし、不足/失敗を accepting routeへ変換しない。

source-derived wall orderingは不変かつstrictで、internal 1,800 s < each external 2,100 s、serial external `2*2,100=4,200` s < workflow 21,600 s。driverは producer/checkerをserialにのみ起動する。

## 6. F5 — durable rollback on the bound directory fd

producer 2044--2115 / checker 2010--2082 行の writer は repo-root -> `ci` -> `out` を `O_DIRECTORY|O_NOFOLLOW` の openat chainでbindし、tempを同じ fd上の `O_CREAT|O_EXCL|O_NOFOLLOW` で作る。成功経路の complete write -> file fsync -> same-dirfd `renameat2(..., RENAME_NOREPLACE)` -> directory fsync は保持した。

typed/untyped failureでは、descriptor closeを試みた後、`renamed` に応じて temp又はfinal basenameを同じ bound dirfdからunlinkし、entryが既に無い場合も含め必ずその directory fdをfsyncしてからclose/re-raiseする。unlink/fsync/close の rollback errorは隠さず `ResourceStop(... rollback)` にして非受理とする。したがって pre-rename write/file-fsync/close/rename failure と post-rename directory-fsync failureの両方で durable removal boundaryが閉じる。

driver 18--22行の final owner pins、exact-one terminals、UNKNOWN拒否、serial terminal equality、receipt/verdict/P0/23-authority/projection/evaluator/mutation/rank/resource cross-bindings、receipt/verdict rehashを保持した。accepted sentinelは driver 207--234行相当の no-follow dirfd chain、exclusive create、file/directory fsync後にだけ exact `D363_V4_ACCEPTED` を持つ。

## 7. Retained task374 PASS clauses

- canonical P0 の23-owner complete acyclic authority graph、accepted task198 receipt `31,017,244 / 82f795...b19f5`、receipt body seal `c8f7e65f...02b9f`、manifest seal `0f630669...3684`、evaluator contract digest `4fc38881...8b8`、11-row ledger digest `040ab853...cd7` を保持した。
- v303-only projection allowlist と task227 consumer `schema/modulus/ten_to_eleven/occurrences/bar_epsilon_1/u0` を保持し、full package、`B_a`、PB-chain fields、literals、task192 ancestryをclosure inputへ入れない。presence-only `rword_f/rword_g` は exact `V303_OMITTED_NOT_CONSUMED`。
- source call-site scanは producer `t227.closure(...)` 1件（2207行）、checker `verify_gate(...)` 1件（2286行）、opposite-side call 0件。486 ideal rows、729 translates、rank/echelon/ancestry、MEMBER replay又はNONMEMBER dual evidenceをcomplete gateで要求する。frozen verifier内部の span comparisons 12 と wrapper reverse comparisons 0 の区別も維持した。
- baseline + 12 real ordinary mutations、exact narrow first reasons、全 conclusion flags falseを保持した。
- driverは accepting-only serial route、exact terminal/cross-bindings、bounded no-overwrite publicationとdurable sentinelを保持した。current v3 receipt/verdict/path alias referenceは driver/両Pythonで0件。

## 8. Recomputed resource and avoidable-work inventory

| bounded quantity | v4 source formula | exact bound/cap |
|---|---|---:|
| immutable authority | recursive 23-owner sum | 33,121,619 bytes |
| P0 + authority | `16,417+33,121,619` | 33,138,036 < authority cap 40,000,000 |
| producer six imported sources | exact source-size sum | 894,133 bytes |
| producer input | `16,417+33,121,619+2*894,133` | 34,926,302 < 60,000,000 |
| checker seven imported sources | exact source-size sum | 1,450,252 bytes |
| checker before production receipt | `16,417+33,121,619+2*1,450,252` | 36,038,540 |
| checker with max receipt | `36,038,540+19,000,000` | 55,038,540 < 60,000,000 |
| producer normal fixed-point transient | `3*19,000,000+65,536` | 57,065,536 bytes |
| failed-normal + emergency cumulative charge | `57,065,536+(3*65,536+65,536)` | 57,327,680 bytes, cap exact |
| checker verdict fixed-point transient | `3*1,000,000+65,536` | 3,065,536 bytes |
| checker private Q0 | `5*1,469,664`; construction `2*` | 7,348,320; peak component 14,696,640 bytes |
| hard total address space | Linux `RLIMIT_AS` | 4,294,967,296 bytes |
| wall | internal / each external / serial / workflow | 1,800 / 2,100 / 4,200 / 21,600 s |

全23 authority ownersは一回ずつphysical read/hashする。動的 sourceはその後、compile/exec用 pre-read/hash と post-read/hashを一回ずつ行い、module loaderの隠れたreadは0。task198 31-MB ownerは各 sideで physical read/hash 1、DOM 1、full canonical raw comparison 1、body-seal canonical traversal 1で、raw mutationによる追加 full-size passは0。小 manifestはordinary baseline/snapshot validatorとmutant validatorで再構成するが、31-MB raw/DOMを参照しない。

task226は各 sideで base build 1 + projected-area builds 3。producer closure 1、checker verifier 1。mutation workは各 side exact 12。F3のowner-local lists/dictsは上表のreference/vector幅だけで、full task226 ABI/reference bundleをcaseごとに複製しない。

serializerの `3N+65,536` は同時生存するold encoded bytes/new JSON text/new encoded bytesとstreaming chunkのsource chargeである。task198 DOM、loaded modules、task226 structures、closure/verifier structuresのPython-object実 peakをpayload byte数と同一視しない。これらのtotal hard upper boundaryは4-GiB `RLIMIT_AS`、RSS samplesはboundary telemetryだけでin-call interruptの証拠ではない。この便は未実行なのでactual RSS/timeを報告しない。

## 9. Commands deliberately not run

実行したのは指定 ownerのread-only PowerShell全文/byte/SHA/inventory inspection、text patch、P0のPowerShell canonical formattingだけである。Python、Node、GAP、GHA、candidate producer/checker/driver、workflow/GitHub Actions、git、network、compile/py_compile/AST syntax checkは実行していない。`ci/out` のv4 candidate receipt/verdictも作成されていない。

A3/V4 VERSIONED OWNERS:                COMPLETE
TASK374 F1 CHECKER BUDGET API:          REPAIRED
TASK374 F2 DUPLICATE 31-MB PROCESSING:  REPAIRED
TASK374 F3 FULL-REFERENCE DEEPCOPY:     REPAIRED
TASK374 F4 INTERNAL DEADLINE COVERAGE:  REPAIRED
TASK374 F5 PRE-RENAME ROLLBACK FSYNC:   REPAIRED
TASK374 RETAINED PASS CLAUSES:          RETAINED
CANDIDATE EXECUTION:                    UNEXECUTED
FRESH INDEPENDENT STATIC AUDIT:         REQUIRED
PRE-A0 A3/V4 GHA:                       FORBIDDEN
ACTUAL A3 NUMERATOR:                    remains 0/3
A0 / COFINAL LIFT / FAKE / IHARA:       NONE

TASK377_R07_PRE_A0_A3_V4_BOUNDED_REPAIR
