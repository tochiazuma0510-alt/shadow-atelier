# Luna reply 154 — GF(5) finite Burau fiber producer

Implemented only the authorized producer:

- `search/d972_b4_burau_fiber_v2.g`

The repaired v1 producer was copied into a new versioned lane.  This v2 lane accepts only `(q,a)=(5,2)` and `(5,4)`, uses prime-field digits `[0..q-1]`, and has permutation degree

```text
36 + 5*5^4 = 3161
```

It preserves the common-word `E(F2')=[H,H]` gate, exact `H'` projection kernel/cosets, all 972 roof word/key replays, literal A.18 maps, reverse-list `PaperProd`, the Artin `x13` canary, separate identity/nonidentity finite image-defect counts, and candidate-only status `CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER`.

The parse-safe selftest checks the GF(5) vector bijection, all three B4 Artin relations and determinants, one-line permutation serialization, reversed `PaperProd`, reversed `x13`, swapped A.18 factors, an exact enumerated toy-kernel deletion mutation, and corrupted word/key mutations.  Full mode additionally asserts `Length(Elements(K))=Size(K)`, distinct complete enumeration of the actual projection kernel, fixation of the roof block by every kernel element, and incompleteness after deleting exactly the last enumerated kernel element (including the `|K|=1` case); this is recorded as `exact_kernel_canary` in the receipt with `complete` and `order` fields.  No local GAP run was performed, as required.  Static `git diff --check -- search/d972_b4_burau_fiber_v2.g` passes.

Frozen input bindings are unchanged from task 153:

| input | SHA-256 |
|---|---|
| `search/certs/d972_b4_word_key_artifact_v1_20260816.json` | `564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9` |
| semantic premise object (`M`, `P`, 972/324/648, index-3) | `3a2168fc88c86c21eea4bff6fd2958bf18fe7bcee506e0c3cdf6c6f2a2cef729` |
| `search/d972_b4_burau_fiber_v2.g` | `0ca63ada9c1524ef65ca4815c8eda506efa040b43ce4e42b5f061934f0d23d0b` |

## GHA handoff

The parent may invoke the existing workflow without editing it:

```text
gh workflow run gap-run.yml --ref <source-commit> \
  -f script=search/d972_b4_burau_fiber_v2.g \
  -f preamble='D972_B4_BURAU_Q:=5;; D972_B4_BURAU_A:=2;;' \
  -f out_dir=ci/out/burau-gf5-a2 -f timeout_min=330 -f with_pquot_packages=true
```

Quote-free selftest preamble:

```text
D972_B4_BURAU_Q:=5;; D972_B4_BURAU_A:=2;; D972_B4_BURAU_SELFTEST:=true;;
```

Expected producer output is `ci/out/d972_b4_burau_fiber_v2.json`.  A `(5,4)` run uses only `D972_B4_BURAU_A:=4;;`.  The 3161-point action and exact kernel enumeration may be substantially more expensive than GF(3)/GF(4); timeout, memory exhaustion, empty/broken fibers, or incomplete enumeration remain `UNKNOWN_RESOURCE`/UNKNOWN and never B.

No commit, push, or dispatch was performed.
