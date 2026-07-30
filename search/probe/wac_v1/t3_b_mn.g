#############################################################################
## search/probe/wac_v1/t3_b_mn.g   [T3 / 準 pure-cycle 剛性]
##
## Murnaghan-Nakayama を自前実装し、Frobenius 和で
##   T_all^{(k,j)}(ell,a) = #{(g,h): g in 2^k1^*, h in 3^j1^*, g*h = (ell,1^a)}
## を n<=40 程度まで計算する(完全指標表を作らずに済む)。
##
## 使う事実: t<ell なら lambda の ell-weight は 0 or 1 で、chi_lambda(w0)=0 は
## ell-weight 0 の全 lambda で成立 => 和は ell*p(t) 項に落ちる。
## さらに chi_lambda(2^k1^{f2})=0 は 2-core が 1^{f2} 型でない lambda で成立(MN)。
##
## 検算: n<=20 は t3_a_chars.g(完全指標表)と一致すべき。
## GAP 4.16.0 単系統。台帳請求権なし。
#############################################################################

## ---- 分割 <-> beta 集合 -----------------------------------------------
BetaOf := function(lam)
  local r, i;
  r := Length(lam);
  return List([1..r], i -> lam[i] + r - i);
end;;
PartOfBeta := function(B)
  local b, r, i;
  b := Reversed(SortedList(B));       # 降順
  r := Length(b);
  return Filtered(List([1..r], i -> b[i] - (r-i)), x -> x > 0);
end;;

## lam から長さ q の rim hook を取り除く全ての結果 [新 lam, 符号]
RimRemovals := function(lam, q)
  local B, res, i, bi, nb, ht, Bset;
  B := BetaOf(lam);
  Bset := Set(B);
  res := [];
  for i in [1..Length(B)] do
    bi := B[i];
    if bi - q >= 0 and not (bi - q) in Bset then
      ht := Number(B, x -> x < bi and x > bi - q);
      nb := ShallowCopy(B); nb[i] := bi - q;
      Add(res, [ PartOfBeta(nb), (-1)^ht ]);
    fi;
  od;
  return res;
end;;

## 標準盤の個数(hook length formula)
FDimCache := NewDictionary([1], true);;
FDim := function(lam)
  local n, i, jj, conj, prod, h, v, key;
  key := ShallowCopy(lam);
  v := LookupDictionary(FDimCache, key); if v <> fail then return v; fi;
  n := Sum(lam);
  if n = 0 then return 1; fi;
  conj := AssociatedPartition(lam);
  prod := 1;
  for i in [1..Length(lam)] do
    for jj in [1..lam[i]] do
      h := (lam[i] - jj) + (conj[jj] - i) + 1;
      prod := prod * h;
    od;
  od;
  v := Factorial(n)/prod;
  AddDictionary(FDimCache, key, v);
  return v;
end;;

## chi_lam( q^{(|lam|-f)/q} 1^f )  : q-rim hook を全部剥いでから f^mu
ChiPowCache := 0;;  ChiPowQ := 0;;  ChiPowF := 0;;
ChiPow := function(lam)
  local v, s, rr;
  v := LookupDictionary(ChiPowCache, lam); if v <> fail then return v; fi;
  if Sum(lam) = ChiPowF then
    v := FDim(lam);
  else
    s := 0;
    for rr in RimRemovals(lam, ChiPowQ) do
      s := s + rr[2]*ChiPow(rr[1]);
    od;
    v := s;
  fi;
  AddDictionary(ChiPowCache, lam, v);
  return v;
end;;
ChiAtPow := function(lam, q, f)     ## 呼び出し口(キャッシュを q,f ごとに張り替え)
  local savC, savQ, savF, v;
  savC := ChiPowCache; savQ := ChiPowQ; savF := ChiPowF;
  if not (IsRecord(savC) or savC = 0) then fi;
  ChiPowCache := NewDictionary([1], true); ChiPowQ := q; ChiPowF := f;
  v := ChiPow(lam);
  ChiPowCache := savC; ChiPowQ := savQ; ChiPowF := savF;
  return v;
end;;

## 高速化: 同じ (q,f) の連続呼び出しでキャッシュを共有するための版
SetChiCtx := function(q,f)
  ChiPowCache := NewDictionary([1], true); ChiPowQ := q; ChiPowF := f;
  return true;
end;;

CentSizeOfType := function(lam)
  local s, c;
  s := 1;
  for c in Collected(SortedList(lam)) do s := s*c[1]^c[2]*Factorial(c[2]); od;
  return s;
end;;

## T_all(ell, a, k, j)  : S_m, m=ell+a
TAllMN := function(ell, a, k, j)
  local m, w0, c1, c2, cw, lams, lam, s, x2, x3, xw, f2, f3, chi2, chi3, chiw, fl;
  m := ell + a;
  if 2*k > m or 3*j > m then return 0; fi;
  f2 := m - 2*k; f3 := m - 3*j;
  w0 := Concatenation([ell], ListWithIdenticalEntries(a,1));
  c1 := Factorial(m)/CentSizeOfType(Concatenation(ListWithIdenticalEntries(k,2),
                                                  ListWithIdenticalEntries(f2,1)));
  c2 := Factorial(m)/CentSizeOfType(Concatenation(ListWithIdenticalEntries(j,3),
                                                  ListWithIdenticalEntries(f3,1)));
  lams := Partitions(m);
  ## chi_lam(w0) != 0 の lam だけ残す(ell-rim hook をもつもの)
  lams := Filtered(lams, lam -> Length(RimRemovals(lam, ell)) > 0);
  s := 0;
  for lam in lams do
    SetChiCtx(ell, a);  chiw := ChiPow(lam);
    if chiw = 0 then continue; fi;
    SetChiCtx(2, f2);   chi2 := ChiPow(lam);
    if chi2 = 0 then continue; fi;
    SetChiCtx(3, f3);   chi3 := ChiPow(lam);
    if chi3 = 0 then continue; fi;
    fl := FDim(lam);
    s := s + chi2*chi3*chiw/fl;
  od;
  return c1*c2*s/Factorial(m);
end;;

TTransMN := function(ell, t, k, j)
  local s, a;
  s := 0;
  for a in [0..t] do
    s := s + (-1)^(t-a)*Binomial(t,a)*TAllMN(ell,a,k,j);
  od;
  return s;
end;;

## 木モデルの予言(種数 0):  N = Cat(m-1) * m!/(t! f3! f2!),  m = t+f2+f3-1
TreePred := function(n, t, k, j)
  local f2, f3, m;
  f2 := n - 2*k; f3 := n - 3*j;
  m := t + f2 + f3 - 1;
  if m < 1 then return fail; fi;
  return Binomial(2*m-2, m-1)/m * Factorial(m)/(Factorial(t)*Factorial(f2)*Factorial(f3));
end;;

Report := function(ell, t, k, j)
  local n, tt, cw, N, g0, pred;
  n := ell + t; cw := ell*Factorial(t);
  g0 := (k + 2*j - (ell + 2*t - 1))/2;
  tt := TTransMN(ell,t,k,j);
  N := tt/cw;
  pred := TreePred(n,t,k,j);
  Print("  ell=", ell, " t=", t, " n=", n, " (k,j)=(", k, ",", j, ")",
        " f2=", n-2*k, " f3=", n-3*j, " genus=", g0,
        "\n      T_trans=", tt, "  |C|=", cw, "  N=", N,
        "   木モデル予言(genus0)=", pred,
        "   一致? ", (g0 = 0 and N = pred), "\n");
  return N;
end;;

Print("############ T3-B : MN engine + 木モデル照合 ############\n");

Print("\n[1] 較正(t3_a_chars.g の完全指標表と一致すべき)\n");
Report(9,1,4,3);;      ## 期待 N=6   (W-E-A10-9t1)
Report(13,3,8,5);;     ## 期待 N=2
Report(17,3,10,6);;    ## 期待 N=10
Report(19,3,10,7);;    ## 期待 N=140
Report(9,3,6,4);;      ## 期待 N=1/3 (Aut=C3)
Report(14,4,9,6);;     ## 期待 N=1/2 (Aut=C2)

Print("\n[2] 壁窓 P-WALL-2 (n=24, ell=19, t=5, 不動点なし)\n");
Report(19,5,12,8);;    ## 期待 N=1  (既知の悉皆 2280 と一致すべき)

Print("\n[3] 予言テスト: n=36, ell=29, t=7, (k,j)=(18,12) 不動点なし\n");
Print("    木モデルの予言: N = Cat(5)*6!/7! = 42/7 = 6,  T_trans = 6*29*5040 = 876960\n");
Report(29,7,18,12);;

Print("\nT3_B_DONE\n");
QUIT;
