# Luna task 157cv - registered launcher for the frozen row18 workflow

## Role and scope

This is a GitHub Actions registration/bootstrap repair only.  The mathematics,
producer, checker, terminal interpretation, and frozen B4-B connection from
`sol/luna_task_157cu_literal_row18_stage_impl.md` must not be reopened or
changed.

GitHub returned HTTP 404 when parent tried to dispatch the new
`d972-b4-literal-row18-stage-v1.yml`, because a workflow absent from the
default branch is not yet registered for manual dispatch.  The already
registered workflow
`.github/workflows/d972-d972core-c2six-intersection-v2.yml` can be dispatched
at the working branch and may call a same-ref reusable workflow.

## Authorized files

Modify/create only:

- `.github/workflows/d972-b4-literal-row18-stage-v1.yml`
- `.github/workflows/d972-d972core-c2six-intersection-v2.yml`
- `sol/luna_reply_157cu_literal_row18_stage_impl.md`
- `sol/luna_reply_157cv_row18_registered_launcher.md`

Parent Sol owns this task file and the reset-bootstrap update.  Do not touch
any producer/checker or other dirty-tree file.

## Required repair

1. Add `workflow_call` to the new literal-row18 workflow while retaining its
   manual `workflow_dispatch` entry and every existing pinned computation
   step unchanged.
2. Add one optional typed `workflow_dispatch` choice/input to the registered
   C2-v2 workflow, defaulting to its existing core behavior.  Its existing
   push behavior and core job must remain unchanged for push/default dispatch.
3. For the literal-row18 choice only, call the same-ref local reusable
   workflow with `uses: ./.github/workflows/d972-b4-literal-row18-stage-v1.yml`.
   Do not duplicate or weaken its hash gates.
4. Refresh the literal workflow SHA in the 157cu reply and record the launcher
   workflow SHA in the 157cv reply.  Run only lightweight YAML/static checks.

Do not run GAP, Git, GitHub Actions, or heavy Python.  End the new reply with
exactly:

`ROW18_REGISTERED_LAUNCHER_READY`
