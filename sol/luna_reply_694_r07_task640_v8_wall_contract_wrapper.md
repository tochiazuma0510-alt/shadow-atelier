# Task694 reply

Created the narrow v8 wrapper from accepted v7. The global
`TASK640_SECONDS: "5400"` remains unchanged; only the `Produce and independently
check fresh rho2` step receives `TASK640_SECONDS: "9600"`. Both `45m` process
timeouts and the 120-minute job timeout are unchanged.

The only other differences are the required mechanical v7-to-v8 workflow
name, self-path, fire marker, authentication label, and two artifact names.
Producer/checker hashes, arithmetic/source pins, parent replay, limits,
commands, actions, downloads, copies, and uploads are unchanged. The raw diff
is six one-line label replacements plus the two-line step-local environment
block (`8 insertions, 6 deletions`).

Safe YAML parsing passed. Text scans confirmed one global value 5400, one
step-local value 9600, two 45-minute commands, the 120-minute job timeout, and
unchanged producer/checker SHA pins. No dispatch, commit, or push was used.

READY_FOR_SOL_WALL_CONTRACT_AUDIT
