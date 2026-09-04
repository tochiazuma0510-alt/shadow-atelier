# Sol reply -- Task911 narrow dual-orbit and blockwise-scalar audit

## Verdict

PASS.  All four commissioned gates pass.  I used only the already-local
Task712 tables and Task907 lambda for the numerical replay, and a standalone
stdlib-only F3 parser/enumerator/reducer which imports neither v15 executable
nor any producer orbit helper.

## F1 -- PASS: roots and first children

The replay input identities are:

| object | bytes | SHA-256 |
|---|---:|---|
| Task712 `manifest.json` | 24,277 | `48c5d1f455e775cbcb3d887248de72d6bbda9df25deb5bafb8f02c8d121bdd47` |
| Task907 `lambda.bin` | 12,096 | `7522ee1f00f386b229ea46bc0f2b9fdf2854cf03c262f40a2f60dd9ced0102ed` |

I independently checked each relevant table's outer manifest receipt and
inner canonical EOF marker/body receipt, unpacked lambda in four-trits-per-byte
order, and computed `B_fwd^T lambda` directly from triples.  The result is:

| character | support | first nonzero coordinate/value | packed SHA-256 |
|---:|---:|---:|---|
| 0 | 2,742 | 3/2 | `af62027aa99fbd1a4b7b53c6b380b4e7fa7403915ea91f9d51d7cb2198c7e053` |
| 1 | 0 | none | `8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838` |
| 2 | 0 | none | `8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838` |
| 3 | 0 | none | `8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838` |

For character 0, direct application of the four `T_fwd^T` maps in actor order
`[1,-1,2,-2]` gives support 2,742 in every case and packed hashes

```text
aa54bbed30791f3f771c5fb8d74e38329564101cbcd805db20e1e232595e7033
1b98282910ed00d253cad00cbc389b9c85c6b84be9b8da0418ece4f8b0218cd8
f98650b321a16e846539698d98710a544fd1953656afcaecbee995523f0def2b
2245611c3efcef71758e281950ca4b23ba96d0991880cdb92ecafa0fac7aa8b4
```

Chronological F3 insertion of root followed by these children has rank 5 and
normalized insertion leads `[3,1,0,2,4]`.  Since every actor adjoint is
linear, each zero root in characters 1--3 has an identically zero full actor
orbit; this implication does not depend on an enumeration shortcut.

## F2 -- PASS: exact character-0 orbit

The independent breadth-first traversal deduplicated only exact 9,072-byte
packed raw rows.  Each of the four character-0 tables was independently found
to be monomial (36,288 distinct sources, 36,288 distinct destinations, all
coefficients one).  Processing all four labelled edges of every dequeued row
gave:

```text
orbit_size=504
labelled_edges=2016
queue_remaining=0
closed=true
sorted_packed_orbit_sha256=b651766655e28c82723b57df02858f910f37d3af1950c83df628c26da3e304dc
```

Standalone Gaussian elimination over F3 on the 504-by-504 restriction to
coordinates 0--503 gave rank 504 and pivots exactly `0,1,...,503`.  Encoding
that pivot list as little-endian u32 values gives SHA-256
`ab653854bfb7d723efdafaad705d6ab7b88bdd865cb4b8474a5d3932f5b4f39d`.
Thus reply910's exact closure and independence claims are reproduced without
using a producer orbit helper.

## F3 -- PASS: v540 equals v15 entry by entry

The audited v15 producer and checker have exact receipts

```text
producer  126565 bytes  76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632
checker   141770 bytes  8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662
```

Their `_global_relations` traversals give the same offsets:

```text
old ranks/ranges     505,503,503,503       offsets 0,505,1008,1511
old total                                      2014
new ranks/ranges     1509,1512,1512,1512   offsets 2014,3523,5035,6547
new total                                      6045
all P1 rows                                    8059
defect ranges        [0,2064), [2064,4120), [4120,6176), [6176,8232)
defect origins                                 8232
scalar relations     44 + 4*8059              32280
```

For every seed, v15 adds one old reduction from each old character and, for
each of its four distinct old-character origins, one origin reduction from
each of the four new target blocks.  This is exactly v540 (2.1), including
all 16 target-block expressions.  For old row `(a,p)` and actor slot `t`, it
adds the one old transition and the four new-block reductions at origin
`range[a].start+44+4*p+t`, exactly (2.2).  For new row `(b,p)`, it adds only
the transition in block `b`, exactly (2.3).  As a further multiplicity check,
v15's `new_contributions` is
`44*4*4 + 2014*4*4 = 32928`.

Both `_pair` implementations compute `direct - sum(c*value[index])` modulo
3, so every sign in v540 is correct.  Combining coincident local terms before
evaluation or adding their evaluated scalars blockwise is the same F3-linear
operation; no coefficient or multiplicity changes.

The actual Task554 producer creates origins in character, then seed, then
pivot/actor order and records the four ranges.  Its independent checker
reconstructs every expected origin record, checks every packet row, requires
`origin_cursor == len(defect_origins)`, and checks every block's complete
`origin_reductions` roster and actor transitions.  Hence the prepare roster is
the required bijection from 8,232 origin IDs to 44 seed plus 8,056 old-actor
slots.

It is therefore sufficient to retain prepare plus one new block: that block
contributes its one summand to every seed/old-actor accumulator and supplies
all of its own new-actor entries before release.  The final array is scanned
only after all four blocks, in unchanged v15 order -- seeds `0..43`, then P1
rows `0..8058`, with actor slots `[1,-1,2,-2]`.  No simultaneous pair of new
blocks occurs in a relation.

## F4 -- PASS: claim boundary and Task908

The zero roots and the 504-dimensional character-0 orbit are dual preflight
only.  They provide neither an actual P1 scalar, scalar EOF/Violation, a
Grade-2 terminal, nor any A0/common/cofinal-lift/fake/Ihara conclusion.

Task908's one-active-character reduction is mathematically safe.  For a zero
covector, all P1 values, all four adjoint-child values, and every direct seed
pairing are zero; equations v533 (2.1)--(2.2) therefore make all 32,280
scalars zero.  Linearity keeps characters 1--3 zero under every word, so only
character 0 can contribute a violation.  Character 0 still requires the
actual P1 value pass and the prescribed complete scalar scan; no terminal is
prejudged here.

No repair is required.

```text
VERDICT=PASS
DUAL_PREFLIGHT_ACCEPTED=yes
BLOCKWISE_SCALAR_EQUIVALENCE_ACCEPTED=yes
TASK908_MATH_SAFE=yes
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```
