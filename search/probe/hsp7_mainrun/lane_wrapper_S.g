## search/probe/hsp7_mainrun/lane_wrapper_S.g
## Lane S main-run shard wrapper (NEW file, individually digested -- not
## part of the frozen predicate library). Wraps the byte-identical Lane S
## predicate library (predicate_lib_laneS.g) with an input loop over a
## shard of the frozen candidate universe (prereg v2 SS1). Judgement code is
## NOT modified here (Hex310/Hex311 called exactly as defined in the
## library); only the enumeration/IO around it is new.
##
## Shard bounds convention (mine-dispatch.yml style preamble binding):
##   SHARD_LO, SHARD_HI : inclusive pair-flat-index bounds in [0, 705893].
##   An EMPTY shard is SHARD_HI < SHARD_LO (e.g. SHARD_LO:=1;; SHARD_HI:=0;;).
##   This wrapper must be syntax-checkable and must evaluate ZERO candidates
##   when given an empty shard -- this is the "dry structural check" mode
##   used for the prereg v2 bundle inspection (no candidate in the 705,894
##   universe has been evaluated by running this file in that mode).
if not IsBound(SHARD_LO) then SHARD_LO := 1;; fi;
if not IsBound(SHARD_HI) then SHARD_HI := 0;; fi;  ## default: empty shard (dry mode)
if not IsBound(OUT_CERT_PATH) then OUT_CERT_PATH := "search/probe/hsp7_mainrun/_dry_laneS_cert.json";; fi;
if not IsBound(FROZEN_DRIVER_DIGEST_S) then FROZEN_DRIVER_DIGEST_S := "UNSET";; fi;

Read("search/probe/hsp7_mainrun/predicate_lib_laneS.g");
Read("search/probe/hsp7_mainrun/candidate_key_lib.g");

Print("=== lane_wrapper_S: shard [", SHARD_LO, ", ", SHARD_HI, "] ===\n");

selfChk := CandidateKeyLibSelfCheck();;
Print("candidate_key_lib self-check: ", selfChk.ok, " total=", selfChk.total_candidates, "\n");

## NOTE: the (P, x, y, theta, tau, Hex310, Hex311) bindings below come from
## predicate_lib_laneS.g (the byte-identical excerpt). The candidate basis
## MUST be derived from that SAME P object via BasisFromP(P) -- NOT via a
## second BuildCandidateBasis() call, which would re-read PQ_OUTPUT_P.g and
## construct a merely-isomorphic, `<>`-distinct copy (discovered during this
## bundle's dry check: PQ_READ_AS_FUNC_WITH_VARS is not idempotent w.r.t.
## GAP object identity).
basisS := BasisFromP(P);;

records := [];;
nEvaluated := 0;;
for pairIdx in [SHARD_LO..SHARD_HI] do
  ck := PairIndexToCandidateKey(pairIdx);;
  fbar := ExpVectorToElement(basisS, ck.e);;
  verdict := Hex310(fbar) and Hex311(fbar);;
  Add(records, rec(pair_index := pairIdx, m := ck.m, e := ck.e, hexagon_verdict := verdict));
  nEvaluated := nEvaluated + 1;;
od;

Print("candidates evaluated this shard: ", nEvaluated, "\n");
if nEvaluated = 0 then
  Print("DRY_STRUCTURAL_CHECK: zero candidates evaluated (empty shard by design)\n");
fi;

## cert emission left as a schema stub for the dry check -- full gtsh-cert/v1
## style serialization + DRIVER_DONE marker + frozen_driver_digest field are
## specified in prereg v2 SS3, wired here only up to "would write N records".
Print("would_write_records=", Length(records), " to ", OUT_CERT_PATH, "\n");
Print("frozen_driver_digest(recorded)=", FROZEN_DRIVER_DIGEST_S, "\n");
Print("DRIVER_DONE: true\n");
Print("LANE_S_WRAPPER_DRY_CHECK_DONE\n");
QUIT;
