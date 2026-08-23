#############################################################################
## D972 corrected pentagon-interleave canary producer (GAP component).
##
## This source is producer-only.  It constructs the literal fourth
## Zassenhaus quotients with NQ identical relations, never the rejected
## exponent-two window gamma_4(G)G^2.
#############################################################################

if LoadPackage("nq") <> true then
  Error("PENT159N: nq package unavailable");
fi;

P159EvalExtRep := function(w, imgs)
  local e, i, z, k, n;
  e := ExtRepOfObj(w);
  z := One(imgs[1]);
  i := 1;
  while i <= Length(e) do
    k := e[i]; n := e[i+1];
    if not IsInt(k) or not IsInt(n) or k < 1 or k > Length(imgs) then
      Error("PENT159N: malformed external word representation");
    fi;
    z := z * imgs[k]^n;
    i := i + 2;
  od;
  return z;
end;

P159BuildD4pFromFp := function(G, p)
  local fg, gens, rels, ext, eg, mapped, u, v, laws, E, phi, Q, qgens;
  if not p in [2,3] then Error("PENT159N: unsupported prime"); fi;
  fg := FreeGroupOfFpGroup(G);
  gens := GeneratorsOfGroup(fg);
  rels := RelatorsOfFpGroup(G);
  ext := FreeGroup(Length(gens)+2);
  eg := GeneratorsOfGroup(ext);
  mapped := List(rels, w -> P159EvalExtRep(w,eg{[1..Length(gens)]}));
  u := eg[Length(gens)+1];
  v := eg[Length(gens)+2];
  if p=2 then laws := [u^4, Comm(u,v)^2];
  else laws := [u^9, Comm(u,v)^3];
  fi;
  E := ext / Concatenation(mapped,laws);
  phi := NqEpimorphismNilpotentQuotient(E,
    [ext.(Length(gens)+1),ext.(Length(gens)+2)],3);
  if phi=fail then Error("PENT159N: NQ epimorphism failed"); fi;
  Q := Image(phi);
  qgens := List([1..Length(gens)],i -> Image(phi,E.(i)));
  return rec(group:=Q,marked:=qgens,epi:=phi,extended:=E,
    source_generator_count:=Length(gens),source_relator_count:=Length(rels));
end;

## Calibration required by the contract: |F2/D4_2(F2)|=128.
P159F2 := FreeGroup("x","y");
P159F2fp := P159F2 / [];
P159F2q2 := P159BuildD4pFromFp(P159F2fp,2);
Print("PENT159N_F2_D4P_CALIBRATION prime=2 order=",
  Size(P159F2q2.group)," class=",NilpotencyClassOfGroup(P159F2q2.group),"\n");
if Size(P159F2q2.group) <> 128 then
  Error("PENT159N: F2/D4_2 calibration order mismatch");
fi;

Print("PENT159N_GAP_STAGE0_PASS\n");
