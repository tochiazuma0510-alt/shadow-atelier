# Luna task 157db — fail-closed GHA driver for frozen 157da

Date: 2026-08-18

## Role and scope

You are Luna. Implement only the thin GHA driver needed to run the already
frozen 157da producer and its independent Python checker in the same generic
`gap-run.yml` job. Do not alter the 157da producer, checker, reply, any workflow,
or any mathematical predicate.

Authorized files only:

1. `search/d972_b345_q3_gha_driver_v1.g`
2. `sol/luna_reply_157db_b345_q3_gha_driver.md`

No local GAP, Python, Git, GHA, package install, or heavy computation. Static
inspection only. Follow `AGENTS.md`.

## Frozen inputs

The driver must fail closed on exact SHA256:

```text
search/d972_b345_q3_chief_v1.g
  46827beb2b3cd93a9b29f9431b76ffc9626f7d40307dc2a6733f6900fa955b32
search/check_d972_b345_q3_chief_v1.py
  9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```

Use `HexSHA256(StringFile(path))`. Do not pin a mutable branch or download any
content.

## Exact two-mode contract

The generic workflow supplies exactly one of the producer's existing flags in
its preamble.

### Canary

```gap
D972_B345_Q3_SELFTEST:=true;;
```

The driver must:

1. reject if `D972_B345_Q3_RUN=true` is also bound;
2. `Read` the frozen producer, thereby running its self-test;
3. invoke exactly once, with a fixed command and no interpolated user input,
   `python3 -B search/check_d972_b345_q3_chief_v1.py --self-test`;
4. capture stdout+stderr in `ci/out/d972_b345_q3_checker_selftest.log`;
5. create a fixed success-sentinel file only after Python exits zero;
6. require the sentinel and exactly one
   `D972_B345_Q3_CHECKER_SELFTEST_PASS` marker in the captured log;
7. echo the captured log and print exactly one final
   `B345_Q3_GHA_DRIVER_PASS mode=selftest` marker.

### Full

```gap
D972_B345_Q3_RUN:=true;;
D972_B345_Q3_OUTPUT:="ci/out/d972_b345_q3_chief_v1.json";;
```

The driver must:

1. reject if the self-test flag is also true;
2. require the output path to be bound and exactly the fixed path above;
3. `Read` the frozen producer, thereby running the full construction;
4. require the artifact file to exist and be nonempty;
5. invoke exactly once, with a fixed command and no interpolated user input,
   `python3 -B search/check_d972_b345_q3_chief_v1.py ci/out/d972_b345_q3_chief_v1.json`;
6. capture stdout+stderr in `ci/out/d972_b345_q3_checker_full.log`;
7. create a distinct fixed success sentinel only after Python exits zero;
8. require the sentinel and exactly one `B345_Q3_CHECKER_PASS` marker;
9. echo the checker log and print exactly one final
   `B345_Q3_GHA_DRIVER_PASS mode=full artifact_sha256=<digest>` marker.

If neither mode is selected, error. Treat a bound flag with value other than
literal `true` as not selected; still require exactly one selected mode.

## Shell/status safety

- Commands and paths are fixed literals; do not insert a preamble value into a
  shell command.
- Remove only the four exact checker log/sentinel paths before their mode runs,
  so stale files cannot pass a rerun. Do not use recursive deletion or globs.
- A checker failure must leave no success sentinel and must cause GAP `Error`.
- The checker log must be printed back to the GAP log whether it passes or fails
  as far as the available GAP/shell control permits.
- Implement a tiny literal substring-occurrence counter in GAP and require
  exactly one marker, not merely `PositionSublist <> fail`.
- The full receipt's terminal token remains checker-owned; the driver must not
  reinterpret `EXACT_WITH_WORD_CORRECTION`, `MISSING_TYPED_D2`, or
  `UNKNOWN_RESOURCE`.

## Static audit and reply

Statically check balanced GAP delimiters/strings as far as possible without
executing GAP. In the reply report:

- final driver SHA256 and byte count;
- the two frozen input SHA pins;
- exact generic-workflow dispatch inputs for canary and full;
- expected driver/checker markers and artifact paths;
- explicit statement that workflow and mathematical files were untouched.

Terminal implementation token:

```text
B345_Q3_GHA_DRIVER_READY
```
