#############################################################################
## d972_b34_a5_selected_lift_gha_driver_v1.g
##
## Thin fail-closed same-job driver.  Upstreams run in separate GAP processes
## so their global producers cannot contaminate the registered 157dp process.
#############################################################################

if LoadPackage("json")<>true then Error("157dp driver: GAP json unavailable"); fi;;

D972A5LGDProducerPath := "search/d972_b34_a5_selected_lift_v1.g";;
D972A5LGDProducerSHA := "ed350659ea6f77c0151e84e92395b050e7c0d65455c2e8e8a7d9851af9393440";;
D972A5LGDCheckerPath := "search/check_d972_b34_a5_selected_lift_v1.py";;
D972A5LGDCheckerSHA := "e4bd98a491c1017ebae2c8529318935e2bff613436d8c1a57bcb64fbf0dfcaa6";;
D972A5LGDQ3DriverPath := "search/d972_b345_q3_gha_driver_v1.g";;
D972A5LGDQ3DriverSHA := "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831";;
D972A5LGDFC8DriverPath := "search/d972_b4_fc8_a5four_gha_driver_v1.g";;
D972A5LGDFC8DriverSHA := "806d8bfa32ecb1f24f0873147da9e13b56fa171294f081cdd321894b77c545af";;
D972A5LGDQ3Artifact := "ci/out/d972_b345_q3_chief_v1.json";;
D972A5LGDQ3ArtifactSHA := "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;
D972A5LGDFC8Artifact := "ci/out/d972_b4_fc8_a5four_v1.json";;
D972A5LGDFC8ArtifactSHA := "558faee7864ab1162aaa40a9d2e2ad7bd1926987561cde9e3d3a9ee69690c584";;
D972A5LGDArtifact := "ci/out/d972_b34_a5_selected_lift_v1.json";;
D972A5LGDPositive := "B34_A5_LAYER_FIXED_OUTSIDE_ROOF_LIFT_CROSSCHECKED";;
D972A5LGDNegative := "B4_A_FIXED_OUTSIDE_ROOF_FIBRE_OBSTRUCTION_CROSSCHECKED";;
D972A5LGDUnknown := "B34_A5_LAYER_UNKNOWN_RESOURCE";;
D972A5LGDSelfLog := "ci/out/d972_b34_a5_selected_lift_checker_selftest.log";;
D972A5LGDSelfOK := "ci/out/d972_b34_a5_selected_lift_checker_selftest.ok";;
D972A5LGDFullLog := "ci/out/d972_b34_a5_selected_lift_checker_full.log";;
D972A5LGDFullOK := "ci/out/d972_b34_a5_selected_lift_checker_full.ok";;

D972A5LGDRequireSHA := function(path,expected,label)
  local raw,got;
  raw:=StringFile(path);;
  if raw=fail then Error("157dp driver: missing ",label," ",path); fi;
  got:=HexSHA256(raw);;
  if got<>expected then Error("157dp driver: SHA drift ",label," got=",got); fi;
  return raw;
end;;

D972A5LGDCount := function(raw,needle)
  local n,m,i,count;
  if raw=fail or not IsString(raw) or Length(needle)=0 then return 0; fi;
  n:=Length(raw);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972A5LGDEscape := function(s)
  local z;
  z:=ReplacedString(s,"\\","\\\\");;
  z:=ReplacedString(z,"\"","\\\"");;
  z:=ReplacedString(z,"\n","\\n");;
  z:=ReplacedString(z,"\r","\\r");;
  z:=ReplacedString(z,"\t","\\t");;
  return z;
end;;

D972A5LGDJson := function(x)
  local names,parts,n;
  if x=fail then return "null"; fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",D972A5LGDEscape(x),"\""); fi;
  if IsRecord(x) then
    names:=ShallowCopy(RecNames(x));; Sort(names);; parts:=[];;
    for n in names do Add(parts,Concatenation(D972A5LGDJson(n),":",D972A5LGDJson(x.(n)))); od;
    return Concatenation("{",JoinStringsWithSeparator(parts,","),"}");
  fi;
  if IsList(x) then
    return Concatenation("[",JoinStringsWithSeparator(List(x,D972A5LGDJson),","),"]");
  fi;
  Error("157dp driver: unsupported JSON value");
end;;

D972A5LGDCheckedWrite := function(path,obj)
  local expected,f,actual;
  expected:=Concatenation(D972A5LGDJson(obj),"\n");;
  f:=OutputTextFile(path,false);;
  if f=fail then Error("157dp driver: output open failed ",path); fi;
  SetPrintFormattingStatus(f,false);; PrintTo(f,expected);; CloseStream(f);;
  actual:=StringFile(path);;
  if actual=fail or actual<>expected then Error("157dp driver: output readback drift"); fi;
end;;

D972A5LGDRequireLog := function(logPath,okPath,sentinel,markers)
  local raw,m;
  raw:=StringFile(logPath);;
  if StringFile(okPath)<>sentinel or raw=fail then
    if raw<>fail then Print(raw,"\n"); fi;
    Error("157dp driver: subprocess did not exit zero ",logPath);
  fi;
  for m in markers do
    if D972A5LGDCount(raw,m)<>1 then
      Print(raw,"\n");; Error("157dp driver: marker count drift ",m);
    fi;
  od;
  return raw;
end;;

D972A5LGDNormalizeFC8 := function()
  local freshRaw,freshObj,observed,needle,replacement,expectedRaw,normalizedRaw,
    freshOther,normalizedObj,normalizedOther,logRaw;
  freshRaw:=StringFile(D972A5LGDFC8Artifact);;
  if freshRaw=fail or D972A5LGDCount(freshRaw,"\"runtime_ms\":")<>1 then
    Error("157dp driver: FC8 fresh runtime_ms occurrence drift");
  fi;
  freshObj:=JsonStringToGap(freshRaw);;
  if freshObj=fail or not IsBound(freshObj.performance.runtime_ms) or
     not IsInt(freshObj.performance.runtime_ms) or freshObj.performance.runtime_ms<0 then
    Error("157dp driver: FC8 fresh runtime_ms type drift");
  fi;
  if freshRaw<>Concatenation(D972A5LGDJson(freshObj),"\n") then
    Error("157dp driver: FC8 fresh receipt is not canonical JSON");
  fi;
  observed:=freshObj.performance.runtime_ms;;
  needle:=Concatenation("\"runtime_ms\":",String(observed));;
  replacement:="\"runtime_ms\":598";;
  if D972A5LGDCount(freshRaw,needle)<>1 then
    Error("157dp driver: FC8 runtime value is not uniquely located");
  fi;
  expectedRaw:=ReplacedString(freshRaw,needle,replacement);;
  freshOther:=StructuralCopy(freshObj);; Unbind(freshOther.performance.runtime_ms);;
  freshObj.performance.runtime_ms:=598;;
  D972A5LGDCheckedWrite(D972A5LGDFC8Artifact,freshObj);;
  normalizedRaw:=StringFile(D972A5LGDFC8Artifact);;
  if normalizedRaw<>expectedRaw or HexSHA256(normalizedRaw)<>D972A5LGDFC8ArtifactSHA then
    Error("157dp driver: FC8 runtime-only normalization did not reach frozen SHA");
  fi;
  normalizedObj:=JsonStringToGap(normalizedRaw);;
  normalizedOther:=StructuralCopy(normalizedObj);; Unbind(normalizedOther.performance.runtime_ms);;
  if D972A5LGDJson(freshOther)<>D972A5LGDJson(normalizedOther) or
     normalizedObj.performance.runtime_ms<>598 then
    Error("157dp driver: FC8 normalization changed a mathematical field");
  fi;
  Exec("rm -f 'ci/out/d972_b34_a5_fc8_normalized_checker.log' 'ci/out/d972_b34_a5_fc8_normalized_checker.ok' && python3 -B search/check_d972_b4_fc8_a5four_v1.py ci/out/d972_b4_fc8_a5four_v1.json > 'ci/out/d972_b34_a5_fc8_normalized_checker.log' 2>&1 && printf '%s' 'D972_B34_A5_FC8_NORMALIZED_CHECKER_EXIT_ZERO' > 'ci/out/d972_b34_a5_fc8_normalized_checker.ok'");;
  logRaw:=D972A5LGDRequireLog("ci/out/d972_b34_a5_fc8_normalized_checker.log",
    "ci/out/d972_b34_a5_fc8_normalized_checker.ok",
    "D972_B34_A5_FC8_NORMALIZED_CHECKER_EXIT_ZERO",["FC8_A5_FOUR_CHECKER_PASS"]);;
  return rec(observed_runtime_ms:=observed,normalized_sha256:=HexSHA256(normalizedRaw),
    normalized_checker_log_sha256:=HexSHA256(logRaw));
end;;

D972A5LGDRequireSHA(D972A5LGDProducerPath,D972A5LGDProducerSHA,"producer");;
D972A5LGDRequireSHA(D972A5LGDCheckerPath,D972A5LGDCheckerSHA,"checker");;
D972A5LGDRequireSHA(D972A5LGDQ3DriverPath,D972A5LGDQ3DriverSHA,"q3 driver");;
D972A5LGDRequireSHA(D972A5LGDFC8DriverPath,D972A5LGDFC8DriverSHA,"FC8 driver");;

D972A5LGDSelf:=IsBound(D972_B34_A5_SELECTED_LIFT_SELFTEST) and
  D972_B34_A5_SELECTED_LIFT_SELFTEST=true;;
D972A5LGDFull:=IsBound(D972_B34_A5_SELECTED_LIFT_RUN) and
  D972_B34_A5_SELECTED_LIFT_RUN=true;;
if D972A5LGDSelf=D972A5LGDFull then
  Error("157dp driver: select exactly one SELFTEST/RUN mode");
fi;

Exec("mkdir -p 'ci/out'");;
if D972A5LGDSelf then
  Read(D972A5LGDProducerPath);;
  if not IsBound(D972A5LCheckedIoMarkerCount) or D972A5LCheckedIoMarkerCount<>1 or
     D972A5LCheckedIoMarker<>"D972_B34_A5_SELECTED_LIFT_CHECKED_IO_SELFTEST_PASS" then
    Error("157dp driver: producer selftest marker drift");
  fi;
  Exec("rm -f 'ci/out/d972_b34_a5_selected_lift_checker_selftest.log' 'ci/out/d972_b34_a5_selected_lift_checker_selftest.ok' && python3 -B search/check_d972_b34_a5_selected_lift_v1.py --self-test > 'ci/out/d972_b34_a5_selected_lift_checker_selftest.log' 2>&1 && printf '%s' 'D972_B34_A5_SELECTED_LIFT_CHECKER_SELFTEST_EXIT_ZERO' > 'ci/out/d972_b34_a5_selected_lift_checker_selftest.ok'");;
  D972A5LGDSelfRaw:=D972A5LGDRequireLog(D972A5LGDSelfLog,D972A5LGDSelfOK,
    "D972_B34_A5_SELECTED_LIFT_CHECKER_SELFTEST_EXIT_ZERO",
    ["D972_B34_A5_SELECTED_LIFT_CHECKER_SELFTEST_PASS"]);;
  Print(D972A5LGDSelfRaw,"\nB34_A5_SELECTED_LIFT_GHA_DRIVER_PASS mode=selftest\n");
else
  if not IsBound(D972_B34_A5_SELECTED_LIFT_OUTPUT) or
     D972_B34_A5_SELECTED_LIFT_OUTPUT<>D972A5LGDArtifact then
    Error("157dp driver: full output must be fixed ci/out artifact");
  fi;
  Exec("rm -f 'ci/out/d972_b34_a5_selected_lift_v1.json' 'ci/out/d972_b34_a5_selected_lift_checker_full.log' 'ci/out/d972_b34_a5_selected_lift_checker_full.ok' 'ci/out/d972_b345_q3_chief_v1.json' 'ci/out/d972_b345_q3_checker_full.log' 'ci/out/d972_b345_q3_checker_full.ok' 'ci/out/d972_b34_a5_upstream_q3.log' 'ci/out/d972_b34_a5_upstream_q3.ok' && gap -q --quitonbreak -c 'D972_B345_Q3_RUN:=true;; D972_B345_Q3_OUTPUT:=\"ci/out/d972_b345_q3_chief_v1.json\";; Read(\"search/d972_b345_q3_gha_driver_v1.g\");;' > 'ci/out/d972_b34_a5_upstream_q3.log' 2>&1 && printf '%s' 'D972_B34_A5_UPSTREAM_Q3_EXIT_ZERO' > 'ci/out/d972_b34_a5_upstream_q3.ok'");;
  D972A5LGDQ3Log:=D972A5LGDRequireLog("ci/out/d972_b34_a5_upstream_q3.log",
    "ci/out/d972_b34_a5_upstream_q3.ok","D972_B34_A5_UPSTREAM_Q3_EXIT_ZERO",
    ["B345_Q3_CHECKER_PASS","B345_Q3_GHA_DRIVER_PASS mode=full"]);;
  D972A5LGDRequireSHA(D972A5LGDQ3Artifact,D972A5LGDQ3ArtifactSHA,"q3 artifact");;

  Exec("rm -f 'ci/out/d972_b4_fc8_a5four_v1.json' 'ci/out/d972_b4_fc8_a5four_checker_full.log' 'ci/out/d972_b4_fc8_a5four_checker_full.ok' 'ci/out/d972_b34_a5_upstream_fc8.log' 'ci/out/d972_b34_a5_upstream_fc8.ok' && gap -q --quitonbreak -c 'D972_B4_FC8_RUN:=true;; D972_B4_FC8_OUTPUT:=\"ci/out/d972_b4_fc8_a5four_v1.json\";; Read(\"search/d972_b4_fc8_a5four_gha_driver_v1.g\");;' > 'ci/out/d972_b34_a5_upstream_fc8.log' 2>&1 && printf '%s' 'D972_B34_A5_UPSTREAM_FC8_EXIT_ZERO' > 'ci/out/d972_b34_a5_upstream_fc8.ok'");;
  D972A5LGDFC8Log:=D972A5LGDRequireLog("ci/out/d972_b34_a5_upstream_fc8.log",
    "ci/out/d972_b34_a5_upstream_fc8.ok","D972_B34_A5_UPSTREAM_FC8_EXIT_ZERO",
    ["FC8_A5_FOUR_CHECKER_PASS","FC8_A5_FOUR_GHA_DRIVER_PASS mode=full"]);;
  D972A5LGDFC8Normalization:=D972A5LGDNormalizeFC8();;

  D972_B34_A5_SELECTED_LIFT_FC8_OBSERVED_RUNTIME_MS:=
    D972A5LGDFC8Normalization.observed_runtime_ms;;
  D972_B34_A5_SELECTED_LIFT_FC8_NORMALIZATION_CHECKED:=true;;
  Read(D972A5LGDProducerPath);;
  D972A5LGDArtifactRaw:=StringFile(D972A5LGDArtifact);;
  if D972A5LGDArtifactRaw=fail or Length(D972A5LGDArtifactRaw)=0 then
    Error("157dp driver: producer artifact missing");
  fi;
  D972A5LGDArtifactObj:=JsonStringToGap(D972A5LGDArtifactRaw);;
  if D972A5LGDArtifactObj=fail or not IsBound(D972A5LGDArtifactObj.terminal_token) or
     not D972A5LGDArtifactObj.terminal_token in
       [D972A5LGDPositive,D972A5LGDNegative,D972A5LGDUnknown] then
    Error("157dp driver: artifact terminal drift");
  fi;
  Exec("rm -f 'ci/out/d972_b34_a5_selected_lift_checker_full.log' 'ci/out/d972_b34_a5_selected_lift_checker_full.ok' && python3 -B search/check_d972_b34_a5_selected_lift_v1.py ci/out/d972_b34_a5_selected_lift_v1.json > 'ci/out/d972_b34_a5_selected_lift_checker_full.log' 2>&1 && printf '%s' 'D972_B34_A5_SELECTED_LIFT_CHECKER_FULL_EXIT_ZERO' > 'ci/out/d972_b34_a5_selected_lift_checker_full.ok'");;
  D972A5LGDFullRaw:=D972A5LGDRequireLog(D972A5LGDFullLog,D972A5LGDFullOK,
    "D972_B34_A5_SELECTED_LIFT_CHECKER_FULL_EXIT_ZERO",
    ["B34_A5_SELECTED_LIFT_CHECKER_PASS",D972A5LGDArtifactObj.terminal_token]);;
  Print(D972A5LGDFullRaw,"\nB34_A5_SELECTED_LIFT_GHA_DRIVER_PASS terminal=",
    D972A5LGDArtifactObj.terminal_token," artifact_sha256=",
    HexSHA256(D972A5LGDArtifactRaw)," q3_bootstrap_sha256=",HexSHA256(D972A5LGDQ3Log),
    " fc8_bootstrap_sha256=",HexSHA256(D972A5LGDFC8Log),
    " fc8_fresh_runtime_ms=",D972A5LGDFC8Normalization.observed_runtime_ms,"\n");
fi;
