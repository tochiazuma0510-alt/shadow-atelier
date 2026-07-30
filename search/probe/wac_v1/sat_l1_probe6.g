#############################################################################
## search/probe/wac_v1/sat_l1_probe6.g
##  追補用の 2 点確認:
##   (A) 定理 SURV+ : Xi(f_z) = z^{a1} (= a1*z*a1) を全 z で直接照合(4 窓)
##   (B) 三角群ゲート: Delta(2,3,5) = <A,B | A^2, B^3, (B^-1 A)^5> の位数 = 60
##       (=> ord(w)=5 の窓は <a1,b1> <= A5 ゆえ A_n (n>=6) に到達しない)
##       ついでに Delta(2,3,m), m=3..7 の有限/無限を確認
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
ChkA := function(nn, a1, b1, label)
  local Snn, aE, bE, s1, s2, xb, yb, v, Cv, z, f, al, ok, okg;
  Snn := SymmetricGroup(nn);
  aE := a1*(nn+1,nn+3); bE := b1*(nn+1,nn+3,nn+2);
  s1 := bE^-1*aE; s2 := aE*bE^2; xb := s1^2; yb := s2^2;
  v := a1*b1^-1; Cv := Centralizer(Snn, v);
  ok := true; okg := true;
  for z in Elements(Cv) do
    f := (a1^z)*a1;
    al := a1*z*a1;                       ## 予測される Xi 像
    if xb^al <> xb then okg := false; fi;
    if yb^al <> yb^f then ok := false; fi;
  od;
  Print(label, "   Xi(f_z) = z^a1 が全 z で成立? ", ok,
        "    z^a1 in Stab(xbar)? ", okg,
        "    |C_Sn(w)| = ", Size(Centralizer(Snn, b1^-1*a1)), "\n");
  return true;
end;;

Print("=== (A) SURV+ : Xi(f_z) = a1*z*a1 ===\n");
ChkA(10, ( 1, 2)( 3, 6)( 7,10), ( 2,10, 6)( 3, 5, 4)( 7, 9, 8), "A10-5x2t0");;
ChkA(15, ( 1, 4)( 5, 9)( 6,15)( 7,13)( 8,11),
     ( 1, 3, 2)( 4,10, 9)( 5, 8,15)( 6,14,13)( 7,12,11), "A15-5x3t0");;
ChkA(20, ( 1,14)( 2,15)( 3,10)( 5, 9)( 6, 7)(12,19)(13,16)(17,18),
     ( 1,13,15)( 2,14,10)( 3, 9, 4)( 5, 8, 7)(11,20,19)(12,18,16), "A20-5x4t0-C");;
ChkA(20, ( 1,15)( 3,14)( 4, 5)( 6,13)( 7,20)( 8, 9)(10,19)(11,18)(12,16),
     ( 1,14, 2)( 3,13, 5)( 6,12,20)( 7,19, 9)(10,18,15)(11,17,16), "A20-5x4t0-B");;

Print("\n=== (B) 三角群ゲート Delta(2,3,m) = <A,B | A^2,B^3,(B^-1*A)^m> ===\n");
DoTri := function(m)
  local F, G, sz;
  F := FreeGroup("A","B");
  G := F / [ F.1^2, F.2^3, (F.2^-1*F.1)^m ];
  sz := Size(G);
  Print("  m=", m, "  |Delta(2,3,m)| = ", sz,
        "   ", String(sz) <> "infinity", "\n");
  return true;
end;;
DoTri(3);; DoTri(4);; DoTri(5);; DoTri(6);; DoTri(7);;
Print("\nSAT_L1_PROBE6_DONE\n");
QUIT;
