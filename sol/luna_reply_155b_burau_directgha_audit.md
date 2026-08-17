# Luna reply 155b — independent direct-GHA audit

## Verdict

**PASS.** I found no blocker or high-severity issue that can prevent the lane
from running or create a false A/B result.  The audited workflow SHA-256 is

`850b49a9f6ac10de0a514cb8d711714490a1e4be27fe305caead8328c85d8a85`.

## Audit findings

- The closed `workflow_dispatch` choices are at lines 4–21.  The push trigger
  is restricted to the exact branch at lines 22–29.  The matrix expression at
  line 41 expands a push to exactly `fromJSON(["2","4"])`, while a manual
  dispatch expands only its selected choice; with the two declared triggers it
  cannot duplicate manual lanes.  `set -euo pipefail` at line 54 and the
  unguarded campaign calls at lines 233–238 mean the `return` at line 230
  aborts a failed selftest before that lane can invoke full mode.  Permissions,
  checkout credential handling, runner, and finite timeout are covered at
  lines 31–46.
- The three frozen URL/SHA pairs are exactly present at lines 70–75.  SHA checks
  precede extraction at lines 80–88.  `extract_one_root` rejects ambiguous
  core/JSON roots at lines 90–109 and 118–120; the required-packages archive is
  deliberately checked as a nonempty all-directory top-level set at lines
  121–131 and is placed under the private root's `pkg/`.
- GAP is built from the extracted 4.16.0 source at lines 107–116.  JSON is
  configured and built against that same `gap_src` at lines 131–136, and the
  invocation search path includes the private root.  Driver preamble gates
  exact version plus `GAPDoc`/`json` loads before the producer at lines 143–156.
  The generated bindings and modes match the producer interface (producer
  lines 22–36, selftest markers 169–172, full markers 322–324).
- The GAP invocation uses `--quitonbreak -q -o 12g`; `PIPESTATUS[0]` is captured
  immediately after `tee` at lines 159–163.  GAP `Syntax error:`/`Error,`
  diagnostics are fail-closed at lines 164–172.  Selftest marker cardinality
  is exact at lines 174–187.  Full mode requires the parameter-matching DONE
  and permitted nonterminal/candidate FINAL marker, a nonempty receipt, q/a,
  972 rows with unique target keys, and an allowed status at lines 188–227.
  No A/B promotion is present.
- The evidence upload is `always()` at lines 240–247 and names artifacts by
  event mode, matrix `a`, and run attempt at line 244.  The receipt is within
  the uploaded `ci/out/` tree.  No credentials or user-controlled shell,
  URL, preamble, or output path enters the driver.

## Read-only checks

- Read the complete 155 and 155b task files, workflow, and producer interface.
- PyYAML parse: `YAML_PARSE_PASS` (single `direct-gap` job; dynamic matrix
  expression retained).
- Frozen URL/SHA, exact push branch, and absence of `setup-gap`: all passed.
- Workflow whitespace scan: `WORKFLOW_WHITESPACE_PASS`.
- `git diff --check` was run for the workflow/reply scope; the workflow also
  has no trailing-whitespace lines.  Bash execution was not run locally (no
  local GAP or runtime); the embedded Bash was audited line-by-line, including
  heredoc termination, `PIPESTATUS`, `set -e`, marker counts, and artifact
  failure flow.  Runtime remains for the parent GHA broker.
