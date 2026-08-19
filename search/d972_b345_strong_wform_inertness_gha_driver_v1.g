#############################################################################
## d972_b345_strong_wform_inertness_gha_driver_v1.g
## Thin fail-closed same-job q3 -> producer -> independent-checker driver.
#############################################################################

D972T53Q3ProducerPath := "search/d972_b345_q3_chief_v1.g";;
D972T53Q3ProducerSHA :=
  "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755";;
D972T53Q3CheckerPath := "search/check_d972_b345_q3_chief_v1.py";;
D972T53Q3CheckerSHA :=
  "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73";;
D972T53Q3DriverPath := "search/d972_b345_q3_gha_driver_v1.g";;
D972T53Q3DriverSHA :=
  "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831";;
D972T53ProducerPath := "search/d972_b345_strong_wform_inertness_v1.py";;
D972T53ProducerSHA := "d41123a8c4803f6ac67387ac9bbf1a32f797b90d6233605a5511713f215244be";;
D972T53CheckerPath := "search/check_d972_b345_strong_wform_inertness_v1.py";;
D972T53CheckerSHA := "a8345c6c27fea24147dc7c310bbda48ea5bc08b7a0a720ded961af13a5b961e8";;
D972T53Q3Artifact := "ci/out/d972_b345_q3_chief_v1.json";;
D972T53Q3ArtifactSHA :=
  "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;
D972T53Artifact := "ci/out/d972_b345_strong_wform_inertness_v1.json";;
D972T53ArtifactSHAFile := "ci/out/d972_b345_strong_wform_inertness_v1.sha256";;
D972T53Q3Child := "ci/out/d972_b345_strong_wform_inertness_v1_q3_child.g";;
D972T53Q3ChildLog := "ci/out/d972_b345_strong_wform_inertness_v1_q3_child.log";;
D972T53Q3ChildOk := "ci/out/d972_b345_strong_wform_inertness_v1_q3_child.ok";;
D972T53ProducerLog := "ci/out/d972_b345_strong_wform_inertness_v1_producer.log";;
D972T53ProducerOk := "ci/out/d972_b345_strong_wform_inertness_v1_producer.ok";;
D972T53CheckerLog := "ci/out/d972_b345_strong_wform_inertness_v1_checker.log";;
D972T53CheckerOk := "ci/out/d972_b345_strong_wform_inertness_v1_checker.ok";;
D972T53SelfLog := "ci/out/d972_b345_strong_wform_inertness_v1_selftest.log";;
D972T53SelfOk := "ci/out/d972_b345_strong_wform_inertness_v1_selftest.ok";;
D972T53Q3ChildSentinel := "D972_B345_T53_STRONG_S_Q3_CHILD_EXIT_ZERO";;
D972T53ProducerSentinel := "D972_B345_T53_STRONG_S_PRODUCER_EXIT_ZERO";;
D972T53CheckerSentinel := "D972_B345_T53_STRONG_S_CHECKER_EXIT_ZERO";;
D972T53SelfSentinel := "D972_B345_T53_STRONG_S_SELFTEST_EXIT_ZERO";;

D972T53RequireSHA := function(path,expected)
  local raw,got;
  raw:=StringFile(path);;
  if raw=fail then Error("157ea driver: missing source ",path); fi;
  got:=HexSHA256(raw);;
  if got<>expected then Error("157ea driver: source SHA drift ",path," got=",got); fi;
  return true;
end;;

D972T53Count := function(text,needle)
  local i,n,m,count;
  if not IsString(text) or not IsString(needle) or Length(needle)=0 then
    Error("157ea driver: occurrence input");
  fi;
  n:=Length(text);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if text{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972T53ReadRequired := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("157ea driver: missing ",label); fi;
  return raw;
end;;

D972T53CheckedWrite := function(path,text)
  local stream,got;
  stream:=OutputTextFile(path,false);;
  if stream=fail then Error("157ea driver: q3 child script open"); fi;
  SetPrintFormattingStatus(stream,false);;
  PrintTo(stream,text);;
  CloseStream(stream);;
  got:=StringFile(path);;
  if got=fail or got<>text then Error("157ea driver: q3 child script readback"); fi;
  return true;
end;;

D972T53RequireSHA(D972T53Q3ProducerPath,D972T53Q3ProducerSHA);;
D972T53RequireSHA(D972T53Q3CheckerPath,D972T53Q3CheckerSHA);;
D972T53RequireSHA(D972T53Q3DriverPath,D972T53Q3DriverSHA);;
D972T53RequireSHA(D972T53ProducerPath,D972T53ProducerSHA);;
D972T53RequireSHA(D972T53CheckerPath,D972T53CheckerSHA);;

D972T53Self:=IsBound(D972_B345_T53_STRONG_S_SELFTEST) and
  D972_B345_T53_STRONG_S_SELFTEST=true;;
D972T53Full:=IsBound(D972_B345_T53_STRONG_S_RUN) and
  D972_B345_T53_STRONG_S_RUN=true;;
if D972T53Self=D972T53Full then
  Error("157ea driver: select exactly one of SELFTEST and RUN");
fi;

if D972T53Self then
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_strong_wform_inertness_v1_selftest.log' 'ci/out/d972_b345_strong_wform_inertness_v1_selftest.ok' && python3 -u -B search/d972_b345_strong_wform_inertness_v1.py --self-test > 'ci/out/d972_b345_strong_wform_inertness_v1_selftest.log' 2>&1 && python3 -u -B search/check_d972_b345_strong_wform_inertness_v1.py --self-test >> 'ci/out/d972_b345_strong_wform_inertness_v1_selftest.log' 2>&1 && printf '%s' 'D972_B345_T53_STRONG_S_SELFTEST_EXIT_ZERO' > 'ci/out/d972_b345_strong_wform_inertness_v1_selftest.ok'");;
  D972T53SelfRaw:=D972T53ReadRequired(D972T53SelfLog,"selftest log");;
  if StringFile(D972T53SelfOk)<>D972T53SelfSentinel then
    Error("157ea driver: combined selftest did not exit zero");
  fi;
  if D972T53Count(D972T53SelfRaw,
       "D972_B345_T53_STRONG_S_PRODUCER_SELFTEST_PASS")<>1 or
     D972T53Count(D972T53SelfRaw,
       "B345_T53_STRONG_S_INERTNESS_CHECKER_SELFTEST_PASS")<>1 then
    Error("157ea driver: combined selftest marker count");
  fi;
  Print(D972T53SelfRaw,"\n");;
  Print("B345_T53_STRONG_S_INERTNESS_GHA_DRIVER_PASS mode=selftest\n");;
else
  if not IsBound(D972_B345_T53_STRONG_S_OUTPUT) or
     D972_B345_T53_STRONG_S_OUTPUT<>D972T53Artifact then
    Error("157ea driver: full output must be fixed ci/out artifact");
  fi;
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_q3_chief_v1.json' 'ci/out/d972_b345_q3_checker_full.log' 'ci/out/d972_b345_q3_checker_full.ok' 'ci/out/d972_b345_strong_wform_inertness_v1_q3_child.g' 'ci/out/d972_b345_strong_wform_inertness_v1_q3_child.log' 'ci/out/d972_b345_strong_wform_inertness_v1_q3_child.ok' 'ci/out/d972_b345_strong_wform_inertness_v1.json' 'ci/out/d972_b345_strong_wform_inertness_v1.sha256' 'ci/out/d972_b345_strong_wform_inertness_v1_producer.log' 'ci/out/d972_b345_strong_wform_inertness_v1_producer.ok' 'ci/out/d972_b345_strong_wform_inertness_v1_checker.log' 'ci/out/d972_b345_strong_wform_inertness_v1_checker.ok'");;
  D972T53Q3ChildText:=Concatenation(
    "if GAPInfo.Version<>\"4.16.0\" then Error(\"GAP 4.16.0 required\"); fi;;\n",
    "if LoadPackage(\"smallgrp\")<>true then Error(\"smallgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"autpgrp\")<>true then Error(\"autpgrp LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"anupq\")<>true then Error(\"anupq LoadPackage failed\"); fi;;\n",
    "if LoadPackage(\"json\")<>true then Error(\"json LoadPackage failed\"); fi;;\n",
    "D972_B345_Q3_RUN:=true;;\n",
    "D972_B345_Q3_OUTPUT:=\"ci/out/d972_b345_q3_chief_v1.json\";;\n",
    "Read(\"search/d972_b345_q3_gha_driver_v1.g\");;\n",
    "QUIT_GAP(0);;\n");;
  D972T53CheckedWrite(D972T53Q3Child,D972T53Q3ChildText);;
  Exec("bash -o pipefail -c 'gap -l \";/usr/share/gap;/usr/lib/gap;${GAP_P2_PACKAGE_ROOT:?}\" --quitonbreak -q -o 12g ci/out/d972_b345_strong_wform_inertness_v1_q3_child.g 2>&1 | tee ci/out/d972_b345_strong_wform_inertness_v1_q3_child.log' && printf '%s' 'D972_B345_T53_STRONG_S_Q3_CHILD_EXIT_ZERO' > 'ci/out/d972_b345_strong_wform_inertness_v1_q3_child.ok'");;
  D972T53Q3ChildRaw:=D972T53ReadRequired(D972T53Q3ChildLog,"q3 child log");;
  if StringFile(D972T53Q3ChildOk)<>D972T53Q3ChildSentinel then
    Error("157ea driver: q3 child did not exit zero");
  fi;
  D972T53Q3Raw:=D972T53ReadRequired(D972T53Q3Artifact,"q3 artifact");;
  if HexSHA256(D972T53Q3Raw)<>D972T53Q3ArtifactSHA then
    Error("157ea driver: regenerated q3 artifact SHA drift");
  fi;
  D972T53Q3CheckerRaw:=D972T53ReadRequired(
    "ci/out/d972_b345_q3_checker_full.log","q3 checker log");;
  if StringFile("ci/out/d972_b345_q3_checker_full.ok")<>
       "D972_B345_Q3_CHECKER_FULL_EXIT_ZERO" or
     D972T53Count(D972T53Q3CheckerRaw,"B345_Q3_CHECKER_PASS")<>1 then
    Error("157ea driver: q3 checker gate");
  fi;
  Print("D972_B345_T53_STRONG_S_DRIVER_PHASE q3_crosschecked\n");;
  Exec("bash -o pipefail -c 'python3 -u -B search/d972_b345_strong_wform_inertness_v1.py --q3 ci/out/d972_b345_q3_chief_v1.json --output ci/out/d972_b345_strong_wform_inertness_v1.json 2>&1 | tee ci/out/d972_b345_strong_wform_inertness_v1_producer.log' && printf '%s' 'D972_B345_T53_STRONG_S_PRODUCER_EXIT_ZERO' > 'ci/out/d972_b345_strong_wform_inertness_v1_producer.ok'");;
  D972T53ProducerRaw:=D972T53ReadRequired(D972T53ProducerLog,"producer log");;
  if StringFile(D972T53ProducerOk)<>D972T53ProducerSentinel then
    Error("157ea driver: producer did not exit zero");
  fi;
  D972T53TerminalCount:=0;;
  for D972T53Token in [
      "B345_T53_STRONG_S_EXACT_TYPED_INERT",
      "B345_T53_STRONG_S_PREFIX_INCOMPLETE",
      "B345_T53_STRONG_S_UNKNOWN_RESOURCE",
      "B345_T53_STRONG_S_UNKNOWN_INPUT"] do
    D972T53TerminalCount:=D972T53TerminalCount+
      D972T53Count(D972T53ProducerRaw,D972T53Token);;
  od;
  if D972T53TerminalCount<>1 then
    Error("157ea driver: producer terminal marker count");
  fi;
  Print("D972_B345_T53_STRONG_S_DRIVER_PHASE producer_complete\n");;
  Exec("bash -o pipefail -c 'python3 -u -B search/check_d972_b345_strong_wform_inertness_v1.py --q3 ci/out/d972_b345_q3_chief_v1.json --receipt ci/out/d972_b345_strong_wform_inertness_v1.json 2>&1 | tee ci/out/d972_b345_strong_wform_inertness_v1_checker.log' && printf '%s' 'D972_B345_T53_STRONG_S_CHECKER_EXIT_ZERO' > 'ci/out/d972_b345_strong_wform_inertness_v1_checker.ok'");;
  D972T53CheckerRaw:=D972T53ReadRequired(D972T53CheckerLog,"checker log");;
  if StringFile(D972T53CheckerOk)<>D972T53CheckerSentinel or
     D972T53Count(D972T53CheckerRaw,
       "B345_T53_STRONG_S_INERTNESS_CHECKER_PASS")<>1 then
    Error("157ea driver: independent checker gate");
  fi;
  Exec("sha256sum 'ci/out/d972_b345_strong_wform_inertness_v1.json' | awk '{printf \"%s\",$1}' > 'ci/out/d972_b345_strong_wform_inertness_v1.sha256'");;
  D972T53ArtifactSHAValue:=D972T53ReadRequired(
    D972T53ArtifactSHAFile,"T53 artifact SHA");;
  if Length(D972T53ArtifactSHAValue)<>64 then
    Error("157ea driver: artifact SHA length");
  fi;
  Print("B345_T53_STRONG_S_INERTNESS_GHA_DRIVER_PASS mode=full artifact_sha256=",
    D972T53ArtifactSHAValue,"\n");;
fi;
