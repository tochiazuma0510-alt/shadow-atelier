#############################################################################
## search/probe/wac_v1/l25t5_rehunt.g
##  生成の穴の最後の1点、ell=25,t=5(n=30)の狙い撃ち再ハント。
##  裁定254/tmax_budget_and_holes_v1.md §2.3 の残り UNKNOWN。
##  厳密計数(search/certs/l25t5_count_20260731.json)で T_trans([25,1^5])=378000>0
##  (推移な(2,3)-分解は実在)が確定済み。旧ハント(tmax_holes_hunt2.g、
##  max_restart=40,max_step=6000)は40 hit全て非推移(軌道[28,1,1]/[29,1])で
##  取りこぼした。本 probe は非生成 hit だけでなく非推移 hit・A_n/S_n でない
##  推移 hit も「捨てて続行」し、全ての落ち先(位数・軌道長分布)を記録する。
##  期待値/予言はコードに書かない -- どの型に落ちるかは測って初めて分かる。
##  手本: tmax_holes_hunt2.g(非生成hitを捨てて続行の設計)+ dl3_search.g
##  (時間cap付きHunt・cert出力パターン)。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
SizeScreen([4096, 0]);;

JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");   ## JStr, JB, JArr, JoinC, WriteFile

NC := function(p, nn)
  return nn - NrMovedPoints(p) + Length(Cycles(p, MovedPoints(p)));
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_l25t5_rehunt_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1 .. 64]};
end;;

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
    Error("l25t5_rehunt.g: ValidateJsonFile: python json.load failed to parse ", path,
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
## ---- fixed target: ell=25, t=5, n=30 ----
#############################################################################
ELL := 25;;  T := 5;;  N := ELL + T;;
W0 := MakeCyc([1 .. ELL]);;   ## 25-cycle, fixes 26..30
NCw0 := NC(W0, N);;
signW0 := SignPerm(W0);;

## closed-form budget check (tmax_budget_and_holes_v1.md 定理): 5t <= ell+6-6*delta(n)
DeltaN := function(n)
  return (n mod 4)/2 + (2/3)*(n mod 3);
end;;
deltaN := DeltaN(N);;
budgetRHS := ELL + 6 - 6*deltaN;;
budgetLHS := 5*T;;
closedFormFeasible := (budgetLHS <= budgetRHS);;

Print("ell=", ELL, " t=", T, " n=", N, " NC(w0)=", NCw0, " sign(w0)=", signW0, "\n");
Print("closed-form budget: 5t=", budgetLHS, " <= ell+6-6*delta(n)=", budgetRHS,
      " (delta(n)=", deltaN, ")  feasible=", closedFormFeasible, "\n");

## explicit Ree+parity (k,j) enumeration (same method as dl3_search.g/tmax_scan.g)
jmax := Int(N/3);;
budgetKList := [];;
for k in [0 .. Int(N/2)] do
  jNeed := (N + NCw0 - 2 - k);;
  if (2*jmax >= jNeed) then Add(budgetKList, k); fi;
od;;
bpKList := Filtered(budgetKList, k -> ((-1)^k = signW0));;
Print("budget-feasible k (parity ignored) = ", budgetKList, "\n");
Print("budget+parity-feasible k = ", bpKList, "\n");

#############################################################################
## ---- 2-opt hunt loop: 非生成 hit・非推移 hit・A_n/S_n でない推移 hit も
##      全て「捨てて続行」。落ち先を位数+軌道長で分類して記録する。 ----
#############################################################################
RecordHit := function(dist, key)
  local idx;
  idx := PositionProperty(dist, r -> r.key = key);
  if idx = fail then
    Add(dist, rec(key := key, count := 1));
  else
    dist[idx].count := dist[idx].count + 1;
  fi;
end;;

HuntLoop := function(n, w0, k, maxRestart, maxStep, timeCapMs)
  local rs, pts, m, d, step, i, j, m2, d2, mk, Def, t0, hits, dist,
        a1, b1, G, trans, genLabel, orbLens, key, timedOut, restartsUsed;
  mk := function(mm) return Product(List(mm, p -> (p[1],p[2])), ()); end;
  Def := function(mm) return NrMovedPoints((mk(mm)*w0^-1)^3); end;
  t0 := Runtime();
  hits := 0;
  dist := [];
  timedOut := false;
  restartsUsed := 0;
  for rs in [1 .. maxRestart] do
    restartsUsed := rs;
    if Runtime() - t0 > timeCapMs then timedOut := true; break; fi;
    pts := Shuffle(ShallowCopy([1 .. n]));
    m := List([1 .. k], i -> [pts[2*i-1], pts[2*i]]);
    d := Def(m);
    for step in [1 .. maxStep] do
      if Runtime() - t0 > timeCapMs then timedOut := true; break; fi;
      if d = 0 then
        hits := hits + 1;
        a1 := mk(m); b1 := a1 * w0^-1;
        G := Group(a1, b1);
        trans := IsTransitive(G, [1 .. n]);
        if trans then
          if Size(G) = Size(AlternatingGroup(n)) and G = AlternatingGroup(n) then
            genLabel := "A_n";
          elif Size(G) = Size(SymmetricGroup(n)) and G = SymmetricGroup(n) then
            genLabel := "S_n";
          else
            genLabel := "other_transitive";
          fi;
        else
          genLabel := "intransitive";
        fi;
        orbLens := SortedList(List(Orbits(G, [1 .. n]), Length));
        key := Concatenation(genLabel, "|order=", String(Size(G)), "|orbits=", String(orbLens));
        RecordHit(dist, key);
        if genLabel = "A_n" or genLabel = "S_n" then
          return rec(found := true, a1 := a1, b1 := b1, gen := genLabel,
                      restarts := restartsUsed, hits := hits, dist := dist, timedOut := false);
        fi;
        ## non-generating (or non-transitive) hit: discard, move to next restart
        break;
      fi;
      i := Random([1 .. k]); j := Random([1 .. k]);
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
    if timedOut then break; fi;
  od;
  return rec(found := false, restarts := restartsUsed, hits := hits, dist := dist,
              timedOut := timedOut);
end;;

MAX_RESTART := 2000;;
MAX_STEP := 20000;;
TIME_CAP_MS := 1200000;;  ## 20 minutes
L25T5_SEED := 20260731;;
Reset(GlobalMersenneTwister, L25T5_SEED);;

Print("\n=== HuntLoop start: n=", N, " k(s)=", bpKList,
      "  restart<=", MAX_RESTART, " step<=", MAX_STEP, " timeCap=", TIME_CAP_MS, "ms ===\n");

## per design, bpKList is expected to be a single value (k=14) but loop generally
## over all budget+parity-feasible k, splitting the time cap evenly.
kResults := [];;
foundRec := fail;;
overallT0 := Runtime();;
perKCap := TIME_CAP_MS;;
if Length(bpKList) > 0 then
  perKCap := Int(TIME_CAP_MS / Length(bpKList));
fi;;

for k in bpKList do
  if foundRec <> fail then break; fi;
  Print("-- k=", k, " (perKCap=", perKCap, "ms) --\n");
  hres := HuntLoop(N, W0, k, MAX_RESTART, MAX_STEP, perKCap);;
  Print("   found=", hres.found, " restarts_used=", hres.restarts, " hits=", hres.hits,
        " timed_out=", hres.timedOut, "\n");
  Print("   dist=", hres.dist, "\n");
  Add(kResults, rec(k := k, res := hres));
  if hres.found then
    foundRec := rec(k := k, a1 := hres.a1, b1 := hres.b1, gen := hres.gen);
  fi;
od;;
totalElapsedMs := Runtime() - overallT0;;

Print("\n=== HuntLoop done. total_elapsed_ms=", totalElapsedMs, "  found=",
      (foundRec <> fail), " ===\n");

#############################################################################
## ---- JSON serialization ----
#############################################################################
DistToJson := function(dist)
  local items, r;
  items := [];
  for r in dist do
    Add(items, Concatenation("{\"key\":", JStr(r.key), ",\"count\":", String(r.count), "}"));
  od;
  return JArr(items);
end;;

KResultsToJson := function(krs)
  local items, kr;
  items := [];
  for kr in krs do
    Add(items, Concatenation(
      "{\"k\":", String(kr.k),
      ",\"found\":", JB(kr.res.found),
      ",\"restarts_used\":", String(kr.res.restarts),
      ",\"hits\":", String(kr.res.hits),
      ",\"timed_out\":", JB(kr.res.timedOut),
      ",\"landing_distribution\":", DistToJson(kr.res.dist),
      "}"));
  od;
  return JArr(items);
end;;

selfSha := ComputeSha256File("search/probe/wac_v1/l25t5_rehunt.g");;

resultBlock := "";;
if foundRec <> fail then
  resultBlock := Concatenation(
    "  \"result\":\"HIT\",\n",
    "  \"witness\":{\n",
    "    \"k\":", String(foundRec.k), ",\n",
    "    \"gen_label\":", JStr(foundRec.gen), ",\n",
    "    \"a1\":", JStr(String(foundRec.a1)), ",\n",
    "    \"b1\":", JStr(String(foundRec.b1)), "\n",
    "  },\n");
else
  resultBlock := "  \"result\":\"UNKNOWN\",\n";
fi;;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"wac_v1-l25t5-rehunt-cert/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/l25t5_rehunt.g\",\n",
  "  \"window_label\":\"L25T5-REHUNT\",\n",
  "  \"f_orientation\":\"n_a\",\n",
  "  \"note\":\"raw measurements only -- interpretation-free. ell=25,t=5,n=30 の狙い撃ち再ハント(生成の穴の最後の1点、裁定254/tmax_budget_and_holes_v1.md §2.3)。厳密計数 search/certs/l25t5_count_20260731.json で T_trans([25,1^5])=378000>0 が確定済み(推移な分解は実在)。旧ハント(tmax_holes_hunt2.g, max_restart=40,max_step=6000)は40 hit全て非推移(軌道[28,1,1]/[29,1])で取りこぼした可能性がある。本 probe は非生成 hit だけでなく非推移 hit・A_n/S_n でない推移 hit も『捨てて続行』し、全ての落ち先(gen_label/群位数/軌道長)を landing_distribution に記録する。期待値/予言はコードに書いていない。result=UNKNOWN は非存在の証明ではない(一級の結果)。\",\n",
  "  \"target\":{\"ell\":", String(ELL), ",\"t\":", String(T), ",\"n\":", String(N), "},\n",
  "  \"budget\":{\n",
  "    \"NC_w0\":", String(NCw0), ",\n",
  "    \"sign_w0\":", String(signW0), ",\n",
  "    \"closed_form_delta_n\":", String(deltaN), ",\n",
  "    \"closed_form_5t\":", String(budgetLHS), ",\n",
  "    \"closed_form_rhs\":", String(budgetRHS), ",\n",
  "    \"closed_form_feasible\":", JB(closedFormFeasible), ",\n",
  "    \"budget_feasible_k\":", JArr(List(budgetKList, String)), ",\n",
  "    \"budget_and_parity_feasible_k\":", JArr(List(bpKList, String)), "\n",
  "  },\n",
  "  \"search_params\":{\n",
  "    \"seed\":", String(L25T5_SEED), ",\n",
  "    \"max_restart\":", String(MAX_RESTART), ",\n",
  "    \"max_step\":", String(MAX_STEP), ",\n",
  "    \"time_cap_ms_total\":", String(TIME_CAP_MS), ",\n",
  "    \"time_cap_ms_per_k\":", String(perKCap), ",\n",
  "    \"total_elapsed_ms\":", String(totalElapsedMs), "\n",
  "  },\n",
  resultBlock,
  "  \"k_results\":", KResultsToJson(kResults), ",\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"gap_invocation\":\"gap -q -o 4g search/probe/wac_v1/l25t5_rehunt.g\"\n",
  "  }\n",
  "}\n");;

outName := "search/certs/l25t5_rehunt_20260731.json";;
WriteFile(outName, cert);;
ValidateJsonFile(outName);;
Print("\nWrote ", outName, " (json.load OK)\n");
Print("\nL25T5_REHUNT_DRIVER_DONE\n");
QUIT;
