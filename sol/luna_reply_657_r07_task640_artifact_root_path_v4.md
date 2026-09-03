# Luna Task657 reply

Created the versioned v4 workflow with only the authorized mechanical v4
identity/output-label changes and four Task625 payload-root corrections. The
uploaded verdict remains at `$RUNNER_TEMP/task625/task625-verdict.json`; the
old checker payload, replayed-verdict destination, producer `--task601`, and
new checker `--task601` now use
`$RUNNER_TEMP/task625/task625-payload`.

No Python, mathematics, existing workflow, GHA, or git operation was changed.

Workflow: 10,038 bytes / 161 LF lines / SHA-256
`3a91aca913faf79dadd0e16d181c6e270df660ead0b19acbd6045b2f7cfb92fb`.
Changed lines are 1 (workflow name), 10 (self path), 41 (fire marker), 54
(step label), 125 (old-checker payload), 127 (replayed verdict destination),
136 and 140 (both `--task601` roots), and 147/157 (output labels). Lines
123/127 retain the top-level uploaded verdict. Task659 restored the missing
line 40 `false &&`; beyond that inert line, a v3/v4 normalized diff showed no
other semantic delta.

Bounded YAML safe parse, exact path census, full-SHA action scan, and inert
guard check: PASS. This reply's final self-hash is supplied out of band.

READY_FOR_TASK658_PATH_ONLY_AUDIT
