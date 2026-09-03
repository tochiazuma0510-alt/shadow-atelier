# Luna reply 572 — persistent packed GF(3) stream worker v2

Implemented exactly the four authorized v2 files. This remains a bounded
candidate primitive. Task565 integration, production phases, GHA dispatch,
certificates, and mathematical membership decisions were not performed.

## Output receipts

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_packed_gf3_stream_worker_v2.c` | 18820 | `782f740a56027f2cf9d05456664df610164e1ea2c74c1fe77b2d8d1cd5f4fc25` |
| `search/d972_packed_gf3_stream_worker_v2.py` | 8827 | `864f0105e9ce44d5ad59969f203686c7fd7daa8af2d0cefd183058377e3de551` |
| `search/check_d972_packed_gf3_stream_worker_v2.py` | 12468 | `55a53e792793ca73967ac0f475409a6cb9c01b47296b07f9060919a197ccc28c` |
| `sol/luna_reply_572_r07_packed_gf3_stream_worker_v2.md` | measured after close | measured after close |

The service uses schema/version 2 and fixed little-endian binary files:
`basis.bin` (accepted normalized rows), `leads.bin` (lead and opaque ID),
variable-length `transcript.bin`, `offsets.bin` (record starts plus EOF),
optional synchronized `companion.bin`, and a 296-byte SHA-256 manifest.
The C worker is a persistent framed stdin service: each packed offer returns a
response before the next frame. It retains accepted basis, lead map, one work
row, current reduction list, and bounded protocol state; historical offers and
reductions are streamed to disk. It prints monotone `PROGRESS` records,
authenticates committed prefixes on restart, truncates only uncommitted tails,
rebuilds the lead map, validates transcript chronology/offsets, and commits
the manifest via flushed atomic replacement. Resource exhaustion is typed
`UNKNOWN_RESOURCE`.

The Python client accepts byte-like packed rows, memoryviews and file slices,
has no production timeout or implicit reference fallback, and exposes
one-record transcript parsing and manifest authentication. The reference is
explicitly test-only. The independent checker performs dense-coordinate GF(3)
reduction and uses packing only at the I/O boundary; it imports neither the
wrapper nor the C source.

## Commands and results

```text
$env:PYTHONPYCACHEPREFIX=Join-Path $env:TEMP 'd972-stream-v2-cache'
python -B -m py_compile search/d972_packed_gf3_stream_worker_v2.py search/check_d972_packed_gf3_stream_worker_v2.py
```

Exit 0. The checker was run serially:

```text
python -B -u search/check_d972_packed_gf3_stream_worker_v2.py
```

Exit 0; final pure-run wall time 0.196881 s. Fixture output:

```json
{"checkpoint_resume": "PASS", "companion": "PASS", "compiled_service": "NOT_RUN_NO_COMPILER", "compiler": "none", "dynamic_closure": "PASS", "expression_replay": "PASS", "fixture": "PASS", "frozen_cases": 6, "member_nonmember": "PASS", "mutation_categories": 13, "mutations_rejected": 13, "offset_eof": "PASS", "random_rows": 40, "reference_seconds": 0.201062}
```

Coverage includes all six v4 frozen cases and the chained trace
`[[1,1],[0,2],[2,2]]`; deterministic random/dependent/scale-two/multi-trit/
nonmonotone rows; complete expression and target remainder replay; dynamic
accepted-response closure; checkpoint prefix plus injected-tail protocol
resume; companion reduction, scaling and dependent handoff; and mutations of
basis byte, lead, row ID, coefficient, scale, offset, EOF, manifest hash,
future pivot, duplicate lead, truncation, schema and version. The bounded
reference run reports 40 random rows and 13/13 mutation rejections.

`Get-Command clang,gcc,cc,cl -ErrorAction SilentlyContinue` found no local C
compiler. Thus no compiled service, RSS measurement, or speedup is claimed;
the compiled service fixture is explicitly `COMPILED_SERVICE_NOT_RUN_NO_COMPILER`.
The v2 ABI accepts explicit 64-bit rank/offer/transcript-byte caps without the
v1 static input-size gate, but compiled calibration and large-envelope RSS
remain mandatory. The checker/emulator is not evidence of compiled execution.
The optional companion basis is reconstructed in-process for a fresh service;
compiled companion-resume execution remains an audit item because no local C
compiler was available.

TASK565 INTEGRATION: not performed
CURRENT GRADE-ONE RUNS: unchanged
GRADE-TWO PRODUCTION: not launched
MATHEMATICAL TERMINAL: none
verified=false

PACKED_GF3_STREAM_WORKER_V2_CANDIDATE_AUDIT_REQUIRED
