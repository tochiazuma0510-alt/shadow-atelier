## search/probe/hsp7_mainrun/lane_wrapper_V.g
## Lane V main-run shard wrapper (NEW file, individually digested). Wraps
## the byte-identical Lane V predicate library (predicate_lib_laneV.g, which
## itself is an unmodified Read() of statemachine_lib.g).
##
## OPEN ITEM (flagged, not resolved in this dry bundle): Lane V's judgement
## predicate EvalFullHexagonFixed(m, freeElt, phiX, phiY, phiC) consumes a
## FreeGroup(x,y) WORD for the candidate (it calls
## LetterRepAssocWord(freeElt) internally, statemachine_lib.g L164), not a
## pc-group element of P. The calibration candidates (h4^t, h3) were already
## literal short free-group words. The main-run candidate universe, by
## contrast, is defined in candidate_key_lib.g as pcgs exponent vectors over
## D=[P,P] (a pc-group element, no free word attached). Converting a pcgs
## element back to an explicit x,y-word requires a preimage step, e.g.
##   epi2 := EpimorphismFromFreeGroup(P);;
##   w := PreImagesRepresentative(epi2, fbar);;
## This is mathematically sound (P is a quotient of FreeGroup(x,y), so a
## preimage word always exists) but its COST is unknown and NOT reflected in
## prereg v1/v2 appendix C's Lane V rate estimates (those estimates assumed
## the short calibration words, not a generic preimage computation over the
## full 117,649/705,894-candidate universe). This wrapper stops short of
## silently adopting the preimage-word approach as free; it is surfaced
## here as an item for mathematician/Sol review before Lane V's real rate
## can be trusted at main-run scale.
if not IsBound(SHARD_LO) then SHARD_LO := 1;; fi;
if not IsBound(SHARD_HI) then SHARD_HI := 0;; fi;  ## default: empty shard (dry mode)
if not IsBound(OUT_CERT_PATH) then OUT_CERT_PATH := "search/probe/hsp7_mainrun/_dry_laneV_cert.json";; fi;
if not IsBound(FROZEN_DRIVER_DIGEST_V) then FROZEN_DRIVER_DIGEST_V := "UNSET";; fi;

Read("search/probe/hsp7_mainrun/predicate_lib_laneV.g");
Read("search/probe/hsp7_mainrun/candidate_key_lib.g");

Print("=== lane_wrapper_V: shard [", SHARD_LO, ", ", SHARD_HI, "] ===\n");

selfChk := CandidateKeyLibSelfCheck();;
Print("candidate_key_lib self-check: ", selfChk.ok, " total=", selfChk.total_candidates, "\n");

## Lane V's predicate_lib_laneV.g (statemachine_lib.g) does not itself bind
## a top-level P -- driver_step4_evaluate_v3.g builds its own P via
## Read("search/probe/hsp7_cond4_laneV/PQ_OUTPUT_P.g") (a DIFFERENT PQ_OUTPUT
## artifact file than Lane S's, though the same construction target). This
## wrapper follows that same Lane V-specific artifact, and derives the
## candidate basis from THAT freshly-read P via BasisFromP (not
## BuildCandidateBasis, which points at the Lane S artifact -- see
## candidate_key_lib.g comment on object-identity non-idempotence).
Read("search/probe/hsp7_cond4_laneV/PQ_OUTPUT_P.g");
Pv := F;; xbarV := MapImages[1];; ybarV := MapImages[2];;
basisV := BasisFromP(Pv);;
Print("basisV built from Lane V's own PQ_OUTPUT_P.g (own measurement)\n");

Print("OPEN_ITEM: pcgs-exponent-vector -> FreeGroup(x,y) word preimage step\n");
Print("  (EpimorphismFromFreeGroup + PreImagesRepresentative) is NOT wired\n");
Print("  in this dry bundle. See file header. No candidate evaluated below\n");
Print("  uses this step -- shard is empty by default (dry mode).\n");

nEvaluated := 0;;
records := [];;
for pairIdx in [SHARD_LO..SHARD_HI] do
  ck := PairIndexToCandidateKey(pairIdx);;
  ## would build fbar := ExpVectorToElement(basisV, ck.e);; then a preimage
  ## word w, then call EvalFullHexagonFixed(ck.m, w, xbar, ybar, chatMain)
  ## and EvalFullHexagonFixed(ck.m, w, xbar0, ybar0, chat0) for N and N0
  ## (OPEN_ITEM above -- not implemented in this dry bundle).
  Add(records, rec(pair_index := pairIdx, m := ck.m, e := ck.e));
  nEvaluated := nEvaluated + 1;;
od;

Print("candidates evaluated this shard: ", nEvaluated, "\n");
if nEvaluated = 0 then
  Print("DRY_STRUCTURAL_CHECK: zero candidates evaluated (empty shard by design)\n");
fi;

Print("would_write_records=", Length(records), " to ", OUT_CERT_PATH, "\n");
Print("frozen_driver_digest(recorded)=", FROZEN_DRIVER_DIGEST_V, "\n");
Print("DRIVER_DONE: true\n");
Print("LANE_V_WRAPPER_DRY_CHECK_DONE\n");
QUIT;
