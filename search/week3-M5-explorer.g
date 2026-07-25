# week3-M5-explorer.g -- explorer for M5 = K^(3) cap N5 = ker(phi_M) (Week 3, second general object)
#
# Usage: .\gap.ps1 search\week3-M5-explorer.g
#
# Design source (read in full before implementation, per commander instructions):
#   provenance/LEDGER.md 2026-07-25 "Week 3 続: M5 の宇宙の事前登録" entry (fixtures, cap, counts vocabulary note)
#   sol/sol_reply_04_week3_first_data.md P18-P20 / W24 (object choice, fixtures, withdrawal condition)
#   search/week3-L-explorer.g (machinery reused near-verbatim: MakeDn/MakeGn/AbstractProd/compOfFix/
#     DnElemToAE/JSON helpers/BFSWords/EvalWordQT/BuildQTGeneral/ParseK3Shadows -- all copied unchanged
#     below except where noted)
#   docs/wp2-transversal-model.md (12-rule Q x T table -- BuildQTGeneral already implements it with a
#     general phiC parameter, i.e. it is c-generic; L01 exercised it only with phiC=Identity since c
#     died there. This is the first object where phiC is a genuinely non-trivial element.)
#   docs/week1-定義ノート.md SS on 簡約 hexagon (Prop 3.4): (3.10)/(3.11) live entirely inside F2/N_F2
#     (the x,y-generated part) and do not reference c at all -- so the reduced-hexagon candidate
#     enumeration below is untouched by c being alive; only the QxT full-hexagon double-check ((3.3)(3.4),
#     via BuildQTGeneral with phiC=chat) actually exercises c != 1.
#
# ================================================================================
# DESIGN NOTE (own derivation, to be reported to commander): PB3 = F2 x <c> (c central, PB3/<c> = F2,
# and <x,y> is a normal complement to <c> -- standard fact for the pure braid group on 3 strands).
# phi_M restricted to F2 (i.e. built from xhat,yhat alone) already has full image G3 x C5 (order 540):
# its C5-projection is <t^2> = C5 (gcd(2,5)=1) and its G3-projection is G3 (order 108, as in the
# dihedral case); Goursat's lemma then forces the subdirect product <xhat,yhat> <= G3 x C5 to be the
# full external direct product, because the only common quotient of G3 (abelianization order 4, a
# 2-group) and the simple group C5 is trivial. Hence chat = (1, t) (t = C5-part of c) is automatically
# already inside <xhat,yhat>, and Q_M := Group(xhat,yhat) has order 540 with no need to separately
# adjoin chat as a generator for group-order purposes. We still build chat explicitly (identity on the
# G3 blocks, order-1 rotation on the C5 block) because it is needed as phiC for the QxT model below --
# this is exactly the "c survives" refinement flagged by the task (c is trivial in Q_L but not in Q_M).
# The reduced-hexagon enumeration (theta/tau, candidate loop) below only ever uses xhat/yhat/theta/tau,
# mirroring week3-L-explorer.g verbatim in structure -- this is justified because Prop 3.4's reduced
# hexagon (3.10)/(3.11) is a statement about F2/(M5 cap F2) alone, and F2/(M5 cap F2) is canonically
# isomorphic to Q_M = <xhat,yhat> via w |-> phi_M(w,c^0) (kernel of the restricted map is exactly
# M5 cap F2 by construction). c only re-enters at the full-hexagon QxT double-check stage, via phiC.
# ================================================================================

SizeScreen([4096, 0]);;
startTime := Runtime();;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ================= basic helpers (copied verbatim from week3-L-explorer.g / suite-wp2-shard-a.g) =================
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

# ================= Q x T (transversal-cocycle) model, generalized to any Q (copied verbatim) =================
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

# ================= hand-written minimal string scanner (K3.v1.json reduction target, copied verbatim) =================
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
# Build G3 = MakeGn(3) (order 108, on points 1-9) and C5 (order 5, on points 10-14)
# ================================================================================
gn := MakeGn(3);;
Print("G3 = MakeGn(3): |G3| = ", Size(gn.G), " (expect 108)\n");

tPerm := PermList(Concatenation([2..5],[1]));;
if Order(tPerm) <> 5 then
  Error("C5 fixture FAILED: Order(tPerm) = ", Order(tPerm), ", expected 5");
fi;
Print("[", PF(true), "] C5 fixture: Order(t) = 5\n");

# shift a 5-point permutation onto points 10..14
ShiftC5 := function(p) return PermList(Concatenation(List([1..9],j->j), List([1..5], j -> 9 + (j^p)))); end;;

# ---- Q_M construction on 14 points: G3 on 1-9, C5 on 10-14 ----
# x -> ((r,s,s), t^2), y -> ((rs,r,rs), t^2), c -> ((1,1,1), t)
xhat := gn.x * ShiftC5(tPerm^2);;
yhat := gn.y * ShiftC5(tPerm^2);;
chat := ShiftC5(tPerm);;   # identity on points 1-9 (gn.x/gn.y not involved), rotation on 10-14

# sanity: xhat/yhat/chat act disjointly on the two blocks by construction; confirm chat is identity on 1-9
if compOfFix(chat, 1, 9) <> () then
  Error("chat fixture FAILED: chat must act as identity on points 1-9 (G3 block)");
fi;
Print("[", PF(true), "] chat fixture: identity on G3 block (points 1-9)\n");

QM := Group(xhat, yhat);;

# ---- fixture self-checks (W24: five fixtures; any failure -> stop before enumeration) ----
fixtureOK := true;;

qmSize := Size(QM);;
if qmSize <> 540 then
  fixtureOK := false;
  Print("[", PF(false), "] |Q_M| = ", qmSize, ", expected 540\n");
else
  Print("[", PF(true), "] |Q_M| = ", qmSize, " (expect 540, = |PB3:M5|)\n");
fi;

# chat must already lie in <xhat,yhat> per the design-note Goursat argument above
if fixtureOK and not (chat in QM) then
  fixtureOK := false;
  Print("[", PF(false), "] chat not in Group(xhat,yhat) -- Goursat argument in header is wrong\n");
elif fixtureOK then
  Print("[", PF(true), "] chat in Group(xhat,yhat) (confirms Q_M = G3 x C5 full direct product)\n");
fi;

indexB3 := 6 * qmSize;;
if indexB3 <> 3240 then
  fixtureOK := false;
  Print("[", PF(false), "] |B3:M5| = 6*|Q_M| = ", indexB3, ", expected 3240\n");
else
  Print("[", PF(true), "] |B3:M5| = ", indexB3, " (expect 3240)\n");
fi;

M5ord := Lcm(Order(xhat), Order(yhat));;
if M5ord <> 30 then
  fixtureOK := false;
  Print("[", PF(false), "] M5_ord = Lcm(Order(xhat),Order(yhat)) = ", M5ord, ", expected 30\n");
else
  Print("[", PF(true), "] M5_ord = ", M5ord, " (expect 30)\n");
fi;

DQM := DerivedSubgroup(QM);;
derivedOrder := Size(DQM);;
if derivedOrder <> 27 then
  fixtureOK := false;
  Print("[", PF(false), "] |[Q_M,Q_M]| = ", derivedOrder, ", expected 27\n");
else
  Print("[", PF(true), "] |[Q_M,Q_M]| = ", derivedOrder, " (expect 27)\n");
fi;

XM := Filtered([0..M5ord-1], mm -> Gcd(2*mm+1,M5ord) = 1);;
rawExpected := Length(XM) * derivedOrder;;
if Length(XM) <> 16 then
  fixtureOK := false;
  Print("[", PF(false), "] |X_M| = ", Length(XM), ", expected 16\n");
else
  Print("[", PF(true), "] |X_M| = ", Length(XM), " (expect 16)\n");
fi;
if rawExpected <> 432 then
  fixtureOK := false;
  Print("[", PF(false), "] charming母集合 = |X_M|*derived = ", rawExpected, ", expected 432\n");
else
  Print("[", PF(true), "] charming母集合 = ", rawExpected, " (expect 432 = 16*27)\n");
fi;

if not fixtureOK then
  Print("\n[UNKNOWN] W24: fixture self-check FAILED (at least one of the five fixtures did not match).\n");
  Print("列挙へ進まず停止する(silent cap 禁止・事前登録どおり)。\n");
fi;

if fixtureOK then

Print("\n全 fixture 自己検査 PASS (5/5). 実装続行.\n\n");

# ================================================================================
# Enumeration (reduced hexagon inside Q_M, mirrors week3-L-explorer.g's ProcessDihedral-style loop)
# reduced hexagon (Prop 3.4, (3.10)/(3.11)) lives inside F2/(M5 cap F2) = Q_M (x,y only) -- c not used here.
# ================================================================================
qmrec := rec(x := xhat, y := yhat, G := QM);;

zM := AbstractProd([xhat, yhat])^-1;;
thetaHom := GroupHomomorphismByImages(QM, QM, [xhat,yhat], [yhat,xhat]);;
tauHom := GroupHomomorphismByImages(QM, QM, [xhat,yhat], [yhat,zM]);;
if thetaHom = fail or tauHom = fail then
  Error("theta/tau homomorphism construction failed for Q_M");
fi;

t0 := Runtime();;
bfs := BFSWords(qmrec);;
t1 := Runtime();;
Print("BFS over Q_M: covered ", Length(bfs.elements), " elements (expect 540), time_ms=", t1-t0, "\n");
if Length(bfs.elements) <> Size(QM) then
  Error("BFS did not cover full Q_M: covered=", Length(bfs.elements), " expected=", Size(QM));
fi;

Dwords := [];;
for elt in bfs.elements do
  if elt in DQM then Add(Dwords, rec(elt:=elt, word:=LookupDictionary(bfs.wordOf, elt))); fi;
od;
Print("Dwords (candidates f in [Q_M,Q_M]): ", Length(Dwords), " (expect 27)\n");

rawCount := 0;;  hexPass := 0;;  charmPass := 0;;  surjPass := 0;;  shadows := [];;
t0 := Runtime();;
for cand in Dwords do
  f := cand.elt;
  for m in XM do
    rawCount := rawCount + 1;
    u := 2*m+1;
    thetaf := Image(thetaHom, f);
    hex310 := AbstractProd([f, thetaf]) = Identity(QM);
    ymf := AbstractProd([yhat^m, f]);
    tauymf := Image(tauHom, ymf);
    tau2ymf := Image(tauHom, tauymf);
    hex311 := AbstractProd([tau2ymf, tauymf, ymf]) = Identity(QM);
    if hex310 and hex311 then
      hexPass := hexPass + 1;
      charmPass := charmPass + 1;   # f in [Q_M,Q_M] by construction -> charming holds
      genA := xhat^u;
      genB := AbstractProd([f^-1, yhat^u, f]);
      surj := Size(Group(genA, genB)) = Size(QM);
      if surj then
        surjPass := surjPass + 1;
        Add(shadows, rec(m:=m, f:=f, word:=cand.word));
      fi;
    fi;
  od;
od;
t1 := Runtime();;
Print("reduced hexagon + surjective enumeration: time_ms=", t1-t0, "\n");
Print("counts: raw_candidates(=母集合/pre_hex_charming)=", rawCount, " hexagon_pass=", hexPass,
      " charming_pass=", charmPass, " surjective_pass=", surjPass, "\n");
if rawCount <> 432 then
  Print("  [ANOMALY] raw_candidates = ", rawCount, ", design expected 432 (16 x 27)\n");
fi;

# ================================================================================
# Full hexagon double-check on Q_M x T model (3240 points) -- c genuinely alive here (phiC = chat)
# ================================================================================
t0 := Runtime();;
qt := BuildQTGeneral(QM, xhat, yhat, chat);;
t1 := Runtime();;
Print("Q_M x T model built: np=", qt.np, " total_points=", 6*qt.np, " time_ms=", t1-t0, "\n");
qt.xx := qt.s1^2;;  qt.yy := qt.s2^2;;  qt.cc := (qt.s1*qt.s2*qt.s1)^2;;

if not (qt.s1*qt.s2*qt.s1 = qt.s2*qt.s1*qt.s2) then
  Error("QxT braid relation failed for M5");
fi;
Print("[", PF(true), "] QxT braid relation s1 s2 s1 = s2 s1 s2 holds\n");

t0 := Runtime();;
qtGroupSize := Size(Group(qt.s1, qt.s2));;
t1 := Runtime();;
Print("Size(<s1,s2>) = ", qtGroupSize, " (expect 3240), time_ms=", t1-t0, "\n");
if qtGroupSize <> 3240 then
  Error("QxT |<s1,s2>| mismatch for M5: got ", qtGroupSize, ", expected 3240");
fi;

# independent self-check of qt.cc: Delta^2 = c should act on QxT as "right-mult by phiC, block-diagonal
# across all 6 T-blocks, T-coordinate fixed" -- build that permutation independently (without reusing
# BuildQTGeneral's internal loop) and compare.
ccExpected := [];;
for tt in [1..6] do
  for i in [1..qt.np] do
    Add(ccExpected, (tt-1)*qt.np + qt.posOf(qt.elts[i]*chat));
  od;
od;
ccExpected := PermList(ccExpected);;
if qt.cc <> ccExpected then
  Error("QxT c-component self-check FAILED for M5: (s1 s2 s1)^2 != block-diagonal right-mult-by-chat");
fi;
Print("[", PF(true), "] QxT cc = (s1 s2 s1)^2 = block-diagonal right-mult-by-chat (independent self-check)\n");
if qt.cc = () then
  Print("  [ANOMALY] qt.cc is the identity -- c should be alive (order 5) in Q_M, contradicts design\n");
else
  Print("  Order(qt.cc) = ", Order(qt.cc), " (expect 5 -- c is alive)\n");
fi;

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
# composition_table (3.53) and inverse_map (3.54), generalized to Q_M / M5_ord=30
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
    Ehom := GroupHomomorphismByImages(QM, QM, [xhat,yhat], [imgx,imgy]);
    if Ehom = fail then
      Print("  [ANOMALY] E_{m1,f1} hom construction failed i1=", i1, "\n");
      continue;
    fi;
    newm := (2*m1*m2 + m1 + m2) mod M5ord;
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
  uinv := Gcdex(u1, M5ord).coeff1 mod M5ord;
  mtilde := ((-uinv*m1) mod M5ord);
  imgx := xhat^u1;
  imgy := AbstractProd([f1^-1, yhat^u1, f1]);
  Ehom := GroupHomomorphismByImages(QM, QM, [xhat,yhat], [imgx,imgy]);
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
# M5_ord=30, K3_ord=6, 6 | 30 -> new_m := m mod 6 satisfies 2*new_m+1 = 2m+1 (mod 6) automatically.
# ================================================================================
k3Shadows := ParseK3Shadows("certificates/K3.v1.json");;
Print("Parsed K3.v1.json: ", Length(k3Shadows), " shadows (expect 12)\n");
if Length(k3Shadows) <> 12 then
  Print("  [ANOMALY] K3.v1.json shadow count parsed as ", Length(k3Shadows), ", expected 12\n");
fi;

redImages := [];;  redSeen := [];;
for sh in shadows do
  newm := sh.m mod 6;
  idx := fail;
  for t in [1..Length(k3Shadows)] do
    if k3Shadows[t].m = newm and k3Shadows[t].triple = sh.triple then idx := t; break; fi;
  od;
  if idx = fail then
    Print("  [ANOMALY] reduction M5->K3: shadow (m=", sh.m, ", reduced_m=", newm, ", triple=", sh.triple, ") has no image in K3!\n");
    Add(redImages, -1);
  else
    Add(redImages, idx-1);
    if not (idx in redSeen) then Add(redSeen, idx); fi;
  fi;
od;
redSurjective := Length(redSeen) = Length(k3Shadows);;
Print("reduction M5 -> K3: images=", redImages, "  surjective=", redSurjective,
      "  (covered ", Length(redSeen), " of ", Length(k3Shadows), " K3 shadows)\n");

Print("\n|GT(M5)| = ", Length(shadows), "\n");
Print("累計 elapsed ms: ", Runtime()-startTime, "\n\n");

# ================================================================================
# certificate JSON assembly
# ================================================================================
ShadowToJsonM := function(sh)
  local fw, ft, kcertStr;
  fw := WordToJson(sh.word);
  ft := JArr([ JPair(sh.triple[1][1], sh.triple[1][2]),
               JPair(sh.triple[2][1], sh.triple[2][2]),
               JPair(sh.triple[3][1], sh.triple[3][2]) ]);
  kcertStr := "{\"type\":\"brute\",\"expected_kernel_index\":3240}";
  return Concatenation("{\"m\":", String(sh.m), ",\"f_word\":", fw, ",\"f_triple\":", ft,
                        ",\"kernel_cert\":", kcertStr, "}");
end;;

shadowsJson := [];;
for sh in shadows do Add(shadowsJson, ShadowToJsonM(sh)); od;

ctJson := [];;
for cti in compTable do Add(ctJson, Concatenation("[",String(cti[1]),",",String(cti[2]),",",String(cti[3]),"]")); od;

imJson := [];;
for imi in invMap do Add(imJson, Concatenation("[",String(imi[1]),",",String(imi[2]),"]")); od;

redImgStr := [];;
for i in redImages do Add(redImgStr, String(i)); od;
reductionJson := Concatenation("[{\"to\":\"K3\",\"image\":[", JoinC(redImgStr,","),
                                "],\"surjective\":", JB(redSurjective), "}]");

target := Concatenation(
  "{\"family\":\"general\",\"id\":\"M01\",",
  "\"construction\":{",
  "\"x_hat\":\"G3=(r,s,s) form (MakeGn(3)) on pts1-9; C5=t^2 on pts10-14\",",
  "\"y_hat\":\"G3=(rs,r,rs) form on pts1-9; C5=t^2 on pts10-14\",",
  "\"c_hat\":\"identity on pts1-9 (G3); C5=t on pts10-14 -- c survives (order 5), unlike L01 where c maps to 1\"",
  "},",
  "\"phi\":{\"desc\":\"x->((r,s,s),t^2), y->((rs,r,rs),t^2), c->((1,1,1),t) (left action)\",\"q_order\":540},",
  "\"invariants\":{\"index_PB3\":540,\"index_B3\":3240,\"N_ord\":30,\"derived_order\":27}}");

counts := Concatenation(
  "{\"raw_candidates\":", String(rawCount), ",\"hexagon_pass\":", String(hexPass),
  ",\"charming_pass\":", String(charmPass), ",\"surjective_pass\":", String(surjPass),
  ",\"double_check_full_hexagon_fail\":", String(dblFail),
  ",\"kernel_cert_fail\":0,",
  "\"kernel_cert_note\":\"type=brute: GAP side records only the type/expected_kernel_index per design; the well-definedness brute-force check itself is delegated to crosscheck/ (not computed here; this run does not touch crosscheck/)\"",
  "}");

lsWitnessNote := "\"ls_witness_note\":\"N/A: Thm 5.2 (5.1) kappaFn/witness formulas are dihedral-specific (Dih family); not applicable to family=general target M01. Field left as empty array per schema.\"";

rawFieldNote := "\"raw_candidates_field_note\":\"field name kept as raw_candidates for backward compatibility with existing crosscheck/ and L01; its semantic meaning is pre_hex_charming (母集合 before the reduced-hexagon+charming filter) per Sol 便04 P27 -- rename deferred to a checker-update pass, per task instruction\"";

s := Concatenation(
  "{\"schema\":\"gtsh-cert/v1\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/week3-M5-explorer.g\",\"date\":\"2026-07-25\"},",
  "\"target\":", target, ",",
  "\"conventions\":{\"dn_element\":\"[a,e] = r^a s^e (G3 factor only, n=3)\",",
  "\"c5_element\":\"t^k in Z/5, x,y の C5 成分 = t^2, c の C5 成分 = t^1\",",
  "\"action\":\"left(rs = s のち r)\",",
  "\"f_word_alphabet\":\"x,y(c は不要 -- f in [Q_M,Q_M])\",",
  lsWitnessNote, ",",
  rawFieldNote,
  "},",
  "\"shadows\":", JArr(shadowsJson), ",",
  "\"counts\":", counts, ",",
  "\"composition_table\":", JArr(ctJson), ",",
  "\"inverse_map\":", JArr(imJson), ",",
  "\"reduction\":", reductionJson, ",",
  "\"ls_witness\":[]",
  "}");

WriteFile("certificates/M01.v1.json", s);
Print("wrote certificates/M01.v1.json\n");

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");

fi; # fixtureOK

QUIT;
