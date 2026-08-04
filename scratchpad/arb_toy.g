# arb_toy.g -- independent arbitration check of the Lane V state machine.
# Scale-model window (depth 2 analogue of NW(7)):
#   Q = F2/(gamma3(F2) F2^3) = extraspecial 3^{1+2}, exponent 3, order 27
#   c |-> 1, so B3/N has order 6*27 = 162 and is built LITERALLY from the presentation.
# Dummy family analogue: f = [x,y]^k, k=0,1,2 lives in the TOP layer gamma2(Q)
#   (central, elementary abelian), exactly as h4^t lives in gamma4(P).
#   theta(a)=a^-1 and tau(a)=a  ==> (3.10) and (3.11)|_{m=0} hold exactly.
#   So Prop 3.4 predicts full (3.3)(3.4) PASS for k=0,1,2.

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

FreeB := FreeGroup("s1","s2");;
s1 := FreeB.1;; s2 := FreeB.2;;
xw := s1^2;; yw := s2^2;;
rels := [ s1*s2*s1*(s2*s1*s2)^-1,
          (s1*s2)^3,
          xw^3, yw^3, Comm(xw,yw)^3,
          Comm(Comm(xw,yw),xw), Comm(Comm(xw,yw),yw) ];;
Gfp := FreeB/rels;;
Print("Size(B3/N) = ", Size(Gfp), "  (expect 162)\n");
iso := IsomorphismPermGroup(Gfp);;
S1 := Image(iso, Gfp.1);;  S2 := Image(iso, Gfp.2);;
GP := Group(S1,S2);;
Xg := S1^2;;  Yg := S2^2;;  Cg := (S1*S2)^3;;
Qg := Group(Xg,Yg);;
Print("Size(Q) = ", Size(Qg), " (expect 27);  c trivial in N: ", Cg = One(GP), "\n");
Print("braid relation in the literal group: ", S1*S2*S1 = S2*S1*S2, "\n");
Print("N_ord = ", Lcm([Order(Xg),Order(Yg),Order(Cg)]), "\n");
aa := Comm(Xg,Yg);;
Print("a := [x,y] order ", Order(aa), ", central in Q: ", ForAll(GeneratorsOfGroup(Qg), g -> g*aa = aa*g), "\n\n");

# ===== verbatim copy of Lane V statemachine_lib.g (ApplyGen / ApplyQElt / ApplyGenPow) =====
ApplyGen := function(state, gen, phiX, phiY, phiC)
  local t, d, phiXi, phiYi, phiCi, newT, newD;
  t := state[1]; d := state[2];
  phiXi := phiX^-1; phiYi := phiY^-1; phiCi := phiC^-1;
  if gen = 1 then
    if t=1 then newD:=d; newT:=2;
    elif t=2 then newD:=d*phiX; newT:=1;
    elif t=3 then newD:=d; newT:=5;
    elif t=4 then newD:=d; newT:=6;
    elif t=5 then newD:=d*phiXi*phiYi*phiC; newT:=3;
    else newD:=d*phiY; newT:=4; fi;
  elif gen = -1 then
    if t=1 then newD:=d*phiXi; newT:=2;
    elif t=2 then newD:=d; newT:=1;
    elif t=3 then newD:=d*phiCi*phiY*phiX; newT:=5;
    elif t=4 then newD:=d*phiYi; newT:=6;
    elif t=5 then newD:=d; newT:=3;
    else newD:=d; newT:=4; fi;
  elif gen = 2 then
    if t=1 then newD:=d; newT:=3;
    elif t=2 then newD:=d; newT:=4;
    elif t=3 then newD:=d*phiY; newT:=1;
    elif t=4 then newD:=d*phiYi*phiXi*phiC; newT:=2;
    elif t=5 then newD:=d; newT:=6;
    else newD:=d*phiX; newT:=5; fi;
  elif gen = -2 then
    if t=1 then newD:=d*phiYi; newT:=3;
    elif t=2 then newD:=d*phiCi*phiX*phiY; newT:=4;
    elif t=3 then newD:=d; newT:=1;
    elif t=4 then newD:=d; newT:=2;
    elif t=5 then newD:=d*phiXi; newT:=6;
    else newD:=d; newT:=5; fi;
  else Error("ApplyGen: unknown gen ", gen); fi;
  return [newT, newD];
end;;
ApplyQElt := function(state, q) return [state[1], state[2]*q]; end;;
ApplyGenPow := function(state, genIdx, n, phiX, phiY, phiC)
  local s, i;
  s := state;
  if n >= 0 then for i in [1..n] do s := ApplyGen(s, genIdx, phiX, phiY, phiC); od;
  else for i in [1..(-n)] do s := ApplyGen(s, -genIdx, phiX, phiY, phiC); od; fi;
  return s;
end;;

# ===== TEST A: which coset model does the table implement?  g = d~ * t~ ? =====
TrV := [ One(GP), S1, S2, S1*S2, S2*S1, S1*S2*S1 ];;
StateToElt := function(st) return st[2] * TrV[st[1]]; end;;   # model A: g = d * t
StateToEltB := function(st) return TrV[st[1]] * st[2]; end;;  # model B: g = t * d
GenElt := function(g) if g=1 then return S1; elif g=-1 then return S1^-1;
  elif g=2 then return S2; else return S2^-1; fi; end;;
ApplyWordSeq := function(st, seq, pX,pY,pC)
  local g, s; s := st;
  for g in seq do s := ApplyGen(s, g, pX,pY,pC); od; return s;
end;;
LiteralSeq := function(seq)
  local g, e; e := One(GP);
  for g in seq do e := e * GenElt(g); od; return e;
end;;
testSeqs := [ [1], [2], [1,1], [2,2], [1,1,2,2], [2,2,1,1], [1,2,1], [2,1,2],
              [-1,2,2,-1], [1,-2,1,-2,1], [1,1,1,2,-1,-1,2,2], [-2,-1,-2,1,1,2] ];;
okA := 0;; okB := 0;;
for sq in testSeqs do
  st := ApplyWordSeq([1, One(Qg)], sq, Xg, Yg, Cg);
  if StateToElt(st)  = LiteralSeq(sq) then okA := okA + 1; fi;
  if StateToEltB(st) = LiteralSeq(sq) then okB := okB + 1; fi;
od;
Print("TEST A (coset model of the ApplyGen table), ", Length(testSeqs), " words:\n");
Print("  model A  g = d~ * t~ , left-to-right = paper order : ", okA, "/", Length(testSeqs), " [", PF(okA=Length(testSeqs)), "]\n");
Print("  model B  g = t~ * d~                               : ", okB, "/", Length(testSeqs), " [", PF(okB=Length(testSeqs)), "]\n\n");

# ===== TEST B: the correctness contract of ApplyQElt =====
# state (t,d) denotes g = d~ t~ .  Right-multiplying g by a pure-Q element q must give
# g*q = d~ t~ q~ .  ApplyQElt returns [t, d*q] which denotes d~ q~ t~ = g * (t~^-1 q~ t~).
Print("TEST B (ApplyQElt contract:  ApplyQElt(s,q) must equal s * q ):\n");
qsample := [Xg, Yg, aa, Xg*Yg];;
badB := 0;; totB := 0;;
for t in [1..6] do
  for q in qsample do
    totB := totB + 1;
    if StateToElt(ApplyQElt([t, One(Qg)], q)) <> TrV[t]*q then badB := badB + 1; fi;
  od;
od;
Print("  violations = ", badB, " / ", totB, "   (0 expected if ApplyQElt were correct)\n");
for t in [1..6] do
  Print("    t=", t, ": ApplyQElt-vs-truth agrees for q in sample: ",
        List(qsample, q -> StateToElt(ApplyQElt([t,One(Qg)],q)) = TrV[t]*q), "\n");
od;
Print("\n");

# ===== TEST Cg: full (3.3)(3.4) three ways =====
# (i) literal in B3/N ; (ii) Lane V EvalFullHexagon verbatim ; (iii) fixed = sigma-word expansion
EvalLiteral := function(m, f)
  local u;
  u := 2*m+1;
  return rec(hex33 := (S1^u * f^-1 * S2^u * f = f^-1 * S1 * S2 * Xg^(-m) * Cg^m),
             hex34 := (f^-1 * S2^u * f * S1^u = S2 * S1 * Yg^(-m) * Cg^m * f));
end;;
# Lane V verbatim
EvalFullHexagon := function(m, f, phiX, phiY, phiC)
  local u, base, finv, xm, ym, cm, lhs33, rhs33, lhs34, rhs34, s;
  u := 2*m+1;  finv := f^-1;  xm := phiX^(-m);  cm := phiC^m;
  base := [1, Identity(f)];
  s := ApplyGenPow(base, 1, u, phiX, phiY, phiC);
  s := ApplyQElt(s, finv);
  s := ApplyGenPow(s, 2, u, phiX, phiY, phiC);
  s := ApplyQElt(s, f);      lhs33 := s;
  s := ApplyQElt(base, finv);
  s := ApplyGenPow(s, 1, 1, phiX, phiY, phiC);
  s := ApplyGenPow(s, 2, 1, phiX, phiY, phiC);
  s := ApplyQElt(s, xm);
  s := ApplyQElt(s, cm);     rhs33 := s;
  s := ApplyQElt(base, finv);
  s := ApplyGenPow(s, 2, u, phiX, phiY, phiC);
  s := ApplyQElt(s, f);
  s := ApplyGenPow(s, 1, u, phiX, phiY, phiC);  lhs34 := s;
  ym := phiY^(-m);
  s := ApplyGenPow(base, 2, 1, phiX, phiY, phiC);
  s := ApplyGenPow(s, 1, 1, phiX, phiY, phiC);
  s := ApplyQElt(s, ym);
  s := ApplyQElt(s, cm);
  s := ApplyQElt(s, f);      rhs34 := s;
  return rec(hex33 := (lhs33 = rhs33), hex34 := (lhs34 = rhs34),
             defect33 := rhs33[2]^-1 * lhs33[2], defect34 := rhs34[2]^-1 * lhs34[2]);
end;;
# fixed: every pure-Q factor is expanded into a sigma-letter sequence and pushed
# through the (validated) ApplyGen.   x = s1^2, y = s2^2, a = [x,y] = x^-1 y^-1 x y
SeqPow := function(seq, k)
  local r, i, inv, g;
  r := [];
  if k >= 0 then for i in [1..k] do Append(r, seq); od;
  else inv := Reversed(List(seq, g -> -g));
       for i in [1..(-k)] do Append(r, inv); od; fi;
  return r;
end;;
seqA := [-1,-1,-2,-2,1,1,2,2];;      # a = [x,y]
seqX := [1,1];;                       # x
seqY := [2,2];;                       # y
EvalFixed := function(m, k)
  local u, fs, fis, s, l33, r33, l34, r34;
  u := 2*m+1;
  fs  := SeqPow(seqA, k);  fis := SeqPow(seqA, -k);
  s := ApplyWordSeq([1,One(Qg)], Concatenation(SeqPow(seqX,0), []), Xg,Yg,Cg);
  # LHS(3.3) = s1^u f^-1 s2^u f
  s := ApplyWordSeq([1,One(Qg)], Concatenation(SeqPow([1],u), fis, SeqPow([2],u), fs), Xg,Yg,Cg);  l33 := s;
  # RHS(3.3) = f^-1 s1 s2 x^-m c^m      (c=1 here)
  s := ApplyWordSeq([1,One(Qg)], Concatenation(fis, [1,2], SeqPow(seqX,-m)), Xg,Yg,Cg);            r33 := s;
  # LHS(3.4) = f^-1 s2^u f s1^u
  s := ApplyWordSeq([1,One(Qg)], Concatenation(fis, SeqPow([2],u), fs, SeqPow([1],u)), Xg,Yg,Cg);  l34 := s;
  # RHS(3.4) = s2 s1 y^-m c^m f
  s := ApplyWordSeq([1,One(Qg)], Concatenation([2,1], SeqPow(seqY,-m), fs), Xg,Yg,Cg);             r34 := s;
  return rec(hex33 := (l33 = r33), hex34 := (l34 = r34));
end;;

Print("TEST Cg: full (3.3)(3.4), m=0, f = a^k = [x,y]^k   (Prop 3.4 predicts PASS for all k)\n");
Print("   k | literal(3.3,3.4) | LaneV verbatim | LaneV defect(3.3) = f ? | fixed(sigma-word)\n");
for k in [0,1,2] do
  f := aa^k;
  lit := EvalLiteral(0, f);
  lv  := EvalFullHexagon(0, f, Xg, Yg, Cg);
  fx  := EvalFixed(0, k);
  Print("   ", k, " | ", PF(lit.hex33), "/", PF(lit.hex34),
        "  | ", PF(lv.hex33), "/", PF(lv.hex34),
        "  | ", lv.defect33 = f, "  | ", PF(fx.hex33), "/", PF(fx.hex34), "\n");
od;
Print("\nTEST C2: same, m=2 (the other element of X_N), f = a^k -- machine-vs-literal only\n");
for k in [0,1,2] do
  f := aa^k;
  lit := EvalLiteral(2, f);
  lv  := EvalFullHexagon(2, f, Xg, Yg, Cg);
  fx  := EvalFixed(2, k);
  Print("   k=", k, " literal=", PF(lit.hex33), "/", PF(lit.hex34),
        "  LaneV=", PF(lv.hex33), "/", PF(lv.hex34),
        "  fixed=", PF(fx.hex33), "/", PF(fx.hex34), "\n");
od;
Print("\n[DONE]\n");
QUIT;
