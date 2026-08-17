# Luna reply 157ax: exact four-forget core quotient

## Scope and source binding

The producer and checker bind the following immutable inputs:

- Phase-2b source receipt: search/certs/d972_phase2b_nonsplit_v1_20260813.json
  SHA-256 648335000ff70f37d357c9c27ec5054cd4366b281c616f0391c4c7580cd4bcb9.
- Its independent checker receipt:
  90db0fc500eb44bd905059d7a00dfaf4920c8c9890ed151d773141456fd059bb.
- Canonical four PB4-to-PB3 forgetting maps:
  search/certs/d972_b4_marity_reduction_maps_v1.json
  SHA-256 6bab29852ec35210abe7bfc46e68c5457abc76653af3778921a71be8256dbfc2.
- Existing map-checker SHA-256
  eb87e9d42ecde979b82a31beec8fdedea3e221a55d4881f8a71dbaffc2a7a032.

No old raw-158 presentation is read or used.

## B3 normality and four-map reduction

The pinned marked arrays reconstruct E of order 32256, V of order 64, and
P=E/V of order 504.  The checker independently replays the two finite
marked quotient automorphisms

    theta: (X,Y) -> (Y,X)
    tau:   (X,Y) -> (Y,Z),   Z=(Y*X)^-1

as bijections on both E and P.  Together with the central PB3 generator
mapping to one, this proves that both N_E and N_P are B3-normal from the
marked quotient data, rather than from the N_E_isolated label alone.

The canonical strand-forgetting artifact is replayed with target order
(y12,y13,y23)=(X,Z,Y).  All six PB4 generator images, in coordinate order
(d_1,d_2,d_3,d_4), are

    x12 -> (1,1,X,X)
    x13 -> (1,X,1,Z)
    x14 -> (1,Z,Z,1)
    x23 -> (X,1,1,Y)
    x24 -> (Z,1,Y,1)
    x34 -> (Y,Y,1,1).

Because the kernels are B3-normal, the B4/PB4=S4 core orbit has 24 conjugates
but reduces exactly to these four forget-strand kernels.  The producer records
the three frozen conjugation identities from the map artifact and the
checker rejects any map-table mutation.

## Direct-product certificate

The producer does not enumerate a subgroup of E^4 or P^4.  It uses these
four pure-coordinate commutator witnesses, with pair indices in the generator
order (x12,x13,x14,x23,x24,x34):

    coordinate 1: [x23,x34] = ([X,Y],1,1,1)
    coordinate 2: [x13,x34] = (1,[X,Y],1,1)
    coordinate 3: [x12,x24] = (1,1,[X,Y],1)
    coordinate 4: [x12,x23] = (1,1,1,[X,Y]).

The independent checker replays every permutation identity.  It also
reconstructs the normal closure of [X,Y] from the pinned E arrays and obtains
order 32256; in the canonical P quotient the corresponding normal closure
has order 504.  Hence each coordinate copy is present, proving

    G_E = E^4
    G_P = P^4

by a finite structural certificate.  The pair projections are therefore all
E^2 and P^2; no large subgroup enumeration is trusted.

Consequently the coordinatewise quotient has

    |G_E| = 32256^4 = 1082535236962615296
    |G_P| = 504^4   = 64524128256
    |ker(G_E -> G_P)| = 64^4 = 16777216

and

    C_P/C_E ~= V^4 ~= (C_2)^24.

A nonzero witness is required in the full GAP run: the producer asks for a
source word mapping to the pure first-coordinate element (u,1,1,1), where
u is the pinned nonidentity module basis element.  The checker replays the
word, checks that the first coordinate lies in V and is nonidentity, and
checks that all four images vanish in P.

## B4 action and factors

The receipt stores the six blockwise conjugation matrices on the ordered
basis (u,v,w,x,y,z) for every pure PB4 generator, together with the
theta/tau stabilizer matrices.  The S4 quotient action is stored by the
coordinate transpositions

    (1 2), (2 3), (3 4)

and the action is the induced four-coordinate module: PB4 acts through P^4,
while B4/PB4=S4 transports the four factors, with the checked B3 stabilizer
twists.  The structural factor record is one irreducible 24-dimensional
induced module (multiplicity one).  The input boundary records that B4
isolatedness and cofinal B4-B have not been claimed by this local cell.

## Versioned assets and no-GAP checks

Created only:

- search/d972_c2six_fourforget_core_v1.g
- search/check_d972_c2six_fourforget_core_v1.py
- .github/workflows/d972-c2six-fourforget-core-v1.yml
- this reply

The independent bounded Python selftest passes:

    D972_C2SIX_FOURFORGET_CORE_CHECKER_SELFTEST_PASS

No local GAP, git, push, or GHA was run.  The workflow performs the GAP
4.16.0 run, independently checks the lossless receipt, uploads evidence on
failure, and emits UNKNOWN_TIMEOUT rather than treating a wall-clock stop
as a result.

FOURFORGET_CORE_READY_FOR_GHA

## Parent broker record

The parent Sol session committed and pushed the frozen 157ax bundle at
commit `8d761af957285e322019eba8195cbf19c6e1113c`.  The resulting GitHub Actions
run is `32059992054` (`d972-c2six-fourforget-core-v1`), initially queued on
2026-08-18 JST.  Its runtime result is not predeclared here.

## JSON package root repair (parent-directed)

Run `32059992054` failed before the GAP mathematics: `LoadPackage("json")`
was unavailable.  The workflow had built the package at
`$json_root/pkg/json` but exported `$json_root/pkg`; GAP consequently searched
the wrong package parent.  The one-line repair exports `$json_root`, so GAP
searches `$json_root/pkg/json`.  The parent committed and pushed this repair
as `89940c65d92aaa40191ac038f671fb1b7c923bfe`; rerun `32061782819`
(`d972-c2six-fourforget-core-v1`) was launched and then failed at the GAP
selftest as described below.  No local GAP was run.

The same rerun then reached the GAP selftest and exposed a GAP 4.16 syntax
error at producer line 158: GAP does not accept an inline `if ... then ...
else ... fi` as a `List` expression.  The pure-coordinate expected-value
helper was rewritten as an explicit loop, with no change to its mathematics.
The updated producer hash is
`19e6f491d6fc2b187f781b8d29d3ae80707a53186b5c35c5e04c14924209337a` and the
workflow hash binding was updated.  A static audit found no remaining inline
conditional expressions in either the repaired 157ax producer or the new
157bd producer; no local GAP was run.
