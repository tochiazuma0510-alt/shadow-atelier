#############################################################################
## search/probe/wac_v1/lt_count_gen.g
##  l25t5_count.g の一般化(原本 search/probe/wac_v1/l25t5_count.g は残置)。
##  (ell,t) セルのリストを preamble 変数 LT_CELLS から IsBound ガードで
##  受け取り、セルごとに厳密計数(l25t5_count.g のロジック逐語移植: 指標表の
##  class multiplication coefficient による T_all + 巡回の集合分割上の
##  Moebius 反転による T_trans)して JSON 配列に積む。
##
##  preamble 変数(未指定なら既定値):
##    LT_CELLS   -- (ell,t) セルのリスト [[ell1,t1],[ell2,t2],...]
##                  (既定 [[25,5]] -- 既知セル l25t5_count.g と同一)
##    LT_OUTPUT  -- 出力ファイル名(既定 "search/certs/lt_count_gen_<日付>.json")
##
##  較正規律(l25t5_count.g §7 継承): 「同じスクリプトで lambda=(23,1^3)
##  (n=26・既に A_26 の witness あり)を先に流し、T_trans>0 を確認してから
##  本番へ」。一般化版でも較正窓は装置較正であり LT_CELLS の全セルに共通の
##  装置なので、先頭で1回だけ実行する(セルごとに繰り返さない -- 設計注記)。
##  不一致(T_trans<=0)なら Error で fail-closed に停止する(黙って続行しない)。
##
##  期待値・「不在のはず/存在のはず」はコードに書かない -- 較正判定は
##  「計算結果がゼロより大きいか」という原本指定の形以外の閾値を持ち込まない。
##
##  Single lane (GAP 4.16.0). raw measurements only. NOT a ledger claim by
##  itself. No commit / no push (発射は司令塔・mine 経由)。
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");

if not IsBound(LT_CELLS) then
  LT_CELLS := [[25,5]];
fi;
if not IsBound(LT_OUTPUT) then
  LT_OUTPUT := "search/certs/lt_count_gen_20260801.json";
fi;

Read("search/gaplib_common.g");   ## JStr, JB, JoinC, JArr, WriteFile

#############################################################################
## ---- sha256 / JSON 構文検査(l25t5_count.g と同一パターン) ----
#############################################################################
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_lt_count_gen_selfsha.txt";
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
    Error("lt_count_gen.g: ValidateJsonFile: python json.load failed to parse ", path,
          " -- got: ", line);
  fi;
  return true;
end;;

#############################################################################
## ---- T_all / T_trans / |C_Sn(w)| (l25t5_count.g/sat_l1_probe8.g と同一実装の再定義) ----
#############################################################################
TAllCache := NewDictionary([1,1], true);;

TAll := function(lambda)
  local n, tbl, cp, idx, kk, i, j, tot, part, invs, thr, key, v;
  key := SortedList(lambda);
  v := LookupDictionary(TAllCache, key);
  if v <> fail then return v; fi;
  n := Sum(lambda);
  if n = 0 then return 1; fi;
  if n = 1 then AddDictionary(TAllCache, key, 1); return 1; fi;
  tbl := CharacterTable("Symmetric", n);
  cp := ClassParameters(tbl);
  kk := First([1..Length(cp)], z -> SortedList(cp[z][2]) = key);
  if kk = fail then return fail; fi;
  invs := []; thr := [];
  for i in [1..Length(cp)] do
    part := cp[i][2];
    if ForAll(part, e -> e in [1,2]) then Add(invs, i); fi;
    if ForAll(part, e -> e in [1,3]) then Add(thr, i); fi;
  od;
  tot := 0;
  for i in invs do for j in thr do
    tot := tot + ClassMultiplicationCoefficient(tbl, j, i, kk);
  od; od;
  AddDictionary(TAllCache, key, tot);
  return tot;
end;;

## 集合 {1..m} の全分割
SetPartitions := function(m)
  local rec1;
  rec1 := function(i, blocks)
    local res, b, nb, k;
    if i > m then return [ List(blocks, ShallowCopy) ]; fi;
    res := [];
    for k in [1..Length(blocks)] do
      nb := List(blocks, ShallowCopy);
      Add(nb[k], i);
      Append(res, rec1(i+1, nb));
    od;
    nb := List(blocks, ShallowCopy); Add(nb, [i]);
    Append(res, rec1(i+1, nb));
    return res;
  end;
  return rec1(1, []);
end;;

TTransCache := NewDictionary([1,1], true);;
TTransPartitionCount := NewDictionary([1,1], true);;   ## 分解数(算法パラメタ・raw)

TTrans := function(lambda)
  local key, v, m, parts, tot, pi, prod, B, sub, ok;
  key := SortedList(lambda);
  v := LookupDictionary(TTransCache, key);
  if v <> fail then return v; fi;
  m := Length(lambda);
  if m = 1 then
    v := TAll(lambda);            ## 巡回 1 本 ==> 全分解が推移的
    AddDictionary(TTransCache, key, v);
    AddDictionary(TTransPartitionCount, key, 1);
    return v;
  fi;
  parts := SetPartitions(m);
  AddDictionary(TTransPartitionCount, key, Length(parts));
  tot := 0;
  for pi in parts do
    if Length(pi) = 1 then continue; fi;   ## 自明分割 = 求めたい項
    prod := 1;
    for B in pi do
      sub := lambda{B};
      prod := prod * TTrans(sub);
    od;
    tot := tot + prod;
  od;
  v := TAll(lambda) - tot;
  AddDictionary(TTransCache, key, v);
  return v;
end;;

CentSize := function(lambda)
  local mult, s, L, c;
  mult := Collected(SortedList(lambda));
  s := 1;
  for c in mult do s := s * c[1]^c[2] * Factorial(c[2]); od;
  return s;
end;;

#############################################################################
## ---- Report: 1 窓ぶんの計算+記録(JSON 化可能な rec を返す) ----
#############################################################################
Report := function(lambda, label)
  local ta, tt, cw, t0, t1, npart, key;
  t0 := Runtime();
  ta := TAll(lambda);
  tt := TTrans(lambda);
  cw := CentSize(lambda);
  key := SortedList(lambda);
  npart := LookupDictionary(TTransPartitionCount, key);
  if npart = fail then npart := -1; fi;   ## m=1 の場合など未記録なら -1(raw)
  t1 := Runtime();
  Print("  ", label, "\n     w=", lambda, "  n=", Sum(lambda),
        "   |C_Sn(w)|=", cw, "\n     T_all=", ta, "  T_trans=", tt,
        "   T_trans/|C| = ", tt/cw, "   elapsed_ms=", t1-t0,
        "   partitions_of_cycles=", npart, "\n");
  return rec(label := label, lambda := lambda, n := Sum(lambda),
             cent_size := cw, t_all := ta, t_trans := tt,
             partitions_of_cycles := npart, elapsed_ms := t1 - t0);
end;;

RecToJson := function(r)
  return Concatenation(
    "{\"label\":", JStr(r.label),
    ",\"lambda\":", JArr(List(r.lambda, String)),
    ",\"n\":", String(r.n),
    ",\"cent_size\":", String(r.cent_size),
    ",\"t_all\":", String(r.t_all),
    ",\"t_trans\":", String(r.t_trans),
    ",\"partitions_of_cycles\":", String(r.partitions_of_cycles),
    ",\"elapsed_ms\":", String(r.elapsed_ms),
    "}");
end;;

#############################################################################
## ---- lambda ビルダー: (ell,t) セル -> [ell, 1, 1, ..., 1](t 個の 1) ----
#############################################################################
CellToLambda := function(cell)
  local ell, t, lam, i;
  ell := cell[1]; t := cell[2];
  lam := [ell];
  for i in [1 .. t] do Add(lam, 1); od;
  return lam;
end;;

CellLabel := function(cell)
  return Concatenation("ell=", String(cell[1]), ",t=", String(cell[2]),
    " (n=", String(cell[1]+cell[2]), ")");
end;;

#############################################################################
## ---- 較正(§7 継承): (23,1^3) n=26, A_26 witness 既知。全セル共通の装置較正 ----
##      なので LT_CELLS の内容に関わらず先頭で 1 回だけ実行する。
#############################################################################
Print("=== 較正: (23,1^3) n=26(既に A_26 witness あり)-- 装置較正・1回のみ ===\n");
CalibStart := Runtime();;
CalibResult := Report([23,1,1,1], "ell=23,t=3 (n=26): A_26 witness 既知(裁定254/tmax_holes_hunt.g)");;
CalibElapsedMs := Runtime() - CalibStart;;

CalibPass := CalibResult.t_trans > 0;;
Print("較正判定(T_trans>0か): ", CalibPass, "\n");

if not CalibPass then
  Error("lt_count_gen.g: 較正 FAIL: T_trans((23,1^3))<=0 -- 既知の A_26 witness と矛盾するので",
        " 機構そのものに欠陥がある。全セルの計算を fail-closed で打ち切る。");
fi;

#############################################################################
## ---- 本番: LT_CELLS の各セルを計算 ----
#############################################################################
Print("\n=== 本番: LT_CELLS = ", LT_CELLS, " ===\n");
CellResultsStart := Runtime();;
CellResults := [];;
for cell in LT_CELLS do
  Add(CellResults, Report(CellToLambda(cell), CellLabel(cell)));
od;;
CellResultsElapsedMs := Runtime() - CellResultsStart;;

#############################################################################
## ---- JSON 出力 ----
#############################################################################
selfSha := ComputeSha256File("search/probe/wac_v1/lt_count_gen.g");;
outName := LT_OUTPUT;;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"wac_v1-lt-count-gen-cert/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/lt_count_gen.g\",\n",
  "  \"window_label\":\"LT-COUNT-GEN\",\n",
  "  \"spec_ref\":\"docs/notes/pent_exists_level_v1.md #7 (裁定_255_PENT委嘱3検収.md 項目7で受理) の一般化(mine driver 一般化・裁定330注記に基づく)\",\n",
  "  \"note\":\"raw measurements only -- interpretation-free. T_all/T_trans は指標表の class multiplication coefficient と巡回集合分割上の Moebius 反転による厳密計数(l25t5_count.g/sat_l1_probe8.g と同一機構)。較正規律: 既知 (23,1^3)(n=26, A_26 witness既知) を LT_CELLS の内容に関わらず先頭で1回だけ流し T_trans>0 を確認してから LT_CELLS の各セルへ進む(全セル共通の装置較正・セルごとに繰り返さない)。不一致なら Error で fail-closed に停止する。期待値/予言はコードに書いていない -- 較正の可否は計算結果とゼロとの比較のみで判定する。partitions_of_cycles は Bell数(算法パラメタ)であり計数結果の予言ではない。\",\n",
  "  \"calibration\":{\n",
  "    \"target\":\"(23,1^3) n=26\",\n",
  "    \"elapsed_ms\":", String(CalibElapsedMs), ",\n",
  "    \"result\":", RecToJson(CalibResult), ",\n",
  "    \"pass_t_trans_gt_0\":", JB(CalibPass), "\n",
  "  },\n",
  "  \"cells\":{\n",
  "    \"requested\":", JArr(List(LT_CELLS, c -> Concatenation("[", String(c[1]), ",", String(c[2]), "]"))), ",\n",
  "    \"elapsed_ms\":", String(CellResultsElapsedMs), ",\n",
  "    \"results\":", JArr(List(CellResults, RecToJson)), "\n",
  "  },\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"gap_invocation\":\"gap -q -o 12g search/probe/wac_v1/lt_count_gen.g (preamble: LT_CELLS := [[ell1,t1],...];; LT_OUTPUT := \\\"...\\\";;)\"\n",
  "  }\n",
  "}\n");;

WriteFile(outName, cert);;
ValidateJsonFile(outName);;
Print("\nWrote ", outName, " (json.load OK)\n");
Print("\nLT_COUNT_GEN_DRIVER_DONE\n");
QUIT;
