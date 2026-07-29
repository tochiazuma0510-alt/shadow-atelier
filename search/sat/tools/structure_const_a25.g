#############################################################################
## search/sat/tools/structure_const_a25.g -- EXACT class-only solution
## count for the n=25, ell=17 SAT target (sol/sol_reply_84_math11.md sec
## 6.3), computed via the S_25 ordinary character table (1958 classes,
## Murnaghan-Nakayama-based construction, no brute enumeration). Answers:
## for the FIXED u=(1..17)(18,19)(20,21)(22,23)(24,25), how many a in the
## conjugacy class 2^12 1 have b:=a*u^-1 in class 3^8 1?
##
## Derivation (class-algebra structure constant, standard textbook
## identity): let A = class(2^12,1), B = class(3^8,1), U = class(u)
## (note u and u^-1 share a class since both are type (17,2,2,2,2)).
## For a FIXED representative u0 of U, by conjugation-invariance the
## quantity M := #{b in B : b*u0 in A} is the SAME for every choice of
## u0 in U. Summing over all of U gives
##   Sum_{u0 in U} #{b in B : b*u0 in A} = a_{B,U,A} * |A|
## where a_{B,U,A} = ClassMultiplicationCoefficient(B,U,A) is the number
## of pairs (b,u0) in B x U whose product equals one FIXED representative
## of A (GAP's standard definition). Hence M = a_{B,U,A} * |A| / |U|.
## Since b*u0 = a  <=>  b = a*u0^-1, and u0 ranges over U while u0^-1
## ranges over U^-1 = U (same class), M is EXACTLY the count of interest:
## #{a in A : a*u^-1 in B} for our fixed u.
#############################################################################
ct := CharacterTable("Symmetric",25);;
ords := OrdersClassRepresentatives(ct);;
sizes := SizesConjugacyClasses(ct);;
# find class indices matching our partitions via CycleStructurePerm-style check
# use ClassParameters if available
cp := ClassParameters(ct);;
Print("sample cp[1]=", cp[1], "\n");
FindClassByPartition := function(ct, part)
  local cp, i, n;
  cp := ClassParameters(ct);
  n := Sum(part);
  for i in [1..Length(cp)] do
    if SortedList(cp[i][2]) = SortedList(part) then
      return i;
    fi;
  od;
  return fail;
end;;

idxA := FindClassByPartition(ct, [1,2,2,2,2,2,2,2,2,2,2,2,2]);;   # 2^12 1
idxB := FindClassByPartition(ct, [1,3,3,3,3,3,3,3,3]);;           # 3^8 1
idxU := FindClassByPartition(ct, [2,2,2,2,17]);;                  # (17,2,2,2,2)
Print("idxA=", idxA, " idxB=", idxB, " idxU=", idxU, "\n");
Print("sizeA=", sizes[idxA], " sizeB=", sizes[idxB], " sizeU=", sizes[idxU], "\n");

# a_{B,U,A}: pairs (b,u0) with b in B, u0 in U, b*u0 = fixed elt of A
c_BUA := ClassMultiplicationCoefficient(ct, idxB, idxU, idxA);;
Print("ClassMultiplicationCoefficient(B,U,A)=", c_BUA, "\n");

M := c_BUA * sizes[idxA] / sizes[idxU];;
Print("M (= #{b in B : b*u0 in A} for FIXED u0) = ", M, "\n");
Print("EQUALS #{a in class(2^12,1) : a*uinv in class(3^8,1)} for our FIXED u = ", M, "\n");
QUIT;
