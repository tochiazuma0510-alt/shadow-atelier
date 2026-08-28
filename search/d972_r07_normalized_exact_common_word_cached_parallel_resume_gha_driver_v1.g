#############################################################################
## Task311 task192 persistent-process boundary adapter driver v1.
## ASCII only.  It pins inputs and runs the producer before the checker.
#############################################################################
D311Driver:="search/d972_r07_normalized_exact_common_word_cached_parallel_resume_gha_driver_v1.g";;
D311Schema:="d972-r07-normalized-exact-common-word-cached-parallel/driver/v1";;
D311Version:="task311-v1";;
D311Producer:="search/d972_r07_normalized_exact_common_word_cached_parallel_v4.py";;
D311Checker:="crosscheck/check_d972_r07_normalized_exact_common_word_cached_parallel_v4.py";;
D311Fixture:="search/certs/d972_r07_normalized_exact_common_word_cached_parallel_selftest_v1_20260828.json";;
D311Resume:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip";;
D311Manifest:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json";;
D311Receipt:="ci/out/d972_r07_normalized_exact_common_word_cached_parallel_v4.json";;
D311Verdict:="ci/out/d972_r07_normalized_exact_common_word_cached_parallel_v4.verdict.json";;
D311ProducerLog:="ci/out/d972_r07_normalized_exact_common_word_cached_parallel_v4.producer.log";;
D311CheckerLog:="ci/out/d972_r07_normalized_exact_common_word_cached_parallel_v4.checker.log";;
D311Shell:="ci/out/d972_r07_normalized_exact_common_word_cached_parallel_v4.sh";;
D311Checkpoint:="ci/out/d972_r07_normalized_exact_common_word_cached_parallel_v4.json.checkpoint.json";;
D311OK:="ci/out/d972_r07_normalized_exact_common_word_cached_parallel_v4.ok";;
D311Sentinel:="R07_NORMALIZED_EXACT_COMMON_WORD_CACHED_PARALLEL_V4_DRIVER_SENTINEL";;
D311ProducerPass:="R07_NORMALIZED_EXACT_COMMON_WORD_CACHED_PARALLEL_V4_SELFTEST_PASS";;
D311ProducerPrefix:="R07_NORMALIZED_EXACT_COMMON_WORD_CACHED_PARALLEL_V4_PRODUCER_TERMINAL";;
D311CheckerPass:="R07_NORMALIZED_EXACT_COMMON_WORD_CACHED_PARALLEL_V4_CHECKER_PASS";;
D311CheckerPrefix:="R07_NORMALIZED_EXACT_COMMON_WORD_CACHED_PARALLEL_V4_CHECKER_TERMINAL";;

if not IsBound(GetEnv) then GetEnv:=name->fail; fi;;
D311Mode:=GetEnv("D972_R07_V4_MODE");;
if D311Mode=fail or D311Mode="" then D311Mode:="SELFTEST"; fi;;
if Position(["SELFTEST","PRODUCTION"],D311Mode)=fail then
  Error("task311 mode must be SELFTEST or PRODUCTION");
fi;

if not IsExistingFile(D311Driver) or
   D311Schema<>"d972-r07-normalized-exact-common-word-cached-parallel/driver/v1" or
   D311Version<>"task311-v1" then
  Error("task311 driver identity");
fi;

D311Pins:=[
 ["search/d972_r07_normalized_exact_common_word_cached_v3.py",193704,"f27b4971351832b8730fb8cce4e782e893a958dfb850203cc735c7bc3aa31f37"],
 ["crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py",154009,"dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10"],
 ["search/d972_r07_normalized_exact_common_word_cached_gha_driver_v3.g",11548,"2f7ff7b459e46d014268907ff5ba5f03c035836e8f8df79a2c5f4cdc3b75351d"],
 ["search/certs/d972_r07_normalized_exact_common_word_cached_selftest_v3_20260827.json",276,"c49f434ad3daf1cc661ba45563dbb9557d436f91dca78c8ee0f47ed70332da12"],
 ["search/d972_r07_normalized_exact_common_word_parallel_v5.py",39234,"19a2970fcf072c25c606d0305fd999c8481353e0be20879de4be2aa26f6fb90c"],
 ["crosscheck/check_d972_r07_normalized_exact_common_word_parallel_v5.py",32486,"530d67c854017a538fa2185b8bc5c48834a785f5bd6db38452db3551695cf1df"],
 ["search/d972_r07_normalized_exact_common_word_parallel_gha_driver_v5.g",7971,"0ac1b26d1844fdc16cc2701c536f50fd5415a7ef2479e030ebde96af79af4902"],
 ["search/certs/d972_r07_normalized_exact_common_word_parallel_selftest_v5_20260828.json",1195,"4d481ba84e3c452c79f344e66a0eea5322ec8b64c15a81f1a290c22ce18e3fc9"],
 ["sol/proof_r07_frozen_dual_boundary_mapreduce_v254.md",6195,"e9fc7a69525200e8e1c0e8152652229227877ba923378ade8afa199c4f4ee1a0"],
 ["sol/proof_r07_boundary_adapter_state_and_local_provenance_v255.md",8814,"06c93c46b48b681e0316d302058b72bc0b76fe9d12888cde3f7e45dc3a93ffa0"],
 ["sol/audit_r07_task192_cumulative_pairs_and_persistent_pool_v256.md",4790,"f5a0c6e625e5113e4213b62762267fc9a5437cafd9f9751e603b055c549c1251"],
 ["search/d972_r07_normalized_exact_common_word_cached_resume_gha_driver_v2.g",19682,"169da7aa149d68907abb435f380b9ec2994c2bc285c6a17f13431614a388f5ad"],
 [D311Resume,5001811,"f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566"],
 [D311Manifest,1328,"6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302"]
];;

D311Pin:=function(row)
  local raw;
  if not IsExistingFile(row[1]) then Error("task311 missing pin ",row[1]); fi;
  raw:=StringFile(row[1]);;
  if raw=fail or Length(raw)<>row[2] or HexSHA256(raw)<>row[3] then
    Error("task311 pin drift ",row[1]);
  fi;
end;;
for D311Row in D311Pins do D311Pin(D311Row);; od;

if D311Mode="SELFTEST" then
  D311Tag:="selftest";;
else
  D311Tag:="production";;
fi;
D311Receipt:=Concatenation("ci/out/d972_r07_normalized_exact_common_word_cached_parallel_v4_",D311Tag,".json");;
D311Verdict:=Concatenation("ci/out/d972_r07_normalized_exact_common_word_cached_parallel_v4_",D311Tag,".verdict.json");;
D311ProducerLog:=Concatenation("ci/out/d972_r07_normalized_exact_common_word_cached_parallel_v4_",D311Tag,".producer.log");;
D311CheckerLog:=Concatenation("ci/out/d972_r07_normalized_exact_common_word_cached_parallel_v4_",D311Tag,".checker.log");;
D311Shell:=Concatenation("ci/out/d972_r07_normalized_exact_common_word_cached_parallel_v4_",D311Tag,".sh");;
D311Checkpoint:=Concatenation(D311Receipt,".checkpoint.json");;
D311OK:=Concatenation("ci/out/d972_r07_normalized_exact_common_word_cached_parallel_v4_",D311Tag,".ok");;

D311Outputs:=[D311Receipt,D311Verdict,D311ProducerLog,D311CheckerLog,
  D311Shell,D311Checkpoint,D311OK];;
for D311Path in D311Outputs do
  if IsExistingFile(D311Path) then Error("task311 stale output ",D311Path); fi;
od;

Exec("mkdir -p ci/out");;
D311Stream:=OutputTextFile(D311Shell,false);;
if D311Stream=fail then Error("task311 shell open"); fi;
SetPrintFormattingStatus(D311Stream,false);;
PrintTo(D311Stream,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
PrintTo(D311Stream,"workers=$(nproc 2>/dev/null || printf 2)\n");
PrintTo(D311Stream,"if [ \"$workers\" -lt 2 ]; then workers=2; fi\n");
PrintTo(D311Stream,"if [ \"$workers\" -gt 4 ]; then workers=4; fi\n");
if D311Mode="SELFTEST" then
  PrintTo(D311Stream,"python3 -u -B ",D311Producer,
    " --mode SELFTEST --fixture ",D311Fixture,
    " --boundary-workers \"$workers\" --output ",D311Receipt,
    " > ",D311ProducerLog," 2>&1\n");
else
  PrintTo(D311Stream,"python3 -u -B ",D311Producer,
    " --mode PRODUCTION --resume ",D311Resume,
    " --boundary-workers \"$workers\" --seconds 10800 --boundary-pairs 8000000",
    " --fibre-scans 80000000 --candidate-words 2000000 --retained-columns 250000",
    " --checkpoint-bytes 4000000000 --rss-bytes 5700000000 --oracle-rounds 1",
    " --output ",D311Receipt," > ",D311ProducerLog," 2>&1\n");
fi;
PrintTo(D311Stream,"test -s ",D311Receipt," -a -s ",D311ProducerLog,"\n");
PrintTo(D311Stream,"grep -Ec '^",D311ProducerPrefix," .+$' ",D311ProducerLog," | grep -qx 1\n");
if D311Mode="SELFTEST" then
  PrintTo(D311Stream,"grep -Fxc '",D311ProducerPass,"' ",D311ProducerLog," | grep -qx 1\n");
fi;
PrintTo(D311Stream,"python3 -u -B ",D311Checker,
  " --mode ",D311Mode," --fixture ",D311Fixture,
  " --receipt ",D311Receipt," --output ",D311Verdict,
  " > ",D311CheckerLog," 2>&1\n");
PrintTo(D311Stream,"test -s ",D311Verdict," -a -s ",D311CheckerLog,"\n");
if D311Mode="SELFTEST" then
  PrintTo(D311Stream,"grep -Fxc '",D311CheckerPass,"' ",D311CheckerLog," | grep -qx 1\n");
fi;
PrintTo(D311Stream,"grep -Ec '^",D311CheckerPrefix," terminal=.+$' ",D311CheckerLog," | grep -qx 1\n");
PrintTo(D311Stream,"producer_terminal=$(grep -E '^",D311ProducerPrefix," ' ",D311ProducerLog,
  " | sed -E 's/^",D311ProducerPrefix," //')\n");
PrintTo(D311Stream,"checker_terminal=$(grep -E '^",D311CheckerPrefix," terminal=' ",D311CheckerLog,
  " | sed -E 's/^",D311CheckerPrefix," terminal=//')\n");
PrintTo(D311Stream,"test \"$producer_terminal\" = \"$checker_terminal\"\n");
PrintTo(D311Stream,"test -n \"$producer_terminal\" -a -n \"$checker_terminal\"\n");
if D311Mode="SELFTEST" then
  PrintTo(D311Stream,"test ! -e ",D311Checkpoint,"\n");
else
  PrintTo(D311Stream,"case \"$producer_terminal\" in\n");
  PrintTo(D311Stream,"  R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD) test ! -e ",D311Checkpoint," ;;\n");
  PrintTo(D311Stream,"  UNKNOWN_RESOURCE:*) test -s ",D311Checkpoint," ;;\n");
  PrintTo(D311Stream,"  UNKNOWN_INPUT:*) test ! -e ",D311Checkpoint," ;;\n");
  PrintTo(D311Stream,"  *) echo task311 unexpected terminal >&2; exit 1 ;;\n");
  PrintTo(D311Stream,"esac\n");
fi;
PrintTo(D311Stream,"printf '%s' '",D311Sentinel,"' > ",D311OK,"\n");
PrintTo(D311Stream,"test -s ",D311OK,"\n");
CloseStream(D311Stream);;

Exec(Concatenation("bash ",D311Shell));;
D311Observed:=StringFile(D311OK);;
if D311Observed=fail or D311Observed<>D311Sentinel then
  Error("task311 sentinel mismatch");
fi;
Print("R07_NORMALIZED_EXACT_COMMON_WORD_CACHED_PARALLEL_V4_DRIVER_PASS mode=",D311Mode,"\n");
