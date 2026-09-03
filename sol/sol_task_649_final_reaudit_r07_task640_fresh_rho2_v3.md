# Sol(max) Task649: final bounded release re-audit of Task640 v3

Role: Sol mathematical/code auditor.  Read this complete mail, the complete
Task646 reply, Task648 instruction/reply, and audit the exact frozen quartet.
Write only `sol/sol_reply_649_final_reaudit_r07_task640_fresh_rho2_v3.md`.
Do not implement, edit inputs, run production/GHA, use git, or add optional
design requirements.  This audit is limited to the three Task646 blockers and
regression of the already-passing R1/R3/R4/R5/R7 gates.

## 1. Exact frozen quartet

| file | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 27,474 | 304 | `060202458e8643acb1ed42d2ad94b9f192406c57b803dc7f3b07897c39115ef7` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 90,762 | 1,548 | `ff3ed7d2287baa807a3577c0f72ddc7f33bce00322d8a581a1d263c393eda774` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml` | 9,974 | 161 | `7f53ca31cac0d2c828a9e1ac57e87f324bd0787c98cbfffb7e9ce9875808858a` |
| `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md` | 2,972 | 58 | `1a2c3584f93e93152de1874cc7ca16d8d9820ed7ee4dedf4b75eab1c35df3243` |

Abort with `INPUT_MISMATCH` if any differs.

## 2. Close only F646-A/B/C

1. **F646-A:** check that producer and checker use exactly the same JSON
   scalar types for the four run/attempt identifiers and that exact parent
   equality remains strict.  Confirm the live selftest rejects both a type
   mutation and an envelope/digest mutation.
2. **F646-B:** check the fixed seven-key filename roster and equality of every
   complete receipt object against independently reconstructed bytes.  Aliases,
   duplicate names and filename/size/digest mutations must be rejected.
3. **F646-C:** trace each new mutation through a helper genuinely used on the
   production path.  Cover manifest header/claims, parent, roots,
   occurrence type/coordinate/sign and slot order, raw-seed-before-cancel,
   typed endpoints, signed inverse/PP/block/prefix/right multiplication,
   nonidentity product, full-signature grouping, direct/occurrence equality,
   target/lower/top/packed/roundtrip, receipts and live leaf parsing.  Tiny
   callbacks/arrays are intended; do not demand production-sized fixtures.

Check the finite `unpack` name-collision repair found by the live packing
fixture: dense packing must call the local trit unpacker, while endpoint
decoding calls `unpack_element`; no call site may silently change authority.

## 3. Regression and decision

Rerun bounded serial `py_compile`, both selftests, YAML safe parse, forbidden
checker shared-exec/import scan and immutable action scan.  Confirm R1/R3/R4/
R5/R7 remain as accepted in Task646, ancestry remains stream-only, replay is
bucket-only, caps are live, all later claims are false/null, and the workflow
is still inert under `false &&`.

Return exactly:

- `PASS`, `SAFE_TO_DISPATCH_GHA=yes` if the three concrete blockers are closed;
  or
- `FAIL`, `SAFE_TO_DISPATCH_GHA=no` with only a concrete release counterexample.

A PASS authorizes one fresh-rho2 GHA consumer only.  It declares no residual,
grade2 decision, A0, order 54,432, cofinal lift, fake, Ihara, cross-check or
Lean verification.  Report reply bytes/lines/SHA-256 and `verified=false`.
