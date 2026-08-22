## scratchpad/koubou83_c3lift_check_v1_1.g
## GAP-C3-3 / GAP-C3-2 独立照合 -- M0 追加タスク(数学者裁定 memo §7 由来)への対応版。
##
## M0 の診断: v1 の 𝒯 代表構成行 (旧) `W.y^nu * W.x^(-nu)` が **規約 W-1 違反**と裁定された。
## 規約 W-1(week1-定義ノート.md §1.5.1、正本): paper の積 "AB" は GAP では `B*A` に対応する
## ((AB)*i = A*(B*i) 対 i^{B*A}=(i^B)^A)。paper 語 "y^nu x^{-nu}" は A=y^nu, B=x^{-nu} なので
## GAP 形は B*A = `x^-nu * y^nu` であるべきで、旧実装の `y^nu * x^-nu` は A*B(逆順)になっていた
## -- ちょうど [y-bar^nu, x-bar^-nu] 分だけずれる形で「mod Phi(P) 一致・元不一致」という v1 の
## 観測(t_pair_valid=false x11)を説明する候補(補題 U' との矛盾から artifact と裁定)。
## 本 script は 𝒯 照合部のみを正しい規約で再計算する(タスク1の構造測定は再走しない --
## v1 の値をそのまま参照する。P/Phi(P)/Ad(x)/Ad(x)^2 の計算自体は W-1 と無関係で再走の必要が
## ないが、比較に必要な軽量計算として再構成はする)。
##
## 出所: 発注 = 司令塔(タスク: koubou83 c3lift indep check v1、M0 追加)。
## 正本: scratchpad/gt_grt_dictionary_memo_v1.md §3.2/§3.3.2/§3.3.3/§3.3.4(数学的言明のみを参照。
##       数学者の補助スクリプト scratchpad/math_c3cover_test_v2.g は未読・不使用 -- 著者分離)。
## 入力: search/iso_census83_deep15_data.g の DEEP15(producer 資産・既存)から
##       id=[1152,154161](1レコード)・id=[1152,154163](2レコード、同一 window の別 words 表現)
##       を抽出。窓の shadow 値自体には非接触(候補値には触れない/新規に自前で計算する)。
## 機構: (F2) commutation-rule machinery(MakeWindow/TT/TH/RtOf/CorrectedShadows)は
##       search/wall-miner-v4.g 由来の producer 標準実装をこの script 内で再記述(verbatim
##       再掲・iso_census83_deep15_v1.g と同じ移植パターン)。数学者の scratchpad は使わない。
##
## タスク1(GAP-C3-3): 両窓で G=F2/N_{F2} の下中心列・P(=Syl2(G')相当)・Phi(P)・d(P)・
##   x^3,y^3,z^3 in Phi(P)?・Ad(x-bar) の P/Phi(P) 上の位数と固定点を独立に測定。
## タスク2(GAP-C3-2): ker(chi_vir) の元(m=0 スライス)ごとに T_{0,f} の P/Phi(P) 上の
##   誘導作用を計算し、Ad(x-bar) の生成する内部 C3 = {id, Ad(x), Ad(x)^2} と一致するかを判別。
##
## 規律: 判定語(genuine/verified 等)は書かない。UNKNOWN一級。格上げ禁止。

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");

t0Global := GAPLIB_WallElapsedMs();;

INPUT_DATA_SHA256 := "75905c604b83058ff6406f5c115bfa3325fd4424c98125750e49c2b76bbd35ec";;
INPUT_WBC_SHA256   := "aadf1afa5e1a171d10d0aa1f9657e823cad669b960e08da7b9e7618f2ea4f998";;
INPUT_GAPLIB_SHA256 := "f80eeeae71c4e39f8b3d62d997d18635f5ea8fb339a6d0578e834300ea4d4911";;
INPUT_PRELUDE_SHA256 := "2e4da671ad9d018be1bc6f2f387f0e1d597e87c2c0e807eef40aeef3b92deece";;
SCRIPT_SHA256_PLACEHOLDER := "PENDING_SELF_HASH";;

## ================= B3 = <a,b | aba=bab> setup (same reconstruction pattern as
## search/iso_census83_deep15_v1.g -- independent re-typing, math scratchpad not read) =================
BF3 := FreeGroup("a", "b");;
brelD := BF3.1*BF3.2*BF3.1*BF3.2^-1*BF3.1^-1*BF3.2^-1;;
B3 := BF3 / [brelD];;
ga := B3.1;;  gb := B3.2;;
a := ga;;  b := gb;;   # global bind for EvalString(word) -- DEEP15 words use bare a,b

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

## ================= (F2) window record: x=s1^2, y=s2^2, Delta=s1 s2 s1, delta=s1 s2, c=Delta^2 ===
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
Read("search/iso_census83_deep15_data.g");;   # defines DEEP15 (producer asset, unmodified)
if Length(DEEP15) <> 15 then Error("DEEP15 length != 15, got ", Length(DEEP15)); fi;

Rec154161 := First(DEEP15, r -> r.id = [1152, 154161]);;
Recs154163 := Filtered(DEEP15, r -> r.id = [1152, 154163]);;
if Rec154161 = fail then Error("record [1152,154161] not found in DEEP15"); fi;
if Length(Recs154163) <> 2 then Error("expected exactly 2 records for [1152,154163], got ", Length(Recs154163)); fi;

## ================= Task 1: independent structural measurement =================
# gamma_1=G, gamma_{i+1}=[G,gamma_i], stop when size stabilizes (maxSteps safety bound)
LCSCompute := function(G, maxSteps)
  local series, cur, nxt, i;
  series := [G];;
  cur := G;;
  for i in [1 .. maxSteps] do
    nxt := CommutatorSubgroup(G, cur);;
    Add(series, nxt);;
    if Size(nxt) = Size(cur) then return series; fi;
    cur := nxt;;
  od;;
  return series;;
end;;

# induced action of an endomorphism-on-P (given as a GAP function P-elt -> P-elt) on P/Phi(P);
# returns rec(order:=.., fixed_nontrivial_count:=.., is_identity:=.., action_table:=list of [q,image])
InducedFrattiniAction := function(P, PhiP, actionFn)
  local natMap, Q2, elemsQ2, idQ2, mapTable, q, preim, img, ApplyMap, ord, allId, cq, i, fixedList;
  natMap := NaturalHomomorphismByNormalSubgroup(P, PhiP);;
  Q2 := Image(natMap);;
  elemsQ2 := Elements(Q2);;
  idQ2 := Identity(Q2);;
  mapTable := [];;
  for q in elemsQ2 do
    preim := PreImagesRepresentative(natMap, q);;
    img := Image(natMap, actionFn(preim));;
    Add(mapTable, [q, img]);;
  od;;
  ApplyMap := function(q)
    local r;
    r := First(mapTable, rr -> rr[1] = q);;
    return r[2];;
  end;;
  ord := 1;;
  repeat
    allId := true;;
    for q in elemsQ2 do
      cq := q;;
      for i in [1 .. ord] do cq := ApplyMap(cq); od;;
      if cq <> q then allId := false; break; fi;
    od;;
    if allId then break; fi;
    ord := ord + 1;;
  until ord > Size(P) + 1;
  fixedList := Filtered(elemsQ2, q -> (q <> idQ2) and (ApplyMap(q) = q));;
  return rec(q2_size := Size(Q2), order := ord, fixed_nontrivial_count := Length(fixedList),
             is_identity := (ord = 1), map_table := mapTable, apply := ApplyMap, elems := elemsQ2, idQ2 := idQ2);;
end;;

Task1Measure := function(W, label)
  local G, LCS, gamma2, gamma3, gamma2eq3, P, PhiP, sizeP, sizePhi, dP,
        x3, y3, z3, x3inPhi, y3inPhi, z3inPhi, adx, adx2, lcsSizes;
  G := W.PN;;
  LCS := LCSCompute(G, 12);;
  lcsSizes := List(LCS, Size);;
  gamma2 := LCS[2];;
  if Length(LCS) >= 3 then gamma3 := LCS[3]; else gamma3 := LCS[2]; fi;
  gamma2eq3 := (Size(gamma2) = Size(gamma3));;
  P := gamma2;;   # = DerivedSubgroup(G); since |G|=192=2^6*3 and G^ab has no 2-part predicted,
                  # P should already be the full Sylow-2 of G' (checked numerically below, not assumed)
  sizeP := Size(P);;
  PhiP := FrattiniSubgroup(P);;
  sizePhi := Size(PhiP);;
  dP := LogInt(sizeP / sizePhi, 2);;
  x3 := W.x^3;;  y3 := W.y^3;;  z3 := W.z^3;;
  x3inPhi := x3 in PhiP;;  y3inPhi := y3 in PhiP;;  z3inPhi := z3 in PhiP;;
  adx := InducedFrattiniAction(P, PhiP, p -> W.x * p * W.x^-1);;
  adx2 := InducedFrattiniAction(P, PhiP, p -> W.x^2 * p * W.x^-2);;
  return rec(label := label, bq_order := Size(W.Bq), g_order := Size(G), n_ord := W.Nord,
             lcs_sizes := lcsSizes, gamma2_size := Size(gamma2), gamma3_size := Size(gamma3),
             gamma2_eq_gamma3 := gamma2eq3,
             p_size := sizeP, phi_p_size := sizePhi, d_p := dP,
             p_is_sylow2_of_g := (Size(G) mod sizeP = 0 and Gcd(sizeP, Size(G) / sizeP) = 1),
             x3_in_phi := x3inPhi, y3_in_phi := y3inPhi, z3_in_phi := z3inPhi,
             adx_order := adx.order, adx_fixed_nontrivial_count := adx.fixed_nontrivial_count,
             adx2_order := adx2.order, adx2_fixed_nontrivial_count := adx2.fixed_nontrivial_count,
             q2_size := adx.q2_size,
             adxRec := adx, adx2Rec := adx2, W := W, P := P, PhiP := PhiP);;
end;;

## ================= Task 2: ker(chi_vir) discriminating procedure (GAP-C3-2) =================
## chi_vir([m,f]) taken mod N_ord equals 1 iff m == 0 (m ranges over its own single-rep window
## [0,N_ord-1]; per memo's own derivation in Thm C3-LIFT(iii), chi(g)=1 mod 2*N_ord forces m=0
## mod N_ord exactly, i.e. m=0 in this index range). ker(chi_vir) = { [0,f] in GT(N) }.
## NOTE (Sol trap #12 avoidance): m's own modulus is N_ord; u=2m+1's modulus is 2*N_ord. This
## script never reduces u mod N_ord -- u is used only as a literal group-element exponent
## (x^u), and m=0 selection uses m's own modulus (N_ord) only, per the memo's derivation, not
## an ad hoc assumption made independently here.

Task2Discriminate := function(W, P, PhiP, adxRec, adx2Rec, label)
  local charmingSet, corr, kerChi, results, m, f, u, psi, actionFn, ind, matchId, matchAdx,
        matchAdx2, external, verdict, nu, tCandidates, nuRange, tMatch, rec_, matched,
        natMapPP, tCandidatesInP, tModPhiList, fModPhi, matchedModPhi, nuModPhi;

  charmingSet := Filtered([0 .. W.Nord - 1], mm -> Gcd(2*mm+1, W.Nord) = 1);;
  corr := CorrectedShadows(W, charmingSet);;
  # ker(chi_vir): chi_vir([m,f]) = (2m+1) mod N_ord = 1 mod N_ord. Since N_ord is even here,
  # this is NOT the same as "m=0 only" -- (2m+1) mod N_ord = 1 mod N_ord reduces to
  # m = 0 mod (N_ord / Gcd(2,N_ord)), i.e. m=0 AND (when N_ord even) m=N_ord/2 both qualify.
  # (This is exactly the m-modulus vs u-modulus distinction flagged as a known trap --
  # computed directly here via literal mod arithmetic, not assumed.)
  kerChi := Filtered(corr, s -> (2*s[1] + 1) mod W.Nord = 1 mod W.Nord);;

  # T-candidates: T = { (paper) y^nu x^(-nu) : nu } -- per regulation W-1 (week1-定義ノート.md
  # SS1.5.1, authoritative): paper product "AB" corresponds to GAP `B*A`. Here A=y^nu, B=x^-nu,
  # so the GAP-side element is B*A = x^-nu * y^nu (NOT y^nu * x^-nu, which was v1's bug --
  # M0 diagnosis: v1 had the two factors in paper order instead of the W-1-mandated reversed
  # GAP order, i.e. off by the commutator [y-bar^nu, x-bar^-nu]).
  nuRange := [0 .. 2*W.Nord - 1];;
  tCandidates := List(nuRange, nu -> [nu, W.x^(-nu) * W.y^nu]);;

  # secondary, coarser cross-check: does f coincide with some T-candidate only modulo Phi(P)
  # (i.e. in the 2-dim F2 quotient), even when exact group-element equality fails? Only
  # T-candidates that actually lie in P are eligible (P = DerivedSubgroup(G) is a proper
  # subgroup; a generic y^nu x^-nu need not lie in P at all).
  natMapPP := NaturalHomomorphismByNormalSubgroup(P, PhiP);;
  tCandidatesInP := Filtered(tCandidates, tc -> tc[2] in P);;
  tModPhiList := List(tCandidatesInP, tc -> [tc[1], Image(natMapPP, tc[2])]);;

  results := [];;
  for rec_ in kerChi do
    m := rec_[1];;  f := rec_[2];;  u := 2*m + 1;;   # m=0 so u=1
    psi := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y], [W.x^u, AbstractProd([f^-1, W.y^u, f])]);;
    if psi = fail then
      Add(results, rec(m := m, f_order := Order(f), well_defined := false, in_P := fail));;
      continue;;
    fi;
    actionFn := function(p) return Image(psi, p); end;;
    # sanity: psi should preserve P (P = gamma2(G), characteristic in G, hence preserved by any
    # automorphism of G) -- check numerically rather than assume
    if Image(psi, P) <> P then
      Add(results, rec(m := m, f_order := Order(f), well_defined := true, in_P := false));;
      continue;;
    fi;
    ind := InducedFrattiniAction(P, PhiP, actionFn);;
    matchId := ForAll(ind.elems, q -> ind.apply(q) = q);;
    matchAdx := ForAll(ind.elems, q -> ind.apply(q) = adxRec.apply(q));;
    matchAdx2 := ForAll(ind.elems, q -> ind.apply(q) = adx2Rec.apply(q));;
    external := not (matchId or matchAdx or matchAdx2);;
    # cross-check against T = {(m=0, y^nu x^-nu)} -- T (fake torus) has first coordinate
    # fixed at m=0 (u=1); a raw f-value coincidence at m<>0 is recorded but is NOT a T-image
    # (the pair [m,f] as a whole must match, not just the f-component) -- flagged via t_pair_valid.
    matched := Filtered(tCandidates, tc -> tc[2] = f);;
    if Length(matched) > 0 then
      nu := matched[1][1];;
    else
      nu := fail;;
    fi;
    # coarser check: f mod Phi(P) equal to some T-candidate mod Phi(P)?
    fModPhi := Image(natMapPP, f);;
    matchedModPhi := Filtered(tModPhiList, tc -> tc[2] = fModPhi);;
    if Length(matchedModPhi) > 0 then
      nuModPhi := matchedModPhi[1][1];;
    else
      nuModPhi := fail;;
    fi;
    Add(results, rec(m := m, f_order := Order(f), well_defined := true, in_P := true,
                      action_order := ind.order, action_is_id := matchId,
                      matches_adx := matchAdx, matches_adx2 := matchAdx2,
                      external_action := external, matched_nu := nu,
                      t_pair_valid := (m = 0 and nu <> fail),
                      matched_nu_modphi := nuModPhi));;
  od;;

  return rec(label := label, n_ord := W.Nord, charming_set_size := Length(charmingSet),
             derived_subgroup_order := Size(DerivedSubgroup(W.PN)),
             shadow_total := Length(corr), ker_chi_vir_size := Length(kerChi),
             nu_range_tried := [0, 2*W.Nord - 1], results := results);;
end;;

## ================= JSON helpers for the per-window records =================
JBoolOrNull := function(v)
  if v = fail then return "null"; fi;
  return JB(v);;
end;;

JIntOrNull := function(v)
  if v = fail then return "null"; fi;
  return String(v);;
end;;

JTask1 := function(r)
  return Concatenation("{",
    "\"label\":", JStr(r.label), ",",
    "\"bq_order\":", String(r.bq_order), ",",
    "\"g_order\":", String(r.g_order), ",",
    "\"n_ord\":", String(r.n_ord), ",",
    "\"lcs_sizes\":", JArr(List(r.lcs_sizes, String)), ",",
    "\"gamma2_size\":", String(r.gamma2_size), ",",
    "\"gamma3_size\":", String(r.gamma3_size), ",",
    "\"gamma2_eq_gamma3\":", JB(r.gamma2_eq_gamma3), ",",
    "\"p_size\":", String(r.p_size), ",",
    "\"phi_p_size\":", String(r.phi_p_size), ",",
    "\"d_p\":", String(r.d_p), ",",
    "\"p_is_sylow2_of_g\":", JB(r.p_is_sylow2_of_g), ",",
    "\"x3_in_phi\":", JB(r.x3_in_phi), ",",
    "\"y3_in_phi\":", JB(r.y3_in_phi), ",",
    "\"z3_in_phi\":", JB(r.z3_in_phi), ",",
    "\"q2_size\":", String(r.q2_size), ",",
    "\"adx_order\":", String(r.adx_order), ",",
    "\"adx_fixed_nontrivial_count\":", String(r.adx_fixed_nontrivial_count), ",",
    "\"adx2_order\":", String(r.adx2_order), ",",
    "\"adx2_fixed_nontrivial_count\":", String(r.adx2_fixed_nontrivial_count),
    "}");;
end;;

## action_order/action_is_id/matches_adx/matches_adx2/external_action/matched_nu are only
## present on rows where well_defined and in_P are both true (IsBound guard below).
JTask2ResultRow := function(row)
  local parts;
  parts := [ "{",
    "\"m\":", String(row.m), ",",
    "\"f_order\":", String(row.f_order), ",",
    "\"well_defined\":", JB(row.well_defined), ",",
    "\"in_P\":", JBoolOrNull(row.in_P) ];;
  if IsBound(row.action_order) then
    Append(parts, [ ",\"action_order\":", String(row.action_order),
                     ",\"action_is_id\":", JB(row.action_is_id),
                     ",\"matches_adx\":", JB(row.matches_adx),
                     ",\"matches_adx2\":", JB(row.matches_adx2),
                     ",\"external_action\":", JB(row.external_action),
                     ",\"matched_nu\":", JIntOrNull(row.matched_nu),
                     ",\"t_pair_valid\":", JB(row.t_pair_valid),
                     ",\"matched_nu_modphi\":", JIntOrNull(row.matched_nu_modphi) ]);;
  fi;
  Append(parts, [ "}" ]);;
  return Concatenation(parts);;
end;;

JTask2 := function(r)
  return Concatenation("{",
    "\"label\":", JStr(r.label), ",",
    "\"n_ord\":", String(r.n_ord), ",",
    "\"charming_set_size\":", String(r.charming_set_size), ",",
    "\"derived_subgroup_order\":", String(r.derived_subgroup_order), ",",
    "\"shadow_total\":", String(r.shadow_total), ",",
    "\"ker_chi_vir_size\":", String(r.ker_chi_vir_size), ",",
    "\"nu_range_tried\":", JPair(r.nu_range_tried[1], r.nu_range_tried[2]), ",",
    "\"nontrivial_action_count\":", String(Length(Filtered(r.results, x -> IsBound(x.action_is_id) and not x.action_is_id))), ",",
    "\"external_action_count\":", String(Length(Filtered(r.results, x -> IsBound(x.external_action) and x.external_action))), ",",
    "\"results\":[", JoinC(List(r.results, JTask2ResultRow), ","), "]",
    "}");;
end;;

## ================= run all 3 records =================
Print("############################################################\n");
Print("# koubou83_c3lift_check_v1_1.g -- M0 fix: T-candidates per regulation W-1 (was: y^nu*x^-nu, now: x^-nu*y^nu)\n");
Print("############################################################\n");

S154161 := BuildWindowFromWords(Rec154161.index, Rec154161.words);;
Wwin154161 := MakeWindow(S154161.s1, S154161.s2);;
S154163a := BuildWindowFromWords(Recs154163[1].index, Recs154163[1].words);;
Wwin154163a := MakeWindow(S154163a.s1, S154163a.s2);;
S154163b := BuildWindowFromWords(Recs154163[2].index, Recs154163[2].words);;
Wwin154163b := MakeWindow(S154163b.s1, S154163b.s2);;

Print("\n=== Task 1: structural measurement ===\n");
t1_154161 := Task1Measure(Wwin154161, "1152-154161");;
Print("  [1152-154161] |G|=", t1_154161.g_order, " N_ord=", t1_154161.n_ord,
      " lcs_sizes=", t1_154161.lcs_sizes, " gamma2=gamma3: ", t1_154161.gamma2_eq_gamma3,
      " |P|=", t1_154161.p_size, " |Phi(P)|=", t1_154161.phi_p_size, " d(P)=", t1_154161.d_p,
      " x3,y3,z3 in Phi(P): ", [t1_154161.x3_in_phi, t1_154161.y3_in_phi, t1_154161.z3_in_phi],
      " Ad(x) order=", t1_154161.adx_order, " fixed(nontrivial)=", t1_154161.adx_fixed_nontrivial_count, "\n");

t1_154163a := Task1Measure(Wwin154163a, "1152-154163a");;
Print("  [1152-154163a] |G|=", t1_154163a.g_order, " N_ord=", t1_154163a.n_ord,
      " lcs_sizes=", t1_154163a.lcs_sizes, " gamma2=gamma3: ", t1_154163a.gamma2_eq_gamma3,
      " |P|=", t1_154163a.p_size, " |Phi(P)|=", t1_154163a.phi_p_size, " d(P)=", t1_154163a.d_p,
      " x3,y3,z3 in Phi(P): ", [t1_154163a.x3_in_phi, t1_154163a.y3_in_phi, t1_154163a.z3_in_phi],
      " Ad(x) order=", t1_154163a.adx_order, " fixed(nontrivial)=", t1_154163a.adx_fixed_nontrivial_count, "\n");

t1_154163b := Task1Measure(Wwin154163b, "1152-154163b");;
Print("  [1152-154163b] |G|=", t1_154163b.g_order, " N_ord=", t1_154163b.n_ord,
      " lcs_sizes=", t1_154163b.lcs_sizes, " gamma2=gamma3: ", t1_154163b.gamma2_eq_gamma3,
      " |P|=", t1_154163b.p_size, " |Phi(P)|=", t1_154163b.phi_p_size, " d(P)=", t1_154163b.d_p,
      " x3,y3,z3 in Phi(P): ", [t1_154163b.x3_in_phi, t1_154163b.y3_in_phi, t1_154163b.z3_in_phi],
      " Ad(x) order=", t1_154163b.adx_order, " fixed(nontrivial)=", t1_154163b.adx_fixed_nontrivial_count, "\n");

Print("\n=== Task 2: ker(chi_vir) discriminating procedure (GAP-C3-2) ===\n");
t2_154161 := Task2Discriminate(t1_154161.W, t1_154161.P, t1_154161.PhiP, t1_154161.adxRec, t1_154161.adx2Rec, "1152-154161");;
Print("  [1152-154161] shadow_total=", t2_154161.shadow_total, " ker_chi_vir_size=", t2_154161.ker_chi_vir_size,
      " charming_set_size=", t2_154161.charming_set_size, "\n");

t2_154163a := Task2Discriminate(t1_154163a.W, t1_154163a.P, t1_154163a.PhiP, t1_154163a.adxRec, t1_154163a.adx2Rec, "1152-154163a");;
Print("  [1152-154163a] shadow_total=", t2_154163a.shadow_total, " ker_chi_vir_size=", t2_154163a.ker_chi_vir_size,
      " charming_set_size=", t2_154163a.charming_set_size, "\n");

t2_154163b := Task2Discriminate(t1_154163b.W, t1_154163b.P, t1_154163b.PhiP, t1_154163b.adxRec, t1_154163b.adx2Rec, "1152-154163b");;
Print("  [1152-154163b] shadow_total=", t2_154163b.shadow_total, " ker_chi_vir_size=", t2_154163b.ker_chi_vir_size,
      " charming_set_size=", t2_154163b.charming_set_size, "\n");

## ================= write cert JSON =================
out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/koubou83_c3lift_indepcheck_v1_1\",",
  "\"dir_frame_tag\":\"DIR: \\u6b63\\u5074(\\u7b97\\u8853\\u4e0b\\u754c)/FRAME: B\\u2083-gentle \\u00d7 \\u6955\\u5186\\u88ab\\u8986\",",
  "\"authority\":\"scratchpad/gt_grt_dictionary_memo_v1.md \\u00a73.2/\\u00a73.3.2/\\u00a73.3.3/\\u00a73.3.4 (GAP-C3-3/GAP-C3-2 \\u3010\\u9818\\u57df\\u5206\\u96e2\\u3011\\u72ec\\u7acb\\u518d\\u5b9f\\u88c5\\u3002\\u6570\\u5b66\\u8005\\u306e scratchpad/math_c3cover_test_v2.g \\u306f\\u672a\\u8aad\\u30fb\\u4e0d\\u4f7f\\u7528)\",",
  "\"note\":\"raw measurement only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044\\u3002UNKNOWN\\u306f\\u4e00\\u7d1a\\u306e\\u7d50\\u679c\\u3002cross-checked \\u3067\\u3042\\u3063\\u3066 verified \\u3067\\u306f\\u306a\\u3044\\u3002\",",
  "\"m0_note\":\"\\u8ffd\\u52a0\\u30bf\\u30b9\\u30af M0(\\u6570\\u5b66\\u8005\\u88c1\\u5b9a memo \\u00a77\\u7531\\u6765)\\u3002v1 \\u306e 𝒯 \\u4ee3\\u8868\\u69cb\\u6210\\u884c\\u306f `W.y^nu*W.x^(-nu)` \\u3067\\u898f\\u7d04 W-1 \\u9055\\u53cd\\u3068\\u88c1\\u5b9a\\uff08week1-\\u5b9a\\u7fa9\\u30ce\\u30fc\\u30c8.md \\u00a71.5.1: paper \\u7a4d 'AB' \\u306f GAP \\u3067\\u306f B*A\\uff09\\u3002\\u672c v1_1 \\u3067\\u306f `W.x^(-nu)*W.y^nu` \\u306b\\u4fee\\u6b63\\u3057\\u3066\\u518d\\u8d70\\u3002\\u30bf\\u30b9\\u30af1(\\u69cb\\u9020\\u6e2c\\u5b9a)\\u306f v1 \\u3068\\u540c\\u4e00\\u306e\\u5024\\u3067\\u518d\\u8d70\\u4e0d\\u8981(\\u672c script \\u3067\\u3082\\u5185\\u90e8\\u8a08\\u7b97\\u3068\\u3057\\u3066\\u306f\\u5b9f\\u884c\\u3055\\u308c\\u308b\\u304c\\u5024\\u306f v1 \\u3068\\u5b8c\\u5168\\u4e00\\u81f4\\u3059\\u308b\\u306f\\u305a)\\u3002\",",
  "\"gap_version\":", JStr(GAPInfo.Version), ",",
  "\"provenance\":{",
    "\"input_data_file\":\"search/iso_census83_deep15_data.g\",",
    "\"input_data_sha256\":", JStr(INPUT_DATA_SHA256), ",",
    "\"input_week3_battery_common_sha256\":", JStr(INPUT_WBC_SHA256), ",",
    "\"input_gaplib_common_sha256\":", JStr(INPUT_GAPLIB_SHA256), ",",
    "\"input_prelude_sha256\":", JStr(INPUT_PRELUDE_SHA256), ",",
    "\"prior_cert_v1\":\"search/certs/koubou83_c3lift_indepcheck_v1_20260822.json\",",
    "\"script_path\":\"scratchpad/koubou83_c3lift_check_v1_1.g\",",
    "\"script_sha256\":", JStr(SCRIPT_SHA256_PLACEHOLDER),
  "},",
  "\"task1_structural_measurement\":[",
    JTask1(t1_154161), ",", JTask1(t1_154163a), ",", JTask1(t1_154163b),
  "],",
  "\"task2_ker_chivir_discrimination\":[",
    JTask2(t2_154161), ",", JTask2(t2_154163a), ",", JTask2(t2_154163b),
  "],",
  "\"memo_claimed_values_for_reference_only\":{",
    "\"p_size\":64,\"phi_p_size\":16,\"d_p\":2,",
    "\"x3_y3_z3_in_phi_p\":true,",
    "\"ad_xbar_order\":3,\"ad_xbar_fixed_nontrivial_count\":0",
  "},",
  "\"elapsed_wall_ms\":", String(GAPLIB_WallElapsedMs() - t0Global),
  "}"
);;

WriteFile("search/certs/koubou83_c3lift_indepcheck_v1_1_20260822.json", out);;
Print("\nWrote search/certs/koubou83_c3lift_indepcheck_v1_1_20260822.json\n");
Print("KOUBOU83_C3LIFT_INDEPCHECK_V1_1_DONE\n");
QUIT;
