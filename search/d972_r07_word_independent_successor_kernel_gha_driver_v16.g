#############################################################################
## R07 A4 actual driver with fail-closed diagnostic artifact capture.
## ASCII only.  The mathematical producer/checker are unchanged v11 owners.
#############################################################################
if not IsBound(D345Mode) or D345Mode<>"PRODUCTION" then
 Error("task357 PRODUCTION required");
fi;

D357Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g";;
D357BaseBytes:=13775;;
D357BaseSHA:="a12c9267d050fe8ae9155cc9c42dd35dc5f1a66452c54f6a2cc7246f9a009fb0";;
D357Inner:="ci/out/a4_task357_inner.g";;

D357Read:=function(path)
 local raw;
 raw:=StringFile(path);;
 if raw=fail or Length(raw)=0 then Error("task357 missing input ",path); fi;
 return raw;
end;;

D357Count:=function(raw,needle)
 local i,n,m,count;
 n:=Length(raw);;m:=Length(needle);;count:=0;;
 if m=0 then Error("task357 empty needle"); fi;
 if n<m then return 0; fi;
 for i in [1..n-m+1] do
  if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
 od;
 return count;
end;;

D357ReplaceOnce:=function(raw,old,new)
 if D357Count(raw,old)<>1 then Error("task357 replacement cardinality"); fi;
 return ReplacedString(raw,old,new);
end;;

D357Raw:=D357Read(D357Base);;
if Length(D357Raw)<>D357BaseBytes or HexSHA256(D357Raw)<>D357BaseSHA then
 Error("task357 frozen v6 driver drift");
fi;

D357Pairs:=[
 ["D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v6.py\";;",
  "D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v11.py\";;"],
 ["D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py\";;",
  "D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v11.py\";;"],
 ["D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g\";;",
  "D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v16.g\";;"],
 ["D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.json\";;",
  "D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v16diag.json\";;"],
 ["D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.verdict.json\";;",
  "D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v16diag.verdict.json\";;"],
 ["D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.checkpoint.json\";;",
  "D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v16diag.producer.checkpoint.json\";;"],
 ["D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.checkpoint.json\";;",
  "D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v16diag.checker.checkpoint.json\";;"],
 ["D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.log\";;",
  "D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v16diag.producer.log\";;"],
 ["D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.log\";;",
  "D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v16diag.checker.log\";;"],
 ["D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.sh\";;",
  "D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v16diag.sh\";;"],
 ["D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.ok\";;",
  "D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v16diag.ok\";;"],
 ["[D345Producer,219187,\"aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a\"],",
  "[D345Producer,2038,\"f3cccb104402ee031baba59487a8e4f71dbe8fb244ff220db96f8814950f868e\"],"],
 ["[D345Checker,258847,\"432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf\"],",
  "[D345Checker,2376,\"552e7d866574fe6d92bf3586c63ff2640057d19b77b6e982078c52b9ae896026\"],"]
];;
for D357Pair in D357Pairs do
 D357Raw:=D357ReplaceOnce(D357Raw,D357Pair[1],D357Pair[2]);;
od;

D357OldTail:=Concatenation(
 "Exec(\"bash ci/out/d972_r07_word_independent_successor_kernel_v6.sh\");\n",
 "if not IsExistingFile(D345OK) then Error(\"task345 missing completion sentinel\"); fi;\n",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_DRIVER_PASS\\n\");");;
D357NewTail:=Concatenation(
 "D345DiagTail:=function(path,label) local raw,start; ",
 "if not IsExistingFile(path) then Print(label,\" MISSING\\n\"); return; fi; ",
 "raw:=D345Read(path); start:=Maximum(1,Length(raw)-65535); ",
 "Print(label,\" BEGIN\\n\",raw{[start..Length(raw)]},\"\\n\",label,\" END\\n\"); end;;\n",
 "Exec(Concatenation(\"bash \",D345Sh));\n",
 "if IsExistingFile(D345OK) then ",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_DRIVER_PASS\\n\"); ",
 "else Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V16_DIAGNOSTIC_NO_SENTINEL\\n\"); ",
 "D345DiagTail(D345PLog,\"A4_PRODUCER_LOG\"); ",
 "D345DiagTail(D345CLog,\"A4_CHECKER_LOG\"); fi;\n",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V16_CAPTURE_PASS\\n\");");;
D357Raw:=D357ReplaceOnce(D357Raw,D357OldTail,D357NewTail);;

for D357Pair in D357Pairs do
 if D357Count(D357Raw,D357Pair[1])<>0 or D357Count(D357Raw,D357Pair[2])<>1 then
  Error("task357 post-replacement gate");
 fi;
od;
if D357Count(D357Raw,D357OldTail)<>0 or D357Count(D357Raw,D357NewTail)<>1 then
 Error("task357 diagnostic-tail gate");
fi;

Exec("mkdir -p ci/out");;
D357Stream:=OutputTextFile(D357Inner,false);;
if D357Stream=fail then Error("task357 inner driver open"); fi;
SetPrintFormattingStatus(D357Stream,false);;
PrintTo(D357Stream,D357Raw);;
CloseStream(D357Stream);;
if D357Read(D357Inner)<>D357Raw then Error("task357 inner readback"); fi;
Read(D357Inner);;
