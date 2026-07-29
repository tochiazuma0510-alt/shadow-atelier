## r4_structconst_scan.g -- compute structure constants for all (w0-type, k, m)
## cells for n=20, r=4, xbar=(5,5,5,5) window.  a in class 2^k 1^(20-2k),
## b := a*w0^-1, b in class 3^m 1^(20-3m).  k restricted to parity forced
## by sign(w0) (see r4_existence_20260730.json step1_parity_accounting).
## m ranges 1..6 (3*6=18<=20).
## Formula (validated against tail8_exact.g n=21 case, exact match 4160):
##   #{a' in A : a'*w0^-1 in B} = (|A|/|K(w0)|) * CMC(ct, iB, iW0, iA)
## Prints raw numbers only. No judgement.

n := 20;;
ct := CharacterTable("Symmetric", n);;
cp := ClassParameters(ct);;
sizes := SizesConjugacyClasses(ct);;

FindClassByPartition := function(cp, part)
  local i, p, sorted;
  sorted := Reversed(SortedList(Filtered(part, x -> x > 0)));
  for i in [1..Length(cp)] do
    p := cp[i][2];
    if Reversed(SortedList(Filtered(p, x -> x > 0))) = sorted then
      return i;
    fi;
  od;
  return fail;
end;;

PartitionCycles := function(n, cycLens)
  local used, part;
  used := Sum(cycLens);
  part := ShallowCopy(cycLens);
  Append(part, List([1..n-used], x -> 1));
  return part;
end;;

## w0 types (mirror r4_existence_search.g)
w0types := [
  rec(label:="type-A_(5,5,5,5)", cyc:=[5,5,5,5], sign:=1),
  rec(label:="type-B_(10,5,5)",  cyc:=[10,5,5],  sign:=-1),
  rec(label:="type-C_(10,10)",   cyc:=[10,10],   sign:=1)
];;

for wt in w0types do
  wt.w0part := PartitionCycles(n, wt.cyc);;
  wt.iW0 := FindClassByPartition(cp, wt.w0part);;
  ## k parity: even if sign(w0)=+1, odd if sign(w0)=-1 (from JSON step1)
  if wt.sign = 1 then
    wt.kparity := 0;
  else
    wt.kparity := 1;
  fi;
od;;

Print("#########################################################\n");
Print("## r4_structconst_scan  n=20  (3 w0-types x k x m=1..6)\n");
Print("#########################################################\n");

results := [];;
for wt in w0types do
  Print("\n=== ", wt.label, "  iW0=", wt.iW0, " |K(w0)|=", sizes[wt.iW0],
        "  sign=", wt.sign, "  kparity=", wt.kparity, " ===\n");
  for k in [1..QuoInt(n,2)] do
    if (k mod 2) <> wt.kparity then continue; fi;
    apart := PartitionCycles(n, List([1..k], x->2));;
    iA := FindClassByPartition(cp, apart);;
    for m in [1..6] do
      bpart := PartitionCycles(n, List([1..m], x->3));;
      iB := FindClassByPartition(cp, bpart);;
      cmc := ClassMultiplicationCoefficient(ct, iB, wt.iW0, iA);;
      val := (sizes[iA] / sizes[wt.iW0]) * cmc;;
      Print("  k=", k, " m=", m, "  iA=", iA, " |A|=", sizes[iA],
            " iB=", iB, " |B|=", sizes[iB], "  CMC=", cmc,
            "  structconst=", val, "\n");
      Add(results, rec(w0type:=wt.label, k:=k, m:=m, iA:=iA, sizeA:=sizes[iA],
                        iB:=iB, sizeB:=sizes[iB], iW0:=wt.iW0, sizeW0:=sizes[wt.iW0],
                        cmc:=cmc, structconst:=val));
    od;
  od;
od;

Print("\n\n#########################################################\n");
Print("## SANITY CHECK: sum over m of structconst(k,m) should equal\n");
Print("## |A_k| (every a in class A has a*w0^-1 landing SOMEWHERE,\n");
Print("## and the only possible orders for b are checked separately --\n");
Print("## here we just check internal consistency: for fixed w0type,k,\n");
Print("## sum_m structconst <= |A_k| (equality only if EVERY a*w0^-1 has\n");
Print("## order exactly 3, which is not generally true; this is an\n");
Print("## upper-bound sanity check, not an equality assert).\n");
Print("#########################################################\n");
for wt in w0types do
  for k in [1..QuoInt(n,2)] do
    if (k mod 2) <> wt.kparity then continue; fi;
    apart := PartitionCycles(n, List([1..k], x->2));;
    iA := FindClassByPartition(cp, apart);;
    total := Sum(Filtered(results, r -> r.w0type=wt.label and r.k=k), r -> r.structconst);;
    Print("  ", wt.label, " k=", k, "  sum_m structconst = ", total,
          "  |A_k| = ", sizes[iA], "  sum <= |A_k| ? ", total <= sizes[iA], "\n");
  od;
od;

Print("\nSTRUCTCONST_SCAN_DONE\n");
QUIT;
