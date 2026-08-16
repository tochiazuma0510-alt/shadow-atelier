#############################################################################
## d972_b4_marity_m_export_v1.g
##
## Phase-A producer for the PB3 object M = K^(9) intersect N_S4.  This is
## deliberately separate from the PB4/972 producer: it exports the named
## PB3 maps and lossless permutation images, and never emits B4_stable=true.
## Intended through .github/workflows/gap-run.yml on GAP 4.16.0.
#############################################################################

Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

if IsBound(D972_B4_MARITY_SELFTEST) and D972_B4_MARITY_SELFTEST = true then
  Print("D972_B4_MARITY_M_EXPORT_V1_SELFTEST_PASS serializer=gap-run-boundary\n");
else
  if not IsBound(D972_B4_MARITY_OUTPUT) then
    D972_B4_MARITY_OUTPUT := "ci/out/d972_b4_marity_m_export_v1.json";;
  fi;

  JsonIntList := function(values)
    return JArr(List(values, String));
  end;;
  PermImageJson := function(p, degree)
    return JsonIntList(List([1 .. degree], i -> i^p));
  end;;
  PermPairJson := function(p, q, degree)
    return Concatenation("[", PermImageJson(p, degree), ",", PermImageJson(q, degree), "]");
  end;;
  ShiftPermLocal := function(p, offset, size)
    local values, j;
    values := [1 .. offset + size];
    for j in [1 .. size] do
      values[offset + j] := offset + (j^p);
    od;
    return PermList(values);
  end;;
  DirectSumPermLocal := function(p, degreeP, q, degreeQ)
    return p * ShiftPermLocal(q, degreeP, degreeQ);
  end;;

  # The common presentation is B3=<s1,s2 | s1*s2*s1=s2*s1*s2>.
  B3 := FreeGroup("s1", "s2");;
  s1 := B3.1;;
  s2 := B3.2;;
  braidRelator := s1*s2*s1*(s2*s1*s2)^-1;;

  g9 := MakeGn(9);;
  if Size(g9.G) <> 2916 or Lcm(Order(g9.x), Order(g9.y)) <> 18 then
    Error("d972_b4_marity_m_export_v1: MakeGn(9) anchor drift");
  fi;

  CheckGF8();;
  Smat := MakeMatGF8(1,0,1,1);;
  Tmat := MakeMatGF8(4,3,1,5);;
  Sperm := MatToPermGF8(Smat);;
  Tperm := MatToPermGF8(Tmat);;
  wPerm := Sperm * Tperm^-1;;
  Xperm := wPerm^2;;
  Yperm := Sperm^-1 * Xperm * Sperm;;
  Pgrp := Group(Xperm, Yperm);;
  if Size(Pgrp) <> 504 or Lcm(Order(Xperm), Order(Yperm)) <> 9 then
    Error("d972_b4_marity_m_export_v1: S4 window anchor drift");
  fi;

  XM := DirectSumPermLocal(g9.x, 27, Xperm, 9);;
  YM := DirectSumPermLocal(g9.y, 27, Yperm, 9);;
  GM := Group(XM, YM);;
  if Size(GM) <> 1469664 or Lcm(Order(XM), Order(YM)) <> 18 then
    Error("d972_b4_marity_m_export_v1: M anchor drift");
  fi;

  hK9 := GroupHomomorphismByImages(B3, g9.G, [s1,s2], [g9.x,g9.y]);;
  hS4 := GroupHomomorphismByImages(B3, Pgrp, [s1,s2], [Xperm,Yperm]);;
  hM := GroupHomomorphismByImages(B3, GM, [s1,s2], [XM,YM]);;
  if hK9 = fail or hS4 = fail or hM = fail then
    Error("d972_b4_marity_m_export_v1: B3 map construction failed");
  fi;
  relK9 := (Image(hK9, braidRelator) = Identity(g9.G));;
  relS4 := (Image(hS4, braidRelator) = Identity(Pgrp));;
  relM := (Image(hM, braidRelator) = Identity(GM));;
  if not (relK9 and relS4 and relM) then
    Error("d972_b4_marity_m_export_v1: braid relator replay failed");
  fi;

  k9Json := Concatenation(
    "{\"name\":\"K^(9)\",\"kernel_name\":\"K^(9)\",",
    "\"source_definition\":\"MakeGn(9)\",\"target_degree\":27,",
    "\"target_order\":", String(Size(g9.G)), ",",
    "\"marked_generator_labels\":[\"s1\",\"s2\"],",
    "\"generator_images\":", PermPairJson(g9.x,g9.y,27), ",",
    "\"braid_relator_replay\":", JB(relK9), "}");
  s4Json := Concatenation(
    "{\"name\":\"N_S4\",\"kernel_name\":\"N_S4\",",
    "\"source_definition\":\"GF(8) PSL(2,8) S,T window\",\"target_degree\":9,",
    "\"target_order\":", String(Size(Pgrp)), ",",
    "\"marked_generator_labels\":[\"s1\",\"s2\"],",
    "\"generator_images\":", PermPairJson(Xperm,Yperm,9), ",",
    "\"braid_relator_replay\":", JB(relS4), "}");
  mJson := Concatenation(
    "{\"source_group\":\"PB3\",\"target_name\":\"M\",",
    "\"target_definition\":\"K^(9) intersect N_S4\",\"target_degree\":36,",
    "\"target_order\":", String(Size(GM)), ",\"M_ord\":", String(Lcm(Order(XM),Order(YM))), ",",
    "\"marked_generator_labels\":[\"s1\",\"s2\"],\"generator_names\":[\"XM\",\"YM\"],",
    "\"generator_images\":", PermPairJson(XM,YM,36), ",",
    "\"braid_relator_replay\":", JB(relM), "}");
  proofJson := Concatenation(
    "{\"status\":\"PROVED_BY_COMMON_B3_KERNEL_IDENTITY\",",
    "\"named_intersection\":\"M=K^(9) intersect N_S4\",",
    "\"identity\":\"ker(delta_M)=ker(q_K9) intersect ker(q_N_S4)\",",
    "\"diagonal_map\":\"s1->(g9.x,Xperm), s2->(g9.y,Yperm)\",",
    "\"component_relator_replay\":{\"K^(9)\":", JB(relK9), ",\"N_S4\":", JB(relS4), "},",
    "\"diagonal_relator_replay\":", JB(relM), ",",
    "\"component_orders\":[2916,504],\"diagonal_order\":1469664,",
    "\"proof_scope\":\"PB3 named-kernel identity only; no PB4 PC presentation or 972 fibers\"}");

  cert := Concatenation(
    "{\"schema\":\"d972-b4-marity-m-export/v1\",",
    "\"status\":\"PROVED_M_PB3_TYPED\",",
    "\"source_group\":\"PB3\",\"target_group\":\"PB3/M\",",
    "\"presentation\":{\"name\":\"B3\",\"generators\":[\"s1\",\"s2\"],",
    "\"relator\":\"s1*s2*s1*(s2*s1*s2)^-1\",\"relator_replay\":", JB(relM), "},",
    "\"components\":[", k9Json, ",", s4Json, "],",
    "\"combined\":", mJson, ",\"named_intersection_proof\":", proofJson, ",",
    "\"phase_boundary\":{\"B4_stable\":false,\"pb4_pc_presentation\":\"MISSING\",",
    "\"full_972_fibers\":\"MISSING\",\"next_dependency\":\"lossless PB4 7^41 PC presentation plus typed reduction-fiber producer\"},",
    "\"provenance\":{\"producer\":\"search/probe/wac_v1/d972_b4_marity_m_export_v1.g\",",
    "\"construction_sources\":[\"search/week3-battery-common.g\",\"search/week3-psl-common.g\"]}} ");
  WriteFile(D972_B4_MARITY_OUTPUT, cert);;
  Print("D972_B4_MARITY_M_EXPORT_V1_WRITTEN ", D972_B4_MARITY_OUTPUT, "\n");
fi;
