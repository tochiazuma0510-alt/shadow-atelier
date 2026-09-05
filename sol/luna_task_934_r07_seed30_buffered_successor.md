# Task934/935 — minimum buffered-read successor

Root authorizes a versioned correction of one identified I/O setting while
preserving the executed v1 sources and workflow. No arithmetic changes.

1. Task929 worker owns only new
   `search/d972_r07_actual_seed30_materializer_v2.py` and
   `sol/luna_reply_934_r07_seed30_buffered_successor.md`.
   Copy frozen producer v1 via apply_patch, changing ONLY the P1 instruction
   stream's `buffering=0` to `buffering=1 << 20`. Keep binary cache reading,
   schema/ABI, all constants/arithmetic/selection, tests and output unchanged.
   Report the exact one-line diff, bytes and SHA; no local execution.
2. Task930 worker owns only new
   `.github/workflows/d972-r07-actual-seed30-materializer-v2.yml` and
   `sol/luna_reply_935_r07_seed30_buffered_workflow.md`.
   Copy v1 with only workflow/marker/artifact names, producer v2 path and
   producer SHA/bytes updated. Checker v1 and its pin remain unchanged.
   No new tests, gates, generic framework or historical rerun.
3. Root reviews this one-line fix and frozen pins, and alone decides whether
   to cancel/replace run33946247365. No worker git/network/credentials/GHA.
   The unbuffered line reader is a concrete avoidable hotspot; exact time
   spent there has not been profiled and must not be invented.
