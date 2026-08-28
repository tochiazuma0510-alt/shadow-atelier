# Luna reply 226 / task249 seventh execution-order repair

Status: **UNEXECUTED**. I read AGENTS.md and task249 in full (with the
superseded repair contracts for context). Only the five authorized task226 files were edited. No
Python, Node, GAP, git, GHA, or network command was run.

## Repairs

1. Corrected the blockwise Fox signs:
   `d_raw=d_occ=-G`, `B_a=F-G`, and `e=d_raw-B_a=-F`. Both D1 images are
   retained; no false `D1(d)=0` condition is imposed.
2. Replaced coincident-key dictionary differences with accumulating sparse
   addition for xi, endpoints, translated-minus-original u0, and all related
   sparse rows. Added live zero-cancellation SELFTEST cases for `r_o=1`,
   `R_B(g)=1`, and translated `w_o=w_o`.
3. Added separate `seal_task192(self_digest)` and
   `seal_task198(self_digest_sha256)` adapters and retained exact sidecar
   authentication.
4. Fixed checker indentation and made COMPLETE reconstruction consume and
   compare authenticated task192 `g760/c_exact/corrected_word` and task198
   `occurrence_ledger` before ABI comparison. Verdict reconstruction SHA now
   hashes the fresh independent rebuild.
5. Added field-targeted, resealed mutation branches and before/after target
   digests for the exact 26-name roster; each caught reason must contain its
   exact gate and acceptance raises uncaught `MutationAccepted`. ABI seal is
   the sole intentionally stale seal mutation. Producer/checker/fixture rosters
   remain equal.
6. Added literal fresh rebuild comparisons for `words`, `occurrences`,
   `group`, `identities`, `w`, `epsilon`, `u0`, and the frozen ABI, plus exact
   signed u0 provenance and occurrence-u0 equality checks.
7. Added independent bounded PB3 arithmetic with every finite triple and both
   inverse orders, and direct PB3/PB4 bracket/order oracle calls to both
   SELFTEST paths.
8. Reordered producer SELFTEST so probes and production-shaped canaries are
   attached before validation, mutation execution, transcript attachment, and
   final validation. The checker validates, reruns/compares probes, then runs
   its independent mutation suite.
9. Made `word_g0` and `word_a` mutations alter a signed generator letter, kept
   `word_f` distinct, and raised producer/checker `input_bytes` to the explicit
   2,100,000,000-byte finite bound, matching the driver estimate.
10. Pinned producer/checker/fixture exact bytes and SHA-256 in the serial GAP
   driver; kept driver itself unpinned, terminal checks anchored, and stale
   outputs fail-closed.
11. Added live malformed-input authenticator and live resource-budget probes;
   RSS is measured when available rather than published as an unenforced
   `None` value. UNKNOWN remains `accepted=false, independent=false`.
12. Eighth repair: changed the three driver SHA-256 pins to exact lowercase
   `sha256sum` serialization without weakening the case-sensitive equality
   gates. Producer/checker/fixture source contents were not altered.

## Static checks

Producer/checker/fixture mutation rosters match at exactly 26 entries. JSON remains
ASCII-only. The checker declarations are top-level at column zero, its mutation
validation try/except/else is outside the conditional reseal branch, and the
`abi_seal` mutation reaches that common block. The implementation remains
unexecuted and no acceptance claim is made.

Frozen task226 ABI spelling for task227:

```text
schema = d972-r07-v216-specialization-abi/v1
occurrences[i].u0 = translated_w_o - w_o
abi.u0[i] = {
  ordinal,
  terms=w_o,
  translated_terms=translated_w_o,
  source_coefficient_terms=[
    {source=translated, coefficient=1, terms=translated_w_o},
    {source=original, coefficient=-1, terms=w_o, ancestry=occurrences[i].ancestry}
  ]
}
```

Exact 26-name mutation roster:

```text
word_g0, word_a, word_f, ledger_block, ledger_sign, ledger_orientation,
ledger_prefix, group_width, group_brackets, actor_convention, fox_d_occ,
fox_d_raw, fox_B_a, fox_e, fox_D1_d, fox_D1_e, occurrence_p, u0_value,
u0_provenance, abi_seal, task192_binding, task198_binding, terminal_input,
terminal_resource, output_freshness, forbidden_conclusion
```

Static audit: `check_attestation` is top-level at column zero; `abi_seal`
enters the common validation try/except/else block with resealing skipped.
The PB3 oracle loops every finite triple `(a,b,c)` and both inverse orders.

Measured source identities (PowerShell bytes/SHA-256; no runtime execution):

```text
producer 39821 78cc0c12252f2d68ebd9fbe456f27df75498689ee5ec09bce40fe275e79e1fe7
checker  33849 6e0ce2412ee8798fb08647330f6656ef2a52e9eafbf96810b41b2726480ac278
fixture   1187 91c62b70b3275e9e3bee9689bd677049adc172cb0519a2ccf2808d17d6cabef3
```

Edited driver identity (PowerShell bytes/SHA-256, lowercase serialization):

```text
driver 5167 178dc9555238a526ef83b16d50a20b4523b1a153dcba7ccc353478efd01dc8e2
```

The reply is the report itself; its final byte/SHA identity is supplied
out-of-band in the task return to avoid a self-referential embedded digest.

```text
A2 PAPER CONTRACT:                 1/3
A2 IMPLEMENTATION SELFTEST:        0/1 UNEXECUTED
A2 ACTUAL SPECIALIZATION:          0/1 AWAITING A0/A1
A3 AND LATER:                      UNCHANGED
COMPATIBLE COFINAL LIFT / FAKE / IHARA: NOT DECLARED
```
