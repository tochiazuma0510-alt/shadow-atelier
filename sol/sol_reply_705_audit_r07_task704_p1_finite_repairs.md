# Sol(max) Task705: Task704 finite P1 repair audit

## Verdict

`PASS_P1_FINITE_REPAIRS_SAFE_FOR_GHA_REPLAY`

`SAFE_TO_DISPATCH_GHA=yes`

`verified=false`

The two finite Task702 code/fixture blockers are closed on the exact frozen
candidate.  No 1.7-GiB all-five replay, production action, workflow action,
artifact download, git operation, or code change was performed.

## Audited receipts

| path | bytes | LF count | final LF | SHA-256 |
|---|---:|---:|---|---|
| `sol/sol_reply_702_audit_r07_task699_p1_structural_ingest.md` | `9478` | `142` | yes | `34ff2f6c79f79c4f08896c969951256ef83dc6aca6803481b00858f24100c93d` |
| `sol/luna_task_704_r07_p1_structural_finite_repairs.md` | `2476` | `27` | yes | `036530180aef5ae84b00913bfa9f2d0df1cb4d240fa01508012258851ce37934` |
| `sol/luna_reply_704_r07_p1_structural_finite_repairs.md` | `2286` | `56` | yes | `f352ead1f522d8e7142fcdcafb8c24085464edd3d6b36692deb4636f3e7db788` |
| `search/d972_r07_grade2_specific_owner_prejoin_v1.py` | `47995` | `545` | yes | `38fcbe3757d1b14fd19f4f557f763c1f5f6a2e8da47e0e061707cf28c5064d73` |
| `sol/sol_task_705_audit_r07_task704_p1_finite_repairs.txt` | `1859` | `9` | yes | `ee56eaf423451fa1a4226182c8deab1cc48e617adb2d7da244ae2e34925658bc` |

The candidate receipt exactly matches the Task705 frozen claim.

## F702-1: closed

The production `validate_block_semantics` now closes both Python bool/int
aliases:

- `_plain_int` excludes booleans (`:77`), and the DAG predicate applies it to
  both `pivot_leads[pivot]` and `node['lead']` before comparing them
  (`:399-402`).  Therefore `node['lead']=False` cannot alias declared lead
  zero.
- `downstream_claim_flags` must be a dictionary with exactly the
  `FALSE_CLAIMS` keys, and every required value must satisfy `is False`
  (`:379-385`).  Integer zero cannot alias JSON false, and extra or missing
  keys cannot pass.

These are not dead predicates or fixture substitutes.  `ingest_all_five`
calls this same helper at `:531`.  The live `block_fixture` mutation loop
adds `node_lead_bool` and `false_claim_ints` (`:440-455`); its rejection
wrapper recomputes the DAG digest and invokes the same helper, failing the
selftest if either mutation is accepted.  A bounded instrumented execution
observed the exact outcomes

```text
node_lead_bool   REJECT block_dag_node
false_claim_ints REJECT block_semantics
semantic_rejections=7
```

Thus both charged holes are closed in production code and reached by live
rejecting fixtures.

## F702-2: closed

The bounded fixture creates exactly a canonical HEAD, canonical body, and its
declared basis member (`:463-470`).  It calls `validate_block_envelope` once
with the matching fixture digest/parent and then rewrites a still-canonical
HEAD with the wrong parent and calls that same helper again (`:471-476`).
The bounded run observed canonical `ACCEPT` and wrong-parent
`REJECT block_envelope`, and the ordinary selftest reports
`envelope_accept=1` and `envelope_wrong_parent_rejections=1`.

This is the production helper used by `ingest_all_five`, not a copied
validator.  A static call census finds only its two five-argument fixture
calls at `:471/:474` and the three-argument production call at `:531`.
Consequently production takes the `None` defaults and derives the indexed
body digest from `PARENTS` and the fixed prepare-parent digest (`:411-412`);
neither value is supplied by fixture state, CLI input, or artifact data.
Canonical HEAD/body bytes, body SHA-256, and the exact three-file roster are
unconditional checks after those choices (`:413-417`).  The optional fixture
arguments override only the fixture's expected body digest and HEAD parent.
They do not parameterize the production basis pin: `scan_block_basis`
unconditionally compares against `BLOCK_BASIS_SHA[index]` at `:421`, and the
production path calls it immediately after the envelope and semantic gates
at `:531`.

Thus the fixture parameters do not weaken the production `PARENTS`, basis,
roster, or canonical-byte pins, and no fixture-only validator has entered the
production path.

## Bounded regression checks

Both permitted commands passed against the frozen source:

```text
python -m py_compile search/d972_r07_grade2_specific_owner_prejoin_v1.py
python -B search/d972_r07_grade2_specific_owner_prejoin_v1.py --selftest
status=PASS
block_fixture={semantic_rejections:7,row_rejections:3,cross_family_collision:1,
               envelope_accept:1,envelope_wrong_parent_rejections:1}
```

Static inspection found no repair-side arithmetic, ingestion-order, block
rank, production-root, basis-consumption, dense-family, or parallelism
change.  The file imports no concurrency package.  The added allocation is
only the bounded temporary three-file fixture.  The Task640/result-dependent
join remains `NOT_READY` at `:28-30` and `:544`; no Task640 or precision-two
work is entered.  No unrelated release blocker was found within Task705's
finite regression boundary.

## F702-3 and claim boundary

F702-3 is deliberately **not** closed by these bounded checks.  Structural
promotion still awaits a replacement actual all-five GHA replay whose
terminal is bound in its run receipt to the exact candidate code bytes,
namely `47995` bytes, `545` LF, and SHA-256
`38fcbe3757d1b14fd19f4f557f763c1f5f6a2e8da47e0e061707cf28c5064d73`.
After that, the later independent checker and semantic equality replay remain
separate required gates.  This verdict authorizes only dispatch of that
replacement replay; it does not promote the structural result and makes no
verified, precision-two, Task640, or mathematical equality claim.
