#############################################################################
## search/probe/wac_v1/ss_classes.g -- EXACT class-level gate for non-alternating P
##
## For P simple (Z(P)=1): Stab_{Aut(P)}(xbar) is an extension of a subgroup of
## Out(P) by C_P(xbar); for every P below Out(P) is (visibly) solvable, so
##      Cor 7.2 holds  <=>  C_P(xbar) is NONSOLVABLE.
## Necessary conditions on xbar (from Lemma 0.2 / Cor 0.4):
##      xbar = u^2 with ord(u) >= 7   =>   ord(xbar) >= 4  and  xbar is a square
##      of an element of order >= 7.
## This script enumerates ALL classes and reports every class passing them.
## Single lane. NOT a ledger claim. No commit. No u (sealed symbol).
#############################################################################

Cands := [
  ["PSL(3,5)",  PSL(3,5)],   ["PSL(3,7)",  PSL(3,7)],
  ["PSL(3,8)",  PSL(3,8)],   ["PSL(3,9)",  PSL(3,9)],
  ["PSL(4,3)",  PSL(4,3)],   ["PSU(4,2)",  PSU(4,2)],
  ["PSU(3,4)",  PSU(3,4)],   ["PSU(3,5)",  PSU(3,5)],
  ["PSp(6,2)",  PSp(6,2)],   ["PSp(4,5)",  PSp(4,5)],
  ["M11", MathieuGroup(11)],  ["M12", MathieuGroup(12)],
  ["M22", MathieuGroup(22)],  ["M23", MathieuGroup(23)],
  ["M24", MathieuGroup(24)],  ["J2",  PrimitiveGroup(100,1)],
];;

for pair in Cands do
  nm := pair[1];  G0 := pair[2];
  if not IsPermGroup(G0) then G := Image(IsomorphismPermGroup(G0)); else G := G0; fi;
  Print("\n===== ", nm, "  |P|=", Size(G), "  degree=", LargestMovedPoint(G), " =====\n");
  ccl := ConjugacyClasses(G);
  ords := Set(List(ccl, c -> Order(Representative(c))));
  hits := 0;
  for c in ccl do
    x := Representative(c);
    if Order(x) < 4 then continue; fi;
    cx := Centralizer(G, x);
    if IsSolvableGroup(cx) then continue; fi;
    # is xbar a square of an element of order >= 7 ?
    sq := Filtered(ccl, d -> Order(Representative(d)) >= 7 and
                             Representative(d)^2 in c);
    hits := hits + 1;
    Print("  CLASS ord(xbar)=", Order(x), " |class|=", Size(c),
          " |C_P(xbar)|=", Size(cx), " (", StructureDescription(cx),
          ") NONSOLVABLE ; sources u with ord>=7 and u^2 ~ xbar : ",
          List(sq, d -> Order(Representative(d))), "\n");
  od;
  if hits = 0 then
    Print("  no class with ord>=4 and nonsolvable centralizer  -> DEAD for Cor 7.2\n");
  fi;
  Print("  (element orders present: ", ords, ")\n");
od;
Print("\nSS_CLASSES_DONE\n");
QUIT;
