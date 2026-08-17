# Luna reply 154b — independent GF(5) Burau cross-check

Implemented only:

- `search/check_d972_b4_burau_fiber_v2.py`

At the time of this v2 implementation the v1 checker was unchanged; it was
subsequently repaired and relation-audited in its own task.  This v2 checker
remains standalone and does not import it.  No local GAP run, full q=5 scan,
commit, push, or dispatch was performed.

## Independent implementation

The checker is standalone and does not import v1, GAP, the producer, or
producer helpers.  It independently reconstructs the frozen 36-point D972
roof, all 972 signed word/key replays, prime-field GF(5) Burau arithmetic at
`(q,a)=(5,2)` or `(5,4)`, the six pure generators, the five literal A.18
pairs, and the opposite-convention raw defect.

For a receipt it reconstructs `H`, `H'`, the 36-point pointwise stabilizer
kernel using SymPy 1.14, and every exact nonempty `h0*K` coset.  Producer
orders, kernel data, representatives, counts, witnesses, status, and optional
digests are not trusted.  Supplied kernel generators are additionally
shape-checked, tested inside the independently reconstructed pointwise kernel,
and required to generate exactly that kernel (an empty list or explicit
identity generators are allowed only when reconstructed `|K|=1`).  The producer runtime
`exact_kernel_canary` must contain `complete`, exact `order`,
`distinct_complete`, `fixes_roof_block`, and `deleted_element_incomplete`, all
passing.  The checker also deletes one element from the reconstructed full
kernel enumeration—including identity to `[]` when `|K|=1`—and fail-closes if
completeness is not detectably lost.  Candidate status
`CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER` is promoted only after complete
independent replay; producer self-promotion to CROSSCHECKED is rejected.

The checker rejects unsupported parameters, syntax/error diagnostics, missing
or duplicate rows/keys, malformed one-line permutations, empty/incomplete
fibers, metadata/source digest drift, and all-pass claims containing a zero
fiber.  `UNKNOWN_RESOURCE` remains nonterminal UNKNOWN.

## Verification

Commands run:

```text
python -m py_compile search/check_d972_b4_burau_fiber_v2.py
python search/check_d972_b4_burau_fiber_v2.py --self-test
```

Both passed, with markers:

```text
D972_B4_BURAU_FIBER_V2_CHECKER_SELFTEST_PASS
D972_B4_BURAU_FIBER_V2_CHECKER_FINAL_MARKER status=PASS
```

The lightweight selftest covers GF(5) vector bijection, all three B4 Artin
relations (two braids and the distant commuting relation), and determinant
canaries, all 972 roof replays, PaperProd reversal, reversed `x13`, swapped
leading A.18 factors on a common word, kernel-element deletion, and corrupt
roof word/key mutations.  It does not construct or scan the full q=5 finite
group.

Checker SHA-256:

```text
23F91C877CD4D92E5CBB0742F9C78E5FD397A6D346A107A7A342BF8F3D7019CB
```

Frozen source bindings retained from the v1 artifact are:

- word artifact SHA-256: `564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9`
- canonical rows SHA-256: `283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930`
- target tuple SHA-256: `32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91`
- semantic premise SHA-256: `3a2168fc88c86c21eea4bff6fd2958bf18fe7bcee506e0c3cdf6c6f2a2cef729`

## Resource risk

At q=5 the combined action degree is `36+5*5^4 = 3161`.  SymPy
Schreier–Sims, derived-subgroup construction, 36 successive stabilizers, and
exact kernel enumeration are the dominant costs.  No timing or finite-fiber
status is inferred from the lightweight selftest.  Any cap, timeout,
truncation, empty/broken projection fiber, or producer/checker disagreement
must remain UNKNOWN.

## Key-image regression repair

The key-to-roof reconstruction now applies D9 block offsets `0,9,18` and the
PSL block offset `27`.  The selftest explicitly compares this reconstruction
against the direct roof-word image for all 972 stored rows.  Updated checker
SHA-256 is the value recorded above.

The v1 sibling checker was later updated independently for the same roof
offset regression and now carries the full three-relation gate; this does not
create an import or implementation dependency between v1 and v2.

The final v2 audit revision also performs the supplied-generator and actual
reconstructed-K completeness gates on the terminal receipt path, including
the empty/identity-generator and trivial-kernel deletion edge fixtures in the
lightweight selftest.  After the final generator-conversion edit,
`py_compile` and `--self-test` were rerun and passed;
the final checker SHA-256 is
`23F91C877CD4D92E5CBB0742F9C78E5FD397A6D346A107A7A342BF8F3D7019CB`.
