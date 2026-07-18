# Scratch calibration: build the 12-rule Q x T model for N5 (Q=C5, phi(c)=t != 1)
# and directly test full hexagon (3.3)(3.4) for f=1, m=0..4, compare to known {0,1,3,4}
# (established independently in suite-wp1.g section 3 via a *different* 8-point rep).

# Q = C5 = {0,1,2,3,4} additive.  phi: x->2, y->2, c->1  (t^2, t^2, t^1)
np := 5;;
Qelts := [0,1,2,3,4];;
posOf := function(v) return (v mod 5) + 1; end;;
qmul := function(a,b) return (a+b) mod 5; end;;
qinv := function(a) return (5-a) mod 5; end;;
phiX := 2;; phiY := 2;; phiC := 1;;
phiXi := qinv(phiX);; phiYi := qinv(phiY);;

# Build sigma1-hat, sigma2-hat on Q x T (30 points), T-blocks 1..6 = e,s1,s2,s1s2,s2s1,Delta
# point index = (t-1)*np + i  where Qelts[i] is the Q-component
imgS1 := [];; imgS2 := [];;
for t in [1..6] do
  for i in [1..np] do
    d := Qelts[i];
    pt := (t-1)*np + i;
    # sigma1 rules (from wp2-transversal-model.md table)
    if t=1 then val:=d;                                    tp:=2;
    elif t=2 then val:=qmul(d,phiX);                        tp:=1;
    elif t=3 then val:=d;                                    tp:=5;
    elif t=4 then val:=d;                                    tp:=6;
    elif t=5 then val:=qmul(qmul(d,phiXi),qmul(phiYi,phiC)); tp:=3;   # p = x^-1 y^-1 c
    else       val:=qmul(d,phiY);                            tp:=4;
    fi;
    imgS1[pt] := (tp-1)*np + posOf(val);
    # sigma2 rules
    if t=1 then val:=d;                                    tp:=3;
    elif t=2 then val:=d;                                    tp:=4;
    elif t=3 then val:=qmul(d,phiY);                         tp:=1;
    elif t=4 then val:=qmul(qmul(d,phiYi),qmul(phiXi,phiC)); tp:=2;   # p = y^-1 x^-1 c
    elif t=5 then val:=d;                                    tp:=6;
    else       val:=qmul(d,phiX);                            tp:=5;
    fi;
    imgS2[pt] := (tp-1)*np + posOf(val);
  od;
od;
s1 := PermList(imgS1);; s2 := PermList(imgS2);;

Print("braid relation: ", s1*s2*s1 = s2*s1*s2, "\n");
GG := Group(s1,s2);;
Print("|<s1,s2>| = ", Size(GG), " (expect 30)\n");

XX := s1^2;; YY := s2^2;; CC := (s1*s2*s1)^2;;
Print("Order XX=", Order(XX), " YY=", Order(YY), " CC=", Order(CC), "\n");
Nord := Lcm(Order(XX),Order(YY),Order(CC));;
Print("N_ord = ", Nord, " (expect 5)\n");

# self-check: XX should equal "right mult by phiX at block1" i.e XX sends (d,t1)->(d+phiX,t1)
selfcheckX := true;; selfcheckY := true;; selfcheckC := true;;
for i in [1..np] do
  base := (1-1)*np+i;
  d := Qelts[i];
  if base^XX <> (1-1)*np+posOf(qmul(d,phiX)) then selfcheckX:=false; fi;
  if base^YY <> (1-1)*np+posOf(qmul(d,phiY)) then selfcheckY:=false; fi;
  if base^CC <> (1-1)*np+posOf(qmul(d,phiC)) then selfcheckC:=false; fi;
od;
Print("self-check XX matches phiX at t1 block: ", selfcheckX, "\n");
Print("self-check YY matches phiY at t1 block: ", selfcheckY, "\n");
Print("self-check CC matches phiC at t1 block: ", selfcheckC, "\n");

# full hexagon (3.3)(3.4), f=1 (identity), for m=0..4
Print("\n--- full hexagon on Q x T model, f=1 ---\n");
passingM := [];;
for m in [0..4] do
  u := 2*m+1;
  lhs33 := s1^u * s2^u;;
  rhs33 := s1*s2 * XX^(-m) * CC^m;;
  hex33 := (lhs33 = rhs33);;
  lhs34 := s2^u * s1^u;;
  rhs34 := s2*s1 * YY^(-m) * CC^m;;
  hex34 := (lhs34 = rhs34);;
  unitCond := Gcd(u,5)=1;;
  isShadow := hex33 and hex34 and unitCond;;
  if isShadow then Add(passingM, m); fi;
  Print("m=",m," u=",u," hex33=",hex33," hex34=",hex34," unit=",unitCond,"\n");
od;
Print("passing m (Q x T model): ", passingM, "\n");
Print("expected from suite-wp1.g (independent 8-point rep): [0,1,3,4]\n");
Print("MATCH: ", passingM = [0,1,3,4], "\n");
QUIT;
