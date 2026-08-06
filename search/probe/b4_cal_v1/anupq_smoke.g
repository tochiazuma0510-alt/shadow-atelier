## anupq_smoke.g -- verify the ANUPQ 'pq' binary actually works on this GAP
## runner (not just LoadPackage returning true -- the local Windows/Cygwin
## build has 'pq' dying with an iostream error despite LoadPackage succeeding,
## per docs/notes/b4_direct_adjudication_feasibility_v1_2.md sec5.4). This
## script is the GHA canary: if it fails here, P1 must not run.
##
## Canary fact (same doc, sec5.4 footnote): PQuotient(FreeGroup(2),7,2) = 7^5,
## NOT 7^3 (which is |F2:gamma_3(F2)*F2^7)| -- the well-known ClassBound vs
## true-Exponent-7 discrepancy that motivates the Exponent:=7 requirement).
## This is a cheap (seconds), well-specified, independently-checkable value.
Read("search/gaplib_common.g");
Read("search/probe/wac_v1/gap_output_prelude.g");

if LoadPackage("anupq") <> true then
  Print("ANUPQ_SMOKE_FAIL: LoadPackage(\"anupq\") did not return true\n");
  Error("ANUPQ_SMOKE_FAIL: LoadPackage failed");
fi;
Print("LoadPackage(\"anupq\") = true\n");

F2 := FreeGroup("x","y");;

## Pq(F : Prime:=p, ClassBound:=c) returns the pc-quotient group directly
## (confirmed API, matches search/probe/hsp7_gap_v1/stage3_gen_setup.g's
## working usage and anupq's own test suite anupq03.tst: "Pq(procId :
## ClassBound:=1); <pc group of size 4 ...>"). No Exponent here (canary
## deliberately matches the doc's OWN footnote value, sec5.4, which is the
## ClassBound-only 7^5 result -- NOT the Exponent:=7-corrected value).
t0 := GAPLIB_WallElapsedMs();
if not IsBound(Pq) then
  Print("ANUPQ_SMOKE_FAIL: Pq is not bound after LoadPackage\n");
  Error("ANUPQ_SMOKE_FAIL: Pq not bound");
fi;
result := Pq(F2 : Prime := 7, ClassBound := 2);;
t1 := GAPLIB_WallElapsedMs();

sz := Size(result);;
Print("Pq(F2:Prime:=7,ClassBound:=2) computed in ", t1-t0, " ms, |result| = ", sz,
      "  (expect 7^5 = ", 7^5, ")\n");

if sz = 7^5 then
  Print("ANUPQ_SMOKE_PASS: pq binary functional, canary value matches.\n");
else
  Print("ANUPQ_SMOKE_FAIL: canary value mismatch (got ", sz, ", expected ", 7^5, ")\n");
fi;

Print("ALL_DONE\n");
