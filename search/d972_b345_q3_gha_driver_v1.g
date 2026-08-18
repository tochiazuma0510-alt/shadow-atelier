#############################################################################
## d972_b345_q3_gha_driver_v1.g
##
## Thin same-job driver for the frozen 157da GAP producer and independent
## Python checker.  All shell commands and paths are source literals.  The
## generic gap-run preamble selects exactly one existing producer mode.
#############################################################################

D972Q3GDProducerPath := "search/d972_b345_q3_chief_v1.g";;
D972Q3GDProducerSHA :=
  "e3dad87ad066fc9c605e1eecaddbe63efd63ac68500e0fcff0d6d62eb7d83af3";;
D972Q3GDCheckerPath := "search/check_d972_b345_q3_chief_v1.py";;
D972Q3GDCheckerSHA :=
  "9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb";;
D972Q3GDArtifactPath := "ci/out/d972_b345_q3_chief_v1.json";;
D972Q3GDSelfLogPath := "ci/out/d972_b345_q3_checker_selftest.log";;
D972Q3GDSelfSentinelPath := "ci/out/d972_b345_q3_checker_selftest.ok";;
D972Q3GDFullLogPath := "ci/out/d972_b345_q3_checker_full.log";;
D972Q3GDFullSentinelPath := "ci/out/d972_b345_q3_checker_full.ok";;
D972Q3GDSelfSentinel := "D972_B345_Q3_CHECKER_SELFTEST_EXIT_ZERO";;
D972Q3GDFullSentinel := "D972_B345_Q3_CHECKER_FULL_EXIT_ZERO";;
D972Q3GDSelfMarker := "D972_B345_Q3_CHECKER_SELFTEST_PASS";;
D972Q3GDFullMarker := "B345_Q3_CHECKER_PASS";;

D972Q3GDRequireSHA := function(path,expected)
  local raw,got;
  raw:=StringFile(path);;
  if raw=fail then
    Error("157db driver: frozen input missing: ",path);
  fi;
  got:=HexSHA256(raw);;
  if got<>expected then
    Error("157db driver: frozen input SHA drift: ",path," got=",got);
  fi;
  return true;
end;;

D972Q3GDCountOccurrences := function(text,needle)
  local count,i,n,m;
  if not IsString(text) or not IsString(needle) or Length(needle)=0 then
    Error("157db driver: occurrence counter input drift");
  fi;
  n:=Length(text);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if text{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972Q3GDEchoLog := function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail then
    Print("157db driver: checker log missing: ",path,"\n");
    return fail;
  fi;
  Print(raw,"\n");
  return raw;
end;;

D972Q3GDRequireSHA(D972Q3GDProducerPath,D972Q3GDProducerSHA);;
D972Q3GDRequireSHA(D972Q3GDCheckerPath,D972Q3GDCheckerSHA);;

D972Q3GDSelfSelected:=false;;
if IsBound(D972_B345_Q3_SELFTEST) and D972_B345_Q3_SELFTEST=true then
  D972Q3GDSelfSelected:=true;;
fi;
D972Q3GDFullSelected:=false;;
if IsBound(D972_B345_Q3_RUN) and D972_B345_Q3_RUN=true then
  D972Q3GDFullSelected:=true;;
fi;
if D972Q3GDSelfSelected and D972Q3GDFullSelected then
  Error("157db driver: SELFTEST and RUN cannot both be true");
fi;
if not D972Q3GDSelfSelected and not D972Q3GDFullSelected then
  Error("157db driver: select exactly one literal-true mode");
fi;

if D972Q3GDSelfSelected then
  Exec("mkdir -p 'ci/out'");;
  Read(D972Q3GDProducerPath);;
  if not IsBound(D972Q3AtomicIoSelftestMarker) or
     D972Q3AtomicIoSelftestMarker<>"D972_B345_Q3_ATOMIC_IO_SELFTEST_PASS backend=IO_rename replace=true" or
     not IsBound(D972Q3AtomicIoSelftestMarkerCount) or
     D972Q3AtomicIoSelftestMarkerCount<>1 then
    Error("157df: atomic IO selftest marker count drift");
  fi;
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_q3_checker_selftest.log' 'ci/out/d972_b345_q3_checker_selftest.ok' && python3 -B search/check_d972_b345_q3_chief_v1.py --self-test > 'ci/out/d972_b345_q3_checker_selftest.log' 2>&1 && printf '%s' 'D972_B345_Q3_CHECKER_SELFTEST_EXIT_ZERO' > 'ci/out/d972_b345_q3_checker_selftest.ok'");;
  D972Q3GDSelfLog:=D972Q3GDEchoLog(D972Q3GDSelfLogPath);;
  D972Q3GDSelfSentinelRaw:=StringFile(D972Q3GDSelfSentinelPath);;
  if D972Q3GDSelfSentinelRaw<>D972Q3GDSelfSentinel then
    Error("157db driver: Python self-test did not exit zero");
  fi;
  if D972Q3GDSelfLog=fail or
     D972Q3GDCountOccurrences(D972Q3GDSelfLog,D972Q3GDSelfMarker)<>1 then
    Error("157db driver: Python self-test marker count is not one");
  fi;
  Print("B345_Q3_GHA_DRIVER_PASS mode=selftest\n");
else
  if not IsBound(D972_B345_Q3_OUTPUT) or
     D972_B345_Q3_OUTPUT<>D972Q3GDArtifactPath then
    Error("157db driver: full output path must be the fixed ci/out artifact");
  fi;
  Read(D972Q3GDProducerPath);;
  D972Q3GDFullArtifactRaw:=StringFile(D972Q3GDArtifactPath);;
  if D972Q3GDFullArtifactRaw=fail or Length(D972Q3GDFullArtifactRaw)=0 then
    Error("157db driver: full producer artifact missing or empty");
  fi;
  D972Q3GDFullArtifactSHA:=HexSHA256(D972Q3GDFullArtifactRaw);;
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_b345_q3_checker_full.log' 'ci/out/d972_b345_q3_checker_full.ok' && python3 -B search/check_d972_b345_q3_chief_v1.py ci/out/d972_b345_q3_chief_v1.json > 'ci/out/d972_b345_q3_checker_full.log' 2>&1 && printf '%s' 'D972_B345_Q3_CHECKER_FULL_EXIT_ZERO' > 'ci/out/d972_b345_q3_checker_full.ok'");;
  D972Q3GDFullLog:=D972Q3GDEchoLog(D972Q3GDFullLogPath);;
  D972Q3GDFullSentinelRaw:=StringFile(D972Q3GDFullSentinelPath);;
  if D972Q3GDFullSentinelRaw<>D972Q3GDFullSentinel then
    Error("157db driver: Python full checker did not exit zero");
  fi;
  if D972Q3GDFullLog=fail or
     D972Q3GDCountOccurrences(D972Q3GDFullLog,D972Q3GDFullMarker)<>1 then
    Error("157db driver: Python full checker marker count is not one");
  fi;
  Print("B345_Q3_GHA_DRIVER_PASS mode=full artifact_sha256=",
    D972Q3GDFullArtifactSHA,"\n");
fi;
