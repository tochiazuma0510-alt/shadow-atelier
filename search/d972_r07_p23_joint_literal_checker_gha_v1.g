#############################################################################
##
##  GHA driver for the independent R07 p=2/p=3 joint literal checker.
##
##  This wrapper is ASCII-only.  The generic gap-run workflow reads it, and
##  GAP delegates the heavy standard-library Python replay to the independent
##  checker.  A shell success is accepted only with the exact terminal marker
##  and the versioned JSON result.
##
#############################################################################

checker := "crosscheck/check_d972_r07_p23_joint_literal_v1.py";;
outdir := "ci/out";;
logfile := "ci/out/d972_r07_p23_joint_literal_checker_v1.log";;
resultfile := "ci/out/d972_r07_p23_joint_literal_checker_v1.json";;
passfile := "ci/out/d972_r07_p23_joint_literal_checker_v1.pass";;

if IsBound(R07_P23_DRIVER_SELFTEST) and R07_P23_DRIVER_SELFTEST = true then
  cmd := Concatenation(
    "python3 -B ", checker, " --selftest > ", logfile, " 2>&1",
    " && test \"$(grep -Fxc 'R07_P23_JOINT_CHECKER_SELFTEST status=PASS d_length=72 a=-8 w23_length=616' ",
    logfile, ")\" -eq 1",
    " && touch ", passfile
  );;
else
  cmd := Concatenation(
    "python3 -B ", checker, " --out-dir ", outdir,
    " > ", logfile, " 2>&1",
    " && test -f ", resultfile,
    " && test \"$(grep -Fxc 'R07_P23_JOINT_CHECKER_FINAL status=PASS' ",
    logfile, ")\" -eq 1",
    " && test \"$(grep -Fxc 'R07_P23_JOINT_CHECKER_FINAL status=FAIL' ",
    logfile, ")\" -eq 0",
    " && touch ", passfile
  );;
fi;;

Exec(cmd);;
if IsExistingFile(logfile) then
  Exec(Concatenation("cat ", logfile));;
fi;;
if not IsExistingFile(passfile) then
  Error("R07_P23_GHA_DRIVER_STOP: checker, marker, or result gate failed");
fi;;

if IsBound(R07_P23_DRIVER_SELFTEST) and R07_P23_DRIVER_SELFTEST = true then
  Print("R07_P23_GHA_DRIVER_SELFTEST_PASS\n");;
else
  Print("R07_P23_GHA_DRIVER_FINAL status=PASS\n");;
fi;;
QUIT_GAP(0);;

