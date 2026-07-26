# search/e2c6-common-data.g -- shared class-6 (A_3^(6)) transcribed table data + core
# operators, factored out for the j=3 gate (docs/manifest_e2c6j3_v1.md) so that the frozen,
# hash-ledgered j=2 gate file (search/e2c6-sweep.g, tag v1.0-g1 lineage / 裁定20 ratified) is
# NOT touched by this new work. This file is a VERBATIM re-transcription of the same public
# object (same group A_3^(6), same commander-designated ratified spec docs:
# docs/manifest_e2c6_sweep_v2.md, docs/委嘱16_ob定義_opus_v1.md, sol/sol_reply_22_ob.md) --
# it duplicates (does not import/Read) search/e2c6-sweep.g's own definitions, per the
# INPUT DISCIPLINE those specs establish (data traced to crosscheck/agree6_claude.json via
# the same one-off transcription tool; the operator code -- SNF-based linear solve, kappa
# cocycle, ob quotient formula -- is generic algebra, re-typed fresh here exactly as
# e2c6-sweep.g's own header describes for ITS relationship to search/e2-sweep-r2.g).
#
# STATUS (2026-07-26, implementer, j=3 gate build): this module is READ by
# search/e2c6j3-sweep.g only. It is NOT itself a runnable gate script (no fixtures, no FIRE
# lock, no certificate writers) -- purely shared data + pure functions, so that e2c6j3-sweep.g
# stays legible for its OWN j=3-specific content (linear stage at modulus 8, the 便24 F8
# lambda-shortcut, new first condition, M6-style multiplicity table).
#
# SizeScreen/LoadPackage("polycyclic") and gaplib_common.g are Read by the CALLING script
# (e2c6j3-sweep.g), not here, to avoid double-Read surprises.

# ================================================================================
# AUTO-TRANSCRIBED DATA (from crosscheck/agree6_claude.json -- verbatim copy of
# search/e2c6-sweep.g's own transcription, same source, same self-checks below)
# ================================================================================
BASIS21 := ["w","p","q","r1","r2","r3","t1","t2","t3","t4","t5","t6","s1","s2","s3","s4","s5","u1","u2","u3","u4"];;

ThetaTable21 := [
  [-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,-1,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0],
  [0,-1,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0],
  [0,0,0,0,-1,0,0,0,0,0,-1,-1,0,0,0,0,0,0,-2,0,0],
  [0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0],
  [0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,-1,0,0,-1,0,0,0,0,0,0,-2,-2,1],
  [0,0,0,0,0,0,0,-1,0,0,-1,0,0,0,0,0,0,-2,-2,0,-1],
  [0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,-2,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,-3,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,-2,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1]
];;

SigmaTablePoly21 := [
  [[1,0,0,0,0], [-1,0,0,0,0], [0,1,0,0,0], [1,0,0,0,0], [0,-1,0,0,0], [0,0,1,0,0], [-1,0,0,0,0], [0,1,0,0,0], [0,0,-1,0,0], [0,0,0,1,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [0,-1,0,0,0], [0,0,1,0,0], [0,0,0,-1,0], [0,0,0,0,1], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,1,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [0,0,0,0,0], [-1,0,0,0,0], [0,1,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [0,-1,0,0,0], [0,0,1,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [-1,0,0,0,0], [0,1,0,0,0], [0,0,-1,0,0], [0,0,0,1,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0]],
  [[0,0,0,0,0], [-1,0,0,0,0], [-1,0,0,0,0], [2,0,0,0,0], [2,-1,0,0,0], [1,-1,0,0,0], [-3,0,0,0,0], [-3,2,0,0,0], [-2,2,-1,0,0], [-1,1,-1,0,0], [-1,0,0,0,0], [0,0,0,0,0], [4,0,0,0,0], [4,-3,0,0,0], [3,-3,2,0,0], [2,-2,2,-1,0], [1,-1,1,-1,0], [2,0,0,0,0], [1,-1,0,0,0], [0,0,0,0,0], [-3,1,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,-1,0,0,0], [0,1,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [0,-1,0,0,0], [0,0,1,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [-1,0,0,0,0], [-1,0,0,0,0], [0,0,0,0,0], [2,0,0,0,0], [2,-1,0,0,0], [1,-1,0,0,0], [1,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [-3,0,0,0,0], [-3,2,0,0,0], [-2,2,-1,0,0], [-1,1,-1,0,0], [-2,0,0,0,0], [-1,1,0,0,0], [0,0,0,0,0], [2,-1,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [2,0,0,0,0], [1,0,0,0,0], [-3,0,0,0,0], [-6,1,0,0,0], [-5,2,0,0,0], [-2,1,0,0,0], [-3,0,0,0,0], [-1,0,0,0,0], [6,0,0,0,0], [12,-3,0,0,0], [12,-6,1,0,0], [8,-5,2,0,0], [3,-2,1,0,0], [9,0,0,0,0], [9,-3,0,0,0], [2,-1,0,0,0], [-6,3,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [-1,0,0,0,0], [0,1,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [-1,0,0,0,0], [-1,0,0,0,0], [0,0,0,0,0], [-1,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [2,0,0,0,0], [2,-1,0,0,0], [1,-1,0,0,0], [0,0,0,0,0], [3,0,0,0,0], [0,-1,0,0,0], [0,0,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [2,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [0,0,0,0,0], [-3,0,0,0,0], [-6,1,0,0,0], [-5,2,0,0,0], [-2,1,0,0,0], [-4,0,0,0,0], [-7,1,0,0,0], [-2,1,0,0,0], [3,-1,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [-1,0,0,0,0], [-3,0,0,0,0], [-3,0,0,0,0], [-1,0,0,0,0], [-2,0,0,0,0], [-1,0,0,0,0], [4,0,0,0,0], [12,-1,0,0,0], [15,-3,0,0,0], [10,-3,0,0,0], [3,-1,0,0,0], [12,0,0,0,0], [17,-2,0,0,0], [5,-1,0,0,0], [-8,2,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [-1,0,0,0,0], [0,1,0,0,0], [-1,0,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [-1,0,0,0,0], [-1,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [2,0,0,0,0], [2,-1,0,0,0], [1,-1,0,0,0], [1,1,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [-1,0,0,0,0], [-1,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [-2,0,0,0,0], [0,0,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [2,0,0,0,0], [1,0,0,0,0], [0,0,0,0,0], [3,0,0,0,0], [3,0,0,0,0], [0,0,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [-1,0,0,0,0], [-3,0,0,0,0], [-3,0,0,0,0], [-1,0,0,0,0], [-2,0,0,0,0], [-6,0,0,0,0], [-3,0,0,0,0], [2,0,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [4,0,0,0,0], [6,0,0,0,0], [4,0,0,0,0], [1,0,0,0,0], [5,0,0,0,0], [9,0,0,0,0], [3,0,0,0,0], [-4,0,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [0,0,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [-1,0,0,0,0], [-1,0,0,0,0], [0,0,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [2,0,0,0,0], [1,0,0,0,0], [0,0,0,0,0]],
  [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0]]
];;

EmComponents21 := [
  [rec(coef:=-1, shift:=1, k:=2)],
  [rec(coef:=1, shift:=2, k:=3)],
  [rec(coef:=-1, shift:=1, k:=3)],
  [rec(coef:=-1, shift:=3, k:=4)],
  [rec(coef:=1, shift:=2, k:=4)],
  [rec(coef:=-1, shift:=1, k:=4)],
  [rec(coef:=1, shift:=4, k:=5)],
  [rec(coef:=-1, shift:=3, k:=5)],
  [rec(coef:=1, shift:=2, k:=5)],
  [rec(coef:=-1, shift:=1, k:=5)],
  [rec(coef:=1, shift:=0, k:=1), rec(coef:=7, shift:=0, k:=2), rec(coef:=17, shift:=0, k:=3), rec(coef:=17, shift:=0, k:=4), rec(coef:=6, shift:=0, k:=5)],
  [rec(coef:=-1, shift:=0, k:=2), rec(coef:=-4, shift:=0, k:=3), rec(coef:=-6, shift:=0, k:=4), rec(coef:=-3, shift:=0, k:=5)],
  [rec(coef:=-1, shift:=5, k:=6)],
  [rec(coef:=1, shift:=4, k:=6)],
  [rec(coef:=-1, shift:=3, k:=6)],
  [rec(coef:=1, shift:=2, k:=6)],
  [rec(coef:=-1, shift:=1, k:=6)],
  [rec(coef:=-1, shift:=0, k:=1), rec(coef:=-10, shift:=0, k:=2), rec(coef:=-34, shift:=0, k:=3), rec(coef:=-52, shift:=0, k:=4), rec(coef:=-37, shift:=0, k:=5), rec(coef:=-10, shift:=0, k:=6)],
  [rec(coef:=1, shift:=0, k:=2), rec(coef:=7, shift:=0, k:=3), rec(coef:=17, shift:=0, k:=4), rec(coef:=17, shift:=0, k:=5), rec(coef:=6, shift:=0, k:=6)],
  [rec(coef:=-1, shift:=0, k:=3), rec(coef:=-4, shift:=0, k:=4), rec(coef:=-6, shift:=0, k:=5), rec(coef:=-3, shift:=0, k:=6)],
  [rec(coef:=3, shift:=0, k:=3), rec(coef:=10, shift:=0, k:=4), rec(coef:=11, shift:=0, k:=5), rec(coef:=4, shift:=0, k:=6)]
];;  # indexed by BASIS21 position

KappaTerms := [
  rec(out:="t5", in1:="p", in2:="w", coef:=1),
  rec(out:="t6", in1:="q", in2:="w", coef:=1),
  rec(out:="u1", in1:="r1", in2:="w", coef:=1),
  rec(out:="u2", in1:="r2", in2:="w", coef:=1),
  rec(out:="u3", in1:="r3", in2:="w", coef:=1),
  rec(out:="u4", in1:="q", in2:="p", coef:=1)
];;

DThetaFormula := rec(
  t5 := [rec(mcoef:=[-1,0,0], vars:=["q"]), rec(mcoef:=[-1,0,0], vars:=["r2"]), rec(mcoef:=[-1,0,0], vars:=["t3"])],
  t6 := [rec(mcoef:=[-1,0,0], vars:=["p"]), rec(mcoef:=[-1,0,0], vars:=["r2"]), rec(mcoef:=[-1,0,0], vars:=["t2"])],
  u1 := [rec(mcoef:=[-1,0,0], vars:=["r3"]), rec(mcoef:=[-2,0,0], vars:=["t3"]), rec(mcoef:=[-2,0,0], vars:=["s4"])],
  u2 := [rec(mcoef:=[-2,0,0], vars:=["r2"]), rec(mcoef:=[-2,0,0], vars:=["t2"]), rec(mcoef:=[-2,0,0], vars:=["t3"]), rec(mcoef:=[-3,0,0], vars:=["s3"])],
  u3 := [rec(mcoef:=[-1,0,0], vars:=["r1"]), rec(mcoef:=[-2,0,0], vars:=["t2"]), rec(mcoef:=[-2,0,0], vars:=["s2"])],
  u4 := [rec(mcoef:=[1,0,0], vars:=["t2"]), rec(mcoef:=[-1,0,0], vars:=["t3"]), rec(mcoef:=[-1,0,0], vars:=["p","q"])]
);;

DSigmaFormula := rec(
  t5 := [rec(mcoef:=[-1,0,0], vars:=["q"]), rec(mcoef:=[1,0,0], vars:=["r2"]), rec(mcoef:=[-3,0,0], vars:=["r3"]), rec(mcoef:=[1,0,0], vars:=["t3"]), rec(mcoef:=[-2,0,0], vars:=["t4"]), rec(mcoef:=[1,0,0], vars:=["C(w)"])],
  t6 := [rec(mcoef:=[-1,0,0], vars:=["r3"]), rec(mcoef:=[-1,0,0], vars:=["t2"]), rec(mcoef:=[1,0,0], vars:=["t3"]), rec(mcoef:=[-1,0,0], vars:=["t4"]), rec(mcoef:=[0,-1,0], vars:=["C(w)"])],
  u1 := [rec(mcoef:=[2,0,0], vars:=["q"]), rec(mcoef:=[-2,0,0], vars:=["r2"]), rec(mcoef:=[9,0,0], vars:=["r3"]), rec(mcoef:=[-4,0,0], vars:=["t3"]), rec(mcoef:=[12,0,0], vars:=["t4"]), rec(mcoef:=[-2,0,0], vars:=["s4"]), rec(mcoef:=[5,0,0], vars:=["s5"]), rec(mcoef:=[-1,0,0], vars:=["C(w)"])],
  u2 := [rec(mcoef:=[1,-1,0], vars:=["q"]), rec(mcoef:=[-1,1,0], vars:=["r2"]), rec(mcoef:=[9,-3,0], vars:=["r3"]), rec(mcoef:=[3,0,0], vars:=["t2"]), rec(mcoef:=[-7,1,0], vars:=["t3"]), rec(mcoef:=[17,-2,0], vars:=["t4"]), rec(mcoef:=[3,0,0], vars:=["s3"]), rec(mcoef:=[-6,0,0], vars:=["s4"]), rec(mcoef:=[9,0,0], vars:=["s5"]), rec(mcoef:=[0,1,0], vars:=["C(w)"])],
  u3 := [rec(mcoef:=[2,-1,0], vars:=["r3"]), rec(mcoef:=[0,-1,0], vars:=["t2"]), rec(mcoef:=[-2,1,0], vars:=["t3"]), rec(mcoef:=[5,-1,0], vars:=["t4"]), rec(mcoef:=[-2,0,0], vars:=["s2"]), rec(mcoef:=[3,0,0], vars:=["s3"]), rec(mcoef:=[-3,0,0], vars:=["s4"]), rec(mcoef:=[3,0,0], vars:=["s5"]), rec(mcoef:=[0,0,-1], vars:=["C(w)"])],
  u4 := [rec(mcoef:=[0,1,0], vars:=["w"]), rec(mcoef:=[1,0,0], vars:=["p"]), rec(mcoef:=[-3,1,0], vars:=["q"]), rec(mcoef:=[2,-1,0], vars:=["r2"]), rec(mcoef:=[-6,3,0], vars:=["r3"]), rec(mcoef:=[3,-1,0], vars:=["t3"]), rec(mcoef:=[-8,2,0], vars:=["t4"]), rec(mcoef:=[2,0,0], vars:=["s4"]), rec(mcoef:=[-4,0,0], vars:=["s5"]), rec(mcoef:=[0,1,0], vars:=["C(w)"]), rec(mcoef:=[-1,0,0], vars:=["C(q)"]), rec(mcoef:=[0,1,0], vars:=["w","q"]), rec(mcoef:=[1,0,0], vars:=["p","q"])]
);;

# ================================================================================
# index bookkeeping: Abar (15) = w,p,q,r1,r2,r3,t1,t2,t3,t4,s1,s2,s3,s4,s5 (skip t5,t6,u1-4)
#                     C    (6)  = t5,t6,u1,u2,u3,u4
# ================================================================================
NameIdx21 := function(nm) return Position(BASIS21, nm); end;;
AbarNames := ["w","p","q","r1","r2","r3","t1","t2","t3","t4","s1","s2","s3","s4","s5"];;
CNames := ["t5","t6","u1","u2","u3","u4"];;
AbarIdx21 := List(AbarNames, NameIdx21);;   # positions in the 21-list
CIdx21 := List(CNames, NameIdx21);;
NAB := Length(AbarNames);;   # 15
NC6 := Length(CNames);;      # 6

# name -> position in AbarNames, for readability at call sites (e.g. IdxP/IdxR2/IdxS3/IdxW
# below, used directly by e2c6j3-sweep.g's lambda formula (8.3)).
IdxAbar := function(nm) return Position(AbarNames, nm); end;;
IdxW := IdxAbar("w");;    IdxP := IdxAbar("p");;   IdxR2 := IdxAbar("r2");;   IdxS3 := IdxAbar("s3");;

# ================================================================================
# GenBinom(m,k) = m(m-1)...(m-k+1)/k!  -- generalized binomial, any integer m
# ================================================================================
GenBinom := function(m,k)
  local num, i;
  if k < 0 then return 0; fi;
  if k = 0 then return 1; fi;
  num := 1;
  for i in [0..k-1] do num := num * (m-i); od;
  return num / Factorial(k);
end;;

EvalPoly5 := function(p5, m)
  return p5[1] + p5[2]*GenBinom(m,1) + p5[3]*GenBinom(m,2) + p5[4]*GenBinom(m,3) + p5[5]*GenBinom(m,4);
end;;

EvalEmComponent := function(terms, m)
  local s, t;
  s := 0;
  for t in terms do s := s + t.coef * GenBinom(m + t.shift, t.k); od;
  return s;
end;;

# ================================================================================
# Full 21x21 linear operators (theta is m-independent; sigma depends on m via EvalPoly5)
# ================================================================================
SigmaMat21 := function(m)
  local M, i, j;
  M := List([1..21], i -> List([1..21], j -> EvalPoly5(SigmaTablePoly21[i][j], m)));
  return M;
end;;

EmVec21 := function(m)
  return List([1..21], i -> EvalEmComponent(EmComponents21[i], m));
end;;

# ================================================================================
# SELF-CHECK 1: theta^2 = id on all 21 generators (sanity on the transcribed table itself)
# ================================================================================
Theta21OfVec := function(f) return f * ThetaTable21; end;;
E2C6_thetaSqOk := true;;
for E2C6_kk in [1..21] do
  E2C6_ek := List([1..21], x->0);; E2C6_ek[E2C6_kk] := 1;;
  if Theta21OfVec(Theta21OfVec(E2C6_ek)) <> E2C6_ek then E2C6_thetaSqOk := false; fi;
od;;

# ================================================================================
# Abar-restricted (bar) operators
# ================================================================================
ThetaBarMat := List(AbarIdx21, i -> List(AbarIdx21, j -> ThetaTable21[i][j]));;   # 15x15, m-indep
SigmaBarMat := function(m) return List(AbarIdx21, i -> List(AbarIdx21, j -> EvalPoly5(SigmaTablePoly21[i][j], m))); end;;
EmBar15 := function(m) return List(AbarIdx21, i -> EvalEmComponent(EmComponents21[i], m)); end;;
EmC6 := function(m) return List(CIdx21, i -> EvalEmComponent(EmComponents21[i], m)); end;;
ThetaOnCMat := List(CIdx21, i -> List(CIdx21, j -> ThetaTable21[i][j]));;         # 6x6, m-indep
SigmaOnCMat := function(m) return List(CIdx21, i -> List(CIdx21, j -> EvalPoly5(SigmaTablePoly21[i][j], m))); end;;

ThetaBar := function(f) return f * ThetaBarMat; end;;
SigmaBar := function(f,m) return f * SigmaBarMat(m); end;;

# ================================================================================
# kappa(a,b): Abar(15) x Abar(15) -> C(6), per KappaTerms
# ================================================================================
Kappa := function(a15, b15)
  local out, term, ai, bi;
  out := List([1..NC6], x -> 0);
  for term in KappaTerms do
    ai := a15[Position(AbarNames, term.in1)];
    bi := b15[Position(AbarNames, term.in2)];
    out[Position(CNames, term.out)] := out[Position(CNames, term.out)] + term.coef * ai * bi;
  od;
  return out;
end;;

EvalDFormTerm := function(term, avec15, m, mPolyLen)
  local mc, v, av;
  if mPolyLen = 1 then
    mc := term.mcoef[1];
  else
    mc := term.mcoef[1] + term.mcoef[2]*GenBinom(m,1) + term.mcoef[3]*GenBinom(m,2);
  fi;
  if Length(term.vars) = 1 then
    v := term.vars[1];
    if Length(v) > 2 and v{[1,2]} = "C(" then
      av := avec15[Position(AbarNames, v{[3..Length(v)-1]})];
      return mc * GenBinom(av, 2);
    else
      return mc * avec15[Position(AbarNames, v)];
    fi;
  else
    return mc * avec15[Position(AbarNames, term.vars[1])] * avec15[Position(AbarNames, term.vars[2])];
  fi;
end;;

DThetaOf := function(avec15)
  local out, cc, terms, t, val;
  out := List([1..NC6], x -> 0);
  for cc in [1..NC6] do
    terms := DThetaFormula.(CNames[cc]);
    val := 0;
    for t in terms do val := val + EvalDFormTerm(t, avec15, 0, 1); od;
    out[cc] := val;
  od;
  return out;
end;;

DSigmaOf := function(avec15, m)
  local out, cc, terms, t, val;
  out := List([1..NC6], x -> 0);
  for cc in [1..NC6] do
    terms := DSigmaFormula.(CNames[cc]);
    val := 0;
    for t in terms do val := val + EvalDFormTerm(t, avec15, m, 3); od;
    out[cc] := val;
  od;
  return out;
end;;

EkAbar := function(i) local v; v := List([1..NAB], x->0); v[i] := 1; return v; end;;

# SELF-CHECK 2 (d_theta_formula / d_sigma_formula linear-term consistency with theta_table /
# sigma_table_poly's own C-columns) -- same discipline as e2c6-sweep.g.
E2C6_dThetaSelfCheckOk := true;;
for E2C6_gg in [1..NAB] do
  E2C6_got := DThetaOf(EkAbar(E2C6_gg));
  E2C6_colC := List(CIdx21, ci -> ThetaTable21[AbarIdx21[E2C6_gg]][ci]);
  if E2C6_got <> E2C6_colC then E2C6_dThetaSelfCheckOk := false; fi;
od;;

E2C6_dSigmaSelfCheckOk := true;;
for E2C6_gg in [1..NAB] do
  E2C6_got0 := DSigmaOf(EkAbar(E2C6_gg), 0);
  E2C6_got7 := DSigmaOf(EkAbar(E2C6_gg), 7);
  E2C6_colC0 := List(CIdx21, ci -> EvalPoly5(SigmaTablePoly21[AbarIdx21[E2C6_gg]][ci], 0));
  E2C6_colC7 := List(CIdx21, ci -> EvalPoly5(SigmaTablePoly21[AbarIdx21[E2C6_gg]][ci], 7));
  if E2C6_got0 <> E2C6_colC0 or E2C6_got7 <> E2C6_colC7 then E2C6_dSigmaSelfCheckOk := false; fi;
od;;

# ================================================================================
# q_theta_full(f) := -kappa(theta_bar(f), f) + d_theta_formula(f), q_N_full analogously.
# SIGN: -kappa (sign-fixed, matches class-5 precedent and route-G cross-check --
# see search/e2c6-sweep.g header for the discovery record; carried forward here unchanged).
# ================================================================================
QThetaFullRaw := function(f15) return -Kappa(ThetaBar(f15), f15) + DThetaOf(f15); end;;

DSigma2Raw := function(f15, m)
  local sf, a, b;
  sf := SigmaBar(f15, m);
  a := DSigmaOf(sf, m);
  b := DSigmaOf(f15, m) * SigmaOnCMat(m);
  return a + b;
end;;

QNFullRaw := function(f15, m)
  local ebar, Sf, S2f, eps, dS2, dS, c1, c2, c3;
  ebar := EmBar15(m);
  Sf := SigmaBar(f15, m);
  S2f := SigmaBar(Sf, m);
  eps := EmC6(m);
  dS2 := DSigma2Raw(f15, m);
  dS := DSigmaOf(f15, m);
  c1 := -Kappa(ebar, S2f);
  c2 := -Kappa(ebar+S2f, Sf);
  c3 := -Kappa(ebar+S2f+Sf, f15);
  return eps + dS2 + dS + c1 + c2 + c3;
end;;

# ================================================================================
# RATIFIED OB LAYER core (裁定20): ob := [q_theta - 3^{-1}(1+theta)q_N] in Ob := C^theta/(1+theta)K.
# ObFromQPair is R-generic (R = 2^(j-1)); the READOUT convention for R>2 (a in R[2], b-bar in
# R/2R, per 委嘱16 eq 0.3/0.6) is IMPLEMENTED IN e2c6j3-sweep.g (not here), since it is
# j=3-gate-specific interpretation, not shared machinery.
# ================================================================================
ModInverse := function(a, n)
  if n = 1 then return 0; fi;
  return Gcdex(a, n).coeff1 mod n;
end;;

ModVec := function(v, n) return List(v, x -> x mod n); end;;

ThetaOnCVec := function(qC) return qC * ThetaOnCMat; end;;

ObFromQPair := function(qTheta6, qN6, R)
  local inv3, thQN, corr, v, idxU4, idxU2;
  inv3 := ModInverse(3, R);
  thQN := ThetaOnCVec(qN6);
  corr := List([1..NC6], i -> inv3 * (qN6[i] + thQN[i]));
  v := ModVec(List([1..NC6], i -> qTheta6[i] - corr[i]), R);
  idxU4 := Position(CNames, "u4");;  idxU2 := Position(CNames, "u2");;
  return rec(v := v, ob_a := v[idxU4], ob_b := v[idxU2]);
end;;

ObFromF := function(f15in, m, j)
  local R, f15, qTheta6, qN6, res;
  R := 2^(j-1);
  f15 := List(f15in, x -> x mod 2^j);;
  qTheta6 := QThetaFullRaw(f15);;
  qN6 := QNFullRaw(f15, m);;
  res := ObFromQPair(qTheta6, qN6, R);;
  res.qTheta6 := qTheta6;;  res.qN6 := qN6;;  res.R := R;;
  return res;
end;;

# ================================================================================
# LINEAR STAGE (class 6, rank 15): (1+theta_bar) f = 0  AND  N_bar f = -Ebar_m, over Z
# (unreduced), solvability tested mod 2^j via SNF -- j-GENERIC (works for j=2 and j=3 alike;
# this is exactly what makes this module reusable for the j=3 gate).
# ================================================================================
V2Val := function(n)
  local v, nn;
  if n = 0 then return 1000000; fi;
  v := 0; nn := AbsInt(n);
  while nn mod 2 = 0 do nn := nn/2; v := v+1; od;
  return v;
end;;

IntBool := function(b) if b then return 1; else return 0; fi; end;;

BuildLinearSystemC6 := function(m)
  local n, thMat, smMat, sm2Mat, b, rows, rhs, i, k;
  n := NAB;
  thMat := ThetaBarMat;;
  smMat := SigmaBarMat(m);;
  sm2Mat := smMat * smMat;;
  b := EmBar15(m);;
  rows := [];;  rhs := [];;
  for i in [1..n] do
    rows[i] := List([1..n], k -> thMat[k][i] + IntBool(i=k));
    rhs[i] := 0;
  od;
  for i in [1..n] do
    rows[n+i] := List([1..n], k -> IntBool(i=k) + smMat[k][i] + sm2Mat[k][i]);
    rhs[n+i] := -b[i];
  od;
  return rec(n:=n, rows:=rows, rhs:=rhs, b:=b);
end;;

BuildSnfData := function(sysBuilder, m)
  local sys, snf;
  sys := sysBuilder(m);;
  snf := SmithNormalFormIntegerMatTransforms(sys.rows);;
  return rec(m:=m, sys:=sys, U:=snf.rowtrans, V:=snf.coltrans, D:=snf.normal, rank:=snf.rank, n:=sys.n);
end;;

# Solvability test mod 2^j (j-generic). Returns solvable(bool); if solvable, K-kernel
# generators (vec in Z^n, order=2^k) fully covering ker(M mod 2^j) -- this IS K_m^(j) (the
# homogeneous kernel of `rows`, i.e. ker(1+theta_bar) cap ker(N_bar_m) mod 2^j), independent
# of rhs (rhs only used for the solvability test itself and for ExtractF0's particular soln).
TestAtJ := function(snfData, j)
  local n, rank, D, U, V, b, c, modulus, i, failRow, ok, kgens, ord, genY, genX, d, v2d;
  n := snfData.n;  rank := snfData.rank;  D := snfData.D;  U := snfData.U;  V := snfData.V;
  b := snfData.sys.rhs;
  c := U * b;;
  modulus := 2^j;;
  ok := true;  failRow := 0;
  for i in [1..rank] do
    d := D[i][i];  v2d := V2Val(d);
    if V2Val(c[i]) < Minimum(v2d, j) then ok := false; failRow := i; break; fi;
  od;
  if ok then
    for i in [rank+1..Length(c)] do
      if V2Val(c[i]) < j then ok := false; failRow := i; break; fi;
    od;
  fi;
  if not ok then
    return rec(solvable:=false, failRow:=failRow, modulus:=modulus);
  fi;
  kgens := [];;
  for i in [1..n] do
    if i <= rank then
      d := D[i][i];  v2d := V2Val(d);
    else
      v2d := 1000000;
    fi;
    if v2d >= j then
      ord := 2^j;  genY := List([1..n], k -> 0);  genY[i] := 1;
    else
      ord := 2^v2d;  genY := List([1..n], k -> 0);  genY[i] := 2^(j - v2d);
    fi;
    genX := V * genY;;
    if ord > 1 then
      Add(kgens, rec(vec:=genX, order:=ord));
    fi;
  od;
  return rec(solvable:=true, modulus:=modulus, kgens:=kgens);
end;;

ExtractF0 := function(snfData, j)
  local n, rank, D, U, V, b, c, modulus, i, d, v2d, g, dprime, cprime, modprime, yi, y, f0;
  n := snfData.n;  rank := snfData.rank;  D := snfData.D;  U := snfData.U;  V := snfData.V;
  b := snfData.sys.rhs;  c := U * b;;  modulus := 2^j;;
  y := List([1..n], x -> 0);;
  for i in [1..rank] do
    d := D[i][i];  v2d := V2Val(d);
    if v2d >= j then
      y[i] := 0;
    else
      g := 2^v2d;  dprime := d/g;  cprime := c[i]/g;  modprime := modulus/g;
      if modprime = 1 then
        yi := 0;
      else
        yi := (Gcdex(dprime, modprime).coeff1 * cprime) mod modprime;
      fi;
      y[i] := yi;
    fi;
  od;
  f0 := V * y;;
  return f0;
end;;

Mod2j := function(v, modulus) return List(v, x -> x mod modulus); end;;

# ================================================================================
# CLASS-5 CONTROL model (independent classical truncated Magnus embedding, degree 3, dim 10),
# reused for the G2 fixture below -- j-generic (BuildSnfData/TestAtJ take j as a parameter).
# ================================================================================
DG5 := 3;;  BASIS5 := [];;  IDXTAB5 := List([1..DG5+1], x -> List([1..DG5+1], y -> 0));;
for E2C6_dd in [0..DG5] do
  for E2C6_aa in [E2C6_dd,E2C6_dd-1..0] do
    E2C6_bb := E2C6_dd - E2C6_aa;
    Add(BASIS5, [E2C6_aa,E2C6_bb]);
    IDXTAB5[E2C6_aa+1][E2C6_bb+1] := Length(BASIS5);
  od;
od;;
NN5 := Length(BASIS5);;  # 10
IdxOf5 := function(a,b)
  if a < 0 or b < 0 or a > DG5 or b > DG5 then return 0; fi;
  return IDXTAB5[a+1][b+1];
end;;
ZeroP5 := function() return List([1..NN5], x->0); end;;
ConstP5 := function(c) local v; v := ZeroP5(); if c <> 0 then v[IdxOf5(0,0)] := c; fi; return v; end;;
Sgen5 := function() local v; v := ZeroP5(); v[IdxOf5(1,0)] := 1; return v; end;;
Tgen5 := function() local v; v := ZeroP5(); v[IdxOf5(0,1)] := 1; return v; end;;
Pmul5 := function(u,v)
  local r, i, j2, a1,b1,a2,b2, idx;
  r := ZeroP5();
  for i in [1..NN5] do
    if u[i] <> 0 then
      a1 := BASIS5[i][1];  b1 := BASIS5[i][2];
      for j2 in [1..NN5] do
        if v[j2] <> 0 then
          a2 := BASIS5[j2][1];  b2 := BASIS5[j2][2];
          if a1+a2+b1+b2 <= DG5 then
            idx := IdxOf5(a1+a2, b1+b2);
            r[idx] := r[idx] + u[i]*v[j2];
          fi;
        fi;
      od;
    fi;
  od;
  return r;
end;;
Ppow5 := function(u, k)
  local r, b, n;
  r := ConstP5(1);  b := ShallowCopy(u);  n := k;
  while n > 0 do
    if n mod 2 = 1 then r := Pmul5(r,b); fi;
    b := Pmul5(b,b);
    n := QuoInt(n,2);
  od;
  return r;
end;;
PinvUnit5 := function(u)
  local x, r, t, i;
  x := u - ConstP5(1);
  r := ConstP5(1);  t := ConstP5(1);
  for i in [1..DG5] do
    t := Pmul5(t, x);
    if i mod 2 = 1 then r := r - t; else r := r + t; fi;
  od;
  return r;
end;;
Sunit5 := function() return ConstP5(1) + Sgen5(); end;;
Tunit5 := function() return ConstP5(1) + Tgen5(); end;;
Psubst5 := function(f, U, V)
  local r, Up, Vp, i, a, b;
  r := ZeroP5();
  Up := [ConstP5(1)];  Vp := [ConstP5(1)];
  for i in [1..DG5] do
    Add(Up, Pmul5(Up[i], U));
    Add(Vp, Pmul5(Vp[i], V));
  od;
  for i in [1..NN5] do
    if f[i] <> 0 then
      a := BASIS5[i][1];  b := BASIS5[i][2];
      if a+b <= DG5 then
        r := r + f[i] * Pmul5(Up[a+1], Vp[b+1]);
      fi;
    fi;
  od;
  return r;
end;;
ThetaP5 := function(f) return -1 * Psubst5(f, Tgen5(), Sgen5()); end;;
TauP5 := function(f)
  local invs, invt, rho;
  invs := PinvUnit5(Sunit5());
  invt := PinvUnit5(Tunit5());
  rho := Pmul5(invs,invt) - ConstP5(1);
  return Pmul5(Psubst5(f, Tgen5(), rho), invs);
end;;
SigmaP5 := function(f, m) return Pmul5(Ppow5(Tunit5(), m), TauP5(f)); end;;
EmP5 := function(m)
  local s,t,st,AA,c,k,invsm;
  if m = 0 then return ZeroP5(); fi;
  s := Sunit5();  t := Tunit5();  st := Pmul5(s,t);
  AA := function(u,n) local r,p,i; r:=ZeroP5(); p:=ConstP5(1);
    for i in [0..n-1] do r := r+p; p := Pmul5(p,u); od; return r; end;
  c := ZeroP5();
  for k in [2..m] do c := Pmul5(t, AA(st,k-1)) + Pmul5(t,c); od;
  invsm := Ppow5(PinvUnit5(s), m);
  return c - Pmul5(invsm, Pmul5(AA(s,m), AA(st,m)));
end;;
MatOf5 := function(op)
  local n, mo, i, e;
  n := NN5;  mo := [];
  for i in [1..n] do
    e := ZeroP5();  e[i] := 1;
    Add(mo, op(e));
  od;
  return mo;
end;;

BuildLinearSystemC5 := function(m)
  local n, thMat, smMat, sm2Mat, b, rows, rhs, i, k;
  n := NN5;
  thMat := MatOf5(ThetaP5);;
  smMat := MatOf5(x -> SigmaP5(x,m));;
  sm2Mat := smMat * smMat;;
  b := EmP5(m);;
  rows := [];;  rhs := [];;
  for i in [1..n] do
    rows[i] := List([1..n], k -> thMat[k][i] + IntBool(i=k));
    rhs[i] := 0;
  od;
  for i in [1..n] do
    rows[n+i] := List([1..n], k -> IntBool(i=k) + smMat[k][i] + sm2Mat[k][i]);
    rhs[n+i] := -b[i];
  od;
  return rec(n:=n, rows:=rows, rhs:=rhs, b:=b);
end;;
