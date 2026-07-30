#############################################################################
## search/probe/wac_v1/t3_c_sweep.g   [T3 / 準 pure-cycle 剛性]
##
## MN エンジンで (ell 素数, t, k, j) を系統掃引し
##   (i) 種数 0 での木モデル閉形  N = Cat(m-1)*m!/(t! f2! f3!),  m=t+f2+f3-1
##       を全行で照合、
##   (ii) 種数 >=1 の N を実測(閉形は未導出 = UNKNOWN)、
##   (iii) Jordan 安全域(ell 素数, ell>n/2, ell<=n-3 <=> t>=3)で N=1 になる窓を列挙。
##
## GAP 4.16.0 単系統。台帳請求権なし。
#############################################################################

BetaOf := function(lam)
  local r, i; r := Length(lam);
  return List([1..r], i -> lam[i] + r - i);
end;;
PartOfBeta := function(B)
  local b, r, i;
  b := Reversed(SortedList(B)); r := Length(b);
  return Filtered(List([1..r], i -> b[i] - (r-i)), x -> x > 0);
end;;
RimRemovals := function(lam, q)
  local B, res, i, bi, nb, ht, Bset;
  B := BetaOf(lam); Bset := Set(B); res := [];
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
FDimCache := NewDictionary([1], true);;
FDim := function(lam)
  local n, i, jj, conj, prod, h, v;
  v := LookupDictionary(FDimCache, lam); if v <> fail then return v; fi;
  n := Sum(lam); if n = 0 then return 1; fi;
  conj := AssociatedPartition(lam); prod := 1;
  for i in [1..Length(lam)] do for jj in [1..lam[i]] do
    prod := prod * ((lam[i]-jj) + (conj[jj]-i) + 1);
  od; od;
  v := Factorial(n)/prod; AddDictionary(FDimCache, lam, v); return v;
end;;

ChiCache := 0;; ChiQ := 0;; ChiF := 0;;
ChiRec := function(lam)
  local v, s, rr;
  v := LookupDictionary(ChiCache, lam); if v <> fail then return v; fi;
  if Sum(lam) = ChiF then v := FDim(lam);
  else
    s := 0;
    for rr in RimRemovals(lam, ChiQ) do s := s + rr[2]*ChiRec(rr[1]); od;
    v := s;
  fi;
  AddDictionary(ChiCache, lam, v); return v;
end;;
CtxCache := NewDictionary([1,1,1], true);;   ## (m,q,f) -> dictionary
UseCtx := function(m,q,f)
  local d;
  d := LookupDictionary(CtxCache, [m,q,f]);
  if d = fail then d := NewDictionary([1], true); AddDictionary(CtxCache,[m,q,f],d); fi;
  ChiCache := d; ChiQ := q; ChiF := f; return true;
end;;

LamCache := NewDictionary([1,1], true);;
GoodLams := function(m, ell)
  local v;
  v := LookupDictionary(LamCache, [m,ell]); if v <> fail then return v; fi;
  v := Filtered(Partitions(m), lam -> Length(RimRemovals(lam, ell)) > 0);
  AddDictionary(LamCache, [m,ell], v); return v;
end;;
CentSizeOfType := function(lam)
  local s, c; s := 1;
  for c in Collected(SortedList(lam)) do s := s*c[1]^c[2]*Factorial(c[2]); od;
  return s;
end;;

TAllCache := NewDictionary([1,1,1,1], true);;
TAllMN := function(ell, a, k, j)
  local m, c1, c2, lams, lam, s, f2, f3, cw, cz, ct, key, v, i;
  m := ell + a;
  if 2*k > m or 3*j > m then return 0; fi;
  key := [ell,a,k,j];
  v := LookupDictionary(TAllCache, key); if v <> fail then return v; fi;
  f2 := m - 2*k; f3 := m - 3*j;
  c1 := Factorial(m)/CentSizeOfType(Concatenation(ListWithIdenticalEntries(k,2),
                                                  ListWithIdenticalEntries(f2,1)));
  c2 := Factorial(m)/CentSizeOfType(Concatenation(ListWithIdenticalEntries(j,3),
                                                  ListWithIdenticalEntries(f3,1)));
  lams := GoodLams(m, ell);
  cw := []; UseCtx(m,ell,a); for lam in lams do Add(cw, ChiRec(lam)); od;
  cz := []; UseCtx(m,2,f2);  for lam in lams do Add(cz, ChiRec(lam)); od;
  ct := []; UseCtx(m,3,f3);  for lam in lams do Add(ct, ChiRec(lam)); od;
  s := 0;
  for i in [1..Length(lams)] do
    if cw[i] <> 0 and cz[i] <> 0 and ct[i] <> 0 then
      s := s + cz[i]*ct[i]*cw[i]/FDim(lams[i]);
    fi;
  od;
  v := c1*c2*s/Factorial(m);
  AddDictionary(TAllCache, key, v); return v;
end;;
TTransMN := function(ell, t, k, j)
  local s, a;
  s := 0;
  for a in [0..t] do s := s + (-1)^(t-a)*Binomial(t,a)*TAllMN(ell,a,k,j); od;
  return s;
end;;
TreePred := function(n, t, k, j)
  local f2, f3, m;
  f2 := n - 2*k; f3 := n - 3*j; m := t + f2 + f3 - 1;
  if m < 1 then return fail; fi;
  return Binomial(2*m-2,m-1)/m * Factorial(m)/(Factorial(t)*Factorial(f2)*Factorial(f3));
end;;

Print("############ T3-C : 系統掃引(MN)+ 木モデル閉形の照合 ############\n");
Print("## 列: ell t n (k,j) f2 f3 genus | T_trans |C| N | 木モデル予言 | 一致 | Jordan\n");

bad := [];;   ok0 := 0;;  rows := 0;;  onesJordan := [];;
DoSweep := function(ellList, nMax, tMax)
  local ell,t,n,k,j,tt,cw,N,g0,pred,jordan,agree;
  for ell in ellList do
   for t in [0..tMax] do
    n := ell+t; if n > nMax then continue; fi;
    cw := ell*Factorial(t);
    for k in [0..QuoInt(n,2)] do
     if (k - (ell-1)) mod 2 <> 0 then continue; fi;
     for j in [0..QuoInt(n,3)] do
      if k+2*j < ell+2*t-1 then continue; fi;
      if (k+2*j-(ell+2*t-1)) mod 2 <> 0 then continue; fi;
      g0 := (k+2*j-(ell+2*t-1))/2;
      tt := TTransMN(ell,t,k,j);
      if tt = 0 then continue; fi;
      N := tt/cw; pred := TreePred(n,t,k,j);
      jordan := IsPrime(ell) and 2*ell > n and ell <= n-3;
      rows := rows+1;
      agree := (g0 <> 0) or (N = pred);
      if g0 = 0 then
        if N = pred then ok0 := ok0+1; else Add(bad, [ell,t,k,j,N,pred]); fi;
      fi;
      if N = 1 and jordan then Add(onesJordan, [ell,t,n,k,j,g0]); fi;
      Print("  ", ell, " ", t, " ", n, " (", k, ",", j, ") f2=", n-2*k,
            " f3=", n-3*j, " g=", g0, " | ", tt, " ", cw, " N=", N,
            " | pred=", pred, " | ", agree, " | J=", jordan, "\n");
     od;
    od;
   od;
  od;
  return true;
end;;

DoSweep([5,7,11,13,17,19], 26, 8);;
DoSweep([23], 30, 7);;
DoSweep([29], 34, 5);;

Print("\n=== 種数 0 行の木モデル照合: 一致 ", ok0, " 件 / 不一致 ", Length(bad), " 件\n");
if Length(bad) > 0 then Print("  不一致: ", bad, "\n"); fi;
Print("=== Jordan 安全域(推移<=>生成)で N=1 の窓: ", onesJordan, "\n");
Print("    (書式 [ell,t,n,k,j,genus])\n");

Print("\n=== 追加: Jordan 安全域の種数 1 窓 n=32 (ell=29,t=3,k=16,j=10) ===\n");
tt := TTransMN(29,3,16,10);;
Print("    T_trans=", tt, "  |C|=", 29*6, "  N=", tt/(29*6), "\n");

Print("\nT3_C_DONE\n");
QUIT;
