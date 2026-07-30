#############################################################################
## search/probe/wac_v1/sat_l1_probe5.g
##  判別実験: A の座標パターンを決めているのは
##    (仮説 X・司令塔) S' の可換部分群の固定空間か
##    (仮説 Y・本稿)   w = b1^-1*a1 の 2ell-巡回が束ねるブロック対か
##  ==> w の各 2ell-巡回が割れてできる xbar-ブロック対を直接出力し、
##      A の「等値になる座標対」と一致するかを見る。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
Pair := function(nn, a1, b1, label)
  local aE, bE, s1, s2, xb, w, cycw, cycx, i, j, blocks, pr, l, hit;
  aE := a1*(nn+1,nn+3); bE := b1*(nn+1,nn+3,nn+2);
  s1 := bE^-1*aE; s2 := aE*bE^2; xb := s1^2;
  w := b1^-1*a1;
  cycx := Cycles(xb, MovedPoints(xb));
  cycw := Cycles(w, MovedPoints(w));
  Print("\n===== ", label, " =====\n");
  Print("  xbar blocks (この番号が A の座標): \n");
  for i in [1..Length(cycx)] do Print("    #", i, " = ", cycx[i], "\n"); od;
  Print("  w の巡回(長さつき):\n");
  for l in cycw do Print("    len ", Length(l), " : ", l, "\n"); od;
  Print("  各 w-巡回が触れる xbar-ブロック番号:\n");
  for l in cycw do
    blocks := [];
    for j in [1..Length(cycx)] do
      if ForAny(l, p -> p in cycx[j]) then Add(blocks, j); fi;
    od;
    Print("    len ", Length(l), "  -> ブロック ", blocks, "\n");
  od;
  return true;
end;;

Pair(20, ( 1,14)( 2,15)( 3,10)( 5, 9)( 6, 7)(12,19)(13,16)(17,18),
     ( 1,13,15)( 2,14,10)( 3, 9, 4)( 5, 8, 7)(11,20,19)(12,18,16),
     "C 枝 (eps=0, w=(10,10), A={(a,a,b,b)} 実測)");;
Pair(20, ( 1,15)( 3,14)( 4, 5)( 6,13)( 7,20)( 8, 9)(10,19)(11,18)(12,16),
     ( 1,14, 2)( 3,13, 5)( 6,12,20)( 7,19, 9)(10,18,15)(11,17,16),
     "B 枝 (eps=1, w=(10,5,5), A={(a,a,c,d)} 実測)");;
Pair(15, ( 1, 4)( 5, 9)( 6,15)( 7,13)( 8,11),
     ( 1, 3, 2)( 4,10, 9)( 5, 8,15)( 6,14,13)( 7,12,11),
     "r=3 窓 (w=(10,5), A={(a,a,b)} のはず)");;
Print("\nSAT_L1_PROBE5_DONE\n");
QUIT;
