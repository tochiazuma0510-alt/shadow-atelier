# Luna Task632: finite Task625 static/performance repair

Role: Luna implementation.  Apply only the four finite repairs isolated by
Sol(max) Task631 to the still-unreleased Task625 v2 quartet.  Do not run
production/GHA/git and do not refactor unrelated routing or authentication.

The pre-repair exact snapshot is:

- producer 71,954 bytes / SHA-256
  `c3b7d53accb8b0814049cae4e1cadebc905941031b156dd12763ac2072219cf0`;
- checker 101,254 bytes / SHA-256
  `33dd8cf7fdc94c971e58a09211e5acbf749980dfc49109f3bf51db4495d46002`;
- workflow 6,077 bytes / SHA-256
  `35682ef40110d15199ddc5e17300b25e17d44bd414d59d2346bca86fbf95f653`;
- Task625 reply 7,968 bytes / SHA-256
  `b3872695fb287841c5d4078471fdadc076c6a3c6eac45e0656c626e3f79b7b17`.

Read the completed Task631 reply before finalizing.  Modify only:

1. `search/d972_r07_a0_grade1_selected_slp_v2.py`;
2. `search/check_d972_r07_a0_grade1_selected_slp_v2.py`;
3. `.github/workflows/d972-r07-a0-grade1-selected-slp-v2.yml`; and
4. create `sol/luna_reply_632_r07_task625_static_performance_repair.md`.

Do not edit the historical Task625 reply or any theorem/audit/v220 file.

## R1: one outgoing-edge construction per active node

Keep the existing whole-graph streaming prevalidation and its constant-memory
property.  During the later coefficient pass, for each nonzero node generate
and validate/materialize that node's outgoing checked edge tuple exactly once,
reuse it for every exact path in that node bucket, then release it.  Do not
materialize or retain all graph edges globally.  Provider calls for a two-path
active node must be independent of the number of paths (one streaming
prevalidation call plus one coefficient-pass call), and fixtures must measure
this.  `state_edge_traversals` still counts state-edge pairs with multiplicity,
not provider calls.

## R2: no terminal full leaf-map clone

In the producer, retain literal leaves from first insertion under
`(seed, exact freely-reduced tuple)` keys.  Do not build a second full leaf
dictionary merely to replace transient path IDs at the end.  The binary leaf
bytes and sorting contract must remain identical.  The checker remains an
independent exact-tuple implementation.

## R3: no second tuple allocation after canonical multiplication

For already-tuple canonical freely reduced products, validate/scan and intern
or remember the tuple without reconstructing it with a second tuple
comprehension.  Non-tuple external inputs must still be canonicalized and all
letter/path-length/free-reduction gates must remain.  Do not weaken exact word
equality or use endpoint/signature coalescence.

## R4: manifest-inclusive durable cap

Construct the canonical manifest bytes before publication and enforce the
durable cap on the sum of every payload file **including `manifest.json`**.
Report that inclusive total in terminal telemetry; the independent checker
must recompute and cap-check the same inclusive byte total.  Avoid a
self-referential manifest-size field unless a stable fixed-point encoding is
explicitly proved; terminal/checker telemetry is sufficient.  Resource
exhaustion must remove staging and publish no partial payload.

## Gates and reply

Retain every Task625/Task622 fixture and add bounded producer/checker tests for
R1--R4, including a two-path provider-call count, no producer terminal leaf
clone path, canonical tuple reuse without gate weakening, and a manifest byte
that crosses the durable cap.  Run only serial `py_compile`, both selftests,
YAML parsing, exact hash-pin checks, and whitespace checks with cache outside
the repository.

Update workflow executable/reply hashes after the quartet is fixed.  Preserve
the 60-minute/8-GiB/7-GiB limits and v475 pin.  Report final bytes/SHA-256,
test outputs, copied invariants, and remaining result-dependent risk in the
new Task632 reply.  Explicitly state that production, A0, COMMON, cofinal,
fake, Ihara and Lean verification were not run or established.
