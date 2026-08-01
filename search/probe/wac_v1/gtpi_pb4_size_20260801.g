#############################################################################
## search/probe/wac_v1/gtpi_pb4_size_20260801.g
##  P6-2 : size estimate for a PB_4-level check of the K_pi window.
##
##  NOTE ON SOURCES: the definitional source for the PB_4-based GT groupoid
##  (arXiv 2008.00066) is NOT in the atelier.  No external search was done
##  (literature gate).  This file therefore measures ONLY what is already
##  present in the frozen window construction: the images of the six pure
##  braid generators X_{ij} (1<=i<j<=4) that pent_settled_struct/proofcheck2
##  already build in order to define cof[1..5].  Those images generate the
##  PB_4-level window quotient implicit in the construction.  Whether that
##  quotient is THE window of 2008.00066 is UNKNOWN and is not claimed here.
##
##  Window block imported byte-identical from
##    search/probe/wac_v1/pent_settled_cent_proofcheck2_20260731.g
##  Single GAP lane.  NOT a ledger claim.
#############################################################################
n := 5;;
tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; ss := tt*XX^3;;
b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
xb := s1^2;; yb := s2^2;; PN := Group(xb,yb);; Eg := Group(aE,bE);;
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
QP := Group(Psi(gx), Psi(gy), Psi(gc));;

Print("== ambient ==\n");
Print("  |E| = ",Size(Eg),"   structure ",StructureDescription(Eg),"\n");
Print("  |P_N| = |A5 window| = ",Size(PN),"\n");
Print("  |Q_P| = |PB_3/K_pi| = ",Size(QP),"   |[Q_P,Q_P]| = ",
      Size(DerivedSubgroup(QP)),"\n");

## ------------------------------------------------------------------
## the six PB_4 generators already present in the construction
## ------------------------------------------------------------------
gens4 := [X12v, X13v, X14v, X23v, X24v, X34v];;
nm4   := ["X12","X13","X14","X23","X24","X34"];;
Q4 := Group(gens4);;
Print("\n== PB_4-level window quotient implicit in the construction ==\n");
for i in [1..6] do
  Print("  ",nm4[i]," = ",String(gens4[i]),"   order ",Order(gens4[i]),"\n");
od;
Print("  Q4 := <X_ij> <= E ;  |Q4| = ",Size(Q4),
      "   structure ",StructureDescription(Q4),"\n");
D4 := DerivedSubgroup(Q4);;
Print("  |[Q4,Q4]| = ",Size(D4),"   structure ",StructureDescription(D4),"\n");
Print("  Z(Q4) size = ",Size(Centre(Q4)),
      "   Q4/[Q4,Q4] size = ",Size(Q4)/Size(D4),"\n");
Print("  index of Q4 in E = ",Size(Eg)/Size(Q4),"\n");

## the PB_3 sub-picture inside it (forgetting strand 4)
Q3 := Group([X12v,X13v,X23v]);;
Print("\n  <X12,X13,X23> (PB_3 image) : |.| = ",Size(Q3),
      "   structure ",StructureDescription(Q3),"\n");
Print("  P_N = <xb,yb> : |.| = ",Size(PN),
      "   equal to <X12,X13,X23> ? ",Q3 = PN,"\n");

## ------------------------------------------------------------------
## cost model: a PB_4-level GT-shadow scan of the same shape as P6-1
##   universe = charm x [Q,Q]  (because condition c4 is  q in [Q,Q])
## ------------------------------------------------------------------
Print("\n== scan-cost model (same shape as the PB_3 run) ==\n");
Print("  PB_3 level  : charm(4) x |[Q_P,Q_P]|(",Size(DerivedSubgroup(QP)),
      ") = ",4*Size(DerivedSubgroup(QP))," Chk-calls   [actually run]\n");
Print("  PB_4 level, IF the window quotient is Q4 and c4 keeps the same shape:\n");
Print("     charm(4) x |[Q4,Q4]|(",Size(D4),") = ",4*Size(D4)," Chk-calls\n");
Print("  naive (no c4 cut) PB_4 scan : charm(4) x |Q4|(",Size(Q4),") = ",
      4*Size(Q4),"\n");

## ------------------------------------------------------------------
## the *pullback* window, for contrast: index is exact, no enumeration
## ------------------------------------------------------------------
Print("\n== pullback window (contrast) ==\n");
Print("  PB_4 -->> PB_3 (forget strand 4) is surjective, so the pullback of\n");
Print("  K_pi has index exactly |PB_3/K_pi| = ",Size(QP),
      " in PB_4 -- no coset enumeration needed.\n");
Print("  But that window contains the whole Fadell-Neuwirth kernel F_3, so the\n");
Print("  PB_4 quotient collapses to Q_P and every genuinely-PB_4 condition is\n");
Print("  vacuous.  It is therefore NOT a usable PB_4-level window.\n");

Print("\n== DONE ==\n");
QUIT;
