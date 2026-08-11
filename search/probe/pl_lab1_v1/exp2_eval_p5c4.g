## exp2_eval_p5c4.g -- W-a/W-c experiment on P_{4,5}: verify LCS dims, build
## theta/tau automorphisms, extract degree-graded action, solve linearized
## hexagon kernel dimension per degree (m=0 layer), compare to dim S_k.
Read("search/probe/pl_lab1_v1/PQ_OUTPUT_p5c4.g");;
P := F;;  MapImagesP := ShallowCopy(MapImages);;
Unbind(F);; Unbind(MapImages);;

x := MapImagesP[1];;  y := MapImagesP[2];;
p := 5;;  c := 4;;

Print("|P| = ", Size(P), " (predict 5^8=", 5^8, ")\n");
Print("Exponent test: x^5=1? ", x^5 = Identity(P), "  y^5=1? ", y^5 = Identity(P), "\n");

lcs := LowerCentralSeriesOfGroup(P);;
Print("LCS length: ", Length(lcs), "\n");
lcsDims := List([1..Length(lcs)-1], i -> LogInt(Size(lcs[i])/Size(lcs[i+1]), p));;
Print("LCS layer dims: ", lcsDims, " (predict Witt(2,k) k=1..4 = [2,1,2,3])\n");
Print("gamma_5(P) trivial? ", Size(lcs[Length(lcs)]) = 1, "\n");

# theta: x<->y ; tau: x->y, y->z=(xy)^-1
zElt := (x*y)^-1;;
thetaHom := GroupHomomorphismByImages(P, P, [x,y], [y,x]);;
tauHom := GroupHomomorphismByImages(P, P, [x,y], [y,zElt]);;
Print("thetaHom well-defined? ", thetaHom <> fail, "\n");
Print("tauHom well-defined? ", tauHom <> fail, "\n");

pcgs := Pcgs(P);;
Print("pcgs length: ", Length(pcgs), "\n");

# determine weight (LCS degree) of each pcgs generator: weight k iff gen in gamma_k \ gamma_{k+1}
weightOfGen := [];;
for i in [1..Length(pcgs)] do
  for k in [1..Length(lcs)-1] do
    if pcgs[i] in lcs[k] and not (pcgs[i] in lcs[k+1]) then
      weightOfGen[i] := k;
      break;
    fi;
  od;
od;
Print("weight of each pcgs generator: ", weightOfGen, "\n");

# for a group element g, get its degree-k COMPONENT: exponents of g w.r.t. pcgs,
# restricted to positions of weight exactly k (this is the projection to gamma_k/gamma_{k+1}
# when g in gamma_k -- exponents at weight <k positions should be 0 if g in gamma_k)
DegreeKComponent := function(g, k)
  local expv, idxs, i;
  expv := ExponentsOfPcElement(pcgs, g);
  idxs := Filtered([1..Length(pcgs)], i -> weightOfGen[i] = k);
  return List(idxs, i -> expv[i]) mod p;
end;;

# sanity: for g in gamma_k, exponents at weight<k positions should ALL be 0
CheckPureWeight := function(g, k)
  local expv, i;
  expv := ExponentsOfPcElement(pcgs, g);
  for i in [1..Length(pcgs)] do
    if weightOfGen[i] < k and expv[i] mod p <> 0 then
      return false;
    fi;
  od;
  return true;
end;;

# build theta-bar, tau-bar matrices on degree k, using pcgs weight-k generators as basis
BuildLinOp := function(hom, k)
  local idxs, basisElts, M, i, img, comp, ok;
  idxs := Filtered([1..Length(pcgs)], i -> weightOfGen[i] = k);
  basisElts := List(idxs, i -> pcgs[i]);
  M := [];
  ok := true;
  for i in [1..Length(basisElts)] do
    img := Image(hom, basisElts[i]);
    if not CheckPureWeight(img, k) then ok := false; fi;
    comp := DegreeKComponent(img, k);
    Add(M, comp);
  od;
  return rec(matrix:=M, pure_weight_ok:=ok);
end;;

# solve dim ker(1+thetabar) intersect ker(1+taubar+tau2bar) over F_p, degree k
SolveHexKernel := function(k)
  local thOp, tauOp, thM, tauM, tau2M, dim, I, A1, A2, combinedM, i, ker;
  thOp := BuildLinOp(thetaHom, k);
  tauOp := BuildLinOp(tauHom, k);
  thM := thOp.matrix;  tauM := tauOp.matrix;
  dim := Length(thM);
  if dim = 0 then
    return rec(dim_layer:=0, kernel_dim:=0, theta_pure_ok:=thOp.pure_weight_ok, tau_pure_ok:=tauOp.pure_weight_ok);
  fi;
  I := IdentityMat(dim, GF(p));
  # convention: M[i] = coords of image of basis vector i, so operator acts as v -> v*M
  # (row vector on the left). (1+thetabar) as matrix (I+thM); kernel = {v : v*(I+thM)=0}.
  A1 := (I + thM) * One(GF(p));
  tau2M := tauM * tauM;  # tau^2-bar = tau-bar squared (compose the induced linear map with itself)
  A2 := (I + tauM + tau2M) * One(GF(p));
  # combined system: v*(I+thM)=0 AND v*(I+tauM+tau2M)=0 <=> v * [A1 | A2] = 0
  # (side-by-side column concatenation, same dim rows)
  combinedM := List([1..dim], i -> Concatenation(A1[i], A2[i]));
  ker := NullspaceMat(combinedM);
  return rec(dim_layer:=dim, kernel_dim:=Length(ker),
             theta_pure_ok:=thOp.pure_weight_ok, tau_pure_ok:=tauOp.pure_weight_ok);
end;;

dimS_known := [0,0,1,0];; # k=1..4 (frozen per design doc)
for k in [1..c] do
  Print("=== degree k=", k, " ===\n");
  Print(SolveHexKernel(k), "  (dim S_", k, " known = ", dimS_known[k], ")\n");
od;

Print("EXP2_DONE\n");
QUIT;
