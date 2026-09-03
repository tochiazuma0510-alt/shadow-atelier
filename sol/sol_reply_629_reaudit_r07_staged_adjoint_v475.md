# Sol(max) Task629 reply: finite re-audit of staged-adjoint v475

## Verdict

`PASS`.

V475 applies both Task628 repairs exactly and introduces no mathematical or
claim-boundary regression.  No remaining finite defect was found.

This is a paper/static verdict only.  It is not an actual Task625 acceptance,
selected payload, residual, grade decision, or numerator.  No implementation,
production/GHA, or git operation was performed.  `verified=false`.

## Input binding

| input | bytes | SHA-256 |
|---|---:|---|
| Task629 | 783 | `c9fda0ba0be81ddc34c02ca59b10ba02096ba312b068b81b34304149a7b64165` |
| repaired v475 | 8,253 | `757ffab5aa011643efa3df4b133dc03d423895d57a003ed6830a47528388148e` |
| Task628 reply | 9,721 | `09c2d5defc272ddd18e0e300879e6860ba7ffd8e876ecc81adc26b7d20ab126a` |

Both requested inputs were read completely.

## Repair re-audit

### 1. Stable serialization: PASS

The complete v475 byte stream has:

```text
embedded CR bytes             0
other forbidden control bytes 0
UTF-8 replacement characters  0
```

Both the definition and formula (5.1) now contain the stable literal
`E_{\mathrm{reached}}`; the former `E_{<CR>m reached}` corruption is absent.
The accompanying TeX-delimiter cleanup restores notation without changing
the theorem.

### 2. Multiplicity definition: PASS

Section 5 now defines `E_{\mathrm{reached}}` as the number of processed
pairs

```text
(nonzero accumulated state, outgoing constructor edge),
```

explicitly counted with multiplicity over states, and immediately says that
it is not the number of distinct constructor edges.  Thus a node supporting
`r` exact paths and having `d` outgoing edges contributes `r*d` traversals,
as required.  Formula (5.1)

```text
sum_v |supp(A_v)| + E_reached
```

therefore counts the one-time nonzero state expansions and all resulting
edge updates; it no longer admits the undercount identified in Task628.

Exact-word construction/serialization, dictionary storage, resident memory,
path length, live entries and durable bytes are expressly governed by
separate telemetry and caps.  V475 still calls the bound result-dependent,
states that it need not be uniformly small, maps every exhausted cap to
`UNKNOWN_RESOURCE`, and forbids accepting a partial leaf map.  It therefore
does not turn the staged schedule into a uniform runtime or memory claim.

## Unchanged theorem and claim boundary

The load-bearing parts accepted in Task628 remain unchanged:

- the complete `G`, `L`, `B`, `D`, `O`, leaf dependency order;
- decreasing within-stage pivot order and explicit receipt checks for strict
  actor-parent and reduction arrows;
- accumulation of the complete `F3` coefficient at each exact
  `(node, freely-reduced path)` before its sole expansion;
- exact left-to-right `red(Pq)` multiplication and injective word interning;
- prohibition on quotient endpoints, signatures, hashes, or transient IDs as
  word equality; and
- independent producer/checker schedulers and complete compact-leaf stream
  comparison.

The only substantive section-5 additions implement Task628's requested
definition and make its resource accounting more explicit.  The status change
from candidate to `PAPER-CLOSED (TASK628 REPAIR APPLIED)` is justified by the
Task628 mathematical PASS plus these now-completed finite repairs.  It is not
an empirical promotion: v475 continues to state that run `33723160379` ended
`UNKNOWN_RESOURCE:time`, the actual selected payload and fresh residual were
not produced, and no grade was decided.

The final boundary continues to make no A0, COMMON, cofinal, fake, or Ihara
claim and expressly retains `verified=false`.

## Final status

```text
TASK628 SERIALIZATION REPAIR:            PASS
TASK628 STATE-EDGE MULTIPLICITY REPAIR:  PASS
STAGED-ADJOINT PAPER THEOREM:            PASS
ACTUAL TASK625 / SELECTED PAYLOAD:       NOT ACCEPTED HERE
GRADE / A0 / COMMON / COFINAL / FAKE:   NOT DECLARED
IHARA:                                   NOT DECLARED
verified:                                false
OVERALL:                                 PASS
```

`R07_STAGED_ADJOINT_V475_REAUDIT_PASS`
