#############################################################################
## scratchpad/kpi_orient_feasibility.g
##
## FEASIBILITY CHECK for the K_pi orientation-calibration task ("PENT-NORM
## on the EXISTING K_pi finite quotient vs existing Chk6 c3-pentagon").
##
## Question: does rho (the order-5 automorphism of K(0,5) permuting the 5
## marked points) have a natural lift onto the EXISTING D5=Eg^5 packing used
## by Chk6/Pent in gtpi_closure_20260801.g -- WITHOUT constructing K(0,5)
## itself (that construction is out of scope / being built elsewhere per
## docs/notes/hs_prop7_translation_v1.md sec 3.2, 5.1).
##
## Test: define sigma : D5 -> D5 as the cyclic shift of the 5 direct-product
## factors (the only "free", choice-free candidate for rho's action on this
## packing, since the 5 factors are exactly the 5 slots PsiAt(w,i) uses).
## Necessary condition for "natural lift onto QP": sigma(QP) = QP.
## This is NOT sufficient to prove sigma literally implements rho on K(0,5)
## marked points (that would need explicit generator-image matching against
## x_{i,i+1}), but if it FAILS, there is certainly no natural lift via this
## packing, and we stop honestly per the task's own fallback instruction.
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");

## ---- BLOCK I, byte-identical import (same source as gtpi_closure_20260801.g) ----
n := 5;;
tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; ss := tt*XX^3;;
b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
xb := s1^2;; yb := s2^2;; PN := Group(xb,yb);; Eg := Group(aE,bE);;
Nord := Lcm(Order(xb),Order(yb),Order(cc));;
charm := Filtered([0..Nord-1], z->GcdInt(2*z+1,Nord)=1);;
X12v := xb;; X23v := yb;; X13v := yb^-1*xb^-1;;
X34v := xb;; X24v := s1^-1*yb*s1;; X14v := s1^-1*X13v*s1;;
cof := [ [ X12v, X23v, X13v ],
         [ X23v, X34v, X24v ],
         [ X23v*X13v, X34v, X24v*X14v ],
         [ X13v*X12v, X34v*X24v, X14v ],
         [ X12v, X24v*X23v, X14v*X13v ] ];;
cofc := List([1..5], i -> cof[i][2]*cof[i][3]*cof[i][1]);;
D5 := DirectProduct(Eg,Eg,Eg,Eg,Eg);;
emb := List([1..5], i -> Embedding(D5,i));;
proj := List([1..5], i -> Projection(D5,i));;
Pack := function(l) return Product(List([1..5], i -> Image(emb[i], l[i]))); end;;
Fw := FreeGroup("x","y","c");;
gx := GeneratorsOfGroup(Fw)[1];; gy := GeneratorsOfGroup(Fw)[2];;
gc := GeneratorsOfGroup(Fw)[3];;
Rev := function(w)
  local l, r;
  l := LetterRepAssocWord(w); r := Reversed(l);
  return AssocWordByLetterRep(FamilyObj(gx), r);
end;;
PsiAt := function(w, i)
  return MappedWord(Rev(w), [gx,gy,gc], [cof[i][1],cof[i][2],cofc[i]]);
end;;
Psi := function(w) return Pack(List([1..5], i -> PsiAt(w,i))); end;;
one5 := One(D5);;
QP := Group(Psi(gx), Psi(gy), Psi(gc));;
QF := Group(Psi(gx), Psi(gy));;
gensQP := [Psi(gx),Psi(gy),Psi(gc)];;
redMap := GroupHomomorphismByImages(QP, PN, gensQP, [xb,yb,()]);;
coarse_of := function(w) return MappedWord(w, [gx,gy,gc], [xb,yb,()]); end;;
Ader := DerivedSubgroup(QP);;
kappa := (1,4)(2,5);;
Pent := function(w)
  local v; v := List([1..5], i -> PsiAt(w,i));
  return v[1]*v[4]*v[2] = v[3]*v[5];
end;;
epiP := GroupHomomorphismByImages(Fw, QP, [gx,gy,gc], gensQP);;
WordOf := function(q) return Rev(PreImagesRepresentative(epiP,q)); end;;
## ---- end of byte-identical import ----

Print("== SETUP ==  |D5|=",Size(D5),"  |QP|=",Size(QP),"  |Ader|=",Size(Ader),
      "  |PN|=",Size(PN),"\n");

## ----------------------------------------------------------------------
## Candidate lift: sigma = cyclic shift of the 5 direct-product factors.
## sigma(d) has component i equal to (old component (i-1 mod 5)) i.e.
## component list is rotated by one slot.  Direction is immaterial for the
## sigma(QP)=QP test (an automorphism and its inverse stabilize the same
## subgroups).
## ----------------------------------------------------------------------
SigmaMap := function(d)
  local comps, shifted;
  comps := List([1..5], i -> Image(proj[i], d));
  shifted := List([1..5], i -> comps[((i-2) mod 5) + 1]);  ## comp i <- old comp i-1
  return Pack(shifted);
end;;

## sanity: SigmaMap is a bijective endomorphism of D5 (built from perm-block
## relabelling, so automatically an automorphism -- verify on generators)
sigGensOK := ForAll(GeneratorsOfGroup(D5), g -> SigmaMap(g) in D5);;
Print("   SigmaMap(gens of D5) land in D5 : ", sigGensOK, "\n");

## THE key feasibility test: does sigma stabilize QP (the actually-used
## fine window subgroup for K_pi)?
imgsQP := List(gensQP, SigmaMap);;
Print("   Sigma(Psi(x)) in QP : ", imgsQP[1] in QP, "\n");
Print("   Sigma(Psi(y)) in QP : ", imgsQP[2] in QP, "\n");
Print("   Sigma(Psi(c)) in QP : ", imgsQP[3] in QP, "\n");
sigmaStabilizesQP := ForAll(imgsQP, x -> x in QP);;
Print("   sigma(QP) subseteq QP (necessary for natural lift) : ",
      sigmaStabilizesQP, "\n");

## Also test on Ader = [QP,QP] (the c4 window that actually carries the 20
## measured shadows), since that's the group PENT-NORM would need to act on.
sigmaStabilizesAder := ForAll(Elements(Ader), x -> SigmaMap(x) in Ader);;
Print("   sigma(Ader) subseteq Ader : ", sigmaStabilizesAder, "\n");

## order of sigma restricted to QP, if it stabilizes it (should be 1 or 5
## if it is to have any hope of being rho | order-5 by construction of the
## 5-fold shift; report regardless)
if sigmaStabilizesQP then
  ordSigmaOnQP := Order(GroupHomomorphismByFunction(QP,QP,SigmaMap));;
  Print("   NOTE: could not compute Order via homomorphism object directly; ",
        "checking sigma^5 = id on generators instead\n");
fi;
five := function(d) local r,i; r:=d; for i in [1..5] do r:=SigmaMap(r); od; return r; end;;
sig5OK := ForAll(gensQP, g -> five(g) = g);;
Print("   sigma^5 = identity on gensQP : ", sig5OK, "\n");
sig1OK := ForAll(gensQP, g -> SigmaMap(g) = g);;
Print("   sigma = identity on gensQP (degenerate case) : ", sig1OK, "\n");

Print("\n== VERDICT ==\n");
if sigmaStabilizesQP and sigmaStabilizesAder and (not sig1OK) then
  Print("   FEASIBLE (candidate lift exists) -- proceed to PENT-NORM row-by-row check.\n");
else
  Print("   NOT FEASIBLE via this candidate lift -- no natural rho-action on the\n");
  Print("   existing K_pi finite quotient without constructing K(0,5) itself.\n");
fi;
