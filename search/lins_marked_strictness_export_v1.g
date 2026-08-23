#############################################################################
## lins_marked_strictness_export_v1.g
##
## Producer for ruling 1624 / mail 159h, LINS marked-source export.
##
## Universe (fixed for the production run): every nonidentity node returned
## by one LowIndexNormalSubgroupsSearch(B3, 2000) call.  LINS nodes are normal
## subgroups L of B3, hence Core_B3(L)=L.  For every node this script exports
## the exact marked permutation map on sigma1,sigma2 and x=sigma1^2,
## y=sigma2^2,c=(sigma1*sigma2*sigma1)^2.
##
## The roof is M=K^(9) cap N_S4.  Its compact marked PB3/M model has order
## 1,469,664 and c maps to 1.  For K=M cap Core_B3(L), the script computes
##
##   J_F2  = im(F2 -> PB3/M x B3/L),
##   J_PB3 = im(PB3 -> PB3/M x B3/L),
##
## and records |J_F2|/|PB3/M|=[M_F2:K_F2] and
## |J_PB3|/|PB3/M|=[M:K].  Thus F2 strictness is measured from the marked
## joint image, not inferred from L<>1, IdGroup, or a twin label.
##
## Full production is GHA-only.  A bounded local preflight can set either
## global LINS_MARKED_INDEX_HI before Read(), or environment variable
## LINS_MARKED_INDEX_HI.  The output can likewise be overridden through
## LINS_MARKED_OUTPUT.  Preflight output makes no 4,265-row CLAIM-COVER.
#############################################################################

Read("search/probe/wac_v1/gap_output_prelude.g");;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

LMEV1ScriptPath := "search/lins_marked_strictness_export_v1.g";;
LMEV1ReferenceCensusPath :=
  "search/certs/lins_census_2000_v1_20260811.json";;
LMEV1ReferenceCensusSHA :=
  "d0832df8a4e61adff45c5c24c8eba32f5d388f55412907ed5ffdf714b2b4b958";;

if not IsBound(LINS_MARKED_INDEX_HI) then
  LMEV1EnvBound := GetEnv("LINS_MARKED_INDEX_HI");;
  if LMEV1EnvBound <> fail and Length(LMEV1EnvBound) > 0 then
    LINS_MARKED_INDEX_HI := Int(LMEV1EnvBound);;
  else
    LINS_MARKED_INDEX_HI := 2000;;
  fi;
fi;
if not IsBound(LINS_MARKED_OUTPUT) then
  LMEV1EnvOutput := GetEnv("LINS_MARKED_OUTPUT");;
  if LMEV1EnvOutput <> fail and Length(LMEV1EnvOutput) > 0 then
    LINS_MARKED_OUTPUT := LMEV1EnvOutput;;
  else
    LINS_MARKED_OUTPUT :=
      "search/certs/lins_marked_strictness_export_v1_20260823.json";;
  fi;
fi;

if not IsInt(LINS_MARKED_INDEX_HI) or LINS_MARKED_INDEX_HI < 2 or
   LINS_MARKED_INDEX_HI > 2000 then
  Error("LMEV1: LINS_MARKED_INDEX_HI must be an integer in [2,2000]");
fi;

LMEV1ReferenceRaw := StringFile(LMEV1ReferenceCensusPath);;
if LMEV1ReferenceRaw = fail or
   HexSHA256(LMEV1ReferenceRaw) <> LMEV1ReferenceCensusSHA then
  Error("LMEV1: reference LINS-2000 census missing or SHA256 drift");
fi;
LMEV1ScriptRaw := StringFile(LMEV1ScriptPath);;
if LMEV1ScriptRaw = fail then Error("LMEV1: cannot read own source"); fi;
LMEV1ScriptSHA := HexSHA256(LMEV1ScriptRaw);;

LMEV1ShiftPerm := function(p, offset, size)
  local images, j;
  images := [1..offset+size];
  for j in [1..size] do images[offset+j] := offset + (j^p); od;
  return PermList(images);
end;;

LMEV1DirectSumPerm := function(p, psize, q, qsize)
  return p * LMEV1ShiftPerm(q, psize, qsize);
end;;

LMEV1PermDegree := function(G)
  local d;
  d := LargestMovedPoint(G);
  if d = 0 then return 1; fi;
  return d;
end;;

LMEV1WordsJson := function(words)
  return JArr(List(words, JStr));
end;;

LMEV1HistogramJson := function(values)
  local vals, parts, v;
  vals := Set(values);
  parts := [];
  for v in vals do
    Add(parts, Concatenation("{\"ratio\":", String(v),
      ",\"count\":", String(Number(values, x -> x = v)), "}"));
  od;
  return JArr(parts);
end;;

#############################################################################
## Fixed compact marked model of PB3/M = G9 x PSL(2,8).
#############################################################################
LMEV1G9Rec := MakeGn(9);;
if Size(LMEV1G9Rec.G) <> 2916 then Error("LMEV1: G9 order drift"); fi;
CheckGF8();;
LMEV1SMat := MakeMatGF8(1,0,1,1);;
LMEV1TMat := MakeMatGF8(4,3,1,5);;
LMEV1SPerm := MatToPermGF8(LMEV1SMat);;
LMEV1TPerm := MatToPermGF8(LMEV1TMat);;
LMEV1WPerm := LMEV1SPerm * LMEV1TPerm^-1;;
LMEV1X4 := LMEV1WPerm^2;;
LMEV1Y4 := LMEV1SPerm^-1 * LMEV1X4 * LMEV1SPerm;;
LMEV1P4 := Group(LMEV1X4, LMEV1Y4);;
if Size(LMEV1P4) <> 504 then Error("LMEV1: PSL(2,8) order drift"); fi;

LMEV1MX := LMEV1DirectSumPerm(LMEV1G9Rec.x, 27, LMEV1X4, 9);;
LMEV1MY := LMEV1DirectSumPerm(LMEV1G9Rec.y, 27, LMEV1Y4, 9);;
LMEV1M := Group(LMEV1MX, LMEV1MY);;
LMEV1MOrder := Size(LMEV1M);;
LMEV1MDegree := 36;;
if LMEV1MOrder <> 1469664 then Error("LMEV1: PB3/M order drift"); fi;

LMEV1MMarkedCanonical := Concatenation(
  "x=", String(LMEV1MX), "\n",
  "y=", String(LMEV1MY), "\n",
  "c=()\n",
  "order=", String(LMEV1MOrder), "\n");;
LMEV1MMarkedSHA := HexSHA256(LMEV1MMarkedCanonical);;

#############################################################################
## One LINS call and exact per-node marked joint images.
#############################################################################
LMEV1F := FreeGroup("a", "b");;
LMEV1a := LMEV1F.1;;
LMEV1b := LMEV1F.2;;
LMEV1Rel := LMEV1a * LMEV1b * LMEV1a *
  (LMEV1b * LMEV1a * LMEV1b)^-1;;
LMEV1B3 := LMEV1F / [LMEV1Rel];;
LMEV1s1 := LMEV1B3.1;;
LMEV1s2 := LMEV1B3.2;;
LMEV1x := LMEV1s1^2;;
LMEV1y := LMEV1s2^2;;
LMEV1c := (LMEV1s1 * LMEV1s2 * LMEV1s1)^2;;

if LoadPackage("lins") <> true then Error("LMEV1: LINS package load failed"); fi;
LMEV1T0 := GAPLIB_WallElapsedMs();;
LMEV1Search := LowIndexNormalSubgroupsSearch(LMEV1B3,
  LINS_MARKED_INDEX_HI);;
LMEV1Nodes := ComputedNormalSubgroups(LMEV1Search);;
LMEV1TLins := GAPLIB_WallElapsedMs();;
Print("LMEV1_LINS_DONE bound=", LINS_MARKED_INDEX_HI,
  " nodes=", Length(LMEV1Nodes), " elapsed_ms=", LMEV1TLins-LMEV1T0,
  "\n");;

LMEV1Rows := [];;
LMEV1F2Ratios := [];;
LMEV1PB3Ratios := [];;
LMEV1Idx1Count := 0;;
LMEV1StrictF2Count := 0;;
LMEV1StrictPB3Count := 0;;
LMEV1CenterOnlyCount := 0;;
LMEV1Processed := 0;;

for LMEV1Node in LMEV1Nodes do
  LMEV1L := Grp(LMEV1Node);;
  LMEV1Index := Index(LMEV1Node);;
  if LMEV1Index = 1 then
    LMEV1Idx1Count := LMEV1Idx1Count + 1;
    continue;
  fi;
  if not IsNormal(LMEV1B3, LMEV1L) then
    Error("LMEV1: LINS emitted a non-normal node");
  fi;

  LMEV1GenWords := Set(List(GeneratorsOfGroup(LMEV1L), String));;
  LMEV1NodeKey := HexSHA256(Concatenation(
    "index=", String(LMEV1Index), "\n",
    JoinC(LMEV1GenWords, "\n"), "\n"));;

  LMEV1Hom := NaturalHomomorphismByNormalSubgroup(LMEV1B3, LMEV1L);;
  LMEV1Q := Image(LMEV1Hom);;
  LMEV1Iso := IsomorphismPermGroup(LMEV1Q);;
  if LMEV1Iso = fail then Error("LMEV1: quotient permutation isomorphism failed"); fi;
  LMEV1Qp := Image(LMEV1Iso);;
  if Size(LMEV1Qp) <> LMEV1Index then Error("LMEV1: quotient order/index drift"); fi;
  LMEV1Degree := LMEV1PermDegree(LMEV1Qp);;
  LMEV1S1p := Image(LMEV1Iso, Image(LMEV1Hom, LMEV1s1));;
  LMEV1S2p := Image(LMEV1Iso, Image(LMEV1Hom, LMEV1s2));;
  LMEV1Xp := LMEV1S1p^2;;
  LMEV1Yp := LMEV1S2p^2;;
  LMEV1Cp := (LMEV1S1p * LMEV1S2p * LMEV1S1p)^2;;
  if LMEV1Xp <> Image(LMEV1Iso, Image(LMEV1Hom, LMEV1x)) or
     LMEV1Yp <> Image(LMEV1Iso, Image(LMEV1Hom, LMEV1y)) or
     LMEV1Cp <> Image(LMEV1Iso, Image(LMEV1Hom, LMEV1c)) then
    Error("LMEV1: marked x/y/c evaluation drift");
  fi;
  if LMEV1S1p*LMEV1S2p*LMEV1S1p <>
     LMEV1S2p*LMEV1S1p*LMEV1S2p then
    Error("LMEV1: quotient braid relation drift");
  fi;
  LMEV1PureImageOrder := Size(Group(LMEV1Xp, LMEV1Yp));;
  LMEV1PB3ImageOrder := Size(Group([LMEV1Xp, LMEV1Yp, LMEV1Cp]));;

  LMEV1JX := LMEV1DirectSumPerm(LMEV1MX, LMEV1MDegree,
    LMEV1Xp, LMEV1Degree);;
  LMEV1JY := LMEV1DirectSumPerm(LMEV1MY, LMEV1MDegree,
    LMEV1Yp, LMEV1Degree);;
  LMEV1JC := LMEV1ShiftPerm(LMEV1Cp, LMEV1MDegree,
    LMEV1Degree);;
  LMEV1JointF2Order := Size(Group(LMEV1JX, LMEV1JY));;
  LMEV1JointPB3Order := Size(Group([LMEV1JX, LMEV1JY, LMEV1JC]));;
  if LMEV1JointF2Order mod LMEV1MOrder <> 0 or
     LMEV1JointPB3Order mod LMEV1MOrder <> 0 then
    Error("LMEV1: joint-image ratio is nonintegral");
  fi;
  LMEV1F2Ratio := LMEV1JointF2Order / LMEV1MOrder;;
  LMEV1PB3Ratio := LMEV1JointPB3Order / LMEV1MOrder;;
  if LMEV1PB3Ratio mod LMEV1F2Ratio <> 0 then
    Error("LMEV1: PB3/F2 strictness ratio incompatibility");
  fi;
  LMEV1StrictF2 := LMEV1F2Ratio > 1;;
  LMEV1StrictPB3 := LMEV1PB3Ratio > 1;;
  LMEV1CenterOnly := LMEV1StrictPB3 and not LMEV1StrictF2;;
  if LMEV1StrictF2 then LMEV1StrictF2Count := LMEV1StrictF2Count + 1; fi;
  if LMEV1StrictPB3 then LMEV1StrictPB3Count := LMEV1StrictPB3Count + 1; fi;
  if LMEV1CenterOnly then LMEV1CenterOnlyCount := LMEV1CenterOnlyCount + 1; fi;
  Add(LMEV1F2Ratios, LMEV1F2Ratio);
  Add(LMEV1PB3Ratios, LMEV1PB3Ratio);

  LMEV1SourceCanonical := Concatenation(
    "node_key=", LMEV1NodeKey, "\n",
    "index=", String(LMEV1Index), "\n",
    "degree=", String(LMEV1Degree), "\n",
    "sigma1=", String(LMEV1S1p), "\n",
    "sigma2=", String(LMEV1S2p), "\n",
    "x=", String(LMEV1Xp), "\n",
    "y=", String(LMEV1Yp), "\n",
    "c=", String(LMEV1Cp), "\n");;
  LMEV1SourceSHA := HexSHA256(LMEV1SourceCanonical);;

  LMEV1StrictClass := "NO_REFINEMENT";;
  if LMEV1CenterOnly then LMEV1StrictClass := "PB3_CENTER_ONLY"; fi;
  if LMEV1StrictF2 then LMEV1StrictClass := "STRICT_F2"; fi;
  LMEV1RowJson := Concatenation(
    "{\"node_id\":\"", LMEV1NodeKey, "\"",
    ",\"b3_index\":", String(LMEV1Index),
    ",\"canonical_id_words\":", LMEV1WordsJson(LMEV1GenWords),
    ",\"marked_quotient_map\":{",
      "\"quotient_order\":", String(LMEV1Index),
      ",\"permutation_degree\":", String(LMEV1Degree),
      ",\"sigma1\":", JStr(String(LMEV1S1p)),
      ",\"sigma2\":", JStr(String(LMEV1S2p)),
      ",\"x_eq_sigma1_sq\":", JStr(String(LMEV1Xp)),
      ",\"y_eq_sigma2_sq\":", JStr(String(LMEV1Yp)),
      ",\"c_eq_delta_sq\":", JStr(String(LMEV1Cp)),
      ",\"F2_image_order\":", String(LMEV1PureImageOrder),
      ",\"PB3_image_order\":", String(LMEV1PB3ImageOrder), "}",
    ",\"core_B3_L\":{",
      "\"construction\":\"L (normality is part of the LINS node contract)\"",
      ",\"equals_L\":true",
      ",\"index\":", String(LMEV1Index),
      ",\"canonical_id_words\":", LMEV1WordsJson(LMEV1GenWords), "}",
    ",\"joint_image\":{",
      "\"F2_order\":", String(LMEV1JointF2Order),
      ",\"PB3_order\":", String(LMEV1JointPB3Order), "}",
    ",\"source_K\":\"M cap Core_B3(L)\"",
    ",\"strictness\":{",
      "\"F2_ratio_MF_over_KF\":", String(LMEV1F2Ratio),
      ",\"PB3_ratio_M_over_K\":", String(LMEV1PB3Ratio),
      ",\"strict_F2\":", JB(LMEV1StrictF2),
      ",\"strict_PB3\":", JB(LMEV1StrictPB3),
      ",\"class\":", JStr(LMEV1StrictClass), "}",
    ",\"source_digest_sha256\":\"", LMEV1SourceSHA, "\"}");;
  Add(LMEV1Rows, rec(key := LMEV1NodeKey, json := LMEV1RowJson));
  LMEV1Processed := LMEV1Processed + 1;
  if LMEV1Processed mod 100 = 0 then
    Print("LMEV1_PROGRESS processed=", LMEV1Processed,
      " elapsed_ms=", GAPLIB_WallElapsedMs()-LMEV1T0, "\n");
  fi;
od;

Sort(LMEV1Rows, function(a,b) return a.key < b.key; end);;
LMEV1Keys := List(LMEV1Rows, r -> r.key);;
if Length(Set(LMEV1Keys)) <> Length(LMEV1Keys) then
  Error("LMEV1: duplicate canonical node id");
fi;
LMEV1RowsText := JoinC(List(LMEV1Rows, r -> r.json), ",\n");;
LMEV1RowsSHA := HexSHA256(Concatenation(LMEV1RowsText, "\n"));;
LMEV1FullMode := LINS_MARKED_INDEX_HI = 2000;;
LMEV1CoverComplete := LMEV1FullMode and Length(LMEV1Nodes) = 4266 and
  LMEV1Idx1Count = 1 and LMEV1Processed = 4265;;
if LMEV1FullMode and not LMEV1CoverComplete then
  Error("LMEV1: full-run CLAIM-COVER cardinality drift");
fi;

LMEV1Output := Concatenation(
  "{\n",
  "  \"schema\":\"lins-marked-strictness-export/v1\",\n",
  "  \"status\":\"CANDIDATE_GAP_PRODUCER\",\n",
  "  \"verified\":false,\n",
  "  \"authority\":\"ruling 1624 / mail 159h section next-axis-2\",\n",
  "  \"universe\":{",
    "\"group\":\"B3=<sigma1,sigma2 | sigma1 sigma2 sigma1=sigma2 sigma1 sigma2>\"",
    ",\"method\":\"one LowIndexNormalSubgroupsSearch call\"",
    ",\"index_upper_bound\":", String(LINS_MARKED_INDEX_HI),
    ",\"nodes_total\":", String(Length(LMEV1Nodes)),
    ",\"identity_nodes_excluded\":", String(LMEV1Idx1Count),
    ",\"nonidentity_rows\":", String(LMEV1Processed), "},\n",
  "  \"claim_cover\":{",
    "\"claim\":\"all 4,265 nonidentity nodes of the fixed index<=2000 LINS call\"",
    ",\"complete\":", JB(LMEV1CoverComplete),
    ",\"mode\":", JStr(Concatenation("bound_", String(LINS_MARKED_INDEX_HI))), "},\n",
  "  \"source_pins\":{",
    "\"reference_census_path\":", JStr(LMEV1ReferenceCensusPath),
    ",\"reference_census_sha256\":", JStr(LMEV1ReferenceCensusSHA),
    ",\"producer_path\":", JStr(LMEV1ScriptPath),
    ",\"producer_sha256\":", JStr(LMEV1ScriptSHA), "},\n",
  "  \"roof_M\":{",
    "\"name\":\"M=K^(9) cap N_S4\"",
    ",\"model\":\"compact marked PB3/M = G9 x PSL(2,8)\"",
    ",\"order\":", String(LMEV1MOrder),
    ",\"permutation_degree\":", String(LMEV1MDegree),
    ",\"marked_model_sha256\":", JStr(LMEV1MMarkedSHA),
    ",\"c_image\":\"identity\"},\n",
  "  \"summary\":{",
    "\"strict_F2_count\":", String(LMEV1StrictF2Count),
    ",\"strict_PB3_count\":", String(LMEV1StrictPB3Count),
    ",\"PB3_center_only_count\":", String(LMEV1CenterOnlyCount),
    ",\"F2_ratio_histogram\":", LMEV1HistogramJson(LMEV1F2Ratios),
    ",\"PB3_ratio_histogram\":", LMEV1HistogramJson(LMEV1PB3Ratios),
    ",\"rows_sha256\":", JStr(LMEV1RowsSHA),
    ",\"lins_elapsed_ms\":", String(LMEV1TLins-LMEV1T0),
    ",\"total_elapsed_ms\":", String(GAPLIB_WallElapsedMs()-LMEV1T0), "},\n",
  "  \"interpretation_limit\":\"Inventory and exact finite marked joint-image measurement only. No GT(K) enumeration, no isolated/genuine/non-arithmetic verdict, no OBS-UNIF-1 promotion, and no Lean verification.\",\n",
  "  \"rows\":[\n", LMEV1RowsText, "\n  ]\n",
  "}\n");;

WriteFile(LINS_MARKED_OUTPUT, LMEV1Output);;
LMEV1OutputRaw := StringFile(LINS_MARKED_OUTPUT);;
if LMEV1OutputRaw = fail then Error("LMEV1: output write failed"); fi;
Print("LMEV1_OUTPUT path=", LINS_MARKED_OUTPUT,
  " bytes=", Length(LMEV1OutputRaw),
  " sha256=", HexSHA256(LMEV1OutputRaw), "\n");;
Print("LMEV1_SUMMARY rows=", LMEV1Processed,
  " strict_f2=", LMEV1StrictF2Count,
  " strict_pb3=", LMEV1StrictPB3Count,
  " center_only=", LMEV1CenterOnlyCount,
  " cover=", LMEV1CoverComplete, "\n");;
Print("ALL_DONE\n");;
