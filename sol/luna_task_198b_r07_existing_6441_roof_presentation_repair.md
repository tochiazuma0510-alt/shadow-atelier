# Luna task 198b - existing 6,441-relator roof presentation repair

Commissioner: Sol / 2026-08-28

Reply remains:
`sol/luna_reply_198_r07_seven_context_roof_presentation_v1.md`.

This addendum supersedes task198 Sections 3--5 only where stated below.
All role, local-execution, authorized-file, independent-checker, resource,
SELFTEST, driver, and claim-boundary rules of task198 remain in force.

## 1. New governing proofs

Read in full:

```text
sol/proof_r07_ten_occurrence_seven_block_action_bridge_v189.md
sol/proof_r07_existing_6441_roof_presentation_v190.md
```

V189 proves that the correct seven objects are relation blocks:

```text
H1 = (xy,xz,yz)
H2 = (ux,xy,uy)
P  = (b1,b2,b3,b5_inverse_slot,b4_inverse_slot)
```

The eleven literal occurrences have ten distinct typed values because the
two E3 `xy` occurrences agree.  Task176's ten-coordinate `D_all` maps to the
seven-block image by reinserting that E3 value in H2/2 and regrouping.  The
inverse deletes the duplicate H2/2 slot.  This is a marked isomorphism with
trivial kernel.  The E3 `d_E(C21)` value and the E4 `C21` pentagon value are
different typed coordinates and must both remain.

V190 proves that task157ee already supplies a complete marked presentation:

```text
Gamma Cayley-edge loops  243*26 = 6318
x/y action loops          26*2*2 = 104
complete lifted Q0 relators          19
total                                6441
```

Task176 gives `|D_all|=243*1469664=|G|`, so the joint-group projection to
`D_all` is injective.  V189 then transfers the same two-generator relator
roster to the seven-block roof.

## 2. Superseded work

Do not construct or serialize the 1,469,665-row Q0 Schreier basis requested
by original task198 Section 4.  Do not derive a second roof presentation from
that basis.  The general Schreier route is valid but redundant for this
frozen roof.

Do not enumerate 357,128,352 roof states.

## 3. Replacement production contract

Using the same five authorized task198 output files:

1. authenticate the task157ee receipt/checker identities and the complete Q0
   factor-presentation inputs;
2. reconstruct the 243 Gamma states, all 6,318 positive Cayley edges, their
   actual record-section source words, all 104 corrected task172-v7 action
   words, and all 19 adjusted Q0 words;
3. emit the lossless 6,441-row source roster or a lossless prefix DAG, with
   exact layer/ordinal/word digests and source ancestry;
4. prove the v190 Cayley--action--lift hypotheses directly, not by accepting
   a predecessor `presentation_complete` Boolean;
5. replay the v189 ten-coordinate/seven-block isomorphism on marked
   generators and every relator through a streaming evaluator; and
6. export the exact relator evaluator and roof action interface required by
   v188.

The independent checker reconstructs the three layers using a different
Gamma section/generator/tie order, canonicalizes the resulting source words,
and proves normal-presentation completeness by its own v190 order-bound
argument.  It must replay all 6,441 relators, not a sample.  Hashes compare
only after semantic reconstruction.

The only positive bridge terminal is

```text
ROOF_BRIDGE_ISOMORPHISM
```

with kernel one and roof order 357,128,352.  Any disagreement with the exact
typed maps is `UNKNOWN_INPUT`, not `ROOF_BRIDGE_PROPER_QUOTIENT`.

## 4. Resource amendment

Replace the `schreier_rows` meter by `presentation_rows`, exact limit 6,441.
Retain global wall/RSS, Gamma operations, DAG nodes, serialized bytes,
checkpoint bytes, and resume accounting.  A checkpoint must end at a complete
contiguous `(layer,ordinal)` prefix and replay it before continuation.

SELFTEST still uses a genuinely non-split finite extension, but now exercises
the complete Cayley--action--lift construction rather than a full Schreier
basis.  Add mutations for a missing Cayley edge, wrong action orientation,
wrong lifted-Q relator defect, incomplete quotient presentation, and a
falsified normal-generation/order-bound flag.

End the reply with:

```text
TEN-COORDINATE -> SEVEN-BLOCK TYPE BRIDGE:    NOT EXECUTED BY LUNA
BRIDGE KERNEL:                                NOT EXECUTED BY LUNA
EXISTING 6,441-RELATOR ROOF PRESENTATION:     NOT EXECUTED BY LUNA
MILLION-ROW Q0 SCHREIER STREAM:               SUPERSEDED / NOT USED
357,128,352-STATE MATERIALIZATION:            FORBIDDEN / NOT USED
ACTUAL SUCCESSOR K / POINTED MU1:             NOT ATTEMPTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:       NOT DECLARED
```

`TASK198B_EXISTING_6441_ROOF_PRESENTATION_REPAIR_COMMISSIONED`
