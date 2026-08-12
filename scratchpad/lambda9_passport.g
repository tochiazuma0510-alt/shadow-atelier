# extract the full passport of lambda_9 from the BuildPnFull(9)/H9fun construction
# (same construction as search/w9_k3_p1_0d_check.g -- read-only, no cert written)
SizeScreen([4096, 0]);;

BuildPnFull := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, X, Y, Gfull;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  a1 := tr(r,1);;  a2 := tr(r,2);;  a3 := tr(r,3);;
  q1 := tr(s,2)*tr(s,3);;  q2 := tr(s,1)*tr(s,3);;
  X := a1*q1;;
  Y := a1*a2*a3*q2;;
  Gfull := Group(a1,a2,a3,q1,q2);;
  return rec(n:=n, X:=X, Y:=Y, G:=Gfull);;
end;;

P9 := BuildPnFull(9);;
# H9fun as in the original script
r := PermList(Concatenation([2..9],[1]));;
s := PermList(List([1..9], j -> ((9 - (j-1)) mod 9) + 1));;
tr := function(p, i)
  local l, j;
  l := List([1..27], k -> k);
  for j in [1..9] do l[j + (i-1)*9] := (j^p) + (i-1)*9; od;
  return PermList(l);
end;;
a1 := tr(r,1);; a2 := tr(r,2);; a3 := tr(r,3);;
q1 := tr(s,2)*tr(s,3);; q2 := tr(s,1)*tr(s,3);;
G := Group(a1,a2,a3,q1,q2);;
H9fun := Group(a2, a1*a3, q2);;
D := Size(G)/Size(H9fun);;
Print("index D = ", D, "\n");
phi := FactorCosetAction(G, H9fun);;
Xi := Image(phi, a1*q1);;
Yi := Image(phi, a1*a2*a3*q2);;
Zi := (Xi*Yi)^-1;;
monG := Group(Xi, Yi);;
Print("|monG| = ", Size(monG), "\n");
Print("transitive on 18 points: ", IsTransitive(monG, [1..18]), "\n");
Print("cycle type X   : ", CycleStructurePerm(Xi), "  order ", Order(Xi), "\n");
Print("cycle type Y   : ", CycleStructurePerm(Yi), "  order ", Order(Yi), "\n");
Print("cycle type Z=(XY)^-1: ", CycleStructurePerm(Zi), "  order ", Order(Zi), "\n");
Print("X as cycles: ", Xi, "\n");
Print("Y as cycles: ", Yi, "\n");
Print("Z as cycles: ", Zi, "\n");

# block systems
bl := AllBlocks(monG);;
Print("all block representatives: ", bl, "\n");
Print("block sizes present: ", Set(List(bl, b -> Length(b))), "\n");
b3 := Filtered(bl, b -> Length(b) = 3);;
Print("number of size-3 block reps: ", Length(b3), "  -> ", b3, "\n");

# degree-6 quotient (E -> P1_t)
if Length(b3) > 0 then
  bs := Orbit(monG, b3[1], OnSets);;
  Print("size-3 block system: ", bs, "\n");
  IndP := function(p, bsy)
    local n2, bo, i, pt, im, idx;
    n2 := Length(bsy);; bo := [];;
    for idx in [1..n2] do for pt in bsy[idx] do bo[pt] := idx; od; od;
    im := [];;
    for i in [1..n2] do im[i] := bo[ bsy[i][1]^p ]; od;
    return PermList(im);
  end;;
  qX := IndP(Xi, bs);; qY := IndP(Yi, bs);; qZ := IndP(Zi, bs);;
  quot := Group(qX,qY);;
  Print("--- degree-6 quotient E -> P1_t ---\n");
  Print("|quotG| = ", Size(quot), "\n");
  Print("qX = ", qX, "  type ", CycleStructurePerm(qX), "\n");
  Print("qY = ", qY, "  type ", CycleStructurePerm(qY), "\n");
  Print("qZ = ", qZ, "  type ", CycleStructurePerm(qZ), "\n");
  Print("deck (centralizer in S6) order = ", Size(Centralizer(SymmetricGroup(6), quot)), "\n");
  # genus of the degree-6 cover
  Print("quot blocks: ", AllBlocks(quot), "\n");
fi;

# genus of the degree-18 cover by Riemann-Hurwitz
rh := (18 - Length(Cycles(Xi,[1..18]))) + (18 - Length(Cycles(Yi,[1..18]))) + (18 - Length(Cycles(Zi,[1..18])));;
Print("sum (e-1) = ", rh, "  => 2g-2 = ", -2*18 + rh, " => g = ", (-2*18+rh+2)/2, "\n");
QUIT;
