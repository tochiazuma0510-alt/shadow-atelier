# Task944 -- lambda-free root packet: narrow implementation decision

## F1. Recommendation and retained state

Recommend one bounded packet-plus-root-loop handoff, subject to root adoption.
Packet plus one current-root result is smaller by loop/prefix wiring, but
retains one-hit handoffs. The same fixed 44-seed implementation can consume
successive hits using the successful insertion code, without an actor engine
or generic framework. This reply does not authorize or implement that work.

Retain run33956437467/1, head b9ae78b0950b186463849c3ec874f6474f359851,
artifact9966542166 (archive984053 bytes; exact pins in Task944).
The inspected manifest/result name rank1356, generation8061, state head
d467e4e60b8bff88272cddd4b01d630d763e863b4500015c7c6c077b23ddf26b.
Seed30/34 are saved pivots; seed35/36's old scalars are stale. New values unknown.

## F2. Exact reuse and smallest missing adapters

In producer937 (`d972_r07_rank1355_root_seed_scalars_v1.py`), reuse
`pinned_parent_descriptors` (148), `new_roots` (266), and `scalar_stream` (374).
Adapt `root_record` (280) to explicit current generation/head/lambda arguments;
its `NEW_*` constants cannot survive into changing-lambda records.
Adapt the body/source/seed traversal of `seed_only_fold` (326) to primal
relations; do not call its old scalar fold or `p1_root_values` (292).

In producer940 (`d972_r07_actual_root_seed_materializer_v3.py`), reuse
packing/dot/B helpers, `validate_p1_instruction` (684), `validate_old_state`
(998), `physical_reduce` (1239), `normalize_pivot` (1270), `update_target`
(1284), and `check_final_separator` (1301). Extract the lower/full-top lift
arithmetic and literal receipts from `replay_selected_seed` (823).
`separator_after_append` (1318) and the append/output part of `materialize`
(1412) need explicit current state arguments instead of `CURRENT_*` constants.

Missing functions are only: collect all 44 sealed relations; build the fixed
primal packet with row-streamed subtraction; load the exact rank1356 start;
evaluate packet root scalars; and wrap the existing one-step append in a loop.
Scalar first-hit archive pins and contracted P1/q arrays disappear from the
packet path. Use each side's own accepted evaluator once per seed for all
four components; no global monkeypatch or third seed evaluator is needed.

## F3. One-pass packet and bounded live data

Collect all old-source then target/source contributions from five Task554
bodies, one body resident. Write per-seed ordered events, including cancelled
literal nodes, and finalize their seals before numerical coefficient folding.
Keep a 44-by8059 uint8 coefficient table: 354596 bytes. This is not a full
8059-by241928 lift matrix. The raw seed evaluator initializes 44 full defects.

Stream the P1 cache/instructions once (instruction buffer at least1MiB),
retaining compact referenced instruction/row receipts, not all decoded rows.
For each top row, subtract its coefficient into the relevant seed accumulators.
Stream the twelve lower blobs once using the existing old/new component
placement. Process coefficients per seed/row with bounded scratch, avoiding
a broadcasted 44-by-full-lift temporary. No P1 pass occurs per root hit.

Named persistent accumulators are top6386688 bytes and lower4258144 bytes;
packed top output is1596672 bytes. Additional live data includes one raw seed,
one decoded row/component, F3 scratch, four q vectors and packed state rows.
These are array sizes, not RSS/runtime guarantees. Require all96776 lower
entries zero per seed and independently reconstruct every top slice; release
lower/coefficient working arrays after sealing their receipts.

Packet files need only fixed parent/dictionary/lift pins, packed tops with
explicit character/seed offsets, 44 lower-zero/component receipts, per-seed
ordered ancestry, and a shared referenced-P1-root index. Selected literal
words join that ancestry to P1 roots, preserving inverse/order/projector
conventions. Hits reference packet rows and these roots; they need neither
reparsed Task554 bodies nor duplicated ancestry for every changing lambda.

## F4. Fixed start, bounded loop and durable prefix

The start adapter authenticates the old1354 base plus two exact saved deltas.
The new seed34 result's parents.state already names base plus seed30; join
its predecessor/head, pivot, current target and lambda receipts, then retain
the rows in insertion order. No existing artifact is changed or concatenated.
This adapter needs no new scalar authority and no old target/Conn replay.

At each step form four fresh B-adjoints and all 176 character-major/seed-order
packet pairings. First nonzero selects one B application, one nonzero pivot
append and one current-target update. Regenerate lambda and directly test
all saved/new rows and the updated target, then rescan the same fixed packet.
Stop at ROOT_SEEDS_ZERO or MEMBER_CANDIDATE: at most176 new appends, followed
by the terminal root test. This is not actor/grade2/A0 completion.

Use an immutable packet and sequential step directories with the v3 receipts.
Each step references packet/predecessor, not copied base snapshots. Fsync its
complete files/sealed manifest before atomically advancing a small HEAD.
Diagnostics retain the complete prefix; incomplete tail is not a step.
Resume there without repeating seed30/seed34 or completed inserts.
An unpassed prefix remains candidate: the independent checker reconstructs
the packet once and replays that new prefix before it can be accepted.

## F5. Inputs and claim boundary

No missing input found: Task554/P1/Task712, base, both saved deltas and exact
receipts are available. Only root's scope adoption remains, not another gate.
Only this reply was edited; no numerical execution/network/credentials/git.
Accepted lineages stay disclosed; cross_checked=false, verified=false;
no grade2/full-A0 promotion is claimed.
