#############################################################################
## search/probe/wac_v1/wall_family_scan.g
##  ジョブ2: P-WALL-2(n=24)以外に非可解核の窓があるか -- 族的確認。
##  対象: w0 型 = (ell, 1^t)、t>=5(C(w0) ⊇ S_t が非可解になりうる域)、
##  ell は奇素数で ell > n/2(原始性が自動になる設計)、n = ell+t を
##  [WALL_N_MIN..WALL_N_MAX](既定 20..34)で枚挙。
##
##  各候補 (n, ell) で:
##   予算チェック(dl3_search.g 由来の parity+Ree budget)
##   -> 2-opt で実現対 (a1,b1) を探す(dl3_search.g の Hunt をそのまま流用)
##   -> HIT なら窓 assert 一式(braid/c=1/P=A_n/|E|/N_ord)
##   -> C_Sn(w0) の位数/構造/可解性(measure only, assert しない)/導来長
##   -> |C_Sn(w0)| <= 5000 なら SURV 全数検算、超えるならランダム 200 個の
##      f_z(Cv からランダム抽出)を検算し「全数でない」ことを明記。
##
##  preamble 変数(未指定なら既定値):
##    WALL_N_MIN, WALL_N_MAX     -- n の走査範囲(既定 20..34)
##    WALL_ELL_MIN, WALL_ELL_MAX -- ell(=n-t)のフィルタ範囲(既定 0..10^9、shard分割用)
##    WALL_SHARD                 -- shard ラベル(出力ファイル名・cert 記録用、任意)
##    WALL_MAXRESTART, WALL_MAXSTEP, WALL_TIME_CAP_PER_K_MS, WALL_TOTAL_TIME_CAP_MS
##        -- Hunt の 2-opt 予算・時間 cap(既定は spectrum_scan.g と同様)
##    WALL_RANDOM_SAMPLE_N       -- |C(w0)|>5000 のときのランダム f_z サンプル数(既定 200)
##
##  raw measurements only -- 予言値/期待値はコードに書かない(接触遮断:
##  ideas/・sol/・docs/notes/sat_l1_v1.md は本スクリプト作成時に未読)。可解性は
##  測るだけで assert しない(非可解を期待しても、コード上は判定条件に使わない)。
##  fail-closed: cap 超過は明記し黙って打ち切らない。
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
  tmp := "search/.tmp_wallfam_cert_sha.txt";
  out := "search/.tmp_wallfam_cert_sha.out";
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
    Error("wall_family_scan.g: Sha256OfString: sha256sum did not return a hash line");
  fi;
  return line{[1 .. 64]};
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_wallfam_cert_selfsha.txt";
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
if not IsBound(WALL_N_MIN) then WALL_N_MIN := 20; fi;
if not IsBound(WALL_N_MAX) then WALL_N_MAX := 34; fi;
if not IsBound(WALL_ELL_MIN) then WALL_ELL_MIN := 0; fi;
if not IsBound(WALL_ELL_MAX) then WALL_ELL_MAX := 1000000000; fi;
if not IsBound(WALL_SHARD) then WALL_SHARD := ""; fi;
if not IsBound(WALL_MAXRESTART) then WALL_MAXRESTART := 60; fi;
if not IsBound(WALL_MAXSTEP) then WALL_MAXSTEP := 1500; fi;
if not IsBound(WALL_TIME_CAP_PER_K_MS) then WALL_TIME_CAP_PER_K_MS := 8000; fi;
if not IsBound(WALL_TOTAL_TIME_CAP_MS) then WALL_TOTAL_TIME_CAP_MS := 10200000; fi;
if not IsBound(WALL_RANDOM_SAMPLE_N) then WALL_RANDOM_SAMPLE_N := 200; fi;

WALL_SEED := 20260731;;
Reset(GlobalMersenneTwister, WALL_SEED);;

#############################################################################
## ---- serialization ----
#############################################################################
CandRecToJson := function(r)
  local base;
  base := Concatenation(
    "{\"n\":", String(r.n), ",\"ell\":", String(r.ell), ",\"t\":", String(r.t),
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
    ",\"window_asserts\":{",
      "\"braid_holds\":", JB(r.braid_holds),
      ",\"c_eq_identity\":", JB(r.c_eq_identity),
      ",\"P_eq_An\":", JB(r.p_eq_an),
      ",\"E_size\":", String(r.e_size),
      ",\"N_ord\":", String(r.n_ord), "}",
    ",\"centralizer_w0\":{\"size\":", String(r.cw_size),
      ",\"structure_description\":", JStr(r.cw_struct),
      ",\"solvable\":", JB(r.cw_solvable),
      ",\"derived_length\":", String(r.cw_derived_length), "}",
    ",\"surv\":{\"mode\":", JStr(r.surv_mode),
      ",\"cv_size\":", String(r.cv_size),
      ",\"sample_size\":", String(r.surv_sample_size),
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

for n in [WALL_N_MIN .. WALL_N_MAX] do
  if TotalCapHit then continue; fi;
  Print("\n##### n=", n, " #####\n");

  ## ell odd prime, ell > n/2, t := n-ell >= 5, and within shard filter
  ellCands := Filtered([3 .. n-5], x -> IsPrimeInt(x) and 2*x > n
                        and x >= WALL_ELL_MIN and x <= WALL_ELL_MAX);;

  for ell in ellCands do
    if Runtime() - scanT0 > WALL_TOTAL_TIME_CAP_MS then
      TotalCapHit := true;
      Add(records, rec(n := n, ell := ell, t := n-ell, w0type := "n/a", signw0 := 0, ncw0 := 0,
                        feasible_k := [], result := "SKIPPED_TIME_CAP"));
      break;
    fi;
    t := n - ell;;
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
      Add(records, rec(n := n, ell := ell, t := t, w0type := wtype, signw0 := signW0, ncw0 := NCw0,
                        feasible_k := [], result := "SKIPPED_BUDGET"));
      continue;
    fi;

    found := fail; kTried := 0;
    for k in kList do
      if Runtime() - scanT0 > WALL_TOTAL_TIME_CAP_MS then TotalCapHit := true; break; fi;
      kTried := kTried + 1;
      hres := Hunt(n, w0, k, WALL_MAXRESTART, WALL_MAXSTEP, WALL_TIME_CAP_PER_K_MS);;
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
      Add(records, rec(n := n, ell := ell, t := t, w0type := wtype, signw0 := signW0, ncw0 := NCw0,
                        feasible_k := kList, result := "NO_HIT"));
    else
      a1 := found.a1;; b1 := found.b1;;
      w := b1^-1 * a1;;
      v := a1 * b1^-1;;
      aE := a1 * (n+1, n+3);; bE := b1 * (n+1, n+3, n+2);;
      s1 := bE^-1 * aE;; s2 := aE * bE^2;;
      braidHolds := (s1*s2*s1 = s2*s1*s2);;
      W := MakeWindow(s1, s2);;
      cIsOne := (W.c = Identity(W.Bq));;
      pEqAn := (W.PN = AlternatingGroup(n));;
      Esize := Size(Group(aE, bE));;
      Nord := W.Nord;;

      Cw := Centralizer(SymmetricGroup(n), w);;
      CwSize := Size(Cw);;
      CwStruct := StructureDescription(Cw);;
      CwSolvable := IsSolvable(Cw);;
      if CwSolvable then CwDerivedLength := DerivedLength(Cw); else CwDerivedLength := -1; fi;

      Cv := Centralizer(SymmetricGroup(n), v);;
      CvSize := Size(Cv);;
      passCount := 0; hexFail := 0; genFail := 0; sampleSize := 0; survMode := "";
      if CwSize <= 5000 then
        survMode := "full";
        for z in Elements(Cv) do
          f := (a1^z) * a1;
          if not (s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f) then hexFail := hexFail+1;
          elif Group(W.x, W.y^f) <> W.PN then genFail := genFail+1;
          else passCount := passCount+1; fi;
        od;
        sampleSize := CvSize;
      else
        survMode := "random_sample(not_exhaustive)";
        CvElts := Elements(Cv);;
        sampleSize := Minimum(WALL_RANDOM_SAMPLE_N, Length(CvElts));;
        sampleIdx := List([1..sampleSize], i -> Random([1..Length(CvElts)]));;
        for idx in sampleIdx do
          z := CvElts[idx];;
          f := (a1^z) * a1;
          if not (s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f) then hexFail := hexFail+1;
          elif Group(W.x, W.y^f) <> W.PN then genFail := genFail+1;
          else passCount := passCount+1; fi;
        od;
      fi;

      Print("  HIT n=", n, " ell=", ell, " t=", t, " k=", found.k, " gen=", found.gen,
            " |C(w0)|=", CwSize, " solvable=", CwSolvable, " surv=", survMode, "\n");

      Add(records, rec(n := n, ell := ell, t := t, w0type := wtype, signw0 := signW0, ncw0 := NCw0,
        feasible_k := kList, result := "HIT",
        k := found.k, j := found.j, gen := found.gen, a1 := a1, b1 := b1,
        braid_holds := braidHolds, c_eq_identity := cIsOne, p_eq_an := pEqAn,
        e_size := Esize, n_ord := Nord,
        cw_size := CwSize, cw_struct := CwStruct, cw_solvable := CwSolvable,
        cw_derived_length := CwDerivedLength,
        surv_mode := survMode, cv_size := CvSize, surv_sample_size := sampleSize,
        surv_pass := passCount, surv_hex_fail := hexFail, surv_gen_fail := genFail));
    fi;
  od;
od;

Print("\n=== WALL FAMILY SCAN DONE (total_time_cap_hit=", TotalCapHit, ") ===\n");

#############################################################################
## ---- JSON 出力 ----
#############################################################################
selfSha := ComputeSha256File("search/probe/wac_v1/wall_family_scan.g");;

shardSuffix := "";
if WALL_SHARD <> "" then shardSuffix := Concatenation("_", WALL_SHARD); fi;
outName := Concatenation("search/certs/wall_family", shardSuffix, "_20260731.json");;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"wac_v1-wall-family-cert/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/wall_family_scan.g\",\n",
  "  \"window_label\":\"WALL-FAMILY-SCAN\",\n",
  "  \"f_orientation\":\"mathematician_handwritten\",\n",
  "  \"note\":\"raw measurements only -- interpretation-free. P-WALL-2(n=24)以外に非可解核の窓があるか(族的確認)。可解性は測定するだけで判定条件には使わない(assert しない)。hexagon 判定は search/probe/wac_v1/sat_l1_probe11.g / wall2_cert.g と同じ検算済み手書き式(kerchi-judge.g の RtOf は不採用)。W(x,y,c,Bq,PN,N_ord)は search/kerchi-judge.g (JUDGE_LIBRARY_ONLY) の MakeWindow を再利用。a1 は 2-opt 山登り(dl3_search.g の Hunt をそのまま流用)。|C_Sn(w0)|>5000 の場合は SURV をランダム抽出に切り替え、全数でないことを surv.mode に明記する。NOT a ledger claim.\",\n",
  "  \"params\":{\n",
  "    \"n_min\":", String(WALL_N_MIN), ",\n",
  "    \"n_max\":", String(WALL_N_MAX), ",\n",
  "    \"ell_min\":", String(WALL_ELL_MIN), ",\n",
  "    \"ell_max\":", String(WALL_ELL_MAX), ",\n",
  "    \"shard\":", JStr(WALL_SHARD), ",\n",
  "    \"seed\":", String(WALL_SEED), ",\n",
  "    \"max_restart\":", String(WALL_MAXRESTART), ",\n",
  "    \"max_step\":", String(WALL_MAXSTEP), ",\n",
  "    \"time_cap_per_k_ms\":", String(WALL_TIME_CAP_PER_K_MS), ",\n",
  "    \"total_time_cap_ms\":", String(WALL_TOTAL_TIME_CAP_MS), ",\n",
  "    \"random_sample_n\":", String(WALL_RANDOM_SAMPLE_N), "\n",
  "  },\n",
  "  \"total_time_cap_hit\":", JB(TotalCapHit), ",\n",
  "  \"records\":", JArr(List(records, CandRecToJson)), ",\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"gap_invocation\":\"gap -q -o 2g search/probe/wac_v1/wall_family_scan.g (preamble sets WALL_N_MIN/MAX/ELL_MIN/ELL_MAX/SHARD)\"\n",
  "  }\n",
  "}\n");;

WriteFile(outName, cert);;
Print("\nWrote ", outName, "\n");
Print("\nWALL_FAMILY_DRIVER_DONE\n");
QUIT;
