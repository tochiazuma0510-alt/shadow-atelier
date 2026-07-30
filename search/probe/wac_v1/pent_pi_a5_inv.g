#############################################################################
## pent_pi_a5_inv.g -- PENT-π 装置検査: pentagon 判定の類不変性テスト
## 理論(C1 p.13 + Prop 2.4)では判定は f の N_{PB3} 類のみに依存するはず。
## 各元の BFS 代表語 w に対し、x^5(A5 では恒等 = N_{F2} の元)を後置/前置
## した別代表語で判定が変わるかを測る。変われば装置(g_ij データ)が
## 真の余面データでない証拠(コンベンション以前の構造バグ)。
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

cof := BuildCofaces(S1^2, S2^2, (S1^2)^S2, ((S1^2)^S2)^S3, (S2^2)^S3, S3^2);;
bfs := BFSFullGroup(xbar, ybar, 100);;

x5word := List([1..5], i -> rec(g:="x", e:=1));;
y5word := List([1..5], i -> rec(g:="y", e:=1));;

viol := 0;; checked := 0;;
for elt in bfs.elements do
  word := LookupDictionary(bfs.wordOf, elt);
  v0 := PentagonHolds(word, cof);
  vApp := PentagonHolds(Concatenation(word, x5word), cof);
  vPre := PentagonHolds(Concatenation(x5word, word), cof);
  vAppY := PentagonHolds(Concatenation(word, y5word), cof);
  checked := checked + 1;
  if not (v0 = vApp and v0 = vPre and v0 = vAppY) then
    viol := viol + 1;
    if viol <= 5 then
      Print("VIOLATION elt=", elt, " v0=", v0, " app=", vApp, " pre=", vPre, " appY=", vAppY, "\n");
    fi;
  fi;
od;;
Print("INVARIANCE TEST: checked=", checked, " violations=", viol, "\n");

## 追加診断: 余面像の x^5 が実際に「消える」か(= phi(x12^5) 等が
## 5 本の余面それぞれで pentagon 等式に透明か)を直接見る:
## 各余面 c について Img_c(x^5) を印字(恒等なら類不変性は自明)
Print("cofactor images of x^5:  c123=", (cof.c123.x)^5, "  c234=", (cof.c234.x)^5,
      "  c12_3_4=", (cof.c12_3_4.x)^5, "  c1_23_4=", (cof.c1_23_4.x)^5,
      "  c1_2_34=", (cof.c1_2_34.x)^5, "\n");
Print("cofactor images of y^5:  c123=", (cof.c123.y)^5, "  c234=", (cof.c234.y)^5,
      "  c12_3_4=", (cof.c12_3_4.y)^5, "  c1_23_4=", (cof.c1_23_4.y)^5,
      "  c1_2_34=", (cof.c1_2_34.y)^5, "\n");
Print("PENT_PI_INV_DONE\n");
QUIT;
