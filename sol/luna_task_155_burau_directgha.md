# Luna task 155 — pinned direct GAP 4.16.0 GHA lane

## Purpose and division

The generic `gap-run.yml` currently fails before our script because
`gap-actions/setup-gap@v3.8.0` cannot resolve release metadata.  Implement a
new, narrowly scoped, versioned workflow that bypasses that metadata lookup by
downloading the exact official GAP 4.16.0 core release asset directly.

- Luna implementation: create `.github/workflows/d972-burau-direct-v1.yml`.
- Luna report: `sol/luna_reply_155_burau_directgha.md`.
- Do not modify `gap-run.yml`, either Burau producer/checker, or any other file.
- Do not run local GAP, commit, push, or dispatch.  The parent is the sole git
  and GHA broker.

## Frozen inputs

- GAP core URL:
  `https://github.com/gap-system/gap/releases/download/v4.16.0/gap-4.16.0-core.tar.gz`
- GAP core SHA256:
  `8c35f406046f1172de658375dcd5beaf9644888cd16f8f5e7db163afc9fade1a`
- GAP 4.16.0 required-packages URL (needed because JSON 2.4.0 declares
  GAPDoc >= 1.5):
  `https://github.com/gap-system/gap/releases/download/v4.16.0/packages-required-v4.16.0.tar.gz`
- GAP required-packages SHA256:
  `ad9652185df53a7cf81dc41520dc3cca8321b171bbcc921b7ee9c66f5e9c35e2`
- JSON 2.4.0 URL:
  `https://github.com/gap-packages/json/releases/download/v2.4.0/json-2.4.0.tar.gz`
- JSON SHA256:
  `ce49399f5f5dc4caf95213f5dd7ec09988f2ae93364817e88ff075a09a22826a`
- Producer: `search/d972_b4_burau_fiber_v2.g`
- Output receipt: `ci/out/d972_b4_burau_fiber_v2.json`

## Workflow contract

1. Keep `workflow_dispatch` with closed choices:
   - `a`: `2` or `4` (default 2)
   - `mode`: `selftest` or `full` (default selftest)
   Also add a `push` trigger restricted to the exact work branch
   `sol/d972-dmtcp-provision-v420` and paths relevant to this dedicated lane.
   This is necessary because GitHub only accepts `workflow_dispatch` when the
   workflow path already exists on the default branch.  A branch push must
   create exactly two matrix lanes, a=2 and a=4.  Each push lane must run
   selftest first and proceed to full only if its own selftest gates pass.
   No arbitrary script, preamble, output path, shell, or URL input.
2. Run on `ubuntu-latest`, least permissions (`contents: read`), checkout with
   `persist-credentials: false`, and a generous but finite job timeout.
3. Install only build prerequisites.  Download all three frozen archives with
   fail/retry flags, verify each exact SHA256 before extraction, and reject
   ambiguous extraction roots.  The required-packages archive has top-level
   package directories such as `./gapdoc/`; extract it under the private GAP
   root's `pkg/` directory.
4. Configure and build GAP 4.16.0 in a temporary job directory.  Install/build
   pinned JSON 2.4.0 under a private GAP package root.  Do not query release
   metadata and do not use `setup-gap`.
5. Gate exact `GAPInfo.Version = "4.16.0"`, successful
   `LoadPackage("GAPDoc")`, and successful `LoadPackage("json")` before
   reading the producer.  Print a provenance marker containing all three
   pinned SHAs.
6. Generate each driver from the closed input/matrix value only, using the producer's
   exact public bindings:
   `D972_B4_BURAU_Q:=5;; D972_B4_BURAU_A:=<2|4>;;`
   `D972_B4_BURAU_MODE:="selftest";;` for selftest, or
   `D972_B4_BURAU_MODE:="run";;` plus
   `D972_B4_BURAU_OUTPUT:="ci/out/d972_b4_burau_fiber_v2.json";;` for full,
   followed by `Read("search/d972_b4_burau_fiber_v2.g");`.
7. Run GAP with `--quitonbreak -q -o 12g`, preserve the real GAP exit code
   through `tee`, and fail closed on any GAP `Syntax error:` or `Error,`
   diagnostic.
8. For selftest, require exactly one exact
   `D972_B4_BURAU_FIBER_V2_GAP_SELFTEST_PASS q=5 a=<a>` marker and exactly one
   exact `D972_B4_BURAU_FIBER_V2_GAP_FINAL_MARKER status=PASS` marker.  For
   full mode, require exactly one parameter-matching `..._DONE q=5 a=<a> ...`
   line, exactly one `..._FINAL_MARKER status=<allowed> output=ci/out/...json`
   line, and a nonempty receipt.  Also
   parse the receipt with Python's standard `json` module and require q=5,
   matching a, 972 unique rows, and a nonterminal/candidate-only producer
   status.  Never promote A or B in the workflow.
   On the push campaign retain separate selftest/full drivers and logs in
   `ci/out/`; any selftest failure must prevent that lane's full invocation.
9. Upload `ci/out/` and the receipt when present, including on failure.  Give
   artifacts unique names containing mode/a/run-attempt so parallel runs do
   not collide.  Logs must not expose credentials.
10. Pin action major versions already used in the repository; do not introduce
    third-party actions beyond checkout/upload-artifact.

## Static acceptance

- YAML parses with an available local parser.
- Shell blocks pass a careful fail-closed audit (especially PIPESTATUS and
  marker counts).
- `git diff --check` is clean.
- Report the exact file hash and every local check performed.  Runtime remains
  for the parent on GHA.
