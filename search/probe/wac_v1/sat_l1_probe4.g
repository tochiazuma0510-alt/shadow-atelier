#############################################################################
## search/probe/wac_v1/sat_l1_probe4.g
##  定理 SURV / 予想 SAT-ORD の全 9 窓一斉検査(norm_embedding_20260731 と同一窓)。
##  予測: |ker chi~| = |C_{S_n}(v)|,  v := a1*b1^-1  (~ w = b1^-1*a1)
##  各窓で: |C_Sn(v)|・構造・全 z で hexagon+生成 が通るか・単射か を出す。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
Chk := function(nn, a1, b1, label, kerCert)
  local Snn, aE, bE, s1, s2, xb, yb, PN, v, Cv, z, f, fs, ok1, ok2;
  Snn := SymmetricGroup(nn);
  aE := a1*(nn+1,nn+3); bE := b1*(nn+1,nn+3,nn+2);
  s1 := bE^-1*aE; s2 := aE*bE^2;
  xb := s1^2; yb := s2^2; PN := Group(xb,yb);
  v := a1*b1^-1;
  Cv := Centralizer(Snn, v);
  fs := []; ok1 := true; ok2 := true;
  for z in Elements(Cv) do
    f := (a1^z)*a1;
    if SignPerm(f) <> 1 then ok1 := false; fi;
    if not (s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f) then ok1 := false; fi;
    if Group(xb, yb^f) <> PN then ok2 := false; fi;
    Add(fs, f);
  od;
  Print(label, "  n=", nn,
        "\n    v type ", CycleStructurePerm(v), " ord ", Order(v),
        "   sign(a1)=", SignPerm(a1),
        "\n    |C_Sn(v)| = ", Size(Cv), "   実測 |ker| = ", kerCert,
        "   一致? ", Size(Cv) = kerCert,
        "\n    構造 ", StructureDescription(Cv),
        "\n    全 z: hexagon ", ok1, "  生成 ", ok2,
        "  相異なる f_z ", Length(Set(fs)), " (単射? ", Length(Set(fs))=Size(Cv), ")\n");
  return true;
end;;

Chk(10, ( 1, 2)( 3, 5)( 4,10)( 6, 9), ( 2, 9, 5)( 3, 4,10)( 6, 8, 7),
    "W-E-A10-9t1 ", 9);;
Chk(11, ( 2,11)( 3, 8)( 4, 5)( 6, 7)( 9,10), ( 1, 9,11)( 2,10, 8)( 3, 7, 5),
    "W-E-A11-9t2 ", 18);;
Chk(12, ( 3, 9)( 4,11)( 5, 7)( 6,12)( 8,10),
    ( 1, 9, 2)( 3, 8,11)( 4,10, 7)( 5, 6,12), "W-E-A12-9t3 ", 18);;
Chk(13, ( 2,10)( 3, 8)( 4,12)( 5, 6)( 7,13)( 9,11),
    ( 1, 9,10)( 2,11, 8)( 3, 7,12)( 4,13, 6), "W-E-A13-9t4 ", 72);;
Chk(10, ( 1, 2)( 3, 6)( 7,10), ( 2,10, 6)( 3, 5, 4)( 7, 9, 8),
    "W-E-A10-5x2t0 ", 10);;
Chk(15, ( 1, 4)( 5, 9)( 6,15)( 7,13)( 8,11),
    ( 1, 3, 2)( 4,10, 9)( 5, 8,15)( 6,14,13)( 7,12,11), "W-E-A15-5x3t0 ", 50);;
Chk(16, ( 1, 2)( 3,14)( 4,10)( 5,12)( 6, 8)( 7,16)( 9,13)(11,15),
    ( 2,11,14)( 3,15,10)( 4, 9,12)( 5,13, 8)( 6, 7,16), "W-D-A16-11a ", 88);;
Chk(18, ( 1,17)( 2, 6)( 3,14)( 5,15)( 7,16)( 8,13)(10,12)(11,18),
    ( 1,16, 6)( 2, 5,14)( 3,15, 4)( 7,17,13)( 8,12, 9)(10,11,18),
    "W-D-A18-13a ", 104);;
Chk(20, ( 1, 7)( 2,16)( 3, 5)( 4,20)( 6,17)( 8, 9)(10,15)(11,19)(12,13)(14,18),
    ( 1, 6,16)( 2,17, 5)( 3, 4,20)( 7,15, 9)(10,14,19)(11,18,13),
    "W-D-A20-15a ", 120);;
Print("\nSAT_L1_PROBE4_DONE\n");
QUIT;
