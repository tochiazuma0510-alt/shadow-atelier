# Luna reply 152 — k=9 explicit-BQ relative bridge v6

Date: 2026-08-17.  No local GAP, workflow edit, dispatch, commit, or push
was performed.  The only executed checks were Python compilation/selftests.

## Result

v6 closes the finite full-marked quotient bridge that v5 did not target:

\[
  P=\langle \widetilde s_1,\widetilde s_2\rangle
       \longrightarrow BQ=\langle s_1,s_2\rangle,
  \qquad \widetilde s_i\mapsto s_i,
\]

where `BQ` is the explicit finite permutation model from
`D972BuildBase(false)`, with order `8,817,984` and pure order `1,469,664`.
For each preregistered unit `z in {1,2,4,5,7,8}`, the producer constructs
the C9 lift `(s_i,c9^z)`, checks the braid relation, marked images, onto map,
and requires `|ker(P -> BQ)|=9`.  Its pure subgroup is separately mapped onto
the fixed M-model and requires pure kernel order 9.  Thus `N <= M` is recorded
only from the kernel composition `B3 -> P -> BQ`; it is not inferred from an
order coincidence.

The five A.18 maps are still checked in native order
`[x12,x13,x23]`, with paper-to-native `[1,3,2]` and
`tau=X^-1*Y^-1`.  The finite five-coface map and its inverse are checked on
generators, so `N_PB3_intersection_exact` is a finite-presentation kernel
statement rather than a one-way relator check.

## Critical v5 repair

The frozen word artifact rows are exactly `[m,key,word]` (three fields).  The
v5 producer accessed `rows[ri][4]`, which is out of range in GAP and would stop
the row scan before producing a valid receipt.  v6 uses `rows[ri][1]` for `m`
and `rows[ri][3]` for the signed word, and has a static row-shape gate.

## What is still not terminal

The direct BQ and finite five-coface bridge does not prove the B4 statement.
Each v6 cell therefore emits these fields as literal `UNKNOWN` and the
checker rejects any attempted promotion:

```text
b4_normality             UNKNOWN
isolated                  UNKNOWN
all_shadows_settled       UNKNOWN
semantic_M_binding_exact  false
outside_648_identified    false
terminal_allowed          false
```

If a GHA cell has a genuine zero among the 972 finite row bits, v6 labels it a
`FINITE_C9_ROW_SCAN_NONTERMINAL` candidate, not B4-A.  If the finite bridge
gate fails, row bits and zero count are emitted as JSON `null`; the producer
never manufactures a zero by filling unavailable rows with `false`.

## Versioned files

- `search/probe/b4_cal_v1/d972_b4_k9_relative_c3_v6.g`
- `search/check_d972_b4_k9_relative_c3_v6.py`
- `search/d972_b4_k9_relative_c3_v6_manifest.json`
- this report

SHA-256:

```text
3c017a0de2b6587b336cc24bcfe835dcbcddbfff6eb1d8a1a1fd94fb6bcd0bb4  search/probe/b4_cal_v1/d972_b4_k9_relative_c3_v6.g
a907fe990e512852ba94582b1396be49f19868d2891cd22f31adc3c631d5224a  search/check_d972_b4_k9_relative_c3_v6.py
240bce1f96d9f37f4eca1631d183e3f829fb0e48e6b2106c07709338ccb21afc  search/d972_b4_k9_relative_c3_v6_manifest.json
```

Static checks run:

```text
python -B -m py_compile search/check_d972_b4_k9_relative_c3_v6.py
python search/check_d972_b4_k9_relative_c3_v6.py --selftest
D972_B4_K9_RELATIVE_C3_V6_SELFTEST_PASS {'BQ_order': 8817984, 'kernel': 9, 'rows': 972, 'terminal': False}
```

Static source canaries also pass: no `FreeGroup`, no
`IsomorphismFpGroupByGenerators`, and no v5 `[4]` row access occurs in the
v6 producer.  A GAP runtime receipt is intentionally not claimed here.

## GHA preamble for the parent

```powershell
$env:D972_B4_K9_RELATIVE_C3_V6_SELFTEST='false'
$env:D972_B4_K9_RELATIVE_C3_V6_OUTPUT='ci/out/d972_b4_k9_relative_c3_v6.json'
.\gap.ps1 search/probe/b4_cal_v1/d972_b4_k9_relative_c3_v6.g
python search/check_d972_b4_k9_relative_c3_v6.py ci/out/d972_b4_k9_relative_c3_v6.json
```

The GHA run is needed to learn whether any of the six full-BQ cells actually
has kernel C9 and a finite zero row.  Even a zero row remains nonterminal
until the B4-normal/isolated/settled, semantic-M, and outside-648 receipts
are supplied.
