#############################################################################
## search/probe/wac_v1/w5_isolated_check_20260805.g
## 【W5-GAP-1】= W-5 窓(N := K^(5) cap N_Q)の isolated 性の機械検査。
##
## 委嘱: 司令塔(2026-08-05)。位置づけ: docs/notes/ideas_020_review_v1.md
##   §4.6 【W5-GAP-1】(isolated 未確認・d(W-5)=5 はその条件つき結論)。
##   窓の構成・数値正本: 裁定473(scratchpad/w5_order_check.g の実測 --
##   |PB3/N|=1000, N_ord=20, |X_N|=16)。
##
## 定義(docs/notes/ihnec_v1.md より、再定義しない):
##   settled: shadow (m,f) について、ker(T_{m,f}) = N。
##   isolated: GT(N) の全 shadow が settled ⇒ GT(N)=GTSh(N,N) は有限群。
##   運用定義(k5_genuine_campaign_v1.md §5.2 段 K5-8 と同一):
##     各 shadow で x -> x^u, y -> f^-1 y^u f (u=2m+1) が Aut(PB3/N) に
##     延びるか。fail 0 なら isolated、fail>0 なら isolated でない。
##   (この運用定義は search/week3-psl-common.g の RunPSLWindow の settled
##    witness search と同一系統 -- ただし W-5 には PGL(2,q) のような既知の
##    明示 Aut() 元リストが無いため、GAP の GroupHomomorphismByImages +
##    IsBijective で「Aut(P_N) に延びるか」を直接判定する。この関数は
##    week3-battery-common.g の EnumerateReducedHexagon 内の thetaHom/tauHom
##    構成と同じ GAP 機構であり、本ファイル独自の新規アルゴリズムではない)。
##
## 手順: N の GT(N) を transversal-cocycle モデル(week3-battery-common.g の
##   EnumerateReducedHexagon = quotient-shortcut 実装。c_in_N=true な窓では
##   これが正しい実装であることは既に週3 battery/PSL 群で確立済み)で全列挙
##   -> 全 shadow で settled 判定 -> isolated か。
##   BuildQTGeneral (12-rule Q x T モデル、docs/wp2-transversal-model.md)も
##   week3-psl-common.g の RunPSLWindow と同じく braid 関係の頑健性チェック
##   として併走させる(shadow 判定そのものには使わない -- 判定は quotient-
##   shortcut 側、これも RunPSLWindow と同じ役割分担)。
##
## 事前登録(コード外の予言をここに明記):
##   isolated: UNKNOWN (予言しない -- 本検査は前提検査であり、d(W-5)=5 の
##   結論そのものを検査するものではない)。
##
## fixture(A5-CONV型・先行必須): K^(3) 単体。Thm 4.3(2405.11725)により
##   全 n>=3 で K^(n) は isolated と保証されている基準対象であり、かつ
##   k5_genuine_campaign_v1.md §5.2 アンカーA4(K5-4)の凍結値
##   |GT(K^(3))|=12(= Thm 4.6 の式 2*n0*phi(n0), n0=3, alpha=0 の値。
##   本スクリプトの shadow_total フィールドがこれに対応する)と照合できる。
##   この fixture が FAIL したら規約バグの疑いがあるため本検査(W-5 の実測)
##   へは進まない。
##
## 非接触宣言: Im R(K^(5) への還元像)・d_N・封印3量(c_mu-hat / PSL窓の
##   構造量 / epsilon bits)・u値(u_{5,alpha} 型の算術量。本ファイルの
##   ローカル変数 u=2m+1 は shadow の charming 指数であり、別物 --
##   k5_genuine_campaign_v1.md 冒頭 erratum N-1 の記号衝突注意と同じ区別)
##   は入力にも出力にも含めない。isolated 判定に必要な範囲を越える量が
##   要ると分かった場合は停止して司令塔へ上申する(このスクリプトは実際
##   そこまで到達しなかった -- 全量、有限群論の範囲内で完結した)。
##
## 独立性: certificates/*.json / search/certs/*.json は一切読まない。
##   PB3/K^(5)・PB3/N_Q ともに GAP で生成器から新規構築する
##   (search/week3-battery-common.g の MakeGn/MakeQ8 は共有ヘルパーとして
##   逐語再利用 -- scratchpad/w5_order_check.g と同一パターン)。
##
## 規律: gap.ps1 経由・-o 2g。乗算規約 AbstractProd
##   (week3-battery-common.g の EnumerateReducedHexagon を逐語利用)。
##   (GAP のトップレベルスクリプトは if ブロック内で QUIT を使えないため、
##    中断はネストした if で本体をスキップする形にし、QUIT はファイル末尾
##    1 箇所のみに置く)
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/week3-battery-common.g");;

Print("=== W5-GAP-1: N := K^(5) cap N_Q の isolated 性検査 ===\n");
Print("(事前登録: isolated = UNKNOWN -- 予言しない、前提検査)\n\n");

# ---- settled 判定ヘルパー(定義: 各 shadow (m,f) で x->x^u, y->f^-1 y^u f が
#      Aut(P_N) に延びるか。extends <=> GroupHomomorphismByImages が fail を
#      返さず、かつ得られた自己準同型が全単射) ----
SettledCheck := function(qrec, shadows)
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

CountByM := function(detailList, mVal)
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
## FIXTURE (A5-CONV型・先行必須): K^(3) 単体
##   Thm 4.3 で isolated が保証されている既知対象。campaign K5-4 アンカー
##   A4 の凍結値 |GT(K^(3))|=12 (= shadow_total) と照合してから先へ進む。
#############################################################################
Print("--- FIXTURE: K^(3) (isolated 既知 -- Thm 4.3 / campaign アンカーA4) ---\n");
gn3 := MakeGn(3);;
qrec3 := rec(x:=gn3.x, y:=gn3.y, c:=(), G:=gn3.G);;
g3Size := Size(gn3.G);;
nOrd3 := Lcm(Order(gn3.x), Order(gn3.y));;
Print("|G3| = ", g3Size, "  (expect 108)\n");
Print("K3_ord = ", nOrd3, "  (expect 6)\n");
charmingSet3 := Filtered([0..nOrd3-1], mm -> Gcd(2*mm+1, nOrd3) = 1);;
Print("charming_set(K3) = ", charmingSet3, "\n");

result3 := EnumerateReducedHexagon(qrec3, charmingSet3);;
Print("candidate_total = ", result3.candidate_total, " (T2 full-enumeration candidate count, not the anchor value)\n");
Print("h10_fail=", result3.h10_fail, " h11_fail=", result3.h11_fail,
      " generation_fail=", result3.generation_fail,
      " shadow_total=", result3.shadow_total, "  (campaign K5-4 frozen |GT(K^(3))|: expect 12)\n");

settled3 := SettledCheck(qrec3, result3.shadows);;
Print("settled: ", settled3.settled_count, "/", settled3.total, "\n");

fixtureOK := (result3.shadow_total = 12) and (settled3.total = result3.shadow_total)
             and (settled3.settled_count = settled3.total);;
Print("[", PF(fixtureOK), "] FIXTURE PASS (shadow_total=12 かつ全shadow settled)\n");

if fixtureOK then

#############################################################################
## 本測定: N := K^(5) cap N_Q (W-5)。裁定473の実測構成を逐語流用
##   (scratchpad/w5_order_check.g と同一パターン。証明書非読・新規構築)。
#############################################################################
Print("\n--- 本測定: W-5 = K^(5) cap N_Q ---\n");
gn5 := MakeGn(5);;
q8rec := MakeQ8();;

xhat := PermList(Concatenation(List([1..15], j -> j^gn5.x), List([1..8], j -> 15 + (j^q8rec.x))));;
yhat := PermList(Concatenation(List([1..15], j -> j^gn5.y), List([1..8], j -> 15 + (j^q8rec.y))));;
QW5 := Group(xhat, yhat);;
qw5Size := Size(QW5);;
Print("|PB3/N| = ", qw5Size, "  (裁定473: expect 1000)\n");

nOrdW5 := Lcm(Order(xhat), Order(yhat));;
Print("N_ord = ", nOrdW5, "  (裁定473 erratum: expect 20)\n");

constructionMatch := (qw5Size = 1000) and (nOrdW5 = 20);;

if not constructionMatch then
  Print("\n*** 構成不一致(裁定473の実測と異なる) -- 停止。 ***\n");
fi;

if constructionMatch then

qrecW5 := rec(x:=xhat, y:=yhat, c:=(), G:=QW5);;
charmingSetW5 := Filtered([0..nOrdW5-1], mm -> Gcd(2*mm+1, nOrdW5) = 1);;
Print("charming_set(W-5) = ", charmingSetW5, "  (length ", Length(charmingSetW5), ", erratum expect 16)\n");

t0 := Runtime();;
resultW5 := EnumerateReducedHexagon(qrecW5, charmingSetW5);;
t1 := Runtime();;
Print("reduced hexagon enumeration: time_ms=", t1-t0, "\n");
Print("candidate_total=", resultW5.candidate_total, " h10_fail=", resultW5.h10_fail,
      " h11_fail=", resultW5.h11_fail, " generation_fail=", resultW5.generation_fail,
      " shadow_total=", resultW5.shadow_total, "\n");

shadowSumCheckW5 := (resultW5.candidate_total - resultW5.h10_fail - resultW5.h11_fail
                      - resultW5.generation_fail = resultW5.shadow_total);;
Print("[", PF(shadowSumCheckW5), "] shadow_total 引き算整合性チェック\n");

# ---- QxT transversal model 補助チェック(braid relation robustness --
#      week3-psl-common.g の RunPSLWindow と同じ役割: 判定そのものには
#      使わず、頑健性の傍証としてのみ記録する) ----
t0 := Runtime();;
qtW5 := BuildQTGeneral(QW5, xhat, yhat, ());;
t1 := Runtime();;
braidOkW5 := (qtW5.s1*qtW5.s2*qtW5.s1 = qtW5.s2*qtW5.s1*qtW5.s2);;
Print("[", PF(braidOkW5), "] QxT braid relation (12-rule model, ", qtW5.np*6,
      " points), time_ms=", t1-t0, "\n");

# ---- settled 判定: 全 shadow について x->x^u, y->f^-1 y^u f が Aut(P_N) に
#      延びるか(GroupHomomorphismByImages + IsBijective) ----
t0 := Runtime();;
settledW5 := SettledCheck(qrecW5, resultW5.shadows);;
t1 := Runtime();;
Print("settled: ", settledW5.settled_count, "/", settledW5.total, "  time_ms=", t1-t0, "\n");

# ---- m 別内訳(charming 値ごとの settled 集計) ----
settledByM := List(charmingSetW5, mVal -> CountByM(settledW5.detail, mVal));;
Print("settled_by_m = ", settledByM, "\n");

notSettledDetail := Filtered(settledW5.detail, sd -> not sd.settled);;

isolatedW5 := "UNKNOWN";;
if settledW5.total = 0 then
  isolatedW5 := "UNKNOWN";
  Print("\n[UNKNOWN] shadow_total = 0 -- settled 判定の対象が無い。isolated は判定不能。\n");
fi;
if settledW5.total > 0 and settledW5.settled_count = settledW5.total then
  isolatedW5 := "true";
  Print("\n*** isolated = TRUE (全 ", settledW5.total, " shadow が settled) ***\n");
fi;
if settledW5.total > 0 and settledW5.settled_count <> settledW5.total then
  isolatedW5 := "false";
  Print("\n*** isolated = FALSE (settled ", settledW5.settled_count, "/", settledW5.total,
        " -- ", settledW5.total - settledW5.settled_count, " 件が not settled) ***\n");
fi;

#############################################################################
## 証明書(cert)出力
#############################################################################
notSettledJson := [];;
for sd in notSettledDetail do
  Add(notSettledJson, Concatenation("{\"m\":", String(sd.m), ",\"f_word\":", WordToJson(sd.f_word), "}"));
od;

settledByMJson := [];;
for sd in settledByM do
  Add(settledByMJson, Concatenation("{\"m\":", String(sd.m), ",\"total\":", String(sd.total),
      ",\"settled\":", String(sd.settled), "}"));
od;

certStr := Concatenation(
  "{\"schema\":\"gtsh-cert/w5-isolated-check/v1\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/probe/wac_v1/w5_isolated_check_20260805.g\",\"date\":\"2026-08-05\"},",
  "\"tier\":\"prerequisite-check\",",
  "\"target\":{\"window\":\"W-5\",\"N_definition\":\"K^(5) cap N_Q\",\"source_ruling\":\"LEDGER 473\"},",
  "\"preregistration\":{\"isolated_prediction\":\"UNKNOWN\",\"note\":\"予言しない -- 前提検査(isolated is a precondition check, not a d(W-5) prediction)\"},",
  "\"non_contact_declaration\":{\"Im_R_reduction_image\":\"not touched\",\"d_N\":\"not touched\",",
  "\"sealed_quantities\":\"not touched (c_mu_hat / PSL window structural quantities / eps bits)\",",
  "\"u_arithmetic_value\":\"not touched (u=2m+1 charming exponent used locally is a distinct object, see campaign erratum N-1)\"},",
  "\"independence\":\"no certificates/*.json or search/certs/*.json read; PB3/K^(5) and PB3/N_Q rebuilt from generators via search/week3-battery-common.g MakeGn/MakeQ8 (verbatim reuse, same pattern as scratchpad/w5_order_check.g)\",",
  "\"fixture\":{\"object\":\"K^(3)\",\"g_size\":", String(g3Size), ",\"n_ord\":", String(nOrd3),
  ",\"charming_set\":", JArr(List(charmingSet3,String)),
  ",\"candidate_total\":", String(result3.candidate_total),
  ",\"shadow_total\":", String(result3.shadow_total),
  ",\"settled_count\":", String(settled3.settled_count),
  ",\"settled_total\":", String(settled3.total),
  ",\"pass\":", String(fixtureOK),
  ",\"note\":\"campaign k5_genuine_campaign_v1.md sec.5.2 anchor A4 (K5-4) frozen |GT(K^(3))|=12 (shadow_total); Thm 4.3 asserts K^(n) isolated for all n>=3\"},",
  "\"construction\":{\"pb3_over_n_size\":", String(qw5Size), ",\"n_ord\":", String(nOrdW5),
  ",\"expected_from_ruling_473\":{\"pb3_over_n_size\":1000,\"n_ord\":20},\"match\":", String(constructionMatch), "},",
  "\"universe\":{\"charming_set\":", JArr(List(charmingSetW5,String)),
  ",\"charming_set_size\":", String(Length(charmingSetW5)), "},",
  "\"hexagon_enumeration\":{\"candidate_total\":", String(resultW5.candidate_total),
  ",\"h10_fail\":", String(resultW5.h10_fail),
  ",\"h11_fail\":", String(resultW5.h11_fail),
  ",\"generation_fail\":", String(resultW5.generation_fail),
  ",\"shadow_total\":", String(resultW5.shadow_total),
  ",\"sum_check_pass\":", String(shadowSumCheckW5), "},",
  "\"qxt_braid_relation_check\":{\"pass\":", String(braidOkW5), ",\"points\":", String(qtW5.np*6), "},",
  "\"settled_summary\":{\"settled_count\":", String(settledW5.settled_count),
  ",\"total\":", String(settledW5.total),
  ",\"settled_by_m\":", JArr(settledByMJson),
  ",\"not_settled_detail\":", JArr(notSettledJson), "},",
  "\"isolated_verdict\":\"", isolatedW5, "\",",
  "\"crosscheck_status\":\"not cross-checked (single GAP implementation; no independent crosscheck/ implementation run against this cert)\",",
  "\"verified_status\":\"not verified (Lean not used)\"",
  "}");;

WriteFile("search/certs/w5_isolated_check_20260805.json", certStr);;
Print("\nwrote search/certs/w5_isolated_check_20260805.json\n");

fi; # constructionMatch
fi; # fixtureOK

if not fixtureOK then
  Print("\nW5_ISOLATED_CHECK_ABORTED_FIXTURE_FAIL\n");
fi;

Print("\nW5_ISOLATED_CHECK_DONE\n");
QUIT;
