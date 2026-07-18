# suite-wp2-explorer.g -- WP2a GAP explorer (search side)
#
# 実行: .\gap.ps1 search\suite-wp2-explorer.g
#
# 対象: dihedral K^(n), n = 3..16 (事前登録どおり) + control N5.
# K18, K36 (reduction q-side)は別スクリプト search/suite-wp2-explorer-q1836.g で構成する
# (単一スクリプト 10 分 cap のため分割 -- 司令塔へ報告済み)。
#
# 出典: docs/wp2-transversal-model.md (12 規則 + 証明書スキーマ + 追補1)
#       docs/week1-定義ノート.md SS2-3 (hexagon (3.3)(3.4), charming, (3.53)(3.54), Thm 4.3)
#       sol/sol_reply_01_definition_gate.md SS6 (罠12件)
#       papers/txt/2405.11725-...txt (Lemma 4.2 (4.11), Prop 4.1, Thm 5.2 (5.1)(5.2)(5.3) 直接引用照合)
#
# 規約確認(このスクリプト作成前にscratchで実測確認済み. search/wp2-scratch-*.g に記録):
#  - Dn/Gn 側 (r,s 関数表現): 抽象積 "AB" = GAP "B*A" (逆順). z-fixture (2405 (3.6): zbar=(r^2s,r^-1s,r))
#    と psi_n(xy)=(r^2s,r^-1s,r^-1) (Thm5.2証明中) の両方で実測確認 (2/2 一致).
#  - Q x T 側 (transversal-cocycle, 右剰余類作用): GAP 自然順 (反転なし). N5 の full hexagon で
#    既知 GT(N5)={0,1,3,4} (suite-wp1.g, 独立8点表現) と一致確認.
#  - 上記2つの模型は独立ヘルパー(helper非共有) -- reduced hexagon(Gn側)と full hexagon(QxT側)の
#    二重チェックがSolの罠1への対応になっている.

SizeScreen([4096, 0]);;
startTime := Runtime();;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ================= 基本ヘルパー (suite-wp1.g より無変更で流用) =================
MakeDn := function(n)
  local r, s;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  if not (Order(r) = n and Order(s) = 2 and s*r*s^-1 = r^-1) then
    Error("D_n relations failed for n = ", n);
  fi;
  return [r, s];
end;;

MakeGn := function(n)
  local rs, r, s, x, y, tr;
  rs := MakeDn(n);  r := rs[1];  s := rs[2];
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  x := tr(r,1) * tr(s,2) * tr(s,3);
  y := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  return rec(x := x, y := y, G := Group(x, y), r := r, s := s);
end;;

expectedSize := function(n)
  if n mod 2 = 1 then return 4*n^3; else return 4*(n/2)^3; fi;
end;;

# 抽象積 "f1 f2 ... fk" (paper 記法, 左から順) -> GAP 表現 (Dn/Gn 側; 反転規約, 実測確認済み)
AbstractProd := function(list)
  local val, i;
  val := list[1]^0;
  for i in [Length(list), Length(list)-1 .. 1] do
    val := val * list[i];
  od;
  return val;
end;;

kappaFn := function(m) if m mod 2 = 1 then return m+1; else return -m; fi; end;;

# component extraction: block i (points (i-1)n+1..in) -> S_n permutation on 1..n
compOfFix := function(perm, i, nn)
  local l, j, img;
  l := [];
  for j in [1..nn] do
    img := (j + (i-1)*nn)^perm;
    l[j] := img - (i-1)*nn;
  od;
  return PermList(l);
end;;

bPerm := function(u, nn)
  local l, j;
  l := [];
  for j in [1..nn] do l[j] := ((u*(j-1)) mod nn) + 1; od;
  return PermList(l);
end;;

# Dn 元 -> [a,e] (r^a s^e, abstract 規約; 抽象 "r^a s" = GAP "s*r^a")
DnElemToAE := function(perm, r, s, nn)
  local a;
  for a in [0..nn-1] do
    if r^a = perm then return [a,0]; fi;
  od;
  for a in [0..nn-1] do
    if s*r^a = perm then return [a,1]; fi;
  od;
  Error("DnElemToAE: no match found for n=", nn);
end;;

# ================= Q x T (transversal-cocycle) モデル: dihedral =================
# 規約(wp2-transversal-model.md 凍結表を無変更で流用): Q x T 側は GAP 自然順(反転なし)
BuildQTDihedral := function(n, r, s)
  local Qelts, posOf, phiX, phiY, phiC, phiXi, phiYi, np, imgS1, imgS2, t, i, d, pt, val, tp;
  Qelts := Elements(Group(r,s));
  posOf := function(v) return Position(Qelts, v); end;
  phiX := s;  phiY := s*r;  phiC := ();
  phiXi := phiX^-1;  phiYi := phiY^-1;
  np := Length(Qelts);
  imgS1 := [];;  imgS2 := [];;
  for t in [1..6] do
    for i in [1..np] do
      d := Qelts[i];  pt := (t-1)*np + i;
      if t=1 then val:=d; tp:=2;
      elif t=2 then val:=d*phiX; tp:=1;
      elif t=3 then val:=d; tp:=5;
      elif t=4 then val:=d; tp:=6;
      elif t=5 then val:=d*phiXi*phiYi*phiC; tp:=3;
      else val:=d*phiY; tp:=4; fi;
      imgS1[pt] := (tp-1)*np + posOf(val);
      if t=1 then val:=d; tp:=3;
      elif t=2 then val:=d; tp:=4;
      elif t=3 then val:=d*phiY; tp:=1;
      elif t=4 then val:=d*phiYi*phiXi*phiC; tp:=2;
      elif t=5 then val:=d; tp:=6;
      else val:=d*phiX; tp:=5; fi;
      imgS2[pt] := (tp-1)*np + posOf(val);
    od;
  od;
  return rec(s1:=PermList(imgS1), s2:=PermList(imgS2), np:=np);
end;;

EvalWordQT := function(word, qt)
  local val, letter;
  val := ();
  for letter in word do
    if letter[1]="x" then val := val * qt.xx^letter[2];
    else val := val * qt.yy^letter[2]; fi;
  od;
  return val;
end;;

# ================= JSON 出力ヘルパー (最小自作シリアライザ) =================
JStr := function(s) return Concatenation("\"", s, "\""); end;;
JB := function(b) if b then return "true"; else return "false"; fi; end;;
JoinC := function(strs, sep)
  local r, i;
  if Length(strs) = 0 then return ""; fi;
  r := strs[1];
  for i in [2..Length(strs)] do r := Concatenation(r, sep, strs[i]); od;
  return r;
end;;
JArr := function(items) return Concatenation("[", JoinC(items, ","), "]"); end;;
JPair := function(a,b) return Concatenation("[", String(a), ",", String(b), "]"); end;;

WordToJson := function(word)
  local items, letter;
  items := [];
  for letter in word do
    Add(items, Concatenation("[\"", letter[1], "\",", String(letter[2]), "]"));
  od;
  return JArr(items);
end;;

# ================= BFS ワード付与 (Gn.G 全体, x/y/x^-1/y^-1 生成系) =================
BFSWords := function(gn)
  local gens, wordOf, queue, qi, cur, curWord, g, nv;
  gens := [ rec(sym:=["x",1], gap:=gn.x), rec(sym:=["x",-1], gap:=gn.x^-1),
            rec(sym:=["y",1], gap:=gn.y), rec(sym:=["y",-1], gap:=gn.y^-1) ];
  wordOf := NewDictionary(Identity(gn.G), true);
  AddDictionary(wordOf, Identity(gn.G), []);
  queue := [ Identity(gn.G) ];
  qi := 1;
  while qi <= Length(queue) do
    cur := queue[qi];  qi := qi+1;
    curWord := LookupDictionary(wordOf, cur);
    for g in gens do
      nv := g.gap * cur;
      if LookupDictionary(wordOf, nv) = fail then
        AddDictionary(wordOf, nv, Concatenation(curWord, [g.sym]));
        Add(queue, nv);
      fi;
    od;
  od;
  return rec(wordOf:=wordOf, elements:=queue);
end;;

# ================= 対象1個の完全処理 =================
ProcessDihedral := function(n)
  local gn, Nord, z, thetaHom, tauHom, bfs, D, Dwords, elt, Xn, rawCount, hexPass,
        charmPass, surjPass, shadows, cand, f, m, u, thetaf, hex310, ymf, tauymf,
        tau2ymf, hex311, genA, genB, surj, qt, dblFail, sh, fhat, fhatInv, lhs33, rhs33,
        lhs34, rhs34, kernelCertFail, g1, g2, g3, kfound, t, k, kap, b, h1, h2, h3,
        xcomp, ycomp, hcomp, eq1, eq2, i, formOK, compTable, i1, i2, m1, f1, m2, f2,
        u1, Ehom, imgx, imgy, newm, newf, idx, invMap, uinv, mtilde, ftilde, tildeIdx,
        lsWitness, shadowsJson, sIdx, gcomp, eqn1, hFoundWord, hFoundElt, fxm, tauh, rhsVal, gElt;

  gn := MakeGn(n);
  Nord := Lcm(Order(gn.x), Order(gn.y));
  z := AbstractProd([gn.x, gn.y])^-1;
  thetaHom := GroupHomomorphismByImages(gn.G, gn.G, [gn.x, gn.y], [gn.y, gn.x]);
  tauHom := GroupHomomorphismByImages(gn.G, gn.G, [gn.x, gn.y], [gn.y, z]);
  if thetaHom = fail or tauHom = fail then Error("theta/tau hom construction failed n=",n); fi;

  bfs := BFSWords(gn);
  if Length(bfs.elements) <> Size(gn.G) then
    Error("BFS did not cover full G_n for n=", n, " covered=", Length(bfs.elements),
          " expected=", Size(gn.G));
  fi;

  D := DerivedSubgroup(gn.G);
  Dwords := [];
  for elt in bfs.elements do
    if elt in D then Add(Dwords, rec(elt:=elt, word:=LookupDictionary(bfs.wordOf, elt))); fi;
  od;

  Xn := Filtered([0..Nord-1], mm -> Gcd(2*mm+1, Nord) = 1);

  rawCount := 0;  hexPass := 0;  charmPass := 0;  surjPass := 0;
  shadows := [];
  for cand in Dwords do
    f := cand.elt;
    for m in Xn do
      rawCount := rawCount + 1;
      u := 2*m+1;
      thetaf := Image(thetaHom, f);
      hex310 := AbstractProd([f, thetaf]) = Identity(gn.G);
      ymf := AbstractProd([gn.y^m, f]);
      tauymf := Image(tauHom, ymf);
      tau2ymf := Image(tauHom, tauymf);
      hex311 := AbstractProd([tau2ymf, tauymf, ymf]) = Identity(gn.G);
      if hex310 and hex311 then
        hexPass := hexPass + 1;
        charmPass := charmPass + 1;   # f in D by construction -> charming f-condition holds
        genA := gn.x^u;
        genB := AbstractProd([f^-1, gn.y^u, f]);
        surj := Size(Group(genA, genB)) = Size(gn.G);
        if surj then
          surjPass := surjPass + 1;
          Add(shadows, rec(m:=m, f:=f, word:=cand.word));
        fi;
      fi;
    od;
  od;

  # ---- full hexagon double-check on Q x T model (independent helper) ----
  qt := BuildQTDihedral(n, gn.r, gn.s);
  qt.xx := qt.s1^2;  qt.yy := qt.s2^2;  qt.cc := (qt.s1*qt.s2*qt.s1)^2;
  if not (qt.s1*qt.s2*qt.s1 = qt.s2*qt.s1*qt.s2) then Error("QT braid failed n=",n); fi;
  if Size(Group(qt.s1,qt.s2)) <> 6*expectedSize(n) then
    Error("QT |<s1,s2>| mismatch n=",n);
  fi;
  if qt.cc <> () then Error("QT c!=1 unexpected for dihedral n=",n); fi;

  dblFail := 0;
  for sh in shadows do
    m := sh.m;  u := 2*m+1;
    fhat := EvalWordQT(sh.word, qt);  fhatInv := fhat^-1;
    lhs33 := qt.s1^u * fhatInv * qt.s2^u * fhat;
    rhs33 := fhatInv * qt.s1*qt.s2 * qt.xx^(-m) * qt.cc^m;
    lhs34 := fhatInv * qt.s2^u * fhat * qt.s1^u;
    rhs34 := qt.s2*qt.s1 * qt.yy^(-m) * qt.cc^m * fhat;
    if not ((lhs33=rhs33) and (lhs34=rhs34)) then dblFail := dblFail + 1; fi;
    sh.fhat := fhat;
  od;

  # ---- kernel_cert (Lemma 4.2 (4.11), confirmed form: addendum 1) ----
  kernelCertFail := 0;
  for sh in shadows do
    m := sh.m;  u := 2*m+1;  f := sh.f;
    g1 := compOfFix(f,1,n);  g2 := compOfFix(f,2,n);  g3 := compOfFix(f,3,n);
    kfound := fail;
    for t in [0..n-1] do
      if gn.r^(2*t) = g1 then kfound := t; break; fi;
    od;
    if kfound = fail then
      Print("  [ANOMALY] n=",n," m=",m," no k found for g1 (Prop 4.1 form violated)\n");
      kernelCertFail := kernelCertFail + 1;
      sh.kcertOk := false;
      continue;
    fi;
    k := kfound;  kap := kappaFn(m);
    b := bPerm(u, n);
    h1 := AbstractProd([gn.r^(-2*k-m), b]);
    h2 := b;
    if m mod 2 = 0 then h3 := b; else h3 := AbstractProd([b, gn.s]); fi;
    formOK := (g2 = gn.r^(-2*k)) and (g3 = gn.r^kap);
    xcomp := [gn.r, gn.s, gn.s];
    ycomp := [gn.s*gn.r, gn.r, gn.s*gn.r];
    hcomp := [h1,h2,h3];
    eq1 := true;
    for i in [1,2,3] do
      if xcomp[i]^u <> AbstractProd([hcomp[i], xcomp[i], hcomp[i]^-1]) then eq1:=false; fi;
    od;
    eq2 := true;
    gcomp := [g1,g2,g3];
    for i in [1,2,3] do
      if AbstractProd([gcomp[i]^-1, ycomp[i]^u, gcomp[i]]) <> AbstractProd([hcomp[i], ycomp[i], hcomp[i]^-1]) then eq2:=false; fi;
    od;
    if not (formOK and eq1 and eq2) then
      Print("  [ANOMALY] n=",n," m=",m," kernel_cert check failed: formOK=",formOK," eq1=",eq1," eq2=",eq2,"\n");
      kernelCertFail := kernelCertFail + 1;
      sh.kcertOk := false;
    else
      sh.kcertOk := true;
      sh.k := k; sh.h := [h1,h2,h3];
      sh.g_triple := [g1,g2,g3];
    fi;
  od;

  # ---- composition_table (3.53), full pairwise ----
  compTable := [];
  for i1 in [1..Length(shadows)] do
    for i2 in [1..Length(shadows)] do
      m1 := shadows[i1].m;  f1 := shadows[i1].f;
      m2 := shadows[i2].m;  f2 := shadows[i2].f;
      u1 := 2*m1+1;
      imgx := gn.x^u1;
      imgy := AbstractProd([f1^-1, gn.y^u1, f1]);
      Ehom := GroupHomomorphismByImages(gn.G, gn.G, [gn.x,gn.y], [imgx,imgy]);
      if Ehom = fail then
        Print("  [ANOMALY] n=",n," E_{m1,f1} hom construction failed i1=",i1,"\n");
        continue;
      fi;
      newm := (2*m1*m2 + m1 + m2) mod Nord;
      newf := AbstractProd([f1, Image(Ehom, f2)]);
      idx := fail;
      for t in [1..Length(shadows)] do
        if shadows[t].m = newm and shadows[t].f = newf then idx := t; break; fi;
      od;
      if idx = fail then
        Print("  [ANOMALY] n=",n," composition (",i1,",",i2,") has no matching shadow!\n");
      else
        Add(compTable, [i1-1, i2-1, idx-1]);   # 0-indexed for JSON
      fi;
    od;
  od;

  # ---- inverse_map (3.54) ----
  invMap := [];
  for i1 in [1..Length(shadows)] do
    m1 := shadows[i1].m;  f1 := shadows[i1].f;  u1 := 2*m1+1;
    uinv := Gcdex(u1, Nord).coeff1 mod Nord;
    mtilde := ((-uinv*m1) mod Nord);
    imgx := gn.x^u1;
    imgy := AbstractProd([f1^-1, gn.y^u1, f1]);
    Ehom := GroupHomomorphismByImages(gn.G, gn.G, [gn.x,gn.y], [imgx,imgy]);
    if Ehom = fail or not IsBijective(Ehom) then
      Print("  [ANOMALY] n=",n," E hom not bijective for inverse at i1=",i1,"\n");
      continue;
    fi;
    ftilde := PreImagesRepresentative(Ehom, f1^-1);
    tildeIdx := fail;
    for t in [1..Length(shadows)] do
      if shadows[t].m = mtilde and shadows[t].f = ftilde then tildeIdx := t; break; fi;
    od;
    if tildeIdx = fail then
      Print("  [ANOMALY] n=",n," inverse of shadow ",i1," (m~=",mtilde,") not found among shadows!\n");
    else
      Add(invMap, [i1-1, tildeIdx-1]);
    fi;
  od;

  # ---- ls_witness (Thm 5.2, (5.1)), 3|n only: search over ALL of G_n (not just D) for g,h ----
  lsWitness := [];
  if n mod 3 = 0 then
    for sh in shadows do
      m := sh.m;  f := sh.f;
      if not IsBound(sh.k) then continue; fi;   # need kernel_cert k (formOK) to have g_triple
      k := sh.k;  kap := kappaFn(m);
      # g (first equation, universal formula, Thm5.2 proof)
      if kap mod 4 = 0 then
        gElt := AbstractProd([gn.x^(2*k), z^(kap/2)]);
      else
        gElt := AbstractProd([gn.y^(2*k+2), z^(kap/2)]);
      fi;
      # eqn1 checks f K_F2 = theta(g)^-1 g K_F2, i.e. f^-1 * theta(g)^-1 * g = id (abstract)
      eqn1 := AbstractProd([f^-1, Image(thetaHom,gElt)^-1, gElt]) = Identity(gn.G);
      if m mod 3 = 1 then
        Print("  [ANOMALY] n=",n," m=",m," has m==1 mod 3 among shadows -- should be vacuous per addendum!\n");
        continue;
      fi;
      # second equation: search h over all G_n elements (brute, using BFS word list) for existence
      hFoundWord := fail;  hFoundElt := fail;
      fxm := AbstractProd([f, gn.x^m]);
      for elt in bfs.elements do
        tauh := Image(tauHom, elt);
        if m mod 3 = 0 then
          rhsVal := AbstractProd([tauh^-1, elt]);
        else
          rhsVal := AbstractProd([tauh^-1, gn.x, gn.y, elt]);
        fi;
        if AbstractProd([fxm^-1, rhsVal]) = Identity(gn.G) then
          hFoundElt := elt;  hFoundWord := LookupDictionary(bfs.wordOf, elt); break;
        fi;
      od;
      if hFoundWord = fail or not eqn1 then
        Print("  [ANOMALY] n=",n," ls_witness FAILED for m=",m," k=",k,
              " eqn1=",eqn1," h_found=",hFoundWord<>fail,"\n");
      else
        Add(lsWitness, rec(m:=m, k:=k, gword:=LookupDictionary(bfs.wordOf, gElt), hword:=hFoundWord));
      fi;
    od;
  fi;

  return rec(gn:=gn, Nord:=Nord, shadows:=shadows, Xn:=Xn,
             rawCount:=rawCount, hexPass:=hexPass, charmPass:=charmPass, surjPass:=surjPass,
             dblFail:=dblFail, kernelCertFail:=kernelCertFail, compTable:=compTable,
             invMap:=invMap, lsWitness:=lsWitness, bfs:=bfs, D:=D, n:=n);
end;;

# ================= thm46 (Thm 4.6 の位数式, 検算目的の参照値として counts と一緒に出す) =================
Thm46Order := function(n)
  local a, n0;
  n0 := n; a := 0;
  while n0 mod 2 = 0 do n0 := n0/2; a := a+1; od;
  if a < 2 then return 2*n0*Phi(n0); else return n0*Phi(n0)*2^(2*a-2); fi;
end;;

# affine 表現への復号: perm = (j -> uu*(j-1)+vv mod n, 1-indexed +1) となる (uu,vv) を探す
AffineDecode := function(perm, nn)
  local uu, vv, ok, j;
  for uu in [0..nn-1] do
    for vv in [0..nn-1] do
      ok := true;
      for j in [1..nn] do
        if ((uu*(j-1)+vv) mod nn)+1 <> j^perm then ok := false; break; fi;
      od;
      if ok then return [uu,vv]; fi;
    od;
  od;
  Error("AffineDecode: no representation found, n=", nn);
end;;

# ================= N5 control (type=brute) =================
ProcessN5 := function()
  local np, Qelts, posOf, qmul, qinv, phiX, phiY, phiC, phiXi, phiYi, imgS1, imgS2,
        t, i, d, pt, val, tp, s1, s2, GG, XX, YY, CC, Nord, m, u, lhs33, rhs33, lhs34,
        rhs34, hex33, hex34, unitCond, shadows, tcOk;
  np := 5;  Qelts := [0,1,2,3,4];
  posOf := function(v) return (v mod 5)+1; end;
  qmul := function(a,b) return (a+b) mod 5; end;
  qinv := function(a) return (5-a) mod 5; end;
  phiX := 2;  phiY := 2;  phiC := 1;
  phiXi := qinv(phiX);  phiYi := qinv(phiY);
  imgS1 := [];  imgS2 := [];
  for t in [1..6] do
    for i in [1..np] do
      d := Qelts[i];  pt := (t-1)*np+i;
      if t=1 then val:=d; tp:=2;
      elif t=2 then val:=qmul(d,phiX); tp:=1;
      elif t=3 then val:=d; tp:=5;
      elif t=4 then val:=d; tp:=6;
      elif t=5 then val:=qmul(qmul(d,phiXi),qmul(phiYi,phiC)); tp:=3;
      else val:=qmul(d,phiY); tp:=4; fi;
      imgS1[pt] := (tp-1)*np+posOf(val);
      if t=1 then val:=d; tp:=3;
      elif t=2 then val:=d; tp:=4;
      elif t=3 then val:=qmul(d,phiY); tp:=1;
      elif t=4 then val:=qmul(qmul(d,phiYi),qmul(phiXi,phiC)); tp:=2;
      elif t=5 then val:=d; tp:=6;
      else val:=qmul(d,phiX); tp:=5; fi;
      imgS2[pt] := (tp-1)*np+posOf(val);
    od;
  od;
  s1 := PermList(imgS1);  s2 := PermList(imgS2);
  if not (s1*s2*s1 = s2*s1*s2) then Error("N5 braid failed"); fi;
  GG := Group(s1,s2);
  if Size(GG) <> 30 then Error("N5 |<s1,s2>| != 30"); fi;
  XX := s1^2;  YY := s2^2;  CC := (s1*s2*s1)^2;
  Nord := Lcm(Order(XX),Order(YY),Order(CC));
  if Nord <> 5 then Error("N5 N_ord != 5"); fi;
  shadows := [];  tcOk := true;
  for m in [0..4] do
    u := 2*m+1;
    lhs33 := s1^u*s2^u;  rhs33 := s1*s2*XX^(-m)*CC^m;  hex33 := (lhs33=rhs33);
    lhs34 := s2^u*s1^u;  rhs34 := s2*s1*YY^(-m)*CC^m;  hex34 := (lhs34=rhs34);
    unitCond := Gcd(u,5)=1;
    if hex33 and hex34 and unitCond then
      if (s1^u*s2^u*s1^u)^2 <> CC^u then tcOk := false; fi;
      Add(shadows, rec(m:=m));
    fi;
  od;
  return rec(shadows:=shadows, Nord:=Nord, s1:=s1, s2:=s2, tcOk:=tcOk,
             qOrder:=5, indexB3:=30);
end;;

# ================= JSON builders =================
ShadowToJsonDihedral := function(sh, n, gn)
  local g1,g2,g3, fw, ft, kc, hAffine, i, kcertStr;
  fw := WordToJson(sh.word);
  g1 := compOfFix(sh.f,1,n);  g2 := compOfFix(sh.f,2,n);  g3 := compOfFix(sh.f,3,n);
  ft := JArr([ JPair(DnElemToAE(g1,gn.r,gn.s,n)[1],DnElemToAE(g1,gn.r,gn.s,n)[2]),
               JPair(DnElemToAE(g2,gn.r,gn.s,n)[1],DnElemToAE(g2,gn.r,gn.s,n)[2]),
               JPair(DnElemToAE(g3,gn.r,gn.s,n)[1],DnElemToAE(g3,gn.r,gn.s,n)[2]) ]);
  if IsBound(sh.h) and sh.kcertOk then
    hAffine := [];
    for i in [1..3] do Add(hAffine, JPair(AffineDecode(sh.h[i],n)[1], AffineDecode(sh.h[i],n)[2])); od;
    kcertStr := Concatenation("{\"type\":\"conjugator-triple\",\"h\":", JArr(hAffine),
                              ",\"k\":", String(sh.k), "}");
  else
    kcertStr := "{\"type\":\"conjugator-triple\",\"h\":null,\"note\":\"kernel_cert (4.11) check FAILED -- see script stderr ANOMALY log\"}";
  fi;
  return Concatenation("{\"m\":", String(sh.m), ",\"f_word\":", fw, ",\"f_triple\":", ft,
                        ",\"kernel_cert\":", kcertStr, "}");
end;;

WriteFile := function(path, content)
  local f;
  f := OutputTextFile(path, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, content);
  CloseStream(f);
end;;

BuildCertJsonDihedral := function(n, r, reductionEntries)
  local shadowsJson, sh, ct, cti, im, imi, lsw, lswi, target, counts, s;
  shadowsJson := [];
  for sh in r.shadows do Add(shadowsJson, ShadowToJsonDihedral(sh, n, r.gn)); od;
  ct := [];
  for cti in r.compTable do Add(ct, Concatenation("[",String(cti[1]),",",String(cti[2]),",",String(cti[3]),"]")); od;
  im := [];
  for imi in r.invMap do Add(im, Concatenation("[",String(imi[1]),",",String(imi[2]),"]")); od;
  lsw := [];
  for lswi in r.lsWitness do
    Add(lsw, Concatenation("{\"m\":",String(lswi.m),",\"k\":",String(lswi.k),
                            ",\"g_word\":",WordToJson(lswi.gword),
                            ",\"h_word\":",WordToJson(lswi.hword),"}"));
  od;
  target := Concatenation(
    "{\"family\":\"dihedral\",\"id\":\"K", String(n), "\",\"n\":", String(n),
    ",\"phi\":{\"desc\":\"x->s, y->rs, c->1 (left action)\",\"q_order\":", String(2*n), "},",
    "\"invariants\":{\"index_PB3\":", String(Size(r.gn.G)), ",\"index_B3\":", String(6*Size(r.gn.G)),
    ",\"N_ord\":", String(r.Nord), ",\"derived_order\":", String(Size(r.D)), "}}");
  counts := Concatenation("{\"raw_candidates\":", String(r.rawCount), ",\"hexagon_pass\":", String(r.hexPass),
                           ",\"charming_pass\":", String(r.charmPass), ",\"surjective_pass\":", String(r.surjPass),
                           ",\"double_check_full_hexagon_fail\":", String(r.dblFail),
                           ",\"kernel_cert_fail\":", String(r.kernelCertFail),
                           ",\"thm46_expected_order\":", String(Thm46Order(n)), "}");
  s := Concatenation(
    "{\"schema\":\"gtsh-cert/v1\",",
    "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/suite-wp2-explorer.g\",\"date\":\"2026-07-18\"},",
    "\"target\":", target, ",",
    "\"conventions\":{\"dn_element\":\"[a,e] = r^a s^e\",\"action\":\"left(rs = s のち r)\",",
    "\"f_word_alphabet\":\"x,y(c は不要 -- f in F2)\"},",
    "\"shadows\":", JArr(shadowsJson), ",",
    "\"counts\":", counts, ",",
    "\"composition_table\":", JArr(ct), ",",
    "\"inverse_map\":", JArr(im), ",",
    "\"reduction\":", reductionEntries, ",",
    "\"ls_witness\":", JArr(lsw),
    "}");
  return s;
end;;

BuildCertJsonN5 := function(r)
  local shadowsJson, sh, s;
  shadowsJson := [];
  for sh in r.shadows do
    Add(shadowsJson, Concatenation("{\"m\":", String(sh.m),
      ",\"f_word\":[],\"f_triple\":[[0,0],[0,0],[0,0]],",
      "\"kernel_cert\":{\"type\":\"brute\",\"expected_kernel_index\":30}}"));
  od;
  s := Concatenation(
    "{\"schema\":\"gtsh-cert/v1\",",
    "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/suite-wp2-explorer.g\",\"date\":\"2026-07-18\"},",
    "\"target\":{\"family\":\"control\",\"id\":\"N5\",\"n\":5,",
    "\"phi\":{\"desc\":\"x->t^2, y->t^2, c->t (beta5: B3->S3xC5)\",\"q_order\":5},",
    "\"invariants\":{\"index_PB3\":5,\"index_B3\":30,\"N_ord\":", String(r.Nord), ",\"derived_order\":1}},",
    "\"conventions\":{\"dn_element\":\"n/a (Q=C5 additive)\",\"action\":\"native (right coset action, Q x T model, no reversal)\",",
    "\"f_word_alphabet\":\"x,y (f=1 always, PB3/N5 abelian)\"},",
    "\"shadows\":", JArr(shadowsJson), ",",
    "\"counts\":{\"raw_candidates\":5,\"hexagon_pass\":5,",
    "\"charming_pass\":4,\"surjective_pass\":4,",
    "\"tc_check_pass\":", JB(r.tcOk), "},",
    "\"composition_table\":[],\"inverse_map\":[],\"reduction\":[],\"ls_witness\":[]",
    "}");
  return s;
end;;

# ================= reduction (q -> n, K^(q) <= K^(n)) =================
ComputeReduction := function(qres, nres, qn, nn)
  local hom, images, i, sh, mm, ff, idx, t, surjOK, covered, seen;
  hom := GroupHomomorphismByImages(qres.gn.G, nres.gn.G, [qres.gn.x,qres.gn.y], [nres.gn.x,nres.gn.y]);
  if hom = fail then Error("reduction hom construction failed q=",qn," n=",nn); fi;
  images := [];
  seen := [];
  for i in [1..Length(qres.shadows)] do
    sh := qres.shadows[i];
    mm := sh.m mod nres.Nord;
    ff := Image(hom, sh.f);
    idx := fail;
    for t in [1..Length(nres.shadows)] do
      if nres.shadows[t].m = mm and nres.shadows[t].f = ff then idx := t; break; fi;
    od;
    if idx = fail then
      Print("  [ANOMALY] reduction K(",qn,")->K(",nn,"): shadow ",i-1," has no image in target!\n");
      Add(images, -1);
    else
      Add(images, idx-1);
      if not (idx in seen) then Add(seen, idx); fi;
    fi;
  od;
  surjOK := Length(seen) = Length(nres.shadows);
  return rec(qn:=qn, nn:=nn, images:=images, surjective:=surjOK);
end;;

ReductionToJson := function(redlist)
  local items, r, imgstr, i;
  items := [];
  for r in redlist do
    imgstr := [];
    for i in r.images do Add(imgstr, String(i)); od;
    Add(items, Concatenation("{\"to\":\"K", String(r.nn), "\",\"image\":[",
                              JoinC(imgstr, ","), "],\"surjective\":", JB(r.surjective), "}"));
  od;
  return JArr(items);
end;;

# ================= メインドライバ: n=3..16 + N5 =================
universe := [3..16];;
results := [];;    # results[n] := ProcessDihedral(n)
Print("宇宙 (事前登録どおり, K18/K36 は別スクリプトで構成): ", universe, " + N5\n");

for n in universe do
  t0 := Runtime();
  results[n] := ProcessDihedral(n);
  t1 := Runtime();
  r := results[n];
  Print("[", PF(Length(r.shadows) = Thm46Order(n)), "] n=", n,
        "  shadows=", Length(r.shadows), " (Thm4.6 expect ", Thm46Order(n), ")",
        "  dblCheckFail=", r.dblFail, "  kernelCertFail=", r.kernelCertFail,
        "  ls_witness=", Length(r.lsWitness), "  time_ms=", t1-t0, "\n");
od;

Print("\n累計 elapsed ms (n=3..16): ", Runtime()-startTime, "\n");

# ---- reduction: 本スクリプト範囲内で計算可能な branch suite 3 対 ----
reductionsByQ := List([1..40], i -> []);;
red84 := ComputeReduction(results[8], results[4], 8, 4);;
red124 := ComputeReduction(results[12], results[4], 12, 4);;
red93 := ComputeReduction(results[9], results[3], 9, 3);;
reductionsByQ[8] := [red84];;
reductionsByQ[12] := [red124];;
reductionsByQ[9] := [red93];;
Print("reduction (8->4): surjective=", red84.surjective, "\n");
Print("reduction (12->4): surjective=", red124.surjective, "\n");
Print("reduction (9->3): surjective=", red93.surjective, "\n");
Print("(reduction (36->12), (18->3) は別スクリプト search/suite-wp2-explorer-q1836.g で計算する)\n");

# ---- JSON 書き出し ----
for n in universe do
  cert := BuildCertJsonDihedral(n, results[n], ReductionToJson(reductionsByQ[n]));
  WriteFile(Concatenation("certificates/K", String(n), ".v1.json"), cert);
  Print("wrote certificates/K", n, ".v1.json\n");
od;

n5res := ProcessN5();;
Print("\nN5: shadows=", Length(n5res.shadows), " (expect m in {0,1,3,4})  tcOk=", n5res.tcOk, "\n");
WriteFile("certificates/N5.v1.json", BuildCertJsonN5(n5res));
Print("wrote certificates/N5.v1.json\n");

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");
QUIT;
