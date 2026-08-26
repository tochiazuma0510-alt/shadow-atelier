# math_gdyn_tpin_v1.g -- infinity-orbit pin check + S3-symmetrized level-1 window order
# author: mathematician (Opus 5). small verification script, integer/finite-group only.
LogTo();
A := AlternatingGroup(4);;
els := Elements(A);;
pairs := Filtered(Cartesian(els,els), p -> Order(p[1])=3 and Order(p[2])=3 and Order(p[1]*p[2])=2);;
Print("PAIRS(a,b) order3,order3,ab order2 : ", Length(pairs), "\n");

# (1) universal claim: a*b*a^-1 is never in <a>
bad := 0;;
for p in pairs do
  if p[1]*p[2]*p[1]^-1 in Subgroup(A,[p[1]]) then bad := bad+1; fi;
od;
Print("CLAIM1 a*b*a^-1 in <a> counterexamples : ", bad, " / ", Length(pairs), "\n");

# (2) universal claim: b itself is never in <a>  (=> r=y is also invalid)
bad2 := 0;;
for p in pairs do
  if p[2] in Subgroup(A,[p[1]]) then bad2 := bad2+1; fi;
od;
Print("CLAIM2 b in <a> counterexamples : ", bad2, " / ", Length(pairs), "\n");

# (3) explicit model: the coset {g : g b g^-1 in <a>}
a := pairs[1][1];; b := pairs[1][2];;
Ca := Subgroup(A,[a]);;
S := Filtered(els, g -> g*b*g^-1 in Ca);;
Print("MODEL a=",a," b=",b," ab=",a*b,"\n");
Print("S = {g : g b g^-1 in <a>} size ", Length(S), " : ", S, "\n");
Print("  a in S ? ", a in S, "\n");
Print("  b in S ? ", b in S, "\n");
Print("  a*b*a^-1 in S ? ", a*b*a^-1 in S, "\n");
Print("  S = <a>*s0 ? ", AsSortedList(S) = AsSortedList(List(Elements(Ca), u -> u*S[1])), "\n");
Print("  S = s0*<b> ? ", AsSortedList(S) = AsSortedList(List(Elements(Subgroup(A,[b])), u -> S[1]*u)), "\n");

# (4) S3-symmetrized level-1 window  N1sym = intersection of the 3 kernels
F := FreeGroup("x","y");;
x := F.1;; y := F.2;;
h1 := GroupHomomorphismByImages(F, A, [x,y], [a,b]);;
th := GroupHomomorphismByImages(F, F, [x,y], [y, y^-1*x^-1]);;   # x->y, y->z
Print("theta is endo? ", th <> fail, "  theta^3 = id on x ? ",
      Image(th, Image(th, Image(th, x))) = x, "\n");
th2 := th*th;;
h2 := th*h1;;    # GAP: f*g means "apply f then g"
h3 := th2*h1;;
D := DirectProduct(A,A,A);;
e1 := Embedding(D,1);; e2 := Embedding(D,2);; e3 := Embedding(D,3);;
gen := function(g)
  return Image(e1, Image(h1,g)) * Image(e2, Image(h2,g)) * Image(e3, Image(h3,g));
end;;
Q := Subgroup(D, [gen(x), gen(y)]);;
Print("|F2/N1sym| = ", Size(Q), "   (upper bound 12^3 = 1728)\n");
Print("  index in A4^3 = ", 1728/Size(Q), "\n");
Print("  Q abelianized = ", AbelianInvariants(Q), "\n");
Print("  images of x,y,z orders = ", [Order(gen(x)), Order(gen(y)), Order(gen(y^-1*x^-1))], "\n");
Print("  |F2/N1| = ", Size(A), "\n");

# (5) fr package availability
ok := LoadPackage("fr");;
Print("LOADPACKAGE fr : ", ok, "\n");
if ok = true then
  Print("fr version : ", InstalledPackageVersion("fr"), "\n");
fi;
Print("DONE\n");
QUIT;
