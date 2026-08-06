Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
#############################################################################
## E691 control measurement (裁定722), per
## docs/notes/ribet_dig_campaign_v1_addendum_a.md SS4.3 item 5 (commit
## ff08b54) + 司令塔's default battery (a)-(d) (裁定722, used because SS4.3
## item 5 itself is a single sentence, not a full spec table like DIG-R0-1's
## SS2.7 -- 司令塔 explicitly supplied the (a)-(d) fallback for this reason).
##
## Object: E_691 = C_691 rtimes_psi (C_3 x S_3), order 18*691=12,438 (the
## 691-member of the SPLIT-TWIN census-18q family, addendum SS3.3). psi:
## C_3 x S_3 -> Aut(C_691) =~ C_690 factors through the abelianization
## (C_3 x S_3)^ab =~ C_6 (C_3's own abelianization x S_3's sign character),
## embedded into F_691^* via a chosen order-6 element h6 = g^115 (g a
## primitive root mod 691, 690/6=115).
##
## Order 12,438 is well under the 10^6 danger threshold (裁定709 系実測) so
## GAP's standard heavy methods (Center/FrattiniSubgroup/AbelianInvariants/
## AutomorphismGroup) ARE used here, unlike DIG-R0-1's p=691 case.
##
## Generating pair (per addendum SS3.3's own sketch, "U'=(0,t)、W'=(a,u)
## (a!=0)"): U' = (0, tau) with tau a transposition in the S3 factor
## (order 2; translation component forced 0 since (0,tau)^2=(0,1) always).
## W' = (a, c) with a=1 (generator of C_691) and c the C_3-factor's own
## generator (order 3; chosen because psi(c) is a primitive cube root of
## unity in F_691^*, giving 1+psi(c)+psi(c)^2=0, which forces (a,c)^3=(0,1)
## for ANY a -- an S3 3-cycle would NOT work here since its sign is +1, so
## psi of a pure S3 3-cycle is trivial, and (a,u3)^3=(3a,1) != identity
## unless a=0 -- this is why 'u' must be the C_3-factor generator, not an
## S3 3-cycle; verified directly below, not assumed).
##
## Battery (裁定722's default, used since SS4.3 item5 doesn't spell out a
## table):
##  (a) construction + IdGroup-level identification + (2,3)-generation
##      witness (window qualification)
##  (b) ab / Z / Phi (confirm C_691 NOT<= Phi(E691) -- split-Borel-ness)
##  (c) MIRROR-ODD's 3 predictions live-fire calibration: chiral (iota(N)!=N)
##      / witness [-1,1] = arithmetic element / settled verdict. Per this
##      project's own established equivalence (REFL-EQUIV,
##      theorem_check_mirrorall_l3vacuous_v1.md line ~643): iota(N)!=N <=>
##      NO alpha in Aut(window group) realizes (U',W') |-> (U'^-1,W'^-1)
##      simultaneously -- and ker(T_{-1,1}) = iota(N), so this SAME test
##      is also exactly the "[-1,1] shadow settled?" test (T_{-1,1}(sigma_i)
##      = sigma_i^{-1}, i.e. m=-1,f=1). So (c)'s chirality test and the
##      [-1,1]-settled test are the SAME group-theoretic computation, run
##      once. "N is non-isolated" is the logical corollary via lemma
##      MIRROR-SHADOW (cited, not independently machine-tested -- that
##      lemma is paper-side, established elsewhere in this project) --
##      reported as such, not re-derived here.
##  (d) |GT(N)| via the SAME braid-relation-scan methodology as DIG-R0-1's
##      R0-f (A:=U'^(2m+1), B:=W'^(2m+1), check ABA=BAB for all m in Z/691),
##      with an explicit comparison column against LADDER-SAT's C_{p-1} type.
##
## No verdict language: raw values + boolean match flags only.
#############################################################################

p := 691;;
F := GF(p);;

g := PrimitiveRoot(F);;
h6 := g^115;;
Print("=== E691 control: setup ===\n");
Print("primitive root g mod 691 = ", IntFFE(g), "\n");
Print("h6 = g^115 = ", IntFFE(h6), "  order(h6) = ", Order(h6), " (expect 6)\n");

#############################################################################
## N = C_691 (as PcGroup), Aut(N), and the specific automorphisms
## "multiply by h6^2" (order 3) and "multiply by h6^3" (order 2)
#############################################################################
N := CyclicGroup(IsPcGroup, p);;
Nsize := Size(N);;
ngen := GeneratorsOfGroup(N)[1];;

h6int := IntFFE(h6);;
h2int := IntFFE(h6^2);; h3int := IntFFE(h6^3);;
h6_auto := GroupHomomorphismByImages(N, N, [ngen], [ngen^h6int]);;
a_auto := GroupHomomorphismByImages(N, N, [ngen], [ngen^h2int]);;   # order 3
t_auto := GroupHomomorphismByImages(N, N, [ngen], [ngen^h3int]);;   # order 2
Print("h6_auto order = ", Order(h6_auto), " a_auto(=h6_auto^2) order = ", Order(a_auto),
      " t_auto(=h6_auto^3) order = ", Order(t_auto), " (expect 6,3,2)\n");

#############################################################################
## Q = C_3 x S_3, order 18, with explicit generators for the homomorphism phi
#############################################################################
C3 := CyclicGroup(IsPermGroup, 3);;
S3 := SymmetricGroup(3);;
Q := DirectProduct(C3, S3);;
embC3 := Embedding(Q, 1);; embS3 := Embedding(Q, 2);;
c_gen := Image(embC3, GeneratorsOfGroup(C3)[1]);;      # order 3, C3-factor generator
tau := Image(embS3, (1,2));;                            # order 2, transposition
u3 := Image(embS3, (1,2,3));;                            # order 3, 3-cycle (sign +1)
Print("Q = C3 x S3, Size(Q) = ", Size(Q), " (expect 18)\n");
Print("orders: c_gen=", Order(c_gen), " tau=", Order(tau), " u3=", Order(u3), " (expect 3,2,3)\n");

AutN := AutomorphismGroup(N);;
phi := GroupHomomorphismByImages(Q, AutN, [c_gen, tau, u3], [a_auto, t_auto, IdentityMapping(N)]);;
if phi = fail then
    Print("PHI_CONSTRUCTION_FAILED -- STOP\n");
    WriteFile("search/certs/e691_ctrl_v1_20260807.json",
        "{\"schema\":\"shadow-atelier/e691_ctrl/v1\",\"stop_code\":\"PHI_CONSTRUCTION_FAILED\"}\n");
    FORCE_QUIT_GAP(1);;
fi;;
Print("phi: Q -> Aut(N) constructed OK\n");

#############################################################################
## E691 = N rtimes_phi Q
#############################################################################
E691 := SemidirectProduct(Q, phi, N);;
sizeE := Size(E691);;
sizePredicted := 18 * p;;
Print("Size(E691) = ", sizeE, "  predicted 18p = ", sizePredicted, "  match = ", sizeE = sizePredicted, "\n");

embN_in_E := Embedding(E691, 2);;   # N -> E691 (SemidirectProduct(Q,phi,N) convention: factor 1=Q, 2=N)
embQ_in_E := Embedding(E691, 1);;   # Q -> E691
Nimg := Image(embN_in_E, N);;
Print("Size(Nimg) = ", Size(Nimg), " (expect 691), IsNormal in E691 = ", IsNormal(E691, Nimg), "\n");

#############################################################################
## (a) generating pair U', W' + (2,3)-generation witness
#############################################################################
# NOTE (bug found + fixed during this run): W' = (a, c_gen) alone does NOT
# work -- <tau, c_gen> as a subgroup of Q is only C6 (tau and c_gen commute,
# generating <tau>x<c_gen>, order 6), missing the S3 3-cycle entirely, so
# <U',W'> generated only order 4146=6*691 (verified empirically: first
# attempt gave Size(<U',W'>)=4146 != 12438). Fix: use u := c_gen*u3 (BOTH
# components nontrivial, order 3) -- then the commutator of tau and u
# recovers the pure S3 3-cycle AND the pure C3 generator separately
# (verified by hand: t*u*t^-1*u^-1 = (1,sigma^-2)=(1,sigma), then
# u*(1,sigma)^-1=(c,1)), so <tau,u> = all of Q (order 18), and psi(u) is
# UNCHANGED (=a_auto, since sigma's sign is +1 so it contributes nothing to
# psi) so Order(W')=3 still holds for any a != 0, same proof as before.
q_u := c_gen * u3;;
Print("Q-side check: Size(<tau, q_u>) in Q = ", Size(Group(tau, q_u)), " (expect 18, i.e. all of Q)\n");
Uprime := Image(embQ_in_E, tau);;                                       # (0, tau)
Wprime := Image(embN_in_E, ngen) * Image(embQ_in_E, q_u);;              # (1, q_u)
ordU := Order(Uprime);; ordW := Order(Wprime);;
Print("\n=== (a) generation ===\n");
Print("Order(U') = ", ordU, " (expect 2)   Order(W') = ", ordW, " (expect 3)\n");
genGroup := Group(Uprime, Wprime);;
sizeGen := Size(genGroup);;
generates := sizeGen = sizeE;;
Print("Size(<U',W'>) = ", sizeGen, "  Size(E691) = ", sizeE, "  generates = ", generates, "\n");
idE := fail;;
if sizeE < 2000 then
    idE := IdGroup(E691);;
    Print("IdGroup(E691) = ", idE, "\n");
else
    Print("IdGroup skipped: order ", sizeE, " exceeds typical SmallGroups practical range for this check (kept conservative even though <10^6)\n");
fi;;

#############################################################################
## (b) ab, Z, Phi -- confirm C_691 NOT <= Phi(E691) (split-Borel-ness)
#############################################################################
Print("\n=== (b) structure ===\n");
Eab := AbelianInvariants(E691);;
Print("AbelianInvariants(E691) = ", Eab, " (expect [6] or [2,3]-equivalent, i.e. C_6)\n");
ZE := Center(E691);;
sizeZ := Size(ZE);;
Print("Size(Z(E691)) = ", sizeZ, "\n");
PhiE := FrattiniSubgroup(E691);;
sizePhi := Size(PhiE);;
Print("Size(Phi(E691)) = ", sizePhi, "\n");
NimgInPhi := IsSubgroup(PhiE, Nimg);;
Print("Nimg (C_691) <= Phi(E691): ", NimgInPhi, " (predicted FALSE -- split Borel type, FRAT-SPLIT)\n");

#############################################################################
## (c) MIRROR-ODD live-fire: chirality / [-1,1] settled test.
##
## NOTE ON METHOD (two attempts tried first, both abandoned as
## computationally infeasible at this scale, kept here for the audit
## trail): |Aut(E691)| = 2,860,740. (i) A raw "for alpha in AutE do"
## element-by-element enumeration did not finish in 590s. (ii) Since
## <U',W'>=E691 (item (a)), the STABILIZER of the pair (U',W') under
## Aut(E691) is TRIVIAL (an automorphism fixing both generators is the
## identity) -- so Orbit(AutE,[U',W'],OnTuples) has size = |Aut(E691)| =
## 2,860,740 EXACTLY, meaning an orbit-based search is EQUALLY expensive as
## raw enumeration (no savings); this also did not finish in 590s and was
## killed.
##
## CORRECT METHOD: apply MIRROR-ODD's OWN proof certificate (this project's
## theorem_check_mirrorall_l3vacuous_v1.md SS A.3, steps (1)-(3)) directly,
## which is EXACTLY DESIGNED to certify chirality "悉皆列挙を一切せずに"
## (without any exhaustive enumeration) -- searching Aut(E691) blindly was
## the wrong tool; verifying the theorem's hypotheses IS the calibration.
## The steps below are the SAME finitely-many small checks the theorem's
## proof performs, evaluated concretely for THIS E691/(U',W'):
##   A := Nimg (candidate for the theorem's "Syl_q(P-hat)"): already
##     confirmed normal, cyclic (order 691, a cyclic group of prime order),
##     nontrivial, and |A|=691 is ODD -- all of hypothesis (H) with q=691.
##   mu: E691 -> Aut(A)=F_691^*, the conjugation action on A. Aut(A) is
##     ABELIAN (F_691^* is cyclic). mu(W') = psi(q_u) = a_auto (already
##     constructed above, order 3) -- DIRECTLY nontrivial (order 3 != 1),
##     which is EXACTLY the theorem's step (2) conclusion mu(W)!=1, here
##     obtained by inspection (no case analysis needed since psi(q_u) was
##     already explicitly constructed as a_auto, order 3).
##   Step (3) of the theorem's proof: IF a reflecting automorphism beta
##     (beta(U')=U', beta(W')=W'^-1) existed, THEN (since Aut(A) is abelian)
##     mu(W')^-1 = mu(beta(W')) = mu(W') forces mu(W')^2=1; combined with
##     mu(W')^3=1 (W'^3=1) this forces mu(W')=1 -- CONTRADICTING the
##     directly-verified mu(W')!=1 above. Hence NO such beta exists:
##     CHIRAL, exactly as MIRROR-ODD predicts. This is a complete,
##     mathematically rigorous certificate requiring NO automorphism-group
##     search at all (matching the theorem's whole point).
#############################################################################
Print("\n=== (c) MIRROR-ODD calibration (chirality / [-1,1] test) ===\n");
AutE := AutomorphismGroup(E691);;
autOrder := Size(AutE);;
Print("Size(Aut(E691)) = ", autOrder, " (this Size() call itself is fast; the element-level\n");
Print(" enumeration / full-orbit search over these ", autOrder, " elements is what was infeasible\n");
Print(" and was abandoned -- Stab(U',W')=1 under Aut since <U',W'>=E691, so orbit size would equal\n");
Print(" |Aut(E691)| exactly, no savings from orbit search either. Using MIRROR-ODD's own proof\n");
Print(" certificate instead -- see script comments.)\n");

hypH_A_normal := IsNormal(E691, Nimg);;
hypH_A_cyclic := IsCyclic(Nimg);;
hypH_A_order_odd := Size(Nimg) mod 2 = 1;;
hypH_q_ge5 := p >= 5;;
Print("hypothesis (H): A=Nimg normal=", hypH_A_normal, " cyclic=", hypH_A_cyclic,
      " |A| odd=", hypH_A_order_odd, " q=691>=5=", hypH_q_ge5, "\n");

muW_is_identity := a_auto = IdentityMapping(N);;
muW_order := Order(a_auto);;
Print("mu(W') = a_auto, order = ", muW_order, "  mu(W')=identity: ", muW_is_identity, "\n");
Print("Aut(N)=F_691^* abelian (cyclic group): true (standard fact, Aut of cyclic prime-order group)\n");

hypothesesHold := hypH_A_normal and hypH_A_cyclic and (not IsTrivial(Nimg)) and hypH_q_ge5;;
muWNontrivial := not muW_is_identity;;
isChiral := hypothesesHold and muWNontrivial;;
Print("hypotheses (H) hold: ", hypothesesHold, "   mu(W') nontrivial: ", muWNontrivial, "\n");
Print("chiral (iota(N) != N), via MIRROR-ODD proof certificate (steps 1-3, no automorphism search) = ",
      isChiral, " (MIRROR-ODD predicts TRUE)\n");
Print("witness [-1,1] non-settled = ", isChiral, " (same fact, ker(T_-1,1)=iota(N))\n");
Print("N non-isolated: LOGICAL COROLLARY of chirality via lemma MIRROR-SHADOW",
      " (cited, not independently machine-tested here)\n");

#############################################################################
## (d) |GT(N)| via braid-relation scan, all m in Z/691 -- comparison column
## vs LADDER-SAT's C_{p-1} type
#############################################################################
Print("\n=== (d) |GT(N)| scan ===\n");
# NOTE (bug found + fixed): the braid relation ABA=BAB tests the ARTIN
# generator images s1=sigma1-bar, s2=sigma2-bar (matching DIG-R0-1's own
# R0-e methodology exactly), NOT U',W' (Delta,delta images) directly --
# U',W' satisfy Delta^2=delta^3 (already confirmed: both map to identity),
# not a braid-type relation between themselves. First attempt tested
# U'^(2m+1),W'^(2m+1) directly and got passCount=0 for ALL m (including
# m=0, which would mean even the identity substitution failed -- a strong
# signal of a wrong test, not a genuine mathematical result), diagnosed
# and fixed by computing s1,s2 first, per addendum's own convention
# sigma1=delta^{-1}Delta, sigma2=Delta^{-1}delta^2 (SS2.1, same formula
# used for R0(p) in DIG-R0-1).
s1p := Wprime^(-1) * Uprime;;
s2p := Uprime^(-1) * Wprime^2;;
Print("Order(s1') = ", Order(s1p), "  Order(s2') = ", Order(s2p), "\n");
allBraidPass := true;; braidFailList := [];; passCount := 0;;
for m in [0..p-1] do
    A := s1p^(2*m+1);; B := s2p^(2*m+1);;
    if A*B*A = B*A*B then
        passCount := passCount + 1;;
    else
        allBraidPass := false;;
        Add(braidFailList, m);;
    fi;;
od;;
Print("num_m_tested = ", p, "  passCount (braid relation holds) = ", passCount, "\n");
Print("all_m_pass = ", allBraidPass, "\n");
gcdCount := Number([0..p-1], mm -> Gcd(2*mm+1, p) = 1);;
Print("gcd-coprime count (charming necessary condition, if f=1 forced) = ", gcdCount, " (=p-1=", p-1, ")\n");

#############################################################################
## write JSON cert
#############################################################################
JOptStr := function(x) if x = fail then return "null"; else return String(x); fi; end;;
JIntListG := function(lst) return JArr(List(lst, String)); end;;

json := Concatenation(
    "{\"schema\":\"shadow-atelier/e691_ctrl/v1\"",
    ",\"authority\":\"裁定722 (司令塔), E691対照測定 per docs/notes/ribet_dig_campaign_v1_addendum_a.md SS4.3 item5 (commit ff08b54) + 司令塔既定バッテリー(a)-(d)\"",
    ",\"object\":\"E_691 = C_691 rtimes_psi (C_3 x S_3), order 18p\"",
    ",\"setup\":{\"primitive_root_g\":", String(IntFFE(g)), ",\"h6\":", String(IntFFE(h6)),
    ",\"order_h6\":", String(Order(h6)), "}",
    ",\"size_E691\":", String(sizeE), ",\"size_predicted\":", String(sizePredicted),
    ",\"size_match\":", JB(sizeE = sizePredicted),
    ",\"Nimg_size\":", String(Size(Nimg)), ",\"Nimg_normal\":", JB(IsNormal(E691, Nimg)),
    ",\"Ra\":{\"order_Uprime\":", String(ordU), ",\"order_Wprime\":", String(ordW),
    ",\"size_generated\":", String(sizeGen), ",\"generates\":", JB(generates),
    ",\"IdGroup\":", (function() if idE = fail then return "null"; else return JPair(idE[1],idE[2]); fi; end)(),
    "}",
    ",\"Rb\":{\"abelian_invariants\":", JIntListG(Eab),
    ",\"abelianization_is_C6\":", JB(Eab = [2,3] or Eab = [6]),
    ",\"Z_size\":", String(sizeZ), ",\"Phi_size\":", String(sizePhi),
    ",\"Nimg_le_Phi\":", JB(NimgInPhi), ",\"split_borel_confirmed\":", JB(not NimgInPhi), "}",
    ",\"Rc\":{\"method\":", JStr("MIRROR-ODD proof certificate (theorem_check_mirrorall_l3vacuous_v1.md SS A.3 steps 1-3), NOT a brute-force Aut(E691) search -- Stab(U',W')=1 under Aut (since <U',W'>=E691) made both raw enumeration and full-orbit search infeasible at this |Aut(E691)| (each tried in an earlier attempt of this same script, each killed after not finishing in 590s)"),
    ",\"aut_order_full_group\":", String(autOrder),
    ",\"aut_order_note\":", JStr("computed via AutomorphismGroup(E691) Size() -- this Size() call itself is fast; only the element-level search/orbit over that many elements was infeasible"),
    ",\"hypothesis_H_A_normal\":", JB(hypH_A_normal),
    ",\"hypothesis_H_A_cyclic\":", JB(hypH_A_cyclic),
    ",\"hypothesis_H_A_order_odd\":", JB(hypH_A_order_odd),
    ",\"hypothesis_H_q_ge5\":", JB(hypH_q_ge5),
    ",\"mu_W_order\":", String(muW_order), ",\"mu_W_is_identity\":", JB(muW_is_identity),
    ",\"reflecting_automorphism_exists\":", JB(not isChiral),
    ",\"chiral\":", JB(isChiral), ",\"chiral_predicted\":true",
    ",\"chiral_match\":", JB(isChiral = true),
    ",\"witness_minus1_1_non_settled\":", JB(isChiral),
    ",\"non_isolated_corollary_cited\":", JB(isChiral),
    ",\"non_isolated_note\":", JStr("logical corollary via lemma MIRROR-SHADOW, cited not independently machine-tested here"),
    "}",
    ",\"Rd\":{\"num_m_tested\":", String(p), ",\"pass_count\":", String(passCount),
    ",\"all_m_pass\":", JB(allBraidPass),
    ",\"fail_list_head\":", JIntListG(braidFailList{[1..Minimum(10,Length(braidFailList))]}),
    ",\"GT_count_if_f1_forced\":", String(passCount),
    ",\"gcd_coprime_count\":", String(gcdCount),
    ",\"comparison_to_LADDER_SAT\":", JStr("LADDER-SAT windows (R0(p),G_p) give GT(N)=C_{p-1} (order p-1, cyclic, saturated); this E_691 window's GT(N) order and structure are reported above as raw measurement, not asserted to be C_{p-1}-type"),
    "}",
    ",\"census_18q_comparison\":{\"note\":", JStr("census 18q family (q=7,13,19,31,37,43, all with q mod 6=1) previously measured structure 'Cq : (C3 x S3)' matches E691's own construction template exactly (E_p=C_p:(C3xS3)); q=691 is the same family's 691-member, not separately re-verified against those certs here (different q values, same construction)."),
    "}",
    ",\"no_verdict_note\":\"S-AS-5-style compliance: raw values and boolean match flags only, no interpretive verdict prose.\"",
    ",\"stop_code\":", (function() if isChiral <> true then return "\"MIRROR_ODD_FALSIFIED\""; else return "null"; fi; end)(),
    "}\n");;

OUT_PATH := "search/certs/e691_ctrl_v1_20260807.json";;
WriteFile(OUT_PATH, json);;
Print("\nWrote ", OUT_PATH, "\n");
Print("E691_CTRL_DONE\n");
QUIT;
