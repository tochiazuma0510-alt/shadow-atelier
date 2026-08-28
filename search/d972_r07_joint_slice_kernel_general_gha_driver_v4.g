#############################################################################
## R07 task296 serial driver. ASCII only.
#############################################################################
if not IsBound(D296Mode) then Error("task296 MODE required"); fi;
if D296Mode<>"SELFTEST" and D296Mode<>"PRODUCTION" then Error("task296 MODE"); fi;
D296Producer:="search/d972_r07_joint_slice_kernel_general_v4.py";;
D296Checker:="crosscheck/check_d972_r07_joint_slice_kernel_general_v4.py";;
D296Fixture:="search/certs/d972_r07_joint_slice_kernel_general_selftest_v4_20260828.json";;
D296Receipt:="ci/out/d972_r07_joint_slice_kernel_general_v4.json";;
D296Verdict:="ci/out/d972_r07_joint_slice_kernel_general_v4.verdict.json";;
D296PLog:="ci/out/d972_r07_joint_slice_kernel_general_v4.producer.log";;
D296CLog:="ci/out/d972_r07_joint_slice_kernel_general_v4.checker.log";;
D296Sh:="ci/out/d972_r07_joint_slice_kernel_general_v4.sh";;
D296OK:="ci/out/d972_r07_joint_slice_kernel_general_v4.ok";;
D296Pins:=[[D296Producer,10673,"319f8df5c639387667cbf153ce0549dce973ebfa8fcd504910ca668277f5dbf4"],[D296Checker,20071,"39a7e1f1844b66440a0bea942253de8574987d7fd7eb7337eae42cd858a3a492"],[D296Fixture,10311,"a352c9e588894f1195e58066992fa3677cad77c0f4739303fb8abbcc2dca34b2"]];;
D296Read:=function(path) local x; x:=StringFile(path); if x=fail or Length(x)=0 then Error("task296 missing ",path); fi; return x; end;;
D296Pin:=function(row) local x; if row[2]=0 then Error("task296 unresolved pin ",row[1]); fi; x:=D296Read(row[1]); if Length(x)<>row[2] or HexSHA256(x)<>row[3] then Error("task296 pin drift ",row[1]); fi; end;;
for D296PinRow in D296Pins do D296Pin(D296PinRow); od;
if IsExistingFile(D296Receipt) or IsExistingFile(D296Verdict) or IsExistingFile(D296PLog) or IsExistingFile(D296CLog) or IsExistingFile(D296Sh) or IsExistingFile(D296OK) then Error("task296 stale output"); fi;
D296S:=OutputTextFile(D296Sh,false);; SetPrintFormattingStatus(D296S,false);;
PrintTo(D296S,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
if D296Mode="SELFTEST" then
  PrintTo(D296S,"python3 -u -B ",D296Producer," --mode SELFTEST --fixture ",D296Fixture," --output ",D296Receipt," > ",D296PLog," 2>&1 || { cat ",D296PLog,"; exit 1; }\n");
  PrintTo(D296S,"grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V4_PRODUCER_SELFTEST_PASS' ",D296PLog," >/dev/null || { cat ",D296PLog,"; exit 1; }\n");
  PrintTo(D296S,"python3 -u -B ",D296Checker," --mode SELFTEST --fixture ",D296Fixture," --receipt ",D296Receipt," --output ",D296Verdict," > ",D296CLog," 2>&1 || { cat ",D296CLog,"; exit 1; }\n");
  PrintTo(D296S,"grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V4_CHECKER_SELFTEST_PASS mutation_attempted=19 mutation_rejected=19' ",D296CLog," >/dev/null || { cat ",D296CLog,"; exit 1; }\n");
else
  PrintTo(D296S,"python3 -u -B ",D296Producer," --mode PRODUCTION --output ",D296Receipt," > ",D296PLog," 2>&1 || { cat ",D296PLog,"; exit 1; }\n");
  PrintTo(D296S,"python3 -u -B ",D296Checker," --mode PRODUCTION --receipt ",D296Receipt," --output ",D296Verdict," > ",D296CLog," 2>&1 || { cat ",D296CLog,"; exit 1; }\n");
  PrintTo(D296S,"grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V4_PRODUCER_TERMINAL STATIC_BLOCKED:actual typed matrices are not staged' ",D296PLog," >/dev/null || { cat ",D296PLog,"; exit 1; }\n");
  PrintTo(D296S,"grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V4_CHECKER_TERMINAL STATIC_BLOCKED:actual typed matrices are not staged' ",D296CLog," >/dev/null || { cat ",D296CLog,"; exit 1; }\n");
fi;
PrintTo(D296S,"printf 'R07_JOINT_SLICE_KERNEL_GENERAL_V4_OK\\n' > ",D296OK,"\ntest -s ",D296OK,"\n"); CloseStream(D296S);;
Exec("bash ci/out/d972_r07_joint_slice_kernel_general_v4.sh");
if not IsExistingFile(D296OK) then Error("task296 missing completion"); fi;
Print("R07_JOINT_SLICE_KERNEL_GENERAL_V4_DRIVER_PASS\\n");
