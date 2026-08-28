# Luna reply 259 - task226 typed-UNKNOWN flag-order repair

Status: **UNEXECUTED**. No Python, Node, GAP, git, GHA, or network command was
run. Edits were confined to the authorized task226 five-file set; the fixture
was inspected and retained byte-for-byte.

## Static repair

The producer now dispatches its public bracket lookup to PB3 exactly when the
noncentral degree is `d=3`, to PB4 exactly when `d=6`, and raises `Q degree`
for every other value. The independent checker implements the same domain
restriction separately. Each implementation derives and enforces central
tuple width one for PB3 and four for PB4, while retaining canonical `0..8`
residues in both orientations.

Both `class2_facts` paths now exercise the positive and negative nonzero
canaries

```text
PB3: (0,1) -> (1,),       (0,2) -> (8,)
PB4: (0,1) -> (1,0,0,0), (0,3) -> (8,0,0,0).
```

Every commutator and direct/inverse roster assertion remains. The checker PB4
direct-roster assertion's accidental two-argument `tuple` call was repaired,
so that existing assertion is executable rather than weakened or removed.

## Additional whole-file audit repairs

The checker emits the preregistered `mutation word` and `mutation width`
gate names used by its fixed mutation table. Its semantic validator rejects
any non-false downstream flag among `boundary_membership`, `pointed_mu1`,
`exact_pb_endpoint_zero`, `cofinal_lift`, `fake`, and `Ihara_witness`; hence
the `forbidden_conclusion` owner mutation is non-vacuous and rejected by its
own gate.

The checker SELFTEST now passes its existing budget object to the existing
terminal-probe helper. This restores the intended terminal probe without
changing its terminal contract. Multiplication, inverse, word, Fox, ABI,
mutation roster, terminal meanings, and conclusion meanings were otherwise
left unchanged.

## Typed-UNKNOWN classification repair

After JSON parsing and canonical self-digest authentication, the checker now
authenticates the mode-specific schema and terminal before considering
conclusion flags. It requires all six top-level conclusion flags to be exactly false only
for `SELFTEST` and `COMPLETE`. Authentic `UNKNOWN_INPUT` and
`UNKNOWN_RESOURCE` receipts retain their exact typed terminal without package
reconstruction or a positive verdict; missing mathematical flags on those
nonaccepting receipts are not reinterpreted as `UNKNOWN_INPUT`.

The checker SELFTEST's independently constructed malformed-input and live
resource-cap envelopes are both sealed and passed through this same classifier.
It requires their classifications to remain `UNKNOWN_INPUT` and
`UNKNOWN_RESOURCE`, respectively, and still compares the complete probe
envelopes with the producer's probes. The serial driver retains its exact
producer/checker terminal-equality gate.

## Final identities

```text
producer  40316  2529d8db89021185c51a4a244af8888041017048925838b42bfcb632dafe573c
checker   34979  aae3babcc998f7f4832e1639c357fc13e9d0eed822a793c6331e696508817424
driver     5167  5810dc785b1c66c48967b82ede7dacb6e8dc17c6152ef05514ce9930e773e630
fixture     1187  91c62b70b3275e9e3bee9689bd677049adc172cb0519a2ccf2808d17d6cabef3
reply     reported out of band after final close (self-referential digest avoided)
```

The driver pins the exact producer/checker/fixture identities above and
continues comparing Linux `sha256sum` output against lowercase digests. The
reply's exact fifth byte/SHA identity is supplied to parent Sol out of band,
because embedding a file's own full SHA-256 changes that identity.

```text
A2 PAPER CONTRACT:                 1/3
A2 IMPLEMENTATION SELFTEST:        0/1 UNEXECUTED
A2 ACTUAL SPECIALIZATION:          0/1 AWAITING A0/A1
COMPATIBLE COFINAL LIFT / FAKE / IHARA: NOT DECLARED
```

`TASK259_TASK226_TYPED_UNKNOWN_FLAG_ORDER_REPAIR_UNEXECUTED`
