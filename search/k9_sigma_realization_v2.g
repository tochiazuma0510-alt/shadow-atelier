## search/k9_sigma_realization_v2.g -- [SIG-1] sigma_1, sigma_2 realization in Aut(G_9), v2 (裁定1135)
##
## 正本: docs/notes/d972_h1_adjudication_v1.md §7 [SIG-1] + docs/notes/ad_convention_note_v1.md
##   (裁定1135・数学者裁定): 正典の Ad 規約は LEFT: Ad(g)(w) = g w g^-1。
##
## v1 (search/k9_sigma_realization_v1.g) からの修正点(司令塔指示・裁定1135):
##   v1 は AbstractProd([y9^-1,x9^-1]) を使って alpha1(y) を組んだが、AbstractProd は
##   「paper 記法(左から右)-> GAP 積(逆順変換)」の規約(week3-battery-common.g のコメント
##   "reversal convention" 参照)であるため、AbstractProd([y9^-1,x9^-1]) は実際には
##   x9^-1*y9^-1 を返していた(第2形・sigma_i^-1 共役側)。これは (1.11)/(1.12) の第1形
##   ( sigma_i 共役側、alpha1(y)=y^-1 x^-1 の GAP 積そのもの)と語順が入れ替わっていた。
##   v2 は AbstractProd を使わず、GAP の * 演算子で直接 y9^-1*x9^-1 / x9^-1*y9^-1 を書く
##   ことでこの反転を除去する(第1形を正しく実装)。
##
##   sigma_bar_1: x |-> x,        y |-> y^-1 x^-1   (第1形, sigma_1 共役)
##   sigma_bar_2: x |-> x^-1 y^-1, y |-> y            (第1形, sigma_2 共役)
##
##   GAP の ^ 演算子は g^h = h^-1*g*h (RIGHT) なので、正典 LEFT Ad(x)(w)=x*w*x^-1 と
##   一致する GAP 標準関数呼び出しは ConjugatorAutomorphism(G9, x9^-1) である
##   (ad_convention_note_v1.md §1 末尾の注意)。v1 は素朴な x^-1*w*x / x*w*x^-1 の両方を
##   手計算で比較していたが誤解を招きやすいので、v2 では ConjugatorAutomorphism との
##   直接比較も併記する(両者が一致することの機械確認)。
##
## 規律: u/c 非接触・封印3量非接触・prereg 量非計算・判定語なし・UNKNOWN 一級。
## u 影響注記: 本実現(v2)を sigma_1^u 経由の量(chi_vir・ker T)に使う下流は v2 のみ参照
## すること(v1 は第2形=sigma_i の逆元を実現しており、u の符号が反転しうる)。

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");   # MakeGn, JB, JStr, JPair, JoinC (AbstractProd NOT used here)

t0Global := GAPLIB_WallElapsedMs();;

Print("############################################################\n");
Print("# k9_sigma_realization_v2.g -- [SIG-1] alpha_1,alpha_2 in Aut(G_9), first form (裁定1135)\n");
Print("############################################################\n");

## ================= [S-1] G_9 = PB3/K^(9), order 2916 (既存資産 MakeGn(9)) =================
Print("\n=== [S-1] G_9 := MakeGn(9) ===\n");
g9 := MakeGn(9);;
G9 := g9.G;;  x9 := g9.x;;  y9 := g9.y;;
g9size := Size(G9);;
Print("  |G_9| = ", g9size, " (expect 2916)\n");
g9sizeOk := (g9size = 2916);;
if not g9sizeOk then
  Error("k9_sigma_realization_v2: G_9 order mismatch -- refusing to proceed");
fi;

## ================= [S-2] alpha_1, alpha_2, FIRST FORM (direct GAP product, no AbstractProd) =====
Print("\n=== [S-2] alpha_1, alpha_2, first form: a1(y)=y^-1*x^-1, a2(x)=x^-1*y^-1 ===\n");
imgY1 := y9^-1 * x9^-1;;   # y^-1 x^-1, direct GAP product (paper order preserved, no reversal)
alpha1 := GroupHomomorphismByImages(G9, G9, [x9, y9], [x9, imgY1]);;
imgX2 := x9^-1 * y9^-1;;   # x^-1 y^-1, direct GAP product
alpha2 := GroupHomomorphismByImages(G9, G9, [x9, y9], [imgX2, y9]);;

alpha1IsFail := (alpha1 = fail);;
alpha2IsFail := (alpha2 = fail);;
Print("  alpha1 construction fail = ", alpha1IsFail, "  alpha2 construction fail = ", alpha2IsFail, "\n");
Print("  alpha1(y) = ", imgY1, "   alpha2(x) = ", imgX2, "\n");

alpha1IsBij := false;;  alpha2IsBij := false;;
if not alpha1IsFail then alpha1IsBij := IsBijective(alpha1); fi;;
if not alpha2IsFail then alpha2IsBij := IsBijective(alpha2); fi;;
Print("  alpha1 bijective (=automorphism) = ", alpha1IsBij, "\n");
Print("  alpha2 bijective (=automorphism) = ", alpha2IsBij, "\n");

## braid relation check: alpha1 alpha2 alpha1 = alpha2 alpha1 alpha2, verified pointwise on
## generators x9,y9 (sufficient since both sides are endomorphisms of G9=<x9,y9>).
ApplyChain := function(homlist, g)
  local v, h;
  v := g;
  for h in homlist do v := Image(h, v); od;
  return v;
end;;

lhsX := ApplyChain([alpha1, alpha2, alpha1], x9);;
lhsY := ApplyChain([alpha1, alpha2, alpha1], y9);;
rhsX := ApplyChain([alpha2, alpha1, alpha2], x9);;
rhsY := ApplyChain([alpha2, alpha1, alpha2], y9);;
braidOnX_lr := (lhsX = rhsX);;
braidOnY_lr := (lhsY = rhsY);;
Print("  braid check (apply order alpha1,alpha2,alpha1 to generators, left-to-right):\n");
Print("    lhs(x)=", lhsX, "  rhs(x)=", rhsX, "  equal_on_x=", braidOnX_lr, "\n");
Print("    lhs(y)=", lhsY, "  rhs(y)=", rhsY, "  equal_on_y=", braidOnY_lr, "\n");
braidHoldsOnGenerators := braidOnX_lr and braidOnY_lr;;
Print("  braid_relation_holds_on_generators = ", braidHoldsOnGenerators, "\n");

## ================= [S-3] H := <alpha_1, alpha_2> <= Aut(G_9), |H| =================
Print("\n=== [S-3] H := <alpha1, alpha2> <= Aut(G_9) ===\n");
hSize := fail;;  hSizeOk := false;;  centerG9Size := fail;;
if alpha1IsBij and alpha2IsBij then
  AutG9H := Group(alpha1, alpha2);;
  hSize := Size(AutG9H);;
  centerG9Size := Size(Center(G9));;
  hSizeOk := (hSize = 17496);;
  Print("  Z(G_9) order = ", centerG9Size, " (=1 predicts |H|=17496 injectivity)\n");
  Print("  |H| = ", hSize, " (predicted 17496 if Z(G_9)=1): ", hSizeOk, "\n");
else
  Print("  [SKIP] alpha1 or alpha2 not bijective -- cannot form H := <alpha1,alpha2> in Aut(G_9)\n");
fi;

## ================= [S-4] alpha_i^2 vs LEFT Ad(x),Ad(y) and GAP ConjugatorAutomorphism =================
Print("\n=== [S-4] alpha_i^2 vs canon LEFT Ad(x),Ad(y); cross-check via GAP ConjugatorAutomorphism ===\n");
alpha1SqOnX := fail;; alpha1SqOnY := fail;; alpha2SqOnX := fail;; alpha2SqOnY := fail;;
if alpha1IsBij then
  alpha1SqOnX := ApplyChain([alpha1, alpha1], x9);;
  alpha1SqOnY := ApplyChain([alpha1, alpha1], y9);;
fi;;
if alpha2IsBij then
  alpha2SqOnX := ApplyChain([alpha2, alpha2], x9);;
  alpha2SqOnY := ApplyChain([alpha2, alpha2], y9);;
fi;;

## canon LEFT Ad(g)(w) := g*w*g^-1, computed directly by hand (no GAP ^ operator, which is RIGHT)
AdLeftOnX_x := x9 * x9 * x9^-1;;   # Ad(x)(x) = x*x*x^-1
AdLeftOnY_x := x9 * y9 * x9^-1;;   # Ad(x)(y) = x*y*x^-1
AdLeftOnX_y := y9 * x9 * y9^-1;;   # Ad(y)(x) = y*x*y^-1
AdLeftOnY_y := y9 * y9 * y9^-1;;   # Ad(y)(y) = y*y*y^-1

Print("  alpha1^2(x) = ", alpha1SqOnX, "   alpha1^2(y) = ", alpha1SqOnY, "\n");
Print("  LEFT Ad(x)(x) [x*x*x^-1] = ", AdLeftOnX_x, "   LEFT Ad(x)(y) [x*y*x^-1] = ", AdLeftOnY_x, "\n");
alpha1SqEqAdLeftX := (alpha1SqOnX = AdLeftOnX_x) and (alpha1SqOnY = AdLeftOnY_x);;
Print("  alpha1^2 == LEFT Ad(x) on {x,y} : ", alpha1SqEqAdLeftX, "\n");

Print("  alpha2^2(x) = ", alpha2SqOnX, "   alpha2^2(y) = ", alpha2SqOnY, "\n");
Print("  LEFT Ad(y)(x) [y*x*y^-1] = ", AdLeftOnX_y, "   LEFT Ad(y)(y) [y*y*y^-1] = ", AdLeftOnY_y, "\n");
alpha2SqEqAdLeftY := (alpha2SqOnX = AdLeftOnX_y) and (alpha2SqOnY = AdLeftOnY_y);;
Print("  alpha2^2 == LEFT Ad(y) on {x,y} : ", alpha2SqEqAdLeftY, "\n");

## GAP standard-library cross-check: ConjugatorAutomorphism(G, h) sends w -> w^h = h^-1*w*h (RIGHT
## by GAP's own convention for the automorphism it returns's ACTION on elements via ^); per
## ad_convention_note_v1.md, canon LEFT Ad(x)(w)=x*w*x^-1 corresponds to GAP's
## ConjugatorAutomorphism(G9, x9^-1) (h=x^-1 so w^h = (x^-1)^-1*w*x^-1 = x*w*x^-1).
convAutoAvailable := true;;
convAuto1 := fail;; convAuto1Alt := fail;; conv1EqXinv := fail;; conv1EqX := fail;;
convAuto2 := fail;; convAuto2Alt := fail;; conv2EqYinv := fail;; conv2EqY := fail;;
if IsBound(ConjugatorAutomorphism) then
  convAuto1 := ConjugatorAutomorphism(G9, x9^-1);;   # predicted match for alpha1^2
  convAuto1Alt := ConjugatorAutomorphism(G9, x9);;   # predicted mismatch
  conv1EqXinv := (Image(convAuto1, x9) = alpha1SqOnX) and (Image(convAuto1, y9) = alpha1SqOnY);;
  conv1EqX := (Image(convAuto1Alt, x9) = alpha1SqOnX) and (Image(convAuto1Alt, y9) = alpha1SqOnY);;
  convAuto2 := ConjugatorAutomorphism(G9, y9^-1);;   # predicted match for alpha2^2
  convAuto2Alt := ConjugatorAutomorphism(G9, y9);;   # predicted mismatch
  conv2EqYinv := (Image(convAuto2, x9) = alpha2SqOnX) and (Image(convAuto2, y9) = alpha2SqOnY);;
  conv2EqY := (Image(convAuto2Alt, x9) = alpha2SqOnX) and (Image(convAuto2Alt, y9) = alpha2SqOnY);;
  Print("  GAP ConjugatorAutomorphism(G9, x9^-1) == alpha1^2 on {x,y} : ", conv1EqXinv, "   (x9 instead: ", conv1EqX, ")\n");
  Print("  GAP ConjugatorAutomorphism(G9, y9^-1) == alpha2^2 on {x,y} : ", conv2EqYinv, "   (y9 instead: ", conv2EqY, ")\n");
else
  convAutoAvailable := false;;
  Print("  [SKIP] ConjugatorAutomorphism not bound in this GAP session -- recorded as UNKNOWN\n");
fi;;

t1Global := GAPLIB_WallElapsedMs();;
Print("\n総経過 = ", t1Global - t0Global, " ms\n");

## ================= JSON 出力 =================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_k9sigma_v2.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/k9_sigma_realization_v2.g");;

hSizeStr := "null";;
if hSize <> fail then hSizeStr := String(hSize); fi;;
centerG9SizeStr := "null";;
if centerG9Size <> fail then centerG9SizeStr := String(centerG9Size); fi;;

convJsonFields := "";;
if convAutoAvailable then
  convJsonFields := Concatenation(
    "\"conjugator_automorphism_available\":true,",
    "\"alpha1_sq_eq_conjugator_x_inv\":", JB(conv1EqXinv), ",",
    "\"alpha1_sq_eq_conjugator_x\":", JB(conv1EqX), ",",
    "\"alpha2_sq_eq_conjugator_y_inv\":", JB(conv2EqYinv), ",",
    "\"alpha2_sq_eq_conjugator_y\":", JB(conv2EqY)
  );;
else
  convJsonFields := "\"conjugator_automorphism_available\":false";;
fi;;

cert := Concatenation(
  "{\"schema\":\"sigma_realization/v2\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/k9_sigma_realization_v2.g\",\"order\":\"裁定1135 (Ad規約修正: implementer構成が第2形だった件の是正)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/d972_h1_adjudication_v1.md §7 [SIG-1] + docs/notes/ad_convention_note_v1.md §3\"",
  ",\"supersedes\":\"search/certs/k9_sigma_realization_v1_20260813.json (v1 は第2形=sigma_i^-1共役側で構成されていた -- braid/|H|=17496/中心化群は規約に不変だが、sigma_i の同定とu経由量の符号に影響しうる。v1 は残置・参照は非推奨)\"",
  ",\"convention\":{",
    "\"canon\":\"LEFT: Ad(g)(w) = g*w*g^-1 (照合_B3表示_T2土台 §4 逐語・p.4/p.5 画像照合済・裁定1135)\",",
    "\"implemented_form\":\"first form of (1.11)/(1.12): a1: x->x, y->y^-1*x^-1 ; a2: x->x^-1*y^-1, y->y (= sigma_i conjugation side, NOT sigma_i^-1)\",",
    "\"alpha_sq_gap_note\":\"a1^2 = (w -> x*w*x^-1) [LEFT Ad(x)]; in GAP this equals ConjugatorAutomorphism(G9, x9^-1), NOT ConjugatorAutomorphism(G9, x9), because GAP's g^h means h^-1*g*h (RIGHT)\",",
    "\"u_sign_impact_note\":\"本実現(v2)を sigma_1^u 経由の量(chi_vir・ker T)に使う下流は v2 のみ参照すること。v1(第2形)は sigma_i の逆元を実現しており u の符号が反転しうる。\"",
  "},",
  "\"s1_g9\":{\"g9_size\":", String(g9size), ",\"g9_size_expected\":2916,\"g9_size_ok\":", JB(g9sizeOk), "},",
  "\"s2_alpha_construction\":{",
    "\"alpha1_construction_fail\":", JB(alpha1IsFail), ",\"alpha1_is_bijective\":", JB(alpha1IsBij), ",",
    "\"alpha2_construction_fail\":", JB(alpha2IsFail), ",\"alpha2_is_bijective\":", JB(alpha2IsBij), ",",
    "\"braid_relation_holds_on_generators\":", JB(braidHoldsOnGenerators), ",",
    "\"braid_detail\":{\"equal_on_x\":", JB(braidOnX_lr), ",\"equal_on_y\":", JB(braidOnY_lr), "}",
  "},",
  "\"s3_h_group\":{",
    "\"h_size\":", hSizeStr, ",\"h_size_expected_if_center_trivial\":17496,\"h_size_matches_expected\":", JB(hSizeOk), ",",
    "\"center_g9_size\":", centerG9SizeStr,
  "},",
  "\"s4_alpha_squared_vs_ad\":{",
    "\"alpha1_squared_eq_left_ad_x\":", JB(alpha1SqEqAdLeftX), ",",
    "\"alpha2_squared_eq_left_ad_y\":", JB(alpha2SqEqAdLeftY), ",",
    convJsonFields, ",",
    "\"note\":\"LEFT Ad(g)(w):=g*w*g^-1 (canon). GAP's ConjugatorAutomorphism(G,h) implements w->w^h=h^-1*w*h (RIGHT), so the canon-matching call is with h=g^-1.\"",
  "},",
  "\"u_touched\":false,\"c_touched\":false,\"prereg_quantities_untouched\":true",
  ",\"no_verdict_note\":\"machine values only; verdict は司令塔/数学者。UNKNOWN は一級の結果。\"",
  ",\"total_elapsed_ms\":", String(t1Global - t0Global),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/k9_sigma_realization_v2_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
Print("K9_SIGMA_REALIZATION_V2_DONE\n");
QUIT;
