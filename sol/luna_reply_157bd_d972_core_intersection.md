# Luna reply 157bd: D972 core intersection with the C2^24 B4 cell

## Decision

For the pinned four strand-deletion maps, the structural answer is

    W = C_M/K_0 ~= V^4 ~= C2^24
    rank_F2(W) = 24.

This is conditional on the separate 157bb isolation certificate for
C_E,C_P,C_M.  It is not a B4-B, ML, cofinality, or Ihara claim.

The exact verdict token at the end means that the bounded GAP workflow is
ready to produce the lossless 24-word receipt; it does not pretend that a
local GAP run was performed.

## Pinned inputs and conventions

The producer/checker bind:

- search/certs/d972_phase2b_nonsplit_v1_20260813.json
  SHA-256
  648335000ff70f37d357c9c27ec5054cd4366b281c616f0391c4c7580cd4bcb9;
- its checker receipt SHA-256
  90db0fc500eb44bd905059d7a00dfaf4920c8c9890ed151d773141456fd059bb;
- search/certs/d972_b4_marity_reduction_maps_v1.json
  SHA-256
  6bab29852ec35210abe7bfc46e68c5457abc76653af3778921a71be8256dbfc2;
- the canonical MakeGn(9) source
  search/week3-battery-common.g
  SHA-256
  aadf1afa5e1a171d10d0aa1f9657e823cad669b960e08da7b9e7618f2ea4f998;
- search/d972_dovetail_core_v2.g
  SHA-256
  1c3348003805df874ab6d42503720259564eec25c1aebfb1c548a759e3d9f7ae.

The four maps are replayed in target order (X,Z,Y) and all six PB4 pure
generators are retained in source order (x12,x13,x14,x23,x24,x34).  The
resulting E-coordinate rows are exactly

    x12 -> (1,1,X,X)
    x13 -> (1,X,1,Z)
    x14 -> (1,Z,Z,1)
    x23 -> (X,1,1,Y)
    x24 -> (Z,1,Y,1)
    x34 -> (Y,Y,1,1).

The same six rows are independently replayed with
G9=PB3/K^(9), where |G9|=2916 and MakeGn(9) uses
x=(r,s,s), y=(sr,r,sr) on three D9 blocks.  No onto assertion for the
four-coordinate G9 image is made.

## Why the rank is forced to be 24

Let

    F = image(PB4 -> E^4 x G9^4)
    H9 = image(PB4 -> G9^4).

The E^4 projection of F is E^4.  The independent pure-coordinate
commutators are

    [x23,x34] = ([X,Y],1,1,1)
    [x13,x34] = (1,[X,Y],1,1)
    [x12,x24] = (1,1,[X,Y],1)
    [x12,x23] = (1,1,1,[X,Y]).

The pinned normal closure of [X,Y] is all E (order 32256), and its P-image
has normal closure all P (order 504).  Thus the four factor projections and
the four pure-coordinate witnesses give E^4 and P^4 structurally; no
large E^4/P^4 enumeration is used.

The marked E is perfect: the normal closure of one commutator is E, hence
E'=E, so (E^4)'=E^4.  On the other side, H9 is a subgroup of G9^4, and
G9 is a subgroup of D9^3; therefore H9 is solvable.  Goursat's lemma applied
to the subdirect product

    F <= E^4 x H9

identifies a common quotient of a perfect group and a solvable group.  That
quotient is both perfect and solvable, hence trivial.  Consequently

    F = E^4 x H9.

This is the key point: compatibility constraints in the G9^4 projection may
make H9 proper, but they cannot remove any pure E^4 element.  Therefore the
kernel of the G9^4 projection inside the E^4 image is all of E^4.  Imposing
the P^4 identity then gives exactly

    E^4 kernel of P^4 = V^4.

Since N_M=K^(9) intersect N_P, this is precisely the image of C_M/K_0 in
C_P/C_E, subject to the stated 157bb isolation condition.

## Lossless certificate

The GAP producer constructs the joint permutation image on eight disjoint
blocks (four degree-72 E blocks and four degree-27 G9 blocks).  For each
coordinate 1..4 and each pinned module basis element (u,v,w,x,y,z), it asks
PreImagesRepresentative for a signed word in the six PB4 generators mapping
to

    (1,...,basis,...,1) in E^4
    (1,1,1,1)       in G9^4.

The receipt therefore contains 24 lossless records with:

- coordinate and module-basis index;
- signed source word in +/-1,...,+/-6;
- all four degree-72 E target arrays;
- all four degree-9 P target arrays (all identity);
- all four degree-27 G9 target arrays (all identity).

The independent Python checker rebuilds E/V/P and MakeGn(9) without importing
producer code, replays every word in E^4, P^4, and G9^4, and checks the
distinct 24 basis targets.  Thus the word list itself certifies rank 24;
the Goursat argument certifies that the list spans the entire possible image.

The receipt also records the induced B4 action: PB4 acts blockwise through
P^4, B4/PB4=S4 permutes the four coordinates, and the pinned B3 stabilizer
twists are retained.  The structural composition-factor record is one
24-dimensional induced V-module with multiplicity one.

## Versioned assets and checks

Created/updated only within the authorized scope:

- search/d972_d972core_c2six_intersection_v1.g
- search/check_d972_d972core_c2six_intersection_v1.py
- .github/workflows/d972-d972core-c2six-intersection-v1.yml
- this reply
- the parent-directed 157ax JSON-root/inline-if repair and its reply note.

Final 157bd hashes (before the parent-directed witness-index repair):

- producer:
  52005b33e3357afa85a5f0400eb9f9589ab052d0f18f0844a7e514bb16438aae;
- independent checker:
  d0ba83e21fab0dcb2dd29a9b5d70ab67f2abb5938be4cf9f99c5df0d6c4dc06c;
- workflow:
  f82e7110e5ee0a13db362df8e01b795e521d5ab42ba0576438a183c4b925f208.

The bounded Python selftest passes:

    D972_CORE_INTERSECTION_CHECKER_SELFTEST_PASS

No local GAP, git, push, or GHA was run.  The workflow uses the corrected
JSON package parent ($json_root, containing pkg/json) and emits
UNKNOWN_TIMEOUT rather than treating a timeout as a mathematical result.

## Parent-directed witness-index correction

An independent audit found a coordinate indexing defect in the pure-coordinate
witness replay: the 1-based witness coordinate was compared directly with the
0-based tuple index.  It is now compared as `index == coordinate - 1`.  The
bounded checker selftest additionally replays all four pure witnesses and
rejects a mutated witness permutation.  No producer mathematics changed and
no local GAP, git, push, or GHA was run.

The repaired checker selftest remains
`D972_CORE_INTERSECTION_CHECKER_SELFTEST_PASS`.  The hashes below are the
repaired working-tree bindings and await the parent commit/rerun:

    52005b33e3357afa85a5f0400eb9f9589ab052d0f18f0844a7e514bb16438aae  search/d972_d972core_c2six_intersection_v1.g
    bf08617ec9b1c9943ed3f655efecaa8fdb12a3125aaea7f9fa80564c81d5bd22  search/check_d972_d972core_c2six_intersection_v1.py
    77efe8d1cdef6ce69b95c00109abf42d13991de37f8e5a6a76e9223a190bead6  .github/workflows/d972-d972core-c2six-intersection-v1.yml

## Operational run record

The current 157bd broker run is `32063204094` on commit `fb81f566`; it is the
pre-repair run and must not be read as validation of the repaired bundle.  The
workflow's short-marker-prefix gate and the checker coordinate/mutation repairs
are awaiting the parent commit and rerun.  The exact order/rank values remain
receipt and independent-checker gates.  The repaired checker selftest remains
`D972_CORE_INTERSECTION_CHECKER_SELFTEST_PASS`.  No local GAP, git, push, or
GHA was run in this follow-up.

D972_CORE_INTERSECTION_RANK_24_READY_FOR_GHA
