#############################################################################
## R07 task304 serial driver. ASCII only.
#############################################################################
if not IsBound(D307Mode) then Error("task304 MODE required"); fi;
if D307Mode<>"SELFTEST" and D307Mode<>"PRODUCTION" then Error("task304 MODE"); fi;
D307Producer:="search/d972_r07_joint_slice_kernel_general_v9.py";;
D307Checker:="crosscheck/check_d972_r07_joint_slice_kernel_general_v9.py";;
D307Fixture:="search/certs/d972_r07_joint_slice_kernel_general_selftest_v9_20260828.json";;
D307Receipt:="ci/out/d972_r07_joint_slice_kernel_general_v9.json";;
D307Verdict:="ci/out/d972_r07_joint_slice_kernel_general_v9.verdict.json";;
D307PLog:="ci/out/d972_r07_joint_slice_kernel_general_v9.producer.log";;
D307CLog:="ci/out/d972_r07_joint_slice_kernel_general_v9.checker.log";;
D307Sh:="ci/out/d972_r07_joint_slice_kernel_general_v9.sh";;
D307OK:="ci/out/d972_r07_joint_slice_kernel_general_v9.ok";;
D307Pins:=[[D307Producer,13001,"1e38453980eac5dc4b3b8edcb63235a7de60684393491a5bc01cdd356f4d103a"],[D307Checker,24995,"5cadaeb180e2058466a9a97bb54c5b98393e2e4096035f4e64b69a65d0da8121"],[D307Fixture,10356,"6a866e980422afc405c4d6b574c06cee8ca8ee6792b536a006e4d104724c7cd"]];;
D307Read:=function(path) local x; x:=StringFile(path); if x=fail or Length(x)=0 then Error("task304 missing ",path); fi; return x; end;;
D307Pin:=function(row) local x; if row[2]=0 then Error("task304 unresolved pin ",row[1]); fi; x:=D307Read(row[1]); if Length(x)<>row[2] or HexSHA256(x)<>row[3] then Error("task304 pin drift ",row[1]); fi; end;;
for D307PinRow in D307Pins do D307Pin(D307PinRow); od;
if IsExistingFile(D307Receipt) or IsExistingFile(D307Verdict) or IsExistingFile(D307PLog) or IsExistingFile(D307CLog) or IsExistingFile(D307Sh) or IsExistingFile(D307OK) then Error("task304 stale output"); fi;
D307S:=OutputTextFile(D307Sh,false);; SetPrintFormattingStatus(D307S,false);;
PrintTo(D307S,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
if D307Mode="SELFTEST" then
  ## Both SELFTEST success terminals normalize to the documented common value SELFTEST_COMPLETE.
  PrintTo(D307S,"python3 -u -B \"",D307Producer,"\" --mode SELFTEST --fixture \"",D307Fixture,"\" --output \"",D307Receipt,"\" > \"",D307PLog,"\" 2>&1 || { cat \"",D307PLog,"\"; exit 1; }\n");
  PrintTo(D307S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V9_PRODUCER_SELFTEST_PASS' \"",D307PLog,"\")\" = \"1\" || { cat \"",D307PLog,"\"; exit 1; }\n");
  PrintTo(D307S,"test -s \"",D307Receipt,"\"\ntest -s \"",D307PLog,"\"\n");
  PrintTo(D307S,"python3 -u -B \"",D307Checker,"\" --mode SELFTEST --fixture \"",D307Fixture,"\" --receipt \"",D307Receipt,"\" --output \"",D307Verdict,"\" > \"",D307CLog,"\" 2>&1 || { cat \"",D307CLog,"\"; exit 1; }\n");
  PrintTo(D307S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V9_CHECKER_SELFTEST_PASS mutation_attempted=19 mutation_rejected=19' \"",D307CLog,"\")\" = \"1\" || { cat \"",D307CLog,"\"; exit 1; }\n");
  PrintTo(D307S,"test -s \"",D307Verdict,"\"\ntest -s \"",D307CLog,"\"\nD307Pterm=SELFTEST_COMPLETE\nD307Cterm=SELFTEST_COMPLETE\ntest -n \"$D307Pterm\"\ntest -n \"$D307Cterm\"\ntest \"$D307Pterm\" = \"$D307Cterm\"\n");
else
  PrintTo(D307S,"python3 -u -B \"",D307Producer,"\" --mode PRODUCTION --output \"",D307Receipt,"\" > \"",D307PLog,"\" 2>&1 || { cat \"",D307PLog,"\"; exit 1; }\n");
  PrintTo(D307S,"python3 -u -B \"",D307Checker,"\" --mode PRODUCTION --receipt \"",D307Receipt,"\" --output \"",D307Verdict,"\" > \"",D307CLog,"\" 2>&1 || { cat \"",D307CLog,"\"; exit 1; }\n");
  PrintTo(D307S,"test -s \"",D307Receipt,"\"\ntest -s \"",D307PLog,"\"\ntest -s \"",D307Verdict,"\"\ntest -s \"",D307CLog,"\"\n");
  PrintTo(D307S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V9_PRODUCER_TERMINAL STATIC_BLOCKED:actual typed matrices are not staged' \"",D307PLog,"\")\" = \"1\" || { cat \"",D307PLog,"\"; exit 1; }\n");
  PrintTo(D307S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V9_CHECKER_TERMINAL STATIC_BLOCKED:actual typed matrices are not staged' \"",D307CLog,"\")\" = \"1\" || { cat \"",D307CLog,"\"; exit 1; }\n");
  PrintTo(D307S,"D307Pterm=$(sed -n 's/^R07_JOINT_SLICE_KERNEL_GENERAL_V9_PRODUCER_TERMINAL //p' \"",D307PLog,"\")\nD307Cterm=$(sed -n 's/^R07_JOINT_SLICE_KERNEL_GENERAL_V9_CHECKER_TERMINAL //p' \"",D307CLog,"\")\ntest -n \"$D307Pterm\"\ntest -n \"$D307Cterm\"\ntest \"$D307Pterm\" = \"$D307Cterm\"\n");
fi;
PrintTo(D307S,"printf 'R07_JOINT_SLICE_KERNEL_GENERAL_V9_OK\\n' > \"",D307OK,"\"\ntest \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V9_OK' \"",D307OK,"\")\" = \"1\"\n"); CloseStream(D307S);;
Exec("bash ci/out/d972_r07_joint_slice_kernel_general_v9.sh");
if not IsExistingFile(D307OK) then Error("task304 missing completion"); fi;
Print("R07_JOINT_SLICE_KERNEL_GENERAL_V9_DRIVER_PASS\\n");

