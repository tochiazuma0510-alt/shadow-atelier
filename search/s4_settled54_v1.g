# search/s4_settled54_v1.g -- S4-SETTLED-54 (裁定889, 仕様更新 裁定891/892: 4点同時再監査 cert).
#
# Fresh, independent RE-EXECUTION (not a re-read of the old cert) of GT(N_S4), producing a single
# re-audit cert with 4 items, each tagged by evidence type (direct computation vs citation),
# per 裁定892:
#   (a) enumeration completeness of GT(N_S4)'s candidate set (direct + citation)
#   (b) kernel equality ker(T_{m,f})=N_S4 for all 54 shadows -- PRIMARY route = DIRECT finite-group
#       computation (裁定892: construct psi = induced self-map of Gg=PB3/N via
#       GroupHomomorphismByImages, check well-defined + Kernel(psi) trivial). The K5-8
#       automorphism-witness search is kept ONLY as a SECONDARY cross-reference, explicitly NOT
#       load-bearing (does not feed into the isolated computation), to avoid candidate-on-candidate
#       (OP-SETTLED is Sol-unaudited, per 裁定892 point 1).
#   (c) spec-staleness check -- citation only (裁定892 point 3: no new judgment needed)
#   (2) c in N_S4 -- direct machine value (PU-F7's S^2=() boolean, already computed and
#       fixture-gating upstream, now also surfaced as its own field instead of the previously
#       hardcoded "c_in_N":true JSON string)
#
# 847 dependency audit (read in full before reuse, this session):
#   search/week3-psl-S4.g            -- driver this script mirrors (39 lines)
#   search/week3-psl-common.g        -- GF(8) arithmetic (CheckGF8 self-check), PGammaL(2,8) element
#                                        enumeration, RunPSLWindow incl. settled witness search
#                                        (lines 371-390: [m,f] settled iff exists h in Aut(Ghat) with
#                                        h^-1*X*h = X^u and h^-1*Y*h = f^-1*Y^u*f, u=2m+1), PU-F7
#                                        (S^2=() check, c_in_N proxy per docs/week3-manifest_v2_psl.md
#                                        line 213: "c in N: barDelta^2=1 in Q (S^2=1 ...)")
#   search/week3-battery-common.g    -- JSON helpers (JStr/JB/JoinC/JArr/WriteFile), and
#                                        EnumerateReducedHexagon (shadow enumeration feeding into
#                                        RunPSLWindow; S4 has c_in_N=true so the quotient-shortcut
#                                        path is used, not the word-level c-not-in-N machinery)
#   docs/week3-manifest_v2_psl.md    -- S,T marking convention: S = image of Delta-bar (Delta =
#                                        sigma_1 sigma_2 sigma_1), T = image of delta_B-bar, so
#                                        S^2 = image of c=Delta^2 directly (line 213, PU-F7)
# Additive, non-breaking edits were made to week3-psl-common.g: "LastRunSettled" / "LastRunEnum" /
# "LastRunKernelEq" / "LastRunCInN" global stashes, each placed immediately after an existing
# Print/assignment statement, exposing already-computed in-memory results to this caller without
# re-parsing JSON. None of these alter any existing function's return value, Print output, or
# written cert bytes for any window (S1-S7).
#
# This script duplicates the S4-specific setup boilerplate (S/T matrices, cfg record) exactly as
# week3-psl-S4.g does -- this duplication is the SAME pattern already used across S1-S7 (each window
# script owns its own small setup, calling the shared RunPSLWindow) and does not touch the reused
# settled-search algorithm itself.

SizeScreen([4096, 0]);;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

CheckGF8();;

Smat := MakeMatGF8(1,0,1,1);;
Tmat := MakeMatGF8(4,3,1,5);;
Sperm := MatToPermGF8(Smat);;
Tperm := MatToPermGF8(Tmat);;

pglElts8 := BuildPGLElementsGF8();;
frobPerm := FrobPermGF8();;
autGrp8 := Group(Concatenation(List(pglElts8, e -> e.perm), [frobPerm]));;
autElts8Full := Elements(autGrp8);;

autElements := List(autElts8Full, p -> rec(mat:=p, perm:=p));;
autElementToStr := function(p) return String(p); end;;

cfg := rec(
  id := "S4",
  ambientGroupName := "PSL(2,8)", caseLabel := "A_split_inner", objectCount := 1, autOrbitIndex := 1,
  Sperm := Sperm, Tperm := Tperm,
  SmatStr := MatToStrGF8(Smat), TmatStr := MatToStrGF8(Tmat),
  detSJson := "\"not_applicable_q_even\"",
  autElements := autElements, autElementToStr := autElementToStr, autSizeExp := 1512,
  ghatSizeExp := 504, gSizeExp := 504, eOrdExp := 9, kOrdExp := 9, b3PointsExp := 3024,
  charmingSetExp := [0,2,3,5,6,8], exactOrderExp := 18
);;

ok := RunPSLWindow(cfg);;
if not ok then
  Print("[HALT] S4-SETTLED-54: window did not complete (fixture or Aut-size mismatch).\n");
fi;
if ok then

kernelTrivialCount := Length(Filtered(LastRunKernelEq.detail, r -> r.well_defined and r.kernel_trivial));;
kernelWellDefinedCount := Length(Filtered(LastRunKernelEq.detail, r -> r.well_defined));;
isolated := (kernelTrivialCount = LastRunSettled.shadowTotal);;   # PRIMARY: direct kernel-equality route
settledIsolatedCrossCheck := (LastRunSettled.settledCount = LastRunSettled.shadowTotal);;  # SECONDARY (K5-8)
enumComplete := (LastRunEnum.dwordsCount = LastRunEnum.derivedSubgroupOrderIndependent)
                 and LastRunEnum.shadowSumCheck
                 and (LastRunEnum.candidateTotal = LastRunEnum.dwordsCount * LastRunEnum.charmingSetSize);;
Print("\n[S4-SETTLED-54] shadow_total=", LastRunSettled.shadowTotal,
      " kernel_trivial_count(PRIMARY)=", kernelTrivialCount,
      " settled_count(K5-8,SECONDARY)=", LastRunSettled.settledCount,
      " isolated(PRIMARY)=", isolated, " enum_complete=", enumComplete,
      " c_in_N(PU-F7 direct)=", LastRunCInN.sBarSquaredIsIdentity, "\n");

settledJson2 := [];;
for sd in LastRunSettled.settledDetail do
  if sd.settled then
    Add(settledJson2, Concatenation("{\"m\":", String(sd.m), ",\"f_word\":", WordToJson(sd.f_word),
        ",\"settled\":true,\"automorphism_witness\":\"", autElementToStr(sd.witness_mat), "\"}"));
  else
    Add(settledJson2, Concatenation("{\"m\":", String(sd.m), ",\"f_word\":", WordToJson(sd.f_word),
        ",\"settled\":false,\"automorphism_witness\":null}"));
  fi;
od;;

# (a) enumeration-completeness point (裁定891 point a): raw facts + static-source citation of the
# no-descent-filter-contamination finding (裁定529 / docs/notes/auto_settled_check_v1.md 付録A.1),
# which was established for the SAME shared function EnumerateReducedHexagon this window also uses
# (week3-battery-common.g, no window-specific override for S4).
enumJson := Concatenation(
  "{\"g_size\":", String(LastRunEnum.gSize), ",",
  "\"bfs_covers_full_g\":true,",
  "\"derived_subgroup_order_via_dwords_count\":", String(LastRunEnum.dwordsCount), ",",
  "\"derived_subgroup_order_independent_gap_call\":", String(LastRunEnum.derivedSubgroupOrderIndependent), ",",
  "\"derived_subgroup_order_agrees\":", JB(LastRunEnum.dwordsCount = LastRunEnum.derivedSubgroupOrderIndependent), ",",
  "\"charming_set_size\":", String(LastRunEnum.charmingSetSize), ",\"n_ord\":", String(LastRunEnum.nOrd), ",",
  "\"candidate_total\":", String(LastRunEnum.candidateTotal), ",",
  "\"candidate_total_eq_dwords_times_charming\":", JB(LastRunEnum.candidateTotal = LastRunEnum.dwordsCount * LastRunEnum.charmingSetSize), ",",
  "\"shadow_total\":", String(LastRunEnum.shadowTotal), ",",
  "\"shadow_sum_check\":", JB(LastRunEnum.shadowSumCheck), ",",
  "\"no_descent_filter_in_enumeration\":{\"claim\":\"EnumerateReducedHexagon's per-candidate loop calls only theta/tau GroupHomomorphismByImages (well-definedness, W1) and Size(Group(genA,genB))=Size(G) (SURJ); it never calls an Aut-extension / K5-8 witness check while building the candidate/shadow set\",",
    "\"source\":\"search/week3-battery-common.g lines 315-372 (read in full this session, 847 audit)\",",
    "\"corroborating_ruling\":\"裁定529, docs/notes/auto_settled_check_v1.md 付録A.1 (AS-GAP-3 closed for this SAME shared function)\"}",
  "}");;

# (b) kernel-equality point (裁定892 point 1: DIRECT route is primary). For each shadow [m,f],
# psi := induced self-map of Gg=PB3/N_S4 (X->X^u, Y->f^-1 Y^u f) via GroupHomomorphismByImages.
# well_defined=(psi<>fail); kernel_trivial=(Size(Kernel(psi))=1). This directly computes
# ker(T_{m,f}) cap PB3 = N_S4 cap PB3 at the PB3/N level (elementary argument, not attributed to any
# candidate document: N_S4 <= PB3 for this "quotient_ok"/c_in_N window per PU-F7 below, and the
# B3/PB3=S3 quotient component of T_{m,f} is untouched by m,f -- Delta-bar,delta_B-bar are FIXED
# markings independent of the shadow per PU-F8 -- so kernel equality at the full B3 level reduces to
# triviality of Kernel(psi) here, GIVEN c_in_N holds, which is checked directly in (2) below).
kernelEqDetailJson := [];;
for sd in LastRunKernelEq.detail do
  Add(kernelEqDetailJson, Concatenation("{\"m\":", String(sd.m), ",\"f_word\":", WordToJson(sd.f_word),
      ",\"well_defined\":", JB(sd.well_defined),
      ",\"kernel_trivial\":", JB(sd.well_defined and sd.kernel_trivial),
      ",\"kernel_size\":", (function() if sd.well_defined then return String(sd.kernel_size); else return "null"; fi; end)(), "}"));
od;;

kernelEqJson := Concatenation(
  "{\"method\":\"direct: GroupHomomorphismByImages(Gg,Gg,[X,Y],[X^u,f^-1*Y^u*f]) then Kernel(psi) size, evaluated at PB3/N_S4 (order ", String(LastRunEnum.gSize), ")\",",
  "\"well_defined_count\":", String(kernelWellDefinedCount), ",",
  "\"kernel_trivial_count\":", String(kernelTrivialCount), ",",
  "\"shadow_total\":", String(LastRunSettled.shadowTotal), ",",
  "\"detail\":", JArr(kernelEqDetailJson), ",",
  "\"secondary_cross_reference\":{\"method\":\"K5-8 automorphism-witness search (exists h in Aut(Ghat) with h^-1 X h=X^u, h^-1 Y h=f^-1 Y^u f), NOT load-bearing for isolated below\",",
    "\"settled_count\":", String(LastRunSettled.settledCount), ",",
    "\"agrees_with_direct_kernel_trivial_count\":", JB(LastRunSettled.settledCount = kernelTrivialCount), ",",
    "\"note\":\"kept only as a second-system corroboration (裁定892 point 1); if these two counts agree it is corroborating evidence for OP-SETTLED (docs/notes/auto_settled_check_v1.md), not the other way around\"}",
  "}");;

# (2) c in N_S4 -- direct machine value, not a hardcode. S = image of Delta-bar (docs/week3-manifest_v2_psl.md
# S,T marking convention line 149/213), so S^2 = image of c=Delta^2; this is the SAME boolean already
# gating fixtureOK/PU-F7 upstream (week3-psl-common.g), now surfaced explicitly instead of leaving the
# JSON output's separate "c_in_N":true field as an unlinked hardcoded string.
cInNJson := Concatenation(
  "{\"method\":\"direct: S^2 = () in Ghat, where S = image of Delta-bar (Delta=sigma_1 sigma_2 sigma_1), so S^2 = image of c=Delta^2 -- PU-F7\",",
  "\"s_squared_is_identity\":", JB(LastRunCInN.sBarSquaredIsIdentity), ",",
  "\"paper_cross_reference\":{\"argument\":\"c is central in B3, hence central in PB3; its image lies in Z(PSL(2,8)); Z(PSL(2,8))=1 (PSL simple, trivial center) => image = 1 => c in N_S4\",",
    "\"status\":\"cited for mathematician review per 裁定892 point 2, not asserted as a proof by this implementer\",\"load_bearing\":false}",
  "}");;

# (c) spec-staleness (裁定892 point 3: citation only, no new judgment)
cCheckJson := "{\"claim\":\"no descent-filter contamination in shadow enumeration\",\"citation\":\"裁定529, docs/notes/auto_settled_check_v1.md 付録A.1 (AS-GAP-3 closed for the SAME shared function EnumerateReducedHexagon this S4 window also uses)\",\"new_judgment_required\":false}";;

outJson := Concatenation(
  "{\"schema\":\"s4-settled54/v2\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/s4_settled54_v1.g\",\"task\":\"S4-SETTLED-54 (裁定889, 仕様更新 裁定891/892)\"},",
  "\"reused_from\":{\"driver\":\"search/week3-psl-S4.g\",\"library\":\"search/week3-psl-common.g:RunPSLWindow\",",
    "\"note\":\"fresh independent re-execution; not a re-read of certificates/S4.v2.json\"},",
  "\"ambient_group\":\"PSL(2,8)\",\"aut_group\":\"PGammaL(2,8)\",\"aut_size\":", String(Length(autElements)), ",",
  "\"a_enumeration_completeness\":", enumJson, ",",
  "\"b_kernel_equality\":", kernelEqJson, ",",
  "\"c_spec_staleness_check\":", cCheckJson, ",",
  "\"point2_c_in_N\":", cInNJson, ",",
  "\"isolated\":", JB(isolated), ",",
  "\"isolated_method\":\"PRIMARY: (kernel_trivial_count == shadow_total) via direct kernel-equality (b); the final Def-3.13 (settled-per-shadow => isolated) one-line step is mathematician review per 裁定889/891\",",
  "\"settled_isolated_k5_8_cross_check\":", JB(settledIsolatedCrossCheck), ",",
  "\"prior_claim\":{\"source\":\"certificates/S4.v2.json (existing hardcoded isolated:UNKNOWN) + docs/notes/surj_s4_v2.md human-derived claim\",",
    "\"claimed_settled_count\":54,\"claimed_shadow_total\":54}",
  "}");;

WriteFile("search/certs/s4_settled54_v2_20260812.json", outJson);;
Print("wrote search/certs/s4_settled54_v2_20260812.json\n");
fi;
QUIT;
