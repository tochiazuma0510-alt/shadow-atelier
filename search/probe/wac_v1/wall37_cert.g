#############################################################################
## search/probe/wac_v1/wall37_cert.g
##  n=37 の非可解窓(ell=31, t=6, C31 x S6, |C(w0)|=22320)の正式 cert 化 probe。
##  wall28_cert.g(P-WALL-28, n=28)と同型(逐語複製・n/witness/出力名のみ差替)。
##  witness (a1, b1) は search/certs/scans/tmax_scan_29-31_ell29-31_20260731.json
##  の records[ell=31].t_records[t=6](n=37, stage="HIT")から逐語。検算ロジックは
##  wall28_cert.g をそのまま踏襲する(hexagon 判定は search/kerchi-judge.g の
##  RtOf ではなく sat_l1_probe11.g の検算済み手書き式を採用 -- 同じ判定
##  規約の逸脱理由も同文で記録する)。
##  raw measurements only -- 予言値・期待値はコードに書かない(接触遮断)。
##  cert 生成後、python json.load で構文検証し、失敗したら Error で止める
##  (前回の事故対策 -- GAP の出力整形は SetPrintFormattingStatus で無効化済み
##  だが、二重確認として独立パーサで読めることを機械的に確認する)。
##
##  ローカル smoke 用の truncate knob(CI では常に全数): 実行前に GAP 変数
##  WALL_SMOKE_LIMIT を preamble で正の整数に束縛すると、SURV 全数検算の
##  ループを Elements(Cv) の先頭 WALL_SMOKE_LIMIT 元に切り詰める(ローカルの
##  RAM/時間節約のみが目的)。既定(未束縛または 0)は全数 -- CI は preamble
##  を注入しないのでこの既定のまま走る。truncate した場合は出力 cert 名に
##  "_smoke" を付け、正規名の cert を上書きしないようにする(全数実行の
##  cert とローカル smoke 生成物を機構で混同できなくする)。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
SizeScreen([4096, 0]);;

JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");

NC := function(p, nn)
  return nn - NrMovedPoints(p) + Length(Cycles(p, MovedPoints(p)));
end;;

Sha256OfString := function(s)
  local tmp, out, f, line;
  tmp := "search/.tmp_wall37_cert_sha.txt";
  out := "search/.tmp_wall37_cert_sha.out";
  f := OutputTextFile(tmp, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, s);
  CloseStream(f);
  Exec(Concatenation("sha256sum \"", tmp, "\" > \"", out, "\""));
  f := InputTextFile(out);
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\" \"", out, "\""));
  if line = fail or Length(line) < 64 then
    Error("wall37_cert.g: Sha256OfString: sha256sum did not return a hash line");
  fi;
  return line{[1 .. 64]};
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_wall37_cert_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1 .. 64]};
end;;

## ---- fail-closed JSON syntax check (前回の事故対策) ----
## GAP に汎用 JSON parser は同梱していないので、python の json.load を
## 外部プロセスとして呼び、構文的に読めることだけを確認する(意味検証では
## ない -- 意味の照合は独立の照合器が別途行う)。失敗したら Error で止め、
## 壊れた cert を残さない。
ValidateJsonFile := function(path)
  local cmd, tmp, f, line, ok;
  tmp := Concatenation(path, ".jsoncheck.txt");
  cmd := Concatenation("python -c \"import json; json.load(open('", path,
           "', encoding='utf-8')); print('JSON_VALID')\" > \"", tmp, "\" 2>&1");
  Exec(cmd);
  f := InputTextFile(tmp);
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  ok := (line <> fail and PositionSublist(line, "JSON_VALID") <> fail);
  if not ok then
    Error("wall37_cert.g: ValidateJsonFile: python json.load failed to parse ", path,
          " -- got: ", line);
  fi;
  return true;
end;;

#############################################################################
## ---- witness (n=37, ell=31, t=6; search/certs/scans/tmax_scan_29-31_
##      ell29-31_20260731.json の該当 HIT レコードから逐語) ----
#############################################################################
n := 37;;
a1 := (1,30)(2,11)(3,7)(4,5)(8,10)(9,35)(12,29)(13,15)(14,32)(16,28)(17,19)(18,36)(20,27)(21,23)(22,33)(24,26)(25,37)(31,34);;
b1 := (1,29,11)(2,10,7)(3,6,5)(8,9,35)(12,28,15)(13,14,32)(16,27,19)(17,18,36)(20,26,23)(21,22,33)(24,25,37)(30,31,34);;
Snn := SymmetricGroup(n);;  Ann := AlternatingGroup(n);;

Print("=== P-WALL-37 窓 assert (n=", n, ") ===\n");
Print("a1 = ", a1, "\nb1 = ", b1, "\n");

a1sq := (a1^2 = ());;
b1cube := (b1^3 = ());;
kk := NrMovedPoints(a1) / 2;;
jj := NrMovedPoints(b1) / 3;;
signA1 := SignPerm(a1);;
a1type := CycleStructurePerm(a1);;
b1type := CycleStructurePerm(b1);;
w := b1^-1 * a1;;
v := a1 * b1^-1;;
wtype := CycleStructurePerm(w);;
word := Order(w);;
xbtype0 := CycleStructurePerm(w^2);;
xbord0 := Order(w^2);;
genAn := (Group(a1, b1) = Ann);;

reeC := NC(a1, n) + NC(b1, n) + NC(w, n);;
reeGenus := ((3*n - reeC) - 2*n + 2) / 2;;

aE := a1 * (n+1, n+3);;
bE := b1 * (n+1, n+3, n+2);;
s1 := bE^-1 * aE;;
s2 := aE * bE^2;;
braidHolds := (s1*s2*s1 = s2*s1*s2);;

W := MakeWindow(s1, s2);;
cIsOne := (W.c = Identity(W.Bq));;
pEqAn := (W.PN = Ann);;
Esize := Size(Group(aE, bE));;
EEqSixAn := (Esize = 6 * Size(Ann));;
Nord := W.Nord;;
charmingSet := Filtered([0 .. Nord-1], z -> Gcd(2*z+1, Nord) = 1);;
cm := Length(charmingSet);;

Print("  a1^2=1 ", a1sq, "  b1^3=1 ", b1cube, "  k=", kk, "  j=", jj,
      "  sign(a1)=", signA1, "\n");
Print("  a1 型 ", a1type, "  b1 型 ", b1type, "\n");
Print("  w 型 ", wtype, " ord ", word, "    xbar=w^2 型 ", xbtype0, " ord ", xbord0, "\n");
Print("  <a1,b1> = A_", n, " ? ", genAn, "\n");
Print("  Ree: c(a1)+c(b1)+c(w) = ", reeC, "   n+2 = ", n+2, "   genus = ", reeGenus, "\n");
Print("  braid ", braidHolds, "   c=1 ", cIsOne, "   P=A_", n, " ? ", pEqAn,
      "   |E|=6|A_", n, "| ? ", EEqSixAn, "\n");
Print("  N_ord = ", Nord, "   c_m = ", cm, "\n");

#############################################################################
## ---- (ii) C_Sn(w0) の位数・構造・可解性 ----
#############################################################################
Cw := Centralizer(Snn, w);;
CwSize := Size(Cw);;
CwStruct := StructureDescription(Cw);;
CwSolvable := IsSolvable(Cw);;
if CwSolvable then CwDerivedLength := DerivedLength(Cw); else CwDerivedLength := -1; fi;
StabXbar := Centralizer(Snn, W.x);;
StabXbarSize := Size(StabXbar);;
StabXbarSolvable := IsSolvable(StabXbar);;
Print("\n=== C_S", n, "(w0) ===\n");
Print("  |C_S", n, "(w0)| = ", CwSize, "   構造 ", CwStruct, "   可解? ", CwSolvable,
      "   導来長 ", CwDerivedLength, "\n");
Print("  |Stab(xbar)| = ", StabXbarSize, "   可解? ", StabXbarSolvable, "\n");

#############################################################################
## ---- (iii) SURV 構成 f_z=(a1^z)a1 の全数検算(wall28_cert.g と同じ judge 規約:
## RtOf は不採用 -- sat_l1_probe11/13 の検算済み手書き式を使う) ----
## smoke knob: WALL_SMOKE_LIMIT が正の整数に束縛されていれば、Elements(Cv)
## の先頭 WALL_SMOKE_LIMIT 元だけを検算する(ローカル専用・CI は既定 = 全数)。
#############################################################################
Cv := Centralizer(Snn, v);;
CvSize := Size(Cv);;
CvElts := Elements(Cv);;
isSmoke := false;;
if IsBound(WALL_SMOKE_LIMIT) and IsInt(WALL_SMOKE_LIMIT) and WALL_SMOKE_LIMIT > 0
   and WALL_SMOKE_LIMIT < Length(CvElts) then
  CvElts := CvElts{[1 .. WALL_SMOKE_LIMIT]};;
  isSmoke := true;;
fi;
if isSmoke then
  Print("\n=== SURV 全数検算 (|C_S", n, "(v)| = ", CvSize,
        "; SMOKE truncated to ", Length(CvElts), " elements) ===\n");
else
  Print("\n=== SURV 全数検算 (|C_S", n, "(v)| = ", CvSize, ") ===\n");
fi;
passCount := 0;;  hexFail := 0;;  genFail := 0;;  alphas := [];;
for z in CvElts do
  f := (a1^z) * a1;
  if not (s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f) then
    hexFail := hexFail + 1;
  elif Group(W.x, W.y^f) <> W.PN then
    genFail := genFail + 1;
  else
    passCount := passCount + 1;
    Add(alphas, a1 * z * a1);
  fi;
od;
Print("  通過 = ", passCount, "   hexagon 落ち = ", hexFail, "   全射 落ち = ", genFail,
      "   合計 = ", passCount + hexFail + genFail, "\n");

XiIm := Group(alphas);;
XiImSize := Size(XiIm);;
XiImStruct := StructureDescription(XiIm);;
XiImSolvable := IsSolvable(XiIm);;
if XiImSolvable then XiImDerivedLength := DerivedLength(XiIm); else XiImDerivedLength := -1; fi;
XiEqCw := (XiIm = Cw);;
Print("  Xi 像位数 = ", XiImSize, "   構造 ", XiImStruct, "   可解? ", XiImSolvable,
      "   導来長 ", XiImDerivedLength, "   = C_S", n, "(w0) ? ", XiEqCw, "\n");

#############################################################################
## ---- (iv) LID-1 canonical string + SHA-256 ----
#############################################################################
lid1Str := Concatenation("LID1/v1|id=P-WALL-37|n=", String(n),
             "|a1=", String(a1), "|b1=", String(b1),
             "|S1=", String(s1), "|S2=", String(s2));;
lid1Sha := Sha256OfString(lid1Str);;
Print("\n  LID-1 = ", lid1Str, "\n  LID-1 sha256 = ", lid1Sha, "\n");

selfSha := ComputeSha256File("search/probe/wac_v1/wall37_cert.g");;

#############################################################################
## ---- JSON 出力 ----
#############################################################################
if isSmoke then
  outName := "search/certs/wall37_cert_20260731_smoke.json";;
else
  outName := "search/certs/wall37_cert_20260731.json";;
fi;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"wac_v1-wall28-cert/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/wall37_cert.g\",\n",
  "  \"window_label\":\"P-WALL-37\",\n",
  "  \"f_orientation\":\"probe11_handwritten_hexagon\",\n",
  "  \"source_witness\":\"search/certs/scans/tmax_scan_29-31_ell29-31_20260731.json (ell=31, t=6, n=37, stage=HIT レコード), 逐語\",\n",
  "  \"note\":\"raw measurements only -- 予言値/期待値はコードに書かず、全て計算値をそのまま記録する。W(x,y,c,Bq,PN,N_ord)は search/kerchi-judge.g (JUDGE_LIBRARY_ONLY) の MakeWindow を再利用。hexagon判定は同ファイルの RtOf ではなく search/probe/wac_v1/sat_l1_probe11.g の検算済み手書き式(s1*f^-1*s2*f=f^-1*s1*s2 かつ f^-1*s2*f*s1=s2*s1*f)をそのまま採用 -- wall28_cert.g と同じ judge 規約(RtOf は AbstractProd の反転規約下で実データ上この式と不一致 -- 診断: scratchpad/diag_hex.g)。\",\n",
  "  \"n\":", String(n), ",\n",
  "  \"a1\":", JStr(String(a1)), ",\n",
  "  \"b1\":", JStr(String(b1)), ",\n",
  "  \"window_asserts\":{\n",
  "    \"a1_sq_eq_1\":", JB(a1sq), ",\n",
  "    \"b1_cube_eq_1\":", JB(b1cube), ",\n",
  "    \"k\":", String(kk), ",\n",
  "    \"j\":", String(jj), ",\n",
  "    \"sign_a1\":", String(signA1), ",\n",
  "    \"a1_cycle_type\":", JStr(String(a1type)), ",\n",
  "    \"b1_cycle_type\":", JStr(String(b1type)), ",\n",
  "    \"w0_cycle_type\":", JStr(String(wtype)), ",\n",
  "    \"w0_order\":", String(word), ",\n",
  "    \"xbar_cycle_type\":", JStr(String(xbtype0)), ",\n",
  "    \"xbar_order\":", String(xbord0), ",\n",
  "    \"gen_eq_An\":", JB(genAn), ",\n",
  "    \"ree_sum\":", String(reeC), ",\n",
  "    \"ree_n_plus_2\":", String(n+2), ",\n",
  "    \"ree_genus\":", String(reeGenus), ",\n",
  "    \"braid_holds\":", JB(braidHolds), ",\n",
  "    \"c_eq_identity\":", JB(cIsOne), ",\n",
  "    \"P_eq_An\":", JB(pEqAn), ",\n",
  "    \"E_size\":", String(Esize), ",\n",
  "    \"E_eq_6_An\":", JB(EEqSixAn), ",\n",
  "    \"N_ord\":", String(Nord), ",\n",
  "    \"charming_count\":", String(cm), "\n",
  "  },\n",
  "  \"centralizer_w0\":{\n",
  "    \"size\":", String(CwSize), ",\n",
  "    \"structure_description\":", JStr(CwStruct), ",\n",
  "    \"solvable\":", JB(CwSolvable), ",\n",
  "    \"derived_length\":", String(CwDerivedLength), "\n",
  "  },\n",
  "  \"centralizer_xbar\":{\n",
  "    \"size\":", String(StabXbarSize), ",\n",
  "    \"solvable\":", JB(StabXbarSolvable), "\n",
  "  },\n",
  "  \"surv_scan\":{\n",
  "    \"Cv_size\":", String(CvSize), ",\n",
  "    \"pass_count\":", String(passCount), ",\n",
  "    \"hexagon_fail_count\":", String(hexFail), ",\n",
  "    \"generation_fail_count\":", String(genFail), ",\n",
  "    \"total_checked\":", String(passCount + hexFail + genFail), "\n",
  "  },\n",
  "  \"xi_image\":{\n",
  "    \"size\":", String(XiImSize), ",\n",
  "    \"structure_description\":", JStr(XiImStruct), ",\n",
  "    \"solvable\":", JB(XiImSolvable), ",\n",
  "    \"derived_length\":", String(XiImDerivedLength), ",\n",
  "    \"eq_centralizer_w0\":", JB(XiEqCw), "\n",
  "  },\n",
  "  \"lid1\":{\n",
  "    \"canonical_string\":", JStr(lid1Str), ",\n",
  "    \"sha256\":", JStr(lid1Sha), "\n",
  "  },\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), "\n",
  "  }\n",
  "}\n");;

WriteFile(outName, cert);;
ValidateJsonFile(outName);;
Print("\nWrote ", outName, " (json.load OK)\n");
Print("\nWALL37_CERT_DONE\n");
QUIT;
