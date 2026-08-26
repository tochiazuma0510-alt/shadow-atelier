#############################################################################
## R07 g760 L3 target6 append-only-delta producer-only driver v4.
## ASCII only.  One Python producer, zero checker processes.
#############################################################################

D972R4Producer :=
  "search/d972_r07_760_l3_target6_delta_resume_v4.py";;
D972R4Checker :=
  "crosscheck/check_d972_r07_760_l3_target6_resume_v2.py";;
D972R4Preflight :=
  "search/certs/d972_r07_760_l3_target6_delta_resume_preflight_v4_20260826.json";;
D972R4Artifact :=
  "ci/out/d972_r07_760_l3_target6_delta_resume_v4.json";;
D972R4Log :=
  "ci/out/d972_r07_760_l3_target6_delta_resume_v4_producer.log";;
D972R4Timing :=
  "ci/out/d972_r07_760_l3_target6_delta_resume_v4_timing.txt";;
D972R4Hashes :=
  "ci/out/d972_r07_760_l3_target6_delta_resume_v4_checkpoint_hashes.txt";;
D972R4OK :=
  "ci/out/d972_r07_760_l3_target6_delta_resume_v4.ok";;
D972R4CheckpointDir :=
  "ci/out/d972_r07_760_l3_target6_delta_resume_v4_checkpoints";;
D972R4InnerSeconds := 21000;;
D972R4OuterSeconds := 22500;;

D972R4Pins := [
  [D972R4Producer,
   "08f2237ac6aa438dded775c55627f07ffeff74145765b6e9791a898d594d77ef",88429],
  [D972R4Checker,
   "7cc683ccf16880d3c8794573dfffcbbf0b453cdcf2e7cd2e5665eb78a9e26365",63772],
  [D972R4Preflight,
   "0a715bcedec3283894461444fa3d7f542255a436780327bb95f87d1a411e4fbf",34608],
  ["sol/luna_task_166_r07_target6_delta_checkpoint_v4.md",
   "3d861d83017bd26978553f72dc9654e1bfe62393fa3c94124227a2cc404aa7bd",5816],
  ["sol/luna_reply_165_r07_target6_relator_checkpoint_v3.md",
   "1e446578e1566e8c95578b50826e673111fd2b7df9c5df50098b4758b38c55e9",9628],
  ["search/d972_r07_760_l3_target6_relator_resume_v3.py",
   "0f1ef3bfd341cc5e596b4d84e4122a56b87488dc894dbf58f0561f288ac8a22f",105736],
  ["search/d972_r07_760_l3_target6_relator_resume_gha_driver_v3.g",
   "5784cc29c5dbc24a89867ebb3a275000ffaa698ba2b3c1a6adc4d4b6efdc7870",15861],
  ["search/certs/d972_r07_760_l3_target6_relator_resume_preflight_v3_20260826.json",
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

D972R4Read := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then
    Error("R07 delta resume v4 driver: missing or empty ",label);
  fi;
  return raw;
end;;

D972R4ReadMaybeEmpty := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail then
    Error("R07 delta resume v4 driver: missing ",label);
  fi;
  return raw;
end;;

D972R4Count := function(raw,needle)
  local i,n,m,count;
  if not IsString(raw) or not IsString(needle) or Length(needle)=0 then
    Error("R07 delta resume v4 driver: count input");
  fi;
  n:=Length(raw);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972R4Pin := function(row)
  local raw,got;
  if not IsList(row) or Length(row)<>3 or not IsString(row[1]) or
     not IsString(row[2]) or Length(row[2])<>64 or
     not IsInt(row[3]) or row[3]<=0 then
    Error("R07 delta resume v4 driver: malformed pin");
  fi;
  raw:=D972R4Read(row[1],row[1]);; got:=HexSHA256(raw);;
  if got<>row[2] or Length(raw)<>row[3] then
    Error("R07 delta resume v4 driver: pin drift ",row[1]);
  fi;
  return true;
end;;

D972R4CleanLog := function(raw,label)
  local token;
  for token in ["Traceback (most recent call last):", "SyntaxError",
                "RuntimeError", "Error,", "Reject:", " FAIL ",
                " failed"] do
    if D972R4Count(raw,token)<>0 then
      Error("R07 delta resume v4 driver: forbidden log token ",
            label," ",token);
    fi;
  od;
  return true;
end;;

D972R4ShellQuote := function(path)
  if not IsString(path) or Length(path)=0 or
     PositionSublist(path,"\"")<>fail or
     PositionSublist(path,"\n")<>fail or
     PositionSublist(path,"\r")<>fail then
    Error("R07 delta resume v4 driver: unsafe shell path");
  fi;
  return Concatenation("\"",path,"\"");
end;;

D972R4RemoveOwn := function(paths)
  local path;
  if Length(Set(paths))<>Length(paths) then
    Error("R07 delta resume v4 driver: duplicate cleanup path");
  fi;
  for path in paths do
    if IsExistingFile(path) then RemoveFile(path);; fi;
  od;
  if ForAny(paths,IsExistingFile) then
    Error("R07 delta resume v4 driver: stale own output survived");
  fi;
  return true;
end;;

D972R4DeltaPath := function(j,r)
  local js,rs;
  if not j in [9..12] or not r in [1..11] then
    Error("R07 delta resume v4 driver: delta index");
  fi;
  js:=String(j);; rs:=String(r);;
  if j<10 then js:=Concatenation("0",js);; fi;
  if r<10 then rs:=Concatenation("0",rs);; fi;
  return Concatenation(D972R4CheckpointDir,
    "/d972_r07_760_l3_target6_delta_resume_v4_j",js,
    "_r",rs,".delta.jsonl.gz");
end;;

D972R4JPath := function(j)
  local js;
  if not j in [9..12] then
    Error("R07 delta resume v4 driver: j index");
  fi;
  js:=String(j);;
  if j<10 then js:=Concatenation("0",js);; fi;
  return Concatenation(D972R4CheckpointDir,
    "/d972_r07_760_l3_target6_delta_resume_v4_j",js,
    ".json");
end;;

for D972R4PinRow in D972R4Pins do D972R4Pin(D972R4PinRow);; od;

D972R4Self :=
  IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_SELFTEST) and
  D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_SELFTEST=true;;
D972R4Run :=
  IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RUN) and
  D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RUN=true;;
if D972R4Self=D972R4Run then
  Error("R07 delta resume v4 driver: select exactly one mode");
fi;

D972R4UsePython3 := false;;
if IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_USE_PYTHON3) then
  if not D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_USE_PYTHON3 in
       [true,false] then
    Error("R07 delta resume v4 driver: USE_PYTHON3 boolean");
  fi;
  D972R4UsePython3:=
    D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_USE_PYTHON3;;
fi;
D972R4Python:="python";;
if D972R4UsePython3 then D972R4Python:="python3";; fi;
if D972R4Run and not D972R4UsePython3 then
  Error("R07 delta resume v4 driver: full requires python3");
fi;

D972R4ResumeDelta :=
  IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RESUME_DELTA_J) or
  IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RESUME_DELTA_R);;
D972R4ResumeJ :=
  IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RESUME_J);;
if D972R4ResumeDelta and
   not (IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RESUME_DELTA_J)
        and
        IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RESUME_DELTA_R))
   then
  Error("R07 delta resume v4 driver: incomplete delta resume pair");
fi;
if D972R4ResumeDelta and D972R4ResumeJ then
  Error("R07 delta resume v4 driver: two resume modes");
fi;
D972R4ResumePath:=fail;;
if D972R4ResumeDelta then
  D972R4ResumeDeltaJ:=
    D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RESUME_DELTA_J;;
  D972R4ResumeDeltaR:=
    D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RESUME_DELTA_R;;
  D972R4ResumePath:=D972R4DeltaPath(
    D972R4ResumeDeltaJ,D972R4ResumeDeltaR);;
elif D972R4ResumeJ then
  D972R4ResumeJValue:=
    D972_R07_760_L3_TARGET6_DELTA_RESUME_V4_RESUME_J;;
  D972R4ResumePath:=D972R4JPath(D972R4ResumeJValue);;
fi;

if D972R4Self then
  if D972R4ResumePath<>fail then
    Error("R07 delta resume v4 driver: selftest cannot resume");
  fi;
  D972R4TempDirectory:=DirectoryTemporary();;
  if D972R4TempDirectory=fail then
    Error("R07 delta resume v4 driver: no temporary directory");
  fi;
  D972R4SelfLog:=Filename(D972R4TempDirectory,"selftest.log");;
  D972R4SelfOK:=Filename(D972R4TempDirectory,"selftest.ok");;
  D972R4RemoveOwn([D972R4SelfLog,D972R4SelfOK]);;
  D972R4SelfCommand:=Concatenation(
    D972R4Python," -u -B ",D972R4ShellQuote(D972R4Producer),
    " --self-test > ",D972R4ShellQuote(D972R4SelfLog)," 2>&1 && ",
    "echo D972_R07_DELTA_RESUME_V4_SELFTEST_EXIT_ZERO > ",
    D972R4ShellQuote(D972R4SelfOK));;
  if D972R4Count(D972R4SelfCommand,D972R4Producer)<>1 or
     D972R4Count(D972R4SelfCommand,D972R4Checker)<>0 then
    Error("R07 delta resume v4 driver: selftest command shape");
  fi;
  Exec(D972R4SelfCommand);;
  D972R4SelfRaw:=D972R4Read(D972R4SelfLog,"selftest log");;
  D972R4CleanLog(D972R4SelfRaw,"selftest");;
  if D972R4Count(D972R4Read(D972R4SelfOK,"selftest sentinel"),
       "D972_R07_DELTA_RESUME_V4_SELFTEST_EXIT_ZERO")<>1 or
     D972R4Count(D972R4SelfRaw,
       "R07_760_L3_TARGET6_DELTA_RESUME_V4_PRODUCER_SELFTEST_PASS")<>1 or
     D972R4Count(D972R4SelfRaw,"delta_mutations=12")<>1 or
     D972R4Count(D972R4SelfRaw,"j2_exhaustive=59049")<>1 or
     D972R4Count(D972R4SelfRaw,"append_only=true")<>1 or
     D972R4Count(D972R4SelfRaw,"exact_replay=true")<>1 then
    Error("R07 delta resume v4 driver: selftest markers");
  fi;
  Print("R07_760_L3_TARGET6_DELTA_RESUME_V4_GHA_DRIVER_PASS ",
        "mode=selftest producer_processes=1 checker_processes=0 ",
        "delta_mutations=12 grade=CANDIDATE\n");;
else
  D972R4OwnOutputs:=[D972R4Artifact,D972R4Log,D972R4Timing,
                     D972R4Hashes,D972R4OK];;
  D972R4RemoveOwn(D972R4OwnOutputs);;
  Exec(Concatenation("mkdir -p ",D972R4ShellQuote(D972R4CheckpointDir)));;
  if D972R4ResumePath=fail then
    D972R4CheckpointOutputs:=[];;
    for D972R4J in [9..12] do
      for D972R4R in [1..11] do
        Add(D972R4CheckpointOutputs,D972R4DeltaPath(D972R4J,D972R4R));;
      od;
      Add(D972R4CheckpointOutputs,D972R4JPath(D972R4J));;
    od;
    D972R4RemoveOwn(D972R4CheckpointOutputs);;
    D972R4ResumeArg:="";;
    D972R4ResumeMode:="initial";;
  else
    if not IsExistingFile(D972R4ResumePath) then
      Error("R07 delta resume v4 driver: resume artifact not preseeded");
    fi;
    D972R4ResumeArg:=Concatenation(
      " --resume-checkpoint ",D972R4ShellQuote(D972R4ResumePath));;
    D972R4ResumeMode:="preseeded";;
  fi;
  D972R4FullCommand:=Concatenation(
    "bash -o pipefail -c 'set -e; SECONDS=0; ",
    "timeout --signal=TERM 22500s python3 -u -B ",D972R4Producer,
    " --full --seconds 21000 --checkpoint-dir ",D972R4CheckpointDir,
    " --output ",D972R4Artifact,D972R4ResumeArg,
    " 2>&1 | tee ",D972R4Log,"; producer_elapsed=$SECONDS; ",
    "final_margin=$((22500-SECONDS)); ",
    "if [ $final_margin -le 0 ]; then exit 98; fi; ",
    "find ",D972R4CheckpointDir,
    " -maxdepth 1 -type f -print0 | sort -z | xargs -0 -r sha256sum > ",
    D972R4Hashes,"; ",
    "checkpoint_count=$(wc -l < ",D972R4Hashes,"); ",
    "printf \"producer_elapsed=%s\\nfinal_margin=%s\\n",
    "inner_seconds=21000\\nouter_seconds=22500\\n",
    "producer_processes=1\\nchecker_processes=0\\n",
    "grade=CANDIDATE\\ncheckpoint_count=%s\\nresume_mode=%s\\n\" ",
    "$producer_elapsed $final_margin $checkpoint_count ",D972R4ResumeMode,
    " > ",D972R4Timing,"; ",
    "printf %s D972_R07_DELTA_RESUME_V4_EXIT_ZERO > ",D972R4OK,"'");;
  if D972R4Count(D972R4FullCommand,
       "python3 -u -B search/d972_r07_760_l3_target6_delta_resume_v4.py")<>1 or
     D972R4Count(D972R4FullCommand,"--full")<>1 or
     D972R4Count(D972R4FullCommand,"--seconds 21000")<>1 or
     D972R4Count(D972R4FullCommand,D972R4Checker)<>0 or
     PositionSublist(D972R4FullCommand,"crosscheck/")<>fail then
    Error("R07 delta resume v4 driver: full command shape");
  fi;
  Exec(D972R4FullCommand);;
  if D972R4Read(D972R4OK,"full sentinel")<>
       "D972_R07_DELTA_RESUME_V4_EXIT_ZERO" then
    Error("R07 delta resume v4 driver: producer process");
  fi;
  D972R4Raw:=D972R4Read(D972R4Log,"producer log");;
  D972R4CleanLog(D972R4Raw,"producer");;
  if D972R4Count(D972R4Raw,
       "R07_760_L3_TARGET6_DELTA_RESUME_V4_PRODUCER_PASS")<>1 then
    Error("R07 delta resume v4 driver: producer marker");
  fi;
  D972R4ReceiptRaw:=D972R4Read(D972R4Artifact,"full receipt");;
  D972R4ReceiptSHA:=HexSHA256(D972R4ReceiptRaw);;
  if D972R4Count(D972R4Raw,
       Concatenation(" sha256=",D972R4ReceiptSHA))<>1 or
     D972R4Count(D972R4Raw,
       Concatenation(" bytes=",String(Length(D972R4ReceiptRaw))))<>1 or
     D972R4Count(D972R4ReceiptRaw,"\"grade\":\"CANDIDATE\"")<1 or
     D972R4Count(D972R4ReceiptRaw,
       "\"delta_chain_reconstructs_full_relator_state\":true")<>1 or
     D972R4Count(D972R4ReceiptRaw,
       "\"delta_checkpoint_is_resource_recovery_only\":true")<>1 or
     D972R4Count(D972R4ReceiptRaw,
       "\"inherited_prefix_grade\":\"producer_control_flow_candidate_only\"")<>1 then
    Error("R07 delta resume v4 driver: receipt envelope");
  fi;
  for D972R4Claim in ["actual_A18_occurrence","all_bases_obstruction",
      "compatible_cofinal_lift","ihara_witness",
      "normalized_Brunnian_class"] do
    if D972R4Count(D972R4ReceiptRaw,
         Concatenation("\"",D972R4Claim,"\":false"))<1 then
      Error("R07 delta resume v4 driver: false global claim");
    fi;
  od;
  D972R4TerminalCount:=0;; D972R4Terminal:=fail;;
  for D972R4Token in ["R07_760_L3_TARGET6_NONMEMBER",
      "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE",
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
      "R07_760_L3_TARGET6_INPUT_STOP"] do
    D972R4PCount:=D972R4Count(D972R4Raw,
      Concatenation("terminal=",D972R4Token));;
    D972R4JCount:=D972R4Count(D972R4ReceiptRaw,
      Concatenation("\"terminal_token\":\"",D972R4Token,"\""));;
    if D972R4PCount=1 and D972R4JCount=1 then
      D972R4TerminalCount:=D972R4TerminalCount+1;;
      D972R4Terminal:=D972R4Token;;
    elif D972R4PCount<>0 or D972R4JCount<>0 then
      Error("R07 delta resume v4 driver: terminal mismatch");
    fi;
  od;
  if D972R4TerminalCount<>1 then
    Error("R07 delta resume v4 driver: exclusive terminal");
  fi;
  D972R4HashRaw:=D972R4ReadMaybeEmpty(
    D972R4Hashes,"checkpoint hash ledger");;
  D972R4HashLines:=Filtered(SplitString(D972R4HashRaw,"\n","\r"),
                            line->Length(line)>0);;
  for D972R4HashLine in D972R4HashLines do
    if Length(D972R4HashLine)<68 or D972R4HashLine{[65,66]}<>"  " then
      Error("R07 delta resume v4 driver: hash ledger line");
    fi;
    D972R4CheckpointSHA:=D972R4HashLine{[1..64]};;
    D972R4CheckpointPath:=D972R4HashLine{[67..Length(D972R4HashLine)]};;
    if D972R4Count(D972R4ReceiptRaw,
         Concatenation("\"sha256\":\"",D972R4CheckpointSHA,"\""))<1 or
       D972R4Count(D972R4ReceiptRaw,
         Concatenation("\"path\":\"",D972R4CheckpointPath,"\""))<1 then
      Error("R07 delta resume v4 driver: checkpoint hash binding");
    fi;
  od;
  D972R4TimingRaw:=D972R4Read(D972R4Timing,"timing ledger");;
  if D972R4Count(D972R4TimingRaw,"inner_seconds=21000")<>1 or
     D972R4Count(D972R4TimingRaw,"outer_seconds=22500")<>1 or
     D972R4Count(D972R4TimingRaw,"producer_processes=1")<>1 or
     D972R4Count(D972R4TimingRaw,"checker_processes=0")<>1 or
     D972R4Count(D972R4TimingRaw,
       Concatenation("checkpoint_count=",String(Length(D972R4HashLines))))<>1 then
    Error("R07 delta resume v4 driver: timing ledger");
  fi;
  Print("R07_760_L3_TARGET6_DELTA_RESUME_V4_GHA_DRIVER_PASS mode=full ",
        "terminal=",D972R4Terminal," grade=CANDIDATE cross_checked=false ",
        "producer_processes=1 checker_processes=0 checkpoints=",
        Length(D972R4HashLines)," resume_mode=",D972R4ResumeMode,
        " receipt_sha256=",D972R4ReceiptSHA,
        " receipt_bytes=",Length(D972R4ReceiptRaw),
        " log_sha256=",HexSHA256(D972R4Raw),
        " timing_sha256=",HexSHA256(D972R4TimingRaw),
        " checkpoint_hash_ledger_sha256=",HexSHA256(D972R4HashRaw),"\n");;
fi;
