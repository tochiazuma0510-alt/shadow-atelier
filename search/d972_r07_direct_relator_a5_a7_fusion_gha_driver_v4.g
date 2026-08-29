#############################################################################
## Task376 direct-relator canonical-M A5/A7 binder. ASCII only.
#############################################################################
if not IsBound(D376Mode) then Error("task376 MODE required"); fi;
if D376Mode<>"PRODUCTION" then Error("task376 production-only mode"); fi;
if not IsBound(D376Task193Receipt) then
  Error("task376 task193 receipt required");
fi;
if not IsBound(D376Task193Verdict) then
  Error("task376 task193 verdict required");
fi;

D376Producer:="search/d972_r07_direct_relator_a5_a7_fusion_v4.py";;
D376Checker:="crosscheck/check_d972_r07_direct_relator_a5_a7_fusion_v4.py";;
D376ProducerBytes:=26841;;
D376ProducerSHA:="0f07716b38c427eeaa9bd920721a170ede85d0cad805f2fa55bbe614bd9229f1";;
D376CheckerBytes:=24239;;
D376CheckerSHA:="f494d12c050e4d1c5f199fa771d56ca5326c365439e617f2cbe892cf7b3b6a01";;
D376Receipt:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v4.json";;
D376Verdict:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v4.checker.json";;
D376Checkpoint:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v4.checkpoint.json";;
D376Sidecar:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v4.a5-sidecar.json";;
D376ProducerLog:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v4.producer.log";;
D376CheckerLog:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v4.checker.log";;
D376Script:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v4.sh";;
D376OK:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v4.ok";;

D376SafePath:=function(path,area)
  local bad;
  if not IsString(path) or Length(path)<7 or path{[1..6]}<>area then
    return false;
  fi;
  for bad in [" ","'","\"",";","&","|","$","(",")","<",">"] do
    if Position(path,bad[1])<>fail then return false; fi;
  od;
  if Position(path,CharInt(96))<>fail then return false; fi;
  return true;
end;;

if not D376SafePath(D376Task193Receipt,"ci/in/") then
  Error("task376 bad task193 receipt path");
fi;
if not D376SafePath(D376Task193Verdict,"ci/in/") then
  Error("task376 bad task193 verdict path");
fi;

D376ResumeBound:=IsBound(D376ResumePath);;
if D376ResumeBound<>IsBound(D376ResumeBytes) or
   D376ResumeBound<>IsBound(D376ResumeSHA) then
  Error("task376 resume path/bytes/SHA must be all-or-none");
fi;
D376ResumeArgs:="";;
if D376ResumeBound then
  if not D376SafePath(D376ResumePath,"ci/in/") then
    Error("task376 bad resume path");
  fi;
  if not IsInt(D376ResumeBytes) or D376ResumeBytes<=0 then
    Error("task376 bad resume bytes");
  fi;
  if not IsString(D376ResumeSHA) or Length(D376ResumeSHA)<>64 then
    Error("task376 bad resume SHA");
  fi;
  D376ResumeArgs:=Concatenation(" --resume-path ",D376ResumePath,
    " --resume-bytes ",String(D376ResumeBytes),
    " --resume-sha256 ",D376ResumeSHA);
fi;

for D376Path in [D376Receipt,D376Verdict,D376Checkpoint,D376Sidecar,
                 D376ProducerLog,D376CheckerLog,D376Script,D376OK] do
  if IsExistingFile(D376Path) then Error("task376 stale output ",D376Path); fi;
od;
Exec("mkdir -p ci/out");;
D376S:=OutputTextFile(D376Script,false);;
if D376S=fail then Error("task376 script open"); fi;
SetPrintFormattingStatus(D376S,false);;
PrintTo(D376S,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D376S,"test \"$(wc -c < ",D376Producer,")\" = \"",
  String(D376ProducerBytes),"\"\n");;
PrintTo(D376S,"test \"$(sha256sum ",D376Producer,
  " | awk '{print $1}')\" = \"",D376ProducerSHA,"\"\n");;
PrintTo(D376S,"test \"$(wc -c < ",D376Checker,")\" = \"",
  String(D376CheckerBytes),"\"\n");;
PrintTo(D376S,"test \"$(sha256sum ",D376Checker,
  " | awk '{print $1}')\" = \"",D376CheckerSHA,"\"\n");;
PrintTo(D376S,"python3 -u -B ",D376Producer,
  " --mode PRODUCTION --task193-receipt ",D376Task193Receipt,
  " --task193-verdict ",D376Task193Verdict,
  " --output ",D376Receipt,
  " --checkpoint ",D376Checkpoint,
  " --a5-sidecar ",D376Sidecar,D376ResumeArgs,
  " > ",D376ProducerLog," 2>&1\n");;
PrintTo(D376S,"cat ",D376ProducerLog,"\n");;
PrintTo(D376S,"p=$(sed -n 's/^R07_DIRECT_RELATOR_A5_A7_FUSION_V4_PRODUCER_TERMINAL //p' ",
  D376ProducerLog,")\n");;
PrintTo(D376S,"case \"$p\" in R07_DIRECT_RELATOR_A5_A7_FUSION_MEMBER|R07_ZERO_BASE_A5_A6_NONMEMBER|UNKNOWN_RESOURCE:*) ;; *) exit 1;; esac\n");;
PrintTo(D376S,"test -s ",D376Receipt," && test -s ",D376Checkpoint,"\n");;
PrintTo(D376S,"python3 -u -B ",D376Checker,
  " --mode PRODUCTION --task193-receipt ",D376Task193Receipt,
  " --task193-verdict ",D376Task193Verdict,
  " --receipt ",D376Receipt,
  " --checkpoint ",D376Checkpoint,
  " --a5-sidecar ",D376Sidecar,
  " --output ",D376Verdict,
  " > ",D376CheckerLog," 2>&1\n");;
PrintTo(D376S,"cat ",D376CheckerLog,"\n");;
PrintTo(D376S,"c=$(sed -n 's/^R07_DIRECT_RELATOR_A5_A7_FUSION_V4_CHECKER terminal=//p' ",
  D376CheckerLog,")\n");;
PrintTo(D376S,"test \"$c\" = \"$p\"\n");;
PrintTo(D376S,"grep -Eq '\"status\":\"ACCEPTED(_RESOURCE)?\"' ",
  D376Verdict,"\n");;
PrintTo(D376S,"grep -Fq '\"terminal\":\"'\"$p\"'\"' ",D376Verdict,"\n");;
PrintTo(D376S,"if test \"$p\" != R07_ZERO_BASE_A5_A6_NONMEMBER; then test -s ",
  D376Sidecar,"; fi\n");;
PrintTo(D376S,"test -s ",D376Receipt," && test -s ",D376Verdict,
  " && test -s ",D376ProducerLog," && test -s ",D376CheckerLog,
  " && test -s ",D376Checkpoint,"\n");;
PrintTo(D376S,"printf '%s\\n' 'R07_DIRECT_RELATOR_A5_A7_FUSION_V4_DRIVER_COMPLETE' > ",
  D376OK,"\n");;
CloseStream(D376S);;
Exec(Concatenation("bash ",D376Script));;
if not IsExistingFile(D376OK) then Error("task376 missing success marker"); fi;
Print("R07_DIRECT_RELATOR_A5_A7_FUSION_V4_DRIVER_COMPLETE\n");;
