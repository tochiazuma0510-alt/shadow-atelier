#############################################################################
# R07 task324/v12 bounded selftest driver; generated shell is ASCII-only.
#############################################################################
P := "search/d972_r07_joint_slice_kernel_general_v12.py";;
C := "crosscheck/check_d972_r07_joint_slice_kernel_general_v12.py";;
F := "search/certs/d972_r07_joint_slice_kernel_general_selftest_v12_20260829.json";;
PO := "ci/out/d972_r07_joint_slice_kernel_general_v12.producer.json";;
CO := "ci/out/d972_r07_joint_slice_kernel_general_v12.checker.json";;
PL := "ci/out/d972_r07_joint_slice_kernel_general_v12.producer.log";;
CL := "ci/out/d972_r07_joint_slice_kernel_general_v12.checker.log";;
OK := "ci/out/d972_r07_joint_slice_kernel_general_v12.ok";;
S := "ci/out/d972_r07_joint_slice_kernel_general_v12.sh";;

PrintTo(S,"set -eu\n");
PrintTo(S,"test \"$(wc -c < ",P,")\" = 13322\n");
PrintTo(S,"test \"$(sha256sum ",P," | awk '{print $1}')\" = 00b15e6b58865dcde137e1f963ce2ea13ce940781b88ee758ca4219fe386a2ca\n");
PrintTo(S,"test \"$(wc -c < ",C,")\" = 9988\n");
PrintTo(S,"test \"$(sha256sum ",C," | awk '{print $1}')\" = 6610a369491b6ba752e4536d5997a5f102785a84a6c2993e5249b5a757b48968\n");
PrintTo(S,"test \"$(wc -c < ",F,")\" = 615\n");
PrintTo(S,"test \"$(sha256sum ",F," | awk '{print $1}')\" = 84cf882cc46e5bce2ff4d51abe09201d6372e89008f7e9c44ba75f078e6de1e2\n");
PrintTo(S,"for v in v7 v8 v9 v10 v11 v12; do test ! -e ci/out/d972_r07_joint_slice_kernel_general_$v.producer.json -a ! -e ci/out/d972_r07_joint_slice_kernel_general_$v.checker.json -a ! -e ci/out/d972_r07_joint_slice_kernel_general_$v.producer.log -a ! -e ci/out/d972_r07_joint_slice_kernel_general_$v.checker.log -a ! -e ci/out/d972_r07_joint_slice_kernel_general_$v.ok; done\n");
PrintTo(S,"python3 -B -u ",P," --selftest --fixture ",F," --output ",PO," > ",PL," 2>&1\n");
PrintTo(S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V12_PRODUCER_SELFTEST_PASS' ",PL," || true)\" -eq 1\n");
PrintTo(S,"python3 -B -u ",C," --selftest --fixture ",F," --producer-receipt ",PO," --output ",CO," > ",CL," 2>&1\n");
PrintTo(S,"test \"$(grep -Fxc 'R07_JOINT_SLICE_KERNEL_GENERAL_V12_CHECKER_PASS terminal=SELFTEST_COMPLETE mutation_attempted=34 mutation_rejected=34' ",CL," || true)\" -eq 1\n");
PrintTo(S,"test -s ",PO," -a -s ",CO,"\n");
PrintTo(S,"SEAL_DIGEST=$(sha256sum ",CO," | awk '{print $1}'); test \"${#SEAL_DIGEST}\" = 64; test -n \"$SEAL_DIGEST\"\n");
PrintTo(S,"PTERM=$(grep -E -c '^R07_JOINT_SLICE_KERNEL_GENERAL_V12_PRODUCER_(SELFTEST_PASS|TERMINAL (UNKNOWN_INPUT|UNKNOWN_RESOURCE|STATIC_BLOCKED:actual typed matrices are not staged))$' ",PL," || true); test \"$PTERM\" -eq 1\n");
PrintTo(S,"CTERM=$(grep -E -c '^R07_JOINT_SLICE_KERNEL_GENERAL_V12_CHECKER_PASS terminal=(UNKNOWN_INPUT|UNKNOWN_RESOURCE|SELFTEST_COMPLETE|STATIC_BLOCKED:actual typed matrices are not staged)( mutation_attempted=34 mutation_rejected=34)?$' ",CL," || true); test \"$CTERM\" -eq 1\n");
PrintTo(S,"printf '%s\\n' R07_JOINT_SLICE_KERNEL_GENERAL_V12_DRIVER_PASS > ",OK,"\n");
PrintTo(S,"test \"$(wc -l < ",OK,")\" = 1\n");
CloseStream(S);
Print("R07 task324 v12 driver source emitted; execution is external.\n");
