# Luna reply 157cv - registered row18 launcher

## Result

The registration/bootstrap repair is implemented in the authorized workflow
and reply files only.  No producer, checker, mathematics, computation step, or
terminal interpretation was changed.  I did not run GAP, Git, GitHub Actions,
or heavy Python.

## Reusable row18 workflow

`.github/workflows/d972-b4-literal-row18-stage-v1.yml` now exposes
`workflow_call` while retaining `workflow_dispatch`.  Its permissions, frozen
computational hashes, immutable action revisions, producer command,
independent checker, timeout behavior, and evidence upload remain unchanged.
The later 157cw packaging repair adds only a pinned official-ZIP bootstrap for
the intentionally gitignored PackageGT `PaB.py` before its existing hash gate.

Final SHA-256:

```text
57c90154335128d5f4f1863452a82a4caf3bd016df6342540bf908a19df4a20d
```

The same value replaces the former literal-workflow hash in
`sol/luna_reply_157cu_literal_row18_stage_impl.md`.

## Registered launcher

The already registered
`.github/workflows/d972-d972core-c2six-intersection-v2.yml` now has one
optional typed `workflow_dispatch` choice named `target`:

```text
core            (default)
literal-row18
```

Push events and a dispatch with the default/omitted `core` choice run the
existing core job.  Only a manual dispatch with `target=literal-row18` skips
that job and invokes the same-ref reusable workflow through exactly:

```yaml
uses: ./.github/workflows/d972-b4-literal-row18-stage-v1.yml
```

The existing immutable external-action check remains fail-closed.  Its only
new exception is the exact local reusable-workflow path above; every other
`uses:` entry must still carry a 40-hex revision.

Final launcher SHA-256:

```text
e8dbd952c8dd44b192341d35354dc221e12698dde6c2ca3ea9f464d1506931c8
```

## Static checks

Lightweight YAML parsing and structural assertions check both triggers, the
optional choice/default/options, mutually exclusive job conditions, exact
same-ref call path, preservation of the core push paths, all immutable action
references, and all existing row18 hash-gate values.

ROW18_REGISTERED_LAUNCHER_READY
