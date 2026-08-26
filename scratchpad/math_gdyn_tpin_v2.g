# math_gdyn_tpin_v2.g -- full-S3 symmetrized level-1 window, wreath-recursion template, FR smoke test
LogTo();
A := AlternatingGroup(4);;
els := Elements(A);;
pairs := Filtered(Cartesian(els,els), p -> Order(p[1])=3 and Order(p[2])=3 and Order(p[1]*p[2])=2);;
a := pairs[1][1];; b := pairs[1][2];;
F := FreeGroup("x","y");;
x := F.1;; y := F.2;;
h1 := GroupHomomorphismByImages(F, A, [x,y], [a,b]);;
th := GroupHomomorphismByImages(F, F, [x,y], [y, y^-1*x^-1]);;    # x->y->z->x
om := GroupHomomorphismByImages(F, F, [x,y], [y, x]);;            # x<->y
alphas := [ IdentityMapping(F), th, th*th, om, om*th, om*th*th ];;
Print("S3 endos ok : ", ForAll(alphas, m -> m <> fail), "\n");
homs := List(alphas, al -> al*h1);;
D := DirectProduct(List([1..6], i -> A));;
emb := List([1..6], i -> Embedding(D,i));;
gen := function(g)
  local r, i;
  r := One(D);
  for i in [1..6] do r := r * Image(emb[i], Image(homs[i], g)); od;
  return r;
end;;
Q6 := Subgroup(D, [gen(x), gen(y)]);;
Print("|F2/N1sym(full S3)| = ", Size(Q6), "\n");
Print("  orders of images of x,y,z = ", [Order(gen(x)),Order(gen(y)),Order(gen(y^-1*x^-1))], "\n");
Print("  abelian invariants = ", AbelianInvariants(Q6), "\n");
if Size(Q6) <= 2000 then Print("  IdGroup = ", IdGroup(Q6), "\n"); fi;

# C3-only version for comparison
D3 := DirectProduct(A,A,A);;
emb3 := List([1..3], i -> Embedding(D3,i));;
gen3 := function(g)
  local r,i; r := One(D3);
  for i in [1..3] do r := r*Image(emb3[i], Image(homs[i], g)); od;
  return r;
end;;
Q3 := Subgroup(D3,[gen3(x),gen3(y)]);;
Print("|F2/N1sym(C3 only)| = ", Size(Q3), "\n");

# ---- wreath recursion template: Q_{k+1} = image of F2 -> Q_k wr A4 ----
# demonstrated with a PLACEHOLDER psi (identity-like) purely to show the API cost;
# the real psi must come from the inertia data (see spec).
Print("---- wreath API cost probe ----\n");
W := WreathProduct(A, A);;
Print("|A4 wr A4| = ", Size(W), "  (= 12^13 ? ", Size(W) = 12^13, ")\n");

# ---- FR smoke test ----
ok := LoadPackage("fr");;
Print("fr loaded : ", ok, "\n");
if ok = true then
  M := FRMachine([[[],[1]]],[(1,2)]);;          # adding machine  a = <1,a> sigma
  Print("FRMachine built : ", M <> fail, "\n");
  e := FRElement(M,1);;
  Print("Activity level1 : ", Activity(e,1), "\n");
  Print("Activity level2 : ", Activity(e,2), "\n");
  Print("Activity level3 : ", Activity(e,3), "\n");
  Print("|<a> at level 3| = ", Size(Group(Activity(e,3))), " (expect 8)\n");
fi;
Print("DONE\n");
QUIT;
