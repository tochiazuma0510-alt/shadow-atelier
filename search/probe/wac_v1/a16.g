#############################################################################
## search/probe/wac_v1/a16.g -- WA-c: realize n=16, lam(u)=(11,2,2,1)
## Single lane. NOT a ledger claim. No commit.
#############################################################################

WacCT := function(p, n)
  return SortedList(List(Orbits(Group(p), [1..n]), Length));
end;;
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
    p := p * WacCyc(List([1..len], j -> base + j)); base := base + len;
  od;
  return p;
end;;

n := 16;;
S16 := SymmetricGroup(16);; A16 := AlternatingGroup(16);;
uu := (1,2,3,4,5,6,7,8,9,10,11)*(12,13)*(14,15);;   # type (11,2,2,1)
Print("u type = ", WacCT(uu,16), "  ord = ", Order(uu),
      "  u^2 type = ", WacCT(uu^2,16), " ord = ", Order(uu^2), "\n");
Print("u in A16 ? ", SignPerm(uu) = 1, "\n\n");

inv := WacBlock(8,2);;              # 2^8
Print("target a1 class type = ", WacCT(inv,16), " sign=", SignPerm(inv), "\n");
Print("target b1 class type = 3^5 1 ; sign=", SignPerm(WacBlock(5,3)), "\n\n");

found := [];; trans := 0;; isA16 := 0;;
for i in [1..400000] do
  a1 := inv ^ Random(S16);
  b1 := a1 * uu^-1;              # a1*b1 = u^-1  <=>  u = b1^-1*a1
  if WacCT(b1,16) = [1,3,3,3,3,3] then
    G := Group(a1,b1);
    if IsTransitive(G, [1..16]) then
      trans := trans + 1;
      if G = A16 then
        isA16 := isA16 + 1;
        if Length(found) = 0 then Add(found, rec(a1:=a1, b1:=b1)); fi;
      fi;
    else
      Add(found, rec(a1:=a1, b1:=b1, orb := List(Orbits(G,[1..16]), Length)));
    fi;
  fi;
od;
Print("pairs with correct (a1,b1) classes: ", Length(found),
      "  transitive: ", trans, "  = A16: ", isA16, "\n");
if isA16 > 0 then
  Print("a1 := ", found[1].a1, ";;\n");
  Print("b1 := ", found[1].b1, ";;\n");
  Print("check: b1^-1*a1 = u ? ", found[1].b1^-1 * found[1].a1 = uu, "\n");
  Print("ord(a1)=", Order(found[1].a1), " ord(b1)=", Order(found[1].b1), "\n");
else
  Print("orbit shapes of the intransitive ones found:\n");
  for r in found do if IsBound(r.orb) then Print("   ", r.orb, "\n"); fi; od;
fi;
Print("\nA16_DONE\n");
QUIT;
