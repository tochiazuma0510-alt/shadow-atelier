#############################################################################
## A0 production successor: replayable pre-pool checkpoint and safe paths.
## ASCII only.
#############################################################################
D358Base:="search/d972_r07_history_free_positive_fast_resume_gha_driver_v15.g";;
D358BaseBytes:=3802;;
D358BaseSHA:="25506e156b6d524e13294f392a65bf8d24b048925d30a0dbc60e03be1b9117f7";;
D358Outer:="ci/out/a0_task358_outer.g";;

D358OldProducer:="D353Producer:=\"search/d972_r07_history_free_positive_fast_resume_v15.py\";;";;
D358NewProducer:="D353Producer:=\"search/d972_r07_history_free_positive_fast_resume_v17.py\";;";;
D358OldProducerBytes:="D353ProducerBytes:=2253;;";;
D358NewProducerBytes:="D353ProducerBytes:=2451;;";;
D358OldProducerSHA:="D353ProducerSHA:=\"6412ea39f1b0559738c44fff0a9aa5f6c8366c55193b74f5c6df1ded977dc2a9\";;";;
D358NewProducerSHA:="D353ProducerSHA:=\"8d88068960d71a7a5dffe93aeb7f8dd872e5b4e9b2ced181a15c7a1db8047ed1\";;";;
D358OldChecker:="D353Checker:=\"crosscheck/check_d972_r07_history_free_positive_fast_resume_v15.py\";;";;
D358NewChecker:="D353Checker:=\"crosscheck/check_d972_r07_history_free_positive_fast_resume_v17.py\";;";;
D358OldCheckerBytes:="D353CheckerBytes:=1316;;";;
D358NewCheckerBytes:="D353CheckerBytes:=1317;;";;
D358OldCheckerSHA:="D353CheckerSHA:=\"5edc81c1436694e8495a444ce8ebb3efebd80fa9dcf62717f73874d5e55a5a3c\";;";;
D358NewCheckerSHA:="D353CheckerSHA:=\"6056438d39c94534b2c48f47190053a7d74fd8ef3901919bb23698fb6c465a2d\";;";;
D358OldInner:="D353Inner:=\"ci/out/d972_r07_history_free_positive_fast_resume_v15_inner.g\";;";;
D358NewInner:="D353Inner:=\"ci/out/a0_task358_inner.g\";;";;
D358OldBase:="D353NewBase:=\"d972_r07_history_free_positive_fast_resume_v15\";;";;
D358NewBase:="D353NewBase:=\"d972_r07_history_free_positive_fast_resume_v17\";;";;
D358OldProducerPin:="D353NewProducerPin:=\"[D342Producer,2253,\\\"6412ea39f1b0559738c44fff0a9aa5f6c8366c55193b74f5c6df1ded977dc2a9\\\"]\";;";;
D358NewProducerPin:="D353NewProducerPin:=\"[D342Producer,2451,\\\"8d88068960d71a7a5dffe93aeb7f8dd872e5b4e9b2ced181a15c7a1db8047ed1\\\"]\";;";;
D358OldCheckerPin:="D353NewCheckerPin:=\"[D342Checker,1316,\\\"5edc81c1436694e8495a444ce8ebb3efebd80fa9dcf62717f73874d5e55a5a3c\\\"]\";;";;
D358NewCheckerPin:="D353NewCheckerPin:=\"[D342Checker,1317,\\\"6056438d39c94534b2c48f47190053a7d74fd8ef3901919bb23698fb6c465a2d\\\"]\";;";;
D358OldSentinel:="D353NewSentinel:=\"R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V15_DRIVER_PASS\";;";;
D358NewSentinel:="D353NewSentinel:=\"R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V17_DRIVER_PASS\";;";;

D358Read:=function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task358 missing input ",path); fi;
  return raw;
end;;

D358Count:=function(raw,needle)
  local i,n,m,count;
  n:=Length(raw);;m:=Length(needle);;count:=0;;
  if m=0 then Error("task358 empty needle"); fi;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D358Raw:=D358Read(D358Base);;
if Length(D358Raw)<>D358BaseBytes or HexSHA256(D358Raw)<>D358BaseSHA then
  Error("task358 frozen driver gate");
fi;
D358Pairs:=[
  [D358OldProducer,D358NewProducer],
  [D358OldProducerBytes,D358NewProducerBytes],
  [D358OldProducerSHA,D358NewProducerSHA],
  [D358OldChecker,D358NewChecker],
  [D358OldCheckerBytes,D358NewCheckerBytes],
  [D358OldCheckerSHA,D358NewCheckerSHA],
  [D358OldInner,D358NewInner],
  [D358OldBase,D358NewBase],
  [D358OldProducerPin,D358NewProducerPin],
  [D358OldCheckerPin,D358NewCheckerPin],
  [D358OldSentinel,D358NewSentinel]
];;
D358Patched:=D358Raw;;
for D358Pair in D358Pairs do
  if D358Count(D358Patched,D358Pair[1])<>1 or
     D358Count(D358Patched,D358Pair[2])<>0 then
    Error("task358 substitution cardinality");
  fi;
  D358Patched:=ReplacedString(D358Patched,D358Pair[1],D358Pair[2]);;
od;
for D358Pair in D358Pairs do
  if D358Count(D358Patched,D358Pair[1])<>0 or
     D358Count(D358Patched,D358Pair[2])<>1 then
    Error("task358 substitution gate");
  fi;
od;

Exec("mkdir -p ci/out");;
D358Stream:=OutputTextFile(D358Outer,false);;
if D358Stream=fail then Error("task358 outer driver open"); fi;
SetPrintFormattingStatus(D358Stream,false);;
PrintTo(D358Stream,D358Patched);;
CloseStream(D358Stream);;
if D358Read(D358Outer)<>D358Patched then Error("task358 outer readback"); fi;
Read(D358Outer);;
