# Luna task 250 - task226 lowercase driver-pin repair v1

Commissioner: Sol / 2026-08-28

Reply to:
`sol/luna_reply_226_r07_actual_two_word_endpoint_specializer_v2.md`.

Role: bounded mechanical repair only.  Read task249 and its current five-file
return first.  Do not run Python, Node, GAP, git, GHA, or network locally.
Edit only the task226 GAP driver and the task226 Luna reply.  Do not alter the
producer, checker, fixture, formulas, ABI, caps, or mutation roster.

## 1. Exact rejection

The current driver stores the three producer/checker/fixture SHA-256 values
in uppercase, but compares them on the Ubuntu runner against the lowercase
text printed by `sha256sum`.  Bash `test` is case-sensitive, so SELFTEST must
stop at the first source pin before either Python program runs.

Replace the three stored driver SHA strings by the exact lowercase values
already measured from the shared tree:

```text
producer 78cc0c12252f2d68ebd9fbe456f27df75498689ee5ec09bce40fe275e79e1fe7
checker  6e0ce2412ee8798fb08647330f6656ef2a52e9eafbf96810b41b2726480ac278
fixture  91c62b70b3275e9e3bee9689bd677049adc172cb0519a2ccf2808d17d6cabef3
```

Do not normalize the live `sha256sum` output and do not weaken the equality
gate.  Update the reply so its reported digests use the same exact lowercase
serialization and explicitly records this eighth repair.  Re-read the two
edited shared files and report their byte/SHA identities.  Remain
`UNEXECUTED`.

End with the same v220 boundary:

```text
A2 PAPER CONTRACT:                 1/3
A2 IMPLEMENTATION SELFTEST:        0/1 UNEXECUTED
A2 ACTUAL SPECIALIZATION:          0/1 AWAITING A0/A1
A3 AND LATER:                      UNCHANGED
COMPATIBLE COFINAL LIFT / FAKE / IHARA: NOT DECLARED
```
