#############################################################################
## A4 v23 PRODUCTION/RESUME driver for the v14/v16 canonical batch owners.
## ASCII only.  Frozen v6 driver is restored directly.
#############################################################################
if not IsBound(D384Mode) then Error("task384 MODE required"); fi;
if D384Mode<>"PRODUCTION" and D384Mode<>"RESUME" then
 Error("task384 MODE must be PRODUCTION or RESUME");
fi;

D384Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g";;
D384BaseBytes:=13775;;
D384BaseSHA:="a12c9267d050fe8ae9155cc9c42dd35dc5f1a66452c54f6a2cc7246f9a009fb0";;
D384Inner:="ci/out/a4_task384_inner.g";;
D384Pairs:=[
 ["D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v6.py\";;",
  "D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v14.py\";;"],
 ["D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py\";;",
  "D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v16.py\";;"],
 ["D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g\";;",
  "D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v23.g\";;"],
 ["D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.json\";;",
  "D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v23.json\";;"],
 ["D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.verdict.json\";;",
  "D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v23.verdict.json\";;"],
 ["D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.checkpoint.json\";;",
  "D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v23.producer.checkpoint.json\";;"],
 ["D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.checkpoint.json\";;",
  "D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v23.checker.checkpoint.json\";;"],
 ["D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.log\";;",
  "D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v23.producer.log\";;"],
 ["D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.log\";;",
  "D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v23.checker.log\";;"],
 ["D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.sh\";;",
  "D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v23.sh\";;"],
 ["D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.ok\";;",
  "D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v23.ok\";;"],
 ["[D345Producer,219187,\"aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a\"],",
  "[D345Producer,11918,\"0c7595d50765062a6d2270d5b40c44b753f0ea4a96311795994a3c2502fe0c2c\"],"],
 ["[D345Checker,258847,\"432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf\"],",
  "[D345Checker,12407,\"1470f12585d8ed16bb1dea0480787ba99d80592d3a034215cbbde20748f6090e\"],"]
];;

D384Read:=function(path)
 local raw;
 raw:=StringFile(path);;
 if raw=fail or Length(raw)=0 then Error("task384 missing input ",path); fi;
 return raw;
end;;
D384Count:=function(raw,needle)
 local i,n,m,count;
 n:=Length(raw);; m:=Length(needle);; count:=0;;
 if m=0 then Error("task384 empty needle"); fi;
 if n<m then return 0; fi;
 for i in [1..n-m+1] do
  if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
 od;
 return count;
end;;
D384ReplaceOnce:=function(raw,old,new)
 if D384Count(raw,old)<>1 then Error("task384 replacement cardinality"); fi;
 return ReplacedString(raw,old,new);
end;;

D384Raw:=D384Read(D384Base);;
if Length(D384Raw)<>D384BaseBytes or HexSHA256(D384Raw)<>D384BaseSHA then
 Error("task384 frozen v6 driver drift");
fi;
for D384Pair in D384Pairs do
 D384Raw:=D384ReplaceOnce(D384Raw,D384Pair[1],D384Pair[2]);;
od;
D384OldTail:=Concatenation(
 "Exec(\"bash ci/out/d972_r07_word_independent_successor_kernel_v6.sh\");\n",
 "if not IsExistingFile(D345OK) then Error(\"task345 missing completion sentinel\"); fi;\n",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_DRIVER_PASS\\n\");");;
D384NewTail:=Concatenation(
 "D345DiagTail:=function(path,label) local raw,start; ",
 "if not IsExistingFile(path) then Print(label,\" MISSING\\n\"); return; fi; ",
 "raw:=D345Read(path); start:=Maximum(1,Length(raw)-65535); ",
 "Print(label,\" BEGIN\\n\",raw{[start..Length(raw)]},\"\\n\",label,\" END\\n\"); end;;\n",
 "Exec(Concatenation(\"bash \",D345Sh));\n",
 "if IsExistingFile(D345OK) then ",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V23_DRIVER_PASS\\n\"); ",
 "else Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V23_DIAGNOSTIC_NO_SENTINEL\\n\"); fi;\n",
 "D345DiagTail(D345PLog,\"A4_PRODUCER_LOG\");\n",
 "D345DiagTail(D345CLog,\"A4_CHECKER_LOG\");\n",
 "Print(\"R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V23_CAPTURE_PASS\\n\");");;
D384Raw:=D384ReplaceOnce(D384Raw,D384OldTail,D384NewTail);;

for D384Pair in D384Pairs do
 if D384Count(D384Raw,D384Pair[1])<>0 or D384Count(D384Raw,D384Pair[2])<>1 then
  Error("task384 post-replacement gate");
 fi;
od;
if D384Count(D384Raw,D384OldTail)<>0 or D384Count(D384Raw,D384NewTail)<>1 then
 Error("task384 diagnostic-tail gate");
fi;
Exec("mkdir -p ci/out");;
D384Stream:=OutputTextFile(D384Inner,false);;
if D384Stream=fail then Error("task384 inner driver open"); fi;
SetPrintFormattingStatus(D384Stream,false);;
PrintTo(D384Stream,D384Raw);;
CloseStream(D384Stream);;
if D384Read(D384Inner)<>D384Raw then Error("task384 inner readback"); fi;
D345Mode:=D384Mode;;
Read(D384Inner);;
