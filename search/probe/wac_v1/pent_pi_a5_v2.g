## PENT-π v2 -- 欠陥修正版(裁定 252 用)。
## 修正の根拠: C1 (2.4)(p.9 画像照合)-- N_{PB3} は 5 余面の逆像の交わり。
## (K_π)_{PB3} は N_A より真に小 ⟹ N_A 類の pentagon 判定は ∃-判定
## (類の持ち上げのどれかが (2.20) を満たすか)。ideas_015 破綻点 2 の復活。
## 実装: 核(ker F2->A5)の Schreier 生成元の 3 複合余面像が生成する H3 ≤ E^3
## の軌道で fiber を走る。全直進辞書(audit_07 で c-check PASS)。
SetPrintFormattingStatus("*stdout*", false);;
EvalS := function(word, ximg, yimg)
  local val, l; val := ximg^0;
  for l in word do
    if l.g = "x" then val := val * ximg^l.e; else val := val * yimg^l.e; fi;
  od;
  return val;
end;;
InvW := function(word) return Reversed(List(word, l -> rec(g := l.g, e := -l.e))); end;;
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
g13 := S2*S1^2*S2^-1;; g24 := S3*S2^2*S3^-1;; g14 := S3*S2*S1^2*S2^-1*S3^-1;;
if not (g23*g12*g13 = ()) then Error("c-check fail"); fi;
c123 := rec(x := g12, y := g23);;      c234 := rec(x := g23, y := g34);;
c3 := rec(x := g13*g23, y := g34);;    ## c12_3_4
c4 := rec(x := g12*g13, y := g24*g34);;## c1_23_4
c5 := rec(x := g12, y := g23*g24);;    ## c1_2_34

## straight BFS(語は右に伸ばす)
gens4 := [rec(g:="x",e:=1), rec(g:="x",e:=-1), rec(g:="y",e:=1), rec(g:="y",e:=-1)];;
wordOf := NewDictionary((), true);;
AddDictionary(wordOf, (), []);;
queue := [ () ];; qi := 1;;
while qi <= Length(queue) do
  cur := queue[qi]; qi := qi + 1;
  curWord := LookupDictionary(wordOf, cur);
  for gl in gens4 do
    if gl.g = "x" then gp := xbar^gl.e; else gp := ybar^gl.e; fi;
    nv := cur * gp;
    if LookupDictionary(wordOf, nv) = fail then
      AddDictionary(wordOf, nv, Concatenation(curWord, [gl]));
      Add(queue, nv);
    fi;
  od;
od;;
if Length(queue) <> 60 then Error("BFS != 60"); fi;

## Schreier 生成元の 3 複合余面像 → H3 ≤ E^3(24 点上)
D3 := DirectProduct(Group(S1,S2), Group(S1,S2), Group(S1,S2));;
e1 := Embedding(D3,1);; e2 := Embedding(D3,2);; e3 := Embedding(D3,3);;
tupleOf := function(h)
  return Image(e1, EvalS(h, c3.x, c3.y)) * Image(e2, EvalS(h, c4.x, c4.y)) * Image(e3, EvalS(h, c5.x, c5.y));
end;;
schreier := [];;
for elt in queue do
  u := LookupDictionary(wordOf, elt);
  for gl in gens4 do
    if gl.g = "x" then gp := xbar^gl.e; else gp := ybar^gl.e; fi;
    w := Concatenation(u, [gl]);
    u2 := LookupDictionary(wordOf, elt*gp);
    h := Concatenation(w, InvW(u2));
    if EvalS(h, xbar, ybar) <> () then Error("schreier not in kernel"); fi;
    if EvalS(h, c234.x, c234.y) <> () then Error("c234 does not kill kernel?"); fi;
    Add(schreier, tupleOf(h));
  od;
od;;
H3 := Group(schreier);;
Print("H3 size = ", Size(H3), "\n");
if Size(H3) > 2000000 then Error("H3 too large for direct enumeration: ", Size(H3)); fi;
H3elts := Elements(H3);;
p1 := Projection(D3,1);; p2 := Projection(D3,2);; p3 := Projection(D3,3);;

## ∃-判定: 各 A5 類 f について、base 三つ組 * H3 軌道に (2.20) 解があるか
liveCount := 0;; liveList := [];;
for elt in queue do
  u := LookupDictionary(wordOf, elt);
  F123 := EvalS(u, c123.x, c123.y);
  F234 := EvalS(u, c234.x, c234.y);
  b3 := EvalS(u, c3.x, c3.y);
  b4 := EvalS(u, c4.x, c4.y);
  b5 := EvalS(u, c5.x, c5.y);
  live := false;
  for h in H3elts do
    h3 := Image(p1, h); h4 := Image(p2, h); h5 := Image(p3, h);
    ## paper (2.20) straight: F234 * F1_23_4 * F123 = F1_2_34 * F12_3_4
    if F234 * (b4*h4) * F123 = (b5*h5) * (b3*h3) then
      live := true; break;
    fi;
  od;
  if live then liveCount := liveCount + 1; Add(liveList, elt); fi;
od;;
Print("EXISTENTIAL pentagon census: live = ", liveCount, " / 60\n");

## 20 shadow への貼り付け(readA=straight 左→右)
Read("search/probe/wac_v1/_pent_pi_shadows.g");;
EvalFW := function(fw, xi, yi) local v,p; v:=xi^0; for p in fw do if p[1]="x" then v:=v*xi^p[2]; else v:=v*yi^p[2]; fi; od; return v; end;;
shPass := 0;; perM := rec(m0:=0,m1:=0,m3:=0,m4:=0);;
for sh in SHADOW_LIST do
  e := EvalFW(sh.f_word, xbar, ybar);
  if e in liveList then
    shPass := shPass + 1;
    if sh.m = 0 then perM.m0 := perM.m0+1; elif sh.m = 1 then perM.m1 := perM.m1+1;
    elif sh.m = 3 then perM.m3 := perM.m3+1; else perM.m4 := perM.m4+1; fi;
  fi;
od;;
Print("shadows: ", shPass, "/20  per-m [m0,m1,m3,m4]=[", perM.m0, ",", perM.m1, ",", perM.m3, ",", perM.m4, "]\n");
Print("PENT_PI_V2_DONE\n");
Print("LIVE_LIST: ");; for e in liveList do Print(e, " | "); od;; Print("\n");;
QUIT;
