# Luna reply 153 — finite Burau fiber

Implemented the authorized versioned pair:

- `search/d972_b4_burau_fiber_v1.g`
- `search/check_d972_b4_burau_fiber_v1.py`

No workflow YAML, commit, push, dispatch, or heavy local GAP run was performed.  The independent Python checker selftest passes:

```text
D972_B4_BURAU_FIBER_CHECKER_SELFTEST_PASS
D972_B4_BURAU_FIBER_CHECKER_FINAL_MARKER status=PASS
```

The producer uses the unreduced Burau block `[[1-a,a],[1,0]]`, supports `q=3` and `q=4` (GF(4) integer encoding `a=2` is the primitive element), checks braid/invertibility canaries, uses the explicit reverse-list `PaperProd`, and preserves `x13=PaperProd([s2,s1^2,s2^-1])`.  It reconstructs all six pure generators and the five literal A.18 pairs.  For each artifact row it independently replays the representative word to the stored roof key, obtains an exact representative with `PreImagesRepresentative(pi|H',f)`, and scans the complete coset `h0*ker(pi|H')`; no word-length/random truncation is used.

Receipt contract includes exact `|H|`, `|H'|`, projection order and kernel order, every row’s exact `H'` representative and complete kernel-coset size, separate identity/nonidentity finite image-defect counts, first witnesses, `E(F2')=[H,H]`/common-word provenance, semantic premise digest, and all five negative-test labels.  The checker independently reconstructs the kernel and cosets, so the producer does not duplicate all kernel elements or every coset in the receipt.  GAP emits only `CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER`; only producer/checker agreement may promote it to `B4_A_BURAU_FINITE_ZERO_FIBER_CROSSCHECKED`.  Finite matrix identity is recorded only as the tested raw-A.18 image defect `D_(q,a)(h)=I`, never as profinite identity.

Frozen input bindings:

| input | SHA-256 |
|---|---|
| `search/certs/d972_b4_word_key_artifact_v1_20260816.json` | `564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9` |
| semantic premise object (`M`, `P`, 972/324/648, index-3) | `3a2168fc88c86c21eea4bff6fd2958bf18fe7bcee506e0c3cdf6c6f2a2cef729` |
| `search/d972_b4_burau_fiber_v1.g` (current draft) | `8a65fe2fa8c56a2b7552ace96df482cc1d5ad32ee28512824946a44daf59b4d8` |
| independent SymPy/roof checker | `819519e93a95e0fbff7b7d4d51f5af633da029e033f33038f100db968e53169e` |

## GHA handoff

After the parent session commits the versioned files, invoke the existing workflow without editing it:

```text
gh workflow run gap-run.yml --ref <source-commit> \
  -f script=search/d972_b4_burau_fiber_v1.g \
  -f preamble='D972_B4_BURAU_MODE:="run";; D972_B4_BURAU_Q:=3;; D972_B4_BURAU_A:=-1;; D972_B4_BURAU_OUTPUT:="search/certs/d972_b4_burau_fiber_q3_a-1.json";;' \
  -f out_dir=search/certs -f timeout_min=330 -f with_pquot_packages=false
```

Expected artifact: `search/certs/d972_b4_burau_fiber_q3_a-1.json`; run the checker against that artifact after download.  If q3 is all-pass, run the same invocation in parallel with `D972_B4_BURAU_Q:=4;; D972_B4_BURAU_A:=2;;` and output `search/certs/d972_b4_burau_fiber_q4_a2.json`.  The current producer/checker contract advertises only these GF(3)/GF(4) lanes; all-pass remains `UNKNOWN`, and timeout/resource failure remains `UNKNOWN_RESOURCE`.

Resource scale is degree `36+5q^4` (441 at q=3; 1316 at q=4), with exact kernel enumeration and complete coset scans.  The q=4 lane is consequently substantially more memory-intensive; use the 330-minute workflow timeout and retain the fail-closed status if enumeration does not finish.
