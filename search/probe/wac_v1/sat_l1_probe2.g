#############################################################################
## search/probe/wac_v1/sat_l1_probe2.g
##  還元 {H1,H2} <=> (f*a1)^2=1 かつ (f*b1^-1)^3=1 (probe1 で確認) を用いて
##  r=4 の 2 枝(C: eps=0 / B: eps=1)の Xi(ker) を **安く** 再計算する。
##  従来の悉皆は CSy x Stab = 1.1e8。ここは alpha を
##    L1 = B_x (625)  と  L2 = Stab の 2-元 (~856)
##  に限り、内側を C_{S_n}(ybar) の偶元 (7500) に限る ==> ~1.1e7。
##  出力: A = Xi(ker) cap B_x の座標・2-部 S' のブロック置換。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
CycFromList := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;

Scan := function(nn, a1, b1, label)
  local Snn, Ann, aE, bE, s1, s2, xb, yb, PN, Stab, CSy, ev, cyc, Bg, Bx,
        L1, L2, al, c, f, hits, cnt, i, j, v, vecs, Ag, blk, bp, k, pt,
        res2, tot;
  Snn := SymmetricGroup(nn); Ann := AlternatingGroup(nn);
  aE := a1*(nn+1,nn+3); bE := b1*(nn+1,nn+3,nn+2);
  s1 := bE^-1*aE; s2 := aE*bE^2;
  xb := s1^2; yb := s2^2; PN := Group(xb,yb);
  Print("\n===== ", label, "  n=", nn, " =====\n");
  Print("  sign(a1) = ", SignPerm(a1), "   (eps=0 <=> +1)\n");
  Print("  <a1,b1> = A_n ? ", Group(a1,b1)=Ann, "   = S_n ? ", Group(a1,b1)=Snn, "\n");
  Print("  P = <xbar,ybar> = A_n ? ", PN = Ann, "\n");
  Stab := Centralizer(Snn, xb);
  CSy  := Centralizer(Snn, yb);
  Print("  |Stab| = ", Size(Stab), "   |C_Sn(ybar)| = ", Size(CSy), "\n");
  cyc := Cycles(xb, MovedPoints(xb));
  Bg := List(cyc, l -> CycFromList(l));
  Bx := Group(Bg);
  Print("  xbar cycles = ", cyc, "\n  |B_x| = ", Size(Bx),
        "   xbar = 全対角? ", Product(Bg) = xb, "\n");
  ev := Filtered(Elements(CSy), p -> SignPerm(p) = 1);
  Print("  偶な c の個数 = ", Length(ev), "\n");
  L1 := Elements(Bx);
  L2 := Filtered(Elements(Stab), p -> Order(p) in [2,4,8]);
  Print("  scan: |L1(B_x)| = ", Length(L1), "  |L2(2-元)| = ", Length(L2),
        "   総反復 = ", (Length(L1)+Length(L2))*Length(ev), "\n");
  hits := []; res2 := [];
  for al in Concatenation(L1, L2) do
    cnt := 0;
    for c in ev do
      f := c*al;
      if (f*a1)^2 = () and (f*b1^-1)^3 = () then
        if Group(xb, yb^f) = PN then cnt := cnt + 1; fi;
      fi;
    od;
    if cnt > 0 then
      if al in Bx then Add(hits, [al, cnt]); else Add(res2, [al, cnt]); fi;
    fi;
  od;
  Print("  ---- 結果 ----\n");
  Print("  B_x 内で実現された alpha の個数 |A| = ", Length(hits), "\n");
  Print("  alpha あたりの f の個数(集合) = ", Set(List(hits, h -> h[2])),
        "   (すべて 1 なら Xi 単射)\n");
  Ag := Group(List(hits, h -> h[1]));
  Print("  A は部分群? ", Size(Ag) = Length(hits), "   |<A>| = ", Size(Ag),
        "   ", StructureDescription(Ag), "\n");
  vecs := [];
  for al in List(hits, h -> h[1]) do
    v := [];
    for i in [1..Length(Bg)] do
      j := cyc[i][1];
      v[i] := Position(cyc[i], j^al) - 1;
    od;
    Add(vecs, v);
  od;
  Print("  A の B_x-座標(mod 5):\n");
  for v in Set(vecs) do Print("      ", v, "\n"); od;
  Print("  2-元で実現された alpha の個数 = ", Length(res2), "\n");
  for i in res2 do
    al := i[1];
    bp := [];
    for k in [1..Length(cyc)] do
      pt := cyc[k][1]^al;
      for j in [1..Length(cyc)] do
        if pt in cyc[j] then bp[k] := j; fi;
      od;
    od;
    Print("      ord=", Order(al), "  ブロック置換 = ", bp, "  f の個数 ", i[2], "\n");
  od;
  return true;
end;;

Scan(20, ( 1,14)( 2,15)( 3,10)( 5, 9)( 6, 7)(12,19)(13,16)(17,18),
     ( 1,13,15)( 2,14,10)( 3, 9, 4)( 5, 8, 7)(11,20,19)(12,18,16),
     "W-E-A20-5x4t0-C (eps=0)");;
Scan(20, ( 1,15)( 3,14)( 4, 5)( 6,13)( 7,20)( 8, 9)(10,19)(11,18)(12,16),
     ( 1,14, 2)( 3,13, 5)( 6,12,20)( 7,19, 9)(10,18,15)(11,17,16),
     "W-E-A20-5x4t0-B (eps=1)");;
Print("\nSAT_L1_PROBE2_DONE\n");
QUIT;
