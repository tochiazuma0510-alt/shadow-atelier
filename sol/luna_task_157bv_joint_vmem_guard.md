# Luna task 157bv — joint vmem guard unit repair

Role: Luna operational repair.  The joint workflow run 32071832977 failed
before mathematics because `ulimit -v 12000000` specifies KiB while Python's
`resource.RLIMIT_AS` reports bytes; its assertion compared the soft limit to
the unconverted integer.

Authorized changes only:

- `.github/workflows/d972-burau-joint-v1.yml`
- `sol/luna_task_157bv_joint_vmem_guard.md`
- `sol/luna_reply_157bv_joint_vmem_guard.md`

Replace the assertion with an exact, visibly unit-correct conversion
(`12000000 * 1024`) and keep the 12-GB virtual-memory guard.  Do not edit the
producer/checker, run local GAP/Git/GHA, push, or dispatch.  Perform only
YAML/static embedded-block checks and report the failed run, root cause,
repair, final workflow SHA, and exact authorized files.
