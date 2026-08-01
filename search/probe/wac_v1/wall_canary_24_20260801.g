#############################################################################
## search/probe/wac_v1/wall_canary_24_20260801.g
##  P5-3(発案係第17便・採択札)初動 probe: n=24 壁窓(ker chi~ = C19 x S5・
##  非可解・P-WALL-2)で複素共役カナリア ĉ(m = N_ord-1 層)を計測する。
##
##  設計版歴:
##   v1: 候補生成に kerchi-judge.g CorrectedShadowsXi の候補構成部分
##       (f0:=hRep^-1; f:=f0*c, 右剰余類)を流用し、受理判定は手書き検算式
##       (3.3)(3.4) の m 一般化に差し替えた。m=0 回帰アンカーが 120/2280 で
##       FAIL(120=|S5|、比19=N_ord)。
##   v2 (WAC-CAN-2, 裁定382): 原因確定 = 候補生成が「judge 向き」(f0=hRep^-1
##       の右剰余類)、受理が「手書き向き」(f^-1 y^u f = target を直接満たす
##       f0=hRep の左剰余類)という向き規約の混用。同型4度目の事故(教訓は
##       CV-13 として台帳鋳造・以後の新規 probe テンプレへ)。
##       修正: f0 := hRep(反転しない)・f := c*f0(左剰余類)。YImg(W,u,f) =
##       f^-1*y^u*f を単一定義し、候補生成・受理器・生成条件の3箇所全てが
##       これを呼ぶ。生成直後に向き自己検査 assert(YImg(W,u,f)=target)を
##       fail-closed で実施。
##       受理は4段: (1) HexagonHolds (3.3)(3.4) literal (2) GenerationHolds
##       (3) WD-P: GroupHomomorphismByImages(P,P,[x,y],[x^u,YImg])<>fail
##           (落ちは wd_fail_count 別欄、フィルタ)
##       (4) settled(Bq 水準 hom): フィルタにしない・別欄 settled_fail_count
##           で報告のみ(コスト予算超過時は明示 skip)。
##       前提 assert 3 点: IsNaturalAlternatingGroup(P)・charming gcd(u,Nord)=1・
##       予算 scanned=|Stab|x|C_P(y^u)|。
##       合格条件は個数一致でなく **集合等号**: Set(accepted at m=0) =
##       Set({(a1^z)a1 : z in C_S24(v)} の既知 SURV witness 集合)。
##
##  意味づけの規律: 壁窓は dihedral 窓でないため BFC/TB 枠組の適用可否は
##  未整理。本 probe は群論観測のみを機械出力し、算術的意味づけ・矛盾解釈
##  は一切行わない(接触遮断 — 期待値をコードに書かない)。
##
##  宇宙: n=24 窓固定(P-WALL-2・既存 witness 実物 a1,b1 逐語)・m=0(アンカー)
##  と m=N_ord-1 のみ。拡大しない。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");

JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");   # MakeWindow / RtOf(診断専用) / AbstractProd 等を読み込む

Sha256OfString := function(s)
  local tmp, out, f, line;
  tmp := "search/.tmp_wallcanary_sha.txt";
  out := "search/.tmp_wallcanary_sha.out";
  f := OutputTextFile(tmp, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, s);
  CloseStream(f);
  Exec(Concatenation("sha256sum \"", tmp, "\" > \"", out, "\""));
  f := InputTextFile(out);
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\" \"", out, "\""));
  if line = fail or Length(line) < 64 then
    Error("wall_canary_24: Sha256OfString: sha256sum did not return a hash line");
  fi;
  return line{[1 .. 64]};
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_wallcanary_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1 .. 64]};
end;;

#############################################################################
## ---- witness (P-WALL-2, n=24; wall2_cert.g と逐語同一) ----
#############################################################################
n := 24;;
a1 := ( 1,13)( 2, 9)( 3, 5)( 4,24)( 6, 8)( 7,21)(10,12)(11,20)(14,16)(15,22)(17,19)(18,23);;
b1 := ( 1,12, 9)( 2, 8, 5)( 3, 4,24)( 6, 7,21)(10,11,20)(13,19,16)(14,15,22)(17,18,23);;
Snn := SymmetricGroup(n);;  Ann := AlternatingGroup(n);;

w0 := b1^-1 * a1;;   # xbar (order 19)
v0 := a1 * b1^-1;;   # SURV 参照用(既知 witness 集合の再構成に使う)

aE := a1 * (n+1, n+3);;
bE := b1 * (n+1, n+3, n+2);;
s1 := bE^-1 * aE;;
s2 := aE * bE^2;;
braidHolds := (s1*s2*s1 = s2*s1*s2);;
if not braidHolds then
  Error("wall_canary_24: braid relation fails for the wall2 witness -- refusing to proceed");
fi;

W := MakeWindow(s1, s2);;
Nord := W.Nord;;
cRaw := (s1*s2)^3;;
cIsOne := (cRaw = Identity(W.Bq));;

Print("=== wall_canary_24 v2 (WAC-CAN-2): setup ===\n");
Print("  n=", n, "  N_ord=", Nord, "  c=(s1 s2)^3=1 (raw) ? ", cIsOne, "\n");
Print("  W.PN = A_", n, " ? ", W.PN = Ann, "   W.c=Identity(Bq) (AbstractProd 版) ? ",
      W.c = Identity(W.Bq), "\n");

if not cIsOne then
  Error("wall_canary_24: precondition c=1 (raw (s1*s2)^3) FAILS -- the (3.3)(3.4) ",
        "instantiation below assumes this window's c is central-trivial (as wall2_cert.g ",
        "found); refusing to proceed with a formula that silently drops a nontrivial c^m term");
fi;

Cw := Centralizer(Snn, w0);;
CwSize := Size(Cw);;
CwStruct := StructureDescription(Cw);;
CwSolvable := IsSolvable(Cw);;
Print("  |C_S", n, "(w0)| = ", CwSize, "  構造 ", CwStruct, "  可解? ", CwSolvable, "\n");

#############################################################################
## ---- 単一定義: YImg (f^-1 y^u f) -- 候補生成・受理器・生成条件の3箇所が
##      これだけを呼ぶ(向き規約の混用を再発させない、CV-13)----
#############################################################################
YImg := function(W, u, f) return f^-1 * W.y^u * f; end;;

#############################################################################
## ---- 主計器: (3.3)(3.4) の一般 m 版(raw GAP 乗算・docs/week1-定義ノート.md
##      L160-161 の逐語代入)----
#############################################################################
HexagonHolds := function(W, m, f)
  local u, lhs1, rhs1, lhs2, rhs2;
  u := 2*m + 1;
  lhs1 := W.s1^u * f^-1 * W.s2^u * f;
  rhs1 := f^-1 * W.s1 * W.s2 * W.x^(-m) * W.c^m;
  lhs2 := f^-1 * W.s2^u * f * W.s1^u;
  rhs2 := W.s2 * W.s1 * W.y^(-m) * W.c^m * f;
  return rec(eq1 := (lhs1 = rhs1), eq2 := (lhs2 = rhs2));
end;;

GenerationHolds := function(W, m, f)
  local u;
  u := 2*m + 1;
  return Group(W.x^u, YImg(W, u, f)) = W.PN;
end;;

#############################################################################
## ---- Xi 型候補生成(WAC-CAN-2 修正版: 左剰余類・literal 向き) ----
##  f0 := hRep(反転しない -- hRep 自体が f0^-1*yu*f0=target を満たす)
##  f  := c*f0(c は C_P(yu) の左からの積、右でない)
##  生成直後に YImg(W,u,f)=target の自己検査 assert(fail-closed)。
#############################################################################
FindShadowCandidates := function(W, m, Snn)
  local u, yu, Cyu, cElts, Stab, stabElts, alpha0, s, target, hRep, f0, c, f,
        out, scanned, hx, genOK, wdHom, wdFail, budgetHolds;
  u := 2*m + 1;

  ## 前提 assert (1)(2)
  if not IsNaturalAlternatingGroup(W.PN) then
    Error("FindShadowCandidates: W.PN is not a natural alternating group -- ",
          "fast automorphism path invalid, refusing to proceed");
  fi;
  if Gcd(u, W.Nord) <> 1 then
    Error("FindShadowCandidates: m=", m, " is not charming (gcd(2m+1,N_ord)<>1) -- refusing");
  fi;

  yu := W.y^u;
  Cyu := Centralizer(W.PN, yu);
  cElts := Elements(Cyu);
  Stab := Centralizer(Snn, W.x);
  stabElts := Elements(Stab);
  alpha0 := RepresentativeAction(Snn, W.x, W.x^u);
  out := [];  scanned := 0;  wdFail := 0;
  if alpha0 = fail then
    return rec(alpha0_found := false, candidates := out, scanned := 0, wd_fail_count := 0,
               stab_size := Length(stabElts), cyu_size := Length(cElts), budget_holds := true);
  fi;
  for s in stabElts do
    target := W.y ^ (s * alpha0);
    hRep := RepresentativeAction(W.PN, yu, target, OnPoints);
    if hRep = fail then continue; fi;
    f0 := hRep;;   # literal 向き: f0^-1 * yu * f0 = target を直接満たす(反転しない)
    for c in cElts do
      f := c * f0;;   # 左剰余類(WAC-CAN-2 の修正本体)
      scanned := scanned + 1;

      ## CV-13 向き自己検査(fail-closed)
      if YImg(W, u, f) <> target then
        Error("FindShadowCandidates: CV-13 orientation self-check FAILED at m=", m,
              " -- YImg(W,u,f) <> target for a freshly constructed candidate; this ",
              "should be structurally impossible given f=c*f0, f0^-1*yu*f0=target, ",
              "c centralizing yu -- refusing to continue silently");
      fi;

      ## 受理 (1): hexagon literal (3.3)(3.4)
      hx := HexagonHolds(W, m, f);;
      if not (hx.eq1 and hx.eq2) then continue; fi;

      ## 受理 (2): generation condition
      genOK := GenerationHolds(W, m, f);;
      if not genOK then continue; fi;

      ## 受理 (3): WD-P (well-definedness at P level, フィルタ・別欄計上)
      wdHom := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y], [W.x^u, YImg(W, u, f)]);;
      if wdHom = fail then
        wdFail := wdFail + 1;
        continue;
      fi;

      Add(out, f);
    od;
  od;
  budgetHolds := (scanned = Length(stabElts) * Length(cElts));;
  if not budgetHolds then
    Error("FindShadowCandidates: 予算 assert FAILS -- scanned(", scanned,
          ") <> |Stab|*|C_P(yu)|(", Length(stabElts) * Length(cElts),
          ") -- some stab element failed to find hRep; investigate before trusting counts");
  fi;
  return rec(alpha0_found := true, candidates := out, scanned := scanned, wd_fail_count := wdFail,
             stab_size := Length(stabElts), cyu_size := Length(cElts), budget_holds := budgetHolds);
end;;

#############################################################################
## ---- 受理 (4): settled (Bq 水準 hom) -- フィルタにしない、別欄報告のみ。
##      コスト予算(既定 150 秒)を超えたら明示 skip。
#############################################################################
SettledReport := function(W, m, fs, timeBudgetMs)
  local u, t0, i, hom, failCount, evaluated, skippedReason;
  u := 2*m + 1;;
  t0 := Runtime();;
  failCount := 0;;  evaluated := 0;;  skippedReason := "";;
  for i in [1 .. Length(fs)] do
    if Runtime() - t0 > timeBudgetMs then
      skippedReason := Concatenation("time_budget_exceeded_after_", String(evaluated),
                                      "_of_", String(Length(fs)));;
      break;;
    fi;
    hom := GroupHomomorphismByImages(W.Bq, W.Bq, [W.s1, W.s2],
             [W.s1^u, fs[i]^-1 * W.s2^u * fs[i]]);;
    evaluated := evaluated + 1;;
    if hom = fail then failCount := failCount + 1; fi;
  od;
  return rec(computed_fully := (evaluated = Length(fs)), fail_count := failCount,
             total_evaluated := evaluated, total_candidates := Length(fs),
             skipped_reason := skippedReason);
end;;

SETTLED_TIME_BUDGET_MS := 150000;;

#############################################################################
## ---- 既知 SURV witness 集合の再構成(wall2_cert.g / sat_l1_probe11.g 逐語
##      再現・m=0 の集合等号アンカー用)----
#############################################################################
BuildKnownSurvFs := function(Snn, a1, s1, s2, W, v0)
  local Cv, out, z, f;
  Cv := Centralizer(Snn, v0);;
  out := [];;
  for z in Elements(Cv) do
    f := (a1^z) * a1;;
    if SignPerm(f) <> 1 then continue; fi;
    if not (s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f) then continue; fi;
    if Group(W.x, W.y^f) <> W.PN then continue; fi;
    Add(out, f);
  od;
  return out;
end;;

#############################################################################
## ---- 回帰アンカー: m=0 で候補生成+4段受理が既知 2280 と集合として一致するか ----
#############################################################################
Print("\n=== 回帰アンカー: m=0 (Xi型候補生成 v2 + (3.3)(3.4) 一般式) ===\n");
t0 := Runtime();;
anchorRes := FindShadowCandidates(W, 0, Snn);;
t1 := Runtime();;
anchorCount := Length(anchorRes.candidates);;
Print("  alpha0 found = ", anchorRes.alpha0_found, "  stab_size=", anchorRes.stab_size,
      "  cyu_size=", anchorRes.cyu_size, "  scanned=", anchorRes.scanned,
      "  budget_holds=", anchorRes.budget_holds, "  wd_fail_count=", anchorRes.wd_fail_count,
      "  candidates=", anchorCount, "  経過=", (t1-t0)/1000.0, "s\n");

knownSurvFs := BuildKnownSurvFs(Snn, a1, s1, s2, W, v0);;
knownSurvCount := Length(knownSurvFs);;
setEqAnchor := (Set(anchorRes.candidates) = Set(knownSurvFs));;
anchorMatches2280 := (anchorCount = 2280) and (knownSurvCount = 2280);;
Print("  known_surv_count=", knownSurvCount, "\n");
Print("  ", PF(setEqAnchor), " 集合等号(Set(候補)=Set(既知SURV)) = ", setEqAnchor, "\n");
Print("  ", PF(anchorMatches2280), " 個数一致(両方とも2280) = ", anchorMatches2280, "\n");

anchorPass := setEqAnchor and anchorMatches2280;;

settledM0 := rec(computed_fully := false, fail_count := 0, total_evaluated := 0,
                  total_candidates := 0, skipped_reason := "not_run_pre_anchor_check");;
if anchorPass then
  Print("\n=== settled 報告(m=0, フィルタでない・別欄のみ) ===\n");
  t0 := Runtime();;
  settledM0 := SettledReport(W, 0, anchorRes.candidates, SETTLED_TIME_BUDGET_MS);;
  t1 := Runtime();;
  Print("  computed_fully=", settledM0.computed_fully, "  evaluated=", settledM0.total_evaluated,
        "/", settledM0.total_candidates, "  fail_count=", settledM0.fail_count,
        "  skipped_reason=", settledM0.skipped_reason, "  経過=", (t1-t0)/1000.0, "s\n");
fi;

if not anchorPass then
  Print("\n*** ANCHOR FAILURE (v2): m=0 の一般コード経路が既存 witness と集合として一致しない ***\n");
  Print("*** ここで停止し、数値のみ報告する ***\n");
  Print("WALL_CANARY_24_ANCHOR_FAIL\n");
fi;

#############################################################################
## ---- m = N_ord - 1 層(複素共役カナリア候補)----
#############################################################################
mC := Nord - 1;;
uC := 2*mC + 1;;
Print("\n=== カナリア本体: m_c = N_ord-1 = ", mC, "  (u_c = ", uC, ") ===\n");

canaryRes := rec(alpha0_found := false, candidates := [], scanned := 0, wd_fail_count := 0,
                  stab_size := 0, cyu_size := 0, budget_holds := true);;
canaryStatus := "skipped_anchor_fail";;
settledM18 := rec(computed_fully := false, fail_count := 0, total_evaluated := 0,
                   total_candidates := 0, skipped_reason := "not_run");;

if anchorPass then
  t0 := Runtime();;
  canaryRes := FindShadowCandidates(W, mC, Snn);;
  t1 := Runtime();;
  canaryStatus := "measured";;
  Print("  alpha0 found = ", canaryRes.alpha0_found, "  stab_size=", canaryRes.stab_size,
        "  cyu_size=", canaryRes.cyu_size, "  scanned=", canaryRes.scanned,
        "  budget_holds=", canaryRes.budget_holds, "  wd_fail_count=", canaryRes.wd_fail_count,
        "  candidates=", Length(canaryRes.candidates), "  経過=", (t1-t0)/1000.0, "s\n");

  Print("\n=== settled 報告(m=", mC, ", フィルタでない・別欄のみ) ===\n");
  t0 := Runtime();;
  settledM18 := SettledReport(W, mC, canaryRes.candidates, SETTLED_TIME_BUDGET_MS);;
  t1 := Runtime();;
  Print("  computed_fully=", settledM18.computed_fully, "  evaluated=", settledM18.total_evaluated,
        "/", settledM18.total_candidates, "  fail_count=", settledM18.fail_count,
        "  skipped_reason=", settledM18.skipped_reason, "  経過=", (t1-t0)/1000.0, "s\n");
else
  Print("  SKIPPED (anchor failed)\n");
fi;

canaryCount := Length(canaryRes.candidates);;

#############################################################################
## ---- (2)(3) 見つかった候補ごとの位数・conjugator・C19/S5 作用
##      (合成則 (3.53) を raw で実装、候補多数の場合は先頭 CANARY_SAMPLE_CAP
##      件のみ処理し、cert に truncated 明記 -- silent cap でない) ----
#############################################################################
BuildEh := function(W, m1, f1)
  local u1;
  u1 := 2*m1 + 1;
  return GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y], [W.x^u1, YImg(W, u1, f1)]);
end;;

ShadowMul := function(W, p1, p2)
  local m1, f1, m2, f2, Eh, nm, nf;
  m1 := p1[1];;  f1 := p1[2];;  m2 := p2[1];;  f2 := p2[2];;
  Eh := BuildEh(W, m1, f1);;
  if Eh = fail then return fail; fi;
  nm := (2*m1*m2 + m1 + m2) mod W.Nord;;
  nf := f1 * Image(Eh, f2);;
  return [nm, nf];
end;;

ShadowOrder := function(W, g, capIter)
  local ident, cur, k;
  ident := [0, Identity(W.PN)];;
  cur := g;;  k := 1;;
  while cur <> ident and k <= capIter do
    cur := ShadowMul(W, cur, g);;
    if cur = fail then return rec(order := -1, note := "Eh_fail_during_power", reached := k); fi;
    k := k + 1;;
  od;
  if cur = ident then return rec(order := k, note := "found", reached := k);
  else return rec(order := -1, note := "cap_exceeded", reached := k - 1); fi;
end;;

ORDER_CAP := 250;;
CANARY_SAMPLE_CAP := 20;;

## S5 因子上の誘導作用(Cw を正規化する場合のみ適用)
InduceS5Report := function(Cw, w0, g)
  local homQ, Q, gensCw, gensQ, imgGens, actConj, q0;
  homQ := NaturalHomomorphismByNormalSubgroup(Cw, Group(w0));;
  Q := Image(homQ);;
  gensCw := GeneratorsOfGroup(Cw);;
  gensQ := List(gensCw, x -> Image(homQ, x));;
  imgGens := List(gensCw, x -> Image(homQ, x^g));;
  actConj := function(lst, qq) return List(lst, xx -> xx^qq); end;;
  q0 := RepresentativeAction(Q, gensQ, imgGens, actConj);;
  if q0 <> fail then
    return rec(applicable := true, quotient_size := Size(Q),
               quotient_struct := StructureDescription(Q),
               inner_witness_found := true, witness_order := Order(q0));
  else
    return rec(applicable := true, quotient_size := Size(Q),
               quotient_struct := StructureDescription(Q),
               inner_witness_found := false, witness_order := -1);
  fi;
end;;

## 1 候補分の計測をまとめて行う(位数・conjugator・C19 作用・S5 誘導作用)
ProcessCandidate := function(W, Snn, Cw, w0, Nord, mC, uC, f, capIter)
  local ordRes, ytarget, g, gOrder, gFound, normalizesW0, rVal, normalizesCw, s5report;
  ordRes := ShadowOrder(W, [mC, f], capIter);;
  ytarget := YImg(W, uC, f);;
  g := RepresentativeAction(Snn, [W.x, W.y], [W.x^uC, ytarget], OnTuples);;
  gFound := (g <> fail);;
  gOrder := -1;;  normalizesW0 := false;;  rVal := -1;;  normalizesCw := false;;
  s5report := rec(applicable := false);;
  if gFound then
    gOrder := Order(g);;
    normalizesW0 := (w0^g in Group(w0));;
    if normalizesW0 then
      rVal := First([0 .. Nord-1], rr -> w0^rr = w0^g);;
      if rVal = fail then rVal := -1; fi;
    fi;
    normalizesCw := (Cw^g = Cw);;
    if normalizesCw then
      s5report := InduceS5Report(Cw, w0, g);;
    fi;
  fi;
  return rec(
    shadow_order := ordRes.order, shadow_order_note := ordRes.note,
    shadow_order_iterations_reached := ordRes.reached,
    conjugator_found := gFound, conjugator_order := gOrder,
    normalizes_w0 := normalizesW0, c19_action_r := rVal,
    normalizes_ker_chi := normalizesCw, s5_factor := s5report
  );
end;;

canarySampleTruncated := (Length(canaryRes.candidates) > CANARY_SAMPLE_CAP);;
canarySample := canaryRes.candidates;;
if canarySampleTruncated then
  canarySample := canaryRes.candidates{[1 .. CANARY_SAMPLE_CAP]};;
fi;;

candidateReports := List(canarySample,
  f -> ProcessCandidate(W, Snn, Cw, w0, Nord, mC, uC, f, ORDER_CAP));;

PrintCandidateReport := function(i, cr)
  Print("  候補#", i, ": shadow_order=", cr.shadow_order, " (", cr.shadow_order_note, ")",
        "  conjugator_found=", cr.conjugator_found, "  conjugator_order=", cr.conjugator_order,
        "  normalizes_w0=", cr.normalizes_w0, "  r(C19)=", cr.c19_action_r,
        "  normalizes_ker_chi=", cr.normalizes_ker_chi, "\n");
  if cr.s5_factor.applicable then
    Print("    S5因子: |Q|=", cr.s5_factor.quotient_size, " 構造=", cr.s5_factor.quotient_struct,
          " 内部witness発見=", cr.s5_factor.inner_witness_found,
          " witness位数=", cr.s5_factor.witness_order, "\n");
  fi;
end;;

Print("\n=== (2)(3) 候補ごとの計測", " (sample_cap=", CANARY_SAMPLE_CAP,
      " truncated=", canarySampleTruncated, ") ===\n");
for i in [1 .. Length(candidateReports)] do
  PrintCandidateReport(i, candidateReports[i]);
od;;

#############################################################################
## ---- 診断欄: RtOf(kerchi-judge 一般式)との比較(主計器ではない) ----
#############################################################################
Print("\n=== 診断: RtOf(m=", mC, ") vs 主計器の一致(既知逸脱の追加診断材料) ===\n");
RtOfDiagOne := function(W, mC, f)
  local rtofVal, rtofMatches;
  rtofVal := RtOf(W, mC, f);;
  rtofMatches := (rtofVal = W.c^mC);;
  Print("  候補: RtOf(W,", mC, ",f) = c^", mC, " ? ", rtofMatches, "\n");
  return rtofMatches;
end;;
rtofDiag := List(canarySample, f -> RtOfDiagOne(W, mC, f));;
## m=0 anchor 側でも同様の診断(1件のみ、コスト抑制のため先頭候補)
rtofDiagM0 := fail;;
if Length(anchorRes.candidates) > 0 then
  rtofDiagM0 := (RtOf(W, 0, anchorRes.candidates[1]) = W.c^0);;
  Print("  (参考) m=0 先頭候補: RtOf(W,0,f) = c^0 ? ", rtofDiagM0, "\n");
fi;;

#############################################################################
## ---- 補助(B): ker chi~ = Cw 内の対合共役類の機械列挙 ----
#############################################################################
Print("\n=== 補助: ker chi~ = C_S", n, "(w0) 内の対合(位数2)共役類 ===\n");
allClasses := ConjugacyClasses(Cw);;
invClasses := Filtered(allClasses, cl -> Order(Representative(cl)) = 2);;
MakeInvClassReport := function(cl)
  local rep;
  rep := Representative(cl);;
  Print("  class_size=", Size(cl), "  cycle_type=", CycleStructurePerm(rep), "\n");
  return rec(
    class_size := Size(cl),
    representative_cycle_type := String(CycleStructurePerm(rep)),
    representative_perm := String(rep)
  );
end;;
invClassReports := List(invClasses, MakeInvClassReport);;
Print("  対合共役類の総数 = ", Length(invClasses), "\n");

#############################################################################
## ---- JSON 出力 ----
#############################################################################
CandidateReportJson := function(cr)
  local s5json;
  if cr.s5_factor.applicable then
    s5json := Concatenation(
      "{\"applicable\":true,\"quotient_size\":", String(cr.s5_factor.quotient_size),
      ",\"quotient_struct\":", JStr(cr.s5_factor.quotient_struct),
      ",\"inner_witness_found\":", JB(cr.s5_factor.inner_witness_found),
      ",\"witness_order\":", String(cr.s5_factor.witness_order), "}");
  else
    s5json := "{\"applicable\":false}";
  fi;
  return Concatenation(
    "{\"shadow_order\":", String(cr.shadow_order),
    ",\"shadow_order_note\":", JStr(cr.shadow_order_note),
    ",\"shadow_order_iterations_reached\":", String(cr.shadow_order_iterations_reached),
    ",\"conjugator_found\":", JB(cr.conjugator_found),
    ",\"conjugator_order\":", String(cr.conjugator_order),
    ",\"normalizes_w0\":", JB(cr.normalizes_w0),
    ",\"c19_action_r\":", String(cr.c19_action_r),
    ",\"normalizes_ker_chi\":", JB(cr.normalizes_ker_chi),
    ",\"s5_factor\":", s5json, "}");
end;;

InvClassJson := function(ic)
  return Concatenation(
    "{\"class_size\":", String(ic.class_size),
    ",\"representative_cycle_type\":", JStr(ic.representative_cycle_type),
    ",\"representative_perm\":", JStr(ic.representative_perm), "}");
end;;

SettledJson := function(sr)
  return Concatenation(
    "{\"computed_fully\":", JB(sr.computed_fully),
    ",\"fail_count\":", String(sr.fail_count),
    ",\"total_evaluated\":", String(sr.total_evaluated),
    ",\"total_candidates\":", String(sr.total_candidates),
    ",\"skipped_reason\":", JStr(sr.skipped_reason), "}");
end;;

selfSha := ComputeSha256File("search/probe/wac_v1/wall_canary_24_20260801.g");;

rtofDiagJson := JArr(List(rtofDiag, JB));;
rtofDiagM0Json := "null";;
if rtofDiagM0 <> fail then rtofDiagM0Json := JB(rtofDiagM0); fi;;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"wac_v1-wall-canary/v2\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/wall_canary_24_20260801.g\",\n",
  "  \"window_label\":\"P-WALL-2\",\n",
  "  \"card_label\":\"P5-3(発案係第17便・採択札)・WAC-CAN-2 修正版(裁定382)\",\n",
  "  \"source_witness\":\"search/probe/wac_v1/wall2_cert.g の a1,b1 逐語(P-WALL-2 witness)\",\n",
  "  \"note\":\"群論観測のみ・算術的意味づけ保留。壁窓は dihedral 窓でないため BFC/TB 枠組の適用可否は未整理。判定は本 probe に埋め込まない(接触遮断)。主計器 = docs/week1-定義ノート.md (3.3)(3.4) の m への literal 代入。RtOf(kerchi-judge.g 一般式)は診断専用。v1 の anchor failure(120/2280)は候補生成の向き規約混用(judge向き右剰余類 vs 手書き向き左剰余類)が原因と確定(裁定382) -- v2 で f0:=hRep(反転なし)・f:=c*f0(左剰余類)に修正し、生成直後に向き自己検査 assert を追加。\",\n",
  "  \"f_orientation\":\"literal (f0 = hRep directly, i.e. f0^-1*y^u*f0 = target; candidates f = c*f0 for c in C_P(y^u), a LEFT coset; matches wall2_cert.g / docs/week1-定義ノート.md (3.3)(3.4) hand-derived convention, NOT kerchi-judge.g CorrectedShadowsXi's right-coset f0*c convention)\",\n",
  "  \"n\":", String(n), ",\n",
  "  \"a1\":", JStr(String(a1)), ",\n",
  "  \"b1\":", JStr(String(b1)), ",\n",
  "  \"n_ord\":", String(Nord), ",\n",
  "  \"c_raw_is_identity\":", JB(cIsOne), ",\n",
  "  \"ker_chi_tilde\":{\n",
  "    \"size\":", String(CwSize), ",\n",
  "    \"structure_description\":", JStr(CwStruct), ",\n",
  "    \"solvable\":", JB(CwSolvable), "\n",
  "  },\n",
  "  \"regression_anchor_m0\":{\n",
  "    \"alpha0_found\":", JB(anchorRes.alpha0_found), ",\n",
  "    \"stab_size\":", String(anchorRes.stab_size), ",\n",
  "    \"cyu_size\":", String(anchorRes.cyu_size), ",\n",
  "    \"scanned\":", String(anchorRes.scanned), ",\n",
  "    \"budget_holds\":", JB(anchorRes.budget_holds), ",\n",
  "    \"wd_fail_count\":", String(anchorRes.wd_fail_count), ",\n",
  "    \"candidates_found\":", String(anchorCount), ",\n",
  "    \"known_surv_count\":", String(knownSurvCount), ",\n",
  "    \"set_equality_with_known_surv\":", JB(setEqAnchor), ",\n",
  "    \"matches_known_2280\":", JB(anchorMatches2280), ",\n",
  "    \"anchor_pass\":", JB(anchorPass), ",\n",
  "    \"settled_report\":", SettledJson(settledM0), "\n",
  "  },\n",
  "  \"canary_m18\":{\n",
  "    \"status\":", JStr(canaryStatus), ",\n",
  "    \"m\":", String(mC), ",\n",
  "    \"u\":", String(uC), ",\n",
  "    \"alpha0_found\":", JB(canaryRes.alpha0_found), ",\n",
  "    \"stab_size\":", String(canaryRes.stab_size), ",\n",
  "    \"cyu_size\":", String(canaryRes.cyu_size), ",\n",
  "    \"scanned\":", String(canaryRes.scanned), ",\n",
  "    \"budget_holds\":", JB(canaryRes.budget_holds), ",\n",
  "    \"wd_fail_count\":", String(canaryRes.wd_fail_count), ",\n",
  "    \"candidates_found\":", String(canaryCount), ",\n",
  "    \"settled_report\":", SettledJson(settledM18), ",\n",
  "    \"per_candidate_sample_cap\":", String(CANARY_SAMPLE_CAP), ",\n",
  "    \"per_candidate_sample_truncated\":", JB(canarySampleTruncated), ",\n",
  "    \"per_candidate\":", JArr(List(candidateReports, CandidateReportJson)), "\n",
  "  },\n",
  "  \"diagnostic_rtof_comparison\":{\n",
  "    \"note\":\"主計器ではない。既知逸脱(RtOf 不一致)の追加診断材料のみ。canary_m18 側はサンプル(per_candidate_sample_cap 件)にのみ適用。\",\n",
  "    \"m18_matches\":", rtofDiagJson, ",\n",
  "    \"m0_first_candidate_matches\":", rtofDiagM0Json, "\n",
  "  },\n",
  "  \"auxiliary_involution_classes_in_ker\":", JArr(List(invClassReports, InvClassJson)), ",\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), "\n",
  "  }\n",
  "}\n");;

WriteFile("search/certs/wall_canary_24_20260801.json", cert);;
Print("\nWrote search/certs/wall_canary_24_20260801.json\n");
Print("\nWALL_CANARY_24_DONE\n");
QUIT;
