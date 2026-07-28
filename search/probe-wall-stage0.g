#############################################################################
## probe-wall-stage0.g
##
## Wall-solver pre-probe: size measurement only, no mathematical claim.
## Uses GAP package LINS (LowIndexNormalSubgroupsSearch) to count normal
## subgroups of B3 = <a,b | aba=bab> up to a given index bound.
##
## This file expects a global variable PROBE_N (positive integer, the
## index bound for this stage) to already be bound before this file is
## read. A driver stub (written per-stage by the calling shell) sets
## PROBE_N and then does: Read("search/probe-wall-stage0.g");
##
## Output: writes one JSON record to the file named by PROBE_OUTFILE
## (also expected to be pre-bound; defaults to
## "search/certs/wall_probe_20260728_stageXX.json" if absent).
##
## No interpretation is performed here: this script only counts and
## records raw facts (index, count, PB3-membership by kernel containment,
## abelian invariants of the finite quotient B3/N). It does not decide
## whether any N is "genuine" or relevant to GT-shadow.
#############################################################################

if not IsBound(PROBE_N) then
    Error("PROBE_N must be bound before reading this script.");
fi;

if LoadPackage("lins") <> true then
    Error("Failed to load GAP package LINS.");
fi;

if not IsBound(PROBE_OUTFILE) then
    PROBE_OUTFILE := Concatenation("search/certs/wall_probe_20260728_stage_",
                                    String(PROBE_N), ".json");
fi;

# --- Build B3 = <a,b | aba=bab> as an fp-group ------------------------------
F := FreeGroup("a", "b");
a := F.1;;
b := F.2;;
rel := a * b * a * (b * a * b)^-1;
B3 := F / [rel];
ga := B3.1;;
gb := B3.2;;

# --- Standard surjection B3 -> S3, kernel = PB3 -----------------------------
# a -> (1,2), b -> (2,3); check braid relation holds in S3 (sanity, not a claim):
# (1,2)(2,3)(1,2) = (1,3) = (2,3)(1,2)(2,3), so the images satisfy aba=bab.
S3 := SymmetricGroup(3);
phi := GroupHomomorphismByImages(B3, S3, [ga, gb], [(1,2), (2,3)]);
if phi = fail then
    Error("Failed to build B3 -> S3 homomorphism (sanity check failed).");
fi;
PB3 := Kernel(phi);

# --- Run LINS search, timing with Runtime() (ms of CPU time) ---------------
t0 := Runtime();
gr := LowIndexNormalSubgroupsSearch(B3, PROBE_N);
nodes := ComputedNormalSubgroups(gr);
t1 := Runtime();
elapsed_ms := t1 - t0;

# --- Per-node raw data (no interpretation) ----------------------------------
records := [];
for nd in nodes do
    N := Grp(nd);
    idx := Index(nd);
    inPB3 := IsSubset(PB3, N);
    # Edge case: N = B3 itself (index 1) triggers a FactorGroup/InverseMutable
    # failure in this GAP/LINS combination for the fp-group quotient by the
    # whole group; the quotient is trivially the trivial group, so short-circuit.
    if idx = 1 then
        abinv := [];
        qstruct := "1";
    else
        Q := FactorGroup(B3, N);
        abinv := AbelianInvariants(Q);
        qstruct := StructureDescription(Q);
    fi;
    Add(records, rec(
        index := idx,
        in_PB3 := inPB3,
        quotient_abelian_invariants := abinv,
        quotient_structure_description := qstruct
    ));
od;

# --- Write JSON (hand-rolled, no external json package assumed) ------------
PrintJsonRecord := function(strm, r)
    local first, ai;
    PrintTo(strm, "    {\n");
    PrintTo(strm, "      \"index\": ", r.index, ",\n");
    if r.in_PB3 then
        PrintTo(strm, "      \"in_PB3\": true,\n");
    else
        PrintTo(strm, "      \"in_PB3\": false,\n");
    fi;
    PrintTo(strm, "      \"quotient_abelian_invariants\": [");
    first := true;
    for ai in r.quotient_abelian_invariants do
        if not first then
            PrintTo(strm, ", ");
        fi;
        PrintTo(strm, ai);
        first := false;
    od;
    PrintTo(strm, "],\n");
    PrintTo(strm, "      \"quotient_structure_description\": \"",
            r.quotient_structure_description, "\"\n");
    PrintTo(strm, "    }");
end;

outstrm := OutputTextFile(PROBE_OUTFILE, false);
SetPrintFormattingStatus(outstrm, false);
PrintTo(outstrm, "{\n");
PrintTo(outstrm, "  \"stage_index_bound\": ", PROBE_N, ",\n");
PrintTo(outstrm, "  \"lins_elapsed_ms_Runtime\": ", elapsed_ms, ",\n");
PrintTo(outstrm, "  \"normal_subgroup_count\": ", Length(records), ",\n");
PrintTo(outstrm, "  \"pb3_count\": ",
        Length(Filtered(records, r -> r.in_PB3)), ",\n");
PrintTo(outstrm, "  \"records\": [\n");
for i in [1 .. Length(records)] do
    PrintJsonRecord(outstrm, records[i]);
    if i < Length(records) then
        PrintTo(outstrm, ",\n");
    else
        PrintTo(outstrm, "\n");
    fi;
od;
PrintTo(outstrm, "  ]\n");
PrintTo(outstrm, "}\n");
CloseStream(outstrm);

Print("STAGE_DONE n=", PROBE_N, " count=", Length(records),
      " pb3_count=", Length(Filtered(records, r -> r.in_PB3)),
      " elapsed_ms=", elapsed_ms, "\n");
