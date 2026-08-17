# Luna reply 157ab — tuple-v4 independent audit

## Verdict

PASS — dispatch-ready under the stated static/lightweight audit scope.

This is a dispatch-readiness result only.  It makes no A/B conclusion.  No
local GAP, full campaign, Git, or GHA action was run.

## 1. Fiber orientation and semantic binding

The producer's tuple product is `tmul(a,b) = (a.roof*b.roof,
a.block*b.block)` with the explicit paper composition convention.  Its exact
section `sec` is a right inverse to the roof projection on the generated
subgroup, and `K` is the exact kernel of `H' -> P'`.  For the section element
`h0 = sec[target_roof]` and any `h` in the same `H'` fiber,
`h0^-1*h` has identity roof and lies in `K`; hence `h = h0*k`.  Conversely
every `h0*k` is in `H'` and has the same roof.  Therefore the complete fiber
is the producer's right fiber `h0*K`, not `K*h0` and not a source-word
coset.

The frozen signed source word is replayed only to bind each roof/key.  The
literal word is not required to be in `H'`; `h0` is obtained from the exact
H' Schreier section above that roof.  The raw five-component A.18 matrix
defect is evaluated on every serialized element of each reconstructed
`h0*K`, with identity and nonidentity counts and witness checks.

## 2. Exactness and order gates

The producer and checker use uncapped BFS/closure operations throughout:

- `H` and the projected sections are exhaustively traversed;
- Schreier relators generate the kernel;
- the kernel is exhaustively enumerated and its generators are reduced only
  by exact enumeration (no heuristic or order cap);
- the normal closure starts at `[x,y]`, tests conjugates by both generators
  and inverses until closed, and requires projected order `|P'|`;
- quotient cosets are exhaustively traversed and order identities are gated.

The receipt and independent checker require the stated values
`|P|=1469664`, `|P'|=367416`, `|H|=105815808`, `|H'|=2939328`, and
`|K|=8`, together with the exact kernel elements/generators and all 972
rows.  There is no sampling or word-length bound in the full path.

## 3. Source-word regression

Both self-tests emit and require the frozen negative regression:

```text
D972_B4_BURAU_V4_SOURCE_WORD_ROOF_ONLY_NEGATIVE_PASS row=2 exponent=(-4,-8) nonzero=956
```

Thus row 2 has free abelianization `(-4,-8)`, and 956/972 rows have
nonzero exponent pairs.  This blocks reintroduction of the invalid premise
that every literal source word lies in `H'`.

## 4. Checker independence and adversarial gates

The checker does not import the producer or earlier tuple helpers.  It
rebuilds the roof, finite-field arithmetic, Burau generators, all five A.18
pairs, tuple operations, exact section/Schreier kernel, normal closure,
quotient, and complete fibers independently.  It replays all 972 words for
roof/key binding and losslessly verifies source hashes, artifact hashes,
semantic roles, h0 membership/projection, kernel completeness, fiber
digests, and every raw defect/count/witness.

The checker self-tests reject source word/key corruption, product-orientation
mutation, h0 corruption, kernel deletion (including the trivial-kernel toy
case), defective kernel data, and source-role drift.  Status and count gates
are fail-closed: calibration all-pass remains
`UNKNOWN_BURAU_SPECIALIZATION_ALLPASS`; only a q5 zero-fiber producer
candidate can be promoted by checker agreement to
`B4_A_BURAU_FINITE_ZERO_FIBER_CROSSCHECKED`.

## 5. Workflow audit

The workflow is bound to the exact branch
`sol/d972-dmtcp-provision-v420` and the versioned producer/checker/frozen
artifact paths, with read-only contents permission and
`persist-credentials: false`.  It runs q3/a=-1 and q4/a=2 calibration lanes
in parallel, self-test before full execution, then independently checks both
receipts before enabling the q5/a=2,4 matrix.  Calibration and q5 artifacts
are attempt-specific and uploaded with `always()`.

The pinned Python/SymPy/mpmath requirements use hashes; Python 3.13 and
SymPy 1.14.0 are checked.  Each lane applies `ulimit -v 12000000`, has a
360-minute timeout, captures pipeline exit status with `PIPESTATUS`, checks
marker cardinality and receipt row/key/index gates, and rejects
`UNKNOWN_RESOURCE`.  The exact final marker is checked for the expected
receipt path.  q5 accepts only the producer candidate or all-pass status and
then runs the independent checker with both calibration receipts.

## 6. Lightweight evidence

Commands run (and only these runtime checks):

```text
python -B -m py_compile search/d972_b4_burau_fiber_v4.py search/check_d972_b4_burau_fiber_v4.py
python -B search/d972_b4_burau_fiber_v4.py --self-test
python -B search/check_d972_b4_burau_fiber_v4.py --self-test
python -c "import yaml; p=yaml.safe_load(open('.github/workflows/d972-burau-tuple-v4.yml')); print('YAML_PARSE_PASS',list(p['jobs']))"
```

Observed markers:

```text
D972_B4_BURAU_V4_SOURCE_WORD_ROOF_ONLY_NEGATIVE_PASS row=2 exponent=(-4,-8) nonzero=956
D972_B4_BURAU_FIBER_V4_NEGATIVE_FIXTURES_PASS
D972_B4_BURAU_FIBER_V4_SELFTEST_PASS
D972_B4_BURAU_FIBER_V4_SOURCE_WORD_ROOF_ONLY_NEGATIVE_PASS row=2 exponent=(-4,-8) nonzero=956
D972_B4_BURAU_FIBER_V4_CHECKER_SELFTEST_PASS
D972_B4_BURAU_FIBER_V4_CHECKER_FINAL_MARKER status=PASS
YAML_PARSE_PASS ['calibrate', 'q5']
```

## SHA-256 of audited files

```text
search/d972_b4_burau_fiber_v4.py          AA8726570C58840A000B4B247B34ECCD39A958F97087E6745216E2055B578CEC
search/check_d972_b4_burau_fiber_v4.py    BB398FE265BB81D5DC36312B4468238B8420FC866CC6A8CAE7AD1EACEE5AB2C7
.github/workflows/d972-burau-tuple-v4.yml 52641B62F17D63B2399CC5833918049E3A1AFC78C40AC1FF3DD8508B7F00AC24
sol/luna_reply_157u_tuple_v4_semantic_repair.md EBE068F3881452290F02FDEFB14043DAA15193F58559FEE13FEC008DCAD7CF4C
```
