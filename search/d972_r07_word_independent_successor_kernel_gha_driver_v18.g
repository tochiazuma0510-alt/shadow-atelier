#############################################################################
## A4 v18 diagnostic/capture driver for the v12/v13 hot-path owners.
## ASCII only.  One producer and one independent checker invocation.
#############################################################################
if not IsBound(D361Mode) or D361Mode<>"PRODUCTION" then
 Error("task361 PRODUCTION required");
fi;

D361Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v16.g";;
D361BaseBytes:=5548;;
D361BaseSHA:="fea184f49f262d15bbe9b4a9a26c959d1e60f5d99fc79d47ec323c07a6179337";;
D361Inner:="ci/out/a4_task361_inner.g";;
D361Pairs:=[
 ["D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v6.py\";;",
  "D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v12.py\";;"],
 ["D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py\";;",
  "D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v13.py\";;"],
 ["D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g\";;",
  "D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v18.g\";;"],
 ["D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.json\";;",
  "D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v18diag.json\";;"],
 ["D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.verdict.json\";;",
  "D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v18diag.verdict.json\";;"],
 ["D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.checkpoint.json\";;",
  "D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v18diag.producer.checkpoint.json\";;"],
 ["D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.checkpoint.json\";;",
  "D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v18diag.checker.checkpoint.json\";;"],
 ["D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.log\";;",
  "D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v18diag.producer.log\";;"],
 ["D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.log\";;",
  "D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v18diag.checker.log\";;"],
 ["D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.sh\";;",
  "D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v18diag.sh\";;"],
 ["D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.ok\";;",
  "D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v18diag.ok\";;"],
 ["[D345Producer,219187,\"aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a\"],",
  "[D345Producer,7209,\"816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5\"],"],
 ["[D345Checker,258847,\"432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf\"],",
  "[D345Checker,8050,\"f563f560d5987f7ca4e9fda07f53ddc525b53b99b13497ace04e90d1d766948b\"],"]
];;

D361Read:=function(path)
 local raw;
 raw:=StringFile(path);;
 if raw=fail or Length(raw)=0 then Error("task361 missing input ",path); fi;
 return raw;
end;;
D361Count:=function(raw,needle)
 local i,n,m,count;
 n:=Length(raw);;m:=Length(needle);;count:=0;;
 if m=0 then Error("task361 empty needle"); fi;
 if n<m then return 0; fi;
 for i in [1..n-m+1] do
  if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
 od;
 return count;
end;;
D361ReplaceOnce:=function(raw,old,new)
 if D361Count(raw,old)<>1 then Error("task361 replacement cardinality"); fi;
 return ReplacedString(raw,old,new);
end;;

D361Raw:=D361Read(D361Base);;
if Length(D361Raw)<>D361BaseBytes or HexSHA256(D361Raw)<>D361BaseSHA then
 Error("task361 frozen v16 driver drift");
fi;
for D361Pair in D361Pairs do D361Raw:=D361ReplaceOnce(D361Raw,D361Pair[1],D361Pair[2]);; od;
D361OldTail:=Concatenation(
 "Exec(\"bash ci/out/d972_r07_word_independent_successor_kernel_v6.sh\");\n",
 "if not IsExistingFile(D345OK) then Error(\"task345 missing completion sentinel\"); fi;\n",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_DRIVER_PASS\\n\");");;
D361NewTail:=Concatenation(
 "D345DiagTail:=function(path,label) local raw,start; ",
 "if not IsExistingFile(path) then Print(label,\" MISSING\\n\"); return; fi; ",
 "raw:=D345Read(path); start:=Maximum(1,Length(raw)-65535); ",
 "Print(label,\" BEGIN\\n\",raw{[start..Length(raw)]},\"\\n\",label,\" END\\n\"); end;;\\n",
 "Exec(Concatenation(\"bash \",D345Sh));\\n",
 "if IsExistingFile(D345OK) then ",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V18_DRIVER_PASS\\n\"); ",
 "else Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V18_DIAGNOSTIC_NO_SENTINEL\\n\"); ",
 "D345DiagTail(D345PLog,\"A4_PRODUCER_LOG\"); ",
 "D345DiagTail(D345CLog,\"A4_CHECKER_LOG\"); fi;\\n",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V18_CAPTURE_PASS\\n\");");;
D361Raw:=D361ReplaceOnce(D361Raw,D361OldTail,D361NewTail);;

for D361Pair in D361Pairs do
 if D361Count(D361Raw,D361Pair[1])<>0 or D361Count(D361Raw,D361Pair[2])<>1 then
  Error("task361 post-replacement gate");
 fi;
od;
if D361Count(D361Raw,D361OldTail)<>0 or D361Count(D361Raw,D361NewTail)<>1 then
 Error("task361 diagnostic-tail gate");
fi;
Exec("mkdir -p ci/out");;
D361Stream:=OutputTextFile(D361Inner,false);;
if D361Stream=fail then Error("task361 inner driver open"); fi;
SetPrintFormattingStatus(D361Stream,false);;
PrintTo(D361Stream,D361Raw);;
CloseStream(D361Stream);;
if D361Read(D361Inner)<>D361Raw then Error("task361 inner readback"); fi;
Read(D361Inner);;
