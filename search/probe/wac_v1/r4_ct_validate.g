## Validate the class-multiplication-coefficient formula for structure
## constants against the KNOWN value from tail8_exact.g (n=21):
##   w0 = u = (1..13)(14,15)(16,17)(18,19)(20,21)  [cycle type 13,2,2,2,2]
##   a0 class = 2^10 1^1 (10 transpositions, 1 fixed point)
##   b  class = 3^7      (7 three-cycles, 0 fixed points)
##   known structconst = 4160  (from tail8_exact.g comment / TARGET)
## Formula being validated:
##   #{a' in A : a'*w0^-1 in B} = (|A| / |K(w0)|) * CMC(ct, iB, iW0, iA)
## where CMC(ct,i,j,k) = ClassMultiplicationCoefficient = #{(x,y) in Ci x Cj :
## xy = z} for fixed z in Ck.
n := 21;;
ct := CharacterTable("Symmetric", n);;
cp := ClassParameters(ct);;
sizes := SizesConjugacyClasses(ct);;

## helper: find class index matching a cycle-type partition (list of part
## sizes with multiplicity, e.g. k transpositions + rest fixed points).
## ClassParameters format: [1, partition] with partition descending, sum=n.
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

w0part := PartitionCycles(21, [13,2,2,2,2]);;
apart  := PartitionCycles(21, List([1..10], x->2));;
bpart  := PartitionCycles(21, List([1..7], x->3));;

iW0 := FindClassByPartition(cp, w0part);;
iA  := FindClassByPartition(cp, apart);;
iB  := FindClassByPartition(cp, bpart);;
Print("iW0=", iW0, " iA=", iA, " iB=", iB, "\n");
Print("|K(w0)|=", sizes[iW0], " |A|=", sizes[iA], " |B|=", sizes[iB], "\n");

cmc := ClassMultiplicationCoefficient(ct, iB, iW0, iA);;
Print("CMC(ct,iB,iW0,iA) = ", cmc, "\n");
val := (sizes[iA] / sizes[iW0]) * cmc;;
Print("formula result = ", val, "   known target = 4160   MATCH? ", val = 4160, "\n");
QUIT;
