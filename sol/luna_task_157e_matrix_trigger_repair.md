# Luna task 157e — close matrix workflow input trigger

Read `sol/luna_reply_157b_burau_matrix_audit.md` and make the smallest repair.

Authorized files:

- `.github/workflows/d972-burau-matrix-v1.yml`
- `search/d972_b4_burau_matrix_v1.g`
- `sol/luna_reply_157e_matrix_trigger_repair.md`

Do not touch other files, run local GAP, commit, push, or dispatch.

Requirements:

1. Add every dynamically loaded source to `on.push.paths`: the v1 worker and
   its four directly read helper files identified by audit 157b.  Keep the
   existing trigger paths and exact branch.
2. For maximum GAP 4.16 API clarity, replace the prime-field receipt encoder's
   `Int(x)` with documented `IntFFE(x)`; leave the explicit GF(4) encoding
   unchanged.
3. Reparse YAML, recompute hashes, run static path-closure checks and `git diff
   --check`.  Report the exact files changed.  No other semantic or workflow
   change is authorized.
