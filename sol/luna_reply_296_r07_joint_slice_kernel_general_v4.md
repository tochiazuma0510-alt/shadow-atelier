# Luna reply 296 - R07 joint-slice kernel general v4

Only the five authorized task296 v4 paths were created. Task291--294 and all
other paths were left untouched. No Python, Node, GAP, GHA, network, or git
command was executed; status is UNEXECUTED.

## Final identities

```text
producer  10673 319f8df5c639387667cbf153ce0549dce973ebfa8fcd504910ca668277f5dbf4
checker   20071 39a7e1f1844b66440a0bea942253de8574987d7fd7eb7337eae42cd858a3a492
driver    3815  f3f5162ee26ce2c0142be5fbc68e6b565eb4c5486655aa40c1abc34194373290
fixture   10311 a352c9e588894f1195e58066992fa3677cad77c0f4739303fb8abbcc2dca34b2
reply     [self-referential SHA intentionally omitted]
```

v4 separates the RREF kernel basis from the independently enumerated full
kernel. `kernel_dim` is the basis rank and basis length; the checker reports
`full_nonzero_kernel_cardinality=3^kernel_dim-1` as a separate field. The dim=2
and zero-dimensional canaries are literal fixture expectations.

Closure remains rank-admitting with plural seeds, distinct named actions, and
complete seed/action/parent theta ancestry replay. Receipt terminal, Hd1
content, MEMBER theta, NONMEMBER dual, per-action equivariance, and eleven
occurrence coordinates are independently checked.

All 19 mutations are semantically exercised. Kernel mutation uses a legal
variable-length non-kernel or dependent basis alteration; Hd1 mutation uses a
legal-length content change that changes its span. Receipt-owned mutations are
resealed before checker replay.

```text
case                         kernel-dim  full-nonzero  terminal
nonzero-member                    2          8         MEMBER
outside-nonmember                 1          2         NONMEMBER
zero-member                       1          2         MEMBER
zero-nonmember                    0          0         NONMEMBER
post-c-cancel                     1          2         MEMBER

SELFTEST / checker:          UNEXECUTED
production actual typed ABI: STATIC_BLOCKED
A5/A6 / lift/fake/Ihara:     NOT DECLARED
```

TASK296_R07_JOINT_SLICE_KERNEL_GENERAL_V4_UNEXECUTED

## Parent Sol dispatch

Parent static audit accepted the v4 SELFTEST for GHA execution and rejected
all v1--v3 returns as superseded.  The generic unchanged workflow was
dispatched as follows:

```text
run id       33163411739
commit sha   97ae4410
mode         SELFTEST
script       search/d972_r07_joint_slice_kernel_general_gha_driver_v4.g
timeout      60 minutes
status       DISPATCHED
```

This dispatch is an implementation test only.  A5/A6 actual inputs and all
witness conclusions remain absent pending the run result.

The first CLI dispatch lost the quoted GAP string before execution:

```text
run id       33163411739
terminal     dispatcher failure: Variable SELFTEST must have a value
math engine  NOT STARTED
```

It is not a SELFTEST result.  Parent re-dispatched through the JSON API so
the literal preamble `D296Mode:="SELFTEST";;` is preserved:

```text
run id       33163594826
commit sha   97ae44101e9109068b3b93c46e06de4e6ae1f7d0
status       FAILURE BEFORE MATHEMATICAL SELFTEST
```

The JSON dispatch did preserve the exact quoted preamble and reached the
Python producer.  It then failed in fixture parsing before compiling any of
the five cases:

```text
RuntimeError: fixture seal/schema
source       parse_fixture, first require call
cause        value.get("fixture_seal") is a nonempty string, while require
             accepts only the singleton boolean True (`ok is True`)
artifact     none (upload step skipped)
```

Thus v4 has no accepted implementation SELFTEST.  This is a fail-closed
Boolean-typing defect, not an A5/A6 mathematical result.  A versioned v5
repair must normalize every truthy non-Boolean predicate before re-execution;
the actual A5/A6 numerators remain zero.
