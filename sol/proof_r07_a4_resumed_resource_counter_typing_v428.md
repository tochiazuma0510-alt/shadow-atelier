# R07 A4 resumed-resource counter typing (v428)

Author: Sol / 2026-09-02

Status: narrow correction to v423 for a resumed delta-chain producer.  It
separates the prior closed-base counter snapshot from the terminal process
snapshot and gives the exact checker predicate for the immutable row-26
artifact.  It does not by itself cross-check row 26 or retain row-27 work.
`verified=false`.

## 1. The equality rejected by the actual artifact is mistyped

For run `33506331399`, the producer result contains three distinct objects.

1. `resource.completed_counters` is the authenticated counter snapshot of
   the resumed **base checkpoint**, whose cursor is `next_row=25`.
2. The sealed delta chain appends rows 25 and 26 and its HEAD is
   `last_row=26,next_row=27`.
3. `resource.semantic_counters` is the terminal process snapshot.  It
   includes the closed row work and the subsequent transient row-27
   `dual_pullback` work up to the wall stop.

Consequently

\[
 C_{\rm base}=C_{\rm completed}
 \quad\hbox{and}\quad
 C_{\rm completed}\leq C_{\rm terminal}^{\rm sem},
\tag{1.1}
\]

but equality of the two right-hand maps is neither intended nor true.  For
example the exact artifact has

```text
                         completed       terminal semantic
bridge_rows                    24                 26
membership_queries             24                 26
active_keys                      0          1,094,076
boundary_rank_rises              0            138,784
correlation_pairs                0         46,789,964
```

The last three differences are dominated by the open row-27 query and are
not durable progress.  Thus replacing `completed == semantic` by an assertion
that all terminal work is closed would be equally wrong.

## 2. Three independent predicates

Let `B` be the canonical base checkpoint, `H` the sealed delta HEAD and
ordered delta chain, and `T` the terminal resource object.

### 2.1 Closed mathematical cursor

Authenticate `B`, replay every delta independently in order, and require all
row, bridge, query/event, epoch, queue, word-DAG, seal, previous-hash, chain,
and HEAD equations.  This replay alone determines the closed cursor

\[
 H=(\operatorname{last\_row},\operatorname{next\_row})=(26,27).
\tag{2.1}

No terminal counter is used to infer (2.1).

### 2.2 Historical completed snapshot

Require

\[
 \boxed{
 T.\mathrm{completed\_counters}
 =B.\mathrm{semantic\_counters}
 =B.\mathrm{completed\_counters}.}
\tag{2.2}

The domains must be exactly the registered semantic domain.  Every value is
numeric and nonnegative, is at most its cap, and is componentwise at most the
terminal semantic map.  Equation (2.2) prevents an arbitrary weaker map from
being relabelled as the completed base.  It deliberately does not say that
the terminal-minus-base work is durable.

### 2.3 Terminal typed resource envelope

Apply v423 to the terminal canonical map and its genuine typed views:

```text
resource.counters
resource.semantic_counters
resource.host_counters
resource.peak_counters
resource.restore_validation_counters
```

For every registered key, the canonical counter equals its unique typed-view
occurrence.  Exactly the reason's trigger coordinate may exceed its cap; all
other terminal coordinates remain bounded.  In the actual artifact the
unique trigger is

```text
wall_seconds = 14402.408729186 > 14400
last_replayable_state = dual_pullback
```

The historical `completed_counters` map is **not** a second typed occurrence
of the terminal semantic map and is therefore not put through the terminal
duplication-equality gate.  It is governed by (2.2).

## 3. Soundness

### Theorem 3.1 (RESUMED RESOURCE SEPARATION)

Predicates 2.1--2.3 are sufficient to accept an `UNKNOWN_RESOURCE` transport
while certifying only its sealed closed cursor.

#### Proof

Predicate 2.1 independently reconstructs every durable transition and fixes
the cursor (2.1).  Predicate 2.2 binds the purported historical completed
snapshot to the authenticated base and prevents it from being forged or
confused with terminal work.  Predicate 2.3 proves that the process stopped
for one authenticated resource excess, with all terminal counter types and
other caps intact.  Since no difference
`terminal semantic - completed` is used as a closed-state claim, transient
row-27 work cannot advance the certified cursor.  Conversely, demanding
equality between those snapshots rejects every honest resumed computation
which does any work after its base checkpoint.  \(\square\)

The theorem is about counter typing, not row semantics.  Promotion of row 26
still requires the independent delta/row replay in Predicate 2.1.

## 4. Required checker and driver regression gates

A versioned successor must use the exact immutable artifact as a positive
regression fixture and reject mutations of:

- the base/completed equality (2.2), either base copy, or the completed
  domain;
- componentwise `completed <= terminal semantic`;
- any base, delta, HEAD, chain, row-25, or row-26 seal/content;
- the unique wall trigger, cap, typed-view equality, or last replayable state;
- any second over-cap coordinate;
- producer status/reason/checkpoint bindings; and
- the checker output self seal or exact terminal cardinality.

The checker-only driver must invoke the checker with explicit
`--producer`, `--output`, `--checkpoint`, `--resume`, authority inputs, and
caps.  Because the frozen checker resolves all `ci/out` paths against its
repository `ROOT`, the six authenticated replay files must be copied to
`$root/ci/out/<exact basename>`, not to a synthetic cwd cone.  The driver runs
one checker and no producer, requires exactly one checker terminal line, a
sealed nonempty verdict of the expected status, and fail-closes on any
Traceback/STOP/nonzero exit.

## 5. v220 consequence

```text
row 26 producer delta chain:             structurally sealed candidate
v423 unique over-cap rule:               retained
completed == terminal semantic:          rejected premise
resumed counter relation (2.2):          paper closed here
independent row-26 replay:                implementation/GHA still required
A4 numerator:                            remains 1/3 UNKNOWN_RESOURCE
```

`R07_A4_RESUMED_RESOURCE_COUNTER_TYPING_V428_PAPER_GRADE`
