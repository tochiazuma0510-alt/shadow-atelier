## exp5_normchk_isotypic.g -- NORM-CHK (裁定783(1)): full S3-isotypic
## decomposition (m_triv, m_sgn, m_std) of the MEASURED gamma_p/gamma_{p+1}
## via exact nullspace computations (avoids mod-p trace ambiguity -- at
## p7c7, dim_layer=12 > p=7 makes raw trace mod p ambiguous by multiples
## of p; nullspace/rank computations have no such ambiguity).
## S3 acting via theta (order 2, transposition), tau (order 3):
##   triv: theta=+1, tau=+1  -> ker(1-theta) cap ker(1-tau)
##   sgn:  theta=-1, tau=+1  -> ker(1+theta) cap ker(1-tau)
##   std:  (already computed in pl_lab1_v1.g as kernel_dim) -> ker(1+theta) cap ker(1+tau+tau^2)
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

DoTarget := function(path, p, k)
  local P, xG, yG, lcs, pcgs, weightOfGen, i, kk, zElt, thetaHom, tauHom,
        DegreeKComponent, CheckPureWeight, BuildLinOp, thOp, tauOp, thM, tauM, tau2M,
        dimLayer, I, mTrivMat, mSgnMat, mStdMat1, mStdMat2, combTriv, combSgn, combStd, j,
        kerTriv, kerSgn, kerStd;
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
  I := IdentityMat(dimLayer, GF(p));;
  tau2M := tauM * tauM;;

  ## triv: ker(1-theta) cap ker(1-tau)
  mTrivMat := (I - thM*One(GF(p)));;
  combTriv := List([1..dimLayer], i -> Concatenation(mTrivMat[i], (I-tauM*One(GF(p)))[i]));;
  kerTriv := NullspaceMat(combTriv);;

  ## sgn: ker(1+theta) cap ker(1-tau)
  mSgnMat := (I + thM*One(GF(p)));;
  combSgn := List([1..dimLayer], i -> Concatenation(mSgnMat[i], (I-tauM*One(GF(p)))[i]));;
  kerSgn := NullspaceMat(combSgn);;

  ## std (recompute for cross-check against pl_lab1_v1's kernel_dim): ker(1+theta) cap ker(1+tau+tau^2)
  combStd := List([1..dimLayer], i -> Concatenation((I+thM*One(GF(p)))[i], (I+tauM*One(GF(p))+tau2M*One(GF(p)))[i]));;
  kerStd := NullspaceMat(combStd);;

  Print("p=", p, " k=", k, " dim_layer=", dimLayer,
        " m_triv=", Length(kerTriv), " m_sgn=", Length(kerSgn), " m_std=", Length(kerStd),
        " sum_check(m_triv+m_sgn+2*m_std)=", Length(kerTriv)+Length(kerSgn)+2*Length(kerStd),
        " (should equal dim_layer=", dimLayer, ")\n");
end;;

DoTarget("search/probe/pl_lab1_v1/PQ_OUTPUT_p5c5.g", 5, 5);
DoTarget("search/probe/pl_lab1_v1/PQ_OUTPUT_p7c7.g", 7, 7);

Print("EXP5_DONE\n");
QUIT;
