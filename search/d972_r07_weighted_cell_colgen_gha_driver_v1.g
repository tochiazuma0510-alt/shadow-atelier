#############################################################################
## Task 177 weighted-cell column-generation driver v1.
## ASCII only.  Producer and checker are serial and helper-nonshared.
#############################################################################

T177ModeVariable := "D972_R07_WEIGHTED_CELL_COLGEN_V1_MODE";;
T177ProductionModePreamble := "D972_R07_WEIGHTED_CELL_COLGEN_V1_MODE:=\"PRODUCTION\";";;
T177SelftestModePreamble := "D972_R07_WEIGHTED_CELL_COLGEN_V1_MODE:=\"SELFTEST\";";;
T177Producer := "search/d972_r07_weighted_cell_colgen_v1.py";;
T177Checker := "crosscheck/check_d972_r07_weighted_cell_colgen_v1.py";;
T177Fixture := "search/certs/d972_r07_weighted_cell_colgen_selftest_v1_20260827.json";;
T177Receipt := "ci/out/d972_r07_weighted_cell_colgen_receipt_v1.json";;
T177Verdict := "ci/out/d972_r07_weighted_cell_colgen_verdict_v1.json";;
T177ProducerLog := "ci/out/d972_r07_weighted_cell_colgen_producer_v1.log";;
T177CheckerLog := "ci/out/d972_r07_weighted_cell_colgen_checker_v1.log";;
T177Timing := "ci/out/d972_r07_weighted_cell_colgen_timing_v1.txt";;
T177Hashes := "ci/out/d972_r07_weighted_cell_colgen_hashes_v1.txt";;
T177Shell := "ci/out/d972_r07_weighted_cell_colgen_command_v1.sh";;
T177DriverVerdict := "ci/out/d972_r07_weighted_cell_colgen_driver_verdict_v1.txt";;
T177DriverPass := "ci/out/d972_r07_weighted_cell_colgen_driver_pass_v1.done";;
T177StageP := "ci/out/d972_r07_weighted_cell_colgen_producer_v1.done";;
T177StageC := "ci/out/d972_r07_weighted_cell_colgen_checker_v1.done";;
T177StageSP := "ci/out/d972_r07_weighted_cell_colgen_selftest_producer_v1.done";;
T177StageSC := "ci/out/d972_r07_weighted_cell_colgen_selftest_checker_v1.done";;
T177Unknown := "UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED";;
T177SelftestTerminal := "FIXTURE_PASS";;
T177Timeout := 20000;;

T177Read := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task177 missing ",label," ",path); fi;
  return raw;
end;;

T177Count := function(raw,needle)
  local at,n,tail,start;
  if Length(needle)=0 then Error("task177 empty count needle"); fi;
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

T177Pin := function(path,expected_sha,expected_bytes)
  local raw;
  raw:=T177Read(path,"pin");;
  if Length(raw)<>expected_bytes or HexSHA256(raw)<>expected_sha then
    Error("task177 pin drift ",path);
  fi;
  return true;
end;;

T177RejectExisting := function(paths)
  local path;
  if Length(paths)<>Length(Set(paths)) then Error("task177 duplicate output"); fi;
  for path in paths do
    if IsExistingFile(path) then Error("task177 pre-existing output ",path); fi;
  od;
  return true;
end;;

## Immutable task, proof, source, checker, and fixture pins.
## Positive task175/task176 run pins are intentionally absent: production is
## held at UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED until the parent reseals them.
T177Pin("sol/luna_task_177_r07_weighted_cell_column_generation_v1.md",
  "680bfdddf5031bd7b070871a4bb965187cc0d44c8c5c12a451549e173cd3a4da",9077);;
T177Pin("sol/proof_r07_full_e4_seven_evaluation_orbit_selector_v110.md",
  "dd0b75d6dc85229405a3a95e3631a709aa40a0ad21f2c17b96106dae2c7989dc",12136);;
T177Pin("sol/proof_r07_context_fibre_dual_correlation_v118.md",
  "6ef2cbf4ebf5ff3466b5eaf21ef4da572684517eb2f6d18c23fd12c8ad3ada3b",8776);;
T177Pin("sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md",
  "b82c81e0a053658fdb48cbb4d3054a094a57a81b2fd5d0153bcd0735ef4852b3",8545);;
T177Pin("sol/proof_r07_weighted_context_cell_selector_v132.md",
  "a6096938bf5a8b0bdb4844ea973f2687d7eb1b28438ef2d8cc08cdf273667614",13394);;
T177Pin("sol/proof_pb3_two_relator_presentation_equality_v121.md",
  "efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5",5762);;
T177Pin("sol/proof_pb4_eleven_relator_presentation_equality_v108.md",
  "4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f",6742);;
T177Pin("sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md",
  "daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348",7939);;
T177Pin(T177Producer,
  "d955d7717f55ffca3abb92229b96ce2b8ee092ddae3d5e6c7379df92f3892d2e",29523);;
T177Pin(T177Checker,
  "b4d8d046c6850042e0c74778ff8410d9725ef8d0d9387ddb2f75325a6f72d50e",20157);;
T177Pin(T177Fixture,
  "d118633552b5d827d62101f063ba9d7d60fd4335f3744169f85f6cbb2b95da8b",4932);;

T177AssertOne := function(raw,needle,label)
  if T177Count(raw,needle)<>1 then Error("task177 exact marker ",label); fi;
  return true;
end;;

T177WriteDriverPass := function(line)
  local stream;
  stream:=OutputTextFile(T177DriverPass,false);;
  if stream=fail then Error("task177 driver pass open"); fi;
  SetPrintFormattingStatus(stream,false);;
  PrintTo(stream,line,"\n");;
  CloseStream(stream);;
  return true;
end;;

T177WriteEmitter := function()
  local stream,raw;
  stream:=OutputTextFile(T177Shell,false);;
  if stream=fail then Error("task177 emitter open"); fi;
  SetPrintFormattingStatus(stream,false);;
  PrintTo(stream,"#!/usr/bin/env bash\nset -euo pipefail\n");;
  PrintTo(stream,"if [ \"${1:-}\" != '--emit-driver-pass' ] || [ \"$#\" -ne 2 ]; then exit 64; fi\n");;
  PrintTo(stream,"case \"$2\" in\n");;
  PrintTo(stream,"  SELFTEST) d177_mode='SELFTEST'; d177_terminal='FIXTURE_PASS' ;;\n");;
  PrintTo(stream,"  UNKNOWN_INPUT) d177_mode='PRODUCTION'; d177_terminal='UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED' ;;\n");;
  PrintTo(stream,"  *) exit 65 ;;\n");;
  PrintTo(stream,"esac\n");;
  PrintTo(stream,"d177_line=\"R07_WEIGHTED_CELL_COLGEN_GHA_DRIVER_PASS mode=${d177_mode} terminal=${d177_terminal}\"\n");;
  PrintTo(stream,"case \"$d177_line\" in *$'\\n'*|*$'\\r'*) exit 66 ;; esac\n");;
  PrintTo(stream,"test \"$(printf '%s\\n' \"$d177_line\" | wc -l)\" -eq 1\n");;
  PrintTo(stream,"printf '%s\\n' \"$d177_line\"\n");;
  PrintTo(stream,"exit 0\n");;
  CloseStream(stream);;
  raw:=T177Read(T177Shell,"emitter shell");;
  if T177Count(raw,"\\\n")<>0 then
    Error("task177 emitter contains backslash-newline");
  fi;
  return true;
end;;

T177EmitExternal := function(code)
  if code<>"SELFTEST" and code<>"UNKNOWN_INPUT" then
    Error("task177 emitter code ",code);
  fi;
  Exec(Concatenation("bash ",T177Shell," --emit-driver-pass ",code));;
  return true;
end;;

T177CleanLog := function(raw,label)
  local token;
  for token in ["Traceback (most recent call last):","SyntaxError",
                "AssertionError","PRODUCER_STOP","CHECKER_STOP",
                "Killed"] do
    if T177Count(raw,token)<>0 then Error("task177 bad ",label," ",token); fi;
  od;
  return true;
end;;

T177UnknownReceiptGate := function(raw)
  local required,token;
  required:=["\"schema\":\"d972-r07-weighted-cell-colgen/v1\"",
    "\"status\":\"UNKNOWN_INPUT\"",
    "\"terminal\":\"UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED\"",
    "\"reason\":\"PREREQUISITE_NOT_PINNED\"",
    "\"result\":null","\"self_digest_sha256\":",
    "\"all_seven_solution\":false","\"correction_word\":false",
    "\"separator\":false","\"cofinal_lift\":false",
    "\"fake\":false","\"Ihara_witness\":false"];;
  for token in required do
    if T177Count(raw,token)<>1 then Error("task177 unknown receipt gate ",token); fi;
  od;
  if T177Count(raw,"R07_WEIGHTED_CELL_COLGEN_COMMON_WORD")<>0 or
     T177Count(raw,"R07_WEIGHTED_CELL_COLGEN_SEPARATOR")<>0 then
    Error("task177 unknown receipt mixed terminal");
  fi;
  return true;
end;;

T177VerdictGate := function(raw)
  local required,token;
  required:=["\"schema\":\"d972-r07-weighted-cell-colgen/v1/checker-v1\"",
    "\"status\":\"PASS\"",
    "\"terminal\":\"UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED\"",
    "\"receipt_terminal\":\"UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED\"",
    "\"reason\":\"PREREQUISITE_NOT_PINNED\"",
    "\"producer_receipt_sha256\":","\"self_digest_sha256\":"];;
  for token in required do
    if T177Count(raw,token)<>1 then Error("task177 verdict gate ",token); fi;
  od;
  return true;
end;;

T177TerminalAgreement := function(raw_receipt,raw_verdict)
  local receipt_count,verdict_count;
  receipt_count:=T177Count(raw_receipt,
    "\"terminal\":\"UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED\"");;
  verdict_count:=T177Count(raw_verdict,
    "\"receipt_terminal\":\"UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED\"");;
  if receipt_count<>1 or verdict_count<>1 then
    Error("task177 terminal disagreement");
  fi;
  return T177Unknown;
end;;

T177Preamble := Concatenation(
  "timeout 20000s bash -o pipefail -c '",
  "set -euo pipefail; mkdir -p ci/out; ",
  "python3 -B ",T177Producer," --run-colgen --output ",T177Receipt,
  " >",T177ProducerLog," 2>&1; echo T177_PRODUCER_STAGE_DONE >",T177StageP,
  "; python3 -B ",T177Checker," --check --receipt ",T177Receipt,
  " --verdict ",T177Verdict," >",T177CheckerLog,
  " 2>&1; echo T177_CHECKER_STAGE_DONE >",T177StageC,"'");;

T177SelftestPreamble := Concatenation(
  "timeout 1800s bash -o pipefail -c '",
  "set -euo pipefail; mkdir -p ci/out; python3 -B ",T177Producer,
  " --selftest --fixture ",T177Fixture," >",T177ProducerLog,
  " 2>&1; echo T177_SELFTEST_PRODUCER_STAGE_DONE >",T177StageSP,
  "; python3 -B ",T177Checker," --selftest --fixture ",T177Fixture,
  " >",T177CheckerLog,
  " 2>&1; echo T177_SELFTEST_CHECKER_STAGE_DONE >",T177StageSC,"'");;

T177RunSelftest := function()
  local rawp,rawc;
  T177RejectExisting([T177ProducerLog,T177CheckerLog,T177StageSP,T177StageSC,
    T177StageP,T177StageC,T177DriverPass,T177Receipt,T177Verdict,T177Hashes,
    T177Shell,T177Timing,T177DriverVerdict]);;
  T177WriteEmitter();;
  T177Exec(T177SelftestPreamble);;
  rawp:=T177Read(T177ProducerLog,"selftest producer log");;
  rawc:=T177Read(T177CheckerLog,"selftest checker log");;
  T177CleanLog(rawp,"producer");; T177CleanLog(rawc,"checker");;
  T177AssertOne(rawp,"R07_WEIGHTED_CELL_COLGEN_PRODUCER_SELFTEST_PASS mutations=12 rejected=12 linked_nonabelian_order=6","producer selftest");;
  T177AssertOne(rawc,"R07_WEIGHTED_CELL_COLGEN_CHECKER_SELFTEST_PASS mutations=12 rejected=12 linked_nonabelian_order=6","checker selftest");;
  T177AssertOne(T177Read(T177StageSP,"producer stage"),"T177_SELFTEST_PRODUCER_STAGE_DONE\n","producer stage");;
  T177AssertOne(T177Read(T177StageSC,"checker stage"),"T177_SELFTEST_CHECKER_STAGE_DONE\n","checker stage");;
  T177WriteDriverPass("R07_WEIGHTED_CELL_COLGEN_GHA_DRIVER_PASS mode=SELFTEST terminal=FIXTURE_PASS");;
  T177AssertOne(T177Read(T177DriverPass,"driver selftest pass"),"R07_WEIGHTED_CELL_COLGEN_GHA_DRIVER_PASS mode=SELFTEST terminal=FIXTURE_PASS","driver selftest pass");
  T177EmitExternal("SELFTEST");;
  return true;
end;;

T177RunProduction := function()
  local rawp,rawc,rawr,rawv,terminal;
  T177RejectExisting([T177ProducerLog,T177CheckerLog,T177StageSP,T177StageSC,
    T177StageP,T177StageC,T177DriverPass,T177Receipt,T177Verdict,T177Hashes,
    T177Shell,T177Timing,T177DriverVerdict]);;
  T177WriteEmitter();;
  T177Exec(T177Preamble);;
  rawp:=T177Read(T177ProducerLog,"producer log");;
  rawc:=T177Read(T177CheckerLog,"checker log");;
  rawr:=T177Read(T177Receipt,"receipt");;
  rawv:=T177Read(T177Verdict,"verdict");;
  T177CleanLog(rawp,"producer");; T177CleanLog(rawc,"checker");;
  T177AssertOne(T177Read(T177StageP,"producer stage"),"T177_PRODUCER_STAGE_DONE\n","producer stage");;
  T177AssertOne(T177Read(T177StageC,"checker stage"),"T177_CHECKER_STAGE_DONE\n","checker stage");;
  T177AssertOne(rawp,"R07_WEIGHTED_CELL_COLGEN_PRODUCER_TERMINAL UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED","producer terminal");;
  T177AssertOne(rawc,"R07_WEIGHTED_CELL_COLGEN_CHECKER_PASS terminal=UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED","checker terminal");;
  terminal:=T177TerminalAgreement(rawr,rawv);;
  if terminal<>T177Unknown then Error("task177 unexpected terminal ",terminal); fi;
  T177UnknownReceiptGate(rawr);; T177VerdictGate(rawv);;
  PrintTo(T177Hashes,Concatenation("producer_sha256=",HexSHA256(rawp),
    "\nchecker_sha256=",HexSHA256(rawc),"\nreceipt_sha256=",HexSHA256(rawr),
    "\nverdict_sha256=",HexSHA256(rawv),"\n"));
  PrintTo(T177DriverVerdict,rawv);
  PrintTo(T177Timing,"mode=PRODUCTION terminal=UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED timeout_seconds=20000\n");
  T177WriteDriverPass("R07_WEIGHTED_CELL_COLGEN_GHA_DRIVER_PASS mode=PRODUCTION terminal=UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED");;
  T177AssertOne(T177Read(T177DriverPass,"driver production pass"),"R07_WEIGHTED_CELL_COLGEN_GHA_DRIVER_PASS mode=PRODUCTION terminal=UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED","driver production pass");
  T177EmitExternal("UNKNOWN_INPUT");;
  return true;
end;;

T177Exec := function(command)
  Exec(command);;
  return true;
end;;

T177Mode := "UNBOUND";;
T177ModeRuns := 0;;
T177BindMode := function(mode)
  if T177Mode<>"UNBOUND" then Error("task177 mode rebind"); fi;
  if mode<>"PRODUCTION" and mode<>"SELFTEST" then Error("task177 invalid mode ",mode); fi;
  T177Mode:=mode;; T177ModeRuns:=T177ModeRuns+1;;
  if mode="PRODUCTION" then return T177RunProduction(); fi;
  return T177RunSelftest();
end;;

T177RunSelected := function(mode)
  return T177BindMode(mode);
end;;

if not IsBound(D972_R07_WEIGHTED_CELL_COLGEN_V1_MODE) then
  Error("task177 mode variable unbound before Read");
fi;
if D972_R07_WEIGHTED_CELL_COLGEN_V1_MODE<>"PRODUCTION" and
   D972_R07_WEIGHTED_CELL_COLGEN_V1_MODE<>"SELFTEST" then
  Error("task177 external mode invalid");
fi;
T177RunSelected(D972_R07_WEIGHTED_CELL_COLGEN_V1_MODE);;
if T177ModeRuns<>1 then Error("task177 mode dispatch count"); fi;
