#############################################################################
## search/probe/wac_v1/gtpi_closure_20260801.g
##
##  P6-1 (GTPI) : composition probe for the theorem candidate
##      red : GT(K_pi) --> GT(N_A) ~= F_20   is a group isomorphism
##  at the PB_3-level implemented model.
##
##  IF-FIRST FREEZE (written BEFORE this file was run):
##      docs/notes/gtpi_cv9_freeze_v1.md
##      SHA-256 b5b3969812bc168a7995efba556e46ef217e1fd710bb66b4c6bc53b819cd539c
##  All predictions P-GTPI-1..7 and the CV-9-1 declarations (input universe /
##  comparison target / equivalence / normal form / filter / failure state)
##  are in that file.  This probe does NOT assert any predicted value:
##  everything is COMPUTED and LOGGED; the commander/Sol compare.
##
##  Window / cof / D5 / Psi / PsiAt / coarse_of / Hex / Pent / Chk6 / WordOf
##  imported BYTE-IDENTICAL from
##      search/probe/wac_v1/pent_settled_cent_proofcheck2_20260731.g
##      SHA-256 9ee1d981ca126a8ebbfacd5d5a7bf8e21af6222ff2fd76dc5eae6f7bd27596f4
##  (which in turn imported them byte-identical from pent_settled_struct /
##   pent_t2t3_v3.1).  Nothing in the imported block is edited.
##
##  ORIENTATION (frozen, freeze doc sec.2):
##      T'_{m,q} : Psi(x)|->Psi(x)^u , Psi(y)|-> q Psi(y)^u q^{-1} , Psi(c)|->Psi(c)^u
##      composition o = "apply the RIGHT one first"; never GAP's map product.
##
##  LEVEL CAVEAT: PB_3-level model only.  Says nothing about the PB_4-level
##  GT(K_pi) of C1 Prop 2.11 / 2008.00066.
##  Single GAP lane.  NOT a ledger claim.
#############################################################################

## ==========================================================================
## BLOCK I -- imported byte-identical (window, Psi, coarse_of, Hex, Chk6)
## ==========================================================================
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

Hex := function(m,f)
  local u; u := 2*m+1;
  return s1^u*f^-1*s2^u*f = f^-1*s1*s2*xb^(-m)*cc^m and
         f^-1*s2^u*f*s1^u = s2*s1*yb^(-m)*cc^m*f;
end;;
PhiOf := function(m,f)
  local u;  u := 2*m+1;
  return GroupHomomorphismByImages(PN,PN,[xb,yb],[xb^u,(yb^u)^f]);
end;;
X13w := gx^-1*gc*gy^-1;;
SubW := function(w, ix, iy, ic) return MappedWord(w,[gx,gy,gc],[ix,iy,ic]); end;;
Aut1 := function(w) return SubW(w, gx, gy^-1*X13w*gy, gc); end;;
Aut2 := function(w) return SubW(w, X13w, gy, gc); end;;
Pent := function(w)
  local v; v := List([1..5], i -> PsiAt(w,i));
  return v[1]*v[4]*v[2] = v[3]*v[5];
end;;
epiP := GroupHomomorphismByImages(Fw, QP, [gx,gy,gc], gensQP);;
WordOf := function(q) return Rev(PreImagesRepresentative(epiP,q)); end;;
Chk6 := function(m, q)
  local w, P0, R0, S0, D1, D2, c1, c2, c3, c4, c5, sb, u;
  w := WordOf(q); u := 2*m+1;
  P0 := gx^m * w^-1 * Aut2(gy^m * w);
  R0 := (X13w*gy)^m;
  D1 := Aut1(P0) * (Aut1(Aut2(R0)))^-1 * w;
  c1 := Psi(D1) = one5;
  S0 := (gx*X13w)^m;
  D2 := w^-1 * Aut2(gy^m*w) * Aut2(Aut1(gx^m))
        * ( Aut2(Aut1(S0)) * Aut2(Aut1(w)) )^-1;
  c2 := Psi(D2) = one5;
  c3 := Pent(w);
  c4 := (q in Ader);
  sb := Group(Psi(gx^u), Psi(w^-1*gy^u*w));
  c5 := (Size(sb) = Size(QF));
  return [c1,c2,c3,c4,c5, c1 and c2 and c3 and c4 and c5];
end;;
## ==================== end of imported block ================================

Print("== BLOCK I setup ==  |QP|=",Size(QP),"  |Ader|=",Size(Ader),
      "  |PN|=",Size(PN),"  Nord=",Nord,"  charm=",charm,"\n");
Print("   ord Psi(x)=",Order(Psi(gx)),"  ord Psi(y)=",Order(Psi(gy)),
      "  ord Psi(c)=",Order(Psi(gc)),"  exponent(QP)=",Exponent(QP),"\n");

## ==========================================================================
## BLOCK II -- coarse universe S = GT(N_A), and the machine comparison with
##             the pre-registered 20 rows of cert pent_t2t3_v32_20260801.json
## ==========================================================================
shad := [];;
for m in charm do for f in Elements(PN) do
  if Hex(m,f) and Group(xb,yb^f)=PN then Add(shad,[m,f]); fi;
od; od;
Print("\n== BLOCK II ==  |GT(N_A)| = ",Length(shad),"\n");

## pre-registered rows, transcribed from cert shadows[].{m,f_perm}
preReg := [ [0,()], [0,(2,3,4)], [0,(1,2,3,4,5)], [0,(1,2,4,5,3)], [0,(1,5,3)],
            [1,(1,3,5,4,2)], [1,(1,3,5,2,4)], [1,(1,4,3,2,5)], [1,(1,4)(2,5)],
            [1,(1,5,4,3,2)],
            [3,(1,3,5,4,2)], [3,(1,3,5,2,4)], [3,(1,4,3,2,5)], [3,(1,4)(2,5)],
            [3,(1,5,4,3,2)],
            [4,()], [4,(2,3,4)], [4,(1,2,3,4,5)], [4,(1,2,4,5,3)], [4,(1,5,3)] ];;
preRegMatch := (Set(shad) = Set(preReg));;
Print("   pre-registered 20 rows == regenerated shad (as sets) : ",
      preRegMatch,"\n");
if not preRegMatch then
  Error("PRE-REGISTRATION MISMATCH: the frozen universe is not the computed one");
fi;

Cy := Centralizer(PN,yb);;
SigTab := List(charm, m -> [m, Filtered(Elements(PN), g -> PhiOf(m,g) <> fail)]);;
SigOf := function(m) return First(SigTab,r->r[1]=m)[2]; end;;
SmOf  := function(m) return List(Filtered(shad,z->z[1]=m),z->z[2]); end;;
Print("   |C_P(yb)|=",Size(Cy),"   |Sigma_m| = ",List(charm,m->Length(SigOf(m))),
      "   |S_m| = ",List(charm,m->Length(SmOf(m))),"\n");
## P-GTPI-7 second half : does Hex pick exactly one element per <yb>-coset?
oneCoset := ForAll(charm, m -> ForAll(SmOf(m), f1 ->
              Number(SmOf(m), f2 -> f2*f1^-1 in Cy) = 1));;
Print("   Hex picks exactly one f per C_P(yb)-coset inside S_m : ",oneCoset,"\n");

## ==========================================================================
## BLOCK III -- fine universe G, EXHAUSTIVE.
##   Chk6 condition c4 is literally  q in Ader = [QP,QP]  (imported line),
##   so scanning Ader (60 elements) x charm (4) is EXHAUSTIVE over QP, not a
##   shortcut.  We log the witness of that fact.
## ==========================================================================
Print("\n== BLOCK III ==  exhaustive scan over charm x Ader (",
      Length(charm),"x",Size(Ader)," = ",Length(charm)*Size(Ader)," Chk6 calls)\n");
AderElts := Elements(Ader);;
## structural fact behind P-GTPI-3: rho|_A and (coarse_of o WordOf)|_A bijective
rhoOnA    := List(AderElts, q -> Image(redMap,q));;
labOnA    := List(AderElts, q -> coarse_of(WordOf(q)));;
rhoA_bij  := (Length(Set(rhoOnA)) = Size(Ader)) and (Set(rhoOnA) = Set(Elements(PN)));;
labA_bij  := (Length(Set(labOnA)) = Size(Ader)) and (Set(labOnA) = Set(Elements(PN)));;
AcapV     := Size(Intersection(Ader, Kernel(redMap)));;
Print("   rho|_A : A -> P bijective : ",rhoA_bij,
      "    (coarse_of o WordOf)|_A bijective : ",labA_bij,
      "    |A cap ker rho| = ",AcapV,"\n");

Gfine := [];;
for m in charm do
  for q in AderElts do
    if Chk6(m,q)[6] then Add(Gfine,[m,q]); fi;
  od;
od;
Print("   |G| = ",Length(Gfine)," (exhaustive)\n");
## label / rho of each fine shadow
Gm   := List(Gfine, t -> t[1]);;
Gq   := List(Gfine, t -> t[2]);;
Gf   := List(Gfine, t -> coarse_of(WordOf(t[2])));;   ## author-side label
Gg   := List(Gfine, t -> Image(redMap,t[2]));;        ## our-side label
redImg := List([1..Length(Gfine)], i -> [Gm[i], Gf[i]]);;
redSurj := (Set(redImg) = Set(shad));;
redInj  := (Length(Set(redImg)) = Length(Gfine));;
Print("   red (author label) surjective onto GT(N_A) : ",redSurj,
      "   injective : ",redInj,"\n");
Print("   fine shadows per coarse shadow (multiset of fibre counts) : ",
      Set(List(shad, z -> Number(redImg, r -> r = z))),"\n");
## unit
unitIdx := First([1..Length(Gfine)], i -> Gm[i]=0 and Gq[i]=One(QP));;
Print("   index of (m,q)=(0,1_QP) in G : ",unitIdx,"\n");

## ==========================================================================
## BLOCK IV -- T' homomorphisms, and the 400-pair composition table
## ==========================================================================
Print("\n== BLOCK IV ==  T' (aligned) and 400-pair composition\n");
TpOf := function(m,q)
  local u; u := 2*m+1;
  return GroupHomomorphismByImages(QP,QP,gensQP,
           [Psi(gx)^u, q*Psi(gy)^u*q^-1, Psi(gc)^u]);
end;;
TmixOf := function(m,q)          ## DUM-G3 : the mixed (v3.1) convention
  local u; u := 2*m+1;
  return GroupHomomorphismByImages(QP,QP,gensQP,
           [Psi(gx)^u, q^-1*Psi(gy)^u*q, Psi(gc)^u]);
end;;
Tp   := List(Gfine, t -> TpOf(t[1],t[2]));;
Tmix := List(Gfine, t -> TmixOf(t[1],t[2]));;
TpDefined   := List(Tp,   h -> h <> fail);;
TmixDefined := List(Tmix, h -> h <> fail);;
KerSize := function(h)
  if h = fail then return -1; else return Size(Kernel(h)); fi;
end;;
TpKer   := List(Tp,   h -> KerSize(h));;
TmixKer := List(Tmix, h -> KerSize(h));;
Print("   T' well-defined : ",Number(TpDefined,z->z),"/",Length(Gfine),
      "   kernel sizes : ",Set(TpKer),"\n");
Print("   T  well-defined : ",Number(TmixDefined,z->z),"/",Length(Gfine),
      "   kernel sizes : ",Set(TmixKer),"\n");

## normal form for m'' (freeze doc sec.4, NF)
MppOf := function(u1,u2)
  return First(charm, z -> ((2*z+1) - u1*u2) mod Nord = 0);
end;;
IdxOf := function(m,q)
  return First([1..Length(Gfine)], i -> Gm[i]=m and Gq[i]=q);
end;;

nPairs := 0;; nP1 := 0;; nClosed := 0;; nRev := 0;; nMixClosed := 0;;
nRedAuth := 0;; nRedOur := 0;; nMppAgree := 0;; nMixDefinedPair := 0;;
MT := List([1..Length(Gfine)], i -> List([1..Length(Gfine)], j -> 0));;
failRows := [];;
for i in [1..Length(Gfine)] do
  for j in [1..Length(Gfine)] do
    nPairs := nPairs + 1;
    u1 := 2*Gm[i]+1;; u2 := 2*Gm[j]+1;;
    mpp := MppOf(u1,u2);
    ## (3.53) m-formula cross-check
    if mpp = (2*Gm[i]*Gm[j] + Gm[i] + Gm[j]) mod Nord then
      nMppAgree := nMppAgree + 1; fi;
    ## --- P-GTPI-1 : composite of the two T' is again of T' shape ---
    qpp := Image(Tp[i], Gq[j]) * Gq[i];
    hcomp_x := Image(Tp[i], Image(Tp[j], Psi(gx)));
    hcomp_y := Image(Tp[i], Image(Tp[j], Psi(gy)));
    hcomp_c := Image(Tp[i], Image(Tp[j], Psi(gc)));
    upp := 2*mpp+1;
    shapeOK := (hcomp_x = Psi(gx)^upp) and
               (hcomp_y = qpp*Psi(gy)^upp*qpp^-1) and
               (hcomp_c = Psi(gc)^upp);
    if shapeOK then nP1 := nP1 + 1; fi;
    ## --- P-GTPI-2 : closure ---
    k := IdxOf(mpp, qpp);
    if k <> fail then nClosed := nClosed + 1; MT[i][j] := k;
    else MT[i][j] := 0; Add(failRows, [i,j,mpp,String(Image(redMap,qpp))]); fi;
    ## --- DUM-G2 : reversed order ---
    qrev := Gq[i] * Image(Tp[i], Gq[j]);
    if IdxOf(mpp, qrev) <> fail then nRev := nRev + 1; fi;
    ## --- DUM-G3 : mixed convention ---
    if Tmix[i] <> fail then
      nMixDefinedPair := nMixDefinedPair + 1;
      qmix := Gq[i] * Image(Tmix[i], Gq[j]);
      if IdxOf(mpp, qmix) <> fail then nMixClosed := nMixClosed + 1; fi;
    fi;
    ## --- P-GTPI-4 : red is a homomorphism, both coordinates ---
    ##   author side : f'' = f_1 * E_{m1,f1}(f_2)     (canon (3.53))
    e1 := PhiOf(Gm[i], Gf[i]);
    if e1 <> fail then
      if coarse_of(WordOf(qpp)) = Gf[i] * Image(e1, Gf[j]) then
        nRedAuth := nRedAuth + 1; fi;
    fi;
    ##   our side   : g'' = Phi'_{m1,g1}(g_2) * g_1   (dialogue T-21 lemma OPP)
    p1 := GroupHomomorphismByImages(PN,PN,[xb,yb],[xb^u1, Gg[i]*yb^u1*Gg[i]^-1]);
    if p1 <> fail then
      if Image(redMap,qpp) = Image(p1, Gg[j]) * Gg[i] then
        nRedOur := nRedOur + 1; fi;
    fi;
  od;
od;
Print("   pairs                                  : ",nPairs,"\n");
Print("   P-GTPI-1  composite has T' shape       : ",nP1,"/",nPairs,"\n");
Print("   m'' NF  ==  (3.53) 2m1m2+m1+m2 mod 5   : ",nMppAgree,"/",nPairs,"\n");
Print("   P-GTPI-2  closure  (m'',q'') in G      : ",nClosed,"/",nPairs,"\n");
Print("   P-GTPI-4  red author-side hom          : ",nRedAuth,"/",nPairs,"\n");
Print("   P-GTPI-4  red our-side hom             : ",nRedOur,"/",nPairs,"\n");
Print("   DUM-G2    REVERSED order lands in G    : ",nRev,"/",nPairs,"\n");
Print("   DUM-G3    MIXED conv. lands in G       : ",nMixClosed,"/",
      nMixDefinedPair," (defined pairs)\n");
if Length(failRows) > 0 then
  Print("   closure failures (first 10): ",failRows{[1..Minimum(10,Length(failRows))]},"\n");
fi;

## ==========================================================================
## BLOCK V -- group structure of (G,*) from the table, and F_20
## ==========================================================================
Print("\n== BLOCK V ==  group structure\n");
tableTotal := ForAll(MT, r -> ForAll(r, z -> z <> 0));;
Print("   multiplication table total (no holes)  : ",tableTotal,"\n");
assocOK := "not_evaluated";; latinOK := "not_evaluated";;
idxIdentity := "none";; ordDist := "not_evaluated";;
idG := "not_evaluated";; idH := "not_evaluated";;
sdG := "not_evaluated";; sdH := "not_evaluated";;
isoGH := "not_evaluated";; regHomOK := "not_evaluated";;
invAll := "not_evaluated";;
if tableTotal then
  assocOK := ForAll([1..Length(Gfine)], a -> ForAll([1..Length(Gfine)], b ->
               ForAll([1..Length(Gfine)], c -> MT[MT[a][b]][c] = MT[a][MT[b][c]])));
  latinOK := ForAll([1..Length(Gfine)], a -> Length(Set(MT[a])) = Length(Gfine))
             and ForAll([1..Length(Gfine)], b ->
                   Length(Set(List([1..Length(Gfine)], a -> MT[a][b])))
                   = Length(Gfine));
  idxIdentity := First([1..Length(Gfine)], e ->
                   ForAll([1..Length(Gfine)], a -> MT[e][a]=a and MT[a][e]=a));
  invAll := ForAll([1..Length(Gfine)], a ->
              ForAny([1..Length(Gfine)], b -> MT[a][b] = idxIdentity));
  ## right-regular representation:  rho_i(j) = j*i  (GAP acts on the right,
  ## so THIS one is a homomorphism; freeze doc sec.2.4 discipline)
  regperm := List([1..Length(Gfine)], i ->
               PermList(List([1..Length(Gfine)], j -> MT[j][i])));
  Greg := Group(regperm);
  regHomOK := ForAll([1..Length(Gfine)], a -> ForAll([1..Length(Gfine)], b ->
                regperm[a]*regperm[b] = regperm[MT[a][b]]));
  idG := IdGroup(Greg);  sdG := StructureDescription(Greg);
  ## element orders in (G,*)
  ordOf := function(a)
    local k, z; k := 1; z := a;
    while z <> idxIdentity do z := MT[z][a]; k := k+1; od;
    return k; end;
  ordDist := Collected(List([1..Length(Gfine)], a -> ordOf(a)));
fi;
## coarse side H = < E_{m,f} > inside Aut(P)
phis := List(shad, z -> PhiOf(z[1],z[2]));;
Print("   all 20 coarse E_{m,f} well-defined     : ",
      ForAll(phis, h -> h <> fail),"\n");
Hgrp := Group(phis);;
idH := IdGroup(Hgrp);; sdH := StructureDescription(Hgrp);;
Print("   |H| = ",Size(Hgrp),"   IdGroup(H) = ",idH,"   ",sdH,"\n");
Print("   IdGroup((G,*)) = ",idG,"   ",sdG,"\n");
Print("   assoc = ",assocOK,"   latin = ",latinOK,
      "   identity index = ",idxIdentity,"   inverses = ",invAll,"\n");
Print("   right-regular rep is a homomorphism    : ",regHomOK,"\n");
Print("   order distribution in (G,*)            : ",ordDist,"\n");
## explicit isomorphism (m,q) |-> Phi'_{m,rho(q)}  (freeze doc P-GTPI-6)
PhiPrimeOf := function(m,g)
  local u; u := 2*m+1;
  return GroupHomomorphismByImages(PN,PN,[xb,yb],[xb^u, g*yb^u*g^-1]);
end;;
pp := List([1..Length(Gfine)], i -> PhiPrimeOf(Gm[i], Gg[i]));;
ppDefined := ForAll(pp, h -> h <> fail);;
ppDistinct := (Length(Set(pp)) = Length(Gfine));;
ppInH := false;;
if ppDefined then ppInH := ForAll(pp, h -> h in Hgrp); fi;
## homomorphism test with o = "apply right first": Phi'_{i o j} = Phi'_i o Phi'_j
ppHom := "not_evaluated";;
if tableTotal and ppDefined then
  ppHom := ForAll([1..Length(Gfine)], a -> ForAll([1..Length(Gfine)], b ->
             ForAll([xb,yb], z ->
               Image(pp[MT[a][b]], z) = Image(pp[a], Image(pp[b], z)))));
fi;
Print("   Phi'-map: defined=",ppDefined,"  distinct=",ppDistinct,
      "  lands in H=",ppInH,"  is a homomorphism (right-first)=",ppHom,"\n");
## and the author-side map (m,f) |-> E_{m,f}
eeHom := "not_evaluated";;
if tableTotal then
  eeHom := ForAll([1..Length(Gfine)], a -> ForAll([1..Length(Gfine)], b ->
             ForAll([xb,yb], z ->
               Image(PhiOf(Gm[MT[a][b]],Gf[MT[a][b]]), z)
               = Image(PhiOf(Gm[a],Gf[a]), Image(PhiOf(Gm[b],Gf[b]), z)))));
fi;
Print("   E-map (author labels) is a homomorphism (right-first)=",eeHom,"\n");

## ==========================================================================
## BLOCK VI -- coarse literal closure (P-GTPI-7) on all 400 coarse pairs
## ==========================================================================
Print("\n== BLOCK VI ==  coarse literal closure\n");
nCoarse := 0;; nCoarseClosed := 0;;
for a in shad do for b in shad do
  nCoarse := nCoarse + 1;
  u1 := 2*a[1]+1;; u2 := 2*b[1]+1;;
  mpp := MppOf(u1,u2);
  e1 := PhiOf(a[1],a[2]);
  if e1 <> fail then
    fpp := a[2] * Image(e1, b[2]);
    if [mpp,fpp] in shad then nCoarseClosed := nCoarseClosed + 1; fi;
  fi;
od; od;
Print("   P-GTPI-7  (m'', f1*E(f2)) literally in GT(N_A) : ",
      nCoarseClosed,"/",nCoarse,"\n");

## ==========================================================================
## BLOCK VII -- discriminating dummies DUM-G1 / DUM-G4
## ==========================================================================
Print("\n== BLOCK VII ==  dummies\n");
Vker := Kernel(redMap);;
zc := First(Elements(Vker), z -> z <> One(QP));;
dumIdx := First([1..Length(Gfine)], i -> Gq[i] <> One(QP));;
qbad := Gq[dumIdx]*zc;;
dumSameCoarseLabel := (coarse_of(WordOf(qbad)) = Gf[dumIdx]);;
dumSameRho := (Image(redMap,qbad) = Gg[dumIdx]);;
dumChk := Chk6(Gm[dumIdx], qbad);;
dumInG := (First([1..Length(Gfine)], i -> Gm[i]=Gm[dumIdx] and Gq[i]=qbad) <> fail);;
## and does the *composition* with the bad element leave G?
dumClosureBreaks := "not_evaluated";;
i0 := 1;;
qppbad := Image(Tp[i0], qbad) * Gq[i0];;
mppbad := MppOf(2*Gm[i0]+1, 2*Gm[dumIdx]+1);;
dumClosureBreaks := (IdxOf(mppbad,qppbad) = fail);;
Print("   DUM-G1  |V|=",Size(Vker),"  z<>1 chosen; q_bad = q*z\n");
Print("      coarse label unchanged : ",dumSameCoarseLabel,
      "   rho unchanged : ",dumSameRho,"\n");
Print("      Chk6(q_bad) = ",dumChk,"   q_bad in G : ",dumInG,"\n");
Print("      composing with q_bad leaves G : ",dumClosureBreaks,"\n");
## DUM-G4 : non-charming m = 2 (u = 5 = 0 mod 5)
dum4 := TpOf(2, Gq[1]);;
dum4def := (dum4 <> fail);;
dum4ker := KerSize(dum4);;
dum4hex := Number(Elements(PN), f -> Hex(2,f));;
Print("   DUM-G4  m=2 (u=5): T' defined=",dum4def,
      "  |ker|=",dum4ker,"  #f with Hex(2,f)=",dum4hex,"\n");

## ==========================================================================
## BLOCK VIII -- cert
## ==========================================================================
JBool := function(b) if b = true then return "true"; elif b = false then
  return "false"; else return Concatenation("\"",String(b),"\""); fi; end;;
JStr := function(s) return Concatenation("\"",String(s),"\""); end;;
JIntList := function(l) return Concatenation("[",
  JoinStringsWithSeparator(List(l,String),","),"]"); end;;

outPath := "search/certs/gtpi_closure_20260801.json";;
outJ := OutputTextFile(outPath, false);;
SetPrintFormattingStatus(outJ, false);;
AppendTo(outJ,"{");
AppendTo(outJ,"\"schema\":\"gtpi-closure/v1\",");
AppendTo(outJ,"\"generated_by\":\"search/probe/wac_v1/gtpi_closure_20260801.g\",");
AppendTo(outJ,"\"freeze_doc\":\"docs/notes/gtpi_cv9_freeze_v1.md\",");
AppendTo(outJ,"\"freeze_doc_sha256\":\"b5b3969812bc168a7995efba556e46ef217e1fd710bb66b4c6bc53b819cd539c\",");
AppendTo(outJ,"\"imported_from\":\"search/probe/wac_v1/pent_settled_cent_proofcheck2_20260731.g\",");
AppendTo(outJ,"\"imported_from_sha256\":\"9ee1d981ca126a8ebbfacd5d5a7bf8e21af6222ff2fd76dc5eae6f7bd27596f4\",");
AppendTo(outJ,"\"pre_registration_cert\":\"search/certs/pent_t2t3_v32_20260801.json\",");
AppendTo(outJ,"\"pre_registration_cert_sha256\":\"d8fe5372e0236e48b622fe117bfc9cdc98f5cd6e859f0ad8634d9b1f924cc088\",");
AppendTo(outJ,"\"level_caveat\":\"PB_3-level implemented model ONLY. Not the PB_4-level GT(K_pi) of C1 Prop 2.11 / 2008.00066.\",");
AppendTo(outJ,"\"convention\":\"T' aligned: Psi(y)|->q Psi(y)^u q^{-1}. Composition o = apply the RIGHT factor first; GAP map products are never used.\",");
AppendTo(outJ,"\"setup\":{\"QP_size\":",String(Size(QP)),
  ",\"Ader_size\":",String(Size(Ader)),
  ",\"PN_size\":",String(Size(PN)),
  ",\"N_ord\":",String(Nord),
  ",\"charm\":",JIntList(charm),
  ",\"ord_Psi_x\":",String(Order(Psi(gx))),
  ",\"ord_Psi_y\":",String(Order(Psi(gy))),
  ",\"ord_Psi_c\":",String(Order(Psi(gc))),
  ",\"exponent_QP\":",String(Exponent(QP)),"},");
AppendTo(outJ,"\"coarse\":{\"GT_N_A_size\":",String(Length(shad)),
  ",\"pre_registered_rows_match\":",JBool(preRegMatch),
  ",\"Sigma_m_sizes\":",JIntList(List(charm,m->Length(SigOf(m)))),
  ",\"S_m_sizes\":",JIntList(List(charm,m->Length(SmOf(m)))),
  ",\"Hex_picks_one_per_Cyb_coset\":",JBool(oneCoset),
  ",\"all_E_mf_well_defined\":",JBool(ForAll(phis,h->h<>fail)),
  ",\"H_size\":",String(Size(Hgrp)),
  ",\"H_IdGroup\":",JIntList(idH),
  ",\"H_structure\":",JStr(sdH),"},");
AppendTo(outJ,"\"fine\":{\"scan_universe\":\"charm x Ader (EXHAUSTIVE: Chk6 c4 is literally q in DerivedSubgroup(QP))\"",
  ",\"scan_size\":",String(Length(charm)*Size(Ader)),
  ",\"G_size\":",String(Length(Gfine)),
  ",\"rho_restricted_to_A_bijective\":",JBool(rhoA_bij),
  ",\"coarse_label_restricted_to_A_bijective\":",JBool(labA_bij),
  ",\"A_cap_ker_rho_size\":",String(AcapV),
  ",\"red_surjective\":",JBool(redSurj),
  ",\"red_injective\":",JBool(redInj),
  ",\"fibre_counts_seen\":",JIntList(Set(List(shad,z->Number(redImg,r->r=z)))),
  ",\"unit_index\":",String(unitIdx),
  ",\"Tprime_well_defined_count\":",String(Number(TpDefined,z->z)),
  ",\"Tprime_kernel_sizes\":",JIntList(Set(TpKer)),
  ",\"Tmixed_well_defined_count\":",String(Number(TmixDefined,z->z)),
  ",\"Tmixed_kernel_sizes\":",JIntList(Set(TmixKer)),"},");
AppendTo(outJ,"\"composition\":{\"pairs\":",String(nPairs),
  ",\"P_GTPI_1_shape\":",String(nP1),
  ",\"mpp_NF_equals_canon_3_53\":",String(nMppAgree),
  ",\"P_GTPI_2_closure\":",String(nClosed),
  ",\"P_GTPI_4_red_author_hom\":",String(nRedAuth),
  ",\"P_GTPI_4_red_our_hom\":",String(nRedOur),
  ",\"DUM_G2_reversed_order_in_G\":",String(nRev),
  ",\"DUM_G3_mixed_defined_pairs\":",String(nMixDefinedPair),
  ",\"DUM_G3_mixed_in_G\":",String(nMixClosed),
  ",\"closure_failure_count\":",String(Length(failRows)),"},");
AppendTo(outJ,"\"group_structure\":{\"table_total\":",JBool(tableTotal),
  ",\"associative\":",JBool(assocOK),
  ",\"latin_square\":",JBool(latinOK),
  ",\"identity_index\":",JStr(idxIdentity),
  ",\"all_have_inverses\":",JBool(invAll),
  ",\"right_regular_is_hom\":",JBool(regHomOK),
  ",\"G_IdGroup\":",JIntList(idG),
  ",\"G_structure\":",JStr(sdG),
  ",\"order_distribution\":",JStr(ordDist),
  ",\"PhiPrime_defined\":",JBool(ppDefined),
  ",\"PhiPrime_distinct\":",JBool(ppDistinct),
  ",\"PhiPrime_in_H\":",JBool(ppInH),
  ",\"PhiPrime_is_hom\":",JBool(ppHom),
  ",\"E_author_is_hom\":",JBool(eeHom),"},");
AppendTo(outJ,"\"coarse_closure\":{\"pairs\":",String(nCoarse),
  ",\"P_GTPI_7_literal_closure\":",String(nCoarseClosed),"},");
AppendTo(outJ,"\"dummies\":{\"DUM_G1_V_size\":",String(Size(Vker)),
  ",\"DUM_G1_coarse_label_unchanged\":",JBool(dumSameCoarseLabel),
  ",\"DUM_G1_rho_unchanged\":",JBool(dumSameRho),
  ",\"DUM_G1_Chk6\":\"",String(dumChk),"\"",
  ",\"DUM_G1_in_G\":",JBool(dumInG),
  ",\"DUM_G1_composition_leaves_G\":",JBool(dumClosureBreaks),
  ",\"DUM_G4_m2_Tprime_defined\":",JBool(dum4def),
  ",\"DUM_G4_m2_kernel_size\":",String(dum4ker),
  ",\"DUM_G4_m2_Hex_solutions\":",String(dum4hex),"},");
AppendTo(outJ,"\"rows\":[");
for i in [1..Length(Gfine)] do
  if i > 1 then AppendTo(outJ,","); fi;
  AppendTo(outJ,"{\"idx\":",String(i),
    ",\"m\":",String(Gm[i]),
    ",\"f_author\":",JStr(Gf[i]),
    ",\"g_rho\":",JStr(Gg[i]),
    ",\"Tprime_defined\":",JBool(TpDefined[i]),
    ",\"Tprime_kernel\":",String(TpKer[i]),
    ",\"Tmixed_defined\":",JBool(TmixDefined[i]),
    ",\"Tmixed_kernel\":",String(TmixKer[i]),"}");
od;
AppendTo(outJ,"],");
AppendTo(outJ,"\"multiplication_table\":[");
for i in [1..Length(Gfine)] do
  if i > 1 then AppendTo(outJ,","); fi;
  AppendTo(outJ,JIntList(MT[i]));
od;
AppendTo(outJ,"],");
AppendTo(outJ,"\"source_digest_sha256\":\"PENDING_POSTPROCESS\",");
AppendTo(outJ,"\"grade\":\"single GAP lane + paper. NOT cross-checked, NOT Lean-verified. CV-9 main checkpoint (non-party reading) NOT yet performed.\"");
AppendTo(outJ,"}\n");
CloseStream(outJ);
Print("\n== cert written: ",outPath," ==\n");
Print("== DONE ==\n");
QUIT;
