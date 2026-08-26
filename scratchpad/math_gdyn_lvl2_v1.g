# math_gdyn_lvl2_v1.g -- (A) A4-kernel uniqueness by type, (B) 576 explained, (C) 3^5 deficit explained
LogTo();
A := AlternatingGroup(4);;
els := Elements(A);;
gen := Filtered(Cartesian(els,els), p -> Size(Subgroup(A,[p[1],p[2]])) = 12);;
Print("epimorphisms F2->A4 (generating pairs) : ", Length(gen), "\n");
types := List(gen, p -> [Order(p[1]), Order(p[2]), Order((p[1]*p[2])^-1)]);;
tset := Set(types);;
Print("types present : ", tset, "\n");
for t in tset do
  n := Number(types, s -> s = t);
  Print("  type ", t, " : ", n, " pairs  -> kernels = ", n/24, " (|Aut(A4)|=24, action free)\n");
od;

# (A) explicit check that Aut(A4) acts freely on generating pairs
aut := AutomorphismGroup(A);;
Print("|Aut(A4)| = ", Size(aut), "\n");
stabsizes := Set(List(gen, p -> Number(Elements(aut), al -> Image(al,p[1])=p[1] and Image(al,p[2])=p[2])));;
Print("stabilizer sizes of generating pairs in Aut(A4) : ", stabsizes, " (1 = free)\n");

# (B) the three type-permuted kernels and the index of their intersection
a := (2,3,4);; b := (1,2,3);;
F := FreeGroup("x","y");; x := F.1;; y := F.2;;
h1 := GroupHomomorphismByImages(F,A,[x,y],[a,b]);;
th := GroupHomomorphismByImages(F,F,[x,y],[y, y^-1*x^-1]);;
homs := [ h1, th*h1, (th*th)*h1 ];;
Print("types of the three strands (orders of images of x,y,z):\n");
for hh in homs do
  Print("   ", [Order(Image(hh,x)), Order(Image(hh,y)), Order(Image(hh,y^-1*x^-1))], "\n");
od;
D := DirectProduct(A,A,A);;
e := List([1..3], i -> Embedding(D,i));;
gg := function(w) local r,i; r:=One(D);
  for i in [1..3] do r := r*Image(e[i], Image(homs[i], w)); od; return r; end;;
Q := Subgroup(D,[gg(x),gg(y)]);;
Print("|F2/N1sym| = ", Size(Q), "   index in A4^3 = ", 1728/Size(Q), "\n");
# the single F3 relation among the three C3-quotients
# nu_i(x), nu_i(y) in F3 :  strand1 (1,-1), strand2 (1,0), strand3 (0,1)
M := [[1,-1],[1,0],[0,1]] * One(GF(3));;
Print("rank over GF(3) of the three C3-characters = ", RankMat(M), " of 3  => deficiency 3^",
      3-RankMat(M), "\n");

# (C) the 3^5 deficit of |Q2| : rank of  lambda_u = delta_{alpha(u)} - delta_{beta(u)}
Ca := Subgroup(A,[a]);; Cb := Subgroup(A,[b]);;
cosA := List(RightCosets(A,Ca), c -> AsSortedList(Elements(c)));;   # 4 vertex points
cosB := List(RightCosets(A,Cb), c -> AsSortedList(Elements(c)));;   # 4 face points
alpha := function(u) return First([1..4], i -> u in cosA[i]); end;;
beta  := function(u) return First([1..4], i -> u in cosB[i]); end;;
rows := [];;
for u in els do
  v := List([1..8], i -> 0);
  v[alpha(u)] := v[alpha(u)] + 1;
  v[4+beta(u)] := v[4+beta(u)] - 1;
  Add(rows, v*One(GF(3)));
od;
r := RankMat(rows);;
Print("rank_F3 span{ delta_alpha(u) - delta_beta(u) : u in A4 } = ", r, " of 12 coordinates\n");
Print("  => image in C3^12 has order 3^", r, " ; deficit 3^", 12-r, "\n");
Print("  predicted |Q2| = 12 * 2^24 * 3^", r, " = 2^26 * 3^", r+1, "\n");
Print("  measured  |Q2| = 440301256704 = 2^26*3^8 ? ",
      440301256704 = 2^26*3^8, "  ; predicted matches ? ", r+1 = 8, "\n");
# also: the E-part (6 points over infinity) is killed because nu(z)=0
Print("nu(z) in C3 = A4/V4 : order of image of z = ", Order(Image(h1,y^-1*x^-1)),
      " (=2 => dies in C3)\n");
Print("DONE\n");
QUIT;
