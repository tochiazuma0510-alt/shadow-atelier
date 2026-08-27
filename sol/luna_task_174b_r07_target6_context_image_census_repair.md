# Luna task 174b: target6 context-image census implementation repair

Date: 2026-08-27
Role: Luna / static implementation repair only

## 1. Ruling

Task 174 v1 is `STOP`: it is a conservative INPUT_STOP design draft, not an
implemented census.  Read the complete task, reply, five deliverables, and
the independent audit message supplied with this commission.  Repair the
implementation without running Python, GAP, Node, git, or GHA locally.

The following defects are mandatory to close: stale mutable task169 pin,
context-pair serialization type error, wrong parent-letter assignment,
four-signed-letter discovery instead of positive x/y discovery, missing
projection/fibre/Delta3/section data, INPUT_STOP-only checker, fictitious
selftests, dormant driver, live placeholders, nonreproducible fixture, and
inflated reply language.

## 2. Authorized files

Edit only the five still-uncommitted task-174 files:

```text
search/d972_r07_target6_context_image_census_v1.py
crosscheck/check_d972_r07_target6_context_image_census_v1.py
search/d972_r07_target6_context_image_census_gha_driver_v1.g
search/certs/d972_r07_target6_context_image_census_preflight_v1_20260827.json
sol/luna_reply_174_r07_target6_context_image_census_v1.md
```

Do not touch task169 or any predecessor.  No execution is authorized.

## 3. Stable input boundary

Remove task169 as an imported module and as a pin.  It is an uncommitted,
currently changing implementation and cannot authenticate task174.  Rebuild
the required typed E4, registry rows 1--3, and Delta3 quotient directly from
the frozen task172-v7, task168, task157ee/q3 inputs and their exact immutable
pins.  Pin every actually imported source/artifact, including the complete
task172-v7 and task157ee receipts needed for context rows and marked values.

Add final exact producer/checker/static-fixture pins to the GHA driver after
the Python sources and fixture are frozen.  No placeholder or wildcard may
remain.

## 4. Complete producer

Implement the full task-174 contract, not a plan string.

- Evaluate and cross-bind `x,y,x^-1,y^-1,xy` in all three exact contexts.
- Require literal 154-byte E4 serialization per coordinate and a literal
  462-byte concatenated triple key.  Serialize a context *pair* through its
  two E4 values explicitly; never pass the pair to an E4-value serializer.
- Discover by positive generators in the exact order `x,y`.  Record the
  actual generator used on every new parent edge.  After closure, reconstruct
  and validate all four signed transitions `x,y,x^-1,y^-1`.
- Enforce the 2,000,000-state cap before inserting a novel state.  Distinguish
  state-cap and deadline stops, retain exact seen/frontier/discovery-prefix
  digests, and clear all INPUT_STOP-only reason/unknown fields on an executed
  run.
- For COMPLETE, compute every individual and pair projection image and
  kernel, literal set digests, uniform fibres, Lagrange identities, equality
  pattern, sections/statistics, full closure, Delta3 quotient/surjectivity/
  fibres, and overflow-safe `6441*|Delta_E|`.
- Run at least 20 pinned predecessor word canaries through both evaluators.
- Emit a canonical self-digested receipt to an explicit `--output`; do not
  overwrite the checked-in static fixture.

The intersection of the kernels of all three literal coordinate projections
of a subgroup of `E4^3` is necessarily the identity.  Record and prove that
fact.  The original request for a nontrivial *common three-coordinate kernel*
fixture was ill-typed and is superseded; instead use a nontrivial individual
or pair-projection kernel fixture.

## 5. Independent checker

The checker must handle COMPLETE, UNKNOWN_RESOURCE, and INPUT_STOP.  It may
import pinned predecessor APIs under fresh names but never the task174
producer or its helpers.

For COMPLETE, independently enumerate with a different positive-generator
order, compare literal sorted state-set and all image/kernel/pair sets,
rebuild four-letter closure, replay at least 1,000 sections (or all if
smaller), and independently rebuild the Delta3 quotient and every count and
digest.  Different discovery order must not be confused with different
canonical state-set identity.

For UNKNOWN_RESOURCE, rerun the same registered cap/deadline contract only
to the extent needed to authenticate the exact bounded prefix; never infer a
group order or projection census.  INPUT_STOP validates only the immutable
static fixture and cannot yield a cross-checked census.

Use production-path small fixtures for a genuinely nonabelian linked image
strictly below the direct product, unequal individual kernels, a nontrivial
individual or pair kernel, honest cap UNKNOWN, and corrupted parent
rejection.  Implement the full mutation list from task174 against real
validator paths.

## 6. Executable serial driver

The ASCII driver must actually execute, not merely construct a shell string.
Provide distinct cheap fixture-selftest and GHA census modes.  In census mode:

1. reject only driver-owned `ci/out` outputs;
2. leave the checked-in INPUT_STOP fixture immutable;
3. run producer with an explicit `--output` under `timeout` and `pipefail`;
4. run checker serially on that receipt under a second bounded timeout;
5. call every terminal/JSON/boundary gate;
6. require exact source pins, exactly one producer and checker marker, and
   exactly one allowed terminal;
7. write receipt, verdict, full logs, hashes, timing, and final sentinel.

The producer plus checker outer caps and upload margin must total at most
21,600 seconds.  Preserve logs on every failure.  An UNKNOWN_RESOURCE result
may be cross-checked only as a bounded prefix and must remain UNKNOWN.

## 7. Static fixture and reply

Regenerate the checked-in INPUT_STOP fixture from the producer's actual
default/static path and bind its exact bytes/SHA.  Its reason must not claim
a currently running Python process; use the timeless reason
`LOCAL_EXECUTION_NOT_AUTHORIZED_STATIC_FIXTURE`.

The reply must honestly distinguish implemented-but-unexecuted paths from
results.  Report static hashes and `GHA dispatched=false`; do not claim any
projection, fibre, order, mutation, or checker result before execution.  End
with `R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_STATIC_READY` only if no placeholder
remains; otherwise keep STOP.
