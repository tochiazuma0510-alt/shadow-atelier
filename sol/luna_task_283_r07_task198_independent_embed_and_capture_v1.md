# Luna task 283 - task198 independent embed bridge and producer capture v1

Commissioner: Sol / 2026-08-28

Reply to `sol/luna_reply_283_r07_task198_independent_embed_and_capture_v1.md`.

Role: bounded mechanical implementation only.  Do not run Python, Node, GAP,
git, GHA, or network locally.  Parent Sol owns the mathematical ruling,
execution, commits, and workflow dispatch.

Read this commission, the full current task198 producer/checker/driver, the
task157ee independent checker, and the producer/checker seedspan-triple4
helpers before editing.  Edit only:

```text
crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py
search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g
sol/luna_reply_283_r07_task198_independent_embed_and_capture_v1.md
```

Do not change the producer, fixture, predecessor, proof, ledger, workflow, or
any other file.

## 1. Authenticated production outcome and exact failure

GHA run `33143444409` at immutable head
`d3d17b62b3760012af5f768ef87308287dcf30e0` emitted exactly

```text
R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_TERMINAL ROOF_BRIDGE_ISOMORPHISM
```

after about three hours.  The independent checker then stopped immediately:

```text
AttributeError: module 'c198_old' has no attribute 'embed_f2'
```

The failing call is task157ee checker's `JointGroup.eval`.  Task198 currently
passes the producer-side module
`search/d972_b345_seedspan_triple4_v1.py`; that module deliberately names the
map `embed_f2_pb3`.  The authenticated independent helper

```text
search/check_d972_b345_seedspan_triple4_v1.py
574347 bytes
sha256 ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981
```

has the exact checker-side `embed_f2(word)=substitute(word,[[1],[3]])` used by
task157ee.  The producer-side `embed_f2_pb3` is the same literal map, but the
checker must use the independently pinned implementation, not install a
runtime alias on the producer module.

This run is a positive producer candidate but not independent production
acceptance.  A1 remains 3/4.

## 2. Surgical independent-helper repair

In the task198 checker:

1. Add the exact independent seedspan helper above to `PINS` and to the
   path-sorted normalized `DEPENDENCY_CONE`; update the exact member count.
2. In `reconstruct_roster`, keep the current producer-side arithmetic module
   solely for `reconstruct_quotients`, `cheap_context_registry`, and the
   later bridge runtime returned as `rebuilt["old"]`.
3. Load the new checker-side helper under a distinct fresh module name and
   pass that checker helper, not the producer arithmetic module, to both
   `task157ee_checker.JointGroup` and
   `task157ee_checker.factor_presentation`.
4. Require before the large construction that both implementations expose
   their expected functions and agree on at least the fixed nonpalindromic
   signed probe `[1,-2,1,2]`.  This probe is only an orientation/type canary;
   do not replace any full reconstruction or factor-order check by it.
5. Return the producer-side arithmetic module unchanged as `rebuilt["old"]`
   so every existing fine-deletion/bridge replay remains byte-for-byte in the
   same convention.

Do not import the task198 producer, share producer state IDs, weaken the
alternate traversal, or remove any exact 6,441-row, factor-order, deletion,
bridge, mutation, resource, or receipt predicate.

Update the driver dependency cone and pins for the new independent helper,
and refresh only identities forced by this task.

## 3. SELFTEST reachability canary

The old toy SELFTEST did not reach the production helper mismatch.  Add a
small checker-owned dependency bridge canary to the existing checker SELFTEST
which loads the two pinned helper modules under distinct fresh names and
checks the same nonpalindromic probe equality and callable/key availability.
It must not enumerate Q0, Gamma, the 6,441 rows, or call SymPy.  Preserve the
existing full toy receipt, 44 mutations, verdict, and exact terminal marker.

## 4. Producer capture mode

The failed run's positive receipt was lost because the generic artifact step
was skipped after checker failure.  Extend only the existing GAP driver with
a third exact mode:

```text
PRODUCER_CAPTURE
```

Requirements:

- all production input/manifest pins and optional resume-pair checks applying
  to `PRODUCTION` also apply to `PRODUCER_CAPTURE`;
- run the exact unchanged production producer command with the same resource
  caps and output paths;
- do not launch the checker in this mode;
- require exactly one producer terminal from the unchanged vocabulary
  `ROOF_BRIDGE_ISOMORPHISM|UNKNOWN_RESOURCE|UNKNOWN_INPUT`;
- require a nonempty producer receipt, write the exact terminal file and final
  sentinel, and return driver success so `ci/out` is uploaded even for a
  typed resource/input capture;
- print a distinct final marker containing
  `mode=PRODUCER_CAPTURE terminal=<exact terminal>`;
- never describe capture success as independent acceptance;
- preserve SELFTEST and PRODUCTION behavior, commands, predicates, and
  positive-only final production gate;
- driver remains ASCII-only.

## 5. Delivery

Audit all uses of the two old-module objects in `reconstruct_roster` and state
which object is used at each call.  Record exact final byte counts and SHA-256
identities for producer, checker, driver, fixture, the new independent helper,
and reply (reply may omit its self-referential SHA).  Leave all execution
status `UNEXECUTED`.

End with:

```text
TASK198 INDEPENDENT F2->PB3 HELPER:             REPAIRED STATICALLY
TASK198 PRODUCER CAPTURE MODE:                  IMPLEMENTED STATICALLY
FULL PRODUCER+INDEPENDENT CHECKER SELFTEST:     NOT EXECUTED BY LUNA
ACTUAL PRODUCER CAPTURE RERUN:                  NOT EXECUTED BY LUNA
ACTUAL INDEPENDENT PRODUCTION ACCEPTANCE:       NOT OBTAINED
A1 / ACTUAL K / COMPATIBLE LIFT / IHARA:        NOT DECLARED
```

`TASK283_TASK198_INDEPENDENT_EMBED_AND_CAPTURE_COMMISSIONED`
