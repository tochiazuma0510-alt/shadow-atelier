# Luna reply 275 - task227 SELFTEST envelope schema repair

UNEXECUTED: no Python, Node, GAP, git, GHA, or network command was run. Only
the five authorized task227 files were changed; task226/task233, task229,
predecessors, proofs, and workflows were not changed.

## Static repair

- Removed producer focus/reference equality sentinels. Producer and checker
  independently decode canonical sparse data, reconstruct w/u0/target,
  ancestry rows, queue/orbit closure, canonical 486 rows, all 729 translates,
  block c_i, lambda, kappa, four replay rows/digests, quotient, and dual
  pairings/annihilation.
- Every one-to-one mutation now changes an extant owner in a production-shaped
  SELFTEST case and runs the complete validator; only the validator rejection
  class is caught, with fixed preregistered gates and uncaught MutationAccepted.
- Added exact `direct|inverse` ABI vocabulary and canonical H1/H2/P target
  block checks in both implementations. Cases carry exact terminal, typed
  resource cap/phase, and explicit false downstream flags, all validated.
- Checker independently reruns all 24 mutations and requires exact roster,
  gates, and 24/24 rejection evidence. Driver pins are refreshed; fixture
  roster and identity are unchanged.
- Preserved the exact nonzero block remainder for NONMEMBER certificates and
  require `block_combined + block_remainder == target`; MEMBER requires zero
  remainder. Both sides rebuild block echelon pivots/ancestry from block rows
  and compare the complete canonical encoding.
- Replaced the resource dictionary with a sealed typed `UNKNOWN_RESOURCE`
  canary, use the active invocation budget for independent orbit work, and
  made the occurrence-basis mutation fail its structural owner gate first.
- Fixed the producer terminal branch syntax, changed the occurrence owner to a
  canonical ordinal-11 row, threaded exact selftest/production resource phase
  through checker verification, and run actor-roster/Q-axiom checks once per
  SELFTEST while keeping production structural checks mandatory.
- Renamed the checker occurrence structural rejection to its preregistered
  `occurrence basis row` owner gate; no mutation data or ordering changed.
- Fixed the producer expected-row comparison to read the typed ABI owner
  `abi["u0"][i]`, preserving the encoded occurrence-vector check and roster
  equality.
- Fixed the envelope schema owner: SELFTEST certificates now use
  `SELFTEST_SCHEMA`, while production and UNKNOWN certificates retain
  `SCHEMA`; the digest is sealed after schema selection.

## Identities

```text
producer  44033  658c773df56f4f4271aa1ddfb347db03562f73b124e06f9e602ca2b231347763
checker   30232  196b2bf96b39d6a9f63ae2d5a83c9e981f2cab0f67b78395800ebe6c0dbad661
driver     5216  d5a402c2e352442085934085ac47eca7c3411115a1d7f04f8a4b3e08be373c1c
fixture     594  d4130b99d62eb7f2dd0a5ee887881e68798637cb4945747f47f883f4961bf911
reply     3467  (self-referential SHA intentionally omitted; final SHA reported to parent)
```

No accepted task226 production package or production MEMBER/NONMEMBER terminal
was inferred. A3 remains zero pending parent execution and audit.

```text
A3 ACTUAL PACKAGE:             0/3 AWAITING ACCEPTED TASK226
A3 486/729/ORBIT EQUALITY:     0/3 UNEXECUTED
A3 MEMBER OR DUAL:             0/3 UNEXECUTED
A4 AND LATER:                  UNCHANGED
COMPATIBLE COFINAL LIFT / FAKE / IHARA: NOT DECLARED
```

`TASK275_TASK227_SELFTEST_ENVELOPE_SCHEMA_UNEXECUTED`
