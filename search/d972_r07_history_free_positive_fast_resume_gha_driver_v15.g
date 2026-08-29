#############################################################################
## A0 production successor: raised cap plus resumable UNKNOWN binding.
## ASCII only.
#############################################################################
D353BaseDriver:="search/d972_r07_history_free_positive_fast_resume_gha_driver_v13.g";;
D353BaseDriverBytes:=12538;;
D353BaseDriverSHA:="8e9a4db93d05af93641c417235c57bc864267f1f2aafd9f575dc57caebbd5238";;
D353Producer:="search/d972_r07_history_free_positive_fast_resume_v15.py";;
D353ProducerBytes:=2253;;
D353ProducerSHA:="6412ea39f1b0559738c44fff0a9aa5f6c8366c55193b74f5c6df1ded977dc2a9";;
D353Checker:="crosscheck/check_d972_r07_history_free_positive_fast_resume_v15.py";;
D353CheckerBytes:=1316;;
D353CheckerSHA:="5edc81c1436694e8495a444ce8ebb3efebd80fa9dcf62717f73874d5e55a5a3c";;
D353Inner:="ci/out/d972_r07_history_free_positive_fast_resume_v15_inner.g";;
D353OldBase:="d972_r07_history_free_positive_fast_resume_v13";;
D353NewBase:="d972_r07_history_free_positive_fast_resume_v15";;
D353OldProducerPin:="[D342Producer,147409,\"4d1be83fefbb1a1c0b23010825c0013b80650439b714dce7e35a6e0f53a2ff2a\"]";;
D353NewProducerPin:="[D342Producer,2253,\"6412ea39f1b0559738c44fff0a9aa5f6c8366c55193b74f5c6df1ded977dc2a9\"]";;
D353OldCheckerPin:="[D342Checker,131946,\"42e8f6df8d85169bf4039bc4195a0e47c284ad475a177414308ba28f99377b64\"]";;
D353NewCheckerPin:="[D342Checker,1316,\"5edc81c1436694e8495a444ce8ebb3efebd80fa9dcf62717f73874d5e55a5a3c\"]";;
D353OldSentinel:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V13_DRIVER_PASS";;
D353NewSentinel:="R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V15_DRIVER_PASS";;

D353Read:=function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task353 missing input ",path); fi;
  return raw;
end;;

D353Pin:=function(path,bytes,digest)
  local raw;
  raw:=D353Read(path);;
  if Length(raw)<>bytes or HexSHA256(raw)<>digest then
    Error("task353 pin drift ",path);
  fi;
end;;

D353Count:=function(raw,needle)
  local i,n,m,count;
  n:=Length(raw);;m:=Length(needle);;count:=0;;
  if m=0 then Error("task353 empty needle"); fi;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D353Pin(D353BaseDriver,D353BaseDriverBytes,D353BaseDriverSHA);;
D353Pin(D353Producer,D353ProducerBytes,D353ProducerSHA);;
D353Pin(D353Checker,D353CheckerBytes,D353CheckerSHA);;
D353Raw:=D353Read(D353BaseDriver);;
if D353Count(D353Raw,D353OldBase)<>5 or
   D353Count(D353Raw,D353OldProducerPin)<>1 or
   D353Count(D353Raw,D353OldCheckerPin)<>1 or
   D353Count(D353Raw,D353OldSentinel)<>1 then
  Error("task353 frozen substitution cardinality");
fi;
D353Patched:=ReplacedString(D353Raw,D353OldBase,D353NewBase);;
D353Patched:=ReplacedString(D353Patched,D353OldProducerPin,D353NewProducerPin);;
D353Patched:=ReplacedString(D353Patched,D353OldCheckerPin,D353NewCheckerPin);;
D353Patched:=ReplacedString(D353Patched,D353OldSentinel,D353NewSentinel);;
if D353Count(D353Patched,D353OldBase)<>0 or
   D353Count(D353Patched,D353OldProducerPin)<>0 or
   D353Count(D353Patched,D353OldCheckerPin)<>0 or
   D353Count(D353Patched,D353OldSentinel)<>0 or
   D353Count(D353Patched,D353NewBase)<>5 or
   D353Count(D353Patched,D353NewProducerPin)<>1 or
   D353Count(D353Patched,D353NewCheckerPin)<>1 or
   D353Count(D353Patched,D353NewSentinel)<>1 then
  Error("task353 patched substitution cardinality");
fi;

Exec("mkdir -p ci/out");;
D353Stream:=OutputTextFile(D353Inner,false);;
if D353Stream=fail then Error("task353 inner driver open"); fi;
SetPrintFormattingStatus(D353Stream,false);;
PrintTo(D353Stream,D353Patched);;
CloseStream(D353Stream);;
if D353Read(D353Inner)<>D353Patched then Error("task353 inner driver readback"); fi;
Read(D353Inner);;
