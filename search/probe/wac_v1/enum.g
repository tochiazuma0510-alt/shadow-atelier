#############################################################################
## search/probe/wac_v1/enum.g -- WA-c: minimal alternating target search
## Combinatorial gate (Ree + parity + hyperbolicity + Hol-sieve) then exact
## class structure constants in S_n. Single lane. NOT a ledger claim. No commit.
#############################################################################

SqType := function(lam)   # cycle type of u^2 from cycle type of u
  local out, p;
  out := [];
  for p in lam do
    if p mod 2 = 0 then Add(out, p/2); Add(out, p/2);
    else Add(out, p); fi;
  od;
  return SortedList(out);
end;;

MaxMult := function(l)
  return Maximum(List(Set(l), v -> Number(l, w -> w = v)));
end;;

Print("===== E-1: combinatorial survivors, n = 9..24 =====\n");
Print("(t=c(u); need t <= k+2j+2-n for SOME even k<=floor(n/2), j<=floor(n/3))\n\n");
surv := [];;
for n in [9..24] do
  kmax := QuoInt(n,2); if kmax mod 2 = 1 then kmax := kmax - 1; fi;
  jmax := QuoInt(n,3);
  B := kmax + 2*jmax + 2 - n;
  for lam in Partitions(n) do
    t := Length(lam);
    if t <= B and (n - t) mod 2 = 0 and Lcm(lam) >= 7 then
      s := SqType(lam);
      if MaxMult(s) >= 5 and Lcm(s) >= 3 then
        Add(surv, rec(n:=n, lam:=SortedList(lam), t:=t, sq:=s,
                      ordu:=Lcm(lam), ordx:=Lcm(s), B:=B));
        Print("n=", n, "  lam(u)=", SortedList(lam), " t=", t, " (B=", B, ")",
              "  ord(u)=", Lcm(lam),
              "  type(xbar)=", s, " ord=", Lcm(s), "\n");
      fi;
    fi;
  od;
od;
Print("\ntotal combinatorial survivors: ", Length(surv), "\n");

Print("\n===== E-2: exact structure constants in S_n =====\n");
Print("count of pairs (a1,b1), a1 in 2^k 1^*, b1 in 3^j 1^*, with a1*b1 = u^-1 fixed\n\n");

for r in surv do
  n := r.n;
  tbl := CharacterTable("Symmetric", n);;
  parts := ClassParameters(tbl);;   # each entry [1, partition]
  pidx := function(p)
    return First([1..Length(parts)], i -> SortedList(parts[i][2]) = SortedList(p));
  end;
  ok := false;
  for j in [1..QuoInt(n,3)] do
    for k in [1..QuoInt(n,2)] do
      if k mod 2 = 0 and k + 2*j + 2 - n >= r.t then
        la := Concatenation(List([1..k], z->2), List([1..n-2*k], z->1));
        lb := Concatenation(List([1..j], z->3), List([1..n-3*j], z->1));
        ia := pidx(la); ib := pidx(lb); ic := pidx(r.lam);
        cc := ClassMultiplicationCoefficient(tbl, ia, ib, ic);
        if cc > 0 then ok := true; fi;
        Print("  n=", n, " lam=", r.lam, "  a1=2^", k, " b1=3^", j,
              "  structconst = ", cc, "\n");
      fi;
    od;
  od;
  Print("  --> n=", n, " lam=", r.lam, " REALIZABLE(class level)? ", ok, "\n\n");
od;

Print("ENUM_DONE\n");
QUIT;
