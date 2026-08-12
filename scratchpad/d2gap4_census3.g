# [D2-GAP-4] census v3: Galois-invariants of the 3 covers with |monG|=324
# (all in the resolvent class of lambda_9). Question: are they pairwise
# distinguishable by Galois-invariants (=> each is Galois-stable => field of
# moduli of lambda_9 is Q), or are they an orbit?
SizeScreen([4096,0]);;
S3 := SymmetricGroup(3);; E3 := Elements(S3);;
THREE := Filtered(E3, g -> Order(g)=3);; TRANSP := Filtered(E3, g -> Order(g)=2);;
qX := [2,3,4,5,6,1];; qY := [1,4,5,2,3,6];;
PT := function(i,j) return 3*(i-1)+j; end;;
Build := function(alpha,beta)
  local lx,ly,i,j; lx:=[]; ly:=[];
  for i in [1..6] do for j in [1..3] do
    lx[PT(i,j)] := PT(qX[i], j^alpha[i]); ly[PT(i,j)] := PT(qY[i], j^beta[i]); od; od;
  return [PermList(lx), PermList(ly)];
end;;
LX := (1,11,8,13,6,15,4,17,2,10,9,12,7,14,5,16,3,18);;
LY := (2,9)(3,8)(4,7)(5,6)(10,17)(11,16)(12,15)(13,14);;
NormY := function(X,Y)
  local pts,p,k,rel,l,i; pts:=[1]; p:=1;
  for k in [2..18] do p := p^X; pts[k] := p; od;
  rel := []; for k in [1..18] do rel[pts[k]] := k; od;
  l := []; for i in [1..18] do l[rel[i]] := rel[i^Y]; od; return PermList(l);
end;;
std := PermList(Concatenation([2..18],[1]));;
LN := NormY(LX,LY);;
LClass := Set(List([0..17], k -> LN^(std^k)));;

found := [];;   # one representative per cover with |monG|=324
for a6 in THREE do for b1 in TRANSP do for b6 in TRANSP do
 for b2 in E3 do for b3 in E3 do
   t := Build([(),(),(),(),(),a6],[b1,b2,b3,b2^-1,b3^-1,b6]);
   z := (t[1]*t[2])^-1;
   if Order(t[1])=18 and CycleStructurePerm(t[2])=[8] and Order(z)=18 then
     G := Group(t[1],t[2]);
     if IsTransitive(G,[1..18]) and Size(G)=324 then
       ny := NormY(t[1],t[2]);
       if not ForAny(found, r -> r.ny in Set(List([0..17],k->ny^(std^k)))) then
         Add(found, rec(ny:=ny, X:=t[1], Y:=t[2], G:=G, isL:=(ny in LClass)));
       fi;
     fi;
   fi;
 od; od; od; od; od;

Print("distinct covers with |monG|=324 : ", Length(found), "\n\n");
i := 0;
for r in found do
  i := i+1;
  deck := Size(Centralizer(SymmetricGroup(18), r.G));
  Print("cover #", i, "   is lambda_9 : ", r.isL, "\n");
  Print("   StructureDescription(monG) = ", StructureDescription(r.G), "\n");
  Print("   deck (centralizer) order   = ", deck, "\n");
  Print("   |Z(monG)|                  = ", Size(Center(r.G)), "\n");
  Print("   derived series orders      = ", List(DerivedSeriesOfGroup(r.G), Size), "\n");
  Print("   #conjugacy classes of monG = ", Length(ConjugacyClasses(r.G)), "\n");
  Print("   all block sizes            = ", Set(List(AllBlocks(r.G), b->Length(b))), "\n");
  Print("   Y-normalised               = ", r.ny, "\n");
  # are the three pairwise isomorphic as permutation groups?
od;

Print("\n--- pairwise: are the 3 permutation groups conjugate in S18? ---\n");
for i in [1..Length(found)] do
 for j in [i+1..Length(found)] do
   Print("  (",i,",",j,") conjugate subgroups of S18 : ",
         RepresentativeAction(SymmetricGroup(18), found[i].G, found[j].G) <> fail, "\n");
 od;
od;

Print("\n--- are the 3 triples related by an outer symmetry (swap of branch points 0<->infty)? ---\n");
# a Galois-invariant refinement: the S18-class of the *unordered* triple under
# the S3-action on the 3 branch points is preserved by Galois; check whether the
# three covers are related by such a relabelling.
for i in [1..Length(found)] do
  X := found[i].X;; Y := found[i].Y;; Z := (X*Y)^-1;;
  Print("  cover #", i, " : perms of (X,Y,Z) giving normalised-Y classes:\n");
  for pr in [[X,Y],[Z,Y],[X^-1,Z^-1],[Y^-1,X^-1]] do
    if Order(pr[1]) = 18 then
      ny := NormY(pr[1], pr[2]);
      Print("      -> matches lambda_9 : ", ny in LClass, "\n");
    fi;
  od;
od;
QUIT;
