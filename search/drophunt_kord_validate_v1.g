#############################################################################
## drophunt_kord_validate_v1.g
##
## Ruling 1720 repair. Computes the two fixed constants Order(MX), Order(MY)
## for the roof M = K^(9) cap N_S4 (PB3/M = G9 x PSL(2,8) compact model,
## same construction as lins_marked_strictness_export_v1.g / the earlier
## drophunt_calibration_fibcost_v1.g), and cross-validates the claim
##
##   Order(image of x in F2/K_F2) = lcm(Order(MX), Order(x-image in B3/L))
##
## (and same for y), hence
##
##   K_ord := lcm(Order(x-image in F2/K_F2), Order(y-image in F2/K_F2))
##          = lcm(Order(MX), Order(MY), Order(x-image in B3/L), Order(y-image in B3/L))
##
## against DIRECT computation of Order(JX), Order(JY) in the actual joint
## permutation group, for the 3 small STRICT_F2 target rows already used in
## drophunt_calibration_fibcost_v1.g (b3_index of L in {3,8,48}).
##
## This validates that K_ord can be derived PURELY ARITHMETICALLY (cycle-
## length lcm) from data already stored per row in
## lins_marked_strictness_export_v1_20260823.json (x_eq_sigma1_sq,
## y_eq_sigma2_sq permutation strings) plus the two fixed constants computed
## here once, WITHOUT rebuilding all 4,265 quotient groups.
#############################################################################

Read("search/probe/wac_v1/gap_output_prelude.g");;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

DHKVOutPath := "search/certs/drophunt_kord_validate_v1_20260829.json";;

DHKVG9Rec := MakeGn(9);;
if Size(DHKVG9Rec.G) <> 2916 then Error("DHKV: G9 order drift"); fi;
CheckGF8();;
DHKVSMat := MakeMatGF8(1,0,1,1);;
DHKVTMat := MakeMatGF8(4,3,1,5);;
DHKVSPerm := MatToPermGF8(DHKVSMat);;
DHKVTPerm := MatToPermGF8(DHKVTMat);;
DHKVWPerm := DHKVSPerm * DHKVTPerm^-1;;
DHKVX4 := DHKVWPerm^2;;
DHKVY4 := DHKVSPerm^-1 * DHKVX4 * DHKVSPerm;;
DHKVP4 := Group(DHKVX4, DHKVY4);;
if Size(DHKVP4) <> 504 then Error("DHKV: PSL(2,8) order drift"); fi;

DHKVShiftPerm := function(p, offset, size)
  local images, j;
  images := [1..offset+size];
  for j in [1..size] do images[offset+j] := offset + (j^p); od;
  return PermList(images);
end;;

DHKVDirectSumPerm := function(p, psize, q, qsize)
  return p * DHKVShiftPerm(q, psize, qsize);
end;;

DHKVPermDegree := function(G)
  local d;
  d := LargestMovedPoint(G);;
  if d = 0 then return 1; fi;
  return d;
end;;

DHKVMX := DHKVDirectSumPerm(DHKVG9Rec.x, 27, DHKVX4, 9);;
DHKVMY := DHKVDirectSumPerm(DHKVG9Rec.y, 27, DHKVY4, 9);;
DHKVMOrder := Size(Group(DHKVMX, DHKVMY));;
DHKVMDegree := 36;;
if DHKVMOrder <> 1469664 then Error("DHKV: PB3/M order drift"); fi;

DHKVOrdMX := Order(DHKVMX);;
DHKVOrdMY := Order(DHKVMY);;
DHKVKOrdM := Lcm(DHKVOrdMX, DHKVOrdMY);;
Print("DHKV_M_CONST Order(MX)=", DHKVOrdMX, " Order(MY)=", DHKVOrdMY,
  " M_ord(lcm)=", DHKVKOrdM, "\n");;
if DHKVKOrdM <> 18 then
  Print("DHKV_WARNING M_ord computed=", DHKVKOrdM, " expected 18 (sol_reply_159_iv.md verbatim)\n");;
fi;;

DHKVF := FreeGroup("a", "b");;
DHKVa := DHKVF.1;; DHKVb := DHKVF.2;;
DHKVRel := DHKVa * DHKVb * DHKVa * (DHKVb * DHKVa * DHKVb)^-1;;
DHKVB3 := DHKVF / [DHKVRel];;
DHKVs1 := DHKVB3.1;; DHKVs2 := DHKVB3.2;;

if LoadPackage("lins") <> true then Error("DHKV: LINS package load failed"); fi;
DHKVT0 := GAPLIB_WallElapsedMs();;
DHKVSearch := LowIndexNormalSubgroupsSearch(DHKVB3, 48);;
DHKVNodes := ComputedNormalSubgroups(DHKVSearch);;
Print("DHKV_LINS48_DONE nodes=", Length(DHKVNodes), "\n");;

DHKVTargetIdx := [3, 8, 48];;
DHKVRows := [];;

for DHKVNode in DHKVNodes do
  DHKVIdx := Index(DHKVNode);;
  if DHKVIdx = 1 then continue; fi;
  if not (DHKVIdx in DHKVTargetIdx) then continue; fi;

  DHKVL := Grp(DHKVNode);;
  DHKVHom := NaturalHomomorphismByNormalSubgroup(DHKVB3, DHKVL);;
  DHKVQ := Image(DHKVHom);;
  DHKVIso := IsomorphismPermGroup(DHKVQ);;
  DHKVQp := Image(DHKVIso);;
  DHKVS1p := Image(DHKVIso, Image(DHKVHom, DHKVs1));;
  DHKVS2p := Image(DHKVIso, Image(DHKVHom, DHKVs2));;
  DHKVXp := DHKVS1p^2;; DHKVYp := DHKVS2p^2;;
  DHKVDeg := DHKVPermDegree(DHKVQp);;

  DHKVJX := DHKVDirectSumPerm(DHKVMX, DHKVMDegree, DHKVXp, DHKVDeg);;
  DHKVJY := DHKVDirectSumPerm(DHKVMY, DHKVMDegree, DHKVYp, DHKVDeg);;

  ## Direct computation (ground truth)
  DHKVDirectOrdJX := Order(DHKVJX);;
  DHKVDirectOrdJY := Order(DHKVJY);;
  DHKVDirectKord := Lcm(DHKVDirectOrdJX, DHKVDirectOrdJY);;

  ## Formula-based (arithmetic-only) computation
  DHKVOrdXpL := Order(DHKVXp);;
  DHKVOrdYpL := Order(DHKVYp);;
  DHKVFormulaOrdJX := Lcm(DHKVOrdMX, DHKVOrdXpL);;
  DHKVFormulaOrdJY := Lcm(DHKVOrdMY, DHKVOrdYpL);;
  DHKVFormulaKord := Lcm(DHKVFormulaOrdJX, DHKVFormulaOrdJY);;

  DHKVMatch := (DHKVDirectKord = DHKVFormulaKord);;
  Print("DHKV_ROW b3_index=", DHKVIdx,
    " direct_Kord=", DHKVDirectKord, " formula_Kord=", DHKVFormulaKord,
    " match=", DHKVMatch,
    " Kord_over_Mord=", DHKVDirectKord/DHKVKOrdM, "\n");;
  if not DHKVMatch then Error("DHKV: formula mismatch -- STOP, do not trust arithmetic derivation"); fi;

  Add(DHKVRows, rec(b3_index:=DHKVIdx, direct_Kord:=DHKVDirectKord,
    formula_Kord:=DHKVFormulaKord, match:=DHKVMatch,
    Kord_over_Mord:=DHKVDirectKord/DHKVKOrdM));;
od;;

DHKVRowsJson := JoinC(List(DHKVRows, r -> Concatenation(
  "{\"b3_index\":", String(r.b3_index),
  ",\"direct_Kord\":", String(r.direct_Kord),
  ",\"formula_Kord\":", String(r.formula_Kord),
  ",\"match\":", JB(r.match),
  ",\"Kord_over_Mord\":", String(r.Kord_over_Mord), "}")), ",\n");;

DHKVOutput := Concatenation(
  "{\n",
  "  \"schema\":\"drophunt-kord-validate/v1\",\n",
  "  \"M_ord_computed\":", String(DHKVKOrdM), ",\n",
  "  \"Order_MX\":", String(DHKVOrdMX), ",\n",
  "  \"Order_MY\":", String(DHKVOrdMY), ",\n",
  "  \"all_rows_match\":", JB(ForAll(DHKVRows, r -> r.match)), ",\n",
  "  \"rows\":[\n", DHKVRowsJson, "\n  ]\n",
  "}\n");;

WriteFile(DHKVOutPath, DHKVOutput);;
Print("DHKV_OUTPUT path=", DHKVOutPath, "\n");;
Print("ALL_DONE\n");;
