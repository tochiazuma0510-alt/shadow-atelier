# R07 rank-99 tau-free nonzero-constant literal prefix (v431)

Author: Sol / 2026-09-02

Status: paper implementation theorem.  This is the minimal rank99-v5
specialization of v143 and v414 for the already reached tau-free,
coordinates-0--2 branch.  It removes `NONZERO_CONSTANT_SELECTOR` as a
mathematical stop without rebuilding the omitted seven Q0 coordinate stores.
It asserts no current COMMON word, A0 terminal, compatible lift, fake, or
Ihara witness.  The finite extension premises are cross-checked, not Lean
verified; `verified=false`.

## 1. Frozen branch and exact formula

The adopted rank99-v5 producer has already performed, in this order:

1. exact replay of the closed rank99/56 prefix;
2. construction of the separating physical dual `lambda`;
3. exhaustive six-action search;
4. the tau-free adjoint; and
5. the gate that every required context coordinate lies in `{0,1,2}`.

For a compact seed `i`, its independently checked compiled formula is

\[
 F_i(\delta)=K_i+
 \sum_{(j,t)\in R_i} c^{(i)}_{j,t}
       {\bf1}_{\pi_j(\delta)=t},
 \qquad j\in\{0,1,2\},
 \tag{1.1}
\]

over `F_3`.  Equal `(j,t)` entries have already been merged and zero
coefficients deleted.  The v5 raw identity gate proves that (1.1) equals the
direct physical pairing of `lambda` with the corresponding literal conjugate
column.  The v5 producer and checker also already evaluate the compiled ABI
including `K_i`; only the production gate

```text
UNKNOWN:NONZERO_CONSTANT_SELECTOR
```

prevents that evaluator from being used when `K_i != 0`.

The exact kernel orders of the three live coordinate maps are all nine.  Put

\[
 U_i=\bigcup_{(j,t)\in R_i}\pi_j^{-1}(t),\qquad
 W_i=9|R_i|.
 \tag{1.2}
\]

Then `|U_i| <= W_i`.  Moreover the cross-checked task176 extension gives the
literal global roster

\[
 (q,\gamma)\longmapsto
 u_\Gamma(\gamma)u_{Q_0}(q),
 \qquad |Q_0|=1,469,664,\quad |\Gamma|=243,
 \tag{1.3}
\]

of `357,128,352` distinct elements.  In the frozen serialization, cursor
`s` has

```text
qid, gid = divmod(s, 243).
```

## 2. The bounded positive selector

### Theorem 2.1 (NONZERO-K W+1 LITERAL PREFIX AT A FRESH ANCHOR)

Assume `K_i != 0` and that no row has yet been added under the current batch
anchor.  Evaluating (1.1) on the first `W_i+1` distinct elements of (1.3)
returns a nonzero value.  The corresponding direct literal column strictly
raises the anchor physical rank.

#### Proof

At most `W_i` roster elements lie in `U_i`, by (1.2).  Hence among any
`W_i+1` distinct roster elements there is a `delta` outside `U_i`.  Every
indicator in (1.1) then vanishes and

\[
 F_i(\delta)=K_i\ne0.
\]

By the frozen v5 raw/compiled identity, this value is
`lambda(r_i(delta))`.  At a fresh batch anchor the separating dual annihilates
the present physical span.  Therefore `r_i(delta)` cannot lie in that span and its
nonmutating reduction is nonzero.  A global-selector wrapper around the
unchanged v424/v5 literal/physical core then reconstructs the conjugate,
checks all ten coordinates, the exact exponent pair, forbidden-E condition,
direct pairing, row digest, and predicted pivot before one physical
insertion.  Thus the returned column is both literal and rank-raising.
\(\square\)

The fresh-anchor hypothesis is load-bearing.  After one row with nonzero
anchor pairing has been inserted, the fixed anchor functional need not
annihilate the enlarged within-batch span.  A later nonzero formula value
would then no longer by itself prove independence.  V427 already proves that
any nonempty prefix of at most 16 certified rows may be closed.  Therefore a
minimal successor uses this exact boundary:

- if a nonzero-K formula is reached while `rows` is nonempty, close those
  rows and restart with the newly computed dual;
- if `rows` is empty, use Theorem 2.1, retain its first rise, and close that
  one-row batch immediately.

This is not a discarded partial batch and not a new mathematical terminal.
It is an ordinary variable-length v427 close with one dual update.

No support-fibre enumeration is required in the nonzero-constant branch.
Trying support fibres first is sound but cannot improve the worst-case bound
and is not part of the minimal successor.

## 3. Full coordinates without seven additional Q0 stores

The current selective runtime retains only the three 40-byte Q0 stores needed
for coordinates 0--2.  The inherited historical `global_candidate` combines
stored rows and therefore must **not** be called: with only three stores it
constructs a three-entry tuple, whereas the current literal checker requires
ten coordinates.

For cursor `s`, instead construct only the word

\[
 w_s=u_\Gamma(\mathrm{gid})u_{Q_0}(\mathrm{qid})
 \tag{3.1}
\]

from the already retained Gamma section words and Q0 parent/letter tree.
Evaluate `w_s` directly through the pinned `coordinate_blobs` routine.  This
returns all ten typed coordinate blobs and simultaneously checks the literal
word.  Consequently the successor needs:

- no fourth through tenth Q0 store;
- no second Q0 BFS;
- no global-roster cache;
- no boundary closure or large matrix copy; and
- at most `W_i+1` ten-coordinate word evaluations for a nonzero-K seed.

Distinctness is inherited from the exact extension roster (1.3), not inferred
from a digest.  The producer records `(qid+1,gid+1,cursor)`, the literal word,
the complete coordinate tuple or its load-bearing replay fields, `K_i`,
`W_i`, and the selector cursor.  The independent checker reconstructs (3.1)
from the cursor and re-evaluates all ten coordinates; it does not trust a
producer-supplied row or scalar.

This is not the old support-fibre cursor.  Use the disjoint typed record

```text
["global_nonzero_constant", seed_index, cursor, W]
```

and retain the old integer-first four-entry cursor unchanged for support
fibres.  The global wrapper must not invent a `(coordinate,target,ordinal)`:
the guaranteed outside point is generally in none of those fibres.  Producer
and checker dispatch on the first cursor entry and share only frozen
arithmetic primitives, not selector validation code.

## 4. Exact v6 branch contract

A surgical successor of rank99-v5 may replace only the nonzero-constant stop
by the following branch:

```text
for each formula in printed seed order:
    if K == 0:
        keep the existing complete support-fibre schedule
    else:
        if rows is nonempty:
            close the current certified prefix and restart the outer round
        W = sum(sf.kernel_orders[j] for (j,t) in merged)
        require W < 357128352
        for cursor in range(W + 1):
            qid, gid = divmod(cursor, 243)
            word = reduce(gamma.section_word(gid) + q0_section_word(qid))
            blobs = direct_coordinate_blobs(word)       # all ten
            scalar = compiled_formula_scalar(formula, blobs)
            if scalar != 0:
                call the typed global wrapper around the unchanged literal/physical core
                require its direct scalar equals scalar
                retain the first actual rank rise
                close this one-row batch and restart the outer round
        require one retained rise                       # fresh-anchor theorem invariant
```

For the frozen branch `j in {0,1,2}`, every term in `W` is exactly nine and
`W` is tiny relative to `357,128,352`; the inequality is nevertheless checked
at runtime.  The existing action-first order, printed seed order, soft flush,
resource limits, checkpoint chain, COMMON replay, and positive-only claim
boundary remain unchanged.  The only batching refinement is the already
proved v427 permission to close the existing prefix before a nonzero-K
formula and to close the guaranteed nonzero-K rise as a one-row batch.

The checker must reject at least: wrong `(qid,gid)` for a cursor, a nonliteral
word, any of ten coordinate drifts, `W` drift, a cursor outside `0..W`, a
zero compiled scalar, direct-pairing drift, dependent-row promotion, and any
change to the rank99/56 prefix.  A time/RSS stop remains
`UNKNOWN_RESOURCE`; no incomplete prefix is a negative certificate.

### 4.1 Preserve an actual v5 resource prefix

The current v5 production is already running, so a successor must not force a
restart from C99.  Its resume parser accepts exactly:

1. canonical C99;
2. an independently authenticated closed v5 checkpoint; or
3. an independently authenticated closed v6 checkpoint.

For case 2, first validate the v5 schema, binding, state seal, complete
rank99 prefix, appended batches, segments, rolling prefix and ledger using
the frozen v5 constants.  Migration changes only the top-level schema and
binding and recomputes the top-level state seal.  It does not change a row,
batch, segment, profile, cursor, prefix digest, ledger digest, or historical
identity.  The actual v5 file identity becomes the input identity of the
first new v6 segment, exactly as an ordinary resume does.  The independent
checker implements the same legacy validation separately; it must not call
the producer resume helper.  Thus every durable rise found by the running v5
lane remains usable.

## 5. v220 consequence

This theorem is execution readiness, not a milestone numerator:

```text
A0 actual COMMON:                         still 0/1
rank99-v5 current production:              unchanged and still running
NONZERO_CONSTANT_SELECTOR mathematical stop: removed on tau-free S0--S2 branch
extra full-Q0 stores/global cache:          not required
positive promotion:                        still requires independent literal replay
```

`R07_RANK99_TAU_FREE_NONZERO_CONSTANT_GLOBAL_PREFIX_V431_PAPER_GRADE`
