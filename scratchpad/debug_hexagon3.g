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
  return rec(x := x, y := y, G := Group(x, y));
end;;
gn := MakeGn(3);;
chat0 := Identity(gn.G);;
Print("ord(x)=",Order(gn.x)," ord(y)=",Order(gn.y),"\n");

m := 5;; u := 2*m+1;; f:=Identity(gn.G);;
base := [1, Identity(gn.G)];;
s := ApplyGenPow(base,1,u,gn.x,gn.y,chat0);;
Print("s1^",u," applied to basepoint: t=",s[1]," d=",s[2],"\n");
s2 := ApplyGenPow(s,2,u,gn.x,gn.y,chat0);;
Print("then s2^",u,": t=",s2[1]," d=",s2[2]," == LHS33\n");

s3 := ApplyGenPow(base,1,1,gn.x,gn.y,chat0);;
s4 := ApplyGenPow(s3,2,1,gn.x,gn.y,chat0);;
Print("s1*s2 applied to basepoint: t=",s4[1]," d=",s4[2],"\n");
xm := gn.x^(-m);;
s5 := ApplyQElt(s4,xm);;
Print("then *x^-m: t=",s5[1]," d=",s5[2]," == RHS33\n");
QUIT;
