#############################################################################
## twin-witness-mirror-v1_1.g -- 双子 witness 走 v1.1 修理束(裁定607)
##
## v1(search/twin-witness-mirror-v1.g)は不改変(並置)。本ファイルは falsifier
## の CV-9 判読(docs/notes/twin_witness_cv9_reading_v1.md)が指摘した穴のうち
## 系統A(GAP)側で修理すべきもの:
##   【作業1】W-a full hexagon (3.3)(3.4) を B3/N 上、[-1,1] で評価(両方向)
##   【作業2】S-TW-6 カナリアを識別型に差し替え(tau を実際に GroupHomomorphism
##            として実装し、正しい語順(paper積)では恒等・逆順では非自明、と
##            いう対照を Q 上で実測する。旧カナリア x^-1(xy)y^-1=e は撤回)
##   【作業3(その1)】in_PB3 / c_in_N を「census からのコピー」ではなく、この
##            スクリプト自身で独立に(再)計算する(D-3 discipline)。
##   MC-1 v1.1 export: 凍結 schema §2.7 の全フィールドを埋める。全 15 対・両
##            方向のデータを出す(v1 は M1 side のみだった -- 穴8 の修理)。
##
## 登録集合: L2(15対・c_in_N・in_PB3、票 twin_witness_prereg_iffirst_v1.md
## sec1, SETDIGEST 済み検証)。データソースは v1 と共通の生成ファイル
## search/twin_witness_l2_data_v1_generated.g(不変・再利用)。
## L3(13対、裁定T-1)非接触。封印・705,894非接触。
#############################################################################

Read("search/gaplib_common.g");
Read("search/probe/wac_v1/gap_output_prelude.g");

#############################################################################
## ---------------------- shared B3 / PB3 / S3can setup ----------------------
#############################################################################
BF3 := FreeGroup("a", "b");;
ga := BF3.1;;  gb := BF3.2;;
brel := ga * gb * ga * (gb * ga * gb)^-1;;
B3 := BF3 / [brel];;
ga := B3.1;;  gb := B3.2;;

S3can := SymmetricGroup(3);;
phiCan := GroupHomomorphismByImages(B3, S3can, [ga, gb], [(1,2), (2,3)]);;
if phiCan = fail then Error("canonical B3 -> S3 map failed sanity check"); fi;
PB3 := Kernel(phiCan);;

DeltaElt := ga*gb*ga;;
c_elt := DeltaElt^2;;

## global 'a','b' bindings used by EvalString below -- default = identity map
a := ga;;  b := gb;;

## ---------------------- abstract F2 = <x,y> for tau/theta -------------------
## x = a^2 image, y = b^2 image -- tau, theta act on the ABSTRACT free group
## F2 (universal, N-independent); mapped into each window's Q via a genuine
## substitution homomorphism (x |-> qx, y |-> qy), not by hand-reduced
## identities. This is the actual "run the tau mechanism" fix (穴1/作業2).
F2abs := FreeGroup("x", "y");;
xg := F2abs.1;;  yg := F2abs.2;;
## tau: x -> y, y -> (x*y)^-1  (z := (xy)^-1, tau: x->y->z->x cyclically)
tauHom := GroupHomomorphismByImages(F2abs, F2abs, [xg,yg], [yg, (xg*yg)^-1]);;
if tauHom = fail then Error("tau homomorphism construction failed"); fi;
## theta: x <-> y (swap)
thetaHom := GroupHomomorphismByImages(F2abs, F2abs, [xg,yg], [yg, xg]);;
if thetaHom = fail then Error("theta homomorphism construction failed"); fi;

## sanity: tau^3 = id on F2abs generators (checked once, universally)
tau2_x := ImageElm(tauHom, ImageElm(tauHom, xg));;
tau3_x := ImageElm(tauHom, tau2_x);;
tau2_y := ImageElm(tauHom, ImageElm(tauHom, yg));;
tau3_y := ImageElm(tauHom, tau2_y);;
tauCubeIsId := (tau3_x = xg) and (tau3_y = yg);;
Print("tau^3 = id on F2abs generators (universal sanity): ", tauCubeIsId, "\n");
if not tauCubeIsId then Error("tau^3 <> id -- tau implementation is wrong, STOP"); fi;

#############################################################################
## ---------------------- load L2 registered set (generated data file) ------
#############################################################################
Read("search/twin_witness_l2_data_v1_generated.g");   # defines L2Pairs (unchanged from v1)
Print("Loaded L2Pairs: ", Length(L2Pairs), " pairs (expect 15)\n");
if Length(L2Pairs) <> 15 then
  Error("L2Pairs count mismatch -- STOP (scope 1 data file corrupt or stale)");
fi;

#############################################################################
## ---------------------- word evaluation helper -----------------------------
#############################################################################
EvalWordB3 := function(wordStr) return EvalString(wordStr); end;;
EvalWordListB3 := function(wordStrList) return List(wordStrList, EvalWordB3); end;;

#############################################################################
## ---------------------- per-window processing (one side: N, K) -------------
#############################################################################
## Processes ONE directed window: quotient Q_N := B3/N built from Nwords,
## with the partner K's words also available for kernel-identification.
## Returns a record with everything MC-1 v1.1 needs for this ONE direction.
ProcessWindow := function(idx, pair_uid, N_uid, K_uid, Nwords, Kwords)
  local Ngens, Nsub, hmN, QN, sizeN, wc_class,
        a_save, b_save, iotaNwordsInN, iotaKwordsInN,
        imgIotaN_inN, imgIotaK_inN, selfTrivial, partnerTrivial,
        mclass, witnessWord, i,
        qa, qb, cImg, cInN_indep,
        s3hom, inPB3_indep,
        lhs33, rhs33, ok33, lhs34, rhs34, ok34, hexagonFull,
        hom2Q, tauWord_y1, tauWord_y1_1, tauWord_y1_2,
        P1elt, P2elt, P3elt, canaryFwd, canaryRev, canaryDiscrim,
        surjOK, genImgsInv, surjSub, rho;

  Ngens := EvalWordListB3(Nwords);;
  Nsub := Subgroup(B3, Ngens);;
  hmN := NaturalHomomorphismByNormalSubgroup(B3, Nsub);;
  QN := Image(hmN);;
  sizeN := Size(QN);;

  qa := ImageElm(hmN, ga);;  qb := ImageElm(hmN, gb);;

  ## --- iota(N) vs N, iota(N) vs K (mirror classification, v1 method) ---
  a := ga^-1;;  b := gb^-1;;
  iotaNwordsInN := EvalWordListB3(Nwords);;
  iotaKwordsInN := EvalWordListB3(Kwords);;
  a := ga;;  b := gb;;

  imgIotaN_inN := List(iotaNwordsInN, w -> ImageElm(hmN, w));;
  imgIotaK_inN := List(iotaKwordsInN, w -> ImageElm(hmN, w));;

  selfTrivial := ForAll(imgIotaN_inN, w -> w = One(QN));;
  partnerTrivial := ForAll(imgIotaK_inN, w -> w = One(QN));;

  witnessWord := fail;;
  for i in [1..Length(Nwords)] do
    if imgIotaN_inN[i] <> One(QN) then witnessWord := Nwords[i]; break; fi;
  od;;

  if selfTrivial then
    mclass := "M0";;
  elif partnerTrivial then
    mclass := "M1";;
  else
    mclass := "M2";;
  fi;

  ## --- 【作業3-その1】 c_in_N: independently recomputed (not copied from cert) ---
  cImg := ImageElm(hmN, c_elt);;
  cInN_indep := (cImg = One(QN));;

  ## --- in_PB3: independently recomputed via homomorphism-factors-through test ---
  ## (GroupHomomorphismByImages returns fail iff the assignment qa->(1,2),
  ## qb->(2,3) is NOT consistent with the relations already holding in QN,
  ## i.e. iff ker(B3->QN) is NOT contained in ker(B3->S3can) = PB3.)
  s3hom := GroupHomomorphismByImages(QN, S3can, [qa,qb], [(1,2),(2,3)]);;
  inPB3_indep := (s3hom <> fail);;

  ## --- 【作業1】 full hexagon (3.3)(3.4) on Q_N at [-1,1] -----------------
  ## (3.3): sigma1^-1*sigma2^-1 =? sigma1*sigma2*x*c^-1   (x=sigma1^2)
  lhs33 := qa^-1 * qb^-1;;
  rhs33 := qa*qb*qa^2*(ImageElm(hmN,c_elt))^-1;;
  ok33 := (lhs33 = rhs33);;
  ## (3.4): sigma2^-1*sigma1^-1 =? sigma2*sigma1*y*c^-1   (y=sigma2^2)
  lhs34 := qb^-1 * qa^-1;;
  rhs34 := qb*qa*qb^2*(ImageElm(hmN,c_elt))^-1;;
  ok34 := (lhs34 = rhs34);;
  hexagonFull := ok33 and ok34;;

  ## --- 【作業2】 discriminating canary via ACTUAL tau homomorphism --------
  ## Build hom2Q: F2abs -> QN sending x|->qx=qa^2, y|->qy=qb^2 (genuine
  ## substitution homomorphism, not hand-reduced identity).
  hom2Q := GroupHomomorphismByImages(F2abs, QN, [xg,yg], [qa^2, qb^2]);;
  if hom2Q = fail then Error("F2abs -> QN substitution hom failed to build"); fi;

  ## P3 := y^-1 (in F2abs);  P2 := tau(y^-1);  P1 := tau(tau(y^-1)) = tau^2(y^-1)
  ## -- all computed by RUNNING tauHom, not by hand-simplification.
  tauWord_y1 := yg^-1;;                                  # P3, abstractly
  tauWord_y1_1 := ImageElm(tauHom, tauWord_y1);;          # tau(y^-1) = P2
  tauWord_y1_2 := ImageElm(tauHom, tauWord_y1_1);;        # tau^2(y^-1) = P1

  P1elt := ImageElm(hom2Q, tauWord_y1_2);;   # tau^2(y^-1) mapped into QN
  P2elt := ImageElm(hom2Q, tauWord_y1_1);;   # tau(y^-1)   mapped into QN
  P3elt := ImageElm(hom2Q, tauWord_y1);;     # y^-1        mapped into QN

  ## forward (paper-product order, W-4 correct convention): P1*P2*P3 =? 1
  canaryFwd := (P1elt * P2elt * P3elt = One(QN));;
  ## reversed (wrong convention, syntactic reversal of the SAME 3 elements):
  canaryRev := (P3elt * P2elt * P1elt = One(QN));;
  ## discriminating iff forward holds AND reversed does NOT (i.e. the two
  ## conventions are actually told apart in this window -- if qx,qy commute
  ## in QN the contrast degenerates, which we detect and report honestly).
  canaryDiscrim := canaryFwd and (not canaryRev);;

  ## --- W-c SURJ: <a^-1,b^-1> = Q_N -----------------------------------------
  genImgsInv := [qa^-1, qb^-1];;
  surjSub := Subgroup(QN, genImgsInv);;
  surjOK := (Size(surjSub) = sizeN);;

  return rec(
    index := idx, pair_uid := pair_uid, N_uid := N_uid, K_uid := K_uid,
    Nwords := Nwords, Kwords := Kwords,
    sizeN := sizeN, mclass := mclass,
    selfTrivial := selfTrivial, partnerTrivial := partnerTrivial,
    witnessWord := witnessWord,
    cInN_indep := cInN_indep, inPB3_indep := inPB3_indep,
    hexagon33 := ok33, hexagon34 := ok34, hexagonFull := hexagonFull,
    canaryFwd := canaryFwd, canaryRev := canaryRev, canaryDiscrim := canaryDiscrim,
    surjOK := surjOK,
    QN := QN, hmN := hmN, Nsub := Nsub, qa := qa, qb := qb
  );;
end;;

#############################################################################
## ---------------------- main loop: BOTH directions, all 15 pairs -----------
#############################################################################
AllResults := [];;   # one entry per direction (30 total: A-side, B-side per pair)
t0 := GAPLIB_WallElapsedMs();

for pr in L2Pairs do
  idx := pr.index;;
  Print("\n=== pair index=", idx, " pair_uid=", pr.pair_uid, " ===\n");

  resA := ProcessWindow(idx, pr.pair_uid, pr.A_uid, pr.B_uid, pr.A, pr.B);;
  resB := ProcessWindow(idx, pr.pair_uid, pr.B_uid, pr.A_uid, pr.B, pr.A);;

  Print("  A-side: |Q|=", resA.sizeN, " class=", resA.mclass,
        " c_in_N(indep)=", resA.cInN_indep, " in_PB3(indep)=", resA.inPB3_indep,
        " hexagonFull=", resA.hexagonFull, " canaryFwd=", resA.canaryFwd,
        " canaryRev=", resA.canaryRev, " discrim=", resA.canaryDiscrim,
        " surj=", resA.surjOK, "\n");
  Print("  B-side: |Q|=", resB.sizeN, " class=", resB.mclass,
        " c_in_N(indep)=", resB.cInN_indep, " in_PB3(indep)=", resB.inPB3_indep,
        " hexagonFull=", resB.hexagonFull, " canaryFwd=", resB.canaryFwd,
        " canaryRev=", resB.canaryRev, " discrim=", resB.canaryDiscrim,
        " surj=", resB.surjOK, "\n");

  Add(AllResults, resA);;
  Add(AllResults, resB);;

  if GAPLIB_CheckCap(1700.0, "twin-witness-mirror-v1_1 per-pair pass") then
    Print("[CAP WARNING] stopping early\n");
    break;
  fi;
od;

t1 := GAPLIB_WallElapsedMs();
Print("\n=== ALL WINDOWS DONE (", Length(AllResults), " directed entries), elapsed_ms=", t1 - t0, " ===\n");

#############################################################################
## ---------------------- summary -------------------------------------------
#############################################################################
countM0 := 0;; countM1 := 0;; countM2 := 0;;
allHexagonOK := true;; allCanaryDiscrim := true;; allSurjOK := true;;
allCinNOK := true;; allInPB3OK := true;;
for r in AllResults do
  if r.mclass = "M0" then countM0 := countM0+1;
  elif r.mclass = "M1" then countM1 := countM1+1;
  else countM2 := countM2+1; fi;
  allHexagonOK := allHexagonOK and r.hexagonFull;;
  allCanaryDiscrim := allCanaryDiscrim and r.canaryDiscrim;;
  allSurjOK := allSurjOK and r.surjOK;;
  allCinNOK := allCinNOK and r.cInN_indep;;
  allInPB3OK := allInPB3OK and r.inPB3_indep;;
od;
Print("\n=== SUMMARY (v1.1, 30 directed entries) ===\n");
Print("M0=", countM0, " M1=", countM1, " M2=", countM2, "\n");
Print("all directed windows: hexagonFull=", allHexagonOK,
      " canaryDiscrim=", allCanaryDiscrim, " surjOK=", allSurjOK,
      " c_in_N(indep)=", allCinNOK, " in_PB3(indep)=", allInPB3OK, "\n");

#############################################################################
## ---------------------- MC-1 v1.1 export (ALL 15 pairs, BOTH directions) --
#############################################################################
## Frozen schema (prereg doc sec 2.7) fields, all populated:
##   target_window_uid, source_kernel_uid, index, in_PB3, c_in_N,
##   perm_degree, s1_perm, s2_perm, N_gen_words, K_gen_words,
##   witness_word, shadow{m,f_word}, checks{braid,N_in_ker,K_in_ker,
##   imorder,iota_w_nontrivial,hexagon_full,surj}
## PLUS (beyond frozen schema, additive only): mclass, canary_fwd/rev/discrim,
## cInN_indep/inPB3_indep (independently recomputed, for D-3 compliance).
JStrLocal := function(s) return Concatenation("\"", s, "\""); end;;

mc1Parts := [];;
Add(mc1Parts, "{\n  \"schema\": \"mirror_cert/v1.1 (frozen v1 schema fully populated + additive fields)\",\n");
Add(mc1Parts, "  \"mirror_certs\": [\n");
first := true;;
for r in AllResults do
  isoN := IsomorphismPermGroup(r.QN);;
  QNp := Image(isoN);;
  s1p := ImageElm(isoN, r.qa);;
  s2p := ImageElm(isoN, r.qb);;
  deg := LargestMovedPoint(QNp);;
  if deg = 0 or deg = fail then deg := NrMovedPoints(QNp); fi;
  if deg = 0 then deg := 1; fi;   # degenerate guard (should not occur here)
  s1list := List([1..deg], i -> i^s1p);;
  s2list := List([1..deg], i -> i^s2p);;

  ## checks{} block per frozen schema
  braidCheck := true;;   # universal, holds by construction of B3 (relator)
  nInKerCheck := ForAll(r.Nwords, w -> ImageElm(r.hmN, EvalWordB3(w)) = One(r.QN));;
  ## K_in_ker: partner's words trivial under iota-substitution (= mirror partner test)
  a := ga^-1;; b := gb^-1;;
  kInKerCheck := ForAll(r.Kwords, w -> ImageElm(r.hmN, EvalWordB3(w)) = One(r.QN));;
  a := ga;; b := gb;;
  imorderCheck := (r.sizeN = r.index);;
  iotaWNontrivial := (r.witnessWord <> fail);;

  if not first then Add(mc1Parts, ",\n"); fi;
  first := false;;
  Add(mc1Parts, Concatenation(
    "    {\n",
    "      \"index\": ", String(r.index), ",\n",
    "      \"pair_uid\": ", JStrLocal(r.pair_uid), ",\n",
    "      \"target_window_uid\": ", JStrLocal(r.N_uid), ",\n",
    "      \"source_kernel_uid\": ", JStrLocal(r.K_uid), ",\n",
    "      \"in_PB3\": ", JB(r.inPB3_indep), ",\n",
    "      \"c_in_N\": ", JB(r.cInN_indep), ",\n",
    "      \"perm_degree\": ", String(deg), ",\n",
    "      \"s1_perm\": ", JArr(List(s1list, String)), ",\n",
    "      \"s2_perm\": ", JArr(List(s2list, String)), ",\n",
    "      \"N_gen_words\": ", JArr(List(r.Nwords, JStrLocal)), ",\n",
    "      \"K_gen_words\": ", JArr(List(r.Kwords, JStrLocal)), ",\n",
    "      \"witness_word\": ", (function() if r.witnessWord=fail then return "null"; else return JStrLocal(r.witnessWord); fi; end)(), ",\n",
    "      \"shadow\": { \"m\": -1, \"f_word\": [] },\n",
    "      \"checks\": {\n",
    "        \"braid\": ", JB(braidCheck), ",\n",
    "        \"N_in_ker\": ", JB(nInKerCheck), ",\n",
    "        \"K_in_ker\": ", JB(kInKerCheck), ",\n",
    "        \"imorder\": ", JB(imorderCheck), ",\n",
    "        \"iota_w_nontrivial\": ", JB(iotaWNontrivial), ",\n",
    "        \"hexagon_full\": ", JB(r.hexagonFull), ",\n",
    "        \"surj\": ", JB(r.surjOK), "\n",
    "      },\n",
    "      \"mclass\": ", JStrLocal(r.mclass), ",\n",
    "      \"canary_v1_1\": {\n",
    "        \"forward_paper_product_trivial\": ", JB(r.canaryFwd), ",\n",
    "        \"reversed_convention_trivial\": ", JB(r.canaryRev), ",\n",
    "        \"discriminates\": ", JB(r.canaryDiscrim), "\n",
    "      }\n",
    "    }"
  ));
od;
Add(mc1Parts, "\n  ]\n}\n");
WriteFile("search/certs/twin_witness_mc1_export_v1_1_20260806.json", Concatenation(mc1Parts));
Print("\nWrote search/certs/twin_witness_mc1_export_v1_1_20260806.json\n");
Print("ALL_DONE\n");
