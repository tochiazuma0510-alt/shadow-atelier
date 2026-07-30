#############################################################################
## search/probe/wac_v1/sat_l1_probe17.g
##  【裁定用・確定実験】原因 = f の向き(f vs f^-1)。
##  probe16 で A_10 全域を走査した結果:
##    judge 集合 J と 私の手書き集合 M は  **J = { f^-1 : f in M }**(集合として)
##    |J| = |M| = 65(hexagon のみ)/ 50(生成込)で位数は完全一致。
##  ここでは SURV 構成 f_z に対し、judge の実物条件を f_z^-1 で検査する。
##  期待: W-CENT-B 162/162、P-WALL-2 2280/2280 が judge 条件を通過。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
Read("search/week3-battery-common.g");;
Read("search/probe/wac_v1/_judge_core_extract.g");;

Chk17 := function(nn, a1, b1, label)
  local aE, bE, s1, s2, W, one, v, Cv, z, f, okF, okFi, okGen, okGenI, n0, alp, XiIm, Snn;
  Snn := SymmetricGroup(nn);
  aE := a1*(nn+1,nn+3);; bE := b1*(nn+1,nn+3,nn+2);;
  s1 := bE^-1*aE;; s2 := aE^-1*bE^2;;
  W := MakeWindow(s1, s2);
  one := Identity(W.Bq);
  v := a1*b1^-1;
  Cv := Centralizer(Snn, v);
  Print("\n===== ", label, "  n=", nn, " =====\n");
  Print("  |C_Sn(v)| = ", Size(Cv), "   N_ord = ", W.Nord, "   c=1 ? ", W.c = one, "\n");
  okF := 0; okFi := 0; okGen := 0; okGenI := 0; alp := [];
  for z in Elements(Cv) do
    f := (a1^z)*a1;
    ## judge 実物条件を f にそのまま当てる
    if AbstractProd([f, TH(W, f)]) = one and RtOf(W, 0, f) = W.c^0 then
      okF := okF + 1;
      if Size(Group(W.x, AbstractProd([f^-1, W.y, f]))) = Size(W.PN) then okGen := okGen+1; fi;
    fi;
    ## judge 実物条件を f^-1 に当てる(向きを合わせた版)
    if AbstractProd([f^-1, TH(W, f^-1)]) = one and RtOf(W, 0, f^-1) = W.c^0 then
      okFi := okFi + 1;
      if Size(Group(W.x, AbstractProd([f, W.y, f^-1]))) = Size(W.PN) then
        okGenI := okGenI + 1;
        Add(alp, a1*z*a1);
      fi;
    fi;
  od;
  Print("  judge 条件を f_z       に当てて通過: ", okF,  " / ", Size(Cv),
        "   (生成込 ", okGen, ")\n");
  Print("  judge 条件を f_z^{-1}  に当てて通過: ", okFi, " / ", Size(Cv),
        "   (生成込 ", okGenI, ")   <== 向きを合わせた版\n");
  if Length(alp) > 0 then
    XiIm := Group(alp);
    Print("  Xi 像 <a1*z*a1> の位数 = ", Size(XiIm), "  ", StructureDescription(XiIm),
          "   可解? ", IsSolvable(XiIm), "\n");
    Print("  judge 規約でも同じ alpha か: ybar^{alpha} = f*ybar*f^-1 を全 z で ? ",
          ForAll(Elements(Cv), z2 -> W.y^(a1*z2*a1) =
                 AbstractProd([((a1^z2)*a1)^-1, W.y, (a1^z2)*a1])), "\n");
  fi;
  return true;
end;;

Chk17(18, ( 1, 2)( 3, 4)( 5, 9)( 6,18)( 7,15)( 8,10)(11,14)(16,17),
      ( 2, 9, 4)( 5, 8,18)( 6,17,15)( 7,14,10)(11,13,12), "W-CENT-B");;
Chk17(24, ( 1,13)( 2, 9)( 3, 5)( 4,24)( 6, 8)( 7,21)(10,12)(11,20)(14,16)(15,22)(17,19)(18,23),
      ( 1,12, 9)( 2, 8, 5)( 3, 4,24)( 6, 7,21)(10,11,20)(13,19,16)(14,15,22)(17,18,23),
      "P-WALL-2");;
Print("\nSAT_L1_PROBE17_DONE\n");
QUIT;
