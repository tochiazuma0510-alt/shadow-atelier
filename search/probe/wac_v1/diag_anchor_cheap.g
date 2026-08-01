SizeScreen([4096,0]);;
n := 24;;
a1 := ( 1,13)( 2, 9)( 3, 5)( 4,24)( 6, 8)( 7,21)(10,12)(11,20)(14,16)(15,22)(17,19)(18,23);;
b1 := ( 1,12, 9)( 2, 8, 5)( 3, 4,24)( 6, 7,21)(10,11,20)(13,19,16)(14,15,22)(17,18,23);;
Snn := SymmetricGroup(n);;
aE := a1*(25,27);;  bE := b1*(25,27,26);;
s1 := bE^-1*aE;;  s2 := aE*bE^2;;
x := s1^2;;  y := s2^2;;
P := Group(x,y);;
w0 := b1^-1*a1;; v := a1*b1^-1;;
Print("braid ", s1*s2*s1 = s2*s1*s2, "  P=A24 ", P = AlternatingGroup(24),
      "  x=w0^2 ", x = w0^2, "  y=v^2 ", y = v^2, "\n");
Print("Fix(x)=", Difference([1..24],MovedPoints(x)), "  Fix(y)=", Difference([1..24],MovedPoints(y)), "\n");

Cw := Centralizer(Snn,x);;  Cv := Centralizer(Snn,y);;
Ca := Centralizer(Snn,a1);;
Print("|Cw|=",Size(Cw)," |Cv|=",Size(Cv),
      " |Cw cap Cv|=",Size(Intersection(Cw,Cv)),
      " |Cv cap C(a1)|=",Size(Intersection(Cv,Ca)),
      " |Cw cap C(a1)|=",Size(Intersection(Cw,Ca)),"\n");

## SURV family (handwritten orientation), f_z = (a1^z)*a1
Fl := List(Elements(Cv), z -> (a1^z)*a1);;
Fs := Set(Fl);;
Print("|F| distinct = ", Length(Fs), "  (out of 2280 parameters z)\n");

## M-test = handwritten literal (3.3)(3.4) at m=0
Mtest := function(f) return s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f; end;;
GenM := function(f) return Group(x, y^f) = P; end;;
Print("F passes M-hex: ", Number(Fs, Mtest), " / ", Length(Fs),
      "   +gen: ", Number(Fs, f -> Mtest(f) and GenM(f)), "\n");

## J-test = judge orientation (AbstractProd reversed products), m=0
AP := function(l) local val,i; val := l[1]^0;
  for i in [Length(l),Length(l)-1..1] do val := val*l[i]; od; return val; end;;
Dlt := AP([s1,s2,s1]);;  dlt := AP([s1,s2]);;  cc := Dlt^2;;
TTf := function(g) return AP([dlt,g,dlt^-1]); end;;
THf := function(g) return AP([Dlt,g,Dlt^-1]); end;;
RtOf0 := function(f) local Wd; Wd := AP([y^0,f]);
  return AP([TTf(TTf(Wd)),TTf(Wd),Wd]); end;;
Jtest := function(f) return AP([f,THf(f)]) = Identity(Group(s1,s2)) and RtOf0(f) = cc^0; end;;
Print("c = Identity ? ", cc = Identity(Group(s1,s2)), "\n");
Print("F passes J: ", Number(Fs, Jtest), " / ", Length(Fs),
      "    F^-1 passes J: ", Number(Fs, f -> Jtest(f^-1)), " / ", Length(Fs), "\n");

## F cap F^-1
FinvS := Set(List(Fs, f -> f^-1));;
FFint := Intersection(Fs, FinvS);;
Print("|F cap F^-1| = ", Size(FFint), "\n");

## which z produce the orientation-symmetric part?
Fixy := Difference([1..24], MovedPoints(y));;
S5v := SymmetricGroup(Fixy);;
zs := Filtered(Elements(Cv), z -> (((a1^z)*a1) in FinvS));;
Print("|{z in Cv : f_z in F cap F^-1}| = ", Length(zs),
      "   = Sym(Fix(y)) ? ", Set(zs) = Set(Elements(S5v)), "\n");
Print("  that z-set is a subgroup? ", IsGroup(Group(zs)) and Size(Group(zs)) = Length(zs),
      "  |<zs>|=", Size(Group(zs)), "  structure ", StructureDescription(Group(zs)), "\n");

## membership in the two candidate-generation sets
orb := Set(List(Elements(Cw), s -> y^s));;
Print("|orb of y under Cw| = ", Length(orb), "\n");
Print("F subset S_lit  (y^f     in orb): ", Number(Fs, f -> (y^f)      in orb), " / ", Length(Fs), "\n");
Print("F subset S_code (y^(f^-1) in orb): ", Number(Fs, f -> (y^(f^-1)) in orb), " / ", Length(Fs), "\n");
Print("F cap F^-1 subset S_code ? ", ForAll(FFint, f -> (y^(f^-1)) in orb), "\n");
Print("DIAG_CHEAP_DONE\n");
QUIT;
