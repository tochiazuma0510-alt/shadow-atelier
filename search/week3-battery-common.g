# week3-battery-common.g -- shared helpers for search/week3-battery-{1a,1b,2a,2b}.g
#
# Read via: Read("search/week3-battery-common.g");  (called from each stage script,
# cwd = repo root because gap.ps1 invokes gap.exe from the shell's working directory).
#
# Design source (spec projection only, per commander workorder 1):
#   search/manifest_spec_v1.md (the only normative spec)
#   docs/wp2-transversal-model.md (12-rule Q x T model)
#   docs/week1-定義ノート.md SS1-2 (hexagon, reduced hexagon, charming)
#   search/week3-L-explorer.g, search/week3-M5-explorer.g (implementation patterns --
#     MakeDn/MakeGn/AbstractProd/compOfFix/DnElemToAE/BFSWords/EvalWordQT/BuildQTGeneral/
#     JSON helpers copied near-verbatim and generalized where the manifest needs it)
#
# All four stages in this workorder (1a/1b/2a/2b) have c_in_N = true (manifest spec S2. (4)
# for each stage), so the quotient-shortcut theta/tau (GroupHomomorphismByImages) is valid
# throughout (the M5 word-level trap does NOT apply here -- that is specific to c surviving,
# which only happens at stage A2 in this 7-stage plan, out of scope for this workorder).

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ================= D_n / G_n (dihedral tower helpers, copied verbatim) =================
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

# abstract product "f1 f2 ... fk" (paper notation, left to right) -> GAP form (reversal convention)
AbstractProd := function(list)
  local val, i;
  val := list[1]^0;
  for i in [Length(list), Length(list)-1 .. 1] do
    val := val * list[i];
  od;
  return val;
end;;

# component extraction: block i (points (i-1)*nn+1..i*nn) -> S_nn permutation on 1..nn
compOfFix := function(perm, i, nn)
  local l, j, img;
  l := [];
  for j in [1..nn] do
    img := (j + (i-1)*nn)^perm;
    l[j] := img - (i-1)*nn;
  od;
  return PermList(l);
end;;

# generalized block extraction for unequal-size blocks: block occupies points
# [offset+1 .. offset+size] -> S_size permutation on 1..size
compOfBlock := function(perm, offset, size)
  local l, j, img;
  l := [];
  for j in [1..size] do
    img := (j + offset)^perm;
    l[j] := img - offset;
  od;
  return PermList(l);
end;;

# ================= Q8 (self-contained quaternion algebra, regular permutation rep) =================
# elements indexed 1..8 <-> (sign,unit): unit in {0=1,1=i,2=j,3=k}, sign in {+1,-1}.
QUnitTable := [ [[1,0],[1,1],[1,2],[1,3]],     # 1 * {1,i,j,k}
                 [[1,1],[-1,0],[1,3],[-1,2]],  # i * {1,i,j,k} = {i,-1,k,-j}
                 [[1,2],[-1,3],[-1,0],[1,1]],  # j * {1,i,j,k} = {j,-k,-1,i}
                 [[1,3],[1,2],[-1,1],[-1,0]] ];; # k * {1,i,j,k} = {k,j,-i,-1}

QMul := function(g, h)
  local t;
  t := QUnitTable[g[2]+1][h[2]+1];
  return [ g[1]*h[1]*t[1], t[2] ];
end;;

IdxOfQ := function(g) return g[2]*2 + (1 - g[1])/2 + 1; end;;
ElemOfIdxQ := function(idx)
  local k, unit, signCode;
  k := idx - 1;
  unit := QuoInt(k, 2);
  signCode := k mod 2;
  if signCode = 0 then return [1, unit]; else return [-1, unit]; fi;
end;;

QRegPerm := function(d)
  local l, idx;
  l := [];
  for idx in [1..8] do l[idx] := IdxOfQ(QMul(d, ElemOfIdxQ(idx))); od;
  return PermList(l);
end;;

QLabelOfElem := function(g)
  local unitNames;
  unitNames := ["1","i","j","k"];
  if g[1] = 1 then
    if g[2] = 0 then return "1"; else return unitNames[g[2]+1]; fi;
  else
    if g[2] = 0 then return "-1"; else return Concatenation("-", unitNames[g[2]+1]); fi;
  fi;
end;;

QLabelOfPerm := function(p) return QLabelOfElem(ElemOfIdxQ(1^p)); end;;

MakeQ8 := function()
  local xh, yh, ch;
  xh := QRegPerm([1,1]);  yh := QRegPerm([1,2]);  ch := QRegPerm([1,0]);
  return rec(x:=xh, y:=yh, c:=ch, G:=Group(xh,yh), label:=QLabelOfPerm);
end;;

# Dn element -> [a,e] (r^a s^e, abstract convention; abstract "r^a s" = GAP "s*r^a")
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

# ================= JSON output helpers (copied verbatim) =================
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

WriteFile := function(path, content)
  local f;
  f := OutputTextFile(path, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, content);
  CloseStream(f);
end;;

# ================= BFS word assignment (generic over any rec(x,y,G)) =================
BFSWords := function(gr)
  local gens, wordOf, queue, qi, cur, curWord, g, nv;
  gens := [ rec(sym:=["x",1], gap:=gr.x), rec(sym:=["x",-1], gap:=gr.x^-1),
            rec(sym:=["y",1], gap:=gr.y), rec(sym:=["y",-1], gap:=gr.y^-1) ];
  wordOf := NewDictionary(Identity(gr.G), true);
  AddDictionary(wordOf, Identity(gr.G), []);
  queue := [ Identity(gr.G) ];
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

# ================= evaluate an x/y word inside a QxT model =================
EvalWordQT := function(word, qt)
  local val, letter;
  val := ();
  for letter in word do
    if letter[1]="x" then val := val * qt.xx^letter[2];
    else val := val * qt.yy^letter[2]; fi;
  od;
  return val;
end;;

# ================= Q x T (transversal-cocycle) model, generalized to any Q =================
# (docs/wp2-transversal-model.md 12-rule table; copied verbatim from week3-M5-explorer.g)
BuildQTGeneral := function(Qgrp, phiX, phiY, phiC)
  local Qelts, posDict, posOf, phiXi, phiYi, np, imgS1, imgS2, t, i, d, pt, val, tp;
  Qelts := Elements(Qgrp);
  np := Length(Qelts);
  posDict := NewDictionary(Qelts[1], true);
  for i in [1..np] do AddDictionary(posDict, Qelts[i], i); od;
  posOf := function(v) return LookupDictionary(posDict, v); end;
  phiXi := phiX^-1;  phiYi := phiY^-1;
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
  return rec(s1:=PermList(imgS1), s2:=PermList(imgS2), np:=np, elts:=Qelts, posOf:=posOf);
end;;

# ================= hand-written minimal string scanner (K3.v1.json reduction target) =================
# (copied verbatim from week3-L-explorer.g / week3-M5-explorer.g)
FindPositionFrom := function(str, marker, startPos)
  local n, m, i, k, matched;
  n := Length(str);  m := Length(marker);
  if m = 0 then return startPos; fi;
  for i in [startPos..n-m+1] do
    matched := true;
    for k in [1..m] do
      if str[i+k-1] <> marker[k] then matched := false; break; fi;
    od;
    if matched then return i; fi;
  od;
  return fail;
end;;

DigitRunsToInts := function(s)
  local ints, cur, c;
  ints := [];  cur := "";
  for c in s do
    if c in "0123456789" then
      Append(cur, [c]);
    else
      if Length(cur) > 0 then Add(ints, Int(cur)); fi;
      cur := "";
    fi;
  od;
  if Length(cur) > 0 then Add(ints, Int(cur)); fi;
  return ints;
end;;

ParseK3Shadows := function(path)
  local content, stream, mk1, sStart, mk2, sEnd, shadowsStr, shadowsList, pos, j,
        digitStr, mVal, ftMk, ftStart, ftEndMk, ftEnd, tripleStr, ints;
  stream := InputTextFile(path);
  if stream = fail then Error("ParseK3Shadows: cannot open ", path); fi;
  content := ReadAll(stream);
  CloseStream(stream);
  mk1 := "\"shadows\":[";
  pos := FindPositionFrom(content, mk1, 1);
  if pos = fail then Error("ParseK3Shadows: shadows marker not found in ", path); fi;
  sStart := pos + Length(mk1);
  mk2 := "],\"counts\":";
  sEnd := FindPositionFrom(content, mk2, sStart);
  if sEnd = fail then Error("ParseK3Shadows: counts marker not found in ", path); fi;
  shadowsStr := content{[sStart..sEnd-1]};
  shadowsList := [];
  pos := 1;
  while true do
    pos := FindPositionFrom(shadowsStr, "\"m\":", pos);
    if pos = fail then break; fi;
    j := pos + 4;
    digitStr := "";
    while j <= Length(shadowsStr) and shadowsStr[j] in "0123456789" do
      Append(digitStr, [shadowsStr[j]]);  j := j+1;
    od;
    if Length(digitStr) = 0 then Error("ParseK3Shadows: empty m digit run at pos ", pos); fi;
    mVal := Int(digitStr);
    ftMk := "\"f_triple\":";
    ftStart := FindPositionFrom(shadowsStr, ftMk, pos);
    if ftStart = fail then Error("ParseK3Shadows: f_triple marker not found after pos ", pos); fi;
    ftEndMk := ",\"kernel_cert\":";
    ftEnd := FindPositionFrom(shadowsStr, ftEndMk, ftStart);
    if ftEnd = fail then Error("ParseK3Shadows: kernel_cert boundary not found after f_triple at ", ftStart); fi;
    tripleStr := shadowsStr{[ftStart+Length(ftMk)..ftEnd-1]};
    ints := DigitRunsToInts(tripleStr);
    if Length(ints) <> 6 then
      Error("ParseK3Shadows: f_triple int count != 6 (got ", Length(ints), ") at pos ", ftStart);
    fi;
    Add(shadowsList, rec(m:=mVal, triple:=[[ints[1],ints[2]],[ints[3],ints[4]],[ints[5],ints[6]]]));
    pos := pos + 4;
  od;
  return shadowsList;
end;;

# ================= generic reduced-hexagon enumeration (quotient shortcut, c_in_N = true) =================
# qrec = rec(x,y,c,G).  charmingSet = list of m in [0..nOrd-1] with gcd(2m+1,nOrd)=1 (spec-given,
# NOT recomputed here -- the manifest's charming_set is spec-disclosed and passed in by the caller).
# Returns rec with the exclusive staged counts (F16/W49) + shadows (only the ones that pass all
# three stages) + generation_detail (per-candidate pass/fail, G-05).
EnumerateReducedHexagon := function(qrec, charmingSet)
  local G, D, thetaHom, tauHom, zElt, bfs, Dwords, elt, cand, f, m, u, thetaf, hex310,
        ymf, tauymf, tau2ymf, hex311, genA, genB, surj, h10Fail, h11Fail, genFail,
        shadows, genDetail, candidateTotal;
  G := qrec.G;
  D := DerivedSubgroup(G);
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  if thetaHom = fail or tauHom = fail then
    Error("EnumerateReducedHexagon: theta/tau homomorphism construction failed (c_in_N assumption may be violated)");
  fi;
  bfs := BFSWords(qrec);
  if Length(bfs.elements) <> Size(G) then
    Error("EnumerateReducedHexagon: BFS did not cover full G: covered=", Length(bfs.elements), " expected=", Size(G));
  fi;
  Dwords := [];
  for elt in bfs.elements do
    if elt in D then Add(Dwords, rec(elt:=elt, word:=LookupDictionary(bfs.wordOf, elt))); fi;
  od;
  h10Fail := 0;  h11Fail := 0;  genFail := 0;  shadows := [];  genDetail := [];
  candidateTotal := Length(Dwords) * Length(charmingSet);
  for cand in Dwords do
    f := cand.elt;
    for m in charmingSet do
      u := 2*m+1;
      thetaf := Image(thetaHom, f);
      hex310 := AbstractProd([f, thetaf]) = Identity(G);
      if not hex310 then
        h10Fail := h10Fail + 1;
        Add(genDetail, rec(m:=m, f_word:=cand.word, pass:=false, stage:="h10_fail"));
        continue;
      fi;
      ymf := AbstractProd([qrec.y^m, f]);
      tauymf := Image(tauHom, ymf);
      tau2ymf := Image(tauHom, tauymf);
      hex311 := AbstractProd([tau2ymf, tauymf, ymf]) = Identity(G);
      if not hex311 then
        h11Fail := h11Fail + 1;
        Add(genDetail, rec(m:=m, f_word:=cand.word, pass:=false, stage:="h11_fail"));
        continue;
      fi;
      genA := qrec.x^u;
      genB := AbstractProd([f^-1, qrec.y^u, f]);
      surj := Size(Group(genA, genB)) = Size(G);
      if not surj then
        genFail := genFail + 1;
        Add(genDetail, rec(m:=m, f_word:=cand.word, pass:=false, stage:="generation_fail"));
      else
        Add(shadows, rec(m:=m, f:=f, word:=cand.word));
        Add(genDetail, rec(m:=m, f_word:=cand.word, pass:=true, stage:="pass"));
      fi;
    od;
  od;
  return rec(candidate_total:=candidateTotal, h10_fail:=h10Fail, h11_fail:=h11Fail,
             generation_fail:=genFail, shadow_total:=Length(shadows), shadows:=shadows,
             generation_detail:=genDetail, dwords_count:=Length(Dwords));
end;;

# ================= E_m table (U-F9): E_m := X^m Z^m Y^m, independent per-layer computation =================
ComputeEmTable := function(qrec, nOrd)
  local zElt, m, val, out;
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  out := [];
  for m in [0..nOrd-1] do
    val := AbstractProd([qrec.x^m, zElt^m, qrec.y^m]);
    Add(out, rec(m:=m, value:=val));
  od;
  return out;
end;;

# ================= generic Heisenberg-like class-2 group mod (nMod,nMod,cMod) =================
# elements (a,b,e), a,b in Z/nMod, e in Z/cMod; (a,b,e)(a',b',e') = (a+a',b+b',e+e'+a*b')
# (same cocycle form as H3 in week3-L-explorer.g, generalized moduli; independently hand-verified
# for (nMod,cMod)=(4,2) against manifest U-F4's explicit relations for P2 before use).
HeisMul := function(g, h, nMod, cMod)
  return [ (g[1]+h[1]) mod nMod, (g[2]+h[2]) mod nMod, (g[3]+h[3]+g[1]*h[2]) mod cMod ];
end;;

HeisIdxOfElem := function(e, nMod, cMod) return e[1]*nMod*cMod + e[2]*cMod + e[3] + 1; end;;
HeisElemOfIdx := function(idx, nMod, cMod)
  local k, a, b, e;
  k := idx - 1;
  a := QuoInt(k, nMod*cMod);  k := k mod (nMod*cMod);
  b := QuoInt(k, cMod);  e := k mod cMod;
  return [a, b, e];
end;;

HeisRegPerm := function(d, nMod, cMod)
  local l, idx, total;
  total := nMod*nMod*cMod;
  l := [];
  for idx in [1..total] do l[idx] := HeisIdxOfElem(HeisMul(d, HeisElemOfIdx(idx,nMod,cMod), nMod, cMod), nMod, cMod); od;
  return PermList(l);
end;;

MakeHeis := function(nMod, cMod)
  local Xe, Ye, xh, yh;
  Xe := [1,0,0];  Ye := [0,1,0];
  xh := HeisRegPerm(Xe, nMod, cMod);
  yh := HeisRegPerm(Ye, nMod, cMod);
  return rec(x:=xh, y:=yh, c:=(), G:=Group(xh,yh), nMod:=nMod, cMod:=cMod);
end;;

# ================= P3 = F2/F2^4 gamma_4(F2), order 128, class 3 =================
# Constructed as an explicit polycyclic-style presentation on generators X,Y,w,p,q with
# w:=[X,Y], p:=[w,X], q:=[w,Y] (manifest sec.2 stage 2b "derived_basis"), central gamma_3=<p,q>,
# and X^4=Y^4=w^2=p^2=q^2=1. This presentation was independently verified (search/tmp-p3-build.g,
# deleted after use) to produce a group of order EXACTLY 128 matching every relation in fixture
# U-F5 (exponent 4, class 3, gamma_3=<p,q> central of order 4, w^2=p^2=q^2=1) via GAP's own
# Todd-Coxeter coset enumeration + IsomorphismPcGroup -- this is not assumed, it is computed and
# cross-checked against the fixture before being adopted as P3 (report to commander).
MakeP3 := function()
  local F, gens, Xg, Yg, wg, pg, qg, rels, Gfp, sz, iso, Pc, imgsG, Xp, Yp;
  F := FreeGroup("Xg","Yg","wg","pg","qg");
  gens := GeneratorsOfGroup(F);
  Xg := gens[1];  Yg := gens[2];  wg := gens[3];  pg := gens[4];  qg := gens[5];
  rels := [
    Xg^4, Yg^4, wg^2, pg^2, qg^2,
    Comm(Xg,Yg)*wg^-1,
    Comm(wg,Xg)*pg^-1,
    Comm(wg,Yg)*qg^-1,
    Comm(pg,Xg), Comm(pg,Yg), Comm(qg,Xg), Comm(qg,Yg), Comm(pg,wg), Comm(qg,wg), Comm(pg,qg)
  ];
  Gfp := F/rels;
  sz := Size(Gfp);
  if sz <> 128 then
    Error("MakeP3: presentation did not produce order 128, got ", sz);
  fi;
  iso := IsomorphismPcGroup(Gfp);
  Pc := Image(iso);
  imgsG := List(GeneratorsOfGroup(Gfp), g -> Image(iso,g));
  Xp := imgsG[1];  Yp := imgsG[2];
  return rec(x:=Xp, y:=Yp, c:=Identity(Pc), G:=Pc);
end;;

# ================= word-level (natural left-to-right) machinery -- stage A2 only =================
# *** SUPERSEDED (裁定166・docs/notes/wcp5d_resolution_v1.md WDICT-4, 2026-07-29) ***
# The "natural" ruling below is WITHDRAWN (撤回済み). It was superseded first by the
# "prepend" ruling at L598-610 (which is itself the historically later, correct-per-WDICT-4
# convention pick between the two word-level accumulation orders) -- but WCP5-D found a
# THIRD, deeper bug that neither convention fixes: for c NOT IN N windows, tau (x->y,y->z)
# generally does NOT descend to F2/N_F2 at all (Ad(delta) differs from the naive tau by a
# c^{e(w)} factor, docs/notes/wcp5d_resolution_v1.md Prop 2) -- so BOTH word-level enumerators
# below (natural AND prepend) can silently mis-evaluate the reduced hexagon on such windows,
# independent of which left/right accumulation convention is chosen. The original 2026-07-26
# ruling text is left below unmodified for the historical record; treat it as superseded, not
# as current guidance.
# coordinator ruling 2026-07-26 [SUPERSEDED, see above]: A2 (c_in_N=false) MUST use word-level evaluation with the NATURAL
# left-to-right homomorphism convention (word [w1,...,wk] represents the F2 element w1*w2*...*wk,
# phi(w1...wk)=phi(w1)*...*phi(wk) using Q's own multiplication in matching order -- the SAME side
# established correct during stage 1a's crosscheck bug-hunt), explicitly NOT the "prepend"
# convention used by week3-M5-explorer.g's EvalWordInQ (that convention is only self-consistent
# there because it is paired with a matching "reversed" BFSWords storage scheme specific to that
# script's own left-regular-permutation-representation choice; mixing conventions is what caused
# the bug found in crosscheck/check-v2.mjs -- see that file's evalWordLeftAccum comment).

# NaturalBFSWords: word list [w1,...,wk] stored so that extending by appending a new letter at the
# END corresponds to RIGHT-multiplying the current element by that letter (cur*g) -- natural
# left-to-right reading.
NaturalBFSWords := function(gr)
  local gens, wordOf, queue, qi, cur, curWord, g, nv;
  gens := [ rec(sym:=["x",1], gap:=gr.x), rec(sym:=["x",-1], gap:=gr.x^-1),
            rec(sym:=["y",1], gap:=gr.y), rec(sym:=["y",-1], gap:=gr.y^-1) ];
  wordOf := NewDictionary(Identity(gr.G), true);
  AddDictionary(wordOf, Identity(gr.G), []);
  queue := [ Identity(gr.G) ];
  qi := 1;
  while qi <= Length(queue) do
    cur := queue[qi];  qi := qi+1;
    curWord := LookupDictionary(wordOf, cur);
    for g in gens do
      nv := cur * g.gap;   # natural: append g extends the word by right-multiplication
      if LookupDictionary(wordOf, nv) = fail then
        AddDictionary(wordOf, nv, Concatenation(curWord, [g.sym]));
        Add(queue, nv);
      fi;
    od;
  od;
  return rec(wordOf:=wordOf, elements:=queue);
end;;

# NaturalEvalWordInQ: phi(w1...wk) = phi(w1)*phi(w2)*...*phi(wk) in Q, natural order.
NaturalEvalWordInQ := function(word, xg, yg, idG)
  local val, letter;
  val := idG;
  for letter in word do
    if letter[1]="x" then val := val * xg^letter[2];
    else val := val * yg^letter[2]; fi;
  od;
  return val;
end;;

ThetaLetterNatural := function(l)
  if l[1] = "x" then return [["y",l[2]]]; else return [["x",l[2]]]; fi;
end;;
TauLetterNatural := function(l)
  if l[1] = "x" then
    return [["y",l[2]]];
  else
    if l[2] = 1 then return [["y",-1],["x",-1]]; else return [["x",1],["y",1]]; fi;
  fi;
end;;
ThetaWordNatural := function(word) return Concatenation(List(word, ThetaLetterNatural)); end;;
TauWordNatural := function(word) return Concatenation(List(word, TauLetterNatural)); end;;

# *** WARNING (裁定166・docs/notes/wcp5d_resolution_v1.md, 2026-07-29): for c NOT IN N windows,
# DO NOT use this function (or EnumerateWordLevelHexagonPrepend below) to decide the reduced
# hexagon / shadow membership. tau (x->y, y->z=(xy)^-1) generally fails to descend to F2/N_F2
# when c is not in N (the true descended map is Ad(delta), which differs from naive tau by a
# c^{e(w)} twist depending on the BFS word's total exponent sum e(w) -- so the SAME group
# element f can pass or fail (3.11) depending on which word represents it; docs/notes/
# wcp5d_resolution_v1.md V5c gives an explicit reversal witness). Use the (F2) quotient rule
# instead (PB3/N-internal, theta~ = Ad(Delta), tau~ = Ad(delta); see search/wall-miner-v4.g's
# CorrectedShadows for the GAP implementation) for any c-not-in-N window. This function is left
# in place uncut (not deleted, not Error()-stubbed) per the coordinator's instruction, purely
# as a preserved historical artifact / negative fixture -- it is NOT safe to call on c-not-in-N
# windows for a real lead/claim.
# EnumerateWordLevelHexagon: word-level (3.10)/(3.11) via natural evaluation (mandatory when
# c_in_N=false). Also computes the quotient-shortcut result per candidate as a DIAGNOSTIC ONLY
# (A-F4: judged by word-level; quotient-shortcut recorded for comparison, quotient_eval_diff_count).
EnumerateWordLevelHexagon := function(qrec, charmingSet)
  local G, D, bfs, Dwords, elt, cand, f, m, u, thetaWord, hex310, yWordM, ymfWord, tauWord1,
        tauWord2, hex311, genA, genB, surj, h10Fail, h11Fail, genFail, shadows, genDetail,
        candidateTotal, thetaHom, tauHom, zElt, quotientAvailable, thetaHomF, ymfElt, tauHomYmf,
        tau2HomYmf, hex311Quot, hex310Quot, thetaFQuot, diffCount, diffDetail;
  G := qrec.G;
  D := DerivedSubgroup(G);
  # diagnostic-only quotient shortcut (may legitimately fail to construct since c_in_N=false;
  # if it fails to construct we just skip the diagnostic comparison for that stage)
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  quotientAvailable := (thetaHom <> fail) and (tauHom <> fail);
  bfs := NaturalBFSWords(qrec);
  if Length(bfs.elements) <> Size(G) then
    Error("EnumerateWordLevelHexagon: BFS did not cover full G: covered=", Length(bfs.elements), " expected=", Size(G));
  fi;
  Dwords := [];
  for elt in bfs.elements do
    if elt in D then Add(Dwords, rec(elt:=elt, word:=LookupDictionary(bfs.wordOf, elt))); fi;
  od;
  h10Fail := 0;  h11Fail := 0;  genFail := 0;  shadows := [];  genDetail := [];  diffCount := 0;  diffDetail := [];
  candidateTotal := Length(Dwords) * Length(charmingSet);
  for cand in Dwords do
    f := cand.elt;
    for m in charmingSet do
      u := 2*m+1;
      thetaWord := ThetaWordNatural(cand.word);
      hex310 := NaturalEvalWordInQ(Concatenation(cand.word, thetaWord), qrec.x, qrec.y, Identity(G)) = Identity(G);
      if quotientAvailable then
        thetaFQuot := Image(thetaHom, f);
        hex310Quot := AbstractProd([f, thetaFQuot]) = Identity(G);
      fi;
      if not hex310 then
        h10Fail := h10Fail + 1;
        Add(genDetail, rec(m:=m, f_word:=cand.word, pass:=false, stage:="h10_fail"));
        if quotientAvailable and hex310Quot <> hex310 then
          diffCount := diffCount + 1;
          Add(diffDetail, rec(m:=m, f_word:=cand.word, word_level:=hex310, quotient_shortcut:=hex310Quot, at:="3.10"));
        fi;
        continue;
      fi;
      yWordM := List([1..m], ii -> ["y",1]);
      ymfWord := Concatenation(yWordM, cand.word);
      tauWord1 := TauWordNatural(ymfWord);
      tauWord2 := TauWordNatural(tauWord1);
      hex311 := NaturalEvalWordInQ(Concatenation(tauWord2, tauWord1, ymfWord), qrec.x, qrec.y, Identity(G)) = Identity(G);
      if quotientAvailable then
        ymfElt := AbstractProd([qrec.y^m, f]);
        tauHomYmf := Image(tauHom, ymfElt);
        tau2HomYmf := Image(tauHom, tauHomYmf);
        hex311Quot := AbstractProd([tau2HomYmf, tauHomYmf, ymfElt]) = Identity(G);
      fi;
      if not hex311 then
        h11Fail := h11Fail + 1;
        Add(genDetail, rec(m:=m, f_word:=cand.word, pass:=false, stage:="h11_fail"));
        if quotientAvailable and hex311Quot <> hex311 then
          diffCount := diffCount + 1;
          Add(diffDetail, rec(m:=m, f_word:=cand.word, word_level:=hex311, quotient_shortcut:=hex311Quot, at:="3.11"));
        fi;
        continue;
      fi;
      if quotientAvailable and ((not hex310Quot) or (not hex311Quot)) then
        diffCount := diffCount + 1;
        Add(diffDetail, rec(m:=m, f_word:=cand.word, word_level:=true, quotient_shortcut:=false, at:="pass_vs_fail"));
      fi;
      genA := qrec.x^u;
      genB := AbstractProd([f^-1, qrec.y^u, f]);
      surj := Size(Group(genA, genB)) = Size(G);
      if not surj then
        genFail := genFail + 1;
        Add(genDetail, rec(m:=m, f_word:=cand.word, pass:=false, stage:="generation_fail"));
      else
        Add(shadows, rec(m:=m, f:=f, word:=cand.word));
        Add(genDetail, rec(m:=m, f_word:=cand.word, pass:=true, stage:="pass"));
      fi;
    od;
  od;
  return rec(candidate_total:=candidateTotal, h10_fail:=h10Fail, h11_fail:=h11Fail,
             generation_fail:=genFail, shadow_total:=Length(shadows), shadows:=shadows,
             generation_detail:=genDetail, dwords_count:=Length(Dwords),
             quotient_eval_diff_count:=diffCount, quotient_eval_diff_detail:=diffDetail,
             quotient_shortcut_available:=quotientAvailable);
end;;

# ================= word-level (prepend, week3-M5-explorer.g convention) machinery =================
# coordinator ruling 2026-07-26 (reversing the earlier "natural" ruling, on evidence): A2 must use
# the SAME prepend convention as week3-M5-explorer.g's EvalWordInQ, paired with the SAME BFSWords
# (already defined above, prepend-storage). Ground-truth check via genuine GAP FreeGroup
# automorphisms (theta,tau on F2 directly, no custom word-substitution code) confirmed: the
# "paper's word AB = GAP's B*A" reversal (established via 1a's S3-marking and A1's A5-marking
# fixtures) applies generally, and for objects NOT built via an artificial left-regular
# permutation representation (like A5 here), only ONE reversal applies -- so prepend accumulation
# (which already embeds that single reversal) is correct, not natural/append. For objects that ARE
# built via left-regular representation (Q8/D_n/H3/P2/P3), TWO reversals compose (representation
# reversal + paper-GAP reversal) and cancel, which is why natural accumulation happened to look
# right there. ThetaLetter/TauLetter substitution RULES are identical either way (pure automorphism
# letter-substitution, convention-independent); only the FINAL evaluation accumulation differs.
ThetaLetter := function(l)
  if l[1] = "x" then return [["y",l[2]]]; else return [["x",l[2]]]; fi;
end;;
TauLetter := function(l)
  if l[1] = "x" then
    if l[2] = 1 then return [["y",1]]; else return [["y",-1]]; fi;
  else
    if l[2] = 1 then return [["y",-1],["x",-1]]; else return [["x",1],["y",1]]; fi;
  fi;
end;;
ThetaWord := function(word) return Concatenation(List(word, ThetaLetter)); end;;
TauWord := function(word) return Concatenation(List(word, TauLetter)); end;;

# EvalWordInQ: prepend accumulation (val := g^pow * val for each letter, processing the word list
# left to right) -- matches week3-M5-explorer.g exactly.
EvalWordInQ := function(word, xg, yg, idG)
  local val, letter;
  val := idG;
  for letter in word do
    if letter[1]="x" then val := xg^letter[2] * val;
    else val := yg^letter[2] * val; fi;
  od;
  return val;
end;;

# *** WARNING (裁定166・docs/notes/wcp5d_resolution_v1.md WDICT-4, 2026-07-29): prepend IS the
# correct left/right accumulation convention (definition note S1.5 convention W-2), but that is
# a SEPARATE question from the c-not-in-N descent bug above EnumerateWordLevelHexagon. For
# c-not-in-N windows this function is ALSO unsafe (same tau-does-not-descend root cause;
# WDICT-4: "c not in N ではどちらも誤り"). Use the (F2) quotient rule (search/wall-miner-v4.g's
# CorrectedShadows) for c-not-in-N windows instead. Left uncut per the coordinator's instruction.
# EnumerateWordLevelHexagonPrepend: word-level (3.10)/(3.11) via prepend evaluation (the spec's
# pre-registered convention for A2, per manifest_spec_v1.md's "M5実装と同一" instruction).
EnumerateWordLevelHexagonPrepend := function(qrec, charmingSet)
  local G, D, bfs, Dwords, elt, cand, f, m, u, thetaWord, hex310, yWordM, ymfWord, tauWord1,
        tauWord2, hex311, genA, genB, surj, h10Fail, h11Fail, genFail, shadows, genDetail,
        candidateTotal, thetaHom, tauHom, zElt, quotientAvailable, hex310Quot, hex311Quot,
        thetaFQuot, ymfElt, tauHomYmf, tau2HomYmf, diffCount, diffDetail;
  G := qrec.G;
  D := DerivedSubgroup(G);
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  quotientAvailable := (thetaHom <> fail) and (tauHom <> fail);
  bfs := BFSWords(qrec);
  if Length(bfs.elements) <> Size(G) then
    Error("EnumerateWordLevelHexagonPrepend: BFS did not cover full G: covered=", Length(bfs.elements), " expected=", Size(G));
  fi;
  Dwords := [];
  for elt in bfs.elements do
    if elt in D then Add(Dwords, rec(elt:=elt, word:=LookupDictionary(bfs.wordOf, elt))); fi;
  od;
  h10Fail := 0;  h11Fail := 0;  genFail := 0;  shadows := [];  genDetail := [];  diffCount := 0;  diffDetail := [];
  candidateTotal := Length(Dwords) * Length(charmingSet);
  for cand in Dwords do
    f := cand.elt;
    for m in charmingSet do
      u := 2*m+1;
      thetaWord := ThetaWord(cand.word);
      hex310 := EvalWordInQ(Concatenation(cand.word, thetaWord), qrec.x, qrec.y, Identity(G)) = Identity(G);
      if quotientAvailable then
        thetaFQuot := Image(thetaHom, f);
        hex310Quot := AbstractProd([f, thetaFQuot]) = Identity(G);
      fi;
      if not hex310 then
        h10Fail := h10Fail + 1;
        Add(genDetail, rec(m:=m, f_word:=cand.word, pass:=false, stage:="h10_fail"));
        if quotientAvailable and hex310Quot <> hex310 then
          diffCount := diffCount + 1;
          Add(diffDetail, rec(m:=m, f_word:=cand.word, word_level:=hex310, quotient_shortcut:=hex310Quot, at:="3.10"));
        fi;
        continue;
      fi;
      yWordM := List([1..m], ii -> ["y",1]);
      ymfWord := Concatenation(yWordM, cand.word);
      tauWord1 := TauWord(ymfWord);
      tauWord2 := TauWord(tauWord1);
      hex311 := EvalWordInQ(Concatenation(tauWord2, tauWord1, ymfWord), qrec.x, qrec.y, Identity(G)) = Identity(G);
      if quotientAvailable then
        ymfElt := AbstractProd([qrec.y^m, f]);
        tauHomYmf := Image(tauHom, ymfElt);
        tau2HomYmf := Image(tauHom, tauHomYmf);
        hex311Quot := AbstractProd([tau2HomYmf, tauHomYmf, ymfElt]) = Identity(G);
      fi;
      if not hex311 then
        h11Fail := h11Fail + 1;
        Add(genDetail, rec(m:=m, f_word:=cand.word, pass:=false, stage:="h11_fail"));
        if quotientAvailable and hex311Quot <> hex311 then
          diffCount := diffCount + 1;
          Add(diffDetail, rec(m:=m, f_word:=cand.word, word_level:=hex311, quotient_shortcut:=hex311Quot, at:="3.11"));
        fi;
        continue;
      fi;
      if quotientAvailable and ((not hex310Quot) or (not hex311Quot)) then
        diffCount := diffCount + 1;
        Add(diffDetail, rec(m:=m, f_word:=cand.word, word_level:=true, quotient_shortcut:=false, at:="pass_vs_fail"));
      fi;
      genA := qrec.x^u;
      genB := AbstractProd([f^-1, qrec.y^u, f]);
      surj := Size(Group(genA, genB)) = Size(G);
      if not surj then
        genFail := genFail + 1;
        Add(genDetail, rec(m:=m, f_word:=cand.word, pass:=false, stage:="generation_fail"));
      else
        Add(shadows, rec(m:=m, f:=f, word:=cand.word));
        Add(genDetail, rec(m:=m, f_word:=cand.word, pass:=true, stage:="pass"));
      fi;
    od;
  od;
  return rec(candidate_total:=candidateTotal, h10_fail:=h10Fail, h11_fail:=h11Fail,
             generation_fail:=genFail, shadow_total:=Length(shadows), shadows:=shadows,
             generation_detail:=genDetail, dwords_count:=Length(Dwords),
             quotient_eval_diff_count:=diffCount, quotient_eval_diff_detail:=diffDetail,
             quotient_shortcut_available:=quotientAvailable);
end;;

# ================= robustness check (natural vs prepend, quotient_ok stages only) =================
# For stages using the quotient-SHORTCUT (EnumerateReducedHexagon: theta/tau via genuine
# GroupHomomorphismByImages on the ACTUAL group elements, never touching word storage at all), the
# convention question does not even arise for the pass/fail judgement -- but we can still check
# robustness DIAGNOSTICALLY by running BOTH word-level evaluators (natural and prepend) against the
# same candidate set and confirming they agree with each other (and, ideally, with the trusted
# shortcut result). Cheap: reuses EnumerateWordLevelHexagon (natural) and
# EnumerateWordLevelHexagonPrepend (prepend) on the same qrec/charmingSet.
CheckConventionRobust := function(qrec, charmingSet)
  local natRes, prepRes, natMap, prepRes2, agree, mismatches, k1, k2;
  natRes := EnumerateWordLevelHexagon(qrec, charmingSet);
  prepRes := EnumerateWordLevelHexagonPrepend(qrec, charmingSet);
  agree := (natRes.h10_fail = prepRes.h10_fail) and (natRes.h11_fail = prepRes.h11_fail)
           and (natRes.generation_fail = prepRes.generation_fail) and (natRes.shadow_total = prepRes.shadow_total);
  return rec(agree:=agree, natural:=rec(h10_fail:=natRes.h10_fail, h11_fail:=natRes.h11_fail,
             generation_fail:=natRes.generation_fail, shadow_total:=natRes.shadow_total),
             prepend:=rec(h10_fail:=prepRes.h10_fail, h11_fail:=prepRes.h11_fail,
             generation_fail:=prepRes.generation_fail, shadow_total:=prepRes.shadow_total));
end;;

Print("week3-battery-common.g loaded.\n");
