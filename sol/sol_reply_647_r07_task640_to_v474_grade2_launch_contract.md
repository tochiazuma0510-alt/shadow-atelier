# Sol(max) Task647 reply: Task640-to-v474 grade-two launch contract

## Verdict

`READY_FOR_LUNA_CONTRACT`

There is no missing mathematical datum.  The complete grade-one presentation
can be reconstructed from the already sealed Task554 prepare and four
exhausted character blocks, and v474/Task626 gives the exact targeted decision
once a fresh residual is independently accepted.  Task640 has not yet supplied
such a residual.  The now-completed Task646 audit returned `FAIL` and
`SAFE_TO_DISPATCH_GHA=no`; the contract is therefore conditional on its finite
release defects being repaired and re-audited, followed by an actual accepted
run.

Task565 is not an accepted grade-two module or checker.  Its forward arithmetic
is useful translation material, but its known authentication, checker-isolation
and resource defects must not cross the new boundary.  The shortest sound path
is a new grade-two-specific owner and an independently reconstructed checker,
not completion of the Task565 full-module route and not a generic framework.

No implementation, production computation, GHA run, proof/v220 edit, or git
operation was performed.  `verified=false`.

## 1. The two disjoint accepted inputs

### 1.1 Future witness-side input: an accepted Task640 residual

The mathematical datum is

```text
rho2 in P = F3^48384,
packed as 12,096 bytes, four consecutive trits per byte,
with coordinate order fixed in Section 3.1 below.
```

For a byte containing coordinates `4j,...,4j+3`, the canonical encoding is
`t0 + 3*t1 + 9*t2 + 27*t3`; hence every byte is in `0..80`.  The dense form is
48,384 bytes in `0,1,2`, and unpacking the packed form must equal it entry by
entry.  The residual is accepted only together with the independently checked
identity

```text
rho2 = gr_2(direct target - direct physical replay(C_1)),
all 32,260 physical lower/auxiliary coordinates = 0.
```

The present frozen Task640 quartet is rejected dispatch-candidate code:

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 27,227 | `d8957511167f3ace568f59fd2d50dfcdbd7a16fc50bd4475077fcd73dbc3a5b9` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 85,627 | `3b8b335da4a2233977464fc553e040a3a0f0c79d5bf58451255d8370e63e88af` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml` | 9,974 | `0f8df3e4bfd22024ffd0f3c5841717441dc03dedb8834cec9fe46a460634826f` |
| `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md` | 2,833 | `508c28e322dae868f2dd7043a3ed4a01c4110fffb8fbe4154b4d25c29577896f` |

The grade-two owner may consume its output only after all of the following
gates pass.

1. An exact repaired successor receives `PASS`, `SAFE_TO_DISPATCH_GHA=yes` in
   a new finite re-audit.  Task646 found three concrete blockers in this
   quartet: producer/checker disagree on string versus integer types for four
   parent run fields; the checker follows self-declared filenames instead of
   requiring the seven canonical receipt filenames; and the advertised R8
   mutations do not exercise the live production validators.  The repair must
   close all three without weakening R1/R3/R4/R5/R7.  A static pass alone is
   not a residual.
2. Root authenticates the actual Task640 workflow run, attempt, event head,
   job, conclusion, and the nonexpired immutable artifact named
   `task640-fresh-rho2-v3-<run>-<attempt>`, including artifact id, archive byte
   count, digest, and matching `workflow_run.id/head_sha`.  These values must
   be read from the actual run; no placeholder is legal.
3. The payload has one canonical `manifest.json`, the producer marker
   `R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V3_CANDIDATE`, and exact receipts
   for:

   ```text
   rho2.bin                    12,096 bytes
   rho2-dense.bin              48,384 bytes
   lower-dense.bin             32,260 bytes, all zero
   target-dense.bin            80,644 bytes
   path-signatures.json        canonical, actual byte count/hash
   signature-buckets.json      canonical, actual byte count/hash
   authenticated-roots.json    exact accepted Task625 roots bytes
   ```

   The two JSON-table sizes are result-dependent and must be taken from the
   manifest.  The manifest must bind support, the canonical sorted sparse
   `(coordinate,value)` digest, dense SHA, packed SHA, and packing round trip.
4. The independent Task640 checker emits canonical schema
   `d972.r07.a0.fresh-precision2-endpoint-signature.v3.checker` and marker
   `R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V3_CHECKER_PASS`, binding the exact
   payload-manifest SHA, packed-rho SHA, and counts 32,260/48,384.  Root then
   performs the external artifact audit.  A producer manifest without this
   checker receipt is not accepted.
5. The manifest/checker must bind the accepted Task625/639 parent exactly:
   run/attempt/job `33734643746/1/100582244001`, head
   `b401d724bbdbef8cf67e96def22fc51c014ab546`, artifact id `9885925239`,
   archive bytes `50,793,121`, digest
   `sha256:ac3121f3bc1a7e2a6c267f20352e953b7343f9085015dd74e4a67e4b90129a75`,
   manifest SHA
   `381f961fc808076c5c0adbc98e32c19742565087bffbcd5f99772533e05d5c22`,
   rerun-and-byte-equal checker verdict SHA
   `a650aa8d5d78f52145fff5ba7769ad2036cfd16e90e3caaf367b4517e07d2740`,
   all fifteen Task639 file receipts, and the Task595 MEMBER body/basis/zero
   remainder pins.  The exact prior root followed by selected root order is
   `C_1=Compose(C_<1,C_T)`.
6. Both producer and checker must independently perform the raw-source seed
   gate before cancellation, all nonzero exact-key direct all-seven canaries,
   all eleven typed endpoint slots, the first-six restriction only afterward,
   and the full dense lower/top replay.  All later claim fields remain their
   required false/null values.  `NOT_READY`, `UNKNOWN_RESOURCE`, a partial
   payload, an unchecked stored `next_degree2_residual`, or a hash-only equality
   is not an accepted `rho2`.

The eleven endpoint slots belong to this witness receipt.  They do not enlarge
the module-side source from six occurrence tags to eleven.  In particular no
`11 -> 6` adapter is an input to v474: Task640's five P-slots remain typed
endpoint evidence, while the accepted dense `rho2` already lives in the
48,384-coordinate physical two-hexagon row.

### 1.2 Presentation-side input: the complete grade-one transition presentation

The immutable source bytes are the Task554 v3-schema states from
run/attempt `33677346616/1`, head
`22c6dddb43d107c05e65f53ad898823ae8ebe276`:

| phase | exact artifact id | exact state-body SHA-256 | rank/receipt |
|---|---:|---|---|
| prepare | `9865061266` | `1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865` | old ranks `505,503,503,503`; 8,232 origins |
| block 0 | `9865238399` | `9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74` | rank 1,509; attempts 14,268; FIFO EOF |
| block 1 | `9865242284` | `d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6` | rank 1,512; attempts 14,280; FIFO EOF |
| block 2 | `9865193269` | `a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac` | rank 1,512; attempts 14,280; FIFO EOF |
| block 3 | `9865239848` | `642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01` | rank 1,512; attempts 14,280; FIFO EOF |

The artifact names are exactly
`task554-grade1-v3-prepare-33677346616-1` and
`task554-grade1-v3-state-block-<a>-33677346616-1`.  Before a launch, root must
also query and freeze each actual archive size/digest/expiry/workflow envelope;
the state-body pins above do not substitute for that service receipt.  Inside
the artifacts, require canonical HEAD/body linkage, the common embedded input
manifest and all its pins, exact parent linkage from each block to prepare,
every blob filename/shape/byte count/SHA, and no extra or missing phase file.

From those bytes the owner and checker must reconstruct the following typed
object, not merely trust a summary:

```text
P_1 = (b_0,...,b_8058), rank 8,059,
b_i in F3^96,776 = source degrees 0 and 1 plus 8 auxiliaries,
44 exact seed reductions in the ordered b_i,
four exact actor reductions for every b_i,
literal prior-only DAG ancestry, actual leads and scales for every b_i.
```

The global basis order and offsets are fixed:

```text
old character blocks:  offsets 0, 505, 1008, 1511
new H^[1] blocks:       offsets 2014, 3523, 5035, 6547
end:                    8059
```

Each stored basis row must be nonzero, normalized at its actual first nonzero
coordinate, have a distinct in-range lead, and have a topologically prior
reduction/DAG.  The checker must replay all 44 seed equalities and all
`4*8059` actor equalities, not sample them.  It must also replay v451's
extension, negative substitution, crossed-cochain, PB3 translated-boundary,
both PB4 block, filtration, occurrence/aggregation, auxiliary and integral
normalized-exponent gates.

The Task606/639 results authenticate the registered physical grade-one MEMBER
route and the selected witness.  They do not make a separate Task565
transition-presentation artifact accepted.  Thus the exact Task554 bytes are
accepted immutable input, while their assembly and the complete semantic
checks just listed are recomputed at the new boundary.

### 1.3 Status taxonomy

| status | may be treated as input authority? |
|---|---|
| Task554 prepare/four-block bytes with the exact run/artifact/state receipts | yes, as immutable raw presentation data |
| Task625/639 selected SLP and a future externally accepted Task640 payload/checker pair | yes, as the witness chain and `rho2` |
| assembled `P_1`, precision-two lifts, defects, maps, connections, separators | only after deterministic recomputation and new receipts |
| Task565 source code and bounded fixtures | specification/translation material only |
| a Task565 `FIRST_RUNG_GRADE2_MODULE_READY` artifact | none exists or is accepted |
| Task565 checker output, old join state, Task595 physical basis as a presentation | never an authority for this contract |

## 2. Smallest reusable and translatable shelf

No new abstraction layer is needed.  The following narrow surfaces suffice.

| exact path | accepted use in the new producer/checker |
|---|---|
| `search/d972_r07_a0_first_rung_grade1_v4.py` (`1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4`) | Producer-side translation or exact hash-pinned reuse of `pack_trits`, `unpack_trits`, packed AXPY, `PackedEchelon.reduce_packed/_accept_remainder`, and canonical state/blob readers.  Its `Context`, `act_pair` and `aggregate_pair` are useful precision-one preflight references.  No phase runner is called. |
| `crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v2.py` (`a0504ae6a2562aab3b9af5ba7ed672bcc87bbd1cfdf5cc9fd3489240e51008e3`) | Translate the independent checker's local `pack/unpack`, `IndependentOwner`, `read_sealed/read_blob`, `Arithmetic`, `aggregate_pair`, source-state loading and 8,059-row ordering.  It is a base for the new independent parser, not a grade-two proof by itself. |
| `search/d972_r07_a0_first_rung_grade2_prebuild_v1.py` (`acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8`) | Translate only the audited forward arithmetic: the fixed monomial/layout tables; polynomial multiplication and `e_polynomial`; source views; `act_precision2`; `associated_degree2_actor`; `evaluate_seed_precision2`; `aggregate_precision2`; the v451 preflight; presentation assembly/lift/defect formulas; and the lower-first recursion in `run_merge_core`.  Refactor these into the charged one-row interfaces in Section 3. |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` (`3b8b335da4a2233977464fc553e040a3a0f0c79d5bf58451255d8370e63e88af`) | Its self-owned quotient/word/Fox and truncated-ring evaluator is useful checker-side translation material only after the Task646 R2/R6/R8 repairs receive a new PASS.  The grade-two checker still copies no executable producer helper and reconstructs its maps locally. |

The following Task565 surfaces are explicitly rejected as reusable owners:

- `run_block_core`, `validate_block_state`, `run_merge_core` as a completed
  module artifact, `run_member_join`, `validate_join_state`, and the phase
  dispatcher;
- `search/check_d972_r07_a0_first_rung_grade2_prebuild_v1.py` as an independent
  checker (`fc6f9976b4e3164d4dff31c05256750ddb4758856f39ac5b1fceb43249fbdecf`).

Task568 found that this checker can accept false/dependent declared bases and
insufficiently founded DAGs, has no real join checker, shares the floor helper
with the producer, and performs repeated dense decoding.  The producer also
stores unbounded nested coefficient forests, repeats the four word projectors
per defect, and repeats dense row work.  Omitting Task565's H2 blocks, final
module and join avoids their local holes; it does not waive fresh independent
validation of the upstream Task554 presentation and lift DAG.

## 3. Finite producer interface

### 3.1 Frozen coordinate and traversal orders

All serialization and every producer/checker loop use these orders verbatim:

```text
field                         order
characters                    (0,0), (0,1), (1,0), (1,1)
actors                        x, x^-1, y, y^-1 = 1,-1,2,-2
degree-two monomials          u1^2,u1u2,u1u3,u2^2,u2u3,u3^2
source coordinate in V_a      tag 0..5, component 0..1,
                              monomial 0..5, PSL index 0..503
physical P coordinate         character 0..3, block 0..1,
                              component 0..1, monomial 0..5,
                              PSL index 0..503
physical L coordinate         degree 0 (8,064), then degree 1 (24,192),
                              then four auxiliaries
grade-two defect origins      seeds 1..44, then
                              (basis i=0..8058, actor in the fixed order)
```

Thus origin `o<44` is seed `o+1`, and origin
`o=44+4*i+t_index` is the transition of `b_i` by the indexed actor.  No
monomial subowner and no action on an already aggregated physical row is
legal.

The six occurrence aggregation triples are exactly

```text
(tag,physical block,coefficient) =
(0,0,1),(1,0,2),(2,0,1),(3,1,2),(4,1,2),(5,1,1).
```

The six prefix shifts are reconstructed from the exact `g760` tag images as

```text
identity, tags(g760)[2], tags(g760)[2],
tags(g760)[5] * tags(g760)[4]^-1,
tags(g760)[5], tags(g760)[5],
```

using the pinned multiplication convention.  Producer and checker derive this
table independently and check every resulting sparse coordinate entry.

### 3.2 Presentation and lift API

The producer exposes an internal read-only `Presentation1` with these finite
operations:

```text
basis(i)                  -> normalized b_i, lead, scale, literal DAG
seed_reduction(s)         -> canonical coefficient stream in b_0..b_8058
actor_reduction(i,t)      -> canonical coefficient stream in b_0..b_8058
lift2(i)                  -> exact source row through degree 2 plus auxiliaries
```

`lift2(i)` is reconstructed in increasing `i` from its authenticated prior-only
DAG.  Its truncation through degree one must be byte-equal to `basis(i)`.
Coefficient streams are flat binary records with exact row count, nonzero
count, EOF and content hash; they are not nested JSON lists.

### 3.3 Sequential connection transducer

For each offer `i=0,...,8058`, compute the exact physical lift

```text
ell_i in L = F3^32260,     g_i in P = F3^48384.
```

The stateful operation

```text
connection_step(i, lower_state)
```

reduces `ell_i` against earlier normalized lower pivots in actual-leading-
coordinate order.  If it accepts at lower pivot `j` with scale `sigma_i`,
store

```text
u_j = sigma_i * (e_i - sum_p q[i,p] u_p),
ell(u_j), g(u_j).
```

If it is lower-dependent, store

```text
k_i = e_i - sum_p q[i,p] u_p,
c_i = g_i - sum_p q[i,p] g(u_p),
```

and emit the connection record even if `c_i=0` or is physically dependent.
The connection order is increasing dependent offer index.  EOF means all
8,059 offers were consumed exactly once.  It records the actual lower rank
`p`, exactly `8059-p` dependent offers, the reduction/scale transcript and a
rolling row/ancestry digest.  No grade-one value such as 1,661 or 5,044 may be
silently copied as this grade-two lower rank.

### 3.4 One requested defect slice

The pure operation

```text
defect_slice(a,o) -> d[a,o] in V_a = F3^36288
```

constructs the complete precision-two seed or actor-transition defect from
`Presentation1`, first compares all 96,776 source lower/auxiliary coordinates
with zero, and only then returns the requested direct character slice.  It
binds `(a,o)`, the full seed/transition expression, parent row, actor and all
lift DAG references.  Direct slicing is permitted only after the four pinned
v447 projector words are structurally proved to be the four character
selectors and to resolve the identity; four expensive word applications per
defect are not required.  All six monomials remain coupled.  A one-character
flat packet may be produced by calls `o=0..32279`, but the API never requires
four resident packets.

### 3.5 Forward and adjoint maps

For every character `a` and actor `t` expose

```text
T_fwd(a,t,v) : V_a -> V_a
T_adj(a,t,q) : V_a* -> V_a*
B_fwd(a,v)   : V_a -> P
B_adj(a,lam) : P* -> V_a*.
```

Each map is generated from a canonical sorted sparse coordinate table.  If a
forward table entry is `(source,destination,c)`, the definitions are

```text
F(v)[destination] += c*v[source],
F*(q)[source]      += c*q[destination].
```

Duplicate destinations are combined mod 3 and zero sums deleted.  This
identity is checked for every table entry, character, tag, component,
monomial, PSL index, sign and prefix.  Also check
`T(a,x)T(a,x^-1)=T(a,y)T(a,y^-1)=id`.  `B` is built occurrence-first from the
six-tag table and only then aggregated.  Sampled dot products are regression
canaries, not the transpose proof.

For an actor tuple `w=(t1,...,tm)`, the only convention is

```text
T[a,w] = T[a,t1] ... T[a,tm],
q[a,w] = B_adj(a,lambda) composed with T[a,w],
right extension w+t uses T_adj(a,t)(q[a,w]).
```

The primal violation uses the identical tuple `B_fwd(a,T[a,w]d[a,o])`.
Words are stored as topological `(parent,appended_actor)` records; no reversal
or unrecorded rewriting is allowed.

### 3.6 Packed echelon, pairing and ancestry

All widths here are divisible by four.  A packed reducer must reject bytes
outside `0..80`, locate the actual first nonzero trit, reduce by the pivot
registered at that lead, and record reductions in encounter order.  A nonzero
remainder with leading value 2 is scaled by 2, so every stored pivot has lead
value 1.  Pivot ids are insertion order; leads are unique but need not be
monotone.  Packed AXPY and packed dot-product tables are checked against dense
GF(3) arithmetic on bounded exhaustive byte canaries.

For a dual offer, persist two logically separate objects:

1. the normalized packed pivot used for later reductions; and
2. the unreduced raw representative descriptor carrying its exact word, used
   for children and defect pairings.

The raw full row may be recomputed from its descriptor when consumed, avoiding
a second 329-MB basis, but its reconstructed packed hash must match the offer
receipt.  A normalized combination may be paired only if the emitted primal
row is the identical recorded combination; the shortest implementation uses
raw representatives only.

Every physical row inserted into `S` carries a content-addressed ancestry DAG:

- connection: offer `i`, `ell_i/g_i`, ordered lower reductions, all recursive
  `u_p` scales, and the complete lifted-`b_i` literal DAG;
- orbit violation: character, defect id, exact actor word and the complete
  seed/transition defect expression;
- physical insertion: raw row hash, prior S reductions, lead and normalization
  scale.

Records are topological flat binary streams with explicit counts/lengths/EOF.
Anonymous rows, digest-only span assertions, and forward references are
rejected.

### 3.7 Canonical separator and CEGAR loop

Let the normalized rows of current `S` be constraints with right side zero and
append the equation `rho2` with right side one.  Compute the unique reduced row
echelon form of this augmented equation system using physical coordinates
`0..48383` as variable order, pivots normalized to one, and elimination above
and below every pivot.  If consistent, set every free functional coordinate to
zero and back-substitute; this defines the canonical `lambda`.  If
inconsistent, retain the row-operation coefficients of the contradiction.
They express `rho2` in `S` after normalizing the nonzero coefficient of the
last equation, and hence give the MEMBER back-substitution.

For a consistent separator, test connections for this same `lambda`, then
characters in the fixed order.  For one character, offer
`q[a,empty]=B_adj(a,lambda)` and use FIFO; every accepted raw representative
spawns four right-extended children in actor order and is paired with defect
ids `0..32279`.  Store normalized pivots separately from raw descriptors.
The exact orbit receipt is

```text
rank r_a <= 36,288,
offers = 1 + 4*r_a,
FIFO EOF, every child dependent at EOF,
pairings = 32,280*r_a, pairing EOF.
```

At the first nonzero connection/pairing, construct the matching primal row,
reduce it against `S`, require it to be independent, insert it with ancestry,
and begin a new separator pass.  A deterministic batch may retain multiple
violations only by inserting them in discovery order and keeping only those
independent of `S` plus the earlier batch.  This gives the audited bound of at
most `48,384-r0+1` separator solves.

## 4. Genuinely independent terminal checker

The checker imports neither the producer, Task565, the grade-one producer nor
their floor helper.  It may parse the same pinned raw tables, but it locally
reconstructs the marked quotient, affine/truncated polynomial arithmetic,
six occurrence maps, character maps, `T`, `B`, both adjoints, packing and
echelon logic.  It authenticates both parent blocks, every canonical
state/blob/checkpoint link, all order tables, every actual lead/scale and every
structural transpose entry before considering a terminal.

### MEMBER

The checker must:

1. independently reconstruct every raw row named by the selected S ancestry;
2. replay all physical reductions and the contradiction/back-substitution,
   obtaining the exact coefficient expression for `rho2`;
3. expand connections through the lower recursion and every other row through
   its defect, actor word, lift and source literal ancestry;
4. build the canonical literal grade-two update using the v465/v469 order and
   evaluate it directly through precision two; and
5. compare all 32,260 lower/auxiliary coordinates with zero and all 48,384 top
   coordinates with the accepted dense `rho2`, not merely their hashes.

Only this supplies a selected `Delta C_2` for the v479 witness branch.  It is
not a complete presentation `P_2`.

### NONMEMBER

The checker must independently verify `lambda(rho2)=1` and recompute the same
canonical separator.  It then:

1. replays all 8,059 connection offers to connection EOF, reconstructs every
   dependent `c_i`, and checks `lambda(c_i)=0` (rows already in `S` may be
   skipped only through their checked containment ancestry);
2. for each of four characters, reconstructs the root dual, every accepted
   raw representative and normalized pivot, all four children of each
   accepted row, exact FIFO exhaustion and offer count;
3. pairs every accepted raw representative with every one of the 32,280
   independently reconstructed defect slices, in order, and requires zero;
   and
4. matches exact transcript counts/digests and EOF markers to the producer
   certificate.

The exact pairing total is `32,280*(r_0+r_1+r_2+r_3)` and is at most
`4,685,506,560` in one outer pass.  A zero dual root has rank zero, one root
offer and zero pairings; it still needs an EOF receipt.  Completion for an old
separator cannot be reused after `S` changes.  These gates prove that the
final `lambda` annihilates every generator in
`span(Conn)+sum_a B_a(H_a)` while separating `rho2`.

Every cap, missing parent, interrupted stream, noncanonical row, incomplete
connection/orbit/pairing scan, or checker cap has the sole mathematical status
`UNKNOWN_RESOURCE`/`NOT_READY`.  A checkpoint, a producer-only terminal or a
digest without replay is never MEMBER or NONMEMBER.

## 5. Streaming and honest resource envelope

The exact packed row-family ceilings are:

| live family | row bytes x maximum rows | packed bytes |
|---|---:|---:|
| physical `S` basis | `12,096 x 48,384` | `585,252,864` |
| one normalized character-dual basis | `9,072 x 36,288` | `329,204,736` |
| lower pivots | `8,065 x 8,059` | `64,995,835` |
| lower grade companions | `12,096 x 8,059` | `97,481,664` |
| one character defect packet | `9,072 x 32,280` | `292,844,160` |
| all connection rows, if retained (do not) | `12,096 x 8,059` | `97,481,664` |
| full source precision-one basis cache | `24,194 x 8,059` | `194,979,446` |
| full source degree-two lift cache | `36,288 x 8,059` | `292,444,992` |

The first four rows total `1,076,935,099` bytes.  If both source caches and one
current defect packet are also live, the exact packed-file total is
`1,857,203,697` bytes (about 1.73 GiB), before map tables, transcripts, array
headers, decoded scratch, page cache and interpreter overhead.  V474's
separate conservative dense lower-basis/companion allowance is
`650,393,860` bytes.  These are byte counts, not an RSS promise.

Use read-only mmap or sequential file-backed owners, one decoded row/chunk at a
time, and packed AXPY/pairing.  Only one character defect packet and one dual
basis may be live.  Store raw dual representatives as recomputable descriptors,
stream connections instead of storing 8,059 physical rows, and unmap/discard
the current dual basis on a violation or after its character receipt.  Four
defect packets may exist durably if useful, but only one is mapped; the
shortest disk path constructs one character packet, consumes it, and moves on.

A release workflow should preregister and enforce the existing hard 7-GiB
internal RSS ceiling (`7,516,192,768` bytes), an 8-GiB virtual-memory
outer guard, explicit wall/offer/pairing/separator/path/transcript/durable-byte
caps, and a transcript cap independent of RSS.  The raw totals above leave
room under 7 GiB only if nested Python objects and dense cast temporaries are
absent.  Exceeding any chosen cap is an honest `UNKNOWN_RESOURCE`; the theorem
does not promise completion inside one runner.

Safe sharing/omission is exactly:

- share within one executable the authenticated sparse descriptor for a map
  and derive its adjoint mechanically; the independent checker derives a
  separate descriptor;
- share one defect-origin ancestry across its four direct slices, and
  recompute a rare slice on demand or stream one flat character packet once;
- omit all Task565 primal H2 closures, its final physical module, all four
  simultaneous character owners, stored connection rows and a second full
  raw-dual matrix;
- retain only the monotone targeted span `S`, one current dual basis, the
  lower connection transducer and flat ancestry/checkpoint streams.

The only authorized reductions are exact echelon normalization, exact direct
character slicing after the projector identity, processing the four direct
summands one at a time, replacing primal closure by v474's dual annihilator
criterion, recomputing raw representatives from exact word descriptors, and
batching only independently inserted violations.  Signature merging,
monomial splitting, dropping zero-looking origins before their gates,
physical action after aggregation, sampled transpose checks, or replacing the
complete presentation by the selected Task625 span is not span-preserving.

Task568's concrete warnings remain load-bearing: nested coefficient metadata
was already at least 1.429 GB at only 100 pairs per expression and 7.107 GB at
500 before integer/DAG/row costs; its formal pair ceiling exceeds 500 GB.
Repeated full-row decode/cast paths read hundreds of GB, and the old
per-defect word projectors alone extrapolated to about 2.98 hours.  None may be
copied into the new hot path.

## 6. One bounded GHA definition and exact checkpoints

Yes, one bounded workflow definition can legally dovetail a primal targeted
prefix and the dual CEGAR passes.  It cannot guarantee a terminal in one
bounded job.  Its legal state machine is sequential:

```text
AUTH_INPUTS
 -> BUILD_OR_AUTH_PRESENTATION
 -> PRIMAL_PREFIX
 -> SEPARATOR
 -> CONNECTION_SCAN
 -> DUAL_CHAR_0 -> ... -> DUAL_CHAR_3
 -> MEMBER | NONMEMBER | UNKNOWN_RESOURCE(checkpoint)
```

`PRIMAL_PREFIX` inserts a preregistered canonical prefix of the sequential
connections (and, only if explicitly requested, canonical forward rows built
by the same defect/word/B interface), checking `rho2` after each insertion.
Every prefix row has ancestry and lies in `M2`, so it is a legal initial `S`.
The dual passes then add counterexample rows to that same monotone `S`.  There
must be one writer and one deterministic discovery order; concurrent mutation
of `S` is forbidden.

An atomic checkpoint consists of a canonical HEAD, canonical body and
content-addressed flat blobs with at least the following fields:

```text
schema/version/generation/previous_checkpoint_sha256
exact producer, workflow and input-parent receipt blocks
all dimensions, coordinate/order tables and map-table digests
rho2 packed/dense hashes and selected resource caps

phase and safe cursor; initial rank r0; current S rank
S packed rows, leads, normalization/reduction stream and ancestry-DAG receipt

connection transducer:
  next offer, lower rank/leads/packed pivots, packed top companions,
  u-recursion stream, dependent count, rolling digest, structural EOF flag

current separator pass:
  pass index, augmented-system transcript, canonical lambda/hash,
  connection-test cursor and current-lambda transcript hash

current character only:
  character, dual rank/leads/normalized packed basis,
  raw representative parent/actor descriptors and hashes,
  FIFO read cursor, next child, current raw representative,
  next defect-pair cursor and rolling pairing digest

completed characters for this same lambda:
  content-addressed compact event-stream receipt containing raw descriptors,
  leads/scales/reductions, pairing ranges and rolling hashes,
  plus rank, offer count, FIFO-EOF and complete-pairing EOF

cumulative and current-run wall/RSS/offer/pairing/transcript/durable meters
terminal = null | MEMBER | NONMEMBER | UNKNOWN_RESOURCE
```

Only a HEAD installed after all body/blob hashes close is resumable; orphaned
blobs are ignored.  Resume reauthenticates immutable parents, code version,
all row leads and transcript prefixes.  A code change requires a versioned,
audited migration rather than silently reading the old checkpoint.

Progress reusable across separator passes is only the presentation/maps,
lower transducer and monotone `S`.  A connection zero test and all dual-orbit
receipts are tied to the exact current `lambda`; they reset after a violation.
Within an interrupted pass their exact cursors are reusable.  Only the current
character's normalized dual basis is retained; completed characters can be
recomputed by the independent terminal checker from compact receipts.  No
primal H2 closure or full `M2` is checkpointed.

On a cap, the workflow uploads the sealed checkpoint under an operational
`UNKNOWN_RESOURCE` marker and does not invoke or upload a mathematical terminal
checker verdict.  On a terminal, it runs the independent checker in a separate
step/job and uploads the certificate only after its exact marker.  Thus a
single workflow definition may be resumed through multiple bounded runs, but
no checkpoint is a negative certificate.

## 7. Luna implementation and release order

### Can be completed before Task640 produces `rho2`

1. In parallel, close Task646 R2/R6/R8 in a versioned Task640 successor and
   obtain a new finite `PASS`; the current quartet remains inert and must not
   run.  This is the witness-input lane, not part of the grade-two owner.
2. Create one versioned, grade-two-specific producer, one nonimporting checker,
   and one inert workflow.  Do not edit Task565 and do not build a generalized
   grade-`e` framework.
3. Implement canonical state/blob and flat coefficient/DAG formats; independently
   ingest the exact Task554 prepare/four-block parents and close every
   presentation structural/replay gate.
4. Translate the precision-two forward arithmetic and v451 preflight into the
   producer; reconstruct it separately in the checker.  Freeze coordinate
   tables and perform complete structural forward/adjoint comparison.
5. Implement and fixture `lift2`, one `defect_slice`, `connection_step`, packed
   echelon/pairing, raw ancestry and canonical separator.  Include mutations
   for coefficient 2, nonmonotone leads, a dependent nonzero connection,
   forward DAG edge, actor-word reversal, sign/prefix, monomial split, map
   transpose and each EOF.
6. Implement the CEGAR state machine, exact checkpoint/resume validation,
   MEMBER literal expansion and NONMEMBER four-orbit checker.  Fixtures use
   tiny dimensions but drive the live validators, not toy dictionaries.
7. Add fixed resource caps, `UNKNOWN_RESOURCE` routing, immutable action/code
   pins, success-only terminal upload and checkpoint-only cap upload.  Run the
   normal static/serial release audit while the workflow remains inert.

### The single result-dependent join after Task640

8. After a repaired Task640 re-audit plus a real run and external artifact audit accept the
   payload, insert its actual run/artifact/manifest/checker identities and the
   exact `rho2` packed/dense hashes into a new immutable launch manifest.
   Reauthenticate both disjoint parents, decode/compare every residual
   coordinate once, and initialize the canonical separator checkpoint.  This
   is the only result-dependent code/data join.  Root may then release the
   workflow without rebuilding or accepting a Task565 module.

Shortest-path release gates are therefore: exact source parents; static audit
of the new pair; bounded fixtures; accepted Task640 receipt; inert-guard
removal at an exact head; one bounded run; independent terminal checker;
external run/artifact audit.  Missing any gate gives `NOT_READY` or
`UNKNOWN_RESOURCE`, never an inferred decision.

## 8. v220 accounting

The current accounting stays

```text
A0 actual:                         0/1
first-rung grades cross-checked:  1/6
```

It moves to `2/6` only after an actual v474 grade-two `MEMBER` certificate
passes the independent checker above and the immutable run/artifact is
externally accepted.  That MEMBER supplies the selected `Delta C_2` and
advances the v479 witness branch; it still does not supply the complete
presentation `P_2`.  An accepted `NONMEMBER` is a valid decision of this
grade-two extension problem, but it kills the selected witness branch.  The
successful first-rung numerator therefore remains `1/6`, and a different
grade-one branch would be needed.  Neither terminal changes
`A0 actual: 0/1` by itself.

Fresh `rho2` is only the question to be decided.  A partial span `S` is only
positive search state unless it already contains `rho2` and the full MEMBER
ancestry/replay gates close; an incomplete dual scan proves no negative.  Even
an accepted grade-two MEMBER leaves grades 3--6, order 54,432, the separate
presentation branch, full-Q0/A0 compatibility and cofinal lifting open.
Consequently no fresh residual, partial closure, or grade-two terminal alone
is a COMMON word, fake witness, or Ihara result.

## Audited theorem/shelf pins and claim boundary

| input | bytes | SHA-256 |
|---|---:|---|
| v474 | 12,755 | `a0ae668799de33d79b5e80ca2a6b7b50224770528b1201d8fb999506757c08c9` |
| Task626 | 6,645 | `b05e8a7e2ec46f49ba8b3399c0d2b876dddfdd5fa8cc1781a472e17828e3430e` |
| v479 | 12,280 | `df6850c9e7c86a83ade26c37064a7deb38ec3c8d7907b1eec6ff0d5268b22986` |
| Task641 | 12,498 | `498df880f86805cffab50756dc32435a2a79a3426071c7bdd290820a6dadddf7` |
| Task642 | 19,930 | `7dacfaabf4aebeb254c30eb71da8dd69e9c9e64be20bab84af235a9bbdc98b24` |
| Task646 | 10,783 | `fe1a6fbec8a3b4518b2e12cae72f3dd46e29d910ed3ad5b5407264bda7183c41` |
| v451 | 8,050 | `3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4` |
| Task565 producer | 145,917 | `acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8` |
| Task565 checker | 80,693 | `fc6f9976b4e3164d4dff31c05256750ddb4758856f39ac5b1fceb43249fbdecf` |

```text
TASK640 RHO2:                         NOT YET ACCEPTED BY THIS AUDIT
GRADE-ONE PRESENTATION SOURCE BYTES:  AVAILABLE; SEMANTIC REPLAY REQUIRED
V474 TARGETED DECISION CONTRACT:      READY FOR LUNA
GRADE-TWO MEMBER/NONMEMBER:           NOT RUN
FIRST RUNG / A0:                      1/6, 0/1 actual
ORDER 54,432 / FULL-Q0 / COFINAL:     NOT DECIDED
COMMON / FAKE / IHARA:                NOT DECLARED
verified:                              false
```

The final reply byte count, LF count and SHA-256 are measured after the file is
sealed and supplied in the task handoff; embedding its own digest would be
self-referential.
