# Luna task 275 — task227 SELFTEST envelope schema repair v1

Role: bounded one-owner implementation repair.  Read the current task227
producer, independent checker, fixture, driver, and reply in full.  Do not run
Python, Node, GAP, git, GHA, or network.  Edit only the producer, driver pin,
and existing task227 reply.  Parent Sol owns execution and repository work.

GHA diagnostic run `33148427632`, immutable head
`97de2a2943f178a29ab6c774d521ce7f0bf7bc12`, produced:

```text
D227_PRODUCER_TERMINAL UNKNOWN_RESOURCE
D227_CHECKER_TERMINAL UNKNOWN_INPUT reason=consumer schema
```

This is a SELFTEST envelope bug, not a resource or mathematical terminal.
`selftest()` builds a complete five-case result, but returns it through
`certificate(SELFTEST, result)`, whose top-level `schema` is always the
production `SCHEMA`.  The independent checker correctly requires the
top-level `SELFTEST_SCHEMA` in SELFTEST mode.  The producer therefore reaches
serialization and is then caught by its resource budget only because the
wrong envelope is larger than the already-accounted budget path; the checker
sees the wrong schema first.

Repair exactly this schema owner.  A SELFTEST certificate must have top-level
`schema == SELFTEST_SCHEMA`; production MEMBER/NONMEMBER/UNKNOWN envelopes must
retain `schema == SCHEMA`.  Compute `self_digest_sha256` only after the final
schema has been installed.  Do not weaken or change the checker rule, the five
cases, the 24 mutation roster, the exact remainder/member equivalence,
486/729/orbit comparisons, resource caps, terminal vocabulary, or any
mathematics.  Refresh the producer pin in the driver and the existing reply.

Report the exact changed owner and final identities as `UNEXECUTED`.  A3 stays
`0/3`: no actual accepted task226 package, actual orbit equality, or actual
MEMBER/NONMEMBER terminal exists merely from this SELFTEST repair.

