# Luna reply 157au: power runtime probe repair

## Verdict

POWER_RUNTIME_PROBE_REPAIR_READY

Only `.github/workflows/d972-power-spectrum-v2.yml` and this reply were
modified.  No local GAP, git, push, or GHA was run.

## Exact repair

The invalid one-line probe at workflow line 53 was replaced by the proven
noninteractive batch/heredoc pattern using `QUIT_GAP(0)`:

```diff
-          actual_gap="$(gap -q -c 'Print(GAPInfo.Version); quit;')"
+          actual_gap="$(gap -q -b <<'GAP' | tail -n 1
+          Print(GAPInfo.Version, "\n");
+          QUIT_GAP(0);
+          GAP
+          )"
+          test -n "$actual_gap"
           test "$actual_gap" = "$D972_GAP_VERSION"
```

`tail -n 1` removes any startup noise; the nonempty check rejects an empty
probe, and exact equality rejects extra text or an unexpected/multiline final
value.  The apt pin `4.12.1-2build2`, runtime equality `4.12.1`, every source
hash, producer/checker command, selftest ordering, final markers, and all
fail-closed gates are unchanged.

## Static validation

The YAML parser and a static extraction of the runtime bash fragment passed:

```text
YAML_AND_BASH_RUNTIME_STATIC_PASS
```

The check confirmed `workflow_dispatch`, the heredoc/`QUIT_GAP(0)` sequence,
the nonempty and exact-version tests, and absence of the invalid `gap -q -c`
probe.  A local Bash executable was unavailable, so no shell execution was
attempted; this was intentionally a static-only audit.

## New workflow SHA-256

```text
40e9a9906a89864a5ad77bbbf6ed532ab061e6d061571b5428201c982a53980d  .github/workflows/d972-power-spectrum-v2.yml
```

POWER_RUNTIME_PROBE_REPAIR_READY
