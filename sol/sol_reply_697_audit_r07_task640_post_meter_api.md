# Sol(max) Task697 — bounded post-Meter API compatibility audit

## Verdict

`verified=false`

There is one deterministic post-Meter interface failure.  The v8 wrapper
repairs construction of the pinned v12f `Meter`, but the producer then returns
a light runtime without the deletion map required by
`ProducerAllSeven.coordinates`.  The first empty-path signature must therefore
stop before endpoint or precision-two arithmetic begins.

## Exact inputs

| path | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 27,899 | 312 | `684c629eef8100175b676a4e4762db18f67e5a99672b4107facc7dad412acfc2` |
| `search/d972_r07_history_free_positive_fast_resume_v12f.py` | 343,155 | 6,472 | `22d2ebda554cfacc78393dda7f43a9a6550e7f134dd8f44f87ab0f62241bbbbb` |
| `search/d972_r07_a0_first_rung_grade2_prebuild_v1.py` | 145,917 | 3,499 | `acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v8.yml` | 10,214 | 162 | `ebc77080a5b51626ea170362bb3b6de441c7530694ce6387fae5a79e0705c5e6` |
| transitive `search/d972_r07_a0_first_rung_grade1_v4.py` API source | 144,552 | 3,326 | `1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4` |

The producer and workflow hashes equal the frozen Task697 values; the v12f
and prebuild hashes equal the producer's embedded pins.  Workflow line 130
sets the production step's `TASK640_SECONDS` to `9600`, which exactly meets
v12f `Meter.__init__(seconds)` at lines 538–543.  Thus the former Meter error
is not this failure.

## Deterministic failure

`load_all_seven` has these actual return types:

- the dynamically loaded v12f module;
- a `v12f.ProducerAllSeven` instance;
- the `dict[str, Any]` returned by `v12f.build_light`.

At producer lines 95–96, only `build_light(registry, meter)` is called before
constructing and returning the model.  The exact light-runtime literal at
v12f lines 1185–1190 contains `live`, `p176`, `old`, `e3`, `e4`, `contexts`,
`aliases`, `context_public`, `bridge`, `roster`, `joint_group`, `q3`, `meter`,
`q3_literal_owner`, and `joint_receipt`; it contains no `delete` entry.
Creating `ProducerAllSeven(runtime)` itself does not read `delete`, so that
step can finish.

The first use is producer line 226:

```python
trie = {(): signature((), all_seven)}
```

`signature` calls `ProducerAllSeven.coordinates`.  That method unconditionally
evaluates `self.rt["delete"]` at v12f line 984.  Since no intervening call can
install the key, Python must raise `KeyError('delete')`; `main` catches it and
reports `NOT_READY`.  This is independent of downloaded data and occurs before
the endpoint gate, `direct_column`, bucket arithmetic, dense replay, target
construction, or rho2 publication.

The pinned v12f lifecycle installs the required map only in
`build_heavy(runtime, registry, meter)`: it constructs the fine deletion at
lines 2917–2922 and publishes `runtime["delete"]` at line 2993.

### Single minimal repair

In `load_all_seven`, immediately after producer line 95 and before returning
or using `ProducerAllSeven`, add the one missing pinned lifecycle call:

```python
runtime = module.build_light(registry, meter)
runtime = module.build_heavy(runtime, registry, meter)
return module, module.ProducerAllSeven(runtime), runtime
```

This audit makes no time/RSS prediction for that call; resource feasibility is
outside Task697.  A different repair would have to construct and bind exactly
the same authenticated deletion API and is not established by the frozen
code.

## Remaining API/shape census

Conditioned only on supplying that required runtime member, no second
deterministic API mismatch was found:

- `coordinates(word)` accepts a signed-word sequence and returns the ten
  packed coordinate blobs produced by `eval_word_coordinates`; `signature`
  selects `TEN=(0,1,2,3,0,4,5,6,7,8,9)` to form six E3 plus five E4 entries.
- `producer_unpack_element(runtime, raw, block)` and
  `producer_element_blob(runtime, value)` have the exact four- and two-argument
  shapes used by `extend_signature`; E3 uses blocks 1/2 and E4 block 3.
- E3/E4 provide `identity`, `mul`, `inverse`, and `eval`; `packed_joint_blob`
  accepts `(value, label)`.  The endpoint comparisons are therefore byte/blob
  compatible.
- `direct_column(delta_word, relator_word)` accepts the two sequences passed
  at producer line 242 and returns `(dict[bytes,int], dict[str,Any])`; ignoring
  that return value is legal.
- `grade1.Context(words)` exposes the six-entry `aggregate_table`,
  `physical_shifts`, and `source_word_tags(word)`.  `affine_inv(value)` and
  `affine_mul(left,right)` exactly match the first-six base-gate calls.
- `evaluate_seed_precision2(context, word)` returns four arrays with source
  shapes; `act_precision2(context, degree0, degree1, degree2, auxiliary,
  tag_actors)` consumes those shapes; `aggregate_precision2` returns physical
  widths `8064`, `24192`, `48384`, and `4` matching the replay buffers.
- `direct_target_precision2(context, words)` returns the same four physical
  shapes.  `grade1.pack_trits(row)` and `unpack_trits(row, width)` match the
  48,384-trit / 12,096-byte rho2 calls.

No data-dependent mathematical outcome, resource duration, checker behavior,
or general hardening receives a verdict.  No heavy execution, code change,
GHA operation, or git operation was performed.

FAIL_POST_METER_API
