# Task 129 modular-dimension producer.
# ASCII only. Run through: .\gap.ps1 search\g3bridge_moddim_v1.g

out := "search/certs/g3bridge_moddim_v1_gap_raw_20260813.json";
checkpoint := "search/certs/g3bridge_moddim_v1_gap_checkpoint.json";

PrintTo(checkpoint,
  "{\"schema\":\"g3bridge_moddim_gap_checkpoint/v1\",",
  "\"stage\":\"start\",\"complete\":false}\n");

p := PSL(2,8);
if Size(p) <> 504 then
  Error("unexpected PSL(2,8) order");
fi;

ordinary := CharacterTable("L2(8)");
brauer := BrauerTable(ordinary, 3);
degrees := List(Irr(brauer), chi -> chi[1]);
nontrivialDegrees := Filtered(degrees, degree -> degree > 1);
minimumDegree := Minimum(nontrivialDegrees);
generators := GeneratorsOfGroup(p);
permutationImages := List(generators, generator -> List([1..9], point -> point ^ generator));

PrintTo(checkpoint,
  "{\"schema\":\"g3bridge_moddim_gap_checkpoint/v1\",",
  "\"stage\":\"brauer_and_permutation_action\",\"complete\":false,",
  "\"psl_order\":", Size(p), ",\"brauer_degrees\":", degrees, "}\n");

PrintTo(out,
  "{\"schema\":\"g3bridge_moddim_gap_raw/v1\",",
  "\"gap_version\":\"", GAPInfo.Version, "\",",
  "\"psl_order\":", Size(p), ",",
  "\"permutation_degree\":9,",
  "\"generator_images\":", permutationImages, ",",
  "\"brauer_character_degrees_characteristic_3\":", degrees, ",",
  "\"minimum_nontrivial_brauer_degree\":", minimumDegree, ",",
  "\"complete\":true}\n");

PrintTo(checkpoint,
  "{\"schema\":\"g3bridge_moddim_gap_checkpoint/v1\",",
  "\"stage\":\"complete\",\"complete\":true}\n");

QUIT_GAP(0);
