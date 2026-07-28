# sgnc_check2.g -- general-k check of  Phi_{2n-1,f} = inn_paper( ((1-2k)e1) q3 )
# and of what the fixture-style raw decomposition would report.  ASCII only.
SizeScreen([4096, 0]);;
AbstractProd := function(list)
  local val, i;
  val := list[1]^0;
  for i in [Length(list), Length(list)-1 .. 1] do val := val * list[i]; od;
  return val;
end;;
BuildPn := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, q3, X, Y, Gfull;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  a1 := tr(r,1);; a2 := tr(r,2);; a3 := tr(r,3);;
  q1 := tr(s,2)*tr(s,3);; q2 := tr(s,1)*tr(s,3);; q3 := tr(s,1)*tr(s,2);;
  X := AbstractProd([a1,q1]);; Y := AbstractProd([a1,a2,a3,q2]);;
  Gfull := Group(a1,a2,a3,q1,q2);;
  return rec(n:=n,a1:=a1,a2:=a2,a3:=a3,q1:=q1,q2:=q2,q3:=q3,X:=X,Y:=Y,G:=Gfull);
end;;
AExp := function(v, P, n)
  local i,j,k;
  for i in [0..n-1] do for j in [0..n-1] do for k in [0..n-1] do
    if P.a1^i * P.a2^j * P.a3^k = v then return [i,j,k]; fi;
  od; od; od;
  return fail;
end;;

for n in [3,5,7,9] do
  P := BuildPn(n);;  u := 4*n-1;;
  Print("n = ", n, "\n");
  allok := true;;
  for k in [0..n-1] do
    # paper F = (2k, -2k, 0) in A  (Thm 4.3 with varkappa(2n-1) = 0 mod n)
    F := P.a1^(2*k) * P.a2^(-2*k);;              # A is abelian: raw = paper
    # Phi_{m,f}: X -> X^u ,  Y -> F^-1 Y^u F  (paper word => AbstractProd)
    PX := P.X^u;;
    PY := AbstractProd([F^-1, P.Y^u, F]);;
    # prediction: h = ((1-2k) e1) q3   in PAPER normal form a . q
    h := AbstractProd([P.a1^(1-2*k), P.q3]);;
    ok := (AbstractProd([h, P.X, h^-1]) = PX) and (AbstractProd([h, P.Y, h^-1]) = PY);;
    # what the fixture's raw decomposition (g * q3^-1 in A) would report for this h
    rawA := AExp(h * Inverse(P.q3), P, n);;
    papA := AExp(Inverse(P.q3) * h, P, n);;
    if not ok then allok := false; fi;
    Print("  k=", k, " : inn_paper(((1-2k)e1)q3)=Phi ? ", ok,
          "   paperNF=(", papA[1], ",", papA[2], ",", papA[3], ")",
          "   fixture-raw=(", rawA[1], ",", rawA[2], ",", rawA[3], ")",
          "   [(1-2k) mod n = ", (1-2*k) mod n, " , -(1-2k) mod n = ", (2*k-1) mod n, "]\n");
  od;
  Print("  ALL k PASS: ", allok, "\n");
od;
Print("\nSGNC-CHECK2 DONE\n");
QUIT;
