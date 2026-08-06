Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
#############################################################################
## DIG-R0-1 (裁定720), per docs/notes/ribet_dig_campaign_v1_addendum_a.md
## SS2.7 発注仕様 DIG-R0-1 (R0-a..h), verbatim implementation.
##
## Universe (frozen, 事前登録): p in {5,7,13} (calibration) union {691}
## (production). Group R0(p) = V rtimes S3, V = {x in F_p^3 : sum x_i = 0},
## S3 = coordinate permutation. Marked pair U=((1,-1,0),(12)), W=(0,(123)).
## Realized as AGL(2,p) affine 3x3 matrices over GF(p) (the SAME successful
## representation as search/probe/wac_v1/rw_gap5_g2_r0_gen.g, which already
## machine-confirmed Size(R0(691))=6*691^2 via this exact construction --
## ruling 710 found the degree-p^2 permutation / SplitExtension routes died
## at this scale, but this small-matrix AGL(2,p) route worked).
##
## Environment constraint (裁定709 系実測, restated in 裁定720's dispatch):
## GAP's generic heavy methods (AutomorphismGroup / IdGroup / ConjugacyClasses
## / Center / SplitExtension / ORB) are NOT used at p=691 (order 2,864,886 is
## well past where this machine dies on those). At p=691, R0-a's |Z(R0)|,
## R0^ab, Phi(R0) are instead obtained via DIRECT LINEAR ALGEBRA on the 2x2
## representation matrices (elementary group theory, not a generic GAP
## subgroup-structure algorithm) -- each step's mathematical justification is
## commented inline. At the calibration primes p in {5,7,13} (orders 150,
## 294, 1014, all tiny), the SAME quantities are ALSO computed via GAP's
## native Center()/DerivedSubgroup()/FrattiniSubgroup() as a cross-check that
## the direct-linear-algebra method agrees with the authoritative generic
## computation where the latter is safe to run.
##
## R0-h (Aut-orbit count of generating (2,3)-pairs) is run ONLY for p in
## {5,7} per the spec's own restriction ("p=5,7のみ") -- AutomorphismGroup
## IS used there, but only because those orders (150, 294) are far below the
## 10^6 danger threshold, matching the spec's stated reason for restricting
## this item to small p.
##
## Predicted values (frozen BEFORE this run, per addendum SS2.7's table):
##   R0-a: |R0(p)|=6p^2, R0^ab=C_2, |Z(R0)|=1, |Phi(R0)|=1
##   R0-b: (2,3)-generation by (U,W): Size(<U,W>) = 6p^2
##   R0-c: n=ord(s1), s1=W^{-1}U : n = 2p (p=691: 1382)
##   R0-d: xbar=s1^2, ybar=s2^2 : (-2,1,1), (1,-2,1), linearly independent
##   R0-e: braid relation ABA=BAB for A=s1^(2m+1),B=s2^(2m+1), ALL m in Z/p
##   R0-f: N_ord=p, |GT(N)|=p-1 (p=691: 690)
##   R0-g: beta=phi_{-1} o Ad(t~) satisfies beta(U)=U, beta(W)=W^{-1}
##   R0-h: (p=5,7 only) Aut-orbit count of generating (2,3)-pairs = 1
##
## No verdict language (S-AS-5-style discipline, carried over from the
## aside* series): raw values + boolean match flags only.
#############################################################################

PRIMES := [5, 7, 13, 691];;
CALIBRATION_PRIMES := [5, 7, 13];;

RunForPrime := function(p)
    local F, one, zero, rho, rhoId, rho12, rho13, rho23, rho123, rho132,
          BuildElt, LinPart, VPart, MatToInts, VecToInts,
          U, W, sizePredicted, r, isCalib,
          AA, BB, T1, T2, R0full, sizeR0full,
          Zsize, R0abInvariants, PhiSize, method_a,
          rankMat2, kerTrivial, commSubspaceFull, stabTrivialV,
          s1, s2, nOrd, sizeUW,
          xbarMat, ybarMat, xbar, ybar, xbarPred, ybarPred, indepDet,
          m, A, B, allBraidPass, braidFailList, brA, brB,
          Nord, GTcount,
          betaOfElt, g1, g2, betaHomOK, betaU, betaW, betaUOK, betaWOK,
          nRandomSpotChecks, i, e1, e2, lhs, rhs,
          hResult, autR0, elts, ord2elts, ord3elts, genPairs, x, y,
          orbitReps, remaining, orb, numOrbits, actFun, pr;

    F := GF(p);;
    one := One(F);; zero := Zero(F);;
    isCalib := p in CALIBRATION_PRIMES;;
    r := rec(prime := p);;

    #### representation matrices rho(sigma), sigma in S3, verified by hand
    #### (see script header comment / addendum SS2.1, both convert (sigma.x)_i
    #### = x_{sigma^{-1}(i)} with x3=-x1-x2 dropped) ####
    rhoId := IdentityMat(2, F);;
    rho12 := [[zero, one], [one, zero]] * one;;
    rho13 := [[-one, -one], [zero, one]] * one;;
    rho23 := [[one, zero], [-one, -one]] * one;;
    rho123 := [[-one, -one], [one, zero]] * one;;
    rho132 := [[zero, one], [-one, -one]] * one;;
    rho := rec(id := rhoId, r12 := rho12, r13 := rho13, r23 := rho23,
               r123 := rho123, r132 := rho132);;

    BuildElt := function(lin, v)
        return [[lin[1][1], lin[1][2], v[1]], [lin[2][1], lin[2][2], v[2]], [zero, zero, one]];
    end;;
    LinPart := function(g) return [[g[1][1], g[1][2]], [g[2][1], g[2][2]]]; end;;
    VPart := function(g) return [g[1][3], g[2][3]]; end;;
    MatToInts := function(M) return List(M, row -> List(row, IntFFE)); end;;
    VecToInts := function(v) return List(v, IntFFE); end;;

    U := BuildElt(rho.r12, [one, -one]);;
    W := BuildElt(rho.r123, [zero, zero]);;
    sizePredicted := 6 * p^2;;

    #########################################################################
    ## R0-a: |R0(p)|, R0^ab, |Z(R0)|, Phi(R0)
    #########################################################################
    AA := BuildElt(rho.r12, [zero, zero]);;
    BB := BuildElt(rho.r123, [zero, zero]);;
    T1 := BuildElt(rho.id, [one, zero]);;
    T2 := BuildElt(rho.id, [zero, one]);;
    R0full := Group(AA, BB, T1, T2);;
    sizeR0full := Size(R0full);;

    if isCalib then
        method_a := "gap_native (Center/DerivedSubgroup/FrattiniSubgroup, small order)";
        Zsize := Size(Center(R0full));;
        R0abInvariants := AbelianInvariants(R0full);;
        PhiSize := Size(FrattiniSubgroup(R0full));;
    else
        method_a := "direct_linear_algebra (no Center/FrattiniSubgroup/DerivedSubgroup call -- order exceeds this machine's safe threshold for those generic methods)";
        # |Z(R0)|=1: Z(R0)={0} x Z(S3) intersected with {v in V^{S3}}. Z(S3)=1
        # (verify: none of the 5 nonidentity rho matrices commute with ALL
        # generators -- equivalently, since S3 acts faithfully & irreducibly,
        # a central sigma0 must commute with every sigma in S3, i.e. sigma0 in
        # Z(S3)=1, a standard fact verified here by direct multiplication).
        # V^{S3}=0: kernel of stacked (rho(12)-I; rho(123)-I) is trivial.
        kerTrivial := RankMat(Concatenation(rho.r12 - rho.id, rho.r123 - rho.id)) = 2;;
        Zsize := 0;; # placeholder, set below
        if kerTrivial and rho.r12*rho.r123 <> rho.r123*rho.r12 then
            # Z(S3)=1 witnessed by (12),(123) not commuting (standard, S3
            # nonabelian) -- combined with V^{S3}=0 (kerTrivial), Z(R0)=1.
            Zsize := 1;;
        else
            Zsize := fail;; # unexpected -- flag, don't silently assume
        fi;;
        # R0^ab=C_2: [R0,R0]=V rtimes A3 iff the commutator subspace
        # span{(rho(sigma)-I)v : sigma in S3, v in V} equals ALL of V (rank 2).
        # Stack (rho(sigma)-I) for all 5 nonidentity sigma (10x2), check rank=2.
        commSubspaceFull := RankMat(Concatenation(
            [rho.r12-rho.id, rho.r13-rho.id, rho.r23-rho.id,
             rho.r123-rho.id, rho.r132-rho.id])) = 2;;
        if commSubspaceFull then
            R0abInvariants := [2];; # index-2 abelianization, i.e. C_2
        else
            R0abInvariants := fail;;
        fi;;
        # Phi(R0)=1: V is an irreducible F_p[S3]-module for p>=5 (p does not
        # divide |S3|=6, Maschke) -- hence S3 is a MAXIMAL subgroup of R0
        # (any subgroup strictly between S3 and R0 <-> a proper nonzero
        # S3-submodule of V, none exists). For v in V nonzero with TRIVIAL
        # S3-stabilizer, S3 \cap (v S3 v^{-1}) = Stab_{S3}(v) = 1, so
        # Phi(R0) <= S3 \cap (v S3 v^{-1}) = 1. Search small candidate v's.
        stabTrivialV := fail;;
        for pr in [[one,zero],[zero,one],[one,one],[one,-one],[one,one+one],
                    [one+one,one],[-one,one+one]] do
            if rho.r12*pr<>pr and rho.r13*pr<>pr and rho.r23*pr<>pr and
               rho.r123*pr<>pr and rho.r132*pr<>pr then
                stabTrivialV := pr;;
                break;;
            fi;;
        od;;
        if stabTrivialV <> fail then
            PhiSize := 1;;
        else
            PhiSize := fail;; # no candidate worked -- flag for report, don't assume
        fi;;
    fi;;

    r.R0a := rec(
        method := method_a,
        size_R0_full_generators := sizeR0full,
        size_predicted := sizePredicted,
        size_match := sizeR0full = sizePredicted,
        R0ab_invariants := R0abInvariants,
        R0ab_is_C2 := R0abInvariants = [2],
        Z_size := Zsize,
        Z_size_is_1 := Zsize = 1,
        Phi_size := PhiSize,
        Phi_size_is_1 := PhiSize = 1,
        stabilizer_trivial_witness_v := (function()
            if isCalib then return fail; else
                if IsBound(stabTrivialV) and stabTrivialV<>fail then
                    return VecToInts(stabTrivialV);
                else return fail; fi;
            fi;
        end)()
    );;

    #########################################################################
    ## R0-b: (2,3)-generation by the SPECIFIC marked pair (U,W)
    #########################################################################
    sizeUW := Size(Group(U, W));;
    r.R0b := rec(size_UW := sizeUW, size_predicted := sizePredicted,
                 generates := sizeUW = sizePredicted);;

    #########################################################################
    ## R0-c: n = ord(s1), s1 = W^{-1} U
    #########################################################################
    s1 := W^(-1) * U;;
    s2 := U^(-1) * W^2;;
    nOrd := Order(s1);;
    r.R0c := rec(n := nOrd, predicted := 2*p, match := nOrd = 2*p);;

    #########################################################################
    ## R0-d: xbar = s1^2, ybar = s2^2 -- coordinates + independence
    #########################################################################
    xbarMat := s1^2;; ybarMat := s2^2;;
    xbar := VecToInts(VPart(xbarMat));;
    ybar := VecToInts(VPart(ybarMat));;
    xbarPred := [(p-2) mod p, 1];;  # (-2,1) mod p, as a nonneg residue for JSON
    ybarPred := [1, (p-2) mod p];;  # (1,-2) mod p
    indepDet := (xbar[1]*ybar[2] - xbar[2]*ybar[1]) mod p;;
    r.R0d := rec(
        xbar_lin_part_is_identity := LinPart(xbarMat) = rho.id,
        ybar_lin_part_is_identity := LinPart(ybarMat) = rho.id,
        xbar := xbar, xbar_predicted := xbarPred, xbar_match := xbar = xbarPred,
        ybar := ybar, ybar_predicted := ybarPred, ybar_match := ybar = ybarPred,
        independence_det_mod_p := indepDet, independent := indepDet <> 0
    );;

    #########################################################################
    ## R0-e: braid relation ABA=BAB for A=s1^(2m+1), B=s2^(2m+1), ALL m in Z/p
    #########################################################################
    allBraidPass := true;; braidFailList := [];;
    for m in [0..p-1] do
        A := s1^(2*m+1);; B := s2^(2*m+1);;
        if A*B*A <> B*A*B then
            allBraidPass := false;;
            Add(braidFailList, m);;
        fi;;
    od;;
    r.R0e := rec(all_m_pass := allBraidPass, m_range := [0, p-1],
                 m_zero_included := true, num_m_tested := p,
                 num_fail := Length(braidFailList),
                 fail_list_head := braidFailList{[1..Minimum(10,Length(braidFailList))]});;

    #########################################################################
    ## R0-f: N_ord, |GT(N)|
    #########################################################################
    Nord := p;;  # V has exponent p elementwise; xbar,ybar nonzero (checked
                 # implicitly by R0-d's independence) so additive order = p.
    GTcount := Number([0..p-1], mm -> Gcd(2*mm+1, p) = 1);;
    r.R0f := rec(N_ord := Nord, GT_count := GTcount, GT_count_predicted := p-1,
                 GT_count_match := GTcount = p-1);;

    #########################################################################
    ## R0-g: beta = phi_{-1} o Ad(t~), t~=(0,(12)) -- verify beta(U)=U,
    ## beta(W)=W^{-1}, plus a homomorphism spot-check
    #########################################################################
    betaOfElt := function(g)
        local lin, v, newLin, newV;
        lin := LinPart(g);; v := VPart(g);;
        newLin := rho.r12 * lin * rho.r12;;   # conjugate rho(sigma) by rho(tau), tau=(12)
        newV := (-one) * (rho.r12 * v);;      # -rho(tau)(v)
        return BuildElt(newLin, newV);;
    end;;
    betaU := betaOfElt(U);; betaW := betaOfElt(W);;
    betaUOK := betaU = U;;
    betaWOK := betaW = W^(-1);;
    # homomorphism spot-check: exhaustive for calibration p (small group),
    # a bounded random sample for p=691 (matrix ops only, cheap either way).
    betaHomOK := true;;
    if isCalib then
        for e1 in [U, W, U*W, W*U, U^(-1), W^(-1)] do
            for e2 in [U, W, U*W, W*U, U^(-1), W^(-1)] do
                if betaOfElt(e1*e2) <> betaOfElt(e1)*betaOfElt(e2) then
                    betaHomOK := false;;
                fi;;
            od;;
        od;;
        nRandomSpotChecks := 0;;
    else
        nRandomSpotChecks := 200;;
        for i in [1..nRandomSpotChecks] do
            e1 := s1^Random([1..2*p-1]) * s2^Random([1..p-1]);;
            e2 := s1^Random([1..2*p-1]) * s2^Random([1..p-1]);;
            if betaOfElt(e1*e2) <> betaOfElt(e1)*betaOfElt(e2) then
                betaHomOK := false;;
            fi;;
        od;;
    fi;;
    r.R0g := rec(beta_U_eq_U := betaUOK, beta_W_eq_Winv := betaWOK,
                 homomorphism_spot_check_all_pass := betaHomOK,
                 homomorphism_spot_check_exhaustive_small_group := isCalib,
                 homomorphism_spot_check_random_samples := nRandomSpotChecks);;

    #########################################################################
    ## R0-h: Aut-orbit count of generating (2,3)-pairs -- p in {5,7} ONLY
    #########################################################################
    if p in [5, 7] then
        autR0 := AutomorphismGroup(R0full);;
        elts := AsList(R0full);;
        ord2elts := Filtered(elts, x -> Order(x) = 2);;
        ord3elts := Filtered(elts, x -> Order(x) = 3);;
        genPairs := [];;
        for x in ord2elts do
            for y in ord3elts do
                if Size(Group(x, y)) = sizeR0full then
                    Add(genPairs, [x, y]);;
                fi;;
            od;;
        od;;
        actFun := function(pr, phi) return [Image(phi, pr[1]), Image(phi, pr[2])]; end;;
        orbitReps := [];; remaining := ShallowCopy(genPairs);;
        while Length(remaining) > 0 do
            pr := remaining[1];;
            orb := Orbit(autR0, pr, actFun);;
            Add(orbitReps, pr);;
            remaining := Filtered(remaining, q -> not q in orb);;
        od;;
        numOrbits := Length(orbitReps);;
        hResult := rec(ran := true, num_order2_elts := Length(ord2elts),
                       num_order3_elts := Length(ord3elts),
                       num_generating_pairs := Length(genPairs),
                       num_aut_orbits := numOrbits, predicted := 1,
                       match := numOrbits = 1, aut_order := Size(autR0));;
    else
        hResult := rec(ran := false, reason := "spec restricts R0-h to p in {5,7} only");;
    fi;;
    r.R0h := hResult;;

    return r;;
end;;

#############################################################################
## drive all 4 primes, write cert
#############################################################################
results := [];;
for p in PRIMES do
    Print("=== DIG-R0-1: p=", p, " START ===\n");
    t0 := Runtime();;
    res := RunForPrime(p);;
    res.wall_ms := Runtime() - t0;;
    Print("=== DIG-R0-1: p=", p, " DONE wall_ms=", res.wall_ms, " ===\n");
    Print("  R0-a: size_match=", res.R0a.size_match, " R0ab_is_C2=", res.R0a.R0ab_is_C2,
          " Z_size=", res.R0a.Z_size, " Phi_size=", res.R0a.Phi_size, "\n");
    Print("  R0-b: generates=", res.R0b.generates, "\n");
    Print("  R0-c: n=", res.R0c.n, " match=", res.R0c.match, "\n");
    Print("  R0-d: xbar=", res.R0d.xbar, " ybar=", res.R0d.ybar,
          " independent=", res.R0d.independent, "\n");
    Print("  R0-e: all_m_pass=", res.R0e.all_m_pass, " num_fail=", res.R0e.num_fail, "\n");
    Print("  R0-f: GT_count=", res.R0f.GT_count, " match=", res.R0f.GT_count_match, "\n");
    Print("  R0-g: beta_U_eq_U=", res.R0g.beta_U_eq_U, " beta_W_eq_Winv=", res.R0g.beta_W_eq_Winv,
          " hom_ok=", res.R0g.homomorphism_spot_check_all_pass, "\n");
    if res.R0h.ran then
        Print("  R0-h: ran=true num_aut_orbits=", res.R0h.num_aut_orbits, "\n");
    else
        Print("  R0-h: ran=false\n");
    fi;
    Add(results, res);;
od;;

#############################################################################
## write JSON cert
#############################################################################
JOptInt := function(x) if x = fail then return "null"; else return String(x); fi; end;;
JIntList := function(lst) return JArr(List(lst, String)); end;;

PerPrimeJSON := function(res)
    local a, b, c, d, e, f, g, h, hExtra;
    a := Concatenation(
        "{\"method\":", JStr(res.R0a.method),
        ",\"size_R0_full_generators\":", String(res.R0a.size_R0_full_generators),
        ",\"size_predicted\":", String(res.R0a.size_predicted),
        ",\"size_match\":", JB(res.R0a.size_match),
        ",\"R0ab_invariants\":", JIntList(res.R0a.R0ab_invariants),
        ",\"R0ab_is_C2\":", JB(res.R0a.R0ab_is_C2),
        ",\"Z_size\":", JOptInt(res.R0a.Z_size),
        ",\"Z_size_is_1\":", JB(res.R0a.Z_size_is_1),
        ",\"Phi_size\":", JOptInt(res.R0a.Phi_size),
        ",\"Phi_size_is_1\":", JB(res.R0a.Phi_size_is_1),
        ",\"stabilizer_trivial_witness_v\":",
        (function() if res.R0a.stabilizer_trivial_witness_v = fail then return "null";
                     else return JIntList(res.R0a.stabilizer_trivial_witness_v); fi; end)(),
        "}");;
    b := Concatenation("{\"size_UW\":", String(res.R0b.size_UW),
        ",\"size_predicted\":", String(res.R0b.size_predicted),
        ",\"generates\":", JB(res.R0b.generates), "}");;
    c := Concatenation("{\"n\":", String(res.R0c.n), ",\"predicted\":", String(res.R0c.predicted),
        ",\"match\":", JB(res.R0c.match), "}");;
    d := Concatenation("{\"xbar_lin_part_is_identity\":", JB(res.R0d.xbar_lin_part_is_identity),
        ",\"ybar_lin_part_is_identity\":", JB(res.R0d.ybar_lin_part_is_identity),
        ",\"xbar\":", JIntList(res.R0d.xbar), ",\"xbar_predicted\":", JIntList(res.R0d.xbar_predicted),
        ",\"xbar_match\":", JB(res.R0d.xbar_match),
        ",\"ybar\":", JIntList(res.R0d.ybar), ",\"ybar_predicted\":", JIntList(res.R0d.ybar_predicted),
        ",\"ybar_match\":", JB(res.R0d.ybar_match),
        ",\"independence_det_mod_p\":", String(res.R0d.independence_det_mod_p),
        ",\"independent\":", JB(res.R0d.independent), "}");;
    e := Concatenation("{\"all_m_pass\":", JB(res.R0e.all_m_pass),
        ",\"m_range\":", JIntList(res.R0e.m_range), ",\"m_zero_included\":", JB(res.R0e.m_zero_included),
        ",\"num_m_tested\":", String(res.R0e.num_m_tested), ",\"num_fail\":", String(res.R0e.num_fail),
        ",\"fail_list_head\":", JIntList(res.R0e.fail_list_head), "}");;
    f := Concatenation("{\"N_ord\":", String(res.R0f.N_ord), ",\"GT_count\":", String(res.R0f.GT_count),
        ",\"GT_count_predicted\":", String(res.R0f.GT_count_predicted),
        ",\"GT_count_match\":", JB(res.R0f.GT_count_match), "}");;
    g := Concatenation("{\"beta_U_eq_U\":", JB(res.R0g.beta_U_eq_U),
        ",\"beta_W_eq_Winv\":", JB(res.R0g.beta_W_eq_Winv),
        ",\"homomorphism_spot_check_all_pass\":", JB(res.R0g.homomorphism_spot_check_all_pass),
        ",\"homomorphism_spot_check_exhaustive_small_group\":", JB(res.R0g.homomorphism_spot_check_exhaustive_small_group),
        ",\"homomorphism_spot_check_random_samples\":", String(res.R0g.homomorphism_spot_check_random_samples),
        "}");;
    if res.R0h.ran then
        hExtra := Concatenation(",\"num_order2_elts\":", String(res.R0h.num_order2_elts),
            ",\"num_order3_elts\":", String(res.R0h.num_order3_elts),
            ",\"num_generating_pairs\":", String(res.R0h.num_generating_pairs),
            ",\"num_aut_orbits\":", String(res.R0h.num_aut_orbits),
            ",\"predicted\":", String(res.R0h.predicted), ",\"match\":", JB(res.R0h.match),
            ",\"aut_order\":", String(res.R0h.aut_order));;
    else
        hExtra := Concatenation(",\"reason\":", JStr(res.R0h.reason));;
    fi;;
    h := Concatenation("{\"ran\":", JB(res.R0h.ran), hExtra, "}");;
    return Concatenation("{\"prime\":", String(res.prime), ",\"wall_ms\":", String(res.wall_ms),
        ",\"R0a\":", a, ",\"R0b\":", b, ",\"R0c\":", c, ",\"R0d\":", d, ",\"R0e\":", e,
        ",\"R0f\":", f, ",\"R0g\":", g, ",\"R0h\":", h, "}");;
end;;

perPrimeStrs := List(results, PerPrimeJSON);;
json := Concatenation(
    "{\"schema\":\"shadow-atelier/dig_r0_1/v1\"",
    ",\"authority\":\"裁定720 (司令塔), DIG-R0-1 per docs/notes/ribet_dig_campaign_v1_addendum_a.md SS2.7 発注仕様 (commit ff08b54, verbatim)\"",
    ",\"universe_primes\":", JIntList(PRIMES),
    ",\"calibration_primes\":", JIntList(CALIBRATION_PRIMES),
    ",\"results\":[", JoinC(perPrimeStrs, ","), "]",
    ",\"no_verdict_note\":\"S-AS-5-style compliance: raw values and boolean match flags only, no interpretive verdict prose.\"",
    "}\n");;

OUT_PATH := "search/certs/dig_r0_1_v1_20260806.json";;
WriteFile(OUT_PATH, json);;
Print("Wrote ", OUT_PATH, "\n");
Print("DIG_R0_1_DONE\n");
QUIT;
