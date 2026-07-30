#############################################################################
## search/probe/wac_v1/sat_l1_probe14.g
##  【裁定用】hexagon 判定式の非等価の原因特定。
##  judge(kerchi-judge.g)は簡約 hexagon (3.10)(3.11) を AbstractProd(反転規約)
##  で書く:  Dlt := AbstractProd([s1,s2,s1]) = GAP s1*s2*s1
##           dlt := AbstractProd([s1,s2])    = GAP s2*s1     <-- ここが要点
##  私の probe は literal (3.3)(3.4) を GAP 語順そのままで書いた。
##  代数的には  私 = {(f*a)^2=1, (f*b^-1)^3=1},  a=s1*s2*s1, b=s1*s2
##             judge = {(f*a)^2=1, (f*dlt^-1)^3=1}, dlt=s2*s1
##  ==> 差は b=s1*s2 と dlt=s2*s1 の一点のみ。どちらが tau (x->y->z->x) か。
##  (A) tau の同定: theta,tau を x,y,z 上で直接検査
##  (B) 4 通りの判定式の解集合を比較(n=10, n=18)
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
Diag := function(nn, a1, b1, label)
  local Snn, aE, bE, s1, s2, xb, yb, PN, a, b, dlt, zb1, zb2, g, nm,
        Sol, cand, f, Stb, CSy, al, cc, res, cands, i;
  Snn := SymmetricGroup(nn);
  aE := a1*(nn+1,nn+3); bE := b1*(nn+1,nn+3,nn+2);
  s1 := bE^-1*aE; s2 := aE*bE^2;
  xb := s1^2; yb := s2^2; PN := Group(xb,yb);
  a := s1*s2*s1; b := s1*s2; dlt := s2*s1;
  Print("\n===== ", label, " n=", nn, " =====\n");
  Print("  a=s1*s2*s1 (=Dlt) ord ", Order(a), "   b=s1*s2 ord ", Order(b),
        "   dlt=s2*s1 ord ", Order(dlt), "   b=dlt? ", b=dlt, "\n");
  Print("  dlt = b^s1 ? ", dlt = b^s1, "\n");
  ## ---- (A) theta の同定 ----
  Print("  --- theta (x<->y) ---\n");
  Print("    a*xb*a = yb ?  ", a*xb*a = yb, "     (a は対合ゆえ左右同一)\n");
  Print("    a*yb*a = xb ?  ", a*yb*a = xb, "\n");
  ## ---- (A) tau の同定: x -> y -> z -> x ----
  zb1 := (xb*yb)^-1;   ## GAP 語順そのまま
  zb2 := (yb*xb)^-1;   ## paper "xy" の反転読み
  Print("  --- tau (x->y->z->x) の候補 4 通り ---\n");
  cands := [ ["u -> b^-1*u*b   (右共役 b)",   u -> b^-1*u*b],
             ["u -> b*u*b^-1   (左共役 b)",   u -> b*u*b^-1],
             ["u -> dlt^-1*u*dlt (右共役 dlt)", u -> dlt^-1*u*dlt],
             ["u -> dlt*u*dlt^-1 (左共役 dlt)", u -> dlt*u*dlt^-1] ];
  for i in [1..4] do
    g := cands[i][2];
    Print("    ", cands[i][1], " :  x->y ? ", g(xb) = yb,
          "   y->z1 ? ", g(yb) = zb1, "   y->z2 ? ", g(yb) = zb2,
          "   z1->x ? ", g(zb1) = xb, "   z2->x ? ", g(zb2) = xb, "\n");
  od;
  ## ---- (B) 4 通りの判定式の解集合 ----
  Stb := Centralizer(Snn, xb); CSy := Centralizer(Snn, yb);
  res := [ [], [], [], [], [] ];
  for al in Elements(Stb) do
    for cc in Elements(CSy) do
      f := cc*al;
      if SignPerm(f) <> 1 then continue; fi;
      ## 1: 私の literal (3.3)(3.4) (GAP 語順そのまま)
      if s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f then Add(res[1], f); fi;
      ## 2: (3.3)(3.4) を反転して読んだもの
      if f*s2*f^-1*s1 = s2*s1*f^-1 and s1*f*s2*f^-1 = f*s1*s2 then Add(res[2], f); fi;
      ## 3: judge 型  {(f*a)^2=1, (f*dlt^-1)^3=1}
      if (f*a)^2 = () and (f*dlt^-1)^3 = () then Add(res[3], f); fi;
      ## 4: 私の簡約形 {(f*a)^2=1, (f*b^-1)^3=1}
      if (f*a)^2 = () and (f*b^-1)^3 = () then Add(res[4], f); fi;
      ## 5: judge 型の左共役版 {(f*a)^2=1, (f*dlt)^3=1}
      if (f*a)^2 = () and (f*dlt)^3 = () then Add(res[5], f); fi;
    od;
  od;
  Print("  --- 解集合の大きさ(生成条件は未適用)---\n");
  Print("    [1] literal (3.3)(3.4) GAP 語順      : ", Length(res[1]), "\n");
  Print("    [2] (3.3)(3.4) 反転読み              : ", Length(res[2]), "\n");
  Print("    [3] judge 型 (f*a)^2,(f*dlt^-1)^3    : ", Length(res[3]), "\n");
  Print("    [4] 私の簡約形 (f*a)^2,(f*b^-1)^3    : ", Length(res[4]), "\n");
  Print("    [5] (f*a)^2,(f*dlt)^3                : ", Length(res[5]), "\n");
  Print("    集合一致: [1]=[4] ", Set(res[1])=Set(res[4]),
        "   [1]=[3] ", Set(res[1])=Set(res[3]),
        "   [2]=[3] ", Set(res[2])=Set(res[3]),
        "   [2]=[5] ", Set(res[2])=Set(res[5]),
        "   [1]=[2] ", Set(res[1])=Set(res[2]), "\n");
  return true;
end;;

Diag(10, ( 1, 2)( 3, 6)( 7,10), ( 2,10, 6)( 3, 5, 4)( 7, 9, 8),
     "W-E-A10-5x2t0 (証明書 |ker|=10)");;
Diag(18, ( 1, 2)( 3, 4)( 5, 9)( 6,18)( 7,15)( 8,10)(11,14)(16,17),
     ( 2, 9, 4)( 5, 8,18)( 6,17,15)( 7,14,10)(11,13,12),
     "W-CENT-B (n=18)");;
Print("\nSAT_L1_PROBE14_DONE\n");
QUIT;
