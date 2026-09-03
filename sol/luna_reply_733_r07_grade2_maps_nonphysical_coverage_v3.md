# Luna Reply 733 — grade-two maps nonphysical coverage v3

## Result

`DONE`. The observed GHA failure was repaired as the requested finite tuple-index correction. V2 was not overwritten. No actual `--emit`/`--check`, workflow edit, GHA operation, or git operation was performed.

V3 is a candidate for independent audit/relaunch only. It does not claim an accepted map artifact or any grade-two/A0/COMMON/cofinal/fake/Ihara result. `verified=false`.

## Output receipts

| file | bytes | LF | final LF | SHA-256 |
|---|---:|---:|---|---|
| `search/d972_r07_grade2_forward_adjoint_maps_v3.py` | 46,179 | 989 | yes | `7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84` |
| `search/check_d972_r07_grade2_forward_adjoint_maps_v3.py` | 49,727 | 1,013 | yes | `d334b3cea69a2505a5c57794cedb9f40701881bf2801757606491dcd5d6feec6` |
| `sol/luna_reply_733_r07_grade2_maps_nonphysical_coverage_v3.md` | sealed reply | sealed reply | yes | supplied externally after sealing |

Checker v3 pins and authenticates exactly:

```text
path   search/d972_r07_grade2_forward_adjoint_maps_v3.py
SHA256 7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84
```

## Finite repair

Both independent `verify_coverage` implementations now branch on the destination type:

```text
nonphysical (tag,component,monomial,psl):
  component=1, monomial=2, psl=3

physical (character,block,component,monomial,psl):
  component=2, monomial=3, psl=4
```

Source decoding remains `(tag,component,monomial,psl)` at indices `0/1/2/3`. Physical character/block checks remain at `0/1`. The all-tags, both-components, all-six-monomials, and all-504-PSL requirements are unchanged.

No sparse entry, action, aggregation, transpose, inverse, coordinate encoding, parser, source-pin, bool gate, or safe-output formula was changed.

## Mandatory live regression

Each selftest now sends the actual complete character-zero `T_fwd(x)` record family through its own production coverage helper and requires the exact receipt:

```text
source coordinates:       36288
source tags:              0..5
source components:        0..1
source monomials:         0..5
source PSL count:         504
destination coordinates:  36288
destination tags:         0..5 (decoded nonphysical tuple)
destination components:   0..1
destination monomials:    0..5
destination PSL count:    504
```

The existing full character-zero actor inverse-pair and nonidentity-prefix/B aggregation fixtures remain active. A live mutation redirects every destination with monomial 5 into monomial 0 while retaining every source coordinate. The same production coverage helper rejects because destination monomial 5 disappears.

## V2/V3 diff scope

```text
producer: +36 / -6 lines
checker:  +34 / -9 lines
```

These changes comprise only v3 schema/marker/source-pin updates, the physical/nonphysical destination-index branch, exact live coverage receipt, malformed-destination regression, and rejection-count update.

## Bounded commands and results

Bytecode cache was redirected outside the repository. Executed only:

```text
python -m py_compile search/d972_r07_grade2_forward_adjoint_maps_v3.py search/check_d972_r07_grade2_forward_adjoint_maps_v3.py
python search/d972_r07_grade2_forward_adjoint_maps_v3.py --selftest
python search/check_d972_r07_grade2_forward_adjoint_maps_v3.py --selftest
```

Results:

```text
py_compile: PASS                         wall 0.319 s
producer v3 selftest: PASS              wall 1.177 s
  internal elapsed 0.928 s
  fixture_rejection_count 3
checker v3 selftest: PASS               wall 1.068 s
  internal elapsed 0.946 s
  fixture_rejection_count 13
```

The new third/thirteenth rejection is the malformed nonphysical destination-coverage mutation. All prior producer/checker fixtures remain green.

```text
ACTUAL_MAP_BUILD=DEFERRED_TO_GHA
GRADE2_DECISION=NOT_RUN
A0=false
COMMON=false
COMPATIBLE_LIFT=false
FAKE=false
IHARA=false
verified=false
```

`R07_GRADE2_MAPS_NONPHYSICAL_COVERAGE_V3_CANDIDATE`
