# Luna reply 270 - task226 unsigned-xi checker repair

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

## Executed rejection and rg/rf owner repair

Parent execution established that run `33145825325` failed the driver
sentinel, run `33146069436` reached the exact positive producer SELFTEST
terminal, and run `33146219086` reached that same producer terminal before
the checker returned `UNKNOWN_INPUT reason=fresh complete ABI rebuild`. This
Luna pass did not execute those runs or any replacement run.

The producer's `rg/rf` names no longer get overwritten by flattened free
words. `literals.rg` and `literals.rf` now serialize the exact eleven
per-occurrence quotient values from `rkeys_g/rkeys_f`: six Q3 values of width
four followed by five Q4 values of width ten. The three block free words
remain only under `relation_words_g/f` and their existing `R_B_g0/f` aliases.

Before whole-ABI comparison, both producer and independent checker now
require exactly eleven `rg/rf` rows and re-evaluate each corresponding
`rword_g/rword_f`. Every re-evaluated value must equal both the literal roster
entry and the owning occurrence's `r_g/r_f`. Thus this field has a named
semantic gate and is not protected only by a whole-object digest/equality.

A key-by-key static comparison of the remaining ABI found no further shape
mismatch: the top-level ABI fields, all occurrence fields, substitutions,
signed factor and block-word rosters, Fox-chain dictionaries, endpoints,
`minus_fox` fields, and `u0` ancestry have matching producer/checker shapes.
No PB3/PB4 arithmetic, Fox identity, ledger, typed-UNKNOWN, mutation owner,
or conclusion semantics was changed.

## Unsigned xi checker repair

Parent diagnostic run `33147829352` localized the next producer/checker ABI
difference to `occurrences[1].xi_o[0].coefficient`: producer `2`, checker `1`.
The producer already implements the preregistered placement

```text
xi_o = r_o^-1 - 1,
w_o  = factor_sign * P_o * xi_o.
```

The independent checker reconstruction now likewise leaves `xi` unsigned,
first translates it by `P_o`, and applies `factor_sign` only to the resulting
`wo` coefficients. Consequently negative-factor occurrences serialize the
same unsigned `xi_o` as positive-factor occurrences while retaining the sign
in `w_o`. Words, prefix/orientation handling, quotient rosters, Fox data,
mutation owners, typed UNKNOWN gates, and false conclusions are unchanged.
This Luna pass did not execute the checker or full serial driver.

## Final identities

```text
producer  40556  a1532740a7343bd8166c17947f6bd95203a4abdaaafd8e0d9607d3cdf202e6fb
checker   35436  b81de8d7701995c5022dc2e97099599b18dafa6030233f29c37e60dfb70084eb
driver     5167  866469da9629c6218cf40012e36fdbabf5d1a6a20d726a7d9581fc75eafc19d6
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

`TASK270_TASK226_UNSIGNED_XI_CHECKER_REPAIR_UNEXECUTED`
