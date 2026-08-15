# Luna reply 152 — B4 low-index GHA handoff

Status: `READY_FOR_GAP_RUN`; no local GAP run, workflow edit, commit, push, or dispatch was performed.

## Versioned producer

Added [search/d972_b4_lowindex_v1.g](C:\Users\81905\Desktop\shadow-atelier\search\d972_b4_lowindex_v1.g). It is self-contained for Linux GAP-run execution: all reads are repository-relative and no `%TEMP%`/Windows path or worker-definition import is used.

Frozen gates retained:

- `U_REL=158` and rho preserves K05 relators; exact rho⁵ construction gate.
- Exact compact roof count `972`.
- Product order `rho^4, rho^3, rho^2, rho^1, rho^0`.
- Low-index bound `LowIndexSubgroupsFpGroup(Ufp,7)`, including indices 5, 6, and 7.
- All 158 relator images and q∘rho⁵=q checked for every quotient.

Each quotient emits only a bounded aggregate line. On the first defect, the receipt writes `h_images`, `rho_words`, all 158 `all_relators`, exact `target_keys`/`roof_words`, defect row/index, and the word/key binding digest. An all-pass run writes quotient aggregates and status `UNKNOWN_ALLPASS_CONTINUE`; it never claims B.

The GAP-global output override is:

```gap
D972_B4_LOWINDEX_OUTPUT := "ci/out/d972_b4_lowindex_v1.json";;
```

The producer defaults to that path if the override is absent.

## Exact gap-run dispatch inputs (not dispatched)

```text
workflow: gap-run.yml
script: search/d972_b4_lowindex_v1.g
preamble: D972_B4_LOWINDEX_OUTPUT := "ci/out/d972_b4_lowindex_v1.json";;
out_dir: ci/out
timeout_min: 120
```

The unchanged generic workflow creates `ci/out`, prepends the preamble, reads the producer, and uploads `ci/out/run.log` plus the configured output directory.

## Python checker contract audit

`search/check_d972_b4_finite_image_v2.py` requires the defect receipt schema `d972-b4-finite-image/v2`, six permutation images, six rho words, exactly 158 relators, rho⁵ closure, 972 roof words, frozen target-key digest
`9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62`, and frozen relator digest
`12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e`. The producer emits those fields on a defect.

Adversarial blocker: the checker’s `FROZEN_WORD_KEY_ARTIFACT_DIGEST` is currently empty, so it deliberately rejects every terminal receipt until the independently generated word/key artifact is pinned. The producer therefore reports its computed binding digest but does not bypass this checker gate. All-pass low-index output is not sent down the checker’s terminal defect path.

## Tests performed

```text
python -B -m py_compile search/check_d972_b4_finite_image_v2.py
PASS

python -B search/check_d972_b4_finite_image_v2.py --help
PASS (selftest runs before argparse; usage printed)

Static producer audit:
PASS — no C:/Users, TEMP, luna_ paths, or workflow edits
PASS — max index 7, U_REL=158, exact 972, rho^4..rho^0, ci/out override present
```

No mathematical verdict is asserted by this handoff. A max-7 all-pass remains UNKNOWN; only a checker-accepted sound defect can establish B4-A.
