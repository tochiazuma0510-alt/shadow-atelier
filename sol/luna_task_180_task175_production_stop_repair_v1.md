# Luna task 180 - task175 production hard-stop observability and repair v1

Commissioner: Sol / 2026-08-27

Role: Luna implementation audit.  This is a bounded mechanical repair of a
prerequisite for the R07 positive common-word search.  It is not a new
mathematical search.

## 1. Observed failure

Task175 repaired SELFTEST passed in GHA run `33042352557`.  Production run
`33042556905` at head
`896676506b62d727a6533a912d555afaac7c248f` ran from
`2026-08-27T05:28:39Z` to `2026-08-27T06:09:36Z`, then failed.

The only public terminal diagnostic was:

```text
Error, task175 missing ci/out/d972_r07_all_seven_raw_bridge_preflight_checker_v1.log
```

Thus the producer command exited nonzero before the checker command was
started.  Its stdout/stderr had been redirected only to an unuploaded file,
so the originating Python exception or resource exit is absent from the GHA
log.  This is a hard implementation/resource stop, not a mathematical
negative result and not a task175 positive receipt.

Current exact runtime identities are:

```text
search/d972_r07_all_seven_raw_bridge_preflight_v1.py
  bytes=57132
  sha256=ef0df11b4aa4efe3fc7b5136e7348c0920609ec9974e2fc918c7bd795deb28ca
crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py
  bytes=79414
  sha256=4b6cd61050bbdfa23c4bb1e0b62b151fb93dec12a64e912b17fc6d320601c228
search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g
  bytes=14797
  sha256=e4fa11d9b1f2ab7f0f0eb6c35c9a15bfa3c1fa5b3db37fefb67cd516273b4b2d
```

## 2. Objective

Statically audit the production producer path and driver shell boundary.
If the originating failure is provable from the source, repair it minimally.
In every case, repair observability so a producer/checker nonzero exit prints
the captured stage log into the GHA step log and leaves an exact stage/exit
diagnostic before GAP performs its fail-closed checks.

The repair must preserve:

1. exactly one serial producer followed by exactly one independent checker;
2. no conversion of Python exceptions, OOM, timeout, or nonzero exit into a
   typed `UNKNOWN` or a receipt;
3. pipefail and the existing 9000-second outer cap;
4. rejection of pre-existing output/log/stage files;
5. exact positive and UNKNOWN terminal contracts; and
6. the existing helper-nonshared checker boundary.

Using `2>&1 | tee <stage-log>` under an exact pipefail shell is acceptable,
provided the original exit status is retained.  A separate ASCII exit-code
file and GAP assertion is also acceptable.  Do not merely pre-create the
missing checker log, since that would conceal the producer failure.

## 3. Static audit targets

Audit at least:

- every production-only call after `run_preflight()` starts;
- the 6,441-row full roster checks and 110-pair Fox replay;
- mutation replay and large receipt serialization;
- tuple/bytes boundaries inherited from task172/task157ee;
- memory-amplifying duplicate reconstruction or JSON copies;
- the precise behavior of GAP `Exec` after a nonzero shell command; and
- whether the approximately 2,457-second stop matches an internal timeout,
  resource cap, or deterministic late exception.

Do not guess a Python root cause that the static source does not prove.  If
the root remains unknown, make the observability repair only and state that
one diagnostic GHA rerun is required.

## 4. SELFTEST contract

Extend bounded SELFTEST/static gates so they prove:

1. a successful producer/checker path still reaches the old exact markers;
2. a deliberately nonzero producer probe exposes one exact producer-stage
   failure marker/log line and cannot run the checker;
3. a deliberately nonzero checker probe exposes one exact checker-stage
   failure marker/log line and cannot emit driver PASS; and
4. no failed probe leaves a positive receipt or verdict.

The probes must be bounded and noncommutative semantics from the existing
fixture must remain covered.  Production programming failures remain hard
nonzero STOPs.

## 5. Files and discipline

You may edit only the minimum needed subset of:

- `search/d972_r07_all_seven_raw_bridge_preflight_v1.py`
- `crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py`
- `search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g`
- `search/certs/d972_r07_all_seven_raw_bridge_preflight_selftest_v1_20260827.json`
- `sol/luna_reply_180_task175_production_stop_repair_v1.md`

Do not edit workflows, task176/task179 files, proofs, or predecessor replies.
Do not run Python, Node, GAP, git, or GHA locally.  Parent alone audits,
commits, pushes, and dispatches.  Keep the GAP driver ASCII-only.  Record a
complete changed-boundary inventory and final bytes/SHA-256 identities in the
reply.

```text
TASK175_PRODUCTION_STOP_REPAIR_V1_IMPLEMENTATION_REQUIRED
```
