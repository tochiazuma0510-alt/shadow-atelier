# Sol(max) task 507 - audit rank99 nonzero-constant literal prefix v431

Role: independent Sol(max) mathematical auditor.  Audit only paper v431 as
the proof premise of Task506.  Do not edit the paper or implementation, run
production/GHA/git, or design a broader selector.  Write only
`sol/sol_reply_507_audit_r07_rank99_nonzero_constant_global_prefix_v431.md`.

Frozen subject:

```text
sol/proof_r07_rank99_tau_free_nonzero_constant_global_prefix_v431.md
  9592 7b08f2526b00f4b12e67b9de57e03b7e87936050bfe8c3f9200130ed1ef850a4
```

Read v143, v414, v426, v427 and the exact audited rank99-v5 producer/checker
call sites needed for the ruling.  Do not trust v431's prose.

Independently decide all of the following:

1. On the reached tau-free coordinates-0--2 branch, the compiled formula is
   exactly `K + sum c_(j,t) 1[pi_j=t]`, merged support has union size at most
   `W=sum |ker pi_j|=9|R|`, and any `W+1` distinct Delta elements contain an
   outside point with value `K != 0`.
2. The `(qid,gid)=divmod(cursor,243)` roster order and literal word
   `Gamma.section_word(gid)+Q0.section_word(qid)` are the frozen task176/v143
   order, contain distinct elements, and direct word evaluation really yields
   all ten coordinates without the seven omitted Q0 stores.  Confirm that the
   inherited `sf.global_candidate` would be mistyped in the three-store
   runtime and must not be used.
3. Nonzero pairing proves a rank rise only at a fresh anchor.  Check that
   closing pre-existing rows before the scan and closing the guaranteed row as
   a one-row v427 batch is sufficient, preserves printed seed/action order,
   and cannot loop without either a rank rise, COMMON, or a typed resource
   stop.
4. The disjoint cursor
   `["global_nonzero_constant",seed,cursor,W]` carries enough information for
   independent reconstruction and cannot be confused with the old integer-
   first support cursor.
5. The proposed v5-to-v6 checkpoint migration is mathematically lossless:
   exact v5 validation precedes migration; changing only top schema/binding/
   seal leaves historical rows, segment identities, prefix and ledger valid;
   the actual v5 file can be the next v6 segment input without reopening an
   ancestor.  Identify any additional field that must be rebound, if one
   exists.
6. No claimed conclusion exceeds positive discovery: a partial prefix or
   resource stop remains nonnegative, and A0 stays 0/1 until final independent
   literal replay.

Use bounded static/source reconstruction only.  Return
`GO_FOR_IMPLEMENTATION` if the theorem and exact contract are sound.  Else
return `STOP` with the smallest false statement and minimal paper/Task506
repair.  End with exactly one of:

`TASK507_R07_RANK99_NONZERO_CONSTANT_GLOBAL_PREFIX_V431_AUDIT_GO`

or

`TASK507_R07_RANK99_NONZERO_CONSTANT_GLOBAL_PREFIX_V431_AUDIT_STOP`
