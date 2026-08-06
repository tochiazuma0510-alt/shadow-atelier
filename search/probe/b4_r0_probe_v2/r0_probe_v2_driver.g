#############################################################################
## search/probe/b4_r0_probe_v2/r0_probe_v2_driver.g
## R0 probe v2 -- SmallGroups(192) sweep + GQuotients existence test.
## Authority: docs/notes/b4_r0_probe_prereg_iffirst_v2.md (frozen, verbatim
## adherence). Implements P0 (sanity) -> P1 (SG-AB filter) -> P2 (structure
## filter F2) -> P3 (GQuotients existence + Q measurement) -> P4 (window
## confirmation), plus the mandatory filter-soundness spot-check (SS6).
##
## Single GAP lane (【R0v2-GAP-1】 -- candidate/single-system by design; a
## second system is only triggered IF a non-abelian window is found, as a
## separate follow-up task).
##
## OPERATIONAL DEVIATION (executed via 司令塔 instruction, this session):
## local GAP was tied up on a long-running G4/G5 lane with no ETA, so this
## run executes on a GHA ubuntu runner instead of gap.ps1 -o 2g (mirrors the
## disposition already used for b4-r0.yml/v1). Memory flags are passed as
## EXPLICIT BYTE COUNTS (not 'g' suffix notation) as a defense against a
## suspected unit-suffix interpretation difference between the local
## Windows GAP build and the GHA Linux build. Diagnostic note (this
## session's local --help read of gap.exe): -o/--maxworkspace is only a
## WARN threshold ("GAP may allocate more"); the actual hard cap is
## -K/--limitworkspace ("GAP never allocates more"). This is unrelated to
## the frozen mathematical universe of the prereg (base group, PB4 words,
## caps, filters, stopping rules) -- execution-environment only.
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;

Print("=== memory diagnostic (defense against -o suffix interpretation ambiguity) ===\n");
Print("GAPInfo.CommandLineOptions = ", GAPInfo.CommandLineOptions, "\n");
Print("GasmanStatistics() = ", GasmanStatistics(), "\n");

OPERATIONAL_DEVIATION_NOTE := "executed on GHA ubuntu runner (local GAP occupied by long-running G4/G5 lane, no ETA) instead of local gap.ps1 -o 2g; memory flags passed as explicit byte counts (not 'g' suffix) defending against a suspected unit-suffix interpretation difference between local Windows GAP and GHA Linux GAP builds; -o/--maxworkspace confirmed (local --help read) to be a WARN-only threshold, -K/--limitworkspace is the actual hard cap; prereg's frozen mathematical universe (base group SS4.1, PB4 words (A.2), caps SS3.5, filters SS3.2-3.3, stopping rules SS6) is UNCHANGED";;

PREREG_PATH := "docs/notes/b4_r0_probe_prereg_iffirst_v2.md";;
DRIVER_PATH := "search/probe/b4_r0_probe_v2/r0_probe_v2_driver.g";;
OUT_PATH := "search/certs/b4_r0_probe_v2_20260806.json";;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_r0v2_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then Error("sha256 fail for ", relpath); fi;
  return line{[1 .. 64]};
end;;

#############################################################################
## Timing / caps (SS3.5, SS3.3): wall cap 2400000ms, stage caps P1/P2/P3 =
## 600000/600000/1200000ms. Stage-relative elapsed uses GAPLIB_WallElapsedMs
## (wall clock, not CPU -- gaplib_common.g trap (3)).
#############################################################################
WALL_CAP_MS := 2400000;;
STAGE_CAP_P1_MS := 600000;;
STAGE_CAP_P2_MS := 600000;;
STAGE_CAP_P3_MS := 1200000;;

overallStop := false;;
capReason := "";;

#############################################################################
## P0 -- base group + PB4 subgroup + sanity Index=24
#############################################################################
Print("=== P0: B4 presentation + PB4 subgroup sanity ===\n");
F := FreeGroup("a","b","c");;
fa := F.1;; fb := F.2;; fc := F.3;;
rels := [ fa*fc*fa^-1*fc^-1,               ## ac=ca
          fa*fb*fa*(fb*fa*fb)^-1,          ## aba=bab
          fb*fc*fb*(fc*fb*fc)^-1 ];;       ## bcb=cbc
B4fp := F / rels;;
a := B4fp.1;; b := B4fp.2;; c := B4fp.3;;

## PB4 generators (A.2), verbatim from prereg SS4.1
X12 := a^2;;
X23 := b^2;;
X34 := c^2;;
X13 := b*a^2*b^-1;;
X24 := c*b^2*c^-1;;
X14 := c*b*a^2*b^-1*c^-1;;
pbGens := [X12,X13,X14,X23,X24,X34];;
pbNames := ["X12","X13","X14","X23","X24","X34"];;

Delta4sq := (a*b*c)^4;;   ## center generator, per SS4.1

PB4sub := Subgroup(B4fp, pbGens);;
sanityIndex := Index(B4fp, PB4sub);;
Print("Index(B4fp,PB4sub) = ", sanityIndex, "  (expect 24)\n");

if sanityIndex <> 24 then
  Print("STOP: PRESENTATION_BROKEN (S-R0-2')\n");
  cert := Concatenation(
    "{\n\"schema\":\"shadow-atelier/b4-r0-probe-v2/v1\",\n",
    "\"verdict\":\"STOP(PRESENTATION_BROKEN)\",\n",
    "\"sanity\":{\"index_B4_PB4\":", String(sanityIndex), "},\n",
    "\"operational_deviation\":", JStr(OPERATIONAL_DEVIATION_NOTE), ",\n",
    "\"grade\":\"candidate / single-system / not cross-checked / not verified (no Lean)\"\n}\n");;
  WriteFile(OUT_PATH, cert);;
  Print("Wrote ", OUT_PATH, " (STOP)\n");
  QUIT;
fi;

#############################################################################
## S-R0-1': NrSmallGroups(192) must equal 10494 (library-version guard)
#############################################################################
nrSG := NrSmallGroups(192);;
Print("NrSmallGroups(192) = ", nrSG, " (expect 10494)\n");
if nrSG <> 10494 then
  Print("STOP: LIBRARY_MISMATCH (S-R0-1')\n");
  cert := Concatenation(
    "{\n\"schema\":\"shadow-atelier/b4-r0-probe-v2/v1\",\n",
    "\"verdict\":\"STOP(LIBRARY_MISMATCH)\",\n",
    "\"nr_small_groups_192\":", String(nrSG), ",\n",
    "\"sanity\":{\"index_B4_PB4\":", String(sanityIndex), "},\n",
    "\"operational_deviation\":", JStr(OPERATIONAL_DEVIATION_NOTE), ",\n",
    "\"grade\":\"candidate / single-system / not cross-checked / not verified (no Lean)\"\n}\n");;
  WriteFile(OUT_PATH, cert);;
  Print("Wrote ", OUT_PATH, " (STOP)\n");
  QUIT;
fi;

#############################################################################
## P1 -- SG-AB filter: G^ab cyclic, |G^ab| in {2,4}
#############################################################################
Print("\n=== P1: SG-AB filter over ", nrSG, " groups ===\n");
p1Start := GAPLIB_WallElapsedMs();;
p1Passed := [];;
p1UntestedFrom := fail;;
i := 1;;
while i <= nrSG do
  G := SmallGroup(192, i);;
  Aab := G / DerivedSubgroup(G);;
  if IsCyclic(Aab) and Size(Aab) in [2,4] then
    Add(p1Passed, rec(id := i, Gab_size := Size(Aab)));;
  fi;
  if (i mod 500) = 0 then
    Print("  P1 progress: ", i, "/", nrSG, "  passed so far: ", Length(p1Passed),
          "  wall=", GAPLIB_WallElapsedMs() - p1Start, "ms\n");
  fi;
  if (GAPLIB_WallElapsedMs() - p1Start) > STAGE_CAP_P1_MS then
    p1UntestedFrom := i + 1;;
    Print("[CAP EXCEEDED] P1 at i=", i, "\n");
    break;
  fi;
  i := i + 1;;
od;
p1ElapsedMs := GAPLIB_WallElapsedMs() - p1Start;;
Print("P1 done: passed=", Length(p1Passed), " elapsed=", p1ElapsedMs, "ms",
      "  cap_hit=", p1UntestedFrom <> fail, "\n");

if Length(p1Passed) = 0 and p1UntestedFrom = fail then
  Print("STOP: FILTER_TOO_STRONG (S-R0-9') -- P1 passed 0\n");
fi;

#############################################################################
## P2 -- structure filter F2: exists N normal, |N|=8, N nonabelian,
## IdGroup(G/N)=[24,12] (S4)
#############################################################################
Print("\n=== P2: structure filter over ", Length(p1Passed), " P1-survivors ===\n");
p2Start := GAPLIB_WallElapsedMs();;
p2Passed := [];;
p2UntestedIds := [];;
p2CapHit := false;;
j := 1;;
while j <= Length(p1Passed) do
  id := p1Passed[j].id;;
  G := SmallGroup(192, id);;
  cand := [];;
  for N in NormalSubgroups(G) do
    if Size(N) = 8 and not IsAbelian(N) then
      Q := G / N;;
      if IdGroup(Q) = [24,12] then
        AddSet(cand, IdGroup(N));;
      fi;
    fi;
  od;
  if Length(cand) > 0 then
    Add(p2Passed, rec(id := id, N_idgroup := cand));;
  fi;
  if (j mod 50) = 0 then
    Print("  P2 progress: ", j, "/", Length(p1Passed), "  passed so far: ", Length(p2Passed),
          "  wall=", GAPLIB_WallElapsedMs() - p2Start, "ms\n");
  fi;
  if (GAPLIB_WallElapsedMs() - p2Start) > STAGE_CAP_P2_MS then
    p2CapHit := true;;
    p2UntestedIds := List(p1Passed{[j+1 .. Length(p1Passed)]}, r -> r.id);;
    Print("[CAP EXCEEDED] P2 at j=", j, "\n");
    break;
  fi;
  j := j + 1;;
od;
p2ElapsedMs := GAPLIB_WallElapsedMs() - p2Start;;
Print("P2 done: passed=", Length(p2Passed), " elapsed=", p2ElapsedMs, "ms",
      "  cap_hit=", p2CapHit, "\n");

if Length(p2Passed) = 0 and not p2CapHit and Length(p1Passed) > 0 then
  Print("STOP: FILTER_TOO_STRONG (S-R0-9') -- P2 passed 0\n");
fi;

#############################################################################
## P3 -- GQuotients existence + Q measurement
#############################################################################
Print("\n=== P3: GQuotients over ", Length(p2Passed), " P2-survivors ===\n");
p3Start := GAPLIB_WallElapsedMs();;
p3Records := [];;
p3UntestedIds := [];;
p3CapHit := false;;
nonabelianWindows := [];;
k := 1;;
while k <= Length(p2Passed) do
  id := p2Passed[k].id;;
  G := SmallGroup(192, id);;
  epis := GQuotients(B4fp, G);;
  epiRecs := [];;
  for ei in [1 .. Length(epis)] do
    phi := epis[ei];;
    qgens := List(pbGens, x -> Image(phi, x));;
    Q := Subgroup(G, qgens);;
    Qsize := Size(Q);;
    Qab := IsAbelian(Q);;
    Qid := fail;;
    if Qsize > 0 then
      Qid := IdGroup(Q);;
    fi;
    d2img := Image(phi, Delta4sq);;
    d2InN := (d2img = One(G));;
    sigOrders := [ Order(Image(phi,a)), Order(Image(phi,b)), Order(Image(phi,c)) ];;
    isWindow := (Qsize = 8) and (not Qab);;
    Add(epiRecs, rec(epi_index := ei, Q_order := Qsize, Q_idgroup := Qid,
        Q_is_abelian := Qab, delta2_in_N := d2InN, sigma_orders := sigOrders,
        is_window := isWindow));;
    if isWindow then
      Add(nonabelianWindows, rec(smallgroup_id := id, epi_index := ei,
          Gab_size := (First(p1Passed, r -> r.id = id)).Gab_size,
          N_idgroup := (First(p2Passed, r -> r.id = id)).N_idgroup,
          n_epis := Length(epis), Q_order := Qsize, Q_idgroup := Qid,
          Q_is_abelian := Qab, delta2_in_N := d2InN, sigma_orders := sigOrders,
          Nt_index := 192));;
      Print("  *** WINDOW CANDIDATE: id=", id, " epi=", ei, " Q_idgroup=", Qid, " ***\n");
    fi;
  od;
  Add(p3Records, rec(smallgroup_id := id, n_epis := Length(epis), epis := epiRecs));;
  Print("  P3: id=", id, " n_epis=", Length(epis), " wall=", GAPLIB_WallElapsedMs() - p3Start, "ms\n");
  if (GAPLIB_WallElapsedMs() - p3Start) > STAGE_CAP_P3_MS then
    p3CapHit := true;;
    p3UntestedIds := List(p2Passed{[k+1 .. Length(p2Passed)]}, r -> r.id);;
    Print("[CAP EXCEEDED] P3 at k=", k, "\n");
    break;
  fi;
  k := k + 1;;
od;
p3ElapsedMs := GAPLIB_WallElapsedMs() - p3Start;;
Print("P3 done: groups_processed=", Length(p3Records), " windows=", Length(nonabelianWindows),
      " elapsed=", p3ElapsedMs, "ms  cap_hit=", p3CapHit, "\n");

anyCapHit := (p1UntestedFrom <> fail) or p2CapHit or p3CapHit;;

#############################################################################
## SS6 -- mandatory filter-soundness spot-check: 20 random from P1-rejected,
## 20 random from P2-rejected, run GQuotients(B4fp,G) DIRECTLY and confirm
## no window emerges. Fixed seed for reproducibility (recorded in cert).
#############################################################################
Print("\n=== filter-soundness spot-check ===\n");
SPOTCHECK_SEED := 20260806;;
Reset(GlobalMersenneTwister, SPOTCHECK_SEED);;

SampleWithoutReplacement := function(lst, kk)
  local pool, result, idx;
  pool := ShallowCopy(lst);;
  result := [];;
  while Length(result) < kk and Length(pool) > 0 do
    idx := Random(GlobalMersenneTwister, [1 .. Length(pool)]);;
    Add(result, pool[idx]);;
    Remove(pool, idx);;
  od;
  return result;
end;;

p1PassedIds := List(p1Passed, r -> r.id);;
if p1UntestedFrom = fail then
  p1TestedIds := [1 .. nrSG];;
else
  p1TestedIds := [1 .. p1UntestedFrom - 1];;
fi;
p1RejectedPool := Filtered(p1TestedIds, x -> not (x in p1PassedIds));;

p2PassedIds := List(p2Passed, r -> r.id);;
p2RejectedPool := Filtered(p1PassedIds, x -> not (x in p2PassedIds) and not (x in p2UntestedIds));;

spotP1Sample := SampleWithoutReplacement(p1RejectedPool, 20);;
spotP2Sample := SampleWithoutReplacement(p2RejectedPool, 20);;

SpotCheckOne := function(id)
  local G, epis, ei, phi, qgens, Q, hasWindow;
  G := SmallGroup(192, id);;
  epis := GQuotients(B4fp, G);;
  hasWindow := false;;
  for ei in [1 .. Length(epis)] do
    phi := epis[ei];;
    qgens := List(pbGens, x -> Image(phi, x));;
    Q := Subgroup(G, qgens);;
    if Size(Q) = 8 and not IsAbelian(Q) then
      hasWindow := true;;
    fi;
  od;
  return rec(id := id, n_epis := Length(epis), window_found := hasWindow);;
end;;

spotP1Results := List(spotP1Sample, SpotCheckOne);;
spotP2Results := List(spotP2Sample, SpotCheckOne);;

spotAllClear := ForAll(spotP1Results, r -> not r.window_found) and
                ForAll(spotP2Results, r -> not r.window_found);;
Print("spot-check P1-rejected: ", Length(spotP1Results), " sampled, all_clear=",
      ForAll(spotP1Results, r -> not r.window_found), "\n");
Print("spot-check P2-rejected: ", Length(spotP2Results), " sampled, all_clear=",
      ForAll(spotP2Results, r -> not r.window_found), "\n");

filterUnsound := not spotAllClear;;

#############################################################################
## Verdict (SS6 table)
#############################################################################
totalElapsedMs := GAPLIB_WallElapsedMs();;
verdict := "";;
if filterUnsound then
  verdict := "STOP(FILTER_UNSOUND)";;
elif anyCapHit then
  verdict := "UNKNOWN(partial)";;
elif Length(nonabelianWindows) > 0 then
  verdict := "NONABELIAN_WINDOW_FOUND";;
else
  verdict := "NOT_FOUND_AT_192";;
fi;
Print("\nVERDICT: ", verdict, "  total_elapsed_ms=", totalElapsedMs, "\n");

#############################################################################
## Cert assembly
#############################################################################
gapVersionStr := GAPInfo.Version;;
smallgrpVersionStr := "builtin-library";;

P1PassedJson := JArr(List(p1Passed, r -> Concatenation(
  "{\"id\":", String(r.id), ",\"Gab_size\":", String(r.Gab_size), "}")));;

P2PassedJson := JArr(List(p2Passed, r -> Concatenation(
  "{\"id\":", String(r.id), ",\"N_idgroup\":", JArr(List(r.N_idgroup, p -> JPair(p[1],p[2]))), "}")));;

QIdJson := function(qid)
  if qid = fail then return "null"; else return JPair(qid[1],qid[2]); fi;
end;;

EpiRecJson := function(er)
  return Concatenation(
    "{\"epi_index\":", String(er.epi_index),
    ",\"Q_order\":", String(er.Q_order),
    ",\"Q_idgroup\":", QIdJson(er.Q_idgroup),
    ",\"Q_is_abelian\":", JB(er.Q_is_abelian),
    ",\"delta2_in_N\":", JB(er.delta2_in_N),
    ",\"sigma_orders\":", JArr(List(er.sigma_orders,String)),
    ",\"is_window\":", JB(er.is_window), "}");
end;;

P3Json := JArr(List(p3Records, function(pr)
  ## NOTE: P2 only checks ABSTRACT factor-structure existence (a normal N
  ## with the right IdGroup); GQuotients on the CONCRETE B4fp presentation
  ## is a strictly stronger existence test and can legitimately return an
  ## empty list for a P2-survivor. Guard against pr.epis=[] (empty-list
  ## indexing would otherwise error here).
  if Length(pr.epis) = 0 then
    return Concatenation(
      "{\"smallgroup_id\":", String(pr.smallgroup_id),
      ",\"n_epis\":0,\"Q_order\":null,\"Q_idgroup\":null,\"Q_is_abelian\":null",
      ",\"delta2_in_N\":null,\"sigma_orders\":null,\"epis_detail\":[]}");
  fi;
  return Concatenation(
    "{\"smallgroup_id\":", String(pr.smallgroup_id),
    ",\"n_epis\":", String(pr.n_epis),
    ",\"Q_order\":", String(pr.epis[1].Q_order),
    ",\"Q_idgroup\":", QIdJson(pr.epis[1].Q_idgroup),
    ",\"Q_is_abelian\":", JB(pr.epis[1].Q_is_abelian),
    ",\"delta2_in_N\":", JB(pr.epis[1].delta2_in_N),
    ",\"sigma_orders\":", JArr(List(pr.epis[1].sigma_orders,String)),
    ",\"epis_detail\":", JArr(List(pr.epis, EpiRecJson)), "}");
end));;

NonabWinJson := JArr(List(nonabelianWindows, function(w)
  return Concatenation(
    "{\"smallgroup_id\":", String(w.smallgroup_id),
    ",\"epi_index\":", String(w.epi_index),
    ",\"Gab_size\":", String(w.Gab_size),
    ",\"N_idgroup\":", JArr(List(w.N_idgroup, p -> JPair(p[1],p[2]))),
    ",\"n_epis\":", String(w.n_epis),
    ",\"Q_order\":", String(w.Q_order),
    ",\"Q_idgroup\":", QIdJson(w.Q_idgroup),
    ",\"Q_is_abelian\":", JB(w.Q_is_abelian),
    ",\"delta2_in_N\":", JB(w.delta2_in_N),
    ",\"sigma_orders\":", JArr(List(w.sigma_orders,String)),
    ",\"Nt_index\":", String(w.Nt_index), "}");
end));;

p1UntestedJson := "[]";;
if p1UntestedFrom <> fail then
  p1UntestedJson := JArr(List([p1UntestedFrom .. nrSG], String));;
fi;
p2UntestedJson := JArr(List(p2UntestedIds, String));;
p3UntestedJson := JArr(List(p3UntestedIds, String));;

SpotRecJson := function(r)
  return Concatenation("{\"id\":", String(r.id), ",\"n_epis\":", String(r.n_epis),
      ",\"window_found\":", JB(r.window_found), "}");
end;;
SpotP1Json := JArr(List(spotP1Results, SpotRecJson));;
SpotP2Json := JArr(List(spotP2Results, SpotRecJson));;

selfSha := ComputeSha256File(DRIVER_PATH);;
preregSha := ComputeSha256File(PREREG_PATH);;

cert := Concatenation(
"{\n",
"\"schema\":\"shadow-atelier/b4-r0-probe-v2/v1\",\n",
"\"driver_self_sha256\":", JStr(selfSha), ",\n",
"\"prereg_doc_sha256\":", JStr(preregSha), ",\n",
"\"prereg_version\":\"v2 (SmallGroups-192 sweep; supersedes-method-only of v1)\",\n",
"\"gap_version\":", JStr(gapVersionStr), ",\n",
"\"smallgrp_version\":", JStr(smallgrpVersionStr), ",\n",
"\"nr_small_groups_192\":", String(nrSG), ",\n",
"\"base_group\":\"B4 = <a,b,c | aba=bab, bcb=cbc, ac=ca>\",\n",
"\"pb4_generators\":", JArr(List(pbNames, JStr)), ",\n",
"\"sanity\":{\"index_B4_PB4\":", String(sanityIndex), "},\n",
"\"wall_cap_ms\":", String(WALL_CAP_MS), ",\n",
"\"stage_caps_ms\":{\"P1\":", String(STAGE_CAP_P1_MS), ",\"P2\":", String(STAGE_CAP_P2_MS), ",\"P3\":", String(STAGE_CAP_P3_MS), "},\n",
"\"stage_elapsed_ms\":{\"P1\":", String(p1ElapsedMs), ",\"P2\":", String(p2ElapsedMs), ",\"P3\":", String(p3ElapsedMs), "},\n",
"\"total_elapsed_ms\":", String(totalElapsedMs), ",\n",
"\"p1_passed\":", P1PassedJson, ",\n",
"\"p1_passed_count\":", String(Length(p1Passed)), ",\n",
"\"p2_passed\":", P2PassedJson, ",\n",
"\"p2_passed_count\":", String(Length(p2Passed)), ",\n",
"\"p3\":", P3Json, ",\n",
"\"filter_soundness_spotcheck\":{\"seed\":", String(SPOTCHECK_SEED),
  ",\"p1_rejected_sampled\":", SpotP1Json,
  ",\"p2_rejected_sampled\":", SpotP2Json,
  ",\"all_clear\":", JB(spotAllClear), "},\n",
"\"nonabelian_windows\":", NonabWinJson, ",\n",
"\"windows_count\":", String(Length(nonabelianWindows)), ",\n",
"\"cap_hit\":{\"P1\":", JB(p1UntestedFrom <> fail), ",\"P2\":", JB(p2CapHit), ",\"P3\":", JB(p3CapHit), "},\n",
"\"untested_ids\":{\"P1\":", p1UntestedJson, ",\"P2\":", p2UntestedJson, ",\"P3\":", p3UntestedJson, "},\n",
"\"verdict\":", JStr(verdict), ",\n",
"\"grade\":\"candidate / single-system / not cross-checked / not verified (no Lean)\",\n",
"\"scope_declaration\":{\"iota\":false,\"twins\":false,\"gtshadow_predicates\":false,\"sealed_quantities\":false},\n",
"\"authority\":\"docs/notes/b4_r0_probe_prereg_iffirst_v2.md (frozen, verbatim), executed per instruction\",\n",
"\"operational_deviation\":", JStr(OPERATIONAL_DEVIATION_NOTE), "\n",
"}\n");;

WriteFile(OUT_PATH, cert);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nR0_PROBE_V2_DONE\n");
QUIT;
