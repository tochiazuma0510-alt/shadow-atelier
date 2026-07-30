#############################################################################
## search/probe/wac_v1/centb_cert.g
##  裁定241 工程1(便89監査資料): W-CENT-B(n=18)の再走可能・独立 cert 生成 probe。
##  witness (a1,b1) は ops/express/20260731_数学者Opus_壁到達と窓2枚.md 窓B
##  (判別)から逐語。検算ロジックは search/probe/wac_v1/sat_l1_probe13.g を
##  踏襲するが、hexagon 判定式は自前で再導出せず、search/kerchi-judge.g
##  (JUDGE_LIBRARY_ONLY モード)の MakeWindow/TT/RtOf をそのまま呼ぶ
##  (探索器内の再利用であり、照合器との分離は破らない -- 照合はこの JSON
##  だけを入力にする別プロセスが担う)。
##  raw measurements only -- 予言値・期待値はコードに書かない(接触遮断)。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
SizeScreen([4096, 0]);;

JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");

NC := function(p, nn)
  return nn - NrMovedPoints(p) + Length(Cycles(p, MovedPoints(p)));
end;;

Sha256OfString := function(s)
  local tmp, out, f, line;
  tmp := "search/.tmp_centb_cert_sha.txt";
  out := "search/.tmp_centb_cert_sha.out";
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
    Error("centb_cert.g: Sha256OfString: sha256sum did not return a hash line");
  fi;
  return line{[1 .. 64]};
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_centb_cert_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1 .. 64]};
end;;

#############################################################################
## ---- witness (窓 B / W-CENT-B, n=18; 速達文書の窓Bから逐語) ----
#############################################################################
n := 18;;
a1 := ( 1, 2)( 3, 4)( 5, 9)( 6,18)( 7,15)( 8,10)(11,14)(16,17);;
b1 := ( 2, 9, 4)( 5, 8,18)( 6,17,15)( 7,14,10)(11,13,12);;
Snn := SymmetricGroup(n);;  Ann := AlternatingGroup(n);;

Print("=== W-CENT-B 窓 assert (n=", n, ") ===\n");
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
cIsOne := (W.c = Identity(W.Bq));;
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
## ---- (iii) SURV 構成 f_z=(a1^z)a1 の全数検算 ----
## NOTE (implementer, 実測で判明した逸脱): 当初 kerchi-judge.g の RtOf/TT
## (JUDGE_LIBRARY_ONLY 再利用)を hexagon 判定に流用しようとしたが、
## AbstractProd の反転規約(kerchi-judge.g 自身のコメントが警告している
## 「見た目 f^-1*w*f だが実際は f*w*f^-1」の罠)のもとで RtOf(W,0,f)=c^0 を
## 具体的な witness で評価すると、probe13/probe11(数学者 Opus 5 検算済み・
## 速達文書の「全通過(落ち0)」の根拠)の手書き二式と実データ上で不一致に
## なることを診断で確認した(scratchpad/diag_hex.g、n=18 の非自明な f で
## eq1=eq2=true だが RtOf(W,0,f)=c^0 は false)。RtOf は m,f の一般形の
## 判定式であり、SURV 定理の f_z=(a1^z)a1 構成に対する (3.3)(3.4) の
## 直書き式(probe11/13)とは異なる式になっている可能性が高い -- これは
## この場で司令塔が裁定すべき数学判断であり、実装担当が黙って選ぶべき
## ものではないため、ここでは probe11/probe13 の検算済み式をそのまま
## 再利用する(kerchi-judge の RtOf は不採用、理由を cert にも記録)。
#############################################################################
Cv := Centralizer(Snn, v);;
CvSize := Size(Cv);;
Print("\n=== SURV 全数検算 (|C_S", n, "(v)| = ", CvSize, ") ===\n");
passCount := 0;;  hexFail := 0;;  genFail := 0;;  alphas := [];;
for z in Elements(Cv) do
  f := (a1^z) * a1;
  if not (s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f) then
    hexFail := hexFail + 1;
  elif Group(W.x, W.y^f) <> W.PN then
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
lid1Str := Concatenation("LID1/v1|id=W-CENT-B|n=", String(n),
             "|a1=", String(a1), "|b1=", String(b1),
             "|S1=", String(s1), "|S2=", String(s2));;
lid1Sha := Sha256OfString(lid1Str);;
Print("\n  LID-1 = ", lid1Str, "\n  LID-1 sha256 = ", lid1Sha, "\n");

selfSha := ComputeSha256File("search/probe/wac_v1/centb_cert.g");;

#############################################################################
## ---- JSON 出力 ----
#############################################################################
cert := Concatenation(
  "{\n",
  "  \"schema\":\"wac_v1-centb-cert/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/centb_cert.g\",\n",
  "  \"window_label\":\"W-CENT-B\",\n",
  "  \"source_witness\":\"ops/express/20260731_数学者Opus_壁到達と窓2枚.md 窓B(判別), 逐語\",\n",
  "  \"note\":\"raw measurements only -- 予言値/期待値はコードに書かず、全て計算値をそのまま記録する。W(x,y,c,Bq,PN,N_ord)は search/kerchi-judge.g (JUDGE_LIBRARY_ONLY) の MakeWindow を再利用。hexagon判定は同ファイルの RtOf ではなく search/probe/wac_v1/sat_l1_probe13.g の検算済み手書き式(s1*f^-1*s2*f=f^-1*s1*s2 かつ f^-1*s2*f*s1=s2*s1*f)をそのまま採用 -- RtOf(m=0)は AbstractProd の反転規約下で実データ上この式と不一致(診断: scratchpad/diag_hex.g)。要司令塔裁定、逸脱として報告済み。\",\n",
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

WriteFile("search/certs/centb_cert_20260731.json", cert);;
Print("\nWrote search/certs/centb_cert_20260731.json\n");
Print("\nCENTB_CERT_DONE\n");
QUIT;
