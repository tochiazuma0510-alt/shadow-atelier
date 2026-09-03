# Sol(max) Task655 — terminal bounded release audit of Task640 v3

## Scope

Read the complete Task649 and Task652 audit replies and Task654 mail/reply.
Independently audit the final frozen Task640 quartet below. This is a terminal
bounded release decision, not a request for optional hardening or redesign.
Do not edit implementation, run production work, dispatch GHA, or use git.

| file | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 27,474 | 304 | `060202458e8643acb1ed42d2ad94b9f192406c57b803dc7f3b07897c39115ef7` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 92,071 | 1,563 | `889b7c7753e53e9c73c5edd575443446b0e3051794d6f20356809244c57cbd32` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml` | 9,974 | 161 | `4d76e057838af7d7c1d6ad28203bdfeec545be36aaf94a815b22bfad58a15f39` |
| `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md` | 2,972 | 58 | `a187b207f4cbf97c0b20fe28c8edd33a39f60cbdf34909a5cfba56000dd4287b` |

Task654 reply: 1,620 bytes / 26 LF lines / SHA-256
`106a1c3f2dad3d9e41df997d206de690e79099517ad6ae5dcd75fb5fdafebe19`.
Stop with `INPUT_MISMATCH` if any value differs.

## Charged checks only

1. Confirm the production negative factor is created through the same
   `signed_base_factor` called by selftest, the negative fixture uses a
   non-self-inverse S3 3-cycle with independently fixed inverse, and replacing
   the negative branch by the base makes selftest fail.
2. Confirm Task652's already-passing ancestry binding, prefix reverse/order,
   and packing-roundtrip live mutations remain effective.
3. Regression-only recheck F646-A/B and R1/R3/R4/R5/R7: exact typed parent and
   fixed receipt names; endpoint/all-seven/direct-occurrence route; streaming
   ancestry; dense/packing replay; claim flags; checker independence; resource
   caps; exact hash pins and immutable actions; inert `false &&` guard.
4. Run bounded serial py_compile/selftests/YAML/import/action/inert checks and
   only tiny charged source mutations if needed. No new audit surface.

Write only `sol/sol_reply_655_final_release_audit_r07_task640_v3.md`, with exact
evidence and one verdict:

- `PASS / SAFE_TO_DISPATCH_GHA=yes`, or
- `FAIL / SAFE_TO_DISPATCH_GHA=no` with one concrete required blocker.

A PASS authorizes only a fresh-rho2 Task640 run. It proves no rho2 value,
grade-two MEMBER/NONMEMBER, A0, compatible cofinal lift, fake, Ihara,
cross-check, or Lean verification.
