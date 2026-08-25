#############################################################################
## R07 g760 C-13/L3 target6 GHA driver v1.
## ASCII only.  Full mode is GHA-only and runs producer then checker serially.
#############################################################################

D972L3Producer := "search/d972_r07_760_l3_target6_v1.py";;
D972L3Checker := "crosscheck/check_d972_r07_760_l3_target6_v1.py";;
D972L3Preflight :=
  "search/certs/d972_r07_760_l3_target6_preflight_v1_20260826.json";;
D972L3Artifact := "ci/out/d972_r07_760_l3_target6_v1.json";;
D972L3ProducerLog := "ci/out/d972_r07_760_l3_target6_v1_producer.log";;
D972L3CheckerLog := "ci/out/d972_r07_760_l3_target6_v1_checker.log";;
D972L3MathOK := "ci/out/d972_r07_760_l3_target6_v1_math.ok";;
D972L3Timing := "ci/out/d972_r07_760_l3_target6_v1_timing.txt";;
D972L3TotalSeconds := 21000;;
D972L3ProducerSeconds := 10200;;
D972L3Dialogue := Concatenation("docs/",
  List([229,175,190,232,169,177,229,184,179],CharInt),".md");;

D972L3Pins := [
  [D972L3Producer,
   "a73b78d1a9ed6faae3230bef07c24194733dee77334e8e5006c38b8d00b46ac0",35202],
  [D972L3Checker,
   "e8cc6b5acaeaee88147a5ebcb3490a2a51aeaa45f73adf839df732df6ac986b1",40489],
  [D972L3Preflight,
   "0711173b953e164c20ae2ce249d8bce1220b892899d9e14308601d731678d6ba",663404],
  ["sol/luna_task_163_r07_760_l3_target6_v1.md",
   "9fcdf2f25b724e9dbc225f417b0036e126e7b5e37a0778dab5e0299ee2f74e12",9066],
  ["provenance/CLAIMS.md",
   "37325e7e7d734f7619785eb1832a051a4e35bb7409e0adaad413443a13038c00",68363],
  [D972L3Dialogue,
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
  ["search/koubou158_L3_radical_v1_2.py",
   "05e96bb3e7d0e9b949cb8d9ec0d216f97a698777df82d56449bcc20f89933f17",14488],
  ["search/koubou158_L3_core_v1_2.py",
   "4366ebd1759fbd11a795b251101776836ef4ec2a28b7b947b93727208e199c63",31192],
  ["crosscheck/check_koubou158_L3_radical_v1.py",
   "451aa614d2c83f43291fa80abf09abe425004288717ed6278b5690b511724529",28198],
  ["search/certs/koubou158_L3_radical_v1_1_20260822.json",
   "4a80c0b4c063eaab31ce32aad69eb9f21c220278dc748e31439aef9af38a2ca2",17418],
  ["search/certs/koubou158_L3_radical_v1_2_20260822.json",
   "56ab4592bf5b64fbe5605afe063681e8c059929cd8abbc07323988aff4a8440f",20930],
  ["crosscheck/verdicts/koubou158_L3_radical_crosscheck_v1_20260822.json",
   "c87e12ba96ea95607e99701e1e92786ac93ba08c91ad424dbea1f252304b1b78",7654],
  ["ci/b345_157en_artifacts_32458556448/d972_b345_q3_chief_v1.json",
   "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72",231570],
  ["search/d972_b345_seedspan_triple4_v1.py",
   "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29",535219]
];;

D972L3Read := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then
    Error("R07 g760 L3 driver: missing or empty ",label);
  fi;
  return raw;
end;;

D972L3Count := function(raw,needle)
  local i,n,m,count;
  if not IsString(raw) or not IsString(needle) or Length(needle)=0 then
    Error("R07 g760 L3 driver: count input");
  fi;
  n:=Length(raw);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972L3Pin := function(row)
  local raw,got;
  if not IsList(row) or Length(row)<>3 or not IsString(row[1]) or
     not IsString(row[2]) or Length(row[2])<>64 or
     not IsInt(row[3]) or row[3]<=0 then
    Error("R07 g760 L3 driver: malformed pin");
  fi;
  raw:=D972L3Read(row[1],row[1]);; got:=HexSHA256(raw);;
  if got<>row[2] or Length(raw)<>row[3] then
    Error("R07 g760 L3 driver: pin drift ",row[1]," sha=",got,
          " bytes=",Length(raw));
  fi;
  return true;
end;;

D972L3CleanLog := function(raw,label)
  local token;
  for token in ["Traceback (most recent call last):", "SyntaxError",
                "RuntimeError", "Error,", "Reject:", " FAIL ",
                " failed"] do
    if D972L3Count(raw,token)<>0 then
      Error("R07 g760 L3 driver: forbidden log token ",label," ",token);
    fi;
  od;
  return true;
end;;

D972L3ShellQuote := function(path)
  if not IsString(path) or Length(path)=0 or
     PositionSublist(path,"\"")<>fail or
     PositionSublist(path,"\n")<>fail or
     PositionSublist(path,"\r")<>fail then
    Error("R07 g760 L3 driver: unsafe shell path");
  fi;
  return Concatenation("\"",path,"\"");
end;;

D972L3RemoveOwn := function(paths)
  local path;
  if Length(Set(paths))<>Length(paths) then
    Error("R07 g760 L3 driver: duplicate cleanup path");
  fi;
  for path in paths do
    if IsExistingFile(path) then RemoveFile(path);; fi;
  od;
  if ForAny(paths,IsExistingFile) then
    Error("R07 g760 L3 driver: stale own output survived cleanup");
  fi;
  return true;
end;;

for D972L3PinRow in D972L3Pins do D972L3Pin(D972L3PinRow);; od;

D972L3Self := IsBound(D972_R07_760_L3_TARGET6_V1_SELFTEST) and
  D972_R07_760_L3_TARGET6_V1_SELFTEST=true;;
D972L3Run := IsBound(D972_R07_760_L3_TARGET6_V1_RUN) and
  D972_R07_760_L3_TARGET6_V1_RUN=true;;
if D972L3Self=D972L3Run then
  Error("R07 g760 L3 driver: select exactly one mode");
fi;

D972L3Python := "python";;
if IsBound(D972_R07_760_L3_TARGET6_V1_PYTHON) then
  D972L3Python:=D972_R07_760_L3_TARGET6_V1_PYTHON;;
fi;
if not D972L3Python in ["python","python3"] then
  Error("R07 g760 L3 driver: Python binding");
fi;
if D972L3Run and D972L3Python<>"python3" then
  Error("R07 g760 L3 driver: GHA full requires python3");
fi;

if D972L3Self then
  D972L3TempDirectory:=DirectoryTemporary();;
  if D972L3TempDirectory=fail then
    Error("R07 g760 L3 driver: no external temporary directory");
  fi;
  D972L3TempRoot:=Filename(D972L3TempDirectory,"");;
  D972L3SelfReceipt:=Filename(D972L3TempDirectory,"preflight.json");;
  D972L3SelfLog:=Filename(D972L3TempDirectory,"selftest.log");;
  D972L3SelfOK:=Filename(D972L3TempDirectory,"selftest.ok");;
  D972L3RepoRoot:=Filename(DirectoryCurrent(),"");;
  if Length(Set([D972L3SelfReceipt,D972L3SelfLog,D972L3SelfOK]))<>3 or
     ForAny([D972L3SelfReceipt,D972L3SelfLog,D972L3SelfOK],x->
       PositionSublist(x,D972L3TempRoot)<>1 or
       PositionSublist(x,D972L3RepoRoot)=1) then
    Error("R07 g760 L3 driver: selftest path boundary");
  fi;
  D972L3RemoveOwn([D972L3SelfReceipt,D972L3SelfLog,D972L3SelfOK]);;
  D972L3SelfCommand:=Concatenation(
    D972L3Python," -u -B \"",D972L3Producer,"\" --self-test > ",
    D972L3ShellQuote(D972L3SelfLog)," 2>&1 && ",
    D972L3Python," -u -B \"",D972L3Checker,"\" --self-test >> ",
    D972L3ShellQuote(D972L3SelfLog)," 2>&1 && ",
    D972L3Python," -u -B \"",D972L3Producer,
    "\" --preflight --output ",D972L3ShellQuote(D972L3SelfReceipt)," >> ",
    D972L3ShellQuote(D972L3SelfLog)," 2>&1 && ",
    D972L3Python," -u -B \"",D972L3Checker,"\" --receipt ",
    D972L3ShellQuote(D972L3SelfReceipt)," --mutations >> ",
    D972L3ShellQuote(D972L3SelfLog)," 2>&1 && echo ",
    "D972_R07_760_L3_TARGET6_V1_SELFTEST_EXIT_ZERO > ",
    D972L3ShellQuote(D972L3SelfOK));;
  Exec(D972L3SelfCommand);;
  D972L3SelfRaw:=D972L3Read(D972L3SelfLog,"selftest log");;
  D972L3CleanLog(D972L3SelfRaw,"selftest");;
  if D972L3Count(D972L3Read(D972L3SelfOK,"selftest sentinel"),
       "D972_R07_760_L3_TARGET6_V1_SELFTEST_EXIT_ZERO")<>1 or
     D972L3Count(D972L3SelfRaw,
       "R07_760_L3_TARGET6_V1_PRODUCER_SELFTEST_PASS")<>1 or
     D972L3Count(D972L3SelfRaw,
       "R07_760_L3_TARGET6_V1_CHECKER_SELFTEST_PASS")<>1 or
     D972L3Count(D972L3SelfRaw,
       "R07_760_L3_TARGET6_V1_PRODUCER_PASS preflight_state=R07_760_L3_TARGET6_PREFLIGHT_READY")<>1 or
     D972L3Count(D972L3SelfRaw,
       "R07_760_L3_TARGET6_V1_CHECKER_PASS preflight_state=R07_760_L3_TARGET6_PREFLIGHT_READY")<>1 or
     D972L3Count(D972L3SelfRaw,"mutations=11 full_replay=false")<>1 then
    Error("R07 g760 L3 driver: selftest markers");
  fi;
  D972L3SelfReceiptRaw:=D972L3Read(D972L3SelfReceipt,"selftest receipt");;
  D972L3SelfReceiptSHA:=HexSHA256(D972L3SelfReceiptRaw);;
  if D972L3Count(D972L3SelfRaw,
       Concatenation(" sha256=",D972L3SelfReceiptSHA))<>1 or
     D972L3Count(D972L3SelfRaw,
       Concatenation(" receipt_sha256=",D972L3SelfReceiptSHA))<>1 or
     D972L3Count(D972L3SelfRaw,
       Concatenation(" bytes=",String(Length(D972L3SelfReceiptRaw))))<>1 then
    Error("R07 g760 L3 driver: selftest receipt binding");
  fi;
  Print("R07_760_L3_TARGET6_V1_GHA_DRIVER_PASS mode=selftest ",
        "preflight_mutations=11 receipt_sha256=",D972L3SelfReceiptSHA,
        " bytes=",Length(D972L3SelfReceiptRaw),"\n");;
else
  D972L3OwnOutputs:=[D972L3Artifact,D972L3ProducerLog,D972L3CheckerLog,
    D972L3MathOK,D972L3Timing];;
  D972L3RemoveOwn(D972L3OwnOutputs);;
  Exec(Concatenation(
    "mkdir -p 'ci/out' && bash -o pipefail -c '",
    "set -e; SECONDS=0; ",
    "python3 -u -B search/d972_r07_760_l3_target6_v1.py --full ",
    "--seconds 10200 --output ci/out/d972_r07_760_l3_target6_v1.json ",
    "2>&1 | tee ci/out/d972_r07_760_l3_target6_v1_producer.log; ",
    "producer_elapsed=$SECONDS; remaining=$((21000-SECONDS)); ",
    "if [ $remaining -le 0 ]; then exit 97; fi; ",
    "python3 -u -B crosscheck/check_d972_r07_760_l3_target6_v1.py ",
    "--full --mutations --seconds $remaining ",
    "--receipt ci/out/d972_r07_760_l3_target6_v1.json ",
    "2>&1 | tee ci/out/d972_r07_760_l3_target6_v1_checker.log; ",
    "final_elapsed=$SECONDS; final_margin=$((21000-final_elapsed)); ",
    "if [ $final_margin -le 0 ]; then exit 98; fi; ",
    "printf \"producer_elapsed=%s\\nchecker_initial_remaining=%s\\n",
    "final_elapsed=%s\\nfinal_margin=%s\\nshared_seconds=21000\\n",
    "producer_cap_seconds=10200\\n\" $producer_elapsed $remaining ",
    "$final_elapsed $final_margin > ",D972L3Timing,"; ",
    "printf %s D972_R07_760_L3_TARGET6_V1_MATH_EXIT_ZERO > ",
    D972L3MathOK,"'"));;
  if D972L3Read(D972L3MathOK,"full sentinel")<>
       "D972_R07_760_L3_TARGET6_V1_MATH_EXIT_ZERO" then
    Error("R07 g760 L3 driver: producer/checker process");
  fi;
  D972L3PRaw:=D972L3Read(D972L3ProducerLog,"producer log");;
  D972L3CRaw:=D972L3Read(D972L3CheckerLog,"checker log");;
  D972L3CleanLog(D972L3PRaw,"producer");;
  D972L3CleanLog(D972L3CRaw,"checker");;
  if D972L3Count(D972L3PRaw,
       "R07_760_L3_TARGET6_V1_PRODUCER_PASS")<>1 or
     D972L3Count(D972L3CRaw,
       "R07_760_L3_TARGET6_V1_CHECKER_PASS")<>1 then
    Error("R07 g760 L3 driver: final marker counts");
  fi;
  D972L3ReceiptRaw:=D972L3Read(D972L3Artifact,"full receipt");;
  D972L3ReceiptSHA:=HexSHA256(D972L3ReceiptRaw);;
  if D972L3Count(D972L3PRaw,
       Concatenation(" sha256=",D972L3ReceiptSHA))<>1 or
     D972L3Count(D972L3PRaw,
       Concatenation(" bytes=",String(Length(D972L3ReceiptRaw))))<>1 or
     D972L3Count(D972L3CRaw,
       Concatenation(" receipt_sha256=",D972L3ReceiptSHA))<>1 then
    Error("R07 g760 L3 driver: full receipt binding");
  fi;
  D972L3TerminalCount:=0;; D972L3MatchedTerminal:=fail;;
  for D972L3Token in ["R07_760_L3_TARGET6_NONMEMBER",
      "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE",
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
      "R07_760_L3_TARGET6_INPUT_STOP"] do
    D972L3PCount:=D972L3Count(D972L3PRaw,
      Concatenation("terminal=",D972L3Token));;
    D972L3CCount:=D972L3Count(D972L3CRaw,
      Concatenation("terminal=",D972L3Token));;
    if D972L3PCount=1 and D972L3CCount=1 then
      D972L3TerminalCount:=D972L3TerminalCount+1;;
      D972L3MatchedTerminal:=D972L3Token;;
    elif D972L3PCount<>0 or D972L3CCount<>0 then
      Error("R07 g760 L3 driver: producer/checker terminal mismatch");
    fi;
  od;
  if D972L3TerminalCount<>1 then
    Error("R07 g760 L3 driver: exclusive terminal");
  fi;
  D972L3TimingRaw:=D972L3Read(D972L3Timing,"timing ledger");;
  if D972L3Count(D972L3TimingRaw,"shared_seconds=21000")<>1 or
     D972L3Count(D972L3TimingRaw,"producer_cap_seconds=10200")<>1 or
     D972L3Count(D972L3TimingRaw,"final_margin=")<>1 then
    Error("R07 g760 L3 driver: timing ledger");
  fi;
  Print("R07_760_L3_TARGET6_V1_GHA_DRIVER_PASS mode=full terminal=",
        D972L3MatchedTerminal," artifact_sha256=",D972L3ReceiptSHA,
        " bytes=",Length(D972L3ReceiptRaw),"\n");;
fi;
