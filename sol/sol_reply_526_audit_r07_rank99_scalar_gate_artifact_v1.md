# Sol(max) reply 526 -- rank99-v7 scalar-gate artifact audit

## Verdict

`AUDITED_ZERO_PROGRESS_WITH_CONTAINED_REGRESSION`

Run `33570220633` ended in canonical claims-false
`UNKNOWN / correction:scalar_gates`. Its returned checkpoint is a new READY
wrapper/seal around exactly the input rank99 prefix, with no appended row,
batch, segment, rank, count, or round. Therefore it made **zero durable prefix
progress**. The defect is contained in the retired rank99 custom
formula/selector lane; none of that lane is authority for the current rank111
lazy K=0 work.

This is not a nonexistence result and promotes no prefix, COMMON word,
NONMEMBER result, compatible lift, fake witness, or Ihara witness.

## F1. Artifact authentication -- PASS

Commissioned outer identity:

```text
run/job       33570220633 / 100062348518
head          4d57c024df74b257e5b4e724b69e6c4d51ff667f
artifact      9828236283 / gap-run-out
API size      26278 bytes
service SHA   sha256:d87bb87fa3b8749b46a72884adb869e159d52c278c025015406337954499ca49
```

The exact head is a local commit (`Promote audited rank99 global-selector
repair`). The v7 producer/checker/driver worktree blobs equal their blobs at
that head. The service SHA above is the supplied GitHub digest of the absent
compressed container, so I do not claim to have recomputed it from extracted
members. I independently authenticated the extracted payload: exactly six
regular files, 371,054 bytes total.

| member | bytes | SHA-256 |
|---|---:|---|
| `d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.checkpoint` | 356142 | `1cdbcbdc789e69f8b49b314c3dc3c3d91853fd5fd170863af77c8d5f10eb5fa7` |
| `d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.json` | 389 | `38f6fdd148c5be85bd3eea44027a87c2774c642c02adbd252d46551436bf53a1` |
| `d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.producer.log` | 4051 | `f603686691bd78a5b6328760fefac80bd07f2c72c13cd9f2a827d0a33724b5af` |
| `d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.sh` | 6272 | `9bc1ca3e1d81e54aae393b30638f7e412e2530592f92ee26914c5d77dc929988` |
| `driver.g` | 149 | `e94d8e40fab21abb6c419a1d66e4940137502a4ff6dc64a822472d23c72032c4` |
| `run.log` | 4051 | `f603686691bd78a5b6328760fefac80bd07f2c72c13cd9f2a827d0a33724b5af` |

The two logs are byte-identical. They show only Q0/S0/S1/S2 store-build
counters, no `progress batch=` receipt, then
`R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6 status=UNKNOWN`.

The result is canonical JSON. Stored and recomputed self-digest are both
`39749f219b7b5dc34140cbaccc82d28dda41b293cb80e18c2bcdf805f1c5dea3`.
Its exact boundary is:

```text
schema    d972-r07-a0-dual-anchored-rank99-durable-discovery/v6
binding   b679d6b91f3b2cba0b4105b3b5b028c0ec694cb87079833a1617aeff5ad539e3
status    UNKNOWN
terminal  UNKNOWN
reason    correction:scalar_gates
claims    A0=false COMMON=false NONMEMBER=false fake=false Ihara=false
```

There is no checker result/log or owned OK marker. The generated shell admits
only `COMMON_CANDIDATE` or `UNKNOWN_RESOURCE`; this plain `UNKNOWN` therefore
failed closed.

## F2. Checkpoint authentication and prefix delta -- PASS, delta zero

Canonical-body recomputation gives the stored checkpoint seal exactly:

```text
checkpoint schema      d972-r07-a0-dual-anchored-rank99-durable-discovery/v6/checkpoint
checkpoint binding     b679d6b91f3b2cba0b4105b3b5b028c0ec694cb87079833a1617aeff5ad539e3
phase                   READY
prefix_digest           131daa9207c588d8f6914f65c29724c73341bb2f0de62515a6fbc86ceca2cc26
returned state_sha256   2235b4c489b79a013b832947fb1bef7d581648015313975e89dee228b6165e89
input path              search/certs/d972_r07_a0_dual_anchored_rank99_candidate_v1.json
input bytes/SHA-256     173082 / bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358
input state_sha256      f2de40c3b16053464b8cf7d397f8fd05ca4439a46ca7e45df93e60bbc11a312d
```

Both `input_checkpoint` and `c99_identity` name that exact input. Direct JSON
comparison gives:

| durable field | input | returned | decision |
|---|---:|---:|---|
| accepted sources | 56 | 56 | exact list equality |
| `accepted_count` | 56 | 56 | equal |
| `rank` | 99 | 99 | equal |
| batches / `batch_count` | 3 / 3 | 3 / 3 | exact list/count equality |
| `round` | 12 | 12 | equal |
| `open_batch` | false | false | equal |
| current dual profile | present | present | exact equality |
| `appended_batches` / `segments` | absent | `[]` / `[]` | no addition |

Also, `prefix_records` is exactly the 56 input sources, `base_prefix` is their
first eight, `base_batches` is the three input batches, `ready_core_digest` is
null, and the empty-ledger digest is
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.
The returned v6-schema READY re-seal is not byte-identical to the input, but
it carries no durable prefix increment. Exact decision: **zero durable prefix
progress**.

## F3. What `correction:scalar_gates` does and does not identify

The label occurs at the inherited v5 `retain_correction_candidate` gate:

```python
scalar = compiled_formula_scalar(formula, direct)
need(scalar in (1, 2) and pair(dual, row, v4.b) == scalar,
     "correction:scalar_gates")
```

The generated v6 `_v6_selector_block` calls this helper in its K=0 branch.
The v6 K-nonzero `_retain_global` instead labels these conjuncts
`global:zero_scalar` and `global:direct_pair`; v7 only patches the global zero
case. Thus this terminal is uniquely the inherited K=0 support-fibre route.

Before it, `retain_correction_candidate` had obtained a nonzero remainder,
matched replayed and fresh rows, passed exponent and forbidden-E gates, and
matched the direct coordinate tuple/fibre. `formula_bundle` had passed its
separate `formula:identity` canary. `compiled_formula_scalar` returned a typed
member of `{0,1,2}`; an exception in any of its shape/type checks would have a
different reason.

The artifact proves only

```text
not (s in {1,2} and p == s)
s = compiled_formula_scalar(formula,direct)
p = pair(dual,row,v4.b)
```

It cannot distinguish predicate (1) `s in {1,2}` failing (`s=0`) from
predicate (2) `p==s` failing with nonzero `s`; Python short-circuiting means
`pair` is not evaluated when `s=0`. Predicate (3), an earlier ill-typed/model
identity failure, is not the observed terminal. Passing the identity canary
does not establish the custom formula semantics at this selected conjugate.

The exact candidate is unrecoverable from this artifact: result/logs omit
seed, coordinate, target, ordinal, delta, formula, row/dual digests, `s`, and
`p`; the last checkpoint is pre-selector READY with no open row. The smallest
distinguishing probe is to split this one gate into
`need(s in (1,2), "correction:zero_scalar")` and, only after it passes,
`need(pair(dual,row,v4.b)==s, "correction:direct_pair")`. For a self-contained
receipt, also persist the candidate identifiers/digests and the evaluated
`s,p`, then stop claims-false before `phys.add`. This is O(1) after reaching
the candidate. A fresh process would still need state replay because the
provenance was not persisted; I did not run it.

## F4. Containment: exact rank99 material not to copy

Current frozen authorities have the commissioned identities:

```text
task445 producer v3  12215  0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37
checker v7            3653  e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1
theorem v433          10495  3a8b5085e3a0a712dfd32c246cf472ca16616a2e3d7af494e4fcc8b30d02d940
Task524 audit         13304  3b028e05ac74310a2001494e0d112d0ab389bee82b83c5b8ed7cb84a91c39af5
```

Do **not** copy into rank111 lazy K=0:

- rank99 `model179`, `formula_bundle`, `compiled_formula_scalar`;
- `selector_literal`, `literal_row`, `retain_correction_candidate`;
- v6 `_global_literal_word`, `_retain_global`, `_v6_selector_block`;
- v7 source-text rewriting/`exec` monkey-patch machinery;
- the inference that membership in one listed support fibre makes the full K=0
  formula nonzero (other coincident terms may cancel it);
- rank99 C99/rank51 checkpoints, 56 rows, batches, segments, ledgers, selector
  cursors, W/profile data, schemas, bindings, or seals; or
- rank99 batched fresh-anchor/close machinery as state owner.

In particular, task445 `weighted_hit` evaluates the *whole* current formula
and performs `if not scalar: continue` before row insertion. That semantic
guard is exactly what the rank99 support-fibre shortcut did not establish.

The rank111 successor must retain these current task445 authorities:

- model/formula: `m.model179(p179,P)`, `model.occurrence_data(word,raw)`, exact
  44 compact-relator order, current merged mod-3 data, `b.formula_scalar`;
- normalized constant: current `P["dual"]` coefficients `N\x01`, `N\x02`,
  exact `exp_pair`, divisibility by 18, and
  `K=(N1*(ex//18)+N2*(ey//18))%3` from `compile_formulas`;
- support fibre: `m.selective_runtime`, `sf.canonical`,
  `sf.ensure_kernel_prefix(coordinate,9)`, `sf.kernel_candidate`, and the
  printed order embodied by `b.weighted_hit`;
- rows: `aggregate(replay_atom(...))` equals selected-conjugate
  `aggregate(seed_v12(...))`; replay uses `b.direct_row`, while the checker
  independently reconstructs `action_row`/`replay_atom`;
- final admission: nonzero whole-formula scalar and
  `b.pair(current_dual,row)==scalar`;
- update: task445 carry-forward `insert(...,state)`, one `PackedEchelon.add`,
  exactly one post-rise `b.update(P,m)`, durable write, then restart under the
  returned dual; and
- checker-v7 independent replay of prefix, selector provenance, row/pivot,
  pre/post dual and remainder, rank, and update.

V433/Task524 remain positive-only: compile seed-by-seed, skip an unsupported
seed only as a whole, infer no negative claim from no-hit/truncation, and add
only after selected-literal, fresh-row, direct-pair, nonzero-remainder, and
pivot gates agree. The v431 K-nonzero theorem is not a license to call the
rank99 implementation; K nonzero remains typed claims-false
`UNKNOWN_RESOURCE` in the commissioned K0-only lane.

## F5. Exact v220 consequence

No numerator changes. Relative to v220 Delta369:

```text
A0 actual COMMON                0/1 unchanged
single-row stable prefix        68 sources / rank 111 / round 73 unchanged
separate batched stable prefix  56 sources / rank 99 / 3 batches / round 12 unchanged
rank99-v7 continuation          ended UNKNOWN:correction:scalar_gates; +0 durable rows
A4                              1/3 UNKNOWN_RESOURCE, cross-checked through row 26 unchanged
A1 / A2 / A3                   4/4 / 2/3 / 3/3 unchanged
compatible lift/fake/Ihara      no new witness; unchanged
```

The transient nonzero remainder is not promotable: there is no passed scalar
equality, insertion, closed batch, or independent checker receipt.

## Bounded evidence commands

```powershell
$A = Join-Path $env:LOCALAPPDATA 'Temp\shadow-atelier-run33570220633-art9828236283'
Get-ChildItem -LiteralPath $A -File | Sort-Object Name | ForEach-Object {
  [pscustomobject]@{Name=$_.Name; Bytes=$_.Length;
    SHA256=(Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLower()}
}
node -e "const fs=require('fs'),c=require('crypto');const ps=process.argv.slice(1),raws=ps.map(p=>fs.readFileSync(p,'utf8')),[cp,ip,r]=raws.map(JSON.parse);const sha=x=>c.createHash('sha256').update(x).digest('hex'),seal=(o,k)=>{o={...o};delete o[k];return sha(JSON.stringify(o))},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);console.log({canonical:raws.map((x,j)=>x===JSON.stringify([cp,ip,r][j])+'\n'),file_sha:ps.map(p=>sha(fs.readFileSync(p))),state:[cp.state_sha256,seal(cp,'state_sha256'),ip.state_sha256,seal(ip,'state_sha256')],result:[r.self_digest_sha256,seal(r,'self_digest_sha256')],sources:eq(cp.accepted_sources,ip.accepted_sources),prefix:eq(cp.prefix_records,ip.accepted_sources),batches:eq(cp.batches,ip.batches),profile:eq(cp.current_dual_profile,ip.current_dual_profile),counters:[cp.accepted_count,ip.accepted_count,cp.rank,ip.rank,cp.batch_count,ip.batch_count,cp.round,ip.round],appended:[cp.appended_batches,cp.segments]})" `
  "$A\d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.checkpoint" `
  'search/certs/d972_r07_a0_dual_anchored_rank99_candidate_v1.json' `
  "$A\d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.json"
$auditHead = '4d57c024df74b257e5b4e724b69e6c4d51ff667f'
$auditV7Files = @('search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.py',
  'crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.py',
  'search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v7.g')
git show -s --format='%H %s' $auditHead
git ls-tree $auditHead -- $auditV7Files
$auditV7Files | ForEach-Object { git hash-object -- $_ }
rg -n --fixed-strings 'correction:scalar_gates' search crosscheck sol
```

I read the complete frozen rank99 v5/v6/v7 producer/checker/driver chain and
the complete task445/v433/Task524 authorities. I ran no production, large
replay, GAP, GHA, network operation, adoption, release, or git mutation, and
changed no file other than this commissioned reply.

`AUDITED_ZERO_PROGRESS_WITH_CONTAINED_REGRESSION`
