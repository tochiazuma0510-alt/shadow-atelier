## search/koubou83_m3_l2_check_v2.g (GHA 実行用コピー・原本 scratchpad/koubou83_m3_l2_check_v2.g)
## M3(E[4] レーン)独立照合 v2 -- 線形則版(仕様: scratchpad/koubou83_m3_l2_linear_spec_v1.md)。
## 段2(GHA venue)裁定: local(-o 2g / -o 384m 両方)で単一窓ですら 10 分 cap 超過・
## 原因はローカル機の空きメモリ枯渇(実測 8%程度)と特定・司令塔裁定によりGHAへ計算を移送。
## 発火: push-trigger touch commit(2026-08-23・裁定: workflow_dispatch は新規ワークフロー未登録のため不可)。
##
## 著者分離: 線形則(定理 PUSH・正準基底・A の値・自己検証例・5項目の行列語訳)の導出は
## 工房数学者(scratchpad/koubou83_m3_l2_linear_spec_v1.md、著者分離のため c83_m3_e4_lane_v1.md
## 未読で独立導出)。本スクリプトの実装(GAPコード化・実行・cert生成)は implementer。
## checker 自身は数学者の探索スクリプト scratchpad/m3_l2_probe_v*.g / m3_e4_field_numcheck_v1.py
## は未読・不使用(著者分離)。
##
## v1(scratchpad/koubou83_m3_l2_check_v1.g)との違い: 旧版は shadow 48個ごとに
## GroupHomomorphismByImages で degree-1152 permutation group 上に自己準同型を構築しており、
## これが実測で致命的に遅かった(単一 window ですら 10 分 cap 超・司令塔裁定によりこの経路は
## 深追いせず放棄)。本 v2 は仕様の定理 PUSH に従い、事前計算(§3・1回・数百ms級)の後は
## shadow ごとに coord(f) 1回(P^ab 内の離散対数、16通り総当たり)+2x2 行列演算のみで
## theta_bar を再構成する。GroupHomomorphismByImages は一切使わない。
##
## DIR: 判定の独立照合 / FRAME: B3-gentle 窓 x E[4]

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");

t0Global := GAPLIB_WallElapsedMs();;
Print("CKPT01 t0Global set t=", t0Global, "\n");

INPUT_DATA_SHA256    := "75905c604b83058ff6406f5c115bfa3325fd4424c98125750e49c2b76bbd35ec";;
INPUT_WBC_SHA256     := "aadf1afa5e1a171d10d0aa1f9657e823cad669b960e08da7b9e7618f2ea4f998";;
INPUT_GAPLIB_SHA256  := "f80eeeae71c4e39f8b3d62d997d18635f5ea8fb339a6d0578e834300ea4d4911";;
INPUT_PRELUDE_SHA256 := "2e4da671ad9d018be1bc6f2f387f0e1d597e87c2c0e807eef40aeef3b92deece";;
Print("CKPT02 constants set t=", GAPLIB_WallElapsedMs(), "\n");
SPEC_PATH := "scratchpad/koubou83_m3_l2_linear_spec_v1.md";;
SPEC_RAW := StringFile(SPEC_PATH);;
if SPEC_RAW = fail then Error("cannot read linear spec for sha256: ", SPEC_PATH); fi;
Print("CKPT03 SPEC_RAW read (len=", Length(SPEC_RAW), ") t=", GAPLIB_WallElapsedMs(), "\n");
SPEC_SHA256 := HexSHA256(SPEC_RAW);;
Print("CKPT04 SPEC_SHA256 computed t=", GAPLIB_WallElapsedMs(), "\n");
ERRATA_PATH := "scratchpad/koubou83_m3_l2_linear_spec_v1_1_errata.md";;
ERRATA_RAW := StringFile(ERRATA_PATH);;
if ERRATA_RAW = fail then Error("cannot read errata for sha256: ", ERRATA_PATH); fi;
ERRATA_SHA256 := HexSHA256(ERRATA_RAW);;
Print("CKPT04b ERRATA_SHA256 computed t=", GAPLIB_WallElapsedMs(), "\n");
SCRIPT_PATH := "search/koubou83_m3_l2_check_v2.g";;
SCRIPT_RAW := StringFile(SCRIPT_PATH);;
if SCRIPT_RAW = fail then Error("cannot read checker source for runtime SHA: ", SCRIPT_PATH); fi;
Print("CKPT05 SCRIPT_RAW read (len=", Length(SCRIPT_RAW), ") t=", GAPLIB_WallElapsedMs(), "\n");
SCRIPT_SHA256 := HexSHA256(SCRIPT_RAW);;
Print("CKPT06 SCRIPT_SHA256 computed t=", GAPLIB_WallElapsedMs(), "\n");

## ================= B3 = <a,b | aba=bab> setup (own lineage, reused verbatim) =================
BF3 := FreeGroup("a", "b");;
brelD := BF3.1*BF3.2*BF3.1*BF3.2^-1*BF3.1^-1*BF3.2^-1;;
B3 := BF3 / [brelD];;
ga := B3.1;;  gb := B3.2;;
a := ga;;  b := gb;;   # global bind for EvalString(word) -- DEEP15 words use bare a,b
Print("CKPT07 B3 built t=", GAPLIB_WallElapsedMs(), "\n");

## ================= W-1 semantic gate (FIXED 2026-08-23: evaluated in a window's PERMUTATION
## group, not the raw finitely-presented B3) =================
## Root cause of the GHA/local 10-min-cap stalls (localized via CKPT checkpoints, run
## 32617461891): the four identities below used to be evaluated on raw elements of B3 =
## BF3/[brelD] -- an INFINITE finitely-presented group. GAP's `=`/`<>` on fp-group elements
## solves the word problem via a generic method with no termination guarantee for this
## representation; it never returned within the 10-30 min caps (confirmed: CKPT07 "B3 built"
## fired at t=1ms, CKPT08 "W1_GATE pass" never fired). Every OTHER group-theoretic operation in
## this script (Index(B3,N), IsNormal(B3,N), NaturalHomomorphismByNormalSubgroup(B3,N) inside
## BuildWindowFromWords) was already fine -- those use Todd-Coxeter coset enumeration against a
## known finite-index subgroup, a different and well-optimized code path; confirmed correct by
## full-script grep, no other raw B3-element `=`/`<>`/Order call exists.
##
## Mathematical justification for moving the check into a window's permutation group (commander
## ruling 2026-08-23, ledger-recorded):
##  1. positivePass: f1*sigma2*f1^-1 = x^-1*sigma2*x, with f1=x^-1*y, y=sigma2^2, reduces by free
##     reduction alone to y*sigma2*y^-1 = sigma2 (power-commutativity) -- TRUE IN ANY QUOTIENT of
##     the free group, in particular in any window's permutation image. Checking it there loses
##     no information relative to checking it in the abstract B3.
##  2. formerRejected, noncentralPass are INEQUALITIES. Any inequality that holds in a quotient
##     also held in the group being quotiented (the converse can fail, but that direction is not
##     needed): if two elements are already distinct after collapsing more relations, they were
##     distinct before. So verifying the inequalities in a window's permutation group is at least
##     as conclusive as verifying them in B3 -- not merely "no weaker", genuinely load-bearing.
##  3. Fail-closed is preserved unconditionally: if either gate unexpectedly fails when evaluated
##     in the window's permutation group, this still aborts via Error() below -- no softening.
W1SemanticGate := function(s1, s2)
  local sigma2, x, y, f1, formerRawOrderError, correctLhs, correctRhs,
        formerLhs, positivePass, formerRejected, noncentralPass;
  sigma2 := s2;;  x := s1^2;;  y := s2^2;;
  f1 := x^-1 * y;;
  formerRawOrderError := y * x^-1;;
  correctLhs := f1 * sigma2 * f1^-1;;
  correctRhs := x^-1 * sigma2 * x;;
  formerLhs := formerRawOrderError * sigma2 * formerRawOrderError^-1;;
  positivePass := (correctLhs = correctRhs);;
  formerRejected := (formerLhs <> correctRhs);;
  noncentralPass := (correctRhs <> sigma2);;
  if not (positivePass and formerRejected and noncentralPass) then
    Error("W-1 semantic gate failed: positive=", positivePass,
          " former_rejected=", formerRejected, " noncentral=", noncentralPass);
  fi;
  return rec(gate_id := "W-1/noncommutative-B3/nu-1/v1",
             word_convention_id := "W-1/paper-product-to-raw-reversed/v1",
             evaluated_in := "window-1-permutation-group (fixed 2026-08-23, was raw fp-B3)",
             positive_identity_pass := positivePass,
             former_error_rejected := formerRejected,
             noncentral_fixture_pass := noncentralPass,
             overall_pass := positivePass and formerRejected and noncentralPass);;
end;;

BuildWindowFromWords := function(indexExpected, words)
  local genElts, N, idxOk, isNormal, hm, Gimg, isoQ, s1, s2;
  genElts := List(words, w -> EvalString(w));;
  N := Subgroup(B3, genElts);;
  idxOk := (Index(B3, N) = indexExpected);;
  isNormal := IsNormal(B3, N);;
  if not (idxOk and isNormal) then
    Error("BuildWindowFromWords: index/normality mismatch, idx_ok=", idxOk, " is_normal=", isNormal);
  fi;
  hm := NaturalHomomorphismByNormalSubgroup(B3, N);;
  Gimg := Image(hm);;
  isoQ := IsomorphismPermGroup(Gimg);;
  s1 := Image(isoQ, Image(hm, ga));;
  s2 := Image(isoQ, Image(hm, gb));;
  return rec(s1 := s1, s2 := s2);;
end;;

MakeWindow := function(s1, s2)
  local xx, yy, DD, dd, cc, zz;
  xx := s1^2;  yy := s2^2;
  DD := AbstractProd([s1, s2, s1]);  dd := AbstractProd([s1, s2]);
  cc := DD^2;  zz := AbstractProd([xx, yy])^-1;
  return rec(s1 := s1, s2 := s2, x := xx, y := yy, Dlt := DD, dlt := dd, c := cc, z := zz,
             Bq := Group(s1, s2), PN := Group(xx, yy),
             Nord := Lcm(Order(xx), Order(yy), Order(cc)));
end;;

TT := function(W, g) return AbstractProd([W.dlt, g, W.dlt^-1]); end;;
TH := function(W, g) return AbstractProd([W.Dlt, g, W.Dlt^-1]); end;;
RtOf := function(W, m, f)
  local Wd;
  Wd := AbstractProd([W.y^m, f]);
  return AbstractProd([TT(W, TT(W, Wd)), TT(W, Wd), Wd]);
end;;

CorrectedShadows := function(W, charmingSet)
  local out, f, m, u;
  out := [];
  for f in Elements(DerivedSubgroup(W.PN)) do
    if AbstractProd([f, TH(W, f)]) <> Identity(W.Bq) then continue; fi;
    for m in charmingSet do
      u := 2*m + 1;
      if RtOf(W, m, f) <> W.c^m then continue; fi;
      if Size(Group(W.x^u, AbstractProd([f^-1, W.y^u, f]))) <> Size(W.PN) then continue; fi;
      Add(out, [m, f]);
    od;
  od;
  return Set(out);
end;;

## ================= extract the 3 DEEP15 records (154161 x1, 154163 x2) =================
Print("CKPT09 before DEEP15 Read t=", GAPLIB_WallElapsedMs(), "\n");
Read("search/iso_census83_deep15_data.g");;
Print("CKPT10 DEEP15 Read done, len=", Length(DEEP15), " t=", GAPLIB_WallElapsedMs(), "\n");
if Length(DEEP15) <> 15 then Error("DEEP15 length != 15, got ", Length(DEEP15)); fi;

Rec154161 := First(DEEP15, r -> r.id = [1152, 154161]);;
Recs154163 := Filtered(DEEP15, r -> r.id = [1152, 154163]);;
if Rec154161 = fail then Error("record [1152,154161] not found in DEEP15"); fi;
if Length(Recs154163) <> 2 then Error("expected exactly 2 records for [1152,154163], got ", Length(Recs154163)); fi;
Print("CKPT11 records extracted t=", GAPLIB_WallElapsedMs(), "\n");

## ================= build window 1 EARLY so the W-1 gate can run in its (fast) permutation
## group instead of raw fp-B3 (see W1SemanticGate comment above for the fix rationale) =========
S154161 := BuildWindowFromWords(Rec154161.index, Rec154161.words);;
Print("CKPT11b S154161 built t=", GAPLIB_WallElapsedMs(), "\n");
Wwin154161 := MakeWindow(S154161.s1, S154161.s2);;
Print("CKPT11c Wwin154161 built, |PN|=", Size(Wwin154161.PN), " t=", GAPLIB_WallElapsedMs(), "\n");

W1_GATE := W1SemanticGate(S154161.s1, S154161.s2);;
if not W1_GATE.overall_pass then Error("W1_GATE overall_pass=false, aborting fail-closed"); fi;
Print("CKPT08 W1_GATE pass=", W1_GATE.overall_pass, " t=", GAPLIB_WallElapsedMs(), "\n");

## ================= mod-4 2x2 matrix / vector arithmetic (pure integers, no group theory) ======
DetMod4 := function(M) return (M[1][1]*M[2][2] - M[1][2]*M[2][1]) mod 4; end;;

MatMulMod4 := function(M1, M2)
  return [[ (M1[1][1]*M2[1][1] + M1[1][2]*M2[2][1]) mod 4, (M1[1][1]*M2[1][2] + M1[1][2]*M2[2][2]) mod 4 ],
          [ (M1[2][1]*M2[1][1] + M1[2][2]*M2[2][1]) mod 4, (M1[2][1]*M2[1][2] + M1[2][2]*M2[2][2]) mod 4 ]];;
end;;

MatAddMod4 := function(M1, M2)
  return [[ (M1[1][1]+M2[1][1]) mod 4, (M1[1][2]+M2[1][2]) mod 4 ],
          [ (M1[2][1]+M2[2][1]) mod 4, (M1[2][2]+M2[2][2]) mod 4 ]];;
end;;

MatSubMod4 := function(M1, M2)
  return [[ (M1[1][1]-M2[1][1]) mod 4, (M1[1][2]-M2[1][2]) mod 4 ],
          [ (M1[2][1]-M2[2][1]) mod 4, (M1[2][2]-M2[2][2]) mod 4 ]];;
end;;

MatVecMod4 := function(M, v)
  return [ (M[1][1]*v[1] + M[1][2]*v[2]) mod 4, (M[2][1]*v[1] + M[2][2]*v[2]) mod 4 ];;
end;;

VecAddMod4 := function(v1, v2) return [ (v1[1]+v2[1]) mod 4, (v1[2]+v2[2]) mod 4 ]; end;;
VecEqMod4  := function(v1, v2) return (v1[1] mod 4)=(v2[1] mod 4) and (v1[2] mod 4)=(v2[2] mod 4); end;;

MatEqMod4 := function(M1, M2)
  return (M1[1][1] mod 4) = (M2[1][1] mod 4) and (M1[1][2] mod 4) = (M2[1][2] mod 4)
     and (M1[2][1] mod 4) = (M2[2][1] mod 4) and (M1[2][2] mod 4) = (M2[2][2] mod 4);;
end;;

NegMod4 := function(M)
  return [[ (4 - M[1][1]) mod 4, (4 - M[1][2]) mod 4 ],
          [ (4 - M[2][1]) mod 4, (4 - M[2][2]) mod 4 ]];;
end;;

IDMOD4 := [[1,0],[0,1]];;

MatOrderMod4 := function(M)
  local cur, ord;
  cur := M;;  ord := 1;;
  while not MatEqMod4(cur, IDMOD4) do
    cur := MatMulMod4(cur, M);;
    ord := ord + 1;;
    if ord > 200 then Error("MatOrderMod4: order exceeds bound (M not invertible mod 4?), M=", M); fi;
  od;
  return ord;;
end;;

BuildGL2Z4 := function()
  local out, a2, b2, c2, d2, M, det;
  out := [];;
  for a2 in [0..3] do for b2 in [0..3] do for c2 in [0..3] do for d2 in [0..3] do
    M := [[a2,b2],[c2,d2]];;
    det := DetMod4(M);;
    if det mod 2 = 1 then Add(out, M); fi;
  od; od; od; od;
  return out;;
end;;

Print("CKPT12 before BuildGL2Z4 t=", GAPLIB_WallElapsedMs(), "\n");
GL2Z4 := BuildGL2Z4();;
Print("CKPT13 BuildGL2Z4 done, len=", Length(GL2Z4), " t=", GAPLIB_WallElapsedMs(), "\n");
if Length(GL2Z4) <> 96 then Error("BuildGL2Z4 size mismatch, expected 96 got ", Length(GL2Z4)); fi;

MatInverseMod4 := function(M)
  local X;
  for X in GL2Z4 do
    if MatEqMod4(MatMulMod4(M, X), IDMOD4) then return X; fi;
  od;
  Error("MatInverseMod4: no inverse found, M=", M);
end;;

GL2Z4Aux := function(A)
  local centralizer, cyclicA, ord, cur, i, normalizer, X, Xinv, conj, inCyclic, T;
  centralizer := Filtered(GL2Z4, X -> MatEqMod4(MatMulMod4(X, A), MatMulMod4(A, X)));;
  ord := MatOrderMod4(A);;
  cyclicA := [ IDMOD4 ];;
  cur := A;;
  for i in [1 .. ord - 1] do Add(cyclicA, cur); cur := MatMulMod4(cur, A); od;
  normalizer := [];;
  for X in GL2Z4 do
    Xinv := MatInverseMod4(X);;
    conj := MatMulMod4(MatMulMod4(X, A), Xinv);;
    inCyclic := ForAny(cyclicA, T -> MatEqMod4(T, conj));;
    if inCyclic then Add(normalizer, X); fi;
  od;
  return rec(aut_pab_size := Length(GL2Z4), centralizer_size := Length(centralizer),
             cyclic_A_size := Length(cyclicA), normalizer_size := Length(normalizer));;
end;;

## ================= §1/§3 of the spec: A is the FIXED constant matrix in the canonical basis ===
## paper Ad(xbar) = [[0,-1],[1,-1]] mod 4 in the (v1,v2) basis (v1:=[y x^-1], v2:=A v1).
## This is a universal constant under this basis choice -- NOT re-derived per window (spec Sec.1).
A_CONST := [[0,3],[1,3]];;   ## [[0,-1],[1,-1]] mod 4

## ================= §3 precompute (per window, ONE time, cheap): q, Pab, v1, v2, coord() ======
Precompute := function(W, label)
  local G, P, D, q, Pab, s, v1, v2, gate1, gate2, gate3, gate4, gateOrient1, gateOrient2, coord,
        isoPabPc, v1Pc, v2Pc;
  Print("  CKPT-PC-A [", label, "] entering Precompute t=", GAPLIB_WallElapsedMs(), "\n");
  G := W.PN;;
  Print("  CKPT-PC-B [", label, "] G=W.PN, |G|=", Size(G), " t=", GAPLIB_WallElapsedMs(), "\n");
  P := DerivedSubgroup(G);;
  Print("  CKPT-PC-C [", label, "] P=DerivedSubgroup(G), |P|=", Size(P), " t=", GAPLIB_WallElapsedMs(), "\n");
  D := DerivedSubgroup(P);;
  Print("  CKPT-PC-D [", label, "] D=DerivedSubgroup(P), |D|=", Size(D), " t=", GAPLIB_WallElapsedMs(), "\n");
  q := NaturalHomomorphismByNormalSubgroup(P, D);;
  Print("  CKPT-PC-E [", label, "] q built t=", GAPLIB_WallElapsedMs(), "\n");
  Pab := Image(q);;
  Print("  CKPT-PC-F [", label, "] Pab=Image(q), |Pab|=", Size(Pab), " t=", GAPLIB_WallElapsedMs(), "\n");

  ## GATE 1 (item 1): P^ab invariants = [4,4]
  gate1 := (AbelianInvariants(Pab) = [4,4]);;
  Print("  CKPT-PC-G [", label, "] gate1=", gate1, " t=", GAPLIB_WallElapsedMs(), "\n");
  if not gate1 then Error("Precompute GATE1 failed for ", label, ": invariants=", AbelianInvariants(Pab)); fi;

  ## canonical basis: s = paper (y x^-1) -> raw GAP x^-1*y (W-1)
  s := W.x^-1 * W.y;;
  v1 := Image(q, s);;
  ## errata E-1/E-2 (2026-08-23): W-1 relates paper and GAP by an ANTI-isomorphism
  ## (iota(AB)=iota(B)iota(A)), which preserves inverses, so
  ##   iota(Ad_paper(g)(v)) = iota(g^-1) iota(v) iota(g) = iota(v)^iota(g)
  ## i.e. paper Ad(g) <-> GAP `v^g` (NOT `v^(g^-1)` as v1 of this spec had it).
  ## paper Ad(xbar)(v1) = x v1 x^-1  =>  GAP v1^x.
  v2 := Image(q, s^(W.x));;
  Print("  CKPT-PC-H [", label, "] v1,v2 built t=", GAPLIB_WallElapsedMs(), "\n");

  gate2 := (Size(Subgroup(Pab, [v1, v2])) = 16 and Order(v1) = 4 and Order(v2) = 4);;
  Print("  CKPT-PC-I [", label, "] gate2=", gate2, " t=", GAPLIB_WallElapsedMs(), "\n");
  if not gate2 then Error("Precompute GATE2 (basis) failed for ", label); fi;

  ## GATE: I + A + A^2 = 0 i.e. v1 * v2 * (A^2 v1) = identity in Pab. A^2 v1 <-> GAP v1^(x^2)
  ## under the corrected (anti-isomorphism) convention.
  gate3 := (v1 * v2 * Image(q, s^(W.x^2)) = One(Pab));;
  Print("  CKPT-PC-J [", label, "] gate3=", gate3, " t=", GAPLIB_WallElapsedMs(), "\n");
  if not gate3 then Error("Precompute GATE3 (I+A+A^2=0) failed for ", label); fi;

  ## GATE: Ad(ybar) = Ad(xbar) on Pab (both give v2), corrected convention: GAP v1^y.
  gate4 := (Image(q, s^(W.y)) = v2);;
  Print("  CKPT-PC-K [", label, "] gate4=", gate4, " t=", GAPLIB_WallElapsedMs(), "\n");
  if not gate4 then Error("Precompute GATE4 (Ad(ybar)=Ad(xbar)) failed for ", label); fi;

  ## GATE-ORIENT (errata E-3, mandatory fail-closed): the I+A+A^2=0 and Ad(ybar)=Ad(xbar)
  ## gates above are symmetric under A<->A^-1 (basis-orientation-blind), so they would PASS
  ## even under the old wrong convention -- they cannot by themselves catch an orientation bug.
  ## These two probe nu=2 specifically, which IS orientation-sensitive (verbatim from errata):
  ##   paper [y^2 x^-2] = v1+v2 = (1,1)         (positive)
  ##   paper [y x^-2 y] = -v2 = (0,3)            (negative canary)
  ## Under the wrong (v1-of-spec) convention these come out swapped -- (0,3) and (1,1)
  ## respectively -- so this pair is guaranteed to fail if the orientation regresses.
  gateOrient1 := (Image(q, W.x^-2 * W.y^2) = v1 * v2);;
  gateOrient2 := (Image(q, W.y * W.x^-2 * W.y) = v2^-1);;
  Print("  CKPT-PC-N [", label, "] gateOrient1=", gateOrient1, " gateOrient2=", gateOrient2,
        " t=", GAPLIB_WallElapsedMs(), "\n");
  if not (gateOrient1 and gateOrient2) then
    Error("Precompute GATE-ORIENT failed for ", label, ": orient1=", gateOrient1,
          " orient2=", gateOrient2, " -- basis orientation regression (errata E-3)");
  fi;

  ## perf note: Pab inherits P's large-degree (~1152) permutation representation via q, so raw
  ## Pab element comparisons are pathologically slow when repeated (measured previously: this
  ## exact pattern, called once per shadow x 16 combos, was the dominant cost even after removing
  ## GroupHomomorphismByImages). Re-encode into a PcGroup ONCE here; all coord() comparisons then
  ## happen in the cheap representation. This changes nothing mathematically (isoPabPc is a
  ## bijective homomorphism, so equality is preserved) -- pure performance fix, spec-neutral.
  isoPabPc := IsomorphismPcGroup(Pab);;
  Print("  CKPT-PC-L [", label, "] isoPabPc built t=", GAPLIB_WallElapsedMs(), "\n");
  v1Pc := Image(isoPabPc, v1);;
  v2Pc := Image(isoPabPc, v2);;
  Print("  CKPT-PC-M [", label, "] v1Pc,v2Pc built t=", GAPLIB_WallElapsedMs(), "\n");

  ## coord(w): discrete log of Image(q,w) in the (v1,v2) basis, (Z/4)^2, 16-combo search
  coord := function(w)
    local target, aa, bb;
    target := Image(isoPabPc, Image(q, w));;
    for aa in [0..3] do
      for bb in [0..3] do
        if v1Pc^aa * v2Pc^bb = target then return [aa, bb]; fi;
      od;
    od;
    Error("coord: no representation found for w=", w);
  end;;

  return rec(label := label, G := G, P := P, D := D, q := q, Pab := Pab, v1 := v1, v2 := v2,
             coord := coord, gate1 := gate1, gate2 := gate2, gate3 := gate3, gate4 := gate4,
             gateOrient1 := gateOrient1, gateOrient2 := gateOrient2,
             abelian_invariants := AbelianInvariants(Pab));;
end;;

## ================= theorem PUSH: theta_bar(m,f) from coord(f) and e = u mod 3 only ============
## e in {1,2} guaranteed by charming (gcd(u,Nord)=1 with Nord=12 => 3 does not divide u).
ComputeThetaBar := function(pc, m, f)
  local u, e, Ae, coordf, AeMinusI, term1, Sigma_e, sigmaE_v1, thetaV1, thetaV2, Theta,
        closedForm, alpha, beta, detGeneral, detClosed, epsE, Nab;
  u := 2*m + 1;;
  e := u mod 3;;
  if not (e = 1 or e = 2) then
    Error("ComputeThetaBar: e=u mod 3 not in {1,2} (charming violated?), u=", u, " e=", e);
  fi;
  if e = 1 then Ae := A_CONST; else Ae := MatMulMod4(A_CONST, A_CONST); fi;
  coordf := pc.coord(f);;
  AeMinusI := MatSubMod4(Ae, IDMOD4);;
  term1 := MatVecMod4(AeMinusI, coordf);;
  if e = 1 then Sigma_e := IDMOD4; else Sigma_e := MatAddMod4(IDMOD4, A_CONST); fi;
  sigmaE_v1 := MatVecMod4(Sigma_e, [1,0]);;   ## v1 has coordinate (1,0) by definition of the basis
  thetaV1 := VecAddMod4(term1, sigmaE_v1);;   ## (alpha, beta)
  thetaV2 := MatVecMod4(Ae, thetaV1);;
  Theta := [[thetaV1[1], thetaV2[1]], [thetaV1[2], thetaV2[2]]];;

  ## cross-check against the spec's explicit closed form (Sec.4 row (4)) -- must match exactly
  alpha := thetaV1[1];;  beta := thetaV1[2];;
  if e = 1 then
    closedForm := [[alpha, (4-beta) mod 4], [beta, (alpha-beta) mod 4]];;
  else
    closedForm := [[alpha, (beta-alpha) mod 4], [beta, (4-alpha) mod 4]];;
  fi;
  if not MatEqMod4(Theta, closedForm) then
    Error("ComputeThetaBar: general formula and closed form (Sec.4) disagree, m=", m, " e=", e,
          " general=", Theta, " closed=", closedForm);
  fi;

  ## det cross-check: det = eps_e * N(alpha+beta*A), N(x)=alpha^2-alpha*beta+beta^2, eps_1=+1,eps_2=-1
  Nab := (alpha*alpha - alpha*beta + beta*beta) mod 4;;
  if e = 1 then epsE := 1; else epsE := -1; fi;
  detClosed := (epsE * Nab) mod 4;;
  detGeneral := DetMod4(Theta);;
  if detGeneral <> detClosed then
    Error("ComputeThetaBar: det cross-check mismatch, m=", m, " general=", detGeneral, " closed=", detClosed);
  fi;

  return rec(m := m, u := u, e := e, alpha := alpha, beta := beta, matrix := Theta, det := detGeneral);;
end;;

## ================= per-window pipeline =================
RunWindow := function(W, label)
  local pc, f1_word, f2_word, selftestI, selftestA, selftestA2, ok0, ok1, ok2,
        x3c, y3c, z3c, x3even, y3even, cuspOk, charmingSet, corr, rows, row, m, f,
        weilPassCount, destructivePassCount, semilinearPassCount, fInPCount, thetaRow,
        kerChiRows, h0Rows, distinctMats, isNew, M, thetaTIdentification, tCandidates,
        detCheck, semiOk, weilOk, destrOk, fInP, kerChiList;
  Print(" CKPT-RW-A [", label, "] entering RunWindow t=", GAPLIB_WallElapsedMs(), "\n");
  pc := Precompute(W, label);;
  Print(" CKPT-RW-B [", label, "] Precompute returned t=", GAPLIB_WallElapsedMs(), "\n");

  ## ---- section 2 self-test (MUST run first, fail-closed) ----
  selftestI := ComputeThetaBar(pc, 0, Identity(pc.P));;
  ok0 := MatEqMod4(selftestI.matrix, IDMOD4);;
  Print(" CKPT-RW-C [", label, "] selftest[0,1] done ok0=", ok0, " t=", GAPLIB_WallElapsedMs(), "\n");

  f1_word := W.x^-1 * W.y;;   ## paper y x^-1 -> raw x^-1*y (= s itself, W-1)
  selftestA := ComputeThetaBar(pc, 0, f1_word);;
  ok1 := MatEqMod4(selftestA.matrix, A_CONST);;
  Print(" CKPT-RW-D [", label, "] selftest[0,f1] done ok1=", ok1, " t=", GAPLIB_WallElapsedMs(), "\n");

  ## f2: paper word "y^2 x^-2" (w_2 = ybar^2 xbar^-2) -> raw form per W-1 (paper AB -> GAP B*A,
  ## A=y^2,B=x^-2) = x^-2*y^2 -- errata E-4 confirms this translation was correct all along
  ## (v1_1_errata.md: "your f2 translation was correct"; the bug was solely the v2/ad_convention
  ## direction in Precompute, fixed above). Expected coord (1,1), expected theta = A^2 =
  ## [[3,1],[3,0]], det -3 = 1 (mod 4).
  f2_word := W.x^-2 * W.y^2;;
  selftestA2 := ComputeThetaBar(pc, 0, f2_word);;
  ok2 := MatEqMod4(selftestA2.matrix, MatMulMod4(A_CONST, A_CONST));;
  Print(" CKPT-RW-E [", label, "] selftest[0,f2] done ok2=", ok2, " t=", GAPLIB_WallElapsedMs(), "\n");

  if not (ok0 and ok1 and ok2) then
    Error("SELF-TEST FAILED for ", label, ": [0,1]->I:", ok0, " [0,f1]->A:", ok1, " [0,f2]->A^2:", ok2,
          " selftestI=", selftestI.matrix, " selftestA=", selftestA.matrix, " selftestA2=", selftestA2.matrix);
  fi;

  ## ---- item 2: cusp death (refined per spec: in 2*Pab, y3=x3, z3=-2*x3) ----
  x3c := pc.coord(W.x^3);;
  y3c := pc.coord(W.y^3);;
  z3c := pc.coord(W.z^3);;
  Print(" CKPT-RW-F [", label, "] cusp coords done t=", GAPLIB_WallElapsedMs(), "\n");
  x3even := (x3c[1] mod 2 = 0) and (x3c[2] mod 2 = 0);;
  cuspOk := x3even and VecEqMod4(y3c, x3c)
            and VecEqMod4(z3c, [ (4 - 2*x3c[1]) mod 4, (4 - 2*x3c[2]) mod 4 ]);;

  ## ---- full 48-shadow sweep ----
  charmingSet := Filtered([0 .. W.Nord - 1], mm2 -> Gcd(2*mm2 + 1, W.Nord) = 1);;
  Print(" CKPT-RW-G [", label, "] charmingSet computed, size=", Length(charmingSet), " t=", GAPLIB_WallElapsedMs(), "\n");
  corr := CorrectedShadows(W, charmingSet);;
  Print(" CKPT-RW-H [", label, "] CorrectedShadows returned, size=", Length(corr), " t=", GAPLIB_WallElapsedMs(), "\n");
  if Length(corr) <> 48 then Error("RunWindow: expected 48 corrected shadows, got ", Length(corr)); fi;

  rows := [];;
  weilPassCount := 0;;  destructivePassCount := 0;;  semilinearPassCount := 0;;  fInPCount := 0;;
  for row in corr do
    m := row[1];;  f := row[2];;
    fInP := (f in pc.P);;
    if fInP then fInPCount := fInPCount + 1; fi;
    thetaRow := ComputeThetaBar(pc, m, f);;
    weilOk := (thetaRow.det = (2*m+1) mod 4);;
    if weilOk then weilPassCount := weilPassCount + 1; fi;
    ## destructive control: compare det against (u+2) mod 4 instead of u -- MUST fail (48/48 FAIL expected)
    destrOk := (thetaRow.det = (2*m+1+2) mod 4);;
    if destrOk then destructivePassCount := destructivePassCount + 1; fi;
    ## semilinear law: Theta * A = A^e * Theta
    if thetaRow.e = 1 then semiOk := MatEqMod4(MatMulMod4(thetaRow.matrix, A_CONST), MatMulMod4(A_CONST, thetaRow.matrix));
    else semiOk := MatEqMod4(MatMulMod4(thetaRow.matrix, A_CONST), MatMulMod4(MatMulMod4(A_CONST,A_CONST), thetaRow.matrix)); fi;
    if semiOk then semilinearPassCount := semilinearPassCount + 1; fi;
    Add(rows, rec(m := m, u := thetaRow.u, e := thetaRow.e, alpha := thetaRow.alpha, beta := thetaRow.beta,
                   matrix := thetaRow.matrix, det := thetaRow.det, f_in_P := fInP,
                   weil_ok := weilOk, destructive_control_ok := destrOk, semilinear_ok := semiOk));;
    if Length(rows) mod 8 = 0 then
      Print(" CKPT-RW-ROW [", label, "] row ", Length(rows), "/48 done t=", GAPLIB_WallElapsedMs(), "\n");
    fi;
  od;
  Print(" CKPT-RW-I [", label, "] shadow sweep loop done, weil=", weilPassCount, "/48 t=", GAPLIB_WallElapsedMs(), "\n");

  ## ---- ker(chi_vir) (12 elements, m in {0,6}) and H0 (m=0 subset, 6 elements); theta_t id ----
  kerChiRows := Filtered(rows, r -> (2*r.m + 1) mod W.Nord = 1 mod W.Nord);;
  h0Rows := Filtered(kerChiRows, r -> r.m = 0);;
  kerChiList := List(kerChiRows, r -> rec(m := r.m, alpha := r.alpha, beta := r.beta, matrix := r.matrix));;

  distinctMats := [];;
  for row in h0Rows do
    isNew := true;;
    for M in distinctMats do if MatEqMod4(M, row.matrix) then isNew := false; break; fi; od;
    if isNew then Add(distinctMats, row.matrix); fi;
  od;

  tCandidates := Filtered(distinctMats, M -> MatOrderMod4(M) = 2);;
  thetaTIdentification := "UNKNOWN";;
  if Length(tCandidates) = 1 then
    if MatEqMod4(tCandidates[1], [[3,0],[0,3]]) then
      thetaTIdentification := "x<->y swap type (-I, matches proven prediction)";;
    elif MatEqMod4(tCandidates[1], [[1,0],[1,3]]) then
      thetaTIdentification := "complex conjugation [11,1] type ([[1,0],[1,-1]], NOT -I)";;
    else
      thetaTIdentification := "NEITHER of the two predicted types -- flag for review";;
    fi;
  fi;

  return rec(label := label, pc := pc,
             self_test := rec(zero_to_I := ok0, f1_to_A := ok1, f2_to_A2 := ok2,
                               matrix_0_1 := selftestI.matrix, matrix_0_f1 := selftestA.matrix,
                               matrix_0_f2 := selftestA2.matrix),
             cusp_death := rec(x3_coord := x3c, y3_coord := y3c, z3_coord := z3c,
                                x3_in_2Pab := x3even, y3_eq_x3 := VecEqMod4(y3c,x3c),
                                z3_eq_neg2x3 := VecEqMod4(z3c, [ (4-2*x3c[1]) mod 4, (4-2*x3c[2]) mod 4 ]),
                                overall_ok := cuspOk),
             shadow_total := Length(corr), f_in_P_count := fInPCount,
             weil_pass_count := weilPassCount, weil_total := Length(rows),
             destructive_control_pass_count := destructivePassCount,
             semilinear_pass_count := semilinearPassCount,
             ker_chi_vir_size := Length(kerChiRows), h0_size := Length(h0Rows),
             ker_chi_vir_list := kerChiList,
             distinct_h0_matrix_count := Length(distinctMats),
             t_order2_candidate_count := Length(tCandidates),
             t_matrix_candidates := tCandidates,
             theta_t_identification := thetaTIdentification,
             rows := rows);;
end;;

## ================= JSON helpers =================
JVec := function(v) return JPair(v[1], v[2]); end;;
JMat := function(M) return Concatenation("[[", String(M[1][1]), ",", String(M[1][2]), "],[",
                                          String(M[2][1]), ",", String(M[2][2]), "]]"); end;;
JMatList := function(ms) return JArr(List(ms, JMat)); end;;

JKerChiEntry := function(r)
  return Concatenation("{\"m\":", String(r.m), ",\"alpha\":", String(r.alpha), ",\"beta\":", String(r.beta),
                        ",\"matrix\":", JMat(r.matrix), "}");;
end;;

JRunWindow := function(rw)
  return Concatenation("{",
    "\"label\":", JStr(rw.label), ",",
    "\"precompute_gates\":{",
      "\"gate1_invariants_4_4\":", JB(rw.pc.gate1), ",",
      "\"gate2_basis_order4_independent\":", JB(rw.pc.gate2), ",",
      "\"gate3_I_plus_A_plus_A2_eq_0\":", JB(rw.pc.gate3), ",",
      "\"gate4_ad_ybar_eq_ad_xbar\":", JB(rw.pc.gate4), ",",
      "\"gate_orient1_y2xm2_eq_v1v2\":", JB(rw.pc.gateOrient1), ",",
      "\"gate_orient2_yxm2y_eq_v2inv\":", JB(rw.pc.gateOrient2), ",",
      "\"abelian_invariants\":", JArr(List(rw.pc.abelian_invariants, String)),
    "},",
    "\"self_test_section2\":{",
      "\"zero_to_I\":", JB(rw.self_test.zero_to_I), ",",
      "\"f1_to_A\":", JB(rw.self_test.f1_to_A), ",",
      "\"f2_to_A2\":", JB(rw.self_test.f2_to_A2), ",",
      "\"matrix_0_1\":", JMat(rw.self_test.matrix_0_1), ",",
      "\"matrix_0_f1\":", JMat(rw.self_test.matrix_0_f1), ",",
      "\"matrix_0_f2\":", JMat(rw.self_test.matrix_0_f2),
    "},",
    "\"item1_p_ab_invariants\":{\"abelian_invariants\":", JArr(List(rw.pc.abelian_invariants,String)),
      ",\"is_4_4\":", JB(rw.pc.abelian_invariants = [4,4]), "},",
    "\"item2_cusp_death\":{",
      "\"x3_coord\":", JVec(rw.cusp_death.x3_coord), ",",
      "\"y3_coord\":", JVec(rw.cusp_death.y3_coord), ",",
      "\"z3_coord\":", JVec(rw.cusp_death.z3_coord), ",",
      "\"x3_in_2Pab\":", JB(rw.cusp_death.x3_in_2Pab), ",",
      "\"y3_eq_x3\":", JB(rw.cusp_death.y3_eq_x3), ",",
      "\"z3_eq_neg2x3\":", JB(rw.cusp_death.z3_eq_neg2x3), ",",
      "\"overall_ok\":", JB(rw.cusp_death.overall_ok),
    "},",
    "\"item3_theta_t\":{",
      "\"h0_size\":", String(rw.h0_size), ",",
      "\"distinct_h0_matrix_count\":", String(rw.distinct_h0_matrix_count), ",",
      "\"h0_injective\":", JB(rw.distinct_h0_matrix_count = rw.h0_size), ",",
      "\"t_order2_candidate_count\":", String(rw.t_order2_candidate_count), ",",
      "\"t_matrix_candidates\":", JMatList(rw.t_matrix_candidates), ",",
      "\"identification\":", JStr(rw.theta_t_identification),
    "},",
    "\"item4_weil_canary\":{",
      "\"shadow_total\":", String(rw.shadow_total), ",",
      "\"weil_pass_count\":", String(rw.weil_pass_count), ",",
      "\"weil_total\":", String(rw.weil_total), ",",
      "\"all_48_pass\":", JB(rw.weil_pass_count = 48 and rw.weil_total = 48), ",",
      "\"destructive_control_pass_count\":", String(rw.destructive_control_pass_count), ",",
      "\"destructive_control_all_fail_as_expected\":", JB(rw.destructive_control_pass_count = 0),
    "},",
    "\"item5_semilinear_law\":{",
      "\"semilinear_pass_count\":", String(rw.semilinear_pass_count), ",",
      "\"all_48_pass\":", JB(rw.semilinear_pass_count = 48),
    "},",
    "\"item6_f_in_P_scope_assert\":{",
      "\"f_in_P_count\":", String(rw.f_in_P_count), ",",
      "\"all_48_in_P\":", JB(rw.f_in_P_count = 48),
    "},",
    "\"ker_chi_vir_alpha_beta_list\":[", JoinC(List(rw.ker_chi_vir_list, JKerChiEntry), ","), "]",
    "}");;
end;;

## ================= run all 3 records =================
Print("############################################################\n");
Print("# koubou83_m3_l2_check_v2.g -- linear-evaluation independent cross-check (spec v1)\n");
Print("############################################################\n");

## S154161/Wwin154161 already built earlier (right after DEEP15 extraction) so the W-1 gate
## could run in window 1's permutation group instead of raw fp-B3 -- not rebuilt here.
Print("CKPT14 reusing already-built S154161/Wwin154161 t=", GAPLIB_WallElapsedMs(), "\n");
S154163a := BuildWindowFromWords(Recs154163[1].index, Recs154163[1].words);;
Wwin154163a := MakeWindow(S154163a.s1, S154163a.s2);;
Print("CKPT16 Wwin154163a built t=", GAPLIB_WallElapsedMs(), "\n");
S154163b := BuildWindowFromWords(Recs154163[2].index, Recs154163[2].words);;
Wwin154163b := MakeWindow(S154163b.s1, S154163b.s2);;
Print("CKPT17 Wwin154163b built t=", GAPLIB_WallElapsedMs(), "\n");

if Size(Wwin154161.PN) <> 192 or Size(Wwin154163a.PN) <> 192 or Size(Wwin154163b.PN) <> 192 then
  Error("PIN: |G| != 192 in some record");
fi;
if Wwin154161.Nord <> 12 or Wwin154163a.Nord <> 12 or Wwin154163b.Nord <> 12 then
  Error("PIN: N_ord != 12");
fi;
Print("CKPT18 PIN asserts passed, entering RunWindow(154161) t=", GAPLIB_WallElapsedMs(), "\n");

RW_154161  := RunWindow(Wwin154161,  "1152-154161");;
Print("CKPT19 RunWindow(154161) returned t=", GAPLIB_WallElapsedMs(), "\n");
Print("  [1152-154161] self-test=", RW_154161.self_test.zero_to_I and RW_154161.self_test.f1_to_A
      and RW_154161.self_test.f2_to_A2, " weil=", RW_154161.weil_pass_count, "/48",
      " destructive_pass(expect0)=", RW_154161.destructive_control_pass_count,
      " semilinear=", RW_154161.semilinear_pass_count, "/48",
      " theta_t=", RW_154161.theta_t_identification, "\n");

RW_154163a := RunWindow(Wwin154163a, "1152-154163a");;
Print("  [1152-154163a] self-test=", RW_154163a.self_test.zero_to_I and RW_154163a.self_test.f1_to_A
      and RW_154163a.self_test.f2_to_A2, " weil=", RW_154163a.weil_pass_count, "/48",
      " destructive_pass(expect0)=", RW_154163a.destructive_control_pass_count,
      " semilinear=", RW_154163a.semilinear_pass_count, "/48",
      " theta_t=", RW_154163a.theta_t_identification, "\n");

RW_154163b := RunWindow(Wwin154163b, "1152-154163b");;
Print("  [1152-154163b] self-test=", RW_154163b.self_test.zero_to_I and RW_154163b.self_test.f1_to_A
      and RW_154163b.self_test.f2_to_A2, " weil=", RW_154163b.weil_pass_count, "/48",
      " destructive_pass(expect0)=", RW_154163b.destructive_control_pass_count,
      " semilinear=", RW_154163b.semilinear_pass_count, "/48",
      " theta_t=", RW_154163b.theta_t_identification, "\n");

Aux := GL2Z4Aux(A_CONST);;
Print("\n=== GL2(Z/4) auxiliary (constant A, universal across windows) ===\n");
Print("  |Aut(Pab)|=", Aux.aut_pab_size, " |C(A)|=", Aux.centralizer_size,
      " |<A>|=", Aux.cyclic_A_size, " |N(<A>)|=", Aux.normalizer_size, "\n");

## ---- 3-record agreement ----
AGREE := rec(
  self_test_all_pass := RW_154161.self_test.zero_to_I and RW_154161.self_test.f1_to_A and RW_154161.self_test.f2_to_A2
                     and RW_154163a.self_test.zero_to_I and RW_154163a.self_test.f1_to_A and RW_154163a.self_test.f2_to_A2
                     and RW_154163b.self_test.zero_to_I and RW_154163b.self_test.f1_to_A and RW_154163b.self_test.f2_to_A2,
  item1_all_4_4 := (RW_154161.pc.abelian_invariants=[4,4]) and (RW_154163a.pc.abelian_invariants=[4,4])
               and (RW_154163b.pc.abelian_invariants=[4,4]),
  item2_cusp_death_all_ok := RW_154161.cusp_death.overall_ok and RW_154163a.cusp_death.overall_ok
                         and RW_154163b.cusp_death.overall_ok,
  item3_identification_all_same := (RW_154161.theta_t_identification = RW_154163a.theta_t_identification)
                                and (RW_154163a.theta_t_identification = RW_154163b.theta_t_identification),
  item3_identification := RW_154161.theta_t_identification,
  item4_weil_all_48_all_records := (RW_154161.weil_pass_count=48) and (RW_154163a.weil_pass_count=48)
                                and (RW_154163b.weil_pass_count=48),
  item4_destructive_control_all_zero := (RW_154161.destructive_control_pass_count=0)
                                     and (RW_154163a.destructive_control_pass_count=0)
                                     and (RW_154163b.destructive_control_pass_count=0),
  item5_semilinear_all_48_all_records := (RW_154161.semilinear_pass_count=48) and (RW_154163a.semilinear_pass_count=48)
                                      and (RW_154163b.semilinear_pass_count=48),
  item6_f_in_P_all_48 := (RW_154161.f_in_P_count=48) and (RW_154163a.f_in_P_count=48) and (RW_154163b.f_in_P_count=48)
);;

Print("\n=== 3-record agreement ===\n");
Print("  ", AGREE, "\n");

## ================= write cert JSON =================
out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/koubou83_m3_l2_indepcheck_v1/linear_v2\",",
  "\"dir_frame_tag\":\"DIR: \\u5224\\u5b9a\\u306e\\u72ec\\u7acb\\u7167\\u5408 / FRAME: B\\u2083-gentle \\u7a93 \\u00d7 E[4]\",",
  "\"authority\":\"scratchpad/c83_m3_e4_lane_v1.md (\\u8a00\\u660e\\u306e\\u307f\\u53c2\\u7167\\u3002\\u6570\\u5b66\\u8005\\u306e\\u30b9\\u30af\\u30ea\\u30d7\\u30c8 scratchpad/m3_l2_probe_v*.g / m3_e4_field_numcheck_v1.py \\u306f\\u672a\\u8aad\\u30fb\\u4e0d\\u4f7f\\u7528 -- \\u8457\\u8005\\u5206\\u96e2)\",",
  "\"linear_spec_authorship_separation\":\"\\u5c0e\\u51fa(\\u5b9a\\u7406PUSH\\u30fb\\u6b63\\u6e96\\u57fa\\u5e95\\u30fbA\\u306e\\u5024\\u30fb\\u81ea\\u5df1\\u691c\\u8a3c\\u4f8b\\u30fb5\\u9805\\u76ee\\u306e\\u884c\\u5217\\u8a9e\\u8a33)=\\u5de5\\u623f\\u6570\\u5b66\\u8005(scratchpad/koubou83_m3_l2_linear_spec_v1.md\\u3001c83_m3_e4_lane_v1.md \\u3092\\u8457\\u8005\\u5206\\u96e2\\u306e\\u305f\\u3081\\u672a\\u8aad\\u3067\\u72ec\\u7acb\\u5c0e\\u51fa)\\u3002\\u5b9f\\u88c5(GAP\\u30b3\\u30fc\\u30c9\\u5316\\u30fb\\u5b9f\\u884c\\u30fbcert\\u751f\\u6210)=implementer\\u3002\",",
  "\"note\":\"raw measurement only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044\\u3002UNKNOWN\\u306f\\u4e00\\u7d1a\\u306e\\u7d50\\u679c\\u3002cross-checked \\u3067\\u3042\\u3063\\u3066 verified \\u3067\\u306f\\u306a\\u3044\\u3002\",",
  "\"method_note\":\"v1(GroupHomomorphismByImages\\u306e degree-1152 permutation \\u7fa4\\u4e0a\\u81ea\\u5df1\\u6e96\\u540c\\u578b\\u5199\\u69cb\\u7bc9)\\u306f\\u5358\\u4e00 window \\u3067\\u3059\\u3089 10 \\u5206 cap \\u8d85\\u904e\\u3057\\u672a\\u5b8c\\u4e86(\\u53f8\\u4ee4\\u5854\\u88c1\\u5b9a\\u3067\\u6df1\\u8ffd\\u3044\\u305b\\u305a\\u653e\\u68c4)\\u3002v2 \\u306f\\u4e8b\\u524d\\u8a08\\u7b97(\\u30671\\u56de)+shadow\\u3054\\u3068 coord(f)+2x2\\u884c\\u5217\\u6f14\\u7b97\\u306e\\u307f\\u3067\\u518d\\u69cb\\u6210\\u3002\",",
  "\"errata_note\":\"v1 \\u4ed5\\u69d8\\u306e\\u57fa\\u5e95\\u5411\\u304d\\u8aa4\\u308a(ad_convention \\u306e\\u65b9\\u5411\\u3001v2:=Image(q,s^(x^-1)) \\u306e1\\u884c)\\u3092\\u81ea\\u5df1\\u691c\\u8a3c+Weil canary \\u304c\\u6355\\u7378\\u3057\\u3001v1.1 errata(scratchpad/koubou83_m3_l2_linear_spec_v1_1_errata.md)\\u3067\\u4fee\\u6b63\\u3002\\u5b9a\\u7406PUSH\\u81ea\\u4f53\\u306f\\u4e0d\\u5909\\u3002\",",
  "\"w1_gate_fix_note\":\"2026-08-23 \\u4fee\\u7406: \\u771f\\u56e0\\u306f GroupHomomorphismByImages \\u3067\\u306f\\u306a\\u304f W1SemanticGate \\u5185\\u90e8\\u3067\\u306e\\u751f\\u306e\\u6709\\u9650\\u8868\\u793a\\u7fa4(fp-B3=BF3/[brelD]\\u3001\\u7121\\u9650\\u7fa4)\\u8981\\u7d20\\u540c\\u58eb\\u306e `=`/`<>` \\u5224\\u5b9a(\\u8a9e\\u306e\\u554f\\u984c\\u3092\\u4e00\\u822c\\u624b\\u6cd5\\u3067\\u89e3\\u304b\\u305b\\u3066\\u3044\\u305f\\u305f\\u3081\\u975e\\u7d42\\u6b62)\\u3002CKPT \\u306b\\u3088\\u308b\\u5c40\\u6240\\u5316(run 32617461891)\\u3067 CKPT07(B3\\u69cb\\u7bc9\\u5b8c\\u4e86 t=1ms)\\u3068 CKPT08(W1_GATE\\u5224\\u5b9a\\u5b8c\\u4e86)\\u306e\\u9593\\u3067\\u505c\\u6b62\\u3068\\u78ba\\u8a8d\\u3002\\u4fee\\u6b63: W1 gate \\u306e4\\u7b49\\u5f0f\\u3092 window 1 \\u306e\\u7f6e\\u63db\\u7fa4(\\u65e2\\u306b\\u9ad8\\u901f\\u3068\\u78ba\\u8a8d\\u6e08)\\u3067\\u8a55\\u4fa1\\u3059\\u308b\\u3088\\u3046\\u5909\\u66f4\\u3002\\u6570\\u5b66\\u7684\\u5983\\u5f53\\u6027(\\u53f8\\u4ee4\\u5854\\u88c1\\u5b9a): \\u7b49\\u5f0f positivePass \\u306f\\u81ea\\u7531\\u7c21\\u7d04\\u3060\\u3051\\u3067\\u6210\\u7acb\\u3059\\u308b\\u6052\\u7b49\\u5f0f\\u306a\\u306e\\u3067\\u4efb\\u610f\\u306e\\u5546\\u3067\\u771f\\u3002\\u4e0d\\u7b49\\u5f0f formerRejected/noncentralPass \\u306f\\u5546\\u3067\\u6210\\u7acb\\u3059\\u308c\\u3070\\u5143\\u306e\\u7fa4\\u3067\\u3082\\u6210\\u7acb(\\u4e0d\\u7b49\\u306f\\u5546\\u304b\\u3089\\u6301\\u3061\\u4e0a\\u304c\\u308b)\\u3002fail-closed \\u306f\\u4e0d\\u5909(window \\u5074\\u3067\\u4e88\\u671f\\u306b\\u53cd\\u3057\\u3066 fail \\u3059\\u308c\\u3070\\u5373 Error \\u3067\\u505c\\u6b62)\\u3002\",",
  "\"gap_version\":", JStr(GAPInfo.Version), ",",
  "\"provenance\":{",
    "\"input_data_file\":\"search/iso_census83_deep15_data.g\",",
    "\"input_data_sha256\":", JStr(INPUT_DATA_SHA256), ",",
    "\"input_week3_battery_common_sha256\":", JStr(INPUT_WBC_SHA256), ",",
    "\"input_gaplib_common_sha256\":", JStr(INPUT_GAPLIB_SHA256), ",",
    "\"input_prelude_sha256\":", JStr(INPUT_PRELUDE_SHA256), ",",
    "\"linear_spec_path\":", JStr(SPEC_PATH), ",",
    "\"linear_spec_sha256\":", JStr(SPEC_SHA256), ",",
    "\"linear_spec_errata_path\":", JStr(ERRATA_PATH), ",",
    "\"linear_spec_errata_sha256\":", JStr(ERRATA_SHA256), ",",
    "\"script_path\":", JStr(SCRIPT_PATH), ",",
    "\"script_sha256\":", JStr(SCRIPT_SHA256),
  "},",
  "\"w1_semantic_gate\":{",
    "\"gate_id\":", JStr(W1_GATE.gate_id), ",",
    "\"evaluated_in\":", JStr(W1_GATE.evaluated_in), ",",
    "\"positive_identity_pass\":", JB(W1_GATE.positive_identity_pass), ",",
    "\"former_error_rejected\":", JB(W1_GATE.former_error_rejected), ",",
    "\"noncentral_fixture_pass\":", JB(W1_GATE.noncentral_fixture_pass), ",",
    "\"overall_pass\":", JB(W1_GATE.overall_pass),
  "},",
  "\"ad_convention\":{",
    "\"paper_ad_x(u)\":\"x*u*x^-1\",",
    "\"gap_power_convention\":\"u^x = x^-1*u*x\",",
    "\"w1_relation\":\"paper<->GAP are related by an ANTI-isomorphism (iota(AB)=iota(B)iota(A)); anti-isomorphisms preserve inverses, so paper Ad(g)(v) = g v g^-1 corresponds to GAP `v^g` (NOT `v^(g^-1)`). errata E-1/E-6 (2026-08-23), v1 of the spec had this backwards.\",",
    "\"implementation\":\"paper Ad(xbar)(v1) = x v1 x^-1 = GAP v1^x (corrected 2026-08-23); A is the FIXED constant [[0,-1],[1,-1]] mod 4 in the canonical basis v1:=[y x^-1], v2:=A v1 (spec Sec.1), not re-derived per window\",",
    "\"A_const\":", JMat(A_CONST),
  "},",
  "\"per_window\":[", JRunWindow(RW_154161), ",", JRunWindow(RW_154163a), ",", JRunWindow(RW_154163b), "],",
  "\"gl2z4_aux_universal\":{",
    "\"aut_pab_size\":", String(Aux.aut_pab_size), ",",
    "\"centralizer_A_size\":", String(Aux.centralizer_size), ",",
    "\"cyclic_A_size\":", String(Aux.cyclic_A_size), ",",
    "\"normalizer_cyclic_A_size\":", String(Aux.normalizer_size),
  "},",
  "\"three_record_agreement\":{",
    "\"self_test_all_pass\":", JB(AGREE.self_test_all_pass), ",",
    "\"item1_all_4_4\":", JB(AGREE.item1_all_4_4), ",",
    "\"item2_cusp_death_all_ok\":", JB(AGREE.item2_cusp_death_all_ok), ",",
    "\"item3_identification_all_same\":", JB(AGREE.item3_identification_all_same), ",",
    "\"item3_identification\":", JStr(AGREE.item3_identification), ",",
    "\"item4_weil_all_48_all_records\":", JB(AGREE.item4_weil_all_48_all_records), ",",
    "\"item4_destructive_control_all_zero\":", JB(AGREE.item4_destructive_control_all_zero), ",",
    "\"item5_semilinear_all_48_all_records\":", JB(AGREE.item5_semilinear_all_48_all_records), ",",
    "\"item6_f_in_P_all_48\":", JB(AGREE.item6_f_in_P_all_48),
  "},",
  "\"elapsed_wall_ms\":", String(GAPLIB_WallElapsedMs() - t0Global),
  "}"
);;

WriteFile("search/certs/koubou83_m3_l2_indepcheck_v1_20260823.json", out);;
Print("\nWrote search/certs/koubou83_m3_l2_indepcheck_v1_20260823.json\n");
Print("KOUBOU83_M3_L2_INDEPCHECK_V2_DONE\n");
QUIT;
