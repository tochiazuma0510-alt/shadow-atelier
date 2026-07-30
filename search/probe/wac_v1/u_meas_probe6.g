# u_meas_probe6.g -- Nielsen count for the WINDOW A quotient passport
# C = W/phi -> P^1_t : degree 10, passport (3^3 1, 3^3 1, (9,1)), monodromy A10.
# Raw measurements only.

Print("=== u_meas_probe6 : window A quotient passport Nielsen count ===\n");
MakeCycles := function(cyclist, n)
  local img, cyc, i, m;
  img := [1..n];
  for cyc in cyclist do
    m := Length(cyc);
    for i in [1..m] do img[cyc[i]] := cyc[(i mod m)+1]; od;
  od;
  return PermList(img);
end;

a1 := (1,2)(3,5)(4,10)(6,9);; b1 := (2,9,5)(3,4,10)(6,8,7);;
XA := (b1^-1*a1)^2;; YA := (a1*b1^-1)^2;;
piA := b1^-1;;
TA := piA^-1;; TB := XA^-1*piA;; cq := TA*TB;;
Print("c_q = Theta(A)Theta(B) = Y^-1 ? ", cq = YA^-1, "  ord=", Order(cq), "\n");

# enumerate all elements of S10 of cycle type (3,3,3,1)
S10 := SymmetricGroup(10);;
cands := Filtered(Elements(S10), g -> Order(g)=3 and NrMovedPoints(g)=9);;
Print("#elements of type (3,3,3,1) in S10 = ", Length(cands), "\n");

sols := [];;
for g in cands do
  h := g^-1*cq;
  if Order(h)=3 and NrMovedPoints(h)=9 then Add(sols,[g,h]); fi;
od;
Print("#solutions (A,B) with AB=c_q, both type (3,3,3,1) = ", Length(sols), "\n");
gs := List(sols, pr -> Size(Group(pr[1],pr[2])));;
Print("monodromy multiplicities = ", List(Set(gs), s -> [s, Number(gs,x->x=s)]), "\n");

A10 := AlternatingGroup(10);;
solA := Filtered(sols, pr -> Size(Group(pr[1],pr[2])) = Size(A10));;
Print("#with monodromy A10 = ", Length(solA), "\n");
CSq := Centralizer(S10, cq);;
Print("|C_S10(c_q)| = ", Size(CSq), "\n");
orb := [];; seen := [];;
for pr in solA do
  if not pr in seen then
    o := Set(List(Elements(CSq), g -> [pr[1]^g, pr[2]^g]));
    Append(seen,o); Add(orb,o);
  fi;
od;
Print("#S10-classes of quotient dessins with monodromy A10 = ", Length(orb),
      "  sizes = ", List(orb,Length), "\n");
Print("ours is class ", First([1..Length(orb)], i -> [TA,TB] in orb[i]), "\n");
Print("=== done ===\n");
QUIT;
