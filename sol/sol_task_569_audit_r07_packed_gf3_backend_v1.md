# Sol Task 569: independent audit of the packed GF(3) C backend (v1)

Author: Sol / 2026-09-03

## 1. Role and bounded objective

You are Sol(max), an independent mathematical/implementation auditor.  Audit
the Task567 candidate primitive:

- `search/d972_packed_gf3_echelon_backend_v1.c`;
- `search/d972_packed_gf3_echelon_backend_v1.py`;
- `search/check_d972_packed_gf3_echelon_backend_v1.py`;
- `sol/luna_reply_567_r07_packed_gf3_compiled_backend_v1.md`.

Read all of Task567 first.  Decide whether this is an exact, bounded replacement
for the existing v4 `PackedEchelon` hot loop and a viable primitive for the
Task565 grade-two closures.  Do not audit row 36/648, alter current GHA runs,
or redesign the mathematics.

## 2. Output and execution boundary

Write only `sol/sol_reply_569_audit_r07_packed_gf3_backend_v1.md`.  Do not edit
the candidate, workflows, v220 or certificates; do not commit, push or
dispatch.  Temporary outputs and builds belong outside the repository.  Use
bounded serial tests only.  If no local C compiler is actually available,
perform the complete static audit and pure independent checks and report the
compiled execution as an explicit remaining gate; do not invent timings.

Record input byte sizes and SHA-256 values independently.

## 3. Exact algebra and receipt audit

Check the C code and wrapper line by line for:

1. the exact four-trits-per-byte GF(3) encoding, field operations and v4 pivot
   policy, including scale two, several live trits in one byte, repeated visit
   to a pivot byte, insertion-order pivot IDs and out-of-lead-order pivots;
2. proof/enforcement of the suffix-update invariant (all earlier bytes zero),
   and equality to a full-row AXPY—not merely equality on convenient fixtures;
3. complete per-input reductions, accepted/dependent flag, normalization scale,
   new pivot, target remainder and coefficients, with the same coefficient and
   sign convention as v4;
4. deterministic basis/lead/ledger ordering, opaque row-ID preservation and a
   real deterministic resume boundary;
5. fail-closed schema/version/file-length/byte/lead/offset/integer-overflow and
   allocation-product validation; and
6. claim discipline: it is a linear-algebra primitive only and cannot certify
   source closure, PB gates, MEMBER or NONMEMBER without caller replay/dual.

For each PASS cite functions and line numbers.  For a failure give a minimal
counterexample and classify it as load-bearing or local repair.

## 4. Independence, memory and speed audit

Establish that the checker does not import/share the wrapper or C helpers and
really reconstructs complete receipts with a dense GF(3) reference.  Re-run
the bounded pure fixtures and all mandated mutation gates serially.

Inspect production-scale paths for duplicate full input/basis matrices,
unbounded Python objects, per-pivot process calls, repeated whole-file copies,
quadratic ledger buffering, and missing progress/checkpoint/atomicity.  Give
quantitative upper bounds where the ABI makes them possible.  Distinguish a
correctness blocker, a likely 8-GiB/6-hour blocker, and an optional
optimization.  Do not require cosmetic work.

Also decide explicitly whether Task565 can call the backend once per streamed
phase without changing row order or ancestry, and list the smallest caller-side
integration work still required.  Do not perform that integration.

## 5. Verdict

Return exactly one headline:

```text
PACKED_GF3_BACKEND_V1_AUDIT_PASS_STATIC_COMPILED_GATE_REMAINS
PACKED_GF3_BACKEND_V1_AUDIT_PASS_AFTER_REPAIR
PACKED_GF3_BACKEND_V1_AUDIT_FAIL
```

Even on PASS, no production or mathematical terminal follows and
`verified=false`.

