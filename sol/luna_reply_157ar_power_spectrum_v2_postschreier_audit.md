# Luna post-Schreier audit: power-spectrum v2 (157ar)

## Verdict

The post-Schreier repair closes the prior compact-subgroup gap.  The
independent certificate is mathematically sufficient, and all bounded static,
finite-factor, and mutation checks passed.  No local GAP, git, push, or GHA
was run.

## 1. Schreier indexing and orientation

`enumerate_factor` starts with the identity only as vertex zero, but stores a
separate word list.  Each newly reached vertex receives
`words[i] + [1,2,-1,-2][k]` while the actual edge is computed from the actual
factor generators (`search/check_d972_power_spectrum_v2.py:162-186`).  The
Schreier verifier evaluates relators at the actual `(x9,y9)` and `(x4,y4)`:

```text
relator = words9[i] + [letter] + [-w for w in reversed(words9[j])]
eval_word(relator, (x9, y9))
eval_word(relator, (x4, y4))
```

This is at `:225-234`; it does not use `elements[0:2]`.  The reverse-negative
word is the correct inverse under the checker convention
`pprod(a,b)=b o a` and `eval_word`'s left-to-right accumulation: if the edge
is `s_i * letter = s_j`, then
`s_i * letter * s_j^(-1)` has trivial G9 projection.

## 2. Direct-product certificate

The certificate is a valid Schreier proof.  The 2,916 BFS section words give a
transversal for the epimorphism `F(x,y) -> G9`; all four directed generator
edges per section vertex produce 11,664 standard Schreier generators for its
kernel.  The checker independently verifies every G9 projection is identity
and evaluates the corresponding PSL words.  Their generated subgroup has
order 504 (`:227-239`).

The projection of
`C=< (x9,x4),(y9,y4) >` onto G9 is onto because the section enumeration has
2,916 elements (`:198-200`).  Each Schreier relator lies in C and in the G9
kernel, and the PSL projections generate all PSL, hence
`{1} x PSL <= C`.  For any `(g,p)` in `G9 x PSL`, choose `(g,q)` in C from
the surjective G9 projection and multiply by `(1,q^-1 p)`; therefore
`C=G9 x PSL`.  This proves that factor-wise membership implies membership in
the actual compact roof, rather than merely in an ambient direct product.

The verifier binds the independently recomputed certificate to the exact
receipt metadata (`search/check_d972_power_spectrum_v2.py:253-269`), requiring
section factor G9, orders 2,916 and 504, 11,664 edges, and kernel order 504.
The producer emits the same exact record
(`search/d972_power_spectrum_v2.g:191-193`).

## 3. All target actions and associativity

For each of the 972 rows, the checker computes both factor target images and
requires membership in the independently enumerated factor (`:270-281`).  It
then propagates the image from the identity over every directed Cayley edge,
rejecting any relation inconsistency and any image outside the factor
(`:282-299`).  The direct-product certificate above upgrades these two
factor endomorphisms to a well-defined endomorphism of the actual compact
roof; no producer table or GAP `GroupHomomorphismByImages` result is trusted.

The checker independently reconstructs every one of the 972^2 products from
the frozen words and compares the complete computed table to the receipt
(`search/check_d972_power_spectrum_v2.py:482-496`).  It then independently
checks identity, unique two-sided inverses, exact orders, square/cube maps, and
the folded exponent (`:508-541`).  Finally, for all 945,441 pairs it checks
the lambda action and both compact generator images of
`h_(i*j)=h_j o h_i` (`:382-410,543-546`).  Since each action is independently
known to be an endomorphism, equality on the two compact generators is a
valid associativity proof, not a nearby generator-only law.

## 4. Receipt, runtime, and source gates

The checker requires exact schema/status/972-row count, semantic roof and
artifact digests, exact runtime manifest hashes, fail-closed outside metadata,
sorted frozen keys, every row index, lossless word/key replay, duplicate
rejection, factor certificate, full table, digests, powers, and associativity
(`search/check_d972_power_spectrum_v2.py:356-481,482-551`).  A missing row,
duplicate row, altered word/key, product cell, or certificate field cannot
pass these gates.

The core remains definition-only with four fixed helper Reads and no dynamic
task Read, environment dispatch, or `QUIT`
(`search/d972_dovetail_core_v2.g:1-12`).  The producer reads that core and
regains control at its own dispatch (`search/d972_power_spectrum_v2.g:8,210`).
The workflow covers and hashes the complete five-file transitive runtime plus
the artifact, has `workflow_dispatch`, runs producer selftest before full, and
uses immutable action SHAs (`.github/workflows/d972-power-spectrum-v2.yml:3-19,39-57,67-95`).
The GAP runner/package remain the explicitly disclosed Ubuntu apt contract:
`ubuntu-24.04`, `gap=4.12.1-2build2`, and runtime `4.12.1`; no stronger image
immutability is claimed.

## 5. Bounded hostile mutations

All mutations were in-memory or helper-level; no repository file was changed.
Each was rejected as follows:

```text
PY_FACTOR_SCHREIER_PASS {'section_order': 2916, 'other_order': 504,
  'schreier_edge_count': 11664, 'kernel_generated_order': 504}
WRONG_ACTUAL_GENERATOR_REJECTED
ONE_SCHREIER_EDGE_REJECTED
WRONG_KERNEL_ORDER_REJECTED
ONE_TARGET_ACTION_REJECTED
ONE_PRODUCT_CELL_REJECTED
PRODUCT_MUTATION_PASS
```

The wrong-generator and one-edge mutations failed the G9 Schreier projection
gate; the kernel-order mutation failed the serialized certificate equality;
the target-action mutation (a within-factor transposition) failed factor image
membership; and the product-cell mutation failed the exact `table ==
computed` gate.

## 6. Static checks and hashes

```text
D972_POWER_SPECTRUM_V2_CHECKER_SELFTEST_PASS
PY_AST_PASS
YAML_WORKFLOW_DISPATCH_PASS
PY_FACTOR_SCHREIER_PASS
```

Current SHA-256 values are:

```text
1c3348003805df874ab6d42503720259564eec25c1aebfb1c548a759e3d9f7ae  search/d972_dovetail_core_v2.g
1855cf69b78cda06f5a829f4a4d500f4f8e89431e88110271e2567d78e6ba651  search/d972_power_spectrum_v2.g
c5a837d5c194ecb42163d8944c59aaa919705bd488129068aa5324830ae00213  search/check_d972_power_spectrum_v2.py
2fee55211194660452d33b1e87b8ef02d1a0e95fb6070c357b7083201717675a  .github/workflows/d972-power-spectrum-v2.yml
2e4da671ad9d018be1bc6f2f387f0e1d597e87c2c0e807eef40aeef3b92deece  search/probe/wac_v1/gap_output_prelude.g
f80eeeae71c4e39f8b3d62d997d18635f5ea8fb339a6d0578e834300ea4d4911  search/gaplib_common.g
aadf1afa5e1a171d10d0aa1f9657e823cad669b960e08da7b9e7618f2ea4f998  search/week3-battery-common.g
e48e50d55562983415b5691d07e3d893182620b1f73b8fe35ea77815ad9695c4  search/week3-psl-common.g
564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9  search/certs/d972_b4_word_key_artifact_v1_20260816.json
```

PASS_POWER_SPECTRUM_V2_POSTSCHREIER
