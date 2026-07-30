#############################################################################
## search/probe/wac_v1/l25t5_count.g
##  T_trans([25,1^5]) (n=30) の厳密計数 -- 発注仕様は
##  docs/notes/pent_exists_level_v1.md §7「付録 -- ell=25,t=5 の T_trans
##  計数の発注仕様」(裁定_255_PENT委嘱3検収.md 項目7で受理)。機構は
##  search/probe/wac_v1/sat_l1_probe8.g と同一(指標表 class multiplication
##  coefficient による T_all + 巡回の集合分割上の Moebius 反転による T_trans)。
##  ここでは同じ関数を自己完結的に再定義する(探索器内の使い回しであり、
##  探索器/照合器分離の対象外 -- 両方とも探索側)。
##
##  較正規律(§7 末尾): 「同じスクリプトで lambda=(23,1^3)(n=26・既に A_26 の
##  witness あり)を先に流し、T_trans>0 を確認してから本番へ」を厳守する。
##  期待値・「不在のはず/存在のはず」はコードに書かない -- 較正判定は
##  「計算結果がゼロより大きいか」という §7 指定の形以外の閾値を持ち込まない。
##
##  ピーク 8-16GB 見込み(S_30 の指標表 5604 類)につき CI 専。ローカルでは
##  preamble で L25T5_SMOKE_ONLY:=true;; を渡し、フェーズ1(既知の軽量窓の
##  再現)だけを実行する smoke に留める(重い較正/本番フェーズはスキップ)。
##  例: gap -c 'L25T5_SMOKE_ONLY:=true;;' search/probe/wac_v1/l25t5_count.g
##
##  Single lane (GAP 4.16.0). raw measurements only. NOT a ledger claim by
##  itself. No commit / no push (発射は司令塔・mine 経由)。
#############################################################################

if not IsBound(L25T5_SMOKE_ONLY) then
  L25T5_SMOKE_ONLY := false;
fi;

Read("search/gaplib_common.g");   ## JStr, JB, JoinC, JArr, WriteFile

#############################################################################
## ---- sha256 / JSON 構文検査(tmax_scan.g と同一パターン) ----
#############################################################################
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_l25t5_cert_selfsha.txt";
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
    Error("l25t5_count.g: ValidateJsonFile: python json.load failed to parse ", path,
          " -- got: ", line);
  fi;
  return true;
end;;

#############################################################################
## ---- T_all / T_trans / |C_Sn(w)| (sat_l1_probe8.g と同一実装の再定義) ----
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
## ---- フェーズ1: smoke(既知の軽量窓・sat_l1_probe8.g §較正 と同一窓) ----
##      ローカルでも(8GB でも)秒〜分オーダーで完走する軽量チェック。
#############################################################################
SmokeStart := Runtime();;
Print("=== フェーズ1: smoke(既知の軽量窓の再現・機構の疎通確認)===\n");
SmokeResults := [];;
Add(SmokeResults, Report([9,1],      "n=10 梯子(sat_l1_probe8.g 較正窓)"));
Add(SmokeResults, Report([9,2],      "n=11 梯子(同上)"));
Add(SmokeResults, Report([9,2,1],    "n=12 梯子(同上)"));
Add(SmokeResults, Report([9,2,2],    "n=13 梯子(同上)"));
Add(SmokeResults, Report([11,2,2,1], "n=16 D族(同上)"));
SmokeElapsedMs := Runtime() - SmokeStart;;
Print("L25T5_SMOKE_DONE elapsed_ms=", SmokeElapsedMs, "\n");

if L25T5_SMOKE_ONLY then
  Print("\n[L25T5_SMOKE_ONLY=true につきフェーズ2/3(較正本番・本番)はスキップ]\n");
fi;

## 注意(GAP 罠): QUIT は if-then-fi の内側では使えない("cannot be used in
## this context")。分岐は if not L25T5_SMOKE_ONLY then <本体> fi; で包み、
## QUIT はファイル末尾の最上位でのみ呼ぶ。
if not L25T5_SMOKE_ONLY then

#############################################################################
## ---- フェーズ2: 較正本番 -- (23,1^3) n=26, A_26 witness 既知 (§7 末尾規律) ----
#############################################################################
Print("\n=== フェーズ2: 較正本番 (23,1^3) n=26(既に A_26 witness あり)===\n");
CalibStart := Runtime();;
CalibResult := Report([23,1,1,1], "ell=23,t=3 (n=26): A_26 witness 既知(裁定254/tmax_holes_hunt.g)");;
CalibElapsedMs := Runtime() - CalibStart;;

## §7 規律: 「T_trans>0 を確認してから本番へ」-- ここでの判定はゼロとの比較の
## みであり、大きさの予測値は一切持ち込まない(接触遮断)。
CalibPass := CalibResult.t_trans > 0;;
Print("較正判定(T_trans>0か): ", CalibPass, "\n");

if not CalibPass then
  Print("\n[較正 FAIL: T_trans((23,1^3))<=0 -- 既知の A_26 witness と矛盾するので\n");
  Print(" 機構そのものに欠陥がある。本番 (25,1^5) は走らせず fail-closed で打ち切る]\n");
fi;

#############################################################################
## ---- フェーズ3: 本番 -- (25,1^5) n=30(UNKNOWN・裁定254 §2.3) ----
#############################################################################
MainResult := fail;;
MainElapsedMs := 0;;
if CalibPass then
  Print("\n=== フェーズ3: 本番 (25,1^5) n=30(UNKNOWN)===\n");
  MainStart := Runtime();;
  MainResult := Report([25,1,1,1,1,1], "ell=25,t=5 (n=30): UNKNOWN(裁定254 §2.3・tmax_budget_and_holes_v1.md)");;
  MainElapsedMs := Runtime() - MainStart;;
fi;

#############################################################################
## ---- JSON 出力 ----
#############################################################################
selfSha := ComputeSha256File("search/probe/wac_v1/l25t5_count.g");;
outName := "search/certs/l25t5_count_20260731.json";;

MainJsonField := "null";;
if MainResult <> fail then
  MainJsonField := RecToJson(MainResult);
fi;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"wac_v1-l25t5-count-cert/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/l25t5_count.g\",\n",
  "  \"window_label\":\"L25T5-COUNT\",\n",
  "  \"spec_ref\":\"docs/notes/pent_exists_level_v1.md #7 (裁定_255_PENT委嘱3検収.md 項目7で受理)\",\n",
  "  \"note\":\"raw measurements only -- interpretation-free. T_all/T_trans は指標表の class multiplication coefficient と巡回集合分割上の Moebius 反転による厳密計数(sat_l1_probe8.g と同一機構)。較正規律(#7末尾): 既知 (23,1^3)(n=26, A_26 witness既知) を先に流し T_trans>0 を確認してから本番 (25,1^5)(n=30) へ進む。期待値/予言はコードに書いていない -- 較正の可否は計算結果とゼロとの比較のみで判定する。partitions_of_cycles は Bell数(算法パラメタ、6巡回なら Bell(6)=203)であり計数結果の予言ではない。\",\n",
  "  \"mode\":\"full\",\n",
  "  \"smoke\":{\n",
  "    \"elapsed_ms\":", String(SmokeElapsedMs), ",\n",
  "    \"results\":", JArr(List(SmokeResults, RecToJson)), "\n",
  "  },\n",
  "  \"calibration\":{\n",
  "    \"target\":\"(23,1^3) n=26\",\n",
  "    \"elapsed_ms\":", String(CalibElapsedMs), ",\n",
  "    \"result\":", RecToJson(CalibResult), ",\n",
  "    \"pass_t_trans_gt_0\":", JB(CalibPass), "\n",
  "  },\n",
  "  \"main\":{\n",
  "    \"target\":\"(25,1^5) n=30\",\n",
  "    \"attempted\":", JB(CalibPass), ",\n",
  "    \"elapsed_ms\":", String(MainElapsedMs), ",\n",
  "    \"result\":", MainJsonField, "\n",
  "  },\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"gap_invocation\":\"gap -q -o 12g search/probe/wac_v1/l25t5_count.g (preamble 既定 = full mode; L25T5_SMOKE_ONLY:=true;; でローカル smoke のみ)\"\n",
  "  }\n",
  "}\n");;

WriteFile(outName, cert);;
ValidateJsonFile(outName);;
Print("\nWrote ", outName, " (json.load OK)\n");

fi;   ## not L25T5_SMOKE_ONLY

if L25T5_SMOKE_ONLY then
  Print("\nL25T5_COUNT_DRIVER_DONE (smoke-only mode -- no cert written)\n");
else
  Print("\nL25T5_COUNT_DRIVER_DONE\n");
fi;
QUIT;
