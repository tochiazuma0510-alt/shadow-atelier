#############################################################################
## A0 transport successor: keep generated drivers outside owned-output prefix.
## ASCII only.
#############################################################################
D354Base:="search/d972_r07_history_free_positive_fast_resume_gha_driver_v15.g";;
D354BaseBytes:=3802;;
D354BaseSHA:="25506e156b6d524e13294f392a65bf8d24b048925d30a0dbc60e03be1b9117f7";;
D354OldInner:="ci/out/d972_r07_history_free_positive_fast_resume_v15_inner.g";;
D354NewInner:="ci/out/a0_task354_inner.g";;
D354Outer:="ci/out/a0_task354_outer.g";;

D354Read:=function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task354 missing input ",path); fi;
  return raw;
end;;

D354Count:=function(raw,needle)
  local i,n,m,count;
  n:=Length(raw);;m:=Length(needle);;count:=0;;
  if m=0 then Error("task354 empty needle"); fi;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D354Raw:=D354Read(D354Base);;
if Length(D354Raw)<>D354BaseBytes or HexSHA256(D354Raw)<>D354BaseSHA or
   D354Count(D354Raw,D354OldInner)<>1 or
   D354Count(D354Raw,D354NewInner)<>0 then
  Error("task354 frozen driver gate");
fi;
D354Patched:=ReplacedString(D354Raw,D354OldInner,D354NewInner);;
if D354Count(D354Patched,D354OldInner)<>0 or
   D354Count(D354Patched,D354NewInner)<>1 then
  Error("task354 substitution gate");
fi;
Exec("mkdir -p ci/out");;
D354Stream:=OutputTextFile(D354Outer,false);;
if D354Stream=fail then Error("task354 outer driver open"); fi;
SetPrintFormattingStatus(D354Stream,false);;
PrintTo(D354Stream,D354Patched);;
CloseStream(D354Stream);;
if D354Read(D354Outer)<>D354Patched then Error("task354 outer readback"); fi;
Read(D354Outer);;
