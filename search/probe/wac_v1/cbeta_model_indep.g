# C-beta stage 3'-a/b/c, INDEPENDENT implementer execution (commander order 2026-08-01,
# ruling 310, C-beta section of docs/notes/u7_fire_log_v1_addendum_grade.md Sec 4.2.3).
#
# INDEPENDENT re-derivation from the handbook (Sec 4.2.3.2-4), written in GAP (not imported
# from the mathematician's self-check search/probe/wac_v1/cbeta_model.py / cbeta_nielsen.py,
# which are python and use a different construction technique: per-element python loops with
# hand-rolled coset canonicalisation. Here we use GAP's native regular representation +
# ActionHomomorphism + RightCosets, the SAME machinery already used for the abstract side in
# search/probe/wac_v1/u7_cbeta_marked_triple.g -- this file does not read the python files.
#
# Model-side data (Sec 4.2.3.2), generalised so item 4 (C-beta-IND dummy-h self-check) can
# swap in an arbitrary alphaLabel instead of the window's alpha:
#   h(k) = (k-i)^r0 (k+i)^{-r0} (k-1)^rinf (k+1)^{-rinf},   g(k) = (k+1)/(k-1)
#   V4 = < sigma: k->-k, theta: k->1/k >  (commuting involutions)
#   Abar^dual = (Z/n)^2 with characters (c_h,c_g)
#   sigma . (c_h,c_g)      = (-c_h, -c_g)
#   theta . (c_h,c_g)      = (-c_h + 2*alphaLabel*c_g, c_g)
#   (sigma*theta).(c_h,c_g)= (c_h - 2*alphaLabel*c_g, -c_g)      [= sigma.(theta.(c_h,c_g)),
#                                                                   verified they commute]
#
# chi values read directly from the divisor of h (Sec 4.2.3.3):
#   chi_0   (over k=i,  v=sigma*theta) = (r0, 0)
#   chi_inf (over k=1,  v=theta)       = (rinf, -1)
#   chi_1   (over k=0,  v=sigma)       = (0,0)          [Kummer-unramified]
# For the window family r0=1, rinf=-alpha, so chi_0=(1,0), chi_inf=(-alpha,-1) as in the
# handbook table.

# ---------- generic abstract-side builder (same technique as u7_cbeta_marked_triple.g) ----------
# EXTENDED 2026-08-01 (ruling 312, commander cross-table order): the abstract H is now the
# oddH_full_proof_v1.md Sec 2 family H_{j,alpha,beta} = < a_j, a1^alpha * a_{j'}, a1^beta * q_j >
# with j=2, beta=0, i.e. H_{2,alphaPrime,0} = < a2, a1^alphaPrime * a3, q2 >. alphaPrime=1
# reproduces the original u7_cbeta_marked_triple.g / u7_thirdroute_cbeta_20260801.json H
# exactly. markX, markY, markZ themselves (a1*q1, a1*a2*a3*q2, inverse product) do NOT
# depend on alphaPrime -- only which subgroup H (hence which coset action / which images of
# X,Y,Z) does. This is what makes a 3x3 cross table model(alpha) x abstract(alphaPrime)
# meaningful: same three group elements, three different marked quotients.
BuildAbstract := function(n, alphaPrime)
    local D, gens, r, s, D3, emb1, emb2, emb3, a1, a2, a3, q1, q2, markX, markY, markZ,
          G7, H, act, Ximg, Yimg, Zimg, M;
    D := DihedralGroup(IsPermGroup, 2*n);;
    gens := GeneratorsOfGroup(D);;
    r := gens[1];; s := gens[2];;
    D3 := DirectProduct(D, D, D);;
    emb1 := Embedding(D3,1);; emb2 := Embedding(D3,2);; emb3 := Embedding(D3,3);;
    a1 := Image(emb1,r);; a2 := Image(emb2,r);; a3 := Image(emb3,r);;
    q1 := Image(emb2,s)*Image(emb3,s);;
    q2 := Image(emb1,s)*Image(emb3,s);;
    G7 := Group(a1,a2,a3,q1,q2);;
    markX := a1*q1;; markY := a1*a2*a3*q2;; markZ := (markX*markY)^-1;;
    H := Subgroup(G7, [a2, a1^alphaPrime*a3, q2]);;
    act := ActionHomomorphism(G7, RightCosets(G7,H), OnRight);;
    Ximg := Image(act,markX);; Yimg := Image(act,markY);; Zimg := Image(act,markZ);;
    M := Group(Ximg,Yimg,Zimg);;
    return rec(deg:=2*n, X:=Ximg, Y:=Yimg, Z:=Zimg, M:=M,
               G7order:=Size(G7), Horder:=Size(H), Morder:=Size(M),
               transitive:=IsTransitive(M,[1..2*n]));
end;;

# BFS-canonical relabelling of a transitive 2-generator permutation pair (g0,g1) on `deg`
# points, starting from point `start`. Used to test simultaneous conjugacy without computing
# a normaliser: (g0,g1) and (g0',g1') generate conjugate marked triples iff some canonical
# form of (g0,g1) from some start point equals some canonical form of (g0',g1').
CanonForm := function(g0, g1, deg, start)
    local lab, order, i, x, gg, y, rl, p;
    lab := [];; order := [start];; lab[start] := 0;;
    i := 1;;
    while i <= Length(order) do
        x := order[i]; i := i+1;
        for gg in [g0,g1] do
            y := x^gg;
            if not IsBound(lab[y]) then
                lab[y] := Length(order);
                Add(order, y);
            fi;
        od;
    od;
    if Length(order) <> deg then return fail; fi;
    rl := function(p) return List(order, j -> lab[j^p]); end;;
    return [rl(g0), rl(g1)];
end;;

TripleConjugate := function(g0a, g1a, dega, g0b, g1b, degb)
    local s, ca, cb;
    if dega <> degb then return false; fi;
    ca := CanonForm(g0a, g1a, dega, 1);
    if ca = fail then return fail; fi;
    for s in [1..degb] do
        cb := CanonForm(g0b, g1b, degb, s);
        if cb = ca then return true; fi;
    od;
    return false;
end;;

# ---------- model-side builder (Sec 4.2.3.2-4) ----------
BuildModel := function(n, r0, rinf, alphaLabel)
    local idx, elts, ch, cg, v, VT, vact, mul, one, invElt, genElts, genPerms, g,
          Ggrp, Hperm, Hgrp, act, Mperm, imgOf, chi0, chi1, chiInf,
          C0, C1, Cinf, x, sq, x0, x1, xi, g0img, g1img, giimg, gensub,
          triples, seen, orbits, orb, c, key, triplesB, seenB, orbitsB;

    idx := function(t) return t[3]*n^2 + t[1]*n + t[2] + 1; end;;
    elts := [];;
    for v in [0..3] do
        for ch in [0..n-1] do
            for cg in [0..n-1] do
                Add(elts, [ch,cg,v]);
            od;
        od;
    od;;

    VT := [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]];;

    vact := function(v, ch, cg)
        if v = 0 then return [ch, cg];
        elif v = 1 then return [ (-ch) mod n, (-cg) mod n ];
        elif v = 2 then return [ (-ch + 2*alphaLabel*cg) mod n, cg mod n ];
        else return [ (ch - 2*alphaLabel*cg) mod n, (-cg) mod n ]; fi;
    end;;

    mul := function(x,y)
        local a;
        a := vact(x[3], y[1], y[2]);
        return [ (x[1]+a[1]) mod n, (x[2]+a[2]) mod n, VT[x[3]+1][y[3]+1] ];
    end;;

    one := [0,0,0];;

    invElt := function(x)
        local a;
        # x*(a,v)=one  =>  v = x[3] (self-inverse in V4), and x[1..2] + vact(x[3],a) = (0,0)
        a := vact(x[3], (-x[1]) mod n, (-x[2]) mod n);
        return [a[1], a[2], x[3]];
    end;;

    genElts := [ [1,0,0], [0,1,0], [0,0,1], [0,0,2] ];;
    genPerms := List(genElts, g -> PermList(List(elts, y -> idx(mul(g,y)))));;
    Ggrp := Group(genPerms);;

    Hperm := List([ [0,1,0], [0,0,1] ], g -> PermList(List(elts, y -> idx(mul(g,y)))));;
    Hgrp := Subgroup(Ggrp, Hperm);;

    act := ActionHomomorphism(Ggrp, RightCosets(Ggrp,Hgrp), OnRight);;
    Mperm := Image(act, Ggrp);;

    imgOf := function(t) return Image(act, PermList(List(elts, y -> idx(mul(t,y))))); end;;

    chi0 := [ r0 mod n, 0 ];;
    chiInf := [ rinf mod n, (n-1) mod n ];;   # (-1) mod n written positively
    chi1 := [0,0];;

    C0 := [];;
    for ch in [0..n-1] do
        for cg in [0..n-1] do
            x := [ch,cg,3];
            sq := mul(x,x);
            if [sq[1],sq[2]] = chi0 then Add(C0, x); fi;
        od;
    od;;

    Cinf := [];;
    for ch in [0..n-1] do
        for cg in [0..n-1] do
            x := [ch,cg,2];
            sq := mul(x,x);
            if [sq[1],sq[2]] = chiInf then Add(Cinf, x); fi;
        od;
    od;;

    C1 := [];;
    for ch in [0..n-1] do
        for cg in [0..n-1] do
            Add(C1, [ch,cg,1]);
        od;
    od;;

    # Nielsen triple search on the degree-2n images: x0 in C0, x1 in C1, want
    # (imgOf(x0)*imgOf(x1)*imgOf(xi))=identity for some xi in Cinf, and the three images
    # generate the full Mperm.
    #
    # S9 (product_order self-check, commander order 2026-08-01): the handbook Sec 4.2.3.5
    # item 4 flags TWO independent conventions for "g0 g1 ginf = 1":
    #   ORDER-A (GAP-native): g0img*g1img*giimg = One   [x^(pq) = (x^p)^q, "p then q"]
    #   ORDER-B (reversed):   giimg*g1img*g0img = One   [(pq)(x)=p(q(x)) math convention,
    #                          i.e. relator read right-to-left under GAP multiplication]
    # Both are computed; results tabulated separately (triplesA/triplesB, orbitsA/orbitsB).
    triples := [];;    # ORDER-A
    triplesB := [];;   # ORDER-B
    for x0 in C0 do
        g0img := imgOf(x0);
        for x1 in C1 do
            g1img := imgOf(x1);
            for xi in Cinf do
                giimg := imgOf(xi);
                if g0img*g1img*giimg = One(Mperm) then
                    gensub := Group(g0img, g1img);
                    if Size(gensub) = Size(Mperm) then
                        Add(triples, [g0img, g1img, giimg]);
                    fi;
                fi;
                if giimg*g1img*g0img = One(Mperm) then
                    gensub := Group(g0img, g1img);
                    if Size(gensub) = Size(Mperm) then
                        Add(triplesB, [g0img, g1img, giimg]);
                    fi;
                fi;
            od;
        od;
    od;;

    # orbits under simultaneous Mperm-conjugation (ORDER-A)
    seen := [];; orbits := [];;
    for x in triples do
        key := ViewString(x);
        if key in seen then continue; fi;
        orb := [];;
        for c in Mperm do
            Add(orb, [x[1]^c, x[2]^c, x[3]^c]);
        od;
        orb := DuplicateFreeList(orb);
        Append(seen, List(orb, ViewString));
        Add(orbits, orb);
    od;;

    # orbits under simultaneous Mperm-conjugation (ORDER-B)
    seenB := [];; orbitsB := [];;
    for x in triplesB do
        key := ViewString(x);
        if key in seenB then continue; fi;
        orb := [];;
        for c in Mperm do
            Add(orb, [x[1]^c, x[2]^c, x[3]^c]);
        od;
        orb := DuplicateFreeList(orb);
        Append(seenB, List(orb, ViewString));
        Add(orbitsB, orb);
    od;;

    return rec(n:=n, r0:=r0, rinf:=rinf, alphaLabel:=alphaLabel, deg:=2*n,
               Ggrp:=Ggrp, Hgrp:=Hgrp, Mperm:=Mperm,
               C0:=C0, C1:=C1, Cinf:=Cinf, chi0:=chi0, chi1:=chi1, chiInf:=chiInf,
               triples:=triples, orbits:=orbits,
               triplesB:=triplesB, orbitsB:=orbitsB, imgOf:=imgOf);
end;;

# ---------------------------------------------------------------------------
# driver: window cases (n=7, alpha=1,2,3), calibration (n=3, alpha=1), and the
# C-beta-IND dummy-h self-check (n=7, alphaLabel out of window e.g. 4).
# ---------------------------------------------------------------------------
RunCase := function(n, alpha, label)
    local m, a, ordersC0, ordersCinf, cyctypesC0, cyctypesCinf, cyctypeC1,
          ok, x, cf_abstract, matched, matchedB, t;
    m := BuildModel(n, 1, (-alpha) mod n, alpha);;
    a := BuildAbstract(n, 1);;   # fixed H_{2,1,0} abstract side, as in the original 20260801 cert
    ordersC0 := DuplicateFreeList(List(m.C0, x -> Order(m.imgOf(x))));;
    ordersCinf := DuplicateFreeList(List(m.Cinf, x -> Order(m.imgOf(x))));;
    cyctypesC0 := DuplicateFreeList(List(m.C0, x -> CycleStructurePerm(m.imgOf(x))));;
    cyctypesCinf := DuplicateFreeList(List(m.Cinf, x -> CycleStructurePerm(m.imgOf(x))));;
    cyctypeC1 := DuplicateFreeList(List(m.C1, x -> CycleStructurePerm(m.imgOf(x))));;

    matched := false;;
    for t in m.triples do
        ok := TripleConjugate(t[1], t[2], m.deg, a.X, a.Y, a.deg);
        if ok = true then matched := true; break; fi;
    od;;

    # S9 (product_order self-check): repeat S4/S5/S6 under ORDER-B (reversed convention)
    matchedB := false;;
    for t in m.triplesB do
        ok := TripleConjugate(t[1], t[2], m.deg, a.X, a.Y, a.deg);
        if ok = true then matchedB := true; break; fi;
    od;;

    Print("==== ", label, " (n=", n, ", alpha=", alpha, ") ====\n");
    Print("chi0=", m.chi0, " chi1=", m.chi1, " chiInf=", m.chiInf, "\n");
    Print("|Ggrp|(=|M^mod| abstract-regular)=", Size(m.Ggrp),
          "  expected 4n^2=", 4*n^2, "\n");
    Print("|Hgrp|=", Size(m.Hgrp), " expected 2n=", 2*n, "\n");
    Print("|Mperm|(model monodromy on ", m.deg, " pts)=", Size(m.Mperm),
          " expected 4n^2=", 4*n^2, "\n");
    Print("|C0|=", Length(m.C0), " orders(C0 images)=", ordersC0,
          " cyctypes(C0)=", cyctypesC0, "\n");
    Print("|Cinf|=", Length(m.Cinf), " orders(Cinf images)=", ordersCinf,
          " cyctypes(Cinf)=", cyctypesCinf, "\n");
    Print("|C1|=", Length(m.C1), " cyctypes(C1 images)=", cyctypeC1, "\n");
    Print("n_triples=", Length(m.triples), " n_orbits=", Length(m.orbits),
          " orbit_sizes=", List(m.orbits,Length), "\n");
    Print("abstract: |G7|=", a.G7order, " |H|=", a.Horder, " |M_abs|=", a.Morder,
          " transitive=", a.transitive, "\n");
    Print("MODEL_TRIPLE_MATCHES_ABSTRACT(any orbit member conj to (X,Y)) = ", matched, "\n");
    Print("--- S9 (product_order self-check, ORDER-B: giimg*g1img*g0img=One) ---\n");
    Print("n_triplesB=", Length(m.triplesB), " n_orbitsB=", Length(m.orbitsB),
          " orbit_sizesB=", List(m.orbitsB,Length), "\n");
    Print("MODEL_TRIPLE_MATCHES_ABSTRACT_ORDERB = ", matchedB, "\n");
    Print("\n");
end;;

Print("### C-beta stage 3'-a/b/c independent GAP execution ###\n\n");
RunCase(7, 1, "WINDOW");
RunCase(7, 2, "WINDOW");
RunCase(7, 3, "WINDOW");
RunCase(3, 1, "CALIBRATION n=3");

Print("### C-beta-IND self-check: dummy h (alphaLabel out of window, n=7) ###\n");
Print("operational test: same code, alphaLabel=99 (not 1,2,3) -- does it run to completion?\n");
RunCase(7, 99 mod 7, "DUMMY-H (alphaLabel=99 mod 7, i.e. same residue as alpha=1 -- see note)\n");
# NOTE: since alphaLabel only matters mod n in our construction (all arithmetic is mod n),
# a genuinely "different" alphaLabel must be tested by an out-of-{1,2,3} residue mod 7 that
# is not equivalent to any window case. Residues mod 7 coprime to structure: window uses
# alpha in {1,2,3} (representatives of [alpha] up to alpha<->alpha^{-1} etc per addendum).
# Use alphaLabel=5 (=-2 mod 7, distinct residue from 1,2,3,4=-3,6=-1) as the dummy.
RunCase(7, 5, "DUMMY-H (alphaLabel=5, out-of-window residue mod 7)");

Print("DONE\n");
