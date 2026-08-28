# Luna reply 301 - task299/v5 adversarial static audit

## Verdict

**REJECT (static audit).**  The v5 producer cannot pass its own 19-mutation
SELFTEST gate.  This is an implementation rejection, not an A5/A6 result.
Task299/v5 paths were not modified.  No Python, Node, GAP, GHA, git, or
network command was run; status is **UNEXECUTED**.

## Audited identities

```text
producer  11068  3aa70565ba899f575ccc7e3dfd721b0f2125704b407eb9ed39e5f652654172cd
checker   20176  27bcd293b1a00ba1c9287d82adc77e955eea2c3e1b36f9b2badead2879d3ffe6
driver     3815  02fdf7d6656471871e3cd18ba83c5cf7925b480b6e48a63ddff05e98ec6a4796
fixture   10313  b2435019aaaf69321635a2d2ed8fd25400775dda90a6a619f8143c4535887525
task299 reply 1759  07d6b8b70d91397952c2b19a7c5a3f238722adbc957e4290ab4f23b21b4db4c7
task301 reply  [self-referential SHA intentionally omitted]
```

## Fatal mutation-path finding

`search/d972_r07_joint_slice_kernel_general_v5.py:98-121` mutates the case
selected at `:133`, namely `f["cases"][1]` (`outside-nonmember`).  For owner
`terminal`, `:118` sets `c["terminal"] = "MUTATED"`.  In `compile_case`:

* `:91` computes `expected = case["terminal"] == "MEMBER"`, hence `False`;
* the unchanged outside case is semantically nonmember, so `is_member` is
  also `False` and that check passes;
* `:95-97` constructs a valid nonmember dual and returns a result whose
  terminal is still the unchecked string `"MUTATED"`.

Therefore `mutate(..., "terminal")` returns a non-`None` result and records
`accepted=True`.  The producer's `:134` requirement
`not any(x["accepted"] for x in controls)` must then raise.  The producer
does not enforce the terminal enum `{MEMBER, NONMEMBER}` before using it as a
Boolean discriminator.  This alone makes the required 19/19 producer gate
unattainable.

The checker independently catches this receipt mutation: its replay requires
the receipt terminal to equal both the case terminal and the canonical
`MEMBER`/`NONMEMBER` value (`crosscheck/...v5.py:137-138`).  That does not cure
the producer-side failure, which occurs first in the driver.

## Requirement-by-requirement trace

* **Boolean repair / all `require` calls - PASS statically.** Producer
  `:52-55` and checker `:85-87` use `ok is not True`; the audited call sites
  supply comparisons, `all`/`any`, `isinstance`, or explicit `bool(duals)`.
  The v4 failing string seal predicate is replaced by explicit string type and
  literal equality at producer `:56-60` and checker `:247-251`.

* **Fixture seal canary - PASS producer-side, limited checker-side.** Producer
  `:122-127` changes the seal to a wrong nonempty string and requires
  `validate_fixture` to reject it.  Checker requires the literal seal at
  `:247`; it has no separately executed wrong-seal mutation canary.

* **`d` versus `3^d-1` - PASS.** Producer emits basis dimension and the
  separate `3**len(nvec)-1` field at `:88-97`.  Checker independently
  reconstructs the full kernel and checks `len(kernel)+1 == 3**len(receipt_kernel)`
  at `:154-161`, then reports the two quantities separately at `:175`.

* **Five cases - PASS structurally.** Fixture contains the five named cases
  and expectations (`fixture:6-12`); producer requires five at `:57`, and
  checker requires five and replays all five at `:248-263`.

* **Nineteen mutations - REJECT overall because of the fatal terminal path.**
  The roster is exactly the 19-owner list (`producer:14`, `fixture:14`,
  `checker:16`).  Producer executes all owners at `:132-134`; checker executes
  an independent owner-by-owner set at `:264-269`.  The producer's terminal
  owner is nevertheless accepted as described above.

* **Plural seeds and named actions - PASS structurally.** The first fixture
  case has two seeds and distinct `m`/`n` actions (`fixture:8`).  Producer
  starts every seed and traverses every named action (`producer:79-87`), while
  checker rebuilds the queue and traverses the action list in reverse order
  (`checker:112-127`), providing an independent order.

* **Zero-dimensional canary - PASS structurally.** `zero-nonmember` has
  zero-dimensional `D`, a nonzero `C` row, expected `kernel_dim=0` and
  `full_nonzero_kernel_cardinality=0` (`fixture:6,11`).  Both producer and
  checker retain the empty left-kernel basis and check its cardinality.

* **Independent producer/checker mathematics - PASS structurally.** Checker
  has its own vector, rank, closure, left-kernel, and membership code; it does
  not import the producer (`checker:92-175,177-206,269,281`).  Its mutation
  oracle uses `independent_terminal` and receipt replay, while explicitly
  ignoring producer mutation controls (`:267-269`).

* **Terminal, receipt, and ancestry replay - PASS for checker coverage.**
  Checker validates receipt digest (`:252-258`), all five replay results,
  terminal semantics and receipt terminal (`:137-144`), typed rows and seed /
  action ancestry (`:145-153`), kernel/Hd1 content, member equations, and
  nonmember dual equations (`:154-175`).

* **Driver binding - partial only.** Byte/SHA pins and stale-output rejection
  are present (`driver:15-19`), and fixed producer/checker terminal lines are
  grepped in production (`:28-31`).  The driver does not explicitly compare
  producer and checker terminal values for equality; it checks two independent
  fixed strings.  This is an additional audit limitation if terminal equality
  is required by the follow-up contract.

## Scope and status

This is an independent static audit of task299/v5 against the supplied
follow-up requirements and the task296/v4 fixture-seal failure.  It makes no
mathematical or execution claim.  **Actual A5/A6 count: zero; not counted.**

`TASK301_R07_TASK299_V5_STATIC_AUDIT_REJECT_UNEXECUTED`
