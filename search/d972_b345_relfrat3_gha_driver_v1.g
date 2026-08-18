#############################################################################
## d972_b345_relfrat3_gha_driver_v1.g
##
## Thin same-job bootstrap.  A full run first regenerates and independently
## checks the frozen 157da q=3 artifact, binds its exact successful SHA, then
## runs the relative-Frattini producer and independent checker.
#############################################################################

D972RFQ3DriverPath := "search/d972_b345_q3_gha_driver_v1.g";;
D972RFQ3DriverSHA :=
  "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831";;
D972RFProducerPath := "search/d972_b345_relfrat3_v1.py";;
D972RFProducerSHA :=
  "4b73fbfe19bb33a9decdec5fda437f58f61a3ecb1989090bd08151f60ce6609e";;
D972RFCheckerPath := "search/check_d972_b345_relfrat3_v1.py";;
D972RFCheckerSHA :=
  "3d86240237229b250943c4795c24c32ac75af9229534c73d16bd838f6d6d0101";;
D972RFQ3Artifact := "ci/out/d972_b345_q3_chief_v1.json";;
D972RFQ3ArtifactSHA :=
  "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;
D972RFArtifact := "ci/out/d972_b345_relfrat3_v1.json";;
D972RFProducerLog := "ci/out/d972_b345_relfrat3_producer.log";;
D972RFProducerOk := "ci/out/d972_b345_relfrat3_producer.ok";;
D972RFCheckerLog := "ci/out/d972_b345_relfrat3_checker.log";;
D972RFCheckerOk := "ci/out/d972_b345_relfrat3_checker.ok";;
D972RFSelfLog := "ci/out/d972_b345_relfrat3_selftest.log";;
D972RFSelfOk := "ci/out/d972_b345_relfrat3_selftest.ok";;
D972RFProducerSentinel := "D972_B345_RELFRAT3_PRODUCER_EXIT_ZERO";;
D972RFCheckerSentinel := "D972_B345_RELFRAT3_CHECKER_EXIT_ZERO";;
D972RFSelfSentinel := "D972_B345_RELFRAT3_SELFTEST_EXIT_ZERO";;

D972RFRequireSHA := function(path,expected)
  local raw,got;
  raw:=StringFile(path);;
  if raw=fail then Error("157dl driver: missing source ",path); fi;
  got:=HexSHA256(raw);;
  if got<>expected then
    Error("157dl driver: source SHA drift ",path," got=",got);
  fi;
  return true;
end;;

D972RFCount := function(text,needle)
  local i,n,m,count;
  if not IsString(text) or not IsString(needle) or Length(needle)=0 then
    Error("157dl driver: occurrence input");
  fi;
  n:=Length(text);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if text{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972RFReadRequired := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("157dl driver: missing ",label); fi;
  return raw;
end;;

D972RFRequireSHA(D972RFQ3DriverPath,D972RFQ3DriverSHA);;
D972RFRequireSHA(D972RFProducerPath,D972RFProducerSHA);;
D972RFRequireSHA(D972RFCheckerPath,D972RFCheckerSHA);;

D972RFSelf:=IsBound(D972_B345_RELFRAT3_SELFTEST) and
  D972_B345_RELFRAT3_SELFTEST=true;;
D972RFFull:=IsBound(D972_B345_RELFRAT3_RUN) and
  D972_B345_RELFRAT3_RUN=true;;
if D972RFSelf=D972RFFull then
  Error("157dl driver: select exactly one of SELFTEST and RUN");
fi;

if D972RFSelf then
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_relfrat3_selftest.log' 'ci/out/d972_b345_relfrat3_selftest.ok' && python3 -B search/d972_b345_relfrat3_v1.py --self-test > 'ci/out/d972_b345_relfrat3_selftest.log' 2>&1 && python3 -B search/check_d972_b345_relfrat3_v1.py --self-test >> 'ci/out/d972_b345_relfrat3_selftest.log' 2>&1 && printf '%s' 'D972_B345_RELFRAT3_SELFTEST_EXIT_ZERO' > 'ci/out/d972_b345_relfrat3_selftest.ok'");;
  D972RFSelfRaw:=D972RFReadRequired(D972RFSelfLog,"selftest log");;
  if StringFile(D972RFSelfOk)<>D972RFSelfSentinel then
    Error("157dl driver: selftests did not exit zero");
  fi;
  if D972RFCount(D972RFSelfRaw,
       "D972_B345_RELFRAT3_PRODUCER_SELFTEST_PASS")<>1 or
     D972RFCount(D972RFSelfRaw,
       "D972_B345_RELFRAT3_CHECKER_SELFTEST_PASS")<>1 then
    Error("157dl driver: selftest marker count");
  fi;
  Print(D972RFSelfRaw,"\n");;
  Print("B345_RELFRAT3_GHA_DRIVER_PASS mode=selftest\n");;
else
  if not IsBound(D972_B345_RELFRAT3_OUTPUT) or
     D972_B345_RELFRAT3_OUTPUT<>D972RFArtifact then
    Error("157dl driver: full output must be fixed ci/out artifact");
  fi;
  # The q3 driver clears its checker files; this outer driver also removes the
  # artifact and every downstream sentinel before the same-job bootstrap.
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_q3_chief_v1.json' 'ci/out/d972_b345_q3_checker_full.log' 'ci/out/d972_b345_q3_checker_full.ok' 'ci/out/d972_b345_relfrat3_v1.json' 'ci/out/d972_b345_relfrat3_producer.log' 'ci/out/d972_b345_relfrat3_producer.ok' 'ci/out/d972_b345_relfrat3_checker.log' 'ci/out/d972_b345_relfrat3_checker.ok'");;
  D972_B345_Q3_RUN:=true;;
  D972_B345_Q3_OUTPUT:=D972RFQ3Artifact;;
  Read(D972RFQ3DriverPath);;
  D972RFQ3Raw:=D972RFReadRequired(D972RFQ3Artifact,"q3 artifact");;
  if HexSHA256(D972RFQ3Raw)<>D972RFQ3ArtifactSHA then
    Error("157dl driver: regenerated q3 artifact SHA drift");
  fi;
  D972RFQ3CheckerRaw:=D972RFReadRequired(
    "ci/out/d972_b345_q3_checker_full.log","q3 checker log");;
  if StringFile("ci/out/d972_b345_q3_checker_full.ok")<>
       "D972_B345_Q3_CHECKER_FULL_EXIT_ZERO" or
     D972RFCount(D972RFQ3CheckerRaw,"B345_Q3_CHECKER_PASS")<>1 then
    Error("157dl driver: q3 checker gate");
  fi;
  Exec("python3 -B search/d972_b345_relfrat3_v1.py ci/out/d972_b345_q3_chief_v1.json ci/out/d972_b345_relfrat3_v1.json > 'ci/out/d972_b345_relfrat3_producer.log' 2>&1 && printf '%s' 'D972_B345_RELFRAT3_PRODUCER_EXIT_ZERO' > 'ci/out/d972_b345_relfrat3_producer.ok'");;
  D972RFProducerRaw:=D972RFReadRequired(D972RFProducerLog,"producer log");;
  if StringFile(D972RFProducerOk)<>D972RFProducerSentinel then
    Error("157dl driver: producer did not exit zero");
  fi;
  D972RFTerminalCount:=0;;
  for D972RFToken in [
      "B345_RELFRAT3_LITERAL_PAIR_PASS",
      "B345_RELFRAT3_SEARCH_INCOMPLETE",
      "B345_RELFRAT3_UNKNOWN_RESOURCE"] do
    D972RFTerminalCount:=D972RFTerminalCount+
      D972RFCount(D972RFProducerRaw,D972RFToken);;
  od;
  if D972RFTerminalCount<>1 then
    Error("157dl driver: producer terminal marker count");
  fi;
  D972RFArtifactRaw:=D972RFReadRequired(D972RFArtifact,"relative artifact");;
  Exec("python3 -B search/check_d972_b345_relfrat3_v1.py ci/out/d972_b345_q3_chief_v1.json ci/out/d972_b345_relfrat3_v1.json > 'ci/out/d972_b345_relfrat3_checker.log' 2>&1 && printf '%s' 'D972_B345_RELFRAT3_CHECKER_EXIT_ZERO' > 'ci/out/d972_b345_relfrat3_checker.ok'");;
  D972RFCheckerRaw:=D972RFReadRequired(D972RFCheckerLog,"checker log");;
  if StringFile(D972RFCheckerOk)<>D972RFCheckerSentinel or
     D972RFCount(D972RFCheckerRaw,"B345_RELFRAT3_CHECKER_PASS")<>1 then
    Error("157dl driver: checker gate");
  fi;
  Print(D972RFProducerRaw,"\n",D972RFCheckerRaw,"\n");;
  Print("B345_RELFRAT3_GHA_DRIVER_PASS mode=full artifact_sha256=",
    HexSHA256(D972RFArtifactRaw),"\n");;
fi;
