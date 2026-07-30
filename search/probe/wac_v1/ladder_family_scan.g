#############################################################################
## search/probe/wac_v1/ladder_family_scan.g
##  ジョブ3: N_ord = 9 以外の梯子族(N_ord in {11,13,15,17,19,21,25})で
##  (ell, 1^t) 窓を t の全域(preamble で bound)で撃ち、核の律(|ker| と構造)
##  の表を作る。既存の search/strike-a13-ladder.g は無改変(新規に書く)。
##  N_ord は既存の a13 梯子(N_ord=9 系: w0 = 9-cycle, t=1..4)と同じ規約で
##  w0 の cycle length そのもの(ell := N_ord)。
##
##  各 (ell, t) で:
##   予算チェック(dl3_search.g 由来の parity+Ree budget)
##   -> 2-opt で実現対 (a1,b1) を探す(dl3_search.g の Hunt をそのまま流用)
##   -> HIT なら C_Sn(w0) の位数/構造/導来長・(|C|<=5000 なら) SURV 全数通過数
##      (超える場合は "skipped(size)" と明記してスキップ)
##
##  preamble 変数(未指定なら既定値):
##    LADDER_ELLS       -- 走査する ell(=N_ord)のリスト(既定 [11,13,15,17,19,21,25])
##    LADDER_T_MIN, LADDER_T_MAX -- t の走査範囲(既定 0..12。fail-closed cap --
##                                  全域を謳うが計算資源上の上限として明記する)
##    LADDER_SHARD      -- shard ラベル(出力ファイル名・cert 記録用、任意)
##    LADDER_MAXRESTART, LADDER_MAXSTEP, LADDER_TIME_CAP_PER_K_MS,
##    LADDER_TOTAL_TIME_CAP_MS -- Hunt の 2-opt 予算・時間 cap
##
##  raw measurements only -- 予言値/期待値はコードに書かない(接触遮断:
##  ideas/・sol/・docs/notes/sat_l1_v1.md は本スクリプト作成時に未読)。
##  fail-closed: t の上限は preamble の LADDER_T_MAX で明示 cap(黙って打ち切らない)。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
SizeScreen([4096, 0]);;

JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");   ## 定義済み: MakeWindow, JStr, JB, JArr, JoinC, WriteFile

NC := function(p, nn)
  return nn - NrMovedPoints(p) + Length(Cycles(p, MovedPoints(p)));
end;;

Sha256OfString := function(s)
  local tmp, out, f, line;
  tmp := "search/.tmp_ladderfam_cert_sha.txt";
  out := "search/.tmp_ladderfam_cert_sha.out";
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
    Error("ladder_family_scan.g: Sha256OfString: sha256sum did not return a hash line");
  fi;
  return line{[1 .. 64]};
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_ladderfam_cert_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1 .. 64]};
end;;

MakeCyc := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;

Hunt := function(n, w0, k, maxRestart, maxStep, timeCapMs)
  local rs, pts, m, d, step, i, j, m2, d2, mk, Def, t0;
  mk := function(mm) return Product(List(mm, p -> (p[1],p[2])), ()); end;
  Def := function(mm) return NrMovedPoints((mk(mm)*w0^-1)^3); end;
  t0 := Runtime();
  for rs in [1..maxRestart] do
    if Runtime() - t0 > timeCapMs then
      return rec(a1 := fail, timedOut := true, restarts := rs);
    fi;
    pts := Shuffle(ShallowCopy([1..n]));
    m := List([1..k], i -> [pts[2*i-1], pts[2*i]]);
    d := Def(m);
    for step in [1..maxStep] do
      if d = 0 then
        return rec(a1 := mk(m), timedOut := false, restarts := rs, steps := step);
      fi;
      i := Random([1..k]); j := Random([1..k]);
      m2 := List(m, ShallowCopy);
      if i = j then
        continue;
      elif Random([1,2]) = 1 then
        m2[i] := [m[i][1], m[j][1]]; m2[j] := [m[i][2], m[j][2]];
      else
        m2[i] := [m[i][1], m[j][2]]; m2[j] := [m[i][2], m[j][1]];
      fi;
      d2 := Def(m2);
      if d2 <= d then m := m2; d := d2; fi;
    od;
  od;
  return rec(a1 := fail, timedOut := false, restarts := maxRestart);
end;;

#############################################################################
## ---- preamble defaults ----
#############################################################################
if not IsBound(LADDER_ELLS) then LADDER_ELLS := [11, 13, 15, 17, 19, 21, 25]; fi;
if not IsBound(LADDER_T_MIN) then LADDER_T_MIN := 0; fi;
if not IsBound(LADDER_T_MAX) then LADDER_T_MAX := 12; fi;
if not IsBound(LADDER_SHARD) then LADDER_SHARD := ""; fi;
if not IsBound(LADDER_MAXRESTART) then LADDER_MAXRESTART := 60; fi;
if not IsBound(LADDER_MAXSTEP) then LADDER_MAXSTEP := 1500; fi;
if not IsBound(LADDER_TIME_CAP_PER_K_MS) then LADDER_TIME_CAP_PER_K_MS := 8000; fi;
if not IsBound(LADDER_TOTAL_TIME_CAP_MS) then LADDER_TOTAL_TIME_CAP_MS := 10200000; fi;

LADDER_SEED := 20260731;;
Reset(GlobalMersenneTwister, LADDER_SEED);;

#############################################################################
## ---- serialization ----
#############################################################################
CandRecToJson := function(r)
  local base;
  base := Concatenation(
    "{\"ell\":", String(r.ell), ",\"t\":", String(r.t), ",\"n\":", String(r.n),
    ",\"w0_cycle_type\":", JStr(String(r.w0type)),
    ",\"sign_w0\":", String(r.signw0), ",\"NC_w0\":", String(r.ncw0),
    ",\"feasible_k\":", JArr(List(r.feasible_k, String)),
    ",\"result\":", JStr(r.result));
  if r.result <> "HIT" then
    return Concatenation(base, "}");
  fi;
  return Concatenation(base,
    ",\"k\":", String(r.k), ",\"j\":", String(r.j), ",\"gen_label\":", JStr(r.gen),
    ",\"a1\":", JStr(String(r.a1)), ",\"b1\":", JStr(String(r.b1)),
    ",\"N_ord_measured\":", String(r.n_ord_measured),
    ",\"centralizer_w0\":{\"size\":", String(r.cw_size),
      ",\"structure_description\":", JStr(r.cw_struct),
      ",\"solvable\":", JB(r.cw_solvable),
      ",\"derived_length\":", String(r.cw_derived_length), "}",
    ",\"surv\":{\"mode\":", JStr(r.surv_mode),
      ",\"cv_size\":", String(r.cv_size),
      ",\"pass_count\":", String(r.surv_pass), ",\"hex_fail\":", String(r.surv_hex_fail),
      ",\"gen_fail\":", String(r.surv_gen_fail), "}",
    "}");
end;;

#############################################################################
## ---- main scan ----
#############################################################################
scanT0 := Runtime();;
TotalCapHit := false;;
records := [];;

for ell in LADDER_ELLS do
  if TotalCapHit then continue; fi;
  Print("\n##### ell(N_ord)=", ell, " #####\n");

  for t in [LADDER_T_MIN .. LADDER_T_MAX] do
    if TotalCapHit then break; fi;
    if Runtime() - scanT0 > LADDER_TOTAL_TIME_CAP_MS then
      TotalCapHit := true;
      Add(records, rec(ell := ell, t := t, n := ell+t, w0type := "n/a", signw0 := 0, ncw0 := 0,
                        feasible_k := [], result := "SKIPPED_TIME_CAP"));
      break;
    fi;
    n := ell + t;;
    w0 := MakeCyc([1..ell]);;
    NCw0 := NC(w0, n);;
    signW0 := SignPerm(w0);;
    wtype := CycleStructurePerm(w0);;

    jmax := Int(n/3);;
    kList := [];
    for k in [0 .. Int(n/2)] do
      parityOk := ((-1)^k = signW0);
      jNeed := (n + NCw0 - 2 - k);
      budgetOk := (2*jmax >= jNeed);
      if parityOk and budgetOk then Add(kList, k); fi;
    od;

    if Length(kList) = 0 then
      Add(records, rec(ell := ell, t := t, n := n, w0type := wtype, signw0 := signW0, ncw0 := NCw0,
                        feasible_k := [], result := "SKIPPED_BUDGET"));
      continue;
    fi;

    found := fail;
    for k in kList do
      if Runtime() - scanT0 > LADDER_TOTAL_TIME_CAP_MS then TotalCapHit := true; break; fi;
      hres := Hunt(n, w0, k, LADDER_MAXRESTART, LADDER_MAXSTEP, LADDER_TIME_CAP_PER_K_MS);;
      if hres.a1 <> fail then
        a1 := hres.a1;; b1 := a1 * w0^-1;;
        G := Group(a1, b1);;
        genLabel := "other";
        if Size(G) = Size(SymmetricGroup(n)) and G = SymmetricGroup(n) then genLabel := "S_n";
        elif Size(G) = Size(AlternatingGroup(n)) and G = AlternatingGroup(n) then genLabel := "A_n"; fi;
        if genLabel = "A_n" or genLabel = "S_n" then
          found := rec(a1 := a1, b1 := b1, k := k, j := NrMovedPoints(b1)/3, gen := genLabel);
          break;
        fi;
      fi;
    od;

    if found = fail then
      Add(records, rec(ell := ell, t := t, n := n, w0type := wtype, signw0 := signW0, ncw0 := NCw0,
                        feasible_k := kList, result := "NO_HIT"));
    else
      a1 := found.a1;; b1 := found.b1;;
      w := b1^-1 * a1;;
      v := a1 * b1^-1;;
      aE := a1 * (n+1, n+3);; bE := b1 * (n+1, n+3, n+2);;
      s1 := bE^-1 * aE;; s2 := aE * bE^2;;
      W := MakeWindow(s1, s2);;
      NordMeasured := W.Nord;;

      Cw := Centralizer(SymmetricGroup(n), w);;
      CwSize := Size(Cw);;
      CwStruct := StructureDescription(Cw);;
      CwSolvable := IsSolvable(Cw);;
      if CwSolvable then CwDerivedLength := DerivedLength(Cw); else CwDerivedLength := -1; fi;

      Cv := Centralizer(SymmetricGroup(n), v);;
      CvSize := Size(Cv);;
      passCount := 0; hexFail := 0; genFail := 0; survMode := "";
      if CwSize <= 5000 then
        survMode := "full";
        for z in Elements(Cv) do
          f := (a1^z) * a1;
          if not (s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f) then hexFail := hexFail+1;
          elif Group(W.x, W.y^f) <> W.PN then genFail := genFail+1;
          else passCount := passCount+1; fi;
        od;
      else
        survMode := "skipped(size)";
      fi;

      Print("  HIT ell=", ell, " t=", t, " n=", n, " k=", found.k, " gen=", found.gen,
            " |C(w0)|=", CwSize, " N_ord=", NordMeasured, " surv=", survMode, "\n");

      Add(records, rec(ell := ell, t := t, n := n, w0type := wtype, signw0 := signW0, ncw0 := NCw0,
        feasible_k := kList, result := "HIT",
        k := found.k, j := found.j, gen := found.gen, a1 := a1, b1 := b1,
        n_ord_measured := NordMeasured,
        cw_size := CwSize, cw_struct := CwStruct, cw_solvable := CwSolvable,
        cw_derived_length := CwDerivedLength,
        surv_mode := survMode, cv_size := CvSize,
        surv_pass := passCount, surv_hex_fail := hexFail, surv_gen_fail := genFail));
    fi;
  od;
od;

Print("\n=== LADDER FAMILY SCAN DONE (total_time_cap_hit=", TotalCapHit, ") ===\n");

#############################################################################
## ---- JSON 出力 ----
#############################################################################
selfSha := ComputeSha256File("search/probe/wac_v1/ladder_family_scan.g");;

shardSuffix := "";
if LADDER_SHARD <> "" then shardSuffix := Concatenation("_", LADDER_SHARD); fi;
outName := Concatenation("search/certs/ladder_family", shardSuffix, "_20260731.json");;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"wac_v1-ladder-family-cert/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/ladder_family_scan.g\",\n",
  "  \"window_label\":\"LADDER-FAMILY-SCAN\",\n",
  "  \"f_orientation\":\"mathematician_handwritten\",\n",
  "  \"note\":\"raw measurements only -- interpretation-free. N_ord=9 以外の梯子族(N_ord in {11,13,15,17,19,21,25}、ここでは ell := N_ord、既存 search/strike-a13-ladder.g の N_ord=9 系の規約と同じ)を (ell,1^t) 窓で t の preamble bound 域全体を撃つ。既存 strike-a13-ladder.g は無改変・未参照(新規実装)。hexagon 判定は search/probe/wac_v1/sat_l1_probe11.g / wall2_cert.g と同じ検算済み手書き式(kerchi-judge.g の RtOf は不採用)。W(x,y,c,Bq,PN,N_ord)は search/kerchi-judge.g (JUDGE_LIBRARY_ONLY) の MakeWindow を再利用(N_ord_measured として記録し、ell との一致は解釈せず raw のまま出す)。a1 は 2-opt 山登り(dl3_search.g の Hunt をそのまま流用)。NOT a ledger claim.\",\n",
  "  \"params\":{\n",
  "    \"ells\":", JArr(List(LADDER_ELLS, String)), ",\n",
  "    \"t_min\":", String(LADDER_T_MIN), ",\n",
  "    \"t_max\":", String(LADDER_T_MAX), ",\n",
  "    \"shard\":", JStr(LADDER_SHARD), ",\n",
  "    \"seed\":", String(LADDER_SEED), ",\n",
  "    \"max_restart\":", String(LADDER_MAXRESTART), ",\n",
  "    \"max_step\":", String(LADDER_MAXSTEP), ",\n",
  "    \"time_cap_per_k_ms\":", String(LADDER_TIME_CAP_PER_K_MS), ",\n",
  "    \"total_time_cap_ms\":", String(LADDER_TOTAL_TIME_CAP_MS), "\n",
  "  },\n",
  "  \"total_time_cap_hit\":", JB(TotalCapHit), ",\n",
  "  \"records\":", JArr(List(records, CandRecToJson)), ",\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"gap_invocation\":\"gap -q -o 2g search/probe/wac_v1/ladder_family_scan.g (preamble sets LADDER_ELLS/LADDER_T_MIN/LADDER_T_MAX/LADDER_SHARD)\"\n",
  "  }\n",
  "}\n");;

WriteFile(outName, cert);;
Print("\nWrote ", outName, "\n");
Print("\nLADDER_FAMILY_DRIVER_DONE\n");
QUIT;
