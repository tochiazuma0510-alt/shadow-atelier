# Luna reply 179 — R07 positive-only common-word column generation v1

Date: 2026-08-27
Role: Luna mechanical implementation / static audit only

## 1. Verdict

**STATIC GO after the run-33051754958 import-collision repair; GHA
re-SELFTEST is pending.**

The five-file task179 bundle is implemented.  The production route is not an
unconditional seal or stub: after exact-pin authentication it calls the live
task175 reconstruction, rebuilds the complete 6,441 relation roster, rebuilds
the task176 `Gamma=243` / `Q0=1,469,664` linked section and singleton
`A_S,L_S,Gamma_S^0` data, and then enters the positive column-generation loop.

I did **not** run Python, Node, GAP, git, GHA, or the full production search
locally.  The earlier bundle passed GHA SELFTEST run `33051614930`; this new
import repair still requires the parent's clean GHA re-SELFTEST before the
production run is restarted.

## 2. Created files and pre-cascade identities

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_positive_common_word_colgen_v1.py` | 90602 | `6b7f98ca696beb1fff1fea9c7942b847b94ce4523e2459ccb4140948ed3b2a08` |
| `crosscheck/check_d972_r07_positive_common_word_colgen_v1.py` | 50059 | `13aaae5a9dcbb7810530cb95fd85905a785e4c75e9c694c621275530864ca009` |
| `search/d972_r07_positive_common_word_colgen_gha_driver_v1.g` | 12357 | `d93bad273efa30d77a3aa144444741174513c886e6a510ad3e5eb3c3325d5414` |
| `search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json` | 407 | `46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78` |

These are the exact identities before the parent performs the authorized
one-time task175/task176 pin cascade.  That cascade necessarily changes the
producer, then the checker's producer pin, then the driver's producer/checker
pins and their three derived hashes.

All four machine assets are ASCII-only, contain no NUL, and contain no
placeholder token.  The fixture parsed as JSON by a read-only PowerShell
static check.  No file outside the five authorized paths was edited.

## 3. Production implementation

The producer implements the following actual path.

1. `build_runtime` (producer line 360) authenticates the fixed sources, calls
   task175's real `run_preflight`, independently reconstructs the task157ee
   joint group/6,441 word roster, and constructs task176's noncontiguous
   deletion, ten contexts, all 243 Gamma states, all 1,469,664 positive Q0
   section states, singleton A/L tables, Gamma kernels, adjusted L words, and
   literal section parents/letters.  It uses task176's packed serializer;
   `value[0]+value[1]` is not used.
2. The target is assembled only as the negative of task175
   `raw_base_targets.H1/H2/P`, with three block tags and two zero exponent
   rows.  `stacked_target` is never used as the target.
3. `AllSevenModel` (line 528) constructs all eleven literal occurrences in
   the fixed H1/H2/pentagon order.  It merges equal
   `(coordinate,target)` terms in F3, deletes zero sums, and compares every
   materialized ACTIVE scalar with a fresh direct all-seven Fox column.
   Its occurrence transport includes the internal base-factor action in each
   positive `g_i*c_i` slot and omits it in each inverse
   `(g_i*c_i)^-1=c_i^-1*g_i^-1` slot, exactly as the left Fox product rule
   requires; the checker rebuilds this sign split independently.
   The task175 110-row table is used only by task175 as a canary, never as the
   full weighted table.
4. `boundary_oracle` (line 867) is a new typed H1/H2/P port.  It does not
   import the old six-component E4 target6 functional.  It builds
   `t=g*h^-1`, requires `t*h=g`, accumulates the complete scalar for a
   translation, and only then materializes an ACTIVE PB3/PB4 column.
5. `FibreOracle` (line 735) performs exact lazy singleton queries against the
   full live Q0 section and A table.  It never infers a multi-coordinate cell
   from singleton independence.  It replays the literal Gamma-plus-section
   word, then runs the powers-of-two kernel-prefix and `K!=0` global
   interleave.  No 357,128,352-element Delta array is materialized.
6. `PositiveSearch` (line 945) provides deterministic append-only F3
   echelon, an exact sparse annihilating dual, coefficient ancestry, ACTIVE
   rank gates, an initial authenticated boundary/correction subset, and an
   atomic full checkpoint after every rank increase.  The checkpoint retains
   input/target/pivot hashes, every literal column, live-fibre roster,
   completed kernel prefix, global cursors, boundary restart semantics, and
   resource counters.
7. A resume input can be passed directly with `--resume`.  The GAP driver also
   accepts the fixed path
   `ci/in/d972_r07_positive_common_word_colgen_checkpoint_v1.json` only when
   `D972_R07_POSITIVE_COMMON_WORD_COLGEN_V1_RESUME_SHA256` is bound and exact.
   The current generic workflow does not download a prior artifact into that
   path, so **cross-run GHA ingress remains operationally UNKNOWN** until the
   parent supplies such an overlay or approved workflow mechanism.
8. On membership the producer recovers coefficients in retained-column
   order, keeps PB3/PB4 chains separate, uses the literal inverse for every
   coefficient 2, forms `reduce(g760+correction)`, and directly replays joint
   kernel membership, both exponent sums, H1, H2, and the five factors in the
   frozen pentagon order.  Boundary words are never inserted into the source
   correction word.

Registered defaults are 19,800 seconds internally (the driver supplies
19,200), 5.7 GB RSS, 8,000,000 boundary pairs, 80,000,000 lazy fibre scans,
2,000,000 candidate words, 250,000 retained columns, and 4 GB checkpoint
bytes.  No withdrawn v136 value (`1536`, `9893376`, or unconditional signed-64
safety) occurs in the bundle.

## 4. Independent checker

The checker does not import the task179 producer.  It loads the independent
task175 checker arithmetic and has separate sparse Gaussian, Fox, word,
weighted-formula, translation, and S3 SELFTEST implementations.

- `independent_formula` (checker line 347) rebuilds all eleven occurrence
  terms and the exponent constant.
- `replay_columns` (line 440) independently rebuilds every boundary or
  correction row, replays the exact active dual, checks `t*h=g`, recomputes
  the complete boundary correlation contributors, and replays every pivot,
  rank transition, and ancestry.
- `validate_common` (line 599) checks the target identity, literal
  coefficient-2 inverse columns, correction word, joint-kernel/exponent
  gates, all seven direct relations, boundary chains, embedded checkpoint,
  and the finite-only claim boundary.
- UNKNOWN validation accepts only typed input/resource terminals, rejects a
  programming exception disguised as UNKNOWN, checks the absence of positive
  and negative claims, and fully replays a checkpoint sidecar when present.

The checker does not repeat an unsuccessful positive search prefix; this is
the v140 positive-witness distinction, not a completeness claim.

## 5. SELFTEST and driver

The immutable fixture is the noncommutative extension
`1 -> A3 -> S3 -> C2 -> 1`.  Its two relation blocks and ordered three-factor
product exercise the actual sparse dual, boundary ACTIVE path, singleton
support section, kernel-prefix path, nonzero exponent/global path, rank
increase, coefficient-2 word inversion, checkpoint, and positive receipt.

Producer and checker each route the 15 commissioned mutations through their
normal semantic validator.  The independent checker mutation entry point is
at line 849.  No whole-dictionary equality oracle is used.

The ASCII GAP driver is strictly serial.  It rejects stale owned artifacts,
authenticates every registered source, uses exact unwrapped child markers,
caps the producer/checker sequence below six hours, rejects traceback/STOP
logs, and disables GAP console formatting before the final exact sentinel.
It does not dispatch or alter a workflow.

Suggested parent preambles after the pin cascade are:

```gap
D972_R07_POSITIVE_COMMON_WORD_COLGEN_V1_MODE:="SELFTEST";;
Read("search/d972_r07_positive_common_word_colgen_gha_driver_v1.g");
```

and, only after SELFTEST passes and task175 is repaired:

```gap
D972_R07_POSITIVE_COMMON_WORD_COLGEN_V1_MODE:="PRODUCTION";;
Read("search/d972_r07_positive_common_word_colgen_gha_driver_v1.g");
```

Allowed producer terminals are exactly:

```text
R07_POSITIVE_COMMON_WORD_COLGEN_COMMON_WORD
UNKNOWN_RESOURCE:<registered phase and cap>
UNKNOWN_INPUT:<authenticated missing or malformed input>
```

There is no separator terminal.  Uncaught implementation exceptions remain
hard nonzero STOPs.

## 6. Concrete predecessor blocker

The commission pins are intentionally still present, but both predecessor
bundles drifted during their authorized repairs:

- task176 commission pins were `63872/5cf5617b...`,
  `82983/892b9b2e...`, `15817/9d854d02...`; the successful final task176
  sources visible at freeze were instead
  `66109/878cf1d8...`, `84980/4e6b97aa...`,
  `15929/1c6dc7f1...` (parent reported production run 33044121344,
  receipt `13649089/715441d8...`, Gamma 243, Q0 1,469,664,
  full D 357,128,352, cross-checked).
- task175 commission pins were `57132/ef0df11b...` and
  `79414/4b6cd610...`; the live repair sources at freeze were
  `59707/b3947094...` and `85848/c55ec99a...`.  Parent reported run
  33042556905 ended hard nonzero without a checker log, so no positive
  task175 receipt exists yet.

Accordingly the current bundle is correctly fail-closed and must not be
presented as runtime PASS.  Parent should finish task175, freeze task175 and
task176, update those six identities once, cascade task179 producer/checker/
driver hashes, then run SELFTEST.  No mathematical negative conclusion follows
from this blocker or from any later `UNKNOWN_RESOURCE` checkpoint.

## 7. Claim boundary

Even a future `COMMON_WORD` proves only the finite universal B4 all-seven word
of v110/v140 and supplies v129's intrinsic `(d,rho)` saturation input.  It is
not a cofinal lift, fake, Ihara witness, or proof about all 972 shadows.

## 8. Parent audit and final live-source pin cascade

This section supersedes the predecessor blocker in Section 6 for source
identity only. Parent audited the task182 coarse inverse, the v143 weighted
support theorem implementation, typed UNKNOWN resource handling, and
checkpoint resume semantics. A nonzero checkpoint remainder reconstructs its
exact dual from the retained basis and binds the stored dual, dual digest,
correction-progress digest, completed-row cursor, and coordinate-specific
kernel cursor. Exhaustion of a guaranteed `W+1` prefix is a hard invariant
failure, never typed UNKNOWN.

The final live predecessor pins cascaded into producer, checker, and driver
are:

| bundle | producer | checker | driver |
|---|---|---|---|
| task175 | `60306 / 1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa` | `88503 / 0b45c3daa1db6cad63d434170c65d0dbfa928efc51543b881dc0aa2e3a0f1fce` | `22052 / 919e7a9efe7385444c480203dc51525873e770236777dd61e2f6fc1ef22de494` |
| task176 | `66109 / 878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b` | `84980 / 4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695` | `15929 / 1c6dc7f10d9b27092c2441a274ff74726d8899599ac10c2b8cc47cb59da02995` |

Final task179 source identities after that ordered cascade are:

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_positive_common_word_colgen_v1.py` | 123,870 | `47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7` |
| `crosscheck/check_d972_r07_positive_common_word_colgen_v1.py` | 73,780 | `de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d` |
| `search/d972_r07_positive_common_word_colgen_gha_driver_v1.g` | 12,872 | `48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b` |
| `search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json` | 407 | `46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78` |

Static verdict after parent audit is `STATIC GO / execution pending`.
Neither Python nor GAP has been run locally. GHA SELFTEST and production
receipts remain the next evidence gates.

## Follow-up checker audit (parent GHA)

Parent GHA SELFTEST run `33050709958` at head `8fcce352` failed only in the
checker: independent weighted mutation #8 set
`weighted_support.W_plus_1_impossible.typed_unknown=True`, but the checker
omitted that field from `validate_selftest` and accepted the mutation. The
checker now requires `typed_unknown=False` and
`hard_invariant_failure=True`; accepted-mutation diagnostics include the
ordinal. The producer/checker/driver marker counts remain 15 ordinary plus 8
weighted mutations.

Post-repair identities:

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_positive_common_word_colgen_v1.py` | 119,396 | `4dcae739a8d1181341ae90a7375e7ca7c465d404582e53a24b6fc84ab7a3f5f4` |
| `crosscheck/check_d972_r07_positive_common_word_colgen_v1.py` | 70,020 | `9cd543debaa7893c807cd7eec8af6fa200241c61d13bc42b5418a7826a839974` |
| `search/d972_r07_positive_common_word_colgen_gha_driver_v1.g` | 12,974 | `cfa8c36b6139e501cad34e5a6515e749fdf6f59febc2c56e3d298ba0420a63ec` |
| `search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json` | 407 | `46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78` |

No local Python/Node/GAP/git/GHA execution was performed for this repair.

## Driver-only GHA repair

Re-SELFTEST run `33051307164` at head `c0593608` reached producer PASS and
checker PASS with exact 15 ordinary plus 8 weighted markers. The driver then
failed because `SetPrintFormattingStatus(OutputTextUser,false)` is not a GAP
4.16 method. The final sentinel now uses the supported
`WriteLine(OutputTextUser(),Concatenation(...))` form.

Updated driver identity: 12,872 bytes,
`fbab67e85de604f157f8bd93f53d64e7265121508aa948c1e01341e78d1b5a11`.
No producer/checker changes were made in this repair; local execution and
git/GHA remain forbidden.

## Final predecessor repair cascade before rerun

Task175 production run `33047989700` subsequently exposed and rejected a
producer-only bare-name error after `roster_replayed`: `add_scaled` was not
defined. The repaired call is the authenticated predecessor API
`old.add_scaled`; task175 producer/driver are now respectively
`60306 / 1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa`
and
`21580 / dbe147f98774fde50dee86de7306f9e18243ac1becef0ec7516765bcb2e08765`.
The task175 checker is unchanged.

After cascading those pins through task179 producer, the repaired independent
checker, and the driver in that order, the identities for the next GHA rerun
are:

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_positive_common_word_colgen_v1.py` | 119,396 | `448123e3ccba4324f4d19a09eeb6a2ba217d611ef5053d4cfa27e61ac69a2512` |
| `crosscheck/check_d972_r07_positive_common_word_colgen_v1.py` | 70,020 | `473bad89f9656dd67f4313398b5bdbb253a3495e1e20855d90781b4875309f2d` |
| `search/d972_r07_positive_common_word_colgen_gha_driver_v1.g` | 12,974 | `eee30a3f482704799dee75e0b0663ceb53b27f3e420d2413cca7bb08262f37fa` |
| fixture | 407 | `46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78` |

Both failed runs are implementation evidence only. Static status is
`STATIC GO / GHA re-SELFTEST pending`.

## Ultimate identities for the next GHA rerun

The driver-only GAP stream repair occurred after the cascade table immediately
above. The authoritative next-run quartet is therefore:

- producer: `119396 / 448123e3ccba4324f4d19a09eeb6a2ba217d611ef5053d4cfa27e61ac69a2512`;
- checker: `70020 / 473bad89f9656dd67f4313398b5bdbb253a3495e1e20855d90781b4875309f2d`;
- driver: `12872 / fbab67e85de604f157f8bd93f53d64e7265121508aa948c1e01341e78d1b5a11`;
- fixture: `407 / 46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78`.

## Parent GHA SELFTEST PASS and production launch

The repaired bundle passed GHA SELFTEST run `33051614930` at head
`731a950b5f1aa91b3817f9bb70ec8c3de50c3beb`. The exact three external
markers are:

```text
R07_POSITIVE_COMMON_WORD_COLGEN_V1_PRODUCER_SELFTEST_PASS mutation_attempted=15 mutation_rejected=15 coarse_inverse_checks=4 weighted_mutation_attempted=8 weighted_mutation_rejected=8
R07_POSITIVE_COMMON_WORD_COLGEN_V1_CHECKER_SELFTEST_PASS mutation_attempted=15 mutation_rejected=15 coarse_inverse_checks=4 weighted_mutation_attempted=8 weighted_mutation_rejected=8
R07_POSITIVE_COMMON_WORD_COLGEN_V1_GHA_DRIVER_PASS mode=SELFTEST terminal=SELFTEST
```

Downloaded artifact identities include:

- receipt: `7511 / b237427153c71b23fb56d36828f3eeaf7f09139b3df68d16a1c2262afadb2cc8`;
- helper-nonshared verdict: `367 / 815c223c956eecb202015e10fd6dffeed1e786cd13e39ef4b2a1d5697e685973`;
- producer log: `184 / 06a69378c5af25cc6ac002103c89acdd2e702c796ca4266b4b09678024b0fa4f`;
- checker log: `183 / afe29d0e609d4a7b5e3b09d401d8f9cacb1c5bd715d342f3ffb1034c67ec9894`;
- run log: `450 / 72cc2645d742b87a22fedc7b0d49e4d9709365975cb7c51c053652992879fc9e`.

This promotes the finite bundle to `SELFTEST PASS`. Parent launched the
actual production search as run `33051754958` at the same head, concurrently
with task175 production run `33051614970`. Both production outcomes remain
pending; no finite common word, cofinal lift, fake, or Ihara witness is yet
declared.

## Production run 33051754958 import-collision repair

This section supersedes the final sentence immediately above. Production run
`33051754958`, head
`731a950b5f1aa91b3817f9bb70ec8c3de50c3beb`, failed after approximately 82
minutes and before `PositiveSearch`/column generation. The exact first error
was:

```text
AffineInput: authenticated module name already bound: _d972_157ed_old_producer
```

The deterministic call chain was old producer `build_runtime` line 471 ->
`prev.authenticated_input(v172.Q3)` -> predecessor
`load_pinned_module(..., "_d972_157ed_old_producer")`. Task175's earlier
`run_preflight()` had already authenticated and registered that exact module;
the second call rejected its own fixed name. This is an import lifecycle bug,
not a failed mathematical gate.

The repair is deliberately narrow.

1. Producer lines 144--226 now authenticate a module's path, byte count, and
   SHA before loading. Repeating the same `(name,path,pin)` reuses the exact
   bound object; the same name with a different pinned path is a hard
   collision.
2. At producer lines 466--467, the task175-bound
   `_d972_157ed_old_producer` is reused only after its on-disk source is
   checked against the exact task179 seedspan pin. The second
   `authenticated_input` call is gone.
3. Producer lines 495--515 bind v172's Q3 and predecessor constants to the
   task179 pins, reconstruct the literal 6,441-row roster with the reused
   arithmetic, and require exact serialized equality with task175. These
   collision/roster gates now run before Gamma/Q0 enumeration, so this failure
   class cannot consume the later expensive section preamble again.
4. The production input/checkpoint records the authenticated reuse policy.
   Checker lines 878 and 955 require that exact record for checkpoint and
   COMMON_WORD validation.
5. Producer and helper-nonshared checker each execute a bounded real loader
   control in SELFTEST: same-name/same-path is imported twice and must return
   the same module; same-name/different-pinned-path must be rejected. The
   checker independently executes its control and binds it to the producer
   receipt. No producer helper is imported by the checker.

Run `33051754958` stopped before `PositiveSearch` was constructed, hence it
created no authenticated task179 column checkpoint that can safely skip the
preamble. The existing resume contract starts from a post-preamble column
state and does not serialize live Gamma/Q0 Python objects. Therefore no
fabricated cache was added: the next job must reconstruct the preamble once.
The repaired ordering merely moves all collision-prone import/roster gates
ahead of the expensive Gamma/Q0 enumeration.

Final repaired machine identities are:

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_positive_common_word_colgen_v1.py` | 123,870 | `47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7` |
| `crosscheck/check_d972_r07_positive_common_word_colgen_v1.py` | 73,780 | `de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d` |
| `search/d972_r07_positive_common_word_colgen_gha_driver_v1.g` | 12,872 | `48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b` |
| fixture | 407 | `46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78` |

No local Python/Node/GAP/git/GHA execution was performed for this repair.
Current status is `STATIC GO / repaired SELFTEST and production pending`.
The final cascade also binds the task175 PB3 repair committed at
`9ec72d68f3ba99fbfe2d2bebfd5d78e0dcf2deea`; task175 files themselves were
not edited by task179.

## Parent production audit 2026-08-28

Run `33059993513`, head
`3d5bd79e9c4647e1166d5f5c8cd73d4d21889525`, completed its producer with the
typed terminal

```text
UNKNOWN_RESOURCE:phase=positive_boundary_correlation:cap=wall_seconds:value=19212.567360263998:limit=19200.0
```

The job then exhausted its outer window before the independent-checker
sentinel and uploaded no artifact.  This is neither `COMMON_WORD` nor a
nonmembership certificate: it says only that the exact complete-boundary
correlation was still running at the registered wall cap.  The task192 cached
successor is the versioned continuation of this schedule.  No lift, fake, or
Ihara claim is promoted from this run.

## Repaired import-control SELFTEST PASS and production relaunch

The final repaired bundle passed GHA SELFTEST run `33059348708` at head
`95601cd88071a2422f5123cc21fac12f391c1ae0`.  The artifact contains the
exact producer, independent-checker, and driver PASS markers, with all 15
semantic and all 8 weighted mutations rejected.  The producer receipt and
independent verdict additionally bind

```text
same_name_same_path_reused=true
same_name_cross_path_rejected=true
second_authenticated_input_call=false
module_import_double_cross=true
```

Thus the exact collision class from run `33051754958` is now exercised on
both routes and rejected at the committed source identities.  This promotes
the repaired bundle to `SELFTEST PASS`.

Parent launched the fresh production search as run `33059993513` at head
`3d5bd79e9c4647e1166d5f5c8cd73d4d21889525`.  The task179 machine files at
that head are byte-identical to the SELFTEST bundle; the intervening commit
adds only the Sol paper theorem v155.  Production is pending.  No
`COMMON_WORD`, cofinal lift, fake, or Ihara witness is claimed by the
dispatch.
