# Task 607 - audit of canonical selected-dependency SLP v468

## Verdict

`PASS_AFTER_REPAIR`

The repaired v468 serialization is readable and the central separation is
correct: the graph-reachable, ordered noncommutative SLP is the source
witness, while coefficient coalescence belongs only to a quotient-specific
adjoint evaluation.  The typed graph is finite and acyclic, its constructors
retain the data needed to define one free-source word, cancellation may not
prune source edges, and refinement naturality is stated at exactly the right
strength.

Two narrow load-bearing repairs remain.

1. Theorem 4.2 applies `F^1/F^2` to all selected nodes even though v465
   expressly says that old/lower nodes are not licensed as source-filtration
   elements by physical-lower replay.  The conclusion must be typed as a
   physical-grade equality for those nodes, with endpoint and complete
   physical replay premises, or must add a separate source-membership replay.
2. Checker item 5 must compare every reached origin/scale/ordered reduction
   record with the deterministic reroute or authenticated source expression.
   Reproducing only the terminal packed basis and MEMBER equality cannot
   authenticate the noncommutative local edge order that makes this SLP
   canonical.

Neither repair changes the selected graph, source word, adjoint formula, or
implementation architecture.  No flat word and no unselected discovery
closure are required.

## 1. Exact audit inputs

I restarted the audit after the serialization repair and read every numbered
input in full.

| input | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_607_audit_r07_canonical_selected_dependency_slp_v1.md` | 1,481 | 31 | `fe495f507a074d24750b125da3f3792d791f14fcab2169b0eb04935f16d87b2f` |
| `sol/proof_r07_selected_ancestry_slp_lift_v465.md` | 9,801 | 253 | `b779fca02449a1e4465bf0a29f7da8388f4c2e32c28a6f959e8c50189f2c7693` |
| `sol/proof_r07_reverse_selected_physical_slp_extraction_v466.md` | 6,810 | 153 | `0a7f1cf9d4f2d494379d39ea62ad20c0c27bb9935f29e9a9af4874493e0de308` |
| `sol/proof_r07_selected_slp_adjoint_fox_replay_v467.md` | 8,481 | 201 | `f80a63b2db0efe56777a48d1ddaab61518df9a802884549834e63e517e9a8dc5` |
| `sol/proof_r07_canonical_selected_dependency_slp_v468.md` | 12,016 | 284 | `b1e0f09ae0c6f136804e37bc8db8cba85bccede0880ed5f26afed880d28829a6` |
| `sol/luna_task_601_r07_grade1_selected_slp_extraction_v1.md` | 5,347 | 101 | `3d4c069c0800454bf03866f6ae682fb7608cfab43b9a8f91bc0776b0f5575ced` |

The commissioned repaired-v468 SHA-256 matches exactly.

## 2. Canonical syntax versus adjoint coalescence

V468 Section 1 makes the necessary distinction.

- The source object recursively interprets every origin, ordered edge
  occurrence, coefficient, scale, actor and root as a literal operation in
  the fixed free group.  This graph is quotient-independent.
- The adjoint object is a derived current-quotient calculation.  Once exact
  endpoint-one gates justify Fox additivity, equal current states may have
  their scalars added in `F_3` and a zero state may be discarded.

The second operation cannot mutate the first.  Even if two incoming weights
on a child sum to zero in the current grade, the two local edge occurrences
remain in their respective ordered parent products.  Deleting them can alter
a commutator or the next-grade term.  V468 (1.2), Section 3 and Section 5 all
state this correctly.  Keying adjoint coalescence by the typed node and actor
path, binding it to the canonical-parent digest, and marking it

```text
quotient_specific_evaluation = true
common_source_witness = false
```

prevents the derived scalar map from being passed off as the source witness.

## 3. Finiteness and acyclicity

The completed-old-owner references do not introduce a cycle.  The dependency
directions are:

```text
physical grade
  -> earlier physical-grade nodes
  -> physical lower or character block
physical lower
  -> earlier physical-lower nodes
  -> completed old owner
character block
  -> earlier character-block nodes
  -> defect
defect
  -> arbitrary nodes of the already completed old owner
old owner
  -> earlier old-owner nodes
  -> literal seed/actor leaves
```

Thus every within-owner edge strictly lowers the accepted-node identifier,
while every cross-owner edge strictly lowers the type order.  A
`seed_reductions` or `actor_transitions` expression may mention an old pivot
whose identifier is larger than some other old pivot; this is harmless
because the edge entered the old owner from the strictly later defect layer.
Once inside an old node, its own ancestry again points only backward.  There
is no edge from the old owner back to defect, block, lower or physical grade.

The three roots add no cycle.  `C_T` refers to the finite 3,317-entry selected
root list; `C_<1` is the separately sealed finite ordered prior SLP; and
`C_1` has exactly those two children in registered composition order.
Consequently Theorem 4.1's lexicographic induction is valid under its explicit
authenticated-record hypotheses.

## 4. Sufficiency of the typed word data

Formula (2.2) has the correct exact-word convention:

1. origin first;
2. every local reduction child in recorded order, with power `-q`;
3. the whole product raised to the normalization scale `sigma`.

The fixed representatives `[0]=0`, `[1]=1`, `[2]=-1` make coefficient two an
inverse.  Thus both a reduction coefficient two and a normalizing scale two
have the correct associated-grade sign while retaining an exact
noncommutative word.

The R07-specific expansions also carry the necessary information:

- an old-derived physical-grade origin contains its exact old word followed
  by every signed lower-pivot link in lower-reducer order before its own
  grade reductions;
- a physical-lower pivot carries the same complete old origin, ordered lower
  reductions and its own normalization, so its stored grade companion is
  scaled consistently with its lower pivot;
- character-block actor origins retain the exact literal actor, while defect
  origins retain all four pure-`Q_1` actor words, character signs and
  registered order;
- seed and transition defects retain the referenced completed-old expression
  with its exact signs and order; and
- old accepted nodes retain projected-seed or actor-parent origin, earlier
  reductions, and the outer scale.

Together with exact original identifiers and typed references, these data
define one SLP; no quotient coefficient vector is used to define its syntax.
The roots (3.2)--(3.3) then retain the exact Task595 coefficient-list order,
the sealed `canonical_solution["terms"]` order, and the registered
`canonical_solution + update` composition order.  This is sufficient to
define one element of the free source without allocating its flat spelling.

## 5. Load-bearing repair 1: type Theorem 4.2 correctly

The proof of Theorem 4.2 begins:

```text
Apply the quotient homomorphism F^1 -> F^1/F^2 to (2.2).
```

That argument is valid for a pure node only after its origin and constructed
word are known to lie in `F^1`.  V465 Proposition 2.2 deliberately withholds
that premise for old/lower physical nodes.  Its two direct equations

```text
E_<1^phys(W) = 0
E_1^phys(W)  = stored normalized grade row
```

license a row in the registered physical fibre.  They do not prove
`W in F^1` and expressly do not prove membership in a source relative kernel.
The final sentence of v468's proof acknowledges this distinction but cannot
make the preceding source quotient applicable.

This is a real type gap, not optional exposition.  A physical map can kill an
element outside a chosen source filtration, so physical-lower zero alone
cannot make its class in `F^1/F^2` defined.

Repair Theorem 4.2 and its proof as follows.

- Keep `[W_j]_1=b_j` only for the pure branch covered by v465 Theorem 2.1.
- For every reached old/lower-derived branch, require the exact current
  endpoint gate and the complete per-node physical replay, and state its
  conclusion in the physical modules:

  `E_<1^phys(W_j)=0` and
  `E_1^phys(W_j)=b_j` (or its registered normalized companion).
- Use those typed physical equalities, the authenticated owner recurrences
  and v467's endpoint-one additivity to conclude
  `E_1^phys(C_T)=sum_i a_i b_{j_i}` and then the complete precision-one target
  equality for `C_1`.
- Do not infer `C_T in F^1` or any source relative-kernel membership.  If a
  source associated-grade statement is wanted in addition, make the separate
  direct source-reduction replay an explicit hypothesis.

This preserves the intended positive handoff and exactly matches v465's
lower-first licence.

## 6. Load-bearing repair 2: authenticate each canonical local transcript

Checker items 1--4 correctly authenticate the parent data, encoding, graph
closure, literal words, local orders and three roots.  Item 5, however, says
only that the checker reproduces the grade-one packed basis and MEMBER
equality.  Those terminal objects do not by themselves authenticate the
candidate's local noncommutative ancestry.

For example, permuting two recorded reduction factors leaves their abelian
grade-one sum and hence the terminal packed pivot unchanged, but generally
changes the free word and its grade-two residual.  A self-consistent selected
payload could therefore pass structural checks and terminal basis equality
while failing the claimed canonical reducer order.

Amend item 5 to require the Task601 check already intended by v465--v466:

- during the exact deterministic physical reroute, compare every reached
  origin, normalization scale, coefficient and ordered reduction interval
  with the exported physical-grade/lower transcript;
- compare every reached block/old edge and every non-DAG
  `seed_reductions`/`actor_transitions` expression, including character
  signs and child order, with the authenticated sealed source record; and
- replay each reached normalized row and lower grade companion against the
  referenced packed rows, before accepting the terminal basis and 3,317-term
  MEMBER equation.

The checker may discard transient records for unselected nodes.  It need not
serialize the full discovery DAG: it only compares or retains a record when
its original identifier lies in the graph-reachable selected set.  Exact
local transcript comparison, not export of all unselected nodes, supplies the
missing authority for the word `canonical`.

## 7. Reachability and minimal payload

V468's graph closure rule is correct.  Start from each nonzero root occurrence
and traverse every nonzero local child reference, including physical-lower
links and reached non-DAG defect expressions.  Marking is Boolean graph
reachability, not a mod-three flow computation.  Each selected node retains
its complete ordered edge interval, including duplicate occurrences if any.

This is precisely the least dependency-closed payload.  Omitted discovery
nodes cannot influence a root once every child edge of each reached node has
been authenticated.  Conversely, net-zero adjoint flow does not authorize
omitting a reached node or edge.  After repair 2 binds each local record to
the authoritative replay, an independent checker needs neither a flat word
nor the whole unselected owner.

## 8. Naturality and claim boundary

Theorem 4.3 is sound independently of the Theorem 4.2 repair.  Exact leaves
live in the common free source, and ordered product, inverse, conjugation and
registered composition commute with evaluation along the assumed triangles
`r_(Q',Q) pi_Q' = pi_Q`.  Structural induction therefore gives natural
evaluation of this one word.

V468 correctly does not infer that the word solves the target at a
refinement.  Current-grade coefficient cancellation, current endpoint-one,
and the current MEMBER equation need not persist upward.  The next residual
must be computed from this exact ordered representative, and relative-kernel
surjectivity remains a separate gate.

After the two repairs, the checker obligations are necessary and sufficient
for the claimed selected-source handoff: authenticate inputs, authoritative
local transcripts and exact reachability; check finite typed syntax and all
three roots; replay current endpoints and every mixed physical licence; and
finally replay the complete precision-one equation before computing a fresh
residual.  Resource exhaustion remains UNKNOWN_RESOURCE.

Nothing here produces the actual selected payload or fresh grade-two
residual, promotes a rung, proves compatible/cofinal solvability, or declares
A0, COMMON, fake or Ihara.  No Lean proof exists.

```text
TASK607_V468_AUDIT:                         PASS_AFTER_REPAIR
CANONICAL_GRAPH_ACYCLIC:                   YES
EDGE_PRUNING_BY_CURRENT_COEFFICIENT:        FORBIDDEN
CURRENT_ADJOINT_COALESCENCE:               ALLOWED_AFTER_ENDPOINT_GATES
SOURCE_ASSOCIATED_GRADE_FOR_MIXED_NODES:   NOT_ESTABLISHED
REFINEMENT_NATURALITY_OF_THE_WORD:         SOUND
ACTUAL_SELECTED_PAYLOAD_OR_GRADE2_RESULT:  NOT_PRODUCED
A0_COMMON_COFINAL_FAKE_IHARA:              NOT_DECLARED
verified:                                  false
```

