## search/pchi1_v2.g -- pchi1_v2 (裁定813①, docs/notes/cv9_chi_semantics_audit_v1.md).
## Fixes the bug in search/pchi1_v1.g:63 (the `if IsPrimeInt(p) then` filter silently DROPPED
## every non-prime-order chief factor -- i.e. every case where the "1-dimensional F_p" premise
## of the predicate fails -- from the census 46-member measurement, without recording that they
## were dropped. falsifier's independent audit (cv9_chi_semantics_audit_v1.md SS1-B) found the
## dropped factors include: 8 pairs' |W|=4 (dim-2 F_2, likely from the Q8 normal subgroup
## structure per addendum_a SS1.2 Q8-FAM), [384,608]'s |W|=4 factors x2, [750,6]'s |W|=25
## (dim-2 F_5, the falsifier's specifically flagged "特記対象": image C6, det order 1) across
## all 10 members, and 4 NON-ABELIAN chief factors ([120,5]/[336,114]/[336,208]/[360,51],
## |G/C_G(W)|=60/168/336/60).
##
## CHI-CARRY convention compliance (裁定813 provisional adoption, cv9_chi_semantics_audit_v1.md
## SS3): "chi_semantics"="section" (this measures conjugation action on a NORMAL-in-NORMAL
## chief-series section W=A/B with A,B BOTH normal in the whole group G -- the "section"
## reading, NOT an abstract F_p[G]-module or representation-theoretic composition factor
## reading -- those are explicitly OUT OF SCOPE for this predicate per the audit's adopted
## convention). "factor_filter"="none" (no IsPrimeInt or any other filter -- EVERY chief-series
## factor is reported). Non-abelian factors report ONLY |G/C_G(W)| (ord_chi_w is null -- Aut(W)
## is non-commutative for a non-abelian W, so "the order of a character" is not defined; this
## is the CHI-CARRY-mandated omission, not a bug).
##
## Domain: SAME 23-pair/46-member census list as search/hcen_ab_v1.g (id_group list reused
## verbatim, already cross-checked by crosscheck/check_hcen_ab.py). M5 excluded (outside the
## 23-pair census domain, per hcen_ab_v1.g's own disclosure) -- consistent with pchi1_v1.g's
## own domain scope.
## PROVENANCE NOTE (falsifier's "反証できなかった範囲" disclosure, cv9_chi_semantics_audit_v1.md
## SS(reflex)): the id_group list here is taken from search/hcen_ab_v1.g, which itself is a
## verified join against search/certs/r6a_summary_v1_20260806.json + search/certs/
## lins_twin_census_v1_20260806.json (both are census certs recording id=IdGroup(B3/N) for
## actual normal subgroups N of B3 -- i.e. "id_group" IS ALREADY B3/N by the SOURCE census
## cert's own construction, not re-derived in this script). This script does NOT re-verify
## that provenance chain itself (SmallGroup(id) trivially reconstructs an abstract group with
## that IdGroup label, which is a faithful reconstruction of the ISOMORPHISM TYPE B3/N by
## definition of IdGroup -- there is no additional gap here beyond what hcen_ab_v1.g/
## crosscheck/check_hcen_ab.py already established).
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

## ============ 23-pair / 46-member target list (VERBATIM reuse of search/hcen_ab_v1.g's list) ============
PAIRS := [
  rec(pair_fiber:="lt384:idx24:pair0",  index:=24,  m0_id:=[24,3],   m1_id:=[24,3]),
  rec(pair_fiber:="lt384:idx72:pair2",  index:=72,  m0_id:=[72,3],   m1_id:=[72,3]),
  rec(pair_fiber:="lt384:idx120:pair6", index:=120, m0_id:=[120,15], m1_id:=[120,15]),
  rec(pair_fiber:="lt384:idx120:pair7", index:=120, m0_id:=[120,5],  m1_id:=[120,5]),
  rec(pair_fiber:="lt384:idx168:pair11",index:=168, m0_id:=[168,22], m1_id:=[168,22]),
  rec(pair_fiber:="lt384:idx216:pair16",index:=216, m0_id:=[216,3],  m1_id:=[216,3]),
  rec(pair_fiber:="lt384:idx264:pair24",index:=264, m0_id:=[264,12], m1_id:=[264,12]),
  rec(pair_fiber:="lt384:idx312:pair27",index:=312, m0_id:=[312,25], m1_id:=[312,25]),
  rec(pair_fiber:="lt384:idx336:pair30",index:=336, m0_id:=[336,208],m1_id:=[336,208]),
  rec(pair_fiber:="lt384:idx336:pair35",index:=336, m0_id:=[336,114],m1_id:=[336,114]),
  rec(pair_fiber:="lt384:idx360:pair38",index:=360, m0_id:=[360,14], m1_id:=[360,14]),
  rec(pair_fiber:="lt384:idx360:pair39",index:=360, m0_id:=[360,51], m1_id:=[360,51]),
  rec(pair_fiber:="idx384:608",         index:=384, m0_id:=[384,608],m1_id:=[384,608]),
  rec(pair_fiber:="idx750:pair0", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair1", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair2", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair3", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair4", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair5", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair6", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair7", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair8", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
  rec(pair_fiber:="idx750:pair9", index:=750, m0_id:=[750,6], m1_id:=[750,6]),
];;

## measure EVERY chief factor (no filter), via the SAME ActionHomomorphism-based conjugation
## action method used in search/meas_chi_m5_v1.g (uniform across dim=1/dim>=2/non-abelian).
MeasureAllFactors := function(idpair)
  local G, cs, out, i, N1, N2, wSize, nat, Q, isElemAb, pVal, dimVal, actFun, hom, imgOrd, ordChiW;
  G := SmallGroup(idpair[1], idpair[2]);
  cs := ChiefSeries(G);
  out := [];
  for i in [1..Length(cs)-1] do
    N1 := cs[i];  N2 := cs[i+1];
    wSize := Size(N1)/Size(N2);
    nat := NaturalHomomorphismByNormalSubgroup(N1, N2);
    Q := Image(nat);
    isElemAb := IsElementaryAbelian(Q);
    pVal := fail;  dimVal := fail;
    if isElemAb and wSize > 1 then
      pVal := FactorsInt(wSize)[1];
      dimVal := LogInt(wSize, pVal);
    fi;
    actFun := function(q, g)
      local n;
      n := PreImagesRepresentative(nat, q);
      return Image(nat, n^g);
    end;
    hom := ActionHomomorphism(G, Elements(Q), actFun);
    imgOrd := Size(Image(hom));
    ordChiW := fail;
    if dimVal = 1 then ordChiW := imgOrd; fi;
    Add(out, rec(factor_index:=i, w_size:=wSize, is_elementary_abelian:=isElemAb,
                 p:=pVal, dim:=dimVal, g_mod_cg_w:=imgOrd, ord_chi_w:=ordChiW));
  od;
  return out;
end;;

results := [];;
allOrdChiW_dim1 := [];;   # only dim=1 factors have a well-defined ord
allGmodCgW := [];;        # every factor's |G/C_G(W)| (well-defined regardless of abelian-ness)
for pr in PAIRS do
  m0res := MeasureAllFactors(pr.m0_id);;
  m1res := MeasureAllFactors(pr.m1_id);;
  Add(results, rec(pair_fiber:=pr.pair_fiber, index:=pr.index, m0_id:=pr.m0_id, m0_factors:=m0res,
                    m1_id:=pr.m1_id, m1_factors:=m1res));
  for r in m0res do
    Add(allGmodCgW, r.g_mod_cg_w);
    if r.ord_chi_w <> fail then Add(allOrdChiW_dim1, r.ord_chi_w); fi;
  od;
  for r in m1res do
    Add(allGmodCgW, r.g_mod_cg_w);
    if r.ord_chi_w <> fail then Add(allOrdChiW_dim1, r.ord_chi_w); fi;
  od;
  Print(pr.pair_fiber, ": m0=", m0res, "\n");
od;

maxOrdDim1 := 0;;
if Length(allOrdChiW_dim1) > 0 then maxOrdDim1 := Maximum(allOrdChiW_dim1); fi;
maxGmodCgW := Maximum(allGmodCgW);;
totalFactorsMeasured := Length(allGmodCgW);;

Print("total_factors_measured(no filter)=", totalFactorsMeasured,
      " total_dim1_factors=", Length(allOrdChiW_dim1),
      " max_ord_dim1=", maxOrdDim1, " max_g_mod_cg_w_any=", maxGmodCgW, "\n");

## specifically flag the [750,6] dim=2/F_5 factor (falsifier's named special case: image C6, det order 1)
p750recs := Filtered(results, r -> r.m0_id = [750,6]);;
p750_dim2_f5 := [];;
for r in p750recs do
  for f in r.m0_factors do
    if f.dim = 2 and f.p = 5 then Add(p750_dim2_f5, rec(pair_fiber:=r.pair_fiber, factor:=f)); fi;
  od;
od;
Print("[750,6] dim=2/F_5 factors found: ", Length(p750_dim2_f5), "\n");
for r in p750_dim2_f5 do
  Print("  ", r.pair_fiber, ": ", r.factor, "\n");
od;

## ============ JSON output ============
JFactor := function(r)
  local pStr, dimStr, ordStr;
  if r.p = fail then pStr := "null"; else pStr := String(r.p); fi;
  if r.dim = fail then dimStr := "null"; else dimStr := String(r.dim); fi;
  if r.ord_chi_w = fail then ordStr := "null"; else ordStr := String(r.ord_chi_w); fi;
  return Concatenation("{",
    "\"factor_index\":", String(r.factor_index), ",",
    "\"w_size\":", String(r.w_size), ",",
    "\"is_elementary_abelian\":", JB(r.is_elementary_abelian), ",",
    "\"p\":", pStr, ",",
    "\"dim\":", dimStr, ",",
    "\"g_mod_cg_w\":", String(r.g_mod_cg_w), ",",
    "\"ord_chi_w\":", ordStr,
    "}");
end;;

JMember := function(r)
  return Concatenation("{",
    "\"pair_fiber\":", JStr(r.pair_fiber), ",",
    "\"index\":", String(r.index), ",",
    "\"m0_id_group\":", JPair(r.m0_id[1], r.m0_id[2]), ",",
    "\"m0_factors\":[", JoinC(List(r.m0_factors, JFactor), ","), "],",
    "\"m1_id_group\":", JPair(r.m1_id[1], r.m1_id[2]), ",",
    "\"m1_factors\":[", JoinC(List(r.m1_factors, JFactor), ","), "]",
    "}");
end;;

JP750Rec := function(r)
  return Concatenation("{",
    "\"pair_fiber\":", JStr(r.pair_fiber), ",",
    "\"factor\":", JFactor(r.factor),
    "}");
end;;

out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/pchi1_v2\",",
  "\"authority\":\"", "\\u88c1\\u5b9a813(1) -- docs/notes/cv9_chi_semantics_audit_v1.md (falsifier CV-9 \\u5224\\u8aad\\u3001\\u898f\\u7d04 CHI-CARRY \\u6682\\u5b9a\\u63a1\\u629e)\",",
  "\"supersedes_note\":\"search/certs/pchi1_v1_20260811.json's IsPrimeInt filter (pchi1_v1.g:63) silently DROPPED every non-prime-order chief factor without recording it. This script applies NO filter -- every chief-series factor is reported.\",",
  "\"chi_semantics\":\"section\",",
  "\"factor_filter\":\"none\",",
  "\"provenance_note\":\"id_group list reused VERBATIM from search/hcen_ab_v1.g (already cross-checked by crosscheck/check_hcen_ab.py against search/certs/r6a_summary_v1_20260806.json + search/certs/lins_twin_census_v1_20260806.json). SmallGroup(id_group) reconstructs the ISOMORPHISM TYPE B3/N by definition of IdGroup -- not re-verified further in this script (per falsifier's own disclosed-limitation note, cv9_chi_semantics_audit_v1.md, this is inherited from hcen_ab_v1.g, not a new gap).\",",
  "\"predicate_note\":\"for each G in the census 46-member domain, ChiefSeries(G) is taken; for EVERY consecutive chief factor N1/N2 (elementary abelian or not), the conjugation action of G on N1/N2 induces g_mod_cg_w=|G/C_G(W)| (well-defined regardless of W's structure). ord_chi_w is reported ONLY when dim=1 (Aut(F_p) is cyclic, so the action's image order IS the twist character's order; for dim>=2 or non-abelian W, Aut(W) is non-commutative and 'the order of a character' is undefined -- CHI-CARRY convention).\",",
  "\"members\":[", JoinC(List(results, JMember), ","), "],",
  "\"total_factors_measured\":", String(totalFactorsMeasured), ",",
  "\"total_dim1_factors\":", String(Length(allOrdChiW_dim1)), ",",
  "\"max_ord_dim1\":", String(maxOrdDim1), ",",
  "\"max_g_mod_cg_w_any_factor\":", String(maxGmodCgW), ",",
  "\"p750_id6_dim2_F5_factors\":[", JoinC(List(p750_dim2_f5, JP750Rec), ","), "],",
  "\"no_verdict_note\":\"raw chief-factor data (p,dim,w_size,is_elementary_abelian,g_mod_cg_w,ord_chi_w) and booleans only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002\"",
  "}"
);;

WriteFile("search/certs/pchi1_v2_20260811.json", out);;
Print("Wrote search/certs/pchi1_v2_20260811.json\n");
Print("PCHI1_V2_DONE\n");
QUIT;
