# Luna reply 157bv — joint vmem guard unit repair

## Verdict

The pre-math operational failure is repaired with a one-line, unit-correct
assertion.  No producer/checker file was changed, and no local GAP, Git,
push, dispatch, or GHA run was performed.

## Failure and root cause

Joint run `32071832977` failed in every matrix lane before mathematical work.
The workflow executed:

```text
ulimit -v 12000000
```

On Linux, `ulimit -v` takes KiB, whereas Python's
`resource.getrlimit(resource.RLIMIT_AS)` reports bytes.  The old assertion
compared `soft` with `12000000` and therefore rejected the correctly applied
limit of `12000000 * 1024` bytes.

## Repair

In `.github/workflows/d972-burau-joint-v1.yml`, the guard now computes and
checks the conversion explicitly:

```python
soft, hard = resource.getrlimit(resource.RLIMIT_AS)
expected = 12000000 * 1024
assert soft == expected
```

The shell guard remains `ulimit -v 12000000`; only the erroneous unit
comparison changed.  The diagnostic marker now prints the byte value and
the converted expected value.

## Static checks

```text
JOINT_YAML_PARSE_PASS jobs=['joint']
JOINT_EMBEDDED_PY_COMPILE_PASS blocks=1
JOINT_STATIC_BLOCK_AUDIT_PASS run_blocks=1 escaped_interpolations=0
JOINT_VMEM_ASSERTION_UNIT_PASS expected_bytes=12000000*1024
```

The exact authorized files for this bounded repair are:

```text
sol/luna_task_157bv_joint_vmem_guard.md
sol/luna_reply_157bv_joint_vmem_guard.md
.github/workflows/d972-burau-joint-v1.yml
```

Final workflow SHA256:

```text
.github/workflows/d972-burau-joint-v1.yml
8741EF5FEB89B5301BA74419E182B585A0794FBC1C5F3F3DD4698E31851209AD
```

JOINT_VMEM_GUARD_REPAIRED
