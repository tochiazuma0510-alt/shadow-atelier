## HS main-run Lane V wrapper, runnable certificate-emitting CF version.
## It evaluates full (3.3)/(3.4) on both N and N0 with the closed-form
## predicate.  Candidate elements never pass through a word-preimage loop.

if not IsBound(RUN_MODE) then Error("LANE_V_STOP: RUN_MODE must be BASIS_ONLY, SHARD, or REGISTERED"); fi;
if RUN_MODE = "BASIS_ONLY" then
  if not IsBound(OUT_BASIS_PATH) then Error("LANE_V_STOP: OUT_BASIS_PATH is required"); fi;
elif not IsBound(OUT_CERT_PATH) then Error("LANE_V_STOP: OUT_CERT_PATH is required"); fi;
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

Read("search/probe/hsp7_mainrun/predicate_lib_laneV_cf.g");
Read("search/probe/hsp7_mainrun/candidate_key_lib.g");
Read("search/probe/hsp7_mainrun/cert_io.g");

cfToyMain := SelfTestCF_Main();;
cfToyControl := SelfTestCF_Control();;
if not cfToyMain.ok or cfToyMain.mismatches <> 0 or
   not cfToyControl.ok or cfToyControl.mismatches <> 0 then
  Error("LANE_V_STOP: CF literal toy regression gate failed");
fi;
if RUN_MODE = "REGISTERED" then
  ## The registered gate is explicitly two-path.  Production SHARD mode uses
  ## CF only; REGISTERED mode additionally loads the frozen state-machine
  ## baseline and compares each named fixture field by field.
  Read("search/probe/hsp7_mainrun/predicate_lib_laneV.g");
  baselineToy := TestToyFixtureLiteralVsFixed();;
  baselineToyExt := TestToyFixtureExtended();;
  if not baselineToy.ok or baselineToy.mismatches <> 0 or
     not baselineToyExt.ok or baselineToyExt.mismatches <> 0 then
    Error("LANE_V_STOP: baseline literal toy regression gate failed");
  fi;
fi;

if not CandidateKeyLibSelfCheck().ok then Error("LANE_V_STOP: key self-check failed"); fi;

## Build the Lane-V P and independently pin it to the authoritative Lane-S
## semantic basis.  Merely taking Pcgs(D) in two isomorphic GAP objects is
## not enough: the generator-by-generator image equality below is the gate
## that makes one exponent tuple mean the same element in both lanes.
dataV := PQ_READ_AS_FUNC_WITH_VARS("search/probe/hsp7_cond4_laneV/PQ_OUTPUT_P.g", ["F","MapImages"]);;
Pv := dataV.F;; xv := dataV.MapImages[1];; yv := dataV.MapImages[2];;
basisV := BasisFromP(Pv);;
if not CandidateBasisSemanticSelfCheck(basisV).ok then
  Error("LANE_V_STOP: group-level candidate-key semantic gate failed");
fi;
dataSmap := PQ_READ_AS_FUNC_WITH_VARS("search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g", ["F","MapImages"]);;
PsMap := dataSmap.F;; xsMap := dataSmap.MapImages[1];; ysMap := dataSmap.MapImages[2];;
basisSMap := BasisFromP(PsMap);;
if not CandidateBasisSemanticSelfCheck(basisSMap).ok then
  Error("LANE_V_STOP: authoritative Lane-S basis semantic gate failed");
fi;
svMap := GroupHomomorphismByImages(PsMap, Pv, [xsMap,ysMap], [xv,yv]);;
if svMap = fail or not IsBijective(svMap) then
  Error("LANE_V_STOP: authoritative Lane-S -> Lane-V generator map is not bijective");
fi;
if Image(svMap) <> Pv then Error("LANE_V_STOP: S->V map image does not generate Pv"); fi;
for ii in [1..6] do
  if ImageElm(svMap, basisSMap.gens[ii]) <> basisV.gens[ii] then
    Error("LANE_V_STOP: pcgs semantic basis mismatch at generator ", ii);
  fi;
od;

thetaV := GroupHomomorphismByImages(Pv, Pv, [xv,yv], [yv,xv]);;
tauV := GroupHomomorphismByImages(Pv, Pv, [xv,yv], [yv,(xv*yv)^-1]);;
thetaSMap := GroupHomomorphismByImages(PsMap, PsMap, [xsMap,ysMap], [ysMap,xsMap]);;
tauSMap := GroupHomomorphismByImages(PsMap, PsMap, [xsMap,ysMap], [ysMap,(xsMap*ysMap)^-1]);;
basisMaterialSMap := BuildCandidateBasisMaterial(basisSMap, xsMap, ysMap,
  thetaSMap, tauSMap, fail, PCGS_SOURCE_ARTIFACT_PATH,
  PCGS_SOURCE_ARTIFACT_SHA256);;
basisMaterialV := BuildCandidateBasisMaterial(basisV, xv, yv, thetaV, tauV,
  rec(source_basis := basisSMap, map := svMap), PCGS_SOURCE_ARTIFACT_PATH,
  PCGS_SOURCE_ARTIFACT_SHA256);;
if basisMaterialSMap.relative_orders <> basisMaterialV.relative_orders or
   basisMaterialSMap.pair_commutator_coordinates <> basisMaterialV.pair_commutator_coordinates or
   basisMaterialSMap.theta_image_coordinates <> basisMaterialV.theta_image_coordinates or
   basisMaterialSMap.tau_image_coordinates <> basisMaterialV.tau_image_coordinates then
  Error("LANE_V_STOP: S->V bridge does not preserve ordered basis structure/action material");
fi;
if basisMaterialSMap.ambient_named_generator_coordinates <>
     basisMaterialV.ambient_named_generator_coordinates or
   basisMaterialSMap.ambient_pcgs_relative_orders <>
     basisMaterialV.ambient_pcgs_relative_orders or
   basisMaterialSMap.ordered_basis_in_ambient_coordinates <>
     basisMaterialV.ordered_basis_in_ambient_coordinates then
  Error("LANE_V_STOP: S->V bridge does not preserve ambient named/basis coordinates");
fi;
if RUN_MODE = "BASIS_ONLY" then
  WriteCandidateBasisMaterial(OUT_BASIS_PATH, basisMaterialV);;
  Print("PCGS_BASIS_MATERIAL_WRITTEN: ", OUT_BASIS_PATH, "\n");
  QuitGap(0);
fi;

C7V := CyclicGroup(IsPcGroup, 7);;
gcv := GeneratorsOfGroup(C7V)[1];;
N0v := DirectProduct(Pv, C7V);;
embPv := Embedding(N0v, 1);; embCv := Embedding(N0v, 2);;
x0v := Image(embPv, xv);; y0v := Image(embPv, yv);; c0v := Image(embCv, gcv);;
cNv := One(Pv);;

autosN := BuildHexAutos(Pv, xv, yv, cNv);;
autosN0 := BuildHexAutos(N0v, x0v, y0v, c0v);;
if not autosN.A1_bijective or not autosN.A2_bijective or
   not autosN0.A1_bijective or not autosN0.A2_bijective then
  Error("LANE_V_STOP: explicit automorphism bijectivity gate failed");
fi;
mdepsN := List(XN_ORDERED, mm -> BuildMDependent(autosN, xv, yv, cNv, mm));;
mdepsN0 := List(XN_ORDERED, mm -> BuildMDependent(autosN0, x0v, y0v, c0v, mm));;

MakeLaneVCandidate := function(m, fbar, ffree, fixtureId)
  local e, fidx, pidx;
  e := ExponentsOfPcElement(basisV.pcgsD, fbar);
  if e = fail then Error("LANE_V_STOP: candidate not in D=[P,P]"); fi;
  fidx := ExpVectorToFIndex(e);; pidx := CandidateKeyToPairIndex(m, e);;
  return rec(m := m, fbar := fbar, e := e, f_index := fidx,
             pair_index := pidx, ffree := ffree, fixture_id := fixtureId);
end;;

candidates := [];;
if RUN_MODE = "SHARD" then
  if not IsBound(SHARD_LO) or not IsBound(SHARD_HI) then
    Error("LANE_V_STOP: SHARD_LO/SHARD_HI required in SHARD mode");
  fi;
  if SHARD_LO < 0 or SHARD_HI > 705893 or SHARD_HI < SHARD_LO then
    Error("LANE_V_STOP: shard must be a nonempty inclusive subrange of [0,705893]");
  fi;
  for pairIdx in [SHARD_LO..SHARD_HI] do
    ck := PairIndexToCandidateKey(pairIdx);;
    Add(candidates, rec(m := ck.m,
      fbar := ExpVectorToElement(basisV, ck.e), e := ck.e,
      f_index := ck.f_index, pair_index := pairIdx, ffree := fail,
      fixture_id := "main"));
  od;
  certLo := SHARD_LO;; certHi := SHARD_HI;;
elif RUN_MODE = "REGISTERED" then
  h4v := Comm(Comm(Comm(xv,yv),xv),xv) * Comm(Comm(Comm(xv,yv),xv),yv)^4
         * Comm(Comm(Comm(xv,yv),yv),yv);;
  h3v := Comm(Comm(xv,yv),xv) * Comm(Comm(xv,yv),yv);;
  FreeXYV := FreeGroup("x", "y");;
  FxV := FreeXYV.1;; FyV := FreeXYV.2;;
  h4freeV := Comm(Comm(Comm(FxV,FyV),FxV),FxV)
             * Comm(Comm(Comm(FxV,FyV),FxV),FyV)^4
             * Comm(Comm(Comm(FxV,FyV),FyV),FyV);;
  h3freeV := Comm(Comm(FxV,FyV),FxV) * Comm(Comm(FxV,FyV),FyV);;
  for t in [0..6] do
    Add(candidates, MakeLaneVCandidate(0, h4v^t, h4freeV^t,
      Concatenation("h4t", String(t))));
  od;
  Add(candidates, MakeLaneVCandidate(0, h3v, h3freeV, "h3"));
  for mm in [1,2,4,5,6] do
    Add(candidates, MakeLaneVCandidate(mm, One(Pv), One(FreeXYV),
      Concatenation("one-m", String(mm))));
  od;
  certLo := -1;; certHi := -1;;
else
  Error("LANE_V_STOP: RUN_MODE must be SHARD or REGISTERED");
fi;

out := HSOpenCert(OUT_CERT_PATH, "V", "pair", 705894, certLo, certHi,
  CLASS_ID, RUN_ID, RUN_ATTEMPT, COMMIT_SHA, SOURCE_BUNDLE_SHA256,
  WRAPPER_SHA256, PREDICATE_SHA256, AUX_SHA256, SCHEMA_SHA256,
  CandidateBasisMaterialJson(basisMaterialV), PCGS_BASIS_FINGERPRINT);;
first := true;; n := 0;; mismatch := 0;;
for cnd in candidates do
  mi := Position(XN_ORDERED, cnd.m);;
  if mi = fail then Error("LANE_V_STOP: m outside registered X_N"); fi;
  rN := EvalFullHexagonCF(mdepsN[mi], autosN, cnd.fbar);;
  f0 := Image(embPv, cnd.fbar);;
  rN0 := EvalFullHexagonCF(mdepsN0[mi], autosN0, f0);;
  vN := rN.hex33 and rN.hex34;; vN0 := rN0.hex33 and rN0.hex34;;
  baselineAgree := true;;
  if RUN_MODE = "REGISTERED" then
    rbN := EvalFullHexagonFixed(cnd.m, cnd.ffree, xv, yv, cNv);;
    rbN0 := EvalFullHexagonFixed(cnd.m, cnd.ffree, x0v, y0v, c0v);;
    baselineAgree := (rbN.hex33 = rN.hex33) and (rbN.hex34 = rN.hex34)
                     and (rbN0.hex33 = rN0.hex33) and (rbN0.hex34 = rN0.hex34);;
    if not baselineAgree then
      Error("LANE_V_INTEGRITY_STOP: CF/baseline mismatch at ", cnd.fixture_id);
    fi;
  fi;
  if vN <> vN0 then mismatch := mismatch + 1; fi;
  row := Concatenation(
    "{\"pair_index\":", String(cnd.pair_index),
    ",\"f_index\":", String(cnd.f_index),
    ",\"candidate_key\":{\"m\":", String(cnd.m), ",\"e\":", HSJsonIntList(cnd.e), "}",
    ",\"fixture_id\":", HSJsonQuote(cnd.fixture_id),
    ",\"N\":{\"hex33\":", HSJsonBool(rN.hex33), ",\"hex34\":", HSJsonBool(rN.hex34),
      ",\"verdict\":", HSJsonBool(vN), "}",
    ",\"N0\":{\"hex33\":", HSJsonBool(rN0.hex33), ",\"hex34\":", HSJsonBool(rN0.hex34),
      ",\"verdict\":", HSJsonBool(vN0), "}",
    ",\"N_N0_agree\":", HSJsonBool(vN=vN0),
    ",\"CF_baseline_agree\":", HSJsonBool(baselineAgree), "}");;
  HSCertWriteRecord(out, first, row);; first := false;; n := n + 1;;
od;
HSCloseCert(out, n, 0, mismatch=0, true);;
Print("CERT_WRITTEN: ", OUT_CERT_PATH, " records=", n, " N_N0_mismatch=", mismatch, "\n");
if mismatch > 0 then Error("LANE_V_INTEGRITY_STOP: N/N0 verdict mismatch"); fi;
Print("DRIVER_DONE: true\n");
QUIT;
