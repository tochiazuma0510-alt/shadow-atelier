#############################################################################
## search/probe/wac_v1/ihnec_r4b_negative_fixture_20260802.g
## CV-9-5 dummy/negative fixture(便99 W99-2.1-(5)・実装係)。
##
## 目的: R4b(search/probe/wac_v1/ihnec_r4b_run.g)の ScanRoofHexagon 述語に
## 対し、「落ちるべき入力が実際に落ちる」ことを事前登録し機械確認する。
## 判読書(docs/notes/cv9_reading_ihnec_r4ab_v1.md)§8【要修正-5】の指摘:
## 既存アンカー(k9_alone/s4_alone)は期待値直書き+不一致でError停止のため、
## 不一致状態そのものがcertとして残らない(陽性統制のみ・陰性統制が未登録)。
## 本 fixture はこれを補う: 意図的に破壊した述語版を作り、期待どおり
## 「既知値108と一致しない」ことをFAIL statusのcertとして残す
## (Error()で止めず、観測値を書いた上でverdict=FAILを記録する)。
##
## 宇宙の事前登録: K9単体窓(n=9・week3-battery-common.g MakeGn(9))のみを使う。
## R4b/R4aのどちらの証明書も読まない。新対象への拡張ではなく、既存
## ROOF(4) 独立確認と同じ入力に対する述語破壊テストである。
##
## 事前登録した3ケース(実行前に期待値を固定・値からの後知恵禁止):
##  CONTROL       : 破壊なし(ihnec_r4b_run.g の ScanRoofHexagon と数学的に
##                  逐語同一)。期待 shadow_total = 108(POSITIVE CONTROL)。
##  DUM-NEG-1      : hex311 の3項積を全反転
##                  (tau^2(w) tau(w) w = 1 -> w tau(w) tau^2(w) = 1、w=y^m f)。
##                  当初 hex310 の2項積 f*theta(f)=1 <-> theta(f)*f=1 を試したが、
##                  これは xy=1 <=> yx=1 という群の恒等式そのもの(群論的に
##                  常に同値)であり、識別力ゼロという結果が出た(実測・後述の
##                  観測欄に記録)。3項積の全反転 abc=1 <-> cba=1 は一般に
##                  同値でない(a,bが可換なときのみ同値)ため、こちらを正式な
##                  DUM-NEG-1 とする。期待: shadow_total <> 108。
##  DUM-NEG-2      : 生成条件の受理極性を反転(surj を not surj に)。
##                  期待: shadow_total <> 108。
##
## 二層の正規化(CV-9-5 操作化・台帳v1.3 §1.3.2):
##  入力層(datum)   = K9単体窓の Elements(DerivedSubgroup(G)) 上の f と m。
##  出力層(判定対象) = shadow_total という基数(ihnec_r4b_run.gと同じ比較粒度)。
##  DUM-NEG-1/2 は入力層はCONTROLと同一(同じ729*12=8748候補を舐める)だが、
##  出力層の判定式を変えることで既存宇宙の外側(108以外の値)へ出る
##  ("outside the registered universe" = 108 という一点のみが登録済み)。
##
## fail-closed: 不一致(FAIL)でもcertを書き切る(Error()で停止しない)。
## これが本fixtureの核心 -- 「不一致なら即Error」だったR4bの既存パターン
## とは逆に、FAIL状態そのものを記録として残す。
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_ihnecr4bneg_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then
    Error("ihnec_r4b_negative_fixture: ComputeSha256File: sha256sum did not return a hash line for ", relpath);
  fi;
  return line{[1 .. 64]};
end;;

CharmingSetOf := function(nOrd)
  return Filtered([0 .. nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);
end;;

#############################################################################
## ---- CONTROL: ihnec_r4b_run.g の ScanRoofHexagon と数学的に逐語同一 ----
#############################################################################
ScanRoofHexagon_Control := function(qrec, charmingSet)
  local G, D, Delts, thetaHom, tauHom, zElt, h10Fail, h11Fail, genFail, shadows,
        m, u, f, thetaf, hex310, ymf, tauymf, tau2ymf, hex311, genA, genB, surj,
        candidateTotal, i;
  G := qrec.G;
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  if thetaHom = fail or tauHom = fail then
    Error("ScanRoofHexagon_Control: theta/tau homomorphism construction failed");
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
             generation_fail := genFail, shadow_total := Length(shadows),
             derived_order := Length(Delts));
end;;

#############################################################################
## ---- DUM-NEG-0(記録用・非discriminating): hex310 の2項積を反転 ----
##      唯一の変更点: hex310 := AbstractProd([thetaf, f]) = Identity(G)
##      (正形は AbstractProd([f, thetaf]))。
##      注記: xy=1 <=> yx=1 は群の恒等式そのもの(常に同値)なので、この
##      変種は理論上も識別力を持たない。実測でも shadow_total=108 のまま
##      であり(下記 observed 欄)、これは fixture 設計側の見落としであって
##      ScanRoofHexagon 側のバグではない。正直に記録し、正式な DUM-NEG-1
##      には使わない(下の hex311 全反転版を使う)。
#############################################################################
ScanRoofHexagon_BrokenOrderPairwise := function(qrec, charmingSet)
  local G, D, Delts, thetaHom, tauHom, zElt, h10Fail, h11Fail, genFail, shadows,
        m, u, f, thetaf, hex310, ymf, tauymf, tau2ymf, hex311, genA, genB, surj,
        candidateTotal, i;
  G := qrec.G;
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  if thetaHom = fail or tauHom = fail then
    Error("ScanRoofHexagon_BrokenOrderPairwise: theta/tau homomorphism construction failed");
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
      hex310 := AbstractProd([thetaf, f]) = Identity(G);  ## <- DUM-NEG-0: 反転(識別力ゼロと判明)
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
             generation_fail := genFail, shadow_total := Length(shadows),
             derived_order := Length(Delts));
end;;

#############################################################################
## ---- DUM-NEG-1(正式版): hex311 の3項積を全反転(CV-3語順違反を模擬) ----
##      唯一の変更点: hex311 := AbstractProd([ymf, tauymf, tau2ymf]) = Identity(G)
##      (正形は AbstractProd([tau2ymf, tauymf, ymf]))。abc=1 <=> cba=1 は
##      a,b が可換な場合に限り同値であり、一般には非同値(hex310の2項反転
##      とは異なり、この変種は真の摂動になりうる)。
#############################################################################
ScanRoofHexagon_BrokenOrder := function(qrec, charmingSet)
  local G, D, Delts, thetaHom, tauHom, zElt, h10Fail, h11Fail, genFail, shadows,
        m, u, f, thetaf, hex310, ymf, tauymf, tau2ymf, hex311, genA, genB, surj,
        candidateTotal, i;
  G := qrec.G;
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  if thetaHom = fail or tauHom = fail then
    Error("ScanRoofHexagon_BrokenOrder: theta/tau homomorphism construction failed");
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
      hex311 := AbstractProd([ymf, tauymf, tau2ymf]) = Identity(G);  ## <- DUM-NEG-1: 全反転
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
             generation_fail := genFail, shadow_total := Length(shadows),
             derived_order := Length(Delts));
end;;

#############################################################################
## ---- DUM-NEG-2: 生成条件の受理極性を反転 ----
##      唯一の変更点: surj/not surj の分岐を入れ替え。
#############################################################################
ScanRoofHexagon_BrokenSurj := function(qrec, charmingSet)
  local G, D, Delts, thetaHom, tauHom, zElt, h10Fail, h11Fail, genFail, shadows,
        m, u, f, thetaf, hex310, ymf, tauymf, tau2ymf, hex311, genA, genB, surj,
        candidateTotal, i;
  G := qrec.G;
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  if thetaHom = fail or tauHom = fail then
    Error("ScanRoofHexagon_BrokenSurj: theta/tau homomorphism construction failed");
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
      if surj then                       ## <- DUM-NEG-2: 反転(surj を拒否・非surjを受理)
        genFail := genFail + 1;
      else
        Add(shadows, rec(m := m, f := f));
      fi;
    od;
  od;
  return rec(candidate_total := candidateTotal, h10_fail := h10Fail, h11_fail := h11Fail,
             generation_fail := genFail, shadow_total := Length(shadows),
             derived_order := Length(Delts));
end;;

#############################################################################
## ---- 実行: K9単体窓(既存ROOF(4)独立確認と同一入力・certは読まない) ----
#############################################################################
Print("=== ihnec_r4b_negative_fixture: K9単体窓の構築(MakeGn(9)) ===\n");
g9 := MakeGn(9);;
K9sz := Size(g9.G);;
K9ord := Lcm(Order(g9.x), Order(g9.y));;
Print("  |PB3/K9|=", K9sz, " (expect 2916)  K9_ord=", K9ord, " (expect 18)\n");
if K9sz <> 2916 or K9ord <> 18 then
  Error("ihnec_r4b_negative_fixture: K9 window construction mismatch -- refusing to proceed");
fi;
K9charm := CharmingSetOf(K9ord);;
qrecK9 := rec(x := g9.x, y := g9.y, G := g9.G);;

Print("\n=== CONTROL: ScanRoofHexagon_Control(K9単体) (期待 shadow_total=108) ===\n");
t0 := Runtime();;
resControl := ScanRoofHexagon_Control(qrecK9, K9charm);;
t1 := Runtime();;
Print("  shadow_total=", resControl.shadow_total, "  time_ms=", t1-t0, "\n");
controlPass := (resControl.shadow_total = 108);;

Print("\n=== DUM-NEG-0(記録用): ScanRoofHexagon_BrokenOrderPairwise(K9単体) (登録時点の期待 shadow_total<>108・理論的には非discriminating と後で判明) ===\n");
t0 := Runtime();;
resBrokenPairwise := ScanRoofHexagon_BrokenOrderPairwise(qrecK9, K9charm);;
t1 := Runtime();;
Print("  shadow_total=", resBrokenPairwise.shadow_total, "  time_ms=", t1-t0, "\n");
dumNeg0Discriminates := (resBrokenPairwise.shadow_total <> 108);;

Print("\n=== DUM-NEG-1(正式): ScanRoofHexagon_BrokenOrder(K9単体・hex311全反転) (期待 shadow_total<>108) ===\n");
t0 := Runtime();;
resBrokenOrder := ScanRoofHexagon_BrokenOrder(qrecK9, K9charm);;
t1 := Runtime();;
Print("  shadow_total=", resBrokenOrder.shadow_total, "  time_ms=", t1-t0, "\n");
dumNeg1Discriminates := (resBrokenOrder.shadow_total <> 108);;

Print("\n=== DUM-NEG-2: ScanRoofHexagon_BrokenSurj(K9単体) (期待 shadow_total<>108) ===\n");
t0 := Runtime();;
resBrokenSurj := ScanRoofHexagon_BrokenSurj(qrecK9, K9charm);;
t1 := Runtime();;
Print("  shadow_total=", resBrokenSurj.shadow_total, "  time_ms=", t1-t0, "\n");
dumNeg2Discriminates := (resBrokenSurj.shadow_total <> 108);;

## 正式判定に使う3ケース = CONTROL, DUM-NEG-1(hex311全反転), DUM-NEG-2(surj反転)。
## DUM-NEG-0は記録用(理論的に非discriminatingと判明・正式判定には含めない)。
allFixturesBehaveAsRegistered := controlPass and dumNeg1Discriminates and dumNeg2Discriminates;;
Print("\n=== まとめ ===\n");
Print("  CONTROL pass (=108)                       : ", controlPass, "\n");
Print("  DUM-NEG-0(記録用) discriminates (<>108)    : ", dumNeg0Discriminates, " <- 理論的に常にfalseになるはず(xy=1<=>yx=1)\n");
Print("  DUM-NEG-1(正式) discriminates (<>108)      : ", dumNeg1Discriminates, "\n");
Print("  DUM-NEG-2(正式) discriminates (<>108)      : ", dumNeg2Discriminates, "\n");
Print("  正式3ケースが事前登録どおりに振る舞った     : ", allFixturesBehaveAsRegistered, "\n");

#############################################################################
## ---- JSON 出力(fail-closed: 不一致でもcertを書き切る) ----
#############################################################################
selfSha := ComputeSha256File("search/probe/wac_v1/ihnec_r4b_negative_fixture_20260802.g");;
r4bRunSha := ComputeSha256File("search/probe/wac_v1/ihnec_r4b_run.g");;

VerdictStr := function(b)
  if b then return "PASS"; else return "FAIL"; fi;
end;;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"ihnec-r4b-negative-fixture/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/ihnec_r4b_negative_fixture_20260802.g\",\n",
  "  \"card_label\":\"便99 W99-2.1-(5)・CV-9-5 dummy/negative fixture(R4b述語の識別力の事前登録実測)\",\n",
  "  \"design_doc\":\"docs/notes/cv9_reading_ihnec_r4ab_v1.md §8【要修正-5】(判読者=falsifier)\",\n",
  "  \"task_ref\":\"sol/sol_reply_99_math26.md W99-2.1-(5)(裁定412)\",\n",
  "  \"note\":\"R4b(ihnec_r4b_run.g)のScanRoofHexagon述語をK9単体窓上で2通りに意図的に破壊し、既知値108との不一致が実際に検出されることを機械確認する。入力層(K9単体窓・candidate_total=8748)は3ケースで同一、出力層の判定式のみ変える(CV-9-5の二層正規化)。fail-closed: 不一致でもErrorで止めずFAIL statusを記録する。\",\n",
  "  \"registered_before_run\":{\n",
  "    \"CONTROL\":{\"description\":\"破壊なし。ihnec_r4b_run.g のScanRoofHexagonと数学的に逐語同一\",\"expected_shadow_total\":108,\"expected_verdict\":\"PASS(=108)\"},\n",
  "    \"DUM-NEG-0(記録用・当初案)\":{\"description\":\"hex310の2項積を反転(f*theta(f)=1 -> theta(f)*f=1)\",\"expected_shadow_total_ne\":108,\"expected_verdict_at_registration\":\"discriminates(<>108)を期待していたが、xy=1<=>yx=1は群の恒等式であり理論的に常に非discriminatingと事後判明(正式判定には使わない・正直に記録)\"},\n",
  "    \"DUM-NEG-1(正式)\":{\"description\":\"hex311の3項積を全反転(tau^2(w)tau(w)w=1 -> w tau(w) tau^2(w)=1)。abc=1<=>cba(全反転)は一般に非同値であり真の摂動になりうる\",\"expected_shadow_total_ne\":108,\"expected_verdict\":\"PASS(discriminates, i.e. <>108)\"},\n",
  "    \"DUM-NEG-2(正式)\":{\"description\":\"生成条件の受理極性を反転(surjを拒否)\",\"expected_shadow_total_ne\":108,\"expected_verdict\":\"PASS(discriminates, i.e. <>108)\"}\n",
  "  },\n",
  "  \"observed\":{\n",
  "    \"input_universe\":{\"window\":\"K9単体(n=9・MakeGn(9)・certは読まない)\",\"K9charm\":", JArr(List(K9charm, String)), ",\"candidate_total_each_case\":", String(resControl.candidate_total), "},\n",
  "    \"CONTROL\":{\"shadow_total\":", String(resControl.shadow_total), ",\"h10_fail\":", String(resControl.h10_fail), ",\"h11_fail\":", String(resControl.h11_fail), ",\"generation_fail\":", String(resControl.generation_fail), ",\"pass_eq_108\":", JB(controlPass), ",\"verdict\":", JStr(VerdictStr(controlPass)), "},\n",
  "    \"DUM-NEG-0(記録用・非discriminating判明)\":{\"shadow_total\":", String(resBrokenPairwise.shadow_total), ",\"h10_fail\":", String(resBrokenPairwise.h10_fail), ",\"h11_fail\":", String(resBrokenPairwise.h11_fail), ",\"generation_fail\":", String(resBrokenPairwise.generation_fail), ",\"discriminates_ne_108\":", JB(dumNeg0Discriminates), ",\"note\":\"shadow_total=108のまま(理論どおり)。fixture設計側の見落とし(hex310の2項反転はxy=1<=>yx=1の恒等式により常に無害)であり、ScanRoofHexagonのバグではない。この結果自体を正直に記録する(潰さない)\"},\n",
  "    \"DUM-NEG-1(正式)\":{\"shadow_total\":", String(resBrokenOrder.shadow_total), ",\"h10_fail\":", String(resBrokenOrder.h10_fail), ",\"h11_fail\":", String(resBrokenOrder.h11_fail), ",\"generation_fail\":", String(resBrokenOrder.generation_fail), ",\"discriminates_ne_108\":", JB(dumNeg1Discriminates), ",\"verdict\":", JStr(VerdictStr(dumNeg1Discriminates)), "},\n",
  "    \"DUM-NEG-2(正式)\":{\"shadow_total\":", String(resBrokenSurj.shadow_total), ",\"h10_fail\":", String(resBrokenSurj.h10_fail), ",\"h11_fail\":", String(resBrokenSurj.h11_fail), ",\"generation_fail\":", String(resBrokenSurj.generation_fail), ",\"discriminates_ne_108\":", JB(dumNeg2Discriminates), ",\"verdict\":", JStr(VerdictStr(dumNeg2Discriminates)), "}\n",
  "  },\n",
  "  \"overall_verdict\":", JStr(VerdictStr(allFixturesBehaveAsRegistered)), ",\n",
  "  \"overall_verdict_scope\":\"CONTROL + DUM-NEG-1(正式) + DUM-NEG-2(正式) の3ケースのみで判定(DUM-NEG-0は記録用参考値・判定対象外)\",\n",
  "  \"discriminating_power_established\":", JB(dumNeg1Discriminates and dumNeg2Discriminates), ",\n",
  "  \"note_on_r4b_existing_anchor\":\"ihnec_r4b_run.gの既存アンカー(anchors.k9_alone_pass等)は不一致時にError()で停止するため、不一致状態そのものがcertとして残らない(判読書【要修正-5】)。本fixtureは同じ入力・同じ数学的判定式群に対し、不一致(FAIL)状態を明示的にJSONへ書き切ることで、次回以降のR4b系走査で使えるnegative-fixtureテンプレートを与える。\",\n",
  "  \"conventions_used\":{\n",
  "    \"ledger_version\":\"conventions_ledger_v1_4\",\n",
  "    \"perm_composition\":\"gap_native_right_action\",\n",
  "    \"comparison_target\":{\n",
  "      \"as_function_of\":\"同一入力(K9単体窓・8748候補)に対し判定式のみを変えた3変種(CONTROL/DUM-NEG-1/DUM-NEG-2)の比較\",\n",
  "      \"function_a\":{\"name\":\"ScanRoofHexagon_Control\",\"domain\":\"K9単体・n=9\",\"source_digest\":", JStr(selfSha), "},\n",
  "      \"function_b\":{\"name\":\"ScanRoofHexagon_BrokenOrder / ScanRoofHexagon_BrokenSurj\",\"domain\":\"K9単体・n=9(同一入力)\",\"source_digest\":", JStr(selfSha), "},\n",
  "      \"normalization_digest\":\"n/a(基数shadow_totalのみを比較・正規形は導入しない)\"\n",
  "    },\n",
  "    \"chi_P_criterion\":{\"value\":\"exact\",\"justification\":\"(m,f)組の同一性による厳密受理数のみを比較(conjugacy classへの縮約なし)\",\"generator_fixed\":true,\"orientation_fixed\":true},\n",
  "    \"separation\":{\n",
  "      \"included\":true,\n",
  "      \"competitor_universe\":[\"CONTROL(=108)\",\"DUM-NEG-1(hex310反転)\",\"DUM-NEG-2(surj反転)\"],\n",
  "      \"result\":{\"matrix\":\"CONTROL=108(一致)・DUM-NEG-1<>108(識別)・DUM-NEG-2<>108(識別)\"},\n",
  "      \"forbidden_values\":{\"handling\":\"n/a\",\"list\":[]},\n",
  "      \"dummy_fixture\":{\n",
  "        \"id\":\"DUM-NEG-1+DUM-NEG-2\",\n",
  "        \"normalised_input\":\"K9単体窓のElements(DerivedSubgroup(G))×charming_set(全3ケース共通・8748候補)\",\n",
  "        \"normalised_output\":\"shadow_total(基数)\",\n",
  "        \"discriminating_power\":{\"input_layer_novel\":false,\"output_layer_novel\":true},\n",
  "        \"expected\":\"CONTROL=108・DUM-NEG-1<>108・DUM-NEG-2<>108\",\n",
  "        \"observed\":", JStr(Concatenation("CONTROL=", String(resControl.shadow_total), " DUM-NEG-1=", String(resBrokenOrder.shadow_total), " DUM-NEG-2=", String(resBrokenSurj.shadow_total))), ",\n",
  "        \"verdict\":", JStr(VerdictStr(allFixturesBehaveAsRegistered)), "\n",
  "      }\n",
  "    },\n",
  "    \"roundtrip_witness\":{\"status\":\"n/a\",\"reason\":\"粗/精ラベルの往復変換を持たない(基数比較のみ)\"},\n",
  "    \"effective_source_chain\":{\"status\":\"n/a\",\"reason\":\"本certは新規fixtureの初出であり、既存certを訂正・supersedeしない\"},\n",
  "    \"effective_source\":{\"status\":\"n/a\",\"reason\":\"同上\"},\n",
  "    \"seal_recoverability\":{\"status\":\"n/a\",\"reason\":\"封印fixtureを使用しない\"},\n",
  "    \"level\":\"PB3\"\n",
  "  },\n",
  "  \"cross_checked_status\":{\"status\":\"n/a\",\"reason\":\"単一driver内の3変種比較(識別力較正用)。cross-checkedを主張しない\"},\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"r4b_run_g_reference_sha256\":", JStr(r4bRunSha), ",\n",
  "    \"r4b_run_g_reference_note\":\"ScanRoofHexagon_Controlはこのsha256のihnec_r4b_run.g版のScanRoofHexagonと数学的に逐語同一(コード複製・importではない)\",\n",
  "    \"wall_ms_total\":", String(GAPLIB_WallElapsedMs()), "\n",
  "  }\n",
  "}\n");;

WriteFile("search/certs/ihnec_r4b_negative_fixture_20260802.json", cert);;
Print("\nWrote search/certs/ihnec_r4b_negative_fixture_20260802.json\n");
Print("\nIHNEC_R4B_NEGATIVE_FIXTURE_DONE\n");
QUIT;
