# Sol(max) Task703 — exact Task701 v9 release audit

Audit only the final Task701 delta against Task697 and accepted Task700.

Frozen final inputs:

- producer SHA-256
  `8719929bfd6d134320da8c6fc1a8df527f458c1523f8edb0330b539649097206`;
- inert v9 workflow SHA-256
  `b381c5ebd8d791bdd36925898d25f4292a05fc62e83588f1782b0e32242e7186`;
- Task701 reply SHA-256
  `5079de2349909b3d79cef4755e8127d5f826268beb971bf203076ae26e7b8676`.

Check that the producer translates exactly the minimal deletion prefix,
installs it after `build_light` before the first coordinate call, checks order
59,049 and the zero-word typed identity canary, calls no full `build_heavy`,
and leaves later arithmetic unchanged.  Check that the workflow pins the
final producer, retains step-local 9,600/global 5,400 and all old commands/
caps/pins, with only v9 labels and the inert guard otherwise.

Do not add requirements, edit, run real deletion, or perform generic audit.
Write only `sol/sol_reply_703_audit_r07_task701_v9_release.md` with
`PASS_MINIMAL_DELETE_ONLY / SAFE_TO_DISPATCH_GHA=yes` or one exact blocker,
input/reply hashes and `verified=false`.
