#############################################################################
## search/probe/wac_v1/dl3_search.g
##  T5 標的: w0 の巡回型が (ell, 1^4) (ell 奇素数, n=ell+4) の窓の実現対
##  (a1,b1) を探す。a1^2=1, b1^3=1, w:=b1^-1*a1 の型が (ell,1^4),
##  <a1,b1> in {A_n, S_n}。ell=7,11,13,17,19,23 を順に走査、最初に見つかった
##  ell で打ち切る。(k,j) = a1 の互換本数 / b1 の3-巡回本数は
##  Riemann-Hurwitz/Ree 予算 c(a1)+c(b1)+c(w) <= n+2 をコードで枚挙して試す
##  (等号=種数0だけでなく不等号側=種数>0も試す)。
##
##  raw measurements only -- 予言値/期待値はコードに書かない(接触遮断:
##  ideas/・sol/・docs/notes/sat_l1_v1.md は本スクリプト作成時に未読)。
##  見つかったら wall2_cert.g と同じ検算一式(窓 assert・C(w0) の位数/構造/
##  導来長・SURV 全数検算)を行い cert を出す。
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
  tmp := "search/.tmp_dl3_cert_sha.txt";
  out := "search/.tmp_dl3_cert_sha.out";
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
    Error("dl3_search.g: Sha256OfString: sha256sum did not return a hash line");
  fi;
  return line{[1 .. 64]};
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_dl3_cert_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1 .. 64]};
end;;

#############################################################################
## ---- MakeCyc / w0 builder ----
#############################################################################
MakeCyc := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;

#############################################################################
## ---- 2-opt local search Hunt (probe12 の Hunt を一般化: k 本の互換を
##      探索し、b1 := a1*w0^-1 の b1^3=1 (=> 型が(3^*,1^*)) を目標にする) ----
#############################################################################
Hunt := function(n, w0, k, maxRestart, maxStep, timeCapMs)
  local rs, pts, m, d, step, i, j, m2, d2, mk, Def, t0;
  mk := function(mm) return Product(List(mm, p -> (p[1],p[2])), ()); end;
  Def := function(mm) return NrMovedPoints((mk(mm)*w0^-1)^3); end;
  t0 := Runtime();
  for rs in [1..maxRestart] do
    if Runtime() - t0 > timeCapMs then
      return rec(a1 := fail, timedOut := true, restarts := rs);
    fi;
    pts := Shuffle(ShallowCopy([1..n]));
    m := List([1..k], i -> [pts[2*i-1], pts[2*i]]);
    d := Def(m);
    for step in [1..maxStep] do
      if d = 0 then
        return rec(a1 := mk(m), timedOut := false, restarts := rs, steps := step);
      fi;
      i := Random([1..k]); j := Random([1..k]);
      m2 := List(m, ShallowCopy);
      if i = j then
        continue;
      elif Random([1,2]) = 1 then
        m2[i] := [m[i][1], m[j][1]]; m2[j] := [m[i][2], m[j][2]];
      else
        m2[i] := [m[i][1], m[j][2]]; m2[j] := [m[i][2], m[j][1]];
      fi;
      d2 := Def(m2);
      if d2 <= d then m := m2; d := d2; fi;
    od;
  od;
  return rec(a1 := fail, timedOut := false, restarts := maxRestart);
end;;

#############################################################################
## ---- main scan over ell ----
#############################################################################
ELLS := [7, 11, 13, 17, 19, 23];;
DL3_SEED := 20260731;;
Reset(GlobalMersenneTwister, DL3_SEED);;

foundEll := fail;;
foundA1 := fail;; foundB1 := fail;; foundW0 := fail;; foundGen := fail;;
ellLog := [];;

TIME_CAP_PER_K_MS := 40000;;   ## 40s per k value (2-opt hunt)
TOTAL_TIME_CAP_MS := 480000;;  ## 8 minutes total scan budget (leaves headroom for cert compute)
scanT0 := Runtime();;

for ell in ELLS do
  if foundEll <> fail then break; fi;
  n := ell + 4;;
  Sn := SymmetricGroup(n);;
  An := AlternatingGroup(n);;
  w0 := MakeCyc([1..ell]);;   ## fixes ell+1..ell+4
  NCw0 := NC(w0, n);;
  signW0 := SignPerm(w0);;
  Print("\n#####################################################\n");
  Print("## ell=", ell, "  n=", n, "  w0 type=", CycleStructurePerm(w0),
        "  sign(w0)=", signW0, "  NC(w0)=", NCw0, "\n");
  Print("#####################################################\n");

  ## enumerate feasible k (parity from sign(w0)=sign(a1)=(-1)^k, and
  ## Ree budget k+2j >= n+NCw0-2 achievable with j <= Int(n/3))
  jmax := Int(n/3);;
  kList := [];;
  for k in [0 .. Int(n/2)] do
    parityOk := ((-1)^k = signW0);;
    jNeed := (n + NCw0 - 2 - k);;   ## need 2j >= jNeed, i.e. j >= jNeed/2
    budgetOk := (2*jmax >= jNeed);;
    if parityOk and budgetOk then
      Add(kList, k);;
    fi;
  od;
  Print("  feasible k list (parity+Ree-budget-achievable) = ", kList, "\n");

  ellRec := rec(ell := ell, n := n, feasible_k := ShallowCopy(kList), attempts := []);;

  for k in kList do
    if foundEll <> fail then break; fi;
    if Runtime() - scanT0 > TOTAL_TIME_CAP_MS then
      Print("  [total time cap reached -- skipping remaining k/ell]\n");
      Add(ellRec.attempts, rec(k := k, skipped := true, reason := "total_time_cap"));
      continue;
    fi;
    Print("  -- trying k=", k, " (2-opt hunt) ...\n");
    hres := Hunt(n, w0, k, 400, 4000, TIME_CAP_PER_K_MS);;
    if hres.a1 = fail then
      Print("     NO HIT (timedOut=", hres.timedOut, ", restarts=", hres.restarts, ")\n");
      Add(ellRec.attempts, rec(k := k, hit := false, timed_out := hres.timedOut,
                                restarts := hres.restarts));
    else
      a1 := hres.a1;;
      b1 := a1 * w0^-1;;
      jActual := NrMovedPoints(b1) / 3;;
      reeC := NC(a1,n) + NC(b1,n) + NCw0;;
      reeOk := (reeC <= n+2);;
      G := Group(a1, b1);;
      genLabel := "other";;
      if Size(G) = Size(Sn) and G = Sn then genLabel := "S_n";
      elif Size(G) = Size(An) and G = An then genLabel := "A_n"; fi;
      Print("     HIT: k=", k, " j=", jActual, " reeC=", reeC, " (<=", n+2, "? ", reeOk,
            ")  <a1,b1>=", genLabel, " |G|=", Size(G), "\n");
      Add(ellRec.attempts, rec(k := k, hit := true, j := jActual, ree_sum := reeC,
                                ree_ok := reeOk, gen := genLabel, group_order := Size(G)));
      if genLabel = "A_n" or genLabel = "S_n" then
        foundEll := ell;; foundA1 := a1;; foundB1 := b1;; foundW0 := w0;;
        foundGen := genLabel;;
      fi;
    fi;
  od;
  Add(ellLog, ellRec);;
od;

Print("\n=== SCAN SUMMARY ===\n");
for r in ellLog do
  Print("ell=", r.ell, " n=", r.n, " feasible_k=", r.feasible_k, "\n");
  for a in r.attempts do
    Print("   ", a, "\n");
  od;
od;

if foundEll = fail then
  Print("\nNO REALIZATION PAIR FOUND for any ell in ", ELLS, "\n");
  Print("\nDL3_SEARCH_NO_HIT\n");

  ## write a negative-result cert honestly recording every attempt
  attemptsJson := [];;
  for r in ellLog do
    attJson := [];;
    for a in r.attempts do
      if IsBound(a.skipped) then
        Add(attJson, Concatenation("{\"k\":", String(a.k),
              ",\"skipped\":true,\"reason\":", JStr(a.reason), "}"));
      elif a.hit = false then
        Add(attJson, Concatenation("{\"k\":", String(a.k), ",\"hit\":false,\"timed_out\":",
              JB(a.timed_out), ",\"restarts\":", String(a.restarts), "}"));
      else
        Add(attJson, Concatenation("{\"k\":", String(a.k), ",\"hit\":true,\"j\":", String(a.j),
              ",\"ree_sum\":", String(a.ree_sum), ",\"ree_ok\":", JB(a.ree_ok),
              ",\"gen\":", JStr(a.gen), ",\"group_order\":", String(a.group_order), "}"));
      fi;
    od;
    Add(attemptsJson, Concatenation("{\"ell\":", String(r.ell), ",\"n\":", String(r.n),
          ",\"feasible_k\":", JArr(List(r.feasible_k, String)),
          ",\"attempts\":", JArr(attJson), "}"));
  od;

  negCert := Concatenation(
    "{\n",
    "  \"schema\":\"wac_v1-dl3-cert/v1\",\n",
    "  \"generated_by\":\"search/probe/wac_v1/dl3_search.g\",\n",
    "  \"window_label\":\"T5-dl3\",\n",
    "  \"result\":\"NO_HIT\",\n",
    "  \"note\":\"raw measurements only -- (ell,1^4) 実現対は与えられた ell 走査・(k,j)枚挙・2-opt hunt 予算内では見つからなかった。非存在の証明ではない(UNKNOWN)。\",\n",
    "  \"ells_scanned\":", JArr(List(ELLS, String)), ",\n",
    "  \"per_ell_log\":", JArr(attemptsJson), "\n",
    "}\n");;
  WriteFile("search/certs/dl3_cert_20260731.json", negCert);;
  Print("\nWrote search/certs/dl3_cert_20260731.json (NO_HIT)\n");

else

#############################################################################
## ---- FOUND: full window/cert computation, mirrors wall2_cert.g ----
#############################################################################
n := foundEll + 4;;
a1 := foundA1;; b1 := foundB1;; w0Rep := foundW0;;
Snn := SymmetricGroup(n);;  Ann := AlternatingGroup(n);;

Print("\n=== FOUND: ell=", foundEll, "  n=", n, "  gen=", foundGen, " ===\n");
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
genSn := (Group(a1, b1) = Snn);;

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
Print("  <a1,b1> = A_", n, " ? ", genAn, "   = S_", n, " ? ", genSn, "\n");
Print("  Ree: c(a1)+c(b1)+c(w) = ", reeC, "   n+2 = ", n+2, "   genus = ", reeGenus, "\n");
Print("  braid ", braidHolds, "   c=1 ", cIsOne, "   P=A_", n, " ? ", pEqAn,
      "   |E|=6|A_", n, "| ? ", EEqSixAn, "\n");
Print("  N_ord = ", Nord, "   c_m = ", cm, "\n");

#############################################################################
## ---- (ii) C_Sn(w0) の位数・構造・導来長・可解性 ----
#############################################################################
Cw := Centralizer(Snn, w);;
CwSize := Size(Cw);;
CwStruct := StructureDescription(Cw);;
CwSolvable := IsSolvable(Cw);;
if CwSolvable then CwDerivedLength := DerivedLength(Cw); else CwDerivedLength := -1; fi;
StabXbar := Centralizer(Snn, W.x);;
StabXbarSize := Size(StabXbar);;
StabXbarSolvable := IsSolvable(StabXbar);;
Print("\n=== C_S", n, "(w0) ===\n");
Print("  |C_S", n, "(w0)| = ", CwSize, "   構造 ", CwStruct, "   可解? ", CwSolvable,
      "   導来長 ", CwDerivedLength, "\n");
Print("  |Stab(xbar)| = ", StabXbarSize, "   可解? ", StabXbarSolvable, "\n");

#############################################################################
## ---- (iii) SURV 構成 f_z=(a1^z)a1 の全数検算 (wall2_cert.g と同じ judge
## 規約: RtOf は不採用 -- sat_l1_probe11/13 の検算済み手書き式を使う) ----
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
if XiImSolvable then XiImDerivedLength := DerivedLength(XiIm); else XiImDerivedLength := -1; fi;
XiEqCw := (XiIm = Cw);;
Print("  Xi 像位数 = ", XiImSize, "   構造 ", XiImStruct, "   可解? ", XiImSolvable,
      "   導来長 ", XiImDerivedLength, "   = C_S", n, "(w0) ? ", XiEqCw, "\n");

#############################################################################
## ---- (iv) LID-1 canonical string + SHA-256 ----
#############################################################################
lid1Str := Concatenation("LID1/v1|id=T5-dl3|ell=", String(foundEll), "|n=", String(n),
             "|a1=", String(a1), "|b1=", String(b1),
             "|S1=", String(s1), "|S2=", String(s2));;
lid1Sha := Sha256OfString(lid1Str);;
Print("\n  LID-1 = ", lid1Str, "\n  LID-1 sha256 = ", lid1Sha, "\n");

selfSha := ComputeSha256File("search/probe/wac_v1/dl3_search.g");;

#############################################################################
## ---- scan log JSON (all ell attempted, honest record) ----
#############################################################################
attemptsJson := [];;
for r in ellLog do
  attJson := [];;
  for a in r.attempts do
    if IsBound(a.skipped) then
      Add(attJson, Concatenation("{\"k\":", String(a.k),
            ",\"skipped\":true,\"reason\":", JStr(a.reason), "}"));
    elif a.hit = false then
      Add(attJson, Concatenation("{\"k\":", String(a.k), ",\"hit\":false,\"timed_out\":",
            JB(a.timed_out), ",\"restarts\":", String(a.restarts), "}"));
    else
      Add(attJson, Concatenation("{\"k\":", String(a.k), ",\"hit\":true,\"j\":", String(a.j),
            ",\"ree_sum\":", String(a.ree_sum), ",\"ree_ok\":", JB(a.ree_ok),
            ",\"gen\":", JStr(a.gen), ",\"group_order\":", String(a.group_order), "}"));
    fi;
  od;
  Add(attemptsJson, Concatenation("{\"ell\":", String(r.ell), ",\"n\":", String(r.n),
        ",\"feasible_k\":", JArr(List(r.feasible_k, String)),
        ",\"attempts\":", JArr(attJson), "}"));
od;

#############################################################################
## ---- JSON 出力 ----
#############################################################################
cert := Concatenation(
  "{\n",
  "  \"schema\":\"wac_v1-dl3-cert/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/dl3_search.g\",\n",
  "  \"window_label\":\"T5-dl3\",\n",
  "  \"result\":\"HIT\",\n",
  "  \"found_ell\":", String(foundEll), ",\n",
  "  \"note\":\"raw measurements only -- 予言値/期待値はコードに書かず、全て計算値をそのまま記録する。W(x,y,c,Bq,PN,N_ord)は search/kerchi-judge.g (JUDGE_LIBRARY_ONLY) の MakeWindow を再利用。hexagon判定は同ファイルの RtOf ではなく search/probe/wac_v1/sat_l1_probe11.g の検算済み手書き式(s1*f^-1*s2*f=f^-1*s1*s2 かつ f^-1*s2*f*s1=s2*s1*f)をそのまま採用(wall2_cert.g と同じ judge 規約)。a1 は 2-opt 山登り(probe12 の Hunt を一般化)で構成、seed=20260731。\",\n",
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
  "    \"gen_eq_Sn\":", JB(genSn), ",\n",
  "    \"gen_label\":", JStr(foundGen), ",\n",
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
  "    \"solvable\":", JB(CwSolvable), ",\n",
  "    \"derived_length\":", String(CwDerivedLength), "\n",
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
  "    \"derived_length\":", String(XiImDerivedLength), ",\n",
  "    \"eq_centralizer_w0\":", JB(XiEqCw), "\n",
  "  },\n",
  "  \"scan_log\":{\n",
  "    \"ells_scanned\":", JArr(List(ELLS, String)), ",\n",
  "    \"per_ell\":", JArr(attemptsJson), "\n",
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

WriteFile("search/certs/dl3_cert_20260731.json", cert);;
Print("\nWrote search/certs/dl3_cert_20260731.json\n");
Print("\nDL3_CERT_DONE\n");

fi;
QUIT;
