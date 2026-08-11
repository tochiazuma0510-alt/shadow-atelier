## search/wincnotn_j_v1.g -- WIN-CNOTN-J (裁定828). For each of the 83 window-AND-c-notin-N
## members recorded in search/certs/wincnotn_v1_20260812.json's win_cnotn_target_members
## (裁定823③), report e=|G^ab| and j=e/2 raw, plus a machine flag j_notin_{1,3} (j not in {1,3},
## i.e. j does not divide 3). Per AB-2J (N<=PB3 ==> e even), all 83 members are window (in_PB3
## =true per WIN-CNOTN's own classification), so e SHOULD be even -- an odd e would itself be an
## ANOMALY, reported raw (not silently treated as impossible). No prediction is frozen here (裁
## 定828's own instruction: "予言は凍結しない・在庫の記述統計").
## Provenance: id_group list read directly from search/certs/wincnotn_v1_20260812.json's own
## win_cnotn_target_members field (that cert's own provenance chain -- census/lins output --
## already established elsewhere; SmallGroup(id_group) reconstructs the isomorphism type by
## definition of IdGroup, same convention as search/pchi1_v2.g).
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

## ============ 83 (index,id_group) entries (verbatim from wincnotn_v1_20260812.json) ============
MEMBERS := [
  rec(index:=1026, id:=[1026,23]), rec(index:=1026, id:=[1026,23]),
  rec(index:=1008, id:=[1008,116]), rec(index:=1008, id:=[1008,116]),
  rec(index:=1008, id:=[1008,523]), rec(index:=1008, id:=[1008,523]),
  rec(index:=1008, id:=[1008,521]), rec(index:=1008, id:=[1008,521]),
  rec(index:=1008, id:=[1008,684]), rec(index:=1008, id:=[1008,684]),
  rec(index:=1008, id:=[1008,683]), rec(index:=1008, id:=[1008,683]),
  rec(index:=1116, id:=[1116,18]), rec(index:=1116, id:=[1116,18]),
  rec(index:=1134, id:=[1134,46]), rec(index:=1134, id:=[1134,46]),
  rec(index:=1134, id:=[1134,56]), rec(index:=1134, id:=[1134,56]),
  rec(index:=1134, id:=[1134,55]), rec(index:=1134, id:=[1134,55]),
  rec(index:=1134, id:=[1134,53]), rec(index:=1134, id:=[1134,53]),
  rec(index:=1152, id:=[1152,154161]), rec(index:=1152, id:=[1152,154163]), rec(index:=1152, id:=[1152,154163]),
  rec(index:=1170, id:=[1170,17]), rec(index:=1170, id:=[1170,17]),
  rec(index:=1260, id:=[1260,45]), rec(index:=1260, id:=[1260,45]),
  rec(index:=1332, id:=[1332,23]), rec(index:=1332, id:=[1332,23]),
  rec(index:=1368, id:=[1368,46]), rec(index:=1368, id:=[1368,46]),
  rec(index:=1386, id:=[1386,18]), rec(index:=1386, id:=[1386,18]),
  rec(index:=1404, id:=[1404,33]), rec(index:=1404, id:=[1404,33]),
  rec(index:=1404, id:=[1404,34]), rec(index:=1404, id:=[1404,34]),
  rec(index:=1458, id:=[1458,651]), rec(index:=1458, id:=[1458,651]),
  rec(index:=1512, id:=[1512,547]), rec(index:=1512, id:=[1512,547]),
  rec(index:=1512, id:=[1512,56]), rec(index:=1512, id:=[1512,56]),
  rec(index:=1512, id:=[1512,450]), rec(index:=1512, id:=[1512,450]),
  rec(index:=1512, id:=[1512,57]), rec(index:=1512, id:=[1512,57]),
  rec(index:=1548, id:=[1548,18]), rec(index:=1548, id:=[1548,18]),
  rec(index:=1638, id:=[1638,42]), rec(index:=1638, id:=[1638,42]),
  rec(index:=1638, id:=[1638,51]), rec(index:=1638, id:=[1638,51]),
  rec(index:=1674, id:=[1674,21]), rec(index:=1674, id:=[1674,21]),
  rec(index:=1710, id:=[1710,21]), rec(index:=1710, id:=[1710,21]),
  rec(index:=1728, id:=[1728,31095]), rec(index:=1728, id:=[1728,31095]),
  rec(index:=1764, id:=[1764,112]), rec(index:=1764, id:=[1764,112]),
  rec(index:=1764, id:=[1764,18]), rec(index:=1764, id:=[1764,18]),
  rec(index:=1872, id:=[1872,119]), rec(index:=1872, id:=[1872,119]),
  rec(index:=1872, id:=[1872,570]), rec(index:=1872, id:=[1872,570]),
  rec(index:=1872, id:=[1872,568]), rec(index:=1872, id:=[1872,568]),
  rec(index:=1872, id:=[1872,781]), rec(index:=1872, id:=[1872,781]),
  rec(index:=1872, id:=[1872,780]), rec(index:=1872, id:=[1872,780]),
  rec(index:=1890, id:=[1890,39]), rec(index:=1890, id:=[1890,39]),
  rec(index:=1890, id:=[1890,40]), rec(index:=1890, id:=[1890,40]),
  rec(index:=1944, id:=[1944,48]), rec(index:=1944, id:=[1944,48]),
  rec(index:=1998, id:=[1998,23]), rec(index:=1998, id:=[1998,23]),
];;

Print("Total members to measure: ", Length(MEMBERS), "\n");

results := [];;
oddECount := 0;;
jNotin13Count := 0;;
for m in MEMBERS do
  G := SmallGroup(m.id[1], m.id[2]);;
  Gab := G / DerivedSubgroup(G);;
  eVal := Size(Gab);;
  eIsCyclic := IsCyclic(Gab);;
  eEven := (eVal mod 2 = 0);;
  jVal := fail;;
  jNotin13 := fail;;
  if eEven then
    jVal := eVal / 2;
    jNotin13 := not (jVal = 1 or jVal = 3);
    if jNotin13 then jNotin13Count := jNotin13Count + 1; fi;
  else
    oddECount := oddECount + 1;
  fi;
  Add(results, rec(index:=m.index, id:=m.id, e:=eVal, e_is_cyclic:=eIsCyclic, e_even:=eEven,
                    j:=jVal, j_notin_1_3:=jNotin13));
  Print("index=", m.index, " id=", m.id, " e=", eVal, " cyclic=", eIsCyclic, " even=", eEven,
        " j=", jVal, " j_notin_{1,3}=", jNotin13, "\n");
od;

Print("odd_e_count(ANOMALY if >0)=", oddECount, " j_notin_1_3_count=", jNotin13Count, "\n");

## ============ JSON output ============
JResult := function(r)
  local jStr, jFlagStr;
  if r.j = fail then jStr := "null"; else jStr := String(r.j); fi;
  if r.j_notin_1_3 = fail then jFlagStr := "null"; else jFlagStr := JB(r.j_notin_1_3); fi;
  return Concatenation("{",
    "\"index\":", String(r.index), ",",
    "\"id_group\":", JPair(r.id[1], r.id[2]), ",",
    "\"e\":", String(r.e), ",",
    "\"e_is_cyclic\":", JB(r.e_is_cyclic), ",",
    "\"e_even\":", JB(r.e_even), ",",
    "\"j\":", jStr, ",",
    "\"j_notin_1_3\":", jFlagStr,
    "}");
end;;

out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/wincnotn_j_v1\",",
  "\"authority\":\"", "\\u88c1\\u5b9a828 -- WIN-CNOTN-J (search/certs/wincnotn_v1_20260812.json \\u306e83\\u4ef6\\u306e e,j \\u5024\\u30ec\\u30dd\\u30fc\\u30c8)\",",
  "\"provenance_note\":\"index/id_group list read directly from search/certs/wincnotn_v1_20260812.json's win_cnotn_target_members field. SmallGroup(id_group) reconstructs the isomorphism type by definition of IdGroup (same convention as search/pchi1_v2.g). NO new census/lins run.\",",
  "\"predicate_note\":\"NO prediction frozen (裁定828: descriptive inventory only, no verdict). AB-2J (N<=PB3 => e even) predicts e should be even for all 83 members (all are in_PB3=true per WIN-CNOTN's own classification) -- an odd e would be an ANOMALY, reported raw (odd_e_count field), not silently treated as impossible.\",",
  "\"total_members\":", String(Length(results)), ",",
  "\"results\":[", JoinC(List(results, JResult), ","), "],",
  "\"odd_e_count\":", String(oddECount), ",",
  "\"j_notin_1_3_count\":", String(jNotin13Count), ",",
  "\"no_verdict_note\":\"raw e/j values and booleans only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002\"",
  "}"
);;

WriteFile("search/certs/wincnotn_j_v1_20260812.json", out);;
Print("Wrote search/certs/wincnotn_j_v1_20260812.json\n");
Print("WINCNOTN_J_DONE\n");
QUIT;
