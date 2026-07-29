#############################################################################
## search/w62-scan.g -- W6-2 段 A(重い Xi 走査だけを行い shadow 集合を永続化)
##
## 発案会議 006 / W6-2。1 プロセス 1 窓(-o 2g のヒープ枯渇対策 —
## 走査と群論を同一プロセスでやると exit 255 で落ちる実測あり)。
## 窓の選択: 環境変数 W62_ONLY(= 窓 ID)。
## 出力: search/certs/.w62_shadows_<id>.g  (GAP で Read できる shadow 一覧)
#############################################################################
SizeScreen([4096, 0]);;
JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");
Read("search/gaplib_common.g");
Read("search/w62-windows.g");
t0 := GAPLIB_WallElapsedMs();;
JUDGE_FORCE_SCAN_MODE := "xi_restricted";;

wspec := W62_GetWindow();;
Print("=== w62-scan: ", wspec.id, " (A", wspec.n, ") ===\n");
W := W62_MakeW(wspec);;
ch := Filtered([0 .. W.Nord - 1], mm -> Gcd(2*mm+1, W.Nord) = 1);;
Print("N_ord = ", W.Nord, "  |charming| = ", Length(ch),
      "  P_N = A", wspec.n, "? ", Size(W.PN) = Factorial(wspec.n)/2, "\n");

corrRes := CorrectedShadows(W, ch);;
corr := corrRes.shadows;;
Print("scan_mode = ", corrRes.scan_mode, "  shadow_total = ", Length(corr),
      "  scanned = ", corrRes.scanned_count,
      "  settled_fail = ", corrRes.settled_fail_count, "\n");

items := List(corr, s -> Concatenation("[", String(s[1]), ",", String(s[2]), "]"));;
out := Concatenation(
  "W62_ID := ", JStr(wspec.id), ";;\n",
  "W62_NORD := ", String(W.Nord), ";;\n",
  "W62_SCAN_MODE := ", JStr(corrRes.scan_mode), ";;\n",
  "W62_SCANNED := ", String(corrRes.scanned_count), ";;\n",
  "W62_SETTLED_FAIL := ", String(corrRes.settled_fail_count), ";;\n",
  "W62_SHADOWS := [\n", JoinC(items, ",\n"), "\n];;\n");;
path := Concatenation("search/certs/.w62_shadows_", wspec.id, ".g");;
WriteFile(path, out);;
Print("wrote ", path, "\n");
Print("elapsed = ", (GAPLIB_WallElapsedMs()-t0)/1000.0, " s\n");
Print("W62_SCAN_DONE\n");
QUIT;
