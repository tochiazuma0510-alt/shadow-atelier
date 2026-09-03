# Luna Task648: last finite Task640 v3 release repair

Role: Luna implementation.  Read this complete mail and the complete Task646
reply, then repair the same Task640 v3 quartet in place.  Modify only:

1. `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`;
2. `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`;
3. `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml`;
4. `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md`.

Do not make a v4, edit proofs/v220/audit replies, run production/GHA, use git,
or redesign the endpoint arithmetic.  R1, R3, R4, R5 and R7 are accepted and
must remain unchanged.  Close only the three concrete Task646 blockers below.

Task646 reply: 10,783 bytes / 209 lines / SHA-256
`fe1a6fbec8a3b4518b2e12cae72f3dd46e29d910ed3ad5b5407264bda7183c41`.

## 1. F646-A: canonical parent scalar types

The producer emits `task601_run`, `task601_attempt`, `source_run` and
`candidate_run` as JSON strings.  Make the checker expected parent use the
same four exact strings.  Do not weaken exact dictionary equality, coerce
untrusted input, or change the workflow identifiers.  Add a tiny live parent
validator used by production and selftest so an integer/string mutation is
rejected.

## 2. F646-B: exact seven receipt objects

In the checker define the exact key-to-filename roster:

```text
rho2_packed       rho2.bin
rho2_dense        rho2-dense.bin
lower_dense       lower-dense.bin
target_dense      target-dense.bin
path_signatures   path-signatures.json
signature_buckets signature-buckets.json
roots             authenticated-roots.json
```

For every key require the complete receipt object to equal
`{file: fixed_name, bytes: len(independently expected bytes), sha256:
sha(independently expected bytes)}`.  It is fine to authenticate the named
blob early and perform the complete equality after its expected bytes have
been independently reconstructed.  Reject aliases, duplicate names and
renames.  Route a tiny filename/size/digest mutation roster through the same
production receipt validator.

## 3. F646-C: real live-predicate fixtures

Replace the synthetic `if unequal: fail(...)` mutation count with small
validators which are genuinely called by production and by `--selftest`.
Factor only what is already inline; do not build a generic framework.  At
minimum the production path and fixtures must share these predicates/helpers:

1. exact parent equality and false/null claim equality;
2. exact root shape/order and occurrence type/coordinate/sign roster;
3. reached seeds from raw terms before cancellation;
4. endpoint identity by typed slot, including slot 1 versus 5 and E3 versus
   E4;
5. signature right extension and full-signature bucket grouping;
6. direct-versus-occurrence equality and nonidentity block-product rejection;
7. exact target/lower/top/packed bytes, packing roundtrip and the seven exact
   receipts; and
8. the existing live leaf/header/record/EOF/ancestry-binding parser.

Use tiny stand-ins/callbacks for group multiplication and byte arrays so the
selftests remain serial and finish in seconds.  They must reject mutations of
sign, inverse/PP/block/prefix/right-multiplication order, premature signature
merge, a raw seed cancelled only after source collection, missing/swapped
roots, parent scalar/envelope, manifest field/claim, receipt filename/size/
digest, target/lower/top/packed values and malformed leaf data.  Crucially,
the rejection must come from a helper invoked by production, not a lambda
which calls `fail` merely because two toy constants differ.

The producer need not duplicate the checker's full adversarial roster, but
its production ordering helpers and leaf parser must be the ones its bounded
selftest exercises.  The checker is the independent acceptance authority.
Do not run a real group, graph, ancestry or dense production fixture.

## 4. Frozen boundary and handoff

Keep the workflow inert under `false &&`, producer-side pinned v12f allowed,
checker shared semantic execution absent, ancestry stream-only, bucket-only
dense replay, all live caps and every later claim false/null.

Run bounded serial `py_compile`, both selftests, YAML safe parse, forbidden
shared exec/import scan and immutable action scan.  Update workflow pins only
after the Python/reply bytes are final.  Report exact bytes/lines/SHA-256 of
all four files in the completion message (the reply may state that its own
post-write hash is supplied out of band).  End the reply with
`READY_FOR_TASK649_FINAL_REAUDIT`.
