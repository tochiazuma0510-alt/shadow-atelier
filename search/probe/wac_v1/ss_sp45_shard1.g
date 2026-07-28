## ss_sp45_shard1.g -- W-D-Sp45-6a 実現の shard 1(決定的・悉皆)
##
## shard0b で「u を固定したときの因数分解 u = p*q (ord p =3, ord q =2) は 78 通り」
## と判明した(構造定数 24+54)。|C_G(u)| = 12 ゆえ u は 1 個固定してよい(共役で移る)。
## よって **乱択は不要**: 対合を全列挙(10,075 個)して p := u*q の位数 3 を検査し、
## 得られた 78 対それぞれで <a1,b1> = P を検査すれば決着する。
##   a1 := q (位数 2),  b1 := p^-1 (位数 3),  b1^-1*a1 = p*q = u  ✓
## B3 = <a,b | a^2=b^3> (a = Delta = s1s2s1, b = delta = s1s2) より
##   sigma_1 |-> b1^-1*a1 = u,   sigma_2 |-> a1*b1^-1
## シャード: 対合類ごと(cap 検査つき)。
## 実行: .\gap.ps1 search\probe\wac_v1\ss_sp45_shard1.g
SizeScreen([4096,0]);;
Read("search/gaplib_common.g");
t0 := GAPLIB_WallElapsedMs();;
Print("############ ss_sp45 shard1: 決定的悉皆 ############\n");

G := Image(IsomorphismPermGroup(PSp(4,5)));;
n := Size(G);;
deg := LargestMovedPoint(G);;
Print("PSp(4,5): |P| = ", n, "  deg = ", deg, "\n");
ccl := ConjugacyClasses(G);;
ordsC := List(ccl, c -> Order(Representative(c)));;
cenC  := List(ccl, c -> Size(Centralizer(G, Representative(c))));;

# --- 目標類 X (ord 6, |C|=360) と u 源 U (ord 12, 2乗 in X) ---
iX := Filtered([1..Length(ccl)], i -> ordsC[i] = 6 and cenC[i] = 360);;
if Length(iX) <> 1 then Error("目標類が一意でない: ", iX); fi;
iX := iX[1];;
Xrep := Representative(ccl[iX]);;
CX := Centralizer(G, Xrep);;
Print("目標類 X: ord = 6, |C| = ", Size(CX), ", C = ", StructureDescription(CX),
      "  (C3 x SL(2,5)? ", StructureDescription(CX) = "C3 x SL(2,5)", ")\n");
iU := Filtered([1..Length(ccl)], i -> ordsC[i] = 12 and
        Representative(ccl[i])^2 in ccl[iX]);;
if Length(iU) <> 1 then Error("u 源が一意でない: ", iU); fi;
iU := iU[1];;
u := Representative(ccl[iU]);;
Print("u 源 U: ord(u) = ", Order(u), ", |C_G(u)| = ", cenC[iU],
      ", u^2 は目標類か: ", u^2 in ccl[iX], "\n");

invIdx := Filtered([1..Length(ccl)], i -> ordsC[i] = 2);;
Print("対合類 = ", List(invIdx, i -> rec(size := Size(ccl[i]), cen := cenC[i])), "\n");
Print("対合の総数 = ", Sum(invIdx, i -> Size(ccl[i])), "\n");

# --- シャード: 対合類ごとに悉皆 ---
sols := [];;
for i in invIdx do
  lab := Concatenation("shard1-invclass", String(i));
  els := AsList(ccl[i]);
  cnt := 0;
  for q in els do
    if Order(u*q) = 3 then
      cnt := cnt + 1;
      Add(sols, rec(q := q, p := u*q, invclass := i));
    fi;
  od;
  Print("  [", lab, "] |class| = ", Length(els), "  |C| = ", cenC[i],
        "  解 (ord(u*q)=3) = ", cnt, "\n");
  if GAPLIB_CheckCap(600.0, lab) then Error("cap 超過"); fi;
od;
Print("因数分解の総数 = ", Length(sols), "  (shard0b の構造定数 78 と一致? ",
      Length(sols) = 78, ")\n");

# --- 生成条件の検査 ---
Print("\n--- <a1,b1> = P か(", Length(sols), " 対を悉皆)---\n");
genOK := [];;
for s in sols do
  a1 := s.q;
  b1 := (s.p)^-1;
  if Order(a1) <> 2 or Order(b1) <> 3 then Error("位数不整合"); fi;
  if b1^-1*a1 <> u then Error("b1^-1*a1 <> u"); fi;
  if Size(Group(a1,b1)) = n then Add(genOK, rec(a1:=a1, b1:=b1, invclass:=s.invclass)); fi;
od;
Print("生成する対 = ", Length(genOK), " / ", Length(sols), "\n");
Print("  対合類ごとの内訳 = ", Collected(List(genOK, s -> s.invclass)), "\n");
if GAPLIB_CheckCap(600.0, "shard1-gen") then Error("cap 超過"); fi;

# --- 判定 ---
Print("\n############ 判定 ############\n");
if Length(genOK) = 0 then
  Print("REALIZATION = FALSE\n");
  Print("PSp(4,5) には a1^2=b1^3=1, <a1,b1>=P, ord(b1^-1 a1)=12,\n");
  Print("(b1^-1 a1)^2 in [C3 x SL(2,5) の類] を同時に満たす対は **存在しない**\n");
  Print("(u を 1 個固定した 78 通りの因数分解を悉皆・u の類は共役で尽くされる)\n");
else
  Print("REALIZATION = TRUE\n");
  s := genOK[1];
  a1 := s.a1;;  b1 := s.b1;;
  S1P := b1^-1*a1;;   S2P := a1*b1^-1;;
  Print("  a1 := ", a1, ";;\n");
  Print("  b1 := ", b1, ";;\n");
  Print("  ord(a1)=", Order(a1), " ord(b1)=", Order(b1),
        " ord(S1P)=", Order(S1P), " ord(S1P^2)=", Order(S1P^2),
        " S1P^2 in X? ", S1P^2 in ccl[iX], "\n");
  Print("  braid(P 部) s1s2s1 = s2s1s2 ? ", S1P*S2P*S1P = S2P*S1P*S2P, "\n");
  # E = P x S3 を 156+3 = 159 点で組む(P: 1..156, S3: 157,158,159)
  t1 := (157,158);;  t2 := (158,159);;
  S1 := S1P*t1;;  S2 := S2P*t2;;
  E := Group(S1,S2);;
  Print("  JUDGE_S1_IMG := ", S1, ";;\n");
  Print("  JUDGE_S2_IMG := ", S2, ";;\n");
  Print("  JUDGE_ID := \"W-D-Sp45-6a\";;\n");
  Print("  braid 関係 ? ", S1*S2*S1 = S2*S1*S2, "\n");
  Print("  |E| = ", Size(E), " (期待 |P|*6 = ", n*6, " ? ", Size(E) = n*6, ")\n");
  cE := (S1*S2*S1)^2;;
  Print("  ord(c) = ", Order(cE), "   ord(x=S1^2) = ", Order(S1^2),
        "   N_ord = lcm(ord x, ord y, ord c) = ",
        Lcm(Order(S1^2), Order(S2^2), Order(cE)), " (期待 6)\n");
fi;

Print("\n経過 = ", (GAPLIB_WallElapsedMs()-t0)/1000.0, " s\n");
Print("SS_SP45_SHARD1_DONE\n");
QUIT;
