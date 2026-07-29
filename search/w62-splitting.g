#############################################################################
## search/w62-splitting.g -- W6-2 段 C(統合・最終証明書)
##
## 発案会議 006 / W6-2: GTSh(N,N) の拡大 1 -> K -> G -> Q -> 1
## (K = ker chi~, Q = Im chi~)は分裂するか。
##
## 3 段構成(-o 2g のヒープ枯渇対策 — 走査と群論を同一プロセスで回すと
## exit 255 で落ちる実測あり。1 窓 1 プロセス):
##   段 A  search/w62-scan.g   (env W62_ONLY=<窓 ID>)  重い Xi 走査 -> shadow 永続化
##   段 B  search/w62-split.g  (env W62_ONLY=<窓 ID>)  分裂判定 -> 部分証明書
##   段 C  本 script                                     3 部分を統合
## 窓仕様は search/w62-windows.g(strike-a{16,18,20}.g から逐語)。
##
## 出力: search/certs/w62_splitting_20260729.json
## 解釈はしない(観測の記録に徹する)。
#############################################################################
SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");
Read("search/w62-windows.g");

ReadWholeFile := function(path)
  local f, s;
  f := InputTextFile(path);
  if f = fail then Error("w62-splitting: 部分証明書が無い: ", path); fi;
  s := ReadAll(f);  CloseStream(f);
  return s;
end;;
GetIntField := function(s, key)
  local mk, p, q, i, ch;
  mk := Concatenation("\"", key, "\":");
  p := PositionSublist(s, mk);
  if p = fail then Error("field not found: ", key); fi;
  q := p + Length(mk);  i := q;
  while i <= Length(s) and s[i] <> ',' and s[i] <> '}' do i := i + 1; od;
  return s{[q .. i-1]};
end;;

parts := [];;  ids := [];;
for w in W62_WINDOWS do
  Add(parts, ReadWholeFile(Concatenation("search/certs/.w62_part_", w.id, ".json")));
  Add(ids, w.id);
od;

Print("############################################################\n");
Print("# W6-2 splitting -- summary\n");
Print("############################################################\n");
allSplit := true;;  noneSplit := true;;
for i in [1 .. Length(parts)] do
  sp := GetIntField(parts[i], "SPLITS");
  Print(ids[i], " : |G|=", GetIntField(parts[i],"G_order"),
        " |K|=", GetIntField(parts[i],"K_order"),
        " |Q|=", GetIntField(parts[i],"Q_order"),
        " Q=", GetIntField(parts[i],"Q_struct"),
        " gcd(|K|,|Q|)=", GetIntField(parts[i],"gcd_K_Q"),
        " 補群クラス数=", GetIntField(parts[i],"complement_class_count"),
        "  **SPLITS=", sp, "**\n");
  if sp = "true" then noneSplit := false; else allSplit := false; fi;
od;
Print("\nall_three_split = ", allSplit, "   none_split = ", noneSplit, "\n");

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha_w62.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1..64]};
end;;

cert := Concatenation(
 "{\"schema\":\"w62-splitting/v1\"",
 ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"scripts\":[\"search/w62-windows.g\",\"search/w62-scan.g\",\"search/w62-split.g\",\"search/w62-splitting.g\"],\"date\":\"2026-07-29\",\"task\":\"ideation-006 W6-2\"}",
 ",\"question\":\"Does the extension 1 -> K -> G -> Q -> 1 split, where G = GTSh(N,N), K = ker(chi-tilde), Q = Im(chi-tilde)?\"",
 ",\"method\":\"windows rebuilt verbatim as in search/strike-a{16,18,20}.g (generating pair (a1,b1), s1 = b^-1 a, s2 = a^-1 b^2 inside A_n x S_3); G and K reconstructed with kerchi-judge.g v1.3 MakeWindow/CorrectedShadows/GroupOfShadows under JUDGE_FORCE_SCAN_MODE = xi_restricted; splitting decided by ComplementClassesRepresentatives on the Pc presentation of G; every complement verified by |H| = |Q|, H cap K = 1, <H,K> = G, and H isomorphic to Q\"",
 ",\"note_shard\":\"three-stage sharding (one GAP process per window per stage): running scan and group theory in a single process exhausts the 2g heap (observed exit 255, no GAP Error)\"",
 ",\"note_schur_zassenhaus\":\"gcd(|K|,|Q|) is 2, 4, 8 respectively, i.e. never 1 -- splitting is NOT forced by Schur-Zassenhaus in any of the three windows\"",
 ",\"results\":[", JoinC(parts, ","), "]",
 ",\"all_three_split\":", JB(allSplit),
 ",\"none_split\":", JB(noneSplit),
 ",\"provenance\":{\"windows_sha256\":", JStr(ComputeSha256File("search/w62-windows.g")),
   ",\"scan_sha256\":", JStr(ComputeSha256File("search/w62-scan.g")),
   ",\"split_sha256\":", JStr(ComputeSha256File("search/w62-split.g")),
   ",\"merge_sha256\":", JStr(ComputeSha256File("search/w62-splitting.g")), "}",
 ",\"interpretation\":\"none -- observation record only (do not interpret)\"",
 "}");;

WriteFile("search/certs/w62_splitting_20260729.json", cert);;
Print("\nwrote search/certs/w62_splitting_20260729.json\n");
Print("W62_SPLITTING_MERGE_DONE\n");
QUIT;
