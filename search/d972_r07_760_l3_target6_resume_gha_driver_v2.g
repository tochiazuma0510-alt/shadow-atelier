#############################################################################
## R07 g760 L3 target6 checkpoint/resume producer-only GHA driver v2.
## ASCII only.  Full mode runs exactly one Python producer and no checker.
#############################################################################

D972R2Producer := "search/d972_r07_760_l3_target6_resume_v2.py";;
D972R2Checker :=
  "crosscheck/check_d972_r07_760_l3_target6_resume_v2.py";;
D972R2Preflight :=
  "search/certs/d972_r07_760_l3_target6_resume_preflight_v2_20260826.json";;
D972R2PriorReceipt :=
  "search/certs/d972_r07_760_l3_target6_prior_run32901384400_v1_20260826.json";;
D972R2PriorLog :=
  "search/certs/d972_r07_760_l3_target6_prior_run32901384400_producer_v1_20260826.log";;
D972R2Artifact := "ci/out/d972_r07_760_l3_target6_resume_v2.json";;
D972R2Log := "ci/out/d972_r07_760_l3_target6_resume_v2_producer.log";;
D972R2Timing := "ci/out/d972_r07_760_l3_target6_resume_v2_timing.txt";;
D972R2OK := "ci/out/d972_r07_760_l3_target6_resume_v2.ok";;
D972R2CheckpointDir :=
  "ci/out/d972_r07_760_l3_target6_resume_v2_checkpoints";;
D972R2InnerSeconds := 21000;;
D972R2OuterSeconds := 21600;;
D972R2Dialogue := Concatenation("docs/",
  List([229,175,190,232,169,177,229,184,179],CharInt),".md");;

# The v2 producer-only lane authenticates the checker as packaging, but never
# executes or imports it.  The remaining rows are the clean v1 dependency
# boundary inherited by the frozen producer core.
D972R2Pins := [
  [D972R2Producer,
   "9f6f8c2d3d3dbbc69373e1413b5d47a8893d6be62b228dc04ecd522a4fa51238",35068],
  [D972R2Checker,
   "7cc683ccf16880d3c8794573dfffcbbf0b453cdcf2e7cd2e5665eb78a9e26365",63772],
  [D972R2Preflight,
   "272d4c4e91bb0234d49316277b354b722dfcb1366e47e9bf00d745469a1c1a94",7986],
  [D972R2PriorReceipt,
   "1c739559eee368ba676c694960be21db94d6bc2292a6136d89b97bedfef3e15b",3239],
  [D972R2PriorLog,
   "fc3901c29f958e216e17ba175be4857ee26cc140f3f809f0e29833b636ccd436",164],
  ["sol/luna_task_164_r07_760_l3_target6_resume_v2.md",
   "761359bda0fc14543ab9266ec61139006403525d828811bb2af5d27d34ccfc9d",5292],
  ["search/d972_r07_760_l3_target6_v1.py",
   "7048e73a02e76df5d49fd359c52d5be70ae99d70aa95ebe74b28c4a18f130fde",53284],
  ["search/certs/d972_r07_760_l3_target6_preflight_v1_20260826.json",
   "4d305a1af415ffb5acf1d029a69c1b720961fce88dc86575d8fde2d504a787ab",663780],
  ["sol/luna_task_163_r07_760_l3_target6_v1.md",
   "9fcdf2f25b724e9dbc225f417b0036e126e7b5e37a0778dab5e0299ee2f74e12",9066],
  ["provenance/CLAIMS.md",
   "174ddbb50d1579c9373482552759ed2ec822846f1dd83c8d73b13c652ae77f64",66635],
  [D972R2Dialogue,
   "a5eadcc04468b593e0a1c7896409a59b55c6442ca489df6a91aac60d6e128a06",234377],
  ["sol/proof_r07_joint_derived_commutator_rebase_v92.md",
   "cc56e2187fac08ffa70fe3753e200627e776b5fa591738dee5da908e4d217387",5969],
  ["sol/audit_r07_uniform_explicit_lift_checkpoint_v95.md",
   "12877306446bcfe8b57b01751c929bdee78d15300c4f90a8311764ff2d7eeeae",5324],
  ["sol/luna_task_162_r07_760_commutator_affine_rhs_v3.md",
   "8ca38afc6f30e8e6074f191a17541f508f29ba1da58d3b286ba4fcf33406ae21",4053],
  ["sol/luna_reply_162_r07_760_commutator_affine_rhs_v3.md",
   "70ebb7bf433fafd77dc828efe5f71b9dd6dc982e7682a4c6397695b6a2e6bcf5",8833],
  ["search/certs/d972_r07_616_to_760_commutator_affine_rhs_preflight_v3_20260826.json",
   "55752b6c1a748fb0b25a86d6fc1a0381a82b203112568b0b1963c5665cef0408",184890],
  ["ci/b345_157en_artifacts_32458556448/d972_b345_q3_chief_v1.json",
   "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72",231570],
  ["search/d972_b345_seedspan_triple4_v1.py",
   "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29",535219]
];;

D972R2Read := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then
    Error("R07 resume v2 driver: missing or empty ",label);
  fi;
  return raw;
end;;

D972R2Count := function(raw,needle)
  local i,n,m,count;
  if not IsString(raw) or not IsString(needle) or Length(needle)=0 then
    Error("R07 resume v2 driver: count input");
  fi;
  n:=Length(raw);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972R2Pin := function(row)
  local raw,got;
  if not IsList(row) or Length(row)<>3 or not IsString(row[1]) or
     not IsString(row[2]) or Length(row[2])<>64 or
     not IsInt(row[3]) or row[3]<=0 then
    Error("R07 resume v2 driver: malformed pin");
  fi;
  raw:=D972R2Read(row[1],row[1]);; got:=HexSHA256(raw);;
  if got<>row[2] or Length(raw)<>row[3] then
    Error("R07 resume v2 driver: pin drift ",row[1]," sha=",got,
          " bytes=",Length(raw));
  fi;
  return true;
end;;

D972R2CleanLog := function(raw,label)
  local token;
  for token in ["Traceback (most recent call last):", "SyntaxError",
                "RuntimeError", "Error,", "Reject:", " FAIL ",
                " failed"] do
    if D972R2Count(raw,token)<>0 then
      Error("R07 resume v2 driver: forbidden log token ",label," ",token);
    fi;
  od;
  return true;
end;;

D972R2ShellQuote := function(path)
  if not IsString(path) or Length(path)=0 or
     PositionSublist(path,"\"")<>fail or
     PositionSublist(path,"\n")<>fail or
     PositionSublist(path,"\r")<>fail then
    Error("R07 resume v2 driver: unsafe shell path");
  fi;
  return Concatenation("\"",path,"\"");
end;;

D972R2RemoveOwn := function(paths)
  local path;
  if Length(Set(paths))<>Length(paths) then
    Error("R07 resume v2 driver: duplicate cleanup path");
  fi;
  for path in paths do
    if IsExistingFile(path) then RemoveFile(path);; fi;
  od;
  if ForAny(paths,IsExistingFile) then
    Error("R07 resume v2 driver: stale own output survived cleanup");
  fi;
  return true;
end;;

D972R2CheckpointPath := function(j)
  if not j in [9..12] then Error("R07 resume v2 driver: checkpoint j"); fi;
  return Concatenation(D972R2CheckpointDir,
    "/d972_r07_760_l3_target6_resume_v2_j",String(j),".json");
end;;

for D972R2PinRow in D972R2Pins do D972R2Pin(D972R2PinRow);; od;

D972R2Self :=
  IsBound(D972_R07_760_L3_TARGET6_RESUME_V2_SELFTEST) and
  D972_R07_760_L3_TARGET6_RESUME_V2_SELFTEST=true;;
D972R2Run :=
  IsBound(D972_R07_760_L3_TARGET6_RESUME_V2_RUN) and
  D972_R07_760_L3_TARGET6_RESUME_V2_RUN=true;;
if D972R2Self=D972R2Run then
  Error("R07 resume v2 driver: select exactly one mode");
fi;

if IsBound(D972_R07_760_L3_TARGET6_RESUME_V2_PYTHON) then
  Error("R07 resume v2 driver: obsolete string Python binding forbidden");
fi;
D972R2UsePython3 := false;;
if IsBound(D972_R07_760_L3_TARGET6_RESUME_V2_USE_PYTHON3) then
  if not D972_R07_760_L3_TARGET6_RESUME_V2_USE_PYTHON3 in [true,false] then
    Error("R07 resume v2 driver: USE_PYTHON3 must be boolean");
  fi;
  D972R2UsePython3:=
    D972_R07_760_L3_TARGET6_RESUME_V2_USE_PYTHON3;;
fi;
D972R2Python := "python";;
if D972R2UsePython3 then D972R2Python:="python3";; fi;
if D972R2Run and not D972R2UsePython3 then
  Error("R07 resume v2 driver: full requires USE_PYTHON3=true");
fi;

if D972R2Self then
  D972R2TempDirectory:=DirectoryTemporary();;
  if D972R2TempDirectory=fail then
    Error("R07 resume v2 driver: no external temporary directory");
  fi;
  D972R2TempRoot:=Filename(D972R2TempDirectory,"");;
  D972R2SelfLog:=Filename(D972R2TempDirectory,"selftest.log");;
  D972R2SelfOK:=Filename(D972R2TempDirectory,"selftest.ok");;
  D972R2RepoRoot:=Filename(DirectoryCurrent(),"");;
  if Length(Set([D972R2SelfLog,D972R2SelfOK]))<>2 or
     ForAny([D972R2SelfLog,D972R2SelfOK],x->
       PositionSublist(x,D972R2TempRoot)<>1 or
       PositionSublist(x,D972R2RepoRoot)=1) then
    Error("R07 resume v2 driver: selftest path boundary");
  fi;
  D972R2RemoveOwn([D972R2SelfLog,D972R2SelfOK]);;
  D972R2SelfCommand:=Concatenation(
    D972R2Python," -u -B ",D972R2ShellQuote(D972R2Producer),
    " --self-test > ",D972R2ShellQuote(D972R2SelfLog)," 2>&1 && ",
    "echo D972_R07_760_L3_TARGET6_RESUME_V2_SELFTEST_EXIT_ZERO > ",
    D972R2ShellQuote(D972R2SelfOK));;
  if D972R2Count(D972R2SelfCommand,D972R2Producer)<>1 or
     D972R2Count(D972R2SelfCommand,D972R2Checker)<>0 or
     D972R2Count(D972R2SelfCommand," -u -B ")<>1 then
    Error("R07 resume v2 driver: selftest command shape");
  fi;
  Exec(D972R2SelfCommand);;
  D972R2SelfRaw:=D972R2Read(D972R2SelfLog,"selftest log");;
  D972R2CleanLog(D972R2SelfRaw,"selftest");;
  if D972R2Count(D972R2Read(D972R2SelfOK,"selftest sentinel"),
       "D972_R07_760_L3_TARGET6_RESUME_V2_SELFTEST_EXIT_ZERO")<>1 or
     D972R2Count(D972R2SelfRaw,
       "R07_760_L3_TARGET6_RESUME_V2_PRODUCER_SELFTEST_PASS")<>1 or
     D972R2Count(D972R2SelfRaw,"checkpoint_mutations=6")<>1 or
     D972R2Count(D972R2SelfRaw,"relator_state=absent")<>1 then
    Error("R07 resume v2 driver: selftest markers");
  fi;
  Print("R07_760_L3_TARGET6_RESUME_V2_GHA_DRIVER_PASS ",
        "mode=selftest producer_processes=1 checker_processes=0 ",
        "checkpoint_mutations=6 grade=CANDIDATE\n");;
else
  D972R2OwnOutputs:=[D972R2Artifact,D972R2Log,D972R2Timing,D972R2OK];;
  for D972R2J in [9..12] do
    Add(D972R2OwnOutputs,D972R2CheckpointPath(D972R2J));;
  od;
  D972R2RemoveOwn(D972R2OwnOutputs);;
  D972R2FullCommand:=Concatenation(
    "mkdir -p '",D972R2CheckpointDir,"' && bash -o pipefail -c '",
    "set -e; SECONDS=0; timeout --signal=TERM 21600s ",
    "python3 -u -B search/d972_r07_760_l3_target6_resume_v2.py ",
    "--full --start-j 9 --seconds 21000 --checkpoint-dir ",
    D972R2CheckpointDir," --output ",D972R2Artifact," ",
    "2>&1 | tee ",D972R2Log,"; producer_elapsed=$SECONDS; ",
    "final_margin=$((21600-SECONDS)); ",
    "if [ $final_margin -le 0 ]; then exit 98; fi; ",
    "checkpoint_count=$(find ",D972R2CheckpointDir,
    " -maxdepth 1 -type f -name '\''d972_r07_760_l3_target6_resume_v2_j*.json'\'' | wc -l); ",
    "printf \"producer_elapsed=%s\\nfinal_margin=%s\\n",
    "inner_seconds=21000\\nouter_seconds=21600\\n",
    "producer_processes=1\\nchecker_processes=0\\n",
    "grade=CANDIDATE\\ncheckpoint_count=%s\\n\" ",
    "$producer_elapsed $final_margin $checkpoint_count > ",D972R2Timing,"; ",
    "printf %s D972_R07_760_L3_TARGET6_RESUME_V2_EXIT_ZERO > ",
    D972R2OK,"'");;
  if D972R2Count(D972R2FullCommand,
       "python3 -u -B search/d972_r07_760_l3_target6_resume_v2.py")<>1 or
     D972R2Count(D972R2FullCommand,"--full")<>1 or
     D972R2Count(D972R2FullCommand,"--start-j 9")<>1 or
     D972R2Count(D972R2FullCommand,"--seconds 21000")<>1 or
     D972R2Count(D972R2FullCommand,D972R2Checker)<>0 or
     PositionSublist(D972R2FullCommand,"crosscheck/")<>fail then
    Error("R07 resume v2 driver: full command shape");
  fi;
  Exec(D972R2FullCommand);;
  if D972R2Read(D972R2OK,"full sentinel")<>
       "D972_R07_760_L3_TARGET6_RESUME_V2_EXIT_ZERO" then
    Error("R07 resume v2 driver: producer process");
  fi;
  D972R2Raw:=D972R2Read(D972R2Log,"producer log");;
  D972R2CleanLog(D972R2Raw,"producer");;
  if D972R2Count(D972R2Raw,
       "R07_760_L3_TARGET6_RESUME_V2_PRODUCER_PASS")<>1 then
    Error("R07 resume v2 driver: producer marker");
  fi;
  D972R2ReceiptRaw:=D972R2Read(D972R2Artifact,"full receipt");;
  D972R2ReceiptSHA:=HexSHA256(D972R2ReceiptRaw);;
  if D972R2Count(D972R2Raw,
       Concatenation(" sha256=",D972R2ReceiptSHA))<>1 or
     D972R2Count(D972R2Raw,
       Concatenation(" bytes=",String(Length(D972R2ReceiptRaw))))<>1 or
     D972R2Count(D972R2ReceiptRaw,"\"grade\":\"CANDIDATE\"")<2 or
     D972R2Count(D972R2ReceiptRaw,
       "\"inherited_candidate_prefix\":[2,3,4,5,6,7,8]")<2 or
     D972R2Count(D972R2ReceiptRaw,
       "\"inherited_prefix_grade\":\"producer_control_flow_candidate_only\"")<2 or
     D972R2Count(D972R2ReceiptRaw,"\"start_j\":9")<2 or
     D972R2Count(D972R2ReceiptRaw,
       "\"unfinished_j_inferred\":false")<>1 or
     D972R2Count(D972R2ReceiptRaw,
       "\"actual_A18_lift_claimed\":false")<>1 or
     D972R2Count(D972R2ReceiptRaw,
       "\"run_id\":32901384400")<>1 or
     D972R2Count(D972R2ReceiptRaw,
       "1c739559eee368ba676c694960be21db94d6bc2292a6136d89b97bedfef3e15b")<1 or
     D972R2Count(D972R2ReceiptRaw,
       "fc3901c29f958e216e17ba175be4857ee26cc140f3f809f0e29833b636ccd436")<1 then
    Error("R07 resume v2 driver: receipt fixed envelope");
  fi;
  for D972R2Claim in ["actual_A18_occurrence","all_bases_obstruction",
      "compatible_cofinal_lift","ihara_witness",
      "normalized_Brunnian_class"] do
    if D972R2Count(D972R2ReceiptRaw,
         Concatenation("\"",D972R2Claim,"\":false"))<1 then
      Error("R07 resume v2 driver: false global claim ",D972R2Claim);
    fi;
  od;
  D972R2TerminalCount:=0;; D972R2Terminal:=fail;;
  for D972R2Token in ["R07_760_L3_TARGET6_NONMEMBER",
      "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE",
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
      "R07_760_L3_TARGET6_INPUT_STOP"] do
    D972R2PCount:=D972R2Count(D972R2Raw,
      Concatenation("terminal=",D972R2Token));;
    D972R2JCount:=D972R2Count(D972R2ReceiptRaw,
      Concatenation("\"terminal_token\":\"",D972R2Token,"\""));;
    if D972R2PCount=1 and D972R2JCount=1 then
      D972R2TerminalCount:=D972R2TerminalCount+1;;
      D972R2Terminal:=D972R2Token;;
    elif D972R2PCount<>0 or D972R2JCount<>0 then
      Error("R07 resume v2 driver: terminal mismatch");
    fi;
  od;
  if D972R2TerminalCount<>1 then
    Error("R07 resume v2 driver: exclusive terminal");
  fi;
  if D972R2Terminal in ["R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
                        "R07_760_L3_TARGET6_INPUT_STOP"] then
    if D972R2Count(D972R2ReceiptRaw,
         "\"mathematical_membership_claimed\":false")<>1 or
       D972R2Count(D972R2ReceiptRaw,
         "\"mathematical_nonmembership_claimed\":false")<>1 or
       D972R2Count(D972R2ReceiptRaw,"\"stage\":")<1 or
       D972R2Count(D972R2ReceiptRaw,"\"reason\":")<1 then
      Error("R07 resume v2 driver: claim-free stop");
    fi;
  elif D972R2Terminal="R07_760_L3_TARGET6_NONMEMBER" then
    if D972R2Count(D972R2ReceiptRaw,
         "\"all_generated_rows_annihilated\":true")<1 or
       D972R2Count(D972R2ReceiptRaw,
         "\"target_pairing_nonzero\":true")<1 then
      Error("R07 resume v2 driver: NONMEMBER candidate canaries");
    fi;
  fi;
  D972R2CheckpointCount:=0;; D972R2MissingSeen:=false;;
  for D972R2J in [9..12] do
    D972R2Checkpoint:=D972R2CheckpointPath(D972R2J);;
    if IsExistingFile(D972R2Checkpoint) then
      if D972R2MissingSeen then
        Error("R07 resume v2 driver: non-prefix checkpoint roster");
      fi;
      D972R2CheckpointRaw:=D972R2Read(D972R2Checkpoint,"checkpoint");;
      D972R2CheckpointSHA:=HexSHA256(D972R2CheckpointRaw);;
      if D972R2Count(D972R2ReceiptRaw,
           Concatenation("\"path\":\"",D972R2Checkpoint,"\""))<>1 or
         D972R2Count(D972R2ReceiptRaw,
           Concatenation("\"sha256\":\"",D972R2CheckpointSHA,"\""))<1 or
         D972R2Count(D972R2ReceiptRaw,
           Concatenation("\"bytes\":",String(Length(D972R2CheckpointRaw))))<1 or
         D972R2Count(D972R2CheckpointRaw,
           "\"schema\":\"d972-r07-760-l3-target6-resume-checkpoint/v2\"")<>1 or
         D972R2Count(D972R2CheckpointRaw,
           "\"checkpoint_state\":\"R07_760_L3_TARGET6_RESUME_V2_CHECKPOINT_READY\"")<>1 or
         D972R2Count(D972R2CheckpointRaw,
           "\"grade\":\"CANDIDATE\"")<>1 then
        Error("R07 resume v2 driver: checkpoint binding");
      fi;
      D972R2CheckpointCount:=D972R2CheckpointCount+1;;
      Print("R07_760_L3_TARGET6_RESUME_V2_CHECKPOINT j=",D972R2J,
            " path=",D972R2Checkpoint," sha256=",D972R2CheckpointSHA,
            " bytes=",Length(D972R2CheckpointRaw),"\n");;
    else
      D972R2MissingSeen:=true;;
    fi;
  od;
  if D972R2Count(D972R2Raw,
       Concatenation(" checkpoints=",String(D972R2CheckpointCount)))<>1 then
    Error("R07 resume v2 driver: checkpoint marker count");
  fi;
  if D972R2Terminal="R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE" and
     D972R2CheckpointCount<>4 then
    Error("R07 resume v2 driver: MEMBER checkpoint completeness");
  fi;
  if D972R2Terminal="R07_760_L3_TARGET6_NONMEMBER" and
     D972R2CheckpointCount=0 then
    Error("R07 resume v2 driver: NONMEMBER missing checkpoint");
  fi;
  D972R2TimingRaw:=D972R2Read(D972R2Timing,"timing ledger");;
  if D972R2Count(D972R2TimingRaw,"inner_seconds=21000")<>1 or
     D972R2Count(D972R2TimingRaw,"outer_seconds=21600")<>1 or
     D972R2Count(D972R2TimingRaw,"producer_processes=1")<>1 or
     D972R2Count(D972R2TimingRaw,"checker_processes=0")<>1 or
     D972R2Count(D972R2TimingRaw,"grade=CANDIDATE")<>1 or
     D972R2Count(D972R2TimingRaw,
       Concatenation("checkpoint_count=",String(D972R2CheckpointCount)))<>1 then
    Error("R07 resume v2 driver: timing ledger");
  fi;
  D972R2LogSHA:=HexSHA256(D972R2Raw);;
  D972R2TimingSHA:=HexSHA256(D972R2TimingRaw);;
  Print("R07_760_L3_TARGET6_RESUME_V2_GHA_DRIVER_PASS mode=full ",
        "terminal=",D972R2Terminal," grade=CANDIDATE ",
        "cross_checked=false producer_processes=1 checker_processes=0 ",
        "checkpoints=",D972R2CheckpointCount," receipt=",D972R2Artifact,
        " receipt_sha256=",D972R2ReceiptSHA,
        " receipt_bytes=",Length(D972R2ReceiptRaw)," log=",D972R2Log,
        " log_sha256=",D972R2LogSHA," log_bytes=",Length(D972R2Raw),
        " timing=",D972R2Timing," timing_sha256=",D972R2TimingSHA,
        " timing_bytes=",Length(D972R2TimingRaw),"\n");;
fi;
