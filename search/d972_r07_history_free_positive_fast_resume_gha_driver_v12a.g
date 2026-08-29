#############################################################################
## Task354 R07 A0/v12a deterministic SELFTEST_BOOTSTRAP artifact driver.
## ASCII only.  V12a has no production or resume entry point.
#############################################################################
D354P0:="ci/in/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12a.manifest.v1.json";;
D354Producer:="search/d972_r07_history_free_positive_fast_resume_v12a.py";;
D354Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_v12a.py";;
D354Fixture:="search/certs/d972_r07_history_free_positive_fast_resume_selftest_v12a_20260829.json";;
D354Zip:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip";;
D354Member:="d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json";;
D354Raw:="ci/resume/d972_r07_history_free_positive_fast_resume_selftest_v12a.raw.json";;
D354Receipt:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12a.receipt.json";;
D354Verdict:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12a.verdict.json";;
D354ProducerLog:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12a.producer.log";;
D354CheckerLog:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12a.checker.log";;
D354ProducerTerminal:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12a.producer.terminal";;
D354CheckerTerminal:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12a.checker.terminal";;
D354Shell:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12a.driver.sh";;
D354SentinelPath:="ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12a.artifact.ok";;
D354Artifact:="V12A_SELFTEST_BOOTSTRAP_ARTIFACT";;
D354ProducerLine:=Concatenation("V12A_PRODUCER_TERMINAL ",D354Artifact);;
D354CheckerLine:=Concatenation("V12A_CHECKER_TERMINAL ",D354Artifact);;
D354Sentinel:="V12A_SELFTEST_BOOTSTRAP_ARTIFACT_READY";;

if not IsBound(D972_R07_A0_V12A_MODE) then
  Error("task354 explicit D972_R07_A0_V12A_MODE binding required");
fi;
if not IsString(D972_R07_A0_V12A_MODE) or
   D972_R07_A0_V12A_MODE<>"SELFTEST_BOOTSTRAP" then
  Error("task354 production/resume/unknown mode forbidden");
fi;

D354Pins:=[
 [D354P0,10058,"f127bac60d4fb41d984fcfdc57f77a32cc88e32905207009e6758ec913d1d52d"],
 [D354Producer,304762,"0e938caeb83b4e65440495b0f50952135d4bfca4309aef38f16c00f50d2905cf"],
 [D354Checker,237150,"b3d95ae7bb7c82878121a5a386e934b425259ef5ea00e80f31d7202d827750a0"],
 [D354Fixture,22094,"6a87bf608bf0a392ff77d3aacbe813a0cc01f54d67bd5d346fb75ee1e7000ffc"],
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
D354RawPin:=[D354Raw,86368039,
 "c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab"];;

D354Read:=function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task354 missing/nonempty gate ",path); fi;
  return raw;
end;;

D354Pin:=function(row)
  local raw;
  raw:=D354Read(row[1]);;
  if Length(raw)<>row[2] or HexSHA256(raw)<>row[3] then
    Error("task354 physical pin drift ",row[1]);
  fi;
end;;

for D354Row in D354Pins do D354Pin(D354Row);; od;

Exec("mkdir -p ci/out ci/resume");;
D354StaleRoots:=[
 ["ci/out","d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12a"],
 ["ci/resume","d972_r07_history_free_positive_fast_resume_selftest_v12a"]
];;
for D354Root in D354StaleRoots do
  D354Contents:=DirectoryContents(D354Root[1]);;
  if D354Contents=fail then Error("task354 stale scan unavailable ",D354Root[1]); fi;
  for D354Name in D354Contents do
    if PositionSublist(D354Name,D354Root[2])=1 then
      Error("task354 stale v12a output ",D354Root[1],"/",D354Name);
    fi;
  od;
od;

D354Outputs:=[D354Raw,D354Receipt,D354Verdict,D354ProducerLog,
 D354CheckerLog,D354ProducerTerminal,D354CheckerTerminal,D354Shell,
 D354SentinelPath];;
if Length(D354Outputs)<>Length(Set(D354Outputs)) then
  Error("task354 duplicate transport path");
fi;

D354Stream:=OutputTextFile(D354Shell,false);;
if D354Stream=fail then Error("task354 shell open"); fi;
SetPrintFormattingStatus(D354Stream,false);;
PrintTo(D354Stream,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D354Stream,"producer_tmp='",D354ProducerLog,".tmp'\n");
PrintTo(D354Stream,"checker_tmp='",D354CheckerLog,".tmp'\n");
PrintTo(D354Stream,"producer_terminal_tmp='",D354ProducerTerminal,".tmp'\n");
PrintTo(D354Stream,"checker_terminal_tmp='",D354CheckerTerminal,".tmp'\n");
PrintTo(D354Stream,"python3 -B - '",D354Zip,"' '",D354Raw,"' <<'PY'\n");
PrintTo(D354Stream,"import hashlib, os, stat, sys, zipfile\n");
PrintTo(D354Stream,"source, output = sys.argv[1:]\n");
PrintTo(D354Stream,"expected_archive_bytes = 5001811\n");
PrintTo(D354Stream,"expected_archive_sha = 'f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566'\n");
PrintTo(D354Stream,"expected_name = '",D354Member,"'\n");
PrintTo(D354Stream,"expected_size = 86368039\n");
PrintTo(D354Stream,"expected_sha = 'c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab'\n");
PrintTo(D354Stream,"temporary = output + '.tmp'\n");
PrintTo(D354Stream,"flags = os.O_RDONLY | getattr(os, 'O_CLOEXEC', 0) | getattr(os, 'O_NOFOLLOW', 0)\n");
PrintTo(D354Stream,"fd = os.open(source, flags)\n");
PrintTo(D354Stream,"try:\n");
PrintTo(D354Stream,"    before = os.fstat(fd)\n");
PrintTo(D354Stream,"    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size != expected_archive_bytes:\n");
PrintTo(D354Stream,"        raise SystemExit('task354 archive physical owner gate')\n");
PrintTo(D354Stream,"    owner = os.fdopen(fd, 'rb', closefd=False)\n");
PrintTo(D354Stream,"    archive_digest = hashlib.sha256()\n");
PrintTo(D354Stream,"    while True:\n");
PrintTo(D354Stream,"        block = owner.read(1048576)\n");
PrintTo(D354Stream,"        if not block: break\n");
PrintTo(D354Stream,"        archive_digest.update(block)\n");
PrintTo(D354Stream,"    if archive_digest.hexdigest() != expected_archive_sha:\n");
PrintTo(D354Stream,"        raise SystemExit('task354 archive digest gate')\n");
PrintTo(D354Stream,"    owner.seek(0)\n");
PrintTo(D354Stream,"    with zipfile.ZipFile(owner, 'r') as archive:\n");
PrintTo(D354Stream,"        infos = archive.infolist()\n");
PrintTo(D354Stream,"        if len(infos) != 1 or infos[0].filename != expected_name or infos[0].is_dir() or infos[0].file_size != expected_size:\n");
PrintTo(D354Stream,"            raise SystemExit('task354 sole exact archive member gate')\n");
PrintTo(D354Stream,"        digest = hashlib.sha256(); size = 0\n");
PrintTo(D354Stream,"        with archive.open(infos[0], 'r') as incoming, open(temporary, 'xb') as outgoing:\n");
PrintTo(D354Stream,"            while True:\n");
PrintTo(D354Stream,"                block = incoming.read(1048576)\n");
PrintTo(D354Stream,"                if not block: break\n");
PrintTo(D354Stream,"                outgoing.write(block); digest.update(block); size += len(block)\n");
PrintTo(D354Stream,"            outgoing.flush(); os.fsync(outgoing.fileno())\n");
PrintTo(D354Stream,"    after = os.fstat(fd)\n");
PrintTo(D354Stream,"    if (before.st_dev, before.st_ino, before.st_size, before.st_nlink, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_nlink, after.st_mtime_ns):\n");
PrintTo(D354Stream,"        raise SystemExit('task354 archive TOCTOU gate')\n");
PrintTo(D354Stream,"    if size != expected_size or digest.hexdigest() != expected_sha:\n");
PrintTo(D354Stream,"        raise SystemExit('task354 raw member digest gate')\n");
PrintTo(D354Stream,"    os.link(temporary, output)\n");
PrintTo(D354Stream,"    os.unlink(temporary)\n");
PrintTo(D354Stream,"    directory_fd = os.open(os.path.dirname(output) or '.', os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))\n");
PrintTo(D354Stream,"    try: os.fsync(directory_fd)\n");
PrintTo(D354Stream,"    finally: os.close(directory_fd)\n");
PrintTo(D354Stream,"finally:\n");
PrintTo(D354Stream,"    os.close(fd)\n");
PrintTo(D354Stream,"    try: os.unlink(temporary)\n");
PrintTo(D354Stream,"    except FileNotFoundError: pass\n");
PrintTo(D354Stream,"PY\n");
PrintTo(D354Stream,"timeout --foreground 10800s python3 -u -B '",D354Producer,
 "' --mode SELFTEST_BOOTSTRAP --source '",D354Raw,"' --manifest '",D354P0,
 "' --output '",D354Receipt,"' --seconds 10800 --workers 4 > \"$producer_tmp\" 2>&1\n");
PrintTo(D354Stream,"test -s '",D354Receipt,"' -a -s \"$producer_tmp\"\n");
PrintTo(D354Stream,"timeout --foreground 7200s python3 -u -B '",D354Checker,
 "' --mode SELFTEST_BOOTSTRAP --manifest '",D354P0,"' --receipt '",D354Receipt,
 "' --verdict '",D354Verdict,"' > \"$checker_tmp\" 2>&1\n");
PrintTo(D354Stream,"test -s '",D354Verdict,"' -a -s \"$checker_tmp\"\n");
PrintTo(D354Stream,"test \"$(grep -c '^V12A_PRODUCER_TERMINAL ' \"$producer_tmp\")\" -eq 1\n");
PrintTo(D354Stream,"test \"$(grep -Fxc '",D354ProducerLine,"' \"$producer_tmp\")\" -eq 1\n");
PrintTo(D354Stream,"grep -Fx '",D354ProducerLine,"' \"$producer_tmp\" | sed 's/^V12A_PRODUCER_TERMINAL //' > \"$producer_terminal_tmp\"\n");
PrintTo(D354Stream,"test \"$(grep -c '^V12A_CHECKER_TERMINAL ' \"$checker_tmp\")\" -eq 1\n");
PrintTo(D354Stream,"test \"$(grep -Fxc '",D354CheckerLine,"' \"$checker_tmp\")\" -eq 1\n");
PrintTo(D354Stream,"grep -Fx '",D354CheckerLine,"' \"$checker_tmp\" | sed 's/^V12A_CHECKER_TERMINAL //' > \"$checker_terminal_tmp\"\n");
PrintTo(D354Stream,"test \"$(wc -l < \"$producer_terminal_tmp\")\" -eq 1\n");
PrintTo(D354Stream,"test \"$(wc -l < \"$checker_terminal_tmp\")\" -eq 1\n");
PrintTo(D354Stream,"cmp -s \"$producer_terminal_tmp\" \"$checker_terminal_tmp\"\n");
PrintTo(D354Stream,"grep -Fqx '",D354Artifact,"' \"$producer_terminal_tmp\"\n");
PrintTo(D354Stream,"publish() { src=$1; dst=$2; test -f \"$src\"; test ! -e \"$dst\"; ln -- \"$src\" \"$dst\"; rm -- \"$src\"; }\n");
PrintTo(D354Stream,"publish \"$producer_tmp\" '",D354ProducerLog,"'\n");
PrintTo(D354Stream,"publish \"$checker_tmp\" '",D354CheckerLog,"'\n");
PrintTo(D354Stream,"publish \"$producer_terminal_tmp\" '",D354ProducerTerminal,"'\n");
PrintTo(D354Stream,"publish \"$checker_terminal_tmp\" '",D354CheckerTerminal,"'\n");
PrintTo(D354Stream,"timeout --foreground 3600s python3 -B - '",D354P0,"' '",D354Receipt,
 "' '",D354Verdict,"' '",D354SentinelPath,"' <<'PY'\n");
PrintTo(D354Stream,"import hashlib, json, os, stat, sys\n");
PrintTo(D354Stream,"p0_path, receipt_path, verdict_path, sentinel = sys.argv[1:]\n");
PrintTo(D354Stream,"artifact = 'V12A_SELFTEST_BOOTSTRAP_ARTIFACT'\n");
PrintTo(D354Stream,"placeholder = 'TO_BE_GENERATED_BY_AUDITED_V12A_SELFTEST'\n");
PrintTo(D354Stream,"false_claims = {'common_word': False, 'finite_common_word': False, 'separator': False, 'negative': False, 'cofinal_lift': False, 'fake': False, 'ihara_witness': False}\n");
PrintTo(D354Stream,"def canonical(value):\n");
PrintTo(D354Stream,"    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')\n");
PrintTo(D354Stream,"def digest(raw): return hashlib.sha256(raw).hexdigest()\n");
PrintTo(D354Stream,"def need(condition, reason):\n");
PrintTo(D354Stream,"    if not condition: raise SystemExit('task354 artifact gate: ' + reason)\n");
PrintTo(D354Stream,"def read_json_owner(path, maximum):\n");
PrintTo(D354Stream,"    flags = os.O_RDONLY | getattr(os, 'O_CLOEXEC', 0) | getattr(os, 'O_NOFOLLOW', 0)\n");
PrintTo(D354Stream,"    fd = os.open(path, flags)\n");
PrintTo(D354Stream,"    try:\n");
PrintTo(D354Stream,"        before = os.fstat(fd)\n");
PrintTo(D354Stream,"        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and 0 < before.st_size <= maximum, 'physical owner ' + path)\n");
PrintTo(D354Stream,"        parts = []\n");
PrintTo(D354Stream,"        remaining = before.st_size\n");
PrintTo(D354Stream,"        while remaining:\n");
PrintTo(D354Stream,"            block = os.read(fd, min(1048576, remaining))\n");
PrintTo(D354Stream,"            need(bool(block), 'short read ' + path)\n");
PrintTo(D354Stream,"            parts.append(block); remaining -= len(block)\n");
PrintTo(D354Stream,"        need(not os.read(fd, 1), 'long read ' + path)\n");
PrintTo(D354Stream,"        after = os.fstat(fd); path_after = os.lstat(path)\n");
PrintTo(D354Stream,"        left = (before.st_dev, before.st_ino, before.st_size, before.st_nlink, before.st_mtime_ns)\n");
PrintTo(D354Stream,"        right = (after.st_dev, after.st_ino, after.st_size, after.st_nlink, after.st_mtime_ns)\n");
PrintTo(D354Stream,"        named = (path_after.st_dev, path_after.st_ino, path_after.st_size, path_after.st_nlink, path_after.st_mtime_ns)\n");
PrintTo(D354Stream,"        need(left == right == named and not stat.S_ISLNK(path_after.st_mode), 'TOCTOU ' + path)\n");
PrintTo(D354Stream,"    finally: os.close(fd)\n");
PrintTo(D354Stream,"    raw = b''.join(parts)\n");
PrintTo(D354Stream,"    try: value = json.loads(raw.decode('ascii'))\n");
PrintTo(D354Stream,"    except (UnicodeError, json.JSONDecodeError) as exc: raise SystemExit('task354 artifact JSON ' + path) from exc\n");
PrintTo(D354Stream,"    need(type(value) is dict and raw == canonical(value) + b'\\n', 'canonical physical JSON ' + path)\n");
PrintTo(D354Stream,"    return value, raw\n");
PrintTo(D354Stream,"def check_sealed(value, label):\n");
PrintTo(D354Stream,"    body = dict(value); self_claim = body.pop('self_digest', None)\n");
PrintTo(D354Stream,"    need(type(self_claim) is str and digest(canonical(body)) == self_claim, label + ' self seal')\n");
PrintTo(D354Stream,"    semantic_claim = body.pop('semantic_digest', None)\n");
PrintTo(D354Stream,"    need(type(semantic_claim) is str and digest(canonical(body)) == semantic_claim, label + ' semantic digest')\n");
PrintTo(D354Stream,"p0, p0_raw = read_json_owner(p0_path, 16777216)\n");
PrintTo(D354Stream,"receipt, receipt_raw = read_json_owner(receipt_path, 536870912)\n");
PrintTo(D354Stream,"verdict, verdict_raw = read_json_owner(verdict_path, 536870912)\n");
PrintTo(D354Stream,"p0_body = dict(p0); p0_self = p0_body.pop('self_digest_sha256', None)\n");
PrintTo(D354Stream,"need(type(p0_self) is str and digest(canonical(p0_body)) == p0_self, 'P0 self seal')\n");
PrintTo(D354Stream,"need(p0.get('mode') == 'SELFTEST_BOOTSTRAP' and p0.get('status') == 'COMPLETE' and p0.get('execution') == 'UNEXECUTED', 'P0 envelope')\n");
PrintTo(D354Stream,"need(p0.get('candidate_only') is True and p0.get('production_authorized') is False and p0.get('resume_authorized') is False and p0.get('acceptance_preregistration') is False and p0.get('requires_v12b_physical_pin') is True, 'P0 authority')\n");
PrintTo(D354Stream,"for label in ('R', 'V'):\n");
PrintTo(D354Stream,"    row = p0['prospective_outputs'][label]\n");
PrintTo(D354Stream,"    need(all(row[field] == placeholder for field in ('bytes', 'sha256', 'self_digest', 'semantic_digest')), 'P0 prospective ' + label)\n");
PrintTo(D354Stream,"check_sealed(receipt, 'R'); check_sealed(verdict, 'V')\n");
PrintTo(D354Stream,"r_expected = set(p0['constructors']['R']['deterministic_field_set']) | {'semantic_digest', 'self_digest'}\n");
PrintTo(D354Stream,"v_expected = set(p0['constructors']['V']['deterministic_field_set']) | {'semantic_digest', 'self_digest'}\n");
PrintTo(D354Stream,"need(set(receipt) == r_expected and set(verdict) == v_expected, 'constructor field sets')\n");
PrintTo(D354Stream,"for value, schema, execution in ((receipt, 'd972-r07-history-free-positive-fast-resume/v12a/selftest-bootstrap', 'SELFTEST_BOOTSTRAP_COMPLETE_CANDIDATE'), (verdict, 'd972-r07-history-free-positive-fast-resume/v12a/verdict', 'SELFTEST_CHECKER_COMPLETE_CANDIDATE')):\n");
PrintTo(D354Stream,"    need(value.get('schema') == schema and value.get('status') == 'CANDIDATE_ONLY' and value.get('terminal') == artifact and value.get('mode') == 'SELFTEST_BOOTSTRAP' and value.get('execution') == execution, 'candidate envelope')\n");
PrintTo(D354Stream,"    need(value.get('candidate_only') is True and value.get('production_authorized') is False and value.get('requires_v12b_physical_pin') is True and value.get('claims') == false_claims and value.get('no_acceptance_or_negative_claim') is True and 'checkpoint' not in value, 'forbidden claims')\n");
PrintTo(D354Stream,"p0_public = {'path': p0['manifest_path'], 'semantic_schema': p0['schema'], 'self_digest_sha256': p0_self, 'physical_sha256': digest(p0_raw)}\n");
PrintTo(D354Stream,"need(receipt.get('p0') == p0_public and verdict.get('p0') == p0_public, 'P0 physical binding')\n");
PrintTo(D354Stream,"need(receipt.get('p0_sources') == p0['sources'] and verdict.get('p0_sources') == p0['sources'], 'byte-exact v12a source binding')\n");
PrintTo(D354Stream,"need(receipt.get('frozen_authorities') == p0['frozen_authorities'] and verdict.get('frozen_authorities') == p0['frozen_authorities'], 'frozen authority binding')\n");
PrintTo(D354Stream,"snapshots = dict(p0['frozen_authorities']); snapshots.pop('raw_checkpoint'); snapshots.pop('checkpoint_archive')\n");
PrintTo(D354Stream,"need(receipt.get('source_snapshots') == snapshots and verdict.get('source_snapshots') == snapshots, 'physical source snapshot binding')\n");
PrintTo(D354Stream,"raw_row = p0['frozen_authorities']['raw_checkpoint']\n");
PrintTo(D354Stream,"need(receipt.get('source') == {'path': raw_row['path'], 'member': '",D354Member,"', 'bytes': raw_row['bytes'], 'sha256': raw_row['sha256'], 'parsed_once': True}, 'raw checkpoint binding')\n");
PrintTo(D354Stream,"need(receipt.get('production_and_resume') == 'FORBIDDEN_UNTIL_V12B', 'R v12b gate')\n");
PrintTo(D354Stream,"need(verdict.get('receipt_bytes') == len(receipt_raw) and verdict.get('receipt_sha256') == digest(receipt_raw) and verdict.get('receipt_self_digest') == receipt['self_digest'] and verdict.get('receipt_semantic_digest') == receipt['semantic_digest'], 'V physical R binding')\n");
PrintTo(D354Stream,"projection = verdict.get('receipt_physical')\n");
PrintTo(D354Stream,"need(type(projection) is dict and projection.get('logical_case_path') == 'receipt' and projection.get('owner_kind') == 'regular' and projection.get('byte_length') == len(receipt_raw) and projection.get('content_sha256') == digest(receipt_raw), 'V independent physical projection')\n");
PrintTo(D354Stream,"need(projection.get('link_count_before') == 1 and projection.get('link_count_after') == 1 and projection.get('symlink_or_reparse') is False and projection.get('single_open_handle') is True and projection.get('opened_handle_stable') is True and projection.get('pathname_matches_opened_handle') is True and projection.get('substitution_detected') is False and projection.get('first_typed_rejection') is None, 'V physical projection gates')\n");
PrintTo(D354Stream,"need(projection.get('canonical_before_sha256') == digest(receipt_raw) and projection.get('canonical_after_sha256') == digest(receipt_raw), 'V physical projection digest')\n");
PrintTo(D354Stream,"need(verdict.get('final_heavy_identity_sha256') == receipt.get('final_heavy_identity_sha256') and verdict.get('final_heavy_carrier') == receipt.get('final_heavy_carrier') and verdict.get('h_final') == receipt.get('h_final'), 'V heavy carrier binding')\n");
PrintTo(D354Stream,"temporary = sentinel + '.tmp'\n");
PrintTo(D354Stream,"fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_CLOEXEC', 0), 0o600)\n");
PrintTo(D354Stream,"try:\n");
PrintTo(D354Stream,"    payload = b'V12A_SELFTEST_BOOTSTRAP_ARTIFACT_READY'\n");
PrintTo(D354Stream,"    view = memoryview(payload)\n");
PrintTo(D354Stream,"    while view:\n");
PrintTo(D354Stream,"        count = os.write(fd, view)\n");
PrintTo(D354Stream,"        need(count > 0, 'sentinel short write'); view = view[count:]\n");
PrintTo(D354Stream,"    os.fsync(fd)\n");
PrintTo(D354Stream,"finally: os.close(fd)\n");
PrintTo(D354Stream,"try:\n");
PrintTo(D354Stream,"    os.link(temporary, sentinel); os.unlink(temporary)\n");
PrintTo(D354Stream,"    directory_fd = os.open(os.path.dirname(sentinel) or '.', os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))\n");
PrintTo(D354Stream,"    try: os.fsync(directory_fd)\n");
PrintTo(D354Stream,"    finally: os.close(directory_fd)\n");
PrintTo(D354Stream,"except BaseException:\n");
PrintTo(D354Stream,"    try: os.unlink(temporary)\n");
PrintTo(D354Stream,"    except FileNotFoundError: pass\n");
PrintTo(D354Stream,"    raise\n");
PrintTo(D354Stream,"PY\n");
CloseStream(D354Stream);;

Exec(Concatenation("timeout --foreground 21600s bash ",D354Shell));;
D354Pin(D354RawPin);;
D354Observed:=D354Read(D354SentinelPath);;
if D354Observed<>D354Sentinel then Error("task354 artifact sentinel mismatch"); fi;
Print(D354Sentinel,"\n");
