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
  459c9b1728316a064644ce2e658c0e09dd06b0722fab3e767aaf6f51ebb91d45

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
| `search/d972_b345_q3_gha_driver_v1.g` | 5,108 | `e3883d8f28dc07ddad5088f2b19e4f78680f5953ed7b5e3220e3f0dd892f4da1` |

Canary run `32129602522` at commit
`b40c7fcae815a4fe6e725001496982e24d6198aa` completed setup and reached the GAP
script, then failed after about 1m39s with
`Error, immutable lists cannot be sorted`. The exact cause was the producer's
in-place sort of GAP 4.16's immutable `RecNames` result. The producer now sorts
a `ShallowCopy`; the driver change is only its corresponding producer SHA pin.

Static inspection found balanced round/square delimiters and balanced
`if/fi`, loop/`od`, and `function/end` tokens after removing comments and string
literals. Both shell commands are fixed source strings, contain exactly one
Python invocation, and remove only their named log/sentinel pair. No local
execution or runtime syntax claim is made; the repaired registered canary is the
next gate. The failed run was a serialization mutability bug, not a driver,
checker, ANUPQ, or mathematical predicate failure.

Follow-up canary run `32130140976` at commit
`522dc918e51fe14f5c68ea19620b214e7930ec92` passed that immutable-list point,
then stopped before ANUPQ with
`157da selftest: cross-language formula digest drift`. GAP classifies the empty
list as a string as well as a list, so the producer serialized empty formula
arrays as `""`; Python canonical JSON uses `[]`. The producer now handles the
empty-list case before `IsString`, and this driver pins that repaired producer.
The next GHA canary is the runtime test. No workflow, checker, certificate, or
mathematical predicate was modified.

## 157df atomic-write driver supersession

Canary `32130817181` passed. Full run `32131160061` stopped before ANUPQ at
the first checkpoint because the GAP process lacked the prior rename binding.
The producer now requires the official IO package and a successful
`IO_rename` after closing a same-directory temporary stream. The destination
is not removed first, and any unavailable package/operation/failure result is
fatal.

The self-test branch now creates `ci/out` before reading the producer. After
the read it requires exactly one producer-side atomic-I/O self-test count and
the exact marker
`D972_B345_Q3_ATOMIC_IO_SELFTEST_PASS backend=IO_rename replace=true` before
invoking the independent checker self-test. The producer's direct scan also
has exactly one post-return branch marker, for first typed witness or all 162
exhausted; this is operational reporting, not an A/B verdict.

Current pins:

```text
producer  search/d972_b345_q3_chief_v1.g        76,704  e3dad87ad066fc9c605e1eecaddbe63efd63ac68500e0fcff0d6d62eb7d83af3
driver    search/d972_b345_q3_gha_driver_v1.g     5,463  6a3cb5339468dd7f1b214c67d9791b0f752d0df625f06781470dc24c92a8a859
checker   search/check_d972_b345_q3_chief_v1.py 87,732  9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```

Only I/O, self-test, and direct-scan logging gates changed. Mathematical
inputs, predicates, ordering, terminal mapping, ANUPQ budget, and receipt
acceptance are unchanged. Ready token:
`B345_Q3_ATOMIC_WRITE_REPAIR_READY_FOR_GHA`.

## 157dg checked-write driver supersession

Canary `32132850360` stopped before ANUPQ because the optional I/O package was
unavailable. The producer now performs a core closed write followed by exact
`StringFile` readback; this is a checked-write contract, not an atomicity
claim. The driver gates the exact-one marker
`D972_B345_Q3_CHECKED_IO_SELFTEST_PASS backend=OutputTextFile replace=true readback=true`
before invoking the checker. If the producer is killed or readback fails, the
driver cannot reach the checker or its final success marker.

Current pins:

```text
producer  76,867  b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755
driver     5,488  93a03d8d44694f016603bebd3909fe718dbbd6fe8018c17f5460c040bc3aea76
checker   87,732  9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```
