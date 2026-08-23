#############################################################################
## P3 fixed-row36 v9 dependency-complete launcher over frozen v8 math.
#############################################################################

P159OR36P3V9RequireSha:=function(path,expected)
  local raw,actual;
  raw:=StringFile(path);
  if raw=fail then
    Error("PENT159O_ROW36_P3_V9: missing immutable input ",path);
  fi;
  actual:=HexSHA256(raw);
  if actual<>expected then
    Error("PENT159O_ROW36_P3_V9: immutable input hash mismatch ",path,
      " expected=",expected," actual=",actual);
  fi;
  Print("PENT159O_ROW36_P3_V9_PIN_PASS path=",path," bytes=",Length(raw),
    " sha256=",actual,"\n");
end;

P159OR36P3V9RequireSha("search/d972_row36_pent_bridge_p3_producer_v2.py",
  "41cf6a9d7d580083c1e451a831dd10c53243bb44869494e6e5e97a922a3bab72");
P159OR36P3V9RequireSha("search/d972_row36_pent_bridge_common_p3_v8.py",
  "46194661f3d80c5d95025a3e4efad3b0ba25a28d9f77657d554060cb070e3d9e");
P159OR36P3V9RequireSha("search/d972_row36_pent_bridge_p3_producer_v8.py",
  "bd1911b1b9f2a3665e81529694be8e6d421d93a713644c6355e9f360ed7b6a3b");
P159OR36P3V9RequireSha(
  "search/d972_row36_pent_bridge_p3_transition_worker_generator_v8.py",
  "2c56f5a77e5809f5976778739cab3487d30bb58074d171c74fd59ee6f9fcd27b");
P159OR36P3V9RequireSha(
  "search/d972_row36_pent_bridge_p3_transition_worker_v8.g",
  "dc87c6872a68141f30be15ebad05d9ea12f343347fdf953e944d335294559035");
P159OR36P3V9RequireSha("search/d972_row36_pent_bridge_p3_prereg_gha_v8.g",
  "fa06dc6d2989e8a7402a39876252067b891e8b66d4d9441fe0ba646f7429e20e");
P159OR36P3V9RequireSha(
  "search/certs/d972_row36_pent_bridge_p3_prereg_execution_manifest_v8_20260824.json",
  "9a3699215c3ce331539028db5c12d30ce594175dfec3975ddb83fc2f2285786c");

Print("PENT159O_ROW36_P3_V9_DEPENDENCY_COMPLETE_PASS missing_v8_runtime_entry=search/d972_row36_pent_bridge_p3_producer_v2.py math_change=false universe_change=false predicate_execution=false delegated_schema=v8\n");
Read("search/d972_row36_pent_bridge_p3_prereg_gha_v8.g");
