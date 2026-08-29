#############################################################################
## R07 task345 production-only validation repair driver v9. ASCII only.
#############################################################################
if not IsBound(D345Mode) or D345Mode<>"PRODUCTION" then
 Error("task345 v9 PRODUCTION required");
fi;

D345V9Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g";;
D345V9Generated:="ci/out/d972_r07_word_independent_successor_kernel_gha_driver_v9.generated.g";;
D345V9Raw:=StringFile(D345V9Base);;
if D345V9Raw=fail or Length(D345V9Raw)<>13775 or
   HexSHA256(D345V9Raw)<>"a12c9267d050fe8ae9155cc9c42dd35dc5f1a66452c54f6a2cc7246f9a009fb0" then
 Error("task345 v9 frozen v6 driver drift");
fi;

D345V9ReplaceOnce:=function(raw,old,new)
 local p;
 p:=PositionSublist(raw,old);
 if p=fail or PositionSublist(raw,old,p+1)<>fail then
  Error("task345 v9 replacement count");
 fi;
 return Concatenation(raw{[1..p-1]},new,raw{[p+Length(old)..Length(raw)]});
end;;

D345V9Raw:=D345V9ReplaceOnce(D345V9Raw,
 "D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v6.py\";;",
 "D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v8.py\";;");;
D345V9Raw:=D345V9ReplaceOnce(D345V9Raw,
 "D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py\";;",
 "D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v8.py\";;");;
D345V9Raw:=D345V9ReplaceOnce(D345V9Raw,
 "D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g\";;",
 "D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v9.g\";;");;
D345V9Raw:=D345V9ReplaceOnce(D345V9Raw,
 "D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.json\";;",
 "D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v8.json\";;");;
D345V9Raw:=D345V9ReplaceOnce(D345V9Raw,
 "D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.verdict.json\";;",
 "D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v8.verdict.json\";;");;
D345V9Raw:=D345V9ReplaceOnce(D345V9Raw,
 "D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.checkpoint.json\";;",
 "D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v8.producer.checkpoint.json\";;");;
D345V9Raw:=D345V9ReplaceOnce(D345V9Raw,
 "D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.checkpoint.json\";;",
 "D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v8.checker.checkpoint.json\";;");;
D345V9Raw:=D345V9ReplaceOnce(D345V9Raw,
 "D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.log\";;",
 "D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v8.producer.log\";;");;
D345V9Raw:=D345V9ReplaceOnce(D345V9Raw,
 "D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.log\";;",
 "D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v8.checker.log\";;");;
D345V9Raw:=D345V9ReplaceOnce(D345V9Raw,
 "D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.sh\";;",
 "D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v8.sh\";;");;
D345V9Raw:=D345V9ReplaceOnce(D345V9Raw,
 "D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.ok\";;",
 "D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v8.ok\";;");;
D345V9Raw:=D345V9ReplaceOnce(D345V9Raw,
 "[D345Producer,219187,\"aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a\"],",
 "[D345Producer,1599,\"dc22270e3c36c5025c495c012d68d702277979fb3446cb4051459502936ac5ea\"],");;
D345V9Raw:=D345V9ReplaceOnce(D345V9Raw,
 "[D345Checker,258847,\"432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf\"],",
 "[D345Checker,1614,\"c6099b732db86803ceeef66fb5db4c050828d0d7da4e3bfc92a66534d035cd84\"],");;
D345V9Raw:=D345V9ReplaceOnce(D345V9Raw,
 "Exec(\"bash ci/out/d972_r07_word_independent_successor_kernel_v6.sh\");",
 "Exec(\"bash ci/out/d972_r07_word_independent_successor_kernel_v8.sh\");");;

PrintTo(D345V9Generated,D345V9Raw);;
Read(D345V9Generated);;
