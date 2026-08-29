#############################################################################
## Task380 R07 A0/v12c deterministic SELFTEST_BOOTSTRAP artifact driver.
## ASCII only.  V12c has no production or resume entry point.
#############################################################################
D380P0:="ci/in/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.manifest.v1.json";;
D380Producer:="search/d972_r07_history_free_positive_fast_resume_v12d.py";;
D380Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_v12d.py";;
D380Fixture:="search/certs/d972_r07_history_free_positive_fast_resume_selftest_v12c_20260829.json";;
D380Zip:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip";;
D380Member:="d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json";;
D380Raw:="ci/resume/d972_r07_history_free_positive_fast_resume_selftest_v12c.raw.json";;
D380Receipt:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.receipt.json";;
D380Verdict:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.verdict.json";;
D380ProducerLog:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.producer.log";;
D380CheckerLog:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.checker.log";;
D380ProducerTerminal:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.producer.terminal";;
D380CheckerTerminal:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.checker.terminal";;
D380Shell:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.driver.sh";;
D380SentinelPath:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.artifact.ok";;
D380Artifact:="V12C_SELFTEST_BOOTSTRAP_ARTIFACT";;
D380ProducerLine:=Concatenation("V12C_PRODUCER_TERMINAL ",D380Artifact);;
D380CheckerLine:=Concatenation("V12C_CHECKER_TERMINAL ",D380Artifact);;
D380Sentinel:="V12C_SELFTEST_BOOTSTRAP_ARTIFACT_READY";;

if not IsBound(D972_R07_A0_V12C_MODE) then
  Error("task380 explicit D972_R07_A0_V12C_MODE binding required");
fi;
if not IsString(D972_R07_A0_V12C_MODE) or
   D972_R07_A0_V12C_MODE<>"SELFTEST_BOOTSTRAP" then
  Error("task380 production/resume/unknown mode forbidden");
fi;

D380Pins:=[
 [D380P0,11476,"24fbc1f9d7a7be3c96e1a56d4eb97d0aa5ccca9233f1e552088e9848bc081d74"],
 [D380Producer,342850,"cd78b2c7d38da9a18e636a2917880c135329501b8e5af1aa9fb3dd7a9a46a628"],
 [D380Checker,298456,"4d4750162af04cd4961e5872c9538ef13723e6d6635361568f6487a94ed35046"],
 [D380Fixture,22785,"6fb7fe92c3cf93f54e44f9f26c3e920d131dbc626fc826d8b5bb4745bf67c8ec"],
 ["sol/audit_r07_task298_six_hour_cancel_no_artifact_v279.md",3844,"f669705e93a5ad3c84fb94a5b7f8ec4cf3cedd103df1e0b1d78460e9c8b1f5c9"],
 ["sol/sol_reply_337_r07_task325_v6_code_performance_audit_v1.md",42611,"035f3d987746f9662fb66da512889da7ad4f7ad899a3cc768e626093ce050f4a"],
 ["ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip",5001811,"f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566"],
 ["sol/luna_task_342_r07_a0_v7_fast_positive_resume.md",15393,"9fca7eb266b433436f44a25f0b984d6941c5a1696e960a80e062c5abefcc028d"],
 ["search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py",33409,"f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f"],
 ["search/d972_b345_joint_kernel_qstar_closure_v1.py",67945,"06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"],
 ["ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json",2166036,"1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"],
 ["search/d972_r07_positive_common_word_colgen_v1.py",123870,"47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"],
 ["ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json",1328,"6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302"],
 ["search/d972_b345_seedspan_triple4_v1.py",535219,"fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"],
 ["search/d972_b345_triple_cube_raw_lambda_census_v1.py",126942,"d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"],
 ["search/d972_b345_target6_dual_colgen_v2.py",444497,"b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7"],
 ["sol/proof_r07_history_free_positive_common_word_verifier_v265.md",10122,"fd30ccb2458691ec7844d304f220a4be7d704259318c452f928f8088552ecb0a"],
 ["sol/proof_r07_two_way_basis_checkpoint_resume_v275.md",7662,"51febdaadcdf9130af4dd0586969f28f533ff3e9d06d883841aa115410dd40ea"],
 ["sol/proof_r07_triangular_checkpoint_basis_resume_v276.md",5571,"5765aec25e08e687841451d3707ba16e0f3e2c6c4d9de6c120e92bdafe071abb"],
 ["sol/proof_r07_boundary_first_lazy_runtime_resume_v277.md",9070,"2539fa530195b7c5fe7035d2261301ed85c471af2df313fd33fb01e96df9a56d"],
 ["sol/proof_r07_selected_support_positive_replay_v278.md",7055,"f9dcb97c86e401bd96a92805b6c31428483d624874388bcc0439d1f7dc2f390b"],
 ["ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json",231570,"3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"],
 ["search/d972_r07_all_seven_raw_bridge_preflight_v1.py",60306,"1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa"],
 ["search/d972_r07_all_seven_extension_section_census_v1.py",66109,"878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"],
 ["crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py",84980,"4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"],
 ["ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.json",757,"e6a45a34353ce1fb54c99b4f9cbc8b106f34bfc751dd50044f2a79da72cad5e5"],
 ["ci/in/d972_r07_all_seven_extension_section_census_v1.manifest.json",349,"de62e5e55a2e348a3cce297764f7ff4bfedc10ebe2545f22cbc1551f15e1adc1"],
 ["ci/in/d972_r07_all_seven_extension_section_census_v1.json",13649089,"715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41"],
 ["ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.recovery.manifest.json",2035,"41d2cb72614ce7e2d5b2d7a9000e861414da1c749876b3d51f1ccf2ca63390a8"],
 ["ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.recovery.manifest.v2.json",2690,"67dd555f6e0f943d0161ef2f2c8124b4cc31c9167846b45b43fd2001f5fbba3f"],
 ["sol/luna_reply_176_r07_all_seven_extension_section_census_v1.md",47164,"aa173122310e33910d546bd3e02a98a6bf16aea9d3aad066b7d49976098ebb0c"],
 ["search/d972_r07_full_e4_joint_orbit_preflight_v7.py",21918,"92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed"]
];;
D380RawPin:=[D380Raw,86368039,
 "c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab"];;

D380Read:=function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task380 missing/nonempty gate ",path); fi;
  return raw;
end;;

D380Pin:=function(row)
  local raw;
  raw:=D380Read(row[1]);;
  if Length(raw)<>row[2] or HexSHA256(raw)<>row[3] then
    Error("task380 physical pin drift ",row[1]);
  fi;
end;;

for D380Row in D380Pins do D380Pin(D380Row);; od;

if not IsDirectoryPath("ci/out") then
  if CreateDir("ci/out")=fail then Error("task380 cannot create ci/out"); fi;
fi;
if not IsDirectoryPath("ci/resume") then
  if CreateDir("ci/resume")=fail then Error("task380 cannot create ci/resume"); fi;
fi;
D380StaleRoots:=[
 ["ci/out","d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c"],
 ["ci/resume","d972_r07_history_free_positive_fast_resume_selftest_v12c"]
];;
for D380Root in D380StaleRoots do
  D380Contents:=DirectoryContents(D380Root[1]);;
  if D380Contents=fail then Error("task380 stale scan unavailable ",D380Root[1]); fi;
  for D380Name in D380Contents do
    if PositionSublist(D380Name,D380Root[2])=1 then
      Error("task380 stale v12c output ",D380Root[1],"/",D380Name);
    fi;
  od;
od;

D380Outputs:=[D380Raw,D380Receipt,D380Verdict,D380ProducerLog,
 D380CheckerLog,D380ProducerTerminal,D380CheckerTerminal,D380Shell,
 D380SentinelPath];;
if Length(D380Outputs)<>Length(Set(D380Outputs)) then
  Error("task380 duplicate transport path");
fi;

D380Stream:=OutputTextFile(D380Shell,false);;
if D380Stream=fail then Error("task380 shell open"); fi;
SetPrintFormattingStatus(D380Stream,false);;
PrintTo(D380Stream,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D380Stream,"test \"$(uname -s)\" = Linux\n");
PrintTo(D380Stream,"test \"$(uname -m)\" = x86_64\n");
PrintTo(D380Stream,"for command in python3 timeout grep sed cmp uname wc; do command -v \"$command\" >/dev/null; done\n");
PrintTo(D380Stream,"producer_tmp='",D380ProducerLog,".tmp'\n");
PrintTo(D380Stream,"checker_tmp='",D380CheckerLog,".tmp'\n");
PrintTo(D380Stream,"producer_terminal_tmp='",D380ProducerTerminal,".tmp'\n");
PrintTo(D380Stream,"checker_terminal_tmp='",D380CheckerTerminal,".tmp'\n");
PrintTo(D380Stream,"cleanup_owned() {\n");
PrintTo(D380Stream,"python3 -B - '",D380Raw,"' '",D380Raw,".tmp' '",D380Receipt,"' '",D380Verdict,"' \"$producer_tmp\" \"$checker_tmp\" \"$producer_terminal_tmp\" \"$checker_terminal_tmp\" '",D380ProducerLog,"' '",D380CheckerLog,"' '",D380ProducerTerminal,"' '",D380CheckerTerminal,"' '",D380SentinelPath,"' '",D380SentinelPath,".tmp' <<'PY'\n");
PrintTo(D380Stream,"import os, sys\n");
PrintTo(D380Stream,"failures = []\n");
PrintTo(D380Stream,"for path in sys.argv[1:]:\n");
PrintTo(D380Stream,"    directory = os.path.dirname(path) or '.'; name = os.path.basename(path)\n");
PrintTo(D380Stream,"    try: directory_fd = os.open(directory, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0))\n");
PrintTo(D380Stream,"    except BaseException as exc: failures.append(path + ':dir:' + type(exc).__name__); continue\n");
PrintTo(D380Stream,"    try:\n");
PrintTo(D380Stream,"        try: os.unlink(name, dir_fd=directory_fd); os.fsync(directory_fd)\n");
PrintTo(D380Stream,"        except FileNotFoundError: pass\n");
PrintTo(D380Stream,"        except BaseException as exc: failures.append(path + ':' + type(exc).__name__)\n");
PrintTo(D380Stream,"    finally: os.close(directory_fd)\n");
PrintTo(D380Stream,"if failures: raise SystemExit('task380 cleanup rollback failure ' + ','.join(failures))\n");
PrintTo(D380Stream,"PY\n");
PrintTo(D380Stream,"}\n");
PrintTo(D380Stream,"trap cleanup_owned EXIT\n");
PrintTo(D380Stream,"python3 -B - '",D380Zip,"' '",D380Raw,"' <<'PY'\n");
PrintTo(D380Stream,"import hashlib, os, stat, sys, zipfile\n");
PrintTo(D380Stream,"source, output = sys.argv[1:]\n");
PrintTo(D380Stream,"expected_archive_bytes = 5001811\n");
PrintTo(D380Stream,"expected_archive_sha = 'f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566'\n");
PrintTo(D380Stream,"expected_name = '",D380Member,"'\n");
PrintTo(D380Stream,"expected_size = 86368039\n");
PrintTo(D380Stream,"expected_sha = 'c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab'\n");
PrintTo(D380Stream,"temporary = output + '.tmp'\n");
PrintTo(D380Stream,"directory = os.path.dirname(output) or '.'\n");
PrintTo(D380Stream,"directory_fd = os.open(directory, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0))\n");
PrintTo(D380Stream,"parent_before = os.fstat(directory_fd); named_parent = os.lstat(directory)\n");
PrintTo(D380Stream,"if not stat.S_ISDIR(parent_before.st_mode) or stat.S_ISLNK(named_parent.st_mode) or (parent_before.st_dev, parent_before.st_ino, parent_before.st_mode) != (named_parent.st_dev, named_parent.st_ino, named_parent.st_mode):\n");
PrintTo(D380Stream,"    raise SystemExit('task380 raw publication parent identity')\n");
PrintTo(D380Stream,"temporary_visible = False; output_visible = False; success = False\n");
PrintTo(D380Stream,"flags = os.O_RDONLY | getattr(os, 'O_CLOEXEC', 0) | getattr(os, 'O_NOFOLLOW', 0)\n");
PrintTo(D380Stream,"fd = os.open(source, flags)\n");
PrintTo(D380Stream,"try:\n");
PrintTo(D380Stream,"    before = os.fstat(fd)\n");
PrintTo(D380Stream,"    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size != expected_archive_bytes:\n");
PrintTo(D380Stream,"        raise SystemExit('task380 archive physical owner gate')\n");
PrintTo(D380Stream,"    owner = os.fdopen(fd, 'rb', closefd=False)\n");
PrintTo(D380Stream,"    archive_digest = hashlib.sha256()\n");
PrintTo(D380Stream,"    while True:\n");
PrintTo(D380Stream,"        block = owner.read(1048576)\n");
PrintTo(D380Stream,"        if not block: break\n");
PrintTo(D380Stream,"        archive_digest.update(block)\n");
PrintTo(D380Stream,"    if archive_digest.hexdigest() != expected_archive_sha:\n");
PrintTo(D380Stream,"        raise SystemExit('task380 archive digest gate')\n");
PrintTo(D380Stream,"    owner.seek(0)\n");
PrintTo(D380Stream,"    with zipfile.ZipFile(owner, 'r') as archive:\n");
PrintTo(D380Stream,"        infos = archive.infolist()\n");
PrintTo(D380Stream,"        if len(infos) != 1 or infos[0].filename != expected_name or infos[0].is_dir() or infos[0].file_size != expected_size:\n");
PrintTo(D380Stream,"            raise SystemExit('task380 sole exact archive member gate')\n");
PrintTo(D380Stream,"        digest = hashlib.sha256(); size = 0\n");
PrintTo(D380Stream,"        temp_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_CLOEXEC', 0) | getattr(os, 'O_NOFOLLOW', 0)\n");
PrintTo(D380Stream,"        temp_fd = os.open(os.path.basename(temporary), temp_flags, 0o600, dir_fd=directory_fd); temporary_visible = True\n");
PrintTo(D380Stream,"        with archive.open(infos[0], 'r') as incoming, os.fdopen(temp_fd, 'wb') as outgoing:\n");
PrintTo(D380Stream,"            while True:\n");
PrintTo(D380Stream,"                block = incoming.read(1048576)\n");
PrintTo(D380Stream,"                if not block: break\n");
PrintTo(D380Stream,"                outgoing.write(block); digest.update(block); size += len(block)\n");
PrintTo(D380Stream,"            outgoing.flush(); os.fsync(outgoing.fileno())\n");
PrintTo(D380Stream,"    after = os.fstat(fd); named_after = os.lstat(source)\n");
PrintTo(D380Stream,"    if stat.S_ISLNK(named_after.st_mode) or (before.st_dev, before.st_ino, before.st_mode, before.st_size, before.st_nlink, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_mode, after.st_size, after.st_nlink, after.st_mtime_ns) or (after.st_dev, after.st_ino, after.st_mode, after.st_size, after.st_nlink, after.st_mtime_ns) != (named_after.st_dev, named_after.st_ino, named_after.st_mode, named_after.st_size, named_after.st_nlink, named_after.st_mtime_ns):\n");
PrintTo(D380Stream,"        raise SystemExit('task380 archive TOCTOU gate')\n");
PrintTo(D380Stream,"    if size != expected_size or digest.hexdigest() != expected_sha:\n");
PrintTo(D380Stream,"        raise SystemExit('task380 raw member digest gate')\n");
PrintTo(D380Stream,"    temp_stat = os.stat(os.path.basename(temporary), dir_fd=directory_fd, follow_symlinks=False)\n");
PrintTo(D380Stream,"    os.link(os.path.basename(temporary), os.path.basename(output), src_dir_fd=directory_fd, dst_dir_fd=directory_fd, follow_symlinks=False); output_visible = True\n");
PrintTo(D380Stream,"    verify_fd = os.open(os.path.basename(output), flags, dir_fd=directory_fd)\n");
PrintTo(D380Stream,"    try:\n");
PrintTo(D380Stream,"        final_stat = os.fstat(verify_fd); verify = hashlib.sha256(); verify_size = 0\n");
PrintTo(D380Stream,"        if (temp_stat.st_dev, temp_stat.st_ino, temp_stat.st_size) != (final_stat.st_dev, final_stat.st_ino, final_stat.st_size): raise SystemExit('task380 raw final identity')\n");
PrintTo(D380Stream,"        while True:\n");
PrintTo(D380Stream,"            block = os.read(verify_fd, 1048576)\n");
PrintTo(D380Stream,"            if not block: break\n");
PrintTo(D380Stream,"            verify.update(block); verify_size += len(block)\n");
PrintTo(D380Stream,"        if verify_size != expected_size or verify.hexdigest() != expected_sha: raise SystemExit('task380 raw final digest')\n");
PrintTo(D380Stream,"        os.fsync(verify_fd)\n");
PrintTo(D380Stream,"    finally: os.close(verify_fd)\n");
PrintTo(D380Stream,"    parent_after = os.fstat(directory_fd)\n");
PrintTo(D380Stream,"    if (parent_before.st_dev, parent_before.st_ino, parent_before.st_mode) != (parent_after.st_dev, parent_after.st_ino, parent_after.st_mode): raise SystemExit('task380 raw parent changed')\n");
PrintTo(D380Stream,"    os.fsync(directory_fd)\n");
PrintTo(D380Stream,"    os.unlink(os.path.basename(temporary), dir_fd=directory_fd); temporary_visible = False; os.fsync(directory_fd); success = True\n");
PrintTo(D380Stream,"finally:\n");
PrintTo(D380Stream,"    os.close(fd)\n");
PrintTo(D380Stream,"    rollback = []\n");
PrintTo(D380Stream,"    if not success and output_visible:\n");
PrintTo(D380Stream,"        try: os.unlink(os.path.basename(output), dir_fd=directory_fd); os.fsync(directory_fd); output_visible = False\n");
PrintTo(D380Stream,"        except BaseException as exc: rollback.append('final:' + type(exc).__name__)\n");
PrintTo(D380Stream,"    if temporary_visible:\n");
PrintTo(D380Stream,"        try: os.unlink(os.path.basename(temporary), dir_fd=directory_fd); os.fsync(directory_fd); temporary_visible = False\n");
PrintTo(D380Stream,"        except BaseException as exc: rollback.append('temp:' + type(exc).__name__)\n");
PrintTo(D380Stream,"    os.close(directory_fd)\n");
PrintTo(D380Stream,"    if rollback: raise SystemExit('task380 raw rollback failure ' + ','.join(rollback))\n");
PrintTo(D380Stream,"PY\n");
PrintTo(D380Stream,"timeout --foreground 9900s python3 -u -B '",D380Producer,
 "' --mode SELFTEST_BOOTSTRAP --source '",D380Raw,"' --manifest '",D380P0,
 "' --output '",D380Receipt,"' --seconds 9600 --workers 4 > \"$producer_tmp\" 2>&1\n");
PrintTo(D380Stream,"test -s '",D380Receipt,"' -a -s \"$producer_tmp\"\n");
PrintTo(D380Stream,"timeout --foreground 5700s python3 -u -B '",D380Checker,
 "' --mode SELFTEST_BOOTSTRAP --manifest '",D380P0,"' --receipt '",D380Receipt,
 "' --verdict '",D380Verdict,"' > \"$checker_tmp\" 2>&1\n");
PrintTo(D380Stream,"test -s '",D380Verdict,"' -a -s \"$checker_tmp\"\n");
PrintTo(D380Stream,"test \"$(grep -c '^V12C_PRODUCER_TERMINAL ' \"$producer_tmp\")\" -eq 1\n");
PrintTo(D380Stream,"test \"$(grep -Fxc '",D380ProducerLine,"' \"$producer_tmp\")\" -eq 1\n");
PrintTo(D380Stream,"grep -Fx '",D380ProducerLine,"' \"$producer_tmp\" | sed 's/^V12C_PRODUCER_TERMINAL //' > \"$producer_terminal_tmp\"\n");
PrintTo(D380Stream,"test \"$(grep -c '^V12C_CHECKER_TERMINAL ' \"$checker_tmp\")\" -eq 1\n");
PrintTo(D380Stream,"test \"$(grep -Fxc '",D380CheckerLine,"' \"$checker_tmp\")\" -eq 1\n");
PrintTo(D380Stream,"grep -Fx '",D380CheckerLine,"' \"$checker_tmp\" | sed 's/^V12C_CHECKER_TERMINAL //' > \"$checker_terminal_tmp\"\n");
PrintTo(D380Stream,"test \"$(wc -l < \"$producer_terminal_tmp\")\" -eq 1\n");
PrintTo(D380Stream,"test \"$(wc -l < \"$checker_terminal_tmp\")\" -eq 1\n");
PrintTo(D380Stream,"cmp -s \"$producer_terminal_tmp\" \"$checker_terminal_tmp\"\n");
PrintTo(D380Stream,"grep -Fqx '",D380Artifact,"' \"$producer_terminal_tmp\"\n");
PrintTo(D380Stream,"publish() {\n");
PrintTo(D380Stream,"python3 -B - \"$1\" \"$2\" <<'PY'\n");
PrintTo(D380Stream,"import os, stat, sys\n");
PrintTo(D380Stream,"source, target = sys.argv[1:]\n");
PrintTo(D380Stream,"directory = os.path.dirname(target) or '.'\n");
PrintTo(D380Stream,"if (os.path.dirname(source) or '.') != directory: raise SystemExit('task380 log cross-directory publication')\n");
PrintTo(D380Stream,"directory_fd = os.open(directory, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0))\n");
PrintTo(D380Stream,"source_name = os.path.basename(source); target_name = os.path.basename(target)\n");
PrintTo(D380Stream,"source_visible = True; target_visible = False; success = False\n");
PrintTo(D380Stream,"try:\n");
PrintTo(D380Stream,"    parent_before = os.fstat(directory_fd); source_stat = os.stat(source_name, dir_fd=directory_fd, follow_symlinks=False)\n");
PrintTo(D380Stream,"    if not stat.S_ISREG(source_stat.st_mode) or source_stat.st_nlink != 1: raise SystemExit('task380 log source owner')\n");
PrintTo(D380Stream,"    try: os.stat(target_name, dir_fd=directory_fd, follow_symlinks=False); raise SystemExit('task380 stale log target')\n");
PrintTo(D380Stream,"    except FileNotFoundError: pass\n");
PrintTo(D380Stream,"    os.link(source_name, target_name, src_dir_fd=directory_fd, dst_dir_fd=directory_fd, follow_symlinks=False); target_visible = True\n");
PrintTo(D380Stream,"    verify_fd = os.open(target_name, os.O_RDONLY | getattr(os, 'O_CLOEXEC', 0) | getattr(os, 'O_NOFOLLOW', 0), dir_fd=directory_fd)\n");
PrintTo(D380Stream,"    try:\n");
PrintTo(D380Stream,"        final_stat = os.fstat(verify_fd)\n");
PrintTo(D380Stream,"        if (source_stat.st_dev, source_stat.st_ino, source_stat.st_size) != (final_stat.st_dev, final_stat.st_ino, final_stat.st_size): raise SystemExit('task380 log final identity')\n");
PrintTo(D380Stream,"        os.fsync(verify_fd)\n");
PrintTo(D380Stream,"    finally: os.close(verify_fd)\n");
PrintTo(D380Stream,"    parent_after = os.fstat(directory_fd)\n");
PrintTo(D380Stream,"    if (parent_before.st_dev, parent_before.st_ino, parent_before.st_mode) != (parent_after.st_dev, parent_after.st_ino, parent_after.st_mode): raise SystemExit('task380 log parent changed')\n");
PrintTo(D380Stream,"    os.fsync(directory_fd); os.unlink(source_name, dir_fd=directory_fd); source_visible = False; os.fsync(directory_fd)\n");
PrintTo(D380Stream,"    final_fd = os.open(target_name, os.O_RDONLY | getattr(os, 'O_CLOEXEC', 0) | getattr(os, 'O_NOFOLLOW', 0), dir_fd=directory_fd)\n");
PrintTo(D380Stream,"    try:\n");
PrintTo(D380Stream,"        retained = os.fstat(final_fd)\n");
PrintTo(D380Stream,"        if not stat.S_ISREG(retained.st_mode) or retained.st_nlink != 1 or (source_stat.st_dev, source_stat.st_ino, source_stat.st_size) != (retained.st_dev, retained.st_ino, retained.st_size): raise SystemExit('task380 retained log identity')\n");
PrintTo(D380Stream,"        os.fsync(final_fd)\n");
PrintTo(D380Stream,"    finally: os.close(final_fd)\n");
PrintTo(D380Stream,"    os.fsync(directory_fd); success = True\n");
PrintTo(D380Stream,"finally:\n");
PrintTo(D380Stream,"    rollback = []\n");
PrintTo(D380Stream,"    if not success and target_visible:\n");
PrintTo(D380Stream,"        try: os.unlink(target_name, dir_fd=directory_fd); os.fsync(directory_fd); target_visible = False\n");
PrintTo(D380Stream,"        except BaseException as exc: rollback.append('final:' + type(exc).__name__)\n");
PrintTo(D380Stream,"    if not success and source_visible:\n");
PrintTo(D380Stream,"        try: os.unlink(source_name, dir_fd=directory_fd); os.fsync(directory_fd); source_visible = False\n");
PrintTo(D380Stream,"        except BaseException as exc: rollback.append('temp:' + type(exc).__name__)\n");
PrintTo(D380Stream,"    os.close(directory_fd)\n");
PrintTo(D380Stream,"    if rollback: raise SystemExit('task380 log rollback failure ' + ','.join(rollback))\n");
PrintTo(D380Stream,"PY\n");
PrintTo(D380Stream,"}\n");
PrintTo(D380Stream,"publish \"$producer_tmp\" '",D380ProducerLog,"'\n");
PrintTo(D380Stream,"publish \"$checker_tmp\" '",D380CheckerLog,"'\n");
PrintTo(D380Stream,"publish \"$producer_terminal_tmp\" '",D380ProducerTerminal,"'\n");
PrintTo(D380Stream,"publish \"$checker_terminal_tmp\" '",D380CheckerTerminal,"'\n");
PrintTo(D380Stream,"timeout --foreground 1500s python3 -B - '",D380P0,"' '",D380Receipt,
 "' '",D380Verdict,"' '",D380SentinelPath,"' '",D380Raw,"' <<'PY'\n");
PrintTo(D380Stream,"import hashlib, json, os, signal, stat, sys, time\n");
PrintTo(D380Stream,"p0_path, receipt_path, verdict_path, sentinel, raw_path = sys.argv[1:]\n");
PrintTo(D380Stream,"artifact = 'V12C_SELFTEST_BOOTSTRAP_ARTIFACT'\n");
PrintTo(D380Stream,"placeholder = 'TO_BE_GENERATED_BY_AUDITED_V12C_SELFTEST'\n");
PrintTo(D380Stream,"false_claims = {'common_word': False, 'finite_common_word': False, 'separator': False, 'negative': False, 'cofinal_lift': False, 'fake': False, 'ihara_witness': False}\n");
PrintTo(D380Stream,"artifact_started = time.monotonic(); artifact_internal_seconds = 1200.0\n");
PrintTo(D380Stream,"def deadline():\n");
PrintTo(D380Stream,"    if time.monotonic() - artifact_started > artifact_internal_seconds: raise SystemExit('task380 artifact internal deadline')\n");
PrintTo(D380Stream,"def artifact_alarm(_signum, _frame): raise SystemExit('task380 artifact signal deadline')\n");
PrintTo(D380Stream,"if not hasattr(signal, 'setitimer'): raise SystemExit('task380 artifact signal unavailable')\n");
PrintTo(D380Stream,"signal.signal(signal.SIGALRM, artifact_alarm); signal.setitimer(signal.ITIMER_REAL, artifact_internal_seconds, 0.0)\n");
PrintTo(D380Stream,"def canonical(value):\n");
PrintTo(D380Stream,"    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')\n");
PrintTo(D380Stream,"def digest(raw): return hashlib.sha256(raw).hexdigest()\n");
PrintTo(D380Stream,"def need(condition, reason):\n");
PrintTo(D380Stream,"    if not condition: raise SystemExit('task380 artifact gate: ' + reason)\n");
PrintTo(D380Stream,"def read_json_owner(path, maximum):\n");
PrintTo(D380Stream,"    flags = os.O_RDONLY | getattr(os, 'O_CLOEXEC', 0) | getattr(os, 'O_NOFOLLOW', 0)\n");
PrintTo(D380Stream,"    fd = os.open(path, flags)\n");
PrintTo(D380Stream,"    try:\n");
PrintTo(D380Stream,"        before = os.fstat(fd)\n");
PrintTo(D380Stream,"        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and 0 < before.st_size <= maximum, 'physical owner ' + path)\n");
PrintTo(D380Stream,"        parts = []\n");
PrintTo(D380Stream,"        remaining = before.st_size\n");
PrintTo(D380Stream,"        while remaining:\n");
PrintTo(D380Stream,"            deadline()\n");
PrintTo(D380Stream,"            block = os.read(fd, min(1048576, remaining))\n");
PrintTo(D380Stream,"            need(bool(block), 'short read ' + path)\n");
PrintTo(D380Stream,"            parts.append(block); remaining -= len(block)\n");
PrintTo(D380Stream,"        need(not os.read(fd, 1), 'long read ' + path)\n");
PrintTo(D380Stream,"        after = os.fstat(fd); path_after = os.lstat(path)\n");
PrintTo(D380Stream,"        left = (before.st_dev, before.st_ino, before.st_size, before.st_nlink, before.st_mtime_ns)\n");
PrintTo(D380Stream,"        right = (after.st_dev, after.st_ino, after.st_size, after.st_nlink, after.st_mtime_ns)\n");
PrintTo(D380Stream,"        named = (path_after.st_dev, path_after.st_ino, path_after.st_size, path_after.st_nlink, path_after.st_mtime_ns)\n");
PrintTo(D380Stream,"        need(left == right == named and not stat.S_ISLNK(path_after.st_mode), 'TOCTOU ' + path)\n");
PrintTo(D380Stream,"    finally: os.close(fd)\n");
PrintTo(D380Stream,"    raw = b''.join(parts); owner_digest = digest(raw); owner_bytes = len(raw)\n");
PrintTo(D380Stream,"    try: value = json.loads(raw.decode('ascii'))\n");
PrintTo(D380Stream,"    except (UnicodeError, json.JSONDecodeError) as exc: raise SystemExit('task380 artifact JSON ' + path) from exc\n");
PrintTo(D380Stream,"    need(type(value) is dict and raw == canonical(value) + b'\\n', 'canonical physical JSON ' + path)\n");
PrintTo(D380Stream,"    del raw, parts\n");
PrintTo(D380Stream,"    return value, {'bytes': owner_bytes, 'sha256': owner_digest}\n");
PrintTo(D380Stream,"def check_sealed(value, label):\n");
PrintTo(D380Stream,"    body = dict(value); self_claim = body.pop('self_digest', None)\n");
PrintTo(D380Stream,"    need(type(self_claim) is str and digest(canonical(body)) == self_claim, label + ' self seal')\n");
PrintTo(D380Stream,"    semantic_claim = body.pop('semantic_digest', None)\n");
PrintTo(D380Stream,"    need(type(semantic_claim) is str and digest(canonical(body)) == semantic_claim, label + ' semantic digest')\n");
PrintTo(D380Stream,"p0, p0_owner = read_json_owner(p0_path, 16777216)\n");
PrintTo(D380Stream,"receipt, receipt_owner = read_json_owner(receipt_path, 536870912)\n");
PrintTo(D380Stream,"p0_body = dict(p0); p0_self = p0_body.pop('self_digest_sha256', None)\n");
PrintTo(D380Stream,"need(type(p0_self) is str and digest(canonical(p0_body)) == p0_self, 'P0 self seal')\n");
PrintTo(D380Stream,"need(p0.get('mode') == 'SELFTEST_BOOTSTRAP' and p0.get('status') == 'COMPLETE' and p0.get('execution') == 'UNEXECUTED', 'P0 envelope')\n");
PrintTo(D380Stream,"need(p0.get('candidate_only') is True and p0.get('production_authorized') is False and p0.get('resume_authorized') is False and p0.get('acceptance_preregistration') is False and p0.get('requires_v12c_physical_pin') is True, 'P0 authority')\n");
PrintTo(D380Stream,"need(p0.get('sources') == {}, 'P0 one-way empty executable source graph')\n");
PrintTo(D380Stream,"frozen_paths = [row['path'] for row in p0['frozen_authorities'].values()]\n");
PrintTo(D380Stream,"need(len(frozen_paths) == len(set(frozen_paths)) and frozen_paths.count('search/certs/d972_r07_history_free_positive_fast_resume_selftest_v12c_20260829.json') == 1, 'P0 unique frozen physical owners')\n");
PrintTo(D380Stream,"for label in ('R', 'V'):\n");
PrintTo(D380Stream,"    row = p0['prospective_outputs'][label]\n");
PrintTo(D380Stream,"    need(all(row[field] == placeholder for field in ('bytes', 'sha256', 'self_digest', 'semantic_digest')), 'P0 prospective ' + label)\n");
PrintTo(D380Stream,"check_sealed(receipt, 'R')\n");
PrintTo(D380Stream,"r_expected = set(p0['constructors']['R']['deterministic_field_set']) | {'semantic_digest', 'self_digest'}\n");
PrintTo(D380Stream,"need(set(receipt) == r_expected, 'R constructor field set')\n");
PrintTo(D380Stream,"for value, schema, execution in ((receipt, 'd972-r07-history-free-positive-fast-resume/v12c/selftest-bootstrap', 'SELFTEST_BOOTSTRAP_COMPLETE_CANDIDATE'),):\n");
PrintTo(D380Stream,"    need(value.get('schema') == schema and value.get('status') == 'CANDIDATE_ONLY' and value.get('terminal') == artifact and value.get('mode') == 'SELFTEST_BOOTSTRAP' and value.get('execution') == execution, 'candidate envelope')\n");
PrintTo(D380Stream,"    need(value.get('candidate_only') is True and value.get('production_authorized') is False and value.get('requires_v12c_physical_pin') is True and value.get('claims') == false_claims and value.get('no_acceptance_or_negative_claim') is True and 'checkpoint' not in value, 'forbidden claims')\n");
PrintTo(D380Stream,"p0_public = {'path': p0['manifest_path'], 'bytes': p0_owner['bytes'], 'sha256': p0_owner['sha256'], 'self_digest_sha256': p0_self}\n");
PrintTo(D380Stream,"need(receipt.get('p0') == p0_public, 'R P0 physical binding')\n");
PrintTo(D380Stream,"need(receipt.get('p0_sources') == p0['sources'], 'R byte-exact v12c source binding')\n");
PrintTo(D380Stream,"need(receipt.get('frozen_authorities') == p0['frozen_authorities'], 'R frozen authority binding')\n");
PrintTo(D380Stream,"snapshots = dict(p0['frozen_authorities']); snapshots.pop('raw_checkpoint'); snapshots.pop('checkpoint_archive')\n");
PrintTo(D380Stream,"need(receipt.get('source_snapshots') == snapshots, 'R physical source snapshot binding')\n");
PrintTo(D380Stream,"raw_row = p0['frozen_authorities']['raw_checkpoint']\n");
PrintTo(D380Stream,"need(receipt.get('source') == {'path': raw_row['path'], 'member': '",D380Member,"', 'bytes': raw_row['bytes'], 'sha256': raw_row['sha256'], 'parsed_once': True}, 'raw checkpoint binding')\n");
PrintTo(D380Stream,"need(receipt.get('production_and_resume') == 'FORBIDDEN_PENDING_INDEPENDENT_AUDIT', 'R audit gate')\n");
PrintTo(D380Stream,"producer_complete = receipt.get('selftest', {}).get('complete_mutation_ledger')\n");
PrintTo(D380Stream,"need(type(producer_complete) is list and len(producer_complete) == 75 and receipt['selftest'].get('complete_mutation_ledger_sha256') == digest(canonical(producer_complete)), 'R complete 75-case ledger')\n");
PrintTo(D380Stream,"receipt_summary = {'self_digest': receipt['self_digest'], 'semantic_digest': receipt['semantic_digest'], 'p0': receipt['p0'], 'p0_sources': receipt['p0_sources'], 'frozen_authorities': receipt['frozen_authorities'], 'source_snapshots': receipt['source_snapshots'], 'final_heavy_identity_sha256': receipt.get('final_heavy_identity_sha256'), 'final_heavy_carrier_sha256': digest(canonical(receipt.get('final_heavy_carrier'))), 'h_final': receipt.get('h_final'), 'producer_measurements': [digest(canonical(row)) for row in producer_complete]}\n");
PrintTo(D380Stream,"receipt.clear(); deadline()\n");
PrintTo(D380Stream,"verdict, verdict_owner = read_json_owner(verdict_path, 536870912)\n");
PrintTo(D380Stream,"check_sealed(verdict, 'V')\n");
PrintTo(D380Stream,"v_expected = set(p0['constructors']['V']['deterministic_field_set']) | {'semantic_digest', 'self_digest'}\n");
PrintTo(D380Stream,"need(set(verdict) == v_expected, 'V constructor field set')\n");
PrintTo(D380Stream,"need(verdict.get('schema') == 'd972-r07-history-free-positive-fast-resume/v12c/verdict' and verdict.get('status') == 'CANDIDATE_ONLY' and verdict.get('terminal') == artifact and verdict.get('mode') == 'SELFTEST_BOOTSTRAP' and verdict.get('execution') == 'SELFTEST_CHECKER_COMPLETE_CANDIDATE', 'V candidate envelope')\n");
PrintTo(D380Stream,"need(verdict.get('candidate_only') is True and verdict.get('production_authorized') is False and verdict.get('requires_v12c_physical_pin') is True and verdict.get('claims') == false_claims and verdict.get('no_acceptance_or_negative_claim') is True and 'checkpoint' not in verdict, 'V forbidden claims')\n");
PrintTo(D380Stream,"need(verdict.get('p0') == p0_public and verdict.get('p0_sources') == p0['sources'] and verdict.get('frozen_authorities') == p0['frozen_authorities'] and verdict.get('source_snapshots') == snapshots, 'V P0/source binding')\n");
PrintTo(D380Stream,"need(verdict.get('receipt_bytes') == receipt_owner['bytes'] and verdict.get('receipt_sha256') == receipt_owner['sha256'] and verdict.get('receipt_self_digest') == receipt_summary['self_digest'] and verdict.get('receipt_semantic_digest') == receipt_summary['semantic_digest'], 'V physical R binding')\n");
PrintTo(D380Stream,"projection = verdict.get('receipt_physical')\n");
PrintTo(D380Stream,"need(type(projection) is dict and projection.get('logical_case_path') == 'receipt' and projection.get('owner_kind') == 'regular' and projection.get('byte_length') == receipt_owner['bytes'] and projection.get('content_sha256') == receipt_owner['sha256'], 'V independent physical projection')\n");
PrintTo(D380Stream,"need(projection.get('link_count_before') == 1 and projection.get('link_count_after') == 1 and projection.get('symlink_or_reparse') is False and projection.get('single_open_handle') is True and projection.get('opened_handle_stable') is True and projection.get('pathname_matches_opened_handle') is True and projection.get('substitution_detected') is False and projection.get('first_typed_rejection') is None, 'V physical projection gates')\n");
PrintTo(D380Stream,"need(projection.get('canonical_before_sha256') == receipt_owner['sha256'] and projection.get('canonical_after_sha256') == receipt_owner['sha256'], 'V physical projection digest')\n");
PrintTo(D380Stream,"raw_rebuild = verdict.get('independent_raw_reconstruction')\n");
PrintTo(D380Stream,"need(type(raw_rebuild) is dict and raw_rebuild.get('parsed_once') is True and raw_rebuild.get('basis_annihilation') is True and raw_rebuild.get('rank_before') == 2896 and raw_rebuild.get('rank_after') == 2897, 'V independent raw epoch')\n");
PrintTo(D380Stream,"need(raw_rebuild.get('target_pairing') in (1, 2) and raw_rebuild.get('target_pairing') == raw_rebuild.get('remainder_pairing') and type(raw_rebuild.get('selected_coordinate')) is int, 'V independent dual selection')\n");
PrintTo(D380Stream,"comparison = verdict.get('mutation_ledger', {}).get('producer_checker_complete_comparison')\n");
PrintTo(D380Stream,"need(type(comparison) is dict and comparison.get('case_count') == 75 and comparison.get('group_order') == ['triangular', 'boundary', 'selected_correction', 'positive', 'physical', 'phase', 'phase_positive'] and comparison.get('both_measurement_ledgers_retained') is True and type(comparison.get('pairs')) is list and len(comparison['pairs']) == 75, 'V complete 75-case comparison')\n");
PrintTo(D380Stream,"need(all(row.get('contract_fields_exact') is True and len(row.get('producer_physical_digest', '')) == 64 and len(row.get('checker_physical_digest', '')) == 64 and len(row.get('producer_event_trace_digest', '')) == 64 and len(row.get('checker_event_trace_digest', '')) == 64 for row in comparison['pairs']), 'V measured 75-case identities')\n");
PrintTo(D380Stream,"checker_complete = verdict.get('mutation_ledger', {}).get('complete')\n");
PrintTo(D380Stream,"need(type(checker_complete) is list and len(checker_complete) == 75 and verdict['mutation_ledger'].get('complete_sha256') == digest(canonical(checker_complete)), 'V checker complete ledger seal')\n");
PrintTo(D380Stream,"need([row['producer_measurement_sha256'] for row in comparison['pairs']] == receipt_summary['producer_measurements'] and [row['checker_measurement_sha256'] for row in comparison['pairs']] == [digest(canonical(row)) for row in checker_complete], 'R/V exact measured ledger comparison')\n");
PrintTo(D380Stream,"need(verdict.get('final_heavy_identity_sha256') == receipt_summary['final_heavy_identity_sha256'] and digest(canonical(verdict.get('final_heavy_carrier'))) == receipt_summary['final_heavy_carrier_sha256'] and verdict.get('h_final') == receipt_summary['h_final'], 'V heavy carrier binding')\n");
PrintTo(D380Stream,"def rehash_owner(path, expected):\n");
PrintTo(D380Stream,"    deadline(); h = hashlib.sha256(); size = 0\n");
PrintTo(D380Stream,"    flags = os.O_RDONLY | getattr(os, 'O_CLOEXEC', 0) | getattr(os, 'O_NOFOLLOW', 0)\n");
PrintTo(D380Stream,"    fd = os.open(path, flags)\n");
PrintTo(D380Stream,"    try:\n");
PrintTo(D380Stream,"        before = os.fstat(fd)\n");
PrintTo(D380Stream,"        named_before = os.lstat(path)\n");
PrintTo(D380Stream,"        need(stat.S_ISREG(before.st_mode) and not stat.S_ISLNK(named_before.st_mode) and before.st_nlink == 1, 'post-validation physical owner ' + path)\n");
PrintTo(D380Stream,"        while True:\n");
PrintTo(D380Stream,"            deadline(); block = os.read(fd, 1048576)\n");
PrintTo(D380Stream,"            if not block: break\n");
PrintTo(D380Stream,"            h.update(block); size += len(block)\n");
PrintTo(D380Stream,"        after = os.fstat(fd); named_after = os.lstat(path); os.fsync(fd)\n");
PrintTo(D380Stream,"        identity = lambda row: (row.st_dev, row.st_ino, row.st_mode, row.st_size, row.st_nlink, row.st_mtime_ns)\n");
PrintTo(D380Stream,"        need(identity(before) == identity(named_before) == identity(after) == identity(named_after), 'post-validation TOCTOU ' + path)\n");
PrintTo(D380Stream,"    finally: os.close(fd)\n");
PrintTo(D380Stream,"    need(size == expected['bytes'] and h.hexdigest() == expected['sha256'], 'post-validation rehash ' + path)\n");
PrintTo(D380Stream,"rehash_owner(receipt_path, receipt_owner); rehash_owner(verdict_path, verdict_owner)\n");
PrintTo(D380Stream,"deadline()\n");
PrintTo(D380Stream,"temporary = sentinel + '.tmp'\n");
PrintTo(D380Stream,"directory = os.path.dirname(sentinel) or '.'; temp_name = os.path.basename(temporary); final_name = os.path.basename(sentinel)\n");
PrintTo(D380Stream,"directory_fd = os.open(directory, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0))\n");
PrintTo(D380Stream,"temporary_visible = False; final_visible = False; success = False\n");
PrintTo(D380Stream,"try:\n");
PrintTo(D380Stream,"    parent_before = os.fstat(directory_fd); named_parent = os.lstat(directory)\n");
PrintTo(D380Stream,"    need(stat.S_ISDIR(parent_before.st_mode) and not stat.S_ISLNK(named_parent.st_mode) and (parent_before.st_dev, parent_before.st_ino, parent_before.st_mode) == (named_parent.st_dev, named_parent.st_ino, named_parent.st_mode), 'sentinel parent identity')\n");
PrintTo(D380Stream,"    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_CLOEXEC', 0) | getattr(os, 'O_NOFOLLOW', 0)\n");
PrintTo(D380Stream,"    fd = os.open(temp_name, flags, 0o600, dir_fd=directory_fd); temporary_visible = True\n");
PrintTo(D380Stream,"    try:\n");
PrintTo(D380Stream,"        payload = b'V12C_SELFTEST_BOOTSTRAP_ARTIFACT_READY'; view = memoryview(payload)\n");
PrintTo(D380Stream,"        while view:\n");
PrintTo(D380Stream,"            count = os.write(fd, view); need(count > 0, 'sentinel short write'); view = view[count:]\n");
PrintTo(D380Stream,"        os.fsync(fd); temp_stat = os.fstat(fd)\n");
PrintTo(D380Stream,"    finally: os.close(fd)\n");
PrintTo(D380Stream,"    os.link(temp_name, final_name, src_dir_fd=directory_fd, dst_dir_fd=directory_fd, follow_symlinks=False); final_visible = True\n");
PrintTo(D380Stream,"    verify_fd = os.open(final_name, os.O_RDONLY | getattr(os, 'O_CLOEXEC', 0) | getattr(os, 'O_NOFOLLOW', 0), dir_fd=directory_fd)\n");
PrintTo(D380Stream,"    try:\n");
PrintTo(D380Stream,"        final_stat = os.fstat(verify_fd); final_raw = os.read(verify_fd, len(payload) + 1)\n");
PrintTo(D380Stream,"        need((temp_stat.st_dev, temp_stat.st_ino, temp_stat.st_size) == (final_stat.st_dev, final_stat.st_ino, final_stat.st_size) and final_raw == payload, 'sentinel final identity')\n");
PrintTo(D380Stream,"        os.fsync(verify_fd)\n");
PrintTo(D380Stream,"    finally: os.close(verify_fd)\n");
PrintTo(D380Stream,"    need((parent_before.st_dev, parent_before.st_ino, parent_before.st_mode) == (os.fstat(directory_fd).st_dev, os.fstat(directory_fd).st_ino, os.fstat(directory_fd).st_mode), 'sentinel parent changed')\n");
PrintTo(D380Stream,"    os.fsync(directory_fd); os.unlink(temp_name, dir_fd=directory_fd); temporary_visible = False; os.fsync(directory_fd); success = True\n");
PrintTo(D380Stream,"finally:\n");
PrintTo(D380Stream,"    rollback = []\n");
PrintTo(D380Stream,"    if not success and final_visible:\n");
PrintTo(D380Stream,"        try: os.unlink(final_name, dir_fd=directory_fd); os.fsync(directory_fd); final_visible = False\n");
PrintTo(D380Stream,"        except BaseException as exc: rollback.append('final:' + type(exc).__name__)\n");
PrintTo(D380Stream,"    if temporary_visible:\n");
PrintTo(D380Stream,"        try: os.unlink(temp_name, dir_fd=directory_fd); os.fsync(directory_fd); temporary_visible = False\n");
PrintTo(D380Stream,"        except BaseException as exc: rollback.append('temp:' + type(exc).__name__)\n");
PrintTo(D380Stream,"    os.close(directory_fd)\n");
PrintTo(D380Stream,"    if rollback: raise SystemExit('task380 sentinel rollback failure ' + ','.join(rollback))\n");
PrintTo(D380Stream,"rehash_owner(raw_path, {'bytes': 86368039, 'sha256': 'c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab'})\n");
PrintTo(D380Stream,"rehash_owner(sentinel, {'bytes': len(payload), 'sha256': digest(payload)})\n");
PrintTo(D380Stream,"PY\n");
PrintTo(D380Stream,"trap - EXIT\n");
CloseStream(D380Stream);;

D380Timeout:=Filename(DirectoriesSystemPrograms(),"timeout");;
D380Bash:=Filename(DirectoriesSystemPrograms(),"bash");;
if D380Timeout=fail or D380Bash=fail then
  Error("task380 status-bearing timeout/bash lookup failed");
fi;
D380Status:=Process(DirectoryCurrent(),D380Timeout,InputTextNone(),
 OutputTextUser(),["--foreground","18000s",D380Bash,D380Shell]);;
if D380Status<>0 then
  Error("task380 status-bearing driver failure status ",D380Status);
fi;
Print(D380Sentinel,"\n");
