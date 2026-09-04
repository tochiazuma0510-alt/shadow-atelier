# Luna Task913 -- minimal repair of actual R07 root-scalar batch v1

## 1. Scope

Read Task908 and the complete Sol(max) Task912 reply.  Repair only:

1. `search/d972_r07_actual_grade2_root_scalar_batch_v1.py`;
2. `search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py`;
3. `sol/luna_reply_908_r07_actual_root_scalar_batch_v1.md`.

Do not change the workflow or any other file.  Do not run/download actual
parents, GHA or git.  This is a bounded checker/selftest repair, not a rewrite
of the accepted scalar evaluator.

## 2. Complete output comparison

In checker `check_output`, reconstruct the complete expected terminal,
result and manifest objects and require exact equality, including every
upper-claim field, terminal kind, file roster, and exact launch, separator,
P1 and Task712 parent joins.  Reject unchecked additional fields.  A
coherently resealed false Grade2/A0/COMMON/cofinal/fake/Ihara claim, wrong
launch or wrong parent join must fail.

## 3. Executed bounded controls

Replace each literal selftest-success label with a control that actually ran.
At minimum exercise:

- separator sealed-field mutation rejection;
- Task712 transpose/table mutation rejection;
- P1 truncation or manifest/file-digest mutation rejection;
- Task554 expression/order mutation rejection;
- zero-root and all-four-root-EOF terminal logic;
- seed-first and actor-first violation order;
- a complete 32,280-origin scalar EOF scan using tiny values;
- the actual two-block/four-slot accumulator traversal against a direct
  independent reference;
- coherently resealed relation, child, scalar-prefix, terminal-claim and
  result-join mutations through the checker.

Use existing validators and evaluator functions wherever possible.  Generic
hash inequalities, duplicated expressions, and returned `True` constants do
not count.  Keep both public selftests at seconds scale; no large matrix,
parent data, 504-orbit scan or Python 110-million-term loop.

## 4. Receipts

Run `py_compile` and both public selftests.  Update the Task908 reply with
exact bytes/LF/SHA-256 and end with `READY_FOR_SOL_REAUDIT=yes`.  Preserve all
conservative claim boundaries and `verified=false`.
