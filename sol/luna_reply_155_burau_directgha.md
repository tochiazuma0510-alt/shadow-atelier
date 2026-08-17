# Luna reply 155 — pinned direct GAP 4.16.0 GHA lane

Implemented only the authorized files:

- `.github/workflows/d972-burau-direct-v1.yml`
- `sol/luna_reply_155_burau_directgha.md`

The workflow retains closed manual `workflow_dispatch` choices
`a={2,4}` and `mode={selftest,full}`, and adds a push trigger restricted to
`sol/d972-dmtcp-provision-v420` with dedicated-lane paths.  Its dynamic matrix
expands push events to exactly two lanes (`a=2` and `a=4`) while a manual
dispatch expands to only the selected `a` lane.  It directly downloads and SHA-256 verifies
the frozen GAP 4.16.0 core, GAP required-packages, and JSON 2.4.0 archives,
rejects ambiguous archive roots, builds GAP in a temporary job directory, and
builds JSON beneath a private GAP package root.  It gates the exact GAP
version and successful `GAPDoc` and JSON loads before reading
`search/d972_b4_burau_fiber_v2.g`.  GAP runs from the built extracted source
root (the official non-install build layout), and JSON is configured against
that same GAP root.

The generated driver uses only the closed inputs and the producer's exact
`D972_B4_BURAU_Q/A/MODE/OUTPUT` bindings.  GAP runs with
`--quitonbreak -q -o 12g`; `PIPESTATUS` preserves the real exit status through
`tee`, diagnostics are fail-closed, and selftest/full marker cardinalities are
checked exactly.  Full mode additionally validates the q/a values, 972 unique
receipt rows, and candidate/unknown-only status using Python's standard
`json` module.  No workflow promotion of A or B is possible.

For push campaigns, each lane runs its own selftest first and invokes full mode
only after that lane's selftest gates pass; selftest/full drivers and logs are
separate under `ci/out/`.  Evidence is uploaded with mode/a/run-attempt-specific
artifact names on both success and failure.  No credentials are printed or
accepted as inputs, and no third-party actions beyond checkout/upload-artifact
are used.

Frozen archive bindings:

| input | value |
|---|---|
| GAP core URL | `https://github.com/gap-system/gap/releases/download/v4.16.0/gap-4.16.0-core.tar.gz` |
| GAP core SHA-256 | `8c35f406046f1172de658375dcd5beaf9644888cd16f8f5e7db163afc9fade1a` |
| GAP required-packages URL | `https://github.com/gap-system/gap/releases/download/v4.16.0/packages-required-v4.16.0.tar.gz` |
| GAP required-packages SHA-256 | `ad9652185df53a7cf81dc41520dc3cca8321b171bbcc921b7ee9c66f5e9c35e2` |
| JSON URL | `https://github.com/gap-packages/json/releases/download/v2.4.0/json-2.4.0.tar.gz` |
| JSON SHA-256 | `ce49399f5f5dc4caf95213f5dd7ec09988f2ae93364817e88ff075a09a22826a` |

Local checks performed (no local GAP, commit, push, or dispatch):

- YAML structure inspected against the repository's workflow conventions.
- Shell control flow audited for closed inputs, archive-root rejection,
  required-package extraction, `PIPESTATUS`, diagnostic gates, exact marker
  counts, receipt checks, and `always()` artifact upload.
- `git diff --check -- .github/workflows/d972-burau-direct-v1.yml sol/luna_reply_155_burau_directgha.md`.
- SHA-256 of `.github/workflows/d972-burau-direct-v1.yml`:
  `850b49a9f6ac10de0a514cb8d711714490a1e4be27fe305caead8328c85d8a85`.
- A local `bash -n` attempt through Git Bash was blocked by the host's
  `couldn't create signal pipe, Win32 error 5`; the workflow shell was
  manually audited fail-closed, and the CI runtime remains the authoritative
  Bash check.

Runtime remains for the parent GHA broker.
