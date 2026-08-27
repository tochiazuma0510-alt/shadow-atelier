## Task184 exact-commutator successor driver v1.  ASCII only.
if not IsBound(D972_R07_EXACT_COMMUTATOR_COMMON_WORD_V1_MODE) then Error("task184 driver: MODE required"); fi;
D184Mode:=D972_R07_EXACT_COMMUTATOR_COMMON_WORD_V1_MODE;;
if D184Mode<>"SELFTEST" and D184Mode<>"PRODUCTION" then Error("task184 driver: bad MODE"); fi;
D184Producer:="search/d972_r07_exact_commutator_common_word_v1.py";;
D184Checker:="crosscheck/check_d972_r07_exact_commutator_common_word_v1.py";;
D184Fixture:="search/certs/d972_r07_exact_commutator_common_word_selftest_v1_20260827.json";;
D184Receipt:="ci/out/d972_r07_exact_commutator_common_word_v1.json";;
D184Verdict:="ci/out/d972_r07_exact_commutator_common_word_verdict_v1.json";;
D184ProducerLog:="ci/out/d972_r07_exact_commutator_common_word_producer_v1.log";;
D184CheckerLog:="ci/out/d972_r07_exact_commutator_common_word_checker_v1.log";;
D184Shell:="ci/out/d972_r07_exact_commutator_common_word_command_v1.sh";;
D184OK:="ci/out/d972_r07_exact_commutator_common_word_v1.ok";;
D184Input:="ci/in/d972_r07_positive_common_word_colgen_v1.json";;
D184ProducerBytes:=28570;; D184ProducerSHA:="37f7b029e23eb95e97b8f521746630cd42dd42f88cfb5161aa87bd7f33b8d06e";;
D184CheckerBytes:=15778;; D184CheckerSHA:="8e03c8be8491f9957c76fdf7d94fdcc518c08a088d1614ea613d95218febaa8f";;
D184FixtureBytes:=307;; D184FixtureSHA:="ab45ef8d467c92b70d1716f8d4053d99f0dd35479b57898d12887a703393eec2";;
D184Read:=function(path,label) local raw; raw:=StringFile(path); if raw=fail then Error("task184 driver: missing ",label); fi; return raw; end;;
D184Pin:=function(path,size,digest) local raw; raw:=D184Read(path,"pin"); if Length(raw)<>size or HexSHA256(raw)<>digest then Error("task184 driver: pin drift ",path); fi; end;;
D184Clean:=function(raw,label) local bad; for bad in ["Traceback (most recent call last):","CHECKER_STOP","PRODUCER_STOP","SyntaxError","AssertionError","Killed"] do if PositionSublist(raw,bad)<>fail then Error("task184 driver: bad ",label); fi; od; end;;
D184Pin("sol/proof_r07_task179_relative_frattini_successor_v145.md",13819,"b08f140838b78424cafa9528eafbcab9442f94cf92ce2cb42e15fc88ed489a51");;
D184Pin("sol/proof_r07_exact_commutator_positive_common_word_v146.md",9065,"a167df351d55e82781cb60cd2b4dbfdf5cd2ea4f50251643a6e0b83332557cee");;
D184Pin(D184Fixture,D184FixtureBytes,D184FixtureSHA);;
D184Pin(D184Producer,D184ProducerBytes,D184ProducerSHA);;
D184Pin(D184Checker,D184CheckerBytes,D184CheckerSHA);;

for D184Path in [D184Receipt,D184Verdict,D184ProducerLog,D184CheckerLog,D184Shell,D184OK] do
  if IsExistingFile(D184Path) then Error("task184 driver: stale output ",D184Path); fi;
od;
D184Stream:=OutputTextFile(D184Shell,false);;
if D184Stream=fail then Error("task184 driver: shell open"); fi;
PrintTo(D184Stream,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");;
if D184Mode="SELFTEST" then
  PrintTo(D184Stream,"python3 -u -B ",D184Producer," --mode SELFTEST --output ",D184Receipt," 2>&1 | tee ",D184ProducerLog,"\n");;
  PrintTo(D184Stream,"test ${PIPESTATUS[0]} -eq 0\n");;
  PrintTo(D184Stream,"grep -Fxc 'R07_EXACT_COMMUTATOR_COMMON_WORD_V1_PRODUCER_SELFTEST_PASS mutations=17' ",D184ProducerLog,"\n");;
  PrintTo(D184Stream,"python3 -u -B ",D184Checker," --mode SELFTEST --receipt ",D184Receipt," --verdict ",D184Verdict," 2>&1 | tee ",D184CheckerLog,"\n");;
  PrintTo(D184Stream,"test ${PIPESTATUS[0]} -eq 0\n");;
  PrintTo(D184Stream,"grep -Fxc 'R07_EXACT_COMMUTATOR_COMMON_WORD_V1_CHECKER_SELFTEST_PASS mutations=17' ",D184CheckerLog,"\n");;
else
  if not IsExistingFile(D184Input) then Error("task184 driver: task179 input missing"); fi;
  if not IsBound(D972_R07_EXACT_COMMUTATOR_COMMON_WORD_V1_INPUT_SHA256) then
    Error("task184 driver: task179 input SHA required");
  fi;
  if HexSHA256(D184Read(D184Input,"task179 input"))<>
     D972_R07_EXACT_COMMUTATOR_COMMON_WORD_V1_INPUT_SHA256 then
    Error("task184 driver: task179 input pin drift");
  fi;
  PrintTo(D184Stream,"python3 -u -B ",D184Producer," --mode PRODUCTION --task179-receipt ",D184Input," --output ",D184Receipt," 2>&1 | tee ",D184ProducerLog,"\n");;
  PrintTo(D184Stream,"test ${PIPESTATUS[0]} -eq 0\n");;
  PrintTo(D184Stream,"python3 -u -B ",D184Checker," --mode PRODUCTION --receipt ",D184Receipt," --verdict ",D184Verdict," 2>&1 | tee ",D184CheckerLog,"\n");;
  PrintTo(D184Stream,"test ${PIPESTATUS[0]} -eq 0\n");;
fi;
CloseStream(D184Stream);;
D184ShellRaw:=D184Read(D184Shell,"generated shell");;
if PositionSublist(D184ShellRaw,"\\\n")<>fail then Error("task184 driver: wrapped shell"); fi;
Exec(Concatenation("bash ",D184Shell));;
D184ProducerRaw:=D184Read(D184ProducerLog,"producer log");; D184CheckerRaw:=D184Read(D184CheckerLog,"checker log");;
D184Clean(D184ProducerRaw,"producer");; D184Clean(D184CheckerRaw,"checker");;
if PositionSublist(D184ProducerRaw,"R07_EXACT_COMMUTATOR_COMMON_WORD_V1_PRODUCER_")=fail then Error("task184 driver: producer marker"); fi;
if PositionSublist(D184CheckerRaw,"R07_EXACT_COMMUTATOR_COMMON_WORD_V1_CHECKER_")=fail then Error("task184 driver: checker marker"); fi;
WriteLine(OutputTextUser(),Concatenation("R07_EXACT_COMMUTATOR_COMMON_WORD_V1_GHA_DRIVER_PASS mode=",D184Mode));;
