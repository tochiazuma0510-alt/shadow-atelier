## search/probe/hsp7_cond4_laneP_p5control/driver_stepQ1_build_K05_gen_setup_p5.g
## NW-P7 (p=5 control). Q-side: Q5 := K(0,5)/W5, W5 = gamma_5(K(0,5)) K(0,5)^5.
## K(0,5) の fp presentation は p 非依存(hs_prop7_translation_v1.md SS8.7.1-8.7.2)につき
## Lane P 資産(search/probe/hsp7_cond4_laneP/driver_step1_build_K05_gen_setup.g の
## stage1-2継承ロジック)をそのまま再掲・継承する。p-quotient の呼び出しのみ p=5
## (Prime:=5, Exponent:=5) に取り直す(付録A-1未決(a)の後者=司令塔認可済みの読み,
## sol_reply_102_math29.md F102-1.4)。

Read("search/probe/wac_v1/gap_output_prelude.g");
LoadPackage("anupq");

Print("=== NW-P7 driver stepQ1: build K(0,5)fp (inherited stage1-2, p-independent) + gen SetupFile for Q5 ===\n");

## ---- inherited from stage1_pb4.g / driver_step1 (Lane P cond4 calibration) ----
F := FreeGroup("s1","s2","s3");;
s1 := F.1;; s2 := F.2;; s3 := F.3;;
rels := [ s1*s3*s1^-1*s3^-1,
          s1*s2*s1*(s2*s1*s2)^-1,
          s2*s3*s2*(s3*s2*s3)^-1 ];;
B4 := F / rels;;
b1 := B4.1;; b2 := B4.2;; b3 := B4.3;;

X12 := b1^2;;
X23 := b2^2;;
X34 := b3^2;;
X13 := b2*b1^2*b2^-1;;
X24 := b3*b2^2*b3^-1;;
X14 := b3*X13*b3^-1;;

gensPB4 := [X12,X13,X14,X23,X24,X34];;

PB4sub := Subgroup(B4, gensPB4);;
idx := Index(B4, PB4sub);;
Print("[B4:PB4] = ", idx, " (expect 24)\n");

iso := IsomorphismFpGroupByGenerators(PB4sub, gensPB4);;
PB4fp := Image(iso);;
gPB4 := GeneratorsOfGroup(PB4fp);;
gX12 := gPB4[1];; gX13 := gPB4[2];; gX14 := gPB4[3];;
gX23 := gPB4[4];; gX24 := gPB4[5];; gX34 := gPB4[6];;

## ---- inherited from stage2_k05.g ----
Delta2 := (b1*b2*b3)^4;;
Print("Delta4^2 in PB4sub? ", Delta2 in PB4sub, "\n");
Delta2img := ImageElm(iso, Delta2);;

FPB4 := FreeGroupOfFpGroup(PB4fp);;
relsPB4 := RelatorsOfFpGroup(PB4fp);;
Delta2word := UnderlyingElement(Delta2img);;
K05fp := FPB4 / Concatenation(relsPB4, [Delta2word]);;
gK := GeneratorsOfGroup(K05fp);;
kX12 := gK[1];; kX13 := gK[2];; kX14 := gK[3];;
kX23 := gK[4];; kX24 := gK[5];; kX34 := gK[6];;

Print("K05fp: ", K05fp, "\n");
abK := AbelianInvariants(K05fp);;
Print("AbelianInvariants(K05fp) = ", abK, " (expect [0,0,0,0,0])\n");

## sphere row-product dictionary (HS2000 p.3124-3125, j昇順) -- p非依存
x15 := (kX12*kX13*kX14)^-1;;
x25 := (kX12*kX23*kX24)^-1;;
x35 := (kX13*kX23*kX34)^-1;;
x45 := (kX14*kX24*kX34)^-1;;

## rho(x_ij) = x_{i+3,j+3} mod 5 on the 6 named generators (inherited, p非依存)
rhoImages := [ x45, kX14, kX24, x15, x25, kX12 ];;

## anchor (ii) at fp level (inherited check, p非依存)
relsK := RelatorsOfFpGroup(K05fp);;
FK := FreeGroupOfFpGroup(K05fp);;
nbad := 0;;
for r in relsK do
  w := MappedWord(r, GeneratorsOfGroup(FK), rhoImages);
  if not IsOne(w) then nbad := nbad + 1; fi;
od;
Print("anchor(ii) rho well-defined at fp level: bad relators = ", nbad, " / ", Length(relsK), " (expect 0)\n");

## ---- j-embedding and h4/h3 words directly in K05fp (p非依存, inherited) ----
jx := kX12;; jy := kX23;;

jh4 := Comm(Comm(Comm(jx,jy),jx),jx) * Comm(Comm(Comm(jx,jy),jx),jy)^4
       * Comm(Comm(Comm(jx,jy),jy),jy);;
Print("jh4 = j(h4) computed in K05fp (as a word).\n");

jh3 := Comm(Comm(jx,jy),jx) * Comm(Comm(jx,jy),jy);;
Print("jh3 = j(h3) computed in K05fp (as a word).\n");

## ---- NEW for NW-P7: build ANUPQ SetupFile for Q5 = K05fp / W5, W5 = gamma_5(K05fp) K05fp^5 ----
## (only the prime changes vs the cond4 calibration Lane P run, which used Prime:=7)
setupFileQ5 := "search/probe/hsp7_cond4_laneP_p5control/pq_setup_Q5.txt";;
res := Pq(K05fp : Prime := 5, ClassBound := 4, Exponent := 5,
          SetupFile := setupFileQ5);;
Print("Pq(K05fp : Prime:=5, ClassBound:=4, Exponent:=5, SetupFile) returned: ", res, "\n");
Print("SetupFile written to: ", setupFileQ5, "\n");

Print("STAGEQ1_DONE\n");
QUIT;
