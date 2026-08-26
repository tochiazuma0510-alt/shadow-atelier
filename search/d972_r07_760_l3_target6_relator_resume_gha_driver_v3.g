#############################################################################
## R07 g760 L3 target6 full-relator-checkpoint producer-only driver v3.
## ASCII only.  One Python producer, zero checker processes.
#############################################################################

D972R3Producer :=
  "search/d972_r07_760_l3_target6_relator_resume_v3.py";;
D972R3Checker :=
  "crosscheck/check_d972_r07_760_l3_target6_resume_v2.py";;
D972R3Preflight :=
  "search/certs/d972_r07_760_l3_target6_relator_resume_preflight_v3_20260826.json";;
D972R3Artifact :=
  "ci/out/d972_r07_760_l3_target6_relator_resume_v3.json";;
D972R3Log :=
  "ci/out/d972_r07_760_l3_target6_relator_resume_v3_producer.log";;
D972R3Timing :=
  "ci/out/d972_r07_760_l3_target6_relator_resume_v3_timing.txt";;
D972R3Hashes :=
  "ci/out/d972_r07_760_l3_target6_relator_resume_v3_checkpoint_hashes.txt";;
D972R3OK :=
  "ci/out/d972_r07_760_l3_target6_relator_resume_v3.ok";;
D972R3CheckpointDir :=
  "ci/out/d972_r07_760_l3_target6_relator_resume_v3_checkpoints";;
D972R3InnerSeconds := 21000;;
D972R3OuterSeconds := 22500;;

D972R3Pins := [
  [D972R3Producer,
   "0f1ef3bfd341cc5e596b4d84e4122a56b87488dc894dbf58f0561f288ac8a22f",105736],
  [D972R3Checker,
   "7cc683ccf16880d3c8794573dfffcbbf0b453cdcf2e7cd2e5665eb78a9e26365",63772],
  [D972R3Preflight,
   "5928b30f0de8c0aa65e141cdb4101b77c412ab20541ee35c0b74e8680b68c59c",22409],
  ["sol/luna_task_165_r07_target6_relator_checkpoint_v3.md",
   "32025aa1cb8587188c57c1f164c1bcbd585a37b5f19f5abec89c458ca8d6084f",5132],
  ["search/d972_r07_760_l3_target6_resume_v2.py",
   "9f6f8c2d3d3dbbc69373e1413b5d47a8893d6be62b228dc04ecd522a4fa51238",35068],
  ["search/d972_r07_760_l3_target6_resume_gha_driver_v2.g",
   "6241566df743069b7da6924e7c2facd766ef058b622f5e44f87c90f1d5392935",17443],
  ["search/certs/d972_r07_760_l3_target6_resume_preflight_v2_20260826.json",
   "272d4c4e91bb0234d49316277b354b722dfcb1366e47e9bf00d745469a1c1a94",7986],
  ["sol/luna_task_164_r07_760_l3_target6_resume_v2.md",
   "761359bda0fc14543ab9266ec61139006403525d828811bb2af5d27d34ccfc9d",5292],
  ["sol/luna_reply_164_r07_760_l3_target6_resume_v2.md",
   "b7e1a59dd301813344a243733a3ea6bc19368e892b8ce1d86d4e9232cd2c25d2",12948],
  ["search/d972_r07_760_l3_target6_v1.py",
   "7048e73a02e76df5d49fd359c52d5be70ae99d70aa95ebe74b28c4a18f130fde",53284],
  ["ci/b345_157en_artifacts_32458556448/d972_b345_q3_chief_v1.json",
   "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72",231570]
];;

D972R3Read := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then
    Error("R07 relator resume v3 driver: missing or empty ",label);
  fi;
  return raw;
end;;

D972R3ReadMaybeEmpty := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail then
    Error("R07 relator resume v3 driver: missing ",label);
  fi;
  return raw;
end;;

D972R3Count := function(raw,needle)
  local i,n,m,count;
  if not IsString(raw) or not IsString(needle) or Length(needle)=0 then
    Error("R07 relator resume v3 driver: count input");
  fi;
  n:=Length(raw);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972R3Pin := function(row)
  local raw,got;
  if not IsList(row) or Length(row)<>3 or not IsString(row[1]) or
     not IsString(row[2]) or Length(row[2])<>64 or
     not IsInt(row[3]) or row[3]<=0 then
    Error("R07 relator resume v3 driver: malformed pin");
  fi;
  raw:=D972R3Read(row[1],row[1]);; got:=HexSHA256(raw);;
  if got<>row[2] or Length(raw)<>row[3] then
    Error("R07 relator resume v3 driver: pin drift ",row[1]);
  fi;
  return true;
end;;

D972R3CleanLog := function(raw,label)
  local token;
  for token in ["Traceback (most recent call last):", "SyntaxError",
                "RuntimeError", "Error,", "Reject:", " FAIL ",
                " failed"] do
    if D972R3Count(raw,token)<>0 then
      Error("R07 relator resume v3 driver: forbidden log token ",
            label," ",token);
    fi;
  od;
  return true;
end;;

D972R3ShellQuote := function(path)
  if not IsString(path) or Length(path)=0 or
     PositionSublist(path,"\"")<>fail or
     PositionSublist(path,"\n")<>fail or
     PositionSublist(path,"\r")<>fail then
    Error("R07 relator resume v3 driver: unsafe shell path");
  fi;
  return Concatenation("\"",path,"\"");
end;;

D972R3RemoveOwn := function(paths)
  local path;
  if Length(Set(paths))<>Length(paths) then
    Error("R07 relator resume v3 driver: duplicate cleanup path");
  fi;
  for path in paths do
    if IsExistingFile(path) then RemoveFile(path);; fi;
  od;
  if ForAny(paths,IsExistingFile) then
    Error("R07 relator resume v3 driver: stale own output survived");
  fi;
  return true;
end;;

D972R3RelatorPath := function(j,r)
  local js,rs;
  if not j in [9..12] or not r in [1..11] then
    Error("R07 relator resume v3 driver: relator index");
  fi;
  js:=String(j);; rs:=String(r);;
  if j<10 then js:=Concatenation("0",js);; fi;
  if r<10 then rs:=Concatenation("0",rs);; fi;
  return Concatenation(D972R3CheckpointDir,
    "/d972_r07_760_l3_target6_relator_resume_v3_j",js,
    "_r",rs,".checkpoint.jsonl.gz");
end;;

D972R3JPath := function(j)
  local js;
  if not j in [9..12] then
    Error("R07 relator resume v3 driver: j index");
  fi;
  js:=String(j);;
  if j<10 then js:=Concatenation("0",js);; fi;
  return Concatenation(D972R3CheckpointDir,
    "/d972_r07_760_l3_target6_relator_resume_v3_j",js,
    ".json");
end;;

for D972R3PinRow in D972R3Pins do D972R3Pin(D972R3PinRow);; od;

D972R3Self :=
  IsBound(D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_SELFTEST) and
  D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_SELFTEST=true;;
D972R3Run :=
  IsBound(D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RUN) and
  D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RUN=true;;
if D972R3Self=D972R3Run then
  Error("R07 relator resume v3 driver: select exactly one mode");
fi;

D972R3UsePython3 := false;;
if IsBound(D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_USE_PYTHON3) then
  if not D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_USE_PYTHON3 in
       [true,false] then
    Error("R07 relator resume v3 driver: USE_PYTHON3 boolean");
  fi;
  D972R3UsePython3:=
    D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_USE_PYTHON3;;
fi;
D972R3Python:="python";;
if D972R3UsePython3 then D972R3Python:="python3";; fi;
if D972R3Run and not D972R3UsePython3 then
  Error("R07 relator resume v3 driver: full requires python3");
fi;

D972R3ResumeRel :=
  IsBound(D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RESUME_RELATOR_J) or
  IsBound(D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RESUME_RELATOR_R);;
D972R3ResumeJ :=
  IsBound(D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RESUME_J);;
if D972R3ResumeRel and
   not (IsBound(D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RESUME_RELATOR_J)
        and
        IsBound(D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RESUME_RELATOR_R))
   then
  Error("R07 relator resume v3 driver: incomplete relator resume pair");
fi;
if D972R3ResumeRel and D972R3ResumeJ then
  Error("R07 relator resume v3 driver: two resume modes");
fi;
D972R3ResumePath:=fail;;
if D972R3ResumeRel then
  D972R3ResumeRelJ:=
    D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RESUME_RELATOR_J;;
  D972R3ResumeRelR:=
    D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RESUME_RELATOR_R;;
  D972R3ResumePath:=D972R3RelatorPath(
    D972R3ResumeRelJ,D972R3ResumeRelR);;
elif D972R3ResumeJ then
  D972R3ResumeJValue:=
    D972_R07_760_L3_TARGET6_RELATOR_RESUME_V3_RESUME_J;;
  D972R3ResumePath:=D972R3JPath(D972R3ResumeJValue);;
fi;

if D972R3Self then
  if D972R3ResumePath<>fail then
    Error("R07 relator resume v3 driver: selftest cannot resume");
  fi;
  D972R3TempDirectory:=DirectoryTemporary();;
  if D972R3TempDirectory=fail then
    Error("R07 relator resume v3 driver: no temporary directory");
  fi;
  D972R3SelfLog:=Filename(D972R3TempDirectory,"selftest.log");;
  D972R3SelfOK:=Filename(D972R3TempDirectory,"selftest.ok");;
  D972R3RemoveOwn([D972R3SelfLog,D972R3SelfOK]);;
  D972R3SelfCommand:=Concatenation(
    D972R3Python," -u -B ",D972R3ShellQuote(D972R3Producer),
    " --self-test > ",D972R3ShellQuote(D972R3SelfLog)," 2>&1 && ",
    "echo D972_R07_RELATOR_RESUME_V3_SELFTEST_EXIT_ZERO > ",
    D972R3ShellQuote(D972R3SelfOK));;
  if D972R3Count(D972R3SelfCommand,D972R3Producer)<>1 or
     D972R3Count(D972R3SelfCommand,D972R3Checker)<>0 then
    Error("R07 relator resume v3 driver: selftest command shape");
  fi;
  Exec(D972R3SelfCommand);;
  D972R3SelfRaw:=D972R3Read(D972R3SelfLog,"selftest log");;
  D972R3CleanLog(D972R3SelfRaw,"selftest");;
  if D972R3Count(D972R3Read(D972R3SelfOK,"selftest sentinel"),
       "D972_R07_RELATOR_RESUME_V3_SELFTEST_EXIT_ZERO")<>1 or
     D972R3Count(D972R3SelfRaw,
       "R07_760_L3_TARGET6_RELATOR_RESUME_V3_PRODUCER_SELFTEST_PASS")<>1 or
     D972R3Count(D972R3SelfRaw,"checkpoint_mutations=16")<>1 or
     D972R3Count(D972R3SelfRaw,"j2_exhaustive=59049")<>1 or
     D972R3Count(D972R3SelfRaw,"full_pivots=true")<>1 then
    Error("R07 relator resume v3 driver: selftest markers");
  fi;
  Print("R07_760_L3_TARGET6_RELATOR_RESUME_V3_GHA_DRIVER_PASS ",
        "mode=selftest producer_processes=1 checker_processes=0 ",
        "checkpoint_mutations=16 grade=CANDIDATE\n");;
else
  D972R3OwnOutputs:=[D972R3Artifact,D972R3Log,D972R3Timing,
                     D972R3Hashes,D972R3OK];;
  D972R3RemoveOwn(D972R3OwnOutputs);;
  Exec(Concatenation("mkdir -p ",D972R3ShellQuote(D972R3CheckpointDir)));;
  if D972R3ResumePath=fail then
    D972R3CheckpointOutputs:=[];;
    for D972R3J in [9..12] do
      for D972R3R in [1..11] do
        Add(D972R3CheckpointOutputs,D972R3RelatorPath(D972R3J,D972R3R));;
      od;
      Add(D972R3CheckpointOutputs,D972R3JPath(D972R3J));;
    od;
    D972R3RemoveOwn(D972R3CheckpointOutputs);;
    D972R3ResumeArg:="";;
    D972R3ResumeMode:="initial";;
  else
    if not IsExistingFile(D972R3ResumePath) then
      Error("R07 relator resume v3 driver: resume artifact not preseeded");
    fi;
    D972R3ResumeArg:=Concatenation(
      " --resume-checkpoint ",D972R3ShellQuote(D972R3ResumePath));;
    D972R3ResumeMode:="preseeded";;
  fi;
  D972R3FullCommand:=Concatenation(
    "bash -o pipefail -c 'set -e; SECONDS=0; ",
    "timeout --signal=TERM 22500s python3 -u -B ",D972R3Producer,
    " --full --seconds 21000 --checkpoint-dir ",D972R3CheckpointDir,
    " --output ",D972R3Artifact,D972R3ResumeArg,
    " 2>&1 | tee ",D972R3Log,"; producer_elapsed=$SECONDS; ",
    "final_margin=$((22500-SECONDS)); ",
    "if [ $final_margin -le 0 ]; then exit 98; fi; ",
    "find ",D972R3CheckpointDir,
    " -maxdepth 1 -type f -print0 | sort -z | xargs -0 -r sha256sum > ",
    D972R3Hashes,"; ",
    "checkpoint_count=$(wc -l < ",D972R3Hashes,"); ",
    "printf \"producer_elapsed=%s\\nfinal_margin=%s\\n",
    "inner_seconds=21000\\nouter_seconds=22500\\n",
    "producer_processes=1\\nchecker_processes=0\\n",
    "grade=CANDIDATE\\ncheckpoint_count=%s\\nresume_mode=%s\\n\" ",
    "$producer_elapsed $final_margin $checkpoint_count ",D972R3ResumeMode,
    " > ",D972R3Timing,"; ",
    "printf %s D972_R07_RELATOR_RESUME_V3_EXIT_ZERO > ",D972R3OK,"'");;
  if D972R3Count(D972R3FullCommand,
       "python3 -u -B search/d972_r07_760_l3_target6_relator_resume_v3.py")<>1 or
     D972R3Count(D972R3FullCommand,"--full")<>1 or
     D972R3Count(D972R3FullCommand,"--seconds 21000")<>1 or
     D972R3Count(D972R3FullCommand,D972R3Checker)<>0 or
     PositionSublist(D972R3FullCommand,"crosscheck/")<>fail then
    Error("R07 relator resume v3 driver: full command shape");
  fi;
  Exec(D972R3FullCommand);;
  if D972R3Read(D972R3OK,"full sentinel")<>
       "D972_R07_RELATOR_RESUME_V3_EXIT_ZERO" then
    Error("R07 relator resume v3 driver: producer process");
  fi;
  D972R3Raw:=D972R3Read(D972R3Log,"producer log");;
  D972R3CleanLog(D972R3Raw,"producer");;
  if D972R3Count(D972R3Raw,
       "R07_760_L3_TARGET6_RELATOR_RESUME_V3_PRODUCER_PASS")<>1 then
    Error("R07 relator resume v3 driver: producer marker");
  fi;
  D972R3ReceiptRaw:=D972R3Read(D972R3Artifact,"full receipt");;
  D972R3ReceiptSHA:=HexSHA256(D972R3ReceiptRaw);;
  if D972R3Count(D972R3Raw,
       Concatenation(" sha256=",D972R3ReceiptSHA))<>1 or
     D972R3Count(D972R3Raw,
       Concatenation(" bytes=",String(Length(D972R3ReceiptRaw))))<>1 or
     D972R3Count(D972R3ReceiptRaw,"\"grade\":\"CANDIDATE\"")<1 or
     D972R3Count(D972R3ReceiptRaw,
       "\"full_relator_state_serialized\":true")<>1 or
     D972R3Count(D972R3ReceiptRaw,
       "\"relator_checkpoint_is_resource_recovery_only\":true")<>1 or
     D972R3Count(D972R3ReceiptRaw,
       "\"inherited_prefix_grade\":\"producer_control_flow_candidate_only\"")<>1 then
    Error("R07 relator resume v3 driver: receipt envelope");
  fi;
  for D972R3Claim in ["actual_A18_occurrence","all_bases_obstruction",
      "compatible_cofinal_lift","ihara_witness",
      "normalized_Brunnian_class"] do
    if D972R3Count(D972R3ReceiptRaw,
         Concatenation("\"",D972R3Claim,"\":false"))<1 then
      Error("R07 relator resume v3 driver: false global claim");
    fi;
  od;
  D972R3TerminalCount:=0;; D972R3Terminal:=fail;;
  for D972R3Token in ["R07_760_L3_TARGET6_NONMEMBER",
      "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE",
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
      "R07_760_L3_TARGET6_INPUT_STOP"] do
    D972R3PCount:=D972R3Count(D972R3Raw,
      Concatenation("terminal=",D972R3Token));;
    D972R3JCount:=D972R3Count(D972R3ReceiptRaw,
      Concatenation("\"terminal_token\":\"",D972R3Token,"\""));;
    if D972R3PCount=1 and D972R3JCount=1 then
      D972R3TerminalCount:=D972R3TerminalCount+1;;
      D972R3Terminal:=D972R3Token;;
    elif D972R3PCount<>0 or D972R3JCount<>0 then
      Error("R07 relator resume v3 driver: terminal mismatch");
    fi;
  od;
  if D972R3TerminalCount<>1 then
    Error("R07 relator resume v3 driver: exclusive terminal");
  fi;
  D972R3HashRaw:=D972R3ReadMaybeEmpty(
    D972R3Hashes,"checkpoint hash ledger");;
  D972R3HashLines:=Filtered(SplitString(D972R3HashRaw,"\n","\r"),
                            line->Length(line)>0);;
  for D972R3HashLine in D972R3HashLines do
    if Length(D972R3HashLine)<68 or D972R3HashLine{[65,66]}<>"  " then
      Error("R07 relator resume v3 driver: hash ledger line");
    fi;
    D972R3CheckpointSHA:=D972R3HashLine{[1..64]};;
    D972R3CheckpointPath:=D972R3HashLine{[67..Length(D972R3HashLine)]};;
    if D972R3Count(D972R3ReceiptRaw,
         Concatenation("\"sha256\":\"",D972R3CheckpointSHA,"\""))<1 or
       D972R3Count(D972R3ReceiptRaw,
         Concatenation("\"path\":\"",D972R3CheckpointPath,"\""))<1 then
      Error("R07 relator resume v3 driver: checkpoint hash binding");
    fi;
  od;
  D972R3TimingRaw:=D972R3Read(D972R3Timing,"timing ledger");;
  if D972R3Count(D972R3TimingRaw,"inner_seconds=21000")<>1 or
     D972R3Count(D972R3TimingRaw,"outer_seconds=22500")<>1 or
     D972R3Count(D972R3TimingRaw,"producer_processes=1")<>1 or
     D972R3Count(D972R3TimingRaw,"checker_processes=0")<>1 or
     D972R3Count(D972R3TimingRaw,
       Concatenation("checkpoint_count=",String(Length(D972R3HashLines))))<>1 then
    Error("R07 relator resume v3 driver: timing ledger");
  fi;
  Print("R07_760_L3_TARGET6_RELATOR_RESUME_V3_GHA_DRIVER_PASS mode=full ",
        "terminal=",D972R3Terminal," grade=CANDIDATE cross_checked=false ",
        "producer_processes=1 checker_processes=0 checkpoints=",
        Length(D972R3HashLines)," resume_mode=",D972R3ResumeMode,
        " receipt_sha256=",D972R3ReceiptSHA,
        " receipt_bytes=",Length(D972R3ReceiptRaw),
        " log_sha256=",HexSHA256(D972R3Raw),
        " timing_sha256=",HexSHA256(D972R3TimingRaw),
        " checkpoint_hash_ledger_sha256=",HexSHA256(D972R3HashRaw),"\n");;
fi;
