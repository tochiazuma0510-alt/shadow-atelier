# Sol reply 310 — task303/v5 GHA SELFTEST acceptance

## Verdict

**CROSS-CHECKED implementation SELFTEST; not an actual A0 result.**

The fixed-dual process map/reduce candidate which passed independent Sol(max)
static audit in task308 was executed on GHA and returned matching producer and
helper-nonshared checker PASS terminals.

```text
run id          33166406322
head sha        ec047436ee2fdfc8a6df1673105f4b8c5a678723
workflow        gap-run.yml
conclusion      success
artifact id     9683764319
artifact digest 68c91a6648a1e243d2ee7d6613a9bd1f458f2fcb2b2073519e1b5d887782525a
```

The artifact was downloaded outside the repository and independently read.
Its exact files include:

| member | bytes | SHA-256 |
|---|---:|---|
| `.ok` | 56 | `8ab0c769786279a254c5d56363eae525bd9f9e19dbf326206530cca10b48e26a` |
| `.selftest.json` | 53,226 | `d2332a0381a4bf55d50ff05bf4ea6d30f75e83f98efb533a771f1deb73e64c17` |
| `.selftest.log` | 279 | `c63bd5e2eb91f5379aaca50e049a12129c0a75c46d7168c5e246488069a4ed02` |
| `.selftest.verdict.json` | 6,589 | `1c6d825fa1115fa737bd2fd8540dcfa6807b93a4258fa14bb0318d5af5f89cd7` |

## Observed gates

The log contains exactly one each of

```text
R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_SELFTEST_PASS
R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_PRODUCER_TERMINAL PASS
R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_CHECKER_PASS
R07_NORMALIZED_EXACT_COMMON_WORD_PARALLEL_V5_CHECKER_TERMINAL PASS
```

The runner selected four processes.  The producer receipt and independent
checker verdict agree on all four cases, worker counts 2/3/4, two distinct
frozen epochs with state isolation, and 20 attempted / 20 rejected mutations.
The producer reports 14 completed batches, 44 completed shards, and 112
synthetic pair evaluations.  Both files bind every mathematical conclusion
flag (`common_word`, `finite_common_word`, `cofinal_lift`, `fake`, and
`ihara_witness`) to false.

Under the repository hierarchy this producer/checker agreement is
**cross-checked**, not Lean-verified.  The fixture is synthetic and the
production resume adapter remains absent, so A0 actual stays 0/1.

```text
TASK303 STATIC SOL(MAX) AUDIT:             PASS
TASK303 GHA PRODUCER/CHECKER SELFTEST:     CROSS-CHECKED
AUTHENTICATED TASK192 PRODUCTION ADAPTER:  NOT YET IMPLEMENTED
A0 ACTUAL:                                 0/1
FAKE / IHARA:                              NO CONCLUSION
```

`TASK310_R07_TASK303_V5_GHA_SELFTEST_CROSS_CHECKED`

