#############################################################################
## drophunt_calibration_fibcost_v1.g
##
## DROP-HUNT-DOUBLE calibration (implementer, 2026-08-29). This script does
## NOT recompute the LINS index/joint-image census (that is already exactly
## computed for all 4,265 rows in
## ci/lins_marked_artifacts_32626064970/lins_marked_export/
## lins_marked_strictness_export_v1_20260823.json, status
## CANDIDATE_GAP_PRODUCER, verified:false -- reused as-is, see
## scratchpad/drophunt_fib_distribution_v1.json).
##
## What THIS script measures (genuinely new, not in any existing artifact):
## real GAP wall time for the two per-row operations that dominate the
## producer's cost (quotient-group construction via
## NaturalHomomorphismByNormalSubgroup + IsomorphismPermGroup, and joint-image
## group-order computation), isolated per row, for the 3 cheapest STRICT_F2
## windows (b3_index of L in {3,8,48}, #fib(K) in {9,8,4}).
##
## IMPORTANT SCOPE LIMIT (flagged, not silently assumed away): this does NOT
## time hexagon/charming/onto predicate evaluation per raw candidate -- no
## generic reusable checker for arbitrary K exists yet in this repo (see
## calibration report item c). The numbers below are a lower bound on real
## fibre-exhaustion cost (they cover "build the search space", not "search
## it"), reported honestly as such.
#############################################################################

Read("search/probe/wac_v1/gap_output_prelude.g");;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

DHFCOutPath := "search/certs/drophunt_calibration_fibcost_v1_20260829.json";;

#############################################################################
## Rebuild PB3/M = G9 x PSL(2,8), exactly as in lins_marked_strictness_export_v1.g
#############################################################################
DHFCG9Rec := MakeGn(9);;
if Size(DHFCG9Rec.G) <> 2916 then Error("DHFC: G9 order drift"); fi;
CheckGF8();;
DHFCSMat := MakeMatGF8(1,0,1,1);;
DHFCTMat := MakeMatGF8(4,3,1,5);;
DHFCSPerm := MatToPermGF8(DHFCSMat);;
DHFCTPerm := MatToPermGF8(DHFCTMat);;
DHFCWPerm := DHFCSPerm * DHFCTPerm^-1;;
DHFCX4 := DHFCWPerm^2;;
DHFCY4 := DHFCSPerm^-1 * DHFCX4 * DHFCSPerm;;
DHFCP4 := Group(DHFCX4, DHFCY4);;
if Size(DHFCP4) <> 504 then Error("DHFC: PSL(2,8) order drift"); fi;

DHFCShiftPerm := function(p, offset, size)
  local images, j;
  images := [1..offset+size];
  for j in [1..size] do images[offset+j] := offset + (j^p); od;
  return PermList(images);
end;;

DHFCDirectSumPerm := function(p, psize, q, qsize)
  return p * DHFCShiftPerm(q, psize, qsize);
end;;

DHFCPermDegree := function(G)
  local d;
  d := LargestMovedPoint(G);;
  if d = 0 then return 1; fi;
  return d;
end;;

DHFCMX := DHFCDirectSumPerm(DHFCG9Rec.x, 27, DHFCX4, 9);;
DHFCMY := DHFCDirectSumPerm(DHFCG9Rec.y, 27, DHFCY4, 9);;
DHFCM := Group(DHFCMX, DHFCMY);;
DHFCMOrder := Size(DHFCM);;
DHFCMDegree := 36;;
if DHFCMOrder <> 1469664 then Error("DHFC: PB3/M order drift"); fi;

DHFCF := FreeGroup("a", "b");;
DHFCa := DHFCF.1;; DHFCb := DHFCF.2;;
DHFCRel := DHFCa * DHFCb * DHFCa * (DHFCb * DHFCa * DHFCb)^-1;;
DHFCB3 := DHFCF / [DHFCRel];;
DHFCs1 := DHFCB3.1;; DHFCs2 := DHFCB3.2;;

#############################################################################
## Small LINS call (bound 48) to reconstruct the 3 cheapest target L's
## without a fresh LINS(B3,2000) call and without hand-parsing word strings.
#############################################################################
if LoadPackage("lins") <> true then Error("DHFC: LINS package load failed"); fi;

DHFCT0 := GAPLIB_WallElapsedMs();;
DHFCSearchT0 := GAPLIB_WallElapsedMs();;
DHFCSearch := LowIndexNormalSubgroupsSearch(DHFCB3, 48);;
DHFCNodes := ComputedNormalSubgroups(DHFCSearch);;
DHFCSearchElapsed := GAPLIB_WallElapsedMs() - DHFCSearchT0;;
Print("DHFC_LINS48_DONE nodes=", Length(DHFCNodes),
  " elapsed_ms=", DHFCSearchElapsed, "\n");;

DHFCTargetIdx := [3, 8, 48];;
DHFCRows := [];;

for DHFCNode in DHFCNodes do
  DHFCIdx := Index(DHFCNode);;
  if DHFCIdx = 1 then continue; fi;
  if not (DHFCIdx in DHFCTargetIdx) then continue; fi;

  DHFCRowT0 := GAPLIB_WallElapsedMs();;
  DHFCL := Grp(DHFCNode);;

  DHFCQuotT0 := GAPLIB_WallElapsedMs();;
  DHFCHom := NaturalHomomorphismByNormalSubgroup(DHFCB3, DHFCL);;
  DHFCQ := Image(DHFCHom);;
  DHFCIso := IsomorphismPermGroup(DHFCQ);;
  DHFCQp := Image(DHFCIso);;
  DHFCS1p := Image(DHFCIso, Image(DHFCHom, DHFCs1));;
  DHFCS2p := Image(DHFCIso, Image(DHFCHom, DHFCs2));;
  DHFCXp := DHFCS1p^2;; DHFCYp := DHFCS2p^2;; DHFCCp := (DHFCS1p*DHFCS2p*DHFCS1p)^2;;
  DHFCQuotElapsed := GAPLIB_WallElapsedMs() - DHFCQuotT0;;

  DHFCDeg := DHFCPermDegree(DHFCQp);;
  DHFCJX := DHFCDirectSumPerm(DHFCMX, DHFCMDegree, DHFCXp, DHFCDeg);;
  DHFCJY := DHFCDirectSumPerm(DHFCMY, DHFCMDegree, DHFCYp, DHFCDeg);;
  DHFCJC := DHFCShiftPerm(DHFCCp, DHFCMDegree, DHFCDeg);;

  DHFCJointT0 := GAPLIB_WallElapsedMs();;
  DHFCJointF2Order := Size(Group(DHFCJX, DHFCJY));;
  DHFCJointPB3Order := Size(Group([DHFCJX, DHFCJY, DHFCJC]));;
  DHFCJointElapsed := GAPLIB_WallElapsedMs() - DHFCJointT0;;

  DHFCF2Ratio := DHFCJointF2Order / DHFCMOrder;;
  DHFCPB3Ratio := DHFCJointPB3Order / DHFCMOrder;;
  DHFCFib := DHFCPB3Ratio * DHFCF2Ratio;;

  DHFCRowElapsed := GAPLIB_WallElapsedMs() - DHFCRowT0;;

  Print("DHFC_ROW b3_index=", DHFCIdx,
    " PB3_ratio=", DHFCPB3Ratio, " F2_ratio=", DHFCF2Ratio,
    " fib=", DHFCFib,
    " quot_ms=", DHFCQuotElapsed, " joint_ms=", DHFCJointElapsed,
    " row_total_ms=", DHFCRowElapsed, "\n");;

  Add(DHFCRows, rec(
    b3_index := DHFCIdx,
    PB3_ratio_M_over_K := DHFCPB3Ratio,
    F2_ratio_MF_over_KF := DHFCF2Ratio,
    fib_K := DHFCFib,
    quot_build_ms := DHFCQuotElapsed,
    joint_image_ms := DHFCJointElapsed,
    row_total_ms := DHFCRowElapsed
  ));;
od;;

DHFCTotalElapsed := GAPLIB_WallElapsedMs() - DHFCT0;;
Print("DHFC_SUMMARY rows_measured=", Length(DHFCRows),
  " total_elapsed_ms=", DHFCTotalElapsed, "\n");;

DHFCRowsJson := JoinC(List(DHFCRows, r -> Concatenation(
  "{\"b3_index\":", String(r.b3_index),
  ",\"PB3_ratio_M_over_K\":", String(r.PB3_ratio_M_over_K),
  ",\"F2_ratio_MF_over_KF\":", String(r.F2_ratio_MF_over_KF),
  ",\"fib_K\":", String(r.fib_K),
  ",\"quot_build_ms\":", String(r.quot_build_ms),
  ",\"joint_image_ms\":", String(r.joint_image_ms),
  ",\"row_total_ms\":", String(r.row_total_ms), "}")), ",\n");;

DHFCOutput := Concatenation(
  "{\n",
  "  \"schema\":\"drophunt-calibration-fibcost/v1\",\n",
  "  \"status\":\"CANDIDATE_LOWER_BOUND_PROXY\",\n",
  "  \"verified\":false,\n",
  "  \"note\":\"Times quotient-group construction (NaturalHomomorphismByNormalSubgroup ",
  "+ IsomorphismPermGroup) and joint-image order computation for the 3 cheapest ",
  "STRICT_F2 windows, via LowIndexNormalSubgroupsSearch(B3,48) (not a fresh ",
  "LINS(B3,2000) call). Does NOT time hexagon/charming/onto predicate ",
  "evaluation per raw candidate -- no generic reusable checker for arbitrary K ",
  "exists yet in this repo (see calibration report item c). This is a LOWER ",
  "BOUND on real fibre-exhaustion cost (search-space construction only, not ",
  "search), reported honestly as such.\",\n",
  "  \"lins48_search_elapsed_ms\":", String(DHFCSearchElapsed), ",\n",
  "  \"total_elapsed_ms\":", String(DHFCTotalElapsed), ",\n",
  "  \"rows\":[\n", DHFCRowsJson, "\n  ]\n",
  "}\n");;

WriteFile(DHFCOutPath, DHFCOutput);;
DHFCOutRaw := StringFile(DHFCOutPath);;
Print("DHFC_OUTPUT path=", DHFCOutPath, " bytes=", Length(DHFCOutRaw),
  " sha256=", HexSHA256(DHFCOutRaw), "\n");;
Print("ALL_DONE\n");;
