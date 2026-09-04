# Sol reply -- Task907 / R07 physical-state Separator run 2 audit

## Verdict

PASS.  I audited the downloaded final candidate at
`C:/Users/81905/AppData/Local/Temp/shadow-atelier-task904-run33891714539-final`
read-only.  Its producer terminal, independent-checker result, authenticated
state, and a third helper-independent replay agree on a `Separator` for the
current initial physical space S0:

```text
lambda(S0)=0
lambda(rho2)=1
dim(S0)=1354
```

It is an input to the scalar/CEGAR loop, not a full Grade-2 NONMEMBER or any
upper arithmetic claim.

## Exact final-object receipts

The root roster is exactly the two directories `state`, `output`, plus
`checker-result.json`; the state and output sub-rosters are exact.  Every
receipt in reply906 recomputed as follows:

| file | bytes | SHA-256 |
|---|---:|---|
| `state/HEAD` | 299 | `f789ac352864ae662beced75f9004887fe677f81eee922eb9d9200dcaf6860ef` |
| `state/manifest.json` | 7,780 | `d11d551c2b1a127bd900c013cbc684eef698372660ff733b10f82bb4793f227b` |
| `state/physical.bin` | 16,377,984 | `1246ae0c23c7dcbfc2a1c2f73075f38968a4ab7b2e5c8fc006f0f8aafae2d57e` |
| `state/physical-p1-coeff.bin` | 2,728,310 | `a2d462ea6c8685a59e28f3f5d1c89656e2e942a65110a21184e33c6cb334826c` |
| `state/instructions.jsonl` | 86,919,157 | `a7cbe317ba92b0d4076623dfd5ea672d2ef4b154f5be2862e0dc232ba91309c2` |
| `output/lambda.bin` | 12,096 | `7522ee1f00f386b229ea46bc0f2b9fdf2854cf03c262f40a2f60dd9ced0102ed` |
| `output/reverse-substitution.jsonl` | 232,321 | `b1119a6aa506e8ccca339dfbc140f5a59a5bc732db2f266f2a81dff762e115f7` |
| `output/terminal.json` | 457,656 | `098d5961cddc187d01c08e22f9f40ce55a7a02e8a1b1d088eca8c804957098cf` |
| `output/result.json` | 457,791 | `d23892a4319a6d7eaa3d09af17a84e59cb6b0a1635f527fb77dc1038ae749968` |
| `checker-result.json` | 515 | `2cad883205a5a1dc6e8795567004e071c3a7868351cf1d801727a695b43aa433` |

All four JSON objects and every line of both JSONL streams are canonical
ASCII with a final LF.  `HEAD.manifest_sha256` is the recomputed state
manifest hash; its generation/rank/cursor/rolling head join the manifest.
The terminal binds that same manifest hash.  Removing only
`terminal_receipt` from `result.json` gives `terminal.json` exactly, and the
receipt contains its exact 457,656 bytes and SHA.  Reconstructing the complete
expected checker-result object from audited values gives the downloaded
checker result byte-for-byte.

## Independent replay

I used a standalone base-3 decoder, packer, rolling-hash replay, and dot
product; it imports neither frozen producer nor checker.

| gate | result | independent evidence |
|---|---|---|
| Source/state instruction chains | PASS | Parsed 8,059 actual state lines.  The embedded source chain independently counted 6,705 source pivots and 1,354 source connections, summed 7,665,974 source reductions, and ended at `3cb1bcf691038d71082b8d4774c5dd8898a239e71ef64da22ec486ba923cb8bd`.  The state chain counted 1,354 physical pivots, 6,705 skipped offers, zero physical dependents, and ended at `69fdcc8cd740f8ea11bd198aaf44bcf50d1c4980331f51aa7f792544b00f9d88`. |
| Physical store and order | PASS | All 1,354 packed rows have the recorded normalized lead and zero entries at every earlier insertion lead; offsets and rank counters advance exactly.  Lead order is genuinely nonmonotone: it begins `0,3,1,4,2,...`, with first inversion `3 -> 1`.  Store sizes are exactly `1354*12096` and `1354*2015`. |
| Target reduction | PASS | Starting from the exact rho2-v17 packed vector (12,096 bytes, SHA `b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e`) and sweeping actual rows in insertion order independently reproduced all 884 recorded nonzero reductions, including row/coefficient hashes.  The packed remainder and SHA `e0053fc6e745e4459e0324d26320bf9f5e434a2942fa4a519ebaf9e28df50011` agree; its first nonzero coordinate/value is exactly `1417/2`. |
| Reverse transcript | PASS | Canonically parsed 1,354 actual transcript lines and replayed pivot IDs 1,353 down to 0.  Every offer, lead, packed-row SHA, lambda value, and zero row equation agrees.  Repacking the constructed functional equals `lambda.bin` byte-for-byte. |
| Direct dot check | PASS | The independent decoder found lambda support 914 and SHA `7522ee1f00f386b229ea46bc0f2b9fdf2854cf03c262f40a2f60dd9ced0102ed`.  Direct dot products over all 48,384 coordinates gave zero for each of all 1,354 physical rows (`bad=0`) and one for exact rho2-v17. |
| Terminal/checker/parents | PASS | Terminal and checker both say `Separator`; checker independently records PASS, 8,059 offers, rank 1,354, skipped 6,705, dependent 0, 884 reductions, free coordinate 1,417, nonmonotone insertion, and complete reverse substitution.  The state binds connection manifest SHA `262e4493844540c00e816efe36fdcdadba9b4fc99526beaa7c5acb9a84887ddf` and both source rolling/ancestry data; target reduction binds rho2 manifest SHA `55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488`; terminal binds the exact state manifest. |
| Final publication authority | PASS | Reply906 records commit `7b7b9de20faaa3b8f26e331bb738b374f6f5708c`, run `33891714539/1`, job `101084707867`, producer/checker success, and both uploads success.  Its final artifact is ID `9944214057`, name `d972-r07-grade2-physical-state-separator-v2-candidate-33891714539-1`, 107,195,261 archive bytes, digest `sha256:2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017`.  The frozen 20,126-byte workflow SHA is `e7529e03f0125ae0d6b28f1fb817757d61d1f12dcb48ad929052fe7a1e81b6d7`; it publishes exactly this final three-entry roster only after both named steps succeed.  The downloaded 107,193,909 uncompressed payload matches that stanza exactly and contains the successful checker result.  The distinct unchecked artifact ID `9944212161` and its diagnostic extras are absent.  The outer archive digest is recorded authority rather than recomputed from the already-expanded directory, consistent with the no-credentials boundary. |

The embedded candidate fields remain `cross_checked=false` because they are
immutable run bytes.  This Sol audit promotes only the same-object initial-S0
separator in the claims ledger; it does not rewrite the artifact and does not
reserve the word verified.

```text
VERDICT=PASS
INITIAL_SEPARATOR_CROSS_CHECKED=yes
CURRENT_S0_RANK=1354
LAMBDA_S0=0
LAMBDA_RHO2=1
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```
