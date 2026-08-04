# driver_step1_gen_setup_P.g -- Lane V, self-built (independent of Lane S code) construction
# of P = F2/(gamma5(F2)F2^7), via ANUPQ's own non-interactive SetupFile batch mode
# (docs/notes/hsp7_cond4_lanespec_v1.md Appendix B: SetupFile procedure, package-provided,
# not a self-authored protocol). p=7, ClassBound=4 (class <=4), Exponent=7 per NW(7)
# (hs_prop7_translation_v1.md SS8.7.1 定義VAR / SS8.7.3 定義NW(p), p=7,e=1).
#
# This writes the setup command file only; pq.exe is run in a separate step
# (driver_step2_run_pq.ps1) since it is an external, non-GAP executable.
Read("search/probe/wac_v1/gap_output_prelude.g");
LoadPackage("anupq");;

F2 := FreeGroup("x","y");;
setupPath := "search/probe/hsp7_cond4_laneV/pqsetup_P.txt";
r := Pq(F2 : Prime:=7, ClassBound:=4, Exponent:=7, SetupFile:=setupPath);
Print("Pq(F2 : Prime:=7,ClassBound:=4,Exponent:=7,SetupFile) returned: ", r, "\n");
Print("setup file written to: ", setupPath, "\n");
QUIT;
