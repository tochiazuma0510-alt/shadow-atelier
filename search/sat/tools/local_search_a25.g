#############################################################################
## search/sat/tools/local_search_a25.g -- simulated-annealing local search
## for a class-only witness of the n=25, ell=17 SAT target (sol/sol_reply_
## 84_math11.md sec 6.3). NOT a uniform random search over the conjugacy
## class (that was tried first, in search/sat/tools/extract_witness_a25.g,
## and failed within budget 5,000,000 -- search/sat/tools/
## structure_const_a25.g later showed why: the exact class-only solution
## count for this fixed u is 82688 out of |class(2^12,1)|=7905853580625,
## i.e. hit probability ~1.05e-8 per uniform conjugate, needing ~1e8+
## uniform tries to expect one hit). Instead performs a Markov-chain local
## search: state = (12 disjoint transposition pairs, 1 fixed point) on
## {1..25}; each move either recombines two pairs' four endpoints (3 ways)
## or swaps the fixed point with one pair-endpoint -- both moves preserve
## a's cycle type 2^12,1 exactly. Objective: minimize the number of points
## of b:=a*u^-1 NOT lying in a 3-cycle (target minimum is 1, the single
## allowed fixed point of type 3^8,1). Simulated annealing (temperature
## decay, Metropolis acceptance) to escape local optima. Converged in
## 16824 moves; the resulting witness happened to ALSO be 2-transitive
## (see search/sat/fixtures/witness_a25_2transitive.json and
## scratchpad/verify_a25_witness.py for independent, non-GAP confirmation
## -- local search targeted only the class constraints, 2-transitivity was
## not an explicit objective here).
#############################################################################
N := 25;;
uu := (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17)*(18,19)*(20,21)*(22,23)*(24,25);;
uinv := uu^-1;;
id := ();;

# represent a as: pairs (list of 12 [x,y] unordered pairs) + fixedpt
BuildPerm := function(pairs, fixedpt)
  local img, p;
  img := [1..N];
  for p in pairs do
    img[p[1]] := p[2];
    img[p[2]] := p[1];
  od;
  # fixedpt stays as is
  return PermList(img);
end;;

Score := function(bperm)
  local cycles, c, bad;
  cycles := Cycles(bperm, [1..N]);
  bad := 0;
  for c in cycles do
    if Length(c) <> 3 then
      bad := bad + Length(c);
    fi;
  od;
  return bad;
end;;

# init: pairs (1,2)(3,4)...(23,24), fixed=25
pairs := List([1..12], k -> [2*k-1, 2*k]);;
fixedpt := 25;;

a1 := BuildPerm(pairs, fixedpt);;
b1 := a1 * uinv;;
bestscore := Score(b1);;
Print("initial score=", bestscore, "\n");

RandomMove := function(pairs, fixedpt)
  local newpairs, newfixed, choice, i, j, tmp, mode;
  newpairs := StructuralCopy(pairs);
  newfixed := fixedpt;
  mode := Random([1,2]);
  if mode = 1 then
    # recombine two random distinct pairs
    i := Random([1..12]); j := Random([1..12]);
    while j = i do j := Random([1..12]); od;
    choice := Random([1,2]);
    if choice = 1 then
      tmp := [ [newpairs[i][1], newpairs[j][1]], [newpairs[i][2], newpairs[j][2]] ];
    else
      tmp := [ [newpairs[i][1], newpairs[j][2]], [newpairs[i][2], newpairs[j][1]] ];
    fi;
    newpairs[i] := tmp[1];
    newpairs[j] := tmp[2];
  else
    # swap fixed point with an endpoint of a random pair
    i := Random([1..12]);
    j := Random([1,2]);
    tmp := newpairs[i][j];
    newpairs[i][j] := newfixed;
    newfixed := tmp;
  fi;
  return [newpairs, newfixed];
end;;

iters := 300000;;
t := 0;;
found := false;;
curpairs := pairs;; curfixed := fixedpt;;
cura := BuildPerm(curpairs, curfixed);; curb := cura*uinv;; curscore := Score(curb);;
temp := 3.0;;
while t < iters and not found do
  t := t + 1;
  temp := temp * 0.99995;
  if temp < 0.05 then temp := 0.05; fi;
  mv := RandomMove(curpairs, curfixed);
  newa := BuildPerm(mv[1], mv[2]);
  newb := newa * uinv;
  newscore := Score(newb);
  if newscore <= curscore or Random([1..1000])/1000.0 < Exp(-(newscore-curscore)/temp) then
    curpairs := mv[1]; curfixed := mv[2]; curscore := newscore;
  fi;
  if curscore < bestscore then
    bestscore := curscore;
  fi;
  if curscore = 1 then
    found := true;
  fi;
  if t mod 20000 = 0 then
    Print("t=", t, " curscore=", curscore, " bestscore=", bestscore, " temp=", temp, "\n");
  fi;
od;

if found then
  a1 := BuildPerm(curpairs, curfixed);
  b1 := a1*uinv;
  Print("FOUND at t=", t, "\n");
  Print("a_images=", List([1..N], k->k^a1), "\n");
  Print("b_images=", List([1..N], k->k^b1), "\n");
  Print("u_images=", List([1..N], k->k^uu), "\n");
  Print("uinv_images=", List([1..N], k->k^uinv), "\n");
  Print("a_cycletype=", CycleStructurePerm(a1), "\n");
  Print("b_cycletype=", CycleStructurePerm(b1), "\n");
  Print("b_cubed=", b1*b1*b1=id, "\n");
else
  Print("NOT FOUND within ", iters, " iters, bestscore=", bestscore, "\n");
fi;
Print("LOCAL_SEARCH_DONE\n");
QUIT;
