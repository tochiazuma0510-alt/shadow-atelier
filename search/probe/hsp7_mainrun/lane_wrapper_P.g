## HS main-run Lane P wrapper, runnable certificate-emitting CONV-P version.
## The PENT predicate is independent of m, so the wrapper evaluates each
## f-index once and emits the independently checkable six pair-key expansion.

if not IsBound(RUN_MODE) then Error("LANE_P_STOP: RUN_MODE must be BASIS_ONLY, SHARD, or REGISTERED"); fi;
if RUN_MODE = "BASIS_ONLY" then
  if not IsBound(OUT_BASIS_PATH) then Error("LANE_P_STOP: OUT_BASIS_PATH is required"); fi;
elif not IsBound(OUT_CERT_PATH) then Error("LANE_P_STOP: OUT_CERT_PATH is required"); fi;
if not IsBound(CLASS_ID) then CLASS_ID := "UNSET"; fi;
if not IsBound(RUN_ID) then RUN_ID := "UNSET"; fi;
if not IsBound(RUN_ATTEMPT) then RUN_ATTEMPT := "UNSET"; fi;
if not IsBound(COMMIT_SHA) then COMMIT_SHA := "UNSET"; fi;
if not IsBound(SOURCE_BUNDLE_SHA256) then SOURCE_BUNDLE_SHA256 := "UNSET"; fi;
if not IsBound(WRAPPER_SHA256) then WRAPPER_SHA256 := "UNSET"; fi;
if not IsBound(PREDICATE_SHA256) then PREDICATE_SHA256 := "UNSET"; fi;
if not IsBound(AUX_SHA256) then AUX_SHA256 := "UNSET"; fi;
if not IsBound(SCHEMA_SHA256) then SCHEMA_SHA256 := "UNSET"; fi;
if not IsBound(PCGS_BASIS_FINGERPRINT) then PCGS_BASIS_FINGERPRINT := "UNSET"; fi;
if not IsBound(PCGS_SOURCE_ARTIFACT_PATH) then PCGS_SOURCE_ARTIFACT_PATH := "UNSET"; fi;
if not IsBound(PCGS_SOURCE_ARTIFACT_SHA256) then PCGS_SOURCE_ARTIFACT_SHA256 := "UNSET"; fi;

Read("search/probe/hsp7_mainrun/predicate_lib_laneP.g");
Read("search/probe/hsp7_mainrun/predicate_lib_laneP_conv.g");
Read("search/probe/hsp7_mainrun/candidate_key_lib.g");
Read("search/probe/hsp7_mainrun/cert_io.g");

if not CandidateKeyLibSelfCheck().ok then Error("LANE_P_STOP: key self-check failed"); fi;
epiChecked := GroupHomomorphismByImages(K05fp, Qgrp, gK, mapImages);;
if epiChecked = fail or not IsSurjective(epiChecked) or Image(epiChecked) <> Qgrp then
  Error("LANE_P_STOP: K05fp -> Q epi failed well-defined/surjective/image gate");
fi;
if sizeQ <> 7^40 or gamma5size <> 1 or dimGamma4 <> 21 then
  Error("LANE_P_STOP: Q structural anchors differ from frozen values");
fi;
if not IsBijective(rhoQ) then Error("LANE_P_STOP: rhoQ is not bijective"); fi;
rhoQ5Gate := rhoQ*rhoQ*rhoQ*rhoQ*rhoQ;;
if not ForAll(epiGens, gg -> ImageElm(rhoQ5Gate,gg)=gg) then
  Error("LANE_P_STOP: rhoQ^5 is not identity on the generating image");
fi;
if not ForAny(epiGens, gg -> ImageElm(rhoQ,gg)<>gg) then
  Error("LANE_P_STOP: rhoQ unexpectedly equals identity");
fi;
dataP := PQ_READ_AS_FUNC_WITH_VARS("search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g", ["F","MapImages"]);;
Pmain := dataP.F;; xmain := dataP.MapImages[1];; ymain := dataP.MapImages[2];;
basisP := BasisFromP(Pmain);;
if not CandidateBasisSemanticSelfCheck(basisP).ok then
  Error("LANE_P_STOP: group-level candidate-key semantic gate failed");
fi;
thetaP := GroupHomomorphismByImages(Pmain, Pmain, [xmain,ymain], [ymain,xmain]);;
tauP := GroupHomomorphismByImages(Pmain, Pmain, [xmain,ymain], [ymain,(xmain*ymain)^-1]);;
basisMaterialP := BuildCandidateBasisMaterial(basisP, xmain, ymain, thetaP, tauP, fail,
  PCGS_SOURCE_ARTIFACT_PATH, PCGS_SOURCE_ARTIFACT_SHA256);;
if RUN_MODE = "BASIS_ONLY" then
  WriteCandidateBasisMaterial(OUT_BASIS_PATH, basisMaterialP);;
  Print("PCGS_BASIS_MATERIAL_WRITTEN: ", OUT_BASIS_PATH, "\n");
  QuitGap(0);
fi;
convP := BuildConvP(Pmain, xmain, ymain, jx, jy, epiChecked);;
if not convP.image_generated or not convP.image_bijective then
  Error("LANE_P_STOP: CONV-P map image/bijectivity gate did not pass");
fi;

MakeLanePCandidate := function(fbar, nativeQ, fixtureId)
  local e, fidx;
  e := ExponentsOfPcElement(basisP.pcgsD, fbar);
  if e = fail then Error("LANE_P_STOP: candidate not in D=[P,P]"); fi;
  fidx := ExpVectorToFIndex(e);
  return rec(fbar := fbar, e := e, f_index := fidx,
             nativeQ := nativeQ, fixture_id := fixtureId);
end;;

candidates := [];;
if RUN_MODE = "SHARD" then
  if not IsBound(SHARD_LO_F) or not IsBound(SHARD_HI_F) then
    Error("LANE_P_STOP: SHARD_LO_F/SHARD_HI_F required in SHARD mode");
  fi;
  if SHARD_LO_F < 0 or SHARD_HI_F > 117648 or SHARD_HI_F < SHARD_LO_F then
    Error("LANE_P_STOP: shard must be a nonempty inclusive subrange of [0,117648]");
  fi;
  for fIdx in [SHARD_LO_F..SHARD_HI_F] do
    ee := FIndexToExpVector(fIdx);;
    Add(candidates, rec(fbar := ExpVectorToElement(basisP, ee), e := ee,
      f_index := fIdx, nativeQ := fail, fixture_id := "main"));
  od;
  certLo := SHARD_LO_F;; certHi := SHARD_HI_F;;
elif RUN_MODE = "REGISTERED" then
  h4p := Comm(Comm(Comm(xmain,ymain),xmain),xmain)
         * Comm(Comm(Comm(xmain,ymain),xmain),ymain)^4
         * Comm(Comm(Comm(xmain,ymain),ymain),ymain);;
  h3p := Comm(Comm(xmain,ymain),xmain) * Comm(Comm(xmain,ymain),ymain);;
  for t in [0..6] do
    Add(candidates, MakeLanePCandidate(h4p^t, jh4Q^t,
      Concatenation("h4t", String(t))));
  od;
  Add(candidates, MakeLanePCandidate(h3p, jh3Q, "h3"));
  certLo := -1;; certHi := -1;;
else
  Error("LANE_P_STOP: RUN_MODE must be SHARD or REGISTERED");
fi;

out := HSOpenCert(OUT_CERT_PATH, "P", "f", 117649, certLo, certHi,
  CLASS_ID, RUN_ID, RUN_ATTEMPT, COMMIT_SHA, SOURCE_BUNDLE_SHA256,
  WRAPPER_SHA256, PREDICATE_SHA256, AUX_SHA256, SCHEMA_SHA256,
  CandidateBasisMaterialJson(basisMaterialP), PCGS_BASIS_FINGERPRINT);;
first := true;; n := 0;;
for cnd in candidates do
  fQ := ConvPElement(convP, cnd.fbar);;
  vv := PENT(fQ);;
  nativeAgree := true;; nativeVerdictAgree := true;;
  if RUN_MODE = "REGISTERED" then
    nativeAgree := (fQ = cnd.nativeQ);;
    nativeVerdictAgree := (vv = PENT(cnd.nativeQ));;
    if not nativeAgree or not nativeVerdictAgree then
      Error("LANE_P_INTEGRITY_STOP: CONV-P/native mismatch at ", cnd.fixture_id);
    fi;
  fi;
  six := FIndexToSixPairIndices(cnd.f_index);;
  row := Concatenation(
    "{\"f_index\":", String(cnd.f_index),
    ",\"f_key\":{\"e\":", HSJsonIntList(cnd.e), "}",
    ",\"joined_pair_indices\":", HSJsonIntList(six),
    ",\"fixture_id\":", HSJsonQuote(cnd.fixture_id),
    ",\"pentagon_verdict\":", HSJsonBool(vv),
    ",\"CONV_native_element_agree\":", HSJsonBool(nativeAgree),
    ",\"CONV_native_verdict_agree\":", HSJsonBool(nativeVerdictAgree), "}");;
  HSCertWriteRecord(out, first, row);; first := false;; n := n + 1;;
od;
HSCloseCert(out, n, 0, true, true);;
Print("CERT_WRITTEN: ", OUT_CERT_PATH, " records=", n, "\n");
Print("DRIVER_DONE: true\n");
QUIT;
