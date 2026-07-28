## ss_sp45_shard0b.g -- shard 0 再走(構造定数は ctbllib の S4(5) 表で計算)
## shard0 は CharacterTable(G) の Irr 計算で落ちたため、Irr を持つ ATLAS 表を使う。
## 表は群と独立に (位数, 中心化群位数, 2 乗写像) で目標類を同定する。
SizeScreen([4096,0]);;
Read("search/gaplib_common.g");
t0 := GAPLIB_WallElapsedMs();;
Print("############ ss_sp45 shard0b: 構造定数(ATLAS 表)############\n");

tbl := CharacterTable("S4(5)");;
if tbl = fail then Error("CharacterTable(\"S4(5)\") not available"); fi;
Print("表 = ", Identifier(tbl), "   |G| = ", Size(tbl), " (期待 4680000: ",
      Size(tbl) = 4680000, ")\n");
ords := OrdersClassRepresentatives(tbl);;
cens := SizesCentralizers(tbl);;
pm2  := PowerMap(tbl, 2);;
nc := Length(ords);;
Print("類の個数 = ", nc, " (群側 shard0 の 34 と一致? ", nc = 34, ")\n");

X6 := Filtered([1..nc], i -> ords[i] = 6 and cens[i] = 360);;
U12 := Filtered([1..nc], i -> ords[i] = 12 and pm2[i] in X6);;
AA := Filtered([1..nc], i -> ords[i] = 2);;
BB := Filtered([1..nc], i -> ords[i] = 3);;
Print("目標類 X (ord 6, |C|=360) = ", X6, "\n");
Print("u 源 U (ord 12, 2乗 in X) = ", U12, "  |C| = ", List(U12,i->cens[i]), "\n");
Print("対合類 A = ", AA, " |C| = ", List(AA,i->cens[i]), "\n");
Print("位数 3 類 B = ", BB, " |C| = ", List(BB,i->cens[i]), "\n");

Print("\n--- 構造定数 c(B, A, U) = #{(p,q): p in B, q in A, p q = u_fixed in U} ---\n");
total := 0;;  live := [];;
for U in U12 do
  for B in BB do
    for A in AA do
      cc := ClassMultiplicationCoefficient(tbl, B, A, U);
      Print("   U=", U, "(", ords[U], ") B=", B, "(", ords[B], ") A=", A, "(", ords[A],
            ")   c = ", cc, "\n");
      total := total + cc;
      if cc > 0 then Add(live, [U,B,A,cc]); fi;
    od;
  od;
od;
Print("\n構造定数の総和 = ", total, "\n");
if total = 0 then
  Print("**類レベル判定: 因数分解 u = p*q (p 位数3, q 位数2) が存在しない**\n");
  Print("**==> 生成条件を課すまでもなく W-D-Sp45-6a は死亡**\n");
else
  Print("**類レベル判定: 因数分解は存在(live = ", live, ")。生成条件を shard 1 で検査**\n");
fi;

# 参考: 対合類 x 位数3類 の積が到達しうる位数 12 の類(全体像)
Print("\n--- 参考: すべての位数 12 類への到達可否 ---\n");
for U in Filtered([1..nc], i -> ords[i] = 12) do
  s := 0;
  for B in BB do for A in AA do s := s + ClassMultiplicationCoefficient(tbl,B,A,U); od; od;
  Print("   U=", U, " |C|=", cens[U], " 2乗先=", pm2[U], "(|C|=", cens[pm2[U]],
        ")  sum c = ", s, "\n");
od;

Print("\n経過 = ", (GAPLIB_WallElapsedMs()-t0)/1000.0, " s\n");
Print("SS_SP45_SHARD0B_DONE\n");
QUIT;
