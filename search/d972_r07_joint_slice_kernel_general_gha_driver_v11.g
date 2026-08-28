#############################################################################
## R07 task324 serial driver. ASCII only.
#############################################################################
if not IsBound(D307Mode) then Error("task324 MODE required"); fi;
if D307Mode<>"SELFTEST" and D307Mode<>"PRODUCTION" then Error("task324 MODE"); fi;
D324Producer:="search/d972_r07_joint_slice_kernel_general_v11.py";;
D324Checker:="crosscheck/check_d972_r07_joint_slice_kernel_general_v11.py";;
D324Fixture:="search/certs/d972_r07_joint_slice_kernel_general_selftest_v11_20260828.json";;
D324Receipt:="ci/out/d972_r07_joint_slice_kernel_general_v11.json";;
D324Verdict:="ci/out/d972_r07_joint_slice_kernel_general_v11.verdict.json";;
D324PLog:="ci/out/d972_r07_joint_slice_kernel_general_v11.producer.log";;
D324CLog:="ci/out/d972_r07_joint_slice_kernel_general_v11.checker.log";;
D324Sh:="ci/out/d972_r07_joint_slice_kernel_general_v11.sh";;
D324OK:="ci/out/d972_r07_joint_slice_kernel_general_v11.ok";;
D324Pins:=[
[D324Producer,48381,"52fa8eb2dc784012f087b0790661f94e446746253e6fe0d8a28dea5a49db84b8"],
[D324Checker,52662,"c22fab29394e6d4fb2a7c6e0042547c5adaba9308794d9e2c654757e24176f26"],
[D324Fixture,12964,"cab24a5e6ddd7812094b920bffd7688564092a3c9b718484bf3f887cf59d2058"]
];;
D324Read:=function(path) local value; value:=StringFile(path); if value=fail or Length(value)=0 then Error("task324 missing ",path); fi; return value; end;;
D324Pin:=function(row) local value; value:=D324Read(row[1]); if Length(value)<>row[2] or HexSHA256(value)<>row[3] then Error("task324 pin drift ",row[1]); fi; end;;
for D324PinRow in D324Pins do D324Pin(D324PinRow); od;
D324Stale:=[
"ci/out/d972_r07_joint_slice_kernel_general_v7.json",
"ci/out/d972_r07_joint_slice_kernel_general_v7.verdict.json",
"ci/out/d972_r07_joint_slice_kernel_general_v7.producer.log",
"ci/out/d972_r07_joint_slice_kernel_general_v7.checker.log",
"ci/out/d972_r07_joint_slice_kernel_general_v7.sh",
"ci/out/d972_r07_joint_slice_kernel_general_v7.ok",
"ci/out/d972_r07_joint_slice_kernel_general_v8.json",
"ci/out/d972_r07_joint_slice_kernel_general_v8.verdict.json",
"ci/out/d972_r07_joint_slice_kernel_general_v8.producer.log",
"ci/out/d972_r07_joint_slice_kernel_general_v8.checker.log",
"ci/out/d972_r07_joint_slice_kernel_general_v8.sh",
"ci/out/d972_r07_joint_slice_kernel_general_v8.ok",
"ci/out/d972_r07_joint_slice_kernel_general_v9.json",
"ci/out/d972_r07_joint_slice_kernel_general_v9.verdict.json",
"ci/out/d972_r07_joint_slice_kernel_general_v9.producer.log",
"ci/out/d972_r07_joint_slice_kernel_general_v9.checker.log",
"ci/out/d972_r07_joint_slice_kernel_general_v9.sh",
"ci/out/d972_r07_joint_slice_kernel_general_v9.ok",
"ci/out/d972_r07_joint_slice_kernel_general_v10.json",
"ci/out/d972_r07_joint_slice_kernel_general_v10.verdict.json",
"ci/out/d972_r07_joint_slice_kernel_general_v10.producer.log",
"ci/out/d972_r07_joint_slice_kernel_general_v10.checker.log",
"ci/out/d972_r07_joint_slice_kernel_general_v10.sh",
"ci/out/d972_r07_joint_slice_kernel_general_v10.ok",
D324Receipt,D324Verdict,D324PLog,D324CLog,D324Sh,D324OK
];;
for D324StalePath in D324Stale do
  if IsExistingFile(D324StalePath) then Error("task324 stale output ",D324StalePath); fi;
od;
D324S:=OutputTextFile(D324Sh,false);; SetPrintFormattingStatus(D324S,false);;
PrintTo(D324S,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
if D307Mode="SELFTEST" then
  PrintTo(D324S,"python3 -u -B \"",D324Producer,"\" --mode SELFTEST --fixture \"",D324Fixture,"\" --output \"",D324Receipt,"\" > \"",D324PLog,"\" 2>&1 || { cat \"",D324PLog,"\"; exit 1; }\n");
  PrintTo(D324S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V11_PRODUCER_SELFTEST_PASS' \"",D324PLog,"\")\" = \"1\" || { cat \"",D324PLog,"\"; exit 1; }\n");
  PrintTo(D324S,"test -s \"",D324Receipt,"\"\ntest -s \"",D324PLog,"\"\n");
  PrintTo(D324S,"test \"$(grep -Eo '\"self_digest_sha256\":\"[0-9a-f]{64}\"' \"",D324Receipt,"\" | wc -l)\" = \"1\"\n");
  PrintTo(D324S,"python3 -u -B \"",D324Checker,"\" --mode SELFTEST --fixture \"",D324Fixture,"\" --receipt \"",D324Receipt,"\" --output \"",D324Verdict,"\" > \"",D324CLog,"\" 2>&1 || { cat \"",D324CLog,"\"; exit 1; }\n");
  PrintTo(D324S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V11_CHECKER_SELFTEST_PASS mutation_attempted=19 mutation_rejected=19' \"",D324CLog,"\")\" = \"1\" || { cat \"",D324CLog,"\"; exit 1; }\n");
  PrintTo(D324S,"test -s \"",D324Verdict,"\"\ntest -s \"",D324CLog,"\"\n");
  PrintTo(D324S,"test \"$(grep -Eo '\"verdict_digest_sha256\":\"[0-9a-f]{64}\"' \"",D324Verdict,"\" | wc -l)\" = \"1\"\n");
  PrintTo(D324S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V11_PRODUCER_TERMINAL SELFTEST_COMPLETE' \"",D324PLog,"\")\" = \"1\" || { cat \"",D324PLog,"\"; exit 1; }\n");
  PrintTo(D324S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V11_CHECKER_TERMINAL SELFTEST_COMPLETE' \"",D324CLog,"\")\" = \"1\" || { cat \"",D324CLog,"\"; exit 1; }\n");
  PrintTo(D324S,"D324Pterm=$(sed -n 's/^R07_JOINT_SLICE_KERNEL_GENERAL_V11_PRODUCER_TERMINAL //p' \"",D324PLog,"\")\nD324Cterm=$(sed -n 's/^R07_JOINT_SLICE_KERNEL_GENERAL_V11_CHECKER_TERMINAL //p' \"",D324CLog,"\")\ntest -n \"$D324Pterm\"\ntest -n \"$D324Cterm\"\ntest \"$D324Pterm\" = \"$D324Cterm\"\n");
else
  PrintTo(D324S,"python3 -u -B \"",D324Producer,"\" --mode PRODUCTION --output \"",D324Receipt,"\" > \"",D324PLog,"\" 2>&1 || { cat \"",D324PLog,"\"; exit 1; }\n");
  PrintTo(D324S,"test -s \"",D324Receipt,"\"\ntest -s \"",D324PLog,"\"\n");
  PrintTo(D324S,"test \"$(grep -Eo '\"self_digest_sha256\":\"[0-9a-f]{64}\"' \"",D324Receipt,"\" | wc -l)\" = \"1\"\n");
  PrintTo(D324S,"python3 -u -B \"",D324Checker,"\" --mode PRODUCTION --receipt \"",D324Receipt,"\" --output \"",D324Verdict,"\" > \"",D324CLog,"\" 2>&1 || { cat \"",D324CLog,"\"; exit 1; }\n");
  PrintTo(D324S,"test -s \"",D324Verdict,"\"\ntest -s \"",D324CLog,"\"\n");
  PrintTo(D324S,"test \"$(grep -Eo '\"verdict_digest_sha256\":\"[0-9a-f]{64}\"' \"",D324Verdict,"\" | wc -l)\" = \"1\"\n");
  PrintTo(D324S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V11_PRODUCER_TERMINAL STATIC_BLOCKED:actual typed matrices are not staged' \"",D324PLog,"\")\" = \"1\" || { cat \"",D324PLog,"\"; exit 1; }\n");
  PrintTo(D324S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V11_CHECKER_TERMINAL STATIC_BLOCKED:actual typed matrices are not staged' \"",D324CLog,"\")\" = \"1\" || { cat \"",D324CLog,"\"; exit 1; }\n");
  PrintTo(D324S,"D324Pterm=$(sed -n 's/^R07_JOINT_SLICE_KERNEL_GENERAL_V11_PRODUCER_TERMINAL //p' \"",D324PLog,"\")\nD324Cterm=$(sed -n 's/^R07_JOINT_SLICE_KERNEL_GENERAL_V11_CHECKER_TERMINAL //p' \"",D324CLog,"\")\ntest -n \"$D324Pterm\"\ntest -n \"$D324Cterm\"\ntest \"$D324Pterm\" = \"$D324Cterm\"\n");
fi;
PrintTo(D324S,"printf 'R07_JOINT_SLICE_KERNEL_GENERAL_V11_OK\\n' > \"",D324OK,"\"\n"); CloseStream(D324S);;
Exec("bash ci/out/d972_r07_joint_slice_kernel_general_v11.sh");
if not IsExistingFile(D324OK) or Length(D324Read(D324OK))=0 then Error("task324 missing completion"); fi;
Print("R07_JOINT_SLICE_KERNEL_GENERAL_V11_DRIVER_PASS\n");
