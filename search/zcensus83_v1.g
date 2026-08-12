# search/zcensus83_v1.g -- Z-CENSUS-83 + SPLIT-6E classification + calibration gate (裁定960)
# 仕様 = docs/notes/ideas_chidoor_83win_v1.md 札1(SPLIT-6E)・札2(Z-CENSUS-83)
#
# 実行: .\gap.ps1 search\zcensus83_v1.g
#
# 【1】SPLIT-6E: 83窓(+M5)を e 値で三分(A:e=6 / B:6|e,e!=6 / C:6∤e)
# 【2】較正ゲート: c∈N側57件(window∧c∈N)で「e|6」を全数検査(1件でも外れれば即報告)
# 【3】Z-CENSUS-83: 各窓で z=ord(c mod N)(c=(sigma1 sigma2)^3、NAME-COLLIDE注記どおり B3 中心生成元)
#      + ab下界 z_ab=e/gcd(e,6) + 比 delta=z/z_ab
#
# データ入力: search/zcensus83_data.g(search/certs/lins_census_2000_v1_20260811.json から
#   Python で再構成した TARGET83/CONTROL57 の canonical_id_words -- 847監査: 既存の committed cert
#   の生データを読むだけで新規 census/lins 呼び出しはしない)。M5 は別途 week3-M5-explorer.g の
#   BuildQTGeneral 機構(既存・847監査済み)を独立に再実行して z を得る(このスクリプトは
#   week3-M5-explorer.g を Read() せず、e=10(search/certs/m5_win_chk_v1_20260811.json で既測)・
#   z=5(このセッションで week3-M5-explorer.g を独立に再実行し Order(qt.cc)=5 を確認済み)を
#   別経路の生値として直接記録する -- 新規測定はしない)。
#
# u・封印非接触。判定語なし(生値のみ)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/zcensus83_data.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

Print("############################################################\n");
Print("# zcensus83_v1.g -- SPLIT-6E + calibration + Z-CENSUS-83(裁定960)\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;
failures := 0;;

Print("TARGET83 count = ", Length(TARGET83), " (期待 83)\n");
Print("CONTROL57 count = ", Length(CONTROL57), " (期待 57)\n");
if Length(TARGET83) <> 83 then failures := failures + 1; fi;
if Length(CONTROL57) <> 57 then failures := failures + 1; fi;

# ====================================================================
# B3 = <a,b | aba=bab> の構成、c := (a*b)^3(NAME-COLLIDE注記の中心生成元)
# ====================================================================
BF3 := FreeGroup("a", "b");;
brel := BF3.1*BF3.2*BF3.1*BF3.2^-1*BF3.1^-1*BF3.2^-1;;   # a*b*a*(b*a*b)^-1 = 1
B3 := BF3 / [brel];;
a := B3.1;;  b := B3.2;;   # global bind for EvalString(word) below
cElt := (a*b)^3;;

Print("|<a,b|aba=bab>| construction OK, c=(a*b)^3 defined\n");

# ====================================================================
# 部分群 N の再構成 + z=ord(c mod N) の測定(member 1 件あたり)
# ====================================================================
MeasureMember := function(m)
  local genElts, w, N, idxOk, isNormal, hom, cImg, z, Gid, Gab, eVal;
  genElts := List(m.words, w -> EvalString(w));;
  N := Subgroup(B3, genElts);;
  idxOk := (Index(B3, N) = m.index);;
  isNormal := IsNormal(B3, N);;
  z := fail;;
  if isNormal and idxOk then
    hom := NaturalHomomorphismByNormalSubgroup(B3, N);;
    cImg := Image(hom, cElt);;
    z := Order(cImg);;
  fi;
  Gid := SmallGroup(m.id[1], m.id[2]);;
  Gab := Gid / DerivedSubgroup(Gid);;
  eVal := Size(Gab);;
  return rec(index:=m.index, id:=m.id, e:=eVal, idx_ok:=idxOk, is_normal:=isNormal, z:=z);
end;;

Print("\n============================================================\n");
Print("# TARGET83 の測定\n");
Print("============================================================\n");
target83Results := [];;
cnt := 0;;
for m in TARGET83 do
  cnt := cnt + 1;;
  r := MeasureMember(m);;
  Add(target83Results, r);;
  if not (r.idx_ok and r.is_normal) then
    Print("[ANOMALY] index=", r.index, " id=", r.id, " idx_ok=", r.idx_ok, " is_normal=", r.is_normal, "\n");
    failures := failures + 1;
  fi;
  if cnt mod 20 = 0 then Print("  ...", cnt, "/", Length(TARGET83), " done\n"); fi;
od;;
Print("TARGET83 測定完了: ", Length(target83Results), " 件\n");

Print("\n============================================================\n");
Print("# CONTROL57(c∈N)の測定 + 較正ゲート(e|6 の全数検査)\n");
Print("============================================================\n");
control57Results := [];;
calibFailCount := 0;;
cnt := 0;;
for m in CONTROL57 do
  cnt := cnt + 1;;
  r := MeasureMember(m);;
  Add(control57Results, r);;
  eDiv6 := (6 mod r.e = 0);;
  r.e_divides_6 := eDiv6;;
  if not eDiv6 then
    calibFailCount := calibFailCount + 1;;
    Print("[CALIBRATION-FAIL] index=", r.index, " id=", r.id, " e=", r.e, " (e does NOT divide 6)\n");
  fi;
  if cnt mod 20 = 0 then Print("  ...", cnt, "/", Length(CONTROL57), " done\n"); fi;
od;;
Print("CONTROL57 測定完了: ", Length(control57Results), " 件\n");
Print("較正ゲート: e|6 違反件数 = ", calibFailCount, " / ", Length(control57Results), "\n");
calibPass := (calibFailCount = 0);;
Print("[", PF(calibPass), "] 較正ゲート(c∈N ⟹ e|6): ", calibPass, "\n");
if not calibPass then failures := failures + 1; fi;

# ====================================================================
# M5(既存の別経路測定を直接記録・新規測定なし)
# ====================================================================
m5E := 10;;    # search/certs/m5_win_chk_v1_20260811.json (e_abelianization_order)
m5Z := 5;;     # このセッションで week3-M5-explorer.g を独立再実行し Order(qt.cc)=5 を確認済み

# ====================================================================
# 【1】SPLIT-6E 分類(TARGET83 + M5)
# ====================================================================
Print("\n============================================================\n");
Print("# SPLIT-6E 分類\n");
Print("============================================================\n");

ClassifyType := function(eVal)
  if eVal = 6 then return "A"; fi;
  if eVal mod 6 = 0 then return "B"; fi;   # 6|e (e は 6 の倍数), e<>6 (since eVal<>6 already excluded)
  return "C";;
end;;
# 自己訂正(初稿バグ): 「6 mod eVal = 0」(=e|6、e が 6 の約数)と「eVal mod 6 = 0」(=6|e、e が
# 6 の倍数)を取り違えていた。SPLIT-6E の B 型定義(docs/notes/ideas_chidoor_83win_v1.md 札1)は
# 「6|e・e>=12」= e が 6 の倍数、なので正しくは eVal mod 6 = 0。較正ゲート(c∈N ⟹ e|6)側の
# 「6 mod r.e = 0」はそのまま正しい(e が 6 の約数、という別の主張)。

typeCounts := rec(A:=0, B:=0, C:=0);;
for r in target83Results do
  ty := ClassifyType(r.e);;
  r.split6e_type := ty;;
  if ty = "A" then typeCounts.A := typeCounts.A + 1;
  elif ty = "B" then typeCounts.B := typeCounts.B + 1;
  else typeCounts.C := typeCounts.C + 1; fi;
od;;
m5Type := ClassifyType(m5E);;
Print("A型(e=6): ", typeCounts.A, " 件(札の予測 15)\n");
Print("B型(6|e,e<>6): ", typeCounts.B, " 件(札の予測 66)\n");
Print("C型(6∤e): ", typeCounts.C, " 件(TARGET83内)+ M5(型=", m5Type, ")\n");
Print("合計 = ", typeCounts.A+typeCounts.B+typeCounts.C, " (期待 83)\n");
splitTotalOk := (typeCounts.A+typeCounts.B+typeCounts.C = 83);;
if not splitTotalOk then failures := failures + 1; fi;

# ====================================================================
# 【3】Z-CENSUS-83: z_ab, delta の計算
# ====================================================================
Print("\n============================================================\n");
Print("# Z-CENSUS-83: z, z_ab, delta\n");
Print("============================================================\n");

ComputeZab := function(eVal) return eVal / Gcd(eVal, 6); end;;

zDeltaAnomaly := 0;;
for r in target83Results do
  r.z_ab := ComputeZab(r.e);;
  if r.z <> fail then
    r.delta := r.z / r.z_ab;;
    if not IsInt(r.delta) then
      Print("[ANOMALY] index=", r.index, " id=", r.id, ": delta=z/z_ab=", r.z, "/", r.z_ab, " is not an integer\n");
      zDeltaAnomaly := zDeltaAnomaly + 1;;
      failures := failures + 1;
    fi;
  else
    r.delta := fail;;
  fi;
od;;
m5Zab := ComputeZab(m5E);;
m5Delta := m5Z / m5Zab;;
Print("M5: e=", m5E, " z=", m5Z, " z_ab=", m5Zab, " delta=", m5Delta, "\n");

zValues := List(Filtered(target83Results, r -> r.z <> fail), r -> r.z);;
Print("z 値の分布(TARGET83、z 取得成功 ", Length(zValues), "/", Length(target83Results), " 件): ",
      Collected(zValues), "\n");
deltaValues := List(Filtered(target83Results, r -> r.delta <> fail), r -> r.delta);;
Print("delta 値の分布: ", Collected(deltaValues), "\n");

# ====================================================================
# 総括
# ====================================================================
Print("\n############################################################\n");
if failures = 0 then
  Print("ZCENSUS83 ALL PASSED\n");
else
  Print("ZCENSUS83 FAILURES: ", failures, "\n");
fi;

t1 := GAPLIB_WallElapsedMs();;
Print("経過(壁時計) = ", (t1-t0)/1000.0, " s\n");

# ====================================================================
# 証明書 JSON
# ====================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_zc83.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

ValOrNull := function(v)
  if v = fail then return "null"; fi;
  return String(v);
end;;

Target83Json := function(lst)
  local parts, r;
  parts := [];
  for r in lst do
    Add(parts, Concatenation(
      "{\"index\":", String(r.index), ",\"id_group\":", JPair(r.id[1],r.id[2]),
      ",\"e\":", String(r.e), ",\"split6e_type\":\"", r.split6e_type, "\"",
      ",\"idx_ok\":", JB(r.idx_ok), ",\"is_normal\":", JB(r.is_normal),
      ",\"z\":", ValOrNull(r.z), ",\"z_ab\":", String(r.z_ab), ",\"delta\":", ValOrNull(r.delta),
      "}"));
  od;
  return JArr(parts);
end;;

Control57Json := function(lst)
  local parts, r;
  parts := [];
  for r in lst do
    Add(parts, Concatenation(
      "{\"index\":", String(r.index), ",\"id_group\":", JPair(r.id[1],r.id[2]),
      ",\"e\":", String(r.e), ",\"e_divides_6\":", JB(r.e_divides_6),
      ",\"idx_ok\":", JB(r.idx_ok), ",\"is_normal\":", JB(r.is_normal),
      ",\"z\":", ValOrNull(r.z),
      "}"));
  od;
  return JArr(parts);
end;;

scriptSha256 := ComputeSha256File("search/zcensus83_v1.g");;

cert := Concatenation(
  "{\"schema\":\"chidoor-split6e-z/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/zcensus83_v1.g\",\"order\":\"裁定960 / docs/notes/ideas_chidoor_83win_v1.md 札1・札2\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"data_source\":{\"census\":\"search/certs/lins_census_2000_v1_20260811.json\",",
    "\"band\":[1000,2000],\"extraction_script\":\"search/extract_zcensus83.py (committed -- 847 note: reads existing committed cert only, produces search/zcensus83_data.g)\"}",
  ",\"target83_count\":", String(Length(TARGET83)),
  ",\"control57_count\":", String(Length(CONTROL57)),
  ",\"split6e_classification\":{\"A_e_eq_6\":", String(typeCounts.A),
    ",\"B_6_divides_e_ne6\":", String(typeCounts.B),
    ",\"C_6_notdivides_e\":", String(typeCounts.C),
    ",\"札の予測\":{\"A\":15,\"B\":66,\"C_残\":2},",
    "\"total\":", String(typeCounts.A+typeCounts.B+typeCounts.C), "}",
  ",\"calibration_gate\":{\"claim\":\"c in N (control57) => e|6\",",
    "\"fail_count\":", String(calibFailCount), ",\"total\":", String(Length(control57Results)),
    ",\"pass\":", JB(calibPass), "}",
  ",\"target83_detail\":", Target83Json(target83Results),
  ",\"control57_detail\":", Control57Json(control57Results),
  ",\"m5\":{\"e\":", String(m5E), ",\"z\":", String(m5Z), ",\"z_ab\":", String(m5Zab),
    ",\"delta\":", String(m5Delta), ",\"split6e_type\":\"", m5Type, "\",",
    "\"source_note\":\"e from search/certs/m5_win_chk_v1_20260811.json; z from independent re-run of search/week3-M5-explorer.g's BuildQTGeneral (Order(qt.cc)) this session, not a new measurement method\"}",
  ",\"z_value_distribution_target83\":\"", ReplacedString(String(Collected(zValues)), "\n", " "), "\"",
  ",\"delta_value_distribution_target83\":\"", ReplacedString(String(Collected(deltaValues)), "\n", " "), "\"",
  ",\"u_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"overall_failures\":", String(failures),
  ",\"elapsed_wall_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/zcensus83_v2_20260812.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");

Print("\nZCENSUS83 DONE\n");
QUIT;
