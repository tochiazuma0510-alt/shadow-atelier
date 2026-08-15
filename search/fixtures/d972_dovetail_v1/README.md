# D972 dovetail checker fixtures

These fixtures belong to the independent checker, not to the producer or GAP
worker. Run them with:

```powershell
python search/check_d972_dovetail_v1.py --self-test
```

`negative_witness_mutations.json` corrupts one lossless witness field at a
time: factor map, kernel order, braid claim, full-B3 word-level mode,
settlement, the canonical `m` modulus, a fiber source row, and an extension
relator. The checker must reject every mutation.

`negative_state_mutations.json` covers a wrong parent hash, a sequence gap,
and duplicate semantic keys after replay. `intentional_interrupt_resume.json`
specifies the positive hash-transition invariant: the sequence advances by
exactly one, the parent is the prior checkpoint, the agreed cursor is
preserved, and no semantic key is lost or duplicated. The workflow restore
itself is tested separately by executing its preparation program twice with
three nonempty bound ledgers and requiring byte-identical restoration.

The synthetic positive candidate exercises serialization and the exact fiber
recount only. It is explicitly labelled `PARSE_ONLY_FIXTURE`; campaign rows
additionally require the isolated GAP reconstruction of the full extension,
the canonical D972 marking, the complete charming/full-hexagon loop, exact
surjectivity and synchronized finite Cayley/Schreier settlement, followed by
an independent normal-form fiber and zero-set comparison. The generated GAP
program reads neither the campaign producer nor its worker.
