Read("search/probe/wac_v1/gap_output_prelude.g");
LoadPackage("anupq");
Read("search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g");
P := F;;
D := DerivedSubgroup(P);;
Print("|P| = ", Size(P), "\n");
Print("|D|=|[P,P]| = ", Size(D), "\n");
pcgsD := Pcgs(D);;
Print("NumberOfGenerators(pcgsD) = ", Length(pcgsD), "\n");
Print("RelativeOrders(pcgsD) = ", RelativeOrders(pcgsD), "\n");
# sanity: exponent vector -> element, using pcgs base-7 semantics
g := List(pcgsD, x->x);;
Print("gens listable: ", Length(g), "\n");
e := [0,0,0,0,0,1];;
elt := Product([1..6], i -> g[i]^e[i]);;
Print("elt for e=[0,0,0,0,0,1] computed OK: ", elt<>fail, "\n");
Print("6 * 7^6 = ", 6*7^6, " (expect 705894)\n");
Print("DRY_CHECK_DONE\n");
QUIT;
