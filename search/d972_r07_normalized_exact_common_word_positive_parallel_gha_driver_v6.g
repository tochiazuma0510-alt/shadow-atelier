#############################################################################
## Task325 positive-only persistent parallel adapter v6 driver.
## ASCII only.  This file has no recursive self-hash.
#############################################################################
D325ModeVariable:="D972_R07_POSITIVE_PARALLEL_V6_MODE";;
D325Mode:="SELFTEST";;
if IsBound(GetEnv) then
  D325EnvMode:=GetEnv(D325ModeVariable);;
  if D325EnvMode<>fail and D325EnvMode<>"" then D325Mode:=D325EnvMode;; fi;
fi;
if D325Mode<>"SELFTEST" and D325Mode<>"PRODUCTION" then
  Error("task325 mode must be SELFTEST or PRODUCTION");
fi;

D325Producer:="search/d972_r07_normalized_exact_common_word_positive_parallel_v6.py";;
D325Checker:="crosscheck/check_d972_r07_normalized_exact_common_word_positive_parallel_v6.py";;
D325Fixture:="search/certs/d972_r07_normalized_exact_common_word_positive_parallel_selftest_v6_20260828.json";;
D325Resume:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip";;
D325Manifest:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json";;
D325ProducerPrefix:="R07_NORMALIZED_EXACT_COMMON_WORD_POSITIVE_PARALLEL_V6_PRODUCER_TERMINAL";;
D325CheckerPrefix:="R07_NORMALIZED_EXACT_COMMON_WORD_POSITIVE_PARALLEL_V6_CHECKER_TERMINAL";;
D325SelfMarker:="R07_NORMALIZED_EXACT_COMMON_WORD_POSITIVE_PARALLEL_V6_SELFTEST_PASS";;
D325CheckerSelfMarker:="R07_NORMALIZED_EXACT_COMMON_WORD_POSITIVE_PARALLEL_V6_CHECKER_SELFTEST_PASS";;
D325Common:="R07_NORMALIZED_EXACT_COMMON_WORD_POSITIVE_PARALLEL_V6_COMMON_WORD";;
D325Sentinel:="R07_NORMALIZED_EXACT_COMMON_WORD_POSITIVE_PARALLEL_V6_DRIVER_PASS";;

if D325Mode="SELFTEST" then D325Tag:="selftest";;
else D325Tag:="production";; fi;
D325Base:=Concatenation("ci/out/d972_r07_normalized_exact_common_word_positive_parallel_v6_",D325Tag);;
D325Receipt:=Concatenation(D325Base,".json");;
D325Verdict:=Concatenation(D325Base,".verdict.json");;
D325ProducerLog:=Concatenation(D325Base,".producer.log");;
D325CheckerLog:=Concatenation(D325Base,".checker.log");;
D325ProducerTerminalFile:=Concatenation(D325Base,".producer.terminal");;
D325CheckerTerminalFile:=Concatenation(D325Base,".checker.terminal");;
D325Shell:=Concatenation(D325Base,".sh");;
D325Inner:=Concatenation(D325Receipt,".inner_v3.json");;
D325Checkpoint:=Concatenation(D325Receipt,".checkpoint.json");;
D325OK:=Concatenation(D325Base,".ok");;

D325Pins:=[
 [D325Producer,127376,"6f06465bc4599f91dee32ecab9624971c33461b12c7d38139684f578ee9d9218"],
 [D325Checker,58516,"fe3b83309eaff0531f0154a31a1a7a051171fb6a1ae8a3f706eb672f6659e47c"],
 [D325Fixture,4102,"a6ade562478f86fcd986f119f4d349949c7a866332999acb1d9605a039fcb8ad"],
 ["sol/luna_task_325_r07_task192_positive_only_persistent_parallel_v6.md",10172,"b22813ff9aa5250af25412db34f98b6e40996115a874e895b497e3a8753e4bf8"],
 ["sol/proof_r07_positive_only_common_word_colgen_v140.md",10073,"6d388a74c75d55d215b0035496c451aa9de5bbc7a8248c277e76021092b8562b"],
 ["sol/proof_r07_history_free_positive_common_word_verifier_v265.md",10122,"fd30ccb2458691ec7844d304f220a4be7d704259318c452f928f8088552ecb0a"],
 ["sol/audit_r07_task192_boundary_resume_semantics_v253.md",4110,"a1d9f6d3d8cb31d8b261dd5cb1977865abfeba24bfc6aae7436d2a893e3ef19a"],
 ["sol/proof_r07_frozen_dual_boundary_mapreduce_v254.md",6195,"e9fc7a69525200e8e1c0e8152652229227877ba923378ade8afa199c4f4ee1a0"],
 ["sol/proof_r07_boundary_adapter_state_and_local_provenance_v255.md",8814,"06c93c46b48b681e0316d302058b72bc0b76fe9d12888cde3f7e45dc3a93ffa0"],
 ["sol/audit_r07_task192_cumulative_pairs_and_persistent_pool_v256.md",4790,"f5a0c6e625e5113e4213b62762267fc9a5437cafd9f9751e603b055c549c1251"],
 ["sol/sol_reply_319_r07_task311_persistent_parallel_code_performance_audit.md",20604,"9b9908eadf0f8c8204f9397d2af0511ba98959a979a00058c7b28cae9c74f981"],
 ["sol/luna_task_321_r07_task192_persistent_parallel_adapter_v5_rewrite.md",9128,"681b7a1a4b8edcd6f788f8d01aca930d60f3e61330293e70a4db47df205d2cc9"],
 ["sol/luna_reply_321_r07_task192_persistent_parallel_adapter_v5.md",12122,"bd8104b462f35979af2fd2ee820ad08a1c1c165cac6e2558a8e4eba6e7946c8b"],
 ["search/d972_r07_normalized_exact_common_word_parallel_v5.py",39234,"19a2970fcf072c25c606d0305fd999c8481353e0be20879de4be2aa26f6fb90c"],
 ["crosscheck/check_d972_r07_normalized_exact_common_word_parallel_v5.py",32486,"530d67c854017a538fa2185b8bc5c48834a785f5bd6db38452db3551695cf1df"],
 ["search/d972_r07_normalized_exact_common_word_parallel_gha_driver_v5.g",7971,"0ac1b26d1844fdc16cc2701c536f50fd5415a7ef2479e030ebde96af79af4902"],
 ["search/certs/d972_r07_normalized_exact_common_word_parallel_selftest_v5_20260828.json",1195,"4d481ba84e3c452c79f344e66a0eea5322ec8b64c15a81f1a290c22ce18e3fc9"],
 ["search/d972_r07_normalized_exact_common_word_cached_v3.py",193704,"f27b4971351832b8730fb8cce4e782e893a958dfb850203cc735c7bc3aa31f37"],
 ["crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py",154009,"dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10"],
 ["search/d972_r07_normalized_exact_common_word_cached_gha_driver_v3.g",11548,"2f7ff7b459e46d014268907ff5ba5f03c035836e8f8df79a2c5f4cdc3b75351d"],
 ["search/certs/d972_r07_normalized_exact_common_word_cached_selftest_v3_20260827.json",276,"c49f434ad3daf1cc661ba45563dbb9557d436f91dca78c8ee0f47ed70332da12"],
 ["search/d972_r07_normalized_exact_common_word_cached_resume_gha_driver_v2.g",19682,"169da7aa149d68907abb435f380b9ec2994c2bc285c6a17f13431614a388f5ad"],
 ["sol/luna_reply_298_r07_task192_checkpoint_resume_transport_v2.md",9200,"732c9b1d279e9201d4cce3b432b5a4805a60d346d6104865246ce0a3030af22f"],
 [D325Resume,5001811,"f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566"],
 [D325Manifest,1328,"6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302"]
];;

D325Read:=function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task325 missing input ",path); fi;
  return raw;
end;;

D325Pin:=function(row)
  local raw;
  raw:=D325Read(row[1]);;
  if Length(raw)<>row[2] or HexSHA256(raw)<>row[3] then
    Error("task325 pin drift ",row[1]);
  fi;
end;;

for D325Row in D325Pins do D325Pin(D325Row);; od;

Exec("mkdir -p ci/out");;
D325StalePrefixes:=[
 "d972_r07_normalized_exact_common_word_cached_parallel_v4",
 "d972_r07_normalized_exact_common_word_parallel_v4",
 "d972_r07_normalized_exact_common_word_parallel_v5",
 "d972_r07_normalized_exact_common_word_cached_parallel_v5",
 "d972_r07_normalized_exact_common_word_parallel_v6",
 "d972_r07_normalized_exact_common_word_cached_parallel_v6",
 "d972_r07_normalized_exact_common_word_positive_parallel_v6"
];;
D325Contents:=DirectoryContents("ci/out");;
if D325Contents=fail then Error("task325 cannot inspect ci/out"); fi;
for D325Name in D325Contents do
  for D325Prefix in D325StalePrefixes do
    if PositionSublist(D325Name,D325Prefix)=1 then
      Error("task325 stale v4-v6 owned output ",D325Name);
    fi;
  od;
od;

D325Outputs:=[D325Receipt,D325Verdict,D325ProducerLog,D325CheckerLog,
 D325ProducerTerminalFile,D325CheckerTerminalFile,D325Shell,D325Inner,
 D325Checkpoint,D325OK];;
if Length(D325Outputs)<>Length(Set(D325Outputs)) then
  Error("task325 duplicate output path");
fi;
for D325Path in D325Outputs do
  if IsExistingFile(D325Path) then Error("task325 stale output ",D325Path); fi;
od;

D325Stream:=OutputTextFile(D325Shell,false);;
if D325Stream=fail then Error("task325 shell open"); fi;
SetPrintFormattingStatus(D325Stream,false);;
PrintTo(D325Stream,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
PrintTo(D325Stream,"available=$(nproc 2>/dev/null || printf 2)\n");
PrintTo(D325Stream,"if [ \"$available\" -ge 4 ]; then workers=4; else workers=2; fi\n");
if D325Mode="SELFTEST" then
  PrintTo(D325Stream,"python3 -u -B ",D325Producer,
    " --mode SELFTEST --fixture ",D325Fixture,
    " --boundary-workers \"$workers\" --output ",D325Receipt,
    " > ",D325ProducerLog," 2>&1\n");
else
  PrintTo(D325Stream,"python3 -u -B ",D325Producer,
    " --mode PRODUCTION --fixture ",D325Fixture,
    " --resume ",D325Resume," --resume-manifest ",D325Manifest,
    " --boundary-workers \"$workers\" --seconds 19800",
    " --boundary-pairs 8000000 --fibre-scans 80000000",
    " --candidate-words 2000000 --retained-columns 250000",
    " --checkpoint-bytes 4000000000 --rss-bytes 5700000000",
    " --oracle-rounds 1 --output ",D325Receipt,
    " > ",D325ProducerLog," 2>&1\n");
fi;
PrintTo(D325Stream,"test -s ",D325Receipt," -a -s ",D325ProducerLog,"\n");
PrintTo(D325Stream,"test \"$(grep -c '^",D325ProducerPrefix," ' ",D325ProducerLog,")\" -eq 1\n");
PrintTo(D325Stream,"grep -E '^",D325ProducerPrefix," ' ",D325ProducerLog,
  " | sed 's/^",D325ProducerPrefix," //' > ",D325ProducerTerminalFile,"\n");
if D325Mode="SELFTEST" then
  PrintTo(D325Stream,"grep -Fxc '",D325SelfMarker,"' ",D325ProducerLog," | grep -qx 1\n");
fi;

PrintTo(D325Stream,"python3 -u -B ",D325Checker," ",D325Receipt,
  " --output ",D325Verdict," > ",D325CheckerLog," 2>&1\n");
PrintTo(D325Stream,"test -s ",D325Verdict," -a -s ",D325CheckerLog,"\n");
PrintTo(D325Stream,"test \"$(grep -c '^",D325CheckerPrefix," terminal=' ",D325CheckerLog,")\" -eq 1\n");
PrintTo(D325Stream,"grep -E '^",D325CheckerPrefix," terminal=' ",D325CheckerLog,
  " | sed 's/^",D325CheckerPrefix," terminal=//' > ",D325CheckerTerminalFile,"\n");
if D325Mode="SELFTEST" then
  PrintTo(D325Stream,"grep -Fxc '",D325CheckerSelfMarker,"' ",D325CheckerLog," | grep -qx 1\n");
fi;
PrintTo(D325Stream,"test -s ",D325ProducerTerminalFile," -a -s ",D325CheckerTerminalFile,"\n");
PrintTo(D325Stream,"test \"$(wc -l < ",D325ProducerTerminalFile,")\" -eq 1\n");
PrintTo(D325Stream,"test \"$(wc -l < ",D325CheckerTerminalFile,")\" -eq 1\n");
PrintTo(D325Stream,"cmp -s ",D325ProducerTerminalFile," ",D325CheckerTerminalFile,"\n");
PrintTo(D325Stream,"grep -Fq '\"self_digest_sha256\":\"' ",D325Receipt,"\n");
PrintTo(D325Stream,"grep -Fq '\"self_digest_sha256\":\"' ",D325Verdict,"\n");
PrintTo(D325Stream,"terminal=$(tr -d '\\n' < ",D325ProducerTerminalFile,")\n");
PrintTo(D325Stream,"case \"$terminal\" in\n");
PrintTo(D325Stream,"  ",D325SelfMarker,") test ! -e ",D325Inner," -a ! -e ",D325Checkpoint," ;;\n");
PrintTo(D325Stream,"  ",D325Common,") test -s ",D325Inner," -a ! -e ",D325Checkpoint," ;;\n");
PrintTo(D325Stream,"  UNKNOWN_RESOURCE:*) test -s ",D325Checkpoint," -a ! -e ",D325Inner," ;;\n");
PrintTo(D325Stream,"  UNKNOWN_INPUT:*) test ! -e ",D325Checkpoint," -a ! -e ",D325Inner," ;;\n");
PrintTo(D325Stream,"  *) exit 1 ;;\n");
PrintTo(D325Stream,"esac\n");
PrintTo(D325Stream,"printf '%s' '",D325Sentinel,"' > ",D325OK,"\n");
PrintTo(D325Stream,"test -s ",D325OK,"\n");
CloseStream(D325Stream);;

Exec(Concatenation("bash ",D325Shell));;
D325Observed:=D325Read(D325OK);;
if D325Observed<>D325Sentinel then Error("task325 sentinel mismatch"); fi;
Print(D325Sentinel," mode=",D325Mode,"\n");
