#############################################################################
## R07 task345 production-only validation repair driver. ASCII only.
#############################################################################
if not IsBound(D345Mode) or D345Mode<>"PRODUCTION" then
 Error("task345 v7 PRODUCTION required");
fi;

D345V7Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g";;
D345V7Generated:="ci/out/d972_r07_word_independent_successor_kernel_gha_driver_v7.generated.g";;
D345V7Raw:=StringFile(D345V7Base);;
if D345V7Raw=fail or Length(D345V7Raw)<>13775 or
   HexSHA256(D345V7Raw)<>"a12c9267d050fe8ae9155cc9c42dd35dc5f1a66452c54f6a2cc7246f9a009fb0" then
 Error("task345 v7 frozen v6 driver drift");
fi;

D345V7ReplaceOnce:=function(raw,old,new)
 local p;
 p:=PositionSublist(raw,old);
 if p=fail or PositionSublist(raw,old,p+1)<>fail then
  Error("task345 v7 replacement count");
 fi;
 return Concatenation(raw{[1..p-1]},new,raw{[p+Length(old)..Length(raw)]});
end;;

D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,
 "D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v6.py\";;",
 "D345Producer:=\"search/d972_r07_word_independent_successor_kernel_v7.py\";;");;
D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,
 "D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v6.py\";;",
 "D345Checker:=\"crosscheck/check_d972_r07_word_independent_successor_kernel_v7.py\";;");;
D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,
 "D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v6.g\";;",
 "D345Driver:=\"search/d972_r07_word_independent_successor_kernel_gha_driver_v7.g\";;");;
D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,
 "D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.json\";;",
 "D345Receipt:=\"ci/out/d972_r07_word_independent_successor_kernel_v7.json\";;");;
D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,
 "D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.verdict.json\";;",
 "D345Verdict:=\"ci/out/d972_r07_word_independent_successor_kernel_v7.verdict.json\";;");;
D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,
 "D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.checkpoint.json\";;",
 "D345PCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v7.producer.checkpoint.json\";;");;
D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,
 "D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.checkpoint.json\";;",
 "D345CCheckpoint:=\"ci/out/d972_r07_word_independent_successor_kernel_v7.checker.checkpoint.json\";;");;
D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,
 "D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.producer.log\";;",
 "D345PLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v7.producer.log\";;");;
D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,
 "D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.checker.log\";;",
 "D345CLog:=\"ci/out/d972_r07_word_independent_successor_kernel_v7.checker.log\";;");;
D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,
 "D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.sh\";;",
 "D345Sh:=\"ci/out/d972_r07_word_independent_successor_kernel_v7.sh\";;");;
D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,
 "D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v6.ok\";;",
 "D345OK:=\"ci/out/d972_r07_word_independent_successor_kernel_v7.ok\";;");;
D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,
 "[D345Producer,219187,\"aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a\"],",
 "[D345Producer,1412,\"02cea428e003430a16493f90b4b82d1fb9d78f789bc28e51a54f764d555949be\"],");;
D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,
 "[D345Checker,258847,\"432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf\"],",
 "[D345Checker,1198,\"e81667190a0ae398aa4414df5e83525f0a8857e06e8362764b6728aad266f0d6\"],");;

PrintTo(D345V7Generated,D345V7Raw);;
Read(D345V7Generated);;
