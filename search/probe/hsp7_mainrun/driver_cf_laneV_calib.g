## search/probe/hsp7_mainrun/driver_cf_laneV_calib.g
## Lane V CF re-calibration driver (裁定527発火・implementer, 2026-08-05).
## Re-runs the 13 registered Lane V fixtures (8 dummy/h3 candidates + NW-P8
## m-sweep 5) through the CLOSED-FORM predicate (predicate_lib_laneV_cf.g)
## instead of the baseline EvalFullHexagonFixed (predicate_lib_laneV.g /
## statemachine_lib.g). Read-only w.r.t. the baseline: statemachine_lib.g is
## Read() unchanged and used ONLY for (a) its own TOY self-test gates and
## (b) a two-path cross-check (same fixtures, both evaluators, judgment
## vectors compared). No baseline file is modified.
##
## Prints log lines in the SAME format driver_step4_evaluate_v3.g used, so
## search/probe/hsp7_ci_calib/parse_and_compare.py (unmodified) can parse this
## driver's log exactly as it parses the baseline's.
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/probe/hsp7_cond4_laneV/statemachine_lib.g");      ## baseline (read-only, for gates + cross-check)
Read("search/probe/hsp7_mainrun/predicate_lib_laneV_cf.g");    ## CF (new)
LoadPackage("anupq");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

## ---- gate 1: baseline's own TOY fixtures (unchanged, must still pass) ----
toyGate := TestToyFixtureLiteralVsFixed();;
if (not toyGate.ok) or (toyGate.mismatches > 0) then
  Error("BASELINE_TOY_GATE_FAILED");
fi;
extGate := TestToyFixtureExtended();;
if (not extGate.ok) or (extGate.mismatches > 0) then
  Error("BASELINE_EXT_TOY_GATE_FAILED");
fi;
Print("[GATE PASS] baseline TOY fixtures (6/6, 7/7) clean.\n");

## ---- gate 2: CF's own TOY fixtures (new, ported from conv_check.g/2.g) ----
cfMain := SelfTestCF_Main();;
if (not cfMain.ok) or (cfMain.mismatches > 0) then
  Error("CF_TOY_MAIN_GATE_FAILED");
fi;
Print("[GATE PASS] CF TOY main window: ", cfMain.mismatches, "/", cfMain.total, " mismatches.\n");
cfCtrl := SelfTestCF_Control();;
if (not cfCtrl.ok) or (cfCtrl.mismatches > 0) then
  Error("CF_TOY_CONTROL_GATE_FAILED");
fi;
Print("[GATE PASS] CF TOY control window: ", cfCtrl.mismatches, "/", cfCtrl.total, " mismatches.\n\n");

## ---- rebuild P (Lane V's own PQ_OUTPUT_P.g, identical to driver_step4_evaluate_v3.g) ----
Read("search/probe/hsp7_cond4_laneV/PQ_OUTPUT_P.g");
P := F;;
xbar := MapImages[1];;
ybar := MapImages[2];;
Print("|P| = ", Size(P), "\n");

chatMain := Identity(P);;

C7 := CyclicGroup(IsPcGroup, 7);;
gc := GeneratorsOfGroup(C7)[1];;
N0grp := DirectProduct(P, C7);;
embP := Embedding(N0grp, 1);;  embC := Embedding(N0grp, 2);;
xbar0 := Image(embP, xbar);;  ybar0 := Image(embP, ybar);;  chat0 := Image(embC, gc);;
Print("|N0grp| = ", Size(N0grp), "  Order(chat0) = ", Order(chat0), "\n");

## ---- CF one-time setup: A1,A2 as automorphisms of P (N window) and N0grp (N0 window) ----
t0 := Runtime();;
autosN := BuildHexAutos(P, xbar, ybar, chatMain);;
t1 := Runtime();;
setupTimeN_ms := t1 - t0;;
Print("CF setup (BuildHexAutos, N window): ", setupTimeN_ms, " ms\n");

t0 := Runtime();;
autosN0 := BuildHexAutos(N0grp, xbar0, ybar0, chat0);;
t1 := Runtime();;
setupTimeN0_ms := t1 - t0;;
Print("CF setup (BuildHexAutos, N0 window): ", setupTimeN0_ms, " ms\n\n");

## ---- 8 dummy/h3 candidates, as DIRECT P-elements (CF consumes elements, not words) ----
h4bar := Comm(Comm(Comm(xbar,ybar),xbar),xbar) * Comm(Comm(Comm(xbar,ybar),xbar),ybar)^4
         * Comm(Comm(Comm(xbar,ybar),ybar),ybar);;
h3bar := Comm(Comm(xbar,ybar),xbar) * Comm(Comm(xbar,ybar),ybar);;

## baseline (free-word) versions, for the two-path cross-check only:
FreeXY := FreeGroup("x", "y");;
Fx := FreeXY.1;;  Fy := FreeXY.2;;
h4free := Comm(Comm(Comm(Fx,Fy),Fx),Fx) * Comm(Comm(Comm(Fx,Fy),Fx),Fy)^4
          * Comm(Comm(Comm(Fx,Fy),Fy),Fy);;
h3free := Comm(Comm(Fx,Fy),Fx) * Comm(Comm(Fx,Fy),Fy);;

candidates := [];;
for t in [0..6] do
  Add(candidates, rec(key_id := t+1, m := 0, fword := Concatenation("h4^", String(t)),
                       felt := h4bar^t, feltN0 := Image(embP, h4bar^t), ffree := h4free^t));
od;
Add(candidates, rec(key_id := 8, m := 0, fword := "h3 = [[x,y],x]*[[x,y],y]",
                     felt := h3bar, feltN0 := Image(embP, h3bar), ffree := h3free));

## ---- N window: CF path, m=0 shared across all 8 candidates -> one BuildMDependent call ----
mdepN_m0 := BuildMDependent(autosN, xbar, ybar, chatMain, 0);;
laneV_N_results_cf := [];;
cfTimes_N := [];;
baseTimes_N := [];;
twoPathMismatch_N := 0;;
for c in candidates do
  tA := Runtime();;
  rcf := EvalFullHexagonCF(mdepN_m0, autosN, c.felt);;
  tB := Runtime();;
  Add(cfTimes_N, tB - tA);
  tA := Runtime();;
  rbase := EvalFullHexagonFixed(c.m, c.ffree, xbar, ybar, chatMain);;
  tB := Runtime();;
  Add(baseTimes_N, tB - tA);
  verdict := "FAIL";; if rcf.hex33 and rcf.hex34 then verdict := "PASS"; fi;
  Add(laneV_N_results_cf, rec(key_id := c.key_id, fword := c.fword, hex33 := rcf.hex33, hex34 := rcf.hex34, verdict := verdict));
  if (rcf.hex33 <> rbase.hex33) or (rcf.hex34 <> rbase.hex34) then
    twoPathMismatch_N := twoPathMismatch_N + 1;
    Print("TWO_PATH_MISMATCH at key_id=", c.key_id, " CF=", rcf, " baseline=", rbase, "\n");
  fi;
  Print("N  candidate key_id=", c.key_id, " f=", c.fword, " : (3.3)=", rcf.hex33, " (3.4)=", rcf.hex34, " verdict=", verdict, "\n");
od;
Print("two-path mismatch count (N window, 8 candidates, CF vs baseline) = ", twoPathMismatch_N, "\n\n");

## ---- N0 window: CF path (same 8 candidates), for audit parity with the baseline driver ----
mdepN0_m0 := BuildMDependent(autosN0, xbar0, ybar0, chat0, 0);;
laneV_N0_results_cf := [];;
twoPathMismatch_N0 := 0;;
for c in candidates do
  rcf := EvalFullHexagonCF(mdepN0_m0, autosN0, c.feltN0);;
  rbase := EvalFullHexagonFixed(c.m, c.ffree, xbar0, ybar0, chat0);;
  verdict := "FAIL";; if rcf.hex33 and rcf.hex34 then verdict := "PASS"; fi;
  Add(laneV_N0_results_cf, rec(key_id := c.key_id, fword := c.fword, hex33 := rcf.hex33, hex34 := rcf.hex34, verdict := verdict));
  if (rcf.hex33 <> rbase.hex33) or (rcf.hex34 <> rbase.hex34) then
    twoPathMismatch_N0 := twoPathMismatch_N0 + 1;
    Print("TWO_PATH_MISMATCH_N0 at key_id=", c.key_id, " CF=", rcf, " baseline=", rbase, "\n");
  fi;
  Print("N0 candidate key_id=", c.key_id, " f=", c.fword, " : (3.3)=", rcf.hex33, " (3.4)=", rcf.hex34, " verdict=", verdict, "\n");
od;
Print("two-path mismatch count (N0 window, 8 candidates, CF vs baseline) = ", twoPathMismatch_N0, "\n\n");

n_vs_n0_mismatch_8cand_cf := 0;;
for i in [1..8] do
  if laneV_N_results_cf[i].verdict <> laneV_N0_results_cf[i].verdict then
    n_vs_n0_mismatch_8cand_cf := n_vs_n0_mismatch_8cand_cf + 1;
  fi;
od;
Print("N vs N0 mismatch count (8 candidates, CF path) = ", n_vs_n0_mismatch_8cand_cf, "\n\n");

## ---- NW-P8 m-sweep: f = identity, m in {1,2,4,5,6}, CF path + two-path cross-check ----
mSweep := [1,2,4,5,6];;
freeOne := One(FreeXY);;
idP := Identity(P);;
idN0 := Identity(N0grp);;
p8results_cf := [];;
cfTimes_sweep := [];;
baseTimes_sweep := [];;
twoPathMismatch_sweep := 0;;
for m in mSweep do
  mdepN_m := BuildMDependent(autosN, xbar, ybar, chatMain, m);;
  tA := Runtime();;
  rN_cf := EvalFullHexagonCF(mdepN_m, autosN, idP);;
  tB := Runtime();;
  Add(cfTimes_sweep, tB - tA);
  tA := Runtime();;
  rN_base := EvalFullHexagonFixed(m, freeOne, xbar, ybar, chatMain);;
  tB := Runtime();;
  Add(baseTimes_sweep, tB - tA);
  vN_cf := "FAIL";; if rN_cf.hex33 and rN_cf.hex34 then vN_cf := "PASS"; fi;

  mdepN0_m := BuildMDependent(autosN0, xbar0, ybar0, chat0, m);;
  rN0_cf := EvalFullHexagonCF(mdepN0_m, autosN0, idN0);;
  rN0_base := EvalFullHexagonFixed(m, freeOne, xbar0, ybar0, chat0);;
  vN0_cf := "FAIL";; if rN0_cf.hex33 and rN0_cf.hex34 then vN0_cf := "PASS"; fi;

  if (rN_cf.hex33 <> rN_base.hex33) or (rN_cf.hex34 <> rN_base.hex34)
     or (rN0_cf.hex33 <> rN0_base.hex33) or (rN0_cf.hex34 <> rN0_base.hex34) then
    twoPathMismatch_sweep := twoPathMismatch_sweep + 1;
    Print("TWO_PATH_MISMATCH_SWEEP at m=", m, "\n");
  fi;
  Add(p8results_cf, rec(m := m, verdictN := vN_cf, verdictN0 := vN0_cf, agree := (vN_cf = vN0_cf)));
  Print("NW-P8 m=", m, ": N=", vN_cf, " N0=", vN0_cf, " agree=", (vN_cf=vN0_cf), "\n");
od;
p8_mismatch_count_cf := Length(Filtered(p8results_cf, r -> not r.agree));;
Print("\nNW-P8 mismatch count (N vs N0, CF path) = ", p8_mismatch_count_cf, " (of 5)\n");
Print("two-path mismatch count (m-sweep, CF vs baseline) = ", twoPathMismatch_sweep, "\n\n");

## ---- timing summary (single-pass, coarse -- ms resolution too coarse for a
## single fast call, kept for the raw record) ----
avgCF_N := Sum(cfTimes_N) / Length(cfTimes_N);;
avgBase_N := Sum(baseTimes_N) / Length(baseTimes_N);;
avgCF_sweep := Sum(cfTimes_sweep) / Length(cfTimes_sweep);;
avgBase_sweep := Sum(baseTimes_sweep) / Length(baseTimes_sweep);;
Print("=== TIMING single-pass (fixture candidates only -- NOT sampled from the 705,894-candidate universe) ===\n");
Print("N window, 8 dummy/h3 candidates: avg CF = ", avgCF_N, " ms/candidate, avg baseline = ", avgBase_N, " ms/candidate\n");
Print("m-sweep, 5 candidates (f=identity): avg CF = ", avgCF_sweep, " ms/candidate, avg baseline = ", avgBase_sweep, " ms/candidate\n");
Print("CF one-time setup cost (BuildHexAutos): N window = ", setupTimeN_ms, " ms, N0 window = ", setupTimeN0_ms, " ms\n");
Print("raw per-candidate CF times (N window, ms): ", cfTimes_N, "\n");
Print("raw per-candidate baseline times (N window, ms): ", baseTimes_N, "\n");
Print("raw per-candidate CF times (sweep, ms): ", cfTimes_sweep, "\n");
Print("raw per-candidate baseline times (sweep, ms): ", baseTimes_sweep, "\n\n");

## ---- REPEATED timing benchmark (ms resolution floor workaround): each of
## the 8 N-window candidates is evaluated REPS times back-to-back by each
## evaluator (fixture candidates ONLY -- the frozen 8 dummy/h3 + m=0, never
## the 705,894-candidate universe), total wall time measured once per
## evaluator, divided by (REPS * 8) to get a per-candidate average with
## enough resolution to be meaningful. This is the number reported as the
## "measured reduction factor" in the cert (SS designed constraint: timing
## on fixture candidates only). ----
REPS := 2000;;
t0 := Runtime();;
for rep in [1..REPS] do
  for c in candidates do
    dummyCF := EvalFullHexagonCF(mdepN_m0, autosN, c.felt);
  od;
od;
t1 := Runtime();;
totalCF_ms := t1 - t0;;
perCandCF_ms := totalCF_ms / (REPS * Length(candidates));;

t0 := Runtime();;
for rep in [1..REPS] do
  for c in candidates do
    dummyBase := EvalFullHexagonFixed(c.m, c.ffree, xbar, ybar, chatMain);
  od;
od;
t1 := Runtime();;
totalBase_ms := t1 - t0;;
perCandBase_ms := totalBase_ms / (REPS * Length(candidates));;

reductionFactor := totalBase_ms / totalCF_ms;;
Print("=== TIMING repeated benchmark (REPS=", REPS, ", 8 N-window fixture candidates only) ===\n");
Print("total CF time = ", totalCF_ms, " ms over ", REPS*Length(candidates), " calls => per-candidate = ", perCandCF_ms, " ms\n");
Print("total baseline time = ", totalBase_ms, " ms over ", REPS*Length(candidates), " calls => per-candidate = ", perCandBase_ms, " ms\n");
Print("measured reduction factor (baseline/CF) = ", reductionFactor, "x\n\n");

Print("\n=== SUMMARY ===\n");
Print("two_path_mismatch_N=", twoPathMismatch_N, "\n");
Print("two_path_mismatch_N0=", twoPathMismatch_N0, "\n");
Print("two_path_mismatch_sweep=", twoPathMismatch_sweep, "\n");
Print("n_vs_n0_mismatch_8cand_cf=", n_vs_n0_mismatch_8cand_cf, "\n");
Print("p8_mismatch_count_cf=", p8_mismatch_count_cf, "\n");
Print("measured_reduction_factor=", reductionFactor, "\n");
Print("per_candidate_cf_ms=", perCandCF_ms, "\n");
Print("per_candidate_baseline_ms=", perCandBase_ms, "\n");

Print("\n[DONE] driver_cf_laneV_calib.g complete.\n");
QUIT;
