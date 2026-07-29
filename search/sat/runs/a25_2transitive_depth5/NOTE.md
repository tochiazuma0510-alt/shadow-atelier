# a25_2transitive_depth5 run artifacts -- exclusions

Run: https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/30467990745
(`workflow_dispatch`, `run_label=calibration`, CNF sha256
`0408f2d67ab3d64a12032299bd8355715b58a7942ba3f671d9bd82890bfa3286` matching
`search/sat/out/a25_2transitive_depth5.cnf`).

Two files present in the downloaded CI artifact are NOT committed here:

- `problem.cnf` -- byte-identical (same SHA-256,
  `0408f2d6...b0afc28` per `SHA256SUMS.txt`) to the already-committed
  `search/sat/out/a25_2transitive_depth5.cnf`. Omitted to avoid duplicating
  a 35MB file.
- `proof.lrat.gz` -- 260,287,433 bytes, SHA-256
  `bd251e9b83a3831d5856be23a4ea623cd43d41a84609d06fd4dd17f64d7a4d1f`.
  Exceeds GitHub's 100MB per-file hard limit, so it cannot be pushed.
  Kept locally at `scratchpad/a25_2transitive_depth5_proof.lrat.gz` (not
  committed -- scratchpad is gitignored/ephemeral) and reproducible by
  re-running the workflow against the same pinned CNF sha256, or by
  downloading the original CI artifact while it remains available
  (GitHub Actions artifact retention window). `search/sat/tools/../
  lrat_check.py` (the project's independent LRAT checker, see
  search/sat/README.md) has NOT been run against this specific proof --
  only drat-trim's own `s VERIFIED` (see `drat_verify.txt` in this
  directory) has been confirmed for this run.

Everything else in this directory (`result.txt`, `run_label.txt`,
`kissat_out.txt`, `kissat_time.txt`, `drat_verify.txt`, `core.cnf.gz`,
`proof.drat.gz`, `SHA256SUMS.txt`) is the verbatim CI artifact.
