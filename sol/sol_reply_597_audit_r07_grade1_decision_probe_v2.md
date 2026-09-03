# Task 597 independent audit — grade-one decision-first probe v2

## Verdict

`PASS_AFTER_REPAIR`

The production merge path is mathematically exact.  It routes the frozen
2,014 old-basis rows and 6,045 block-basis rows in the v3 order, avoids the
known second lower reduction, and tests exactly whether the registered
grade-one residual belongs to the resulting lower-zero grade span.  I found
no production path which can emit a false MEMBER or false NONMEMBER.

The completed candidate from run `33707397894`, attempt `1`, job
`100499387350`, commit
`93f746ad1b649796e1bc28e00ff34993498929ee` is internally consistent with
that audited path and may be retained as **candidate** MEMBER evidence.

Two small pre-existing protocol/fixture defects must nevertheless be
repaired: the MEMBER fixture does not bind the target it actually reduced and
the fixture checker does not authenticate the pristine decision artifacts;
and the producer has no explicit pre-seal marker.  These defects do not alter
the completed production calculation or require discarding its immutable
artifact, but they prevent an unqualified `PASS` for the commissioned v2
package.

`verified=false`.  The production result is not yet `cross-checked`; no Lean
certificate or independent full routing replay was performed here.

## 1. Frozen routing and the lower-first factorization

The two merge loops are extensionally the v3 loops.

- `validate_prepare_state` fixes four old blocks in character order, and the
  explicit rank gate fixes their pivot counts as `[505,503,503,503]`, whose
  sum is 2,014.  V2 traverses each block and then each insertion-ordered pivot
  exactly as v3 does.
- For each old row it constructs the same occurrence lower/grade pair and
  calls the same `aggregate_pair`.  It reduces the physical lower row once,
  applies the returned coefficients to the grade companion, and either
  accepts the already-reduced lower remainder or offers the lower-dependent
  companion to the grade owner.
- The four sealed block ranks are fixed as `[1509,1512,1512,1512]`, whose sum
  is 6,045.  V2 loads block owners `0,1,2,3` and offers their pivots in the
  same insertion order through the same `aggregate_pure_grade` call as v3.
- The intermediate assertion at 2,014 and terminal assertion at 8,059 prevent
  truncation, duplication, or an unnoticed extra row.  The body records the
  actual owner offer counts and ranks.

Thus the only intentional change from v3 is removal of its lines 1784/1790
duplicate lower reduction: V2 performs `reduce_packed` once and then only the
acceptance tail.  `lower_grade` remains indexed by lower pivot id, so all
later companion reductions use the same coefficients and rows as v3.

## 2. `accept_already_reduced`

The helper is textually and extensionally the acceptance tail of frozen v3
`PackedEchelon.insert`:

1. it chooses the first nonzero packed byte and the first nonzero trit in that
   byte;
2. reads the leading coefficient, normalizes coefficient 2 by packed scale
   2, and copies the normalized row;
3. appends insertion-ordered `rows` and `leads` while inserting `(lead,pivot)`
   into the lead-ordered lists and map; and
4. returns the original reduction list unchanged, including on a dependent
   row.

In addition to the commissioned fixture, I ran a bounded, in-memory comparison
against `PackedEchelon.insert` on 10,000 deterministic cases of widths
4--32.  It included 898 newly accepted coefficient-2 pivots, 8,200 dependent
rows, and 2,953 states reached after a non-monotone lead insertion.  Return
records, packed matrix bytes, insertion leads, ordered pivots, ordered keys,
lead maps, and reduction ancestry agreed in every case.

## 3. Exact decision predicate and failure paths

The lower-first construction is block elimination on paired rows.  A row with
nonzero lower remainder becomes a lower pivot together with its reduced grade
companion.  A row whose lower remainder is zero contributes its reduced grade
companion to the grade owner.  Consequently the grade owner spans precisely
the grade components of the registered routed span having lower component
zero.  The registered residual has lower component zero, so

\[
  \rho\in \operatorname{span}(\text{all routed paired rows})
  \quad\Longleftrightarrow\quad
  \operatorname{rem}_{E}(\rho)=0.
\]

V2 reads and authenticates the registered packed residual, reduces it once by
the completed grade owner, and derives `member` only from the exact packed
zero test.  The terminal string is selected from that Boolean.  It performs
no dual, ancestry expansion, presentation construction, or later replay which
could change the Boolean.

Input and polled resource errors return nonzero and do not seal a decision.
An uncaught `MemoryError`, I/O error, hard timeout, or signal also fails the
workflow step; `pipefail` plus success-only staging/upload prevents a partial
local state from becoming a candidate artifact.  HEAD is written last and an
existing HEAD is rejected.  Accordingly these less descriptive hard-failure
paths are fail-closed, not false NONMEMBER paths.  Catching every operating
system failure is not a load-bearing repair.

## 4. Required minimal repairs

### R1 — bind and actually authenticate both fixture targets

The MEMBER fixture reduces the nonzero target `[1,1,0,0,0,0,0,0]` and gets
coefficients `[[0,1],[1,1]]`, but its body sets both `residual_receipt` and
`remainder_receipt` to the all-zero remainder blob and hashes the remainder as
the residual.  Therefore the body does not bind the target exercised by the
fixture; relative to its recorded zero residual, its nonempty coefficient
list is wrong.

The checker also parses pristine HEAD/body bytes without checking the body
hash or canonical HEAD/body encoding.  It never checks pristine blob hashes,
and it does not authenticate the NONMEMBER body or its blobs.  Its five
"mutation rejections" are direct inequality/existence observations rather
than calls to an artifact validator, so a pre-corrupted but still parseable
fixture can pass.

Minimal repair:

1. In `fixture`, write the packed `target` as a fixture-only residual blob,
   put that receipt in `residual_receipt`, and hash `target.tobytes()` for the
   dense residual hash.  Keep the independently written remainder receipt.
2. In the fixture checker, use one small loader for both MEMBER and NONMEMBER
   outputs which checks canonical HEAD/body bytes, HEAD-to-body SHA, exact
   receipt shape/name/length/SHA, and then independently decodes the basis,
   recorded residual, and remainder.  It must reduce the recorded residual,
   compare the actual remainder and terminal, and on MEMBER compare the exact
   coefficient list/reconstruction.
3. Make each corruption test invoke that loader and require rejection.  The
   extra target blob is fixture-only; the production candidate remains the
   specified four files.

### R2 — add the missing pre-seal marker

Production and fixture logs have
`TARGET_REDUCTION_END` followed by `DECISION_SEAL_DONE`, but no
`DECISION_SEAL_BEGIN`.  V463 explicitly requires flushed markers immediately
before and after the seal.  Emit `DECISION_SEAL_BEGIN` after target reduction
and before the first decision blob/body write, in both modes, and make the
checker demand the strict marker order.  No checkpoint or arithmetic change
is needed.

### Hash consequence

After R1/R2, recompute the v2 producer/checker hashes in the workflow gate and
record final bytes/SHA values.  Do not change frozen v3.  The current
commissioned workflow byte image has SHA-256
`5045b4ca2b1fa7522cf127c4ab6b4de1d614958983adc5c16be0b12c14a9ddd4`,
not the `81eb842c...` value reported in Luna reply 595.  The latter is a stale
receipt and must not be cited as the current workflow hash.  Since the source
repairs change the gated hashes anyway, one final receipt refresh is enough.

## 5. Completed candidate consistency check

I inspected the downloaded four-file artifact read-only.  Its receipts are:

| file | bytes | SHA-256 |
|---|---:|---|
| `decision-v2.HEAD` | 162 | `07de7a817e8c5ae2e7346402a290c32631d05b0cc621d03702faa6cb43a948c0` |
| decision body | 56,666 | `62412762b3a208d31febb6c6b8d4707f880471ed32cf62c79c18108065ab7b5d` |
| grade basis | 30,506,112 | `b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d` |
| remainder | 6,048 | `564cbfafc869a8c6eb761a392caa5e792b546bf577af7fe808177b2fdf13cbb0` |

HEAD, body, and both included blob receipts authenticate exactly.  The body
fields satisfy all routing identities:

\[
\begin{aligned}
505+503+503+503 &= 2014,\\
1509+1512+1512+1512 &= 6045,\\
2014+6045 &= 8059,\\
8059-1661 &= 6398\quad\text{grade offers},\\
5044\cdot 6048 &= 30,506,112\quad\text{basis bytes}.
\end{aligned}
\]

The 5,044 listed leads are distinct, in range, and equal the actual first
nonzero coordinate of their respective packed basis rows; every pivot is
normalized to coefficient 1.  All 3,317 member-coefficient entries have a
distinct valid pivot id and coefficient 1 or 2.  The remainder blob is exactly
6,048 zero bytes, consistent with support 0 and the MEMBER terminal.

I also used a standalone base-3 packed addition/reduction table, without
importing v2 or v3 helpers, for an artifact-level algebra check.  Summing the
5,044-row candidate basis at the 3,317 recorded coefficients reconstructs

- packed residual SHA-256
  `648696895595f479b6e2ccb65332589cf8a1a3bf4cf3f92be37e7910f72b79e6`,
  exactly the residual receipt hash; and
- dense residual SHA-256
  `5503afc98809a92f5734e8b1ac198b60eef33d9c4751658c79ad6c3927884134`,
  exactly the body's dense residual hash.

Independently reducing that reconstructed residual by the candidate basis
returns zero and reproduces the exact 3,317-pair coefficient list.  This rules
out an internally false MEMBER seal relative to the supplied basis and bound
residual.

The route log is also consistent with the old v3 prefix: lower rank is 1,661,
grade rank reaches 5,044 at logical row 7,168 and remains 5,044 through 7,936
and 8,059.  Thus the formerly unlogged last 123 positions add no grade pivot.
The 347.872-second total is consistent with the measured roughly-six-minute
v3 route and shows that no dual/ancestry/post-decision stall was entered.

This check is deliberately not called a full independent replay: the supplied
basis itself was built by the audited producer.

## 6. Hot path and workflow

The production hot path retains frozen v3's NumPy packed pivot search and
packed AXPY.  It has no Python bytewise pivot scan, closure queue, new
ancestry/DAG, physical roster, transition presentation, dual, or literal
replay.  The per-old-row dense remainder zero check, dense grade companion,
block `dense_row`, authenticated source-blob passes, and one terminal
`matrix_bytes` stack are all bounded operations already present on the
measured v3 route; none plausibly changes it into a long terminal run.  I do
not require optional rewrites of those operations.

The workflow otherwise passes the commissioned gates:

- current producer/checker/v3 hashes equal its three environment pins, and
  authentication precedes large downloads;
- exact source run `33677346616`, attempt `1`, the named prepare artifact, and
  the four attempt-qualified block artifacts are selected;
- checkout is the event SHA, Python is 3.13, NumPy is pinned to 2.5.1, actions
  are commit-pinned, and permissions are read-only;
- internal time is 2,400 seconds, outer command timeout is 45 minutes, job
  timeout is 60 minutes, internal RSS is 7 GiB, and virtual-memory ulimit is
  8 GiB;
- the four decision files are staged/uploaded only on success, while existing
  logs are uploaded under `always()`.

The successful run and its immutable artifact satisfy these operational
bounds.  R1/R2 and the stale workflow receipt are the only required package
repairs; no production arithmetic or timeout enlargement is warranted.

## 7. Minimal replay required for `cross-checked`

The remaining load-bearing gap is provenance of the candidate basis from the
registered 8,059 rows.  The smallest genuinely independent result replay is:

1. Independently authenticate the exact prepare and four block HEAD/body/blob
   chain named above and require the candidate's prepare/block digests and
   four rank vectors.  Do not import the v2/v3 validators.
2. With independently implemented base-3 packing, physical aggregation, and
   echelon logic (no v2/v3 arithmetic or aggregation helper sharing), route
   exactly the 2,014 old rows lower-first and then the 6,045 block pivots in
   the registered order.
3. Obtain lower rank 1,661, grade-offer count 6,398, and grade rank 5,044.
   Prefer exact comparison of the deterministic basis bytes/leads to
   `b562c980...`; if the checker deliberately uses a different echelon normal
   form, prove equality of the two spans by equal rank and mutual reduction.
4. Load the authenticated registered residual and independently reduce it by
   that independently routed span.  It must be zero.  Comparing the 3,317
   coefficient reconstruction and the two residual hashes above is a final
   inexpensive consistency gate.

There is no need to regenerate the four source closures, construct a dual,
build ancestry, replay literal words, or enter degree two for this finite
decision.  Agreement of that replay promotes only
"registered grade-one residual is MEMBER of the registered routed span" to
`cross-checked`; it does not make an A0/common/cofinal/Ihara declaration and
does not make the result `verified`.

## 8. Audited input receipts

| input | bytes | SHA-256 |
|---|---:|---|
| task 597 | 2,516 | `3e4c0c471e3e98f20765b7b3bb1f787cf799965a23b2ca0c64a37a855c72b67f` |
| v463 factorization | 5,104 | `13afd22ca19776c160376e70f95669ea3c8dee7d84c07b0f57677c1c11074bc3` |
| task 593 audit | 8,340 | `defa5878d60487661f8906388d430f1d763c296b117693b2f8fd229976ecc476` |
| frozen v3 producer | 138,202 | `bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff` |
| v2 producer | 12,106 | `5a445cf9a263c1968c004f04227d9f5bd5349e433f4dfd8776af80b1d53d9748` |
| v2 fixture checker | 4,447 | `8d757763ff8ebd7787fef513c732a81411fdac43fb672787b028f8caedbd4696` |
| recovery workflow | 6,841 | `5045b4ca2b1fa7522cf127c4ab6b4de1d614958983adc5c16be0b12c14a9ddd4` |
| Luna task 595 | 3,918 | `97ca5979cc30f465d280c3ea8c9833f0a996abc360ac5781cc1f5c9c2346c206` |
| Luna reply 595 | 2,643 | `088382c06d103ce4e67de173b917b56b8ee5e6f5b07c5695d75aac0d8ce71a2c` |

No production command, git/GHA operation, implementation edit, workflow edit,
proof edit, certificate edit, or v220 edit was performed by this audit.

PASS_AFTER_REPAIR
