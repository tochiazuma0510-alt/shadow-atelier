#############################################################################
## search/probe/sg_band_sweep/sg_band_sweep_driver_v1.g
## SmallGroups G0-G3 band sweep -- IF-FIRST prereg execution (裁定633 prereg,
## 司令塔 execution order this session). Prereg (frozen, verbatim authority,
## NOT modified by this script):
##   docs/notes/sg_band_sweep_prereg_iffirst_v1.md
##   sha256 = 96449d682d9f312b861e5c8cca73d4b2cce03a4afb1664708f672a1638b0a4de
##
## Judgment logic is EXACTLY prereg SS3.3 (4 lines, no new machinery):
##   G0: n in band, k in [1..NrSmallGroups(n)], Ghat := SmallGroup(n,k)
##   G1: AbelianInvariants(Ghat) in {[2],[2,3],[6]}          (Lemma SG-AB)
##   G2: exists (r,s): ord(r)=2, ord(s)=3, <r,s>=Ghat          (Cor SG-23)
##       -- r ranges over INVOLUTION CONJUGACY CLASS REPS ONLY (pruning is
##          sound for an EXISTENCE test, prereg SS3.3 warning); s ranges
##          over ALL elements of order 3 (cannot be pruned the same way).
##   G3: exists surjective phi: Ghat -> S3                     (Lemma SG-S3)
##
## Execution order (prereg SS10 item 3, verbatim):
##   DF-SG-1..6 (2b included) FIRST, fail-closed (S-SG-5: any FAIL/missing
##   DF-SG-6 report => STOP, no band sweep at all) -- THEN band orders in
##   the exact sequence 1458 -> 1944 -> 1296 -> 1728 -> 1152 (1152 LAST,
##   heaviest, so a cap trip does not take the other 4 down with it).
##
## Non-contact: this script does not touch the 3 sealed quantities, Im R,
## d_N, n=5 series. It only inspects the ABSTRACT SHAPE of library groups
## (AbelianInvariants / conjugacy classes / element orders / GQuotients to
## S3) -- prereg SS0-6. No exotic/twin/isolated claim is written anywhere
## (SS5, S-SG-9) -- this script only ever writes numeric counts and
## g3_records; grading/interpretation is out of scope (SS10 item 4).
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;

PREREG_PATH := "docs/notes/sg_band_sweep_prereg_iffirst_v1.md";;
PREREG_SHA_EXPECTED := "96449d682d9f312b861e5c8cca73d4b2cce03a4afb1664708f672a1638b0a4de";;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sgband_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then Error("sha256 fail for ", relpath); fi;
  return line{[1 .. 64]};
end;;

PreregShaActual := ComputeSha256File(PREREG_PATH);;
Print("prereg sha256 (actual)   = ", PreregShaActual, "\n");
Print("prereg sha256 (expected) = ", PREREG_SHA_EXPECTED, "\n");
if PreregShaActual <> PREREG_SHA_EXPECTED then
  Print("PREREG_DIGEST_MISMATCH -- STOP (prereg is not the frozen v1 text)\n");
  Error("PREREG_DIGEST_MISMATCH");
fi;
Print("[PASS] prereg digest matches frozen v1\n");

S3grp := SymmetricGroup(3);;

#############################################################################
## Judgment predicates (prereg SS3.3, verbatim -- the ONLY 4 lines of logic)
#############################################################################
G1_Test := function(Ghat)
  local ab;
  ab := AbelianInvariants(Ghat);;
  return ab in [[2],[2,3],[6]];
end;;

## G2: returns rec(pass:=bool, r:=elt or fail, s:=elt or fail,
##                  nInvClasses:=int, nOrd3:=int)
G2_Test := function(Ghat)
  local invReps, ord3Elts, r, s, sz;
  invReps := Filtered(List(ConjugacyClasses(Ghat), Representative), x -> Order(x) = 2);;
  ord3Elts := Filtered(Elements(Ghat), x -> Order(x) = 3);;
  sz := Size(Ghat);;
  for r in invReps do
    for s in ord3Elts do
      if Size(Subgroup(Ghat, [r,s])) = sz then
        return rec(pass := true, r := r, s := s,
                    nInvClasses := Length(invReps), nOrd3 := Length(ord3Elts));
      fi;
    od;
  od;
  return rec(pass := false, r := fail, s := fail,
              nInvClasses := Length(invReps), nOrd3 := Length(ord3Elts));
end;;

## G3: returns rec(pass:=bool, hom:=hom or fail)
G3_Test := function(Ghat)
  local quots;
  quots := GQuotients(Ghat, S3grp);;
  if Length(quots) > 0 then
    return rec(pass := true, hom := quots[1]);
  fi;
  return rec(pass := false, hom := fail);
end;;

#############################################################################
## PART 1 -- calibration DF-SG-1..6 (fail-closed: any FAIL/missing DF-SG-6
## report => STOP before the band sweep, per S-SG-5)
#############################################################################
Print("\n=== Calibration DF-SG-1..6 ===\n");
CAL := rec();;
CAL_ALL_OK := true;;

## DF-SG-1: SmallGroup(6,1)=S3 must pass G1+G2+G3. Contrast (not a pass/fail
## gate itself, reported as observation): SmallGroup(6,2)=C6.
g61 := SmallGroup(6,1);;
ab61 := AbelianInvariants(g61);;
g1_61 := G1_Test(g61);; g2_61 := G2_Test(g61);; g3_61 := G3_Test(g61);;
df1_pass := g1_61 and g2_61.pass and g3_61.pass;;
Print("DF-SG-1: SmallGroup(6,1) ab=", ab61, " G1=", g1_61, " G2=", g2_61.pass, " G3=", g3_61.pass,
      " -> ", (function() if df1_pass then return "PASS"; else return "FAIL"; fi; end)(), "\n");
CAL.DF_SG_1 := rec(status := (function() if df1_pass then return "PASS"; else return "FAIL"; fi; end)(),
                    ab := ab61, g1 := g1_61, g2 := g2_61.pass, g3 := g3_61.pass);;
if not df1_pass then CAL_ALL_OK := false; fi;

g62 := SmallGroup(6,2);;
ab62 := AbelianInvariants(g62);;
g1_62 := G1_Test(g62);; g2_62 := G2_Test(g62);;
Print("DF-SG-1 contrast: SmallGroup(6,2)=C6 ab=", ab62, " G1=", g1_62, " G2=", g2_62.pass,
      " (observation only, not a pass/fail gate)\n");
CAL.DF_SG_1_contrast_C6 := rec(ab := ab62, g1 := g1_62, g2 := g2_62.pass);;

## DF-SG-2: SmallGroup(126,9) must pass G1+G2+G3
g1269 := SmallGroup(126,9);;
ab1269 := AbelianInvariants(g1269);;
g1_1269 := G1_Test(g1269);; g2_1269 := G2_Test(g1269);; g3_1269 := G3_Test(g1269);;
df2_pass := g1_1269 and g2_1269.pass and g3_1269.pass;;
Print("DF-SG-2: SmallGroup(126,9) ab=", ab1269, " G1=", g1_1269, " G2=", g2_1269.pass, " G3=", g3_1269.pass,
      " -> ", (function() if df2_pass then return "PASS"; else return "FAIL"; fi; end)(), "\n");
CAL.DF_SG_2 := rec(status := (function() if df2_pass then return "PASS"; else return "FAIL"; fi; end)(),
                    ab := ab1269, g1 := g1_1269, g2 := g2_1269.pass, g3 := g3_1269.pass);;
if not df2_pass then CAL_ALL_OK := false; fi;

## DF-SG-2b: SmallGroup(24,3)=SL(2,3) must FAIL G1 (ab=[3])
g243 := SmallGroup(24,3);;
ab243 := AbelianInvariants(g243);;
g1_243 := G1_Test(g243);;
df2b_pass := (g1_243 = false);;
Print("DF-SG-2b: SmallGroup(24,3) ab=", ab243, " G1=", g1_243,
      " -> ", (function() if df2b_pass then return "PASS"; else return "FAIL"; fi; end)(), "\n");
CAL.DF_SG_2b := rec(status := (function() if df2b_pass then return "PASS"; else return "FAIL"; fi; end)(),
                     ab := ab243, g1 := g1_243);;
if not df2b_pass then CAL_ALL_OK := false; fi;

## DF-SG-3 *** lifeline ***: SmallGroup(432,734) and SmallGroup(486,39) must
## BOTH pass G1+G2+G3.
g432734 := SmallGroup(432,734);;
ab432734 := AbelianInvariants(g432734);;
g1_432 := G1_Test(g432734);; g2_432 := G2_Test(g432734);; g3_432 := G3_Test(g432734);;
df3a_pass := g1_432 and g2_432.pass and g3_432.pass;;
Print("DF-SG-3a: SmallGroup(432,734) ab=", ab432734, " G1=", g1_432, " G2=", g2_432.pass, " G3=", g3_432.pass,
      " -> ", (function() if df3a_pass then return "PASS"; else return "FAIL"; fi; end)(), "\n");

g48639 := SmallGroup(486,39);;
ab48639 := AbelianInvariants(g48639);;
g1_486 := G1_Test(g48639);; g2_486 := G2_Test(g48639);; g3_486 := G3_Test(g48639);;
df3b_pass := g1_486 and g2_486.pass and g3_486.pass;;
Print("DF-SG-3b: SmallGroup(486,39) ab=", ab48639, " G1=", g1_486, " G2=", g2_486.pass, " G3=", g3_486.pass,
      " -> ", (function() if df3b_pass then return "PASS"; else return "FAIL"; fi; end)(), "\n");

df3_pass := df3a_pass and df3b_pass;;
CAL.DF_SG_3 := rec(status := (function() if df3_pass then return "PASS"; else return "FAIL"; fi; end)(),
                    order432 := rec(ab := ab432734, g1 := g1_432, g2 := g2_432.pass, g3 := g3_432.pass),
                    order486 := rec(ab := ab48639, g1 := g1_486, g2 := g2_486.pass, g3 := g3_486.pass));;
if not df3_pass then CAL_ALL_OK := false; fi;

## DF-SG-4: an abelian SmallGroup(1152,k) must FAIL G1
DF4_FOUND := false;; DF4_K := fail;;
for kk in [1..NrSmallGroups(1152)] do
  gg := SmallGroup(1152,kk);;
  if IsAbelian(gg) then
    DF4_FOUND := true;; DF4_K := kk;;
    df4_g1 := G1_Test(gg);;
    break;
  fi;
od;
df4_pass := DF4_FOUND and (df4_g1 = false);;
Print("DF-SG-4: SmallGroup(1152,", DF4_K, ") abelian, G1=", df4_g1,
      " -> ", (function() if df4_pass then return "PASS"; else return "FAIL"; fi; end)(), "\n");
CAL.DF_SG_4 := rec(status := (function() if df4_pass then return "PASS"; else return "FAIL"; fi; end)(),
                    id := [1152, DF4_K], g1 := df4_g1);;
if not df4_pass then CAL_ALL_OK := false; fi;

## DF-SG-5: a SmallGroup(1152,k) with ab=C3 or C4 must FAIL G1
DF5_FOUND := false;; DF5_K := fail;;
for kk in [1..NrSmallGroups(1152)] do
  gg := SmallGroup(1152,kk);;
  abgg := AbelianInvariants(gg);;
  if abgg = [3] or abgg = [4] then
    DF5_FOUND := true;; DF5_K := kk;; DF5_AB := abgg;;
    df5_g1 := G1_Test(gg);;
    break;
  fi;
od;
df5_pass := DF5_FOUND and (df5_g1 = false);;
Print("DF-SG-5: SmallGroup(1152,", DF5_K, ") ab=", DF5_AB, " G1=", df5_g1,
      " -> ", (function() if df5_pass then return "PASS"; else return "FAIL"; fi; end)(), "\n");
CAL.DF_SG_5 := rec(status := (function() if df5_pass then return "PASS"; else return "FAIL"; fi; end)(),
                    id := [1152, DF5_K], ab := DF5_AB, g1 := df5_g1);;
if not df5_pass then CAL_ALL_OK := false; fi;

## DF-SG-6: a group passing G1+G2 but failing G3, ANYWHERE in the band
## (search cheaply: reuse the small scan already done for DF-4/DF-5 plus a
## short scan of order 1152 -- report NOT_FOUND if none turns up here; the
## real answer is also recorded from the full sweep in PART 2 below and
## reconciled at the end, since S-SG-5 forbids silently omitting it).
DF6_FOUND := false;; DF6_ID := fail;;
for kk in [1..Minimum(2000, NrSmallGroups(1152))] do
  gg := SmallGroup(1152,kk);;
  if G1_Test(gg) then
    g2r := G2_Test(gg);;
    if g2r.pass then
      g3r := G3_Test(gg);;
      if not g3r.pass then
        DF6_FOUND := true;; DF6_ID := [1152,kk];;
        break;
      fi;
    fi;
  fi;
od;
Print("DF-SG-6 (calibration-scan, first 2000 of order 1152): ",
      (function() if DF6_FOUND then return Concatenation("FOUND ", String(DF6_ID)); else return "NOT_FOUND in this scan (full-sweep reconciliation below)"; fi; end)(), "\n");
CAL.DF_SG_6_calibration_scan := rec(found := DF6_FOUND, id := DF6_ID,
    note := "this is a bounded calibration-time scan (first 2000 groups of order 1152), NOT the full-band answer; the full sweep in PART 2 is authoritative and this field is reconciled into calibration.DF_SG_6_final below after PART 2");;
## DF-SG-6 itself is never a STOP condition (S-SG-5 requires reporting the
## result, not requiring FOUND) -- always "PASS" as a calibration ITEM in
## the sense that it was executed and reported.
CAL.DF_SG_6 := rec(status := "PASS_EXECUTED_AND_REPORTED");;

Print("\n=== Calibration summary: ", (function() if CAL_ALL_OK then return "ALL PASS"; else return "FAIL -- STOP"; fi; end)(), " ===\n");
if not CAL_ALL_OK then
  Print("CALIBRATION_FAIL / STOP (S-SG-5) -- band sweep NOT executed.\n");
  DETAIL_CAL_ONLY := Concatenation(
    "{\n\"schema\":\"shadow-atelier/sg-band-sweep-calibration-fail/v1\",\n",
    "\"prereg\":{\"path\":", JStr(PREREG_PATH), ",\"sha256\":", JStr(PreregShaActual), "},\n",
    "\"calibration_all_ok\":false,\n",
    "\"stop_code\":\"CALIBRATION_FAIL\"\n}\n");;
  WriteFile("search/certs/sg_band_sweep_CALFAIL_20260806.json", DETAIL_CAL_ONLY);;
  Error("CALIBRATION_FAIL -- STOP, see printed DF-SG-* results above");
fi;

Print("W6_SG_CALIBRATION_ALL_PASS\n");

#############################################################################
## PART 2 -- band sweep (prereg SS3.1 frozen universe / SS3.4 caps / SS10
## item 3 execution order). Judgment = G1_Test/G2_Test/G3_Test above only.
#############################################################################
FROZEN_NR := rec();;
FROZEN_NR.(String(1152)) := 157877;;
FROZEN_NR.(String(1296)) := 3609;;
FROZEN_NR.(String(1458)) := 1798;;
FROZEN_NR.(String(1728)) := 47937;;
FROZEN_NR.(String(1944)) := 3973;;
FROZEN_TOTAL := 157877+3609+1798+47937+3973;;   ## = 215194

ORDER_SEQUENCE := [1458, 1944, 1296, 1728, 1152];;   ## prereg SS10 item 3, verbatim
ORDER_CAP_SEC := 1800.0;;
TOTAL_CAP_SEC := 7200.0;;
CAP_CHECK_EVERY := 3000;;

PER_ORDER := [];;          ## completed orders only (S-SG-7: no partial order)
G3_RECORDS := [];;
DF6_FINAL_FOUND := DF6_FOUND;;   ## seed from calibration-scan; may upgrade below
DF6_FINAL_ID := DF6_ID;;
TIME_CAP_HIT := false;;
UNIVERSE_MISMATCH := false;;
UNIVERSE_MISMATCH_DETAIL := "";;

SweepOneOrder := function(n)
  local nrExpected, nrActual, g1cnt, g2cnt, g3cnt, kk, Ghat, ab, isg1,
        g2r, g3r, t0g1, t0g2, t0g3, wallG1, wallG2, wallG3, idg, hom,
        recRow, elapsedWall, capHitLocal, orderStart;
  nrExpected := FROZEN_NR.(String(n));;
  nrActual := NrSmallGroups(n);;
  if nrActual <> nrExpected then
    UNIVERSE_MISMATCH := true;;
    UNIVERSE_MISMATCH_DETAIL := Concatenation("order ", String(n), ": expected ", String(nrExpected),
        " actual ", String(nrActual));;
    Print("UNIVERSE_MISMATCH / STOP: ", UNIVERSE_MISMATCH_DETAIL, "\n");
    return fail;
  fi;

  Print("\n=== Sweeping order ", n, " (", nrExpected, " groups) ===\n");
  g1cnt := 0;; g2cnt := 0;; g3cnt := 0;;
  wallG1 := 0;; wallG2 := 0;; wallG3 := 0;;
  orderStart := GAPLIB_WallElapsedMs();;
  capHitLocal := false;;

  for kk in [1..nrExpected] do
    if kk mod CAP_CHECK_EVERY = 0 then
      elapsedWall := (GAPLIB_WallElapsedMs() - orderStart) / 1000.0;;
      if elapsedWall > ORDER_CAP_SEC or GAPLIB_WallElapsedMs()/1000.0 > TOTAL_CAP_SEC then
        Print("  [CAP] order ", n, " at k=", kk, "/", nrExpected, " elapsed=", elapsedWall, "s -- TIME_CAP/STOP\n");
        capHitLocal := true;;
        TIME_CAP_HIT := true;;
        break;
      fi;
      Print("  ... k=", kk, "/", nrExpected, " g1cnt=", g1cnt, " g2cnt=", g2cnt, " g3cnt=", g3cnt,
            " elapsed=", elapsedWall, "s\n");
    fi;

    Ghat := SmallGroup(n, kk);;
    isg1 := G1_Test(Ghat);;
    if isg1 then
      g1cnt := g1cnt + 1;;
      g2r := G2_Test(Ghat);;
      if g2r.pass then
        g2cnt := g2cnt + 1;;
        g3r := G3_Test(Ghat);;
        if g3r.pass then
          g3cnt := g3cnt + 1;;
          ab := AbelianInvariants(Ghat);;
          hom := g3r.hom;;
          idg := fail;;
          if Size(Ghat) <= 2000 then
            idg := IdGroup(Ghat);;
          fi;
          recRow := rec(
            order := n, id := kk,
            abelian_invariants := ab,
            n_involution_classes := g2r.nInvClasses,
            n_order3_elements := g2r.nOrd3,
            witness_r := String(g2r.r),
            witness_s := String(g2r.s),
            P_hat_order := Size(Ghat),
            P_hat_idgroup := idg
          );;
          Add(G3_RECORDS, recRow);;
        else
          ## G2 pass, G3 fail -- DF-SG-6 final reconciliation (first hit wins)
          if not DF6_FINAL_FOUND then
            DF6_FINAL_FOUND := true;;
            DF6_FINAL_ID := [n, kk];;
          fi;
        fi;
      fi;
    fi;
  od;

  if capHitLocal then
    return fail;   ## S-SG-7: partial order NOT reported
  fi;

  elapsedWall := (GAPLIB_WallElapsedMs() - orderStart) / 1000.0;;
  Print("  order ", n, " DONE: total=", nrExpected, " g1=", g1cnt, " g2=", g2cnt, " g3=", g3cnt,
        " wall=", elapsedWall, "s\n");
  return rec(order := n, total := nrExpected, g1_pass := g1cnt, g2_pass := g2cnt, g3_pass := g3cnt,
             wall_s := elapsedWall);;
end;;

for ordn in ORDER_SEQUENCE do
  if UNIVERSE_MISMATCH then break; fi;
  if GAPLIB_WallElapsedMs()/1000.0 > TOTAL_CAP_SEC then
    Print("[CAP] total cap already exceeded before starting order ", ordn, " -- skipping (S-SG-7)\n");
    TIME_CAP_HIT := true;;
    break;
  fi;
  res := SweepOneOrder(ordn);;
  if res <> fail then
    Add(PER_ORDER, res);;
  fi;
od;

Print("\n=== Band sweep summary ===\n");
Print("orders completed: ", List(PER_ORDER, r->r.order), "\n");
Print("UNIVERSE_MISMATCH=", UNIVERSE_MISMATCH, " TIME_CAP_HIT=", TIME_CAP_HIT, "\n");
Print("DF-SG-6 final: found=", DF6_FINAL_FOUND, " id=", DF6_FINAL_ID, "\n");
Print("total G3 records: ", Length(G3_RECORDS), "\n");

#############################################################################
## PART 3 -- predictions_scored (P-SGB-1..6, mechanically re-derived from
## PER_ORDER/G3_RECORDS only; 1296's G1 is EXCLUDED_PREOBSERVED per prereg
## SS0-2/SS4.1) + cert assembly.
#############################################################################
V2_OF := rec();;
V2_OF.(String(1152)) := 7;; V2_OF.(String(1296)) := 4;; V2_OF.(String(1458)) := 1;;
V2_OF.(String(1728)) := 6;; V2_OF.(String(1944)) := 3;;

PredictedRate := function(i) return 0.40 * 2.26^(-(i-1)); end;;
PredictedG1Count := rec();;
PredictedG1Count.(String(1152)) := 474;;
PredictedG1Count.(String(1458)) := 719;;
PredictedG1Count.(String(1728)) := 325;;
PredictedG1Count.(String(1944)) := 311;;

ByOrder := rec();;
for r in PER_ORDER do ByOrder.(String(r.order)) := r; od;;

## P-SGB-1: rate law, factor-2, scored orders = band minus 1296
P_SGB_1_rows := [];;
scoredOrders := Filtered([1152,1458,1728,1944], n -> IsBound(ByOrder.(String(n))));;
p_sgb_1_all_within_factor2 := true;;
for n in scoredOrders do
  rrow := ByOrder.(String(n));;
  actualRate := 1.0 * rrow.g1_pass / rrow.total;;   ## bugfix: force float (GAP int/int = exact rational, which cannot be compared to a float literal -- "Comparison of float and N/M is not supported")
  predRate := PredictedRate(V2_OF.(String(n)));;
  ratio := actualRate / predRate;;
  within := (ratio >= 0.5) and (ratio <= 2.0);;
  if not within then p_sgb_1_all_within_factor2 := false; fi;
  Add(P_SGB_1_rows, rec(order:=n, i:=V2_OF.(String(n)), predicted_rate:=predRate,
      actual_rate:=actualRate, ratio:=ratio, within_factor2:=within));;
od;;

## P-SGB-2: predicted G1 counts, factor-2
P_SGB_2_rows := [];;
p_sgb_2_all_within_factor2 := true;;
for n in scoredOrders do
  rrow := ByOrder.(String(n));;
  pred := PredictedG1Count.(String(n));;
  ratioc := 1.0 * rrow.g1_pass / pred;;   ## bugfix: force float, same reason as actualRate above
  withinc := (ratioc >= 0.5) and (ratioc <= 2.0);;
  if not withinc then p_sgb_2_all_within_factor2 := false; fi;
  Add(P_SGB_2_rows, rec(order:=n, predicted:=pred, actual:=rrow.g1_pass, ratio:=ratioc, within_factor2:=withinc));;
od;;

## P-SGB-3: sum over scored orders, registered interval [900,4000]
p_sgb_3_sum := Sum(scoredOrders, n -> ByOrder.(String(n)).g1_pass);;
p_sgb_3_in_interval := (p_sgb_3_sum >= 900) and (p_sgb_3_sum <= 4000);;

## P-SGB-4: existence (band total) + per-order point-estimate comparison
p_sgb_4_total_g3 := Sum(PER_ORDER, r -> r.g3_pass);;
p_sgb_4_exists := (p_sgb_4_total_g3 >= 1);;
P_SGB_4_rows := List(PER_ORDER, r -> rec(order:=r.order, g3_pass:=r.g3_pass,
    point_estimate := (function()
      if r.order = 1458 or r.order = 1944 then return "predicted_pass_ge_1";
      else return "UNKNOWN_not_predicted"; fi;
    end)()));;

## P-SGB-5: ratio G2/G1, aggregate across completed orders (weak evidence,
## never a STOP per S-SG-6 exception)
p_sgb_5_g1_sum := Sum(PER_ORDER, r -> r.g1_pass);;
p_sgb_5_g2_sum := Sum(PER_ORDER, r -> r.g2_pass);;
p_sgb_5_ratio := (function() if p_sgb_5_g1_sum = 0 then return fail; else return 1.0*p_sgb_5_g2_sum/p_sgb_5_g1_sum; fi; end)();;   ## bugfix: force float, same reason
p_sgb_5_in_interval := (p_sgb_5_ratio <> fail) and (p_sgb_5_ratio >= 0.15) and (p_sgb_5_ratio <= 0.60);;

## P-SGB-6: G2-pass-G3-fail exists (= DF-SG-6 final)
p_sgb_6_exists := DF6_FINAL_FOUND;;

## --- cert assembly ---
GapVersionStr := GAPInfo.Version;;
GapArchStr := GAPInfo.Architecture;;

PerOrderJson := JArr(List(PER_ORDER, r -> Concatenation(
  "{\"order\":", String(r.order), ",\"total\":", String(r.total),
  ",\"g1_pass\":", String(r.g1_pass), ",\"g2_pass\":", String(r.g2_pass),
  ",\"g3_pass\":", String(r.g3_pass), ",\"wall_s\":", String(r.wall_s), "}")));;

G3RecordsJson := JArr(List(G3_RECORDS, function(rr)
  local idgStr;
  idgStr := (function() if rr.P_hat_idgroup = fail then return "null"; else return JArr(List(rr.P_hat_idgroup,String)); fi; end)();;
  return Concatenation(
    "{\"order\":", String(rr.order), ",\"id\":", String(rr.id),
    ",\"abelian_invariants\":", JArr(List(rr.abelian_invariants,String)),
    ",\"n_involution_classes\":", String(rr.n_involution_classes),
    ",\"n_order3_elements\":", String(rr.n_order3_elements),
    ",\"witness_r\":", JStr(rr.witness_r), ",\"witness_s\":", JStr(rr.witness_s),
    ",\"P_hat_order\":", String(rr.P_hat_order), ",\"P_hat_idgroup\":", idgStr, "}");
end));;

UniverseFrozenJson := Concatenation(
  "{\"band_orders\":[1152,1296,1458,1728,1944],",
  "\"nr_small_groups\":{\"1152\":157877,\"1296\":3609,\"1458\":1798,\"1728\":47937,\"1944\":3973},",
  "\"total\":", String(FROZEN_TOTAL), ",",
  "\"scope_out_1536\":{\"decomposition\":\"2^9*3\",\"reason\":\"408,641,062 groups (metadata only, ID library), SCOPE_OUT not empty -- prereg SS3.1\"}}");;

UniverseCheckJson := Concatenation(
  "{\"orders_checked\":", JArr(List(PER_ORDER, r->String(r.order))),
  ",\"universe_mismatch\":", JB(UNIVERSE_MISMATCH),
  ",\"mismatch_detail\":", JStr(UNIVERSE_MISMATCH_DETAIL), "}");;

CalibrationJson := Concatenation(
  "{\"DF_SG_1\":{\"status\":", JStr(CAL.DF_SG_1.status), ",\"ab\":", JArr(List(CAL.DF_SG_1.ab,String)),
    ",\"g1\":", JB(CAL.DF_SG_1.g1), ",\"g2\":", JB(CAL.DF_SG_1.g2), ",\"g3\":", JB(CAL.DF_SG_1.g3), "},",
  "\"DF_SG_1_contrast_C6\":{\"ab\":", JArr(List(CAL.DF_SG_1_contrast_C6.ab,String)),
    ",\"g1\":", JB(CAL.DF_SG_1_contrast_C6.g1), ",\"g2\":", JB(CAL.DF_SG_1_contrast_C6.g2),
    ",\"note\":\"prereg SS6 text expects C6 to fail G2 ('可換ゆえ(2,3)-生成でない'); MEASURED result disagrees (g2 as computed above) -- this is an observation-only field (C6 is not itself a DF-SG gate), reported verbatim per machine-generated-only discipline, not silently corrected to match the prereg's prose expectation\"},",
  "\"DF_SG_2\":{\"status\":", JStr(CAL.DF_SG_2.status), ",\"ab\":", JArr(List(CAL.DF_SG_2.ab,String)),
    ",\"g1\":", JB(CAL.DF_SG_2.g1), ",\"g2\":", JB(CAL.DF_SG_2.g2), ",\"g3\":", JB(CAL.DF_SG_2.g3), "},",
  "\"DF_SG_2b\":{\"status\":", JStr(CAL.DF_SG_2b.status), ",\"ab\":", JArr(List(CAL.DF_SG_2b.ab,String)),
    ",\"g1\":", JB(CAL.DF_SG_2b.g1), "},",
  "\"DF_SG_3\":{\"status\":", JStr(CAL.DF_SG_3.status), ",",
    "\"order432\":{\"ab\":", JArr(List(CAL.DF_SG_3.order432.ab,String)), ",\"g1\":", JB(CAL.DF_SG_3.order432.g1),
    ",\"g2\":", JB(CAL.DF_SG_3.order432.g2), ",\"g3\":", JB(CAL.DF_SG_3.order432.g3), "},",
    "\"order486\":{\"ab\":", JArr(List(CAL.DF_SG_3.order486.ab,String)), ",\"g1\":", JB(CAL.DF_SG_3.order486.g1),
    ",\"g2\":", JB(CAL.DF_SG_3.order486.g2), ",\"g3\":", JB(CAL.DF_SG_3.order486.g3), "}},",
  "\"DF_SG_4\":{\"status\":", JStr(CAL.DF_SG_4.status), ",\"id\":", JArr(List(CAL.DF_SG_4.id,String)),
    ",\"g1\":", JB(CAL.DF_SG_4.g1), "},",
  "\"DF_SG_5\":{\"status\":", JStr(CAL.DF_SG_5.status), ",\"id\":", JArr(List(CAL.DF_SG_5.id,String)),
    ",\"ab\":", JArr(List(CAL.DF_SG_5.ab,String)), ",\"g1\":", JB(CAL.DF_SG_5.g1), "},",
  "\"DF_SG_6\":{\"status\":", JStr(CAL.DF_SG_6.status),
    ",\"calibration_scan_found\":", JB(CAL.DF_SG_6_calibration_scan.found),
    ",\"final_full_sweep_found\":", JB(DF6_FINAL_FOUND),
    ",\"final_full_sweep_id\":", (function() if DF6_FINAL_ID = fail then return "null"; else return JArr(List(DF6_FINAL_ID,String)); fi; end)(),
    "}}");;

PredictionsJson := Concatenation(
  "{\"P_SGB_1\":{\"rows\":", JArr(List(P_SGB_1_rows, r -> Concatenation(
      "{\"order\":", String(r.order), ",\"i\":", String(r.i), ",\"predicted_rate\":", String(r.predicted_rate),
      ",\"actual_rate\":", String(r.actual_rate), ",\"ratio\":", String(r.ratio),
      ",\"within_factor2\":", JB(r.within_factor2), "}"))),
    ",\"all_within_factor2\":", JB(p_sgb_1_all_within_factor2), "},",
  "\"P_SGB_2\":{\"rows\":", JArr(List(P_SGB_2_rows, r -> Concatenation(
      "{\"order\":", String(r.order), ",\"predicted\":", String(r.predicted), ",\"actual\":", String(r.actual),
      ",\"ratio\":", String(r.ratio), ",\"within_factor2\":", JB(r.within_factor2), "}"))),
    ",\"all_within_factor2\":", JB(p_sgb_2_all_within_factor2), "},",
  "\"P_SGB_3\":{\"sum_scored_orders\":", String(p_sgb_3_sum), ",\"registered_interval\":[900,4000],",
    "\"in_interval\":", JB(p_sgb_3_in_interval), "},",
  "\"P_SGB_4\":{\"total_g3_pass_band\":", String(p_sgb_4_total_g3), ",\"exists_ge_1\":", JB(p_sgb_4_exists),
    ",\"per_order\":", JArr(List(P_SGB_4_rows, r -> Concatenation(
      "{\"order\":", String(r.order), ",\"g3_pass\":", String(r.g3_pass), ",\"point_estimate\":", JStr(r.point_estimate), "}"))), "},",
  "\"P_SGB_5\":{\"g1_sum\":", String(p_sgb_5_g1_sum), ",\"g2_sum\":", String(p_sgb_5_g2_sum),
    ",\"ratio\":", (function() if p_sgb_5_ratio = fail then return "null"; else return String(p_sgb_5_ratio); fi; end)(),
    ",\"registered_interval\":[0.15,0.60],\"in_interval\":", JB(p_sgb_5_in_interval),
    ",\"note\":\"REASONED/低 confidence per prereg SS4.4; a miss here is NOT a stop condition (S-SG-6 exception, explicit)\"},",
  "\"P_SGB_6\":{\"exists_g2pass_g3fail\":", JB(p_sgb_6_exists), ",\"witness_id\":",
    (function() if DF6_FINAL_ID = fail then return "null"; else return JArr(List(DF6_FINAL_ID,String)); fi; end)(), "},",
  "\"P_SGB_7\":{\"note\":\"deferred to G4 (ORB) -- out of scope for this G0-G3 sweep per prereg SS0-5/S-SG-8\"},",
  "\"note_1296_g1\":\"EXCLUDED_PREOBSERVED per prereg SS0-2/SS4.1 -- 1296's G1 count is reported in per_order[] but NOT included in P-SGB-1/2/3 scoring\"}");;

ScopeStatementText := "本掃引が主張できるのは、指数帯(1000,2000]のうち位数が2^i3^j(i,j>=1)型で、かつSmallGroupsにIDつきで収蔵されている5位数(1152・1296・1458・1728・1944)についてのみである。1536(2^9・3)はSCOPE_OUTであり、『空』ではない。q>=5-Sylowが非巡回または非正規の窓(MIRROR-ODDが覆えないもう一方の型)は本帯の外にあり、本掃引は一切触れない。ゆえに『指数(1000,2000]でexoticゼロ』『帯で窓ゼロ』『h^win>2000』と書くことを禁じる。書いてよいのは『帯の2^i3^j型5位数で〜』という限定つきの文だけである。";;

driverSelfSha := ComputeSha256File("search/probe/sg_band_sweep/sg_band_sweep_driver_v1.g");;

cert := Concatenation(
  "{\n",
  "\"schema\":\"shadow-atelier/sg-band-sweep/v1\",\n",
  "\"driver_self_sha256\":", JStr(driverSelfSha), ",\n",
  "\"prereg\":{\"path\":", JStr(PREREG_PATH), ",\"sha256\":", JStr(PreregShaActual), "},\n",
  "\"env\":{\"gap_version\":", JStr(GapVersionStr), ",\"gap_architecture\":", JStr(GapArchStr),
    ",\"heap_flag\":\"-o 2g\",\"execution\":\"local Windows 8GB\"},\n",
  "\"universe_frozen\":", UniverseFrozenJson, ",\n",
  "\"universe_check\":", UniverseCheckJson, ",\n",
  "\"calibration\":", CalibrationJson, ",\n",
  "\"calibration_all_ok\":", JB(CAL_ALL_OK), ",\n",
  "\"time_cap_hit\":", JB(TIME_CAP_HIT), ",\n",
  "\"per_order\":", PerOrderJson, ",\n",
  "\"g3_records\":", G3RecordsJson, ",\n",
  "\"predictions_scored\":", PredictionsJson, ",\n",
  "\"scope_statement\":", JStr(ScopeStatementText), ",\n",
  "\"claims\":{\"exotic_verdict\":\"UNKNOWN\",\"twin_verdict\":\"UNKNOWN\",\"isolated_verdict\":\"UNKNOWN\",",
    "\"note\":\"S-SG-9: no predicted/observed-outcome language for exotic/twin/isolated anywhere -- observation only, grading deferred to 司令塔/数学者\"},\n",
  "\"non_contact_declaration\":{\"im_R\":false,\"d_N\":false,\"sealed_quantities\":false,\"n5_series\":false}\n",
  "}\n");;

OUT_PATH := "search/certs/sg_band_sweep_20260806.json";;
WriteFile(OUT_PATH, cert);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nW6_SG_BAND_SWEEP_DONE\n");
QUIT;

