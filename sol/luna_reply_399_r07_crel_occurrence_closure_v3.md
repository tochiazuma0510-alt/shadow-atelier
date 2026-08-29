# Luna reply 399 — r07 C_rel occurrence closure v3

## Result

Created the requested v3 producer, independent checker, GHA driver, and reply. Existing v2 files were not modified.

## Exact artifacts

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_crel_occurrence_closure_v3.py` | 26765 | `8d1ee5d06fd5dc760c2df1fa760cb64280903c2a10561b4340f93ed313deb817` |
| `crosscheck/check_d972_r07_crel_occurrence_closure_v3.py` | 35157 | `7409847c42581631495cadae549e7cff019d4f9e30c6398b679fb9e5e50b829c` |
| `search/d972_r07_crel_occurrence_closure_gha_driver_v3.g` | 7932 | `9395acdade96fca3bd70105e674b0f687c92d6900ae33d0fea8fdf3f72fa4eb1` |

The driver embeds the v3 producer/checker paths, output base, byte counts, and SHA-256 pins.

## F398-1 repair

- The checker reads the pinned task382 producer bytes into a separate minimal identity namespace and gates `frozen_identities` callable availability plus receipt equality before checker/physical restoration.
- The `restore_v14()` checker namespace remains the source of `CHECKER_BRIDGE_OWNER_LAYOUT`; the checker namespace remains separately retained for checker arithmetic/authority. The producer identity namespace is used only for `frozen_identities`.
- Missing identity owners are fatal (`UNKNOWN_INPUT`), never silently skipped.
- All v2 ancestry/replay fields, direct candidate replay, exact producer transcript comparison, rank-0 closure, reverse two-way span, and `complete:true`/UNKNOWN `complete:false` behavior are preserved.

## Checks

- AST parse and Python compile probes: passed for both v3 Python files.
- Minimal pinned producer identity restoration probe: passed; `frozen_identities()` callable and returned 9 entries.
- Deliberate identity-mismatch gate probe: passed; failed before `authenticate_physical_owners` was reached.
- GHA source pin/path consistency probe: passed.
- No production, SELFTEST, GHA dispatch, GAP, git, or network execution was performed.

## Claim boundary

The v3 artifact claims only computed `W_C` in raw occurrence space, with the stated closure and replay checks. It does not claim actual `L/[J,L]`, leading-onto, compatible lift, fake/Ihara witness, or Lean verification.
