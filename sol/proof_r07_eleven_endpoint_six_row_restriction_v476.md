# R07: eleven endpoint gates and the six-row precision-two restriction (v476)

Author: Sol / 2026-09-03

Status: candidate typing repair for the v470--v471 precision-two consumer.
It distinguishes the eleven endpoint slots of the full all-seven interpreter
from the six occurrence rows of the current two-hexagon first-rung quotient.
It constructs no payload or residual and proves no grade decision, A0,
COMMON, cofinal lift, fake, or Ihara conclusion.  `verified=false`.

## 1. The two ordered occurrence lists are different objects

Let \(F=F(x,y)\), put

\[
 z=(xy)^{-1},\qquad u=(yx)^{-1},
\]

in the frozen displayed-word convention, and let \(J_{11}\) be the ordered
actual list used by the direct all-seven evaluator:

| ordinal | label | quotient | sign | endpoint-coordinate |
|---:|---|---|---:|---:|
| 1 | `H1_fxy` | \(E_3\) | \(+\) | 0 |
| 2 | `H1_fxz` | \(E_3\) | \(-\) | 1 |
| 3 | `H1_fyz` | \(E_3\) | \(+\) | 2 |
| 4 | `H2_fux` | \(E_3\) | \(-\) | 3 |
| 5 | `H2_fxy` | \(E_3\) | \(-\) | 0 |
| 6 | `H2_fuy` | \(E_3\) | \(+\) | 4 |
| 7 | `P_b1` | \(E_4\) | \(+\) | 5 |
| 8 | `P_b2` | \(E_4\) | \(+\) | 6 |
| 9 | `P_b3` | \(E_4\) | \(+\) | 7 |
| 10 | `P_b5_inverse` | \(E_4\) | \(-\) | 8 |
| 11 | `P_b4_inverse` | \(E_4\) | \(-\) | 9 |

Thus the eleven-to-ten endpoint-coordinate list is

```text
[0,1,2,3,0,4,5,6,7,8,9].
```

The repeated coordinate zero is not a repeated occurrence: ordinals 1 and 5
have different physical blocks, signs, and prefixes and remain distinct
receipt slots.  The five \(E_4\) pairs and the prefix of every slot are the
exact `pcontexts` / `raw_specs` / reverse-block prefix records of the actual
v12f owner; their printed labels do not license reconstructing a different
factor order.

Write

\[
 H_6=(1,2,3,4,5,6),\qquad P_5=(7,8,9,10,11).        \tag{1.1}
\]

There is a canonical restriction of ordered endpoint tuples

\[
 \pi_H:\prod_{j\in J_{11}}E_j\longrightarrow E_3^6,
 \qquad(g_1,\ldots,g_{11})\longmapsto(g_1,\ldots,g_6). \tag{1.2}
\]

It is merely coordinate restriction.  It is not a homomorphism from five
pentagon Fox rows into the six hexagon Fox rows.

## 2. Why the present residual has only six row slots

The current first-rung branch is the exact necessary projection fixed in
v437 (4.4): it keeps the two registered hexagon gradients and normalized
exponents and **drops the PB4 block**.  At higher precision, v445 (2.4),
v446 (1.4), and v451 retain the corresponding occurrence source

\[
 \mathcal O_H=igoplus_{h\in H_6}k[Q_2]^2              \tag{2.1}
\]

before applying the signed prefixes and the two-hexagon physical map.  The
six source slots have signs and target blocks

```text
(H1_fxy,H1_fxz,H1_fyz) -> (block 0; +,-,+)
(H2_fux,H2_fxy,H2_fuy) -> (block 1; -,-,+).
```

For one character and one degree-two monomial the physical target has

\[
 2\text{ hexagons}\cdot2\text{ Fox components}\cdot504=2016
                                                               \tag{2.2}
\]

coordinates.  With four characters and six coupled degree-two monomials the
fresh top block is consequently

\[
 4\cdot6\cdot2016=48,384,                              \tag{2.3}
\]

while its registered lower/auxiliary block has

\[
 8,064+24,192+4=32,260                                \tag{2.4}
\]

coordinates.  Neither number contains a pentagon Fox-row coordinate.

This is not a claim that the pentagon change is zero.  It says only that the
present first-rung residual is computed after a typed projection whose target
does not contain that block.  A full all-seven or later B4 certificate must
evaluate the five pentagon rows in its own \(E_4\)-typed physical module.

## 3. Restriction of the leaf formula

Let the authenticated Task625 source graph and prior root give the exact
finite leaf coefficient map

\[
 \mu:(s,P)\longmapsto\mu_{s,P}\in\mathbf F_3,          \tag{3.1}
\]

including the registered terms of \(C_{<1}\), the selected update \(C_T\),
and their ordered complete root \(C_1\).  For every path define the complete
endpoint signature

\[
 \Sigma_{11}(P)=\bigl(\eta_j\theta_j(P)\bigr)_{j\in J_{11}}. \tag{3.2}
\]

Assume, as in v470, the directly replayed endpoint gate

\[
 \eta_j\theta_j(r_s)=1                               \tag{3.3}
\]

for every reached seed and all eleven slots.  For a complete signature
\(\tau\), put

\[
 \bar\mu_{s,\tau}
 =\sum_{P:\Sigma_{11}(P)=\tau}\mu_{s,P}.             \tag{3.4}
\]

### Theorem 3.1 (full endpoint signature, six-row output)

For every \(h\in H_6\),

\[
 \boxed{
 D_h(C_1)=\sum_{s,\tau}\bar\mu_{s,\tau}\,
                 (\pi_H\tau)_hD_h(r_s).}             \tag{3.5}
\]

Applying the six fixed prefixes/signs and the registered occurrence-first
aggregation to (3.5) gives exactly the current two-hexagon replay through
precision two.

#### Proof

The endpoint-one Fox conjugate identity gives, occurrencewise,

\[
 D_h(Pr_sP^{-1})=\eta_h\theta_h(P)D_h(r_s).
\]

Summing the exact leaves gives v470's formula for each \(h\).  Equality of
complete signatures implies equality of their first six coordinates, so
regrouping by (3.4) proves (3.5).  Prefix translation, sign, PB3 normal map,
and aggregation are fixed linear maps applied only after the occurrence rows;
they preserve the equality. \(\square\)

The use of \(\Sigma_{11}\) is deliberately finer than necessary for the
six-row value.  Two paths with equal \(H_6\) endpoints but unequal \(P_5\)
endpoints could be combined for the projected row, but must not be combined
in a reusable full all-seven/P receipt.  Keeping all eleven therefore
preserves the stronger future handoff without changing the present sum.

## 4. Exact consumer contract

A consumer of a successful Task625 payload must perform the following typed
steps in order.

1. Authenticate the Task595 decision, Task625 producer manifest and
   independent checker verdict, exact three roots, canonical source graph,
   literal dictionary, and compact `R07LEAF1` stream.  Recompute the exact
   leaf table; the binary stream is a comparison target, not graph authority.
2. Seal the ordered eleven-context table above, including the actual five
   `pcontexts`, the coordinate list, quotient type, substitution, inverse
   sign, and fixed prefix.  Directly check (3.3), with repeated slots retained.
3. Build or independently evaluate the exact prefix trie for
   \(\Sigma_{11}\) and seal every exact-path-to-signature assignment and
   every nonzero (3.4) bucket.  Signature equality is used only after exact
   paths and the endpoint gate have been retained.
4. Authenticate entrywise that the Task565/v451 six occurrence matrices,
   crossed cochains, marked generator images, signs, and prefixes are exactly
   ordinals 1--6 of the actual table.  This is a six-to-six identity check,
   not `% 6` and not an eleven-to-six algebraic adapter.
5. Evaluate seed derivatives only in the six \(H_6\) slots for the current
   row, apply (3.5), and then apply the two-hexagon physical chain.  Keep the
   five \(P_5\) endpoint records, but do not inject their Fox rows into this
   target and do not assert their contribution is zero.
6. Evaluate the correspondingly projected target independently.  Replay all
   32,260 lower/auxiliary coordinates, compare the selected degree-one update
   separately with Task595/Task625, and require zero lower difference.
7. Only then seal the 48,384-trit fresh \(\rho_2\), its 12,096-byte packing,
   support, sparse digest, packed digest, and every parent hash.  This is an
   input to the grade-two decision, not a MEMBER result.

The producer and checker may implement the same ordered mathematical table,
but they must obtain it from separately pinned data or independent literal
construction.  A six-tag placeholder table, `% len(tags)`, or reuse of one
slot's prefix for another fails the contract.  Resource exhaustion is
`UNKNOWN_RESOURCE` and cannot produce an empty or negative result.

## 5. Scope and claim boundary

Theorem 3.1 repairs an interface ambiguity only.  It does not promote the
v437 two-hexagon necessary projection to the full A0 equation.  In
particular, a positive result in all six first-rung grades still leaves the
typed PB4/B4 component and the later compatibility gates.

```text
ACTUAL ELEVEN ENDPOINT ORDER:                 FIXED ON PAPER
CURRENT 48,384-TRIT OUTPUT SLOTS:             FIRST SIX H OCCURRENCES ONLY
ELEVEN-TO-SIX ROW ADAPTER:                    NOT NEEDED / WRONG TYPE
FULL SIGNATURE -> SIX-ROW RESTRICTION:        PAPER-CLOSED
PENTAGON FOX CHANGE:                          NOT ASSERTED ZERO
TASK625 ACTUAL PAYLOAD / FRESH RHO2:          NOT YET PRODUCED
GRADE TWO / COMPLETE FIRST RUNG:              NOT DECIDED
FULL PB4 / A0 / COMMON / COFINAL LIFT:        NOT DECIDED
FAKE / IHARA:                                 NOT DECLARED
verified:                                      false
```

`R07_ELEVEN_ENDPOINT_SIX_ROW_RESTRICTION_V476_CANDIDATE`
