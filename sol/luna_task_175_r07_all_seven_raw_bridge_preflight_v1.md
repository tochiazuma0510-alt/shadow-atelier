# Luna task 175 — R07 all-seven raw bridge preflight v1

Date: 2026-08-27
Role: Luna implementation/cross-check only.  The mathematical rulings are
fixed by Sol v121--v123.

## 0. Scope and authorized files

Implement the bounded all-seven input preflight specified in task 173.  Do not
run an orbit image, column generation, affine solve, correction search, or
cofinal argument.

Authorized new files only:

```text
search/d972_r07_all_seven_raw_bridge_preflight_v1.py
crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py
search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g
search/certs/d972_r07_all_seven_raw_bridge_preflight_v1_20260827.json
sol/luna_reply_175_r07_all_seven_raw_bridge_preflight_v1.md
```

Do not edit any existing file.  Do not run Python, GAP, Node, git, or GHA
locally in this task.  Static reading, source writing, Python AST parsing by a
non-Python parser if already available, ASCII scans, and hashes are allowed.
The parent broker will audit, commit, push, and execute the bundle on GHA.

## 1. Frozen rulings and pins

Read all of the following before implementation:

```text
189a642fc8654f163b0b7964b75043ea393cac31a0b56b84ae0fddf2f73c3695
  sol/luna_reply_173_r07_all_seven_raw_bridge_inventory_v1.md
efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5
  sol/proof_pb3_two_relator_presentation_equality_v121.md
daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348
  sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md
272aabc882599031c4da0472f8f2340043b32571e8e05ecaa58fc5ad1c6a31ac
  sol/audit_r07_all_seven_bridge_checkpoint_v123.md
4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f
  sol/proof_pb4_eleven_relator_presentation_equality_v108.md
```

Use the current task-172 v7 shelf, not v2:

```text
92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed
  search/d972_r07_full_e4_joint_orbit_preflight_v7.py
e3917ec05b95b8996e3a5cec1cc2bfde51c3ed8c6972175fd9be9e1178205c23
  crosscheck/check_d972_r07_full_e4_orbit_preflight_v7.py
86c6f3a72a3f852a1be7c5323bf72c7ad987377fd5483b6e32528fe263e290ff
  search/certs/d972_r07_full_e4_orbit_preflight_v7_20260827.json
```

The q=3 and task-157ee input receipts must retain their existing exact hashes
and run provenance.  Fail closed on every pin mismatch.

## 2. Exact target

Use one and the same corrected word

\[
f_1=\operatorname{reduce}(g_{760}\,c)
\]

in both source-E3 hexagons and all five E4 pentagon occurrences.  For this
preflight, `c` is not a solved correction: choose a deterministic, nonempty,
word-bearing relation from the complete 6,441-row registered normal roster,
record its layer, ordinal, conjugator/record provenance, reduced signed word,
length, and SHA-256, and prove by direct joint evaluation that it is identity.
This row is solely a typed formula/canary witness.  Never call it the final
correction.

The target blocks are disjoint and ordered:

```text
1 = H1 / E3 / 3 C1 components
2 = H2 / E3 / 3 C1 components
3 = P  / E4 / 6 C1 components
```

Keys are `(block_tag, component, exact element blob)`.  No cross-block
cancellation is allowed.

## 3. Quotient and source-context retraction gate

Freshly reconstruct typed E3 and E4 arithmetic from the authenticated q=3
receipt.  Then implement v122 rather than merely pinning its prose:

1. reconstruct the coarse fourth deletion by projecting the fourth P block
   and fourth G9 block of Q4 to Q0;
2. reconstruct the fine deletion on marked PB4 images
   `(1,2,identity,3,identity,identity)`;
3. reconstruct endpoint insertion at PB4 marked indices `(1,2,4)`;
4. validate both fine maps against the serialized pc collectors and check
   deletion after insertion on every PB3 pc generator and all three marked
   generators;
5. construct the product map `d_E:E4->E3` and check `d_E o i_E=id_E3` on all
   three marks;
6. bind E4 registry IDs 21--25 to source-E3 pairs
   `(x,y),(x,z),(y,z),(u,x),(u,y)` and directly require that deletion of every
   left/right blob is the corresponding E3 blob.

Use `z=(y*x)^-1`, `u=(x*y)^-1` in the frozen paper-product convention.  Do not
use strand-permutation symmetry and do not trust names without blob equality.
Return `UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE` on any failure.

## 4. Literal all-seven reconstruction

Reconstruct independently of task-172's public booleans:

1. `g760`, its length 760, exponent sums `[0,0]`, and signed-word digest;
2. the 26 nonempty correction records and all 6,441 expanded roster words in
   layers `6318 + 104 + 19`;
3. the five unique source-E3 pairs, five E4 pentagon pairs, and all eleven
   occurrence aliases;
4. the literal H1 and H2 words for `g760`, `c`, and `f1`;
5. all five pentagon factors and the ordered product
   `b1*b2*b3*b5^-1*b4^-1` for all three words;
6. the three raw base Fox targets, three direct changes
   `R(f1) R(g760)^-1`, and the three literal prefix-transport formulas;
7. one canonical stacked sparse target with block tags.

Every direct change must equal its independently assembled prefix formula.
Serialize the five pentagon factor values and all four intermediate products;
also compare the ordered factor replay to direct `pentagon_word(f1)`
evaluation.  H1, H2, and P quotient values for `f1` must be identity at this
canary relation, or fail closed.

## 5. Exact D2 and Fox canaries

Construct the two PB3 and eleven PB4 raw Fox columns, require quotient value
identity and `D1=0` for every column, and pin:

```text
PB3 exact by v121
PB4 exact by v108
```

Do not infer `ker D1 = image D2`.

Run at least 110 actual word-bearing conjugation canaries, at least ten for
each of the eleven f-occurrence slots.  Stratify them across gamma-edge,
xy-action, and Q0-relator layers.  Every conjugator is nonempty.  Compare
direct Fox evaluation of `q r q^-1` with left translation by the full typed
slot context.  Cover H2 separately and cover both inverse pentagon factors.

Include at least two same-complete-context/different-conjugator pairs with
different freely reduced conjugates and equal full H1/H2/P tagged rows.
Include a separately labelled actual-product Fox additivity canary.  This
discharges the two successor debts recorded by v119.

## 6. Independent checker

The checker must import neither the producer nor any producer word, Fox,
context, quotient, pc-map, serialization, or mutation helper.  It may read the
same pinned immutable inputs.  It must freshly rebuild:

- free reduction, inverse, substitution, and paper products;
- g760 and the complete 6,441-row roster;
- E3/E4 arithmetic and both pc maps;
- all five source and five pentagon contexts;
- both hexagons, all five cofaces, and the literal pentagon;
- left Fox, D1, 2+11 raw D2 columns, the stacked target, every canary, and all
  direct quotient products.

Required destructive controls include at least:

```text
correction left/right
corrected/base sign
H2 u/z substitution
inverse Fox prefix
each negative pentagon factor and their order
coface slot 1/3 swap
E3/E4 rank or blob swap
context-name-only deduplication
dropped or changed block tag
fourth/third deletion swap
fine insertion index 4/3 swap
derived u or z order
one actual roster letter
one actual-product additivity term
```

Mutations must traverse the full reconstruction/validator path.  A digest-only
mutation harness is insufficient.

## 7. Terminals and claim boundary

The only positive terminal is

```text
R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_READY
```

It means only that the complete typed raw input for the later all-seven
orbit/stacked solve is independently replayed.  It means no orbit image,
membership result, correction, lift, fake, or Ihara witness.

Fail-closed terminals must distinguish at least:

```text
UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE
UNKNOWN_INPUT:PB3_PRESENTATION_PIN
UNKNOWN_INPUT:RAW_FORMULA
UNKNOWN_INPUT:FOX_CANARY
UNKNOWN_RESOURCE:<phase>
```

All mathematical promotion flags beyond bounded preflight are false.

## 8. GHA driver and report

The ASCII-only driver must use the generic `gap-run.yml`, exact source pins,
one fixed artifact path, exact-one producer/checker markers, pipefail, and a
single fail-closed timeout.  It may launch one Python producer followed by one
Python checker; no parallel local execution contract is needed.  Supply
selftest/preflight mode and production-preflight mode, but do not dispatch.

The reply must report static audit, hashes, expected runtime/RSS, precise GHA
preamble, terminals, mutation count, and every remaining UNKNOWN.  End with

```text
R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_STATIC_READY
```
