/-
Marking.lean — proof-of-life for the Lean 工場 (司令塔 workorder 3.5).

Encodes the A5 marking identity from search/manifest_spec_v1.md stage A1
(`marking`: t=(1 2 3), a=(1 4 5), X = a t^-1 = (1 3 2 4 5), Y = t X t^-1 = (1 3 4 5 2),
 s = t X^3 = (1 4)(3 5), theta_P = Ad(s)`), i.e. `s ∘ X ∘ s⁻¹ = Y`, as permutations of
`Fin 5` (0-indexed: subtract 1 from every 1-indexed label in the spec's cycle notation).

Plain Lean 4 core only — no Mathlib (8GB RAM constraint, minimal dependency footprint).
Permutations are written as total functions `Fin 5 → Fin 5` by explicit case split, so
`decide` can settle the identity by direct computation. `s` is an involution (checked
separately), so `s⁻¹ = s` and `s ∘ X ∘ s⁻¹` is encoded pointwise as `s (X (s i))`.
-/

/-- `s = (1 4)(3 5)` in the spec's 1-indexed cycle notation, 0-indexed here as `(0 3)(2 4)`. -/
def s : Fin 5 → Fin 5
  | 0 => 3
  | 1 => 1
  | 2 => 4
  | 3 => 0
  | 4 => 2

/-- `X = (1 3 2 4 5)` in the spec's 1-indexed cycle notation, 0-indexed here as `(0 2 1 3 4)`. -/
def X : Fin 5 → Fin 5
  | 0 => 2
  | 1 => 3
  | 2 => 1
  | 3 => 4
  | 4 => 0

/-- `Y = (1 3 4 5 2)` in the spec's 1-indexed cycle notation, 0-indexed here as `(0 2 3 4 1)`. -/
def Y : Fin 5 → Fin 5
  | 0 => 2
  | 1 => 0
  | 2 => 3
  | 3 => 4
  | 4 => 1

/-- `s` is an involution, so `s⁻¹ = s` as a function on `Fin 5`. -/
theorem s_involution :
    s (s 0) = 0 ∧ s (s 1) = 1 ∧ s (s 2) = 2 ∧ s (s 3) = 3 ∧ s (s 4) = 4 := by
  decide

/-- proof-of-life: the A5 marking identity `s ∘ X ∘ s⁻¹ = Y` (spec `theta_P = Ad(s)`),
checked pointwise on all five elements of `Fin 5` by direct computation (`decide`). -/
theorem marking_identity :
    s (X (s 0)) = Y 0 ∧
    s (X (s 1)) = Y 1 ∧
    s (X (s 2)) = Y 2 ∧
    s (X (s 3)) = Y 3 ∧
    s (X (s 4)) = Y 4 := by
  decide

#print axioms marking_identity
