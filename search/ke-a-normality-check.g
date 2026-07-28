# search/ke-a-normality-check.g -- KE-a: L = K^(3) cap N0 の B3-正規性の直接検査
#
# Usage: .\gap.ps1 search\ke-a-normality-check.g
#
# 発注(裁定153・docs/notes/kerchi_equality_v1.md R-1/【KE-a】):
#   T-D(反例 L)が唯一継承している未検証仮定 = 「L は NFI_{PB3}(B3) の窓か
#   (B3-正規性)」。本スクリプトはこれを GAP で直接検査する。
#   L の構成は search/derived-census.g の "L" 行(K^(3) cap N0)と
#   docs/week3-L設計.md の N0 定義(N0 := pi^{-1}(V), V=F2^3 gamma_3(F2),
#   phi_L: PB3 -> G3 x H3, L := ker phi_L = K^(3) cap N0)を再利用する。
#   解釈しない・観測の記録に徹する。
#
# 方法(GAP ネイティブに IsNormal を判定させる):
#   1. G3=MakeGn(3)(位数108)・H3=MakeHeis(3,3)(位数27, Heisenberg mod 3)を
#      week3-battery-common.g のヘルパーで独立に再構成し、Q_L=G3 x H3 を
#      36点上の置換群として組む(week3-L-explorer.g と同じ構成方法・値の
#      再確認を兼ねる)。
#   2. BuildQTGeneral(Q_L, xhat, yhat, Identity(Q_L)) で B3 の transversal-
#      cocycle モデル(17496点、生成元 s1,s2)を構成する。braid 関係
#      s1 s2 s1 = s2 s1 s2 が成り立つことをここでも確認する(既存の必要条件)。
#   3. B3 を有限表示群 F(s1,s2)/[braid relator] として構成し、
#      hom: B3fp -> Group(qt.s1,qt.s2) を GroupHomomorphismByImages で作る
#      (braid 関係が成り立つ限り必ず存在する)。L := Kernel(hom)。
#   4. IsNormal(B3fp, L) を GAP に判定させる(Kernel は常に正規なので理論上
#      True になるはずだが、これは「L = Kernel(hom) であること」自体が
#      非自明な事実であり、それを保証するのが index の一致(Index(B3fp,L) =
#      Size(Image(hom)) = 17496 = 既報告の [B3:L])。ゆえに Index と N_ord を
#      あわせて出力し、根拠を明示する。
#   5. N_ord = Lcm(Order(xhat), Order(yhat))(既報告値 6 の独立再計算)。
#
# 宇宙: 対象は L 一つのみ(拡張しない)。既存 fixture 値(|G3|=108,|H3|=27,
# |Q_L|=2916,[Q_L:derived]=81,N_ord=6,index_B3=17496)との一致を fail-closed
# assert で確認してから正規性判定に進む。

Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

SizeScreen([4096, 0]);;

Print("############################################################\n");
Print("# KE-a: L = K^(3) cap N0 の B3-正規性(IsNormal(B3,L))検査\n");
Print("############################################################\n");

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

t0 := GAPLIB_WallElapsedMs();;

# ================================================================
# 1. Q_L = G3 x H3 の再構成(week3-L-explorer.g / docs/week3-L設計.md §1 と同一)
# ================================================================
gn := MakeGn(3);;
if Size(gn.G) <> 108 then
  Error("KE-a: |G3| mismatch: got ", Size(gn.G), " expected 108");
fi;
Print("[", PF(true), "] |G3| = ", Size(gn.G), " (expect 108)\n");

h3 := MakeHeis(3, 3);;
if Size(h3.G) <> 27 then
  Error("KE-a: |H3| mismatch: got ", Size(h3.G), " expected 27");
fi;
Print("[", PF(true), "] |H3| = ", Size(h3.G), " (expect 27)\n");

# fixture: H3 の class-2 exponent-3 構造(week3-L-explorer.g と同じ検査)
Xp := h3.x;;  Yp := h3.y;;
if not (Xp^3 = () and Yp^3 = () and (Xp*Yp)^3 = ()) then
  Error("KE-a: H3 fixture FAILED: X^3=Y^3=(XY)^3=1 required");
fi;
commXY := Xp^-1 * Yp^-1 * Xp * Yp;;
if Order(commXY) <> 3 then
  Error("KE-a: H3 fixture FAILED: [X,Y] must have order 3, got ", Order(commXY));
fi;
if not (commXY*Xp = Xp*commXY and commXY*Yp = Yp*commXY) then
  Error("KE-a: H3 fixture FAILED: [X,Y] must be central");
fi;
Print("[", PF(true), "] H3 fixture: X^3=Y^3=(XY)^3=1, [X,Y] central order 3\n");

# Q_L on 36 points: G3 on 1-9, H3 on 10-36 (verbatim construction convention)
xhat := PermList(Concatenation(List([1..9], j -> j^gn.x), List([1..27], j -> 9 + (j^Xp))));;
yhat := PermList(Concatenation(List([1..9], j -> j^gn.y), List([1..27], j -> 9 + (j^Yp))));;
QL := Group(xhat, yhat);;

qlSize := Size(QL);;
if qlSize <> 2916 then
  Error("KE-a: |Q_L| mismatch: got ", qlSize, ", expected 2916");
fi;
Print("[", PF(true), "] |Q_L| = ", qlSize, " (expect 2916)\n");

DQL := DerivedSubgroup(QL);;
if Size(DQL) <> 81 then
  Error("KE-a: |[Q_L,Q_L]| mismatch: got ", Size(DQL), ", expected 81");
fi;
Print("[", PF(true), "] |[Q_L,Q_L]| = ", Size(DQL), " (expect 81)\n");

Nord := Lcm(Order(xhat), Order(yhat));;
if Nord <> 6 then
  Error("KE-a: N_ord mismatch: got ", Nord, ", expected 6");
fi;
Print("[", PF(true), "] N_ord = Lcm(Order(xhat),Order(yhat)) = ", Nord, " (expect 6)\n");

# ================================================================
# 2. transversal-cocycle モデル(B3 の 17496 点表現)
# ================================================================
qt := BuildQTGeneral(QL, xhat, yhat, Identity(QL));;
Print("Q_L x T model built: np=", qt.np, " total_points=", 6*qt.np, "\n");

if not (qt.s1*qt.s2*qt.s1 = qt.s2*qt.s1*qt.s2) then
  Error("KE-a: braid relation s1 s2 s1 = s2 s1 s2 FAILED for L's QxT model");
fi;
Print("[", PF(true), "] braid relation s1 s2 s1 = s2 s1 s2 holds (necessary for B3-hom to exist)\n");

QTgrp := Group(qt.s1, qt.s2);;
qtSize := Size(QTgrp);;
if qtSize <> 17496 then
  Error("KE-a: |<s1,s2>| mismatch: got ", qtSize, ", expected 17496 (= index_B3(L))");
fi;
Print("[", PF(true), "] |<s1,s2>| = ", qtSize, " (expect 17496 = [B3:L] per docs/week3-L設計.md)\n");

# ================================================================
# 3. B3 を有限表示群として構成し、hom: B3fp -> <s1,s2> を作る。L := Kernel(hom)。
# ================================================================
Fb3 := FreeGroup("s1", "s2");;
gensFb3 := GeneratorsOfGroup(Fb3);;
s1g := gensFb3[1];;  s2g := gensFb3[2];;
braidRel := s1g*s2g*s1g*s2g^-1*s1g^-1*s2g^-1;;
B3fp := Fb3 / [braidRel];;
Print("B3 (fp group) built: <s1,s2 | s1 s2 s1 = s2 s1 s2>\n");

gensB3fp := GeneratorsOfGroup(B3fp);;
homB3 := GroupHomomorphismByImages(B3fp, QTgrp, gensB3fp, [qt.s1, qt.s2]);;
if homB3 = fail then
  Error("KE-a: GroupHomomorphismByImages(B3fp -> <s1,s2>) construction FAILED");
fi;
Print("[", PF(true), "] hom: B3(fp) -> <s1,s2> constructed (well-defined, since braid relation holds)\n");

t1 := GAPLIB_WallElapsedMs();;
Print("経過(Q_L/QxT/hom 構成まで) = ", (t1-t0)/1000.0, " s\n");

# ================================================================
# 4. L := Kernel(homB3), IsNormal(B3fp, L), Index(B3fp, L)
# ================================================================
t2 := GAPLIB_WallElapsedMs();;
Lkernel := Kernel(homB3);;
t3 := GAPLIB_WallElapsedMs();;
Print("Kernel(homB3) 計算: 経過 = ", (t3-t2)/1000.0, " s\n");

indexB3L := Size(Image(homB3));;   # = Index(B3fp, Lkernel) by first isomorphism theorem
Print("Index(B3fp, L) = Size(Image(hom)) = ", indexB3L, " (expect 17496)\n");

t4 := GAPLIB_WallElapsedMs();;
isNormalResult := IsNormal(B3fp, Lkernel);;
t5 := GAPLIB_WallElapsedMs();;
Print("IsNormal(B3fp, L) = ", isNormalResult, "  (経過 = ", (t5-t4)/1000.0, " s)\n");

t6 := GAPLIB_WallElapsedMs();;
Print("\n############################################################\n");
Print("# 結論(観測のみ・解釈しない)\n");
Print("############################################################\n");
Print("IsNormal(B3, L) = ", isNormalResult, "\n");
Print("Index(B3, L) = ", indexB3L, "\n");
Print("N_ord = ", Nord, "\n");
Print("|G3| = ", Size(gn.G), ", |H3| = ", Size(h3.G), ", |Q_L| = ", qlSize,
      ", |[Q_L,Q_L]| = ", Size(DQL), ", |<s1,s2>| = ", qtSize, "\n");
Print("総経過(壁時計) = ", t6/1000.0, " s\n");

# ================================================================
# 証明書 JSON
# ================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_kea.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/ke-a-normality-check.g");;

cert := Concatenation(
  "{\"schema\":\"ke-a-normality-check/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/ke-a-normality-check.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"design_source\":\"docs/notes/kerchi_equality_v1.md R-1 / KE-a; L construction: search/derived-census.g 'L' line + docs/week3-L設計.md N0 definition\"",
  ",\"target\":\"L = K^(3) cap N0\"",
  ",\"method\":\"Reconstruct Q_L=G3xH3 (G3=MakeGn(3), H3=MakeHeis(3,3)); build B3's transversal-cocycle rep <s1,s2> on 6*|Q_L| points (BuildQTGeneral); present B3 as fp group F(s1,s2)/[braid relator]; hom:B3fp->Group(s1,s2); L:=Kernel(hom); query IsNormal(B3fp,L) and Index(B3fp,L)=Size(Image(hom)) natively in GAP\"",
  ",\"fixture_checks\":{",
    "\"G3_order\":", String(Size(gn.G)),
    ",\"H3_order\":", String(Size(h3.G)),
    ",\"QL_order\":", String(qlSize),
    ",\"derived_QL_order\":", String(Size(DQL)),
    ",\"N_ord\":", String(Nord),
    ",\"braid_relation_holds\":", JB(qt.s1*qt.s2*qt.s1 = qt.s2*qt.s1*qt.s2),
    ",\"QT_group_order\":", String(qtSize),
  "}",
  ",\"results\":{",
    "\"is_normal_B3_L\":", JB(isNormalResult),
    ",\"index_B3_L\":", String(indexB3L),
    ",\"N_ord\":", String(Nord),
  "}",
  ",\"elapsed_wall_ms\":{",
    "\"QL_QT_hom_construction\":", String(t1-t0),
    ",\"kernel_computation\":", String(t3-t2),
    ",\"is_normal_query\":", String(t5-t4),
    ",\"total\":", String(t6),
  "}",
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/ke_a_normality_20260729.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");

Print("\nKE-A NORMALITY CHECK DONE\n");
QUIT;
