#############################################################################
## search/probe/wac_v1/ree_check.g -- corroboration for docs/notes/ree_capsule_v1.md
##  RC-1: mechanise proof B's bookkeeping (B-1..B-4) on real (2,3)-triples
##  RC-2: Ree bound c(a')+c(b')+c(u') <= n+2 on sampled (2,3)-generating pairs
##  RC-3: Lemma 3.1 (n=7,8) by exhaustive partition enumeration
## Single lane. NOT a ledger claim. No commit. No u (sealed symbol).
#############################################################################

NCyc := function(p, n) return Length(Orbits(Group(p), [1..n])); end;;

WacCyc := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;
WacBlock := function(blocks, len)
  local p, i, base;
  p := (); base := 0;
  for i in [1..blocks] do
    p := p * WacCyc(List([1..len], j -> base + j)); base := base + len;
  od;
  return p;
end;;

## minimal transposition decomposition: length n - c(p), left-to-right product
MinTransp := function(p, n)
  local out, o, lst, i;
  out := [];
  for o in Orbits(Group(p), [1..n]) do
    if Length(o) > 1 then
      lst := [o[1]];
      while Length(lst) < Length(o) do Add(lst, lst[Length(lst)]^p); od;
      for i in [2..Length(lst)] do Add(out, (lst[1], lst[i])); od;
    fi;
  od;
  if Product(out, ()) <> p then Error("MinTransp: product mismatch"); fi;
  if Length(out) <> n - NCyc(p, n) then Error("MinTransp: length mismatch"); fi;
  return out;
end;;

## simulate proof B (B-1)..(B-4) on a transposition word whose product is 1
ProofB := function(word, n)
  local pi, comp, find, t, a, b, merges, splits, spanning, ok, ra, rb, sameCyc, o;
  pi := ();
  comp := List([1..n], i -> i);
  find := function(x) while comp[x] <> x do x := comp[x]; od; return x; end;
  merges := 0; splits := 0; spanning := 0; ok := true;
  for t in word do
    a := SmallestMovedPoint(t); b := LargestMovedPoint(t);
    o := First(Orbits(Group(pi), [1..n]), z -> a in z);
    sameCyc := b in o;
    if sameCyc then splits := splits + 1; else merges := merges + 1; fi;
    ra := find(a); rb := find(b);
    if ra <> rb then
      spanning := spanning + 1;
      comp[ra] := rb;
      if sameCyc then ok := false; fi;       # would violate (B-3)
    fi;
    pi := pi * t;
  od;
  if pi <> () then Error("ProofB: word does not multiply to identity"); fi;
  return rec(L := Length(word), merges := merges, splits := splits,
             spanning := spanning, spanning_all_merge := ok);
end;;

Print("===== RC-1 / RC-2 : proof B bookkeeping + Ree bound on (2,3)-triples =====\n");
Print("  (a' b' u' = 1 with a'^2 = b'^3 = 1, <a',b'> transitive)\n\n");
for n in [7..16] do
  Sn := SymmetricGroup(n);; An := AlternatingGroup(n);;
  cnt := 0;; worst := 0;; okL := true;; okM := true;; okS := true;; okRee := true;;
  for trial in [1..3000] do
    a1 := WacBlock(Random([1..QuoInt(n,2)]), 2) ^ Random(Sn);
    b1 := WacBlock(Random([1..QuoInt(n,3)]), 3) ^ Random(Sn);
    G := Group(a1, b1);
    if IsTransitive(G, [1..n]) then
      cnt := cnt + 1;
      uu := b1^-1 * a1;
      s := NCyc(a1,n) + NCyc(b1,n) + NCyc(uu,n);
      if s > worst then worst := s; fi;
      if s > n + 2 then okRee := false; fi;
      if cnt <= 40 then                       # proof-B simulation on a subsample
        w := Concatenation(MinTransp(a1,n), MinTransp(b1,n), MinTransp(uu,n));
        r := ProofB(w, n);
        if r.L <> 2*r.merges then okL := false; fi;
        if r.merges < n-1 then okM := false; fi;
        if not r.spanning_all_merge then okS := false; fi;
        if r.spanning <> n-1 then okS := false; fi;
      fi;
    fi;
  od;
  Print("n=", n, " transitive samples=", cnt,
        "  max sum c = ", worst, " (bound ", n+2, ")  Ree_ok=", okRee,
        "  L=2*merge:", okL, "  merge>=n-1:", okM,
        "  spanning(=n-1) all merge:", okS, "\n");
od;

Print("\n===== RC-3 : Lemma 3.1, exhaustive over cycle types of A_n, n=7,8 =====\n");
for n in [7,8] do
  kmax := QuoInt(n,2);; jmax := QuoInt(n,3);;
  ree := kmax + 2*jmax + 2 - n;;
  Print("n=", n, "  Ree upper bound on c(u') = ", ree, "\n");
  cand := [];;
  for lam in Partitions(n) do
    if (n - Length(lam)) mod 2 <> 0 then continue; fi;    # xbar in A_n
    mult := Maximum(List(Set(lam), v -> Number(lam, w -> w = v)));
    if mult >= 5 and Lcm(lam) >= 3 then Add(cand, SortedList(lam)); fi;
  od;
  Print("  xbar types with (>=5 equal cycles) and ord>=3 : ", cand, "\n");
  for lam in cand do
    # all u' in S_n with u'^2 of type lam : enumerate by cycle type of u'
    mn := infinity;
    for mu in Partitions(n) do
      sq := [];
      for p in mu do
        if p mod 2 = 0 then Add(sq, p/2); Add(sq, p/2); else Add(sq, p); fi;
      od;
      if SortedList(sq) = lam then
        if Length(mu) < mn then mn := Length(mu); fi;
      fi;
    od;
    Print("    lam=", lam, " : min c(u') over all u' with u'^2 of this type = ",
          mn, "   > Ree bound ", ree, " ? ", mn > ree, "\n");
  od;
od;

Print("\nREE_CHECK_DONE\n");
QUIT;
