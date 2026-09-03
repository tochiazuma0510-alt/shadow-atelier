# Sol(max) Task672 — audit Task640 v6 verdict-layout repair

You are Sol(max).  Audit the inert workflow produced by Task669 against the
v5 failure receipt in Task670.  Write only
`sol/sol_reply_672_audit_r07_task640_parent_verdict_layout_v6.md`; no code edit,
git, GHA, download, or production run.

Read v5 and v6 workflows, Task669 task/reply, Task670, and both fresh Python
consumers at their Task625 payload validators.  Check by bounded static means:

1. after a successful exact checker replay and `cmp`, both byte-equal files
   required by both consumers exist under the nested payload with exact names;
2. the original is copied from the authenticated artifact-root verdict and the
   replay from the just-produced verdict; neither copy precedes `cmp`;
3. aside from mechanical v6 labels, artifact labels and the inert guard, this
   one copy is the entire v5-to-v6 semantic delta;
4. Task625 path/cap/service pins, Task554/595 downloads, all code hashes,
   time/RSS caps, timeout, action SHA pins, success-only residual upload and log
   upload are unchanged;
5. the workflow is syntactically valid and definitely inert; removing only
   `false &&` would produce the intended authorized release without changing
   the event predicate.

Reject unrelated hardening or re-auditing the already passed Python math.
Report exact bytes/LF/SHA and normalized diff.  End exactly:

```text
PASS_LAYOUT_ONLY / SAFE_TO_DISPATCH_GHA=yes
```

or

```text
FAIL_LAYOUT_ONLY / SAFE_TO_DISPATCH_GHA=no
```

Candidate only; `verified=false`; no v220 numerator change.
