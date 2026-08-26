# math_gdyn_g8_decide_v1.g -- DECIDE G8 without building psi_T as a homomorphism.
#
# Theory (see report): S := psi_T(N_f)N_f/N_f <= G,  Lambda_{N_f} = 3Z^2  (since G^ab = C3 x C3).
#   (G/S)^ab = F3^2 / lambda(W),  lambda := nu o psi_T : H_T -> F3^2 ,  W := image of N_f in H_T^ab (x) F3.
#   W is a hyperplane (codim 1) because Hbar^ab (x) F3 = F3 (measured: Hbar^ab = [3]).
#   W = ker(chi), chi = the mod-3 abelianization character of Hbar pulled back to H_T.
#   lambda(W) = F3^2  <=>  ker(lambda) NOT contained in W  <=>  chi NOT in span{lambda_1, lambda_2}.
#   G solvable (order 2^6*3^2) => G/S perfect => trivial.  Hence:
#      chi in span{lambda1,lambda2}  <=>  S != G  <=>  G8 PASS.
LogTo();
A := AlternatingGroup(4);;
a := (2,3,4);; b := (1,2,3);;
F := FreeGroup("x","y");; x := F.1;; y := F.2;; z := (x*y)^-1;;
h1 := GroupHomomorphismByImages(F,A,[x,y],[a,b]);;
th := GroupHomomorphismByImages(F,F,[x,y],[y, y^-1*x^-1]);;
homs := [ h1, th*h1, (th*th)*h1 ];;
D := DirectProduct(A,A,A);;
emb := List([1..3], i -> Embedding(D,i));;
gg := function(w) local r,i; r:=One(D);
  for i in [1..3] do r := r*Image(emb[i], Image(homs[i], w)); od; return r; end;;
G := Subgroup(D,[gg(x),gg(y)]);;
pr1 := GroupHomomorphismByImages(G, A, [gg(x),gg(y)], [Image(h1,x),Image(h1,y)]);;
Hbar := Kernel(pr1);;
Print("|G|=",Size(G)," |Hbar|=",Size(Hbar)," Hbar^ab=",AbelianInvariants(Hbar),"\n");

# --- BFS: word representatives r_u for every u in A4 (w.r.t. a,b) ---
reps := rec();;
words := [ One(F) ];; elts := [ One(A) ];;
i := 1;;
while i <= Length(elts) do
  for pr in [[x,a],[y,b],[x^-1,a^-1],[y^-1,b^-1]] do
    ne := elts[i]*pr[2];
    if not ne in elts then Add(elts, ne); Add(words, words[i]*pr[1]); fi;
  od;
  i := i + 1;
od;
Print("transversal size = ", Length(elts), " (expect 12); identity word first ? ",
      words[1] = One(F), "\n");
rep := function(u) return words[Position(elts,u)]; end;;

# --- the 14 inertia words ---
Ca := Subgroup(A,[a]);; Cb := Subgroup(A,[b]);; Cz := Subgroup(A,[(a*b)^-1]);;
lc := function(H) return List(Set(List(Elements(A), u -> Set(List(Elements(H), h -> u*h)))),
                              c -> Representative(c)); end;;
cosA := Set(List(Elements(A), u -> Set(List(Elements(Ca), h -> u*h))));;
cosB := Set(List(Elements(A), u -> Set(List(Elements(Cb), h -> u*h))));;
cosZ := Set(List(Elements(A), u -> Set(List(Elements(Cz), h -> u*h))));;
Print("left cosets: |A/<a>|=",Length(cosA)," |A/<b>|=",Length(cosB)," |A/<z>|=",Length(cosZ),"\n");
inert := [];; tag := [];;
for c in cosA do u := Minimum(c); r := rep(u); Add(inert, r*x^3*r^-1); Add(tag, ["0", u]); od;
for c in cosB do u := Minimum(c); r := rep(u); Add(inert, r*y^3*r^-1); Add(tag, ["1", u]); od;
for c in cosZ do u := Minimum(c); r := rep(u); Add(inert, r*z^2*r^-1); Add(tag, ["inf", u]); od;
Print("number of inertia generators = ", Length(inert), " (expect 14)\n");
Print("all lie in H_T ? ", ForAll(inert, w -> Image(h1,w) = One(A)), "\n");
Print("their images generate Hbar ? ",
      Subgroup(G, List(inert, w -> gg(w))) = Hbar, "\n");

# --- identify the three special ones ---
r0 := x*y*x^-1;;
spec0 := x^3;;  spec1 := y^3;;  specInf := r0*y^3*r0^-1;;
posOf := function(w) return First([1..Length(inert)], i -> gg(inert[i]) = gg(w)
          and tag[i][1] = "?"); end;;
# match by (level, coset)
i0  := First([1..14], i -> tag[i][1]="0"   and tag[i][2] in Set(List(Elements(Ca), h->One(A)*h)));;
i1  := First([1..14], i -> tag[i][1]="1"   and tag[i][2] in Set(List(Elements(Cb), h->One(A)*h)));;
uinf := Image(h1, r0);;
iinf:= First([1..14], i -> tag[i][1]="1"   and tag[i][2] in Set(List(Elements(Cb), h->uinf*h)));;
Print("special indices (0-point, 1-point, inf-point) = ", [i0,i1,iinf],
      "  distinct ? ", Length(Set([i0,i1,iinf]))=3, "\n");

# --- lambda = nu o psi_T  in the 14 coordinates ---
lam1 := List([1..14], i -> 0);;  lam2 := List([1..14], i -> 0);;
lam1[i0]  := 1;  lam2[i0]  := 0;      # psi_T -> x , nu(x)=(1,0)
lam1[i1]  := 0;  lam2[i1]  := 1;      # psi_T -> y , nu(y)=(0,1)
lam1[iinf]:= 2;  lam2[iinf]:= 2;      # psi_T -> z , nu(z)=(-1,-1)=(2,2)
Print("lambda1 = ", lam1, "\nlambda2 = ", lam2, "\n");
Print("sum(lambda1) mod 3 = ", Sum(lam1) mod 3, "  sum(lambda2) mod 3 = ", Sum(lam2) mod 3,
      "  (both 0 = functional kills the product relation)\n");

# --- chi : the mod-3 abelianization character of Hbar ---
q := MaximalAbelianQuotient(Hbar);;
Ab := Image(q);;
Print("Hbar^ab as a group : order ", Size(Ab), " invariants ", AbelianInvariants(Ab), "\n");
t := First(Elements(Ab), u -> Order(u) = 3);;
chi := List(inert, w -> First([0,1,2], j -> Image(q, gg(w)) = t^j));;
Print("chi = ", chi, "\n");
Print("sum(chi) mod 3 = ", Sum(chi) mod 3, "\n");
Print("chi vanishes on the 11 non-special ? ",
      ForAll(Difference([1..14],[i0,i1,iinf]), i -> chi[i] = 0), "\n");

# --- membership test over GF(3) ---
Mat := [ lam1*One(GF(3)), lam2*One(GF(3)) ];;
Mat2 := Concatenation(Mat, [ chi*One(GF(3)) ]);;
r1 := RankMat(Mat);; r2 := RankMat(Mat2);;
Print("rank{lambda1,lambda2} = ", r1, " ; rank{lambda1,lambda2,chi} = ", r2, "\n");
Print("chi in span{lambda1,lambda2} ? ", r1 = r2, "\n");
if r1 = r2 then
  Print("=> (G/S)^ab = C3  => S <> G  => G8 PASS\n");
else
  Print("=> (G/S)^ab = trivial => G/S perfect; |G|=2^6*3^2 solvable => G/S = 1 => S = G => G8 FAIL\n");
fi;
Print("support(chi)    = ", Filtered([1..14], i -> chi[i] <> 0), "\n");
Print("support(lambda) = ", Filtered([1..14], i -> lam1[i] <> 0 or lam2[i] <> 0), "\n");
Print("supports disjoint ? ", Intersection(Filtered([1..14], i -> chi[i] <> 0),
      Filtered([1..14], i -> lam1[i] <> 0 or lam2[i] <> 0)) = [], "\n");
Print("chi supported exactly on the 6 inertia over infinity (indices 9..14) ? ",
      Filtered([1..14], i -> chi[i] <> 0) = [9..14], "\n");
Print("DONE\n");
QUIT;
