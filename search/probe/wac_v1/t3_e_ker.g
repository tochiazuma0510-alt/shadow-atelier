#############################################################################
## search/probe/wac_v1/t3_e_ker.g   [T3 / 準 pure-cycle 剛性]
##
## 目的: 「Nielsen 類の軌道数 N」と「ker chi~ の大きさ」の関係を実測で確定する。
##
## 記号 (sat_l1_v1 §2, §6.2): f in P=A_n, g:=f*a1, h:=f*b1^-1, v:=a1*b1^-1=g*h,
##   hexagon(m=0)  <=>  g^2=1 かつ h^3=1                     [定理 RED]
##   全射条件      <=>  <xbar, ybar^f> = P.
## ここで xbar = w^2 = a1 v^2 a1、ybar = v^2、ybar^f = a1 (g v^2 g) a1 なので
##   全射条件  <=>  < v^2 , g v^2 g > = A_n        (a1 共役で移すだけ)
## => ker chi~  <->  K(v) := { g : g^2=1, (g v)^3=1, < v^2, g v^2 g > = A_n }.
##
## 一方 T3 の N は  F(v) := { g : g^2=1, (gv)^3=1, <g, gv> >= A_n } の
## C(v)-軌道数。K(v) ⊆ F(v) は自明(<v^2,gv^2g> ⊆ <g,gv>)。
## 本 probe は K(v) を直接測り、F(v)/C(v) との差を出す。
##
## GAP 4.16.0 単系統。台帳請求権なし。
#############################################################################

InvolutionsOfType := function(n, k)
  local res, img, free, rec1;
  res := []; img := List([1..n], x -> x); free := List([1..n], x -> true);
  rec1 := function(np, nf)
    local i, q;
    i := First([1..n], x -> free[x]);
    if i = fail then
      if np = k then Add(res, PermList(ShallowCopy(img))); fi;
      return;
    fi;
    if nf > 0 then free[i] := false; rec1(np, nf-1); free[i] := true; fi;
    if np < k then
      free[i] := false;
      for q in [i+1..n] do
        if free[q] then
          free[q] := false; img[i] := q; img[q] := i;
          rec1(np+1, nf);
          img[i] := i; img[q] := q; free[q] := true;
        fi;
      od;
      free[i] := true;
    fi;
    return;
  end;
  rec1(0, n-2*k);
  return res;
end;;
CycleTypeOf := function(p,n) return SortedList(CycleLengths(p,[1..n])); end;;

KerTest := function(ell, t, k, j)
  local n, v, y, An, sols, g, h, gen, ker, C, cg, orbF, orbK, a1, orb_a1, x;
  n := ell+t;
  v := PermList(Concatenation(List([1..ell-1], x->x+1), [1], [ell+1..n]));
  y := v^2;                                     ## ybar
  An := AlternatingGroup(n);
  Print("\n### ell=", ell, " t=", t, " n=", n, " (k,j)=(", k, ",", j, ")",
        "   v 型=", CycleTypeOf(v,n), "  ybar=v^2 型=", CycleTypeOf(y,n), "\n");
  sols := [];
  for g in InvolutionsOfType(n,k) do
    h := g*v;
    if h^3 = () and CycleTypeOf(h,n) =
       SortedList(Concatenation(ListWithIdenticalEntries(j,3),
                                ListWithIdenticalEntries(n-3*j,1))) then
      Add(sols, g);
    fi;
  od;
  gen := Filtered(sols, g -> Size(Group(g, g*v)) >= Factorial(n)/2);
  ker := Filtered(gen, g -> Group(y, y^g) = An or Size(Group(y,y^g)) >= Factorial(n)/2);
  cg := [v]; Append(cg, List([ell+1..n-1], x -> (x,x+1)));
  C := Group(cg);
  orbF := Orbits(C, gen, OnPoints);
  Print("    |F(v)| (<g,h> >= A_n) = ", Length(gen),
        "   C(v)-軌道数 N = ", Length(orbF), "\n");
  Print("    |K(v)| (全射条件 <v^2,gv^2g>=A_n) = ", Length(ker), "   |C(v)| = ", Size(C), "\n");
  if Length(ker) > 0 then
    orbK := Orbits(C, ker, OnPoints);
    Print("    K(v) の C(v)-軌道数 = ", Length(orbK),
          "   軌道長 = ", Collected(List(orbK, Length)), "\n");
    a1 := ker[1];
    orb_a1 := Orbit(C, a1, OnPoints);
    Print("    SURV 軌道 a1^{C(v)} の長さ = ", Length(orb_a1),
          "   K(v) = a1^{C(v)} ? ", Set(ker) = Set(orb_a1), "\n");
    Print("    => |ker chi~| = ", Length(ker), " ,  |C(v)| = ", Size(C),
          " ,  CENT (= 等号) ? ", Length(ker) = Size(C), "\n");
  fi;
  return true;
end;;

Print("############ T3-E : ker chi~ の真の大きさ vs Nielsen 軌道数 N ############\n");
KerTest(9,1,4,3);;     ## 既知: 工房実測 |ker|=9.  N=6 なら「N=1 は必要条件ではない」
KerTest(7,2,4,3);;     ## N=1 だが <g,h> は A_9 に届かない(PSL(2,8) 504)
KerTest(11,2,6,4);;    ## N=6
KerTest(13,3,8,5);;    ## N=2 (Jordan 安全域)
KerTest(11,1,6,3);;    ## genus 0, (k,j)=(6,3): N=2
KerTest(13,2,6,5);;    ## N=10

Print("\nT3_E_DONE\n");
QUIT;
