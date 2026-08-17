# Luna reply 157r — exact D972 shadow power/order spectrum

## Result

Implemented the authorized four-file lane:

- `search/d972_power_spectrum_v1.g`
- `search/check_d972_power_spectrum_v1.py`
- `.github/workflows/d972-power-spectrum-v1.yml`
- this reply

The producer is intentionally not run locally.  The final numerical order
spectrum is therefore a GHA result, not a local claim.  The producer is
fail-closed unless the frozen semantic roof scan returns exactly 972 distinct,
settled rows and the frozen target-key digest
`9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62`.

## Exact construction and receipt contract

The GAP producer reads the frozen D972 constructors and runs the complete
`D972ScanCalibrationBase` scan.  It then canonicalizes every row into the
lexicographic frozen key order and stores its lossless degree-36 compact roof
permutation.  The receipt stores all 972 rows, the full 972 x 972 product
table, row/product SHA-256 digests, identity, two-sided inverse indices, and
exact orders.

Shadow multiplication is the practical GT-shadow law from
`papers/txt/2008.00066-what-are-gt-shadows.txt`, Proposition 2.14 and formulas
(2.52)/(2.55):

`m = 2*m1*m2 + m1 + m2 (mod 18)` and
`f = f2 * f1(x^(2*m2+1), f2^-1*y^(2*m2+1)*f2)`.

The GAP side records orientation and virtual-cyclotomic canaries and checks
closure for every product-table entry.  Associativity is recorded as the
complete function-composition generator/table gate: the affine lambda law is
associative and the f-part is composition of endomorphisms, while every pair
is exhaustively closed and serialized.

The Python checker does not import the producer or call GAP.  It independently
rebuilds the D9^3 + PSL(2,8) degree-36 roof, verifies the artifact SHA and
canonical row digest, replays all 972 authenticated common words, recomputes
all 945,441 products from (2.55), and rejects any corrupted key, compact
permutation, product entry/digest, identity, inverse, or order.  It then
rebuilds every row power and order from the independently recomputed table.

## Outside-label boundary

The checker searches repository certificates for a lossless authenticated
`Im(Ih_M)` label, requiring the exact semantic M and matching frozen artifact
and target-key digests.  No such authenticated label is accepted by this
lane, so the receipt is explicitly:

`outside_label_status=UNKNOWN_MISSING_AUTHENTICATED_LABEL`

`outside_rows` and `outside_order_histogram` remain null, and no 648 split is
inferred from cardinality, complement, row order, `m`, or a hard-coded list.
The all-972 spectrum remains valid input to the later CRT power-absorption
theorem and is not A/B evidence.

## Workflow and static checks

`.github/workflows/d972-power-spectrum-v1.yml` is restricted to the exact
`sol/d972-dmtcp-provision-v420` push branch and closed repository paths.  It
uses credential-free checkout, installs only the GAP runtime, runs the
selftest before the full producer, then the independent checker, preserves
`PIPESTATUS`, and always uploads attempt-unique logs and receipts.  There are
no arbitrary producer inputs or sample/bounded completeness claims.

Local checks (no GAP, no full scan, no GHA, no git operations):

- `python -m py_compile search/check_d972_power_spectrum_v1.py` — pass
- `python search/check_d972_power_spectrum_v1.py --self-test` —
  `D972_POWER_SPECTRUM_CHECKER_SELFTEST_PASS`
- Python AST parse — pass
- YAML parse — `YAML_PARSE_PASS`

Expected GHA runtime is bounded by the six-hour job timeout; the complete GAP
roof scan and 945,441 exact product replays are deliberately deferred to the
hosted worker.  No local numerical spectrum or outside conclusion is claimed.

## SHA-256

```text
search/d972_power_spectrum_v1.g
F9A3A7FDB6224DBDE68C914A245B2EDA8E9C057BD1AEE3DAC2E93D8F5CCABBC4

search/check_d972_power_spectrum_v1.py
A17020B3F24E57483E0D647AD487FEE35E73D712BFC581C2CEA3604FE2525C8D

.github/workflows/d972-power-spectrum-v1.yml
1764EA9AC930217B724CC1F214714A5379AE5E92FB30C948E7B24E2F22C2C472
```

No GHA run ID or commit SHA exists in this child lane; the parent session owns
broker operations.
