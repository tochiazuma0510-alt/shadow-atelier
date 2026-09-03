# Task 594 — independent audit of selected-ancestry SLP lift v464

## Verdict

`PASS_AFTER_REPAIR`

The central idea is correct: a finite authenticated acyclic group-word SLP is
itself one explicit free-source word instruction.  It need not be expanded to
a flat letter list, and structural evaluation of that one syntax tree is
automatically natural across compatible finite quotients.  The sign and scale
in v464 (1.3) agree with the frozen echelon convention, and recomputing the
next residual from the exact chosen SLP is mandatory.

Two load-bearing application points need a local paper repair before the
claim can be used for the grade-one positive handoff:

1. v464 does not state enough filtration/action hypotheses, and its
   lower-first paragraph conflates a zero lower **physical** image with
   membership in the source filtration/relative kernel.  For a lower-first
   node, both its complete lower/auxiliary zero and its associated-grade row
   must be established by direct evaluation of the exact SLP; they do not
   follow from Theorem 2.1's pure-(F^d) hypothesis.
2. Section 4 exports only the selected update root (C_T), but the actual
   positive finalizer checks the authenticated earlier correction **plus**
   that update.  (C_T) solves the grade-one residual; it does not by itself
   reproduce the full grade-one target or define the correct degree-two
   residual.  The handoff needs one top root for the complete correction in
   the registered composition order.

These are finite statement/interface repairs, not a counterexample to the SLP
construction and not a request for implementation hardening or flat
materialization.

`verified=false`; this was a read-only mathematical/code-path audit.  No
production phase, implementation, workflow, proof, v220, git, or GHA action
was run or changed.

## Frozen receipt

| commissioned input read in full | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_594_audit_r07_selected_ancestry_slp_lift_v1.md` | 1,368 | 26 | `44fe435f9f4680af3748e570cc996038e7676c0392d24c8d04ccf124b6415cdb` |
| `sol/proof_r07_selected_ancestry_slp_lift_v464.md` | 6,724 | 176 | `a36890fe0b0093047b49af1435402822a83f642f130db9678c5f920924e10179` |
| `sol/proof_r07_instruction_tree_relative_layer_lift_v395.md` | 9,347 | 273 | `92ac7e6d4810b81b5e63364febc4e359bc08837a9353d90a232c6dc6b7b15c37` |
| `sol/proof_r07_filtered_transition_defect_closure_v444.md` | 9,953 | 254 | `705afdc595f21f64356b70469a8444708b8a8c8e6306c218e942863a560ef645` |
| `sol/proof_r07_grade1_to_grade2_split_presentation_handoff_repair_v451.md` | 8,050 | 229 | `3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4` |
| `sol/proof_r07_compressed_pair_dag_exact_endpoint_v281.md` | 9,834 | 311 | `dff47329041f6a82b38249c51a5f8d794751349eba602ad99b60582aa5dba228` |
| `search/d972_r07_a0_first_rung_grade1_v4.py` | 144,552 | 3,326 | `1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4` |

## 1. Sign, scale, and recursion

The convention in v464 is correct.  The packed reducer records coefficients
(q_{jp}) with

\[
 r_j=z_j-\sum_{p<j}q_{jp}b_p,
 \qquad b_j=\sigma_jr_j,
 \quad \sigma_j\in\{1,2\}.
\]

In the code, `reduce_packed` subtracts the pivot multiple, and
`_accept_remainder` uses scale 1 for leading coefficient 1 and scale 2 for
leading coefficient 2.  `LiteralExpander.member_update` consequently sends
the origin coefficient (+a_j\sigma_j) and every prior-pivot coefficient
(-a_j\sigma_jq_{jp}).  This is exactly the associated-grade class of

\[
 \left(Z_j\prod_{p<j}^{\longrightarrow}
 W_p^{[-q_{jp}]}\right)^{[\sigma_j]}.
\]

Here coefficient 2 is represented by inverse, as required in an exponent-3
associated grade.  Inverting the whole ordered product when
(\sigma_j=2) reverses it at the exact word level, but that is not a defect:
the SLP records that inverse operation, its grade class is multiplication by
2, and its potentially different higher-grade contribution is precisely why
the next residual must be freshly evaluated.

The recursion is well founded provided the exported typed syntax enforces the
rule already stated in Section 1: every reduction edge and actor-parent edge
targets an earlier node.  The frozen producers create pivot nodes in that
order, and the layer dependency is one-way:

```text
physical grade -> physical lower / block / old
physical lower -> old
block -> defect -> old
old -> projected seed or earlier old actor node.
```

Taking the downward closure of the selected roots therefore terminates.  No
unselected discovery branch is mathematically needed once every referenced
edge has been retained.

## 2. Required filtration and lower-kernel repair

Theorem 2.1 is sound under its intended hypotheses, but the current statement
does not list all of them.  It needs an actor-stable normal filtration:

\[
 F^{d+1}\triangleleft F^d\triangleleft F,
 \qquad P F^iP^{-1}=F^i
\]

for every registered actor word (P) used by the SLP, with
(F^d/F^{d+1}) abelian of exponent three.  The registered actor action must
be the action actually induced by this conjugation.  Likewise, for a
refinement (Q'\to Q), the two source quotient maps must form the commuting
triangle.  Abelian exponent-three quotients alone do not imply either actor
stability or that the recorded linear actor is the induced one.

Under these hypotheses, structural induction gives v464 (2.1), and the
naturality equation (3.1) is exact.  This is only a hypothesis clarification;
the registered R07 tower is intended to provide these commuting maps.

The lower-first sentence after Theorem 2.1 needs a substantive type
correction.  Some selected physical-grade nodes are constructed from old
lifts and physical-lower pivots which individually have nonzero lower parts.
They are not covered by the theorem's premise that every origin already lies
in (F^d).  Moreover, vanishing of the aggregated regular lower block alone
does not prove membership in a source relative kernel.  The exact certificate
must distinguish:

- zero under the complete registered lower physical map, including normalized
  exponent, PB3 augmentation, boundary and every other auxiliary coordinate;
- membership in the corresponding legal physical fibre; and
- membership in a source reduction kernel such as v395's (K^D), which is a
  stronger assertion and follows only from direct source-reduction replay.

For each selected lower-first node, direct evaluation of the exact word SLP
must first prove the applicable complete lower/auxiliary zero and then prove
that its degree-(d) evaluation equals the stored normalized grade row.
Only that pair of equalities licenses the node as the required fibre element.
A coefficient-row cancellation, or “lower physical combination is zero”
without the auxiliary and grade replay, is insufficient.  With this repair,
the lower-first ancestry used by v444/v451 is correctly typed; no relative
kernel surjectivity is inferred.

## 3. The missing complete-correction root

The actual positive finalization path makes the omission in v464 Section 4
decisive:

- line 2703 computes `update = expander.member_update()` from the selected
  physical-grade coefficients;
- line 2716 checks that this update changes no lower/auxiliary coordinate;
- line 2718 forms `canonical_solution["terms"] + update` and only then
  canonicalizes the **accumulated** correction;
- lines 2719--2724 replay that accumulated correction against the complete
  precision-one target; and
- lines 2725--2729 evaluate that accumulated correction at degree two and
  subtract it from the degree-two target.

Thus the SLP called (C_T) in (1.4) is the fibre update satisfying

\[
 [A(C_T)]_d=\rho_d,
\]

not the complete correction whose image is the full target.  Let
(C_{<d}) denote the authenticated earlier correction.  Section 4 must add a
top-level node

\[
 C_d=\operatorname{Compose}(C_{<d},C_T)               \tag{R1}
\]

in the exact registered source composition order (for the present finalizer,
the order corresponding to `canonical_solution + update`).  The checker must
replay (C_d), not (C_T) alone, against the full grade-one target and must
compute

\[
 \rho_{d+1}=\operatorname{gr}_{d+1}
       \bigl(T-A(C_d)\bigr)                           \tag{R2}
\]

only after all lower and auxiliary coordinates vanish.  The prior correction
must itself be an authenticated literal-word SLP (a fixed ordered product of
its already registered literal terms is enough).

This repair also pins the noncommutative order which a flattened F3 term map
currently discards.  Any other ordering with the same associated-grade class
is a possible lift, but it generally changes (R2), so the certificate must
choose one and replay that same one.

## 4. Selected ancestry is sufficient after one explicit payload repair

The frozen states contain enough information to build the selected SLP.  The
present `LiteralExpander` demonstrates the dependency graph:

- `member_coefficients` select physical-grade roots;
- `physical_grade_dag` supplies their scale, ordered grade reductions and
  either block-basis or old-connection origin, including lower reductions;
- `physical_lower_dag` supplies the selected lower-pivot ancestry;
- each character block's `dag_nodes` supplies defect/actor origins, scale and
  ordered reductions;
- `prepare.defect_origins`, together with the selected old
  `seed_reductions` or `actor_transitions`, expands each seed or transition
  defect; and
- the selected old `dag_nodes`, exact relator words, pure-Q1 actor words and
  literal actor labels terminate the recursion.

The last-but-one item is not itself a DAG-node edge.  Section 4 item 3's phrase
“every origin” must therefore be made explicit: a pruned handoff must include
each reached `defect_origin` and the particular reached seed-reduction or
actor-transition expression from the authenticated prepare state.  It must
also include the earlier correction root from Section 3 above.  Without those
records, a standalone checker reaches the analogue of code lines 2405--2421
and cannot continue to old nodes.

With those two additions, the finite payload is sufficient.  Its canonical
encoding must bind node type, node index, ordered child/edge list, scale,
origin, literal leaf word, actor word, selected root coefficient, the complete
root (R1), and the parent decision/state digests.  An independent interpreter
can then evaluate each selected node once per quotient and evaluate the same
root separately in each of the eleven registered occurrences, using that
occurrence's substitution, prefix and sign before physical aggregation.
Neither the entire discovery DAG nor a flat leaf multiset is required.

This is not optional provenance decoration: the two non-DAG relation records
and the complete root are required to make the selected syntax executable.
Conversely, demanding all unselected nodes, a second discovery pivot order,
or full flat materialization would be optional hardening and is rejected.

## 5. Common-source explicitness, v281, and claim boundary

A finite acyclic SLP with literal free-word leaves and literal group
operations is a constructive definition of one element of the free source
group.  Authentication fixes that syntax; memoized evaluation is merely an
efficient interpretation of the same element.  Therefore it is a genuinely
explicit common-source word, even if its exponentially longer flat letter
list is never allocated.  For compatible quotient maps, structural induction
proves that all evaluations are reductions of this one source word.  This is
syntactic naturality, not a family of unrelated finite-stage coefficient
choices.

V464 does not weaken v281.  V281's factored-pair A7 ZERO gate still separately
requires expanded literal pairs, helper-nonshared exact endpoint replay and
full-chain reconstruction.  V464 expressly supplies a different positive
representative for the current filtered correction and requires fresh direct
replay.  Its “no flattening” conclusion must not be imported into v281's A7
positive gate.

Finally, evaluating one SLP at every quotient proves compatibility of its
values, not that those values solve every quotient problem.  V464 neither
proves (B_{n+1}(K^D_n)=K^L_n), supplies v395's right inverses, nor proves the
class-specific defect membership at future edges.  It also states that the
actual grade-one coefficients/SLP are unavailable.  Consequently no
relative-kernel surjectivity, cofinal existence, compatible lift, A0, COMMON,
fake, or Ihara conclusion follows.

## Exact load-bearing paper repair

Make one versioned successor to v464 and only:

1. add the actor-stable normal-filtration, induced-action, and commuting
   quotient-map hypotheses to Sections 1--3;
2. replace the lower-first paragraph by the typed complete lower/auxiliary and
   associated-grade direct replay in Section 2 above, explicitly separating a
   physical fibre from a source reduction kernel;
3. distinguish “(C_T) solves the selected grade residual” from “the complete
   correction hits the target,” add the authenticated prior-correction SLP and
   complete root (R1), and require (R2) from that root;
4. add reached `defect_origin` records and their reached old
   seed/transition-reduction expressions to Section 4's selected payload, and
   bind a canonical ordered SLP encoding to the decision and state digests;
5. qualify the three `PAPER-CLOSED` SLP lines by these hypotheses and retain
   every existing non-surjectivity, fresh-residual, v281 and no-cofinality
   boundary.

No implementation change, materialized flat expansion, full-DAG export,
additional computation, or optional mutation/hardening campaign is required
by this verdict.
