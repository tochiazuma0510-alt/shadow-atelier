## exp3_check_all.g -- W-a canary check for all 5 targets: |P|, exponent,
## LCS layer dims vs Witt(2,k). Pure structural check, no hexagon/dim S_k
## comparison (that part is on hold pending design addendum per 裁定779).
CheckTarget := function(path, p, c, wittList)
  local P, x, y, lcs, lcsDims, i, expOk;
  Read(path);
  P := F;;
  x := MapImages[1];;  y := MapImages[2];;
  Unbind(F);;  Unbind(MapImages);;
  Print("--- p=", p, " c=", c, " ---\n");
  Print("|P| = ", Size(P), "  (naive Witt-sum predicts p^", Sum(wittList), "=", p^Sum(wittList), ")\n");
  expOk := (x^p = Identity(P)) and (y^p = Identity(P));
  Print("x^p=1 and y^p=1? ", expOk, "\n");
  lcs := LowerCentralSeriesOfGroup(P);;
  Print("LCS length (num nontrivial layers + 1): ", Length(lcs), "\n");
  lcsDims := List([1..Length(lcs)-1], i -> LogInt(Size(lcs[i])/Size(lcs[i+1]), p));;
  Print("LCS layer dims (measured):  ", lcsDims, "\n");
  Print("Witt(2,k) k=1..", c, " (naive free predict): ", wittList, "\n");
  Print("gamma_{c+1}(P) trivial? ", Size(lcs[Length(lcs)]) = 1, "\n");
  Print("MATCH per degree: ", List([1..Length(lcsDims)], i -> lcsDims[i] = wittList[i]), "\n");
  Print("\n");
end;;

# Witt(2,k) k=1..8 = 2,1,2,3,6,9,18,30
CheckTarget("search/probe/pl_lab1_v1/PQ_OUTPUT_p5c4.g", 5, 4, [2,1,2,3]);
CheckTarget("search/probe/pl_lab1_v1/PQ_OUTPUT_p5c5.g", 5, 5, [2,1,2,3,6]);
CheckTarget("search/probe/pl_lab1_v1/PQ_OUTPUT_p5c6.g", 5, 6, [2,1,2,3,6,9]);
CheckTarget("search/probe/pl_lab1_v1/PQ_OUTPUT_p7c6.g", 7, 6, [2,1,2,3,6,9]);
CheckTarget("search/probe/pl_lab1_v1/PQ_OUTPUT_p7c7.g", 7, 7, [2,1,2,3,6,9,18]);

Print("EXP3_DONE\n");
QUIT;
