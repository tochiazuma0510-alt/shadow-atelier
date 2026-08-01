n := 5;; tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; ss := tt*XX^3;; b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;;
xb := s1^2;; yb := s2^2;; Eg := Group(aE,bE);;
X13v := yb^-1*xb^-1;; X34v := xb;; X24v := s1^-1*yb*s1;; X14v := s1^-1*X13v*s1;;
t := First(Elements(Eg), z -> s2*z*s2 = z*s2*z and s1*z = z*s1);;
Print("unique t = ",String(t),"   order ",Order(t),"\n");
Print("t = s1^-1 ? ",t = s1^-1,"    t = s1 ? ",t = s1,"\n");
Print("A34 = t^2 = ",String(t^2),"   X34v = ",String(X34v),
      "   equal ? ",t^2 = X34v,"   inverse-equal ? ",t^2 = X34v^-1,"\n");
Print("A24 = t s2^2 t^-1 = ",String(t*yb*t^-1),"   X24v = ",String(X24v),
      "   equal ? ",t*yb*t^-1 = X24v,"\n");
Print("A13 = s2 s1^2 s2^-1 = ",String(s2*xb*s2^-1),"   X13v = ",String(X13v),
      "   equal ? ",s2*xb*s2^-1 = X13v,
      "   inverse-equal ? ",s2*xb*s2^-1 = X13v^-1,"\n");
Print("A14 = t s2 s1^2 s2^-1 t^-1 = ",String(t*s2*xb*s2^-1*t^-1),
      "   X14v = ",String(X14v),"   equal ? ",t*s2*xb*s2^-1*t^-1 = X14v,
      "   inverse-equal ? ",t*s2*xb*s2^-1*t^-1 = X14v^-1,"\n");
Print("<A_ij from t> size = ",
  Size(Group([xb,s2*xb*s2^-1,t*s2*xb*s2^-1*t^-1,yb,t*yb*t^-1,t^2])),"\n");
Print("== DONE ==\n"); QUIT;
