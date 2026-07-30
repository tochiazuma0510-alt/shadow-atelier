## lift 非依存性の決定実験(pent_recoding_v1 の最優先課題):
## (S1,S2) を固定し、B4 関係式を満たす第 3 生成元像 S3 ∈ E を全枚挙。
## 各 lift の pentagon-live 集合を計算し、一致するかを見る。
SetPrintFormattingStatus("*stdout*", false);;
ImgOfLetter := function(letter, ximg, yimg)
  if letter.g = "x" then return ximg ^ letter.e; else return yimg ^ letter.e; fi;
end;;
EvalWord := function(word, ximg, yimg)
  local val, i; val := ximg^0;
  for i in [Length(word), Length(word)-1 .. 1] do val := val * ImgOfLetter(word[i], ximg, yimg); od;
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
  return rec(c123 := rec(x := g12, y := g23), c234 := rec(x := g23, y := g34),
    c12_3_4 := rec(x := Comp(g13, g23), y := g34),
    c1_23_4 := rec(x := Comp(g12, g13), y := Comp(g24, g34)),
    c1_2_34 := rec(x := g12, y := Comp(g23, g24)));
end;;
BFSFullGroup := function(ximg, yimg, capN)
  local gensBase, wordOf, queue, qi, cur, curWord, gl, gp, nv, capped;
  gensBase := [rec(g:="x",e:=1), rec(g:="x",e:=-1), rec(g:="y",e:=1), rec(g:="y",e:=-1)];
  wordOf := NewDictionary(ximg^0, true); AddDictionary(wordOf, ximg^0, []);
  queue := [ ximg^0 ]; qi := 1; capped := false;
  while qi <= Length(queue) do
    cur := queue[qi]; qi := qi + 1; curWord := LookupDictionary(wordOf, cur);
    for gl in gensBase do
      gp := ImgOfLetter(gl, ximg, yimg); nv := gp * cur;
      if LookupDictionary(wordOf, nv) = fail then
        if Length(queue) >= capN then capped := true; break; fi;
        AddDictionary(wordOf, nv, Concatenation(curWord, [gl])); Add(queue, nv);
      fi;
    od;
    if capped then break; fi;
  od;
  return rec(wordOf := wordOf, elements := queue, capped := capped);
end;;
X5 := (1,3,2,4,5);; Y5 := (1,3,4,5,2);; A5g := AlternatingGroup(5);;
found := [];;
for s in Elements(A5g) do
  if s <> () and s^2 = () then
    for t in Elements(A5g) do
      if t <> () and t^3 = () then
        a := s*(6,7); b := t*(6,7,8); s1 := b^-1*a; s2 := a*b^2;
        if s1^2 = X5 and s2^2 = Y5 and Size(Group(s,t)) = 60 then Add(found, rec(s1:=s1, s2:=s2)); fi;
      fi;
    od;
  fi;
od;;
W := found[1];; S1 := W.s1;; S2 := W.s2;;
EWIN := Group(S1, S2);;  ## E = <s1,s2>
xbar := S1^2;; ybar := S2^2;;
bfs := BFSFullGroup(xbar, ybar, 100);;

## S3 候補の全枚挙: B4 関係式 2 本(rel1 は S1,S2 のみで既成立)
cands := Filtered(Elements(EWIN), g -> (S2*g*S2 = g*S2*g) and (S1*g = g*S1));;
Print("valid S3 images in E: ", Length(cands), "\n");

liveSets := [];;
for S3 in cands do
  g12 := S1^2;; g23 := S2^2;; g34 := S3^2;;
  g13 := (S1^2)^S2;; g24 := (S2^2)^S3;; g14 := ((S1^2)^S2)^S3;;
  cof := BuildCofaces(g12, g23, g13, g14, g24, g34);
  live := [];
  for elt in bfs.elements do
    if PentagonHolds(LookupDictionary(bfs.wordOf, elt), cof) then Add(live, elt); fi;
  od;
  Add(liveSets, rec(S3 := S3, live := Set(live), n := Length(live), triv := (S3^2 = ())));
od;;

## 集計: live 集合の異なり方
distinct := [];;
for r in liveSets do
  found2 := false;
  for d in distinct do
    if d.live = r.live then d.count := d.count + 1; found2 := true; break; fi;
  od;
  if not found2 then Add(distinct, rec(live := r.live, count := 1, n := r.n, example_S3 := r.S3)); fi;
od;;
Print("distinct live sets: ", Length(distinct), "\n");
for d in distinct do
  Print("  |live|=", d.n, " count=", d.count, " exS3=", d.example_S3, "\n");
od;;
## 退化 lift(S3²=1 ⟹ x34↦1)と非退化の内訳
Print("degenerate lifts (x34->1): ", Length(Filtered(liveSets, r -> r.triv)), "\n");
nondeg := Filtered(liveSets, r -> not r.triv);;
Print("nondegenerate lifts: ", Length(nondeg), "\n");
nd := [];;
for r in nondeg do
  found2 := false;
  for d in nd do if d.live = r.live then d.count := d.count+1; found2 := true; break; fi; od;
  if not found2 then Add(nd, rec(live := r.live, count := 1, n := r.n)); fi;
od;;
Print("distinct live sets among nondegenerate: ", Length(nd), "\n");
for d in nd do Print("  |live|=", d.n, " count=", d.count, "\n"); od;;
QUIT;
