import P1.BlockA

/- Finite equal-cardinality core for LA-2. -/

def la2SwapZero {m : Nat} [NeZero m] (a x : Fin m) : Fin m :=
  if x = 0 then a else if x = a then 0 else x

theorem la2SwapZero_involutive {m : Nat} [NeZero m] (a x : Fin m) :
    la2SwapZero a (la2SwapZero a x) = x := by
  classical
  by_cases ha : a = 0
  case pos =>
    subst a
    by_cases hx : x = 0
    case pos =>
      subst x
      simp [la2SwapZero]
    case neg =>
      simp [la2SwapZero, hx]
  case neg =>
    by_cases hx0 : x = 0
    case pos =>
      subst x
      simp [la2SwapZero, ha]
    case neg =>
      by_cases hxa : x = a
      case pos =>
        subst x
        simp [la2SwapZero, ha]
      case neg =>
        simp [la2SwapZero, hx0, hxa]

theorem la2SwapZero_injective {m : Nat} [NeZero m] (a : Fin m) :
    Function.Injective (la2SwapZero a) := by
  intro x y h
  calc
    x = la2SwapZero a (la2SwapZero a x) := (la2SwapZero_involutive a x).symm
    _ = la2SwapZero a (la2SwapZero a y) := congrArg (la2SwapZero a) h
    _ = y := la2SwapZero_involutive a y

theorem la2SwapZero_self {m : Nat} [NeZero m] (a : Fin m) :
    la2SwapZero a a = 0 := by
  classical
  by_cases ha : a = 0
  case pos =>
    subst a
    simp [la2SwapZero]
  case neg =>
    simp [la2SwapZero, ha]

def la2FinTail {m : Nat} (g : Fin (m + 1) -> Fin (m + 1))
    (hne : forall i : Fin m, Not (g i.succ = 0)) (i : Fin m) : Fin m :=
  (g i.succ).pred (hne i)

theorem la2FinTail_succ {m : Nat} (g : Fin (m + 1) -> Fin (m + 1))
    (hne : forall i : Fin m, Not (g i.succ = 0)) (i : Fin m) :
    (la2FinTail g hne i).succ = g i.succ := by
  exact Fin.succ_pred _ _

theorem la2Fin_injective_surjective :
    forall m : Nat, forall f : Fin m -> Fin m,
      Function.Injective f -> Function.Surjective f := by
  intro m
  induction m with
  | zero =>
      intro f hf y
      exact Fin.elim0 y
  | succ m ih =>
      intro f hf
      let a : Fin (m + 1) := f 0
      let g : Fin (m + 1) -> Fin (m + 1) := fun x => la2SwapZero a (f x)
      have hg_inj : Function.Injective g := by
        intro x y h
        apply hf
        exact la2SwapZero_injective a h
      have hg_zero : g 0 = 0 := by
        change la2SwapZero a (f 0) = 0
        exact la2SwapZero_self a
      have hg_succ_ne : forall i : Fin m, Not (g i.succ = 0) := by
        intro i hzero
        have hsame : g i.succ = g 0 := by
          rw [hg_zero]
          exact hzero
        exact Fin.succ_ne_zero i (hg_inj hsame)
      let r : Fin m -> Fin m := la2FinTail g hg_succ_ne
      have hr_inj : Function.Injective r := by
        intro i j hij
        have hsucc : (r i).succ = (r j).succ := congrArg Fin.succ hij
        have hgij : g i.succ = g j.succ := by
          calc
            g i.succ = (r i).succ := (la2FinTail_succ g hg_succ_ne i).symm
            _ = (r j).succ := hsucc
            _ = g j.succ := la2FinTail_succ g hg_succ_ne j
        have hsij : i.succ = j.succ := hg_inj hgij
        apply Fin.ext
        exact Nat.succ.inj (congrArg Fin.val hsij)
      have hr_surj : Function.Surjective r := ih r hr_inj
      have hg_surj : Function.Surjective g := by
        intro y
        cases Fin.eq_zero_or_eq_succ y with
        | inl hzero =>
            exact Exists.intro 0 (hg_zero.trans hzero.symm)
        | inr hsucc =>
            cases hsucc with
            | intro j hj =>
                subst y
                have hex := hr_surj j
                cases hex with
                | intro i hi =>
                    refine Exists.intro i.succ ?_
                    have hs := congrArg Fin.succ hi
                    rw [la2FinTail_succ g hg_succ_ne i] at hs
                    exact hs
      intro y
      have hex := hg_surj (la2SwapZero a y)
      cases hex with
      | intro x hx =>
          refine Exists.intro x ?_
          change la2SwapZero a (f x) = la2SwapZero a y at hx
          have hs := congrArg (la2SwapZero a) hx
          calc
            f x = la2SwapZero a (la2SwapZero a (f x)) :=
              (la2SwapZero_involutive a (f x)).symm
            _ = la2SwapZero a (la2SwapZero a y) := hs
            _ = y := la2SwapZero_involutive a y
theorem la2Fin_surjective_injective (m : Nat) (f : Fin m -> Fin m)
    (hf : Function.Surjective f) : Function.Injective f := by
  classical
  let s : Fin m -> Fin m := fun y => Classical.choose (hf y)
  have hs_right : forall y : Fin m, f (s y) = y := by
    intro y
    exact Classical.choose_spec (hf y)
  have hs_inj : Function.Injective s := by
    intro x y h
    calc
      x = f (s x) := (hs_right x).symm
      _ = f (s y) := congrArg f h
      _ = y := hs_right y
  have hs_surj : Function.Surjective s :=
    la2Fin_injective_surjective m s hs_inj
  intro x y hxy
  have hx := hs_surj x
  have hy := hs_surj y
  cases hx with
  | intro a ha =>
      cases hy with
      | intro b hb =>
          have hab : a = b := by
            calc
              a = f (s a) := (hs_right a).symm
              _ = f x := congrArg f ha
              _ = f y := hxy
              _ = f (s b) := congrArg f hb.symm
              _ = b := hs_right b
          calc
            x = s a := ha.symm
            _ = s b := congrArg s hab
            _ = y := hb

theorem la2Plain_to_injective {A B : Type} (e : PlainEquiv A B) :
    Function.Injective e.toFun := by
  intro x y h
  calc
    x = e.invFun (e.toFun x) := (e.left_inv x).symm
    _ = e.invFun (e.toFun y) := congrArg e.invFun h
    _ = y := e.left_inv y

theorem la2Plain_inv_injective {A B : Type} (e : PlainEquiv A B) :
    Function.Injective e.invFun := by
  intro x y h
  calc
    x = e.toFun (e.invFun x) := (e.right_inv x).symm
    _ = e.toFun (e.invFun y) := congrArg e.toFun h
    _ = y := e.right_inv y

theorem la2Plain_to_surjective {A B : Type} (e : PlainEquiv A B) :
    Function.Surjective e.toFun := by
  intro y
  exact Exists.intro (e.invFun y) (e.right_inv y)

theorem la2Plain_inv_surjective {A B : Type} (e : PlainEquiv A B) :
    Function.Surjective e.invFun := by
  intro x
  exact Exists.intro (e.toFun x) (e.left_inv x)

theorem la2FiniteMap_injective_iff_surjective {m : Nat} {A B : Type}
    (eA : PlainEquiv (Fin m) A) (eB : PlainEquiv (Fin m) B) (f : A -> B) :
    Function.Injective f <-> Function.Surjective f := by
  let q : Fin m -> Fin m := fun i => eB.invFun (f (eA.toFun i))
  constructor
  case mp =>
    intro hf
    have hq_inj : Function.Injective q := by
      intro i j h
      apply la2Plain_to_injective eA
      apply hf
      apply la2Plain_inv_injective eB
      exact h
    have hq_surj : Function.Surjective q :=
      la2Fin_injective_surjective m q hq_inj
    intro b
    have hex := hq_surj (eB.invFun b)
    cases hex with
    | intro i hi =>
        refine Exists.intro (eA.toFun i) ?_
        have h := congrArg eB.toFun hi
        change eB.toFun (eB.invFun (f (eA.toFun i))) =
          eB.toFun (eB.invFun b) at h
        rw [eB.right_inv, eB.right_inv] at h
        exact h
  case mpr =>
    intro hf
    have hq_surj : Function.Surjective q := by
      intro j
      have hex := hf (eB.toFun j)
      cases hex with
      | intro a ha =>
          refine Exists.intro (eA.invFun a) ?_
          change eB.invFun (f (eA.toFun (eA.invFun a))) = j
          rw [eA.right_inv, ha]
          have hj := eB.left_inv j
          exact hj
    have hq_inj : Function.Injective q :=
      la2Fin_surjective_injective m q hq_surj
    intro a b hab
    have hq : q (eA.invFun a) = q (eA.invFun b) := by
      change eB.invFun (f (eA.toFun (eA.invFun a))) =
        eB.invFun (f (eA.toFun (eA.invFun b)))
      rw [eA.right_inv, eA.right_inv, hab]
    have hi := hq_inj hq
    calc
      a = eA.toFun (eA.invFun a) := (eA.right_inv a).symm
      _ = eA.toFun (eA.invFun b) := congrArg eA.toFun hi
      _ = b := eA.right_inv b
namespace window

variable {n : Nat} [NeZero n]

def xCodeToFin (c : XCode n) : Fin (2 * n) :=
  match c.odd with
  | false => Fin.mk c.rot.val (by omega)
  | true => Fin.mk (n + c.rot.val) (by omega)

def finToXCode (k : Fin (2 * n)) : XCode n :=
  if h : k.val < n then
    XCode.mk (Fin.mk k.val h) false
  else
    XCode.mk (Fin.mk (k.val - n) (by omega)) true

theorem xCodeToFin_finToXCode (k : Fin (2 * n)) :
    xCodeToFin (finToXCode k) = k := by
  unfold finToXCode
  by_cases h : k.val < n
  case pos =>
    simp [h, xCodeToFin]
  case neg =>
    simp [h, xCodeToFin]
    apply Fin.ext
    exact Nat.add_sub_of_le (Nat.le_of_not_gt h)

theorem finToXCode_xCodeToFin (c : XCode n) :
    finToXCode (xCodeToFin c) = c := by
  cases c with
  | mk r odd =>
      cases r with
      | mk v hv =>
          cases odd
          case false =>
            simp [xCodeToFin, finToXCode, hv]
          case true =>
            have hnot : Not (n + v < n) := by omega
            simp [xCodeToFin, finToXCode, hnot]

def xCodeFinEquiv : PlainEquiv (Fin (2 * n)) (XCode n) :=
  PlainEquiv.mk finToXCode xCodeToFin xCodeToFin_finToXCode finToXCode_xCodeToFin

end window
def la2PlainRefl (A : Type) : PlainEquiv A A :=
  PlainEquiv.mk (fun x => x) (fun x => x) (fun _ => rfl) (fun _ => rfl)

namespace window

variable {n : Nat} [NeZero n]

def powerSeedExponent (c : XCode n) : Nat :=
  2 * c.rot.val + if c.odd then 1 else 0

def powerSeedFin (c : XCode n) : Fin (2 * n) :=
  Fin.mk (powerSeedExponent c) (by
    cases c with
    | mk r odd =>
        cases odd <;> simp [powerSeedExponent] <;> omega)

def powerCode (c : XCode n) : XCode n :=
  XCode.mk (c.rot + c.rot + if c.odd then 1 else 0) c.odd

theorem xpowGn_powerSeed (c : XCode n) :
    xpowGn (n := n) (powerSeedExponent c) = xrep (powerCode c) := by
  cases c with
  | mk r odd =>
      cases odd
      case false =>
        apply Subtype.ext
        rw [xpowGn_val]
        change epow (X : En n) (2 * r.val) = _
        rw [epow_X_even]
        simp [powerCode, xrep, xrepEn, done_]
      case true =>
        apply Subtype.ext
        rw [xpowGn_val]
        change emul (epow (X : En n) (2 * r.val)) X = _
        rw [epow_X_even]
        simp [powerCode, xrep, xrepEn, X, emul, dmul,
          a1, q1, done_, fin_add_assoc]

theorem powerSeedFin_injective :
    Function.Injective (powerSeedFin (n := n)) := by
  intro c d h
  cases c with
  | mk r er =>
      cases d with
      | mk s es =>
          cases er <;> cases es
          case false.false =>
            have hv := congrArg Fin.val h
            simp [powerSeedFin, powerSeedExponent] at hv
            have hrs : r = s := by
              apply Fin.ext
              omega
            subst s
            rfl
          case false.true =>
            have hv := congrArg Fin.val h
            simp [powerSeedFin, powerSeedExponent] at hv
            omega
          case true.false =>
            have hv := congrArg Fin.val h
            simp [powerSeedFin, powerSeedExponent] at hv
            omega
          case true.true =>
            have hv := congrArg Fin.val h
            simp [powerSeedFin, powerSeedExponent] at hv
            have hrs : r = s := by
              apply Fin.ext
              omega
            subst s
            rfl

theorem powerSeedFin_surjective :
    Function.Surjective (powerSeedFin (n := n)) := by
  exact (la2FiniteMap_injective_iff_surjective
    (xCodeFinEquiv (n := n)) (la2PlainRefl (Fin (2 * n)))
    (powerSeedFin (n := n))).mp powerSeedFin_injective

end window
namespace window

variable {n : Nat} [NeZero n]

theorem finDouble_injective (hn : NatOdd n) :
    Function.Injective (fun r : Fin n => r + r) := by
  intro a b h
  cases hn with
  | intro m hm =>
      have hv := congrArg Fin.val h
      simp only [Fin.val_add] at hv
      have hmoda : (a.val + a.val) % n =
          if a.val + a.val < n then a.val + a.val else a.val + a.val - n := by
        by_cases ha : a.val + a.val < n
        case pos =>
          simp [ha, Nat.mod_eq_of_lt ha]
        case neg =>
          have hage : n <= a.val + a.val := Nat.le_of_not_gt ha
          have hrem : a.val + a.val - n < n := by omega
          have hh := Nat.mod_eq_sub_mod (a := a.val + a.val) (b := n) hage
          rw [Nat.mod_eq_of_lt hrem] at hh
          simp [ha, hh]
      have hmodb : (b.val + b.val) % n =
          if b.val + b.val < n then b.val + b.val else b.val + b.val - n := by
        by_cases hb : b.val + b.val < n
        case pos =>
          simp [hb, Nat.mod_eq_of_lt hb]
        case neg =>
          have hbge : n <= b.val + b.val := Nat.le_of_not_gt hb
          have hrem : b.val + b.val - n < n := by omega
          have hh := Nat.mod_eq_sub_mod (a := b.val + b.val) (b := n) hbge
          rw [Nat.mod_eq_of_lt hrem] at hh
          simp [hb, hh]
      rw [hmoda, hmodb] at hv
      by_cases ha : a.val + a.val < n
      case pos =>
        by_cases hb : b.val + b.val < n
        case pos =>
          simp [ha, hb] at hv
          apply Fin.ext
          omega
        case neg =>
          simp [ha, hb] at hv
          apply Fin.ext
          omega
      case neg =>
        by_cases hb : b.val + b.val < n
        case pos =>
          simp [ha, hb] at hv
          apply Fin.ext
          omega
        case neg =>
          simp [ha, hb] at hv
          apply Fin.ext
          omega

theorem powerCode_injective (hn : NatOdd n) :
    Function.Injective (powerCode (n := n)) := by
  intro c d h
  cases c with
  | mk r er =>
      cases d with
      | mk s es =>
          cases er <;> cases es
          case false.false =>
            have hr := congrArg XCode.rot h
            simp [powerCode] at hr
            have hrs := finDouble_injective hn hr
            subst s
            rfl
          case false.true =>
            have he := congrArg XCode.odd h
            exact Bool.noConfusion he
          case true.false =>
            have he := congrArg XCode.odd h
            exact Bool.noConfusion he
          case true.true =>
            have hr := congrArg XCode.rot h
            simp [powerCode] at hr
            have hr2 : r + r + 1 = s + s + 1 := by
              rw [fin_add_assoc, fin_add_assoc]
              exact hr
            have hd : r + r = s + s :=
              fin_add_right_cancel 1 (r + r) (s + s) hr2
            have hrs := finDouble_injective hn hd
            subst s
            rfl

theorem powerCode_surjective (hn : NatOdd n) :
    Function.Surjective (powerCode (n := n)) := by
  exact (la2FiniteMap_injective_iff_surjective
    (xCodeFinEquiv (n := n)) (xCodeFinEquiv (n := n))
    (powerCode (n := n))).mp (powerCode_injective hn)

theorem bounded_power_eq_xrep (k : Fin (2 * n)) :
    Exists (fun c : XCode n => xpowGn (n := n) k.val = xrep c) := by
  have hex := powerSeedFin_surjective (n := n) k
  cases hex with
  | intro c hc =>
      refine Exists.intro (powerCode c) ?_
      have hp := xpowGn_powerSeed c
      have hval := congrArg Fin.val hc
      change powerSeedExponent c = k.val at hval
      rw [hval] at hp
      exact hp

theorem xrep_eq_bounded_power (hn : NatOdd n) (c : XCode n) :
    Exists (fun k : Fin (2 * n) => xrep c = xpowGn (n := n) k.val) := by
  have hex := powerCode_surjective hn c
  cases hex with
  | intro d hd =>
      refine Exists.intro (powerSeedFin d) ?_
      rw [hd.symm]
      exact (xpowGn_powerSeed d).symm

end window
namespace window

variable {n : Nat} [NeZero n]

theorem xpowGn_add (a b : Nat) :
    xpowGn (n := n) (a + b) = xpowGn (n := n) a * xpowGn (n := n) b := by
  induction b with
  | zero =>
      change xpowGn (n := n) a = xpowGn (n := n) a * 1
      exact (Gn_groupLaws.mul_one _).symm
  | succ b ih =>
      change xpowGn (n := n) (a + b) * Xg =
        xpowGn (n := n) a * (xpowGn (n := n) b * Xg)
      rw [ih]
      exact Gn_groupLaws.mul_assoc _ _ _

theorem xpowGn_period_mul (h3 : 3 <= n) (hn : NatOdd n) (q : Nat) :
    xpowGn (n := n) ((2 * n) * q) = 1 := by
  have hperiod : xpowGn (n := n) (2 * n) = 1 :=
    (Gn_ord_X (by omega) hn).1
  induction q with
  | zero =>
      rfl
  | succ q ih =>
      rw [Nat.mul_succ]
      rw [xpowGn_add, ih, hperiod]
      exact Gn_groupLaws.one_mul 1

theorem xpowGn_mod_period (h3 : 3 <= n) (hn : NatOdd n) (k : Nat) :
    xpowGn (n := n) k = xpowGn (n := n) (k % (2 * n)) := by
  have hdecomp : k = (2 * n) * (k / (2 * n)) + k % (2 * n) := by
    calc
      k = k % (2 * n) + (2 * n) * (k / (2 * n)) :=
        (Nat.mod_add_div k (2 * n)).symm
      _ = (2 * n) * (k / (2 * n)) + k % (2 * n) := Nat.add_comm _ _
  calc
    xpowGn (n := n) k =
        xpowGn (n := n) ((2 * n) * (k / (2 * n)) + k % (2 * n)) :=
      congrArg (xpowGn (n := n)) hdecomp
    _ = xpowGn (n := n) ((2 * n) * (k / (2 * n))) *
        xpowGn (n := n) (k % (2 * n)) := xpowGn_add _ _
    _ = 1 * xpowGn (n := n) (k % (2 * n)) :=
      congrArg (fun z : Gn n => z * xpowGn (n := n) (k % (2 * n)))
        (xpowGn_period_mul h3 hn _)
    _ = xpowGn (n := n) (k % (2 * n)) :=
      (Gn_groupLaws (n := n)).one_mul _

def InXPowers (g : Gn n) : Prop :=
  Exists (fun k : Fin (2 * n) => g = xpowGn (n := n) k.val)

theorem genX_iff_InXPowers (h3 : 3 <= n) (hn : NatOdd n) (g : Gn n) :
    genX g <-> InXPowers g := by
  constructor
  case mp =>
    intro hg
    cases hg with
    | intro k hk =>
        have hpos : 0 < 2 * n := by
          have hn0 := NeZero.ne n
          omega
        let r : Fin (2 * n) := Fin.mk (k % (2 * n)) (Nat.mod_lt k hpos)
        refine Exists.intro r ?_
        calc
          g = xpowGn (n := n) k := hk
          _ = xpowGn (n := n) (k % (2 * n)) := xpowGn_mod_period h3 hn k
          _ = xpowGn (n := n) r.val := rfl
  case mpr =>
    intro hg
    cases hg with
    | intro k hk =>
        exact Exists.intro k.val hk

theorem InXPowers_iff_exists_xrep (hn : NatOdd n) (g : Gn n) :
    InXPowers g <-> Exists (fun c : XCode n => g = xrep c) := by
  constructor
  case mp =>
    intro hg
    cases hg with
    | intro k hk =>
        have hex := bounded_power_eq_xrep k
        cases hex with
        | intro c hc =>
            refine Exists.intro c ?_
            exact hk.trans hc
  case mpr =>
    intro hg
    cases hg with
    | intro c hc =>
        have hex := xrep_eq_bounded_power hn c
        cases hex with
        | intro k hk =>
            refine Exists.intro k ?_
            exact hc.trans hk

theorem genX_iff_exists_xrep (h3 : 3 <= n) (hn : NatOdd n) (g : Gn n) :
    genX g <-> Exists (fun c : XCode n => g = xrep c) := by
  exact (genX_iff_InXPowers h3 hn g).trans (InXPowers_iff_exists_xrep hn g)

end window
namespace window

variable {n : Nat} [NeZero n]

def xZero : XCode n := XCode.mk 0 false

theorem xrep_xZero : xrep (xZero (n := n)) = 1 := by
  apply Subtype.ext
  rfl

theorem xrep_injective : Function.Injective (xrep (n := n)) := by
  intro c d h
  cases c with
  | mk r er =>
      cases d with
      | mk s es =>
          have hv := congrArg Subtype.val h
          cases er <;> cases es <;>
            simp [xrep, xrepEn] at hv <;> simp_all

def xCodeDiv (c d : XCode n) : XCode n :=
  XCode.mk (d.rot - c.rot) (xor c.odd d.odd)

theorem xrep_inv_mul (c d : XCode n) :
    Inv.inv (xrep c) * xrep d = xrep (xCodeDiv c d) := by
  apply Subtype.ext
  change emul (einv (xrepEn c)) (xrepEn d) = xrepEn (xCodeDiv c d)
  cases c with
  | mk r er =>
      cases d with
      | mk s es =>
          cases er <;> cases es <;>
            simp [xrepEn, xCodeDiv, einv, dinv, emul, dmul,
              fin_sub_eq_add_neg, fin_add_comm]

theorem eq_of_inv_mul_eq_one (a b : Gn n) (h : Inv.inv a * b = 1) : a = b := by
  calc
    a = a * 1 := ((Gn_groupLaws (n := n)).mul_one a).symm
    _ = a * (Inv.inv a * b) := congrArg (fun z : Gn n => a * z) h.symm
    _ = (a * Inv.inv a) * b :=
      ((Gn_groupLaws (n := n)).mul_assoc a (Inv.inv a) b).symm
    _ = 1 * b := congrArg (fun z : Gn n => z * b)
      ((Gn_groupLaws (n := n)).mul_inv a)
    _ = b := (Gn_groupLaws (n := n)).one_mul b

end window
namespace window

variable {n : Nat} [NeZero n]

theorem leftCoset_mul_right_eq {H0 : Gn n -> Prop} (hs : IsSubgrp H0)
    (a h : Gn n) (hh : H0 h) :
    leftCoset H0 (a * h) = leftCoset H0 a := by
  apply funext
  intro x
  apply propext
  constructor
  case mp =>
    intro hx
    cases hx with
    | intro u hu =>
        cases hu with
        | intro hHu hxu =>
            refine Exists.intro (h * u) (And.intro (hs.mul_mem hh hHu) ?_)
            calc
              x = (a * h) * u := hxu
              _ = a * (h * u) := (Gn_groupLaws (n := n)).mul_assoc _ _ _
  case mpr =>
    intro hx
    cases hx with
    | intro u hu =>
        cases hu with
        | intro hHu hxu =>
            refine Exists.intro (Inv.inv h * u)
              (And.intro (hs.mul_mem (hs.inv_mem hh) hHu) ?_)
            calc
              x = a * u := hxu
              _ = a * (1 * u) := congrArg (fun z : Gn n => a * z)
                ((Gn_groupLaws (n := n)).one_mul u).symm
              _ = a * ((h * Inv.inv h) * u) :=
                congrArg (fun z : Gn n => a * (z * u))
                  ((Gn_groupLaws (n := n)).mul_inv h).symm
              _ = a * (h * (Inv.inv h * u)) :=
                congrArg (fun z : Gn n => a * z)
                  ((Gn_groupLaws (n := n)).mul_assoc h (Inv.inv h) u)
              _ = (a * h) * (Inv.inv h * u) :=
                ((Gn_groupLaws (n := n)).mul_assoc a h (Inv.inv h * u)).symm

theorem inv_mul_mem_of_leftCoset_eq {H0 : Gn n -> Prop} (hs : IsSubgrp H0)
    (a b : Gn n) (heq : leftCoset H0 a = leftCoset H0 b) :
    H0 (Inv.inv a * b) := by
  have hb : leftCoset H0 b b := by
    exact Exists.intro 1 (And.intro hs.one_mem ((Gn_groupLaws (n := n)).mul_one b).symm)
  have ha : leftCoset H0 a b := by
    rw [heq]
    exact hb
  cases ha with
  | intro h hh =>
      cases hh with
      | intro hH hbh =>
          have hd : Inv.inv a * b = h := by
            calc
              Inv.inv a * b = Inv.inv a * (a * h) :=
                congrArg (fun z : Gn n => Inv.inv a * z) hbh
              _ = (Inv.inv a * a) * h :=
                ((Gn_groupLaws (n := n)).mul_assoc (Inv.inv a) a h).symm
              _ = 1 * h := congrArg (fun z : Gn n => z * h)
                ((Gn_groupLaws (n := n)).inv_mul a)
              _ = h := (Gn_groupLaws (n := n)).one_mul h
          rw [hd]
          exact hH

end window
namespace window

variable {n : Nat} [NeZero n]

def orbitCoset (H0 : Gn n -> Prop) (c : XCode n) : LeftCosets H0 :=
  Subtype.mk (leftCoset H0 (xrep c)) (Exists.intro (xrep c) rfl)

theorem orbitCoset_surjective_iff_Transitive {H0 : Gn n -> Prop}
    (hs : IsSubgrp H0) :
    Function.Surjective (orbitCoset H0) <-> Transitive H0 := by
  constructor
  case mp =>
    intro horbit g
    let K : LeftCosets H0 :=
      Subtype.mk (leftCoset H0 g) (Exists.intro g rfl)
    have hex := horbit K
    cases hex with
    | intro c hc =>
        have hp : leftCoset H0 (xrep c) = leftCoset H0 g :=
          congrArg Subtype.val hc
        have hgg : leftCoset H0 g g :=
          Exists.intro 1
            (And.intro hs.one_mem ((Gn_groupLaws (n := n)).mul_one g).symm)
        have hgc : leftCoset H0 (xrep c) g := by
          rw [hp]
          exact hgg
        cases hgc with
        | intro h hh =>
            cases hh with
            | intro hH hfac =>
                exact Exists.intro c (Exists.intro h (And.intro hH hfac))
  case mpr =>
    intro htrans K
    cases K.property with
    | intro g hK =>
        have htg := htrans g
        cases htg with
        | intro c hrest =>
            cases hrest with
            | intro h hdata =>
                cases hdata with
                | intro hH hfac =>
                    refine Exists.intro c ?_
                    apply Subtype.ext
                    change leftCoset H0 (xrep c) = K.val
                    calc
                      leftCoset H0 (xrep c) = leftCoset H0 (xrep c * h) :=
                        (leftCoset_mul_right_eq hs (xrep c) h hH).symm
                      _ = leftCoset H0 g :=
                        congrArg (leftCoset H0) hfac.symm
                      _ = K.val := hK.symm

theorem orbitCoset_injective_iff_TrivialInter {H0 : Gn n -> Prop}
    (hs : IsSubgrp H0) :
    Function.Injective (orbitCoset H0) <-> TrivialInter H0 := by
  constructor
  case mp =>
    intro horbit c hc
    have hcos : leftCoset H0 (xrep c) = leftCoset H0 1 := by
      calc
        leftCoset H0 (xrep c) = leftCoset H0 (1 * xrep c) :=
          congrArg (leftCoset H0) ((Gn_groupLaws (n := n)).one_mul (xrep c)).symm
        _ = leftCoset H0 1 := leftCoset_mul_right_eq hs 1 (xrep c) hc
    have heq : orbitCoset H0 c = orbitCoset H0 (xZero (n := n)) := by
      apply Subtype.ext
      change leftCoset H0 (xrep c) = leftCoset H0 (xrep (xZero (n := n)))
      rw [xrep_xZero]
      exact hcos
    exact horbit heq
  case mpr =>
    intro htriv c d hcd
    have hcos : leftCoset H0 (xrep c) = leftCoset H0 (xrep d) :=
      congrArg Subtype.val hcd
    have hmem : H0 (Inv.inv (xrep c) * xrep d) :=
      inv_mul_mem_of_leftCoset_eq hs (xrep c) (xrep d) hcos
    have hdiv : H0 (xrep (xCodeDiv c d)) := by
      rw [xrep_inv_mul] at hmem
      exact hmem
    have hzero := htriv (xCodeDiv c d) hdiv
    have hone : Inv.inv (xrep c) * xrep d = 1 := by
      rw [xrep_inv_mul, hzero]
      exact xrep_xZero
    exact xrep_injective (eq_of_inv_mul_eq_one (xrep c) (xrep d) hone)

end window
namespace window

variable {n : Nat} [NeZero n]

/-- The paper P3: the actual cyclic subgroup generated by X is transitive on left cosets. -/
def CyclicTransitive (H0 : Gn n -> Prop) : Prop :=
  forall g : Gn n, Exists (fun x : Gn n =>
    genX x /\ Exists (fun h : Gn n => H0 h /\ g = x * h))

/-- The paper intersection condition: the actual subgroup generated by X meets H trivially. -/
def CyclicTrivialInter (H0 : Gn n -> Prop) : Prop :=
  forall x : Gn n, genX x -> H0 x -> x = 1

theorem cyclicTransitive_iff_Transitive (h3 : 3 <= n) (hn : NatOdd n)
    (H0 : Gn n -> Prop) : CyclicTransitive H0 <-> Transitive H0 := by
  constructor
  case mp =>
    intro hcyc g
    have hg := hcyc g
    cases hg with
    | intro x hx =>
        cases hx with
        | intro hxpow hrest =>
            have hcode := (genX_iff_exists_xrep h3 hn x).mp hxpow
            cases hcode with
            | intro c hc =>
                cases hrest with
                | intro h hh =>
                    cases hh with
                    | intro hH hfac =>
                        refine Exists.intro c (Exists.intro h (And.intro hH ?_))
                        rw [hc] at hfac
                        exact hfac
  case mpr =>
    intro htrans g
    have hg := htrans g
    cases hg with
    | intro c hrest =>
        cases hrest with
        | intro h hh =>
            cases hh with
            | intro hH hfac =>
                refine Exists.intro (xrep c) (And.intro ?_
                  (Exists.intro h (And.intro hH hfac)))
                apply (genX_iff_exists_xrep h3 hn (xrep c)).mpr
                exact Exists.intro c rfl

theorem cyclicTrivialInter_iff_TrivialInter (h3 : 3 <= n) (hn : NatOdd n)
    (H0 : Gn n -> Prop) : CyclicTrivialInter H0 <-> TrivialInter H0 := by
  constructor
  case mp =>
    intro hcyc c hc
    have hxpow : genX (xrep c) := by
      apply (genX_iff_exists_xrep h3 hn (xrep c)).mpr
      exact Exists.intro c rfl
    have hone := hcyc (xrep c) hxpow hc
    apply xrep_injective
    calc
      xrep c = 1 := hone
      _ = xrep (xZero (n := n)) := xrep_xZero.symm
  case mpr =>
    intro htriv x hxpow hxH
    have hcode := (genX_iff_exists_xrep h3 hn x).mp hxpow
    cases hcode with
    | intro c hc =>
        have hcH : H0 (xrep c) := by
          rw [hc.symm]
          exact hxH
        have hzero := htriv c hcH
        calc
          x = xrep c := hc
          _ = xrep (xZero (n := n)) := congrArg xrep hzero
          _ = 1 := xrep_xZero

theorem coded_transitive_iff_trivial_inter (H0 : Gn n -> Prop)
    (iw : Index2nWitness H0) : Transitive H0 <-> TrivialInter H0 := by
  have hfinite := la2FiniteMap_injective_iff_surjective
    (xCodeFinEquiv (n := n)) iw.cosetEquiv (orbitCoset H0)
  constructor
  case mp =>
    intro htrans
    have hsurj := (orbitCoset_surjective_iff_Transitive iw.isSubgroup).mpr htrans
    have hinj := hfinite.mpr hsurj
    exact (orbitCoset_injective_iff_TrivialInter iw.isSubgroup).mp hinj
  case mpr =>
    intro htriv
    have hinj := (orbitCoset_injective_iff_TrivialInter iw.isSubgroup).mpr htriv
    have hsurj := hfinite.mp hinj
    exact (orbitCoset_surjective_iff_Transitive iw.isSubgroup).mp hsurj

/-- LA-2 / oddH Lemma C(2), with the paper hypotheses and the exact P1 witness.
The left side is the actual action of the cyclic subgroup generated by X, not a code action. -/
theorem transitive_iff_trivial_inter (h3 : 3 <= n) (hn : NatOdd n)
    (H0 : Gn n -> Prop) (iw : Index2nWitness H0) :
    CyclicTransitive H0 <-> CyclicTrivialInter H0 := by
  constructor
  case mp =>
    intro hp3
    have ht := (cyclicTransitive_iff_Transitive h3 hn H0).mp hp3
    have hi := (coded_transitive_iff_trivial_inter H0 iw).mp ht
    exact (cyclicTrivialInter_iff_TrivialInter h3 hn H0).mpr hi
  case mpr =>
    intro hi
    have hit := (cyclicTrivialInter_iff_TrivialInter h3 hn H0).mp hi
    have ht := (coded_transitive_iff_trivial_inter H0 iw).mpr hit
    exact (cyclicTransitive_iff_Transitive h3 hn H0).mpr ht

end window
namespace window

variable {n : Nat} [NeZero n]

def XPowerCarrier : Type := Subtype (fun x : Gn n => genX x)

def cyclicOrbitCoset (H0 : Gn n -> Prop) (x : XPowerCarrier (n := n)) :
    LeftCosets H0 :=
  Subtype.mk (leftCoset H0 x.val) (Exists.intro x.val rfl)

theorem cyclicTransitive_iff_leftCosetAction {H0 : Gn n -> Prop}
    (hs : IsSubgrp H0) :
    CyclicTransitive H0 <-> Function.Surjective (cyclicOrbitCoset H0) := by
  constructor
  case mp =>
    intro htrans K
    cases K.property with
    | intro g hK =>
        have hg := htrans g
        cases hg with
        | intro x hx =>
            cases hx with
            | intro hxpow hrest =>
                cases hrest with
                | intro h hh =>
                    cases hh with
                    | intro hH hfac =>
                        let xp : XPowerCarrier (n := n) := Subtype.mk x hxpow
                        refine Exists.intro xp ?_
                        apply Subtype.ext
                        change leftCoset H0 x = K.val
                        calc
                          leftCoset H0 x = leftCoset H0 (x * h) :=
                            (leftCoset_mul_right_eq hs x h hH).symm
                          _ = leftCoset H0 g := congrArg (leftCoset H0) hfac.symm
                          _ = K.val := hK.symm
  case mpr =>
    intro horbit g
    let K : LeftCosets H0 :=
      Subtype.mk (leftCoset H0 g) (Exists.intro g rfl)
    have hex := horbit K
    cases hex with
    | intro xp hxp =>
        have hp : leftCoset H0 xp.val = leftCoset H0 g :=
          congrArg Subtype.val hxp
        have hgg : leftCoset H0 g g :=
          Exists.intro 1
            (And.intro hs.one_mem ((Gn_groupLaws (n := n)).mul_one g).symm)
        have hgx : leftCoset H0 xp.val g := by
          rw [hp]
          exact hgg
        cases hgx with
        | intro h hh =>
            cases hh with
            | intro hH hfac =>
                exact Exists.intro xp.val
                  (And.intro xp.property (Exists.intro h (And.intro hH hfac)))

end window
