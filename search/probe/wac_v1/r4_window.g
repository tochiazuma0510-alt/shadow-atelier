#############################################################################
## search/probe/wac_v1/r4_window.g
##  r=4 判別窓(xbar=(5,5,5,5), n=20)の 2 枝の窓 assert と諸元。
##  canonical 対は search/certs/r4_exhaustive_20260730.json の orbit_reps から
##  「eq_S20 / eq_A20 が true になる最初の代表」を取る(LID-1: 同一性は語+SHA)。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
CycFromList := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;
NC := function(p, n)
  return n - NrMovedPoints(p) + Length(Cycles(p, MovedPoints(p)));
end;;

DoR4 := function(nn, a1, b1, wid)
  local Snn, Ann, aE, bE, WinE, s1, s2, cc, xb, yb, PN, Nord, charm, cm,
        Stab, CPy, S2, cyc, Bg, Bx, BS, NX, Xi, naive, predKer, predG, i, v;
  Snn := SymmetricGroup(nn); Ann := AlternatingGroup(nn);
  Print("\n===== ", wid, "   n=", nn, " =====\n");
  Print("a1 = ", a1, "\nb1 = ", b1, "\n");
  Print("a1^2=1 ", a1^2=(), "  b1^3=1 ", b1^3=(),
        "  k=", NrMovedPoints(a1)/2, "  j=", NrMovedPoints(b1)/3,
        "  sign(a1)=", SignPerm(a1), "  sign(b1)=", SignPerm(b1), "\n");
  Print("w = b1^-1*a1 = ", b1^-1*a1, "\n");
  Print("   w type ", CycleStructurePerm(b1^-1*a1), " ord ", Order(b1^-1*a1), "\n");
  Print("xbar = w^2 type ", CycleStructurePerm((b1^-1*a1)^2),
        " ord ", Order((b1^-1*a1)^2), "\n");
  Print("<a1,b1> = ", Size(Group(a1,b1)), "  A_n? ", Group(a1,b1)=Ann,
        "  S_n? ", Group(a1,b1)=Snn, "\n");
  Print("Ree c(a)+c(b)+c(w) = ", NC(a1,nn), "+", NC(b1,nn), "+", NC(b1^-1*a1,nn),
        " = ", NC(a1,nn)+NC(b1,nn)+NC(b1^-1*a1,nn), "   n+2 = ", nn+2,
        "   genus = ",
        ((3*nn-(NC(a1,nn)+NC(b1,nn)+NC(b1^-1*a1,nn)))-2*nn+2)/2, "\n");
  aE := a1*(nn+1,nn+3); bE := b1*(nn+1,nn+3,nn+2);
  WinE := Group(aE,bE);
  s1 := bE^-1*aE; s2 := aE*bE^2; cc := (s1*s2)^3;
  Print("|E| = ", Size(WinE), "   = 6|A_n| ? ", Size(WinE)=6*Size(Ann), "\n");
  Print("braid ? ", s1*s2*s1=s2*s1*s2, "   c=(s1s2)^3=1 ? ", cc=(),
        "   ord(s1)=", Order(s1), "\n");
  xb := s1^2; yb := s2^2; PN := Group(xb,yb);
  Print("|P| = ", Size(PN), "  = |A_n| ? ", Size(PN)=Size(Ann), "\n");
  Nord := Lcm(Order(xb), Order(yb), Order(cc));
  Print("ord(x)=", Order(xb), " ord(y)=", Order(yb), " ord(c)=", Order(cc),
        "   N_ord = ", Nord, "\n");
  Print("[P,P]=P ? ", DerivedSubgroup(PN)=PN, "\n");
  charm := Filtered([0..Nord-1], z -> GcdInt(2*z+1,Nord)=1);
  cm := Length(charm);
  Print("charming m = ", charm, "   c_m = ", cm, " = phi(2N) = ", Phi(2*Nord), "\n");
  Stab := Centralizer(Snn, xb); CPy := Centralizer(PN, yb);
  NX := Normalizer(Snn, Group(xb));
  Print("Stab(xbar) = ", Size(Stab), "  ", StructureDescription(Stab), "\n");
  Print("C_P(ybar)  = ", Size(CPy), "\n");
  Print("N_{S_n}(<xbar>) = ", Size(NX), "\n");
  S2 := SylowSubgroup(Stab, 2);
  Print("S := Syl_2(Stab) = ", Size(S2), "  ", StructureDescription(S2), "\n");
  ## base B_x と S の固定点
  cyc := Cycles(xb, MovedPoints(xb));
  Bg := List(cyc, c -> CycFromList(c));
  Bx := Group(Bg);
  Print("xbar の巡回 (r=", Length(cyc), "): ", cyc, "\n");
  Print("base B_x = ", Size(Bx), " (=5^", Length(cyc), ")   xbar = 対角? ",
        Product(Bg) = xb, "\n");
  BS := Centralizer(Bx, S2);
  Print("C_{B_x}(S) = ", Size(BS), "  ", StructureDescription(BS),
        "   = <xbar> ? ", BS = Group(xb), "\n");
  Print("   S の 4 ブロックへの作用が推移的か: (|C_B(S)| = 5 なら全対角)\n");
  Xi := cm * Size(CPy) * Size(Stab);
  naive := cm * Size(Ann);
  Print("Xi budget    = ", Xi, "\n");
  Print("naive budget = ", naive, "\n");
  Print("JUDGE_S1_IMG := ", s1, ";;\n");
  Print("JUDGE_S2_IMG := ", s2, ";;\n");
  Print("JUDGE_ID := \"", wid, "\";;   ## degree(E) = ", nn+3, "\n");
  return;
end;;

## ---- B 枝: type-B (10,5,5), k=9, m=6 -> S20  (eps=1, fibre product) ----
DoR4(20,
  (1,15)(3,14)(4,5)(6,13)(7,20)(8,9)(10,19)(11,18)(12,16),
  (1,14,2)(3,13,5)(6,12,20)(7,19,9)(10,18,15)(11,17,16),
  "W-E-A20-5x4t0-B");

## ---- C 枝: type-C (10,10), k=8, m=6 -> A20  (eps=0, direct product) ----
DoR4(20,
  (1,14)(2,15)(3,10)(5,9)(6,7)(12,19)(13,16)(17,18),
  (1,13,15)(2,14,10)(3,9,4)(5,8,7)(11,20,19)(12,18,16),
  "W-E-A20-5x4t0-C");

## ---- 予言対象の群の IdGroup ----
Print("\n---- 予言される群の IdGroup ----\n");
D8 := DihedralGroup(IsPermGroup, 8);;
C5 := CyclicGroup(IsPermGroup, 5);;
K1 := DirectProduct(C5, D8);;
Print("C5 x D8 : |.| = ", Size(K1), "  IdGroup = ", IdGroup(K1),
      "  ", StructureDescription(K1), "\n");
Hol5 := Group((1,2,3,4,5),(2,3,5,4));;
Print("Hol(C5) : |.| = ", Size(Hol5), "  IdGroup = ", IdGroup(Hol5), "\n");
G1 := DirectProduct(D8, Hol5);;
Print("D8 x Hol(C5) : |.| = ", Size(G1), "  IdGroup = ", IdGroup(G1),
      "  ", StructureDescription(G1), "  dl = ", DerivedLength(G1), "\n");
Print("R4_WINDOW_DONE\n");
QUIT;
