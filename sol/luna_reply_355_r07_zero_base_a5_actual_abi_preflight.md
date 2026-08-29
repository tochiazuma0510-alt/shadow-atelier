# Luna reply 355 — zero-base A5 actual ABI preflight

## 0. 判定

これは v345 に限定した機械的 ABI 棚卸しである。コード、GAP、Python、GHA は実行していない。

```
IMPLEMENTATION:                  BLOCKED
SELFTEST / PRODUCTION:           UNEXECUTED
FIVE FROZEN CASES:               BLOCKED
ACTUAL A5 / ACTUAL A6:           0/3 / 0/3
LIFT / FAKE / IHARA:             NONE
```

理由は、現在の A4/A0 の実行がまだ accepted positive receipt/verdict を出しておらず、A0 に結び付いた task193 の actual owner もまだ無いためである。従って以下は「最小 ABI の固定」であり、実行済み A5 証人の主張ではない。

## 1. 既存 owner と正本フィールド

### A3 zero receipt/verdict

A3 の run-level owner は現在の GHA run `33244921126` である（この run の receipt/verdict は `ci/in` にまだ staging されていない）。既存の cross-checked terminal は

```
R07_PRE_A0_A3_PROJECTED_MEMBER
```

で、self digest は
`a3f452074bf1e722591949372ae2b16c4d9fed0a2a5cba26a7eba58c7b30b43e`、verdict digest は
`71f239868b46989b12289baa9acae73ecd19701b6b0a7dd33107527f33aa4b7e`。

この actual zero branch で既に出ているのは、replay target、lambda、kappa がいずれも canonical empty sparse vector であること、および A3 receipt/verdict の cross-check である。A5 はこれを次のように使うだけでよい。

```
target = [] ; lambda = [] ; kappa0 = [] ; r0 = e1
```

これは v345 の zero-base 前提であり、A3 の古い local base-pair roster を入力にしてはならない。

### A4 producer/checker

実 owner は次の wrapper と frozen body である。

```
producer: search/d972_r07_word_independent_successor_kernel_v11.py
checker:  crosscheck/check_d972_r07_word_independent_successor_kernel_v11.py
producer wrapper: 2038 bytes,
  sha256=f3cccb104402ee031baba59487a8e4f71dbe8fb244ff220db96f8814950f868e
checker wrapper: 2376 bytes,
  sha256=552e7d866574fe6d92bf3586c63ff2640057d19b77b6e982078c52b9ae896026
frozen producer: d972_r07_word_independent_successor_kernel_v6.py
  sha256=aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a
frozen checker: crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py
  sha256=432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf
schema: d972-r07-word-independent-successor-kernel/v6
positive terminal: R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS
```

wrapper v11 の bridge partition は `((0,1,2),(3,4,5),(6),(7),(8),(9),(10))` に固定されている。

A4 positive result の top-level 必須 terminal fields は次である。

```
schema, status="COMPLETE", terminal=R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS,
complete=true,
A4_presentation_input=1, A4_invariant_closure=1, A4_word_bearing_K=1,
authority, primitive_inventory, forward_dag, kernel,
performance, resource, driver_contract, forbidden_downstream
```

`kernel` 内で zero-base A5 が実際に必要とする最小部分は、完走標識と ordered word-bearing K roster である。

```
kernel.complete=true
kernel.K_roster=[{
  label, rank, pivot, row, word,
  discrepancy, candidate_E, Q, c,
  rho0, rho1, rho1_flattened, rho1_actual_flattened, q,
  raw_coefficients, normalization_scale,
  ancestry, word_formula, E_formula, replay, strict_rank_rise
}]
```

ここで `K_roster` は `public_k_roster(oracle.basis.k_items)` の public record であり、process-local の `word_node`/`candidate_node` は含めない。A5 checker は literal word と rho/replay 情報を独立に再生する必要がある。

現在の A4 run `33245807123` は active で、accepted A4 receipt/verdict はまだ無い。従って上記の K roster は ABI として確定しているが、actual emitted artifact としては未取得である。

### task198 presentation/occurrence owner

既に accepted で local に存在する owner は

```
ci/in/d972_r07_seven_context_roof_presentation_v1.json
```

```
schema: d972-r07-seven-context-roof-presentation/v1
status: COMPLETE
terminal: ROOF_BRIDGE_ISOMORPHISM
self_digest_sha256:
  c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f
```

同じ accepted package の acceptance/attestation/verdict files は同じ `ci/in/` にある。

task198 の A5 側に再利用できる実フィールドは次である。

```
Delta0.presentation.rows = 6441
Delta0.presentation.layer_counts =
  {Gamma_Cayley: 6318, action: 104, Q0_lift: 19}
bridge.occurrence_ledger
bridge.occurrence_ledger_sha256
bridge.typed_coordinate_ledger_sha256
bridge.seven_blocks
bridge.ten_to_eleven
bridge.marked_replay
bridge.relator_replay
evaluator.context_maps
evaluator.joint_coordinate_image
evaluator.coordinate_ledger_sha256
evaluator.relator_rows_sha256
evaluator.registry_callable
evaluator.runtime_constructor
```

occurrence ledger item の実 schema は

```
block, block_index, block_slot, context_id, factor_sign,
fox_prefix_occurrences, occurrence, ordinal, orientation, role,
ten_index, type
```

である。A5 はこれを使って literal A0 correction word の eleven-occurrence vector を構成する。固定 toy tag `o0,...,o10` を使ってはならない。

### A0 producer/checker

現行 owner は次である。

```
producer: search/d972_r07_history_free_positive_fast_resume_v15.py
checker:  crosscheck/check_d972_r07_history_free_positive_fast_resume_v15.py
frozen producer body: d972_r07_history_free_positive_fast_resume_v13.py
  sha256=4d1be83fefbb1a1c0b23010825c0013b80650439b714dce7e35a6e0f53a2ff2a
frozen checker body: crosscheck/check_d972_r07_history_free_positive_fast_resume_v13.py
  sha256=42e8f6df8d85169bf4039bc4195a0e47c284ad475a177414308ba28f99377b64
v15 producer wrapper sha256=6412ea39f1b0559738c44fff0a9aa5f6c8366c55193b74f5c6df1ded977dc2a9
v15 checker wrapper sha256=5edc81c1436694e8495a444ce8ebb3efebd80fa9dcf62717f73874d5e55a5a3c
schema: d972-r07-history-free-positive-fast-resume/v10
positive terminal: R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_COMMON_WORD
```

Positive A0 `common_candidate` が実際に出す fields は次である。

```
schema, status="COMMON_WORD", terminal=R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_COMMON_WORD,
source, source_snapshots, light_input_sha256, heavy_input_sha256,
triangular_certificate, basis_authority, target, formal_solution,
selected_old, selected_new, selected_corrections, boundary_preimage,
correction_word, corrected_word, g760,
producer_sparse_equality, producer_joint_kernel, producer_all_seven_replay,
boundary_owner, monitor, selftest, claims, claim_boundary
```

`correction_word` が A5 の literal `c`、`corrected_word` が `red(g760 c)` である。A0 自体は `e1` を emit しない。現在の A0 run `33246619673` は active で、positive common receipt/verdict はまだ無い（従って `c` も未取得）。UNKNOWN receipt は terminal が typed `UNKNOWN_INPUT:...` または `UNKNOWN_RESOURCE:phase=...` で、A5 の literal correction input には昇格できない。

### task193 owner

現存する compiler は

```
search/d972_r07_second_frattini_affine_prefix_compiler_v1.py
```

```
schema: d972-r07-second-frattini-affine-prefix-compiler/v1
terminal: R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1
```

ただし現 v1 は authenticated task186 receipt/attestation を入力する旧 owner であり、現行 A0 v15 の `correction_word` に結び付いた actual receipt/verdict は `ci/in` に無い。したがってこれは「ABI の候補」であって actual A5 input ではない。

task193 positive output の利用可能な field は次である。

```
beta1.beta1_H1, beta1.beta1_H2, beta1.beta1_P
```

各 defect item は

```
block, word, prefix_transitions, affine_identity, fox_row, d1
```

を持つ。v345 の符号規約に従い、A5 owner は literal A0 `c` を task193 側で再生し、`e1(c) = -beta1^193(c)` を保つ必要がある。単一 digest の信頼や 3 つの beta blob の結合だけでは eleven-occurrence A5 vector にならない。必要なのは occurrence ledger への再挿入を含む full replay である。

## 2. 最小 zero-base A5 producer/checker input manifest

以下は設計上の manifest であり、ファイルとして作成・staging はしていない。v345 に従い、anchor/adapted-basis/A3-base-pair は含めない。

```
{
  "a3_zero": {
    "receipt_owner": "GHA run 33244921126",
    "verdict_owner": "GHA run 33244921126",
    "terminal": "R07_PRE_A0_A3_PROJECTED_MEMBER",
    "cross_checked": true,
    "target": [], "lambda": [], "kappa0": []
  },
  "task198": {
    "receipt": "ci/in/d972_r07_seven_context_roof_presentation_v1.json",
    "schema": "d972-r07-seven-context-roof-presentation/v1",
    "terminal": "ROOF_BRIDGE_ISOMORPHISM",
    "occurrence_ledger": "/bridge/occurrence_ledger",
    "seven_blocks": "/bridge/seven_blocks",
    "ten_to_eleven": "/bridge/ten_to_eleven",
    "evaluator": "/evaluator"
  },
  "a4": {
    "producer": "search/d972_r07_word_independent_successor_kernel_v11.py",
    "checker": "crosscheck/check_d972_r07_word_independent_successor_kernel_v11.py",
    "schema": "d972-r07-word-independent-successor-kernel/v6",
    "terminal": "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS",
    "required": ["complete", "/kernel/K_roster"],
    "accepted_word_bearing_basis": true
  },
  "a0": {
    "producer": "search/d972_r07_history_free_positive_fast_resume_v15.py",
    "checker": "crosscheck/check_d972_r07_history_free_positive_fast_resume_v15.py",
    "schema": "d972-r07-history-free-positive-fast-resume/v10",
    "terminal": "R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_COMMON_WORD",
    "literal_c": "/correction_word",
    "corrected_word": "/corrected_word",
    "g760": "/g760",
    "source_snapshots": "/source_snapshots"
  },
  "task193_actual": {
    "required": "A0-v15-bound successor receipt and independent verdict",
    "literal_binding": "same c as /a0/literal_c",
    "accepted_terminal": "R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1",
    "replay_source": ["beta1_H1", "beta1_H2", "beta1_P", "prefix_transitions", "fox_row"],
    "derived_field": "e1(c) = -beta1^193(c), reconstructed on task198 occurrence ledger"
  }
}
```

For the producer/checker pair, `a4` and `a0` must each be independently replayed and pinned. The A5 checker must not accept a producer-only K roster or a producer-only beta digest.

Once these five owner inputs exist, the zero-base A5 data flow is only:

```
accepted A4 K words
  -> (k_i-1)d1 and (k_i-1) odot w seeds
  -> marked x±/y± closure
  -> block map C / post-C nullspace
  -> H d1

A0 literal c + task193 replay
  -> beta1^193(c)
  -> e1(c) = -beta1^193(c)
  -> membership e1(c) in H d1
```

The A5 checker must also preserve the v345 zero-base rule `kappa0=0`, hence `r0=e1`; no separate A3 correction term is an input.

## 3. Fields already emitted vs. fields deferred

### Already emitted / available now

* task198 complete physical receipt, bridge/occurrence ledger, seven-block and ten-to-eleven maps, evaluator ABI, and their digest/attestation material.
* A3 zero receipt/verdict and its cross-checked empty target/lambda/kappa result (GHA owner only; not staged in `ci/in`).
* A4 v11 producer/checker wrappers, frozen-byte pins, schema, terminal contract, and the shape of `kernel.K_roster` (the current active run has not emitted an accepted roster).
* A0 v15 producer/checker wrappers, frozen-byte pins, schema, terminal contract, and the positive `common_candidate` field schema (the current active run has not emitted a positive `correction_word`).
* task193 v1's beta field schema and sign convention, but not an A0-v15-bound actual receipt.

### Available only after current A4/A0/task193 successors finish

* A4 accepted positive receipt/verdict and its literal, independently replayable `/kernel/K_roster`.
* A0 accepted positive receipt/verdict and literal `/correction_word` `c`, `/corrected_word`, and `/g760` binding.
* A task193 successor receipt/verdict that consumes that same literal `c` and exposes a replayable eleven-occurrence `e1` (or the beta records plus enough owners to reconstruct it).
* A5's actual closure-derived `H d1`, `e1` membership result, and checker terminal.
* A6's closure-derived factored records `(coefficient, prefix_DAG_node, original_A4_kernel_word_index)`.

No current UNKNOWN A4/A0 terminal supplies these positive fields.

## 4. Explicitly obsolete requirements

The zero-base A5 manifest and checker must reject or ignore all of the following:

```
projection_anchor / anchor / anchor_diagnostics
projections / adapted basis / change_matrix / inverse_change_matrix
nonzero projected generator z0
kappa0_ancestry / kappa0_times_d1
local A3 base-pair roster / base_pairs
hardcoded o0,...,o10 occurrence tags
hardcoded toy width-11 or width-13 vectors
```

In particular, A4's legacy `anchor_diagnostics` may still be present as a producer diagnostic, but it is not an A5 zero-base input. Requiring it would reintroduce the v345-obsolete nonzero anchor branch.

## 5. Reuse candidates and blockers

### Safe reuse candidates

* A4's `public_k_roster` record shape, literal `word`, `rho0/rho1`, rank/pivot metadata, and replay/ancestry fields; consume through an independent checker, not by importing producer code.
* task198's `occurrence_ledger`, `seven_blocks`, `ten_to_eleven`, evaluator coordinate ledger, and runtime constructor.
* A0's literal `correction_word`, `corrected_word`, `g760`, and source snapshot identity.
* task193's `beta1_H1/H2/P`, `prefix_transitions`, `fox_row`, `relation_words`, and direct replay fields, after replacing task186 binding with the literal A0 v15 binding.
* The existing fused compiler's abstract sparse-linear-algebra/data-flow shapes (`Basis.reduce/add/contains`, closure queue, `c_apply`, left-kernel/span/solve patterns) only as implementation patterns. Its toy values and owner fields are not evidence.

### Current blockers

1. A4 run `33245807123` is active; no accepted positive A4 artifact means no actual word-bearing K roster.
2. A0 run `33246619673` is active; no accepted positive A0 artifact means no literal `c`.
3. The available task193 v1 is task186-bound and has no staged actual receipt/verdict bound to the current A0 `c`; therefore no actual replayable `e1` exists.
4. With any one of these absent, an A5 producer/checker can only be a selftest or schema preflight; it cannot emit an actual zero-base witness. A6 and all downstream lift/fake/Ihara labels therefore remain unentered.

