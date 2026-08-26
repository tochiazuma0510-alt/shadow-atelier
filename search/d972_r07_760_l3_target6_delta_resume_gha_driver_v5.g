#############################################################################
## R07 g760 L3 target6 append-only-delta producer-only driver v5.
## ASCII only.  One Python producer, zero checker processes.
#############################################################################

D972R5Producer :=
  "search/d972_r07_760_l3_target6_delta_resume_v5.py";;
D972R5Checker :=
  "crosscheck/check_d972_r07_760_l3_target6_resume_v2.py";;
D972R5Preflight :=
  "search/certs/d972_r07_760_l3_target6_delta_resume_preflight_v5_20260827.json";;
D972R5Artifact :=
  "ci/out/d972_r07_760_l3_target6_delta_resume_v5.json";;
D972R5Log :=
  "ci/out/d972_r07_760_l3_target6_delta_resume_v5_producer.log";;
D972R5Timing :=
  "ci/out/d972_r07_760_l3_target6_delta_resume_v5_timing.txt";;
D972R5Hashes :=
  "ci/out/d972_r07_760_l3_target6_delta_resume_v5_checkpoint_hashes.txt";;
D972R5OK :=
  "ci/out/d972_r07_760_l3_target6_delta_resume_v5.ok";;
D972R5CheckpointDir :=
  "ci/out/d972_r07_760_l3_target6_delta_resume_v5_checkpoints";;
D972R5InnerSeconds := 19200;;
D972R5OuterSeconds := 19800;;
D972R5MaxNewRelators := 11;;

D972R5Pins := [
  [D972R5Producer,
   "94184831ede05c78d7206e62dbdd5c564daa493330fe1c5e433be2804267652b",108142],
  [D972R5Checker,
   "7cc683ccf16880d3c8794573dfffcbbf0b453cdcf2e7cd2e5665eb78a9e26365",63772],
  [D972R5Preflight,
   "76da0c9f78f3efff305289bb864e25819a722c2362dc2dffb250c98be9244305",36718],
  ["sol/luna_task_167_r07_target6_postclosure_recovery_v5.md",
   "3b885303f4bf512fc7a9a8e3f124f87a91ca4f3c7728920ee420d781dbe23e8c",7170],
  ["search/d972_r07_760_l3_target6_delta_resume_v4.py",
   "08f2237ac6aa438dded775c55627f07ffeff74145765b6e9791a898d594d77ef",88429],
  ["search/d972_r07_760_l3_target6_delta_resume_gha_driver_v4.g",
   "274291371fd5548d5cf5505c5b250cb88a7c74e08ab23f5d0b437a58a079e531",16494],
  ["search/certs/d972_r07_760_l3_target6_delta_resume_preflight_v4_20260826.json",
   "0a715bcedec3283894461444fa3d7f542255a436780327bb95f87d1a411e4fbf",34608],
  ["sol/luna_reply_166_r07_target6_delta_checkpoint_v4.md",
   "6ed022217995157752b523cc50aaae86ed494a81bee00f4c811c9816548f09df",9216],
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

D972R5Read := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then
    Error("R07 delta resume v5 driver: missing or empty ",label);
  fi;
  return raw;
end;;

D972R5ReadMaybeEmpty := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail then
    Error("R07 delta resume v5 driver: missing ",label);
  fi;
  return raw;
end;;

D972R5Count := function(raw,needle)
  local i,n,m,count;
  if not IsString(raw) or not IsString(needle) or Length(needle)=0 then
    Error("R07 delta resume v5 driver: count input");
  fi;
  n:=Length(raw);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972R5Pin := function(row)
  local raw,got;
  if not IsList(row) or Length(row)<>3 or not IsString(row[1]) or
     not IsString(row[2]) or Length(row[2])<>64 or
     not IsInt(row[3]) or row[3]<=0 then
    Error("R07 delta resume v5 driver: malformed pin");
  fi;
  raw:=D972R5Read(row[1],row[1]);; got:=HexSHA256(raw);;
  if got<>row[2] or Length(raw)<>row[3] then
    Error("R07 delta resume v5 driver: pin drift ",row[1]);
  fi;
  return true;
end;;

D972R5CleanLog := function(raw,label)
  local token;
  for token in ["Traceback (most recent call last):", "SyntaxError",
                "RuntimeError", "Error,", "Reject:", " FAIL ",
                " failed"] do
    if D972R5Count(raw,token)<>0 then
      Error("R07 delta resume v5 driver: forbidden log token ",
            label," ",token);
    fi;
  od;
  return true;
end;;

D972R5ShellQuote := function(path)
  if not IsString(path) or Length(path)=0 or
     PositionSublist(path,"\"")<>fail or
     PositionSublist(path,"\n")<>fail or
     PositionSublist(path,"\r")<>fail then
    Error("R07 delta resume v5 driver: unsafe shell path");
  fi;
  return Concatenation("\"",path,"\"");
end;;

D972R5RemoveOwn := function(paths)
  local path;
  if Length(Set(paths))<>Length(paths) then
    Error("R07 delta resume v5 driver: duplicate cleanup path");
  fi;
  for path in paths do
    if IsExistingFile(path) then RemoveFile(path);; fi;
  od;
  if ForAny(paths,IsExistingFile) then
    Error("R07 delta resume v5 driver: stale own output survived");
  fi;
  return true;
end;;

D972R5DeltaPath := function(j,r)
  local js,rs;
  if not j in [9..12] or not r in [1..11] then
    Error("R07 delta resume v5 driver: delta index");
  fi;
  js:=String(j);; rs:=String(r);;
  if j<10 then js:=Concatenation("0",js);; fi;
  if r<10 then rs:=Concatenation("0",rs);; fi;
  return Concatenation(D972R5CheckpointDir,
    "/d972_r07_760_l3_target6_delta_resume_v5_j",js,
    "_r",rs,".delta.jsonl.gz");
end;;

D972R5JPath := function(j)
  local js;
  if not j in [9..12] then
    Error("R07 delta resume v5 driver: j index");
  fi;
  js:=String(j);;
  if j<10 then js:=Concatenation("0",js);; fi;
  return Concatenation(D972R5CheckpointDir,
    "/d972_r07_760_l3_target6_delta_resume_v5_j",js,
    ".json");
end;;

if IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_MAX_NEW_RELATORS) then
  if not IsInt(
      D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_MAX_NEW_RELATORS) or
     D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_MAX_NEW_RELATORS<1 or
     D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_MAX_NEW_RELATORS>44 then
    Error("R07 delta resume v5 driver: MAX_NEW_RELATORS range 1..44");
  fi;
  D972R5MaxNewRelators:=
    D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_MAX_NEW_RELATORS;;
fi;

D972R5Terminals := [
  "R07_760_L3_TARGET6_NONMEMBER",
  "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE",
  "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
  "R07_760_L3_TARGET6_INPUT_STOP"
];;

D972R5AuditReceipt := function(raw,log,terminal)
  local token,pcount,jcount,exclusive,claim;
  if not IsString(raw) or not IsString(log) or
     not terminal in D972R5Terminals then return false; fi;
  if D972R5Count(log,
       "R07_760_L3_TARGET6_DELTA_RESUME_V5_PRODUCER_PASS")<>1 or
     D972R5Count(log,Concatenation(
       " sha256=",HexSHA256(raw)," bytes=",String(Length(raw))))<>1 then
    return false;
  fi;
  if D972R5Count(raw,"\"grade\":\"CANDIDATE\"")<1 or
     D972R5Count(raw,"\"grade\":\"VERIFIED\"")<>0 or
     D972R5Count(raw,"\"grade\":\"CROSS_CHECKED\"")<>0 or
     D972R5Count(raw,
       "\"delta_chain_reconstructs_full_relator_state\":true")<>1 or
     D972R5Count(raw,
       "\"delta_checkpoint_is_resource_recovery_only\":true")<>1 or
     D972R5Count(raw,
       "\"inherited_prefix_grade\":\"producer_control_flow_candidate_only\"")<>2 or
     D972R5Count(raw,"\"mathematical_membership_claimed\":true")<>0 or
     D972R5Count(raw,"\"mathematical_nonmembership_claimed\":true")<>0 or
     D972R5Count(raw,"\"actual_A18_lift_claimed\":true")<>0 then
    return false;
  fi;
  for claim in ["actual_A18_occurrence","all_bases_obstruction",
      "compatible_cofinal_lift","ihara_witness",
      "normalized_Brunnian_class"] do
    if D972R5Count(raw,Concatenation("\"",claim,"\":false"))<1 or
       D972R5Count(raw,Concatenation("\"",claim,"\":true"))<>0 then
      return false;
    fi;
  od;
  exclusive:=0;;
  for token in D972R5Terminals do
    pcount:=D972R5Count(log,Concatenation("terminal=",token));;
    jcount:=D972R5Count(raw,
      Concatenation("\"terminal_token\":\"",token,"\""));;
    if token=terminal then
      if pcount<>1 or jcount<>1 or
         D972R5Count(raw,
           Concatenation("\"status\":\"",token,"\""))<>1 or
         D972R5Count(raw,
           Concatenation("\"state\":\"",token,"\""))<1 then
        return false;
      fi;
      exclusive:=exclusive+1;;
    elif pcount<>0 or jcount<>0 then
      return false;
    fi;
  od;
  if exclusive<>1 then return false; fi;
  if terminal="R07_760_L3_TARGET6_NONMEMBER" then
    if D972R5Count(raw,"\"first_nonmember_j\":null")<>0 or
       D972R5Count(raw,"\"nonmember\":true")<1 or
       D972R5Count(raw,"\"safe_stop\":false")<>1 then return false; fi;
  elif terminal="R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE" then
    if D972R5Count(raw,"\"first_nonmember_j\":null")<>1 or
       D972R5Count(raw,"\"fresh_j_order_tested\":[9,10,11,12]")<>1 or
       D972R5Count(raw,"\"safe_stop\":false")<>1 then
      return false;
    fi;
  else
    if D972R5Count(raw,"\"stop_stage\":\"")<>1 or
       D972R5Count(raw,"\"stop_reason\":\"")<>1 or
       D972R5Count(raw,
         "\"stop_reason_sanitized_ascii_bounded\":true")<>1 then
      return false;
    fi;
    if D972R5Count(raw,"\"safe_stop\":true")+
         D972R5Count(raw,"\"safe_stop\":false")<>1 then return false; fi;
    if terminal="R07_760_L3_TARGET6_INPUT_STOP" and
       D972R5Count(raw,"\"safe_stop\":true")<>0 then return false; fi;
    if D972R5Count(raw,"\"safe_stop\":true")=1 and
       (D972R5Count(raw,
          "\"safe_stop_checkpoint_authenticated\":true")<>1 or
        D972R5Count(raw,Concatenation("\"max_new_relators\":",
          String(D972R5MaxNewRelators)))<>1 or
        D972R5Count(raw,Concatenation("\"new_relators_completed\":",
          String(D972R5MaxNewRelators)))<>1 or
        D972R5Count(raw,"\"exact_next_j\":")<>1 or
        D972R5Count(raw,"\"exact_next_j\":null")<>0 or
        D972R5Count(raw,"\"exact_next_relator\":")<>1 or
        D972R5Count(raw,"\"exact_next_relator\":null")<>0 or
        D972R5Count(raw,"\"unfinished_relator_inferred\":false")<>1) then
      return false;
    fi;
  fi;
  return true;
end;;

D972R5ReplaceFirst := function(raw,old,new)
  local p,left,right,q;
  p:=PositionSublist(raw,old);;
  if p=fail then Error("R07 delta resume v5 driver: fixture needle"); fi;
  if p=1 then left:="";; else left:=raw{[1..p-1]};; fi;
  q:=p+Length(old);;
  if q>Length(raw) then right:="";;
  else right:=raw{[q..Length(raw)]};; fi;
  return Concatenation(left,new,right);
end;;

D972R5Fixture := function(terminal)
  local first,nonmember,safe,authenticated;
  first:="null";; nonmember:="false";; safe:="false";;
  authenticated:="false";;
  if terminal="R07_760_L3_TARGET6_NONMEMBER" then
    first:="9";; nonmember:="true";;
  elif terminal="R07_760_L3_TARGET6_UNKNOWN_RESOURCE" then
    safe:="true";; authenticated:="true";;
  fi;
  return Concatenation(
    "{\"claims\":{\"actual_A18_occurrence\":false,",
    "\"all_bases_obstruction\":false,",
    "\"compatible_cofinal_lift\":false,\"ihara_witness\":false,",
    "\"normalized_Brunnian_class\":false},\"grade\":\"CANDIDATE\",",
    "\"resume_contract\":{\"inherited_prefix_grade\":",
    "\"producer_control_flow_candidate_only\"},\"status\":\"",terminal,
    "\",\"terminal_token\":\"",terminal,"\",\"result\":{",
    "\"state\":\"",terminal,"\",\"inherited_prefix_grade\":",
    "\"producer_control_flow_candidate_only\",",
    "\"delta_chain_reconstructs_full_relator_state\":true,",
    "\"delta_checkpoint_is_resource_recovery_only\":true,",
    "\"mathematical_membership_claimed\":false,",
    "\"mathematical_nonmembership_claimed\":false,",
    "\"actual_A18_lift_claimed\":false,\"first_nonmember_j\":",first,",",
    "\"fresh_j_order_tested\":[9,10,11,12],\"nonmember\":",nonmember,",",
    "\"stop_stage\":\"toy\",\"stop_reason\":\"toy\",",
    "\"stop_reason_sanitized_ascii_bounded\":true,\"safe_stop\":",safe,",",
    "\"safe_stop_checkpoint_authenticated\":",authenticated,",",
    "\"max_new_relators\":",String(D972R5MaxNewRelators),",",
    "\"new_relators_completed\":",String(D972R5MaxNewRelators),",",
    "\"exact_next_j\":10,\"exact_next_relator\":1,",
    "\"unfinished_relator_inferred\":false}}") ;
end;;

D972R5FixtureLog := function(raw,terminal)
  return Concatenation(
    "R07_760_L3_TARGET6_DELTA_RESUME_V5_PRODUCER_PASS terminal=",terminal,
    " grade=CANDIDATE sha256=",HexSHA256(raw),
    " bytes=",String(Length(raw)),"\n");
end;;

D972R5DriverFixtureSelftest := function()
  local token,raw,log,bad,rejected;
  for token in D972R5Terminals do
    raw:=D972R5Fixture(token);; log:=D972R5FixtureLog(raw,token);;
    if not D972R5AuditReceipt(raw,log,token) then
      Error("R07 delta resume v5 driver: valid terminal fixture ",token);
    fi;
  od;
  rejected:=0;;
  raw:=D972R5Fixture("R07_760_L3_TARGET6_UNKNOWN_RESOURCE");;
  log:=D972R5FixtureLog(raw,"R07_760_L3_TARGET6_UNKNOWN_RESOURCE");;
  bad:=Concatenation(raw,
    "\"inherited_prefix_grade\":\"producer_control_flow_candidate_only\"");;
  if not D972R5AuditReceipt(bad,D972R5FixtureLog(bad,
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE"),
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE") then rejected:=rejected+1;; fi;
  bad:=D972R5ReplaceFirst(raw,
    "\"inherited_prefix_grade\":\"producer_control_flow_candidate_only\"",
    "\"inherited_prefix_grade\":\"wrong\"");;
  if not D972R5AuditReceipt(bad,D972R5FixtureLog(bad,
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE"),
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE") then rejected:=rejected+1;; fi;
  bad:=D972R5ReplaceFirst(raw,"\"ihara_witness\":false",
                              "\"ihara_witness\":true");;
  if not D972R5AuditReceipt(bad,D972R5FixtureLog(bad,
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE"),
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE") then rejected:=rejected+1;; fi;
  bad:=D972R5ReplaceFirst(raw,
    "\"delta_checkpoint_is_resource_recovery_only\":true",
    "\"delta_checkpoint_is_resource_recovery_only\":false");;
  if not D972R5AuditReceipt(bad,D972R5FixtureLog(bad,
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE"),
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE") then rejected:=rejected+1;; fi;
  bad:=D972R5ReplaceFirst(raw,"\"mathematical_membership_claimed\":false",
                              "\"mathematical_membership_claimed\":true");;
  if not D972R5AuditReceipt(bad,D972R5FixtureLog(bad,
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE"),
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE") then rejected:=rejected+1;; fi;
  bad:=D972R5ReplaceFirst(raw,"\"grade\":\"CANDIDATE\"",
                              "\"grade\":\"VERIFIED\"");;
  if not D972R5AuditReceipt(bad,D972R5FixtureLog(bad,
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE"),
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE") then rejected:=rejected+1;; fi;
  bad:=Concatenation(raw,
    "\"terminal_token\":\"R07_760_L3_TARGET6_UNKNOWN_RESOURCE\"");;
  if not D972R5AuditReceipt(bad,D972R5FixtureLog(bad,
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE"),
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE") then rejected:=rejected+1;; fi;
  if not D972R5AuditReceipt(raw,
      D972R5FixtureLog(raw,"R07_760_L3_TARGET6_INPUT_STOP"),
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE") then rejected:=rejected+1;; fi;
  if not D972R5AuditReceipt(Concatenation(raw,"x"),log,
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE") then rejected:=rejected+1;; fi;
  bad:=D972R5ReplaceFirst(log,Concatenation(" bytes=",String(Length(raw))),
                              " bytes=0");;
  if not D972R5AuditReceipt(raw,bad,
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE") then rejected:=rejected+1;; fi;
  bad:=D972R5ReplaceFirst(raw,"\"stop_stage\":\"toy\"",
                              "\"stopped_at\":\"toy\"");;
  if not D972R5AuditReceipt(bad,D972R5FixtureLog(bad,
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE"),
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE") then rejected:=rejected+1;; fi;
  bad:=D972R5Fixture("R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE");;
  bad:=D972R5ReplaceFirst(bad,"\"fresh_j_order_tested\":[9,10,11,12]",
                              "\"fresh_j_order_tested\":[9]");;
  if not D972R5AuditReceipt(bad,D972R5FixtureLog(bad,
      "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE"),
      "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE") then rejected:=rejected+1;; fi;
  bad:=D972R5Fixture("R07_760_L3_TARGET6_NONMEMBER");;
  bad:=D972R5ReplaceFirst(bad,"\"first_nonmember_j\":9",
                              "\"first_nonmember_j\":null");;
  if not D972R5AuditReceipt(bad,D972R5FixtureLog(bad,
      "R07_760_L3_TARGET6_NONMEMBER"),
      "R07_760_L3_TARGET6_NONMEMBER") then rejected:=rejected+1;; fi;
  raw:=D972R5Fixture("R07_760_L3_TARGET6_UNKNOWN_RESOURCE");;
  log:=D972R5FixtureLog(raw,"R07_760_L3_TARGET6_UNKNOWN_RESOURCE");;
  bad:=Concatenation(log,log);;
  if not D972R5AuditReceipt(raw,bad,
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE") then rejected:=rejected+1;; fi;
  raw:=D972R5Fixture("R07_760_L3_TARGET6_UNKNOWN_RESOURCE");;
  bad:=D972R5ReplaceFirst(raw,
    "\"safe_stop_checkpoint_authenticated\":true",
    "\"safe_stop_checkpoint_authenticated\":false");;
  if not D972R5AuditReceipt(bad,D972R5FixtureLog(bad,
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE"),
      "R07_760_L3_TARGET6_UNKNOWN_RESOURCE") then rejected:=rejected+1;; fi;
  if rejected<>15 then
    Error("R07 delta resume v5 driver: fixture mutations ",rejected);
  fi;
  return rejected;
end;;

for D972R5PinRow in D972R5Pins do D972R5Pin(D972R5PinRow);; od;

D972R5Self :=
  IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_SELFTEST) and
  D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_SELFTEST=true;;
D972R5Run :=
  IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_RUN) and
  D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_RUN=true;;
if D972R5Self=D972R5Run then
  Error("R07 delta resume v5 driver: select exactly one mode");
fi;

D972R5UsePython3 := false;;
if IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_USE_PYTHON3) then
  if not D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_USE_PYTHON3 in
       [true,false] then
    Error("R07 delta resume v5 driver: USE_PYTHON3 boolean");
  fi;
  D972R5UsePython3:=
    D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_USE_PYTHON3;;
fi;
D972R5Python:="python";;
if D972R5UsePython3 then D972R5Python:="python3";; fi;
if D972R5Run and not D972R5UsePython3 then
  Error("R07 delta resume v5 driver: full requires python3");
fi;

D972R5ResumeDelta :=
  IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_RESUME_DELTA_J) or
  IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_RESUME_DELTA_R);;
D972R5ResumeJ :=
  IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_RESUME_J);;
if D972R5ResumeDelta and
   not (IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_RESUME_DELTA_J)
        and
        IsBound(D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_RESUME_DELTA_R))
   then
  Error("R07 delta resume v5 driver: incomplete delta resume pair");
fi;
if D972R5ResumeDelta and D972R5ResumeJ then
  Error("R07 delta resume v5 driver: two resume modes");
fi;
D972R5ResumePath:=fail;;
if D972R5ResumeDelta then
  D972R5ResumeDeltaJ:=
    D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_RESUME_DELTA_J;;
  D972R5ResumeDeltaR:=
    D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_RESUME_DELTA_R;;
  D972R5ResumePath:=D972R5DeltaPath(
    D972R5ResumeDeltaJ,D972R5ResumeDeltaR);;
elif D972R5ResumeJ then
  D972R5ResumeJValue:=
    D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_RESUME_J;;
  D972R5ResumePath:=D972R5JPath(D972R5ResumeJValue);;
fi;

if D972R5Self then
  if D972R5ResumePath<>fail then
    Error("R07 delta resume v5 driver: selftest cannot resume");
  fi;
  D972R5TempDirectory:=DirectoryTemporary();;
  if D972R5TempDirectory=fail then
    Error("R07 delta resume v5 driver: no temporary directory");
  fi;
  D972R5SelfLog:=Filename(D972R5TempDirectory,"selftest.log");;
  D972R5SelfOK:=Filename(D972R5TempDirectory,"selftest.ok");;
  D972R5RemoveOwn([D972R5SelfLog,D972R5SelfOK]);;
  D972R5FixtureMutations:=D972R5DriverFixtureSelftest();;
  D972R5SelfCommand:=Concatenation(
    D972R5Python," -u -B ",D972R5ShellQuote(D972R5Producer),
    " --self-test > ",D972R5ShellQuote(D972R5SelfLog)," 2>&1 && ",
    "echo D972_R07_DELTA_RESUME_V5_SELFTEST_EXIT_ZERO > ",
    D972R5ShellQuote(D972R5SelfOK));;
  if D972R5Count(D972R5SelfCommand,D972R5Producer)<>1 or
     D972R5Count(D972R5SelfCommand,D972R5Checker)<>0 then
    Error("R07 delta resume v5 driver: selftest command shape");
  fi;
  Exec(D972R5SelfCommand);;
  D972R5SelfRaw:=D972R5Read(D972R5SelfLog,"selftest log");;
  D972R5CleanLog(D972R5SelfRaw,"selftest");;
  if D972R5Count(D972R5Read(D972R5SelfOK,"selftest sentinel"),
       "D972_R07_DELTA_RESUME_V5_SELFTEST_EXIT_ZERO")<>1 or
     D972R5Count(D972R5SelfRaw,
       "R07_760_L3_TARGET6_DELTA_RESUME_V5_PRODUCER_SELFTEST_PASS")<>1 or
     D972R5Count(D972R5SelfRaw,"delta_mutations=12")<>1 or
     D972R5Count(D972R5SelfRaw,"j2_exhaustive=59049")<>1 or
     D972R5Count(D972R5SelfRaw,"postclosure_next_j=10")<>1 or
     D972R5Count(D972R5SelfRaw,"safe_resumed_new=1")<>1 or
     D972R5Count(D972R5SelfRaw,"append_only=true")<>1 or
     D972R5Count(D972R5SelfRaw,"exact_replay=true")<>1 then
    Error("R07 delta resume v5 driver: selftest markers");
  fi;
  Print("R07_760_L3_TARGET6_DELTA_RESUME_V5_GHA_DRIVER_PASS ",
        "mode=selftest producer_processes=1 checker_processes=0 ",
        "delta_mutations=12 driver_fixture_mutations=",
        D972R5FixtureMutations," terminals=4 grade=CANDIDATE\n");;
else
  D972R5OwnOutputs:=[D972R5Artifact,D972R5Log,D972R5Timing,
                     D972R5Hashes,D972R5OK];;
  D972R5RemoveOwn(D972R5OwnOutputs);;
  Exec(Concatenation("mkdir -p ",D972R5ShellQuote(D972R5CheckpointDir)));;
  if D972R5ResumePath=fail then
    D972R5CheckpointOutputs:=[];;
    for D972R5J in [9..12] do
      for D972R5R in [1..11] do
        Add(D972R5CheckpointOutputs,D972R5DeltaPath(D972R5J,D972R5R));;
      od;
      Add(D972R5CheckpointOutputs,D972R5JPath(D972R5J));;
    od;
    D972R5RemoveOwn(D972R5CheckpointOutputs);;
    D972R5ResumeArg:="";;
    D972R5ResumeMode:="initial";;
  else
    if not IsExistingFile(D972R5ResumePath) then
      Error("R07 delta resume v5 driver: resume artifact not preseeded");
    fi;
    D972R5ResumeArg:=Concatenation(
      " --resume-checkpoint ",D972R5ShellQuote(D972R5ResumePath));;
    D972R5ResumeMode:="preseeded";;
  fi;
  D972R5FullCommand:=Concatenation(
    "bash -o pipefail -c 'set -e; SECONDS=0; ",
    "timeout --signal=TERM 19800s python3 -u -B ",D972R5Producer,
    " --full --seconds 19200 --max-new-relators ",
    String(D972R5MaxNewRelators)," --checkpoint-dir ",D972R5CheckpointDir,
    " --output ",D972R5Artifact,D972R5ResumeArg,
    " 2>&1 | tee ",D972R5Log,"; producer_elapsed=$SECONDS; ",
    "workflow_margin=$((21600-SECONDS)); ",
    "if [ $workflow_margin -lt 1800 ]; then exit 98; fi; ",
    "producer_log_sha256=$(sha256sum ",D972R5Log,
    " | cut -d \" \" -f1); ",
    "producer_log_bytes=$(wc -c < ",D972R5Log,"); ",
    "receipt_sha256=$(sha256sum ",D972R5Artifact,
    " | cut -d \" \" -f1); ",
    "receipt_bytes=$(wc -c < ",D972R5Artifact,"); ",
    "find ",D972R5CheckpointDir,
    " -maxdepth 1 -type f -print0 | sort -z | xargs -0 -r sha256sum > ",
    D972R5Hashes,"; ",
    "checkpoint_count=$(wc -l < ",D972R5Hashes,"); ",
    "printf \"producer_elapsed=%s\\nworkflow_margin=%s\\n",
    "inner_seconds=19200\\nouter_seconds=19800\\nworkflow_seconds=21600\\n",
    "producer_processes=1\\nchecker_processes=0\\n",
    "grade=CANDIDATE\\ncheckpoint_count=%s\\nresume_mode=%s\\n",
    "max_new_relators=%s\\nproducer_log_sha256=%s\\nproducer_log_bytes=%s\\n",
    "receipt_sha256=%s\\nreceipt_bytes=%s\\n\" ",
    "$producer_elapsed $workflow_margin $checkpoint_count ",D972R5ResumeMode,
    " ",String(D972R5MaxNewRelators),
    " $producer_log_sha256 $producer_log_bytes $receipt_sha256 $receipt_bytes",
    " > ",D972R5Timing,"; ",
    "printf %s D972_R07_DELTA_RESUME_V5_EXIT_ZERO > ",D972R5OK,"'");;
  if D972R5Count(D972R5FullCommand,
       "python3 -u -B search/d972_r07_760_l3_target6_delta_resume_v5.py")<>1 or
     D972R5Count(D972R5FullCommand,"--full")<>1 or
     D972R5Count(D972R5FullCommand,"--seconds 19200")<>1 or
     D972R5Count(D972R5FullCommand,"--max-new-relators")<>1 or
     D972R5Count(D972R5FullCommand,D972R5Checker)<>0 or
     PositionSublist(D972R5FullCommand,"crosscheck/")<>fail then
    Error("R07 delta resume v5 driver: full command shape");
  fi;
  Exec(D972R5FullCommand);;
  if D972R5Read(D972R5OK,"full sentinel")<>
       "D972_R07_DELTA_RESUME_V5_EXIT_ZERO" then
    Error("R07 delta resume v5 driver: producer process");
  fi;
  D972R5Raw:=D972R5Read(D972R5Log,"producer log");;
  D972R5CleanLog(D972R5Raw,"producer");;
  if D972R5Count(D972R5Raw,
       "R07_760_L3_TARGET6_DELTA_RESUME_V5_PRODUCER_PASS")<>1 then
    Error("R07 delta resume v5 driver: producer marker");
  fi;
  D972R5ReceiptRaw:=D972R5Read(D972R5Artifact,"full receipt");;
  D972R5ReceiptSHA:=HexSHA256(D972R5ReceiptRaw);;
  D972R5TerminalCount:=0;; D972R5Terminal:=fail;;
  for D972R5Token in D972R5Terminals do
    D972R5PCount:=D972R5Count(D972R5Raw,
      Concatenation("terminal=",D972R5Token));;
    D972R5JCount:=D972R5Count(D972R5ReceiptRaw,
      Concatenation("\"terminal_token\":\"",D972R5Token,"\""));;
    if D972R5PCount=1 and D972R5JCount=1 then
      D972R5TerminalCount:=D972R5TerminalCount+1;;
      D972R5Terminal:=D972R5Token;;
    elif D972R5PCount<>0 or D972R5JCount<>0 then
      Error("R07 delta resume v5 driver: terminal mismatch");
    fi;
  od;
  if D972R5TerminalCount<>1 then
    Error("R07 delta resume v5 driver: exclusive terminal");
  fi;
  if not D972R5AuditReceipt(
      D972R5ReceiptRaw,D972R5Raw,D972R5Terminal) then
    Error("R07 delta resume v5 driver: structural receipt audit");
  fi;
  D972R5HashRaw:=D972R5ReadMaybeEmpty(
    D972R5Hashes,"checkpoint hash ledger");;
  D972R5HashLines:=Filtered(SplitString(D972R5HashRaw,"\n","\r"),
                            line->Length(line)>0);;
  if D972R5Count(D972R5ReceiptRaw,
       Concatenation("\"checkpoint_manifest_count\":",
         String(Length(D972R5HashLines))))<>1 then
    Error("R07 delta resume v5 driver: checkpoint manifest count binding");
  fi;
  for D972R5HashLine in D972R5HashLines do
    if Length(D972R5HashLine)<68 or D972R5HashLine{[65,66]}<>"  " then
      Error("R07 delta resume v5 driver: hash ledger line");
    fi;
    D972R5CheckpointSHA:=D972R5HashLine{[1..64]};;
    D972R5CheckpointPath:=D972R5HashLine{[67..Length(D972R5HashLine)]};;
    if D972R5Count(D972R5ReceiptRaw,
         Concatenation("\"sha256\":\"",D972R5CheckpointSHA,"\""))<1 or
       D972R5Count(D972R5ReceiptRaw,
         Concatenation("\"path\":\"",D972R5CheckpointPath,"\""))<1 then
      Error("R07 delta resume v5 driver: checkpoint hash binding");
    fi;
  od;
  D972R5TimingRaw:=D972R5Read(D972R5Timing,"timing ledger");;
  if D972R5Count(D972R5TimingRaw,"inner_seconds=19200")<>1 or
     D972R5Count(D972R5TimingRaw,"outer_seconds=19800")<>1 or
     D972R5Count(D972R5TimingRaw,"workflow_seconds=21600")<>1 or
     D972R5Count(D972R5TimingRaw,
       Concatenation("max_new_relators=",String(D972R5MaxNewRelators)))<>1 or
     D972R5Count(D972R5TimingRaw,
       Concatenation("producer_log_sha256=",HexSHA256(D972R5Raw)))<>1 or
     D972R5Count(D972R5TimingRaw,
       Concatenation("producer_log_bytes=",String(Length(D972R5Raw))))<>1 or
     D972R5Count(D972R5TimingRaw,
       Concatenation("receipt_sha256=",D972R5ReceiptSHA))<>1 or
     D972R5Count(D972R5TimingRaw,
       Concatenation("receipt_bytes=",String(Length(D972R5ReceiptRaw))))<>1 or
     D972R5Count(D972R5TimingRaw,"producer_processes=1")<>1 or
     D972R5Count(D972R5TimingRaw,"checker_processes=0")<>1 or
     D972R5Count(D972R5TimingRaw,
       Concatenation("checkpoint_count=",String(Length(D972R5HashLines))))<>1 then
    Error("R07 delta resume v5 driver: timing ledger");
  fi;
  Print("R07_760_L3_TARGET6_DELTA_RESUME_V5_GHA_DRIVER_PASS mode=full ",
        "terminal=",D972R5Terminal," grade=CANDIDATE cross_checked=false ",
        "producer_processes=1 checker_processes=0 checkpoints=",
        Length(D972R5HashLines)," resume_mode=",D972R5ResumeMode,
        " receipt_sha256=",D972R5ReceiptSHA,
        " receipt_bytes=",Length(D972R5ReceiptRaw),
        " log_sha256=",HexSHA256(D972R5Raw),
        " timing_sha256=",HexSHA256(D972R5TimingRaw),
        " checkpoint_hash_ledger_sha256=",HexSHA256(D972R5HashRaw),"\n");;
fi;
