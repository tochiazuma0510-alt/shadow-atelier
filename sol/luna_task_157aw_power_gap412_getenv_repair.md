# Luna task 157aw — remove GAP 4.12 GetEnv dependency

## Scope

Act as Luna.  GHA run `32056404236` at commit
`955f8a9a202b1f6f6ae921f9ef22e83ebb382f4b` passed the exact runtime bind and
then failed before selftest with:

```text
Error, Variable: 'GetEnv' must have a value
not in any function at search/d972_power_spectrum_v2.g:10
```

Modify only:

- `search/d972_power_spectrum_v2.g`
- `.github/workflows/d972-power-spectrum-v2.yml`
- `sol/luna_reply_157aw_power_gap412_getenv_repair.md`

Do not run local GAP, git, push, or GHA.

## Requirements

1. Remove every dependency on `GetEnv`.  The producer must consume two
   explicitly pre-bound GAP globals (mode and output path), with fail-closed
   validation and safe deterministic defaults only when they are genuinely
   absent.
2. Invoke selftest and full mode from workflow using the proven
   `gap -q -b` heredoc plus `Read("search/d972_power_spectrum_v2.g")` and
   `QUIT_GAP(0)`.  Preserve correct pipeline exit capture and exact one-marker
   checks.  Do not use the broken `gap -q -c ... quit;` form.
3. Preserve all mathematical computation, row/table serialization, core/helper
   reads, checker logic, hashes for unchanged sources, apt/runtime pins, and
   fail-closed gates.
4. Update the producer SHA in workflow after the edit.  Parse YAML, run Python
   checker compile/selftest, and statically validate both GAP heredocs.  No
   local GAP execution.
5. Include hostile static cases for absent mode, invalid mode, and empty output
   path.  State the exact behavior.
6. Return `POWER_GAP412_GETENV_REPAIR_READY` or `BLOCKER: <exact defect>`, with
   final producer/workflow hashes.

