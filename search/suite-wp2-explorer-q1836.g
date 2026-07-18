# suite-wp2-explorer-q1836.g -- WP2a GAP explorer, K18 & K36 分割スクリプト
#
# 主スクリプト search/suite-wp2-explorer.g が n=3..16+N5 を完走した後、reduction branch
# suite の残り2対 (36,12),(18,3) の q 側 K18,K36 をここで構成する(単一スクリプト10分cap
# のため分割。K3,K12 は reduction 計算のためここで再計算する -- 主スクリプトの結果は
# GAPセッション間で永続しないため)。
#
# ヘルパー関数(MakeDn/MakeGn/AbstractProd/kappaFn/compOfFix/bPerm/DnElemToAE/
# BuildQTDihedral/EvalWordQT/JSON系/BFSWords/ProcessDihedral/Thm46Order/AffineDecode/
# ShadowToJsonDihedral/WriteFile/BuildCertJsonDihedral/ComputeReduction/ReductionToJson)
# は search/suite-wp2-explorer.g と全く同一の実装(コピー、helper非共有の対象は
# 探索器/照合器の分離であって、同一探索器内の関数複製はこの規律の対象外)。

SizeScreen([4096, 0]);;
startTime := Runtime();;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

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

AbstractProd := function(list)
  local val, i;
  val := list[1]^0;
  for i in [Length(list), Length(list)-1 .. 1] do
    val := val * list[i];
  od;
  return val;
end;;

kappaFn := function(m) if m mod 2 = 1 then return m+1; else return -m; fi; end;;

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
        charmPass := charmPass + 1;
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
        Add(compTable, [i1-1, i2-1, idx-1]);
      fi;
    od;
  od;

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

  lsWitness := [];
  if n mod 3 = 0 then
    for sh in shadows do
      m := sh.m;  f := sh.f;
      if not IsBound(sh.k) then continue; fi;
      k := sh.k;  kap := kappaFn(m);
      if kap mod 4 = 0 then
        gElt := AbstractProd([gn.x^(2*k), z^(kap/2)]);
      else
        gElt := AbstractProd([gn.y^(2*k+2), z^(kap/2)]);
      fi;
      eqn1 := AbstractProd([f^-1, Image(thetaHom,gElt)^-1, gElt]) = Identity(gn.G);
      if m mod 3 = 1 then
        Print("  [ANOMALY] n=",n," m=",m," has m==1 mod 3 among shadows -- should be vacuous per addendum!\n");
        continue;
      fi;
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

Thm46Order := function(n)
  local a, n0;
  n0 := n; a := 0;
  while n0 mod 2 = 0 do n0 := n0/2; a := a+1; od;
  if a < 2 then return 2*n0*Phi(n0); else return n0*Phi(n0)*2^(2*a-2); fi;
end;;

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
    "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/suite-wp2-explorer-q1836.g\",\"date\":\"2026-07-18\"},",
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

ComputeReduction := function(qres, nres, qn, nn)
  local hom, images, i, sh, mm, ff, idx, t, surjOK, seen;
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

# ================= メインドライバ: K18, K36 + reduction triangle =================
Print("宇宙 (branch suite: K18,K36 + K3,K4,K12 reconstruction; reduction triangle): 構成開始\n");

t0 := Runtime();
res3 := ProcessDihedral(3);
t1 := Runtime();
Print("[recompute] n=3  shadows=", Length(res3.shadows), " (expect 12)  time_ms=", t1-t0, "\n");

t0 := Runtime();
res4 := ProcessDihedral(4);
t1 := Runtime();
Print("[recompute] n=4  shadows=", Length(res4.shadows), " (expect 4)  time_ms=", t1-t0, "\n");

t0 := Runtime();
res12 := ProcessDihedral(12);
t1 := Runtime();
Print("[recompute] n=12  shadows=", Length(res12.shadows), " (expect 24)  time_ms=", t1-t0, "\n");

t0 := Runtime();
res18 := ProcessDihedral(18);
t1 := Runtime();
Print("n=18  shadows=", Length(res18.shadows), " (Thm4.6 formula expects ", Thm46Order(18), ")",
      "  dblFail=", res18.dblFail, " kernelCertFail=", res18.kernelCertFail,
      " ls_witness=", Length(res18.lsWitness), "  time_ms=", t1-t0, "\n");

t0 := Runtime();
res36 := ProcessDihedral(36);
t1 := Runtime();
Print("n=36  shadows=", Length(res36.shadows), " (Thm4.6 formula expects ", Thm46Order(36), ")",
      "  dblFail=", res36.dblFail, " kernelCertFail=", res36.kernelCertFail,
      " ls_witness=", Length(res36.lsWitness), "  time_ms=", t1-t0, "\n");

Print("\n累計 elapsed ms (n=3,12 recompute + 18 + 36): ", Runtime()-startTime, "\n");

red183 := ComputeReduction(res18, res3, 18, 3);
red3612 := ComputeReduction(res36, res12, 36, 12);
red364 := ComputeReduction(res36, res4, 36, 4);
Print("reduction (18->3): surjective=", red183.surjective, "\n");
Print("reduction (36->12): surjective=", red3612.surjective, "\n");
Print("reduction (36->4): surjective=", red364.surjective, "\n");

cert18 := BuildCertJsonDihedral(18, res18, ReductionToJson([red183]));
WriteFile("certificates/K18.v1.json", cert18);
Print("wrote certificates/K18.v1.json\n");

cert36 := BuildCertJsonDihedral(36, res36, ReductionToJson([red3612, red364]));
WriteFile("certificates/K36.v1.json", cert36);
Print("wrote certificates/K36.v1.json\n");

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");
QUIT;
