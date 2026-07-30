#############################################################################
## search/probe/wac_v1/expA_scan.g
##   実験 A(裁定 243 工程 1)工程 1: 「N_gen >= 2 になる最小 passport」の探索
##
## 入力: なし(自己完結)。触れてよいデータ範囲: 対称群の指標表のみ(ctbllib)。
## モード: 計数のみ。窓の実物(a1,b1)は一切構成しない。
##
## 計算する量(sat_l1_v1 §10.6.2 の機構をそのまま使用):
##   T_all(λ)   = #{(g,h): g^2=1, h^3=1, g*h = w0}          (w0 の型 λ)
##   T_trans(λ) = そのうち <g,h> が推移的なもの(巡回の集合分割上の Moebius)
##   T_gen(λ)   = そのうち <g,h> ⊇ A_n なもの                (= |ker χ~|;定理 RED)
##   N_gen(λ)   = T_gen/|C_Sn(w0)|                           (SAT-RIG の自由作用)
##
## 判定の格(本 probe が厳密に言えること):
##   (a) R := T_trans/|C| は N_gen の**上界**(T_gen <= T_trans)。
##       ⟹ R < 2 なら N_gen <= 1 が**厳密に**従う(全 λ で有効)。
##   (b) λ が clean(= 素数の部分 ℓ で n/2 < ℓ <= n-3 をもつ)なら
##       推移 ⟹ 原始(ブロック論法)⟹ Jordan ⟹ ⊇A_n。よって T_gen = T_trans、
##       **N_gen = R が厳密**。
##   (c) それ以外(R>=2 かつ non-clean)は本 probe では UNDETERMINED。
##
## 自己検査(不変量):
##   I1: probe8 の 11 窓較正値を再現する。
##   I2: clean λ では R は非負整数でなければならない(自由作用の帰結)。破れたらバグ。
##
## f_orientation: N/A(この probe は f を構成しない — 計数のみ)
## Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
Read("search/gaplib_common.g");

#############################################################################
## ---- 指標表キャッシュ ------------------------------------------------------
#############################################################################
TblCache := NewDictionary(1, true);;
GetTbl := function(n)
  local v, tbl, cp, invs, thr, i, part;
  v := LookupDictionary(TblCache, n);
  if v <> fail then return v; fi;
  tbl := CharacterTable("Symmetric", n);
  cp  := ClassParameters(tbl);
  invs := [];  thr := [];
  for i in [1..Length(cp)] do
    part := cp[i][2];
    if ForAll(part, e -> e in [1,2]) then Add(invs, i); fi;
    if ForAll(part, e -> e in [1,3]) then Add(thr, i); fi;
  od;
  v := rec(tbl := tbl, cp := cp, invs := invs, thr := thr);
  AddDictionary(TblCache, n, v);
  return v;
end;;

TAllCache := NewDictionary([1,1], true);;
TAll := function(lambda)
  local key, v, n, R, kk, tot, i, j;
  key := SortedList(lambda);
  v := LookupDictionary(TAllCache, key);
  if v <> fail then return v; fi;
  n := Sum(lambda);
  if n = 0 then return 1; fi;
  if n = 1 then AddDictionary(TAllCache, key, 1); return 1; fi;
  R := GetTbl(n);
  kk := First([1..Length(R.cp)], z -> SortedList(R.cp[z][2]) = key);
  if kk = fail then return fail; fi;
  tot := 0;
  for i in R.invs do for j in R.thr do
    tot := tot + ClassMultiplicationCoefficient(R.tbl, j, i, kk);
  od; od;
  AddDictionary(TAllCache, key, tot);
  return tot;
end;;

SetPartitions := function(m)
  local rec1;
  rec1 := function(i, blocks)
    local res, nb, k;
    if i > m then return [ List(blocks, ShallowCopy) ]; fi;
    res := [];
    for k in [1..Length(blocks)] do
      nb := List(blocks, ShallowCopy);
      Add(nb[k], i);
      Append(res, rec1(i+1, nb));
    od;
    nb := List(blocks, ShallowCopy); Add(nb, [i]);
    Append(res, rec1(i+1, nb));
    return res;
  end;
  return rec1(1, []);
end;;

TTransCache := NewDictionary([1,1], true);;
TTrans := function(lambda)
  local key, v, m, parts, tot, pi, prod, B;
  key := SortedList(lambda);
  v := LookupDictionary(TTransCache, key);
  if v <> fail then return v; fi;
  m := Length(lambda);
  if m = 1 then
    v := TAll(lambda);
    AddDictionary(TTransCache, key, v); return v;
  fi;
  parts := SetPartitions(m);
  tot := 0;
  for pi in parts do
    if Length(pi) = 1 then continue; fi;
    prod := 1;
    for B in pi do prod := prod * TTrans(lambda{B}); od;
    tot := tot + prod;
  od;
  v := TAll(lambda) - tot;
  AddDictionary(TTransCache, key, v);
  return v;
end;;

CentSize := function(lambda)
  local mult, s, c;
  mult := Collected(SortedList(lambda));
  s := 1;
  for c in mult do s := s * c[1]^c[2] * Factorial(c[2]); od;
  return s;
end;;

## clean 判定: 素数 ℓ で n/2 < ℓ <= n-3 なる部分をもつか
CleanEll := function(lambda)
  local n, l, best;
  n := Sum(lambda);  best := fail;
  for l in Set(lambda) do
    if IsPrime(l) and 2*l > n and l <= n-3 then best := l; fi;
  od;
  return best;
end;;

#############################################################################
## ---- I1: 較正(probe8 の 11 窓)---------------------------------------------
#############################################################################
CAL := [ [[5,5],75,50], [[10],65,65], [[5,5,2],275,100], [[10,5],1035,710],
         [[9,1],90,54], [[9,2],90,54], [[9,2,1],270,54], [[9,2,2],216,72],
         [[11,2,2,1],2354,88] ];;
Print("=== I1 較正(probe8 の値の再現)===\n");
CALFAIL := 0;;
for cc in CAL do
  ta := TAll(cc[1]);  tt := TTrans(cc[1]);
  if ta <> cc[2] or tt <> cc[3] then
    CALFAIL := CALFAIL + 1;
    Print("  [FAIL] ", cc[1], " got T_all=", ta, " T_trans=", tt,
          " expected ", cc[2], "/", cc[3], "\n");
  else
    Print("  [ok] ", cc[1], "  T_all=", ta, " T_trans=", tt, "\n");
  fi;
od;
Print("I1 CAL_FAILS = ", CALFAIL, "\n\n");

#############################################################################
## ---- 走査 -------------------------------------------------------------------
#############################################################################
if not IsBound(EXPA_NLO) then EXPA_NLO := 8;; fi;
if not IsBound(EXPA_NHI) then EXPA_NHI := 20;; fi;
if not IsBound(EXPA_CLEANONLY) then EXPA_CLEANONLY := false;; fi;

ROWS := [];;
INTFAIL := 0;;
Print("=== 走査 n=", EXPA_NLO, "..", EXPA_NHI,
      "  (clean_only=", EXPA_CLEANONLY, ") ===\n");
Print("# 列: n | lambda | ord(w0) | |C| | T_all | T_trans | R=T_trans/|C| | clean_ell | 判定\n");
for n in [EXPA_NLO .. EXPA_NHI] do
  fb := QuoInt(n,2) + 2*QuoInt(n,3) - n + 2;     ## Ree: c(lambda) <= fb
  cands := [];
  if EXPA_CLEANONLY then
    for l in Filtered([5..n-3], z -> IsPrime(z) and 2*z > n) do
      for kk in [1 .. fb-1] do
        for mu in Partitions(n-l, kk) do
          Add(cands, SortedList(Concatenation([l], mu)));
        od;
      od;
    od;
  else
    for kk in [1 .. fb] do
      for mu in Partitions(n, kk) do Add(cands, SortedList(mu)); od;
    od;
  fi;
  cands := Set(cands);
  cands := Filtered(cands, lam -> Lcm(lam) >= 7);
  Print("-- n=", n, "  Ree c<=", fb, "  #lambda=", Length(cands), "\n");
  for lam in cands do
    if GAPLIB_CheckCap(540.0, "expA_scan") then
      Print("!! CAP reached at n=", n, " lambda=", lam, " -- stopping scan\n");
      break;
    fi;
    ta := TAll(lam);
    if ta = fail or ta = 0 then continue; fi;
    tt := TTrans(lam);
    if tt <= 0 then continue; fi;
    cw := CentSize(lam);
    R  := tt/cw;
    ce := CleanEll(lam);
    verdict := "";
    if ce <> fail then
      if not IsInt(R) then
        INTFAIL := INTFAIL + 1;
        verdict := "**I2-VIOLATION** (clean なのに R が非整数)";
      elif R >= 2 then
        verdict := Concatenation("*** N_gen = ", String(R), " >= 2  <== 標的 ***");
      else
        verdict := Concatenation("N_gen = ", String(R), " (厳密)");
      fi;
    else
      if R < 2 then
        verdict := "N_gen <= 1 (厳密・上界による)";
      else
        verdict := "UNDETERMINED (non-clean, R>=2)";
      fi;
    fi;
    if ce = fail then cestr := "-"; else cestr := String(ce); fi;
    Print("  ", n, " | ", lam, " | ord=", Lcm(lam), " | |C|=", cw, " | ", ta,
          " | ", tt, " | ", R, " | ", cestr, " | ", verdict, "\n");
    Add(ROWS, rec(n := n, lam := lam, ord := Lcm(lam), cw := cw, ta := ta,
                  tt := tt, clean := ce, R := R));
  od;
od;

Print("\n=== 要約 ===\n");
Print("I2 違反(clean で R 非整数) = ", INTFAIL, "\n");
hits := Filtered(ROWS, r -> r.clean <> fail and IsInt(r.R) and r.R >= 2);;
Print("clean かつ N_gen>=2 の passport 個数 = ", Length(hits), "\n");
for r in hits do
  Print("   HIT: n=", r.n, " lambda=", r.lam, " |C|=", r.cw,
        " T_gen=", r.tt, " N_gen=", r.R, " (clean ell=", r.clean, ")\n");
od;
und := Filtered(ROWS, r -> r.clean = fail and r.R >= 2);;
Print("UNDETERMINED(non-clean, R>=2)の個数 = ", Length(und), "\n");
Print("そのうち n 最小 = ",
      List(Filtered(und, r -> r.n = Minimum(List(und, z -> z.n))), r -> r.lam), "\n");
Print("\nEXPA_SCAN_DONE\n");
QUIT;
