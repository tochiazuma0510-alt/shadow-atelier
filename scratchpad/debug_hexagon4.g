Read("search/probe/hsp7_cond4_laneV/statemachine_lib.g");
MakeDn := function(n)
  local r, s;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  return [r, s];
end;;
MakeGn := function(n)
  local rs, r, s, x, y, tr;
  rs := MakeDn(n);  r := rs[1];  s := rs[2];
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  x := tr(r,1) * tr(s,2) * tr(s,3);
  y := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  return rec(x := x, y := y, G := Group(x, y), r:=r, tr:=tr);
end;;
gn := MakeGn(3);;
chat0 := Identity(gn.G);;
f := gn.tr(gn.r,3);; m:=2;; u:=2*m+1;;

base := [1, Identity(gn.G)];;
finv := f^-1;;

# LHS33
s := ApplyGenPow(base,1,u,gn.x,gn.y,chat0);;
s := ApplyQElt(s, finv);;
s := ApplyGenPow(s,2,u,gn.x,gn.y,chat0);;
s := ApplyQElt(s, f);;
lhs33 := s;;
Print("LHS33: t=",lhs33[1]," d=",lhs33[2],"\n");

# RHS33 variants
sA := ApplyQElt(base, finv);; sA := ApplyGenPow(sA,1,1,gn.x,gn.y,chat0);; sA := ApplyGenPow(sA,2,1,gn.x,gn.y,chat0);;
Print("f^-1 s1 s2 (base, before x^-m c^m): t=",sA[1]," d=",sA[2],"\n");

v1 := ApplyQElt(ApplyQElt(sA, gn.x^(-m)), chat0^m);;
Print("V1 (x^-m then c^m): t=",v1[1]," d=",v1[2]," match=", v1=lhs33, "\n");
v2 := ApplyQElt(ApplyQElt(sA, gn.x^(m)), chat0^m);;
Print("V2 (x^+m then c^m): t=",v2[1]," d=",v2[2]," match=", v2=lhs33, "\n");
v3 := ApplyQElt(ApplyQElt(sA, chat0^m), gn.x^(-m));;
Print("V3 (c^m then x^-m): t=",v3[1]," d=",v3[2]," match=", v3=lhs33, "\n");

# what Q-element, if any, transforms sA into lhs33 (both should be at same T since c trivial doesn't change T)
Print("sA[1]=",sA[1]," lhs33[1]=",lhs33[1],"\n");
if sA[1] = lhs33[1] then
  needed := sA[2]^-1 * lhs33[2];;
  Print("needed right-mult Q-element (sA * X = lhs33): X = ", needed, "\n");
  Print("x^m = ", gn.x^m, "   x^-m = ", gn.x^(-m), "\n");
fi;
QUIT;
