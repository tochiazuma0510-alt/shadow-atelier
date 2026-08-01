# C-beta stage 5, FULL CROSS TABLE (commander order 2026-08-01, ruling 312, following the
# mathematician's diagnosis in u7_fire_log_v1_addendum_grade.md Sec 4.2.4: the alpha=2,3
# mismatch found earlier is conjectured to be a right/left coset-action convention artifact,
# NOT a genuine [alpha] determination). Falsifiable prediction under test:
#   model(alpha) is simultaneously M-conjugate to abstract(alphaPrime) iff
#     (alpha,alphaPrime) in {(1,1),(2,3),(3,2)}     -- i.e. a diagonal SWAP of 2<->3, 1 fixed.
# All 9 cells (alpha,alphaPrime) in {1,2,3}^2 are measured; the prediction is not hard-coded
# into the search -- only reported afterwards, per "prediction not written into the code"
# instruction. Independent of cbeta_model.py / cbeta_nielsen.py (python reference).
Read("search/probe/wac_v1/cbeta_model_indep.g");;

n := 7;;
alphas := [1,2,3];;

# pre-build all model triples (ORDER-A) and all abstract sides once
modelData := [];;
for a in alphas do
    Add(modelData, [a, BuildModel(n, 1, (-a) mod n, a)]);
od;;

abstractData := [];;
for ap in alphas do
    Add(abstractData, [ap, BuildAbstract(n, ap)]);
od;;

Print("### C-beta stage 5 cross table: model(alpha) x abstract(alphaPrime), n=7 ###\n\n");
Print("abstract side sizes (H_{2,alphaPrime,0}):\n");
for pr in abstractData do
    Print("  alphaPrime=", pr[1], "  |G7|=", pr[2].G7order, " |H|=", pr[2].Horder,
          " |M_abs|=", pr[2].Morder, " transitive=", pr[2].transitive, "\n");
od;
Print("\n");

results := [];;
for md in modelData do
    alpha := md[1];; m := md[2];;
    row := [];;
    for pr in abstractData do
        alphaPrime := pr[1];; a := pr[2];;
        matched := false;;
        for t in m.triples do
            if TripleConjugate(t[1], t[2], m.deg, a.X, a.Y, a.deg) = true then
                matched := true; break;
            fi;
        od;
        Add(row, matched);
        Print("model(alpha=", alpha, ") x abstract(alphaPrime=", alphaPrime, ") : MATCH = ",
              matched, "\n");
    od;
    Add(results, [alpha, row]);
od;;

Print("\n### cross table summary (rows=model alpha, cols=abstract alphaPrime 1,2,3) ###\n");
for r in results do
    Print("model alpha=", r[1], ":  ", r[2], "\n");
od;;

Print("\n### prediction check (reported only, not injected into search) ###\n");
predicted := [[1,1,true],[1,2,false],[1,3,false],
              [2,1,false],[2,2,false],[2,3,true],
              [3,1,false],[3,2,true],[3,3,false]];;
allmatch := true;;
for p in predicted do
    a := p[1];; ap := p[2];; exp := p[3];;
    for r in results do
        if r[1] = a then
            got := r[2][ap];
            Print("  cell(alpha=", a, ",alphaPrime=", ap, "): predicted=", exp,
                  " actual=", got, "  ", (got=exp), "\n");
            if got <> exp then allmatch := false; fi;
        fi;
    od;
od;;
Print("\nPREDICTION_FULLY_CONFIRMED = ", allmatch, "\n");
Print("DONE\n");
