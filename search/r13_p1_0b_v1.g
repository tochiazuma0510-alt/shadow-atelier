# search/r13_p1_0b_v1.g -- [P1-0b] block-system cycle-type measurement (裁定993・
#   docs/notes/w9_ansatz_v2_blocks.md §2.4/§7)
#
# For BOTH block systems found in r13_p1_0_blocks_v1 (size 9 x 2, size 3 x 6), compute the
# INDUCED action of sigma_0=X, sigma_1=Y, sigma_inf=Z=(XY)^-1 on the blocks themselves, and report
# cycle types. Fail-closed watches per the spec:
#   size-9 system: predict sigma_1-bar = identity (§2.1) -- halt if violated
#   size-3 system: sigma_1's fixed-block count a and transposition count b satisfy a+2b=6;
#                  b odd contradicts Riemann-Hurwitz -- halt if violated
#   b=0 => g(C_2)=0 ; b=2 => g(C_2)=1

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

BuildPnFull := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, X, Y, Gfull;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  a1 := tr(r,1);;  a2 := tr(r,2);;  a3 := tr(r,3);;
  q1 := tr(s,2)*tr(s,3);;  q2 := tr(s,1)*tr(s,3);;
  X := AbstractProd([a1,q1]);;  Y := AbstractProd([a1,a2,a3,q2]);;
  Gfull := Group(a1,a2,a3,q1,q2);;
  return rec(n:=n, a1:=a1, a2:=a2, a3:=a3, q1:=q1, q2:=q2, X:=X, Y:=Y, G:=Gfull);;
end;;

P9 := BuildPnFull(9);;
H9fun := Group(P9.a2, P9.a1*P9.a3, P9.q2);;
D := Size(P9.G)/Size(H9fun);;

phiAction9 := FactorCosetAction(P9.G, H9fun);;
Ximg9 := Image(phiAction9, P9.X);;   # sigma_0
Yimg9 := Image(phiAction9, P9.Y);;   # sigma_1
Zimg9 := (Ximg9*Yimg9)^-1;;          # sigma_inf
monG := Group(Ximg9, Yimg9);;
Print("|monG| = ", Size(monG), " D = ", D, "\n");

blocks := AllBlocks(monG);;
Print("AllBlocks representatives = ", blocks, "\n");

# identify the size-9 and size-3 representative blocks
rep9 := First(blocks, b -> Length(b) = 9);;
rep3 := First(blocks, b -> Length(b) = 3);;
Print("[", PF(rep9 <> fail and rep3 <> fail), "] found both a size-9 and a size-3 representative block\n");

# CycleType helper: given a permutation of D points and a partition into blocks (list of lists),
# compute the induced permutation on the set of blocks, then report cycle type on that quotient set.
InducedCycleType := function(perm, blockSystem)
  local nBlocks, blockOfPoint, pt, idx, b, images, i, imgPt, imgBlockIdx, quotPerm, cyc;
  nBlocks := Length(blockSystem);;
  blockOfPoint := [];;
  for idx in [1..nBlocks] do
    for pt in blockSystem[idx] do blockOfPoint[pt] := idx; od;
  od;
  images := [];;
  for i in [1..nBlocks] do
    imgPt := blockSystem[i][1]^perm;;
    imgBlockIdx := blockOfPoint[imgPt];;
    # sanity: ALL points of block i should map into the SAME target block (block system property)
    if ForAny(blockSystem[i], p -> blockOfPoint[p^perm] <> imgBlockIdx) then
      Error("InducedCycleType: block system not perm-invariant under this generator -- bug");
    fi;
    images[i] := imgBlockIdx;;
  od;
  quotPerm := PermList(images);;
  cyc := Collected(List([1..nBlocks], i -> CycleLength(quotPerm, i)));;
  return rec(quotPerm:=quotPerm, cycleType:=List(cyc, e -> [e[1], e[2]/e[1]]));;
end;;

blockSystem9 := Orbit(monG, rep9, OnSets);;
blockSystem3 := Orbit(monG, rep3, OnSets);;
Print("size-9 system: ", Length(blockSystem9), " blocks. size-3 system: ", Length(blockSystem3), " blocks.\n");

# ---- size-9 (2-block) system ----
Print("\n=== size-9 x 2 block system ===\n");
ct9X := InducedCycleType(Ximg9, blockSystem9);;
ct9Y := InducedCycleType(Yimg9, blockSystem9);;
ct9Z := InducedCycleType(Zimg9, blockSystem9);;
Print("sigma_0 (X) induced cycle type on 2 blocks: ", ct9X.cycleType, "\n");
Print("sigma_1 (Y) induced cycle type on 2 blocks: ", ct9Y.cycleType, "\n");
Print("sigma_inf (Z) induced cycle type on 2 blocks: ", ct9Z.cycleType, "\n");

sigma1Bar9IsIdentity := (ct9Y.quotPerm = ());;
Print("[", PF(sigma1Bar9IsIdentity), "] WATCH (2.1 prediction): sigma_1-bar = identity on size-9 system: ",
      sigma1Bar9IsIdentity, "\n");
if not sigma1Bar9IsIdentity then
  Print("[HALT] size-9 system prediction VIOLATED -- reporting per spec, not proceeding further interpretation.\n");
fi;

# ---- size-3 (6-block) system ----
Print("\n=== size-3 x 6 block system ===\n");
ct3X := InducedCycleType(Ximg9, blockSystem3);;
ct3Y := InducedCycleType(Yimg9, blockSystem3);;
ct3Z := InducedCycleType(Zimg9, blockSystem3);;
Print("sigma_0 (X) induced cycle type on 6 blocks: ", ct3X.cycleType, "\n");
Print("sigma_1 (Y) induced cycle type on 6 blocks: ", ct3Y.cycleType, "\n");
Print("sigma_inf (Z) induced cycle type on 6 blocks: ", ct3Z.cycleType, "\n");

# sigma_1's fixed-block count a and transposition count b (a + 2b = 6)
aFixed := 0;;  bTrans := 0;;  otherCycles := 0;;
for e in ct3Y.cycleType do
  if e[1] = 1 then aFixed := e[2];
  elif e[1] = 2 then bTrans := e[2];
  else otherCycles := otherCycles + e[2]; fi;
od;;
Print("sigma_1 on size-3 system: a(fixed)=", aFixed, " b(transpositions)=", bTrans,
      " other_cycle_count=", otherCycles, " (order>2 cycles, should be 0 if sigma_1 has order<=2 image)\n");
aPlus2bOk := (aFixed + 2*bTrans = 6) and (otherCycles = 0);;
Print("[", PF(aPlus2bOk), "] a+2b=6 and no higher-order cycles: ", aPlus2bOk, "\n");

bOdd := (bTrans mod 2 = 1);;
Print("[", PF(not bOdd), "] WATCH: b is NOT odd (RH consistency): b=", bTrans, "\n");
if bOdd then
  Print("[HALT] b is ODD -- contradicts Riemann-Hurwitz per spec. STOPPING, reporting raw values only.\n");
fi;

gC2 := fail;;
if bTrans = 0 then gC2 := 0;
elif bTrans = 2 then gC2 := 1;
fi;;
Print("\n★★★ g(C_2) = ", gC2, " (0 if b=0, 1 if b=2) ★★★\n");

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_p10b.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

CTJson := function(ct)
  local parts, e;
  parts := [];
  for e in ct do Add(parts, JPair(e[1],e[2])); od;
  return JArr(parts);
end;;

ValOrNull := function(v)
  if v = fail then return "null"; fi;
  return String(v);
end;;

scriptSha256 := ComputeSha256File("search/r13_p1_0b_v1.g");;

cert := Concatenation(
  "{\"schema\":\"r13-p1-0b/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/r13_p1_0b_v1.g\",\"order\":\"裁定993 / docs/notes/w9_ansatz_v2_blocks.md §2.4/§7 [P1-0b]\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"size9_system\":{",
    "\"sigma0_cycle_type\":", CTJson(ct9X.cycleType),
    ",\"sigma1_cycle_type\":", CTJson(ct9Y.cycleType),
    ",\"sigmainf_cycle_type\":", CTJson(ct9Z.cycleType),
    ",\"sigma1_bar_is_identity\":", JB(sigma1Bar9IsIdentity),
  "}",
  ",\"size3_system\":{",
    "\"sigma0_cycle_type\":", CTJson(ct3X.cycleType),
    ",\"sigma1_cycle_type\":", CTJson(ct3Y.cycleType),
    ",\"sigmainf_cycle_type\":", CTJson(ct3Z.cycleType),
    ",\"a_fixed\":", String(aFixed), ",\"b_transpositions\":", String(bTrans),
    ",\"a_plus_2b_eq_6\":", JB(aPlus2bOk),
    ",\"b_odd\":", JB(bOdd),
  "}",
  ",\"g_C2\":", ValOrNull(gC2),
  ",\"u_touched\":false",
  ",\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/r13_p1_0b_v1_20260812.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
