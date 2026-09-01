# Luna task 464 -- minimal contract repair for compact actual positive owner v3

Role: Luna implementation only.  Do not run production, dispatch GHA, edit
workflows, commit, push, or touch files outside the four outputs below.

Task462 v2 passed the actual-arithmetic/44-row proxy gates, but it is not yet
adoptable for two small envelope reasons: its receipts do not explicitly say
`resumable=false`, and its GHA nonpositive branch checks only A5/A6 rather than
the complete no-claim frontier.  Make a guarded, versioned v3 successor.  Do
not change the mathematical engine, roster, target, action closure, PB oracle,
or resource caps.

## 1. Required outputs

Create only:

1. `search/d972_r07_compact_direct_relator_a5_a6_positive_v3.py`;
2. `crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v3.py`;
3. `search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v3.g`;
4. `sol/luna_reply_464_r07_compact_actual_positive_owner_v3.md`.

## 2. Exact inherited bases

Guard these Task462 v2 physical sources exactly:

```text
producer 7707 47cc53c0b59cbca0981983373d30604cbffd874cfa01d2d2adef599e505a21d3
checker  7720 535c7b8aa0983748204d0e381d367d3398380ea3097cd48ef374dfc3daf38c67
driver   3763 1f6a5c51e382ffcb063bbb0b150073e6bc499662182a35f58b3b8f32f00e0d88
```

The guarded generated v2 bodies are:

```text
producer 61341 289dbff63af59daec0478bdc6eee376b711c4b944fee08d671b3e10a323b5539
checker  47815 ee826f1873e045574838e4fd478530edf2ef5986683c7f0ad72cf4958baac262
```

Preserve every Task193/Task198/Task411 pin and every actual arithmetic call.

## 3. Only permitted producer/checker changes

- Version schema/marker/source pins from v2 to v3 by exact cardinality-guarded
  transforms.
- Every producer receipt, including MEMBER, UNKNOWN_INCOMPLETE,
  UNKNOWN_RESOURCE, and UNKNOWN_INPUT, must contain top-level
  `"resumable": false` under the producer self seal.
- The independent checker must exact-pin the v3 producer and require
  `receipt["resumable"] is False` before accepting MEMBER.  It must retain the
  Task411-checker roster reconstruction and actual Task456 MEMBER replay.
- No checkpoint/resume option or state file may be introduced.

## 4. Driver repair

Keep one producer process, the 14,400-second / 5,700,000,000-byte caps, and
checker invocation only for MEMBER.  In every accepted nonpositive branch,
parse the sealed JSON receipt and require exactly:

```text
resumable        false
A5               NONE
A6_M             false
A7               NONE
compatible_lift  NONE
fake             NONE
Ihara            NONE
```

Use a short inline Python JSON assertion if that is clearer and safer than
multiple whitespace-sensitive greps.  It may inspect only the already written
receipt and must not import producer helpers.  Continue to accept only:

```text
UNKNOWN_INCOMPLETE:compact_direct_span_exhausted
UNKNOWN_RESOURCE:*
UNKNOWN_INPUT:*
```

## 5. Bounded gates

Run only repo-external-cache `py_compile`, load-without-main, exact source and
generated-body pins, actual 44-row producer/checker roster equality, a
read-only proxy gate, and static driver branch/process/cap/no-resume scans.
Do not run production or a synthetic mathematical MEMBER.  Report exact
physical/generated pins and state that GHA/runtime remain unexecuted.

