#############################################################################
## d972_r07_relfrat3_actual_class_gha_driver_v1.g
##
## Checker-only GHA driver for the slow independent 4096-order replay.
## The full mode launches exactly one Python process and never imports or
## executes the producer.  All source and receipt inputs are byte/SHA pinned.
#############################################################################

D972R07V1ProducerPath :=
  "search/d972_r07_relfrat3_actual_class_v1.py";;
D972R07V1ProducerBytes := 35980;;
D972R07V1ProducerSHA :=
  "e131fda73b6bbda69b6f6a4db805e4d7961c3396b496acf7da83a1ecb8bfead2";;
D972R07V1CheckerPath :=
  "search/check_d972_r07_relfrat3_actual_class_v1.py";;
D972R07V1CheckerBytes := 30775;;
D972R07V1CheckerSHA :=
  "536535791af70f411b91eb3876dfd69b2ce9a7086b35ce660d88a63120b59b40";;
D972R07V1ReceiptPath :=
  "search/certs/d972_r07_relfrat3_actual_class_preflight_v1_20260826.json";;
D972R07V1ReceiptBytes := 473404;;
D972R07V1ReceiptSHA :=
  "2d23aababa215955699f3774205bbe8356b52a3067f4f8d052f84048a5bc7f3d";;

D972R07V1FullLog :=
  "ci/out/d972_r07_relfrat3_actual_class_v1_checker_full.log";;
D972R07V1FullOK :=
  "ci/out/d972_r07_relfrat3_actual_class_v1_checker_full.ok";;
D972R07V1SelfLog :=
  "ci/out/d972_r07_relfrat3_actual_class_v1_checker_selftest.log";;
D972R07V1SelfOK :=
  "ci/out/d972_r07_relfrat3_actual_class_v1_checker_selftest.ok";;
D972R07V1FullSentinel :=
  "D972_R07_RELFRAT3_ACTUAL_CLASS_V1_CHECKER_FULL_EXIT_ZERO";;
D972R07V1SelfSentinel :=
  "D972_R07_RELFRAT3_ACTUAL_CLASS_V1_CHECKER_SELFTEST_EXIT_ZERO";;
D972R07V1FullMarker := Concatenation(
  "R07_RELFRAT3_ACTUAL_CLASS_V1_CHECKER_PASS ",
  "terminal=R07_RELFRAT3_TYPE_MISMATCH_STOP mutations=7 ",
  "dictionary_replayed=true receipt_sha256=",
  D972R07V1ReceiptSHA);;
D972R07V1SelfMarker := Concatenation(
  "R07_RELFRAT3_ACTUAL_CLASS_V1_CHECKER_SELFTEST_PASS ",
  "stdlib_adapter=1 mutations=7 negative=0");;

D972R07V1Count := function(text,needle)
  local i,n,m,count;
  if not IsString(text) or not IsString(needle) or Length(needle)=0 then
    Error("R07 v1 GHA driver: occurrence input");
  fi;
  n:=Length(text);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if text{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972R07V1ReadPinned := function(path,bytes,sha,label)
  local raw,got;
  raw:=StringFile(path);;
  if raw=fail then Error("R07 v1 GHA driver: missing ",label); fi;
  if Length(raw)<>bytes then
    Error("R07 v1 GHA driver: byte drift ",label," got=",Length(raw));
  fi;
  got:=HexSHA256(raw);;
  if got<>sha then
    Error("R07 v1 GHA driver: SHA drift ",label," got=",got);
  fi;
  return raw;
end;;

D972R07V1ReadRequired := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then
    Error("R07 v1 GHA driver: missing or empty ",label);
  fi;
  return raw;
end;;

D972R07V1RequireCleanLog := function(raw,label)
  local token;
  for token in ["Traceback", "SyntaxError", "Error", "FAIL",
                "producer import", "PRODUCER_PASS"] do
    if D972R07V1Count(raw,token)<>0 then
      Error("R07 v1 GHA driver: forbidden diagnostic in ",label,
            " token=",token);
    fi;
  od;
  return true;
end;;

D972R07V1ProducerRaw:=D972R07V1ReadPinned(
  D972R07V1ProducerPath,D972R07V1ProducerBytes,D972R07V1ProducerSHA,
  "producer");;
D972R07V1CheckerRaw:=D972R07V1ReadPinned(
  D972R07V1CheckerPath,D972R07V1CheckerBytes,D972R07V1CheckerSHA,
  "checker");;
D972R07V1ReceiptRaw:=D972R07V1ReadPinned(
  D972R07V1ReceiptPath,D972R07V1ReceiptBytes,D972R07V1ReceiptSHA,
  "receipt");;

if D972R07V1Count(D972R07V1CheckerRaw,
     "d972_r07_relfrat3_actual_class_v1.py")<>0 or
   D972R07V1Count(D972R07V1CheckerRaw,"import producer")<>0 then
  Error("R07 v1 GHA driver: checker has producer import/reference");
fi;
D972R07V1Self:=
  IsBound(D972_R07_RELFRAT3_ACTUAL_CLASS_V1_SELFTEST) and
  D972_R07_RELFRAT3_ACTUAL_CLASS_V1_SELFTEST=true;;
D972R07V1Full:=
  IsBound(D972_R07_RELFRAT3_ACTUAL_CLASS_V1_RUN) and
  D972_R07_RELFRAT3_ACTUAL_CLASS_V1_RUN=true;;
if D972R07V1Self=D972R07V1Full then
  Error("R07 v1 GHA driver: select exactly one of SELFTEST and RUN");
fi;

if D972R07V1Self then
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_r07_relfrat3_actual_class_v1_checker_selftest.log' 'ci/out/d972_r07_relfrat3_actual_class_v1_checker_selftest.ok' && python3 -u -B search/check_d972_r07_relfrat3_actual_class_v1.py --self-test > 'ci/out/d972_r07_relfrat3_actual_class_v1_checker_selftest.log' 2>&1 && printf '%s' 'D972_R07_RELFRAT3_ACTUAL_CLASS_V1_CHECKER_SELFTEST_EXIT_ZERO' > 'ci/out/d972_r07_relfrat3_actual_class_v1_checker_selftest.ok'");;
  D972R07V1Raw:=D972R07V1ReadRequired(D972R07V1SelfLog,"selftest log");;
  if StringFile(D972R07V1SelfOK)<>D972R07V1SelfSentinel then
    Error("R07 v1 GHA driver: selftest process did not exit zero");
  fi;
  D972R07V1RequireCleanLog(D972R07V1Raw,"selftest log");;
  if D972R07V1Count(D972R07V1Raw,D972R07V1SelfMarker)<>1 or
     D972R07V1Count(D972R07V1Raw,
       "R07_RELFRAT3_ACTUAL_CLASS_V1_CHECKER_SELFTEST_PASS")<>1 then
    Error("R07 v1 GHA driver: selftest marker count");
  fi;
  Print("R07_RELFRAT3_ACTUAL_CLASS_V1_GHA_DRIVER_PASS mode=selftest ",
        "checker_marker_count=1\n");;
else
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_r07_relfrat3_actual_class_v1_checker_full.log' 'ci/out/d972_r07_relfrat3_actual_class_v1_checker_full.ok' && bash -o pipefail -c 'python3 -u -B search/check_d972_r07_relfrat3_actual_class_v1.py --receipt search/certs/d972_r07_relfrat3_actual_class_preflight_v1_20260826.json --mutations 2>&1 | tee ci/out/d972_r07_relfrat3_actual_class_v1_checker_full.log' && printf '%s' 'D972_R07_RELFRAT3_ACTUAL_CLASS_V1_CHECKER_FULL_EXIT_ZERO' > 'ci/out/d972_r07_relfrat3_actual_class_v1_checker_full.ok'");;
  D972R07V1Raw:=D972R07V1ReadRequired(D972R07V1FullLog,"full log");;
  if StringFile(D972R07V1FullOK)<>D972R07V1FullSentinel then
    Error("R07 v1 GHA driver: full checker did not exit zero");
  fi;
  D972R07V1RequireCleanLog(D972R07V1Raw,"full log");;
  if D972R07V1Count(D972R07V1Raw,D972R07V1FullMarker)<>1 or
     D972R07V1Count(D972R07V1Raw,
       "R07_RELFRAT3_ACTUAL_CLASS_V1_CHECKER_PASS")<>1 then
    Error("R07 v1 GHA driver: full checker marker count");
  fi;
  Print("R07_RELFRAT3_ACTUAL_CLASS_V1_GHA_DRIVER_PASS mode=full ",
        "checker_marker_count=1 receipt_sha256=",D972R07V1ReceiptSHA,"\n");;
fi;
