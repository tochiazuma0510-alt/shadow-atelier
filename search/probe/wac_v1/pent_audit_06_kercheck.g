## 決定検査: 各余面像は ker(F2 -> A5) を殺すか(理論 Prop 2.4 の要求)。
## 一般の核元 h(ランダム語 w とその BFS 代表 u の差 h = w u^-1)で
## 5 余面を個別評価。殺さない余面 = 壊れている座標。
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
InvW := function(word) return Reversed(List(word, l -> rec(g := l.g, e := -l.e))); end;;
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
W := found[1];; S1 := W.s1;; S2 := W.s2;; S3 := W.s1;;
xbar := S1^2;; ybar := S2^2;;
g12 := S1^2;; g23 := S2^2;; g34 := S3^2;;
g13 := (S1^2)^S2;; g24 := (S2^2)^S3;; g14 := ((S1^2)^S2)^S3;;
cofs := rec(
  c123    := rec(x := g12, y := g23),
  c234    := rec(x := g23, y := g34),
  c12_3_4 := rec(x := Comp(g13, g23), y := g34),
  c1_23_4 := rec(x := Comp(g12, g13), y := Comp(g24, g34)),
  c1_2_34 := rec(x := g12, y := Comp(g23, g24))
);;
bfs := BFSFullGroup(xbar, ybar, 100);;

## 一般核元の生成: 乱数語 w -> elt -> BFS 代表 u -> h = w * u^-1 (elt(h)=1)
mkrand := function(len, seedlist)
  local w, i, gpick;
  w := [];
  for i in [1..len] do
    gpick := seedlist[((i*7+len*3) mod Length(seedlist)) + 1];
    Add(w, gpick);
  od;
  return w;
end;;
gens4 := [rec(g:="x",e:=1), rec(g:="y",e:=1), rec(g:="x",e:=-1), rec(g:="y",e:=-1)];;
names := ["c123","c234","c12_3_4","c1_23_4","c1_2_34"];;
failCount := rec(c123:=0, c234:=0, c12_3_4:=0, c1_23_4:=0, c1_2_34:=0);;
tests := 0;;
for len in [3,4,5,6,7,8,9,10,11,12] do
  for shift in [0,1,2,3] do
    w := mkrand(len, Concatenation(gens4{[1+shift..4]}, gens4{[1..shift]}));
    elt := EvalWord(w, xbar, ybar);
    u := LookupDictionary(bfs.wordOf, elt);
    h := Concatenation(w, InvW(u));     ## h evaluates to identity in A5
    if EvalWord(h, xbar, ybar) <> () then Error("h not in kernel?!"); fi;
    tests := tests + 1;
    for nm in names do
      c := cofs.(nm);
      if EvalWord(h, c.x, c.y) <> () then failCount.(nm) := failCount.(nm) + 1; fi;
    od;
  od;
od;;
Print("kernel-killing test: ", tests, " kernel elements\n");
for nm in names do
  Print("  ", nm, ": kills kernel in ", tests - failCount.(nm), "/", tests, " cases  (FAIL=", failCount.(nm), ")\n");
od;;
QUIT;
