#############################################################################
## search/probe/wac_v1/ss_nonalt3.g -- realize the non-alternating candidates
## Target: (2,3)-generating pair (a1,b1) of P with u=b1^-1*a1, ord(u)>=7 and
## C_P(u^2) NONSOLVABLE.  Then E = P x S3 (Prop 0.3), P perfect.
## Single lane. NOT a ledger claim. No commit. No u (sealed symbol).
#############################################################################
RandOrd := function(G, d)
  local g, o, t;
  t := 0;
  repeat g := Random(G); o := Order(g); t := t+1;
     if t > 400 then return fail; fi; until o mod d = 0;
  return g^(o/d);
end;;

Hunt := function(nm, G, outsz, tries)
  local i, a1, b1, uu, xx, cx, gen, hit, tally;
  Print("\n===== ", nm, " |P|=", Size(G), " deg=", LargestMovedPoint(G),
        " |Out|=", outsz, " =====\n");
  gen := 0; hit := 0; tally := [];
  for i in [1..tries] do
    a1 := RandOrd(G,2); b1 := RandOrd(G,3);
    if a1 = fail or b1 = fail then continue; fi;
    if Size(Group(a1,b1)) = Size(G) then
      gen := gen + 1;
      uu := b1^-1*a1;
      if Order(uu) >= 7 then
        xx := uu^2;
        if Order(xx) >= 4 then
          cx := Centralizer(G, xx);
          if not IsSolvableGroup(cx) then
            hit := hit + 1;
            if hit = 1 then
              Print("  HIT at try ", i, ": ord(u)=", Order(uu),
                    " N_ord=ord(xbar)=", Order(xx),
                    " |C_P(xbar)|=", Size(cx), " (", StructureDescription(cx), ")\n");
              Print("  c_m=phi(", 2*Order(xx), ")=", Phi(2*Order(xx)),
                    "  Xi<=", Phi(2*Order(xx))*Size(cx)*Size(cx)*outsz,
                    "  naive=", Phi(2*Order(xx))*Size(G), "\n");
              Print("  a1 := ", a1, ";;\n  b1 := ", b1, ";;\n");
            fi;
          fi;
          if not [Order(uu), Order(xx), IsSolvableGroup(cx)] in tally then
            Add(tally, [Order(uu), Order(xx), IsSolvableGroup(cx)]); fi;
        fi;
      fi;
    fi;
  od;
  Print("  (2,3)-generating pairs: ", gen, "/", tries,
        "   Cor 7.2 hits: ", hit, "\n");
  Print("  observed [ord u, ord xbar, C solvable]: ", tally, "\n");
end;;

Hunt("PSU(3,4)", Image(IsomorphismPermGroup(PSU(3,4))), 4, 20000);
Hunt("J2",       PrimitiveGroup(100,1),                 2, 12000);
Hunt("PSL(3,5)", Image(IsomorphismPermGroup(PSL(3,5))), 2, 20000);
Print("\nSS_NONALT3_DONE\n");
QUIT;
