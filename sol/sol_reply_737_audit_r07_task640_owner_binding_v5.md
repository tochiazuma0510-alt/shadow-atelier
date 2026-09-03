# Task737 audit -- Task640 owner binding v5

## Verdict

`PASS_WITH_FINITE_TEXT_REPAIR`

`OWNER_BINDING_V5_SAFE_FOR_GHA=yes`

The v5 executable repair is correct and is safe to bind into the GHA job.  The
finite text repair is only to this commission's input list: the two named
paths do not exist.  The unambiguous, previously accepted paths are

```text
search/d972_r07_task640_fresh_endpoint_independent_checker_v4.py
  -> search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py
search/d972_r07_grade2_explicit_v12f.py
  -> search/d972_r07_history_free_positive_fast_resume_v12f.py
```

The corrected names are fixed by Task735's commission and reply, v5's own
pin/path, and the accepted Task723 audit.  No producer, checker, arithmetic,
or workflow byte needs repair.  I used the corrected authorities below.

## 1. Mechanical v4 -> v5 proof

`git diff --no-index` reports exactly one hunk: one new comment and

```diff
-    q3_owner = validate_q3_literal_owner(q3)
+    q3_owner = module.validate_q3_literal_owner(q3)
```

Three independent finite comparisons agree:

- deleting the exact 73-byte comment line and replacing the sole qualified
  call by the old call makes the v5 bytes exactly equal to v4;
- after comments/newlines are removed by `tokenize`, the only token edit is
  insertion of `NAME module`, `OP .`;
- an AST transformer that unqualifies that one call performs exactly one
  rewrite and then gives an AST dump identical to v4.

The raw census is v4 `(qualified, unqualified)=(0,1)` and v5 `(1,0)`.  The
size delta is exactly 80 bytes: 73 bytes for the comment and 7 for `module.`.
Thus every other executable statement and assertion is byte-identical.

## 2. Exact module owner and contract

Production reaches the call only through

```text
main -> evaluate -> load_all_seven -> build_endpoint_minimal
```

`load_all_seven` first hashes
`search/d972_r07_history_free_positive_fast_resume_v12f.py` against the
literal v12f pin, imports that exact path under `task640_v12f`, constructs
`Meter` and `SourceRegistry` from that same module, and passes the same local
`module` object to `build_endpoint_minimal`.  The builder first calls
`registry.authenticate`, then obtains `q3` from that registry, and directly
calls `module.validate_q3_literal_owner(q3)`.  There is no reassignment,
unqualified call, copied validator, exception catch, or fallback.

The v12f bytes rehash to the embedded pin
`22d2ebda554cfacc78393dda7f43a9a6550e7f134dd8f44f87ab0f62241bbbbb`.
Its top-level export is unique and has exactly one required positional
parameter, no defaults, varargs, keyword-only arguments, or kwargs:

```text
def validate_q3_literal_owner(q3: dict[str, Any]) -> dict[str, Any]
dynamic callable: true
inspect.signature: (q3: 'dict[str, Any]') -> 'dict[str, Any]'
```

An import-only check under a non-main name confirmed the callable's module
and origin.  Independently, all 28 `SOURCE_PINS` snapshots authenticated via
that module's `SourceRegistry`; its Q3 receipt was 231,570 bytes with SHA-256
`3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`.
On Windows the import-only check supplied an inert in-memory `resource`
module because that POSIX module is unavailable; no resource function or
v12f main/runtime builder was executed.

## 3. Bounded compile and SELFTEST

With `PYTHONPYCACHEPREFIX` set to the fresh external directory
`C:\Users\81905\AppData\Local\Temp\shadow-atelier-task737-166f74310f8c45fd866b3074c7febbfa`:

```text
Python 3.13.14
python -m py_compile search/d972_r07_a0_fresh_precision2_endpoint_signature_v5.py
exit 0

python search/d972_r07_a0_fresh_precision2_endpoint_signature_v5.py --selftest
exit 0
```

The SELFTEST terminal was:

```json
{"actor_multiplication":"PASS","build_heavy_trap_called":false,"coefficient_2":"PASS","context_order":31,"endpoint_ceiling":484,"endpoint_fine_source_order":59049,"endpoint_installer":"PASS","first_six_shift_mutations":1,"fixture":"PASS","forbidden_runtime_rejections":1,"g760_length":760,"generic_builders_called":false,"inverse_action":"PASS","joint_equality_cases":14,"joint_mutation_rejections":2,"leaf_live_mutations":4,"occurrence_components":11,"q0_marked_rows":2,"rho2_bytes":12096,"runtime_profile_mutations":1,"seed_cache_bytes":10644832,"wrong_fine_order_rejected":1}
```

The AST local-call closure rooted at `selftest` has empty intersection with
`evaluate`, `load_all_seven`, `build_endpoint_minimal`, `load_kernel`, all
three real parent authenticators, and paper-pin authentication.  `main`
returns immediately after SELFTEST.  The deletion fixture uses `FakeP176` and
a one-entry dictionary; 59,049 is checked as a receipt value, not built.
The unchanged frozen profile enforces 31 contexts, 46 named uses, source
order 59,049, two Q0 rows, 760 g760 letters, 11 occurrence components, and
endpoint ceiling 484.  Its mutation and forbidden-runtime tests reject
widening.  No real endpoint or preregistered-universe extension ran.

## 4. Independent-checker protocol compatibility

Byte normalization in section 1 proves every protocol and mathematical byte
outside the corrected call is unchanged.  Direct comparison with accepted
checker v4 (93,236 bytes, 1,592 LF, SHA-256
`581f9a5a9aa65ae298bf6d6f785ed1063ddfb0caf8a0c06e15f30ec2e713fd6f`)
confirms:

- producer schema `d972.r07.a0.fresh-precision2-endpoint-signature.v4` and
  candidate marker `R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V4_CANDIDATE`;
- payload names `rho2.bin`, `rho2-dense.bin`, `lower-dense.bin`,
  `target-dense.bin`, `path-signatures.json`, `signature-buckets.json`, and
  `authenticated-roots.json`;
- checker marker `R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V4_CHECKER_PASS`
  and verdict schema
  `d972.r07.a0.fresh-precision2-endpoint-signature.v4.checker`, with the same
  manifest/rho2 hashes, checked coordinate counts, and false
  `cross_checked`/`verified` fields;
- dimensions `(lower,top,packed)=(32260,48384,12096)`, occurrence coordinates
  `(0,1,2,3,0,4,5,6,7,8,9)`, signs
  `(1,-1,1,-1,-1,1,1,1,1,-1,-1)`, all endpoint/direct-column/lower/rho2
  assertions, parent pins, caps, and all false downstream claim flags.

The existing checker is therefore still the exact consumer; no checker v5
or protocol migration is warranted.

## 5. Allocation, reconstruction, concurrency, and retry audit

There is exactly one new executable call target and no new loop, import,
container, branch, process/thread operation, retry, or alternate slow path.
The called v12f validator checks exactly two 36-point marked rows, constructs
two constant-size converted rows and one 36-entry product, and returns their
small receipt.  It has no concurrency, retry, boundary reconstruction, or
dense mathematical allocation.  v12f was already imported by v4; qualifying
the call adds no import.  The pre-existing quotient and single fine-deletion
construction remain unchanged and are outside this one-call delta.  No
performance or memory regression was found.

## 6. Receipts, commands, and limitations

Audited v5 exact receipt:

| file | bytes | LF | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v5.py` | 43,838 | 671 | yes | `2f8cb910c79cb6046c8cd7a83f77e9e883187fe81b43209e3a8d09679a12ad6b` |

Commands used were `git diff --no-index` (read-only), an inline `python -B -`
byte/token/AST/pin/import/registry audit, the isolated `py_compile`, the v5
`--selftest`, `rg`, `Get-Content`, and `Get-FileHash`.  No GHA, git mutation,
real parent, real 59,049 build, full checker run, output artifact, fresh rho2,
or Lean run was performed.  The workflow binding itself was not audited.

The exact receipt of this reply is emitted by the parent handoff after this
file is sealed.  Embedding the SHA-256 of the complete file in that same file
would be a self-referential fixed-point demand; an in-file value could not be
an honest post-seal digest.

```text
REAL_RUN=DEFERRED_TO_GHA
FRESH_RHO2=NOT_PRODUCED
cross_checked=false
verified=false
```
