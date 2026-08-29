#############################################################################
## Task379 actual-A0 class-two q2 driver. ASCII only; no dispatch or retry.
#############################################################################
if not IsBound(D379Mode) then Error("task379 MODE required"); fi;
if D379Mode<>"PRODUCTION" then Error("task379 production-only mode"); fi;
if not IsBound(D379Task193Receipt) then
  Error("task379 task193 receipt required");
fi;
if not IsBound(D379Task193Verdict) then
  Error("task379 task193 verdict required");
fi;
if not IsBound(D379Task198Receipt) then
  D379Task198Receipt:="ci/in/d972_r07_seven_context_roof_presentation_v1.json";
fi;
if not IsBound(D379Task198Manifest) then
  D379Task198Manifest:="ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json";
fi;
if not IsBound(D379Task198Producer) then
  D379Task198Producer:="ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt";
fi;
if not IsBound(D379Task198Checker) then
  D379Task198Checker:="ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt";
fi;
if not IsBound(D379Task198Verdict) then
  D379Task198Verdict:="ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json";
fi;
if not IsBound(D379Seconds) then D379Seconds:=14400; fi;
if not IsBound(D379RSSBytes) then D379RSSBytes:=5000000000; fi;
if not IsBound(D379Operations) then D379Operations:=2000000000; fi;
if not IsBound(D379CheckpointBytes) then D379CheckpointBytes:=200000000; fi;
if not IsInt(D379Seconds) or D379Seconds<=0 then
  Error("task379 bad seconds cap");
fi;
if not IsInt(D379RSSBytes) or D379RSSBytes<=0 then
  Error("task379 bad RSS cap");
fi;
if not IsInt(D379Operations) or D379Operations<=0 then
  Error("task379 bad operation cap");
fi;
if not IsInt(D379CheckpointBytes) or D379CheckpointBytes<65536 then
  Error("task379 bad checkpoint cap");
fi;

D379Producer:="search/d972_r07_actual_a0_class_two_q2_v1.py";;
D379Checker:="crosscheck/check_d972_r07_actual_a0_class_two_q2_v1.py";;
D379ProducerBytes:=50355;;
D379ProducerSHA:="c61d8f2cd96e6dd5c36089ddb83f6519c5e42b0dac66b42e9cec46ca9adfe9a6";;
D379CheckerBytes:=51554;;
D379CheckerSHA:="0b2d944d1655c359ab7252a732fe99f3c92add8e7ea9d45d44825707698deaa0";;
D379Receipt:="ci/out/d972_r07_actual_a0_class_two_q2_v1.json";;
D379Verdict:="ci/out/d972_r07_actual_a0_class_two_q2_v1.checker.json";;
D379Checkpoint:="ci/out/d972_r07_actual_a0_class_two_q2_v1.checkpoint.json";;
D379ProducerLog:="ci/out/d972_r07_actual_a0_class_two_q2_v1.producer.log";;
D379CheckerLog:="ci/out/d972_r07_actual_a0_class_two_q2_v1.checker.log";;
D379Script:="ci/out/d972_r07_actual_a0_class_two_q2_v1.sh";;
D379OK:="ci/out/d972_r07_actual_a0_class_two_q2_v1.ok";;

D379SafeInput:=function(path)
  local bad;
  if not IsString(path) or Length(path)<7 or path{[1..6]}<>"ci/in/" then
    return false;
  fi;
  if PositionSublist(path,"/../")<>fail or
     PositionSublist(path,"/./")<>fail or
     PositionSublist(path,"//")<>fail or
     Position(path,'\\')<>fail then
    return false;
  fi;
  for bad in [" ","'","\"",";","&","|","$","(",")","<",">",
              "*","?","[","]","{","}","!","#",":","\t","\n","\r"] do
    if Position(path,bad[1])<>fail then return false; fi;
  od;
  if Position(path,CharInt(96))<>fail then return false; fi;
  return true;
end;;

D379IsHex64:=function(value)
  local letter;
  if not IsString(value) or Length(value)<>64 then return false; fi;
  for letter in value do
    if Position("0123456789abcdef",letter)=fail then return false; fi;
  od;
  return true;
end;;

for D379Input in [D379Task193Receipt,D379Task193Verdict,
                   D379Task198Receipt,D379Task198Manifest,
                   D379Task198Producer,D379Task198Checker,
                   D379Task198Verdict] do
  if not D379SafeInput(D379Input) then
    Error("task379 unsafe physical input path");
  fi;
od;

D379ResumeBound:=IsBound(D379ResumePath);;
if D379ResumeBound<>IsBound(D379ResumeBytes) or
   D379ResumeBound<>IsBound(D379ResumeSHA) then
  Error("task379 resume path/bytes/SHA must be all-or-none");
fi;
D379ResumeArgs:="";;
if D379ResumeBound then
  if not D379SafeInput(D379ResumePath) then
    Error("task379 unsafe resume path");
  fi;
  if not IsInt(D379ResumeBytes) or D379ResumeBytes<=0 then
    Error("task379 bad resume bytes");
  fi;
  if not D379IsHex64(D379ResumeSHA) then
    Error("task379 bad resume SHA");
  fi;
  D379ResumeArgs:=Concatenation(" --resume-path ",D379ResumePath,
    " --resume-bytes ",String(D379ResumeBytes),
    " --resume-sha256 ",D379ResumeSHA);
fi;

for D379Path in [D379Receipt,D379Verdict,D379Checkpoint,
                  D379ProducerLog,D379CheckerLog,D379Script,D379OK] do
  if IsExistingFile(D379Path) then Error("task379 stale output ",D379Path); fi;
od;
Exec("mkdir -p ci/out");;
D379S:=OutputTextFile(D379Script,false);;
if D379S=fail then Error("task379 script open"); fi;
SetPrintFormattingStatus(D379S,false);;
PrintTo(D379S,"#!/usr/bin/env bash\nset -euo pipefail\n");;
PrintTo(D379S,"test \"$(wc -c < ",D379Producer,")\" = \"",
  String(D379ProducerBytes),"\"\n");;
PrintTo(D379S,"test \"$(sha256sum ",D379Producer,
  " | awk '{print $1}')\" = \"",D379ProducerSHA,"\"\n");;
PrintTo(D379S,"test \"$(wc -c < ",D379Checker,")\" = \"",
  String(D379CheckerBytes),"\"\n");;
PrintTo(D379S,"test \"$(sha256sum ",D379Checker,
  " | awk '{print $1}')\" = \"",D379CheckerSHA,"\"\n");;
PrintTo(D379S,"python3 -u -B ",D379Producer,
  " --mode PRODUCTION --task193-receipt ",D379Task193Receipt,
  " --task193-verdict ",D379Task193Verdict,
  " --task198-receipt ",D379Task198Receipt,
  " --task198-manifest ",D379Task198Manifest,
  " --task198-producer ",D379Task198Producer,
  " --task198-checker ",D379Task198Checker,
  " --task198-verdict ",D379Task198Verdict,
  " --output ",D379Receipt,
  " --checkpoint ",D379Checkpoint,
  " --seconds ",String(D379Seconds),
  " --rss-bytes ",String(D379RSSBytes),
  " --max-operations ",String(D379Operations),
  " --checkpoint-bytes ",String(D379CheckpointBytes),D379ResumeArgs,
  " > ",D379ProducerLog," 2>&1\n");;
PrintTo(D379S,"cat ",D379ProducerLog,"\n");;
PrintTo(D379S,"p=$(sed -n 's/^R07_ACTUAL_A0_CLASS_TWO_Q2_V1_PRODUCER_TERMINAL //p' ",
  D379ProducerLog,")\n");;
PrintTo(D379S,"case \"$p\" in R07_ACTUAL_A0_CLASS_TWO_Q2_V1_COMPLETE|UNKNOWN_INPUT|UNKNOWN_RESOURCE) ;; *) exit 1;; esac\n");;
PrintTo(D379S,"test -s ",D379Receipt," && test -s ",D379Checkpoint,"\n");;
PrintTo(D379S,"final=\"$p\"\n");;
PrintTo(D379S,"if test \"$p\" = R07_ACTUAL_A0_CLASS_TWO_Q2_V1_COMPLETE; then\n");;
PrintTo(D379S,"  python3 -u -B ",D379Checker,
  " --mode PRODUCTION --task193-receipt ",D379Task193Receipt,
  " --task193-verdict ",D379Task193Verdict,
  " --task198-receipt ",D379Task198Receipt,
  " --task198-manifest ",D379Task198Manifest,
  " --task198-producer ",D379Task198Producer,
  " --task198-checker ",D379Task198Checker,
  " --task198-verdict ",D379Task198Verdict,
  " --receipt ",D379Receipt,
  " --checkpoint ",D379Checkpoint,
  " --output ",D379Verdict,
  " --seconds ",String(D379Seconds),
  " --rss-bytes ",String(D379RSSBytes),
  " --max-operations ",String(D379Operations),
  " > ",D379CheckerLog," 2>&1\n");;
PrintTo(D379S,"  cat ",D379CheckerLog,"\n");;
PrintTo(D379S,"  c=$(sed -n 's/^R07_ACTUAL_A0_CLASS_TWO_Q2_V1_CHECKER terminal=//p' ",
  D379CheckerLog,")\n");;
PrintTo(D379S,"  case \"$c\" in\n");;
PrintTo(D379S,"    R07_ACTUAL_A0_CLASS_TWO_Q2_V1_COMPLETE) grep -Fq '\"status\":\"ACCEPTED\"' ",D379Verdict," ;;\n");;
PrintTo(D379S,"    UNKNOWN_RESOURCE) grep -Fq '\"status\":\"UNKNOWN\"' ",D379Verdict,"; final=UNKNOWN_RESOURCE ;;\n");;
PrintTo(D379S,"    *) exit 1 ;;\n");;
PrintTo(D379S,"  esac\n");;
PrintTo(D379S,"else\n");;
PrintTo(D379S,"  test ! -e ",D379Verdict,"\n");;
PrintTo(D379S,"  printf '%s\\n' \"TASK379_CHECKER_NOT_RUN producer_terminal=$p\" > ",D379CheckerLog,"\n");;
PrintTo(D379S,"fi\n");;
PrintTo(D379S,"printf '%s\\n' \"R07_ACTUAL_A0_CLASS_TWO_Q2_V1_DRIVER_COMPLETE terminal=$final\" > ",D379OK,"\n");;
CloseStream(D379S);;
Exec(Concatenation("bash ",D379Script));;
if not IsExistingFile(D379OK) then Error("task379 missing success marker"); fi;
Print("R07_ACTUAL_A0_CLASS_TWO_Q2_V1_DRIVER_COMPLETE\n");;
