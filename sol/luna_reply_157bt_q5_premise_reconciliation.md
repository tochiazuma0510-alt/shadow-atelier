# Luna reply 157bt — q5 premise reconciliation

## Verdict

The earlier 157bn verdict is superseded on the narrow question asked here.
Under the project's accepted, source-pinned theorem framework, the three
premise bindings needed by the direct q5 obstruction are available:

| requested binding | verdict under the accepted premises | evidence grade |
|---|---|---|
| `build_roof` is the marked `PB3/M` roof for `M=K^(9) intersection N_S4` | PASS* | paper/theorem-framework-relative; finite realization is independently cross-checked, not Lean-verified |
| the frozen 972 rows are exactly the underlying set of `X=GT^heart(M)=GT(M)` | PASS* | theorem-level group target plus set-level NF cross-check; the JSON is not itself a Cayley-table proof |
| `A <= I <= X`, `|A|=324`, `|X|=972` | PASS* | accepted arithmetic/order theorem package; no explicit 324-row membership list is required |

The asterisks are important: PASS here means “closed relative to the
accepted paper/theorem premises and the recorded finite certificates”.  It
does not mean Lean `verified`, and it does not mean that q5 has already
returned a zero fiber.  The first remaining item is the actual complete q5
finite-fiber receipt.  A zero receipt at that gate gives the terminal B4-A
implication below.

No local GAP, Git, or GHA was run.

## 1. What changed since 157bn

The old blocker was correct for the phase-0 ledger but is no longer the
current effective chain.  `provenance/CLAIMS.md:100-103` still preserves the
historical C-972 wording (“scalar cardinality only”); that entry must not be
silently rewritten.  It is superseded for the present audit by the later
versioned rulings:

* R1131 records the independent `|GT(M)|=972` remeasurement.
* R1132--R1133 close the isolatedness route: K9 is isolated by the cited
  theorem, N_S4 is accepted isolated from the 54/54 kernel-trivial and
  `#C=1` receipt, and the intersection theorem makes M isolated.
* R1139 explicitly says that the P4 full-pullback assertion is open but is
  excluded from the minimum needed for the cardinality/index argument.
* R1142--R1145 adopt the P3/P5-prime closure package.  Thus the arithmetic
  Kummer formula and the relevant common-field identification are not waiting
  for a new 324-row classifier.
* R490 activates the NF-972 image-set equality; R506 adopts the repaired B
  artifact without retracting the mathematical set equality.

R1161's remaining open card is the stronger card-P4 statement
(`A_S4` as a complete pullback).  It is not a fourth premise for the direct
q5 contradiction.  Treating that stronger bookkeeping assertion as if it
were the order or inclusion premise was the semantic overreach in 157bn.

## 2. Roof binding: `build_roof` and the named M

### 2.1 The theorem-level object

The authoritative ROOF section of `docs/notes/ihnec_v1.md:353-369` gives,
for

```text
M = K^(9) intersection N_S4,
G9 = PB3/K^(9),
P  = PB3/N_S4 = PSL(2,8),
```

the natural marked quotient

```text
PB3/M ~= G9 x P,
|PB3/M| = 2916 * 504 = 1469664,
M_ord = 18.
```

The proof is not an order-only coincidence: the two natural projections are
onto, Goursat applies, and the solvability of `G9` versus the nonabelian
simple factor `P` forces the common quotient to be trivial.  Since the
central element `c` lies in both kernels, the standard `PB3 = F2 x <c>`
decomposition gives the corresponding `F2/M_F2` quotient.

The later canonical addendum makes the same point in a form used by the
current implementation.  Its equations (3)--(5),
`docs/notes/triad972_canonical_addendum_v2.md:45-108`, identify the quotient
through the natural factor maps, not by matching a permutation-group order.

### 2.2 Generator and marking pin

`search/d972_semantic_m_manifest_v1.json:4-33` fixes the source presentation
and the Artin bridge:

```text
x12 = s1^2,
x13 = s2*s1^2*s2^(-1),
x23 = s2^2,
c   = (s1*s2)^3,
```

It records the K9 factor of order 2916 and degree 27, the PSL(2,8) factor of
order 504 and degree 9, the joint order 1469664, and the kernel-intersection
identity.  The manifest's `infinite_group_api_forbidden` flag is an honest
scope restriction on the checker; it is not being cited as an abstract proof.

The finite realization in
`search/d972_b4_burau_fiber_v4.py:165-172` constructs the same marked
generators as a 27-point K9 block plus the 9-point GF(8)/PSL block.  Its
`roof_key` split and canonical coordinates are at `:190-203`; the word
loader binds the 972 keys and rejects duplicate keys at `:205-223`.

Therefore (i) is PASS* in the requested sense: the paper/ROOF theorem and
the frozen standard presentation bind the named quotient, while the code is
the finite, independently replayed realization of that binding.  The code
alone would still be only a candidate; the theorem-relative qualification is
deliberate.

## 3. The 972 rows and the group-valued target

### 3.1 Set equality, not “two identical computations”

The frozen tuple file
`search/certs/nf972_sourcemap_a_tuples_v2_20260804.json` has

```text
count = 972
canonical_bytes_sha256 = 32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91
```

Source map A is the factor-certificate fiber-product route.  Its v3 receipt
records K9=108, S4=54, 972 baseline tuples, 0 duplicates, and the 108/54
projections, with all four diagnostic fixtures firing:
`search/certs/nf972_sourcemap_a_v3_20260804.json`.

Source map B is the direct roof enumeration.  Its v4 receipt records
`derived_order=367416`, `shadow_total=972`, 972 distinct tuples, 0
duplicates, and the 108/54 projection checks:
`search/certs/nf972_sourcemap_b_v4_20260804.json`.

The fourth-party comparator records

```text
set_equal = true,
count_a = count_b = 972,
duplicates_a = duplicates_b = 0,
```

with matching projections in
`search/certs/nf972_crosscheck3_cert_20260804.json`.  The CV-9 reading is
precise about what this means: A and B use different universes and maps; the
same object means the same normalized image set, not the same computation
(`docs/notes/nf972_cv9_reading_v1.md:41-48`).  Its independent third
reconstruction also checks the can4 marking and the multiplication
convention (`:54-74`), while recording the B self-check tautology caveat
(`:97-112`).  Accordingly the correct grade is set-level cross-checked
candidate, not “two independent 972 counts proved everything”.

The later word artifact binds the q5 words to exactly this object:

```text
count = 972
frozen_tuple_sha256 = 32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91
source_target_key_digest = 9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62
canonical_bytes_sha256 = 283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930
```

The target digest line above is the artifact's recorded value; the exact
file is `search/certs/d972_b4_word_key_artifact_v1_20260816.json`.

### 3.2 Why this is an equality to X as a group

The row JSON does not carry a 972-by-972 Cayley table.  The group structure
comes from the theorem-level isolated roof:

```text
GT(M) = GT(K^(9)) x_U GT(N_S4),
|GT(M)| = (108 * 54) / 6 = 972.
```

This is equations (5)--(6) of
`docs/notes/triad972_canonical_addendum_v2.md:83-108`, with the underlying
ROOF proof in `ihnec_v1.md:353-369`.  The NF cross-check supplies the exact
underlying set and the word artifact supplies the exact q5 row-to-key
binding.  Hence the mathematically correct statement is:

```text
{frozen 972 NF rows} = underlying_set(X),  X = GT^heart(M) = GT(M),
```

where the last equality and the group law are theorem consequences of
isolatedness, not claims made by a digest.  This closes (ii) without
requiring a new abstract Cayley-table proof.

## 4. The order and inclusion bundle

### 4.1 Isolated roof and group target

The decisive primary pages were inspected as page images:

* `papers/2401.06870-gt-shadows-gentle-version.pdf`, p.20,
  Definition 3.13: an isolated object has `GT(N)=GTSh(N,N)`, a finite
  group.
* The same PDF, p.21, Propositions 3.14--3.15 and Remark 3.16: finite
  intersections of isolated objects are isolated and reductions between
  isolated objects are group homomorphisms.

The accepted K9/N_S4 premises in R1132--R1133 therefore give M isolated.
The direct finite measurements are evidence for the premises, not a
replacement for the source theorem.

### 4.2 X has order 972

The factor groups have accepted orders 108 and 54, and the common charming
coordinate group has order 6.  The fiber-product theorem gives

```text
|X| = 108 * 54 / 6 = 972.
```

R1131's independent 972 remeasurement, R490's later image-set adoption, and
the NF certificates are the machine side of the same theorem-level statement.

### 4.3 A has order 324, and A is inside I

The accepted arithmetic addendum
`docs/notes/triad972_canonical_addendum_v2.md:5-43,110-130` gives

```text
r = |<[a_mod9]> intersection <[b_mod9]>| = 3,
d9 = 9,
dS4 = 9,
|A| = 12*d9*dS4/r = 12*9*9/3 = 324.
```

The factor 12 is `[Q(zeta_9):Q] * [Q(zeta_9,i):Q(zeta_9)]`; it is not an
extra row-count convention.  R1122--R1125 close the local/Kummer values and
R1142--R1145 adopt the P3/P5-prime field and dessin binding needed to read
the two factors as the same arithmetic object.  This is the accepted
theorem-framework arithmetic image, not the declaration
`arithmetic_count=324` in `semantic()`.

Now let

```text
pi_M : widehat GT -> X,
I     = image(pi_M),
A     = image(G_Q -> widehat GT -> X).
```

For isolated M, the primary compatible-action/reduction theorem makes
`pi_M` a group homomorphism.  Since `widehat GT` is a group, `I` is a
subgroup of X.  The arithmetic Ihara map factors through the same
`pi_M`, hence `A <= I <= X`.  This is a statement about the typed maps, not
about recognizing arithmetic rows from their NF keys.  It is also why a
324-row membership list is unnecessary.

The original-primary anchors for the q5 route were checked from page images
of `papers/2008.00066-what-are-gt-shadows.pdf`:

* p.13, equation (2.20) and Definition 2.6 define the typed pentagon and
  finite GT pairs;
* p.14, Corollary 2.7 gives the induced group homomorphisms through arities
  2, 3, and 4;
* p.18, Proposition 2.11 identifies the induced finite source kernel and
  records compatibility with the coface maps.

The notation distinction is intentional: q5 uses the original `widehat GT`,
not the gentle-only `widehat GT_gen`.  No unresolved
`widehat GT = widehat GT_gen` (the U-10 issue in
`docs/week1-定義ノート.md:182`) is being smuggled into this argument.

Thus (iii) is PASS* under the accepted theorem premises:

```text
A <= I <= X,
|A| = 324,
|X| = 972,
[X:A] = 3.
```

## 5. Why the open P4 card does not block q5

R1139 already records the relevant dependency fact: the P4 full-pullback
assertion is open, but it is not used in the minimum derivation of `|A|`.
R1142--R1145 close the P3/P5-prime links that are used to identify the
arithmetic compositum and the common Kummer subgroup.  R1161 preserves the
stronger card-P4 (`A_S4` complete pullback) as open under the
“do not close what was not closed” rule.

That open card could matter for a per-row arithmetic *description* or for a
stronger full-pullback theorem.  It does not affect any of the following
facts used by q5:

1. M is isolated, so X is a finite group and `pi_M` is defined;
2. the roof set is all 972 elements of X;
3. the arithmetic image has order 324 and lies in `I`; and
4. a finite Burau obstruction is a one-way obstruction to membership in I.

Consequently P4 is not the first missing lemma for the q5-zero implication.

## 6. Literal A.18/Burau implication

The rest of the bridge is source-level, not a claim about gentle shadows.
The original PDF pages checked above are supplemented by p.48 Proposition
A.2 and p.49 equations (A.18)--(A.19).  Proposition A.2 says the displayed
coface formulas are group homomorphisms; p.49 gives the five literal PB3 to
PB4 substitutions.  Therefore a genuine `widehat GT` element satisfies the
typed pentagon (2.20), and every finite quotient/continuous representation
of the five coface images sends its pentagon defect to the identity.

The v4 implementation pins the same five parts in
`search/d972_b4_burau_fiber_v4.py:348-382` and checks the finite braid,
commuting, and invertibility relations before scanning.  It reconstructs an
exact finite right fiber `h0*K`, rather than testing one representative;
the complete-section and no-word-bound evidence is recorded at
`:743-858`, and the independent checker replays the fiber and every defect
at `search/check_d972_b4_burau_fiber_v4.py:849-975`.

The Burau object in this paragraph is an auxiliary finite continuous
quotient of PB4.  It is not being presented as an isolated NFI_PB4(B4)
refinement or as the source object in the inverse-limit theorem.  The A.18
coface homomorphisms are applied to the finite image of any hypothetical
`widehat GT` lift; that is exactly why the older typed-PB4-source demand from
157bi/157bn is unnecessary here.

For a target row `t`, write `F_q(t)` for the complete finite image fiber
used by that q5 receipt.  The only implication needed is

```text
t in I
  => some widehat-GT lift of t exists
  => its finite Burau image lies in F_q(t)
  => its A.18 pentagon defect is the identity.
```

Hence a complete receipt with zero identity defects in `F_q(t)` proves
`t notin I`.  No isolated PB4 source fiber, raw 158, explicit arithmetic
324-list, or cofinal refinement chain is needed for this one-way step.  In
particular, this is not the invalid inference “a finite positive test proves
genuine”; the converse is deliberately not used.

## 7. First remaining gate and terminal consequence

The first remaining item is the operational/semantic gate

```text
Q5-FIBER-COMPLETENESS:
the q5 producer and independent checker must return a receipt proving that
the finite Burau/A.18 image fiber over the selected frozen row is complete,
with the literal A.18 maps in this auxiliary quotient, and that every member
has nonidentity defect.
```

The v4 code supplies the exact-fiber contract and calibration gates, but the
repository snapshot has no accepted q5 zero-fiber receipt yet (the available
`ci/out` entry is the earlier resource-unknown v3 artifact).  Thus the
premise reconciliation is PASS, while the current A/B result remains
pending the actual q5 run.

Once that receipt has a zero identity count, the terminal proof is exactly:

```text
complete q5 fiber has no identity pentagon image
=> selected t is not in I
=> I != X
=> A <= I <= X and [X:A]=3 imply I=A
=> every element of X\\A (648 elements) is not a widehat-GT image,
   hence is B4-A/fake.
```

This last line is the original B4 conclusion.  It does not assert a B4-B
counterexample; it shows why a q5 zero is a terminal A certificate rather
than a partial measurement.

## Grade boundary and hashes

The paper statements and accepted ledger chain are `theorem-framework-
relative`; the finite NF and Burau artifacts are candidate/cross-checked
evidence.  No part of this reply calls the result Lean-verified.  The
historical scalar-only C-972 entry is retained as provenance, while the later
R490/R506 set-level adoption is the current effective status.

Reply hash is computed over all bytes before the following hash line.

SHA256(content before this line): f7b0a4afbee54210876de7a7200460a36227d94026a5163e605d2c3a8549b955

Q5_PREMISE_RECONCILIATION_PASS
