#############################################################################
## search/probe/wac_v1/pent_pi_a5.g
##  実験 PENT-π(裁定 248・ideas_015 §3.2): A₅ 窓 N_A への π-lift
##  (σ₃ ↦ σ₁ による B₄ ↠ B₃ の合成)で pentagon (2.20) を初計測する。
##
##  起草: 司令塔(研究者指示により委譲せず司令塔自身が実装・2026-07-31)。
##
##  数学的根拠(全て画像照合済み・裁定 248 再照合):
##   - pentagon (2.20)(p.13 実物): φ234(f)·φ1,23,4(f)·φ123(f)·N
##       = φ1,2,34(f)·φ12,3,4(f)·N  (PB₄/N 内・paper 積順)
##   - 余面の生成元値 (A.18)(p.49 実物・15 値照合済)
##   - x_ij の定義 (A.2)(A.4)(p.44 実物): x12=σ1², x23=σ2², x13=σ2σ1²σ2⁻¹
##   - well-definedness(p.13 Def 2.6 直後): 判定は f の N_{PB3} 類のみに依存。
##     π-lift では (K_π)_{PB3} = ker(ρ3)∩PB3 = N_A ちょうど(ψ̃_π∘incl = ρ3)
##     ⟹ A₅ の元ごとの判定が well-defined・代表語 1 本で足りる。
##
##  規約: EvalWord は AbstractProd 反転積(paper AB = GAP B*A)。
##  以下の word/eval/pentagon 機構は search/probe/wac_v1/pentagon_check.g
##  (N(34) で論文値 4096/254016 を接触遮断下で完全再現 = 較正 PASS)から
##  逐語コピー(独立再実装の較正を継承するため改変しない)。
##
##  接触遮断: 期待値(arithmetical 4 個の一覧・予言 P-PENT-1 の値)は本
##  ファイルに書かない。突合は司令塔が裁定で行う。
##
##  出力: search/certs/pent_pi_a5_20260731.json(raw measurements only)
#############################################################################

SetPrintFormattingStatus("*stdout*", false);;

#############################################################################
## ---- pentagon_check.g から逐語コピー(較正済み機構・改変禁止) ----
#############################################################################
ImgOfLetter := function(letter, ximg, yimg)
  if letter.g = "x" then return ximg ^ letter.e; else return yimg ^ letter.e; fi;
end;;

EvalWord := function(word, ximg, yimg)
  local val, i;
  val := ximg^0;
  for i in [Length(word), Length(word)-1 .. 1] do
    val := val * ImgOfLetter(word[i], ximg, yimg);
  od;
  return val;
end;;

Comp := function(s, t) return t * s; end;;

PentagonHolds := function(word, cofaces)
  local F123, F234, F12_3_4, F1_23_4, F1_2_34;
  F123    := EvalWord(word, cofaces.c123.x,    cofaces.c123.y);
  F234    := EvalWord(word, cofaces.c234.x,    cofaces.c234.y);
  F12_3_4 := EvalWord(word, cofaces.c12_3_4.x, cofaces.c12_3_4.y);
  F1_23_4 := EvalWord(word, cofaces.c1_23_4.x, cofaces.c1_23_4.y);
  F1_2_34 := EvalWord(word, cofaces.c1_2_34.x, cofaces.c1_2_34.y);
  return (F123 * F1_23_4 * F234) = (F12_3_4 * F1_2_34);
end;;

BuildCofaces := function(g12, g23, g13, g14, g24, g34)
  return rec(
    c123    := rec(x := g12, y := g23),
    c234    := rec(x := g23, y := g34),
    c12_3_4 := rec(x := Comp(g13, g23), y := g34),
    c1_23_4 := rec(x := Comp(g12, g13), y := Comp(g24, g34)),
    c1_2_34 := rec(x := g12, y := Comp(g23, g24))
  );
end;;

BFSFullGroup := function(ximg, yimg, capN)
  local gensBase, wordOf, queue, qi, cur, curWord, gl, gp, nv, capped;
  gensBase := [rec(g:="x",e:=1), rec(g:="x",e:=-1), rec(g:="y",e:=1), rec(g:="y",e:=-1)];
  wordOf := NewDictionary(ximg^0, true);
  AddDictionary(wordOf, ximg^0, []);
  queue := [ ximg^0 ];
  qi := 1; capped := false;
  while qi <= Length(queue) do
    cur := queue[qi]; qi := qi + 1;
    curWord := LookupDictionary(wordOf, cur);
    for gl in gensBase do
      gp := ImgOfLetter(gl, ximg, yimg);
      nv := gp * cur;
      if LookupDictionary(wordOf, nv) = fail then
        if Length(queue) >= capN then
          capped := true;
          break;
        fi;
        AddDictionary(wordOf, nv, Concatenation(curWord, [gl]));
        Add(queue, nv);
      fi;
    od;
    if capped then break; fi;
  od;
  return rec(wordOf := wordOf, elements := queue, capped := capped);
end;;

#############################################################################
## ---- STEP 1: A₅ 窓の再構成(certificates/A1.v2.json の枠組み) ----
##  X, Y は A1.v2.json target_definition のとおり。s3 marking: Δ↦(1 2),
##  δ↦(1 2 3)(tail 点 {6,7,8} 上で (6,7), (6,7,8))。
##  a = s·(6,7), b = t·(6,7,8), σ1 = b⁻¹a, σ2 = ab² (sat_l1 §1 の GAP 規約)。
##  (s,t) は s²=1, t³=1, ⟨s,t⟩=A₅, σ1²|₅=X, σ2²|₅=Y で総当たり同定する。
#############################################################################
X5 := (1,3,2,4,5);;
Y5 := (1,3,4,5,2);;
A5 := AlternatingGroup(5);;

found := [];;
for s in Elements(A5) do
  if s <> () and s^2 = () then
    for t in Elements(A5) do
      if t <> () and t^3 = () then
        a := s * (6,7);
        b := t * (6,7,8);
        s1 := b^-1 * a;
        s2 := a * b^2;
        if s1^2 = X5 and s2^2 = Y5 then
          if Size(Group(s, t)) = 60 then
            Add(found, rec(s := s, t := t, a := a, b := b, s1 := s1, s2 := s2));
          fi;
        fi;
      fi;
    od;
  fi;
od;;

if Length(found) = 0 then
  Error("PENT-PI STOP: no (s,t) realizes the A1.v2 marking under convention s1=b^-1*a, s2=a*b^2");
fi;
Print("STEP1: marking solutions found = ", Length(found), "\n");
W := found[1];;

EWIN := Group(W.a, W.b);;
Print("STEP1: |EWIN| = ", Size(EWIN), "\n");
if Size(EWIN) <> 360 then Error("PENT-PI STOP: |EWIN| <> 360"); fi;

xbar := W.s1^2;;  ybar := W.s2^2;;
P5 := Group(xbar, ybar);;
if Size(P5) <> 60 then Error("PENT-PI STOP: |<xbar,ybar>| <> 60"); fi;

## braid & c asserts(窓 assert)
assert_braid := (W.s1*W.s2*W.s1 = W.s2*W.s1*W.s2);;
## c = x23 x12 x13 (paper) = GAP g13*g12*g23; PB3 では c↦1 のはず
g13_B3 := (W.s1^2) ^ W.s2;;   ## paper σ2σ1²σ2⁻¹ = GAP (S1²)^S2(反転規約の像)
assert_c_triv := (g13_B3 * xbar * ybar = ());;
if not assert_braid then Error("PENT-PI STOP: braid fails"); fi;
if not assert_c_triv then Error("PENT-PI STOP: c does not vanish (x13 convention?)"); fi;
Print("STEP1: braid OK, c->1 OK\n");

#############################################################################
## ---- STEP 2: π-lift(σ3 ↦ σ1)と 6 生成元の像 ----
##  paper (A.2): x12=σ1², x23=σ2², x34=σ3², x13=σ2σ1²σ2⁻¹, x24=σ3σ2²σ3⁻¹,
##  x14=σ3σ2σ1²σ2⁻¹σ3⁻¹。反転規約の像: paper ABC = GAP C*B*A ⟹
##  paper 共役 gXg⁻¹ = GAP X^g。σ3 の像 = S1。
#############################################################################
S1 := W.s1;; S2 := W.s2;; S3 := W.s1;;   ## π-lift: σ3 ↦ σ1

## B4 の 3 関係式(像の上で・assert)
if not (S1*S2*S1 = S2*S1*S2) then Error("PENT-PI STOP: B4 rel 1"); fi;
if not (S2*S3*S2 = S3*S2*S3) then Error("PENT-PI STOP: B4 rel 2"); fi;
if not (S1*S3 = S3*S1) then Error("PENT-PI STOP: B4 rel 3"); fi;

g12 := S1^2;;
g23 := S2^2;;
g34 := S3^2;;
g13 := (S1^2) ^ S2;;
g24 := (S2^2) ^ S3;;
g14 := ((S1^2) ^ S2) ^ S3;;

nondegenerate_x34 := (g34 <> ());;
if not nondegenerate_x34 then Error("PENT-PI STOP: x34 -> 1 (degenerate)"); fi;
Print("STEP2: pi-lift OK, x34 image nontrivial\n");

cofacesPi := BuildCofaces(g12, g23, g13, g14, g24, g34);;

#############################################################################
## ---- STEP 3: A₅ = F2/(K_π)_{F2} の全 60 元の census(π-lift pentagon) ----
##  well-definedness(p.13)+ (K_π)_{PB3} = N_A により、元ごとに BFS の
##  代表語 1 本で判定してよい。
#############################################################################
bfs := BFSFullGroup(xbar, ybar, 100);;
if bfs.capped or Length(bfs.elements) <> 60 then
  Error("PENT-PI STOP: BFS over A5 failed: ", Length(bfs.elements));
fi;

censusPi := [];;
passPi := 0;;
for elt in bfs.elements do
  word := LookupDictionary(bfs.wordOf, elt);
  ok := PentagonHolds(word, cofacesPi);
  if ok then passPi := passPi + 1; fi;
  Add(censusPi, rec(elt := elt, word := word, pass := ok));
od;;
Print("STEP3: pi-lift pentagon census: pass = ", passPi, " / 60\n");

#############################################################################
## ---- STEP 4: PENT-VOID 対照(Prop 3.9 型の退化持ち上げ) ----
##  x14 = x24 = x34 ↦ id, x12 ↦ xbar, x23 ↦ ybar, x13 ↦ ψ(x13)。
##  (注記: この退化像の核が B4-正規である保証は本 probe では確認しない。
##   目的は「退化像では pentagon が刈らない」現象の機械的対照のみ。)
#############################################################################
cofacesVoid := BuildCofaces(xbar, ybar, g13_B3, (), (), ());;
passVoid := 0;;
for elt in bfs.elements do
  word := LookupDictionary(bfs.wordOf, elt);
  if PentagonHolds(word, cofacesVoid) then passVoid := passVoid + 1; fi;
od;;
Print("STEP4: degenerate-lift pentagon census: pass = ", passVoid, " / 60\n");

#############################################################################
## ---- STEP 5: A1.v2.json の 20 shadow の f を census に対応付け ----
##  f_word は [["y",1],["x",-1]] 形式。語順規約が不明なため、両読み
##  (そのまま / 反転)で元を評価し、両方の verdict を記録する(判定は
##  元ごとに well-defined なので、正しい読みの側が正しい verdict)。
#############################################################################
shadowRows := [];;
shadowStream := InputTextFile("search/probe/wac_v1/_pent_pi_shadows.tmp");;
if shadowStream <> fail then
  CloseStream(shadowStream);
fi;

## f_word は司令塔が python で前処理して GAP 読み込み可能な形式にした
## ファイル _pent_pi_shadows.g を Read する(無ければ skip して census のみ)。
shadowsLoaded := false;;
if IsExistingFile("search/probe/wac_v1/_pent_pi_shadows.g") then
  Read("search/probe/wac_v1/_pent_pi_shadows.g");   ## defines SHADOW_LIST
  shadowsLoaded := true;
fi;

EvalFWord := function(fw, ximg, yimg)   ## fw = list of [gen, exp]
  local val, pair;
  val := ximg^0;
  for pair in fw do    ## 読み A: 左から右へ GAP 積
    if pair[1] = "x" then val := val * ximg^pair[2];
    else val := val * yimg^pair[2]; fi;
  od;
  return val;
end;;

EvalFWordRev := function(fw, ximg, yimg)  ## 読み B: 反転積(AbstractProd 型)
  local val, i, pair;
  val := ximg^0;
  for i in [Length(fw), Length(fw)-1 .. 1] do
    pair := fw[i];
    if pair[1] = "x" then val := val * ximg^pair[2];
    else val := val * yimg^pair[2]; fi;
  od;
  return val;
end;;

verdictOfElt := function(elt)
  local r;
  for r in censusPi do
    if r.elt = elt then return r.pass; fi;
  od;
  return fail;
end;;

if shadowsLoaded then
  for sh in SHADOW_LIST do
    eltA := EvalFWord(sh.f_word, xbar, ybar);
    eltB := EvalFWordRev(sh.f_word, xbar, ybar);
    Add(shadowRows, rec(
      m := sh.m,
      f_word := sh.f_word,
      pentagon_readA := verdictOfElt(eltA),
      pentagon_readB := verdictOfElt(eltB),
      reads_agree := (verdictOfElt(eltA) = verdictOfElt(eltB))
    ));
  od;
  Print("STEP5: mapped ", Length(shadowRows), " shadows\n");
else
  Print("STEP5: shadow file not present -- census only\n");
fi;

#############################################################################
## ---- STEP 6: cert 出力 ----
#############################################################################
PermToStr := function(p) local s; s := String(p); return s; end;;
WordToStr := function(word)
  local parts, l;
  parts := [];
  for l in word do Add(parts, Concatenation(l.g, "^", String(l.e))); od;
  return JoinStringsWithSeparator(parts, ".");
end;;

json := "";;
Append(json, "{\n");
Append(json, "\"schema\": \"wac_v1-pent-pi-cert/v1\",\n");
Append(json, "\"generated_by\": \"search/probe/wac_v1/pent_pi_a5.g\",\n");
Append(json, "\"window_label\": \"PENT-PI-A5\",\n");
Append(json, "\"f_orientation\": \"abstractprod_reversed_matching_paB_compAll\",\n");
Append(json, "\"note\": \"raw measurements only -- NOT a ledger claim. pentagon (2.20) census over F2/(K_pi)_F2 = A5 for the pi-lift (sigma3 |-> sigma1) of the A5 window N_A. CAVEAT: this is the verdict for THIS lift only; lift-independence is untested (ruling 248). Degenerate-lift census is a mechanical contrast (its kernel's B4-normality is NOT verified here). Machinery copied verbatim from pentagon_check.g which reproduced the published N(34) count 4096/254016 under contact isolation (calibration PASS).\",\n");
Append(json, Concatenation("\"marking_solutions_found\": ", String(Length(found)), ",\n"));
Append(json, Concatenation("\"chosen_s\": \"", PermToStr(W.s), "\",\n"));
Append(json, Concatenation("\"chosen_t\": \"", PermToStr(W.t), "\",\n"));
Append(json, Concatenation("\"E_size\": ", String(Size(EWIN)), ",\n"));
Append(json, "\"window_asserts\": {\"braid\": true, \"c_maps_to_identity\": true, \"P_size_60\": true, \"B4_relations_on_images\": true, \"x34_image_nontrivial\": true},\n");
Append(json, Concatenation("\"pi_lift_images\": {\"g12\": \"", PermToStr(g12), "\", \"g23\": \"", PermToStr(g23), "\", \"g13\": \"", PermToStr(g13), "\", \"g14\": \"", PermToStr(g14), "\", \"g24\": \"", PermToStr(g24), "\", \"g34\": \"", PermToStr(g34), "\"},\n"));
Append(json, Concatenation("\"census_total\": ", String(Length(bfs.elements)), ",\n"));
Append(json, Concatenation("\"pentagon_pass_pi_lift\": ", String(passPi), ",\n"));
Append(json, Concatenation("\"pentagon_pass_degenerate_lift\": ", String(passVoid), ",\n"));

Append(json, "\"census_pi_lift\": [\n");
first := true;;
for r in censusPi do
  if not first then Append(json, ",\n"); fi;
  first := false;
  Append(json, Concatenation("  {\"elt\": \"", PermToStr(r.elt), "\", \"word\": \"", WordToStr(r.word), "\", \"pass\": ", String(r.pass), "}"));
od;;
Append(json, "\n],\n");

Append(json, "\"shadows\": [\n");
first := true;;
for r in shadowRows do
  if not first then Append(json, ",\n"); fi;
  first := false;
  fws := [];
  for pr in r.f_word do Add(fws, Concatenation("[\"", pr[1], "\",", String(pr[2]), "]")); od;
  Append(json, Concatenation("  {\"m\": ", String(r.m), ", \"f_word\": [", JoinStringsWithSeparator(fws, ","), "], \"pentagon_readA\": ", String(r.pentagon_readA), ", \"pentagon_readB\": ", String(r.pentagon_readB), ", \"reads_agree\": ", String(r.reads_agree), "}"));
od;;
Append(json, "\n],\n");

Append(json, "\"provenance\": {\"gap_version\": \"4.16.0\", \"machinery_source\": \"pentagon_check.g (N34 calibration PASS)\", \"gap_invocation\": \"gap -q -o 2g search/probe/wac_v1/pent_pi_a5.g\"}\n");
Append(json, "}\n");

outPath := "search/certs/pent_pi_a5_20260731.json";;
PrintTo(outPath, "");;
out := OutputTextFile(outPath, false);;
SetPrintFormattingStatus(out, false);;
AppendTo(out, json);;
CloseStream(out);;
Print("CERT WRITTEN: ", outPath, "\n");
Print("PENT_PI_DONE pass_pi=", passPi, "/60 pass_void=", passVoid, "/60\n");
QUIT;
