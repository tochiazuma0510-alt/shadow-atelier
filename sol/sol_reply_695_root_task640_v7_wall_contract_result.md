# Root Task695 — Task640 v7 result and v8 wall-contract release decision

Date: 2026-09-03

## v7 result

GHA run/attempt `33756591288/1`, job `100652403037`, exact event head
`8e5b492acfba7d53a8d36831776d8ec91749ea5c`, concluded `failure`.
Steps 1--10 passed, including the complete accepted Task625 checker replay and
byte comparison.  Step 10 ran from `2026-09-03T12:41:17Z` to
`2026-09-03T12:53:03Z` (11 minutes 46 seconds).

Step 11 invoked the fresh producer and stopped immediately with the typed
terminal

```json
{"error":"wall_seconds_must_equal_9600","status":"NOT_READY"}
```

The fresh producer calls `load_all_seven()`, which constructs the hash-pinned
v12f `Meter`; that constructor requires its frozen `WALL_SECONDS=9600`.
Workflow v7 supplied the global `TASK640_SECONDS=5400`.  No rho2 arithmetic,
resource terminal, checker decision or residual upload occurred.

## Narrow v8 correction

Luna Task694 created only a versioned wrapper successor.  On the single step
`Produce and independently check fresh rho2`, v8 overrides
`TASK640_SECONDS` to `9600`.  The global value remains `5400`; both external
process timeouts remain `45m`; the job timeout remains 120 minutes; all
arithmetic files, hashes, parent identities, caps and commands are unchanged.
Apart from v7-to-v8 labels and artifact names, this two-line step environment
is the whole semantic delta.

The inert v8 workflow is 10,214 bytes / 162 LF lines / SHA-256
`ebc77080a5b51626ea170362bb3b6de441c7530694ce6387fae5a79e0705c5e6`.
Task694's reply is 968 bytes / 19 LF lines / SHA-256
`5e1c0d94ec86d61e14dc7feafcec663164bb8eb0642149ba9fa39f8d29298af4`.
The mechanical YAML check passed.  Root's exact v7/v8 diff confirms no other
semantic change.  This is sufficient for direct release; no broadened code or
mathematical re-audit is commissioned.

```text
V7 TASK625 REPLAY: PASS
V7 FRESH RHO2:     NOT STARTED (typed wall-contract input stop)
V8 WRAPPER:        SAFE_TO_RELEASE
A0 ACTUAL:         0/1
FIRST RUNG:        1/6 cross-checked
FAKE / IHARA:      NOT DECLARED
verified:          false
```
