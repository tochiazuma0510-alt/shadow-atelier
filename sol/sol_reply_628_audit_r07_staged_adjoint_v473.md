# Sol(max) Task628 reply: staged-adjoint theorem v473

## Verdict

`PASS_AFTER_REPAIR`.

The staged theorem is mathematically sound for the actual selected-SLP DAG.
The dependency list is complete, the displayed order is topological, and I
found no cross-stage return, actor-parent reversal, or contribution that can
arrive after its destination node has been released.  Exact path
coalescence reproduces the old pathwise sum over `F3` without quotient
coalescence.

One finite repair is required in section 5 only: two embedded carriage-return
bytes corrupt the intended `E_{\mathrm{reached}}` notation, and that symbol
must explicitly count **state-edge traversals with multiplicity**, not merely
distinct constructor edges.  No DAG, coefficient, schedule, or theorem
redesign is needed.

This is a paper/static verdict, not Task625 acceptance or a numerator.
No code, production/GHA, or git operation was performed.  All grade, A0,
COMMON, cofinal, fake and Ihara claims remain false; `verified=false`.

## Audited snapshot

| input | bytes | SHA-256 |
|---|---:|---|
| Task628 | 1,344 | `f874083d5ce98870020eb85beb19cce1a9390739637ceb15f5cd0c7e0224a3ff` |
| v473 | 7,785 | `c402a8db82cc3cf36a5572b6b21cad824dd6efa2e698f9492999164e1d9177eb` |
| Task601 producer | 47,935 | `cfd581f8a71176f9252555a94028a8482ede862ee3430098270109e52fa0d3ff` |
| Task601 checker | 71,637 | `09ee815345e9ad2cfd80799a5bf7daf4446cda0eb3d8bc79bd7b3d9c61fa86c8` |
| pinned v3 constructor | 138,202 | `bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff` |
| Task618 reply | 12,980 | `e97c2cfc3e7c02ec385245f670335088fe42f128ae3b2ba0c96dd4b46bbdcc88` |
| Task620 reply | 15,314 | `3741a8027cf73e04ea865a20dcb070b7d2f92d1b419aaedbdd15df998969552d` |
| Task622 reply | 8,106 | `4eaf1f92f4ef1fdd0a7f3289175d7c8b97c5ac85714b0b368d4aa66a20f151e0` |
| v220 snapshot containing Delta419 | 973,773 | `c847ac2017ca1994b5d45b08c5f7409560460ac9ca0780e9060a60130491dd1b` |

I read v473 completely, inspected the complete producer/checker ancestry
construction and leaf-recurrence paths, and used the accepted Task618/620/622
source-DAG findings.  Delta419's immutable recorded facts agree with v473:
run `33723160379/1`, job `100546373059`, finished the 8,059-row physical
route at ranks `1661/5044` with 3,317 coefficients, then timed out after
159,383,552 expansions with 4,440 pending, 456 then-current leaves, maximum
path length 21, current RSS 1,420,152,832 and peak RSS 2,686,074,880 bytes.
Those facts diagnose a time terminal, not a completed leaf payload.

## 1. Actual node types and complete arrows

The concrete recurrence has exactly the following expansion dependencies.

| node | origin contribution | reduction contribution |
|---|---|---|
| `G_i` | one `B_(a,j)` or `O_(a,j)`; an old connection also contributes its recorded `L_j` rows | `G_j`, always `j<i` |
| `L_i` | one `O_(a,j)` | `L_j`, always `j<i` |
| `B_(a,i)` | one `D_o` for a defect origin, or its actor parent `B_(a,j)` | `B_(a,j)`, always `j<i` |
| `D_o` | seed: literal leaves; transition: acted `O_(a,j)` | the exact seed/transition expression in `O_(a,j)` |
| `O_(a,i)` | projected-seed literal leaves, or its actor parent `O_(a,j)` | `O_(a,j)`, always `j<i` |

This is precisely v473 (2.2).  There is no omitted `L -> B`, `B -> L`,
`O -> D`, or return to `G`.  A defect is safely shared across source-block
characters: the block-character projector has already been recorded in the
incoming coefficient and exact path, while `D_o` itself is determined by its
single authenticated lower-character origin.

The strict within-stage inequalities are genuine construction facts.
Every accepted physical or source pivot receives its new append index only
after reduction against already existing pivots.  The v3 old and block actor
constructors similarly take an already accepted parent and, if the child is
new, append it at a larger index.  Thus all `G`, `L`, `B` and `O` reduction
edges, and all `B`/`O` actor-parent edges, point to a smaller pivot.

The old transition expression attached to a `D_o` need not use only pivots
smaller than the transition's old parent: it is an expression in the
completed old basis and can mention any authenticated old pivot.  This is
not a counterexample.  V473 places **every** `D_o` before **every** `O_(a,j)`,
so all such contributions arrive before any old pivot is expanded.

V473 correctly makes the inequalities receipt gates rather than trusting a
`DAG` label.  The staged producer and independent checker must explicitly
check actor-origin kind, character/range, and `0 <= parent < child`, in
addition to the already required reduction inequalities.  This is an
implementation obligation already present at v473 lines 57--60, not an
additional paper repair.

## 2. Topological schedule

Read expansion arrows from a node to the nodes needed to express it.  Then:

1. decreasing `G` processes every higher grade source before a lower grade
   pivot and accumulates all cross-stage input into `L`, `B` and `O`;
2. decreasing `L` receives all `G` input first and sends only to lower-index
   `L` or to `O`;
3. decreasing `B` within each character receives all `G` input first and
   sends only to lower-index `B` or `D`;
4. all `D` origins run only after all four `B` stages, so a shared defect has
   its complete incoming coefficient; each `D` sends only to `O` or leaves;
5. decreasing `O` within each character begins only after `G`, `L` and all
   `D` origins have contributed, and sends only to lower-index `O` or leaves;
6. leaves are retained until all `D` and `O` stages finish.

The `L` and `B` stages have no arrows between them, so their relative order
is indeed immaterial.  Characters within a `B` stage and within an `O` stage
are also independent.  Consequently, immediately before a node `v` is read,
all possible incoming nodes have been processed and no unprocessed node has
an edge back to `v`.  Releasing `A_v` after expansion is therefore safe.

The three attempted failure patterns do not produce a counterexample:

- a grade-to-old shortcut still waits at `O` until after the defect stage;
- an actor origin always points to an earlier pivot and is therefore later in
  the decreasing expansion schedule;
- a diamond or a third late contribution reaches its destination before that
  destination's stage, so all equal `(node,path)` terms meet modulo three
  before the single expansion.

## 3. Exact coefficients and free words

For an edge with registered scalar `alpha` and registered source word `q`,
the staged update is

```text
A_destination[red(P q)] += c*alpha  (mod 3).
```

For a wordless reduction edge, `q` is empty.  This is the same recurrence as
the audited producer/checker paths: node scales multiply both the origin and
the negatives of ordered reductions; grade/lower/block/old reductions carry
the recorded minus sign; transition defects contribute the acted old parent
with no spurious scale and subtract their exact transition expression; seed
and projected-seed branches carry the registered character coefficient.
Coefficient two remains two in `F3`.

Both audited paths multiply the accumulated prefix on the left by appending
the actor or pure-Q1 word on the right.  The checker implements cancellation
directly on signed letters, independently of the producer helper.  Since
free reduction is canonical and multiplication in the free group is
associative, every root-to-node path contributes to exactly the same
`(node, freely-reduced path)` key as in pathwise expansion.  Linearity and
distributivity over `F3` then justify coalescing before expansion.  No PSL or
other finite-quotient endpoint, endpoint signature, non-injective hash, or
transient intern ID enters equality of keys.  Final serialization retains the
exact signed tuple.

## 4. Resource statement and sole repair

The theorem makes no uniform speedup claim.  The supports `N_v`, number of
exact interned words `U`, live-entry peak, maximum exact path length, final
leaf population and all caps remain result-dependent; exhaustion is
`UNKNOWN_RESOURCE`, and a partial leaf map is not a payload.  Thus the
mathematical schedule removes repeated expansion of an already incomplete
state but does not promise that the complete exact state set is small.

The current bytes at v473 section 5 contain two bare `0x0d` characters:

```text
E_{<CR>m reached}
```

both in the definition and in (5.1).  Replace both by a stable serialization,
for example `E_{\mathrm{reached}}`.  In the same sentence define it as the
number of processed pairs `(nonzero accumulated state, outgoing constructor
edge)`, counted with multiplicity over states.  Then

```text
sum_v |supp(A_v)| + E_reached
```

correctly counts state expansions plus edge updates.  Counting only distinct
DAG edges would be false whenever one node has two nonzero exact paths.  Word
construction/serialization, dictionary storage and RSS remain separately
covered by `U`, path-length/live-entry/durable-byte telemetry and explicit
caps.  This two-token serialization/definition correction is the complete
necessary repair.

## Final status

```text
ACTUAL DAG TYPE AND TOPOLOGICAL SCHEDULE:  PASS
EXACT F3 COEFFICIENT PROPAGATION:          PASS
EXACT FREE-WORD COALESCENCE:               PASS
NO RELEASE-AFTER-LATE-ARRIVAL:             PASS
RESOURCE CLAIM:                            PASS AFTER ONE LOCAL REPAIR
TASK625 / ACTUAL SELECTED PAYLOAD:          NOT ACCEPTED HERE
GRADE / A0 / COMMON / COFINAL / FAKE:      NOT DECLARED
IHARA:                                      NOT DECLARED
verified:                                   false
OVERALL:                                    PASS_AFTER_REPAIR
```

`R07_STAGED_ADJOINT_V473_PASS_AFTER_REPAIR`
