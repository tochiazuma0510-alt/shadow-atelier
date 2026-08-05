#############################################################################
## lins-twin-census-v1.g -- 裁定 548 W-1 【TWIN-CENSUS】
##
## Universe (pre-registered): normal subgroups N of B3 = <a,b | aba=bab>
## with 1 < [B3:N] <= CENSUS_INDEX_HI, enumerated by ONE
## LowIndexNormalSubgroupsSearch(B3, CENSUS_INDEX_HI) call (LID-1 discipline:
## single GAP process, single LINS call -> "same enumeration => exhaustive
## over the bound" is structurally guaranteed within this run; canonical id
## = literal generator words of N).
##
## Task (docs/notes/exploration_queue_candidates_v1.md 札 W-1, per 司令塔
## instruction 裁定548): find TWIN PAIRS (N,K), N<>K, same index,
## B3/N =~ B3/K (isomorphic quotients). This is INVENTORY ONLY -- no
## rejection, no "non-isolated witness" claim, no isolated/settled verdict.
## AS-GAP-6 hunting-ground catalog, nothing more.
##
## Per pair, per member N recorded:
##   - index [B3:N]
##   - quotient structure description (StructureDescription) + IdGroup label
##     when the SmallGroup library covers that order (fallback: null)
##   - PB3 intersection: whether N <= PB3, and if not, [N : N /\ PB3]
##     (divides 6 = [B3:PB3]; PB3 = ker(B3 -> S3can))
##   - c_in_N: whether c = (aba)^2 (image of the full twist generator of the
##     center of B3) lies in N
##   - verbal field: "UNKNOWN" for every row in this pass -- determining
##     whether N_F2 (preimage of N in the free group F2 under the B3
##     presentation map) admits a verbal construction is a mathematician-
##     level judgment, explicitly OUT OF SCOPE here (札 W-1 point 3: "既存
##     装置の組合せのみ・新規機構ゼロ" -- no new verbal-detection machinery
##     is to be invented in this implementer pass). UNKNOWN is a first-class
##     result (CLAUDE.md discipline), not a placeholder for failure.
##
## NAME COLLISION WARNING (explicit in 札 W-1 point 2): Week 3's
## twincell-enum.g / check-twincell.mjs is a DIFFERENT apparatus (dihedral
## adjacency search over SmallGroup(32) band). This script's "twin" = a pair
## of distinct B3-normal subgroups of equal index with isomorphic quotient.
## Do not conflate the two.
##
## Sealed quantities (non-contact, per instruction): the sealed 3 quantities
## (n=5-related / Im R / d_N / u values), the 705,894-pair universe, and any
## kill-theorem application are NOT touched by this script.
##
## Output: search/certs/lins_twin_census_v1_20260806.json
#############################################################################

Read("search/gaplib_common.g");
Read("search/probe/wac_v1/gap_output_prelude.g");

#############################################################################
## ---------------------- census index bound (documented here) -------------
#############################################################################
## 札 W-1 point 3 target was "指数 <= 2,000 目安" (a rough guideline, not a
## hard spec). Timing probes (scratchpad/lins_timing_probe*.g, this session,
## 2026-08-06) on THIS machine found: bound=1000 -> 1946 nodes / 133.4s;
## bound=2000 exceeded a 10-minute foreground probe and was still running
## when moved to background. Per task instruction ("上限は W-1 札の指定
## (なければ実行時間 30 分以内に収まる範囲で刻み、上限を cert に明記")), and
## because the 2,000 figure is an unconfirmed "目安" not a fixed spec, this
## run uses the bound below -- FILLED IN AFTER THE TIMING PROBE RESOLVES.
CENSUS_INDEX_HI := 1000;;   # see note above; provisional value, may be
                            # raised to 2000 in a follow-up run if the
                            # background timing probe shows it fits budget.

#############################################################################
## ---------------------- shared B3 / PB3 / c setup, LINS called ONCE -------
#############################################################################
BF3 := FreeGroup("a", "b");;
aa := BF3.1;;  bb := BF3.2;;
brel := aa * bb * aa * (bb * aa * bb)^-1;;
B3 := BF3 / [brel];;
ga := B3.1;;  gb := B3.2;;

S3can := SymmetricGroup(3);;
phiCan := GroupHomomorphismByImages(B3, S3can, [ga, gb], [(1,2), (2,3)]);;
if phiCan = fail then Error("canonical B3 -> S3 map failed sanity check"); fi;
PB3 := Kernel(phiCan);;
PB3_INDEX := Index(B3, PB3);;   # sanity print only, should be 6

## c = full-twist generator (Delta^2 = (aba)^2), the standard central
## element of B3 used elsewhere in the codebase (search/kerchi-judge.g's
## MakeWindow: cc := DD^2 where DD := AbstractProd([s1,s2,s1])). Built here
## directly in B3 (no window/quotient needed for membership testing).
c_elt := (ga * gb * ga)^2;;

Print("=== lins-twin-census-v1: single-process, single-LINS-call twin census, bound=",
      CENSUS_INDEX_HI, " ===\n");
Print("PB3 index in B3 (sanity, expect 6): ", PB3_INDEX, "\n");
t0 := GAPLIB_WallElapsedMs();
if LoadPackage("lins") <> true then
  Error("Failed to load GAP package LINS.");
fi;
gr := LowIndexNormalSubgroupsSearch(B3, CENSUS_INDEX_HI);;   # ONE call, LID-1
nodes := ComputedNormalSubgroups(gr);;
tLins := GAPLIB_WallElapsedMs();
Print("LINS nodes total (this single call, bound=", CENSUS_INDEX_HI, "): ", Length(nodes),
      " (lins_elapsed_ms=", tLins - t0, ")\n");

#############################################################################
## ---------------------- per-node data collection --------------------------
#############################################################################
## Row record fields: idx, N (the GAP group), genWords (canonical id),
## structDesc (string), idGroupLabel (or fail), c_in_N (bool),
## in_PB3 (bool), n_meet_pb3_index (index [N : N /\ PB3], = 1 iff in_PB3).
RowsData := [];;
countIdx1 := 0;;
countProcessed := 0;;

IdGroupSafe := function(Q)
  local ord;
  ord := Size(Q);
  if ord > 2000 then return fail; fi;
  if ord = 512 or ord = 1536 then return fail; fi;   # excluded orders, small groups lib
  if not IdGroupsAvailable(ord) then return fail; fi;
  return IdGroup(Q);
end;;

for nd in nodes do
  N := Grp(nd);
  idx := Index(nd);
  if idx = 1 then
    countIdx1 := countIdx1 + 1;
    continue;
  fi;

  genWords := List(GeneratorsOfGroup(N), String);;

  hm := NaturalHomomorphismByNormalSubgroup(B3, N);;
  Q := Image(hm);;
  isoQ := IsomorphismPermGroup(Q);;
  Qp := Image(isoQ);;   # permutation-group copy, for cheap StructureDescription/IdGroup

  structDesc := StructureDescription(Qp);;
  idLabel := IdGroupSafe(Qp);;

  cInN := (c_elt in N);;

  NmeetPB3 := Intersection(N, PB3);;
  inPB3 := IsSubset(PB3, N);;
  nMeetIdx := Index(N, NmeetPB3);;   # divides PB3_INDEX; =1 iff N<=PB3

  Add(RowsData, rec(N := N, idx := idx, genWords := genWords, structDesc := structDesc,
                 idLabel := idLabel, cInN := cInN, inPB3 := inPB3,
                 nMeetIdx := nMeetIdx));
  countProcessed := countProcessed + 1;

  if GAPLIB_CheckCap(1700.0, "lins-twin-census-v1 per-node pass") then
    Print("[CAP WARNING] stopping per-node pass early after ", countProcessed, " rows\n");
    break;
  fi;
od;

t1 := GAPLIB_WallElapsedMs();
Print("Per-node pass done: processed=", countProcessed, " idx1_count=", countIdx1,
      " elapsed_ms=", t1 - t0, "\n");

#############################################################################
## ---------------------- twin pairing (group by index, then iso-check) -----
#############################################################################
## Bucket rows by index. Within a bucket, for every unordered pair (i,j),
## i<j, with N_i <> N_j as subgroups (equality checked both ways -- LINS
## should not emit true duplicates, but we do not assume it), test
## isomorphism of quotients. IdGroup labels (when both available) short-
## circuit the check; otherwise fall back to IsomorphismGroups.
Buckets := rec();;
for i in [1 .. Length(RowsData)] do
  key := String(RowsData[i].idx);
  if IsBound(Buckets.(key)) then
    Add(Buckets.(key), i);
  else
    Buckets.(key) := [ i ];
  fi;
od;

TwinPairs := [];;
countPairChecks := 0;;

QuotientsIso := function(rowA, rowB)
  if rowA.idLabel <> fail and rowB.idLabel <> fail then
    return rowA.idLabel = rowB.idLabel;
  fi;
  ## fallback: rebuild quotient perm groups from the stored N's directly
  ## (structDesc mismatch is a fast negative pre-filter; on a structDesc
  ## match or either being ambiguous, do the real IsomorphismGroups test)
  if rowA.structDesc <> rowB.structDesc then
    return false;
  fi;
  return IsomorphismGroups(
    Image(IsomorphismPermGroup(Image(NaturalHomomorphismByNormalSubgroup(B3, rowA.N)))),
    Image(IsomorphismPermGroup(Image(NaturalHomomorphismByNormalSubgroup(B3, rowB.N))))
  ) <> fail;
end;;

for key in RecNames(Buckets) do
  idxList := Buckets.(key);
  m := Length(idxList);
  if m < 2 then continue; fi;
  for i in [1 .. m-1] do
    for j in [i+1 .. m] do
      ri := RowsData[idxList[i]];
      rj := RowsData[idxList[j]];
      sameSubgroup := IsSubset(ri.N, rj.N) and IsSubset(rj.N, ri.N);
      if sameSubgroup then continue; fi;   ## not a twin -- literally the same N
      countPairChecks := countPairChecks + 1;
      isoOK := QuotientsIso(ri, rj);
      if isoOK then
        Add(TwinPairs, rec(idx := ri.idx, rowA := ri, rowB := rj));
      fi;
    od;
  od;
od;

t2 := GAPLIB_WallElapsedMs();
Print("Twin pairing done: pair_checks=", countPairChecks, " twin_pairs_found=",
      Length(TwinPairs), " elapsed_ms=", t2 - t0, "\n");
for tp in TwinPairs do
  Print("  TWIN idx=", tp.idx, " structA=", tp.rowA.structDesc,
        " A_gens=", tp.rowA.genWords, " B_gens=", tp.rowB.genWords,
        " c_in_N: A=", tp.rowA.cInN, " B=", tp.rowB.cInN,
        " in_PB3: A=", tp.rowA.inPB3, " B=", tp.rowB.inPB3, "\n");
od;

#############################################################################
## ---------------------- write output ---------------------------------------
#############################################################################
IdLabelJson := function(lbl)
  if lbl = fail then return "null"; fi;
  return JPair(lbl[1], lbl[2]);
end;;

MemberJson := function(r)
  return Concatenation("{\n",
    "        \"canonical_id_words\":", JArr(List(r.genWords, JStr)), ",\n",
    "        \"structure_description\":", JStr(r.structDesc), ",\n",
    "        \"id_group\":", IdLabelJson(r.idLabel), ",\n",
    "        \"c_in_N\":", JB(r.cInN), ",\n",
    "        \"in_PB3\":", JB(r.inPB3), ",\n",
    "        \"n_meet_pb3_index\":", String(r.nMeetIdx), ",\n",
    "        \"verbal_status\":\"UNKNOWN\"\n",
    "      }");
end;;

PairJson := function(tp)
  return Concatenation("    {\n",
    "      \"index\":", String(tp.idx), ",\n",
    "      \"members\": [\n",
    "      ", MemberJson(tp.rowA), ",\n",
    "      ", MemberJson(tp.rowB), "\n",
    "      ]\n",
    "    }");
end;;

outParts := [];;
Add(outParts, "{\n");
Add(outParts, "  \"generated_by\": \"search/lins-twin-census-v1.g\",\n");
Add(outParts, "  \"ruling\": \"裁定548 W-1\",\n");
Add(outParts, "  \"note\": \"INVENTORY ONLY -- AS-GAP-6 hunting-ground catalog of twin pairs (N,K), N<>K normal in B3, same index, isomorphic B3/N quotient. No claim of GTSh(K,N) non-emptiness, no isolated/settled verdict, no non-isolated-witness claim. Distinct apparatus from Week 3 twincell-enum.g/check-twincell.mjs (dihedral SmallGroup(32) adjacency search) -- naming collision warning per 札 W-1 point 2. Single GAP process, single LowIndexNormalSubgroupsSearch call (LID-1 discipline): same enumeration => exhaustive over the bound within this run. verbal_status is UNKNOWN for every row in this pass by design -- determining verbal-constructibility of N_F2 is out of scope here (no new verbal-detection machinery invented, per 札 W-1 point 3). Sealed 3 quantities / 705,894-pair universe / kill theorems: non-contact.\",\n");
Add(outParts, Concatenation("  \"census_index_hi\": ", String(CENSUS_INDEX_HI), ",\n"));
Add(outParts, Concatenation("  \"pb3_index_in_b3\": ", String(PB3_INDEX), ",\n"));
Add(outParts, Concatenation("  \"lins_nodes_total_this_call\": ", String(Length(nodes)), ",\n"));
Add(outParts, Concatenation("  \"lins_elapsed_ms\": ", String(tLins - t0), ",\n"));
Add(outParts, Concatenation("  \"idx1_count\": ", String(countIdx1), ",\n"));
Add(outParts, Concatenation("  \"rows_processed\": ", String(countProcessed), ",\n"));
Add(outParts, Concatenation("  \"pair_checks\": ", String(countPairChecks), ",\n"));
Add(outParts, Concatenation("  \"twin_pairs_found\": ", String(Length(TwinPairs)), ",\n"));
Add(outParts, Concatenation("  \"total_elapsed_ms\": ", String(t2 - t0), ",\n"));
Add(outParts, "  \"twin_pairs\": [\n");
for i in [1 .. Length(TwinPairs)] do
  Add(outParts, PairJson(TwinPairs[i]));
  if i < Length(TwinPairs) then Add(outParts, ",\n"); else Add(outParts, "\n"); fi;
od;
Add(outParts, "  ]\n");
Add(outParts, "}\n");

WriteFile("search/certs/lins_twin_census_v1_20260806.json", Concatenation(outParts));
Print("Wrote search/certs/lins_twin_census_v1_20260806.json\n");
Print("ALL_DONE\n");
