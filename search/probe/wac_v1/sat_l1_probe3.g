#############################################################################
## search/probe/wac_v1/sat_l1_probe3.g
##  定理 SURV の機械確認:
##    v := a1*b1^-1 とおくと、z in C_{S_n}(v) ごとに f_z := (a1^z)*a1 in A_n は
##    m=0 hexagon を満たす(構成的「生き残り」)。z |-> f_z は単射。
##  検査項目:
##   (1) |C_{S_n}(v)| と cycle type / 構造 / IdGroup を測定 vs 実測 |ker chi~|
##   (2) 全 z で hexagon((f a1)^2=1, (f b1^-1)^3=1)と生成条件が通るか
##   (3) z |-> f_z が単射か・像が Sol と一致するか(小窓は Sol を悉皆で持つ)
##   (4) Xi(f_z) =: alpha_z の写像 z |-> alpha_z が(反)準同型か
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
Chk := function(nn, a1, b1, label, doFull)
  local Snn, Ann, aE, bE, s1, s2, xb, yb, PN, v, Cv, els, z, f, fs, ok1, ok2,
        Stab, CSy, al, cc, Sol, alphas, i, j, hom, anti, az, idg;
  Snn := SymmetricGroup(nn); Ann := AlternatingGroup(nn);
  aE := a1*(nn+1,nn+3); bE := b1*(nn+1,nn+3,nn+2);
  s1 := bE^-1*aE; s2 := aE*bE^2;
  xb := s1^2; yb := s2^2; PN := Group(xb,yb);
  Print("\n===== ", label, "  n=", nn, " =====\n");
  v := a1*b1^-1;
  Print("  w=b1^-1*a1 型 ", CycleStructurePerm(b1^-1*a1), " ord ", Order(b1^-1*a1),
        "\n  v=a1*b1^-1 型 ", CycleStructurePerm(v), " ord ", Order(v), "\n");
  Cv := Centralizer(Snn, v);
  Print("  |C_Sn(v)| = ", Size(Cv), "   ", StructureDescription(Cv), "\n");
  if Size(Cv) <= 2000 then
    idg := IdGroup(Cv);
    Print("  IdGroup(C_Sn(v)) = ", idg, "\n");
  fi;
  Print("  C_Sn(v) cap C_Sn(a1) = ", Size(Intersection(Cv, Centralizer(Snn,a1))),
        "  (1 なら z|->f_z は単射)\n");
  ## (2)(3) 構成
  els := Elements(Cv); fs := [];
  ok1 := true; ok2 := true;
  for z in els do
    f := (a1^z)*a1;
    if SignPerm(f) <> 1 then ok1 := false; fi;
    if not ((f*a1)^2 = () and (f*b1^-1)^3 = ()) then ok1 := false; fi;
    if not (s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f) then ok1 := false; fi;
    if Group(xb, yb^f) <> PN then ok2 := false; fi;
    Add(fs, f);
  od;
  Print("  全 z で f_z in A_n かつ hexagon(還元形・原形とも)成立? ", ok1, "\n");
  Print("  全 z で生成条件 <xbar, ybar^f> = P 成立?               ", ok2, "\n");
  Print("  相異なる f_z の個数 = ", Length(Set(fs)), " / |C_Sn(v)| = ", Size(Cv),
        "   単射? ", Length(Set(fs)) = Size(Cv), "\n");
  ## (4) Xi 像と(反)準同型性
  alphas := [];
  for i in [1..Length(els)] do
    al := RepresentativeAction(Snn, [xb,yb], [xb, yb^fs[i]], OnTuples);
    Add(alphas, al);
  od;
  Print("  alpha_z がすべて定義可能? ", not fail in alphas,
        "   相異なる alpha の個数 = ", Length(Set(alphas)), "\n");
  hom := true; anti := true;
  for i in [1..Length(els)] do
    for j in [1..Length(els)] do
      az := Position(els, els[i]*els[j]);
      if alphas[az] <> alphas[i]*alphas[j] then hom := false; fi;
      if alphas[az] <> alphas[j]*alphas[i] then anti := false; fi;
    od;
  od;
  Print("  z |-> alpha_z は準同型? ", hom, "   反準同型? ", anti, "\n");
  ## Sol との一致(小窓のみ悉皆)
  if doFull then
    Stab := Centralizer(Snn, xb); CSy := Centralizer(Snn, yb);
    Sol := [];
    for al in Elements(Stab) do
      for cc in Elements(CSy) do
        f := cc*al;
        if SignPerm(f) = 1 and (f*a1)^2 = () and (f*b1^-1)^3 = ()
           and Group(xb, yb^f) = PN then Add(Sol, f); fi;
      od;
    od;
    Print("  悉皆 Sol(= ker chi~)の個数 = ", Length(Set(Sol)),
          "   構成像と一致? ", Set(Sol) = Set(fs), "\n");
  fi;
  return true;
end;;

Chk(10, ( 1, 2)( 3, 6)( 7,10), ( 2,10, 6)( 3, 5, 4)( 7, 9, 8),
    "W-E-A10-5x2t0 (|ker|=10)", true);;
Chk(15, ( 1, 4)( 5, 9)( 6,15)( 7,13)( 8,11),
    ( 1, 3, 2)( 4,10, 9)( 5, 8,15)( 6,14,13)( 7,12,11),
    "W-E-A15-5x3t0 (|ker|=50)", true);;
Chk(20, ( 1,14)( 2,15)( 3,10)( 5, 9)( 6, 7)(12,19)(13,16)(17,18),
    ( 1,13,15)( 2,14,10)( 3, 9, 4)( 5, 8, 7)(11,20,19)(12,18,16),
    "W-E-A20-5x4t0-C eps=0 (|ker|=200)", false);;
Chk(20, ( 1,15)( 3,14)( 4, 5)( 6,13)( 7,20)( 8, 9)(10,19)(11,18)(12,16),
    ( 1,14, 2)( 3,13, 5)( 6,12,20)( 7,19, 9)(10,18,15)(11,17,16),
    "W-E-A20-5x4t0-B eps=1 (|ker|=500)", false);;
Print("\nSAT_L1_PROBE3_DONE\n");
QUIT;
