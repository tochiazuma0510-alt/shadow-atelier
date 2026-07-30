## live 集合の正体検査: pentagon(π-lift) の live 8 元 = RED(m=0 hexagon,
## 生成条件なし)の解集合か?(裁定 249 の観察の直接判定)
SetPrintFormattingStatus("*stdout*", false);;
X5 := (1,3,2,4,5);; Y5 := (1,3,4,5,2);; A5g := AlternatingGroup(5);;
found := [];;
for s in Elements(A5g) do
  if s <> () and s^2 = () then
    for t in Elements(A5g) do
      if t <> () and t^3 = () then
        a := s*(6,7); b := t*(6,7,8); s1 := b^-1*a; s2 := a*b^2;
        if s1^2 = X5 and s2^2 = Y5 and Size(Group(s,t)) = 60 then Add(found, rec(s:=s, t:=t)); fi;
      fi;
    od;
  fi;
od;;
W := found[1];;
live := [ (), (1,4,2), (2,5,3), (1,2,4), (2,3,5), (1,3,5,4,2), (1,3,2,5,4), (1,4)(3,5) ];;
## RED (sat_l1 定理 RED・judge 向き両方): (f a1)^2=1 かつ (f b1^-1)^3=1
redA := Filtered(Elements(A5g), f -> (f*W.s)^2 = () and (f*W.t^-1)^3 = ());;
redB := Filtered(Elements(A5g), f -> (W.s*f)^2 = () and (W.t^-1*f)^3 = ());;
redC := Filtered(Elements(A5g), f -> (f^-1*W.s)^2 = () and (f^-1*W.t^-1)^3 = ());;
Print("RED setA size=", Length(redA), " eq_live=", Set(redA) = Set(live), "\n");
Print("RED setB size=", Length(redB), " eq_live=", Set(redB) = Set(live), "\n");
Print("RED setC size=", Length(redC), " eq_live=", Set(redC) = Set(live), "\n");
Print("live size=", Length(live), "\n");
QUIT;
