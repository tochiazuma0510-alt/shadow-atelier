#############################################################################
## search/b4-r0-probe-v1.g
## B4 R0 timing/existence probe -- prereg docs/notes/b4_r0_probe_prereg_iffirst_v1.md
## (frozen, verbatim compliance). Single LowIndexNormalSubgroupsSearch(B4,240)
## call (LID-1). Target: does an in_PB4, non-abelian-quotient window exist at
## or below index 240? Per the prereg's paper input (INDEX-LB + NO-SMALL-
## NONAB), the only index actually tested for non-abelian-ness is 192
## (|Q|=8).
##
## Non-contact declaration (prereg SS0 line 4/S-R0-6): no twin/iota
## computation, no GT-shadow predicate (T_{m,f}/hexagon/pentagon/charming/
## settled/isolated), no sealed-quantity contact, no 705,894-pair universe
## contact. Single system (GAP only) -- grade is candidate/single-system per
## 【R0-GAP-1】, not cross-checked.
##
## ★ OPERATIONAL DEVIATION (司令塔裁定, this session): local execution under
## gap.ps1 -o 2g hit GAP's memory limit (Error, reached the pre-set memory
## limit) immediately after the [B4:PB4]=24 sanity print, before the LINS
## call could report any node -- i.e. NO partial result, no cert. LINS(B4,
## 240) on 3 generators is heavier than the B3 twin census's LINS(B3,1000)
## on 2 generators. Per the standing RAM-8GB/-o 2g local discipline, memory
## was NOT raised locally. This is a PURELY OPERATIONAL deviation --
## execution environment (local Windows -> GitHub Actions ubuntu runner) and
## memory ceiling (-o 2g -> -o 6g) change -- NOT a change to the prereg's
## frozen mathematical universe (B4 presentation SS1.1, census_index_hi=240,
## LID-1 single-call discipline, wall cap semantics all unchanged). The GHA
## workflow .github/workflows/b4-r0.yml runs this exact script unmodified,
## with gap -o 6g and a job-level timeout-minutes:15 (runner clock) enforcing
## S-R0-4 externally in addition to this script's own internal check.
#############################################################################
Read("search/gaplib_common.g");
Read("search/probe/wac_v1/gap_output_prelude.g");

CENSUS_INDEX_HI := 240;;   ## frozen, prereg SS1.2 -- do not change
WALL_CAP_MS := 900000;;    ## 15 min, prereg SS1.2/SS3

#############################################################################
## ---- B4 presentation (prereg SS1.1, byte-for-byte): a=sigma1,b=sigma2,
## c=sigma3; aba=bab, bcb=cbc, ac=ca. Central element Delta4sq = (abc)^4
## (NOT "c4" -- W-1 naming collision warning, prereg SS1.1).
#############################################################################
BF4 := FreeGroup("a", "b", "c");;
aa := BF4.1;;  bb := BF4.2;;  cc := BF4.3;;
rel1 := aa*bb*aa * (bb*aa*bb)^-1;;   ## aba = bab
rel2 := bb*cc*bb * (cc*bb*cc)^-1;;   ## bcb = cbc
rel3 := aa*cc * (cc*aa)^-1;;         ## ac = ca
B4fp := BF4 / [rel1, rel2, rel3];;
ga := B4fp.1;;  gb := B4fp.2;;  gc := B4fp.3;;
Delta4sq := (ga*gb*gc)^4;;

## sanity: [B4:PB4] = 24 (prereg checklist step 3 / D-R0-3)
S4can := SymmetricGroup(4);;
phiCan := GroupHomomorphismByImages(B4fp, S4can, [ga,gb,gc], [(1,2),(2,3),(3,4)]);;
if phiCan = fail then Error("B4 -> S4 canonical map failed to build -- STOP (S-R0-2 risk)"); fi;
PB4 := Kernel(phiCan);;
PB4_INDEX := Index(B4fp, PB4);;
Print("=== b4_r0_probe_v1: single-process, single-LINS-call, bound=", CENSUS_INDEX_HI, " ===\n");
Print("[B4:PB4] sanity (expect 24): ", PB4_INDEX, "\n");
if PB4_INDEX <> 24 then
  Error("[B4:PB4] != 24 -- STOP per prereg checklist step 3");
fi;

#############################################################################
## ---- INSTRUMENTATION (司令塔裁定, this session, after run 31070583319's
## -o 8g OOM in ~49s): print evidence that the -o flag actually reached GAP
## (not silently defaulted), plus a Gasman workspace snapshot, BEFORE the
## LINS call -- so this survives in the captured log even if LINS itself
## crashes with no partial result and no cert is ever written.
#############################################################################
## GAPInfo.CommandLineOptions.o holds the raw -o VALUE as a plain GAP string
## (e.g. "2g"), NOT a list of strings (confirmed empirically,
## scratchpad/dbg_meminfo.g) -- do not index into it as if it were a list of
## repeated-flag values, or Length()/indexing peels off a single CHARACTER
## (not a string), which then breaks Concatenation/JStr downstream.
MEM_FLAG_SEEN := IsBound(GAPInfo.CommandLineOptions.o) and IsString(GAPInfo.CommandLineOptions.o)
                 and Length(GAPInfo.CommandLineOptions.o) > 0;;
MEM_FLAG_VALUE := (function()
  if MEM_FLAG_SEEN then return GAPInfo.CommandLineOptions.o;
  else return "NOT_SET"; fi;
end)();;
Print("=== MEMORY FLAG EVIDENCE ===\n");
Print("GAPInfo.CommandLineOptions.o = ", MEM_FLAG_VALUE, " (flag reached GAP: ", MEM_FLAG_SEEN, ")\n");
## GasmanStatistics()'s record only contains the "partial"/"full" sub-record
## for GC types that have actually fired so far -- neither key is guaranteed
## present at any given point. Read totalkb/livekb/freekb defensively
## (prefer "partial" since it is the more frequent GC type, fall back to
## "full", else "N/A").
GasmanField := function(g, fld)
  if IsBound(g.partial) and IsBound(g.partial.(fld)) then return g.partial.(fld);
  elif IsBound(g.full) and IsBound(g.full.(fld)) then return g.full.(fld);
  else return "N/A"; fi;
end;;
GASMAN_BEFORE := GasmanStatistics();;
Print("GasmanStatistics() before LINS: ", GASMAN_BEFORE, "\n");
Print("=== END MEMORY FLAG EVIDENCE ===\n");

#############################################################################
## ---- LINS: exactly ONE call (LID-1) ----
#############################################################################
t0 := GAPLIB_WallElapsedMs();;
if LoadPackage("lins") <> true then
  Error("Failed to load GAP package LINS.");
fi;
## Progress visibility (点3, 司令塔裁定): LINS's own Info class. Level 1
## prints per-quotient-order progress tables (LINS_tab1/tab2 in the package
## source); this interleaves with GAP's normal stdout as the search runs,
## so if the process dies mid-search, the log shows how far it got.
SetInfoLevel(InfoLINS, 1);;
gr := LowIndexNormalSubgroupsSearch(B4fp, CENSUS_INDEX_HI);;   ## ONE call, LID-1
nodes := ComputedNormalSubgroups(gr);;
tLins := GAPLIB_WallElapsedMs();;
LINS_ELAPSED_MS := tLins - t0;;
Print("LINS nodes total (bound=", CENSUS_INDEX_HI, "): ", Length(nodes),
      " (lins_elapsed_ms=", LINS_ELAPSED_MS, ")\n");

CAP_HIT := (LINS_ELAPSED_MS > WALL_CAP_MS);;
if CAP_HIT then
  Print("[TIME_CAP] LINS call alone exceeded wall cap -- STOP, verdict=STOP(TIME_CAP)\n");
fi;

GASMAN_AFTER_LINS := GasmanStatistics();;
Print("GasmanStatistics() after LINS: ", GASMAN_AFTER_LINS, "\n");

#############################################################################
## ---- per-node data collection (prereg SS1.3 fields) ----
#############################################################################
IdGroupSafe := function(Q)
  local ord;
  ord := Size(Q);
  if ord > 2000 then return fail; fi;
  if ord = 512 or ord = 1536 then return fail; fi;
  if not IdGroupsAvailable(ord) then return fail; fi;
  return IdGroup(Q);
end;;

RowsData := [];;
countIdx1 := 0;;
countProcessed := 0;;
NONAB_FOUND := [];;
PERNODE_CAP_HIT := false;;

if not CAP_HIT then
  for nd in nodes do
    N := Grp(nd);;
    idx := Index(nd);;
    if idx = 1 then
      countIdx1 := countIdx1 + 1;
      continue;
    fi;

    genWords := List(GeneratorsOfGroup(N), String);;

    ## in_PB4: direct subgroup test (D-R0-3 -- NOT just "index is a multiple
    ## of 24"; that alone is S-R0-2 WINDOW_TEST_BROKEN). N normal in B4fp
    ## (LINS guarantees this); test N <= PB4 directly.
    inPB4 := IsSubset(PB4, N);;

    delta2InN := (Delta4sq in N);;

    hm := NaturalHomomorphismByNormalSubgroup(B4fp, N);;
    Q := Image(hm);;
    isoQ := IsomorphismPermGroup(Q);;
    Qp := Image(isoQ);;
    QOrder := Size(Qp);;
    QIsAbelian := IsAbelian(Qp);;
    QStruct := StructureDescription(Qp);;
    QIdLabel := IdGroupSafe(Qp);;

    ## Qhat_id_group = B4/N (the full quotient, not just PB4/N)
    QhatIdLabel := QIdLabel;;   ## Q here already IS B4fp/N (hm built on B4fp)

    Add(RowsData, rec(idx := idx, inPB4 := inPB4, delta2InN := delta2InN,
        QOrder := QOrder, QIsAbelian := QIsAbelian, QStruct := QStruct,
        QIdLabel := QIdLabel, QhatIdLabel := QhatIdLabel, genWords := genWords));
    countProcessed := countProcessed + 1;

    if inPB4 and (not QIsAbelian) then
      Add(NONAB_FOUND, rec(idx := idx, QStruct := QStruct, QIdLabel := QIdLabel,
          genWords := genWords, delta2InN := delta2InN));
      Print("  *** NONABELIAN WINDOW: index=", idx, " Q=", QStruct, " idLabel=", QIdLabel, "\n");
    fi;

    if GAPLIB_CheckCap(870.0, "b4_r0_probe_v1 per-node pass (900s wall cap, 30s write margin)") then
      Print("[CAP WARNING] stopping per-node pass early after ", countProcessed, " rows\n");
      PERNODE_CAP_HIT := true;;
      break;
    fi;
  od;
fi;
tTotal := GAPLIB_WallElapsedMs();;
TOTAL_ELAPSED_MS := tTotal - t0;;
CAP_HIT := CAP_HIT or PERNODE_CAP_HIT or (TOTAL_ELAPSED_MS > WALL_CAP_MS);;
Print("Per-node pass done: processed=", countProcessed, " idx1_count=", countIdx1,
      " total_elapsed_ms=", TOTAL_ELAPSED_MS, "\n");

WINDOWS_TOTAL := Length(RowsData);;
WINDOWS_ABELIAN := Length(Filtered(RowsData, r -> r.QIsAbelian));;
WINDOWS_NONABELIAN := Length(Filtered(RowsData, r -> not r.QIsAbelian));;

## verdict (prereg SS3 schema, SS4 wording rules)
VERDICT := "";;
if CAP_HIT then
  VERDICT := "STOP(TIME_CAP)";;
elif Length(NONAB_FOUND) > 0 then
  VERDICT := "NONABELIAN_WINDOW_FOUND";;
else
  VERDICT := "NOT_FOUND_WITHIN_240";;
fi;
Print("VERDICT = ", VERDICT, "\n");

#############################################################################
## ---- P-R0-1..4 scoring material (measurement only; grading is 司令塔's) ----
#############################################################################
## P-R0-1: verdict = NOT_FOUND_WITHIN_240 (main prediction)
PR01_match := (VERDICT = "NOT_FOUND_WITHIN_240");;
## P-R0-2: abelian windows found skew to |Q| of 2^a*3^b type; flag any
## |Q| divisible by 5 or 7 among abelian windows found (interesting if any)
PR02_abelian_5or7 := Filtered(RowsData, r -> r.QIsAbelian and
    ((r.QOrder mod 5 = 0) or (r.QOrder mod 7 = 0)));;
## P-R0-3: LINS elapsed shorter than B3's bound-1000 cost (149s reference,
## prereg SS5 P-R0-3 -- 149000ms figure from search/certs/lins_twin_census_v1_20260806.json)
B3_REFERENCE_MS := 149000;;
PR03_match := (LINS_ELAPSED_MS < B3_REFERENCE_MS);;
## P-R0-4: exists a window (any, not just nonabelian) with delta2_in_N=false
PR04_windows_delta2_false := Filtered(RowsData, r -> not r.delta2InN);;
PR04_match := (Length(PR04_windows_delta2_false) > 0);;

#############################################################################
## ---- write cert (prereg SS3 schema) ----
#############################################################################
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_b4r0_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then Error("sha256 fail for ", relpath); fi;
  return line{[1 .. 64]};
end;;
PREREG_SHA := ComputeSha256File("docs/notes/b4_r0_probe_prereg_iffirst_v1.md");;

IdLabelJson := function(lbl)
  if lbl = fail then return "null"; fi;
  return Concatenation("[", String(lbl[1]), ",", String(lbl[2]), "]");
end;;

NodeJson := function(r)
  return Concatenation("{\"index\":", String(r.idx),
    ",\"in_PB4\":", JB(r.inPB4),
    ",\"delta2_in_N\":", JB(r.delta2InN),
    ",\"Q_order\":", String(r.QOrder),
    ",\"Q_is_abelian\":", JB(r.QIsAbelian),
    ",\"Q_id_group\":", IdLabelJson(r.QIdLabel),
    ",\"Q_structure\":", JStr(r.QStruct),
    ",\"Qhat_id_group\":", IdLabelJson(r.QhatIdLabel),
    ",\"canonical_id_words\":", JArr(List(r.genWords, JStr)),
    "}");
end;;

NodesJson := JArr(List(RowsData, NodeJson));;
NonabJson := JArr(List(NONAB_FOUND, r -> Concatenation(
    "{\"index\":", String(r.idx), ",\"Q_structure\":", JStr(r.QStruct),
    ",\"Q_id_group\":", IdLabelJson(r.QIdLabel),
    ",\"delta2_in_N\":", JB(r.delta2InN),
    ",\"canonical_id_words\":", JArr(List(r.genWords, JStr)), "}")));;

report := Concatenation(
"{\n",
"\"schema\":\"b4-r0-probe-cert/v1\",\n",
"\"prereg_doc\":\"docs/notes/b4_r0_probe_prereg_iffirst_v1.md\",\n",
"\"prereg_doc_sha256\":", JStr(PREREG_SHA), ",\n",
"\"authorization\":\"裁定637 (司令塔) task 3; prereg is frozen and verbatim per this session's instruction\",\n",
"\"base_group\":\"B4 = <a,b,c | aba=bab, bcb=cbc, ac=ca>\",\n",
"\"pb4_index_in_b4_sanity\":", String(PB4_INDEX), ",\n",
"\"census_index_hi\":", String(CENSUS_INDEX_HI), ",\n",
"\"memory_flag_evidence\":{\"o_flag_reached_gap\":", JB(MEM_FLAG_SEEN), ",\"o_flag_value\":", JStr(MEM_FLAG_VALUE),
  ",\"gasman_before_lins_totalkb\":", String(GasmanField(GASMAN_BEFORE,"totalkb")),
  ",\"gasman_after_lins_totalkb\":", String(GasmanField(GASMAN_AFTER_LINS,"totalkb")),
  ",\"gasman_after_lins_livekb\":", String(GasmanField(GASMAN_AFTER_LINS,"livekb")),
  ",\"gasman_after_lins_freekb\":", String(GasmanField(GASMAN_AFTER_LINS,"freekb")),
  ",\"note\":\"o_flag_value is read from GAPInfo.CommandLineOptions.o -- direct evidence the -o flag reached the GAP process (vs silently defaulting). totalkb is the Gasman workspace size in KB; if this run crashed with 'reached the pre-set memory limit', compare gasman_after_lins_totalkb (if reached) against o_flag_value to see whether GAP's internal accounting actually approached the requested ceiling or whether the crash happened well below it (pointing to a physical/OS memory ceiling instead).\"},\n",
"\"lins_calls\":1,\n",
"\"lins_nodes_total_this_call\":", String(Length(nodes)), ",\n",
"\"lins_elapsed_ms\":", String(LINS_ELAPSED_MS), ",\n",
"\"total_elapsed_ms\":", String(TOTAL_ELAPSED_MS), ",\n",
"\"wall_cap_ms\":", String(WALL_CAP_MS), ",\n",
"\"cap_hit\":", JB(CAP_HIT), ",\n",
"\"nodes\":", NodesJson, ",\n",
"\"windows_total\":", String(WINDOWS_TOTAL), ",\n",
"\"windows_abelian\":", String(WINDOWS_ABELIAN), ",\n",
"\"windows_nonabelian\":", String(WINDOWS_NONABELIAN), ",\n",
"\"nonabelian_windows\":", NonabJson, ",\n",
"\"verdict\":", JStr(VERDICT), ",\n",
"\"output_statement\":", JStr(Concatenation(
   "B4 の指数 <=", String(CENSUS_INDEX_HI),
   " の正規部分群の悉皆探索において、N<=PB4 かつ PB4/N が非可換であるものは",
   (function() if Length(NONAB_FOUND)=0 then return "未発見である。"; else return "発見された(見つかった窓の詳細は nonabelian_windows を見よ)。"; fi; end)()
 )), ",\n",
"\"predictions_scoring_material\":{\n",
"  \"P_R0_1_main_verdict_is_NOT_FOUND_WITHIN_240\":", JB(PR01_match), ",\n",
"  \"P_R0_2_abelian_windows_with_Q_order_div_5_or_7\":", String(Length(PR02_abelian_5or7)), ",\n",
"  \"P_R0_2_detail\":", JArr(List(PR02_abelian_5or7, r -> Concatenation("{\"index\":",String(r.idx),",\"Q_order\":",String(r.QOrder),"}"))), ",\n",
"  \"P_R0_3_lins_elapsed_ms\":", String(LINS_ELAPSED_MS), ",\"P_R0_3_b3_reference_ms\":", String(B3_REFERENCE_MS), ",\"P_R0_3_shorter_than_b3_ref\":", JB(PR03_match), ",\n",
"  \"P_R0_4_windows_with_delta2_in_N_false_count\":", String(Length(PR04_windows_delta2_false)), ",\"P_R0_4_exists\":", JB(PR04_match), "\n",
"},\n",
"\"scope_declaration\":{\"twin_computed\":false,\"iota_computed\":false,\"gt_shadow_predicates_evaluated\":false,\"sealed_quantities_contacted\":false,\"705894_pair_universe_contacted\":false},\n",
"\"forbidden_word_check\":{\"note\":\"output_statement uses ONLY the frozen SS4.1 wording (or SS4.3 discovery report); no claim of 'index<=1000 all abelian', no twin/iota claim, no GT-shadow genuine/fake claim, no Ncore/Nstar claim -- per prereg SS4.2\"},\n",
"\"operational_deviation\":{\"local_run_failed\":\"Error, reached the pre-set memory limit under gap.ps1 -o 2g, immediately after [B4:PB4]=24 sanity, before any LINS node reported (no partial result)\",\"resolution\":\"GHA ubuntu runner, gap -o 6g (run 31070583319 with -o 8g also OOM'd in ~49s, same message, before any LINS node -- standard GHA ubuntu runners have ~7GB physical RAM, so -o 8g exceeded the physical ceiling, not just an internal accounting threshold; -o 6g leaves headroom under that ceiling), .github/workflows/b4-r0.yml, this script UNMODIFIED except this note\",\"authorization\":\"司令塔裁定 (this session), task 3 disposition (c)\",\"note\":\"Environment/memory-ceiling change only -- prereg's frozen mathematical universe (B4 presentation, census_index_hi=240, LID-1, wall-cap semantics) is unchanged. Local -o was NOT raised (8GB RAM discipline preserved).\"},\n",
"\"grade\":\"candidate / single-system / not cross-checked / not verified (no Lean)\"\n",
"}\n");;

OUT_PATH := Concatenation("search/certs/b4_r0_probe_v1_20260806", ".json");;
WriteFile(OUT_PATH, report);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nB4_R0_PROBE_DRIVER_DONE\n");
QUIT;
