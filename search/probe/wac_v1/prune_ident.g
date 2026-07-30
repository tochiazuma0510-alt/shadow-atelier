#############################################################################
## search/probe/wac_v1/prune_ident.g
##  レーン A-1: 核の奇部 A が base B = C_ell^r のどの部分加群かを名指しする。
##  m=0 の hexagon (3.3)(3.4)(c=1) を Xi-制限で解き ker chi~ の f-座標を出す。
##   (3.3)  s1 * f^-1 * s2 * f  =  f^-1 * s1 * s2
##   (3.4)  f^-1 * s2 * f * s1  =  s2 * s1 * f
##   + 全射性  <xbar, ybar^f> = P ,  charming: f in [P,P] = P = A_n
##  Xi-制限: ybar^f = alpha(ybar) (alpha in Stab(xbar)) <=> f in C_{S_n}(ybar)*alpha
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
  local Snn, Ann, aE, bE, s1, s2, xb, yb, PN, Stab, CSy, kerf, al, cc, f,
        cent, Kgrp, cyc, Bg, B, vecs, v, i, j, sums, cand, seen;
  Snn := SymmetricGroup(nn); Ann := AlternatingGroup(nn);
  aE := a1*(nn+1,nn+3); bE := b1*(nn+1,nn+3,nn+2);
  s1 := bE^-1*aE; s2 := aE*bE^2;
  xb := s1^2; yb := s2^2; PN := Group(xb,yb);
  Print("\n===== ", label, "  n=", nn, "  r=", rr,
        "  |P|=", Size(PN), "  ord(xb)=", Order(xb), " =====\n");
  Stab := Centralizer(Snn, xb);
  CSy  := Centralizer(Snn, yb);
  Print("  |Stab(xbar)| = ", Size(Stab), "   |C_{S_n}(ybar)| = ", Size(CSy), "\n");
  kerf := []; cand := 0;
  for al in Elements(Stab) do
    for cc in Elements(CSy) do
      f := cc*al;
      if SignPerm(f) = 1 then
        cand := cand + 1;
        if s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f then
          if Group(xb, yb^f) = PN then AddSet(kerf, f); fi;
        fi;
      fi;
    od;
  od;
  Print("  Xi-制限の候補数(重複込) = ", cand, "\n");
  Print("  |ker chi~| (m=0 shadow の個数) = ", Length(kerf), "\n");
  ## alpha = id 層 (f in C_P(ybar)) では E_{0,f} = id ゆえ shadow 合成 = 通常の積
  cent := Filtered(kerf, f -> yb^f = yb);
  Kgrp := Group(cent);
  Print("  うち f in C_P(ybar) : ", Length(cent),
        "   <それら> の位数 = ", Size(Kgrp), " ", StructureDescription(Kgrp),
        "   閉じている? ", Size(Kgrp) = Length(cent), "\n");
  ## base B_y
  cyc := Cycles(yb, MovedPoints(yb));
  Bg := List(cyc, c -> CycFromList(c));
  B := Group(Bg);
  Print("  ybar の巡回 = ", cyc, "\n");
  Print("  base B_y = <巡回> 位数 ", Size(B), " (= 5^", rr, ")   ybar = 対角? ",
        Product(Bg) = yb, "\n");
  Print("  A <= B_y ? ", IsSubgroup(B, Kgrp), "     ybar in A ? ", yb in Kgrp,
        "     xbar in A ? ", xb in Kgrp, "\n");
  ## 座標ベクトル
  vecs := [];
  for f in Elements(Kgrp) do
    v := [];
    for i in [1..Length(Bg)] do
      j := cyc[i][1];
      v[i] := Position(cyc[i], j^f) - 1;
    od;
    Add(vecs, v);
  od;
  Print("  A の B_y-座標ベクトル(mod 5):\n");
  for v in Set(vecs) do Print("      ", v, "    座標和 = ", Sum(v) mod 5, "\n"); od;
  sums := Set(List(vecs, v -> Sum(v) mod 5));
  Print("  座標和の集合 = ", sums, "   ==> 和ゼロ部分加群か? ", sums = [0], "\n");
  Print("  dim_F5 A = ", LogInt(Size(Kgrp),5), "    r = ", rr,
        "    r-1 = ", rr-1, "\n");
  ## ker 全体の f のうち C_P(ybar) 外のものの様子
  Print("  ker の f のうち ybar を中心化しないもの: ",
        Length(kerf) - Length(cent), " 個\n");
  return rec(kerf := kerf, cent := cent, A := Kgrp, xb := xb, yb := yb,
             B := B, Bg := Bg, cyc := cyc);
end;;

R2 := Analyse(10, ( 1, 2)( 3, 6)( 7,10), ( 2,10, 6)( 3, 5, 4)( 7, 9, 8),
              2, "W-E-A10-5x2t0");;
R3 := Analyse(15, ( 1, 4)( 5, 9)( 6,15)( 7,13)( 8,11),
              ( 1, 3, 2)( 4,10, 9)( 5, 8,15)( 6,14,13)( 7,12,11),
              3, "W-E-A15-5x3t0");;

Print("\nPRUNE_IDENT_DONE\n");
QUIT;
