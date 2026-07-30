#############################################################################
## search/probe/wac_v1/sat_l1_probe15.g
##  【裁定用・決定実験】judge の実物(kerchi-judge.g の MakeWindow/TH/RtOf)を
##  そのままロードし、m=0 層の解集合を私の手書き式の解集合と直接突合する。
##  窓: W-E-A10-5x2t0(証明書 |ker chi~| = 10・judge 経由で発行済)
##  転記ミスの可能性を排除するため、判定は judge の関数呼び出しで行う。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/kerchi-judge.g");;

BuildW := function(a1, b1, nn)
  local Sn, S3, Dgrp, embA, embS, agen, bgen, s1, s2;
  Sn := SymmetricGroup(nn);; S3 := SymmetricGroup(3);;
  Dgrp := DirectProduct(Sn, S3);;
  embA := Embedding(Dgrp, 1);; embS := Embedding(Dgrp, 2);;
  agen := Image(embA, a1) * Image(embS, (1,3));;
  bgen := Image(embA, b1) * Image(embS, (1,3,2));;
  s1 := bgen^-1 * agen;;
  s2 := agen^-1 * bgen^2;;
  return rec(W := MakeWindow(s1, s2), agen := agen, bgen := bgen);
end;;

Test := function(nn, a1, b1, label)
  local R, W, a, b, dlt, P, f, S_judge, S_mine, S_dlt, S_dltinv, n1, n2;
  R := BuildW(a1, b1, nn);
  W := R.W;
  a := W.Dlt; b := W.s1*W.s2; dlt := W.dlt;
  Print("\n===== ", label, " =====\n");
  Print("  Dlt=AbstractProd([s1,s2,s1]) = s1*s2*s1 ? ", W.Dlt = W.s1*W.s2*W.s1,
        "   ord ", Order(W.Dlt), "\n");
  Print("  dlt=AbstractProd([s1,s2])    = s2*s1 ? ", W.dlt = W.s2*W.s1,
        "   ord ", Order(W.dlt), "   (= s1*s2 ? ", W.dlt = W.s1*W.s2, ")\n");
  Print("  c = Dlt^2 = 1 ? ", W.c = Identity(W.Bq), "   N_ord = ", W.Nord, "\n");
  P := DerivedSubgroup(W.PN);
  Print("  |[P,P]| = ", Size(P), "   = |P| ? ", Size(P) = Size(W.PN), "\n");
  S_judge := []; S_mine := []; S_dlt := []; S_dltinv := [];
  for f in Elements(P) do
    ## --- judge の実物の 2 条件(m=0) ---
    if AbstractProd([f, TH(W, f)]) = Identity(W.Bq) and
       RtOf(W, 0, f) = W.c^0 then Add(S_judge, f); fi;
    ## --- 私の手書き literal (3.3)(3.4) at m=0 ---
    if W.s1*f^-1*W.s2*f = f^-1*W.s1*W.s2 and
       f^-1*W.s2*f*W.s1 = W.s2*W.s1*f then Add(S_mine, f); fi;
    ## --- 私の簡約形(b = s1*s2)---
    if (f*a)^2 = Identity(W.Bq) and (f*b^-1)^3 = Identity(W.Bq) then Add(S_dlt, f); fi;
    ## --- dlt 版(judge の tau)---
    if (f*a)^2 = Identity(W.Bq) and (f*dlt^-1)^3 = Identity(W.Bq) then Add(S_dltinv, f); fi;
  od;
  Print("  --- m=0 層の解集合(生成条件は未適用)---\n");
  Print("    judge の実物 (TH + RtOf)          : ", Length(S_judge), "\n");
  Print("    私の literal (3.3)(3.4)           : ", Length(S_mine), "\n");
  Print("    私の簡約形 (f*a)^2,(f*b^-1)^3     : ", Length(S_dlt), "\n");
  Print("    dlt 版     (f*a)^2,(f*dlt^-1)^3   : ", Length(S_dltinv), "\n");
  Print("    集合一致: judge=mine ? ", Set(S_judge)=Set(S_mine),
        "   judge=簡約(b) ? ", Set(S_judge)=Set(S_dlt),
        "   judge=dlt版 ? ", Set(S_judge)=Set(S_dltinv), "\n");
  Print("    mine = 簡約(b) ? ", Set(S_mine)=Set(S_dlt), "\n");
  ## judge 集合が f -> f^-1 で mine に写るか
  Print("    judge = { f^-1 : f in mine } ? ",
        Set(S_judge) = Set(List(S_mine, x -> x^-1)), "\n");
  return true;
end;;

Test(10, ( 1, 2)( 3, 6)( 7,10), ( 2,10, 6)( 3, 5, 4)( 7, 9, 8),
     "W-E-A10-5x2t0 (証明書 |ker|=10)");;
Print("\nSAT_L1_PROBE15_DONE\n");
QUIT;
