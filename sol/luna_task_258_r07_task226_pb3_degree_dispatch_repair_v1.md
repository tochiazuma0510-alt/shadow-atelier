# Luna task 258 — task226 PB3 degree-dispatch repair v1

Role: bounded implementation repair only.  Read task254 and all current five
task226 files in full.  Do not run Python, Node, GAP, git, GHA, or network.
Edit only those same five task226 files.

## Exact static rejection

The producer's public bracket lookup currently says

```python
if d == 1: return PB3_BRACKETS[...]
return PB4_BRACKETS[...]
```

but `d` is the noncentral degree and `class2_facts` / `cmul` call it with
`d=3` for PB3 and `d=6` for PB4.  Consequently every PB3 calculation selects
the PB4 table; the returned tuple even has length four where the PB3 central
width is one.  Task254's mod-9 normalization did not repair this dispatch.
The independent checker already dispatches PB3 on `d==3`.

## Required repair

1. Producer must select PB3 exactly for `d==3`, PB4 exactly for `d==6`, and
   reject every other degree.  Retain canonical `0..8` residue output.
2. Independently require in both producer and checker that the bracket tuple
   width is one for PB3 and four for PB4.  Exercise a positive and negative
   nonzero bracket in each table, including PB3 `(0,2)=8` and PB4
   `(0,3)=(8,0,0,0)`.  Keep every commutator/direct-roster assertion.
3. Do not alter multiplication, inverse, word, Fox, ABI, mutation, terminal,
   or conclusion semantics.
4. Refresh exact driver pins and reply identities; Linux digest pins remain
   lowercase.  Report `UNEXECUTED` and all five byte/SHA identities.

## Additional static audit before delivery

While reading the whole checker, parent found three more guaranteed SELFTEST
stops which must be repaired in this same bounded pass (semantics are retained;
only the owning gates are made executable):

1. Checker mutation expectations for `word_g0/word_a/word_f` are
   `mutation word`, but checker `validate` emits `word replay`.  Its
   `group_width` expectation is `mutation width`, but validation emits
   `widths`.  Make the checker use the same exact preregistered gate vocabulary
   as producer (or update its fixed expected table and fixture consistently),
   so an observed owner rejection is compared exactly and does not fail merely
   because of two names for the same gate.
2. Checker `independent_mutations` sets `pkg["fake"]=True` for
   `forbidden_conclusion`, but checker `validate` never inspects downstream
   flags; the mutation is therefore accepted.  Require every pkg flag
   `boundary_membership, pointed_mu1, exact_pb_endpoint_zero, cofinal_lift,
   fake, Ihara_witness` to be exactly false, with the preregistered forbidden-
   conclusion gate.
3. In the normal checker path also require the six corresponding top-level
   receipt flags to be exactly false.  UNKNOWN receipts remain nonaccepting;
   do not infer any later gate.

Keep mutations one-owner, non-vacuous, and fail-open on an accepted mutation.

Parent Sol will rerun GHA.  A2 remains 1/3 until producer and independent
checker SELFTEST both pass.
