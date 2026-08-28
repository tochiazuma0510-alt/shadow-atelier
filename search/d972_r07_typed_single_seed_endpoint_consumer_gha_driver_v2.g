#############################################################################
## Task227 typed single-seed endpoint consumer v2.
## Serial fail-closed GAP driver; no workflow edits.
#############################################################################
D227ModeVariable:="D972_R07_TYPED_SINGLE_SEED_ENDPOINT_CONSUMER_V2_MODE";;
if not IsBound(D972_R07_TYPED_SINGLE_SEED_ENDPOINT_CONSUMER_V2_MODE) then
  Error("task227: supply quoted mode"); fi;
D227Mode:=D972_R07_TYPED_SINGLE_SEED_ENDPOINT_CONSUMER_V2_MODE;;
if not IsString(D227Mode) or not D227Mode in ["SELFTEST","PRODUCTION"] then
  Error("task227: mode"); fi;
D227P:="search/d972_r07_typed_single_seed_endpoint_consumer_v2.py";;
D227C:="crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py";;
D227F:="search/certs/d972_r07_typed_single_seed_endpoint_consumer_selftest_v2_20260828.json";;
D227R:="ci/out/d972_r07_typed_single_seed_endpoint_consumer_v2.json";;
D227V:="ci/out/d972_r07_typed_single_seed_endpoint_consumer_v2.verdict.json";;
D227PL:="ci/out/d972_r07_typed_single_seed_endpoint_consumer_v2.producer.log";;
D227CL:="ci/out/d972_r07_typed_single_seed_endpoint_consumer_v2.checker.log";;
D227S:="ci/out/d972_r07_typed_single_seed_endpoint_consumer_v2.sh";;
D227OK:="ci/out/d972_r07_typed_single_seed_endpoint_consumer_v2.ok";;
D227Sentinel:="R07_TYPED_SINGLE_SEED_ENDPOINT_CONSUMER_V2_SENTINEL";;
D227Selftest:="R07_TYPED_SINGLE_SEED_ENDPOINT_CONSUMER_V2_SELFTEST_PASS";;
D227Read:=function(path,label)
  local raw; raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task227: missing ",label); fi;
  return raw;
end;;
D227Pin:=function(row)
  local raw; raw:=D227Read(row[1],"pin");;
  if Length(raw)<>row[3] or HexSHA256(raw)<>row[2] then
    Error("task227: pin drift ",row[1]); fi;
end;;
D227Pins:=[
  [D227P,"755ba97e55266bcdb51796cc1a89a562efa782db48475d0e3479e82e325cde8e",47135],
  [D227C,"32b667988ff90c94329f4ed57d1eaf91256f0987b43f8f9855988dc973b23c86",34175],
  [D227F,"d4130b99d62eb7f2dd0a5ee887881e68798637cb4945747f47f883f4961bf911",594]
];;
for D227PinRow in D227Pins do D227Pin(D227PinRow);; od;
for D227Path in [D227R,D227V,D227PL,D227CL,D227S,D227OK] do
  if IsExistingFile(D227Path) then Error("task227: stale output ",D227Path); fi;
od;
if not IsExistingFile(D227P) or not IsExistingFile(D227C) or
   not IsExistingFile(D227F) then Error("task227: missing source/fixture"); fi;
if not IsDirectoryPath("ci/out") then
  if CreateDir("ci/out")=fail then Error("task227: cannot create ci/out"); fi;
fi;
if not IsDirectoryPath("ci/out") then Error("task227: ci/out is not a directory"); fi;
D227Stream:=OutputTextFile(D227S,false);;
if D227Stream=fail then Error("task227: cannot open command script"); fi;
SetPrintFormattingStatus(D227Stream,false);
PrintTo(D227Stream,"set -euo pipefail\n");
PrintTo(D227Stream,"printf 'D227_GHA_ESTIMATE wall_seconds=21600 rss_bytes=6442450944\\n'\n");
if D227Mode="SELFTEST" then
  PrintTo(D227Stream,"python3 -u -B ",D227P," --selftest --fixture ",D227F,
    " --output ",D227R," > ",D227PL," 2>&1 || { cat ",D227PL,"; exit 1; }\n");
  PrintTo(D227Stream,"grep -Fxc 'D227_PRODUCER_TERMINAL ",D227Selftest,
    "' ",D227PL," | grep -qx 1\n");
  PrintTo(D227Stream,"python3 -u -B ",D227C," ",D227R,
    " --selftest --fixture ",D227F," --verdict ",D227V,
    " > ",D227CL," 2>&1 || { cat ",D227CL,"; exit 1; }\n");
  PrintTo(D227Stream,"grep -Fxc 'D227_CHECKER_TERMINAL ",D227Selftest,
    "' ",D227CL," | grep -qx 1\n");
else
  PrintTo(D227Stream,"python3 -u -B ",D227P," --task226 ",
    "ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.json",
    " --task226-verdict ",
    "ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.verdict.json",
    " --task226-binding ",
    "ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.binding.json",
    " --output ",D227R," > ",D227PL," 2>&1 || { cat ",D227PL,"; exit 1; }\n");
  PrintTo(D227Stream,"grep -Ec '^D227_PRODUCER_TERMINAL (PROJECTED_MEMBER_SEED|PROJECTED_NONMEMBER_DUAL|UNKNOWN_INPUT|UNKNOWN_RESOURCE)$' ",D227PL," | grep -qx 1\n");
  PrintTo(D227Stream,"python3 -u -B ",D227C," ",D227R,
    " --task226 ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.json",
    " --task226-verdict ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.verdict.json",
    " --task226-binding ci/in/d972_r07_actual_two_word_endpoint_specializer_v2.binding.json",
    " --verdict ",D227V," > ",D227CL," 2>&1 || { cat ",D227CL,"; exit 1; }\n");
  PrintTo(D227Stream,"grep -Ec '^D227_CHECKER_TERMINAL (PROJECTED_MEMBER_SEED|PROJECTED_NONMEMBER_DUAL|UNKNOWN_INPUT|UNKNOWN_RESOURCE)' ",D227CL," | grep -qx 1\n");
  PrintTo(D227Stream,"p=$(sed -n 's/^D227_PRODUCER_TERMINAL //p' ",D227PL," | head -n 1)\n");
  PrintTo(D227Stream,"c=$(sed -n 's/^D227_CHECKER_TERMINAL //p' ",D227CL," | head -n 1 | cut -d' ' -f1)\n");
  PrintTo(D227Stream,"test \"$p\" = \"$c\"\n");
fi;
PrintTo(D227Stream,"test -s ",D227R,"\n");
PrintTo(D227Stream,"printf '%s' '",D227Sentinel,"_",D227Mode,"' > ",D227OK,"\n");
CloseStream(D227Stream);; Exec(Concatenation("bash ",D227S));
if StringFile(D227OK)<>Concatenation(D227Sentinel,"_",D227Mode) then
  Error("task227: sentinel"); fi;
Print("D227_DRIVER_PASS mode=",D227Mode,"\n");
