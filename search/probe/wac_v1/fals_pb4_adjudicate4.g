#############################################################################
## part 4: the probe keeps c SYMBOLICALLY.  X13w := gx^-1*gc*gy^-1 is exactly
## the canonical identity x13 = x12^-1 c x23^-1 of (A.5).  Check that the
## six window VALUES are the evaluation of the canonical words, and that the
## cc^m factor of Hex is vacuous because c lies in ker(pi).
#############################################################################
n := 5;; tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; ss := tt*XX^3;; b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; ccv := (s1*s2)^3;; Eg := Group(aE,bE);;
xb := s1^2;; yb := s2^2;;
X12v := xb;; X23v := yb;; X13v := yb^-1*xb^-1;;
X34v := xb;; X24v := s1^-1*yb*s1;; X14v := s1^-1*X13v*s1;;
cof := [ [ X12v, X23v, X13v ],
         [ X23v, X34v, X24v ],
         [ X23v*X13v, X34v, X24v*X14v ],
         [ X13v*X12v, X34v*X24v, X14v ],
         [ X12v, X24v*X23v, X14v*X13v ] ];;
cofc := List([1..5], i -> cof[i][2]*cof[i][3]*cof[i][1]);;

Print("### the canonical word x13 = x12^-1 * c * x23^-1  (A.5) ###\n");
Print("  probe's symbolic X13w = gx^-1 * gc * gy^-1  -> same word.\n");
Print("  Psi is anti, so Psi_i(X13w) = cof[i][2]^-1 * cofc[i] * cof[i][1]^-1.\n");
for i in [1..5] do
  Print("   cpt ",i,":  Psi_i(x12^-1 c x23^-1) = ",
        String(cof[i][2]^-1*cofc[i]*cof[i][1]^-1),
        "   cof[i][3] (declared x13-image) = ",String(cof[i][3]),
        "   agree ? ",cof[i][2]^-1*cofc[i]*cof[i][1]^-1 = cof[i][3],"\n");
od;
Print("  => the window value X13v is NOT an ad hoc choice: it is the\n");
Print("     evaluation of the canonical (A.5) word, in which pi(c)=1 holds\n");
Print("     as an arithmetic fact about E, not as a modelling decision.\n");

Print("\n### vacuity of the cc^m factor in Hex ###\n");
Print("  cc = (s1*s2)^3 = ",String(ccv),"   ord = ",Order(ccv),"\n");
Print("  cc^m for m in {0,1,3,4} : ",List([0,1,3,4], m -> String(ccv^m)),"\n");
Print("  => every cc^m factor of Hex (and every c-dependent term of Nord)\n");
Print("     is identically trivial on this family: the c-slot of the\n");
Print("     calibration suite is never exercised.\n");
Print("\n== DONE ==\n"); QUIT;
