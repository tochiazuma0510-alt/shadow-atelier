## WD-4 repair attempt: compare cofc[i] against pi(c) computed INDEPENDENTLY
## from the braid representation, not derived from the rows.
n := 5;; tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; ss := tt*XX^3;; b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
xb := s1^2;; yb := s2^2;;
X12v := xb;; X23v := yb;; X13v := yb^-1*xb^-1;;
X34v := xb;; X24v := s1^-1*yb*s1;; X14v := s1^-1*X13v*s1;;
cof := [ [X12v,X23v,X13v], [X23v,X34v,X24v], [X23v*X13v,X34v,X24v*X14v],
         [X13v*X12v,X34v*X24v,X14v], [X12v,X24v*X23v,X14v*X13v] ];;
cofc := List([1..5], i -> cof[i][2]*cof[i][3]*cof[i][1]);;
X13fwd := s2*xb*s2^-1;; X14fwd := s1*X13fwd*s1^-1;; X24fwd := s1*yb*s1^-1;;
cofM := [ [X12v,X23v,X13fwd], [X23v,X34v,X24fwd],
          [X23v*X13fwd,X34v,X24fwd*X14fwd],
          [X13fwd*X12v,X34v*X24fwd,X14fwd],
          [X12v,X24fwd*X23v,X14fwd*X13fwd] ];;
cofcM := List([1..5], i -> cofM[i][2]*cofM[i][3]*cofM[i][1]);;
Print("pi(c) = (s1 s2)^3 = ",String(cc),"  order ",Order(cc),"\n");
Print("aligned cofc[i] : ",List(cofc,String),"\n");
Print("   all = pi(c) ? ",ForAll(cofc, z -> z = cc),"\n");
Print("mixed   cofc[i] : ",List(cofcM,String),"\n");
Print("   all = pi(c) ? ",ForAll(cofcM, z -> z = cc),"\n");
Print("WD-4' DISCRIMINATING ? ",
      ForAll(cofc,z->z=cc) and not ForAll(cofcM,z->z=cc),"\n");
Print("== DONE ==\n"); QUIT;
