# Luna Task915 -- fix checker launch-SHA handoff

Task914 found one fatal wiring omission after Task913: checker
`validate_launch` does not return `launch_sha256`, while `check_output` reads
`base["launch_sha256"]`.  The public actual checker would therefore raise a
`KeyError` after replay.

Modify only:

- `search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py`;
- `sol/luna_reply_908_r07_actual_root_scalar_batch_v1.md`.

Return the SHA-256 of the authenticated exact canonical launch bytes from
`validate_launch`, matching the producer/result contract.  Add a bounded test
that exercises this real handoff rather than only a synthetic dictionary.
Run `py_compile` and both public selftests, update exact receipts, and end the
Task908 reply with `READY_FOR_SOL_REAUDIT=yes`.  Make no other change; do not
run actual parents, GHA or git.
