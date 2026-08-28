# R07 task307 v8 GHA all-case fixture failure audit v261

Author: Sol / 2026-08-28

Status: authenticated execution audit.  Three GHA dispatches used immutable
head `048edd18d098c5aa48fbf828d78edfd952a4c5da`.  The first two stopped in
the dispatch preamble, and the third reached the v8 producer and failed its
new all-case preflight.  None is a mathematical MEMBER/NONMEMBER result, an
actual A5/A6 milestone, a lift, fake certificate, or Ihara conclusion.

## 1. Dispatch input stops

Run `33168665097` received

```text
GAP_RUN_PREAMBLE: D307Mode:=\
Error, task304 MODE required
```

because a PowerShell command-line escape was used where PowerShell did not
preserve the quoted value.  Run `33168864708` received

```text
GAP_RUN_PREAMBLE: D307Mode:=SELFTEST;;
Error, Variable: 'SELFTEST' must have a value
```

because `gh workflow run -f` removed the embedded JSON quotes.  These two
runs did not enter either Python program.  They are parent dispatch-input
errors, not defects or evidence about the generalized kernel.

Run `33168987097` was dispatched through the JSON API and retained the exact
literal preamble

```text
D307Mode:="SELFTEST";;
```

This is the required dispatch method for subsequent string-valued GAP
preambles.

## 2. Executed v8 failure

Run `33168987097` reached
`search/d972_r07_joint_slice_kernel_general_v8.py`.  Before compiling a
case it stopped at the commissioned preflight with

```text
RuntimeError: fixture preflight dimensions A_E
Error, task304 missing completion
```

The driver therefore failed closed and uploaded no accepted artifact.

Independent read-only parsing of the exact v8 fixture gives:

| case | A_E row lengths | A_E_binding row lengths |
|---|---|---|
| nonzero-member | 11,11,11,11,11,11,11,11,11,11,11 | 11,11,11,11,11,11,11,11,11,11,11 |
| outside-nonmember | 11,11,11,11,11,11,10,10,11,11,11 | 11,11,11,11,11,11,10,10,11,11,11 |
| zero-member | 11,11,11,11,11,11,10,10,11,11,11 | 11,11,11,11,11,11,10,10,11,11,11 |
| zero-nonmember | 11,11,11,11,11,11,10,10,11,11,11 | 11,11,11,11,11,11,10,10,11,11,11 |
| post-c-cancel | 11,11,11,11,11,11,10,10,11,11,11 | 11,11,11,11,11,11,10,10,11,11,11 |

In each of the last four cases, rows 6 and 7 of both matrices are the same
truncated ten-entry standard-basis rows.  Thus task312 repaired the first
case only.  Task314's static assertion that all 30 pairs had the displayed
dimensions is refuted by literal bytes and executed preflight and no longer
authorizes v8 acceptance.

## 3. Bounded successor

Task316 commissions a versioned v9 which changes only the sixteen truncated
row arrays: two rows, in two matrices, in four cases.  Each gets one trailing
zero.  Expected tuples and all semantic code remain fixed.  V9 must undergo
a fresh independent correctness/performance audit before GHA execution.

```text
RUN 33168665097:                         DISPATCH INPUT STOP
RUN 33168864708:                         DISPATCH INPUT STOP
RUN 33168987097:                         EXECUTED PREFLIGHT FAILURE
IMMUTABLE HEAD:                          048edd18d098c5aa48fbf828d78edfd952a4c5da
V8 FIVE-CASE A_E SHAPE:                  1/5 VALID
V8 FIVE-CASE A_E_BINDING SHAPE:          1/5 VALID
TASK314 EXECUTION AUTHORIZATION:          SUPERSEDED
ACTUAL A5 / ACTUAL A6:                   0/3 / 0/3
LIFT / FAKE / IHARA:                     NONE
```

`R07_TASK307_V8_GHA_ALL_CASE_FIXTURE_FAILURE_V261_AUDIT`
