# R07 final-heavy carrier to actual A2 splice theorem (v300)

## 0. Scope

V289 gives a version-independent semantic carrier for an accepted positive
A0 word, while v299 replaces the copied preselection summary by the
checker-local final carrier

\[
 H^*=(P0,\text{sources},\text{authorities},
      \operatorname{OwnerPre}(T176),\operatorname{Sel}(r)).
\]

This note proves the exact splice between those two objects.  It fixes what a
future v12b COMMON receipt must export and shows that the already
cross-checked v225 A2 specializer does not need A0's global search tables.
It is a paper theorem only.  V12a remains candidate-only, no v12b COMMON
receipt exists, and no actual A2, lift, fake, or Ihara witness is claimed.

## 1. Positive projection of the selected statement

Let an **accepted production carrier** be a tuple

\[
 \mathcal A_{12b}=(R_b,V_b,M_b),
\tag{1.1}
\]

where `R_b` is a future v12b COMMON receipt, `V_b` is its separately
implemented positive checker verdict, and `M_b` binds their physical bytes,
sources, immutable run, and accepted v12a bootstrap owners.  In particular,
`V_b` has independently reconstructed the v299 objects

\[
 \operatorname{OwnerPre}_{\rm chk}(T176)
 =\operatorname{OwnerPre}_{\rm prod}(T176),
 \qquad
 \operatorname{Sel}_{\rm chk}(r)=\operatorname{Sel}_{\rm prod}(r).
\tag{1.2}
\]

Neither a v12a `V12A_SELFTEST_BOOTSTRAP_ARTIFACT` nor an UNKNOWN/resource
terminal is an accepted production carrier.

The correction part of `Sel(r)` must have the following typed subobject.  The
field names used by an implementation may differ, but its registered decoder
must establish these meanings rather than infer them from a digest.

```text
Pos(Sel(r)) = {
  base_word:       g0,
  correction_word: a,
  corrected_word:  f,
  correction_factors:
      [(selected_row_key, coefficient, literal_factor)],
  exponent_pair:   (0,0),
  occurrence_replay: omega_occ,
  direct_replay:     omega_dir
}
```

The ordinary producer and checker validators separately require

\[
 a=\operatorname{red}(a),\qquad
 f=\operatorname{red}(f)=\operatorname{red}(g_0a),\qquad
 \operatorname{exp}(a)=(0,0),
\tag{1.3}
\]

and reconstruct `a` in the registered selected-row order.  Coefficient two
uses the inverse literal factor and the negative row over \(\mathbf F_3\).
They also require all eleven typed occurrence values and the direct H1/H2/P
values in `omega_occ,omega_dir` to equal their own replay.  Equality of
lengths, hashes, or a producer Boolean cannot replace these checks.

Define the stable positive projection

\[
 \Pi_+(H^*)=(g_0,a,f,\omega,\iota),
\tag{1.4}
\]

where \(\omega=(\omega_{\rm occ},\omega_{\rm dir})\), and \(\iota\) is the
closed dialect tag together with the physical identities of
`R_b,V_b,M_b`, their exact positive terminals, `h_final*`, and the transitive
v12a/P0/task176 authority root.  `RunPre`, unselected K0 tables, checkpoint
rows, worker schedules, and mutation ledgers do not occur in (1.4).

## 2. Independent decoder obligation

There must be two decoder implementations

\[
 D_{12b}^{\rm prod}(R_b,V_b,M_b),\qquad
 D_{12b}^{\rm chk}(R_b,V_b,M_b).
\tag{2.1}
\]

Each opens and validates the three physical owners and the closed v12b
dialect before extracting `Pos(Sel(r))`.  The checker decoder may use the
accepted v12b verdict's physical binding but may not import the producer
decoder or read a producer-supplied `positive_projection` as authority.
Acceptance requires

\[
 D_{12b}^{\rm prod}=D_{12b}^{\rm chk}=\Pi_+(H^*)
\tag{2.2}
\]

as typed canonical objects, as well as (1.3) and the literal replay
equalities.  A2 may serialize (2.2) as a small adapter receipt, but the A2
checker must reconstruct it from the original three owners.

This creates no physical-hash cycle.  The future order is

```text
v12a sources -> P0a -> bootstrap Ra -> bootstrap Va
                         |
                         v
v12b sources/P0b (pin Ra,Va) -> production Rb -> production Vb -> A2
```

`P0b` does not predict `Rb` or `Vb`; their physical binding is supplied by
`Mb` after production.  A2 points only backward along this DAG.

## 3. Splice theorem

### Theorem 3.1 (FINAL-CARRIER POSITIVE PROJECTION)

Assume:

1. `R_b,V_b,M_b` form an accepted positive v12b production carrier;
2. v299's independent `OwnerPre` and selected-statement equalities pass;
3. both decoders satisfy (1.2)--(2.2); and
4. the accepted task198 word-independent interface is fixed.

Then \(\Pi_+(H^*)\) is exactly a v289 stable semantic carrier and supplies
the full literal-word premise of the v225 A2 specializer.  The resulting A2
package

\[
 \mathcal S_{\rm PB}
   =\bigl((B(o),\rho_o,\sigma_o,P_o,\xi_o)_{o=1}^{11},
          (\epsilon_B)_{B=H1,H2,P},w,\bar\epsilon_1,u_0\bigr)
\tag{3.1}
\]

is independent of `RunPre`, the unselected global search trajectory, and the
chosen v12 implementation of that trajectory.

#### Proof

By v299, equality of the independently built `OwnerPre` objects binds the
same frozen task176 and primitive owners, while equality of the two
`Sel(r)` objects binds the same actual selected Q0/Gamma/K0/kernel/dual and
literal correction.  The ordinary validators, not canonical equality alone,
establish (1.3) and the two literal replay equalities.  Thus (1.4) satisfies
all authentication and word conditions of the stable carrier in v289.

V225 constructs each occurrence prefix, sign, group key, and
\(\xi_o=\rho_o(g_0)^{-1}-1\) from \(g_0\) and the fixed task198 ledger.  It
constructs the residual endpoints from the corrected word \(f\), then
projects them through the pinned Q3/Q4 and \(D_1\) maps.  None of these
operations reads an unselected A0 row, table, cursor, checkpoint, or worker
event.  Therefore the output is precisely (3.1) and is extensional in
\(\Pi_+(H^*)\) and task198.  QED.

### Corollary 3.2 (NO SECOND GLOBAL SEARCH IN A2)

After an accepted v12b COMMON carrier exists, actual A2 specialization needs
only the two small decoders, literal word/replay validation, and the existing
v225 PB construction.  Reopening the full task176 global roster or rebuilding
the ten 1,469,664-state A0 tables cannot strengthen the A2 equality and is
forbidden as avoidable work.

This does not mean A2 may trust a digest.  The heavy work is discharged by
the accepted upstream producer/checker pair; A2 still performs two physical
decodings and independently reconstructs all of its own occurrence, Fox,
Q3/Q4, and endpoint mathematics.

## 4. Exact implementation handoff

Once the v12b schema is frozen, the only new A2 predecessor work is a
versioned branch satisfying Section 2.  The existing cross-checked v225
specializer remains unchanged.  Required ordinary-validator mutations are:

1. v12b dialect and exact positive producer/checker terminals;
2. each physical `R_b,V_b,M_b` identity and verdict-to-receipt binding;
3. `h_final*`, the v12a bootstrap root, and the task176 transitive root;
4. one letter and the order in each of \(g_0,a,f\);
5. one selected factor, coefficient-two inversion, and free reduction;
6. one typed occurrence replay and one direct H1/H2/P replay; and
7. task198 physical identity and one ledger slot.

Every mutation is applied to an owner before the ordinary decoder and must
produce one narrow first rejection.  No A0 search, resume, K0, or checkpoint
mutation belongs in this downstream adapter.

## 5. Fixed frontier

```text
H* -> STABLE POSITIVE CARRIER:          PAPER PROOF
STABLE CARRIER -> V225 ACTUAL PREMISE:  PAPER PROOF (v289 + v300)
SECOND A0 GLOBAL BUILD INSIDE A2:       PROVED UNNECESSARY
V12A BOOTSTRAP ARTIFACT AS A2 INPUT:    FORBIDDEN
V12B COMMON / DECODER IMPLEMENTATION:   NOT YET AVAILABLE
ACTUAL A0 / A2:                         0/1 / 0/1
ACTUAL A3, LIFT, FAKE, IHARA:           NONE
```

`R07_FINAL_HEAVY_CARRIER_TO_ACTUAL_A2_V300_PAPER_GRADE`
