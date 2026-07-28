#############################################################################
## search/wcp5d-verify.g -- FINDING WCP5-D の決着検算(数学者・裁定164/165)
##
## 正本ノート: docs/notes/wcp5d_resolution_v1.md
##
## 検証する命題(すべて fail-closed assert):
##  V1  Ad(Delta)|_{PB3/N} : x->y, y->x   (theta に c-補正は不要)
##  V2  Ad(delta)|_{PB3/N} : x->y, y->z*c (tau は c だけずれる)  ... V1/V2 は
##      LINS(index<=192)の N ⊴ B3, N<=PB3 全 66 個で一斉検査
##  V3  tau(x->y,y->z) が F2/N_F2 に降りるのは c in N の窓に限る(実測)
##  V4  **補正則**: [m,f] が GT-shadow  <=>  f*theta~(f) = 1  かつ
##        Rt(m,f) := tau~^2(y^m f) . tau~(y^m f) . (y^m f) = c^m   かつ 全射
##      (tau~ := Ad(delta), 評価は PB3/N の中。c^m が欠けているのが旧実装)
##      W-C-p5 と W-A-B3idx192-s4 の全候補で FULL hexagon (3.3)(3.4) と一致
##  V5  旧実装(語レベル)は述語 Rt = c^{m+e(w)} を検査している(e(w)=語の総指数和)
##      -> 同じ群元でも語を変えると判定が反転する(反例を明示)
##  V6  (3.53) は c-補正不要: 補正後の shadow 集合は 1600/1600 で閉じる
##  V7  GTSh(N5,N5) = C2 x Aff(F5)(位数 40・導来長 2・ker chi~ = C5)
##      GTSh(idx192-s4) = C4 x C2(位数 8・導来長 1・ker chi~ = 1・T-A 回復)
##
## 実行: .\gap.ps1 search\wcp5d-verify.g   (壁時計 ~15 s)
#############################################################################

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");
if LoadPackage("lins") <> true then Error("LINS load failed"); fi;
t0 := GAPLIB_WallElapsedMs();;
FAILS := 0;;
Chk := function(ok, label)
  if not ok then FAILS := FAILS + 1; fi;
  Print("[", PF(ok), "] ", label, "\n");
end;;

#############################################################################
## 共通: 与えられた marking (s1,s2) から窓データを組む
#############################################################################
MakeWindow := function(s1, s2)
  local xx, yy, DD, dd, cc, zz;
  xx := s1^2;  yy := s2^2;
  DD := AbstractProd([s1,s2,s1]);  dd := AbstractProd([s1,s2]);
  cc := DD^2;  zz := AbstractProd([xx,yy])^-1;
  return rec(s1:=s1, s2:=s2, x:=xx, y:=yy, Dlt:=DD, dlt:=dd, c:=cc, z:=zz,
             Bq:=Group(s1,s2), PN:=Group(xx,yy),
             Nord:=Lcm(Order(xx),Order(yy),Order(cc)));
end;;

# tau~ = Ad(delta), theta~ = Ad(Delta) -- N ⊴ B3 なので常に PB3/N を保つ
TT := function(W, g) return AbstractProd([W.dlt, g, W.dlt^-1]); end;;
TH := function(W, g) return AbstractProd([W.Dlt, g, W.Dlt^-1]); end;;
RtOf := function(W, m, f)
  local Wd;
  Wd := AbstractProd([W.y^m, f]);
  return AbstractProd([TT(W,TT(W,Wd)), TT(W,Wd), Wd]);
end;;

# FULL hexagon (3.3)(3.4) + 全射(= 定義そのもの)
FullShadows := function(W, charmingSet)
  local out, f, m, u;
  out := [];
  for f in Elements(DerivedSubgroup(W.PN)) do
    for m in charmingSet do
      u := 2*m+1;
      if AbstractProd([W.s1^u, f^-1, W.s2^u, f])
         <> AbstractProd([f^-1, W.s1, W.s2, W.x^(-m), W.c^m]) then continue; fi;
      if AbstractProd([f^-1, W.s2^u, f, W.s1^u])
         <> AbstractProd([W.s2, W.s1, W.y^(-m), W.c^m, f]) then continue; fi;
      if Size(Group(W.x^u, AbstractProd([f^-1, W.y^u, f]))) <> Size(W.PN) then continue; fi;
      Add(out, [m,f]);
    od;
  od;
  return Set(out);
end;;

# 補正済み簡約 hexagon(V4)
CorrectedShadows := function(W, charmingSet)
  local out, f, m, u;
  out := [];
  for f in Elements(DerivedSubgroup(W.PN)) do
    if AbstractProd([f, TH(W,f)]) <> Identity(W.Bq) then continue; fi;
    for m in charmingSet do
      u := 2*m+1;
      if RtOf(W,m,f) <> W.c^m then continue; fi;
      if Size(Group(W.x^u, AbstractProd([f^-1, W.y^u, f]))) <> Size(W.PN) then continue; fi;
      Add(out, [m,f]);
    od;
  od;
  return Set(out);
end;;

# (3.53) 閉性 + 群構造
GroupOfShadows := function(W, S)
  local n, tbl, i, j, m1, f1, u1, Eh, nm, nf, p, closed, regs, GT, H, prev, len, sizes;
  n := Length(S);  tbl := [];  closed := true;
  for i in [1..n] do
    m1 := S[i][1];  f1 := S[i][2];  u1 := 2*m1+1;
    Eh := GroupHomomorphismByImages(W.PN, W.PN, [W.x,W.y],
            [W.x^u1, AbstractProd([f1^-1, W.y^u1, f1])]);
    if Eh = fail then return rec(closed:=false, note:="E hom fail"); fi;
    tbl[i] := [];
    for j in [1..n] do
      nm := (2*m1*S[j][1] + m1 + S[j][1]) mod W.Nord;
      nf := AbstractProd([f1, Image(Eh, S[j][2])]);
      p := Position(S, [nm,nf]);
      if p = fail then closed := false; tbl[i][j] := 1; else tbl[i][j] := p; fi;
    od;
  od;
  if not closed then return rec(closed:=false); fi;
  regs := List([1..n], i -> PermList(tbl[i]));
  GT := Group(regs);
  H := GT;  len := 0;  sizes := [Size(GT)];
  while not IsTrivial(H) and len < 10 do
    prev := H;  H := DerivedSubgroup(H);  len := len+1;  Add(sizes, Size(H));
    if Size(H) = Size(prev) then len := -1; break; fi;
  od;
  return rec(closed:=true, G:=GT, order:=Size(GT), regs:=regs,
             derived_sizes:=sizes, derived_length:=len,
             ker:=Group(List(Filtered([1..n], i -> S[i][1]=0), i -> regs[i])));
end;;

#############################################################################
## V1/V2/V3 -- LINS 一斉検査
#############################################################################
Print("\n===== V1/V2/V3: LINS(index<=192) 全窓での theta/tau の正体 =====\n");
BF3 := FreeGroup("a","b");;
B3 := BF3 / [ BF3.1*BF3.2*BF3.1*(BF3.2*BF3.1*BF3.2)^-1 ];;
ga := B3.1;;  gb := B3.2;;
PB3 := Kernel(GroupHomomorphismByImages(B3, SymmetricGroup(3), [ga,gb], [(1,2),(2,3)]));;
gr := LowIndexNormalSubgroupsSearch(B3, 192);;
nTot := 0;; nV1 := 0;; nV2 := 0;; nCin := 0;; nTauDescCin := 0;; nTauDescCout := 0;; nCout := 0;;
for nd in ComputedNormalSubgroups(gr) do
  if Index(nd) = 1 then continue; fi;
  if not IsSubset(PB3, Grp(nd)) then continue; fi;
  hm := NaturalHomomorphismByNormalSubgroup(B3, Grp(nd));
  iso := IsomorphismPermGroup(Image(hm));
  W := MakeWindow(Image(iso, Image(hm, ga)), Image(iso, Image(hm, gb)));
  nTot := nTot + 1;
  if TH(W,W.x) = W.y and TH(W,W.y) = W.x then nV1 := nV1 + 1; fi;
  if TT(W,W.x) = W.y and TT(W,W.y) = AbstractProd([W.z, W.c]) then nV2 := nV2 + 1; fi;
  if W.c = Identity(W.Bq) then
    nCin := nCin + 1;
    if GroupHomomorphismByImages(W.PN,W.PN,[W.x,W.y],[W.y,W.z]) <> fail then
      nTauDescCin := nTauDescCin + 1; fi;
  else
    nCout := nCout + 1;
    if GroupHomomorphismByImages(W.PN,W.PN,[W.x,W.y],[W.y,W.z]) <> fail then
      nTauDescCout := nTauDescCout + 1; fi;
  fi;
od;
Print("  対象窓 = ", nTot, "  (c in N: ", nCin, " / c notin N: ", nCout, ")\n");
Chk(nV1 = nTot, Concatenation("V1 Ad(Delta): x->y, y->x  (", String(nV1), "/", String(nTot), ")"));
Chk(nV2 = nTot, Concatenation("V2 Ad(delta): x->y, y->z*c  (", String(nV2), "/", String(nTot), ")"));
Chk(nTauDescCin = nCin, Concatenation("V3a c in N の窓では tau が F2/N_F2 に降りる (",
    String(nTauDescCin), "/", String(nCin), ")"));
Print("  [obs] c notin N の窓で tau が降りるもの = ", nTauDescCout, "/", nCout,
      "  -> 降りない ", nCout - nTauDescCout, " 窓が語レベル経路の危険域\n");

#############################################################################
## V4/V5/V6/V7 -- 窓ごとの検分
#############################################################################
CheckWindow := function(label, W, expectMethodADiff)
  local ch, full, corr, gi, wlP, setP, bfs, ExpSum, badFs, f, w, w2, ok5, m, ymf, t1w, t2w, accW, accW2;
  Print("\n===== ", label, " =====\n");
  Print("  |B3/N|=", Size(W.Bq), " |PB3/N|=", Size(Group(W.x,W.y,W.c)), " |P_N|=", Size(W.PN),
        " ord(x)=", Order(W.x), " ord(y)=", Order(W.y), " ord(c)=", Order(W.c),
        " ord(s1)=", Order(W.s1), " N_ord=", W.Nord, "\n");
  ch := Filtered([0..W.Nord-1], mm -> Gcd(2*mm+1, W.Nord) = 1);
  full := FullShadows(W, ch);
  corr := CorrectedShadows(W, ch);
  Chk(full = corr, Concatenation("V4 補正則 [f.theta~(f)=1 & Rt=c^m] = FULL hexagon  (|FULL|=",
      String(Length(full)), ", |補正則|=", String(Length(corr)), ")"));
  wlP := EnumerateWordLevelHexagonPrepend(rec(x:=W.x, y:=W.y, c:=W.c, G:=W.PN), ch);
  setP := Set(List(wlP.shadows, s -> [s.m, s.f]));
  Print("  [obs] 旧実装(prepend 語レベル) shadow = ", Length(setP),
        "  FULL との差分 = ", Length(Filtered(setP, k -> not (k in full))), "\n");
  Chk((setP <> full) = expectMethodADiff, "V5a 旧実装は FULL と不一致(既知)");
  # V5b(普遍形): 旧実装が実際に検査している述語は Rt = c^{m + e(w)}(e = BFS 語の総指数和)
  bfs := BFSWords(rec(x:=W.x, y:=W.y, G:=W.PN));
  ExpSum := function(ww) return Sum(List(ww, l -> l[2])); end;
  ok5 := true;
  for f in Elements(DerivedSubgroup(W.PN)) do
    w := LookupDictionary(bfs.wordOf, f);
    for m in ch do
      if ( (AbstractProd([f, TH(W,f)]) = Identity(W.Bq))
           and (RtOf(W,m,f) = W.c^(m + ExpSum(w)))
           and (Size(Group(W.x^(2*m+1), AbstractProd([f^-1, W.y^(2*m+1), f]))) = Size(W.PN)) )
         <> ([m,f] in setP) then ok5 := false; fi;
    od;
  od;
  Chk(ok5, "V5b 旧実装の述語 = [Rt = c^{m+e(w)}](正則は Rt = c^m — ずれは c^{e(w)})");
  # V5c(該当窓のみ・観測): 同一 f・別語で判定が反転する具体例
  if setP <> full then
    badFs := Set(List(Filtered(setP, k -> not (k in full)), k -> k[2]));
    for f in badFs do
      w := LookupDictionary(bfs.wordOf, f);
      w2 := Concatenation(w, List([1..Order(W.x)], i -> ["x",1]));  # x^ord(x) in N_F2
      accW := [];  accW2 := [];
      for m in ch do
        ymf := Concatenation(List([1..m], i -> ["y",1]), w);
        t1w := TauWord(ymf);  t2w := TauWord(t1w);
        if EvalWordInQ(Concatenation(t2w,t1w,ymf), W.x, W.y, Identity(W.PN)) = Identity(W.PN)
          then Add(accW, m); fi;
        ymf := Concatenation(List([1..m], i -> ["y",1]), w2);
        t1w := TauWord(ymf);  t2w := TauWord(t1w);
        if EvalWordInQ(Concatenation(t2w,t1w,ymf), W.x, W.y, Identity(W.PN)) = Identity(W.PN)
          then Add(accW2, m); fi;
      od;
      Print("  [obs] f: 語 w (e=", ExpSum(w), " ; e mod ord(c)=", ExpSum(w) mod Order(W.c),
            ") -> (3.11) 合格 m = ", accW, " ;  同じ元の語 w.x^", Order(W.x), " (e=", ExpSum(w2),
            " ; mod ord(c)=", ExpSum(w2) mod Order(W.c), ") -> m = ", accW2,
            " ;  FULL = ", List(Filtered(full, k->k[2]=f), k->k[1]),
            "   [判定反転? ", accW <> accW2, "]\n");
    od;
  fi;
  gi := GroupOfShadows(W, full);
  Chk(gi.closed, "V6 (3.53) 閉性(補正後の shadow 集合)");
  if gi.closed then
    Print("  V7 |GTSh| = ", gi.order, "  StructureDescription = ", StructureDescription(gi.G),
          "  IdGroup = ", IdGroup(gi.G), "\n");
    Print("     導来列 = ", gi.derived_sizes, "  導来長 = ", gi.derived_length,
          "  metabelian? ", gi.derived_length >= 0 and gi.derived_length <= 2, "\n");
    Print("     |ker chi~| = ", Size(gi.ker), " 可換? ", IsAbelian(gi.ker),
          "  構造 = ", StructureDescription(gi.ker),
          "   T-A 予測 = ", gi.order, "/", Phi(2*W.Nord), " = ", gi.order/Phi(2*W.Nord),
          "  T-A 成立? ", Size(gi.ker) = gi.order/Phi(2*W.Nord), "\n");
  fi;
  return gi;
end;;

# ---- W-C-p5 : N5 = ker(B3 -> S3 x SL(2,F5)) ----
psi2 := IsomorphismPermGroup(Group([[1,1],[0,1]]*One(GF(2)), [[1,0],[1,1]]*One(GF(2))));;
psi5 := IsomorphismPermGroup(Group([[1,1],[0,1]]*One(GF(5)), [[1,0],[4,1]]*One(GF(5))));;
DP := DirectProduct(Image(psi2), Image(psi5));;
Wp5 := MakeWindow(
  Image(Embedding(DP,1), Image(psi2,[[1,1],[0,1]]*One(GF(2)))) *
    Image(Embedding(DP,2), Image(psi5,[[1,1],[0,1]]*One(GF(5)))),
  Image(Embedding(DP,1), Image(psi2,[[1,0],[1,1]]*One(GF(2)))) *
    Image(Embedding(DP,2), Image(psi5,[[1,0],[4,1]]*One(GF(5)))));;
gp5 := CheckWindow("W-C-p5  (N5 = ker(B3 -> S3 x SL(2,F5)))", Wp5, true);;
if gp5.closed then
  Aff5 := Group([ PermList(List([0..4], t -> ((t+1) mod 5)+1)),
                  PermList(List([0..4], t -> ((2*t) mod 5)+1)) ]);;
  Chk(IsomorphismGroups(gp5.G, DirectProduct(CyclicGroup(IsPermGroup,2), Aff5)) <> fail,
      "V7a GTSh(N5,N5) = C2 x Aff(F5)(監査予想)");
  # ---- witness: 生成元と関係の exact データ(f は SL(2,F5) の行列で書く)----
  Print("\n  -- witness: GTSh(N5,N5) の生成元(f は SL(2,F5) 行列)--\n");
  prj5 := Projection(DP, 2);;
  MatOf := function(f) return PreImagesRepresentative(psi5, Image(prj5, f)); end;;
  S5 := FullShadows(Wp5, Filtered([0..Wp5.Nord-1], mm -> Gcd(2*mm+1, Wp5.Nord) = 1));;
  kerSh := Filtered(S5, k -> k[1] = 0);;
  Print("     ker chi~ = { [0,f] } の 5 元の f:\n");
  for k in kerSh do
    Print("       ", MatOf(k[2]), "   ord(f)=", Order(k[2]), "\n");
  od;
  gens := SmallGeneratingSet(gp5.G);;
  Print("     GTSh の最小生成系 (", Length(gens), " 個) を shadow 座標で:\n");
  for g in gens do
    i := Position(gp5.regs, g);
    Print("       [m=", S5[i][1], ", u=", 2*S5[i][1]+1, ", f=", MatOf(S5[i][2]),
          "]  位数 ", Order(g), "\n");
  od;
  Print("     関係: |GTSh|=40, ker chi~ = C5 ⊴ GTSh, GTSh/ker = (Z/20)^x = C4 x C2,\n");
  Print("            導来部分群 = ker chi~ = C5 (導来列 40 -> 5 -> 1), Z(GTSh) の位数 = ",
        Size(Centre(gp5.G)), "\n");
fi;

# ---- W-A-B3idx192-s4 ----
serial := rec();;  target := fail;;
for nd in ComputedNormalSubgroups(gr) do
  if Index(nd) = 1 then continue; fi;
  if not IsSubset(PB3, Grp(nd)) then continue; fi;
  if Index(nd) < 84 or Index(nd) > 192 then continue; fi;
  if IsBound(serial.(String(Index(nd)))) then
    serial.(String(Index(nd))) := serial.(String(Index(nd)))+1;
  else serial.(String(Index(nd))) := 1; fi;
  if Index(nd) = 192 and serial.(String(Index(nd))) = 4 then target := Grp(nd); fi;
od;
if target = fail then Error("W-A-B3idx192-s4 not found"); fi;
hm := NaturalHomomorphismByNormalSubgroup(B3, target);;
iso := IsomorphismPermGroup(Image(hm));;
Ws4 := MakeWindow(Image(iso, Image(hm, ga)), Image(iso, Image(hm, gb)));;
gs4 := CheckWindow("W-A-B3idx192-s4", Ws4, true);;
if gs4.closed then
  Chk(Size(gs4.ker) = gs4.order/Phi(2*Ws4.Nord),
      "V7b idx192-s4 の T-A 個数等式は補正後に回復(採掘器の ker=2 は旧実装由来)");
fi;

Print("\n############################################################\n");
Print("# 総括: FAILS = ", FAILS, "\n");
Print("############################################################\n");
Print("経過(壁時計) = ", GAPLIB_WallElapsedMs()/1000.0, " s\n");
Print("\nWCP5D-VERIFY DONE\n");
QUIT;
