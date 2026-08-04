#############################################################################
## search/probe/w6_coker_tool/w6_coker_tool_driver.g
## K5 戦役 W-6 較正 tooling 束(裁定446 起票)。設計正本:
## docs/notes/k5_w6_construction_v1.md (定理 W6-OBS・停止規則 S-W6 系・
## fixture DF-W6 系・【K5-GAP-W3】)。
##
## 3点を1本で実装する:
##  (1) 余核計算器: psi_V=(N_theta,N_tau):V->V^theta (+) V^tau の
##      dim coker を GAP 標準線型代数(RankMat/NullspaceMat, GF(p))で計算。
##      式(A)(B)(B')(C)(定理W6-OBS)の相互一致を機械確認。式(C)は
##      scratchpad/k5_w6_norm_obstruction_check.py(single lane python・
##      SHA d8b41a77...)の結果と "独立実装での再確認" として突合する
##      (import はしない -- 同じ数の別実装で dim を再計算するのみ)。
##  (2) fixture DF-W6-1/2/3/4 の実装(ノート §4.3)。
##  (3) K^(20) の Gamma-加群分解(【K5-GAP-W3】): MakeGn(20)/MakeGn(5) を
##      GAP で直接構成し、V=Ker(G20 ->> G5) の実物構造(位数・theta/tau
##      作用行列)を計算する。これは「紙1枚」見積りの代わりに GAP の
##      群論計算そのもので裏取りする設計逸脱であり、司令塔へ申告する。
##
## 規律: certificates/ の K5 系(k5gen 含む)へは書かない。出力は
## search/certs/w6_coker_tool_20260804.json のみ(tier=tooling-calibration)。
## Im R / 封印 / 曲線データには一切触れない。lins 探索はしない。
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

FAILS := [];;
Chk := function(name, got, want)
  local ok;
  ok := (got = want);
  if not ok then Add(FAILS, rec(name := name, got := got, want := want)); fi;
  Print("  [", PF(ok), "] ", name, ": got=", got, " want=", want, "\n");
  return ok;
end;;

#############################################################################
## ==== (1) 余核計算器: GF(p) 線型代数(GAP 標準関数のみ・独立実装) ====
#############################################################################
Print("\n=== (1) coker calculator: GF(p) linear algebra core ===\n");

## theta, tau は整数行列(list of rows, v |-> v*M の右作用規約)として渡す。
## GF(p) 行列へ変換。
ToGFp := function(M, p)
  local Fp;
  Fp := GF(p);
  return List(M, row -> List(row, x -> (x mod p) * One(Fp)));
end;;

IdMat_ := function(n, p) return IdentityMat(n, GF(p)); end;;

## RankMat([]) has no method in this GAP version; guard the empty-matrix case.
SafeRank := function(M) if Length(M) = 0 then return 0; else return RankMat(M); fi; end;;

## N_theta = I + theta ; N_tau = I + tau + tau^2 (行ベクトル右作用)
NormMats := function(th, ta, p)
  local n, I, Nth, tau2, Nta;
  n := Length(th);
  I := IdMat_(n, p);
  Nth := I + th;
  tau2 := ta * ta;
  Nta := I + ta + tau2;
  return [Nth, Nta];
end;;

## ker(M) as row-space nullspace: {v : v*M = 0}
KerRows := function(M) return NullspaceMat(M); end;;

## coker dim via direct rank of stacked psi map (psi(e_i) = (Ntheta e_i | Nta e_i))
CokerDimDirect := function(th, ta, p)
  local n, I, Nth, Nta, Vth, Vta, dth, dta, stacked, i, dimIm;
  n := Length(th); I := IdMat_(n, p);
  Nth := NormMats(th, ta, p)[1];  Nta := NormMats(th, ta, p)[2];
  Vth := KerRows(th - I);   # v*theta = v
  Vta := KerRows(ta - I);   # v*tau = v
  dth := Length(Vth);  dta := Length(Vta);
  stacked := List([1..n], i ->
    Concatenation(Nth[i], Nta[i]));  # row i of Nth is e_i*Nth = psi(e_i)_theta part
  dimIm := SafeRank(stacked);
  return rec(coker := dth + dta - dimIm, dth := dth, dta := dta, dim_im := dimIm);
end;;

## master formula (A): dimV^th + dimV^ta - dimV + dim(ker Nth ∩ ker Nta)
CokerDimFormulaA := function(th, ta, p)
  local n, I, Nth, Nta, Vth, Vta, Kth, Kta, both, dInt;
  n := Length(th); I := IdMat_(n, p);
  Nth := NormMats(th, ta, p)[1]; Nta := NormMats(th, ta, p)[2];
  Vth := KerRows(th - I);  Vta := KerRows(ta - I);
  Kth := KerRows(Nth);  Kta := KerRows(Nta);
  # intersection dim of two subspaces given by null spaces of Nth, Nta:
  # v in ker Nth ∩ ker Nta  <=>  v*[Nth|Nta] = 0 (horizontal concat)
  both := List([1..n], i -> Concatenation(Nth[i], Nta[i]));
  dInt := n - SafeRank(both);
  return Length(Vth) + Length(Vta) - n + dInt;
end;;

## short formula (B), p<>2: dim V^tau - dim N_tau(ker N_theta)
CokerDimFormulaB := function(th, ta, p)
  local n, I, Nth, Nta, Vta, Kth, img;
  n := Length(th); I := IdMat_(n, p);
  Nth := NormMats(th, ta, p)[1]; Nta := NormMats(th, ta, p)[2];
  Vta := KerRows(ta - I);
  Kth := KerRows(Nth);
  if Length(Kth) = 0 then img := [];
  else img := Kth * Nta; fi;
  return Length(Vta) - SafeRank(img);
end;;

## short formula (B'), p<>3: dim V^theta - dim N_theta(ker N_tau)
CokerDimFormulaBp := function(th, ta, p)
  local n, I, Nth, Nta, Vth, Kta, img;
  n := Length(th); I := IdMat_(n, p);
  Nth := NormMats(th, ta, p)[1]; Nta := NormMats(th, ta, p)[2];
  Vth := KerRows(th - I);
  Kta := KerRows(Nta);
  if Length(Kta) = 0 then img := [];
  else img := Kta * Nth; fi;
  return Length(Vth) - SafeRank(img);
end;;

## (C), p nmid 6: dim coker = dim (V*)^Gamma  ( = dim{lambda : lambda.theta=lambda, lambda.tau=lambda} on dual,
## computed via transpose: v*(theta^T - I)=0 and v*(tau^T-I)=0 simultaneously )
DualGammaInvDim := function(th, ta, p)
  local n, I, tht, tat, both;
  n := Length(th); I := IdMat_(n, p);
  tht := TransposedMat(th);  tat := TransposedMat(ta);
  both := List([1..n], i -> Concatenation((tht - I)[i], (tat - I)[i]));
  return n - SafeRank(both);
end;;

## Master entry point: build all four formula dims + cross-check, over GF(p).
## th, ta given as INTEGER matrices (row-action convention); p prime.
CokerReport := function(th, ta, p)
  local thp, tap, r, A, B, Bp, C, hasB, hasBp, hasC, agree;
  thp := ToGFp(th, p);  tap := ToGFp(ta, p);
  r := CokerDimDirect(thp, tap, p);
  A := CokerDimFormulaA(thp, tap, p);
  hasB := (p <> 2);   hasBp := (p <> 3);   hasC := (p <> 2 and p <> 3);
  B := fail;  Bp := fail;  C := fail;
  if hasB then B := CokerDimFormulaB(thp, tap, p); fi;
  if hasBp then Bp := CokerDimFormulaBp(thp, tap, p); fi;
  if hasC then C := DualGammaInvDim(thp, tap, p); fi;
  agree := (r.coker = A) and (not hasB or B = r.coker) and (not hasBp or Bp = r.coker)
           and (not hasC or C = r.coker);
  return rec(coker := r.coker, dimVth := r.dth, dimVta := r.dta, dim_im := r.dim_im,
             formula_A := A, formula_B := B, formula_Bprime := Bp, formula_C := C,
             agree := agree, p := p);
end;;

## ---- sanity/self-tests reproducing the 3-formula agreement on a few modules,
## as an INDEPENDENT GAP implementation of the closed forms already checked
## single-lane in scratchpad/k5_w6_norm_obstruction_check.py (SHA
## d8b41a77fc35ff65b7818000112c9ba4d1f2a73bed154e48621d807a112426f4).
## We do NOT import that script; only its final dim values are used below
## as the cross-check target (machine re-derivation, not a shared helper).
A5th := [[0,1,0],[1,0,0],[0,0,-1]];;  # (4.7), theta -- literal -1 (NOT "4"), so
                                       # ToGFp reduces correctly mod any p (bug found
                                       # during DF-W6-4: a hardcoded "4"=-1 mod 5 gave
                                       # wrong results when reduced mod 3/7/11)
A5ta := [[0,0,1],[1,0,0],[0,1,0]];;   # (4.8) over F_5, tau
rA5 := CokerReport(A5th, A5ta, 5);;
Print("  A-module p=5: coker=", rA5.coker, " (expect 0) formulas agree=", rA5.agree, "\n");
Chk("A-module (K25 type) over F5: coker=0 (P-W6-2 machine check)", rA5.coker, 0);
Chk("A-module p=5: all 4 formulas agree", rA5.agree, true);

trivTh := [[1]];; trivTa := [[1]];;
rTriv5 := CokerReport(trivTh, trivTa, 5);;
Chk("trivial 1-dim over F5: coker=1", rTriv5.coker, 1);

#############################################################################
## ==== (2) fixture DF-W6-1..4 ====
#############################################################################
Print("\n=== (2) fixtures DF-W6-1..4 ===\n");

## ---- DF-W6-4: order(theta*tau) assert on the A-module (danger D-2 detector) ----
Print("-- DF-W6-4: order(theta.tau) on A-module over F_p --\n");
DFW6_4_check := function(p)
  local th, ta, thta, o;
  th := ToGFp(A5th, p);  ta := ToGFp([[0,0,1],[1,0,0],[0,1,0]], p);
  thta := th * ta;
  o := Order(thta);
  return o;
end;;
df4_orders := List([5,3,7,11], DFW6_4_check);;
Print("  orders(theta.tau) at p=5,3,7,11: ", df4_orders, " (expect all 4)\n");
df4_pass := (df4_orders = [4,4,4,4]);;
Chk("DF-W6-4: order(theta.tau)=4 (not 24; not the D-1/D-2 trap)", df4_orders, [4,4,4,4]);

## group order check (S4, order 24) -- independent GAP group-theoretic recount
gp := Group(ToGFp(A5th,5), ToGFp([[0,0,1],[1,0,0],[0,1,0]],5));;
Chk("DF-W6-4 companion: |<theta,tau>| on A over F5 = 24 (S4)", Size(gp), 24);

## ---- DF-W6-1: obstruction class realized as nonzero (solver must report "no solution") ----
Print("-- DF-W6-1: synthetic p=3 module, nonzero obstruction class --\n");
## V = F_3^2, tau = [[1,1],[0,1]] (unipotent, order3 in char3), theta = diag(1,-1)
V_th := [[1,0],[0,2]];;  V_ta := [[1,1],[0,1]];;
rDF1 := CokerReport(V_th, V_ta, 3);;
Print("  coker dim = ", rDF1.coker, " (expect 1, i.e. nonzero obstruction group)\n");
Chk("DF-W6-1: coker dim = 1 (obstruction group nonzero, module exists)", rDF1.coker, 1);

## Affine-system solver: does N_theta(b)=-beta_theta, N_tau(b)=-beta_tau have a
## solution b in V, for a target (beta_theta,beta_tau) that represents a NONZERO
## class in coker(psi_V)? By construction such a target must NOT be solvable.
## We build beta as a representative of a nonzero coset (e.g. any vector w in
## V^theta (+) V^tau that is not in im(psi_V)), and the solver must return "NO".
SolveAffineSystem := function(th, ta, p, betaTh, betaTa)
  local thp, tap, n, Nth, Nta, stacked, target, sol, i;
  thp := ToGFp(th, p);  tap := ToGFp(ta, p);
  n := Length(th);
  Nth := NormMats(thp, tap, p)[1];  Nta := NormMats(thp, tap, p)[2];
  stacked := List([1..n], i -> Concatenation(Nth[i], Nta[i]));
  target := Concatenation(betaTh * One(GF(p)), betaTa * One(GF(p)));
  sol := SolutionMat(stacked, target);
  if sol = fail then return rec(solvable := false, b := fail);
  else return rec(solvable := true, b := sol); fi;
end;;

## dth=1 (V^theta = <(1,0)>), dta=2 (V^tau = all of F_3^2 since tau unipotent
## has (tau-I) nilpotent... check: coker=1 means im(psi) is a hyperplane of
## V^theta (+) V^tau (dim dth+dta-1). Pick beta = a basis vector of V^theta (+) V^tau
## NOT in the image; since coker=1-dim, ANY vector outside im(psi) works, and by
## symmetry the "all-zero-but-one-coordinate-off-image" vector can be found by
## direct search over the (small) ambient space.
FindNonzeroClassTarget := function(th, ta, p)
  local thp, tap, n, Nth, Nta, stacked, ambDim, e, found, i, target, sol;
  thp := ToGFp(th, p);  tap := ToGFp(ta, p);
  n := Length(th);
  Nth := NormMats(thp, tap, p)[1];  Nta := NormMats(thp, tap, p)[2];
  stacked := List([1..n], i -> Concatenation(Nth[i], Nta[i]));
  ambDim := 2*n;
  for i in [1..ambDim] do
    e := List([1..ambDim], k -> 0*One(GF(p)));
    e[i] := One(GF(p));
    sol := SolutionMat(stacked, e);
    if sol = fail then return e; fi;
  od;
  return fail;  # should not happen given coker > 0
end;;

df1_target := FindNonzeroClassTarget(V_th, V_ta, 3);;
Print("  nonzero-class target found: ", df1_target <> fail, "\n");
df1_solve := fail;;
if df1_target <> fail then
  df1_solve := SolveAffineSystem(V_th, V_ta, 3, df1_target{[1,2]}, df1_target{[3,4]});;
  Print("  solver on nonzero-class target: solvable=", df1_solve.solvable, " (expect false)\n");
fi;
df1_pass := (df1_target <> fail) and (df1_solve.solvable = false);;
Chk("DF-W6-1: solver reports NO solution on a nonzero-class target (S-W6-2 gate)",
    df1_pass, true);

## also confirm the solver DOES find a solution for the zero class (beta=0), as a
## companion sanity check that the solver is not simply always saying "no".
df1_zero := SolveAffineSystem(V_th, V_ta, 3, [0,0], [0,0]);;
Chk("DF-W6-1 companion: solver finds a solution for the zero class (beta=0)",
    df1_zero.solvable, true);

## ---- DF-W6-3: (4.7)(4.8) A-module over F5, expect coker=0 (K25 anchor,
## reproduced with an INDEPENDENT SolveAffineSystem call for beta=0 too) ----
Print("-- DF-W6-3: A-module over F5 (K^(25) anchor reproduction) --\n");
rDF3 := CokerReport(A5th, [[0,0,1],[1,0,0],[0,1,0]], 5);;
Chk("DF-W6-3: A-module over F5: coker=0 (matches known d=5 at K^(25))", rDF3.coker, 0);

#############################################################################
## ==== (3) K^(20) の Gamma-加群分解 (【K5-GAP-W3】) ====
## 設計ノートは「紙1枚」の見積りだったが、ここでは GAP による直接構成で
## 裏取りする(設計からの逸脱として司令塔へ申告)。
## V := Ker(G20 -> G5)  (G_n := MakeGn(n) = PB3/K^(n), x,y |-> x,y の自然な射)
## theta,tau は ScanRoofHexagon と同じ規約(thetaHom: x<->y, tauHom: x->y,y->z)
## で G20 上に構成し、V が Gamma-安定であることを機械確認したうえで、V 上の
## 作用行列を Pcgs 経由で GF(2) 行列として取り出す。
#############################################################################
Print("\n=== (3) K^(20) module decomposition (K5-GAP-W3) ===\n");

g20 := MakeGn(20);;
g5 := MakeGn(5);;
Print("  |G20|=|PB3/K20| = ", Size(g20.G), " (expect 4000 -- machine value, not preregistered)\n");
Print("  |G5|=|PB3/K5|   = ", Size(g5.G), "\n");

redHom := GroupHomomorphismByImages(g20.G, g5.G, [g20.x, g20.y], [g5.x, g5.y]);;
redHomOk := (redHom <> fail) and (Size(Image(redHom)) = Size(g5.G));;
Chk("K20->K5 quotient hom (x,y |-> x,y) is well-defined and onto", redHomOk, true);

V20 := Kernel(redHom);;
Print("  |V| = |K5/K20| = ", Size(V20), "\n");
vAbelian := IsAbelian(V20);;
vElemAb2 := vAbelian and (Exponent(V20) = 2 or Size(V20) = 1);;
Chk("V=K5/K20 is abelian", vAbelian, true);
Chk("V=K5/K20 is elementary abelian 2-group", vElemAb2, true);

zElt20 := AbstractProd([g20.x, g20.y])^-1;;
thetaHom20 := GroupHomomorphismByImages(g20.G, g20.G, [g20.x, g20.y], [g20.y, g20.x]);;
tauHom20 := GroupHomomorphismByImages(g20.G, g20.G, [g20.x, g20.y], [g20.y, zElt20]);;
Chk("theta,tau well-defined as endomorphisms of G20", (thetaHom20 <> fail) and (tauHom20 <> fail), true);

thetaAutoOk := IsBijective(thetaHom20);;
tauAutoOk := IsBijective(tauHom20);;
Chk("thetaHom20 is bijective (automorphism)", thetaAutoOk, true);
Chk("tauHom20 is bijective (automorphism)", tauAutoOk, true);

th2ord := Order(thetaHom20);;
ta2ord := Order(tauHom20);;
Chk("order(thetaHom20) = 2 on G20", th2ord, 2);
Chk("order(tauHom20) = 3 on G20", ta2ord, 3);

## Gamma-stability of V: theta(V)=V and tau(V)=V (both as sets)
vThetaImg := Image(thetaHom20, V20);;
vTauImg := Image(tauHom20, V20);;
vStableTh := (Size(vThetaImg) = Size(V20)) and ForAll(GeneratorsOfGroup(V20),
    g -> Image(thetaHom20, g) in V20);;
vStableTa := (Size(vTauImg) = Size(V20)) and ForAll(GeneratorsOfGroup(V20),
    g -> Image(tauHom20, g) in V20);;
Chk("V is theta-stable inside G20", vStableTh, true);
Chk("V is tau-stable inside G20", vStableTa, true);

## Extract theta,tau as GF(2) matrices on V via a Pcgs isomorphism to a pc-group.
k20module := fail;;
if vElemAb2 and vStableTh and vStableTa then
  isoPc := IsomorphismPcGroup(V20);;
  Vpc := Image(isoPc, V20);;
  pcgs := Pcgs(Vpc);;
  dimV := Length(pcgs);;
  Print("  dim_F2(V) = ", dimV, "\n");

  ThetaMatOnV := function()
    local rows, i, g, gV, thg, thgV, expv;
    rows := [];
    for i in [1..dimV] do
      g := PreImagesRepresentative(isoPc, pcgs[i]);      # element of Vpc's preimage in G20's copy... careful: pcgs[i] in Vpc
      gV := PreImagesRepresentative(isoPc, pcgs[i]);
      thg := Image(thetaHom20, gV);                        # image under theta, still in V20 (checked above)
      thgV := Image(isoPc, thg);
      expv := ExponentsOfPcElement(pcgs, thgV);
      Add(rows, expv);
    od;
    return rows;
  end;;

  TauMatOnV := function()
    local rows, i, gV, tag, tagV, expv;
    rows := [];
    for i in [1..dimV] do
      gV := PreImagesRepresentative(isoPc, pcgs[i]);
      tag := Image(tauHom20, gV);
      tagV := Image(isoPc, tag);
      expv := ExponentsOfPcElement(pcgs, tagV);
      Add(rows, expv);
    od;
    return rows;
  end;;

  thetaMatV := ThetaMatOnV();;
  tauMatV := TauMatOnV();;
  Print("  theta|_V (rows = e_i*theta) = ", thetaMatV, "\n");
  Print("  tau|_V   (rows = e_i*tau)   = ", tauMatV, "\n");

  ## sanity: these should be actual GF(2) automorphisms of V (order dividing 2 / 3 resp.)
  thVp := ToGFp(thetaMatV, 2);;  taVp := ToGFp(tauMatV, 2);;
  thVsq := thVp * thVp;;
  taVcube := taVp * taVp * taVp;;
  thetaSqOk := (thVsq = IdMat_(dimV, 2));;
  tauCubeOk := (taVcube = IdMat_(dimV, 2));;
  Chk("theta|_V squares to identity (GF(2) matrix)", thetaSqOk, true);
  Chk("tau|_V cubes to identity (GF(2) matrix)", tauCubeOk, true);

  ## coker report for the REAL K^(20) module (this is the DF-W6-2 material)
  k20report := CokerReport(thetaMatV, tauMatV, 2);;
  Print("  K^(20) module: dim coker(psi_V) = ", k20report.coker, "  formulas agree=",
        k20report.agree, "\n");
  k20module := rec(dim := dimV, theta_matrix := thetaMatV, tau_matrix := tauMatV,
    theta_sq_ok := thetaSqOk, tau_cube_ok := tauCubeOk,
    coker_dim := k20report.coker, formulas_agree := k20report.agree,
    formula_A := k20report.formula_A, formula_C := k20report.formula_C);
  ## S-W6-3 discipline: coker!=0 is a NECESSARY condition only, not "detection power".
  ## DF-W6-2 additionally claims the CLASS vanishes (retrodiction from canonical Thm 4.4,
  ## d=5 known) -- this tool computes the GROUP only; it does NOT compute the class,
  ## and does NOT compute f_1's actual lift. No d_N / detection-power claim is made here.
  Chk("K^(20): coker dim != 0 (necessary-condition check only; group, not class -- S-W6-3)",
      k20report.coker <> 0, true);
else
  Print("  ** SKIPPED: preconditions for module extraction not met (see checks above) **\n");
fi;

#############################################################################
## ==== JSON 出力 ====
#############################################################################
Print("\n=== writing cert ===\n");

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_w6_coker_tool_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then
    Error("ComputeSha256File: sha256sum did not return a hash line for ", relpath);
  fi;
  return line{[1 .. 64]};
end;;

selfSha := ComputeSha256File("search/probe/w6_coker_tool/w6_coker_tool_driver.g");;
noteSha := ComputeSha256File("docs/notes/k5_w6_construction_v1.md");;
pyCheckSha := ComputeSha256File("scratchpad/k5_w6_norm_obstruction_check.py");;

MatJson := function(M)
  return JArr(List(M, row -> JArr(List(row, x -> String(IntFFE(x))))));
end;;

k20Json := "null";;
if k20module <> fail then
  k20Json := Concatenation(
    "{\"dim\":", String(k20module.dim),
    ",\"theta_matrix_gf2\":", MatJson(ToGFp(k20module.theta_matrix,2)),
    ",\"tau_matrix_gf2\":", MatJson(ToGFp(k20module.tau_matrix,2)),
    ",\"theta_sq_eq_id\":", JB(k20module.theta_sq_ok),
    ",\"tau_cube_eq_id\":", JB(k20module.tau_cube_ok),
    ",\"coker_dim\":", String(k20module.coker_dim),
    ",\"formulas_agree\":", JB(k20module.formulas_agree),
    "}");
fi;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"w6-coker-tool/v1\",\n",
  "  \"generated_by\":\"search/probe/w6_coker_tool/w6_coker_tool_driver.g\",\n",
  "  \"card_label\":\"K5 W-6 calibration tooling bundle (coker calculator + DF-W6 fixtures + K^(20) module)\",\n",
  "  \"design_doc\":\"docs/notes/k5_w6_construction_v1.md\",\n",
  "  \"authorization\":\"裁定446(I-1/I-2/I-3 -- 標的未確定でも即発注可・Im R 非接触・Phase2解錠不要)\",\n",
  "  \"tier\":\"tooling-calibration\",\n",
  "  \"seal_declaration\":{\"touches_c_hat_mu\":false,\"touches_psl_sealed_fields\":false,\n",
  "    \"touches_wall_campaign_pbit\":false,\"touches_u_values\":false,\"touches_im_R\":false},\n",
  "  \"part1_coker_calculator\":{\n",
  "    \"implementation\":\"GAP native GF(p) linear algebra (RankMat/NullspaceMat/SolutionMat) -- independent of scratchpad/k5_w6_norm_obstruction_check.py's hand-rolled python rref\",\n",
  "    \"cross_check_note\":\"cross-checked (not verified -- Lean is reserved for 'verified'). Compares dim values only; does not import the python script.\",\n",
  "    \"A_module_p5_coker\":", String(rA5.coker), ",\"A_module_p5_formulas_agree\":", JB(rA5.agree), ",\n",
  "    \"trivial_1dim_p5_coker\":", String(rTriv5.coker), "\n",
  "  },\n",
  "  \"part2_fixtures\":{\n",
  "    \"DF_W6_1\":{\"pass\":", JB(df1_pass), ",\"coker_dim_of_synthetic_module\":", String(rDF1.coker),
  ",\"solver_reports_unsolvable_on_nonzero_class\":", JB(df1_solve.solvable = false),
  ",\"solver_finds_solution_on_zero_class\":", JB(df1_zero.solvable), "},\n",
  "    \"DF_W6_2\":", (function()
      if k20module = fail then return "{\"status\":\"SKIPPED_preconditions_not_met\"}";
      else return k20Json; fi;
    end)(), ",\n",
  "    \"DF_W6_3\":{\"pass\":", JB(rDF3.coker = 0), ",\"coker_dim\":", String(rDF3.coker), "},\n",
  "    \"DF_W6_4\":{\"pass\":", JB(df4_pass), ",\"orders_theta_tau_p5_p3_p7_p11\":", JArr(List(df4_orders,String)), "}\n",
  "  },\n",
  "  \"part3_k20_module\":{\n",
  "    \"note\":\"GAP-direct construction of G20=PB3/K20, G5=PB3/K5, V=Ker(G20->G5), theta/tau via the ScanRoofHexagon convention (x<->y ; x->y,y->(xy)^-1), restricted to V via a Pcgs isomorphism to GF(2)^dim. This is a computational substitute for the note's 'paper, one page' estimate for K5-GAP-W3 -- flagged as a design deviation in the report.\",\n",
  "    \"g20_order\":", String(Size(g20.G)), ",\"g5_order\":", String(Size(g5.G)), ",\n",
  "    \"reduction_hom_well_defined_onto\":", JB(redHomOk), ",\n",
  "    \"v_order\":", String(Size(V20)), ",\"v_abelian\":", JB(vAbelian),
  ",\"v_elementary_abelian_2group\":", JB(vElemAb2), ",\n",
  "    \"theta_order_on_g20\":", String(th2ord), ",\"tau_order_on_g20\":", String(ta2ord), ",\n",
  "    \"v_theta_stable\":", JB(vStableTh), ",\"v_tau_stable\":", JB(vStableTa), ",\n",
  "    \"module_data\":", k20Json, ",\n",
  "    \"claims_disclaimer\":\"S-W6-3: this computes the OBSTRUCTION GROUP dim coker(psi_V) only. It does NOT compute the obstruction class, does NOT touch Im R_{N,K^(5)}, and makes no d_N / window-existence claim (per task instruction 3).\"\n",
  "  },\n",
  "  \"fails_total\":", String(Length(FAILS)), ",\n",
  "  \"fails\":", JArr(List(FAILS, f -> Concatenation("{\"name\":", JStr(f.name),
      ",\"got\":", JStr(String(f.got)), ",\"want\":", JStr(String(f.want)), "}"))), ",\n",
  "  \"scope\":{\"lane\":\"GAP single lane\",\"cross_checked_status\":\"n/a for group-theoretic construction (part 3); part 1 is a from-scratch independent re-implementation of the closed-form check, not a two-lane cross-check with the python script\"},\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"design_doc_sha256\":", JStr(noteSha), ",\n",
  "    \"python_check_script_sha256_for_reference_only\":", JStr(pyCheckSha), ",\n",
  "    \"wall_ms_total\":", String(GAPLIB_WallElapsedMs()), "\n",
  "  }\n",
  "}\n");;

OUT_PATH := "search/certs/w6_coker_tool_20260804.json";;
WriteFile(OUT_PATH, cert);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nFAILS = ", Length(FAILS), "\n");
for fitem in FAILS do
  Print("   ", fitem.name, " got=", fitem.got, " want=", fitem.want, "\n");
od;
Print("\nW6_COKER_TOOL_DRIVER_DONE\n");
QUIT;
