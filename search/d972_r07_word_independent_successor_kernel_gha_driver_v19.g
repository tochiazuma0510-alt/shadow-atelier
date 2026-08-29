#############################################################################
## A4 v19 one-layer diagnostic/capture driver for the v12/v13 owners.
## ASCII only.  Frozen v6 driver is read directly.
#############################################################################
if not IsBound(D364Mode) or D364Mode<>"PRODUCTION" then
 Error("task364 PRODUCTION required");
fi;

D364Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g";;
D364BaseBytes:=13775;;
D364BaseSHA:="a12c9267d050fe8ae9155cc9c42dd35dc5f1a66452c54f6a2cc7246f9a009fb0";;
D364Inner:="ci/out/a4_task364_inner.g";;
D364Pairs:=[
 ["D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v6.py\";;",
  "D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v12.py\";;"],
 ["D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py\";;",
  "D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v13.py\";;"],
 ["D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g\";;",
  "D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v19.g\";;"],
 ["D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.json\";;",
  "D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v19diag.json\";;"],
 ["D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.verdict.json\";;",
  "D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v19diag.verdict.json\";;"],
 ["D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.checkpoint.json\";;",
  "D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v19diag.producer.checkpoint.json\";;"],
 ["D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.checkpoint.json\";;",
  "D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v19diag.checker.checkpoint.json\";;"],
 ["D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.log\";;",
  "D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v19diag.producer.log\";;"],
 ["D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.log\";;",
  "D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v19diag.checker.log\";;"],
 ["D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.sh\";;",
  "D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v19diag.sh\";;"],
 ["D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.ok\";;",
  "D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v19diag.ok\";;"],
 ["[D345Producer,219187,\"aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a\"],",
  "[D345Producer,7209,\"816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5\"],"],
 ["[D345Checker,258847,\"432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf\"],",
  "[D345Checker,8050,\"f563f560d5987f7ca4e9fda07f53ddc525b53b99b13497ace04e90d1d766948b\"],"]
];;

D364Read:=function(path)
 local raw;
 raw:=StringFile(path);;
 if raw=fail or Length(raw)=0 then Error("task364 missing input ",path); fi;
 return raw;
end;;
D364Count:=function(raw,needle)
 local i,n,m,count;
 n:=Length(raw);;m:=Length(needle);;count:=0;;
 if m=0 then Error("task364 empty needle"); fi;
 if n<m then return 0; fi;
 for i in [1..n-m+1] do
  if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
 od;
 return count;
end;;
D364ReplaceOnce:=function(raw,old,new)
 if D364Count(raw,old)<>1 then Error("task364 replacement cardinality"); fi;
 return ReplacedString(raw,old,new);
end;;

D364Raw:=D364Read(D364Base);;
if Length(D364Raw)<>D364BaseBytes or HexSHA256(D364Raw)<>D364BaseSHA then
 Error("task364 frozen v6 driver drift");
fi;
for D364Pair in D364Pairs do D364Raw:=D364ReplaceOnce(D364Raw,D364Pair[1],D364Pair[2]);; od;
D364OldTail:=Concatenation(
 "Exec(\"bash ci/out/d972_r07_word_independent_successor_kernel_v6.sh\");\n",
 "if not IsExistingFile(D345OK) then Error(\"task345 missing completion sentinel\"); fi;\n",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_DRIVER_PASS\\n\");");;
D364NewTail:=Concatenation(
 "D345DiagTail:=function(path,label) local raw,start; ",
 "if not IsExistingFile(path) then Print(label,\" MISSING\\n\"); return; fi; ",
 "raw:=D345Read(path); start:=Maximum(1,Length(raw)-65535); ",
 "Print(label,\" BEGIN\\n\",raw{[start..Length(raw)]},\"\\n\",label,\" END\\n\"); end;;\\n",
 "Exec(Concatenation(\"bash \",D345Sh));\\n",
 "if IsExistingFile(D345OK) then ",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V19_DRIVER_PASS\\n\"); ",
 "else Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V19_DIAGNOSTIC_NO_SENTINEL\\n\"); ",
 "D345DiagTail(D345PLog,\"A4_PRODUCER_LOG\"); ",
 "D345DiagTail(D345CLog,\"A4_CHECKER_LOG\"); fi;\\n",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V19_CAPTURE_PASS\\n\");");;
D364Raw:=D364ReplaceOnce(D364Raw,D364OldTail,D364NewTail);;

for D364Pair in D364Pairs do
 if D364Count(D364Raw,D364Pair[1])<>0 or D364Count(D364Raw,D364Pair[2])<>1 then
  Error("task364 post-replacement gate");
 fi;
od;
if D364Count(D364Raw,D364OldTail)<>0 or D364Count(D364Raw,D364NewTail)<>1 then
 Error("task364 diagnostic-tail gate");
fi;
Exec("mkdir -p ci/out");;
D364Stream:=OutputTextFile(D364Inner,false);;
if D364Stream=fail then Error("task364 inner driver open"); fi;
SetPrintFormattingStatus(D364Stream,false);;
PrintTo(D364Stream,D364Raw);;
CloseStream(D364Stream);;
if D364Read(D364Inner)<>D364Raw then Error("task364 inner readback"); fi;
Read(D364Inner);;
