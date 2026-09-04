# Luna Task 842 — one reached nonpromotion repair for P1 release v9

Read the complete Task838 audit.  Repair only its sole remaining blocker in
new versioned files:

- `search/d972_r07_canonical_p1_dag_degree2_lift_v10.py`;
- `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v9.yml`;
- `sol/luna_reply_842_r07_p1_reached_nonpromotion_repair_v9.md`.

Keep the row-building mathematics, order, schemas and all immutable inputs
unchanged.  Factor the final promotion into one narrow helper which is called
both by the production success tail and by the production
`except (ResourceStop, KeyboardInterrupt)` path.  On the latter call it must
re-raise the supplied terminal after rollback and must be incapable of
writing/removing a candidate output.  On success it performs the existing
checkpoint unlink, manifest write and atomic staging-to-output replace.

Make one bounded permanent fixture write post-checkpoint orphan bytes, enter
that same factored helper with an actual `ResourceStop` and an actual fresh
requested output path, then assert: rollback is the authenticated prefix,
the helper was reached, the terminal propagated, and the requested output was
not created.  Also exercise the helper's tiny success branch so a helper that
never promotes cannot pass.  Do not call the heavyweight production build or
change its arithmetic body merely to satisfy the fixture.

Update the workflow only for the new fixed producer path/SHA/bytes/LF,
version labels and fire token `[fire-r07-canonical-p1-degree2-lift-v9]`.
Preserve the repaired heredoc, canonical cross-runner pins and all prior
fixtures.  Run bounded selftest, py_compile, YAML and extracted-shell syntax.
No GHA/git/extra hardening.  End `IMPLEMENTED_AUDIT_REQUIRED`.
