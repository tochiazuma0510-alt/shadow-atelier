# Sol reply 498 — frozen-pin audit of rank99-v5 COMMON to Task193 handoff

Verdict: `STOP_DO_NOT_ADOPT`.

## Frozen subject authentication

The seven Task498 subjects match exactly:

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_rank99_v5_task193_carrier_v1.py` | 17290 | `34983cfaec66f426bdfc63eae5230c27a34f02c847f6154ba81771e6c995b0cd` |
| `crosscheck/check_d972_r07_rank99_v5_task193_carrier_v1.py` | 17400 | `fde1cf20ed2111bddabb47abd8fd6c165db3f6e4f4c00a4acf493ceb9c0f169b` |
| `search/d972_r07_rank99_v5_task193_carrier_gha_driver_v1.g` | 3019 | `9bb7dc6778517089f3ae77f94a99d065330635552443f8e701f1e9df8dd46b99` |
| `search/d972_r07_second_frattini_affine_prefix_compiler_v6.py` | 5512 | `0f1bf66f53d8cd4decdcd28b1ef6c1b185329f1b8b00f9e681bff112d8534fc1` |
| `crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v6.py` | 5428 | `ce735eb1fafb743a53b17ef056b56f4cbd3bf1ff39969dabb5b708c4c43519fb` |
| `search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v6.g` | 2840 | `5996afa5bd1fed76506d7b46f26f7695a418117f71c40ddf366a7d688279c531` |
| `sol/luna_reply_496_r07_rank99_v5_task193_handoff.md` | 4532 | `0bc486985b8935494bbd30cc4e1e57cf232b8008783d881aedf9ea4012d574dd` |

The Task193-v5 owners also match their frozen pins
`12207/fab51e296170ac34ebe48b49d79d3460017a51cd797d524e7b0d89481f23960f`
and
`7795/941eab0d9c60726436c866427de04b7c25b4ae1934fbf0a1d464f2010a7e2b9e`.
Independent application of every declared replacement with its pre/post
cardinality reproduces the generated bodies exactly:

- producer: `12282/2d26dd83c930165f740ec53b621b03d1b57b1232a7b2cd1905730033f4e20341`;
- checker: `7831/b1e7b9047b839fcf5306cf32bb7876f4d55ef8e5f1eb0c48829a348811911ea3`.

The carrier itself pins the exact rank99-v5 producer/checker/driver and uses
binding `0e0123e99309a768910e150d5bf4725295a0dc35eab7e15eac66538a3a37d56b`,
head `dd6d90b64e2bfba73d7f131f4da876235746f314`, and run `33553895281`.
The job number `100009888831` occurs in none of the six implementation files.
Both carrier-side `artifact_id` parsers independently rejected nonnumeric,
zero, `00`, `01`, signed, whitespace-padded, integer-typed, and drift inputs.

## F1 — Task193-v6 does not rebuild the rank99-v5 provenance firewall

This is a dispatch-blocking defect in both generated Task193-v6 bodies.
Their inherited `firewall` / `boundary` predicates were patched for path and
field names, but not for the new provenance semantics.  They require only the
exact source head plus a *positive digit string* for run/artifact.  They do
not require run `33553895281`, do not require or inspect the carrier
`upstream` record (hence do not bind the v5 schema, binding, head, run, and
artifact), and do not inspect or compare the carrier-checker verdict's
`inputs` record.  In particular, their digit test accepts a leading-zero
artifact id.

An independent in-memory fixture constructed a canonically sealed carrier
receipt with the exact accepted schema/terminal/pins and self-consistent
literal fields, but with

```text
inputs.source_head = dd6d90b64e2bfba73d7f131f4da876235746f314
inputs.run_id       = 1
inputs.artifact_id  = 01
upstream            = absent
```

and a canonically sealed PASS-shaped carrier verdict bound to that receipt
identity.  The exact frozen generated functions both returned normally:

```text
producer_firewall_accepts=true
checker_boundary_accepts=true
```

The bounded reproduction was
`python -B "$env:TEMP\task498_adversarial.py"`; its decisive JSON field was

```json
{"artifact_id":"01","checker_boundary_accepts":true,"producer_firewall_accepts":true,"run_id":"1","upstream_field_present":false}
```

Thus a re-sealed, checker-marker-shaped pair that the actual carrier checker
could never emit crosses both Task193-v6 firewalls.  This directly fails
Task497 sections 2 and 4: canonical dynamic artifact typing and binding
without drift are lost at the handoff, and the independent v6 checker does
not rebuild the new carrier firewall.  The shipped self-tests do not exercise
this case.

## Smallest repair

Make a versioned successor of both Task193 wrappers (and repin its driver),
without changing the frozen affine-prefix owner.  In both the producer
firewall and the independently written checker boundary, require:

1. exact run `33553895281`, exact head, and canonical artifact text matching
   `[1-9][0-9]*`;
2. the exact complete `upstream` dictionary, including v5 schema, binding,
   implementation head, run, and the same artifact text;
3. equality of head/run/artifact and all three physical v5 identities across
   carrier `inputs` and checker-verdict `inputs`, in addition to the existing
   verdict-to-carrier physical identity;
4. independent rejection fixtures for missing `upstream`, wrong run,
   leading-zero artifact, and receipt/upstream/verdict artifact drift.

These are provenance-only replacements permitted by the v417 pin-migration
boundary; no search, replay, resource, Task193, or A0 algorithm should change.

## Other bounded gates

AST parsing, all four supplied fixture/self-test entry points, generated-body
pins/cardinalities, and bounded GAP `ReadAsFunction` parsing passed.  Each
driver statically contains one producer command followed by one checker
command, exact owned sentinels, no fixture/default/retry/pool/selector path,
and UNKNOWN/ERROR/Traceback rejection.  No production, GHA, git, A0, or
Task193 heavy run was performed, and no bytecode cache remains from the
audit.

Mathematics changes: **no**.  The v416/v417 extensional mathematics and all
A0/A2/lift/fake/Ihara claim boundaries remain unchanged; this STOP concerns
only provenance authentication at the Task193-v6 handoff.

TASK498_R07_RANK99_V5_TASK193_HANDOFF_FROZEN_AUDIT
