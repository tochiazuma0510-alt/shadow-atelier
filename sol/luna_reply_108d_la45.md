# Luna 108d / LA-4+LA-5 recovery report

## Result

LA-4 and LA-5 are closed in one new module:

- `lean/P1/BlockA_LA45.lean`

The module imports only `P1.BlockA`; it is independent of the in-flight LA-2/LA-3
modules.  It uses the actual `window.H : Gn n → Prop`, actual `window.J`, and actual
`conjugatePred` on `Gn n` throughout.

## Exact baseline and isolation

- Read-only source supplied by the commission:
  `C:\Users\81905\AppData\Local\Temp\shadow-atelier-luna106g-b0b23ce9e00145629c7479f5576be1ea`
- Fresh recovery worktree:
  `C:\Users\81905\AppData\Local\Temp\shadow-atelier-la45-recovery-e6715adc168e4891b5747df89a4cda89`
- Detached baseline verified by `git rev-parse HEAD`:
  `82ff1047b80a50b8a3098a83d71424ed2c6ec26d`

The first local `git clone` transport attempt failed because Git for Windows could not
create its `sh.exe` shared-memory mapping (Win32 error 5).  I therefore copied only the
read-only source's `.git` database into a fresh `%TEMP%` directory, set
`core.longpaths=true`, and ran a forced detached checkout of the exact required SHA.
The source and shared workspace were never mutated.

## Closed statements

The module provides:

1. Actual A-conjugation formula:
   `conjugate_by_rotation`, with
   `beta ↦ beta + 2 * (x1 - alpha * xj')` represented additively as
   `beta + (delta + delta)`.
2. Actual Q-conjugation and `q1` formula:
   `conjugate_by_parity`, `conjugate_by_q1`, where `q1` fixes `beta` and sends
   `alpha ↦ -alpha`.
3. Full arbitrary-element formula:
   `conjugate_parameters`, with the parity-adjusted `alpha'` used in the affine
   `beta` formula.
4. Actual normalizing predicates:
   `Normalizes` and `normalizer`.
5. Lemma H(3):
   `normalizer_eq_H_iff (hn : NatOdd n) ... :
      normalizer (H j alpha beta) = H j alpha beta ↔ alpha ≠ 0`.
   The condition is exactly nonzero; no unit hypothesis is introduced.
6. Conjugacy-class characterization:
   `conjugate_H_iff`, giving precisely
   `k = j ∧ (alpha' = alpha ∨ alpha' = -alpha)`, with the second affine parameter
   free.
7. Separate exact finite witnesses:
   - `conjugacyClassEquivNonzero`:
     `PlainEquiv (Fin (2 * n)) (Lambda (H j alpha beta))` under `alpha ≠ 0`;
   - `conjugacyClassEquivZero`:
     `PlainEquiv (Fin n) (Lambda (H j 0 beta))`.

Oddness is explicit in every theorem/witness that uses invertibility of doubling.  A
core-only explicit `Fin (2*n) ↔ XCode n` bijection is included; the result is not merely
an arithmetic formula or an informal cardinality claim.

## Checks

Run from the fresh clone's `lean/` directory:

```text
lake build +P1.BlockA_LA45:olean
```

Result: exit 0, `Built P1.BlockA_LA45`; only pre-existing/import and non-fatal linter
warnings.

```text
lake env lean P1/BlockA_LA45.lean
```

Result: exit 0.

Forbidden-token scan over the new module for
`sorry|admit|axiom|native_decide|ofReduce|True`: no hits.  `git diff --check`: clean.

An external `%TEMP%` audit file imported the module and ran `#print axioms`:

```text
conjugate_by_rotation        [propext, Quot.sound]
conjugate_by_q1              [propext, Quot.sound]
conjugate_parameters         [propext, Quot.sound]
normalizer_eq_H_iff          [propext, Quot.sound]
conjugate_H_iff              [propext, Classical.choice, Quot.sound]
fin2nXCodeEquiv              [propext, Quot.sound]
conjugacyClassEquivNonzero   [propext, Classical.choice, Quot.sound]
conjugacyClassEquivZero      [propext, Classical.choice, Quot.sound]
```

`Classical.choice` is exposed only by choosing the oddness witness / inverse of an
explicitly proved bijection.  There are no project axioms, `sorry`, `admit`, or reduction
shortcuts.

## Changed files and prohibited actions

Changed only in the fresh recovery worktree:

- `lean/P1/BlockA_LA45.lean`
- `sol/luna_reply_108d_la45.md` (this report)

No `BlockA.lean`, maps, manifest, receipt, lake configuration, or workflow file was
edited.  No credentials were accessed; no commit, push, or workflow dispatch was made.
