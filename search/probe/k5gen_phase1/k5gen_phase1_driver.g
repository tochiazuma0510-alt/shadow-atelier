#############################################################################
## search/probe/k5gen_phase1/k5gen_phase1_driver.g
## K^(5) genuine 戦役 Phase 1 較正(K5-1..K5-5)。Sol 便99検収(裁定412・
## F99-4.1)で GO・認可範囲は K5-1..K5-5 のみ。設計正本:
## docs/notes/k5_genuine_campaign_v1.md SS5(実装様式)・SS5.2(段の定義)・
## SS5.3(識別力fixture)・SS5.5(停止規則 S-1..S-6)・SS6.1 N-1(theta_epsの語)。
##
## 実行してよいのはこの5段だけ(裁定412 F99-4.1・逸脱禁止):
##  K5-1(アンカーA1): K5.v1.json / K15.v1.json の (m,f_triple) 座標を読み、
##    R:(m~,k~)->(m~ mod10, k~ mod5) の像を整数演算で計算(★追加列挙ゼロ)。
##  K5-2(アンカーA2): 既存 K3 プローブ(K9/K18/L01/M01 の reduction:{to:"K3"})
##    にK3 側dの抽出(既知値 d=3 x4)を適用。
##  K5-3(アンカーA3): ScanRoofHexagon を K^(5) 単体(MakeGn(5))に適用 -> 40。
##  K5-4(アンカーA4): 同関数を K^(3) 単体(MakeGn(3))に適用 -> 12。
##  K5-5(識別力): SS5.3 の DF-1/DF-2/DF-3 を d 抽出器に流す。
##
## 証明書非読の例外: K5-1(K5.v1.json/K15.v1.json)と K5-2(K9/K18/L01/M01の
## reduction欄)は、その定義そのものが既存cert座標の突合であるため読む
## (SS5.2の記述どおり)。K5-3/K5-4/K5-5 は一切 certificates/*.json を読まない
## (期待値は本ファイル内のリテラル定数)。この解釈は司令塔への報告事項。
##
## namespace: 出力は certificates/k5gen/ のみ(SS6.2 X-8・既存
## k5blocks/k5e/k5fixture/k5pipeline には1バイトも書かない)。
## eps欄名は theta_eps(SS6.1 N-1・epsbitsの語を使わない・grep自己検査対象)。
##
## 停止規則: S-1(アンカー外れ即停止)・S-2(DF-1がd=1を返さないなら即停止)。
## S-3(T1でd_N=1)・S-4(封印量接触)・S-6(settled fail)は Phase1 の範囲外
## (T1/T2 の本測定を一切行わないため発火しない)。
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_k5gen_p1_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then
    Error("k5gen_phase1_driver: ComputeSha256File: sha256sum did not return a hash line for ", relpath);
  fi;
  return line{[1 .. 64]};
end;;

ModInverse := function(a, n)
  local k;
  for k in [1 .. n-1] do
    if (a*k) mod n = 1 then return k; fi;
  od;
  Error("ModInverse: no inverse of ", a, " mod ", n);
end;;

Kappa := function(m, n)
  if m mod 2 = 1 then return (m+1) mod n; else return (-m) mod n; fi;
end;;

CharmingSetOfN := function(nOrd)
  return Filtered([0 .. nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);
end;;

## ---- 単一定義: 簡約 hexagon 判定式(ihnec_r4b_run.g ScanRoofHexagon と逐語同一) ----
## EnumerateReducedHexagon(week3-battery-common.g)と数学的に同一の判定式。
## 列挙戦略のみ Elements(DerivedSubgroup(G)) の直接列挙(word不要・RAM節約)。
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

STOP_HIT := false;;
STOP_STAGE := "";;
STOP_REASON := "";;
STOP_OBSERVED := "";;
STOP_EXPECTED := "";;

HaltNow := function(stage, reason, observed, expected)
  STOP_HIT := true;;
  STOP_STAGE := stage;;
  STOP_REASON := reason;;
  STOP_OBSERVED := observed;;
  STOP_EXPECTED := expected;;
  Print("\n*** S-1/S-2 STOP at ", stage, ": ", reason,
        "  observed=", observed, "  expected=", expected, " ***\n");
end;;

#############################################################################
## ==== K5-0: 宇宙の再現(K5-3の前提・MakeGn(5)) ====
#############################################################################
Print("=== K5-0: 宇宙の再現 G5 = MakeGn(5) ===\n");
g5 := MakeGn(5);;
G5size := Size(g5.G);;
G5derivedSize := Size(DerivedSubgroup(g5.G));;
K5ord := Lcm(Order(g5.x), Order(g5.y));;
X5 := CharmingSetOfN(K5ord);;
Print("  |PB3/K5|=", G5size, " (expect 500)  |[G5,G5]|=", G5derivedSize,
      " (expect 125)  K5_ord=", K5ord, " (expect 10)\n");
Print("  X5=", X5, " (expect [0,1,3,4,5,6,8,9])\n");
k50_pass := (G5size = 500) and (G5derivedSize = 125) and (K5ord = 10)
            and (X5 = [0,1,3,4,5,6,8,9]);;
if not k50_pass then
  HaltNow("K5-0", "universe reproduction mismatch",
          Concatenation("|G5|=",String(G5size),",|D|=",String(G5derivedSize),
                         ",K5ord=",String(K5ord),",X5=",String(X5)),
          "|G5|=500,|D|=125,K5ord=10,X5=[0,1,3,4,5,6,8,9]");
fi;

#############################################################################
## ==== K5-1(アンカーA1・★追加列挙ゼロ): K5.v1.json / K15.v1.json 座標突合 ====
## 証明書非読の例外点その1。K5/K15 の (m,f_triple) を読み、Theta5・reduction
## R:(m~,k~) -> (m~ mod10, k~ mod5) を整数演算のみで計算する。
## Im の測定(T1/T2)は一切行わない -- 既存2証明書の座標の内部無矛盾性のみ。
#############################################################################
if not STOP_HIT then
Print("\n=== K5-1: K5.v1.json / K15.v1.json 座標突合(アンカーA1) ===\n");
inv2_5 := ModInverse(2, 5);;
Print("  inv2 mod 5 = ", inv2_5, " (expect 3)\n");

k5CertShadows := ParseK3Shadows("certificates/K5.v1.json");;
Print("  K5.v1.json shadow count = ", Length(k5CertShadows), " (expect 40)\n");

## Theta5 from cert: (k,u,eps) for each of the 40 shadows, plus (m,k) pairs.
k5CertTheta := [];;
k5CertMK := [];;
k5CertReflOK := true;;
for s5c in k5CertShadows do
  a1 := s5c.triple[1][1];;  e1 := s5c.triple[1][2];;
  a2 := s5c.triple[2][1];;  e2 := s5c.triple[2][2];;
  a3 := s5c.triple[3][1];;  e3 := s5c.triple[3][2];;
  if e1 <> 0 or e2 <> 0 or e3 <> 0 then k5CertReflOK := false;; fi;
  kk := (inv2_5 * a1) mod 5;;
  uu := (2*s5c.m + 1) mod 5;;
  ee := s5c.m mod 2;;
  Add(k5CertTheta, [kk, uu, ee]);;
  Add(k5CertMK, [s5c.m mod 10, kk]);;
od;
k5CertThetaSet := Set(k5CertTheta);;
k5CertMKSet := Set(k5CertMK);;
Print("  K5 cert: reflection-free = ", k5CertReflOK, "  |Theta5 set| = ",
      Length(k5CertThetaSet), " (expect 40)\n");

k15CertShadows := ParseK3Shadows("certificates/K15.v1.json");;
Print("  K15.v1.json shadow count = ", Length(k15CertShadows), " (expect 240)\n");
inv2_15 := ModInverse(2, 15);;
Print("  inv2 mod 15 = ", inv2_15, " (expect 8)\n");

k15Rimage := [];;
k15MValues := Set(List(k15CertShadows, s -> s.m));;
for s15c in k15CertShadows do
  a1_15 := s15c.triple[1][1];;
  k15 := (inv2_15 * a1_15) mod 15;;
  Add(k15Rimage, [s15c.m mod 10, k15 mod 5]);;
od;
k15RimageSet := Set(k15Rimage);;
## fiber sizes over the 40 target pairs
fiberSizes := List(k15RimageSet, pr -> Length(Filtered(k15Rimage, x -> x = pr)));;
fiberUniform6 := (Set(fiberSizes) = [6]);;
## m-part map: X15 (16 values) -> X5 (8 values) mod 10, 2-to-1
m15mod10 := Set(List(k15MValues, mm -> mm mod 10));;
m15fiberSizes := List(m15mod10, mv -> Length(Filtered(k15MValues, mm -> mm mod 10 = mv)));;
m15TwoToOne := (Set(m15fiberSizes) = [2]);;

Print("  |X15| = ", Length(k15MValues), " (expect 16)\n");
Print("  R image size = ", Length(k15RimageSet), " (expect 40)\n");
Print("  R image = K5 cert (m mod10,k) set ? ", (k15RimageSet = k5CertMKSet), "\n");
Print("  fiber uniform 6 ? ", fiberUniform6, "  fiber sizes seen = ", Set(fiberSizes), "\n");
Print("  m-part X15->X5 surjective 2-to-1 ? ", m15TwoToOne, " and onto X5 ? ",
      (m15mod10 = Set(X5)), "\n");

k51_pass := k5CertReflOK and (Length(k5CertThetaSet) = 40)
            and (Length(k15CertShadows) = 240) and (Length(k15MValues) = 16)
            and (Length(k15RimageSet) = 40) and (k15RimageSet = k5CertMKSet)
            and fiberUniform6 and m15TwoToOne and (m15mod10 = Set(X5));;
Print("  K5-1 (P-K5-2 instance) pass = ", k51_pass, "\n");
if not k51_pass then
  HaltNow("K5-1", "K5/K15 cert coordinate cross-check (P-K5-2) failed",
          Concatenation("reflOK=",String(k5CertReflOK),
            ",|thetaSet|=",String(Length(k5CertThetaSet)),
            ",|K15shadows|=",String(Length(k15CertShadows)),
            ",|X15|=",String(Length(k15MValues)),
            ",|Rimage|=",String(Length(k15RimageSet)),
            ",Rimage=K5MK?",String(k15RimageSet = k5CertMKSet),
            ",fiberUniform6=",String(fiberUniform6),
            ",m15TwoToOne=",String(m15TwoToOne)),
          "reflOK=true,|thetaSet|=40,|K15shadows|=240,|X15|=16,|Rimage|=40,Rimage=K5MK?true,fiberUniform6=true,m15TwoToOne=true");
fi;
fi;

#############################################################################
## ==== K5-2(アンカーA2): 既存 K3 プローブ4本の reduction 突合(d=3 x4) ====
## K9.v1.json / K18.v1.json / L01.v1.json / M01.v1.json の reduction:{to:"K3"}
## 欄(既存資産)を読み、image が K3 の12元へ全射(=full)であることを確認する。
## 全射ならば Im=GT(K3) 全体 ⟹ Im∩F0_3=F0_3(サイズ3)⟹ d=3(既測FV-05相当)。
#############################################################################
if not STOP_HIT then
Print("\n=== K5-2: 既存K3プローブ4本の reduction 突合(アンカーA2) ===\n");

ReadReductionImage := function(path)
  local content, stream, mk, pos, mk2, pos2, arrStr, ints, mkSurj, posSurj, surjStr;
  stream := InputTextFile(path);
  if stream = fail then Error("ReadReductionImage: cannot open ", path); fi;
  content := ReadAll(stream);
  CloseStream(stream);
  mk := "\"image\":[";
  pos := FindPositionFrom(content, mk, 1);
  if pos = fail then Error("ReadReductionImage: image marker not found in ", path); fi;
  mk2 := "],\"surjective\":";
  pos2 := FindPositionFrom(content, mk2, pos);
  if pos2 = fail then Error("ReadReductionImage: surjective marker not found in ", path); fi;
  arrStr := content{[pos+Length(mk) .. pos2-1]};
  ints := DigitRunsToInts(arrStr);
  posSurj := pos2 + Length(mk2);
  if content{[posSurj..posSurj+3]} = "true" then surjStr := true; else surjStr := false; fi;
  return rec(image := ints, surjective := surjStr);
end;;

k3ProbeFiles := ["certificates/K9.v1.json", "certificates/K18.v1.json",
                 "certificates/L01.v1.json", "certificates/M01.v1.json"];;
k3ProbeResults := [];;
for pth in k3ProbeFiles do
  rr := ReadReductionImage(pth);;
  imgSet := Set(rr.image);;
  fullOnto12 := (imgSet = Set([0..11]));;
  dVal := 0;;
  if fullOnto12 and rr.surjective then dVal := 3;; else dVal := -1;; fi;
  Add(k3ProbeResults, rec(path := pth, image_len := Length(rr.image),
                          image_distinct := Length(imgSet), surjective := rr.surjective,
                          full_onto_12 := fullOnto12, d := dVal));
  Print("  ", pth, ": image_len=", Length(rr.image), " distinct=", Length(imgSet),
        " surjective=", rr.surjective, " full_onto_12=", fullOnto12, " => d=", dVal, "\n");
od;

k52_pass := ForAll(k3ProbeResults, r -> r.full_onto_12 and r.surjective and r.d = 3);;
Print("  K5-2 (4 probes all d=3) pass = ", k52_pass, "\n");
if not k52_pass then
  HaltNow("K5-2", "K3 probe anchor (4x d=3) failed",
          List(k3ProbeResults, r -> [r.path, r.d]), "all d=3");
fi;
fi;

#############################################################################
## ==== K5-3(アンカーA3): ScanRoofHexagon(K5単体) -> 40、Theta集合をK5-1と突合 ====
#############################################################################
if not STOP_HIT then
Print("\n=== K5-3: ScanRoofHexagon(K5 単体) (アンカーA3) ===\n");
qrec5 := rec(x := g5.x, y := g5.y, G := g5.G);;
t0 := Runtime();;
res5 := ScanRoofHexagon(qrec5, X5);;
t1 := Runtime();;
Print("  candidate_total=", res5.candidate_total, " h10_fail=", res5.h10_fail,
      " h11_fail=", res5.h11_fail, " generation_fail=", res5.generation_fail,
      " shadow_total=", res5.shadow_total, " (expect 40)  time_ms=", t1-t0, "\n");

## extract Theta5 from freshly-built shadows (independent of the cert read in K5-1)
freshTheta5 := [];;
allElts40 := [];;   # rec(m,k,u,theta_eps) for K5-5 use
for sh5 in res5.shadows do
  b1 := compOfFix(sh5.f, 1, 5);;  ae1 := DnElemToAE(b1, g5.r, g5.s, 5);;
  b2 := compOfFix(sh5.f, 2, 5);;  ae2 := DnElemToAE(b2, g5.r, g5.s, 5);;
  b3 := compOfFix(sh5.f, 3, 5);;  ae3 := DnElemToAE(b3, g5.r, g5.s, 5);;
  reflOK := (ae1[2]=0) and (ae2[2]=0) and (ae3[2]=0);;
  kkf := (inv2_5 * ae1[1]) mod 5;;
  uuf := (2*sh5.m + 1) mod 5;;
  eef := sh5.m mod 2;;
  Add(freshTheta5, [kkf, uuf, eef, reflOK, ae2[1], ae3[1]]);;
  Add(allElts40, rec(m := sh5.m, k := kkf, u := uuf, theta_eps := eef));;
od;
freshReflOK := ForAll(freshTheta5, t -> t[4]);;
## structural check: f_triple = (r^{2k}, r^{-2k}, r^{kappa(m)}) (SS1.3) -- second/third
## component consistency, computed per-shadow (not per-tuple, since m is needed for kappa).
freshK2OK := true;;  freshK3OK := true;;
for sh5b in res5.shadows do
  bb1 := compOfFix(sh5b.f, 1, 5);;  aa1 := DnElemToAE(bb1, g5.r, g5.s, 5)[1];;
  bb2 := compOfFix(sh5b.f, 2, 5);;  aa2 := DnElemToAE(bb2, g5.r, g5.s, 5)[1];;
  bb3 := compOfFix(sh5b.f, 3, 5);;  aa3 := DnElemToAE(bb3, g5.r, g5.s, 5)[1];;
  kkb := (inv2_5 * aa1) mod 5;;
  if (aa2 mod 5) <> ((-2*kkb) mod 5) then freshK2OK := false;; fi;
  if (aa3 mod 5) <> (Kappa(sh5b.m, 5) mod 5) then freshK3OK := false;; fi;
od;
freshThetaSet := Set(List(freshTheta5, t -> [t[1],t[2],t[3]]));;
Print("  fresh reflection-free = ", freshReflOK, "  |fresh Theta5 set| = ",
      Length(freshThetaSet), " (expect 40)\n");
Print("  fresh Theta5 set = K5-1 cert-derived Theta5 set ? ",
      (freshThetaSet = k5CertThetaSet), "\n");

k53_pass := (res5.shadow_total = 40) and freshReflOK and freshK2OK and freshK3OK
            and (Length(freshThetaSet) = 40) and (freshThetaSet = k5CertThetaSet);;
Print("  K5-3 pass = ", k53_pass, "\n");
if not k53_pass then
  HaltNow("K5-3", "ScanRoofHexagon(K5 alone) anchor failed",
          Concatenation("shadow_total=",String(res5.shadow_total),
            ",freshReflOK=",String(freshReflOK),
            ",|freshThetaSet|=",String(Length(freshThetaSet)),
            ",matchesCert=",String(freshThetaSet = k5CertThetaSet)),
          "shadow_total=40,freshReflOK=true,|freshThetaSet|=40,matchesCert=true");
fi;
fi;

#############################################################################
## ==== K5-4(アンカーA4): ScanRoofHexagon(K3単体) -> 12(向き規約の経時変化検出) ====
#############################################################################
if not STOP_HIT then
Print("\n=== K5-4: ScanRoofHexagon(K3 単体) (アンカーA4) ===\n");
g3 := MakeGn(3);;
K3ord := Lcm(Order(g3.x), Order(g3.y));;
X3 := CharmingSetOfN(K3ord);;
Print("  |PB3/K3|=", Size(g3.G), "  K3_ord=", K3ord, " (expect 6)  X3=", X3, " (expect [0,2,3,5])\n");
qrec3 := rec(x := g3.x, y := g3.y, G := g3.G);;
t0 := Runtime();;
res3 := ScanRoofHexagon(qrec3, X3);;
t1 := Runtime();;
Print("  candidate_total=", res3.candidate_total, " h10_fail=", res3.h10_fail,
      " h11_fail=", res3.h11_fail, " generation_fail=", res3.generation_fail,
      " shadow_total=", res3.shadow_total, " (expect 12)  time_ms=", t1-t0, "\n");

k54_pass := (K3ord = 6) and (X3 = [0,2,3,5]) and (res3.shadow_total = 12);;
Print("  K5-4 pass = ", k54_pass, "\n");
if not k54_pass then
  HaltNow("K5-4", "ScanRoofHexagon(K3 alone) anchor failed",
          Concatenation("K3ord=",String(K3ord),",X3=",String(X3),
            ",shadow_total=",String(res3.shadow_total)),
          "K3ord=6,X3=[0,2,3,5],shadow_total=12");
fi;
fi;

#############################################################################
## ==== K5-5(識別力): DF-1/DF-2/DF-3(SS5.3) ====
## 抽出器: 与えられた候補像 Im(allElts40 の部分集合)から
##   d_N          = |Im cap F0|            (F0 = {theta_eps=0, u=1})
##   image_size   = |Im|
##   chi_image    = {(2*e.m+1) mod 20 : e in Im}   (theta_epsではなくmから直接;
##                    定義そのもの chi~=[m,f]->2m+1 mod20 を使う -- CRT再構成は
##                    しない、cert非読の代わりにfreshに作った allElts40 のmを使う)
##   iota_in_image = iota(theta=(0,4,1)) in Im ?
#############################################################################
if not STOP_HIT then
Print("\n=== K5-5: 識別力fixture DF-1/DF-2/DF-3 ===\n");

Q20units := Filtered([0..19], a -> Gcd(a,20)=1);;

ExtractMeasurement := function(ImList, allElts)
  local d_N, imageSize, chiSet, iotaIn, F0cnt;
  F0cnt := Length(Filtered(ImList, e -> e.u = 1 and e.theta_eps = 0));;
  d_N := F0cnt;;
  imageSize := Length(ImList);;
  chiSet := Set(List(ImList, e -> (2*e.m+1) mod 20));;
  iotaIn := ForAny(ImList, e -> e.k=0 and e.u=4 and e.theta_eps=1);;
  return rec(d_N := d_N, image_size := imageSize, chi_image := chiSet,
             chi_image_full := (chiSet = Set(Q20units)), iota_in_image := iotaIn);
end;;

## DF-1: H1 = Q^std = {k=0} (8 elements)
H1list := Filtered(allElts40, e -> e.k = 0);;
mDF1 := ExtractMeasurement(H1list, allElts40);;
Print("  DF-1 (H1, |H1|=", Length(H1list), "): d_N=", mDF1.d_N,
      " image_size=", mDF1.image_size, " chi_image=", mDF1.chi_image,
      " chi_image_full=", mDF1.chi_image_full, " iota_in_image=", mDF1.iota_in_image, "\n");
df1_pass := (Length(H1list) = 8) and (mDF1.d_N = 1) and (mDF1.image_size = 8)
            and mDF1.chi_image_full and mDF1.iota_in_image;;
Print("  DF-1 pass (expect d_N=1,image_size=8,chi full,iota true) = ", df1_pass, "\n");

## S-2: if DF-1 does not give d_N=1, halt immediately (before checking DF-2/DF-3)
if not df1_pass then
  HaltNow("K5-5-DF1", "S-2: discriminating fixture DF-1 did not return d_N=1",
          Concatenation("|H1|=",String(Length(H1list)),",d_N=",String(mDF1.d_N),
            ",image_size=",String(mDF1.image_size),",chi_full=",String(mDF1.chi_image_full),
            ",iota_in=",String(mDF1.iota_in_image)),
          "|H1|=8,d_N=1,image_size=8,chi_full=true,iota_in=true");
fi;
fi;

if not STOP_HIT then
## DF-2: H^bad = {theta_eps=0} (20 elements, parity trap)
Hbadlist := Filtered(allElts40, e -> e.theta_eps = 0);;
mDF2 := ExtractMeasurement(Hbadlist, allElts40);;
Print("  DF-2 (H^bad, |H^bad|=", Length(Hbadlist), "): d_N=", mDF2.d_N,
      " image_size=", mDF2.image_size, " chi_image=", mDF2.chi_image,
      " chi_image_full=", mDF2.chi_image_full, " iota_in_image=", mDF2.iota_in_image, "\n");
df2_pass := (Length(Hbadlist) = 20) and (mDF2.d_N = 5) and (mDF2.image_size = 20)
            and (Length(mDF2.chi_image) = 4) and (not mDF2.chi_image_full)
            and (not mDF2.iota_in_image);;
Print("  DF-2 pass (expect d_N=5,image_size=20,|chi|=4(broken),iota false) = ", df2_pass, "\n");

## DF-3: X5 に m=2(notin X5) を混ぜた charming set を ScanRoofHexagon(K5)へ与え、
## charming_pass(=shadow_total)が増えないことを確認(生成器側の向き規約 CV-13)。
X5corrupt := Concatenation(X5, [2]);;
Print("  X5corrupt = ", X5corrupt, " (m=2 injected, gcd(5,10)=5 so m=2 should never survive)\n");
t0 := Runtime();;
res5corrupt := ScanRoofHexagon(qrec5, X5corrupt);;
t1 := Runtime();;
Print("  res5corrupt.shadow_total=", res5corrupt.shadow_total, " (expect = res5.shadow_total = ",
      res5.shadow_total, ")  time_ms=", t1-t0, "\n");
m2Shadows := Filtered(res5corrupt.shadows, s -> s.m = 2);;
Print("  shadows with m=2 in corrupted run = ", Length(m2Shadows), " (expect 0)\n");
df3_pass := (res5corrupt.shadow_total = res5.shadow_total) and (Length(m2Shadows) = 0);;
Print("  DF-3 pass (charming_pass does not increase, m=2 contributes 0 shadows) = ", df3_pass, "\n");

k55_pass := df1_pass and df2_pass and df3_pass;;
Print("  K5-5 (P-K5-11) pass = ", k55_pass, "\n");
if not k55_pass and df1_pass then
  ## DF-1 itself already passed (S-2 did not fire); DF-2/DF-3 failing is a plain
  ## anchor-style fixture failure -- record via the generic stop path too, since a
  ## broken discriminating power still means "以後の全PASSは情報量ゼロ".
  HaltNow("K5-5-DF23", "discriminating fixture DF-2/DF-3 failed",
          Concatenation("df2_pass=",String(df2_pass),",df3_pass=",String(df3_pass)),
          "df2_pass=true,df3_pass=true");
fi;
fi;

#############################################################################
## ==== JSON 出力(certificates/k5gen/ のみ) ====
#############################################################################
selfSha := ComputeSha256File("search/probe/k5gen_phase1/k5gen_phase1_driver.g");;
planSha := ComputeSha256File("docs/notes/k5_genuine_campaign_v1.md");;

OUT_DIR := "certificates/k5gen";;
if STOP_HIT then
  OUT_PATH := Concatenation(OUT_DIR, "/k5gen_phase1_STOP.json");;
else
  OUT_PATH := Concatenation(OUT_DIR, "/k5gen_phase1_20260802.json");;
fi;

if STOP_HIT then
  cert := Concatenation(
    "{\n",
    "  \"schema\":\"k5gen-phase1-stop/v1\",\n",
    "  \"generated_by\":\"search/probe/k5gen_phase1/k5gen_phase1_driver.g\",\n",
    "  \"card_label\":\"K5 genuine campaign Phase 1 (K5-1..K5-5) -- STOP (S-1/S-2)\",\n",
    "  \"design_doc\":\"docs/notes/k5_genuine_campaign_v1.md\",\n",
    "  \"stop\":{\n",
    "    \"stage\":", JStr(STOP_STAGE), ",\n",
    "    \"stop_reason\":", JStr(STOP_REASON), ",\n",
    "    \"observed\":", JStr(String(STOP_OBSERVED)), ",\n",
    "    \"expected\":", JStr(String(STOP_EXPECTED)), "\n",
    "  },\n",
    "  \"seal_declaration\":{\"touches_c_hat_mu\":false,\"touches_psl_sealed_fields\":false,\n",
    "    \"touches_wall_campaign_pbit\":false,\"touches_u_values\":false},\n",
    "  \"provenance\":{\n",
    "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
    "    \"script_sha256\":", JStr(selfSha), ",\n",
    "    \"plan_frozen_sha\":", JStr(planSha), ",\n",
    "    \"predictions_frozen\":\"docs/notes/k5_genuine_campaign_v1.md\",\n",
    "    \"wall_ms_total\":", String(GAPLIB_WallElapsedMs()), "\n",
    "  }\n",
    "}\n");;
  WriteFile(OUT_PATH, cert);;
  Print("\nWrote STOP cert ", OUT_PATH, "\n");
  Print("\nK5GEN_PHASE1_DRIVER_DONE (STOPPED at ", STOP_STAGE, ")\n");
fi;

if not STOP_HIT then
k3ProbeJson := function(r)
  return Concatenation("{\"path\":", JStr(r.path), ",\"image_len\":", String(r.image_len),
    ",\"image_distinct\":", String(r.image_distinct), ",\"surjective\":", JB(r.surjective),
    ",\"full_onto_12\":", JB(r.full_onto_12), ",\"d\":", String(r.d), "}");
end;;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"k5gen-phase1/v1\",\n",
  "  \"generated_by\":\"search/probe/k5gen_phase1/k5gen_phase1_driver.g\",\n",
  "  \"card_label\":\"K^(5) genuine campaign Phase 1 calibration (K5-1..K5-5)\",\n",
  "  \"design_doc\":\"docs/notes/k5_genuine_campaign_v1.md\",\n",
  "  \"authorization\":\"Sol 便99検収・裁定412 F99-4.1・GO(K5-1..K5-5のみ)\",\n",
  "  \"note\":\"Phase1は較正のみ。d_gen(5)の値・fake非存在・W-6の存在について本certは何も主張しない(裁定412 F99-4.1条項5)。K5-1/K5-2は既存certの座標・reduction突合そのもの(定義上の証明書読み込み)。K5-3/K5-4/K5-5は certificates/*.json を一切読まない(期待値はdriver内リテラル定数)。\",\n",
  "  \"target\":{\"family\":\"genuine-probe-calibration\",\"id\":\"K5gen.phase1\",\n",
  "    \"base\":{\"id\":\"K5\",\"n\":5,\"N_ord\":10,\"index_PB3\":500,\"gt_order\":40}},\n",
  "  \"tier\":\"calibration\",\n",
  "  \"anchors\":{\n",
  "    \"k5_universe\":{\"pass\":", JB(k50_pass), ",\"pb3_over_k5\":", String(G5size),
        ",\"derived_order\":", String(G5derivedSize), ",\"k5_ord\":", String(K5ord),
        ",\"x5\":", JArr(List(X5,String)), "},\n",
  "    \"k15_to_k5_reduction\":{\"pass\":", JB(k51_pass),
        ",\"k5_shadow_count\":", String(Length(k5CertShadows)),
        ",\"k15_shadow_count\":", String(Length(k15CertShadows)),
        ",\"x15_size\":", String(Length(k15MValues)),
        ",\"r_image_size\":", String(Length(k15RimageSet)),
        ",\"r_image_equals_k5_mk_set\":", JB(k15RimageSet = k5CertMKSet),
        ",\"fiber_uniform_6\":", JB(fiberUniform6),
        ",\"m_part_two_to_one_onto_x5\":", JB(m15TwoToOne and (m15mod10 = Set(X5))), "},\n",
  "    \"k3_probes\":{\"pass\":", JB(k52_pass), ",\"probes\":",
        JArr(List(k3ProbeResults, k3ProbeJson)), "},\n",
  "    \"k5_alone\":{\"pass\":", JB(k53_pass), ",\"shadow_total\":", String(res5.shadow_total),
        ",\"fresh_theta_matches_cert\":", JB(freshThetaSet = k5CertThetaSet), "},\n",
  "    \"k3_alone\":{\"pass\":", JB(k54_pass), ",\"shadow_total\":", String(res3.shadow_total),
        ",\"k3_ord\":", String(K3ord), ",\"x3\":", JArr(List(X3,String)), "},\n",
  "    \"discriminating_fixtures\":{\n",
  "      \"DF1\":{\"pass\":", JB(df1_pass), ",\"d_N\":", String(mDF1.d_N),
            ",\"image_size\":", String(mDF1.image_size), ",\"theta_eps_field_used\":true,\n",
  "            \"chi_image\":", JArr(List(mDF1.chi_image,String)), ",\"chi_image_full\":", JB(mDF1.chi_image_full),
            ",\"iota_in_image\":", JB(mDF1.iota_in_image), "},\n",
  "      \"DF2\":{\"pass\":", JB(df2_pass), ",\"d_N\":", String(mDF2.d_N),
            ",\"image_size\":", String(mDF2.image_size),
  "            ,\"chi_image\":", JArr(List(mDF2.chi_image,String)), ",\"chi_image_full\":", JB(mDF2.chi_image_full),
            ",\"iota_in_image\":", JB(mDF2.iota_in_image), "},\n",
  "      \"DF3\":{\"pass\":", JB(df3_pass), ",\"shadow_total_corrupt\":", String(res5corrupt.shadow_total),
            ",\"shadow_total_clean\":", String(res5.shadow_total),
            ",\"m2_shadow_count\":", String(Length(m2Shadows)), "}\n",
  "    }\n",
  "  },\n",
  "  \"anchors_all_pass\":", JB(k50_pass and k51_pass and k52_pass and k53_pass and k54_pass and k55_pass), ",\n",
  "  \"measurement\":{\"note\":\"Phase1は実測窓のT1/T2を一切走らせていない(K5-6以降は未認可)。d_Nはdiscriminating fixtureの自己較正値のみ(DF-1/DF-2)。eps欄名はtheta_epsであり壁キャンペーン語彙とは別物(SS6.1 N-1)。\"},\n",
  "  \"scope\":{\"lane\":\"GAP single lane\",\"cross_checked_status\":\"n/a(単系統GAP。cross-checkedを主張しない)\"},\n",
  "  \"conventions_used\":{\n",
  "    \"ledger_version\":\"conventions_ledger_v1_3\",\n",
  "    \"perm_composition\":\"gap_native_right_action\",\n",
  "    \"reduced_hexagon_predicate\":\"逐語 search/probe/wac_v1/ihnec_r4b_run.g ScanRoofHexagon(EnumerateReducedHexagonと数学的に同一) をそのままK5/K3単体に適用。列挙戦略はElements(DerivedSubgroup(G))直接列挙。\",\n",
  "    \"comparison_target\":\"K5-1/K5-2は既存cert(K5.v1.json/K15.v1.json/K9.v1.json/K18.v1.json/L01.v1.json/M01.v1.json)座標との突合。K5-3/K5-4/K5-5はdriver内リテラル定数のみとの突合(証明書非読)。\",\n",
  "    \"independence_note\":\"c_in_N=true window(K5,K3ともに MakeGn 経由・c not survivingの語彙は本windowに現れない)ゆえ quotient-shortcut theta/tau (GroupHomomorphismByImages) が有効。\"\n",
  "  },\n",
  "  \"seal_declaration\":{\"touches_c_hat_mu\":false,\"touches_psl_sealed_fields\":false,\n",
  "    \"touches_wall_campaign_pbit\":false,\"touches_u_values\":false},\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"plan_frozen_sha\":", JStr(planSha), ",\n",
  "    \"predictions_frozen\":\"docs/notes/k5_genuine_campaign_v1.md\",\n",
  "    \"wall_ms_total\":", String(GAPLIB_WallElapsedMs()), "\n",
  "  }\n",
  "}\n");;

WriteFile(OUT_PATH, cert);;
Print("\nWrote ", OUT_PATH, "\n");
Print("\nK5GEN_PHASE1_DRIVER_DONE\n");
fi;

QUIT;

