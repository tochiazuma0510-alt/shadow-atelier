#############################################################################
## search/_probe_epsilon_bits_v2.g -- 裁定222 工程 (v2 拡張・実装担当作)
##
## _probe_epsilon_bits.g (v1) を非破壊で拡張(v1 は温存):
##   1. 交差ビット c(a_i,a_j) 欄: Q_2 = Syl_2(Q) の生成対 g_i を求め(Q が
##      アーベル・階数 = Length(AbelianInvariants(Q2)) 前提、非アーベルなら
##      fail-closed)、その C_G(S) 内 lift を層(m 値)から探索、
##      [lift_i, lift_j] の tilde G = C_G(S)/A での像が単位元か(bit 0 =
##      A 内)否か(bit 1 = z 込み、C_K(S)=A×Z(S) の Z(S) 成分)を判定。
##      Q_2 の階数 >= 2 の窓だけ非自明(現有窓では A20 のみ)。他窓は
##      vacuous と明示。
##      lift の任意性検査: 層内に複数の中心化 lift があれば別 lift でも
##      同じビットになるかを確認(2 通りの lift で同値)。
##   2. loc_diag: A16 に加え A20 でも Sigma_S の C_PN(x) との関係・
##      D|_Sigma_S の型数を測る(裁定222 残務)。
##
## 対象窓: A16(W-D-A16-11a) / A18(W-D-A18-13a) / A20(W-D-A20-15a) /
##         梯子 t=4(W-E-A13-9t4)。宇宙は指示どおりこの 4 窓に限定
##         (勝手な追加・削減はしない)。
##
## docs/notes/ の予言系(P-EPS 系)は読まない(接触遮断)。
## 出力: search/certs/epsbits_v2_20260730.json
#############################################################################
SizeScreen([4096, 0]);;
JUDGE_LIBRARY_ONLY := true;;
JUDGE_SKIP_LEGACY_CROSSCHECK := true;;
Read("search/kerchi-judge.g");
Read("search/gaplib_common.g");
Read("search/w62-windows.g");

PrintStr := function(x)
  local s, ss;
  ss := "";;
  s := OutputTextString(ss, true);;
  SetPrintFormattingStatus(s, false);;
  PrintTo(s, x);;
  CloseStream(s);;
  return ss;
end;;

#############################################################################
## 交差ビット: Q2 の生成対を層(m)から探す。候補は「その m 層の代表 shadow の
## Qhom 像」。同一 m 層の全 shadow が同一 Q 元に写ることも検査する。
#############################################################################
FindQ2GeneratingPair := function(corr, regs, Qhom, Q2, Nord)
  local m, idx, qimgSet, qimg, candList, c1, c2, found, g1c, g2c;
  candList := [];;
  for m in [0 .. Nord - 1] do
    idx := Filtered([1 .. Length(corr)], i -> corr[i][1] = m);;
    if Length(idx) = 0 then continue; fi;
    qimgSet := Set(List(idx, i -> Image(Qhom, regs[i])));;
    if Length(qimgSet) <> 1 then
      Error("FindQ2GeneratingPair: m=", m, " 層が単一の Q 元に写らない ",
            "(", Length(qimgSet), " 種) -- fail-closed");
    fi;
    qimg := qimgSet[1];;
    if qimg in Q2 then
      Add(candList, rec(m := m, qimg := qimg, ord := Order(qimg)));;
    fi;
  od;
  found := false;;
  g1c := fail;;  g2c := fail;;
  for c1 in candList do
    for c2 in candList do
      if c1.m <> c2.m and Size(Subgroup(Q2, [c1.qimg, c2.qimg])) = Size(Q2) then
        g1c := c1;;  g2c := c2;;  found := true;;  break;;
      fi;
    od;
    if found then break; fi;
  od;
  if not found then
    Error("FindQ2GeneratingPair: Q2 を生成する m-層の対が見つからない -- fail-closed");
  fi;
  return rec(g1 := g1c, g2 := g2c, cand_count := Length(candList));;
end;;

#############################################################################
## 交差ビット本体: g1,g2 の層から C_G(S) 内 lift を探し、コミュテータの
## tilde G = C_G(S)/A での像を判定。複数 lift があれば任意性検査も行う。
#############################################################################
MeasureCrossBit := function(corr, regs, S, hom, pair)
  local idx1, idx2, cen1, cen2, lift1a, lift2a, primComm, primImg, primBit,
        altBits, ZS, zNontrivial, zt, zCheck, liftInvariant, b, cenIdxToM;
  idx1 := Filtered([1 .. Length(corr)], i -> corr[i][1] = pair.g1.m);;
  idx2 := Filtered([1 .. Length(corr)], i -> corr[i][1] = pair.g2.m);;
  cen1 := Filtered(idx1, i -> IsTrivial(CommutatorSubgroup(Group(regs[i]), S)));;
  cen2 := Filtered(idx2, i -> IsTrivial(CommutatorSubgroup(Group(regs[i]), S)));;
  if Length(cen1) = 0 or Length(cen2) = 0 then
    Error("MeasureCrossBit: Q2 生成子の層に S を中心化する shadow がない ",
          "-- 交差ビット測定不能 -- fail-closed");
  fi;
  lift1a := regs[cen1[1]];;  lift2a := regs[cen2[1]];;
  primComm := Comm(lift1a, lift2a);;
  primImg := Image(hom, primComm);;
  primBit := not IsOne(primImg);;

  altBits := [];;
  if Length(cen1) >= 2 then
    b := not IsOne(Image(hom, Comm(regs[cen1[2]], lift2a)));;
    Add(altBits, rec(which := "g1_alt_lift", bit := b, matches_primary := (b = primBit)));;
  fi;
  if Length(cen2) >= 2 then
    b := not IsOne(Image(hom, Comm(lift1a, regs[cen2[2]])));;
    Add(altBits, rec(which := "g2_alt_lift", bit := b, matches_primary := (b = primBit)));;
  fi;
  if Length(altBits) = 0 then
    liftInvariant := "untested (each Q2-generator layer has only 1 centralizing lift)";;
  else
    liftInvariant := ForAll(altBits, r -> r.matches_primary);;
  fi;

  ZS := Center(S);;
  zNontrivial := Filtered(GeneratorsOfGroup(ZS), z -> not IsOne(z));;
  if Length(zNontrivial) = 0 and Size(ZS) > 1 then
    zNontrivial := Filtered(Elements(ZS), z -> not IsOne(z));;
  fi;
  if Size(ZS) = 2 and Length(zNontrivial) >= 1 then
    zt := Image(hom, zNontrivial[1]);;
    zCheck := rec(ZS_order := Size(ZS),
      z_image_trivial := IsOne(zt),
      bit1_equals_z := (primBit and primImg = zt),
      consistent := (not primBit) or (primImg = zt));;
  else
    zCheck := rec(ZS_order := Size(ZS), note := "|Z(S)| <> 2 -- z-identification skipped, raw bit only");;
  fi;

  return rec(
    g1_m := pair.g1.m, g1_ord := pair.g1.ord,
    g2_m := pair.g2.m, g2_ord := pair.g2.ord,
    cand_layer_count := pair.cand_count,
    layer1_size := Length(idx1), layer1_centralizing := Length(cen1),
    layer2_size := Length(idx2), layer2_centralizing := Length(cen2),
    primary_bit := primBit,
    alt_lift_checks := altBits,
    lift_invariant := liftInvariant,
    z_check := zCheck
  );;
end;;

#############################################################################
## loc_diag (裁定222 残務: A16 で測った量を A20 でも測る)
#############################################################################
ProcessLocDiag := function(wspec, corr, regs, W, G, K)
  local S, ZS, Sidx, SigS, Zidx, SigZ, cx, cy, perm, permObj, Nord, mneg,
        negIdx, Dmaps, i, f, u, Th, thetaFixesZS;
  S := SylowSubgroup(K, 2);;  ZS := Centre(S);;
  Sidx := Filtered([1 .. Length(corr)], i -> regs[i] in S);;
  SigS := List(Sidx, i -> corr[i][2]);;
  Zidx := Filtered([1 .. Length(corr)], i -> regs[i] in ZS);;
  SigZ := List(Zidx, i -> corr[i][2]);;
  cx := Filtered(SigS, s -> s * W.x = W.x * s);;
  cy := Filtered(SigS, s -> s * W.y = W.y * s);;
  thetaFixesZS := ForAll(SigZ, s -> TH(W, s) = s);;
  perm := List(SigS, s -> Position(SigS, TH(W, s)));;
  permObj := PermList(perm);;
  Nord := W.Nord;;  mneg := ((-1 - 1) / 2) mod Nord;;
  negIdx := Filtered([1 .. Length(corr)], i -> corr[i][1] = mneg
             and IsTrivial(CommutatorSubgroup(Group(regs[i]), S)));;
  Dmaps := [];;
  for i in negIdx do
    f := corr[i][2];  u := 2 * corr[i][1] + 1;
    Th := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y],
            [W.x^u, AbstractProd([f^-1, W.y^u, f])]);
    Add(Dmaps, List(SigS, s -> Position(SigS, Image(Th, TH(W, s)))));
  od;
  return rec(
    window_id := wspec.id, N_ord := Nord,
    S_struct := StructureDescription(S), ZS_order := Size(ZS),
    SigS_size := Length(SigS),
    SigS_centralizing_x := Length(cx),
    SigS_leq_CPNx := (Length(cx) = Length(SigS)),
    SigS_centralizing_y := Length(cy),
    SigZ_size := Length(SigZ),
    theta_fixes_ZS := thetaFixesZS,
    theta_perm_on_SigS_str := PrintStr(permObj),
    theta_perm_order := Order(permObj),
    uneg1_centralizing_count := Length(negIdx),
    D_restricted_distinct_types := Length(Set(Dmaps))
  );;
end;;

#############################################################################
## W62 系窓 (A16/A18/A20) の一括処理: P bit + 交差ビット + loc_diag
#############################################################################
ProcessW62Window := function(wspec, epsMS, doLocDiag)
  local corr, gi, G, K, regs, Nord, S, oddp, A, hom, Gt, CG, CGt,
        Qhom, Qgrp, Q2, invs, rank, vacuous, items, spec, m, expOrd, u, idx,
        cen, ords, good, i0, pair, crossRec, locRec, item;
  Read(Concatenation("search/certs/.w62_shadows_", wspec.id, ".g"));
  W := W62_MakeW(wspec);;
  corr := Set(List(W62_SHADOWS, s -> [s[1], s[2]]));;
  gi := GroupOfShadows(W, corr);;
  if not gi.closed then
    Error("ProcessW62Window: (3.53) closure FAILED for ", wspec.id, " -- fail-closed");
  fi;
  G := gi.G;;  K := gi.ker;;  regs := gi.regs;;
  Nord := W.Nord;;
  S := SylowSubgroup(K, 2);;
  oddp := Filtered(PrimeDivisors(Size(K)), p -> p <> 2);;
  if Length(oddp) > 0 then
    A := Subgroup(K, Concatenation(List(oddp, p -> GeneratorsOfGroup(SylowSubgroup(K, p)))));;
  else
    A := TrivialSubgroup(K);;
  fi;
  hom := NaturalHomomorphismByNormalSubgroup(G, A);;
  Gt := Image(hom);;
  CG := Centralizer(G, S);;
  CGt := Image(hom, CG);;

  Qhom := NaturalHomomorphismByNormalSubgroup(G, K);;
  Qgrp := Image(Qhom);;
  if not IsAbelian(Qgrp) then
    Error("ProcessW62Window: ", wspec.id, ": Q は非アーベル -- 前提(Q アーベル)違反 -- fail-closed");
  fi;
  Q2 := SylowSubgroup(Qgrp, 2);;
  invs := AbelianInvariants(Q2);;
  rank := Length(invs);;
  vacuous := (rank < 2);;

  # ---- P bits ----
  items := [];;
  for spec in epsMS do
    m := spec[1];  expOrd := spec[2];
    u := (2 * m + 1) mod (2 * Nord);
    idx := Filtered([1 .. Length(corr)], i -> corr[i][1] = m);;
    cen := Filtered(idx, i -> IsTrivial(CommutatorSubgroup(Group(regs[i]), S)));;
    ords := List(cen, i -> Order(Image(hom, regs[i])));;
    good := Filtered([1 .. Length(cen)], j -> ords[j] = expOrd);;
    Add(items, rec(u := u, m := m, ord_Q_expected := expOrd,
      layer_size := Length(idx), centralizing := Length(cen),
      lift_order_distribution := PrintStr(Collected(ords)),
      same_order_lift_count := Length(good), P_bit := (Length(good) = 0)));;
  od;

  # ---- cross bit ----
  crossRec := rec(Q2_struct := StructureDescription(Q2), Q2_invariant_factors := invs,
    Q2_rank := rank, vacuous := vacuous);;
  if not vacuous then
    pair := FindQ2GeneratingPair(corr, regs, Qhom, Q2, Nord);;
    crossRec := ShallowCopy(crossRec);;
    crossRec.measurement := MeasureCrossBit(corr, regs, S, hom, pair);;
  else
    crossRec.reason := "Q2 の階数 < 2 (Syl_2(Q) が巡回) -- 交差ビットは構造上非自明にならない";;
  fi;

  # ---- loc_diag (A16, A20 のみ呼び出し側で指定) ----
  locRec := fail;;
  if doLocDiag then
    locRec := ProcessLocDiag(wspec, corr, regs, W, G, K);;
  fi;

  Print("\n=== ", wspec.id, ": |tilde G|=", Size(CGt), "=", StructureDescription(CGt),
        "  |Q|=", Size(Qgrp), " Q_struct=", StructureDescription(Qgrp),
        "  Q2_struct=", StructureDescription(Q2), " vacuous=", vacuous, " ===\n");
  for item in items do
    Print("  u=", item.u, " m=", item.m, " ord_Q=", item.ord_Q_expected,
          " P_bit=", item.P_bit, " (same_order_lifts=", item.same_order_lift_count, ")\n");
  od;
  if not vacuous then
    Print("  cross-bit: g1(m=", crossRec.measurement.g1_m, ",ord=", crossRec.measurement.g1_ord,
          ") g2(m=", crossRec.measurement.g2_m, ",ord=", crossRec.measurement.g2_ord,
          ")  primary_bit=", crossRec.measurement.primary_bit,
          "  lift_invariant=", crossRec.measurement.lift_invariant, "\n");
  fi;
  if locRec <> fail then
    Print("  loc_diag: |Sigma_S|=", locRec.SigS_size, " centralizing_x=", locRec.SigS_centralizing_x,
          " SigS<=C_PN(x)? ", locRec.SigS_leq_CPNx,
          "  D|SigS distinct types=", locRec.D_restricted_distinct_types, "\n");
  fi;

  return rec(window_id := wspec.id, N_ord := Nord,
    tildeG_order := Size(CGt), tildeG_struct := StructureDescription(CGt),
    Q_order := Size(Qgrp), Q_struct := StructureDescription(Qgrp),
    K_struct := StructureDescription(K),
    P_items := items, cross := crossRec, loc_diag := locRec);;
end;;

#############################################################################
## 梯子 t=4 (W-E-A13-9t4): 自己完結窓構築 (search/_probe_epsilon_bits_a13ladder.g
## の t=4 分のみを転用・同一パターン)
#############################################################################
BuildS1S2 := function(a1, b1, n)
  local Sn, S3, Dgrp, embA, embS, agen, bgen, s1, s2;
  Sn := SymmetricGroup(n);;  S3 := SymmetricGroup(3);;
  Dgrp := DirectProduct(Sn, S3);;
  embA := Embedding(Dgrp, 1);;  embS := Embedding(Dgrp, 2);;
  agen := Image(embA, a1) * Image(embS, (1,3));;
  bgen := Image(embA, b1) * Image(embS, (1,3,2));;
  s1 := bgen^-1 * agen;;
  s2 := agen^-1 * bgen^2;;
  return rec(s1 := s1, s2 := s2, Dgrp := Dgrp);;
end;;

CANON_T4 := rec(id := "W-E-A13-9t4", n := 13, t := 4,
    a1 := ( 2,10)( 3, 8)( 4,12)( 5, 6)( 7,13)( 9,11),
    b1 := ( 1, 9,10)( 2,11, 8)( 3, 7,12)( 4,13, 6),
    s1lit := ( 1, 2, 3, 4, 5, 6, 7, 8, 9)(10,11)(12,13)(14,15),
    s2lit := ( 1,10, 8,12, 6, 5,13, 3,11)( 2, 9)( 4, 7)(15,16));;
XI_BOUND_T4 := 139968;;

ProcessLadderT4 := function()
  local built, s1, s2, W, xiRes, corr, gi, G, K, regs, Nord, S, oddp, A, hom,
        CG, CGt, Qhom, Qgrp, Q2, invs, rank, vacuous, charmingSet, items,
        m, u, idx, expOrd, cen, ords, good, crossRec, item;
  built := BuildS1S2(CANON_T4.a1, CANON_T4.b1, CANON_T4.n);;
  s1 := built.s1;;  s2 := built.s2;;
  if s1 <> CANON_T4.s1lit or s2 <> CANON_T4.s2lit then
    Error("ProcessLadderT4: transcription mismatch -- fail-closed");
  fi;
  W := MakeWindow(s1, s2);;
  if W.Nord <> 9 then
    Error("ProcessLadderT4: N_ord = ", W.Nord, " <> 9 -- universe assumption violated");
  fi;
  charmingSet := Filtered([0 .. W.Nord - 1], m -> Gcd(2 * m + 1, W.Nord) = 1);;
  JUDGE_FORCE_SCAN_MODE := "xi_restricted";;
  xiRes := CorrectedShadowsXi(W, charmingSet);;
  Print("  [Xi] ladder t4: scanned_count=", xiRes.scanned_count, " bound=", XI_BOUND_T4,
        " shadow_total=", Length(xiRes.shadows), "\n");
  if xiRes.scanned_count > XI_BOUND_T4 then
    Error("ProcessLadderT4: xi scanned_count exceeds bound -- fail-closed");
  fi;
  corr := xiRes.shadows;;
  gi := GroupOfShadows(W, corr);;
  if not gi.closed then
    Error("ProcessLadderT4: (3.53) closure FAILED -- fail-closed");
  fi;
  G := gi.G;;  K := gi.ker;;  regs := gi.regs;;  Nord := W.Nord;;
  S := SylowSubgroup(K, 2);;
  oddp := Filtered(PrimeDivisors(Size(K)), p -> p <> 2);;
  if Length(oddp) > 0 then
    A := Subgroup(K, Concatenation(List(oddp, p -> GeneratorsOfGroup(SylowSubgroup(K, p)))));;
  else
    A := TrivialSubgroup(K);;
  fi;
  hom := NaturalHomomorphismByNormalSubgroup(G, A);;
  CG := Centralizer(G, S);;
  CGt := Image(hom, CG);;

  Qhom := NaturalHomomorphismByNormalSubgroup(G, K);;
  Qgrp := Image(Qhom);;
  if not IsAbelian(Qgrp) then
    Error("ProcessLadderT4: Q は非アーベル -- 前提違反 -- fail-closed");
  fi;
  Q2 := SylowSubgroup(Qgrp, 2);;
  invs := AbelianInvariants(Q2);;
  rank := Length(invs);;
  vacuous := (rank < 2);;

  items := [];;
  for m in charmingSet do
    idx := Filtered([1 .. Length(corr)], i -> corr[i][1] = m);;
    if Length(idx) = 0 then continue; fi;
    u := (2 * m + 1) mod (2 * Nord);;
    expOrd := Order(Image(Qhom, regs[idx[1]]));;
    cen := Filtered(idx, i -> IsTrivial(CommutatorSubgroup(Group(regs[i]), S)));;
    ords := List(cen, i -> Order(Image(hom, regs[i])));;
    good := Filtered([1 .. Length(cen)], j -> ords[j] = expOrd);;
    Add(items, rec(u := u, m := m, ord_Q_expected := expOrd,
      layer_size := Length(idx), centralizing := Length(cen),
      lift_order_distribution := PrintStr(Collected(ords)),
      same_order_lift_count := Length(good), P_bit := (Length(good) = 0)));;
  od;

  crossRec := rec(Q2_struct := StructureDescription(Q2), Q2_invariant_factors := invs,
    Q2_rank := rank, vacuous := vacuous);;
  if not vacuous then
    crossRec.measurement := MeasureCrossBit(corr, regs, S, hom,
      FindQ2GeneratingPair(corr, regs, Qhom, Q2, Nord));;
  else
    crossRec.reason := "Q2 の階数 < 2 (Syl_2(Q) が巡回) -- 交差ビットは構造上非自明にならない";;
  fi;

  Print("\n=== ", CANON_T4.id, ": |tilde G|=", Size(CGt), "=", StructureDescription(CGt),
        "  |Q|=", Size(Qgrp), " Q_struct=", StructureDescription(Qgrp),
        "  Q2_struct=", StructureDescription(Q2), " vacuous=", vacuous, " ===\n");
  for item in items do
    Print("  u=", item.u, " m=", item.m, " ord_Q=", item.ord_Q_expected,
          " P_bit=", item.P_bit, " (same_order_lifts=", item.same_order_lift_count, ")\n");
  od;

  return rec(window_id := CANON_T4.id, n := CANON_T4.n, t := CANON_T4.t, N_ord := Nord,
    xi_scanned_count := xiRes.scanned_count, xi_bound := XI_BOUND_T4,
    tildeG_order := Size(CGt), tildeG_struct := StructureDescription(CGt),
    Q_order := Size(Qgrp), Q_struct := StructureDescription(Qgrp),
    K_struct := StructureDescription(K),
    P_items := items, cross := crossRec, loc_diag := fail);;
end;;

#############################################################################
## JSON 化ヘルパ
#############################################################################
JPItem := function(it)
  return Concatenation("{\"u\":", String(it.u), ",\"m\":", String(it.m),
    ",\"ord_Q_expected\":", String(it.ord_Q_expected),
    ",\"layer_size\":", String(it.layer_size),
    ",\"centralizing\":", String(it.centralizing),
    ",\"lift_order_distribution\":", JStr(it.lift_order_distribution),
    ",\"same_order_lift_count\":", String(it.same_order_lift_count),
    ",\"P_bit\":", JB(it.P_bit), "}");;
end;;

JAltBit := function(r)
  return Concatenation("{\"which\":", JStr(r.which), ",\"bit\":", JB(r.bit),
    ",\"matches_primary\":", JB(r.matches_primary), "}");;
end;;

JLiftInvariant := function(v)
  if v = true or v = false then return JB(v); fi;
  return JStr(String(v));;
end;;

JZCheck := function(z)
  if IsBound(z.note) then
    return Concatenation("{\"ZS_order\":", String(z.ZS_order), ",\"note\":", JStr(z.note), "}");;
  fi;
  return Concatenation("{\"ZS_order\":", String(z.ZS_order),
    ",\"z_image_trivial\":", JB(z.z_image_trivial),
    ",\"bit1_equals_z\":", JB(z.bit1_equals_z),
    ",\"consistent\":", JB(z.consistent), "}");;
end;;

JCross := function(c)
  local base, m;
  base := Concatenation("{\"Q2_struct\":", JStr(c.Q2_struct),
    ",\"Q2_invariant_factors\":", JStr(PrintStr(c.Q2_invariant_factors)),
    ",\"Q2_rank\":", String(c.Q2_rank),
    ",\"vacuous\":", JB(c.vacuous));;
  if c.vacuous then
    return Concatenation(base, ",\"reason\":", JStr(c.reason), "}");;
  fi;
  m := c.measurement;;
  return Concatenation(base,
    ",\"measurement\":{",
    "\"g1_m\":", String(m.g1_m), ",\"g1_ord\":", String(m.g1_ord),
    ",\"g2_m\":", String(m.g2_m), ",\"g2_ord\":", String(m.g2_ord),
    ",\"cand_layer_count\":", String(m.cand_layer_count),
    ",\"layer1_size\":", String(m.layer1_size), ",\"layer1_centralizing\":", String(m.layer1_centralizing),
    ",\"layer2_size\":", String(m.layer2_size), ",\"layer2_centralizing\":", String(m.layer2_centralizing),
    ",\"primary_bit\":", JB(m.primary_bit),
    ",\"alt_lift_checks\":[", JoinC(List(m.alt_lift_checks, JAltBit), ","), "]",
    ",\"lift_invariant\":", JLiftInvariant(m.lift_invariant),
    ",\"z_check\":", JZCheck(m.z_check),
    "}}");;
end;;

JLocDiag := function(l)
  if l = fail then return "null"; fi;
  return Concatenation("{\"window_id\":", JStr(l.window_id), ",\"N_ord\":", String(l.N_ord),
    ",\"S_struct\":", JStr(l.S_struct), ",\"ZS_order\":", String(l.ZS_order),
    ",\"SigS_size\":", String(l.SigS_size),
    ",\"SigS_centralizing_x\":", String(l.SigS_centralizing_x),
    ",\"SigS_leq_CPNx\":", JB(l.SigS_leq_CPNx),
    ",\"SigS_centralizing_y\":", String(l.SigS_centralizing_y),
    ",\"SigZ_size\":", String(l.SigZ_size),
    ",\"theta_fixes_ZS\":", JB(l.theta_fixes_ZS),
    ",\"theta_perm_on_SigS\":", JStr(l.theta_perm_on_SigS_str),
    ",\"theta_perm_order\":", String(l.theta_perm_order),
    ",\"uneg1_centralizing_count\":", String(l.uneg1_centralizing_count),
    ",\"D_restricted_distinct_types\":", String(l.D_restricted_distinct_types), "}");;
end;;

JWindow := function(r)
  return Concatenation("{\"window_id\":", JStr(r.window_id),
    ",\"N_ord\":", String(r.N_ord),
    ",\"tildeG_order\":", String(r.tildeG_order), ",\"tildeG_struct\":", JStr(r.tildeG_struct),
    ",\"Q_order\":", String(r.Q_order), ",\"Q_struct\":", JStr(r.Q_struct),
    ",\"K_struct\":", JStr(r.K_struct),
    ",\"P_items\":[", JoinC(List(r.P_items, JPItem), ","), "]",
    ",\"cross_bit\":", JCross(r.cross),
    ",\"loc_diag\":", JLocDiag(r.loc_diag), "}");;
end;;

#############################################################################
## メイン: 4 窓を順に処理
#############################################################################
w16 := First(W62_WINDOWS, w -> w.id = "W-D-A16-11a");;
w18 := First(W62_WINDOWS, w -> w.id = "W-D-A18-13a");;
w20 := First(W62_WINDOWS, w -> w.id = "W-D-A20-15a");;

res16 := ProcessW62Window(w16, [ [10, 2] ], true);;
res18 := ProcessW62Window(w18, [ [2, 4], [12, 2] ], false);;
res20 := ProcessW62Window(w20, [ [3, 4], [5, 2], [14, 2] ], true);;
resT4 := ProcessLadderT4();;

outJson := Concatenation(
  "{\n",
  "  \"schema\":\"eps-bits-v2/1\",\n",
  "  \"generated_by\":\"search/_probe_epsilon_bits_v2.g\",\n",
  "  \"note\":\"裁定222工程: 交差ビット欄(Q2不変因子基底lift+lift任意性検査)とA16/A20 loc_diagの追加測定。測定値のみ、解釈なし。v1(_probe_epsilon_bits.g)は非上書き。\",\n",
  "  \"windows\":[\n    ", JWindow(res16), ",\n    ", JWindow(res18), ",\n    ",
  JWindow(res20), ",\n    ", JWindow(resT4), "\n  ]\n",
  "}\n");;
WriteFile("search/certs/epsbits_v2_20260730.json", outJson);;
Print("\nwrote search/certs/epsbits_v2_20260730.json\n");
Print("EPSBITS_V2_DONE\n");
QUIT;
