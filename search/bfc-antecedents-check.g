# search/bfc-antecedents-check.g -- 第二系統(GAP)照合: docs/week4-BFC攻略_opus_v1.md
# の検算 V1-V8(search/week4-bfc-antecedents.mjs, node 単系統 13/13)を、
# node のソースを一切参照せず、G_3 = PB_3/K^(3) の定義(D1 (3.1)(3.6)(4.9)(4.12))
# から独立に GAP で再構成して検査する。
#
# 規律:
#  - helper 非共有: 本スクリプトは search/week4-bfc-antecedents.mjs を import/参照しない。
#    G3 の構成(MakeDn/MakeGn)は search/k3-lambda-action.g(既存・独立に D1 から
#    再構成済み)の permutation-group 実装を再利用する -- これは node の
#    integer-encoding 実装(dec/enc1/mul1)とは別の表現であり、"同じ helper" ではない。
#  - 入力は docs/week4-BFC攻略_opus_v1.md の V1-V8 の主張文そのもの(§11.2 の表と
#    search/week4-bfc-antecedents.mjs 冒頭コメントの定義)。数値レベルで突合する。
#  - K^(5) 個別モデル・u には一切触れない。
#
# Usage: .\gap.ps1 search\bfc-antecedents-check.g
#
# ================================================================================

Read("search/gaplib_common.g");;
startTime := Runtime();;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;
pass := 0;; failCount := 0;;
ck := function(name, ok)
  if ok then pass := pass + 1; else failCount := failCount + 1; fi;
  Print("[", PF(ok), "] ", name, "\n");
end;;

# ================= MakeDn / MakeGn(search/k3-lambda-action.g と同一実装を再利用) =================
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

gn := MakeGn(3);;
G3 := gn.G;; xg := gn.x;; yg := gn.y;; r := gn.r;; s := gn.s;; tr := gn.tr;;
Print("|G3| = ", Size(G3), " (expect 108)\n");
if Size(G3) <> 108 then Error("G3 order mismatch"); fi;

# ================= z-bar の marked transport (Sol 便44 F6.1 修理) =================
# D1 (3.6): z-bar = (x-bar y-bar)^{-1} = (r^2 s, r^-1 s, r)。x-bar,y-bar は
# MakeGn 内部で「論文の rs は GAP の s*r」という移送規約(Sol 便01 F3,
# Phi=(phi_1,id,phi_3), phi_1(r)=r, phi_1(s)=r^-2 s, phi_3(r)=r^-1, phi_3(s)=s)
# を y-bar = tr(s*r,1)*tr(r,2)*tr(s*r,3) に既に適用して構成されている。
# ところが旧版はここで z-bar だけ生の座標 (r^2 s, r^-1 s, r) を未移送のまま
# tr() に渡していたため、x_g y_g z_g <> 1 になっていた(便44 F6.1 実測:
# n=3 で (r,1,r^2))。安全な修理は zg を (xg*yg)^-1 として直接計算すること --
# xg,yg は既に一貫して移送済みなので、積の逆元を取るだけで自動的に整合する。
# 独立確認として、Phi を D_n 上の準同型として明示構成し、D1 (3.6) の生の
# 座標に Phi を後合成した結果とも一致することを検査する(Phi による同時
# 移送を certificate に残す -- 便44 F6.3 item 4)。
Dn := Group(r, s);;
phi1 := GroupHomomorphismByImages(Dn, Dn, [r, s], [r, r^-2*s]);;
phi3 := GroupHomomorphismByImages(Dn, Dn, [r, s], [r^-1, s]);;
if phi1 = fail or phi3 = fail then
  Error("*** FORMULA-MISMATCH: phi1/phi3 (Sol 便01 Phi transport) は D_n の well-defined homomorphism にならない");
fi;

zg := (xg * yg)^-1;;
zgPhi := tr(Image(phi1, r^2*s), 1) * tr(r^-1*s, 2) * tr(Image(phi3, r), 3);;
ck("0a x_g*y_g*z_g = 1 (D1 (3.6) fixture, fail-closed -- 便44 F6.3 item 1)", xg*yg*zg = One(G3));
ck("0a' z_g = (x_g y_g)^-1 は Phi による生座標の明示移送と一致(独立確認 -- 便44 F6.3 item 4)",
   zg = zgPhi);

# ================= x-bar, y-bar の marked transport(便45 F4.3 修理) =================
# 便44 F6.3 item 4 は「x,y,z,f_{m,k} の同時移送を証明書化」を要求していたが、
# 旧版(v2 証明書)は z_phi_transport_check と kappa_phi_sign_check しか持たず、
# x,y の生座標 (D1 (3.6): x-bar = (r,s,s), y-bar = (rs,r,rs)) を Phi=(phi1,id,phi3)
# に通した結果が xg,yg と一致するか、独立に検査していなかった(Sol 便45 F4.3)。
# 以下で x,y も z と同じ様式で fixture 化する。
xgPhi := tr(Image(phi1, r), 1) * tr(s, 2) * tr(Image(phi3, s), 3);;
ygPhi := tr(Image(phi1, r*s), 1) * tr(r, 2) * tr(Image(phi3, r*s), 3);;
ck("0b x_g は D1 (3.6) 生座標 (r,s,s) の Phi 移送と一致(便45 F4.3)", xg = xgPhi);
ck("0c y_g は D1 (3.6) 生座標 (rs,r,rs) の Phi 移送と一致(便45 F4.3)", yg = ygPhi);

M := Order(xg);;
ck("0 ord(X) = 6 = M", M = 6);

# ================= cycle-type helper(cosets 上の置換の型) =================
CycleType := function(p, d)
  local seen, out, i, j, l;
  seen := List([1..d], x -> false);
  out := [];
  for i in [1..d] do
    if seen[i] then continue; fi;
    j := i; l := 0;
    while not seen[j] do
      seen[j] := true; j := j^p; l := l + 1;
    od;
    Add(out, l);
  od;
  Sort(out, function(a,b) return a > b; end);
  return out;
end;;

# ================= 全部分群の悉皆(V3 用) =================
Print("\n-- LatticeSubgroups(G3) による悉皆(全サイズ) --\n");
L := LatticeSubgroups(G3);;
ccs := ConjugacyClassesSubgroups(L);;
allSubs := [];;
for c in ccs do
  Append(allSubs, AsList(c));
od;
Print("全部分群数 (全共役類展開後) = ", Length(allSubs), "\n");

# ================= 標的 H の同定(order 18, |Lambda|=6, N_P(H)=H, passport (6,2^2 1^2,6)) =================
order18 := Filtered(allSubs, H -> Size(H) = 18);;
Print("order-18 部分群数 = ", Length(order18), "\n");

target := fail;;
for H in order18 do
  if Index(G3, Normalizer(G3, H)) <> 6 then continue; fi;   # |Lambda| = 6
  cosetsH := RightCosets(G3, H);;
  d := Length(cosetsH);;
  hom := ActionHomomorphism(G3, cosetsH, OnRight);;
  ctx := CycleType(Image(hom, xg), d);;
  cty := CycleType(Image(hom, yg), d);;
  ctz := CycleType(Image(hom, zg), d);;
  if ctx = [6] and cty = [2,2,1,1] and ctz = [6] and Normalizer(G3,H) = H then
    target := H; break;
  fi;
od;
ck("1 標的 H を同定(order 18, passport (6,2^2 1^2,6), N_G(H)=H)", target <> fail);

H := target;;
cosetsH := RightCosets(G3, H);;
d := Length(cosetsH);;
hom := ActionHomomorphism(G3, cosetsH, OnRight);;
pxRight := Image(hom, xg);;

# ================= V1: [P:H] = 6 = M かつ <X> は P/H 上推移的 =================
ck("V1 [P:H] = 6 = M かつ <X> は P/H 上推移的(全分岐)",
   d = 6 and Length(Orbit(Group(pxRight), 1)) = 6);

# ================= V2: N_P(H) = H =================
ck("V2 N_P(H) = H", Normalizer(G3, H) = H);

# ================= V3: 「<X> 推移的 かつ |Lambda| = ord(X) = 6」を満たす全 H で N_P(H) = H =================
v3n := 0;; v3bad := 0;;
for Hc in allSubs do
  if Size(Hc) = 1 or Size(Hc) = 108 then continue; fi;
  csc := RightCosets(G3, Hc);;
  dc := Length(csc);;
  homc := ActionHomomorphism(G3, csc, OnRight);;
  pxc := Image(homc, xg);;
  if not Length(Orbit(Group(pxc), 1)) = dc then continue; fi;   # <X> 推移的
  if Index(G3, Normalizer(G3, Hc)) <> 6 then continue; fi;       # |Lambda| = 6 = M
  v3n := v3n + 1;
  if Normalizer(G3, Hc) <> Hc then v3bad := v3bad + 1; fi;
od;
# 便45 F4.2: 便44 F6.3 item 6 が要求したのは「v3n = 12」の明示 assert であり、
# 旧版の `v3n > 0` は将来値がずれても無音で PASS してしまう(差戻し理由3)。
ck(Concatenation("V3 <X> 推移的 かつ |Lambda| = ord(X) を満たす全 H で N_P(H) = H (該当 H = ",
   String(v3n), " 個, 反例 = ", String(v3bad), ", 期待値 12)"), v3bad = 0 and v3n = 12);

# ================= Lambda(target の共役類・6 元)の構成 =================
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

Lam := BuildLambda(H);;
ck("1b |Lambda| = 6", Length(Lam) = 6);

IndexOfSub := function(list, K)
  local i;
  for i in [1..Length(list)] do
    if list[i] = K then return i; fi;
  od;
  return fail;
end;;

# ================= V4: P/H -> Lambda, gH |-> gHg^{-1} が <X>-同変な全単射(左剰余類 gH) =================
LeftCosetsList := function(G, Hs)
  local eltsH, seen, out, g, c;
  eltsH := Elements(Hs);
  seen := [];
  out := [];
  for g in G do
    c := Set(List(eltsH, h -> g*h));
    if not c in seen then
      Add(seen, c); Add(out, c);
    fi;
  od;
  return out;
end;;

LC := LeftCosetsList(G3, H);;
ck("1c |P/H(左剰余類)| = 6", Length(LC) = 6);

# 注: GAP の共役 `H^g` は右作用 g^{-1} H g。論文語の左作用 gHg^{-1} は `H^(g^-1)`
# で実現する(gaplib_common.g の罠(5)と同型の規約差)。
ConjLeft := function(C, g) return C^(g^-1); end;;

cosetToLam := List(LC, c -> IndexOfSub(Lam, ConjLeft(H, c[1])));;
permX := List(LC, c -> Position(LC, Set(List(Elements(H), h -> (xg*c[1])*h))));;
tauX := List(Lam, C -> IndexOfSub(Lam, ConjLeft(C, xg)));;

v4bij := (Length(Set(cosetToLam)) = 6) and not (fail in cosetToLam);;
v4equiv := true;;
for i in [1..6] do
  if cosetToLam[permX[i]] <> tauX[cosetToLam[i]] then v4equiv := false; fi;
od;
ck("V4 P/H -> Lambda は全単射かつ <X>-同変(左移動 <-> tau)", v4bij and v4equiv);
ck("V4b tau は Lambda 上の 6-サイクル(単純推移)", CycleType(PermList(tauX), 6) = [6]);

tauPerm := PermList(tauX);;

# ================= Phi_{m,k}(GT(K^(3)) の 12 元)の構成 =================
# kapExp の根拠(便44 F6.2 修理):
# f_{m,k} = (r^{2k}, r^{-2k}, r^{kappa(m)}) は z-bar と同じ第 3 スロットの
# 生座標パターンであり、z-bar と同じ Phi=(phi_1,id,phi_3) の移送(phi_3(r)=r^-1)
# を第 3 スロットに適用しなければならない(移送を怠ると z-bar と同じ
# x_g y_g z_g <> 1 型の不整合が起きる)。phi_3(r^kappa(m)) = r^{-kappa(m)} なので
# kapExp = (-kap) mod 3 であり、「全単射になる符号を試して選んだ」のではなく
# Phi の明示移送から導ける値である。下の kapPhiCheck で
# Image(phi_3, r^kap) = r^kapExp を kap in {0,1,2} 全部について検査し、
# 導出の正しさを certificate に残す(便44 F6.3 item 4)。IsBijective は
# その後の独立な反証テスト(構成が本当に Aut(G3) の元になっているかの
# fail-closed ガード)であり、符号の選定根拠ではない。
kapPhiCheck := true;;
for kapT in [0, 1, 2] do
  if Image(phi3, r^kapT) <> r^((-kapT) mod 3) then kapPhiCheck := false; fi;
od;
ck("2a kappa(m) 第3スロットの符号 -kap は phi_3(r)=r^-1 の明示移送と一致(便44 F6.2)",
   kapPhiCheck);

BuildPhi := function(m, k)
  local u, kap, kapExp, fk, fkRaw, fkPhi, fkTransportOk, imgX, imgY, phi;
  u := 2*m + 1;
  if m mod 2 = 1 then kap := (m + 1) mod 3; else kap := (-m) mod 3; fi;
  kapExp := (-kap) mod 3;
  fk := tr(r^(2*k), 1) * tr(r^(-2*k), 2) * tr(r^kapExp, 3);
  # 便45 F4.3: f_{m,k} = (r^{2k}, r^{-2k}, r^{kappa(m)}) の生座標(第4.9)(4.12)式)
  # に Phi=(phi1,id,phi3) を後合成した結果が fk(上で kapExp を使って組んだ実装値)
  # と一致することを、抽象的な符号一致(kapPhiCheck、kap in {0,1,2} の総当り)とは
  # 別に、実際にこの (m,k) で使う具体的な三成分すべてについて検査する。
  fkPhi := tr(Image(phi1, r^(2*k)), 1) * tr(r^(-2*k), 2) * tr(Image(phi3, r^kap), 3);;
  fkTransportOk := (fk = fkPhi);;
  imgX := xg^u;
  imgY := fk^-1 * (yg^u) * fk;
  phi := GroupHomomorphismByImages(G3, G3, [xg, yg], [imgX, imgY]);
  return rec(m := m, k := k, kappa := kap, phi := phi, fkTransportOk := fkTransportOk);
end;;

GTel := [];;
for m in [0, 2, 3, 5] do
  for k in [0, 1, 2] do
    rr := BuildPhi(m, k);;
    if rr.phi = fail or not IsBijective(rr.phi) then
      Error("*** FORMULA-MISMATCH: (m,k)=(", m, ",", k, ") は G3 の自己同型にならない");
    fi;
    Add(GTel, rr);
  od;
od;
ck("2 GT(K^(3)) の 12 元がすべて Aut(G3) の元(構成 + 全単射確認)", Length(GTel) = 12);
ck("2b GT(K^(3)) 全 12 元の f_{m,k} が D1 (4.9)(4.12) 生座標の Phi 移送と一致(便45 F4.3)",
   ForAll(GTel, e -> e.fkTransportOk));

# 便45 F4.3: x,y,z,f_{m,k} の同時移送を単一の fail-closed fixture として集約する
# (「Phi による全 marking の同時移送」の証明書化 -- 差戻し理由 3)。
allMarkingsPhiTransportOk :=
  (xg = xgPhi) and (yg = ygPhi) and (zg = zgPhi) and ForAll(GTel, e -> e.fkTransportOk);;
ck("2c Phi による x,y,z,f_{m,k} の全 marking の同時移送(便45 F4.3・差戻し理由3)",
   allMarkingsPhiTransportOk);

StabLambda := function(phi)
  local C, img;
  for C in Lam do
    img := Image(phi, C);;
    if IndexOfSub(Lam, img) = fail then return false; fi;
  od;
  return true;
end;;

F0el := Filtered(GTel, e -> e.m = 0);;
ck("V5 Lambda は Phi(F_0)(3 元)で安定", Length(F0el) = 3 and ForAll(F0el, e -> StabLambda(e.phi)));
ck("V6 Lambda は Phi(GT(K^(3))) 全 12 元で安定(Q-model 側の前件)", ForAll(GTel, e -> StabLambda(e.phi)));

# ================= V7: Aut(G3) 全体(GAP 組込み AutomorphismGroup で独立再計算)・Lambda 安定は 432 個 =================
Print("\n-- AutomorphismGroup(G3) を GAP 組込みで独立計算 --\n");
AutG3 := AutomorphismGroup(G3);;
autOrder := Size(AutG3);;
Print("|Aut(G3)| = ", autOrder, " (expect 1296)\n");

autStabCount := 0;;
for a in AutG3 do
  if StabLambda(a) then autStabCount := autStabCount + 1; fi;
od;
ck(Concatenation("V7 Aut(G3) 全体では Lambda は安定でない(|Aut(G3)|=", String(autOrder),
   ", Lambda を保つ元=", String(autStabCount), ")"),
   autOrder = 1296 and autStabCount = 432 and autStabCount < autOrder);

# GT(K^(3)) の 12 元が実際に AutG3 の 432 元の中に入っているか(独立確認)
gtInAut432 := ForAll(GTel, e -> e.phi in AutG3 and StabLambda(e.phi));;
ck("V6' GT(K^(3)) の 12 元は Aut(G3) の元であり、かつ Lambda-stabilizer 432 元の中にある", gtInAut432);

# ================= V8: b-不変性(finite 版, b in (Z/6)^x = {1,5}) =================
v8ok := true;;
for b in [1, 5] do
  for t in [0 .. 5] do
    if Gcd(6, t) <> Gcd(6, (b*t) mod 6) then v8ok := false; fi;
    if (t = 0) <> (((b*t) mod 6) = 0) then v8ok := false; fi;
  od;
  # tau(mu_6) 生成群が b-ひねりで不変(tau^b が生成する群 = tau が生成する群)
  if Group(tauPerm^b) <> Group(tauPerm) then v8ok := false; fi;
od;
ck("V8 b in (Z/6)^x のひねりで ord(kappa)・ker(kappa)・tau(mu_6) が不変(系 B-8)", v8ok);

# ================= Sol 便 43 F2.1 の反例(正の統制): P = S3 x C2, H = <(12)> x C2, X = ((123),c) =================
Print("\n-- Sol 便 43 F2.1 の反例の GAP 再現(旧 B-2 pairwise 同値の反証・正の統制) --\n");
S3 := Group((1,2,3),(1,2));;
C2 := Group((1,2));;
Pprod := DirectProduct(S3, C2);;
e1 := Embedding(Pprod, 1);; e2 := Embedding(Pprod, 2);;
Xctr := Image(e1, (1,2,3)) * Image(e2, (1,2));;
Hctr := Group(Image(e1, (1,2)), Image(e2, (1,2)));;
idxPH := Index(Pprod, Hctr);;
Mctr := Order(Xctr);;
NPH := Normalizer(Pprod, Hctr) = Hctr;;
ck(Concatenation("F2.1 再現: |P|=", String(Size(Pprod)), ", |H|=", String(Size(Hctr)),
   ", [P:H]=", String(idxPH), ", M=ord(X)=", String(Mctr), ", N_P(H)=H は ", PF(NPH)),
   Size(Pprod) = 12 and Size(Hctr) = 4 and idxPH = 3 and Mctr = 6 and NPH);
ck("F2.1 ★ [P:H] = 3 <> 6 = M(旧 B-2 の pairwise 同値「N_P(H)=H <=> [P:H]=M」は偽・反例確認)",
   idxPH <> Mctr and NPH);

# 便44 F6.3 item 3: <X> が P/H 上推移的であることを明示に検査する
# (旧版は位数・指数・normalizer だけで、<Xctr> の推移性を assert していなかった)。
cosetsCtr := RightCosets(Pprod, Hctr);;
homCtr := ActionHomomorphism(Pprod, cosetsCtr, OnRight);;
pxCtr := Image(homCtr, Xctr);;
transCtr := Length(Orbit(Group(pxCtr), 1)) = idxPH;;
ck("F2.1c <X> は P/H 上推移的(便44 F6.3 item 3)", transCtr);

Print("\n=== ", pass, "/", pass + failCount, " PASS ===\n");

# ================= fail-closed gate(便45 F4.2 修理・差戻し理由3) =================
# 旧版は ck() が failCount を数えるだけで、失敗があっても常に certificate を
# 書き出していた(「fail-closed」と報告しながら実装されていなかった)。
# ここで failCount <> 0 なら証明書を書かずに Error で停止する。
if failCount <> 0 then
  Error("*** FAIL-CLOSED: ", failCount, " 件の検査が FAIL した。証明書は書き出さない(便45 F4.2)。");
fi;

# ================= script/input digest(便44 F6.3 item 5) =================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_bfc.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/bfc-antecedents-check.g");;
inputMdSha256 := ComputeSha256File("docs/week4-BFC攻略_opus_v1.md");;
nodeCertSha256 := ComputeSha256File("search/week4-bfc-antecedents.mjs");;

# ================= 証明書 JSON =================
cert := Concatenation(
  "{\"schema\":\"bfc-antecedents-check/v3\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/bfc-antecedents-check.g\"}",
  ",\"repair_note\":\"Sol 便45 F4 修理(裁定47・差戻し理由3,4): (1) x_g,y_g も z_g と同じ",
  "様式で D1 (3.6) 生座標の Phi=(phi1,id,phi3) 移送と一致することを fixture 化",
  "(旧版は z のみ)。(2) f_{m,k}(GT(K^(3)) 全12元)についても D1 (4.9)(4.12) 生座標の",
  "Phi 移送と一致することを個別に検査し、x,y,z,f_{m,k} の同時移送を単一 fixture",
  "(all_markings_phi_transport_check)として集約。(3) V3 の assert を v3n>0 から",
  "v3n=12 の明示値一致へ強化。(4) certificate 書出し前に failCount<>0 なら Error",
  "する fail-closed gate を実装(旧版は数えるだけで常に書き出していた)。",
  "旧版(v1 は certificates/bfc/retracted/、本便直前の v2 も同ディレクトリへ撤回)。\"",
  ",\"target_group\":{\"name\":\"G3<=D3^3\",\"order\":", String(Size(G3)), "}",
  ",\"target_H\":{\"order\":", String(Size(H)), ",\"index\":", String(d), ",\"lambda_size\":", String(Length(Lam)), "}",
  ",\"pass_count\":", String(pass),
  ",\"fail_count\":", String(failCount),
  ",\"xyz_identity_check\":", JB(xg*yg*zg = One(G3)),
  ",\"x_phi_transport_check\":", JB(xg = xgPhi),
  ",\"y_phi_transport_check\":", JB(yg = ygPhi),
  ",\"z_phi_transport_check\":", JB(zg = zgPhi),
  ",\"fk_phi_transport_check_all12\":", JB(ForAll(GTel, e -> e.fkTransportOk)),
  ",\"all_markings_phi_transport_check\":", JB(allMarkingsPhiTransportOk),
  ",\"kappa_phi_sign_check\":", JB(kapPhiCheck),
  ",\"v3_matching_H_count\":", String(v3n),
  ",\"v3_counterexample_count\":", String(v3bad),
  ",\"v3_expected_count\":12",
  ",\"aut_G3_order\":", String(autOrder),
  ",\"aut_G3_lambda_stabilizer_count\":", String(autStabCount),
  ",\"gt_k3_element_count\":", String(Length(GTel)),
  ",\"sol_f2_1_counterexample\":{\"P_order\":", String(Size(Pprod)),
  ",\"H_order\":", String(Size(Hctr)),
  ",\"index_P_H\":", String(idxPH),
  ",\"M\":", String(Mctr),
  ",\"N_P_H_eq_H\":", JB(NPH),
  ",\"X_transitive_on_P_over_H\":", JB(transCtr), "}",
  ",\"fail_closed\":true",
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"",
  ",\"input_doc_sha256\":\"", inputMdSha256, "\"",
  ",\"input_doc_path\":\"docs/week4-BFC攻略_opus_v1.md\"",
  ",\"node_counterpart_sha256\":\"", nodeCertSha256, "\"",
  ",\"node_counterpart_path\":\"search/week4-bfc-antecedents.mjs\"}",
  ",\"elapsed_cpu_ms\":", String(GAPLIB_ElapsedMs()),
  "}"
);;
WriteFile("certificates/bfc/bfc-antecedents.json", cert);;
Print("Certificate written: certificates/bfc/bfc-antecedents.json\n");
Print("Elapsed CPU ms: ", GAPLIB_ElapsedMs(), "\n");
