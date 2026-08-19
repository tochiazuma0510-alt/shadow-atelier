# Luna reply 157dx — GAP 4.16.0 source transport repair

## Result

The generic `gap-run` workflow now obtains one SHA-pinned official GAP
4.16.0 full archive and builds it directly with the runner toolchain.  The
optional p-quotient branch discovers, authenticates, builds, and loads the
four bundled packages from that same tree.  It no longer consults an OS
package mirror or downloads separate package archives.

This is transport-only.  No mathematical producer, checker, driver, receipt
schema, predicate, terminal, or frozen v8 source pin was changed.

## Incident record

Runs `32228593650`, `32230091145`, and `32235100873` stopped in the old GAP
setup action before optional packages, the GAP driver, or any v8 code ran.
The common stop was its unconditional Ubuntu mirror refresh; the last run
spent the full 120-minute job limit there.  Consequently none of these three
runs is mathematical evidence of either success or failure.

The frozen input workflow was:

```text
7dc89a8c8e02ee1ce9e025365a8d91e933e0c1c4509398b9135f3ca1545d375e  .github/workflows/gap-run.yml
```

## Exact transport

Controlling source provenance is:

```text
URL     https://github.com/gap-system/gap/releases/download/v4.16.0/gap-4.16.0.tar.gz
SHA256  aaa296b32a5d7bf25fd80f241d23ec1f58b74e991ae730fafe40e54eb3af6e7e
```

The setup block asserts `bash`, `curl`, `tar`, `sha256sum`, `make`, `gcc`,
`g++`, and `nproc`; uses fail-closed shell options; gives curl bounded
connection, total, retry-count, retry-delay, and retry-time limits; hashes
before extraction; recreates the fixed extraction target; builds with
`make -j"$(nproc)"`; exports the exact root; and checks
`GAPInfo.Version = "4.16.0"` before its success marker.

The optional branch searches only one level below the authenticated
`$GAPROOT/pkg` and requires exactly one directory and one `PackageInfo.g` for
each package.  GAP metadata is checked before build against the official
v4.16.0 snapshot:

| package | exact version |
|---|---:|
| SmallGrp | 1.5.4 |
| AutPGrp | 1.12.0 |
| ANUPQ | 3.3.3 |
| json | 2.4.0 |

The controlling archive SHA binds all four directories.  As independent
cross-provenance, the previously pinned standalone archive digests are
ANUPQ 3.3.3
`6a1b25ddcdb05abd933911f8e0e718b195d24b502e5d098d4b431db5f371ffc2`
and json 2.4.0
`ce49399f5f5dc4caf95213f5dd7ec09988f2ae93364817e88ff075a09a22826a`;
the repaired workflow does not fetch either archive.  It builds the bundled
json and ANUPQ sources in place using their shipped `configure
--with-gaproot="$GAPROOT"` followed by parallel `make`.

Each package metadata file SHA is recorded in the build marker.  A separate
GAP process then loads all four packages, repeats the exact GAP/package
version gates, and requires one load marker in that step's captured log.
`GAP_P2_PACKAGE_ROOT` is the authenticated full GAP root.  The later generic
driver's existing load preamble and all existing P2 completion/error gates
remain in place; its root-list transport was narrowed from the obsolete OS
paths to this exact root.

## Exact markers

The source setup emits exactly one line of the following form:

```text
GAP_SOURCE_SETUP_PASS version=4.16.0 release_sha256=aaa296b32a5d7bf25fd80f241d23ec1f58b74e991ae730fafe40e54eb3af6e7e gaproot=<GAPROOT>
```

The optional branch emits one metadata marker, one build marker, and exactly
one load marker in its own load log:

```text
P2_PACKAGE_METADATA_PASS
P2_PACKAGE_BUILD_PASS gap_release_sha256=aaa296b32a5d7bf25fd80f241d23ec1f58b74e991ae730fafe40e54eb3af6e7e smallgrp=<DIR> smallgrp_version=1.5.4 smallgrp_info_sha256=<SHA> autpgrp=<DIR> autpgrp_version=1.12.0 autpgrp_info_sha256=<SHA> anupq=<DIR> anupq_version=3.3.3 anupq_info_sha256=<SHA> json=<DIR> json_version=2.4.0 json_info_sha256=<SHA>
P2_PACKAGE_LOAD_PASS GAPInfo.Version=4.16.0 smallgrp=1.5.4 autpgrp=1.12.0 anupq=3.3.3 json=2.4.0
```

The unchanged generic driver preamble intentionally performs its own later
load and emits its pre-existing second `P2_PACKAGE_LOAD_PASS` line.  Thus
"exactly one" above is scoped to the new independent package-load log, where
the workflow checks the count equals one.

## Static audit

- PyYAML 6.0.3 parsed the final workflow into one `gap` job and five steps.
- All three `shell: bash` bodies begin with `set -euo pipefail` and passed
  `bash -n` under `C:\\Program Files\\Git\\bin\\bash.exe` without executing
  them.
- No GitHub expression occurs inside a Bash body.  GitHub `${{ ... }}`
  expressions remain at YAML boundaries; shell `${...}` expansions were
  parsed by Bash.
- Literal/word-boundary searches found zero instances of the old setup
  action, `sudo`, either former OS GAP root, or either forbidden package
  manager command.
- The optional package body has no downloader or extractor.  Its only package
  inputs are the four directories inside the SHA-authenticated full archive.
- The workflow inputs, `timeout-minutes: ${{ fromJSON(inputs.timeout_min) }}`,
  safe script/output path cases, driver construction, `pipefail`, P2 final
  marker checks, and artifact upload remain fail-closed.  The only later
  runner delta is the transport root narrowing described above.
- Static assertions also fixed occurrence counts for the official URL/SHA,
  setup/build/load markers, four `LoadPackage` calls, upload action, and
  driver `tee` pipeline.

No GAP, Git, GHA, producer, checker, or full computation was run.

## First-run boundary

The first canary must still establish runner-side source/compiler
compatibility and confirm that the bundled json/ANUPQ shipped configure
scripts build on the current `ubuntu-latest` image.  Any missing tool,
directory ambiguity, metadata/version drift, configure/build failure, load
failure, or marker-count drift is a hard workflow failure.  This is a
transport risk only; the repair makes no mathematical claim before the
existing producer and independent checker execute.

## Frozen files

| file | bytes | SHA-256 |
|---|---:|---|
| `.github/workflows/gap-run.yml` | 11,346 | `7e732a4edf49306e18067b1003b8495c858bfae79ade8855c49488bb7e4dd763` |
| `sol/luna_reply_157dx_gap_run_aptfree.md` | REPLY_BYTES=006377 | returned after close |

The reply cannot contain its own ordinary SHA-256 without changing the file
being hashed.  Its exact final byte count and SHA-256 are returned with the
completion handoff.

GAP_RUN_APTFREE_416_READY_FOR_CANARY
