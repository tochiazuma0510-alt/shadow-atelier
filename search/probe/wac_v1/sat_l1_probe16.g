#############################################################################
## search/probe/wac_v1/sat_l1_probe16.g
##  【裁定用・決定実験 v2】judge の core 関数を **sed で機械抽出**した
##  _judge_core_extract.g(kerchi-judge.g 146-165 行の逐語コピー)を読み込み、
##  m=0 層の解集合を私の手書き式と直接突合する。転記ミスの余地なし。
##  窓 1: W-E-A10-5x2t0(judge 経由の証明書 |ker chi~| = 10)
##  窓 2: W-CENT-B (n=18)
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
Read("search/week3-battery-common.g");;            ## AbstractProd(反転規約)
Read("search/probe/wac_v1/_judge_core_extract.g");;  ## MakeWindow / TT / TH / RtOf

Chk16 := function(nn, a1, b1, label)
  local aE, bE, s1, s2, W, a, b, dlt, P, f, Sj, Sm, Sb, Sd, one, gen, Sjg, Smg;
  aE := a1*(nn+1,nn+3);; bE := b1*(nn+1,nn+3,nn+2);;
  s1 := bE^-1*aE;; s2 := aE^-1*bE^2;;      ## strike-*.g と同一(a^2=1 ゆえ aE*bE^2 と同じ)
  W := MakeWindow(s1, s2);
  one := Identity(W.Bq);
  a := W.Dlt; b := W.s1*W.s2; dlt := W.dlt;
  Print("\n===== ", label, "  n=", nn, " =====\n");
  Print("  s2 = aE*bE^2 と一致 ? ", s2 = aE*bE^2, "\n");
  Print("  Dlt = s1*s2*s1 ? ", W.Dlt = W.s1*W.s2*W.s1, " ord ", Order(W.Dlt),
        "    dlt = s2*s1 ? ", W.dlt = W.s2*W.s1, " ord ", Order(W.dlt),
        "    dlt = s1*s2 ? ", W.dlt = W.s1*W.s2, "\n");
  Print("  c = 1 ? ", W.c = one, "   N_ord = ", W.Nord, "   |P| = ", Size(W.PN), "\n");
  P := DerivedSubgroup(W.PN);
  Sj := []; Sm := []; Sb := []; Sd := []; Sjg := []; Smg := [];
  for f in Elements(P) do
    ## (J) judge の実物 2 条件(m=0)
    if AbstractProd([f, TH(W, f)]) = one and RtOf(W, 0, f) = W.c^0 then
      Add(Sj, f);
      ## judge の生成条件(u=1): Group(x, AbstractProd([f^-1,y,f]))
      if Size(Group(W.x, AbstractProd([f^-1, W.y, f]))) = Size(W.PN) then Add(Sjg, f); fi;
    fi;
    ## (M) 私の手書き literal (3.3)(3.4) at m=0
    if W.s1*f^-1*W.s2*f = f^-1*W.s1*W.s2 and f^-1*W.s2*f*W.s1 = W.s2*W.s1*f then
      Add(Sm, f);
      if Size(Group(W.x, W.y^f)) = Size(W.PN) then Add(Smg, f); fi;
    fi;
    if (f*a)^2 = one and (f*b^-1)^3 = one then Add(Sb, f); fi;
    if (f*a)^2 = one and (f*dlt^-1)^3 = one then Add(Sd, f); fi;
  od;
  Print("  --- m=0 層(hexagon のみ / +生成)---\n");
  Print("    (J) judge 実物        : ", Length(Sj), "  / 生成込 ", Length(Sjg), "\n");
  Print("    (M) 私の literal      : ", Length(Sm), "  / 生成込 ", Length(Smg), "\n");
  Print("    (b) (f*a)^2,(f*b^-1)^3: ", Length(Sb), "\n");
  Print("    (d) (f*a)^2,(f*dlt^-1)^3: ", Length(Sd), "\n");
  Print("    J=M ? ", Set(Sj)=Set(Sm), "   J=d ? ", Set(Sj)=Set(Sd),
        "   M=b ? ", Set(Sm)=Set(Sb),
        "   J={f^-1: f in M} ? ", Set(Sj)=Set(List(Sm, x->x^-1)), "\n");
  return true;
end;;

Chk16(10, ( 1, 2)( 3, 6)( 7,10), ( 2,10, 6)( 3, 5, 4)( 7, 9, 8),
     "W-E-A10-5x2t0 (証明書 |ker|=10)");;
Chk16(18, ( 1, 2)( 3, 4)( 5, 9)( 6,18)( 7,15)( 8,10)(11,14)(16,17),
     ( 2, 9, 4)( 5, 8,18)( 6,17,15)( 7,14,10)(11,13,12), "W-CENT-B");;
Print("\nSAT_L1_PROBE16_DONE\n");
QUIT;
