# search/a5-dessin-crosscheck.g -- GAP independent re-derivation of the (5,5,5) A5 dessin
# enumeration (task a) and the t=1 Dedekind specialization check (task c-prime), per the
# commander's order (P2 two-system-ization, A5 dessin GAP crosscheck).
#
# Independence note: this script does NOT read search/week4-a5-dessin-unique.mjs (the node
# implementation) -- it is written fresh from the mathematical definitions in the order text
# and re-derives everything (192/120/72 counts, orbits, centralizer, genus, D(v), the
# (g0,g1)->Fix(g1) map, and the t=1/mod-3/F20 Dedekind chain) from GAP primitives only.
#
# Usage: .\gap.ps1 search\a5-dessin-crosscheck.g

SizeScreen([4096, 0]);;
startTime := Runtime();;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;
JB := function(b) if b then return "true"; else return "false"; fi; end;;
JoinC := function(strs, sep)
  local parts, i;
  parts := [];
  for i in [1..Length(strs)] do
    Add(parts, strs[i]);
    if i < Length(strs) then Add(parts, sep); fi;
  od;
  return Concatenation(parts);
end;;
WriteFileRaw := function(path, content)
  local f;
  f := OutputTextFile(path, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, content);
  CloseStream(f);
end;;

Print("GAP version: ", GAPInfo.Version, "\n\n");

# ================================================================================
# task (a): (5,5,5) A5 dessin enumeration in S5. Convention: g0,g1 range over all of S5
# (120x120 = 14400 total pairs checked, "???? per the order); ginf := (g0*g1)^-1; a triple
# (g0,g1,ginf) counts iff ord(g0)=ord(g1)=ord(ginf)=5, i.e. iff ord(g0)=5, ord(g1)=5,
# ord(g0*g1)=5 (ord(ginf)=ord(g0*g1) since inverse has the same order).
# ================================================================================
Print("=== task (a): (5,5,5) A5 dessin enumeration in S5 ===\n");

G := SymmetricGroup(5);;
A5 := AlternatingGroup(5);;
elts := AsList(G);;
Print("|S5| = ", Length(elts), "\n");

allPairs := [];;   # all valid (g0,g1) triples (any generated subgroup)
a5Pairs := [];;    # subset with <g0,g1> of order 60 (= A5, the only such subgroup)
c5Pairs := [];;    # subset with <g0,g1> of order 5 (cyclic)
anomalyCount := 0;;

for g0 in elts do
  if Order(g0) = 5 then
    for g1 in elts do
      if Order(g1) = 5 then
        if Order(g0*g1) = 5 then
          Add(allPairs, [g0,g1]);
          H := Subgroup(G, [g0,g1]);;
          sz := Size(H);;
          if sz = 60 then
            Add(a5Pairs, [g0,g1]);
          elif sz = 5 then
            Add(c5Pairs, [g0,g1]);
          else
            Print("[ANOMALY] pair with |<g0,g1>| = ", sz, " (neither 60 nor 5): g0=", g0, " g1=", g1, "\n");
            anomalyCount := anomalyCount + 1;
          fi;
        fi;
      fi;
    od;
  fi;
od;

totalAll := Length(allPairs);;
totalA5 := Length(a5Pairs);;
totalC5 := Length(c5Pairs);;
Print("total valid (g0,g1,ginf) triples, all order 5 = ", totalAll, "\n");
Print("A5-type (<g0,g1>=A5, order 60) = ", totalA5, "\n");
Print("C5-type (<g0,g1> order 5)      = ", totalC5, "\n");
Print("anomalies (other subgroup order) = ", anomalyCount, "\n");
Print("A5-type + C5-type + anomalies = total: ", PF(totalA5+totalC5+anomalyCount = totalAll), "\n\n");

# --- item 2: orbits of A5-type pairs under diagonal A5-conjugation and S5-conjugation ---
ConjPair := function(pair, a) return [pair[1]^a, pair[2]^a]; end;;

OrbitsUnderGrp := function(pairsList, grpList)
  local seen, orbits, p, orb, a, np;
  seen := [];;
  orbits := [];;
  for p in pairsList do
    if not (p in seen) then
      orb := [];;
      for a in grpList do
        np := ConjPair(p, a);;
        if not (np in orb) then Add(orb, np); fi;
      od;
      Add(orbits, orb);
      Append(seen, orb);
    fi;
  od;
  return orbits;
end;;

A5list := AsList(A5);;
orbitsA5 := OrbitsUnderGrp(a5Pairs, A5list);;
orbitsS5 := OrbitsUnderGrp(a5Pairs, elts);;
orbitSizesA5 := List(orbitsA5, Length);;
orbitSizesS5 := List(orbitsS5, Length);;
Print("A5-conjugation orbits on A5-type pairs: count = ", Length(orbitsA5), ", sizes = ", orbitSizesA5, "\n");
Print("S5-conjugation orbits on A5-type pairs: count = ", Length(orbitsS5), ", sizes = ", orbitSizesS5, "\n\n");

# --- item 3: |C_S5(<g0,g1>)| for A5-type pairs ---
allEqualA5 := ForAll(a5Pairs, p -> Subgroup(G,p) = A5);;
Print("all A5-type <g0,g1> equal A5 exactly (unique order-60 subgroup of S5): ", PF(allEqualA5), "\n");
centA5 := Centralizer(G, A5);;
centSizeA5 := Size(centA5);;
Print("|C_S5(A5)| = ", centSizeA5, "\n\n");

# --- item 4: genus from a representative A5-type triple ---
repPair := a5Pairs[1];;
g0r := repPair[1];; g1r := repPair[2];; ginfr := (g0r*g1r)^(-1);;
NrCyc := function(g) return Length(Orbits(Group(g), [1..5])); end;;
c0 := NrCyc(g0r);; c1 := NrCyc(g1r);; cinf := NrCyc(ginfr);;
sumTerm := (5-c0) + (5-c1) + (5-cinf);;
twoMinus2g := 2*5 - sumTerm;;
genusVal := (2 - twoMinus2g)/2;;
Print("representative A5-type triple: g0=", g0r, " g1=", g1r, " ginf=", ginfr, "\n");
Print("cycle counts (incl. fixed pts): c0=", c0, " c1=", c1, " cinf=", cinf, "\n");
Print("2-2g = 2*5 - sum(5-cycles) = ", twoMinus2g, "  =>  g = ", genusVal, "\n\n");

# check genus is the same for ALL A5-type pairs (not just the representative)
allGenus := List(a5Pairs, function(p)
  local a,b,cc,ca,cb,ccc,st,t22g;
  a := p[1];; b := p[2];; cc := (a*b)^(-1);;
  ca := NrCyc(a);; cb := NrCyc(b);; ccc := NrCyc(cc);;
  st := (5-ca)+(5-cb)+(5-ccc);;
  t22g := 10 - st;;
  return (2-t22g)/2;
end);;
genusConstant := (DuplicateFreeList(allGenus) = [genusVal]);;
Print("genus constant across all ", totalA5, " A5-type triples: ", PF(genusConstant), " (distinct values: ", DuplicateFreeList(allGenus), ")\n\n");

# ================================================================================
# item 5: v = (1,2,3,4,5) (cycle notation: 1->2->3->4->5->1), D(v), and the map
# (g0,g1) |-> Fix(g1) onto {1,...,5}.
# ================================================================================
v := PermList([2,3,4,5,1]);;
Print("v = (1,2,3,4,5) as GAP permutation = ", v, ", order = ", Order(v), "\n");

Dv := Filtered(a5Pairs, p -> p[1] = v);;
Print("|D(v)| (A5-type pairs with g0 = v) = ", Length(Dv), "\n");

FixSet := function(g) return Filtered([1..5], i -> i^g = i); end;;
fixImages := List(Dv, p -> FixSet(p[2]));;
Print("Fix(g1) for each g1 in D(v): ", fixImages, "\n");

allFixEmpty := ForAll(fixImages, s -> Length(s) = 0);;
Print("all Fix(g1) empty (g1 has order 5, fixed-point-free on {1..5}): ", PF(allFixEmpty), "\n");

# well-definedness as a map D(v) -> {1,...,5}: fails iff any Fix(g1) is not a singleton
wellDefinedAsMapTo5 := ForAll(fixImages, s -> Length(s) = 1);;
Print("map (g0,g1)->Fix(g1) well-defined as a map into {1,...,5} (each Fix(g1) a singleton): ", PF(wellDefinedAsMapTo5), "\n");

# if well-defined, test bijectivity onto {1..5}; here (all empty) report FAIL honestly since
# the target instructions ask for this exact check -- do not silently reinterpret.
bijectiveOntoFive := false;;
if wellDefinedAsMapTo5 then
  singletons := List(fixImages, s -> s[1]);;
  bijectiveOntoFive := (Set(singletons) = [1,2,3,4,5]) and (Length(singletons) = Length(Set(singletons)));;
fi;
Print("map is a bijection D(v) -> {1,...,5}: ", PF(bijectiveOntoFive), " (undefined/FAIL if map is not well-defined above)\n");

# <v>-equivariance check: Fix(g1)^v should equal Fix' for the conjugated pair v*(g0,g1)*v^-1
# = (v g0 v^-1, v g1 v^-1) = (v v v^-1, v g1 v^-1) = (v, v g1 v^-1) which remains in D(v) since
# g0-component is unchanged (v is central to itself); check Fix(v g1 v^-1) = FixSet(g1)^v pointwise.
equivOk := true;;
for p in Dv do
  g1 := p[2];;
  conjG1 := g1^(v^(-1));;  # v * g1 * v^-1  (GAP: x^a = a^-1*x*a, so v g1 v^-1 = g1^(v^-1))
  lhsSet := FixSet(conjG1);;
  rhsSet := Set(List(FixSet(g1), i -> i^v));;
  if lhsSet <> rhsSet then equivOk := false; fi;
od;
Print("<v>-equivariance of Fix(.) under conjugation (Fix(v g1 v^-1) = v.Fix(g1)) holds pointwise: ", PF(equivOk), " (both sides are the empty set for every element -- vacuous, not evidence of a working bijection)\n\n");

# ================================================================================
# item 5 CORRECTION (commander, 2026-07-26): the original (a).5 spec above was a
# transcription error on the commander's part -- v2 doc sec.3.6's lemma FC-6 is about
# (2,3,5) pairs (q order 2 "2A", r order 3 "3A"), NOT the (5,5,5) triple's own (g0,g1).
# The block above (old item 5) is left byte-for-byte unmodified as the audit trail of
# the erroneous spec and the honest FAIL finding it produced.
#
# Corrected spec: D(v) := {(q,r) : q in 2A (double transposition, exactly one fixed
# point), r in 3A (3-cycle), qrv=1}. The word "qrv=1" is ambiguous between the paper's
# left-to-right reading and GAP's function-composition convention for permutation
# products, so per the commander's instruction (definition-note sec.1.5 A5-CONV) BOTH
# readings are computed and reported side by side:
#   - MAIN (primary):  v*r*q = One(G)   ("full reverse" of the written word "qrv")
#   - NAIVE (control): q*r*v = One(G)   (literal left-to-right reading)
# ================================================================================
Print("=== task (a) item 5 CORRECTED (commander transcription-error fix, v2 sec.3.6 FC-6 spec) ===\n");

q2Alist := Filtered(elts, x -> Order(x) = 2 and Length(FixSet(x)) = 1);;
r3Alist := Filtered(elts, x -> Order(x) = 3);;
Print("|2A candidates| (order 2, exactly 1 fixed point) = ", Length(q2Alist), "\n");
Print("|3A candidates| (order 3, i.e. 3-cycles in S5)   = ", Length(r3Alist), "\n\n");

ComputeDvFC6 := function(conventionName, eqTest)
  local Dloc, q, r, images, allSingleton, bij, singles, equivOkLoc, p2, qc, rc, lhsS, rhsS, inDvAfter;
  Dloc := [];;
  for q in q2Alist do
    for r in r3Alist do
      if eqTest(q,r) then Add(Dloc, [q,r]); fi;
    od;
  od;
  images := List(Dloc, p2 -> FixSet(p2[1]));;
  allSingleton := ForAll(images, s -> Length(s) = 1);;
  bij := false;;
  if allSingleton then
    singles := List(images, s -> s[1]);;
    bij := (Set(singles) = [1,2,3,4,5]) and (Length(singles) = Length(Set(singles)));;
  fi;
  # Convention note (verified empirically with search/debug-equiv-test.g before wiring this
  # in -- do not trust the naive symbol-for-symbol transcription): GAP's "^" satisfies
  # i^(g*h) = (i^g)^h (right action), which is the REVERSED composition order relative to
  # standard function notation (this project already hit the same "paper AB <-> GAP B*A"
  # reversal in the 2026-07-26 WO2 A2 entry, provenance/LEDGER.md). Consequently the GAP
  # expression q^(v^-1) does NOT compute the permutation whose fixed-point set is the
  # standard-math image v(Fix(q)); q^v does. Concretely (checked on q=(1,2)(3,4), v=(1,2,3,4,5)):
  # Fix(q)={5}; q^v=(2,3)(4,5) has Fix={1}=v(5) (matches); q^(v^-1)=(1,5)(2,3) has Fix={4}
  # (does not match). So "the pair conjugated by v" here means (q^v, r^v), NOT (q^(v^-1), r^(v^-1)).
  equivOkLoc := true;;
  inDvAfter := true;;
  for p2 in Dloc do
    qc := p2[1]^v;;   # matches standard "v q v^-1" under the i^v = v(i) reading (see note above)
    rc := p2[2]^v;;
    if not eqTest(qc,rc) then inDvAfter := false; fi;
    lhsS := FixSet(qc);;
    rhsS := Set(List(FixSet(p2[1]), i -> i^v));;
    if lhsS <> rhsS then equivOkLoc := false; fi;
  od;
  Print("[", conventionName, "] |D(v)| = ", Length(Dloc), "\n");
  Print("[", conventionName, "] Fix(q) images = ", images, "\n");
  Print("[", conventionName, "] each Fix(q) a singleton (well-defined map): ", PF(allSingleton), "\n");
  Print("[", conventionName, "] (q,r)->Fix(q) bijection D(v)->{1..5}: ", PF(bij), "\n");
  Print("[", conventionName, "] conjugated pairs remain in D(v) (closure under <v>): ", PF(inDvAfter), "\n");
  Print("[", conventionName, "] <v>-equivariance Fix(v q v^-1) = v.Fix(q): ", PF(equivOkLoc), "\n\n");
  return rec(count:=Length(Dloc), images:=images, wellDefined:=allSingleton, bijective:=bij,
             stableUnderV:=inDvAfter, equivariant:=equivOkLoc);
end;;

eqMain := function(q,r) return v*r*q = One(G); end;;
eqNaive := function(q,r) return q*r*v = One(G); end;;

resMain := ComputeDvFC6("MAIN v*r*q=1", eqMain);;
resNaive := ComputeDvFC6("NAIVE q*r*v=1", eqNaive);;

Print("elapsed so far (ms): ", Runtime()-startTime, "\n\n");

# ================================================================================
# task (c-prime): t=1 specialization Dedekind check chain
# ================================================================================
Print("=== task (c-prime): t=1 Dedekind specialization check ===\n");

Rx := PolynomialRing(Rationals, ["x"]);;
xx := IndeterminatesOfPolynomialRing(Rx)[1];;

# item 1: plane model x^5 t^3 + (-5x+2) t^2 + (-5x+6) t + 4 at t=1, expanded
coeff_t3 := xx^5;;
coeff_t2 := -5*xx+2;;
coeff_t1 := -5*xx+6;;
coeff_t0 := 4*xx^0;;
Fat1 := coeff_t3 + coeff_t2 + coeff_t1 + coeff_t0;;
target := xx^5 - 10*xx + 12;;
Print("F(x,1) [from plane model, expanded] = ", Fat1, "\n");
Print("target x^5 - 10x + 12               = ", target, "\n");
item1ok := (Fat1 = target);;
Print("item 1 (t=1 specialization matches x^5-10x+12): ", PF(item1ok), "\n\n");

# item 2: factorization x^5-10x+12 = (x+2)(x^4-2x^3+4x^2-8x+6), separable (gcd(f,f')=1 up to units)
f := target;;
fac1 := xx+2;;
fac2 := xx^4 - 2*xx^3 + 4*xx^2 - 8*xx + 6;;
item2a_ok := (fac1*fac2 = f);;
Print("(x+2)(x^4-2x^3+4x^2-8x+6) = x^5-10x+12: ", PF(item2a_ok), "\n");

fprime := Derivative(f);;
gcdff := Gcd(f, fprime);;
gcdDeg := DegreeOfLaurentPolynomial(gcdff);;
Print("f' = ", fprime, "\n");
Print("gcd(f,f') = ", gcdff, " (degree ", gcdDeg, ")\n");
item2b_ok := (gcdDeg = 0);;
Print("item 2 (separable, gcd(f,f') is a nonzero constant): ", PF(item2a_ok and item2b_ok), "\n\n");

factorsOverQ := Factors(Rx, f);;
Print("Factors(f) over Q = ", factorsOverQ, "\n\n");

# item 3: mod 3 factorization degree type
Rx3 := PolynomialRing(GF(3), ["x"]);;
xx3 := IndeterminatesOfPolynomialRing(Rx3)[1];;
one3 := One(GF(3));;
f3 := xx3^5 - (10*one3)*xx3 + (12*one3);;
Print("f mod 3 = ", f3, "\n");
facs3 := Factors(Rx3, f3);;
degs3 := List(facs3, DegreeOfLaurentPolynomial);;
Sort(degs3);;
Print("mod-3 factor degrees (sorted ascending) = ", degs3, "\n");
item3ok := (degs3 = [1,1,1,2]);;
Print("item 3 (mod-3 degree type is the multiset {2,1,1,1}): ", PF(item3ok), "\n\n");

# item 4: cycle types of F20 = N_S5(<(1,2,3,4,5)>); check no transposition-type (2,1,1,1) element
c := PermList([2,3,4,5,1]);;
C5grp := Group(c);;
F20 := Normalizer(G, C5grp);;
F20size := Size(F20);;
Print("|F20| = |N_S5(<(1,2,3,4,5)>)| = ", F20size, "\n");
F20list := AsList(F20);;

CycleTypeOf := function(g)
  local pts, seen, orbs, p, orb, lengths;
  seen := [];;
  lengths := [];;
  for p in [1..5] do
    if not (p in seen) then
      orb := Orbit(Group(g), p);;
      Add(lengths, Length(orb));
      Append(seen, orb);
    fi;
  od;
  Sort(lengths);
  return lengths;
end;;

f20CycleTypes := List(F20list, CycleTypeOf);;
distinctTypes := DuplicateFreeList(f20CycleTypes);;
Sort(distinctTypes);;
Print("distinct cycle types present in F20 (sorted lists, ascending lengths): ", distinctTypes, "\n");
transpositionType := [1,1,1,2];;
hasTranspositionType := (transpositionType in f20CycleTypes);;
Print("F20 contains a transposition-type element (cycle type {2,1,1,1}): ", PF(hasTranspositionType), "\n");
item4ok := not hasTranspositionType;;
Print("item 4 (F20 has NO transposition-type element, as required by the Dedekind test): ", PF(item4ok), "\n\n");

chainAllOk := item1ok and item2a_ok and item2b_ok and item3ok and item4ok;;
Print("=== c-prime chain (items 1-4) overall: ", PF(chainAllOk), " ===\n\n");

Print("total elapsed ms: ", Runtime()-startTime, "\n");

# ================================================================================
# write certificate JSON (numeric facts only; no interpretation)
# ================================================================================
certParts := [];;
Add(certParts, "{\n");
Add(certParts, "  \"schema\": \"a5-dessin-crosscheck/v1\",\n");
Add(certParts, Concatenation("  \"gap_version\": \"", GAPInfo.Version, "\",\n"));
Add(certParts, "  \"input_conventions\": {\n");
Add(certParts, "    \"universe\": \"all (g0,g1) in S5 x S5 (120x120=14400), triple counts iff ord(g0)=ord(g1)=ord(g0*g1)=5, ginf:=(g0*g1)^-1\",\n");
Add(certParts, "    \"v\": \"cycle (1,2,3,4,5), GAP PermList([2,3,4,5,1])\",\n");
Add(certParts, "    \"conjugation_action\": \"a: (g0,g1) -> (g0^a, g1^a) with GAP convention g^a = a^-1*g*a\"\n");
Add(certParts, "  },\n");
Add(certParts, "  \"task_a\": {\n");
Add(certParts, Concatenation("    \"total_triples\": ", String(totalAll), ",\n"));
Add(certParts, Concatenation("    \"a5_type_count\": ", String(totalA5), ",\n"));
Add(certParts, Concatenation("    \"c5_type_count\": ", String(totalC5), ",\n"));
Add(certParts, Concatenation("    \"anomaly_count\": ", String(anomalyCount), ",\n"));
Add(certParts, Concatenation("    \"a5_conjugation_orbit_count\": ", String(Length(orbitsA5)), ",\n"));
Add(certParts, Concatenation("    \"a5_conjugation_orbit_sizes\": ", String(orbitSizesA5), ",\n"));
Add(certParts, Concatenation("    \"s5_conjugation_orbit_count\": ", String(Length(orbitsS5)), ",\n"));
Add(certParts, Concatenation("    \"s5_conjugation_orbit_sizes\": ", String(orbitSizesS5), ",\n"));
Add(certParts, Concatenation("    \"all_a5_type_subgroups_equal_A5\": ", JB(allEqualA5), ",\n"));
Add(certParts, Concatenation("    \"centralizer_S5_of_A5_order\": ", String(centSizeA5), ",\n"));
Add(certParts, Concatenation("    \"representative_cycle_counts\": {\"c0\": ", String(c0), ", \"c1\": ", String(c1), ", \"cinf\": ", String(cinf), "},\n"));
Add(certParts, Concatenation("    \"genus_from_representative\": ", String(genusVal), ",\n"));
Add(certParts, Concatenation("    \"genus_constant_across_all_a5_pairs\": ", JB(genusConstant), ",\n"));
Add(certParts, Concatenation("    \"D_v_count\": ", String(Length(Dv)), ",\n"));
Add(certParts, Concatenation("    \"fix_g1_images\": ", String(fixImages), ",\n"));
Add(certParts, Concatenation("    \"all_fix_g1_empty\": ", JB(allFixEmpty), ",\n"));
Add(certParts, Concatenation("    \"map_well_defined_into_five_points\": ", JB(wellDefinedAsMapTo5), ",\n"));
Add(certParts, Concatenation("    \"map_bijective_onto_five_points\": ", JB(bijectiveOntoFive), ",\n"));
Add(certParts, Concatenation("    \"v_equivariance_pointwise_holds\": ", JB(equivOk), ",\n"));
Add(certParts, "    \"item5_superseded_note\": \"item5 above (fix_g1_images .. v_equivariance_pointwise_holds) implements the commander's ORIGINAL (a).5 wording literally (g0,g1 both order 5); this was a transcription error by the commander -- see item5_corrected below for the actual v2 sec.3.6 FC-6 spec (q order 2, r order 3). Kept unmodified as audit trail.\",\n");
Add(certParts, "    \"item5_corrected\": {\n");
Add(certParts, "      \"spec\": \"D(v) := {(q,r): q in 2A (order 2, exactly 1 fixed point), r in 3A (order 3), qrv=1}; word convention ambiguous, both computed\",\n");
Add(certParts, "      \"primary_convention\": \"main\",\n");
Add(certParts, Concatenation("      \"q2A_candidate_count\": ", String(Length(q2Alist)), ",\n"));
Add(certParts, Concatenation("      \"r3A_candidate_count\": ", String(Length(r3Alist)), ",\n"));
Add(certParts, "      \"main\": {\n");
Add(certParts, "        \"equation\": \"v*r*q = One(G)\",\n");
Add(certParts, Concatenation("        \"D_v_count\": ", String(resMain.count), ",\n"));
Add(certParts, Concatenation("        \"fix_q_images\": ", String(resMain.images), ",\n"));
Add(certParts, Concatenation("        \"well_defined\": ", JB(resMain.wellDefined), ",\n"));
Add(certParts, Concatenation("        \"bijective_onto_five_points\": ", JB(resMain.bijective), ",\n"));
Add(certParts, Concatenation("        \"stable_under_v_conjugation\": ", JB(resMain.stableUnderV), ",\n"));
Add(certParts, Concatenation("        \"v_equivariant\": ", JB(resMain.equivariant), "\n"));
Add(certParts, "      },\n");
Add(certParts, "      \"naive\": {\n");
Add(certParts, "        \"equation\": \"q*r*v = One(G)\",\n");
Add(certParts, Concatenation("        \"D_v_count\": ", String(resNaive.count), ",\n"));
Add(certParts, Concatenation("        \"fix_q_images\": ", String(resNaive.images), ",\n"));
Add(certParts, Concatenation("        \"well_defined\": ", JB(resNaive.wellDefined), ",\n"));
Add(certParts, Concatenation("        \"bijective_onto_five_points\": ", JB(resNaive.bijective), ",\n"));
Add(certParts, Concatenation("        \"stable_under_v_conjugation\": ", JB(resNaive.stableUnderV), ",\n"));
Add(certParts, Concatenation("        \"v_equivariant\": ", JB(resNaive.equivariant), "\n"));
Add(certParts, "      }\n");
Add(certParts, "    }\n");
Add(certParts, "  },\n");
Add(certParts, "  \"task_c_prime\": {\n");
Add(certParts, Concatenation("    \"item1_t1_specialization_matches\": ", JB(item1ok), ",\n"));
Add(certParts, Concatenation("    \"item2a_factorization_matches\": ", JB(item2a_ok), ",\n"));
Add(certParts, Concatenation("    \"item2b_separable_gcd_deg\": ", String(gcdDeg), ",\n"));
Add(certParts, Concatenation("    \"item3_mod3_factor_degrees_sorted\": ", String(degs3), ",\n"));
Add(certParts, Concatenation("    \"item3_matches_2_1_1_1_type\": ", JB(item3ok), ",\n"));
Add(certParts, Concatenation("    \"F20_order\": ", String(F20size), ",\n"));
Add(certParts, Concatenation("    \"F20_distinct_cycle_types\": ", String(distinctTypes), ",\n"));
Add(certParts, Concatenation("    \"F20_has_transposition_type\": ", JB(hasTranspositionType), ",\n"));
Add(certParts, Concatenation("    \"item4_no_transposition_type\": ", JB(item4ok), "\n"));
Add(certParts, "  }\n");
Add(certParts, "}\n");
for idx in [1..Length(certParts)] do
  if not IsString(certParts[idx]) then
    Print("[DEBUG] certParts[", idx, "] is not a string: ", certParts[idx], "\n");
  fi;
od;
certJson := Concatenation(certParts);;
WriteFileRaw("certificates/a5/gap_dessin_crosscheck.json", certJson);;
Print("\nwrote certificates/a5/gap_dessin_crosscheck.json\n");

QUIT;
