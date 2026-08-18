#############################################################################
## Thin same-job driver for the total-linking C3 chief descent.
#############################################################################

Read("search/gaplib_common.g");;
if LoadPackage("json")<>true then Error("157dq driver: JSON unavailable"); fi;;

D972TLGDProducer := "search/d972_b34_total_linking_c3_chief_v1.g";;
D972TLGDProducerSHA := "dba9adc5a8d06665c89e97697bc737a28ec68096ccd02a58db03ccfe63d1d837";;
D972TLGDChecker := "search/check_d972_b34_total_linking_c3_chief_v1.py";;
D972TLGDCheckerSHA := "58c2a67b13f11da04f616e12875cce4fc6e4152cd75231577c4fe111b6a8ff22";;
D972TLGDOldDriver := "search/d972_b34_a5_selected_lift_gha_driver_v1.g";;
D972TLGDOldDriverSHA := "cce2dff8e4a96046d97f70f64a31f279ced5feeeb08dca55de82b59f7154171e";;
D972TLGDOldChecker := "search/check_d972_b34_a5_selected_lift_v1.py";;
D972TLGDOldCheckerSHA := "2d30b1458725cb70d94cb4ab35256988bf23cc2d796a422d3f0b14d1c2f6805e";;
D972TLGDQ3 := "ci/out/d972_b345_q3_chief_v1.json";;
D972TLGDQ3SHA := "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;
D972TLGDFC8 := "ci/out/d972_b4_fc8_a5four_v1.json";;
D972TLGDFC8SHA := "558faee7864ab1162aaa40a9d2e2ad7bd1926987561cde9e3d3a9ee69690c584";;
D972TLGDDP := "ci/out/d972_b34_a5_selected_lift_v1.json";;
D972TLGDDPSHA := "d3cb729d972a1b460cd8f0a76b49cd6abf4eafd7fe0c112ad0ad742de5200157";;
D972TLGDArtifact := "ci/out/d972_b34_total_linking_c3_chief_v1.json";;
D972TLGDSelfLog := "ci/out/d972_b34_total_linking_c3_checker_selftest.log";;
D972TLGDSelfOK := "ci/out/d972_b34_total_linking_c3_checker_selftest.ok";;
D972TLGDFullLog := "ci/out/d972_b34_total_linking_c3_checker_full.log";;
D972TLGDFullOK := "ci/out/d972_b34_total_linking_c3_checker_full.ok";;

D972TLGDRequireSHA := function(path,expected,label)
  local raw,got;
  raw:=StringFile(path);;
  if raw=fail then Error("157dq driver: missing ",label," ",path); fi;
  got:=HexSHA256(raw);;
  if got<>expected then Error("157dq driver: SHA drift ",label," got=",got); fi;
  return raw;
end;;

D972TLGDCount := function(raw,needle)
  local i,n,m,count;
  if raw=fail or Length(needle)=0 then return 0; fi;
  n:=Length(raw);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do if raw{[i..i+m-1]}=needle then count:=count+1;; fi; od;
  return count;
end;;

D972TLGDEscape := function(s)
  local z;
  z:=ReplacedString(s,"\\","\\\\");; z:=ReplacedString(z,"\"","\\\"");;
  z:=ReplacedString(z,"\n","\\n");; z:=ReplacedString(z,"\r","\\r");;
  z:=ReplacedString(z,"\t","\\t");; return z;
end;;

D972TLGDJson := function(x)
  local names,parts,n;
  if x=fail then return "null"; fi; if x=true then return "true"; fi;
  if x=false then return "false"; fi; if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",D972TLGDEscape(x),"\""); fi;
  if IsRecord(x) then
    names:=ShallowCopy(RecNames(x));; Sort(names);; parts:=[];;
    for n in names do Add(parts,Concatenation(D972TLGDJson(n),":",D972TLGDJson(x.(n)))); od;
    return Concatenation("{",JoinStringsWithSeparator(parts,","),"}");
  fi;
  if IsList(x) then return Concatenation("[",JoinStringsWithSeparator(
    List(x,D972TLGDJson),","),"]"); fi;
  Error("157dq driver: unsupported JSON value");
end;;

D972TLGDWrite := function(path,obj)
  local expected,f,actual;
  expected:=Concatenation(D972TLGDJson(obj),"\n");;
  f:=OutputTextFile(path,false);; if f=fail then Error("157dq driver: output open"); fi;
  SetPrintFormattingStatus(f,false);; PrintTo(f,expected);; CloseStream(f);;
  actual:=StringFile(path);;
  if actual=fail or actual<>expected then Error("157dq driver: checked write drift"); fi;
end;;

D972TLGDRequireLog := function(logPath,okPath,sentinel,markers)
  local raw,m;
  raw:=StringFile(logPath);;
  if StringFile(okPath)<>sentinel or raw=fail then
    if raw<>fail then Print(raw,"\n"); fi; Error("157dq driver: subprocess failed ",logPath);
  fi;
  for m in markers do
    if D972TLGDCount(raw,m)<>1 then Print(raw,"\n");;
      Error("157dq driver: marker count drift ",m); fi;
  od;
  return raw;
end;;

D972TLGDNormalizeDP := function()
  local raw,obj,observedDP,observedFC,other,normalized,normalizedOther,log;
  raw:=StringFile(D972TLGDDP);;
  if raw=fail or D972TLGDCount(raw,"\"runtime_ms\":")<>1 or
     D972TLGDCount(raw,"\"observed_fresh_value\":")<>1 then
    Error("157dq driver: 157dp registered runtime fields drift");
  fi;
  obj:=JsonStringToGap(raw);;
  if obj=fail or not IsInt(obj.runtime_ms) or
     not IsInt(obj.pins.fc8_runtime_normalization.observed_fresh_value) then
    Error("157dq driver: 157dp runtime types drift");
  fi;
  if raw<>Concatenation(D972TLGDJson(obj),"\n") then
    Error("157dq driver: fresh 157dp is not canonical JSON");
  fi;
  observedDP:=obj.runtime_ms;;
  observedFC:=obj.pins.fc8_runtime_normalization.observed_fresh_value;;
  other:=StructuralCopy(obj);; Unbind(other.runtime_ms);;
  Unbind(other.pins.fc8_runtime_normalization.observed_fresh_value);;
  obj.runtime_ms:=366;; obj.pins.fc8_runtime_normalization.observed_fresh_value:=500;;
  D972TLGDWrite(D972TLGDDP,obj);;
  normalized:=StringFile(D972TLGDDP);;
  if HexSHA256(normalized)<>D972TLGDDPSHA then
    Error("157dq driver: registered runtime-only normalization did not reach frozen 157dp SHA");
  fi;
  obj:=JsonStringToGap(normalized);; normalizedOther:=StructuralCopy(obj);;
  Unbind(normalizedOther.runtime_ms);;
  Unbind(normalizedOther.pins.fc8_runtime_normalization.observed_fresh_value);;
  if D972TLGDJson(other)<>D972TLGDJson(normalizedOther) or obj.runtime_ms<>366 or
     obj.pins.fc8_runtime_normalization.observed_fresh_value<>500 then
    Error("157dq driver: 157dp normalization changed a mathematical field");
  fi;
  Exec("rm -f 'ci/out/d972_total_linking_dp_normalized.log' 'ci/out/d972_total_linking_dp_normalized.ok' && python3 -B search/check_d972_b34_a5_selected_lift_v1.py ci/out/d972_b34_a5_selected_lift_v1.json > 'ci/out/d972_total_linking_dp_normalized.log' 2>&1 && printf '%s' 'D972_TOTAL_LINKING_DP_NORMALIZED_EXIT_ZERO' > 'ci/out/d972_total_linking_dp_normalized.ok'");;
  log:=D972TLGDRequireLog("ci/out/d972_total_linking_dp_normalized.log",
    "ci/out/d972_total_linking_dp_normalized.ok","D972_TOTAL_LINKING_DP_NORMALIZED_EXIT_ZERO",
    ["B34_A5_SELECTED_LIFT_CHECKER_PASS",
     "B34_A5_LAYER_FIXED_OUTSIDE_ROOF_LIFT_CROSSCHECKED"]);;
  return rec(observed_157dp_runtime_ms:=observedDP,observed_fc8_fresh_runtime_ms:=observedFC,
    normalized_157dp_runtime_ms:=366,normalized_fc8_observation_ms:=500,
    normalized_artifact_sha256:=HexSHA256(normalized),checker_log_sha256:=HexSHA256(log),
    all_other_parsed_fields_equal:=true);
end;;

D972TLGDRequireSHA(D972TLGDProducer,D972TLGDProducerSHA,"producer");;
D972TLGDRequireSHA(D972TLGDChecker,D972TLGDCheckerSHA,"checker");;
D972TLGDRequireSHA(D972TLGDOldDriver,D972TLGDOldDriverSHA,"157dp driver");;
D972TLGDRequireSHA(D972TLGDOldChecker,D972TLGDOldCheckerSHA,"157dp checker");;

D972TLGDSelf:=IsBound(D972_B34_TOTAL_LINKING_C3_SELFTEST) and
  D972_B34_TOTAL_LINKING_C3_SELFTEST=true;;
D972TLGDFull:=IsBound(D972_B34_TOTAL_LINKING_C3_RUN) and
  D972_B34_TOTAL_LINKING_C3_RUN=true;;
if D972TLGDSelf=D972TLGDFull then Error("157dq driver: select SELFTEST or RUN"); fi;
Exec("mkdir -p 'ci/out'");;

if D972TLGDSelf then
  Read(D972TLGDProducer);;
  if not IsBound(D972TLIOMarkerCount) or D972TLIOMarkerCount<>1 or
     D972TLIOMarker<>"D972_B34_TOTAL_LINKING_C3_CHECKED_IO_SELFTEST_PASS" then
    Error("157dq driver: producer selftest marker drift");
  fi;
  Exec("rm -f 'ci/out/d972_b34_total_linking_c3_checker_selftest.log' 'ci/out/d972_b34_total_linking_c3_checker_selftest.ok' && python3 -B search/check_d972_b34_total_linking_c3_chief_v1.py --self-test > 'ci/out/d972_b34_total_linking_c3_checker_selftest.log' 2>&1 && printf '%s' 'D972_TOTAL_LINKING_CHECKER_SELFTEST_EXIT_ZERO' > 'ci/out/d972_b34_total_linking_c3_checker_selftest.ok'");;
  D972TLGDSelfRaw:=D972TLGDRequireLog(D972TLGDSelfLog,D972TLGDSelfOK,
    "D972_TOTAL_LINKING_CHECKER_SELFTEST_EXIT_ZERO",
    ["D972_B34_TOTAL_LINKING_C3_CHECKER_SELFTEST_PASS"]);;
  Print(D972TLGDSelfRaw,"\nB34_TOTAL_LINKING_C3_GHA_DRIVER_PASS mode=selftest\n");
else
  if not IsBound(D972_B34_TOTAL_LINKING_C3_OUTPUT) or
     D972_B34_TOTAL_LINKING_C3_OUTPUT<>D972TLGDArtifact then
    Error("157dq driver: full output path drift");
  fi;
  Exec("rm -f 'ci/out/d972_b345_q3_chief_v1.json' 'ci/out/d972_b4_fc8_a5four_v1.json' 'ci/out/d972_b34_a5_selected_lift_v1.json' 'ci/out/d972_b34_total_linking_c3_chief_v1.json' 'ci/out/d972_b34_total_linking_c3_checker_full.log' 'ci/out/d972_b34_total_linking_c3_checker_full.ok' 'ci/out/d972_total_linking_upstream.log' 'ci/out/d972_total_linking_upstream.ok' && gap -q --quitonbreak -c 'D972_B34_A5_SELECTED_LIFT_RUN:=true;; D972_B34_A5_SELECTED_LIFT_OUTPUT:=\"ci/out/d972_b34_a5_selected_lift_v1.json\";; Read(\"search/d972_b34_a5_selected_lift_gha_driver_v1.g\");;' > 'ci/out/d972_total_linking_upstream.log' 2>&1 && printf '%s' 'D972_TOTAL_LINKING_UPSTREAM_EXIT_ZERO' > 'ci/out/d972_total_linking_upstream.ok'");;
  D972TLGDUpstreamRaw:=D972TLGDRequireLog("ci/out/d972_total_linking_upstream.log",
    "ci/out/d972_total_linking_upstream.ok","D972_TOTAL_LINKING_UPSTREAM_EXIT_ZERO",
    ["B34_A5_SELECTED_LIFT_CHECKER_PASS","B34_A5_SELECTED_LIFT_GHA_DRIVER_PASS"]);;
  D972TLGDRequireLog("ci/out/d972_b345_q3_checker_full.log",
    "ci/out/d972_b345_q3_checker_full.ok","D972_B345_Q3_CHECKER_FULL_EXIT_ZERO",
    ["B345_Q3_CHECKER_PASS"]);;
  D972TLGDRequireLog("ci/out/d972_b4_fc8_a5four_checker_full.log",
    "ci/out/d972_b4_fc8_a5four_checker_full.ok","D972_B4_FC8_CHECKER_FULL_EXIT_ZERO",
    ["FC8_A5_FOUR_CHECKER_PASS"]);;
  D972TLGDRequireSHA(D972TLGDQ3,D972TLGDQ3SHA,"q3 artifact");;
  D972TLGDRequireSHA(D972TLGDFC8,D972TLGDFC8SHA,"FC8 artifact");;
  D972TLGDNormalization:=D972TLGDNormalizeDP();;
  D972TLGDRequireSHA(D972TLGDDP,D972TLGDDPSHA,"157dp normalized artifact");;
  Read(D972TLGDProducer);;
  D972TLGDArtifactRaw:=StringFile(D972TLGDArtifact);;
  if D972TLGDArtifactRaw=fail then Error("157dq driver: missing artifact"); fi;
  D972TLGDArtifactObj:=JsonStringToGap(D972TLGDArtifactRaw);;
  if D972TLGDArtifactObj=fail or not D972TLGDArtifactObj.terminal_token in
    ["B34_TOTAL_LINKING_C3_CHIEF_DESCENT_CROSSCHECKED",
     "B34_TOTAL_LINKING_C3_CANDIDATE_REJECTED_CROSSCHECKED",
     "B34_TOTAL_LINKING_C3_CHIEF_UNKNOWN_INPUT",
     "B34_TOTAL_LINKING_C3_CHIEF_UNKNOWN_RESOURCE"] then
    Error("157dq driver: terminal token drift");
  fi;
  Exec("rm -f 'ci/out/d972_b34_total_linking_c3_checker_full.log' 'ci/out/d972_b34_total_linking_c3_checker_full.ok' && python3 -B search/check_d972_b34_total_linking_c3_chief_v1.py ci/out/d972_b34_total_linking_c3_chief_v1.json > 'ci/out/d972_b34_total_linking_c3_checker_full.log' 2>&1 && printf '%s' 'D972_TOTAL_LINKING_CHECKER_FULL_EXIT_ZERO' > 'ci/out/d972_b34_total_linking_c3_checker_full.ok'");;
  D972TLGDFullRaw:=D972TLGDRequireLog(D972TLGDFullLog,D972TLGDFullOK,
    "D972_TOTAL_LINKING_CHECKER_FULL_EXIT_ZERO",
    ["B34_TOTAL_LINKING_C3_CHECKER_PASS",D972TLGDArtifactObj.terminal_token]);;
  Print(D972TLGDFullRaw,"\nB34_TOTAL_LINKING_C3_GHA_DRIVER_PASS terminal=",
    D972TLGDArtifactObj.terminal_token," artifact_sha256=",HexSHA256(D972TLGDArtifactRaw),
    " upstream_log_sha256=",HexSHA256(D972TLGDUpstreamRaw),
    " dp_fresh_runtime_ms=",D972TLGDNormalization.observed_157dp_runtime_ms,
    " fc8_fresh_runtime_ms=",D972TLGDNormalization.observed_fc8_fresh_runtime_ms,"\n");
fi;
