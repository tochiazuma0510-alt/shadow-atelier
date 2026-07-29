#############################################################################
## search/xi-uid-export.g -- GAP-side canonical UID export for the 15 Xi
## windows (梯子13 + I10-1 2), per 裁定227 (P86-3 item 2 / Sol 便86
## sol_reply_86_math13.md S2 "Xi 完了条件").
##
## Purpose: F86-2.2 (欠落2) found that no artifact ever compared the
## Python re-implementation's actual accepted SET (not just its count) to
## GAP's accepted set. This script exports GAP's own CorrectedShadowsXi
## accepted set, per window, in the exact UID format Sol specified:
##   window_id|m|u2N|full permutation array
## so a downstream comparison script can do a direct set-equality/digest
## check against search/ladder-xi-recheck.py's own UIDs (same format,
## produced independently there -- see that file's candidate_uid()).
##
## This script does NOT implement any independent re-derivation -- it is
## GAP's own reference computation (MakeWindow / CorrectedShadowsXi from
## search/kerchi-judge.g, unchanged), re-run to actually EXPORT the raw
## shadow list instead of only a digest (as the existing a13_ladder_*.json /
## i10_1_*.json certs did). Independence of the comparison comes from the
## OTHER side (search/ladder-xi-recheck.py, which never imports GAP code),
## not from this script.
##
## Input: the 15 windows' own s1/s2/window_id fields, read from the
## already-produced GAP certs (search/certs/a13_ladder_*_20260730.json,
## search/certs/i10_1_*_20260730.json) via gaplib_common.g's
## ReadJsonStringField -- identifying data only (裁定216 point 1 posture),
## not a re-derivation of window construction. N_ord/charming-set/scan are
## recomputed here directly from s1,s2 (not read from the certs), so this
## script does not depend on any digest field the certs may or may not have.
##
## Output: search/certs/xi_uid_gap_<safe_wid>_20260731.json (x15) +
## search/certs/xi_uid_gap_manifest_20260731.json.
##
## Run: .\gap.ps1 search\xi-uid-export.g -o 2g
#############################################################################

Read("search/gaplib_common.g");
JUDGE_LIBRARY_ONLY := true;;
JUDGE_SKIP_LEGACY_CROSSCHECK := true;;
Read("search/kerchi-judge.g");

Sha256OfString := function(str)
  local tmp, f, line;
  tmp := "search/certs/.xi_uid_export_sha_tmp.txt";
  f := OutputTextFile(tmp, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, str);
  CloseStream(f);
  Exec(Concatenation("sha256sum \"", tmp, "\" > \"", tmp, ".out\""));
  f := InputTextFile(Concatenation(tmp, ".out"));
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\" \"", tmp, ".out\""));
  return line{[1..64]};
end;;

CertSha256File := function(path)
  local tmp, f, line;
  tmp := "search/certs/.xi_uid_export_sha_tmp2.txt";
  Exec(Concatenation("sha256sum \"", path, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1..64]};
end;;

# 15 windows: 13 ladder (search/_a13_ladder_driver_spec.md) + 2 I10-1
# (search/_i10_1_driver_spec.md), sourced from their own already-produced
# GAP certs.
WINDOW_CERTS := [
  "search/certs/a13_ladder_W_E_A10_9t1_20260730.json",
  "search/certs/a13_ladder_W_E_A10_9t1_o2_20260730.json",
  "search/certs/a13_ladder_W_E_A10_9t1_o3_20260730.json",
  "search/certs/a13_ladder_W_E_A10_9t1_o4_20260730.json",
  "search/certs/a13_ladder_W_E_A10_9t1_o5_20260730.json",
  "search/certs/a13_ladder_W_E_A10_9t1_o6_20260730.json",
  "search/certs/a13_ladder_W_E_A11_9t2_20260730.json",
  "search/certs/a13_ladder_W_E_A11_9t2_o2_20260730.json",
  "search/certs/a13_ladder_W_E_A11_9t2_o3_20260730.json",
  "search/certs/a13_ladder_W_E_A12_9t3_20260730.json",
  "search/certs/a13_ladder_W_E_A12_9t3_o2_20260730.json",
  "search/certs/a13_ladder_W_E_A12_9t3_o3_20260730.json",
  "search/certs/a13_ladder_W_E_A13_9t4_20260730.json",
  "search/certs/i10_1_W_E_A10_5x2t0_20260730.json",
  "search/certs/i10_1_W_E_A15_5x3t0_20260730.json",
];;

# full permutation array, 1-indexed positions [1..deg], matching
# search/ladder-xi-recheck.py's perm_canonical_str() exactly (that function
# prints, for a size-deg sympy Permutation, "deg<deg>:[img(1),img(2),...,
# img(deg)]" with 1-indexed points and images).
PermArrayStr := function(f, deg)
  local i, parts;
  parts := [];
  for i in [1 .. deg] do
    Add(parts, String(i^f));
  od;
  return Concatenation("deg", String(deg), ":[", JoinC(parts, ","), "]");
end;;

CandidateUid := function(wid, m, u, f, deg)
  return Concatenation(wid, "|m=", String(m), "|u2N=", String(u), "|f=",
    PermArrayStr(f, deg));
end;;

manifestEntries := [];;

for certPath in WINDOW_CERTS do
  Print("\n################################################################\n");
  Print("# ", certPath, "\n");
  Print("################################################################\n");

  s1str := ReadJsonStringField(certPath, "s1");;
  s2str := ReadJsonStringField(certPath, "s2");;
  wid := ReadJsonStringField(certPath, "window_id");;

  s1 := EvalString(s1str);;
  s2 := EvalString(s2str);;
  if not (IsPerm(s1) and IsPerm(s2)) then
    Error("xi-uid-export: EvalString did not yield permutations for ", certPath);
  fi;

  deg := Maximum(LargestMovedPoint(s1), LargestMovedPoint(s2));;
  W := MakeWindow(s1, s2);;
  Nord := W.Nord;;
  charmingSet := Filtered([0 .. Nord - 1], m -> Gcd(2*m+1, Nord) = 1);;

  JUDGE_FORCE_SCAN_MODE := "xi_restricted";;
  xiRes := CorrectedShadowsXi(W, charmingSet);;
  shadows := xiRes.shadows;;

  uids := [];;
  for sh in shadows do
    m := sh[1];;  f := sh[2];;  u := 2*m + 1;;
    Add(uids, CandidateUid(wid, m, u, f, deg));
  od;
  uidsSorted := SortedList(uids);;   # canonicalize before hashing (mirrors
                                      # ladder-xi-recheck.py's digest_set())
  digestStr := "";;
  if Length(uidsSorted) > 0 then
    digestStr := Concatenation(JoinC(uidsSorted, "\n"), "\n");;
  fi;
  digest := Sha256OfString(digestStr);;

  Print("  wid=", wid, " deg=", deg, " N_ord=", Nord,
        " charming=", Length(charmingSet), " scanned=", xiRes.scanned_count,
        " accepted=", Length(shadows), " settled_fail=", xiRes.settled_fail_count,
        " digest=", digest, "\n");

  safeId := ReplacedString(wid, "-", "_");;
  outPath := Concatenation("search/certs/xi_uid_gap_", safeId, "_20260731.json");;

  outParts := [];;
  Add(outParts, "{\n");
  Add(outParts, "  \"schema\": \"xi-uid-gap-export/v1\",\n");
  Add(outParts, "  \"generated_by\": \"search/xi-uid-export.g\",\n");
  Add(outParts, Concatenation("  \"note\": ", JStr(Concatenation(
    "GAP-side canonical UID export for direct set-equality/digest comparison ",
    "against search/ladder-xi-recheck.py (\xe8\xa3\x81\xe5\xae\x9a227 P86-3 item 2). ",
    "Not an independent re-implementation -- this is GAP's own ",
    "CorrectedShadowsXi (search/kerchi-judge.g), re-run to export the raw ",
    "accepted set instead of only a digest. Independence of the comparison ",
    "comes from the python side.")), ",\n"));
  Add(outParts, Concatenation("  \"source_cert\": ", JStr(certPath), ",\n"));
  Add(outParts, Concatenation("  \"window_id\": ", JStr(wid), ",\n"));
  Add(outParts, Concatenation("  \"deg\": ", String(deg), ",\n"));
  Add(outParts, Concatenation("  \"N_ord\": ", String(Nord), ",\n"));
  Add(outParts, Concatenation("  \"charming_count\": ", String(Length(charmingSet)), ",\n"));
  Add(outParts, Concatenation("  \"scanned_count\": ", String(xiRes.scanned_count), ",\n"));
  Add(outParts, Concatenation("  \"accepted_count\": ", String(Length(shadows)), ",\n"));
  Add(outParts, Concatenation("  \"settled_fail_count\": ", String(xiRes.settled_fail_count), ",\n"));
  Add(outParts, Concatenation("  \"accepted_set_digest_sha256\": ", JStr(digest), ",\n"));
  Add(outParts, "  \"accepted_uids\": [\n");
  for i in [1 .. Length(uidsSorted)] do
    Add(outParts, Concatenation("    ", JStr(uidsSorted[i])));
    if i < Length(uidsSorted) then Add(outParts, ",\n"); else Add(outParts, "\n"); fi;
  od;
  Add(outParts, "  ]\n");
  Add(outParts, "}\n");
  WriteFile(outPath, Concatenation(outParts));;
  Print("  WROTE ", outPath, "\n");

  Add(manifestEntries, rec(wid := wid, outfile := outPath, deg := deg, Nord := Nord,
      scanned_count := xiRes.scanned_count, accepted_count := Length(shadows),
      settled_fail_count := xiRes.settled_fail_count,
      accepted_set_digest_sha256 := digest));
od;

manifestParts := [];;
Add(manifestParts, "{\n");
Add(manifestParts, "  \"schema\": \"xi-uid-gap-manifest/v1\",\n");
Add(manifestParts, "  \"generated_by\": \"search/xi-uid-export.g\",\n");
Add(manifestParts, "  \"note\": \"15-window (梯子13+I10-1 2) GAP-side canonical UID export manifest, P86-3 item 2.\",\n");
Add(manifestParts, Concatenation("  \"windows_processed\": ", String(Length(manifestEntries)), ",\n"));
Add(manifestParts, "  \"windows\": [\n");
for i in [1 .. Length(manifestEntries)] do
  e := manifestEntries[i];;
  Add(manifestParts, Concatenation(
    "    {\"wid\":", JStr(e.wid), ",\"outfile\":", JStr(e.outfile),
    ",\"deg\":", String(e.deg), ",\"N_ord\":", String(e.Nord),
    ",\"scanned_count\":", String(e.scanned_count),
    ",\"accepted_count\":", String(e.accepted_count),
    ",\"settled_fail_count\":", String(e.settled_fail_count),
    ",\"accepted_set_digest_sha256\":", JStr(e.accepted_set_digest_sha256),
    ",\"cert_sha256\":", JStr(CertSha256File(e.outfile)), "}"));
  if i < Length(manifestEntries) then Add(manifestParts, ",\n"); else Add(manifestParts, "\n"); fi;
od;
Add(manifestParts, "  ]\n");
Add(manifestParts, "}\n");
WriteFile("search/certs/xi_uid_gap_manifest_20260731.json", Concatenation(manifestParts));;
Print("\nWrote search/certs/xi_uid_gap_manifest_20260731.json\n");
Print("XI_UID_EXPORT_DONE\n");
