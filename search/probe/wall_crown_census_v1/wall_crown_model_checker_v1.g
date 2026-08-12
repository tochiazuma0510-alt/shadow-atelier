#############################################################################
## Independent model lane for wall_crown_census_v1.g.
## Constructs AGL(1,ell) x S_t abstractly, without wall witnesses, shadows,
## MakeWindow, CorrectedShadowsXi, or the producer's helper functions.
#############################################################################

Read("search/probe/wac_v1/gap_output_prelude.g");;

B := function(b)
  if b then return "true"; else return "false"; fi;
end;;
S := s -> Concatenation("\"", ReplacedString(s, "\"", "\\\""), "\"");;
IL := l -> Concatenation("[", JoinStringsWithSeparator(List(l, String), ","), "]");;

OneRow := function(G, cl)
  local M, C, h, Q, Z, id;
  M := Representative(cl);
  C := Core(G, M);
  h := NaturalHomomorphismByNormalSubgroup(G, C);
  Q := Image(h);
  Z := Socle(Q);
  id := fail;
  if Size(Q) <= 2000 then id := IdGroup(Q); fi;
  return rec(i := Index(G,M), c := Size(cl), n := IsNormal(G,M),
             po := Size(Q), ps := StructureDescription(Q), pid := id,
             so := Size(Z), ss := StructureDescription(Z), a := IsAbelian(Z));
end;;

Signature := function(G)
  local F, q, Q, rows;
  F := FrattiniSubgroup(G);
  q := NaturalHomomorphismByNormalSubgroup(G,F);
  Q := Image(q);
  rows := List(ConjugacyClassesMaximalSubgroups(Q), cl -> OneRow(Q,cl));
  return rec(go := Size(G), fo := Size(F), qo := Size(Q),
    gs := StructureDescription(G), qs := StructureDescription(Q), rows := rows);
end;;

RJ := function(r)
  local id;
  if r.pid = fail then id := "null"; else id := IL(r.pid); fi;
  return Concatenation("{\"index\":",String(r.i),
    ",\"class_size\":",String(r.c),",\"maximal_is_normal\":",B(r.n),
    ",\"primitive_order\":",String(r.po),",\"primitive_structure\":",S(r.ps),
    ",\"primitive_id\":",id,",\"socle_order\":",String(r.so),
    ",\"socle_structure\":",S(r.ss),",\"crown_abelian\":",B(r.a),"}");
end;;

SJ := function(label, ell, t, r)
  return Concatenation("{\"label\":",S(label),",\"ell\":",String(ell),
    ",\"t\":",String(t),",\"group_order\":",String(r.go),
    ",\"group_structure\":",S(r.gs),",\"frattini_order\":",String(r.fo),
    ",\"quotient_order\":",String(r.qo),",\"quotient_structure\":",S(r.qs),
    ",\"maximal_class_count\":",String(Length(r.rows)),
    ",\"abelian_crown_count\":",String(Number(r.rows,x->x.a)),
    ",\"nonabelian_crown_count\":",String(Number(r.rows,x->not x.a)),
    ",\"classes\":[",JoinStringsWithSeparator(List(r.rows,RJ),","),"]}");
end;;

specs := [
  ["wall24",19,5], ["wall28",23,5],
  ["wall36",31,5], ["wall37",31,6]
];;
results := [];;
for z in specs do
  ## DirectProduct is intentionally used here; the producer instead obtains
  ## an actual subgroup Normalizer(S_n,<x>) from each wall witness.
  G := DirectProduct(AffineGeneralLinearGroup(1,z[2]), SymmetricGroup(z[3]));
  Add(results, SJ(z[1],z[2],z[3],Signature(G)));
od;

out := Concatenation(
  "{\n\"schema\":\"wall-crown-model-checker/v1\",\n",
  "\"generated_by\":\"search/probe/wall_crown_census_v1/wall_crown_model_checker_v1.g\",\n",
  "\"gap_version\":",S(GAPInfo.Version),",\n",
  "\"model\":\"DirectProduct(AffineGeneralLinearGroup(1,ell),SymmetricGroup(t))\",\n",
  "\"walls\":[",JoinStringsWithSeparator(results,","),"]\n}\n");;
PrintTo("search/certs/wall_crown_model_checker_v1_20260812.json",out);;
Print("WALL_CROWN_MODEL_CHECKER_V1_DONE\n");
QUIT;
