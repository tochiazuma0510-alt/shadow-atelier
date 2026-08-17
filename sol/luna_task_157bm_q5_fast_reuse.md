# Luna task 157bm — q5 fast lane from pinned q3/q4 calibration receipts

## Role / objective

You are Luna, implementation and GHA support.  Build a **versioned, manually
dispatched fast lane** for the existing exact `d972-burau-tuple-v4` q5 scan.
It must reuse the already-completed q3/q4 calibration artifacts from GitHub
Actions run `32051744038`, rather than recomputing those two hour-scale jobs,
then run the unchanged q5 producer/checker for `a=2` and `a=4` in parallel.

This is urgent because a checker-PASS q5 receipt with even one
`identity_image_defect_count=0` row now has an audited direct finite-quotient
route to terminal B4-A.  An all-pass receipt is still only UNKNOWN and must
not be promoted.

## Frozen calibration identities

The parent independently downloaded the old artifacts outside the repo.
Pin and verify at least these exact receipt hashes before q5 starts:

```text
q3 JSON SHA256 = 0813A151CD47A56F29AAB629EBFC35A0293A8CE84D98C24F3A3AC3E0601AD8E2
q4 JSON SHA256 = 414C13FE680C2EEB6F3F75C7F6A7206A707C18A426DA619543232E1A98855DE2
producer source SHA256 recorded by both = aa872657... (compare the full value
against the current producer; do not trust this abbreviated spelling)
```

Known artifact IDs are `9296644565` (q3) and `9297445824` (q4), both from run
`32051744038`.  Discover and pin their exact artifact names/contents via the
GitHub API or the already-existing workflow contract.  Do not silently select
"latest" artifacts.

## Required work

1. Inspect `.github/workflows/d972-burau-tuple-v4.yml` and the current v4
   producer/checker.  Reuse the same q5 commands, timeouts, resource settings,
   source bindings, marker checks, and artifact retention.
2. Add a new versioned manual workflow, suggested path
   `.github/workflows/d972-burau-tuple-q5-fast-v1.yml`.  It may use the GitHub
   API / `actions/download-artifact@v4` with the exact run and artifact IDs or
   names.  Give only the minimal `actions: read` / `contents: read` permission.
3. Verify both downloaded JSON SHA256 values byte-for-byte and validate their
   internal q/a/status/source metadata before running either q5 job.  A missing,
   expired, renamed, or mismatched artifact must hard-fail, never fall back to
   recalibration.
4. Run q5 `a=2` and q5 `a=4` as separate parallel jobs (or a matrix with
   `fail-fast: false`), with the existing independent checker and lossless
   receipts.  Preserve all 972 row ledgers and expose the zero-row count and
   candidate/all-pass token in the step summary without weakening the checker.
5. Keep production mathematical code unchanged unless an actual interface bug
   makes a tiny versioned wrapper necessary.  Do not alter the tuple semantics.
6. Perform static/YAML validation and only lightweight Python selftests locally.
   **Do not run GAP locally and do not launch any heavy local producer.**

## Soundness gates

- Old run `32051744038` failed only after both calibration producers completed,
  at the obsolete workflow literal-marker gate.  The fast lane may reuse the
  receipt only after exact hash/source/internal-contract checks; do not treat
  the old overall run conclusion as a PASS.
- A q5 candidate is terminal only after its own current checker passes.  Do not
  print a terminal theorem token from the workflow itself.
- Never substitute timeout/OOM/resource failure for a mathematical result.

## Allowed files

- `.github/workflows/d972-burau-tuple-q5-fast-v1.yml`
- if strictly required, new versioned helper(s) under `search/` whose names end
  in `_q5_fast_v1`; do not edit existing production scripts
- reply `sol/luna_reply_157bm_q5_fast_reuse.md`

Do not touch any other file.  In particular preserve the user's dirty
`search/d972_b4_burau_matrix_v1.g` and
`search/check_d972_b4_burau_matrix_v1.py`.

## Reply

Write `sol/luna_reply_157bm_q5_fast_reuse.md` with exact files, validation
commands/results, discovered artifact names and full hashes, risks, and a final
`READY_TO_COMMIT_AND_DISPATCH` or `BLOCKED_<reason>` token.  Do not commit,
push, or dispatch; the parent is the sole broker.
