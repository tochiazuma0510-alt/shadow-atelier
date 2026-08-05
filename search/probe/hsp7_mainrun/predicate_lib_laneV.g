## search/probe/hsp7_mainrun/predicate_lib_laneV.g
## Lane V judgement predicate library for HS main-run (prereg v2).
## Unlike Lane S/P (where the predicate functions are inline in the
## calibration driver and had to be extracted as a verbatim excerpt), Lane V
## already keeps its judgement predicate in a SEPARATE file:
## search/probe/hsp7_cond4_laneV/statemachine_lib.g (Read() by the
## calibration driver driver_step4_evaluate_v3.g, line 9). This file is
## therefore the TRUE byte-identical reuse case: no copy, no excerpt, the
## exact same file is Read() unchanged. Its SHA-256 is recorded directly
## (see prereg v2 SS2/appendix-digest table) and MUST match the calibration
## run's copy verbatim -- if this file's bytes ever differ from the
## calibration-run digest, that is the "predicate library changed" STOP
## condition (prereg v2 SS2), not a silent re-baseline.
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/probe/hsp7_cond4_laneV/statemachine_lib.g");
