#############################################################################
## drophunt_checker_producer_v1.g
##
## General-purpose raw-fibre producer for scratchpad/fib_ruling_and_fibre_checker_spec_v1.md
## SS2 (fibre checker spec, ruling 1720/1722). PRODUCER side (GAP). Independent
## checker is search/drophunt_checker_v1.py (Python, standard library only, does
## NOT import this file or its helpers -- reads only this script's JSON receipts).
##
## Scope: windows K := M cap L for L a LINS(B3,<=N) node (roof M = K^(9) cap N_S4,
## fixed compact model PB3/M = G9 x PSL(2,8), order 1,469,664, degree 36). Any
## seed [m_seed, f_seed] with m_seed given mod M_ord=18 and f_seed given as a
## signed x/y letter word (code convention: 1=x, -1=x^-1, 2=y, -2=y^-1, per
## scratchpad/d972_idx3_arith_datum_independent_v1.md SS11.2 and the existing
## d972 word-key artifact).
##
## F1-F5 budget (spec SS2.1), evaluated BEFORE enumeration:
##   F1 = K_ord/M_ord (integrality enforced, fail-closed if not)
##   F2 = [M_F2:K_F2]  (= Size(joint F2 image G)/1,469,664)
##   F3 = F1*F2  (#fib(K), corrected formula per ruling 1720)
##   F4 = K^diamond=K (isolated) -- NOT evaluated here (out of scope for this
##        calibration pass; only needed to RECORD positive verdicts per spec
##        2.0's warning, not to compute NO_LIFT verdicts)
##   F5 = |F2/K_F2| = Size(G) (recorded)
##
## Predicate order (spec SS2.3), per raw candidate (m',f'), SHORT-CIRCUIT on
## first failure (does not change CC-1 candidate-coverage bookkeeping -- every
## candidate still gets a verdict row, just with fewer stages evaluated):
##   1. charming: gcd(2m'+1,K_ord)=1  AND  f' in DerivedSubgroup(F2/K_F2)
##   2. hexagon (3.10): f'*theta(f') = 1   [WORD-LEVEL theta, then eval in quotient]
##      hexagon (3.11): tau^2(y^m'f')*tau(y^m'f')*(y^m'f') = 1  [WORD-LEVEL tau]
##   3. onto: <x^(2m'+1), f'^-1 y^(2m'+1) f'> = F2/K_F2
##   4. reduction-match: m' mod M_ord = m_seed  AND  f' mod M_F2 = f_seed
##      (sanity re-confirmation; true by construction of the raw roster, so a
##      failure here indicates a PRODUCER BUG, not a genuine predicate result --
##      treated as fail-closed Error(), not a silent FAIL verdict)
##
## Raw candidate generation (spec F1/F2 freedoms, independent of the predicate):
##   m' ranges over {m_seed + M_ord*t : t=0..F1-1}
##   f' ranges over the coset {g in G : pi0(g)=pi0(f_seed)} where
##     pi0: G=F2/K_F2 -> Group(MX,MY)=F2/M_F2 is the M-block projection
##     (a genuine group homomorphism because G is built as a block-direct-sum
##     permutation representation: MX,MY act on points [1..36], the L-part acts
##     on points [37..36+deg(L)], and G=<JX,JY> where JX,JY are exactly the
##     block-diagonal direct sums of (MX,Xp) and (MY,Yp) -- so the "restrict to
##     block [1..36]" map is automatically a homomorphism, independent of which
##     subgroup of the full direct product G actually is).
##     H := Kernel(pi0), |H|=F2 (=[M_F2:K_F2]); coset = {f_seed_elt * h : h in H}.
##   Explicit WORDS for coset elements are obtained via
##   GroupHomomorphismByImagesNC(FreeGroup(x,y), G, [JX,JY]) +
##   PreImagesRepresentative (standard GAP free-group-preimage machinery, exact,
##   no BFS/enumeration of G itself -- G can be large (millions) while F2
##   (=|H|, the coset size) stays small for the cheap windows this pass targets).
#############################################################################

Read("search/probe/wac_v1/gap_output_prelude.g");;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

DCPOutDir := "search/certs/";;

DCPShiftPerm := function(p, offset, size)
  local images, j;
  images := [1..offset+size];
  for j in [1..size] do images[offset+j] := offset + (j^p); od;
  return PermList(images);
end;;
DCPDirectSumPerm := function(p, psize, q, qsize)
  return p * DCPShiftPerm(q, psize, qsize);
end;;
DCPPermDegree := function(G)
  local d;
  d := LargestMovedPoint(G);;
  if d = 0 then return 1; fi;
  return d;
end;;

#############################################################################
## Fixed roof M model (identical construction to lins_marked_strictness_export_v1.g)
#############################################################################
DCPG9Rec := MakeGn(9);;
if Size(DCPG9Rec.G) <> 2916 then Error("DCP: G9 order drift"); fi;
CheckGF8();;
DCPSMat := MakeMatGF8(1,0,1,1);; DCPTMat := MakeMatGF8(4,3,1,5);;
DCPSPerm := MatToPermGF8(DCPSMat);; DCPTPerm := MatToPermGF8(DCPTMat);;
DCPWPerm := DCPSPerm * DCPTPerm^-1;; DCPX4 := DCPWPerm^2;;
DCPY4 := DCPSPerm^-1 * DCPX4 * DCPSPerm;;
DCPP4 := Group(DCPX4, DCPY4);;
if Size(DCPP4) <> 504 then Error("DCP: PSL(2,8) order drift"); fi;
DCPMX := DCPDirectSumPerm(DCPG9Rec.x, 27, DCPX4, 9);;
DCPMY := DCPDirectSumPerm(DCPG9Rec.y, 27, DCPY4, 9);;
DCPMDegree := 36;;
DCPMBlock := Group(DCPMX, DCPMY);;
if Size(DCPMBlock) <> 1469664 then Error("DCP: PB3/M order drift"); fi;
DCPOrdMX := Order(DCPMX);; DCPOrdMY := Order(DCPMY);;
DCPMOrd := Lcm(DCPOrdMX, DCPOrdMY);;
if DCPMOrd <> 18 then Error("DCP: M_ord drift, expected 18 got ", DCPMOrd); fi;

DCPF := FreeGroup("a", "b");;
DCPa := DCPF.1;; DCPb := DCPF.2;;
DCPRel := DCPa * DCPb * DCPa * (DCPb * DCPa * DCPb)^-1;;
DCPB3 := DCPF / [DCPRel];;
DCPs1 := DCPB3.1;; DCPs2 := DCPB3.2;;

#############################################################################
## Seeds (row 36 = g*, Mode A; row 71, Mode B). Code convention 1=x,-1=x^-1,
## 2=y,-2=y^-1 (d972 doc SS11.2 / word-key artifact). m_seed=0 for both.
#############################################################################
DCPCodeToLetter := function(c)
  if c = 1 then return ["x",1];
  elif c = -1 then return ["x",-1];
  elif c = 2 then return ["y",1];
  elif c = -2 then return ["y",-1];
  else Error("DCP: bad letter code ", c); fi;
end;;
DCPWordToLetters := function(codes) return List(codes, DCPCodeToLetter); end;;

DCPSeeds := [
  rec(name:="row36", m_seed:=0,
    codes:=[-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1]),
  rec(name:="row71", m_seed:=0,
    codes:=[-1,-1,2,2,-1,-2,-1,-1,2,1,-2,1,1,2])
];;
for DCPSd in DCPSeeds do
  DCPSd.letters := DCPWordToLetters(DCPSd.codes);;
od;;

#############################################################################
## Free-group -> unit-letter-list conversion (mirrors WordFromFpElt pattern
## used elsewhere in this repo, e.g. search/koubou158_m2_hexagon_gen_v2.g,
## rewritten fresh here for this producer -- not imported/shared).
#############################################################################
DCPFreeEltToLetters := function(fpElt)
  local ext, out, i, gen, exp, letterName;
  ext := ExtRepOfObj(UnderlyingElement(fpElt));;
  out := [];;
  for i in [1,3..Length(ext)-1] do
    gen := ext[i];; exp := ext[i+1];;
    if gen = 1 then letterName := "x"; else letterName := "y"; fi;
    if exp > 0 then
      Append(out, List([1..exp], j -> [letterName,1]));
    else
      Append(out, List([1..-exp], j -> [letterName,-1]));
    fi;
  od;
  return out;
end;;

#############################################################################
## Build one window's joint model K := M cap L (L a LINS node already found),
## returning qrec with G, JX, JY, K_ord, M_ord, F2ratio, F3, pi0, H, epi.
#############################################################################
DCPBuildWindow := function(L)
  local hom, Q, iso, Qp, S1p, S2p, Xp, Yp, deg, JX, JY, G, kOrd, f2ratio, f3,
    pi0, H, freeF, fx, fy, epi;
  hom := NaturalHomomorphismByNormalSubgroup(DCPB3, L);;
  Q := Image(hom);;
  iso := IsomorphismPermGroup(Q);;
  Qp := Image(iso);;
  S1p := Image(iso, Image(hom, DCPs1));;
  S2p := Image(iso, Image(hom, DCPs2));;
  Xp := S1p^2;; Yp := S2p^2;;
  deg := DCPPermDegree(Qp);;
  JX := DCPDirectSumPerm(DCPMX, DCPMDegree, Xp, deg);;
  JY := DCPDirectSumPerm(DCPMY, DCPMDegree, Yp, deg);;
  G := Group(JX, JY);;
  kOrd := Lcm(Order(JX), Order(JY));;
  if kOrd mod DCPMOrd <> 0 then
    Error("DCP: K_ord not divisible by M_ord (K not<= M) -- fail-closed stop");
  fi;
  f2ratio := Size(G) / 1469664;;
  if not IsInt(f2ratio) then Error("DCP: F2 ratio nonintegral"); fi;
  f3 := (kOrd/DCPMOrd) * f2ratio;;
  pi0 := GroupHomomorphismByImages(G, DCPMBlock, [JX,JY], [DCPMX,DCPMY]);;
  if pi0 = fail then Error("DCP: M-block projection homomorphism ill-defined"); fi;
  H := Kernel(pi0);;
  if Size(H) <> f2ratio then Error("DCP: |H| != F2 ratio, got ", Size(H), " vs ", f2ratio); fi;
  freeF := FreeGroup("x","y");; fx := freeF.1;; fy := freeF.2;;
  epi := GroupHomomorphismByImagesNC(freeF, G, [fx,fy], [JX,JY]);;
  return rec(G:=G, JX:=JX, JY:=JY, degL:=deg, K_ord:=kOrd, M_ord:=DCPMOrd,
    F2:=f2ratio, F3:=f3, pi0:=pi0, H:=H, epi:=epi, D:=DerivedSubgroup(G));;
end;;

#############################################################################
## Mode A/B shared evaluator: given qrec (window) and a seed, produce the full
## F3-row verdict table. No early stop (same enumerator for both modes; the
## spec permits Mode A to stop at first LIFT_EXISTS but that optimization is
## not needed here since F3 is small for all calibration/cost targets).
#############################################################################
DCPEvalWindow := function(qrec, seed)
  local JFseed, target0, Hlist, cosetF, h, p, wp, mCands, t, rows, m, u,
    okCm, okCf, charming, thetaWord, hex310, yWordM, ymfWord, tauWord1,
    tauWord2, hex311, genA, genB, onto, redOk, verdict, row, stage,
    validCount, tRowStart, tRowElapsed;
  JFseed := EvalWordInQ(seed.letters, qrec.JX, qrec.JY, Identity(qrec.G));;
  target0 := Image(qrec.pi0, JFseed);;
  Hlist := Elements(qrec.H);;
  cosetF := [];;
  for h in Hlist do
    p := JFseed * h;;
    wp := DCPFreeEltToLetters(PreImagesRepresentative(qrec.epi, p));;
    Add(cosetF, rec(perm:=p, word:=wp));;
  od;;
  if Length(cosetF) <> qrec.F2 then Error("DCP: coset size mismatch"); fi;
  mCands := List([0..(qrec.K_ord/qrec.M_ord)-1], t -> seed.m_seed + qrec.M_ord*t);;
  rows := [];; validCount := 0;;
  for m in mCands do
    for h in cosetF do
      tRowStart := GAPLIB_WallElapsedMs();;
      p := h.perm;; wp := h.word;;
      u := 2*m+1;;
      okCm := Gcd(u, qrec.K_ord) = 1;;
      okCf := p in qrec.D;;
      charming := okCm and okCf;;
      stage := "charming_fail";;
      hex310 := false;; hex311 := false;; onto := false;; redOk := false;;
      if charming then
        thetaWord := ThetaWord(wp);;
        hex310 := EvalWordInQ(Concatenation(wp, thetaWord), qrec.JX, qrec.JY, Identity(qrec.G)) = Identity(qrec.G);;
        if hex310 then
          yWordM := List([1..m], ii -> ["y",1]);;
          ymfWord := Concatenation(yWordM, wp);;
          tauWord1 := TauWord(ymfWord);; tauWord2 := TauWord(tauWord1);;
          hex311 := EvalWordInQ(Concatenation(tauWord2, tauWord1, ymfWord), qrec.JX, qrec.JY, Identity(qrec.G)) = Identity(qrec.G);;
          if hex311 then
            genA := qrec.JX^u;; genB := p^-1 * qrec.JY^u * p;;
            onto := Size(Group(genA, genB)) = Size(qrec.G);;
            if onto then
              redOk := (m mod qrec.M_ord = seed.m_seed) and (Image(qrec.pi0, p) = target0);;
              if not redOk then
                Error("DCP: reduction-match FAILED on constructed candidate -- producer bug, fail-closed stop");
              fi;
              stage := "pass";;
            else
              stage := "onto_fail";;
            fi;
          else
            stage := "hex311_fail";;
          fi;
        else
          stage := "hex310_fail";;
        fi;
      fi;
      verdict := charming and hex310 and hex311 and onto and redOk;;
      if verdict then validCount := validCount + 1; fi;
      tRowElapsed := GAPLIB_WallElapsedMs() - tRowStart;;
      Add(rows, rec(m:=m, f_word_codes:=List(wp, function(l) if l[1]="x" then return l[2]; else return 2*l[2]; fi; end),
        charming:=charming, hex310:=hex310, hex311:=hex311, onto:=onto,
        reduction_match:=redOk, verdict:=verdict, stage:=stage, eval_ms:=tRowElapsed));;
    od;;
  od;;
  return rec(evaluated_count:=Length(rows), expected_count:=qrec.F3,
    valid_count:=validCount, rows:=rows);;
end;;

#############################################################################
## JSON emission helpers (row -> compact JSON)
#############################################################################
DCPRowJson := function(r)
  return Concatenation(
    "{\"m\":", String(r.m),
    ",\"f_word_codes\":", JArr(List(r.f_word_codes, String)),
    ",\"charming\":", JB(r.charming),
    ",\"hex310\":", JB(r.hex310),
    ",\"hex311\":", JB(r.hex311),
    ",\"onto\":", JB(r.onto),
    ",\"reduction_match\":", JB(r.reduction_match),
    ",\"verdict\":", JB(r.verdict),
    ",\"stage\":", JStr(r.stage),
    ",\"eval_ms\":", String(r.eval_ms), "}");;
end;;

DCPPermToJsonList := function(p, deg)
  return JArr(List([1..deg], j -> String(j^p)));;
end;;

DCPEmitReceipt := function(pathOut, meta, qrec, seedName, evalResult, totalMs)
  local rowsJson, out, deg;
  rowsJson := JoinC(List(evalResult.rows, DCPRowJson), ",\n");;
  deg := DCPMDegree + qrec.degL;;
  out := Concatenation(
    "{\n",
    "  \"schema\":\"drophunt-checker-producer/v1\",\n",
    "  \"status\":\"CANDIDATE_GAP_PRODUCER\",\n",
    "  \"verified\":false,\n",
    "  \"window\":{",
      "\"node_id\":", JStr(meta.node_id),
      ",\"b3_index_of_L\":", String(meta.b3_index),
      ",\"K_ord\":", String(qrec.K_ord),
      ",\"M_ord\":", String(qrec.M_ord),
      ",\"F1_m_factor\":", String(qrec.K_ord/qrec.M_ord),
      ",\"F2_ratio\":", String(qrec.F2),
      ",\"F3_fib\":", String(qrec.F3),
      ",\"F5_size_G\":", String(Size(qrec.G)),
      ",\"degree\":", String(deg),
      ",\"JX_one_line\":", DCPPermToJsonList(qrec.JX, deg),
      ",\"JY_one_line\":", DCPPermToJsonList(qrec.JY, deg), "},\n",
    "  \"seed\":", JStr(seedName), ",\n",
    "  \"cc1_candidate_coverage\":{",
      "\"evaluated_count\":", String(evalResult.evaluated_count),
      ",\"expected_count\":", String(evalResult.expected_count),
      ",\"match\":", JB(evalResult.evaluated_count = evalResult.expected_count), "},\n",
    "  \"valid_count\":", String(evalResult.valid_count), ",\n",
    "  \"total_elapsed_ms\":", String(totalMs), ",\n",
    "  \"reduction_index_order\":\"source_first\",\n",
    "  \"rows\":[\n", rowsJson, "\n  ]\n",
    "}\n");;
  WriteFile(pathOut, out);;
  return rec(path:=pathOut, bytes:=Length(out), sha256:=HexSHA256(out));;
end;;

Print("DCP_LOADED\n");;
