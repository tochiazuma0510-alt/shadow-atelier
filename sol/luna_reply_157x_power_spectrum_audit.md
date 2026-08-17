# Luna audit: task 157x power spectrum

## Verdict: BLOCKER

The exact 972-row lane is mathematically coherent and the independent checker
replays the authenticated words and all 972^2 products.  It is not yet safe to
preflight because the workflow does not trigger on all source files read by the
worker, and the receipt does not bind those omitted sources.

## F1 — BLOCKER: incomplete source-trigger/provenance closure

`.github/workflows/d972-power-spectrum-v1.yml:7-14` lists the producer, checker,
worker, two worker helpers, and the word-key artifact, but omits:

* `search/probe/wac_v1/gap_output_prelude.g`
* `search/gaplib_common.g`

Those are direct runtime reads at `search/d972_dovetail_worker_v1.g:18-21`.
Therefore a push changing either file can leave this job untriggered while
changing the D972 model or its GAP semantics.  The receipt binds only the word
artifact hashes (`search/d972_power_spectrum_v1.g:183-190`), and the Python
checker checks those same two artifact hashes (`search/check_d972_power_spectrum_v1.py:188-200,252-258`),
not the omitted worker dependencies.  Add both paths to `on.push.paths` and
bind/check their hashes (or an equivalent complete source manifest) before
claiming a reproducible candidate.

## F2 — HIGH: runtime/action pins are not reproducible pins

The workflow uses mutable major tags `actions/checkout@v4` and
`actions/upload-artifact@v4` (`.github/workflows/d972-power-spectrum-v1.yml:24-27,70-78`).
It also installs the distribution GAP package without a version pin and accepts
four different GAP versions (`:29-35`).  This is weaker than the exact-source
claim required by the task: a future runner/package update can change execution
without changing the audited repository files.  Pin action SHAs and the GAP
runtime/image, or record and enforce one immutable runtime plus its digest.

## F3 — HIGH for downstream power-game readiness: 2/3 maps and exponent are
not serialized or checked

The producer computes and serializes the complete table, exact orders,
two-sided inverses, and the order histogram (`search/d972_power_spectrum_v1.g:113-151,161-200`).
The checker independently recomputes the table, identity, inverses, exact
orders, and histogram (`search/check_d972_power_spectrum_v1.py:299-341`).
That is enough to derive square and cube maps and the exponent from the table,
but neither receipt contains explicit `square_map`, `cube_map`, or `exponent`,
and the checker does not derive/check those fields.  This is not a defect in
the serialized multiplication table, but it is an unchecked gap against the
task's stated 2/3-power-game contract.  Either emit and independently verify
these arrays/scalars, or explicitly make their checker-side derivation part of
the contract before using this receipt as the downstream game input.

## F4 — MEDIUM: associativity is asserted, not independently replayed

The producer explains associativity from function composition and checks every
pair for closure (`search/d972_power_spectrum_v1.g:122-133,153-159`), then emits
`associativity_gate=true` (`:194`).  The Python checker computes every table
entry and verifies identity/inverses/orders, but does not validate the
associativity metadata or run a triple/table associativity check
(`search/check_d972_power_spectrum_v1.py:304-344`).  The mathematical
composition argument is reasonable for this construction, so this is not an
independent orientation failure; it remains an unchecked acceptance field.

## PASS findings (conditional on closing F1/F2)

* The worker constructs the marked D972 model and gates the compact pure roof
  order at 1,469,664 (`search/d972_dovetail_worker_v1.g:257-345`).  Its
  calibration scans the literal equations, maps compact to full marked pure
  model bijectively, and requires exactly 972 distinct frozen target keys
  (`:430-510`).  No guessed multiplication or complement/cardinality claim was
  found.
* GAP/paper orientation is explicitly canaried in the producer
  (`search/d972_power_spectrum_v1.g:64-78,153-159`) and independently mirrored
  by Python's reverse `paper_prod` convention and self-test
  (`search/check_d972_power_spectrum_v1.py:236-243,354-360`).  The GF(8)
  degree-9 block and degree-36 compact roof reconstruction are independent of
  the GAP producer/helper imports.
* The checker is standalone (standard-library imports only), verifies the
  artifact and frozen row/tuple digests, replays every signed word, binds every
  lossless 36-point permutation, and recomputes all 945,441 products before
  comparing the serialized table (`search/check_d972_power_spectrum_v1.py:188-200,265-316`).
* The outside lane is fail-closed: the producer writes UNKNOWN with null
  outside data and forbids inference (`search/d972_power_spectrum_v1.g:179-203`),
  while the checker rejects any authenticated outside label not consumed by
  this version (`search/check_d972_power_spectrum_v1.py:211-233,259-263`).
* The workflow runs producer selftests before the full run, preserves pipeline
  status, requires the exact final marker, runs the independent checker, and
  uploads attempt-unique evidence (`.github/workflows/d972-power-spectrum-v1.yml:37-78`).

## Allowed static checks

Ran without GAP, full computation, git, or GHA:

```text
python -B -m py_compile search/check_d972_power_spectrum_v1.py
python -B search/check_d972_power_spectrum_v1.py --self-test
python -B -c "ast.parse(...)"
python -B -c "yaml.safe_load(...)"
```

Results: `D972_POWER_SPECTRUM_CHECKER_SELFTEST_PASS`, `PY_AST_PASS`, and
`YAML_PARSE_PASS`.  The frozen artifact was statically checked at 972 rows.

## Audited hashes (SHA-256)

* `search/d972_power_spectrum_v1.g` —
  `f9a3a7fdb6224dbde68c914a245b2eda8e9c057bd1aee3dac2e93d8f5ccabbc`
* `search/check_d972_power_spectrum_v1.py` —
  `a17020b3f24e57483e0d647ad487fee35e73d712bfc581c2cea3604fe2525c8d`
* `.github/workflows/d972-power-spectrum-v1.yml` —
  `1764ea9ac930217b724cc1f214714a5379ae5e92fb30c948e7b24e2f22c2c472`
* `sol/luna_reply_157r_d972_power_spectrum.md` —
  `48c5b48736cbc403a24a1284ff8d8af4bab833b4846889e9c92b72fe5071c1bc`
* `search/d972_dovetail_worker_v1.g` —
  `f9ad3f8f71dc5af3d20dbef66dc6a25c79a50393be55767c0fb9f077d46994e8`
* `search/gaplib_common.g` —
  `f80eeeae71c4e39f8b3d62d997d18635f5ea8fb339a6d0578e834300ea4d4911`
* `search/probe/wac_v1/gap_output_prelude.g` —
  `2e4da671ad9d018be1bc6f2f387f0e1d597e87c2c0e807eef40aeef3b92deece`
* frozen word-key artifact —
  `564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9`
