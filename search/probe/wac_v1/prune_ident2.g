#############################################################################
## search/probe/wac_v1/prune_ident2.g
##  核の奇部 A の同定は f-座標ではなく **Xi-像** で行う。
##  Xi: [m,f] -> E_{m,f} in Aut(P) = S_n.  m=0 では E_{0,f}(xbar)=xbar,
##  E_{0,f}(ybar)=ybar^f ゆえ Xi([0,f]) = alpha in Stab(xbar) = C_ell wr S_r。
##  f = c*alpha (c in C_{S_n}(ybar)) の分解は一意(C_{S_n}(P)=1)。
##  A := O_{2'}(ker chi~) の Xi-像は base B_x = C_ell^r の部分加群になるはず。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
CycFromList := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;

Analyse := function(nn, a1, b1, rr, label)
  local Snn, aE, bE, s1, s2, xb, yb, PN, Stab, CSy, al, cc, f, pairs, alphas,
        XiIm, A2, cyc, Bg, Bx, v, i, j, vecs, sums, q, Qgen, act, ok, A, S2p,
        f2, z, m, u;
  Snn := SymmetricGroup(nn);
  aE := a1*(nn+1,nn+3); bE := b1*(nn+1,nn+3,nn+2);
  s1 := bE^-1*aE; s2 := aE*bE^2;
  xb := s1^2; yb := s2^2; PN := Group(xb,yb);
  Print("\n===== ", label, "  n=", nn, "  r=", rr, " =====\n");
  Stab := Centralizer(Snn, xb);
  CSy  := Centralizer(Snn, yb);
  pairs := [];
  for al in Elements(Stab) do
    for cc in Elements(CSy) do
      f := cc*al;
      if SignPerm(f) = 1 then
        if s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f then
          if Group(xb, yb^f) = PN then Add(pairs, [f, al]); fi;
        fi;
      fi;
    od;
  od;
  Print("  |ker chi~| = ", Length(pairs), "\n");
  alphas := Set(List(pairs, p -> p[2]));
  Print("  相異なる Xi-像 alpha の個数 = ", Length(alphas),
        "   (= |ker chi~| なら ker Xi = 1)\n");
  XiIm := Group(alphas);
  Print("  Xi(ker) = <alphas> 位数 ", Size(XiIm), "  ",
        StructureDescription(XiIm),
        "   集合として閉? ", Size(XiIm) = Length(alphas), "\n");
  Print("  Xi(ker) <= Stab(xbar)(位数 ", Size(Stab), ") ? ",
        IsSubgroup(Stab, XiIm), "\n");
  ## 奇部 A
  A := SylowSubgroup(XiIm, 5);
  Print("  A := Syl_5(Xi(ker)) 位数 ", Size(A), "  ", StructureDescription(A),
        "   正規? ", IsNormal(XiIm, A), "\n");
  ## base B_x
  cyc := Cycles(xb, MovedPoints(xb));
  Bg := List(cyc, c -> CycFromList(c));
  Bx := Group(Bg);
  Print("  xbar の巡回 = ", cyc, "\n");
  Print("  base B_x 位数 ", Size(Bx), " (=5^", rr, ")   xbar = 対角? ",
        Product(Bg) = xb, "\n");
  Print("  A <= B_x ? ", IsSubgroup(Bx, A), "     xbar in A ? ", xb in A, "\n");
  vecs := [];
  for f in Elements(A) do
    v := [];
    for i in [1..Length(Bg)] do
      j := cyc[i][1];
      v[i] := Position(cyc[i], j^f) - 1;
    od;
    Add(vecs, v);
  od;
  Print("  A の B_x-座標ベクトル (mod 5):\n");
  for v in Set(vecs) do Print("      ", v, "    座標和 = ", Sum(v) mod 5, "\n"); od;
  sums := Set(List(vecs, v -> Sum(v) mod 5));
  Print("  座標和の集合 = ", sums, "   ==> 和ゼロ(augmentation)部分加群? ",
        sums = [0], "\n");
  Print("  dim_F5 A = ", LogInt(Size(A),5), "   r-1 = ", rr-1,
        "   一致? ", LogInt(Size(A),5) = rr-1, "\n");
  ## 2-部
  S2p := SylowSubgroup(XiIm, 2);
  Print("  Syl_2(Xi(ker)) 位数 ", Size(S2p), "  ", StructureDescription(S2p),
        "   生成元 ", GeneratorsOfGroup(S2p), "\n");
  Print("  Syl_2 は base の外(blocks を動かす)? ",
        not IsSubgroup(Bx, S2p), "\n");
  return rec(XiIm := XiIm, A := A, Bx := Bx, Bg := Bg, cyc := cyc, xb := xb);
end;;

R2 := Analyse(10, ( 1, 2)( 3, 6)( 7,10), ( 2,10, 6)( 3, 5, 4)( 7, 9, 8),
              2, "W-E-A10-5x2t0");;
R3 := Analyse(15, ( 1, 4)( 5, 9)( 6,15)( 7,13)( 8,11),
              ( 1, 3, 2)( 4,10, 9)( 5, 8,15)( 6,14,13)( 7,12,11),
              3, "W-E-A15-5x3t0");;

Print("\nPRUNE_IDENT2_DONE\n");
QUIT;
