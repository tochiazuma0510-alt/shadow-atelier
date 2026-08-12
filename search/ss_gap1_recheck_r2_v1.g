#############################################################################
## search/ss_gap1_recheck_r2_v1.g
## [S0-RECHECK] [R-1]/[R-2]: PRED-S0-4 の trace 縮約(python と独立実装)
## p=37,41,43,47 で i2,i3,|Q_p| を整数で算出。
## docs/notes/ssg1_stage0_pred_repair_v1.md §3/§4 対応。
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");

primes := [37,41,43,47];
results := [];

BCHistogram := function(n)
    local hist, b, c;
    hist := ListWithIdenticalEntries(n, 0);
    for b in [0..n-1] do
        for c in [0..n-1] do
            hist[((b*c) mod n) + 1] := hist[((b*c) mod n) + 1] + 1;
        od;
    od;
    return hist;
end;

CountTraceDet := function(t, e, n, hist)
    local total, a, d, kappa;
    total := 0;
    for a in [0..n-1] do
        d := (t - a) mod n;
        kappa := ((a*d - e) mod n);
        total := total + hist[kappa + 1];
    od;
    return total;
end;

for p in primes do
    n := p*p;
    hist := BCHistogram(n);
    count_tr0 := CountTraceDet(0, 1, n, hist);
    count_tr1 := CountTraceDet(1, 1, n, hist);
    count_trm1 := CountTraceDet((-1) mod n, 1, n, hist);
    i2 := 1 + count_tr0/2;
    i3 := 1 + (count_tr1 + count_trm1)/2;
    Qorder := p^4*(p^2-1)/2;
    Add(results, rec(p:=p, n:=n, i2:=i2, i3:=i3, Qorder:=Qorder));
    Print("p=",p," i2=",i2," i3=",i3," |Q|=",Qorder,"\n");
od;

out := OutputTextFile("search/certs/ss_gap1_recheck_r2_gap_20260813.json", false);
SetPrintFormattingStatus(out, false);
PrintTo(out, "{\"schema\":\"ss_gap1_recheck_r2_gap/v1\",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/ss_gap1_recheck_r2_v1.g\"},\"method\":\"trace_det_histogram_independent_GAP_implementation\",\"results\":[");
first := true;
for r in results do
    if not first then PrintTo(out, ","); fi;
    first := false;
    PrintTo(out, "{\"p\":", r.p, ",\"n\":", r.n, ",\"i2\":", r.i2, ",\"i3\":", r.i3, ",\"Qorder\":", r.Qorder, "}");
od;
PrintTo(out, "],\"u_touched\":false,\"c_touched\":false,\"d_no_interpretation\":\"machine values only; verdict は司令塔\"}");
CloseStream(out);
Print("DONE.\n");
