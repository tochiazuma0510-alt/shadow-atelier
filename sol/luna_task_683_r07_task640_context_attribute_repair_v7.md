# Luna Task683 — Task640 Context attribute repair and inert v7

## Exact observed defect

You are Luna.  Repair the fresh-rho2 producer after v6 run/attempt
`33754182010/1`, job `100644492138`.

V6 completed the exact Task625 replay and both verdict copies, then the
producer stopped before arithmetic with:

```text
"'Context' object has no attribute 'shifts'"
```

The authenticated grade1-v4 `Context` defines `physical_shifts`; the producer
uses the nonexistent `context.shifts` once at its first-six prefix gate.
Repository-wide static census confirms that this is the producer's only
`context.shifts` use.  The independent checker defines its own local Context
whose field is legitimately named `shifts`; do not change it.

## Authorized edits

- `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`
- new inert `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v7.yml`
- `sol/luna_reply_683_r07_task640_context_attribute_repair_v7.md`

Do not edit the v6 workflow, checker, Task640 old reply, proof, v220, or any
other file.  No git/GHA dispatch/download/heavy run/parallel Python.

## Required minimal repair

1. Change the one producer comparison to the actual typed field
   `context.physical_shifts`.
2. Factor that first-six shift equality into a small helper used by production
   and selftest.  Add a live fixture object exposing `physical_shifts` but no
   `shifts`, and a one-entry mutation that the same helper rejects.  This must
   red-light reversion to the nonexistent attribute without constructing the
   full real Context.
3. Copy released v6 to v7, update only mechanical v7 labels/self-path/fire and
   output-artifact names, update `PRODUCER_SHA256` to the repaired exact file,
   and make the job inert via `${{ false && (...) }}`.  Preserve every v6
   path/cap/pin/download/copy/timeout/action/upload and checker hash.

Run serial py_compile and both existing selftests, safe YAML parse, a static
census of all producer `context.*` fields against the real grade1 Context,
normalized v6-to-v7 diff, action/inert scan, and prove both verdict copies
remain after `cmp`.  Do not rerun the 11m49s parent or rho2 computation locally.

Reply with exact path bytes/LF/SHA and commands.  End
`READY_FOR_SOL_CONTEXT_AUDIT` or `NOT_READY`.  Candidate only;
`verified=false`; no rho2/A0/fake claim.
