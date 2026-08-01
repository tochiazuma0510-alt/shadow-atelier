#############################################################################
## part 5: EXACT kernel identity (no sampling).
##
##  Psi_probe(w) = Psi_canon(Rev w), Rev = letter reversal (anti-automorphism
##  of F fixing the generators).  Write iota(w):=w^-1 (anti-automorphism).
##  Then beta := Rev o iota is an AUTOMORPHISM of F with beta(g)=g^-1 on each
##  free generator, and for any subgroup K (automatically inverse-closed)
##        Rev(K) = iota(beta(K)) = beta(K).
##  Hence   ker(Psi_probe) = Rev(ker Psi_canon) = beta(ker Psi_canon),
##  and     ker(Psi_probe) = ker(Psi_canon)
##    <=>   beta descends to Q, i.e. g |-> g^-1 on the three generator images
##          extends to an automorphism of Q.
##  So the whole question reduces to ONE finite check.
#############################################################################
n := 5;; tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; ss := tt*XX^3;; b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; Eg := Group(aE,bE);;
xb := s1^2;; yb := s2^2;; t := s1;; sig := [s1,s2,t];;
PiX := function(i,j) local w,k; w:=sig[i]^2;
  for k in [i+1..j-1] do w:=sig[k]*w*sig[k]^-1; od; return w; end;;
D5 := DirectProduct(Eg,Eg,Eg,Eg,Eg);;
emb := List([1..5], i -> Embedding(D5,i));;
Pk := function(l) return Product(List([1..5],i->Image(emb[i],l[i]))); end;;
G := rec(x12:=PiX(1,2),x23:=PiX(2,3),x13:=PiX(1,3),
         x14:=PiX(1,4),x24:=PiX(2,4),x34:=PiX(3,4));;
triF := [ [ G.x12, G.x23, G.x13 ],
          [ G.x23, G.x34, G.x24 ],
          [ G.x13*G.x23, G.x34, G.x14*G.x24 ],
          [ G.x12*G.x13, G.x24*G.x34, G.x14 ],
          [ G.x12, G.x23*G.x24, G.x13*G.x14 ] ];;
Cim := List([1..5], i -> triF[i][1]*triF[i][3]*triF[i][2]);;
PXc := Pk(List([1..5],i->triF[i][1]));;
PYc := Pk(List([1..5],i->triF[i][2]));;
PCc := Pk(Cim);;
Q := Group(PXc,PYc,PCc);;
Print("|Q| = ",Size(Q),"\n");
beta := GroupHomomorphismByImages(Q,Q,[PXc,PYc,PCc],
                                     [PXc^-1,PYc^-1,PCc^-1]);;
if beta = fail then
  Print("beta does NOT descend  =>  ker(Psi_probe) <> ker(Psi_canon)\n");
else
  Print("beta descends to Q.   injective ? ",IsInjective(beta),
        "   surjective ? ",IsSurjective(beta),
        "   |ker| = ",Size(Kernel(beta)),"\n");
  Print("beta is an automorphism of Q ? ",IsBijective(beta),"\n");
  if IsBijective(beta) then
    Print("=>  Rev(ker Psi_canon) = ker Psi_canon  EXACTLY.\n");
    Print("=>  N_{PB3}^{probe} = N_{PB3}^{canon} as subgroups of PB3.\n");
  fi;
fi;
## and the same for the probe's own (anti) presentation, for symmetry
Print("\nsanity: beta^2 = id ? ",
      ForAll([PXc,PYc,PCc], g -> Image(beta,Image(beta,g)) = g),"\n");
Print("\n== DONE ==\n"); QUIT;
