#############################################################################
## d972_b4_fc8_a5four_gha_driver_v1.g
## Thin fail-closed same-job driver: producer, then independent checker.
#############################################################################

D972FCGDProducerPath := "search/d972_b4_fc8_a5four_v1.g";;
D972FCGDProducerSHA := "d482315bb0abc54e9707651a8fb73e73a4a569f101f51c232b76a73fbf57e804";;
D972FCGDCheckerPath := "search/check_d972_b4_fc8_a5four_v1.py";;
D972FCGDCheckerSHA := "5b2f54b7adbddbff914fe2d28786327df9109d4e91fa53b1be03114eed5a65d4";;
D972FCGDArtifact := "ci/out/d972_b4_fc8_a5four_v1.json";;
D972FCGDSelfLog := "ci/out/d972_b4_fc8_a5four_checker_selftest.log";;
D972FCGDSelfOK := "ci/out/d972_b4_fc8_a5four_checker_selftest.ok";;
D972FCGDFullLog := "ci/out/d972_b4_fc8_a5four_checker_full.log";;
D972FCGDFullOK := "ci/out/d972_b4_fc8_a5four_checker_full.ok";;
D972FCGDSelfSentinel := "D972_B4_FC8_CHECKER_SELFTEST_EXIT_ZERO";;
D972FCGDFullSentinel := "D972_B4_FC8_CHECKER_FULL_EXIT_ZERO";;

D972FCGDRequireSHA := function(path,sha)
  local raw,got;
  raw:=StringFile(path);;
  if raw=fail then Error("157do driver: missing source ",path); fi;
  got:=HexSHA256(raw);;
  if got<>sha then Error("157do driver: source SHA drift ",path," got=",got); fi;
end;;

D972FCGDCount := function(text,needle)
  local i,count,n,m;
  if text=fail or Length(needle)=0 then return 0; fi;
  count:=0;; n:=Length(text);; m:=Length(needle);;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if text{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972FCGDRequireSHA(D972FCGDProducerPath,D972FCGDProducerSHA);;
D972FCGDRequireSHA(D972FCGDCheckerPath,D972FCGDCheckerSHA);;

D972FCGDSelf:=IsBound(D972_B4_FC8_SELFTEST) and D972_B4_FC8_SELFTEST=true;;
D972FCGDFull:=IsBound(D972_B4_FC8_RUN) and D972_B4_FC8_RUN=true;;
if D972FCGDSelf=D972FCGDFull then
  Error("157do driver: select exactly one of SELFTEST or RUN");
fi;

Exec("mkdir -p 'ci/out'");;
if D972FCGDSelf then
  Read(D972FCGDProducerPath);;
  if not IsBound(D972FCCheckedIoMarker) or
     D972FCCheckedIoMarker<>
       "D972_B4_FC8_CHECKED_IO_SELFTEST_PASS backend=OutputTextFile readback=true" or
     not IsBound(D972FCCheckedIoMarkerCount) or D972FCCheckedIoMarkerCount<>1 then
    Error("157do driver: producer checked-IO selftest marker drift");
  fi;
  Exec("rm -f 'ci/out/d972_b4_fc8_a5four_checker_selftest.log' 'ci/out/d972_b4_fc8_a5four_checker_selftest.ok' && python3 -B search/check_d972_b4_fc8_a5four_v1.py --self-test > 'ci/out/d972_b4_fc8_a5four_checker_selftest.log' 2>&1 && printf '%s' 'D972_B4_FC8_CHECKER_SELFTEST_EXIT_ZERO' > 'ci/out/d972_b4_fc8_a5four_checker_selftest.ok'");;
  D972FCGDSelfRaw:=StringFile(D972FCGDSelfLog);;
  if StringFile(D972FCGDSelfOK)<>D972FCGDSelfSentinel or
     D972FCGDCount(D972FCGDSelfRaw,"D972_B4_FC8_CHECKER_SELFTEST_PASS")<>1 then
    if D972FCGDSelfRaw<>fail then Print(D972FCGDSelfRaw,"\n"); fi;
    Error("157do driver: checker selftest failed");
  fi;
  Print(D972FCGDSelfRaw,"\nFC8_A5_FOUR_GHA_DRIVER_PASS mode=selftest\n");
else
  if not IsBound(D972_B4_FC8_OUTPUT) or D972_B4_FC8_OUTPUT<>D972FCGDArtifact then
    Error("157do driver: full output path must be fixed ci/out artifact");
  fi;
  Read(D972FCGDProducerPath);;
  D972FCGDArtifactRaw:=StringFile(D972FCGDArtifact);;
  if D972FCGDArtifactRaw=fail or Length(D972FCGDArtifactRaw)=0 then
    Error("157do driver: producer artifact missing or empty");
  fi;
  D972FCGDArtifactSHA:=HexSHA256(D972FCGDArtifactRaw);;
  Exec("rm -f 'ci/out/d972_b4_fc8_a5four_checker_full.log' 'ci/out/d972_b4_fc8_a5four_checker_full.ok' && python3 -B search/check_d972_b4_fc8_a5four_v1.py ci/out/d972_b4_fc8_a5four_v1.json > 'ci/out/d972_b4_fc8_a5four_checker_full.log' 2>&1 && printf '%s' 'D972_B4_FC8_CHECKER_FULL_EXIT_ZERO' > 'ci/out/d972_b4_fc8_a5four_checker_full.ok'");;
  D972FCGDFullRaw:=StringFile(D972FCGDFullLog);;
  if StringFile(D972FCGDFullOK)<>D972FCGDFullSentinel or
     D972FCGDCount(D972FCGDFullRaw,"FC8_A5_FOUR_CHECKER_PASS")<>1 then
    if D972FCGDFullRaw<>fail then Print(D972FCGDFullRaw,"\n"); fi;
    Error("157do driver: independent checker failed");
  fi;
  Print(D972FCGDFullRaw,"\nFC8_A5_FOUR_GHA_DRIVER_PASS mode=full artifact_sha256=",
    D972FCGDArtifactSHA,"\n");
fi;
