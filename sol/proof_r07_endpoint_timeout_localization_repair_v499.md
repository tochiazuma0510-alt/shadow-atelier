# R07 endpoint timeout localization repair v499

Author: Sol / 2026-09-04

## 0. Correction

This note corrects only the historical localization sentence in v495 and
Delta447.  It does not change the endpoint-signature monoid lemma, the v6/v7
implementation repair, the candidate universe, or any mathematical terminal.

Run/attempt `33813729918/1`, job `100841127478`, printed

```text
A0_PROGRESS side=producer phase=endpoint_minimal_step_7_zero_word_canary elapsed_seconds=17
```

before the outer 45-minute timeout.  In the producer, `endpoint_checkpoint`
prints after the immediately preceding assertion.  Therefore the empty-word
call and its identity assertion had completed by 17 seconds.  The run did not
stop *inside* that canary.

The next v5 production region had no progress marker.  It consisted, in order,
of the exact-path trie construction with a direct `signature(prefix)`
comparison at every newly inserted prefix, the per-term `direct_column` loop,
and later precision-two aggregation.  The log alone does not distinguish these
three subregions.  Static inspection nevertheless identifies the first region
as the first reachable unmetered repeated generic endpoint evaluation, and v495
removes exactly that family by the proved right recurrence.

Hence the strongest honest localization is

```text
empty-word canary: PASSED at 17 seconds
timeout: after that canary and before the next recorded phase
first removed hotspot: all-prefix direct signature comparisons
exact dynamic subregion of the old stop: UNKNOWN
```

V495's algebra remains valid independently of this correction:

\[
S(1)=1,\qquad S(pa)=S(p)S(a),
\]

so the empty signature is constructed from identities, the four signed atoms
are evaluated once, and every trie signature is obtained by multiplication.
The v7 release still performs each reached-seed endpoint gate and the separate
direct-column/precision-two work required by the current contract.

```text
HISTORICAL_TIMEOUT_INSIDE_EMPTY_CANARY=RETRACTED
EMPTY_CANARY_PASSED=yes
EXACT_OLD_POST_CANARY_STOP_SUBREGION=UNKNOWN
V495_MONOID_CACHE_THEOREM=UNCHANGED
FRESH_RHO2=NOT_YET_PRODUCED
A0/COMMON/COFINAL/FAKE/IHARA=NOT_DECLARED
verified=false
```
