#############################################################################
## search/probe/wac_v1/pent_settled_cent_proofcheck2_20260731.g
##  Part 2 of the mathematician's verification run for
##  docs/notes/pent_settled_cent_v1.md.  Part 1
##  (pent_settled_cent_proofcheck_20260731.g) established C1/C2/C3 and then
##  exhausted the 2g heap inside an (inessential) random-free-word loop.
##  This file drops that loop and runs the remaining checks C4/C5/C6.
##  Window / cof / Psi / coarse_of / Hex / Chk6 imported byte-identical from
##  pent_settled_struct_20260731.g.  Single GAP lane. NOT a ledger claim.
#############################################################################

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
Print("== setup ==  |QP|=",Size(QP),"  kappa=",String(kappa),
      "  xb^kappa=xb^-1? ",xb^kappa=xb^-1,"  yb^kappa=yb^-1? ",yb^kappa=yb^-1,"\n");

Hex := function(m,f)
  local u; u := 2*m+1;
  return s1^u*f^-1*s2^u*f = f^-1*s1*s2*xb^(-m)*cc^m and
         f^-1*s2^u*f*s1^u = s2*s1*yb^(-m)*cc^m*f;
end;;
shad := [];;
for m in charm do for f in Elements(PN) do
  if Hex(m,f) and Group(xb,yb^f)=PN then Add(shad,[m,f]); fi;
od; od;
if Length(shad) <> 20 then Error("PRECONDITION FAIL: |GT(N_A)| <> 20"); fi;
PhiOf := function(m,f)
  local u;  u := 2*m+1;
  return GroupHomomorphismByImages(PN,PN,[xb,yb],[xb^u,(yb^u)^f]);
end;;
phis := List(shad, z -> PhiOf(z[1],z[2]));;
Hgrp := Group(phis);;
chat := PhiOf(4,());;
CHchat := Centralizer(Hgrp,chat);;
Print("  |H|=",Size(Hgrp)," |C_H(chat)|=",Size(CHchat),"\n");

## ---- Sigma_m (cheap, done before the heavy part) ----
Cy := Centralizer(PN,yb);;
SigTab := [];;
Print("\n== C5: Sigma_m ==   |C_P(yb)| = ",Size(Cy),"\n");
for m in charm do
  sm := Filtered(Elements(PN), g -> PhiOf(m,g) <> fail);
  Add(SigTab,[m,sm]);
  Print("  m=",m,"  |Sigma_m|=",Length(sm),
        "  union of right C_P(yb)-cosets? ",
          ForAll(sm, g -> ForAll(Elements(Cy), z -> z*g in sm)),
        "  kappa-conj stable? ",ForAll(sm,g->g^kappa in sm),
        "  inverse-closed? ",ForAll(sm,g->g^-1 in sm),"\n");
od;
SigOf := function(m) return First(SigTab,r->r[1]=m)[2]; end;;
SmOf := function(m) return List(Filtered(shad,z->z[1]=m),z->z[2]); end;;
for m in charm do
  Print("  m=",m,"  S_m=",List(SmOf(m),String),
        "  S_m kappa-stable? ",ForAll(SmOf(m),g->g^kappa in SmOf(m)),
        "  S_m inverse-closed? ",ForAll(SmOf(m),g->g^-1 in SmOf(m)),"\n");
od;

## ---- rebuild the 20 lifts ----
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
Print("\n== rebuilding the 20 fine lifts ==\n");
qpElts := Elements(QP);;
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
Print("  lifts rebuilt: ",Length(lift),"/20\n");
Unbind(coarseLabelOf);; Unbind(qpElts);;

## ============================================================
## C4 / C6
## ============================================================
Print("\n== C4/C6: per-row table ==\n");
Print("  m  f                g=rho(q)          Phi_mg comm  Twd |kerT| Tflip |kerT'| settled inCH selfInv finvInSm gInSig gEq\n");
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
  r := rec(m:=m, f:=String(f), g:=String(g),
           phi_mg_ok := (phimg<>fail), commutes := commQ,
           T_ok := (homT<>fail), kerT := kT,
           Tflip_ok := (homTf<>fail), kerTflip := kTf,
           settled := (homT<>fail and kT=1),
           in_CH := (PhiOf(m,f) in CHchat),
           f_self_inv := (f = f^-1),
           finv_in_Sm := (f^-1 in SmOf(m)),
           g_in_Sigma := (g in SigOf(m)),
           g_eq := (g = (f^kappa)^-1));
  Add(res,r);
  Print("  ",m,"  ",String(f,-16)," ",String(g,-16)," ",
        String(r.phi_mg_ok,-6),String(commQ,-6),
        String(r.T_ok,-5),String(kT,4),"  ",String(r.Tflip_ok,-6),String(kTf,4),"  ",
        String(r.settled,-7),String(r.in_CH,-6),String(r.f_self_inv,-8),
        String(r.finv_in_Sm,-9),String(r.g_in_Sigma,-7),String(r.g_eq,-6),"\n");
od;

Print("\n== C6 summary ==\n");
Print("  settled (probe T)                : ",Number(res,r->r.settled),"\n");
Print("  T well-defined                   : ",Number(res,r->r.T_ok),"\n");
Print("  kernel sizes seen (T well-def)   : ",
      Set(Filtered(res,r->r.T_ok), r->r.kerT),"\n");
Print("  T' (flipped) well-defined        : ",Number(res,r->r.Tflip_ok),"\n");
Print("  T' (flipped) settled             : ",
      Number(res,r->r.Tflip_ok and r.kerTflip=1),"\n");
Print("  g = (f^kappa)^-1 on all rows     : ",ForAll(res,r->r.g_eq),"\n");
Print("  settled <=> Phi_{m,g} well-def   : ",ForAll(res,r->r.settled=r.phi_mg_ok),"\n");
Print("  (T ok, not settled) <=> commutes : ",
      ForAll(res,r->(r.T_ok and not r.settled)=r.commutes),"\n");
Print("  T not well-def <=> neither       : ",
      ForAll(res,r->(not r.T_ok)=((not r.phi_mg_ok) and (not r.commutes))),"\n");
Print("  settled <=> Phi(m,f) in C_H(chat): ",ForAll(res,r->r.settled=r.in_CH),"\n");
Print("  settled <=> f self-inverse       : ",ForAll(res,r->r.settled=r.f_self_inv),"\n");
Print("  settled <=> f^-1 in S_m          : ",ForAll(res,r->r.settled=r.finv_in_Sm),"\n");
Print("  settled <=> g in Sigma_m         : ",ForAll(res,r->r.settled=r.g_in_Sigma),"\n");
Print("  in C_H(chat) <=> f self-inverse  : ",ForAll(res,r->r.in_CH=r.f_self_inv),"\n");

Print("\n== C6b: closed-form centralizer criterion ==\n");
for tr in lift do
  m := tr[1];; f := tr[2];;
  Print("   m=",m," f=",String(f,-16)," f^kappa*f^-1=",String((f^kappa)*f^-1,-14),
        " in C_P(yb)? ",String(((f^kappa)*f^-1) in Cy,-6),
        " Phi in C_H? ",String((PhiOf(m,f) in CHchat),-6),
        " f=f^-1? ",f=f^-1,"\n");
od;

Print("\n== DONE ==\n");
QUIT;
