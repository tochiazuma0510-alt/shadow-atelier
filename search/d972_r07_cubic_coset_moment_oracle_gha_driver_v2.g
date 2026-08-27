#############################################################################
## Task 178 cubic/coset moment oracle driver v2.
## ASCII only. Producer and checker are serial and helper-nonshared.
#############################################################################

T178ModeVariable := "D972_R07_CUBIC_COSET_MOMENT_ORACLE_V2_MODE";;
T178ProductionModePreamble := "D972_R07_CUBIC_COSET_MOMENT_ORACLE_V2_MODE:=\"PRODUCTION\";";;
T178SelftestModePreamble := "D972_R07_CUBIC_COSET_MOMENT_ORACLE_V2_MODE:=\"SELFTEST\";";;
T178Producer := "search/d972_r07_cubic_coset_moment_oracle_v2.py";;
T178Checker := "crosscheck/check_d972_r07_cubic_coset_moment_oracle_v2.py";;
T178Fixture := "search/certs/d972_r07_cubic_coset_moment_oracle_selftest_v2_20260827.json";;
T178Receipt := "ci/out/d972_r07_cubic_coset_moment_oracle_receipt_v2.json";;
T178Verdict := "ci/out/d972_r07_cubic_coset_moment_oracle_verdict_v2.json";;
T178ProducerLog := "ci/out/d972_r07_cubic_coset_moment_oracle_producer_v2.log";;
T178CheckerLog := "ci/out/d972_r07_cubic_coset_moment_oracle_checker_v2.log";;
T178Timing := "ci/out/d972_r07_cubic_coset_moment_oracle_timing_v2.txt";;
T178Hashes := "ci/out/d972_r07_cubic_coset_moment_oracle_hashes_v2.txt";;
T178Shell := "ci/out/d972_r07_cubic_coset_moment_oracle_command_v2.sh";;
T178DriverVerdict := "ci/out/d972_r07_cubic_coset_moment_oracle_driver_verdict_v2.txt";;
T178DriverPass := "ci/out/d972_r07_cubic_coset_moment_oracle_driver_pass_v2.done";;
T178StageP := "ci/out/d972_r07_cubic_coset_moment_oracle_producer_v2.done";;
T178StageC := "ci/out/d972_r07_cubic_coset_moment_oracle_checker_v2.done";;
T178StageSP := "ci/out/d972_r07_cubic_coset_moment_oracle_selftest_producer_v2.done";;
T178StageSC := "ci/out/d972_r07_cubic_coset_moment_oracle_selftest_checker_v2.done";;
T178Unknown := "UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED";;
T178SelftestTerminal := "FIXTURE_PASS";;
T178Timeout := 20000;;

T178Read := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task178 missing ",label," ",path); fi;
  return raw;
end;;

T178Count := function(raw,needle)
  local at,n,tail,start;
  if Length(needle)=0 then Error("task178 empty count needle"); fi;
  n:=0;; tail:=raw;;
  while Length(tail)>0 do
    at:=PositionSublist(tail,needle);;
    if at=fail then break; fi;
    n:=n+1;;
    start:=at+Length(needle);;
    if start>Length(tail) then tail:="";
    else tail:=tail{[start..Length(tail)]}; fi;
  od;
  return n;
end;;

T178Pin := function(path,expected_sha,expected_bytes)
  local raw;
  raw:=T178Read(path,"pin");;
  if Length(raw)<>expected_bytes or HexSHA256(raw)<>expected_sha then
    Error("task178 pin drift ",path);
  fi;
  return true;
end;;

T178RejectExisting := function(paths)
  local path;
  if Length(paths)<>Length(Set(paths)) then Error("task178 duplicate output"); fi;
  for path in paths do
    if IsExistingFile(path) then Error("task178 pre-existing output ",path); fi;
  od;
  return true;
end;;

## Immutable task, active erratum/proofs, historical v136, task177, source,
## checker, and fixture pins. Positive prerequisites remain unregistered.
T178Pin("sol/luna_task_178_r07_cubic_coset_moment_oracle_v2.md",
  "35890e33e18d0a6150f1173ef1e078eac3d8cbfb1a67dc5edf39abf9ae261ddb",6640);;
T178Pin("sol/luna_task_178a_r07_cubic_moment_resource_erratum.md",
  "ef5062f76d7198a1eaf31c839703513f74bf4f80fd97ec11816422d0b4b5bcee",3213);;
T178Pin("sol/proof_r07_cubic_character_moment_selector_v134.md",
  "1cd3bc0ba0291ab07570a423e6473a54d9a2d4941e310f11e7a55fa16b709477",9402);;
T178Pin("sol/proof_r07_cubic_moment_exact_resource_cap_v136.md",
  "2af3b250aefed10933284847d39e204570b1fdf805313632988d1d49cb0e4a86",4778);;
T178Pin("sol/proof_r07_coarse_anchor_multi_projection_oracle_v137.md",
  "8674eda702a099885da50b9c3feb664a72f345fa4574cffc138a7e892a3f3a67",7908);;
T178Pin("sol/proof_r07_cubic_moment_resource_cap_erratum_v138.md",
  "9dc94b6de5120e54f3b5a5324fb58a24646ad5917b3bd85c36162af29aa86456",6371);;
T178Pin("search/d972_r07_weighted_cell_colgen_v1.py",
  "d955d7717f55ffca3abb92229b96ce2b8ee092ddae3d5e6c7379df92f3892d2e",29523);;
T178Pin("crosscheck/check_d972_r07_weighted_cell_colgen_v1.py",
  "b4d8d046c6850042e0c74778ff8410d9725ef8d0d9387ddb2f75325a6f72d50e",20157);;
T178Pin("search/d972_r07_weighted_cell_colgen_gha_driver_v1.g",
  "cb32e46412622e55b53859d0e2f2684932204dfdff85477244d1619f9df71304",13670);;
T178Pin("search/certs/d972_r07_weighted_cell_colgen_selftest_v1_20260827.json",
  "d118633552b5d827d62101f063ba9d7d60fd4335f3744169f85f6cbb2b95da8b",4932);;
T178Pin(T178Producer,
  "476329117f6bb4b773b6f51dcc328e23445f09bdd3f6ad2c84bae9aa2daa5f29",42320);;
T178Pin(T178Checker,
  "f62ab833fd566296058fa977fd285432dae6bf80d996aedf05a21f5da9052c13",31150);;
T178Pin(T178Fixture,
  "8a7fb3ae2c389b75e98b5a750ab7a2c2c5bc3f00affca8ac57f8ef67ea829aca",6486);;

T178AssertOne := function(raw,needle,label)
  if T178Count(raw,needle)<>1 then Error("task178 exact marker ",label); fi;
  return true;
end;;

T178WriteDriverPass := function(line)
  local stream;
  stream:=OutputTextFile(T178DriverPass,false);;
  if stream=fail then Error("task178 driver pass open"); fi;
  SetPrintFormattingStatus(stream,false);;
  PrintTo(stream,line,"\n");;
  CloseStream(stream);;
  return true;
end;;

T178WriteEmitter := function()
  local stream,raw;
  stream:=OutputTextFile(T178Shell,false);;
  if stream=fail then Error("task178 emitter open"); fi;
  SetPrintFormattingStatus(stream,false);;
  PrintTo(stream,"#!/usr/bin/env bash\nset -euo pipefail\n");;
  PrintTo(stream,"if [ \"${1:-}\" != '--emit-driver-pass' ] || [ \"$#\" -ne 2 ]; then exit 64; fi\n");;
  PrintTo(stream,"case \"$2\" in\n");;
  PrintTo(stream,"  SELFTEST) d178_mode='SELFTEST'; d178_terminal='FIXTURE_PASS' ;;\n");;
  PrintTo(stream,"  UNKNOWN_INPUT) d178_mode='PRODUCTION'; d178_terminal='UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED' ;;\n");;
  PrintTo(stream,"  *) exit 65 ;;\n");;
  PrintTo(stream,"esac\n");;
  PrintTo(stream,"d178_line=\"R07_CUBIC_COSET_MOMENT_ORACLE_V2_GHA_DRIVER_PASS mode=${d178_mode} terminal=${d178_terminal}\"\n");;
  PrintTo(stream,"case \"$d178_line\" in *$'\\n'*|*$'\\r'*) exit 66 ;; esac\n");;
  PrintTo(stream,"test \"$(printf '%s\\n' \"$d178_line\" | wc -l)\" -eq 1\n");;
  PrintTo(stream,"printf '%s\\n' \"$d178_line\"\n");;
  PrintTo(stream,"exit 0\n");;
  CloseStream(stream);;
  raw:=T178Read(T178Shell,"emitter shell");;
  if T178Count(raw,"\\\n")<>0 then
    Error("task178 emitter contains backslash-newline");
  fi;
  return true;
end;;

T178EmitExternal := function(code)
  if code<>"SELFTEST" and code<>"UNKNOWN_INPUT" then
    Error("task178 emitter code ",code);
  fi;
  Exec(Concatenation("bash ",T178Shell," --emit-driver-pass ",code));;
  return true;
end;;

T178CleanLog := function(raw,label)
  local token;
  for token in ["Traceback (most recent call last):","SyntaxError",
                "AssertionError","PRODUCER_STOP","CHECKER_STOP",
                "Killed"] do
    if T178Count(raw,token)<>0 then Error("task178 bad ",label," ",token); fi;
  od;
  return true;
end;;

T178UnknownReceiptGate := function(raw)
  local required,token;
  required:=["\"schema\":\"d972-r07-cubic-coset-moment-oracle/v2\"",
    "\"status\":\"UNKNOWN_INPUT\"",
    "\"terminal\":\"UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED\"",
    "\"reason\":\"PREREQUISITE_NOT_PINNED\"",
    "\"result\":null","\"self_digest_sha256\":",
    "\"all_seven_solution\":false","\"correction_word\":false",
    "\"separator\":false","\"cofinal_lift\":false",
    "\"fake\":false","\"Ihara_witness\":false",
    "\"resource_theorem\":\"v138_SUPPORT_PARAMETRIC_CAP\"",
    "\"integer_arithmetic\":\"ARBITRARY_PRECISION_REQUIRED\"",
    "\"actual_coordinate_count\":10",
    "\"conditional_norm_formula\":\"2*3^10*N*P_actual\"",
    "\"large_table_allocated\":false",
    "\"v136_per_row_1536\"","\"v136_all_rows_9893376\"",
    "\"v136_unconditional_signed64\"",
    "\"registered_dynamic_ceiling\":null"];;
  for token in required do
    if T178Count(raw,token)<>1 then Error("task178 unknown receipt gate ",token); fi;
  od;
  if T178Count(raw,"R07_CUBIC_COSET_MOMENT_ORACLE_V2_COMMON_WORD")<>0 then
    Error("task178 unknown receipt mixed terminal");
  fi;
  return true;
end;;

T178VerdictGate := function(raw)
  local required,token;
  required:=["\"schema\":\"d972-r07-cubic-coset-moment-oracle/v2/checker-v2\"",
    "\"status\":\"PASS\"",
    "\"terminal\":\"UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED\"",
    "\"receipt_terminal\":\"UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED\"",
    "\"reason\":\"PREREQUISITE_NOT_PINNED\"",
    "\"producer_receipt_sha256\":","\"self_digest_sha256\":"];;
  for token in required do
    if T178Count(raw,token)<>1 then Error("task178 verdict gate ",token); fi;
  od;
  return true;
end;;

T178TerminalAgreement := function(raw_receipt,raw_verdict)
  local receipt_count,verdict_count;
  receipt_count:=T178Count(raw_receipt,
    "\"terminal\":\"UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED\"");;
  verdict_count:=T178Count(raw_verdict,
    "\"receipt_terminal\":\"UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED\"");;
  if receipt_count<>1 or verdict_count<>1 then
    Error("task178 terminal disagreement");
  fi;
  return T178Unknown;
end;;

T178Preamble := Concatenation(
  "timeout 20000s bash -o pipefail -c '",
  "set -euo pipefail; mkdir -p ci/out; ",
  "python3 -B ",T178Producer," --run-oracle --output ",T178Receipt,
  " >",T178ProducerLog," 2>&1; echo T178_PRODUCER_STAGE_DONE >",T178StageP,
  "; python3 -B ",T178Checker," --check --receipt ",T178Receipt,
  " --verdict ",T178Verdict," >",T178CheckerLog,
  " 2>&1; echo T178_CHECKER_STAGE_DONE >",T178StageC,"'");;

T178SelftestPreamble := Concatenation(
  "timeout 1800s bash -o pipefail -c '",
  "set -euo pipefail; mkdir -p ci/out; python3 -B ",T178Producer,
  " --selftest --fixture ",T178Fixture," >",T178ProducerLog,
  " 2>&1; echo T178_SELFTEST_PRODUCER_STAGE_DONE >",T178StageSP,
  "; python3 -B ",T178Checker," --selftest --fixture ",T178Fixture,
  " >",T178CheckerLog," 2>&1; echo T178_SELFTEST_CHECKER_STAGE_DONE >",
  T178StageSC,"'");;

T178RunSelftest := function()
  local rawp,rawc;
  T178RejectExisting([T178ProducerLog,T178CheckerLog,T178StageSP,T178StageSC,
    T178StageP,T178StageC,T178DriverPass,T178Receipt,T178Verdict,T178Hashes,
    T178Shell,T178Timing,T178DriverVerdict]);;
  T178WriteEmitter();;
  T178Exec(T178SelftestPreamble);;
  rawp:=T178Read(T178ProducerLog,"selftest producer log");;
  rawc:=T178Read(T178CheckerLog,"selftest checker log");;
  T178CleanLog(rawp,"producer");; T178CleanLog(rawc,"checker");;
  T178AssertOne(rawp,
    "R07_CUBIC_COSET_MOMENT_ORACLE_V2_PRODUCER_SELFTEST_PASS mutations=17 rejected=17 gamma_coarse_order=3 linked_graph_order=3",
    "producer selftest");;
  T178AssertOne(rawc,
    "R07_CUBIC_COSET_MOMENT_ORACLE_V2_CHECKER_SELFTEST_PASS mutations=17 rejected=17 gamma_coarse_order=3 linked_graph_order=3",
    "checker selftest");;
  T178AssertOne(T178Read(T178StageSP,"producer stage"),
    "T178_SELFTEST_PRODUCER_STAGE_DONE\n","producer stage");;
  T178AssertOne(T178Read(T178StageSC,"checker stage"),
    "T178_SELFTEST_CHECKER_STAGE_DONE\n","checker stage");;
  T178WriteDriverPass(
    "R07_CUBIC_COSET_MOMENT_ORACLE_V2_GHA_DRIVER_PASS mode=SELFTEST terminal=FIXTURE_PASS");;
  T178AssertOne(T178Read(T178DriverPass,"driver selftest pass"),
    "R07_CUBIC_COSET_MOMENT_ORACLE_V2_GHA_DRIVER_PASS mode=SELFTEST terminal=FIXTURE_PASS",
    "driver selftest pass");
  T178EmitExternal("SELFTEST");;
  return true;
end;;

T178RunProduction := function()
  local rawp,rawc,rawr,rawv,terminal,stream;
  T178RejectExisting([T178ProducerLog,T178CheckerLog,T178StageSP,T178StageSC,
    T178StageP,T178StageC,T178DriverPass,T178Receipt,T178Verdict,T178Hashes,
    T178Shell,T178Timing,T178DriverVerdict]);;
  T178WriteEmitter();;
  T178Exec(T178Preamble);;
  rawp:=T178Read(T178ProducerLog,"producer log");;
  rawc:=T178Read(T178CheckerLog,"checker log");;
  rawr:=T178Read(T178Receipt,"receipt");;
  rawv:=T178Read(T178Verdict,"verdict");;
  T178CleanLog(rawp,"producer");; T178CleanLog(rawc,"checker");;
  T178AssertOne(T178Read(T178StageP,"producer stage"),
    "T178_PRODUCER_STAGE_DONE\n","producer stage");;
  T178AssertOne(T178Read(T178StageC,"checker stage"),
    "T178_CHECKER_STAGE_DONE\n","checker stage");;
  T178AssertOne(rawp,
    "R07_CUBIC_COSET_MOMENT_ORACLE_V2_PRODUCER_TERMINAL UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED",
    "producer terminal");;
  T178AssertOne(rawc,
    "R07_CUBIC_COSET_MOMENT_ORACLE_V2_CHECKER_PASS terminal=UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED",
    "checker terminal");;
  terminal:=T178TerminalAgreement(rawr,rawv);;
  if terminal<>T178Unknown then Error("task178 unexpected terminal ",terminal); fi;
  T178UnknownReceiptGate(rawr);; T178VerdictGate(rawv);;
  stream:=OutputTextFile(T178Hashes,false);;
  if stream=fail then Error("task178 hashes open"); fi;
  SetPrintFormattingStatus(stream,false);;
  PrintTo(stream,Concatenation("producer_sha256=",HexSHA256(rawp),
    "\nchecker_sha256=",HexSHA256(rawc),"\nreceipt_sha256=",HexSHA256(rawr),
    "\nverdict_sha256=",HexSHA256(rawv),"\n"));;
  CloseStream(stream);;
  stream:=OutputTextFile(T178DriverVerdict,false);;
  if stream=fail then Error("task178 verdict copy open"); fi;
  SetPrintFormattingStatus(stream,false);; PrintTo(stream,rawv);; CloseStream(stream);;
  stream:=OutputTextFile(T178Timing,false);;
  if stream=fail then Error("task178 timing open"); fi;
  SetPrintFormattingStatus(stream,false);
  PrintTo(stream,"mode=PRODUCTION terminal=UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED timeout_seconds=20000\n");;
  CloseStream(stream);;
  T178WriteDriverPass(
    "R07_CUBIC_COSET_MOMENT_ORACLE_V2_GHA_DRIVER_PASS mode=PRODUCTION terminal=UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED");;
  T178AssertOne(T178Read(T178DriverPass,"driver production pass"),
    "R07_CUBIC_COSET_MOMENT_ORACLE_V2_GHA_DRIVER_PASS mode=PRODUCTION terminal=UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED",
    "driver production pass");
  T178EmitExternal("UNKNOWN_INPUT");;
  return true;
end;;

T178Exec := function(command)
  Exec(command);;
  return true;
end;;

T178Mode := "UNBOUND";;
T178ModeRuns := 0;;
T178BindMode := function(mode)
  if T178Mode<>"UNBOUND" then Error("task178 mode rebind"); fi;
  if mode<>"PRODUCTION" and mode<>"SELFTEST" then Error("task178 invalid mode ",mode); fi;
  T178Mode:=mode;; T178ModeRuns:=T178ModeRuns+1;;
  if mode="PRODUCTION" then return T178RunProduction(); fi;
  return T178RunSelftest();
end;;

T178RunSelected := function(mode)
  return T178BindMode(mode);
end;;

## The mode is externally bound before this file is Read; dispatch is exact
## once and no command-line or shell mode can override it.
if not IsBound(D972_R07_CUBIC_COSET_MOMENT_ORACLE_V2_MODE) then
  Error("task178 mode variable unbound before Read");
fi;
if D972_R07_CUBIC_COSET_MOMENT_ORACLE_V2_MODE<>"PRODUCTION" and
   D972_R07_CUBIC_COSET_MOMENT_ORACLE_V2_MODE<>"SELFTEST" then
  Error("task178 external mode invalid");
fi;
T178RunSelected(D972_R07_CUBIC_COSET_MOMENT_ORACLE_V2_MODE);;
if T178ModeRuns<>1 then Error("task178 mode dispatch count"); fi;
