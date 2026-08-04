#############################################################################
## search/probe/w6_bu_s0/iso_gate_check.g
## ISO-GATE 較正 driver: 任意の marked datum(BOTTOM-UP v3 の MARK-ISO 型 --
## rho: PB3 -> P_hat と V=ker(pi) の指定)を入力に、isolated 判定手続きを
## 汎用に走らせる。
##
## 委嘱: 司令塔(2026-08-05)。位置づけ: docs/notes/w6_bottomup_design_v3.md
##   §4【blocker 4】ISO-GATE(fail-closed) -- 【BU-GAP-8】(isolated 判定手続き
##   そのものが未設計。ISO-GATE は fail-closed の受け皿であって判定器ではない
##   -- 実質的な次の律速)。本ファイルはその判定器の較正版プロトタイプの
##   汎用化(「道具の較正のみ」-- 実窓への適用は掘削認可後)。
##
## 出自(逐語一般化の系譜): 元実装は
##   search/probe/wac_v1/w5_isolated_check_20260805.g(裁定482、W-5窓で
##   isolated=TRUE を出した検証済み手順)。settled 判定・EnumerateReducedHexagon
##   の quotient-shortcut・AbstractProd 規約は search/week3-battery-common.g
##   から逐語再利用(本ファイル独自の新規アルゴリズムは無い)。
##
## 定義(docs/notes/ihnec_v1.md より、再定義しない):
##   settled: shadow (m,f) について ker(T_{m,f}) = N。
##   isolated: GT(N) の全 shadow が settled ⇒ GT(N)=GTSh(N,N) は有限群。
##   運用定義(w5_isolated_check_20260805.g / k5_genuine_campaign_v1.md
##   §5.2 段 K5-8 と同一): 各 shadow で x -> x^u, y -> f^-1 y^u f
##   (u=2m+1) が Aut(P_N) に延びるか。
##
## 入力(marked datum の GAP 実現) -- MarkedDatumFromGroup(Ghat, xElt, yElt, cElt):
##   Ghat: 任意の GAP 群(fp 表現・pc 表現・permutation いずれでも可。
##     fp/pc は内部で IsomorphismPermGroup により permutation 表現へ変換
##     してから使う -- EnumerateReducedHexagon の BFS/DerivedSubgroup が
##     permutation 群を前提に組まれているため、逐語再利用の範囲を守る)。
##   xElt/yElt/cElt: rho(sigma1), rho(sigma2), rho(c=Delta^2) を Ghat の
##     元として渡す(呼び出し側が語を評価してから渡す -- 本ファイルは
##     語評価器を持たない)。
##   c_in_N 前提(quotient-shortcut の正当性条件): cElt = Identity(Ghat)。
##   違反時は判定せず ISO_UNKNOWN(reason=C_NOT_IN_N)を返す(fail-closed)。
##
## 罠 12 件の遵守(sol/裁定_01_definition_gate.md):
##   - 指数一致(N_ord/charming_set の一致)を settled 証明に使わない --
##     settled は個別 shadow ごとに GroupHomomorphismByImages+IsBijective
##     で直接判定する(既存実装のまま、ショートカットを増設しない)。
##   - m の法(N_ord = Lcm(Order(x),Order(y)))と u の法(2n、u=2m+1 は
##     shadow の charming 指数であって別物)を混同しない -- N_ord は本
##     ファイル内でその都度 qrec から再計算する(外部から法として受け
##     取らない)。
##   - GAP の部分群比較でなく marked factor map を使う -- settled 判定は
##     GroupHomomorphismByImages による準同型構成そのもので判定し、
##     IsSubgroup 等の比較には依らない。
##
## ISO-GATE 接続欄(docs/notes/w6_bottomup_design_v3.md §4.2 定義 ISO-GATE):
##   ISO(D) in {PROVEN, UNKNOWN}, 既定 UNKNOWN。PROVEN を付けてよいのは
##   (1) ker(rho) = K^(n) の形(Thm 4.3 ショートカット)、または
##   (2) isolated 判定の専用手続きが設計・較正され、その cert が PASS を
##   出した場合(意味論の新設と発効判定は司令塔検問+Sol ゲートの職掌 --
##   本 driver は「専用手続きの候補」を提供するだけで、自分の TRUE 判定を
##   自動的に PROVEN へ格上げしない)。従って本ファイルの
##   iso_gate_state フィールドは、ker=K^(n) ショートカットが成立する
##   場合にのみ "PROVEN" とし、それ以外は driver の isolated_verdict が
##   TRUE であっても "UNKNOWN (pending commander/Sol gate)" のままとする。
##
## 非接触宣言: Im R・d_N・封印3量(c_mu-hat / PSL窓の構造量 / epsilon bits)・
##   u値(u_{n,alpha} 型の算術量)は入力にも出力にも含めない。
## 独立性: certificates/*.json / search/certs/*.json は一切読まない。
##   全群は GAP で生成器から新規構築する。
## 規律: gap.ps1 経由・-o 2g・AbstractProd 規約。実窓(列挙由来)への適用は
##   掘削認可後 -- 本ファイルは fixture 2 本の較正のみ実行する。
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/week3-battery-common.g");;

Print("=== ISO-GATE calibration driver (search/probe/w6_bu_s0/iso_gate_check.g) ===\n");
Print("(汎用手続き -- 実窓非接触。本走行は fixture 2 本の較正のみ)\n\n");

#############################################################################
## MarkedDatumFromGroup: 任意の GAP 群 + marked 生成元像 -> qrec(x,y,c,G)
## (permutation 表現へ正規化。c_in_N 前提のチェックは呼び出し側の責務 --
##  IsoGateCheck 内で改めて検査する)
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

#############################################################################
## settled 判定ヘルパー(w5_isolated_check_20260805.g SettledCheck の逐語
## 一般化 -- ロジック不変、識別子のみ整理)
#############################################################################
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
## IsoGateCheck: 汎用 isolated 判定手続き本体。
##   qrec: rec(x,y,c,G) (MarkedDatumFromGroup の出力、または既に perm 表現の
##     ものを直に渡してもよい -- fixture では既存の qrec 構成を逐語流用する)
##   label: cert 用のラベル文字列
##   kerIsKn: fail、または整数 n(ker(rho)=K^(n) が既知の場合。Thm 4.3
##     ショートカットで ISO-GATE PROVEN を出す唯一の経路。列挙結果と無矛盾
##     であることをここでは assert しない -- 呼び出し側が事前登録する値。
##     本ファイルの fixture 呼び出しでは K^(3) に対し 3 を渡す)
## 戻り値: rec(label, kerIsKn, precondition_ok, g_size, n_ord, charming_set,
##   charming_set_size, hexagon(candidate_total 等), settled(count/total/detail),
##   settled_by_m, isolated_verdict in {"TRUE","FALSE","UNKNOWN"},
##   unknown_reason(""|"C_NOT_IN_N"|"NO_SHADOWS"), iso_gate_state
##   in {"PROVEN","UNKNOWN"}, time_ms(...))
#############################################################################
IsoGateCheck := function(qrec, label, kerIsKn)
  local precheck, nOrd, charmingSet, t0, t1, tHex, hexResult, shadowSumOk,
        tSettled, settled, settledByM, verdict, unknownReason, isoGateState,
        timeHex, timeSettled;
  precheck := (qrec.c = Identity(qrec.G));
  if not precheck then
    return rec(label:=label, kerIsKn:=kerIsKn, precondition_ok:=false,
      g_size:=Size(qrec.G), n_ord:=fail, charming_set:=[], charming_set_size:=0,
      hexagon:=fail, settled:=fail, settled_by_m:=[],
      isolated_verdict:="UNKNOWN", unknown_reason:="C_NOT_IN_N",
      iso_gate_state:="UNKNOWN", time_ms_hexagon:=0, time_ms_settled:=0);
  fi;

  # 罠回避: N_ord は法(m の法)。qrec からその都度再計算し、u=2m+1(shadow 側の
  # charming 指数)とは別の量として扱う(混同しない -- コメント冒頭参照)。
  nOrd := Lcm(Order(qrec.x), Order(qrec.y));
  charmingSet := Filtered([0..nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);

  t0 := Runtime();;
  hexResult := EnumerateReducedHexagon(qrec, charmingSet);;
  t1 := Runtime();;
  timeHex := t1 - t0;

  shadowSumOk := (hexResult.candidate_total - hexResult.h10_fail - hexResult.h11_fail
                  - hexResult.generation_fail = hexResult.shadow_total);

  t0 := Runtime();;
  settled := SettledCheckGeneral(qrec, hexResult.shadows);;
  t1 := Runtime();;
  timeSettled := t1 - t0;

  settledByM := List(charmingSet, mVal -> CountByMGeneral(settled.detail, mVal));

  if settled.total = 0 then
    verdict := "UNKNOWN"; unknownReason := "NO_SHADOWS";
  elif settled.settled_count = settled.total then
    verdict := "TRUE"; unknownReason := "";
  else
    verdict := "FALSE"; unknownReason := "";
  fi;

  # ISO-GATE 接続: PROVEN は ker(rho)=K^(n) ショートカット経由のみ。
  # driver 自身の TRUE 判定は自動で PROVEN に格上げしない
  # (意味論の発効判定は司令塔検問+Sol ゲートの職掌、docs/notes/
  #  w6_bottomup_design_v3.md §4.2 定義 ISO-GATE (2))。
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
    isolated_verdict:=verdict, unknown_reason:=unknownReason,
    iso_gate_state:=isoGateState,
    time_ms_hexagon:=timeHex, time_ms_settled:=timeSettled);
end;;

#############################################################################
## JSON 化ヘルパー(cert 出力用。既存 helper JStr/JB/JArr は
## week3-battery-common.g から再利用。以下は本 driver 固有の組み立てのみ)
#############################################################################
IsoGateResultToJson := function(r)
  local notSettledJson, settledByMJson, sd, base;
  if not r.precondition_ok then
    return Concatenation(
      "{\"label\":", JStr(r.label), ",",
      "\"precondition_ok\":false,",
      "\"g_size\":", String(r.g_size), ",",
      "\"isolated_verdict\":\"UNKNOWN\",",
      "\"unknown_reason\":\"C_NOT_IN_N\",",
      "\"iso_gate_state\":\"UNKNOWN\"",
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
    "\"charming_set\":", JArr(List(r.charming_set,String)), ",",
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
    "\"time_ms_hexagon_enum\":", String(r.time_ms_hexagon), ",",
    "\"time_ms_settled_check\":", String(r.time_ms_settled),
    "}");
  return base;
end;;

#############################################################################
## FIXTURE 1: K^(3) 単体(isolated 既知 -- Thm 4.3 / campaign アンカーA4)
## 逐語出自: w5_isolated_check_20260805.g の fixture ブロック
#############################################################################
Print("--- FIXTURE 1: K^(3) (isolated 既知 -- Thm 4.3, ker(rho)=K^(3)) ---\n");
gn3 := MakeGn(3);;
datum3 := MarkedDatumFromGroup(gn3.G, gn3.x, gn3.y, ());;
Print("|G3| = ", Size(datum3.G), "  (expect 108)\n");

res3 := IsoGateCheck(datum3, "FIXTURE-K3", 3);;
Print("precondition_ok=", res3.precondition_ok, "  N_ord=", res3.n_ord, "  (expect 6)\n");
Print("charming_set(K3) = ", res3.charming_set, "\n");
Print("shadow_total=", res3.hexagon.shadow_total, "  (campaign K5-4 frozen |GT(K^(3))|: expect 12)\n");
Print("settled: ", res3.settled.settled_count, "/", res3.settled.total, "\n");
Print("isolated_verdict=", res3.isolated_verdict, "  iso_gate_state=", res3.iso_gate_state, "\n");

fixture1Ok := res3.precondition_ok and (Size(datum3.G) = 108) and (res3.n_ord = 6)
              and (res3.hexagon.shadow_total = 12) and (res3.settled.total = 12)
              and (res3.settled.settled_count = 12) and (res3.isolated_verdict = "TRUE")
              and (res3.iso_gate_state = "PROVEN");;
Print("[", PF(fixture1Ok), "] FIXTURE-1 PASS (driver reproduces K^(3) known values via general path)\n\n");

#############################################################################
## FIXTURE 2: W-5 = K^(5) cap N_Q(裁定482 の再現 -- 数値一致 assert)
## 逐語出自: w5_isolated_check_20260805.g 本測定ブロック(scratchpad/
## w5_order_check.g と同一構成パターン)
#############################################################################
Print("--- FIXTURE 2: W-5 = K^(5) cap N_Q (裁定482 再現) ---\n");
gn5 := MakeGn(5);;
q8rec := MakeQ8();;
xhat5 := PermList(Concatenation(List([1..15], j -> j^gn5.x), List([1..8], j -> 15 + (j^q8rec.x))));;
yhat5 := PermList(Concatenation(List([1..15], j -> j^gn5.y), List([1..8], j -> 15 + (j^q8rec.y))));;
QW5 := Group(xhat5, yhat5);;
datum5 := MarkedDatumFromGroup(QW5, xhat5, yhat5, ());;
Print("|PB3/N| = ", Size(datum5.G), "  (裁定473: expect 1000)\n");

res5 := IsoGateCheck(datum5, "FIXTURE-W5", fail);;
Print("precondition_ok=", res5.precondition_ok, "  N_ord=", res5.n_ord, "  (裁定473 erratum: expect 20)\n");
Print("charming_set(W-5) size = ", res5.charming_set_size, "  (erratum expect 16)\n");
Print("hexagon: candidate_total=", res5.hexagon.candidate_total, " h10_fail=", res5.hexagon.h10_fail,
      " h11_fail=", res5.hexagon.h11_fail, " generation_fail=", res5.hexagon.generation_fail,
      " shadow_total=", res5.hexagon.shadow_total, "\n");
Print("settled: ", res5.settled.settled_count, "/", res5.settled.total,
      "  time_ms(hexagon)=", res5.time_ms_hexagon, "  time_ms(settled)=", res5.time_ms_settled, "\n");
Print("isolated_verdict=", res5.isolated_verdict, "  iso_gate_state=", res5.iso_gate_state, "\n");

fixture2Ok := res5.precondition_ok and (Size(datum5.G) = 1000) and (res5.n_ord = 20)
              and (res5.charming_set_size = 16) and res5.shadow_sum_check
              and (res5.isolated_verdict = "TRUE");;
Print("[", PF(fixture2Ok), "] FIXTURE-2 PASS (driver reproduces 裁定482 W-5 isolated=TRUE via general path)\n\n");

driverOk := fixture1Ok and fixture2Ok;;
Print("[", PF(driverOk), "] DRIVER OVERALL (both fixtures reproduce known/registered values)\n\n");

#############################################################################
## 時間見積り(位数8000帯・extrapolation のみ -- 実走はしない)
## 観測: |G|=108(K3) と |G|=1000(W-5) の time_ms(hexagon enum) から、
## コストは概ね candidate_total = |Dwords| * |charming_set| に比例し、かつ
## 群演算(Group(genA,genB) の Size 計算による surj 判定)1 回あたりのコストは
## |G| とともに増える(backtrack のコストは |G| に依存)。したがって
## |G|=8000 帯(W-5比 8倍)での実用時間は「少なくとも」candidate_total 比の
## 線形外挿より重いと見るのが安全側 -- 本 driver は上限を保証する測定を
## 行っていないので、ここでの数字は事前登録された予言ではなく単なる目安。
#############################################################################
Print("--- 時間見積り(位数8000帯、extrapolation のみ・実走なし) ---\n");
ratioG := 8000 / Size(datum5.G);;
ratioCandidate := (function()
    if res5.hexagon.candidate_total = 0 then return 0; else
      return ratioG; fi;
  end)();;
estLow_hex := res5.time_ms_hexagon * ratioG;;
estLow_settled := res5.time_ms_settled * ratioG;;
Print("W-5 (|G|=", Size(datum5.G), ") 実測: time_ms_hexagon=", res5.time_ms_hexagon,
      " time_ms_settled=", res5.time_ms_settled, "\n");
Print("線形外挿(|G| 比 x", ratioG, ", 安全側の下限目安 -- 上限ではない): ",
      "hexagon ~= ", estLow_hex, "ms, settled ~= ", estLow_settled, "ms\n");
Print("注意: 群位数比の線形外挿は下限目安に過ぎない。EnumerateReducedHexagon の\n");
Print("  内側ループの Size(Group(genA,genB)) 呼び出しは backtrack ベースで、\n");
Print("  |G| が大きくなるほど 1 回あたりのコストも増える可能性が高い\n");
Print("  (超線形になり得る) -- 実用時間の確定には位数8000帯 fixture の\n");
Print("  実測が別途必要(本委嘱の範囲外。委嘱は較正のみ)。\n\n");

#############################################################################
## cert 出力
#############################################################################
certStr := Concatenation(
  "{\"schema\":\"gtsh-cert/iso-gate-check-driver/v1\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/probe/w6_bu_s0/iso_gate_check.g\",\"date\":\"2026-08-05\"},",
  "\"tier\":\"tool-calibration\",",
  "\"purpose\":\"generalize w5_isolated_check_20260805.g into a reusable ISO-GATE calibration driver over arbitrary marked data (docs/notes/w6_bottomup_design_v3.md sec.4 BU-GAP-8); calibration only, no real-window drilling in this run\",",
  "\"design_authority\":\"commander order 2026-08-05 (BOTTOM-UP v3 MARK-ISO datum -> general iso_gate_check.g driver)\",",
  "\"non_contact_declaration\":{\"Im_R_reduction_image\":\"not touched\",\"d_N\":\"not touched\",",
  "\"sealed_quantities\":\"not touched (c_mu_hat / PSL window structural quantities / eps bits)\",",
  "\"u_arithmetic_value\":\"not touched\"},",
  "\"independence\":\"no certificates/*.json or search/certs/*.json read; all groups rebuilt from generators in this run\",",
  "\"traps_observed\":[",
    "\"exponent-agreement (N_ord/charming_set match) not used as settled proof -- settled decided per-shadow via GroupHomomorphismByImages+IsBijective\",",
    "\"m-modulus (N_ord) vs u-modulus (2n, shadow charming exponent) kept distinct, N_ord recomputed per-datum, never taken as external input\",",
    "\"marked factor map (GroupHomomorphismByImages) used for settled decision, not GAP subgroup comparison\"",
  "],",
  "\"iso_gate_semantics_note\":\"iso_gate_state=PROVEN only fires via ker(rho)=K^(n) Thm4.3 shortcut (route 1). A driver isolated_verdict=TRUE on a non-K^(n) datum does NOT auto-promote to PROVEN -- that promotion (ISO-GATE route 2) is commander/Sol gate territory, out of this tool's authority\",",
  "\"fixtures\":[", IsoGateResultToJson(res3), ",", IsoGateResultToJson(res5), "],",
  "\"fixture1_pass\":", String(fixture1Ok), ",",
  "\"fixture2_pass\":", String(fixture2Ok), ",",
  "\"driver_overall_pass\":", String(driverOk), ",",
  "\"time_estimate_order8000\":{\"basis\":\"linear extrapolation on |G| ratio from W-5 fixture (|G|=1000), labeled as a lower-bound-only guess, NOT a measured guarantee\",",
  "\"w5_g_size\":", String(Size(datum5.G)), ",",
  "\"w5_time_ms_hexagon\":", String(res5.time_ms_hexagon), ",",
  "\"w5_time_ms_settled\":", String(res5.time_ms_settled), ",",
  "\"ratio_to_8000\":", String(ratioG), ",",
  "\"linear_extrapolation_ms_hexagon\":", String(estLow_hex), ",",
  "\"linear_extrapolation_ms_settled\":", String(estLow_settled), ",",
  "\"caveat\":\"per-candidate cost (Size(Group(genA,genB)) backtrack) likely grows with |G|, so true cost at order 8000 is expected to exceed this linear figure -- a dedicated order~8000 fixture run is needed for a real measurement, out of this order's scope\"},",
  "\"crosscheck_status\":\"not cross-checked (single GAP implementation; no independent crosscheck/ implementation run against this cert)\",",
  "\"verified_status\":\"not verified (Lean not used)\"",
  "}");;

WriteFile("search/certs/w6_bu_s0_iso_gate_check_driver_20260805.json", certStr);;
Print("wrote search/certs/w6_bu_s0_iso_gate_check_driver_20260805.json\n");

Print("\nISO_GATE_CHECK_DRIVER_DONE\n");
QUIT;
