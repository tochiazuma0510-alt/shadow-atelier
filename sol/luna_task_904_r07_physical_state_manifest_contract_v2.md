# Luna Task904 -- exact rho2-v17 manifest contract repair and live workflow v2

You are Luna.  This is the smallest implementation repair after GHA run
`33889253581/1` built the complete 1,354-row state and then rejected only at
`rho2_manifest_shape`.  Read AGENTS.md, Tasks899/900/902/903 and their
replies, the accepted flat-stager v4, the v1 producer/checker/workflow, and
`ops/express/20260904_fable_sol_grade2_run1_rho2_manifest_shape.md` completely.
Do not broaden the mathematics, add a solver, reuse the failed live state, or
change an accepted old file.

Create only these new files:

1. `search/d972_r07_grade2_physical_state_separator_v2.py`;
2. `search/check_d972_r07_grade2_physical_state_separator_v2.py`;
3. `.github/workflows/d972-r07-grade2-physical-state-separator-v2.yml`;
4. `sol/luna_reply_904_r07_physical_state_manifest_contract_v2.md`.

## Exact failure and immutable live object

Run `33889253581/1`, job `101076608011`, commit
`1a7bbdeb5be0b5c80fcf9bec2c72940d972f186a`, exited 1 after 82 seconds with
exact producer terminal
`{"status":"REJECTED","error":"rho2_manifest_shape","verified":false}`.
Its unchecked artifact is id `9943198098`, name
`d972-r07-grade2-physical-state-separator-v1-candidate-unchecked-33889253581-1`,
bytes `106041813`, digest
`sha256:4b9b6cc4581b7f222dcd4783593b3d5eab1c558c2088315831a4d08b92002f87`.
This is a wiring failure, not MEMBER/NONMEMBER.

The exact accepted rho2-v17 manifest remains 26,047 bytes with SHA-256
`55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488`.
Root independently expanded that exact artifact under the temporary read-only
path
`C:/Users/81905/AppData/Local/Temp/shadow-atelier-rho2-run33839962829/task640-payload/manifest.json`.
Do not copy it into the repository.  Its relevant actual contract is:

- top-level `schema`, `marker`, `dimensions`, `lower_all_zero`, `rho2`, and
  `files` (plus claim/provenance fields authenticated by the whole-file
  receipt);
- `dimensions == {"lower":32260,"packed_rho2":12096,"top":48384}`;
- `lower_all_zero is true`;
- `rho2.packed_sha256 == b41b9e69...17c2e`,
  `rho2.dense_sha256 == abfafbc7...752e`, and
  `rho2.packing_roundtrip is true`;
- `files` is a dictionary keyed by the seven roles
  `lower_dense,path_signatures,rho2_dense,rho2_packed,roots,signature_buckets,target_dense`;
  every value is the exact existing `{bytes,file,sha256}` receipt.  It is not
  the old list fixture and the three hashes are not top-level fields.

## Required producer/checker delta

Copy v1 to versioned v2, then change only the target-manifest reader and the
corresponding fixtures/mutation controls:

1. On the live path, authenticate manifest bytes/size/SHA before interpreting
   fields.  Parse the actual dictionary contract above.  Normalize the seven
   role receipts by their `file` values only after proving dictionary shape,
   and compare them to the already frozen `RHO2_PAYLOAD_RECEIPTS` exactly.
2. Check dimensions, `lower_all_zero`, packing round-trip and nested rho2
   packed/dense hashes.  Continue to check every payload receipt, exact roster,
   verdict, acquisition, packed/dense equality and all-zero lower bytes.
3. Producer and independent checker must implement the same external
   contract independently; do not share a new parser/helper.
4. Replace the synthetic old-list target fixtures with production-shaped
   dictionary fixtures.  Add a named regression control proving the exact old
   v1 list/top-level-hash shape is rejected and a production-shaped fixture is
   accepted by both sides.  Retain MEMBER, Separator, nonmonotone-pivot,
   stop/resume and all prior mutation controls.
5. Do not change physical elimination, insertion order, reverse substitution,
   state/output schemas, live-parent/final-artifact identities, caps, or claim
   boundaries.

## Workflow v2

Copy accepted workflow v1 to a versioned v2 which authenticates the new v2
producer/checker exact receipts and invokes only them.  Keep all external
parent tuples, stager v4, fresh `resume=false` roots, 1-second completion
polling / approximately-60-second progress, caps 30/30/75, uploads and gates
unchanged.  Give every workflow/artifact/schema label which names this runner
version a consistent v2 label.  Use exactly one new inert marker:

`[task904-r07-physical-state-separator-v2]`.

Run YAML/static checks, py_compile, both selftests and the bounded benchmark
only.  Report exact receipts and the semantic diff.  End with

`R07_PHYSICAL_STATE_MANIFEST_CONTRACT_V2_READY_FOR_SOL_AUDIT`

or the first honest blocker.  Do not use Git, credentials, GHA, or claim an
actual grade-two result.
