#############################################################################
## Task372 R07 A0/v12b deterministic SELFTEST_BOOTSTRAP artifact driver.
## ASCII only.  V12b has no production or resume entry point.
#############################################################################
D372P0:="ci/in/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.manifest.v1.json";;
D372Producer:="search/d972_r07_history_free_positive_fast_resume_v12b.py";;
D372Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_v12b.py";;
D372Fixture:="search/certs/d972_r07_history_free_positive_fast_resume_selftest_v12b_20260829.json";;
D372Zip:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip";;
D372Member:="d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json";;
D372Raw:="ci/resume/d972_r07_history_free_positive_fast_resume_selftest_v12b.raw.json";;
D372Receipt:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.receipt.json";;
D372Verdict:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.verdict.json";;
D372ProducerLog:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.producer.log";;
D372CheckerLog:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.checker.log";;
D372ProducerTerminal:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.producer.terminal";;
D372CheckerTerminal:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.checker.terminal";;
D372Shell:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.driver.sh";;
D372SentinelPath:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.artifact.ok";;
D372Artifact:="V12B_SELFTEST_BOOTSTRAP_ARTIFACT";;
D372ProducerLine:=Concatenation("V12B_PRODUCER_TERMINAL ",D372Artifact);;
D372CheckerLine:=Concatenation("V12B_CHECKER_TERMINAL ",D372Artifact);;
D372Sentinel:="V12B_SELFTEST_BOOTSTRAP_ARTIFACT_READY";;

if not IsBound(D972_R07_A0_V12B_MODE) then
  Error("task372 explicit D972_R07_A0_V12B_MODE binding required");
fi;
if not IsString(D972_R07_A0_V12B_MODE) or
   D972_R07_A0_V12B_MODE<>"SELFTEST_BOOTSTRAP" then
  Error("task372 production/resume/unknown mode forbidden");
fi;

D372Pins:=[
 [D372P0,27295,"ecd722495b02dc48cfa68e3be9751a82664fd895a4b01d185c647b4053fbfbe7"],
 [D372Producer,317154,"614bc65bbb36c0a7504923c9ba7b4700ba04ecb66868d5a90994c65e1577dcd7"],
 [D372Checker,263911,"1b8587de9caabc16f3a51ace1d2ea5a892281d155ea4f4270e830208ec4cd0d0"],
 [D372Fixture,23679,"64a7dd14e26431387f6ff1dd71aad6d977a5db943c4ca42c01fb19477f3a3ddb"],
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
D372RawPin:=[D372Raw,86368039,
 "c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab"];;

D372Read:=function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task372 missing/nonempty gate ",path); fi;
  return raw;
end;;

D372Pin:=function(row)
  local raw;
  raw:=D372Read(row[1]);;
  if Length(raw)<>row[2] or HexSHA256(raw)<>row[3] then
    Error("task372 physical pin drift ",row[1]);
  fi;
end;;

for D372Row in D372Pins do D372Pin(D372Row);; od;

if not IsDirectoryPath("ci/out") then
  if CreateDir("ci/out")=fail then Error("task372 cannot create ci/out"); fi;
fi;
if not IsDirectoryPath("ci/resume") then
  if CreateDir("ci/resume")=fail then Error("task372 cannot create ci/resume"); fi;
fi;
D372StaleRoots:=[
 ["ci/out","d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b"],
 ["ci/resume","d972_r07_history_free_positive_fast_resume_selftest_v12b"]
];;
for D372Root in D372StaleRoots do
  D372Contents:=DirectoryContents(D372Root[1]);;
  if D372Contents=fail then Error("task372 stale scan unavailable ",D372Root[1]); fi;
  for D372Name in D372Contents do
    if PositionSublist(D372Name,D372Root[2])=1 then
      Error("task372 stale v12b output ",D372Root[1],"/",D372Name);
    fi;
  od;
od;

D372Outputs:=[D372Raw,D372Receipt,D372Verdict,D372ProducerLog,
 D372CheckerLog,D372ProducerTerminal,D372CheckerTerminal,D372Shell,
 D372SentinelPath];;
if Length(D372Outputs)<>Length(Set(D372Outputs)) then
  Error("task372 duplicate transport path");
fi;

D372Stream:=OutputTextFile(D372Shell,false);;
if D372Stream=fail then Error("task372 shell open"); fi;
SetPrintFormattingStatus(D372Stream,false);;
PrintTo(D372Stream,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D372Stream,"test \"$(uname -s)\" = Linux\n");
PrintTo(D372Stream,"test \"$(uname -m)\" = x86_64\n");
PrintTo(D372Stream,"for command in python3 timeout grep sed cmp ln rm; do command -v \"$command\" >/dev/null; done\n");
PrintTo(D372Stream,"producer_tmp='",D372ProducerLog,".tmp'\n");
PrintTo(D372Stream,"checker_tmp='",D372CheckerLog,".tmp'\n");
PrintTo(D372Stream,"producer_terminal_tmp='",D372ProducerTerminal,".tmp'\n");
PrintTo(D372Stream,"checker_terminal_tmp='",D372CheckerTerminal,".tmp'\n");
PrintTo(D372Stream,"python3 -B - '",D372Zip,"' '",D372Raw,"' <<'PY'\n");
PrintTo(D372Stream,"import hashlib, os, stat, sys, zipfile\n");
PrintTo(D372Stream,"source, output = sys.argv[1:]\n");
PrintTo(D372Stream,"expected_archive_bytes = 5001811\n");
PrintTo(D372Stream,"expected_archive_sha = 'f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566'\n");
PrintTo(D372Stream,"expected_name = '",D372Member,"'\n");
PrintTo(D372Stream,"expected_size = 86368039\n");
PrintTo(D372Stream,"expected_sha = 'c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab'\n");
PrintTo(D372Stream,"temporary = output + '.tmp'\n");
PrintTo(D372Stream,"flags = os.O_RDONLY | getattr(os, 'O_CLOEXEC', 0) | getattr(os, 'O_NOFOLLOW', 0)\n");
PrintTo(D372Stream,"fd = os.open(source, flags)\n");
PrintTo(D372Stream,"try:\n");
PrintTo(D372Stream,"    before = os.fstat(fd)\n");
PrintTo(D372Stream,"    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size != expected_archive_bytes:\n");
PrintTo(D372Stream,"        raise SystemExit('task372 archive physical owner gate')\n");
PrintTo(D372Stream,"    owner = os.fdopen(fd, 'rb', closefd=False)\n");
PrintTo(D372Stream,"    archive_digest = hashlib.sha256()\n");
PrintTo(D372Stream,"    while True:\n");
PrintTo(D372Stream,"        block = owner.read(1048576)\n");
PrintTo(D372Stream,"        if not block: break\n");
PrintTo(D372Stream,"        archive_digest.update(block)\n");
PrintTo(D372Stream,"    if archive_digest.hexdigest() != expected_archive_sha:\n");
PrintTo(D372Stream,"        raise SystemExit('task372 archive digest gate')\n");
PrintTo(D372Stream,"    owner.seek(0)\n");
PrintTo(D372Stream,"    with zipfile.ZipFile(owner, 'r') as archive:\n");
PrintTo(D372Stream,"        infos = archive.infolist()\n");
PrintTo(D372Stream,"        if len(infos) != 1 or infos[0].filename != expected_name or infos[0].is_dir() or infos[0].file_size != expected_size:\n");
PrintTo(D372Stream,"            raise SystemExit('task372 sole exact archive member gate')\n");
PrintTo(D372Stream,"        digest = hashlib.sha256(); size = 0\n");
PrintTo(D372Stream,"        with archive.open(infos[0], 'r') as incoming, open(temporary, 'xb') as outgoing:\n");
PrintTo(D372Stream,"            while True:\n");
PrintTo(D372Stream,"                block = incoming.read(1048576)\n");
PrintTo(D372Stream,"                if not block: break\n");
PrintTo(D372Stream,"                outgoing.write(block); digest.update(block); size += len(block)\n");
PrintTo(D372Stream,"            outgoing.flush(); os.fsync(outgoing.fileno())\n");
PrintTo(D372Stream,"    after = os.fstat(fd)\n");
PrintTo(D372Stream,"    if (before.st_dev, before.st_ino, before.st_size, before.st_nlink, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_nlink, after.st_mtime_ns):\n");
PrintTo(D372Stream,"        raise SystemExit('task372 archive TOCTOU gate')\n");
PrintTo(D372Stream,"    if size != expected_size or digest.hexdigest() != expected_sha:\n");
PrintTo(D372Stream,"        raise SystemExit('task372 raw member digest gate')\n");
PrintTo(D372Stream,"    os.link(temporary, output)\n");
PrintTo(D372Stream,"    os.unlink(temporary)\n");
PrintTo(D372Stream,"    directory_fd = os.open(os.path.dirname(output) or '.', os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))\n");
PrintTo(D372Stream,"    try: os.fsync(directory_fd)\n");
PrintTo(D372Stream,"    finally: os.close(directory_fd)\n");
PrintTo(D372Stream,"finally:\n");
PrintTo(D372Stream,"    os.close(fd)\n");
PrintTo(D372Stream,"    try: os.unlink(temporary)\n");
PrintTo(D372Stream,"    except FileNotFoundError: pass\n");
PrintTo(D372Stream,"PY\n");
PrintTo(D372Stream,"timeout --foreground 9900s python3 -u -B '",D372Producer,
 "' --mode SELFTEST_BOOTSTRAP --source '",D372Raw,"' --manifest '",D372P0,
 "' --output '",D372Receipt,"' --seconds 9600 --workers 4 > \"$producer_tmp\" 2>&1\n");
PrintTo(D372Stream,"test -s '",D372Receipt,"' -a -s \"$producer_tmp\"\n");
PrintTo(D372Stream,"timeout --foreground 5700s python3 -u -B '",D372Checker,
 "' --mode SELFTEST_BOOTSTRAP --manifest '",D372P0,"' --receipt '",D372Receipt,
 "' --verdict '",D372Verdict,"' > \"$checker_tmp\" 2>&1\n");
PrintTo(D372Stream,"test -s '",D372Verdict,"' -a -s \"$checker_tmp\"\n");
PrintTo(D372Stream,"test \"$(grep -c '^V12B_PRODUCER_TERMINAL ' \"$producer_tmp\")\" -eq 1\n");
PrintTo(D372Stream,"test \"$(grep -Fxc '",D372ProducerLine,"' \"$producer_tmp\")\" -eq 1\n");
PrintTo(D372Stream,"grep -Fx '",D372ProducerLine,"' \"$producer_tmp\" | sed 's/^V12B_PRODUCER_TERMINAL //' > \"$producer_terminal_tmp\"\n");
PrintTo(D372Stream,"test \"$(grep -c '^V12B_CHECKER_TERMINAL ' \"$checker_tmp\")\" -eq 1\n");
PrintTo(D372Stream,"test \"$(grep -Fxc '",D372CheckerLine,"' \"$checker_tmp\")\" -eq 1\n");
PrintTo(D372Stream,"grep -Fx '",D372CheckerLine,"' \"$checker_tmp\" | sed 's/^V12B_CHECKER_TERMINAL //' > \"$checker_terminal_tmp\"\n");
PrintTo(D372Stream,"test \"$(wc -l < \"$producer_terminal_tmp\")\" -eq 1\n");
PrintTo(D372Stream,"test \"$(wc -l < \"$checker_terminal_tmp\")\" -eq 1\n");
PrintTo(D372Stream,"cmp -s \"$producer_terminal_tmp\" \"$checker_terminal_tmp\"\n");
PrintTo(D372Stream,"grep -Fqx '",D372Artifact,"' \"$producer_terminal_tmp\"\n");
PrintTo(D372Stream,"publish() { src=$1; dst=$2; test -f \"$src\"; test ! -e \"$dst\"; ln -- \"$src\" \"$dst\"; rm -- \"$src\"; }\n");
PrintTo(D372Stream,"publish \"$producer_tmp\" '",D372ProducerLog,"'\n");
PrintTo(D372Stream,"publish \"$checker_tmp\" '",D372CheckerLog,"'\n");
PrintTo(D372Stream,"publish \"$producer_terminal_tmp\" '",D372ProducerTerminal,"'\n");
PrintTo(D372Stream,"publish \"$checker_terminal_tmp\" '",D372CheckerTerminal,"'\n");
PrintTo(D372Stream,"timeout --foreground 1500s python3 -B - '",D372P0,"' '",D372Receipt,
 "' '",D372Verdict,"' '",D372SentinelPath,"' <<'PY'\n");
PrintTo(D372Stream,"import hashlib, json, os, stat, sys, time\n");
PrintTo(D372Stream,"p0_path, receipt_path, verdict_path, sentinel = sys.argv[1:]\n");
PrintTo(D372Stream,"artifact = 'V12B_SELFTEST_BOOTSTRAP_ARTIFACT'\n");
PrintTo(D372Stream,"placeholder = 'TO_BE_GENERATED_BY_AUDITED_V12B_SELFTEST'\n");
PrintTo(D372Stream,"false_claims = {'common_word': False, 'finite_common_word': False, 'separator': False, 'negative': False, 'cofinal_lift': False, 'fake': False, 'ihara_witness': False}\n");
PrintTo(D372Stream,"artifact_started = time.monotonic(); artifact_internal_seconds = 1200.0\n");
PrintTo(D372Stream,"def deadline():\n");
PrintTo(D372Stream,"    if time.monotonic() - artifact_started > artifact_internal_seconds: raise SystemExit('task372 artifact internal deadline')\n");
PrintTo(D372Stream,"def canonical(value):\n");
PrintTo(D372Stream,"    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')\n");
PrintTo(D372Stream,"def digest(raw): return hashlib.sha256(raw).hexdigest()\n");
PrintTo(D372Stream,"def need(condition, reason):\n");
PrintTo(D372Stream,"    if not condition: raise SystemExit('task372 artifact gate: ' + reason)\n");
PrintTo(D372Stream,"def read_json_owner(path, maximum):\n");
PrintTo(D372Stream,"    flags = os.O_RDONLY | getattr(os, 'O_CLOEXEC', 0) | getattr(os, 'O_NOFOLLOW', 0)\n");
PrintTo(D372Stream,"    fd = os.open(path, flags)\n");
PrintTo(D372Stream,"    try:\n");
PrintTo(D372Stream,"        before = os.fstat(fd)\n");
PrintTo(D372Stream,"        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and 0 < before.st_size <= maximum, 'physical owner ' + path)\n");
PrintTo(D372Stream,"        parts = []\n");
PrintTo(D372Stream,"        remaining = before.st_size\n");
PrintTo(D372Stream,"        while remaining:\n");
PrintTo(D372Stream,"            deadline()\n");
PrintTo(D372Stream,"            block = os.read(fd, min(1048576, remaining))\n");
PrintTo(D372Stream,"            need(bool(block), 'short read ' + path)\n");
PrintTo(D372Stream,"            parts.append(block); remaining -= len(block)\n");
PrintTo(D372Stream,"        need(not os.read(fd, 1), 'long read ' + path)\n");
PrintTo(D372Stream,"        after = os.fstat(fd); path_after = os.lstat(path)\n");
PrintTo(D372Stream,"        left = (before.st_dev, before.st_ino, before.st_size, before.st_nlink, before.st_mtime_ns)\n");
PrintTo(D372Stream,"        right = (after.st_dev, after.st_ino, after.st_size, after.st_nlink, after.st_mtime_ns)\n");
PrintTo(D372Stream,"        named = (path_after.st_dev, path_after.st_ino, path_after.st_size, path_after.st_nlink, path_after.st_mtime_ns)\n");
PrintTo(D372Stream,"        need(left == right == named and not stat.S_ISLNK(path_after.st_mode), 'TOCTOU ' + path)\n");
PrintTo(D372Stream,"    finally: os.close(fd)\n");
PrintTo(D372Stream,"    raw = b''.join(parts); owner_digest = digest(raw); owner_bytes = len(raw)\n");
PrintTo(D372Stream,"    try: value = json.loads(raw.decode('ascii'))\n");
PrintTo(D372Stream,"    except (UnicodeError, json.JSONDecodeError) as exc: raise SystemExit('task372 artifact JSON ' + path) from exc\n");
PrintTo(D372Stream,"    need(type(value) is dict and raw == canonical(value) + b'\\n', 'canonical physical JSON ' + path)\n");
PrintTo(D372Stream,"    del raw, parts\n");
PrintTo(D372Stream,"    return value, {'bytes': owner_bytes, 'sha256': owner_digest}\n");
PrintTo(D372Stream,"def check_sealed(value, label):\n");
PrintTo(D372Stream,"    body = dict(value); self_claim = body.pop('self_digest', None)\n");
PrintTo(D372Stream,"    need(type(self_claim) is str and digest(canonical(body)) == self_claim, label + ' self seal')\n");
PrintTo(D372Stream,"    semantic_claim = body.pop('semantic_digest', None)\n");
PrintTo(D372Stream,"    need(type(semantic_claim) is str and digest(canonical(body)) == semantic_claim, label + ' semantic digest')\n");
PrintTo(D372Stream,"p0, p0_owner = read_json_owner(p0_path, 16777216)\n");
PrintTo(D372Stream,"receipt, receipt_owner = read_json_owner(receipt_path, 536870912)\n");
PrintTo(D372Stream,"p0_body = dict(p0); p0_self = p0_body.pop('self_digest_sha256', None)\n");
PrintTo(D372Stream,"need(type(p0_self) is str and digest(canonical(p0_body)) == p0_self, 'P0 self seal')\n");
PrintTo(D372Stream,"need(p0.get('mode') == 'SELFTEST_BOOTSTRAP' and p0.get('status') == 'COMPLETE' and p0.get('execution') == 'UNEXECUTED', 'P0 envelope')\n");
PrintTo(D372Stream,"need(p0.get('candidate_only') is True and p0.get('production_authorized') is False and p0.get('resume_authorized') is False and p0.get('acceptance_preregistration') is False and p0.get('requires_v12b_physical_pin') is True, 'P0 authority')\n");
PrintTo(D372Stream,"for label in ('R', 'V'):\n");
PrintTo(D372Stream,"    row = p0['prospective_outputs'][label]\n");
PrintTo(D372Stream,"    need(all(row[field] == placeholder for field in ('bytes', 'sha256', 'self_digest', 'semantic_digest')), 'P0 prospective ' + label)\n");
PrintTo(D372Stream,"check_sealed(receipt, 'R')\n");
PrintTo(D372Stream,"r_expected = set(p0['constructors']['R']['deterministic_field_set']) | {'semantic_digest', 'self_digest'}\n");
PrintTo(D372Stream,"need(set(receipt) == r_expected, 'R constructor field set')\n");
PrintTo(D372Stream,"for value, schema, execution in ((receipt, 'd972-r07-history-free-positive-fast-resume/v12b/selftest-bootstrap', 'SELFTEST_BOOTSTRAP_COMPLETE_CANDIDATE'),):\n");
PrintTo(D372Stream,"    need(value.get('schema') == schema and value.get('status') == 'CANDIDATE_ONLY' and value.get('terminal') == artifact and value.get('mode') == 'SELFTEST_BOOTSTRAP' and value.get('execution') == execution, 'candidate envelope')\n");
PrintTo(D372Stream,"    need(value.get('candidate_only') is True and value.get('production_authorized') is False and value.get('requires_v12b_physical_pin') is True and value.get('claims') == false_claims and value.get('no_acceptance_or_negative_claim') is True and 'checkpoint' not in value, 'forbidden claims')\n");
PrintTo(D372Stream,"p0_public = {'path': p0['manifest_path'], 'semantic_schema': p0['schema'], 'self_digest_sha256': p0_self, 'physical_sha256': p0_owner['sha256']}\n");
PrintTo(D372Stream,"need(receipt.get('p0') == p0_public, 'R P0 physical binding')\n");
PrintTo(D372Stream,"need(receipt.get('p0_sources') == p0['sources'], 'R byte-exact v12b source binding')\n");
PrintTo(D372Stream,"need(receipt.get('frozen_authorities') == p0['frozen_authorities'], 'R frozen authority binding')\n");
PrintTo(D372Stream,"snapshots = dict(p0['frozen_authorities']); snapshots.pop('raw_checkpoint'); snapshots.pop('checkpoint_archive')\n");
PrintTo(D372Stream,"need(receipt.get('source_snapshots') == snapshots, 'R physical source snapshot binding')\n");
PrintTo(D372Stream,"raw_row = p0['frozen_authorities']['raw_checkpoint']\n");
PrintTo(D372Stream,"need(receipt.get('source') == {'path': raw_row['path'], 'member': '",D372Member,"', 'bytes': raw_row['bytes'], 'sha256': raw_row['sha256'], 'parsed_once': True}, 'raw checkpoint binding')\n");
PrintTo(D372Stream,"need(receipt.get('production_and_resume') == 'FORBIDDEN_PENDING_INDEPENDENT_AUDIT', 'R audit gate')\n");
PrintTo(D372Stream,"receipt_summary = {'self_digest': receipt['self_digest'], 'semantic_digest': receipt['semantic_digest'], 'p0': receipt['p0'], 'p0_sources': receipt['p0_sources'], 'frozen_authorities': receipt['frozen_authorities'], 'source_snapshots': receipt['source_snapshots'], 'final_heavy_identity_sha256': receipt.get('final_heavy_identity_sha256'), 'final_heavy_carrier_sha256': digest(canonical(receipt.get('final_heavy_carrier'))), 'h_final': receipt.get('h_final')}\n");
PrintTo(D372Stream,"receipt.clear(); deadline()\n");
PrintTo(D372Stream,"verdict, verdict_owner = read_json_owner(verdict_path, 536870912)\n");
PrintTo(D372Stream,"check_sealed(verdict, 'V')\n");
PrintTo(D372Stream,"v_expected = set(p0['constructors']['V']['deterministic_field_set']) | {'semantic_digest', 'self_digest'}\n");
PrintTo(D372Stream,"need(set(verdict) == v_expected, 'V constructor field set')\n");
PrintTo(D372Stream,"need(verdict.get('schema') == 'd972-r07-history-free-positive-fast-resume/v12b/verdict' and verdict.get('status') == 'CANDIDATE_ONLY' and verdict.get('terminal') == artifact and verdict.get('mode') == 'SELFTEST_BOOTSTRAP' and verdict.get('execution') == 'SELFTEST_CHECKER_COMPLETE_CANDIDATE', 'V candidate envelope')\n");
PrintTo(D372Stream,"need(verdict.get('candidate_only') is True and verdict.get('production_authorized') is False and verdict.get('requires_v12b_physical_pin') is True and verdict.get('claims') == false_claims and verdict.get('no_acceptance_or_negative_claim') is True and 'checkpoint' not in verdict, 'V forbidden claims')\n");
PrintTo(D372Stream,"need(verdict.get('p0') == p0_public and verdict.get('p0_sources') == p0['sources'] and verdict.get('frozen_authorities') == p0['frozen_authorities'] and verdict.get('source_snapshots') == snapshots, 'V P0/source binding')\n");
PrintTo(D372Stream,"need(verdict.get('receipt_bytes') == receipt_owner['bytes'] and verdict.get('receipt_sha256') == receipt_owner['sha256'] and verdict.get('receipt_self_digest') == receipt_summary['self_digest'] and verdict.get('receipt_semantic_digest') == receipt_summary['semantic_digest'], 'V physical R binding')\n");
PrintTo(D372Stream,"projection = verdict.get('receipt_physical')\n");
PrintTo(D372Stream,"need(type(projection) is dict and projection.get('logical_case_path') == 'receipt' and projection.get('owner_kind') == 'regular' and projection.get('byte_length') == receipt_owner['bytes'] and projection.get('content_sha256') == receipt_owner['sha256'], 'V independent physical projection')\n");
PrintTo(D372Stream,"need(projection.get('link_count_before') == 1 and projection.get('link_count_after') == 1 and projection.get('symlink_or_reparse') is False and projection.get('single_open_handle') is True and projection.get('opened_handle_stable') is True and projection.get('pathname_matches_opened_handle') is True and projection.get('substitution_detected') is False and projection.get('first_typed_rejection') is None, 'V physical projection gates')\n");
PrintTo(D372Stream,"need(projection.get('canonical_before_sha256') == receipt_owner['sha256'] and projection.get('canonical_after_sha256') == receipt_owner['sha256'], 'V physical projection digest')\n");
PrintTo(D372Stream,"raw_rebuild = verdict.get('independent_raw_reconstruction')\n");
PrintTo(D372Stream,"need(type(raw_rebuild) is dict and raw_rebuild.get('parsed_once') is True and raw_rebuild.get('basis_annihilation') is True and raw_rebuild.get('rank_before') == 2896 and raw_rebuild.get('rank_after') == 2897, 'V independent raw epoch')\n");
PrintTo(D372Stream,"need(raw_rebuild.get('target_pairing') in (1, 2) and raw_rebuild.get('target_pairing') == raw_rebuild.get('remainder_pairing') and type(raw_rebuild.get('selected_coordinate')) is int, 'V independent dual selection')\n");
PrintTo(D372Stream,"need(verdict.get('final_heavy_identity_sha256') == receipt_summary['final_heavy_identity_sha256'] and digest(canonical(verdict.get('final_heavy_carrier'))) == receipt_summary['final_heavy_carrier_sha256'] and verdict.get('h_final') == receipt_summary['h_final'], 'V heavy carrier binding')\n");
PrintTo(D372Stream,"def rehash_owner(path, expected):\n");
PrintTo(D372Stream,"    deadline(); h = hashlib.sha256(); size = 0\n");
PrintTo(D372Stream,"    flags = os.O_RDONLY | getattr(os, 'O_CLOEXEC', 0) | getattr(os, 'O_NOFOLLOW', 0)\n");
PrintTo(D372Stream,"    fd = os.open(path, flags)\n");
PrintTo(D372Stream,"    try:\n");
PrintTo(D372Stream,"        before = os.fstat(fd)\n");
PrintTo(D372Stream,"        while True:\n");
PrintTo(D372Stream,"            deadline(); block = os.read(fd, 1048576)\n");
PrintTo(D372Stream,"            if not block: break\n");
PrintTo(D372Stream,"            h.update(block); size += len(block)\n");
PrintTo(D372Stream,"        after = os.fstat(fd)\n");
PrintTo(D372Stream,"        need((before.st_dev, before.st_ino, before.st_size, before.st_nlink, before.st_mtime_ns) == (after.st_dev, after.st_ino, after.st_size, after.st_nlink, after.st_mtime_ns), 'post-validation TOCTOU ' + path)\n");
PrintTo(D372Stream,"    finally: os.close(fd)\n");
PrintTo(D372Stream,"    need(size == expected['bytes'] and h.hexdigest() == expected['sha256'], 'post-validation rehash ' + path)\n");
PrintTo(D372Stream,"rehash_owner(receipt_path, receipt_owner); rehash_owner(verdict_path, verdict_owner)\n");
PrintTo(D372Stream,"deadline()\n");
PrintTo(D372Stream,"temporary = sentinel + '.tmp'\n");
PrintTo(D372Stream,"fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_CLOEXEC', 0), 0o600)\n");
PrintTo(D372Stream,"try:\n");
PrintTo(D372Stream,"    payload = b'V12B_SELFTEST_BOOTSTRAP_ARTIFACT_READY'\n");
PrintTo(D372Stream,"    view = memoryview(payload)\n");
PrintTo(D372Stream,"    while view:\n");
PrintTo(D372Stream,"        count = os.write(fd, view)\n");
PrintTo(D372Stream,"        need(count > 0, 'sentinel short write'); view = view[count:]\n");
PrintTo(D372Stream,"    os.fsync(fd)\n");
PrintTo(D372Stream,"finally: os.close(fd)\n");
PrintTo(D372Stream,"try:\n");
PrintTo(D372Stream,"    os.link(temporary, sentinel); os.unlink(temporary)\n");
PrintTo(D372Stream,"    directory_fd = os.open(os.path.dirname(sentinel) or '.', os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))\n");
PrintTo(D372Stream,"    try: os.fsync(directory_fd)\n");
PrintTo(D372Stream,"    finally: os.close(directory_fd)\n");
PrintTo(D372Stream,"except BaseException:\n");
PrintTo(D372Stream,"    try: os.unlink(temporary)\n");
PrintTo(D372Stream,"    except FileNotFoundError: pass\n");
PrintTo(D372Stream,"    raise\n");
PrintTo(D372Stream,"PY\n");
CloseStream(D372Stream);;

Exec(Concatenation("timeout --foreground 18000s bash ",D372Shell));;
D372Pin(D372RawPin);;
D372Observed:=D372Read(D372SentinelPath);;
if D372Observed<>D372Sentinel then Error("task372 artifact sentinel mismatch"); fi;
Print(D372Sentinel,"\n");
