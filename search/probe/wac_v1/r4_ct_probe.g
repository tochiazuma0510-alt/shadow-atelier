## probe: CharacterTable("Symmetric",20) availability + ClassMultiplicationCoefficient
t0 := Runtime();;
ct := CharacterTable("Symmetric", 20);;
Print("built CT, time = ", Runtime()-t0, " ms\n");
Print("NrConjugacyClasses = ", NrConjugacyClasses(ct), "\n");
ordtbl := OrdersClassRepresentatives(ct);;
Print("orders sample: ", ordtbl{[1..10]}, "\n");
sizes := SizesConjugacyClasses(ct);;
Print("Size(G) = ", Size(ct), " sum sizes = ", Sum(sizes), "\n");
## find class of order 2 -- there will be several (different transposition counts)
## GAP's CharacterTable("Symmetric",n) orders classes by partitions; need to map
## cycle type -> class index. Use ClassParameters if available.
if IsBound(ClassParameters) then
  cp := ClassParameters(ct);;
  Print("ClassParameters bound, sample: ", cp{[1..5]}, "\n");
else
  Print("ClassParameters NOT bound as global\n");
fi;
cpx := CharacterParameters(ct);;
Print("first few CharacterParameters: ", cpx{[1..3]}, "\n");
## try the "identifier" route: GAP has function for this table specifically
Print("Identifier: ", Identifier(ct), "\n");
t1 := Runtime();;
cmc := ClassMultiplicationCoefficient(ct, 2, 2, 2);;
Print("ClassMultiplicationCoefficient test = ", cmc, " time=", Runtime()-t1, " ms\n");
QUIT;
