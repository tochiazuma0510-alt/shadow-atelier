# math_gdyn_g8_forcing_v1.g -- is S = G structurally FORCED ? (independent of psi_T's details)
# Logic: S := psi_T(N_f)N_f/N_f <= G.  G/S is a quotient of BOTH G and Hbar = H_T/N_f.
# If G and Hbar have no nontrivial common quotient, then S = G is forced.
LogTo();
A := AlternatingGroup(4);;
a := (2,3,4);; b := (1,2,3);;
F := FreeGroup("x","y");; x := F.1;; y := F.2;;
h1 := GroupHomomorphismByImages(F,A,[x,y],[a,b]);;
th := GroupHomomorphismByImages(F,F,[x,y],[y, y^-1*x^-1]);;
homs := [ h1, th*h1, (th*th)*h1 ];;
D := DirectProduct(A,A,A);;
e := List([1..3], i -> Embedding(D,i));;
gg := function(w) local r,i; r:=One(D);
  for i in [1..3] do r := r*Image(e[i], Image(homs[i], w)); od; return r; end;;
G := Subgroup(D,[gg(x),gg(y)]);;
Print("|G| = ", Size(G), "   IdGroup = ", IdGroup(G), "\n");
pr1 := GroupHomomorphismByImages(G, A, [gg(x),gg(y)], [Image(h1,x),Image(h1,y)]);;
Print("pr1 surjective ? ", Size(Image(pr1)) = 12, "\n");
Hbar := Kernel(pr1);;
Print("|Hbar| = ", Size(Hbar), "   IdGroup = ", IdGroup(Hbar), "\n");
Print("G^ab    = ", AbelianInvariants(G), "\n");
Print("Hbar^ab = ", AbelianInvariants(Hbar), "\n");
Print("3 | |Hbar^ab| ? ", ForAny(AbelianInvariants(Hbar), t -> t mod 3 = 0), "\n");
Print("|G| factors = ", Factors(Size(G)), "  G solvable ? ", IsSolvable(G), "\n");

# exhaustive common-quotient test
nG := Filtered(NormalSubgroups(G), N -> Size(N) < Size(G));;
qG := Set(List(Filtered(nG, N -> Size(G)/Size(N) <= 48), N -> IdGroup(FactorGroup(G,N))));;
nH := Filtered(NormalSubgroups(Hbar), N -> Size(N) < Size(Hbar));;
qH := Set(List(nH, N -> IdGroup(FactorGroup(Hbar,N))));;
Print("nontrivial quotients of G of order<=48 : ", qG, "\n");
Print("nontrivial quotients of Hbar           : ", qH, "\n");
common := Intersection(qG,qH);;
Print("COMMON NONTRIVIAL QUOTIENTS            : ", common, "\n");
Print("=> S = G FORCED ? ", common = [], "\n");

# ---- branch (b) prep : is the type-(3,3,3) A4-kernel already S3-stable ? ----
p333 := Filtered(Cartesian(Elements(A),Elements(A)),
        p -> Size(Subgroup(A,[p[1],p[2]]))=12 and Order(p[1])=3 and Order(p[2])=3
             and Order((p[1]*p[2])^-1)=3);;
Print("\n(3,3,3) generating pairs : ", Length(p333), "  => kernels ", Length(p333)/24, "\n");
a3 := p333[1][1];; b3 := p333[1][2];;
k1 := GroupHomomorphismByImages(F,A,[x,y],[a3,b3]);;
homs3 := [ k1, th*k1, (th*th)*k1 ];;
gg3 := function(w) local r,i; r:=One(D);
  for i in [1..3] do r := r*Image(e[i], Image(homs3[i], w)); od; return r; end;;
Q333 := Subgroup(D,[gg3(x),gg3(y)]);;
Print("|F2/N(3,3,3)sym| = ", Size(Q333), "   (12 => the (3,3,3) kernel is ALREADY S3-stable)\n");
om := GroupHomomorphismByImages(F,F,[x,y],[y,x]);;
Print("  omega-strand type = ", [Order(Image(om*k1,x)),Order(Image(om*k1,y)),
                                 Order(Image(om*k1,y^-1*x^-1))], "\n");
# verbal candidates for N_c
for n in [2,3,4] do
  Print("verbal V_", n, " = F2^", n, "[F2,F2] : index ", n^2, " (S3-stable, GT-window)\n");
od;
Print("DONE\n");
QUIT;
