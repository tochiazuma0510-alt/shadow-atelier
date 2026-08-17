# Luna task 157au — repair GAP runtime probe in power-spectrum v2

## Scope

Act as Luna.  The failed GHA run is `32056025208` at commit
`9b73fbb3c9b3735c8732abdae06cb70ea7946569`.  Read its failed log if needed.
The apt package installed successfully; the exact failure was:

```text
gap -q -c 'Print(GAPInfo.Version); quit;'
Executing command ... has been aborted.
```

Modify only:

- `.github/workflows/d972-power-spectrum-v2.yml`
- `sol/luna_reply_157au_power_runtime_probe_repair.md`

Do not run local GAP, git, push, or GHA.

## Requirements

1. Replace only the invalid GAP version-probe invocation with the same
   noninteractive heredoc/`QUIT_GAP(0)` pattern already proven by the current
   D972 dovetail workflow on run `32055311874`.
2. Preserve the exact apt package pin `4.12.1-2build2`, runtime equality check
   `4.12.1`, every source hash, producer/checker command, and all fail-closed
   gates.
3. Ensure the captured version contains exactly the version string despite any
   startup noise; do not silently accept an empty or multi-line value.
4. Parse YAML and statically validate the bash fragment.  Report the new
   workflow SHA-256 and exact diff.
5. Verdict: `POWER_RUNTIME_PROBE_REPAIR_READY` or `BLOCKER: <exact defect>`.
