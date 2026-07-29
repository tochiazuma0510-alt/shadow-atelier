## r4_cell_logic.g -- shared exhaustive-orbit-enumeration logic for one
## (w0-type, k, m) cell of the r=4, xbar=(5,5,5,5), n=20 window.
## Expects globals set by caller before Read():
##   CELL_LABEL, W0LABEL, W0CYC (list of cycle lengths, sum=20),
##   K (transposition count for a), M (3-cycle count for b),
##   TARGET (structure constant, from r4_structconst_scan.g),
##   OUTFILE (json path), REPSFILE (gap-syntax resume path),
##   TRY_CAP, TIME_CAP_SEC.
## Method: fix w0 (single element); a1 ranges over conjugates of
## a0 = WacBlock(K,2) (uniform via a1 := a0^Random(S20)); b1 := a1*w0^-1;
## accept if Order(b1)=3 and NrMovedPoints(b1)=3*M (exactly M 3-cycles).
## New hits are expanded via their full C_S20(w0)-orbit (stable set).
## Resumable: if REPSFILE exists, seed sols/reps from it before continuing.
#############################################################################

WacCyc := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;
WacBlock := function(blocks, len)
  local p, i, base;
  p := (); base := 0;
  for i in [1..blocks] do
    p := p * WacCyc(List([1..len], j -> base+j)); base := base + len;
  od;
  return p;
end;;
BuildFromCycLens := function(cycLens)
  local p, base, len;
  p := (); base := 0;
  for len in cycLens do
    p := p * WacCyc(List([1..len], j -> base+j));
    base := base + len;
  od;
  return p;
end;;

n := 20;;
S20 := SymmetricGroup(n);; A20 := AlternatingGroup(n);;
w0 := BuildFromCycLens(W0CYC);;
uinv := w0^-1;;
a0 := WacBlock(K, 2);;
id := ();;
C := Centralizer(S20, w0);;

Print("=== CELL ", CELL_LABEL, " ===\n");
Print("  w0 = ", w0, "   a0 = ", a0, "\n");
Print("  |C_S20(w0)| = ", Size(C), "   TARGET = ", TARGET, "   M(3-cycles) = ", M, "\n");

sols := [];; reps := [];;
if IsExistingFile(REPSFILE) then
  Read(REPSFILE);;
  if IsBound(RESUME_REPS) then
    Print("  resuming from ", Length(RESUME_REPS), " saved orbit reps\n");
    for a1 in RESUME_REPS do
      ## defensive validity check: only trust reps that actually satisfy
      ## the target condition (guards against any REPSFILE corruption).
      b1chk := a1 * uinv;
      if Order(b1chk) = 3 and NrMovedPoints(b1chk) = 3*M then
        o := Orbit(C, a1, OnPoints);
        Append(sols, Filtered(o, z -> not z in sols));
        Add(reps, a1);
      else
        Print("  WARNING: skipping invalid resumed rep ", a1,
              " (fails target condition)\n");
      fi;
    od;
    Print("  resumed sols so far: ", Length(sols), " / ", TARGET, "\n");
  fi;
fi;;

t0 := Runtime();;
i := 0;;
timedOut := false;;
while Length(sols) < TARGET and i < TRY_CAP do
  i := i + 1;
  a1 := a0 ^ Random(S20);
  b1 := a1 * uinv;
  if Order(b1) = 3 and NrMovedPoints(b1) = 3*M then
    if not a1 in sols then
      o := Orbit(C, a1, OnPoints);
      Print("  new C(w0)-orbit, size ", Length(o), "  (running total ",
            Length(sols) + Length(o), " / ", TARGET, ")  [try ", i, "]\n");
      Append(sols, Filtered(o, z -> not z in sols));
      Add(reps, a1);
    fi;
  fi;
  if i mod 2000000 = 0 then
    Print("  ... progress: tries=", i, "  sols=", Length(sols), "/", TARGET,
          "  elapsed_sec=", (Runtime()-t0)/1000.0, "\n");
    if (Runtime() - t0) > TIME_CAP_SEC * 1000 then
      timedOut := true;
      Print("  TIME CAP HIT, stopping.\n");
      break;
    fi;
  fi;
od;;
elapsed := (Runtime() - t0) / 1000.0;;
complete := (Length(sols) = TARGET);;
Print("enumerated ", Length(sols), " / ", TARGET, "   COMPLETE? ", complete,
      "   tries=", i, "   elapsed_sec=", elapsed, "\n");

## write resume file (gap-syntax list of orbit reps) regardless of completion
repsOut := OutputTextFile(REPSFILE, false);;
SetPrintFormattingStatus(repsOut, false);;
AppendTo(repsOut, "RESUME_REPS := [\n");
for repIdx in [1..Length(reps)] do
  AppendTo(repsOut, String(reps[repIdx]));
  if repIdx < Length(reps) then
    AppendTo(repsOut, ",\n");
  else
    AppendTo(repsOut, "\n");
  fi;
od;
AppendTo(repsOut, "];\n");
CloseStream(repsOut);;

## classify each orbit representative
out := OutputTextFile(OUTFILE, false);;
SetPrintFormattingStatus(out, false);;
AppendTo(out, "{\n");
AppendTo(out, "  \"cell\": \"", CELL_LABEL, "\",\n");
AppendTo(out, "  \"w0_type\": \"", W0LABEL, "\",\n");
AppendTo(out, "  \"k\": ", K, ",\n");
AppendTo(out, "  \"m\": ", M, ",\n");
AppendTo(out, "  \"target_structconst\": ", TARGET, ",\n");
AppendTo(out, "  \"w0\": \"", String(w0), "\",\n");
AppendTo(out, "  \"a0\": \"", String(a0), "\",\n");
AppendTo(out, "  \"centralizer_order\": ", Size(C), ",\n");
AppendTo(out, "  \"tries\": ", i, ",\n");
AppendTo(out, "  \"elapsed_sec\": ", elapsed, ",\n");
AppendTo(out, "  \"enumerated\": ", Length(sols), ",\n");
AppendTo(out, "  \"complete\": ", complete, ",\n");
AppendTo(out, "  \"timed_out\": ", timedOut, ",\n");
AppendTo(out, "  \"num_orbits\": ", Length(reps), ",\n");
AppendTo(out, "  \"orbit_reps\": [\n");
for idx in [1..Length(reps)] do
  a1 := reps[idx];
  b1 := a1 * uinv;
  G := Group(a1, b1);
  orbLens := SortedList(List(Orbits(G,[1..n]), Length));
  osz := Length(Orbit(C, a1, OnPoints));
  AppendTo(out, "    {\"a\": \"", String(a1), "\", \"b\": \"", String(b1),
            "\", \"orbit_size_under_Cw0\": ", osz,
            ", \"group_order\": ", Size(G),
            ", \"orbit_lengths\": ", orbLens,
            ", \"transitive\": ", IsTransitive(G,[1..n]),
            ", \"eq_A20\": ", G = A20,
            ", \"eq_S20\": ", G = S20, "}");
  if idx < Length(reps) then AppendTo(out, ",\n"); else AppendTo(out, "\n"); fi;
od;
AppendTo(out, "  ]\n");
AppendTo(out, "}\n");
CloseStream(out);;

Print("CELL_DONE ", CELL_LABEL, "\n");
QUIT;
