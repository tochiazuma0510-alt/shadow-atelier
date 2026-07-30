#############################################################################
## search/probe/wac_v1/centb_cert_judge.g
##  Sol 便89 §9 是正(sol/裁定_246_便89検収と定理CENT.md 差戻し5「証明書は
##  judge 規約での versioned 再発行が必要」): W-CENT-B(n=18)の cert を、
##  search/probe/wac_v1/centb_cert.g の手書き規約(mathematician_handwritten)
##  ではなく、**judge 規約**(左共役 -- docs/notes/hexagon_orientation_ruling_v1.md
##  §1 が正本: f_judge = f_hand^{-1})で再発行する。構成は wall2_cert_judge.g
##  と完全並行(witness/窓のみ差し替え)。
##
##  raw measurements only -- 予言値・期待値はコードに書かない(接触遮断)。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
SizeScreen([4096, 0]);;

Read("search/week3-battery-common.g");;
Read("search/probe/wac_v1/_judge_core_extract.g");;

NC := function(p, nn)
  return nn - NrMovedPoints(p) + Length(Cycles(p, MovedPoints(p)));
end;;

Sha256OfString := function(s)
  local tmp, out, f, line;
  tmp := "search/.tmp_centbj_cert_sha.txt";
  out := "search/.tmp_centbj_cert_sha.out";
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
    Error("centb_cert_judge.g: Sha256OfString: sha256sum did not return a hash line");
  fi;
  return line{[1 .. 64]};
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_centbj_cert_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1 .. 64]};
end;;

#############################################################################
## ---- witness (窓 B / W-CENT-B, n=18; centb_cert.g と同一・逐語) ----
#############################################################################
n := 18;;
a1 := ( 1, 2)( 3, 4)( 5, 9)( 6,18)( 7,15)( 8,10)(11,14)(16,17);;
b1 := ( 2, 9, 4)( 5, 8,18)( 6,17,15)( 7,14,10)(11,13,12);;
Snn := SymmetricGroup(n);;  Ann := AlternatingGroup(n);;

Print("=== W-CENT-B 窓 assert (n=", n, ", judge 規約) ===\n");
Print("a1 = ", a1, "\nb1 = ", b1, "\n");

a1sq := (a1^2 = ());;
b1cube := (b1^3 = ());;
kk := NrMovedPoints(a1) / 2;;
jj := NrMovedPoints(b1) / 3;;
signA1 := SignPerm(a1);;
a1type := CycleStructurePerm(a1);;
b1type := CycleStructurePerm(b1);;
w := b1^-1 * a1;;
v := a1 * b1^-1;;
wtype := CycleStructurePerm(w);;
word := Order(w);;
xbtype0 := CycleStructurePerm(w^2);;
xbord0 := Order(w^2);;
genAn := (Group(a1, b1) = Ann);;

reeC := NC(a1, n) + NC(b1, n) + NC(w, n);;
reeGenus := ((3*n - reeC) - 2*n + 2) / 2;;

aE := a1 * (n+1, n+3);;
bE := b1 * (n+1, n+3, n+2);;
s1 := bE^-1 * aE;;
s2 := aE * bE^2;;
braidHolds := (s1*s2*s1 = s2*s1*s2);;

W := MakeWindow(s1, s2);;
one := Identity(W.Bq);;
cIsOne := (W.c = one);;
pEqAn := (W.PN = Ann);;
Esize := Size(Group(aE, bE));;
EEqSixAn := (Esize = 6 * Size(Ann));;
Nord := W.Nord;;
charmingSet := Filtered([0 .. Nord-1], z -> Gcd(2*z+1, Nord) = 1);;
cm := Length(charmingSet);;

Print("  a1^2=1 ", a1sq, "  b1^3=1 ", b1cube, "  k=", kk, "  j=", jj,
      "  sign(a1)=", signA1, "\n");
Print("  a1 型 ", a1type, "  b1 型 ", b1type, "\n");
Print("  w 型 ", wtype, " ord ", word, "    xbar=w^2 型 ", xbtype0, " ord ", xbord0, "\n");
Print("  <a1,b1> = A_", n, " ? ", genAn, "\n");
Print("  Ree: c(a1)+c(b1)+c(w) = ", reeC, "   n+2 = ", n+2, "   genus = ", reeGenus, "\n");
Print("  braid ", braidHolds, "   c=1 ", cIsOne, "   P=A_", n, " ? ", pEqAn,
      "   |E|=6|A_", n, "| ? ", EEqSixAn, "\n");
Print("  N_ord = ", Nord, "   c_m = ", cm, "\n");

#############################################################################
## ---- (ii) C_Sn(w0) の位数・構造・可解性 ----
#############################################################################
Cw := Centralizer(Snn, w);;
CwSize := Size(Cw);;
CwStruct := StructureDescription(Cw);;
CwSolvable := IsSolvable(Cw);;
StabXbar := Centralizer(Snn, W.x);;
StabXbarSize := Size(StabXbar);;
StabXbarSolvable := IsSolvable(StabXbar);;
Print("\n=== C_S", n, "(w0) ===\n");
Print("  |C_S", n, "(w0)| = ", CwSize, "   構造 ", CwStruct, "   可解? ", CwSolvable, "\n");
Print("  |Stab(xbar)| = ", StabXbarSize, "   可解? ", StabXbarSolvable, "\n");

#############################################################################
## ---- (iii) SURV 構成 judge 規約 fj=a1*(a1^z) の全数検算(wall2_cert_judge.g
## と同一式・出典 docs/notes/hexagon_orientation_ruling_v1.md §3) ----
#############################################################################
Cv := Centralizer(Snn, v);;
CvSize := Size(Cv);;
Print("\n=== SURV 全数検算(judge 規約, |C_S", n, "(v)| = ", CvSize, ") ===\n");
passCount := 0;;  hexFail := 0;;  genFail := 0;;  alphas := [];;
for z in Elements(Cv) do
  fj := a1 * (a1^z);;
  if not (AbstractProd([fj, TH(W, fj)]) = one and RtOf(W, 0, fj) = W.c^0) then
    hexFail := hexFail + 1;
  elif Group(W.x, AbstractProd([fj^-1, W.y, fj])) <> W.PN then
    genFail := genFail + 1;
  else
    passCount := passCount + 1;
    Add(alphas, a1 * z * a1);
  fi;
od;
Print("  通過 = ", passCount, "   hexagon 落ち = ", hexFail, "   全射 落ち = ", genFail,
      "   合計 = ", passCount + hexFail + genFail, "\n");

XiIm := Group(alphas);;
XiImSize := Size(XiIm);;
XiImStruct := StructureDescription(XiIm);;
XiImSolvable := IsSolvable(XiIm);;
XiEqCw := (XiIm = Cw);;
Print("  Xi 像位数 = ", XiImSize, "   構造 ", XiImStruct, "   可解? ", XiImSolvable,
      "   = C_S", n, "(w0) ? ", XiEqCw, "\n");

#############################################################################
## ---- (iv) LID-1 canonical string + SHA-256 ----
#############################################################################
lid1Str := Concatenation("LID1/v1|id=W-CENT-B|orient=judge|n=", String(n),
             "|a1=", String(a1), "|b1=", String(b1),
             "|S1=", String(s1), "|S2=", String(s2));;
lid1Sha := Sha256OfString(lid1Str);;
Print("\n  LID-1 = ", lid1Str, "\n  LID-1 sha256 = ", lid1Sha, "\n");

selfSha := ComputeSha256File("search/probe/wac_v1/centb_cert_judge.g");;

#############################################################################
## ---- JSON 出力 ----
#############################################################################
cert := Concatenation(
  "{\n",
  "  \"schema\":\"wac_v1-centb-cert/v2-judge\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/centb_cert_judge.g\",\n",
  "  \"window_label\":\"W-CENT-B\",\n",
  "  \"f_orientation\":\"judge\",\n",
  "  \"source_witness\":\"ops/express/20260731_数学者Opus_壁到達と窓2枚.md 窓B(判別), 逐語(centb_cert.g と同一witness)\",\n",
  "  \"note\":\"raw measurements only -- 予言値/期待値はコードに書かず、全て計算値をそのまま記録する。W(x,y,c,Bq,PN,N_ord)は search/probe/wac_v1/_judge_core_extract.g(kerchi-judge.g 146-165行のsed逐語抽出、改変ゼロ)のMakeWindowを再利用。hexagon判定はjudgeの実物条件(AbstractProd([fj,TH(W,fj)])=1 かつ RtOf(W,0,fj)=c^0)をfj=a1*(a1^z)(訂正版定理SURV, judge規約, docs/notes/hexagon_orientation_ruling_v1.md §3)に適用 -- fj = f_hand^{-1}(同note §1.4)。sat_l1_probe17.gが実証済みの式をcert化しただけで判定ロジック自体は無改変。旧cert centb_cert_20260731.json(mathematician_handwritten, f_orientation欄なし)は非上書き・履歴として残置。\",\n",
  "  \"n\":", String(n), ",\n",
  "  \"a1\":", JStr(String(a1)), ",\n",
  "  \"b1\":", JStr(String(b1)), ",\n",
  "  \"window_asserts\":{\n",
  "    \"a1_sq_eq_1\":", JB(a1sq), ",\n",
  "    \"b1_cube_eq_1\":", JB(b1cube), ",\n",
  "    \"k\":", String(kk), ",\n",
  "    \"j\":", String(jj), ",\n",
  "    \"sign_a1\":", String(signA1), ",\n",
  "    \"a1_cycle_type\":", JStr(String(a1type)), ",\n",
  "    \"b1_cycle_type\":", JStr(String(b1type)), ",\n",
  "    \"w0_cycle_type\":", JStr(String(wtype)), ",\n",
  "    \"w0_order\":", String(word), ",\n",
  "    \"xbar_cycle_type\":", JStr(String(xbtype0)), ",\n",
  "    \"xbar_order\":", String(xbord0), ",\n",
  "    \"gen_eq_An\":", JB(genAn), ",\n",
  "    \"ree_sum\":", String(reeC), ",\n",
  "    \"ree_n_plus_2\":", String(n+2), ",\n",
  "    \"ree_genus\":", String(reeGenus), ",\n",
  "    \"braid_holds\":", JB(braidHolds), ",\n",
  "    \"c_eq_identity\":", JB(cIsOne), ",\n",
  "    \"P_eq_An\":", JB(pEqAn), ",\n",
  "    \"E_size\":", String(Esize), ",\n",
  "    \"E_eq_6_An\":", JB(EEqSixAn), ",\n",
  "    \"N_ord\":", String(Nord), ",\n",
  "    \"charming_count\":", String(cm), "\n",
  "  },\n",
  "  \"centralizer_w0\":{\n",
  "    \"size\":", String(CwSize), ",\n",
  "    \"structure_description\":", JStr(CwStruct), ",\n",
  "    \"solvable\":", JB(CwSolvable), "\n",
  "  },\n",
  "  \"centralizer_xbar\":{\n",
  "    \"size\":", String(StabXbarSize), ",\n",
  "    \"solvable\":", JB(StabXbarSolvable), "\n",
  "  },\n",
  "  \"surv_scan\":{\n",
  "    \"Cv_size\":", String(CvSize), ",\n",
  "    \"pass_count\":", String(passCount), ",\n",
  "    \"hexagon_fail_count\":", String(hexFail), ",\n",
  "    \"generation_fail_count\":", String(genFail), ",\n",
  "    \"total_checked\":", String(passCount + hexFail + genFail), "\n",
  "  },\n",
  "  \"xi_image\":{\n",
  "    \"size\":", String(XiImSize), ",\n",
  "    \"structure_description\":", JStr(XiImStruct), ",\n",
  "    \"solvable\":", JB(XiImSolvable), ",\n",
  "    \"eq_centralizer_w0\":", JB(XiEqCw), "\n",
  "  },\n",
  "  \"lid1\":{\n",
  "    \"canonical_string\":", JStr(lid1Str), ",\n",
  "    \"sha256\":", JStr(lid1Sha), "\n",
  "  },\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), "\n",
  "  }\n",
  "}\n");;

WriteFile("search/certs/centb_cert_judge_20260731.json", cert);;
Print("\nWrote search/certs/centb_cert_judge_20260731.json\n");
Print("\nCENTB_CERT_JUDGE_DONE\n");
QUIT;
