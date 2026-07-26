# search/k3-lambda-action.g -- GAP-18a: K^(3) の 6 点作用と検出器 Lam への F0 作用
#
# Usage: .\gap.ps1 search\k3-lambda-action.g
#
# Design source (read in full before implementation, per commander instructions):
#   docs/委嘱18_K3橋_D2D4_opus_v1.md sec 2 (D2: B1-B5 判定), sec 2.1 (D5 標的の同定 --
#     passport table with |Lam| = H conjugates count 3 or 6), sec 6 GAP-18a row
#     ("Lam(6 元)上の F0 作用が実際に非自明であることは未確認").
#   docs/notes/抽出_Kn定義_D1.md sec 1 (3.1)(3.6) marking x-bar,y-bar,z-bar; sec 3
#     K_ord = lcm(n,2); sec 4 Thm 4.3 (4.12) GT(K^(n)) explicit description,
#     (4.9) kappa(m) := m+1 (m odd), -m (m even).
#   search/week3-M5-explorer.g (MakeDn/MakeGn machinery, reused verbatim below).
#   search/gaplib_common.g (JSON helpers, cap timer, known-trap comments -- Read below).
#
# TASK 1: build the "6-point action" of G3 (index-6 quotient by a subgroup H with
#   |H|=18, H cap <x-bar> = 1, per D1 B3) and report the image order and kernel
#   order (independent recompute of the "image 36, kernel 3" claim in 委嘱18 sec 2.1
#   note). Done for ALL four G3-conjugacy classes of such H (there are 18 such H total,
#   split into classes of size 3,6,3,6 per the sec 2.1 passport table) -- not just one,
#   since 委嘱18's own note states the claim for "この6点作用" generically.
#
# TASK 2: build F0 = ker(chi-tilde) <= GT(K^(3)) explicitly as automorphisms of G3.
#   By Thm 4.3 (4.12) (4 does not divide 3, so no extra k-parity condition), a
#   GT-shadow is (m, (r^{2k}, r^{-2k}, r^{kappa(m)})) with m in X_3, k in Z (mod
#   ord(r^2) = 3 since n=3 odd). F0 = the fiber over m such that 2m+1 = 1 mod
#   2*K_ord (K_ord=6, so mod 12) intersected with X_3's range [0,6) -- i.e. m=0
#   (matching search/week4-d2d4-k3.mjs's B4 computation: fib = {(0,0),(0,1),(0,2)}).
#   For m=0: kappa(0) = -0 = 0 (0 is even). So F0 = { phi_k : k=0,1,2 } where
#   phi_k is the automorphism of G3 = F2/K_{F2}^(3) sending
#     x-bar |-> x-bar^{2*0+1} = x-bar,
#     y-bar |-> f_k^{-1} * y-bar * f_k,   f_k := (r^{2k}, r^{-2k}, r^0) in [G3,G3]
#   (the general hexagon-automorphism formula X->X^{2m+1}, Y->f^{-1}Y^{2m+1}f, with
#   the GT-shadow's second component f playing the role of the twisting element;
#   f_k in [G3,G3] = <r^2>x<r^2>x<r^2> here since 4 does not divide n=3, per D1 (3.8)).
#   phi_0 = identity; phi_1,phi_2 checked to be well-defined automorphisms of G3 via
#   GAP's GroupHomomorphismByImages + IsBijective (if this ever returns fail/false,
#   the script prints FORMULA-MISMATCH and stops rather than silently guessing).
#
#   NOTE ON AMBIGUITY (reported to commander, not resolved by guessing): the task
#   order text says "検出器 Lam(3 元集合・委嘱 18 の定義)" but 委嘱18 sec 2.1's
#   own text defines Lam as the H-conjugate set for the TARGET passport
#   (6,2^2 1^2,6), which it explicitly calls "6 元" (matching 委嘱18 sec 6's own
#   GAP-18a row: "Lam(6 元)"). The OTHER passport class (centralizer 2) has
#   |Lam|=3 but 委嘱18 explicitly says NOT to use it as detector without tangent
#   rigidification. Rather than silently pick one reading, this script computes the
#   F0-action on ALL FOUR G3-conjugacy classes of qualifying H (sizes 3,6,3,6) and
#   reports all four -- see docs/notes/検算_18a.md and the express note filed.
#
# ================================================================================

Read("search/gaplib_common.g");;
startTime := Runtime();;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ================= MakeDn / MakeGn (copied verbatim from week3-M5-explorer.g) =================
MakeDn := function(n)
  local r, s;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  if not (Order(r) = n and Order(s) = 2 and s*r*s^-1 = r^-1) then
    Error("D_n relations failed for n = ", n);
  fi;
  return [r, s];
end;;

MakeGn := function(n)
  local rs, r, s, x, y, tr;
  rs := MakeDn(n);  r := rs[1];  s := rs[2];
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  x := tr(r,1) * tr(s,2) * tr(s,3);
  y := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  return rec(x := x, y := y, G := Group(x, y), r := r, s := s, tr := tr);
end;;

# ================= build G3, marking (3.1)(3.6) =================
gn := MakeGn(3);;
G3 := gn.G;; xg := gn.x;; yg := gn.y;; r := gn.r;; s := gn.s;; tr := gn.tr;;

Print("|G3| = ", Size(G3), " (expect 108)\n");
if Size(G3) <> 108 then Error("G3 order mismatch"); fi;

# z-bar = (r^2 s, r^-1 s, r), (3.6)
zg := tr(r^2*s, 1) * tr(r^-1*s, 2) * tr(r, 3);;

Print("ord(x-bar)=", Order(xg), " ord(y-bar)=", Order(yg), " ord(z-bar)=", Order(zg),
      " (expect 6,6,6 -- passport (6,6,6))\n");
passportG3 := [Order(xg), Order(yg), Order(zg)];;

xcyc := Group(xg);;
Print("|<x-bar>| = ", Size(xcyc), " (expect 6)\n");

# ================= find all order-18 subgroups H with H cap <x-bar> = 1 =================
Print("\n-- enumerating subgroups of G3 (order 108) via LatticeSubgroups --\n");
L := LatticeSubgroups(G3);;
ccs := ConjugacyClassesSubgroups(L);;
order18Classes := Filtered(ccs, c -> Size(Representative(c)) = 18);;
Print("conjugacy classes of order-18 subgroups: ", Length(order18Classes),
      " (class sizes: ", List(order18Classes, Size), ")\n");

qualifying := Filtered(order18Classes,
  c -> Size(Intersection(Representative(c), xcyc)) = 1);;
Print("qualifying classes (H cap <x-bar> = 1): ", Length(qualifying),
      " (class sizes: ", List(qualifying, Size),
      "; total H count = ", Sum(qualifying, Size), " -- expect 18 total)\n");

if Sum(qualifying, Size) <> 18 then
  Print("*** WARNING: total qualifying H count != 18, differs from 委嘱18 sec 2.1 note\n");
fi;

# ---- per-class: passport of the 6-point quotient action, centralizer size, image/kernel of the action ----
AnalyzeClass := function(H)
  local hom, img, ker, cosetAction, xp, yp, zp, passport, cent, d;
  hom := ActionHomomorphism(G3, RightCosets(G3, H), OnRight);
  img := Image(hom);
  ker := Kernel(hom);
  d := Size(RightCosets(G3, H));
  xp := CycleStructurePerm(Image(hom, xg));
  yp := CycleStructurePerm(Image(hom, yg));
  zp := CycleStructurePerm(Image(hom, zg));
  cent := Size(Centralizer(SymmetricGroup(d), img));
  return rec(degree := d, imageOrder := Size(img), kernelOrder := Size(ker),
             genus_data_x := xp, genus_data_y := yp, genus_data_z := zp,
             centralizerOrder := cent, hom := hom);
end;;

classInfo := [];;
for i in [1..Length(qualifying)] do
  H := Representative(qualifying[i]);
  info := AnalyzeClass(H);
  Print("\nclass #", i, ": |Lam| = ", Size(qualifying[i]), ", |H| = ", Size(H), "\n");
  Print("  degree(6-pt action) = ", info.degree, "\n");
  Print("  image order = ", info.imageOrder, ", kernel order = ", info.kernelOrder, "\n");
  Print("  cycle structure of x-bar,y-bar,z-bar images: ", info.genus_data_x, " / ",
        info.genus_data_y, " / ", info.genus_data_z, "\n");
  Print("  centralizer order (Aut of the degree-6 dessin) = ", info.centralizerOrder, "\n");
  Add(classInfo, rec(H := H, lambdaSize := Size(qualifying[i]), info := info));
od;

# ================= Task 1 headline number: image/kernel of "the" 6-point action =================
# 委嘱18 sec 2.1's note ("像 36、核 3") is checked against ALL qualifying classes above;
# report which (if not all) match.
task1Matches := Filtered(classInfo, c -> c.info.imageOrder = 36 and c.info.kernelOrder = 3);;
Print("\n== TASK 1 (image 36 / kernel 3 claim) ==\n");
Print("classes matching image=36,kernel=3: ", Length(task1Matches), " / ", Length(classInfo), "\n");

# ================= Task 2: F0 = {phi_k : k=0,1,2} as automorphisms of G3 =================
Print("\n== TASK 2: building F0 as Aut(G3), m=0, k=0,1,2 ==\n");

BuildPhi := function(k)
  local fk, imgY, phi;
  fk := tr(r^(2*k), 1) * tr(r^(-2*k), 2) * tr(r^0, 3);   # (r^{2k}, r^{-2k}, r^{kappa(0)=0})
  imgY := fk^-1 * yg * fk;
  phi := GroupHomomorphismByImages(G3, G3, [xg, yg], [xg, imgY]);
  return rec(k := k, fk := fk, phi := phi);
end;;

phis := [];;
for k in [0, 1, 2] do
  pr := BuildPhi(k);
  if pr.phi = fail then
    Error("*** FORMULA-MISMATCH: k=", k, " does not extend to a homomorphism G3->G3 -- STOPPING. ",
          "This means the hexagon-automorphism formula as coded does not match Thm 4.3 for this case.");
  fi;
  if not IsBijective(pr.phi) then
    Error("*** FORMULA-MISMATCH: k=", k, " homomorphism is not bijective -- STOPPING");
  fi;
  Print("phi_", k, ": well-defined automorphism of G3 confirmed (bijective). ",
        "order = ", Order(pr.phi), "\n");
  Add(phis, pr);
od;

f0order := Size(Group(List(phis, p -> p.phi)));;
Print("|F0| generated by {phi_0,phi_1,phi_2} as subgroup of Aut(G3) = ", f0order,
      " (expect 3, cyclic)\n");

# ================= Task 2: action of F0 on each Lam (all 4 classes, exhaustive) =================
Print("\n== TASK 2: F0-action on Lam for all four qualifying classes ==\n");

BuildLambda := function(H0)
  local reps, g, K, found, i;
  reps := [];
  for g in G3 do
    K := H0^g;
    found := false;
    for i in [1..Length(reps)] do
      if reps[i] = K then found := true; break; fi;
    od;
    if not found then Add(reps, K); fi;
  od;
  return reps;
end;;

IndexOfSubgroup := function(list, K)
  local i;
  for i in [1..Length(list)] do
    if list[i] = K then return i; fi;
  od;
  return fail;
end;;

resultRows := [];;
for ci in [1..Length(classInfo)] do
  H0 := classInfo[ci].H;
  Lam := BuildLambda(H0);
  Print("\n-- class #", ci, ": |Lam| = ", Length(Lam),
        " (matches conjugacy-class size ", classInfo[ci].lambdaSize, "? ",
        PF(Length(Lam) = classInfo[ci].lambdaSize), ")\n");
  permsOfLambda := [];;
  nontrivial := false;
  for pr in phis do
    permImages := [];
    for lam in Lam do
      Add(permImages, IndexOfSubgroup(Lam, Image(pr.phi, lam)));
    od;
    if fail in permImages then
      Print("*** WARNING: phi_", pr.k, " sends some element of Lam (class #", ci,
            ") OUTSIDE Lam -- F0 does not preserve this class setwise\n");
    else
      Print("  phi_", pr.k, " acting on Lam (as index permutation of 1..", Length(Lam),
            "): ", permImages, "\n");
      if permImages <> [1 .. Length(Lam)] then nontrivial := true; fi;
    fi;
    Add(permsOfLambda, permImages);
  od;
  if nontrivial then
    Print("  ==> F0-action on this Lam is NONTRIVIAL\n");
  else
    Print("  ==> F0-action on this Lam is TRIVIAL\n");
  fi;
  Add(resultRows, rec(classIndex := ci, lambdaSize := Length(Lam),
                       imageOrder := classInfo[ci].info.imageOrder,
                       kernelOrder := classInfo[ci].info.kernelOrder,
                       centralizerOrder := classInfo[ci].info.centralizerOrder,
                       perms := permsOfLambda, nontrivial := nontrivial));
od;

Print("\n==== SUMMARY TABLE ====\n");
for row in resultRows do
  Print("class #", row.classIndex, ": |Lam|=", row.lambdaSize,
        ", image=", row.imageOrder, ", kernel=", row.kernelOrder,
        ", centralizer=", row.centralizerOrder,
        ", F0-action = ", (function() if row.nontrivial then return "NONTRIVIAL"; else return "TRIVIAL"; fi; end)(),
        "\n");
od;

# ================= write certificate JSON =================
rowsJson := [];;
for row in resultRows do
  Add(rowsJson, Concatenation(
    "{\"class_index\":", String(row.classIndex),
    ",\"lambda_size\":", String(row.lambdaSize),
    ",\"image_order\":", String(row.imageOrder),
    ",\"kernel_order\":", String(row.kernelOrder),
    ",\"centralizer_order\":", String(row.centralizerOrder),
    ",\"f0_action_nontrivial\":", JB(row.nontrivial),
    ",\"perms_by_k\":[",
    JoinC(List([1..3], j -> JArr(List(row.perms[j], v -> String(v)))), ","),
    "]}"
  ));
od;

cert := Concatenation(
  "{\"schema\":\"k3-lambda-action/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/k3-lambda-action.g\"}",
  ",\"target\":{\"n\":3,\"group\":\"G3<=D3^3\",\"order\":", String(Size(G3)), "}",
  ",\"passport_G3\":", JArr(List(passportG3, String)),
  ",\"qualifying_H_total\":", String(Sum(qualifying, Size)),
  ",\"f0_generated_order\":", String(f0order),
  ",\"task1_image36_kernel3_class_count\":", String(Length(task1Matches)),
  ",\"task1_total_classes\":", String(Length(classInfo)),
  ",\"classes\":[", JoinC(rowsJson, ","), "]",
  ",\"elapsed_cpu_ms\":", String(GAPLIB_ElapsedMs()),
  "}"
);;

WriteFile("certificates/k3/gap18a.json", cert);;
Print("\nCertificate written: certificates/k3/gap18a.json\n");
Print("Elapsed CPU ms: ", GAPLIB_ElapsedMs(), "\n");
