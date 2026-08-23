# Luna 159n/159o producer addendum v2 — Linux NQ portability repair

## 0. Outcome

The first GHA attempt isolated a transport failure, not a mathematical result:

```text
run 32645265812
commit 406917be
Package nq: executable program is not available
Error, PENT159N: nq package unavailable
```

Run `32645293578` was then dispatched with
`with_pquot_packages=true` and finished with the same missing-NQ failure.  The
existing workflow's opt-in block compiles SmallGrp/AutPGrp/ANUPQ/json only; it
does not compile NQ.  Merely changing that flag therefore does not repair the
missing NQ executable.

I preserved every handed v1 byte and created a versioned stage-0 wrapper which
builds the authenticated bundled NQ package inside the GAP process before it
delegates to v1.

```text
PENT159N_NQ_PORTABILITY_V2_DISPATCH_READY
CORRECTED_PENT_CANARIES_UNKNOWN_ENV_OR_RESOURCE_BLOCKED
```

The second token remains the semantic canary status until the v2 GHA stage and
subsequent producer resume actually run.

## 1. Exact repair and fail-closed boundary

`search/d972_pent_interleave_canary_stage0_v2.g` performs these gates in order:

1. Require Linux, exactly one `PackageInfo("nq")` entry, and NQ version
   `2.5.11`.
2. Without `GetEnv`, derive the unique GAP root from `GAPInfo.RootPaths` for
   which `InstallationPath` is exactly one direct child of `<root>/pkg/`.
   Require the trailing slash and exact package-parent equality before any
   shell interpolation.
3. Authenticate the bundled package sources before executing them:

   | NQ source | SHA-256 |
   |---|---|
   | `PackageInfo.g` | `e5e3370aa823163909a5130f1d803f43051e606305915718bcf7a363e5af5264` |
   | `configure` | `4c09599a55cbdf0eb22998280e197f64ebb2e6ca5ca884b80e3e8d55c1ca0bd0` |
   | `Makefile.in` | `84def846c51b5fe54b79b1ca312ac5629c383ccadbe43349da4d40efa9c5d003` |

4. If `DirectoriesPackagePrograms("nq")` has no executable, run exactly

   ```text
   ./configure --with-gaproot=<authenticated GAPInfo.RootPaths root>
   make -j2
   ```

   inside that authenticated package directory.  Configure and make output go
   to separate uploaded logs.
5. Require exactly one executable named `nq` under the package `bin` tree;
   require the GAP package-program lookup to select the same path.  Record the
   generated `Makefile` and executable SHA-256 values and require both to be
   64-character lowercase hex.
6. Require `LoadPackage("nq")=true`.
7. Authenticate the preserved v1 producer as 2,257 bytes / SHA-256
   `c21b7758f244997d1da9c15c3b09b71a13b1995b379596c849a8eacccc202d6d`,
   then `Read` it unchanged.  Its order-128 assertion and identical-law
   semantics remain the load-bearing mathematical calibration.

The wrapper does not replace the fourth dimension subgroup by an ANUPQ
approximation.  It continues to use NQ identical relations `u^4` and
`Comm(u,v)^2` with nilpotency-class bound 3, exactly as v1 preregistered.

No sentinel survives a failed build because the wrapper removes only its six
exact versioned `ci/out` paths before configure/make and writes the sentinel
only after the executable and hash files exist.  A source drift, shell failure,
multiple executable, lookup mismatch, package-load failure, v1 drift, or
order/class mismatch stops before the final v2 marker.

## 2. Existing-workflow dispatch contract

No workflow edit is needed or authorized.  On a commit containing the exact v2
bundle, the parent broker should use:

```text
workflow: .github/workflows/gap-run.yml
script: search/d972_pent_interleave_canary_stage0_v2.g
preamble: <empty>
out_dir: ci/out
timeout_min: 30
with_pquot_packages: true
```

Exact command:

```powershell
gh workflow run gap-run.yml --ref <BUNDLE_COMMIT_SHA> `
  -f script=search/d972_pent_interleave_canary_stage0_v2.g `
  -f preamble='' `
  -f out_dir=ci/out `
  -f timeout_min=30 `
  -f with_pquot_packages=true
```

`with_pquot_packages=true` is confirmed.  It keeps the runner's pinned optional
package gate active; the v2 source independently compiles and authenticates NQ,
which that workflow branch omits.

Expected uploaded files on the missing-executable branch:

```text
ci/out/driver.g
ci/out/run.log
ci/out/d972_pent159n_nq_configure_v2.log
ci/out/d972_pent159n_nq_make_v2.log
ci/out/d972_pent159n_nq_binary_path_v2.txt
ci/out/d972_pent159n_nq_binary_sha256_v2.txt
ci/out/d972_pent159n_nq_generated_makefile_sha256_v2.txt
ci/out/d972_pent159n_nq_build_v2.ok
```

The ordered success markers are:

```text
P2_PACKAGE_LOAD_PASS GAPInfo.Version=4.16.0
PENT159N_NQ_SOURCE_PIN_PASS
PENT159N_NQ_BUILD_PASS
PENT159N_NQ_LOAD_PASS
PENT159N_V1_DELEGATION_PIN_PASS
PENT159N_F2_D4P_CALIBRATION prime=2 order=128 class=3
PENT159N_GAP_STAGE0_PASS
PENT159N_GAP_STAGE0_V2_PASS
```

Any `Syntax error:`, `Error,`, old “executable program is not available”
diagnostic, or missing final marker is failure.  The generic runner has no
script-specific final-marker gate for this new filename, so artifact review
must enforce the list above.

## 3. Immutable selective-publish bundle

New files to publish, and no others:

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_pent_interleave_canary_stage0_v2.g` | 9,639 | `1d68dd33a96572e920398fc14eb70ba6a61d0c3d532f0ba382594d6eebdee67f` |
| `search/certs/d972_pent_interleave_canary_stage0_manifest_v2_20260823.json` | 4,727 | `ba60a00c7373872adb41f77f703b2daf9cd6cf36fbe1e9d02376047997c013ee` |
| `sol/luna_reply_159n_pent_canaries_v2_addendum.md` | self-pin reported after final formatting | self-pin reported after final formatting |

Runtime prerequisite already present on the base commit:

```text
search/d972_pent_interleave_canary_producer_v1.g
2,257 bytes
c21b7758f244997d1da9c15c3b09b71a13b1995b379596c849a8eacccc202d6d
```

The existing workflow is pinned at 11,346 bytes / SHA-256
`7e732a4edf49306e18067b1003b8495c858bfae79ade8855c49488bb7e4dd763`
and was not modified.

## 4. Claim boundary and execution record

This is a portability implementation, not a successful stage-0 measurement.
Local Win32 GAP remains blocked before startup by the signal-pipe error, so the
Linux-only v2 branch was not locally executed.  The GHA run must supply the
generated Makefile/executable hashes and the order/class observation.

Even a complete v2 PASS establishes only that the frozen v1 construction
reproduces $|F_2/D_4^{(2)}(F_2)|=128$ with class 3.  It does not construct the
$PB_4$ quotient, run either pentagon instrument, enumerate the actual-charming
subset, materialize row 36, prove isolation, freeze the interleave, or name
$K_2$.  A producer resume is mandatory.

Checker firewall was preserved.  No checker source, verdict, or report was
opened or imported.  No git, GHA dispatch, workflow edit, es7ops call, main Sol
reply edit, or dovetail mutation was performed by this child.
