# Luna task 157dx — `gap-run.yml` apt-free GAP 4.16.0 transport repair

## Role and scope

This is a transport-only workflow repair authorized by the researcher after
three consecutive GHA canaries stalled before any GAP/v8 execution.  Do not
change any mathematical producer, checker, driver, receipt schema, predicate,
terminal, or frozen source pin.

Authorized worktree changes are exactly:

1. `.github/workflows/gap-run.yml`
2. `sol/luna_reply_157dx_gap_run_aptfree.md`

Do not edit any other file.  Do not run Git, GHA, GAP, or a full computation.
The parent session is the only commit/push/workflow broker.

Frozen starting workflow:

```text
7dc89a8c8e02ee1ce9e025365a8d91e933e0c1c4509398b9135f3ca1545d375e  .github/workflows/gap-run.yml
```

## Incident to close

Runs `32228593650`, `32230091145`, and `32235100873` never reached optional
packages, the GAP driver, or v8 self-test.  The composite action
`gap-actions/setup-gap@v3.8.0` blocked in its unconditional
`sudo apt-get update`; the completed log showed the Ubuntu/Azure mirror stuck
fetching `noble-updates/main amd64 Packages`.  The last run consumed its full
120-minute job limit in the setup step.  Re-running the same action is STOP.

## Required repair

Replace the `gap-actions/setup-gap@v3.8.0` step with a source-literal,
apt-free Bash setup using the official full GAP 4.16.0 release:

```text
URL    https://github.com/gap-system/gap/releases/download/v4.16.0/gap-4.16.0.tar.gz
SHA256 aaa296b32a5d7bf25fd80f241d23ec1f58b74e991ae730fafe40e54eb3af6e7e
```

The full archive is intentional: it binds the package snapshot, including
SmallGrp and AutPGrp, instead of obtaining mutable Ubuntu packages.

The official v4.16.0 `package-infos.json.gz` records this bundled snapshot:

```text
SmallGrp 1.5.4
AutPGrp  1.12.0
ANUPQ    3.3.3
json     2.4.0
```

The setup step must:

- use `set -euo pipefail`;
- use only runner-provided `bash`, `curl`, `tar`, `sha256sum`, `make`, and the
  compiler toolchain; assert required commands before downloading;
- use `curl --fail --location --silent --show-error`, bounded connect/total
  timeouts, and bounded retries including transient connection failures;
- download into `$RUNNER_TEMP`, verify the exact SHA before extraction, and
  extract into a fresh `$RUNNER_TEMP/gap-4.16.0` (or equally fixed) directory;
- configure and build GAP with `make -j"$(nproc)"` without `apt`, `sudo`, or
  any package-manager/network mirror;
- require the resulting `gap` executable, export exact `GAPROOT` through
  `$GITHUB_ENV`, add the executable directory through `$GITHUB_PATH`, and run
  a fail-closed `GAPInfo.Version = "4.16.0"` smoke gate;
- print one unique setup-success marker containing the release SHA.

There must be no `apt-get`, `apt`, `gap-actions/setup-gap`, or Ubuntu package
installation left in `.github/workflows/gap-run.yml`.

## Optional p-quotient package step

Keep the existing `with_pquot_packages` input and branch, but make it entirely
offline with respect to OS/package mirrors after the full GAP archive has been
downloaded.

- Discover exactly one bundled directory for each of `smallgrp`, `autpgrp`,
  `anupq`, and `json` below `$GAPROOT/pkg`; ambiguity or absence is fatal.
- The full GAP archive SHA is the content provenance for SmallGrp/AutPGrp.
- Require SmallGrp `1.5.4`, AutPGrp `1.12.0`, ANUPQ `3.3.3`, and JSON `2.4.0`
  from their actual `PackageInfo.g`/GAP package metadata before accepting
  them.
- Build the bundled JSON and ANUPQ sources in place with their shipped
  `configure --with-gaproot="$GAPROOT"` and `make -j"$(nproc)"`.  Do not
  redownload them and do not call package managers.
- Set `GAP_P2_PACKAGE_ROOT=$GAPROOT` in `$GITHUB_ENV` so the frozen v8 driver
  contract remains satisfied.
- Run a separate fail-closed GAP gate that loads `smallgrp`, `autpgrp`,
  `anupq`, and `json`, checks GAP 4.16.0 and the exact ANUPQ/JSON versions, and
  emits exactly one `P2_PACKAGE_LOAD_PASS` marker.
- Retain enough directory/version/SHA information in the build marker to make
  the transport auditable.  Do not claim package build success merely from
  directory presence.

The later generic `Run GAP script` package-load preamble and the v8 driver's
own package/pin gates must remain fail-closed.  Do not weaken or remove them.

## Static and syntax audit

Without running GHA/GAP:

1. parse the YAML with a locally available YAML parser if one exists; otherwise
   perform a narrowly scoped structural audit and state the limitation;
2. extract each Bash `run: |` block or otherwise audit quoting, `${...}` and
   GitHub `${{ ... }}` boundaries;
3. prove by literal search that forbidden setup strings are absent;
4. verify the existing driver construction, safe-path checks, `pipefail`,
   upload step, workflow inputs, and `timeout-minutes` semantics are unchanged
   except for the transport repair;
5. record final SHA256/bytes for both authorized files and the exact final
   package/setup success markers.

## Reply

Write `sol/luna_reply_157dx_gap_run_aptfree.md` with:

- exact diff scope;
- the three failed run IDs and the fact that no mathematical code executed;
- official GAP URL/SHA and package provenance;
- all static audit results and any remaining first-run risk;
- final hashes/bytes;
- final token on its own last line:

```text
GAP_RUN_APTFREE_416_READY_FOR_CANARY
```
