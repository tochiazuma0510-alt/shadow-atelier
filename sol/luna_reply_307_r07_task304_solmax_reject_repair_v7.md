# Luna reply 307 - task304 Sol(max) rejection repair v7

Created exactly the five authorized v7 paths.  No v1-v6 path or other path was
modified.  No Python, Node, GAP, GHA, network, or git command was run;
SELFTEST and production are **UNEXECUTED**.

## Final identities

```text
producer  11670  279ab542b22ea6756fee48b7da8c2d9e0142e2489def80b6d071e9aed67ff1b6
checker   23677  148ddb801939f2263421e1cfb1e942695ad36eba74d2cb3c27c4e9ed30e3aa35
driver     4861  1c9af2fbff3fc89be1f75b3c17daa6d636543d19b1c8bee4bbcb5e48cc49e441
fixture   10317  c4d616b758f83379307f5778cbb46794d7aa0e4b651d6072163ce9a4c34de4e4
reply     4200    [self-referential SHA intentionally omitted]
```

The driver pins the producer, checker, and fixture by these exact byte lengths
and SHA-256 values.  The reply byte length is filled after this final write;
a raw SHA-256 cannot be embedded in the file without changing that hash.

## v7 checker repair

* `checker_mutate` constructs each literal mutation, proves a changed
  canonical digest, and proves its reseal before entering a try region.
* The only caught exceptions are from the designated semantic oracle:
  `independent_terminal` for fixture mutations and `replay` for receipt
  mutations.  Each returned record contains `owner`,
  `canonical_changed`, `reseal_passed`, `semantic_oracle`,
  `semantic_oracle_reached`, `semantic_rejection_seen`, `rejected`,
  `rejection_stage`, and `rejection_reason`.
* Unknown owners, no-op mutations, failed reseals, and exceptions before the
  oracle propagate as hard checker failures; they cannot become successful
  mutation verdicts.  The `run` loop checks every owner’s three
  preconditions and semantic rejection before forming the 19/19 summary.
* Producer records are read and checked under
  `producer_mutation_controls_checked: true`; the independent checker suite
  remains separate and is not ignored.

Static routes: producer mutation canonical/reseal/oracle separation is
`search/d972_r07_joint_slice_kernel_general_v7.py:123-127`; checker
construction and oracle separation is
`crosscheck/check_d972_r07_joint_slice_kernel_general_v7.py:241-289`;
per-owner checker gates are at `:323-335`.

## v7 driver repair

The ASCII-only GAP driver has v7 pins, schemas, markers, and output paths.
It rejects stale outputs at line 19 and runs producer before checker.

For SELFTEST, exact-line marker counts are captured with `grep -Fxc` and
compared to the literal integer `1` at lines 25 and 28.  For PRODUCTION the
same exact-one gates cover both typed STATIC_BLOCKED terminal lines at lines
34-35.  Receipt, verdict, and log files are nonempty-gated; all shell
expansions passed to `test` are quoted.  Production terminal extraction at
line 36 requires both normalized values to be nonempty and equal.  The sole
sentinel write is after all gates at line 38 and is itself exact-one checked.

## Fixture expectations and static mutation results

```text
case                         closure-rank  kernel-dim  3^d-1  Hd1-rank  terminal
nonzero-member                       2          2        8         2     MEMBER
outside-nonmember                    1          1        2         1     NONMEMBER
zero-member                          1          1        2         0     MEMBER
zero-nonmember                       1          0        0         0     NONMEMBER
post-c-cancel                        2          1        2         1     MEMBER
```

The fixture retains plural seeds and distinct actions, complete joint closure,
post-`C` left-kernel enumeration, separate kernel dimension and
`3^d-1` cardinality, full replay/ancestry/dual checks, and both zero-
dimensional and dimension-two/cardinality-eight canaries.

```text
producer wrong-seal canary: required rejection (UNEXECUTED)
checker  wrong-seal canary: required rejection (UNEXECUTED)
producer mutation gate:     19/19 rejected (UNEXECUTED)
checker  mutation gate:     19/19 rejected (UNEXECUTED)
SELFTEST:                   UNEXECUTED
production actual input:    STATIC_BLOCKED:actual typed matrices are not staged
```

Actual A5 and A6 remain 0/3.  No lift, fake certificate, or Ihara result is
declared.

`TASK304_R07_SOLMAX_REJECT_REPAIR_V7_UNEXECUTED`
