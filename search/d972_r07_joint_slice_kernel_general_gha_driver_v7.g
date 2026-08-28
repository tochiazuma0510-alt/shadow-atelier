#############################################################################
## R07 task304 serial driver. ASCII only.
#############################################################################
if not IsBound(D307Mode) then Error("task304 MODE required"); fi;
if D307Mode<>"SELFTEST" and D307Mode<>"PRODUCTION" then Error("task304 MODE"); fi;
D307Producer:="search/d972_r07_joint_slice_kernel_general_v7.py";;
D307Checker:="crosscheck/check_d972_r07_joint_slice_kernel_general_v7.py";;
D307Fixture:="search/certs/d972_r07_joint_slice_kernel_general_selftest_v7_20260828.json";;
D307Receipt:="ci/out/d972_r07_joint_slice_kernel_general_v7.json";;
D307Verdict:="ci/out/d972_r07_joint_slice_kernel_general_v7.verdict.json";;
D307PLog:="ci/out/d972_r07_joint_slice_kernel_general_v7.producer.log";;
D307CLog:="ci/out/d972_r07_joint_slice_kernel_general_v7.checker.log";;
D307Sh:="ci/out/d972_r07_joint_slice_kernel_general_v7.sh";;
D307OK:="ci/out/d972_r07_joint_slice_kernel_general_v7.ok";;
D307Pins:=[[D307Producer,11670,"279ab542b22ea6756fee48b7da8c2d9e0142e2489def80b6d071e9aed67ff1b6"],[D307Checker,23677,"148ddb801939f2263421e1cfb1e942695ad36eba74d2cb3c27c4e9ed30e3aa35"],[D307Fixture,10317,"c4d616b758f83379307f5778cbb46794d7aa0e4b651d6072163ce9a4c34de4e4"]];;
D307Read:=function(path) local x; x:=StringFile(path); if x=fail or Length(x)=0 then Error("task304 missing ",path); fi; return x; end;;
D307Pin:=function(row) local x; if row[2]=0 then Error("task304 unresolved pin ",row[1]); fi; x:=D307Read(row[1]); if Length(x)<>row[2] or HexSHA256(x)<>row[3] then Error("task304 pin drift ",row[1]); fi; end;;
for D307PinRow in D307Pins do D307Pin(D307PinRow); od;
if IsExistingFile(D307Receipt) or IsExistingFile(D307Verdict) or IsExistingFile(D307PLog) or IsExistingFile(D307CLog) or IsExistingFile(D307Sh) or IsExistingFile(D307OK) then Error("task304 stale output"); fi;
D307S:=OutputTextFile(D307Sh,false);; SetPrintFormattingStatus(D307S,false);;
PrintTo(D307S,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
if D307Mode="SELFTEST" then
  ## Both SELFTEST success terminals normalize to the documented common value SELFTEST_COMPLETE.
  PrintTo(D307S,"python3 -u -B \"",D307Producer,"\" --mode SELFTEST --fixture \"",D307Fixture,"\" --output \"",D307Receipt,"\" > \"",D307PLog,"\" 2>&1 || { cat \"",D307PLog,"\"; exit 1; }\n");
  PrintTo(D307S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V7_PRODUCER_SELFTEST_PASS' \"",D307PLog,"\")\" = \"1\" || { cat \"",D307PLog,"\"; exit 1; }\n");
  PrintTo(D307S,"test -s \"",D307Receipt,"\"\ntest -s \"",D307PLog,"\"\n");
  PrintTo(D307S,"python3 -u -B \"",D307Checker,"\" --mode SELFTEST --fixture \"",D307Fixture,"\" --receipt \"",D307Receipt,"\" --output \"",D307Verdict,"\" > \"",D307CLog,"\" 2>&1 || { cat \"",D307CLog,"\"; exit 1; }\n");
  PrintTo(D307S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V7_CHECKER_SELFTEST_PASS mutation_attempted=19 mutation_rejected=19' \"",D307CLog,"\")\" = \"1\" || { cat \"",D307CLog,"\"; exit 1; }\n");
  PrintTo(D307S,"test -s \"",D307Verdict,"\"\ntest -s \"",D307CLog,"\"\nD307Pterm=SELFTEST_COMPLETE\nD307Cterm=SELFTEST_COMPLETE\ntest -n \"$D307Pterm\"\ntest -n \"$D307Cterm\"\ntest \"$D307Pterm\" = \"$D307Cterm\"\n");
else
  PrintTo(D307S,"python3 -u -B \"",D307Producer,"\" --mode PRODUCTION --output \"",D307Receipt,"\" > \"",D307PLog,"\" 2>&1 || { cat \"",D307PLog,"\"; exit 1; }\n");
  PrintTo(D307S,"python3 -u -B \"",D307Checker,"\" --mode PRODUCTION --receipt \"",D307Receipt,"\" --output \"",D307Verdict,"\" > \"",D307CLog,"\" 2>&1 || { cat \"",D307CLog,"\"; exit 1; }\n");
  PrintTo(D307S,"test -s \"",D307Receipt,"\"\ntest -s \"",D307PLog,"\"\ntest -s \"",D307Verdict,"\"\ntest -s \"",D307CLog,"\"\n");
  PrintTo(D307S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V7_PRODUCER_TERMINAL STATIC_BLOCKED:actual typed matrices are not staged' \"",D307PLog,"\")\" = \"1\" || { cat \"",D307PLog,"\"; exit 1; }\n");
  PrintTo(D307S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V7_CHECKER_TERMINAL STATIC_BLOCKED:actual typed matrices are not staged' \"",D307CLog,"\")\" = \"1\" || { cat \"",D307CLog,"\"; exit 1; }\n");
  PrintTo(D307S,"D307Pterm=$(sed -n 's/^R07_JOINT_SLICE_KERNEL_GENERAL_V7_PRODUCER_TERMINAL //p' \"",D307PLog,"\")\nD307Cterm=$(sed -n 's/^R07_JOINT_SLICE_KERNEL_GENERAL_V7_CHECKER_TERMINAL //p' \"",D307CLog,"\")\ntest -n \"$D307Pterm\"\ntest -n \"$D307Cterm\"\ntest \"$D307Pterm\" = \"$D307Cterm\"\n");
fi;
PrintTo(D307S,"printf 'R07_JOINT_SLICE_KERNEL_GENERAL_V7_OK\\n' > \"",D307OK,"\"\ntest \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V7_OK' \"",D307OK,"\")\" = \"1\"\n"); CloseStream(D307S);;
Exec("bash ci/out/d972_r07_joint_slice_kernel_general_v7.sh");
if not IsExistingFile(D307OK) then Error("task304 missing completion"); fi;
Print("R07_JOINT_SLICE_KERNEL_GENERAL_V7_DRIVER_PASS\\n");

