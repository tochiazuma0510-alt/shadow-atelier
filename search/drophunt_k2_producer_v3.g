#############################################################################
## drophunt_k2_producer_v3.g -- K2 re-derivation using the v3 (WDICT-5-
## repaired) GROUP-ELEMENT-ONLY predicate (theta~/tau~ via closed-form
## Ad(Delta)/Ad(delta) automorphisms of A=<JX,JY,JC>, no words anywhere).
## Same K1=K^(36) cap N_S4 construction as drophunt_k2_producer_v1.g
## (G36 via the validated (a,e)-triple algebra + right-regular rep), now
## joined with the v3 predicate machinery.
#############################################################################

Read("search/drophunt_checker_producer_v3.g");;

DK3T0 := GAPLIB_WallElapsedMs();;

#############################################################################
## G36 abstract algebra (identical to drophunt_k2_producer_v1.g)
#############################################################################
DK3Dmul := function(left, right, modulus)
  local a, e, b, f, na;
  a := left[1];; e := left[2];; b := right[1];; f := right[2];;
  if e = 0 then na := a + b; else na := a - b; fi;;
  return [((na mod modulus) + modulus) mod modulus, (e+f) mod 2];;
end;;
DK3Gmul := function(left, right, modulus)
  return [DK3Dmul(left[1],right[1],modulus), DK3Dmul(left[2],right[2],modulus), DK3Dmul(left[3],right[3],modulus)];;
end;;
DK3Gid := function() return [[0,0],[0,0],[0,0]]; end;;
DK3Gx := function(modulus) return [[1 mod modulus, 0], [0,1], [0,1]]; end;;
DK3Gy := function(modulus) return [[1 mod modulus, 1], [1 mod modulus, 0], [1 mod modulus, 1]]; end;;

DK3ClosureG36 := function(modulus)
  local x, y, seen, queue, cur, steps, s, nxt, elemToIdx, idx;
  x := DK3Gx(modulus);; y := DK3Gy(modulus);;
  steps := [x, DK3Ginv(x,modulus), y, DK3Ginv(y,modulus)];;
  seen := [DK3Gid()];;
  elemToIdx := NewDictionary(DK3Gid(), true);;
  AddDictionary(elemToIdx, DK3Gid(), 1);;
  queue := [DK3Gid()];;
  idx := 1;;
  while idx <= Length(queue) do
    cur := queue[idx];;
    for s in steps do
      nxt := DK3Gmul(cur, s, modulus);;
      if LookupDictionary(elemToIdx, nxt) = fail then
        Add(seen, nxt);; AddDictionary(elemToIdx, nxt, Length(seen));; Add(queue, nxt);;
      fi;;
    od;;
    idx := idx + 1;;
  od;;
  return rec(elements:=seen, indexOf:=elemToIdx, x:=x, y:=y, modulus:=modulus);;
end;;
DK3Dinv := function(value, modulus)
  local a, e, na;
  a := value[1];; e := value[2];;
  if e = 0 then na := -a; else na := a; fi;;
  return [((na mod modulus) + modulus) mod modulus, e];;
end;;
DK3Ginv := function(value, modulus)
  return [DK3Dinv(value[1],modulus), DK3Dinv(value[2],modulus), DK3Dinv(value[3],modulus)];;
end;;
DK3RegularPerm := function(closureRec, g)
  local n, images, i, prod;
  n := Length(closureRec.elements);;
  images := [1..n];;
  for i in [1..n] do
    prod := DK3Gmul(closureRec.elements[i], g, closureRec.modulus);;
    images[i] := LookupDictionary(closureRec.indexOf, prod);;
  od;;
  return PermList(images);;
end;;

Print("DK3_BUILDING_G36_CLOSURE...\n");;
DK3G36Closure := DK3ClosureG36(36);;
if Length(DK3G36Closure.elements) <> 23328 then Error("DK3: G36 closure order drift"); fi;;
DK3X36 := DK3RegularPerm(DK3G36Closure, DK3G36Closure.x);;
DK3Y36 := DK3RegularPerm(DK3G36Closure, DK3G36Closure.y);;
Print("DK3_G36_READY elapsed_ms=", GAPLIB_WallElapsedMs()-DK3T0, "\n");;

DK3K1MX := DCP3DirectSumPerm(DK3X36, 23328, DCP3X4, 9);;
DK3K1MY := DCP3DirectSumPerm(DK3Y36, 23328, DCP3Y4, 9);;
DK3K1Degree := 23328 + 9;;
DK3K1Block := Group(DK3K1MX, DK3K1MY);;
if Size(DK3K1Block) <> 23328*504 then Error("DK3: K1 block order drift"); fi;;
DK3K1Ord := Lcm(Order(DK3K1MX), Order(DK3K1MY));;
if DK3K1Ord <> 36 then Error("DK3: K1 N_ord drift"); fi;;
Print("DK3_K1BLOCK_ORDER=", Size(DK3K1Block), " N_ord=", DK3K1Ord,
  " elapsed_ms=", GAPLIB_WallElapsedMs()-DK3T0, "\n");;

## ITEM 7: c in K1's own block is a FRAMEWORK ASSUMPTION here too (same
## grounding gap as roof M; K1 is also a K^(n)-type roof, n=36), flagged
## explicitly, not independently measured.
DK3JCK1 := Identity(DK3K1Block);;

DK3Pi0K1toM := GroupHomomorphismByImages(DK3K1Block, DCP3MBlock, [DK3K1MX, DK3K1MY], [DCP3MX, DCP3MY]);;
if DK3Pi0K1toM = fail then Error("DK3: K1->M reduction homomorphism ill-defined"); fi;;

#############################################################################
## L3
#############################################################################
if LoadPackage("lins") <> true then Error("DK3: LINS package load failed"); fi;;
DK3Search := LowIndexNormalSubgroupsSearch(DCP3B3, 3);;
DK3Nodes := ComputedNormalSubgroups(DK3Search);;
DK3L3Node := First(DK3Nodes, n -> Index(n) = 3);;
DK3L3 := Grp(DK3L3Node);;
DK3HomL3 := NaturalHomomorphismByNormalSubgroup(DCP3B3, DK3L3);;
DK3QL3 := Image(DK3HomL3);;
DK3IsoL3 := IsomorphismPermGroup(DK3QL3);;
DK3QpL3 := Image(DK3IsoL3);;
DK3S1L3 := Image(DK3IsoL3, Image(DK3HomL3, DCP3s1));;
DK3S2L3 := Image(DK3IsoL3, Image(DK3HomL3, DCP3s2));;
DK3XL3 := DK3S1L3^2;; DK3YL3 := DK3S2L3^2;;
DK3CpL3 := (DK3S1L3*DK3S2L3*DK3S1L3)^2;;
DK3CinL3 := (DK3CpL3 = Identity(DK3QpL3));;
DK3DegL3 := DCP3PermDegree(DK3QpL3);;
Print("DK3_L3_BUILT degree=", DK3DegL3, " c_in_L3=", DK3CinL3, "\n");;

#############################################################################
## Joint K2 := K1 cap L3, with A := <JX,JY,JC> and closed-form theta~/tau~
#############################################################################
DK3JX := DCP3DirectSumPerm(DK3K1MX, DK3K1Degree, DK3XL3, DK3DegL3);;
DK3JY := DCP3DirectSumPerm(DK3K1MY, DK3K1Degree, DK3YL3, DK3DegL3);;
DK3JC := DCP3DirectSumPerm(DK3JCK1, DK3K1Degree, DK3CpL3, DK3DegL3);;
DK3JointDegree := DK3K1Degree + DK3DegL3;;
DK3G := Group(DK3JX, DK3JY);;
DK3A := Group(DK3JX, DK3JY, DK3JC);;
DK3SizeG := Size(DK3G);;
Print("DK3_JOINT_G_ORDER=", DK3SizeG, " degree=", DK3JointDegree,
  " elapsed_ms=", GAPLIB_WallElapsedMs()-DK3T0, "\n");;

DK3K_ord := Lcm(Order(DK3JX), Order(DK3JY));;
if DK3K_ord mod 18 <> 0 then Error("DK3: K_ord not divisible by 18"); fi;;
DK3F1 := DK3K_ord / 18;;
DK3CinK2 := DK3CinL3;;   # c in K1 assumed (framework), c in L3 measured
Print("DK3_C_IN_K2(assumed_c_in_K1)=", DK3CinK2, " ord(cbar)=", Order(DK3JC), "\n");;

DK3Pi0 := GroupHomomorphismByImages(DK3G, DCP3MBlock, [DK3JX, DK3JY], [DCP3MX, DCP3MY]);;
if DK3Pi0 = fail then Error("DK3: joint pi0 (K2 -> M) ill-defined"); fi;;
DK3H := Kernel(DK3Pi0);;
DK3F2 := Size(DK3H);;
DK3F3 := DK3F1 * DK3F2;;
Print("DK3_RAW_FIB(#fib)=", DK3F3, "  <- should be 48\n");;

## ITEM 6: pin the M-target constant for row36 DIRECTLY in the M model
## (already computed once in DCP3Seeds[1].m_target_pinned at load time).
DK3Seed := DCP3Seeds[1];;

DK3ThetaHom := GroupHomomorphismByImages(DK3A, DK3A, [DK3JX,DK3JY,DK3JC], [DK3JY,DK3JX,DK3JC]);;
DK3TauHom := GroupHomomorphismByImages(DK3A, DK3A, [DK3JX,DK3JY,DK3JC], [DK3JY, DK3JY^-1*DK3JX^-1*DK3JC, DK3JC]);;
Print("DK3_THETA_WD=", DK3ThetaHom<>fail, " TAU_WD=", DK3TauHom<>fail,
  " elapsed_ms=", GAPLIB_WallElapsedMs()-DK3T0, "\n");;
if DK3ThetaHom = fail or DK3TauHom = fail then Error("DK3: theta~/tau~ ill-defined -- fail-closed"); fi;;

DK3JFseed := DCP3EvalWord(DK3Seed.letters, DK3JX, DK3JY, Identity(DK3G));;
DK3Target0 := Image(DK3Pi0, DK3JFseed);;
if DK3Seed.m_target_pinned <> DK3Target0 then
  Error("DK3: pinned M-target != window's own pi0(seed) -- fail-closed stop");
fi;;
Print("DK3_REDUCTION_MATCH_CHECK_AGAINST_PINNED_CONSTANT=true\n");;

DK3D := DerivedSubgroup(DK3G);;
Print("DK3_DERIVED_SUBGROUP_ORDER=", Size(DK3D), " elapsed_ms=", GAPLIB_WallElapsedMs()-DK3T0, "\n");;

DK3Hlist := Elements(DK3H);;
DK3Coset := List(DK3Hlist, h -> DK3JFseed * h);;
Print("DK3_COSET_SIZE=", Length(DK3Coset), "\n");;

DK3MCands := List([0..(DK3K_ord/18)-1], t -> 0 + 18*t);;
DK3ValidCount := 0;;
for DK3m in DK3MCands do
  for DK3p in DK3Coset do
    DK3u := 2*DK3m+1;;
    DK3okCm := Gcd(DK3u, DK3K_ord) = 1;;
    DK3okCf := DK3p in DK3D;;
    DK3charming := DK3okCm and DK3okCf;;
    DK3stage := "charming_fail";;
    DK3hex310 := false;; DK3hex311 := false;; DK3onto := false;; DK3redOk := false;;
    if DK3charming then
      DK3hex310 := (DK3p * Image(DK3ThetaHom, DK3p) = Identity(DK3A));;
      if DK3hex310 then
        DK3ymf := DK3JY^DK3m * DK3p;;
        DK3lhsF2 := Image(DK3TauHom, Image(DK3TauHom, DK3ymf)) * Image(DK3TauHom, DK3ymf) * DK3ymf;;
        DK3rhs := DK3JC^DK3m;;
        DK3hex311 := (DK3lhsF2 = DK3rhs);;
        if DK3hex311 then
          DK3genA := DK3JX^DK3u;; DK3genB := DK3p^-1 * DK3JY^DK3u * DK3p;;
          DK3onto := Size(Group(DK3genA, DK3genB)) = Size(DK3G);;
          if DK3onto then
            DK3redOk := (DK3m mod 18 = 0) and (Image(DK3Pi0, DK3p) = DK3Target0);;
            if not DK3redOk then Error("DK3: reduction-match failed -- fail-closed"); fi;;
            DK3stage := "pass";;
          else DK3stage := "onto_fail"; fi;;
        else DK3stage := "hex311_fail"; fi;;
      else DK3stage := "hex310_fail"; fi;;
    fi;;
    DK3verdict := DK3charming and DK3hex310 and DK3hex311 and DK3onto and DK3redOk;;
    if DK3verdict then DK3ValidCount := DK3ValidCount + 1; fi;;
    Print("DK3_ROW m=", DK3m, " stage=", DK3stage, " verdict=", DK3verdict, "\n");;
  od;;
od;;
Print("DK3_VALID_COUNT=", DK3ValidCount, "  <- should be 2\n");;

DK3TotalElapsed := GAPLIB_WallElapsedMs() - DK3T0;;
Print("DK3_TOTAL_ELAPSED_MS=", DK3TotalElapsed, "\n");;

DK3Output := Concatenation(
  "{\n  \"schema\":\"drophunt-k2-rederivation-v3-p-direct/v1\",\n",
  "  \"predicate\":\"group-element-only, closed-form Ad(Delta)/Ad(delta) automorphisms (WDICT-5 repair)\",\n",
  "  \"K1_block_order\":", String(Size(DK3K1Block)), ",\n",
  "  \"L3_c_in_L3\":", JB(DK3CinL3), ",\n",
  "  \"c_in_K2_assumed_via_c_in_K1_framework_property\":", JB(DK3CinK2), ",\n",
  "  \"theta_welldefined\":", JB(DK3ThetaHom<>fail), ",\n",
  "  \"tau_welldefined\":", JB(DK3TauHom<>fail), ",\n",
  "  \"joint_G_order\":", String(DK3SizeG), ",\n",
  "  \"K_ord\":", String(DK3K_ord), ",\n",
  "  \"F1_m_factor\":", String(DK3F1), ",\n",
  "  \"F2_ratio\":", String(DK3F2), ",\n",
  "  \"raw_fib_F3\":", String(DK3F3), ",\n",
  "  \"expected_raw_fib\":48,\n",
  "  \"raw_fib_matches_expected\":", JB(DK3F3=48), ",\n",
  "  \"valid_count\":", String(DK3ValidCount), ",\n",
  "  \"expected_valid_count\":2,\n",
  "  \"valid_count_matches_expected\":", JB(DK3ValidCount=2), ",\n",
  "  \"reduction_match_against_pinned_constant\":true,\n",
  "  \"total_elapsed_ms\":", String(DK3TotalElapsed), "\n}\n");;
WriteFile("search/certs/drophunt_k2_rederivation_v3_20260828.json", DK3Output);;
Print("DK3_OUTPUT path=search/certs/drophunt_k2_rederivation_v3_20260828.json\n");;
Print("ALL_DONE\n");;
