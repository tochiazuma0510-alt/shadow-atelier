## PSp(4,5): the remaining non-alternating candidate (N_ord = 6 = 2*3 class)
RandOrd := function(G, d)
  local g, o, t;
  t := 0;
  repeat g := Random(G); o := Order(g); t := t+1;
     if t > 400 then return fail; fi; until o mod d = 0;
  return g^(o/d);
end;;
G := Image(IsomorphismPermGroup(PSp(4,5)));;
Print("PSp(4,5) |P|=", Size(G), " deg=", LargestMovedPoint(G), "\n");
Print("--- classes with ord>=4 and NONSOLVABLE centralizer, with u-sources ---\n");
ccl := ConjugacyClasses(G);;
for c in ccl do
  x := Representative(c);
  if Order(x) < 4 then continue; fi;
  cx := Centralizer(G, x);
  if IsSolvableGroup(cx) then continue; fi;
  sq := Filtered(ccl, d -> Order(Representative(d)) >= 7 and Representative(d)^2 in c);
  Print("  ord(x)=", Order(x), " |C|=", Size(cx), " (", StructureDescription(cx),
        ")  N_ord=", Order(x), " c_m=", Phi(2*Order(x)),
        "  Xi<=", Phi(2*Order(x))*Size(cx)*Size(cx)*2,
        "  naive=", Phi(2*Order(x))*Size(G),
        "  u-sources(ord>=7): ", List(sq, d -> Order(Representative(d))), "\n");
od;
Print("--- targeted (2,3) hunt ---\n");
gen := 0;; hit := 0;; tally := [];;
for i in [1..25000] do
  a1 := RandOrd(G,2); b1 := RandOrd(G,3);
  if a1 = fail or b1 = fail then continue; fi;
  if Size(Group(a1,b1)) = Size(G) then
    gen := gen + 1;
    uu := b1^-1*a1;
    if Order(uu) >= 7 and Order(uu^2) >= 4 then
      cx := Centralizer(G, uu^2);
      if not [Order(uu), Order(uu^2), IsSolvableGroup(cx)] in tally then
        Add(tally, [Order(uu), Order(uu^2), IsSolvableGroup(cx)]); fi;
      if not IsSolvableGroup(cx) then
        hit := hit + 1;
        if hit = 1 then
          Print("  HIT try ", i, ": ord(u)=", Order(uu), " N_ord=", Order(uu^2),
                " |C|=", Size(cx), " (", StructureDescription(cx), ")\n");
          Print("  a1 := ", a1, ";;\n  b1 := ", b1, ";;\n");
        fi;
      fi;
    fi;
  fi;
od;
Print("  (2,3)-generating pairs: ", gen, "/25000   hits: ", hit, "\n");
Print("  observed [ord u, N_ord, C solvable]: ", tally, "\n");
Print("\nSS_SP45_DONE\n");
QUIT;
