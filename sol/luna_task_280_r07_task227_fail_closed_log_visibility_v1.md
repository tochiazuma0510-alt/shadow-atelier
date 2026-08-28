# Luna task 280 - task227 fail-closed log visibility v1

Commissioner: Sol / 2026-08-28

Reply by appending a dated task280 section to
`sol/luna_reply_227_r07_typed_single_seed_consumer_v2.md`.

Role: bounded mechanical driver repair only. Do not run Python, Node, GAP,
git, GHA, or network locally. Parent Sol owns mathematics and execution.

Read this commission, the current task227 GAP driver, and the current reply
in full. Edit only:

```text
search/d972_r07_typed_single_seed_endpoint_consumer_gha_driver_v2.g
sol/luna_reply_227_r07_typed_single_seed_consumer_v2.md
```

Do not change producer, checker, fixture, proof, ledger, workflow, or any
predecessor file.

## 1. Authenticated hidden-terminal failure

GHA run `33152004591` at immutable head
`ebb6c5915b78f6cddf6407d72cc0801253b66116` passed the previous checker
decoder crash, but the driver ended only with `Error, task227: sentinel`.
Because the unchanged producer had reached the checker in the preceding run,
the next hidden gate is inferred to be the checker terminal grep; the exact
redirected reason is not observable from this failed run. The workflow
skipped artifact upload, so the driver must expose the relevant log rather
than turn this inference into a claim.

This is not a mathematical terminal and A3 remains 0/3.

## 2. Exact diagnostic repair

Keep every current exact terminal count/equality test and the final sentinel.
For both SELFTEST and PRODUCTION, make every producer/checker terminal `grep`
and producer-versus-checker terminal equality failure print the relevant
existing producer/checker log(s) before returning nonzero. It is acceptable
to use a small shell helper emitted into the existing command script, or
explicit `|| { cat ...; exit 1; }` clauses.

Requirements:

- successful execution remains serial and prints no extra receipt contents;
- failure remains fail-closed and returns nonzero;
- a checker typed-UNKNOWN reason is visible in the GHA job log;
- producer/checker terminal disagreement prints both logs;
- no accepted terminal vocabulary, pin, path, command order, or sentinel is
  weakened or removed;
- driver remains ASCII-only.

The producer/checker/fixture pins are unchanged because those files must
remain byte-for-byte unchanged.

## 3. Delivery

Record exact final byte counts and SHA-256 identities for producer, checker,
driver, fixture, and reply (reply may omit its self-referential SHA). Leave
the result `UNEXECUTED`; parent Sol will rerun on GHA.

End with:

```text
TASK227 FAIL-CLOSED LOG VISIBILITY:             REPAIRED STATICALLY
FULL PRODUCER+INDEPENDENT CHECKER SELFTEST:     NOT EXECUTED BY LUNA
ACTUAL TASK226 PACKAGE / A3 GATE:               NOT OBTAINED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:         NOT DECLARED
```

`TASK280_TASK227_FAIL_CLOSED_LOG_VISIBILITY_COMMISSIONED`
