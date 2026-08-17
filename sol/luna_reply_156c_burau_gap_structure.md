# Luna reply 156c — GAP-native low-memory GF(5) route

## Verdict

**DESIGN PASS / runtime UNKNOWN.** The strongest exact alternative is a
faithful `56 x 56` matrix realization over `GF(5)`: a `36 x 36` permutation
matrix for the roof, followed by five natural `4 x 4` Burau blocks.  It
removes the 3161-point disjoint vector action without quotienting away any
scalar kernel.  No local GAP run was made, so matrix-group performance and
the 367,416-section pass remain to be measured on GHA.

## Primary route: faithful `GL(56,5)` block diagonal image

For a roof permutation `p`, construct a row-action permutation matrix
(`A[i][i^p] := One(F)`) over `F:=GF(5)`.  Construct a block diagonal matrix
from that matrix and the five `4 x 4` A.18 Burau matrices.  A self-contained
builder avoids depending on an uncertain `PermutationMat`/`BlockMatrix`
convenience name:

```gap
F := GF(5);;
PermMat := function(p,n)
  local a,i,j;
  a := List([1..n],i->List([1..n],j->Zero(F)));
  for i in [1..n] do a[i][i^p] := One(F); od;
  return ImmutableMatrix(F,a);
end;;

BlockDiag := function(ms)
  # allocate a zero list of total dimension and copy each matrix on its
  # diagonal; return ImmutableMatrix(F,rows)
end;;

hx56 := BlockDiag(Concatenation(
  [PermMat(roofX,36)], [pair[1] for pair in A18Pairs]));;
hy56 := BlockDiag(Concatenation(
  [PermMat(roofY,36)], [pair[2] for pair in A18Pairs]));;
H := Group(hx56,hy56);;
```

The actual GAP list-comprehension syntax should be expanded to `List(...)`
inside a conservative producer.  The matrix orientation must be canaried by
`PermMat(p*q)=PermMat(p)*PermMat(q)` for the repository's right permutation
convention.  `ImmutableMatrix(GF(5),...)`, `IdentityMat`, matrix multiplication,
and `Group` on matrices are already used in the producer/source tree (for
example `search/d972_b4_burau_fiber_v2.g:89` and the matrix probes).

The representation is faithful: if a block-diagonal image is the identity,
its first block is the identity permutation matrix, hence the roof permutation
is identity, and all five natural Burau matrices are identity.  In particular,
no projective quotient or determinant-only scalar shortcut is present.

## Exact projection, derived kernel, and completeness proof

Keep the compact roof independently as `P:=Group(roofX,roofY)` and define the
roof projection from the two matrix generators:

```gap
pi := GroupHomomorphismByImages(H,P,[hx56,hy56],[roofX,roofY]);;
if pi=fail then Error("56-dimensional roof projection failed"); fi;;
Hp := DerivedSubgroup(H);;
Pp := DerivedSubgroup(P);;
hpg := GeneratorsOfGroup(Hp);;
pip := GroupHomomorphismByImages(Hp,Pp,hpg,List(hpg,g->Image(pi,g)));;
K := Kernel(pip);;
```

The producer already uses this exact API sequence—`DerivedSubgroup`,
`GroupHomomorphismByImages`, `Kernel`, `Elements`, and the order checks—in
`search/d972_b4_burau_fiber_v2.g:208-216`; this is source-confirmed rather
than a guessed API.  Require `Image(pi,Hp)=Pp` and independently require
`Size(P)=1469664`, `Size(Pp)=367416`, `Size(K)=8`, and
`Size(Hp)=Size(K)*Size(Pp)` (or the equivalent exact index formula).
Then `K=Kernel(pip)` is complete by the first isomorphism theorem, not by a
degree-dependent point-stabilizer search.  Enumerate `Elements(K)`, checking
that the list has exactly `Size(K)` distinct elements and every first block
is the identity roof matrix.

For every `f in Elements(Pp)` (exactly 367,416 elements), obtain and round-trip
an exact section element:

```gap
h := PreImagesRepresentative(pip,f);;
if h=fail or Image(pip,h)<>f then Error("section round-trip"); fi;;
```

If literal free words are required, use the confirmed free-group epimorphism
pattern already used by `search/d972_b4_word_key_artifact_v1.g:57-64`:

```gap
F2 := FreeGroup("u","v");;
toH := GroupHomomorphismByImages(F2,H,[F2.1,F2.2],[hx56,hy56]);;
w := PreImagesRepresentative(toH,h);;
if w=fail or Image(toH,w)<>h then Error("word round-trip"); fi;;
```

Stream these 367,416 records rather than retaining all matrix elements and
words simultaneously.  For the 972 roof rows, use the same section map and
retain only each row's representative plus its eight-element exact coset.

An independent relator certificate can avoid asking `Kernel` to discover the
kernel blindly.  Build `Pfp:=Image(IsomorphismFpGroupByGenerators(P,[roofX,
roofY],"roof"))`, take `RelatorsOfFpGroup(Pfp)`, evaluate every relator on
`[hx56,hy56]` with `MappedWord`, and form their `NormalClosure(H,Group(...))`.
The relators normally generate the free-to-`P` kernel, so this normal closure
is `ker(H->P)`.  Intersect it with `Hp` and compare the result set/order with
`K`; equality plus the exact product formula proves the derived kernel is
complete.  This is a certificate/cross-check, not a replacement for the
projection kernel unless equality is established.

## Lower-memory typed direct-product variant

A potentially smaller representation keeps `P` as a permutation group and
each Burau block as a `4 x 4` matrix group:

```gap
M20 := DirectProduct(GM1,GM2,GM3,GM4,GM5);;
D := DirectProduct(P,M20);;
eP := Embedding(D,1);; eM := Embedding(D,2);;
hxD := Image(eP,roofX) * Image(eM,mx);;
hyD := Image(eP,roofY) * Image(eM,my);;
H := Group(hxD,hyD);;
```

`DirectProduct`, `Embedding`, and `Projection` are source-confirmed in
`search/a18-kernel-structure.g:28-29` and the matrix direct-product probes
under `search/probe/b4_cal_v1/`.  The specific mixed-family combination of a
permutation group with a matrix group was not found in the locally available
source/docs, so its compatibility and memory behavior are **unconfirmed**.
If accepted by GAP 4.16, `Projection(D,1)` gives a native exact roof map and
is likely the lowest-memory route.  It should be a separate canary before
being treated as the production path.

## Projective and Goursat alternatives

- A projective action of `GL(4,5)` on 156 points is not faithful: it kills
  scalar matrices.  Determinant does not repair this for dimension four,
  because every scalar `lambda*I_4` has determinant `lambda^4=1` in
  `GF(5)`.  Thus projectivizing the five Burau blocks is not admissible while
  preserving the requested scalar kernels.  A natural matrix block or a
  625-point vector action is required for each block.
- No native high-level `Goursat`/subdirect-product constructor was found in
  the locally available GAP source tree.  Goursat can be implemented exactly
  after constructing the subgroup: compute the two projection kernels with
  `Kernel`, quotient with `NaturalHomomorphismByNormalSubgroup`, and compare
  the quotient orders/isomorphism.  This diagnoses the fiber-product coupling
  but does not itself produce the derived kernel or section words, so it is a
  secondary audit rather than the primary construction.
- `IsomorphismFpGroupByGenerators`, `FreeGroupOfFpGroup`,
  `RelatorsOfFpGroup`, `MappedWord`, and `NormalClosure` are source-confirmed
  in `search/d972_b4_lowindex_v1.g` and the current Burau producer.  They can
  certify relator evaluations, but fp conversion/coset enumeration is a
  runtime risk and should not replace the 56-dimensional matrix canary.

## Ranking for standard GHA memory

1. **56 x 56 faithful block-diagonal matrices:** recommended first route;
   exact, scalar-faithful, uses ordinary matrix-group and homomorphism APIs;
   expected to be dramatically below the 3161-point action, though runtime is
   still UNKNOWN until a bounded GHA canary.
2. **Typed `DirectProduct(P,M20)`:** likely lowest memory if mixed-family
   `DirectProduct` works in GAP 4.16; API compatibility is the principal
   untested risk.
3. **Fp/relator plus normal-closure route:** mathematically exact and useful
   as a cross-check, but presentation conversion and section-word extraction
   can trigger expensive coset enumeration.
4. **Projective/smaller permutation actions:** reject as primary routes because
   they lose scalar kernels unless an additional faithful central mechanism is
   supplied; determinant alone is insufficient here.

No code, local GAP run, git operation, or GHA action was performed.
