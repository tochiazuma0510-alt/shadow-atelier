#############################################################################
## search/ss_gap1_pc5_v1.g
## SS-GAP-1 Stage 0 / PC-5: SL(2,Z/p^2) (p=3,5,7) で
##   A^2=1 (i_2) と B^3=1 (i_3) の個数を "全数列挙"(実際に行列積を計算)で数える。
## これは docs/notes/ss_gap1_count_spec_v1.md 4.1 の Cayley-Hamilton 閉形式
## (tr=0 かつ det=-1 / tr^3=-1 かつ det=tr^2, 非スカラー・スカラーは別枠)
## と独立実装(python, search/ss_gap1_pc5_crosscheck.py)で突き合わせるための
## 探索器(GAP)側 = 実際に行列を掛け算して A^2, B^3 を計算するブルートフォース。
## 出力: search/certs/ss_gap1_pc5_gap_v1_<date>.json (生値のみ)
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");

primes := [3,5,7];
results := [];

for p in primes do
    n := p*p;
    Zn := Integers mod n;
    zero := Zero(Zn);
    elts := List([0..n-1], k -> k*One(Zn));

    countGroup := 0;   # |SL(2,Z/p^2)|
    i2_total := 0;      # #{A in SL2: A^2 = I}  (all, scalar+nonscalar)
    i3_total := 0;      # #{B in SL2: B^3 = I}
    i2_scalar := 0;
    i3_scalar := 0;
    i2_nonscalar := 0;
    i3_nonscalar := 0;

    Id2 := IdentityMat(2, Zn);

    for a in elts do
      for b in elts do
        for c in elts do
          for d in elts do
            det := a*d - b*c;
            if det = One(Zn) then
                countGroup := countGroup + 1;
                A := [[a,b],[c,d]];
                Asq := A*A;
                isScalar := (b = zero) and (c = zero) and (a = d);
                if Asq = Id2 then
                    i2_total := i2_total + 1;
                    if isScalar then
                        i2_scalar := i2_scalar + 1;
                    else
                        i2_nonscalar := i2_nonscalar + 1;
                    fi;
                fi;
                Acu := Asq*A;
                if Acu = Id2 then
                    i3_total := i3_total + 1;
                    if isScalar then
                        i3_scalar := i3_scalar + 1;
                    else
                        i3_nonscalar := i3_nonscalar + 1;
                    fi;
                fi;
            fi;
          od;
        od;
      od;
    od;

    expectedOrder := p^4*(p^2-1);

    rec_p := rec(
        p := p,
        n := n,
        group_order_counted := countGroup,
        group_order_formula := expectedOrder,
        group_order_match := (countGroup = expectedOrder),
        i2_total := i2_total,
        i2_scalar := i2_scalar,
        i2_nonscalar := i2_nonscalar,
        i3_total := i3_total,
        i3_scalar := i3_scalar,
        i3_nonscalar := i3_nonscalar
    );
    Add(results, rec_p);
    Print("p=", p, " done: |SL2|=", countGroup, " (formula ", expectedOrder, ") i2=", i2_total, " i3=", i3_total, "\n");
od;

# JSON 出力
out := OutputTextFile("search/certs/ss_gap1_pc5_gap_v1_20260813.json", false);
SetPrintFormattingStatus(out, false);
PrintTo(out, "{\"schema\":\"ss_gap1_pc5_gap/v1\",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/ss_gap1_pc5_v1.g\",\"order\":\"SS-GAP-1 Stage0 PC-5\"},\"method\":\"brute_force_matrix_mult_full_enumeration_SL2_Zmod_p2\",\"note\":\"i2 = #{A in SL(2,Z/p^2): A*A=I} computed by ACTUAL matrix multiplication, not the CH shortcut. i3 analogous with B*B*B=I.\",\"results\":[");
first := true;
for rec_p in results do
    if not first then
        PrintTo(out, ",");
    fi;
    first := false;
    PrintTo(out, "{\"p\":", rec_p.p,
                  ",\"n\":", rec_p.n,
                  ",\"group_order_counted\":", rec_p.group_order_counted,
                  ",\"group_order_formula\":", rec_p.group_order_formula,
                  ",\"group_order_match\":", rec_p.group_order_match,
                  ",\"i2_total\":", rec_p.i2_total,
                  ",\"i2_scalar\":", rec_p.i2_scalar,
                  ",\"i2_nonscalar\":", rec_p.i2_nonscalar,
                  ",\"i3_total\":", rec_p.i3_total,
                  ",\"i3_scalar\":", rec_p.i3_scalar,
                  ",\"i3_nonscalar\":", rec_p.i3_nonscalar,
                  "}");
od;
PrintTo(out, "],\"u_touched\":false,\"c_touched\":false,\"d_no_interpretation\":\"machine values only; verdict は司令塔\"}");
CloseStream(out);

Print("DONE. wrote search/certs/ss_gap1_pc5_gap_v1_20260813.json\n");
