## search/d972_phase1_v1.g -- TRIAD-972 Phase 1: |Im R_{K,M}| の測定(1ビット)(裁定1133)
##
## 正本: docs/notes/triad972_grade_and_battle_plan_v1_1.md §7 Phase 1(D972-1)。
##   K := K^(27) cap N_S4 への reduction について |Im R_{K,M}| を測る(M = 972 屋根)。
##   事前登録スペクトル: {324, 972} のどちらか。中間値 -> 即停止(fail-closed)。
##
## 設計(全 GT(K) 列挙は不要 -- 司令塔指示の実務路):
##   GT(K) を Elements(DerivedSubgroup(GK)) 経由でフル列挙するのは |GK|~3.97e7 規模で
##   非現実的(RAM 8GB 制約)。代わりに M の 972 shadow それぞれについて「K へ持ち上がるか」
##   を有限検査する(972 回のローカル判定)。
##
##   持ち上がりの必要十分条件(homKtoM: GK -> GM の自然性から機械的に導出・仮定なし):
##     homKtoM(X_K)=X_M, homKtoM(Y_K)=Y_M (構成による)。thetaHom/tauHom は同じ生成元の
##     入れ替えで定義されるため homKtoM と自然に可換 -- ゆえに (m,f) が M の shadow なら、
##     f_K が f の homKtoM 原像であり u_K = 2*m_K+1 が u_M = 2*m+1 と mod Mord(=18) で
##     合同なとき、かつそのときに限り、K 側の hex310/hex311/genA,genB-surjectivity の
##     "M への像" 部分は自動的に一致する(ただし K 側の生の条件自体は個別にチェックする
##     -- 自動的に成り立つのはあくまで "reduction が一致する" 部分のみ)。
##     u_K = u_M (mod 18) <=> m_K = m (mod 9)(2 の mod18可逆性より)。
##   D(GK) = homKtoM^{-1}(D(GM)) が完全に成り立つこと(|D(GK)| = |Ker(homKtoM)|*|D(GM)|
##   を実測で確認)により、f の任意の原像は自動的に D(GK) に入る -- 追加のメンバーシップ
##   検査は不要(本 script 内で実測して確認する・仮定として使わない)。
##
## 陽性対照:
##   (i) 恒等 shadow(m=0, f=Identity(GM))は必ず持ち上がる。
##   (ii) 方法論の scaled-down 全数検証: K^(9) の 108 shadow それぞれについて、
##        同じ候補限定型 lift 判定を K^(27) 側に対して実行し、その結果集合を
##        「K27 の 972 shadow 全数列挙 -> hom27to9 で reduce -> K9 の 108 shadow との
##        一致を数える」という独立なフル列挙による ground truth と突合する。
##        (K27,K9 は規模が小さく両方式が実行可能 -- K,M では左式のみ実行可能なため、
##        この突合が「候補限定ショートカットはフル列挙と同じ答えを返す」ことの
##        機械的な検算になる。)
##
## 規律: u/c 非接触・封印3量非接触・prereg 量非計算・生値のみ・判定語なし・UNKNOWN 一級。

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");
Read("search/week3-psl-common.g");

t0Global := GAPLIB_WallElapsedMs();;
PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

## ================= shared helpers (verbatim from d972_phase0_v1.g) =================
ScanRoofHexagon := function(qrec, charmingSet)
  local G, D, Delts, thetaHom, tauHom, zElt, h10Fail, h11Fail, genFail, shadows,
        m, u, f, thetaf, hex310, ymf, tauymf, tau2ymf, hex311, genA, genB, surj,
        candidateTotal, i;
  G := qrec.G;
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  if thetaHom = fail or tauHom = fail then
    Error("ScanRoofHexagon: theta/tau homomorphism construction failed");
  fi;
  D := DerivedSubgroup(G);
  Delts := Elements(D);
  h10Fail := 0;  h11Fail := 0;  genFail := 0;  shadows := [];
  candidateTotal := Length(Delts) * Length(charmingSet);
  for m in charmingSet do
    u := 2*m + 1;
    for i in [1 .. Length(Delts)] do
      f := Delts[i];
      thetaf := Image(thetaHom, f);
      hex310 := AbstractProd([f, thetaf]) = Identity(G);
      if not hex310 then h10Fail := h10Fail + 1; continue; fi;
      ymf := AbstractProd([qrec.y^m, f]);
      tauymf := Image(tauHom, ymf);
      tau2ymf := Image(tauHom, tauymf);
      hex311 := AbstractProd([tau2ymf, tauymf, ymf]) = Identity(G);
      if not hex311 then h11Fail := h11Fail + 1; continue; fi;
      genA := qrec.x^u;
      genB := AbstractProd([f^-1, qrec.y^u, f]);
      surj := Size(Group(genA, genB)) = Size(G);
      if not surj then
        genFail := genFail + 1;
      else
        Add(shadows, rec(m := m, f := f));
      fi;
    od;
  od;
  return rec(candidate_total := candidateTotal, h10_fail := h10Fail, h11_fail := h11Fail,
             generation_fail := genFail, shadow_total := Length(shadows), shadows := shadows,
             derived_order := Length(Delts));
end;;

CharmingSetOf := function(nOrd)
  return Filtered([0 .. nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);
end;;

ShiftPerm := function(p, offset, size)
  local l, j;
  l := [1 .. offset+size];
  for j in [1 .. size] do l[offset+j] := offset + (j^p); od;
  return PermList(l);
end;;
DirectSumPerm := function(p1, deg1, p2, deg2)
  return p1 * ShiftPerm(p2, deg1, deg2);
end;;

## generic per-candidate hex checker (extracted from ScanRoofHexagon's inner loop,
## same math, applied to a single (m,f) candidate instead of scanning D(G)).
CheckHexCandidate := function(qrec, thetaHom, tauHom, m, f)
  local thetaf, hex310, ymf, tauymf, tau2ymf, hex311, u, genA, genB, surj;
  thetaf := Image(thetaHom, f);
  hex310 := AbstractProd([f, thetaf]) = Identity(qrec.G);
  if not hex310 then return rec(pass := false, stage := "hex310"); fi;
  ymf := AbstractProd([qrec.y^m, f]);
  tauymf := Image(tauHom, ymf);
  tau2ymf := Image(tauHom, tauymf);
  hex311 := AbstractProd([tau2ymf, tauymf, ymf]) = Identity(qrec.G);
  if not hex311 then return rec(pass := false, stage := "hex311"); fi;
  u := 2*m + 1;
  genA := qrec.x^u;
  genB := AbstractProd([f^-1, qrec.y^u, f]);
  surj := Size(Group(genA, genB)) = Size(qrec.G);
  if not surj then return rec(pass := false, stage := "surj"); fi;
  return rec(pass := true, stage := "ok");
end;;

## generic lift-check: for a shadow (m,f) of GT(coarse), search candidates (m_fine,f_fine)
## of GT(fine) that reduce to it under homFineToCoarse, with:
##   f_fine ranging over f0*k for k in Kernel(homFineToCoarse)  (f0 = one preimage of f)
##   m_fine ranging over [0..fineOrd-1] with m_fine = m (mod coarseOrd/ something) filter
## returns rec(found, checked, witness, pass_count)
LiftCheck := function(fineQrec, thetaHomFine, tauHomFine, homFineToCoarse, kerElts,
                      coarseOrd, fineOrd, m, f, earlyExit)
  local f0, mFineCands, checked, passCount, mF, k, fF, res, witness, found, modBase;
  f0 := PreImagesRepresentative(homFineToCoarse, f);
  modBase := coarseOrd / 2;  ## u = 2m+1 (mod coarseOrd) <=> m (mod coarseOrd/2), coarseOrd even
  mFineCands := Filtered([0 .. fineOrd-1],
                    mm -> (mm mod modBase = m mod modBase) and Gcd(2*mm+1, fineOrd) = 1);
  checked := 0;  passCount := 0;  witness := fail;  found := false;
  for mF in mFineCands do
    for k in kerElts do
      fF := f0 * k;
      checked := checked + 1;
      res := CheckHexCandidate(fineQrec, thetaHomFine, tauHomFine, mF, fF);
      if res.pass then
        passCount := passCount + 1;
        if witness = fail then witness := rec(m := mF, f := fF); fi;
        found := true;
        if earlyExit then return rec(found := true, checked := checked, witness := witness,
                                       pass_count := passCount, m_fine_candidates := Length(mFineCands)); fi;
      fi;
    od;
  od;
  return rec(found := found, checked := checked, witness := witness, pass_count := passCount,
             m_fine_candidates := Length(mFineCands));
end;;

Print("############################################################\n");
Print("# d972_phase1_v1.g -- TRIAD-972 Phase 1: |Im R_{K,M}| 測定(裁定1133)\n");
Print("############################################################\n");

## ================= [1-1] windows: K9, K27, N_S4, M, K =================
Print("\n=== [1-1] 窓構成: K9, K27, N_S4, M := K9 cap N_S4, K := K27 cap N_S4 ===\n");
g9 := MakeGn(9);;
g27 := MakeGn(27);;
CheckGF8();;
Smat := MakeMatGF8(1,0,1,1);;
Tmat := MakeMatGF8(4,3,1,5);;
Sperm := MatToPermGF8(Smat);;
Tperm := MatToPermGF8(Tmat);;
wPerm := Sperm * Tperm^-1;;
Xperm := wPerm^2;;
Yperm := Sperm^-1 * Xperm * Sperm;;
Pgrp := Group(Xperm, Yperm);;
Print("  |PB3/K9|=", Size(g9.G), " |PB3/K27|=", Size(g27.G), " |PB3/N_S4|=", Size(Pgrp), "\n");
if Size(g9.G) <> 2916 or Size(g27.G) <> 78732 or Size(Pgrp) <> 504 then
  Error("d972_phase1: base window scale mismatch -- refusing to proceed");
fi;

XM := DirectSumPerm(g9.x, 27, Xperm, 9);;
YM := DirectSumPerm(g9.y, 27, Yperm, 9);;
GM := Group(XM, YM);;
Mord := Lcm(Order(XM), Order(YM));;
PB3overM := Size(GM);;
Print("  |PB3/M| = ", PB3overM, " (expect 1469664)  M_ord = ", Mord, " (expect 18)\n");
if PB3overM <> 1469664 or Mord <> 18 then
  Error("d972_phase1: M window mismatch (should match d972_phase0_v1.g) -- refusing to proceed");
fi;

XK := DirectSumPerm(g27.x, 81, Xperm, 9);;
YK := DirectSumPerm(g27.y, 81, Yperm, 9);;
GK := Group(XK, YK);;
Kord := Lcm(Order(XK), Order(YK));;
PB3overK_measured := Size(GK);;
Print("  |PB3/K| = ", PB3overK_measured, " (measured, actual construction; NOT the arithmetic-product\n");
Print("  estimate 39,696,528 recorded in d972_phase0_v1.g [0-4] as an UNCONSTRUCTED upper bound)\n");
Print("  K_ord = ", Kord, " (expect 54)\n");
if Kord <> 54 then
  Error("d972_phase1: K_ord mismatch -- refusing to proceed");
fi;

## ================= [1-1] homKtoM: GK -> GM (2 epi の合成の核として K を特徴づける自然な写像) ==
Print("\n=== [1-1] homKtoM: GK -> GM (natural quotient, K subseteq M via K27 subseteq K9) ===\n");
homKtoM := GroupHomomorphismByImages(GK, GM, [XK,YK], [XM,YM]);;
homKtoMWellDefined := (homKtoM <> fail);;
if not homKtoMWellDefined then
  Error("d972_phase1: homKtoM construction failed -- K subseteq M expected from Prop 3.5 (K27 subseteq K9)");
fi;
homKtoMSurjective := (Size(Image(homKtoM)) = PB3overM);;
Print("  well_defined=", homKtoMWellDefined, "  surjective(|Image|=|M|)=", homKtoMSurjective, "\n");
if not homKtoMSurjective then
  Error("d972_phase1: homKtoM not surjective -- unexpected, refusing to proceed");
fi;
KerHom := Kernel(homKtoM);;
KerElts := Elements(KerHom);;
kerSize := Size(KerHom);;
kerSizeExpected := PB3overK_measured / PB3overM;;
Print("  |Ker(homKtoM)| = ", kerSize, " (arithmetic |K|/|M| = ", kerSizeExpected, ")\n");

## structural fact check (not assumed -- measured): D(GK) = homKtoM^{-1}(D(GM))
Print("\n=== structural check: D(GK) = homKtoM^{-1}(D(GM)) (measured, not assumed) ===\n");
DGK := DerivedSubgroup(GK);;
DGM := DerivedSubgroup(GM);;
dgkSize := Size(DGK);;  dgmSize := Size(DGM);;
kerCapDGK := Intersection(KerHom, DGK);;
kerCapDGKSize := Size(kerCapDGK);;
kerFullyInDGK := (kerCapDGKSize = kerSize);;
dgkEqPreimage := (dgkSize = kerSize * dgmSize);;
Print("  |D(GK)|=", dgkSize, " |D(GM)|=", dgmSize, " |Ker cap D(GK)|=", kerCapDGKSize, "/", kerSize,
      "  (kernel fully inside D(GK)): ", kerFullyInDGK, "\n");
Print("  |D(GK)| = |Ker|*|D(GM)| ?  ", dgkSize, " = ", kerSize*dgmSize, "  : ", dgkEqPreimage, "\n");
Print("  [", PF(kerFullyInDGK and dgkEqPreimage), "] D(GK) = full preimage of D(GM) under homKtoM\n");
## consequence used below (measured fact, not assumed): every GAP-arbitrary preimage of any
## f in D(GM) under PreImagesRepresentative(homKtoM,f) already lies in D(GK) when the above holds.

## ================= [1-2] K isolated (#C(K)=1): method attempted, same wall as Phase0 [0-2] ====
Print("\n=== [1-2] (H1 for K) #C(K)=1 -- method selection and outcome ===\n");
Print("  marked-factor-map(AutomorphismGroup(PN)) for PN=GK, |GK|=", PB3overK_measured,
      " is larger than |GM|=", PB3overM, " which was already refused in d972_phase0_v1.g [0-2]\n");
Print("  (RAM 8GB constraint, 裁定1117 precedent). Not attempted here for the same reason,\n");
Print("  a fortiori (larger group). well-definedness alternative requires full-B3 generators\n");
Print("  sigma1,sigma2 for the K27 window; not available in reusable codebase assets\n");
Print("  (same blocker as Phase0 [0-2] for K9). [1-2] recorded as UNKNOWN, generic values only.\n");
h1KStatus := "UNKNOWN";;
h1KMethod := "not_attempted_same_blocker_as_phase0_0_2";;

## ================= [1-3]/[1-4]: recompute M's 972 shadows, then per-shadow lift-check into K ===
Print("\n=== [1-3] M window's 972 shadows: independent re-execution (ScanRoofHexagon) ===\n");
tM0 := GAPLIB_WallElapsedMs();;
Mcharm := CharmingSetOf(Mord);;
resM := ScanRoofHexagon(rec(x:=XM, y:=YM, G:=GM), Mcharm);;
tM1 := GAPLIB_WallElapsedMs();;
shadowTotalMOk := (resM.shadow_total = 972);;
Print("  shadow_total=", resM.shadow_total, " (expect 972)  [", PF(shadowTotalMOk), "]  elapsed_ms=", tM1-tM0, "\n");
if not shadowTotalMOk then
  Error("d972_phase1: M shadow_total <> 972 -- refusing to proceed with lift-check on unexpected base");
fi;

Print("\n=== [1-4] per-shadow lift-check: does each of the 972 M-shadows lift to K? ===\n");
zEltK := AbstractProd([XK, YK])^-1;;
thetaHomK := GroupHomomorphismByImages(GK, GK, [XK, YK], [YK, XK]);;
tauHomK := GroupHomomorphismByImages(GK, GK, [XK, YK], [YK, zEltK]);;
if thetaHomK = fail or tauHomK = fail then
  Error("d972_phase1: theta/tau hom construction on K failed");
fi;
Kqrec := rec(x := XK, y := YK, G := GK);;

tL0 := GAPLIB_WallElapsedMs();;
liftResults := [];;
liftedCount := 0;;
idxShadow := 0;;
for sh in resM.shadows do
  idxShadow := idxShadow + 1;;
  lr := LiftCheck(Kqrec, thetaHomK, tauHomK, homKtoM, KerElts, Mord, Kord, sh.m, sh.f, true);;
  if lr.found then liftedCount := liftedCount + 1; fi;
  Add(liftResults, rec(idx := idxShadow, m := sh.m, found := lr.found, checked := lr.checked,
                        m_fine_candidates := lr.m_fine_candidates));
  if idxShadow mod 200 = 0 then
    Print("  progress: ", idxShadow, "/972  lifted_so_far=", liftedCount,
          "  elapsed_ms=", GAPLIB_WallElapsedMs()-tL0, "\n");
  fi;
od;
tL1 := GAPLIB_WallElapsedMs();;
Print("  DONE: checked all 972 M-shadows for K-lift.  lifted_count = ", liftedCount,
      "  elapsed_ms=", tL1-tL0, "\n");

imRSize := liftedCount;;
Print("\n=== [1-5] fail-closed check: |Im R_{K,M}| in {324,972}? ===\n");
inSpectrum := (imRSize = 324) or (imRSize = 972);;
atLeast324 := (imRSize >= 324);;
Print("  |Im R_{K,M}| = ", imRSize, "  in {324,972}: ", inSpectrum, "  >=324: ", atLeast324, "\n");
if not inSpectrum then
  Print("[FAIL-CLOSED SIGNAL] |Im R_{K,M}| is NOT in the pre-registered spectrum {324,972}.\n");
  Print("  Per triad972_grade_and_battle_plan_v1_1.md Sec5.2/Sec7.1: intermediate value =>\n");
  Print("  immediate halt signal ((H1)/(H2) breakage). This script records the raw value and\n");
  Print("  continues to write the cert (no verdict language) -- halting further Phase escalation\n");
  Print("  is a commander/mathematician decision, not made here.\n");
fi;

## ================= positive control (i): identity shadow must lift =================
Print("\n=== positive control (i): identity shadow (m=0, f=Id(GM)) must lift ===\n");
idShadow := First(resM.shadows, sh -> sh.m = 0 and sh.f = Identity(GM));;
idControlFound := false;;  idControlPresent := (idShadow <> fail);;
if idControlPresent then
  lrId := LiftCheck(Kqrec, thetaHomK, tauHomK, homKtoM, KerElts, Mord, Kord, idShadow.m, idShadow.f, true);;
  idControlFound := lrId.found;;
fi;
Print("  identity shadow present in M's 972: ", idControlPresent, "  lifts to K: ", idControlFound, "\n");
if idControlPresent and not idControlFound then
  Print("[CONTROL FAILURE WARNING] identity shadow did not lift -- lift-checker likely has a bug.\n");
fi;

## ================= positive control (ii): scaled-down full-comparison K9/K27 =================
Print("\n=== positive control (ii): K9/K27 scaled-down methodology cross-check ===\n");
tV0 := GAPLIB_WallElapsedMs();;
hom27to9 := GroupHomomorphismByImages(g27.G, g9.G, [g27.x, g27.y], [g9.x, g9.y]);;
hom27to9WellDefined := (hom27to9 <> fail);;
hom27to9Surjective := false;;
if hom27to9WellDefined then
  hom27to9Surjective := (Size(Image(hom27to9)) = Size(g9.G));;
fi;
Print("  hom27to9 well_defined=", hom27to9WellDefined, " surjective=", hom27to9Surjective, "\n");

K9ord := Lcm(Order(g9.x), Order(g9.y));;
K27ord := Lcm(Order(g27.x), Order(g27.y));;
K9charm := CharmingSetOf(K9ord);;
K27charm := CharmingSetOf(K27ord);;
resK9 := ScanRoofHexagon(rec(x:=g9.x, y:=g9.y, G:=g9.G), K9charm);;
resK27 := ScanRoofHexagon(rec(x:=g27.x, y:=g27.y, G:=g27.G), K27charm);;
Print("  |GT(K9)| shadow_total=", resK9.shadow_total, " (expect 108)  |GT(K27)| shadow_total=",
      resK27.shadow_total, " (expect 972)\n");

## ground truth: reduce all 972 K27-shadows via hom27to9, count which of K9's 108 shadows are hit
K9ShadowSet := Set(List(resK9.shadows, sh -> [sh.m, sh.f]));;
groundTruthHit := Set([]);;
for sh27 in resK27.shadows do
  mReduced := sh27.m mod K9ord;;
  fReduced := Image(hom27to9, sh27.f);;
  cand := [mReduced, fReduced];;
  if cand in K9ShadowSet then
    AddSet(groundTruthHit, cand);;
  fi;
od;
groundTruthCount := Length(groundTruthHit);;
Print("  ground truth (full enumeration): |{K9 shadows hit by some K27-shadow reduction}| = ",
      groundTruthCount, " / ", resK9.shadow_total, "\n");

## candidate-based lift-checker applied to the SAME K9/K27 pair (methodology under test)
KerHom27to9 := Kernel(hom27to9);;
KerElts27to9 := Elements(KerHom27to9);;
zElt27 := AbstractProd([g27.x, g27.y])^-1;;
thetaHom27 := GroupHomomorphismByImages(g27.G, g27.G, [g27.x, g27.y], [g27.y, g27.x]);;
tauHom27 := GroupHomomorphismByImages(g27.G, g27.G, [g27.x, g27.y], [g27.y, zElt27]);;
qrec27 := rec(x := g27.x, y := g27.y, G := g27.G);;
checkerHitCount := 0;;
checkerMismatches := [];;
for sh9 in resK9.shadows do
  lr9 := LiftCheck(qrec27, thetaHom27, tauHom27, hom27to9, KerElts27to9, K9ord, K27ord, sh9.m, sh9.f, true);;
  groundTruthSays := ([sh9.m, sh9.f] in groundTruthHit);;
  if lr9.found then checkerHitCount := checkerHitCount + 1; fi;
  if lr9.found <> groundTruthSays then
    Add(checkerMismatches, rec(m := sh9.m, checker_found := lr9.found, ground_truth := groundTruthSays));
  fi;
od;
tV1 := GAPLIB_WallElapsedMs();;
methodologyMatch := (Length(checkerMismatches) = 0);;
Print("  candidate-based checker: |{K9 shadows found liftable}| = ", checkerHitCount, "/", resK9.shadow_total, "\n");
Print("  mismatches vs ground truth: ", Length(checkerMismatches), "  [", PF(methodologyMatch), "]  elapsed_ms=", tV1-tV0, "\n");
if not methodologyMatch then
  Print("[METHODOLOGY WARNING] candidate-based lift-checker disagrees with full enumeration on K9/K27\n");
  Print("  scaled-down cross-check -- the K/M Phase1 measurement above should NOT be trusted as-is.\n");
fi;

t1Global := GAPLIB_WallElapsedMs();;
Print("\n総経過 = ", t1Global - t0Global, " ms\n");

## ================= JSON =================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_d972p1.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/d972_phase1_v1.g");;

JLiftDetailRec := function(r)
  return Concatenation("{\"idx\":", String(r.idx), ",\"m\":", String(r.m), ",\"found\":", JB(r.found),
    ",\"checked\":", String(r.checked), ",\"m_fine_candidates\":", String(r.m_fine_candidates), "}");
end;;
JMismatchRec := function(r)
  return Concatenation("{\"m\":", String(r.m), ",\"checker_found\":", JB(r.checker_found),
    ",\"ground_truth\":", JB(r.ground_truth), "}");
end;;

cert := Concatenation(
  "{\"schema\":\"d972_bit/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/d972_phase1_v1.g\",\"order\":\"裁定1133(TRIAD-972 Phase1・単一ビット測定)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/triad972_grade_and_battle_plan_v1_1.md §7 Phase1(D972-1)\"",
  ",\"windows\":{\"pb3_over_k9\":", String(Size(g9.G)), ",\"pb3_over_k27\":", String(Size(g27.G)),
    ",\"pb3_over_n_s4\":", String(Size(Pgrp)),
    ",\"pb3_over_m\":", String(PB3overM), ",\"m_ord\":", String(Mord),
    ",\"pb3_over_k_measured\":", String(PB3overK_measured), ",\"k_ord\":", String(Kord),
    ",\"pb3_over_k_phase0_arith_estimate\":39696528",
    ",\"pb3_over_k_estimate_vs_measured_note\":\"phase0 [0-4] recorded 39696528 as an UNCONSTRUCTED arithmetic-product upper bound (78732*504); the actual subdirect-product construction here measures ", String(PB3overK_measured), " (< estimate, as expected per pb3_free_factor_check_v1.md §5: subdirect products are usually strictly smaller than the naive product unless independently shown to be the full direct product, as M's case happened to be).\"},",
  "\"hom_k_to_m\":{\"well_defined\":", JB(homKtoMWellDefined), ",\"surjective\":", JB(homKtoMSurjective),
    ",\"kernel_size\":", String(kerSize), ",\"kernel_size_arith_check\":", String(kerSizeExpected), "},",
  "\"derived_subgroup_structural_check\":{",
    "\"dgk_size\":", String(dgkSize), ",\"dgm_size\":", String(dgmSize),
    ",\"ker_cap_dgk_size\":", String(kerCapDGKSize), ",\"ker_size\":", String(kerSize),
    ",\"kernel_fully_inside_dgk\":", JB(kerFullyInDGK),
    ",\"dgk_eq_kernel_times_dgm\":", JB(dgkEqPreimage),
    ",\"dgk_equals_full_preimage_of_dgm\":", JB(kerFullyInDGK and dgkEqPreimage),
  "},",
  "\"h1_k_isolated\":{\"status\":\"", h1KStatus, "\",\"method\":\"", h1KMethod, "\",\"value\":null,",
    "\"blocker_note\":\"marked-factor-map requires AutomorphismGroup(PN) with |PN|=", String(PB3overK_measured),
    " strictly larger than the already-refused |PN|=", String(PB3overM), " case in d972_phase0_v1.g [0-2]; well-definedness alternative needs full-B3 generators for the K27 window, not present in reusable assets (same blocker).\"},",
  "\"m_shadows_recheck\":{\"shadow_total\":", String(resM.shadow_total), ",\"shadow_total_expected\":972,",
    "\"shadow_total_pass\":", JB(shadowTotalMOk), ",\"derived_order\":", String(resM.derived_order), "},",
  "\"phase1_bit\":{",
    "\"lifted_count\":", String(liftedCount), ",\"total_m_shadows\":972,",
    "\"im_r_km_size\":", String(imRSize), ",",
    "\"in_prereg_spectrum_324_972\":", JB(inSpectrum), ",",
    "\"at_least_324\":", JB(atLeast324), ",",
    "\"elapsed_ms\":", String(tL1-tL0), ",",
    "\"per_shadow_detail\":[", JoinC(List(liftResults, JLiftDetailRec), ","), "]",
  "},",
  "\"positive_control_identity\":{\"present_in_m_972\":", JB(idControlPresent),
    ",\"lifts_to_k\":", JB(idControlFound), "},",
  "\"positive_control_k9_k27_methodology_crosscheck\":{",
    "\"hom27to9_well_defined\":", JB(hom27to9WellDefined), ",\"hom27to9_surjective\":", JB(hom27to9Surjective), ",",
    "\"gt_k9_shadow_total\":", String(resK9.shadow_total), ",\"gt_k27_shadow_total\":", String(resK27.shadow_total), ",",
    "\"ground_truth_hit_count\":", String(groundTruthCount), ",",
    "\"candidate_checker_hit_count\":", String(checkerHitCount), ",",
    "\"mismatch_count\":", String(Length(checkerMismatches)), ",",
    "\"methodology_match\":", JB(methodologyMatch), ",",
    "\"mismatches\":[", JoinC(List(checkerMismatches, JMismatchRec), ","), "],",
    "\"elapsed_ms\":", String(tV1-tV0),
  "},",
  "\"u_touched\":false,\"c_touched\":false,\"prereg_quantities_untouched\":true",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔/数学者。UNKNOWN は一級の結果。\"",
  ",\"total_elapsed_ms\":", String(t1Global - t0Global),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/d972_phase1_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
Print("D972_PHASE1_DONE\n");
QUIT;
