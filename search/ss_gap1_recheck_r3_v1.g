#############################################################################
## search/ss_gap1_recheck_r3_v1.g
## [S0-RECHECK] [R-3]: 全数列挙対照(トレース近道を使わない)
## p=13 で SL(2,Z/169) の元を「原始第1列 (a,c)」で構成的に生成し
## (この生成法自体はトレース条件を一切使わない -- gcd(a,c,p)=1 という
## 別の判定条件のみ)、各元について A^2, A^3 を *実際の行列積* で計算し
## +-I への一致で分類する。これは docs/notes/ssg1_stage0_pred_repair_v1.md
## §4 [R-3] の要求どおり、[R-2] のトレース縮約とは独立の経路で
## i2_Qp = #{A in SL: A^2=I or A^2=-I}/2 , i3_Qp = #{A: A^3=I or A^3=-I}/2
## を数え、search/certs/ss_gap1_recheck_r2_gap_20260813.json の p=13相当値
## (元の ss_gap1_s0_v2.g 出力: i2=15380,i3=30759,|Q|=2399124)と突合する。
##
## 生成法: |SL(2,Z/n)| = n * #{(a,c): a,c not both ≡0 mod p}  (n=p^2)
##   各原始 (a,c) に対し、a が単元なら b を n 通り走らせ d=(1+bc)/a で決定、
##   さもなくば(その時は c が単元) d を n 通り走らせ b=(ad-1)/c で決定。
##   これにより各 SL 元がちょうど1回ずつ生成される(O(n^3) 個、O(n^2) の外側ループ)。
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");

p := 13;
n := p*p;

# precompute inverses mod n for units
inv := ListWithIdenticalEntries(n, 0);
for a in [1..n-1] do
    if Gcd(a, n) = 1 then
        inv[a+1] := Int(a^-1 mod n);
    fi;
od;

MyIsUnit := function(x)
    return Gcd(x, n) = 1;
end;

count_A2_I := 0;      # A = +-I trivially (scalar)
count_A2_negI := 0;   # A^2 = -I, nonscalar expected
count_A3_I := 0;
count_A3_negI := 0;
total_elts := 0;

for a in [0..n-1] do
    for c in [0..n-1] do
        if (a mod p = 0) and (c mod p = 0) then
            continue; # not primitive, skip
        fi;
        if MyIsUnit(a) then
            ai := inv[a+1];
            for b in [0..n-1] do
                d := (ai * (1 + b*c)) mod n;
                # matrix (a,b,c,d), det should be 1 -- sanity spot check omitted for speed
                total_elts := total_elts + 1;
                # A^2
                e := (a*a + b*c) mod n; f := (a*b + b*d) mod n;
                g := (c*a + d*c) mod n; h := (c*b + d*d) mod n;
                if e=1 and f=0 and g=0 and h=1 then
                    count_A2_I := count_A2_I + 1;
                elif e=(n-1) and f=0 and g=0 and h=(n-1) then
                    count_A2_negI := count_A2_negI + 1;
                fi;
                # A^3 = A^2 * A
                p1 := (e*a+f*c) mod n; q1 := (e*b+f*d) mod n;
                r1 := (g*a+h*c) mod n; s1 := (g*b+h*d) mod n;
                if p1=1 and q1=0 and r1=0 and s1=1 then
                    count_A3_I := count_A3_I + 1;
                elif p1=(n-1) and q1=0 and r1=0 and s1=(n-1) then
                    count_A3_negI := count_A3_negI + 1;
                fi;
            od;
        else
            # c must be unit since (a,c) primitive and a is not
            ci := inv[c+1];
            for d in [0..n-1] do
                b := (ci * (a*d - 1)) mod n;
                total_elts := total_elts + 1;
                e := (a*a + b*c) mod n; f := (a*b + b*d) mod n;
                g := (c*a + d*c) mod n; h := (c*b + d*d) mod n;
                if e=1 and f=0 and g=0 and h=1 then
                    count_A2_I := count_A2_I + 1;
                elif e=(n-1) and f=0 and g=0 and h=(n-1) then
                    count_A2_negI := count_A2_negI + 1;
                fi;
                p1 := (e*a+f*c) mod n; q1 := (e*b+f*d) mod n;
                r1 := (g*a+h*c) mod n; s1 := (g*b+h*d) mod n;
                if p1=1 and q1=0 and r1=0 and s1=1 then
                    count_A3_I := count_A3_I + 1;
                elif p1=(n-1) and q1=0 and r1=0 and s1=(n-1) then
                    count_A3_negI := count_A3_negI + 1;
                fi;
            od;
        fi;
    od;
od;

SL_order_formula := p^4*(p^2-1);
i2_full := (count_A2_I + count_A2_negI)/2;
i3_full := (count_A3_I + count_A3_negI)/2;

Print("total_elts=", total_elts, " (formula ", SL_order_formula, ")\n");
Print("count_A2_I=", count_A2_I, " count_A2_negI=", count_A2_negI, "\n");
Print("count_A3_I=", count_A3_I, " count_A3_negI=", count_A3_negI, "\n");
Print("i2_Qp(full enum)=", i2_full, "  i3_Qp(full enum)=", i3_full, "\n");

out := OutputTextFile("search/certs/ss_gap1_recheck_r3_gap_20260813.json", false);
SetPrintFormattingStatus(out, false);
PrintTo(out, "{\"schema\":\"ss_gap1_recheck_r3_gap/v1\",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/ss_gap1_recheck_r3_v1.g\"},\"method\":\"literal_full_enumeration_via_primitive_first_column_parametrization_NO_trace_shortcut_actual_matrix_multiplication_A2_A3\",\"p\":13,\"n\":169,\"total_elts_generated\":", total_elts,
      ",\"SL_order_formula\":", SL_order_formula,
      ",\"total_elts_match_formula\":", (total_elts = SL_order_formula),
      ",\"count_A2_eq_I\":", count_A2_I,
      ",\"count_A2_eq_negI\":", count_A2_negI,
      ",\"count_A3_eq_I\":", count_A3_I,
      ",\"count_A3_eq_negI\":", count_A3_negI,
      ",\"i2_Qp_full_enum\":", i2_full,
      ",\"i3_Qp_full_enum\":", i3_full,
      ",\"u_touched\":false,\"c_touched\":false,\"d_no_interpretation\":\"machine values only; verdict は司令塔\"}");
CloseStream(out);
Print("DONE.\n");
