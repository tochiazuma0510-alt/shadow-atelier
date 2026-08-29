#############################################################################
## Task377 positive lift-null dovetail driver. ASCII only.
#############################################################################
if not IsBound(D377Mode) then Error("task377 MODE required"); fi;
if D377Mode<>"PRODUCTION" then Error("task377 production-only mode"); fi;
if not IsBound(D377Task193Receipt) then
  Error("task377 task193 receipt required");
fi;
if not IsBound(D377Task193Verdict) then
  Error("task377 task193 verdict required");
fi;
if not IsBound(D377Cadence) then D377Cadence:=64; fi;
if not IsBound(D377Seconds) then D377Seconds:=14400; fi;
if not IsBound(D377RSSBytes) then D377RSSBytes:=5000000000; fi;
if not IsBound(D377Operations) then D377Operations:=2000000000; fi;
if not IsBound(D377CheckpointBytes) then
  D377CheckpointBytes:=2000000000;
fi;
if not IsInt(D377Cadence) or D377Cadence<=0 then
  Error("task377 bad cadence");
fi;
if not IsInt(D377Seconds) or D377Seconds<=0 then
  Error("task377 bad seconds");
fi;
if not IsInt(D377RSSBytes) or D377RSSBytes<=0 then
  Error("task377 bad RSS cap");
fi;
if not IsInt(D377Operations) or D377Operations<=0 then
  Error("task377 bad operation cap");
fi;
if not IsInt(D377CheckpointBytes) or D377CheckpointBytes<=0 then
  Error("task377 bad checkpoint cap");
fi;

D377Producer:="search/d972_r07_direct_relator_a5_a7_fusion_v6.py";;
D377Checker:="crosscheck/check_d972_r07_direct_relator_a5_a7_fusion_v6.py";;
D377ProducerBytes:=57826;;
D377ProducerSHA:="da9e8ca8e5ea2c30e92eef2d1dba772a0aa4d3eed9d894c7441c40cb49ac6441";;
D377CheckerBytes:=29830;;
D377CheckerSHA:="355dbf657f9b15f61e9fd8eb62717e4a9d905f69545408ac28126b96b38361cc";;
D377Receipt:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v6.json";;
D377Verdict:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v6.checker.json";;
D377Checkpoint:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v6.checkpoint.json";;
D377Sidecar:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v6.a5-sidecar.json";;
D377ProgressLog:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v6.progress.log";;
D377CheckerLog:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v6.checker.log";;
D377Script:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v6.sh";;
D377OK:="ci/out/d972_r07_direct_relator_a5_a7_fusion_v6.ok";;

D377SafePath:=function(path,area)
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

if not D377SafePath(D377Task193Receipt,"ci/in/") then
  Error("task377 bad task193 receipt path");
fi;
if not D377SafePath(D377Task193Verdict,"ci/in/") then
  Error("task377 bad task193 verdict path");
fi;

D377ResumeBound:=IsBound(D377ResumePath);;
if D377ResumeBound<>IsBound(D377ResumeBytes) or
   D377ResumeBound<>IsBound(D377ResumeSHA) then
  Error("task377 resume path/bytes/SHA must be all-or-none");
fi;
D377ResumeArgs:="";;
if D377ResumeBound then
  if not D377SafePath(D377ResumePath,"ci/in/") then
    Error("task377 bad resume path");
  fi;
  if not IsInt(D377ResumeBytes) or D377ResumeBytes<=0 then
    Error("task377 bad resume bytes");
  fi;
  if not IsString(D377ResumeSHA) or Length(D377ResumeSHA)<>64 then
    Error("task377 bad resume SHA");
  fi;
  D377ResumeArgs:=Concatenation(" --resume-path ",D377ResumePath,
    " --resume-bytes ",String(D377ResumeBytes),
    " --resume-sha256 ",D377ResumeSHA);
fi;

for D377Path in [D377Receipt,D377Verdict,D377Checkpoint,D377Sidecar,
                 D377ProgressLog,D377CheckerLog,D377Script,D377OK] do
  if IsExistingFile(D377Path) then Error("task377 stale output ",D377Path); fi;
od;
Exec("mkdir -p ci/out");;
D377S:=OutputTextFile(D377Script,false);;
if D377S=fail then Error("task377 script open"); fi;
SetPrintFormattingStatus(D377S,false);;
PrintTo(D377S,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D377S,"test \"$(wc -c < ",D377Producer,")\" = \"",
  String(D377ProducerBytes),"\"\n");;
PrintTo(D377S,"test \"$(sha256sum ",D377Producer,
  " | awk '{print $1}')\" = \"",D377ProducerSHA,"\"\n");;
PrintTo(D377S,"test \"$(wc -c < ",D377Checker,")\" = \"",
  String(D377CheckerBytes),"\"\n");;
PrintTo(D377S,"test \"$(sha256sum ",D377Checker,
  " | awk '{print $1}')\" = \"",D377CheckerSHA,"\"\n");;
PrintTo(D377S,"python3 -u -B ",D377Producer,
  " --mode PRODUCTION --task193-receipt ",D377Task193Receipt,
  " --task193-verdict ",D377Task193Verdict,
  " --output ",D377Receipt,
  " --checkpoint ",D377Checkpoint,
  " --a5-sidecar ",D377Sidecar,
  " --cadence ",String(D377Cadence),
  " --seconds ",String(D377Seconds),
  " --rss-bytes ",String(D377RSSBytes),
  " --max-operations ",String(D377Operations),
  " --checkpoint-bytes ",String(D377CheckpointBytes),D377ResumeArgs,
  " > ",D377ProgressLog," 2>&1\n");;
PrintTo(D377S,"cat ",D377ProgressLog,"\n");;
PrintTo(D377S,"p=$(sed -n 's/^R07_DIRECT_RELATOR_A5_A7_FUSION_V6_PRODUCER_TERMINAL //p' ",
  D377ProgressLog,")\n");;
PrintTo(D377S,"case \"$p\" in R07_DIRECT_RELATOR_A5_A7_FUSION_MEMBER|R07_ZERO_BASE_A5_A6_NONMEMBER|UNKNOWN_RESOURCE:*) ;; *) exit 1;; esac\n");;
PrintTo(D377S,"test -s ",D377Receipt," && test -s ",D377Checkpoint,"\n");;
PrintTo(D377S,"if test \"$p\" = R07_DIRECT_RELATOR_A5_A7_FUSION_MEMBER; then\n");;
PrintTo(D377S,"  test -s ",D377Sidecar,"\n");;
PrintTo(D377S,"  python3 -u -B ",D377Checker,
  " --mode PRODUCTION --task193-receipt ",D377Task193Receipt,
  " --task193-verdict ",D377Task193Verdict,
  " --receipt ",D377Receipt,
  " --checkpoint ",D377Checkpoint,
  " --a5-sidecar ",D377Sidecar,
  " --output ",D377Verdict,
  " --seconds ",String(D377Seconds),
  " --rss-bytes ",String(D377RSSBytes),
  " > ",D377CheckerLog," 2>&1\n");;
PrintTo(D377S,"  cat ",D377CheckerLog,"\n");;
PrintTo(D377S,"  c=$(sed -n 's/^R07_DIRECT_RELATOR_A5_A7_FUSION_V6_CHECKER terminal=//p' ",
  D377CheckerLog,")\n");;
PrintTo(D377S,"  test \"$c\" = \"$p\"\n");;
PrintTo(D377S,"  grep -Fq '\"status\":\"ACCEPTED\"' ",D377Verdict,"\n");;
PrintTo(D377S,"  grep -Fq '\"terminal\":\"R07_DIRECT_RELATOR_A5_A7_FUSION_MEMBER\"' ",
  D377Verdict,"\n");;
PrintTo(D377S,"else\n");;
PrintTo(D377S,"  test ! -e ",D377Verdict," && test ! -e ",D377CheckerLog,"\n");;
PrintTo(D377S,"fi\n");;
PrintTo(D377S,"printf '%s\\n' \"R07_DIRECT_RELATOR_A5_A7_FUSION_V6_DRIVER_COMPLETE terminal=$p\" > ",
  D377OK,"\n");;
CloseStream(D377S);;
Exec(Concatenation("bash ",D377Script));;
if not IsExistingFile(D377OK) then Error("task377 missing success marker"); fi;
Print("R07_DIRECT_RELATOR_A5_A7_FUSION_V6_DRIVER_COMPLETE\n");;
