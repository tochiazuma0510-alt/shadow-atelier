# Task954 producer — full-origin refinement source freeze

Status: source frozen; GHA runtime pending. This file's public ABI section
was shared with Task955; arithmetic remained independent. The two authorized
files are this reply and `search/d972_r07_full_origin_refinement_v1.py`.
No other file was written by this worker.

## Public ABI (2026-09-05)

Schema prefix `d972.r07.full-origin-refinement.v1`. Canonical JSON is ASCII,
sorted keys, compact separators, one trailing LF. `seal(suffix, fields)` adds
`schema=prefix+'.'+suffix`, then `sha256` of canonical JSON without that
field. File references hash complete bytes, including an embedded seal.
Instructions instead use `rolling_sha256=SHA256(parent_head_bytes ||
canonical(instruction_without_rolling_sha256))`.

CLI retains fixed-v2 parent arguments and adds `--packet-root` (the extracted
run33964709359 candidate). `--output`, `--resume`, `--max-appends` (default32,
range0..32), `--max-seconds` (default1800), `--selftest`, and
`--parent-layout-selftest` are public. The latter takes state/delta/seed34/
packet roots and validates actual JSON only. No old numerical replay is used
by that canary. Claims always `candidate:true,cross_checked:false,verified:false`.

`SCOPE={characters:[0,1,2,3],seeds:44,p1_rows:8059,
actors:[1,-1,2,-2],origins_per_character:32280,total_origins:129120,
order:'character-major;seeds0..43;basis_i0..8058;actors1,-1,2,-2',
operational_append_cap:32,mathematical_total_bound:null}`.

`selection` is null or a plain dict with character, origin_id (within that
character), index (=character*32280+origin_id), origin_kind ('seed'/'actor'),
scalar; seed selections add seed, actor selections add basis_i, actor,
actor_slot. First nonzero follows SCOPE order.

Output top level: `owner.json,start.json,source.json,canonical-index.json,
HEAD,result.json,scans/,steps/`. Diagnostics may be `resource-stop.json`,
`.HEAD.pending-*`, `.result.json.pending-*`, `.packet-pending-*`, and other
atomic `.NAME.pending-*` files for the named top-level JSONs. Under scans/
and steps/, only six-digit completed directories and `.pending-*` or
`.orphan-*` diagnostic directories are permitted. Diagnostic tails are never
counted or replayed. The current scan is published before HEAD references it;
a complete step is published before HEAD advances state and clears the scan.

HEAD seal suffix `head` fields: owner_sha256, producer_sha256,
source_sha256, start_sha256, canonical_index_sha256, packet_manifest_sha256,
completed_steps, step_manifest_sha256, current_scan_manifest_sha256,
rank,generation,state_head,kind. Scan number equals completed_steps, starting0.
Steps start1. Cap1's final scan is cached in HEAD and reused on actual resume;
the independent checker recomputes every referenced new scan.

Each scan directory has `manifest.json`, `result.json`, and for c=0..3:
`root-c{c}.bin` (packed36288), `children-c{c}.bin` (4 concatenated packed36288),
`seeds-c{c}.u8` (44 unsigned trits), `actors-c{c}.u8` (8059x4 row-major),
`p1-c{c}.u8` (5x8059 row-major: root then four children),
`actor-lower-c{c}.u8` (8059x4 row-major). Explicit zero files remain for
structurally zero characters. All files are authenticated; there is one P1
cache contraction pass per newly computed complete scan.

Scan manifest suffix `scan-manifest`: scan,owner_sha256,
canonical_index_sha256,rank,generation,state_head,lambda_sha256,files.
File records use `{file,bytes,sha256}` and are sorted by file.
Scan result suffix `scan`: scan,owner_sha256,canonical_index_sha256,
rank,generation,state_head,lambda_sha256,roots,first_hit,declared_pair_count,
informative_pair_count,structural_zero_pair_count,nonzero_pair_count,
active_characters,p1_pass,lower_pass,formula_id,candidate,cross_checked,verified.
Each plain roots item: character,support,packed_sha256,B_adj_identity,
children (plain actor,support,packed_sha256),seed_values_sha256,
actor_values_sha256,p1_values_sha256,actor_lower_values_sha256.
`p1_pass={cache_passes:1,cache_rows:8059,cache_sha256:<accepted>,
instruction_sha256:<accepted>,active_pairings:5*len(active_characters),
chunk_rows:256}`; `lower_pass={body_reads:5*len(active_characters),
blob_passes:12*len(active_characters),maximum_live_bodies:1}`.
Counts use44+8059*4 per active character, with structural-zero skips explicit.

Canonical index seal suffix `canonical-p1-index`: p1_manifest_sha256,
instruction_sha256,cache_sha256,rows(8059),references. Reference records are
the accepted v3 P1 fields, in node order: node,instruction_offset,
instruction_length,instruction_sha256,ancestry_sha256,predecessor,
p1_sha256,row_sha256,origin_sha256,reductions_sha256,scale,
literal_input_sha256. It is metadata only; no decoded full lift matrix.

Each step directory retains fixed-v2 seven files (lambda.bin omitted for
Member), plus `source-d.bin`, `source-full-top.bin`, `materialization.json`.
The full top is four concatenated packed36288, and source-d is the plain
selected character slice. Materialization seal suffix `materialization`:
selection,mode ('immutable-seed-packet'/'complete-filtered-actor'),
source_d_sha256,source_full_top_sha256,lower_zero,components,input,
relation,p1_references,lift_components,direct_pairing,literal.
Components use accepted `{name,shape,trits,support,packed_bytes,packed_sha256}`.
`input` is null for seed; actor input is `{basis_i,p1_reference,
components,full_actor_components,homogeneous_top_sha256,
lower_to_top_sha256}`. `direct_pairing` is null for seed, otherwise plain
`{homogeneous,lower_to_top,full_direct,correction,defect}` scalars.
Actor `relation` seal suffix `actor-relation` fields: basis_i,actor,actor_slot,
raw_events,raw_event_count,raw_event_final_head,final_coefficients,
referenced_nodes,cancelled_nodes. Events retain the accepted v3 keys node,
event_id,body_role,task554_body_sha256,source_character,target_character,
origin_id,term_ordinal,local_index,global_index,coefficient,rolling_sha256;
`node` equals global_index. `referenced_nodes` is sorted raw-event node ids;
p1_references is sorted union of these and the direct basis_i, even if
numeric coefficients cancel. Seed relation/p1_references/lift_components
reuse immutable packet's corresponding accepted receipts.

Actor literal is a plain dict: defect_operation='ordered-product',
actor_conjugation='t*W*t^-1',basis_i,actor,actor_input_p1_sha256,
relation_sha256 (inner seal),canonical_index_sha256 (complete file),
p1_factor_order='event_id-ascending',p1_exponent_rule='(3-coefficient)%3',
literal_coefficient_collection=false,character,projector_receipt_sha256,
actor_path=[],forward_B,source_d_sha256,parent_state_ancestry_premise=true,
normalized_exponent_pair='NOT_REPLAYED',eleven_slot_replay=false,
full_A0_witness=false,grade2_positive_terminal_complete=false.
Seed literal is fixed-v2 literal_reference verbatim.

Instruction fields match fixed-v2 except selected uses the new selection,
packet relation/p1_roots refs are replaced by scan_manifest_sha256,
materialization_sha256,source_d_sha256,canonical_index_sha256. Retained fields:
schema,step,predecessor,offer,generation,rank,lead,sigma,physical_offset,
packet_manifest_sha256,physical_reductions,physical_sha256,target_scalar,
target_remainder_sha256,rolling_sha256.
Step result suffix `step-result` fields match fixed-v2 except scan is replaced
by scan_manifest_sha256 and materialization_sha256. Literal is copied from
materialization. Step manifest suffix `step-manifest` fields:
step,owner_sha256,packet_manifest_sha256,predecessor_step_manifest_sha256,
parent_state_head,state_head,rank,generation,kind,scan_manifest_sha256,files.

Derived rho2 retains accepted base/seed30/seed34 parent records and adds
roles packet-step-1,packet-step-2,packet-step-3 in order, each exact manifest/
result/plain-target complete JSON byte hashes and state_head. The accepted
identity dict extends fixed-v2 with
`packet_steps:'parent_remainder - child_remainder = target.scalar * accepted_packet_normalized_row'`.
New loop steps keep fixed-v2 new_identity_convention and count only new steps.

All manifests use precisely the fields listed above, plus schema/sha256;
there is no redundant file_roster or assurance dict in new manifests.
Step-result retains the fixed-v2 candidate/cross_checked/verified fields.

Start seal suffix `start`: rank,generation,state_head,lambda_sha256,
target_remainder_sha256,parent_layout (old fixed-v2 parent-layout),
packet_parent_layout (new receipt below),accepted_target_derivation_parents.
Owner seal suffix `owner`: formula_id,scope,accepted_packet_owner_sha256,
accepted_packet_manifest_sha256,p1_parent,task554_parent,task712_parent,
task712_manifest_sha256,word_dictionary_sha256,relator_dictionary_sha256.
The old owner metadata is copied unchanged, excluding its schema/seal/scope.
Source seal suffix `source`: producer_sha256,modules,data,python,numpy.
`modules` maps the five accepted producer filenames (fixed-v2 plus its four
MODULE_PINS) to exact SHA256. Data is fixed-v2 DATA_PINS verbatim.

Packet layout seal suffix `packet-parent-layout`: artifact (run33964709359
tuple), entry_files (sorted exact task954 seven file receipts), steps,
rank1359,generation8064,state_head,lambda_sha256,target_remainder_sha256,
old_target_history_replayed=false. Each step plain dict:
role='packet-step-N',step=N,manifest_schema,result_schema,instruction_schema,
instruction_seal='rolling_sha256',target_seal=null,
target_keys=['parent_remainder_sha256','remainder_sha256','scalar'],
target_scalar,manifest_sha256,result_sha256,instruction_sha256,target_sha256,
state_head,parent_state_head,rank,generation,physical_normalized_sha256,
lambda_sha256,target_remainder_sha256. Target SHA hashes the complete plain
target dict, including trailing LF; zero target_scalar remains legal.

Parent-layout CLI plain output: schema=prefix+'.parent-layout-selftest',
status='PASS',metadata_only=true,parent_layout (old fixed-v2 receipt),
accepted_packet_layout (new packet-parent-layout receipt),rejected_cases,
cross_checked=false,verified=false. Rejected cases comprise the five old
fixed-v2 names plus packet-instruction-generic-seal,
packet-target-generic-seal,packet-target-parent,packet-step-chain,
packet-final-head. Workflow may compare both layout receipts across workers.

Terminal result seal suffix `result`: status='PASS',terminal,
head_sha256,packet_manifest_sha256,owner_sha256,completed_steps,rank,
generation,state_head,scan_manifest_sha256,scan (current sealed scan or null),
lambda_rho2 (derived dict for Separator, null for Member),scope,claims,
candidate=true,cross_checked=false,verified=false.
`claims={FULL_ORIGIN_REFINEMENT_CANDIDATE:true,GRADE2_MEMBER:'NOT_DECIDED',
GRADE2_NONMEMBER:'NOT_DECIDED',DUAL_CLOSURES:'NOT_EXECUTED',
A0:'NOT_DECLARED',COMMON:'NOT_DECLARED',COFINAL_LIFT:'NOT_DECLARED',
FAKE:'NOT_DECLARED',IHARA:'NOT_DECLARED',verified:false}`.

`lower_zero` is boolean true. Both input top hashes cover all four character
slices, packed in order. `lift_components` is a sorted list
`[{node,components:[{role,bytes,sha256},...]},...]`. P1 references strip these
lift_components from the accepted packet references. Seed sets include only
raw-event referenced nodes; actor sets also include the direct basis_i.
New-own actor transition events use origin_id=null (there is no old-source
origin id), source_character=target_character=new owner. Old direct uses
origin_id=ORIGIN_RANGES[source][0]+44+4*local+slot; old-to-new uses this same
origin id and target_character=new owner. Event node=global_index.

## F1. Frozen source and implementation boundary

`search/d972_r07_full_origin_refinement_v1.py`: **97,806 bytes**, SHA256
`d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa`.
Task956 independently confirmed this exact byte/hash tuple and reported no
required static source fix through CLI. This is source evidence, not a runtime
PASS. Published fixed-v1/v2 producers and replies remain immutable.

The start adapter reads the exact seven Task954 entry pins, authenticates the
three complete step directories and their chained file-byte hashes, and uses
the accepted own-v2 prefix loader to attach their rows and targets. It checks
current lambda directly against all 1359 rows and both retained target
remainders. It does not rebuild the fixed44 packet, old Conn/P1 closure, or old
insert/target arithmetic. The canonical P1 instruction stream is authenticated
once into a compact metadata index. New scans contract the packed P1 cache
once each in chunks of 256 rows; the index and completed scans are reused on
resume. No full decoded 8059-by-lift matrix is retained.

The own-v541 actor fold retains its complete K_t b_i + T2,t z_i formula. It
releases every prepare/old-body reference before opening the first new body.
Each active character has five body reads and twelve authenticated lower-blob
passes in this producer's schedule. The independent checker's batching schedule
can differ; its mathematical outputs must match all arrays. Selected actor
materialization additionally reads its input owner's lower blob(s), authenticates
the selected/cancelled P1 references, and streams twelve lower blobs for full
lift subtraction. These selected-consumer reads are separate from scan counts.

The selected input passes through `filtered_actor_source`, the own accepted
v15 full actor. The complete actor top is joined to its homogeneous and
lower-to-top scalar components and the globally folded ActRed scalar. All
96776 lower coordinates are required zero before plain character slicing and
B. The direct input and every ordered raw-event reference survive in literal
receipts even when a numerical coefficient is zero. Accepted v518 orientation
is explicitly `t*W*t^-1`; no legacy homogeneous-only generic materializer is
called.

Every current scan includes the full44 seed and8059x4 actor arrays for all four
characters. A completed scan and then a completed step are durable before the
respective HEAD writes. Cap1's postappend scan is bound to the same owner,
source, canonical index, state head and lambda; actual resume loads that scan
without recomputing it. Uncommitted numbered tails are quarantined as named
diagnostic directories. Resume authenticates the full committed prefix and
performs the final direct separator sweep without replaying completed scans or
inserts. The independent checker must recompute every referenced new scan and
new step.

## F2. CLI and focused runtime gates

The producer command shape is:

```sh
python -B search/d972_r07_full_origin_refinement_v1.py \
  --state-root STATE --delta-root SEED30 --seed34-root SEED34 \
  --packet-root FIXED44_V2 --prepare-root PREPARE \
  --block-root BLOCK0 --block-root BLOCK1 --block-root BLOCK2 --block-root BLOCK3 \
  --p1-root P1 --task712-root TASK712 --output OUTPUT \
  --max-appends 1 --max-seconds 1800
```

The actual second invocation uses the same parent roots/output and adds
`--resume --max-appends 32 --max-seconds 1800`. Default/hard append cap32 is an
operational limit, not a mathematical rank or termination bound. The producer
scans after the final permitted append. Internal resource exhaustion preserves
the complete prefix with UNKNOWN_RESOURCE; an early stop before a normal
terminal receipt emits a separate resource-stop diagnostic and exit3. Ordinary
completed-prefix UNKNOWN_CAP/UNKNOWN_RESOURCE results use statusPASS with that
honest terminal. ROOT_ORIGINS_ZERO retains grade2 NOT_DECIDED and unexecuted
dual closures. MEMBER_CANDIDATE retains the complete-word and other final gates.

Focused gate commands:

```sh
python -B search/d972_r07_full_origin_refinement_v1.py \
  --parent-layout-selftest --state-root STATE --delta-root SEED30 \
  --seed34-root SEED34 --packet-root FIXED44_V2
python -B search/d972_r07_full_origin_refinement_v1.py --selftest
```

The actual-parent canary routes the same strict production layout validator
through the actual accepted fixtures and ten malformed cases. It treats a
plain target and rolling instruction as their actual layouts and accepts the
third saved target scalar0. The focused numerical canary calls the production
full-actor path with a forced nonzero lower-to-top term, checks its direct
adjoint pairing and mixed top/lower identity, and rejects the homogeneous-only
value. The durability canary writes complete full-array scan/step payloads,
checks each before-HEAD order, changes the active character from1 to3, resumes
the committed prefix with the cached terminal scan, checks preserved bytes,
and rejects a changed owner and a late actor-array byte corruption.

These commands were **not run locally**. Syntax/import checks, both actual-parent
canaries with equal layout receipts, the focused numerical/durability canaries,
actual cap1 then real resume32, full independent new-array/materializer/step
replay, timings/RSS and the new terminal result remain GHA gates. Task955 owns
the independent checker and workflow; root alone owns release and dispatch.

## F3. Explicit TCB and scope

The producer imports only its own accepted lineage, after source/data pins:

| Source | SHA256 |
|---|---|
| fixed_root_packet_loop_v2 | e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6 |
| actual_root_seed_materializer_v3 | 36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332 |
| rank1355_root_seed_scalars_v1 | 973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb |
| actual_grade2_root_scalar_batch_v2 | 3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856 |
| targeted_grade2_owner_generated_join_v15 | 76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632 |

Names in the table expand as `search/d972_r07_<name>.py`. Raw data pins are
`scratchpad/fuda1_a0_rmax_data.g` (4709 bytes,
625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba)
and `scratchpad/a0_paper_words_v1.json` (115928 bytes,
90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893).
The accepted relator dictionary SHA is
7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8.
Runtime source receipts also name Python/NumPy versions. Task955's arithmetic
helpers were neither read nor imported; only the public ABI above was shared.

The fixed44 parent run is33964709359/1 at
fff114c41bd8748ad0e708919fe0820335c9cce8, artifact9969090590 and the exact ZIP
tuple stated above. Root subsequently reported ruling2125: the accepted fixed44
v2 result is cross-checked within its limits, with three pivots but two changed
target remainders (saved target coefficients1,1,0). This does not grade the new
full-origin implementation or predict its arrays, rank growth or terminal.
M3 remains explicit DERIVED, with base/seed30/seed34 and the three packet target
identities all named. The original rho2 is not claimed directly read here.

No local Python/GAP execution, network, credential, git, dispatch or additional
agent was used by this worker. Source/JSON reads, metadata hashes and static
audits are the local evidence. No new run id or commit SHA was created by this
worker. The whole-word, PB4, other-grade, complete-dual-closure, COMMON, cofinal,
fake and Ihara gates remain outside this bounded implementation. No historical
504 bound is imported.

TASK954_STATUS: SOURCE_FROZEN_RUNTIME_PENDING; cross_checked=false; verified=false.
