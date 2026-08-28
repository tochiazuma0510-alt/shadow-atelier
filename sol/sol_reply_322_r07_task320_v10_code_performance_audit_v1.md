# Sol(max) reply 322 - task320/v10 independent code, semantic, and performance audit

## Verdict

**REJECT / UNEXECUTED.  No synthetic GHA SELFTEST is authorized.**

The byte pins, EOF normalization, literal fixture repair, all thirty
base/binding pairs, all six stored action shapes, and all five arithmetic
tuples pass independent static reconstruction.  The first blocker in audit
order is nevertheless in the load-bearing echelon rewrite: producer lines
48--76 and checker lines 63--115 store only reduced pivot rows.  Neither
implementation stores the row-operation transform from an echelon row back
to the accepted rows.  In particular, checker `coordinates` returns
coefficients indexed by pivot *columns*, not coefficients in insertion/receipt
row order, and no code reconstructs a stored row from such coefficients.
Thus the required ancestry/change-of-basis invariant is not implemented.

Further independent blockers are:

1. The checker echelon is not an independent implementation.  Its
   `_reduce`/`add` at lines 73--92 is the producer's `_reduce`/`insert` at
   lines 58--76 with identifiers and normalization spelling changed.  This
   violates the explicit no-mirroring gate even though there is no import.
2. V9 checker line 145 checked `receipt["closure_rank"]` against the
   independently reconstructed rank.  V10 replaces surrounding span/rank
   work by incremental bases at lines 215--224 but drops that equality
   entirely.  The only `closure_rank` comparison in v10 is the checker's own
   result against the fixture expectation at line 477.  A resealed receipt
   with a false `closure_rank` is therefore accepted.  This is an
   unauthorized loss of replay semantics, not a performance rewrite.
3. Producer lines 224--225 classify any `RuntimeError`, `ValueError`,
   `KeyError`, or `TypeError` from the whole compile as a successful mutation
   rejection.  Checker lines 360--369 and 391--400 likewise classify any of
   five broad exception classes, including `IndexError`, as semantic success
   and do not compare the reason with an owner-specific oracle.  The task
   explicitly forbids a broad swallowed exception from counting.
4. The task318 closure rebuilds are removed, but many other known-basis RREF
   rebuilds remain.  On the five baseline cases the producer makes 13 full
   Hd1/member `rank` calls where a retained Hd1 basis needs at most one build
   per case; eight full rebuilds are avoidable.  The checker makes 72
   Hd1/member/span/ancestry RREF calls in addition to its 33 matrix
   invertibility checks.  At least 58 of those 72 are literal duplicates or
   repeated containment rebuilds.  This fails the task322 no-needless-delay
   gate.

No Python, Node, GAP, GHA, workflow, git, or network command was run.  I used
only read-only PowerShell/.NET byte reads, `Get-FileHash`, `ConvertFrom-Json`,
and read-only `fc.exe`/line source inspection.

## 1. Exact identities, byte scope, and driver

Independent current identities are:

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_joint_slice_kernel_general_v10.py` | 15310 | `54e9264ab6d1771970493c766b10601e848ec6fd432eae7f9d4e1a938753ead8` |
| `crosscheck/check_d972_r07_joint_slice_kernel_general_v10.py` | 28812 | `e186e3ec67adbb8199f78fd15f09eaa36c3e28c2954d39c3bce80648b811b739` |
| `search/d972_r07_joint_slice_kernel_general_gha_driver_v10.g` | 6417 | `6ffe5fe493627fb096387d0ac42a6f22da0351d747d52ba2997789fcd7833a1e` |
| `search/certs/d972_r07_joint_slice_kernel_general_selftest_v10_20260828.json` | 10356 | `645eac3beb37c65803d44bdd3661ddb77f757182fe257cb5809db562bc8240e9` |

For completeness, the task320 reply is 8590 bytes with SHA-256
`18f33cb63c83a2e1859ddb88aed978d0bd7704d2eaa01bdc1cd5fed720e4bbca`.
Every one of the five v10 text files has zero CR bytes and exactly one final
LF.  All four load-bearing files are ASCII; in particular the driver has zero
non-ASCII bytes.

The driver's three byte counts and all three 64-hex SHA pins equal the
identities above.  Its stale roster contains the six output names for each of
v7, v8, v9, and v10, hence 24 paths, and rejects any one before creating the
shell.  In either selected mode the generated shell invokes exactly one
producer and then exactly one checker.  SELFTEST has exact-one full-line
producer PASS, checker PASS, producer terminal, and checker terminal gates;
PRODUCTION has exact-one full-line producer/checker static terminals.  Both
branches extract and compare the terminal suffixes.  The sole `.ok` sentinel
is written only after those gates.  The exact production terminal in both
programs and the driver is

```text
STATIC_BLOCKED:actual typed matrices are not staged
```

Thus the physical byte/pin/driver gate passes.  Source semantic scope does
not pass because the v9 receipt-closure-rank equality was deleted as noted in
the verdict.

After parsing v9 and v10 independently, changing only v10's schema and seal
back to v9 and deleting the last entry of the commissioned twelve action rows
made the two JSON objects exactly equal.  Each old row had length 10, each new
row has the old row as its exact prefix and one appended integer zero, and the
edits are exactly:

```text
nonzero-member      m.eta rows 6,7
outside-nonmember   m.eta rows 6,7
zero-member         m.eta rows 6,7
zero-nonmember      m.eta rows 4,5,6,7
post-c-cancel       m.eta rows 6,7
```

No target, expected object, action/case order, nontrailing scalar, mutation
roster, or terminal moved.  V9's fixture has 27 trailing LF bytes and v10 has
one; this is precisely the commissioned EOF normalization.

## 2. Complete literal type and shape reconstruction

Every scalar below parsed as an integer and lies in `{0,1,2}`.  Literal
equality was tested on the complete nested lists, not inferred from shape.
The required case-by-case table is:

| case | `A_theta / binding` | `A_Z / binding` | `A_E / binding` | `D / binding` | `O / binding` | `C / binding` |
|---|---|---|---|---|---|---|
| `nonzero-member` | 2x2 / 2x2 equal | 2x2 / 2x2 equal | 11x11 / 11x11 equal | 2x2 / 2x2 equal | 11x2 / 11x2 equal | 1x11 / 1x11 equal |
| `outside-nonmember` | 2x2 / 2x2 equal | 2x2 / 2x2 equal | 11x11 / 11x11 equal | 2x2 / 2x2 equal | 11x2 / 11x2 equal | 1x11 / 1x11 equal |
| `zero-member` | 2x2 / 2x2 equal | 2x2 / 2x2 equal | 11x11 / 11x11 equal | 2x2 / 2x2 equal | 11x2 / 11x2 equal | 1x11 / 1x11 equal |
| `zero-nonmember` | 2x2 / 2x2 equal | 2x2 / 2x2 equal | 11x11 / 11x11 equal | 2x2 / 2x2 equal | 11x2 / 11x2 equal | 1x11 / 1x11 equal |
| `post-c-cancel` | 2x2 / 2x2 equal | 2x2 / 2x2 equal | 11x11 / 11x11 equal | 2x2 / 2x2 equal | 11x2 / 11x2 equal | 1x11 / 1x11 equal |

For every `A_E` and `A_E_binding` in all five rows, the exact row-length
list is eleven copies of 11.  For every `O` and binding it is eleven copies
of 2; the other row-length lists are respectively `2,2`, `2,2`, `2,2`, and
`11` as displayed.  Hence all 30 pairs pass literally.

All six stored actions pass the independent full scalar/shape inspection:

| case / action | theta | z | eta | all scalars |
|---|---|---|---|---|
| `nonzero-member / m` | 2 rows, lengths 2,2 | 2 rows, lengths 2,2 | 11 rows, all lengths 11 | integer F3 |
| `nonzero-member / n` | 2 rows, lengths 2,2 | 2 rows, lengths 2,2 | 11 rows, all lengths 11 | integer F3 |
| `outside-nonmember / m` | 2 rows, lengths 2,2 | 2 rows, lengths 2,2 | 11 rows, all lengths 11 | integer F3 |
| `zero-member / m` | 2 rows, lengths 2,2 | 2 rows, lengths 2,2 | 11 rows, all lengths 11 | integer F3 |
| `zero-nonmember / m` | 2 rows, lengths 2,2 | 2 rows, lengths 2,2 | 11 rows, all lengths 11 | integer F3 |
| `post-c-cancel / m` | 2 rows, lengths 2,2 | 2 rows, lengths 2,2 | 11 rows, all lengths 11 | integer F3 |

Producer `parse_fixture` calls the complete five-case preflight before
`selftest` can call `compile_case`.  Checker `run` performs its independently
spelled five-case preflight before loading/replaying the receipt or entering
the mutation loop.  Both inspect all six actions directly rather than infer
their shapes from base matrices.  A v10-schema copy of the old v9 ragged
pattern is rejected in this preflight.

## 3. Independent reconstruction of the five expected tuples

Write `e1=(1,0)` and `e2=(0,1)` over F3.  Appending a zero in columns which
were missing from the malformed action rows does not alter any first-two-
column action used by `O`, but the following was reconstructed from the
literal v10 object itself:

| case | closure and coefficient kernel | Hd1 and terminal certificate | reconstructed tuple |
|---|---|---|---|
| `nonzero-member` | Seeds `e1,e2` already give closure rank 2; `m` swaps and `n` is twice the swap.  `C=0`, so the coefficient kernel is F3^2, dimension 2, with 8 nonzero coefficients. | `D=I`, hence Hd1 is `<e1,e2>`, rank 2.  Target `(1,1)` is represented by theta `(1,1)`. | `2,2,8,2,MEMBER,[1,1],null` |
| `outside-nonmember` | The single `e1` seed and identity action give rank 1.  `C=0`, so kernel dimension 1 and nonzero count 2. | Hd1 is `<e1>`, rank 1.  Target `e2` is outside; `(0,1)` annihilates Hd1 and pairs to 1 with the target. | `1,1,2,1,NONMEMBER,null,[0,1]` |
| `zero-member` | The flat row is nonzero through `O(e1)`, so closure rank 1.  `C=0`, giving kernel dimension 1 and nonzero count 2. | `D=0`, so Hd1 rank is 0.  The zero target has lex-first coefficient zero and theta ancestry `(0,0)`. | `1,1,2,0,MEMBER,[0,0],null` |
| `zero-nonmember` | The flat row is nonzero, but `C(O(e1))=1`; the coefficient kernel has dimension 0 and no nonzero vector. | Hd1 is empty, rank 0.  Target `e1` is separated by dual `(1,0)`. | `1,0,0,0,NONMEMBER,null,[1,0]` |
| `post-c-cancel` | Seed `e1` and the swap produce independent `e1,e2`, rank 2.  Their C-images are both 1, so the coefficient kernel is `<(2,1)>`, dimension 1, with 2 nonzero vectors. | Hd1 is `<(2,1)>`, rank 1.  Target `(1,2)=2(2,1)` and the corresponding theta ancestry is `(1,2)`. | `2,1,2,1,MEMBER,[1,2],null` |

These are exactly the five fixture expectations.  This gate is **5/5
STATIC**.

## 4. Incremental algorithm and performance audit

For the literal fixture, the old and new producer accept the same rows in
the same seed/action precedence; the checker retains its old reverse-action
order.  The exact v10 closure accounting is:

| case | seeds | actions | actual queue pops | programmed pop bound | accepted rank |
|---|---:|---:|---:|---:|---:|
| `nonzero-member` | 2 | 2 | 4 | 6 | 2 |
| `outside-nonmember` | 1 | 1 | 1 | 3 | 1 |
| `zero-member` | 1 | 1 | 1 | 3 | 1 |
| `zero-nonmember` | 1 | 1 | 1 | 3 | 1 |
| `post-c-cancel` | 1 | 1 | 2 | 3 | 2 |

There are nine baseline queue insert/reduction attempts, seven accepted
rows, and nine action expansions.  Each stored row follows one successful
incremental reduction, and no dependent row is appended.  The bounds are
finite and safe.  In the first case exact-flat deduplication suppresses
`m(e1)=e2` and `m(e2)=e1`, while the distinct dependent vectors
`n(e1)=2e2` and `n(e2)=2e1` are each queued and rejected on pop; hence the
advertised count 4 is exact.

The targeted task318 closure repair itself is effective:

```text
producer known-closure full-rank rebuilds: v9 13 -> v10 0
checker  known-closure full-rank rebuilds: v9 18 -> v10 0
checker duplicate first-row containment:  v9  1 -> v10 0
```

However, the new echelon owners do not carry an augmented identity/ancestry
matrix.  Normalizing a reduced pivot row changes it by combinations of prior
accepted rows, but that combination is discarded.  Checker's dictionary
from pivot column to reduction coefficient can reconstruct against its
private normalized pivot rows only; it cannot express the result against
the accepted receipt rows.  Therefore the advertised change-of-basis and
exact stored-row reconstruction are absent.

The two-way closure-span tests, exhaustive left-kernel enumeration, kernel
basis independence/cardinality, Hd1 content, member equations/ancestry, and
nonmember dual equations are otherwise present.  But replay completeness is
still false because `receipt["closure_rank"]` is not bound to the independent
rank.  The receipt fields `kernel_dim`, `full_nonzero_kernel_cardinality`,
`target`, and `slice_membership` are also accepted without direct equality
checks; their mathematical values are recomputed indirectly, but an
internally inconsistent resealed receipt is not rejected.

The remaining full-RREF accounting for the five baseline producer calls is:

```text
15  base-action invertibility checks (necessary semantic gates)
 5  nullspace RREFs (necessary)
13  Hd1 membership/output rank calls
33  total
```

Of the final 13, `rank(hs)` is recomputed for membership and again for the
output; retaining one Hd1 echelon per case removes eight full rebuilds (four
literal duplicates plus four target-extension rebuilds).

The checker baseline accounting is:

```text
 33  base/stored-action invertibility RREFs
  8  target-membership RREFs
 15  repeated Hd1/Hd1-receipt rank fields
 38  Hd1 two-way span RREFs
  6  member-ancestry span RREFs
  5  return-value Hd1 rank RREFs
105  total
```

The 33 invertibility gates are semantically useful.  Of the other 72, at
least 14 repeated `rank(hd1)` calls, all 38 repeated span rebuilds, and all 6
ancestry-span rebuilds are avoidable immediately: 58 full RREF rebuilds.
The remaining target extensions and receipt-Hd1 ranks can also use retained
incremental bases.  Thus the claim that avoidable known-basis rebuilds are
zero is true only for the narrow closure loop, not for the full checker
requested by task322.

All loops are nevertheless fixed and small.  The matrix/RREF maximum is
11x11.  Closure rank is at most 2; the programmed queue-pop maximum is 6.
Producer `span_solve` and both dual searches inspect at most `3^2=9`
coefficient vectors.  Checker left-kernel enumeration also inspects at most
`3^2=9`, never `3^11`.  SELFTEST has exactly five producer baseline compiles
plus 19 mutation compiles, and five checker baseline replays plus 11 raw-case
oracles plus eight receipt replays.  Producer parses one file; checker parses
the fixture and receipt once each.  Mutation copies are bounded in-memory
JSON round trips.  There is no retry, process pool, thread, sleep, polling,
lock, background child, or unbounded queue.  The driver has only the
prescribed serial producer/checker subprocesses.

## 5. Ordered mutation reachability and fail-closed audit

The following table traces the complete ordered roster on the actual chosen
cases.  Every listed mutation changes canonical bytes and is resealed before
the caught semantic call.

| owner | producer mutation and reached rejection | checker mutation and reached rejection |
|---|---|---|
| `field_modulus` | case modulus 3->9; `modulus` | raw case 3->9; `typed field` |
| `theta_seed` | theta seed scalar changes; `theta seeds` binding | raw theta seed changes; `control owner` |
| `theta_action` | `A_theta[0][0]` changes; base/binding `action owner` | same raw field; literal preflight binding equality |
| `z_action` | `A_Z[0][0]` changes; base/binding `action owner` | same raw field; literal preflight binding equality |
| `eta_action` | `A_E[0][0]` changes; base/binding `action owner` | same raw field; literal preflight binding equality |
| `D_entry` | `D[0][0]` changes; `map owner` | same raw field; literal preflight binding equality |
| `O_entry` | `O[0][0]` changes; `map owner` | same raw field; literal preflight binding equality |
| `C_entry` | `C[0][0]` changes; `map owner` | same raw field; literal preflight binding equality |
| `action_order` | action-name list changes; `control owner` | raw name list changes; action-order preflight |
| `premature_C` | phase becomes before-closure; `control owner` | same raw phase; `control owner` |
| `target` | outside target becomes `e1`; terminal/member mismatch | same raw target; independent terminal mismatch |
| `seed_index` | seed binding scalar changes; `theta seeds` | receipt row 1 seed index becomes 99; `seed replay` |
| `parent` | `parent_hint` becomes 1; `control owner` | receipt seed row 1 parent becomes 99; `seed replay` |
| `row_theta` | theta seed scalar changes; `theta seeds` | receipt row 1 theta changes; `row typed replay` |
| `left_kernel` | method flag becomes image; `control owner` | two receipt kernel vectors are made equal; kernel-basis independence |
| `Hd1` | raw C entry changes; `map owner` | receipt Hd1 row changes; Hd1 content |
| `member_ancestry` | seed binding scalar changes; `theta seeds` | receipt member theta changes; member equations/ancestry |
| `dual` | raw terminal becomes MEMBER; terminal/member mismatch | receipt dual scalar changes; dual equations |
| `terminal` | raw terminal becomes MUTATED; terminal enum | receipt terminal becomes MUTATED; receipt terminal |

Thus the concrete current fixture supplies a canonical change and a
reachable rejecting path for all 19 producer and all 19 checker controls.
That does **not** establish the commissioned fail-closed mutation gate:

- the broad catches count unrelated implementation/type/index faults as a
  successful semantic rejection and no owner-specific reason is asserted;
- several producer controls do not mutate their named generated object at
  all.  In particular `seed_index`, `parent`, `row_theta`, `left_kernel`,
  `Hd1`, `member_ancestry`, and `dual` are rejected by earlier fixture/control
  gates rather than an oracle over the named produced certificate field.
  These are wrong-owner tests under task322's stated rule; and
- the independent checker trusts only the producer's `{owner,rejected}`
  booleans for producer mutation controls, with no producer-side canonical,
  seal, stage, or reason transcript to replay.

Accordingly the raw static path count is 19/19 and 19/19, but both mutation
quality verdicts are REJECT.  Actual executed counts remain 0/19 and 0/19.

## 6. Final accounting

```text
BYTE / PIN / PHYSICAL FIXTURE SCOPE:         PASS
SOURCE SEMANTIC RETENTION:                   REJECT (receipt closure_rank gate dropped)
LITERAL BASE/BINDING SHAPES:                 30/30 PASS
LITERAL STORED-ACTION SHAPES:                6/6 PASS
EXPECTED TUPLES:                             5/5 STATIC
PRODUCER INCREMENTAL ALGORITHM:               REJECT (no ancestry/change-of-basis transform)
CHECKER INDEPENDENCE / REPLAY COMPLETENESS:   REJECT (mirrored basis; dropped receipt field gate)
PRODUCER MUTATION STATIC PATHS:               19/19 traced; quality REJECT
CHECKER MUTATION STATIC PATHS:                19/19 traced; quality REJECT
PRODUCER MUTATIONS ACTUAL:                    0/19
CHECKER MUTATIONS ACTUAL:                     0/19
PERFORMANCE / FIXED BOUNDS:                   REJECT (bounded, but avoidable RREF rebuilds remain)
OVERALL:                                      REJECT / UNEXECUTED
EXECUTION:                                    UNEXECUTED
ACTUAL A5 / ACTUAL A6:                        0/3 / 0/3
LIFT / FAKE / IHARA:                          NONE
```

`TASK322_R07_TASK320_V10_CODE_PERFORMANCE_AUDIT_REJECT_UNEXECUTED`
