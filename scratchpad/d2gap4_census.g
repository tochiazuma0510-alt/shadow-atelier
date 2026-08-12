# [D2-GAP-4] census: ALL degree-3 covers W -> E with the branch data forced by
# lambda_9's passport, composed with the FIXED degree-6 map E -> P^1_t.
#
# degree-6 data (measured, lambda9_passport.g):
#   qX = (1,2,3,4,5,6)   [ = local monodromy over t=0, one point of E, e=6 ]
#   qY = (2,4)(3,5)      [ over t=1: fixed pts 1,6 have e=1 (= B_1,B_2);
#                          2-cycles (2,4),(3,5) have e=2 (= B_3,B_4) ]
#   qZ = (1,6,5,2,3,4)   [ over t=infty, one point, e=6 ]
#
# degree-3 layer: blocks {(i,1),(i,2),(i,3)}; X~(i,j) = (qX i, alpha_i j),
#                 Y~(i,j) = (qY i, beta_i j).
# gauge-fix alpha_1..alpha_5 = id (spanning tree along qX). free: alpha_6, beta_1..beta_6.
# local conditions forced by lambda_9's passport ((18),(2^8 1^2),(18)):
#   Q_0  : alpha_6                 must be a 3-cycle   (total ramification)
#   B_1  : beta_1                  must be a transposition
#   B_2  : beta_6                  must be a transposition
#   B_3  : beta_4*beta_2 = id      (unramified)
#   B_4  : beta_5*beta_3 = id      (unramified)
SizeScreen([4096,0]);;

S3 := SymmetricGroup(3);;
E3 := Elements(S3);;
THREE := Filtered(E3, g -> Order(g) = 3);;
TRANSP := Filtered(E3, g -> Order(g) = 2);;

qX := [2,3,4,5,6,1];;          # i -> qX[i]
qY := [1,4,5,2,3,6];;          # (2,4)(3,5)

PT := function(i,j) return 3*(i-1) + j; end;;

Build := function(alpha, beta)
  local lx, ly, i, j;
  lx := []; ly := [];
  for i in [1..6] do
    for j in [1..3] do
      lx[PT(i,j)] := PT(qX[i], j^alpha[i]);
      ly[PT(i,j)] := PT(qY[i], j^beta[i]);
    od;
  od;
  return [PermList(lx), PermList(ly)];
end;;

# lambda_9 reference triple (measured)
LX := (1,11,8,13,6,15,4,17,2,10,9,12,7,14,5,16,3,18);;
LY := (2,9)(3,8)(4,7)(5,6)(10,17)(11,16)(12,15)(13,14);;

# normalise a triple with sigma_0 an 18-cycle: relabel so sigma_0 = (1,2,...,18),
# then two are conjugate iff the Y's agree up to <sigma_0>.
NormY := function(X, Y)
  local pts, p, k, rel, inv, l, i;
  pts := [1]; p := 1;
  for k in [2..18] do p := p^X; pts[k] := p; od;
  rel := [];                      # rel[old] = new
  for k in [1..18] do rel[pts[k]] := k; od;
  l := [];
  for i in [1..18] do l[ rel[i] ] := rel[ i^Y ]; od;
  return PermList(l);
end;;

LYn := NormY(LX, LY);;
std := PermList(Concatenation([2..18],[1]));;
LClass := Set(List([0..17], k -> LYn^(std^k)));;
Print("lambda_9 normalised-Y class size = ", Length(LClass), "\n");

nTot := 0;; nConn := 0;; sizes := [];; nMatch := 0;; matches := [];;
covers := [];;

for a6 in THREE do
 for b1 in TRANSP do
  for b6 in TRANSP do
   for b2 in E3 do
    for b3 in E3 do
      alpha := [(),(),(),(),(),a6];
      beta  := [b1, b2, b3, b2^-1, b3^-1, b6];
      t := Build(alpha, beta);
      nTot := nTot + 1;
      G := Group(t[1], t[2]);
      if IsTransitive(G, [1..18]) then
        nConn := nConn + 1;
        Add(covers, [t[1], t[2], Size(G)]);
        Add(sizes, Size(G));
        if NormY(t[1], t[2]) in LClass then
          nMatch := nMatch + 1;
          Add(matches, [a6, b1, b2, b3, b6]);
        fi;
      fi;
    od;
   od;
  od;
 od;
od;

Print("candidate assignments   = ", nTot, "\n");
Print("connected (transitive)  = ", nConn, "   [ /6 gauge = ", nConn/6, " covers ]\n");
Print("monodromy order multiset= ", Collected(sizes), "\n");
Print("triples S18-conjugate to lambda_9 = ", nMatch, "   [ /6 = ", nMatch/6, " cover(s) ]\n");

# how many connected ones have |monG| = 324 ?
n324 := Length(Filtered(covers, c -> c[3] = 324));;
Print("connected with |monG| = 324 : ", n324, "   [ /6 = ", n324/6, " cover(s) ]\n");

# sanity: check passport of every connected candidate
bad := 0;;
for c in covers do
  z := (c[1]*c[2])^-1;
  if not (Order(c[1]) = 18 and CycleStructurePerm(c[2]) = [8] and Order(z) = 18) then
    bad := bad + 1;
  fi;
od;
Print("connected candidates with WRONG passport = ", bad, "\n");
QUIT;
