#############################################################################
## d972_b345_relfrat3_wordexpr_memo_gha_driver_v10.g
##
## Fail-closed checker-only v10 successor for the frozen WordExpr-memo-v9
## producer.  The q3 producer/checker run once in a separate GAP child, which
## exits before the Python search.  The v9 artifact/schema remain unchanged.
#############################################################################

D972RF3Q3DriverPath := "search/d972_b345_q3_gha_driver_v1.g";;
D972RF3Q3DriverSHA :=
  "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831";;
D972RF3ProducerPath := "search/d972_b345_relfrat3_wordexpr_memo_v9.py";;
D972RF3ProducerSHA :=
  "7dede323c3c52bc7cf7d99af6d542b3683823879a4bb3e340aca8ce53dcf196f";;
D972RF3CheckerPath := "search/check_d972_b345_relfrat3_wordexpr_memo_v10.py";;
D972RF3CheckerSHA :=
  "264258dcb945401e3db10ecd4fedd7a8dd79a8d7b0f31dbc0cfbe643537eac2d";;
D972RF3V8ProducerPath := "search/d972_b345_relfrat3_wordexpr_v8.py";;
D972RF3V8ProducerSHA :=
  "ea2c2901e316bfaa1c42d3f9966de5ec76323139728dfef46d2032608997e8db";;
D972RF3V8CheckerPath := "search/check_d972_b345_relfrat3_wordexpr_v8.py";;
D972RF3V8CheckerSHA :=
  "9d3368504953862e688f474871e72cdc1ae4153e4737b8b6260ba260804db413";;
D972RF3V8DriverPath := "search/d972_b345_relfrat3_wordexpr_gha_driver_v8.g";;
D972RF3V8DriverSHA :=
  "63e9a8dcc87c446fb130665dfe94c29cbe0836f1b87682f9b5ac4a7eb7c25018";;
D972RF3V7ProducerPath := "search/d972_b345_relfrat3_pivot_surgery_v7.py";;
D972RF3V7ProducerSHA :=
  "a19c3353c5cfc6da8ad0b7d941ba94bde043c80e69e33c889c5710c897d7a757";;
D972RF3V7CheckerPath := "search/check_d972_b345_relfrat3_pivot_surgery_v7.py";;
D972RF3V7CheckerSHA :=
  "fbe033704180a808320c897c52613ca6847305dd85ddcd7a70aa825161e8bfa0";;
D972RF3V7DriverPath := "search/d972_b345_relfrat3_pivot_surgery_gha_driver_v7.g";;
D972RF3V7DriverSHA :=
  "1be0ec44674108a2f6319057ba18283206756cf2ef73bfe1e1e5896a6f893d8d";;
D972RF3V6ProducerPath := "search/d972_b345_relfrat3_fixed_candidate_v6.py";;
D972RF3V6ProducerSHA :=
  "178c7e63dafba0b9deb8b4e363552ff87a0b7d1c2a120457f593845d56d9d493";;
D972RF3V6CheckerPath := "search/check_d972_b345_relfrat3_fixed_candidate_v6.py";;
D972RF3V6CheckerSHA :=
  "12c5475c984aa2855c502930169a01cc656ec67507a6aa56d098cd314db011fd";;
D972RF3V6DriverPath := "search/d972_b345_relfrat3_fixed_candidate_gha_driver_v6.g";;
D972RF3V6DriverSHA :=
  "2b36db96d440316292d271c22e662da507dc6afeba20aa0222c8388bab6f4ada";;
D972RF3V5ProducerPath := "search/d972_b345_relfrat3_fixed_candidate_v5.py";;
D972RF3V5ProducerSHA :=
  "e4675906601714ee16219d747cf95ffef54b19e354228dd6e7d3cd99d59127ea";;
D972RF3V5CheckerPath := "search/check_d972_b345_relfrat3_fixed_candidate_v5.py";;
D972RF3V5CheckerSHA :=
  "0cb7e0173fe022f304010c64ef89b7200464f4ad8c1e1bc7c3ad4001ffe12246";;
D972RF3V5DriverPath := "search/d972_b345_relfrat3_fixed_candidate_gha_driver_v5.g";;
D972RF3V5DriverSHA :=
  "3bcb19326bfff1e313870a64cca95840b0e581aa1f7c713ee18300faf149261d";;
D972RF3V4ProducerPath := "search/d972_b345_relfrat3_v4.py";;
D972RF3V4ProducerSHA :=
  "ff2e021647fdaf84697c91f741f2d039575036bc1f389d9dc59dee512e6ca7e1";;
D972RF3V4CheckerPath := "search/check_d972_b345_relfrat3_v4.py";;
D972RF3V4CheckerSHA :=
  "54308d8628cd434bbc6a4522fe86296d72d01b42de8db2bc72ea9a6961157c2b";;
D972RF3V4DriverPath := "search/d972_b345_relfrat3_gha_driver_v4.g";;
D972RF3V4DriverSHA :=
  "b717b6a214913d26207ba4683bbe0403123d5139b5aa45cd7bba62be2b885d56";;
D972RF3V3ProducerPath := "search/d972_b345_relfrat3_v3.py";;
D972RF3V3ProducerSHA :=
  "df60849f9fa4bb6a09e0d23d799e31473960544728db6eb5507a6fd54749343b";;
D972RF3V3CheckerPath := "search/check_d972_b345_relfrat3_v3.py";;
D972RF3V3CheckerSHA :=
  "11345a8db5ff6d08fa8395301c270532d0d96714cc8d77d98643dac04a6856cf";;
D972RF3V3DriverPath := "search/d972_b345_relfrat3_gha_driver_v3.g";;
D972RF3V3DriverSHA :=
  "fe7a76191a484194696931c5acb59ec6ee0115af75d543613281c28e4d6a4d7a";;
D972RF3V2ProducerPath := "search/d972_b345_relfrat3_v2.py";;
D972RF3V2ProducerSHA :=
  "fad364043926dbdc03e56accf089f454d625e0b315c98a7647bc891677313cc8";;
D972RF3V2CheckerPath := "search/check_d972_b345_relfrat3_v2.py";;
D972RF3V2CheckerSHA :=
  "3c8967bea6946b42cef08cd097eab4e9071aae203ee27ac38038c4d5adb83f07";;
D972RF3V2DriverPath := "search/d972_b345_relfrat3_gha_driver_v2.g";;
D972RF3V2DriverSHA :=
  "006e33e97c6f9ac1982887206c904dbcf423c95790ec2fe0c45d9a1b3a2e38aa";;
D972RF3V1ProducerPath := "search/d972_b345_relfrat3_v1.py";;
D972RF3V1ProducerSHA :=
  "4b73fbfe19bb33a9decdec5fda437f58f61a3ecb1989090bd08151f60ce6609e";;
D972RF3V1CheckerPath := "search/check_d972_b345_relfrat3_v1.py";;
D972RF3V1CheckerSHA :=
  "3d86240237229b250943c4795c24c32ac75af9229534c73d16bd838f6d6d0101";;
D972RF3V1DriverPath := "search/d972_b345_relfrat3_gha_driver_v1.g";;
D972RF3V1DriverSHA :=
  "fce9b3ba8c9b686fb6af2bd5a6da1b29f7486616948a6907982af14cd5d8738b";;
D972RF3Q3Artifact := "ci/out/d972_b345_q3_chief_v1.json";;
D972RF3Q3ArtifactSHA :=
  "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;
D972RF3Artifact := "ci/out/d972_b345_relfrat3_wordexpr_memo_v9.json";;
D972RF3ArtifactSHAFile := "ci/out/d972_b345_relfrat3_wordexpr_memo_v10.sha256";;
D972RF3Q3Child := "ci/out/d972_b345_relfrat3_wordexpr_memo_v10_q3_child.g";;
D972RF3Q3ChildLog := "ci/out/d972_b345_relfrat3_wordexpr_memo_v10_q3_child.log";;
D972RF3Q3ChildOk := "ci/out/d972_b345_relfrat3_wordexpr_memo_v10_q3_child.ok";;
D972RF3ProducerLog := "ci/out/d972_b345_relfrat3_wordexpr_memo_v10_producer.log";;
D972RF3ProducerOk := "ci/out/d972_b345_relfrat3_wordexpr_memo_v10_producer.ok";;
D972RF3CheckerLog := "ci/out/d972_b345_relfrat3_wordexpr_memo_v10_checker.log";;
D972RF3CheckerOk := "ci/out/d972_b345_relfrat3_wordexpr_memo_v10_checker.ok";;
D972RF3SelfLog := "ci/out/d972_b345_relfrat3_wordexpr_memo_v10_selftest.log";;
D972RF3SelfOk := "ci/out/d972_b345_relfrat3_wordexpr_memo_v10_selftest.ok";;
D972RF3Q3ChildSentinel := "D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_Q3_CHILD_EXIT_ZERO";;
D972RF3ProducerSentinel := "D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_PRODUCER_EXIT_ZERO";;
D972RF3CheckerSentinel := "D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_CHECKER_EXIT_ZERO";;
D972RF3SelfSentinel := "D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_SELFTEST_EXIT_ZERO";;

D972RF3RequireSHA := function(path,expected)
  local raw,got;
  raw:=StringFile(path);;
  if raw=fail then Error("157dz checker pool-schedule v10 driver: missing source ",path); fi;
  got:=HexSHA256(raw);;
  if got<>expected then
    Error("157dz checker pool-schedule v10 driver: source SHA drift ",path," got=",got);
  fi;
  return true;
end;;

D972RF3Count := function(text,needle)
  local i,n,m,count;
  if not IsString(text) or not IsString(needle) or Length(needle)=0 then
    Error("157dz checker pool-schedule v10 driver: occurrence input");
  fi;
  n:=Length(text);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if text{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972RF3ReadRequired := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("157dz checker pool-schedule v10 driver: missing ",label); fi;
  return raw;
end;;

D972RF3CheckedWrite := function(path,text)
  local stream,got;
  stream:=OutputTextFile(path,false);;
  if stream=fail then Error("157dz checker pool-schedule v10 driver: child script open"); fi;
  SetPrintFormattingStatus(stream,false);;
  PrintTo(stream,text);;
  CloseStream(stream);;
  got:=StringFile(path);;
  if got=fail or got<>text then Error("157dz checker pool-schedule v10 driver: child script readback"); fi;
  return true;
end;;

D972RF3RequireSHA(D972RF3Q3DriverPath,D972RF3Q3DriverSHA);;
D972RF3RequireSHA(D972RF3ProducerPath,D972RF3ProducerSHA);;
D972RF3RequireSHA(D972RF3CheckerPath,D972RF3CheckerSHA);;
D972RF3RequireSHA(D972RF3V8ProducerPath,D972RF3V8ProducerSHA);;
D972RF3RequireSHA(D972RF3V8CheckerPath,D972RF3V8CheckerSHA);;
D972RF3RequireSHA(D972RF3V8DriverPath,D972RF3V8DriverSHA);;
D972RF3RequireSHA(D972RF3V7ProducerPath,D972RF3V7ProducerSHA);;
D972RF3RequireSHA(D972RF3V7CheckerPath,D972RF3V7CheckerSHA);;
D972RF3RequireSHA(D972RF3V7DriverPath,D972RF3V7DriverSHA);;
D972RF3RequireSHA(D972RF3V6ProducerPath,D972RF3V6ProducerSHA);;
D972RF3RequireSHA(D972RF3V6CheckerPath,D972RF3V6CheckerSHA);;
D972RF3RequireSHA(D972RF3V6DriverPath,D972RF3V6DriverSHA);;
D972RF3RequireSHA(D972RF3V5ProducerPath,D972RF3V5ProducerSHA);;
D972RF3RequireSHA(D972RF3V5CheckerPath,D972RF3V5CheckerSHA);;
D972RF3RequireSHA(D972RF3V5DriverPath,D972RF3V5DriverSHA);;
D972RF3RequireSHA(D972RF3V4ProducerPath,D972RF3V4ProducerSHA);;
D972RF3RequireSHA(D972RF3V4CheckerPath,D972RF3V4CheckerSHA);;
D972RF3RequireSHA(D972RF3V4DriverPath,D972RF3V4DriverSHA);;
D972RF3RequireSHA(D972RF3V3ProducerPath,D972RF3V3ProducerSHA);;
D972RF3RequireSHA(D972RF3V3CheckerPath,D972RF3V3CheckerSHA);;
D972RF3RequireSHA(D972RF3V3DriverPath,D972RF3V3DriverSHA);;
D972RF3RequireSHA(D972RF3V2ProducerPath,D972RF3V2ProducerSHA);;
D972RF3RequireSHA(D972RF3V2CheckerPath,D972RF3V2CheckerSHA);;
D972RF3RequireSHA(D972RF3V2DriverPath,D972RF3V2DriverSHA);;
D972RF3RequireSHA(D972RF3V1ProducerPath,D972RF3V1ProducerSHA);;
D972RF3RequireSHA(D972RF3V1CheckerPath,D972RF3V1CheckerSHA);;
D972RF3RequireSHA(D972RF3V1DriverPath,D972RF3V1DriverSHA);;

D972RF3Self:=IsBound(D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_SELFTEST) and
  D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_SELFTEST=true;;
D972RF3Full:=IsBound(D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_RUN) and
  D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_RUN=true;;
if D972RF3Self=D972RF3Full then
  Error("157dz checker pool-schedule v10 driver: select exactly one of SELFTEST and RUN");
fi;

if D972RF3Self then
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_selftest.log' 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_selftest.ok' && python3 -u -B search/d972_b345_relfrat3_wordexpr_memo_v9.py --self-test > 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_selftest.log' 2>&1 && python3 -u -B search/check_d972_b345_relfrat3_wordexpr_memo_v10.py --self-test >> 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_selftest.log' 2>&1 && printf '%s' 'D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_SELFTEST_EXIT_ZERO' > 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_selftest.ok'");;
  D972RF3SelfRaw:=D972RF3ReadRequired(D972RF3SelfLog,"selftest log");;
  if StringFile(D972RF3SelfOk)<>D972RF3SelfSentinel then
    Error("157dz checker pool-schedule v10 driver: selftests did not exit zero");
  fi;
  if D972RF3Count(D972RF3SelfRaw,
       "D972_B345_RELFRAT3_WORDEXPR_MEMO_V9_PRODUCER_SELFTEST_PASS")<>1 or
     D972RF3Count(D972RF3SelfRaw,
       "D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_CHECKER_SELFTEST_PASS")<>1 then
    Error("157dz checker pool-schedule v10 driver: selftest marker count");
  fi;
  Print(D972RF3SelfRaw,"\n");;
  Print("B345_RELFRAT3_WORDEXPR_MEMO_V10_GHA_DRIVER_PASS mode=selftest\n");;
else
  if not IsBound(D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_OUTPUT) or
     D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_OUTPUT<>D972RF3Artifact then
    Error("157dz checker pool-schedule v10 driver: full output must be fixed ci/out artifact");
  fi;
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_q3_chief_v1.json' 'ci/out/d972_b345_q3_checker_full.log' 'ci/out/d972_b345_q3_checker_full.ok' 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_q3_child.g' 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_q3_child.log' 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_q3_child.ok' 'ci/out/d972_b345_relfrat3_wordexpr_memo_v9.json' 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10.sha256' 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_producer.log' 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_producer.ok' 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_checker.log' 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_checker.ok'");;
  D972RF3Q3ChildText:=Concatenation(
    "if GAPInfo.Version<>\"4.16.0\" then Error(\"GAP 4.16.0 required\"); fi;;\n",
    "if LoadPackage(\"smallgrp\")<>true then Error(\"smallgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"autpgrp\")<>true then Error(\"autpgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"anupq\")<>true then Error(\"anupq LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"json\")<>true then Error(\"json LoadPackage failed\"); fi;;\n",
    "D972_B345_Q3_RUN:=true;;\n",
    "D972_B345_Q3_OUTPUT:=\"ci/out/d972_b345_q3_chief_v1.json\";;\n",
    "Read(\"search/d972_b345_q3_gha_driver_v1.g\");;\n",
    "QUIT_GAP(0);;\n");;
  D972RF3CheckedWrite(D972RF3Q3Child,D972RF3Q3ChildText);;
  Exec("bash -o pipefail -c 'gap -l \";/usr/share/gap;/usr/lib/gap;${GAP_P2_PACKAGE_ROOT:?}\" --quitonbreak -q -o 12g ci/out/d972_b345_relfrat3_wordexpr_memo_v10_q3_child.g 2>&1 | tee ci/out/d972_b345_relfrat3_wordexpr_memo_v10_q3_child.log' && printf '%s' 'D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_Q3_CHILD_EXIT_ZERO' > 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_q3_child.ok'");;
  D972RF3Q3ChildRaw:=D972RF3ReadRequired(D972RF3Q3ChildLog,"q3 child log");;
  if StringFile(D972RF3Q3ChildOk)<>D972RF3Q3ChildSentinel then
    Error("157dz checker pool-schedule v10 driver: q3 child did not exit zero");
  fi;
  D972RF3Q3Raw:=D972RF3ReadRequired(D972RF3Q3Artifact,"q3 artifact");;
  if HexSHA256(D972RF3Q3Raw)<>D972RF3Q3ArtifactSHA then
    Error("157dz checker pool-schedule v10 driver: regenerated q3 artifact SHA drift");
  fi;
  D972RF3Q3CheckerRaw:=D972RF3ReadRequired(
    "ci/out/d972_b345_q3_checker_full.log","q3 checker log");;
  if StringFile("ci/out/d972_b345_q3_checker_full.ok")<>
       "D972_B345_Q3_CHECKER_FULL_EXIT_ZERO" or
     D972RF3Count(D972RF3Q3CheckerRaw,"B345_Q3_CHECKER_PASS")<>1 then
    Error("157dz checker pool-schedule v10 driver: q3 checker gate");
  fi;
  Exec("bash -o pipefail -c 'python3 -u -B search/d972_b345_relfrat3_wordexpr_memo_v9.py ci/out/d972_b345_q3_chief_v1.json ci/out/d972_b345_relfrat3_wordexpr_memo_v9.json 2>&1 | tee ci/out/d972_b345_relfrat3_wordexpr_memo_v10_producer.log' && printf '%s' 'D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_PRODUCER_EXIT_ZERO' > 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_producer.ok'");;
  D972RF3ProducerRaw:=D972RF3ReadRequired(D972RF3ProducerLog,"producer log");;
  if StringFile(D972RF3ProducerOk)<>D972RF3ProducerSentinel then
    Error("157dz checker pool-schedule v10 driver: producer did not exit zero");
  fi;
  D972RF3TerminalCount:=0;;
  for D972RF3Token in [
      "B345_RELFRAT3_WORDEXPR_PASS",
      "B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE",
      "B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE",
      "B345_RELFRAT3_WORDEXPR_UNKNOWN_INPUT"] do
    D972RF3TerminalCount:=D972RF3TerminalCount+
      D972RF3Count(D972RF3ProducerRaw,D972RF3Token);;
  od;
  if D972RF3TerminalCount<>1 then
    Error("157dz checker pool-schedule v10 driver: producer terminal marker count");
  fi;
  Exec("bash -o pipefail -c 'python3 -u -B search/check_d972_b345_relfrat3_wordexpr_memo_v10.py ci/out/d972_b345_q3_chief_v1.json ci/out/d972_b345_relfrat3_wordexpr_memo_v9.json 2>&1 | tee ci/out/d972_b345_relfrat3_wordexpr_memo_v10_checker.log' && printf '%s' 'D972_B345_RELFRAT3_WORDEXPR_MEMO_V10_CHECKER_EXIT_ZERO' > 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10_checker.ok'");;
  D972RF3CheckerRaw:=D972RF3ReadRequired(D972RF3CheckerLog,"checker log");;
  if StringFile(D972RF3CheckerOk)<>D972RF3CheckerSentinel or
     D972RF3Count(D972RF3CheckerRaw,
       "B345_RELFRAT3_WORDEXPR_MEMO_V10_CHECKER_PASS")<>1 then
    Error("157dz checker pool-schedule v10 driver: checker gate");
  fi;
  Exec("sha256sum 'ci/out/d972_b345_relfrat3_wordexpr_memo_v9.json' | awk '{printf \"%s\",$1}' > 'ci/out/d972_b345_relfrat3_wordexpr_memo_v10.sha256'");;
  D972RF3ArtifactSHAValue:=D972RF3ReadRequired(
    D972RF3ArtifactSHAFile,"relative artifact SHA");;
  if Length(D972RF3ArtifactSHAValue)<>64 then
    Error("157dz checker pool-schedule v10 driver: relative artifact SHA length");
  fi;
  Print("B345_RELFRAT3_WORDEXPR_MEMO_V10_GHA_DRIVER_PASS mode=full artifact_sha256=",
    D972RF3ArtifactSHAValue,"\n");;
fi;
