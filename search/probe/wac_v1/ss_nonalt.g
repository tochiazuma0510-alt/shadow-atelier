#############################################################################
## search/probe/wac_v1/ss_nonalt.g -- second-strike slate, NON-alternating P
## Keep pairs whose C_P(xbar) is NONSOLVABLE (=> Stab_{Aut(P)}(xbar) also
## nonsolvable, since C_P(xbar) embeds in Stab when Z(P)=1).
##   Xi budget <= c_m * |C_P(ybar)| * |C_P(xbar)| * |Out(P)|
## v2: guard against groups with no order-3 elements (Sz(q)) -- v1 hung there.
## Single lane. NOT a ledger claim. No commit. No u (sealed symbol).
#############################################################################

Cands := [
  ["PSL(3,5)",  PSL(3,5),  2],       # |Out| = gcd(3,4)*1*2 = 2
  ["PSL(3,7)",  PSL(3,7),  6],       # |Out| = gcd(3,6)*1*2 = 6
  ["M11",       MathieuGroup(11), 1],
  ["M12",       MathieuGroup(12), 2],
  ["M22",       MathieuGroup(22), 2],
  ["PSp(6,2)",  PSp(6,2),  1],
  ["PSU(3,4)",  PSU(3,4),  4],
  ["PSL(3,8)",  PSL(3,8),  6],
];;

RandOrd := function(G, d)
  local g, o, tries;
  tries := 0;
  repeat
    g := Random(G); o := Order(g); tries := tries + 1;
    if tries > 400 then return fail; fi;
  until o mod d = 0;
  return g^(o/d);
end;;

for pair in Cands do
  nm := pair[1];  G0 := pair[2];  outsz := pair[3];
  if not IsPermGroup(G0) then G := Image(IsomorphismPermGroup(G0)); else G := G0; fi;
  Print("\n===== ", nm, "  |P|=", Size(G), "  perm degree=",
        LargestMovedPoint(G), "  |Out|=", outsz, " =====\n");
  if Size(G) mod 3 <> 0 then
    Print("  (no elements of order 3 -- not (2,3)-generated)  SKIP\n"); continue; fi;
  keys := [];  gen23 := 0;
  for i in [1..1200] do
    a1 := RandOrd(G,2);  b1 := RandOrd(G,3);
    if a1 = fail or b1 = fail then continue; fi;
    if Size(Group(a1,b1)) = Size(G) then
      gen23 := gen23 + 1;
      uu := b1^-1*a1;
      if Order(uu) >= 7 and Order(uu^2) >= 4 then
        xx := uu^2;
        if not [Order(uu), Order(xx)] in keys then
          Add(keys, [Order(uu), Order(xx)]);
          cx := Centralizer(G, xx);
          Print("  ord(u)=", Order(uu), " N_ord=ord(xbar)=", Order(xx),
                "  |C_P(xbar)|=", Size(cx), " solvable=", IsSolvableGroup(cx));
          if not IsSolvableGroup(cx) then
            Print("  <<< HIT  struct=", StructureDescription(cx),
                  "  c_m=", Phi(2*Order(xx)),
                  "  Xi<=", Phi(2*Order(xx))*Size(cx)*Size(cx)*outsz,
                  "  naive=", Phi(2*Order(xx))*Size(DerivedSubgroup(G)));
          fi;
          Print("\n");
        fi;
      fi;
    fi;
  od;
  Print("  (2,3)-generating pairs seen: ", gen23, " / 1200\n");
od;
Print("\nSS_NONALT_DONE\n");
QUIT;
