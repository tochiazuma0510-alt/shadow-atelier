# Luna reply 496 - rank99 v5 to Task193 handoff

Status: `TASK496_R07_RANK99_V5_TASK193_HANDOFF_PASS`

Task496 was implemented within the seven-file scope.  The two paused Task493
scratch copies were removed only after their required size and SHA-256 checks:

| removed scratch | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_rank99_v4_task193_carrier_v1.py` | 8553 | `18c4932cbff5fbd5885ea03e80cd7f5c9f9c10bdbf4c7cc043985d3196042644` |
| `crosscheck/check_d972_r07_rank99_v4_task193_carrier_v1.py` | 8516 | `82c5e7caa314e530782843bef81e66c431198fdc2d1c479886a14166f0fa1e73` |

## Final output pins

| output | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_rank99_v5_task193_carrier_v1.py` | 17290 | `34983cfaec66f426bdfc63eae5230c27a34f02c847f6154ba81771e6c995b0cd` |
| `crosscheck/check_d972_r07_rank99_v5_task193_carrier_v1.py` | 17400 | `fde1cf20ed2111bddabb47abd8fd6c165db3f6e4f4c00a4acf493ceb9c0f169b` |
| `search/d972_r07_rank99_v5_task193_carrier_gha_driver_v1.g` | 3019 | `9bb7dc6778517089f3ae77f94a99d065330635552443f8e701f1e9df8dd46b99` |
| `search/d972_r07_second_frattini_affine_prefix_compiler_v6.py` | 5512 | `0f1bf66f53d8cd4decdcd28b1ef6c1b185329f1b8b00f9e681bff112d8534fc1` |
| `crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v6.py` | 5428 | `ce735eb1fafb743a53b17ef056b56f4cbd3bf1ff39969dabb5b708c4c43519fb` |
| `search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v6.g` | 2840 | `5996afa5bd1fed76506d7b46f26f7695a418117f71c40ddf366a7d688279c531` |

The v6 source-patched mathematical bodies are pinned as producer
`12282/2d26dd83c930165f740ec53b621b03d1b57b1232a7b2cd1905730033f4e20341`
and checker
`7831/b1e7b9047b839fcf5306cf32bb7876f4d55ef8e5f1eb0c48829a348811911ea3`.
Both are generated solely from the frozen Task193-v5 owners
`12207/fab51e296170ac34ebe48b49d79d3460017a51cd797d524e7b0d89481f23960f`
and
`7795/941eab0d9c60726436c866427de04b7c25b4ae1934fbf0a1d464f2010a7e2b9e`.

## Authenticated upstream

The carrier authenticates the exact v5 discovery trio:

- producer: `104031/25c308ec11b9f36cc9779dfec46058a4956068969d664ee582a26f9cb0db7c09`;
- checker: `71589/970ffe3a78687f3a27a222e089ae3d5e928bbfa048b9aef9f51fcf4c0b5d578d`;
- driver: `9425/bed9105b36fef5e59120d954029ec507b16f393ab2859a7599867a19156b1b5d`.

Binding is `0e0123e99309a768910e150d5bf4725295a0dc35eab7e15eac66538a3a37d56b`;
implementation/source head is `dd6d90b64e2bfba73d7f131f4da876235746f314`;
the active upstream premise is run/job `33553895281 / 100009888831`; the latter
is retained only as the job premise, never as an artifact id.  Production
`--artifact-id` is explicit, canonical positive decimal text, with no
hard-coded value, and the exact text is bound into the carrier receipt,
`upstream.production_artifact_id`, and the independent checker verdict.
The carrier requires the v5 schema, producer COMMON marker, exact checker PASS
line, physical result/checkpoint/log identities, sealed durable state, and the
pinned checker replay before reconstructing the literal carrier.  All stale,
missing, malformed, old-schema/v4, or negative inputs return `UNKNOWN_INPUT`
with all A2/lift/fake/Ihara claims false.

## Bounded verification

- AST parsing of both carrier programs and both v6 wrappers: PASS.
- v5 producer `--mode FIXTURE`, v5 checker `--pin-check`, and v5 checker
  `--self-test`: PASS.
- Carrier producer `--fixture`: PASS; output explicitly contains
  `actual_common=false` and no production terminal.
- Independent carrier checker `--self-test`: PASS; mutation gates cover
  identities, v5 schema/markers, provenance, literal/exponent, physical replay,
  digest, ancestry, right-product, carrier seal, verdict seal, and artifact-id
  nonnumeric/zero/drift rejection.
- Task193-v6 producer `--fixture`: PASS with `actual_common=false`.
- Independent Task193-v6 checker `--self-test`: PASS with
  `actual_common=false`.
- Final pin/driver static gate: PASS; each driver has exactly one producer and
  one post-acceptance checker invocation, exact one-line owned sentinels,
  UNKNOWN/ERROR/Traceback rejection, no fixture/default input, and exact
  current pins.
- GAP `ReadAsFunction` parse through `gap.ps1` for both new drivers: exit 0
  (`TASK496_GAP_PARSE_PASS`; only normal unbound-global warnings).
- Old-schema/v4 rejection fixture: PASS (`UNKNOWN_INPUT`, all claims false).

No production run, GHA dispatch, git operation, persistent fixture, or actual
COMMON result was performed.  Mathematical status is unchanged.

TASK496_R07_RANK99_V5_TASK193_HANDOFF_PASS
