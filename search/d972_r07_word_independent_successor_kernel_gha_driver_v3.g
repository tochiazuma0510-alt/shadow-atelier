#############################################################################
# R07 v3 bounded driver.  This source is ASCII-only and emits one shell job.
#############################################################################
D := "d972_r07_word_independent_successor_kernel";;
P := "search/d972_r07_word_independent_successor_kernel_v3.py";;
C := "crosscheck/check_d972_r07_word_independent_successor_kernel_v3.py";;
F := "search/certs/d972_r07_word_independent_successor_kernel_selftest_v3_20260828.json";;
M := "ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json";;
V := "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json";;
PO := "ci/out/d972_r07_word_independent_successor_kernel_selftest_v3.json";;
CO := "ci/out/d972_r07_word_independent_successor_kernel_checker_verdict_v3.json";;
PL := "ci/out/d972_r07_word_independent_successor_kernel_v3.producer.log";;
CL := "ci/out/d972_r07_word_independent_successor_kernel_v3.checker.log";;
OK := "ci/out/d972_r07_word_independent_successor_kernel_v3.ok";;
S := "ci/out/d972_r07_word_independent_successor_kernel_v3.sh";;

PrintTo(S,"set -eu\n");
PrintTo(S,"test \"$(wc -c < ",P,")\" = 33283\n");
PrintTo(S,"test \"$(sha256sum ",P," | awk '{print $1}')\" = a228657ddf900d503c6d9574cd8fbefb338b0817412fbe108e234cf28f0aebab\n");
PrintTo(S,"test \"$(wc -c < ",C,")\" = 14916\n");
PrintTo(S,"test \"$(sha256sum ",C," | awk '{print $1}')\" = e10098766a07fe5542229b6dbda85fef7dcddb37de965aa3d56a07c1b5f95598\n");
PrintTo(S,"test \"$(wc -c < ",F,")\" = 434\n");
PrintTo(S,"test \"$(sha256sum ",F," | awk '{print $1}')\" = b385994a1e0d44e6c4cde981ab7b91b2db97d26773889c1db8270372799afda4\n");
PrintTo(S,"test -f ",M," && test -f ",V,"\n");
PrintTo(S,"test \"$(sha256sum ",M," | awk '{print $1}')\" = cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4\n");
PrintTo(S,"test \"$(wc -c < ",V,")\" = 150\n");
PrintTo(S,"for x in ci/out/d972_r07_word_independent_successor_kernel_v1 ci/out/d972_r07_word_independent_successor_kernel_v2 ci/out/d972_r07_word_independent_successor_kernel_v3; do test ! -e \"$x.json\" -a ! -e \"$x.ok\" -a ! -e \"$x.producer.log\" -a ! -e \"$x.checker.log\"; done\n");
PrintTo(S,"rm -f ",PO," ",CO," ",PL," ",CL," ",OK,"\n");
PrintTo(S,"python3 -B -u ",P," --selftest --fixture ",F," --output ",PO," > ",PL," 2>&1\n");
PrintTo(S,"test \"$(grep -Fxc 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_PRODUCER_SELFTEST_PASS' ",PL," || true)\" -eq 1\n");
PrintTo(S,"python3 -B -u ",C," --selftest --fixture ",F," --producer-receipt ",PO," --verdict ",CO," > ",CL," 2>&1\n");
PrintTo(S,"test \"$(grep -Fxc 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_CHECKER_PASS terminal=SELFTEST_COMPLETE mutation_attempted=34 mutation_rejected=34' ",CL," || true)\" -eq 1\n");
PrintTo(S,"test -s ",PO," -a -s ",CO,"\n");
PrintTo(S,"PTERM=$(grep -E '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_PRODUCER_(SELFTEST_PASS|TERMINAL (UNKNOWN_INPUT|UNKNOWN_RESOURCE|R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_PASS|SELFTEST_COMPLETE))$' ",PL," | wc -l); test \"$PTERM\" -eq 1\n");
PrintTo(S,"CTERM=$(grep -E '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_CHECKER_PASS terminal=(UNKNOWN_INPUT|UNKNOWN_RESOURCE|R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_PASS|SELFTEST_COMPLETE)( mutation_attempted=34 mutation_rejected=34)?$' ",CL," | wc -l); test \"$CTERM\" -eq 1\n");
PrintTo(S,"printf '%s\\n' R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_DRIVER_PASS > ",OK,"\n");
PrintTo(S,"test \"$(wc -l < ",OK,")\" = 1\n");
PrintTo(S,"test \"$(sed -n '1p' ",OK,")\" = R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_DRIVER_PASS\n");
CloseStream(S);
Print("R07 v3 driver source emitted; runtime execution is external.\n");
