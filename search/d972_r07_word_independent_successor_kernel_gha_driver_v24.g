#############################################################################
## A4 v24 PRODUCTION/RESUME driver for v15/v17 examined-cap owners.
## ASCII only. Frozen v6 driver is restored directly.
#############################################################################
if not IsBound(D385Mode) then Error("task385 MODE required"); fi;
if D385Mode<>"PRODUCTION" and D385Mode<>"RESUME" then
 Error("task385 MODE must be PRODUCTION or RESUME");
fi;

D385Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g";;
D385BaseBytes:=13775;;
D385BaseSHA:="a12c9267d050fe8ae9155cc9c42dd35dc5f1a66452c54f6a2cc7246f9a009fb0";;
D385Inner:="ci/out/a4_task385_inner.g";;
D385Pairs:=[
 ["D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v6.py\";;",
  "D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v15.py\";;"],
 ["D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py\";;",
  "D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v17.py\";;"],
 ["D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g\";;",
  "D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v24.g\";;"],
 ["D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.json\";;",
  "D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v24.json\";;"],
 ["D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.verdict.json\";;",
  "D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v24.verdict.json\";;"],
 ["D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.checkpoint.json\";;",
  "D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v24.producer.checkpoint.json\";;"],
 ["D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.checkpoint.json\";;",
  "D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v24.checker.checkpoint.json\";;"],
 ["D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.log\";;",
  "D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v24.producer.log\";;"],
 ["D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.log\";;",
  "D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v24.checker.log\";;"],
 ["D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.sh\";;",
  "D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v24.sh\";;"],
 ["D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.ok\";;",
  "D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v24.ok\";;"],
 ["[D345Producer,219187,\"aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a\"],",
  "[D345Producer,7417,\"964b2311ac4f2a06ec2a1136e4ff798a9db1760da83bc2809deb912d9c238be7\"],"],
 ["[D345Checker,258847,\"432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf\"],",
  "[D345Checker,7574,\"0b0281af7d38f4c255f7cd3346dc816987da863a29275a2c6c1851366171cef0\"],"]
];;

D385Read:=function(path)
 local raw;
 raw:=StringFile(path);;
 if raw=fail or Length(raw)=0 then Error("task385 missing input ",path); fi;
 return raw;
end;;
D385Count:=function(raw,needle)
 local i,n,m,count;
 n:=Length(raw);; m:=Length(needle);; count:=0;;
 if m=0 then Error("task385 empty needle"); fi;
 if n<m then return 0; fi;
 for i in [1..n-m+1] do
  if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
 od;
 return count;
end;;
D385ReplaceOnce:=function(raw,old,new)
 if D385Count(raw,old)<>1 then Error("task385 replacement cardinality"); fi;
 return ReplacedString(raw,old,new);
end;;

D385Raw:=D385Read(D385Base);;
if Length(D385Raw)<>D385BaseBytes or HexSHA256(D385Raw)<>D385BaseSHA then
 Error("task385 frozen v6 driver drift");
fi;
for D385Pair in D385Pairs do
 D385Raw:=D385ReplaceOnce(D385Raw,D385Pair[1],D385Pair[2]);;
od;
D385OldTail:=Concatenation(
 "Exec(\"bash ci/out/d972_r07_word_independent_successor_kernel_v6.sh\");\n",
 "if not IsExistingFile(D345OK) then Error(\"task345 missing completion sentinel\"); fi;\n",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_DRIVER_PASS\\n\");");;
D385NewTail:=Concatenation(
 "D345DiagTail:=function(path,label) local raw,start; ",
 "if not IsExistingFile(path) then Print(label,\" MISSING\\n\"); return; fi; ",
 "raw:=D345Read(path); start:=Maximum(1,Length(raw)-65535); ",
 "Print(label,\" BEGIN\\n\",raw{[start..Length(raw)]},\"\\n\",label,\" END\\n\"); end;;\n",
 "Exec(Concatenation(\"bash \",D345Sh));\n",
 "if IsExistingFile(D345OK) then ",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V24_DRIVER_PASS\\n\"); ",
 "else Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V24_DIAGNOSTIC_NO_SENTINEL\\n\"); fi;\n",
 "D345DiagTail(D345PLog,\"A4_PRODUCER_LOG\");\n",
 "D345DiagTail(D345CLog,\"A4_CHECKER_LOG\");\n",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V24_CAPTURE_PASS\\n\");");;
D385Raw:=D385ReplaceOnce(D385Raw,D385OldTail,D385NewTail);;

for D385Pair in D385Pairs do
 if D385Count(D385Raw,D385Pair[1])<>0 or D385Count(D385Raw,D385Pair[2])<>1 then
  Error("task385 post-replacement gate");
 fi;
od;
if D385Count(D385Raw,D385OldTail)<>0 or D385Count(D385Raw,D385NewTail)<>1 then
 Error("task385 diagnostic-tail gate");
fi;
Exec("mkdir -p ci/out");;
D385Stream:=OutputTextFile(D385Inner,false);;
if D385Stream=fail then Error("task385 inner driver open"); fi;
SetPrintFormattingStatus(D385Stream,false);;
PrintTo(D385Stream,D385Raw);;
CloseStream(D385Stream);;
if D385Read(D385Inner)<>D385Raw then Error("task385 inner readback"); fi;
D345Mode:=D385Mode;;
Read(D385Inner);;
