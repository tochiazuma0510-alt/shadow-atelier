## 全直進辞書(straight hom・GAP 語順)での核殺しテスト+pentagon 再測定。
## 反転(anti)辞書との比較で正しい実現を決める。判定基準は理論の要求
## (全余面が核を殺す)のみ — 期待値は使わない。
SetPrintFormattingStatus("*stdout*", false);;
EvalStraight := function(word, ximg, yimg)
  local val, l; val := ximg^0;
  for l in word do
    if l.g = "x" then val := val * ximg^l.e; else val := val * yimg^l.e; fi;
  od;
  return val;
end;;
InvW := function(word) return Reversed(List(word, l -> rec(g := l.g, e := -l.e))); end;;
BFSFullGroup := function(ximg, yimg, capN)
  local gensBase, wordOf, queue, qi, cur, curWord, gl, gp, nv, capped;
  gensBase := [rec(g:="x",e:=1), rec(g:="x",e:=-1), rec(g:="y",e:=1), rec(g:="y",e:=-1)];
  wordOf := NewDictionary(ximg^0, true); AddDictionary(wordOf, ximg^0, []);
  queue := [ ximg^0 ]; qi := 1; capped := false;
  while qi <= Length(queue) do
    cur := queue[qi]; qi := qi + 1; curWord := LookupDictionary(wordOf, cur);
    for gl in gensBase do
      gp := ximg^0;
      if gl.g = "x" then gp := ximg^gl.e; else gp := yimg^gl.e; fi;
      nv := cur * gp;   ## straight: 右から積む(語の末尾に追加)
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
W := found[1];; S1 := W.s1;; S2 := W.s2;; S3 := W.s1;;
xbar := S1^2;; ybar := S2^2;;
## straight 辞書: paper 積 = GAP 積(同型)
g12 := S1^2;; g23 := S2^2;; g34 := S3^2;;
g13 := S2*S1^2*S2^-1;;
g24 := S3*S2^2*S3^-1;;
g14 := S3*S2*S1^2*S2^-1*S3^-1;;
## c 整合(straight): c = x23 x12 x13 -> g23*g12*g13 = 1 か
Print("straight c-check: ", g23*g12*g13 = (), "\n");
cofs := rec(
  c123    := rec(x := g12,     y := g23),
  c234    := rec(x := g23,     y := g34),
  c12_3_4 := rec(x := g13*g23, y := g34),
  c1_23_4 := rec(x := g12*g13, y := g24*g34),
  c1_2_34 := rec(x := g12,     y := g23*g24)
);;
bfs := BFSFullGroup(xbar, ybar, 100);;
names := ["c123","c234","c12_3_4","c1_23_4","c1_2_34"];;
failCount := rec(c123:=0, c234:=0, c12_3_4:=0, c1_23_4:=0, c1_2_34:=0);;
gens4 := [rec(g:="x",e:=1), rec(g:="y",e:=1), rec(g:="x",e:=-1), rec(g:="y",e:=-1)];;
tests := 0;;
for len in [3,4,5,6,7,8,9,10,11,12] do
  for shift in [0,1,2,3] do
    w := [];
    for i in [1..len] do
      Add(w, gens4[(((i*7+len*3) + shift) mod 4) + 1]);
    od;
    elt := EvalStraight(w, xbar, ybar);
    u := LookupDictionary(bfs.wordOf, elt);
    h := Concatenation(w, InvW(u));
    if EvalStraight(h, xbar, ybar) <> () then Error("h not in kernel"); fi;
    tests := tests + 1;
    for nm in names do
      c := cofs.(nm);
      if EvalStraight(h, c.x, c.y) <> () then failCount.(nm) := failCount.(nm) + 1; fi;
    od;
  od;
od;;
Print("STRAIGHT kernel-killing: ", tests, " kernel elements\n");
for nm in names do
  Print("  ", nm, ": FAIL=", failCount.(nm), "/", tests, "\n");
od;;
## 全余面 kill なら pentagon 再測定(straight 積順: paper (2.20) そのまま)
allkill := ForAll(names, nm -> failCount.(nm) = 0);;
if allkill then
  passN := 0;
  liveL := [];
  for elt in bfs.elements do
    word := LookupDictionary(bfs.wordOf, elt);
    F123    := EvalStraight(word, cofs.c123.x,    cofs.c123.y);
    F234    := EvalStraight(word, cofs.c234.x,    cofs.c234.y);
    F12_3_4 := EvalStraight(word, cofs.c12_3_4.x, cofs.c12_3_4.y);
    F1_23_4 := EvalStraight(word, cofs.c1_23_4.x, cofs.c1_23_4.y);
    F1_2_34 := EvalStraight(word, cofs.c1_2_34.x, cofs.c1_2_34.y);
    ## paper (2.20): phi234(f) phi1_23_4(f) phi123(f) = phi1_2_34(f) phi12_3_4(f)
    if (F234 * F1_23_4 * F123) = (F1_2_34 * F12_3_4) then
      passN := passN + 1; Add(liveL, elt);
    fi;
  od;
  Print("STRAIGHT pentagon census: pass = ", passN, " / 60\n");
  Print("live: ");
  for e in liveL do Print(e, "  "); od;
  Print("\n");
else
  Print("straight dict does NOT kill kernel on all cofaces -- no remeasure\n");
fi;
QUIT;
