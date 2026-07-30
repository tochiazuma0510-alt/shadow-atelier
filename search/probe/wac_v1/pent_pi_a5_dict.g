#############################################################################
## search/probe/wac_v1/pent_pi_a5_dict.g
##  PENT-π 装置較正(裁定 248・P-PENT-1 発動): σ→x_ij 共役方向の辞書
##  2 通り × f_word 語順 2 通り = 4 組合せを走査し、各組合せの
##  20 shadow 通過数と census(/60)を測る。期待値はコードに書かない。
##  背景: pentagon_check.g の N34 較正は g_ij を論文の置換データで直接
##  受けたため、σ から x_ij を作る段(本実験で初使用)だけが較正外。
#############################################################################
SetPrintFormattingStatus("*stdout*", false);;

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
  queue := [ ximg^0 ]; qi := 1; capped := false;
  while qi <= Length(queue) do
    cur := queue[qi]; qi := qi + 1;
    curWord := LookupDictionary(wordOf, cur);
    for gl in gensBase do
      gp := ImgOfLetter(gl, ximg, yimg);
      nv := gp * cur;
      if LookupDictionary(wordOf, nv) = fail then
        if Length(queue) >= capN then capped := true; break; fi;
        AddDictionary(wordOf, nv, Concatenation(curWord, [gl]));
        Add(queue, nv);
      fi;
    od;
    if capped then break; fi;
  od;
  return rec(wordOf := wordOf, elements := queue, capped := capped);
end;;

## ---- A5 窓(pent_pi_a5.g STEP1 と同一・解は一意と確認済) ----
X5 := (1,3,2,4,5);; Y5 := (1,3,4,5,2);; A5 := AlternatingGroup(5);;
found := [];;
for s in Elements(A5) do
  if s <> () and s^2 = () then
    for t in Elements(A5) do
      if t <> () and t^3 = () then
        a := s*(6,7); b := t*(6,7,8);
        s1 := b^-1*a; s2 := a*b^2;
        if s1^2 = X5 and s2^2 = Y5 and Size(Group(s,t)) = 60 then
          Add(found, rec(s1:=s1, s2:=s2));
        fi;
      fi;
    od;
  fi;
od;;
W := found[1];;
S1 := W.s1;; S2 := W.s2;; S3 := W.s1;;
xbar := S1^2;; ybar := S2^2;;

bfs := BFSFullGroup(xbar, ybar, 100);;

Read("search/probe/wac_v1/_pent_pi_shadows.g");;

EvalFWordA := function(fw, ximg, yimg)
  local val, pair;
  val := ximg^0;
  for pair in fw do
    if pair[1] = "x" then val := val * ximg^pair[2]; else val := val * yimg^pair[2]; fi;
  od;
  return val;
end;;
EvalFWordB := function(fw, ximg, yimg)
  local val, i, pair;
  val := ximg^0;
  for i in [Length(fw), Length(fw)-1 .. 1] do
    pair := fw[i];
    if pair[1] = "x" then val := val * ximg^pair[2]; else val := val * yimg^pair[2]; fi;
  od;
  return val;
end;;

## ---- 辞書 2 通りの x_ij 像 ----
## rev(反同型): paper σ2σ1²σ2⁻¹ = GAP (S1²)^S2  /  straight(同型): GAP S2*S1²*S2⁻¹ = (S1²)^(S2⁻¹)
dicts := [
  rec(label := "rev",
      g12 := S1^2, g23 := S2^2, g34 := S3^2,
      g13 := (S1^2)^S2, g24 := (S2^2)^S3, g14 := ((S1^2)^S2)^S3),
  rec(label := "straight",
      g12 := S1^2, g23 := S2^2, g34 := S3^2,
      g13 := (S1^2)^(S2^-1), g24 := (S2^2)^(S3^-1), g14 := ((S1^2)^(S2^-1))^(S3^-1))
];;

results := [];;
for d in dicts do
  cof := BuildCofaces(d.g12, d.g23, d.g13, d.g14, d.g24, d.g34);
  passCensus := 0;
  verdictOf := NewDictionary(xbar^0, true);
  for elt in bfs.elements do
    word := LookupDictionary(bfs.wordOf, elt);
    ok := PentagonHolds(word, cof);
    if ok then passCensus := passCensus + 1; fi;
    AddDictionary(verdictOf, elt, ok);
  od;
  ## c 整合(paper c = x23 x12 x13 -> 1): rev 読みは GAP g13*g12*g23, straight は g23*g12*g13
  cRev := (d.g13 * d.g12 * d.g23 = ());
  cStr := (d.g23 * d.g12 * d.g13 = ());
  for fr in ["A", "B"] do
    shPass := 0; rows := [];
    for sh in SHADOW_LIST do
      if fr = "A" then elt := EvalFWordA(sh.f_word, xbar, ybar);
      else elt := EvalFWordB(sh.f_word, xbar, ybar); fi;
      v := LookupDictionary(verdictOf, elt);
      if v = true then shPass := shPass + 1; fi;
      Add(rows, rec(m := sh.m, pass := v));
    od;
    Add(results, rec(dict := d.label, fread := fr, census_pass := passCensus,
                     shadows_pass := shPass, c_rev_ok := cRev, c_str_ok := cStr, rows := rows));
    Print("dict=", d.label, " fread=", fr, ": census=", passCensus, "/60 shadows=", shPass, "/20  (c_rev=", cRev, " c_str=", cStr, ")\n");
  od;
od;;

Print("PENT_PI_DICT_DONE\n");
QUIT;
