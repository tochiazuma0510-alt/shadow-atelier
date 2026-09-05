# Task927 reply -- corrected actual seed30 materialization intake

## Outcome

The smallest executable path is a seed30-only producer/checker over fixed
parents.  It should publish a **parent-plus-one-pivot delta**, not rebuild Conn,
not replay the old 8,059-offer construction, and not copy the accepted 107 MB
Task904 state.  The saved Task904 target remainder lets the new `rho2`
reduction be exactly one additional elimination step.

This is an implementation intake only.  No materialization was run here;
`verified=false`, all named A0/COMMON/COFINAL/FAKE/IHARA claims remain
undeclared, and Grade2 remains undecided.

## Exact seed30 extraction and readers

Use global old offsets `(0,505,1008,1511)`, new offsets
`(2014,3523,5035,6547)`, and source origin ranges
`((0,2064),(2064,4120),(4120,6176),(6176,8232))`.

`complete_seedred30()` must append raw ancestry events in this exact order:

1. for source `c=0..3`, read
   `prepare.body.old_blocks[c].record.seed_reductions[30]`, adding the old
   offset for `c`;
2. for target `t=0..3`, then source `c=0..3`, read
   `block[t].body.origin_reductions[ORIGIN_RANGES[c][0]+30]`, adding new
   offset `new_offsets[t]`.

Thus the four new-body origin IDs are `30,2094,4150,6206`.  Preserve body
digest, role, source/target, origin, term ordinal, local index, global index,
and coefficient on every raw event.  Only after this ordered list is sealed
may equal global indices be combined modulo 3 and zero coefficients removed.
The resulting fixed seed30 support is 902; assert this as an actual-input
gate, not as a generic algorithmic constant.

Reuse the Task922 body/descriptor validation contract (`_state_descriptor`,
`_validate_task554_body`) but copy the small reader logic into each independent
source rather than importing the producer.  Positioned reads are sufficient:

- old row: `lower_basis_blob` width 6,056 (owner `d0` slice plus aux) and
  `lifted_grade_blob` width 72,576 (the four `d1` slices);
- new row: `basis_blob` width 18,144 in its target `d1` slice;
- top row: the already-local canonical P1 cache row, width 145,152, split into
  four 36,288 character slices (`PackedCache.row`/`LazyP1.row` layout from the
  accepted v9 source).

Read only the 902 final nonzero rows after authenticating each containing
blob/cache receipt.  Accumulate the complete raw seed evaluation minus these
full lifts and require all 96,776 `d0+d1+aux` trits to be zero.  Then take the
plain character-0 `d2` slice and apply exactly `Task712.B_fwd_a0` once.  There
is no actor loop.  Retain the v518 fixed four-projector order only in the
literal word ancestry: compact seed30 minus the selected canonical P1 word
roots, followed by the full character-0 projector.

## Fixed authority joins (closing Task880 F1/F3/F4)

**Scalar parent.** Require corrected root run `33941591417/1`, head
`2caaf1f33b6f36f8aa754f759ef0e5dccfaf5a74`, source commit
`a68460cf0c1bdae9fde5d3a4fa6501d625d68388`, final artifact `9962060495`
(253,544 archive bytes, digest
`sha256:1091f9946108ef6bf122143da58d32006eba54166ee995996efa177aa89a2ed2`).
Join canonical manifest/result/terminal/character-a0/checker result to the
diagnostic `launch.json` hash
`16adebd65d741efd473017f7a75e4ba394ae2d0cc57733d721baba6ddcf9828a`
and `receipts/source-receipt.json`; require RootViolation char0, seed30,
scalar1, origin30/prefix31, empty actor word, and violation seal
`cba44225c60f14e6203ea51a053f75a56b17e6cc33f146a9262609ac43c1c0f5`.
Also require the saved scalar vector has seed2=0 and seed30=1, without
broadening materialization to the other nonzero seeds.

The one missing immutable input in the task text is the **diagnostics artifact
ID/archive byte count/archive digest**.  Its fixed name is
`d972-r07-actual-root-scalar-batch-v2-diagnostics-33941591417-1`; root must pin
that tuple (or republish the launch/source receipts in a fixed parent) before
the workflow is authoritative.  Local presence alone is not an archive join.

**Task554/P1/Task712.** Stage the exact prepare plus four block parents already
named in Task920 and require their body digests and all selected blob
descriptors to match both the scalar launch and source receipt.  Require the
canonical P1 manifest SHA
`86e8b14cb0a60c86468ffb54a7bf14980366406a1e5bea17018fc6961f331feb`
and its instruction/cache identities, and the exact Task712 table identity
including `B_fwd_a0` SHA
`763affaa7be5dea7a1d432fa5cf43e65177abb1b9fb4935dc4b2e5c37cb5fd67`.
This supplies actual raw rows and ancestry, so no fixture lower provider is
accepted (F1/F3).

**Current S.** Require the accepted Task904 artifact: run `33891714539/1`,
head `7b7b9de20faaa3b8f26e331bb738b374f6f5708c`, artifact `9944214057`, name
`d972-r07-grade2-physical-state-separator-v2-candidate-33891714539-1`,
107,195,261 archive bytes, digest
`sha256:2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017`.
Require state generation/cursor 8059, rank1354, head
`69fdcc8cd740f8ea11bd198aaf44bcf50d1c4980331f51aa7f792544b00f9d88`,
manifest SHA
`d11d551c2b1a127bd900c013cbc684eef698372660ff733b10f82bb4793f227b`,
physical SHA
`1246ae0c23c7dcbfc2a1c2f73075f38968a4ab7b2e5c8fc006f0f8aafae2d57e`,
companion SHA
`a2d462ea6c8685a59e28f3f5d1c89656e2e942a65110a21184e33c6cb334826c`,
instruction SHA
`a7cbe317ba92b0d4076623dfd5ea672d2ef4b154f5be2862e0dc232ba91309c2`,
and accepted checker PASS.  Parse/hash its instruction stream once per
independent program to obtain insertion-order pivot metadata; do not rebuild
the 46-minute Conn history.  The accepted checker is the authority for the
old normalized rows/earlier-zero equations and old lambda(S)=0 (F4).

The rho2 parent remains Task640 run `33839962829/1`, head
`17a8439c766d92719d7ae7d35846ea444da598fa`, artifact `9925190479`, name
`task640-fresh-rho2-v17-33839962829-1`, 6,049,643 archive bytes, digest
`sha256:01722bfda081e577195aa6ca9c0bba3425a50dcfd829eca6ac23e33cb5d79ca4`.
Reuse the separator-v2 stager/target-manifest loader; do not reconstruct rho2.

## One-pivot append and next target result

Reuse the insertion-order kernel of separator-v2 `_physical_reduce`, with no
numeric lead monotonicity test.  Starting from `G`, eliminate against the
1,354 stored pivots, recording each positioned row receipt and scalar.  Check
every old lead is zero afterward, require a nonzero remainder, set `lead` to
its first nonzero coordinate, normalize by its inverse, and independently
check `<q,d>=1`, `<lambda,G>=1`, earlier-pivot zeros, raw-versus-normalized
hashes, scale, and rank `1354 -> 1355`.  Seal a single new instruction using
the existing `_record_state_instruction` rolling-head rule.  Its ancestry is
the raw seed/P1/projector descriptor followed by the authenticated old-pivot
reductions; do not collapse it into a six-tag/full-A0 claim.

Use Task904's already authenticated target reduction (884 reductions), whose
saved remainder SHA is
`e0053fc6e745e4459e0324d26320bf9f5e434a2942fa4a519ebaf9e28df50011`.
Let `N` be the new normalized pivot and `s` the trit of that remainder at the
new lead.  The exact new-state reduction is the single step
`R_new = R_old - s*N`; append this reduction record.  If nonzero, run the
existing `_separator` reverse substitution over the 1,354 parent rows plus N
to publish the next separator.  If zero, publish only a ConnectionMember
**candidate** with the old 884 reductions plus the new literal descriptor.
This reads the small saved remainder and, for a separator, the 16 MB physical
store once; it never repeats the old target elimination or Conn construction.

The delta publication should contain parent artifact/manifest/head receipts,
the one raw and normalized pivot, its reduction and literal-ancestry records,
the updated target reduction, and next separator/member-candidate payload.
The parent remains immutable and is not copied into the candidate.

## Minimal source/workflow set and CLI

Create only:

- `search/d972_r07_actual_seed30_materializer_v1.py`;
- `search/check_d972_r07_actual_seed30_materializer_v1.py` (independent
  arithmetic/JSON checks; no producer import or execution edge);
- `.github/workflows/d972-r07-actual-seed30-materializer-v1.yml`.

Both programs can use the same narrow path interface:
`--scalar-root`, `--scalar-diagnostics-root`, `--prepare-root`, four ordered
`--block-root`, `--p1-root`, `--task712-root`, `--state-root`, `--rho2-root`,
and `--output-root` (checker also receives `--candidate-root`).  Keep exact
artifact tuples/source hashes compiled into the new version and make the
workflow stage those fixed artifacts serially.  Producer, checker, then final
upload are serial; selftests should be bounded synthetic raw-order,
nonmonotone-lead, raw/normalized, and parent-mutation canaries only.

The sole interface decision needed before coding is authorization of the
parent-plus-one-pivot delta ABI versus a monolithic copied state.  The delta
ABI is sufficient for the requested next separator/member candidate and is
the materially smaller implementation.
