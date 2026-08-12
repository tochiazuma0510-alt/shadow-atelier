# [D2-GAP-4] census v2: same as v1 but (a) imposing the FULL passport
# ((18),(2^8 1^2),(18)) and (b) recording the quadratic-resolvent invariant
#   res := ( sgn(beta_2), sgn(beta_3) )  in {+-1}^2
# which classifies the 4 double covers of E branched at {B_1,B_2}
# (= the 4 square roots of O(B_1+B_2) = the 4 points P with [2]P = Q_0).
SizeScreen([4096,0]);;

S3 := SymmetricGroup(3);;
E3 := Elements(S3);;
THREE := Filtered(E3, g -> Order(g) = 3);;
TRANSP := Filtered(E3, g -> Order(g) = 2);;
sgn := function(g) if Order(g) = 2 then return -1; else return 1; fi; end;;

qX := [2,3,4,5,6,1];;
qY := [1,4,5,2,3,6];;
PT := function(i,j) return 3*(i-1) + j; end;;

Build := function(alpha, beta)
  local lx, ly, i, j;
  lx := []; ly := [];
  for i in [1..6] do for j in [1..3] do
    lx[PT(i,j)] := PT(qX[i], j^alpha[i]);
    ly[PT(i,j)] := PT(qY[i], j^beta[i]);
  od; od;
  return [PermList(lx), PermList(ly)];
end;;

LX := (1,11,8,13,6,15,4,17,2,10,9,12,7,14,5,16,3,18);;
LY := (2,9)(3,8)(4,7)(5,6)(10,17)(11,16)(12,15)(13,14);;

NormY := function(X, Y)
  local pts, p, k, rel, l, i;
  pts := [1]; p := 1;
  for k in [2..18] do p := p^X; pts[k] := p; od;
  rel := [];
  for k in [1..18] do rel[pts[k]] := k; od;
  l := [];
  for i in [1..18] do l[ rel[i] ] := rel[ i^Y ]; od;
  return PermList(l);
end;;
std := PermList(Concatenation([2..18],[1]));;
LClass := Set(List([0..17], k -> NormY(LX,LY)^(std^k)));;

rows := [];;
for a6 in THREE do
 for b1 in TRANSP do
  for b6 in TRANSP do
   for b2 in E3 do
    for b3 in E3 do
      alpha := [(),(),(),(),(),a6];
      beta  := [b1, b2, b3, b2^-1, b3^-1, b6];
      t := Build(alpha, beta);
      z := (t[1]*t[2])^-1;
      # full passport filter
      if Order(t[1]) = 18 and CycleStructurePerm(t[2]) = [8] and Order(z) = 18 then
        G := Group(t[1], t[2]);
        if IsTransitive(G,[1..18]) then
          Add(rows, rec( res := [sgn(b2), sgn(b3)],
                         siz := Size(G),
                         isL := (NormY(t[1],t[2]) in LClass) ));
        fi;
      fi;
    od;
   od;
  od;
 od;
od;

Print("assignments passing full passport + connected = ", Length(rows),
      "   [ /6 gauge = ", Length(rows)/6, " covers ]\n\n");

Print("--- monodromy order distribution (assignments; /6 = covers) ---\n");
Print(Collected(List(rows, r -> r.siz)), "\n\n");

Print("--- resolvent class distribution (all covers) ---\n");
for r in [[1,1],[1,-1],[-1,1],[-1,-1]] do
  Print("  res=", r, " : ", Length(Filtered(rows, x -> x.res = r))/6, " covers\n");
od;

Print("\n--- the covers with |monG| = 324 ---\n");
f324 := Filtered(rows, x -> x.siz = 324);;
Print("  count = ", Length(f324)/6, " covers\n");
Print("  their resolvent classes = ", Collected(List(f324, x -> x.res)), "\n");

Print("\n--- lambda_9 itself ---\n");
fl := Filtered(rows, x -> x.isL);;
Print("  matched assignments = ", Length(fl), " (/6 = ", Length(fl)/6, " cover)\n");
Print("  |monG| = ", Set(List(fl, x -> x.siz)), "\n");
Print("  resolvent class = ", Set(List(fl, x -> x.res)), "\n");

Print("\n--- cross-tab  resolvent x |monG| (in covers) ---\n");
for r in [[1,1],[1,-1],[-1,1],[-1,-1]] do
  sub := Filtered(rows, x -> x.res = r);;
  Print("  res=", r, " : ", List(Collected(List(sub, x->x.siz)), p -> [p[1], p[2]/6]), "\n");
od;
QUIT;
