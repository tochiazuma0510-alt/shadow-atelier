#############################################################################
## search/probe/wac_v1/gtpi_pb4_window_gate_20260801.g
##  P6-2 step (1): DOES A PB_4 WINDOW EXIST?
##  Decisive test: does the B_3 -> E representation (s1,s2) extend to B_4 ?
##  If yes then pi := restriction to PB_4 is a homomorphism and ker(pi) is
##  automatically normal in B_4, i.e. ker(pi) in NFI_{PB_4}(B_4).
##  Window block imported byte-identical.  Single GAP lane. NOT a ledger claim.
#############################################################################
n := 5;; tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; ss := tt*XX^3;; b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
xb := s1^2;; yb := s2^2;; PN := Group(xb,yb);; Eg := Group(aE,bE);;
X12v := xb;; X23v := yb;; X13v := yb^-1*xb^-1;;
X34v := xb;; X24v := s1^-1*yb*s1;; X14v := s1^-1*X13v*s1;;

Print("== B_3 braid relation check ==  s1 s2 s1 = s2 s1 s2 ? ",
      s1*s2*s1 = s2*s1*s2,"\n");

## --- search for s3 in E making (s1,s2,s3) a B_4 representation ---
Print("\n== search for s3 with the B_4 braid relations ==\n");
cand := Filtered(Elements(Eg), t ->
          s2*t*s2 = t*s2*t and s1*t = t*s1);;
Print("   #{t in E : s2 t s2 = t s2 t and s1 t = t s1} = ",Length(cand),"\n");
## which of them reproduce the probe's X_{ij} via the standard A_ij words
##   A12=s1^2, A23=s2^2, A34=s3^2,
##   A13=s2 s1^2 s2^-1, A24=s3 s2^2 s3^-1, A14=s3 s2 s1^2 s2^-1 s3^-1
good := [];;
for t in cand do
  a12 := s1^2;;  a23 := s2^2;;  a34 := t^2;;
  a13 := s2*s1^2*s2^-1;;  a24 := t*s2^2*t^-1;;
  a14 := t*s2*s1^2*s2^-1*t^-1;;
  if a12=X12v and a23=X23v and a34=X34v and a24=X24v then
    Add(good,[t, a13=X13v, a14=X14v,
              Size(Group([a12,a13,a14,a23,a24,a34]))]);
  fi;
od;
Print("   #candidates reproducing X12,X23,X34,X24 exactly = ",Length(good),"\n");
for r in good do
  Print("     s3 = ",String(r[1]),"   A13 = X13v ? ",r[2],
        "   A14 = X14v ? ",r[3],"   |<A_ij>| = ",r[4],"\n");
od;
if Length(cand) > 0 then
  Print("   |<s1,s2,t>| for each t : ",
        Set(List(cand, t -> Size(Group(s1,s2,t)))),"\n");
fi;

## --- the canonical (2.4) structure already present: cof[1..5] = phi_* ---
Print("\n== canonical (2.4): the five phi maps vs the probe's cof rows ==\n");
cof := [ [ X12v, X23v, X13v ],
         [ X23v, X34v, X24v ],
         [ X23v*X13v, X34v, X24v*X14v ],
         [ X13v*X12v, X34v*X24v, X14v ],
         [ X12v, X24v*X23v, X14v*X13v ] ];;
nmphi := ["phi_123 (x12,x23,x13)",
          "phi_234 (x23,x34,x24)",
          "phi_12,3,4 (x13x23, x34, x14x24)",
          "phi_1,23,4 (x13x12, x34x24, x14)",
          "phi_1,2,34 (x12, x24x23, x14x13)"];;
pred := [ [X12v,X23v,X13v],
          [X23v,X34v,X24v],
          [X23v*X13v, X34v, X24v*X14v],
          [X13v*X12v, X34v*X24v, X14v],
          [X12v, X24v*X23v, X14v*X13v] ];;
for i in [1..5] do
  Print("   cof[",i,"] == ",nmphi[i]," ?  ",cof[i]=pred[i],"\n");
od;
Print("   <X_ij> = ",Size(Group([X12v,X13v,X14v,X23v,X24v,X34v])),
      "  == P_N ? ",Group([X12v,X13v,X14v,X23v,X24v,X34v]) = PN,"\n");
Print("\n== DONE ==\n"); QUIT;
