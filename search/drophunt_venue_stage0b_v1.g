#############################################################################
## drophunt_venue_stage0b_v1.g -- item 8: venue re-check via EXPORT-DIRECT
## sigma1/sigma2 reconstruction (NO LowIndexNormalSubgroupsSearch re-run).
## Target: b3_index=192, node 064fd39d5e9070c3..., F2=96, |G|=141,087,744
## (~1.41e8, the coordinator's stated true largest-window scale).
#############################################################################

Read("search/drophunt_checker_producer_v3.g");;

DVBT0 := GAPLIB_WallElapsedMs();;

## sigma1,sigma2 read verbatim from
## ci/lins_marked_artifacts_32626064970/lins_marked_export/
## lins_marked_strictness_export_v1_20260823.json row node_id=064fd39d5e9070c3...
DVBS1 := (1,97,65,161,33,129)(2,98,66,162,34,130)(3,99,67,163,35,131)(4,100,68,164,36,132)(5,101,69,165,37,133)(6,102,70,166,38,134)(7,103,71,167,39,135)(8,104,72,168,40,136)(9,109,77,171,47,143)(10,110,78,172,48,144)(11,111,79,169,45,141)(12,112,80,170,46,142)(13,107,75,175,41,137)(14,108,76,176,42,138)(15,105,73,173,43,139)(16,106,74,174,44,140)(17,113,85,178,50,150)(18,114,86,177,49,149)(19,115,87,180,52,152)(20,116,88,179,51,151)(21,117,82,182,54,145)(22,118,81,181,53,146)(23,119,84,184,56,147)(24,120,83,183,55,148)(25,125,92,188,64,153)(26,126,91,187,63,154)(27,127,90,186,62,155)(28,128,89,185,61,156)(29,124,96,192,57,157)(30,123,95,191,58,158)(31,122,94,190,59,159)(32,121,93,189,60,160);;
DVBS2 := (1,105,81,164,44,148)(2,106,82,163,43,147)(3,107,83,162,42,146)(4,108,84,161,41,145)(5,112,88,168,45,149)(6,111,87,167,46,150)(7,110,86,166,47,151)(8,109,85,165,48,152)(9,98,90,170,33,153)(10,97,89,169,34,154)(11,100,92,172,35,155)(12,99,91,171,36,156)(13,101,94,174,38,157)(14,102,93,173,37,158)(15,103,96,176,40,159)(16,104,95,175,39,160)(17,121,67,179,59,129)(18,122,68,180,60,130)(19,123,65,177,57,131)(20,124,66,178,58,132)(21,125,69,183,63,135)(22,126,70,184,64,136)(23,127,71,181,61,133)(24,128,72,182,62,134)(25,113,73,185,49,137)(26,114,74,186,50,138)(27,115,75,187,51,139)(28,116,76,188,52,140)(29,120,79,189,56,143)(30,119,80,190,55,144)(31,118,77,191,54,141)(32,117,78,192,53,142);;

## sanity check 1: braid relation s1 s2 s1 = s2 s1 s2 (must hold, since these
## permutations are supposed to be the images of B3's own generators).
DVBBraidHolds := (DVBS1*DVBS2*DVBS1 = DVBS2*DVBS1*DVBS2);;
Print("DVB_BRAID_RELATION_HOLDS=", DVBBraidHolds, "\n");;
if not DVBBraidHolds then Error("DVB: braid relation FAILS on export-direct sigma1/sigma2 -- fail-closed stop"); fi;;

DVBBuildT0 := GAPLIB_WallElapsedMs();;
DVBDeg := 192;;
DVBX := DVBS1^2;; DVBY := DVBS2^2;; DVBC := (DVBS1*DVBS2*DVBS1)^2;;
DVBQp := Group(DVBS1, DVBS2);;
DVBCinK := (DVBC = Identity(DVBQp));;

DVBJX := DCP3DirectSumPerm(DCP3MX, DCP3MDegree, DVBX, DVBDeg);;
DVBJY := DCP3DirectSumPerm(DCP3MY, DCP3MDegree, DVBY, DVBDeg);;
DVBJC := DCP3DirectSumPerm(DCP3JCM, DCP3MDegree, DVBC, DVBDeg);;
DVBG := Group(DVBJX, DVBJY);;
DVBA := Group(DVBJX, DVBJY, DVBJC);;
DVBSizeG := Size(DVBG);;
DVBBuildElapsed := GAPLIB_WallElapsedMs() - DVBBuildT0;;
Print("DVB_BUILD size_G=", DVBSizeG, " (expect 141087744) build_ms=", DVBBuildElapsed, "\n");;
if DVBSizeG <> 141087744 then Error("DVB: |G| drift from expected 141,087,744"); fi;;

DVBKord := Lcm(Order(DVBJX), Order(DVBJY));;
if DVBKord mod 18 <> 0 then Error("DVB: K_ord not divisible by 18"); fi;;
DVBF1 := DVBKord/18;;
DVBF2 := DVBSizeG/1469664;;
DVBF3 := DVBF1*DVBF2;;
Print("DVB_BUDGET K_ord=", DVBKord, " F1=", DVBF1, " F2=", DVBF2, " F3(fib)=", DVBF3,
  " c_in_K=", DVBCinK, "\n");;

DVBPi0 := GroupHomomorphismByImages(DVBG, DCP3MBlock, [DVBJX,DVBJY], [DCP3MX,DCP3MY]);;
if DVBPi0 = fail then Error("DVB: pi0 ill-defined"); fi;;
DVBH := Kernel(DVBPi0);;
if Size(DVBH) <> DVBF2 then Error("DVB: |H| mismatch"); fi;;

DVBThetaHom := GroupHomomorphismByImages(DVBA, DVBA, [DVBJX,DVBJY,DVBJC], [DVBJY,DVBJX,DVBJC]);;
DVBTauHom := GroupHomomorphismByImages(DVBA, DVBA, [DVBJX,DVBJY,DVBJC], [DVBJY, DVBJY^-1*DVBJX^-1*DVBJC, DVBJC]);;
Print("DVB_THETA_WD=", DVBThetaHom<>fail, " TAU_WD=", DVBTauHom<>fail,
  " full_build_ms=", GAPLIB_WallElapsedMs()-DVBBuildT0, "\n");;

## warmup: one full row36 evaluation
DVBSeed := DCP3Seeds[1];;
DVBWarmT0 := GAPLIB_WallElapsedMs();;
DVBD := DerivedSubgroup(DVBG);;
DVBDerivedMs := GAPLIB_WallElapsedMs() - DVBWarmT0;;
Print("DVB_DERIVED_SUBGROUP_ORDER=", Size(DVBD), " derived_ms=", DVBDerivedMs, "\n");;

DVBJFseed := DCP3EvalWord(DVBSeed.letters, DVBJX, DVBJY, Identity(DVBG));;
DVBTarget0 := Image(DVBPi0, DVBJFseed);;
if DVBSeed.m_target_pinned <> DVBTarget0 then
  Print("DVB_REDUCTION_NOTE target mismatch (expected for a window that may not reduce to g* -- not fail-closed here, informational for a cost probe)\n");;
fi;;

DVBHlist := Elements(DVBH);;
DVBCosetMs := GAPLIB_WallElapsedMs() - DVBWarmT0;;
Print("DVB_COSET_SIZE=", Length(DVBHlist), " coset_build_ms=", DVBCosetMs, "\n");;

## time a handful of individual candidate predicate evaluations (not all F3,
## which could be large -- F3 itself printed above for reference)
DVBSampleCount := Minimum(10, Length(DVBHlist));;
DVBPerCandStart := GAPLIB_WallElapsedMs();;
DVBSampleValid := 0;;
for DVBi in [1..DVBSampleCount] do
  DVBp := DVBJFseed * DVBHlist[DVBi];;
  DVBm := 0;;
  DVBu := 2*DVBm+1;;
  DVBokCm := Gcd(DVBu, DVBKord) = 1;;
  DVBokCf := DVBp in DVBD;;
  if DVBokCm and DVBokCf then
    DVBhex310 := (DVBp * Image(DVBThetaHom, DVBp) = Identity(DVBA));;
    if DVBhex310 then
      DVBymf := DVBJY^DVBm * DVBp;;
      DVBlhsF2 := Image(DVBTauHom, Image(DVBTauHom, DVBymf)) * Image(DVBTauHom, DVBymf) * DVBymf;;
      DVBhex311 := (DVBlhsF2 = DVBJC^DVBm);;
      if DVBhex311 then
        DVBgenA := DVBJX^DVBu;; DVBgenB := DVBp^-1 * DVBJY^DVBu * DVBp;;
        if Size(Group(DVBgenA,DVBgenB)) = DVBSizeG then DVBSampleValid := DVBSampleValid+1; fi;;
      fi;;
    fi;;
  fi;;
od;;
DVBPerCandElapsed := GAPLIB_WallElapsedMs() - DVBPerCandStart;;
DVBPerCandAvg := DVBPerCandElapsed / DVBSampleCount;;
Print("DVB_SAMPLE_PREDICATE sample_count=", DVBSampleCount,
  " total_ms=", DVBPerCandElapsed, " avg_ms_per_candidate=", DVBPerCandAvg,
  " sample_valid=", DVBSampleValid, "\n");;

DVBWarmupTotal := GAPLIB_WallElapsedMs() - DVBWarmT0;;
Print("DVB_WARMUP_TOTAL_ms=", DVBWarmupTotal, "\n");;

DVBMem := GasmanStatistics();;
Print("DVB_MEM ", DVBMem, "\n");;

DVBTotalElapsed := GAPLIB_WallElapsedMs() - DVBT0;;
Print("DVB_TOTAL_ELAPSED_MS=", DVBTotalElapsed, "\n");;

DVBOutput := Concatenation(
  "{\n  \"schema\":\"drophunt-venue-stage0b-export-direct/v1\",\n",
  "  \"method\":\"sigma1/sigma2 read directly from the LINS marked-strictness export artifact, no new LowIndexNormalSubgroupsSearch call\",\n",
  "  \"target_node_id\":\"064fd39d5e9070c3...\",\n",
  "  \"target_b3_index\":192,\n",
  "  \"braid_relation_holds\":", JB(DVBBraidHolds), ",\n",
  "  \"size_G\":", String(DVBSizeG), ",\n",
  "  \"K_ord\":", String(DVBKord), ",\n",
  "  \"F1\":", String(DVBF1), ",\n",
  "  \"F2\":", String(DVBF2), ",\n",
  "  \"F3_fib\":", String(DVBF3), ",\n",
  "  \"c_in_K\":", JB(DVBCinK), ",\n",
  "  \"theta_welldefined\":", JB(DVBThetaHom<>fail), ",\n",
  "  \"tau_welldefined\":", JB(DVBTauHom<>fail), ",\n",
  "  \"stage0b_4_numbers\":{\n",
  "    \"i_window_build_ms\":", String(DVBBuildElapsed), ",\n",
  "    \"ii_warmup_ms\":", String(DVBWarmupTotal), ",\n",
  "    \"iii_per_candidate_ms_approx\":", String(DVBPerCandAvg), ",\n",
  "    \"iv_gasman_stats_raw\":", JStr(String(DVBMem)), "\n",
  "  },\n",
  "  \"total_elapsed_ms\":", String(DVBTotalElapsed), "\n}\n");;
WriteFile("search/certs/drophunt_venue_stage0b_v1_20260828.json", DVBOutput);;
Print("DVB_OUTPUT path=search/certs/drophunt_venue_stage0b_v1_20260828.json\n");;
Print("ALL_DONE\n");;
