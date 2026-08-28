#############################################################################
## drophunt_pgl_producer_v3.g -- item 2 (裁定1751): PGammaL(2,8) window,
## v3 receipt pipeline. Reuses the validated E=PGammaL(2,8) self-contained
## construction from search/drophunt_pgl_producer_v1.g (marking search etc,
## already machine-confirmed: all 6 charming m give pass_count=9), now
## emitting a v3-schema receipt via a self-contained-window variant of
## DCP3EmitReceipt, for checker round-trip per item 5's discipline.
##
## SCHEMA NOTE (self-contained variant): this window is NOT of the K=M cap L
## shape DCP3BuildWindow/DCP3EmitReceipt assume (see search/certs/
## drophunt_pgl_calibration_v1_20260828.json step_b_e_construction_and_
## rederivation.correction_to_the_prior_pass_plan for why: E's own
## GT(E)-style computation is joined to the 972 M-targets purely by matching
## m mod 9, not via a K<=M group-homomorphism reduction). The receipt below
## sets self_contained_E:true and omits/nulls the M-relative fields
## (F1_m_factor, F2_ratio in the usual K<=M sense, reduction_match) that do
## not apply, while keeping the SS4 8-field discipline (predicate_rule,
## c_in_K, tau_descends, F4_isolated, positive_recordability, node_id,
## seed_key, wcp5d_ref) and the null-not-false short-circuit convention.
#############################################################################

Read("search/drophunt_checker_producer_v3.g");;

DPV3T0 := GAPLIB_WallElapsedMs();;

DPV3FRImages := [];;
DPV3FRImages[1] := 1;;
for DPV3x in [0..7] do
  DPV3FRImages[2+DPV3x] := 2 + GF8Mul(DPV3x, DPV3x);;
od;;
DPV3FR := PermList(DPV3FRImages);;
if Order(DPV3FR) <> 3 then Error("DPV3: Frobenius order drift"); fi;;

DPV3E := Group(DCP3X4, DCP3Y4, DPV3FR);;
if Size(DPV3E) <> 1512 then Error("DPV3: E order drift"); fi;;
DPV3DerivedE := DerivedSubgroup(DPV3E);;
if Size(DPV3DerivedE) <> 504 then Error("DPV3: derived(E) order drift"); fi;;

DPV3SCands := Filtered(Elements(DPV3E), g -> Order(g) = 2);;
DPV3TCands := Filtered(Elements(DPV3E), g -> Order(g) = 3);;
DPV3Selected := fail;;
for DPV3s in DPV3SCands do
  if DPV3Selected <> fail then break; fi;;
  for DPV3t in DPV3TCands do
    DPV3w := DPV3s * DPV3t^-1;;
    if not (Order(DPV3w) in [9,18]) then continue; fi;;
    DPV3x := DPV3w^2;;
    if Order(DPV3x) <> 9 then continue; fi;;
    DPV3y := DPV3s^-1 * DPV3x * DPV3s;;
    DPV3yViaT := DPV3t^-1 * DPV3x * DPV3t;;
    DPV3z := (DPV3t^2)^-1 * DPV3x * DPV3t^2;;
    DPV3w2 := DPV3t^-1 * DPV3s;;
    if not (DPV3y = DPV3yViaT and DPV3z*DPV3y*DPV3x = Identity(DPV3E) and DPV3w2^2 = DPV3y) then continue; fi;;
    if Size(Group(DPV3s,DPV3t)) <> 1512 then continue; fi;;
    if Size(Group(DPV3x,DPV3y)) <> 1512 then continue; fi;;
    DPV3Selected := rec(s:=DPV3s, t:=DPV3t, x:=DPV3x, y:=DPV3y);;
    break;;
  od;;
od;;
if DPV3Selected = fail then Error("DPV3: PGL28_MARKING_NOT_FOUND"); fi;;
DPV3s := DPV3Selected.s;; DPV3t := DPV3Selected.t;; DPV3x := DPV3Selected.x;; DPV3y := DPV3Selected.y;;

DPV3Charming := [0,2,3,5,6,8];;
DPV3DerivedElts := Elements(DPV3DerivedE);;
DPV3Rows := [];; DPV3ValidCount := 0;;
for DPV3m in DPV3Charming do
  for DPV3f in DPV3DerivedElts do
    DPV3ThetaF := DPV3s^-1 * DPV3f * DPV3s;;
    DPV3hex310 := (DPV3ThetaF * DPV3f = Identity(DPV3E));;
    DPV3stage := "hex310_fail";; DPV3hex311 := fail;; DPV3onto := fail;;
    if DPV3hex310 then
      DPV3u := 2*DPV3m + 1;;
      DPV3ymf := DPV3f * DPV3y^DPV3m;;
      DPV3TauYmf := DPV3t^-1 * DPV3ymf * DPV3t;;
      DPV3Tau2Ymf := DPV3t^-1 * DPV3TauYmf * DPV3t;;
      DPV3hex311 := (DPV3ymf * DPV3TauYmf * DPV3Tau2Ymf = Identity(DPV3E));;
      if DPV3hex311 then
        DPV3genA := DPV3x^DPV3u;; DPV3genB := DPV3f * DPV3y^DPV3u * DPV3f^-1;;
        DPV3onto := (Size(Group(DPV3genA, DPV3genB)) = 1512);;
        if DPV3onto then DPV3stage := "pass"; else DPV3stage := "onto_fail"; fi;;
      else DPV3stage := "hex311_fail"; fi;;
    fi;;
    DPV3verdict := (DPV3hex310 = true) and (DPV3hex311 = true) and (DPV3onto = true);;
    if DPV3verdict then DPV3ValidCount := DPV3ValidCount + 1; fi;;
    Add(DPV3Rows, rec(m:=DPV3m, perm:=DPV3f, charming:=true, hex310:=DPV3hex310,
      hex311:=DPV3hex311, onto:=DPV3onto, reduction_match:="null", verdict:=DPV3verdict, stage:=DPV3stage));;
  od;;
od;;
Print("DPV3_ROWS_TOTAL=", Length(DPV3Rows), " valid=", DPV3ValidCount, "  <- expect 6*9=54\n");;

#############################################################################
## Self-contained receipt emission (adapted from DCP3EmitReceipt; uses the
## same JStr/JArr/JB/HexSHA256 helpers already loaded).
#############################################################################
DPV3PermToJsonList := function(p, deg) return JArr(List([1..deg], j -> String(j^p))); end;;
DPV3BoolOrNull := function(v) if v = fail or v = "null" then return "null"; fi; return JB(v); end;;

DPV3RowsJson := JoinC(List(DPV3Rows, r -> Concatenation(
  "{\"m\":", String(r.m),
  ",\"perm_one_line\":", DPV3PermToJsonList(r.perm, 9),
  ",\"charming\":", JB(r.charming),
  ",\"hex310\":", DPV3BoolOrNull(r.hex310),
  ",\"hex311\":", DPV3BoolOrNull(r.hex311),
  ",\"onto\":", DPV3BoolOrNull(r.onto),
  ",\"reduction_match\":\"null\"",
  ",\"verdict\":", JB(r.verdict),
  ",\"stage\":", JStr(r.stage), "}")), ",\n");;

DPV3NodeId := "PGammaL(2,8)_self_contained_E_window (search/pgl28_independent_window_producer_v1.py structure)";;
DPV3SeedKeyDigest := HexSHA256("self_contained_E_no_M_level_seed");;

DPV3Output := Concatenation(
  "{\n",
  "  \"schema\":\"drophunt-checker-producer/v3\",\n",
  "  \"status\":\"CANDIDATE_GAP_PRODUCER\",\n",
  "  \"verified\":false,\n",
  "  \"predicate_rule\":\"F2_quotient\",\n",
  "  \"self_contained_E\":true,\n",
  "  \"c_in_K\":true,\n",   # RHS is always Identity in this formulation (no external c-twist)
  "  \"tau_descends\":true,\n",
  "  \"F4_isolated\":\"NOT_EVALUATED\",\n",
  "  \"positive_recordability\":\"NONE\",\n",
  "  \"node_id\":", JStr(DPV3NodeId), ",\n",
  "  \"seed_key\":{\"word\":[],\"seed_name\":\"self_contained_E_all_charming_m\",\"digest\":", JStr(DPV3SeedKeyDigest), "},\n",
  "  \"wcp5d_ref\":\"docs/notes/wcp5d_resolution_v1.md (裁定164/165)\",\n",
  "  \"reduction_index_order\":\"not_applicable_self_contained\",\n",
  "  \"window\":{",
    "\"E_order\":1512",
    ",\"derived_E_order\":", String(Size(DPV3DerivedE)),
    ",\"degree\":9",
    ",\"charming_m_mod9\":", JArr(List(DPV3Charming,String)),
    ",\"Ex_one_line\":", DPV3PermToJsonList(DPV3x, 9),
    ",\"Ey_one_line\":", DPV3PermToJsonList(DPV3y, 9),
    ",\"Es_one_line\":", DPV3PermToJsonList(DPV3s, 9),
    ",\"Et_one_line\":", DPV3PermToJsonList(DPV3t, 9), "},\n",
  "  \"seed\":\"self_contained_E_all_charming_m\",\n",
  "  \"cc1_candidate_coverage\":{\"evaluated_count\":", String(Length(DPV3Rows)),
    ",\"expected_count\":", String(6*504), ",\"match\":", JB(Length(DPV3Rows)=6*504), "},\n",
  "  \"valid_count\":", String(DPV3ValidCount), ",\n",
  "  \"expected_valid_count\":54,\n",
  "  \"total_elapsed_ms\":", String(GAPLIB_WallElapsedMs()-DPV3T0), ",\n",
  "  \"rows\":[\n", DPV3RowsJson, "\n  ]\n",
  "}\n");;
WriteFile("search/certs/drophunt_checker_v3_receipt_PGammaL28_selfcontained_20260829.json", DPV3Output);;
Print("DPV3_OUTPUT path=search/certs/drophunt_checker_v3_receipt_PGammaL28_selfcontained_20260829.json\n");;
Print("DPV3_TOTAL_ELAPSED_MS=", GAPLIB_WallElapsedMs()-DPV3T0, "\n");;
Print("ALL_DONE\n");;
