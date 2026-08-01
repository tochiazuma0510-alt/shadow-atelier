#############################################################################
## search/probe/wac_v1/gtpi_pb4_prop33_20260801.g
##  P6-2 step (3): PB_4-level settled measurement + Prop 3.3 intersection.
##  IF-FIRST FREEZE (written BEFORE this run):
##    docs/notes/gtpi_pb4_cv9_freeze_v1.md
##    SHA-256 66bd8743ceaec9de4d67c7a706dca40d1ffbc469d567f865b9597011925d5d90
##  Window block imported byte-identical from pent_settled_cent_proofcheck2.
##  Contact-blocked: no expected value is asserted.  The ONLY aborting asserts
##  are the well-definedness gates WD-1..WD-3 (freeze sec.3, ruling 370).
##  Single GAP lane.  NOT a ledger claim.
#############################################################################
n := 5;; tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; ss := tt*XX^3;; b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
xb := s1^2;; yb := s2^2;; PN := Group(xb,yb);; Eg := Group(aE,bE);;
Nord := Lcm(Order(xb),Order(yb),Order(cc));;
charm := Filtered([0..Nord-1], z->GcdInt(2*z+1,Nord)=1);;
X12v := xb;; X23v := yb;; X13v := yb^-1*xb^-1;;
X34v := xb;; X24v := s1^-1*yb*s1;; X14v := s1^-1*X13v*s1;;
cof := [ [ X12v, X23v, X13v ], [ X23v, X34v, X24v ],
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
Rev := function(w) local l,r; l:=LetterRepAssocWord(w); r:=Reversed(l);
  return AssocWordByLetterRep(FamilyObj(gx),r); end;;
PsiAt := function(w,i) return MappedWord(Rev(w),[gx,gy,gc],
  [cof[i][1],cof[i][2],cofc[i]]); end;;
Psi := function(w) return Pack(List([1..5], i -> PsiAt(w,i))); end;;
one5 := One(D5);;
QP := Group(Psi(gx),Psi(gy),Psi(gc));; QF := Group(Psi(gx),Psi(gy));;
gensQP := [Psi(gx),Psi(gy),Psi(gc)];;
redMap := GroupHomomorphismByImages(QP,PN,gensQP,[xb,yb,()]);;
coarse_of := function(w) return MappedWord(w,[gx,gy,gc],[xb,yb,()]); end;;
Ader := DerivedSubgroup(QP);;
Hex := function(m,f) local u; u := 2*m+1;
  return s1^u*f^-1*s2^u*f = f^-1*s1*s2*xb^(-m)*cc^m and
         f^-1*s2^u*f*s1^u = s2*s1*yb^(-m)*cc^m*f; end;;
X13w := gx^-1*gc*gy^-1;;
SubW := function(w,ix,iy,ic) return MappedWord(w,[gx,gy,gc],[ix,iy,ic]); end;;
Aut1 := function(w) return SubW(w, gx, gy^-1*X13w*gy, gc); end;;
Aut2 := function(w) return SubW(w, X13w, gy, gc); end;;
Pent := function(w) local v; v := List([1..5], i -> PsiAt(w,i));
  return v[1]*v[4]*v[2] = v[3]*v[5]; end;;
epiP := GroupHomomorphismByImages(Fw,QP,[gx,gy,gc],gensQP);;
WordOf := function(q) return Rev(PreImagesRepresentative(epiP,q)); end;;
Chk6 := function(m,q)
  local w,P0,R0,S0,D1,D2,c1,c2,c3,c4,c5,sb,u;
  w := WordOf(q); u := 2*m+1;
  P0 := gx^m * w^-1 * Aut2(gy^m * w); R0 := (X13w*gy)^m;
  D1 := Aut1(P0) * (Aut1(Aut2(R0)))^-1 * w; c1 := Psi(D1) = one5;
  S0 := (gx*X13w)^m;
  D2 := w^-1 * Aut2(gy^m*w) * Aut2(Aut1(gx^m))
        * ( Aut2(Aut1(S0)) * Aut2(Aut1(w)) )^-1; c2 := Psi(D2) = one5;
  c3 := Pent(w); c4 := (q in Ader);
  sb := Group(Psi(gx^u), Psi(w^-1*gy^u*w)); c5 := (Size(sb) = Size(QF));
  return [c1,c2,c3,c4,c5, c1 and c2 and c3 and c4 and c5]; end;;

## =====================================================================
## WD gates (freeze sec.3) -- the ONLY aborting asserts
## =====================================================================
Print("== WD gates ==\n");
Print("  WD-3 braid: s1s2s1=s2s1s2 ? ",s1*s2*s1=s2*s1*s2,
      "   (sigma3|->s1 so the other two relations are the same / trivial)\n");
if not (s1*s2*s1 = s2*s1*s2) then Error("WD-3 FAIL"); fi;
Print("  order of c=(s1s2)^3 in E : ",Order(cc),"    N_ord = ",Nord,
      "    charm = ",charm,"\n");
wd1 := [];;
for i in [1..5] do
  Add(wd1, PsiAt(X13w,i) = cof[i][3]);
od;
Print("  WD-1 (A.5) x13 = x12^-1 c x23^-1 per component : ",wd1,"\n");
if not ForAll(wd1, z -> z) then Error("WD-1 FAIL (A.5 presentation)"); fi;
wd2 := List([1..5], i -> cofc[i] in Centre(Group(cof[i][1],cof[i][2])));;
Print("  WD-2 cofc[i] central in <cof[i][1],cof[i][2]> : ",wd2,"\n");
if not ForAll(wd2, z -> z) then Error("WD-2 FAIL (not a homomorphism)"); fi;
## WD-4 mixing detector: fwd generators poured into rev row order
X13fwd := s2*xb*s2^-1;;  X14fwd := s1*X13fwd*s1^-1;;  X24fwd := s1*yb*s1^-1;;
cofMix := [ [ X12v, X23v, X13fwd ], [ X23v, X34v, X24fwd ],
            [ X23v*X13fwd, X34v, X24fwd*X14fwd ],
            [ X13fwd*X12v, X34v*X24fwd, X14fwd ],
            [ X12v, X24fwd*X23v, X14fwd*X13fwd ] ];;
cofcMix := List([1..5], i -> cofMix[i][2]*cofMix[i][3]*cofMix[i][1]);;
wd4 := List([1..5], i ->
   MappedWord(Rev(X13w),[gx,gy,gc],[cofMix[i][1],cofMix[i][2],cofcMix[i]])
   = cofMix[i][3]);;
Print("  WD-4 mixing detector (fwd gens x rev rows) : ",wd4,"\n");
Print("       discriminating (contains false) ? ",ForAny(wd4, z -> z = false),
      "\n");

## =====================================================================
## (2.4) : N_PB3 as the intersection of the five pullbacks
## =====================================================================
Print("\n== (2.4) N_PB3 ==\n");
Print("  |PB3/N_PB3| = |QP| = ",Size(QP),"   |F2/N_F2| = |QF| = ",Size(QF),
      "\n  |[QF,QF]| = ",Size(DerivedSubgroup(QF)),
      "   [QP,QP]=[QF,QF] ? ",Ader = DerivedSubgroup(QF),"\n");
Print("  |PB4/N_0| = |<X_ij>| = ",
      Size(Group([X12v,X13v,X14v,X23v,X24v,X34v])),"\n");

## =====================================================================
## GT-heart(N_0) : exhaustive over charm x [QP,QP]
## =====================================================================
Print("\n== GT-heart(N_0) ==\n");
Gfine := [];;
for m in charm do for q in Elements(Ader) do
  if Chk6(m,q)[6] then Add(Gfine,[m,q]); fi;
od; od;
Print("  |GT^heart(N_0)| (exhaustive charm x [QP,QP]) = ",Length(Gfine),"\n");

## =====================================================================
## PB_4-level settled : T_{m,f} on B_4, both conjugation orientations
## =====================================================================
Print("\n== PB_4 settled ==\n");
Aijs := function(t1,t2,t3)
  return [ t1^2, t2*t1^2*t2^-1, t3*t2*t1^2*t2^-1*t3^-1,
           t2^2, t3*t2^2*t3^-1, t3^2 ]; end;;
piA := Aijs(s1,s2,s1);;
piPB4 := Group(piA);;
Print("  |pi(PB_4)| = ",Size(piPB4),"\n");
D2n := DirectProduct(Eg,Eg);;
e1 := Embedding(D2n,1);; e2 := Embedding(D2n,2);;
resAlign := [];; resMix := [];; TimgAlign := [];;
for tr in Gfine do
  m := tr[1];; q := tr[2];; u := 2*m+1;; w := WordOf(q);;
  v1 := PsiAt(w,1);; v3 := PsiAt(w,3);;
  a1 := s1^u;;  a2 := v1*s2^u*v1^-1;;  a3 := v3*s1^u*v3^-1;;
  okA := (a1*a2*a1 = a2*a1*a2) and (a2*a3*a2 = a3*a2*a3) and (a1*a3 = a3*a1);;
  b1 := s1^u;;  b2 := v1^-1*s2^u*v1;;  b3 := v3^-1*s1^u*v3;;
  okB := (b1*b2*b1 = b2*b1*b2) and (b2*b3*b2 = b3*b2*b3) and (b1*b3 = b3*b1);;
  szA := -1;; szB := -1;; aijA := fail;; aijB := fail;;
  if okA then
    aijA := Aijs(a1,a2,a3);
    szA := Size(Group(List([1..6], k ->
      Image(e1,piA[k])*Image(e2,aijA[k]))));
    Add(TimgAlign, aijA);
  fi;
  if okB then
    aijB := Aijs(b1,b2,b3);
    szB := Size(Group(List([1..6], k ->
      Image(e1,piA[k])*Image(e2,aijB[k]))));
  fi;
  Add(resAlign, [m, String(coarse_of(w)), okA, szA, szA = Size(piPB4)]);
  Add(resMix,   [m, String(coarse_of(w)), okB, szB, szB = Size(piPB4)]);
od;
Print("  [aligned v(.)v^-1] T is a B_4 rep : ",Number(resAlign,r->r[3]),"/",
      Length(Gfine),"   pair-image size = |pi(PB4)| : ",
      Number(resAlign,r->r[5]),"/",Length(Gfine),
      "\n     sizes seen : ",Set(resAlign,r->r[4]),"\n");
Print("  [mixed  v^-1(.)v ] T is a B_4 rep : ",Number(resMix,r->r[3]),"/",
      Length(Gfine),"   pair-image size = |pi(PB4)| : ",
      Number(resMix,r->r[5]),"/",Length(Gfine),
      "\n     sizes seen : ",Set(resMix,r->r[4]),"\n");

## =====================================================================
## Prop 3.3 : N^sharp = intersection of the sources
## =====================================================================
Print("\n== Prop 3.3 : N^sharp ==\n");
if Length(TimgAlign) > 0 then
  kk := Length(TimgAlign);
  Dk := DirectProduct(List([1..kk], z -> Eg));
  ek := List([1..kk], i -> Embedding(Dk,i));
  packed := List([1..6], j ->
    Product(List([1..kk], i -> Image(ek[i], TimgAlign[i][j]))));
  Print("  #sources packed = ",kk,"   |PB_4/N^sharp| = ",
        Size(Group(packed)),"\n");
  Print("  |PB_4/N^sharp| = |PB_4/N_0| ? ",
        Size(Group(packed)) = Size(piPB4),"\n");
else
  Print("  no aligned source available\n");
fi;
Print("\n== SCOPE: c-image is trivial in this window (Order(cc)=",Order(cc),
      "), so the c-terms of the shadow conditions are UNTESTED here.\n");
Print("== DONE ==\n"); QUIT;
