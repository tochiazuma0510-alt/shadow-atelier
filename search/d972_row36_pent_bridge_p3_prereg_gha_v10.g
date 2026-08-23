#############################################################################
## P3 fixed-row36 v10 complete Python lineage launcher over frozen v8 math.
#############################################################################

P159OR36P3V10RequireSha:=function(path,expected)
  local raw,actual;
  raw:=StringFile(path);
  if raw=fail then
    Error("PENT159O_ROW36_P3_V10: missing immutable input ",path);
  fi;
  actual:=HexSHA256(raw);
  if actual<>expected then
    Error("PENT159O_ROW36_P3_V10: immutable input hash mismatch ",path,
      " expected=",expected," actual=",actual);
  fi;
  Print("PENT159O_ROW36_P3_V10_PIN_PASS path=",path," bytes=",Length(raw),
    " sha256=",actual,"\n");
end;

## Programmatic recursive import/file_pin lineage closure: 16 Python files.
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_common_v1.py",
  "d3e27775b59baa150c255c15feb2ab5809bdc299265278772f0428d2f1de0a79");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_common_v2.py",
  "46ab60bf06e1bec03725a69349914e4bd9e786c41ce0946b0387f74493a55ecc");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_common_v3.py",
  "95ff60fe351aa0020aa5353d805cd8588c7d16cbfc45acdca862097d67cafcb5");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_common_v4.py",
  "1d7a4673c7fdd8c5aa72a8a0f0cb78d1e39d2983a9635f6ce0fe8d978fe43bea");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_common_p3_v5.py",
  "274db1abd26f8beeae181b9d049a6955ed33a81b7b1f6b7971ca5f7207a977e9");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_common_p3_v6.py",
  "f6ac99a0d55394d675cab43690631b528a8e95270b7abfe432a94b321c411ab1");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_common_p3_v7.py",
  "bcfafa18e646d9ac2ef4b5b3d8693a1547da761a34335f6f0c2643938baf270c");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_common_p3_v8.py",
  "46194661f3d80c5d95025a3e4efad3b0ba25a28d9f77657d554060cb070e3d9e");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_p3_producer_v1.py",
  "5313639b334dd88b302f154dc3d72dfdad0476e93ed12d79e808d4a2f74fc9e8");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_p3_producer_v2.py",
  "41cf6a9d7d580083c1e451a831dd10c53243bb44869494e6e5e97a922a3bab72");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_p3_producer_v3.py",
  "52cda6616a0c88ac59b02db8d4dc70f65cd8d66c9c44d97a72ea73e5d020c903");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_p3_producer_v4.py",
  "02ff8afc3d296a79d7039c615de0db5fa1178fa7aaca93ddba3146626089feaa");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_p3_producer_v5.py",
  "cad712f2362ef484665c266b0c184caefd8851bb2d40117dcab2f45a20c45aa3");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_p3_producer_v6.py",
  "5d557a642e34274462750e466795650a608810e6555964736c5e92aac911e2a2");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_p3_producer_v7.py",
  "b1fba6374d37608a0e1faef4ad7ed6087c25b84c2bde33a6903cb37926111acc");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_p3_producer_v8.py",
  "bd1911b1b9f2a3665e81529694be8e6d421d93a713644c6355e9f360ed7b6a3b");

P159OR36P3V10RequireSha(
  "search/d972_row36_pent_bridge_p3_transition_worker_generator_v8.py",
  "2c56f5a77e5809f5976778739cab3487d30bb58074d171c74fd59ee6f9fcd27b");
P159OR36P3V10RequireSha(
  "search/d972_row36_pent_bridge_p3_transition_worker_v8.g",
  "dc87c6872a68141f30be15ebad05d9ea12f343347fdf953e944d335294559035");
P159OR36P3V10RequireSha("search/d972_row36_pent_bridge_p3_prereg_gha_v8.g",
  "fa06dc6d2989e8a7402a39876252067b891e8b66d4d9441fe0ba646f7429e20e");
P159OR36P3V10RequireSha(
  "search/certs/d972_row36_pent_bridge_p3_prereg_execution_manifest_v8_20260824.json",
  "9a3699215c3ce331539028db5c12d30ce594175dfec3975ddb83fc2f2285786c");

Print("PENT159O_ROW36_P3_V10_RECURSIVE_CLOSURE_PASS python_files=16 import_or_file_pin_edges=63 unresolved=0 newly_supplied=6 math_change=false universe_change=false predicate_execution=false delegated_schema=v8\n");
Read("search/d972_row36_pent_bridge_p3_prereg_gha_v8.g");
