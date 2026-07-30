#############################################################################
## search/probe/wac_v1/r4_existence_search.g
## PRUNE-law r=4 window existence search: xbar type (5,5,5,5), n=20, ell=5,
## r=4, t=0.  Classify w0 candidate types with w0^2 of type (5,5,5,5),
## report parity accounting, then search for realization pairs (a,b):
##   a = involution (product of k disjoint transpositions, "appropriate"
##       parity forced by b needing to be even -- see parity accounting),
##   b := a * w0^-1,  require ord(b) = 3 (b <> identity),
##   classify <a,b> as A20 / S20 / other.
## Structured (small k, exhaustive) + randomized (large k, sampled) scan.
## Single lane (GAP 4.16.0).  NOT a ledger claim.  No commit.  No sealed
## symbol.  Existence search only -- no judgement, no interpretation.
#############################################################################

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
    p := p * WacCyc(List([1..len], j -> base+j)); base := base + len;
  od;
  return p;
end;;
WacCT := function(p, n) return SortedList(List(Orbits(Group(p),[1..n]), Length)); end;;

n := 20;;
Sn := SymmetricGroup(n);; An := AlternatingGroup(n);;

Print("#########################################################\n");
Print("## STEP 0  w0 candidate types with w0^2 type (5,5,5,5)\n");
Print("#########################################################\n");

## Reasoning (paper, restated for the machine check): squaring an m-cycle
## with m odd returns an m-cycle (x->x^2 is a bijection of the cyclic
## group of odd order m); squaring a 2k-cycle returns two k-cycles.
## So the only cycle lengths in w0 that can contribute 5-cycles to w0^2
## are 5 (odd, stays a 5-cycle) and 10 (even, splits into two 5-cycles).
## Partitions of n=20 into parts from {5,10}: 4x5, 2x5+1x10, 2x10.

w0_A := WacBlock(4,5);;                                    ## type (5,5,5,5)
w0_B := WacCyc([1..10]) * WacCyc([11..15]) * WacCyc([16..20]);; ## type (10,5,5)
w0_C := WacCyc([1..10]) * WacCyc([11..20]);;                ## type (10,10)

W0List := [ rec(w0:=w0_A, label:="type-A_(5,5,5,5)"),
            rec(w0:=w0_B, label:="type-B_(10,5,5)"),
            rec(w0:=w0_C, label:="type-C_(10,10)") ];;

for r in W0List do
  Print("-- ", r.label, "\n");
  Print("   w0 type          = ", WacCT(r.w0, n), "\n");
  Print("   sign(w0)         = ", SignPerm(r.w0), "\n");
  Print("   ord(w0)          = ", Order(r.w0), "\n");
  Print("   w0^2 type        = ", WacCT(r.w0^2, n), "\n");
  Print("   ord(w0^2)        = ", Order(r.w0^2), "\n");
  Print("   w0^2 type = (5,5,5,5) ? ", WacCT(r.w0^2,n) = [5,5,5,5], "\n");
od;

Print("\n#########################################################\n");
Print("## STEP 1  parity accounting\n");
Print("#########################################################\n");
## b := a*w0^-1 with a an involution (product of k transpositions,
## sign(a) = (-1)^k).  ord(b)=3 forces b even (sign(b)=+1).
## sign(b) = sign(a)*sign(w0), so sign(a) = sign(w0) is forced.
## => required parity of k: k even if sign(w0)=+1, k odd if sign(w0)=-1.
for r in W0List do
  if SignPerm(r.w0) = 1 then
    r.kparity := 0; r.kparity_label := "even k (a in A20)";
  else
    r.kparity := 1; r.kparity_label := "odd k (a odd perm)";
  fi;
  Print("-- ", r.label, "  sign(w0)=", SignPerm(r.w0),
        "  => required a-type: ", r.kparity_label, "\n");
od;

Print("\n#########################################################\n");
Print("## STEP 2  realization search per w0 type\n");
Print("#########################################################\n");

EXHAUST_THRESH := 1000000;;
SAMPLE_SIZE := 200000;;

Scan := function(rw0)
  local w0, label, kparity, k, cls, clsSize, exhaustive, hits, tries,
        a, b, G, cat, kstats, examples, i, t0, elapsed, totalTries, totalHits,
        firstAn, firstSn, modeLabel, ex;
  w0 := rw0.w0; label := rw0.label; kparity := rw0.kparity;
  Print("\n=== SCAN ", label, "  (w0 = ", w0, ") ===\n");
  kstats := [];
  examples := [];
  totalTries := 0; totalHits := 0;
  firstAn := fail; firstSn := fail;
  for k in [1..QuoInt(n,2)] do
    if (k mod 2) <> kparity then
      continue;
    fi;
    t0 := Runtime();
    cls := WacBlock(k,2);
    clsSize := Size(ConjugacyClass(Sn, cls));
    hits := 0; tries := 0;
    if clsSize <= EXHAUST_THRESH then
      exhaustive := true;
      for a in AsList(ConjugacyClass(Sn, cls)) do
        tries := tries + 1;
        b := a * w0^-1;
        if b <> () and b^3 = () and Order(b) = 3 then
          hits := hits + 1;
          G := Group(a,b);
          if G = An then
            cat := "A20";
            if firstAn = fail then firstAn := rec(a:=a, b:=b, k:=k); fi;
          elif G = Sn then
            cat := "S20";
            if firstSn = fail then firstSn := rec(a:=a, b:=b, k:=k); fi;
          else
            cat := "other";
          fi;
          if Length(examples) < 20 then
            Add(examples, rec(k:=k, a:=a, b:=b, gen:=cat, sizeG:=Size(G)));
          fi;
        fi;
      od;
    else
      exhaustive := false;
      for i in [1..SAMPLE_SIZE] do
        tries := tries + 1;
        a := cls ^ Random(Sn);
        b := a * w0^-1;
        if b <> () and b^3 = () and Order(b) = 3 then
          hits := hits + 1;
          G := Group(a,b);
          if G = An then
            cat := "A20";
            if firstAn = fail then firstAn := rec(a:=a, b:=b, k:=k); fi;
          elif G = Sn then
            cat := "S20";
            if firstSn = fail then firstSn := rec(a:=a, b:=b, k:=k); fi;
          else
            cat := "other";
          fi;
          if Length(examples) < 20 then
            Add(examples, rec(k:=k, a:=a, b:=b, gen:=cat, sizeG:=Size(G)));
          fi;
        fi;
      od;
    fi;
    elapsed := (Runtime() - t0) / 1000.0;
    totalTries := totalTries + tries;
    totalHits := totalHits + hits;
    Add(kstats, rec(k:=k, classSize:=clsSize, exhaustive:=exhaustive,
                     tries:=tries, hits:=hits, elapsed_sec:=elapsed));
    if exhaustive then modeLabel := "EXHAUSTIVE"; else modeLabel := "RANDOM"; fi;
    Print("   k=", k, "  |class|=", clsSize,
          "  mode=", modeLabel,
          "  tries=", tries, "  hits(ord(b)=3)=", hits,
          "  elapsed=", elapsed, "s\n");
  od;
  Print("   -- totals: tries=", totalTries, "  hits=", totalHits, "\n");
  if firstAn <> fail then
    Print("   -- first <a,b>=A20 witness: FOUND at k=", firstAn.k, "\n");
    Print("      a := ", firstAn.a, ";;\n      b := ", firstAn.b, ";;\n");
  else
    Print("   -- first <a,b>=A20 witness: NONE\n");
  fi;
  if firstSn <> fail then
    Print("   -- first <a,b>=S20 witness: FOUND at k=", firstSn.k, "\n");
    Print("      a := ", firstSn.a, ";;\n      b := ", firstSn.b, ";;\n");
  else
    Print("   -- first <a,b>=S20 witness: NONE\n");
  fi;
  Print("   -- all recorded hit examples (up to 20) --\n");
  for ex in examples do
    Print("      [k=", ex.k, " gen=", ex.gen, " |<a,b>|=", ex.sizeG, "]\n");
    Print("        a := ", ex.a, ";;\n");
    Print("        b := ", ex.b, ";;\n");
  od;
  return rec(label:=label, kstats:=kstats, totalTries:=totalTries,
             totalHits:=totalHits, firstAn:=firstAn, firstSn:=firstSn,
             examples:=examples);
end;;

resA := Scan(W0List[1]);;
resB := Scan(W0List[2]);;
resC := Scan(W0List[3]);;

Print("\n#########################################################\n");
Print("## SUMMARY\n");
Print("#########################################################\n");
for res in [resA, resB, resC] do
  Print(res.label, "  totalTries=", res.totalTries,
        "  totalHits=", res.totalHits,
        "  existsA20=", res.firstAn <> fail,
        "  existsS20=", res.firstSn <> fail, "\n");
od;

Print("\nR4_EXISTENCE_SEARCH_DONE\n");
QUIT;
