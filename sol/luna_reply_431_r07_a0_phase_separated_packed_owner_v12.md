# Luna reply 431 — phase-separated packed owner v12

Read the complete task431 brief and `proof_r07_a0_phase_separated_packed_echelon_v407.md`.
Implemented only the four v12 outputs.

The owner keeps occurrence closure and physical insertion in separate phases.
The final re-audit repair adds a durable `frontier_length` equality gate and
requires the occurrence-queue physical echelon to be entirely empty. In every
phase the physical row map, order, expression/source arrays, and packed nnz
counters must agree exactly; physical sources are checked through a single
order-index map for strict processed-prefix order. The positive replay uses
the shared top-level atom helper, applying each prefix with
`for letter in reversed(prefix)`, and the same replay is used for the fresh
physical row and literal ancestry. The checker fixture now includes frontier,
physical-shape, and order mutation rejection.
Stored pivot rows use an owner-local little-endian uint32 registry and aligned
coefficient bytes; candidate rows remain byte-keyed sparse dictionaries. The
payload nnz counters are incremental. Physical rows are not inserted during
occurrence closure; after queue exhaustion, physical rows are built in fixed
occurrence order and consumed occurrence payloads are released. The v11
release migration path is URL/zip/seal pinned and accepts only the registered
checkpoint input, then packs occurrence rows while discarding redundant
physical fields.

The checker independently validates the packed contract, registry/index/order
and pivot normalization, phase-specific physical/occurrence state, queue and
expression/source references, physical source digests, and false claim flags.
Producer and checker now share strict phase gates: unique orders, exact
physical suffixes, processed-prefix PHYSICAL sources, and PHYSICAL-before-action
ordering. Durable output/checkpoint fields are compared phase-by-phase,
including all cursors, frontier length and both payload counters. Checkpoint
seal I/O is streaming and cached; packed uint32 iteration uses memoryview.
The migration constants distinguish the extracted checkpoint (275905469 bytes,
SHA-256 `3ac222801a1a91b8e0f163554835e569a26c2cac0f3f8bea481e1825e5f911b8`)
from its header-excluded gzip payload (275905379 bytes, SHA-256
`36da75dc8e5c21a84b26e35e4adbc9ac47e94f6c1fabbfcddddac03fd81d7ddf`).
Migration discards physical state before packing occurrence rows, seals that
same v12 state before runtime bootstrap, and resumes by explicit phase.

Final pins:

- `search/d972_r07_a0_pb34_direct_quotient_owner_v12.py`: 51884 bytes, SHA-256 `3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3`
- `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v12.py`: 13334 bytes, SHA-256 `e6a16f63725cd23bb1cd8469e2a0d93c7774c979079b7314b653b7ffa439f891`
- `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v12.g`: 7996 bytes, SHA-256 `924b629340bd3d319b75db1edaa6e7d19a99b9fa5de40dd35719a4cb00eb55cd`

The driver uses fresh v12 paths, requires external
`D972_R07_A0_PB34_V12_RUN:=true`, passes the exact registered v11 release URL,
uses one producer/checker with live `tee`, 9000 seconds, and the 4.8 GB cap.

Bounded local gates:

```text
python -B -c "import py_compile; py_compile.compile(..., cfile=TEMP, doraise=True)"
PASS (exit 0)

python -B search/d972_r07_a0_pb34_direct_quotient_owner_v12.py --mode FIXTURE
R07_A0_PHASE_SEPARATED_PACKED_OWNER_V12 FIXTURE_PASS
PASS (exit 0)

python -B crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v12.py --self-test
R07_A0_PHASE_SEPARATED_PACKED_CHECKER_V12_PASS {"fresh_object_mutation_gates":3,"packed_corruption_gates":4,"phase_mutation_gates":5,"status":"FIXTURE_PASS"}
PASS (exit 0)
```

The requested GAP wrapper parse was attempted; this Windows host's GAP binary
failed before parsing with `fatal error - couldn't create signal pipe, Win32
error 5` (exit `-1073741502`). This is an environment gate, not a producer
run; GHA Linux remains the intended driver target.

The fixture additionally covers the separated-phase suffix/six-action resume
invariants, shared registry and direct packed-parent iteration. No production
search, real migration download, workflow edit, commit, push, or
dispatch was performed.

V12_LOCAL_GO_FOR_PARENT_AUDIT_AND_DISPATCH

## Parent dispatch record (2026-08-31)

The independent Sol re-audit ended in `GO`.  The three executable pins above
were committed without further code changes as
`572dd0b94c77a18abce53328a79fe926ad38e2a1` and pushed to
`sol/r07-explicit-lift-20260825`.

The parent dispatched the unchanged generic workflow `.github/workflows/gap-run.yml`
with the exact inputs

```text
script=search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v12.g
preamble=D972_R07_A0_PB34_V12_RUN:=true;;
out_dir=ci/out
timeout_min=180
with_pquot_packages=false
```

Production identifiers:

- run: `33328233304`
- job: `99302076654`
- immutable head: `572dd0b94c77a18abce53328a79fe926ad38e2a1`
- run URL: `https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/33328233304`

At dispatch recording time the job is `in_progress` in GAP setup.  This is
not yet a migration result, common word, compatible lift, fake numerator, or
Ihara witness.

## Immediate driver repair after run 33328233304

The job stopped before Python or migration. GAP evaluated the one-argument
`Concatenation(" --resume-v11-url ...")` while constructing the migration
argument and raised `Concatenation: arguments must be lists`. The constant
argument is now assigned directly as a GAP string; the conditional resume and
multi-argument command constructions are unchanged. This is a driver-only
repair; producer/checker and workflow were not modified, and no production or
download was rerun.

Updated driver pin: 3125 bytes, SHA-256
`b3921e7c975b5bd4dfd2a581829d6c6497230105218dea1af88f0676f7bb1dc8`.

The parent committed the repair as
`7f0222069de7b6c0db593d05b391d12a9da7662e` and redispatched the same
generic-workflow inputs:

- run: `33328450708`
- job: `99302639103`
- immutable head: `7f0222069de7b6c0db593d05b391d12a9da7662e`
- run URL: `https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/33328450708`

This run passed GAP setup and remained in the GAP/Python production step
beyond the prior one-second stop.  Its mathematical terminal is still
pending.

## Recovery repair for run 33328450708

The preserved checkpoint was inspected without modification: 326449173 bytes,
SHA-256 `0b3169fe6e7051fe46a28bb966ffd3dfeada841dce1a6fe2358959dd99402ff1`,
sequence 40, seed 44, parent 410, action 1640, occurrence rank 1316,
frontier 906, and occurrence payload nnz 155059809. Its only schema defect is
the event label `phase="parent"`; the actual saved state is the occurrence
queue (physical state is empty).

The producer now saves the enclosing canonical phase from `guard(event)`
(`parent`, `resume`, and `six_action` are never serialized as phases). For
recovery, `cp_read` permits exactly one transition from `parent` to
`occurrence_queue`, and only after matching the complete authenticated
checkpoint seal and the recorded cursor/rank/frontier/nnz/shape constants.
Unpinned or malformed phase repairs fail closed; the original checkpoint is
never rewritten.

The driver now recovers the exact six-file release asset before starting the
producer. It verifies the zip (132415389 bytes,
SHA-256 `75223cf534c5864ec32ad895887c16e0ff097ba8871d72162156dc9fdafc863a`),
extracts the registered checkpoint entry, verifies its 326449173-byte seal,
then resumes from `ci/out/d972_r07_a0_pb34_direct_quotient_owner_v12_input.checkpoint`.
Recovery is now performed through fresh temporary paths under `ci/in` and
`ci/out`; the archive is checked for exactly the six registered names with no
duplicates, extras, directories, absolute names, or traversal names. The
registered names are the four v12 artifact/log/checkpoint files plus
`driver.g` and `run.log`.
checkpoint is streamed to a temporary file, both validated files are atomically
renamed into place, and a bound recovery seal is created only afterward.
Any pre-existing zip/input/seal is rejected unless all three are regular,
non-symlink files with matching bytes/SHA, exact roster, and seal contents.
The driver also requires a fresh, distinct recovery receipt path before the
shell command. The receipt is written to a same-directory temporary file and
atomically renamed only after either validation branch succeeds; GAP then
reads and exact-matches its fixed content. A stale seal alone can no longer
make a failed recovery appear successful, including for dangling symlinks.
No workflow edit, upload, dispatch, or heavy local run was performed.

Updated pins:

- producer: 51884 bytes, SHA-256 `3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3`
- checker: 13334 bytes, SHA-256 `e6a16f63725cd23bb1cd8469e2a0d93c7774c979079b7314b653b7ffa439f891`
- driver: 7996 bytes, SHA-256 `924b629340bd3d319b75db1edaa6e7d19a99b9fa5de40dd35719a4cb00eb55cd`

Final driver-only gate: the recovery receipt text is passed as one quoted shell
argument, so GAP's exact one-line comparison is preserved; fresh zip/input/seal
installation rejects both existing paths and dangling symlinks (`! -e` and
`! -L` paired for each path).
