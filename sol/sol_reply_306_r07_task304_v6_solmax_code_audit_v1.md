# Sol(max) reply 306 - task304/v6 adversarial static code audit

## Verdict

**REJECT (fail-closed static audit).**  The narrow v5 terminal-enum defect is
repaired, and most of the preserved algebraic SELFTEST structure is present.
However, the independent checker can count a no-op mutation or a failed
reseal as a successful semantic rejection, so its claimed 19/19 gate does not
prove the task304 contract.  The production driver also deterministically
fails on its unquoted, space-containing normalized terminal before terminal
equality and the final sentinel.

No Python, Node, GAP, GHA, network, or git command was run.  Neither SELFTEST
nor production was executed.  No implementation file was changed by this
audit.

## Audited identities

| task304 path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_joint_slice_kernel_general_v6.py` | 11668 | `b0e454fd80145789340258b6d1e555f7bd55f53ad438ad4c34a27d814396551b` |
| `crosscheck/check_d972_r07_joint_slice_kernel_general_v6.py` | 21514 | `dee5b4f43d435ff67166e62d9ecebd91a8883c6490007273b2e2a5f3ce6959f4` |
| `search/d972_r07_joint_slice_kernel_general_gha_driver_v6.g` | 4539 | `11d287701c49b89a742bc830f6a8475a1eaba030d0aef3015981cc34922af3f9` |
| `search/certs/d972_r07_joint_slice_kernel_general_selftest_v6_20260828.json` | 10315 | `4fedd381d527c34249972227b3f62936f9b7daeddf70516745d405ea443a3c46` |
| `sol/luna_reply_304_r07_task299_kernel_terminal_repair_v6.md` | 3504 | `7b4f9c90ab7972dc4e488961edfc4504973b614e1adfee19cd5fef65b65a8606` |

The three driver pins at
`search/d972_r07_joint_slice_kernel_general_gha_driver_v6.g:15` match the
current producer, checker, and fixture bytes/SHA.  The GAP driver contains no
non-ASCII byte.  In accordance with the no-git audit mandate, this is an audit
of the five named paths, not a repository-wide change-set attestation.

## Fatal findings

### F1 - checker mutation preconditions are swallowed as successful rejections

Task304 section 3 requires every checker mutation to prove a canonical change,
reseal the mutant, and then reach a semantic gate.  Those three outcomes must
not be interchangeable.

In `crosscheck/check_d972_r07_joint_slice_kernel_general_v6.py`, the `try`
starts at `:215` and encloses all of the following:

- fixture canonical-difference proof at `:228`;
- fixture reseal proof at `:229-230`;
- fixture semantic oracle at `:231`;
- receipt canonical-difference proof at `:242`;
- receipt reseal proof at `:243-245`; and
- receipt semantic replay at `:246`.

`require` raises `RuntimeError` (`:87-89`), while the common handler catches
that same exception and returns `True` (`:248-249`).  Consequently:

1. a no-op mutation makes `digest(mutant) != digest(baseline)` false and is
   reported as `rejected=True`;
2. a broken or absent reseal is likewise reported as `rejected=True`; and
3. only a semantic rejection should have earned that value, but the caller
   cannot distinguish the three paths.

The list comprehension at `:284` and `all(... is True)` at `:285` therefore
can attach a 19/19 summary even when a mutant never reaches its semantic gate.
This is exactly the class of non-noop/non-circular proof obligation imposed by
task304, although it is not the aggregate-counter circularity of task300.

The literal edits shipped in `:217-240` appear to change their currently
selected baseline objects.  That observation does not repair the harness:
the commissioned code must fail if the canonical-difference or reseal proof
fails, rather than convert that failure into the desired mutation verdict.
The difference/reseal assertions must be outside the exception region that
interprets semantic rejection (or return a structured stage/reason and require
the semantic stage explicitly).

By contrast, the producer gets this separation right: its canonical-change
and reseal assertions are outside the semantic `try`
(`search/d972_r07_joint_slice_kernel_general_v6.py:123-125`), only
`compile_case` is interpreted as the rejection oracle (`:126-127`), and every
individual Boolean verdict is required before the summary (`:139-144`).

### F2 - the production driver cannot reach terminal equality or its sentinel

The generated shell uses `set -euo pipefail`
(`search/d972_r07_joint_slice_kernel_general_gha_driver_v6.g:21`).  Its exact
production terminals contain spaces (`:34-35`):

```text
STATIC_BLOCKED:actual typed matrices are not staged
```

Line `:36` extracts that string and then emits:

```sh
test -n $D299Pterm
test -n $D299Cterm
```

Both expansions are unquoted.  Bash word-splits each terminal into multiple
arguments, so `test` reports an argument-count error.  Under `set -e`, the
script exits before the quoted equality test later on the same generated line
and before the only sentinel write at `:38`.  Thus the individually typed
producer/checker production envelopes do exist
(`search/d972_r07_joint_slice_kernel_general_v6.py:148-149` and
`crosscheck/check_d972_r07_joint_slice_kernel_general_v6.py:295-303`), but the
commissioned production driver contract is deterministically unattainable.

### F3 - the driver tests presence, not exactly one success terminal

Task304 section 4 requires one exact producer success terminal and one exact
checker success terminal.  The four checks at driver `:25`, `:28`, `:34`, and
`:35` run `grep -Fxc ... >/dev/null`.  `grep` exits successfully for any
positive match count; discarding its count does not require the count to equal
one.  An exact-one gate would test the emitted count against `1` (for example,
`grep -Fxc ... | grep -qx 1`).  The pinned programs appear to print one line on
their intended paths, but the driver itself does not enforce the stated
exact-one condition.

## Requirement-by-requirement audit

### 1. Scope and static production boundary - partial

- **PASS:** all five named v6 paths exist, identities are recorded above, and
  the GAP source is ASCII-only.
- **PASS in the producer/checker, REJECT in the driver:** production returns
  the same typed `STATIC_BLOCKED:actual typed matrices are not staged` value,
  but F2 prevents the production driver from completing its gates.

### 2. v5 terminal regression - PASS

The producer now requires the exact enum before Boolean conversion at
`search/d972_r07_joint_slice_kernel_general_v6.py:93`; the comparison occurs
only afterward at `:94`.  The terminal mutant writes `MUTATED` at `:121`, its
canonical change and reseal are checked at `:123-125`, and `compile_case` then
rejects it specifically at the enum gate.  This removes the task301/v5 path in
which every non-`MEMBER` string was treated as expected nonmembership.

The independent checker also enforces the case enum at
`crosscheck/check_d972_r07_joint_slice_kernel_general_v6.py:139` and `:208`,
and receipt/case/computed terminal equality at `:141`.  Its receipt terminal
mutant at `:240` reaches that equality gate for the current literal fixture;
F1 concerns whether the harness proves that route fail-closed.

### 3. Preserved kernel and replay contract - mostly PASS, mutation gate REJECT

- **Five cases and literal expectations:** fixture `:6-12` contains all five
  requested cases.  Static derivation from those literal matrices gives:

| case | closure rank | kernel dim `d` | full nonzero `3^d-1` | Hd1 rank | terminal |
|---|---:|---:|---:|---:|---|
| `nonzero-member` | 2 | 2 | 8 | 2 | `MEMBER` |
| `outside-nonmember` | 1 | 1 | 2 | 1 | `NONMEMBER` |
| `zero-member` | 1 | 1 | 2 | 0 | `MEMBER` |
| `zero-nonmember` | 1 | 0 | 0 | 0 | `NONMEMBER` |
| `post-c-cancel` | 2 | 1 | 2 | 1 | `MEMBER` |

  These are expectations only; they were not executed.

- **Plural seeds/actions:** fixture `:8` has seeds `[1,0]`, `[0,1]` and
  distinct named actions `m`, `n` with distinct matrices.  Producer queue
  closure is at `producer:81-90`; checker reconstructs in reverse action order
  at `checker:113-131`.  Both use the joint `(z,eta)` rank.
- **Post-`C` kernel:** producer applies `C` only after closure and computes the
  left kernel at `producer:90`; checker independently enumerates the full
  nonzero left-kernel roster after closure at `checker:130-134`.
- **`d` versus `3^d-1`:** producer emits the independent basis length and
  `3**len(nvec)-1` fields at `producer:100`.  Checker checks receipt-basis
  independence, the full enumerated roster, `len(kernel)+1 == 3**d`, and full
  spanning at `checker:157-164`, then reports `d` and roster cardinality
  separately at `:178`.  The dimension-two/eight and zero-dimensional/zero
  canaries are literal in fixture `:6`, `:8`, and `:11`.
- **Full replay:** receipt closure span equality and row ranks are checked at
  `checker:142-147`; typed rows plus seed/action ancestry at `:148-156`; kernel
  and Hd1 content at `:157-167`; MEMBER equations/ancestry at `:168-172`; and
  NONMEMBER dual existence and equations at `:173-177`.
- **Checker independence:** imports at `checker:3-8` are standard-library only;
  there is no producer import.  Its closure, rank, full-kernel enumeration,
  Hd1, membership, and dual code is local (`:26-85`, `:94-210`).
- **All `require` arguments:** **PASS.**  Producer `require` is `is not True`
  at `producer:54-55`, and checker has the same rule at `checker:87-89`.
  Every call site supplies an equality/inequality, membership comparison,
  `isinstance`, `all`/`any` Boolean (with explicit negation where needed), or
  explicit `bool(duals)`.  The v4 truthy-string seal defect is absent.
- **Wrong-seal canaries:** **PASS statically.**  Producer independently changes
  the literal fixture seal and requires rejection at `producer:130-133`.
  Checker separately does so at `checker:259-266`, after its ordinary fixture
  validation at `:251-257`.
- **Producer 19/19:** **PASS statically.**  The 19-owner roster is at
  `producer:14` and fixture `:14`; literal mutations are at `producer:101-122`.
  The owner gates are the field/binding/control checks at `:66-80`, target or
  dual terminal semantics at `:93-98`, and the new terminal enum at `:93`.
  Non-noop/reseal proofs and semantic exceptions are separated at `:123-127`,
  with per-owner verdicts before the summary at `:138-144`.
- **Independent checker 19/19:** **REJECT as a proof gate.**  The roster and
  owner-specific fixture/receipt mutations are present (`checker:16`,
  `:212-246`, `:283-286`), and current receipt gates cover ancestry, kernel,
  Hd1, MEMBER, dual, and terminal fields.  F1 nevertheless allows pre-semantic
  mutation failures to masquerade as those verdicts.

One non-load-bearing metadata inconsistency should also be corrected:
`producer_mutation_controls_ignored` is emitted as `True` at checker `:286`,
although producer controls are explicitly read and required at `:280-282`.
The checker does create a separate mutation suite, so this label does not
cause the rejection above, but it is factually inaccurate.

### 4. Driver - REJECT

- **PASS:** exact byte/SHA pins (`:15`), all six stale-output guards (`:19`),
  producer-before-checker sequencing (`:24-28`, `:31-32`), nonempty
  receipt/verdict/log checks (`:26`, `:29`, `:33`), and one statically unique
  sentinel write after the listed gates (`:38`).
- **PASS under the expressly allowed common-value alternative:** SELFTEST
  documents `SELFTEST_COMPLETE` as the common normalized value at `:23`, binds
  both names after the two success-marker checks, and compares them at `:29`.
- **REJECT:** exact-one success-marker enforcement is absent (F3).
- **REJECT:** production normalized equality and completion are unreachable
  because of the unquoted nonempty tests (F2).

### 5. Task304 reply - partial / overclaims rejected gates

`sol/luna_reply_304_r07_task299_kernel_terminal_repair_v6.md:9-14` reports the
four non-self identities correctly; `:45-52` reports all five expected tuples;
`:60-67` marks both mutation suites, wrong-seal canaries, and SELFTEST
`UNEXECUTED`; and `:69-70` correctly keeps actual A5/A6 at 0/3 with no lift,
fake, or Ihara declaration.

Its claims that checker canonical-difference/reseal checks support an
independent 19/19 gate (`:29-32`) and that the production driver successfully
compares normalized terminals (`:37-41`) are not justified because of F1 and
F2.  The reported results remain intentions marked `UNEXECUTED`, not accepted
SELFTEST evidence.

## Final accounting

```text
TASK304/V6 STATIC AUDIT:              REJECT
V5 TERMINAL-ENUM REGRESSION:          REPAIRED STATICALLY
PRODUCER MUTATION GATE:               19 OWNERS PRESENT; STATICALLY SOUND
INDEPENDENT CHECKER MUTATION GATE:    REJECT (PRE-SEMANTIC FAILURES COUNT TRUE)
SELFTEST EXECUTED / ACCEPTED:         NO / 0
PRODUCTION EXECUTED:                  NO
PRODUCTION DRIVER STATIC_BLOCKED GATE: REJECT (UNQUOTED TERMINAL)
ACTUAL A5:                            0/3
ACTUAL A6:                            0/3
LIFT / FAKE / IHARA RESULT:           NONE DECLARED
```

`TASK306_R07_TASK304_V6_SOLMAX_CODE_AUDIT_REJECT_UNEXECUTED`
