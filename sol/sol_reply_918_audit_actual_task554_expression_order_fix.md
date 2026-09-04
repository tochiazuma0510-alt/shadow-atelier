# Task918 narrow audit -- Task554 expression-order fix

## Ruling

PASS.  Task917 makes the actual Task554 expression contract agree with the
authenticated source while preserving its authentication, arithmetic,
resource, workflow, and claim boundaries.

## 1. Diagnostic and expression contract

Run `33902091912/1` (job `101118303556`) reached the actual producer and
failed after 23 seconds with `task554_seed:entry`; diagnostic artifact
`9948055636` has digest
`sha256:e80610fae8319434448f9f4ea02f1c0099f059517c5dd481dd48d7a3a686b1d8`.
The inspected pinned prepare data explains that failure: for example,
character-0 seed 3 is `[[2,2],[0,1]]`.  The reported unsorted counts are
`32/176` seed expressions, `8015/8056` actor transitions, and `1955/2014`
DAG reductions, with no duplicate indices.  Thus increasing-index order was
not an actual parent invariant.

Producer `_expression` and checker `_expr` now impose the same correct
contract.  The value must be a list; each term must be a two-element list;
both entries must be plain integers (booleans excluded); the index must obey
`0 <= index < bound`; the coefficient must be in `{1,2}`; and a local `seen`
set rejects repeated indices.  Neither validator sorts or rewrites the list.
The offset helpers preserve list order, and both production subtraction
loops iterate the authenticated expression directly.  Therefore insertion
order is accepted and retained even though the resulting mod-3 scalar sum is
commutative.

Root additionally reported a bounded direct pass of the exact 15.4 MB pinned
prepare through both repaired validators (`old_blocks=4`, `origins=8232`).
Per Task918 scope, I did not reopen or run that actual body.

## 2. Authentication boundary

Both executables still fix the same five `TASK554_BODY_DIGESTS` and exact
Task554 run/attempt/head plus five artifact id/name/byte/digest receipts.
For every state, the body filename and descriptor digest must equal the
corresponding fixed digest.  `read_json_stream` hashes and size-checks the
file before JSON interpretation; the HEAD is separately authenticated and
must name the same body digest and prepare-parent join.  Only after those
checks does the expression validator run.  Reordering a source expression
therefore changes the authenticated body bytes and is rejected at the fixed
receipt boundary; relaxing the syntax-order condition does not relax source
identity.

The fixed relation-source construction remains unchanged and binds the five
ordered body digests, ranks, offsets, actor order, and counts.  Its established
digest remains
`47effc68794b6d5d9616d5378396a7f10a5d9e0412bfe2ccf95c7e67b1fcf8dc`.

## 3. Executed bounded controls and retained gates

Each public selftest executes acceptance of the actual-style unsorted unique
expression `[[2,2],[0,1]]`, then requires rejection of a duplicate index, an
index equal to the bound, and coefficient zero.  Each also authenticates an
exact canonical temporary body, rewrites only the order of its same valid
terms without changing byte length, and requires the production
`read_json_stream` digest check to reject it before setting
`task554_relation_order_mutation_rejected=true`.  These are executed
positive and negative controls, not literal telemetry.

Source review finds no change to the accepted subtraction formula, relation
source receipt, seed/actor traversal, vectorized P1 path, one cache pass, or
prepare-plus-one-current-block residency.  Exact parents, complete checker
output equality, launch-SHA handoff, workflow pins and 90/40/40-minute caps
remain present.  The workflow is byte-identical to the prior accepted
version.  Claims remain root-batch candidate only, incomplete dual orbits,
Grade2 undecided, no A0/COMMON/cofinal/fake/Ihara declaration, and
`verified=false`.

## 4. Commands and receipts

No actual large body, parent, download, GHA, or git command was run.  A
unique directory under `%TEMP%` was used as `PYTHONPYCACHEPREFIX`.

```text
python -m py_compile search/d972_r07_actual_grade2_root_scalar_batch_v1.py search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py
exit=0  elapsed=1.547 s

python -u search/d972_r07_actual_grade2_root_scalar_batch_v1.py --selftest
exit=0  status=PASS  task554_relation_order_mutation_rejected=true  elapsed=11.308 s

python -u search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py --selftest
exit=0  status=PASS  task554_relation_order_mutation_rejected=true  elapsed=5.009 s
```

Raw-byte LF counts and SHA-256 receipts:

| file | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_actual_grade2_root_scalar_batch_v1.py` | 80161 | 1386 | `ee5ba55668642caf4e77ae02a048745e627776ad60529aafa6adc9bda460f1d7` |
| `search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py` | 83273 | 1347 | `b859e7acaee61490bf27deb49143dbbe66f3f524e628ff876a939c145480b500` |
| `.github/workflows/d972-r07-actual-grade2-root-scalar-batch-v1.yml` | 23735 | 433 | `cfa9814863e2c61db3158b5940854b72e9c0cd0bbd4b0ab53ea4a29fa7a238c3` |
| `sol/luna_reply_908_r07_actual_root_scalar_batch_v1.md` | 5287 | 62 | `52b62927f33b0a182d16328137201ad790909de8b54a47099ea20444315bd10f` |

VERDICT=PASS
SAFE_TO_PUSH_TRIGGER_GHA=yes
