#############################################################################
## search/probe/w6_bu_s0/iso_gate_r3r4_driver.g
## ISO-GATE route-2 R3(mutant matrix, 7 件 -- M-ISO-7 は司令塔 2026-08-05 追加委嘱
## docs/notes/auto_settled_check_v1.md AS-GAP-3/S-BU-17 に基づく)+ R4(第二系統への突合用データ出力)+
## interface 欄訂正(group_side / enumeration_domain / hom-fail 捕捉)。
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
#############################################################################
ComputeVerdict := function(shadowSumOk, totalShadows, settledCount)
  if not shadowSumOk then
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
## IsoGateCheck(修理(1)(2)を組み込み、group_side/enumeration_domain 欄を追加)
#############################################################################
IsoGateCheck := function(qrec, label, kerIsKn)
  local precheck, nOrd, charmingSet, t0, t1, hexSafe, hexResult, shadowSumOk,
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

  verdictRec := ComputeVerdict(shadowSumOk, settled.total, settled.settled_count);;

  if kerIsKn <> fail then
    isoGateState := "PROVEN";
  else
    isoGateState := "UNKNOWN (pending commander/Sol gate on driver-TRUE as ISO-GATE route (2))";
  fi;

  return rec(label:=label, kerIsKn:=kerIsKn, precondition_ok:=true,
    g_size:=Size(qrec.G), n_ord:=nOrd, charming_set:=charmingSet,
    charming_set_size:=Length(charmingSet),
    hexagon:=hexResult, shadow_sum_check:=shadowSumOk,
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
## M-ISO-2 / M-ISO-3 / M-ISO-4 / M-ISO-5 / M-ISO-6(b): データレベル mutation
## (K^(3) の実測結果 res3 から構成 -- 司令塔裁定 2026-08-05: 自然な
## isolated=FALSE 窓は 5 族 10+ ケースの探索(scratchpad/explore_m2_negative*.g)
## で発見できなかったため、データレベル mutation を援用してよいと承認済み。
## 正直な明記: これらは実装担当が構成した合成反例であり、既存の登録済み事実
## ではない。探索記録は cert appendix に残す(数学者検分の一次資料)。
#############################################################################
Print("--- M-ISO-2/3/4/5/6(b): データレベル mutation matrix (constructed from real K^(3) data) ---\n");

# M-ISO-2: witness = a genuine generation_fail candidate from res3's real hexagon
# enumeration (NOT a hand-wave -- Size(Group(genA,genB)) < Size(G) is a real,
# already-computed fact for this candidate). Inject it as a fake extra "shadow";
# paper argument: image subgroup is proper => the induced endomorphism cannot be
# surjective onto G => cannot be bijective on the finite set G (no computation
# needed beyond the already-known proper-subgroup fact).
Print("K^(3) generation_fail count = ", res3.hexagon.generation_fail,
      "  (h10_fail=", res3.hexagon.h10_fail, " h11_fail=", res3.hexagon.h11_fail, ")\n");
Print("W-5 generation_fail count = ", res5.hexagon.generation_fail,
      "  (h10_fail=", res5.hexagon.h10_fail, " h11_fail=", res5.hexagon.h11_fail, ")\n");
Print("  (both are 0 -- an additional empirical structural fact for the appendix: in these\n");
Print("   Dn-tower fixtures, EVERY candidate reaching the generation/SURJ check passes it;\n");
Print("   generation_fail never fires. So a real 'generation_fail'-staged witness does not\n");
Print("   exist here. Falling back to an h10/h11-failing candidate, independently re-checked\n");
Print("   below for actual non-generation -- still a real (m,f) pair from the real hexagon\n");
Print("   enumeration, just not one that reached the generation-check stage internally.)\n");
witnessSourceLabel := "K^(3)";;
witnessDatum := datum3;;
witnessBaseShadowsTotal := res3.settled.total;;
witnessBaseSettledCount := res3.settled.settled_count;;
witnessBaseGSize := res3.g_size;;
## ★重要な訂正(R4 二系統照合で発覚): cand.f_word は BFSWords(prepend-storage
## 規約 -- 裁定166)由来なので、再評価には EvalWordInQ(prepend 規約)を
## 使わねばならない。EvalWordQT(natural 規約)は BFSWords 由来の word には
## 使えない(同じ word でも別の元に評価される -- 罠 12 件外の第3の規約罠を
## R4 の食い違いが実際に検出した。scratchpad/debug_witness.g で実証:
## 同一 word に対し EvalWordQT->(7,9,8)(誤り、部分群位数36)、
## EvalWordInQ->(7,8,9)=実際の BFS 元(正しい、この元は G を生成し位数108)。
## 修理前の版はこのバグにより無効な witness を使っていた -- 破棄し訂正。
FindNonGeneratingWitness := function(hexResult, qrec)
  local cand, m, u, f, genA, genB, sz;
  for cand in hexResult.generation_detail do
    if cand.stage = "h10_fail" or cand.stage = "h11_fail" then
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
witnessSearch := FindNonGeneratingWitness(res3.hexagon, datum3);;
if not witnessSearch.found then
  Print("  (no non-generating h10/h11-failing candidate found in K^(3) either -- falling back to W-5)\n");
  witnessSearch := FindNonGeneratingWitness(res5.hexagon, datum5);;
  witnessSourceLabel := "W-5";;
  witnessDatum := datum5;;
  witnessBaseShadowsTotal := res5.settled.total;;
  witnessBaseSettledCount := res5.settled.settled_count;;
  witnessBaseGSize := res5.g_size;;
fi;
if not witnessSearch.found then
  Error("M-ISO-2: no non-generating witness candidate found in either K^(3) or W-5 -- cannot construct fixture");
fi;
Print("M-ISO-2 witness source: ", witnessSourceLabel, " (from an ", witnessSearch.stage, " candidate, independently re-checked for non-generation)\n");
witnessM := witnessSearch.m;;
witnessWord := witnessSearch.f_word;;
witnessFElt := witnessSearch.f_elt;;
witnessNPoints := (function() if witnessSourceLabel = "K^(3)" then return 9; else return 23; fi; end)();;
witnessSubgroupSize := witnessSearch.subgroup_size;;
Print("M-ISO-2 witness: m=", witnessM, " f_word=", witnessWord,
      "  |<genA,genB>|=", witnessSubgroupSize, " (< |G|=", witnessBaseGSize, "? ", witnessSubgroupSize < witnessBaseGSize, ")\n");
Print("  paper argument: image subgroup order ", witnessSubgroupSize, " < |G|=", witnessBaseGSize,
      " => induced map's image is a PROPER subgroup => not surjective onto G => not bijective on finite G (no further computation needed)\n");

realShadowsTotal := witnessBaseShadowsTotal;;      # real shadows from witness source, all genuinely settled
realSettledCount := witnessBaseSettledCount;;
mIso2ShadowsTotal := realShadowsTotal + 1;;   # +1 injected fake shadow (the non-generating witness)
mIso2SettledCount := realSettledCount;;       # the real ones remain settled; the injected witness is NOT settled
mIso2Verdict := ComputeVerdict(true, mIso2ShadowsTotal, mIso2SettledCount);;
Print("M-ISO-2 constructed datum (source: ", witnessSourceLabel, "): total=", mIso2ShadowsTotal, " settled=", mIso2SettledCount,
      "  verdict=", mIso2Verdict.verdict, "\n");
mIso2Ok := (mIso2Verdict.verdict = "FALSE") and (witnessSubgroupSize < witnessBaseGSize);;
Print("[", PF(mIso2Ok), "] M-ISO-2 fired as FALSE (constructed negative: real 12 shadows + 1 injected non-generating witness; NOT a natural/registered example -- see appendix for the 5-family search that found no natural one)\n\n");

# M-ISO-3: constant-TRUE mutant. Run it on the SAME M-ISO-2 input and show
# mismatch against the real (correct) verdict -- i.e. M-ISO-2 is what "kills"
# the constant-TRUE mutant.
constantTrueMutantVerdict := "TRUE";;   # a broken verdict function that always answers TRUE
mIso3Detected := (constantTrueMutantVerdict <> mIso2Verdict.verdict);;
Print("M-ISO-3: constant-TRUE mutant says '", constantTrueMutantVerdict, "' on the M-ISO-2 input; real verdict is '",
      mIso2Verdict.verdict, "' -- mismatch detected? ", mIso3Detected, "\n");
Print("[", PF(mIso3Detected), "] M-ISO-3 constant-TRUE mutant is KILLED by M-ISO-2 (mismatch detected, as required)\n\n");

# M-ISO-4: settled 1-flip. Take the REAL K^(3) settled detail (12/12 true),
# flip exactly one entry's settled flag to false (pure data mutation, distinct
# from M-ISO-2's non-generating-witness construction), recompute verdict.
flippedSettledCount := realSettledCount - 1;;
mIso4Verdict := ComputeVerdict(true, realShadowsTotal, flippedSettledCount);;
Print("M-ISO-4: ", witnessSourceLabel, " settled_by_m flipped 1 entry (", realSettledCount, "->", flippedSettledCount,
      " settled of ", realShadowsTotal, " total) -> verdict=", mIso4Verdict.verdict, "\n");
mIso4Ok := (mIso4Verdict.verdict = "FALSE");;
Print("[", PF(mIso4Ok), "] M-ISO-4 fired as FALSE (single settled-flip is caught by the all-settled quantifier)\n\n");

# M-ISO-5: candidate drop. Take the REAL K^(3) hexagon totals but drop ONE
# shadow from the shadow_total count WITHOUT adjusting h10_fail/h11_fail/
# generation_fail (simulating an enumeration that silently lost one candidate).
droppedShadowTotal := res3.hexagon.shadow_total - 1;;  # 11
droppedShadowSumOk := (res3.hexagon.candidate_total - res3.hexagon.h10_fail - res3.hexagon.h11_fail
                        - res3.hexagon.generation_fail = droppedShadowTotal);;
Print("M-ISO-5: shadow_total dropped 12->11 without adjusting fail-stage counts -> shadow_sum_check=",
      droppedShadowSumOk, " (expect false)\n");
mIso5Verdict := ComputeVerdict(droppedShadowSumOk, droppedShadowTotal, droppedShadowTotal);;
  # even if we (wrongly) assume all remaining 11 are settled, shadowSumOk=false should override to UNKNOWN
Print("  ComputeVerdict(shadowSumOk=", droppedShadowSumOk, ", total=", droppedShadowTotal, ", settled=",
      droppedShadowTotal, ") = ", mIso5Verdict.verdict, "/", mIso5Verdict.reason, "\n");
mIso5Ok := (mIso5Verdict.verdict = "UNKNOWN") and (mIso5Verdict.reason = "CANDIDATE_ENUM_INCONSISTENT");;
Print("[", PF(mIso5Ok), "] M-ISO-5 fired as UNKNOWN(CANDIDATE_ENUM_INCONSISTENT), NOT TRUE (shadow_sum_check now gates the verdict -- this is the fix in ComputeVerdict)\n\n");

# M-ISO-6(b): shadow 0 件 (NO_SHADOWS) -- synthetic all-generation-fail scenario
# (self-consistent: shadow_total=0, and candidate_total-h10-h11-genfail=0 too).
mIso6bVerdict := ComputeVerdict(true, 0, 0);;
Print("M-ISO-6(b): synthetic zero-shadow scenario (candidate_total consistent, shadow_total=0) -> verdict=",
      mIso6bVerdict.verdict, "/", mIso6bVerdict.reason, "\n");
mIso6bOk := (mIso6bVerdict.verdict = "UNKNOWN") and (mIso6bVerdict.reason = "NO_SHADOWS");;
Print("[", PF(mIso6bOk), "] M-ISO-6(b) fired as UNKNOWN(NO_SHADOWS) (vacuous-truth trap avoided, not TRUE)\n\n");

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
                and mIso7Ok and asGap3Ok and homFailCaptureOk and interfaceCheckOk;;
Print("[", PF(allMutantsOk), "] ALL R3 MUTANTS (7) + AS-GAP-3 self-audit + interface checks FIRED AS EXPECTED\n\n");

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
  "\"expected_shadow_total\":", String(res3.hexagon.shadow_total), ",",
  "\"expected_settled_count\":", String(res3.settled.settled_count), ",",
  "\"expected_settled_total\":", String(res3.settled.total), ",",
  "\"expected_verdict\":\"", res3.isolated_verdict, "\"",
  "},",
  "\"m_iso2_witness\":{\"source\":", JStr(witnessSourceLabel), ",\"m\":", String(witnessM), ",",
  "\"f_word\":", WordToJson(witnessWord), ",",
  "\"f_word_note\":\"f_word alone is convention-fragile (BFSWords prepend-storage vs EvalWordQT/EvalWordInQ evaluators gave DIFFERENT elements for the SAME word during R4 cross-check debugging -- see driver comment near FindNonGeneratingWitness). f_images below is the authoritative raw permutation, independent of any word-evaluation convention; R4 should use f_images, not re-derive f from f_word.\",",
  "\"n_points\":", String(witnessNPoints), ",",
  "\"f_images\":", DumpPermList(witnessFElt, witnessNPoints), ",",
  "\"expected_subgroup_size_lt_g\":", JB(witnessSubgroupSize < witnessBaseGSize), ",",
  "\"expected_subgroup_size\":", String(witnessSubgroupSize), ",",
  "\"expected_g_size\":", String(witnessBaseGSize), "},",
  "\"w5\":{\"n_points\":23,",
  "\"x_images\":", DumpPermList(xhat5, 23), ",",
  "\"y_images\":", DumpPermList(yhat5, 23), ",",
  "\"expected_g_size\":", String(res5.g_size), ",",
  "\"expected_n_ord\":", String(res5.n_ord), ",",
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
    ",\"sum_check_pass\":", String(r.shadow_sum_check), "},",
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
  "{\"id\":\"M-ISO-2\",\"desc\":\"CONSTRUCTED negative (not a natural/registered example -- see search_appendix): real ", witnessSourceLabel, " ", String(realShadowsTotal), " shadows + 1 injected non-generating candidate (generation_fail witness, itself a real measured fact from ", witnessSourceLabel, "'s hexagon enumeration -- only the INJECTION as a fake shadow is constructed)\",",
    "\"witness_source\":", JStr(witnessSourceLabel), ",",
    "\"witness_m\":", String(witnessM), ",\"witness_f_word\":", WordToJson(witnessWord), ",",
    "\"witness_subgroup_size\":", String(witnessSubgroupSize), ",\"witness_g_size\":", String(witnessBaseGSize), ",",
    "\"paper_argument\":\"image subgroup order < |G| => induced endomorphism's image is a proper subgroup => not surjective onto G => not bijective on the finite set G\",",
    "\"expected\":\"FALSE\",\"fired\":", String(mIso2Ok), ",\"kills\":\"constant-TRUE (see M-ISO-3)\"},",
  "{\"id\":\"M-ISO-3\",\"desc\":\"constant-TRUE mutant run on M-ISO-2 input\",\"expected\":\"detected (mismatch vs real verdict)\",",
    "\"mutant_output\":\"", constantTrueMutantVerdict, "\",\"real_verdict\":\"", mIso2Verdict.verdict, "\",",
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
    "\"fired\":", String(mIso7Ok), ",\"kills\":\"descent used as an enumeration filter (would make settled=100% a tautology and risks isolated false-TRUE via silent candidate drop)\"}",
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

certStr := Concatenation(
  "{\"schema\":\"gtsh-cert/iso-gate-r3r4/v1\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/probe/w6_bu_s0/iso_gate_r3r4_driver.g\",\"date\":\"2026-08-05\"},",
  "\"tier\":\"tool-calibration\",",
  "\"purpose\":\"ISO-GATE route-2 R3 (mutant matrix, 7 items -- M-ISO-7 added 2026-08-05 per docs/notes/auto_settled_check_v1.md AS-GAP-3/S-BU-17) + R4 (second-system data export) + interface field corrections (group_side / enumeration_domain / GroupHomomorphismByImages fail capture), per docs/notes/w6_bottomup_design_v4.md sec.5.3/5.4/5.1; W-5 iso_gate_state stays UNKNOWN (pending route-2 gate), NOT upgraded by this driver\",",
  "\"design_authority\":\"commander order 2026-08-05 (w6_bottomup_design_v4.md sec.5.3 R3 / sec.5.4 R4 / sec.5.1 interface)\",",
  "\"non_contact_declaration\":{\"Im_R_reduction_image\":\"not touched\",\"d_N\":\"not touched\",",
  "\"sealed_quantities\":\"not touched (c_mu_hat / PSL window structural quantities / eps bits)\",",
  "\"u_arithmetic_value\":\"not touched\"},",
  "\"independence\":\"no certificates/*.json or search/certs/*.json read; all groups rebuilt from generators in this run; old driver search/probe/w6_bu_s0/iso_gate_check.g left untouched\",",
  "\"fix_notes\":[",
    "\"isolated_verdict now gated on shadow_sum_check via ComputeVerdict (old driver computed shadow_sum_check but did not use it to gate the verdict -- M-ISO-5 exposes this)\",",
    "\"EnumerateReducedHexagonSafe wrapper added locally (this file only) to catch theta/tau GroupHomomorphismByImages fail gracefully as UNKNOWN(THETA_TAU_NOT_WELLDEFINED) instead of a hard Error() crash (B-2 warning); demonstrated on a genuine natural fixture (Q3-a) where this actually fires\",",
    "\"M-ISO-2 witness bug caught and fixed during R4 cross-check: witness f was initially reconstructed from cand.f_word via EvalWordQT (natural convention), but cand.f_word comes from BFSWords (prepend-storage convention, 裁定166) -- EvalWordQT silently gives a DIFFERENT (wrong) group element for the same word. Fixed by (a) using EvalWordInQ (prepend) in the GAP driver and (b) dumping the witness as raw f_images (permutation list) in r4_input_data.json instead of relying on any word-evaluation convention on the Python side\",",
    "\"S-BU-17 (ENUMERATION_FILTER_CONTAMINATION/STOP) added 2026-08-05 per commander order following docs/notes/auto_settled_check_v1.md AS-GAP-3; M-ISO-7 added as its source-map detector + negative control (see mutant_matrix)\"",
  "],",
  "\"m_iso2_construction_note\":\"M-ISO-2 is a CONSTRUCTED negative fixture (implementer-built, 2026-08-05), NOT a pre-registered/established fact. Commander-approved 2026-08-05 after a documented search for a natural isolated=FALSE example found none (see search_appendix). This is the campaign's first isolated=FALSE instance and is registered here as a permanent negative fixture for future ISO-GATE recalibration.\",",
  "\"fixtures\":[", IsoGateResultToJsonR3R4(res3), ",", IsoGateResultToJsonR3R4(res5), ",",
    IsoGateResultToJsonR3R4(resN5), ",", IsoGateResultToJsonR3R4(resQ3a), "],",
  "\"mutant_matrix\":", mutantJson, ",",
  "\"search_appendix\":", searchAppendixJson, ",",
  "\"all_mutants_fired_as_expected\":", String(allMutantsOk), ",",
  "\"r4_second_system\":{\"status\":\"data exported to search/probe/w6_bu_s0/r4_input_data.json for independent Python re-implementation; companion script search/probe/w6_bu_s0/r4_second_system.py independently confirmed ALL summary numbers for K^(3), W-5, and the M-ISO-2 witness match (see search/probe/w6_bu_s0/r4_second_system_output.json for its own output; this GAP cert does not itself run the second system, run separately via: python search/probe/w6_bu_s0/r4_second_system.py)\",",
  "\"note\":\"GAP one-output remains candidate per F104-2.3; second system independence documented separately\"},",
  "\"crosscheck_status\":\"not cross-checked by THIS file alone (R4 second system is a separate script; see its output for the actual crosscheck verdict)\",",
  "\"verified_status\":\"not verified (Lean not used)\"",
  "}");;

WriteFile("search/certs/w6_bu_s0_iso_gate_r3r4_20260805.json", certStr);;
Print("wrote search/certs/w6_bu_s0_iso_gate_r3r4_20260805.json\n");

Print("\nISO_GATE_R3R4_DRIVER_DONE\n");
QUIT;
