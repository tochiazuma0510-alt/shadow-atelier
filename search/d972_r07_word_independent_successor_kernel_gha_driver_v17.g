#############################################################################
## A4 production diagnostic with the v12 checkpoint producer-code pin.
## ASCII only.
#############################################################################
D360Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v16.g";;
D360BaseBytes:=5548;;
D360BaseSHA:="fea184f49f262d15bbe9b4a9a26c959d1e60f5d99fc79d47ec323c07a6179337";;
D360Outer:="ci/out/a4_task360_outer.g";;
D360Pairs:=[
 ["crosscheck/check_d972_r07_word_independent_successor_kernel_v11.py",
  "crosscheck/check_d972_r07_word_independent_successor_kernel_v12.py",1],
 ["2376","2562",1],
 ["552e7d866574fe6d92bf3586c63ff2640057d19b77b6e982078c52b9ae896026",
  "57eb2532df478c4b920e175746b8e51a66e060c76f38c7e8f7804664ceccc6f5",1],
 ["v16diag","v17diag",8],
 ["gha_driver_v16.g","gha_driver_v17.g",1],
 ["V16","V17",2]
];;

D360Read:=function(path)
 local raw;
 raw:=StringFile(path);;
 if raw=fail or Length(raw)=0 then Error("task360 missing input ",path); fi;
 return raw;
end;;

D360Count:=function(raw,needle)
 local i,n,m,count;
 n:=Length(raw);;m:=Length(needle);;count:=0;;
 if m=0 then Error("task360 empty needle"); fi;
 if n<m then return 0; fi;
 for i in [1..n-m+1] do
  if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
 od;
 return count;
end;;

D360Raw:=D360Read(D360Base);;
if Length(D360Raw)<>D360BaseBytes or HexSHA256(D360Raw)<>D360BaseSHA then
 Error("task360 frozen v16 driver drift");
fi;
D360Patched:=D360Raw;;
for D360Pair in D360Pairs do
 if D360Count(D360Patched,D360Pair[1])<>D360Pair[3] or
    D360Count(D360Patched,D360Pair[2])<>0 then
  Error("task360 replacement cardinality");
 fi;
 D360Patched:=ReplacedString(D360Patched,D360Pair[1],D360Pair[2]);;
od;
for D360Pair in D360Pairs do
 if D360Count(D360Patched,D360Pair[1])<>0 or
    D360Count(D360Patched,D360Pair[2])<>D360Pair[3] then
  Error("task360 post-replacement gate");
 fi;
od;

Exec("mkdir -p ci/out");;
D360Stream:=OutputTextFile(D360Outer,false);;
if D360Stream=fail then Error("task360 outer driver open"); fi;
SetPrintFormattingStatus(D360Stream,false);;
PrintTo(D360Stream,D360Patched);;
CloseStream(D360Stream);;
if D360Read(D360Outer)<>D360Patched then Error("task360 outer readback"); fi;
Read(D360Outer);;
