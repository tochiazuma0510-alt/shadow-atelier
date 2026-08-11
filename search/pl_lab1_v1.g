## search/pl_lab1_v1.g -- PL-LAB-1 measurement (裁定774/776/779/781), per
## docs/notes/post_lazard_window_design_v1_addendum_a.md (the REPAIRED
## spec; 本体 post_lazard_window_design_v1.md's def/comparison-series
## fields are SUPERSEDED by this addendum's DEF-PL'/P-PL-0/1'/2'/3').
##
## *** SCOPE DISCLOSURE (read before trusting the def(c,p)/def_k values) ***
## This script computes h_k^meas := dim_Fp( ker(1+theta-bar) intersect
## ker(1+tau-bar+tau-bar^2) ) on the MEASURED gamma_k/gamma_{k+1}(P_{c,p})
## -- i.e. the theta,tau automorphisms of the pc group evaluated exactly
## (via GAP GroupHomomorphismByImages on the actual group, then reduced
## mod gamma_{k+1} via pcgs exponents), for f restricted to being a PURE
## degree-k class (homogeneous in the graded sense). This was verified
## 3/3 against the closed-form H_k (命題 A-1) at p=5,c=4 for k=2,3,4
## before this addendum's repair (裁定781's own citation).
##
## *** IMPORTANT: h_k^meas is NOT necessarily the same quantity as the
## addendum's "s_k^grp" (the TRUE degree-k extension dimension of the
## full INDUCTIVE group-level hexagon solve, which allows f to have
## nonzero lower-degree parts already fixed by a prior partial solution,
## introducing bracket cross-terms [f_i,f_j] (i+j=k, i,j<k) into the
## degree-k equation that h_k^meas's PURE-degree-k analysis does not
## include). This implementer did NOT attempt the full inductive lifting
## computation within this pass (time/complexity constraints, disclosed
## honestly rather than risking a subtly wrong implementation) -- h_k^meas
## is reported as the measured quantity throughout, with this caveat
## attached to every degree k>=2. For k<p, Lazard's categorical
## equivalence (群とLie環が圏同値) guarantees s_k^grp=h_k^meas=H_k exactly
## (addendum §4.1 命題 PLA-1), so this caveat is INERT there; the caveat
## only has bite at k>=p, exactly the point under test -- meaning the
## measured def_k at k=p should be read as "h_k^meas - H_k", NOT
## unconditionally as "the full group-level excess" until the inductive
## refinement is done.
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

WITT := [2,1,2,3,6,9,18,30];;      # Witt(2,k), k=1..8
HK   := [1,0,1,1,2,3,6,10];;       # H_k = (1/3)[Witt(2,k) - tr(tau|Lambda_k)], k=1..8 (命題A-1, addendum_a §1.2)

TARGETS := [
  rec(label:="p5c4_control", p:=5, c:=4, path:="search/probe/pl_lab1_v1/PQ_OUTPUT_p5c4.g", kind:="control"),
  rec(label:="p5c5_main",    p:=5, c:=5, path:="search/probe/pl_lab1_v1/PQ_OUTPUT_p5c5.g", kind:="main"),
  rec(label:="p5c6_extra",   p:=5, c:=6, path:="search/probe/pl_lab1_v1/PQ_OUTPUT_p5c6.g", kind:="extra"),
  rec(label:="p7c4_control", p:=7, c:=4, path:="search/probe/pl_lab1_v1/PQ_OUTPUT_p7c4.g", kind:="control"),
  rec(label:="p7c6_control", p:=7, c:=6, path:="search/probe/pl_lab1_v1/PQ_OUTPUT_p7c6.g", kind:="control"),
  rec(label:="p7c7_main",    p:=7, c:=7, path:="search/probe/pl_lab1_v1/PQ_OUTPUT_p7c7.g", kind:="main"),
];;

results := [];;
stopHit := false;;
stopDetail := "";;

for t in TARGETS do
  if stopHit then continue; fi;
  Read(t.path);
  P := F;;  xG := MapImages[1];;  yG := MapImages[2];;
  Unbind(F);;  Unbind(MapImages);;

  order := Size(P);;
  expOk := (xG^t.p = Identity(P)) and (yG^t.p = Identity(P));;

  lcs := LowerCentralSeriesOfGroup(P);;
  lcsDims := List([1..Length(lcs)-1], i -> LogInt(Size(lcs[i])/Size(lcs[i+1]), t.p));;
  wittList := WITT{[1..t.c]};;
  gammaTrivial := Size(lcs[Length(lcs)]) = 1;;

  ## ---- P-PL-0: k<p must match Witt exactly; STOP if it doesn't ----
  for k in [1..Minimum(t.c, t.p - 1)] do
    if lcsDims[k] <> wittList[k] then
      stopHit := true;
      stopDetail := Concatenation("P_PL_0_VIOLATION_K_LT_P: target=", t.label, " k=", String(k),
                                    " measured=", String(lcsDims[k]), " witt=", String(wittList[k]));
      Print("STOP: ", stopDetail, "\n");
      break;
    fi;
  od;
  if stopHit then continue; fi;

  ppl0DropAtP := 0;;  ppl0DropOkStr := "n/a_c_lt_p";;
  if t.c >= t.p then
    ppl0DropAtP := wittList[t.p] - lcsDims[t.p];;
    ppl0DropOk := (ppl0DropAtP >= 2);;
    if ppl0DropOk then ppl0DropOkStr := "true"; else ppl0DropOkStr := "false"; fi;
    if not ppl0DropOk then
      stopHit := true;
      stopDetail := Concatenation("P_PL_0_NO_DROP_AT_P: target=", t.label, " drop=", String(ppl0DropAtP), " (expected >=2)");
      Print("STOP: ", stopDetail, "\n");
      continue;
    fi;
  fi;

  ## ---- theta, tau automorphisms (exact, on actual group elements) ----
  zElt := (xG*yG)^-1;;
  thetaHom := GroupHomomorphismByImages(P, P, [xG,yG], [yG,xG]);;
  tauHom := GroupHomomorphismByImages(P, P, [xG,yG], [yG,zElt]);;
  if thetaHom = fail or tauHom = fail then
    stopHit := true;
    stopDetail := Concatenation("HOMOMORPHISM_CONSTRUCTION_FAILED: target=", t.label);
    Print("STOP: ", stopDetail, "\n");
    continue;
  fi;

  pcgs := Pcgs(P);;
  weightOfGen := [];;
  for i in [1..Length(pcgs)] do
    for k in [1..Length(lcs)-1] do
      if pcgs[i] in lcs[k] and not (pcgs[i] in lcs[k+1]) then
        weightOfGen[i] := k;
        break;
      fi;
    od;
  od;

  DegreeKComponent := function(g, k)
    local expv, idxs;
    expv := ExponentsOfPcElement(pcgs, g);
    idxs := Filtered([1..Length(pcgs)], i -> weightOfGen[i] = k);
    return List(idxs, i -> expv[i]) mod t.p;
  end;;
  CheckPureWeight := function(g, k)
    local expv, i;
    expv := ExponentsOfPcElement(pcgs, g);
    for i in [1..Length(pcgs)] do
      if weightOfGen[i] < k and expv[i] mod t.p <> 0 then return false; fi;
    od;
    return true;
  end;;
  BuildLinOp := function(hom, k)
    local idxs, basisElts, M, i, img, ok;
    idxs := Filtered([1..Length(pcgs)], i -> weightOfGen[i] = k);
    basisElts := List(idxs, i -> pcgs[i]);
    M := [];  ok := true;
    for i in [1..Length(basisElts)] do
      img := Image(hom, basisElts[i]);
      if not CheckPureWeight(img, k) then ok := false; fi;
      Add(M, DegreeKComponent(img, k));
    od;
    return rec(matrix:=M, pure_weight_ok:=ok);
  end;;
  SolveHexKernel := function(k)
    local thOp, tauOp, thM, tauM, tau2M, dim, I, A1, A2, combinedM, i, ker;
    thOp := BuildLinOp(thetaHom, k);  tauOp := BuildLinOp(tauHom, k);
    thM := thOp.matrix;  tauM := tauOp.matrix;
    dim := Length(thM);
    if dim = 0 then
      return rec(dim_layer:=0, kernel_dim:=0, theta_pure_ok:=thOp.pure_weight_ok, tau_pure_ok:=tauOp.pure_weight_ok);
    fi;
    I := IdentityMat(dim, GF(t.p));
    A1 := (I + thM) * One(GF(t.p));
    tau2M := tauM * tauM;
    A2 := (I + tauM + tau2M) * One(GF(t.p));
    combinedM := List([1..dim], i -> Concatenation(A1[i], A2[i]));
    ker := NullspaceMat(combinedM);
    return rec(dim_layer:=dim, kernel_dim:=Length(ker),
               theta_pure_ok:=thOp.pure_weight_ok, tau_pure_ok:=tauOp.pure_weight_ok);
  end;;

  perDegree := [];;
  hkSumMeasured := 0;;  hkSumPredicted := 0;;
  for k in [2..t.c] do
    r := SolveHexKernel(k);;
    if not (r.theta_pure_ok and r.tau_pure_ok) then
      stopHit := true;
      stopDetail := Concatenation("PURE_WEIGHT_CHECK_FAILED: target=", t.label, " k=", String(k));
      Print("STOP: ", stopDetail, "\n");
      break;
    fi;
    hExp := HK[k];;
    defK := r.kernel_dim - hExp;;
    if k < t.p and defK <> 0 then
      stopHit := true;
      stopDetail := Concatenation("S_PL_2_DEF_K_NONZERO_BELOW_P: target=", t.label, " k=", String(k),
                                    " measured=", String(r.kernel_dim), " H_k=", String(hExp));
      Print("STOP: ", stopDetail, "\n");
      break;
    fi;
    zoneStr := "excess";;
    if k < t.p then zoneStr := "canary"; fi;
    Add(perDegree, rec(k:=k, dim_layer:=r.dim_layer, kernel_dim:=r.kernel_dim, H_k:=hExp, def_k:=defK,
                        zone:=zoneStr));
    hkSumMeasured := hkSumMeasured + r.kernel_dim;;
    hkSumPredicted := hkSumPredicted + hExp;;
  od;
  if stopHit then continue; fi;

  Add(results, rec(
    label:=t.label, p:=t.p, c:=t.c, kind:=t.kind,
    order:=order, exponent_ok:=expOk, gamma_c_plus_1_trivial:=gammaTrivial,
    lcs_dims:=lcsDims, witt_list:=wittList,
    p_pl_0_drop_at_p:=ppl0DropAtP, p_pl_0_drop_ok:=ppl0DropOkStr,
    per_degree:=perDegree,
    def_c_p_measured:=hkSumMeasured, def_c_p_predicted_H:=hkSumPredicted, def_c_p:=(hkSumMeasured-hkSumPredicted)
  ));
  Print(t.label, ": order=", order, " lcs_dims=", lcsDims, " P-PL-0 drop@p=", ppl0DropAtP,
        " sum(h_k^meas, k=2..c)=", hkSumMeasured, " sum(H_k, k=2..c)=", hkSumPredicted, "\n");
od;

if stopHit then
  out := Concatenation("{",
    "\"schema\":\"shadow-atelier/pl_lab1_v1\",",
    "\"stop_code\":", JStr(stopDetail), "",
    "}");
  WriteFile("search/certs/pl_lab1_v1_20260811.json", out);
  Print("Wrote STOP cert. PL_LAB1_STOP\n");
fi;

## ---- JSON output (only if no STOP) ----
if not stopHit then
JPerDeg := function(r)
  return Concatenation("{\"k\":", String(r.k), ",\"dim_layer\":", String(r.dim_layer),
    ",\"kernel_dim\":", String(r.kernel_dim), ",\"H_k\":", String(r.H_k),
    ",\"def_k\":", String(r.def_k), ",\"zone\":", JStr(r.zone), "}");
end;;

JRec := function(r)
  local parts;
  parts := [
    Concatenation("\"label\":", JStr(r.label)),
    Concatenation("\"p\":", String(r.p)),
    Concatenation("\"c\":", String(r.c)),
    Concatenation("\"kind\":", JStr(r.kind)),
    Concatenation("\"order\":", String(r.order)),
    Concatenation("\"exponent_ok\":", JB(r.exponent_ok)),
    Concatenation("\"gamma_c_plus_1_trivial\":", JB(r.gamma_c_plus_1_trivial)),
    Concatenation("\"lcs_dims\":", JArr(List(r.lcs_dims, String))),
    Concatenation("\"witt_list\":", JArr(List(r.witt_list, String))),
    Concatenation("\"p_pl_0_drop_at_p\":", String(r.p_pl_0_drop_at_p)),
    Concatenation("\"p_pl_0_drop_ok\":", JStr(r.p_pl_0_drop_ok)),
    Concatenation("\"per_degree\":[", JoinC(List(r.per_degree, JPerDeg), ","), "]"),
    Concatenation("\"def_c_p_measured\":", String(r.def_c_p_measured)),
    Concatenation("\"def_c_p_predicted_H\":", String(r.def_c_p_predicted_H)),
    Concatenation("\"def_c_p\":", String(r.def_c_p))
  ];
  return Concatenation("{", JoinC(parts, ","), "}");
end;;

controls := Filtered(results, r -> r.kind = "control");;
mains := Filtered(results, r -> r.kind = "main");;
controlsAllDefZero := ForAll(controls, r -> r.def_c_p = 0);;
mainsDefAtC := List(mains, r -> rec(label:=r.label, def:=r.def_c_p));;

out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/pl_lab1_v1\",",
  "\"authority\":\"", "\\u88c1\\u5b9a774/776/779/781 (\\u53f8\\u4ee4\\u5854), docs/notes/post_lazard_window_design_v1_addendum_a.md (\\u4fee\\u7406\\u6e08\\u4ed5\\u69d8: DEF-PL'/P-PL-0/1'/2'/3')\",",
  "\"scope_disclosure\":\"", "h_k^meas\\u306f\\u7d14\\u7cb9\\u6b21\\u6570k\\u306e\\u30b0\\u30ec\\u30fc\\u30c9\\u7247\\u65b9\\u3067\\u306e\\u3081\\u3001\\u4f4e\\u6b21\\u6570\\u90e8\\u5206\\u3068\\u306e\\u30af\\u30ed\\u30b9\\u9805(\\u5e30\\u7d0d\\u7684\\u30ea\\u30d5\\u30c8\\u88dc\\u6b63)\\u306f\\u672a\\u5b9f\\u65bd\\u3002k<p\\u3067\\u306fLazard\\u306e\\u570f\\u540c\\u5024\\u6027\\u3067s_k^grp=h_k^meas=H_k\\u304c\\u4fdd\\u8a3c\\u3055\\u308c\\u308b(\\u547d\\u984c PLA-1)\\u306e\\u3067\\u3053\\u306e\\u65b7\\u308a\\u306f\\u4e0d\\u6d3b\\u6027\\u3002k\\u2265p\\u3067\\u306f h_k^meas \\u306f s_k^grp \\u306e\\u4e0b\\u9650\\u898b\\u7a4d\\u3082\\u308a\\u3068\\u3057\\u3066\\u8aad\\u3080\\u3079\\u304d\\u3067\\u3001\\u78ba\\u5b9a\\u5024\\u3067\\u306f\\u306a\\u3044\\u3002\",",
  "\"pla_gap_1_resolution\":\"CAL-B4\\u306e7^41\\u306f\\u672c\\u6e2c\\u5b9a\\u3067\\u4f7f\\u7528\\u3057\\u3066\\u3044\\u306a\\u3044(\\u65e2\\u5b58\\u30aa\\u30d6\\u30b8\\u30a7\\u30af\\u30c8\\u306f\\u672a\\u767a\\u898b\\u3068\\u4ee5\\u524d\\u306eExplore\\u3067\\u78ba\\u8a8d\\u6e08\\u307f)\\u3002p7c7\\u306f\\u81ea\\u5206\\u3067Exponent:=7\\u3092\\u660e\\u793a\\u3057\\u3066\\u65b0\\u898f\\u69cb\\u6210\\u3057\\u3001x^7=1/y^7=1\\u3092\\u78ba\\u8a8d\\u6e08\\u307f\\u3002\",",
  "\"witt_2_k_reference\":", JArr(List(WITT, String)), ",",
  "\"H_k_reference\":", JArr(List(HK, String)), ",",
  "\"targets\":[", JoinC(List(results, JRec), ","), "],",
  "\"controls_all_def_c_p_zero\":", JB(controlsAllDefZero), ",",
  "\"no_verdict_note\":\"S-PL-4 compliance: raw values (order, lcs_dims, kernel_dim, def_k, def_c_p) and booleans only. \\u5224\\u5b9a\\u8a9e(\\u679d L / \\u679d B \\u306e\\u65ad\\u5b9a)\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002\",",
  "\"stop_code\":null",
  "}"
);;

WriteFile("search/certs/pl_lab1_v1_20260811.json", out);;
Print("Wrote search/certs/pl_lab1_v1_20260811.json\n");
Print("PL_LAB1_DONE\n");
fi;
QUIT;
