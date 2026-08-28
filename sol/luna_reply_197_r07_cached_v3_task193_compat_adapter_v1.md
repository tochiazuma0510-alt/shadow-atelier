# Luna reply 197 - cached-v3 to task193 compatibility adapter v1

No Python, GAP, Node, git, GHA, network, or production execution was
performed. This is a static repair and adversarial source audit only. My
edits were confined to the five authorized task197 paths; because git was
forbidden, this statement is about my edits and is not a claim about the
shared worktree.

## 1. Objective and exact type mismatch

The repaired adapter accepts the positive task192 envelope

```text
d972-r07-normalized-exact-cached-colgen/v3
R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD
```

and emits the task186/task193 envelope

```text
d972-r07-normalized-exact-common-word-colgen/v2
R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD.
```

The producer deep-copies the whole authenticated v3 value, removes the old
outer seal, changes only `schema` and `terminal`, and reseals it (producer
lines 316--329). The final recursive comparison includes the seals and
requires exactly the three ordered changes `/schema`, `/self_digest`, and
`/terminal` (producer lines 401--415). It therefore does not alter a word,
coefficient, sparse row, selected column, exponent, or provenance field.
Both full external checkers remain load-bearing in the driver; the adapter
checker does not replace either one.

## 2. Authorized files and exact identities

The four non-reply task197 identities, recomputed from current bytes with
PowerShell `Get-FileHash`, are:

| authorized file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_cached_v3_task193_compat_adapter_v1.py` | 41745 | `5c39321ef16dd25b09328cfd0bd08ba55d166aa6fc4b2f22534e22697739e7af` |
| `crosscheck/check_d972_r07_cached_v3_task193_compat_adapter_v1.py` | 34820 | `af7bca3dd2ada06c254150282bd2d5338d30292a4288f5a221353d4dbb6d6ff1` |
| `search/d972_r07_cached_v3_task193_compat_adapter_gha_driver_v1.g` | 15036 | `6d6ca58730faa8a26f3c5759de4d989b779ea0dbb28790f8693f587baa2f92e8` |
| `search/certs/d972_r07_cached_v3_task193_compat_adapter_selftest_v1_20260828.json` | 673 | `1d7ae0025aff04094123e9c6fb85cb0d27f83328ef192329eb464ebc84e863b9` |

The reply identity is intentionally omitted from its own body to avoid a
self-referential hash; it is to be reported out of band after this file is
closed.

Producer lines 45--60 and checker lines 44--60 contain identical imported
pin tables. Driver lines 13--26 and 54 pin the task197 artifacts and the
same external cone. I independently recomputed every following imported
identity; all matched:

| imported file | bytes | SHA-256 |
|---|---:|---|
| task192 producer | 193704 | `f27b4971351832b8730fb8cce4e782e893a958dfb850203cc735c7bc3aa31f37` |
| task192 checker | 154009 | `dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10` |
| task192 driver | 11548 | `2f7ff7b459e46d014268907ff5ba5f03c035836e8f8df79a2c5f4cdc3b75351d` |
| task192 fixture | 276 | `c49f434ad3daf1cc661ba45563dbb9557d436f91dca78c8ee0f47ed70332da12` |
| task186 producer | 63053 | `ec73db0a474b3b52d69e19862e8185ae22423b2406f3922b5669d9a4e85fafab` |
| task186 checker | 54982 | `8898798d0d6a9e0b6cd67402e74ba0dc5048b4797a0f7a9657e58d70d553c488` |
| task186 driver | 9630 | `a1c0fc034b127174e5c5795347648db0629314262b9e59689705e887371a7e4e` |
| task186 fixture | 234 | `34dd389d9a3aff50486e57137f8dafea7b14825baec13e3288ed595046940963` |
| task193 producer | 37956 | `7ec85fe5b359a371e7c7c6b701426c5521d2a9651f560cba0193fa9c34aa2530` |
| task193 checker | 33149 | `278903c62c8f742cb985f44267f5f428c12dac9c514117f91eb6ae0daea17940` |
| task193 driver | 9799 | `4ad4231c7e1f10006bd27f4ff8877ebe7ed60dd44a97a6188392234ec0f548ec` |
| task197 contract | 8931 | `f4cbaa9f84b3b50f24902e8d37bcac56043f80b75a6ff0e26f234f569e612b5f` |
| proof v188 | 11314 | `6512e810011105f83f845e9a41f63ee51fe278371f2cee6cc241e8022a41e822` |

The final task192 STABLE repin changed only the task192 checker and driver
rows in both adapter pin tables, then resealed the task197 producer/checker
entries in the GAP driver. The task192 producer and fixture remained
unchanged. Static exact-text comparison found the producer/checker imported
pin tables identical and no occurrence of either superseded task192 pin in
the five authorized files.

After task192 SELFTEST run `33126747887` stopped at a historical task186
reply pin, task192 refreshed only that driver history row.  This adapter
therefore refreshed only its task192 driver pin and the resulting task197
producer/checker/driver identities.  No adapter semantics or fixture changed,
and that stopped task192 run supplied no mathematical result.

The driver has no self-pin. Its task197 producer/checker/fixture pins are
the first three entries on line 54.

## 3. Production input authentication

Producer lines 258--278 require a valid v3 outer seal, exact positive
schema/status/terminal, absent positive checkpoint, registered
exactification source, typed `c_exact`/exponents/A/B, independently digested
direct and star rows, their exact equality, a nonempty corrected word, and
all four direct replay flags. Forbidden fake/cofinal/Ihara claim fields are
accepted only with explicitly harmless false, null, empty-string, empty-list,
or empty-object values (lines 247--255).

The artifact object has an exact eight-key set. Producer lines 223--244 bind
run id, head SHA, artifact id/name, ZIP SHA-256, the fixed member name, member
bytes, and member SHA-256 to the actual canonical v3 bytes. Checker lines
295--305 independently enforce the exact types and byte/hash binding;
notably, `True` cannot substitute for an integer byte count.

Every supplied path is fail-closed. The only external production input must
be the original canonical string under `ci/in/task197/`; producer lines
177--189 and checker lines 185--196 reject absolute paths, backslashes,
normalization changes, empty/dot/dot-dot segments, traversal substrings,
metacharacters, glob characters, whitespace, `ci/out`, and resolved symlink
escape. Every other supplied path must equal its fixed repository-relative
task197 path exactly (producer lines 192--198; checker lines 199--205).
Driver lines 48--65 independently apply the same lexical input/scalar policy
before writing shell text, and quote every shell-reached binding.

In the authorized production chain, a stale v3 attestation cannot reach
PREPARE: driver lines 67--68 reject the attestation and every intermediate,
log, shell, and sentinel if already present. Driver lines 78--79 verify the
bound v3 bytes/SHA before and after the pinned full v3 checker, require its
single exact line, and only then create the attestation. PREPARE binds those
attestation bytes and their SHA (producer lines 362--384). FINALIZE rereads
the same exact line and verifies it against the sealed prepared record
(producer lines 433--442). This freshness statement is about the mandated
driver protocol, not an assertion that a context-free fixed marker alone is
cryptographic proof of when it was written.

Malformed, resource-only, SELFTEST-substituted, wrong-word, wrong-artifact,
or mismatched input reaches no task197 pass marker. Production exceptions
emit `UNKNOWN_INPUT`; the driver's exact-one pass-marker gates then stop the
shell before the sentinel.

## 4. Lossless compatibility conversion

PREPARE authenticates all source pins and input identities, performs the
deep-copy conversion, writes canonical v2 bytes, and writes a sealed prepared
record with exact keyset, artifact, input, attestation, diff, and output
identity (producer lines 362--398). FINALIZE reauthenticates the current v3,
v2, prepared record, artifact, and both exact attestation files before it
constructs the certificate (lines 433--462). The producer never emits the
production v2 checker line; driver line 81 obtains it from the pinned full v2
checker first.

The certificate has an exact keyset (producer lines 97--104 and 416), exact
source table, artifact block, v3/v2 path/bytes/SHA/self-digest identities,
both attestation paths/bytes hashes, the complete three-field recursive diff,
the exact consumed-field ledger, corrected-word/`c_exact`/direct-row equality,
and positive checkpoint absence (lines 419--430). `strict_equal` at lines
148--155 is recursive and type-aware, so bool/int or analogous JSON type
coercion is not equality. The complete diff is stronger than free-word
equality: even a freely equivalent but differently encoded word is rejected.

## 5. Independent checker

The checker imports no adapter producer module and no producer seal, diff,
path, or canonicalization helper. Its imports are only standard-library
modules (checker lines 1--10). It separately implements canonical bytes and
seal validation (lines 108--170), strict recursive type-aware equality
(148--155), path policy (181--205), source authentication (213--219), and
recursive diff (233--251).

Checker lines 262--340 independently enforce the two positive envelopes,
complete three-field diff, every consumed value, exactification/direct-row
semantics, exact artifact types and identities, certificate keysets and seal,
source table, receipt identities, checker lines and attestation hashes, and
all equality ledgers. Production path binding and actual-file loading occur
at lines 308--351. It checks the conversion and the externally generated
attestations; the serial full v3/v2 checker executions in the driver remain
load-bearing and are not claimed to be reproduced by the adapter checker.

## 6. SELFTEST and mutations

The one-line fixture is semantic rather than a count-only manifest. It binds
the signed nonempty correction word `[1,-2,3]`, distinct nontrivial
`c_exact=[1,-2,4]`, nonempty two-entry sparse row with coefficient two,
selected column and solution coefficients, distinct direct corrected word,
all required replay flags, both schemas, the complete three-difference path
list, and mutation count 55.

Producer SELFTEST constructs a full sealed toy independently of the fixture,
then executes the real `prepare(...)` followed by real `finalize(...)`
(producer lines 587--611). Only the two external mathematical checker lines
are explicit, distinct, typed SELFTEST placeholders. The driver then invokes
the real helper-nonshared adapter checker (driver lines 75--76). That checker
independently reconstructs the complete toy v3 object (checker lines
354--405), rereads the producer-created v3/v2/certificate through the same
production-shaped validator (471--498), and compares the entire derived
fixture semantics.

Producer lines 75--93 and checker lines 74--92 register the same ordered set
of exactly 55 unique mutations. Static enumeration found no duplicate,
missing, extra, minimum-count, `continue`, or unknown-name acceptance path.
Every ordinary envelope/certificate mutation changes an existing value and
is resealed before reaching the live validator; the two self-digest mutations
and two raw-attestation mutations are intentionally left invalid at their
respective authentication gates. Stale-output, SELFTEST-as-production, six
unsafe external paths, and internal-path substitution reach their actual
path/staleness gates. All other names must enter an explicit mutation branch
or raise `unregistered mutation` (producer lines 533--640; checker lines
408--526). Runtime rejection of the 55 cases is not claimed here because
execution was prohibited.

## 7. Driver and production handoff

The GAP path gate uses valid `PositionSublist` calls (driver line 51), and the
driver is ASCII-only. The source pin loop precedes all runtime work (lines
54--55), and the full stale set is rejected before shell creation (67--68).
Every producer/checker log must contain exactly one exact marker.

The production order is fixed at driver lines 78--84:

```text
bound v3 bytes/SHA
-> pinned full v3 checker
-> same v3 bytes/SHA again
-> fresh exact v3 attestation
-> PREPARE
-> capture v2 bytes/SHA
-> pinned full v2 checker
-> same v2 bytes/SHA again
-> fresh exact v2 attestation
-> FINALIZE
-> independent adapter checker
-> exact producer/checker terminal equality.
```

Only after all those gates does line 86 write and reread the nonempty
sentinel; lines 87--89 require it before the GAP pass marker. The emitted v2
receipt and v2 attestation paths are exactly the pair expected by task193's
existing `--task186-receipt` and `--task186-attestation` interface.

Conservative GHA estimate: SELFTEST should be budgeted at 2--10 minutes with
low memory, but this is unmeasured. PRODUCTION is uncalibrated and is
dominated by serial full task192-v3 and task186-v2 checker replays; budget the
full 360-minute job ceiling and approximately 6 GiB RSS. Any time or memory
cap is a non-pass, not evidence of impossibility. Adapter conversion itself
is linear in receipt bytes but holds several canonical/deep-copy values.

STATIC VERDICT: GO to parent-controlled GHA SELFTEST and, only after that
passes, parent-controlled PRODUCTION. This is not a runtime pass, a
cross-checked mathematical result, or a fake/Ihara/cofinal claim.

TASK192-v3 POSITIVE INPUT:                    REQUIRED / NOT YET SUPPLIED
LOSSLESS v3 -> v2 COMPATIBILITY ADAPTER:      NOT EXECUTED BY LUNA
FULL v3 CHECKER ATTESTATION:                  NOT EXECUTED BY LUNA
FULL v2 CHECKER ATTESTATION:                  NOT EXECUTED BY LUNA
TASK193-COMPATIBLE RECEIPT:                   NOT PRODUCED BY LUNA
ACTUAL TASK193 beta1 / FIRST MULTIPLIER:       NOT EXECUTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:       NOT DECLARED
