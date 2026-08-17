# Luna reply 155c — focused workflow expression/control-flow audit

## Verdict

**PASS.** No blocker or high-severity issue was found in the requested
push/matrix/context/control-flow scope.  The audited workflow SHA-256 is:

`850b49a9f6ac10de0a514cb8d711714490a1e4be27fe305caead8328c85d8a85`

## Findings

- **Push trigger and path filter (lines 22–29): PASS.** The trigger is
  restricted to the exact branch `sol/d972-dmtcp-provision-v420`, and the
  filter includes the workflow itself at line 26 plus the producer, worker,
  and frozen artifact paths.  A push adding this workflow therefore matches
  its own path filter on that branch.  The manual-dispatch default-branch
  registration requirement is external GitHub repository state, not a defect
  in the push trigger.

- **Dynamic matrix (line 41): PASS.** On `push`, the GitHub expression selects
  the valid JSON string `["2","4"]`, yielding exactly two lanes.  On
  `workflow_dispatch`, it formats the single closed `inputs.a` choice into a
  one-element JSON array, yielding exactly one lane.  The closed choices and
  defaults are defined at lines 5–21; no arbitrary matrix value is accepted.

- **Expression contexts: PASS.** `github.event_name` is available in the
  strategy, environment, and artifact expressions; `inputs.a`/`inputs.mode`
  are available for manual dispatch and are selected only on the non-push
  branch; `matrix.a` is available in job steps and artifact naming; and
  `github.run_attempt` and `always()` are valid at the upload step (lines
  241–247).  The push/manual conditional prevents absent manual inputs from
  controlling push lanes.

- **Bash, heredoc, and exit propagation: PASS.** The script enables
  `set -euo pipefail` at line 54.  The embedded Python heredoc (lines
  200–223) has a valid column-zero `PY` terminator after YAML block
  indentation is removed.  The GAP pipeline is deliberately placed under
  `set +e`, captures `PIPESTATUS[0]` immediately after `tee` (lines 159–163),
  then restores `set -e`.  Diagnostic, exit-status, marker, and receipt gates
  all set `gate_status` and return it (lines 164–230).

- **Selftest-before-full proof: PASS.** In campaign mode, line 234 calls
  selftest before line 235 calls full.  These are unguarded sequential shell
  commands under the caller's restored `set -e`; a nonzero selftest return
  exits the job before the full call.  Exact selftest marker cardinality is
  enforced at lines 179–187.

- **Artifact isolation and promotion safety: PASS.** The artifact name at
  line 244 includes event mode, matrix `a`, and `github.run_attempt`; the two
  push lanes therefore cannot collide, and distinct workflow runs have
  separate artifact namespaces.  The workflow only accepts the producer's
  nonterminal `UNKNOWN_*`, `UNKNOWN_RESOURCE`, or candidate status in its
  receipt gate (lines 216–222).  It performs no checker invocation or A/B
  promotion; candidate output remains candidate evidence.

No workflow file, GAP run, GHA dispatch, or git operation was performed for
this audit.
