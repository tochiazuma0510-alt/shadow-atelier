# Luna reply 157aw: GAP 4.12 environment-binding repair

## Result

`POWER_GAP412_GETENV_REPAIR_READY`

The producer no longer performs an environment lookup.  The workflow binds
the two GAP globals before `Read()`:

```text
D972_POWER_MODE
D972_POWER_OUTPUT
```

The producer consumes those globals with fail-closed validation.  Defaults
are selected only when the corresponding global is genuinely unbound:

```text
mode   -> "full"
output -> "ci/out/d972_power_spectrum_v2.json"
```

If a bound mode is not the string `selftest` or `full`, the producer raises
`D972 power spectrum v2: invalid D972_POWER_MODE`.  If a bound output is not a
string or is empty, it raises `D972 power spectrum v2: empty
D972_POWER_OUTPUT`.  These are the hostile static cases:

| case | exact behavior |
|---|---|
| both globals absent | deterministic full-mode/default-output execution |
| mode absent, output bound nonempty | full mode and the bound output |
| mode bound to `selftest` or `full` | selected mode |
| mode bound to any other value, including empty or `fail` | fail closed before computation |
| output bound to empty, non-string, or `fail` | fail closed before computation |

No `GetEnv` token or dependency remains in the producer.

## Workflow repair

Both execution lanes now use the required form:

```text
gap -q -b <<'GAP' ... GAP
```

Each heredoc binds mode and output, reads
`search/d972_power_spectrum_v2.g`, and calls `QUIT_GAP(0)`.  The runtime
version probe retains its own heredoc.  Selftest and full execution each keep
`set +e`, capture `${PIPESTATUS[0]}` immediately after `tee`, restore
`set -e`, and enforce exactly one corresponding marker.  The full lane still
checks the error patterns, receipt nonemptiness, and independent checker
marker.  No `gap -q -c ... quit;` form was introduced.

The workflow's producer SHA gate was updated after the final producer edit.
Unchanged runtime source/checker/package pins and all mathematical/table
serialization logic were preserved.

## Static verification (no GAP execution)

The following checks passed:

```text
python -m py_compile search/check_d972_power_spectrum_v2.py
python search/check_d972_power_spectrum_v2.py --self-test
  D972_POWER_SPECTRUM_V2_CHECKER_SELFTEST_PASS
PyYAML safe_load(.github/workflows/d972-power-spectrum-v2.yml)
  YAML_PARSE_PASS
static producer/workflow binding and heredoc audit
  GAP_HEREDOC_STATIC_PASS
```

The static heredoc audit found the runtime probe plus exactly two producer
heredocs, two producer `Read()` calls, and three `QUIT_GAP(0)` calls total.
No local GAP, Git, push, or GHA was run.

## Final hashes

```text
search/d972_power_spectrum_v2.g
7AC226FF44F631BBAA4AB2A5C9700B4657FD94C7D959DCAA371BA3F860B97699

.github/workflows/d972-power-spectrum-v2.yml
835473CBF1376EA082A8373912D822BEB0AFDE0B99002967A7E3878DCA60B2BA
```
