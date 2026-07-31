#############################################################################
## search/probe/wac_v1/pent_settled_cent_proofcheck_20260731.g
##
##  Mathematician (Opus 5) verification run for docs/notes/pent_settled_cent_v1.md.
##  Purpose: machine-check every step of the PAPER proof of the settled
##  trichotomy on the pi-window, and machine-check the orientation concern.
##
##  Window / cof / Psi / coarse_of / Hex / Chk6 imported byte-identical from
##  search/probe/wac_v1/pent_settled_struct_20260731.g (which imported them
##  byte-identical from pent_t2t3_v31_20260731.g). No file is edited.
##
##  Checks (all recorded raw; the ONLY hard asserts are the two construction
##  facts already established elsewhere -- |GT(N_A)|=20 and all-20-lifted):
##   C1  Q_P = A x V with A = [Q_P,Q_P] = A5, V = Z(Q_P) = ker(rho) = C5^3.
##   C2  There is a unique kappa in S5 (acting on P=A5) with xb^kappa=xb^-1,
##       yb^kappa=yb^-1; chat := Phi(4,()) equals conjugation by kappa.
##   C3  IDENTITY  rho(q) = ( coarse_of(WordOf(q)) ^ kappa )^-1   for ALL q in Q_P.
##   C4  per row: g:=rho(q); is Phi_{m,g} a well-defined endo of P?
##                is [xb^u, (yb^u)^g] = 1 ?
##                actual T (probe convention q^-1 . q): well-defined? |ker|?
##                flipped T' (q . q^-1): well-defined? |ker|?
##   C5  Sigma_m := { g in P : Phi_{m,g} well-defined }; sizes; is it a union
##       of right cosets of C_P(yb); is it stable under kappa-conjugation.
##   C6  the three candidate criteria on the 20 rows:
##         (a) settled ?          (b) Phi(m,f) in C_H(chat) ?
##         (c) f = f^-1 ?         (d) f^-1 in S_m ?      (e) g in Sigma_m ?
##
##  Single GAP lane. NOT a ledger claim.
#############################################################################

## ---- window (byte-identical) ----
n := 5;;
tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; ss := tt*XX^3;;
b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
xb := s1^2;; yb := s2^2;; PN := Group(xb,yb);; Eg := Group(aE,bE);;
Nord := Lcm(Order(xb),Order(yb),Order(cc));;
charm := Filtered([0..Nord-1], z->GcdInt(2*z+1,Nord)=1);;
Print("== window ==  P=A5? ",PN=AlternatingGroup(5),"  |E|=",Size(Eg),
      "  N_ord=",Nord,"  charming=",charm,
      "  ord(xb)=",Order(xb)," ord(yb)=",Order(yb),"\n");

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
pr1 := Projection(D5,1);;
gensQP := [Psi(gx),Psi(gy),Psi(gc)];;
redMap := GroupHomomorphismByImages(QP, PN, gensQP, [xb,yb,()]);;
coarse_of := function(w) return MappedWord(w, [gx,gy,gc], [xb,yb,()]); end;;
Print(" |QP|=",Size(QP),"  |QF|=",Size(QF),"  ord(Psi(c))=",Order(Psi(gc)),
      "  redMap ok? ",redMap<>fail,"\n");

## ============================================================
## C1  structure  Q_P = A x V
## ============================================================
Print("\n== C1: structure of Q_P ==\n");
Ader := DerivedSubgroup(QP);;
Zc   := Centre(QP);;
Hker := Kernel(redMap);;
Print("  |[QP,QP]| = ",Size(Ader),"   struct = ",StructureDescription(Ader),"\n");
Print("  |Z(QP)|   = ",Size(Zc),"     struct = ",StructureDescription(Zc),"\n");
Print("  |ker rho| = ",Size(Hker),"   struct = ",StructureDescription(Hker),"\n");
Print("  Z(QP) = ker(rho)? ",Zc=Hker,"\n");
Print("  A cap V trivial? ",Size(Intersection(Ader,Zc))=1,
      "   |A|*|V| = |QP|? ",Size(Ader)*Size(Zc)=Size(QP),"\n");
Print("  rho|A injective onto P? ",
      Size(Image(redMap,Ader))=Size(PN)," (|image|=",Size(Image(redMap,Ader)),")\n");
Print("  C_QP(A) = V? ",Centralizer(QP,Ader)=Zc,"\n");
Print("  QP/A structure = ",StructureDescription(QP/Ader),"\n");

## ============================================================
## C2  kappa = the 'real structure' (complex conjugation on P)
## ============================================================
Print("\n== C2: kappa inverting both generators ==\n");
kapCands := Filtered(Elements(SymmetricGroup(5)),
              k -> xb^k = xb^-1 and yb^k = yb^-1);;
Print("  #{k in S5 : xb^k=xb^-1, yb^k=yb^-1} = ",Length(kapCands),
      "  -> ",List(kapCands,String),"\n");
kappa := kapCands[1];;
Print("  kappa = ",String(kappa),"  order=",Order(kappa),
      "  in A5? ",kappa in PN,"  |C_S5(kappa)|=",
      Size(Centralizer(SymmetricGroup(5),kappa)),"\n");

## ---- coarse shadows (byte-identical Hex) ----
Hex := function(m,f)
  local u; u := 2*m+1;
  return s1^u*f^-1*s2^u*f = f^-1*s1*s2*xb^(-m)*cc^m and
         f^-1*s2^u*f*s1^u = s2*s1*yb^(-m)*cc^m*f;
end;;
shad := [];;
for m in charm do for f in Elements(PN) do
  if Hex(m,f) and Group(xb,yb^f)=PN then Add(shad,[m,f]); fi;
od; od;
Print("  |GT(N_A)| = ",Length(shad),"\n");
if Length(shad) <> 20 then Error("PRECONDITION FAIL: |GT(N_A)| <> 20"); fi;

## Phi(m,f) as an automorphism of P
PhiOf := function(m,f)
  local u;  u := 2*m+1;
  return GroupHomomorphismByImages(PN,PN,[xb,yb],[xb^u,(yb^u)^f]);
end;;
phis := List(shad, z -> PhiOf(z[1],z[2]));;
Print("  all 20 Phi well-defined? ",ForAll(phis,p->p<>fail),
      "   all bijective? ",ForAll(phis,p->IsBijective(p)),"\n");
Hgrp := Group(phis);;
Print("  |H| = ",Size(Hgrp),"  struct = ",StructureDescription(Hgrp),
      "  #distinct Phi = ",Length(Set(phis)),"\n");
chatIdx := First([1..20], i -> shad[i][1]=4 and shad[i][2]=());;
chat := phis[chatIdx];;
Print("  chat = Phi(4,()) order = ",Order(chat),
      "   chat = conj by kappa? ",
      ForAll(GeneratorsOfGroup(PN), g -> Image(chat,g) = g^kappa),"\n");
CHchat := Centralizer(Hgrp,chat);;
Print("  |C_H(chat)| = ",Size(CHchat)," struct = ",StructureDescription(CHchat),"\n");

## ============================================================
## C3  IDENTITY  rho(q) = ( coarse_of(WordOf(q)) ^ kappa )^-1
## ============================================================
Print("\n== C3: orientation identity on ALL of Q_P ==\n");
epiP := GroupHomomorphismByImages(Fw, QP, [gx,gy,gc], gensQP);;
WordOf := function(q) return Rev(PreImagesRepresentative(epiP,q)); end;;
qpElts := Elements(QP);;
badId := 0;;
for q in qpElts do
  w := WordOf(q);
  if Image(redMap,q) <> (coarse_of(w)^kappa)^-1 then badId := badId + 1; fi;
od;
Print("  checked ",Length(qpElts)," elements of Q_P;  mismatches = ",badId,"\n");
## also: the raw word-level identity on random words
badW := 0;;
for i in [1..300] do
  w := PseudoRandom(Fw);
  if coarse_of(Rev(w)) <> (coarse_of(w)^kappa)^-1 then badW := badW + 1; fi;
od;
Print("  word-level identity coarse_of(Rev(w)) = (coarse_of(w)^kappa)^-1 :",
      "  300 random words, mismatches = ",badW,"\n");

## ============================================================
## rebuild the 20 lifts exactly as the struct probe does
## ============================================================
X13w := gx^-1*gc*gy^-1;;
SubW := function(w, ix, iy, ic) return MappedWord(w,[gx,gy,gc],[ix,iy,ic]); end;;
Aut1 := function(w) return SubW(w, gx, gy^-1*X13w*gy, gc); end;;
Aut2 := function(w) return SubW(w, X13w, gy, gc); end;;
Pent := function(w)
  local v; v := List([1..5], i -> PsiAt(w,i));
  return v[1]*v[4]*v[2] = v[3]*v[5];
end;;
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
  c4 := (q in DerivedSubgroup(QP));
  sb := Group(Psi(gx^u), Psi(w^-1*gy^u*w));
  c5 := (Size(sb) = Size(QF));
  return [c1,c2,c3,c4,c5, c1 and c2 and c3 and c4 and c5];
end;;
coarseLabelOf := List(qpElts, q -> coarse_of(WordOf(q)));;
lift := [];;
for z in shad do
  fibIdx := Filtered([1..Length(qpElts)], idx -> coarseLabelOf[idx] = z[2]);
  fib := List(fibIdx, idx -> qpElts[idx]);
  tab := List(fib, q -> Chk6(z[1],q));
  witIdx := First([1..Length(fib)], i -> tab[i][6]);
  if witIdx = fail then Error("lift missing for ",z); fi;
  Add(lift,[z[1],z[2],fib[witIdx]]);
od;
Print("\n  rebuilt lifts: ",Length(lift),"/20\n");
if Length(lift) <> 20 then Error("PRECONDITION FAIL: not all 20 lifted"); fi;

## ============================================================
## C5  Sigma_m
## ============================================================
Print("\n== C5: Sigma_m = { g in P : Phi_{m,g} well-defined } ==\n");
Sig := rec();;
Cy := Centralizer(PN,yb);;
Print("  |C_P(yb)| = ",Size(Cy),"\n");
SigTab := [];;
for m in charm do
  sm := Filtered(Elements(PN), g -> PhiOf(m,g) <> fail);
  Add(SigTab,[m,sm]);
  Print("  m=",m,"  |Sigma_m| = ",Length(sm),
        "   union of right cosets of C_P(yb)? ",
        ForAll(sm, g -> ForAll(Elements(Cy), z -> z*g in sm)),
        "   kappa-conj stable? ",ForAll(sm,g->g^kappa in sm),
        "   inverse-closed? ",ForAll(sm,g->g^-1 in sm),"\n");
od;
SigOf := function(m) return First(SigTab,r->r[1]=m)[2]; end;;
SmOf := function(m) return List(Filtered(shad,z->z[1]=m),z->z[2]); end;;
for m in charm do
  Print("  m=",m,"  S_m = ",List(SmOf(m),String),
        "   S_m kappa-stable? ",ForAll(SmOf(m),g->g^kappa in SmOf(m)),"\n");
od;

## ============================================================
## C4 + C6  the 20 rows
## ============================================================
Print("\n== C4/C6: per-row table ==\n");
Print("  m   f                  g=rho(q)          Phi_mg  comm  Twd |kerT| Tflip |kerT'| settled  inCH  fSelfInv  finvInSm  gInSigma\n");
res := [];;
for tr in lift do
  m := tr[1];; f := tr[2];; q := tr[3];; u := 2*m+1;;
  g := Image(redMap,q);
  phimg := PhiOf(m,g);
  commQ := Comm(xb^u, (yb^u)^g) = ();
  homT  := GroupHomomorphismByImages(QP,QP,gensQP,
             [Psi(gx)^u, q^-1*Psi(gy)^u*q, Psi(gc)^u]);
  homTf := GroupHomomorphismByImages(QP,QP,gensQP,
             [Psi(gx)^u, q*Psi(gy)^u*q^-1, Psi(gc)^u]);
  if homT = fail then kT := -1; else kT := Size(Kernel(homT)); fi;
  if homTf = fail then kTf := -1; else kTf := Size(Kernel(homTf)); fi;
  phimf := PhiOf(m,f);
  r := rec(m:=m, f:=String(f), g:=String(g),
           phi_mg_ok := (phimg<>fail),
           commutes := commQ,
           T_ok := (homT<>fail), kerT := kT,
           Tflip_ok := (homTf<>fail), kerTflip := kTf,
           settled := (homT<>fail and kT=1),
           in_CH := (phimf in CHchat),
           f_self_inv := (f = f^-1),
           finv_in_Sm := (f^-1 in SmOf(m)),
           g_in_Sigma := (g in SigOf(m)),
           g_eq_kappaf_inv := (g = (f^kappa)^-1));
  Add(res,r);
  Print("  ",m,"  ",String(f,-18)," ",String(g,-16)," ",
        String(r.phi_mg_ok,-6)," ",String(commQ,-5)," ",
        String(r.T_ok,-4),String(kT,6)," ",String(r.Tflip_ok,-5),String(kTf,7),"  ",
        String(r.settled,-8),String(r.in_CH,-6),String(r.f_self_inv,-10),
        String(r.finv_in_Sm,-10),String(r.g_in_Sigma,-8),"\n");
od;

Print("\n== C6 summary ==\n");
Print("  rows                     : ",Length(res),"\n");
Print("  settled (probe T)        : ",Number(res,r->r.settled),"\n");
Print("  T well-defined           : ",Number(res,r->r.T_ok),"\n");
Print("  T' (flipped) welldef     : ",Number(res,r->r.Tflip_ok),"\n");
Print("  T' (flipped) settled     : ",Number(res,r->r.Tflip_ok and r.kerTflip=1),"\n");
Print("  g = (f^kappa)^-1 all rows: ",ForAll(res,r->r.g_eq_kappaf_inv),"\n");
Print("  settled <=> Phi_mg ok    : ",ForAll(res,r->r.settled=r.phi_mg_ok),"\n");
Print("  (not settled & T ok) <=> commutes : ",
      ForAll(res,r->(r.T_ok and not r.settled)=(r.commutes and not r.phi_mg_ok)),"\n");
Print("  T not well-def <=> (not Phi_mg ok and not commutes): ",
      ForAll(res,r->(not r.T_ok)=((not r.phi_mg_ok) and (not r.commutes))),"\n");
Print("  settled <=> in C_H(chat) : ",ForAll(res,r->r.settled=r.in_CH),"\n");
Print("  settled <=> f self-inv   : ",ForAll(res,r->r.settled=r.f_self_inv),"\n");
Print("  settled <=> f^-1 in S_m  : ",ForAll(res,r->r.settled=r.finv_in_Sm),"\n");
Print("  settled <=> g in Sigma_m : ",ForAll(res,r->r.settled=r.g_in_Sigma),"\n");
Print("  in C_H <=> f self-inv    : ",ForAll(res,r->r.in_CH=r.f_self_inv),"\n");

## extra: is  Phi(m,f) in C_H(chat)  <=>  chat(f) f^-1 in C_P(yb) ?
Print("\n== C6b: centralizer criterion in closed form ==\n");
Print("  Phi in C_H(chat) <=> f^kappa * f^-1 in C_P(yb) : ",
      ForAll(res, r -> r.in_CH), " (all-settled-rows check below)\n");
for tr in lift do
  m := tr[1];; f := tr[2];;
  Print("   m=",m," f=",String(f,-16)," f^kappa*f^-1 = ",
        String((f^kappa)*f^-1,-14)," in C_P(yb)? ",((f^kappa)*f^-1) in Cy,
        "   Phi in C_H? ",(PhiOf(m,f) in CHchat),"\n");
od;

Print("\n== DONE ==\n");
QUIT;
