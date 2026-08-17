# 157u tuple-v4 semantic repair

## Verdict

PASS for the versioned implementation and static/self-test contract.  v4 is a
new producer/checker/workflow; committed v3 was not edited.  The invalid
literal-source-word-in-`H'` premise is removed.  The frozen word is replayed
only to authenticate its roof/key; the exact H' section supplies `h0`, and
the complete fiber is reconstructed as `h0*K`.

No local GAP, full campaign, commit, push, or dispatch was run.

## Authorized files

- `search/d972_b4_burau_fiber_v4.py`
- `search/check_d972_b4_burau_fiber_v4.py`
- `.github/workflows/d972-burau-tuple-v4.yml`
- this reply

The producer retains the tuple representation, exact projected-section BFS,
Reidemeister--Schreier kernel relators, uncapped kernel enumeration,
normal-closure completion, exact coset traversal, q3/q4 calibration values,
q5 `(a=2,4)`, and `UNKNOWN_RESOURCE` fail-closed behavior.  Receipt schema
and terminal marker are versioned as `d972-b4-burau-fiber/v4-lowmem` and
`D972_B4_BURAU_FIBER_V4_FINAL`.

## Semantic repair

The producer now emits and authenticates:

```text
source_word_role = frozen signed word binds roof/key only; literal word need not lie in H'
hprime_preimage_role = exact H' Schreier section representative above the replayed roof
fiber_reconstruction = complete right fiber h0*K with exact matrix-only kernel K
```

For every row it checks direct roof/key replay, obtains the section element
above that roof, gates its exact projection and H' membership through the
section/kernel decomposition, and enumerates every element of `h0*K`.  There
is no `common_word_in_hprime` gate or receipt field.

The producer and checker independently require the frozen negative regression:
row 2 has free abelianization `(-4,-8)` and exactly 956 of 972 rows have
nonzero exponent pairs.  This prevents restoration of the v3 failure.

## Independent checker

The v4 checker does not import the producer or either earlier checker.  It
independently reconstructs compact D972 roof generators, GF(3)/GF(4)/GF(5)
arithmetic, Burau pure generators and all five A.18 pairs, tuple products and
inverses, exact H' section/Schreier kernel, quotient order, and complete
kernel enumeration.

For every receipt it independently authenticates producer source SHA, frozen
artifact hashes, semantic digest, generator/A.18 order, roof orders, q/a,
row count, source-role fields, H/H'/projection/kernel orders, kernel element
and generator completeness, h0 membership/projection, every reconstructed
fiber digest, and every raw five-A.18 defect/count/witness.  The actual
reconstructed-K deletion is checked for incompleteness.  Corrupt product
orientation, source word/key, source-role metadata, h0, kernel data, fiber
digest, and defect counts fail closed in the corresponding gates.  The
producer's serialized digest is used only as a binding; fiber membership,
kernel enumeration, coset contents, and defect counts are recomputed by the
checker.

The q5 workflow first independently checks both exact q3/q4 calibration
receipts, then runs q5 and checks its receipt with both calibration paths and
receipt SHA bindings.  Only a producer candidate plus checker agreement emits
`B4_A_BURAU_FINITE_ZERO_FIBER_CROSSCHECKED`; an all-pass remains UNKNOWN.

## Static evidence

Commands run:

```text
python -B -m py_compile search/d972_b4_burau_fiber_v4.py search/check_d972_b4_burau_fiber_v4.py
python -B search/d972_b4_burau_fiber_v4.py --help
python -B search/check_d972_b4_burau_fiber_v4.py --help
python -B search/d972_b4_burau_fiber_v4.py --self-test
python -B search/check_d972_b4_burau_fiber_v4.py --self-test
python -B -c "import yaml; ...; print('YAML_PARSE_PASS', ...)"
git diff --check -- search/d972_b4_burau_fiber_v4.py search/check_d972_b4_burau_fiber_v4.py .github/workflows/d972-burau-tuple-v4.yml sol/luna_reply_157u_tuple_v4_semantic_repair.md
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

`git diff --check` reported no whitespace issue on the authorized v4 paths.

## SHA-256

```text
search/d972_b4_burau_fiber_v4.py          AA8726570C58840A000B4B247B34ECCD39A958F97087E6745216E2055B578CEC
search/check_d972_b4_burau_fiber_v4.py    BB398FE265BB81D5DC36312B4468238B8420FC866CC6A8CAE7AD1EACEE5AB2C7
.github/workflows/d972-burau-tuple-v4.yml 52641B62F17D63B2399CC5833918049E3A1AFC78C40AC1FF3DD8508B7F00AC24
```
