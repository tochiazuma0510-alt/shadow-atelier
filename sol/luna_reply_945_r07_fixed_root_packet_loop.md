# Task945 / Task947 -- fixed44 packet producer

Producer implementation complete; actual run and independent replay are pending.
No local Python/GAP execution, network, credentials, git, or dispatch occurred.
`cross_checked=false; verified=false`.

## Public ABI v1 (arithmetic-independent contract)

- Schema prefix `d972.r07.fixed-root-packet-loop.v1`; canonical JSON means
  ASCII, sorted keys, compact separators, one final LF. Every sealed object
  hashes its canonical bytes with only its own `sha256` omitted. Receipts
  have `{file,bytes,sha256}`. All hashes are unprefixed lowercase SHA256.
- CLI: `--state-root --delta-root --seed34-root --prepare-root --block-root`
  (four repetitions) `--p1-root --task712-root --output-root`; optional
  `--resume`, `--max-appends` (total committed prefix cap 0..176, default176),
  `--max-seconds` (positive elapsed soft cap), or parent-free `--selftest`.
- `owner.json` (.owner): `formula_id`, `scope`, `p1_parent`,
  `task554_parent`, `task712_parent`, `task712_manifest_sha256` (four),
  `word_dictionary_sha256`, `relator_dictionary_sha256`. Parent roots removed.
  `owner_sha256` everywhere means SHA256 of canonical sealed owner bytes.
  Scope: characters0..3/seeds0..43; order `character-major/seed0-through43`;
  declared_pair_count176; max_appends176; actor_origins_executed0/orbit_rows_executed0.
- `start.json` (.start): exact `rank`, `generation`, `state_head`,
  `lambda_sha256`, `target_remainder_sha256`, `base_manifest_sha256`,
  `seed30_manifest_sha256`, `seed34_manifest_sha256`, `accepted_target_derivation_parents`.
  Each accepted parent has `role`, `manifest_sha256`, `result_sha256`,
  `target_sha256` (hash of complete canonical sealed target), `state_head`.
- `packet/tops.bin`: packed trits, `(character*44+seed)*9072` offset,
  length9072 per 36288-coordinate row; total1596672 bytes.
- `packet/relations.json` (.relations): `event_order`, `seeds` (44).
  Each .seed-relation has `seed`, `raw_events`, `raw_event_count`,
  `raw_event_final_head`, `final_coefficients` (sorted `[node,value]`).
  Event fields and rolling convention are those of accepted v3, including
  cancelled nodes; collection occurs only after the whole raw event seal.
- `packet/p1-roots.json` (.p1-roots): `roots` sorted by node, using accepted
  v3 compact P1-root fields, plus `lift_components` (role/bytes/sha256).
  Include every raw referenced root, including cancelled roots.
- `packet/receipts.json` (.packet-receipts): `raw_seeds`, `seeds`, `p1_pass`,
  `lower_pass`, `regression`, `premises`. Each raw seed (.raw-seed) has seed,
  compact_word, compact_word_sha256, word_dictionary_sha256,
  relator_dictionary_sha256, and accepted v3 component receipts for d0/d1/d2/aux.
  Each seed receipt has seed, lower_width, lower_nonzero_count, lower_zero_count,
  lower_dense_sha256, reduced_components, top_rows. Each top row has character,
  seed, offset, length, sha256, support. v3 component receipt fields unchanged.
- Packet .packet-manifest: owner_sha256, files (four payload receipts),
  file_roster, candidate=true, cross_checked=false, verified=false.
- `steps/000001` etc: physical-raw.bin, physical-remainder.bin,
  physical-normalized.bin, target-remainder.bin, optional lambda.bin,
  instruction.json, result.json, manifest.json. Only complete manifest directories
  form steps. An orphan directory beyond HEAD is an uncommitted tail.
- Instruction (unsealed, rolling hash): schema .instruction, step, predecessor,
  offer, generation, rank, lead, sigma, physical_offset, selected,
  packet_manifest_sha256, relation_sha256, p1_roots_sha256,
  physical_reductions, physical_sha256, target_scalar, target_remainder_sha256,
  rolling_sha256. Selected has character/seed/index/scalar. Rolling hash hashes
  predecessor bytes plus canonical instruction without rolling_sha256.
- Step .step-result: step, kind (Separator/Member), owner_sha256,
  packet_manifest_sha256, parent_state_head, state_head, rank_before/rank_after,
  generation_before/generation_after, selection, scan, pairings (q_d/lambda_G),
  pivot (lead/scale/reductions/normalized_sha256), target (parent_remainder_sha256,
  remainder_sha256/scalar), separator (null for Member), literal, candidate,
  cross_checked/verified false. Selection matches instruction.selected.
- Scan (.root-scan): generation, rank, state_head, lambda_sha256, roots
  [{character,support,packed_sha256,B_adj_identity}], values (4 lists of44),
  declared_pair_count176, nonzero_root_blocks, nonzero_root_block_count,
  informative_pair_count (=44 times nonzero-root count), nonzero_pair_count,
  first_hit (selection or null). No stale fixed active-character assumption.
- Separator: free_coordinate, free_value, lambda_sha256, direct_pairing (v3
  full-row and parent/current remainder fields), lambda_rho2={mode:derived,
  value:1,original_rho2_directly_read:false,accepted_target_derivation_parents,
  newly_executed_target_steps}. The last field is the completed new step count.
  Actual original-rho2 dot is never asserted. Full-word gates remain unfinished.
- Step .step-manifest: step, owner_sha256, packet_manifest_sha256,
  predecessor_step_manifest_sha256 (null for first), parent_state_head,
  state_head, rank, generation, kind, files, file_roster, candidate,
  cross_checked/verified false.
- `HEAD` (.head): owner_sha256, producer_sha256, packet_manifest_sha256,
  start_sha256, completed_steps, step_manifest_sha256 (null at start),
  rank, generation, state_head, kind. Packet and each whole step are durable
  before HEAD advances. Producer resume authenticates these exact pins and
  committed file/rolling joins; checker reconstructs packet/replays new prefix.
- Terminal `result.json` (.result): status PASS, terminal ROOT_SEEDS_ZERO /
  MEMBER_CANDIDATE / UNKNOWN_RESOURCE / UNKNOWN_CAP, head_sha256,
  packet_manifest_sha256, owner_sha256, completed_steps, rank, generation,
  state_head, scan (null only for member), lambda_rho2 (null only for member),
  scope, claims, candidate=true, cross_checked=false, verified=false.
  Even after cap176 the current root scan precedes deciding UNKNOWN_CAP.

### Exact public constants

Scope keys: `characters`, `seeds`, `order`, `declared_pair_count`,
`max_appends`, `actor_origins_executed`, `orbit_rows_executed` with values
`[0,1,2,3]`, `[0..43]`, `character-major/seed0-through43`,176,176,0,0.
Event order is `old-source,then-target/source,stored-term-order`.
Both owner parent descriptors strip `root` recursively.

`p1_pass` keys: manifest_sha256/cache_sha256/instruction_sha256,
instruction_final_head, rows8059, cache_passes1, instruction_passes1,
referenced_roots (raw reference union count), arithmetic_rows (nonzero
coefficient union count). `lower_pass` keys: receipts/full_blob_files12/
blob_passes12/total_authenticated_bytes. Each lower receipt has role,
task554_body_sha256, descriptor, full_file_authenticated=true; role order
old-0-lower/old-0-grade through old-3-lower/old-3-grade then new-0-grade..3.

`regression` has `seed2_char0_raw`={seed2,character0,packed_sha256:
e67d0a0b21aaf41fd1617811b45cd51191a0087c7d04fcc33dda5a58f4fcfca6,
support568,lambda_independent:true,scalar_assertion_retired:true};
`saved_sources`=[{seed30,character0,bytes9072,sha256}, {seed34,...}].
`premises` has complete_defect_lower_zero_executed=true,
v453_direct_slice_after_complete_lower_zero=true,
structural_slicing_retained_as_premise=true, word_projector_replayed=false,
projector_order=[[0,0],[0,1],[1,0],[1,1]], projectors. Each projector has
character/character_label/factors, each factor the unchanged v3 fields
label/pure_word/pure_word_sha256/source_character_sign.

Claims: FIXED_ROOT_PACKET_LOOP_CANDIDATE=true; GRADE2_MEMBER and
GRADE2_NONMEMBER=`NOT_DECIDED`; A0/COMMON/COFINAL_LIFT/FAKE/IHARA=
`NOT_DECLARED`; verified=false.

Accepted target parent roles are `base`, `seed30`, `seed34` in that order.
`lambda_rho2` additionally has `original_rho2_packed_sha256` (the accepted
b41b9e... pin), `accepted_identity_convention`={base:
`rho2 - base_remainder = sum(target.reductions.scalar * base_normalized_row)`,
saved_deltas:
`parent_remainder - child_remainder = sum(target.new_reductions.scalar * saved_normalized_row)`},
and `new_identity_convention`=
`parent_remainder - child_remainder = target.scalar * normalized_row`.
These are retained identity premises for the three named old target receipts;
new target identities and current direct dots are executed. An old separator
dot alone is not the derivation premise.

Step `literal` keys: defect_operation=`ordered-product`, seed,
seed_relation_sha256, p1_roots_sha256, compact_word_sha256,
p1_factor_order=`event_id-ascending`, p1_exponent_rule=`(3-coefficient)%3`,
literal_coefficient_collection=false, character, projector_receipt_sha256
(hash of canonical projector record), actor_path=[], forward_B (identity),
source_d_sha256, parent_state_ancestry_premise=true,
normalized_exponent_pair=`NOT_REPLAYED`, eleven_slot_replay=false,
full_A0_witness=false, grade2_positive_terminal_complete=false.

`source.json` (.source) freezes producer_sha256, modules (the four producer
lineage file/hash pairs), data (the two relative data-file size/hash receipts
below), python (sys.version), numpy (np.__version__). The same source/runtime
and raw inputs must match on resume. It contains no credentials/absolute paths.
Deadline checks occur at parent/table and existing packet body/seed/P1/lower
progress boundaries. A preterminal resource stop returns exit3 and a sealed
`.resource-stop` diagnostic (`status`/`terminal` UNKNOWN_RESOURCE, phase,
complete_prefix_present, head_sha256 or null, candidate=false, false assurance
flags), written to `resource-stop.json` if the output directory already exists.
This diagnostic is not an accepted candidate. A normal between-step stop has
the complete current scan in `result.json`. No cap is reported as an empty root.
Preserved diagnostic tails are `steps/.pending-*`, `steps/.orphan-*`, root
`.packet-pending-*`, and atomic `.<filename>.pending-*`; none count as steps.

## F1. Source freeze and executed contract

New producer: `search/d972_r07_fixed_root_packet_loop_v1.py`, 70509 bytes,
SHA256 `65169d7a26b6daf29152d5afa1352387766ac4024b078caf82a295ca57fbc3fd`.
Only that source and this reply are owned/edited. Old files remain immutable.
No child arithmetic or checker implementation was read/imported/copied.
Coordination was limited to the public schema and receipts above.

The new executable streams all five Task554 bodies once in stored source
order, seals every literal event including cancelled nodes, then folds its
44-by8059 coefficient table. It evaluates the 44 complete raw seeds once,
streams one buffered P1 cache/instruction pass and each of the twelve lower
blobs once, and requires each complete96776-coordinate lower part to vanish.
Each P1 row is decoded at most once, with per-seed bounded F3 scratch; no full
8059-by241928 matrix or broadcasted44-by-full-lift temporary is formed.
Persistent accumulator sizes are top6386688 bytes, lower4258144 bytes, and
coefficients354596 bytes (Task944 formulas); packed top output1596672 bytes.
These sizes do not bound total RSS or runtime: the source context, one decoded
Task554 body, literal events, references, packed state and Python objects also live.

After full subtraction/lower-zero, direct v453 character slices are stored
with raw/component/lower/row receipts and a shared P1-root index. Per-hit
literal records reference this immutable packet, without duplicating its P1
ancestry or re-running the raw evaluator. Seed2's char0 raw SHA/support568
check remains; only the lambda-dependent scalar assertion is retired.
Char0 seed30/34 packet rows must equal the saved actual source-d payload bytes.

The start adapter authenticates Task904 plus the two saved deltas, retains
their insertion order, and directly sweeps the current lambda against all
1356 saved rows and both recent target remainders. Every new loop iteration
derives four fresh B-adjoints and records declared176 pairings separately
from nonzero-root blocks and informative pairings. The first nonzero pair
alone receives forward B, physical reduction, one normalized append, one
target step, and a fresh final lambda/all-row/both-target direct sweep.
The conservative limit remains176; actual packet rank, append count and next
seed are unknown. Historical seed35/36 scalars select nothing here.

Packet completion and whole new steps are fsynced/renamed before HEAD advances.
Resume checks exact owner/start/source/runtime/data/packet pins, the complete
manifest and rolling prefix, loads saved rows/targets/lambda, and directly
checks the final separator before fresh roots. It re-runs neither packet
construction nor completed pivot/target arithmetic. The independent checker
must reconstruct the full packet and replay every new step before acceptance.
Resource expiry before a complete packet leaves diagnostics; resource expiry
after completed steps preserves their HEAD. Signals request a safe stop.

## F2. Module set and retained premises (incremental CV-9)

The executed producer TCB contains the new source above, Python/NumPy/stdlib,
and these four pinned own-lineage modules:

| Module under search/ | Bytes | SHA256 |
| --- | ---: | --- |
| d972_r07_actual_root_seed_materializer_v3.py | 86643 | 36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332 |
| d972_r07_rank1355_root_seed_scalars_v1.py | 31578 | 973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb |
| d972_r07_actual_grade2_root_scalar_batch_v2.py | 118315 | 3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856 |
| d972_r07_targeted_grade2_owner_generated_join_v15.py | 126565 | 76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632 |

The root-scalar-v1 module supplies fixed parent descriptors only; no old scalar
candidate, scalar pass, root q/P1 contractions or old selected-authority path
executes. Materializer-v3 supplies own packing, P1 instruction authentication,
old-state loading, physical reduction/normalization/target update and direct
separator checks. Its fixed-current separator constructor is not used; the new
constructor takes the actual current state. Root-v2 and producer-v15 supply
the accepted source evaluator, Task554/P1/Task712 readers, and adjoint primitive.
No checker module or producer constant monkeypatch is used.

Raw source-data inputs additionally frozen before context construction:

| Relative file | Bytes | SHA256 |
| --- | ---: | --- |
| scratchpad/fuda1_a0_rmax_data.g | 4709 | 625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba |
| scratchpad/a0_paper_words_v1.json | 115928 | 90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893 |

The accepted target identities, fixed canonical lift construction, Task712
table derivation, structural v453 slicing and old state/delta literal ancestry
remain premises. Original rho2 is neither staged nor directly read. The DERIVED
certificate names the exact three target receipts and retains
`rho2 - base_remainder` in the base row span plus the two accepted subtractive
target-delta identities. The new target identities and current direct dots
are executed. An old `lambda(rho2)=1` value is not substituted for those identities.
Whole-word normalized exponent and eleven-slot replay remain unfinished.
This changes the executed-versus-premise contract/TCB and requires incremental
CV-9 after a real run; the new arithmetic is not externally cross-checked yet.

## F3. Fixed actual input tuples

All attempts are1. Root's release broker stages exactly these ten artifacts;
the program authenticates their pinned extracted internal receipts. Archive
metadata below comes from Task944/reply162 and the accepted v3 workflow/source.

| Role | Run | Artifact id | Archive bytes | Archive SHA256 |
| --- | ---: | ---: | ---: | --- |
| Task904 base | 33891714539 | 9944214057 | 107195261 | 2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017 |
| seed30 | 33946247365 | 9963533999 | 915410 | f9627416f0e920fa369f6bc6bb9bffa8c6b15674c0fb7ff37bbebaf77991ace6 |
| seed34 | 33956437467 | 9966542166 | 984053 | a4cb9f63a470636628d9ef02a5b5e55d90fe3b0a2c70f2012d32c9517d87defc |
| P1 | 33851744070 | 9931437113 | 641518300 | 6d6f2ec6eb7f1245b8e7d52645c710ecd519ae0cc442340237d1098c7fa63d5c |
| Task554 prepare | 33677346616 | 9865061266 | 204360988 | da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4 |
| Task554 block0 | 33677346616 | 9865238399 | 81729645 | 2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838 |
| Task554 block1 | 33677346616 | 9865242284 | 82259824 | 849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb |
| Task554 block2 | 33677346616 | 9865193269 | 82200189 | d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d |
| Task554 block3 | 33677346616 | 9865239848 | 82266526 | 87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92 |
| Task712 | 33814194630 | 9915928157 | 22404961 | abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858 |

Source heads: base `7b7b9de20faaa3b8f26e331bb738b374f6f5708c`;
seed30 `7f6dfaddf4150449e62a9b3e85def472fcb41c01`;
seed34 `b9ae78b0950b186463849c3ec874f6474f359851`;
P1 `6673eb2ea15ca6022acc2ddc5a8a204a0380172f`;
Task554 `22c6dddb43d107c05e65f53ad898823ae8ebe276`;
Task712 `5ff2c5a30b604536df12acba8801828a5a7e5fe0`.
Exact names, manifests, source-body/blobs and file-level pins are carried by
the program's inherited fixed descriptors, `SEED34_FILES`, owner/start receipts
and the workflow. No new run id or commit SHA was created by this worker.

## F4. Validation and remaining runtime gates

Only read-only source review and file-byte/SHA metadata checks were performed.
GHA must run syntax checks, source/data pins, the producer/checker canaries,
actual production with cap1, a real second invocation with `--resume` and
total cap176 on the same output, preserved-prefix byte checks, then independent
whole-packet/prefix replay serially. Source/runtime receipts must match the
executed commit and actual Python/NumPy versions. Candidate upload requires
checker PASS; resource/incomplete prefixes remain diagnostic/candidate only.

Producer `--selftest` exercises three changed-interface groups using the actual
append/HEAD/resume functions: nonempty cap/resource classification; complete
step durability before HEAD and prefix roundtrip with diagnostic tails; and
new-lambda active-character change plus wrong-owner rejection. These are
synthetic canaries, not actual-parent claims. They have not run locally.

Reproduction after broker staging (four `--block-root` arguments required):

```text
python -B search/d972_r07_fixed_root_packet_loop_v1.py --selftest
python -B search/d972_r07_fixed_root_packet_loop_v1.py --state-root BASE --delta-root SEED30 --seed34-root SEED34 --prepare-root PREPARE --block-root BLOCK0 --block-root BLOCK1 --block-root BLOCK2 --block-root BLOCK3 --p1-root P1 --task712-root MAPS --output-root OUTPUT --max-appends 1 --max-seconds 1800
python -B search/d972_r07_fixed_root_packet_loop_v1.py --state-root BASE --delta-root SEED30 --seed34-root SEED34 --prepare-root PREPARE --block-root BLOCK0 --block-root BLOCK1 --block-root BLOCK2 --block-root BLOCK3 --p1-root P1 --task712-root MAPS --output-root OUTPUT --resume --max-appends 176 --max-seconds 1800
```

No missing input was found. Numerical packet rank, further appends, next seed,
terminal/root values, timings/RSS and actual checker status remain unknown.
ROOT_SEEDS_ZERO covers only this finite list; MEMBER_CANDIDATE retains unfinished
word gates. No grade2/full-A0, COMMON, cofinal lift, fake or Ihara claim follows.

TASK945_STATUS: SOURCE_FROZEN_RUNTIME_PENDING; cross_checked=false; verified=false.
