#############################################################################
## search/probe/w6_bu_s0/iso_gate_r3r4_driver.g
## ISO-GATE route-2 R3(mutant matrix, 8 件 -- M-ISO-7 は AS-GAP-3/S-BU-17 由来
## 追加委嘱、M-ISO-8 は裁定 535 ③ 新設)+ R4(第二系統への突合用データ出力)+
## interface 欄訂正(group_side / enumeration_domain / hom-fail 捕捉)。
##
## ★★ v2(裁定 535・2026-08-05): falsifier CV-9-2 判読
## (docs/notes/iso_r3r4_cv9_reading_v1.md)+ 数学者 auto_settled_check_v1.md
## 付録 A.2 の合成により、v1 の M-ISO-2/3/4/5/6b(5件)がスカラー層 mutation
## に堕していた欠陥・M-ISO-2 が ComputeVerdict の gate を手渡しで迂回していた
## 欠陥・settled:=true 固定変異体(M-ISO-8)が全走行を生存する欠陥を修理。
## IF-FIRST 凍結は docs/notes/iso_r3r4_iffirst_freeze_v1.md(再走前に起草)。
##
## 委嘱: 司令塔(2026-08-05)。正本: docs/notes/w6_bottomup_design_v4.md
##   §5.3(R3 mutant matrix)・§5.4(R4 第二系統)・§5.1(interface: P vs P-hat)・
##   §5.2(B-2 -- GroupHomomorphismByImages の fail 捕捉)。
##
## 旧 driver(search/probe/w6_bu_s0/iso_gate_check.g)は不改変。本ファイルは
## 別ファイル・別 cert(search/certs/w6_bu_s0_iso_gate_r3r4_20260805.json)。
## IsoGateCheck 等のロジックは旧 driver から逐語移植し、以下の 2 点のみ修理:
##   (1) isolated_verdict を shadow_sum_check にも gate させる(旧 driver は
##       shadow_sum_check を計算するだけで verdict 判定に使っていなかった --
##       M-ISO-5(候補欠落)の検出に必要な修理。ComputeVerdict として分離)。
##   (2) EnumerateReducedHexagon の theta/tau 構成 fail を Error() でなく
##       グレースフルに捕捉する local wrapper(EnumerateReducedHexagonSafe)を
##       追加(B-2 の⚠。共有 helper week3-battery-common.g 自体は無改変)。
##
## W-5 の格(UNKNOWN pending route-2 gate)は変更しない -- 本ファイルは route-2
## gate の R3/R4 要件の実装であって、発効判定(格上げ)はしない(司令塔検問+
## Sol ゲートの職掌)。
##
## 非接触宣言: Im_R/d_N/封印3量/u算術値は非接触。independence: certificates/*.json
## は読まない(全群は GAP で生成器から新規構築)。
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/week3-battery-common.g");;

Print("=== ISO-GATE route-2 R3(mutant matrix)+R4(第二系統データ出力)driver ===\n");
Print("(search/probe/w6_bu_s0/iso_gate_r3r4_driver.g -- 旧 driver 不改変・別 cert)\n\n");

#############################################################################
## 逐語移植(旧 driver と同一ロジック)
#############################################################################
MarkedDatumFromGroup := function(Ghat, xElt, yElt, cElt)
  local iso, Gperm;
  if IsPermGroup(Ghat) then
    return rec(x:=xElt, y:=yElt, c:=cElt, G:=Ghat);
  fi;
  iso := IsomorphismPermGroup(Ghat);
  Gperm := Image(iso);
  return rec(x:=Image(iso,xElt), y:=Image(iso,yElt), c:=Image(iso,cElt), G:=Gperm);
end;;

SettledCheckGeneral := function(qrec, shadows)
  local out, sh, m, u, f, targetX, targetY, hom, settled, settledCount;
  out := [];  settledCount := 0;
  for sh in shadows do
    m := sh.m;  u := 2*m+1;  f := sh.f;
    targetX := qrec.x^u;
    targetY := AbstractProd([f^-1, qrec.y^u, f]);
    hom := GroupHomomorphismByImages(qrec.G, qrec.G, [qrec.x, qrec.y], [targetX, targetY]);
    settled := (hom <> fail) and IsBijective(hom);
    if settled then settledCount := settledCount + 1; fi;
    Add(out, rec(m:=m, f_word:=sh.word, settled:=settled));
  od;
  return rec(detail:=out, settled_count:=settledCount, total:=Length(shadows));
end;;

CountByMGeneral := function(detailList, mVal)
  local totalM, settledM, sd;
  totalM := 0;  settledM := 0;
  for sd in detailList do
    if sd.m = mVal then
      totalM := totalM + 1;
      if sd.settled then settledM := settledM + 1; fi;
    fi;
  od;
  return rec(m:=mVal, total:=totalM, settled:=settledM);
end;;

#############################################################################
## ★修理(1): EnumerateReducedHexagon の theta/tau fail を Error() でなく
## グレースフルに捕捉する local wrapper。week3-battery-common.g 自体は無改変
## (共有ロジックへの影響ゼロ -- 他 script の挙動は変わらない)。
## B-2 の⚠(GroupHomomorphismByImages の fail 捕捉)にこの1点だけが該当する
## (theta/tau は EnumerateReducedHexagon 冒頭で構成され、失敗すれば以降の
## 全計算が無意味になるため、素通しの Error() だった。SettledCheckGeneral の
## hom(shadow ごとの T_{m,f})は元から hom<>fail を見て捕捉済みで無修理)。
#############################################################################
EnumerateReducedHexagonSafe := function(qrec, charmingSet)
  local G, zElt, thetaHom, tauHom, hexResult;
  G := qrec.G;
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  if thetaHom = fail or tauHom = fail then
    return rec(ok:=false, reason:="THETA_TAU_NOT_WELLDEFINED",
      detail:="quotient-shortcut precondition (theta: x->y,y->x / tau: x->y,y->z) does not extend to a well-defined endomorphism of this G -- caught gracefully, not Error()'d");
  fi;
  hexResult := EnumerateReducedHexagon(qrec, charmingSet);
  return rec(ok:=true, reason:="", result:=hexResult);
end;;

#############################################################################
## ★修理(2): ComputeVerdict -- shadow_sum_check を isolated_verdict の gate に
## 使う(旧 driver は shadow_sum_check を計算するだけで、verdict はそれを
## 見ずに settled.total/settled_count のみで決めていた -- 候補が静かに 1 件
## 欠落しても、残りが全部 settled なら TRUE を返してしまう穴があった。
## M-ISO-5(候補欠落)はこの穴を突く mutant で、本修理により UNKNOWN に落ちる
## ことを確認する)。
##
## ★★ v2 修理(裁定 535・falsifier CV-9-2 判読+数学者 auto_settled_check_v1.md
## 付録 A.2 の合成): 第 4 変数 allShadowsGenuine を追加(最優先 gate)。
## M-ISO-2(v2)が「shadow でない候補が shadow リストへ紛れ込んだ」ケースを
## 意味論的に正しく扱うには、settled=false と isolated=FALSE を混同しては
## ならない(数学者 A.2: 「h11-fail 候補に対する正しい挙動は shadow 段で除外
## /UNKNOWN であって非 settled(FALSE)ではない」)。⟹ 新設 stop code
## NONSHADOW_IN_DATUM を shadowSumOk より優先させ、非 shadow 混入を検出した
## ら常に UNKNOWN で止める(isolated=FALSE を偽って伝播させない)。
#############################################################################
ComputeVerdict := function(allShadowsGenuine, shadowSumOk, totalShadows, settledCount)
  if not allShadowsGenuine then
    return rec(verdict:="UNKNOWN", reason:="NONSHADOW_IN_DATUM");
  elif not shadowSumOk then
    return rec(verdict:="UNKNOWN", reason:="CANDIDATE_ENUM_INCONSISTENT");
  elif totalShadows = 0 then
    return rec(verdict:="UNKNOWN", reason:="NO_SHADOWS");
  elif settledCount = totalShadows then
    return rec(verdict:="TRUE", reason:="");
  else
    return rec(verdict:="FALSE", reason:="");
  fi;
end;;

#############################################################################
## ★新設(v2・裁定 535): VerifyShadowsGenuine -- 与えられた shadow リストの
## 各元が実際に hexagon(3.10)(3.11)+SURJ を満たすことを独立に再検査する。
## 通常の実測 fixture(EnumerateReducedHexagon が自分で列挙した shadows)では
## 常に true になる(冗長だが無害)。M-ISO-2(v2)のように shadow リストを
## 手で組み立てる場面でのみ、真に意味のある gate として働く。
#############################################################################
VerifyShadowsGenuine := function(qrec, shadowList)
  local zElt, thetaHom, tauHom, sh, m, u, f, thetaf, hex310, ymf, tauymf, tau2ymf, hex311, genA, genB, surj;
  if Length(shadowList) = 0 then return true; fi;
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(qrec.G, qrec.G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(qrec.G, qrec.G, [qrec.x, qrec.y], [qrec.y, zElt]);
  if thetaHom = fail or tauHom = fail then return false; fi;
  for sh in shadowList do
    m := sh.m;  u := 2*m+1;  f := sh.f;
    thetaf := Image(thetaHom, f);
    hex310 := AbstractProd([f, thetaf]) = Identity(qrec.G);
    if not hex310 then return false; fi;
    ymf := AbstractProd([qrec.y^m, f]);
    tauymf := Image(tauHom, ymf);
    tau2ymf := Image(tauHom, tauymf);
    hex311 := AbstractProd([tau2ymf, tauymf, ymf]) = Identity(qrec.G);
    if not hex311 then return false; fi;
    genA := qrec.x^u;
    genB := AbstractProd([f^-1, qrec.y^u, f]);
    surj := Size(Group(genA, genB)) = Size(qrec.G);
    if not surj then return false; fi;
  od;
  return true;
end;;

#############################################################################
## IsoGateCheck(修理(1)(2)を組み込み、group_side/enumeration_domain 欄を追加)
#############################################################################
IsoGateCheck := function(qrec, label, kerIsKn)
  local precheck, nOrd, charmingSet, t0, t1, hexSafe, hexResult, shadowSumOk, allGenuine,
        tSettled, settled, settledByM, verdictRec, isoGateState, timeHex, timeSettled;
  precheck := (qrec.c = Identity(qrec.G));
  if not precheck then
    return rec(label:=label, kerIsKn:=kerIsKn, precondition_ok:=false,
      g_size:=Size(qrec.G), n_ord:=fail, charming_set:=[], charming_set_size:=0,
      hexagon:=fail, settled:=fail, settled_by_m:=[],
      isolated_verdict:="UNKNOWN", unknown_reason:="C_NOT_IN_N",
      iso_gate_state:="UNKNOWN", time_ms_hexagon:=0, time_ms_settled:=0,
      group_side:="P (=PB3/N, per w6_bottomup_design_v4.md sec.5.1)",
      enumeration_domain:="group_elements");
  fi;

  nOrd := Lcm(Order(qrec.x), Order(qrec.y));
  charmingSet := Filtered([0..nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);

  t0 := Runtime();;
  hexSafe := EnumerateReducedHexagonSafe(qrec, charmingSet);;
  t1 := Runtime();;
  timeHex := t1 - t0;

  if not hexSafe.ok then
    return rec(label:=label, kerIsKn:=kerIsKn, precondition_ok:=true,
      g_size:=Size(qrec.G), n_ord:=nOrd, charming_set:=charmingSet,
      charming_set_size:=Length(charmingSet), hexagon:=fail, settled:=fail, settled_by_m:=[],
      isolated_verdict:="UNKNOWN", unknown_reason:=hexSafe.reason,
      iso_gate_state:="UNKNOWN", time_ms_hexagon:=timeHex, time_ms_settled:=0,
      group_side:="P (=PB3/N, per w6_bottomup_design_v4.md sec.5.1)",
      enumeration_domain:="group_elements");
  fi;
  hexResult := hexSafe.result;

  shadowSumOk := (hexResult.candidate_total - hexResult.h10_fail - hexResult.h11_fail
                  - hexResult.generation_fail = hexResult.shadow_total);

  t0 := Runtime();;
  settled := SettledCheckGeneral(qrec, hexResult.shadows);;
  t1 := Runtime();;
  timeSettled := t1 - t0;

  settledByM := List(charmingSet, mVal -> CountByMGeneral(settled.detail, mVal));

  # v2: genuineness gate (see VerifyShadowsGenuine). For a normal fixture whose
  # shadows come straight from EnumerateReducedHexagon this is always true
  # (redundant but harmless); it only bites when a shadow list is hand-built
  # (M-ISO-2 v2 below).
  allGenuine := VerifyShadowsGenuine(qrec, hexResult.shadows);;

  verdictRec := ComputeVerdict(allGenuine, shadowSumOk, settled.total, settled.settled_count);;

  if kerIsKn <> fail then
    isoGateState := "PROVEN";
  else
    isoGateState := "UNKNOWN (pending commander/Sol gate on driver-TRUE as ISO-GATE route (2))";
  fi;

  return rec(label:=label, kerIsKn:=kerIsKn, precondition_ok:=true,
    g_size:=Size(qrec.G), n_ord:=nOrd, charming_set:=charmingSet,
    charming_set_size:=Length(charmingSet),
    hexagon:=hexResult, shadow_sum_check:=shadowSumOk, all_shadows_genuine:=allGenuine,
    settled:=settled, settled_by_m:=settledByM,
    isolated_verdict:=verdictRec.verdict, unknown_reason:=verdictRec.reason,
    iso_gate_state:=isoGateState,
    time_ms_hexagon:=timeHex, time_ms_settled:=timeSettled,
    group_side:="P (=PB3/N, per w6_bottomup_design_v4.md sec.5.1)",
    enumeration_domain:="group_elements");
end;;

#############################################################################
## FIXTURE 1: K^(3)(M-ISO-1 -- 既知 isolated 陽性、健全性ベース)
#############################################################################
Print("--- FIXTURE 1: K^(3) (M-ISO-1: 既知 isolated 陽性) ---\n");
gn3 := MakeGn(3);;
datum3 := MarkedDatumFromGroup(gn3.G, gn3.x, gn3.y, ());;
res3 := IsoGateCheck(datum3, "M-ISO-1-K3", 3);;
Print("|G3|=", res3.g_size, " (P-side; P-hat-side would be ", 6*res3.g_size, ")  N_ord=", res3.n_ord,
      "  shadow_total=", res3.hexagon.shadow_total, "  settled=", res3.settled.settled_count, "/",
      res3.settled.total, "  verdict=", res3.isolated_verdict, "\n");
mIso1Ok := (res3.g_size = 108) and (res3.hexagon.shadow_total = 12) and (res3.settled.total = 12)
           and (res3.settled.settled_count = 12) and (res3.isolated_verdict = "TRUE");;
Print("[", PF(mIso1Ok), "] M-ISO-1 fired as TRUE (expected TRUE -- basic sanity)\n\n");

#############################################################################
## FIXTURE 2: W-5(interface 確認用 -- group_side 欄・648/6000 対応注記)
#############################################################################
Print("--- FIXTURE 2: W-5 (interface: group_side 確認、P/P-hat 対応の注記) ---\n");
gn5 := MakeGn(5);;
q8rec := MakeQ8();;
xhat5 := PermList(Concatenation(List([1..15], j -> j^gn5.x), List([1..8], j -> 15 + (j^q8rec.x))));;
yhat5 := PermList(Concatenation(List([1..15], j -> j^gn5.y), List([1..8], j -> 15 + (j^q8rec.y))));;
QW5 := Group(xhat5, yhat5);;
datum5 := MarkedDatumFromGroup(QW5, xhat5, yhat5, ());;
res5 := IsoGateCheck(datum5, "W-5-interface-check", fail);;
Print("|PB3/N|=", res5.g_size, " (P-side, 裁定473: expect 1000; P-hat-side would be ", 6*res5.g_size,
      " -- per design v4 sec.5.1 this matches the documented 1000/6000 correspondence)\n");
Print("verdict=", res5.isolated_verdict, "  iso_gate_state=", res5.iso_gate_state,
      "  (W-5 stays UNKNOWN pending route-2 gate -- not upgraded by this driver)\n\n");
interfaceCheckOk := (res5.g_size = 1000) and (6*res5.g_size = 6000) and (res5.iso_gate_state{[1..7]} = "UNKNOWN");;
Print("[", PF(interfaceCheckOk), "] interface group_side note fires (1000 P-side / 6000 P-hat-side documented; W-5 iso_gate_state stays UNKNOWN)\n\n");

#############################################################################
## FIXTURE 3: N5-control -- M-ISO-6(a): c NOT IN N -> UNKNOWN(C_NOT_IN_N)
## (既済 fixture の再確認 -- 逐語再構成、旧 driver と同一ロジック)
#############################################################################
Print("--- FIXTURE 3: N5-control -- M-ISO-6(a): c NOT IN N (既済 fixture 再確認) ---\n");
q5gen := PermList(Concatenation([2..5],[1]));;
Q5 := Group(q5gen);;
qtN5 := BuildQTGeneral(Q5, q5gen^2, q5gen^2, q5gen);;
XXn5 := qtN5.s1^2;;
YYn5 := qtN5.s2^2;;
CCn5 := (qtN5.s1*qtN5.s2*qtN5.s1)^2;;
GN5 := Group(qtN5.s1, qtN5.s2);;
datumN5 := MarkedDatumFromGroup(GN5, XXn5, YYn5, CCn5);;
resN5 := IsoGateCheck(datumN5, "M-ISO-6a-N5control", fail);;
Print("precondition_ok=", resN5.precondition_ok, "  verdict=", resN5.isolated_verdict,
      "  unknown_reason=", resN5.unknown_reason, "\n");
mIso6aOk := (not resN5.precondition_ok) and (resN5.isolated_verdict = "UNKNOWN")
            and (resN5.unknown_reason = "C_NOT_IN_N");;
Print("[", PF(mIso6aOk), "] M-ISO-6(a) fired as UNKNOWN(C_NOT_IN_N) (c NOT IN N precondition-gate branch)\n\n");

#############################################################################
## FIXTURE 4: Q3-a -- theta/tau does not extend (B-2 の hom-fail グレースフル
## 捕捉の実発火。scratchpad/explore_m2_negative.g の探索で見つかった実在ケース
## -- c IN N だが quotient-shortcut 前提(theta/tau の well-definedness)が
## 壊れる自然な窓。旧 driver ならここで Error() が飛んで走行全体が落ちていた;
## 本 driver は EnumerateReducedHexagonSafe で捕捉し UNKNOWN を返す)
#############################################################################
Print("--- FIXTURE 4: Q3-a (BuildQTGeneral, Q=C3) -- B-2 hom-fail グレースフル捕捉 ---\n");
q3gen := PermList([2,3,1]);;
Q3grp := Group(q3gen);;
qtQ3a := BuildQTGeneral(Q3grp, q3gen, q3gen, ());;
Xq3a := qtQ3a.s1^2;;  Yq3a := qtQ3a.s2^2;;  Cq3a := (qtQ3a.s1*qtQ3a.s2*qtQ3a.s1)^2;;
Gq3a := Group(qtQ3a.s1, qtQ3a.s2);;
datumQ3a := MarkedDatumFromGroup(Gq3a, Xq3a, Yq3a, Cq3a);;
Print("c = Identity(G)? ", datumQ3a.c = Identity(datumQ3a.G), "  (expect true -- c IS in N here)\n");
resQ3a := IsoGateCheck(datumQ3a, "HOMFAIL-Q3a", fail);;
Print("precondition_ok=", resQ3a.precondition_ok, "  verdict=", resQ3a.isolated_verdict,
      "  unknown_reason=", resQ3a.unknown_reason, "\n");
homFailCaptureOk := resQ3a.precondition_ok and (Cq3a = Identity(Gq3a))
                    and (resQ3a.isolated_verdict = "UNKNOWN")
                    and (resQ3a.unknown_reason = "THETA_TAU_NOT_WELLDEFINED");;
Print("[", PF(homFailCaptureOk), "] B-2 hom-fail capture fires gracefully (UNKNOWN(THETA_TAU_NOT_WELLDEFINED), no Error() crash) on a genuine c_in_N window where quotient-shortcut precondition fails\n\n");

#############################################################################
## ★★ v2(裁定 535): M-ISO-2/3/4/5/6(b)/8 -- 経路層 mutation へ復元
## (falsifier 判読 docs/notes/iso_r3r4_cv9_reading_v1.md 【重大 2】【重大 3】
##  §4 + 数学者 auto_settled_check_v1.md 付録 A.2 の合成)。
##
## v1 の欠陥(falsifier 実証・数学者裁定): (a) M-ISO-2 は ComputeVerdict の
## 第 1 引数へ手で true を渡し shadow_sum_check を迂回していた(自己矛盾:
## M-ISO-5 と同型の摂動に対し違う扱い) (b) h11-fail 候補は Def 3.7 により
## そもそも GT-shadow でないので、これを「非 settled」として isolated=FALSE
## へ読ませると false-FALSE の経路になる (c) 2/3/4/5/6b の 5 件がすべて
## ComputeVerdict という 10 行の純関数だけを叩くスカラー層の変異になっていた
## (v4 §5.3 の事前登録は shadow 差し替え/列挙落としという経路層の変異)。
##
## 本節の修理: witness を「h11_fail バケツから shadow バケツへ移す」構成へ
## 変更(スカラー手渡しなし)。SettledCheckGeneral の実経路を通し、
## VerifyShadowsGenuine で独立に非 shadow 性を検出させ、
## ComputeVerdict の新 gate(allShadowsGenuine)により
## UNKNOWN(NONSHADOW_IN_DATUM) を返させる(FALSE ではない)。
#############################################################################
Print("--- M-ISO-2(v2)/3/4/5/6(b)/8: 経路層 mutation matrix (real function calls on real data) ---\n");

Print("K^(3) generation_fail count = ", res3.hexagon.generation_fail,
      "  (h10_fail=", res3.hexagon.h10_fail, " h11_fail=", res3.hexagon.h11_fail, ")\n");
Print("  (generation_fail=0 -- an empirical structural fact, logged for the mathematician;\n");
Print("   see auto_settled_check_v1.md Prop GEN-AB for a candidate explanation. Since no\n");
Print("   candidate ever fails SURJ here, the witness must come from the h11_fail bucket --\n");
Print("   which per Def 3.7 is NOT a GT-shadow. This is exactly the point of the v2\n");
Print("   NONSHADOW_IN_DATUM construction below: it tests whether the pipeline correctly\n");
Print("   refuses to launder a non-shadow into an isolated=FALSE claim.)\n");

## witness: 実列挙の h11_fail 候補を 1 件取得(逐語出自は v1 と同じ、witness
## 自体の同定に変更はない -- falsifier が本物と確認済み)
## 探すのは h11_fail 候補のうち像が真部分群になるもの(settled=false が
## element-level で real に発火するもの)。h11_fail というだけでは
## VerifyShadowsGenuine は必ず false を返す(hex311 の再検査は分類と一致する
## ので自動的に一致)が、SettledCheckGeneral の settled 値は真部分群を生成
## する候補でなければ (falsifier 【重大3】が指摘した通り)「たまたま生成して
## しまい settled=true になる」ケースがあり得る(GEN-AB の帰結: generation
## はほぼ常に成立する)。ゆえに像の真部分群性で絞る -- 既に v1 で発見済みの
## m=0, f_word=[y,x,y,x](像位数36)がこの条件を満たす。
FindH11FailWitness := function(hexResult, qrec)
  local cand, m, u, f, genA, genB, sz;
  for cand in hexResult.generation_detail do
    if cand.stage = "h11_fail" then
      m := cand.m;  u := 2*m+1;
      f := EvalWordInQ(cand.f_word, qrec.x, qrec.y, Identity(qrec.G));
      genA := qrec.x^u;
      genB := AbstractProd([f^-1, qrec.y^u, f]);
      sz := Size(Group(genA, genB));
      if sz < Size(qrec.G) then
        return rec(found:=true, m:=m, f_word:=cand.f_word, f_elt:=f, subgroup_size:=sz, stage:=cand.stage);
      fi;
    fi;
  od;
  return rec(found:=false);
end;;
witnessSearch := FindH11FailWitness(res3.hexagon, datum3);;
if not witnessSearch.found then
  Error("M-ISO-2(v2): no h11_fail candidate found in K^(3) -- cannot construct fixture");
fi;
witnessSourceLabel := "K^(3)";;
witnessM := witnessSearch.m;;
witnessWord := witnessSearch.f_word;;
witnessFElt := witnessSearch.f_elt;;
witnessNPoints := 9;;
witnessSubgroupSize := witnessSearch.subgroup_size;;
Print("M-ISO-2(v2) witness: m=", witnessM, " f_word=", witnessWord, " stage=", witnessSearch.stage,
      "  |<genA,genB>|=", witnessSubgroupSize, " (< |G|=", res3.g_size, "? ", witnessSubgroupSize < res3.g_size, ")\n");

## ★ 経路層の核心: witness を h11_fail バケツから shadow バケツへ実際に移す
## (h11_fail: 24->23, shadow_total: 12->13)。SettledCheckGeneral(実関数)へ
## 実際に通す -- カウンタだけを弄らない。
witnessShadowRec := rec(m:=witnessM, f:=witnessFElt, word:=witnessWord);;
mIso2Shadows := Concatenation(res3.hexagon.shadows, [witnessShadowRec]);;   # 12 real + 1 witness = 13
mIso2SettledResult := SettledCheckGeneral(datum3, mIso2Shadows);;            # ★ 実経路(hom+IsBijective)
mIso2H11Fail := res3.hexagon.h11_fail - 1;;    # 24 -> 23 (witness moved OUT of h11_fail)
mIso2ShadowTotal := res3.hexagon.shadow_total + 1;;  # 12 -> 13 (witness moved INTO shadow bucket)
mIso2ShadowSumOk := (res3.hexagon.candidate_total - res3.hexagon.h10_fail - mIso2H11Fail
                     - res3.hexagon.generation_fail = mIso2ShadowTotal);;    # 108-72-23-0 =?= 13
mIso2AllGenuine := VerifyShadowsGenuine(datum3, mIso2Shadows);;              # ★ 独立の非 shadow 検出
mIso2Verdict := ComputeVerdict(mIso2AllGenuine, mIso2ShadowSumOk, mIso2SettledResult.total, mIso2SettledResult.settled_count);;
witnessSettledEntry := First(mIso2SettledResult.detail, d -> d.m = witnessM and d.f_word = witnessWord);;
Print("M-ISO-2(v2): h11_fail 24->", mIso2H11Fail, "  shadow_total 12->", mIso2ShadowTotal,
      "  identity check: 108-72-", mIso2H11Fail, "-0=", mIso2ShadowTotal, "? ", mIso2ShadowSumOk, "\n");
Print("  SettledCheckGeneral (real path) on 13-element list: settled=", mIso2SettledResult.settled_count,
      "/", mIso2SettledResult.total, "  witness settled=", witnessSettledEntry.settled, " (expect false)\n");
## ★v2.1【軽微G】(falsifier iso_r3r4_cv9_reading_v2.md §④): VerifyShadowsGenuine
## は列挙器(EnumerateReducedHexagon)と同一の式で hex310/hex311/SURJ を
## 再計算する。witness は列挙器自身が h11_fail に分類した元なので、
## この再検査が false を返すことは構成上保証されている(発見ではなく定義)。
## 情報量があるのは witness_settled=false と恒等式 108-72-23-0=13 の方であり、
## all_genuine=false 自体は「独立の検出」と読ませない。
Print("  VerifyShadowsGenuine (same formula as the enumerator -- structurally GUARANTEED false here, not an independent discovery; see comment above): all_genuine=", mIso2AllGenuine, " (expect false -- witness was classified h11_fail by the enumerator itself)\n");
Print("  ComputeVerdict = ", mIso2Verdict.verdict, "/", mIso2Verdict.reason, " (expect UNKNOWN/NONSHADOW_IN_DATUM, NOT FALSE)\n");
mIso2Ok := (mIso2Verdict.verdict = "UNKNOWN") and (mIso2Verdict.reason = "NONSHADOW_IN_DATUM")
           and (mIso2ShadowSumOk = true) and (mIso2H11Fail = 23) and (mIso2ShadowTotal = 13)
           and (witnessSettledEntry.settled = false) and (mIso2SettledResult.settled_count = 12)
           and (mIso2SettledResult.total = 13);;
Print("[", PF(mIso2Ok), "] M-ISO-2(v2) fired as UNKNOWN(NONSHADOW_IN_DATUM) -- tests whether the pipeline refuses to launder a non-shadow candidate into isolated=FALSE; NOT a claim that isolated=FALSE has a real witness (AS-GAP-6 remains open, out of scope)\n\n");

# M-ISO-3: constant-TRUE mutant, now a REAL function call (not a string
# literal) run on the SAME real 4-argument input ComputeVerdict receives for
# M-ISO-2(v2).
MutantConstantTrueVerdict := function(allGen, sumOk, tot, settled)
  return rec(verdict:="TRUE", reason:="");
end;;
mIso3MutantResult := MutantConstantTrueVerdict(mIso2AllGenuine, mIso2ShadowSumOk, mIso2SettledResult.total, mIso2SettledResult.settled_count);;
mIso3Detected := (mIso3MutantResult.verdict <> mIso2Verdict.verdict);;
Print("M-ISO-3: constant-TRUE mutant function says '", mIso3MutantResult.verdict, "' on the M-ISO-2(v2) real inputs; real ComputeVerdict says '",
      mIso2Verdict.verdict, "' -- mismatch detected? ", mIso3Detected, "\n");
Print("[", PF(mIso3Detected), "] M-ISO-3 constant-TRUE mutant is KILLED (mismatch detected)\n\n");

# M-ISO-4: settled 1-flip, restored to the DATA layer. Take the REAL K^(3)
# settled.detail list (12 records, all settled=true), flip exactly ONE
# record's settled field, then RECOUNT by actually enumerating the modified
# list (Number(...)), not by scalar arithmetic.
flippedDetail := ShallowCopy(res3.settled.detail);;
flippedDetail[1] := rec(m:=flippedDetail[1].m, f_word:=flippedDetail[1].f_word, settled:=false);;
flippedSettledCount := Number(flippedDetail, x -> x.settled);;
mIso4AllGenuine := VerifyShadowsGenuine(datum3, res3.hexagon.shadows);;  # unaffected -- same real shadow set
## ★v2.1【軽微C】: shadowSumOk はリテラル true でなく res3.shadow_sum_check(実計算値)を渡す
## (settled のフリップは shadow の集合そのものを変えないので数値上は不変・12 のまま true だが、
## anti-pattern を排すため手渡しをやめる)。
mIso4Verdict := ComputeVerdict(mIso4AllGenuine, res3.shadow_sum_check, Length(flippedDetail), flippedSettledCount);;
Print("M-ISO-4: K^(3) settled.detail (real list) with entry 1 flipped, recounted via Number() -> ",
      flippedSettledCount, "/", Length(flippedDetail), " -> verdict=", mIso4Verdict.verdict, "\n");
mIso4Ok := (mIso4Verdict.verdict = "FALSE") and (flippedSettledCount = 11);;
Print("[", PF(mIso4Ok), "] M-ISO-4 fired as FALSE (data-layer settled-flip, real recount)\n\n");

# M-ISO-5: candidate drop, restored to the DATA layer. Take the REAL K^(3)
# hexagon.shadows list (12 records) and literally drop element 1 (list
# slicing), then run the REAL SettledCheckGeneral on the shortened list.
droppedShadows := res3.hexagon.shadows{[2..Length(res3.hexagon.shadows)]};;   # 11 elements, real list slice
droppedSettled := SettledCheckGeneral(datum3, droppedShadows);;               # ★ real function call
droppedAllGenuine := VerifyShadowsGenuine(datum3, droppedShadows);;           # still all genuine (just fewer)
droppedShadowSumOk := (res3.hexagon.candidate_total - res3.hexagon.h10_fail - res3.hexagon.h11_fail
                        - res3.hexagon.generation_fail = Length(droppedShadows));;  # 108-72-24-0=12 =?= 11 -> false
mIso5Verdict := ComputeVerdict(droppedAllGenuine, droppedShadowSumOk, droppedSettled.total, droppedSettled.settled_count);;
Print("M-ISO-5: K^(3) hexagon.shadows (real list, 12 elts) with element 1 dropped -> 11 elts, ",
      "SettledCheckGeneral (real) = ", droppedSettled.settled_count, "/", droppedSettled.total,
      "  shadow_sum_check=", droppedShadowSumOk, " (expect false: 12<>11) -> verdict=", mIso5Verdict.verdict, "/", mIso5Verdict.reason, "\n");
mIso5Ok := (mIso5Verdict.verdict = "UNKNOWN") and (mIso5Verdict.reason = "CANDIDATE_ENUM_INCONSISTENT");;
Print("[", PF(mIso5Ok), "] M-ISO-5 fired as UNKNOWN(CANDIDATE_ENUM_INCONSISTENT), NOT TRUE (data-layer drop via real list slice + real SettledCheckGeneral call)\n\n");

# M-ISO-6(b): zero-shadow, restored to the DATA layer. Run the REAL
# SettledCheckGeneral on an actual empty list (not a hardcoded scalar 0).
emptyShadows := [];;
emptySettled := SettledCheckGeneral(datum3, emptyShadows);;   # real call, loop body never executes
emptyAllGenuine := VerifyShadowsGenuine(datum3, emptyShadows);;  # vacuously true
## ★v2.1【軽微C】: shadowSumOk もリテラル true でなく実計算(candidate_total=h10=h11=genfail=0
## の自己無矛盾シナリオを明示的に組み立てて恒等式を計算する)。
emptyCandidateTotal := 0;;  emptyH10Fail := 0;;  emptyH11Fail := 0;;  emptyGenFail := 0;;
emptyShadowSumOk := (emptyCandidateTotal - emptyH10Fail - emptyH11Fail - emptyGenFail = emptySettled.total);;
mIso6bVerdict := ComputeVerdict(emptyAllGenuine, emptyShadowSumOk, emptySettled.total, emptySettled.settled_count);;
Print("M-ISO-6(b): SettledCheckGeneral([]) (real call on an actual empty list) -> total=",
      emptySettled.total, " settled=", emptySettled.settled_count, " -> verdict=", mIso6bVerdict.verdict, "/", mIso6bVerdict.reason, "\n");
mIso6bOk := (mIso6bVerdict.verdict = "UNKNOWN") and (mIso6bVerdict.reason = "NO_SHADOWS")
            and (emptySettled.total = 0);;
Print("[", PF(mIso6bOk), "] M-ISO-6(b) fired as UNKNOWN(NO_SHADOWS) (real SettledCheckGeneral([]) call, not a scalar constant)\n\n");

#############################################################################
## ★★ v2.1 修理【要修正A】(裁定543・falsifier 再判読 iso_r3r4_cv9_reading_v2.md
## §③(c)): M-ISO-8 の検出機構を verdict 比較から detail 要素比較へ変更。
## falsifier の機械確認: ComputeVerdict(allGenuine=false, sumOk=true, 13, 12)
## と ComputeVerdict(allGenuine=false, sumOk=true, 13, 13) はどちらも
## UNKNOWN/NONSHADOW_IN_DATUM を返す -- M-ISO-2(v2) の datum 上では実 verdict
## は settled 変異に完全に不感(NONSHADOW gate が支配的)。旧版の
## mIso8Detected(naive verdict TRUE vs real verdict UNKNOWN)は実は
## 「genuineness gate の有無」を比較していただけで、settled チャネルを
## 直接叩いていなかった(M-ISO-3 と実質重複)。
## ★ 修理: settled チャネルを直接叩く detail 要素比較にする --
## 実 SettledCheckGeneral の witness エントリ(settled=false)と
## 変異後 MutantSettledAlwaysTrue の witness エントリ(settled=true)を
## 突合し、この食い違いそのものを検出とする(kills 欄もこれに合わせて訂正)。
#############################################################################
Print("--- M-ISO-8: settled:=true 固定変異体(detail 要素比較で settled チャネルを直接検査) ---\n");
MutantSettledAlwaysTrue := function(qrec, shadowList)
  local out, sh;
  out := [];
  for sh in shadowList do
    Add(out, rec(m:=sh.m, f_word:=sh.word, settled:=true));
  od;
  return rec(detail:=out, settled_count:=Length(shadowList), total:=Length(shadowList));
end;;
mIso8MutantSettled := MutantSettledAlwaysTrue(datum3, mIso2Shadows);;   # runs on the SAME 13-elt datum as M-ISO-2(v2)
mIso8WitnessMutantEntry := First(mIso8MutantSettled.detail, d -> d.m = witnessM and d.f_word = witnessWord);;
# ★ the actual kill: real detail says witness settled=false, mutant detail says witness settled=true
mIso8Detected := (witnessSettledEntry.settled <> mIso8WitnessMutantEntry.settled);;
Print("M-ISO-8: settled:=true mutant on M-ISO-2(v2)'s 13-elt datum -> mutant settled_count=",
      mIso8MutantSettled.settled_count, "/", mIso8MutantSettled.total, "\n");
Print("  real detail: witness settled=", witnessSettledEntry.settled,
      "   mutant detail: witness settled=", mIso8WitnessMutantEntry.settled,
      "   mismatch (settled channel struck directly)? ", mIso8Detected, "\n");
Print("  (note, per falsifier: the verdict itself is INSENSITIVE to this mutation on this datum --\n");
Print("   both ComputeVerdict(allGenuine=false, sumOk=true, 13, 12) and (..., 13, 13) return\n");
Print("   UNKNOWN/NONSHADOW_IN_DATUM, since the genuineness gate dominates. The kill is at the\n");
Print("   detail-element level, i.e. this is M-ISO-2(v2)'s own assertion on witnessSettledEntry.settled,\n");
Print("   not a property of M-ISO-8's verdict comparison.)\n");
mIso8Ok := mIso8Detected and (witnessSettledEntry.settled = false) and (mIso8WitnessMutantEntry.settled = true)
           and (mIso2SettledResult.settled_count = 12) and (mIso8MutantSettled.settled_count = 13);;
Print("[", PF(mIso8Ok), "] M-ISO-8 fired: detail-level comparison catches the settled:=true mutant (witness entry false->true), independent of verdict (which is dominated by the NONSHADOW gate on this datum)\n\n");

#############################################################################
## M-ISO-7(司令塔 2026-08-05 追加委嘱、docs/notes/auto_settled_check_v1.md
## 【AS-GAP-3】+ R1-b + S-BU-17): descent フィルタ混入検出 -- source-map 方式。
##
## 【AS-GAP-3】の確認結果(このファイル自身の設計に対する自己監査):
##   EnumerateReducedHexagon(search/week3-battery-common.g)の候補選定ループ
##   (「for cand in Dwords do」以降、shadows へ Add するまでの本体)は
##   hex310/hex311(theta/tau は関数冒頭で1回だけ構成 -- hexagon の
##   well-definedness 用、個々の shadow の descent とは別物)と
##   surj:=Size(Group(genA,genB))=Size(G) だけを見ており、
##   GroupHomomorphismByImages/IsBijective(= descent/K5-8 判定)を
##   一切呼んでいない。descent 判定は SettledCheckGeneral(本ファイル・
##   hexResult.shadows を読むだけの下流関数)でのみ行われ、列挙結果
##   (shadow_total)を変更しない。⟹ 本 driver の列挙は R1-b 適合(汚染なし)。
##   以下は、この自己監査結果を機械的にも裏付ける source-map 検出器と、
##   「もし汚染していたら検出できるか」を示す否定的対照(意図的に汚染した
##   ダミー実装)のペア。
#############################################################################
Print("--- M-ISO-7: descent フィルタ混入検出(source-map)+ AS-GAP-3 自己監査 ---\n");

ExtractFunctionBody := function(sourceText, funcName)
  local startMk, startPos, rest, depth, i, endPos;
  startMk := Concatenation(funcName, " := function");
  startPos := FindPositionFrom(sourceText, startMk, 1);
  if startPos = fail then return fail; fi;
  # naive but sufficient here: find the matching "end;;" by counting
  # function/end pairs is overkill for our purpose -- EnumerateReducedHexagon
  # is a single top-level function with no nested function(...) blocks, so the
  # FIRST "end;;" after start is its own end.
  endPos := FindPositionFrom(sourceText, "end;;", startPos);
  if endPos = fail then return fail; fi;
  return sourceText{[startPos..endPos+4]};
end;;

CheckEnumerationContamination := function(funcBodyText, label)
  local loopStart, decisionZone, contaminated;
  loopStart := FindPositionFrom(funcBodyText, "for cand in Dwords do", 1);
  if loopStart = fail then
    return rec(label:=label, checked:=false, reason:="could not locate per-candidate loop in source");
  fi;
  decisionZone := funcBodyText{[loopStart..Length(funcBodyText)]};
  contaminated := (FindPositionFrom(decisionZone, "GroupHomomorphismByImages", 1) <> fail)
                  or (FindPositionFrom(decisionZone, "IsBijective", 1) <> fail);
  return rec(label:=label, checked:=true, contaminated:=contaminated);
end;;

# (a) real driver's actual enumerator -- self-audit
commonSrcStream := InputTextFile("search/week3-battery-common.g");;
commonSrcText := ReadAll(commonSrcStream);;
CloseStream(commonSrcStream);;
enumBody := ExtractFunctionBody(commonSrcText, "EnumerateReducedHexagon");;
realCheck := CheckEnumerationContamination(enumBody, "EnumerateReducedHexagon (real, search/week3-battery-common.g)");;
Print("AS-GAP-3 self-audit: ", realCheck.label, " -- contaminated=", realCheck.contaminated,
      " (expect false: descent/K5-8 check is NOT used as an enumeration filter here;\n");
Print("  GroupHomomorphismByImages IS called earlier in the SAME function for theta/tau\n");
Print("  (hexagon well-definedness, a fixed x<->y / x->y,y->z substitution, NOT the shadow's\n");
Print("  own (m,f)-specific descent) -- that call is OUTSIDE the 'for cand in Dwords do' loop\n");
Print("  scanned here, so it correctly does not trigger this detector)\n");
asGap3Ok := realCheck.checked and (not realCheck.contaminated);;
Print("[", PF(asGap3Ok), "] AS-GAP-3 CONFIRMED CLEAN: this driver's enumeration does NOT filter shadows by descent (settled=100% on K^(3)/W-5 is explained by sample bias -- known-isolated Dn-tower families per Thm 4.3/Prop 3.14 -- NOT by constant-TRUE contamination)\n\n");

# (b) negative control: a DELIBERATELY contaminated mutant enumerator body
# (never executed as real GAP code -- pure text, used only to prove the
# detector actually discriminates). Mirrors a plausible bug: filtering
# shadows by requiring the descent hom to succeed INSIDE the per-candidate
# loop, before Add(shadows, ...).
contaminatedMutantBody := Concatenation(
  "MutantContaminatedEnumerator := function(qrec, charmingSet)\n",
  "  for cand in Dwords do\n",
  "    for m in charmingSet do\n",
  "      # BUG: descent check used as an enumeration FILTER (K5-8 misuse)\n",
  "      hom := GroupHomomorphismByImages(qrec.G, qrec.G, [qrec.x, qrec.y], [genA, genB]);\n",
  "      if hom <> fail and IsBijective(hom) then\n",
  "        Add(shadows, rec(m:=m, f:=f));\n",
  "      fi;\n",
  "    od;\n",
  "  od;\n",
  "end;;");;
mutantCheck := CheckEnumerationContamination(contaminatedMutantBody, "MutantContaminatedEnumerator (deliberately broken, text-only, never executed)");;
Print("M-ISO-7 negative control: ", mutantCheck.label, " -- contaminated=", mutantCheck.contaminated, " (expect true)\n");
sBu17Verdict := (function() if mutantCheck.contaminated then return "ENUMERATION_FILTER_CONTAMINATION / STOP"; else return "PASS"; fi; end)();;
Print("  S-BU-17 verdict on this mutant: ", sBu17Verdict, "\n");
mIso7Ok := mutantCheck.checked and mutantCheck.contaminated and (sBu17Verdict = "ENUMERATION_FILTER_CONTAMINATION / STOP");;
Print("[", PF(mIso7Ok), "] M-ISO-7 fired: source-map detector correctly flags a deliberately-contaminated enumerator as ENUMERATION_FILTER_CONTAMINATION/STOP, while clearing the real driver (AS-GAP-3)\n\n");

allMutantsOk := mIso1Ok and mIso2Ok and mIso3Detected and mIso4Ok and mIso5Ok and mIso6aOk and mIso6bOk
                and mIso7Ok and mIso8Ok and asGap3Ok and homFailCaptureOk and interfaceCheckOk;;
Print("[", PF(allMutantsOk), "] ALL R3 MUTANTS (8) + AS-GAP-3 self-audit + interface checks FIRED AS EXPECTED\n\n");

#############################################################################
## R4 データ出力: 第二系統(独立 Python 実装)への入力データ(生成元の
## permutation 像のみ -- GAP コード・中間結果は一切含めない。第二系統はこの
## データから群演算・BFS・derived subgroup・hexagon・settled を独立に
## 再実装する)
#############################################################################
Print("--- R4: 第二系統(独立 Python 実装)向けデータ出力 ---\n");
DumpPermList := function(p, n)
  local l, i;
  l := [];
  for i in [1..n] do Add(l, i^p); od;
  return JArr(List(l, String));
end;;

r4DataStr := Concatenation(
  "{\"k3\":{\"n_points\":9,",
  "\"x_images\":", DumpPermList(gn3.x, 9), ",",
  "\"y_images\":", DumpPermList(gn3.y, 9), ",",
  "\"expected_g_size\":", String(res3.g_size), ",",
  "\"expected_n_ord\":", String(res3.n_ord), ",",
  "\"expected_candidate_total\":", String(res3.hexagon.candidate_total), ",",
  "\"expected_h10_fail\":", String(res3.hexagon.h10_fail), ",",
  "\"expected_h11_fail\":", String(res3.hexagon.h11_fail), ",",
  "\"expected_generation_fail\":", String(res3.hexagon.generation_fail), ",",
  "\"expected_shadow_total\":", String(res3.hexagon.shadow_total), ",",
  "\"expected_settled_count\":", String(res3.settled.settled_count), ",",
  "\"expected_settled_total\":", String(res3.settled.total), ",",
  "\"expected_verdict\":\"", res3.isolated_verdict, "\"",
  "},",
  "\"m_iso2_witness\":{\"source\":", JStr(witnessSourceLabel), ",\"m\":", String(witnessM), ",",
  "\"stage\":", JStr(witnessSearch.stage), ",",
  "\"f_word\":", WordToJson(witnessWord), ",",
  "\"f_word_note\":\"f_word alone is convention-fragile (BFSWords prepend-storage vs EvalWordQT/EvalWordInQ evaluators gave DIFFERENT elements for the SAME word -- see driver comment near FindH11FailWitness). f_images below is the authoritative raw permutation, independent of any word-evaluation convention; R4 should use f_images, not re-derive f from f_word.\",",
  "\"n_points\":", String(witnessNPoints), ",",
  "\"f_images\":", DumpPermList(witnessFElt, witnessNPoints), ",",
  "\"expected_subgroup_size_lt_g\":", JB(witnessSubgroupSize < res3.g_size), ",",
  "\"expected_subgroup_size\":", String(witnessSubgroupSize), ",",
  "\"expected_g_size\":", String(res3.g_size), "},",
  "\"m_iso2_v2_reconstruction\":{",
  "\"desc\":\"witness moved from h11_fail bucket to shadow bucket (path-layer, not scalar) -- see docs/notes/iso_r3r4_iffirst_freeze_v1.md sec.7\",",
  "\"expected_h11_fail\":", String(mIso2H11Fail), ",",
  "\"expected_shadow_total\":", String(mIso2ShadowTotal), ",",
  "\"expected_shadow_sum_check\":", JB(mIso2ShadowSumOk), ",",
  "\"expected_settled_count\":", String(mIso2SettledResult.settled_count), ",",
  "\"expected_settled_total\":", String(mIso2SettledResult.total), ",",
  "\"expected_witness_settled\":", JB(witnessSettledEntry.settled), ",",
  "\"expected_all_shadows_genuine\":", JB(mIso2AllGenuine), ",",
  "\"expected_verdict\":\"", mIso2Verdict.verdict, "\",",
  "\"expected_unknown_reason\":\"", mIso2Verdict.reason, "\"",
  "},",
  "\"w5\":{\"n_points\":23,",
  "\"x_images\":", DumpPermList(xhat5, 23), ",",
  "\"y_images\":", DumpPermList(yhat5, 23), ",",
  "\"expected_g_size\":", String(res5.g_size), ",",
  "\"expected_n_ord\":", String(res5.n_ord), ",",
  "\"expected_candidate_total\":", String(res5.hexagon.candidate_total), ",",
  "\"expected_h10_fail\":", String(res5.hexagon.h10_fail), ",",
  "\"expected_h11_fail\":", String(res5.hexagon.h11_fail), ",",
  "\"expected_generation_fail\":", String(res5.hexagon.generation_fail), ",",
  "\"expected_shadow_total\":", String(res5.hexagon.shadow_total), ",",
  "\"expected_settled_count\":", String(res5.settled.settled_count), ",",
  "\"expected_settled_total\":", String(res5.settled.total), ",",
  "\"expected_verdict\":\"", res5.isolated_verdict, "\"",
  "}}");;

WriteFile("search/probe/w6_bu_s0/r4_input_data.json", r4DataStr);;
Print("wrote search/probe/w6_bu_s0/r4_input_data.json (raw generator permutation data for R4 second system)\n\n");

#############################################################################
## cert 出力
#############################################################################
IsoGateResultToJsonR3R4 := function(r)
  local notSettledJson, settledByMJson, sd, base;
  if not r.precondition_ok then
    return Concatenation(
      "{\"label\":", JStr(r.label), ",",
      "\"precondition_ok\":false,",
      "\"g_size\":", String(r.g_size), ",",
      "\"isolated_verdict\":\"UNKNOWN\",",
      "\"unknown_reason\":\"", r.unknown_reason, "\",",
      "\"iso_gate_state\":\"UNKNOWN\",",
      "\"group_side\":", JStr(r.group_side), ",",
      "\"enumeration_domain\":", JStr(r.enumeration_domain),
      "}");
  fi;
  if r.hexagon = fail then
    return Concatenation(
      "{\"label\":", JStr(r.label), ",",
      "\"precondition_ok\":true,",
      "\"g_size\":", String(r.g_size), ",",
      "\"n_ord\":", String(r.n_ord), ",",
      "\"isolated_verdict\":\"UNKNOWN\",",
      "\"unknown_reason\":\"", r.unknown_reason, "\",",
      "\"iso_gate_state\":\"UNKNOWN\",",
      "\"group_side\":", JStr(r.group_side), ",",
      "\"enumeration_domain\":", JStr(r.enumeration_domain),
      "}");
  fi;
  notSettledJson := [];
  for sd in Filtered(r.settled.detail, x -> not x.settled) do
    Add(notSettledJson, Concatenation("{\"m\":", String(sd.m), ",\"f_word\":", WordToJson(sd.f_word), "}"));
  od;
  settledByMJson := [];
  for sd in r.settled_by_m do
    Add(settledByMJson, Concatenation("{\"m\":", String(sd.m), ",\"total\":", String(sd.total),
        ",\"settled\":", String(sd.settled), "}"));
  od;
  base := Concatenation(
    "{\"label\":", JStr(r.label), ",",
    "\"ker_is_Kn\":", (function() if r.kerIsKn = fail then return "null"; else return String(r.kerIsKn); fi; end)(), ",",
    "\"precondition_ok\":true,",
    "\"g_size\":", String(r.g_size), ",",
    "\"n_ord\":", String(r.n_ord), ",",
    "\"charming_set_size\":", String(r.charming_set_size), ",",
    "\"hexagon_enumeration\":{\"candidate_total\":", String(r.hexagon.candidate_total),
    ",\"h10_fail\":", String(r.hexagon.h10_fail),
    ",\"h11_fail\":", String(r.hexagon.h11_fail),
    ",\"generation_fail\":", String(r.hexagon.generation_fail),
    ",\"shadow_total\":", String(r.hexagon.shadow_total),
    ",\"sum_check_pass\":", String(r.shadow_sum_check),
    ",\"all_shadows_genuine\":", String(r.all_shadows_genuine), "},",
    "\"settled_summary\":{\"settled_count\":", String(r.settled.settled_count),
    ",\"total\":", String(r.settled.total),
    ",\"settled_by_m\":", JArr(settledByMJson),
    ",\"not_settled_detail\":", JArr(notSettledJson), "},",
    "\"isolated_verdict\":\"", r.isolated_verdict, "\",",
    "\"unknown_reason\":\"", r.unknown_reason, "\",",
    "\"iso_gate_state\":\"", r.iso_gate_state, "\",",
    "\"group_side\":", JStr(r.group_side), ",",
    "\"enumeration_domain\":", JStr(r.enumeration_domain), ",",
    "\"time_ms_hexagon_enum\":", String(r.time_ms_hexagon), ",",
    "\"time_ms_settled_check\":", String(r.time_ms_settled),
    "}");
  return base;
end;;

mutantJson := Concatenation(
  "[",
  "{\"id\":\"M-ISO-1\",\"desc\":\"known isolated positive (K^(3), Thm 4.3)\",\"expected\":\"TRUE\",",
    "\"fired\":", String(mIso1Ok), ",\"kills\":\"basic soundness\"},",
  "{\"id\":\"M-ISO-2\",\"desc\":\"v2 (裁定535 R-B): witness (real h11_fail candidate from ", witnessSourceLabel, "'s hexagon enumeration) moved from h11_fail bucket to shadow bucket -- path-layer, run through the REAL SettledCheckGeneral. VerifyShadowsGenuine flags it, but this is a STRUCTURALLY GUARANTEED result (same hex310/hex311/SURJ formula as the enumerator that already classified it h11_fail), not an independent discovery -- see 軽微G note; the informative facts are witness_settled=false and the identity 108-72-23-0=13\",",
    "\"witness_source\":", JStr(witnessSourceLabel), ",",
    "\"witness_m\":", String(witnessM), ",\"witness_f_word\":", WordToJson(witnessWord), ",",
    "\"witness_stage\":", JStr(witnessSearch.stage), ",",
    "\"witness_subgroup_size\":", String(witnessSubgroupSize), ",\"witness_g_size\":", String(res3.g_size), ",",
    "\"h11_fail_24_to\":", String(mIso2H11Fail), ",\"shadow_total_12_to\":", String(mIso2ShadowTotal), ",",
    "\"identity_holds\":", JB(mIso2ShadowSumOk), ",",
    "\"settled_via_real_path\":\"", String(mIso2SettledResult.settled_count), "/", String(mIso2SettledResult.total), "\",",
    "\"witness_settled\":", JB(witnessSettledEntry.settled), ",",
    "\"paper_argument\":\"image subgroup order < |G| => induced endomorphism's image is a proper subgroup => not surjective onto G => not bijective on the finite set G (independently confirmed by the real GroupHomomorphismByImages+IsBijective path, not hand-computed)\",",
    "\"is_this_isolated_false\":\"NO -- this fixture does NOT claim isolated=FALSE has a real witness (AS-GAP-6 remains open). It tests whether the pipeline refuses to launder a non-GT-shadow candidate into an isolated=FALSE verdict.\",",
    "\"expected\":\"UNKNOWN(NONSHADOW_IN_DATUM)\",\"fired\":", String(mIso2Ok), ",\"kills\":\"laundering a non-shadow candidate into a false isolated=FALSE claim; also feeds M-ISO-3/8\"},",
  "{\"id\":\"M-ISO-3\",\"desc\":\"constant-TRUE mutant, a real function call (MutantConstantTrueVerdict) run on M-ISO-2(v2)'s real 4-arg input\",\"expected\":\"detected (mismatch vs real verdict)\",",
    "\"mutant_output\":\"", mIso3MutantResult.verdict, "\",\"real_verdict\":\"", mIso2Verdict.verdict, "\",",
    "\"fired\":", String(mIso3Detected), ",\"kills\":\"constant-TRUE returning TRUE unconditionally\"},",
  "{\"id\":\"M-ISO-4\",\"desc\":\"single settled-flip on real K^(3) settled detail (12/12 -> 11/12)\",\"expected\":\"FALSE\",",
    "\"fired\":", String(mIso4Ok), ",\"kills\":\"verdict not actually checking ALL shadows settled\"},",
  "{\"id\":\"M-ISO-5\",\"desc\":\"candidate drop: shadow_total 12->11 without adjusting fail-stage counts\",",
    "\"expected\":\"UNKNOWN or FALSE (not TRUE)\",\"actual\":\"", mIso5Verdict.verdict, "/", mIso5Verdict.reason, "\",",
    "\"fired\":", String(mIso5Ok), ",\"kills\":\"B-1 completeness assumption silently violated\"},",
  "{\"id\":\"M-ISO-6a\",\"desc\":\"c NOT IN N precondition-gate branch (N5-control fixture, 既済再確認)\",\"expected\":\"UNKNOWN(C_NOT_IN_N)\",",
    "\"fired\":", String(mIso6aOk), ",\"kills\":\"vacuous-truth from missing precondition\"},",
  "{\"id\":\"M-ISO-6b\",\"desc\":\"zero-shadow synthetic scenario\",\"expected\":\"UNKNOWN(NO_SHADOWS)\",",
    "\"fired\":", String(mIso6bOk), ",\"kills\":\"vacuous-truth from empty shadow set\"},",
  "{\"id\":\"M-ISO-7\",\"desc\":\"descent-filter-contamination source-map detector (docs/notes/auto_settled_check_v1.md AS-GAP-3/S-BU-17, commander order 2026-08-05): (a) self-audit of THIS driver's real EnumerateReducedHexagon -- contaminated=", JB(realCheck.contaminated), " (b) negative control on a deliberately-broken mutant enumerator -- contaminated=", JB(mutantCheck.contaminated), "\",",
    "\"as_gap_3_verdict\":\"CONFIRMED_CLEAN: enumeration filter (hexagon 3.10/3.11 + charming + SURJ) does not consult descent/K5-8/GroupHomomorphismByImages; settled=100% on K^(3)/W-5 is sample bias (bare K^(n) and its fiber-product caps are known-isolated per Thm 4.3/Prop 3.14), not constant-TRUE contamination\",",
    "\"expected\":\"real=clean, mutant=ENUMERATION_FILTER_CONTAMINATION/STOP\",",
    "\"fired\":", String(mIso7Ok), ",\"kills\":\"descent used as an enumeration filter (would make settled=100% a tautology and risks isolated false-TRUE via silent candidate drop)\"},",
  "{\"id\":\"M-ISO-8\",\"desc\":\"settled:=true fixed mutant (MutantSettledAlwaysTrue), run on M-ISO-2(v2)'s real 13-element datum -- falsifier found this mutant SURVIVED all v1 fixtures+R4 (settled predicate's negative branch had never fired)\",",
    "\"detection_mechanism\":\"detail-element comparison, NOT verdict comparison (v2.1 fix, 裁定543 要修正A): witnessSettledEntry.settled (real SettledCheckGeneral) vs mIso8WitnessMutantEntry.settled (MutantSettledAlwaysTrue), both on the SAME witness of the SAME 13-element datum\",",
    "\"real_witness_settled\":", JB(witnessSettledEntry.settled), ",\"mutant_witness_settled\":", JB(mIso8WitnessMutantEntry.settled), ",",
    "\"real_settled_count\":", String(mIso2SettledResult.settled_count), ",\"mutant_settled_count\":", String(mIso8MutantSettled.settled_count), ",",
    "\"verdict_insensitivity_note\":\"falsifier confirmed (iso_r3r4_cv9_reading_v2.md sec.3(c)) that ComputeVerdict's OUTPUT on this datum is INSENSITIVE to this mutation (NONSHADOW_IN_DATUM fires regardless of settled=12 or 13, since allShadowsGenuine=false dominates) -- the kill is at the detail-element level (this cert's own assertion), not a property discoverable by comparing verdicts. What is actually being struck is the settled CHANNEL, via the same assertion structure M-ISO-2(v2) itself uses.\",",
    "\"expected\":\"real witness settled=false, mutant witness settled=true, mismatch detected at detail level\",",
    "\"fired\":", String(mIso8Ok), ",\"kills\":\"settled predicate fixed to always-true; detected via M-ISO-2(v2)'s own assertion on the witness detail entry (witnessSettledEntry.settled=false and settled_count=12), NOT via a verdict-level comparison (v2.1 correction of the v2 kills-attribution error)\"}",
  "]");;

searchAppendixJson := Concatenation(
  "{\"purpose\":\"pre-M-ISO-2 search for a NATURAL isolated=FALSE fixture (before falling back to constructed mutation) -- kept for mathematician review of the 'settled is automatic given hexagon+SURJ+finiteness' hypothesis flagged to commander\",",
  "\"families_tried\":[",
    "\"bare MakeGn(n) for n=4,5,6,7,9 (all settled=total, all TRUE)\",",
    "\"MakeGn(n) fiber-product-capped with MakeQ8 for n=3,4,6,7 (all settled=total, all TRUE)\",",
    "\"MakeGn(n) fiber-product-capped with MakeHeis(4,2) for n=3,5 (all settled=total, all TRUE)\",",
    "\"MakeGn(3) fiber-product-capped with MakeP3 (order 128) (settled=total, TRUE)\",",
    "\"BuildQTGeneral windows over Q in {C3,C4,C6,S3,D4,A4} with various phi_X/phi_Y/phi_C (mostly c NOT IN N or theta/tau-does-not-extend; the ones with c IN N and theta/tau well-defined were not found in this pass)\"",
  "],",
  "\"conclusion\":\"no natural mixed-settled (isolated=FALSE) window found among these families up to the sizes tried; hypothesis (not proven here): any (m,f) passing hexagon(3.10)/(3.11)+SURJ is automatically settled by finiteness (surjective endo of finite G is automatically bijective, PROVIDED the induced map is well-defined -- which hexagon passage is meant to guarantee per Prop 3.2). SECOND, STRONGER empirical fact found while building M-ISO-2's witness: in bare MakeGn(n) for n=4,5,6,7,9,10, generation_fail=0 in EVERY case (every candidate that passes hexagon(3.10)/(3.11) ALSO passes the generation/SURJ check -- hexagon and generation never diverge in these fixtures). Both facts escalated to commander/mathematician 2026-08-05 for review; NEITHER is claimed as a theorem by this driver.\",",
  "\"scratch_scripts\":[\"scratchpad/explore_m2_negative.g\",\"scratchpad/explore_m2_negative2.g\",\"scratchpad/explore_m2_negative3.g\",\"scratchpad/explore_m2_negative3_lib.g\",\"scratchpad/explore_m2_negative4.g\",\"scratchpad/explore_m2_negative5.g\",\"scratchpad/explore_m2_negative6.g\",\"scratchpad/explore_m2_negative7.g\"]",
  "}");;

## ★v2.1【要修正B】+【軽微F】(裁定543): conventions_used を機械 diff 可能な
## 形へ再設計。5 項目(perm_composition・abstract_prod_reversal・word_eval・
## h10_fail_bookkeeping_unit・comparison_target)は統制語彙(enum)/固定構造
## にし、散文は別途 `*_note` 欄へ退避(diff 対象外)。この 5 項目 +
## grading_prohibitions の値は Python 側(search/probe/w6_bu_s0/
## r4_second_system.py)と BYTE-IDENTICAL になるよう記述する
## (grading_prohibitions は両側とも conventions_used 内、同一パス --軽微F)。
CANON_GRADING_PROHIBITION := "PERMANENT BAN (commander ruling 535/543, falsifier finding): never write that numeric agreement between two implementations demonstrates convention identity. Any same-object verdict must rest on source-reading (CV-9 judge), never on a cert's own numeric match.";;
conventionsUsedJson := Concatenation(
  "{\"ledger_version\":\"conventions_ledger_v1_6\",",
  "\"perm_composition\":\"gap_native_right\",",
  "\"perm_composition_note\":\"GAP permutations act on the right: i^(p*q)=(i^p)^q. Python's compose(p,q) implements the same convention.\",",
  "\"abstract_prod_reversal\":{\"reversed\":true,\"rule\":\"AbstractProd([a1,...,ak]) = ak*a(k-1)*...*a1\",",
    "\"usages\":[",
      "{\"site\":\"z\",\"formula\":\"AbstractProd([x,y])^-1 = (y*x)^-1\"},",
      "{\"site\":\"hex310\",\"formula\":\"AbstractProd([f,thetaf])=1 <=> thetaf*f=1\"},",
      "{\"site\":\"ymf\",\"formula\":\"AbstractProd([y^m,f]) = f*y^m\"},",
      "{\"site\":\"hex311\",\"formula\":\"AbstractProd([tau2,tau1,ymf])=1 <=> ymf*tau1*tau2=1\"},",
      "{\"site\":\"genB\",\"formula\":\"AbstractProd([f^-1,y^u,f]) = f*y^u*f^-1\"}",
    "]},",
  "\"abstract_prod_reversal_note\":\"confirmed by direct GAP probe and independently by falsifier's third implementation (docs/notes/iso_r3r4_cv9_reading_v1.md sec.2.1)\",",
  "\"word_eval\":[",
    "{\"layer\":\"BFSWords_storage\",\"direction\":\"prepend\",\"word_source\":\"internal_gap\"},",
    "{\"layer\":\"witness_reconstruction\",\"direction\":\"prepend\",\"word_source\":\"internal_gap\"}",
  "],",
  "\"word_eval_note\":\"BFSWords storage is prepend (裁定166); witness reconstruction must use EvalWordInQ (prepend), NOT EvalWordQT (natural), which reconstructs a different element for the same word. Python side bypasses word evaluation entirely via raw f_images but declares the same layer/direction/word_source shape for machine-diffability.\",",
  "\"enumeration_domain\":\"group_elements\",",
  "\"group_side\":\"P_PB3_mod_N\",",
  "\"h10_fail_bookkeeping_unit\":\"per_fm_pair\",",
  "\"h10_fail_bookkeeping_unit_note\":\"theta/tau precondition (hex310) is checked inside the m-loop, redundantly per m, matching the GAP loop structure in EnumerateReducedHexagon exactly; NOT per-f.\",",
  "\"comparison_target\":{",
    "\"as_function_of\":\"marked_datum\",",
    "\"function_a\":{\"name\":\"IsoGateCheck_ComputeVerdict_GAP\",\"domain\":\"marked_datum_to_5_quantities\"},",
    "\"function_b\":{\"name\":\"run_fixture_compute_verdict_python\",\"domain\":\"marked_datum_to_5_quantities\"},",
    "\"normalization_digest\":\"n/a\"",
  "},",
  "\"comparison_target_note\":\"5 quantities = g_size, n_ord, shadow_total, settled_count/total, verdict per docs/notes/iso_r3r4_iffirst_freeze_v1.md sec.2\",",
  "\"effective_source_chain\":[",
    "{\"role\":\"current\",\"path\":\"search/probe/w6_bu_s0/iso_gate_r3r4_driver.g\",\"sha256\":\"n/a (computed post-write by the reporting layer, not embedded here per CV-10 self-reference discipline)\"}",
  "],",
  "\"seal_recoverability\":{\"status\":\"n/a\",\"reason\":\"this cert does not use sealed fixtures\"},",
  "\"grading_prohibitions\":[\"", CANON_GRADING_PROHIBITION, "\"],",
  "\"grading_prohibitions_note\":\"falsifier's third independent implementation showed the compared 5 quantities (|G|, N_ord, shadow_total, settled_count/total) are IDENTICAL whether AbstractProd is evaluated with the real reversal or with the naive (unreversed) paper-order convention -- i.e. this observation window has ZERO discriminating power for convention identity (docs/notes/iso_r3r4_cv9_reading_v1.md sec.3 【重大1】).\",",
  "\"level\":\"PB3\"",
  "}");;

certStr := Concatenation(
  "{\"schema\":\"gtsh-cert/iso-gate-r3r4/v2.1\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/probe/w6_bu_s0/iso_gate_r3r4_driver.g\",\"date\":\"2026-08-05\"},",
  "\"tier\":\"tool-calibration\",",
  "\"purpose\":\"ISO-GATE route-2 R3 (mutant matrix, 8 items) + R4 (second-system data export) + interface field corrections, per docs/notes/w6_bottomup_design_v4.md sec.5.3/5.4/5.1; W-5 iso_gate_state stays UNKNOWN (pending route-2 gate), NOT upgraded by this driver\",",
  "\"design_authority\":\"commander order 2026-08-05 (design v4) + 裁定535 (v2 repair) + 裁定543 (v2.1 repair, following falsifier CV-9-2 re-reading docs/notes/iso_r3r4_cv9_reading_v2.md, cross-checked grading GRANTED conditional on this repair)\",",
  "\"effective_source_chain_note\":\"supersede chain: v1 (search/certs/w6_bu_s0_iso_gate_r3r4_20260805.json) -> v2 (search/certs/w6_bu_s0_iso_gate_r3r4_v2_20260805.json, UNCHANGED by this v2.1 order) -> v2.1 (this file). Both v1 and v2 are left byte-unmodified per CV-10 erratum discipline -- this is a new file, not an in-place rewrite.\",",
  "\"v2_supersedes\":{\"path\":\"search/certs/w6_bu_s0_iso_gate_r3r4_20260805.json\",\"scope\":\"v1 M-ISO-2/3/4/5/6b were scalar-layer mutations of ComputeVerdict only; M-ISO-2 bypassed its own shadow_sum_check gate by hand-passing true; a settled:=true fixed mutant (M-ISO-8) survived all v1 fixtures undetected.\"},",
  "\"v2_1_supersedes\":{\"path\":\"search/certs/w6_bu_s0_iso_gate_r3r4_v2_20260805.json\",\"scope\":\"cross-checked grading granted by falsifier (docs/notes/iso_r3r4_cv9_reading_v2.md sec.3) CONDITIONAL on repairing: 要修正A (M-ISO-8 kills-attribution was verdict-comparison, but the real v2 verdict is INSENSITIVE to the settled mutation on the M-ISO-2(v2) datum -- the actual kill is at the detail-element level; fixed here) and 要修正B (conventions_used had 0/5 machine-diffable keys between the two certs -- free prose vs enum/dict type mismatches and Python-side absences; fixed here with canonical enum/dict values + prose moved to *_note fields). Also folds in 軽微C (literal true shadowSumOk hand-passes in M-ISO-4/6b replaced with computed values), 軽微D (freeze doc erratum, committed standalone per the new permanent rule), 軽微E (Python staged-counter asserts), 軽微F (grading_prohibitions placement unified inside conventions_used on both sides), 軽微G (M-ISO-2's all_shadows_genuine=false is now documented as a STRUCTURALLY GUARANTEED consequence of using the same hex310/hex311/SURJ formula as the enumerator, not an independent detection).\"},",
  "\"non_contact_declaration\":{\"Im_R_reduction_image\":\"not touched\",\"d_N\":\"not touched\",",
  "\"sealed_quantities\":\"not touched (c_mu_hat / PSL window structural quantities / eps bits / 705,894 universe)\",",
  "\"u_arithmetic_value\":\"not touched\"},",
  "\"independence\":\"no certificates/*.json or search/certs/*.json read; all groups rebuilt from generators in this run; old driver search/probe/w6_bu_s0/iso_gate_check.g left untouched\",",
  "\"conventions_used\":", conventionsUsedJson, ",",
  "\"fix_notes\":[",
    "\"isolated_verdict now gated on shadow_sum_check via ComputeVerdict (v1 fix, retained)\",",
    "\"EnumerateReducedHexagonSafe wrapper (v1 fix, retained) -- graceful UNKNOWN(THETA_TAU_NOT_WELLDEFINED) instead of Error() crash\",",
    "\"★ v2 (裁定535 R-A/R-B/③④⑤): ComputeVerdict is now a 4-argument function with a new allShadowsGenuine gate (highest priority, new stop code NONSHADOW_IN_DATUM) -- VerifyShadowsGenuine independently re-checks hex310/hex311/SURJ for every element of a given shadow list, catching non-shadow candidates that a hand-built shadow list might contain\",",
    "\"★ v2: M-ISO-2 rebuilt as a path-layer mutation (witness moved from h11_fail bucket to shadow bucket, real SettledCheckGeneral call on the 13-element list) instead of a scalar ComputeVerdict(true,13,12) hand-call that bypassed its own sum-check gate (falsifier 4.2). Expected verdict is now UNKNOWN(NONSHADOW_IN_DATUM), NOT FALSE -- per mathematician auto_settled_check_v1.md addendum A.2, an h11-fail candidate is not a GT-shadow (Def 3.7), so treating it as a non-settled SHADOW would be a false-FALSE route into isolated=FALSE\",",
    "\"★ v2: M-ISO-3/4/5/6b restored to path-layer mutations (real function calls: MutantConstantTrueVerdict, ShallowCopy+Number() recount, real list slice + SettledCheckGeneral, SettledCheckGeneral([])) instead of scalar arithmetic on ComputeVerdict's inputs\",",
    "\"★ v2 NEW: M-ISO-8 (settled:=true fixed mutant) added -- falsifier found this mutant survived ALL of v1's R3 matrix + R4 crosscheck undetected, because none of the 4 real v1 fixtures ever exercised settled=false. M-ISO-2(v2)'s real non-settled witness now makes this mutant killable\",",
    "\"★ v2.1【要修正A】: M-ISO-8's detection mechanism corrected from verdict-comparison to detail-element comparison. falsifier machine-confirmed ComputeVerdict(allGenuine=false,sumOk=true,13,12) and (...,13,13) BOTH return UNKNOWN/NONSHADOW_IN_DATUM -- the verdict is insensitive to the settled mutation on this datum (the gate dominates). The actual kill is witnessSettledEntry.settled=false vs the mutant's corresponding detail entry=true; kills text corrected accordingly\",",
    "\"★ v2.1【要修正B】: conventions_used redesigned for machine-diffability -- perm_composition/h10_fail_bookkeeping_unit are now bare enum strings, abstract_prod_reversal/word_eval/comparison_target are fixed dict/array shapes byte-identical to the Python cert, prose moved to *_note sibling fields, grading_prohibitions text made byte-identical and placed inside conventions_used on both sides (軽微F)\",",
    "\"★ v2.1【軽微C】: M-ISO-4/6b's literal true shadowSumOk hand-passes replaced with computed values (res3.shadow_sum_check for M-ISO-4; an explicit 0-0-0-0=0 identity computation for M-ISO-6b)\",",
    "\"★ v2.1【軽微G】: comments/cert text clarify that M-ISO-2(v2)'s all_shadows_genuine=false is a structurally guaranteed consequence (same formula as the enumerator that already classified the witness h11_fail), not an independent detection -- the informative facts are witness_settled=false and the identity 108-72-23-0=13\"",
  "],",
  "\"m_iso2_construction_note\":\"★ CORRECTED (v2, per commander 裁定535 ② and mathematician auto_settled_check_v1.md addendum A.2): the v1 claim that M-ISO-2 is 'the campaign's first isolated=FALSE instance' is WITHDRAWN. M-ISO-2 does NOT demonstrate isolated=FALSE for any marked datum -- there is no marked datum here whose GT(N) contains a genuine non-settled GT-shadow. The witness is an h11_fail candidate, which by Def 3.7 is not a GT-shadow at all. M-ISO-2(v2) tests a DIFFERENT, narrower property: that the pipeline detects and refuses to launder a non-shadow candidate (accidentally present in a shadow list) into an isolated=FALSE verdict, returning UNKNOWN(NONSHADOW_IN_DATUM) instead. AS-GAP-6 (obtaining a genuine non-isolated witness, via a twin K != N or a non-verbal N_{F_2}, per w6_bottomup_design_v4.md sec.5.3 and auto_settled_check_v1.md sec.3.2/3.4) remains OPEN and out of scope for this driver.\",",
  "\"fixtures\":[", IsoGateResultToJsonR3R4(res3), ",", IsoGateResultToJsonR3R4(res5), ",",
    IsoGateResultToJsonR3R4(resN5), ",", IsoGateResultToJsonR3R4(resQ3a), "],",
  "\"mutant_matrix\":", mutantJson, ",",
  "\"search_appendix\":", searchAppendixJson, ",",
  "\"all_mutants_fired_as_expected\":", String(allMutantsOk), ",",
  "\"r4_second_system\":{\"status\":\"data exported to search/probe/w6_bu_s0/r4_input_data.json for independent Python re-implementation; companion script search/probe/w6_bu_s0/r4_second_system.py (v2) independently confirmed the 5 comparison quantities (per docs/notes/iso_r3r4_iffirst_freeze_v1.md sec.2) for K^(3), W-5, and the M-ISO-2(v2) reconstructed datum -- see search/probe/w6_bu_s0/r4_second_system_output.json for its own output; this GAP cert does not itself run the second system, run separately via: python search/probe/w6_bu_s0/r4_second_system.py\",",
  "\"note\":\"GAP one-output remains candidate per F104-2.3; second system independence documented separately. Per falsifier CV-9-2 finding 【要修正2】, the Python output only exists on assert-success (exception on mismatch => no output file) -- this is a known weakness, not fixed in this v2 (out of the 6-item order's scope; flagged for a future pass)\"},",
  "\"crosscheck_status\":\"not cross-checked by THIS file alone (R4 second system is a separate script; see its output for the actual crosscheck verdict). Per falsifier CV-9-2, numeric agreement alone does not establish cross-checked status -- see grading_prohibitions above and conventions_used for the source-reading basis of the 'same object' judgment\",",
  "\"verified_status\":\"not verified (Lean not used)\"",
  "}");;

WriteFile("search/certs/w6_bu_s0_iso_gate_r3r4_v2_1_20260805.json", certStr);;
Print("wrote search/certs/w6_bu_s0_iso_gate_r3r4_v2_1_20260805.json (v1 and v2 certs left untouched)\n");

Print("\nISO_GATE_R3R4_DRIVER_DONE\n");
QUIT;
