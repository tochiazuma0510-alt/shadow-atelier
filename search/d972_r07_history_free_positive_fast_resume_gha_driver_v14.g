#############################################################################
## A0 production successor: v13 semantics with only the stale cap lifted.
## ASCII only.
#############################################################################
D352BaseDriver:="search/d972_r07_history_free_positive_fast_resume_gha_driver_v13.g";;
D352BaseDriverBytes:=12538;;
D352BaseDriverSHA:="8e9a4db93d05af93641c417235c57bc864267f1f2aafd9f575dc57caebbd5238";;
D352Producer:="search/d972_r07_history_free_positive_fast_resume_v14.py";;
D352ProducerBytes:=981;;
D352ProducerSHA:="2b7342296613e02e9084c2045c780b1498d797db312570310f343510ea6eaa25";;
D352Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_v14.py";;
D352CheckerBytes:=1312;;
D352CheckerSHA:="8147e2d958d6463b7caf7f43e66b5f1e9fb0b162b5b822e140b2e8f424f5f7cd";;
D352Inner:="ci/out/d972_r07_history_free_positive_fast_resume_v14_inner.g";;
D352OldBase:="d972_r07_history_free_positive_fast_resume_v13";;
D352NewBase:="d972_r07_history_free_positive_fast_resume_v14";;
D352OldProducerPin:="[D342Producer,147409,\"4d1be83fefbb1a1c0b23010825c0013b80650439b714dce7e35a6e0f53a2ff2a\"]";;
D352NewProducerPin:="[D342Producer,981,\"2b7342296613e02e9084c2045c780b1498d797db312570310f343510ea6eaa25\"]";;
D352OldCheckerPin:="[D342Checker,131946,\"42e8f6df8d85169bf4039bc4195a0e47c284ad475a177414308ba28f99377b64\"]";;
D352NewCheckerPin:="[D342Checker,1312,\"8147e2d958d6463b7caf7f43e66b5f1e9fb0b162b5b822e140b2e8f424f5f7cd\"]";;
D352OldSentinel:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V13_DRIVER_PASS";;
D352NewSentinel:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V14_DRIVER_PASS";;

D352Read:=function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task352 missing input ",path); fi;
  return raw;
end;;

D352Pin:=function(path,bytes,digest)
  local raw;
  raw:=D352Read(path);;
  if Length(raw)<>bytes or HexSHA256(raw)<>digest then
    Error("task352 pin drift ",path);
  fi;
end;;

D352Count:=function(raw,needle)
  local i,n,m,count;
  n:=Length(raw);;m:=Length(needle);;count:=0;;
  if m=0 then Error("task352 empty needle"); fi;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D352Pin(D352BaseDriver,D352BaseDriverBytes,D352BaseDriverSHA);;
D352Pin(D352Producer,D352ProducerBytes,D352ProducerSHA);;
D352Pin(D352Checker,D352CheckerBytes,D352CheckerSHA);;
D352Raw:=D352Read(D352BaseDriver);;
if D352Count(D352Raw,D352OldBase)<>5 or
   D352Count(D352Raw,D352OldProducerPin)<>1 or
   D352Count(D352Raw,D352OldCheckerPin)<>1 or
   D352Count(D352Raw,D352OldSentinel)<>1 then
  Error("task352 frozen substitution cardinality");
fi;
D352Patched:=ReplacedString(D352Raw,D352OldBase,D352NewBase);;
D352Patched:=ReplacedString(D352Patched,D352OldProducerPin,D352NewProducerPin);;
D352Patched:=ReplacedString(D352Patched,D352OldCheckerPin,D352NewCheckerPin);;
D352Patched:=ReplacedString(D352Patched,D352OldSentinel,D352NewSentinel);;
if D352Count(D352Patched,D352OldBase)<>0 or
   D352Count(D352Patched,D352OldProducerPin)<>0 or
   D352Count(D352Patched,D352OldCheckerPin)<>0 or
   D352Count(D352Patched,D352OldSentinel)<>0 or
   D352Count(D352Patched,D352NewBase)<>5 or
   D352Count(D352Patched,D352NewProducerPin)<>1 or
   D352Count(D352Patched,D352NewCheckerPin)<>1 or
   D352Count(D352Patched,D352NewSentinel)<>1 then
  Error("task352 patched substitution cardinality");
fi;

Exec("mkdir -p ci/out");;
D352Stream:=OutputTextFile(D352Inner,false);;
if D352Stream=fail then Error("task352 inner driver open"); fi;
SetPrintFormattingStatus(D352Stream,false);;
PrintTo(D352Stream,D352Patched);;
CloseStream(D352Stream);;
if D352Read(D352Inner)<>D352Patched then Error("task352 inner driver readback"); fi;
Read(D352Inner);;
