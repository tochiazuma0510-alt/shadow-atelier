## search/probe/hsp7_mainrun/lane_wrapper_P.g
## Lane P main-run shard wrapper (NEW file, individually digested). Wraps
## the byte-identical Lane P predicate library (predicate_lib_laneP.g).
##
## ADOPTS Sol's accepted optimization (便104 F104-1.5, "PENT_W does not
## contain m"): this wrapper loops over F-INDEX (0..117648, the 117,649
## f-bar values), NOT over the full 705,894 pair index. PENT(fbar) is
## evaluated ONCE per f_index; the join to the 6 candidate_keys sharing
## that f_index is recorded via candidate_key_lib.g's
## FIndexToSixPairIndices(fIndex) -- the SAME formula the join checker
## (join_checker.py) uses, so lane wrapper and join checker cannot drift
## apart on the bijection.
##
## Shard bounds: SHARD_LO_F, SHARD_HI_F are inclusive f_index bounds in
## [0, 117648] (NOT pair-index bounds -- Lane P's shard axis is 6x smaller
## than Lane S/V's because of the adopted optimization). Empty shard =
## SHARD_HI_F < SHARD_LO_F (dry mode default below).
if not IsBound(SHARD_LO_F) then SHARD_LO_F := 1;; fi;
if not IsBound(SHARD_HI_F) then SHARD_HI_F := 0;; fi;  ## default: empty shard (dry mode)
if not IsBound(OUT_CERT_PATH) then OUT_CERT_PATH := "search/probe/hsp7_mainrun/_dry_laneP_cert.json";; fi;
if not IsBound(FROZEN_DRIVER_DIGEST_P) then FROZEN_DRIVER_DIGEST_P := "UNSET";; fi;

Read("search/probe/hsp7_mainrun/predicate_lib_laneP.g");
Read("search/probe/hsp7_mainrun/candidate_key_lib.g");

Print("=== lane_wrapper_P: f-index shard [", SHARD_LO_F, ", ", SHARD_HI_F, "] ===\n");

selfChk := CandidateKeyLibSelfCheck();;
Print("candidate_key_lib self-check: ", selfChk.ok, " total=", selfChk.total_candidates, "\n");

## Lane P evaluates PENT on Q = K(0,5)/W (predicate_lib_laneP.g's Qgrp), a
## DIFFERENT group from P = F2/(gamma5(F2)F2^7). The candidate f-bar for
## Lane P lives in [P,P] (per prereg v1 SS1.2's own statement "charming f-bar
## in [P,P]"), so evaluating PENT on Qgrp requires the SAME translation gap
## flagged for Lane V below: an explicit map from the P-side pcgs exponent
## vector to a Qgrp element. driver_step3_eval_pent.g's own calibration
## candidates (jh4^t, jh3) are already expressed directly as Qgrp/K05fp
## words (jx,jy = kX12,kX23), not derived from a P-side pcgs. This wrapper
## flags rather than silently invents the P->Q candidate translation:
Print("OPEN_ITEM: Lane P general f-bar (from candidate_key_lib exponent\n");
Print("  vector over Pcgs([P,P])) needs an explicit, mathematician-checked\n");
Print("  map into Qgrp/K05fp before per-candidate PENT can be evaluated for\n");
Print("  the full 117,649-element universe (calibration only covered the\n");
Print("  h4^t/h3/identity dummy family, which are already native Qgrp words).\n");
Print("  NOT resolved in this dry bundle -- see prereg v2 open items.\n");

nEvaluated := 0;;
records := [];;
for fIdx in [SHARD_LO_F..SHARD_HI_F] do
  ## would translate fIdx -> Qgrp element here (OPEN_ITEM above), then:
  ##   verdict := PENT(fbarQ);;
  ## and record the join receipt:
  sixPairIdx := FIndexToSixPairIndices(fIdx);;
  Add(records, rec(f_index := fIdx, joined_pair_indices := sixPairIdx));
  nEvaluated := nEvaluated + 1;;
od;

Print("f-values evaluated this shard: ", nEvaluated, "\n");
if nEvaluated = 0 then
  Print("DRY_STRUCTURAL_CHECK: zero f-values evaluated (empty shard by design)\n");
fi;

## join-receipt self-test (pure arithmetic, still zero predicate calls):
## every pair index in [0,705893] must appear in exactly one f_index's
## six-tuple. Spot-check f_index=0 and f_index=117648 (the two boundary
## f-values) map to the expected 6 pair indices.
if FIndexToSixPairIndices(0) <> [0, 117649, 235298, 352947, 470596, 588245] then
  Error("JOIN_RECEIPT_STOP: f_index=0 six-tuple mismatch");
fi;
if FIndexToSixPairIndices(117648) <> [117648, 235297, 352946, 470595, 588244, 705893] then
  Error("JOIN_RECEIPT_STOP: f_index=117648 six-tuple mismatch");
fi;
Print("join receipt boundary self-test PASS (f_index=0 and f_index=117648)\n");

Print("would_write_records=", Length(records), " to ", OUT_CERT_PATH, "\n");
Print("frozen_driver_digest(recorded)=", FROZEN_DRIVER_DIGEST_P, "\n");
Print("DRIVER_DONE: true\n");
Print("LANE_P_WRAPPER_DRY_CHECK_DONE\n");
QUIT;
