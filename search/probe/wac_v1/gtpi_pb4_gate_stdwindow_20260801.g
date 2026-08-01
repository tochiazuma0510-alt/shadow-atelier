## rebuild the window from the STANDARD A_ij (via the unique B_4 extension
## sigma_3 |-> s_1) and compare with the probe's X_ij window.
n := 5;; tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; ss := tt*XX^3;; b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
xb := s1^2;; yb := s2^2;; PN := Group(xb,yb);; Eg := Group(aE,bE);;
BuildQ := function(A12,A13,A14,A23,A24,A34)
  local cof,cofc,D5,emb,Pack,Fw,gx,gy,gc,Rev,PsiAt,Psi,QP;
  cof := [ [A12,A23,A13],[A23,A34,A24],[A23*A13,A34,A24*A14],
           [A13*A12,A34*A24,A14],[A12,A24*A23,A14*A13] ];
  cofc := List([1..5], i -> cof[i][2]*cof[i][3]*cof[i][1]);
  D5 := DirectProduct(Eg,Eg,Eg,Eg,Eg);
  emb := List([1..5], i -> Embedding(D5,i));
  Pack := function(l) return Product(List([1..5],i->Image(emb[i],l[i]))); end;
  Fw := FreeGroup("x","y","c");
  gx := GeneratorsOfGroup(Fw)[1]; gy := GeneratorsOfGroup(Fw)[2];
  gc := GeneratorsOfGroup(Fw)[3];
  Rev := function(w) local l,r; l:=LetterRepAssocWord(w); r:=Reversed(l);
    return AssocWordByLetterRep(FamilyObj(gx),r); end;
  PsiAt := function(w,i) return MappedWord(Rev(w),[gx,gy,gc],
    [cof[i][1],cof[i][2],cofc[i]]); end;
  Psi := function(w) return Pack(List([1..5],i->PsiAt(w,i))); end;
  QP := Group(Psi(gx),Psi(gy),Psi(gc));
  return [Size(QP), Size(DerivedSubgroup(QP)),
          StructureDescription(DerivedSubgroup(QP)),
          Size(Centre(QP))];
end;;
## probe's assignment
pr := BuildQ(xb, yb^-1*xb^-1, s1^-1*(yb^-1*xb^-1)*s1, yb, s1^-1*yb*s1, xb);;
Print("probe X_ij  : |QP|=",pr[1]," |[QP,QP]|=",pr[2]," (",pr[3],
      ") |Z|=",pr[4],"\n");
## standard A_ij with sigma_3 |-> s1
t := s1;;
st := BuildQ(xb, s2*xb*s2^-1, t*s2*xb*s2^-1*t^-1, yb, t*yb*t^-1, t^2);;
Print("standard A_ij: |QP|=",st[1]," |[QP,QP]|=",st[2]," (",st[3],
      ") |Z|=",st[4],"\n");
Print("== DONE ==\n"); QUIT;
