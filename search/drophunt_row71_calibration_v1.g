#############################################################################
## drophunt_row71_calibration_v1.g -- item 3 (裁定1761): row71/row36 as
## FULL GT(M) members, checked DIRECTLY in the roof M itself (m=0, no joint
## window), via the corrected predicate (Wd:=f*y^m, LHS=Wd*tau~(Wd)*tau~^2(Wd)).
## row71 is the calibration gate (B-2: must PASS, frozen "row71 is a full
## shadow of M" value) -- if it fails, that is an immediate bug stop.
## row36 (g*) is the negative/insensitivity control (B-4).
#############################################################################

Read("search/drophunt_checker_producer_v3.g");;

DR7T0 := GAPLIB_WallElapsedMs();;

## M-level A: since c is in M (framework assumption, DCP3CinMGrounding),
## JC_M = Identity(DCP3MBlock). theta~_M, tau~_M built via the SAME closed
## forms, needing only MX,MY,Identity -- no sigma1/sigma2 of M required.
DR7AM := DCP3MBlock;;   # = Group(MX,MY); since JC_M=Identity, A_M = G_M
DR7ThetaM := GroupHomomorphismByImages(DR7AM, DR7AM, [DCP3MX,DCP3MY], [DCP3MY,DCP3MX]);;
DR7TauM := GroupHomomorphismByImages(DR7AM, DR7AM, [DCP3MX,DCP3MY], [DCP3MY, DCP3MY^-1*DCP3MX^-1]);;
Print("DR7_M_LEVEL theta_wd=", DR7ThetaM<>fail, " tau_wd=", DR7TauM<>fail, "\n");;
if DR7ThetaM = fail or DR7TauM = fail then Error("DR7: M-level theta~/tau~ ill-defined -- fail-closed"); fi;;

DR7DerivedM := DerivedSubgroup(DR7AM);;
Print("DR7_DERIVED_M_ORDER=", Size(DR7DerivedM), "\n");;

DR7CheckSeedInM := function(seed, label)
  local f, m, u, okCm, okCf, charming, hex310, ymf, lhs, rhs, hex311,
    genA, genB, onto, verdict, stage;
  f := DCP3EvalWord(seed.letters, DCP3MX, DCP3MY, Identity(DR7AM));;
  m := seed.m_seed;;
  u := 2*m+1;;
  okCm := Gcd(u, 18) = 1;;
  okCf := f in DR7DerivedM;;
  charming := okCm and okCf;;
  stage := "charming_fail";; hex310:=fail;; hex311:=fail;; onto:=fail;;
  if charming then
    hex310 := (f * Image(DR7ThetaM, f) = Identity(DR7AM));;
    if hex310 then
      ymf := DCP3MY^m * f;;   # Wd := y^m*f, product_order="tau2_tau_id" (naive), matches producer
      lhs := Image(DR7TauM, Image(DR7TauM, ymf)) * Image(DR7TauM, ymf) * ymf;;
      rhs := Identity(DR7AM)^m;;   # c^m = Identity always (c in M)
      hex311 := (lhs = rhs);;
      if hex311 then
        genA := DCP3MX^u;; genB := f^-1 * DCP3MY^u * f;;
        onto := Size(Group(genA,genB)) = Size(DR7AM);;
        if onto then stage := "pass"; else stage := "onto_fail"; fi;;
      else stage := "hex311_fail"; fi;;
    else stage := "hex310_fail"; fi;;
  fi;;
  verdict := charming and hex310=true and hex311=true and onto=true;;
  Print("DR7_SEED_IN_M label=", label, " m=", m, " okCm=", okCm, " okCf=", okCf,
    " charming=", charming, " hex310=", hex310, " hex311=", hex311, " onto=", onto,
    " stage=", stage, " verdict(=full_GT_M_member)=", verdict, "\n");;
  return rec(label:=label, charming:=charming, hex310:=hex310, hex311:=hex311,
    onto:=onto, stage:=stage, verdict:=verdict);;
end;;

DR7Row36 := DR7CheckSeedInM(DCP3Seeds[1], "row36");;
DR7Row71 := DR7CheckSeedInM(DCP3Seeds[2], "row71");;

Print("DR7_B2_GATE row71_full_M_shadow(must_be_true)=", DR7Row71.verdict, "\n");;
if not DR7Row71.verdict then
  Print("DR7_B2_GATE_FAILED -- IMMEDIATE BUG STOP PER 裁定1761 CALIBRATION GATE\n");;
fi;;

DR7TotalElapsed := GAPLIB_WallElapsedMs() - DR7T0;;
Print("DR7_TOTAL_ELAPSED_MS=", DR7TotalElapsed, "\n");;

DR7Output := Concatenation(
  "{\n  \"schema\":\"drophunt-row71-calibration/v1\",\n",
  "  \"m_search_class\":\"direct_M_level_m0_full_shadow_check\",\n",
  "  \"row71_B2_gate\":{\"verdict\":", JB(DR7Row71.verdict),
    ",\"charming\":", JB(DR7Row71.charming), ",\"hex310\":", DCP3BoolOrNull(DR7Row71.hex310),
    ",\"hex311\":", DCP3BoolOrNull(DR7Row71.hex311), ",\"onto\":", DCP3BoolOrNull(DR7Row71.onto),
    ",\"stage\":", JStr(DR7Row71.stage), "},\n",
  "  \"row36_B4_control\":{\"verdict\":", JB(DR7Row36.verdict),
    ",\"charming\":", JB(DR7Row36.charming), ",\"hex310\":", DCP3BoolOrNull(DR7Row36.hex310),
    ",\"hex311\":", DCP3BoolOrNull(DR7Row36.hex311), ",\"onto\":", DCP3BoolOrNull(DR7Row36.onto),
    ",\"stage\":", JStr(DR7Row36.stage), "},\n",
  "  \"B2_gate_pass\":", JB(DR7Row71.verdict), ",\n",
  "  \"total_elapsed_ms\":", String(DR7TotalElapsed), "\n}\n");;
WriteFile("search/certs/drophunt_row71_calibration_v1_20260829.json", DR7Output);;
Print("DR7_OUTPUT path=search/certs/drophunt_row71_calibration_v1_20260829.json\n");;
Print("ALL_DONE\n");;
