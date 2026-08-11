## exp4_normchk_traces.g -- NORM-CHK (裁定783(1)): extract Trace(theta-bar),
## Trace(tau-bar) on the MEASURED gamma_p/gamma_{p+1}(P_{c,p}) for the two
## main targets (p5c5 at k=5, p7c7 at k=7), to feed the S3-isotypic
## decomposition of R_p = ker(Lambda_p -> measured).
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

DoTarget := function(path, p, k)
  local P, xG, yG, lcs, pcgs, weightOfGen, i, kk, zElt, thetaHom, tauHom,
        DegreeKComponent, CheckPureWeight, BuildLinOp, thOp, tauOp, thM, tauM,
        traceTheta, traceTau, dimLayer, j;
  Read(path);
  P := F;;  xG := MapImages[1];;  yG := MapImages[2];;
  Unbind(F);;  Unbind(MapImages);;

  lcs := LowerCentralSeriesOfGroup(P);;
  pcgs := Pcgs(P);;
  weightOfGen := [];;
  for i in [1..Length(pcgs)] do
    for kk in [1..Length(lcs)-1] do
      if pcgs[i] in lcs[kk] and not (pcgs[i] in lcs[kk+1]) then
        weightOfGen[i] := kk;
        break;
      fi;
    od;
  od;

  zElt := (xG*yG)^-1;;
  thetaHom := GroupHomomorphismByImages(P, P, [xG,yG], [yG,xG]);;
  tauHom := GroupHomomorphismByImages(P, P, [xG,yG], [yG,zElt]);;

  DegreeKComponent := function(g, kdeg)
    local expv, idxs;
    expv := ExponentsOfPcElement(pcgs, g);
    idxs := Filtered([1..Length(pcgs)], i -> weightOfGen[i] = kdeg);
    return List(idxs, i -> expv[i]) mod p;
  end;;
  CheckPureWeight := function(g, kdeg)
    local expv, i;
    expv := ExponentsOfPcElement(pcgs, g);
    for i in [1..Length(pcgs)] do
      if weightOfGen[i] < kdeg and expv[i] mod p <> 0 then return false; fi;
    od;
    return true;
  end;;
  BuildLinOp := function(hom, kdeg)
    local idxs, basisElts, M, i, img, ok;
    idxs := Filtered([1..Length(pcgs)], i -> weightOfGen[i] = kdeg);
    basisElts := List(idxs, i -> pcgs[i]);
    M := [];  ok := true;
    for i in [1..Length(basisElts)] do
      img := Image(hom, basisElts[i]);
      if not CheckPureWeight(img, kdeg) then ok := false; fi;
      Add(M, DegreeKComponent(img, kdeg));
    od;
    return rec(matrix:=M, pure_weight_ok:=ok);
  end;;

  thOp := BuildLinOp(thetaHom, k);;  tauOp := BuildLinOp(tauHom, k);;
  thM := thOp.matrix;;  tauM := tauOp.matrix;;
  dimLayer := Length(thM);;
  traceTheta := 0;;
  for j in [1..dimLayer] do traceTheta := (traceTheta + thM[j][j]) mod p; od;
  traceTau := 0;;
  for j in [1..dimLayer] do traceTau := (traceTau + tauM[j][j]) mod p; od;

  Print("p=", p, " k=", k, " dim_layer=", dimLayer, " trace(theta-bar) mod p = ", traceTheta,
        " trace(tau-bar) mod p = ", traceTau, " theta_pure_ok=", thOp.pure_weight_ok,
        " tau_pure_ok=", tauOp.pure_weight_ok, "\n");
end;;

DoTarget("search/probe/pl_lab1_v1/PQ_OUTPUT_p5c5.g", 5, 5);
DoTarget("search/probe/pl_lab1_v1/PQ_OUTPUT_p7c7.g", 7, 7);

Print("EXP4_DONE\n");
QUIT;
