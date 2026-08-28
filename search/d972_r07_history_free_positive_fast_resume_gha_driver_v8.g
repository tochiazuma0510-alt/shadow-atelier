#############################################################################
## Task349 R07 A0/v8 audited fast resume driver.
## ASCII only.  The driver has no recursive self pin.
#############################################################################
D342Producer:="search/d972_r07_history_free_positive_fast_resume_v8.py";;
D342Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_v8.py";;
D342Fixture:="search/certs/d972_r07_history_free_positive_fast_resume_selftest_v8_20260829.json";;
D342Zip:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip";;
D342Manifest:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json";;
D342Member:="d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json";;
D342Raw:="ci/resume/d972_r07_history_free_positive_fast_resume_v8.raw.json";;
D342SelftestReceipt:="ci/in/d972_r07_history_free_positive_fast_resume_selftest_v8.accepted.json";;
D342Base:="ci/out/d972_r07_history_free_positive_fast_resume_v8_production";;
D342Receipt:=Concatenation(D342Base,".json");;
D342Checkpoint:=Concatenation(D342Receipt,".checkpoint.json");;
D342Verdict:=Concatenation(D342Base,".verdict.json");;
D342ProducerLog:=Concatenation(D342Base,".producer.log");;
D342CheckerLog:=Concatenation(D342Base,".checker.log");;
D342ProducerTerminal:=Concatenation(D342Base,".producer.terminal");;
D342CheckerTerminal:=Concatenation(D342Base,".checker.terminal");;
D342Shell:=Concatenation(D342Base,".sh");;
D342OK:=Concatenation(D342Base,".ok");;
D342Common:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V8_COMMON_WORD";;
D342Selftest:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V8_SELFTEST_PASS";;
D342ProducerPrefix:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V8_PRODUCER_TERMINAL";;
D342CheckerPrefix:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V8_CHECKER_TERMINAL";;
D342Sentinel:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V8_DRIVER_PASS";;

D342Pins:=[
 [D342Producer,140467,"8499a50d5fc05a5d850de0d4a1ea80d3ddbc0a37c2cfd8b8a28cb3c6f95d5a0e"],
 [D342Checker,102497,"219c42baf0829c41e6f7cdb9376693632162fdd9ca0828e311c7396d80795262"],
 [D342Fixture,2784,"a96d7e400b5f71a03975b9d223b98fe6cc6c22ef8e17fe59f0eac07f4bc7e641"],
 ["sol/luna_task_342_r07_a0_v7_fast_positive_resume.md",15393,"9fca7eb266b433436f44a25f0b984d6941c5a1696e960a80e062c5abefcc028d"],
 ["sol/sol_reply_337_r07_task325_v6_code_performance_audit_v1.md",42611,"035f3d987746f9662fb66da512889da7ad4f7ad899a3cc768e626093ce050f4a"],
 ["sol/proof_r07_history_free_positive_common_word_verifier_v265.md",10122,"fd30ccb2458691ec7844d304f220a4be7d704259318c452f928f8088552ecb0a"],
 ["sol/proof_r07_two_way_basis_checkpoint_resume_v275.md",7662,"51febdaadcdf9130af4dd0586969f28f533ff3e9d06d883841aa115410dd40ea"],
 ["sol/proof_r07_triangular_checkpoint_basis_resume_v276.md",5571,"5765aec25e08e687841451d3707ba16e0f3e2c6c4d9de6c120e92bdafe071abb"],
 ["sol/proof_r07_boundary_first_lazy_runtime_resume_v277.md",9070,"2539fa530195b7c5fe7035d2261301ed85c471af2df313fd33fb01e96df9a56d"],
 ["sol/proof_r07_selected_support_positive_replay_v278.md",7055,"f9dcb97c86e401bd96a92805b6c31428483d624874388bcc0439d1f7dc2f390b"],
 ["sol/audit_r07_task298_six_hour_cancel_no_artifact_v279.md",3844,"f669705e93a5ad3c84fb94a5b7f8ec4cf3cedd103df1e0b1d78460e9c8b1f5c9"],
 ["search/d972_r07_positive_common_word_colgen_v1.py",123870,"47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"],
 ["search/d972_r07_all_seven_raw_bridge_preflight_v1.py",60306,"1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa"],
 ["search/d972_r07_all_seven_extension_section_census_v1.py",66109,"878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"],
 ["ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json",231570,"3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"],
 ["ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json",2166036,"1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"],
 ["search/d972_b345_seedspan_triple4_v1.py",535219,"fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"],
 ["search/d972_b345_triple_cube_raw_lambda_census_v1.py",126942,"d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"],
 ["search/d972_b345_joint_kernel_qstar_closure_v1.py",67945,"06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"],
 ["search/d972_r07_full_e4_joint_orbit_preflight_v7.py",21918,"92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed"],
 ["search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py",33409,"f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f"],
 ["search/d972_b345_target6_dual_colgen_v2.py",444497,"b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7"],
 [D342Manifest,1328,"6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302"],
 [D342Zip,5001811,"f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566"]
];;

D342Read:=function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task349 missing input ",path); fi;
  return raw;
end;;

D342Pin:=function(row)
  local raw;
  raw:=D342Read(row[1]);;
  if Length(raw)<>row[2] or HexSHA256(raw)<>row[3] then
    Error("task349 pin drift ",row[1]);
  fi;
end;;

for D342Row in D342Pins do D342Pin(D342Row);; od;

Exec("mkdir -p ci/out ci/resume");;
D342Contents:=DirectoryContents("ci/out");;
if D342Contents=fail then Error("task349 cannot inspect ci/out"); fi;
for D342Name in D342Contents do
  if PositionSublist(D342Name,
      "d972_r07_history_free_positive_fast_resume_v8_")=1 then
    Error("task349 stale v8 owned output ",D342Name);
  fi;
od;

D342Outputs:=[D342Raw,D342Receipt,D342Checkpoint,D342Verdict,
 D342ProducerLog,D342CheckerLog,D342ProducerTerminal,D342CheckerTerminal,
 D342Shell,D342OK];;
if Length(D342Outputs)<>Length(Set(D342Outputs)) then
  Error("task349 duplicate output path");
fi;
for D342Path in D342Outputs do
  if IsExistingFile(D342Path) then Error("task349 stale output ",D342Path); fi;
od;

D342Stream:=OutputTextFile(D342Shell,false);;
if D342Stream=fail then Error("task349 shell open"); fi;
SetPrintFormattingStatus(D342Stream,false);;
PrintTo(D342Stream,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D342Stream,"available=$(nproc 2>/dev/null || printf 2)\n");
PrintTo(D342Stream,"if [ \"$available\" -ge 4 ]; then workers=4; else workers=2; fi\n");
PrintTo(D342Stream,"python3 -B - ",D342Zip," ",D342Raw," <<'PY'\n");
PrintTo(D342Stream,"import hashlib, os, sys, zipfile\n");
PrintTo(D342Stream,"source, output = sys.argv[1], sys.argv[2]\n");
PrintTo(D342Stream,"expected_name = '",D342Member,"'\n");
PrintTo(D342Stream,"expected_size = 86368039\n");
PrintTo(D342Stream,"expected_sha = 'c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab'\n");
PrintTo(D342Stream,"try:\n");
PrintTo(D342Stream,"    with zipfile.ZipFile(source, 'r') as archive:\n");
PrintTo(D342Stream,"        infos = archive.infolist()\n");
PrintTo(D342Stream,"        if len(infos) != 1 or infos[0].filename != expected_name or infos[0].file_size != expected_size:\n");
PrintTo(D342Stream,"            raise SystemExit('task349 frozen sole ZIP member gate')\n");
PrintTo(D342Stream,"        digest = hashlib.sha256(); size = 0\n");
PrintTo(D342Stream,"        temporary = output + '.tmp.' + str(os.getpid())\n");
PrintTo(D342Stream,"        with archive.open(infos[0], 'r') as incoming, open(temporary, 'xb') as outgoing:\n");
PrintTo(D342Stream,"            while True:\n");
PrintTo(D342Stream,"                block = incoming.read(1048576)\n");
PrintTo(D342Stream,"                if not block: break\n");
PrintTo(D342Stream,"                outgoing.write(block); digest.update(block); size += len(block)\n");
PrintTo(D342Stream,"            outgoing.flush(); os.fsync(outgoing.fileno())\n");
PrintTo(D342Stream,"        if size != expected_size or digest.hexdigest() != expected_sha:\n");
PrintTo(D342Stream,"            raise SystemExit('task349 frozen raw member gate')\n");
PrintTo(D342Stream,"        os.replace(temporary, output)\n");
PrintTo(D342Stream,"        directory_fd = os.open(os.path.dirname(output) or '.', os.O_RDONLY)\n");
PrintTo(D342Stream,"        try: os.fsync(directory_fd)\n");
PrintTo(D342Stream,"        finally: os.close(directory_fd)\n");
PrintTo(D342Stream,"except BaseException:\n");
PrintTo(D342Stream,"    try: os.unlink(temporary)\n");
PrintTo(D342Stream,"    except FileNotFoundError: pass\n");
PrintTo(D342Stream,"    raise\n");
PrintTo(D342Stream,"PY\n");
PrintTo(D342Stream,"mode=\${D972_V8_MODE:-PRODUCTION}\n");
PrintTo(D342Stream,"selftest_receipt=\${D972_V8_SELFTEST_RECEIPT:-",D342SelftestReceipt,"}\n");
PrintTo(D342Stream,"resume=\${D972_V8_RESUME:-}\n");
PrintTo(D342Stream,"resume_manifest=\${D972_V8_RESUME_MANIFEST:-}\n");
PrintTo(D342Stream,"if [ -n \"$resume\" ] && [ -z \"$resume_manifest\" ]; then exit 1; fi\n");
PrintTo(D342Stream,"resume_args=(); if [ -n \"$resume\" ]; then resume_args+=(--resume \"$resume\" --resume-manifest \"$resume_manifest\"); fi\n");
PrintTo(D342Stream,"if [ \"$mode\" = SELFTEST ]; then\n");
PrintTo(D342Stream,"  python3 -u -B ",D342Producer,
 " --mode SELFTEST --source ",D342Raw," --manifest ",D342Manifest,
 " --output ",D342Receipt," --seconds 10800 --workers \"$workers\" > ",
 D342ProducerLog," 2>&1\n");
PrintTo(D342Stream,"else\n");
PrintTo(D342Stream,"python3 -u -B ",D342Producer,
 " --mode PRODUCTION --source ",D342Raw," --manifest ",D342Manifest,
 " --selftest-receipt \"$selftest_receipt\" \"\${resume_args[@]}\"",
 " --output ",D342Receipt," --seconds 10800 --workers \"$workers\" > ",
 D342ProducerLog," 2>&1\n");
PrintTo(D342Stream,"  test -s \"$selftest_receipt\"\n");
PrintTo(D342Stream,"fi\n");
PrintTo(D342Stream,"test -s ",D342Receipt," -a -s ",D342ProducerLog,"\n");
PrintTo(D342Stream,"test \"$(grep -c '^",D342ProducerPrefix," ' ",
 D342ProducerLog,")\" -eq 1\n");
PrintTo(D342Stream,"grep -E '^",D342ProducerPrefix," ' ",D342ProducerLog,
 " | sed 's/^",D342ProducerPrefix," //' > ",D342ProducerTerminal,"\n");
PrintTo(D342Stream,"python3 -u -B ",D342Checker," --receipt ",D342Receipt,
 " --verdict ",D342Verdict," > ",D342CheckerLog," 2>&1\n");
PrintTo(D342Stream,"test -s ",D342Verdict," -a -s ",D342CheckerLog,"\n");
PrintTo(D342Stream,"test \"$(grep -c '^",D342CheckerPrefix," ' ",
 D342CheckerLog,")\" -eq 1\n");
PrintTo(D342Stream,"grep -E '^",D342CheckerPrefix," ' ",D342CheckerLog,
 " | sed 's/^",D342CheckerPrefix," //' > ",D342CheckerTerminal,"\n");
PrintTo(D342Stream,"test \"$(wc -l < ",D342ProducerTerminal,")\" -eq 1\n");
PrintTo(D342Stream,"test \"$(wc -l < ",D342CheckerTerminal,")\" -eq 1\n");
PrintTo(D342Stream,"cmp -s ",D342ProducerTerminal," ",D342CheckerTerminal,"\n");
PrintTo(D342Stream,"terminal=$(tr -d '\\n' < ",D342ProducerTerminal,")\n");
PrintTo(D342Stream,"case \"$terminal\" in\n");
PrintTo(D342Stream,"  ",D342Selftest,") test ! -e ",D342Checkpoint," ;;\n");
PrintTo(D342Stream,"  ",D342Common,") test ! -e ",D342Checkpoint," ;;\n");
PrintTo(D342Stream,"  UNKNOWN_INPUT:*) [[ \"$terminal\" =~ ^UNKNOWN_INPUT:[-A-Za-z0-9_.=,+:]+$ ]] && test ! -e ",D342Checkpoint," ;;\n");
PrintTo(D342Stream,"  UNKNOWN_RESOURCE:phase=*) [[ \"$terminal\" =~ ^UNKNOWN_RESOURCE:phase=[A-Za-z0-9_]+:cap=[A-Za-z0-9_]+:value=[0-9]+([.][0-9]+)?:limit=[0-9]+([.][0-9]+)?$ ]] && ( test -s ",D342Checkpoint," || grep -Fq '\"checkpoint_required\":false' ",D342Receipt," ) ;;\n");
PrintTo(D342Stream,"  *) exit 1 ;;\n");
PrintTo(D342Stream,"esac\n");
PrintTo(D342Stream,"printf '%s' '",D342Sentinel,"' > ",D342OK,"\n");
CloseStream(D342Stream);;

Exec(Concatenation("bash ",D342Shell));;
D342Observed:=D342Read(D342OK);;
if D342Observed<>D342Sentinel then Error("task349 sentinel mismatch"); fi;
Print(D342Sentinel,"\n");
