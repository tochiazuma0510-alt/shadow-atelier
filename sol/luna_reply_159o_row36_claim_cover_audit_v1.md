# Luna 159o post-literal audit -- row-36 full-fibre / CLAIM-COVER gate

Date: 2026-08-24 (JST)  
Role: Luna, read-only mathematical/evidence-contract audit  
Scope: corrected class-3 pent canaries versus the fixed row-36 joint fibre  

## 1. Ruling

```text
P2_QUOTIENT_CANARY_CROSSCHECKED_SCOPED
P3_QUOTIENT_CANARY_PRODUCER_ONLY__CHECKER_PENDING
ROW36_FULL_FIBRE_NOT_MATERIALIZED
CLAIM_COVER_PENT_CANARY_2_NOT_CLOSED
NO_MODE_TOKEN__NO_RUNG_NAME__NO_EXECUTION
```

The complete quotient-level `(m,f)` canaries do **not** close the fixed row-36
full-fibre/`CLAIM-COVER-PENT-CANARY-2` gate, even when combined with the existing
paper proof of isolation/diamond, the marked common-quotient computation, and the
proved raw cardinalities 64 and 34,992.

A separate prime-local materialized row-fibre receipt and helper-disjoint checker
remain mandatory for **both** `p=2` and `p=3` under the frozen 159o contract.  The
large quotient canaries need not be rerun; the missing job is the bounded marked
joint-kernel/row-fibre bridge and its complete per-row predicate ledger.

## 2. Why quotient completeness is not row-fibre coverage

Write

```text
Q_p = F2 / D4_p(F2),
U_p = the canary's complete quotient-level (m,q) universe,
R_p = the raw reduction fibre above the frozen zero-based row 36 in
      J_p = PB3 / (K1 cap D4_p(PB3)).
```

The corrected canaries enumerate

| prime | `|Q_p|` | canary `m` range | `|U_p|` | actual charming+onto | nonidentity defect |
|---:|---:|---:|---:|---:|---:|
| 2 | 128 | 4 | 512 | 8 | 0 |
| 3 | 2,187 | 9 | 19,683 | 18 | 0 |

The row-36 fibre is a different typed set.  With `L=ker(G36 -> G9)`, the already
proved isolated equality `H_p^diamond=H_p`, and maximal common quotient `C_p`, it is

```text
R_p = {(m, j_* z) : m in {0,18}, z in Z_p},

Z_2 = {(l,1,q) : l in L, q in Q_2, alpha(l)=beta(q)},  |Z_2|=32,
Z_3 = L x {1_PSL} x Q_3,                              |Z_3|=17,496.
```

Hence

```text
|R_p| = 16*|Q_p|/|C_p|,
|R_2| = 64       because |C_2|=32,
|R_3| = 34,992   because |C_3|=1.
```

In particular, neither canary universe is the row fibre: `512 != 64` and
`19,683 != 34,992`.  For `p=3`, forgetting the K1 coordinate and reducing the two
central lifts modulo 9 maps 16 row entries to each `q`; this is visibly not a
bijection with the quotient canary universe.

There is a useful abstract implication.  Once the marked projection from `J_p` to
`Q_p` is authenticated, a joint charming+onto row projects to a quotient-level
charming+onto pair, and the five-coface defect is natural under this projection.
Thus a complete blind `U_p` canary can certify that every **already identified**
actual row candidate has trivial class-3 defect.  It cannot identify those joint
candidates or prove their coverage.  It supplies none of the following missing
row data:

1. the explicit marked joint kernel and every element of its row-36 coset;
2. reduction of every materialized word to the exact frozen seed key;
3. which rows pass the two gentle hexagons, charming, and onto in the **joint**
   quotient (passing after projection is only a necessary condition);
4. candidate count equals evaluated count, no omission/duplicate, all rejection
   reasons, and the row-level defect histogram;
5. the frozen requirement that `Dpap(f)` be tied to the same representative word
   used for that row.

The cardinality proof proves the size of `R_p`; a cardinality is not an enumerated
coverage receipt.  Even granting the projection/naturality lemma, it closes only
the defect-value component, not `CLAIM-COVER-PENT-CANARY-2`.

## 3. The frozen contract and the receipts say this explicitly

Sol section 22.5 freezes four gates.  Its fourth gate requires both the instrument
canary and the row-36 full-fibre canary to be producer/checker-separated and
cross-checked.  `sol/luna_task_159o_ladder_launch.md` section 3 separately requires
the isolated/diamond refinement, complete row-36 fibre, and
`CLAIM-COVER-PENT-CANARY-2`.  Section 4 freezes the expected values 64 and 34,992
as predictions and states that they are not substitutes for materialization.

The immutable artifacts agree with that scope boundary:

- The p2-v14 receipt records both `deferred.row36_full_fibre` and
  `deferred.claim_cover_pent_canary_2` as `NOT_IN_V5_P2_BOUNDED_STAGE`.
- Its independent v6 verdict passes the quotient canary but records
  `scope.row36_full_fibre_crosschecked=false` and
  `scope.claim_cover_crosschecked=false`; its `DEFERRED_SCOPE_NOT_PROMOTED` check
  is a PASS.
- The p3-v5 producer receipt records the analogous two fields as
  `NOT_IN_P3_V5_BOUNDED_STAGE`.  Its helper-disjoint checker is still pending.
- The producer addendum section "Scope boundary and firewall" also states that
  the complete row-36 fibre and `CLAIM-COVER-PENT-CANARY-2` remain outside both
  bounded receipts.

Therefore promoting either quotient receipt into a row-fibre receipt would
contradict both its own schema and the independent p2 verdict.

## 4. Status of the four Sol 22.5 gates

| gate | current status | reason |
|---|---|---|
| corrected PB4 quotient separates degree-3 Brunnian data | p2 cross-checked in scoped canary; p3 producer candidate, checker pending | quotient-level evidence only |
| corrected PB3 quotient plus fixed-rung joint quotient and actual index | quotient orders measured; special joint structure/cardinality proved in preflight, but joint materialization receipt/checker absent | not frozen as an execution receipt |
| refined rung isolation | abstract paper proof closed: `H_p` isolated and `H_p^diamond=H_p` for p2,p3 | no diamond enlargement |
| instrument plus row-36 full-fibre canary | p2 instrument cross-checked; p3 instrument checker pending; neither row fibre materialized/cross-checked | gate open |

Thus the global first outstanding predecessor datum is the p3-v5 independent
checker verdict.  Independently of its outcome, the first missing datum specific
to the row gate is

```text
MARKED-QP-COLLECTOR-AND-JOINT-KERNEL-MATERIALIZATION-RECEIPT
```

## 5. Smallest bounded implementation and handoff contract

Do not rerun the 512- or 19,683-entry quotient canaries.  Produce two versioned,
prime-local bridge receipts, p2 first and p3 second, with the following exact
contract.

### 5.1 Frozen inputs

Each manifest binds by path/bytes/SHA-256:

- the fixed K1 marked quotient/reduction artifacts;
- the frozen row-36 full row, target key, and archived word digests;
- the applicable marked `Q_p` collector/presentation and literal Q4 coface maps;
- the common-quotient proof data (`|C_2|=32`, `|C_3|=1`) and maps `alpha,beta`;
- the isolation proof pin and equality `H_p^diamond=H_p`;
- the applicable canary receipt and independent verdict.  The p3 bridge may not
  start before the p3 checker verdict exists and passes.

### 5.2 Materialized joint fibre

Reconstruct the marked image in the K1-by-`Q_p` product rather than asserting its
order.  Emit the marked generators, projections, joint kernel, actual index, and
the common-quotient compatibility checks.  Then deterministically:

1. enumerate the eight `L=ker(G36 -> G9)` elements in frozen G36 code order;
2. enumerate `Q_p` Hall exponent vectors lexicographically;
3. for p2 retain precisely `alpha(l)=beta(q)`; for p3 retain every `(l,q)`;
4. order by `m=0,18`, then L code, then Hall vector;
5. materialize all 64 or 34,992 entries, including joint coordinates, a canonical
   signed source word, word digest, and exact reduction to the row-36 key.

The receipt must bind raw-count/evaluated-count equality, uniqueness, the complete
roster digest, and a no-omission proof against the displayed coordinate rule.

### 5.3 Complete row predicate

For every materialized row, using its same signed word, record separately:

1. literal gentle hexagon (3.10);
2. literal gentle hexagon (3.11);
3. charming;
4. onto in the full joint quotient;
5. exact reduction to row 36;
6. literal five-coface `Dpap` in `PB4/D4_p(PB4)`.

Record sequential counts, every rejection reason, the complete defect histogram,
the actual-survivor roster/digest, and

```text
CLAIM-COVER-PENT-CANARY-2:
raw_count = evaluated_count = expected_count,
no omission, no duplicate, all rows reduce to the frozen key.
```

The cross-checked quotient canary may be cited as an additional projection check,
but under the current frozen contract it does not replace the same-word row
evaluation.  Replacing direct evaluation by a lookup/naturality bridge would need
an explicit Sol contract amendment.

### 5.4 Mandatory destructive checks

At minimum fail on: one row omitted; one row duplicated; `C_2` replaced by a
trivial/direct-product common quotient; a Hall coordinate or marked generator
changed; row 35/37 substituted; central lifts `{0,18}` changed; non-isolated input;
charming accepted without onto; one hexagon omitted; a row word changed between
joint predicates and `Dpap`; receipt or aggregate digest mutation.

### 5.5 Independent checker firewall

The checker handoff is only the immutable receipt/manifest tuple.  A separately
authored checker reconstructs the marked collectors, common-quotient condition,
joint kernel, all 64/34,992 rows, reductions, predicates, counts, and digests from
the frozen upstream inputs.  It must not open or import producer source, helpers,
effective source, logs, or producer report.  No row gate is cross-checked until
both prime-local verdicts pass.

## 6. Evidence pins

| artifact | bytes | SHA-256 |
|---|---:|---|
| `sol/luna_reply_159o_k2_preflight.md` | 34,658 | `461c5e60e13c4034dcb7f2fcef87e42d8b7dfd5b1f6148a944a4d8bae7d42e26` |
| `scratchpad/d972_idx3_arith_datum_independent_v1.md` | 96,640 | `a2fae0a0365a8f1587781c797120a25532b6d274dedc609bad11c0c22082e31a` |
| `sol/luna_task_159o_ladder_launch.md` | 12,324 | `08be5089fcedd8232b39feb3e7491a83b3dad001ca4c2be122491c5acc7dc85a` |
| `sol/luna_task_159n_pent_canaries.md` | 9,602 | `210f2d2de0001d09fffbdd85e6473c2c4627927b0c17e1211ca2580f5b0ebff5` |
| p2-v14 producer receipt, run `32660080668` | 234,702 | `2722e4acfd7087a613bdc63b15a8741c34c84480658682565e3b5af833f75ed5` |
| p2-v14 manifest | 7,566 | `199178782a709723e215e37e6be32346ce369b6ad4335679a0770d64ec3d6fe2` |
| p2 independent v6 verdict | 16,438 | `ef159dbc01d2e0e8ddc536707270b10207cd2654a08ee9a4dd60dd6201a5455a` |
| p2 independent v6 report | 6,412 | `3a912c3afd626ec9075a37f04a1f4a2e4a9c9b672054ae199df3b0131d5d6388` |
| p3-v5 producer receipt, run `32661138818` | 5,223,102 | `8838dbfecbb8f487265801de860c91207de56e4acf5e98088e6d9cd161390530` |
| p3-v5 manifest | 9,376 | `0cb50bd91f65611f52643de082ba9f317b75716ee12545c7e4a285cde61cfe9e` |
| p2-v14/p3-v5 producer addendum | 7,527 | `3d94c8c5f46cf17eb93af47046220e088bd5da53409a03898cee48d2d1101259` |

No producer or checker was executed, no mode token was issued, no rung was named,
and no git, GHA, workflow, or es7ops action was taken in this audit.

```text
ROW36_CLAIM_COVER_STATE_STOP__P3_CHECKER_AND_64_34992_MATERIALIZED_BRIDGES_REQUIRED
```
