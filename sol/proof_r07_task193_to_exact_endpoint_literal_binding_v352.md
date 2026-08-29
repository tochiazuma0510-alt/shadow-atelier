# R07 task193-to-exact-endpoint literal binding (v352)

Author: Sol / 2026-08-29

Status: paper ABI theorem closing the physical input gap between the accepted
task193-v3 package, a direct-relator A5/A6 MEMBER, and the task292 exact
endpoint core.  Every field is reconstructed from authenticated executable
owners; no occurrence row or Fox source is guessed.  No actual MEMBER or
endpoint result is asserted.  `verified=false`.

## 1. Authenticated inputs

Fix the following physical positive objects.

1. A task193-v3 receipt and independent verdict, containing the literal words

   \[
   g_0=g_{760},\qquad a=c_{\rm exact},\qquad f=g_0a,
   \tag{1.1}
   \]

   the three corrected relation words and the pointed sign replay.
2. The task198 producer-v12 owner and independent checker-v14 owner, each
   restoring the same immutable eleven-occurrence ledger and the ten literal
   context substitutions.
3. A direct-relator A5/A6 MEMBER receipt and independent verdict whose
   polynomial is

   \[
   M=\sum_i a_i(U_i-V_i).
   \tag{1.2}
   \]

   In the v3 receipt `U_i=positive_word`, `V_i=negative_word`; the coefficient,
   prefix and relator index are retained as ancestry.

The endpoint binder authenticates all three source families by exact
path/byte/SHA and authenticates each receipt/verdict binding before using a
field.

## 2. Literal occurrence reconstruction

For occurrence `o=1,...,11`, let the authenticated task198 ledger supply

\[
 (B(o),\tau_o,j_o,\rho_o,\sigma_o,\mathcal P_o,
   \operatorname{orientation}_o),
\tag{2.1}
\]

where `tau_o` is E3 or E4, `j_o` is the ten-coordinate index,
`sigma_o=factor_sign`, and `P_o` is the listed
`fox_prefix_occurrences`.  The executable task198 context at index `j_o`
supplies the two literal PB words

\[
 \rho_o(x),\qquad\rho_o(y).
\tag{2.2}
\]

Set

\[
 r_o=\rho_o(g_0).
\tag{2.3}
\]

For every ordinal `k`, put

\[
 \varphi_k=
 \begin{cases}
 r_k,&\sigma_k=1,\\
 r_k^{-1},&\sigma_k=-1.
 \end{cases}
\tag{2.4}
\]

Multiply the signed factors named by `fox_prefix_occurrences(o)` in their
stored order:

\[
 Q_o=\prod_{k\in\mathcal P_o}^{\rm stored\ order}\varphi_k.
\tag{2.5}
\]

The literal task179 prefix and the intrinsic occurrence chain are

\[
 P_o=\begin{cases}Q_or_o,&\sigma_o=1,\\Q_o,&\sigma_o=-1,
       \end{cases}
 \qquad
 d_o=\delta(r_o^{-1}).
\tag{2.6}
\]

These are exactly v225 equations (2.2)--(2.3).  Consequently the task292
literal fields are not additional input data.  They are the following
deterministic serialization:

```text
ordinal          = o
block            = H1, H2, or P (P1/P2/P3/P5/P4 normalized to P)
position         = 1,2,3 / 1,2,3 / 1,2,3,5,4
type             = task198 type E3/E4
rank             = 3 for H1/H2, 4 for P
rho.x, rho.y     = the exact task198 context words (2.2)
sigma            = task198 factor_sign
prefix_word      = the freely reduced literal P_o in (2.6)
inverse_slot     = (sigma == -1)
orientation      = task198 orientation
registry_label   = "C" + task198 context_id
repeated_e3_key  = "E3_xy" exactly at ordinals 1 and 5, otherwise null
d_sources        = [{coefficient: 1, left_word: [],
                     fox_word: freely_reduce(inverse(r_o)),
                     provenance: authenticated g760/context/ordinal pins}]
```

The `registry_label` rule gives `C21` at the two repeated E3 occurrences and
at the separately typed E4 occurrence, so it preserves rather than merges
that distinction.

### Proposition 2.1 (THE SERIALIZED OCCURRENCES ARE THE ACTUAL `d` OWNER)

Expanding the eleven serialized `d_sources` with their signs and prefixes
gives, blockwise,

\[
 \boxed{
 \sum_{o\in B}\sigma_oP_od_o
   =-\delta_B R_B(g_0)=d_B.}
\tag{2.7}
\]

#### Proof

The task292 `chain_sources` expansion of the single source for occurrence
`o` is literally `delta(r_o^{-1})=d_o`.  Its endpoint engine applies the
stored left prefix `P_o` and sign `sigma_o`.  Hence its block sum is the left
side of (2.7).  V225 Proposition 2.1 identifies that sum with the right
side.  Every factor, inverse and multiplication order in this calculation is
reconstructed by the task198 executable owner.  \(\square\)

## 3. Literal residual reconstruction

Recompute from the pinned task193 constructor and the authenticated corrected
word `f` the three printed relation words

\[
 R_{H1}(f),\qquad R_{H2}(f),\qquad R_P(f).
\tag{3.1}
\]

The first two are the two embedded hexagon words.  The third is the five
factor pentagon in the frozen printed order `(1,3,0,-2,-4)`.  Require literal
equality with task193's `relation_words`; the receipt value alone is not a
constructor oracle.

Serialize

```text
epsilon_sources[B] = [{coefficient: -1, left_word: [],
                       fox_word: R_B(f),
                       provenance: authenticated corrected-word/block pins}]
```

### Proposition 3.1 (THE SERIALIZED EPSILON SOURCE IS THE ACTUAL `e` OWNER)

Task292 expands this source to

\[
 \boxed{e_B=-\delta_B R_B(f),}
\tag{3.2}
\]

and its endpoint is

\[
 \boxed{\epsilon_B=D_{1,B}e_B=1-\overline{R_B(f)}.}
\tag{3.3}
\]

#### Proof

`chain_sources` is the literal left-Fox expansion, including the outer
coefficient `-1`, so it gives (3.2).  The Fox endpoint identity
`D1 delta(w)=w-1` gives (3.3).  These are v225 equations (1.4)--(1.5).
\(\square\)

## 4. The accepted literal-input object

Convert each authenticated v3 pair to

```text
M_terms[i] = {
  coefficient: coefficient,
  U: positive_word,
  V: negative_word,
  ancestry: {prefix, relator_index, source receipt term}
}
```

and collect only inside the endpoint core.  Do not pre-delete dependent or
coefficient-cancelling pairs.  Bind the immutable `M` digest independently
on producer and checker sides.

Together with Sections 2--3, the new accepted object is

```text
schema          = d972-r07-actual-three-exact-pb-endpoints/v3/literal-input
mode            = PRODUCTION
source_words    = {g0: g760, corrected: f, correction: c_exact}
M_terms         = the authenticated direct-relator/lift-null pair list
occurrences     = the eleven rows of Section 2
epsilon_sources = the three rows of Section 3
bindings        = task193, task198, A5/A6 receipt/verdict physical identities
```

Version `v3` is required because task292-v2 production deliberately has no
accepted MEMBER/M input ABI.  The new version may load the frozen v2
`compile_literal` core under a non-main module name, but it must not call or
patch v2's unconditional `production_literal` blocker.

### Theorem 4.1 (PHYSICAL ENDPOINT BINDING)

For the object above, the frozen exact endpoint core computes, for every
`B in {H1,H2,P}`,

\[
 \boxed{
 \eta_B(M)=\epsilon_B-
  \sum_{o\in B}\sigma_oP_o
  \sum_i a_i\bigl(\rho_o(U_i)-\rho_o(V_i)\bigr)
  (r_o^{-1}-1).}
\tag{4.1}

This is exactly the actual universal endpoint

\[
 D_{1,B}\bigl(e_B-(M\star d)_B\bigr).
\tag{4.2}

#### Proof

Proposition 2.1 identifies the occurrence sources with the actual `d_B` and
gives `D1(d_o)=r_o^{-1}-1`.  Proposition 3.1 identifies the fixed source
with `e_B` and its endpoint with `epsilon_B`.  The task292 endpoint compiler
substitutes each literal `U_i,V_i` through the exact `rho_o`, left-translates
by `P_o`, applies `sigma_o`, and collects only after the complete block sum.
Its implemented formula is therefore (4.1).  Equivariance and linearity of
`D1` turn (4.1) into (4.2).  \(\square\)

The theorem applies unchanged when some `M_terms` are v351 lift-null pairs
`Vn-V`: the endpoint core consumes literal F2 word pairs and does not require
their first-shadow image to be nonzero.

## 5. Independent replay and fail-closed boundary

The producer reconstructs Sections 2--4 from the task198-v12 and task193-v3
owners.  The independent checker reconstructs them from task198-v14 and the
independent task193 checker path; it must not accept the producer's serialized
occurrences or epsilon sources without recomputation.

Both sides require:

1. literal `f=freely_reduce(g760+c_exact)`;
2. exact equality of all eleven ledger owner fields with the frozen layout;
3. exact equality of the ten context substitutions;
4. direct replay of (2.7) against task193's pointed `d1` rows;
5. reconstruction of all three relation words and the task193 corrected Fox
   rows with the sign in (3.2);
6. exact binding and collection of every `M` pair; and
7. full faithful Artin normal forms for endpoint equality.

Any absent owner, source drift, word mismatch, sign mismatch or resource stop
is typed UNKNOWN and cannot be promoted to endpoint zero or nonzero.

## 6. Fixed frontier

```text
TASK193/TASK198 -> ELEVEN EXACT d SOURCES:       PAPER CONSTRUCTION
CORRECTED WORD -> THREE EXACT EPSILON SOURCES:   PAPER CONSTRUCTION
V3 M PAIRS -> TASK292 LITERAL M TERMS:           EXACT ABI
COMPILED VALUE = ACTUAL H1/H2/P ENDPOINT:        PAPER PROOF
INDEPENDENT OWNER RECONSTRUCTION CONTRACT:       FIXED
PHYSICAL V3 ENDPOINT BINDER:                     NOT YET IMPLEMENTED
ACTUAL ENDPOINT TERMINAL:                        NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA WITNESS:          NONE
```

`R07_TASK193_TO_EXACT_ENDPOINT_LITERAL_BINDING_V352_PAPER_GRADE`
