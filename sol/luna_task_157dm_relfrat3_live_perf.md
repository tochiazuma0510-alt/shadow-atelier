# Luna 157dm — relative-Frattini-3 live-log / inverse-cache preflight repair

Role: Luna implementation only.  This is a semantics-preserving successor to
157dl.  Do not run GAP, GHA, git, or any heavy/local production computation.

Authorized files only:

1. `search/d972_b345_relfrat3_v1.py`
2. `search/check_d972_b345_relfrat3_v1.py`
3. `search/d972_b345_relfrat3_gha_driver_v1.g`
4. `sol/luna_reply_157dl_b345_relfrat3_fox.md`
5. `sol/luna_reply_157dm_relfrat3_live_perf.md`

Keep every mathematical predicate, search universe/order/cap, receipt
certificate, q3 SHA pin, and terminal meaning unchanged.

## 1. Live GHA progress is explicitly optional

Per the researcher, do not spend development/audit time on live tee.  Leaving
the current redirected producer/checker logs unchanged is acceptable.  If a
fully reviewed pipefail-safe change was already completed before this update,
it may remain; otherwise make no driver logging change.  Correctness and the
inverse repair below have priority.

## 2. Replace raw power inversion by the frozen finite normalized inverse fibre

Current `inverse_order_cache` remembers only the order and reconstructs raw
`S^(ord-1)` inverse words.  This is a dispatch blocker: even the base map can
expand as raw `S^8`, repeating the old exponential-word-growth failure.  Remove
that production path; do not merely cache its first output.

The frozen q3 receipt already authenticates the normalized order-nine roof
orbit and the complete 27-element fine correction fibre.  The inverse of the
selected exponent-2 map lies over canonical exponent 7.  Reconstruct the
canonical exponent-7 word and all 27 authenticated fibre corrections from the
pinned receipt.  Evaluate the resulting finite 27 candidates and choose the
first whose induced six E4 source images compose in both orders with the fixed
base exponent-2 six-image tuple to the six marked E4 generators.  Require exact
uniqueness or record the deterministic first plus the full passing index set;
in either case replay the two-sided identities independently in the checker.
This gives one bounded, short, shared inverse tuple without free-word powering.

Reusing the tuple is sound only for identical induced E4 endomorphisms.  The
five coarse coface checks on a correction are not by themselves a licence to
assume all six `source_words_m0` contexts agree.  For every candidate directly
compute its exact six-image E4 tuple and compare it with the base tuple.  On a
match, reuse the finite exponent-7 inverse and replay both compositions.  If a
candidate has a different tuple, do not reject it mathematically and do not
fall back to raw powers: record a candidate-local
`missing_bounded_inverse_representative` resource skip so an otherwise empty
run ends UNKNOWN_RESOURCE.  A later version may add another finite inverse
fibre for such a tuple.

For each candidate still independently rebuild and certify its own
S-relations, T-relations, ST/TS residuals, Fox gradients, and sparse boundary
ledgers; do not reuse acceptance or a candidate certificate.  Do not combine
the frozen componentwise Q4/Pi4 inverse words.

Bind the normalized exponent-7 row, all 27 tested indices, passing indices,
selected inverse words, tuple-match counts, cache hits/misses, and max inverse
length to the receipt, and make the
checker validate the cache contract without trusting it for the positive
proof (the checker must still reconstruct the selected inverse and all target
words independently).

## 3. Close the unsupported terminal mutation

The current checker accepts a receipt whose terminal is changed to
`B345_RELFRAT3_MISSING_MATCHED_CHAIN` with almost no structural validation.
This producer has no legitimate returned branch with that token: initialization
failure exits nonzero.  Reject that unsupported terminal fail-closed (or define
and independently validate a genuinely empty pre-matched receipt branch, if
already present without broadening scope).  Add a mutation canary.

## 4. Audit

One lightweight selftest/compile pass is authorized after edits.  Add a small
canary for a cache hit with the same quotient endomorphism but a distinct free
representative if feasible; otherwise fail closed and explain.  Run static
hash/pin/diff checks.  Return exact final SHA-256 values and a GO/STOP token.

Do not add the PB5 fallback in this repair.  A direct-lane miss remains honest
UNKNOWN and will trigger the separately designed PB5 continuation.
