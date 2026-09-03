# Luna Task740 -- P1 equality literal-LF producer v5 / checker v3

Role declaration: Luna.  Implement only the finite literal repair proved in
v489.  Do not run the real five-artifact replay, create a workflow, use git, or
change any mathematics/resource architecture.  Reply only to the designated
file.

Read fully:

- `sol/proof_r07_p1_equality_literal_lf_repair_v489.md`
- `search/d972_r07_grade2_p1_componentwise_semantic_replay_v4.py`
- `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v2.py`
- `sol/sol_reply_726_audit_r07_p1_semantic_checker_v2.md`
- actual-failure facts in v489

Create only:

- `search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py`
- `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v3.py`
- `sol/luna_reply_740_r07_p1_equality_literal_lf_v5.md`

## Required repair

1. Copy producer v4 to v5.  Change only the four `record_sha256` literals to:

```text
5b3f5dfd965861f33ec9cb2c2ac2e7401629b73b3571491110d063f47398cb4f
75aa31bfcd4ec622ff985afb6e92bfa16707206508683b012eeb9be1ab2544a6
d732aa55163be06b50199d864761ec0f1eeb5f29fcea171d4e674616c40d7e75
ad89a5738a65e6b1340816534b4dca8b82d3127ae82765a718eec6f6a1025022
```

and `EQUALITY_SHA` to

```text
e04c0d8de2cfbd264d3c93d915dc19e613a001c5278c8efdb704f06d1abb3565
```

Version comments/names only where required.  Do not change lower/lifted pins,
canonical serialization, schemas, arithmetic, replay, resource caps, or flags.

2. Copy independent checker v2 to v3.  Change only its producer source path,
symbol names/comments as necessary, and literal producer SHA to the sealed v5
SHA.  Its independent equality calculation must remain unchanged and must not
learn the five corrected producer constants.

3. Add/retain a bounded fixture proving the corrected equality list passes and
that a backslash-`n` record hash is rejected.  If this can be done by extending
the producer SELFTEST without touching production logic, do so minimally.
Checker mutations and all nonimporting arithmetic must remain intact.

4. Mechanically compare AST/top-level functions.  Report every changed
executable node; reject scope creep.  Run py_compile and both bounded
selftests with cache outside the repository.  Do not replay the actual parents.

5. Report exact bytes/LF/final-LF/SHA256, commands and limitations.  State
`REAL_FIVE_ARTIFACT_REPLAY=DEFERRED_TO_GHA`, `verified=false`.

