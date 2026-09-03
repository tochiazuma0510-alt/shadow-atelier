# Luna Task637 reply: Task625 accumulated-cap release v3

## Result

Created the workflow-only v3 successor.  The audited v2 Python producer,
checker, theorem, reply, source/candidate parents, action pins, serial order,
timeouts, and memory/durable/path limits are unchanged.

The sole non-label production change is:

```text
TASK625_ACCUMULATED_CAP: "2000000" -> "50000000"
```

The workflow identity, fire marker, workflow trigger path, and both artifact
labels were changed consistently from staged-v2 to staged-v3.  The workflow
still executes the v2 producer and independent v2 checker with their exact
Task632 hashes.

## Exact bindings

| input/output | bytes | SHA-256 |
|---|---:|---|
| Task637 mail | 2,928 | `007a942832d6576f1b8aee44fd12da42046b5bde8df252317761c008ca476316` |
| audited v2 workflow | 6,077 | `d5f724eb163faf68e0555ec4e5e32dcf05b2d3df1749da89b8762ff5078e6109` |
| Task634 final reply | 9,172 | `ea8ecc3ab4069ba56fa12069010f0cce7fa0122dc25d93de1bc0d38cf743fa95` |
| v2 producer | 75,000 | `ce036c4a1a92d16a78cb8da8c16dee282a6a981889f821e6df82eaecdd8fba0a` |
| v2 checker | 104,392 | `8c3dd039368f63d62ef79694a196f73d0b626134df39673c5e48c98c7c8787f9` |
| Task632 reply | 7,796 | `6ef38b64baee05ed26a57b8cfbf7e2c80baaa11079ea0775ad9aed5b392d8ab8` |
| theorem v475 | 8,253 | `757ffab5aa011643efa3df4b133dc03d423895d57a003ed6830a47528388148e` |
| new v3 workflow | 6,078 | `736f5f86dde47ebe46fcfdbf8a8d20d4e8f052461c4ae1f137433f6618dd0f9f` |

The exact final byte count and SHA-256 of this reply are reported in the
completion handoff, avoiding a self-referential hash field.

Parent release commit is
`c4ae5094800d4acb812eefb21820b9998afc3804`.  The observed parent terminal is
bound to run/attempt/job `33732940935/1 / 100576830812`, log artifact id
`9884845034`, artifact digest
`44429fafe79808d097130f172ab7766b7a81c1691be6bc60687f128740bdfdf3`,
and producer-log SHA-256
`e5c86f0750fe348d3c30e073ec94053c2753817a8097c8e5280c802ab2b68f37`.

## Bounded gates

```text
YAML safe parse                                      PASS
exact v3-to-v2 normalization                         PASS
  permitted delta: v3 labels/trigger + 50M cap only
producer --selftest                                  PASS
  fixtures=9, expanded=13, traversals=13, max-live=3
checker --selftest                                   PASS
  fixtures=9, expanded=13, traversals=13, max-live=3
source hash pins                                     PASS
immutable action pins                                PASS (6/6, 40 hex)
placeholder/control/trailing-whitespace scan         PASS
```

The first exact-delta invocation had only a PowerShell quoting error; it did
not execute either production program or change a file.  The corrected
read-only comparison passed byte-for-byte after normalizing precisely the
permitted strings.

## Boundary

The accumulated counter measures cumulative insertion/work, not retained
live memory.  RSS remains bounded by the unchanged 7-GiB program cap and
8-GiB VM limit.  Exhaustion at 50,000,000 remains
`UNKNOWN_RESOURCE:staged_state_cap`.

No production route or GHA was run.  No git operation was run.  This static
release does not establish completion, payload validity, A0, COMMON, a
cofinal lift, a fake witness, an Ihara counterexample, cross-checking, or Lean
verification.

READY_FOR_SOL_MAX_REAUDIT
