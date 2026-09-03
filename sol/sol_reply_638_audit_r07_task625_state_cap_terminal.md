# Sol(max) Task638 reply: audit of the Task625 staged-state-cap terminal

## Verdict

`PASS_CAP_ONLY_RERUN`.

Run `33732940935/1`, job `100576830812`, at release commit
`c4ae5094800d4acb812eefb21820b9998afc3804` stopped solely on the cumulative
state-insertion/work counter.  It did not stop on time, RSS, durable bytes,
interned paths, path length, live retained states, or a mathematical
inconsistency.  A versioned workflow-only increase of
`TASK625_ACCUMULATED_CAP` from `2,000,000` to `50,000,000` is the sound minimal
rerun.  The exact final v3 workflow identified below implements only that
permitted successor and is safe for the parent to commit, push, and launch.
Neither Python executable should change.

This verdict authorizes only the exact finite cap-only v3 successor bound
below.  It is not a production result or a completion guarantee.
`verified=false`.

## Exact input binding

| input | bytes | SHA-256 |
|---|---:|---|
| Task638 mail | 1,691 | `53153662aeb01572dd25c273737c71fab0a4ceaa387f0c4dc31c333b3d473ab7` |
| producer log | 4,534 | `e5c86f0750fe348d3c30e073ec94053c2753817a8097c8e5280c802ab2b68f37` |
| audited v2 producer | 75,000 | `ce036c4a1a92d16a78cb8da8c16dee282a6a981889f821e6df82eaecdd8fba0a` |
| audited v2 checker | 104,392 | `8c3dd039368f63d62ef79694a196f73d0b626134df39673c5e48c98c7c8787f9` |
| audited v2 workflow | 6,077 | `d5f724eb163faf68e0555ec4e5e32dcf05b2d3df1749da89b8762ff5078e6109` |
| Task634 final PASS | 9,172 | `ea8ecc3ab4069ba56fa12069010f0cce7fa0122dc25d93de1bc0d38cf743fa95` |
| Luna Task637 instruction | 2,928 | `007a942832d6576f1b8aee44fd12da42046b5bde8df252317761c008ca476316` |
| final v3 workflow | 6,078 | `736f5f86dde47ebe46fcfdbf8a8d20d4e8f052461c4ae1f137433f6618dd0f9f` |
| Task637 final reply | 3,332 | `ff54819bac1a0ec4a88a0c83429497e0bcc66e47d4e8f5376fedb3e4bd149f91` |

The log's size and digest match the Task638/Task637 declarations exactly.
The producer, checker, and v2 workflow are byte-identical to the quartet
accepted by Task634.  The two Task637 final hashes match the completion
handoff exactly.

## 1. Exact terminal diagnosis

The seven completed staged records report insertion deltas

```text
physical-grade   957,456
physical-lower    93,682
block-0          122,862
block-1          170,735
block-2          152,104
block-3           18,415
defect            296,826
                 ---------
cumulative      1,812,080
```

The producer keeps `state_insertions` across stage boundaries.  For every new
node-state or leaf-state key it increments that counter and immediately tests
`state_insertions > caps["accumulated_states"]` before storing the new key.
Therefore another 187,920 new insertions were admissible in the next stage;
the following attempted insertion made the counter `2,000,001` and raised
`UNKNOWN_RESOURCE:staged_state_cap`.

The same terminal string is also used by the live-entry guard, but that guard
cannot be the source here.  At the end of the defect stage the reported live
maximum was only 8,356.  Before the cumulative guard fired, at most 187,920
further successful insertions could increase live storage, giving the strict
upper bound

```text
live entries before failure <= 8,356 + 187,920 = 196,276 < 2,000,000.
```

Popping a bucket only decreases live entries, and every operation that can
increase them first increments and checks the cumulative counter.  Thus the
two same-named call sites are unambiguous for this run: this was a cumulative
work-cap terminal, not a retained-live-state terminal.

All other observed resource coordinates had large margin:

| coordinate | last/maximum observation | bound |
|---|---:|---:|
| elapsed at final completed stage | 448.463583 s | 2,400 s internal |
| peak RSS | 2,699,411,456 bytes | 7,516,192,768 bytes |
| RSS at final completed stage | 1,357,611,008 bytes | 7,516,192,768 bytes |
| durable bytes | 231,680,287 | 7,516,192,768 |
| interned exact paths | 29 | 2,000,000 |
| maximum path length | 20 | 4,096 |
| maximum completed-stage live entries | 8,356 | 2,000,000 |

The log had already passed the exact physical route (`logical=8059`, lower
rank 1,661, grade rank 5,044), the 3,317-coefficient MEMBER closure, packed
source construction, and all four selected-source block copies.  The final
line is the caught `UNKNOWN_RESOURCE` terminal, not a failed equation or an
exception denoting inconsistency.

No `canonical-graph-leaf-sealed` or `payload-sealed` record exists.  The
producer's handler discards staging and returns nonzero; workflow `pipefail`
therefore prevents the serial checker command from starting.  No payload or
checker verdict was produced.

## 2. Staged-schedule evidence

For the completed `G,L,B_0,...,B_3,D` prefix, the telemetry sums to

```text
processed scheduled nodes   12,906
expanded exact states       11,652
state-edge traversals     5,391,606
interned exact paths             29
cumulative insertions     1,812,080
```

These counters have the repaired v475 meanings.  A scheduled node is popped
once after all predecessors, its complete exact-path bucket is expanded, and
the code rejects any later edge to an already processed position.  The large
cumulative insertion count records coefficient updates, cancellations, and
reinsertion before a node is due; it is not a count of repeated downstream
expansions.  Only 11,652 completed `(node, exact path)` states were expanded
over 5.39 million state-edge traversals, and all seven stages completed by
about 448.5 seconds including the much larger physical/source preparation.

Thus the completed prefix gives direct operational evidence that the former
pathwise expand-before-coalescence loop is gone.  It does not prove that the
remaining four `O` stages and leaf stage finish within the fixed resources;
that remains the purpose of the rerun.

## 3. Exact final workflow and minimal rerun boundary

I read the complete 6,078-byte v3 workflow and compared it byte-for-byte with
v2.  The unified delta contains exactly six replacements:

```text
workflow name                       staged-v2 -> staged-v3
workflow trigger path               ...-v2.yml -> ...-v3.yml
TASK625_ACCUMULATED_CAP              2000000 -> 50000000
fire marker                         staged-v2 -> staged-v3
success artifact label              staged-v2 -> staged-v3
always-log artifact label           staged-v2 -> staged-v3
```

Normalizing those five version labels/paths and the one cap value reproduces
the v2 workflow exactly.  YAML parsing, all five source/reply/theorem hash
pins, all six immutable 40-hex action pins, serial producer/checker order,
success-only payload, always-uploaded logs, and whitespace/EOF checks pass.
The workflow intentionally continues to run the audited v2 Python files and
to require the v2 checker's marker.

Changing only the versioned workflow environment value to

```text
TASK625_ACCUMULATED_CAP: "50000000"
```

is sound.  Both audited executables already read this value dynamically; the
producer records it in the manifest and the checker independently derives the
same expected cap from the shared environment.  No algorithm, routing rule,
word equality, receipt schema, or checker independence changes, so changing
either Python hash would be unnecessary and outside the minimal repair.

Precisely, this environment value is used as a shared ceiling for cumulative
insertions and live entries.  Raising it therefore relaxes both numerical
checks, but the failed run is proved above to have hit only the cumulative
one.  The change allocates no memory.  Retained memory remains bounded by the
unchanged 7-GiB RSS check and 8-GiB virtual-memory limit; work remains bounded
by the 2,400-second internal clock, 45-minute command timeout, and 60-minute
job timeout.  The 7-GiB durable cap, 2,000,000-path interning cap, and
4,096-letter path cap also remain unchanged.

`50,000,000` is a finite 25-fold work allowance, not evidence that the
computation will complete.  Hitting it, a clock, RSS/VM, path, or durable
boundary must still yield `UNKNOWN_RESOURCE` and no promoted artifact.  This
residual resource uncertainty is non-blocking for the cap-only rerun.

## 4. Claim boundary after the failed run

The run establishes only authenticated producer progress and the resource
diagnosis above.  Because there is no sealed payload and the independent
checker never ran:

```text
actual selected-SLP payload:   NOT PRODUCED
fresh rho2 / next residual:    UNKNOWN / NOT COMPUTED
direct_occurrence_replay:      false
next_degree2_residual:         null
cross_checked:                 false
verified:                      false
A0:                            false / NOT ESTABLISHED
COMMON:                        false / NOT ESTABLISHED
cofinal lift:                  NOT ESTABLISHED
fake witness:                  false / NOT ESTABLISHED
Ihara counterexample:          false / NOT ESTABLISHED
mathematical NONMEMBER:        NOT ESTABLISHED
run terminal:                  UNKNOWN_RESOURCE:staged_state_cap
```

The failed run does not change the status of any parent candidate or theorem.

```text
TERMINAL CLASSIFICATION:          CUMULATIVE INSERTION/WORK CAP ONLY
V475 COMPLETED-PREFIX BEHAVIOR:   STAGED COALESCENCE OBSERVED
PYTHON PRODUCER CHANGE:           NONE
PYTHON CHECKER CHANGE:            NONE
VERSIONED WORKFLOW CAP RERUN:     PASS
PRODUCTION / MATHEMATICAL RESULT: NONE
verified:                         false
OVERALL:                          PASS_CAP_ONLY_RERUN
```

`R07_TASK625_STATE_CAP_ONLY_RERUN_PASS`
