# Luna reply 169: g760 joint-kernel coefficient intersection v1

Date: 2026-08-27  
Role: Luna / implementation and bounded serial mechanical audit  
Outcome: **historical STOP preserved; static GHA bootstrap ready; no mathematical receipt promoted**

## 1. Exact stop

The first clean-overlay producer preflight ended with the exact uncaught
exception

```text
ResourceStop: relation_roster_wall_seconds_cap
```

The wrapper reported

```text
TASK169_PRODUCER_PROBE exit=1 elapsed_ms=618272 output=C:\Users\81905\AppData\Local\Temp\task169_probe_20260827_01.json
```

That output path was not created.  Consequently there is no task-169
preflight terminal token, no certificate SHA, and no measured
`rank_B_joint` or `rank_B_legal_value`.  If this resource stop occurs in the
full-mode exception boundary it maps to
`R07_760_JOINT_COEFF_UNKNOWN_RESOURCE`; this preflight invocation stopped
before a receipt was written and I do not retroactively label it as a
successful full terminal.

At handoff, `python.exe`/`python3` process count was exactly zero.  No full
j=9 computation, GHA dispatch, workflow edit, git operation, or parallel
local Python/GAP run was performed.

## 2. Command and source actually exercised

The syntax gate, run before the bounded probe, was

```powershell
python -B -c "from pathlib import Path; ps=[Path(r'search/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py'),Path(r'crosscheck/check_d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py')]; [compile(p.read_bytes(),str(p),'exec') for p in ps]; print('TASK169_AST_PASS files=2')"
```

with output

```text
TASK169_AST_PASS files=2
```

The serial bounded probe was

```powershell
python -u -B search/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py --preflight --output C:\Users\81905\AppData\Local\Temp\task169_probe_20260827_01.json
```

from the clean pinned overlay
`C:\Users\81905\AppData\Local\Temp\d972_task168_clean_overlay_v1`.
The exercised producer was:

```text
101639 bytes
SHA-256 ab7963922a26ae0ca9aef1adf064e5b69ce4522b5c1766d70a88a58d45bca0e6
```

The exercised checker and driver copies were:

```text
73738 bytes  SHA-256 5c90f13727a0b815dd2c29ab7ecdba2f03ad6901a8bdd1ab150d8e458ee35b3e
21333 bytes  SHA-256 f1e73a156b6c116114291703537b620157594d308e898b904fbd58993e28dfd0
```

The checker and driver selftests were not started after the producer stop.
The required twice-byte-identical preflight was not reached.

## 3. Implemented exact structure before the stop

The versioned producer/checker/driver implement the task-169 structure:

- pins for task 169, proofs v107/v108/v109, all task-168 assets, and the
  complete task-157ee/157ef source/report/checker/driver/q3/full-receipt
  chain;
- exact target context ids 1,2,3 and literal bindings into the frozen
  31-context registry and 46-name alias table;
- the complete 6,318 Cayley-edge, 104 action, and 19 Q0-factor relator
  roster, losslessly encoded as signed-i8 words with per-row provenance;
- action words with the required orientations
  `x^-1 r x s(target)^-1` and `x r x^-1 s(target)^-1`, and action-local
  ordinals 1 through 104;
- literal equality with the frozen 157ee structural rows;
- 27 conjugates of each of 6,441 relators, direct Schreier reconstruction,
  first-input word-bearing F3 echelon rows, and the historical exponent
  intersection;
- the full affine `z` family, its kernel basis, the induced `a` family,
  lexicographically first `a`, and a canonical `z` for that `a` rather than
  collapsing the output to one point;
- actual relation-word materialization and the registered Q0/E3/31-context/
  46-alias/exp3/Sigma/authenticated-D2 replay path;
- adjacent-depth inclusion, including the empty-child case and rejection of
  a nonempty child after an empty predecessor;
- explicit dependence of
  `rowspace = ker(H1(K3;F3) -> H1(Q;F3))` on the v107 normal-presentation
  theorem;
- demotion of reverse-order elimination to an order-independent elimination
  cross-check.  It is not called an independent Q-presentation route; that
  promotion remains `UNKNOWN_NO_THEOREM_INDEPENDENT_ROUTE`.

The implementation also corrected an important typing defect found during
static audit: the retained `B_joint` basis is replayed in the registered
joint kernel without prematurely requiring the exponent gate; exp3 is
required only after forming `B_legal_value`.

## 4. Task-169b static-final exact-transition implementation

The local STOP remains historical evidence against the old source only.  In
task 169b I completed the acceleration in both helper-nonshared routes,
without executing either route:

- the producer resets the exact `Q0 x E3 x E4^31` state to the identity for
  every freely reduced relation and caches only the exact result of one
  authenticated state times one of the four signed marked generators;
- the checker reconstructs the same four signed letters independently and
  uses four letter-indexed exact transition tables rather than the
  producer's combined `(state, letter)` table;
- both routes retain direct legacy `p_eval` and `group.eval` equality
  canaries at global ordinals
  `1, 6318, 6319, 6422, 6423, 6441` and every positive multiple of 257 at
  most 6,441: 31 canaries in total;
- the receipt binds canary ordinals, rows, exact value blobs, row and stream
  digests, exact cache hit/miss counts, and the unchanged complete 6,441-row
  evaluation digest preimage;
- the checker retains the complete 173,907-row RS route and adds an
  exhaustive S3 fixture for all 1,365 signed words of length at most five,
  plus four fail-closed cache/canary/digest mutations.  Its receipt mutation
  total is 23; the producer preflight's registered total remains 19; and
- producer and checker now accept a separate finite positive
  `--domain-seconds`, default 600 and maximum 5,400.  In producer full mode,
  `--seconds` remains exclusively task 168's budget and
  `--domain-seconds` remains exclusively task 169's roster/RS budget.

The frozen, **unexecuted static-final** sources are:

```text
search/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py
110769 bytes
SHA-256 fc6e9a8b52a1122ef9757e3be32206d080ce053a620a93132eca65eb675137c1

crosscheck/check_d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py
87966 bytes
SHA-256 957f49363f78343cc931831013a04ab1ac6b038cbd50497b8d917396d57480ee
```

The checker pins the first identity exactly.  Neither source contains
`TO_BE_FINALIZED`.  Task 169b itself was read at its final normalized
identity:

```text
sol/luna_task_169b_r07_joint_kernel_gha_bootstrap.md
7330 bytes
SHA-256 c11712949a7f750ef5992309f1ea13ab5805d16dd223e08468690922c7d0f33c
```

## 5. New preflight-only GHA bootstrap

The new ASCII driver is:

```text
search/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_gha_preflight_driver_v1.g
26889 bytes
SHA-256 40397ca851cf60f00c03320684f9defdeea051db35d2431764ac61a6dd8b1af4
```

It has 22 exact pins: the controlling task, frozen producer/checker, task
169, proofs v107--v109, all six task-168 immutable assets, and the complete
task-157ee/157ef source/report/driver/full-receipt/q3 chain.  A PowerShell
read-only pin audit found `literal_pin_rows=20 bad=0`; the two variable-path
producer/checker pins were separately byte/SHA equal.  The driver is ASCII
only and has zero placeholder or wildcard pins.

Its exact invocation flags are:

```gap
D972_R07_JOINT_COEFF_GHA_PREFLIGHT_BOOTSTRAP_V1_SELFTEST := true;;
D972_R07_JOINT_COEFF_GHA_PREFLIGHT_BOOTSTRAP_V1_RUN := true;;
```

Exactly one must be true.  The first performs only an in-memory static
fixture audit with ten rejected mutations and starts zero Python processes.
The second is the only bootstrap lane.  It rejects every pre-existing owned
output and every full-mode request, then runs, serially:

```text
producer --preflight --domain-seconds 5400 -> temporary A
producer --preflight --domain-seconds 5400 -> temporary B
cmp A B
checker --check --domain-seconds 5400 --receipt A -> verdict
```

Each Python process has a 5,700-second outer cap, strictly above the
5,400-second domain cap.  The three-process allowance is 17,100 seconds, the
outer computation command is capped at 17,900 seconds, and the registered
driver envelope is 18,000 seconds.  `bash -o pipefail` and
`set -euo pipefail` are explicit.  Before publication, the driver checks two
producer and one checker processes, byte identity, unique process markers,
the exact READY/PASS tokens, target SHA binding, 6,441 relations, 173,907 RS
rows, 31 legacy canaries, mutation totals 19/23/4, resource policy, and all
forbidden positive claims.  Only after those gates does a second serial
command copy A to the canonical `ci/out` artifact and emit A/B/checker logs,
verdict, hashes, timing, stage sentinel, and final sentinel.  Failure logs
are not removed.

## 6. Static audit and execution boundary

Task 169b explicitly prohibited Python, GAP, Node, git, and GHA execution.
Accordingly no new AST/compiler test, producer/checker selftest, driver
selftest, preflight, or checker run is claimed.  The final static checks were
PowerShell reads only:

```powershell
Get-Item -LiteralPath <path>
Get-FileHash -Algorithm SHA256 -LiteralPath <path>
rg -n "TO_BE_FINALIZED|\*\.py|\*\.json|\*\.g" <bootstrap-driver>
```

They returned the exact identities above and zero placeholders/wildcards.
A read-only delimiter/string scan returned:

```text
producer mode=code stack=0 errors=0
checker  mode=code stack=0 errors=0
driver   in_string=False stack_depth=0 errors=0
```

This is a static lexical audit, not a Python/GAP syntax execution and not a
mathematical cross-check.  The old `TASK169_AST_PASS files=2` in Section 2
applies only to the old exercised hashes and is not silently transferred to
the static-final sources.

## 7. Results and UNKNOWN gates

```text
relation roster target                         6441 (registered, unexecuted final route)
RS row target                                  173907 (registered, unexecuted final route)
direct final-word Omega evaluation completed   UNKNOWN (old run stopped; final route unrun)
rank_B_joint                                   UNKNOWN
H1(Q;F3) dimension                             UNKNOWN
rank_B_legal_value                             UNKNOWN
exponent intersection strict                   UNKNOWN
joint coefficient intersection at j=9          UNKNOWN
actual relation-word correction                UNKNOWN
preflight bytes/SHA                            UNKNOWN (no artifact)
helper-nonshared checker PASS                  UNKNOWN / not run
bootstrap static selftest PASS                 UNKNOWN / not run
twice byte-identical generation                UNKNOWN / not run
full j=9 locally                               false
GHA dispatched                                 false
```

Proofs v108 and v109 remain read and pinned but not consumed.  The intended
receipt boundary remains
`true_PB4_D2_equality_used=false` and
`full_E4_positive_class_reconstructed=false`.

The old full driver was intentionally not edited:

```text
search/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_gha_driver_v1.g
21333 bytes
SHA-256 f1e73a156b6c116114291703537b620157594d308e898b904fbd58993e28dfd0
```

It still has three `TO_BE_FINALIZED` pins and must not be dispatched.  It can
be finalized only after the bootstrap returns a twice-identical preflight
artifact whose exact bytes/SHA can be pinned.  No workflow was changed and no
cross-run artifact ingress was added.

joint-kernel coefficient intersection closes registered value gates only

positive target6 modulo projected D2 is not literal A18

Pi4[3] projection and positive PB4 presentation comparison remain gates

all seven relation evaluations and HT1--HT5 remain required

no fake / cofinal lift / Ihara witness declared

R07_760_JOINT_COEFF_GHA_BOOTSTRAP_STATIC_READY
