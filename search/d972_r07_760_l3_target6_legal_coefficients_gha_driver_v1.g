#############################################################################
## R07 g760 L3 target6 legal-coefficient producer/checker driver v1.
## ASCII only.  Producer and helper-nonshared checker run serially.
#############################################################################

D972LC1Producer :=
  "search/d972_r07_760_l3_target6_legal_coefficients_v1.py";;
D972LC1Checker :=
  "crosscheck/check_d972_r07_760_l3_target6_legal_coefficients_v1.py";;
D972LC1Preflight :=
  "search/certs/d972_r07_760_l3_target6_legal_coefficients_preflight_v1_20260827.json";;
D972LC1Artifact :=
  "ci/out/d972_r07_760_l3_target6_legal_coefficients_v1.json";;
D972LC1Verdict :=
  "ci/out/d972_r07_760_l3_target6_legal_coefficients_crosscheck_v1.json";;
D972LC1ProducerLog :=
  "ci/out/d972_r07_760_l3_target6_legal_coefficients_producer_v1.log";;
D972LC1CheckerLog :=
  "ci/out/d972_r07_760_l3_target6_legal_coefficients_checker_v1.log";;
D972LC1Timing :=
  "ci/out/d972_r07_760_l3_target6_legal_coefficients_timing_v1.txt";;
D972LC1Hashes :=
  "ci/out/d972_r07_760_l3_target6_legal_coefficients_hashes_v1.txt";;
D972LC1OK :=
  "ci/out/d972_r07_760_l3_target6_legal_coefficients_v1.ok";;
D972LC1CheckpointDir :=
  "ci/out/d972_r07_760_l3_target6_delta_resume_v5_checkpoints";;
D972LC1InnerSeconds := 18000;;
D972LC1ProducerOuterSeconds := 18600;;
D972LC1CheckerOuterSeconds := 900;;
D972LC1WorkflowSeconds := 21600;;
D972LC1MaxNewRelators := 11;;

D972LC1Pins := [
  [D972LC1Producer,
   "7db4e174dec13e2f69f4011b09abcc52320699261b164b5eedb18a53fa64b962",57792],
  [D972LC1Checker,
   "a54383185601e8251b7cbac87b6c57f89d3a8df8519cb93014b08a3893825e25",49633],
  [D972LC1Preflight,
   "f390f53e6fc840f41009eb31beab519e36b4989b49ac70f9c8f4df7b32776138",6833],
  ["sol/luna_task_168_r07_jennings_legal_coefficients_v1.md",
   "4d85fd8f9ec69a618828c06498aa22922cf5372e21d10ed65280ca2468f5b7f1",7262],
  ["sol/proof_r07_l3_j9_survival_boundary_v105.md",
   "e370efb2d8232f14ac8799c0d7cca6cf7436c79e42240a4afbf70706b3fd0d94",5624],
  ["sol/proof_r07_jennings_legal_coefficient_selector_v106.md",
   "cedde91c7aa013c985581aac63684ba3ab5357e258f550f46d2900efda1a7f77",6628],
  ["search/d972_r07_760_l3_target6_delta_resume_v5.py",
   "94184831ede05c78d7206e62dbdd5c564daa493330fe1c5e433be2804267652b",108142],
  ["search/d972_r07_760_l3_target6_delta_resume_gha_driver_v5.g",
   "ff820866983c1d1bc5d0a98bb748d4a7fda4e406b3283e6c6a6ccf817011be20",29496],
  ["search/certs/d972_r07_760_l3_target6_delta_resume_preflight_v5_20260827.json",
   "76da0c9f78f3efff305289bb864e25819a722c2362dc2dffb250c98be9244305",36718],
  ["sol/luna_task_167_r07_target6_postclosure_recovery_v5.md",
   "3b885303f4bf512fc7a9a8e3f124f87a91ca4f3c7728920ee420d781dbe23e8c",7170],
  ["sol/luna_reply_167_r07_target6_postclosure_recovery_v5.md",
   "6412ceb1f9e415fc863a46eb9de30314157a73c20bb8374e3c3d9a16e1c10475",11832]
];;

D972LC1Terminals := [
  "R07_760_L3_TARGET6_NONMEMBER",
  "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE",
  "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
  "R07_760_L3_TARGET6_INPUT_STOP"
];;

D972LC1Read := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then
    Error("R07 legal coefficients v1 driver: missing or empty ",label);
  fi;
  return raw;
end;;

D972LC1Count := function(raw,needle)
  local i,n,m,count;
  if not IsString(raw) or not IsString(needle) or Length(needle)=0 then
    Error("R07 legal coefficients v1 driver: count input");
  fi;
  n:=Length(raw);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972LC1ReplaceFirst := function(raw,old,new)
  local at,before,after;
  at:=PositionSublist(raw,old);;
  if at=fail then
    Error("R07 legal coefficients v1 driver: mutation needle");
  fi;
  before:="";; after:="";;
  if at>1 then before:=raw{[1..at-1]};; fi;
  if at+Length(old)<=Length(raw) then
    after:=raw{[at+Length(old)..Length(raw)]};;
  fi;
  return Concatenation(before,new,after);
end;;

D972LC1Pin := function(row)
  local raw;
  if not IsList(row) or Length(row)<>3 or
     not IsString(row[1]) or not IsString(row[2]) or
     Length(row[2])<>64 or not IsInt(row[3]) or row[3]<=0 then
    Error("R07 legal coefficients v1 driver: malformed pin");
  fi;
  raw:=D972LC1Read(row[1],row[1]);;
  if Length(raw)<>row[3] or HexSHA256(raw)<>row[2] then
    Error("R07 legal coefficients v1 driver: pin drift ",row[1]);
  fi;
  return true;
end;;

D972LC1ShellQuote := function(path)
  if not IsString(path) or Length(path)=0 or
     PositionSublist(path,"\"")<>fail or
     PositionSublist(path,"\n")<>fail or
     PositionSublist(path,"\r")<>fail then
    Error("R07 legal coefficients v1 driver: unsafe shell path");
  fi;
  return Concatenation("\"",path,"\"");
end;;

D972LC1CleanLog := function(raw,label)
  local token;
  for token in ["Traceback (most recent call last):", "SyntaxError",
                "RuntimeError", "Error,", "Reject:", " FAIL ",
                " failed"] do
    if D972LC1Count(raw,token)<>0 then
      Error("R07 legal coefficients v1 driver: forbidden log token ",
            label," ",token);
    fi;
  od;
  return true;
end;;

D972LC1RemoveOwn := function(paths)
  local path;
  if Length(Set(paths))<>Length(paths) then
    Error("R07 legal coefficients v1 driver: duplicate cleanup path");
  fi;
  for path in paths do
    if IsExistingFile(path) then RemoveFile(path);; fi;
  od;
  if ForAny(paths,IsExistingFile) then
    Error("R07 legal coefficients v1 driver: stale own output");
  fi;
  return true;
end;;

D972LC1DeltaPath := function(j,r)
  local js,rs;
  if not j in [9..12] or not r in [1..11] then
    Error("R07 legal coefficients v1 driver: delta index");
  fi;
  js:=String(j);; rs:=String(r);;
  if j<10 then js:=Concatenation("0",js);; fi;
  if r<10 then rs:=Concatenation("0",rs);; fi;
  return Concatenation(D972LC1CheckpointDir,
    "/d972_r07_760_l3_target6_delta_resume_v5_j",js,
    "_r",rs,".delta.jsonl.gz");
end;;

D972LC1JPath := function(j)
  local js;
  if not j in [9..12] then
    Error("R07 legal coefficients v1 driver: j index");
  fi;
  js:=String(j);;
  if j<10 then js:=Concatenation("0",js);; fi;
  return Concatenation(D972LC1CheckpointDir,
    "/d972_r07_760_l3_target6_delta_resume_v5_j",js,".json");
end;;

D972LC1AuditPreflight := function(raw)
  return D972LC1Count(raw,
    "\"schema\":\"d972-r07-760-l3-target6-legal-coefficients/v1\"")=1 and
    D972LC1Count(raw,"\"mode\":\"preflight\"")=1 and
    D972LC1Count(raw,"\"grade\":\"CANDIDATE\"")=1 and
    D972LC1Count(raw,"\"mutation_tests_rejected\":11")=1 and
    D972LC1Count(raw,"\"random_exhaustive_cases\":90")=1 and
    D972LC1Count(raw,"\"full_j9_run_locally\":false")=1 and
    D972LC1Count(raw,"\"full_translated_D2_closure_run\":false")=1 and
    D972LC1Count(raw,
      "\"actual_common_word_domain_intersection_computed\":false")=2 and
    D972LC1Count(raw,"\"literal_A18_replayed\":false")=2 and
    D972LC1Count(raw,
      "\"two_hexagons_replayed_as_joint_system\":false")=2 and
    D972LC1Count(raw,"\"cofinal_compatibility_proved\":false")=2 and
    D972LC1Count(raw,"\"actual_A18_lift\":false")=1 and
    D972LC1Count(raw,"\"fake\":false")=1 and
    D972LC1Count(raw,"\"cofinal_lift\":false")=1 and
    D972LC1Count(raw,"\"Ihara_witness\":false")=1;
end;;

D972LC1DriverFixtureSelftest := function()
  local raw,bad,rejected;
  raw:=D972LC1Read(D972LC1Preflight,"preflight");;
  if not D972LC1AuditPreflight(raw) then
    Error("R07 legal coefficients v1 driver: valid preflight");
  fi;
  rejected:=0;;
  bad:=D972LC1ReplaceFirst(raw,"\"fake\":false","\"fake\":true");;
  if not D972LC1AuditPreflight(bad) then rejected:=rejected+1;; fi;
  bad:=D972LC1ReplaceFirst(raw,"\"actual_A18_lift\":false",
                               "\"actual_A18_lift\":true");;
  if not D972LC1AuditPreflight(bad) then rejected:=rejected+1;; fi;
  bad:=D972LC1ReplaceFirst(raw,
    "\"actual_common_word_domain_intersection_computed\":false",
    "\"actual_common_word_domain_intersection_computed\":true");;
  if not D972LC1AuditPreflight(bad) then rejected:=rejected+1;; fi;
  bad:=D972LC1ReplaceFirst(raw,"\"literal_A18_replayed\":false",
                               "\"literal_A18_replayed\":true");;
  if not D972LC1AuditPreflight(bad) then rejected:=rejected+1;; fi;
  bad:=D972LC1ReplaceFirst(raw,"\"mutation_tests_rejected\":11",
                               "\"mutation_tests_rejected\":10");;
  if not D972LC1AuditPreflight(bad) then rejected:=rejected+1;; fi;
  bad:=D972LC1ReplaceFirst(raw,"\"grade\":\"CANDIDATE\"",
                               "\"grade\":\"VERIFIED\"");;
  if not D972LC1AuditPreflight(bad) then rejected:=rejected+1;; fi;
  if rejected<>6 then
    Error("R07 legal coefficients v1 driver: fixture mutations ",rejected);
  fi;
  return rejected;
end;;

for D972LC1PinRow in D972LC1Pins do D972LC1Pin(D972LC1PinRow);; od;

D972LC1Self :=
  IsBound(D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_SELFTEST) and
  D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_SELFTEST=true;;
D972LC1Run :=
  IsBound(D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_RUN) and
  D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_RUN=true;;
if D972LC1Self=D972LC1Run then
  Error("R07 legal coefficients v1 driver: select exactly one mode");
fi;

D972LC1UsePython3 := false;;
if IsBound(D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_USE_PYTHON3) then
  if not D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_USE_PYTHON3 in
       [true,false] then
    Error("R07 legal coefficients v1 driver: USE_PYTHON3 boolean");
  fi;
  D972LC1UsePython3:=
    D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_USE_PYTHON3;;
fi;
D972LC1Python:="python";;
if D972LC1UsePython3 then D972LC1Python:="python3";; fi;
if D972LC1Run and not D972LC1UsePython3 then
  Error("R07 legal coefficients v1 driver: full requires python3");
fi;

D972LC1ResumeDelta :=
  IsBound(D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_RESUME_DELTA_J) or
  IsBound(D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_RESUME_DELTA_R);;
D972LC1ResumeJ :=
  IsBound(D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_RESUME_J);;
if D972LC1ResumeDelta and not (
   IsBound(D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_RESUME_DELTA_J) and
   IsBound(D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_RESUME_DELTA_R)) then
  Error("R07 legal coefficients v1 driver: incomplete delta resume pair");
fi;
if D972LC1ResumeDelta and D972LC1ResumeJ then
  Error("R07 legal coefficients v1 driver: two resume modes");
fi;
D972LC1ResumePath:=fail;;
if D972LC1ResumeDelta then
  D972LC1ResumePath:=D972LC1DeltaPath(
    D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_RESUME_DELTA_J,
    D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_RESUME_DELTA_R);;
elif D972LC1ResumeJ then
  D972LC1ResumePath:=D972LC1JPath(
    D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_RESUME_J);;
fi;

if D972LC1Self then
  if D972LC1ResumePath<>fail then
    Error("R07 legal coefficients v1 driver: selftest cannot resume");
  fi;
  D972LC1Tmp:=DirectoryTemporary();;
  if D972LC1Tmp=fail then
    Error("R07 legal coefficients v1 driver: no temporary directory");
  fi;
  D972LC1SelfLog:=Filename(D972LC1Tmp,"selftest.log");;
  D972LC1SelfOK:=Filename(D972LC1Tmp,"selftest.ok");;
  D972LC1RemoveOwn([D972LC1SelfLog,D972LC1SelfOK]);;
  D972LC1FixtureMutations:=D972LC1DriverFixtureSelftest();;
  D972LC1SelfCommand:=Concatenation(
    D972LC1Python," -u -B ",D972LC1ShellQuote(D972LC1Producer),
    " --self-test > ",D972LC1ShellQuote(D972LC1SelfLog)," 2>&1 && ",
    D972LC1Python," -u -B ",D972LC1ShellQuote(D972LC1Checker),
    " --self-test >> ",D972LC1ShellQuote(D972LC1SelfLog)," 2>&1 && ",
    "echo D972_R07_LEGAL_COEFFICIENTS_V1_SELFTEST_EXIT_ZERO > ",
    D972LC1ShellQuote(D972LC1SelfOK));;
  if D972LC1Count(D972LC1SelfCommand,D972LC1Producer)<>1 or
     D972LC1Count(D972LC1SelfCommand,D972LC1Checker)<>1 then
    Error("R07 legal coefficients v1 driver: selftest command shape");
  fi;
  Exec(D972LC1SelfCommand);;
  D972LC1SelfRaw:=D972LC1Read(D972LC1SelfLog,"selftest log");;
  D972LC1CleanLog(D972LC1SelfRaw,"selftest");;
  if D972LC1Count(D972LC1Read(D972LC1SelfOK,"selftest sentinel"),
       "D972_R07_LEGAL_COEFFICIENTS_V1_SELFTEST_EXIT_ZERO")<>1 or
     D972LC1Count(D972LC1SelfRaw,
       "R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_PRODUCER_SELFTEST_PASS")<>1 or
     D972LC1Count(D972LC1SelfRaw,
       "R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_CHECKER_SELFTEST_PASS")<>1 or
     D972LC1Count(D972LC1SelfRaw,"random_exhaustive=90")<>1 or
     D972LC1Count(D972LC1SelfRaw,"random_exhaustive=70")<>1 or
     D972LC1Count(D972LC1SelfRaw,"mutations=11")<>2 or
     D972LC1Count(D972LC1SelfRaw,"synthetic_full_certificates=1")<>1 or
     D972LC1Count(D972LC1SelfRaw,"full_j9_local=false")<>1 or
     D972LC1Count(D972LC1SelfRaw,"full_D2_local=false")<>1 then
    Error("R07 legal coefficients v1 driver: selftest markers");
  fi;
  Print("R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_GHA_DRIVER_PASS ",
        "mode=selftest producer_processes=1 checker_processes=1 ",
        "driver_fixture_mutations=",D972LC1FixtureMutations,
        " grade=CANDIDATE helper_shared=false\n");;
else
  D972LC1OwnOutputs:=[D972LC1Artifact,D972LC1Verdict,
    D972LC1ProducerLog,D972LC1CheckerLog,D972LC1Timing,
    D972LC1Hashes,D972LC1OK];;
  for D972LC1J in [9..12] do
    D972LC1JS:=String(D972LC1J);;
    if D972LC1J<10 then
      D972LC1JS:=Concatenation("0",D972LC1JS);;
    fi;
    Add(D972LC1OwnOutputs,Concatenation(
      "ci/out/d972_r07_760_l3_target6_legal_coefficients_v1_j",
      D972LC1JS,".json"));;
  od;
  D972LC1RemoveOwn(D972LC1OwnOutputs);;
  Exec(Concatenation("mkdir -p ",
       D972LC1ShellQuote(D972LC1CheckpointDir)));;
  if D972LC1ResumePath=fail then
    D972LC1CheckpointOutputs:=[];;
    for D972LC1J in [9..12] do
      for D972LC1R in [1..11] do
        Add(D972LC1CheckpointOutputs,
            D972LC1DeltaPath(D972LC1J,D972LC1R));;
      od;
      Add(D972LC1CheckpointOutputs,D972LC1JPath(D972LC1J));;
    od;
    D972LC1RemoveOwn(D972LC1CheckpointOutputs);;
    D972LC1ResumeArg:="";; D972LC1ResumeMode:="initial";;
  else
    if not IsExistingFile(D972LC1ResumePath) then
      Error("R07 legal coefficients v1 driver: resume artifact absent");
    fi;
    D972LC1ResumeArg:=Concatenation(
      " --resume-checkpoint ",D972LC1ShellQuote(D972LC1ResumePath));;
    D972LC1ResumeMode:="preseeded";;
  fi;
  D972LC1FullCommand:=Concatenation(
    "bash -o pipefail -c 'set -e; SECONDS=0; ",
    "timeout --signal=TERM 18600s python3 -u -B ",D972LC1Producer,
    " --full --seconds 18000 --max-new-relators 11 --checkpoint-dir ",
    D972LC1CheckpointDir," --coefficient-dir ci/out --output ",
    D972LC1Artifact,D972LC1ResumeArg," 2>&1 | tee ",
    D972LC1ProducerLog,"; producer_elapsed=$SECONDS; ",
    "timeout --signal=TERM 900s python3 -u -B ",D972LC1Checker,
    " --check --receipt ",D972LC1Artifact," --checkpoint-dir ",
    D972LC1CheckpointDir," --output ",D972LC1Verdict,
    " 2>&1 | tee ",D972LC1CheckerLog,
    "; checker_elapsed=$((SECONDS-producer_elapsed)); ",
    "workflow_margin=$((21600-SECONDS)); ",
    "if [ $workflow_margin -lt 1800 ]; then exit 98; fi; ",
    "find ci/out -maxdepth 2 -type f -print0 | sort -z | ",
    "xargs -0 -r sha256sum > ",D972LC1Hashes,"; ",
    "printf \"producer_elapsed=%s\\nchecker_elapsed=%s\\n",
    "workflow_margin=%s\\ninner_seconds=18000\\n",
    "producer_outer_seconds=18600\\nchecker_outer_seconds=900\\n",
    "workflow_seconds=21600\\nproducer_processes=1\\n",
    "checker_processes=1\\nmax_new_relators=11\\nresume_mode=%s\\n\" ",
    "$producer_elapsed $checker_elapsed $workflow_margin ",
    D972LC1ResumeMode," > ",D972LC1Timing,"; ",
    "printf %s D972_R07_LEGAL_COEFFICIENTS_V1_EXIT_ZERO > ",
    D972LC1OK,"'");;
  if D972LC1Count(D972LC1FullCommand,
       Concatenation("python3 -u -B ",D972LC1Producer))<>1 or
     D972LC1Count(D972LC1FullCommand,
       Concatenation("python3 -u -B ",D972LC1Checker))<>1 or
     D972LC1Count(D972LC1FullCommand,"--max-new-relators 11")<>1 or
     D972LC1Count(D972LC1FullCommand,"--check")<>1 then
    Error("R07 legal coefficients v1 driver: full command shape");
  fi;
  Exec(D972LC1FullCommand);;
  if D972LC1Read(D972LC1OK,"full sentinel")<>
       "D972_R07_LEGAL_COEFFICIENTS_V1_EXIT_ZERO" then
    Error("R07 legal coefficients v1 driver: process failure");
  fi;
  D972LC1ProducerRaw:=D972LC1Read(
    D972LC1ProducerLog,"producer log");;
  D972LC1CheckerRaw:=D972LC1Read(
    D972LC1CheckerLog,"checker log");;
  D972LC1CleanLog(D972LC1ProducerRaw,"producer");;
  D972LC1CleanLog(D972LC1CheckerRaw,"checker");;
  if D972LC1Count(D972LC1ProducerRaw,
       "R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_PRODUCER_PASS")<>1 or
     D972LC1Count(D972LC1CheckerRaw,
       "R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_CHECKER_PASS")<>1 then
    Error("R07 legal coefficients v1 driver: process markers");
  fi;
  D972LC1ReceiptRaw:=D972LC1Read(D972LC1Artifact,"producer receipt");;
  D972LC1VerdictRaw:=D972LC1Read(D972LC1Verdict,"checker verdict");;
  D972LC1TerminalCount:=0;; D972LC1Terminal:=fail;;
  for D972LC1Token in D972LC1Terminals do
    if D972LC1Count(D972LC1ProducerRaw,
         Concatenation("terminal=",D972LC1Token))=1 and
       D972LC1Count(D972LC1CheckerRaw,
         Concatenation("terminal=",D972LC1Token))=1 and
       D972LC1Count(D972LC1ReceiptRaw,
         Concatenation("\"terminal_token\":\"",D972LC1Token,"\""))>=1 and
       D972LC1Count(D972LC1VerdictRaw,
         Concatenation("\"terminal_token\":\"",D972LC1Token,"\""))=1 then
      D972LC1TerminalCount:=D972LC1TerminalCount+1;;
      D972LC1Terminal:=D972LC1Token;;
    fi;
  od;
  if D972LC1TerminalCount<>1 or
     D972LC1Count(D972LC1ReceiptRaw,
       "\"actual_common_word_domain_intersection_computed\":false")<2 or
     D972LC1Count(D972LC1ReceiptRaw,
       "\"cofinal_compatibility_proved\":false")<2 or
     D972LC1Count(D972LC1VerdictRaw,
       "\"direct_full_D2_checker_completed\":false")<>1 then
    Error("R07 legal coefficients v1 driver: terminal/boundary audit");
  fi;
  D972LC1TimingRaw:=D972LC1Read(D972LC1Timing,"timing");;
  if D972LC1Count(D972LC1TimingRaw,"inner_seconds=18000")<>1 or
     D972LC1Count(D972LC1TimingRaw,"producer_outer_seconds=18600")<>1 or
     D972LC1Count(D972LC1TimingRaw,"checker_outer_seconds=900")<>1 or
     D972LC1Count(D972LC1TimingRaw,"workflow_seconds=21600")<>1 or
     D972LC1Count(D972LC1TimingRaw,"producer_processes=1")<>1 or
     D972LC1Count(D972LC1TimingRaw,"checker_processes=1")<>1 or
     D972LC1Count(D972LC1TimingRaw,"max_new_relators=11")<>1 then
    Error("R07 legal coefficients v1 driver: timing audit");
  fi;
  Print("R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_GHA_DRIVER_PASS ",
        "mode=full terminal=",D972LC1Terminal,
        " grade=CROSS_CHECKED producer_processes=1 checker_processes=1 ",
        "conditional_on_authenticated_v5_D2=true direct_full_D2=false ",
        "receipt_sha256=",HexSHA256(D972LC1ReceiptRaw),
        " verdict_sha256=",HexSHA256(D972LC1VerdictRaw),
        " timing_sha256=",HexSHA256(D972LC1TimingRaw),"\n");;
fi;
