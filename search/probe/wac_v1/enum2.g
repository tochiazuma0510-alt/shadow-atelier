#############################################################################
## search/probe/wac_v1/enum2.g -- WA-c minimality, BOTH parities of a'
## (the image of E-bar in Aut(A_n)=S_n may be A_n (k even) or S_n (k odd)).
## Single lane. NOT a ledger claim. No commit.
#############################################################################

SqType := function(lam)
  local out, p;
  out := [];
  for p in lam do
    if p mod 2 = 0 then Add(out, p/2); Add(out, p/2); else Add(out, p); fi;
  od;
  return SortedList(out);
end;;
MaxMult := function(l)
  return Maximum(List(Set(l), v -> Number(l, w -> w = v)));
end;;

Print("===== E2-1: survivors n=9..16, k even AND k odd =====\n");
surv := [];;
for n in [9..16] do
  for lam in Partitions(n) do
    t := Length(lam);
    if Lcm(lam) < 7 then continue; fi;
    s := SqType(lam);
    if MaxMult(s) < 5 or Lcm(s) < 3 then continue; fi;
    # sign(u) = (-1)^(n-t) must equal (-1)^k
    kpar := (n - t) mod 2;      # required parity of k
    for k in [1..QuoInt(n,2)] do
      for j in [1..QuoInt(n,3)] do
        if k mod 2 = kpar and k + 2*j + 2 - n >= t then
          Add(surv, rec(n:=n, lam:=SortedList(lam), t:=t, k:=k, j:=j, sq:=s));
          Print("n=", n, " lam(u)=", SortedList(lam), " t=", t,
                "  k=", k, " j=", j, "  ord(u)=", Lcm(lam),
                "  xbar=", s, " ord=", Lcm(s),
                "  image=", ["A","S"][k mod 2 + 1], n, "\n");
        fi;
      od;
    od;
  od;
od;
Print("\ntotal (n,lam,k,j) survivors: ", Length(surv), "\n\n");

Print("===== E2-2: exact structure constants in S_n =====\n");
for r in surv do
  n := r.n;
  tbl := CharacterTable("Symmetric", n);;
  parts := ClassParameters(tbl);;
  pidx := function(p)
    return First([1..Length(parts)], i -> SortedList(parts[i][2]) = SortedList(p));
  end;
  la := Concatenation(List([1..r.k], z->2), List([1..n-2*r.k], z->1));
  lb := Concatenation(List([1..r.j], z->3), List([1..n-3*r.j], z->1));
  cc := ClassMultiplicationCoefficient(tbl, pidx(la), pidx(lb), pidx(r.lam));
  Print("n=", n, " lam=", r.lam, " a'=2^", r.k, "1^", n-2*r.k,
        " b'=3^", r.j, "1^", n-3*r.j, "  structconst = ", cc, "\n");
od;
Print("\nENUM2_DONE\n");
QUIT;
