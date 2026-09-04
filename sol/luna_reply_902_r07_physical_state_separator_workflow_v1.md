# Luna reply -- Task902 / R07 physical-state separator workflow v1

Implemented the authorized workflow and no executable, paper, ledger, or
existing workflow was changed.  The workflow remains candidate-only and does
not declare an actual Grade-2 result.

## Exact workflow receipt

| file | bytes | LF | CR | BOM | ends LF | SHA-256 |
|---|---:|---:|---:|---|---|---|
| `.github/workflows/d972-r07-grade2-physical-state-separator-v1.yml` | 20,126 | 405 | 0 | no | yes | `e4ae6b1e7d17e1dc6df3cb7d1470810a535fce4fb8e208239d0614050ca02b78` |

The inherited Task900 executable receipts are unchanged and are rechecked by
the workflow:

```text
search/d972_r07_grade2_physical_state_separator_v1.py
  bytes=75934 LF=1407 sha256=5f1267a7296a6f613f46a1d431c807da22239419362f32ea7c08b51fd7d6e13f
search/check_d972_r07_grade2_physical_state_separator_v1.py
  bytes=57325 LF=734 sha256=01df70e8c6be4bfdff4fbedc227488edce47b1e9c195466ea7658d36b63ee107
search/stage_d972_r07_targeted_grade2_rho2_v9_flat_v4.py
  bytes=29738 LF=659 sha256=ce84baea0bc18380af8a20e32eb8862f9adc20ad596c2012e127f8b7b8341a4b
```

## Frozen authorities

The runtime API gate requires repository `tochiazuma0510-alt/shadow-atelier`,
repository id `1312092366`, completed-success runs, exact attempts, heads,
workflow paths/ids, job/artifact ids, names, archive bytes, digests, exact
expiry timestamps, `expired == false`, and matching source/head repository ids.
The connection parent is run/attempt `33876776771/1`, head
`b44ec9bd078ce0a6ca596a38cfea5012f4fee4d2`, job `101035535909`, artifact
`9939860701`,
`d972-r07-canonical-p1-physical-connection-v11-candidate-33876776771-1`,
`245546516` bytes, digest
`sha256:0c3753d7384a7850aadab41c9ec2755114475862a0b03fd806e875005a72995a`,
expiry `2026-12-03T13:12:28Z`.  The rho2 parent is run/attempt
`33839962829/1`, head `17a8439c766d92719d7ae7d35846ea444da598fa`, workflow
`.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v17.yml`, workflow id
`349904905`, artifact `9925190479`,
`task640-fresh-rho2-v17-33839962829-1`, `6049643` bytes, digest
`sha256:01722bfda081e577195aa6ca9c0bba3425a50dcfd829eca6ac23e33cb5d79ca4`,
expiry `2026-12-03T05:17:47Z`.

The workflow downloads both artifacts by exact run id/name, constructs the
canonical ASCII rho2 acquisition JSON from the API receipts, and invokes the
accepted v4 flat stager into a fresh runner-temp root.  No payload is
hand-copied or partially selected.  The launch binds `fixture_only=false`,
`resume=false`, the exact live parent/final-artifact tuples, accepted parent
producer-v6/checker-v7 identities, accepted stager identity, and fresh
runner-temp connection/rho2/state/output paths.

## Step graph and release gates

1. Checkout; set up Python 3.13; install exactly `numpy==2.5.1`.
2. Query/authenticate both live parents and build canonical rho2 acquisition.
3. Reserve fresh `connection-download`, `rho2-download`, `rho2-flat`, `state`,
   and `output` roots.
4. Download exact connection and rho2 candidates; authenticate all three
   executable source receipts; run flat-stager v4.
5. Prepare the canonical ASCII launch; run compile, producer selftest,
   checker selftest, and producer benchmark once.
6. Run fresh producer with `--run-launch`, then independent checker with
   `--check-launch` only after producer success.
7. Upload unchecked state and all producer/checker/stager/acquisition/launch
   logs under `always()`; checker logs are included even on checker failure.
8. Upload the final candidate only when both named producer and checker steps
   succeed, with compression level `0` and no `verified` label.

Caps are 30 minutes for each producer/checker and 75 minutes for the job;
timeout/resource exits are recorded as `UNKNOWN_RESOURCE` and retain a
nonzero failure, never `NONMEMBER`.  Each phase polls completion every 1
second (so the completion tail is at most about 1 second) while emitting
progress at start and approximately every 60 seconds.  The physical envelope is
`c(c-1)/2 + target + reverse`, with `c=1354` and at most `915981` physical
reductions.  The workflow uses `ubuntu-24.04`, unbuffered Python output and
periodic producer/checker progress logging.

Completed state roster:

```text
physical.bin
physical-p1-coeff.bin
instructions.jsonl
manifest.json
HEAD
```

Final output roster is either
`member-p1-coeff.bin, terminal.json, result.json` or
`lambda.bin, reverse-substitution.jsonl, terminal.json, result.json`.
Unchecked publication additionally preserves both roots, acquisition and
launch receipts, stager/producer/checker logs, periodic progress, and
resource-status receipts.  Final publication includes the completed state,
terminal output roster, and independent checker result only after both steps
pass.

## Local bounded/static receipts

Run outside the repository pycache:

```text
YAML safe parse: PASS (one job)
workflow static: PASS (one marker, 5 gh api calls, caps 30/30/75,
compression-level: 0 twice)
py_compile producer/checker: PASS
producer --selftest: PASS
checker --selftest: PASS (all 19 mutation/control cases rejected)
producer --benchmark: PASS, status=BOUNDED_ONLY
```

The bounded benchmark reported `offers=6`, `physical_rank=3`,
`physical_reductions=2`, `target_reductions=1`, `reverse_substitution=3`,
`operations=6`, and `live_physical_reduction_upper_bound=915981`.  It is not a
production runtime claim.  No GHA dispatch, credentials, Git operation, or
production artifact was used locally.

The sole audited commit marker root should use is:

```text
[task902-r07-physical-state-separator-v1]
```

Claim boundary remains:

```text
ACTUAL_CONNECTION_STATE=false
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
cross_checked=false
verified=false
```

R07_PHYSICAL_STATE_SEPARATOR_WORKFLOW_V1_READY_FOR_SOL_AUDIT
