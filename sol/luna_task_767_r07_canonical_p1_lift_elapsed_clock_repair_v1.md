# Luna Task 767 — canonical P1 lift exact elapsed-clock repair

Role: Luna implementation only. Process all numbered sections in order.
This is the single finite repair prescribed by independent Task764. Do not
redesign arithmetic, provenance, resources, or workflow structure. Do not use
git, GHA, es7ops, another agent, or real parent artifacts. Modify only the
three designated outputs in section 5.

## 1. Read the exact boundary

Read in full:

1. `sol/sol_reply_764_audit_r07_canonical_p1_degree2_lift_v4_workflow_v1.md`
2. `search/d972_r07_canonical_p1_dag_degree2_lift_v4.py`
3. `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v1.yml`

The accepted raw workflow receipt remains fixed at 2,310 bytes / SHA-256
`323ca2603b9ff7c42449fc0e2421c190eedcd7cd62471b695dee991fb1b728eb` and
contains `checker_process.elapsed_wall_clock="03.76"`. Do not regenerate or
normalize it.

## 2. Versioned one-function repair

Create producer v5 from v4. Change only the provenance/version plumbing and
`validate_elapsed_clock` plus its bounded fixtures. The validator must accept
the exact one-field finite nonnegative seconds spelling `03.76` while still
rejecting empty, nonnumeric, nonfinite, negative, malformed multi-field, and
out-of-range minute/second spellings. Preserve the current accepted colon
forms. Exercise the exact historical `03.76` value through
`validate_checker_workflow_receipt`, not only the isolated parser.

All 8,059-row recurrence, character/actor maps, packet projection, packed
cache, instruction generation, resource behavior, and accepted receipt pins
must remain AST-identical to v4. Do not perform the optional raw-body cleanup;
it is nonblocking and outside this repair.

## 3. Versioned workflow

Create workflow v2 from v1 and mechanically pin the exact v5 bytes/SHA/LF.
Use the exact push fire token
`[fire-r07-canonical-p1-degree2-lift-v2]`. Rename/version the producer
executable and launch/final manifest keys/schemas wherever required so the
new bytes have honest ancestry. Preserve every accepted run/artifact/hash,
all acquisition and output gates, serial execution, 37/38/45-minute caps,
8-GiB cap, and always-uploaded diagnostics. Do not add a lift checker,
connection pass, retry, or heavy test.

## 4. Bounded checks

Run only sequential local checks with bytecode/temp output outside the repo:
py_compile, producer selftest, exact v4-to-v5 AST diff, YAML parse and inline
Python AST. Confirm the arithmetic AST delta is empty and `03.76` reaches the
same production workflow-receipt validator successfully. Record exact
runtimes, bytes/SHA/LF and rejection count.

## 5. Designated outputs

Create only:

1. `search/d972_r07_canonical_p1_dag_degree2_lift_v5.py`
2. `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v2.yml`
3. `sol/luna_reply_767_r07_canonical_p1_lift_elapsed_clock_repair_v1.md`

End with:

`CANONICAL_P1_LIFT_V5_CLOCK_REPAIR=IMPLEMENTED_CANDIDATE`

`SAFE_FOR_NARROW_REAUDIT=yes`

`ACTUAL_8059_ROW_LIFT_REPLAY=NOT_RUN`

`verified=false`
