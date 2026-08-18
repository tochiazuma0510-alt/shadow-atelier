# Luna reply 157dk — B345 q=3 positive run provenance record

Date: 2026-08-18

## Frozen provenance

The successful calculation belongs to branch `sol/b345-q3-chief-v1`. The
parent broker pushed repair commit
`39ee1866e83cc561d6fbab491f37b2b7c0942958` with these exact code pins:

```text
search/d972_b345_q3_chief_v1.g
  b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755
search/check_d972_b345_q3_chief_v1.py
  ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73
search/d972_b345_q3_gha_driver_v1.g
  c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831
```

The run sequence was:

1. Canary run `32135560307`: **SUCCESS**.
2. First full dispatch `32135580224`: failed before any mathematics because
   the CLI invocation stripped the quoted output path. This was solely a
   transport/invocation failure and is not a mathematical rejection.
3. JSON-API full run `32135808950`: **SUCCESS**.

The decisive markers from the successful full run were exactly:

```text
D972_B345_Q3_DIRECT_SCAN_RESULT result=first_typed_witness evaluated=28 exponent=2 correction_index=1
B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION
B345_Q3_CHECKER_PASS terminal=B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION formula_sha256=b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef PB5_order=3486784401
B345_Q3_GHA_DRIVER_PASS mode=full artifact_sha256=3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72
```

## Artifact and receipt

Artifact ID `9323958052` has name `gap-run-out`. Its principal receipt is
`d972_b345_q3_chief_v1.json`, 231570 bytes, with SHA-256
`3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`.

The receipt has schema `d972-b345-q-chief/v1`. It records one solution after
28 evaluated candidates from the preregistered universe of 162. The selected
data are:

```text
exponent:         2
correction_index: 1
roof_row:         37
m:                0
lambda:           1
typed_source_word:
  [-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1]
correction_word:  []
```

Every literal roof, hexagon, pentagon, charming, onto, Q4-settlement, and
Pi4-settlement gate is true. The successful job took approximately 9.9
seconds in the producer and 3.2 seconds in the independent checker.

## Mathematical claim boundary

This receipt is a **cross-checked**, fully typed positive at the authenticated
finite q=3 stage. It is not Lean-verified.

Let `X=ML(M)` and let
`I_K=image(ML(K) -> ML(M))` for this exact isolated stage. Proposition 3.7
makes the reduction a group homomorphism, hence `I_K` a subgroup of `X`.
Proposition 3.11 and arithmetic naturality give `A <= I_K`. The checked typed
word supplies an actual roof element in `I_K \ A`. Together with the accepted
prime-index premise `[X:A]=3`, the subgroup index formula therefore proves

```text
I_K = X
```

for this exact finite q=3 stage.

This result is not by itself a uniform cofinal-stage theorem and is therefore
not yet a final B4-B proof. The first remaining theorem is uniform next-stage
typed absorption, or equivalently sufficient fixed-outside fibre
nonemptiness, over a genuinely cofinal isolated family.

B345_Q3_POSITIVE_RUN_RECORDED
