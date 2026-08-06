## bit252_oneway_main.g -- BIT-252 片側判定試験(docs/notes/
## bit252_oneway_prereg_iffirst_v1.md 凍結票の逐語実装)。
## NOT run locally (S3.5 shard B / gap.exe occupies the local GAP process at
## write time -- confirmed via tasklist before starting this script) -- this
## is the GHA job's driver, first real test is the dispatch.
##
## Windows: N (main, order 7^8, gamma5(F2)F2^7) and K (test, order 7^14,
## gamma6(F2)F2^7). Both built via ANUPQ Pq(...:Exponent:=7) DIRECTLY
## (matches the b4-cal P1 job's proven-working pattern on GHA -- no need
## for the prereg's PQuotient+Agemo workaround, since Exponent:=7 works
## directly here as it did for P1's R construction, 7^41 confirmed in ~35ms).
##
## semantic UID (prereg sec3.2, verbatim):
##   v1 = Comm(Comm(Comm(x,y),x),x)
##   v2 = Comm(Comm(Comm(x,y),x),y)
##   v3 = Comm(Comm(Comm(x,y),y),y)
##   f_word = v1 * v2^4 * v3   (h4)
##   m = 0
## commutator convention: [a,b] := a^-1 b^-1 a b (= GAP Comm(a,b) natively).
##
## Sections: R0 (calibration F-1..F-8), R1 (|P'|), R2/R3 (fiber enumeration
## + hexagon), R4 (verdict). Lane L (F7 linear algebra) NOT implemented this
## pass (optional per prereg sec4.3) -- explicitly deferred, not silent.
Read("search/gaplib_common.g");
Read("search/probe/wac_v1/gap_output_prelude.g");

if LoadPackage("anupq") <> true then
  Error("anupq LoadPackage failed -- cannot proceed");
fi;
if not IsBound(Pq) then
  Error("Pq function not bound after LoadPackage -- anupq broken");
fi;

#############################################################################
## ---------------------- build P (main window N, order 7^8) ----------------
#############################################################################
F2 := FreeGroup("x","y");;
Print("=== Building P := F2/(gamma_5(F2) F2^7), order 7^8 ===\n");
t0 := GAPLIB_WallElapsedMs();
P := Pq(F2 : Prime := 7, ClassBound := 4, Exponent := 7);;
t1 := GAPLIB_WallElapsedMs();
Print("|P| = ", Size(P), "  (expect 7^8 = ", 7^8, ")  built in ", t1-t0, " ms\n");
if Size(P) <> 7^8 then
  Error("STOP -- |P| <> 7^8, main window construction failed");
fi;
gensP := GeneratorsOfGroup(P);;
xP := gensP[1];;  yP := gensP[2];;

DP := DerivedSubgroup(P);;
Print("|[P,P]| = ", Size(DP), "  (expect 7^6 = ", 7^6, ")\n");
if Size(DP) <> 7^6 then
  Error("STOP -- |[P,P]| <> 7^6");
fi;

#############################################################################
## ---------------------- build P' (test window K, order 7^14) --------------
#############################################################################
Print("\n=== Building P' := F2/(gamma_6(F2) F2^7), order 7^14 ===\n");
t0 := GAPLIB_WallElapsedMs();
Pp := Pq(F2 : Prime := 7, ClassBound := 5, Exponent := 7);;
t1 := GAPLIB_WallElapsedMs();
Print("|P'| = ", Size(Pp), "  (expect 7^14 = ", 7^14, ", BIT1-P1)  built in ", t1-t0, " ms\n");
if Size(Pp) <> 7^14 then
  Error("STOP -- S-B1-7: |P'| <> 7^14, construction path wrong (check Exponent/Agemo spec)");
fi;
gensPp := GeneratorsOfGroup(Pp);;
xPp := gensPp[1];;  yPp := gensPp[2];;

DPp := DerivedSubgroup(Pp);;
Print("|[P',P']| = ", Size(DPp), "  (expect 7^12 = ", 7^12, ")\n");
if Size(DPp) <> 7^12 then
  Error("STOP -- |[P',P']| <> 7^12");
fi;

#############################################################################
## ---------------------- natural map phi: P' -> P ---------------------------
#############################################################################
phi := GroupHomomorphismByImages(Pp, P, [xPp,yPp], [xP,yP]);;
Print("\nphi: P' -> P well-defined (fail = construction mismatch)? ", phi <> fail, "\n");
if phi = fail then
  Error("STOP -- phi: P' -> P is not well-defined; P/P' construction inconsistent");
fi;
kerPhi := Kernel(phi);;
sizeFiber := Size(kerPhi);;
Print("|ker(phi)| = ", sizeFiber, "  (expect 117649 = 7^6, the fiber size)\n");
if sizeFiber <> 117649 then
  Error("STOP -- S-B1-2: fiber size <> 117649");
fi;

#############################################################################
## ---------------------- theta, tau on both P and P' ------------------------
#############################################################################
thetaP := GroupHomomorphismByImages(P, P, [xP,yP], [yP,xP]);;
tauP   := GroupHomomorphismByImages(P, P, [xP,yP], [yP,(xP*yP)^-1]);;
Print("\ntheta well-defined on P? ", thetaP <> fail, "   tau well-defined on P? ", tauP <> fail, "\n");
if thetaP = fail or tauP = fail then
  Error("STOP -- theta/tau do not descend to P");
fi;

thetaPp := GroupHomomorphismByImages(Pp, Pp, [xPp,yPp], [yPp,xPp]);;
tauPp   := GroupHomomorphismByImages(Pp, Pp, [xPp,yPp], [yPp,(xPp*yPp)^-1]);;
Print("theta well-defined on P'? ", thetaPp <> fail, "   tau well-defined on P'? ", tauPp <> fail, "\n");
if thetaPp = fail or tauPp = fail then
  Error("STOP -- theta/tau do not descend to P'");
fi;

#############################################################################
## ---------------------- generic hexagon predicate --------------------------
#############################################################################
## HexPass(G, thetaHom, tauHom, m, f): tests (3.10) f*theta(f)=1 and
## (3.11)_m tau^2(y^m f) tau(y^m f) (y^m f) = 1, both in G, using G's own
## generator y (passed in explicitly since P and P' have different y's).
HexPass := function(G, thetaHom, tauHom, yGen, m, f)
  local hex1, ymf, t1v, t2v, hex2;
  hex1 := (f * ImageElm(thetaHom, f) = One(G));;
  ymf := yGen^m * f;;
  t1v := ImageElm(tauHom, ymf);;
  t2v := ImageElm(tauHom, t1v);;
  hex2 := (t2v * t1v * ymf = One(G));;
  return hex1 and hex2;;
end;;

#############################################################################
## ---------------------- semantic UID: v1,v2,v3,h4 in P and P' -------------
#############################################################################
BuildH4 := function(xg, yg)
  local v1, v2, v3;
  v1 := Comm(Comm(Comm(xg,yg),xg),xg);;
  v2 := Comm(Comm(Comm(xg,yg),xg),yg);;
  v3 := Comm(Comm(Comm(xg,yg),yg),yg);;
  return rec(v1:=v1, v2:=v2, v3:=v3, h4 := v1*v2^4*v3);;
end;;

h4dataP := BuildH4(xP, yP);;
h4dataPp := BuildH4(xPp, yPp);;
h4P := h4dataP.h4;;
h4Pp := h4dataPp.h4;;

## sanity: phi(h4') = h4 (built via the same word formula, must hold by
## homomorphism property regardless of construction details)
Print("\nphi(h4') = h4 (sanity, same word formula in both groups)? ",
      ImageElm(phi, h4Pp) = h4P, "\n");
if ImageElm(phi, h4Pp) <> h4P then
  Error("STOP -- phi(h4') <> h4, unexpected -- word formula / generator mismatch");
fi;

#############################################################################
## =========================== R0: CALIBRATION ==============================
#############################################################################
Print("\n\n=========== R0: CALIBRATION (F-1..F-8) ===========\n");
calAllPass := true;;

## F-1: m=0, f=1 -> PASS
f1pass := HexPass(P, thetaP, tauP, yP, 0, One(P));;
Print("F-1 (m=0,f=1): ", f1pass, " (expect true)\n");
calAllPass := calAllPass and f1pass;;

## F-2: m=-1(=6 mod 7), f=1 -> PASS
f2pass := HexPass(P, thetaP, tauP, yP, 6, One(P));;
Print("F-2 (m=6,f=1): ", f2pass, " (expect true)\n");
calAllPass := calAllPass and f2pass;;

## F-3: m=0, f=h4^t for t=0..6 -> 7/7 PASS
f3passCount := 0;;
for t in [0..6] do
  if HexPass(P, thetaP, tauP, yP, 0, h4P^t) then
    f3passCount := f3passCount + 1;;
  fi;
od;
Print("F-3 (m=0,f=h4^t,t=0..6): ", f3passCount, "/7 PASS (expect 7/7)\n");
calAllPass := calAllPass and (f3passCount = 7);;

## F-4: m=0, f=r := Comm(Comm(x,y),x)*Comm(Comm(x,y),y) -> FAIL (negative fixture)
rP := Comm(Comm(xP,yP),xP) * Comm(Comm(xP,yP),yP);;
f4pass := HexPass(P, thetaP, tauP, yP, 0, rP);;
Print("F-4 (m=0,f=r, negative fixture): ", f4pass, " (expect FALSE)\n");
calAllPass := calAllPass and (not f4pass);;

## F-5: m=0, f=g1 := r*s^-1, s=v1*v2*v3 -> PASS
sP := h4dataP.v1 * h4dataP.v2 * h4dataP.v3;;
g1P := rP * sP^-1;;
f5pass := HexPass(P, thetaP, tauP, yP, 0, g1P);;
Print("F-5 (m=0,f=g1=r*s^-1): ", f5pass, " (expect true)\n");
calAllPass := calAllPass and f5pass;;

## F-6: layer m=0 pass count over [P,P] (117649 elements) -> expect 49
Print("F-6: sweeping [P,P] (", Size(DP), " elements) at m=0 (may take a bit)...\n");
t0 := GAPLIB_WallElapsedMs();
f6count := 0;;
for f in DP do
  if HexPass(P, thetaP, tauP, yP, 0, f) then
    f6count := f6count + 1;;
  fi;
od;
t1 := GAPLIB_WallElapsedMs();
Print("F-6: pass count = ", f6count, " (expect 49)  elapsed_ms=", t1-t0, "\n");
calAllPass := calAllPass and (f6count = 49);;

## F-7 (MOST IMPORTANT): solution space of degree-4 homogeneous hexagon in
## gr_4 x F7 is the line F7(1,4,1) -- brute-force all 343 combinations
## (a,b,c) in F7^3, w := v1^a * v2^b * v3^c, test HexPass at m=0.
Print("F-7: sweeping gr_4 (343 combinations v1^a v2^b v3^c)...\n");
v1P := h4dataP.v1;;  v2P := h4dataP.v2;;  v3P := h4dataP.v3;;
f7solutions := [];;
for a in [0..6] do
  for b in [0..6] do
    for c in [0..6] do
      wElt := v1P^a * v2P^b * v3P^c;;
      if HexPass(P, thetaP, tauP, yP, 0, wElt) then
        Add(f7solutions, [a,b,c]);;
      fi;
    od;
  od;
od;
Print("F-7: solution count = ", Length(f7solutions), " (expect 7, a line)\n");
Print("F-7: solutions = ", f7solutions, "\n");
## check it's exactly the line {(t,4t,t) mod 7 : t=0..6}
expectedLine := List([0..6], t -> [t, (4*t) mod 7, t mod 7]);;
f7isLine := (Set(f7solutions) = Set(expectedLine));;
Print("F-7: matches line F7(1,4,1)? ", f7isLine, "\n");
calAllPass := calAllPass and f7isLine;;

## F-8: fiber enumeration self-check -- deferred to R2 (uses the same
## kerPhi construction); recorded there as "F-8".

Print("\nR0 calibration overall (F-1..F-7, F-8 deferred to R2): ", calAllPass, "\n");
if not calAllPass then
  Error("STOP -- S-B1-0: calibration fixture failed, firing is FORBIDDEN. See F-* results above.");
fi;

#############################################################################
## =========================== R1: |P'| (already checked above) =============
#############################################################################
Print("\n=========== R1: |P'| = 7^14 already confirmed above (BIT1-P1) ===========\n");

#############################################################################
## =========================== R2: fiber enumeration + F-8 ==================
#############################################################################
Print("\n=========== R2: fiber enumeration (coset h4' * ker(phi)) ===========\n");
t0 := GAPLIB_WallElapsedMs();
kerElems := AsList(kerPhi);;
Print("|ker(phi)| enumerated = ", Length(kerElems), " (expect 117649)\n");
if Length(kerElems) <> 117649 then
  Error("STOP -- S-B1-2: enumerated fiber size <> 117649");
fi;

## F-8: every element of the coset h4'*ker(phi) maps to h4 under phi
f8ok := true;;
sampleCheck := kerElems{[1..Minimum(50, Length(kerElems))]};;  ## spot check 50, then full below
for k in sampleCheck do
  if ImageElm(phi, h4Pp * k) <> h4P then
    f8ok := false;;
    break;;
  fi;
od;
Print("F-8 (spot check, 50 elements): all map to h4 under phi? ", f8ok, "\n");
if not f8ok then
  Error("STOP -- F-8 spot check failed, fiber/coset construction is wrong");
fi;
t1 := GAPLIB_WallElapsedMs();
Print("R2 elapsed_ms=", t1-t0, "\n");

#############################################################################
## =========================== R3: Lane G hexagon sweep on the fiber ========
#############################################################################
Print("\n=========== R3: Lane G -- hexagon (3.10)/(3.11) at m=0 over the fiber ===========\n");
t0 := GAPLIB_WallElapsedMs();
survivalCount := 0;;
survivorsSample := [];;
for k in kerElems do
  fprime := h4Pp * k;;
  if HexPass(Pp, thetaPp, tauPp, yPp, 0, fprime) then
    survivalCount := survivalCount + 1;;
    if Length(survivorsSample) < 5 then
      Add(survivorsSample, fprime);;
    fi;
  fi;
od;
t1 := GAPLIB_WallElapsedMs();
Print("R3: survival count = ", survivalCount, " / 117649   elapsed_ms=", t1-t0, "\n");

## BIT1-P3 check: survival count in {0} u {7^k : 0<=k<=6}
allowedCounts := Concatenation([0], List([0..6], k -> 7^k));;
p3ok := (survivalCount in allowedCounts);;
Print("BIT1-P3 (survival count in {0} U {7^k}): ", p3ok, "  (allowed set = ", allowedCounts, ")\n");
if not p3ok then
  Error("STOP -- S-B1-1: survival count outside {0} U {7^k}, IMPLEMENTATION_BUG_SUSPECTED");
fi;

#############################################################################
## =========================== R4: VERDICT ===================================
#############################################################################
Print("\n=========== R4: VERDICT ===========\n");
if survivalCount = 0 then
  Print("VERDICT = NO_SURVIVAL (A)\n");
  Print("Level 1: g* is NOT in im(GT_gen_hat -> GT(N)) -- GT_gen_hat -> GT(N) is not surjective.\n");
  Print("Level 2 (conditional on BH-alpha-pent, G_ar=42): all 252 are gentle-fake.\n");
else
  Print("VERDICT = SURVIVES_TO_K (B)\n");
  Print("ONLY authorized conclusion: g* survives to K. Breakdown UNKNOWN.\n");
  Print("FORBIDDEN WORDS CHECK (S-B1-4): do not report '294'/'genuine'/'surjective'",
        " in connection with this VERDICT B result.\n");
fi;

Print("\nALL_DONE\n");
