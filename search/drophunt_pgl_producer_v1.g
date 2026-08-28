#############################################################################
## drophunt_pgl_producer_v1.g -- PGammaL(2,8) window valid=9 re-derivation.
## Step (a) [point-index convention] CONFIRMED MATCHING search/gaplib
## week3-psl-common.g's MatToPermGF8 (point 1=infinity, point 2+x=field
## element x, GF(8) encoding a0+2a1+4a2 poly x^3+x+1) against
## search/pgl28_independent_window_producer_v1.py's matrix_perm (index0=
## infinity, index(1+x)=field element x, SAME GF8 encoding/poly) --
## converting Python's 0-index to GAP's 1-index by adding 1 throughout
## reproduces GAP's formula exactly (images[1]=1 if c=0 else 2+GF8Mul(a,
## GF8Inv(c)); images[2+x]=1 if den=0 else 2+GF8Mul(num,GF8Inv(den))).
##
## Steps (b)-(e): the reference producer does NOT reduce E's structure onto
## M via a group homomorphism -- it runs E's OWN self-contained GT(E)-style
## hexagon/onto check (m mod 9, f ranging over DerivedSubgroup(E)=PSL(2,8),
## theta=Ad(s), tau=Ad(t) for a FRESH marked pair s(order 2),t(order 3)
## found by search within E, generating E itself -- NOT reusing this
## script's own PSL(2,8)-only x4,y4), then JOINS against the pre-existing
## 972-row M-target roster purely via matching m mod 9 (since E and M's own
## f-parts have no common quotient, the join multiplies through uniformly:
## every M-target with a given m mod 9 gets fibre_size = |component_pass[m]|).
## So valid=9 reduces to: is |component_pass[m]|=9 for every charming m in
## {0,2,3,5,6,8} (mod 9), inside E alone -- no M-joint permutation group is
## needed at all.
#############################################################################

Read("search/drophunt_checker_producer_v2.g");;

DPGT0 := GAPLIB_WallElapsedMs();;

## Frobenius permutation on the SAME 9 points as DCP2X4/DCP2Y4 (point 1 =
## infinity, point 2+x = field element x, matching MatToPermGF8's own
## convention exactly -- both this producer's roof-M PSL(2,8) block and this
## Frobenius live on IDENTICAL points, so E:=Group(DCP2X4,DCP2Y4,FR) is
## well-defined on the same 9-point domain).
DPGFRImages := [];;
DPGFRImages[1] := 1;;
for DPGx in [0..7] do
  DPGFRImages[2+DPGx] := 2 + GF8Mul(DPGx, DPGx);;
od;;
DPGFR := PermList(DPGFRImages);;
Print("DPG_FROBENIUS_ORDER=", Order(DPGFR), "  <- expect 3\n");;
if Order(DPGFR) <> 3 then Error("DPG: Frobenius order drift"); fi;;

DPGE := Group(DCP2X4, DCP2Y4, DPGFR);;
DPGESize := Size(DPGE);;
Print("DPG_E_ORDER=", DPGESize, "  <- expect 1512\n");;
if DPGESize <> 1512 then Error("DPG: E=PGammaL(2,8) order drift"); fi;;

DPGDerivedE := DerivedSubgroup(DPGE);;
Print("DPG_DERIVED_E_ORDER=", Size(DPGDerivedE), "  <- expect 504\n");;
if Size(DPGDerivedE) <> 504 then Error("DPG: derived subgroup order drift"); fi;;

#############################################################################
## Search for marked (s,t): s order 2, t order 3 in E, satisfying (ported
## verbatim in logic from search/pgl28_independent_window_producer_v1.py's
## main() marking search):
##   w := s*t^-1 ; x := w^2 ; require Order(x)=9
##   y := s^-1*x*s ; y_via_t := t^-1*x*t ; z := (t^2)^-1*x*t^2
##   w2 := t^-1*s
##   require y=y_via_t and z*y*x=Identity and w2^2=y
##   require <s,t>=E and <x,y>=E (order 1512 each)
#############################################################################
DPGSCands := Filtered(Elements(DPGE), g -> Order(g) = 2);;
DPGTCands := Filtered(Elements(DPGE), g -> Order(g) = 3);;
Print("DPG_S_CANDIDATES=", Length(DPGSCands), " T_CANDIDATES=", Length(DPGTCands), "\n");;

DPGSelected := fail;;
DPGTriedPairs := 0;;
for DPGs in DPGSCands do
  if DPGSelected <> fail then break; fi;;
  for DPGt in DPGTCands do
    DPGTriedPairs := DPGTriedPairs + 1;;
    DPGw := DPGs * DPGt^-1;;
    if not (Order(DPGw) in [9,18]) then continue; fi;;
    DPGx := DPGw^2;;
    if Order(DPGx) <> 9 then continue; fi;;
    DPGy := DPGs^-1 * DPGx * DPGs;;
    DPGyViaT := DPGt^-1 * DPGx * DPGt;;
    DPGz := (DPGt^2)^-1 * DPGx * DPGt^2;;
    DPGw2 := DPGt^-1 * DPGs;;
    if not (DPGy = DPGyViaT and DPGz*DPGy*DPGx = Identity(DPGE) and DPGw2^2 = DPGy) then continue; fi;;
    if Size(Group(DPGs,DPGt)) <> 1512 then continue; fi;;
    if Size(Group(DPGx,DPGy)) <> 1512 then continue; fi;;
    DPGSelected := rec(s:=DPGs, t:=DPGt, w:=DPGw, x:=DPGx, y:=DPGy, z:=DPGz, w2:=DPGw2);;
    break;;
  od;;
od;;
Print("DPG_TRIED_PAIRS=", DPGTriedPairs, " elapsed_ms=", GAPLIB_WallElapsedMs()-DPGT0, "\n");;
if DPGSelected = fail then Error("DPG: PGL28_MARKING_NOT_FOUND -- fail-closed stop"); fi;;
Print("DPG_MARKING_FOUND\n");;

DPGs := DPGSelected.s;; DPGt := DPGSelected.t;;
DPGx := DPGSelected.x;; DPGy := DPGSelected.y;;

#############################################################################
## Component computation: for m in charming(mod 9) = {0,2,3,5,6,8}, for f in
## DerivedSubgroup(E) (504 elements), evaluate theta=Ad(s), tau=Ad(t)
## group-element-level (E is self-contained -- no word-level anything, no
## c-twist issue: this is a plain finite-group GT-style check inside E).
#############################################################################
DPGCharming := [0,2,3,5,6,8];;
DPGDerivedElts := Elements(DPGDerivedE);;
DPGComponentPass := rec();;
for DPGm in DPGCharming do
  DPGPassList := [];;
  for DPGf in DPGDerivedElts do
    DPGThetaF := DPGs^-1 * DPGf * DPGs;;
    if DPGThetaF * DPGf <> Identity(DPGE) then continue; fi;;
    DPGu := 2*DPGm + 1;;
    DPGymf := DPGf * DPGy^DPGm;;
    DPGTauYmf := DPGt^-1 * DPGymf * DPGt;;
    DPGTau2Ymf := DPGt^-1 * DPGTauYmf * DPGt;;
    if DPGymf * DPGTauYmf * DPGTau2Ymf <> Identity(DPGE) then continue; fi;;
    DPGGenA := DPGx^DPGu;;
    DPGGenB := DPGf * DPGy^DPGu * DPGf^-1;;
    if Size(Group(DPGGenA, DPGGenB)) <> DPGESize then continue; fi;;
    Add(DPGPassList, DPGf);;
  od;;
  DPGComponentPass.(String(DPGm)) := DPGPassList;;
  Print("DPG_COMPONENT m=", DPGm, " pass_count=", Length(DPGPassList), "  <- expect 9\n");;
od;;

DPGAllNine := ForAll(DPGCharming, m -> Length(DPGComponentPass.(String(m))) = 9);;
Print("DPG_ALL_M_GIVE_9=", DPGAllNine, "\n");;

DPGTotalElapsed := GAPLIB_WallElapsedMs() - DPGT0;;
Print("DPG_TOTAL_ELAPSED_MS=", DPGTotalElapsed, "\n");;

DPGCountsJson := JoinC(List(DPGCharming, m -> Concatenation(
  "{\"m\":", String(m), ",\"pass_count\":", String(Length(DPGComponentPass.(String(m)))), "}")), ",\n");;

DPGOutput := Concatenation(
  "{\n  \"schema\":\"drophunt-pgl-rederivation/v1\",\n",
  "  \"point_index_convention_check\":\"MATCHES (GAP MatToPermGF8 vs Python matrix_perm, same GF8 encoding/poly, 1-index offset only)\",\n",
  "  \"frobenius_order\":", String(Order(DPGFR)), ",\n",
  "  \"E_order\":", String(DPGESize), ",\n",
  "  \"derived_E_order\":", String(Size(DPGDerivedE)), ",\n",
  "  \"marking_found\":true,\n",
  "  \"tried_pairs\":", String(DPGTriedPairs), ",\n",
  "  \"component_pass_counts\":[\n", DPGCountsJson, "\n  ],\n",
  "  \"all_charming_m_give_9\":", JB(DPGAllNine), ",\n",
  "  \"expected_valid\":9,\n",
  "  \"total_elapsed_ms\":", String(DPGTotalElapsed), "\n}\n");;
WriteFile("search/certs/drophunt_pgl_rederivation_v1_20260828.json", DPGOutput);;
Print("DPG_OUTPUT path=search/certs/drophunt_pgl_rederivation_v1_20260828.json\n");;
Print("ALL_DONE\n");;
