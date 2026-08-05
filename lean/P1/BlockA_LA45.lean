/-
P1/BlockA_LA45.lean -- LA-4/LA-5 for the odd window family.

This module is deliberately independent of the unfinished LA-2 and LA-3 modules.  It
works with the actual subgroup predicates `window.H : Gn n -> Prop` constructed in
`P1.BlockA`, and uses actual conjugation in `Gn n` throughout.
-/

import P1.BlockA

variable {n : Nat} [NeZero n]

namespace window

@[simp] private theorem val_mul (a b : Gn n) :
    (a * b).val = emul a.val b.val := rfl

@[simp] private theorem val_inv (a : Gn n) :
    (a⁻¹).val = einv a.val := rfl

private theorem cancel_double_right (y x rhs : Fin n) :
    y + (-x + -x) = rhs <-> y = rhs + (x + x) := by
  constructor
  · intro h
    calc
      y = (y + (-x + -x)) + (x + x) := by
        have hz : (-x + x : Fin n) = 0 := fin_add_left_neg x
        calc
          y = y + 0 := (fin_add_zero y).symm
          _ = y + ((-x + x) + (-x + x)) := by rw [hz, fin_zero_add]
          _ = (y + (-x + -x)) + (x + x) := by ac_rfl
      _ = rhs + (x + x) := congrArg (fun z => z + (x + x)) h
  · intro h
    rw [h]
    have hz : (x + -x : Fin n) = 0 := fin_add_right_neg x
    calc
      (rhs + (x + x)) + (-x + -x) = rhs + ((x + -x) + (x + -x)) := by ac_rfl
      _ = rhs := by rw [hz, fin_zero_add, fin_add_zero]

@[simp] private theorem rotation_false_iff (x y a z : Fin n) :
    x + (y + -x) = -a + (a + z) <-> y = z := by
  have hx : x + (y + -x) = y := by
    calc
      x + (y + -x) = (x + -x) + y := by ac_rfl
      _ = y := by rw [fin_add_right_neg, fin_zero_add]
  have ha : -a + (a + z) = z := by
    calc
      -a + (a + z) = (-a + a) + z := by ac_rfl
      _ = z := by rw [fin_add_left_neg, fin_zero_add]
  rw [hx, ha]

@[simp] private theorem rotation_true_iff (y x beta a z : Fin n) :
    y + (-x + -x) = beta + (-a + (-a + z)) <->
      y = beta + (x + (x + (-a + (-a + z)))) := by
  rw [cancel_double_right]
  constructor <;> intro h
  · calc
      y = (beta + (-a + (-a + z))) + (x + x) := h
      _ = beta + (x + (x + (-a + (-a + z)))) := by ac_rfl
  · calc
      y = beta + (x + (x + (-a + (-a + z)))) := h
      _ = (beta + (-a + (-a + z))) + (x + x) := by ac_rfl

@[simp] private theorem rotation_false_iff' (x y a z : Fin n) :
    x + (y + -x) = a + (z + -a) <-> y = z := by
  rw [show a + (z + -a) = -a + (a + z) by ac_rfl]
  exact rotation_false_iff x y a z

@[simp] private theorem rotation_true_iff' (y x beta a z : Fin n) :
    -x + (y + -x) = beta + (-a + (z + -a)) <->
      y = z + (beta + (x + (-a + (x + -a)))) := by
  rw [show -x + (y + -x) = y + (-x + -x) by ac_rfl]
  rw [show beta + (-a + (z + -a)) = beta + (-a + (-a + z)) by ac_rfl]
  rw [show z + (beta + (x + (-a + (x + -a)))) =
      beta + (x + (x + (-a + (-a + z)))) by ac_rfl]
  exact rotation_true_iff y x beta a z

private theorem fin_mul_comm_LA45 (a b : Fin n) : a * b = b * a := by
  apply Fin.ext
  simp [Fin.val_mul, Nat.mul_comm]

private theorem fin_neg_mul_comm_LA45 (a b : Fin n) :
    -(a * b) = b * (-a) := by
  rw [fin_mul_comm_LA45 a b]
  exact (fin_mul_neg_window b a).symm

private theorem fin_mul_neg_comm_LA45 (a b : Fin n) :
    b * (-a) = -(a * b) := (fin_neg_mul_comm_LA45 a b).symm

private theorem fin_neg_eq_iff_LA45 (a b : Fin n) :
    -a = b <-> a = -b := by
  constructor <;> intro h
  · have := congrArg Neg.neg h
    simpa [fin_neg_neg] using this
  · have := congrArg Neg.neg h
    simpa [fin_neg_neg] using this

private theorem fin_neg_mul_neg_LA45 (a b : Fin n) :
    (-a) * (-b) = a * b := by
  calc
    (-a) * (-b) = -((-a) * b) := fin_mul_neg_window (-a) b
    _ = -(-(a * b)) := by
      congr 1
      calc
        (-a) * b = b * (-a) := fin_mul_comm_LA45 (-a) b
        _ = -(b * a) := fin_mul_neg_window b a
        _ = -(a * b) := congrArg Neg.neg (fin_mul_comm_LA45 b a)
    _ = a * b := fin_neg_neg (a * b)

private theorem fin_add_neg_eq_iff_LA45 (a y b : Fin n) :
    a + -y = b ↔ y = a + -b := by
  constructor
  · intro h
    have hay : a = b + y := by
      calc
        a = (a + -y) + y := by
          calc
            a = a + 0 := (fin_add_zero a).symm
            _ = a + (-y + y) :=
              congrArg (fun z => a + z) (fin_add_left_neg y).symm
            _ = (a + -y) + y := by ac_rfl
        _ = b + y := congrArg (fun z => z + y) h
    calc
      y = -b + (b + y) := by rw [← fin_add_assoc, fin_add_left_neg, fin_zero_add]
      _ = -b + a := congrArg (fun z => -b + z) hay.symm
      _ = a + -b := by ac_rfl
  · intro h
    have hby : b + y = a := by
      calc
        b + y = b + (a + -b) := congrArg (fun z => b + z) h
        _ = a := by
          rw [show b + (a + -b) = a + (b + -b) by ac_rfl,
            fin_add_right_neg, fin_add_zero]
    calc
      a + -y = (b + y) + -y := congrArg (fun z => z + -y) hby.symm
      _ = b := by
        calc
          (b + y) + -y = b + (y + -y) := by ac_rfl
          _ = b + 0 := by rw [fin_add_right_neg]
          _ = b := fin_add_zero b

private theorem minus_twice_iff_LA45 (x y rhs : Fin n) :
    -x + (y + -x) = rhs ↔ y = rhs + (x + x) := by
  rw [show -x + (y + -x) = y + (-x + -x) by ac_rfl]
  exact cancel_double_right y x rhs

private theorem cancel_neg_x_x_iff_LA45 (x y rhs : Fin n) :
    -x + (x + -y) = rhs ↔ y = -rhs := by
  rw [show -x + (x + -y) = -y by
    calc
      -x + (x + -y) = (-x + x) + -y := by ac_rfl
      _ = 0 + -y := by rw [fin_add_left_neg]
      _ = -y := fin_zero_add (-y)]
  exact fin_neg_eq_iff_LA45 y rhs

private theorem plus_twice_iff_LA45 (x y rhs : Fin n) :
    x + (x + -y) = rhs ↔ y = (x + x) + -rhs := by
  rw [show x + (x + -y) = (x + x) + -y by ac_rfl]
  exact fin_add_neg_eq_iff_LA45 (x + x) y rhs

private theorem fin_cancel_middle_LA45 (a b : Fin n) :
    a + (b + -a) = b := by
  calc
    a + (b + -a) = (a + -a) + b := by ac_rfl
    _ = 0 + b := by rw [fin_add_right_neg]
    _ = b := fin_zero_add b

private theorem fin_cancel_left_LA45 (a b : Fin n) :
    a + (-a + b) = b := by
  calc
    a + (-a + b) = (a + -a) + b := by ac_rfl
    _ = 0 + b := by rw [fin_add_right_neg]
    _ = b := fin_zero_add b

private theorem H_j2_iff (alpha beta : Fin n) (g : Gn n) :
    H .j2 alpha beta g <->
      g.val.2.1.2 = false /\
      g.val.2.2.2 = g.val.1.2 /\
      g.val.1.1 = alpha * g.val.2.2.1 + betaTerm g.val.1.2 beta := by
  constructor
  · rintro ⟨c, rfl⟩
    rcases c with ⟨s, t, e⟩
    cases e <;> simp [encode, encodeEn, betaTerm]
  · rintro ⟨he2, he3, hx1⟩
    refine ⟨⟨g.val.2.1.1, g.val.2.2.1, g.val.1.2⟩, ?_⟩
    apply Subtype.ext
    rcases g with ⟨⟨⟨x1, e1⟩, ⟨⟨x2, e2⟩, ⟨x3, e3⟩⟩⟩, hg⟩
    cases e1 <;> simp_all [encode, encodeEn, betaTerm]

private theorem H_j3_iff (alpha beta : Fin n) (g : Gn n) :
    H .j3 alpha beta g <->
      g.val.2.2.2 = false /\
      g.val.2.1.2 = g.val.1.2 /\
      g.val.1.1 = alpha * g.val.2.1.1 + betaTerm g.val.1.2 beta := by
  constructor
  · rintro ⟨c, rfl⟩
    rcases c with ⟨s, t, e⟩
    cases e <;> simp [encode, encodeEn, betaTerm]
  · rintro ⟨he3, he2, hx1⟩
    refine ⟨⟨g.val.2.2.1, g.val.2.1.1, g.val.1.2⟩, ?_⟩
    apply Subtype.ext
    rcases g with ⟨⟨⟨x1, e1⟩, ⟨⟨x2, e2⟩, ⟨x3, e3⟩⟩⟩, hg⟩
    cases e1 <;> simp_all [encode, encodeEn, betaTerm]

/- The coordinate indexed by `j' = 5-j` in the paper. -/
def otherRotation (j : J) (g : Gn n) : Fin n :=
  match j with
  | .j2 => g.val.2.2.1
  | .j3 => g.val.2.1.1

/- The reflection flag in the `j`-th dihedral coordinate. -/
def fixedFlag (j : J) (g : Gn n) : Bool :=
  match j with
  | .j2 => g.val.2.1.2
  | .j3 => g.val.2.2.2

def conjugatedAlpha (j : J) (alpha : Fin n) (g : Gn n) : Fin n :=
  signed (fixedFlag j g) alpha

def conjugatedBeta (j : J) (alpha beta : Fin n) (g : Gn n) : Fin n :=
  let alpha' := conjugatedAlpha j alpha g
  let delta := g.val.1.1 - alpha' * otherRotation j g
  signed g.val.1.2 beta + (delta + delta)

def rotationElement (x1 x2 x3 : Fin n) : Gn n :=
  ⟨((x1, false), (x2, false), (x3, false)), by rfl⟩

def rotationDelta (j : J) (alpha x1 x2 x3 : Fin n) : Fin n :=
  match j with
  | .j2 => x1 - alpha * x3
  | .j3 => x1 - alpha * x2

/- Lemma I(1), with the paper's `b = x1 e1 + x2 e2 + x3 e3` represented by an
actual element of `Gn n`. -/
theorem conjugate_by_rotation (j : J) (alpha beta x1 x2 x3 : Fin n) :
    conjugatePred (H j alpha beta) (rotationElement x1 x2 x3) =
      H j alpha (beta + (rotationDelta j alpha x1 x2 x3 +
        rotationDelta j alpha x1 x2 x3)) := by
  funext h
  apply propext
  rw [← Gn_code_left_inv h]
  generalize Gn.toCode h = hc
  rcases hc with ⟨y1, y2, y3, f1, f2⟩
  cases j <;> cases f1 <;> cases f2 <;>
    simp [conjugatePred, gnConj, H_j2_iff, H_j3_iff,
      rotationElement, rotationDelta, GnCode.toGn, GnCode.toEn,
      emul, einv, dmul, dinv, betaTerm,
      fin_sub_eq_add_neg, fin_neg_neg,
      fin_add_neg_cancel_window, fin_add_right_neg, fin_add_left_neg,
      fin_zero_add, fin_add_zero, rotation_false_iff, rotation_true_iff,
      rotation_false_iff', rotation_true_iff']

def parityElement (b1 b2 : Bool) : Gn n :=
  GnCode.toGn ⟨0, 0, 0, b1, b2⟩

def parityAlpha (j : J) (alpha : Fin n) (b1 b2 : Bool) : Fin n :=
  match j with
  | .j2 => signed b2 alpha
  | .j3 => signed (xor b1 b2) alpha

def parityBeta (beta : Fin n) (b1 : Bool) : Fin n := signed b1 beta

/- Conjugation by the four elements of `Q`, still inside the actual subtype `Gn n`. -/
theorem conjugate_by_parity (j : J) (alpha beta : Fin n) (b1 b2 : Bool) :
    conjugatePred (H j alpha beta) (parityElement b1 b2) =
      H j (parityAlpha j alpha b1 b2) (parityBeta beta b1) := by
  funext h
  apply propext
  rw [← Gn_code_left_inv h]
  generalize Gn.toCode h = hc
  rcases hc with ⟨y1, y2, y3, f1, f2⟩
  cases j <;> cases b1 <;> cases b2 <;> cases f1 <;> cases f2 <;>
    simp [conjugatePred, gnConj, H_j2_iff, H_j3_iff,
      parityElement, parityAlpha, parityBeta, GnCode.toGn, GnCode.toEn,
      emul, einv, dmul, dinv, betaTerm, signed,
      fin_sub_eq_add_neg, fin_neg_zero, fin_zero_add, fin_add_zero]
  all_goals
    simp only [fin_neg_mul_comm_LA45, fin_neg_eq_iff_LA45,
      fin_neg_mul_neg_LA45, fin_neg_add, fin_neg_neg]
  all_goals simp only [fin_mul_comm_LA45, fin_add_comm]

/- The complete coordinate formula for conjugation by an arbitrary actual element of
`Gn n`.  This is the rotation formula followed by the parity action, compressed into
the five canonical coordinates of `g`. -/
theorem conjugate_parameters (j : J) (alpha beta : Fin n) (g : Gn n) :
    conjugatePred (H j alpha beta) g =
      H j (conjugatedAlpha j alpha g) (conjugatedBeta j alpha beta g) := by
  rw [← Gn_code_left_inv g]
  generalize Gn.toCode g = gc
  rcases gc with ⟨x1, x2, x3, b1, b2⟩
  funext h
  apply propext
  rw [← Gn_code_left_inv h]
  generalize Gn.toCode h = hc
  rcases hc with ⟨y1, y2, y3, f1, f2⟩
  cases j <;> cases b1 <;> cases b2 <;> cases f1 <;> cases f2 <;>
    simp [conjugatePred, gnConj, H_j2_iff, H_j3_iff,
      conjugatedAlpha, conjugatedBeta, fixedFlag, otherRotation,
      GnCode.toGn, GnCode.toEn, emul, einv, dmul, dinv, betaTerm, signed,
      fin_sub_eq_add_neg, fin_neg_zero, fin_zero_add, fin_add_zero,
      fin_neg_neg, fin_neg_add]
  all_goals
    simp only [fin_neg_mul_comm_LA45, fin_neg_eq_iff_LA45,
      fin_neg_mul_neg_LA45, fin_neg_add, fin_neg_neg]
  all_goals try simp only [fin_mul_comm_LA45, fin_add_comm]
  all_goals try ac_rfl
  all_goals try rw [minus_twice_iff_LA45]
  all_goals try rw [cancel_neg_x_x_iff_LA45]
  all_goals try rw [plus_twice_iff_LA45]
  all_goals
    apply Iff.intro <;> intro hh
    · calc
        y1 = _ := hh
        _ = _ := by
          try simp only [fin_neg_add, fin_mul_neg_comm_LA45,
            fin_neg_mul_neg_LA45, fin_neg_neg,
            fin_cancel_middle_LA45, fin_cancel_left_LA45]
          try ac_rfl
    · calc
        y1 = _ := hh
        _ = _ := by
          try simp only [fin_neg_add, fin_mul_neg_comm_LA45,
            fin_neg_mul_neg_LA45, fin_neg_neg,
            fin_cancel_middle_LA45, fin_cancel_left_LA45]
          try ac_rfl

def q1Element : Gn n := parityElement false true

/- Lemma I(2): `q1` fixes `beta` and sends `alpha` to `-alpha`. -/
theorem conjugate_by_q1 (j : J) (alpha beta : Fin n) :
    conjugatePred (H j alpha beta) q1Element = H j (-alpha) beta := by
  rw [q1Element, conjugate_by_parity]
  cases j <;> simp [parityAlpha, parityBeta, signed]

private theorem H_eq_iff_parameters
    (j k : J) (alpha beta alpha' beta' : Fin n) :
    H j alpha beta = H k alpha' beta' ↔
      j = k ∧ alpha = alpha' ∧ beta = beta' := by
  constructor
  · intro heq
    cases j <;> cases k
    · have ha_mem :
          H .j2 alpha' beta' (encode .j2 alpha beta ⟨0, 1, false⟩) := by
        rw [← heq]
        exact ⟨⟨0, 1, false⟩, rfl⟩
      have hb_mem :
          H .j2 alpha' beta' (encode .j2 alpha beta ⟨0, 0, true⟩) := by
        rw [← heq]
        exact ⟨⟨0, 0, true⟩, rfl⟩
      rw [H_j2_iff] at ha_mem hb_mem
      refine ⟨rfl, ?_, ?_⟩
      · simpa [encode, encodeEn, betaTerm, Fin.mul_one] using ha_mem.2.2
      · simpa [encode, encodeEn, betaTerm, Fin.mul_zero, fin_add_zero]
          using hb_mem.2.2
    · have impossible :
          H .j3 alpha' beta' (encode .j2 alpha beta ⟨0, 0, true⟩) := by
        rw [← heq]
        exact ⟨⟨0, 0, true⟩, rfl⟩
      rw [H_j3_iff] at impossible
      simp [encode, encodeEn] at impossible
    · have impossible :
          H .j2 alpha' beta' (encode .j3 alpha beta ⟨0, 0, true⟩) := by
        rw [← heq]
        exact ⟨⟨0, 0, true⟩, rfl⟩
      rw [H_j2_iff] at impossible
      simp [encode, encodeEn] at impossible
    · have ha_mem :
          H .j3 alpha' beta' (encode .j3 alpha beta ⟨0, 1, false⟩) := by
        rw [← heq]
        exact ⟨⟨0, 1, false⟩, rfl⟩
      have hb_mem :
          H .j3 alpha' beta' (encode .j3 alpha beta ⟨0, 0, true⟩) := by
        rw [← heq]
        exact ⟨⟨0, 0, true⟩, rfl⟩
      rw [H_j3_iff] at ha_mem hb_mem
      refine ⟨rfl, ?_, ?_⟩
      · simpa [encode, encodeEn, betaTerm, Fin.mul_one] using ha_mem.2.2
      · simpa [encode, encodeEn, betaTerm, Fin.mul_zero, fin_add_zero]
          using hb_mem.2.2
  · rintro ⟨rfl, rfl, rfl⟩
    rfl

private theorem fin_neg_eq_self_odd (hn : NatOdd n) (a : Fin n) :
    -a = a ↔ a = 0 := by
  constructor
  · intro h
    by_cases ha : a = 0
    · exact ha
    have hav : a.val ≠ 0 := by
      intro hz
      apply ha
      apply Fin.ext
      simpa using hz
    have hneg : (-a).val = n - a.val := by
      rw [Fin.val_neg]
      simp [ha]
    have hval := congrArg Fin.val h
    rw [hneg] at hval
    have heven : NatEven n := ⟨a.val, by omega⟩
    exact False.elim (natOdd_not_natEven n hn heven)
  · rintro rfl
    exact fin_neg_zero

private theorem fin_double_injective_odd (hn : NatOdd n) (a b : Fin n) :
    a + a = b + b ↔ a = b := by
  constructor
  · intro hab
    let d : Fin n := a + -b
    have hdd : d + d = 0 := by
      change (a + -b) + (a + -b) = 0
      calc
        (a + -b) + (a + -b) = (a + a) + (-b + -b) := by ac_rfl
        _ = (b + b) + (-b + -b) :=
          congrArg (fun z => z + (-b + -b)) hab
        _ = 0 := by
          rw [show (b + b) + (-b + -b) =
              (b + -b) + (b + -b) by ac_rfl,
            fin_add_right_neg, fin_zero_add]
    have hdneg : -d = d := by
      apply fin_add_left_cancel d
      rw [fin_add_right_neg, hdd]
    have hd0 : d = 0 := (fin_neg_eq_self_odd hn d).mp hdneg
    calc
      a = (a + -b) + b := by
        rw [fin_add_assoc, fin_add_left_neg, fin_add_zero]
      _ = 0 + b := congrArg (fun z => z + b) hd0
      _ = b := fin_zero_add b
  · rintro rfl
    rfl

/- Actual elementwise normalizing and normalizer predicates. -/
def Normalizes (K : Gn n → Prop) (g : Gn n) : Prop :=
  conjugatePred K g = K

def normalizer (K : Gn n → Prop) : Gn n → Prop :=
  fun g => Normalizes K g

theorem normalizes_H_iff (j : J) (alpha beta : Fin n) (g : Gn n) :
    Normalizes (H j alpha beta) g ↔
      conjugatedAlpha j alpha g = alpha ∧
        conjugatedBeta j alpha beta g = beta := by
  rw [Normalizes, conjugate_parameters, H_eq_iff_parameters]
  simp

private theorem q1_not_mem_H (j : J) (alpha beta : Fin n) :
    ¬ H j alpha beta q1Element := by
  intro h
  cases j
  · rw [H_j2_iff] at h
    simp [q1Element, parityElement, GnCode.toGn, GnCode.toEn] at h
  · rw [H_j3_iff] at h
    simp [q1Element, parityElement, GnCode.toGn, GnCode.toEn] at h

private theorem beta_double_delta_iff (hn : NatOdd n)
    (beta x a : Fin n) :
    beta + (x + (-a + (x + -a))) = beta ↔ x = a := by
  let d : Fin n := x + -a
  have hshape : x + (-a + (x + -a)) = d + d := by
    change x + (-a + (x + -a)) = (x + -a) + (x + -a)
    ac_rfl
  rw [hshape]
  constructor
  · intro h
    have hdd : d + d = 0 := by
      apply fin_add_left_cancel beta
      calc
        beta + (d + d) = beta := h
        _ = beta + 0 := (fin_add_zero beta).symm
    have hd0 : d = 0 :=
      (fin_double_injective_odd hn d 0).mp (by
        simpa [fin_zero_add] using hdd)
    calc
      x = (x + -a) + a := by
        rw [fin_add_assoc, fin_add_left_neg, fin_add_zero]
      _ = d + a := rfl
      _ = 0 + a := congrArg (fun z => z + a) hd0
      _ = a := fin_zero_add a
  · rintro rfl
    dsimp [d]
    calc
      beta + ((x + -x) + (x + -x)) = beta + (0 + 0) := by
        rw [fin_add_right_neg]
      _ = beta := by rw [fin_zero_add, fin_add_zero]

private theorem neg_beta_double_delta_iff (hn : NatOdd n)
    (beta x a : Fin n) :
    -beta + (x + (-a + (x + -a))) = beta ↔ x = beta + a := by
  let d : Fin n := x + -a
  have hshape : x + (-a + (x + -a)) = d + d := by
    change x + (-a + (x + -a)) = (x + -a) + (x + -a)
    ac_rfl
  rw [hshape]
  constructor
  · intro h
    have hdd : d + d = beta + beta := by
      calc
        d + d = beta + (-beta + (d + d)) := by
          symm
          calc
            beta + (-beta + (d + d)) = (beta + -beta) + (d + d) := by ac_rfl
            _ = 0 + (d + d) := by rw [fin_add_right_neg]
            _ = d + d := fin_zero_add (d + d)
        _ = beta + beta := congrArg (fun z => beta + z) h
    have hd : d = beta := (fin_double_injective_odd hn d beta).mp hdd
    calc
      x = (x + -a) + a := by
        rw [fin_add_assoc, fin_add_left_neg, fin_add_zero]
      _ = d + a := rfl
      _ = beta + a := congrArg (fun z => z + a) hd
  · intro h
    have hd : d = beta := by
      change x + -a = beta
      calc
        x + -a = (beta + a) + -a := congrArg (fun z => z + -a) h
        _ = beta := by rw [fin_add_assoc, fin_add_right_neg, fin_add_zero]
    rw [hd]
    calc
      -beta + (beta + beta) = (-beta + beta) + beta := by ac_rfl
      _ = 0 + beta := by rw [fin_add_left_neg]
      _ = beta := fin_zero_add beta

/- Lemma H(3).  The hypothesis is exactly oddness of `n`; the parameter condition is
`alpha ≠ 0`, not the stronger and incorrect condition that `alpha` be a unit. -/
theorem normalizer_eq_H_iff (hn : NatOdd n) (j : J)
    (alpha beta : Fin n) :
    normalizer (H j alpha beta) = H j alpha beta ↔ alpha ≠ 0 := by
  constructor
  · intro hnormalizer halpha
    subst alpha
    have hq1norm : normalizer (H j 0 beta) q1Element := by
      change Normalizes (H j 0 beta) q1Element
      unfold Normalizes
      rw [conjugate_by_q1, fin_neg_zero]
    have hq1mem : H j 0 beta q1Element := by
      rw [← hnormalizer]
      exact hq1norm
    exact q1_not_mem_H j 0 beta hq1mem
  · intro halpha
    funext g
    apply propext
    rw [normalizer, normalizes_H_iff]
    rw [← Gn_code_left_inv g]
    generalize Gn.toCode g = gc
    rcases gc with ⟨x1, x2, x3, b1, b2⟩
    cases j <;> cases b1 <;> cases b2 <;>
      simp [conjugatedAlpha, conjugatedBeta, fixedFlag, otherRotation,
        H_j2_iff, H_j3_iff, GnCode.toGn, GnCode.toEn, signed, betaTerm,
        fin_neg_eq_self_odd hn, halpha, fin_sub_eq_add_neg,
        fin_neg_zero, fin_zero_add, fin_add_zero, fin_neg_neg,
        fin_double_injective_odd hn, fin_mul_comm_LA45,
        beta_double_delta_iff hn, neg_beta_double_delta_iff hn]

private noncomputable def oddHalf (hn : NatOdd n) (x : Fin n) : Fin n :=
  let m := Classical.choose hn
  let u : Fin n := ⟨(m + 1) % n, Nat.mod_lt _ (by
    have hn0 := NeZero.ne n
    omega)⟩
  u * x

private theorem oddHalf_double (hn : NatOdd n) (x : Fin n) :
    oddHalf hn x + oddHalf hn x = x := by
  let m := Classical.choose hn
  have hm : n = 2 * m + 1 := Classical.choose_spec hn
  let u : Fin n := ⟨(m + 1) % n, Nat.mod_lt _ (by
    have hn0 := NeZero.ne n
    omega)⟩
  have hu : u + u = (1 : Fin n) := by
    apply Fin.ext
    change (((m + 1) % n + (m + 1) % n) % n) = 1 % n
    rw [← Nat.add_mod]
    have hsum : (m + 1) + (m + 1) = n + 1 := by omega
    rw [hsum, Nat.add_mod]
    simp
  change u * x + u * x = x
  calc
    u * x + u * x = x * u + x * u := by
      rw [fin_mul_comm_LA45 u x]
    _ = x * (u + u) := (fin_mul_add_window x u u).symm
    _ = x * 1 := congrArg (fun z => x * z) hu
    _ = x := Fin.mul_one x

private theorem conjugate_same_alpha_reachable (hn : NatOdd n)
    (j : J) (alpha beta gamma : Fin n) :
    ∃ g : Gn n,
      H j alpha gamma = conjugatePred (H j alpha beta) g := by
  let x := oddHalf hn (gamma - beta)
  refine ⟨rotationElement x 0 0, ?_⟩
  rw [conjugate_by_rotation, H_eq_iff_parameters]
  refine ⟨rfl, rfl, ?_⟩
  cases j <;>
    simp [rotationDelta, Fin.mul_zero, fin_sub_zero, x,
      oddHalf_double, fin_add_sub_cancel_left_window]

private theorem conjugate_neg_alpha_reachable (hn : NatOdd n)
    (j : J) (alpha beta gamma : Fin n) :
    ∃ g : Gn n,
      H j (-alpha) gamma = conjugatePred (H j alpha beta) g := by
  let x := oddHalf hn (gamma - beta)
  let g : Gn n := GnCode.toGn ⟨x, 0, 0, false, true⟩
  refine ⟨g, ?_⟩
  rw [conjugate_parameters, H_eq_iff_parameters]
  refine ⟨rfl, ?_, ?_⟩
  · cases j <;>
      simp [g, conjugatedAlpha, fixedFlag, GnCode.toGn, GnCode.toEn, signed]
  · cases j <;>
      simp [g, conjugatedAlpha, conjugatedBeta, fixedFlag, otherRotation,
        GnCode.toGn, GnCode.toEn, signed, Fin.mul_zero, fin_sub_zero, x,
        oddHalf_double, fin_add_sub_cancel_left_window]

/- Lemma I(3), as an exact characterization of the conjugates that remain in the
window family.  The free `gamma` coordinate is represented by `beta'`. -/
theorem conjugate_H_iff (hn : NatOdd n) (j k : J)
    (alpha beta alpha' beta' : Fin n) :
    (∃ g : Gn n,
        H k alpha' beta' = conjugatePred (H j alpha beta) g) ↔
      k = j ∧ (alpha' = alpha ∨ alpha' = -alpha) := by
  constructor
  · rintro ⟨g, hg⟩
    rw [conjugate_parameters, H_eq_iff_parameters] at hg
    refine ⟨hg.1, ?_⟩
    rw [hg.2.1]
    cases hflag : fixedFlag j g <;>
      simp [conjugatedAlpha, signed, hflag]
  · rintro ⟨rfl, halpha | halpha⟩
    · subst alpha'
      exact conjugate_same_alpha_reachable hn k alpha beta beta'
    · subst alpha'
      exact conjugate_neg_alpha_reachable hn k alpha beta beta'

private def fin2nToXCode (x : Fin (2 * n)) : XCode n :=
  if h : x.val < n then
    ⟨⟨x.val, h⟩, false⟩
  else
    ⟨⟨x.val - n, by
      have hx := x.isLt
      omega⟩, true⟩

private def xCodeToFin2n (c : XCode n) : Fin (2 * n) :=
  if c.odd then
    ⟨n + c.rot.val, by
      have hr := c.rot.isLt
      omega⟩
  else
    ⟨c.rot.val, by
      have hr := c.rot.isLt
      have hn0 := NeZero.ne n
      omega⟩

private theorem fin2n_xCode_left_inv (x : Fin (2 * n)) :
    xCodeToFin2n (fin2nToXCode x) = x := by
  unfold fin2nToXCode xCodeToFin2n
  split
  · apply Fin.ext
    simp_all
  · apply Fin.ext
    simp_all
    omega

private theorem fin2n_xCode_right_inv (c : XCode n) :
    fin2nToXCode (xCodeToFin2n c) = c := by
  rcases c with ⟨r, odd⟩
  cases odd
  · unfold xCodeToFin2n fin2nToXCode
    simp [r.isLt]
  · unfold xCodeToFin2n fin2nToXCode
    have hnle : ¬ n + r.val < n := by omega
    simp [hnle]

/- An explicit core-only witness that the existing `XCode n` really has `2*n`
elements. -/
def fin2nXCodeEquiv : PlainEquiv (Fin (2 * n)) (XCode n) :=
  ⟨fin2nToXCode, xCodeToFin2n,
    fin2n_xCode_left_inv, fin2n_xCode_right_inv⟩

private def classRepresentative (j : J) (alpha : Fin n) (c : XCode n) :
    Gn n → Prop :=
  H j (signed c.odd alpha) c.rot

private theorem classRepresentative_mem (hn : NatOdd n) (j : J)
    (alpha beta : Fin n) (c : XCode n) :
    ∃ g : Gn n,
      classRepresentative j alpha c = conjugatePred (H j alpha beta) g := by
  rcases c with ⟨gamma, odd⟩
  cases odd
  · simpa [classRepresentative, signed] using
      (conjugate_same_alpha_reachable hn j alpha beta gamma)
  · simpa [classRepresentative, signed] using
      (conjugate_neg_alpha_reachable hn j alpha beta gamma)

private theorem classRepresentative_injective (hn : NatOdd n)
    (halpha : alpha ≠ (0 : Fin n)) (j : J) :
    Function.Injective (classRepresentative j alpha) := by
  intro c d h
  rcases c with ⟨gamma, odd⟩
  rcases d with ⟨delta, odd'⟩
  cases odd <;> cases odd'
  · have hp := (H_eq_iff_parameters j j alpha gamma alpha delta).mp
      (by simpa [classRepresentative, signed] using h)
    cases hp.2.2
    rfl
  · have hp := (H_eq_iff_parameters j j alpha gamma (-alpha) delta).mp
      (by simpa [classRepresentative, signed] using h)
    have hz : alpha = 0 :=
      (fin_neg_eq_self_odd hn alpha).mp hp.2.1.symm
    exact False.elim (halpha hz)
  · have hp := (H_eq_iff_parameters j j (-alpha) gamma alpha delta).mp
      (by simpa [classRepresentative, signed] using h)
    have hz : alpha = 0 :=
      (fin_neg_eq_self_odd hn alpha).mp hp.2.1
    exact False.elim (halpha hz)
  · have hp := (H_eq_iff_parameters j j (-alpha) gamma (-alpha) delta).mp
      (by simpa [classRepresentative, signed] using h)
    cases hp.2.2
    rfl

private theorem classRepresentative_surjective (hn : NatOdd n)
    (j : J) (alpha beta : Fin n) (K : Lambda (H j alpha beta)) :
    ∃ c : XCode n, K.val = classRepresentative j alpha c := by
  rcases K.property with ⟨g, hg⟩
  refine ⟨⟨conjugatedBeta j alpha beta g, fixedFlag j g⟩, ?_⟩
  calc
    K.val = conjugatePred (H j alpha beta) g := hg
    _ = H j (conjugatedAlpha j alpha g)
        (conjugatedBeta j alpha beta g) := conjugate_parameters j alpha beta g
    _ = classRepresentative j alpha
        ⟨conjugatedBeta j alpha beta g, fixedFlag j g⟩ := by
      rfl

private noncomputable def conjugacyClassXCodeEquiv (hn : NatOdd n)
    (halpha : alpha ≠ (0 : Fin n)) (j : J) (beta : Fin n) :
    PlainEquiv (XCode n) (Lambda (H j alpha beta)) where
  toFun c := ⟨classRepresentative j alpha c,
    classRepresentative_mem hn j alpha beta c⟩
  invFun K := Classical.choose (classRepresentative_surjective hn j alpha beta K)
  left_inv c := classRepresentative_injective hn halpha j
    (Classical.choose_spec
      (classRepresentative_surjective hn j alpha beta
        ⟨classRepresentative j alpha c,
          classRepresentative_mem hn j alpha beta c⟩)).symm
  right_inv K := by
    apply Subtype.ext
    exact (Classical.choose_spec
      (classRepresentative_surjective hn j alpha beta K)).symm

/- Exact finite witness for the nonzero branch of Lemma I(3): the conjugacy class
has `2*n` elements. -/
noncomputable def conjugacyClassEquivNonzero (hn : NatOdd n)
    (halpha : alpha ≠ (0 : Fin n)) (j : J) (beta : Fin n) :
    PlainEquiv (Fin (2 * n)) (Lambda (H j alpha beta)) := by
  let e₁ := fin2nXCodeEquiv (n := n)
  let e₂ := conjugacyClassXCodeEquiv hn halpha j beta
  exact
    { toFun := fun x => e₂.toFun (e₁.toFun x)
      invFun := fun K => e₁.invFun (e₂.invFun K)
      left_inv := by
        intro x
        rw [e₂.left_inv, e₁.left_inv]
      right_inv := by
        intro K
        rw [e₁.right_inv, e₂.right_inv] }

private def zeroClassRepresentative (j : J) (gamma : Fin n) : Gn n → Prop :=
  H j 0 gamma

private theorem zeroClassRepresentative_mem (hn : NatOdd n) (j : J)
    (beta gamma : Fin n) :
    ∃ g : Gn n,
      zeroClassRepresentative j gamma = conjugatePred (H j 0 beta) g := by
  simpa [zeroClassRepresentative] using
    (conjugate_same_alpha_reachable hn j 0 beta gamma)

private theorem zeroClassRepresentative_injective (j : J) :
    Function.Injective (zeroClassRepresentative (n := n) j) := by
  intro gamma delta h
  exact ((H_eq_iff_parameters j j 0 gamma 0 delta).mp
    (by simpa [zeroClassRepresentative] using h)).2.2

private theorem zeroClassRepresentative_surjective (hn : NatOdd n)
    (j : J) (beta : Fin n) (K : Lambda (H j 0 beta)) :
    ∃ gamma : Fin n, K.val = zeroClassRepresentative j gamma := by
  rcases K.property with ⟨g, hg⟩
  refine ⟨conjugatedBeta j 0 beta g, ?_⟩
  calc
    K.val = conjugatePred (H j 0 beta) g := hg
    _ = H j (conjugatedAlpha j 0 g) (conjugatedBeta j 0 beta g) :=
      conjugate_parameters j 0 beta g
    _ = zeroClassRepresentative j (conjugatedBeta j 0 beta g) := by
      cases hflag : fixedFlag j g <;>
        simp [conjugatedAlpha, signed, hflag, zeroClassRepresentative,
          fin_neg_zero]

/- Exact finite witness for the zero branch of Lemma I(3): the conjugacy class has
`n` elements. -/
noncomputable def conjugacyClassEquivZero (hn : NatOdd n) (j : J)
    (beta : Fin n) : PlainEquiv (Fin n) (Lambda (H j 0 beta)) where
  toFun gamma := ⟨zeroClassRepresentative j gamma,
    zeroClassRepresentative_mem hn j beta gamma⟩
  invFun K := Classical.choose (zeroClassRepresentative_surjective hn j beta K)
  left_inv gamma := zeroClassRepresentative_injective j
    (Classical.choose_spec
      (zeroClassRepresentative_surjective hn j beta
        ⟨zeroClassRepresentative j gamma,
          zeroClassRepresentative_mem hn j beta gamma⟩)).symm
  right_inv K := by
    apply Subtype.ext
    exact (Classical.choose_spec
      (zeroClassRepresentative_surjective hn j beta K)).symm

end window
