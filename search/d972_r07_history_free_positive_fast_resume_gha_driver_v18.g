#############################################################################
## A0 production successor: narrow pre-pool patch over the safe v17 route.
## ASCII only.
#############################################################################
D359Base:="search/d972_r07_history_free_positive_fast_resume_gha_driver_v17.g";;
D359BaseBytes:=4442;;
D359BaseSHA:="f67ab55fcbcf4ce14dfbd2b6344ce4c331ddddf6b3f2b4f7208365b8d1364784";;
D359Outer:="ci/out/a0_task359_outer.g";;
D359Pairs:=[
  ["v17","v18",3],
  ["V17","V18",1],
  ["2451","2557",2],
  ["8d88068960d71a7a5dffe93aeb7f8dd872e5b4e9b2ced181a15c7a1db8047ed1",
   "55505c6b59ebc9cc61c12c0229668509a2fcf7530ca14dbd791a8b18a95c5433",2],
  ["6056438d39c94534b2c48f47190053a7d74fd8ef3901919bb23698fb6c465a2d",
   "83ebfe5088388f5c84bbab9e52ef28cb8888fb944fbe417cf98041bab34bfaa9",2]
];;

D359Read:=function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task359 missing input ",path); fi;
  return raw;
end;;

D359Count:=function(raw,needle)
  local i,n,m,count;
  n:=Length(raw);;m:=Length(needle);;count:=0;;
  if m=0 then Error("task359 empty needle"); fi;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D359Raw:=D359Read(D359Base);;
if Length(D359Raw)<>D359BaseBytes or HexSHA256(D359Raw)<>D359BaseSHA then
  Error("task359 frozen driver gate");
fi;
D359Patched:=D359Raw;;
for D359Pair in D359Pairs do
  if D359Count(D359Patched,D359Pair[1])<>D359Pair[3] or
     D359Count(D359Patched,D359Pair[2])<>0 then
    Error("task359 substitution cardinality");
  fi;
  D359Patched:=ReplacedString(D359Patched,D359Pair[1],D359Pair[2]);;
od;
for D359Pair in D359Pairs do
  if D359Count(D359Patched,D359Pair[1])<>0 or
     D359Count(D359Patched,D359Pair[2])<>D359Pair[3] then
    Error("task359 substitution gate");
  fi;
od;

Exec("mkdir -p ci/out");;
D359Stream:=OutputTextFile(D359Outer,false);;
if D359Stream=fail then Error("task359 outer driver open"); fi;
SetPrintFormattingStatus(D359Stream,false);;
PrintTo(D359Stream,D359Patched);;
CloseStream(D359Stream);;
if D359Read(D359Outer)<>D359Patched then Error("task359 outer readback"); fi;
Read(D359Outer);;
