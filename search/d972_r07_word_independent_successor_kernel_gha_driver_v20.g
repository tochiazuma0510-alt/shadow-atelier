#############################################################################
## A4 v20 one-layer diagnostic/capture driver for the v12/v13 owners.
## ASCII only.  Frozen v6 driver is read directly.
#############################################################################
if not IsBound(D366Mode) or D366Mode<>"PRODUCTION" then
 Error("task366 PRODUCTION required");
fi;

D366Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g";;
D366BaseBytes:=13775;;
D366BaseSHA:="a12c9267d050fe8ae9155cc9c42dd35dc5f1a66452c54f6a2cc7246f9a009fb0";;
D366Inner:="ci/out/a4_task366_inner.g";;
D366Pairs:=[
 ["D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v6.py\";;",
  "D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v12.py\";;"],
 ["D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py\";;",
  "D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v14.py\";;"],
 ["D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g\";;",
  "D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v20.g\";;"],
 ["D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.json\";;",
  "D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v20diag.json\";;"],
 ["D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.verdict.json\";;",
  "D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v20diag.verdict.json\";;"],
 ["D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.checkpoint.json\";;",
  "D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v20diag.producer.checkpoint.json\";;"],
 ["D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.checkpoint.json\";;",
  "D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v20diag.checker.checkpoint.json\";;"],
 ["D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.log\";;",
  "D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v20diag.producer.log\";;"],
 ["D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.log\";;",
  "D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v20diag.checker.log\";;"],
 ["D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.sh\";;",
  "D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v20diag.sh\";;"],
 ["D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.ok\";;",
  "D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v20diag.ok\";;"],
 ["[D345Producer,219187,\"aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a\"],",
  "[D345Producer,7209,\"816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5\"],"],
 ["[D345Checker,258847,\"432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf\"],",
  "[D345Checker,8074,\"7ff0fb8888b46febb8b373914a3ba31ee555e43c829e60dae915bacfb16b7b47\"],"]
];;

D366Read:=function(path)
 local raw;
 raw:=StringFile(path);;
 if raw=fail or Length(raw)=0 then Error("task366 missing input ",path); fi;
 return raw;
end;;
D366Count:=function(raw,needle)
 local i,n,m,count;
 n:=Length(raw);;m:=Length(needle);;count:=0;;
 if m=0 then Error("task366 empty needle"); fi;
 if n<m then return 0; fi;
 for i in [1..n-m+1] do
  if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
 od;
 return count;
end;;
D366ReplaceOnce:=function(raw,old,new)
 if D366Count(raw,old)<>1 then Error("task366 replacement cardinality"); fi;
 return ReplacedString(raw,old,new);
end;;

D366Raw:=D366Read(D366Base);;
if Length(D366Raw)<>D366BaseBytes or HexSHA256(D366Raw)<>D366BaseSHA then
 Error("task366 frozen v6 driver drift");
fi;
for D366Pair in D366Pairs do D366Raw:=D366ReplaceOnce(D366Raw,D366Pair[1],D366Pair[2]);; od;
D366OldTail:=Concatenation(
 "Exec(\"bash ci/out/d972_r07_word_independent_successor_kernel_v6.sh\");\n",
 "if not IsExistingFile(D345OK) then Error(\"task345 missing completion sentinel\"); fi;\n",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_DRIVER_PASS\\n\");");;
D366NewTail:=Concatenation(
 "D345DiagTail:=function(path,label) local raw,start; ",
 "if not IsExistingFile(path) then Print(label,\" MISSING\\n\"); return; fi; ",
 "raw:=D345Read(path); start:=Maximum(1,Length(raw)-65535); ",
 "Print(label,\" BEGIN\\n\",raw{[start..Length(raw)]},\"\\n\",label,\" END\\n\"); end;;\\n",
 "Exec(Concatenation(\"bash \",D345Sh));\\n",
 "if IsExistingFile(D345OK) then ",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V20_DRIVER_PASS\\n\"); ",
 "else Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V20_DIAGNOSTIC_NO_SENTINEL\\n\"); ",
 "D345DiagTail(D345PLog,\"A4_PRODUCER_LOG\"); ",
 "D345DiagTail(D345CLog,\"A4_CHECKER_LOG\"); fi;\\n",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V20_CAPTURE_PASS\\n\");");;
D366Raw:=D366ReplaceOnce(D366Raw,D366OldTail,D366NewTail);;

for D366Pair in D366Pairs do
 if D366Count(D366Raw,D366Pair[1])<>0 or D366Count(D366Raw,D366Pair[2])<>1 then
  Error("task366 post-replacement gate");
 fi;
od;
if D366Count(D366Raw,D366OldTail)<>0 or D366Count(D366Raw,D366NewTail)<>1 then
 Error("task366 diagnostic-tail gate");
fi;
Exec("mkdir -p ci/out");;
D366Stream:=OutputTextFile(D366Inner,false);;
if D366Stream=fail then Error("task366 inner driver open"); fi;
SetPrintFormattingStatus(D366Stream,false);;
PrintTo(D366Stream,D366Raw);;
CloseStream(D366Stream);;
if D366Read(D366Inner)<>D366Raw then Error("task366 inner readback"); fi;
D345Mode:="PRODUCTION";;
Read(D366Inner);;


