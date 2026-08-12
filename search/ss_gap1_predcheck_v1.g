#############################################################################
## search/ss_gap1_predcheck_v1.g
## SS-GAP-1: 数学者が凍結した予言4点(p=19,23,29,31)の GAP側独立実測。
## docs/notes/ssg1_stage0_pred_failure_v1.md 対応(裁定継続)。
## 同じ trace/det ヒストグラム法(search/ss_gap1_s0_v2.g と同一アルゴリズム、
## 独立コード)。python 側 search/scratchpad/predcheck_run.py の結果と突合。
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");

primes := [19,23,29,31];
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
    U := 2*i2*i3/Qorder;   # exact rational in GAP
    Add(results, rec(p:=p, n:=n, count_tr0:=count_tr0, count_tr1:=count_tr1,
        count_trm1:=count_trm1, i2:=i2, i3:=i3, Qorder:=Qorder, U:=U, Ufloat:=Float(U)));
    Print("p=",p," i2=",i2," i3=",i3," |Q|=",Qorder," U(exact)=",U," U(float)=",Float(U),"\n");
od;

out := OutputTextFile("search/certs/ss_gap1_predcheck_gap_20260813.json", false);
SetPrintFormattingStatus(out, false);
PrintTo(out, "{\"schema\":\"ss_gap1_predcheck_gap/v1\",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/ss_gap1_predcheck_v1.g\"},\"method\":\"trace_det_histogram_independent_GAP_implementation_exact_rational_U\",\"results\":[");
first := true;
for r in results do
    if not first then PrintTo(out, ","); fi;
    first := false;
    PrintTo(out, "{\"p\":", r.p, ",\"n\":", r.n,
                  ",\"count_tr0\":", r.count_tr0,
                  ",\"count_tr1\":", r.count_tr1,
                  ",\"count_trm1\":", r.count_trm1,
                  ",\"i2\":", r.i2,
                  ",\"i3\":", r.i3,
                  ",\"Qorder\":", r.Qorder,
                  ",\"U_exact_rational_string\":\"", r.U, "\"",
                  ",\"U_float\":", r.Ufloat,
                  "}");
od;
PrintTo(out, "],\"u_touched\":false,\"c_touched\":false,\"d_no_interpretation\":\"machine values only; verdict は司令塔\"}");
CloseStream(out);
Print("DONE.\n");
