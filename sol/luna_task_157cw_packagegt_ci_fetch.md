# Luna task 157cw - fetch the pinned PackageGT source in row18 CI

## Scope

This is one concrete GHA packaging repair from failed run `32090197520`.
The run stopped before static tests/GAP because the intentionally gitignored
file `thirdparty/packageGT/extracted/PackageGT/PaB.py` was absent on checkout.
Do not change any mathematics, producer, checker, terminal status, or proof
connection.

Repository provenance already records the official distribution at
`https://sites.temple.edu/vald/files/2024/05/PackageGT.zip` with archive
SHA-256
`c3124483cb1464b9010c091011370db091a76561a2af923a38efb6900f645f95`.
The member `PackageGT/PaB.py` must have SHA-256
`e54c08d3437d0706b4639d7db31f7177c1c82de9c2f820fa7b194fa1c4e378f2`.

## Authorized files

Modify/create only:

- `.github/workflows/d972-b4-literal-row18-stage-v1.yml`
- `sol/luna_reply_157cu_literal_row18_stage_impl.md`
- `sol/luna_reply_157cv_row18_registered_launcher.md`
- `sol/luna_reply_157cw_packagegt_ci_fetch.md`

Parent Sol owns this task file and reset-bootstrap updates.

## Required repair

Before the existing all-input hash gate, download the official ZIP with
fail-closed curl retries, verify the exact archive SHA, extract only
`PackageGT/PaB.py` using Python's standard `zipfile` into the exact path
expected by producer/checker, and verify its existing exact SHA.  Reject a
missing/duplicate member or any digest drift.  Do not vendor the ignored
third-party source into Git and do not weaken/remove its pin.

Refresh the row18 workflow hash in the two existing replies and report the
new immutable workflow hash.  Run YAML/structural/hash checks only.  Do not
run GAP, Git, GHA, or heavy Python.

End the new reply with exactly:

`PACKAGEGT_CI_FETCH_READY`
