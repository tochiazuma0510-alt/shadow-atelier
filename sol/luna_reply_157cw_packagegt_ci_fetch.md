# Luna reply 157cw - PackageGT CI fetch repair

## Result

The pre-GAP packaging failure from run `32090197520` is repaired in the
authorized row18 workflow.  No mathematics, producer, checker, terminal
status, proof connection, or frozen member pin was changed.  I did not run
GAP, Git, GitHub Actions, or heavy Python.

## Fail-closed bootstrap

Before the existing all-input hash gate, the workflow now:

1. downloads the official distribution from
   `https://sites.temple.edu/vald/files/2024/05/PackageGT.zip` with
   fail-on-HTTP-error, redirects, and bounded all-error retries;
2. requires archive SHA-256
   `c3124483cb1464b9010c091011370db091a76561a2af923a38efb6900f645f95`;
3. uses only Python's standard `zipfile` reader and requires exactly one
   non-directory member named `PackageGT/PaB.py`;
4. reads only that member, requires SHA-256
   `e54c08d3437d0706b4639d7db31f7177c1c82de9c2f820fa7b194fa1c4e378f2`,
   and writes it with exclusive creation to
   `thirdparty/packageGT/extracted/PackageGT/PaB.py`;
5. rehashes the written file, after which the pre-existing all-input gate
   independently checks the same member pin again.

No ignored third-party file was added to Git.

## Static checks and final hash

Lightweight YAML/structural checks preserve `workflow_dispatch` plus
`workflow_call`, all eight computation/evidence steps, all immutable action
revisions, and all existing frozen input hashes.  A local read-only archive
inspection also confirms one exact member and both supplied digests.

Final SHA-256 of
`.github/workflows/d972-b4-literal-row18-stage-v1.yml`:

```text
57c90154335128d5f4f1863452a82a4caf3bd016df6342540bf908a19df4a20d
```

The same workflow hash is refreshed in the 157cu and 157cv replies.

PACKAGEGT_CI_FETCH_READY
