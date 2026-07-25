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

Print("week3-battery-common.g loaded.\n");
