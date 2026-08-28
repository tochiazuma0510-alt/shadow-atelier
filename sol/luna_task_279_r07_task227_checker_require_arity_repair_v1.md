# Luna task 279 - task227 checker require-arity repair v1

Commissioner: Sol / 2026-08-28

Reply by appending a dated task279 section to
`sol/luna_reply_227_r07_typed_single_seed_consumer_v2.md`.

Role: bounded mechanical implementation repair only. Do not run Python,
Node, GAP, git, GHA, or network locally. Parent Sol owns mathematics,
execution, and repository brokerage.

Read this commission, the current task227 checker and driver, and the current
task227 reply in full. Edit only:

```text
crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py
search/d972_r07_typed_single_seed_endpoint_consumer_gha_driver_v2.g
sol/luna_reply_227_r07_typed_single_seed_consumer_v2.md
```

Do not change the producer, fixture, proof, ledger, workflow, or predecessor
files.

## 1. Authenticated failure

GHA run `33151329705` at immutable head
`ce273e5c56b9162bde44378ea8f82a7f5dee39ea` reached the independent checker
after the producer completed its full SELFTEST. The checker stopped before a
mathematical terminal at:

```text
check_d972_r07_typed_single_seed_endpoint_consumer_v2.py line 59
block_decode
require(type(value) is list)
TypeError: require() missing 1 required positional argument: 'msg'
```

Classify this as an implementation failure, not MEMBER, NONMEMBER, resource,
or mathematical rejection. A3 remains 0/3.

## 2. Exact repair and complete arity audit

Give the located `block_decode` type guard a stable nonempty diagnostic
message. Preserve the strict `require(ok,msg)` implementation and all
mathematical predicates.

Then statically audit every call to the checker's local `require` function.
Every call must supply exactly two positional arguments and no keyword
arguments. Repair any further arity defect found, but do not rename or weaken
already valid gates. Report the complete list of changed call sites. If the
located call is the only defect, state that explicitly.

Do not perform a global truthiness rewrite. In particular, do not alter any
dual, remainder, membership, span, ancestry, mutation, resource, or terminal
condition except insofar as an actually malformed `require` call cannot be
invoked.

## 3. Delivery

Refresh only the checker pin in the serial GAP driver. Record exact final
byte counts and SHA-256 identities for producer, checker, driver, fixture,
and reply (the reply may omit its self-referential final SHA). Leave the
result `UNEXECUTED`; parent Sol will rerun the full serial GHA SELFTEST.

End with:

```text
TASK227 CHECKER REQUIRE ARITY:                 REPAIRED STATICALLY
FULL PRODUCER+INDEPENDENT CHECKER SELFTEST:    NOT EXECUTED BY LUNA
ACTUAL TASK226 PACKAGE / A3 GATE:              NOT OBTAINED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:        NOT DECLARED
```

`TASK279_TASK227_CHECKER_REQUIRE_ARITY_REPAIR_COMMISSIONED`
