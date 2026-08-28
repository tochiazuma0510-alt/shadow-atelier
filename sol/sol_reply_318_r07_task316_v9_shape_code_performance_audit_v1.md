# Sol(max) reply 318 - task316/v9 independent literal-shape, code, and performance audit

## Verdict

**REJECT / UNEXECUTED.  No synthetic GHA SELFTEST is authorized.**

The commissioned thirty base/binding pairs are now literally equal and have
their prescribed dimensions, and the five advertised arithmetic tuples can
be reconstructed from the typed `theta`, `D`, `O`, and `C` literals.  That is
not enough to execute v9.  The first exact blocker in audit order is driver
line 15: the fixture SHA pin has only 63 hex digits and omits the `b` after
`...afc`.  The pin is

```text
6a866e980422afc405c4d6b574c06cee8ca8ee6792b536a006e4d104724c7cd
```

whereas the current fixture SHA-256 is

```text
6a866e980422afcb405c4d6b574c06cee8ca8ee6792b536a006e4d104724c7cd
```

Thus `D307Pin` necessarily raises `task304 pin drift` before the stale-output
gate or either program invocation.

There is a second independent load-bearing blocker behind that pin.  The
first case's first action has `eta_matrix` row lengths
`11,11,11,11,11,11,10,10,11,11,11`; producer line 105 therefore raises
`RuntimeError("matrix")` in the first `compile_case`.  Five of the six actions
have ragged `eta_matrix` rows.  These action matrices are not among the six
base/binding pairs checked by the new preflight, so the preflight passes and
then the first baseline compilation fails.  Producer mutations, the producer
wrong-seal canary, and every checker replay/mutation are consequently
unreachable from the literal SELFTEST input.

No Python, Node, GAP, GHA, git, workflow, or network command was run.  The
only parsing was read-only PowerShell `ConvertFrom-Json`; byte identities used
`Get-Item`, `Get-FileHash`, and read-only .NET byte/string reads.

## 1. Current identities, schemas, paths, pins, and driver gates

Independent identities of all five commissioned v9 files are:

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_joint_slice_kernel_general_v9.py` | 13001 | `1e38453980eac5dc4b3b8edcb63235a7de60684393491a5bc01cdd356f4d103a` |
| `crosscheck/check_d972_r07_joint_slice_kernel_general_v9.py` | 24995 | `5cadaeb180e2058466a9a97bb54c5b98393e2e4096035f4e64b69a65d0da8121` |
| `search/d972_r07_joint_slice_kernel_general_gha_driver_v9.g` | 4860 | `be0f1d75e7ea3d4814cf234dd00b59e4e1def0745e1d1094170e0b3c18ba9859` |
| `search/certs/d972_r07_joint_slice_kernel_general_selftest_v9_20260828.json` | 10356 | `6a866e980422afcb405c4d6b574c06cee8ca8ee6792b536a006e4d104724c7cd` |
| `sol/luna_reply_316_r07_task307_all_case_fixture_repair_v9.md` | 3137 | `6b89d442b7188eb4d93fb979aeb09d02f43d2ff2f2bc64b439e15047a4175684` |

The Luna reply's self-length claim, 3137, is exact.  Its assertion that the
driver pins all three inputs to the displayed identities is false for the
fixture.  The producer and checker pin rows match exactly; the fixture byte
pin `10356` matches but its digest pin is the 63-digit string above.

The driver contains zero non-ASCII bytes.  The producer, checker, fixture,
driver input/output paths, schemas, seal `literal-static-fixture-v9`, v9
SELFTEST success strings, v9 sentinel, and production terminal
`STATIC_BLOCKED:actual typed matrices are not staged` are internally named as
v9.  Driver line 19 has the six-way stale-output rejection and lines 25, 28,
34, 35, and 38 use full-line `grep -Fxc ... = 1` exact-one gates.  These gates
are syntactically present but are not reachable past the bad pin.

## 2. Independent five-case literal shape enumeration

The exact PowerShell command used from the repository root to enumerate the
six pairs was:

```powershell
$j = Get-Content -LiteralPath 'search/certs/d972_r07_joint_slice_kernel_general_selftest_v9_20260828.json' -Raw -Encoding UTF8 | ConvertFrom-Json
$pairs = @(@('A_theta','A_theta_binding'),@('A_Z','A_Z_binding'),@('A_E','A_E_binding'),@('D','D_binding'),@('O','O_binding'),@('C','C_binding'))
foreach ($case in $j.cases) {
  "CASE $($case.name)"
  foreach ($pair in $pairs) {
    $left = $case.($pair[0]); $right = $case.($pair[1])
    $ldims = "$($left.Count)x$(@($left[0]).Count)"
    $rdims = "$($right.Count)x$(@($right[0]).Count)"
    $llens = (@($left | ForEach-Object { @($_).Count }) -join ',')
    $rlens = (@($right | ForEach-Object { @($_).Count }) -join ',')
    $equal = (($left | ConvertTo-Json -Depth 20 -Compress) -ceq ($right | ConvertTo-Json -Depth 20 -Compress))
    "$($pair[0])=$ldims rows[$llens] | $($pair[1])=$rdims rows[$rlens] | literal_equal=$equal"
  }
}
```

The required casewise `A_E` table is:

| case | `A_E` rows | all `A_E` row lengths | `A_E_binding` rows | all `A_E_binding` row lengths | literal equality |
|---|---:|---|---:|---|---|
| `nonzero-member` | 11 | 11,11,11,11,11,11,11,11,11,11,11 | 11 | 11,11,11,11,11,11,11,11,11,11,11 | yes |
| `outside-nonmember` | 11 | 11,11,11,11,11,11,11,11,11,11,11 | 11 | 11,11,11,11,11,11,11,11,11,11,11 | yes |
| `zero-member` | 11 | 11,11,11,11,11,11,11,11,11,11,11 | 11 | 11,11,11,11,11,11,11,11,11,11,11 | yes |
| `zero-nonmember` | 11 | 11,11,11,11,11,11,11,11,11,11,11 | 11 | 11,11,11,11,11,11,11,11,11,11,11 | yes |
| `post-c-cancel` | 11 | 11,11,11,11,11,11,11,11,11,11,11 | 11 | 11,11,11,11,11,11,11,11,11,11,11 | yes |

Both sides of every other pair, with equality checked on the literal nested
lists rather than inferred from dimensions, are:

| case | `A_theta / binding` | `A_Z / binding` | `D / binding` | `O / binding` | `C / binding` |
|---|---|---|---|---|---|
| `nonzero-member` | 2x2 / 2x2, equal | 2x2 / 2x2, equal | 2x2 / 2x2, equal | 11x2 / 11x2, equal | 1x11 / 1x11, equal |
| `outside-nonmember` | 2x2 / 2x2, equal | 2x2 / 2x2, equal | 2x2 / 2x2, equal | 11x2 / 11x2, equal | 1x11 / 1x11, equal |
| `zero-member` | 2x2 / 2x2, equal | 2x2 / 2x2, equal | 2x2 / 2x2, equal | 11x2 / 11x2, equal | 1x11 / 1x11, equal |
| `zero-nonmember` | 2x2 / 2x2, equal | 2x2 / 2x2, equal | 2x2 / 2x2, equal | 11x2 / 11x2, equal | 1x11 / 1x11, equal |
| `post-c-cancel` | 2x2 / 2x2, equal | 2x2 / 2x2, equal | 2x2 / 2x2, equal | 11x2 / 11x2, equal | 1x11 / 1x11, equal |

Therefore all 30 commissioned base/binding equalities pass literally.  This
does not imply that every matrix subsequently checked by `compile_case` is
well shaped.  The exact second parser command used for action matrices was:

```powershell
$j=Get-Content -LiteralPath 'search/certs/d972_r07_joint_slice_kernel_general_selftest_v9_20260828.json' -Raw -Encoding UTF8 | ConvertFrom-Json
foreach($case in $j.cases){
  foreach($action in $case.actions){
    $tm=$action.theta_matrix;$zm=$action.z_matrix;$em=$action.eta_matrix
    "case=$($case.name) action=$($action.name) theta=$($tm.Count)x$(@($tm[0]).Count) rows[$(@($tm|ForEach-Object{@($_).Count})-join ',')] z=$($zm.Count)x$(@($zm[0]).Count) rows[$(@($zm|ForEach-Object{@($_).Count})-join ',')] eta=$($em.Count)x$(@($em[0]).Count) rows[$(@($em|ForEach-Object{@($_).Count})-join ',')]"
  }
}
```

It gives the following complete action-shape table.  Every theta and Z action
is 2x2 with row lengths `2,2`; the load-bearing eta results are:

| case | action | eta row count | all eta row lengths | required |
|---|---|---:|---|---|
| `nonzero-member` | `m` | 11 | 11,11,11,11,11,11,10,10,11,11,11 | **FAIL** |
| `nonzero-member` | `n` | 11 | 11,11,11,11,11,11,11,11,11,11,11 | pass |
| `outside-nonmember` | `m` | 11 | 11,11,11,11,11,11,10,10,11,11,11 | **FAIL** |
| `zero-member` | `m` | 11 | 11,11,11,11,11,11,10,10,11,11,11 | **FAIL** |
| `zero-nonmember` | `m` | 11 | 11,11,11,11,10,10,10,10,11,11,11 | **FAIL** |
| `post-c-cancel` | `m` | 11 | 11,11,11,11,11,11,10,10,11,11,11 | **FAIL** |

The first literal compile failure is zero-based row 6 of
`nonzero-member/actions[0]/eta_matrix`, length ten where producer line 105
requires an 11x11 matrix.

## 3. Semantic and bytewise v8-to-v9 audit

The load-bearing v8/v9 byte accounting is:

| file | v8 bytes | v9 bytes | literal delta |
|---|---:|---:|---|
| producer | 12999 | 13001 | +2 |
| checker | 24993 | 24995 | +2 |
| driver | 4860 | 4860 | 0 net |
| fixture | 10322 | 10356 | +34 |

Semantic JSON comparison was done by parsing both fixtures, changing only the
v9 schema/seal back to v8, and removing the final entry of rows 6 and 7 from
`A_E` and `A_E_binding` in exactly the four named cases.  The resulting object
is exactly equal to the parsed v8 object.  In particular, all five expected
objects, targets, terminals, action names and order, other matrices, mutation
roster, and case order are unchanged.  A greedy byte alignment after the
schema/seal normalization found exactly sixteen `,0` insertions, consuming
all 10322 v8 bytes at v9 offset 10354, followed by two additional `0a` bytes.

The sixteen data insertions are the commissioned repair.  The EOF bytes are
not.  There are further byte-scope violations:

- After mapping `v9/V9` back to `v8/V8`, the entire v9 producer is the v8
  producer followed by two extra `0a` bytes.
- The same comparison for the checker gives the v8 checker followed by two
  extra `0a` bytes.
- Constructing the expected v9 driver from v8 using only version/path and the
  three exact current byte/SHA pins differs from the actual driver in exactly
  two places: the fixture pin deletes the `b` described in the verdict and an
  extra final `0a` is appended.  Inserting that `b` and deleting the last LF
  makes it byte-for-byte equal to the authorized construction.
- The fixture has the authorized 32 bytes from sixteen literal `,0`
  insertions plus two unauthorized EOF LF bytes.

Thus the fixture's semantic repair scope is exact, but the commissioned
**bytewise** scope is not.  The ragged action matrices are unchanged from v8,
so they are not an extra v8-to-v9 data edit; they are an inherited execution
defect exposed after the repaired preflight.

## 4. Independent reconstruction of the five expected tuples

Write `e1=(1,0)` and `e2=(0,1)` over `F_3`.  The tuple columns below are
closure rank, coefficient-kernel dimension, complete nonzero coefficient
enumeration, post-C `Hd1` space/rank, and terminal evidence.  This calculation
uses the literal theta seeds/actions and `D,O,C`; it does not waive the
separate malformed action-matrix type gate.

| case | closure and coefficient kernel | nonzero coefficients | post-C / terminal evidence | expected tuple |
|---|---|---|---|---|
| `nonzero-member` | Seeds `e1,e2` give closure rank 2.  Both C-images vanish, so `K=F_3^2`, dim 2. | `(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)`; 8 total. | `Hd1=<e1,e2>`, rank 2. Target `(1,1)` uses kernel coefficients `(1,1)` and has MEMBER ancestry theta `(1,1)`. | `(2,2,8,2,MEMBER,[1,1],null)` |
| `outside-nonmember` | The one seed gives closure rank 1; its C-image is 0, so `K=F_3`, dim 1. | `(1),(2)`; 2 total. | `Hd1=<e1>`, rank 1. Target `e2` is outside. Dual `(0,1)` annihilates `e1` and pairs to 1 with `e2`. | `(1,1,2,1,NONMEMBER,null,[0,1])` |
| `zero-member` | The eta component makes the one flat row nonzero, so closure rank 1.  Its C-image is 0, hence kernel dim 1. | `(1),(2)`; 2 total. | `D=0`, so `Hd1=<(0,0)>`, rank 0.  The zero target has the lex-first zero coefficient and MEMBER ancestry theta `(0,0)`. | `(1,1,2,0,MEMBER,[0,0],null)` |
| `zero-nonmember` | The one flat row has C-image 1, so closure rank 1 but the coefficient kernel has dim 0. | empty; 0 total. | `Hd1` is empty, rank 0.  Target `e1` is outside and dual `(1,0)` pairs to 1 (with no Hd1 row to violate). | `(1,0,0,0,NONMEMBER,null,[1,0])` |
| `post-c-cancel` | Seed `e1` and swap give `e1,e2`, closure rank 2.  C-images are `(1,1)`, so `K=< (2,1) >`, dim 1. | `(2,1),(1,2)`; 2 total. | `Hd1=<(2,1)>`, rank 1.  Target `(1,2)=2(2,1)`; multiplying the kernel-basis theta by 2 gives MEMBER ancestry theta `(1,2)`. | `(2,1,2,1,MEMBER,[1,2],null)` |

All five expected objects therefore match the independent arithmetic.  They
remain static arithmetic statements only: the literal producer cannot reach
the first terminal because its preceding action shape check fails.

## 5. Preflight, mutations, seals, fail-closed behavior, and production

Producer `parse_fixture` runs validation and then the five-case/six-pair
preflight before `selftest` calls `compile_case`.  Checker `run` performs the
same preflight before loading a receipt or calling `replay`.  On the current
fixture the 30 checks all pass.  Producer then stops in case 1 at line 105;
checker replay has the same action-matrix check at line 111 (and its mutation
oracle repeats it at line 201).

Both source tuples and the fixture roster contain the same complete ordered
19-owner list:

```text
field_modulus, theta_seed, theta_action, z_action, eta_action,
D_entry, O_entry, C_entry, action_order, premature_C, target,
seed_index, parent, row_theta, left_kernel, Hd1, member_ancestry,
dual, terminal
```

The complete static mutation mapping is:

| owner | producer mutation / intended rejection | checker oracle / intended rejection |
|---|---|---|
| `field_modulus` | modulus 9 / typed modulus | `independent_terminal` / typed field |
| `theta_seed` | mutate seed / seed binding | `independent_terminal` / control binding |
| `theta_action` | mutate `A_theta` / binding | `independent_terminal` / action binding |
| `z_action` | mutate `A_Z` / binding | `independent_terminal` / action binding |
| `eta_action` | mutate `A_E` / binding | `independent_terminal` / action binding |
| `D_entry` | mutate `D` / binding | `independent_terminal` / map binding |
| `O_entry` | mutate `O` / binding | `independent_terminal` / map binding |
| `C_entry` | mutate `C` / binding | `independent_terminal` / map binding |
| `action_order` | mutate name list / order binding | `independent_terminal` / order binding |
| `premature_C` | set before-closure / phase control | `independent_terminal` / phase control |
| `target` | set outside case target to `e1` / terminal mismatch | `independent_terminal` / semantic terminal mismatch |
| `seed_index` | mutate seed binding / seed equality | resealed `replay` / receipt seed index |
| `parent` | mutate `parent_hint` / control owner | resealed `replay` / receipt ancestry |
| `row_theta` | mutate seed / seed equality | resealed `replay` / typed row replay |
| `left_kernel` | change method / control owner | resealed `replay` / basis independence |
| `Hd1` | mutate C / map binding | resealed `replay` / Hd1 span equality |
| `member_ancestry` | mutate seed binding / seed equality | resealed `replay` / member equations/ancestry |
| `dual` | change case terminal / semantic mismatch | resealed `replay` / dual equations |
| `terminal` | illegal enum | resealed `replay` / receipt terminal |

For every producer owner, canonical change and mutation-fixture resealing are
required before entering the caught `compile_case` call.  For every checker
owner, canonical change, reseal, oracle reach, observed semantic exception,
and final rejection are separately required before append.  The checker
splits exactly 11 fixture owners to `independent_terminal` and 8 receipt
owners to `replay`; the receipt case-index roster supplies the required
member and nonmember shapes.  These definitions are fail-closed.

They are not semantically reachable on the current literal baseline.
Producer line 156 must finish all five baseline compilations before its
wrong-nonempty-seal canary at lines 157--160 and its 19-owner loop at line
166.  It fails in the first compilation.  The checker can run its own
wrong-seal canary after preflight, but the serial driver never has an accepted
producer receipt, and a hypothetical replay of the current first case fails
at its ragged action matrix before checker mutations.  Actual mutation counts
therefore remain 0/19 and 0/19.

Both programs define the typed production terminal exactly, and the driver
defines serial producer/checker exact-one comparisons and a sole sentinel.
The wrong fixture pin prevents even that production route from being reached
through this driver.  No production matrices are staged and no A5/A6 progress
is established.

## 6. Performance and fixed bounds

The intended SELFTEST call accounting is fixed and has no second baseline
pass:

```text
producer: 5 baseline compile_case + 19 mutation compile_case = 24
checker:  5 baseline replay + 11 fixture independent_terminal
          + 8 receipt replay                              = 24
```

Producer parses the fixture file once.  Checker parses the fixture once and
the distinct receipt once.  Mutation JSON round-trips are in-memory bounded
copies, not repeated file parses.  With the current literal data and the
driver pin bypassed, however, producer enters exactly one baseline
`compile_case`, fails at its first action eta check, and reaches zero mutation
oracles; the checker has no valid receipt.  No call was actually executed in
this audit.

The preflight performs exactly `5*6=30` deep pair equalities.  One side has
`4+4+121+4+22+11=166` scalar entries, so both sides over five cases give at
most 1660 scalar type/range checks.  Fixed dimensions are Theta 2, Z 2,
E-hat 11, E 1, and flat-row width 13.  Linear closure accepts at most two
rows.  With at most two seeds and two actions, the queue-pop bound is
`2+2*2=6`; the five baseline literals would pop respectively `4,1,1,1,2`
rows after their action matrices were made well typed.

There is no `3^11` enumeration.  Producer `nullspace` is RREF-based;
`span_solve` and both dual searches have maximum `3^2=9`.  Checker
`left_kernel` enumerates by closure-row count, at most `3^2=9`, retaining at
most 8 nonzero vectors.  There is no unbounded retry, process pool, thread,
background subprocess, sleep, polling, or lock.  The only subprocess design
is the prescribed serial producer followed by checker in the one driver
shell.

Nevertheless the explicit no-unnecessary-echelon-rebuild condition fails.
Producer lines 111 and 116 recompute `rank(seen)`/`rank(current)` even though
the construction invariant already says every stored row is independent;
line 116 repeats the same base rank once per action.  On the five intended
baseline closures alone this builds 13 avoidable base echelons (4 in the
pre-pop test and 9 in action tests).  Checker line 120 recomputes the known
current-basis rank on every pop and line 128 recomputes the same accepted
basis rank once per action: 18 avoidable baseline base-echelons.  Checker line
142 also repeats the first producer-row containment that line 143 immediately
checks again.  These are local and bounded, but the commission explicitly
requires rejection of unnecessary echelon rebuilding.  Performance/fixed
bounds is therefore REJECT, independently of the pin and shape blockers.

## 7. Accounting and authorization

The thirty requested base/binding pairs and five arithmetic tuples pass
static inspection.  The exact driver pin, complete case schema, bytewise
repair scope, mutation reachability, and no-redundant-echelon condition do
not.  A bounded synthetic GHA SELFTEST is not authorized.  A static rejection
does not increment v220 A5/A6.

```text
TASK318/V9 LITERAL SHAPE AUDIT:             REJECT
V8->V9 EXACT REPAIR SCOPE:                  REJECT
EXPECTED TUPLES:                            5/5 STATIC
PRODUCER MUTATIONS ACTUAL:                  0/19
CHECKER MUTATIONS ACTUAL:                   0/19
PERFORMANCE / FIXED BOUNDS:                 REJECT
EXECUTION:                                  UNEXECUTED
ACTUAL A5 / ACTUAL A6:                      0/3 / 0/3
LIFT / FAKE / IHARA:                        NONE
```

`TASK318_R07_TASK316_V9_SHAPE_CODE_PERFORMANCE_AUDIT_COMMISSION`
