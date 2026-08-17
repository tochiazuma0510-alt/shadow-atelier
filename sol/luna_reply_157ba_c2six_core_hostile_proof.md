# Luna reply 157ba — hostile audit of the four-forget core proof

## Verdict

```text
PASS_C2SIX_CORE_C2_24
```

The proposed finite-group proof is sound once its finite input facts are
bound exactly as stated below.  The suspected step-3 problem is repaired by
the elementary special case of the diagonal-strip argument; pairwise full
projections really do force `G_P=P^4` for a nonabelian simple `P`.  The
suspected step-5 diagonal also does not exist: the four coordinate modules
are simple and pairwise nonisomorphic as modules for the *fixed* group
`P^4`, so a submodule is a sum of coordinate modules.

This verdict is a verdict on the proof, not a completed machine measurement.
The final receipt still has to bind the four deletion maps, the marked
epimorphism, the nonsplitting test, B3-normality, and the exact finite group
images.  The conclusion below is not an isolatedness, `ML`, 325, cofinality,
or B4-B conclusion.

## 1. Exact deletion maps and pair witnesses

The JSON map order is

```text
(x12,x13,x14,x23,x24,x34)  ->  (y12,y13,y23),
```

and its four rows are exactly

```text
d1: (1,  1,  1, y12,y13,y23)
d2: (1, y12,y13, 1,  1, y23)
d3: (y12,1, y13, 1, y23,1)
d4: (y12,y13,1, y23,1, 1).
```

This is the canonical deletion/relabeling convention.  Each row is onto
`PB3`: the displayed images contain all three PB3 pure generators.  Hence
each coordinate of `G_P` is onto `P` because `psi_P` is onto.

For the pair `(d_i,d_j)`, the following table gives an element whose first
coordinate is trivial and whose second coordinate is visibly nontrivial.
The entries are for `i<j`; the reversed pair is obtained by interchanging
the factors.

| pair | pure word `w` | `(d_i(w),d_j(w))` | image in `P^2` |
|---|---|---|---|
| `(1,2)` | `x13` | `(1,y12)` | `(1,pi(X))` |
| `(1,3)` | `x12` | `(1,y12)` | `(1,pi(X))` |
| `(1,4)` | `x12` | `(1,y12)` | `(1,pi(X))` |
| `(2,3)` | `x12` | `(1,y12)` | `(1,pi(X))` |
| `(2,4)` | `x12` | `(1,y12)` | `(1,pi(X))` |
| `(3,4)` | `x23` | `(1,y23)` | `(1,pi(Y))` |

The last column is not just a label: `X` and `Y` have order 9 in the
certified marked `E` model, while `V` has exponent 2, so their images in
`P=E/V` cannot be trivial.  Thus every pair projection contains a nontrivial
kernel element.  It is important that the proof use these images, not merely
the fact that the abstract kernels of `d_i` and `d_j` differ; a kernel
difference killed by `psi_P` would not suffice.

The maps file records the conjugation identities

```text
p4 o c_(sigma3^-1) = p3,
p3 o c_(sigma2^-1) = p2,
p2 o c_(sigma1^-1) = p1,
```

which are the exact identities needed later for the four-strand core.  No
24-coordinate replacement is needed for this four-deletion construction,
provided the PB3 kernels are normal in `B3` as discussed in Section 5.

## 2. The pair-projection Goursat step

Let `H_ij` be the image of `PB4` in the `i,j` coordinates of `P^4`.  It is a
subdirect subgroup of `P x P`.  Goursat's lemma gives normal subgroups
`N_i,N_j` of `P` and an isomorphism

```text
P/N_i ~= P/N_j
```

describing `H_ij`.  Since `P=PSL(2,8)` is nonabelian simple, each `N_i` and
`N_j` is either `1` or `P`.  Subdirectness rules out either being `P`; the
only alternatives are therefore the full product or a graph of an
isomorphism `P -> P`.  The table in Section 1 supplies `(1,p)` with
`p != 1`, so the graph alternative is impossible.  Consequently

```text
H_ij = P^2 for every i != j.
```

The simplicity used here is the usual special case for `PSL(2,q)`, `q>=4`;
the repository's paper-side note `docs/notes/iso_s4_paper_side_v1.md` §3.2
records the corresponding simplicity and trivial-centre fact.  It is not
being inferred from the order 504 alone.

### Direct proof of the required `P^4` strip lemma

For completeness, let `H <= P^n` be subdirect with all pair projections
onto, where `P` is nonabelian simple.  Induct on `n`.  The projection
`H' <= P^(n-1)` is subdirect and has full pair projections, so by induction
`H'=P^(n-1)`.  Put

```text
L = H intersect (1^(n-1) x P).
```

The last-coordinate projection of `L` is normal in `P`: conjugate an
element of `L` by an element of `H` whose last coordinate is an arbitrary
element of `P`.  It is therefore either `1` or `P`.

* If it is `P`, `H` contains the last coordinate factor and, since its first
  `n-1` projection is full, `H=P^n`.
* If it is `1`, projection to the first `n-1` coordinates identifies `H`
  with the graph of a homomorphism `P^(n-1)->P`.  Each factor image is a
  normal subgroup of `P`, and commuting images from different factors imply
  that at most one factor is nontrivial.  Surjectivity to the last factor
  then makes one pair projection a graph, contradicting the hypothesis.

This proves the induction.  In particular, for the four maps,

```text
G_P = P^4.
```

This is the point at which a generic slogan “pairwise independent implies
independent” would have been unsafe; the simple-factor proof above is the
needed argument.  It would fail for abelian factors or for factors with a
common proper quotient.

## 3. Nonsplitting forces every kernel projection to be nonzero

The coordinatewise quotient map

```text
q : G_E -> G_P=P^4
```

is onto by definition, and its kernel is

```text
K = G_E intersect V^4.
```

Fix coordinate `i` and let

```text
S_i = { (1,...,1,p,1,...,1) : p in P } <= P^4,
H_i = q^(-1)(S_i) <= G_E.
```

Then `H_i/K ~= S_i ~= P`.  Suppose `pr_i(K)=1`, where `pr_i` is the
coordinate projection `G_E <= E^4 -> E`.  If two elements of `H_i` have the
same image in `S_i`, their quotient lies in `K`, and their `i`th E-coordinates
are equal.  Therefore `pr_i` factors through a well-defined homomorphism

```text
s_i : H_i/K ~= P -> E.
```

The quotient map `E->P` composed with `s_i` is the identity: this is exactly
the definition of `H_i` as the preimage of the `i`th coordinate copy.  Thus
`s_i` is a section of `E->P`, contradicting the nonsplitting of

```text
1 -> V -> E -> P -> 1.
```

Hence `pr_i(K) != 1` for all four coordinates.

This argument does not assume a subgroup complement inside `G_E`; it derives
one in `E` from the factorization through `H_i/K`.  That distinction closes
the possible ambiguity in the phrase “restriction over a coordinate copy”.

The nonsplitting premise is presently a finite receipt, not a Lean-verified
theorem: the phase-2b record checks all 512 lifts of the selected order-2
and order-3 generators and finds a nontrivial `V` kernel.  It is sufficient
because any section would send those two generators to an order-2/order-3
lift with trivial kernel.  The receipt and its independent checker must be
bound to the exact `E`, `P`, `pi`, `X`, and `Y` used here.

## 4. The `P^4` module argument and the diagonal audit

Since `V` is elementary abelian, `K <= V^4` is an `F_2`-subspace.  It is
normal in `G_E`, and `G_E -> P^4` is onto.  Conjugation by a lift of an
element of `P^4` therefore preserves `K`.  Conjugation on each copy of `V`
factors through `P`, because `V` is abelian and its own inner conjugations
are trivial.  Thus `K` is a `P^4`-submodule of

```text
V^4 = V_1 direct-sum V_2 direct-sum V_3 direct-sum V_4,
```

where the `j`th factor of `P^4` acts on `V_j` by the certified irreducible
`P`-module and acts trivially on `V_i` for `i != j`.

The phase-2b receipt's irreducibility test is the needed one: every nonzero
vector has full normal closure in `V`, so the coordinate action is a
nontrivial irreducible `P`-module.  It follows that each `V_i` is simple as a
`P^4`-module.  They are pairwise nonisomorphic: the `i`th copy is nontrivial
under the `i`th factor of `P^4`, whereas `V_j` is trivial under that factor
when `j != i`.  Equivalently, their annihilator subgroups in `P^4` differ.

There is consequently no diagonal submodule of the sort that would occur
between two isomorphic copies.  More explicitly, if `W` is a submodule of
the direct sum of pairwise nonisomorphic simple modules, every simple
submodule of `W` maps into at most one coordinate, since

```text
Hom_(P^4)(V_i,V_j) = 0  (i != j).
```

The ambient direct sum is semisimple as a module because it is itself a
direct sum of simple modules; this does not invoke Maschke's theorem (which
would indeed be inapplicable in characteristic 2).  Hence `W` is a direct
sum of a subset of the coordinate modules.  Applying this to `W=K` and
using `pr_i(K) != 0` from Section 3 gives every coordinate module:

```text
K = V_1 direct-sum V_2 direct-sum V_3 direct-sum V_4 = V^4,
|K| = 2^(6*4) = 2^24.
```

This is also why a diagonal graph of an isomorphism `V_i -> V_j` is not a
counterexample: it is not `P^4`-stable. A diagonal could be stable for a
single diagonal copy of `P`, but the proven acting group is the full direct
product `P^4`, not that diagonal subgroup.

## 5. `G_E`, kernels, and the core quotient

From `G_P=P^4` and `K=V^4`, every element of `E^4` lies in `G_E`: given
`e in E^4`, choose `g in G_E` with the same image in `P^4`; then
`e*g^(-1) in V^4=K <= G_E`. Therefore

```text
G_E = E^4.
```

Let

```text
C_E = ker(Phi_E) = intersection_i d_i^(-1)(N_E),
C_P = ker(Phi_P) = intersection_i d_i^(-1)(N_P).
```

Since `Phi_E` is onto `G_E` and `Phi_P=pi^4 o Phi_E`, the first
isomorphism theorem gives

```text
C_P/C_E ~= ker(G_E -> G_P) = K = V^4 ~= C2^24.
```

The direction is `C_E <= C_P`; it is not the reverse.  This quotient
identification is unconditional once the two maps and their kernels are
defined; it does not require enumerating `G_E` or `G_P`.

To call `C_E` and `C_P` the B4 cores, one additional normality statement is
needed.  If `N_E,N_P` are normal in `B3`, then
`L_Q=d_4^(-1)(N_Q)` is normal in the strand-4 stabilizer and in `PB4`, and
the four exact conjugation identities in the maps receipt show

```text
Core_B4(L_Q) = intersection_{i=1}^4 d_i^(-1)(N_Q) = C_Q.
```

If only PB3-normality were known, the four-intersection would still be a
valid kernel construction, but the label “B4 core” and B4 normality would
not follow. The phase-2b report records B3 invariance of `N_E` via the
`theta/tau` Cayley replay; `N_P` inherits it through `pi` only after the
commuting quotient action is explicitly bound. This is a receipt obligation,
not something to infer from `N_Q=ker(PB3->Q)` alone.

## 6. What is certified and what remains a receipt gate

The following are mathematical consequences of the stated inputs:

* the four deletion rows and the pair-witness table imply each pair image is
  full, after `P` simplicity and nontriviality of `pi(X),pi(Y)` are bound;
* the direct strip lemma implies `G_P=P^4`;
* nonsplitting implies all four coordinate projections of `K` are nonzero;
* irreducibility and the fixed `P^4` action imply `K=V^4`; and
* the first-isomorphism argument gives `C_P/C_E ~= C2^24`.

The following are not proved merely by the prose or by the order labels and
must be included in the independent finite receipt:

1. exact equality of the marked `psi_E` and `psi_P` with the pinned arrays;
2. `V` elementary abelian, normal, and irreducible under the marked `P`
   action;
3. `E->P` is onto with kernel exactly `V` and is nonsplit;
4. `P` is the stated nonabelian simple group, not just a group of order 504;
5. all four deletion maps satisfy the PB4 relations and the listed
   conjugation identities;
6. `N_E,N_P` are B3-normal if the objects are to be called B4 cores; and
7. an independent structural checker verifies the resulting orders or the
   equivalent kernel certificates, rather than trusting a producer's
   assertion of `|G_E|` or `|G_P|`.

The existing phase-2b and map records cover most of these as cross-checked
candidate facts, but they are not Lean proofs.  In particular, there is not
yet a final four-forget receipt in the repository that itself records
`|G_P|=504^4`, `|K|=2^24`, and the exact witness/kernel replay.  That absence
does not expose a mathematical gap in the argument; it marks the boundary
between this proof audit and the pending machine measurement.

## 7. Scope of the conclusion

Even if the finite receipt passes, the result is only

```text
Core_B4(L_E) <= Core_B4(L_P),
Core_B4(L_P)/Core_B4(L_E) ~= C2^24,
```

for this explicit four-forget construction.  It does **not** establish:

* that either core is isolated in the paper's charming `GT` groupoid;
* that either core is a typed object in the paper's `NFI_PB4^isolated(B4)`
  Main Line;
* that the quotient is a single B4 chief factor.  `C2^24` is a
  `P^4`-module statement; the additional B4/S4 action and its chief
  filtration still have to be computed;
* that any `ML(K)` reduction has 325 distinct roof values;
* that a PB3 power/annihilator list lifts through this B4 quotient;
* that the pair is part of a cofinal nested isolated family; or
* that a compatible inverse-limit branch exists, hence no B4-B conclusion.

The proof supplies a strong finite core target and removes the proposed
diagonal/strip objections, but the typed `ML`, 325, cofinality, and final
genuine-shadow arguments remain separate gates.

PASS_C2SIX_CORE_C2_24
