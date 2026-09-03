# Root Task661 — Task640 v4 replacement GHA launch receipt

## Failure classification and repair

Task640 v3 run/attempt `33749395427/1`, job `100629227826`, failed before
production at the old Task625 checker replay. All three downloads had passed.
The exact error was a missing
`$RUNNER_TEMP/task625/manifest.json`: Task625's upload has the payload under
`task625-payload/` and its checker verdict at the download root. No Task640
Python arithmetic, rho2 computation, or resource-intensive step ran.

Workflow v4 changes exactly four payload consumers to
`$RUNNER_TEMP/task625/task625-payload` while retaining the verdict at
`$RUNNER_TEMP/task625/task625-verdict.json`. Task660 returned
`PASS_PATH_ONLY / SAFE_TO_DISPATCH_GHA=yes`; its 3,175-byte reply has SHA-256
`73060e6faa04b195c74603986e7f3a65342e7de09edaeb9532591379c7396182`.

## Replacement launch

| field | exact value |
|---|---|
| branch | `sol/r07-explicit-lift-20260825` |
| workflow | `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v4.yml` |
| v4 release commit | `436512709d9183d656827c0abfa926737abaae42` |
| event head | `91eff39e85b3e8e8b771e3ae17b86d224b3f04e9` |
| audited inert v4 SHA-256 | `3a91aca913faf79dadd0e16d181c6e270df660ead0b19acbd6045b2f7cfb92fb` |
| released v4 SHA-256 | `c8deb31cf87554500d665ab6a9740af0529204858d5ec30a91be5b55735dac58` |
| authorized release delta | deletion of the single inert `false &&` line |
| run/attempt | `33750997558/1` |
| job id/name | `100634274219` / `fresh-endpoint` |
| event | `workflow_dispatch` |
| URL | `https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/33750997558` |

The same-workflow push run `33750947320` was `skipped`; there is no duplicate
production run. At the first query the replacement was `in_progress` in exact
event-head checkout.

## Claim boundary

This receipt proves no rho2, grade-two MEMBER/NONMEMBER, A0, full-Q0/order
54,432 solution, compatible cofinal lift, fake, Ihara, cross-check, or Lean
verification. A workflow success remains a candidate until external
run/artifact/checker audit.

`verified=false`
