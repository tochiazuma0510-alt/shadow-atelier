## scratchpad probe (throwaway): try to find explicit sigma1,sigma2 (full B3 generator images)
## for the K(9) dihedral window (MakeGn(9)), such that sigma1^2=x, sigma2^2=y, and the braid
## relation sigma1*sigma2*sigma1 = sigma2*sigma1*sigma2 holds. NOT for cert/production use.
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");

n := 9;;
rs := MakeDn(n);; r := rs[1];; s := rs[2];;
tr := function(p, i)
  local l, j;
  l := List([1..3*n], k -> k);
  for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
  return PermList(l);
end;;
x := tr(r,1) * tr(s,2) * tr(s,3);;
y := tr(s*r,1) * tr(r,2) * tr(s*r,3);;
G := Group(x,y);;
Print("|G|=", Size(G), " ord x,y = ", Order(x), ",", Order(y), " lcm=", Lcm(Order(x),Order(y)), "\n");

## block swap permutation (identity twist): swaps block i <-> block j pointwise
BlockSwap := function(i, j, nn)
  local l, k;
  l := List([1..3*nn], k -> k);
  for k in [1..nn] do
    l[k + (i-1)*nn] := k + (j-1)*nn;
    l[k + (j-1)*nn] := k + (i-1)*nn;
  od;
  return PermList(l);
end;;

tau12 := BlockSwap(1,2,n);;
tau23 := BlockSwap(2,3,n);;

## candidate A: sigma1 = tau12 * tr(s,3) (leaves block3 fixed except twisted by s... but tau12 already
## fixes block3 pointwise, so multiply order matters). Try several small variants and machine-check.
CandidatesS1 := [
  tau12 * tr(s,3),
  tr(s,3) * tau12,
  tau12 * tr(r,3),
  tr(r,3) * tau12,
  tau12,
];;
CandidatesS2 := [
  tau23 * tr(s,1),
  tr(s,1) * tau23,
  tau23 * tr(r,1),
  tr(r,1) * tau23,
  tau23,
];;

found := false;;
for i in [1..Length(CandidatesS1)] do
  for j in [1..Length(CandidatesS2)] do
    s1c := CandidatesS1[i];;  s2c := CandidatesS2[j];;
    sqOk := (s1c^2 = x) and (s2c^2 = y);;
    braidOk := (s1c*s2c*s1c = s2c*s1c*s2c);;
    if sqOk then
      Print("i=",i," j=",j," sqOk=",sqOk," braidOk=",braidOk, "\n");
    fi;
    if sqOk and braidOk then found := true; fi;
  od;
od;
Print("found_any = ", found, "\n");
QUIT;
