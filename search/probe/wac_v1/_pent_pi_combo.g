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
W := found[1];; S1 := W.s1;; S2 := W.s2;; S3 := W.s1;;
xbar := S1^2;; ybar := S2^2;;
cof := BuildCofaces(S1^2, S2^2, (S1^2)^S2, ((S1^2)^S2)^S3, (S2^2)^S3, S3^2);;
bfs := BFSFullGroup(xbar, ybar, 100);;
verdictOf := NewDictionary(xbar^0, true);;
for elt in bfs.elements do
  AddDictionary(verdictOf, elt, PentagonHolds(LookupDictionary(bfs.wordOf, elt), cof));
od;;
Read("search/probe/wac_v1/_pent_pi_shadows.g");;
EvalA := function(fw, xi, yi) local v,p; v:=xi^0; for p in fw do if p[1]="x" then v:=v*xi^p[2]; else v:=v*yi^p[2]; fi; od; return v; end;;
EvalB := function(fw, xi, yi) local v,i,p; v:=xi^0; for i in [Length(fw),Length(fw)-1..1] do p:=fw[i]; if p[1]="x" then v:=v*xi^p[2]; else v:=v*yi^p[2]; fi; od; return v; end;;
combos := ["A","Ainv","B","Binv"];;
for cb in combos do
  cnt := 0; perM := rec(m0:=0, m1:=0, m3:=0, m4:=0);
  for sh in SHADOW_LIST do
    if cb in ["A","Ainv"] then e := EvalA(sh.f_word, xbar, ybar); else e := EvalB(sh.f_word, xbar, ybar); fi;
    if cb in ["Ainv","Binv"] then e := e^-1; fi;
    v := LookupDictionary(verdictOf, e);
    if v = true then
      cnt := cnt + 1;
      if sh.m = 0 then perM.m0 := perM.m0+1; elif sh.m = 1 then perM.m1 := perM.m1+1;
      elif sh.m = 3 then perM.m3 := perM.m3+1; else perM.m4 := perM.m4+1; fi;
    fi;
  od;
  Print("combo=", cb, ": shadows_pass=", cnt, "/20  per-m [m0,m1,m3,m4]=[", perM.m0, ",", perM.m1, ",", perM.m3, ",", perM.m4, "]\n");
od;;
Print("live set (rev dict): ");;
for elt in bfs.elements do
  if LookupDictionary(verdictOf, elt) = true then Print(elt, "  "); fi;
od;;
Print("\nDONE\n");
QUIT;
