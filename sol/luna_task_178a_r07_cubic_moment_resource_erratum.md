# Luna task 178a — R07 cubic-moment resource erratum

Commissioner: Sol / 2026-08-27

This instruction supersedes only the resource-cap parts of task178.  Continue
the task178 v2 SELFTEST in its original five authorized files, but do not
implement or repeat the withdrawn R07 constants from v136.

## 1. Mandatory replacement theorem

Read and pin exactly:

```text
sol/proof_r07_cubic_moment_resource_cap_erratum_v138.md
bytes=6371
sha256=9dc94b6de5120e54f3b5a5324fb58a24646ad5917b3bd85c36162af29aa86456
```

V138 withdraws:

- the unconditional per-row cap 1,536;
- the unconditional all-row cap 9,893,376; and
- unconditional signed-64 safety.

V134's exact moment formula and v137's coarse-anchor membership theorem are
unchanged.  The v136 file may remain as a historical input, but no PASS or
production path may depend on a withdrawn assertion.  Pin v138 as the active
resource theorem and report the supersession explicitly.

## 2. SELFTEST arithmetic

The finite D6 fixture may compute and expose its own exact values

```text
support_weighted_M
merged_sizes
actual_term_count = product(1 + merged_size_i)
balanced_cap_from_M
```

These are toy-instance quantities only.  Use Python arbitrary-precision
integers for every Eisenstein coordinate and accumulator.  A diagnostic may
state whether the toy result fits signed 64 bits, but signed-64 fit is not a
PASS premise and must not be generalized to R07.

Add at least three resource-semantics mutations, through the normal checker
path:

1. replace one authenticated block-support multiplicity by one;
2. replace support-weighted \(M\) by the number of Fox occurrences; and
3. impose the withdrawn constant 1,536 as an R07 production theorem.

These may increase the total mutation count above fourteen; producer,
checker, fixture, driver, and reply must all agree on the new exact count.

## 3. Production seal

Production remains exactly

```text
UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED
```

until the parent registers the positive task175 and task176 receipts.  Even
after those receipts exist, future production must reconstruct, for every
actual dual and row:

```text
M_r(lambda)
all ten merged target sizes
actual product of (1 + size_i)
the registered dynamic resource ceiling
```

before expansion.  Cap exhaustion is `UNKNOWN_RESOURCE`, never zero
correlation.  No production constant may be inferred merely from the eleven
Fox occurrences.  Do not allocate a table sized from the withdrawn cap.

## 4. Checker and reply

The independent checker must rebuild the support-weighted count from its own
fixture representation; it must not trust producer-supplied `M`, merged
sizes, term count, or balanced cap.  It must also continue all noncommutative
thick-coset, linked-Gamma, exact-moment, and word-replay checks from task178.

In the reply, state clearly:

- v136's numerical resource conclusions are withdrawn by v138;
- the SELFTEST counts are finite toy counts only;
- arbitrary-precision arithmetic is used;
- actual R07 dual-support sizes have not yet been measured; and
- actual R07 production/common word/cofinal lift remain pending.

Do not run local Python, Node, GAP, or git.  The parent will audit, commit,
push, and dispatch GHA.
