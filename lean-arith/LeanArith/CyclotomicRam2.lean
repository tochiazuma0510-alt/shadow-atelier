import Mathlib.NumberTheory.NumberField.Cyclotomic.Ideal

/-!
# Ramification of two in an odd cyclotomic tower

This file discharges the proposed `T1_cyclotomic_ram2` boundary using Mathlib's
general ramification formula for cyclotomic extensions.  If `n` is odd, then
`4 * n = 2 ^ (1 + 1) * n`, so the ramification index of `2` in a
`(4 * n)`-cyclotomic extension of `?` is `2 ^ 1 * (2 - 1) = 2`.
-/

namespace LeanArith

open Ideal NumberField RingOfIntegers

/-- In a `(4 * n)`-cyclotomic extension of `?`, with `n` odd, the global
ramification index of the ideal `(2)` is `2`. -/
theorem cyclotomic_ramificationIdxIn_two
    (n : ?) (hn : Odd n)
    (K : Type*) [Field K] [NumberField K]
    [IsCyclotomicExtension {4 * n} ? K] :
    (Ideal.span {(2 : ?)}).ramificationIdxIn (NumberField.RingOfIntegers K) = 2 := by
  have hfactor : 4 * n = 2 ^ (1 + 1) * n := by norm_num
  simpa using
    (IsCyclotomicExtension.Rat.ramificationIdxIn_eq
      (n := 4 * n) (m := n) (p := 2) (k := 1) K hfactor hn.not_two_dvd_nat)

/-- Prime-ideal form of `cyclotomic_ramificationIdxIn_two`: every prime of the
ring of integers above `(2)` has ramification index `2`. -/
theorem cyclotomic_ramificationIdx_two
    (n : ?) (hn : Odd n)
    (K : Type*) [Field K] [NumberField K]
    [IsCyclotomicExtension {4 * n} ? K]
    (P : Ideal (NumberField.RingOfIntegers K))
    [P.IsPrime] [P.LiesOver (Ideal.span {(2 : ?)})] :
    ramificationIdx P ? = 2 := by
  have hfactor : 4 * n = 2 ^ (1 + 1) * n := by norm_num
  simpa using
    (IsCyclotomicExtension.Rat.ramificationIdx_eq
      (n := 4 * n) (m := n) (p := 2) (k := 1) K P hfactor hn.not_two_dvd_nat)

/-- Typed sanity instance: the theorem specializes to twelfth roots of unity
(`n = 3`). -/
example
    (K : Type*) [Field K] [NumberField K]
    [IsCyclotomicExtension {12} ? K] :
    (Ideal.span {(2 : ?)}).ramificationIdxIn (NumberField.RingOfIntegers K) = 2 := by
  simpa using cyclotomic_ramificationIdxIn_two 3 (by decide) K

#print axioms cyclotomic_ramificationIdxIn_two
#print axioms cyclotomic_ramificationIdx_two

end LeanArith
