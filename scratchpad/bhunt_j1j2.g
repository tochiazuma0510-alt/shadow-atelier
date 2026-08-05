## scratchpad/bhunt_j1j2.g
## B-HUNT J1' (Phi-invariance of L=ker(D|_A)) + J2 (identification of C, order-6
## subgroup through anchor c=[6,1]) per docs/notes/bhunt_prereg_iffirst_v1.md.
## Reuses the SAME group construction as the frozen main-run lanes (P built via
## predicate_lib_laneS.g -> PQ_OUTPUT_P.g; candidate-key basis via
## candidate_key_lib.g BasisFromP). Reads the J0 join output
## (scratchpad/bhunt_j0_output.json, already produced by
## scratchpad/bhunt_j0_join.py from existing artifacts, zero new window
## computation there) for the 7-element sets L (m=0) and pent(m0=1).
##
## E_{m,f}(x)=x^{2m+1}, E_{m,f}(y)=f^-1*y^{2m+1}*f  (2401 (3.41), 2405 (2.6)).
## Phi := E_{m,f}|_{gamma3(P)} is the conjugation action on A (CONJ-Phi,
## addendum A Sec 4). Composition [m1,f1] o [m2,f2] = [2 m1 m2+m1+m2, f1
## E_{m1,f1}(f2)] (2405 (2.6)/2401 (3.43)).

Read("search/probe/wac_v1/gap_output_prelude.g");

if not IsBound(J0_INPUT_PATH) then Error("BHUNT_STOP: J0_INPUT_PATH must be bound"); fi;
if not IsBound(OUT_PATH) then Error("BHUNT_STOP: OUT_PATH must be bound"); fi;

Read("search/probe/hsp7_mainrun/predicate_lib_laneS.g");
Read("search/probe/hsp7_mainrun/candidate_key_lib.g");

if not CandidateKeyLibSelfCheck().ok then Error("BHUNT_STOP: candidate key self-check failed"); fi;
basis := BasisFromP(P);;
if not CandidateBasisSemanticSelfCheck(basis).ok then
  Error("BHUNT_STOP: group-level candidate-key semantic gate failed");
fi;
if theta = fail or tau = fail or not IsBijective(theta) or not IsBijective(tau) then
  Error("BHUNT_STOP: theta/tau failed explicit well-defined+bijection gate");
fi;

## ---- read J0 join input (L and pent(m0=1) exponent-vector lists) ----
Read(J0_INPUT_PATH);
## The file J0_INPUT_PATH must bind: L_EVECS (list of 6-int lists, expect 7),
## PENT_M1_EVECS (list of 6-int lists, expect 7), M0 (integer, expect 1),
## C_M (integer, expect 6), C_E (list of 6 ints, expect [0,0,0,0,0,0]).
if not IsBound(L_EVECS) or not IsBound(PENT_M1_EVECS) or not IsBound(M0)
   or not IsBound(C_M) or not IsBound(C_E) then
  Error("BHUNT_STOP: J0 input file missing required bindings");
fi;
if Length(L_EVECS) <> 7 then Error("BHUNT_STOP: |L| != 7, got ", Length(L_EVECS)); fi;
if Length(PENT_M1_EVECS) <> 7 then Error("BHUNT_STOP: |pent(m0)| != 7, got ", Length(PENT_M1_EVECS)); fi;

## ---- element construction from exponent vectors, via the SAME basis/pcgs
## the main-run lanes used (BasisFromP(P) above) ----
L_ELTS := List(L_EVECS, e -> ExpVectorToElement(basis, e));;
PENT_M1_ELTS := List(PENT_M1_EVECS, e -> ExpVectorToElement(basis, e));;

## sanity: L must be a subgroup of D (closed, contains identity) -- own
## measurement, cheap (7x7 multiplication table), not assumed.
idElt := One(P);;
if not (idElt in L_ELTS) then Error("BHUNT_STOP: identity not found in L (unexpected)"); fi;
LClosed := true;;
for aa in L_ELTS do
  for bb in L_ELTS do
    if not (aa*bb in L_ELTS) then LClosed := false; fi;
  od;
od;
Print("own_measurement: L closed under P-multiplication (subgroup check)? ", LClosed, "\n");

## ---- E_{m,f} builder: x->x^(2m+1), y->f^-1 y^(2m+1) f, as an endomorphism of P ----
BuildE := function(m, fElt)
  local u, imgx, imgy, phi;
  u := 2*m+1;
  imgx := x^u;
  imgy := fElt^-1 * y^u * fElt;
  phi := GroupHomomorphismByImages(P, P, [x,y], [imgx, imgy]);
  return phi;
end;;

## ---- J1': measure Phi = E_{M0, f0}|_{gamma3(P)} for f0 = first pent(m0) elt ----
f0 := PENT_M1_ELTS[1];;
PhiM := BuildE(M0, f0);;
if PhiM = fail then Error("BHUNT_STOP: E_{m0,f0} not well-defined (GroupHomomorphismByImages failed)"); fi;
PhiBijective := IsBijective(PhiM);;
Print("own_measurement: Phi = E_{m0,f0} well-defined? ", PhiM <> fail, "\n");
Print("own_measurement: Phi bijective? ", PhiBijective, "\n");

PhiImages := [];;
PhiInvariant := true;;
for i in [1..7] do
  hh := L_ELTS[i];;
  PhiH := ImageElm(PhiM, hh);;
  eImg := ExponentsOfPcElement(basis.pcgsD, PhiH);;
  inD := (eImg <> fail);;
  inL := inD and (eImg in L_EVECS);;
  if not inL then PhiInvariant := false; fi;
  Add(PhiImages, rec(h_e := L_EVECS[i], phi_h_in_D := inD,
                      phi_h_e := eImg, phi_h_in_L := inL));
od;
Print("own_measurement: Phi(L) subset D for all 7? ", ForAll(PhiImages, r -> r.phi_h_in_D), "\n");
Print("own_measurement: Phi(L) = L (Phi-invariance)? ", PhiInvariant, "\n");

## ---- J2: find the unique f0c in pent(m0) with [m0,f0c]^3 = c = [C_M, C_E] ----
## g = [m0,f0c]; g^2 = [m1, f0c*E_{m0,f0c}(f0c)]  (m1 = 2*m0^2+2*m0)
## g^3 = g^2 . g = [2*m1*m0+m1+m0, f1p * E_{m1,f1p}(f0c)]
cElt := ExpVectorToElement(basis, C_E);;  ## identity of P when C_E is all-zero
m1 := 2*M0*M0 + M0 + M0;;
m3raw := 2*m1*M0 + m1 + M0;;
m3mod := m3raw mod 7;;
Print("own_measurement: m3 (raw) = ", m3raw, "  m3 mod 7 = ", m3mod, "  expect C_M=", C_M, "\n");
if m3mod <> C_M then
  Error("BHUNT_STOP: m-component of cube does not match anchor c's m-component; ",
        "BH-3 preconditions violated (SUP-1/SUP-2 chi_vir homomorphism check failed)");
fi;

CCandidates := [];;
for i in [1..7] do
  f0c := PENT_M1_ELTS[i];;
  PhiC := BuildE(M0, f0c);;
  if PhiC = fail then Error("BHUNT_STOP: E_{m0,f0c} not well-defined for candidate ", i); fi;
  f1p := f0c * ImageElm(PhiC, f0c);;
  Phi1 := BuildE(m1, f1p);;
  if Phi1 = fail then Error("BHUNT_STOP: E_{m1,f1p} not well-defined for candidate ", i); fi;
  f3 := f1p * ImageElm(Phi1, f0c);;
  isCube := (f3 = cElt);;
  Add(CCandidates, rec(f0_e := PENT_M1_EVECS[i], cube_f_equals_c := isCube));
  if isCube then
    Print("own_measurement: candidate ", i, " (e=", PENT_M1_EVECS[i], ") satisfies g^3=c\n");
  fi;
od;
nHits := Length(Filtered(CCandidates, r -> r.cube_f_equals_c));;
Print("own_measurement: number of pent(m0) elements with g^3=c : ", nHits, " (BH-3 expects exactly 1)\n");

## ---- BH-5 branch determination ----
## BH-delta (registration falsified) triggers: layer counts already checked in
## J0 (python); here we check nHits<>1 (BH-3 uniqueness violated).
branchDelta := (nHits <> 1);;
branchGamma := (not branchDelta) and (not PhiInvariant);;  ## Phi(L)<>L forces BH-gamma (BH-5)
## if Phi-invariant, BH-alpha/BH-beta remain open (J3 needed, out of window)
branchOpenAlphaBeta := (not branchDelta) and PhiInvariant;;

Print("BH5_PHI_INVARIANT: ", PhiInvariant, "\n");
Print("BH5_BRANCH_DELTA: ", branchDelta, "\n");
Print("BH5_BRANCH_GAMMA: ", branchGamma, "\n");
Print("BH5_BRANCH_OPEN_ALPHA_BETA: ", branchOpenAlphaBeta, "\n");

## ---- write GAP-side JSON fragment (Phi images + C search); Python assembles
## the final cert together with the J0 join output ----
JsonIntList := function(xs)
  local out, i;
  out := "[";
  for i in [1..Length(xs)] do
    if i > 1 then Append(out, ","); fi;
    Append(out, String(xs[i]));
  od;
  Append(out, "]");
  return out;
end;;
JsonBool := function(b) if b then return "true"; else return "false"; fi; end;;

PhiImagesJson := function(rows)
  local out, k, row, e;
  out := "[";
  for k in [1..Length(rows)] do
    if k > 1 then Append(out, ","); fi;
    row := rows[k];
    if row.phi_h_e = fail then e := "null"; else e := JsonIntList(row.phi_h_e); fi;
    Append(out, Concatenation(
      "{\"h_e\":", JsonIntList(row.h_e),
      ",\"phi_h_in_D\":", JsonBool(row.phi_h_in_D),
      ",\"phi_h_e\":", e,
      ",\"phi_h_in_L\":", JsonBool(row.phi_h_in_L), "}"));
  od;
  Append(out, "]");
  return out;
end;;

CCandidatesJson := function(rows)
  local out, k, row;
  out := "[";
  for k in [1..Length(rows)] do
    if k > 1 then Append(out, ","); fi;
    row := rows[k];
    Append(out, Concatenation(
      "{\"f0_e\":", JsonIntList(row.f0_e),
      ",\"cube_f_equals_c\":", JsonBool(row.cube_f_equals_c), "}"));
  od;
  Append(out, "]");
  return out;
end;;

out := OutputTextFile(OUT_PATH, false);;
if out = fail then Error("BHUNT_STOP: cannot open OUT_PATH ", OUT_PATH); fi;
SetPrintFormattingStatus(out, false);;
PrintTo(out,
  "{\n",
  "  \"schema\": \"bhunt-j1j2-gap/v1\",\n",
  "  \"m0\": ", String(M0), ",\n",
  "  \"L_closed_subgroup\": ", JsonBool(LClosed), ",\n",
  "  \"phi_well_defined\": ", JsonBool(PhiM <> fail), ",\n",
  "  \"phi_bijective\": ", JsonBool(PhiBijective), ",\n",
  "  \"phi_images\": ", PhiImagesJson(PhiImages), ",\n",
  "  \"phi_invariant\": ", JsonBool(PhiInvariant), ",\n",
  "  \"m1\": ", String(m1), ",\n",
  "  \"m3_raw\": ", String(m3raw), ",\n",
  "  \"m3_mod7\": ", String(m3mod), ",\n",
  "  \"anchor_c_m\": ", String(C_M), ",\n",
  "  \"anchor_c_e\": ", JsonIntList(C_E), ",\n",
  "  \"c_candidates\": ", CCandidatesJson(CCandidates), ",\n",
  "  \"c_hits_count\": ", String(nHits), ",\n",
  "  \"branch_delta_bh3_uniqueness_violated\": ", JsonBool(branchDelta), ",\n",
  "  \"branch_gamma_phi_noninvariant\": ", JsonBool(branchGamma), ",\n",
  "  \"branch_open_alpha_beta_phi_invariant\": ", JsonBool(branchOpenAlphaBeta), "\n",
  "}\n");;
CloseStream(out);;
Print("CERT_WRITTEN: ", OUT_PATH, "\n");
Print("DRIVER_DONE: true\n");
QUIT;
