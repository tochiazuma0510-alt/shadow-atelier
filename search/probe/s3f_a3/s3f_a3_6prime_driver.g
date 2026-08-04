#############################################################################
## search/probe/s3f_a3/s3f_a3_6prime_driver.g
##
## Sat3F-A3 = BRIDGE-one, (6') 側の有限計算(委嘱: 2026-08-04)。
## 正本: docs/notes/s3_family_draft_v1.md sec.4.3(GAP 検査案)・sec.5.2.3(補題 R')・
##       予言 P-S3F-4(sec.8)。定義の出所:
##  - G_n, H_{j,alpha,beta}, a_i, q_j : docs/notes/oddH_full_proof_v1.md sec.2-sec.5
##    (命題 ODD-H・補題 A-I)
##  - Lambda, tau, rho_0, (R6-act)/(6'), 補題 R' : docs/week4-K3飽和_opus_v3.md
##    sec.5.2.0(型)-sec.5.2.3(縮約)
##  - Phi_{m,f} の GAP-safe な式(diag(u,u,+-u)・AbstractProd 罠の回避) :
##    docs/notes/oddH_full_proof_v1.md sec.11.1/11.4
##
## 対象: n in {3,7,9}, alpha in (Z/n)^x (全単元類)。beta=0 (H_{2,alpha,0} = H^fun 型)。
## 判定内容(1 window あたり):
##   (a) H := H_{2,alpha,0} が |H|=2n^2, N_G(H)=H (alpha<>0 で保証) を満たすか
##   (b) Lambda_alpha := H の G_n-共役類、|Lambda_alpha|=2n か
##   (c) tau(X) := Lambda 上の "共役 by X" 置換。Order(tau(X))=2n か(規約 (3))
##   (d) F_0 = { Phi_{0,f_k} : k=0..n-1 } (Thm4.3 の m=0 分岐)が Lambda を保つか
##       (Phi_{0,f_k}(H') は常に Lambda 内にあるか。fail なら安定性違反として記録)
##   (e) rho_0 : F_0 -> Sym(Lambda) が忠実か(k=0..n-1 の像置換が相異なるか)
##   (f) rho_0(F_0) = tau(mu_{2n}[n]) = <tau(X)^2> か(集合として)
## (e)+(f) = 補題 R' の下で (6') が意味する内容(sec.5.2.3 の縮約)。
##
## 予言 P-S3F-4 はコードに埋め込まない -- 生の測定値のみを cert に書き、
## 突合はレポート側(司令塔)で行う(IF-FIRST・S-7' 型)。
##
## 乗算規約: 本 driver は AbstractProd を一切使わない -- 群元は D_n^3 の
## 具体的な置換(direct product 座標)として直接構成し、Phi_{m,f}(Y) =
## F^-1 * Y^u * F は「具体元どうしの積」として一意に計算される(paper 語を
## GAP 生成子の word として評価しないので、oddH_full_proof_v1.md sec.11.4 が
## 特定した反転バグのクラスは原理的に生じない)。ただし非可換 sanity を
## 1 つ入れる(sec.0 の "convention_sanity_check" -- 順序を反転させると
## diag(u,u,+-u) の予測が崩れることを、実際に崩して見せる)。
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");

JStr := function(s) return Concatenation("\"", String(s), "\""); end;;
JB := function(b) if b then return "true"; else return "false"; fi; end;;

ModN := function(x, n)
  return ((x mod n) + n) mod n;
end;;

Sha256OfString := function(s)
  local tmp, out, f, line;
  tmp := "search/.tmp_s3fa3_sha.txt";
  out := "search/.tmp_s3fa3_sha.out";
  f := OutputTextFile(tmp, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, s);
  CloseStream(f);
  Exec(Concatenation("sha256sum \"", tmp, "\" > \"", out, "\""));
  f := InputTextFile(out);
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\" \"", out, "\""));
  if line = fail or Length(line) < 64 then
    Error("s3fa3: Sha256OfString: sha256sum did not return a hash line");
  fi;
  return line{[1 .. 64]};
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_s3fa3_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1 .. 64]};
end;;

ValidateJsonFile := function(path)
  local cmd, tmp, f, line, ok;
  tmp := Concatenation(path, ".jsoncheck.txt");
  cmd := Concatenation("python -c \"import json; json.load(open('", path,
           "', encoding='utf-8')); print('JSON_VALID')\" > \"", tmp, "\" 2>&1");
  Exec(cmd);
  f := InputTextFile(tmp);
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  ok := (line <> fail and PositionSublist(line, "JSON_VALID") <> fail);
  if not ok then
    Error("s3fa3: ValidateJsonFile: python json.load failed to parse ", path,
          " -- got: ", line);
  fi;
  return true;
end;;

#############################################################################
## ---- G_n の構成(oddH_full_proof_v1.md sec.2) ----
#############################################################################
## D_n on n points: r = (1,2,...,n) (n-cycle), s fixes point 1, s r s^-1 = r^-1.
BuildDn := function(n)
  local rList, sList, r, s;
  rList := List([1 .. n], i -> (i mod n) + 1);
  sList := List([1 .. n], i -> (ModN(n - (i - 1), n)) + 1);
  r := PermList(rList);
  s := PermList(sList);
  if r = fail or s = fail then
    Error("s3fa3: BuildDn(", n, "): PermList construction failed");
  fi;
  if Order(r) <> n then
    Error("s3fa3: BuildDn(", n, "): Order(r) <> n");
  fi;
  if s^2 <> () then
    Error("s3fa3: BuildDn(", n, "): s is not an involution");
  fi;
  if s * r * s^-1 <> r^-1 then
    Error("s3fa3: BuildDn(", n, "): s r s^-1 <> r^-1 (dihedral relation broken)");
  fi;
  return rec(r := r, s := s);
end;;

## G_n <= D_n^3 via X = (r,s,s), Y = (rs,r,rs).
## returns rec with G, X, Y, a1,a2,a3, q1,q2,q3, all as elements of the
## direct-product permutation group P.
BuildGn := function(n)
  local Dn, r, s, P, e1, e2, e3, X, Y, a1, a2, a3, q1, q2, q3, G;
  Dn := BuildDn(n);
  r := Dn.r;  s := Dn.s;
  P := DirectProduct(Group(r, s), Group(r, s), Group(r, s));
  e1 := Embedding(P, 1);  e2 := Embedding(P, 2);  e3 := Embedding(P, 3);
  X := Image(e1, r) * Image(e2, s) * Image(e3, s);
  Y := Image(e1, r*s) * Image(e2, r) * Image(e3, r*s);
  a1 := Image(e1, r);  a2 := Image(e2, r);  a3 := Image(e3, r);
  q1 := Image(e2, s) * Image(e3, s);
  q2 := Image(e1, s) * Image(e3, s);
  q3 := Image(e1, s) * Image(e2, s);
  G := Group(X, Y);
  if not (a1 in G and a2 in G and a3 in G and q1 in G and q2 in G and q3 in G) then
    Error("s3fa3: BuildGn(", n, "): a_i/q_j not in G_n = <X,Y> (lemma A broken)");
  fi;
  if Size(G) <> 4 * n^3 then
    Error("s3fa3: BuildGn(", n, "): |G_n| <> 4n^3 -- got ", Size(G));
  fi;
  if Order(X) <> 2 * n then
    Error("s3fa3: BuildGn(", n, "): Order(X) <> 2n -- got ", Order(X));
  fi;
  return rec(G := G, X := X, Y := Y,
             a1 := a1, a2 := a2, a3 := a3,
             q1 := q1, q2 := q2, q3 := q3);
end;;

## H_{2,alpha,0} = < a2, a1^alpha * a3, q2 >  (j=2, j'=3, beta=0)
BuildH2a0 := function(GnRec, alpha, n)
  local H;
  H := Subgroup(GnRec.G, [GnRec.a2, GnRec.a1^ModN(alpha, n) * GnRec.a3, GnRec.q2]);
  return H;
end;;

## Phi_{0, f_k} : X -> X, Y -> F_k^-1 * Y * F_k, F_k = a1^(2k) * a2^(-2k)  (m=0 branch)
BuildPhi0k := function(GnRec, n, k)
  local Fk, Yimg, phi;
  Fk := GnRec.a1^ModN(2*k, n) * GnRec.a2^ModN(-2*k, n);
  Yimg := Fk^-1 * GnRec.Y * Fk;
  phi := GroupHomomorphismByImages(GnRec.G, GnRec.G, [GnRec.X, GnRec.Y], [GnRec.X, Yimg]);
  return phi;
end;;

SafePos := function(lst, item, ctx)
  local p;
  p := Position(lst, item);
  if p = fail then
    Error("s3fa3: SafePos: item not found in Lambda -- ", ctx,
          " (Phi(F0)-stability of Lambda violated)");
  fi;
  return p;
end;;

#############################################################################
## ---- 一つの n について、全単元 alpha を走査 ----
#############################################################################
RunForN := function(n)
  local GnRec, units, phiList, phiBijAll, phiBijFails, k, phi,
        windows, alpha, H, Nrm, hOrderOK, normEqH, Lam, lamSizeOK,
        tauPerm, tauOrder, tauOK, tauMuN, rhoPerms, kk, imgH, pos,
        stabilityOK, stabilityFailCtx, rhoSet, faithful, dupPairs,
        i, j, imageEq, w, results, Hp;
  GnRec := BuildGn(n);
  units := Filtered([1 .. n-1], a -> Gcd(a, n) = 1);

  ## Phi_{0,f_k}, k=0..n-1 : built once per n (alpha-independent).
  phiList := [];
  phiBijAll := true;
  phiBijFails := [];
  for k in [0 .. n-1] do
    phi := BuildPhi0k(GnRec, n, k);
    if phi = fail then
      phiBijAll := false;
      Add(phiBijFails, k);
    elif not IsBijective(phi) then
      phiBijAll := false;
      Add(phiBijFails, k);
    fi;
    Add(phiList, phi);
  od;

  windows := [];
  for alpha in units do
    H := BuildH2a0(GnRec, alpha, n);
    hOrderOK := (Size(H) = 2 * n^2);
    Nrm := Normalizer(GnRec.G, H);
    normEqH := (Nrm = H);

    Lam := Orbit(GnRec.G, H, OnPoints);
    lamSizeOK := (Length(Lam) = 2 * n);

    ## tau(X) as permutation of positions 1..|Lam| in Lam.
    tauPerm := PermList(List(Lam, Hp -> SafePos(Lam, Hp^GnRec.X,
                 Concatenation("tau at n=", String(n), " alpha=", String(alpha)))));
    tauOrder := Order(tauPerm);
    tauOK := (tauOrder = 2 * n);
    tauMuN := Group([tauPerm^2]);   ## tau(mu_{2n}[n]), order n subgroup

    ## rho_0(Phi_{0,f_k}) for k=0..n-1, as permutations of Lam.
    rhoPerms := [];
    stabilityOK := true;
    stabilityFailCtx := [];
    for kk in [1 .. n] do
      w := [];
      for Hp in Lam do
        imgH := Image(phiList[kk], Hp);
        pos := Position(Lam, imgH);
        if pos = fail then
          stabilityOK := false;
          Add(stabilityFailCtx, rec(k := kk-1, n := n, alpha := alpha));
          pos := 0;  ## placeholder, whole window will be flagged bad below
        fi;
        Add(w, pos);
      od;
      if stabilityOK then
        Add(rhoPerms, PermList(w));
      else
        Add(rhoPerms, fail);
      fi;
    od;

    if stabilityOK then
      rhoSet := Set(rhoPerms);
      faithful := (Length(rhoSet) = n);
      dupPairs := [];
      if not faithful then
        for i in [1 .. n] do
          for j in [i+1 .. n] do
            if rhoPerms[i] = rhoPerms[j] then
              Add(dupPairs, [i-1, j-1]);
            fi;
          od;
        od;
      fi;
      imageEq := (rhoSet = Set(Elements(tauMuN)));
    else
      faithful := fail;
      dupPairs := fail;
      imageEq := fail;
    fi;

    Add(windows, rec(
      n := n, alpha := alpha,
      h_order := Size(H), h_order_ok := hOrderOK,
      normalizer_eq_h := normEqH,
      lambda_size := Length(Lam), lambda_size_ok := lamSizeOK,
      tau_order := tauOrder, tau_order_ok := tauOK,
      tau_mu_n_size := Size(tauMuN),
      lambda_phi_stable := stabilityOK,
      stability_fail_ks := List(stabilityFailCtx, r -> r.k),
      rho0_faithful := faithful,
      rho0_image_size := (Length(Set(Filtered(rhoPerms, x -> x <> fail)))),
      rho0_duplicate_k_pairs := dupPairs,
      rho0_image_eq_tau_mu_n := imageEq,
      six_prime_holds := (stabilityOK and faithful = true and imageEq = true)
    ));
  od;

  return rec(
    n := n,
    g_order := Size(GnRec.G),
    x_order := Order(GnRec.X),
    units := units,
    phi_bijective_all := phiBijAll,
    phi_bijective_fail_ks := phiBijFails,
    windows := windows
  );
end;;

#############################################################################
## ---- 非可換 sanity(convention_sanity_check): 順序反転で崩れることを示す ----
## n=9, m=2 (u=5, gcd(5,18)=1, m even -> kappa(m)=-m mod n=7, sign=+u).
## F = a3^kappa(m) (k=0 branch, so F only twists the 3rd coordinate --
## isolates the non-commutativity). Forward: F^-1*Y^u*F (paper order).
## Backward: F*Y^u*F^-1 (reversed -- the bug class of oddH sec.11.4 line 221).
#############################################################################
RunConventionSanity := function()
  local n, m, u, kappa, GnRec, F, YimgFwd, YimgBwd, phiFwd, phiBwd,
        expA1, expA2, expA3Fwd, fwdA1, fwdA2, fwdA3, bwdA1, bwdA2, bwdA3,
        fwdMatches, bwdMatches, fwdWellDef, bwdWellDef;
  n := 9;  m := 2;  u := 2*m + 1;  kappa := ModN(-m, n); ## m even branch
  GnRec := BuildGn(n);
  F := GnRec.a3^kappa;
  YimgFwd := F^-1 * GnRec.Y^u * F;
  YimgBwd := F * GnRec.Y^u * F^-1;
  phiFwd := GroupHomomorphismByImages(GnRec.G, GnRec.G, [GnRec.X, GnRec.Y],
              [GnRec.X^u, YimgFwd]);
  phiBwd := GroupHomomorphismByImages(GnRec.G, GnRec.G, [GnRec.X, GnRec.Y],
              [GnRec.X^u, YimgBwd]);
  fwdWellDef := (phiFwd <> fail);
  bwdWellDef := (phiBwd <> fail);

  expA1 := GnRec.a1^u;  expA2 := GnRec.a2^u;  expA3Fwd := GnRec.a3^u; ## m even: +u

  if fwdWellDef then
    fwdA1 := Image(phiFwd, GnRec.a1);
    fwdA2 := Image(phiFwd, GnRec.a2);
    fwdA3 := Image(phiFwd, GnRec.a3);
    fwdMatches := (fwdA1 = expA1 and fwdA2 = expA2 and fwdA3 = expA3Fwd);
  else
    fwdMatches := fail;
  fi;

  if bwdWellDef then
    bwdA1 := Image(phiBwd, GnRec.a1);
    bwdA2 := Image(phiBwd, GnRec.a2);
    bwdA3 := Image(phiBwd, GnRec.a3);
    bwdMatches := (bwdA1 = expA1 and bwdA2 = expA2 and bwdA3 = expA3Fwd);
  else
    bwdMatches := fail;
  fi;

  return rec(
    n := n, m := m, u := u, kappa := kappa,
    predicted_diag := Concatenation("(", String(u), ",", String(u), ",", String(u), ")"),
    forward_order := "F^-1 * Y^u * F  (paper word f^-1 y^u f, literal)",
    backward_order := "F * Y^u * F^-1  (reversed -- oddH_full_proof_v1.md sec.11.4 bug class)",
    forward_well_defined := fwdWellDef,
    forward_matches_diag_formula := fwdMatches,
    backward_well_defined := bwdWellDef,
    backward_matches_diag_formula := bwdMatches,
    discriminates := (fwdMatches = true and bwdMatches = false)
  );
end;;

#############################################################################
## ---- 実行 ----
#############################################################################
targetNs := [3, 7, 9];;
allResults := List(targetNs, RunForN);;
sanity := RunConventionSanity();;

#############################################################################
## ---- JSON 出力 ----
#############################################################################
WindowToJson := function(w)
  return Concatenation(
    "      {\n",
    "        \"n\":", String(w.n), ",\n",
    "        \"alpha\":", String(w.alpha), ",\n",
    "        \"h_order\":", String(w.h_order), ",\n",
    "        \"h_order_ok\":", JB(w.h_order_ok), ",\n",
    "        \"normalizer_eq_h\":", JB(w.normalizer_eq_h), ",\n",
    "        \"lambda_size\":", String(w.lambda_size), ",\n",
    "        \"lambda_size_ok\":", JB(w.lambda_size_ok), ",\n",
    "        \"tau_order\":", String(w.tau_order), ",\n",
    "        \"tau_order_ok\":", JB(w.tau_order_ok), ",\n",
    "        \"tau_mu_n_size\":", String(w.tau_mu_n_size), ",\n",
    "        \"lambda_phi_stable\":", JB(w.lambda_phi_stable), ",\n",
    "        \"stability_fail_ks\":", JStr(String(w.stability_fail_ks)), ",\n",
    "        \"rho0_faithful\":", (function() if w.rho0_faithful=fail then return "\"UNKNOWN_stability_violated\""; else return JB(w.rho0_faithful); fi; end)(), ",\n",
    "        \"rho0_image_size\":", String(w.rho0_image_size), ",\n",
    "        \"rho0_duplicate_k_pairs\":", JStr(String(w.rho0_duplicate_k_pairs)), ",\n",
    "        \"rho0_image_eq_tau_mu_n\":", (function() if w.rho0_image_eq_tau_mu_n=fail then return "\"UNKNOWN_stability_violated\""; else return JB(w.rho0_image_eq_tau_mu_n); fi; end)(), ",\n",
    "        \"six_prime_holds\":", JB(w.six_prime_holds), "\n",
    "      }"
  );
end;;

NResultToJson := function(res)
  local windowStrs;
  windowStrs := List(res.windows, WindowToJson);
  return Concatenation(
    "    {\n",
    "      \"n\":", String(res.n), ",\n",
    "      \"g_order\":", String(res.g_order), ",\n",
    "      \"g_order_expected\":", String(4 * res.n^3), ",\n",
    "      \"x_order\":", String(res.x_order), ",\n",
    "      \"x_order_expected\":", String(2 * res.n), ",\n",
    "      \"units\":", JStr(String(res.units)), ",\n",
    "      \"phi_bijective_all\":", JB(res.phi_bijective_all), ",\n",
    "      \"phi_bijective_fail_ks\":", JStr(String(res.phi_bijective_fail_ks)), ",\n",
    "      \"windows\":[\n",
    JoinStringsWithSeparator(windowStrs, ",\n"), "\n",
    "      ]\n",
    "    }"
  );
end;;

nResultStrs := List(allResults, NResultToJson);;

## aggregate: does every unit window at every n in {3,7,9} show six_prime_holds=true?
allSixPrimeFlags := [];;
for w in Concatenation(List(allResults, r -> r.windows)) do
  Add(allSixPrimeFlags, w.six_prime_holds);
od;;
allWindowsSixPrimeHold := ForAll(allSixPrimeFlags, x -> x = true);;
countTotal := Length(allSixPrimeFlags);;
countHold := Length(Filtered(allSixPrimeFlags, x -> x = true));;
countFail := countTotal - countHold;;
failList := [];;
for w in Concatenation(List(allResults, r -> r.windows)) do
  if w.six_prime_holds <> true then
    Add(failList, [w.n, w.alpha]);
  fi;
od;;

selfSha := ComputeSha256File("search/probe/s3f_a3/s3f_a3_6prime_driver.g");;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"s3f-a3-6prime-cert/v1\",\n",
  "  \"generated_by\":\"search/probe/s3f_a3/s3f_a3_6prime_driver.g\",\n",
  "  \"commission\":\"S3F-A3 = BRIDGE-one, (6') 側の有限計算(2026-08-04 委嘱)\",\n",
  "  \"spec_source\":\"docs/notes/s3_family_draft_v1.md sec.4.3 + sec.5.2.3 + sec.8 P-S3F-4 (candidate, Sol 未監査)\",\n",
  "  \"conventions_used\":{\n",
  "    \"dihedral\":\"r=(1..n) n-cycle, s fixes point 1, s*r*s^-1=r^-1 (asserted at runtime)\",\n",
  "    \"G_n\":\"X=(r,s,s), Y=(rs,r,rs) in D_n^3, G_n=<X,Y>, a_i/q_j per oddH_full_proof_v1.md lemma A (asserted: |G_n|=4n^3, ord(X)=2n, a_i/q_j in G_n)\",\n",
  "    \"H_2_alpha_0\":\"<a2, a1^alpha * a3, q2>  (j=2, j'=3, beta=0), per (1.2)\",\n",
  "    \"Lambda_alpha\":\"G_n-conjugacy class of H_{2,alpha,0} (week4 sec.5.2.0 def of Lambda, NOT the coset space G_n/H)\",\n",
  "    \"tau\":\"tau(X) := conjugation-by-X permutation of Lambda (H' -> H'^X); tau(mu_2n[n]) := <tau(X)^2>\",\n",
  "    \"rho_0\":\"rho_0(Phi_{0,f_k})(H') := Phi_{0,f_k}(H') (image subgroup under the automorphism), for H' in Lambda; F_0 = {Phi_{0,f_k}: k=0..n-1}, f_k=(2k,-2k,0) (Thm4.3 m=0 branch)\",\n",
  "    \"multiplication\":\"AbstractProd NOT used anywhere. All group elements are concrete permutations of the D_n^3 realization; Phi(Y)=F^-1*Y^u*F is computed as a literal product of concrete elements (no free-word evaluation), so the AbstractProd order-reversal bug class (oddH_full_proof_v1.md sec.11.4) cannot arise by construction. A non-commutative sanity fixture is included below to confirm order-sensitivity is genuinely being tested.\"\n",
  "  },\n",
  "  \"convention_sanity_check\":{\n",
  "    \"description\":\"n=9,m=2,u=5,F=a3^kappa(m) (k=0 branch): forward order F^-1*Y^u*F must match the paper's diag(u,u,+u) prediction (m even); reversed order F*Y^u*F^-1 must NOT, if this test has discriminating power.\",\n",
  "    \"n\":", String(sanity.n), ",\n",
  "    \"m\":", String(sanity.m), ",\n",
  "    \"u\":", String(sanity.u), ",\n",
  "    \"kappa_m\":", String(sanity.kappa), ",\n",
  "    \"predicted_diag\":", JStr(sanity.predicted_diag), ",\n",
  "    \"forward_order\":", JStr(sanity.forward_order), ",\n",
  "    \"backward_order\":", JStr(sanity.backward_order), ",\n",
  "    \"forward_well_defined\":", JB(sanity.forward_well_defined), ",\n",
  "    \"forward_matches_diag_formula\":", JB(sanity.forward_matches_diag_formula), ",\n",
  "    \"backward_well_defined\":", JB(sanity.backward_well_defined), ",\n",
  "    \"backward_matches_diag_formula\":", (function() if sanity.backward_matches_diag_formula = fail then return "\"N/A_not_well_defined\""; else return JB(sanity.backward_matches_diag_formula); fi; end)(), ",\n",
  "    \"discriminates\":", JB(sanity.discriminates), "\n",
  "  },\n",
  "  \"per_n_results\":[\n",
  JoinStringsWithSeparator(nResultStrs, ",\n"), "\n",
  "  ],\n",
  "  \"summary\":{\n",
  "    \"total_windows_checked\":", String(countTotal), ",\n",
  "    \"windows_with_six_prime_holds\":", String(countHold), ",\n",
  "    \"windows_failing\":", String(countFail), ",\n",
  "    \"failing_n_alpha_pairs\":", JStr(String(failList)), ",\n",
  "    \"all_unit_windows_n_in_3_7_9_six_prime_holds\":", JB(allWindowsSixPrimeHold), "\n",
  "  },\n",
  "  \"prediction_crosscheck_note\":\"P-S3F-4 (docs/notes/s3_family_draft_v1.md sec.8) was registered before this run and is NOT baked into any pass/fail branch above -- summary.all_unit_windows_n_in_3_7_9_six_prime_holds is a raw aggregate of measured six_prime_holds flags. The crosscheck against P-S3F-4 itself is reported in prose outside this cert (S-7' style), per instruction not to embed the prediction in code.\",\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), "\n",
  "  }\n",
  "}\n"
);;

outName := "search/certs/s3f_a3_6prime_20260804.json";;
outStream := OutputTextFile(outName, false);;
SetPrintFormattingStatus(outStream, false);;
PrintTo(outStream, cert);;
CloseStream(outStream);;
ValidateJsonFile(outName);;
Print("\nWrote ", outName, " (json.load OK)\n");
Print("\ns3f_a3 summary: total=", countTotal, " hold=", countHold, " fail=", countFail, "\n");
Print("failing (n,alpha) pairs: ", failList, "\n");
Print("convention sanity discriminates: ", sanity.discriminates, "\n");
Print("\nS3F_A3_6PRIME_DRIVER_DONE\n");
QUIT;
