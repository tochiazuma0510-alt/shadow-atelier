# Luna Task917 -- accept authenticated unsorted Task554 expressions

GHA run `33902091912/1`, job `101118303556`, reached the actual producer and
failed after 23 seconds with `task554_seed:entry`.  The diagnostic artifact is
`9948055636`, digest
`sha256:e80610fae8319434448f9f4ea02f1c0099f059517c5dd481dd48d7a3a686b1d8`.

Root inspected the exact pinned Task554 prepare body.  Its reduction terms
are unique and in range but preserve pivot/insertion order, not increasing
index order.  For example character 0 seed 3 is `[[2,2],[0,1]]`.  Counts of
unsorted expressions are `32/176` seeds, `8015/8056` actor transitions and
`1955/2014` DAG reductions, with no duplicate indices.

Modify only the two Task908 executables and its Luna reply.  In both
expression validators:

- require a list of `[index, coefficient]` pairs;
- require integer index in range and coefficient in `{1,2}`;
- require indices to be unique;
- do not sort or alter input order and do not require increasing indices.

The arithmetic sum is order-independent, while the already authenticated
exact Task554 body SHA fixes the source order.  Replace the incorrect
`_expression` reversed-order rejection selftest by: acceptance of a valid
unsorted expression; rejection of a duplicate index, out-of-range index and
bad coefficient; and a separate exact-body/receipt-digest test showing that
an order mutation is rejected by the authentication boundary.  Preserve the
accepted scalar formula, relation-source digest, workflow, parents, memory
form and claim boundary.

Run `py_compile` and both bounded public selftests, update exact receipts and
end the Task908 reply with `READY_FOR_SOL_REAUDIT=yes`.  Do not run actual
parents, GHA or git.
