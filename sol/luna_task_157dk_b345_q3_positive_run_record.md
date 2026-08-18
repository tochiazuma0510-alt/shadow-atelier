# Luna task 157dk — B345 q=3 positive run provenance record

Date: 2026-08-18

## Role and scope

Documentation-only Luna task. Do not edit code, workflows, prior replies,
CLAIMS, or any file other than the single authorized reply below. Do not run
GAP, Python, Git, or GHA.

Authorized output only:

```text
sol/luna_reply_157dk_b345_q3_positive_run_record.md
```

## Frozen facts to record

Record these facts losslessly and distinguish transport failure from the
successful mathematical run.

1. Branch: `sol/b345-q3-chief-v1`.
2. Repair commit pushed by the parent broker:
   `39ee1866e83cc561d6fbab491f37b2b7c0942958`.
3. Frozen code pins:

```text
search/d972_b345_q3_chief_v1.g
  b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755
search/check_d972_b345_q3_chief_v1.py
  ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73
search/d972_b345_q3_gha_driver_v1.g
  c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831
```

4. Canary run `32135560307`: SUCCESS.
5. First full dispatch `32135580224`: failed before the mathematics because
   the CLI dispatch stripped the quoted output path. Record it explicitly as
   a transport/invocation failure, not a mathematical rejection.
6. JSON-API full run `32135808950`: SUCCESS.
7. Its exact decisive log markers:

```text
D972_B345_Q3_DIRECT_SCAN_RESULT result=first_typed_witness evaluated=28 exponent=2 correction_index=1
B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION
B345_Q3_CHECKER_PASS terminal=B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION formula_sha256=b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef PB5_order=3486784401
B345_Q3_GHA_DRIVER_PASS mode=full artifact_sha256=3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72
```

8. Artifact ID `9323958052`, name `gap-run-out`; principal JSON
   `d972_b345_q3_chief_v1.json`, 231570 bytes, SHA-256
   `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`.
9. Receipt facts: schema `d972-b345-q-chief/v1`; one solution after 28
   candidates out of the preregistered 162; selected exponent 2, correction
   index 1, roof row 37; all literal roof/hexagon/pentagon/charming/onto and
   Q4/Pi4 settlement gates true; typed source word
   `[-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1]`; correction
   word empty; `m=0`, `lambda=1`.
10. Runtime was about 9.9 seconds for the producer and about 3.2 seconds for
    the independent checker in the successful full job.

## Mathematical claim boundary

State exactly:

- This is a **cross-checked** fully typed positive at the authenticated finite
  q=3 stage; do not call it Lean-verified.
- With Prop. 3.7, Prop. 3.11, `A <= I_K`, and `[X:A]=3`, the outside witness
  proves `I_K=X` for this exact stage.
- It is not by itself a uniform cofinal-stage theorem and therefore not yet a
  final B4-B proof. The first remaining theorem is uniform next-stage typed
  absorption (or fixed-outside fibre nonemptiness) over a truly cofinal
  isolated family.

End with token:

```text
B345_Q3_POSITIVE_RUN_RECORDED
```
