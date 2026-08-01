n := 5;; tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; ss := tt*XX^3;; b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
xb := s1^2;; yb := s2^2;; PN := Group(xb,yb);; Eg := Group(aE,bE);;
X12v := xb;; X23v := yb;; X13v := yb^-1*xb^-1;;
X34v := xb;; X24v := s1^-1*yb*s1;; X14v := s1^-1*X13v*s1;;
cof := [ [ X12v, X23v, X13v ], [ X23v, X34v, X24v ],
         [ X23v*X13v, X34v, X24v*X14v ], [ X13v*X12v, X34v*X24v, X14v ],
         [ X12v, X24v*X23v, X14v*X13v ] ];;
cofc := List([1..5], i -> cof[i][2]*cof[i][3]*cof[i][1]);;
D5 := DirectProduct(Eg,Eg,Eg,Eg,Eg);;
emb := List([1..5], i -> Embedding(D5,i));;
Pack := function(l) return Product(List([1..5], i -> Image(emb[i], l[i]))); end;;
Fw := FreeGroup("x","y","c");;
gx := GeneratorsOfGroup(Fw)[1];; gy := GeneratorsOfGroup(Fw)[2];;
gc := GeneratorsOfGroup(Fw)[3];;
Rev := function(w) local l,r; l:=LetterRepAssocWord(w); r:=Reversed(l);
  return AssocWordByLetterRep(FamilyObj(gx), r); end;;
PsiAt := function(w,i) return MappedWord(Rev(w),[gx,gy,gc],
  [cof[i][1],cof[i][2],cofc[i]]); end;;
Psi := function(w) return Pack(List([1..5], i -> PsiAt(w,i))); end;;
QP := Group(Psi(gx),Psi(gy),Psi(gc));; QF := Group(Psi(gx),Psi(gy));;
DQP := DerivedSubgroup(QP);; DQF := DerivedSubgroup(QF);;
Print("|QP|=",Size(QP),"  |QF|=",Size(QF),"\n");
Print("|[QP,QP]|=",Size(DQP),"   |[QF,QF]|=",Size(DQF),"\n");
Print("[QP,QP] = [QF,QF] ? ",DQP = DQF,"\n");
Print("Psi(c) central in QP ? ",Psi(gc) in Centre(QP),"\n");
Print("[QP,QP] <= QF ? ",IsSubgroup(QF,DQP),"\n");
Print("== DONE ==\n"); QUIT;
