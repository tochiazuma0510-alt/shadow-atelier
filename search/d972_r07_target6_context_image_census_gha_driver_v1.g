#############################################################################
## Task 174 target6 simultaneous-context image census driver v1.
## ASCII only.  Producer and helper-nonshared checker run strictly serially.
#############################################################################

D174Producer :=
  "search/d972_r07_target6_context_image_census_v1.py";;
D174Checker :=
  "crosscheck/check_d972_r07_target6_context_image_census_v1.py";;
D174Fixture :=
  "search/certs/d972_r07_target6_context_image_census_preflight_v1_20260827.json";;
D174Receipt :=
  "ci/out/d972_r07_target6_context_image_census_v1.json";;
D174Verdict :=
  "ci/out/d972_r07_target6_context_image_census_crosscheck_v1.json";;
D174ProducerLog :=
  "ci/out/d972_r07_target6_context_image_census_producer_v1.log";;
D174CheckerLog :=
  "ci/out/d972_r07_target6_context_image_census_checker_v1.log";;
D174Hashes :=
  "ci/out/d972_r07_target6_context_image_census_hashes_v1.txt";;
D174Timing :=
  "ci/out/d972_r07_target6_context_image_census_timing_v1.txt";;
D174OK :=
  "ci/out/d972_r07_target6_context_image_census_v1.ok";;

D174StateCap := 2000000;;
D174SoftSeconds := 9000;;
D174ProducerOuterSeconds := 10200;;
D174CheckerOuterSeconds := 10200;;
D174UploadMarginSeconds := 1200;;
D174WorkflowSeconds := 21600;;

D174ProducerSHA :=
  "c7307c0ed21a4cee0798256fefc3f6b0044b1618d76bc76369ccf7e78c4bbaea";;
D174ProducerBytes := 57948;;
D174CheckerSHA :=
  "821a8ee9369c5d879285b4a5e17ac16051d7a1b1e648709d5e6575059970be0b";;
D174CheckerBytes := 85390;;
D174FixtureSHA :=
  "f96115087a4ddeb26552d7be9caadfda62bfcacc2972b1258d0859df567e4c7d";;
D174FixtureBytes := 5971;;

D174Pins := [
  [D174Producer,D174ProducerSHA,D174ProducerBytes],
  [D174Checker,D174CheckerSHA,D174CheckerBytes],
  [D174Fixture,D174FixtureSHA,D174FixtureBytes],
  ["sol/luna_task_174_r07_target6_context_image_census_v1.md",
   "b0ed2024d0dddb99e6a9407eca4ca732dc8f5791052d6a01b09c0b7126375ec4",6765],
  ["sol/luna_task_174b_r07_target6_context_image_census_repair.md",
   "0a17d240740e403706ffe234778dbd0eb1bb9ab78a0e588e4173943ebf8bb7d7",6294],
  ["sol/proof_r07_full_e4_joint_orbit_selector_v109.md",
   "3224f0be545ac1ffe1d3c674087b30f55c0eb97fda0bd7702eb5f85b768255f0",11228],
  ["sol/proof_r07_context_fibre_dual_correlation_v118.md",
   "6ef2cbf4ebf5ff3466b5eaf21ef4da572684517eb2f6d18c23fd12c8ad3ada3b",8776],
  ["sol/proof_r07_extension_section_context_census_v120.md",
   "118cecd8b972c3fbeb7713597196f5b9760366778ff4d47df7eda4fb3e20f436",7367],
  ["sol/audit_r07_full_e4_orbit_preflight_v7_v119.md",
   "48191c65aac368dd15a1da74c133a1afd5eb9b25eda997ed16ddfa3d01200234",4943],
  ["search/d972_r07_full_e4_joint_orbit_preflight_v7.py",
   "92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed",21918],
  ["crosscheck/check_d972_r07_full_e4_orbit_preflight_v7.py",
   "e3917ec05b95b8996e3a5cec1cc2bfde51c3ed8c6972175fd9be9e1178205c23",12423],
  ["search/certs/d972_r07_full_e4_orbit_preflight_v7_20260827.json",
   "86c6f3a72a3f852a1be7c5323bf72c7ad987377fd5483b6e32528fe263e290ff",45246709],
  ["sol/luna_reply_172_r07_full_e4_orbit_preflight_repair_v7.md",
   "62ab78ecf0f832452d2a8e4e929cbc142188f0ba08c9751cc06e9eec026204e2",4200],
  ["sol/luna_task_168_r07_jennings_legal_coefficients_v1.md",
   "4d85fd8f9ec69a618828c06498aa22922cf5372e21d10ed65280ca2468f5b7f1",7262],
  ["sol/luna_reply_168_r07_jennings_legal_coefficients_v1.md",
   "d22bed5ee8331fd5eb1d84256813699d0985df5a5bdf9a31152fdc448f847940",10692],
  ["search/d972_r07_760_l3_target6_legal_coefficients_v1.py",
   "7db4e174dec13e2f69f4011b09abcc52320699261b164b5eedb18a53fa64b962",57792],
  ["crosscheck/check_d972_r07_760_l3_target6_legal_coefficients_v1.py",
   "a54383185601e8251b7cbac87b6c57f89d3a8df8519cb93014b08a3893825e25",49633],
  ["search/d972_r07_760_l3_target6_legal_coefficients_gha_driver_v1.g",
   "bad7911b0958983aacd541bb682b0f14a2903de02cecfc01043b593b17ab1e16",19176],
  ["search/certs/d972_r07_760_l3_target6_legal_coefficients_preflight_v1_20260827.json",
   "f390f53e6fc840f41009eb31beab519e36b4989b49ac70f9c8f4df7b32776138",6833],
  ["search/d972_r07_760_l3_target6_v1.py",
   "7048e73a02e76df5d49fd359c52d5be70ae99d70aa95ebe74b28c4a18f130fde",53284],
  ["sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md",
   "64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4",11226],
  ["sol/luna_reply_157ee_b345_joint_kernel_qstar_closure.md",
   "53f20c2cb1395b8ff59ee961e1d5a14d55156a488eb6fa49edefed5dd7619eee",4118],
  ["search/d972_b345_joint_kernel_qstar_closure_v1.py",
   "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc",67945],
  ["search/check_d972_b345_joint_kernel_qstar_closure_v2.py",
   "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88",5942],
  ["search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g",
   "8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7",3912],
  ["ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json",
   "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df",2166036],
  ["ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json",
   "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72",231570],
  ["search/d972_b345_seedspan_triple4_v1.py",
   "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29",535219]
];;

D174Terminals := [
  "R07_TARGET6_CONTEXT_IMAGE_CENSUS_COMPLETE",
  "R07_TARGET6_CONTEXT_IMAGE_CENSUS_UNKNOWN_RESOURCE",
  "R07_TARGET6_CONTEXT_IMAGE_CENSUS_INPUT_STOP"
];;

D174Read := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then
    Error("task174 census driver: missing or empty ",label," ",path);
  fi;
  return raw;
end;;

D174Count := function(raw,needle)
  local at,count;
  if not IsString(raw) or not IsString(needle) or Length(needle)=0 then
    Error("task174 census driver: count input");
  fi;
  count:=0;; at:=PositionSublist(raw,needle);;
  while at<>fail do
    count:=count+1;;
    at:=PositionSublist(raw,needle,at);;
  od;
  return count;
end;;

D174ReplaceFirst := function(raw,old,new)
  local at,before,after;
  at:=PositionSublist(raw,old);;
  if at=fail then Error("task174 census driver: mutation needle"); fi;
  before:="";; after:="";;
  if at>1 then before:=raw{[1..at-1]};; fi;
  if at+Length(old)<=Length(raw) then
    after:=raw{[at+Length(old)..Length(raw)]};;
  fi;
  return Concatenation(before,new,after);
end;;

D174Pin := function(row)
  local raw;
  if not IsList(row) or Length(row)<>3 or not IsString(row[1]) or
     not IsString(row[2]) or Length(row[2])<>64 or not IsInt(row[3]) or
     row[3]<=0 then Error("task174 census driver: malformed pin"); fi;
  raw:=D174Read(row[1],"pinned input");;
  if Length(raw)<>row[3] or HexSHA256(raw)<>row[2] then
    Error("task174 census driver: pin drift ",row[1]);
  fi;
  return true;
end;;

D174ShellQuote := function(path)
  if not IsString(path) or Length(path)=0 or
     PositionSublist(path,"\"")<>fail or
     PositionSublist(path,"\n")<>fail or
     PositionSublist(path,"\r")<>fail then
    Error("task174 census driver: unsafe shell path");
  fi;
  return Concatenation("\"",path,"\"");
end;;

D174RejectOwned := function(paths)
  local path;
  if Length(Set(paths))<>Length(paths) then
    Error("task174 census driver: duplicate owned output");
  fi;
  for path in paths do
    if IsExistingFile(path) then
      Error("task174 census driver: pre-existing owned output ",path);
    fi;
  od;
  return true;
end;;

D174CleanLog := function(raw,label)
  local token;
  for token in ["Traceback (most recent call last):", "SyntaxError",
                "RuntimeError", "AssertionError", "Error,", "Reject:",
                " FAIL ", " failed", "Killed"] do
    if D174Count(raw,token)<>0 then
      Error("task174 census driver: forbidden log token ",label," ",token);
    fi;
  od;
  return true;
end;;

D174FixtureAudit := function(raw)
  return D174Count(raw,
    "\"schema\":\"d972-r07-target6-context-image-census/v1\"")=1 and
    D174Count(raw,"\"mode\":\"static_fixture\"")=1 and
    D174Count(raw,"\"status\":\"INPUT_STOP\"")=1 and
    D174Count(raw,Concatenation("\"terminal\":\"",D174Terminals[3],"\""))=1 and
    D174Count(raw,
      "\"reason\":\"LOCAL_EXECUTION_NOT_AUTHORIZED_STATIC_FIXTURE\"")=1 and
    D174Count(raw,"\"state_cap\":2000000")=1 and
    D174Count(raw,"\"soft_deadline_seconds\":9000")=1 and
    D174Count(raw,"\"source\":{\"bytes\":57948,\"path\":\"search/d972_r07_target6_context_image_census_v1.py\",\"sha256\":\"c7307c0ed21a4cee0798256fefc3f6b0044b1618d76bc76369ccf7e78c4bbaea\"}")=1 and
    D174Count(raw,"\"target6_solved\":false")=1 and
    D174Count(raw,"\"fake\":false")=1 and
    D174Count(raw,"\"Ihara_witness\":false")=1;
end;;

D174DriverFixtureSelftest := function()
  local raw,bad,rejected;
  raw:=D174Read(D174Fixture,"static fixture");;
  if not D174FixtureAudit(raw) then
    Error("task174 census driver: static fixture audit");
  fi;
  rejected:=0;;
  bad:=D174ReplaceFirst(raw,"\"target6_solved\":false",
                            "\"target6_solved\":true");;
  if not D174FixtureAudit(bad) then rejected:=rejected+1;; fi;
  bad:=D174ReplaceFirst(raw,"\"status\":\"INPUT_STOP\"",
                            "\"status\":\"COMPLETE\"");;
  if not D174FixtureAudit(bad) then rejected:=rejected+1;; fi;
  bad:=D174ReplaceFirst(raw,D174ProducerSHA,
    "0000000000000000000000000000000000000000000000000000000000000000");;
  if not D174FixtureAudit(bad) then rejected:=rejected+1;; fi;
  if rejected<>3 then
    Error("task174 census driver: fixture mutation count ",rejected);
  fi;
  return rejected;
end;;

D174ReceiptAudit := function(raw,terminal)
  local token,registeredCaps,resourceCapSuffix;
  registeredCaps:=Concatenation(
    "\"registered_caps\":{",
    "\"checker_outer_timeout_seconds\":10200,",
    "\"overflow_safe_integer_arithmetic\":true,",
    "\"producer_outer_timeout_seconds\":10200,",
    "\"raw_stream_count_formula\":\"6441*|Delta_E|\",",
    "\"soft_deadline_seconds\":9000,",
    "\"state_cap\":2000000,",
    "\"total_outer_caps_plus_margin_seconds\":21600,",
    "\"workflow_upload_margin_seconds\":1200}");;
  resourceCapSuffix:=
    "\"soft_deadline_seconds\":9000,\"state_cap\":2000000}";;
  if D174Count(raw,
       "\"schema\":\"d972-r07-target6-context-image-census/v1\"")<>1 or
     D174Count(raw,Concatenation("\"terminal\":\"",terminal,"\""))<>1 or
     D174Count(raw,registeredCaps)<>1 or
     D174Count(raw,"\"producer_outer_timeout_seconds\":10200")<>1 or
     D174Count(raw,"\"checker_outer_timeout_seconds\":10200")<>1 or
     D174Count(raw,"\"workflow_upload_margin_seconds\":1200")<>1 or
     D174Count(raw,
       "\"total_outer_caps_plus_margin_seconds\":21600")<>1 or
     D174Count(raw,"\"state_key_width\":462")=0 or
     D174Count(raw,"\"context_pair_blob_width\":308")=0 or
     D174Count(raw,"\"full_D2_correlation_run\":false")<>1 or
     D174Count(raw,"\"full_correction_orbit_correlation_run\":false")<>1 or
     D174Count(raw,"\"target6_solved\":false")<>1 or
     D174Count(raw,"\"all_seven_solved\":false")<>1 or
     D174Count(raw,"\"cofinal_compatibility_proved\":false")<>1 or
     D174Count(raw,"\"fake\":false")<>1 or
     D174Count(raw,"\"Ihara_witness\":false")<>1 or
     D174Count(raw,"\"GHA_dispatched\":false")<>1 or
     D174Count(raw,"\"self_digest_sha256\":\"")<>1 then
    Error("task174 census driver: receipt fixed boundary gate");
  fi;
  for token in D174Terminals do
    if token<>terminal and
       D174Count(raw,Concatenation("\"terminal\":\"",token,"\""))<>0 then
      Error("task174 census driver: mixed receipt terminals");
    fi;
  od;
  if terminal=D174Terminals[1] then
    if D174Count(raw,"\"state_cap\":2000000")<>2 or
       D174Count(raw,"\"soft_deadline_seconds\":9000")<>2 or
       D174Count(raw,resourceCapSuffix)<>1 or
       D174Count(raw,
         "\"phase\":\"complete\",\"reason\":null,\"soft_deadline_seconds\":9000,\"state_cap\":2000000}")<>1 or
       D174Count(raw,Concatenation(
         "\"status\":\"COMPLETE\",\"terminal\":\"",
         D174Terminals[1],"\""))<>1 or
       D174Count(raw,"\"bounded_prefix_only\":false")<>1 or
       D174Count(raw,"\"order_Delta_E\":null")<>0 or
       D174Count(raw,"\"coordinate_projections\":[")<>1 or
       D174Count(raw,"\"pair_projections\":[")<>1 or
       D174Count(raw,"\"order_Delta3\":27")<>1 or
       D174Count(raw,
         "\"digest_domain\":\"D174-PENDING-POSITIVE-FRONTIER-V1\"")<>1 then
      Error("task174 census driver: COMPLETE receipt gate");
    fi;
  elif terminal=D174Terminals[2] then
    if D174Count(raw,"\"state_cap\":2000000")<>2 or
       D174Count(raw,"\"soft_deadline_seconds\":9000")<>2 or
       D174Count(raw,resourceCapSuffix)<>1 or
       D174Count(raw,
         "\"prefix_replayable_without_order_inference\":true")<>1 or
       D174Count(raw,Concatenation(
         "\"status\":\"UNKNOWN_RESOURCE\",\"terminal\":\"",
         D174Terminals[2],"\""))<>1 or
       D174Count(raw,"\"bounded_prefix_only\":true")<>1 or
       D174Count(raw,"\"order_Delta_E\":null")<>1 or
       D174Count(raw,"\"projections\":null")<>1 or
       D174Count(raw,"\"Delta3_quotient\":null")<>1 or
       D174Count(raw,"\"raw_direct_stream_column_count\":null")<>1 or
       D174Count(raw,"\"seen_state_count\":")<>1 or
       D174Count(raw,"\"discovery_prefix_state_count\":")<>1 or
       D174Count(raw,
         "\"digest_domain\":\"D174-PENDING-POSITIVE-FRONTIER-V1\"")<>1 then
      Error("task174 census driver: UNKNOWN receipt gate");
    fi;
  else
    if D174Count(raw,"\"state_cap\":2000000")<>1 or
       D174Count(raw,"\"soft_deadline_seconds\":9000")<>1 or
       D174Count(raw,resourceCapSuffix)<>0 or
       D174Count(raw,"\"resource\":null")<>1 or
       raw<>D174Read(D174Fixture,"immutable INPUT_STOP fixture") then
      Error("task174 census driver: INPUT_STOP is not static fixture");
    fi;
  fi;
  return true;
end;;

D174TerminalGate := function(producerRaw,receiptRaw,verdictRaw)
  local token,selected,answer,padded;
  selected:=0;; answer:=fail;;
  padded:=Concatenation("\n",producerRaw,"\n");;
  for token in D174Terminals do
    if D174Count(padded,Concatenation("\n",token,"\n"))=1 and
       D174Count(receiptRaw,
         Concatenation("\"terminal\":\"",token,"\""))=1 and
       D174Count(verdictRaw,
         Concatenation("\"terminal\":\"",token,"\""))=1 then
      selected:=selected+1;; answer:=token;;
    fi;
  od;
  if selected<>1 then
    Error("task174 census driver: exactly one allowed terminal");
  fi;
  return answer;
end;;

D174VerdictAudit := function(raw,terminal,receiptRaw)
  local grade,receiptNeedle;
  if terminal=D174Terminals[1] then
    grade:="CROSS_CHECKED";;
  elif terminal=D174Terminals[2] then
    grade:="CROSS_CHECKED_BOUNDED_PREFIX_UNKNOWN";;
  else
    grade:="INPUT_ONLY_NOT_A_CENSUS";;
  fi;
  receiptNeedle:=Concatenation(
    "\"receipt\":{\"bytes\":",String(Length(receiptRaw)),
    ",\"path\":\"",D174Receipt,"\",\"sha256\":\"",
    HexSHA256(receiptRaw),"\"}");;
  if D174Count(raw,
       "\"schema\":\"d972-r07-target6-context-image-census-verdict/v1\"")<>1 or
     D174Count(raw,Concatenation("\"grade\":\"",grade,"\""))<>1 or
     D174Count(raw,receiptNeedle)<>1 or
     D174Count(raw,"\"producer_imported\":false")<>1 or
     D174Count(raw,"\"producer_helpers_shared\":false")<>1 or
     D174Count(raw,"\"target6_solved\":false")<>1 or
     D174Count(raw,"\"fake\":false")<>1 or
     D174Count(raw,"\"Ihara_witness\":false")<>1 or
     D174Count(raw,"\"self_digest_sha256\":\"")<>1 then
    Error("task174 census driver: checker verdict gate");
  fi;
  return grade;
end;;

D174TimingAudit := function(raw)
  if D174Count(raw,"producer_status=0\n")<>1 or
     D174Count(raw,"checker_status=0\n")<>1 or
     D174Count(raw,"producer_outer_seconds=10200\n")<>1 or
     D174Count(raw,"checker_outer_seconds=10200\n")<>1 or
     D174Count(raw,"soft_deadline_seconds=9000\n")<>1 or
     D174Count(raw,"workflow_seconds=21600\n")<>1 or
     D174Count(raw,"upload_margin_required_seconds=1200\n")<>1 or
     D174Count(raw,"producer_processes=1\n")<>1 or
     D174Count(raw,"checker_processes=1\n")<>1 or
     D174Count(raw,"serial=true\n")<>1 then
    Error("task174 census driver: timing gate");
  fi;
  return true;
end;;

D174HashAudit := function(raw,paths)
  local path,fileRaw,needle;
  for path in paths do
    fileRaw:=D174Read(path,"hash-bound output");;
    needle:=Concatenation(HexSHA256(fileRaw),"  ",path);
    if D174Count(raw,needle)<>1 then
      Error("task174 census driver: hash ledger gate ",path);
    fi;
  od;
  return true;
end;;

for D174PinRow in D174Pins do D174Pin(D174PinRow);; od;

D174Self :=
  IsBound(D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_SELFTEST) and
  D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_SELFTEST=true;;
D174Run :=
  IsBound(D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_RUN) and
  D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_RUN=true;;
if D174Self=D174Run then
  Error("task174 census driver: select exactly one mode");
fi;

if IsBound(D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_PYTHON) then
  Error("task174 census driver: obsolete string Python binding rejected");
fi;
D174UsePython3:=false;;
if IsBound(D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_USE_PYTHON3) then
  if not D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_USE_PYTHON3 in
       [true,false] then
    Error("task174 census driver: USE_PYTHON3 boolean");
  fi;
  D174UsePython3:=D972_R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_USE_PYTHON3;;
fi;
D174Python:="python";;
if D174UsePython3 then D174Python:="python3";; fi;
if D174Run and not D174UsePython3 then
  Error("task174 census driver: full mode requires python3 boolean");
fi;

if D174Self then
  D174Tmp:=DirectoryTemporary();;
  if D174Tmp=fail then Error("task174 census driver: no temp directory"); fi;
  D174SelfProducerLog:=Filename(D174Tmp,"producer-selftest.log");;
  D174SelfCheckerLog:=Filename(D174Tmp,"checker-selftest.log");;
  D174SelfOK:=Filename(D174Tmp,"selftest.ok");;
  D174RejectOwned([D174SelfProducerLog,D174SelfCheckerLog,D174SelfOK]);;
  D174DriverMutations:=D174DriverFixtureSelftest();;
  D174SelfCommand:=Concatenation(
    D174Python," -u -B ",D174ShellQuote(D174Producer),
    " --selftest > ",D174ShellQuote(D174SelfProducerLog)," 2>&1 && ",
    D174Python," -u -B ",D174ShellQuote(D174Checker),
    " --selftest > ",D174ShellQuote(D174SelfCheckerLog)," 2>&1 && ",
    "printf %s D174_CONTEXT_CENSUS_V1_SELFTEST_EXIT_ZERO > ",
    D174ShellQuote(D174SelfOK));;
  if D174Count(D174SelfCommand,D174Producer)<>1 or
     D174Count(D174SelfCommand,D174Checker)<>1 then
    Error("task174 census driver: selftest command shape");
  fi;
  Exec(D174SelfCommand);;
  D174SelfProducerRaw:=D174Read(D174SelfProducerLog,"producer selftest log");;
  D174SelfCheckerRaw:=D174Read(D174SelfCheckerLog,"checker selftest log");;
  D174CleanLog(D174SelfProducerRaw,"producer selftest");;
  D174CleanLog(D174SelfCheckerRaw,"checker selftest");;
  if D174Read(D174SelfOK,"selftest sentinel")<>
       "D174_CONTEXT_CENSUS_V1_SELFTEST_EXIT_ZERO" or
     D174Count(D174SelfProducerRaw,
       "D174_TARGET6_CONTEXT_IMAGE_CENSUS_V1_SELFTEST_PASS")<>1 or
     D174Count(D174SelfCheckerRaw,
       "D174_TARGET6_CONTEXT_IMAGE_CENSUS_V1_CHECKER_SELFTEST_PASS")<>1 or
     D174Count(D174SelfCheckerRaw,"\"mutation_count\":20")<>1 or
     D174Count(D174SelfCheckerRaw,"\"linked_image_order\":54")<>1 or
     D174Count(D174SelfCheckerRaw,"\"common_kernel_order\":1")<>1 then
    Error("task174 census driver: selftest markers");
  fi;
  Print("R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_GHA_DRIVER_PASS ",
        "mode=selftest producer_processes=1 checker_processes=1 ",
        "serial=true driver_fixture_mutations=",D174DriverMutations,
        " checker_mutations=20 census_executed=false\n");;
else
  D174Owned:=[D174Receipt,D174Verdict,D174ProducerLog,D174CheckerLog,
              D174Hashes,D174Timing,D174OK];;
  D174RejectOwned(D174Owned);;
  Exec("mkdir -p ci/out");;
  D174FullCommand:=Concatenation(
    "timeout --signal=TERM 21600s bash -o pipefail -c '",
    "set +e; SECONDS=0; checker_status=97; ",
    "timeout --signal=TERM 10200s python3 -u -B ",
    D174ShellQuote(D174Producer)," --run-census --output ",
    D174ShellQuote(D174Receipt)," 2>&1 | tee ",
    D174ShellQuote(D174ProducerLog),"; ",
    "producer_status=${PIPESTATUS[0]}; producer_elapsed=$SECONDS; ",
    "if [ $producer_status -eq 0 ] && [ -s ",D174ShellQuote(D174Receipt),
    " ]; then timeout --signal=TERM 10200s python3 -u -B ",
    D174ShellQuote(D174Checker)," --receipt ",D174ShellQuote(D174Receipt),
    " --verdict ",D174ShellQuote(D174Verdict)," 2>&1 | tee ",
    D174ShellQuote(D174CheckerLog),
    "; checker_status=${PIPESTATUS[0]}; else printf ",
    "\"checker_not_started producer_status=%s\\n\" $producer_status > ",
    D174ShellQuote(D174CheckerLog),"; fi; ",
    "checker_elapsed=$((SECONDS-producer_elapsed)); ",
    "workflow_elapsed=$SECONDS; workflow_margin=$((21600-workflow_elapsed)); ",
    "printf \"producer_status=%s\\nchecker_status=%s\\n",
    "producer_elapsed=%s\\nchecker_elapsed=%s\\nworkflow_elapsed=%s\\n",
    "workflow_margin=%s\\nproducer_outer_seconds=10200\\n",
    "checker_outer_seconds=10200\\nsoft_deadline_seconds=9000\\n",
    "workflow_seconds=21600\\nupload_margin_required_seconds=1200\\n",
    "producer_processes=1\\nchecker_processes=1\\nserial=true\\n\" ",
    "$producer_status $checker_status $producer_elapsed $checker_elapsed ",
    "$workflow_elapsed $workflow_margin > ",D174ShellQuote(D174Timing),"; ",
    "exit_code=0; if [ $producer_status -ne 0 ]; then ",
    "exit_code=$producer_status; elif [ $checker_status -ne 0 ]; then ",
    "exit_code=$checker_status; elif [ $workflow_margin -lt 1200 ]; then ",
    "exit_code=98; else printf %s D174_CONTEXT_CENSUS_V1_EXIT_ZERO > ",
    D174ShellQuote(D174OK),"; fi; : > ",D174ShellQuote(D174Hashes),"; ",
    "for f in ",D174ShellQuote(D174Producer)," ",D174ShellQuote(D174Checker),
    " ",D174ShellQuote(D174Fixture)," ",D174ShellQuote(D174Receipt)," ",
    D174ShellQuote(D174Verdict)," ",D174ShellQuote(D174ProducerLog)," ",
    D174ShellQuote(D174CheckerLog)," ",D174ShellQuote(D174Timing)," ",
    D174ShellQuote(D174OK),"; do if [ -f \"$f\" ]; then ",
    "sha256sum \"$f\" >> ",D174ShellQuote(D174Hashes),
    "; fi; done; hash_status=$?; if [ $hash_status -ne 0 ]; then ",
    "rm -f ",D174ShellQuote(D174OK),"; exit 96; fi; exit $exit_code'");;
  if D174Count(D174FullCommand,
       Concatenation("python3 -u -B ",D174ShellQuote(D174Producer)))<>1 or
     D174Count(D174FullCommand,
       Concatenation("python3 -u -B ",D174ShellQuote(D174Checker)))<>1 or
     D174Count(D174FullCommand,"timeout --signal=TERM 10200s")<>2 or
     D174Count(D174FullCommand,"bash -o pipefail -c")<>1 then
    Error("task174 census driver: full command shape");
  fi;
  Exec(D174FullCommand);;
  if D174Read(D174OK,"full sentinel")<>
       "D174_CONTEXT_CENSUS_V1_EXIT_ZERO" then
    Error("task174 census driver: process failure");
  fi;
  D174ProducerRaw:=D174Read(D174ProducerLog,"producer log");;
  D174CheckerRaw:=D174Read(D174CheckerLog,"checker log");;
  D174ReceiptRaw:=D174Read(D174Receipt,"producer receipt");;
  D174VerdictRaw:=D174Read(D174Verdict,"checker verdict");;
  D174TimingRaw:=D174Read(D174Timing,"timing ledger");;
  D174HashesRaw:=D174Read(D174Hashes,"hash ledger");;
  D174CleanLog(D174ProducerRaw,"producer");;
  D174CleanLog(D174CheckerRaw,"checker");;
  if D174Count(D174ProducerRaw,
       "D174_TARGET6_CONTEXT_IMAGE_CENSUS_V1_PRODUCER_PASS")<>1 or
     D174Count(D174CheckerRaw,
       "D174_TARGET6_CONTEXT_IMAGE_CENSUS_V1_CHECKER_PASS")<>1 then
    Error("task174 census driver: exact process markers");
  fi;
  D174Terminal:=D174TerminalGate(
    D174ProducerRaw,D174ReceiptRaw,D174VerdictRaw);;
  D174ReceiptAudit(D174ReceiptRaw,D174Terminal);;
  D174Grade:=D174VerdictAudit(
    D174VerdictRaw,D174Terminal,D174ReceiptRaw);;
  D174TimingAudit(D174TimingRaw);;
  D174HashAudit(D174HashesRaw,
    [D174Producer,D174Checker,D174Fixture,D174Receipt,D174Verdict,
     D174ProducerLog,D174CheckerLog,D174Timing,D174OK]);;
  Print("R07_TARGET6_CONTEXT_IMAGE_CENSUS_V1_GHA_DRIVER_PASS ",
        "mode=full terminal=",D174Terminal," grade=",D174Grade,
        " producer_processes=1 checker_processes=1 serial=true ",
        "receipt_sha256=",HexSHA256(D174ReceiptRaw),
        " receipt_bytes=",Length(D174ReceiptRaw),
        " verdict_sha256=",HexSHA256(D174VerdictRaw),
        " timing_sha256=",HexSHA256(D174TimingRaw),
        " bounded_unknown_remains_unknown=",D174Terminal=D174Terminals[2],
        "\n");;
fi;
