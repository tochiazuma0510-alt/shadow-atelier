## HS main-run Lane S wrapper, runnable certificate-emitting version.
## Lane S evaluates reduced hexagons (3.10) and (3.11) in P.  In particular
## (3.11) is evaluated on y^m*f; the old dry stub accidentally evaluated only
## the m=0 specialization and was therefore unusable for five sixths of the
## registered m-range.

if not IsBound(RUN_MODE) then Error("LANE_S_STOP: RUN_MODE must be BASIS_ONLY, SHARD, or REGISTERED"); fi;
if RUN_MODE = "BASIS_ONLY" then
  if not IsBound(OUT_BASIS_PATH) then Error("LANE_S_STOP: OUT_BASIS_PATH is required"); fi;
elif not IsBound(OUT_CERT_PATH) then Error("LANE_S_STOP: OUT_CERT_PATH is required"); fi;
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

Read("search/probe/hsp7_mainrun/predicate_lib_laneS.g");
Read("search/probe/hsp7_mainrun/candidate_key_lib.g");
Read("search/probe/hsp7_mainrun/cert_io.g");

if not CandidateKeyLibSelfCheck().ok then Error("LANE_S_STOP: key self-check failed"); fi;
basisS := BasisFromP(P);;
if not CandidateBasisSemanticSelfCheck(basisS).ok then
  Error("LANE_S_STOP: group-level candidate-key semantic gate failed");
fi;
if theta = fail or tau = fail or not IsBijective(theta) or not IsBijective(tau) then
  Error("LANE_S_STOP: theta/tau failed explicit well-defined+bijection gate");
fi;
basisMaterialS := BuildCandidateBasisMaterial(basisS, x, y, theta, tau, fail,
  PCGS_SOURCE_ARTIFACT_PATH, PCGS_SOURCE_ARTIFACT_SHA256);;
if RUN_MODE = "BASIS_ONLY" then
  WriteCandidateBasisMaterial(OUT_BASIS_PATH, basisMaterialS);;
  Print("PCGS_BASIS_MATERIAL_WRITTEN: ", OUT_BASIS_PATH, "\n");
  QUIT;
fi;

EvalLaneS := function(m, fbar)
  local ymf, tf, t2f, h310, h311;
  h310 := (fbar * ImageElm(theta, fbar) = One(P));
  ymf := y^m * fbar;
  tf := ImageElm(tau, ymf);
  t2f := ImageElm(tau, tf);
  h311 := (t2f * tf * ymf = One(P));
  return rec(hex310 := h310, hex311 := h311, verdict := h310 and h311);
end;;

MakeLaneSCandidate := function(m, fbar, fixtureId)
  local e, fidx, pidx;
  e := ExponentsOfPcElement(basisS.pcgsD, fbar);
  if e = fail then Error("LANE_S_STOP: candidate not in D=[P,P]"); fi;
  fidx := ExpVectorToFIndex(e);
  pidx := CandidateKeyToPairIndex(m, e);
  return rec(m := m, fbar := fbar, e := e, f_index := fidx,
             pair_index := pidx, fixture_id := fixtureId);
end;;

candidates := [];;
if RUN_MODE = "SHARD" then
  if not IsBound(SHARD_LO) or not IsBound(SHARD_HI) then
    Error("LANE_S_STOP: SHARD_LO/SHARD_HI required in SHARD mode");
  fi;
  if SHARD_LO < 0 or SHARD_HI > 705893 or SHARD_HI < SHARD_LO then
    Error("LANE_S_STOP: shard must be a nonempty inclusive subrange of [0,705893]");
  fi;
  for pairIdx in [SHARD_LO..SHARD_HI] do
    ck := PairIndexToCandidateKey(pairIdx);;
    Add(candidates, rec(m := ck.m,
      fbar := ExpVectorToElement(basisS, ck.e), e := ck.e,
      f_index := ck.f_index, pair_index := pairIdx, fixture_id := "main"));
  od;
  certLo := SHARD_LO;; certHi := SHARD_HI;;
elif RUN_MODE = "REGISTERED" then
  ## Exactly the registered 13 Lane-V/hexagon fixtures: h4^0..6 and h3 at
  ## m=0, followed by f=1 at m=1,2,4,5,6.  No unregistered/main key is read.
  for t in [0..6] do
    Add(candidates, MakeLaneSCandidate(0, h4^t, Concatenation("h4t", String(t))));
  od;
  Add(candidates, MakeLaneSCandidate(0, h3, "h3"));
  for mm in [1,2,4,5,6] do
    Add(candidates, MakeLaneSCandidate(mm, One(P), Concatenation("one-m", String(mm))));
  od;
  certLo := -1;; certHi := -1;;
else
  Error("LANE_S_STOP: RUN_MODE must be SHARD or REGISTERED");
fi;

out := HSOpenCert(OUT_CERT_PATH, "S", "pair", 705894, certLo, certHi,
  CLASS_ID, RUN_ID, RUN_ATTEMPT, COMMIT_SHA, SOURCE_BUNDLE_SHA256,
  WRAPPER_SHA256, PREDICATE_SHA256, AUX_SHA256, SCHEMA_SHA256,
  CandidateBasisMaterialJson(basisMaterialS), PCGS_BASIS_FINGERPRINT);;
first := true;; n := 0;;
for cnd in candidates do
  rr := EvalLaneS(cnd.m, cnd.fbar);;
  row := Concatenation(
    "{\"pair_index\":", String(cnd.pair_index),
    ",\"f_index\":", String(cnd.f_index),
    ",\"candidate_key\":{\"m\":", String(cnd.m), ",\"e\":", HSJsonIntList(cnd.e), "}",
    ",\"fixture_id\":", HSJsonQuote(cnd.fixture_id),
    ",\"hex310\":", HSJsonBool(rr.hex310),
    ",\"hex311\":", HSJsonBool(rr.hex311),
    ",\"verdict\":", HSJsonBool(rr.verdict), "}");;
  HSCertWriteRecord(out, first, row);; first := false;; n := n + 1;;
od;
HSCloseCert(out, n, 0, true, true);;
Print("CERT_WRITTEN: ", OUT_CERT_PATH, " records=", n, "\n");
Print("DRIVER_DONE: true\n");
QUIT;
