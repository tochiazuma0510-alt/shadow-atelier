# Luna reply 157bx — synchronized Burau joint q2/q7 v2

## Verdict

The separate v2 bundle is implemented and statically audited.  Joint v1 was
not modified.  No local GAP, large enumeration, Git, push, dispatch, or GHA
run was performed.

## Authorized files

```text
search/d972_b4_burau_joint_v2.py
search/check_d972_b4_burau_joint_v2.py
.github/workflows/d972-burau-joint-v2.yml
sol/luna_reply_157bx_joint_q2q7_v2.md
```

The producer and checker are separate copies of the audited synchronized
semantics.  The checker independently rebuilds the roof, finite-field
Burau/A.18 transforms, theta/tau/tau2 hexagon images, one common-word
Reidemeister–Schreier fiber, all 972 rows, and full-GT zero/all-pass status.
There is no result-table or helper import shared between them.

## q2/q7 admissibility audit

For prime fields, `a=0` is explicitly excluded because it makes every
Burau generator singular.  The registered values are exactly all remaining
nonzero parameters:

```text
q=2: a=[1]
q=7: a=[1,2,3,4,5,6]
```

For every registered pair the producer and checker independently require
field-unit parameter, inverse matrices for all three Burau generators, both
braid relations, and the commuting relation.  These gates are serialized in
the receipt's independent admissibility audit and checked again by the
checker.  The producer and checker selftests also include corrupt-receipt and
unsynchronized-Cartesian-word negative fixtures.

## Preregistered parallel matrix

The workflow has 14 fail-fast-disabled matrix lanes:

```text
q2a1_full
q3a2_full, q4a2_full, q3a2_q4a2
q3a2_q4a2_q5a2, q3a2_q4a2_q5a4
q7a1_full, q7a2_full, q7a3_full, q7a4_full, q7a5_full, q7a6_full
q5a2_q7a1, q5a4_q7a6
```

Thus every q7 nonzero parameter is calibrated, and two q5+q7 synchronized
configurations provide the direct new-information lanes.  Each lane keeps
the one source word synchronized across all components; no Cartesian fiber
product is introduced.  Resource or cap outcomes remain `UNKNOWN_RESOURCE`
and cannot be promoted by the workflow.  The checker must succeed before a
candidate zero is accepted.

The workflow uses read-only permissions, `persist-credentials:false`, Python
3.13.5, hash-pinned SymPy 1.14.0/mpmath 1.3.0, the 12-GB virtual-memory
guard with the Linux KiB-to-byte conversion, 360-minute timeout, restricted
push paths, `workflow_dispatch`, unique config/attempt artifact names, and
`always()` lossless evidence upload.

## Static tests

Executed locally without heavy computation:

```text
python -B -m py_compile search/d972_b4_burau_joint_v2.py search/check_d972_b4_burau_joint_v2.py
python -B search/d972_b4_burau_joint_v2.py --self-test
python -B search/check_d972_b4_burau_joint_v2.py --self-test
```

Observed markers include:

```text
D972_B4_BURAU_JOINT_V2_CORRUPT_RECEIPT_NEGATIVE_PASS
D972_B4_BURAU_JOINT_V2_Q2Q7_ADMISSIBILITY_AUDIT_PASS q2=[1] q7=[1,2,3,4,5,6]
D972_B4_BURAU_JOINT_V2_NEGATIVE_FIXTURES_PASS
D972_B4_BURAU_JOINT_V2_SELFTEST_PASS
D972_B4_BURAU_JOINT_V2_CHECKER_NEGATIVE_FIXTURES_PASS
D972_B4_BURAU_JOINT_V2_CHECKER_SELFTEST_PASS
D972_B4_BURAU_JOINT_V2_CHECKER_FINAL_MARKER status=PASS
```

Workflow/static audit results:

```text
JOINT_Q2Q7_V2_YAML_PARSE_PASS configs=14
JOINT_Q2Q7_V2_EMBEDDED_PY_COMPILE_PASS blocks=2
JOINT_Q2Q7_V2_STATIC_BLOCK_AUDIT_PASS run_blocks=1 escaped_interpolations=0
JOINT_Q2Q7_V2_MATRIX_PASS q2=1 q7=6 q5q7=2
JOINT_Q2Q7_V2_PRODUCER_CHECKER_BINDING_STATIC_PASS configs=14
JOINT_Q2Q7_V2_HASH_GATES_PASS
```

## SHA-256

```text
search/d972_b4_burau_joint_v2.py          C4E15BF8085853808568345917AD71504B5A53BFACDB116C7A1EE9A605E925BF
search/check_d972_b4_burau_joint_v2.py    05B23EA8201E16820496AA45CF891ABADBD92E6448C9F2A3BC8FD4F17B94F471
.github/workflows/d972-burau-joint-v2.yml 072039DF3867B74C74519BB415F1203B9831D0BAC6DFA18A4BCB8495F7E9D3A3
word artifact                               564A921BE8114BDEB963F679C121E8D9AA90E148C65E95E393874FCBA843E9F9
```

JOINT_Q2Q7_V2_READY
