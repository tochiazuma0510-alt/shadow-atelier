#############################################################################
## A4 v22 PRODUCTION/RESUME diagnostic driver for the v13/v15 owners.
## ASCII only.  Frozen v6 driver is restored directly.
#############################################################################
if not IsBound(D383Mode) then Error("task383 MODE required"); fi;
if D383Mode<>"PRODUCTION" and D383Mode<>"RESUME" then
 Error("task383 MODE must be PRODUCTION or RESUME");
fi;

D383Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g";;
D383BaseBytes:=13775;;
D383BaseSHA:="a12c9267d050fe8ae9155cc9c42dd35dc5f1a66452c54f6a2cc7246f9a009fb0";;
D383Inner:="ci/out/a4_task383_inner.g";;
D383Pairs:=[
 ["D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v6.py\";;",
  "D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v13.py\";;"],
 ["D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py\";;",
  "D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v15.py\";;"],
 ["D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g\";;",
  "D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v22.g\";;"],
 ["D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.json\";;",
  "D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v22diag.json\";;"],
 ["D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.verdict.json\";;",
  "D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v22diag.verdict.json\";;"],
 ["D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.checkpoint.json\";;",
  "D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v22diag.producer.checkpoint.json\";;"],
 ["D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.checkpoint.json\";;",
  "D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v22diag.checker.checkpoint.json\";;"],
 ["D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.log\";;",
  "D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v22diag.producer.log\";;"],
 ["D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.log\";;",
  "D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v22diag.checker.log\";;"],
 ["D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.sh\";;",
  "D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v22diag.sh\";;"],
 ["D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.ok\";;",
  "D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v22diag.ok\";;"],
 ["[D345Producer,219187,\"aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a\"],",
  "[D345Producer,9731,\"c8e93ba9b72971428f2a8dba96049e183bfe1d794ac6008cb6495e6d5661f514\"],"],
 ["[D345Checker,258847,\"432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf\"],",
  "[D345Checker,10487,\"7779d545a679580130a0a191705f96e32834e67eaed37eb934e79aa7875a932d\"],"]
];;

D383Read:=function(path)
 local raw;
 raw:=StringFile(path);;
 if raw=fail or Length(raw)=0 then Error("task383 missing input ",path); fi;
 return raw;
end;;
D383Count:=function(raw,needle)
 local i,n,m,count;
 n:=Length(raw);; m:=Length(needle);; count:=0;;
 if m=0 then Error("task383 empty needle"); fi;
 if n<m then return 0; fi;
 for i in [1..n-m+1] do
  if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
 od;
 return count;
end;;
D383ReplaceOnce:=function(raw,old,new)
 if D383Count(raw,old)<>1 then Error("task383 replacement cardinality"); fi;
 return ReplacedString(raw,old,new);
end;;

D383Raw:=D383Read(D383Base);;
if Length(D383Raw)<>D383BaseBytes or HexSHA256(D383Raw)<>D383BaseSHA then
 Error("task383 frozen v6 driver drift");
fi;
for D383Pair in D383Pairs do
 D383Raw:=D383ReplaceOnce(D383Raw,D383Pair[1],D383Pair[2]);;
od;
D383OldTail:=Concatenation(
 "Exec(\"bash ci/out/d972_r07_word_independent_successor_kernel_v6.sh\");\n",
 "if not IsExistingFile(D345OK) then Error(\"task345 missing completion sentinel\"); fi;\n",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_DRIVER_PASS\\n\");");;
D383NewTail:=Concatenation(
 "D345DiagTail:=function(path,label) local raw,start; ",
 "if not IsExistingFile(path) then Print(label,\" MISSING\\n\"); return; fi; ",
 "raw:=D345Read(path); start:=Maximum(1,Length(raw)-65535); ",
 "Print(label,\" BEGIN\\n\",raw{[start..Length(raw)]},\"\\n\",label,\" END\\n\"); end;;\n",
 "Exec(Concatenation(\"bash \",D345Sh));\n",
 "if IsExistingFile(D345OK) then ",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V22_DRIVER_PASS\\n\"); ",
 "else Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V22_DIAGNOSTIC_NO_SENTINEL\\n\"); fi;\n",
 "D345DiagTail(D345PLog,\"A4_PRODUCER_LOG\");\n",
 "D345DiagTail(D345CLog,\"A4_CHECKER_LOG\");\n",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V22_CAPTURE_PASS\\n\");");;
D383Raw:=D383ReplaceOnce(D383Raw,D383OldTail,D383NewTail);;

for D383Pair in D383Pairs do
 if D383Count(D383Raw,D383Pair[1])<>0 or D383Count(D383Raw,D383Pair[2])<>1 then
  Error("task383 post-replacement gate");
 fi;
od;
if D383Count(D383Raw,D383OldTail)<>0 or D383Count(D383Raw,D383NewTail)<>1 then
 Error("task383 diagnostic-tail gate");
fi;
Exec("mkdir -p ci/out");;
D383Stream:=OutputTextFile(D383Inner,false);;
if D383Stream=fail then Error("task383 inner driver open"); fi;
SetPrintFormattingStatus(D383Stream,false);;
PrintTo(D383Stream,D383Raw);;
CloseStream(D383Stream);;
if D383Read(D383Inner)<>D383Raw then Error("task383 inner readback"); fi;
D345Mode:=D383Mode;;
Read(D383Inner);;
