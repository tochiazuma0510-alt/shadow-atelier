# Luna reply 157bg — Burau tuple v4 marker repair

## Verdict

The authorized workflow repair is complete and bounded to
`.github/workflows/d972-burau-tuple-v4.yml`.  The producer, checker, and
receipt gates were not modified.

## Defect fixed

Run `32051744038` (commit
`983bd8b960c5d71ef686ee0d8a590728913f61d7`) had already completed both
calibrations:

```text
q3 / a=-1: 972 rows, fibre size 8, 1 identity and 7 nonidentity defects,
            status UNKNOWN_BURAU_SPECIALIZATION_ALLPASS
q4 / a=2:  972 rows, fibre size 8, 1 identity and 7 nonidentity defects,
            status UNKNOWN_BURAU_SPECIALIZATION_ALLPASS
```

The old exact-marker expressions accidentally compared a literal
`$BURAU_TAG`/`$BURAU_A` because of single-quoted shell fragments.  Therefore
the completed producers were rejected before q5 dispatch.

## Repair

The calibration step now constructs one expanded
`expected_calibration_marker` and checks

```bash
grep -Fxc -- "$expected_calibration_marker" ...
test "$calibration_marker_count" -eq 1
```

The q5 step constructs the two expanded allowed terminal strings (candidate
and all-pass), counts each with the same exact one-line check, sums the two
counts, and requires exactly one total line:

```bash
q5_allowed_terminal_count=$((q5_candidate_count + q5_unknown_count))
test "$q5_allowed_terminal_count" -eq 1
```

This removes the old `||` pipeline/precedence ambiguity.  The q3/q4 receipt,
independent checker, scalar, row-count, key, status, and `UNKNOWN_RESOURCE`
rejection gates are unchanged.

Before each expensive producer, bounded shell probes now test both cases:

* an expanded tag/value is accepted exactly once;
* a line containing the literal `$BURAU_TAG` or `$BURAU_A` is rejected.

No external dependency was added.  The probes emit
`BURAU_TUPLE_V4_MARKER_EXPANSION_REGRESSION_PASS` and
`BURAU_TUPLE_V4_Q5_MARKER_EXPANSION_REGRESSION_PASS`.

## Checks and provenance

The edited workflow parsed successfully with PyYAML and a static regression
asserted the expanded-marker strings, literal-variable rejection probes,
fail-closed q5 count, preserved `UNKNOWN_RESOURCE` rejection, and absence of
the old variable-fragment grep pattern:

```text
YAML_PARSE_AND_MARKER_STATIC_PASS
```

An equivalent read-only whitespace check found no trailing whitespace.  The
requested `git diff --check` was not run because the parent explicitly
prohibited local Git operations; the parent can run it in the broker audit.

The workflow SHA-256 after repair is:

```text
213a6ae59f55a391770ebc85de36f8fbba9b567f5a1537b616acea2234c80b74
```

The existing action references are mutable version tags, retained as found
and not broadly rewritten:

```text
actions/checkout@v4
actions/setup-python@v5
actions/upload-artifact@v4
actions/download-artifact@v4
```

No local heavy computation, GAP, Git, push, or GHA was run.

BURAU_TUPLE_V4_MARKER_REPAIR_READY_FOR_GHA
