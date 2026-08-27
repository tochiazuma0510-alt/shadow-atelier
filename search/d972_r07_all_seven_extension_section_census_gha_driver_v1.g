#############################################################################
## Task 176 all-seven extension-section census driver v1.
## ASCII only.  Producer and helper-nonshared checker are strictly serial.
#############################################################################

if not IsBound(D972_R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_MODE) then
  Error("task176 driver: MODE must be bound to SELFTEST or PRODUCTION");
fi;
D176Mode:=D972_R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_MODE;;
if D176Mode<>"SELFTEST" and D176Mode<>"PRODUCTION" then
  Error("task176 driver: invalid MODE");
fi;

D176Producer:="search/d972_r07_all_seven_extension_section_census_v1.py";;
D176Checker:="crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py";;
D176Fixture:="search/certs/d972_r07_all_seven_extension_section_census_preflight_v1_20260827.json";;
D176Receipt:="ci/out/d972_r07_all_seven_extension_section_census_v1.json";;
D176Verdict:="ci/out/d972_r07_all_seven_extension_section_census_crosscheck_v1.json";;
D176ProducerLog:="ci/out/d972_r07_all_seven_extension_section_census_producer_v1.log";;
D176CheckerLog:="ci/out/d972_r07_all_seven_extension_section_census_checker_v1.log";;
D176Timing:="ci/out/d972_r07_all_seven_extension_section_census_timing_v1.txt";;
D176Hashes:="ci/out/d972_r07_all_seven_extension_section_census_hashes_v1.txt";;
D176Shell:="ci/out/d972_r07_all_seven_extension_section_census_command_v1.sh";;
D176OK:="ci/out/d972_r07_all_seven_extension_section_census_v1.ok";;

D176ProducerSHA:="52ef71eb2cd9f1a7dd3fe23fabeb53b0316e71825bcc3ada478e90308332506f";;
D176ProducerBytes:=49238;;
D176CheckerSHA:="d60ade51eccfad4b59a24e9be9e28871be56cec0e4a6e0af63c3b5505beb9760";;
D176CheckerBytes:=66752;;
D176FixtureSHA:="b24827b10f8ceb0505802bf7065e2442d176b7b65ecb2066452941c2e7e0a471";;
D176FixtureBytes:=4350;;

D176Pins:=[
  [D176Producer,D176ProducerSHA,D176ProducerBytes],
  [D176Checker,D176CheckerSHA,D176CheckerBytes],
  [D176Fixture,D176FixtureSHA,D176FixtureBytes],
  ["sol/luna_task_176_r07_all_seven_extension_section_census_v1.md","a1778c17c33e42880a6dd0c2480303a13702cb38950cf836a4ca9d8cca6fa332",7054],
  ["search/d972_b345_seedspan_triple4_v1.py","fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29",535219],
  ["search/d972_b345_joint_kernel_qstar_closure_v1.py","06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc",67945],
  ["search/check_d972_b345_joint_kernel_qstar_closure_v2.py","5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88",5942],
  ["search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g","8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7",3912],
  ["sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md","64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4",11226],
  ["sol/luna_reply_157ee_b345_joint_kernel_qstar_closure.md","53f20c2cb1395b8ff59ee961e1d5a14d55156a488eb6fa49edefed5dd7619eee",4118],
  ["ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json","1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df",2166036],
  ["ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json","3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72",231570],
  ["sol/proof_pb4_eleven_relator_presentation_equality_v108.md","4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f",6742],
  ["sol/proof_pb3_two_relator_presentation_equality_v121.md","efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5",5762],
  ["sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md","daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348",7939],
  ["sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md","b82c81e0a053658fdb48cbb4d3054a094a57a81b2fd5d0153bcd0735ef4852b3",8545],
  ["sol/luna_reply_174_r07_target6_context_image_census_v1.md","516d15d4ad73e9e2d8e564789e856224c35a30a235e46e87ad857cb20470b49f",13224]
];;

D176Terminals:=[
  "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS",
  "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_RESOURCE",
  "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_INPUT"
];;

D176Read:=function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task176 driver: missing ",label," ",path); fi;
  return raw;
end;;

D176Count:=function(raw,needle)
  local count,at;
  if Length(needle)=0 then Error("task176 driver: empty count needle"); fi;
  count:=0;; at:=PositionSublist(raw,needle);;
  while at<>fail do
    count:=count+1;; at:=PositionSublist(raw,needle,at);;
  od;
  return count;
end;;

D176Pin:=function(row)
  local raw;
  raw:=D176Read(row[1],"pin");;
  if Length(raw)<>row[3] or HexSHA256(raw)<>row[2] then
    Error("task176 driver: pin drift ",row[1]);
  fi;
  return true;
end;;

D176RejectOwned:=function(paths)
  local path;
  if Length(paths)<>Length(Set(paths)) then Error("task176 driver: duplicate output"); fi;
  for path in paths do
    if IsExistingFile(path) then Error("task176 driver: pre-existing output ",path); fi;
  od;
end;;

D176CleanLog:=function(raw,label)
  local token;
  for token in ["Traceback (most recent call last):","SyntaxError","RuntimeError",
                "AssertionError","CHECKER_STOP","PRODUCER_STOP","Killed"] do
    if D176Count(raw,token)<>0 then Error("task176 driver: bad log ",label," ",token); fi;
  od;
end;;

D176FixtureAudit:=function(raw)
  return D176Count(raw,"\"schema\": \"d972-r07-all-seven-extension-section-census/v1\"")=1 and
         D176Count(raw,"\"status\": \"UNKNOWN_RESOURCE\"")=1 and
         D176Count(raw,"\"reason\": \"LOCAL_EXECUTION_GUARD\"")=1 and
         D176Count(raw,"\"terminal\": \"R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_RESOURCE\"")=1 and
         D176Count(raw,"\"self_digest_sha256\": \"880f490c379fd50ebfa553d6d07e0a14263775c26f29a05efab938fe51afe055\"")=1 and
         D176Count(raw,"\"context_id\":21")=2 and
         D176Count(raw,"\"type\":\"E3\"")=5 and
         D176Count(raw,"\"type\":\"E4\"")=5;
end;;

D176ReceiptAudit:=function(raw,terminal)
  local token,inputReasonCount;
  if D176Count(raw,"\"schema\":\"d972-r07-all-seven-extension-section-census/v1\"")<>1 or
     D176Count(raw,Concatenation("\"terminal\":\"",terminal,"\""))<>1 or
     D176Count(raw,"\"self_digest_sha256\":\"")<>1 or
     D176Count(raw,"\"direct_Delta_enumeration\":false")<>1 or
     D176Count(raw,"\"all_seven_solution\":false")<>1 or
     D176Count(raw,"\"cofinal_lift\":false")<>1 or
     D176Count(raw,"\"fake\":false")<>1 or
     D176Count(raw,"\"Ihara_witness\":false")<>1 then
    Error("task176 driver: receipt fixed gate");
  fi;
  for token in D176Terminals do
    if token<>terminal and D176Count(raw,Concatenation("\"terminal\":\"",token,"\""))<>0 then
      Error("task176 driver: mixed terminals");
    fi;
  od;
  if terminal=D176Terminals[1] then
    if D176Count(raw,"\"status\":\"COMPLETE\"")<>1 or
       D176Count(raw,"\"result\":{")<>1 or
       D176Count(raw,"\"direct_Delta_states_enumerated\":0")<>1 or
       D176Count(raw,"\"Q0_states_enumerated_once\":1469664")<>1 then
      Error("task176 driver: COMPLETE gate");
    fi;
  elif terminal=D176Terminals[2] then
    if D176Count(raw,"\"status\":\"UNKNOWN_RESOURCE\"")<>1 or
       D176Count(raw,"\"result\":null")<>1 then Error("task176 driver: resource gate"); fi;
  else
    inputReasonCount:=D176Count(raw,"\"reason\":\"AUTHENTICATED_INPUT:")+
                      D176Count(raw,"\"reason\":\"CENSUS_REJECT:");;
    if D176Count(raw,"\"status\":\"UNKNOWN_INPUT\"")<>1 or
       D176Count(raw,"\"result\":null")<>1 or inputReasonCount<>1 or
       D176Count(raw,"\"reason\":\"AUTHENTICATED_INPUT:\"")<>0 or
       D176Count(raw,"\"reason\":\"CENSUS_REJECT:\"")<>0 then
      Error("task176 driver: input gate");
    fi;
  fi;
end;;

for D176Row in D176Pins do D176Pin(D176Row);; od;
if not D176FixtureAudit(D176Read(D176Fixture,"fixture")) then
  Error("task176 driver: fixture audit");
fi;
D176RejectOwned([D176Receipt,D176Verdict,D176ProducerLog,D176CheckerLog,
                 D176Timing,D176Hashes,D176Shell,D176OK]);;

D176ShellStream:=OutputTextFile(D176Shell,false);;
if D176ShellStream=fail then Error("task176 driver: shell output open"); fi;
SetPrintFormattingStatus(D176ShellStream,false);;
PrintTo(D176ShellStream,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D176ShellStream,"if [ \"${1:-}\" = '--emit-driver-pass' ]; then\n");;
PrintTo(D176ShellStream,"  test \"$#\" -eq 2\n");;
PrintTo(D176ShellStream,"  case \"$2\" in\n");;
PrintTo(D176ShellStream,"    SELFTEST) d176_mode='SELFTEST'; d176_terminal='SELFTEST'; d176_expected='R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_GHA_DRIVER_PASS mode=SELFTEST terminal=SELFTEST' ;;\n");;
PrintTo(D176ShellStream,"    PASS) d176_mode='PRODUCTION'; d176_terminal='R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS'; d176_expected='R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_GHA_DRIVER_PASS mode=PRODUCTION terminal=R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS' ;;\n");;
PrintTo(D176ShellStream,"    UNKNOWN_RESOURCE) d176_mode='PRODUCTION'; d176_terminal='R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_RESOURCE'; d176_expected='R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_GHA_DRIVER_PASS mode=PRODUCTION terminal=R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_RESOURCE' ;;\n");;
PrintTo(D176ShellStream,"    UNKNOWN_INPUT) d176_mode='PRODUCTION'; d176_terminal='R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_INPUT'; d176_expected='R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_GHA_DRIVER_PASS mode=PRODUCTION terminal=R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_INPUT' ;;\n");;
PrintTo(D176ShellStream,"    *) exit 64 ;;\n");;
PrintTo(D176ShellStream,"  esac\n");;
PrintTo(D176ShellStream,"  d176_line=\"R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_GHA_DRIVER_PASS mode=${d176_mode} terminal=${d176_terminal}\"\n");;
PrintTo(D176ShellStream,"  test \"$d176_line\" = \"$d176_expected\"\n");;
PrintTo(D176ShellStream,"  case \"$d176_line\" in *$'\\n'*|*$'\\r'*) exit 65 ;; esac\n");;
PrintTo(D176ShellStream,"  printf '%s\\n' \"$d176_line\"\n");;
PrintTo(D176ShellStream,"  exit 0\n");;
PrintTo(D176ShellStream,"fi\n");;
PrintTo(D176ShellStream,"command -v python3 >/dev/null\ncommand -v timeout >/dev/null\nmkdir -p ci/out\n");;
if D176Mode="SELFTEST" then
  PrintTo(D176ShellStream,"p0=$(date +%s)\n");;
  PrintTo(D176ShellStream,"timeout --signal=TERM --kill-after=60s 900s python3 -u -B ",D176Producer,
    " --selftest --fixture ",D176Fixture," 2>&1 | tee ",D176ProducerLog,"\n");;
  PrintTo(D176ShellStream,"test ${PIPESTATUS[0]} -eq 0\n");;
  PrintTo(D176ShellStream,"test \"$(grep -Fxc 'R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_PRODUCER_SELFTEST_PASS perm_type_checks=2 deleter_type_checks=6' ",
    D176ProducerLog,")\" -eq 1\np1=$(date +%s)\n");;
  PrintTo(D176ShellStream,"timeout --signal=TERM --kill-after=60s 1200s python3 -u -B ",D176Checker,
    " --selftest --fixture ",D176Fixture," 2>&1 | tee ",D176CheckerLog,"\n");;
  PrintTo(D176ShellStream,"test ${PIPESTATUS[0]} -eq 0\n");;
  PrintTo(D176ShellStream,"test \"$(grep -Fxc 'R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_CHECKER_SELFTEST_PASS mutation_attempted=15 mutation_rejected=15 reject_envelope_checks=3 perm_type_checks=2 deleter_type_checks=6 linked_nonabelian_order=54' ",
    D176CheckerLog,")\" -eq 1\np2=$(date +%s)\n");;
  PrintTo(D176ShellStream,"printf 'mode=SELFTEST producer_seconds=%s checker_seconds=%s\\n' \"$((p1-p0))\" \"$((p2-p1))\" > ",D176Timing,"\n");;
else
  PrintTo(D176ShellStream,"p0=$(date +%s)\n");;
  PrintTo(D176ShellStream,"timeout --signal=TERM --kill-after=60s 9600s python3 -u -B ",D176Producer,
    " --run-census --soft-seconds 9000 --output ",D176Receipt,
    " 2>&1 | tee ",D176ProducerLog,"\n");;
  PrintTo(D176ShellStream,"test ${PIPESTATUS[0]} -eq 0\np1=$(date +%s)\n");;
  PrintTo(D176ShellStream,"test \"$(grep -Ec '^R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_PRODUCER_TERMINAL (R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS|R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_RESOURCE|R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_INPUT)$' ",D176ProducerLog,")\" -eq 1\n");;
  PrintTo(D176ShellStream,"timeout --signal=TERM --kill-after=60s 9600s python3 -u -B ",D176Checker,
    " --receipt ",D176Receipt," --verdict ",D176Verdict,
    " 2>&1 | tee ",D176CheckerLog,"\n");;
  PrintTo(D176ShellStream,"test ${PIPESTATUS[0]} -eq 0\np2=$(date +%s)\n");;
  PrintTo(D176ShellStream,"test \"$(grep -Ec '^R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_CHECKER_PASS terminal=(R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS|R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_RESOURCE|R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_UNKNOWN_INPUT)$' ",D176CheckerLog,")\" -eq 1\n");;
  PrintTo(D176ShellStream,"sha256sum ",D176Receipt," ",D176Verdict," > ",D176Hashes,"\n");;
  PrintTo(D176ShellStream,"printf 'mode=PRODUCTION producer_seconds=%s checker_seconds=%s\\n' \"$((p1-p0))\" \"$((p2-p1))\" > ",D176Timing,"\n");;
fi;
PrintTo(D176ShellStream,"touch ",D176OK,"\n");;
CloseStream(D176ShellStream);;
D176ShellRaw:=D176Read(D176Shell,"generated shell");;
if D176Count(D176ShellRaw,"\\\n")<>0 then
  Error("task176 driver: generated shell contains GAP formatting continuation");
fi;
Exec(Concatenation("bash ",D176Shell));;
if not IsExistingFile(D176OK) then Error("task176 driver: shell sentinel missing"); fi;

D176ProducerRaw:=D176Read(D176ProducerLog,"producer log");;
D176CheckerRaw:=D176Read(D176CheckerLog,"checker log");;
D176CleanLog(D176ProducerRaw,"producer");;
D176CleanLog(D176CheckerRaw,"checker");;
if D176Mode="SELFTEST" then
  if D176Count(D176ProducerRaw,"R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_PRODUCER_SELFTEST_PASS perm_type_checks=2 deleter_type_checks=6")<>1 or
     D176Count(D176CheckerRaw,"mutation_attempted=15 mutation_rejected=15 reject_envelope_checks=3 perm_type_checks=2 deleter_type_checks=6 linked_nonabelian_order=54")<>1 then
    Error("task176 driver: selftest markers");
  fi;
  D176Terminal:="SELFTEST";;
else
  D176ReceiptRaw:=D176Read(D176Receipt,"receipt");;
  D176VerdictRaw:=D176Read(D176Verdict,"verdict");;
  D176Terminal:=fail;;
  for D176Token in D176Terminals do
    if D176Count(D176ProducerRaw,Concatenation("PRODUCER_TERMINAL ",D176Token))=1 and
       D176Count(D176CheckerRaw,Concatenation("CHECKER_PASS terminal=",D176Token))=1 and
       D176Count(D176ReceiptRaw,Concatenation("\"terminal\":\"",D176Token,"\""))=1 and
       D176Count(D176VerdictRaw,Concatenation("\"receipt_terminal\":\"",D176Token,"\""))=1 then
      if D176Terminal<>fail then Error("task176 driver: multiple terminals"); fi;
      D176Terminal:=D176Token;;
    fi;
  od;
  if D176Terminal=fail then Error("task176 driver: no exact terminal"); fi;
  D176ReceiptAudit(D176ReceiptRaw,D176Terminal);;
  if D176Count(D176VerdictRaw,"\"self_digest_sha256\":\"")<>1 or
     D176Count(D176VerdictRaw,Concatenation("\"producer_sha256\":\"",D176ProducerSHA,"\""))<>1 or
     D176Count(D176VerdictRaw,"no all-seven solution/correction/cofinal/fake/Ihara")<>1 then
    Error("task176 driver: verdict boundary");
  fi;
fi;
if D176Mode="SELFTEST" then
  D176EmitCode:="SELFTEST";;
elif D176Terminal=D176Terminals[1] then
  D176EmitCode:="PASS";;
elif D176Terminal=D176Terminals[2] then
  D176EmitCode:="UNKNOWN_RESOURCE";;
elif D176Terminal=D176Terminals[3] then
  D176EmitCode:="UNKNOWN_INPUT";;
else
  Error("task176 driver: no external sentinel code");
fi;
Exec(Concatenation("bash ",D176Shell," --emit-driver-pass ",D176EmitCode));;
