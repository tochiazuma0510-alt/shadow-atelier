#############################################################################
## drophunt_k2_producer_v1.g -- K2 = K1 cap L3 re-derivation through the
## (F2)-repaired system (calibration gate, spec v2 SS7).
## K1 := K^(36) cap N_S4 (roof). Its G36 dihedral factor is built here via
## the SAME abstract (a,e)-triple algebra already validated in
## search/d972_rung_ordinary_idx3_producer_v2.py (dmul/ginv/gmul/gx/gy,
## ported from Python to GAP, preserving the identical formulas -- not a
## fresh derivation), then realized as a permutation group via its own
## right-regular representation (BFS closure over the 23,328-element
## abstract group, matching that script's own machine-confirmed count).
## L3 = the LINS row used throughout this repair (node 16437e56..., b3_index=3,
## the unique normal C3 = ker(exp_B3 mod 3) row).
## Seed: row36 (g*), reduction target computed relative to roof M exactly as
## for the M cap L windows (K2 <= K1 <= M, so the same #fib formula applies
## directly against M without needing to route through K1's own census).
#############################################################################

Read("search/drophunt_checker_producer_v2.g");;   ## reuses DCP2B3, DCP2s1, DCP2s2,
                                                     ## DCP2MX, DCP2MY (roof M model),
                                                     ## DCP2Seeds, EvalWordInQ, ThetaWord,
                                                     ## TauWord (from week3-battery-common.g)

#############################################################################
## G36 abstract (a,e)-triple algebra, ported from
## search/d972_rung_ordinary_idx3_producer_v2.py's dmul/dinv/gmul/ginv/gx/gy
## (same formulas, GAP syntax). Element = list of 3 pairs [a,e], a in
## Z/36, e in {0,1}. dmul(left,right,modulus): a,e=left; b,f=right;
## return [(a + (e=0 ? b : -b)) mod modulus, e xor f].
#############################################################################
DK2Dmul := function(left, right, modulus)
  local a, e, b, f, na;
  a := left[1];; e := left[2];;
  b := right[1];; f := right[2];;
  if e = 0 then na := a + b; else na := a - b; fi;;
  return [((na mod modulus) + modulus) mod modulus, (e+f) mod 2];;
end;;
DK2Dinv := function(value, modulus)
  local a, e, na;
  a := value[1];; e := value[2];;
  if e = 0 then na := -a; else na := a; fi;;
  return [((na mod modulus) + modulus) mod modulus, e];;
end;;
DK2Gmul := function(left, right, modulus)
  return [DK2Dmul(left[1],right[1],modulus), DK2Dmul(left[2],right[2],modulus), DK2Dmul(left[3],right[3],modulus)];;
end;;
DK2Ginv := function(value, modulus)
  return [DK2Dinv(value[1],modulus), DK2Dinv(value[2],modulus), DK2Dinv(value[3],modulus)];;
end;;
DK2Gid := function() return [[0,0],[0,0],[0,0]]; end;;
DK2Gx := function(modulus) return [[1 mod modulus, 0], [0,1], [0,1]]; end;;
DK2Gy := function(modulus) return [[1 mod modulus, 1], [1 mod modulus, 0], [1 mod modulus, 1]]; end;;

## BFS closure over abstract elements (matches producer_v2.py's own
## closure() used to machine-confirm |G36|=23328).
DK2ClosureG36 := function(modulus)
  local x, y, seen, queue, cur, steps, s, nxt, elemToIdx, idxToElem, idx;
  x := DK2Gx(modulus);; y := DK2Gy(modulus);;
  steps := [x, DK2Ginv(x,modulus), y, DK2Ginv(y,modulus)];;
  seen := [DK2Gid()];;
  elemToIdx := NewDictionary(DK2Gid(), true);;
  AddDictionary(elemToIdx, DK2Gid(), 1);;
  queue := [DK2Gid()];;
  idx := 1;;
  while idx <= Length(queue) do
    cur := queue[idx];;
    for s in steps do
      nxt := DK2Gmul(cur, s, modulus);;
      if LookupDictionary(elemToIdx, nxt) = fail then
        Add(seen, nxt);;
        AddDictionary(elemToIdx, nxt, Length(seen));;
        Add(queue, nxt);;
      fi;;
    od;;
    idx := idx + 1;;
  od;;
  return rec(elements:=seen, indexOf:=elemToIdx, x:=x, y:=y, modulus:=modulus);;
end;;

## Right-regular permutation representation: element g acts on the
## enumerated element list by right multiplication (index i -> index of
## elements[i]*g). Gives genuine PERMUTATIONS for x,y on Length(elements) points.
DK2RegularPerm := function(closureRec, g)
  local n, images, i, prod;
  n := Length(closureRec.elements);;
  images := [1..n];;
  for i in [1..n] do
    prod := DK2Gmul(closureRec.elements[i], g, closureRec.modulus);;
    images[i] := LookupDictionary(closureRec.indexOf, prod);;
  od;;
  return PermList(images);;
end;;

Print("DK2_BUILDING_G36_CLOSURE...\n");;
DK2T0 := GAPLIB_WallElapsedMs();;
DK2G36Closure := DK2ClosureG36(36);;
Print("DK2_G36_CLOSURE_DONE order=", Length(DK2G36Closure.elements),
  " elapsed_ms=", GAPLIB_WallElapsedMs()-DK2T0, "\n");;
if Length(DK2G36Closure.elements) <> 23328 then
  Error("DK2: G36 closure order drift, expected 23328");
fi;;

DK2X36 := DK2RegularPerm(DK2G36Closure, DK2G36Closure.x);;
DK2Y36 := DK2RegularPerm(DK2G36Closure, DK2G36Closure.y);;
Print("DK2_X36_Y36_PERMS_BUILT elapsed_ms=", GAPLIB_WallElapsedMs()-DK2T0, "\n");;
if Order(DK2X36) <> 36 or Order(DK2Y36) <> 36 then
  Print("DK2_WARNING orders: ", Order(DK2X36), " ", Order(DK2Y36), "\n");;
fi;;

## PSL(2,8) part -- same generators as roof M (degree 9)
DK2K1MX := DCP2DirectSumPerm(DK2X36, 23328, DCP2X4, 9);;
DK2K1MY := DCP2DirectSumPerm(DK2Y36, 23328, DCP2Y4, 9);;
DK2K1Degree := 23328 + 9;;
DK2K1Block := Group(DK2K1MX, DK2K1MY);;
Print("DK2_K1BLOCK_ORDER=", Size(DK2K1Block), " elapsed_ms=", GAPLIB_WallElapsedMs()-DK2T0, "\n");;
if Size(DK2K1Block) <> 23328*504 then
  Error("DK2: K1 block order drift, expected ", 23328*504);
fi;;
DK2K1Ord := Lcm(Order(DK2K1MX), Order(DK2K1MY));;
Print("DK2_K1_ORD(N_ord)=", DK2K1Ord, "\n");;
if DK2K1Ord <> 36 then Error("DK2: K1 N_ord drift, expected 36"); fi;;

## reduction hom K1Block -> M block (dihedral mod-9 reduction + identity on PSL)
DK2Pi0K1toM := GroupHomomorphismByImages(DK2K1Block, DCP2MBlock, [DK2K1MX, DK2K1MY], [DCP2MX, DCP2MY]);;
if DK2Pi0K1toM = fail then Error("DK2: K1->M reduction homomorphism ill-defined"); fi;;
Print("DK2_PI0_K1_TO_M_CONSTRUCTED elapsed_ms=", GAPLIB_WallElapsedMs()-DK2T0, "\n");;

#############################################################################
## L3: the LINS node used throughout this repair (b3_index=3, ker(exp mod3)).
#############################################################################
if LoadPackage("lins") <> true then Error("DK2: LINS package load failed"); fi;;
DK2Search := LowIndexNormalSubgroupsSearch(DCP2B3, 3);;
DK2Nodes := ComputedNormalSubgroups(DK2Search);;
DK2L3Node := First(DK2Nodes, n -> Index(n) = 3);;
if DK2L3Node = fail then Error("DK2: index-3 LINS node not found at bound 3"); fi;;
DK2L3 := Grp(DK2L3Node);;
DK2HomL3 := NaturalHomomorphismByNormalSubgroup(DCP2B3, DK2L3);;
DK2QL3 := Image(DK2HomL3);;
DK2IsoL3 := IsomorphismPermGroup(DK2QL3);;
DK2QpL3 := Image(DK2IsoL3);;
DK2S1L3 := Image(DK2IsoL3, Image(DK2HomL3, DCP2s1));;
DK2S2L3 := Image(DK2IsoL3, Image(DK2HomL3, DCP2s2));;
DK2XL3 := DK2S1L3^2;; DK2YL3 := DK2S2L3^2;;
DK2CpL3 := (DK2S1L3*DK2S2L3*DK2S1L3)^2;;
DK2CinL3 := (DK2CpL3 = Identity(DK2QpL3));;
DK2DegL3 := DCP2PermDegree(DK2QpL3);;
Print("DK2_L3_BUILT degree=", DK2DegL3, " c_in_L3=", DK2CinL3, "\n");;

#############################################################################
## Joint K2 := K1 cap L3
#############################################################################
DK2JX := DCP2DirectSumPerm(DK2K1MX, DK2K1Degree, DK2XL3, DK2DegL3);;
DK2JY := DCP2DirectSumPerm(DK2K1MY, DK2K1Degree, DK2YL3, DK2DegL3);;
DK2JointDegree := DK2K1Degree + DK2DegL3;;
DK2G := Group(DK2JX, DK2JY);;
DK2SizeG := Size(DK2G);;
Print("DK2_JOINT_G_ORDER=", DK2SizeG, " degree=", DK2JointDegree,
  " elapsed_ms=", GAPLIB_WallElapsedMs()-DK2T0, "\n");;

DK2K_ord := Lcm(Order(DK2JX), Order(DK2JY));;
Print("DK2_K_ORD=", DK2K_ord, "\n");;
if DK2K_ord mod 18 <> 0 then Error("DK2: K_ord not divisible by M_ord=18"); fi;;
DK2F1 := DK2K_ord / 18;;

## c_in_K2: c is in M always (documented); c in K1 assumed via the K^(n)-type
## roof structural property (same as M, now for n=36 -- NOT independently
## re-verified here since K1's own sigma1/sigma2 are not tracked in this
## construction, same documented gap as for M); c in L3 confirmed above.
DK2CinK2 := DK2CinL3;;
Print("DK2_C_IN_K2(assuming_c_in_K1_by_framework_property)=", DK2CinK2, "\n");;

## pi0: G(K2) -> PB3/M, via the K1->M reduction extended trivially on the L3
## block (L3 does not touch M).
DK2Pi0 := GroupHomomorphismByImages(DK2G, DCP2MBlock, [DK2JX, DK2JY], [DCP2MX, DCP2MY]);;
if DK2Pi0 = fail then Error("DK2: joint pi0 (K2 -> M) ill-defined"); fi;;
DK2H := Kernel(DK2Pi0);;
DK2F2 := Size(DK2H);;
Print("DK2_F2_ratio=", DK2F2, " (via Kernel(pi0), elapsed_ms=", GAPLIB_WallElapsedMs()-DK2T0, ")\n");;

DK2F3 := DK2F1 * DK2F2;;
Print("DK2_RAW_FIB(#fib)=", DK2F3, "  <- should be 48\n");;

#############################################################################
## Predicate evaluation for seed row36, IF c_in_K2 (word-level safe).
#############################################################################
if DK2CinK2 then
  DK2FreeF := FreeGroup("x","y");; DK2fx := DK2FreeF.1;; DK2fy := DK2FreeF.2;;
  DK2Epi := GroupHomomorphismByImagesNC(DK2FreeF, DK2G, [DK2fx,DK2fy], [DK2JX,DK2JY]);;
  DK2Seed := DCP2Seeds[1];;   # row36
  DK2JFseed := EvalWordInQ(DK2Seed.letters, DK2JX, DK2JY, Identity(DK2G));;
  DK2Target0 := Image(DK2Pi0, DK2JFseed);;
  DK2Hlist := Elements(DK2H);;
  DK2D := DerivedSubgroup(DK2G);;
  Print("DK2_DERIVED_SUBGROUP_ORDER=", Size(DK2D), " elapsed_ms=", GAPLIB_WallElapsedMs()-DK2T0, "\n");;

  DK2Coset := [];;
  for DK2h in DK2Hlist do
    DK2p := DK2JFseed * DK2h;;
    DK2wp := DCP2FreeEltToLetters(PreImagesRepresentative(DK2Epi, DK2p));;
    Add(DK2Coset, rec(perm:=DK2p, word:=DK2wp));;
  od;;
  Print("DK2_COSET_SIZE=", Length(DK2Coset), " elapsed_ms=", GAPLIB_WallElapsedMs()-DK2T0, "\n");;

  DK2MCands := List([0..(DK2K_ord/18)-1], t -> 0 + 18*t);;
  DK2ValidCount := 0;; DK2Rows := [];;
  for DK2m in DK2MCands do
    for DK2hc in DK2Coset do
      DK2u := 2*DK2m+1;;
      DK2p2 := DK2hc.perm;; DK2wp2 := DK2hc.word;;
      DK2okCm := Gcd(DK2u, DK2K_ord) = 1;;
      DK2okCf := DK2p2 in DK2D;;
      DK2charming := DK2okCm and DK2okCf;;
      DK2stage := "charming_fail";;
      DK2hex310 := false;; DK2hex311 := false;; DK2onto := false;; DK2redOk := false;;
      if DK2charming then
        DK2thetaW := ThetaWord(DK2wp2);;
        DK2hex310 := EvalWordInQ(Concatenation(DK2wp2, DK2thetaW), DK2JX, DK2JY, Identity(DK2G)) = Identity(DK2G);;
        if DK2hex310 then
          DK2yWordM := List([1..DK2m], ii -> ["y",1]);;
          DK2ymfWord := Concatenation(DK2yWordM, DK2wp2);;
          DK2tauWord1 := TauWord(DK2ymfWord);; DK2tauWord2 := TauWord(DK2tauWord1);;
          DK2hex311 := EvalWordInQ(Concatenation(DK2tauWord2, DK2tauWord1, DK2ymfWord), DK2JX, DK2JY, Identity(DK2G)) = Identity(DK2G);;
          if DK2hex311 then
            DK2genA := DK2JX^DK2u;; DK2genB := DK2p2^-1 * DK2JY^DK2u * DK2p2;;
            DK2onto := Size(Group(DK2genA, DK2genB)) = Size(DK2G);;
            if DK2onto then
              DK2redOk := (DK2m mod 18 = 0) and (Image(DK2Pi0, DK2p2) = DK2Target0);;
              if not DK2redOk then Error("DK2: reduction-match failed -- fail-closed"); fi;;
              DK2stage := "pass";;
            else DK2stage := "onto_fail"; fi;;
          else DK2stage := "hex311_fail"; fi;;
        else DK2stage := "hex310_fail"; fi;;
      fi;;
      DK2verdict := DK2charming and DK2hex310 and DK2hex311 and DK2onto and DK2redOk;;
      if DK2verdict then DK2ValidCount := DK2ValidCount + 1; fi;;
      Add(DK2Rows, rec(m:=DK2m, verdict:=DK2verdict, stage:=DK2stage));;
      Print("DK2_ROW m=", DK2m, " stage=", DK2stage, " verdict=", DK2verdict, "\n");;
    od;;
  od;;
  Print("DK2_VALID_COUNT=", DK2ValidCount, "  <- should be 2 (R07 m=0, R40 m=18)\n");;
else
  Print("DK2_BLOCKED_c_notin_K2\n");;
fi;;

DK2TotalElapsed := GAPLIB_WallElapsedMs() - DK2T0;;
Print("DK2_TOTAL_ELAPSED_MS=", DK2TotalElapsed, "\n");;

DK2Output := Concatenation(
  "{\n  \"schema\":\"drophunt-k2-rederivation/v1\",\n",
  "  \"K1_G36_order\":23328,\n",
  "  \"K1_block_order\":", String(Size(DK2K1Block)), ",\n",
  "  \"K1_N_ord\":", String(DK2K1Ord), ",\n",
  "  \"L3_c_in_L3\":", JB(DK2CinL3), ",\n",
  "  \"c_in_K2_assumed_via_c_in_K1_framework_property\":", JB(DK2CinK2), ",\n",
  "  \"joint_G_order\":", String(DK2SizeG), ",\n",
  "  \"joint_degree\":", String(DK2JointDegree), ",\n",
  "  \"K_ord\":", String(DK2K_ord), ",\n",
  "  \"F1_m_factor\":", String(DK2F1), ",\n",
  "  \"F2_ratio\":", String(DK2F2), ",\n",
  "  \"raw_fib_F3\":", String(DK2F3), ",\n",
  "  \"expected_raw_fib\":48,\n",
  "  \"raw_fib_matches_expected\":", JB(DK2F3=48), ",\n",
  "  \"valid_count\":", String(DK2ValidCount), ",\n",
  "  \"expected_valid_count\":2,\n",
  "  \"valid_count_matches_expected\":", JB(DK2ValidCount=2), ",\n",
  "  \"total_elapsed_ms\":", String(DK2TotalElapsed), "\n}\n");;
WriteFile("search/certs/drophunt_k2_rederivation_v1_20260828.json", DK2Output);;
Print("DK2_OUTPUT path=search/certs/drophunt_k2_rederivation_v1_20260828.json\n");;
Print("ALL_DONE\n");;
