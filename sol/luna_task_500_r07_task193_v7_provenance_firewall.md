# Luna task 500 - Task193-v7 exact rank99 provenance firewall

Role: Luna implementation only.  Read Task498 audit in full.  Repair only its
one dispatch-blocking provenance defect.  Do not alter the frozen carrier trio,
rank99-v5, Task193 arithmetic/search/resources, Task499/A4, workflows, git,
GHA or production.

## 1. Frozen inputs

The carrier trio is frozen and must remain byte-identical:

- producer 17290 /
  `34983cfaec66f426bdfc63eae5230c27a34f02c847f6154ba81771e6c995b0cd`;
- checker 17400 /
  `fde1cf20ed2111bddabb47abd8fd6c165db3f6e4f4c00a4acf493ceb9c0f169b`;
- driver 3019 /
  `9bb7dc6778517089f3ae77f94a99d065330635552443f8e701f1e9df8dd46b99`.

Rejected Task193-v6 wrappers are exact transformation owners only:

- producer wrapper 5512 /
  `0f1bf66f53d8cd4decdcd28b1ef6c1b185329f1b8b00f9e681bff112d8534fc1`,
  generated body 12282 /
  `2d26dd83c930165f740ec53b621b03d1b57b1232a7b2cd1905730033f4e20341`;
- checker wrapper 5428 /
  `ce735eb1fafb743a53b17ef056b56f4cbd3bf1ff39969dabb5b708c4c43519fb`,
  generated body 7831 /
  `b1e7b9047b839fcf5306cf32bb7876f4d55ef8e5f1eb0c48829a348811911ea3`;
- driver 2840 /
  `5996afa5bd1fed76506d7b46f26f7695a418117f71c40ddf366a7d688279c531`.

The underlying frozen Task193-v5 mathematical owners remain those pinned in
Task496/498.  V7 must transform the exact generated v6 bodies with explicit
pre/post cardinalities; it must not reimplement the core.

## 2. Outputs only

Create only:

1. `search/d972_r07_second_frattini_affine_prefix_compiler_v7.py`;
2. `crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v7.py`;
3. `search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v7.g`;
4. `sol/luna_reply_500_r07_task193_v7_provenance_firewall.md`.

Do not edit v6 or any carrier file.

## 3. Exact producer and independent-checker firewall

In both generated v7 bodies, independently require the following before any
Task193 owner call:

1. carrier `inputs.source_head` is exactly
   `dd6d90b64e2bfba73d7f131f4da876235746f314` and `inputs.run_id` is exactly
   `33553895281`;
2. `artifact = inputs.artifact_id` is string-typed and canonical ASCII
   positive decimal: first character `1..9`, every character `0..9`; no
   hard-coded artifact value;
3. the carrier has the exact complete `upstream` dictionary

   ```text
   schema = d972-r07-a0-dual-anchored-rank99-durable-discovery/v5
   binding = 0e0123e99309a768910e150d5bf4725295a0dc35eab7e15eac66538a3a37d56b
   implementation_commit = dd6d90b64e2bfba73d7f131f4da876235746f314
   production_run_id = 33553895281
   production_artifact_id = artifact
   ```

   with no missing or extra key;
4. carrier `inputs` has exactly the three physical identities
   `v5_result`, `v5_checkpoint`, `v5_checker_log` plus the three provenance
   fields above, preserving the existing canonical identity-shape checks;
5. carrier-checker verdict `inputs` equals the carrier `inputs` exactly; its
   existing schema/status/terminal/carrier-physical-identity/claims/seal gates
   remain mandatory.

The producer `firewall` and checker `boundary` must implement these gates
separately; do not import one another or share a new helper.  Keep the actual
artifact id dynamic but bind the same exact text through receipt, upstream,
verdict and Task193 output provenance.

## 4. Version and confinement

Move only Task193 wrapper/result/checkpoint/checker-verdict schema and marker
names from v6 to v7, add the two provenance predicates, and repin the v7
driver.  The generated v6-to-v7 diff must show no change to affine-prefix
linear algebra, search order, literal carrier mathematics, replay, resource
bounds, checkpoints, output claim meanings, or compatibility views.

The v7 driver remains positive-only: explicit carrier receipt/verdict, one
producer, one post-acceptance independent checker, exact one-line owned
sentinels, nonempty outputs, and UNKNOWN/RESOURCE/ERROR/Traceback rejection.
No fixture/default/retry/pool/fallback or compact-A5 migration.

## 5. Bounded tests

Run AST, exact owner/generated pins, source-patch cardinality and diff
confinement, v7 producer fixture, independent v7 checker self-test, driver
static/pin gate, GAP `ReadAsFunction`, and generated-shell syntax if present.

The fixture must call the actual generated `firewall` and `boundary`, not a
toy predicate, and independently reject at least:

- missing/extra `upstream` key;
- wrong run and wrong head;
- artifact `0`, `00`, `01`, signed, whitespace, non-ASCII digit and integer;
- receipt/upstream artifact drift;
- receipt/verdict artifact, run, head or any of the three physical-identity
  drifts;
- stale v4/v6 carrier dialect and changed binding.

Also retain one honest-shaped dynamic artifact fixture, explicitly
`actual_common=false`; fixture success is not production progress.  Do not run
Task193 heavy computation, A0, production, GHA or git.  Report exact pins and
end with exactly one of:

`TASK500_R07_TASK193_V7_PROVENANCE_FIREWALL_PASS`

or

`TASK500_R07_TASK193_V7_PROVENANCE_FIREWALL_STOP`
