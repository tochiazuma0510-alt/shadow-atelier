# week3-psl-common.g -- shared helpers for the PSL/PGL seven-window battery (workorder 4).
# Read via: Read("search/week3-psl-common.g");
#
# Design source (spec projection only): search/manifest_spec_v2_psl.md.
# Independence note: this file builds PGL(2,q) from EXPLICIT 2x2 matrices over GF(q) acting on the
# projective line P^1(GF(q)) (q+1 points) -- no GAP library PSL()/PGL()/AutomorphismGroup() calls,
# per spec sec.4.1(a)/4.2 ("明示 2x2 行列からの直接列挙"・"AutomorphismGroup は使わず").

SizeScreen([4096, 0]);;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ================= GF(q) helper: coerce an integer 0..q-1 to a field element =================
FElt := function(q, n) return (n mod q) * One(GF(q)); end;;

# ================= projective line P^1(GF(q)): q+1 points, index 1..q+1 =================
# point 1 = infinity [1:0]; point 1+1+x = [x:1] for x in 0..q-1 (i.e. index 2+x)
MatToPerm := function(q, M)
  local n, images, i, x, a, b, c, d, num, den, img;
  n := q + 1;
  a := M[1][1];  b := M[1][2];  c := M[2][1];  d := M[2][2];
  images := [];
  # point 1: infinity -> [a:c]
  if c = Zero(GF(q)) then images[1] := 1;
  else images[1] := 2 + Int(a/c); fi;
  for x in [0..q-1] do
    num := a*FElt(q,x) + b;
    den := c*FElt(q,x) + d;
    if den = Zero(GF(q)) then images[2+x] := 1;
    else images[2+x] := 2 + Int(num/den); fi;
  od;
  return PermList(images);
end;;

# build a 2x2 matrix over GF(q) from 4 plain integers (row-major [[a,b],[c,d]])
MakeMat := function(q, a, b, c, d)
  return [[FElt(q,a),FElt(q,b)],[FElt(q,c),FElt(q,d)]];
end;;

DetMat2 := function(M) return M[1][1]*M[2][2] - M[1][2]*M[2][1]; end;;

IsSquareInGF := function(q, x)
  local g, e;
  if x = Zero(GF(q)) then return true; fi;
  for e in GF(q) do
    if e <> Zero(GF(q)) and e*e = x then return true; fi;
  od;
  return false;
end;;

# ================= canonical form (first nonzero entry -> 1) for scalar-mod dedup =================
CanonicalizeMat := function(q, M)
  local flat, i, j, first, inv;
  flat := [M[1][1],M[1][2],M[2][1],M[2][2]];
  first := 0;
  for i in [1..4] do
    if flat[i] <> Zero(GF(q)) then first := flat[i]; break; fi;
  od;
  inv := first^-1;
  return [[M[1][1]*inv, M[1][2]*inv],[M[2][1]*inv, M[2][2]*inv]];
end;;

MatKey := function(M) return [M[1][1],M[1][2],M[2][1],M[2][2]]; end;;

# ================= enumerate all of PGL(2,q) as (matrix, permutation) pairs (q+1 points) =================
BuildPGLElements := function(q)
  local elts, seen, a, b, c, d, M, det, canon, key, perm, result;
  result := [];
  seen := [];
  for a in GF(q) do
    for b in GF(q) do
      for c in GF(q) do
        for d in GF(q) do
          det := a*d - b*c;
          if det <> Zero(GF(q)) then
            M := [[a,b],[c,d]];
            canon := CanonicalizeMat(q, M);
            key := MatKey(canon);
            if not (key in seen) then
              Add(seen, key);
              perm := MatToPerm(q, canon);
              Add(result, rec(mat:=canon, perm:=perm));
            fi;
          fi;
        od;
      od;
    od;
  od;
  return result;
end;;

MatToStr := function(M)
  local ent, s, i, j, x;
  s := "[[";
  for i in [1,2] do
    if i=2 then Append(s, "],["); fi;
    for j in [1,2] do
      if j=2 then Append(s, ","); fi;
      x := IntFFE(M[i][j]);
      if x = fail then x := 0; fi;
      Append(s, String(x));
    od;
  od;
  Append(s, "]]");
  return s;
end;;

# ================= centralizer of a permutation w within a list of (mat,perm) records =================
# returns rec(order, generator_mats) -- generator_mats via GAP's own GeneratorsOfGroup on the found
# subgroup (explicit witness elements, not just the count) -- PU-F14.
CentralizerWitness := function(elemList, wPerm)
  local commuting, e, sub, gens, gensMat, g, idx;
  commuting := [];
  for e in elemList do
    if e.perm * wPerm = wPerm * e.perm then Add(commuting, e); fi;
  od;
  sub := Group(List(commuting, e -> e.perm));
  gens := GeneratorsOfGroup(sub);
  gensMat := [];
  for g in gens do
    idx := First(elemList, e -> e.perm = g);
    if idx <> fail then Add(gensMat, idx.mat); fi;
  od;
  return rec(order:=Size(sub), commuting_count:=Length(commuting), generator_mats:=gensMat);
end;;

# ================= class_coefficient: N_Ghat(w^u) = #{(r,g) in T3 x T2 : r*g = w^u} (paper product;
# GAP form per W-4/reversal: paper's "rg" = GAP's "g*r") =================
# T3/T2 built from a FULL element list (elemList: list of perms in Ghat), filtered by order.
ClassCoefficient := function(elemList, target)
  local t3, t2, r, g, count;
  t3 := Filtered(elemList, x -> Order(x) = 3);
  t2 := Filtered(elemList, x -> Order(x) = 2);
  count := 0;
  for r in t3 do
    for g in t2 do
      if g*r = target then count := count + 1; fi;   # paper "rg" -> GAP "g*r" (reversal)
    od;
  od;
  return count;
end;;

Print("week3-psl-common.g loaded.\n");
