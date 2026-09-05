# Task929 -- seed30-only producer resumed and statically completed

## F1. Handoff and claim boundary

The saved 49,632-byte producer was unfinished after its state-parent reader.
Its raw-seed/Task554/P1 implementation was retained and the missing one-pivot
reduction, target update, delta publication, synthetic tests and CLI were
completed in `search/d972_r07_actual_seed30_materializer_v1.py`.

This is a source/static handoff, **not an executed materialization**. No local
Python/GAP, network, credentials, git, dispatch, nested agent or `codex exec`
was used. No new run ID or commit SHA exists from this worker. Root remains
the sole git/GHA broker; actual producer/checker execution is still required.
The previously accepted scalar authority is run33941591417/1 at head
`2caaf1f33b6f36f8aa754f759ef0e5dccfaf5a74`, source commit
`a68460cf0c1bdae9fde5d3a4fa6501d625d68388`.

```text
producer bytes: 79651
producer SHA256: 3ce9293e05f06bf343bd2a54af0ab84ae67f4b922a428cd3c73e38944d6de55c
LF: 1563; CR: 0; BOM: absent; final LF: present
actual materialization: NOT RUN
actual rank1354 -> rank1355: NOT YET ESTABLISHED
GRADE2_MEMBER/GRADE2_NONMEMBER: NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA: NOT_DECLARED
verified=false; cross_checked=false
```

The SHA/size/line-ending facts above were obtained by read-only PowerShell
file inspection, including `Get-FileHash -Algorithm SHA256`; they are not
Python syntax or runtime test results.

## F2. Concrete completion and saved-reader repairs

The fixed path is raw `Eval(seed30)` minus the complete global SeedRed30 full
P1 lifts, all 96,776 lower coordinates zero, complete-defect filtered
character-0 projection equal to its plain top slice, and one Task712 B call.
The producer also reconstructs B-adjoint(lambda) and requires it to equal the
fixed raw q, with both pairings equal to one. Actual selected arithmetic
support must be 902. There is no actor path or seed/orbit batch.

Ordered raw coefficient events are sealed before F3 collection. All raw-event
P1 roots, including numerically cancelled nodes, are retained for literal
ancestry. The descriptor explicitly joins `raw_events.global_index` to
`p1_roots.node`; only the final 902 rows are used for lift subtraction. The
fixed four-projector word order and coefficient-two-as-inverse convention
remain explicit.

Root identified a saved P1-reader defect: accepted v9 `make_instruction`
stores local reduction indices and `reduction_digests` uses `base+index`.
The reader now uses the fixed old/new block base, checks prior local bounds
without sorting away stored order, and authenticates the corresponding global
row receipt. Nullable `literal_input_sha256` is accepted as allowed by that
serializer. No old P1 arithmetic construction is rerun.

The actual scalar checker-result file is space-separated JSON, not the new
producer's compact canonical encoding. Its exact byte/SHA pin is retained,
but the erroneous extra canonical-format rejection was removed. Other
canonical scalar objects and their seals remain checked. Progress is sent
to stderr so stdout is one machine-readable result JSON.

The accepted Task904 instruction stream is now hashed and parsed in one
pass, retaining only insertion-order positioned pivot roots. Its fixed
physical and companion bytes, manifest/HEAD and accepted checker/target
receipts are authenticated. The 8,059-offer/610,996-reduction derivation is
an explicitly retained premise, not recomputed or copied.

The new raw physical row is reduced against all old pivots in insertion
order, not numerical lead order. A nonzero remainder, unique new lead,
earlier-pivot zeros, raw/remainder pairing one, normalizing scale and scaled
normalized pairing are all mandatory before emitting rank1355. One new
instruction uses the accepted rolling-head rule. Its normalized literal DAG
names old instruction roots, reductions and inverse/scale operations rather
than inventing a new P1 companion vector.

The Task904 saved target remainder is decoded from its authenticated hex,
not reconstructed from its hash or reduced through old S again. Exactly one
new pivot is examined; the update is `Rold - scalar*N` (zero elimination when
that scalar is zero). A nonzero remainder receives reverse-substitution
separator ancestry. Zero gives only `ConnectionMemberCandidate`; exponent,
eleven-slot and full-A0 replay remain explicitly unperformed in either branch.

## F3. Frozen output ABI coordinated with Task930

Output is a fresh flat parent-plus-one-pivot delta directory containing:

- `source-d.bin`: 36,288 trits, 9,072 packed bytes;
- `physical-raw.bin`, `physical-remainder.bin`,
  `physical-normalized.bin`, `target-remainder.bin`: each 48,384 trits,
  12,096 packed bytes;
- `lambda.bin`: the same physical width, only for a Separator;
- `instruction.json`: the single rolling-head append, with separate parent
  logical offset and delta offset zero;
- `result.json`: sealed parents, raw seed/subtraction/ancestry,
  raw-materialization, pivot, target update and separator/member-candidate;
- `manifest.json`: sealed exact file roster and byte/SHA receipts.

The old physical state and 884-step target history are references only, never
copied. `result.literal_replay` distinguishes the formal graded word DAG
from unperformed normalized-exponent and eleven-slot replay. Producer and
checker may reuse their distinct accepted source lineages; neither new
program imports the other's arithmetic. Task930 owns the checker/workflow
and received the exact source freeze above.

## F4. CLI and remaining execution

The workflow's path interface is implemented unchanged:

```text
python -B -u search/d972_r07_actual_seed30_materializer_v1.py --selftest

python -B -u search/d972_r07_actual_seed30_materializer_v1.py \
  --scalar-root SCALAR_FINAL --scalar-diagnostics-root SCALAR_DIAGNOSTICS \
  --prepare-root PREPARE \
  --block-root B0 --block-root B1 --block-root B2 --block-root B3 \
  --p1-root P1 --task712-root TASK712 --state-root TASK904 \
  --rho2-root STAGED_TASK640 --output-root FRESH_OUTPUT
```

`--rho2-root` is the accepted flat stager output, not the original archive.
The output directory must not exist and must be disjoint from every parent.
Successful stdout is a single JSON with status PASS, kind, rank transition,
manifest SHA and false verification flags; failed gates return REJECTED and
exit one. Required phase/count progress is on stderr.

Ten bounded synthetic canaries are implemented but **not executed here**:
packing/rejection, nonmonotone insertion, raw/normalized distinction, one
target step, next separator, member-candidate boundary, zero-pivot rejection,
ordered raw cancellation, parent mutation, and the local-base/nullable P1
metadata regression. They load no historical parents. GHA must run these,
the actual producer, and the independent checker serially before publishing
the final candidate. No additional historical audit or orbit enumeration is
a prerequisite of this handoff.

Only the authorized producer and this Task929 reply were edited by this
worker; checker/workflow changes belong to Task930. Repository-wide status
and final commit/run receipts are for root's broker audit.
