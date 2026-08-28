# Luna reply 283 - task198 independent embed bridge and producer capture v1

Commission processed as bounded mechanical implementation.  Only the
authorized task198 checker, GAP driver, and this reply were changed.  The
producer, fixture, predecessors, proofs, ledgers, workflow, and all other
files were left untouched.

## 1. Independent F2-to-PB3 bridge repair

The checker now pins
`search/check_d972_b345_seedspan_triple4_v1.py` at 574347 bytes and SHA-256
`ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981`.
It is present in both checker `PINS` and the normalized, path-sorted
`DEPENDENCY_CONE`.  The checker and driver cones each have exactly 44 unique
rows and their ordered path lists agree.

The unchanged producer receipt still carries its original 43-member
predecessor cone and source map.  The checker authenticates the new
44-member checker cone first, then constructs an exact checker-owned
projection of the unchanged 43-member producer source contract for receipt
and checkpoint comparisons.  This adds authentication without weakening or
retroactively changing producer-owned receipt predicates.

`load_arithmetic_bridge` loads two distinct fresh module objects and requires
their names and callable surfaces:

- producer arithmetic: `reconstruct_quotients`, `cheap_context_registry`,
  `embed_f2_pb3`;
- independent checker arithmetic: `embed_f2`, `reduce_word`, `inv_word`,
  `commutator`.

Both maps must agree on the fixed signed nonpalindromic probe
`[1,-2,1,2]`.  This is only an orientation/type canary; no reconstruction,
6,441-row replay, alternate traversal, factor-order gate, bridge replay,
mutation, resource, checkpoint, or receipt predicate was replaced by it.

## 2. Complete old-module use audit in `reconstruct_roster`

The two module objects have disjoint load-bearing roles:

1. `old` is the producer-side arithmetic helper.  It is used for
   `old.reconstruct_quotients(q3)` and
   `old.cheap_context_registry(e4)`.  It is returned unchanged as
   `rebuilt["old"]`, so the later fine-deletion and task176 bridge replay
   remain in the existing producer arithmetic convention.
2. `checker_old` is the independently pinned checker helper.  It is passed to
   `independent.JointGroup(checker_old, e3, e4, contexts, words)` and
   `independent.factor_presentation(q3, checker_old)`.  It is not returned as
   `rebuilt["old"]` and is not used by the later producer-convention bridge.

Before those calls, the shared loader performs the distinct-object,
callable-surface, and fixed-probe checks.  The task157ee module itself is also
required to expose callable `JointGroup` and `factor_presentation` before the
large construction starts.

## 3. SELFTEST reachability

The existing checker SELFTEST now invokes the same bridge loader under fresh
SELFTEST-only module names immediately after full dependency authentication.
That canary checks object separation, callable availability, and the exact
`[1,-2,1,2]` equality.  The canary itself does not build Q0 or Gamma, does not
enumerate the 6,441 rows, and does not call SymPy.  The existing full toy
receipt, 44-mutation loop, verdict schema, and terminal text remain present.

## 4. `PRODUCER_CAPTURE` driver mode

The GAP driver accepts the third exact mode `PRODUCER_CAPTURE`.

- It applies the same production input pin, task176 manifest, and optional
  resume checkpoint/manifest-pair checks as `PRODUCTION`.
- It emits the exact existing production producer command with the same
  output paths and resource caps.
- It does not emit or launch the independent checker command in capture mode.
- It requires one vocabulary-valid producer terminal and separately requires
  exactly one producer-terminal-prefixed line.
- It requires a nonempty producer receipt, copies the exact captured token to
  the terminal file, writes the normal final sentinel, and permits driver
  success for `ROOF_BRIDGE_ISOMORPHISM`, `UNKNOWN_RESOURCE`, or
  `UNKNOWN_INPUT`.
- Its distinct final marker is
  `R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_GHA_DRIVER_PRODUCER_CAPTURE_PASS`
  with `mode=PRODUCER_CAPTURE terminal=<exact terminal>`.

The existing SELFTEST branch and the positive-only `PRODUCTION` final gate
remain separate.  Static byte inspection found zero non-ASCII bytes in the
driver.

## 5. Final identities

| File | Bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_seven_context_roof_presentation_v1.py` | 137169 | `6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c` |
| `crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py` | 157253 | `001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1` |
| `search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g` | 20541 | `6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068` |
| `search/certs/d972_r07_seven_context_roof_presentation_selftest_v1_20260828.json` | 1605 | `fb31f6a0be2f2f5b530c6fe99796476ea16edb72fe7ddc192323995f2ae55ce7` |
| `search/check_d972_b345_seedspan_triple4_v1.py` | 574347 | `ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981` |
| `sol/luna_reply_283_r07_task198_independent_embed_and_capture_v1.md` | 5856 | self-referential SHA-256 omitted as permitted |

The driver's checker pin was refreshed to the exact final checker identity
above.  Static audits only were performed: Python, Node, GAP, git, GHA, and
network execution are all `UNEXECUTED`.

TASK198 INDEPENDENT F2->PB3 HELPER:             REPAIRED STATICALLY
TASK198 PRODUCER CAPTURE MODE:                  IMPLEMENTED STATICALLY
FULL PRODUCER+INDEPENDENT CHECKER SELFTEST:     NOT EXECUTED BY LUNA
ACTUAL PRODUCER CAPTURE RERUN:                  NOT EXECUTED BY LUNA
ACTUAL INDEPENDENT PRODUCTION ACCEPTANCE:       NOT OBTAINED
A1 / ACTUAL K / COMPATIBLE LIFT / IHARA:        NOT DECLARED

`TASK283_TASK198_INDEPENDENT_EMBED_AND_CAPTURE_COMMISSIONED`
