#############################################################################
## search/_probe_epsilon_bits.g -- ε の「持ち上げ位数」ビットを層ごとに直接測る
##
## 【LG-1】用。Q_2 = Syl_2(Q) の各基底元 u に対し
##   P(u) := [ u の持ち上げが tilde G = C_G(S)/A で位数 ord(u) を取れないか ] ∈ F_2
## を、u の shadow 層(m = (u-1)/2)を走査して直接判定する。
## さらに A20 (Q_2 = C_4 x C_2 非巡回) では交差ビット
##   c(a,b) := [ 持ち上げが tilde G で非可換か ]
## を witness 対で直接確認する。
##
## 入力: EPS_MS := [ [m, 期待位数], ... ](driver が定義)
## 出力: 標準出力 + search/certs/.epsbits_<id>.json
#############################################################################
SizeScreen([4096, 0]);;
JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");
Read("search/gaplib_common.g");
Read("search/w62-windows.g");
wspec := W62_GetWindow();;
Read(Concatenation("search/certs/.w62_shadows_", wspec.id, ".g"));
W := W62_MakeW(wspec);;
corr := Set(List(W62_SHADOWS, s -> [s[1], s[2]]));;
gi := GroupOfShadows(W, corr);;
G := gi.G;; K := gi.ker;; regs := gi.regs;;
Nord := W.Nord;;
D8 := SylowSubgroup(K, 2);;
oddp := Filtered(PrimeDivisors(Size(K)), p -> p <> 2);;
A := Subgroup(K, Concatenation(List(oddp, p -> GeneratorsOfGroup(SylowSubgroup(K, p)))));;
CG := Centralizer(G, D8);;
hom := NaturalHomomorphismByNormalSubgroup(G, A);;   # A は G で正規
Gt := Image(hom);;
CGt := Image(hom, CG);;                              # = tilde G = C_G(S)/A
Print("=== eps-bits: ", W62_ID, "  N_ord = ", Nord, " ===\n");
Print("  |tilde G| = ", Size(CGt), " = ", StructureDescription(CGt),
      "   abelian? ", IsAbelian(CGt), "  (非可換なら交差ビット c ≠ 0)\n");

items := [];;
wits := [];;
for spec in EPS_MS do
  m := spec[1];  expOrd := spec[2];
  u := (2*m+1) mod (2*Nord);
  idx := Filtered([1 .. Length(corr)], i -> corr[i][1] = m);
  # この層のうち D8 を中心化するもの
  cen := Filtered(idx, i -> IsTrivial(CommutatorSubgroup(Group(regs[i]), D8)));
  # tilde G = C_G(S)/A における位数
  ords := List(cen, i -> Order(Image(hom, regs[i])));
  good := Filtered([1..Length(cen)], j -> ords[j] = expOrd);
  Print("\n  u = ", u, " (m = ", m, ")   ord_Q(u) = ", expOrd, "\n");
  Print("    層の大きさ = ", Length(idx), "   うち D8 を中心化 = ", Length(cen), "\n");
  Print("    tilde G での持ち上げ位数の分布 = ", Collected(ords), "\n");
  Print("    **P(u) = ", Length(good) = 0, "**  (false = 同位数持ち上げあり = ビット 0)",
        "   同位数持ち上げ数 = ", Length(good), "\n");
  if Length(good) > 0 then
    i0 := cen[good[1]];
    Print("    witness: m = ", corr[i0][1], "  ord_G = ", Order(regs[i0]),
          "\n      f = ", corr[i0][2], "\n");
    Add(wits, regs[i0]);
  fi;
  Add(items, Concatenation("{\"u\":", String(u), ",\"m\":", String(m),
    ",\"ord_Q\":", String(expOrd),
    ",\"layer_size\":", String(Length(idx)),
    ",\"centralizing\":", String(Length(cen)),
    ",\"same_order_lifts\":", String(Length(good)),
    ",\"P_bit\":", String(Length(good) = 0), "}"));
od;

crossBit := "n/a";;
if Length(wits) >= 2 then
  crossBit := String(not IsOne(Image(hom, Comm(wits[1], wits[2]))));
  Print("\n  交差ビット c(witness1, witness2) = ", crossBit,
        "  (false = 可換 = ビット 0)\n");
fi;

js := Concatenation("{\"schema\":\"eps-bits/v1\"",
  ",\"window_id\":", JStr(wspec.id),
  ",\"N_ord\":", String(Nord),
  ",\"tildeG_struct\":", JStr(StructureDescription(CGt)),
  ",\"tildeG_abelian\":", JB(IsAbelian(CGt)),
  ",\"layers\":", JArr(items),
  ",\"cross_bit_nonzero\":", JStr(crossBit), "}");;
WriteFile(Concatenation("search/certs/.epsbits_", wspec.id, ".json"), js);;
Print("\nwrote search/certs/.epsbits_", wspec.id, ".json\nEPSBITS_DONE\n");
QUIT;
