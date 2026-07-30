#############################################################################
## search/probe/wac_v1/tmax_scan.g
##  裁定247 の新問題: 実効上限 t_max(ell) の走査。定理 LAD は t <= (ell-1)/2
##  を与えるが、実測の最大 t はもっと小さい(ell=25 で上限12に対し実現4)。
##  実効的な障害の所在を切り分けるため、各 (ell,t) について 3 段階の判定を
##  分けて記録する:
##   (a) Ree 予算(dl3_search.g/spectrum_scan.g 由来の (k,j) 枚挙)で
##       feasible な k が存在するか -- パリティ抜きで budgetOk のみを見る。
##       存在しなければ "BUDGET_FAIL"。
##   (b) budget-feasible な k のうち、符号パリティ((-1)^k = sign(w0)) も
##       通る k が存在するか。存在しなければ "PARITY_FAIL"。
##   (c) budget+parity-feasible な k について、2-opt Hunt(dl3_search.g の
##       Hunt をそのまま流用)で実現対 (a1,b1) を探す。<a1,b1> in {A_n,S_n}
##       の最初のヒットで打ち切り。どの k でも見つからなければ "GEN_FAIL"
##       (陰性主張ではない -- 探索予算内で見つからなかっただけ)。見つかれば
##       "HIT" とし、C_Sn(w0) の位数/構造/可解性/導来長を記録する。
##
##  preamble 変数(未指定なら既定値):
##    TMAX_ELLS                      -- 走査する ell のリスト(既定 [11,13,17,19,23,25,29,31])
##    TMAX_SHARD                     -- shard ラベル(出力ファイル名・cert 記録用、任意)
##    TMAX_MAXRESTART, TMAX_MAXSTEP  -- Hunt の 2-opt 予算(既定 60 / 1500)
##    TMAX_TIME_CAP_PER_K_MS         -- Hunt 1回(1 k値)あたりの時間 cap ms(既定 8000)
##    TMAX_TOTAL_TIME_CAP_MS         -- スクリプト全体の時間 cap ms(既定 10200000=170分。
##                                       CI timeout_min=180 に対し cert 書き出しの余裕を残す)
##
##  raw measurements only -- 予言値/期待値はコードに書かない(接触遮断)。
##  fail-closed: 各 cap 超過は "SKIPPED_TIME_CAP" 等で明記し、黙って打ち切らない。
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
  tmp := "search/.tmp_tmax_cert_sha.txt";
  out := "search/.tmp_tmax_cert_sha.out";
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
    Error("tmax_scan.g: Sha256OfString: sha256sum did not return a hash line");
  fi;
  return line{[1 .. 64]};
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_tmax_cert_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1 .. 64]};
end;;

## ---- fail-closed JSON syntax check (前回の事故対策) ----
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
    Error("tmax_scan.g: ValidateJsonFile: python json.load failed to parse ", path,
          " -- got: ", line);
  fi;
  return true;
end;;

#############################################################################
## ---- MakeCyc ----
#############################################################################
MakeCyc := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;

#############################################################################
## ---- 2-opt local search Hunt (dl3_search.g/spectrum_scan.g と同一実装) ----
#############################################################################
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
if not IsBound(TMAX_ELLS) then TMAX_ELLS := [11, 13, 17, 19, 23, 25, 29, 31]; fi;
if not IsBound(TMAX_SHARD) then TMAX_SHARD := ""; fi;
if not IsBound(TMAX_MAXRESTART) then TMAX_MAXRESTART := 60; fi;
if not IsBound(TMAX_MAXSTEP) then TMAX_MAXSTEP := 1500; fi;
if not IsBound(TMAX_TIME_CAP_PER_K_MS) then TMAX_TIME_CAP_PER_K_MS := 8000; fi;
if not IsBound(TMAX_TOTAL_TIME_CAP_MS) then TMAX_TOTAL_TIME_CAP_MS := 10200000; fi;

TMAX_SEED := 20260731;;
Reset(GlobalMersenneTwister, TMAX_SEED);;

#############################################################################
## ---- serialization helpers ----
#############################################################################
KAttemptsToJson := function(atts)
  local items, a;
  items := [];
  for a in atts do
    if IsBound(a.skipped) then
      Add(items, Concatenation("{\"k\":", String(a.k), ",\"skipped\":true,\"reason\":",
            JStr(a.reason), "}"));
    elif a.hit = false then
      Add(items, Concatenation("{\"k\":", String(a.k), ",\"hit\":false,\"timed_out\":",
            JB(a.timed_out), ",\"restarts\":", String(a.restarts), "}"));
    else
      Add(items, Concatenation("{\"k\":", String(a.k), ",\"hit\":true,\"j\":", String(a.j),
            ",\"gen\":", JStr(a.gen), ",\"group_order\":", String(a.group_order), "}"));
    fi;
  od;
  return JArr(items);
end;;

TRecToJson := function(r)
  local base;
  base := Concatenation(
    "{\"t\":", String(r.t),
    ",\"n\":", String(r.n),
    ",\"sign_w0\":", String(r.signw0),
    ",\"NC_w0\":", String(r.ncw0),
    ",\"budget_feasible_k\":", JArr(List(r.budget_feasible_k, String)),
    ",\"budget_and_parity_feasible_k\":", JArr(List(r.bp_feasible_k, String)),
    ",\"stage\":", JStr(r.stage));
  if r.stage = "BUDGET_FAIL" then
    return Concatenation(base, "}");
  elif r.stage = "PARITY_FAIL" then
    return Concatenation(base, "}");
  elif r.stage = "SKIPPED_TIME_CAP" then
    return Concatenation(base, "}");
  elif r.stage = "GEN_FAIL" then
    return Concatenation(base, ",\"k_attempts\":", KAttemptsToJson(r.k_attempts), "}");
  else  ## HIT
    return Concatenation(base,
      ",\"k_attempts\":", KAttemptsToJson(r.k_attempts),
      ",\"k\":", String(r.k), ",\"j\":", String(r.j),
      ",\"gen_label\":", JStr(r.gen),
      ",\"a1\":", JStr(String(r.a1)), ",\"b1\":", JStr(String(r.b1)),
      ",\"braid_holds\":", JB(r.braid_holds),
      ",\"centralizer_w0\":{\"size\":", String(r.centralizer_w0.size),
        ",\"structure_description\":", JStr(r.centralizer_w0.structure),
        ",\"solvable\":", JB(r.centralizer_w0.solvable),
        ",\"derived_length\":", String(r.centralizer_w0.derived_length), "}",
      "}");
  fi;
end;;

EllRecToJson := function(er)
  return Concatenation("{\"ell\":", String(er.ell),
    ",\"t_range\":\"0..", String(er.tmax_theory), "\"",
    ",\"ell_time_cap_hit\":", JB(er.ell_time_cap_hit),
    ",\"t_records\":", JArr(List(er.t_records, TRecToJson)), "}");
end;;

#############################################################################
## ---- main scan ----
#############################################################################
scanT0 := Runtime();;
TotalCapHit := false;;
ellRecords := [];;

for ell in TMAX_ELLS do
  if TotalCapHit then
    Add(ellRecords, rec(ell := ell, tmax_theory := Int((ell-1)/2),
                         ell_time_cap_hit := true, t_records := []));
    continue;
  fi;
  Print("\n##### ell=", ell, " (theory t_max=", Int((ell-1)/2), ") #####\n");

  tRecs := [];;
  ellCapHit := false;;
  tmaxTheory := Int((ell-1)/2);;

  for t in [0 .. tmaxTheory] do
    if Runtime() - scanT0 > TMAX_TOTAL_TIME_CAP_MS then
      TotalCapHit := true; ellCapHit := true;
      break;
    fi;

    n := ell + t;;
    w0 := MakeCyc([1..ell]);;   ## fixes ell+1..ell+t (t fixed points, since deg = n = ell+t)
    NCw0 := NC(w0, n);;
    signW0 := SignPerm(w0);;

    jmax := Int(n/3);;

    ## (a) Ree budget only (parity ignored)
    budgetKList := [];;
    for k in [0 .. Int(n/2)] do
      jNeed := (n + NCw0 - 2 - k);;
      if (2*jmax >= jNeed) then Add(budgetKList, k); fi;
    od;

    if Length(budgetKList) = 0 then
      Add(tRecs, rec(t := t, n := n, signw0 := signW0, ncw0 := NCw0,
                      budget_feasible_k := [], bp_feasible_k := [], stage := "BUDGET_FAIL"));
      continue;
    fi;

    ## (b) among budget-feasible k, does parity also pass?
    bpKList := Filtered(budgetKList, k -> ((-1)^k = signW0));;

    if Length(bpKList) = 0 then
      Add(tRecs, rec(t := t, n := n, signw0 := signW0, ncw0 := NCw0,
                      budget_feasible_k := budgetKList, bp_feasible_k := [],
                      stage := "PARITY_FAIL"));
      continue;
    fi;

    ## (c) among budget+parity-feasible k, 2-opt Hunt for realization
    found := fail; kAttempts := []; tCapHitHere := false;
    for k in bpKList do
      if Runtime() - scanT0 > TMAX_TOTAL_TIME_CAP_MS then
        TotalCapHit := true; ellCapHit := true; tCapHitHere := true;
        Add(kAttempts, rec(k := k, skipped := true, reason := "total_time_cap"));
        break;
      fi;
      hres := Hunt(n, w0, k, TMAX_MAXRESTART, TMAX_MAXSTEP, TMAX_TIME_CAP_PER_K_MS);;
      if hres.a1 = fail then
        Add(kAttempts, rec(k := k, hit := false, timed_out := hres.timedOut,
                            restarts := hres.restarts));
      else
        a1 := hres.a1;; b1 := a1 * w0^-1;;
        G := Group(a1, b1);;
        genLabel := "other";
        if Size(G) = Size(SymmetricGroup(n)) and G = SymmetricGroup(n) then genLabel := "S_n";
        elif Size(G) = Size(AlternatingGroup(n)) and G = AlternatingGroup(n) then genLabel := "A_n"; fi;
        Add(kAttempts, rec(k := k, hit := true, j := NrMovedPoints(b1)/3, gen := genLabel,
                            group_order := Size(G)));
        if genLabel = "A_n" or genLabel = "S_n" then
          found := rec(a1 := a1, b1 := b1, k := k, j := NrMovedPoints(b1)/3, gen := genLabel);
          break;
        fi;
      fi;
    od;

    if found = fail then
      stage := "GEN_FAIL";;
      if tCapHitHere then stage := "SKIPPED_TIME_CAP"; fi;
      Add(tRecs, rec(t := t, n := n, signw0 := signW0, ncw0 := NCw0,
                      budget_feasible_k := budgetKList, bp_feasible_k := bpKList,
                      stage := stage, k_attempts := kAttempts));
    else
      a1 := found.a1;; b1 := found.b1;;
      w := b1^-1 * a1;;   ## = w0 exactly (a1^2=1 identity)
      aE := a1 * (n+1, n+3);; bE := b1 * (n+1, n+3, n+2);;
      s1 := bE^-1 * aE;; s2 := aE * bE^2;;
      braidHolds := (s1*s2*s1 = s2*s1*s2);;

      Cw := Centralizer(SymmetricGroup(n), w);;
      CwSize := Size(Cw);;
      CwStruct := StructureDescription(Cw);;
      CwSolvable := IsSolvable(Cw);;
      if CwSolvable then CwDerivedLength := DerivedLength(Cw); else CwDerivedLength := -1; fi;

      Print("  HIT ell=", ell, " t=", t, " k=", found.k, " gen=", found.gen,
            " |C(w0)|=", CwSize, "\n");

      Add(tRecs, rec(t := t, n := n, signw0 := signW0, ncw0 := NCw0,
        budget_feasible_k := budgetKList, bp_feasible_k := bpKList,
        stage := "HIT", k_attempts := kAttempts,
        a1 := a1, b1 := b1, k := found.k, j := found.j, gen := found.gen,
        braid_holds := braidHolds,
        centralizer_w0 := rec(size := CwSize, structure := CwStruct, solvable := CwSolvable,
                               derived_length := CwDerivedLength)));
    fi;
  od;

  Add(ellRecords, rec(ell := ell, tmax_theory := tmaxTheory,
                       ell_time_cap_hit := ellCapHit, t_records := tRecs));
od;

Print("\n=== SCAN DONE (total_time_cap_hit=", TotalCapHit, ") ===\n");

#############################################################################
## ---- JSON 出力 ----
#############################################################################
selfSha := ComputeSha256File("search/probe/wac_v1/tmax_scan.g");;

shardSuffix := "";
if TMAX_SHARD <> "" then shardSuffix := Concatenation("_", TMAX_SHARD); fi;
ellsStr := JoinC(List(TMAX_ELLS, String), "-");;
outName := Concatenation("search/certs/tmax_scan_", ellsStr, shardSuffix, "_20260731.json");;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"wac_v1-tmax-scan-cert/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/tmax_scan.g\",\n",
  "  \"window_label\":\"TMAX-SCAN\",\n",
  "  \"f_orientation\":\"n_a\"",
  ",\n",
  "  \"note\":\"raw measurements only -- interpretation-free. (ell,t) ごとに 3段階(BUDGET_FAIL/PARITY_FAIL/{GEN_FAIL,HIT})を分けて記録し、実効上限の障害の所在(予算/パリティ/2-opt生成)を切り分ける。GEN_FAIL は陰性主張ではない(探索予算内で未発見なだけ、UNKNOWN)。hexagon 判定・SURV 全数検算は本 probe では行わない(スコープ外 -- 目的は t_max の障害切り分けのみ)。W0 は ell-サイクル(t 個の不動点)。2-opt Hunt は dl3_search.g/spectrum_scan.g と同一実装、seed固定。\",\n",
  "  \"params\":{\n",
  "    \"ells\":", JArr(List(TMAX_ELLS, String)), ",\n",
  "    \"shard\":", JStr(TMAX_SHARD), ",\n",
  "    \"seed\":", String(TMAX_SEED), ",\n",
  "    \"max_restart\":", String(TMAX_MAXRESTART), ",\n",
  "    \"max_step\":", String(TMAX_MAXSTEP), ",\n",
  "    \"time_cap_per_k_ms\":", String(TMAX_TIME_CAP_PER_K_MS), ",\n",
  "    \"total_time_cap_ms\":", String(TMAX_TOTAL_TIME_CAP_MS), "\n",
  "  },\n",
  "  \"total_time_cap_hit\":", JB(TotalCapHit), ",\n",
  "  \"records\":", JArr(List(ellRecords, EllRecToJson)), ",\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"gap_invocation\":\"gap -q -o 2g search/probe/wac_v1/tmax_scan.g (preamble sets TMAX_ELLS/TMAX_SHARD)\"\n",
  "  }\n",
  "}\n");;

WriteFile(outName, cert);;
ValidateJsonFile(outName);;
Print("\nWrote ", outName, " (json.load OK)\n");
Print("\nTMAX_SCAN_DRIVER_DONE\n");
QUIT;
