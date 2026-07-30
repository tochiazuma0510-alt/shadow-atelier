#############################################################################
## search/probe/wac_v1/i10_check.g
##  I10-1 (ideas_010) の判別窓の存在設計。
##  xbar = (ell^r, 1^t) 型。r=3 は ell 奇を強制、系 0.4' は ell>=4 を強制
##  => ell=3 は不可(発案の最小候補 (3,3,3,1^4) は対象非存在)。ell=5 が最小。
##  PART 1: r=2, ell=5, t=0, n=10, w=(10)      -- 悉皆(S10 の全対合)
##  PART 2: r=3, ell=5, t=0, n=15, w=(10)(5)   -- 無作為探索(存在の構成的証明)
##  PART 3: r=3, ell=5, t=1, n=16, w=(10)(5)1  -- 予備
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
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
    p := p * WacCyc(List([1..len], j -> base+j)); base := base + len;
  od;
  return p;
end;;
NC := function(p, n)
  return n - NrMovedPoints(p) + Length(Cycles(p, MovedPoints(p)));
end;;

Window := function(nn, a1, b1, id, xbar)
  local Snn, Ann, aE, bE, WinE, s1, s2, cc, xb, yb, PN, Nord, CPy, StabX,
        charm, cm, O2, Syl;
  Snn := SymmetricGroup(nn); Ann := AlternatingGroup(nn);
  Print("\n===== ", id, "   (n=", nn, ") =====\n");
  Print("a1 = ", a1, "\nb1 = ", b1, "\n");
  Print("a1^2=1 ", a1^2=(), "  b1^3=1 ", b1^3=(),
        "  sign(a1)=", SignPerm(a1), "  sign(b1)=", SignPerm(b1), "\n");
  Print("<a1,b1> = ", Size(Group(a1,b1)), "  A_n? ", Group(a1,b1)=Ann,
        "  S_n? ", Group(a1,b1)=Snn, "\n");
  Print("w type ", CycleStructurePerm(b1^-1*a1), " ord ", Order(b1^-1*a1),
        "   xbar type ", CycleStructurePerm(xbar), " ord ", Order(xbar), "\n");
  Print("Ree c(a)+c(b)+c(w) = ", NC(a1,nn), "+", NC(b1,nn), "+", NC(b1^-1*a1,nn),
        " = ", NC(a1,nn)+NC(b1,nn)+NC(b1^-1*a1,nn), "  n+2 = ", nn+2,
        "  genus = ",
        ((3*nn-(NC(a1,nn)+NC(b1,nn)+NC(b1^-1*a1,nn)))-2*nn+2)/2, "\n");
  aE := a1*(nn+1,nn+3); bE := b1*(nn+1,nn+3,nn+2);
  WinE := Group(aE,bE);
  s1 := bE^-1*aE; s2 := aE*bE^2; cc := (s1*s2)^3;
  Print("|E| = ", Size(WinE), "  = 6|A_n|? ", Size(WinE)=6*Size(Ann), "\n");
  Print("braid ? ", s1*s2*s1=s2*s1*s2, "   c=(s1s2)^3=1 ? ", cc=(),
        "   ord(s1)=", Order(s1), "\n");
  xb := s1^2; yb := s2^2; PN := Group(xb,yb);
  Print("|P| = ", Size(PN), "  = |A_n|? ", Size(PN)=Size(Ann), "\n");
  Nord := Lcm(Order(xb),Order(yb),Order(cc));
  Print("ord(x)=", Order(xb), " ord(y)=", Order(yb), " ord(c)=", Order(cc),
        "   N_ord = ", Nord, "\n");
  CPy := Centralizer(PN, yb); StabX := Centralizer(Snn, xbar);
  O2 := PCore(StabX, 5);
  Print("C_P(ybar)  = ", Size(CPy), "  ", StructureDescription(CPy), "\n");
  Print("Stab(xbar) = ", Size(StabX), "  ", StructureDescription(StabX), "\n");
  Print("   Syl2(Stab) = ", Size(SylowSubgroup(StabX,2)), "  ",
        StructureDescription(SylowSubgroup(StabX,2)), "\n");
  Print("   O_{2'}(Stab) = ", Size(Filtered([1],x->true)), " -> computing\n");
  Syl := NormalSubgroups(StabX);
  Syl := Filtered(Syl, x -> Size(x) mod 2 = 1);
  Print("   largest odd normal subgroup of Stab = ",
        Maximum(List(Syl,Size)), "  ",
        StructureDescription(First(Syl, x -> Size(x)=Maximum(List(Syl,Size)))), "\n");
  Print("   <xbar> order = ", Order(xbar), "\n");
  charm := Filtered([0..Nord-1], m -> GcdInt(2*m+1,Nord)=1);
  cm := Length(charm);
  Print("charming m = ", charm, "  cm = ", cm, "  phi(2*Nord) = ", Phi(2*Nord), "\n");
  Print("[P,P]=P ? ", DerivedSubgroup(PN)=PN, "\n");
  Print("Xi budget    = ", cm*Size(CPy)*Size(StabX), "\n");
  Print("naive budget = ", cm*Size(Ann), "\n");
  Print("JUDGE_S1_IMG := ", s1, ";;\n");
  Print("JUDGE_S2_IMG := ", s2, ";;\n");
  Print("JUDGE_ID := \"", id, "\";;   ## degree(E) = ", nn+3, "\n");
  return;
end;;

Print("#################################################################\n");
Print("## PART 1  r=2, ell=5, t=0, n=10, w = (1..10)   [exhaustive]\n");
Print("#################################################################\n");
w10 := WacCyc([1..10]);;
S10 := SymmetricGroup(10);; A10 := AlternatingGroup(10);;
Print("w = ", w10, "  ord ", Order(w10), "  xbar = w^2 type ",
      CycleStructurePerm(w10^2), " ord ", Order(w10^2), "\n");
sols10 := [];; cnt10 := 0;;
for k in [1..5] do
  for a in AsList(ConjugacyClass(S10, WacBlock(k,2))) do
    b := a*w10^-1;
    if b^3 = () and b <> () then
      cnt10 := cnt10 + 1;
      if Group(a,b) = A10 or Group(a,b) = S10 then Add(sols10,[a,b]); fi;
    fi;
  od;
od;
Print("#(a with b^3=1) = ", cnt10, "    #realizing (A10 or S10) = ",
      Length(sols10), "\n");
if Length(sols10) > 0 then
  Window(10, sols10[1][1], sols10[1][2], "W-E-A10-5x2t0", w10^2);
fi;

Print("\n#################################################################\n");
Print("## PART 2  r=3, ell=5, t=0, n=15, w = (1..10)(11..15)  [random]\n");
Print("#################################################################\n");
w15 := WacCyc([1..10])*WacCyc([11..15]);;
S15 := SymmetricGroup(15);; A15 := AlternatingGroup(15);;
Print("w = ", w15, "  ord ", Order(w15), "  xbar = w^2 type ",
      CycleStructurePerm(w15^2), " ord ", Order(w15^2), "\n");
Print("|C_S15(w)| = ", Size(Centralizer(S15,w15)), "\n");
found15 := [];; tries := 0;; hits := 0;;
for k in [5,7] do
  a0 := WacBlock(k,2);
  for i in [1..300000] do
    tries := tries + 1;
    a := a0^Random(S15);
    b := a*w15^-1;
    if b^3 = () and b <> () then
      hits := hits + 1;
      G := Group(a,b);
      if G = A15 or G = S15 then Add(found15,[a,b,k]); break; fi;
    fi;
  od;
  Print("  k=", k, ": tries so far ", tries, "  order-3 hits ", hits,
        "  realizing found ", Length(found15), "\n");
od;
Print("#realizing pairs found = ", Length(found15), "  (tries=", tries, ")\n");
if Length(found15) > 0 then
  Window(15, found15[1][1], found15[1][2], "W-E-A15-5x3t0", w15^2);
else
  Print("NO REALIZATION FOUND in random search -- UNKNOWN (not a proof of nonexistence)\n");
fi;

Print("\nI10_CHECK_DONE\n");
QUIT;
