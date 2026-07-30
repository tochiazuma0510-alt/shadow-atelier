#############################################################################
## search/probe/wac_v1/spectrum_scan.g
##  ジョブ1: 「どの巡回型 w0 が実現するか」の spectrum 実現域の大規模走査。
##  各 n について w0 の巡回型 tau を (ell,1^t) 型 -> (ell^r,1^t) 型 -> 一般型
##  の順に枚挙(t>=0, ell 奇)。各 tau について:
##   (a) Ree 予算 c(a1)+c(b1)+c(w) <= n+2 と符号パリティで feasible な (k,j)
##       を紙で枚挙(dl3_search.g の設計をそのまま流用)。空なら
##       result="SKIPPED_BUDGET" として次へ。
##   (b) feasible があれば 2-opt 山登り(dl3_search.g の Hunt を再利用)で
##       実現対 (a1,b1) を探す。最初に見つかった k で打ち切り、a1,b1・
##       <a1,b1> の生成先・C_Sn(w0) の位数/構造/可解性/導来長を記録。
##       見つからなければ試行数つきで NO_HIT(陰性主張はしない)。
##   (c) SURV 全数検算は |C_Sn(w0)| <= 5000 のときだけ実行(通過数を記録)。
##       超えたら "skipped(size)" と明記してスキップする。
##
##  preamble 変数(未指定なら既定値):
##    SPEC_N_MIN, SPEC_N_MAX        -- n の走査範囲(既定 10..30)
##    SPEC_SHARD                    -- shard ラベル(出力ファイル名・cert 記録用、任意)
##    SPEC_GENERAL_CAP              -- 一般型 tau を n ごとに何個まで試すか(既定 20)
##    SPEC_MAXRESTART, SPEC_MAXSTEP -- Hunt の 2-opt 予算(既定 60 / 1500)
##    SPEC_TIME_CAP_PER_K_MS        -- Hunt 1回(1 k値)あたりの時間 cap ms(既定 8000)
##    SPEC_TOTAL_TIME_CAP_MS        -- スクリプト全体の時間 cap ms(既定 10200000=170分。
##                                      CI timeout_min=180 に対し cert 書き出しの余裕を残す)
##
##  raw measurements only -- 予言値/期待値はコードに書かない(接触遮断:
##  ideas/・sol/・docs/notes/sat_l1_v1.md は本スクリプト作成時に未読)。
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
  tmp := "search/.tmp_spec_cert_sha.txt";
  out := "search/.tmp_spec_cert_sha.out";
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
    Error("spectrum_scan.g: Sha256OfString: sha256sum did not return a hash line");
  fi;
  return line{[1 .. 64]};
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_spec_cert_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1 .. 64]};
end;;

#############################################################################
## ---- MakeCyc / MakeCycType ----
#############################################################################
MakeCyc := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;

## parts = list of cycle lengths (sum = n implied by caller's ambient degree).
## Builds a permutation with exactly those cycles on consecutive point blocks
## starting at 1 (any length-1 parts are just fixed points, contribute nothing).
MakeCycType := function(parts)
  local w, pos, l;
  w := ();
  pos := 1;
  for l in parts do
    if l > 1 then
      w := w * MakeCyc(List([0 .. l-1], i -> pos + i));
    fi;
    pos := pos + l;
  od;
  return w;
end;;

#############################################################################
## ---- 2-opt local search Hunt (dl3_search.g と同一実装) ----
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
if not IsBound(SPEC_N_MIN) then SPEC_N_MIN := 10; fi;
if not IsBound(SPEC_N_MAX) then SPEC_N_MAX := 30; fi;
if not IsBound(SPEC_SHARD) then SPEC_SHARD := ""; fi;
if not IsBound(SPEC_GENERAL_CAP) then SPEC_GENERAL_CAP := 20; fi;
if not IsBound(SPEC_MAXRESTART) then SPEC_MAXRESTART := 60; fi;
if not IsBound(SPEC_MAXSTEP) then SPEC_MAXSTEP := 1500; fi;
if not IsBound(SPEC_TIME_CAP_PER_K_MS) then SPEC_TIME_CAP_PER_K_MS := 8000; fi;
if not IsBound(SPEC_TOTAL_TIME_CAP_MS) then SPEC_TOTAL_TIME_CAP_MS := 10200000; fi;

SPEC_SEED := 20260731;;
Reset(GlobalMersenneTwister, SPEC_SEED);;

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

TauRecToJson := function(r)
  local partsJson, base;
  partsJson := JArr(List(r.tau.parts, String));
  base := Concatenation(
    "{\"kind\":", JStr(r.tau.kind),
    ",\"ell\":", String(r.tau.ell),
    ",\"r\":", String(r.tau.r),
    ",\"t\":", String(r.tau.t),
    ",\"parts\":", partsJson,
    ",\"w0_cycle_type\":", JStr(String(r.w0type)),
    ",\"sign_w0\":", String(r.signw0),
    ",\"NC_w0\":", String(r.ncw0),
    ",\"feasible_k\":", JArr(List(r.feasible_k, String)),
    ",\"result\":", JStr(r.result));
  if r.result = "SKIPPED_BUDGET" then
    return Concatenation(base, "}");
  elif r.result = "SKIPPED_TIME_CAP" then
    return Concatenation(base, "}");
  elif r.result = "NO_HIT" then
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
      ",\"surv\":{\"mode\":", JStr(r.surv.mode),
        ",\"cw_size\":", String(r.surv.cw_size),
        ",\"cv_size\":", String(r.surv.cv_size),
        ",\"pass_count\":", String(r.surv.pass_count),
        ",\"hex_fail\":", String(r.surv.hex_fail),
        ",\"gen_fail\":", String(r.surv.gen_fail), "}",
      "}");
  fi;
end;;

NRecToJson := function(nr)
  return Concatenation("{\"n\":", String(nr.n),
    ",\"general_partition_total\":", String(nr.general_partition_total),
    ",\"general_used\":", String(nr.general_used),
    ",\"general_truncated\":", JB(nr.general_truncated),
    ",\"n_time_cap_hit\":", JB(nr.n_time_cap_hit),
    ",\"taus\":", JArr(List(nr.taus, TauRecToJson)), "}");
end;;

#############################################################################
## ---- main scan ----
#############################################################################
scanT0 := Runtime();;
TotalCapHit := false;;
records := [];;

for n in [SPEC_N_MIN .. SPEC_N_MAX] do
  if TotalCapHit then
    Add(records, rec(n := n, general_partition_total := 0, general_used := 0,
                      general_truncated := false, n_time_cap_hit := true, taus := []));
    continue;
  fi;
  Print("\n##### n=", n, " #####\n");

  ## ---- build tau list: A then B then C (capped) ----
  tauList := [];

  for ell in Filtered([3 .. n], x -> x mod 2 = 1) do
    Add(tauList, rec(kind := "A", ell := ell, r := 1, t := n - ell, parts := [ell]));
  od;

  for ell in Filtered([3 .. n], x -> x mod 2 = 1) do
    r := 2;
    while r * ell <= n do
      Add(tauList, rec(kind := "B", ell := ell, r := r, t := n - r*ell,
                        parts := List([1..r], i -> ell)));
      r := r + 1;
    od;
  od;

  allParts := Partitions(n);;
  genList := [];
  for p in allParts do
    nontrivial := Filtered(p, x -> x > 1);
    if Length(nontrivial) < 2 then continue; fi;            ## identity / type-A: skip
    if Length(Set(nontrivial)) = 1 then continue; fi;        ## type-B (all equal parts): skip
    Add(genList, p);
  od;
  genCount := Length(genList);;
  genUsed := genList{[1 .. Minimum(genCount, SPEC_GENERAL_CAP)]};;
  genTruncated := (genCount > SPEC_GENERAL_CAP);;
  for p in genUsed do
    Add(tauList, rec(kind := "C", ell := 0, r := 0, t := 0, parts := ShallowCopy(p)));
  od;

  Print("  tau count: A+B=", Length(tauList) - Length(genUsed),
        "  C(used/total)=", Length(genUsed), "/", genCount,
        (genTruncated), "\n");

  nRecs := [];
  nCapHit := false;

  for tau in tauList do
    if Runtime() - scanT0 > SPEC_TOTAL_TIME_CAP_MS then
      TotalCapHit := true; nCapHit := true;
      break;
    fi;
    w0 := MakeCycType(tau.parts);;
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
      Add(nRecs, rec(tau := tau, w0type := wtype, signw0 := signW0, ncw0 := NCw0,
                      feasible_k := [], result := "SKIPPED_BUDGET"));
    else
      found := fail; kAttempts := [];
      for k in kList do
        if Runtime() - scanT0 > SPEC_TOTAL_TIME_CAP_MS then
          TotalCapHit := true; nCapHit := true;
          Add(kAttempts, rec(k := k, skipped := true, reason := "total_time_cap"));
          break;
        fi;
        hres := Hunt(n, w0, k, SPEC_MAXRESTART, SPEC_MAXSTEP, SPEC_TIME_CAP_PER_K_MS);;
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
        noHitResult := "NO_HIT";
        if nCapHit and Length(kAttempts) > 0
           and IsBound(kAttempts[Length(kAttempts)].skipped) then
          noHitResult := "SKIPPED_TIME_CAP";
        fi;
        Add(nRecs, rec(tau := tau, w0type := wtype, signw0 := signW0, ncw0 := NCw0,
                        feasible_k := kList,
                        result := noHitResult,
                        k_attempts := kAttempts));
      else
        a1 := found.a1;; b1 := found.b1;;
        w := b1^-1 * a1;;   ## = w0 exactly (a1^2=1 identity, mirrors dl3_search.g algebra)
        v := a1 * b1^-1;;
        aE := a1 * (n+1, n+3);; bE := b1 * (n+1, n+3, n+2);;
        s1 := bE^-1 * aE;; s2 := aE * bE^2;;
        braidHolds := (s1*s2*s1 = s2*s1*s2);;
        W := MakeWindow(s1, s2);;

        Cw := Centralizer(SymmetricGroup(n), w);;
        CwSize := Size(Cw);;
        CwStruct := StructureDescription(Cw);;
        CwSolvable := IsSolvable(Cw);;
        if CwSolvable then CwDerivedLength := DerivedLength(Cw); else CwDerivedLength := -1; fi;

        Cv := Centralizer(SymmetricGroup(n), v);;
        CvSize := Size(Cv);;
        passCount := 0; hexFail := 0; genFail := 0;
        if CwSize <= 5000 then
          survMode := "full";
          for z in Elements(Cv) do
            f := (a1^z) * a1;
            if not (s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f) then
              hexFail := hexFail + 1;
            elif Group(W.x, W.y^f) <> W.PN then
              genFail := genFail + 1;
            else
              passCount := passCount + 1;
            fi;
          od;
        else
          survMode := "skipped(size)";
        fi;

        Print("  HIT tau=", tau.kind, " parts=", tau.parts, " k=", found.k, " gen=", found.gen,
              " |C(w0)|=", CwSize, " surv=", survMode, "\n");

        Add(nRecs, rec(tau := tau, w0type := wtype, signw0 := signW0, ncw0 := NCw0,
          feasible_k := kList, result := "HIT", k_attempts := kAttempts,
          a1 := a1, b1 := b1, k := found.k, j := found.j, gen := found.gen,
          braid_holds := braidHolds,
          centralizer_w0 := rec(size := CwSize, structure := CwStruct, solvable := CwSolvable,
                                 derived_length := CwDerivedLength),
          surv := rec(mode := survMode, cw_size := CwSize, cv_size := CvSize,
                      pass_count := passCount, hex_fail := hexFail, gen_fail := genFail)));
      fi;
    fi;
  od;

  Add(records, rec(n := n, general_partition_total := genCount, general_used := Length(genUsed),
                    general_truncated := genTruncated, n_time_cap_hit := nCapHit, taus := nRecs));
od;

Print("\n=== SCAN DONE (total_time_cap_hit=", TotalCapHit, ") ===\n");

#############################################################################
## ---- JSON 出力 ----
#############################################################################
selfSha := ComputeSha256File("search/probe/wac_v1/spectrum_scan.g");;

shardSuffix := "";
if SPEC_SHARD <> "" then shardSuffix := Concatenation("_", SPEC_SHARD); fi;
outName := Concatenation("search/certs/spectrum_scan_", String(SPEC_N_MIN), "-", String(SPEC_N_MAX),
             shardSuffix, "_20260731.json");;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"wac_v1-spectrum-scan-cert/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/spectrum_scan.g\",\n",
  "  \"window_label\":\"SPECTRUM-SCAN\",\n",
  "  \"f_orientation\":\"mathematician_handwritten\",\n",
  "  \"note\":\"raw measurements only -- interpretation-free. hexagon 判定は search/probe/wac_v1/sat_l1_probe11.g / wall2_cert.g と同じ検算済み手書き式(kerchi-judge.g の RtOf は不採用)。W(x,y,c,Bq,PN,N_ord)は search/kerchi-judge.g (JUDGE_LIBRARY_ONLY) の MakeWindow を再利用。a1 は 2-opt 山登り(dl3_search.g の Hunt をそのまま流用)。NOT a ledger claim.\",\n",
  "  \"params\":{\n",
  "    \"n_min\":", String(SPEC_N_MIN), ",\n",
  "    \"n_max\":", String(SPEC_N_MAX), ",\n",
  "    \"shard\":", JStr(SPEC_SHARD), ",\n",
  "    \"general_cap\":", String(SPEC_GENERAL_CAP), ",\n",
  "    \"seed\":", String(SPEC_SEED), ",\n",
  "    \"max_restart\":", String(SPEC_MAXRESTART), ",\n",
  "    \"max_step\":", String(SPEC_MAXSTEP), ",\n",
  "    \"time_cap_per_k_ms\":", String(SPEC_TIME_CAP_PER_K_MS), ",\n",
  "    \"total_time_cap_ms\":", String(SPEC_TOTAL_TIME_CAP_MS), "\n",
  "  },\n",
  "  \"total_time_cap_hit\":", JB(TotalCapHit), ",\n",
  "  \"records\":", JArr(List(records, NRecToJson)), ",\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"gap_invocation\":\"gap -q -o 2g search/probe/wac_v1/spectrum_scan.g (preamble sets SPEC_N_MIN/SPEC_N_MAX/SPEC_SHARD)\"\n",
  "  }\n",
  "}\n");;

WriteFile(outName, cert);;
Print("\nWrote ", outName, "\n");
Print("\nSPECTRUM_SCAN_DRIVER_DONE\n");
QUIT;
