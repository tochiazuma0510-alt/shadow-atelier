# Luna reply 157db — frozen 157da same-job GHA driver

Date: 2026-08-18

## Verdict

```text
B345_Q3_GHA_DRIVER_READY
```

The thin fail-closed driver is implemented. It runs the frozen GAP producer and
the independent Python checker in the same generic `gap-run.yml` job. No local
GAP, Python, Git, GHA, package installation, or heavy computation was run.

## Frozen inputs

The driver reads both inputs only after exact `HexSHA256(StringFile(path))`
checks:

```text
search/d972_b345_q3_chief_v1.g
  46827beb2b3cd93a9b29f9431b76ffc9626f7d40307dc2a6733f6900fa955b32

search/check_d972_b345_q3_chief_v1.py
  9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```

No branch, URL, downloaded file, or preamble-controlled shell fragment is used.

## Driver contract

Exactly one literal-`true` mode is accepted. A bound value other than `true` is
not selected, both modes are rejected, and neither mode is rejected.

Self-test mode:

1. reads the frozen producer with `D972_B345_Q3_SELFTEST=true`;
2. removes only its fixed log and sentinel;
3. invokes the fixed Python self-test command exactly once;
4. captures stdout and stderr, then creates the sentinel only through shell
   `&&` after exit zero;
5. echoes the captured log, requires the exact sentinel contents, and counts
   exactly one checker marker with an independent literal substring counter;
6. emits exactly one driver marker.

Full mode applies the same gates after requiring the exact fixed output path and
a nonempty producer artifact. It invokes the checker exactly once on that fixed
artifact and reports its SHA256. The driver does not parse or reinterpret the
producer terminal token; `EXACT_WITH_WORD_CORRECTION`, `MISSING_TYPED_D2`, and
`UNKNOWN_RESOURCE` remain checker-owned.

The four fixed checker paths are:

```text
ci/out/d972_b345_q3_checker_selftest.log
ci/out/d972_b345_q3_checker_selftest.ok
ci/out/d972_b345_q3_checker_full.log
ci/out/d972_b345_q3_checker_full.ok
```

The full producer artifact is:

```text
ci/out/d972_b345_q3_chief_v1.json
```

## Expected markers

Canary checker and final driver markers:

```text
D972_B345_Q3_CHECKER_SELFTEST_PASS
B345_Q3_GHA_DRIVER_PASS mode=selftest
```

Full checker and final driver markers:

```text
B345_Q3_CHECKER_PASS terminal=<checker-owned-token> ...
B345_Q3_GHA_DRIVER_PASS mode=full artifact_sha256=<digest>
```

Each required checker marker must occur exactly once in its captured log. A
nonzero checker exit leaves no success sentinel; the log is echoed before the
driver raises a GAP error.

## Generic-workflow dispatch

Canary:

```powershell
gh workflow run gap-run.yml --ref <COMMIT_SHA> `
  -f script=search/d972_b345_q3_gha_driver_v1.g `
  -f 'preamble=D972_B345_Q3_SELFTEST:=true;;' `
  -f out_dir=ci/out `
  -f timeout_min=20 `
  -f with_pquot_packages=true
```

Full:

```powershell
gh workflow run gap-run.yml --ref <COMMIT_SHA> `
  -f script=search/d972_b345_q3_gha_driver_v1.g `
  -f 'preamble=D972_B345_Q3_RUN:=true;;D972_B345_Q3_OUTPUT:="ci/out/d972_b345_q3_chief_v1.json";;' `
  -f out_dir=ci/out `
  -f timeout_min=330 `
  -f with_pquot_packages=true
```

## File and static audit

| File | Bytes | SHA256 |
|---|---:|---|
| `search/d972_b345_q3_gha_driver_v1.g` | 5,108 | `d44747f24a4d89d86b603ea3b7ec2c166f0e5fe90e235d03ab316047d1b5e135` |

Static inspection found balanced round/square delimiters and balanced
`if/fi`, loop/`od`, and `function/end` tokens after removing comments and string
literals. Both shell commands are fixed source strings, contain exactly one
Python invocation, and remove only their named log/sentinel pair. No execution
or runtime syntax claim is made; the registered canary is the next gate.

No workflow, 157da file, certificate, or mathematical predicate was modified.
