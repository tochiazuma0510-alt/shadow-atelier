# Luna task 274 — task226 checker JSON-native rebuild repair v1

Role: bounded one-owner independent-checker repair.  Read the current task226
producer, checker, fixture, driver, and reply in full.  Do not run Python,
Node, GAP, git, GHA, or network.  Edit only the checker, driver pin, and
existing task226 reply.  Parent Sol owns execution and repository work.

The full diagnostic run `33148423786` at immutable head
`97de2a2943f178a29ab6c774d521ce7f0bf7bc12` gave producer SELFTEST PASS but
checker `UNKNOWN_INPUT reason=fresh complete ABI rebuild`.  The recursive
first-difference run `33148795778` then fixed the exact owner:

```text
D226_FIRSTDIFF ["$.literals.substitutions.PB3.H1[0].<type>","tuple","list"]
D226_REBUILT_DIGEST      dd27a839adaa951652d10c5e3ca2af7d11c7cad95f7e03dac570f473c5475245
D226_RECEIPT_ABI_DIGEST  dd27a839adaa951652d10c5e3ca2af7d11c7cad95f7e03dac570f473c5475245
```

Thus all canonical JSON bytes already agree.  The checker-owned
`literal_substitutions()` retains Python tuples in the freshly rebuilt ABI,
whereas the producer receipt has necessarily decoded them as JSON lists.  A
Python object equality is therefore rejecting a byte-identical independent
reconstruction.

Make the checker reconstruction return a fully JSON-native ABI before sealing
and before the exact object equality: dictionaries, lists, strings, integers,
booleans, and null only.  The conversion must use the checker's own canonical
serializer/decoder (or an exactly equivalent recursive conversion) and must
not consume producer-carried ABI fields.  Recompute the ABI seal after this
normalization.  Retain exact object equality after normalization; do not
replace it by digest-only acceptance and do not weaken any word, Fox, quotient,
occurrence, ancestry, mutation, predecessor, terminal, or forbidden-conclusion
gate.  Production semantics remain unchanged.

Refresh the checker pin in the driver and the existing reply.  Report exact
identities as `UNEXECUTED`.  A2 remains `1/3` until parent GHA obtains both the
producer and independent checker SELFTEST success terminals; actual
specialization remains absent.

