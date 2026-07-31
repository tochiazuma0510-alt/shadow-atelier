# u7_pathB_gap_v2.g -- fast reimplementation of the T-W1/T-W2 independent GAP
# check, using plain integer-indexed arrays (fast) instead of String-keyed
# records (slow in GAP for this size). Same construction as
# search/probe/wac_v1/tw_blocks.py / tw_orient.py, reimplemented independently.
#
# Pure finite-group/permutation computation only. NO curve/lambda/u/valuation
# contact. n=5 excluded (freeze U7-NO5). Does NOT evaluate [gamma]/[delta]/u7.
# New mechanical check added: does <X^2> (Phi(F_0) generator per
# phifam_v1.md L67: Phi(F_0)=inn(<X^2>)) stabilize each AH-block of Lambda?

SGN := [ [1,1,1], [1,-1,-1], [-1,1,-1], [-1,-1,1] ];  # index qi+1, qi=0..3 <-> 1,q1,q2,q3

# Q multiplication table QMUL[qi+1][qj+1] = qk (0-based), s.t. SGN[qi+1]*SGN[qj+1] componentwise = SGN[qk+1]
QMUL := List([1..4], i -> List([1..4], j ->
    Position(SGN, List([1..3], t -> SGN[i][t]*SGN[j][t])) - 1));

RunWindow := function(n, alpha)
    local enc, dec, mul, inv, sizeG,
          U, s, t, Hlist, Hset,
          AHlist,
          X, Y, XY, Z, X2, Z2,
          canon, reps, L, code, ck, k, i, j, jj,
          hcodes, sortedH, minCode, gElts,
          permOf, pX, pY, pZ,
          conjSet, NGeqH, NGset, core, coreSet, a2set, sizeM,
          seen, nb, blk, stack, x2, y2, blocks, bsizes,
          ctype, typY, fixYperBlock, typYperBlock,
          Xswaps, X2stabAll, ratios, phi, xx, ok, y3, block0, r,
          res, blkOfPt, permOfX2, permOfZ2, HInAH;

    enc := function(v, qi) return ((v[1]*n + v[2])*n + v[3])*4 + qi; end;
    dec := function(x)
        local qi, y, cc, bb, aa;
        qi := x mod 4; y := QuoInt(x,4);
        cc := y mod n; y := QuoInt(y,n);
        bb := y mod n; aa := QuoInt(y,n);
        return [[aa,bb,cc], qi];
    end;
    mul := function(x, y)
        local dx, dy, v, qi, w, qj, s1, aw, vsum, qr;
        dx := dec(x); dy := dec(y);
        v := dx[1]; qi := dx[2]; w := dy[1]; qj := dy[2];
        s1 := SGN[qi+1];
        aw := [ w[1]*s1[1], w[2]*s1[2], w[3]*s1[3] ];
        vsum := [ (v[1]+aw[1]) mod n, (v[2]+aw[2]) mod n, (v[3]+aw[3]) mod n ];
        qr := QMUL[qi+1][qj+1];
        return enc(vsum, qr);
    end;
    inv := function(x)
        local dx, v, qi, s1;
        dx := dec(x); v := dx[1]; qi := dx[2]; s1 := SGN[qi+1];
        # inverse of (v,qi) is (act(qi,-v), qi); reduce mod n AFTER applying the
        # sign so negative sign*positive-residue combinations land back in [0,n-1]
        return enc( [ ((-v[1])*s1[1]) mod n, ((-v[2])*s1[2]) mod n, ((-v[3])*s1[3]) mod n ], qi );
    end;

    sizeG := 4*n^3;

    # H = H_{2,alpha,0}: U = { s*e2 + t*(alpha e1 + e3) : s,t in Z/n }, coset reps with q in {0,2}
    Hlist := [];
    for s in [0..n-1] do for t in [0..n-1] do
        Add(Hlist, enc([ (alpha*t) mod n, s, t ], 0));
        Add(Hlist, enc([ (alpha*t) mod n, s, t ], 2));
    od; od;
    Hset := Set(Hlist);

    AHlist := [];
    for i in [0..n-1] do for j in [0..n-1] do for jj in [0..n-1] do
        Add(AHlist, enc([i,j,jj], 0));
        Add(AHlist, enc([i,j,jj], 2));
    od; od; od;

    X := enc([1,0,0], 1);
    Y := enc([1,1,1], 2);
    XY := mul(X, Y);
    Z := inv(XY);
    X2 := mul(X, X);
    Z2 := mul(Z, Z);

    # coset canonical rep: min integer code among {mul(g,h): h in Hset}
    canon := ListWithIdenticalEntries(sizeG, 0); # canon[code+1] = coset id (1-based)
    reps := [];
    for code in [0..sizeG-1] do
        if canon[code+1] <> 0 then continue; fi;
        hcodes := List(Hset, h -> mul(code, h));
        minCode := Minimum(hcodes);
        Add(reps, minCode);
        L := Length(reps);
        for ck in hcodes do
            canon[ck+1] := L;
        od;
    od;
    L := Length(reps);

    permOf := function(g)
        local p, kk;
        p := [];
        for kk in [1..L] do
            p[kk] := canon[ mul(g, reps[kk]) + 1 ];
        od;
        return PermList(p);
    end;

    pX := permOf(X); pY := permOf(Y); pZ := permOf(Z);
    permOfX2 := permOf(X2); permOfZ2 := permOf(Z2);

    # N_G(H) = { g in G : gHg^-1 = H }; check this SET equals H (not "is H normal in G")
    gElts := [0..sizeG-1];
    NGset := Filtered(gElts, code -> Set(List(Hset, h -> mul(mul(code,h), inv(code)))) = Hset);
    NGeqH := (Set(NGset) = Hset);

    # core = intersection of all conjugates of H
    core := Hset;
    for code in gElts do
        core := Intersection(core, Set(List(Hset, h -> mul(mul(code,h), inv(code)))));
        if Length(core) = n then break; fi; # already down to <a2> (size n), can't shrink further meaningfully
    od;
    a2set := Set(List([0..n-1], s -> enc([0,s,0], 0)));
    coreSet := (Set(core) = a2set);
    sizeM := sizeG / Length(core);

    # blocks = AH-orbits on {1..L}
    seen := List([1..L], i -> -1);
    nb := 0; blocks := [];
    for k in [1..L] do
        if seen[k] <> -1 then continue; fi;
        nb := nb + 1;
        blk := [k]; seen[k] := nb; stack := [k];
        while Length(stack) > 0 do
            x2 := Remove(stack);
            for code in AHlist do
                y2 := canon[ mul(code, reps[x2]) + 1 ];
                if seen[y2] = -1 then
                    seen[y2] := nb; Add(stack, y2); Add(blk, y2);
                fi;
            od;
        od;
        Add(blocks, blk);
    od;
    bsizes := List(blocks, Length);

    ctype := function(p, dom)
        local seenc, t2, ss2, cc2, xx2;
        seenc := []; t2 := [];
        for ss2 in dom do
            if ss2 in seenc then continue; fi;
            cc2 := 1; xx2 := ss2^p;
            Add(seenc, ss2);
            while xx2 <> ss2 do
                Add(seenc, xx2); xx2 := xx2^p; cc2 := cc2 + 1;
            od;
            Add(t2, cc2);
        od;
        Sort(t2, function(x,y) return x > y; end);
        return t2;
    end;

    typY := ctype(pY, [1..L]);
    fixYperBlock := List(blocks, b -> Length(Filtered(b, k -> k^pY = k)));
    typYperBlock := List(blocks, b -> ctype(pY, b));

    Xswaps := (blocks[1][1]^pX in Set(blocks[2]));

    X2stabAll := true;
    for k in [1..L] do
        if seen[k^permOfX2] <> seen[k] then X2stabAll := false; break; fi;
    od;

    ratios := [];
    for blk in blocks do
        block0 := blk[1];
        phi := ListWithIdenticalEntries(L, -1);
        xx := block0;
        for j in [0..n-1] do
            phi[xx] := j; xx := xx^permOfX2;
        od;
        r := phi[ block0^permOfZ2 ];
        ok := true;
        for y3 in blk do
            if (phi[y3^permOfZ2] - phi[y3]) mod n <> r then ok := false; break; fi;
        od;
        Add(ratios, [r, ok]);
    od;

    res := rec(
        n := n, alpha := alpha,
        sizeG := sizeG, sizeH := Length(Hset), L := L,
        NG_eq_H := NGeqH, core_is_a2 := coreSet, coreSize := Length(core), sizeM := sizeM,
        blocks := bsizes,
        X_swaps_blocks := Xswaps,
        X2_stabilizes_all_blocks := X2stabAll,
        typeY := typY,
        fixY_per_block := fixYperBlock,
        typeY_per_block := typYperBlock,
        ratios_r0_rinf_per_block := List(ratios, r -> r[1]),
        ratio_translation_consistent := List(ratios, r -> r[2]),
        sum_ratios_mod_n := (ratios[1][1] + ratios[2][1]) mod n
    );
    return res;
end;

WindowToRecord := function(r)
    return r;
end;

Print("=== u7_pathB_gap_v2: independent GAP re-derivation of T-W1/T-W2 (n=3,7,9,11,13) ===\n");
Print("=== plus new check: does <X^2> (Phi(F_0) generator) stabilize each block? ===\n\n");

ns := [3, 7, 9, 11, 13];  # n=5 excluded per freeze U7-NO5
allResults := [];
for n in ns do
    for alpha in [1 .. QuoInt(n-1,2)] do
        r := RunWindow(n, alpha);
        Print(r, "\n");
        Add(allResults, r);
    od;
od;

Print("\n=== SUMMARY ===\n");
okAll := true;
for r in allResults do
    if r.core_is_a2 then
        if r.blocks <> [r.n, r.n] then
            okAll := false; Print("MISMATCH blocks: n=", r.n, " alpha=", r.alpha, "\n");
        fi;
        if r.fixY_per_block <> [1,1] then
            okAll := false; Print("MISMATCH fixY: n=", r.n, " alpha=", r.alpha, "\n");
        fi;
        if not r.X2_stabilizes_all_blocks then
            okAll := false; Print("MISMATCH X2 does not stabilize blocks: n=", r.n, " alpha=", r.alpha, "\n");
        fi;
        if r.sum_ratios_mod_n <> 0 then
            okAll := false; Print("MISMATCH ratio sum: n=", r.n, " alpha=", r.alpha, "\n");
        fi;
        if not r.X_swaps_blocks then
            okAll := false; Print("MISMATCH X does not swap blocks: n=", r.n, " alpha=", r.alpha, "\n");
        fi;
    fi;
od;
if okAll then
    Print("ALL-CONSISTENT (GAP independent system)\n");
else
    Print("SOME-MISMATCH (GAP independent system)\n");
fi;
