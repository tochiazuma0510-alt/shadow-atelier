# week3-L-explorer.g -- WP3a GAP explorer for L = K^(3) cap N0 (Week 3, single object)
#
# Usage: .\gap.ps1 search\week3-L-explorer.g
#
# Design source (read in full before implementation, per commander instructions):
#   docs/week3-L-she-ji.md (week3-L design v1.1) SS1-SS5
#   docs/wp2-transversal-model.md (12-rule table + gtsh-cert/v1 schema + addendum 1)
#   search/suite-wp2-shard-a.g (MakeDn, MakeGn, AbstractProd, compOfFix, BFSWords,
#     BuildQTDihedral, EvalWordQT, JSON helpers -- all generalized/copied from here)
#   search/suite-wp2-shard-b2.g (BuildCertJsonN5 kernel_cert type=brute pattern)
#   certificates/K3.v1.json (reduction target, parsed directly by hand-written string
#     scanner -- see note below)
#
# ================================================================================
# DEVIATION NOTE (must be reported to commander): the task text says Q_L should be
# built as a 54-point permutation group with G3 on points 1-27 and H3 on points
# 28-54.  This is NOT what the existing MakeGn(3) code produces: MakeGn(n) builds
# G_n as 3 blocks of n points each (3n points total), so MakeGn(3) acts on 3*3=9
# points, NOT 27.  This is also confirmed by the design doc's own invariant
# checks: |G3|=108 = Size(Group(gn.x,gn.y)) for gn=MakeGn(3), which is exactly the
# existing 9-point representation (expectedSize(3) = 4*3^3 = 108).  A 27-point
# G3 representation does not correspond to any existing/intended construction
# here (it would require MakeGn(9), order 4*9^3=2916, which is wrong -- that is
# |Q_L| itself, not |G3|).
# We therefore build Q_L on 36 points: G3 = MakeGn(3) on points 1-9 (3 blocks of 3,
# exactly as MakeGn already produces), H3 regular representation on points 10-36
# (27 points).  All required numeric invariants (|G3|=108, |H3|=27, |Q_L|=2916,
# |[Q_L,Q_L]|=81, L_ord=6, X_L={0,2,3,5}) are verified below and match the design
# doc exactly regardless of this point-count choice, since the *content* of the
# G3 factor (MakeGn(3), order 108) is unchanged -- only the total permutation
# degree used to realize the direct product on disjoint domains differs (36 vs the
# textually-stated but code-inconsistent 54).
# ================================================================================

SizeScreen([4096, 0]);;
startTime := Runtime();;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ================= basic helpers (copied verbatim from suite-wp2-shard-a.g) =================
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

# abstract product "f1 f2 ... fk" (paper notation, left to right) -> GAP form
# (reversal convention, empirically verified for the Dn/Gn-style representation;
#  reused unchanged here since Q_L's G3 factor uses the same Gn construction and
#  same "left action" convention as the design doc specifies)
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
# generalizes BuildQTDihedral (suite-wp2-shard-a.g) to an arbitrary finite group Qgrp
# with phiX, phiY, phiC in Qgrp (instead of the D_n-specific r,s).  Uses a dictionary
# for O(1) position lookup since |Q_L| = 2916 makes the O(n) Position() scan used in
# the original dihedral version too slow to be prudent at this scale.
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
  return rec(s1:=PermList(imgS1), s2:=PermList(imgS2), np:=np);
end;;

# ================= H3 = Heisenberg mod 3 (order 27), regular representation =================
# element = [a,b,e] in (Z/3)^3, product (a,b,e)(a',b',e') = (a+a', b+b', e+e'+a*b') mod 3
HMul := function(p, q)
  return [ (p[1]+q[1]) mod 3, (p[2]+q[2]) mod 3, (p[3]+q[3]+p[1]*q[2]) mod 3 ];
end;;

IdxOfElem := function(e) return 9*e[1] + 3*e[2] + e[3] + 1; end;;
ElemOfIdx := function(idx)
  local k, a, b, e;
  k := idx - 1;
  a := QuoInt(k, 9);  k := k mod 9;
  b := QuoInt(k, 3);  e := k mod 3;
  return [a,b,e];
end;;

# left regular representation: point p (idx) -> idx of d*p
H3RegPerm := function(d)
  local l, idx;
  l := [];
  for idx in [1..27] do
    l[idx] := IdxOfElem(HMul(d, ElemOfIdx(idx)));
  od;
  return PermList(l);
end;;

# ================= hand-written minimal string scanner (K3.v1.json reduction target) =================
# Rationale (per commander instructions): reading K3.v1.json's bytes directly and
# pattern-matching "m" / "f_triple" fields guarantees the extracted shadow indices
# match the *actual* on-disk certificate's shadow order exactly.  An independent
# re-derivation of K3's shadows (re-running the dihedral n=3 explorer logic here)
# risks BFS-order-dependent index drift versus the committed certificate file, even
# if the underlying group-theoretic content is identical -- direct parsing avoids
# that risk entirely.  This is not a full JSON parser: it is a fixed-format scanner
# tailored to the known, frozen structure of gtsh-cert/v1 dihedral certificates
# (single-line minified JSON, no embedded escaped quotes in the fields scanned).
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

# ================================================================================
# Build G3 = MakeGn(3) (order 108, on points 1-9) and H3 (order 27, on points 10-36)
# ================================================================================
gn := MakeGn(3);;
Print("G3 = MakeGn(3): |G3| = ", Size(gn.G), " (expect 108)\n");

Xh := [1,0,0];;  Yh := [0,1,0];;  Zeroh := [0,0,0];;
Xp := H3RegPerm(Xh);;  Yp := H3RegPerm(Yh);;

# ---- H3 fixture self-checks (must all hold; Error otherwise) ----
if not (Xp^3 = () and Yp^3 = () and (Xp*Yp)^3 = ()) then
  Error("H3 fixture FAILED: X^3=Y^3=(XY)^3=1 required");
fi;
commXY := Xp^-1 * Yp^-1 * Xp * Yp;;
if Order(commXY) <> 3 then
  Error("H3 fixture FAILED: [X,Y] must have order 3, got ", Order(commXY));
fi;
if not (commXY*Xp = Xp*commXY and commXY*Yp = Yp*commXY) then
  Error("H3 fixture FAILED: [X,Y] must be central (commute with X and Y)");
fi;
if (commXY^-1 * Xp^-1 * commXY * Xp) <> () then
  Error("H3 fixture FAILED: [[X,Y],X] must be trivial");
fi;
Print("[", PF(true), "] H3 fixture: X^3=Y^3=(XY)^3=1, [X,Y] central order 3, [[X,Y],X]=1\n");
Print("  (sanity, non-fatal) |<X,Y>| in H3 regular rep = ", Size(Group(Xp,Yp)), " (expect 27)\n");

# ---- Q_L construction on 36 points: G3 on 1-9, H3 on 10-36 ----
xhat := PermList(Concatenation(List([1..9], j -> j^gn.x), List([1..27], j -> 9 + (j^Xp))));;
yhat := PermList(Concatenation(List([1..9], j -> j^gn.y), List([1..27], j -> 9 + (j^Yp))));;
QL := Group(xhat, yhat);;

# ---- fixture self-checks on Q_L (must all hold; Error otherwise) ----
qlSize := Size(QL);;
if qlSize <> 2916 then
  Error("Q_L fixture FAILED: |Q_L| = ", qlSize, ", expected 2916");
fi;
Print("[", PF(true), "] |Q_L| = ", qlSize, " (expect 2916)\n");

DQL := DerivedSubgroup(QL);;
if Size(DQL) <> 81 then
  Error("Q_L fixture FAILED: |[Q_L,Q_L]| = ", Size(DQL), ", expected 81");
fi;
Print("[", PF(true), "] |[Q_L,Q_L]| = ", Size(DQL), " (expect 81)\n");

Lord := Lcm(Order(xhat), Order(yhat));;
if Lord <> 6 then
  Error("Q_L fixture FAILED: L_ord = Lcm(Order(xhat),Order(yhat)) = ", Lord, ", expected 6");
fi;
Print("[", PF(true), "] L_ord = ", Lord, " (expect 6)\n");

XL := Filtered([0..5], mm -> Gcd(2*mm+1,6) = 1);;
if XL <> [0,2,3,5] then
  Error("Q_L fixture FAILED: X_L = ", XL, ", expected [0,2,3,5]");
fi;
Print("[", PF(true), "] X_L = ", XL, " (expect [0,2,3,5])\n");

Print("\n全 fixture 自己検査 PASS. 実装続行.\n\n");

# ================================================================================
# Enumeration (reduced hexagon inside Q_L, mirrors ProcessDihedral in suite-wp2-shard-a.g)
# ================================================================================
qlrec := rec(x := xhat, y := yhat, G := QL);;

zL := AbstractProd([xhat, yhat])^-1;;
thetaHom := GroupHomomorphismByImages(QL, QL, [xhat,yhat], [yhat,xhat]);;
tauHom := GroupHomomorphismByImages(QL, QL, [xhat,yhat], [yhat,zL]);;
if thetaHom = fail or tauHom = fail then
  Error("theta/tau homomorphism construction failed for Q_L");
fi;

t0 := Runtime();;
bfs := BFSWords(qlrec);;
t1 := Runtime();;
Print("BFS over Q_L: covered ", Length(bfs.elements), " elements (expect 2916), time_ms=", t1-t0, "\n");
if Length(bfs.elements) <> Size(QL) then
  Error("BFS did not cover full Q_L: covered=", Length(bfs.elements), " expected=", Size(QL));
fi;

Dwords := [];;
for elt in bfs.elements do
  if elt in DQL then Add(Dwords, rec(elt:=elt, word:=LookupDictionary(bfs.wordOf, elt))); fi;
od;
Print("Dwords (candidates f in [Q_L,Q_L]): ", Length(Dwords), " (expect 81)\n");

rawCount := 0;;  hexPass := 0;;  charmPass := 0;;  surjPass := 0;;  shadows := [];;
t0 := Runtime();;
for cand in Dwords do
  f := cand.elt;
  for m in XL do
    rawCount := rawCount + 1;
    u := 2*m+1;
    thetaf := Image(thetaHom, f);
    hex310 := AbstractProd([f, thetaf]) = Identity(QL);
    ymf := AbstractProd([yhat^m, f]);
    tauymf := Image(tauHom, ymf);
    tau2ymf := Image(tauHom, tauymf);
    hex311 := AbstractProd([tau2ymf, tauymf, ymf]) = Identity(QL);
    if hex310 and hex311 then
      hexPass := hexPass + 1;
      charmPass := charmPass + 1;   # f in [Q_L,Q_L] by construction -> charming holds
      genA := xhat^u;
      genB := AbstractProd([f^-1, yhat^u, f]);
      surj := Size(Group(genA, genB)) = Size(QL);
      if surj then
        surjPass := surjPass + 1;
        Add(shadows, rec(m:=m, f:=f, word:=cand.word));
      fi;
    fi;
  od;
od;
t1 := Runtime();;
Print("reduced hexagon + surjective enumeration: time_ms=", t1-t0, "\n");
Print("counts: raw_candidates=", rawCount, " hexagon_pass=", hexPass,
      " charming_pass=", charmPass, " surjective_pass=", surjPass, "\n");
if rawCount <> 324 then
  Print("  [ANOMALY] raw_candidates = ", rawCount, ", design expected 324 (4 x 81)\n");
fi;

# ================================================================================
# Full hexagon double-check on Q_L x T model (17496 points)
# ================================================================================
t0 := Runtime();;
qt := BuildQTGeneral(QL, xhat, yhat, Identity(QL));;
t1 := Runtime();;
Print("Q_L x T model built: np=", qt.np, " total_points=", 6*qt.np, " time_ms=", t1-t0, "\n");
qt.xx := qt.s1^2;;  qt.yy := qt.s2^2;;  qt.cc := (qt.s1*qt.s2*qt.s1)^2;;

if not (qt.s1*qt.s2*qt.s1 = qt.s2*qt.s1*qt.s2) then
  Error("QxT braid relation failed for L");
fi;
Print("[", PF(true), "] QxT braid relation s1 s2 s1 = s2 s1 s2 holds\n");

t0 := Runtime();;
qtGroupSize := Size(Group(qt.s1, qt.s2));;
t1 := Runtime();;
Print("Size(<s1,s2>) = ", qtGroupSize, " (expect 17496), time_ms=", t1-t0, "\n");
if qtGroupSize <> 17496 then
  Error("QxT |<s1,s2>| mismatch for L: got ", qtGroupSize, ", expected 17496");
fi;

if qt.cc <> () then
  Error("QxT c-component check failed for L: cc = (s1 s2 s1)^2 should be identity (c=1), got non-identity");
fi;
Print("[", PF(true), "] QxT cc = (s1 s2 s1)^2 = identity (c maps to 1 in Q_L)\n");

dblFail := 0;;
t0 := Runtime();;
for sh in shadows do
  m := sh.m;  u := 2*m+1;
  fhat := EvalWordQT(sh.word, qt);  fhatInv := fhat^-1;
  lhs33 := qt.s1^u * fhatInv * qt.s2^u * fhat;
  rhs33 := fhatInv * qt.s1*qt.s2 * qt.xx^(-m) * qt.cc^m;
  lhs34 := fhatInv * qt.s2^u * fhat * qt.s1^u;
  rhs34 := qt.s2*qt.s1 * qt.yy^(-m) * qt.cc^m * fhat;
  if not ((lhs33=rhs33) and (lhs34=rhs34)) then
    dblFail := dblFail + 1;
    Print("  [ANOMALY] full-hexagon double-check FAILED for shadow m=", m, "\n");
  fi;
  sh.fhat := fhat;
od;
t1 := Runtime();;
Print("full hexagon double-check: dblFail=", dblFail, " (of ", Length(shadows), " shadows), time_ms=", t1-t0, "\n");

# ================================================================================
# composition_table (3.53) and inverse_map (3.54), generalized to Q_L / L_ord=6
# ================================================================================
compTable := [];;
t0 := Runtime();;
for i1 in [1..Length(shadows)] do
  for i2 in [1..Length(shadows)] do
    m1 := shadows[i1].m;  f1 := shadows[i1].f;
    m2 := shadows[i2].m;  f2 := shadows[i2].f;
    u1 := 2*m1+1;
    imgx := xhat^u1;
    imgy := AbstractProd([f1^-1, yhat^u1, f1]);
    Ehom := GroupHomomorphismByImages(QL, QL, [xhat,yhat], [imgx,imgy]);
    if Ehom = fail then
      Print("  [ANOMALY] E_{m1,f1} hom construction failed i1=", i1, "\n");
      continue;
    fi;
    newm := (2*m1*m2 + m1 + m2) mod 6;
    newf := AbstractProd([f1, Image(Ehom, f2)]);
    idx := fail;
    for t in [1..Length(shadows)] do
      if shadows[t].m = newm and shadows[t].f = newf then idx := t; break; fi;
    od;
    if idx = fail then
      Print("  [ANOMALY] composition (", i1, ",", i2, ") has no matching shadow!\n");
    else
      Add(compTable, [i1-1, i2-1, idx-1]);
    fi;
  od;
od;
t1 := Runtime();;
Print("composition_table: ", Length(compTable), " entries (expect ", Length(shadows)^2, "), time_ms=", t1-t0, "\n");

invMap := [];;
t0 := Runtime();;
for i1 in [1..Length(shadows)] do
  m1 := shadows[i1].m;  f1 := shadows[i1].f;  u1 := 2*m1+1;
  uinv := Gcdex(u1, 6).coeff1 mod 6;
  mtilde := ((-uinv*m1) mod 6);
  imgx := xhat^u1;
  imgy := AbstractProd([f1^-1, yhat^u1, f1]);
  Ehom := GroupHomomorphismByImages(QL, QL, [xhat,yhat], [imgx,imgy]);
  if Ehom = fail or not IsBijective(Ehom) then
    Print("  [ANOMALY] E hom not bijective for inverse at i1=", i1, "\n");
    continue;
  fi;
  ftilde := PreImagesRepresentative(Ehom, f1^-1);
  tildeIdx := fail;
  for t in [1..Length(shadows)] do
    if shadows[t].m = mtilde and shadows[t].f = ftilde then tildeIdx := t; break; fi;
  od;
  if tildeIdx = fail then
    Print("  [ANOMALY] inverse of shadow ", i1, " (m~=", mtilde, ") not found among shadows!\n");
  else
    Add(invMap, [i1-1, tildeIdx-1]);
  fi;
od;
t1 := Runtime();;
Print("inverse_map: ", Length(invMap), " entries (expect ", Length(shadows), "), time_ms=", t1-t0, "\n");

# ================================================================================
# G3-component extraction (for f_triple and reduction to K3)
# ================================================================================
for sh in shadows do
  g3perm := PermList(List([1..9], j -> j^sh.f));
  g1c := compOfFix(g3perm, 1, 3);  g2c := compOfFix(g3perm, 2, 3);  g3c := compOfFix(g3perm, 3, 3);
  sh.triple := [ DnElemToAE(g1c, gn.r, gn.s, 3), DnElemToAE(g2c, gn.r, gn.s, 3), DnElemToAE(g3c, gn.r, gn.s, 3) ];
od;

# ================================================================================
# reduction to K3.v1.json (direct byte-level parse, see ParseK3Shadows note above)
# ================================================================================
k3Shadows := ParseK3Shadows("certificates/K3.v1.json");;
Print("Parsed K3.v1.json: ", Length(k3Shadows), " shadows (expect 12)\n");
if Length(k3Shadows) <> 12 then
  Print("  [ANOMALY] K3.v1.json shadow count parsed as ", Length(k3Shadows), ", expected 12\n");
fi;

redImages := [];;  redSeen := [];;
for sh in shadows do
  idx := fail;
  for t in [1..Length(k3Shadows)] do
    if k3Shadows[t].m = sh.m and k3Shadows[t].triple = sh.triple then idx := t; break; fi;
  od;
  if idx = fail then
    Print("  [ANOMALY] reduction L->K3: shadow (m=", sh.m, ", triple=", sh.triple, ") has no image in K3!\n");
    Add(redImages, -1);
  else
    Add(redImages, idx-1);
    if not (idx in redSeen) then Add(redSeen, idx); fi;
  fi;
od;
redSurjective := Length(redSeen) = Length(k3Shadows);;
Print("reduction L -> K3: images=", redImages, "  surjective=", redSurjective,
      "  (covered ", Length(redSeen), " of ", Length(k3Shadows), " K3 shadows)\n");

Print("\n累計 elapsed ms: ", Runtime()-startTime, "\n\n");

# ================================================================================
# certificate JSON assembly
# ================================================================================
ShadowToJsonL := function(sh)
  local fw, ft, kcertStr;
  fw := WordToJson(sh.word);
  ft := JArr([ JPair(sh.triple[1][1], sh.triple[1][2]),
               JPair(sh.triple[2][1], sh.triple[2][2]),
               JPair(sh.triple[3][1], sh.triple[3][2]) ]);
  kcertStr := "{\"type\":\"brute\",\"expected_kernel_index\":17496}";
  return Concatenation("{\"m\":", String(sh.m), ",\"f_word\":", fw, ",\"f_triple\":", ft,
                        ",\"kernel_cert\":", kcertStr, "}");
end;;

shadowsJson := [];;
for sh in shadows do Add(shadowsJson, ShadowToJsonL(sh)); od;

ctJson := [];;
for cti in compTable do Add(ctJson, Concatenation("[",String(cti[1]),",",String(cti[2]),",",String(cti[3]),"]")); od;

imJson := [];;
for imi in invMap do Add(imJson, Concatenation("[",String(imi[1]),",",String(imi[2]),"]")); od;

redImgStr := [];;
for i in redImages do Add(redImgStr, String(i)); od;
reductionJson := Concatenation("[{\"to\":\"K3\",\"image\":[", JoinC(redImgStr,","),
                                "],\"surjective\":", JB(redSurjective), "}]");

target := Concatenation(
  "{\"family\":\"general\",\"id\":\"L01\",",
  "\"construction\":{",
  "\"x_hat\":\"G3=(r,s,s) form (MakeGn(3)) on pts1-9; H3=X=(1,0,0) on pts10-36 (regular rep)\",",
  "\"y_hat\":\"G3=(rs,r,rs) form on pts1-9; H3=Y=(0,1,0) on pts10-36 (regular rep)\",",
  "\"point_count_deviation_note\":\"design text says 54 points (G3 on 1-27,H3 on 28-54); actual MakeGn(3) acts on 9 points not 27, so this cert uses 36 points (G3 on 1-9, H3 on 10-36) -- invariants (|G3|=108 etc) are unaffected, see script header\"",
  "},",
  "\"phi\":{\"desc\":\"x->((r,s,s),X), y->((rs,r,rs),Y), c->(1,1) (left action)\",\"q_order\":2916},",
  "\"invariants\":{\"index_PB3\":2916,\"index_B3\":17496,\"N_ord\":6,\"derived_order\":81}}");

counts := Concatenation(
  "{\"raw_candidates\":", String(rawCount), ",\"hexagon_pass\":", String(hexPass),
  ",\"charming_pass\":", String(charmPass), ",\"surjective_pass\":", String(surjPass),
  ",\"double_check_full_hexagon_fail\":", String(dblFail),
  ",\"kernel_cert_fail\":0,",
  "\"kernel_cert_note\":\"type=brute: GAP side records only the type/expected_kernel_index per design; the well-definedness brute-force check itself is delegated to crosscheck/ (not computed here)\"",
  "}");

lsWitnessNote := "\"ls_witness_note\":\"N/A: Thm 5.2 (5.1) kappaFn/witness formulas are dihedral-specific (Dih family); not applicable to family=general target L01. Field left as empty array per schema.\"";

s := Concatenation(
  "{\"schema\":\"gtsh-cert/v1\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/week3-L-explorer.g\",\"date\":\"2026-07-25\"},",
  "\"target\":", target, ",",
  "\"conventions\":{\"dn_element\":\"[a,e] = r^a s^e (G3 factor only, n=3)\",",
  "\"h3_element\":\"(a,b,e) in (Z/3)^3, X=(1,0,0), Y=(0,1,0), product (a,b,e)(a',b',e')=(a+a',b+b',e+e'+a*b') mod 3\",",
  "\"action\":\"left(rs = s のち r)\",",
  "\"f_word_alphabet\":\"x,y(c は不要 -- f in [Q_L,Q_L])\",",
  lsWitnessNote,
  "},",
  "\"shadows\":", JArr(shadowsJson), ",",
  "\"counts\":", counts, ",",
  "\"composition_table\":", JArr(ctJson), ",",
  "\"inverse_map\":", JArr(imJson), ",",
  "\"reduction\":", reductionJson, ",",
  "\"ls_witness\":[]",
  "}");

WriteFile("certificates/L01.v1.json", s);
Print("wrote certificates/L01.v1.json\n");

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");
QUIT;
