#############################################################################
## search/probe/wac_v1/wall1_existence_search.g
## n=27 realization-pair existence search (裁定240 工程1).  Search for
## pairs (a1,b1) in S27 with:
##   a1^2 = 1, cycle type (2^13,1)         [k=13 transpositions, 1 fixed pt]
##   b1^3 = 1, cycle type (3^9)            [j=9 3-cycles, 0 fixed points]
##   w := b1^-1 * a1  has cycle type (5,5,5,5,5,2)
## and, on any hit, ASSERT <a1,b1> = S27 (order 27!) via a Size() check
## (recorded as pass/fail -- not a blind assumption).
##
## The a1-conjugacy class (type (2^13,1)) has size
##   27! / (2^13 * 13! * 1) = huge -- NOT exhaustible (unlike cent1/cent2's
## n=10/n=12 windows).  This script therefore does NOT claim completeness:
## it is a randomized witness search only.  A "no hit" outcome here is
## reported honestly as "not found within the trial/time budget" -- it is
## NOT a negative existence claim (scope_caveat below is explicit about
## this; no completeness argument is made or implied for this scan).
##
## Method: fix a single representative w0 of the target w-type
## (5,5,5,5,5,2).  Since w = b1^-1*a1 => b1 = a1*w0^-1, draw a1 uniformly
## at random from the (2^13,1) conjugacy class by conjugating a fixed
## representative a0 by a uniform Random(Sn) element (conjugation by a
## uniform group element pushes forward the uniform measure on Sn to the
## uniform measure on the orbit/conjugacy class -- same construction as
## search/probe/wac_v1/r4_existence_search.g's random branch).  Set
## b1 := a1*w0^-1, keep b1-type=(3^9) hits, and among those check
## generation.  Trial cap and wall-time cap below; stop early on first
## generation=S27 hit (existence witness suffices).
##
## RNG: GAP's GlobalMersenneTwister, explicitly Reset() to a recorded
## integer seed before the trial loop -- fully reproducible.
##
## Overridable knobs (IsBound-guarded so a wrapper script can Read() this
## file after pre-defining WALL1_TRIAL_CAP / WALL1_TIME_CAP_SEC / WALL1_SEED
## for a reduced local smoke test WITHOUT modifying this frozen driver;
## the production values below -- trial cap 1e7, time cap 900s (15 min),
## seed 20260730 -- are what ships to the mine-plan CI run, per 裁定240
## 工程1 instruction "試行数上限 10^7(時間 cap 15 分)").
##
## Single lane (GAP 4.16.0).  NOT a ledger claim.  No commit.  No sealed
## symbol.  Existence search only -- no judgement, no interpretation.
## No expected/predicted values are encoded anywhere in this script
## (contact isolation -- docs/notes/sat_l1_v1.md, r4_prediction_v1.md,
## ideas/, sol/ were NOT read while writing this script).
#############################################################################

Read("search/gaplib_common.g");

if not IsBound(WALL1_TRIAL_CAP) then WALL1_TRIAL_CAP := 10000000;; fi;
if not IsBound(WALL1_TIME_CAP_SEC) then WALL1_TIME_CAP_SEC := 900.0;; fi;
if not IsBound(WALL1_SEED) then WALL1_SEED := 20260730;; fi;
if not IsBound(WALL1_PROGRESS_EVERY) then WALL1_PROGRESS_EVERY := 200000;; fi;

n := 27;;
Sn := SymmetricGroup(n);;

CT := function(p) return SortedList(List(Orbits(Group(p),[1..n]), Length)); end;;

#############################################################################
## ---------------------- LID-1-style hashing (literal, not canonical-uid) --
#############################################################################
WACT_Sha256Counter := 0;;
WACT_Sha256OfString := function(s)
  local tmp, out, f, line;
  WACT_Sha256Counter := WACT_Sha256Counter + 1;
  tmp := Concatenation("search/.tmp_wall1_sha_", String(Runtime()), "_",
                        String(WACT_Sha256Counter), ".txt");
  out := Concatenation(tmp, ".sha");
  f := OutputTextFile(tmp, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, s);
  CloseStream(f);
  Exec(Concatenation("sha256sum \"", tmp, "\" > \"", out, "\""));
  f := InputTextFile(out);
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\" \"", out, "\""));
  if line = fail or Length(line) < 64 then
    Error("wall1_existence_search.g: WACT_Sha256OfString: sha256sum did not return a hash line");
  fi;
  return line{[1 .. 64]};
end;;

WACT_Lid1 := function(a1, b1, w)
  local s;
  s := Concatenation("LID1/v1|family=wall1|n=", String(n),
         "|a1=", String(a1), "|b1=", String(b1), "|w=", String(w));
  return rec(canonical_string := s, sha256 := WACT_Sha256OfString(s));
end;;

Print("#########################################################\n");
Print("## STEP 0  fix target w0 (type (5,5,5,5,5,2)) and a1-type\n");
Print("##         representative a0 (type (2^13,1))\n");
Print("#########################################################\n");

## w0 = (1..5)(6..10)(11..15)(16..20)(21..25)(26,27)
w0 := PermList(Concatenation(
        [2,3,4,5,1], [7,8,9,10,6], [12,13,14,15,11],
        [17,18,19,20,16], [22,23,24,25,21], [27,26]));;
## a0 = 13 disjoint transpositions on 1..26, fixed point 27
a0 := (1,2)(3,4)(5,6)(7,8)(9,10)(11,12)(13,14)(15,16)(17,18)(19,20)(21,22)(23,24)(25,26);;

Print("w0       = ", w0, "\n");
Print("w0 type  = ", CT(w0), "  sign(w0) = ", SignPerm(w0), "  ord(w0) = ", Order(w0), "\n");
Print("a0       = ", a0, "\n");
Print("a0 type  = ", CT(a0), "  sign(a0) = ", SignPerm(a0), "  ord(a0) = ", Order(a0), "\n");
Print("WALL1_TRIAL_CAP=", WALL1_TRIAL_CAP, "  WALL1_TIME_CAP_SEC=", WALL1_TIME_CAP_SEC,
      "  WALL1_SEED=", WALL1_SEED, "\n");

Print("\n#########################################################\n");
Print("## STEP 1  randomized trial loop: a1 := a0^Random(Sn),\n");
Print("##         b1 := a1*w0^-1, keep hits with b1 type (3^9),\n");
Print("##         among those check generation <a1,b1> = S27\n");
Print("#########################################################\n");

targetBType := [3,3,3,3,3,3,3,3,3];;

Reset(GlobalMersenneTwister, WALL1_SEED);;

tries := 0;; bTypeHits := 0;; genS27Hits := 0;;
foundWitness := fail;;
bTypeExamples := [];;
t0 := GAPLIB_WallElapsedMs();;
stoppedReason := "exhausted trial cap";;

while tries < WALL1_TRIAL_CAP do
  tries := tries + 1;
  a1 := a0 ^ Random(Sn);
  b1 := a1 * w0^-1;
  if CT(b1) = targetBType then
    bTypeHits := bTypeHits + 1;
    if Length(bTypeExamples) < 20 then
      Add(bTypeExamples, rec(a1:=a1, b1:=b1, tries_at_hit:=tries));
    fi;
    G := Group(a1, b1);
    if Size(G) = Size(Sn) and G = Sn then
      genS27Hits := genS27Hits + 1;
      if foundWitness = fail then
        foundWitness := rec(a1:=a1, b1:=b1, w:=b1^-1*a1, tries_at_hit:=tries, sizeG:=Size(G));
      fi;
      stoppedReason := "found generation=S27 witness -- early stop";;
      break;
    fi;
  fi;
  if tries mod WALL1_PROGRESS_EVERY = 0 then
    Print("   progress: tries=", tries, "  b1-type-hits=", bTypeHits,
          "  genS27hits=", genS27Hits, "  elapsed=",
          (GAPLIB_WallElapsedMs()-t0)/1000.0, "s\n");
  fi;
  if GAPLIB_CheckCap(WALL1_TIME_CAP_SEC, "wall1 trial loop") then
    stoppedReason := "wall-clock time cap exceeded";;
    break;
  fi;
od;

elapsedSec := (GAPLIB_WallElapsedMs()-t0)/1000.0;;
Print("loop done: tries=", tries, "  b1-type-hits=", bTypeHits,
      "  genS27hits=", genS27Hits, "  elapsed=", elapsedSec, "s\n");
Print("stoppedReason = ", stoppedReason, "\n");

Print("\n#########################################################\n");
Print("## STEP 2  witness detail (if found) and up to 20 b1-type-hit\n");
Print("##         examples (regardless of generation outcome)\n");
Print("#########################################################\n");
if foundWitness <> fail then
  Print("REALIZATION WITNESS FOUND at trial #", foundWitness.tries_at_hit, "\n");
  Print("   a1 = ", foundWitness.a1, "  type=", CT(foundWitness.a1),
        "  sign=", SignPerm(foundWitness.a1), "  ord=", Order(foundWitness.a1), "\n");
  Print("   b1 = ", foundWitness.b1, "  type=", CT(foundWitness.b1),
        "  sign=", SignPerm(foundWitness.b1), "  ord=", Order(foundWitness.b1), "\n");
  Print("   w  = b1^-1*a1 = ", foundWitness.w, "  type=", CT(foundWitness.w),
        "  ord=", Order(foundWitness.w), "\n");
  Print("   <a1,b1> order = ", foundWitness.sizeG, "  = S27 order? ",
        foundWitness.sizeG = Size(Sn), " (Size(Sn)=", Size(Sn), ")\n");
  Print("   Group(a1,b1) = Sn check (structural, not just order) : ",
        Group(foundWitness.a1, foundWitness.b1) = Sn, "\n");
  lid := WACT_Lid1(foundWitness.a1, foundWitness.b1, foundWitness.w);
  Print("   LID-1 canonical_string = ", lid.canonical_string, "\n");
  Print("   LID-1 sha256           = ", lid.sha256, "\n");
else
  Print("NO generation=S27 witness found within budget.\n");
fi;
Print("-- b1-type hit examples (up to 20, any generation outcome) --\n");
for i in [1..Length(bTypeExamples)] do
  ex := bTypeExamples[i];
  G := Group(ex.a1, ex.b1);
  Print("   [", i, "] tries_at_hit=", ex.tries_at_hit, "  |<a1,b1>|=", Size(G),
        "  is_S27=", (Size(G)=Size(Sn) and G=Sn), "\n");
od;

Print("\n#########################################################\n");
Print("## SUMMARY\n");
Print("#########################################################\n");
Print("mode                          = RANDOMIZED (not exhaustive -- a1-class\n");
Print("                                 too large; see scope_caveat)\n");
Print("seed                          = ", WALL1_SEED, "\n");
Print("trial_cap                     = ", WALL1_TRIAL_CAP, "\n");
Print("time_cap_sec                  = ", WALL1_TIME_CAP_SEC, "\n");
Print("tries                         = ", tries, "\n");
Print("elapsed_sec                   = ", elapsedSec, "\n");
Print("stopped_reason                = ", stoppedReason, "\n");
Print("b1_type_hits                  = ", bTypeHits, "\n");
Print("generation_S27_hits           = ", genS27Hits, "\n");
Print("exists_realization_pair_found = ", foundWitness <> fail, "\n");

Print("\nWALL1_EXISTENCE_SEARCH_DONE\n");
QUIT;
