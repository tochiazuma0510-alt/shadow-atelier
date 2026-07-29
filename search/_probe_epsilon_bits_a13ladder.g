#############################################################################
## search/_probe_epsilon_bits_a13ladder.g -- 裁定213 工程2 (E-1): 既存の
## search/_probe_epsilon_bits.g (+ a16/a18/a20 driver 3 本) の梯子後付け適用。
## N_ord=9 梯子の canonical 4 窓 (W-E-A10-9t1 / A11-9t2 / A12-9t3 / A13-9t4)
## 各窓・各 u-層 (u in (Z/18)^x の代表, charmingSet 由来) について、
## S = Syl_2(ker chi~) を中心化する shadow の「tilde G = G/A での持ち上げ位数」
## 分布と冪ビット P(u) := [ 同位数の持ち上げが無い ] を直接測る。
## Q = G/ker chi~ は全 4 窓とも C6 巡回 (search/certs/a13_ladder_*.json の
## 8/9 欄で既確認) なので交差ビットは測らない (P のみ)。
##
## 窓の生成対・judge preamble は search/_a13_ladder_driver_spec.md の
## canonical 4 窓欄からの逐語転記 (search/strike-a13-ladder.g の CANON 表と
## 同一)。予言ファイル docs/notes/a13_prediction_v1.md は読まない(接触遮断)。
##
## t=1 (W-E-A10-9t1) は S = Syl_2(ker) が自明 (|S|=1, 既確認)。この場合
## 「中心化」は空虚 -- コード上は CommutatorSubgroup(<g>, TrivialGroup) が
## 常に自明なので自動的に層の全 shadow が cen に入るが、出力には
## centralizer_condition_vacuous フィールドで明示する。
##
## 実行: 1 スクリプト内で 4 窓を順次処理 (状態は関数ローカルに閉じ、
## 窓間の持ち越しなし)。GAP は .\gap.ps1 経由・-o 2g 前提。
## 出力: search/certs/epsbits_a13_ladder_20260730.json (1 ファイルに 4 窓分)
#############################################################################

Read("search/gaplib_common.g");
JUDGE_LIBRARY_ONLY := true;;
JUDGE_SKIP_LEGACY_CROSSCHECK := true;;
Read("search/kerchi-judge.g");

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
## window construction (Prop 0.3, SymmetricGroup(n) realization -- identical
## to search/strike-a13-ladder.g's BuildS1S2, transcribed here to keep the
## probe self-contained and not import strike-a13-ladder.g itself).
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
  return rec(s1 := s1, s2 := s2, Dgrp := Dgrp);
end;;

# canonical 4 windows (literal transcription of search/_a13_ladder_driver_spec.md)
CANON := [
  rec(id := "W-E-A10-9t1", n := 10, t := 1,
      a1 := ( 1, 2)( 3, 5)( 4,10)( 6, 9),
      b1 := ( 2, 9, 5)( 3, 4,10)( 6, 8, 7),
      s1lit := ( 1, 2, 3, 4, 5, 6, 7, 8, 9)(11,12),
      s2lit := ( 1, 5,10, 3, 9, 7, 8, 6, 2)(12,13)),
  rec(id := "W-E-A11-9t2", n := 11, t := 2,
      a1 := ( 2,11)( 3, 8)( 4, 5)( 6, 7)( 9,10),
      b1 := ( 1, 9,11)( 2,10, 8)( 3, 7, 5),
      s1lit := ( 1, 2, 3, 4, 5, 6, 7, 8, 9)(10,11)(12,13),
      s2lit := ( 1,11, 8, 5, 4, 7, 6, 3,10)( 2, 9)(13,14)),
  rec(id := "W-E-A12-9t3", n := 12, t := 3,
      a1 := ( 3, 9)( 4,11)( 5, 7)( 6,12)( 8,10),
      b1 := ( 1, 9, 2)( 3, 8,11)( 4,10, 7)( 5, 6,12),
      s1lit := ( 1, 2, 3, 4, 5, 6, 7, 8, 9)(10,11)(13,14),
      s2lit := ( 1, 2, 9,11, 7,12, 5,10, 3)( 4, 8)(14,15)),
  rec(id := "W-E-A13-9t4", n := 13, t := 4,
      a1 := ( 2,10)( 3, 8)( 4,12)( 5, 6)( 7,13)( 9,11),
      b1 := ( 1, 9,10)( 2,11, 8)( 3, 7,12)( 4,13, 6),
      s1lit := ( 1, 2, 3, 4, 5, 6, 7, 8, 9)(10,11)(12,13)(14,15),
      s2lit := ( 1,10, 8,12, 6, 5,13, 3,11)( 2, 9)( 4, 7)(15,16)),
];;

# Xi-restricted fail-closed scan upper bound per t-family (仕様書表・逐語)
XI_BOUND_BY_T := rec( t1 := 486, t2 := 972, t3 := 8748, t4 := 139968 );;

# order of u in (Z/18)^x (Nord=9 => modulus 2*Nord=18), computed directly
# (no library shortcut assumed -- fail-closed if u not coprime to 18)
ExpOrderMod := function(u, n)
  local cur, k;
  if Gcd(u mod n, n) <> 1 then
    Error("ExpOrderMod: u=", u, " not coprime to n=", n);
  fi;
  cur := u mod n;;  k := 1;;
  while cur <> 1 do
    cur := (cur * u) mod n;;
    k := k + 1;;
  od;
  return k;
end;;

#############################################################################
## per-window epsilon-bit measurement
#############################################################################
ProcessEpsWindow := function(w)
  local built, s1, s2, W, xiBound, xiRes, corr, gi, G, K, regs, oddp, A, S,
        hom, Gt, CG, CGt, Qhom, Q, QInv, QDescr, charmingSet, layers, m, u,
        expOrd, idx, cen, ords, dist, good, Pbit, vacuous, highlight, i0,
        witness, layerRec, layerItems;

  Print("\n################################################################\n");
  Print("# eps-bits window: ", w.id, " (n=", w.n, ", t=", w.t, ")\n");
  Print("################################################################\n");

  built := BuildS1S2(w.a1, w.b1, w.n);;
  s1 := built.s1;;  s2 := built.s2;;
  if s1 <> w.s1lit or s2 <> w.s2lit then
    Error("_probe_epsilon_bits_a13ladder.g: transcription mismatch for window ",
          w.id, " -- computed s1/s2 (from a1,b1 via Prop 0.3) does not match ",
          "the literal JUDGE_S1_IMG/JUDGE_S2_IMG from the spec -- fail-closed");
  fi;

  W := MakeWindow(s1, s2);;
  if W.Nord <> 9 then
    Error("_probe_epsilon_bits_a13ladder.g: window ", w.id, ": N_ord = ",
          W.Nord, " <> 9 -- universe assumption violated, refusing to proceed");
  fi;
  charmingSet := Filtered([0 .. W.Nord - 1], m -> Gcd(2*m+1, W.Nord) = 1);;

  xiBound := XI_BOUND_BY_T.(Concatenation("t", String(w.t)));;
  JUDGE_FORCE_SCAN_MODE := "xi_restricted";;
  xiRes := CorrectedShadowsXi(W, charmingSet);;
  Print("  [Xi] window ", w.id, ": scanned_count=", xiRes.scanned_count,
        " bound=", xiBound, " shadow_total=", Length(xiRes.shadows),
        " settled_fail_count=", xiRes.settled_fail_count, "\n");
  if xiRes.scanned_count > xiBound then
    Error("_probe_epsilon_bits_a13ladder.g: window ", w.id, ": xi scanned_count (",
          xiRes.scanned_count, ") EXCEEDS the fail-closed Xi upper bound (",
          xiBound, ") -- refusing to trust this scan");
  fi;
  corr := xiRes.shadows;;

  gi := GroupOfShadows(W, corr);;
  if not gi.closed then
    Error("_probe_epsilon_bits_a13ladder.g: (3.53) closure FAILED for window ",
          w.id, " -- refusing to report structure of a group not confirmed to exist");
  fi;
  G := gi.G;;  K := gi.ker;;  regs := gi.regs;;

  oddp := Filtered(PrimeDivisors(Size(K)), p -> p <> 2);;
  if Length(oddp) > 0 then
    A := Subgroup(K, Concatenation(List(oddp, p -> GeneratorsOfGroup(SylowSubgroup(K, p)))));;
  else
    A := TrivialSubgroup(K);;
  fi;
  S := SylowSubgroup(K, 2);;
  vacuous := (Size(S) = 1);;

  hom := NaturalHomomorphismByNormalSubgroup(G, A);;   # A normal in K, K normal in G
  Gt := Image(hom);;
  CG := Centralizer(G, S);;
  CGt := Image(hom, CG);;                              # tilde G = C_G(S)/A

  Qhom := NaturalHomomorphismByNormalSubgroup(G, K);;
  Q := Image(Qhom);;
  QInv := AbelianInvariants(Q);;
  QDescr := StructureDescription(Q);;

  Print("  |K|=", Size(K), " |A|=", Size(A), " |S|=", Size(S),
        " (vacuous=", vacuous, ")\n");
  Print("  |Q|=", Size(Q), " Q_struct=", QDescr, " Q_inv=", QInv, "\n");
  Print("  |tilde G|=|C_G(S)/A|=", Size(CGt), " = ", StructureDescription(CGt),
        "   abelian? ", IsAbelian(CGt), "\n");
  if Size(Q) <> 6 or QDescr <> "C6" then
    Print("  [NOTE] Q is NOT the expected C6 for window ", w.id,
          " -- P-only measurement assumption (no cross bit) may not hold; ",
          "recording raw values anyway, no interpretation.\n");
  fi;

  layers := [];;
  layerItems := [];;
  for m in charmingSet do
    u := (2*m + 1) mod (2 * W.Nord);;
    expOrd := ExpOrderMod(u, 2 * W.Nord);;
    idx := Filtered([1 .. Length(corr)], i -> corr[i][1] = m);;
    cen := Filtered(idx, i -> IsTrivial(CommutatorSubgroup(Group(regs[i]), S)));;
    ords := List(cen, i -> Order(Image(hom, regs[i])));;
    dist := Collected(ords);;
    good := Filtered([1 .. Length(cen)], j -> ords[j] = expOrd);;
    Pbit := (Length(good) = 0);;
    highlight := (u = (2 * W.Nord - 1)) or (expOrd >= 4);;   # u=-1 (mod 18), or ord>=4 in (Z/18)^x

    Print("\n  u=", u, " (m=", m, ")  ord_{(Z/18)^x}(u)=", expOrd,
          "  highlight=", highlight, "\n");
    Print("    layer_size=", Length(idx), "  centralizing_S=", Length(cen),
          " (vacuous_condition=", vacuous, ")\n");
    Print("    tildeG lift-order distribution = ", dist, "\n");
    Print("    P(u) = ", Pbit, "  (false = same-order lift exists; same_order_lift_count=",
          Length(good), ")\n");

    witness := "null";;
    if Length(good) > 0 then
      i0 := cen[good[1]];;
      witness := Concatenation("{\"m\":", String(corr[i0][1]),
        ",\"ord_G\":", String(Order(regs[i0])), "}");;
    fi;

    layerRec := rec(u := u, m := m, ord_expected := expOrd, highlight := highlight,
                     layer_size := Length(idx), centralizing_count := Length(cen),
                     centralizer_condition_vacuous := vacuous,
                     lift_order_distribution := dist,
                     same_order_lift_count := Length(good), P_bit := Pbit,
                     witness_json := witness);;
    Add(layers, layerRec);;

    Add(layerItems, Concatenation(
      "{\"u\":", String(u), ",\"m\":", String(m),
      ",\"ord_expected\":", String(expOrd),
      ",\"highlight\":", JB(highlight),
      ",\"layer_size\":", String(Length(idx)),
      ",\"centralizing_count\":", String(Length(cen)),
      ",\"centralizer_condition_vacuous\":", JB(vacuous),
      ",\"lift_order_distribution\":", JStr(PrintStr(dist)),
      ",\"same_order_lift_count\":", String(Length(good)),
      ",\"P_bit\":", JB(Pbit),
      ",\"witness\":", witness, "}"));;
  od;;

  return rec(
    window_id := w.id, n := w.n, t := w.t,
    N_ord := W.Nord,
    xi_scanned_count := xiRes.scanned_count, xi_bound := xiBound,
    shadow_total := Length(corr), settled_fail_count := xiRes.settled_fail_count,
    K_order := Size(K), A_order := Size(A), S_order := Size(S),
    S_struct := StructureDescription(S),
    S_trivial_vacuous := vacuous,
    Q_order := Size(Q), Q_struct := QDescr, Q_invariant_factors := QInv,
    tildeG_order := Size(CGt), tildeG_struct := StructureDescription(CGt),
    tildeG_abelian := IsAbelian(CGt),
    layers := layers, layers_json := layerItems
  );;
end;;

#############################################################################
## main loop
#############################################################################
windowResults := [];;
windowJsonParts := [];;
for w in CANON do
  res := ProcessEpsWindow(w);;
  Add(windowResults, res);;
  Add(windowJsonParts, Concatenation(
    "  {\n",
    "    \"window_id\":", JStr(res.window_id), ",\n",
    "    \"n\":", String(res.n), ",\n",
    "    \"t\":", String(res.t), ",\n",
    "    \"N_ord\":", String(res.N_ord), ",\n",
    "    \"xi_scanned_count\":", String(res.xi_scanned_count), ",\n",
    "    \"xi_bound\":", String(res.xi_bound), ",\n",
    "    \"shadow_total\":", String(res.shadow_total), ",\n",
    "    \"settled_fail_count\":", String(res.settled_fail_count), ",\n",
    "    \"K_order\":", String(res.K_order), ",\n",
    "    \"A_order\":", String(res.A_order), ",\n",
    "    \"S_order\":", String(res.S_order), ",\n",
    "    \"S_struct\":", JStr(res.S_struct), ",\n",
    "    \"S_trivial_vacuous\":", JB(res.S_trivial_vacuous), ",\n",
    "    \"Q_order\":", String(res.Q_order), ",\n",
    "    \"Q_struct\":", JStr(res.Q_struct), ",\n",
    "    \"Q_invariant_factors\":", JStr(PrintStr(res.Q_invariant_factors)), ",\n",
    "    \"tildeG_order\":", String(res.tildeG_order), ",\n",
    "    \"tildeG_struct\":", JStr(res.tildeG_struct), ",\n",
    "    \"tildeG_abelian\":", JB(res.tildeG_abelian), ",\n",
    "    \"layers\":[\n      ", JoinC(res.layers_json, ",\n      "), "\n    ]\n",
    "  }"));;
od;;

outJson := Concatenation(
  "{\n",
  "  \"schema\":\"eps-bits-a13-ladder/v1\",\n",
  "  \"generated_by\":\"search/_probe_epsilon_bits_a13ladder.g\",\n",
  "  \"note\":\"裁定213 工程2 (E-1): 既存 search/_probe_epsilon_bits.g の N_ord=9 梯子 canonical 4窓への転用。測定値のみ、解釈なし。\",\n",
  "  \"windows\":[\n", JoinC(windowJsonParts, ",\n"), "\n  ]\n",
  "}\n");;
WriteFile("search/certs/epsbits_a13_ladder_20260730.json", outJson);;
Print("\nwrote search/certs/epsbits_a13_ladder_20260730.json\n");
Print("EPSBITS_A13_LADDER_DONE\n");
QUIT;
