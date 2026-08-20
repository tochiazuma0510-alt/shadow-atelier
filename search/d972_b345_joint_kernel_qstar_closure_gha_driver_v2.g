#############################################################################
## Versioned checker-only repair driver for the 157ee joint-kernel lane.
#############################################################################

D972JKV2BaseDriver :=
  "search/d972_b345_joint_kernel_qstar_closure_gha_driver_v1.g";;
D972JKV2BaseDriverSHA :=
  "ad536c97644ba28e511ca7cb1f58192bddfecdfce6630fd76dde108589303ad4";;
D972JKV2OldChecker :=
  "search/check_d972_b345_joint_kernel_qstar_closure_v1.py";;
D972JKV2OldCheckerSHA :=
  "9e721634d1f16be806e315eec263ec272bc023587f862703c094b7dd37c0111f";;
D972JKV2Checker :=
  "search/check_d972_b345_joint_kernel_qstar_closure_v2.py";;
D972JKV2CheckerSHA :=
  "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88";;
D972JKV2Task := "sol/luna_task_157ef_b345_joint_kernel_checker_repair.md";;
D972JKV2TaskSHA :=
  "e626802b32e9577e35f5543b252830abdc4461b409972c9f5536ea29d8bb14ed";;
D972JKV2Inner := "ci/out/d972_b345_joint_kernel_qstar_closure_v2_inner.g";;

D972JKV2Read := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("157ef driver: missing ",label); fi;
  return raw;
end;;

D972JKV2RequireSHA := function(path,expected)
  local raw,got;
  raw:=D972JKV2Read(path,path);;got:=HexSHA256(raw);;
  if got<>expected then Error("157ef driver: SHA drift ",path," got=",got); fi;
  return true;
end;;

D972JKV2Count := function(text,needle)
  local i,n,m,count;
  if not IsString(text) or not IsString(needle) or Length(needle)=0 then
    Error("157ef driver: occurrence input");
  fi;
  n:=Length(text);;m:=Length(needle);;count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if text{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972JKV2Write := function(path,text)
  local stream,got;
  stream:=OutputTextFile(path,false);;
  if stream=fail then Error("157ef driver: inner write open"); fi;
  SetPrintFormattingStatus(stream,false);;PrintTo(stream,text);;CloseStream(stream);;
  got:=StringFile(path);;
  if got=fail or got<>text then Error("157ef driver: inner readback"); fi;
  return true;
end;;

D972JKV2RequireSHA(D972JKV2BaseDriver,D972JKV2BaseDriverSHA);;
D972JKV2RequireSHA(D972JKV2OldChecker,D972JKV2OldCheckerSHA);;
D972JKV2RequireSHA(D972JKV2Checker,D972JKV2CheckerSHA);;
D972JKV2RequireSHA(D972JKV2Task,D972JKV2TaskSHA);;

D972JKV2Raw:=D972JKV2Read(D972JKV2BaseDriver,"frozen v1 driver");;
if D972JKV2Count(D972JKV2Raw,D972JKV2OldChecker)<>3 or
   D972JKV2Count(D972JKV2Raw,D972JKV2OldCheckerSHA)<>1 then
  Error("157ef driver: frozen substitution cardinality");
fi;
D972JKV2Patched:=ReplacedString(D972JKV2Raw,D972JKV2OldChecker,
  D972JKV2Checker);;
D972JKV2Patched:=ReplacedString(D972JKV2Patched,D972JKV2OldCheckerSHA,
  D972JKV2CheckerSHA);;
if D972JKV2Count(D972JKV2Patched,D972JKV2OldChecker)<>0 or
   D972JKV2Count(D972JKV2Patched,D972JKV2OldCheckerSHA)<>0 or
   D972JKV2Count(D972JKV2Patched,D972JKV2Checker)<>3 or
   D972JKV2Count(D972JKV2Patched,D972JKV2CheckerSHA)<>1 then
  Error("157ef driver: patched substitution cardinality");
fi;

Exec("mkdir -p 'ci/out'");;
D972JKV2Write(D972JKV2Inner,D972JKV2Patched);;
Read(D972JKV2Inner);;

if D972JKSelf then
  D972JKV2Log:=D972JKV2Read(D972JKSelfLog,"v2 selftest log");;
  if D972JKV2Count(D972JKV2Log,
       "D972_B345_JOINT_KERNEL_QSTAR_CHECKER_V2_SELFTEST_PASS")<>1 then
    Error("157ef driver: repaired selftest marker");
  fi;
  Print("B345_JOINT_KERNEL_QSTAR_GHA_DRIVER_V2_PASS mode=selftest\n");;
else
  D972JKV2Log:=D972JKV2Read(D972JKCheckerLog,"v2 checker log");;
  if D972JKV2Count(D972JKV2Log,
       "D972_B345_JOINT_KERNEL_QSTAR_CHECKER_V2_PASS")<>1 then
    Error("157ef driver: repaired full checker marker");
  fi;
  Print("B345_JOINT_KERNEL_QSTAR_GHA_DRIVER_V2_PASS mode=full artifact_sha256=",
        HexSHA256(D972JKV2Read(D972JKArtifact,"final artifact")),"\n");;
fi;
