# Task949 -- static fixed44 packet and complete-prefix source audit

Author: packet_bounds_audit / 2026-09-05

Verdict: PASS for the source scope below. The diagnostic-tail ABI defect
found during review is repaired. No remaining necessary source/math fix
was found. This is static review only: no Python/GAP, syntax process,
canary, numerical replay, network, credentials, git, or further agent was
run by this auditor. Root separately owns workflow/source-pin closure,
launch and release. No actual packet, rank increase or external grade is
claimed here. `cross_checked=false; verified=false`.

## F1. Exact read scope and source identities

Read Task949 FULL, Task947 FULL and reply948 FULL. Read both complete new
modules while their tails were being completed, then read the completed
append/resume/terminal/CLI and diagnostic/deadline changes, including the
final producer packet-boundary guards and both sides' raw-data pins and
source.json.data additions. Read the relevant
accepted v3 helper implementations for ordered relation collection,
packing/F3 operations, P1 instructions, old-state authentication, physical
reduction/normalization, target update and final separator. Read the v2
P1/Task554 descriptor validators to check that the advertised arithmetic
passes do not hide a second full cache/blob authentication pass.

Read-only Get-FileHash/Get-Item metadata matches the workers' provisional
source freezes:

| File | Bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_fixed_root_packet_loop_v1.py` | 70509 | `65169d7a26b6daf29152d5afa1352387766ac4024b078caf82a295ca57fbc3fd` |
| `search/check_d972_r07_fixed_root_packet_loop_v1.py` | 56545 | `c6a4202180342471d6e8938c0ca50c88d0fcd11bf5d2a8f9d100b83e993dfb3f` |

P/C line references below denote these two files. The workflow and workers'
unfinished final report metadata are outside this source verdict. No broad
historical numerical audit or new source-construction prerequisite was
introduced.

## F2. PASS -- all44 COMPLETE source differences, with literal order

P:364/C:223 collect every old-source seed expression, followed by every
target/source new-block expression, with the accepted global offsets and
origin IDs. The checker uses its own accepted combined_selected arithmetic.
Raw events are retained and sealed before mod3 coefficient collection;
referenced P1 roots come from ALL events, including numerically cancelled
terms. Their fixed event order and per-term coefficient survive in the
shared packet ancestry.

P:429/C:336 evaluate every registered raw seed once, retaining all four
characters. The raw char0 seed2 SHA/support is checked, with no future-lambda
scalar assertion. P:460/C:249 stream all8059 P1 instruction/cache rows in
chronological order, authenticate the complete stream hashes/ancestry and
subtract the coefficients into the44 top accumulators. Only one decoded
row and bounded per-seed scratch are used; no full-lift matrix is created.

P:513/C:293 read the12 lower blobs once. Old lower rows contribute their
owner d0 block AND the shared eight auxiliary slots; old grade companions
contribute all four d1 blocks; new rows contribute the indicated d1 block.
The full lower coordinate count is

```text
4*6048 + 4*18144 + 8 = 96776.
```

P:576/C:336 require every one of these coordinates to vanish for every
seed before applying v453's direct-slice interpretation. They then compare
the char0 seed30/34 source-d bytes with the saved actual payloads. The
packet is exactly the fixed4-by44 root list from reply948 F1, not an actor
or orbit closure. Its1596672 packed top bytes and complete ancillary bytes
are independently reconstructed by C:475/545, not accepted merely because
the producer resealed a manifest.

## F3. PASS -- authenticated rank1356 start and current-lambda scope

P:199/297 and C:136 authenticate the immutable1354 base plus the two
accepted saved deltas, their parent/head/target joins, ordered pivot
positions and exact current remainder/lambda pins. The base offers, Conn
and historical target solve are not regenerated. The saved delta source
payloads enter the packet regression above.

Both sides directly pair the FINAL starting lambda with all1356 physical
rows and both immediately available target remainders. P:334/C:456 bind
the packet owner to the fixed P1, Task554, Task712 and word dictionaries.
P:699/C:590 derive four current B-adjoints, select the first nonzero in
character-major/seed order, and separate176 declared pairs from nonzero
root blocks and informative pairings. The producer skips trivial dots only
when that freshly computed root is zero. No historical active-character or
seed35/36 scalar is reused as current authority.

## F4. PASS -- nonzero scalar to one actual pivot and correct target sign

P:787/C:623 map only the selected packet row through the accepted B and
check the fresh scalar equality q(d)=lambda(Bd). Physical reduction uses
the complete insertion order, never sorted lead order or a first-free
coordinate shortcut. Its remainder retains the nonzero lambda value;
normalization chooses a fresh lead and multiplies by its inverse in F3.
This proves one rank rise, not merely a scalar violation.

The updated target is exactly

```text
r_new = r_parent - r_parent[lead] * normalized_row.
```

Earlier pivot coordinates remain zero. P:742 and the checker-side accepted
next_separator build the new lambda by reverse insertion order, then
directly sweep ALL saved/new physical rows and both target remainders.
Their records use the current generation rather than the old materializer's
fixed generation. C independently reconstructs and compares each complete
step's raw/reduced/normalized physical bytes, target/lambda bytes, ordered
reduction instructions, result and manifest.

Literal references retain the seed, ordered P1 events, common P1-root
index, character projector, B identity and normalization/reduction data.
Full normalized-exponent and eleven-slot replay remain explicitly pending;
the code does not promote a zero graded remainder to a full-word witness.

## F5. PASS -- M3-1 is explicitly DERIVED

P:731/C:445 name the base/seed30/seed34 target-derivation receipts, the
original rho2 digest, the subtraction conventions and the number of new
target steps. They emit mode=derived and
original_rho2_directly_read=false. The mathematical implication is exactly

```text
rho2-r_n in S_n, lambda_n(S_n)=0, lambda_n(r_n)=1
    ==> lambda_n(rho2)=1.
```

The first relation is inherited for the named accepted base/deltas and
extended by the newly executed target steps; the other two are direct
final-lambda checks. This does not inherit a former lambda's dot product
as if lambda had not changed. No original-rho2 restage is needed for this
declared DERIVED scope.

## F6. PASS -- durable completed prefix and actual same-owner resume

P:144/163 seal/fsync the complete packet and whole step directory before
publication. P:985 advances HEAD only after append_step has published its
complete directory. A crash before that HEAD update leaves an uncommitted
tail. A resumed run authenticates owner/source/runtime/start, packet hash
and the complete numbered manifest chain; it loads the saved packet and
new rows/targets/lambdas without replaying completed physical insertions.
P:869 checks the final loaded lambda against all rows before new root work.

The producer's metadata loading is not an independent arithmetic acceptance
of a candidate prefix. C:694 reconstructs the packet and replays every
HEAD-committed new step from the retained start before accepting it. This
preserves Task947's distinction between durable candidate and accepted
prefix. The large base is referenced, not copied into new snapshots.

The defect found during review was that the first checker tail-roster loop
rejected the producer's pending/orphan directories. It is closed at the
hash above. C:554/694 now recognize only named step `.pending-*`/`.orphan-*`
diagnostics and named root `.packet-pending-*`/atomic `.NAME.pending-*`
diagnostics, with kind/no-symlink checks. The named resource-stop.json and
its atomic temporary are also diagnostics. Numbered directories beyond HEAD
are also uncommitted. These entries never supply arithmetic rows. Every
committed packet/step directory still has an exact manifest roster. No
cleanup or broader checkpoint framework was required.

## F7. PASS -- honest terminal and resource boundaries

P:970/985 run a fresh root test after the last allowed append. A nonzero
root at a cap gives UNKNOWN_CAP, and a resource stop with a nonzero root
gives UNKNOWN_RESOURCE. ROOT_SEEDS_ZERO requires the current list's actual
all-zero result. It proves neither packet containment in the state nor
full-image nonmembership. A zero target ends at MEMBER_CANDIDATE, with the
full-word gates explicitly unfinished. C:570/694 independently reproduces
the terminal scan/zero target before accepting the corresponding label.

During initial construction the producer now checks its deadline/signal
at dependency/start/table/context and existing body/seed/P1/lower progress
boundaries. An early ResourceStop emits UNKNOWN_RESOURCE, exit3,
candidate=false and, if the output directory exists, a resource-stop.json
diagnostic. It leaves completed packet/prefix data intact. Once the packet
is available, the ordinary loop stops at complete step boundaries after
the fresh scan. The checker checks its deadline between bounded phases
and emits status UNKNOWN, exit2 and candidate_accepted=false on ResourceStop,
preserving the producer prefix. These are cooperative resource limits,
not a guaranteed exact wall-clock cutoff. No cap, interruption or checker
timeout becomes a mathematical negative result.

## F8. Remaining runtime and grading boundary

The source contains three producer and four checker canaries for the new
interfaces, including changed roots/cap, actual append-before-HEAD/resume,
owner rejection, packet byte comparison and diagnostic tails. I read them;
I did not execute them or claim they passed. Syntax and actual serial
producer/checker execution remain root's runtime gates.

Each side reuses its own pinned v3 materializer, rank1355 root adapter,
corrected root-batch v2 and v15 arithmetic lineage. The checker reads
producer source metadata but does not import the new producer arithmetic.
Both sides authenticate the raw marking file
scratchpad/fuda1_a0_rmax_data.g and word file
scratchpad/a0_paper_words_v1.json before accepted arithmetic import/context
construction; their byte/SHA pins enter source.json.data and same-owner
resume comparison. This closes the newly identified raw-marking input edge.
Complete P1/lift semantics, Task554 relation semantics, Task712 maps,
structural v453 slicing, old rank/Conn/history and accepted old target
derivations retain their disclosed premise roles. Full-word projector,
normalized-exponent and eleven-slot gates are not executed by this packet
loop. These shared premises and old lineage limits still belong in the
workshop's incremental CV-9 account; this source review supplies no third
arithmetic derivation and no external cross-checked grade.

Only this reply file was written for Task949. v220 and all source/workflow
files were left to their assigned owners. Run/commit/dispatch by this
auditor: none.

AUDIT_949_VERDICT: PASS_STATIC_SOURCE_SCOPE; DIAGNOSTIC_TAIL_DEFECT_CLOSED; NO_REMAINING_NECESSARY_SOURCE_FIX_FOUND; RUNTIME_PENDING; CROSS_CHECKED_FALSE; VERIFIED_FALSE
