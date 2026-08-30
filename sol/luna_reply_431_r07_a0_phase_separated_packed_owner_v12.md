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

- `search/d972_r07_a0_pb34_direct_quotient_owner_v12.py`: 50017 bytes, SHA-256 `ff856827e462c9cd09fe6068fed7930b06bbf9de0d04b78e1f20bbf3965063a8`
- `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v12.py`: 13334 bytes, SHA-256 `e6a16f63725cd23bb1cd8469e2a0d93c7774c979079b7314b653b7ffa439f891`
- `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v12.g`: 3125 bytes, SHA-256 `b3921e7c975b5bd4dfd2a581829d6c6497230105218dea1af88f0676f7bb1dc8`

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
