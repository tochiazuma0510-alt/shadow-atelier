Read("search/probe/wac_v1/gap_output_prelude.g");
# R1-GAP-1 blind checker - stage 2: monodromy group order distribution
# over the 1,914,721 canonical S18-conjugacy-class representatives
# produced independently (Node.js) in stage 1 (scratchpad/r1gap1_blind/census.js).
# Input: scratchpad/r1gap1_blind/reps.bin - raw bytes, 18 bytes per
# representative, byte value v in [0,17] = image of point v under tau
# (0-indexed). sigma0 is fixed to the standard 18-cycle x -> x+1 mod 18.

s := StringFile("scratchpad/r1gap1_blind/reps.bin");;
total := Length(s) / 18;;
Print("total reps loaded: ", total, "\n");

sigma0 := PermList(Concatenation([2..18],[1]));;

# canonical target tau (0-indexed), independently derived from the raw
# sigma0/sigma1 values in search/certs/d2_gate_v1_20260813.json
# (lambda9_target_reference), conjugated to the sigma0=standard-cycle
# frame and reduced to its lexicographically-smallest rotation.
targetTau0 := [0,1,16,17,14,15,12,13,10,11,8,9,6,7,4,5,2,3];;
targetTauPerm := PermList(List(targetTau0, x -> x+1));;

distCounts := rec();;
targetOrder := fail;;
targetIdx := fail;;

startTime := Runtime();;
SHARD_START := 0;;
SHARD_END := total;;
if IsBound(ShardStart) then SHARD_START := ShardStart; fi;
if IsBound(ShardEnd) then SHARD_END := Minimum(ShardEnd, total); fi;

for idx in [SHARD_START..SHARD_END-1] do
  row := [];
  for k in [0..17] do
    Add(row, IntChar(s[idx*18 + k + 1]) + 1);
  od;
  tau := PermList(row);
  G := Group(sigma0, tau);
  ord := Size(G);
  ordKey := String(ord);
  if IsBound(distCounts.(ordKey)) then
    distCounts.(ordKey) := distCounts.(ordKey) + 1;
  else
    distCounts.(ordKey) := 1;
  fi;
  if row = List(targetTau0, x -> x+1) then
    targetOrder := ord;
    targetIdx := idx;
  fi;
  if idx mod 100000 = 0 and idx > SHARD_START then
    Print("processed up to idx=", idx, " elapsed_ms=", Runtime()-startTime, "\n");
  fi;
od;

elapsedMs := Runtime() - startTime;;
Print("DONE shard [", SHARD_START, ",", SHARD_END, ") elapsed_ms=", elapsedMs, "\n");
Print("distCounts=", distCounts, "\n");
Print("targetOrder=", targetOrder, "\n");
Print("targetIdx=", targetIdx, "\n");

outstream := OutputTextFile(Concatenation("scratchpad/r1gap1_blind/monorder_shard_", String(SHARD_START), "_", String(SHARD_END), ".json"), false);;
PrintTo(outstream, "{\"shard_start\":", SHARD_START, ",\"shard_end\":", SHARD_END,
  ",\"total_reps\":", total,
  ",\"elapsed_ms\":", elapsedMs,
  ",\"dist\":", distCounts,
  ",\"target_order\":", targetOrder,
  ",\"target_idx\":", targetIdx, "}\n");
CloseStream(outstream);;
