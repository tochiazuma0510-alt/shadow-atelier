# Luna task 157r - exact D972 shadow power/order spectrum on GHA

Role: Luna implementation/computation. Do not run GAP locally. Parent alone
will commit, push, and dispatch after audit.

Authorized new files only:

- `search/d972_power_spectrum_v1.g`
- `search/check_d972_power_spectrum_v1.py`
- `.github/workflows/d972-power-spectrum-v1.yml`
- `sol/luna_reply_157r_d972_power_spectrum.md`

Goal: determine which finite orders occur among the exact 972 D972 shadows,
and, only if a lossless authenticated arithmetic/outside labeling already
exists, the order spectrum of the 648 outside rows. This is input to the CRT
power-absorption theorem; it is not itself A/B evidence.

Requirements:

1. Build the semantic roof `M=K^(9) intersect N_S4` through the frozen current
   D972 constructors and enumerate exactly 972 settled/charming shadows.
2. Construct the shadow multiplication using the published composition law
   (Proposition 2.14 / formula (2.52)/(2.55)), with explicit orientation
   canaries, and compute the identity, inverse, and exact order of all rows.
   Gate closure, associativity (exhaustively or via a mathematically complete
   generator/table check), and agreement with the frozen 972 row keys.
3. Emit a lossless receipt sufficient for a Python checker that does not call
   GAP or reuse the producer multiplication helper. The checker must rebuild
   row powers/orders from the serialized data, reject a corrupted product,
   key, identity, or row order, and gate the exact 972 count/digests.
4. Search the repository for an authenticated lossless `Im(Ih_M)` / 324-row
   arithmetic label. Use it only if its semantic M and key digests match.
   Otherwise report `outside_label_status=UNKNOWN_MISSING_AUTHENTICATED_LABEL`
   and do not infer the outside set from cardinality, row order, complement,
   m, or a hard-coded 648 split. The all-972 order spectrum remains useful.
5. The GHA workflow must be exact-branch, closed-path, credential-free,
   read-only, fail-closed, six-hour, run producer then independent checker,
   and always upload attempt-unique logs/receipt. No arbitrary inputs and no
   bounded/sample computation masquerading as completeness.
6. Run only static syntax/YAML/checker self-tests locally. Do not run the GAP
   producer, commit, push, or dispatch. Report hashes, expected runtime, and
   any semantic blocker.

Use the GAP wrapper only in GHA if needed. Keep every PowerShell file ASCII;
prefer a bash GHA step invoking GAP exactly as existing Linux workflows do.
