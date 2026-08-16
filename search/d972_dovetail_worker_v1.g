#############################################################################
## d972_dovetail_worker_v1.g
##
## Exact finite-presentation worker for the D972 relative-extension dovetail.
##
## Modes are selected with environment variable D972_WORKER_MODE:
##   selftest          - tiny complete C2-by-C2 defect enumeration
##   base-audit        - construct the marked D972 base and check exact gates
##   base-presentation - additionally compute a two-generator fp presentation
##   candidate         - consume one JSON-free GAP task file (D972_TASK_G)
##   shadow-fiber      - charming/hexagon/source-kernel/972-fiber classifier
##
## Output is written to D972_WORKER_OUTPUT (default: stdout only).  Long GAP
## calls are deliberately isolated at mode boundaries: a killed invocation has
## no authority to advance the producer cursor.
#############################################################################

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");
Read("search/week3-psl-common.g");

D972Mode := GetEnv("D972_WORKER_MODE");;
if D972Mode = fail or D972Mode = "" then D972Mode := GetEnv("D972_MODE"); fi;;
if D972Mode = fail or D972Mode = "" then D972Mode := "selftest"; fi;;
D972Output := GetEnv("D972_WORKER_OUTPUT");;
if D972Output = fail or D972Output = "" then D972Output := GetEnv("D972_OUT"); fi;;
if D972Output = fail then D972Output := ""; fi;;

D972Bool := function(x)
  if x then return "true"; else return "false"; fi;
end;;

D972JsonString := function(s)
  local t;
  t := ReplacedString(s, "\\", "\\\\");
  t := ReplacedString(t, "\"", "\\\"");
  t := ReplacedString(t, "\n", "\\n");
  t := ReplacedString(t, "\r", "\\r");
  return Concatenation("\"", t, "\"");
end;;

D972Join := function(xs, sep)
  local ans, i;
  if Length(xs) = 0 then return ""; fi;
  ans := xs[1];
  for i in [2..Length(xs)] do ans := Concatenation(ans, sep, xs[i]); od;
  return ans;
end;;

## This receipt concerns mathematical coverage of one completed finite cell.
## It deliberately does not claim watchdog-safe liveness: GAP's MTC/order
## calls and the current full shadow scan have no serializable continuation.
D972CompletenessReceiptJson := function()
  return Concatenation(
    "{\"scope\":\"fixed labelled H and fixed marked finite presentation of Qbar\"",
    ",\"b3_stable_encoding\":\"enumerate full P=B3/L over B3/M; E=ker(P to S3) is gated to order k|PB3/M|\"",
    ",\"nonabelian_h_supported\":true",
    ",\"automorphism_pairs_exhaustive\":true",
    ",\"relator_defect_tuples_exhaustive\":true",
    ",\"marked_lift_pairs_exhaustive\":true",
    ",\"outer_buckets_prune_nothing\":true",
    ",\"exactness_gate\":\"H embeds and |P|=|H||Qbar|; factor kernel has size |H|\"",
    ",\"argument\":\"chosen lifts induce two automorphisms of H and one H-valued defect for every base relator; conversely the Cayley, conjugation and defect presentation with the exactness gate is precisely an extension; every marked lift lies in one of the enumerated H-cosets\"",
    ",\"workflow_resumable\":false",
    ",\"liveness_status\":\"BLOCKED_NONCHECKPOINTABLE_EXTENSION_CELL\"",
    ",\"noncheckpointable_stages\":[",
      "\"canonical_table_relabel_enumeration\",",
      "\"automorphism_enumeration\",",
      "\"presentation_subgroup_mtc_and_fp_order\",",
      "\"shadow_derived_elements_and_full_pair_scan\"]}"
  );
end;;

D972Emit := function(json)
  if D972Output = "" then
    Print(json, "\n");
  else
    WriteFile(D972Output, Concatenation(json, "\n"));
  fi;
end;;

## Convert a zero-based Cayley table with identity 0 into its faithful regular
## permutation group.  The returned element list is indexed by the table label.
D972GroupFromTable := function(tbl)
  local n, perms, a, images, b, G;
  n := Length(tbl);
  perms := [];
  for a in [1..n] do
    images := List([1..n], b -> tbl[b][a] + 1);
    Add(perms, PermList(images));
  od;
  G := Group(perms);
  return rec(group := G, labelled_elements := perms, order := Size(G));
end;;

D972TableIsGroup := function(tbl)
  local n, seen, a, b, c;
  n := Length(tbl);
  if not ForAll(tbl, r -> IsList(r) and Length(r) = n) then return false; fi;
  if tbl[1] <> [0..n-1] then return false; fi;
  if List(tbl, r -> r[1]) <> [0..n-1] then return false; fi;
  for a in [1..n] do
    if Set(tbl[a]) <> [0..n-1] then return false; fi;
  od;
  for b in [1..n] do
    seen := Set(List([1..n], a -> tbl[a][b]));
    if seen <> [0..n-1] then return false; fi;
  od;
  for a in [1..n] do for b in [1..n] do for c in [1..n] do
    if tbl[tbl[a][b]+1][c] <> tbl[a][tbl[b][c]+1] then return false; fi;
  od; od; od;
  return true;
end;;

## Relabel a table by a zero-based permutation p with p[1]=0.
D972RelabelTable := function(tbl, p)
  local n, pinv, out, a, b;
  n := Length(tbl);
  pinv := List([0..n-1], x -> Position(p, x) - 1);
  out := List([1..n], i -> List([1..n], j -> 0));
  for a in [0..n-1] do for b in [0..n-1] do
    out[p[a+1]+1][p[b+1]+1] := p[tbl[a+1][b+1]+1];
  od; od;
  return out;
end;;

D972FlatTable := tbl -> Concatenation(tbl);;

D972CanonicalTable := function(tbl)
  local n, tail, p, best, moved;
  n := Length(tbl);
  tail := [1..n-1];
  best := fail;
  for p in PermutationsList(tail) do
    moved := D972RelabelTable(tbl, Concatenation([0], p));
    if best = fail or D972FlatTable(moved) < D972FlatTable(best) then best := moved; fi;
  od;
  return best;
end;;

D972TableAutomorphisms := function(tbl)
  local n, tail, p, relabelled, out;
  n := Length(tbl);
  tail := [1..n-1];
  out := [];
  for p in PermutationsList(tail) do
    p := Concatenation([0], p);
    relabelled := D972RelabelTable(tbl, p);
    if relabelled = tbl then Add(out, p); fi;
  od;
  return out;
end;;

## A presentation with normal H and quotient Q is finite: P/<H> = Q, hence
## |P| <= |H||Q|.  D972BuildDefectPresentation enumerates all automorphism
## images of the chosen Q generators and all relator defects.  Every extension
## occurs from the induced conjugations and relator values of a chosen lift.
D972BuildDefectPresentation := function(Hrec, qRelators, autLabels, defects)
  local Htbl, k, d, F, gens, hg, tg, rels, a, b, j, rhs, word,
        aut, hElt, qword, extrep, pos, letter, exp, P, pgens, hp, tp;
  Htbl := Hrec.table;
  k := Length(Htbl);
  d := Length(autLabels);
  F := FreeGroup(k-1+d, "d");
  gens := GeneratorsOfGroup(F);
  hg := Concatenation([One(F)], gens{[1..k-1]});
  tg := gens{[k..k+d-1]};
  rels := [];

  ## Full Cayley relations for H; redundant but exact and deterministic.
  for a in [0..k-1] do for b in [0..k-1] do
    Add(rels, hg[a+1] * hg[b+1] * hg[Htbl[a+1][b+1]+1]^-1);
  od; od;

  ## t_j h_a t_j^-1 = phi_j(h_a).
  for j in [1..d] do
    aut := autLabels[j];
    for a in [0..k-1] do
      Add(rels, tg[j] * hg[a+1] * tg[j]^-1 * hg[aut[a+1]+1]^-1);
    od;
  od;

  ## qRelators use signed generator indices.  Their lift is the enumerated H
  ## defect.  This includes nonsplit and noncentral cases without an H^3 API.
  for j in [1..Length(qRelators)] do
    word := One(F);
    for letter in qRelators[j] do
      if letter > 0 then word := word * tg[letter];
      else word := word * tg[-letter]^-1; fi;
    od;
    Add(rels, word * hg[defects[j]+1]^-1);
  od;
  P := F / rels;
  pgens := GeneratorsOfGroup(P);
  hp := Concatenation([One(P)], pgens{[1..k-1]});
  tp := pgens{[k..k+d-1]};
  return rec(fp := P, h_words := hp, t_words := tp, relators := rels,
             free_group := F, presentation_generators := pgens);
end;;

## Exact finite gate.  The image of H is normal and the quotient is Q, so P is
## finite.  We use an MTC subgroup presentation to test that no H element was
## collapsed.  Size(P)=|H||Q| is then an independent count receipt.
D972ExactEmbeddingGate := function(Pdata, expectedH, expectedQ)
  local P, Hsub, pres, Hfp, hsize, psize, normal;
  P := Pdata.fp;
  Hsub := Subgroup(P, Pdata.h_words{[2..Length(Pdata.h_words)]});
  normal := IsNormal(P, Hsub);
  pres := PresentationSubgroupMtc(P, Hsub, "h", 0);
  Hfp := FpGroupPresentation(pres);
  hsize := Size(Hfp);
  psize := Size(P);
  return rec(normal := normal, h_size := hsize, p_size := psize,
             h_embeds := hsize = expectedH,
             exact_order := psize = expectedH * expectedQ);
end;;

## Marked pair orbit gate.  Since accepted pairs generate P, a pair-preserving
## homomorphism is unique.  Both directions being well-defined and bijective is
## exactly marked-over-base isomorphism; unmarked SmallGroups IDs are unused.
D972MarkedPairIsomorphic := function(P, pairP, Q, pairQ)
  local f, g;
  f := GroupHomomorphismByImages(P, Q, pairP, pairQ);
  if f = fail or not IsBijective(f) then return false; fi;
  g := GroupHomomorphismByImages(Q, P, pairQ, pairP);
  return g <> fail and IsBijective(g);
end;;

D972ShiftPerm := function(p, offset, size)
  local images, j;
  images := [1..offset+size];
  for j in [1..size] do images[offset+j] := offset + (j^p); od;
  return PermList(images);
end;;

D972DirectSumPerm := function(p, psize, q, qsize)
  return p * D972ShiftPerm(q, psize, qsize);
end;;

D972ApplyChain := function(homs, g)
  local h, v;
  v := g;
  for h in homs do v := Image(h, v); od;
  return v;
end;;

## Forward bindings suppress GAP's unbound-global parser warnings; the full
## definitions occur below before any mode is dispatched.
D972SignedWord := fail;;
D972RebuildMarkedCell := fail;;

## Construct barQ=B3/M without a |barQ|-degree regular representation.  The
## K9 and N_S4 quotients are each built on six pure-coset blocks, then combined
## generatorwise.  The degree is 6*2916 + 6*504 = 20520 while the exact group
## order is 8,817,984.
D972BuildBase := function(withPresentation)
  local g9, G9, x9, y9, a1, a2, a1ok, a2ok, braidAut, squareAut,
        qt9, Smat, Tmat, Sperm, Tperm, w, x4, y4, P4, qt4,
        s1, s2, Q, braid, qsize, eps, epsok, kerSize, pureSize,
        iso, Qfp, rels, relLists, fpGens,compactX,compactY,compactPure;
  g9 := MakeGn(9);
  G9 := g9.G; x9 := g9.x; y9 := g9.y;
  if Size(G9) <> 2916 then Error("D972 base: |G9| drift"); fi;

  ## Canonical first-form conjugation action from k9_sigma_realization_v2.g.
  a1 := GroupHomomorphismByImages(G9, G9, [x9,y9], [x9,y9^-1*x9^-1]);
  a2 := GroupHomomorphismByImages(G9, G9, [x9,y9], [x9^-1*y9^-1,y9]);
  a1ok := a1 <> fail and IsBijective(a1);
  a2ok := a2 <> fail and IsBijective(a2);
  if not (a1ok and a2ok) then Error("D972 base: K9 sigma action failed"); fi;
  braidAut := ForAll([x9,y9], z ->
    D972ApplyChain([a1,a2,a1],z) = D972ApplyChain([a2,a1,a2],z));
  squareAut := ForAll([x9,y9], z ->
      D972ApplyChain([a1,a1],z) = x9*z*x9^-1) and
    ForAll([x9,y9], z -> D972ApplyChain([a2,a2],z) = y9*z*y9^-1);
  if not (braidAut and squareAut and Size(Group(a1,a2)) = 17496) then
    Error("D972 base: K9 full-B3 action gates failed");
  fi;
  qt9 := BuildQTGeneral(G9, x9, y9, ());
  if Size(Group(qt9.s1,qt9.s2)) <> 17496 then
    Error("D972 base: K9 transversal quotient order drift");
  fi;

  CheckGF8();
  Smat := MakeMatGF8(1,0,1,1);
  Tmat := MakeMatGF8(4,3,1,5);
  Sperm := MatToPermGF8(Smat);
  Tperm := MatToPermGF8(Tmat);
  w := Sperm*Tperm^-1;
  x4 := w^2;
  y4 := Sperm^-1*x4*Sperm;
  P4 := Group(x4,y4);
  if Size(P4) <> 504 then Error("D972 base: PSL(2,8) order drift"); fi;
  qt4 := BuildQTGeneral(P4, x4, y4, ());
  if Size(Group(qt4.s1,qt4.s2)) <> 3024 then
    Error("D972 base: N_S4 full-B3 quotient order drift");
  fi;

  s1 := D972DirectSumPerm(qt9.s1, 6*2916, qt4.s1, 6*504);
  s2 := D972DirectSumPerm(qt9.s2, 6*2916, qt4.s2, 6*504);
  Q := Group(s1,s2);
  braid := s1*s2*s1 = s2*s1*s2;
  qsize := Size(Q);
  if not braid or qsize <> 8817984 then
    Error("D972 base: marked fibre-product braid/order gate failed");
  fi;
  eps := GroupHomomorphismByImages(Q, SymmetricGroup(3), [s1,s2], [(1,2),(2,3)]);
  epsok := eps <> fail and IsSurjective(eps);
  if not epsok then Error("D972 base: epsilon map failed"); fi;
  kerSize := Size(Kernel(eps));
  pureSize := Size(Group(s1^2,s2^2));
  if kerSize <> 1469664 or pureSize <> 1469664 then
    Error("D972 base: pure-kernel order drift");
  fi;
  compactX:=D972DirectSumPerm(x9,27,x4,9);
  compactY:=D972DirectSumPerm(y9,27,y4,9);
  compactPure:=Group(compactX,compactY);
  if Size(compactPure)<>pureSize then
    Error("D972 base: compact pure model order drift");
  fi;

  relLists := [];
  Qfp := fail;
  if withPresentation then
    iso := IsomorphismFpGroupByGenerators(Q,[s1,s2],"q");
    Qfp := Image(iso);
    fpGens := GeneratorsOfGroup(Qfp);
    if Length(fpGens) <> 2 or Image(iso,s1) <> fpGens[1] or
       Image(iso,s2) <> fpGens[2] then
      Error("D972 base: fp marking was not preserved");
    fi;
    rels := RelatorsOfFpGroup(Qfp);
    relLists := List(rels, D972SignedWord);
    if Size(Qfp) <> qsize or fpGens[1]*fpGens[2]*fpGens[1] <>
       fpGens[2]*fpGens[1]*fpGens[2] then
      Error("D972 base: fp presentation order/braid gate failed");
    fi;
  fi;
  return rec(q:=Q,s1:=s1,s2:=s2,q_size:=qsize,epsilon_kernel_size:=kerSize,
    pure_size:=pureSize,braid:=braid,k9_action_braid:=braidAut,
    k9_action_squares:=squareAut,fp:=Qfp,relator_lists:=relLists,
    k9:=g9,psl4:=P4,qt9:=qt9,qt4:=qt4,
    compact_pure:=compactPure,compact_x:=compactX,compact_y:=compactY,
    component9_degree:=6*2916,component4_degree:=6*504);
end;;

## Canonical target coordinates used by the frozen NF-972 source maps.  These
## routines are deliberately local reimplementations of source-map B's q9/q4
## serializer: three D9 normal forms followed by the PSL(2,8) one-line image.
D972BlockRestrict := function(perm, offset, size)
  local images, j;
  images:=[];
  for j in [1..size] do images[j]:=(offset+j)^perm-offset; od;
  if Set(images)<>[1..size] then Error("target component does not preserve its block"); fi;
  return PermList(images);
end;;

D972D9Coordinates := function(perm)
  local rs,r,s,a,e;
  rs:=MakeDn(9); r:=rs[1]; s:=rs[2];
  for a in [0..8] do for e in [0..1] do
    if perm=r^a*s^e then return [a,e]; fi;
  od; od;
  Error("K9 component block is not in the fixed D9 normal-form table");
end;;

D972Can9 := function(perm27)
  local out,i;
  out:=[];
  for i in [0..2] do Add(out,D972D9Coordinates(D972BlockRestrict(perm27,9*i,9))); od;
  return out;
end;;

D972Can4 := function(perm9)
  return List([1..9],j->j^perm9);
end;;

D972NFTargetKey := function(m, perm27, perm9)
  local can9,can4,can9flat;
  can9:=D972Can9(perm27); can4:=D972Can4(perm9);
  can9flat:=Concatenation(can9[1],can9[2],can9[3]);
  return Concatenation("(",String(m mod 18),";",
    D972Join(List(can9flat,String),","),";",
    D972Join(List(can4,String),","),")");
end;;

D972SignedWord := function(w)
  local ext, out, i, gen, exp, j;
  ext := ExtRepOfObj(w);
  out := [];
  i := 1;
  while i <= Length(ext) do
    gen := ext[i]; exp := ext[i+1];
    if exp > 0 then for j in [1..exp] do Add(out,gen); od;
    else for j in [1..-exp] do Add(out,-gen); od; fi;
    i := i+2;
  od;
  return out;
end;;

D972PermOneLine := function(p, degree)
  return List([1..degree],i->i^p);
end;;

D972HistogramJson := function(counts)
  local sizes, rows, n;
  sizes:=Set(Filtered(counts,n->n>0));
  rows:=[];
  for n in sizes do
    Add(rows,Concatenation("{\"fiber_size\":",String(n),
      ",\"target_count\":",String(Number(counts,x->x=n)),"}"));
  od;
  return Concatenation("[",D972Join(rows,","),"]");
end;;

D972BaseShadowKey := function(B,m,f)
  local idx9,idx4,g9f,p4f;
  idx9:=B.qt9.posOf(One(B.k9.G))^f;
  idx4:=(B.component9_degree+B.qt4.posOf(One(B.psl4)))^f-
    B.component9_degree;
  if idx9<1 or idx9>Length(B.qt9.elts) or
     idx4<1 or idx4>Length(B.qt4.elts) then
    Error("calibration base shadow left the pure first transversal blocks");
  fi;
  g9f:=B.qt9.elts[idx9]; p4f:=B.qt4.elts[idx4];
  return D972NFTargetKey(m,g9f,p4f);
end;;

## Exhaust the base with the literal full-B3 equations.  This is deliberately
## separate from the theta/tau roof shortcut, and therefore calibrates the
## exact equation path subsequently used for c-not-in-L candidates as well.
D972ScanCalibrationBase := function(B)
  local P,s1,s2,x,y,c,F2bar,D,dElts,Nord,charmingMs,rows,keys,
        compact,compactX,compactY,zElt,theta,tau,thetaf,ymf,tauymf,
        tau2ymf,fullF2,toFull,fullf,m,u,f,lhs,rhs,img1,img2,hom,
        settled,settledCount,key,g9f,p4f,candidateCount,targetKeys,
        fiberCounts,targetDigest,shortcutPassCount;
  P:=B.q; s1:=B.s1; s2:=B.s2;
  x:=s1^2; y:=s2^2; c:=AbstractProd([s1,s2,s1])^2;
  if c<>One(P) then Error("base calibration shortcut requires c in M"); fi;
  compact:=B.compact_pure; compactX:=B.compact_x; compactY:=B.compact_y;
  zElt:=AbstractProd([compactX,compactY])^-1;
  theta:=GroupHomomorphismByImages(compact,compact,[compactX,compactY],
    [compactY,compactX]);
  tau:=GroupHomomorphismByImages(compact,compact,[compactX,compactY],
    [compactY,zElt]);
  if theta=fail or tau=fail then
    Error("base calibration theta/tau maps did not descend with c=1");
  fi;
  F2bar:=compact; D:=DerivedSubgroup(F2bar); dElts:=Elements(D);
  fullF2:=Group(x,y);
  toFull:=GroupHomomorphismByImages(compact,fullF2,[compactX,compactY],[x,y]);
  if toFull=fail or not IsBijective(toFull) then
    Error("base calibration compact/full marked pure models disagree");
  fi;
  Nord:=Lcm(Order(x),Order(y),Order(c));
  charmingMs:=Filtered([0..Nord-1],m->Gcd(2*m+1,Nord)=1);
  rows:=[]; keys:=[]; settledCount:=0; shortcutPassCount:=0;
  candidateCount:=Length(charmingMs)*Length(dElts);
  for m in charmingMs do
    u:=2*m+1;
    for f in dElts do
      thetaf:=Image(theta,f);
      if AbstractProd([f,thetaf])=One(compact) then
        ymf:=AbstractProd([compactY^m,f]);
        tauymf:=Image(tau,ymf); tau2ymf:=Image(tau,tauymf);
        if AbstractProd([tau2ymf,tauymf,ymf])=One(compact) and
           Size(Group(compactX^u,
             AbstractProd([f^-1,compactY^u,f])))=Size(compact) then
          shortcutPassCount:=shortcutPassCount+1;
          fullf:=Image(toFull,f);
          lhs:=AbstractProd([s1^u,fullf^-1,s2^u,fullf]);
          rhs:=AbstractProd([fullf^-1,s1,s2,x^(-m),c^m]);
          if lhs<>rhs then Error("base shortcut/full literal equation 3.3 drift"); fi;
          lhs:=AbstractProd([fullf^-1,s2^u,fullf,s1^u]);
          rhs:=AbstractProd([s2,s1,y^(-m),c^m,fullf]);
          if lhs<>rhs then Error("base shortcut/full literal equation 3.4 drift"); fi;
          img1:=s1^u;
          img2:=AbstractProd([fullf^-1,s2^u,fullf]);
          if Size(Group(img1,img2))<>Size(P) then
            Error("base shortcut/full literal surjectivity drift");
          fi;
          hom:=GroupHomomorphismByImages(P,P,[s1,s2],[img1,img2]);
          settled:=hom<>fail and IsBijective(hom);
          if settled then settledCount:=settledCount+1; fi;
          g9f:=D972BlockRestrict(f,0,27);
          p4f:=D972BlockRestrict(f,27,9);
          key:=D972NFTargetKey(m,g9f,p4f);
          Add(rows,rec(m:=m,f:=fullf,key:=key,settled:=settled));
          Add(keys,key);
        fi;
      fi;
    od;
  od;
  targetKeys:=Set(keys);
  fiberCounts:=List(targetKeys,k->Number(keys,x->x=k));
  targetDigest:=HexSHA256(Concatenation(D972Join(targetKeys,"\n"),"\n"));
  if Length(keys)<>Length(targetKeys) or Length(targetKeys)<>972 or
     targetDigest<>"9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62" then
    Error("calibration base target set/order disagrees with frozen NF-972 keys");
  fi;
  return rec(shadows:=rows,shadow_count:=Length(rows),
    settled_count:=settledCount,n_ord:=Nord,derived_order:=Length(dElts),
    charming_m:=charmingMs,candidate_count:=candidateCount,
    shortcut_pass_count:=shortcutPassCount,
    target_keys:=targetKeys,target_key_set_sorted_sha256:=targetDigest,
    fiber_counts:=fiberCounts,image_size:=Length(Filtered(fiberCounts,n->n>0)),
    zero_count:=Number(fiberCounts,n->n=0),
    histogram_json:=D972HistogramJson(fiberCounts));
end;;

## The three order-two marked orbits of sol_reply_143 section 5.4 are rebuilt as
## compact full-B3 quotients.  The split model uses the central double cover
## with pure images x=y=c=z.  The two nonsplit models use Q8 with c=1 and
## c=-1.  BuildQTGeneral supplies the exact six PB3 cosets in all three cases.
D972CalibrationSmallModels := function()
  local C2,z2,qt,S,eps,q8,z8,cval,label,bit,models,degree;
  models:=[];
  C2:=Group((1,2)); z2:=(1,2);
  qt:=BuildQTGeneral(C2,z2,z2,z2);
  S:=Group(qt.s1,qt.s2); degree:=6*Size(C2);
  eps:=GroupHomomorphismByImages(S,SymmetricGroup(3),[qt.s1,qt.s2],
    [(1,2),(2,3)]);
  if qt.s1*qt.s2*qt.s1<>qt.s2*qt.s1*qt.s2 or
     Size(S)<>degree or eps=fail or not IsSurjective(eps) or
     Size(Kernel(eps))<>Size(C2) then
    Error("split C2 calibration factor failed exact full-B3 gates");
  fi;
  Add(models,rec(orbit_id:="split_c2",extension_class:="split",
    c_bit:=1,s1:=qt.s1,s2:=qt.s2,degree:=degree,small_order:=Size(S),
    small_pure_order:=Size(Kernel(eps))));

  q8:=MakeQ8(); z8:=q8.x^2;
  if Size(q8.G)<>8 or z8=One(q8.G) or not (z8 in Centre(q8.G)) then
    Error("nonsplit Q8 calibration factor construction drift");
  fi;
  for cval in [One(q8.G),z8] do
    if cval=One(q8.G) then label:="nonsplit_q8_c0"; bit:=0;
    else label:="nonsplit_q8_c1"; bit:=1; fi;
    qt:=BuildQTGeneral(q8.G,q8.x,q8.y,cval);
    S:=Group(qt.s1,qt.s2); degree:=6*Size(q8.G);
    eps:=GroupHomomorphismByImages(S,SymmetricGroup(3),[qt.s1,qt.s2],
      [(1,2),(2,3)]);
    if qt.s1*qt.s2*qt.s1<>qt.s2*qt.s1*qt.s2 or
       Size(S)<>degree or eps=fail or not IsSurjective(eps) or
       Size(Kernel(eps))<>Size(q8.G) then
      Error("nonsplit Q8 calibration factor failed exact full-B3 gates");
    fi;
    Add(models,rec(orbit_id:=label,extension_class:="nonsplit",
      c_bit:=bit,s1:=qt.s1,s2:=qt.s2,degree:=degree,
      small_order:=Size(S),small_pure_order:=Size(Kernel(eps))));
  od;
  return models;
end;;

D972CalibrationCombinedModel := function(B,M)
  local baseDegree,s1,s2,P,rho,epsilon,pure,kernel,c,F2bar,cInF2;
  baseDegree:=B.component9_degree+B.component4_degree;
  s1:=D972DirectSumPerm(B.s1,baseDegree,M.s1,M.degree);
  s2:=D972DirectSumPerm(B.s2,baseDegree,M.s2,M.degree);
  P:=Group(s1,s2);
  rho:=GroupHomomorphismByImages(P,B.q,[s1,s2],[B.s1,B.s2]);
  epsilon:=GroupHomomorphismByImages(P,SymmetricGroup(3),[s1,s2],
    [(1,2),(2,3)]);
  if s1*s2*s1<>s2*s1*s2 or Size(Group(s1,s2))<>Size(P) or
     rho=fail or not IsSurjective(rho) or Size(Kernel(rho))<>2 or
     Size(P)<>2*B.q_size or epsilon=fail or not IsSurjective(epsilon) then
    Error("order-two calibration diagonal failed full marked factor gates");
  fi;
  pure:=Kernel(epsilon); kernel:=Kernel(rho);
  if Size(pure)<>2*B.pure_size or not IsSubgroup(pure,kernel) then
    Error("order-two calibration diagonal failed pure-extension gates");
  fi;
  c:=AbstractProd([s1,s2,s1])^2;
  F2bar:=Group(s1^2,s2^2); cInF2:=c in F2bar;
  if Size(Group(s1^2,s2^2,c))<>Size(pure) or
     not ForAll(Elements(kernel),z->z*s1^2=s1^2*z and
       z*s2^2=s2^2*z and z*c=c*z) then
    Error("order-two calibration kernel is not central in the pure group");
  fi;
  if M.extension_class="split" then
    if Size(F2bar)<>B.pure_size or cInF2 or c=One(P) or
       not (c in kernel) or Size(Group(F2bar,c))<>Size(pure) then
      Error("split C2 calibration model lacks the exact base-fixing complement");
    fi;
  else
    if Size(F2bar)<>Size(pure) then
      Error("nonsplit Q8 calibration model is not generated by the x,y lifts");
    fi;
  fi;
  return rec(group:=P,s1:=s1,s2:=s2,rho:=rho,epsilon:=epsilon,
    pure:=pure,kernel:=kernel,c:=c,F2bar:=F2bar,c_in_f2:=cInF2,
    model:=M,base_degree:=baseDegree);
end;;

## Projection to the already exhausted base makes this a complete lift scan:
## every full shadow upstairs projects to a base shadow.  For every base row we
## enumerate every charming residue above m and the entire kernel coset above
## f, retain exactly the elements in the upstairs derived subgroup, and then
## rerun both literal equations, surjectivity, and settlement upstairs.
D972ScanCalibrationOrbit := function(B,baseScan,M)
  local C,P,s1,s2,rho,x,y,c,F2bar,D,baseD,imageD,Nord,charmingMs,
        kerElts,dker,targetKeys,fiberCounts,shadowCount,settledCount,
        candidateLiftCount,brow,m,u,fRep,fLifts,h,f,lhs,rhs,img1,img2,
        hom,settled,keyPos,witnessJson,smallS1,smallS2,smallX,smallY,smallC;
  C:=D972CalibrationCombinedModel(B,M);
  P:=C.group; s1:=C.s1; s2:=C.s2; rho:=C.rho;
  x:=s1^2; y:=s2^2; c:=C.c;
  F2bar:=Group(x,y); D:=DerivedSubgroup(F2bar);
  baseD:=DerivedSubgroup(Group(B.s1^2,B.s2^2));
  imageD:=Image(rho,D);
  if Size(imageD)<>Size(baseD) or not IsSubgroup(baseD,imageD) then
    Error("calibration derived projection is not onto the base derived group");
  fi;
  Nord:=Lcm(Order(x),Order(y),Order(c));
  charmingMs:=Filtered([0..Nord-1],m->Gcd(2*m+1,Nord)=1);
  kerElts:=Elements(C.kernel); dker:=Intersection(D,C.kernel);
  targetKeys:=baseScan.target_keys;
  fiberCounts:=List(targetKeys,k->0);
  shadowCount:=0; settledCount:=0; candidateLiftCount:=0;
  for brow in baseScan.shadows do
    fRep:=PreImagesRepresentative(rho,brow.f);
    if fRep=fail then Error("calibration factor map lost a base shadow f"); fi;
    fLifts:=Set(Filtered(List(kerElts,h->fRep*h),f->f in D));
    if Length(fLifts)<>Size(dker) then
      Error("calibration did not enumerate the full derived f-fiber");
    fi;
    for m in Filtered(charmingMs,m->m mod baseScan.n_ord=brow.m) do
      u:=2*m+1;
      for f in fLifts do
        candidateLiftCount:=candidateLiftCount+1;
        lhs:=AbstractProd([s1^u,f^-1,s2^u,f]);
        rhs:=AbstractProd([f^-1,s1,s2,x^(-m),c^m]);
        if lhs=rhs then
          lhs:=AbstractProd([f^-1,s2^u,f,s1^u]);
          rhs:=AbstractProd([s2,s1,y^(-m),c^m,f]);
          if lhs=rhs then
            img1:=s1^u;
            img2:=AbstractProd([f^-1,s2^u,f]);
            if Size(Group(img1,img2))=Size(P) then
              shadowCount:=shadowCount+1;
              hom:=GroupHomomorphismByImages(P,P,[s1,s2],[img1,img2]);
              settled:=hom<>fail and IsBijective(hom);
              if settled then settledCount:=settledCount+1; fi;
              keyPos:=Position(targetKeys,brow.key);
              if keyPos=fail then Error("calibration reduction left target set"); fi;
              fiberCounts[keyPos]:=fiberCounts[keyPos]+1;
            fi;
          fi;
        fi;
      od;
    od;
  od;
  smallS1:=D972PermOneLine(M.s1,M.degree);
  smallS2:=D972PermOneLine(M.s2,M.degree);
  smallX:=D972PermOneLine(M.s1^2,M.degree);
  smallY:=D972PermOneLine(M.s2^2,M.degree);
  smallC:=D972PermOneLine(AbstractProd([M.s1,M.s2,M.s1])^2,M.degree);
  witnessJson:=Concatenation(
    "{\"orbit_id\":",D972JsonString(M.orbit_id),
    ",\"extension_class\":",D972JsonString(M.extension_class),
    ",\"c_bit\":",String(M.c_bit),
    ",\"combined_group_definition\":\"<(base_s1,small_s1),(base_s2,small_s2)> on disjoint supports\"",
    ",\"small_factor\":{\"degree\":",String(M.degree),
      ",\"s1_images\":",String(smallS1),
      ",\"s2_images\":",String(smallS2),
      ",\"x_images\":",String(smallX),
      ",\"y_images\":",String(smallY),
      ",\"c_images\":",String(smallC),
      ",\"full_order\":",String(M.small_order),
      ",\"pure_order\":",String(M.small_pure_order),"}",
    ",\"full_order\":",String(Size(P)),
    ",\"pure_order\":",String(Size(C.pure)),
    ",\"factor_kernel_order\":",String(Size(C.kernel)),
    ",\"braid\":true,\"marked_generation\":true",
    ",\"pure_generated_by_xy\":",D972Bool(Size(C.F2bar)=Size(C.pure)),
    ",\"c_in_xy_subgroup\":",D972Bool(C.c_in_f2),
    ",\"n_ord\":",String(Nord),
    ",\"derived_order\":",String(Size(D)),
    ",\"derived_factor_kernel_order\":",String(Size(dker)),
    ",\"projected_base_shadow_count\":",String(baseScan.shadow_count),
    ",\"candidate_lift_count\":",String(candidateLiftCount),
    ",\"shadow_count\":",String(shadowCount),
    ",\"settled_count\":",String(settledCount),
    ",\"fiber_counts\":",String(fiberCounts),
    ",\"projection_exhaustiveness\":\"every upstairs charming literal shadow projects to a base charming literal shadow; all m-residues and the complete factor-kernel coset in the derived subgroup are enumerated\"}"
  );
  return rec(orbit_id:=M.orbit_id,extension_class:=M.extension_class,
    shadow_count:=shadowCount,settled_count:=settledCount,n_ord:=Nord,
    fiber_counts:=fiberCounts,
    image_size:=Length(Filtered(fiberCounts,n->n>0)),
    zero_count:=Number(fiberCounts,n->n=0),
    histogram_json:=D972HistogramJson(fiberCounts),witness_json:=witnessJson);
end;;

## Machine part of the section 5.4 orbit classification.  A class in
## H^2(V4,F2) is encoded by coefficients of A*a^2+B*a*b+C*b^2.  The two
## transvections induced by the braid generators act by the substitutions
## (a,b)->(a+b,b) and (a,b)->(a,a+b).  We enumerate all eight coefficient
## triples and both c-bits.  The reduction H^2(Q0,C2)=H^2(V4,F2), and the
## rules distinguishing the split/non-split marked c-bits, remain an explicit
## pinned paper premise rather than being misreported as a second machine proof.
D972C2MarkedClassification := function()
  local classes,A,B,C,t1,t2,invariant,specs,cls,bit,ids,json;
  classes:=[];
  for A in [0,1] do for B in [0,1] do for C in [0,1] do
    Add(classes,[A,B,C]);
  od; od; od;
  t1:=v->[v[1],v[2],(v[1]+v[2]+v[3]) mod 2];
  t2:=v->[(v[1]+v[2]+v[3]) mod 2,v[2],v[3]];
  invariant:=Filtered(classes,v->t1(v)=v and t2(v)=v);
  specs:=[];
  for cls in invariant do
    if cls=[0,0,0] then
      ## In the split pure extension x,y alone miss the central kernel, so the
      ## c-bit must be nonzero for the marked PB3 quotient to be onto.
      for bit in [0,1] do
        if bit<>0 then Add(specs,rec(orbit_id:="split_c2",
          extension_class:="split",class_coefficients:=cls,c_bit:=bit)); fi;
      od;
    else
      ## In the nonzero class the x,y lifts generate the Q8 fibre product, so
      ## both central c-images give distinct marked orbits.
      for bit in [0,1] do
        Add(specs,rec(orbit_id:=Concatenation("nonsplit_q8_c",String(bit)),
          extension_class:="nonsplit",class_coefficients:=cls,c_bit:=bit));
      od;
    fi;
  od;
  ids:=List(specs,s->s.orbit_id);
  json:=Concatenation(
    "{\"coefficient_universe_size\":",String(Length(classes)),
    ",\"invariant_classes\":",String(invariant),
    ",\"transvection_1_images\":",String(List(classes,t1)),
    ",\"transvection_2_images\":",String(List(classes,t2)),
    ",\"marked_specs\":[",
      D972Join(List(specs,s->Concatenation("{\"orbit_id\":",
        D972JsonString(s.orbit_id),",\"extension_class\":",
        D972JsonString(s.extension_class),",\"class_coefficients\":",
        String(s.class_coefficients),",\"c_bit\":",String(s.c_bit),"}")),","),"]",
    ",\"paper_premise\":\"sol/sol_reply_143_typedfiber.md section 5.4: H2(Q0,C2)=H2(V4,F2), invariant extension classes classify the central C2 event, and the stated base-fixing marked-bit rules are complete\"",
    ",\"paper_source_sha256\":\"ef6490f286b82ade2ee5995a00a857dd92fbca6f5e136c79f855d81adab7da3a\"",
    ",\"machine_scope\":\"all eight F2 coefficient triples, both transvection fixed-point equations, and every allowed c-bit\"",
    ",\"independent_model_universe_proof\":false",
    ",\"calibration_unlock_authority\":false}"
  );
  return rec(invariant_classes:=invariant,specs:=specs,ids:=ids,json:=json,
    marked_orbit_count:=Length(specs));
end;;

D972CalibrationJson := function(B)
  local baseScan,models,orbits,M,baseCounts,baseCase,k2Case,
        gtOrders,imageSizes,zeroCounts,hists,witnesses,baseWitness,classification;
  if B.fp=fail or Length(B.relator_lists)=0 then
    Error("calibration requires the exact marked base presentation");
  fi;
  baseScan:=D972ScanCalibrationBase(B);
  baseCounts:=baseScan.fiber_counts;
  classification:=D972C2MarkedClassification();
  models:=D972CalibrationSmallModels(); orbits:=[];
  if List(models,m->m.orbit_id)<>classification.ids then
    Error("explicit order-two marked models disagree with F2 classification");
  fi;
  for M in models do Add(orbits,D972ScanCalibrationOrbit(B,baseScan,M)); od;
  gtOrders:=List(orbits,o->o.shadow_count);
  imageSizes:=List(orbits,o->o.image_size);
  zeroCounts:=List(orbits,o->o.zero_count);
  hists:=Concatenation("[",D972Join(List(orbits,o->o.histogram_json),","),"]");
  baseCase:=Concatenation(
    "{\"marked_orbit_count\":",String(Length([baseScan])),
    ",\"gt_orders\":[",String(baseScan.shadow_count),"]",
    ",\"image_sizes\":[",String(baseScan.image_size),"]",
    ",\"zero_fiber_counts\":[",String(baseScan.zero_count),"]",
    ",\"fiber_histograms\":[",baseScan.histogram_json,"]",
    ",\"isolated\":",D972Bool(baseScan.settled_count=baseScan.shadow_count),
    ",\"fiber_counts\":",String(baseCounts),"}"
  );
  k2Case:=Concatenation(
    "{\"marked_orbit_count\":",String(classification.marked_orbit_count),
    ",\"gt_orders\":",String(gtOrders),
    ",\"image_sizes\":",String(imageSizes),
    ",\"zero_fiber_counts\":",String(zeroCounts),
    ",\"fiber_histograms\":",hists,
    ",\"isolated\":",String(List(orbits,o->o.settled_count=o.shadow_count)),
    ",\"marked_orbit_completeness_basis\":\"PINNED_PAPER_PREMISE_PLUS_MACHINE_F2_ENUM\"",
    ",\"three_registered_models_scanned\":true",
    ",\"independent_model_universe_proof\":false",
    ",\"calibration_unlock_authority\":false",
    ",\"orbits\":[",D972Join(List(orbits,o->o.witness_json),","),"]}"
  );
  baseWitness:=Concatenation(
    "{\"construction\":\"marked_diagonal_fiber_product/v1\"",
    ",\"base_marked_fp\":{\"generator_count\":2,\"signed_relators\":",
      String(B.relator_lists),",\"full_order\":",String(B.q_size),
      ",\"pure_order\":",String(B.pure_size),"}",
    ",\"base_scan\":{\"evaluation_mode\":\"compact_theta_tau_exhaustive_c_equals_1_plus_full_b3_literal_recheck_of_every_pass\"",
      ",\"shortcut_precondition_c_identity\":true",
      ",\"n_ord\":",String(baseScan.n_ord),
      ",\"derived_order\":",String(baseScan.derived_order),
      ",\"charming_m\":",String(baseScan.charming_m),
      ",\"candidate_count\":",String(baseScan.candidate_count),
      ",\"shortcut_pass_count\":",String(baseScan.shortcut_pass_count),
      ",\"shadow_count\":",String(baseScan.shadow_count),
      ",\"settled_count\":",String(baseScan.settled_count),
      ",\"target_keys\":[",D972Join(List(baseScan.target_keys,D972JsonString),","),"]",
      ",\"target_key_count\":",String(Length(baseScan.target_keys)),
      ",\"target_key_order_recipe\":\"GAP Set/sort of canonical serialized keys, joined by LF with terminal LF\"",
      ",\"target_key_order_sha256\":",
        D972JsonString(baseScan.target_key_set_sorted_sha256),
      ",\"target_key_set_sorted_sha256\":",
        D972JsonString(baseScan.target_key_set_sorted_sha256),
      ",\"frozen_target_digest_gate\":true",
      ",\"fiber_counts\":",String(baseCounts),"}",
    ",\"c2_marked_classification\":",classification.json,
    ",\"orbits\":[",D972Join(List(orbits,o->o.witness_json),","),"]}"
  );
  return Concatenation("{\"k1_base\":",baseCase,
    ",\"k2_three_marked_orbits\":",k2Case,
    ",\"witness\":",baseWitness,"}");
end;;

D972BaseMode := function(withPresentation)
  local B, result, calibration;
  B := D972BuildBase(withPresentation);
  if D972Mode="base-audit" then calibration:=D972CalibrationJson(B);
  else calibration:="null"; fi;
  result := Concatenation(
    "{\"schema\":\"d972_dovetail_worker/v1\",\"mode\":",
    D972JsonString(D972Mode),
    ",\"status\":\"PASS\",\"braid\":",D972Bool(B.braid),
    ",\"q_order\":",String(B.q_size),
    ",\"qbar_size\":",String(B.q_size),
    ",\"epsilon_kernel_size\":",String(B.epsilon_kernel_size),
    ",\"pure_generator_subgroup_size\":",String(B.pure_size),
    ",\"k9_action_braid\":",D972Bool(B.k9_action_braid),
    ",\"k9_action_squares\":",D972Bool(B.k9_action_squares),
    ",\"fp_generator_count\":",String(2),
    ",\"fp_relator_count\":",String(Length(B.relator_lists)),
    ",\"q_relators\":",String(B.relator_lists),
    ",\"fp_relators\":",String(B.relator_lists),
    ",\"calibration\":",calibration,
    ",\"relative_extension_completeness_receipt\":",D972CompletenessReceiptJson(),
    ",\"monolithic_boundary\":\"BLOCKED_NONCHECKPOINTABLE_EXTENSION_CELL: IsomorphismFpGroupByGenerators/MTC and the full shadow scan have no serializable continuation\"}"
  );
  D972Emit(result);
end;;

D972TableOfGroup := function(G)
  local elts,e,rest,labels,pos,tbl,a,b;
  elts:=Elements(G); e:=Identity(G);
  rest:=Filtered(elts,x->x<>e);
  SortBy(rest,String);
  labels:=Concatenation([e],rest);
  pos:=NewDictionary(labels[1],true);
  for a in [1..Length(labels)] do AddDictionary(pos,labels[a],a); od;
  tbl:=[];
  for a in [1..Length(labels)] do
    Add(tbl,List([1..Length(labels)],b->LookupDictionary(pos,labels[a]*labels[b])-1));
  od;
  return D972CanonicalTable(tbl);
end;;

D972KernelCatalogMode := function()
  local ks,k,available,groups,tables,result;
  ks:=GetEnv("D972_K");
  if ks=fail or ks="" then Error("kernel-catalog needs D972_K"); fi;
  k:=Int(ks);
  available:=SmallGroupsAvailable(k);
  groups:=[]; tables:=[];
  if available then
    groups:=AllSmallGroups(k);
    tables:=Set(List(groups,D972TableOfGroup));
    if Length(tables)<>Length(groups) then
      Error("SmallGroups catalog canonical-table collision/count drift");
    fi;
  fi;
  result:=Concatenation(
    "{\"schema\":\"d972_dovetail_worker/v1\",\"mode\":\"kernel-catalog\"",
    ",\"status\":\"PASS\",\"k\":",String(k),
    ",\"smallgroups_complete\":",D972Bool(available),
    ",\"h_count\":",String(Length(tables)),",\"tables\":",String(tables),
    ",\"fallback_required\":",D972Bool(not available),"}"
  );
  D972Emit(result);
end;;

D972Digits := function(index, base, width)
  local out, i;
  if index < 0 then Error("negative mixed-radix index"); fi;
  out := List([1..width], i -> 0);
  for i in Reversed([1..width]) do
    out[i] := index mod base;
    index := QuoInt(index,base);
  od;
  if index <> 0 then Error("mixed-radix index out of range"); fi;
  return out;
end;;

D972FpGroupFromSignedRelators := function(rank, signedRelators, prefix)
  local F, gens, rels, row, word, letter;
  F := FreeGroup(rank,prefix);
  gens := GeneratorsOfGroup(F);
  rels := [];
  for row in signedRelators do
    word := One(F);
    for letter in row do
      if letter > 0 then word := word*gens[letter];
      else word := word*gens[-letter]^-1; fi;
    od;
    Add(rels,word);
  od;
  return rec(fp:=F/rels,free:=F,relators:=rels);
end;;

D972InverseLabels := function(tbl)
  local k, inv, a, b;
  k := Length(tbl);
  inv := List([1..k],i->-1);
  for a in [0..k-1] do for b in [0..k-1] do
    if tbl[a+1][b+1]=0 and tbl[b+1][a+1]=0 then inv[a+1]:=b; fi;
  od; od;
  if ForAny(inv,x->x<0) then Error("group table has missing inverse"); fi;
  return inv;
end;;

D972OuterBucketPair := function(tbl, auts, p1, p2)
  local k, inv, innerMaps, h, a, v, innerPerms, I, autPerms, canon;
  k := Length(tbl);
  inv := D972InverseLabels(tbl);
  innerMaps := [];
  for h in [0..k-1] do
    v := [];
    for a in [0..k-1] do
      Add(v,tbl[tbl[h+1][a+1]+1][inv[h+1]+1]);
    od;
    Add(innerMaps,v);
  od;
  innerPerms := Set(List(innerMaps,p->PermList(List(p,x->x+1))));
  I := Group(innerPerms);
  autPerms := List(auts,p->PermList(List(p,x->x+1)));
  canon := function(pos)
    local q, best;
    best := fail;
    for q in [1..Length(autPerms)] do
      if autPerms[pos]*autPerms[q]^-1 in I then
        if best=fail or q<best then best:=q; fi;
      fi;
    od;
    return best-1;
  end;
  return [canon(p1),canon(p2)];
end;;

D972CandidateMode := function()
  local taskPath, T, tbl, k, auts, acount, autIndex, a1pos, a2pos,
        defects, liftDigits, Pdata, gate, qdata, Q, qgens, P, pgens,
        rhoImages, rho, rhoOK, rhoKernel, lift1, lift2, braid, generates,
        outerBucket, accepted, relStrings, result, candidateJson,
        candidateArray, smallGroupsComplete, semantic, nextAut, nextDef,
        nextLift, universeExhausted, nextJson,epsilon,epsOK,pureExtensionOrder;
  taskPath := GetEnv("D972_TASK_G");
  if taskPath=fail or taskPath="" then taskPath:=GetEnv("D972_TASK"); fi;
  if taskPath=fail or taskPath="" then Error("candidate mode needs D972_TASK_G"); fi;
  Read(taskPath);
  if not IsBound(D972_TASK) then Error("task file did not bind D972_TASK"); fi;
  T := D972_TASK;
  if not IsBound(T.aut_pair_index) and IsBound(T.automorphism_pair_index) then
    T.aut_pair_index:=T.automorphism_pair_index;
  fi;
  if not IsBound(T.defect_index) and IsBound(T.relator_defect_index) then
    T.defect_index:=T.relator_defect_index;
  fi;
  if not IsBound(T.lift_pair_index) and IsBound(T.marked_lift_index) then
    T.lift_pair_index:=T.marked_lift_index;
  fi;
  if not IsBound(T.q_relators) and IsBound(T.base_relators) then
    T.q_relators:=T.base_relators;
  fi;
  if not IsBound(T.q_order) and IsBound(T.qbar_order) then T.q_order:=T.qbar_order; fi;
  if not IsBound(T.target_keys) and IsBound(T.frozen_target_keys) then
    T.target_keys:=T.frozen_target_keys;
  fi;
  if not IsBound(T.target_keys) and IsBound(T.nf972_target_keys) then
    T.target_keys:=T.nf972_target_keys;
  fi;
  tbl := T.kernel_table;
  k := Length(tbl);
  if not D972TableIsGroup(tbl) or D972CanonicalTable(tbl)<>tbl then
    Error("candidate kernel table is not canonical group table");
  fi;
  auts := D972TableAutomorphisms(tbl);
  acount := Length(auts);
  if T.aut_pair_index < 0 or T.aut_pair_index >= acount^2 then
    Error("aut_pair_index out of range");
  fi;
  a1pos := QuoInt(T.aut_pair_index,acount)+1;
  a2pos := (T.aut_pair_index mod acount)+1;
  defects := D972Digits(T.defect_index,k,Length(T.q_relators));
  liftDigits := D972Digits(T.lift_pair_index,k,2);
  outerBucket := D972OuterBucketPair(tbl,auts,a1pos,a2pos);

  Pdata := D972BuildDefectPresentation(rec(table:=tbl),T.q_relators,
    [auts[a1pos],auts[a2pos]],defects);
  gate := D972ExactEmbeddingGate(Pdata,k,T.q_order);
  P := Pdata.fp;
  pgens := GeneratorsOfGroup(P);
  accepted := false;
  rhoOK := false;
  rhoKernel := fail;
  braid := false;
  generates := false;
  epsOK := false;
  pureExtensionOrder := 0;
  candidateJson := "null";
  if gate.h_embeds and gate.exact_order then
    qdata := D972FpGroupFromSignedRelators(2,T.q_relators,"q");
    Q := qdata.fp;
    qgens := GeneratorsOfGroup(Q);
    if Size(Q)<>T.q_order then Error("task base presentation order drift"); fi;
    rhoImages := Concatenation(List([1..k-1],i->One(Q)),qgens);
    rho := GroupHomomorphismByImages(P,Q,pgens,rhoImages);
    if rho<>fail then
      rhoKernel := Size(Kernel(rho));
      rhoOK := IsSurjective(rho) and rhoKernel=k;
    fi;
    lift1 := Pdata.h_words[liftDigits[1]+1]*Pdata.t_words[1];
    lift2 := Pdata.h_words[liftDigits[2]+1]*Pdata.t_words[2];
    braid := lift1*lift2*lift1=lift2*lift1*lift2;
    generates := Size(Group(lift1,lift2))=Size(P);
    if braid and generates then
      epsilon:=GroupHomomorphismByImages(P,SymmetricGroup(3),[lift1,lift2],
        [(1,2),(2,3)]);
      if epsilon<>fail and IsSurjective(epsilon) then
        pureExtensionOrder:=Size(Kernel(epsilon));
        epsOK:=pureExtensionOrder=k*1469664;
      fi;
    fi;
    accepted := gate.normal and rhoOK and braid and generates and epsOK and
      Image(rho,lift1)=qgens[1] and Image(rho,lift2)=qgens[2];
    if accepted then
      semantic := Concatenation("k=",String(k),";H=",String(D972FlatTable(tbl)),
        ";outer=",String(outerBucket),";aut=",String(T.aut_pair_index),
        ";defect=",String(T.defect_index),";lift=",String(T.lift_pair_index));
      relStrings := List(Pdata.relators,D972SignedWord);
      candidateJson := Concatenation(
        "{\"semantic_key_preorbit\":",D972JsonString(semantic),
        ",\"relative_extension_only\":true",
        ",\"ready_for_producer_ledger\":false",
        ",\"kernel_table\":",String(tbl),
        ",\"outer_bucket\":",String(outerBucket),
        ",\"automorphism_labels\":",String([auts[a1pos],auts[a2pos]]),
        ",\"defects\":",String(defects),
        ",\"lift_labels\":",String(liftDigits),
        ",\"fp_relators\":",String(relStrings),
        ",\"fp_generator_count\":",String(Length(pgens)),
        ",\"factor_images\":",String(Concatenation(List([1..k-1],i->0),[1,2])),
        ",\"order\":",String(gate.p_size),
        ",\"full_b3_quotient_order\":",String(gate.p_size),
        ",\"pure_extension_order\":",String(pureExtensionOrder),
        ",\"kernel_order\":",String(rhoKernel),
        ",\"braid\":true,\"marked_generation\":true}"
      );
    fi;
  fi;
  smallGroupsComplete := IsBound(T.smallgroups_complete) and T.smallgroups_complete;
  if accepted then candidateArray:=candidateJson; else candidateArray:=""; fi;
  nextAut:=T.aut_pair_index; nextDef:=T.defect_index;
  nextLift:=T.lift_pair_index+1; universeExhausted:=false;
  if nextLift=k^2 then
    nextLift:=0; nextDef:=nextDef+1;
    if nextDef=k^Length(T.q_relators) then
      nextDef:=0; nextAut:=nextAut+1;
      if nextAut=acount^2 then universeExhausted:=true; fi;
    fi;
  fi;
  if universeExhausted then nextJson:="null";
  else nextJson:=Concatenation("{\"aut_pair_index\":",String(nextAut),
    ",\"defect_index\":",String(nextDef),",\"lift_pair_index\":",String(nextLift),"}"); fi;
  result := Concatenation(
    "{\"schema\":\"d972_dovetail_worker/v1\",\"mode\":\"candidate\"",
    ",\"status\":\"PASS\",\"smallgroups_complete\":",D972Bool(smallGroupsComplete),
    ",\"h_count\":1,\"aut_count\":",String(acount),
    ",\"base_relator_count\":",String(Length(T.q_relators)),
    ",\"defect_count\":",String(k^Length(T.q_relators)),
    ",\"lift_pair_count\":",String(k^2),
    ",\"cursor\":{\"aut_pair_index\":",String(T.aut_pair_index),
      ",\"defect_index\":",String(T.defect_index),
      ",\"lift_pair_index\":",String(T.lift_pair_index),"}",
    ",\"next_cursor\":",nextJson,
    ",\"current_h_cell_universe_exhausted\":",D972Bool(universeExhausted),
    ",\"k_closed\":false",
    ",\"calibration_only\":",D972Bool(IsBound(T.calibration_only) and T.calibration_only),
    ",\"outer_bucket\":",String(outerBucket),
    ",\"outer_action_valid\":",D972Bool(gate.h_embeds),
    ",\"obstruction_zero\":",D972Bool(gate.h_embeds and gate.exact_order),
    ",\"extension_class_preorbit\":{\"aut_pair_index\":",String(T.aut_pair_index),
      ",\"defect_index\":",String(T.defect_index),"}",
    ",\"outer_action_gate_note\":\"H embeds iff every base relator acts inner with the enumerated defect; this derives the Q-to-Out(H) map without an orientation-sensitive permutation shortcut\"",
    ",\"embedding_gate\":{\"normal\":",D972Bool(gate.normal),
      ",\"h_size\":",String(gate.h_size),",\"p_size\":",String(gate.p_size),
      ",\"h_embeds\":",D972Bool(gate.h_embeds),
      ",\"exact_order\":",D972Bool(gate.exact_order),"}",
    ",\"factor_map_ok\":",D972Bool(rhoOK),
    ",\"pure_extension_order\":",String(pureExtensionOrder),
    ",\"pure_extension_order_exact\":",D972Bool(epsOK),
    ",\"braid\":",D972Bool(braid),",\"marked_generation\":",D972Bool(generates),
    ",\"accepted_count\":",String(Length(Filtered([accepted],x->x))),
    ",\"relative_extension_accepted_count\":",String(Length(Filtered([accepted],x->x))),
    ",\"classification_status\":\"RAW_RELATIVE_EXTENSION_ONLY\"",
    ",\"shadow_fiber_status\":\"REQUIRED_SEPARATE_STAGE\"",
    ",\"exact_972_fibers\":false",
    ",\"ready_for_producer_ledger\":false",
    ",\"relative_extension_completeness_receipt\":",D972CompletenessReceiptJson(),
    ",\"candidates\":[",candidateArray,"]",
    ",\"cursor_advance_authority\":\"this complete receipt only\"}"
  );
  D972Emit(result);
end;;

## A raw relative extension is not a D972 answer.  This second stage performs
## the complete finite classification.  It never uses the theta/tau quotient
## shortcut: both paper-ordered full B3 equations are evaluated literally in
## P=B3/L, so the c-not-in-L case is covered without choosing an F2 word.
## A shadow is settled exactly when its marked images define a bijective
## endomorphism P->P.  Indeed the corresponding B3 map is then that
## automorphism composed with B3->P, hence its source kernel is exactly L.
D972ShadowFiberMode := function()
  local taskPath,T,C,P,pair,s1,s2,k,B,qdata,Q,qgens,qToPerm,pgens,
        rhoImages,rho,rhoOK,gate,markedOK,x,y,c,F2bar,D,Nord,charmingMs,
        fElts,candidatePairCount,m,f,u,lhs,rhs,h33,h34,img1,img2,surj,
        hom,settled,h33Count,h34Count,hexCount,shadowCount,unsettledCount,qf,qperm,idx9,
        idx4,g9f,p4f,key,keyPos,fword,fFp,sourceKey,sourceKeys,sourceMapKeys,sourceRows,
        row,targetKeys,targetSet,targetMaterial,targetDigest,fiberCounts,
        sourceSorted,sourceMaterial,sourceDigest,sourceMapSorted,sourceMapMaterial,
        sourceMapDigest,fiberMaterial,fiberDigest,
        zeroIdx,zeroKeys,positiveCounts,imageCount,fiberSize,uniform,
        isolated,cInL,evalMode,status,accept,exactFibers,firstEmpty,
        result,rowsJson,baseC,baseNord,classificationConsistent,isoP,PP,
        rhoPerm,epsilonP,pureExtensionOrder,i;
  taskPath:=GetEnv("D972_TASK_G");
  if taskPath=fail or taskPath="" then taskPath:=GetEnv("D972_TASK"); fi;
  if taskPath=fail or taskPath="" then Error("shadow-fiber mode needs D972_TASK_G"); fi;
  Read(taskPath);
  if not IsBound(D972_TASK) then Error("shadow-fiber task must bind D972_TASK"); fi;
  T:=D972_TASK;
  if not IsBound(T.q_relators) and IsBound(T.base_relators) then
    T.q_relators:=T.base_relators;
  fi;
  if not IsBound(T.q_order) and IsBound(T.qbar_order) then T.q_order:=T.qbar_order; fi;
  if not IsBound(T.target_keys) then
    Error("shadow-fiber task must carry the frozen ordered target_keys list");
  fi;
  targetKeys:=T.target_keys; targetSet:=Set(targetKeys);
  if Length(targetKeys)<>972 or Length(targetSet)<>972 or
     not ForAll(targetKeys,IsString) then
    Error("frozen target key list must contain 972 distinct strings");
  fi;
  targetMaterial:=Concatenation(D972Join(targetKeys,"\n"),"\n");
  targetDigest:=HexSHA256(targetMaterial);
  ## Reproduction: HexSHA256(Join(tuples,"\n")+"\n") for
  ## search/certs/nf972_sourcemap_b_tuples_v3_20260804.json.
  if targetDigest<>"9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62" then
    Error("frozen NF-972 target-key order/digest mismatch");
  fi;

  C:=D972RebuildMarkedCell(T);
  P:=C.group; pair:=C.pair; s1:=pair[1]; s2:=pair[2]; k:=C.kernel_order;
  B:=D972BuildBase(false);
  if T.q_order<>B.q_size then Error("shadow-fiber base order drift"); fi;
  gate:=D972ExactEmbeddingGate(C.data,k,B.q_size);
  qdata:=D972FpGroupFromSignedRelators(2,T.q_relators,"q");
  Q:=qdata.fp; qgens:=GeneratorsOfGroup(Q);
  if Size(Q)<>B.q_size then Error("shadow-fiber task presentation has wrong order"); fi;
  qToPerm:=GroupHomomorphismByImages(Q,B.q,qgens,[B.s1,B.s2]);
  if qToPerm=fail or not IsBijective(qToPerm) then
    Error("shadow-fiber marked task presentation is not the exact D972 base");
  fi;
  pgens:=C.data.presentation_generators;
  rhoImages:=Concatenation(List([1..k-1],i->One(Q)),qgens);
  rho:=GroupHomomorphismByImages(P,Q,pgens,rhoImages);
  rhoOK:=rho<>fail and IsSurjective(rho) and Size(Kernel(rho))=k and
    Image(rho,s1)=qgens[1] and Image(rho,s2)=qgens[2];
  markedOK:=gate.normal and gate.h_embeds and gate.exact_order and rhoOK and
    s1*s2*s1=s2*s1*s2 and Size(Group(s1,s2))=Size(P);
  if not markedOK then Error("shadow-fiber raw extension witness failed exact rebuild gates"); fi;

  ## Move the exhaustive stage to an exact faithful permutation witness.  The
  ## fp presentation remains the source of truth (and supplies lossless words),
  ## while equality, generation and endomorphism tests use finite permutations.
  isoP:=IsomorphismPermGroup(P);
  if isoP=fail then Error("could not construct faithful permutation witness"); fi;
  PP:=Image(isoP);
  s1:=Image(isoP,s1); s2:=Image(isoP,s2); P:=PP;
  if Size(P)<>gate.p_size or Size(Group(s1,s2))<>Size(P) then
    Error("faithful permutation conversion lost the marked extension");
  fi;
  rhoPerm:=GroupHomomorphismByImages(P,Q,[s1,s2],qgens);
  if rhoPerm=fail or not IsSurjective(rhoPerm) or Size(Kernel(rhoPerm))<>k then
    Error("permutation witness lost the marked factor map");
  fi;
  epsilonP:=GroupHomomorphismByImages(P,SymmetricGroup(3),[s1,s2],[(1,2),(2,3)]);
  if epsilonP=fail or not IsSurjective(epsilonP) then
    Error("permutation witness lost the B3 to S3 map");
  fi;
  pureExtensionOrder:=Size(Kernel(epsilonP));
  if pureExtensionOrder<>k*B.pure_size then
    Error("pure marked extension order is not k*|PB3/M|");
  fi;

  x:=s1^2; y:=s2^2; c:=AbstractProd([s1,s2,s1])^2;
  F2bar:=Group(x,y); D:=DerivedSubgroup(F2bar);
  Nord:=Lcm(Order(x),Order(y),Order(c));
  charmingMs:=Filtered([0..Nord-1],m->Gcd(2*m+1,Nord)=1);
  fElts:=Elements(D);
  candidatePairCount:=Length(charmingMs)*Length(fElts);
  baseC:=AbstractProd([B.s1,B.s2,B.s1])^2;
  baseNord:=Lcm(Order(B.s1^2),Order(B.s2^2),Order(baseC));
  if baseNord<>18 then Error("canonical target N_ord drifted from 18"); fi;

  fiberCounts:=List([1..972],i->0);
  sourceKeys:=[]; sourceMapKeys:=[]; sourceRows:=[];
  h33Count:=0; h34Count:=0; hexCount:=0; shadowCount:=0; unsettledCount:=0;
  for m in charmingMs do
    u:=2*m+1;
    for f in fElts do
      lhs:=AbstractProd([s1^u,f^-1,s2^u,f]);
      rhs:=AbstractProd([f^-1,s1,s2,x^(-m),c^m]);
      h33:=lhs=rhs;
      lhs:=AbstractProd([f^-1,s2^u,f,s1^u]);
      rhs:=AbstractProd([s2,s1,y^(-m),c^m,f]);
      h34:=lhs=rhs;
      if h33 then h33Count:=h33Count+1; fi;
      if h34 then h34Count:=h34Count+1; fi;
      if h33 and h34 then
        hexCount:=hexCount+1;
        img1:=s1^u;
        img2:=AbstractProd([f^-1,s2^u,f]);
        surj:=Size(Group(img1,img2))=Size(P);
        if surj then
          shadowCount:=shadowCount+1;
          hom:=GroupHomomorphismByImages(P,P,[s1,s2],[img1,img2]);
          settled:=hom<>fail and IsBijective(hom);
          if not settled then unsettledCount:=unsettledCount+1; fi;

          ## Exact marked reduction P -> Qbar, then recover the pure K9 and
          ## PSL(2,8) coordinates from the first transversal block of each
          ## direct-sum component.
          qf:=Image(rhoPerm,f); qperm:=Image(qToPerm,qf);
          idx9:=B.qt9.posOf(One(B.k9.G))^qperm;
          idx4:=(B.component9_degree+B.qt4.posOf(One(B.psl4)))^qperm-
            B.component9_degree;
          if idx9<1 or idx9>Length(B.qt9.elts) or
             idx4<1 or idx4>Length(B.qt4.elts) then
            Error("reduced f did not preserve the pure first transversal blocks");
          fi;
          g9f:=B.qt9.elts[idx9]; p4f:=B.qt4.elts[idx4];
          key:=D972NFTargetKey(m,g9f,p4f);
          keyPos:=Position(targetKeys,key);
          if keyPos=fail then
            Error("canonical reduction produced a key outside the frozen 972-set: ",key);
          fi;
          fiberCounts[keyPos]:=fiberCounts[keyPos]+1;
          fFp:=PreImagesRepresentative(isoP,f);
          if fFp=fail then Error("faithful permutation witness has no fp preimage"); fi;
          fword:=D972SignedWord(fFp);
          sourceKey:=Concatenation("(",String(m),";",
            D972Join(List(fword,String),","),")");
          Add(sourceKeys,sourceKey);
          Add(sourceMapKeys,Concatenation(sourceKey,"=>",key));
          row:=Concatenation("{\"m\":",String(m),",\"u\":",String(u),
            ",\"f_word\":",String(fword),
            ",\"target_index\":",String(keyPos-1),
            ",\"target_key\":",D972JsonString(key),
            ",\"settled\":",D972Bool(settled),"}");
          Add(sourceRows,row);
        fi;
      fi;
    od;
  od;
  if shadowCount=0 then Error("identity shadow missing from exhaustive scan"); fi;
  if Length(Set(sourceKeys))<>shadowCount then
    Error("lossless source-key serialization collision");
  fi;
  sourceSorted:=ShallowCopy(sourceKeys); Sort(sourceSorted);
  sourceMaterial:=Concatenation(D972Join(sourceSorted,"\n"),"\n");
  sourceDigest:=HexSHA256(sourceMaterial);
  sourceMapSorted:=ShallowCopy(sourceMapKeys); Sort(sourceMapSorted);
  sourceMapMaterial:=Concatenation(D972Join(sourceMapSorted,"\n"),"\n");
  sourceMapDigest:=HexSHA256(sourceMapMaterial);
  fiberMaterial:=Concatenation(D972Join(List(fiberCounts,String),","),"\n");
  fiberDigest:=HexSHA256(fiberMaterial);
  zeroIdx:=List(Filtered([1..972],i->fiberCounts[i]=0),i->i-1);
  zeroKeys:=List(zeroIdx,i->targetKeys[i+1]);
  positiveCounts:=Set(Filtered(fiberCounts,n->n>0));
  imageCount:=972-Length(zeroIdx);
  uniform:=Length(positiveCounts)=1;
  if uniform then fiberSize:=positiveCounts[1]; else fiberSize:=0; fi;
  isolated:=unsettledCount=0;
  classificationConsistent:=not isolated or
    (uniform and imageCount in [324,972] and shadowCount=imageCount*fiberSize);
  exactFibers:=isolated and classificationConsistent;
  accept:=exactFibers;
  if isolated and not classificationConsistent then status:="INCONSISTENT_STOP";
  else status:="PASS"; fi;
  cInL:=c=One(P);
  if cInL then evalMode:="full_b3_literal_c_in_L";
  else evalMode:="full_b3_literal_c_not_in_L_word_safe"; fi;
  if Length(zeroKeys)=0 then firstEmpty:="null";
  else firstEmpty:=D972JsonString(zeroKeys[1]); fi;
  rowsJson:=D972Join(sourceRows,",");
  result:=Concatenation(
    "{\"schema\":\"d972_dovetail_worker/v1\",\"mode\":\"shadow-fiber\"",
    ",\"status\":",D972JsonString(status),
    ",\"runnable\":true,\"classification_terminal\":true",
    ",\"accept_for_ledger\":",D972Bool(accept),
    ",\"ready_for_producer_ledger\":",D972Bool(accept),
    ",\"relative_extension_rebuilt\":true",
    ",\"extension_order\":",String(Size(P)),
    ",\"full_b3_quotient_order\":",String(Size(P)),
    ",\"pure_extension_order\":",String(pureExtensionOrder),
    ",\"pure_base_order\":",String(B.pure_size),
    ",\"pure_extension_order_exact\":true",
    ",\"kernel_order\":",String(k),
    ",\"factor_map_exact\":",D972Bool(rhoOK),
    ",\"fp_permutation_isomorphism_exact\":true",
    ",\"permutation_witness_degree\":",String(LargestMovedPoint(P)),
    ",\"n_ord\":",String(Nord),",\"target_n_ord\":",String(baseNord),
    ",\"charming_m\":",String(charmingMs),
    ",\"charming_m_count\":",String(Length(charmingMs)),
    ",\"derived_subgroup_order\":",String(Size(D)),
    ",\"charming_pair_universe\":",String(candidatePairCount),
    ",\"hexagon_3_3_pass_count\":",String(h33Count),
    ",\"hexagon_3_4_pass_count\":",String(h34Count),
    ",\"full_hexagon_pair_count\":",String(hexCount),
    ",\"shadow_count\":",String(shadowCount),
    ",\"settled_shadow_count\":",String(shadowCount-unsettledCount),
    ",\"unsettled_shadow_count\":",String(unsettledCount),
    ",\"isolated\":",D972Bool(isolated),
    ",\"all_shadows_settled\":",D972Bool(isolated),
    ",\"source_kernel_method\":\"valid bijective marked endomorphism of finite P=B3/L; its composite with B3 onto P has kernel exactly L\"",
    ",\"full_hexagon_3_3_literal\":true,\"full_hexagon_3_4_literal\":true",
    ",\"shadow_surjectivity_exact\":true",
    ",\"evaluation_mode\":",D972JsonString(evalMode),
    ",\"c_in_l\":",D972Bool(cInL),",\"theta_tau_shortcut_used\":false",
    ",\"target_count\":972,\"target_key_count\":972",
    ",\"target_key_order_sha256\":",D972JsonString(targetDigest),
    ",\"frozen_target_digest_gate\":true",
    ",\"image_size\":",String(imageCount),
    ",\"image_subgroup_order\":",String(imageCount),
    ",\"image_subgroup_order_324_or_972\":",D972Bool(imageCount in [324,972]),
    ",\"fiber_uniform_on_image\":",D972Bool(uniform),
    ",\"fiber_size_on_image\":",String(fiberSize),
    ",\"fiber_counts\":",String(fiberCounts),
    ",\"fiber_vector_sha256\":",D972JsonString(fiberDigest),
    ",\"zero_indices\":",String(zeroIdx),
    ",\"zero_keys\":",String(zeroKeys),
    ",\"zero_count\":",String(Length(zeroKeys)),
    ",\"first_empty_target_key\":",firstEmpty,
    ",\"campaign_stop_first_empty_fiber\":",D972Bool(accept and Length(zeroKeys)>0),
    ",\"equation_3_60_exact\":",D972Bool(exactFibers),
    ",\"exact_972_fibers\":",D972Bool(exactFibers),
    ",\"source_key_count\":",String(Length(sourceKeys)),
    ",\"source_digest_sha256\":",D972JsonString(sourceDigest),
    ",\"source_map_digest_sha256\":",D972JsonString(sourceMapDigest),
    ",\"source_digest_canonicalization\":\"sorted lossless (m;fp-signed-word) records joined by LF with terminal LF\"",
    ",\"source_map_digest_canonicalization\":\"sorted source-key=>frozen-target-key records joined by LF with terminal LF\"",
    ",\"source_rows\":[",rowsJson,"]}"
  );
  D972Emit(result);
end;;

D972RebuildMarkedCell := function(T)
  local tbl,k,auts,acount,a1pos,a2pos,defects,lifts,Pdata,P,l1,l2;
  if not IsBound(T.aut_pair_index) and IsBound(T.automorphism_pair_index) then
    T.aut_pair_index:=T.automorphism_pair_index;
  fi;
  if not IsBound(T.defect_index) and IsBound(T.relator_defect_index) then
    T.defect_index:=T.relator_defect_index;
  fi;
  if not IsBound(T.lift_pair_index) and IsBound(T.marked_lift_index) then
    T.lift_pair_index:=T.marked_lift_index;
  fi;
  if not IsBound(T.q_relators) and IsBound(T.base_relators) then
    T.q_relators:=T.base_relators;
  fi;
  tbl:=T.kernel_table; k:=Length(tbl);
  auts:=D972TableAutomorphisms(tbl); acount:=Length(auts);
  a1pos:=QuoInt(T.aut_pair_index,acount)+1;
  a2pos:=(T.aut_pair_index mod acount)+1;
  defects:=D972Digits(T.defect_index,k,Length(T.q_relators));
  lifts:=D972Digits(T.lift_pair_index,k,2);
  Pdata:=D972BuildDefectPresentation(rec(table:=tbl),T.q_relators,
    [auts[a1pos],auts[a2pos]],defects);
  P:=Pdata.fp;
  l1:=Pdata.h_words[lifts[1]+1]*Pdata.t_words[1];
  l2:=Pdata.h_words[lifts[2]+1]*Pdata.t_words[2];
  return rec(group:=P,pair:=[l1,l2],data:=Pdata,kernel_order:=k,
    automorphism_labels:=[auts[a1pos],auts[a2pos]],defects:=defects,
    lift_labels:=lifts);
end;;

D972CompareMode := function()
  local taskPath,L,R,iso,result;
  taskPath:=GetEnv("D972_TASK_G");
  if taskPath=fail or taskPath="" then taskPath:=GetEnv("D972_TASK"); fi;
  if taskPath=fail or taskPath="" then Error("compare mode needs D972_TASK_G"); fi;
  Read(taskPath);
  if not IsBound(D972_TASK) or not IsBound(D972_TASK.left) or
     not IsBound(D972_TASK.right) then Error("compare task needs left/right cells"); fi;
  L:=D972RebuildMarkedCell(D972_TASK.left);
  R:=D972RebuildMarkedCell(D972_TASK.right);
  if Size(Group(L.pair))<>Size(L.group) or Size(Group(R.pair))<>Size(R.group) then
    Error("compare mode was given a non-generating marked cell");
  fi;
  iso:=D972MarkedPairIsomorphic(L.group,L.pair,R.group,R.pair);
  result:=Concatenation(
    "{\"schema\":\"d972_dovetail_worker/v1\",\"mode\":\"compare\"",
    ",\"status\":\"PASS\",\"marked_over_base_isomorphic\":",D972Bool(iso),
    ",\"criterion\":\"unique pair map well-defined and bijective in both directions\"}"
  );
  D972Emit(result);
end;;

## Minimal complete toy run: Q=C2=<t|t^2>, H=C2.  The identity action and the
## two defects give C2xC2 (non-generating marked lift) and C4 (generating lift).
## Thus exactly one marked extension survives, proving the generic defect path
## includes a nonsplit class and that the generation filter is active.
D972SelfTest := function()
  local tbl, Hrec, aut, split, nonsplit, gs, gn, gateS, gateN,
        pairS, pairN, genS, genN, xN, yN, cN, DN, NordN, m, fN, uN,
        lhsN, rhsN, img1N, img2N, homN, hexN, shadowN, settledN,
        g9, identityTargetKey, targetKeyOK, result;
  tbl := [[0,1],[1,0]];
  if not D972TableIsGroup(tbl) then Error("selftest C2 table rejected"); fi;
  if D972CanonicalTable(tbl) <> tbl then Error("selftest canonical table drift"); fi;
  aut := D972TableAutomorphisms(tbl);
  if Length(aut) <> 1 then Error("selftest Aut(C2) count drift"); fi;
  Hrec := rec(table := tbl);
  split := D972BuildDefectPresentation(Hrec, [[1,1]], [aut[1]], [0]);
  nonsplit := D972BuildDefectPresentation(Hrec, [[1,1]], [aut[1]], [1]);
  gateS := D972ExactEmbeddingGate(split, 2, 2);
  gateN := D972ExactEmbeddingGate(nonsplit, 2, 2);
  pairS := [split.t_words[1], split.t_words[1]];
  pairN := [nonsplit.t_words[1], nonsplit.t_words[1]];
  genS := Size(Group(pairS)) = Size(split.fp);
  genN := Size(Group(pairN)) = Size(nonsplit.fp);
  xN:=pairN[1]^2; yN:=pairN[2]^2;
  cN:=AbstractProd([pairN[1],pairN[2],pairN[1]])^2;
  DN:=Elements(DerivedSubgroup(Group(xN,yN)));
  NordN:=Lcm(Order(xN),Order(yN),Order(cN));
  hexN:=0; shadowN:=0; settledN:=0;
  for m in Filtered([0..NordN-1],m->Gcd(2*m+1,NordN)=1) do
    uN:=2*m+1;
    for fN in DN do
      lhsN:=AbstractProd([pairN[1]^uN,fN^-1,pairN[2]^uN,fN]);
      rhsN:=AbstractProd([fN^-1,pairN[1],pairN[2],xN^(-m),cN^m]);
      if lhsN=rhsN then
        lhsN:=AbstractProd([fN^-1,pairN[2]^uN,fN,pairN[1]^uN]);
        rhsN:=AbstractProd([pairN[2],pairN[1],yN^(-m),cN^m,fN]);
        if lhsN=rhsN then
          hexN:=hexN+1;
          img1N:=pairN[1]^uN;
          img2N:=AbstractProd([fN^-1,pairN[2]^uN,fN]);
          if Size(Group(img1N,img2N))=Size(nonsplit.fp) then
            shadowN:=shadowN+1;
            homN:=GroupHomomorphismByImages(nonsplit.fp,nonsplit.fp,
              pairN,[img1N,img2N]);
            if homN<>fail and IsBijective(homN) then settledN:=settledN+1; fi;
          fi;
        fi;
      fi;
    od;
  od;
  g9:=MakeGn(9);
  identityTargetKey:=D972NFTargetKey(0,One(g9.G),());
  targetKeyOK:=identityTargetKey=
    "(0;0,0,0,0,0,0;1,2,3,4,5,6,7,8,9)";
  result := Concatenation(
    "{\"schema\":\"d972_dovetail_worker/v1\",\"mode\":\"selftest\"",
    ",\"table_group\":true,\"canonical\":true,\"aut_count\":", String(Length(aut)),
    ",\"split\":{\"h_embeds\":", D972Bool(gateS.h_embeds),
      ",\"order\":", String(gateS.p_size), ",\"marked_generates\":", D972Bool(genS), "}",
    ",\"nonsplit\":{\"h_embeds\":", D972Bool(gateN.h_embeds),
      ",\"order\":", String(gateN.p_size), ",\"marked_generates\":", D972Bool(genN), "}",
    ",\"shadow_formula_toy\":{\"n_ord\":",String(NordN),
      ",\"derived_order\":",String(Length(DN)),
      ",\"full_hexagon_count\":",String(hexN),
      ",\"shadow_count\":",String(shadowN),
      ",\"settled_count\":",String(settledN),"}",
    ",\"target_identity_key\":",D972JsonString(identityTargetKey),
    ",\"target_serializer_pass\":",D972Bool(targetKeyOK),
    ",\"relative_extension_completeness_receipt\":",D972CompletenessReceiptJson(),
    ",\"all_pass\":", D972Bool(gateS.h_embeds and gateN.h_embeds and
      gateS.p_size = 4 and gateN.p_size = 4 and not genS and genN and
      NordN=2 and Length(DN)=1 and hexN=2 and shadowN=2 and settledN=2 and
      targetKeyOK), "}"
  );
  D972Emit(result);
end;;

if D972Mode = "selftest" then
  D972SelfTest();
elif D972Mode = "base-audit" then
  D972BaseMode(true);
elif D972Mode = "preflight" then
  D972BaseMode(false);
elif D972Mode = "base-presentation" then
  D972BaseMode(true);
elif D972Mode = "kernel-catalog" then
  D972KernelCatalogMode();
elif D972Mode = "candidate" or D972Mode = "slice" then
  D972CandidateMode();
elif D972Mode = "shadow-fiber" then
  D972ShadowFiberMode();
elif D972Mode = "compare" then
  D972CompareMode();
else
  Error("mode not implemented yet: ", D972Mode);
fi;

QUIT;
