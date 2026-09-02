GRADE2_STREAMED_TRANSCRIPT_V452_AUDIT_PASS_AFTER_REPAIR

# Sol(max) Reply 570: audit of the streamed grade-two transcript

Author: Sol / 2026-09-03

## 0. Audit target and boundary

The final audited v452 is the repaired working-tree object below.

| input | bytes | SHA-256 |
|---|---:|---|
| v452 | 12,975 | `754c5ae214ee48ad530948feb734a50395386e5bb1d8fe25daf0cedc6c3313c1` |
| v450 | 7,649 | `48acc55a73aba140aa73098791d73f936f1b46fc5316d6f56e668be242fdc630` |
| v451 | 8,050 | `3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4` |
| Task565 instruction | 5,986 | `0c0c32831a5fbd055ba158b8f6b1c429aa51a4cdfe1d781e912a2eba016ebef3` |
| Task565 producer inspected for its actual contract | 145,917 | `acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8` |

The snapshot first presented for audit, SHA-256
`dd78cb2d721a824f156871ec3046b82bbb30da4a5553d1ddcdac89f0c55e7b9e`,
had a load-bearing character-order error in (3.3).  During the audit the
middle two rows were swapped into the correct order, and the lossless
accepted-expression, structural-offset, companion-scale and two-stage
physical-ancestry requirements were made explicit.  I independently checked
the resulting object above.  That history is why the verdict is
`PASS_AFTER_REPAIR`, rather than an unqualified pass.

This was a paper/schema audit.  I ran no grade-two phase, production worker,
GHA workflow, membership reduction, or certificate generation.

## 1. Deterministic offer stream

The stream in v452 section 1 matches the actual Task565 closure.  The producer
first inserts every packet row in origin order, then drains a FIFO of accepted
pivot IDs, offering the four children in the fixed actor order

```text
(1,-1,2,-2) = (x,x^-1,y,y^-1).
```

This is visible in Task565 producer lines 2262--2281 and 2282--2307.  Pivot IDs
are consecutive acceptance IDs.  Consequently the FIFO parents are processed
as `0,1,...,r-1`, even though their lead coordinates need not be monotone.
Each accepted pivot contributes exactly four actor offers.  Thus, with

\[
 m=44+4\operatorname{rank}(B_1),\qquad r=\#\text{accepted},
\]

the exact receipt is

\[
 \#\text{offers}=m+4r.
\]

At the Task565 ceilings this is

\[
 m=44+4(8059)=32,280,
 \qquad m+4(36,288)=177,432.
\]

The count is sufficient for queue exhaustion only together with the strict
record-ID sequence: all `(defect,o)` for `o=0,...,m-1`, followed by every
`(actor,i,t)` for consecutive `i` and all four ordered `t`.  V452 fixes that
sequence.  An implementation which checks only the scalar equality, while
allowing a duplicated or skipped actor ID, would not meet the theorem.

The reduction policy also agrees with Task565's `PackedEchelon`: repeatedly
inspect the first nonzero coordinate, use the unique earlier normalized row
with that lead if it exists, revisit the packed byte, and stop at the first
unowned lead.  The ordered reduction trace is therefore deterministic even
when pivot IDs are not ordered by lead.

## 2. Lossless transcript and next presentation

V452 (2.4) closes the only potentially ambiguous coefficient.  For each offer
the full stored expression is exactly

\[
 E_s=q_s\quad\text{if dependent},\qquad
 E_s=q_s\mathbin{\Vert}[(r_s,\sigma_s)]\quad\text{if accepted}.
\]

Indeed `q_s` is the ordered list subtracted in (1.1), while
`b_[r_s]=sigma_s*bar(v_s)`.  Since `sigma_s` is 1 or 2 and is its own inverse
in `F3`, the coefficient of the newly accepted pivot in the complete
`origin_reductions` or `actor_transitions` entry is precisely `sigma_s`, not
one and not `-sigma_s`.

The reconstruction is then bijective:

- a defect record fills `origin_reductions[o]`, and an actor record fills
  `actor_transitions[i][t]` with `E_s`;
- every accepted record gives the DAG node
  `(pivot=r_s, lead=ell_s, scale=sigma_s, origin=id(v_s), reductions=q_s)`;
- the accepted matrix gives `basis_rows` in that same pivot order;
- the accepted records give `pivot_leads`; and
- transcript length gives `attempts`, while (2.5) plus the exact ID stream
  gives `queue_exhausted`.

Conversely, Task565's raw reduction traces, DAG nodes, leads and rows recover
those records without sorting or flattening `q_s`.  Thus no order, reduction
sign, normalization scale, or actor/defect ancestry field remains omitted in
the repaired theorem.

For the future presentation, a block receipt must continue to bind its
character index, the Task565 defect-roster digest, actor order, width, parent
prepare digest and packed-matrix rank.  Those inherited bindings identify a
numeric defect origin with its seed or old-transition literal ancestry.  With
the four character transcripts and v451's global old/new offsets, one can
reconstruct every seed reduction, every old- and new-row transition, and every
accepted literal DAG node needed for the next `T2`; a merge-summary digest is
still not a substitute.

## 3. Authentication, offsets and independent replay

The repaired Corollary 2.2 is sufficient.  The offset object contains all
record starts and a final EOF sentinel.  During its sequential pass, an
independent checker must recompute and compare that entire offset list, check
contiguity and exact EOF, and only then permit indexed reads.  This prevents a
producer-authenticated but structurally false offset table from becoming the
random-access authority.

Authentication and semantic replay are separate gates.  Hash/length checks
bind the bytes and their parents; the checker must also regenerate every
defect or actor offer, perform the first-lead reductions, compare the ordered
`q_s`, status, lead and scale, and compare each normalized accepted row.  V452
lines 140--146 now expressly forbid reducing this to digest comparison.

The concrete implementation must put the encoding version, endian convention,
field widths, character, ambient width, origin count/digest, actor order,
record count, accepted count and the exact byte lengths/hashes of all three
files in the authenticated header/receipt.  This is a mandatory implementation
requirement flowing from “fixed ... width-versioned” and “authenticated”; it
is not an additional mathematical object or an optional optimization.

## 4. Simultaneous pure-grade transform

For the pinned Task565 convention

\[
 \chi_{(a,b)}(c,d)=(-1)^{ac+bd}
\]

and the registered order `(00,01,10,11)`, the correct rows are

```text
chi00:  1  1  1  1
chi01:  1 -1  1 -1
chi10:  1  1 -1 -1
chi11:  1 -1 -1  1
```

These are exactly the rows now displayed in v452 (3.3), and they agree with
Task565's `source_character_sign`.  The original audit snapshot had `chi01`
and `chi10` interchanged.  For example, on a pure `chi01` eigenrow the four
word images have coefficients `(1,-1,1,-1)`; the old displayed second row
gave zero while its third row returned the vector.  Implementing that matrix
literally would have exchanged the two packet labels and broken their parent
bindings.  The current row swap repairs the theorem.

There is no missing normalization: `1/|C|=1/4=1` in `F3`, and all characters
are self-inverse.  The hypothesis that `beta` is lower-zero and pure degree
two is essential.  Each `L_[w_a]^(2)` acts on the whole six-monomial row, so
the transform does not create six independent closures.  Finally, section 3
uses only the genuine associated-grade idempotents `e_chi`; it makes no
idempotence assertion for the full filtered word sums `P_chi` of v451 (1.1).

## 5. Packed defect equations

Write the triangular exact action through degree two as

\[
 A_t(\ell,g)=\bigl(A_t\ell,\ C_t(\ell)+A_t^{(2)}g\bigr).
\]

Subtracting the authenticated relation
`A_t ell_i=sum_j q_[itj] ell_j` gives precisely repaired (4.3),

\[
 \beta_{it}=C_t(\ell_i)+A_t^{(2)}g_i-\sum_jq_{itj}g_j.
\]

There is no additional crossed term on the right-hand linear combination.
Here `C_t` must mean the degree-two component of the *complete* Task565 affine
action on `(ell_i,0)`: it includes the signed kernel substitutions (in
particular a negative column's `u -> 2u+u^2`), section/action data and every
occurrence crossed cochain.  The zero multiplication cocycle does not make
those occurrence terms vanish.  V452 states this load-bearing qualification.

For a seed there is no actor cross term: its exact direct evaluation already
contains its degree-two part.  Hence

\[
 \beta_a=\operatorname{gr}_2(s_a)-\sum_jq_{aj}g_j
\]

is complete.  Both subtraction signs match v444 and the existing Task565
full-array construction.  A packed four-trit AXPY must therefore apply
`-q mod 3` coordinatewise to the referenced packed lift rows.  It changes
storage and call overhead only, not the defect roster or its values.  The
missing TeX backslash in the initial (4.3) snapshot was also repaired.

## 6. Persistence, restart and resource accounting

The source worker contract is sufficient for dynamic closure, rather than
only a static matrix.  Accepted/dependent output is available while the caller
generates future actor offers; committed prefixes contain all counts and file
lengths; restart authenticates those prefixes and reconstructs the small
lead-to-pivot map.  Because accepted pivot IDs are consecutive and actor
parents are FIFO, the offer count together with the FIFO head/tail determines
the next origin or `(pivot,actor-position)`.  A concrete backend must checkpoint
only at a declared offer boundary (or record an intra-offer state) and must
discard or quarantine any uncommitted file suffix before appending.

The numerical products in v452 are all correct:

\[
\begin{aligned}
36,288(36,288/4)&=329,204,736,\\
177,432(8)&=1,419,456,\\
32,260^2/4&=260,176,900,\\
32,260(48,384)/4&=390,216,960,\\
48,384^2/4&=585,252,864.
\end{aligned}
\]

The three physical stores total `1,235,646,724` bytes.  Adding one maximal
source-character basis gives `1,564,851,460` raw packed bytes, below
`2 GiB = 2,147,483,648` by `582,632,188` bytes.  This is a packed-store bound,
not a complete RSS or artifact-size promise.

There is no hidden need for four simultaneous source owners: process or job
boundaries may consume them one at a time.  Likewise the precision-one `B1`
and degree-two lift readers used for the old-row pass must be file-backed and
released/unmapped before a maximal source block is retained.  Transcript and
offset buffers must be bounded.  The variable reduction transcript can be
quadratic in the worst case, so each source and physical transcript needs a
receipt-bound byte cap whose exhaustion seals `UNKNOWN_RESOURCE`; streaming
alone is not a disk bound.  Section 5's explicit cap and section 6's “same
externalization” impose this requirement.  Omitting it in an implementation
would be a production resource blocker, not a theorem counterexample.

Delta coding, compression, a different batch size, and parallel execution of
several character jobs when the runner permits it are optional optimizations.
They are not audit conditions.

## 7. Physical lower-first externalization

The repaired section 6 preserves the paired row operation exactly.  For an
input `(L,g)`, if lower reduction records `q_L`, then

\[
 L'=L-\sum a_iL_i,\qquad g'=g-\sum a_ig_i.
\]

If `L'` is accepted, both members of the pair are multiplied by the same
`sigma_L` before storing the lower pivot and its grade companion.  This scale
is indispensable: scaling only `L'` would make every later companion
elimination wrong.  If `L'=0`, the unscaled `g'` is passed to the grade owner,
which records its own `q_G` and accepted scale `sigma_G`.

The shared physical-offer ID joins the lower transcript to the possible grade
transcript.  Together with the unchanged Task565 physical roster, lower DAG,
grade DAG and source block parents, an accepted grade node therefore expands
through `q_G`, then `q_L`, then the normalized lower-pivot ancestries, and
finally to a lifted-`B1` or `H2` literal origin.  This retains both the
companion coefficients and future literal ancestry.  A pair of unlinked
transcripts, or companion rows without `sigma_L`, would preserve neither the
canonical grade fibre nor its literal representative and must fail closed.

## 8. Classification and claim boundary

- **Theorem error, repaired:** the initial (3.3) exchanged the registered
  `chi01` and `chi10` outputs.  The current matrix is correct.
- **Exact serialization repairs completed:** (2.4) now records the accepted
  pivot coefficient; the offset table is structurally replayed through EOF;
  and section 6 now carries `q_L`, `sigma_L` and the shared two-stage ancestry.
- **Mandatory implementation requirements:** instantiate the authenticated
  binary header, exact-ID checker, atomic prefix restart, source and physical
  transcript byte caps, one-character ownership, complete semantic replay,
  and the two synchronized physical row operations described above.
- **Optional only:** compression, delta encoding, batching choices and extra
  parallelism.

Accordingly, repaired v452 preserves the exact v450--v451 grade-two closure
and future transition presentation while permitting list/JSON externalization
and the four-to-one word-action factorization.  It does not audit or accept a
concrete Task565 integration or Task567 compiled calibration.  It changes no
v220 numerator and proves no grade membership.

```text
STREAMED TRANSCRIPT: paper-exact after the recorded repair
SIMULTANEOUS PURE-GRADE PROJECTORS: paper-exact after the recorded repair
PACKED DEFECT FORMULAS: paper-exact
TASK565/TASK567 PRODUCTION INTEGRATION: still candidate / not accepted here
FIRST RUNG: no grade decided by this audit
A0 / COMMON / COFINAL LIFT / FAKE / IHARA: not declared
verified=false
```
