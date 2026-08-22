## scratchpad/canary_a2_decoder_check.g -- WARN-A2-1 discriminating canary A
## (mathematician instruction via commander message, 2026-08-22)
## Canary A: for every N-basis word (mach.basisWordsp, both windows, both p=2,3),
## compare the PRODUCER's ABGamma(a,b) (the exact function feeding AVecp/BVecp in
## koubou83_A2_48sweep_v2.g) against a FRESH, INDEPENDENTLY-CODED reimplementation
## of the strand-linking algorithm (written from scratch in this script, not calling
## ComputeLinking/ABGamma), in TWO conventions:
##   (raw)    : same convention as producer (no /2) -- catches CODING bugs.
##   (halved) : mathematician's referenced decoder convention (linking()/abg_sigma()
##              in scratchpad/c83_a2check_cond3_v1.py, c83_inn3_witness_decode_v1.py),
##              which expects EVEN per-pair sums and divides by 2 -- catches
##              CONVENTION mismatches (xy-doubled vs raw sigma-word units).
## Does NOT re-run the 48-shadow sweep (commander: "full re-run not needed").

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/iso_census83_deep15_data.g");

BF3 := FreeGroup("a","b");;
brel := BF3.1*BF3.2*BF3.1*BF3.2^-1*BF3.1^-1*BF3.2^-1;;
B3 := BF3/[brel];;
aB3 := B3.1;; bB3 := B3.2;;
a := aB3;; b := bB3;;

targets := [154161, 154163];;
seen := [];; reps := [];;
for r1 in DEEP15 do
  if r1.id[1] = 1152 and (r1.id[2] in targets) and not (r1.id in seen) then
    Add(seen, r1.id); Add(reps, r1);
  fi;
od;;

FreeReduce := function(w)
  local out, l;
  out := [];
  for l in w do
    if Length(out) > 0 and out[Length(out)] = -l then Remove(out, Length(out)); else Add(out, l); fi;
  od;
  return out;
end;;
InvWord := function(w) return List(Reversed(w), l -> -l); end;;
RepWord := function(w, k)
  local out, i;
  out := [];
  if k >= 0 then for i in [1..k] do Append(out, w); od;
  else for i in [1..(-k)] do Append(out, InvWord(w)); od; fi;
  return out;
end;;

PB_next := [ [2,3], [1,4], [5,1], [6,2], [3,6], [4,5] ];;
PB_valw := [ [ [], [] ], [ [1], [] ], [ [], [2] ], [ [], [-2,-1] ], [ [-1,-2], [] ], [ [2], [1] ] ];;
PB_valk := [ [0,0], [0,0], [0,0], [0,1], [1,0], [0,0] ];;
PBcoords := function(W)
  local i, accW, acck, l, letter, nexti, val, kx;
  i := 1;;  accW := [];;  acck := 0;;
  for l in W do
    letter := AbsInt(l);;
    if l > 0 then
      nexti := PB_next[i][letter];;  val := PB_valw[i][letter];;  kx := PB_valk[i][letter];;
      Append(accW, val);;  acck := acck + kx;;  i := nexti;;
    else
      nexti := PB_next[i][letter];;  val := PB_valw[nexti][letter];;  kx := PB_valk[nexti][letter];;
      Append(accW, InvWord(val));;  acck := acck - kx;;  i := nexti;;
    fi;
  od;
  if i <> 1 then Error("PBcoords: not in PB3"); fi;
  return [FreeReduce(accW), acck];;
end;;

## ---- PRODUCER's linking/ABGamma (verbatim copy from koubou83_A2_48sweep_v2.g) ----
ComputeLinking := function(sigmaWord)
  local perm, lk12, lk13, lk23, l, k, s, sA, sB, pr, tmp;
  perm := [1,2,3];;
  lk12 := 0;; lk13 := 0;; lk23 := 0;;
  for l in sigmaWord do
    k := AbsInt(l);;  s := SignInt(l);;
    sA := perm[k];;  sB := perm[k+1];;
    pr := Set([sA, sB]);;
    if pr = [1,2] then lk12 := lk12 + s;
    elif pr = [1,3] then lk13 := lk13 + s;
    elif pr = [2,3] then lk23 := lk23 + s;
    else Error("bad strand pair ", pr); fi;
    tmp := perm[k];;  perm[k] := perm[k+1];;  perm[k+1] := tmp;;
  od;
  return [lk12, lk13, lk23];;
end;;
ABGamma := function(sigmaWord)
  local lk;
  lk := ComputeLinking(sigmaWord);;
  return [lk[1]-lk[2], lk[3]-lk[2], lk[2]];;
end;;

## ---- FRESH INDEPENDENT reimplementation (written from scratch, different data
## structure: dictionary-of-pairs instead of perm-array + 3 scalars, to genuinely
## catch coding slips rather than re-deriving the same code path) ----
IndepLinking := function(sigmaWord)
  local pos, L, l, i, s, j, k, key, tmp, allEven;
  pos := [1,2,3];;
  L := rec( p12 := 0, p13 := 0, p23 := 0 );;
  for l in sigmaWord do
    i := AbsInt(l);;  s := SignInt(l);;
    j := pos[i];;  k := pos[i+1];;
    if (j=1 and k=2) or (j=2 and k=1) then L.p12 := L.p12 + s;
    elif (j=1 and k=3) or (j=3 and k=1) then L.p13 := L.p13 + s;
    elif (j=2 and k=3) or (j=3 and k=2) then L.p23 := L.p23 + s;
    else Error("IndepLinking: bad pair ", [j,k]); fi;
    tmp := pos[i];; pos[i] := pos[i+1];; pos[i+1] := tmp;;
  od;
  return rec(l12:=L.p12, l13:=L.p13, l23:=L.p23, finalPos:=pos);;
end;;
IndepABGammaRaw := function(sigmaWord)
  local lk;
  lk := IndepLinking(sigmaWord);;
  return [lk.l12-lk.l13, lk.l23-lk.l13, lk.l13];;
end;;
## ---- run canary A over every window's basis words, both primes ----
totalWords := 0;;  rawMismatch := 0;;  oddCount := 0;;  halvedMatch := 0;;  halvedMismatch := 0;;
detailLines := [];;

for r1 in reps do
  Print("\n### WINDOW ", r1.id, " ###\n");
  gens := List(r1.words, w -> EvalString(w));;
  N := Subgroup(B3, gens);;
  hm := NaturalHomomorphismByNormalSubgroup(B3, N);;
  iso := IsomorphismPermGroup(Image(hm));;
  s1 := Image(iso, Image(hm, aB3));;  s2 := Image(iso, Image(hm, bB3));;
  Bq := Group(s1,s2);;
  x := s1^2;;  y := s2^2;;  c := (s1*s2*s1)^2;;
  PN := Group(x,y);;
  Els := Elements(PN);;  nn := Length(Els);;
  posOf := function(g) return Position(Els, g); end;;

  if r1.id[2] = 154161 then m0xy := [-1,-1,-1,-1,-1,-1];;
  else m0xy := RepWord([-1,-2], 3);; fi;
  evXY := function(w, xelt, yelt)
    local acc, l;
    acc := xelt^0;;
    for l in w do
      if l=1 then acc := acc*xelt; elif l=-1 then acc := acc*xelt^-1;
      elif l=2 then acc := acc*yelt; elif l=-2 then acc := acc*yelt^-1;
      else Error("bad xy letter ", l); fi;
    od;
    return acc;;
  end;;

  BuildBasisOnly := function(p)
    local onep, zerop, negonep, Foxp, Dmat, i, KDp, cinv, Pmat, imgUp, rankUp,
          PhiMapp, RankTrackerAddp, pivotsUp, uv, RedVecp, pivotsFullp, basisWordsp,
          basisVecsp, wstr, sw, fw, phiv, fullvec, before;
    onep := One(GF(p));;  zerop := Zero(GF(p));;  negonep := -onep;;
    Foxp := function(w)
      local Dx, Dy, pre, l;
      Dx := List([1..nn], ii->zerop);;  Dy := List([1..nn], ii->zerop);;
      pre := Identity(PN);;
      for l in w do
        if l = 1 then Dx[posOf(pre)] := Dx[posOf(pre)] + onep;  pre := pre*x;
        elif l = -1 then pre := pre*x^-1;  Dx[posOf(pre)] := Dx[posOf(pre)] + negonep;
        elif l = 2 then Dy[posOf(pre)] := Dy[posOf(pre)] + onep;  pre := pre*y;
        elif l = -2 then pre := pre*y^-1;  Dy[posOf(pre)] := Dy[posOf(pre)] + negonep;
        else Error("bad xy letter ", l); fi;
      od;
      return Concatenation(Dx, Dy);;
    end;;
    Dmat := NullMat(2*nn, nn, GF(p));;
    for i in [1..nn] do
      Dmat[i][posOf(Els[i]*x)] := Dmat[i][posOf(Els[i]*x)] + onep;
      Dmat[i][i] := Dmat[i][i] + negonep;
      Dmat[nn+i][posOf(Els[i]*y)] := Dmat[nn+i][posOf(Els[i]*y)] + onep;
      Dmat[nn+i][i] := Dmat[nn+i][i] + negonep;
    od;;
    KDp := NullspaceMat(Dmat);;
    cinv := c^-1;;
    Pmat := NullMat(2*nn, 2*nn, GF(p));;
    for i in [1..nn] do
      Pmat[i][posOf(cinv*Els[i])] := onep;;
      Pmat[nn+i][nn+posOf(cinv*Els[i])] := onep;;
    od;;
    imgUp := List(KDp, v -> v*Pmat - v);;
    rankUp := RankMat(imgUp);;
    PhiMapp := function(sigmaWord)
      local coords, w, k, mword, ev;
      coords := PBcoords(sigmaWord);;
      w := coords[1];;  k := coords[2];;
      mword := FreeReduce(Concatenation(w, RepWord(m0xy, -k)));;
      ev := evXY(mword, x, y);;
      if ev <> Identity(PN) then Error("PhiMapP BOOKKEEPING-FAIL"); fi;
      return [Foxp(mword), k mod p];;
    end;;
    RankTrackerAddp := function(pivots, vec)
      local v, col, pp;
      v := ShallowCopy(vec);;
      for pp in pivots do
        col := pp[1];;
        if v[col] <> zerop then v := v - v[col]/pp[2][col] * pp[2]; fi;
      od;
      col := PositionNonZero(v);;
      if col <= Length(v) then Add(pivots, [col, v]); fi;
      return pivots;;
    end;;
    pivotsUp := [];;
    for uv in imgUp do pivotsUp := RankTrackerAddp(pivotsUp, Concatenation(uv, [zerop])); od;;
    pivotsFullp := ShallowCopy(pivotsUp);;
    basisWordsp := [];;  basisVecsp := [];;
    for wstr in r1.words do
      sw := EvalString(wstr);;
      fw := LetterRepAssocWord(UnderlyingElement(PreImagesRepresentative(
              EpimorphismFromFreeGroup(B3 : names:=["a","b"]), sw)));;
      phiv := PhiMapp(fw);;
      fullvec := Concatenation(phiv[1], [phiv[2]*onep]);;
      before := Length(pivotsFullp);;
      pivotsFullp := RankTrackerAddp(pivotsFullp, fullvec);;
      if Length(pivotsFullp) > before then Add(basisWordsp, fw);; Add(basisVecsp, fullvec);; fi;
    od;;
    return basisWordsp;;
  end;;

  for p in [2,3] do
    basisWordsp := BuildBasisOnly(p);;
    Print("  p=", p, "  dBasis=", Length(basisWordsp), "\n");
    for bw in basisWordsp do
      totalWords := totalWords + 1;;
      prodAB := ABGamma(bw);;
      indepRaw := IndepABGammaRaw(bw);;
      if prodAB <> indepRaw then
        rawMismatch := rawMismatch + 1;;
        Add(detailLines, Concatenation("RAW-MISMATCH window=", String(r1.id), " p=", String(p),
              " prod=", String(prodAB), " indep=", String(indepRaw), " word=", String(bw)));;
      fi;
      lk := IndepLinking(bw);;
      if lk.finalPos <> [1,2,3] or lk.l12 mod 2 <> 0 or lk.l13 mod 2 <> 0 or lk.l23 mod 2 <> 0 then
        oddCount := oddCount + 1;;
      else
        halvedAB := [ (lk.l12-lk.l13)/2, (lk.l23-lk.l13)/2, lk.l13/2 ];;
        if prodAB = 2*halvedAB then halvedMatch := halvedMatch + 1;;
        else
          halvedMismatch := halvedMismatch + 1;;
          Add(detailLines, Concatenation("HALVED-x2-MISMATCH window=", String(r1.id), " p=", String(p),
                " prod=", String(prodAB), " 2xhalved=", String(2*halvedAB), " word=", String(bw)));;
        fi;
      fi;
    od;
  od;
od;;

Print("\n===== CANARY A SUMMARY =====\n");
Print("total basis-word evaluations (both windows, both primes): ", totalWords, "\n");
Print("RAW convention (no /2) -- producer ABGamma vs fresh independent reimpl: mismatches=",
      rawMismatch, "  (0 mismatches means producer's core linking algorithm is coding-bug-free)\n");
Print("odd-lk-sum basis words (halved/xy-doubled convention NOT applicable): ", oddCount, " / ", totalWords, "\n");
Print("among EVEN-lk-sum basis words: producer == 2*halved(independent) : match=", halvedMatch,
      "  mismatch=", halvedMismatch, "\n");
Print("\n--- detail (first 20 mismatch lines, if any) ---\n");
for i in [1..Minimum(20,Length(detailLines))] do Print(detailLines[i], "\n"); od;

Print("\nCANARY_A_DONE\n");
