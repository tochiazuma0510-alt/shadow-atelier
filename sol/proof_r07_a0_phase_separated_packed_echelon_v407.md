# R07 A0 phase-separated packed-echelon lemma (v407)

Author: Sol / 2026-08-31

Status: paper implementation lemma refining v405--v406 after the actual v11
resource terminal.  It changes no A0 search universe and asserts no common
word, compatible lift, fake, or Ihara witness.  `verified=false`.

## 1. Actual v11 measurement

Run `33320103188`, job `99280454030`, immutable head
`eb840541ece21f394a6ac46b1b7a6e0a6cd5a301`, completed the 44 seeds and
reached

\[
 r_{\rm occ}=r_{\rm phys}=344,\qquad
 p_{\rm done}=86,\qquad |Q|=258.
\tag{1.1}
\]

Its occurrence and physical pivot stores contained respectively

\[
 31{,}847{,}811\quad\hbox{and}\quad38{,}056{,}986
\tag{1.2}
\]

nonzero entries.  RSS reached the preregistered 4.8 GB cap.  The sealed
checkpoint is 275,905,469 bytes with SHA-256
`3ac222801a1a91b8e0f163554835e569a26c2cac0f3f8bea481e1825e5f911b8`.
Thus the stop is a measured double-storage resource terminal, not an A0
negative and not a failure of the v405 selector.

## 2. Physical insertion is a second phase

Keep the notation of v405.  Its Theorem 2.1 computes the occurrence space
\(\bar W\leq\bar U\) using only occurrence rank.  Its equation (3.4) is

\[
 \operatorname{im}_{\rm corr}=\bar L_g(\bar W)\leq\bar Z.
\tag{2.1}
\]

### Lemma 2.1 (DEFERRED PHYSICAL ECHELON)

No physical pivot is needed while the occurrence queue is nonempty.  If
\(p_1,\ldots,p_r\) is the final occurrence pivot basis, then inserting

\[
 \bar L_g(p_1),\ldots,\bar L_g(p_r)
\tag{2.2}
\]

after the queue exhausts produces exactly the same physical correction span
as inserting each aggregate when its occurrence pivot first appears.

#### Proof

The occurrence frontier and every keep/discard decision depend only on the
echelon in \(\bar U\); v405 explicitly forbids physical dependence from
suppressing descendants.  The map \(\bar L_g\) is linear, so the image of
the final basis is \(\bar L_g(\bar W)\), independently of insertion time.
Sparse echelon insertion preserves the span of its inserted rows.  This gives
(2.2).  \(\square\)

Consequently v11's simultaneous physical echelon was mathematically
redundant during its first phase.  It may be discarded from a v11 checkpoint
without losing any occurrence row, frontier item, source expression, or
future correction direction.

## 3. Packed rows preserve the exact echelon

Let \(K\) be the set of byte-valued quotient coordinates encountered so far.
Maintain an injective registry

\[
 \iota:K\hookrightarrow\{0,\ldots,2^{32}-1\}.
\tag{3.1}
\]

A sparse row \(u=\sum_{k\in S}u_ke_k\), with \(u_k\in\{1,2\}\), is stored
as two aligned byte strings:

1. the increasing array of four-byte unsigned integers \(\iota(k)\);
2. the one-byte coefficient array \(u_k\).

The registry itself stores each coordinate byte string once.  The platform
contract is little-endian with four-byte unsigned integers; a loader rejects
any other contract.

### Lemma 3.1 (PACKED-ROW FAITHFULNESS)

Registry encoding and decoding are mutually inverse.  Replacing stored pivot
dictionaries by the packed representation changes neither pivot selection,
row reduction, rank, source coefficients, nor separating duals.

#### Proof

Injectivity of (3.1) gives a coefficient-preserving bijection between sparse
rows and aligned packed pairs.  Candidate rows remain byte-keyed while a
pivot is selected, so the frozen lexicographic pivot rule is unchanged.
Every use of a stored pivot first iterates the inverse registry and therefore
performs exactly the same \(\mathbf F_3\) axpy as the dictionary owner.
The expression echelon is not re-encoded.  Induction over insertions proves
equality of pivot bytes, normalized rows, expressions and ranks.  The same
decoded rows enter the dual recurrence, proving equality of duals. \(\square\)

For \(N\) stored nonzeros, row payload is exactly \(5N\) bytes before small
tuple/dictionary headers, rather than one Python hash-table entry per
nonzero.  This is an implementation bound only; it is not counted as an A0
mathematical numerator.

## 4. Streaming the transition

After occurrence closure, process pivots in their fixed order.  For pivot
\(p_i\):

1. decode its packed occurrence row;
2. compute \(R_i=\bar L_g(p_i)\);
3. record a deterministic SHA-256 digest of \(R_i\);
4. insert \(R_i\) into the packed physical echelon with source reference
   \(p_i\);
5. delete the now-consumed occurrence row payload.

Keep the occurrence expression map and source DAG.  If the run stops during
this phase, `physical_cursor=i` plus the remaining occurrence payloads and
the already built physical echelon is a complete continuation state.  Since
one occurrence row is removed after its aggregate is inserted, the
transition does not require the full occurrence and full physical payloads
simultaneously.

### Lemma 4.1 (SAFE OCCURRENCE-PAYLOAD RELEASE)

After the occurrence queue is empty and \(R_i\) has been inserted, the stored
coordinate payload of \(p_i\) is no longer needed for search correctness.

#### Proof

No occurrence actor is evaluated after queue exhaustion.  The physical
search uses only the span of the inserted \(R_i\), followed by v404's six
action rows.  Literal provenance uses the retained expression map and source
DAG, not the coordinate payload.  Thus deletion affects neither future row
generation nor ancestry. \(\square\)

## 5. Fresh positive replay from the DAG

For each retained occurrence pivot, recursively expand its expression and
source DAG to atoms `(seed, prefix, coefficient)`.  The atom row is rebuilt
from the authenticated seed and the occurrence actors in reverse prefix
iteration, exactly matching v405's convention that a child adds its new
letter on the left of the stored prefix.  Aggregate the rebuilt atom sum and
require its digest to equal the digest registered in Step 3 above.

### Lemma 5.1 (DAG-ONLY SOURCE RECONSTRUCTION)

The rebuilt row is exactly \(\bar L_g(p_i)\).

#### Proof

A leaf rebuilds its accepted compact relator row.  If a source has stored
prefix \((a_1,\ldots,a_m)\), reverse iteration applies
\(\bar\rho(a_m),\ldots,\bar\rho(a_1)\), yielding the recursively defined
child row.  V406 equation (3.3) says the expression coefficients reconstruct
the normalized pivot.  Linearity of \(\bar L_g\) gives the claimed physical
row.  The independently stored digest is a fail-closed implementation gate,
not a substitute for the final fresh Fox replay. \(\square\)

Hence positive replay needs no deleted occurrence coordinate payload.  It
still must perform v406's literal word, exponent-zero, joint-state, fresh Fox,
quotient-normal, selected-action and target-zero gates.

## 6. Exact migration boundary

The only admissible v11 input is the byte-pinned run-33320103188 checkpoint
from (1.2).  A v12 migrator must:

1. check outer bytes/SHA, v11 seal, schema and binding;
2. load it before constructing the heavy runtime;
3. discard only the partial physical echelon, which Lemma 2.1 makes
   redundant;
4. pack every occurrence pivot through Lemma 3.1;
5. retain the exact order, expressions, sources, queue, `seed_cursor=44`,
   `parent_cursor=86`, `action_cursor=344` and checkpoint sequence;
6. write a fresh v12 checkpoint before taking another actor step.

If loading or migration approaches the resource cap, it must fail closed and
preserve the v11 release mirror.  It must not silently restart, drop frontier
items, increase the RSS cap, or call the v11 partial physical span an A0
result.

```text
V11 44-SEED GATE:                         COMPLETE
V11 OCCURRENCE RANK / FRONTIER:           344 / 258
V11 TERMINAL:                             UNKNOWN_RESOURCE (RSS)
PHYSICAL ECHELON DURING OCCURRENCE PHASE: DEFERRED BY v405
PIVOT STORAGE:                            INJECTIVE PACKED REPRESENTATION
V11 CHECKPOINT:                           MIGRATABLE, BYTE-PIN REQUIRED
A0 COMMON WORD / FAKE / IHARA WITNESS:    NOT YET OBTAINED
```

`R07_A0_PHASE_SEPARATED_PACKED_ECHELON_V407_PAPER_GRADE`
