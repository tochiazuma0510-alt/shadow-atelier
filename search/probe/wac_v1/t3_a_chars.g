#############################################################################
## search/probe/wac_v1/t3_a_chars.g   [T3 / 準 pure-cycle 剛性]
##
## 族 (2^k 1^*, 3^j 1^*, w0=(ell,1^t)) の C_{S_n}(w0)-軌道数 N を指標計数で作表。
##
##  T_all^{(k,j)}(ell,a) := #{(g,h) : g in 2^k1^*, h in 3^j1^*, g*h = w0=(ell,1^a)}
##                          (S_{ell+a} の class multiplication coefficient)
##  非推移分の差し引き:  <g,h> の軌道は w0 の巡回の合併。1-巡回のみからなる
##  ブロック B では T_trans(1^b) = delta_{b,1}(gh=1 かつ g^2=h^3=1 => g=h=1)。
##  ゆえに  T_all(ell,1^t) = sum_a Binomial(t,a) T_trans(ell,1^a)  (二項変換)
##  =>      T_trans(ell,1^t) = sum_a (-1)^{t-a} Binomial(t,a) T_all(ell,1^a).
##  型 (k,j) は非推移分解でも保存される(孤立点は g,h の不動点)ので型ごとに閉じる。
##
##  N := T_trans / (ell * t!)   ( |C_{S_n}(w0)| = ell * t! )
##  ell 素数・t<ell なら Aut(map) | gcd(ell,t) = 1 ゆえ C(w0)-作用は自由 => N は整数。
##
## GAP 4.16.0 単系統。cross-checked ではない。台帳請求権なし。
#############################################################################

TblCache := NewDictionary(1, true);;
CPCache  := NewDictionary(1, true);;

GetTbl := function(m)
  local v;
  v := LookupDictionary(TblCache, m);
  if v = fail then
    v := CharacterTable("Symmetric", m);
    AddDictionary(TblCache, m, v);
  fi;
  return v;
end;;

GetCP := function(m)
  local v;
  v := LookupDictionary(CPCache, m);
  if v = fail then
    v := List(ClassParameters(GetTbl(m)), z -> SortedList(z[2]));
    AddDictionary(CPCache, m, v);
  fi;
  return v;
end;;

ClassIdx := function(m, part)
  local cp;
  cp := GetCP(m);
  return First([1..Length(cp)], z -> cp[z] = SortedList(part));
end;;

## 型 2^k 1^{m-2k} / 3^j 1^{m-3j} / (ell,1^a) の分割表現
TypeInv := function(m,k) return Concatenation(ListWithIdenticalEntries(k,2),
                                              ListWithIdenticalEntries(m-2*k,1)); end;;
TypeThr := function(m,j) return Concatenation(ListWithIdenticalEntries(j,3),
                                              ListWithIdenticalEntries(m-3*j,1)); end;;

TAllCache := NewDictionary([1,1,1,1], true);;
TAllKJ := function(ell, a, k, j)
  local m, key, v, tbl, iw, i2, i3;
  m := ell + a;
  if 2*k > m or 3*j > m then return 0; fi;
  key := [ell,a,k,j];
  v := LookupDictionary(TAllCache, key); if v <> fail then return v; fi;
  tbl := GetTbl(m);
  iw := ClassIdx(m, Concatenation([ell], ListWithIdenticalEntries(a,1)));
  i2 := ClassIdx(m, TypeInv(m,k));
  i3 := ClassIdx(m, TypeThr(m,j));
  if iw = fail or i2 = fail or i3 = fail then return fail; fi;
  v := ClassMultiplicationCoefficient(tbl, i2, i3, iw);
  AddDictionary(TAllCache, key, v);
  return v;
end;;

TTransKJ := function(ell, t, k, j)
  local s, a;
  s := 0;
  for a in [0..t] do
    s := s + (-1)^(t-a) * Binomial(t,a) * TAllKJ(ell,a,k,j);
  od;
  return s;
end;;

## ---------------------------------------------------------------------------
## 掃引: ell, t, (k,j).  genus = (k+2j-(ell+2t-1))/2 >= 0 のみ表示(< 0 は Ree で 0)
## ---------------------------------------------------------------------------
Sweep := function(ellList, nMax, tMax)
  local ell, t, n, k, j, kmax, jmax, ta, tt, cw, N, gen, jordan, prim, printedHdr;
  for ell in ellList do
    for t in [0..tMax] do
      n := ell + t;
      if n > nMax then continue; fi;
      cw := ell * Factorial(t);
      printedHdr := false;
      kmax := QuoInt(n,2); jmax := QuoInt(n,3);
      for k in [0..kmax] do
        ## sgn(w0)=(-1)^{ell-1}; sgn(g)=(-1)^k, sgn(h)=1  =>  k = ell-1 mod 2
        if (k - (ell-1)) mod 2 <> 0 then continue; fi;
        for j in [0..jmax] do
          if k + 2*j < ell + 2*t - 1 then continue; fi;          # genus >= 0
          if (k + 2*j - (ell+2*t-1)) mod 2 <> 0 then continue; fi;
          tt := TTransKJ(ell,t,k,j);
          if tt = 0 then continue; fi;
          ta := TAllKJ(ell,t,k,j);
          N  := tt / cw;
          if not printedHdr then
            Print("\n--- ell=", ell, " t=", t, " n=", n,
                  "   |C(w0)|=", cw, " (=ell*t!)   ell prime? ", IsPrime(ell), "\n");
            printedHdr := true;
          fi;
          ## Jordan: ell 素数 & ell>n/2 (=> 推移なら原始) & ell<=n-3 => <g,h> >= A_n
          jordan := IsPrime(ell) and 2*ell > n and ell <= n-3;
          Print("    (k,j)=(", k, ",", j, ")  g=", 2*k, "pt h=", 3*j,
                "pt  genus=", (k+2*j-(ell+2*t-1))/2,
                "   T_all=", ta, "  T_trans=", tt, "   N=T_trans/|C| = ", N,
                Concatenation(["   Jordan(gen auto)=", String(jordan)]), "\n");
        od;
      od;
    od;
  od;
  return true;
end;;

Print("############ T3-A : N table (character counting) ############\n");
Print("## N = (# C(w0)-orbits on generating-or-merely-transitive (2,3)-factorizations)\n");
Print("## Jordan=true の行では 推移 <=> 生成(A_n or S_n) なので N は剛性そのもの。\n");

Sweep([5,7,9,11,13], 20, 7);;
Sweep([14], 18, 4);;      ## ell 偶(族外・木モデル較正用: Aut 非自明が出るはず)
Sweep([17,19], 22, 3);;

Print("\nT3_A_DONE\n");
QUIT;
