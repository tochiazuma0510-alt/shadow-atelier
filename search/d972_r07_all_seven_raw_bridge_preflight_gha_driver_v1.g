#############################################################################
## Task 175 ASCII-only serial GHA driver.  This file is not dispatched here.
#############################################################################

T175P := "search/d972_r07_all_seven_raw_bridge_preflight_v1.py";;
T175C := "crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py";;
T175ModeVariable := "D972_R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_MODE";;
T175ProductionModePreamble := "D972_R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_MODE:=\"PRODUCTION\";";;
T175SelftestModePreamble := "D972_R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_MODE:=\"SELFTEST\";";;
T175R := "search/certs/d972_r07_all_seven_raw_bridge_preflight_v1_20260827.json";;
T175SelftestR := "ci/out/d972_r07_all_seven_raw_bridge_preflight_selftest_receipt_v1.json";;
T175ROut := "ci/out/d972_r07_all_seven_raw_bridge_preflight_receipt_v1.json";;
T175LogP := "ci/out/d972_r07_all_seven_raw_bridge_preflight_producer_v1.log";;
T175LogC := "ci/out/d972_r07_all_seven_raw_bridge_preflight_checker_v1.log";;
T175Hash := "ci/out/d972_r07_all_seven_raw_bridge_preflight_hashes_v1.txt";;
T175Verdict := "ci/out/d972_r07_all_seven_raw_bridge_preflight_verdict_v1.txt";;
T175DriverVerdict := "ci/out/d972_r07_all_seven_raw_bridge_preflight_driver_verdict_v1.txt";;
T175DriverPass := "ci/out/d972_r07_all_seven_raw_bridge_preflight_driver_pass_v1.done";;
T175StageP := "ci/out/d972_r07_all_seven_raw_bridge_preflight_producer_v1.done";;
T175StageC := "ci/out/d972_r07_all_seven_raw_bridge_preflight_checker_v1.done";;
T175StageSP := "ci/out/d972_r07_all_seven_raw_bridge_preflight_selftest_producer_v1.done";;
T175StageSC := "ci/out/d972_r07_all_seven_raw_bridge_preflight_selftest_checker_v1.done";;
T175Cap := 6441;;
T175FoxCap := 110;;
T175Timeout := 9000;;
T175Terminals := [
 "R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_READY",
 "UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE",
 "UNKNOWN_INPUT:PB3_PRESENTATION_PIN",
 "UNKNOWN_INPUT:RAW_FORMULA",
 "UNKNOWN_INPUT:FOX_CANARY",
 "FIXTURE_PASS",
 "UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD",
 "UNKNOWN_RESOURCE:runtime" ];;
T175UnknownTerminals := [
 "UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE",
 "UNKNOWN_INPUT:PB3_PRESENTATION_PIN",
 "UNKNOWN_INPUT:RAW_FORMULA",
 "UNKNOWN_INPUT:FOX_CANARY",
 "UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD",
 "UNKNOWN_RESOURCE:runtime" ];;

T175Read := function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task175 missing ",path); fi;
  return raw;
end;;

T175Count := function(raw,needle)
  local at,n,tail,start;
  if Length(needle)=0 then Error("task175 empty count needle"); fi;
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

T175RejectExisting := function(paths)
  local p;
  for p in paths do
    if IsExistingFile(p) then Error("task175 pre-existing output ",p); fi;
  od;
  return true;
end;;

T175Pin := function(path,expected_sha,expected_bytes)
  local raw;
  raw:=T175Read(path);;
  if expected_bytes>0 and Length(raw)<>expected_bytes then
    Error("task175 byte pin ",path);
  fi;
  if HexSHA256(raw)<>expected_sha then Error("task175 SHA pin ",path); fi;
  return true;
end;;

## Immutable theorem, inventory, receipt, and current task pins.
T175Pin("sol/luna_task_175b_r07_all_seven_raw_bridge_implementation_repair.md",
 "a41f2446fd1c9f0bd60a7189db682784f4e69e24e8958f7c4505cd1eb9741836",5136);;
T175Pin("sol/luna_task_175_r07_all_seven_raw_bridge_preflight_v1.md",
 "5d0d8e006c6a752e5a525b188c9d95ba0c858aa69147432e639fe3e735ffefee",8584);;
T175Pin("sol/luna_reply_173_r07_all_seven_raw_bridge_inventory_v1.md",
 "189a642fc8654f163b0b7964b75043ea393cac31a0b56b84ae0fddf2f73c3695",24283);;
T175Pin("sol/proof_pb3_two_relator_presentation_equality_v121.md",
 "efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5",5762);;
T175Pin("sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md",
 "daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348",7939);;
T175Pin("sol/audit_r07_all_seven_bridge_checkpoint_v123.md",
 "272aabc882599031c4da0472f8f2340043b32571e8e05ecaa58fc5ad1c6a31ac",5017);;
T175Pin("sol/proof_pb4_eleven_relator_presentation_equality_v108.md",
 "4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f",6742);;
T175Pin("search/d972_r07_full_e4_joint_orbit_preflight_v7.py",
 "92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed",21918);;
T175Pin("crosscheck/check_d972_r07_full_e4_orbit_preflight_v7.py",
 "e3917ec05b95b8996e3a5cec1cc2bfde51c3ed8c6972175fd9be9e1178205c23",12423);;
T175Pin("search/certs/d972_r07_full_e4_orbit_preflight_v7_20260827.json",
 "86c6f3a72a3f852a1be7c5323bf72c7ad987377fd5483b6e32528fe263e290ff",45246709);;
T175Pin("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json",
 "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72",231570);;
T175Pin("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json",
 "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df",2166036);;
T175Pin(T175R,
 "0d9a9588cd4f58531923dc208819f32d552006eea8e323a198382901d132c69f",6870);;
T175Pin(T175P,
 "acec0196fa43c91a5fc0d63c3c8235ee7e33d29f0d3ebdc4cf9fdbd8bccfa525",55273);;
T175Pin(T175C,
 "4b52450c547834725fd61b874976ba1a60435bde60cc868a2ee7913a3c0ad9d8",77970);;
T175Pin("search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py",
 "f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f",33409);;
T175Pin("search/d972_b345_joint_kernel_qstar_closure_v1.py",
 "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc",67945);;
T175Pin("search/d972_b345_target6_dual_colgen_v2.py",
 "b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7",444497);;
T175Pin("search/d972_b345_triple_cube_raw_lambda_census_v1.py",
 "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db",126942);;

## No file is allowed to pre-exist at the start of a GHA attempt.
T175RejectExisting([T175LogP,T175LogC,T175Hash,T175Verdict,T175DriverVerdict,T175DriverPass,T175ROut,T175SelftestR,T175StageP,T175StageC,T175StageSP,T175StageSC]);;

## The host generic gap-run.yml must supply a shell with pipefail and timeout.
## Exactly one producer is followed by exactly one independent checker.
T175Preamble := Concatenation(
 "timeout 9000s bash -o pipefail -c '",
 "set -euo pipefail; mkdir -p ci/out; ",
 "python -B ",T175P," --run-preflight --output ",T175ROut," >",T175LogP," 2>&1; ",
 "echo T175_PRODUCER_STAGE_DONE >",T175StageP,"; ",
 "python -B ",T175C," --check --receipt ",T175ROut," --output ",T175Verdict," >",T175LogC," 2>&1; ",
 "echo T175_CHECKER_STAGE_DONE >",T175StageC,"'");;
T175SelftestPreamble := Concatenation(
 "timeout 9000s bash -o pipefail -c '",
 "set -euo pipefail; mkdir -p ci/out; ",
 "python -B ",T175P," --output ",T175SelftestR," >",T175LogP," 2>&1; ",
 "echo T175_SELFTEST_PRODUCER_DONE >",T175StageSP,"; ",
 "python -B ",T175C," --fixture --receipt ",T175R," >",T175LogC," 2>&1; ",
 "echo T175_SELFTEST_CHECKER_DONE >",T175StageSC,"'");;

## Actual Exec entry points used by the generic gap-run.yml host.
T175Exec := function(command)
  Exec(command);;
  return true;
end;;

T175RunSelftest := function()
  local rawp,rawc,rawr;
  T175RejectExisting([T175LogP,T175LogC,T175SelftestR,T175StageSP,T175StageSC,T175StageP,T175StageC,T175DriverPass]);;
  T175Exec(T175SelftestPreamble);;
  rawp:=T175Read(T175LogP);; rawc:=T175Read(T175LogC);; rawr:=T175Read(T175SelftestR);;
  if T175Read(T175StageSP)<>"T175_SELFTEST_PRODUCER_DONE\n" then Error("task175 selftest producer sentinel"); fi;
  if T175Read(T175StageSC)<>"T175_SELFTEST_CHECKER_DONE\n" then Error("task175 selftest checker sentinel"); fi;
  T175AssertMarker(rawp,"D175_PRODUCER_DONE");;
  T175AssertTerminal(rawp);;
  T175AssertAllowed(rawr,"\"terminal\": \"");;
  T175StaticJsonGate(rawr);;
  T175AssertAllowed(rawc,"terminal=");;
  T175AssertMarker(rawc,"D175_STATIC_CHECK_PASS");;
  PrintTo(T175DriverPass,"D175_DRIVER_PASS\nmode=SELFTEST\nterminal=FIXTURE_PASS\n");
  if T175Count(T175Read(T175DriverPass),"D175_DRIVER_PASS")<>1 then
    Error("task175 selftest driver pass sentinel");
  fi;
  return true;
end;;

T175AssertTerminal := function(raw)
  local t,n;
  n:=0;;
  for t in T175Terminals do n:=n+T175Count(raw,t); od;
  if n<>1 then Error("task175 exact-one terminal failure"); fi;
  return true;
end;;

T175AssertMarker := function(raw,needle)
  if T175Count(raw,needle)<>1 then Error("task175 exact-one marker ",needle); fi;
  return true;
end;;

T175AssertAllowed := function(raw,prefix)
  local t,n;
  n:=0;;
  for t in T175Terminals do n:=n+T175Count(raw,Concatenation(prefix,t)); od;
  if n<>1 then Error("task175 allowed terminal gate ",prefix); fi;
  return true;
end;;

T175ExtractTerminal := function(raw,prefix)
  local t,needle,n,found;
  n:=0;; found:="";;
  for t in T175Terminals do
    needle:=Concatenation(prefix,t);;
    if T175Count(raw,needle)<>0 then
      if T175Count(raw,needle)<>1 then
        Error("task175 terminal multiplicity ",t);
      fi;
      n:=n+1;; found:=t;;
    fi;
  od;
  if n<>1 then Error("task175 terminal extraction"); fi;
  return found;
end;;

T175AssertTerminalAgreement := function(rawr,rawc)
  local receipt_terminal,checker_terminal;
  receipt_terminal:=T175ExtractTerminal(rawr,"\"terminal\": \"");;
  checker_terminal:=T175ExtractTerminal(rawc,"terminal=");;
  if receipt_terminal<>checker_terminal then
    Error("task175 receipt/checker terminal mismatch ",receipt_terminal,"/",checker_terminal);
  fi;
  return receipt_terminal;
end;;

T175JsonGate := function(raw)
  local required,s;
  required:=["roster_contract","context_contract","all_seven_contract",
    "fox_contract","mutation_contract","boundaries","caps","roster",
    "relation_roster","registered_canary","corrected_word","literal_words",
    "raw_base_targets","raw_changes","pentagon","pb3","pb4",
    "stacked_target","fox_replay","mutation_results"];;
  for s in required do
    if PositionSublist(raw,Concatenation("\"",s,"\":"))=fail then Error("task175 JSON coverage ",s); fi;
  od;
  if PositionSublist(raw,"6441")=fail or PositionSublist(raw,"110")=fail then
    Error("task175 count gate");
  fi;
  return true;
end;;

T175StaticJsonGate := function(raw)
  local required,s;
  required:=["roster_contract","context_contract","all_seven_contract",
    "fox_contract","mutation_contract","boundaries","caps"];;
  for s in required do
    if PositionSublist(raw,Concatenation("\"",s,"\":"))=fail then Error("task175 static JSON coverage ",s); fi;
  od;
  if PositionSublist(raw,"6441")=fail or PositionSublist(raw,"110")=fail then
    Error("task175 static count gate");
  fi;
  return true;
end;;

T175ProductionJsonGate := function(raw,terminal)
  if terminal="R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_READY" then
    T175JsonGate(raw);;
    return true;
  fi;
  if Position(T175UnknownTerminals,terminal)=fail then
    Error("task175 unregistered production terminal ",terminal);
  fi;
  # A typed UNKNOWN is an honest fail-closed result.  Its static envelope is
  # checked, while READY remains behind the complete lossless JSON gate.
  T175StaticJsonGate(raw);;
  return true;
end;;

T175RunProduction := function()
  local rawp,rawc,rawr,terminal;
T175RejectExisting([T175LogP,T175LogC,T175Hash,T175Verdict,T175DriverVerdict,T175DriverPass,T175ROut,T175SelftestR,T175StageP,T175StageC,T175StageSP,T175StageSC]);;
  T175Exec(T175Preamble);;
  rawp:=T175Read(T175LogP);; rawc:=T175Read(T175LogC);; rawr:=T175Read(T175ROut);;
  if T175Read(T175StageP)<>"T175_PRODUCER_STAGE_DONE\n" then Error("task175 producer stage sentinel"); fi;
  if T175Read(T175StageC)<>"T175_CHECKER_STAGE_DONE\n" then Error("task175 checker stage sentinel"); fi;
  T175AssertMarker(rawp,"D175_PRODUCER_DONE");;
  T175AssertTerminal(rawp);;
  T175AssertAllowed(rawc,"terminal=");;
  T175AssertAllowed(rawr,"\"terminal\": \"");;
  T175AssertMarker(rawc,"D175_CHECK_PASS");;
  terminal:=T175AssertTerminalAgreement(rawr,rawc);;
  T175ProductionJsonGate(rawr,terminal);;
  PrintTo(T175Hash,"producer_sha256=",HexSHA256(T175Read(T175P)),"\nchecker_sha256=",HexSHA256(T175Read(T175C)),"\nreceipt_sha256=",HexSHA256(rawr),"\nruntime_seconds=bounded_9000\n");
  PrintTo(T175DriverVerdict,"TASK175_VERDICT=",rawc,"\n");
  PrintTo(T175DriverPass,"D175_DRIVER_PASS\nmode=PRODUCTION\nterminal=",terminal,"\n");
  if T175Count(T175Read(T175DriverPass),"D175_DRIVER_PASS")<>1 then
    Error("task175 driver pass sentinel");
  fi;
  return true;
end;;

## Exactly one mode may be bound for a driver Read/dispatch attempt.
T175Mode := "UNBOUND";;
T175ModeRuns := 0;;
T175BindMode := function(mode)
  if T175Mode<>"UNBOUND" then Error("task175 mutually-exclusive mode rebind"); fi;
  if mode<>"PRODUCTION" and mode<>"SELFTEST" then Error("task175 invalid mode ",mode); fi;
  T175Mode:=mode;;
  T175ModeRuns:=T175ModeRuns+1;;
  if mode="PRODUCTION" then return T175RunProduction(); fi;
  return T175RunSelftest();
end;;
T175RunSelected := function(mode)
  return T175BindMode(mode);
end;;

## The generic host binds this variable before Read; Read then dispatches once.
if not IsBound(D972_R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_MODE) then
  Error("task175 mode variable unbound; bind PRODUCTION or SELFTEST before Read");
fi;
if D972_R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_MODE<>"PRODUCTION" and
   D972_R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_MODE<>"SELFTEST" then
  Error("task175 invalid external mode");
fi;
T175RunSelected(D972_R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_V1_MODE);;
if T175ModeRuns<>1 then Error("task175 mode dispatch count"); fi;

## The CI wrapper records complete logs even when a later gate fails.
T175DriverContract := rec(
  workflow:=".github/workflows/gap-run.yml", producer:=T175P, checker:=T175C,
  receipt:=T175R, selftest_receipt:=T175SelftestR, serial:=true, roster_cap:=T175Cap, fox_cap:=T175FoxCap,
  timeout_seconds:=T175Timeout, preexisting_output_rejection:=true,
  mode_variable:=T175ModeVariable, mode_gate:="T175BindMode", production_mode_binding:="PRODUCTION",
  selftest_mode_binding:="SELFTEST", production_mode_preamble:=T175ProductionModePreamble,
  selftest_mode_preamble:=T175SelftestModePreamble, mutually_exclusive:=true,
  exact_one_terminal:=true, json_coverage:=true, full_logs_on_failure:=true,
  terminal_agreement:=true, typed_unknown_gate:=true, driver_pass_sentinel:=T175DriverPass,
  selftest_mode:=T175SelftestPreamble, production_mode:=T175Preamble,
  executable_selftest:=T175RunSelftest, executable_production:=T175RunProduction,
  no_orbit:=true, no_column_generation:=true, no_affine_solve:=true,
  no_correction_search:=true, no_cofinal_argument:=true, dispatch:=false);;
