#############################################################################
## search/probe/wac_v1/nf972_sourcemap_b_run.g
## NF-972 source map B(裁定434・凍結仕様 docs/notes/nf972_freeze_v1.md 逐条)。
##
## 担当範囲: source map B のみ -- 屋根 M = K^(9) cap N_S4 上の「直接悉皆」で
## 得た各 shadow [m,f] を、本 driver が独立に評価する q9,q4 で凍結 NF tuple
## (m0, can9(q9(f)), can4(q4(f))) へ写す。source map A(組立側)は別の係が
## 独立実装中であり、本 driver は A の実装・中間表現・normalizer helper を
## 一切参照しない(共有は凍結仕様の schema のみ)。
##
## 列挙部の再利用について(凍結仕様の許可範囲): search/probe/wac_v1/
## ihnec_r4b_run.g の「屋根での直接悉皆」という設計(Elements(DerivedSubgroup(G))
## の直接列挙 + hexagon 判定式)は再現するが、判定関数 ScanRoofHexagon 自体は
## 再利用せず、本 driver が独自に NF972HexagonOK として再実装する(数学的判定式
## は同一 -- theta/tau・hex310・hex311・生成条件 -- だがコードは別)。NF 化
## (q9/q4 の評価・can9/can4・tuple の canonical serialization)は完全に自前実装
## であり、A 側の正規化コードとは一切共有しない。
##
## can9/can4 の設計判断(凍結仕様 SS1 の「r^a s^ε の指数 tuple」を具体化する
## にあたっての実装係の解釈 -- ops/express/20260804_implementer_nf972b_can9設計判断.md
## に速達済み・司令塔/Sol の確認は未了):
##   G9 = MakeGn(9).G は Sym(27) の部分群で、27点を9点x3ブロックに分けると
##   MakeGn の構成(disjoint support の積: x = tr(r,1)*tr(s,2)*tr(s,3) 等)から
##   各ブロックへの制限は必ず D_9 = <r,s>(位数18)に入る。よって G9 は
##   D_9 x D_9 x D_9(位数5832)の部分群に埋め込め(2916 = 5832/2 と整合)、
##   "指数 tuple"(複数形)・"成分順固定" の文言と符合する。
##   採用: can9(g) = [(a1,eps1),(a2,eps2),(a3,eps3)](ブロック1,2,3 固定順の
##   D_9 正規形)。can4(h) = h の 9点上の one-line image(単純・ブロック不要)。
##
## 設計からの変更点(先に申告する): 分離 fixture(仕様SS4)は当初「本走前」に
## 独立の小サンプルで検査する設計だったが、(a) 本走そのものが軽量(12 m値
## 全体で概ね1分未満)であること、(b) 単一m値のみからサンプルを取ると
## fixture3(mの法の誤り)が構造的に不発になる(m=0のみだと0 mod 9=0=m自身
## で差が出ない)ことが判明したため、実データ resM.shadows から複数m値に
## またがるサンプルを取り、fixture 検査を「本走の直後・cert 書き出しの前」
## に行う設計へ変更した。列挙そのものは同一であり、fixture が判定するのは
## serialization/m0計算方法の食い違いなので、この順序変更は識別力判定の
## 妥当性そのものには影響しない(fail-closed gate は変わらず cert 書き出し
## 前に立っている)。また fixture2(片側 generator swap)は当初
## can9 内部の r,s 役割入替で実装しようとしたが、DerivedSubgroup(GM) の元は
## 構成上すべてのブロックで eps=0(純回転)にしかならない(D_9の交換子部分群
## は回転部分群 <r> のため)ことが判明し、r,s 入替では eps=0 のとき常に
## r^a s^0 = s^0 r^a となり不発が構造的に確定してしまう。よって fixture2 は
## 「q4 側(S4窓)の生成元対応そのものを入替えた別の屋根群 GM2」を実際に
## 構築し直す方式に変更した(q9側は不変・q4側のみの片側入替)。
##
## 宇宙の事前登録: 対象は屋根 M(K^(9) cap N_S4)の1点のみ。既存 R4b と同じ
## 窓・m 範囲(charmingSet_M・12値)。範囲の拡大縮小はしない。
##
## 実行: .\gap.ps1 search\probe\wac_v1\nf972_sourcemap_b_run.g
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

ComputeSha256FileB := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_nf972b_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then
    Error("nf972_sourcemap_b_run: ComputeSha256FileB: sha256sum did not return a hash line for ", relpath);
  fi;
  return line{[1 .. 64]};
end;;

ComputeSha256OfString := function(s)
  local tmp, f, line;
  tmp := "search/.tmp_nf972b_strsha.txt";
  WriteFile(tmp, s);
  Exec(Concatenation("sha256sum \"", tmp, "\" > \"", tmp, ".out\""));
  f := InputTextFile(Concatenation(tmp, ".out"));  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\" \"", tmp, ".out\""));
  if line = fail or Length(line) < 64 then
    Error("nf972_sourcemap_b_run: ComputeSha256OfString: sha256sum failed");
  fi;
  return line{[1 .. 64]};
end;;

#############################################################################
## ---- 簡約 hexagon 判定式 ----
## 【2026-08-04 修正申告】初版は f*thetaf・y^m*f・tau2ymf*tauymf*ymf・
## f^-1*y^u*f という「plain な GAP `*`」で書いていたが、これは R4b
## (search/probe/wac_v1/ihnec_r4b_run.g の ScanRoofHexagon)や生成元評価の
## 基盤である AbstractProd(week3-battery-common.g・paper左右記法->GAPの
## 反転規約)と規約が食い違うバグだった。K9窓(dihedral tower構成)では
## 偶然結果に効かず(108/108が両規約で一致)、S4窓(PSL(2,8)・非可換単純群)
## では規約差が実際に効き、K9.v1.json/S4.v2.json の f_word を評価しての
## 逐語突合で発覚(K9は108/108一致もS4は6/54しか一致せず、原因を追跡)。
## 本版は R4b/AbstractProd と同じ規約(zElt=AbstractProd([x,y])^-1・
## ymf=AbstractProd([y^m,f])・hex311=AbstractProd([tau2ymf,tauymf,ymf])・
## genB=AbstractProd([f^-1,y^u,f]))に統一する。数学的判定式は R4b と同一
## だがコードは別実装(独立性は維持)。
#############################################################################
# BuildQrecWithHoms: qrec(x,y,G)にthetaHom,tauHomを1回だけ付加したものを返す
# (NF972HexagonOKをcandidate毎に呼ぶ際の再構築コストを避ける共有ヘルパ)。
BuildQrecWithHoms := function(x, y, G)
  local zElt, thetaHom, tauHom;
  zElt := AbstractProd([x, y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [x, y], [y, x]);
  tauHom := GroupHomomorphismByImages(G, G, [x, y], [y, zElt]);
  if thetaHom = fail or tauHom = fail then
    Error("BuildQrecWithHoms: theta/tau homomorphism construction failed");
  fi;
  return rec(x := x, y := y, G := G, thetaHom := thetaHom, tauHom := tauHom);
end;;

## qrec は x,y,G に加え BuildQrecWithHoms が1回だけ構築した thetaHom,tauHom
## を持つ(candidate毎の再構築は極めて重い -- M窓は |derived subgroup|=367416
## x 12 m値 = 4,408,992 回呼ばれるため)。
NF972HexagonOK := function(qrec, m, f)
  local G, thetaf, hex310, ymf, tauymf, tau2ymf, hex311, u, genA, genB, surj;
  G := qrec.G;
  thetaf := Image(qrec.thetaHom, f);
  hex310 := (AbstractProd([f, thetaf]) = Identity(G));
  if not hex310 then return false; fi;
  ymf := AbstractProd([qrec.y^m, f]);
  tauymf := Image(qrec.tauHom, ymf);
  tau2ymf := Image(qrec.tauHom, tauymf);
  hex311 := (AbstractProd([tau2ymf, tauymf, ymf]) = Identity(G));
  if not hex311 then return false; fi;
  u := 2*m + 1;
  genA := qrec.x^u;
  genB := AbstractProd([f^-1, qrec.y^u, f]);
  surj := (Size(Group(genA, genB)) = Size(G));
  return surj;
end;;

NF972ScanRoof := function(qrecIn, charmingSet)
  local G, D, Delts, shadows, m, i, f, qrec;
  G := qrecIn.G;
  qrec := BuildQrecWithHoms(qrecIn.x, qrecIn.y, G);
  D := DerivedSubgroup(G);
  Delts := Elements(D);
  shadows := [];
  for m in charmingSet do
    for i in [1 .. Length(Delts)] do
      f := Delts[i];
      if NF972HexagonOK(qrec, m, f) then
        Add(shadows, rec(m := m, f := f));
      fi;
    od;
  od;
  return rec(shadows := shadows, derived_order := Length(Delts));
end;;

CharmingSetOfB := function(nOrd)
  return Filtered([0 .. nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);
end;;

#############################################################################
## ---- 窓構成(K9・S4・M) ----
#############################################################################
Print("=== 窓構成: G9 = MakeGn(9) ===\n");
g9 := MakeGn(9);;
K9sz := Size(g9.G);;
K9ord := Lcm(Order(g9.x), Order(g9.y));;
if K9sz <> 2916 or K9ord <> 18 then
  Error("nf972_sourcemap_b_run: K9 window construction mismatch");
fi;
K9charm := CharmingSetOfB(K9ord);;
Print("  |G9|=", K9sz, " K9_ord=", K9ord, " charming(K9)=", K9charm, "\n");

Print("=== 窓構成: P = PSL(2,8) ===\n");
CheckGF8();;
Smat := MakeMatGF8(1,0,1,1);;
Tmat := MakeMatGF8(4,3,1,5);;
Sperm := MatToPermGF8(Smat);;
Tperm := MatToPermGF8(Tmat);;
wPerm := Sperm * Tperm^-1;;
Xperm := wPerm^2;;
Yperm := Sperm^-1 * Xperm * Sperm;;
Pgrp := Group(Xperm, Yperm);;
Psz := Size(Pgrp);;
Pord := Lcm(Order(Xperm), Order(Yperm));;
if Psz <> 504 or Pord <> 9 then
  Error("nf972_sourcemap_b_run: S4/PSL(2,8) window construction mismatch");
fi;
S4charm := CharmingSetOfB(Pord);;
if S4charm <> [0,2,3,5,6,8] then
  Error("nf972_sourcemap_b_run: S4 charming set mismatch");
fi;
Print("  |P|=", Psz, " N_S4_ord=", Pord, " charming(S4)=", S4charm, "\n");

Print("=== 屋根 M := K9 cap N_S4 (block-diagonal, 27+9=36 points) ===\n");
ShiftPermB := function(p, offset, size)
  local l, j;
  l := [1 .. offset+size];
  for j in [1 .. size] do l[offset+j] := offset + (j^p); od;
  return PermList(l);
end;;
DirectSumPermB := function(p1, deg1, p2, deg2)
  return p1 * ShiftPermB(p2, deg1, deg2);
end;;
XM := DirectSumPermB(g9.x, 27, Xperm, 9);;
YM := DirectSumPermB(g9.y, 27, Yperm, 9);;
GM := Group(XM, YM);;
Mord := Lcm(Order(XM), Order(YM));;
if Size(GM) <> 2916*504 or Mord <> 18 then
  Error("nf972_sourcemap_b_run: roof M construction mismatch -- |GM|=", Size(GM),
        " M_ord=", Mord);
fi;
Mcharm := CharmingSetOfB(Mord);;
Print("  |GM|=", Size(GM), " M_ord=", Mord, " charming(M)=", Mcharm, " (|.|=", Length(Mcharm), ")\n");

# fixture(2)用の別屋根: q4側(S4窓)の生成元対応だけ入替えた埋め込み
# (X<->Yの対応を入替: q9側=g9.x/g9.yは不変・q4側だけXperm<->Ypermを交換)。
XM2 := DirectSumPermB(g9.x, 27, Yperm, 9);;
YM2 := DirectSumPermB(g9.y, 27, Xperm, 9);;
GM2 := Group(XM2, YM2);;

#############################################################################
## ---- 自己検査アンカー(独自コードでの108/54再現。R4bのcert値は読まない) ----
#############################################################################
Print("\n=== 自己検査アンカー: NF972ScanRoof(K9単体) ===\n");
resK9anchor := NF972ScanRoof(rec(x := g9.x, y := g9.y, G := g9.G), K9charm);;
Print("  shadow_total=", Length(resK9anchor.shadows), " (expect 108)\n");
if Length(resK9anchor.shadows) <> 108 then
  Error("nf972_sourcemap_b_run: ANCHOR FAILURE K9-alone = ", Length(resK9anchor.shadows), " <> 108");
fi;

Print("=== 自己検査アンカー: NF972ScanRoof(S4単体) ===\n");
resS4anchor := NF972ScanRoof(rec(x := Xperm, y := Yperm, G := Pgrp), S4charm);;
Print("  shadow_total=", Length(resS4anchor.shadows), " (expect 54)\n");
if Length(resS4anchor.shadows) <> 54 then
  Error("nf972_sourcemap_b_run: ANCHOR FAILURE S4-alone = ", Length(resS4anchor.shadows), " <> 54");
fi;

#############################################################################
## ---- q9,q4 の評価と can9,can4(自前 serialization) ----
##  q9(f): f in GM(36点)の 1..27 点への制限を Sym(27) 元として抽出。
##  can9: q9(f) を 9点x3ブロックに分け、各ブロックを D_9 の (a,eps) 正規形
##        (r^a s^eps = block_i)へ分解。r,s は MakeDn(9)。固定順(1,2,3)。
##  q4(f): f の 28..36 点への制限を 1..9 にシフトして Sym(9) 元として抽出。
##  can4: q4(f) の 9点上の one-line image。
#############################################################################
BlockRestrict := function(perm, offset, size)
  local l, j;
  l := [];
  for j in [1 .. size] do l[j] := (j+offset)^perm - offset; od;
  return PermList(l);
end;;

rs9 := MakeDn(9);;
rGen := rs9[1];;  sGen := rs9[2];;
D9Table := [];;  # D9Table[idx] = rec(a:=a, eps:=eps, perm:=r^a*s^eps), idx 1..18
BuildD9Table := function()
  local a, eps, tab, cand;
  tab := [];
  for a in [0 .. 8] do
    for eps in [0 .. 1] do
      cand := rGen^a * sGen^eps;
      Add(tab, rec(a := a, eps := eps, perm := cand));
    od;
  od;
  return tab;
end;;
D9Table := BuildD9Table();;
if Length(D9Table) <> 18 then Error("nf972_sourcemap_b_run: D9Table size <> 18"); fi;

# D9Decompose: 与えられた9点上の順列(D_9=<r,s>の元であることを前提)を
# (a,eps)へ分解する。マッチしなければ Error(fail-closed -- ブロックがD_9に
# 属さない=q9/G9構成の前提が崩れている、静かに補正しない)。
D9Decompose := function(perm)
  local i, row;
  for i in [1 .. Length(D9Table)] do
    row := D9Table[i];
    if row.perm = perm then return [row.a, row.eps]; fi;
  od;
  Error("nf972_sourcemap_b_run: D9Decompose: block permutation not in <r,s> -- ", perm);
end;;

# Can9OfPerm27: 27点上の順列(GM元のq9射影像)を3ブロックのD9座標tupleへ。
Can9OfPerm27 := function(perm27)
  local out, blk, i, p;
  out := [];
  for i in [1 .. 3] do
    blk := BlockRestrict(perm27, (i-1)*9, 9);
    p := D9Decompose(blk);
    Add(out, p[1]);  Add(out, p[2]);
  od;
  return out;
end;;

Can4OfPerm9 := function(perm9)
  local l, j;
  l := [];
  for j in [1 .. 9] do l[j] := j^perm9; od;
  return l;
end;;

# NFTupleOf: shadow rec(m,f)(f in 36点の屋根群の元) -> rec(m0, can9, can4)
# invertF(既定false): fixture(1)用 -- true のとき f の代わりに f^-1 を使う。
# wrongMod(既定0): fixture(3)用 -- 0以外なら m0 を m mod wrongMod として
#   誤った法で計算する(0なら正しくm自身=M_ordの範囲内の値をそのまま使う)。
NFTupleOf := function(shadowRec, invertF, wrongMod)
  local f, m0, p27, q4perm, can9v, can4v;
  if invertF then f := shadowRec.f^-1; else f := shadowRec.f; fi;
  if wrongMod = 0 then
    m0 := shadowRec.m;
  else
    m0 := shadowRec.m mod wrongMod;
  fi;
  p27 := BlockRestrict(f, 0, 27);
  can9v := Can9OfPerm27(p27);
  q4perm := BlockRestrict(f, 27, 9);
  can4v := Can4OfPerm9(q4perm);
  return rec(m0 := m0, can9 := can9v, can4 := can4v);
end;;

NFTupleSerialize := function(t)
  return Concatenation("(", String(t.m0), ";",
    JoinC(List(t.can9, String), ","), ";",
    JoinC(List(t.can4, String), ","), ")");
end;;

#############################################################################
## ---- v1.1追補(裁定442・§6): 辞書の自己検査(義務・fail-closed) ----
## can9 = K9.v1.json の f_triple 欄の座標規約そのもの・can4 = S4.v2.json の
## witness(=hexagon通過shadowの実体)の点ラベルそのもの、へ統一する。
## 「辞書」= 自構成の marked 生成元像(g9.x,g9.y / Xperm,Yperm)と cert 側の
## marked 生成元像を結ぶ同型。cert 側の生成元は同じ g9.x,g9.y(K9.v1.json は
## search/suite-wp2-explorer.gのMakeGn(9)由来 -- week3-battery-common.gと
## 同一定義を共有インフラとして確認済み)・同じ Xperm,Yperm(S4.v2.jsonは
## search/week3-psl-S4.g+week3-psl-common.gのRunPSLWindow由来 -- 同じ
## S,T行列・同じXperm,Yperm構成式を確認済み)である。よって生成元対応は
## 恒等(x<->x, y<->y)であり、辞書は「恒等」となる ------ ただし恒等だと
## 前提するのではなく、以下で cert の f_word を自分の g9.x/g9.y・
## Xperm/Yperm で評価し、自分の can9/can4 と逐語一致するかを機械検査する
## (罠#3遵守: marked factor map によるチェックであり部分群等号には依らない)。
##
## 【この過程で発見した実装バグ】当初この自己検査で K9 側は108/108一致した
## が S4 側は6/54しか一致しなかった。調査の結果、原因は座標系/markingでは
## なく NF972HexagonOK の乗算規約(ymf・hex311・genB・zElt)が R4b/
## AbstractProd規約と食い違うバグだったと判明(K9窓では偶然結果に効かず、
## S4窓=PSL(2,8)非可換単純群では実際に効いていた)。上のNF972HexagonOK/
## BuildQrecWithHomsは既にAbstractProd規約へ修正済み(このコメント直前の
## セクション参照)。修正後にこの自己検査を再実行し、以下でS4側も54/54へ
## 改善したことを確認する。
#############################################################################
# WordEval: f_word([[gen,exp],...]形式)をxg,ygの積として評価する
# (AbstractProdの反転規約 -- week3-battery-common.gのBFSWords/EnumerateReducedHexagon
# が生成するword(左からsym追加・nv:=g.gap*cur)と整合)。空語は単位元。
WordEval := function(fword, xg, yg)
  local items, pr, g;
  if Length(fword) = 0 then return xg^0; fi;
  items := [];
  for pr in fword do
    if pr[1] = "x" then g := xg; else g := yg; fi;
    Add(items, g^pr[2]);
  od;
  return AbstractProd(items);
end;;

# ParseS4PassingFWords: S4.v2.json の "generation_detail" 配列から
# pass:true の(m,f_word)のみを抽出する自前パーサ(A側の実装は参照しない
# -- cert JSON の生テキストのみから読む。ParseK3Shadows と同じ流儀の
# 手書き文字列スキャン)。
ParseS4PassingFWords := function(path)
  local content, stream, mk1, pos, sStart, mk2, sEnd, body, out, p, mPos, j,
        digitStr, mVal, fwMk, fwStart, depth, k, fwEnd, fwBody, passMk, passPos,
        passVal, items, ip, sym, expSign, expDigits, expVal;
  stream := InputTextFile(path);
  if stream = fail then Error("ParseS4PassingFWords: cannot open ", path); fi;
  content := ReadAll(stream);
  CloseStream(stream);
  mk1 := "\"generation_detail\":[";
  pos := FindPositionFrom(content, mk1, 1);
  if pos = fail then Error("ParseS4PassingFWords: generation_detail marker not found"); fi;
  sStart := pos + Length(mk1);
  mk2 := "],\"frobenius_zero\":";
  sEnd := FindPositionFrom(content, mk2, sStart);
  if sEnd = fail then Error("ParseS4PassingFWords: frobenius_zero boundary not found"); fi;
  body := content{[sStart .. sEnd-1]};
  out := [];
  p := 1;
  while true do
    mPos := FindPositionFrom(body, "\"m\":", p);
    if mPos = fail then break; fi;
    j := mPos + 4;
    digitStr := "";
    while j <= Length(body) and body[j] in "0123456789" do
      Append(digitStr, [body[j]]);  j := j+1;
    od;
    if Length(digitStr) = 0 then Error("ParseS4PassingFWords: empty m digit at ", mPos); fi;
    mVal := Int(digitStr);
    fwMk := "\"f_word\":[";
    fwStart := FindPositionFrom(body, fwMk, mPos);
    if fwStart = fail then Error("ParseS4PassingFWords: f_word marker not found after ", mPos); fi;
    # bracket-depth scan starting at the '[' itself to find the matching ']'
    k := fwStart + Length(fwMk) - 1;  # index of the opening '['
    depth := 0;  fwEnd := fail;
    while k <= Length(body) do
      if body[k] = '[' then depth := depth + 1;
      elif body[k] = ']' then
        depth := depth - 1;
        if depth = 0 then fwEnd := k; break; fi;
      fi;
      k := k + 1;
    od;
    if fwEnd = fail then Error("ParseS4PassingFWords: unbalanced f_word brackets at ", fwStart); fi;
    fwBody := body{[fwStart+Length(fwMk) .. fwEnd-1]};  # contents strictly inside outer [...]
    # parse items like "x",-1 or "y",1 separated by "],["
    items := [];
    ip := 1;
    while true do
      ip := FindPositionFrom(fwBody, "\"", ip);
      if ip = fail then break; fi;
      sym := fwBody[ip+1];
      ip := ip + 4;  # skip: opening quote(ip+0)+sym(ip+1)+closing quote(ip+2)+comma(ip+3) -> land on exponent
      expSign := 1;
      if ip <= Length(fwBody) and fwBody[ip] = '-' then expSign := -1; ip := ip+1; fi;
      expDigits := "";
      while ip <= Length(fwBody) and fwBody[ip] in "0123456789" do
        Append(expDigits, [fwBody[ip]]);  ip := ip+1;
      od;
      expVal := expSign * Int(expDigits);
      Add(items, [[sym], expVal]);
      ip := ip + 1;
    od;
    passMk := "\"pass\":";
    passPos := FindPositionFrom(body, passMk, fwEnd);
    if passPos = fail then Error("ParseS4PassingFWords: pass marker not found after ", fwEnd); fi;
    passVal := (body{[passPos+Length(passMk) .. passPos+Length(passMk)+3]} = "true");
    if passVal then
      Add(out, rec(m := mVal, fword := items));
    fi;
    p := passPos + Length(passMk);
  od;
  return out;
end;;

# ParseS4SettledWitness: S4.v2.json の "settled_detail" 配列(54件・全て
# settled:true)から (m, f_word, automorphism_witness置換) を抽出する自前
# パーサ。automorphism_witness は "()" や "(1,6)(3,5)..." のGAP順列リテラル
# そのものの文字列なので EvalString で直接 Sym(9) の元へ変換する(cert JSON
# は自分たちの生成物であり信頼できる入力 -- 罠#3: これは marked witness
# データそのものであり、部分群等号や自分の計算結果の使い回しではない)。
ParseS4SettledWitness := function(path)
  local content, stream, mk1, pos, sStart, mk2, sEnd, body, out, p, mPos, j,
        digitStr, mVal, fwMk, fwStart, depth, k, fwEnd, fwBody, items, ip, sym,
        expSign, expDigits, expVal, wMk, wStart, wEnd, wStr, wPermVal;
  stream := InputTextFile(path);
  if stream = fail then Error("ParseS4SettledWitness: cannot open ", path); fi;
  content := ReadAll(stream);
  CloseStream(stream);
  mk1 := "\"settled_detail\":[";
  pos := FindPositionFrom(content, mk1, 1);
  if pos = fail then Error("ParseS4SettledWitness: settled_detail marker not found"); fi;
  sStart := pos + Length(mk1);
  mk2 := "],\"settled_count\":";
  sEnd := FindPositionFrom(content, mk2, sStart);
  if sEnd = fail then Error("ParseS4SettledWitness: settled_count boundary not found"); fi;
  body := content{[sStart .. sEnd-1]};
  out := [];
  p := 1;
  while true do
    mPos := FindPositionFrom(body, "\"m\":", p);
    if mPos = fail then break; fi;
    j := mPos + 4;
    digitStr := "";
    while j <= Length(body) and body[j] in "0123456789" do
      Append(digitStr, [body[j]]);  j := j+1;
    od;
    if Length(digitStr) = 0 then Error("ParseS4SettledWitness: empty m digit at ", mPos); fi;
    mVal := Int(digitStr);
    fwMk := "\"f_word\":[";
    fwStart := FindPositionFrom(body, fwMk, mPos);
    if fwStart = fail then Error("ParseS4SettledWitness: f_word marker not found after ", mPos); fi;
    k := fwStart + Length(fwMk) - 1;
    depth := 0;  fwEnd := fail;
    while k <= Length(body) do
      if body[k] = '[' then depth := depth + 1;
      elif body[k] = ']' then
        depth := depth - 1;
        if depth = 0 then fwEnd := k; break; fi;
      fi;
      k := k + 1;
    od;
    if fwEnd = fail then Error("ParseS4SettledWitness: unbalanced f_word brackets at ", fwStart); fi;
    fwBody := body{[fwStart+Length(fwMk) .. fwEnd-1]};
    items := [];
    ip := 1;
    while true do
      ip := FindPositionFrom(fwBody, "\"", ip);
      if ip = fail then break; fi;
      sym := fwBody[ip+1];
      ip := ip + 4;
      expSign := 1;
      if ip <= Length(fwBody) and fwBody[ip] = '-' then expSign := -1; ip := ip+1; fi;
      expDigits := "";
      while ip <= Length(fwBody) and fwBody[ip] in "0123456789" do
        Append(expDigits, [fwBody[ip]]);  ip := ip+1;
      od;
      expVal := expSign * Int(expDigits);
      Add(items, [[sym], expVal]);
      ip := ip + 1;
    od;
    wMk := "\"automorphism_witness\":\"";
    wStart := FindPositionFrom(body, wMk, fwEnd);
    if wStart = fail then Error("ParseS4SettledWitness: automorphism_witness marker not found after ", fwEnd); fi;
    wStart := wStart + Length(wMk);
    wEnd := FindPositionFrom(body, "\"", wStart);
    if wEnd = fail then Error("ParseS4SettledWitness: unterminated automorphism_witness string at ", wStart); fi;
    wStr := body{[wStart .. wEnd-1]};
    wPermVal := EvalString(wStr);
    if not (wPermVal = () or IsPerm(wPermVal)) then
      Error("ParseS4SettledWitness: automorphism_witness did not evaluate to a permutation -- ", wStr);
    fi;
    Add(out, rec(m := mVal, fword := items, witness := wPermVal));
    p := wEnd + 1;
  od;
  return out;
end;;

#############################################################################
## ---- 本走: 屋根 M の全悉皆(12 m値 x derived subgroup) ----
#############################################################################
Print("\n=== 本走: NF972ScanRoof(M, Mcharm 全12値) ===\n");
t0 := Runtime();;
resM := NF972ScanRoof(rec(x := XM, y := YM, G := GM), Mcharm);;
t1 := Runtime();;
Print("  derived_order=", resM.derived_order, " (expect 367416)  shadow_total=", Length(resM.shadows),
      " (expect 972)  time_ms=", t1-t0, "\n");
if Length(resM.shadows) <> 972 then
  Error("nf972_sourcemap_b_run: shadow_total = ", Length(resM.shadows), " <> 972 -- refusing to write a cert");
fi;

#############################################################################
## ---- NF tuple 化(source map B 本体) ----
#############################################################################
Print("\n=== NF tuple 化 ===\n");
NFTuples := List(resM.shadows, s -> NFTupleOf(s, false, 0));;
NFStrings := List(NFTuples, NFTupleSerialize);;
NFStringsSet := Set(ShallowCopy(NFStrings));;
Print("  tuple総数=", Length(NFStrings), " 重複なし集合サイズ=", Length(NFStringsSet), "\n");
dupCount := Length(NFStrings) - Length(NFStringsSet);;
if Length(NFStringsSet) <> 972 or dupCount <> 0 then
  Error("nf972_sourcemap_b_run: NF tuple set size = ", Length(NFStringsSet), " dup=", dupCount,
        " -- expected 972/0. Refusing to write a cert (集合水準の完全性が崩れている)");
fi;

#############################################################################
## ---- 分離 fixture(仕様 SS4・3種)。cert 書き出し前に必ず発火確認(fail-closed)。
## 設計変更の申告はファイル冒頭コメント参照。実データ resM.shadows から
## 複数m値にまたがるサンプルを取る。
#############################################################################
Print("\n=== 分離fixture 3種(cert書き出し前・不発ならCALIBRATION_FAILED) ===\n");

# 複数m値にまたがるサンプル: 各mから最大3件、合計最大36件
FixtureSample := [];;
BuildFixtureSample := function()
  local mval, group, cnt, s;
  for mval in Mcharm do
    group := Filtered(resM.shadows, s -> s.m = mval);
    cnt := 0;
    for s in group do
      Add(FixtureSample, s);
      cnt := cnt + 1;
      if cnt >= 3 then break; fi;
    od;
  od;
end;;
BuildFixtureSample();;
Print("  fixtureサンプル件数=", Length(FixtureSample), " (m値の異なり数=", Length(Mcharm), ")\n");
if Length(FixtureSample) < 2*Length(Mcharm) then
  Error("nf972_sourcemap_b_run: CALIBRATION_FAILED -- fixture sample too small/undiverse (",
        Length(FixtureSample), ")");
fi;

BaselineFixtureTuples := Set(List(FixtureSample, s -> NFTupleSerialize(NFTupleOf(s, false, 0))));;

# fixture 1: 非自己逆元の向き反転(f -> f^-1)
NonSelfInvSample := Filtered(FixtureSample, s -> s.f <> s.f^-1);;
Print("  fixture1: 非自己逆元サンプル数 = ", Length(NonSelfInvSample), " / ", Length(FixtureSample), "\n");
if Length(NonSelfInvSample) = 0 then
  Error("nf972_sourcemap_b_run: CALIBRATION_FAILED -- fixture1 has no non-self-inverse f in sample");
fi;
Fixture1Baseline := Set(List(NonSelfInvSample, s -> NFTupleSerialize(NFTupleOf(s, false, 0))));;
Fixture1Tuples := Set(List(NonSelfInvSample, s -> NFTupleSerialize(NFTupleOf(s, true, 0))));;
Fixture1Fires := (Fixture1Tuples <> Fixture1Baseline);;
Print("  fixture1 (orientation flip, f -> f^-1) set inequality fires = ", Fixture1Fires, "\n");

# fixture 3: m の法の誤り(正しい M_ord=18 の代わりに 9 を使う)
Fixture3Tuples := Set(List(FixtureSample, s -> NFTupleSerialize(NFTupleOf(s, false, 9))));;
Fixture3Fires := (Fixture3Tuples <> BaselineFixtureTuples);;
Print("  fixture3 (wrong modulus: m mod 9 instead of m in Z/18) set inequality fires = ", Fixture3Fires, "\n");

# fixture 2: 片側 generator swap -- q4側(S4窓)の生成元対応を入替えた別屋根
# GM2 で、サンプルに現れる m 値の一部について実際に再悉皆し、その shadow を
# 同一の can9/can4 パイプラインで NF tuple 化して baseline(GM)と比較する。
Fixture2MVals := Set(List(FixtureSample, s -> s.m)){[1 .. Minimum(3, Length(Set(List(FixtureSample, s -> s.m))))]};;
Print("  fixture2: 検査するm値(GM2で再悉皆) = ", Fixture2MVals, "\n");
resGM2Fixture := NF972ScanRoof(rec(x := XM2, y := YM2, G := GM2), Fixture2MVals);;
Print("  fixture2: GM2側 shadow_total(対象m値のみ) = ", Length(resGM2Fixture.shadows), "\n");
Fixture2BaselineSubset := Set(List(Filtered(resM.shadows, s -> s.m in Fixture2MVals),
  s -> NFTupleSerialize(NFTupleOf(s, false, 0))));;
Fixture2SwappedTuples := Set(List(resGM2Fixture.shadows, s -> NFTupleSerialize(NFTupleOf(s, false, 0))));;
Fixture2Fires := (Fixture2SwappedTuples <> Fixture2BaselineSubset);;
Print("  fixture2 (q4-side generator correspondence swap: GM vs GM2) set inequality fires = ", Fixture2Fires, "\n");

allFixturesFire := Fixture1Fires and Fixture2Fires and Fixture3Fires;;
if not allFixturesFire then
  Error("nf972_sourcemap_b_run: CALIBRATION_FAILED -- not all 3 separation fixtures fired set inequality. ",
        "fixture1=", Fixture1Fires, " fixture2=", Fixture2Fires, " fixture3=", Fixture3Fires,
        ". Refusing to write cert (INTEGRITY_STOP).");
fi;
Print("  全fixture発火 -- CALIBRATION OK.\n");

#############################################################################
## ---- 射影像(仕様 SS3 の2): q9側108・q4側54・compatibility quotient一致 ----
#############################################################################
Print("\n=== 射影像と compatibility quotient ===\n");
Proj9Strings := Set(List(NFTuples, t -> Concatenation("(", String(t.m0), ";", JoinC(List(t.can9,String),","), ")")));;
Proj4Strings := Set(List(NFTuples, t -> Concatenation("(", String(t.m0 mod Pord), ";", JoinC(List(t.can4,String),","), ")")));;
Print("  proj9(K9側)距離集合サイズ=", Length(Proj9Strings), " (expect 108)\n");
Print("  proj4(S4側)距離集合サイズ=", Length(Proj4Strings), " (expect 54)\n");
proj9OK := (Length(Proj9Strings) = 108);;
proj4OK := (Length(Proj4Strings) = 54);;

# compatibility quotient一致: K9単体アンカー(独自 NF972ScanRoof(K9単体))の
# NF(m0,can9)集合が、Mの972からのq9射影集合と一致するか。S4単体側も同様。
K9AnchorTuples := Set(List(resK9anchor.shadows, s ->
  Concatenation("(", String(s.m), ";", JoinC(List(Can9OfPerm27(BlockRestrict(s.f,0,27)), String), ","), ")")));;
# K9単体窓ではf自体が27点上の元(G9そのもの)。BlockRestrict(f,0,27)はfが27点
# 上の順列である前提だが、g9.Gの生成元は27点上なのでそのまま使える。
S4AnchorTuples := Set(List(resS4anchor.shadows, s ->
  Concatenation("(", String(s.m), ";", JoinC(List(Can4OfPerm9(PermList(List([1..9], j -> j^s.f))), String), ","), ")")));;
compat9OK := (K9AnchorTuples = Proj9Strings);;
compat4OK := (S4AnchorTuples = Proj4Strings);;
Print("  compatibility(K9単体NF = Mのq9射影) = ", compat9OK, "\n");
Print("  compatibility(S4単体NF = Mのq4射影) = ", compat4OK, "\n");

if not (proj9OK and proj4OK and compat9OK and compat4OK) then
  Print("*** WARNING: 射影像またはcompatibility quotientが期待通りでない -- cert にありのまま記録し即報 ***\n");
fi;

#############################################################################
## ---- v1.1追補(裁定442・§6)辞書の自己検査(義務・fail-closed) ----
## can9射影集合(Proj9Strings)がK9.v1.jsonのf_triple行集合と逐語一致、
## can4射影集合(Proj4Strings)がS4.v2.jsonのwitness(pass:trueのgeneration_detail
## をf_word評価したもの)と逐語一致することを機械検査する。辞書は「自構成の
## marked生成元(g9.x,g9.y / Xperm,Yperm)= cert側のmarked生成元」という恒等
## 対応(week3-battery-common.gのMakeGn/week3-psl-common.gのRunPSLWindowが
## K9.v1.json/S4.v2.jsonの生成元と同一構成式であることをソースコード比較で
## 確認済み -- ops/express/20260804_implementer_nf972b_predicate_bug_found.md
## に記録)。不一致ならINTEGRITY_STOP(補正禁止・即保存・即報)。
#############################################################################
Print("\n=== v1.1追補: 辞書の自己検査(K9.v1.json/S4.v2.jsonとの逐語一致) ===\n");

K9_CERT_PATH := "certificates/K9.v1.json";;
S4_CERT_PATH := "certificates/S4.v2.json";;

k9CertRaw := ParseK3Shadows(K9_CERT_PATH);;
Print("  K9.v1.json shadows parsed = ", Length(k9CertRaw), " (expect 108)\n");
K9CertTupleStrings := Set(List(k9CertRaw, r ->
  Concatenation("(", String(r.m), ";", JoinC(List(Concatenation(r.triple), String), ","), ")")));;

dictK9OK := (K9CertTupleStrings = Proj9Strings);;
Print("  辞書適用後 q9射影 = K9.v1.json f_triple 逐語一致 ? ", dictK9OK, "  (K9側は司令塔第2回突合でA=B一致確認済み・触らない)\n");
if not dictK9OK then
  Error("nf972_sourcemap_b_run: INTEGRITY_STOP -- K9 dictionary self-check regressed (should still be identity/PASS). Report to commander.");
fi;

#############################################################################
## ---- v1.2追補(裁定454・§7)訂正: S4側 sigma は marked 生成元対応で決定 ----
## 【申告】前版はwitness(automorphism_witness = settled判定のconjugator h)
## をq4(f)の像だと誤認してsigma探索していた(司令塔第2回仲裁も同じ誤読・
## 裁定454で訂正)。witnessはcan4の材料にしてはならない(v1.2 pin #1)。
## 正しい手順: cert枠(点ラベル系)を S4.v2.json の marking(S,T行列)から
## week3-psl-common.g と同じ構成規約 X_cert:=w^2, Y_cert:=S^-1*X_cert*S で
## 独自に再構成し、sigma in Sym(9) を (Xperm,Yperm) -> (Xperm_cert,Yperm_cert)
## の同時共役で機械決定する(cert生成コードの構成規約を読むのは「枠定義の
## 読解」として許可されている -- A の実装は引き続き非参照)。
#############################################################################
Print("\n=== v1.2訂正: S4側 sigma は marked 生成元対応で決定 ===\n");

# ---- S4.v2.json の marking(S,T)を自前パースして cert枠を再構成 ----
ParseS4Marking := function(path)
  local content, stream, mk, sPos, sStart, sEnd, sStr, tPos, tStart, tEnd, tStr;
  stream := InputTextFile(path);
  if stream = fail then Error("ParseS4Marking: cannot open ", path); fi;
  content := ReadAll(stream);
  CloseStream(stream);
  mk := "\"S\":\"";
  sPos := FindPositionFrom(content, mk, 1);
  if sPos = fail then Error("ParseS4Marking: \"S\": marker not found"); fi;
  sStart := sPos + Length(mk);
  sEnd := FindPositionFrom(content, "\"", sStart);
  sStr := content{[sStart .. sEnd-1]};
  mk := "\"T\":\"";
  tPos := FindPositionFrom(content, mk, sEnd);
  if tPos = fail then Error("ParseS4Marking: \"T\": marker not found"); fi;
  tStart := tPos + Length(mk);
  tEnd := FindPositionFrom(content, "\"", tStart);
  tStr := content{[tStart .. tEnd-1]};
  return rec(Svals := DigitRunsToInts(sStr), Tvals := DigitRunsToInts(tStr));
end;;

s4Marking := ParseS4Marking(S4_CERT_PATH);;
Print("  parsed marking: S=", s4Marking.Svals, " T=", s4Marking.Tvals, "\n");
if Length(s4Marking.Svals) <> 4 or Length(s4Marking.Tvals) <> 4 then
  Error("nf972_sourcemap_b_run: INTEGRITY_STOP -- marking parse did not yield 4+4 ints. Report to commander.");
fi;

Smat_cert := MakeMatGF8(s4Marking.Svals[1], s4Marking.Svals[2], s4Marking.Svals[3], s4Marking.Svals[4]);;
Tmat_cert := MakeMatGF8(s4Marking.Tvals[1], s4Marking.Tvals[2], s4Marking.Tvals[3], s4Marking.Tvals[4]);;
Sperm_cert := MatToPermGF8(Smat_cert);;
Tperm_cert := MatToPermGF8(Tmat_cert);;
wPerm_cert := Sperm_cert * Tperm_cert^-1;;
Xperm_cert := wPerm_cert^2;;
Yperm_cert := Sperm_cert^-1 * Xperm_cert * Sperm_cert;;
Print("  cert枠: Xperm_cert=Xperm ? ", (Xperm_cert = Xperm), "  Yperm_cert=Yperm ? ", (Yperm_cert = Yperm), "\n");

# ---- sigma in Sym(9): (Xperm,Yperm) -> (Xperm_cert,Yperm_cert) の同時共役 ----
Sym9 := SymmetricGroup(9);;
sigma0 := RepresentativeAction(Sym9, Xperm, Xperm_cert);;
if sigma0 = fail then
  Error("nf972_sourcemap_b_run: INTEGRITY_STOP -- RepresentativeAction failed for Xperm -> Xperm_cert ",
        "(not conjugate in Sym(9)). Report to commander.");
fi;
centX := Centralizer(Sym9, Xperm);;
centXElts := Elements(centX);;
Print("  centralizer(Xperm) in Sym(9) size = ", Length(centXElts), " -- candidate sigma coset size\n");
sigmaCandidates := List(centXElts, c -> sigma0*c);;
validSigmas := Filtered(sigmaCandidates, s -> s*Yperm*s^-1 = Yperm_cert);;
Print("  (Xperm,Yperm)->(Xperm_cert,Yperm_cert) を同時満足する sigma 候補数 = ", Length(validSigmas), "\n");

# 一意性の理論的裏付け: <Xperm_cert,Yperm_cert> = Pgrp_cert の Sym(9) 内
# centralizer が自明かどうかを直接報告する(非自明なら候補が複数になり得る)。
Pgrp_cert_forCent := Group(Xperm_cert, Yperm_cert);;
centOfImageGroup := Centralizer(Sym9, Pgrp_cert_forCent);;
Print("  centralizer_{Sym(9)}(<Xperm_cert,Yperm_cert>) size = ", Size(centOfImageGroup),
      " (自明=1なら sigma は一意のはず)\n");

if Length(validSigmas) = 0 then
  Error("nf972_sourcemap_b_run: INTEGRITY_STOP -- no sigma satisfies (Xperm,Yperm)->(Xperm_cert,Yperm_cert) ",
        "simultaneously. Report to commander -- do not force a correction.");
elif Length(validSigmas) > 1 then
  Error("nf972_sourcemap_b_run: INTEGRITY_STOP -- ", Length(validSigmas),
        " sigma candidates satisfy the simultaneous conjugation (not unique; centralizer size=",
        Size(centOfImageGroup), "). List: ", validSigmas,
        ". Report to commander -- do not pick arbitrarily.");
fi;
sigma := validSigmas[1];;
Print("  sigma (一意) = ", sigma, "\n");
Print("  sigma = identity ? ", (sigma = ()), "\n");

#############################################################################
## ---- can4' = sigma 適用後の one-line(cert点ラベル枠) ----
#############################################################################
Can4OfPerm9Sigma := function(perm9)
  local l, j, transformed;
  transformed := sigma * perm9 * sigma^-1;
  l := [];
  for j in [1 .. 9] do l[j] := j^transformed; od;
  return l;
end;;

#############################################################################
## ---- 自己検査(義務・非トートロジー形・v1.2 §7-6): 別経路突合 ----
## 右辺 = cert枠(Xperm_cert,Yperm_cert)で直接評価した P_cert枠(f)。
## 左辺 = 自表現(Xperm,Yperm)で評価してsigma適用した sigma(P_B(f))。
## witness集合との照合は廃止(v1.2で指示)。
#############################################################################
s4PassingRaw := ParseS4PassingFWords(S4_CERT_PATH);;
Print("  S4.v2.json generation_detail pass:true parsed = ", Length(s4PassingRaw), " (expect 54)\n");

selfCheckRowResults := List(s4PassingRaw, function(r)
  local pB, pCertFrame, lhs;
  pB := WordEval(r.fword, Xperm, Yperm);
  lhs := sigma * pB * sigma^-1;
  pCertFrame := WordEval(r.fword, Xperm_cert, Yperm_cert);
  return (lhs = pCertFrame);
end);;
s4SelfCheckPassCount := Length(Filtered(selfCheckRowResults, x -> x));;
Print("  別経路突合(sigma(P_B(f)) = P_cert枠(f)) PASS件数 = ", s4SelfCheckPassCount, " / ", Length(s4PassingRaw), "\n");
dictS4OK := (s4SelfCheckPassCount = Length(s4PassingRaw) and Length(s4PassingRaw) = 54);;

if not (dictK9OK and dictS4OK) then
  Error("nf972_sourcemap_b_run: INTEGRITY_STOP -- post-sigma non-tautological self-check failed (K9=",
        dictK9OK, " S4=", dictS4OK, " passCount=", s4SelfCheckPassCount, "/", Length(s4PassingRaw),
        "). Refusing to write v3 cert. Report to commander.");
fi;
Print("  辞書自己検査(v1.2非トートロジー形) PASS -- K9=恒等・S4=sigma(下記記録)。\n");

#############################################################################
## ---- v1.2 §7-3: AbstractProd 規約 fixture(A5-CONV 型・既知語->既知像) ----
## 可換な生成元では規約バグが不可視になるため、非可換な Xperm,Yperm(および
## K9側 g9.x,g9.y)で「xy」(paper記法)の評価が GAP の y*x になることを
## 直接検査し、x*y(誤り規約)とは異なることも確認する。
#############################################################################
Print("\n=== v1.2 §7-3: AbstractProd 規約 fixture(A5-CONV型) ===\n");
convFixtureWord := [["x",1],["y",1]];;
convWordS4 := WordEval(convFixtureWord, Xperm, Yperm);;
convExpectedS4 := Yperm * Xperm;;
convWrongS4 := Xperm * Yperm;;
convFixtureS4Pass := (convWordS4 = convExpectedS4) and (convWordS4 <> convWrongS4) and (Xperm*Yperm <> Yperm*Xperm);;
Print("  S4(Xperm,Yperm)非可換fixture: WordEval([x,y])=y*x ? ", (convWordS4=convExpectedS4),
      "  かつ x*yとは不一致 ? ", (convWordS4<>convWrongS4), "  かつXperm,Yperm非可換 ? ",
      (Xperm*Yperm<>Yperm*Xperm), "  => PASS=", convFixtureS4Pass, "\n");

convWordK9 := WordEval(convFixtureWord, g9.x, g9.y);;
convExpectedK9 := g9.y * g9.x;;
convWrongK9 := g9.x * g9.y;;
convFixtureK9Pass := (convWordK9 = convExpectedK9) and (convWordK9 <> convWrongK9) and (g9.x*g9.y <> g9.y*g9.x);;
Print("  K9(g9.x,g9.y)非可換fixture: WordEval([x,y])=y*x ? ", (convWordK9=convExpectedK9),
      "  かつ x*yとは不一致 ? ", (convWordK9<>convWrongK9), "  かつg9.x,g9.y非可換 ? ",
      (g9.x*g9.y<>g9.y*g9.x), "  => PASS=", convFixtureK9Pass, "\n");

if not (convFixtureS4Pass and convFixtureK9Pass) then
  Error("nf972_sourcemap_b_run: INTEGRITY_STOP -- AbstractProd convention fixture (A5-CONV) failed ",
        "(S4=", convFixtureS4Pass, " K9=", convFixtureK9Pass, "). Refusing to write v3 cert.");
fi;
Print("  規約fixture(A5-CONV) 両窓 PASS。\n");

#############################################################################
## ---- canonical 列挙 bytes と sha256 ----
#############################################################################
Print("\n=== canonical serialization ===\n");
SortedNFStrings := ShallowCopy(NFStringsSet);;
Sort(SortedNFStrings);;
CanonicalBytes := JoinC(SortedNFStrings, "\n");;
CanonicalSha256 := ComputeSha256OfString(CanonicalBytes);;
Print("  canonical_sha256=", CanonicalSha256, "\n");

selfSha := ComputeSha256FileB("search/probe/wac_v1/nf972_sourcemap_b_run.g");;

#############################################################################
## ---- tuple 本体 dump(v1・乗算規約バグ修正後に再生成) ----
## 【申告】前版の canonical_sha256 は "ecaf87c77effc1d2ef955969152c58e0825403b4858b4ff21e688fd3c02ffede"
## だったが、NF972HexagonOK の乗算規約バグ(本ファイル冒頭コメント参照)により
## 屋根Mのshadow集合そのものが誤っていたため、修正後の値と一致しないのは
## 正しい(再現性の欠如ではなく、修正による意図した変化)。旧cert/旧dumpは
## search/certs/superseded/ に保存済み。
#############################################################################
Print("\n=== tuple本体dump(972本・JSON配列・v1・バグ修正後) ===\n");
TUPLES_OUT_PATH := "search/certs/nf972_sourcemap_b_tuples_20260804.json";;
PRE_FIX_CANONICAL_SHA := "ecaf87c77effc1d2ef955969152c58e0825403b4858b4ff21e688fd3c02ffede";;
shaChangedFromPreFix := (CanonicalSha256 <> PRE_FIX_CANONICAL_SHA);;
Print("  canonical_sha256(修正後)=", CanonicalSha256, "\n");
Print("  canonical_sha256(修正前・superseded)=", PRE_FIX_CANONICAL_SHA,
      "  differs_as_expected=", shaChangedFromPreFix, "\n");

tuplesJson := Concatenation(
  "{\n",
  "  \"schema\":\"nf972-sourcemap-b-tuples/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/nf972_sourcemap_b_run.g\",\n",
  "  \"source_cert\":\"search/certs/nf972_sourcemap_b_20260804.json\",\n",
  "  \"note\":\"NF972HexagonOKの乗算規約バグ修正後の再生成(ops/express/20260804_implementer_nf972b_predicate_bug_found.md参照)。A側の実装・値は一切参照していない。突合は司令塔が別途実施。\",\n",
  "  \"supersedes\":\"search/certs/superseded/nf972_sourcemap_b_tuples_20260804_PRE_PREDICATE_FIX.json\",\n",
  "  \"supersedes_canonical_sha256\":", JStr(PRE_FIX_CANONICAL_SHA), ",\n",
  "  \"serialization_format\":\"(m0;a1,eps1,a2,eps2,a3,eps3;i1,...,i9)\",\n",
  "  \"sort_order\":\"gap_String_sort_of_serialized_tuple\",\n",
  "  \"count\":", String(Length(SortedNFStrings)), ",\n",
  "  \"canonical_bytes_join\":\"newline\",\n",
  "  \"canonical_bytes_sha256\":", JStr(CanonicalSha256), ",\n",
  "  \"dictionary_selfcheck_pass\":", JB(dictK9OK and dictS4OK), ",\n",
  "  \"tuples\":", JArr(List(SortedNFStrings, JStr)), "\n",
  "}\n");;
WriteFile(TUPLES_OUT_PATH, tuplesJson);;
Print("  Wrote ", TUPLES_OUT_PATH, " (", Length(SortedNFStrings), " tuples)\n");

#############################################################################
## ---- v2出力(【申告】司令塔第2回突合により誤りと判明・v3で置換) ----
## v2はS4側の辞書を「恒等」と主張していたが、その自己検査はS4.v2.jsonの
## f_wordを自分の生成元で評価した結果と自分のq4像を比較するトートロジー
## だった(事故台帳#6型・司令塔指摘)。実際にはS4側にsigma(非恒等)が必要
## だったことが後続のsigma探索(下記)で判明した。v2ファイルは記録として
## 残すが、S4側の内容は無効であることをここに明記し、正しい結果はv3に
## 書く。K9側(dictK9OK)は引き続き有効(司令塔確認済み)。
#############################################################################
Print("\n=== v2出力(S4側は無効と判明・記録として残す) ===\n");
TUPLES_V2_OUT_PATH := "search/certs/nf972_sourcemap_b_tuples_v2_20260804.json";;

tuplesV2Json := Concatenation(
  "{\n",
  "  \"schema\":\"nf972-sourcemap-b-tuples-v2/v1_1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/nf972_sourcemap_b_run.g\",\n",
  "  \"design_doc\":\"docs/notes/nf972_freeze_v1.md v1.1追補(裁定442)SS6\",\n",
  "  \"status\":\"S4側は無効(トートロジー自己検査だったため)-- 正しい結果は nf972_sourcemap_b_tuples_v3_20260804.json を参照。K9側(dictK9OK)は有効。\",\n",
  "  \"note\":\"canonical marking = factor cert座標系(K9.v1.json f_triple・S4.v2.json witness)。K9側の辞書は自構成marked生成元(g9.x,g9.y)とcert側marked生成元の恒等対応(確認済み)。S4側は当初『恒等』と主張したがトートロジーな自己検査によるもので、司令塔第2回突合(A=54/54・B=1/54)により誤りと判明。正しい辞書(sigma)はv3を参照。A側の実装・出力は一切参照していない。\",\n",
  "  \"root_cause_note\":\"第1回突合の交わり9/972は座標系未宣言ではなく、本実装のNF972HexagonOK乗算規約バグ(修正はこのスクリプトの冒頭コメントと ops/express/20260804_implementer_nf972b_predicate_bug_found.md に記録)が原因だった。バグ修正後もS4側の自己検査がトートロジーだったため、点ラベルのずれ(sigma)を見逃していた。\",\n",
  "  \"dictionary\":{\n",
  "    \"k9_type\":\"identity(有効)\",\n",
  "    \"s4_type\":\"INVALID(トートロジー自己検査 -- 実際はsigma非恒等が必要。v3参照)\",\n",
  "    \"k9_cert_path\":", JStr(K9_CERT_PATH), ",\n",
  "    \"s4_cert_path\":", JStr(S4_CERT_PATH), ",\n",
  "    \"k9_cert_shadow_count_parsed\":", String(Length(k9CertRaw)), ",\"k9_cert_expected\":108\n",
  "  },\n",
  "  \"dictionary_selfcheck\":{\n",
  "    \"q9_projection_matches_k9_cert_f_triple_verbatim\":", JB(dictK9OK), ",\n",
  "    \"q4_check_note\":\"v2時点のq4検査は無効(トートロジー)。v3のsigma版を参照。\"\n",
  "  },\n",
  "  \"serialization_format\":\"(m0;a1,eps1,a2,eps2,a3,eps3;i1,...,i9)\",\n",
  "  \"sort_order\":\"gap_String_sort_of_serialized_tuple\",\n",
  "  \"count\":", String(Length(SortedNFStrings)), ",\n",
  "  \"canonical_bytes_sha256\":", JStr(CanonicalSha256), ",\n",
  "  \"tuples\":", JArr(List(SortedNFStrings, JStr)), "\n",
  "}\n");;
WriteFile(TUPLES_V2_OUT_PATH, tuplesV2Json);;
Print("  Wrote ", TUPLES_V2_OUT_PATH, " (", Length(SortedNFStrings),
      " tuples, S4側は無効と明記・v3参照を記載)\n");

#############################################################################
## ---- v3出力(v1.2追補・裁定454の訂正指示): sigma(marked生成元対応)経由の
## 正しい tuple 972本 ----
## can4' = sigma適用後one-line(cert枠=Xperm_cert,Yperm_certで再構成した点
## ラベル系)。can9はK9側で既にA=B一致済みのため不変。dictionary_selfcheck
## は非トートロジー形(cert枠評価 vs 自表現評価+sigma の別経路突合)。
#############################################################################
Print("\n=== v3出力: sigma(marked生成元対応)辞書 tuple v3 ===\n");
TUPLES_V3_OUT_PATH := "search/certs/nf972_sourcemap_b_tuples_v3_20260804.json";;

NFTupleOfV3 := function(shadowRec)
  local f, m0, p27, q4perm, can9v, can4v;
  f := shadowRec.f;
  m0 := shadowRec.m;
  p27 := BlockRestrict(f, 0, 27);
  can9v := Can9OfPerm27(p27);
  q4perm := BlockRestrict(f, 27, 9);
  can4v := Can4OfPerm9Sigma(q4perm);
  return rec(m0 := m0, can9 := can9v, can4 := can4v);
end;;

NFTuplesV3 := List(resM.shadows, NFTupleOfV3);;
NFStringsV3 := List(NFTuplesV3, NFTupleSerialize);;
NFStringsV3Set := Set(ShallowCopy(NFStringsV3));;
dupCountV3 := Length(NFStringsV3) - Length(NFStringsV3Set);;
Print("  v3 tuple総数=", Length(NFStringsV3), " 重複なし集合サイズ=", Length(NFStringsV3Set),
      " 重複=", dupCountV3, "\n");
if Length(NFStringsV3Set) <> 972 or dupCountV3 <> 0 then
  Error("nf972_sourcemap_b_run: v3 tuple set size = ", Length(NFStringsV3Set), " dup=", dupCountV3,
        " -- expected 972/0. Refusing to write v3 cert.");
fi;
SortedNFStringsV3 := ShallowCopy(NFStringsV3Set);;
Sort(SortedNFStringsV3);;
CanonicalBytesV3 := JoinC(SortedNFStringsV3, "\n");;
CanonicalSha256V3 := ComputeSha256OfString(CanonicalBytesV3);;
Print("  v3 canonical_sha256=", CanonicalSha256V3, "\n");

sigmaStr := String(sigma);;

tuplesV3Json := Concatenation(
  "{\n",
  "  \"schema\":\"nf972-sourcemap-b-tuples-v3/v1_2\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/nf972_sourcemap_b_run.g\",\n",
  "  \"design_doc\":\"docs/notes/nf972_freeze_v1.md v1.2追補(裁定454)SS7\",\n",
  "  \"note\":\"can9(K9側)はv1/v2と不変(A=B一致済み・司令塔確認済み)。can4(S4側)はsigma適用後one-lineへ改訂(cert枠=S4.v2.jsonのmarkingからweek3-psl-common.g L275-277と同構成規約で再構成したXperm_cert,Yperm_cert)。v2/前回速達のwitness起点sigma探索は誤り(witness=settled判定のconjugator hであってq4(f)の像ではない・裁定454)だったため廃棄し、本ファイルが正版。A側の実装(nf972_sourcemap_a_driver.py)は一切参照していない -- cert生成コード(week3-psl-common.g)の構成規約を読むのは『枠定義の読解』として許可されている(A非参照とは別枠)。\",\n",
  "  \"supersedes\":\"search/certs/nf972_sourcemap_b_tuples_v2_20260804.json(S4側のみ -- K9側は継続有効)\",\n",
  "  \"dictionary\":{\n",
  "    \"k9\":{\"type\":\"identity\",\"selfcheck_pass\":", JB(dictK9OK), "},\n",
  "    \"s4\":{\n",
  "      \"type\":\"conjugation_by_sigma_via_marked_generator_correspondence\",\n",
  "      \"sigma_domain\":\"Sym(9) acting on the same 9 points as Xperm,Yperm (week3-psl-common.g GF(8) construction)\",\n",
  "      \"sigma_gap_repr\":", JStr(sigmaStr), ",\n",
  "      \"transform\":\"can4'(perm9) := one-line(sigma * perm9 * sigma^-1)\",\n",
  "      \"cert_frame_marking_parsed\":{\"S\":", String(s4Marking.Svals), ",\"T\":", String(s4Marking.Tvals), "},\n",
  "      \"xperm_cert_equals_xperm\":", JB(Xperm_cert = Xperm), ",\n",
  "      \"yperm_cert_equals_yperm\":", JB(Yperm_cert = Yperm), ",\n",
  "      \"determination_method\":\"RepresentativeAction(Sym(9), Xperm, Xperm_cert) で基点sigma0を取得、Centralizer(Sym(9),Xperm)のcosetとして候補を列挙し、sigma*Yperm*sigma^-1=Yperm_cert でフィルタ(Xperm,Yperm同時共役)\",\n",
  "      \"centralizer_xperm_size\":", String(Length(centXElts)), ",\n",
  "      \"candidate_coset_size\":", String(Length(sigmaCandidates)), ",\n",
  "      \"valid_sigma_count\":", String(Length(validSigmas)), ",\n",
  "      \"uniqueness_confirmed\":", JB(Length(validSigmas) = 1), ",\n",
  "      \"centralizer_of_image_group_in_sym9_size\":", String(Size(centOfImageGroup)), ",\n",
  "      \"selfcheck_pass\":", JB(dictS4OK), "\n",
  "    }\n",
  "  },\n",
  "  \"dictionary_selfcheck\":{\n",
  "    \"note\":\"非トートロジー形(v1.2 SS7-6): 右辺=cert枠(Xperm_cert,Yperm_cert)でS4.v2.jsonの各f_wordを直接評価。左辺=自表現(Xperm,Yperm)で同じf_wordを評価しsigmaを適用。両者を全54行で突合(witness集合との照合は廃止)。\",\n",
  "    \"rows_checked\":", String(Length(s4PassingRaw)), ",\n",
  "    \"rows_pass\":", String(s4SelfCheckPassCount), ",\n",
  "    \"all_54_pass\":", JB(dictS4OK), "\n",
  "  },\n",
  "  \"conv_fixture_a5\":{\n",
  "    \"note\":\"v1.2 SS7-3: AbstractProd反転規約(paper AB = GAP B*A)を非可換生成元で機械検査(可換fixtureでは規約バグが不可視なため)。\",\n",
  "    \"s4_fixture_pass\":", JB(convFixtureS4Pass), ",\n",
  "    \"k9_fixture_pass\":", JB(convFixtureK9Pass), "\n",
  "  },\n",
  "  \"serialization_format\":\"(m0;a1,eps1,a2,eps2,a3,eps3;i1,...,i9) -- i1..i9はsigma適用後のone-line(cert枠)\",\n",
  "  \"sort_order\":\"gap_String_sort_of_serialized_tuple\",\n",
  "  \"count\":", String(Length(SortedNFStringsV3)), ",\n",
  "  \"canonical_bytes_sha256\":", JStr(CanonicalSha256V3), ",\n",
  "  \"tuples\":", JArr(List(SortedNFStringsV3, JStr)), "\n",
  "}\n");;
WriteFile(TUPLES_V3_OUT_PATH, tuplesV3Json);;
Print("  Wrote ", TUPLES_V3_OUT_PATH, " (", Length(SortedNFStringsV3), " tuples, dictionary selfcheck K9=",
      dictK9OK, " S4=", dictS4OK, ")\n");

#############################################################################
## ---- JSON 出力 ----
#############################################################################
OUT_PATH := "search/certs/nf972_sourcemap_b_20260804.json";;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"nf972-sourcemap-b/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/nf972_sourcemap_b_run.g\",\n",
  "  \"design_doc\":\"docs/notes/nf972_freeze_v1.md(裁定434凍結)\",\n",
  "  \"card_label\":\"NF-972 source map B(直接悉皆側・独立実装・A非参照)\",\n",
  "  \"independence_note\":\"source map A(組立側)の実装・中間表現・normalizer helperを一切参照・共有しない。共有は凍結仕様のschemaのみ。列挙戦略はihnec_r4b_run.gと同型(Elements(DerivedSubgroup(G))直接列挙)だが判定関数(NF972HexagonOK)・NF化(q9/q4評価・can9/can4・serialization)はすべて自前実装で、R4bのScanRoofHexagonコード自体は再利用していない。\",\n",
  "  \"can9_can4_design_note\":\"can9=27点を9点x3ブロックに分解しD_9=<r,s>正規形(a,eps)の3つ組(固定順)。can4=9点one-line image。この具体化はops/express/20260804_implementer_nf972b_can9設計判断.mdで速達済みの実装係解釈であり司令塔/Sol確認は未了。\",\n",
  "  \"deviation_note\":\"分離fixtureの実行順序を『本走前の独立小サンプル』から『本走直後・cert書き出し前の実データサンプル』へ変更(script冒頭コメントに理由詳記)。fixture2はcan9内r,s入替(構造的に不発と判明)からq4側generator対応を入替えた別屋根GM2での再悉皆比較へ変更。いずれもfail-closed gate(不発ならcert非出力)は維持。\",\n",
  "  \"bug_fix_note\":\"v1.1追補(裁定442)の辞書自己検査を実施中、K9側は108/108一致もS4側は当初6/54しか一致しないことが判明。原因はmarking/座標系ではなくNF972HexagonOKの乗算規約バグ(ymf/hex311/genB/zEltがplainなGAP `*`でAbstractProd反転規約と不一致)。K9窓は偶然結果不変・S4窓(PSL(2,8)非可換単純群)は実際に影響していた。修正後は本cert(972点)・辞書自己検査とも正しい値。旧(バグ版)certはsearch/certs/superseded/に保存。詳細はops/express/20260804_implementer_nf972b_predicate_bug_found.md。\",\n",
  "  \"dictionary_selfcheck\":{\n",
  "    \"design_doc\":\"docs/notes/nf972_freeze_v1.md v1.1追補(裁定442)SS6 + 司令塔第2回突合指示\",\n",
  "    \"note\":\"q9(K9側)は恒等辞書で逐語一致(有効・司令塔確認済み)。q4(S4側)は当初『恒等』と主張したが司令塔指摘によりトートロジー自己検査と判明、正しくは非恒等sigma(Sym(9)の共役)が必要 -- 本v1 cert自体のcan4は恒等のまま(sigma未適用)であり、sigma適用版はsearch/certs/nf972_sourcemap_b_tuples_v3_20260804.jsonを参照。ここに記録するq4フラグは(sigma適用後の)最新の自己検査結果。\",\n",
  "    \"q9_dictionary_type\":\"identity\",\n",
  "    \"q4_dictionary_type\":\"conjugation_by_sigma(詳細はtuples_v3参照・本v1のcan4値自体は非sigma)\",\n",
  "    \"q9_projection_matches_k9_cert_f_triple_verbatim\":", JB(dictK9OK), ",\n",
  "    \"q4_projection_matches_s4_cert_witness_verbatim_after_sigma\":", JB(dictS4OK), "\n",
  "  },\n",
  "  \"windows\":{\n",
  "    \"g9_size\":", String(K9sz), ",\"k9_ord\":", String(K9ord), ",\n",
  "    \"p_size\":", String(Psz), ",\"n_s4_ord\":", String(Pord), ",\n",
  "    \"gm_size\":", String(Size(GM)), ",\"m_ord\":", String(Mord), "\n",
  "  },\n",
  "  \"anchors\":{\n",
  "    \"k9_alone_shadow_total\":", String(Length(resK9anchor.shadows)), ",\"k9_alone_expected\":108,\n",
  "    \"s4_alone_shadow_total\":", String(Length(resS4anchor.shadows)), ",\"s4_alone_expected\":54\n",
  "  },\n",
  "  \"fixtures\":{\n",
  "    \"note\":\"仕様SS4の3種をresM.shadows実データからのサンプル(", String(Length(FixtureSample)), "件・m値", String(Length(Mcharm)), "種にまたがる)で実行。fixture2のみGM2での実再悉皆(対象m値=", JArr(List(Fixture2MVals,String)), ")を伴う。cert書き出し前のfail-closed gate(この cert が存在する時点で全発火済み)。\",\n",
  "    \"fixture1_orientation_flip_fires\":", JB(Fixture1Fires), ",\n",
  "    \"fixture2_q4_side_generator_swap_fires\":", JB(Fixture2Fires), ",\n",
  "    \"fixture3_wrong_modulus_fires\":", JB(Fixture3Fires), "\n",
  "  },\n",
  "  \"main_scan\":{\n",
  "    \"derived_order\":", String(resM.derived_order), ",\"derived_order_expected\":367416,\n",
  "    \"shadow_total\":", String(Length(resM.shadows)), ",\"shadow_total_expected\":972,\n",
  "    \"wall_ms\":", String(t1-t0), "\n",
  "  },\n",
  "  \"nf_tuple_set\":{\n",
  "    \"total_tuples\":", String(Length(NFStrings)), ",\n",
  "    \"distinct_tuples\":", String(Length(NFStringsSet)), ",\n",
  "    \"duplicate_count\":", String(dupCount), ",\n",
  "    \"matches_972_0dup\":", JB(Length(NFStringsSet) = 972 and dupCount = 0), "\n",
  "  },\n",
  "  \"projections\":{\n",
  "    \"proj9_q9_side_size\":", String(Length(Proj9Strings)), ",\"proj9_expected\":108,\"proj9_ok\":", JB(proj9OK), ",\n",
  "    \"proj4_q4_side_size\":", String(Length(Proj4Strings)), ",\"proj4_expected\":54,\"proj4_ok\":", JB(proj4OK), ",\n",
  "    \"compatibility_k9_alone_eq_proj9\":", JB(compat9OK), ",\n",
  "    \"compatibility_s4_alone_eq_proj4\":", JB(compat4OK), "\n",
  "  },\n",
  "  \"canonical_enumeration\":{\n",
  "    \"sort_order\":\"gap_String_sort_of_serialized_tuple\",\n",
  "    \"serialization_format\":\"(m0;a1,eps1,a2,eps2,a3,eps3;i1,...,i9)\",\n",
  "    \"count\":", String(Length(SortedNFStrings)), ",\n",
  "    \"sha256\":", JStr(CanonicalSha256), "\n",
  "  },\n",
  "  \"conventions_used\":{\n",
  "    \"conventions_ver\":\"v1_6\",\n",
  "    \"perm_composition\":\"gap_native_right_action\",\n",
  "    \"cv1_cv2_action_side\":\"q9,q4は右作用のGAP順列制限(BlockRestrict)として評価。can9はD_9=<r,s>のGAP乗算 r^a*s^eps(左から順・GAP native)での正規形照合。can4はone-line image(j -> j^perm)。fixture2はGM2(q4側=S4窓のXperm/Yperm対応を入替えた別屋根)での実再悉皆によるq4側単独のgenerator対応入替。\",\n",
  "    \"reduced_hexagon_predicate\":\"NF972HexagonOK(本driver独自実装・数学的判定式・乗算規約ともihnec_r4b_run.gのScanRoofHexagonとAbstractProd経由で同一。コードは非共有。当初plain `*`で書いており規約が食い違っていたバグを修正済み -- bug_fix_note参照。\",\n",
  "    \"independence_note\":\"source map A の実装・出力(nf972_sourcemap_a_*.json)は一切読まない。G9・P・GMはGAPで生成器から新規構築(week3-*-common.gの既存共有関数を使用 -- これはA/B双方が使い得る共通インフラであり、どちらか固有のnormalizer helperではない)。v1.1追補(裁定442)の指示により certificates/K9.v1.json・certificates/S4.v2.json は辞書自己検査の突合対象として読む(これはA非参照の原則とは別枠 -- factor certは共有仕様の一部であり司令塔指示による)。\"\n",
  "  },\n",
  "  \"cross_checked_status\":{\"status\":\"n/a\",\"reason\":\"本certは source map B 単独の出力。source map A との集合突合は司令塔が別途実施する。\"},\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"wall_ms_total\":", String(GAPLIB_WallElapsedMs()), "\n",
  "  }\n",
  "}\n");;

WriteFile(OUT_PATH, cert);;
Print("\nWrote ", OUT_PATH, "\n");

#############################################################################
## ---- v4出力(CV-9判読 nf972_cv9_reading_v1.md の指摘3点への対応) ----
## 【申告】v1 cert の dictionary_selfcheck 欄は「非トートロジー形」と称して
## いたが、CV-9 判読(falsifier)により、S,T行列をハードコードした同じ
## MakeMatGF8/MatToPermGF8 関数で cert枠を再構成しているため、sigma=()の
## もとでは左辺 sigma*WordEval(w,Xperm,Yperm)*sigma^-1 と右辺
## WordEval(w,Xperm_cert,Yperm_cert) が同一関数・同一引数の同一式になり、
## WordEvalにどんな規約バグがあっても54/54になる無内容検査だったと判定
## された(事故台帳#6型の同一ワークストリーム内2回目)。実装のやり直しは
## 不要(集合一致の結論はfalsifierの独立再構成が既に支持している)-- ここ
## では記述の正直化のみ行う。v1/v2/v3は不改変。旧metadata certはv1の
## ままsearch/certs/nf972_sourcemap_b_20260804.jsonに残し、本v4を新名で
## 追加する。
#############################################################################
Print("\n=== v4出力: CV-9判読3点の記述訂正(v1/v2/v3不改変・新名) ===\n");
OUT_V4_PATH := "search/certs/nf972_sourcemap_b_v4_20260804.json";;

freezeSpecSha := ComputeSha256FileB("docs/notes/nf972_freeze_v1.md");;
k9CertSha := ComputeSha256FileB(K9_CERT_PATH);;
s4CertSha := ComputeSha256FileB(S4_CERT_PATH);;
Print("  freeze_spec_sha256=", freezeSpecSha, "\n");
Print("  k9_cert_sha256=", k9CertSha, "\n");
Print("  s4_cert_sha256=", s4CertSha, "\n");

certV4 := Concatenation(
  "{\n",
  "  \"schema\":\"nf972-sourcemap-b/v4\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/nf972_sourcemap_b_run.g\",\n",
  "  \"design_doc\":\"docs/notes/nf972_freeze_v1.md(裁定434凍結+v1.1裁定442+v1.2裁定454)\",\n",
  "  \"card_label\":\"NF-972 source map B(直接悉皆側・独立実装・A非参照)-- v4: CV-9判読3点の記述訂正版\",\n",
  "  \"supersedes_note\":\"tuples自体(972点・can9/can4値)はv1/v2/v3から不変(CV-9判読で3版逐語同一を確認済み)。本v4はmetadata cert(nf972_sourcemap_b_20260804.json)の記述訂正のみ -- 旧metadata certは不改変のまま残す。\",\n",
  "  \"cv9_reading_ref\":\"docs/notes/nf972_cv9_reading_v1.md\",\n",
  "  \"independence_note\":\"source map A(組立側)の実装・中間表現・normalizer helperを一切参照・共有しない。共有は凍結仕様のschemaのみ。列挙戦略はihnec_r4b_run.gと同型(Elements(DerivedSubgroup(G))直接列挙)だが判定関数(NF972HexagonOK)・NF化(q9/q4評価・can9/can4・serialization)はすべて自前実装で、R4bのScanRoofHexagonコード自体は再利用していない。\",\n",
  "  \"can9_can4_design_note\":\"can9=27点を9点x3ブロックに分解しD_9=<r,s>正規形(a,eps)の3つ組(固定順)。can4=9点one-line image(v3以降はsigma適用後・sigma=()と確認済み)。\",\n",
  "  \"bug_fix_note\":\"v1.1追補(裁定442)の辞書自己検査を実施中、K9側は108/108一致もS4側は当初6/54しか一致しないことが判明。原因はmarking/座標系ではなくNF972HexagonOKの乗算規約バグ(ymf/hex311/genB/zEltがplainなGAP `*`でAbstractProd反転規約と不一致)。修正済み。詳細はops/express/20260804_implementer_nf972b_predicate_bug_found.md。\",\n",
  "  \"dictionary_selfcheck\":{\n",
  "    \"design_doc\":\"docs/notes/nf972_freeze_v1.md v1.2追補(裁定454)SS7-6\",\n",
  "    \"q9_dictionary_type\":\"identity\",\n",
  "    \"q9_projection_matches_k9_cert_f_triple_verbatim\":", JB(dictK9OK), ",\n",
  "    \"q9_selfcheck_status\":\"valid(非トートロジー -- K9.v1.jsonのf_triple欄は自分の計算に由来しない独立な格納値)\",\n",
  "    \"q4_dictionary_type\":\"conjugation_by_sigma_via_marked_generator_correspondence(sigma=() と機械決定・一意性確認済み)\",\n",
  "    \"q4_cert_frame_image_comparison_flag\":", JB(dictS4OK), ",\n",
  "    \"q4_self_check_status\":\"tautological -- see nf972_cv9_reading_v1.md 【重大1】; set-level agreement is instead supported by falsifier's independent reconstruction. sigma=()のため左辺sigma*WordEval(w,Xperm,Yperm)*sigma^-1と右辺WordEval(w,Xperm_cert,Yperm_cert)はcert枠がXperm,Yperm自体と同じ構成関数(MakeMatGF8/MatToPermGF8)から同一引数で再構成されている結果、同一関数・同一引数の同一式になっており、WordEvalの規約バグを検出できない(事故台帳#6型)。上のflag(q4_cert_frame_image_comparison_flag)はこの無内容な式の評価結果であり、証拠として引用しない。\",\n",
  "    \"caveat\":\"q4_cert_frame_image_comparison_flag=trueは『54/54が式として一致した』という事実のみを示し、can4のcert枠一致を独立に裏付けるものではない。can4の正しさの根拠はfalsifierによる独立再構成(nf972_cv9_reading_v1.md)である。\"\n",
  "  },\n",
  "  \"windows\":{\n",
  "    \"g9_size\":", String(K9sz), ",\"k9_ord\":", String(K9ord), ",\n",
  "    \"p_size\":", String(Psz), ",\"n_s4_ord\":", String(Pord), ",\n",
  "    \"gm_size\":", String(Size(GM)), ",\"m_ord\":", String(Mord), "\n",
  "  },\n",
  "  \"anchors\":{\n",
  "    \"k9_alone_shadow_total\":", String(Length(resK9anchor.shadows)), ",\"k9_alone_expected\":108,\n",
  "    \"s4_alone_shadow_total\":", String(Length(resS4anchor.shadows)), ",\"s4_alone_expected\":54\n",
  "  },\n",
  "  \"fixtures\":{\n",
  "    \"fixture1_orientation_flip_fires\":", JB(Fixture1Fires), ",\n",
  "    \"fixture2_q4_side_generator_swap_fires\":", JB(Fixture2Fires), ",\n",
  "    \"fixture3_wrong_modulus_fires\":", JB(Fixture3Fires), ",\n",
  "    \"conv_fixture_a5_s4_pass\":", JB(convFixtureS4Pass), ",\n",
  "    \"conv_fixture_a5_k9_pass\":", JB(convFixtureK9Pass), "\n",
  "  },\n",
  "  \"main_scan\":{\n",
  "    \"derived_order\":", String(resM.derived_order), ",\"derived_order_expected\":367416,\n",
  "    \"shadow_total\":", String(Length(resM.shadows)), ",\"shadow_total_expected\":972\n",
  "  },\n",
  "  \"nf_tuple_set\":{\n",
  "    \"total_tuples\":", String(Length(NFStrings)), ",\n",
  "    \"distinct_tuples\":", String(Length(NFStringsSet)), ",\n",
  "    \"duplicate_count\":", String(dupCount), ",\n",
  "    \"matches_972_0dup\":", JB(Length(NFStringsSet) = 972 and dupCount = 0), "\n",
  "  },\n",
  "  \"projections\":{\n",
  "    \"proj9_q9_side_size\":", String(Length(Proj9Strings)), ",\"proj9_expected\":108,\"proj9_ok\":", JB(proj9OK), ",\n",
  "    \"proj4_q4_side_size\":", String(Length(Proj4Strings)), ",\"proj4_expected\":54,\"proj4_ok\":", JB(proj4OK), ",\n",
  "    \"compatibility_k9_alone_eq_proj9\":", JB(compat9OK), ",\n",
  "    \"compatibility_s4_alone_eq_proj4\":", JB(compat4OK), "\n",
  "  },\n",
  "  \"canonical_enumeration\":{\n",
  "    \"sort_order\":\"gap_String_sort_of_serialized_tuple\",\n",
  "    \"serialization_format\":\"(m0;a1,eps1,a2,eps2,a3,eps3;i1,...,i9)\",\n",
  "    \"count\":", String(Length(SortedNFStrings)), ",\n",
  "    \"sha256\":", JStr(CanonicalSha256), ",\n",
  "    \"note\":\"v1/v2/v3のtuples集合(sha256同一)と一致 -- CV-9判読で3版逐語同一確認済み。\"\n",
  "  },\n",
  "  \"conventions_used\":{\n",
  "    \"conventions_ver\":\"v1_6\",\n",
  "    \"perm_composition\":\"gap_native_right_action\",\n",
  "    \"reduced_hexagon_predicate\":\"NF972HexagonOK(本driver独自実装・数学的判定式・乗算規約ともihnec_r4b_run.gのScanRoofHexagonとAbstractProd経由で同一。当初plain `*`で書いており規約が食い違っていたバグを修正済み -- bug_fix_note参照。\",\n",
  "    \"independence_note\":\"source map A の実装・出力(nf972_sourcemap_a_*.json)は一切読まない。G9・P・GMはGAPで生成器から新規構築。certificates/K9.v1.json・certificates/S4.v2.json は辞書自己検査/枠定義の読解のために読む(A非参照の原則とは別枠・司令塔指示による)。\"\n",
  "  },\n",
  "  \"cross_checked_status\":{\"status\":\"n/a\",\"reason\":\"本certは source map B 単独の出力。source map A との集合突合は司令塔が別途実施する。can4の集合一致の根拠はq4_self_check_statusに明記の通りfalsifierの独立再構成であり、本cert内のtautological flagではない。\"},\n",
  "  \"source_digests\":{\n",
  "    \"note\":\"仕様v1.2 SS3-3で義務化された出所digest。\",\n",
  "    \"freeze_spec_path\":\"docs/notes/nf972_freeze_v1.md\",\n",
  "    \"freeze_spec_sha256\":", JStr(freezeSpecSha), ",\n",
  "    \"k9_cert_path\":", JStr(K9_CERT_PATH), ",\n",
  "    \"k9_cert_sha256\":", JStr(k9CertSha), ",\n",
  "    \"s4_cert_path\":", JStr(S4_CERT_PATH), ",\n",
  "    \"s4_cert_sha256\":", JStr(s4CertSha), "\n",
  "  },\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"wall_ms_total\":", String(GAPLIB_WallElapsedMs()), "\n",
  "  },\n",
  "  \"driver_done\":true,\n",
  "  \"driver_done_marker\":\"NF972_SOURCEMAP_B_DRIVER_DONE\"\n",
  "}\n");;

WriteFile(OUT_V4_PATH, certV4);;
Print("  Wrote ", OUT_V4_PATH, "\n");

#############################################################################
## ---- v5出力(小委嘱: 便102 F102-2.2・規約台帳 v1.6 準拠 conventions_used) ----
## 【申告】v4のconventions_usedはconventions_ver等の独自欄のみで、台帳v1.6
## (docs/notes/conventions_ledger_v1.md SS2)の必須欄(ledger_version・
## effective_source(_chain)・roundtrip_witness・separation・chi_P_criterion・
## level等)を欠いていた(conventions_verはledger_versionの代用にならない)。
## v4は不改変。tuples(972点・sha256)も不変。以下、台帳v1.6の live schema
## (SS2)に沿って欠落欄を補完する。該当しない欄は正直にn/a(scalar)または
## 型つきn/a(object/array・規範8)とする -- 本driverは単系統(source map B)
## の出力であり、A(python)との突合そのものは司令塔が別途行うため
## comparison_target等は「certとcert枠の別経路突合」を対象として記入する。
#############################################################################
Print("\n=== v5出力: 規約台帳v1.6準拠 conventions_used supplement ===\n");
OUT_V5_PATH := "search/certs/nf972_sourcemap_b_v5_20260804.json";;
ledgerSha := ComputeSha256FileB("docs/notes/conventions_ledger_v1.md");;
Print("  ledger_sha256=", ledgerSha, "\n");

# roundtrip_witness: fixture1(向き反転)の非自己逆元witness(実データから1件)
rtWitness := NonSelfInvSample[1];;
rtWitnessLabelBefore := NFTupleSerialize(NFTupleOf(rtWitness, false, 0));;
rtWitnessLabelAfter := NFTupleSerialize(NFTupleOf(rtWitness, true, 0));;

certV5 := Concatenation(
  "{\n",
  "  \"schema\":\"nf972-sourcemap-b/v5\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/nf972_sourcemap_b_run.g\",\n",
  "  \"design_doc\":\"docs/notes/nf972_freeze_v1.md(裁定434/442/454)+docs/notes/conventions_ledger_v1.md(v1.6)\",\n",
  "  \"card_label\":\"NF-972 source map B -- v5: 規約台帳v1.6準拠 conventions_used supplement(便102 F102-2.2委嘱)\",\n",
  "  \"supplement_note\":\"v4(search/certs/nf972_sourcemap_b_v4_20260804.json)は不改変。tuples(972点・v1/v2/v3のsha256=", CanonicalSha256, ")も不変。本v5はconventions_usedブロックを台帳v1.6 SS2 live schemaへ準拠させる補完のみを行う。自己検査flagのtautological注記(v4で正直化済み)は本ファイルのdictionary_selfcheckにも維持する。\",\n",
  "  \"a_side_note\":\"A v3 cert の fixture 説明に『3 mutants』という文言が残っているが実物は4 fixture(orientation flip・generator swap・wrong modulus・AbstractProd conv fixture)である旨、便102 F102-2.2 で non-blocking の文言修正として指摘済み。A側ファイルは一切参照・変更していない -- 本注記は司令塔便の伝聞記録に留まる。\",\n",
  "  \"dictionary_selfcheck\":{\n",
  "    \"q9_projection_matches_k9_cert_f_triple_verbatim\":", JB(dictK9OK), ",\n",
  "    \"q9_selfcheck_status\":\"valid(非トートロジー -- K9.v1.jsonのf_triple欄は自分の計算に由来しない独立な格納値)\",\n",
  "    \"q4_cert_frame_image_comparison_flag\":", JB(dictS4OK), ",\n",
  "    \"q4_self_check_status\":\"tautological -- see nf972_cv9_reading_v1.md【重大1】; set-level agreement is instead supported by falsifier's independent reconstruction. 本flagは証拠として引用しない(v4で正直化済み・v5でも維持)。\"\n",
  "  },\n",
  "  \"conventions_used\":{\n",
  "    \"ledger_version\":\"conventions_ledger_v1_6\",\n",
  "\n",
  "    \"perm_composition\":\"gap_native_right\",\n",
  "    \"conjugation\":\"paper_inn_g_X_g_inv\",\n",
  "    \"conjugation_note\":\"can4'(perm9):=one-line(sigma*perm9*sigma^-1) -- sigma=()と確定済みのため本cert内では恒等作用だが、式の形はInn_sigma(X)=sigma*X*sigma^-1(paper記法)である。\",\n",
  "    \"coset_object\":\"n/a\",\n",
  "    \"action_side\":\"OnRight\",\n",
  "    \"action_side_note\":\"can9/can4のq9,q4評価はGAPのj^perm(右作用)による9/27点上の置換制限(BlockRestrict)。\",\n",
  "    \"coset_side_derivation\":\"n/a(本driverはcosetを構成しない -- 屋根Mの直接悉皆とq9/q4射影のみ)\",\n",
  "\n",
  "    \"word_eval\":[\n",
  "      { \"layer\":\"f_word_to_permutation\", \"direction\":\"reversed\", \"word_source\":\"cert_json(K9.v1.json f_word / S4.v2.json generation_detail f_word)and internal_gap(WordEval)\" }\n",
  "    ],\n",
  "    \"coarse_of\":\"n/a\",\n",
  "    \"word_of\":\"n/a\",\n",
  "\n",
  "    \"roundtrip_witness\":{\n",
  "      \"mode\":\"sampled\",\n",
  "      \"witnesses\":[\n",
  "        { \"element\":", JStr(Concatenation("m=", String(rtWitness.m), " f=", String(rtWitness.f))),
  "          ,\"is_self_inverse\":false,\n",
  "          \"expected_label\":", JStr(rtWitnessLabelBefore), ",\n",
  "          \"observed_label_after_inversion\":", JStr(rtWitnessLabelAfter), ",\n",
  "          \"source\":\"resM.shadows(屋根Mの直接悉皆・本driver自身の計算・script_sha256参照)\" }\n",
  "      ],\n",
  "      \"result\":", JB(Fixture1Fires), ",\n",
  "      \"note\":\"小宇宙(972点)全列挙ではなくFixtureSample(36件・m値12種にまたがる)からの標本(sampled)。全34件の非自己逆元サンプルでfixture1が発火することは本文のfixturesブロックで確認済み(Fixture1Fires=", JB(Fixture1Fires), ")。\"\n",
  "    },\n",
  "\n",
  "    \"characters\":{ \"status\":\"n/a\", \"reason\":\"本driverはchi_vir/chi_tilde_N型の指標machineryを使わない -- can9/can4の比較はGAP順列の直接等価判定による。\" },\n",
  "    \"opposite\":{ \"map\":\"tau\", \"antihomomorphism\":false, \"codomain\":\"G(同一群への GroupHomomorphismByImages)\",\n",
  "      \"note\":\"tauHomはGAPのGroupHomomorphismByImagesで構成した準同型(反準同型ではない) -- hexagon(3.11)判定式tau^2(y^m f)*tau(y^m f)*(y^m f)=1で使用。\" },\n",
  "\n",
  "    \"comparison_target\":{\n",
  "      \"as_function_of\":\"cert枠(K9.v1.json f_triple / S4.v2.json marking から再構成した点ラベル系)と自表現(本driver独自のG9,Pgrp構成)の関数としてのcan9/can4\",\n",
  "      \"function_a\":{ \"name\":\"NF972HexagonOK + Can9OfPerm27/Can4OfPerm9(自表現)\", \"domain\":\"屋根M(=K9 cap N_S4)の972 shadow\",\n",
  "        \"source_digest\":", JStr(selfSha), " },\n",
  "      \"function_b\":{ \"name\":\"K9.v1.json f_triple(直接格納値)/ cert枠(Xperm_cert,Yperm_cert)でのWordEval再評価\", \"domain\":\"K9.v1.json 108行 / S4.v2.json 54行(pass:true)\",\n",
  "        \"source_digest\":", JStr(k9CertSha), " },\n",
  "      \"normalization_digest\":", JStr(freezeSpecSha), "\n",
  "    },\n",
  "\n",
  "    \"separation\":{\n",
  "      \"included\":true,\n",
  "      \"competitor_universe\":[ \"orientation_flip(f->f^-1)\", \"q4_side_generator_correspondence_swap(GM vs GM2)\", \"wrong_modulus(m mod 9 instead of Z/18)\", \"AbstractProd_convention(A5-CONV: paper AB = GAP B*A)\" ],\n",
  "      \"result\":{ \"matrix\":{ \"orientation_flip_fires\":", JB(Fixture1Fires),
  ", \"generator_swap_fires\":", JB(Fixture2Fires),
  ", \"wrong_modulus_fires\":", JB(Fixture3Fires),
  ", \"conv_fixture_s4_pass\":", JB(convFixtureS4Pass),
  ", \"conv_fixture_k9_pass\":", JB(convFixtureK9Pass), " } },\n",
  "      \"forbidden_values\":{ \"handling\":\"MALFORMED\", \"list\":[ \"line\" ] },\n",
  "      \"dummy_fixture\":{\n",
  "        \"id\":\"nf972-b-fixture2-q4-generator-swap\",\n",
  "        \"normalised_input\":\"m in Fixture2MVals(", JArr(List(Fixture2MVals,String)), ")・GM2(q4側generator対応入替)由来のshadow\",\n",
  "        \"normalised_output\":\"NFTupleSerialize(m0,can9,can4)\",\n",
  "        \"discriminating_power\":{ \"input_layer_novel\":true, \"output_layer_novel\":true },\n",
  "        \"expected\":\"baseline(GM)とtuple集合が不一致になる\",\n",
  "        \"observed\":", JB(Fixture2Fires), ",\n",
  "        \"verdict\":", JStr(PF(Fixture2Fires)), "\n",
  "      }\n",
  "    },\n",
  "\n",
  "    \"chi_P_criterion\":{\n",
  "      \"value\":\"exact\",\n",
  "      \"justification\":\"exact = generator/orientationを固定した場合にのみ許す -- 本driverはXperm,Yperm(GF(8)行列S,Tから決定的に構成)・g9.x,g9.y(MakeGn(9)から決定的に構成)というmarked生成元を固定しており、tupleの一致判定はGAP順列/整数の完全等価(conjugacy classへの粗視化は行わない)。\",\n",
  "      \"generator_fixed\":true,\n",
  "      \"orientation_fixed\":true\n",
  "    },\n",
  "\n",
  "    \"representative_vs_invariant\":{\n",
  "      \"exact_representative\":{ \"value\":\"can9/can4のtuple文字列(NFTupleSerialize)\",\n",
  "        \"depends_on\":{ \"model_id\":", JStr(selfSha), ", \"uniformizer_id\":\"r,s(MakeDn(9)) / Xperm,Yperm(GF(8))\",\n",
  "          \"orientation\":\"AbstractProd反転規約(paper AB = GAP B*A)\", \"lift\":\"n/a(整数持上げなし・有限群のみ)\" } },\n",
  "      \"invariants\":{ \"class\":\"shadow_total\", \"order\":\"972(屋根M全体) / 108(K9側射影) / 54(S4側射影)\" }\n",
  "    },\n",
  "\n",
  "    \"effective_source_chain\":[\n",
  "      { \"role\":\"original\", \"path\":\"docs/notes/nf972_freeze_v1.md\", \"sha256\":", JStr(freezeSpecSha), " },\n",
  "      { \"role\":\"current\",  \"path\":\"docs/notes/nf972_freeze_v1.md\", \"sha256\":", JStr(freezeSpecSha), " }\n",
  "    ],\n",
  "    \"effective_source_chain_note\":\"このcertが実装する仕様(interface)の出所連鎖。入力certであるK9.v1.json/S4.v2.jsonの出所はsource_digestsブロック(v4から継承)に記録済み(effective_source_chainは連鎖内の1entryあたり1 artifactの規約に沿い、仕様spec自体のみをここに置く)。\",\n",
  "    \"effective_source\":{ \"path\":\"docs/notes/nf972_freeze_v1.md\", \"sha256\":", JStr(freezeSpecSha), " },\n",
  "\n",
  "    \"seal_recoverability\":{ \"status\":\"n/a\", \"reason\":\"本certは封印fixtureを使用しない。\" },\n",
  "\n",
  "    \"level\":\"PB3\"\n",
  "  },\n",
  "  \"source_digests\":{\n",
  "    \"freeze_spec_path\":\"docs/notes/nf972_freeze_v1.md\",\"freeze_spec_sha256\":", JStr(freezeSpecSha), ",\n",
  "    \"k9_cert_path\":", JStr(K9_CERT_PATH), ",\"k9_cert_sha256\":", JStr(k9CertSha), ",\n",
  "    \"s4_cert_path\":", JStr(S4_CERT_PATH), ",\"s4_cert_sha256\":", JStr(s4CertSha), ",\n",
  "    \"ledger_path\":\"docs/notes/conventions_ledger_v1.md\",\"ledger_sha256\":", JStr(ledgerSha), "\n",
  "  },\n",
  "  \"canonical_enumeration_ref\":{\n",
  "    \"note\":\"tuples本体は不変(v1/v2/v3と同一) -- 972点・重複0。\",\n",
  "    \"sha256\":", JStr(CanonicalSha256), ",\"count\":972\n",
  "  },\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"wall_ms_total\":", String(GAPLIB_WallElapsedMs()), "\n",
  "  },\n",
  "  \"driver_done\":true,\n",
  "  \"driver_done_marker\":\"NF972_SOURCEMAP_B_DRIVER_DONE\"\n",
  "}\n");;

WriteFile(OUT_V5_PATH, certV5);;
Print("  Wrote ", OUT_V5_PATH, "\n");

#############################################################################
## ---- v6以降について ----
## 【重大な申告】v6(便103 F103-7対応)は当初この本driver内に追記して生成
## しようとしたが、本driverはv1〜v5すべてを毎回re-writeする構造(単一の
## 継続実行の中でv1,v2,v3,v4,v5,v6を順に書き出す)であり、GAPLIB_WallElapsedMs()
## 由来のwall_ms_total・selfSha(本ファイル自身のsha256 -- v6のコード追加で
## 必ず変化する)が実行の度に変わるため、「v5以前は不改変」という要求を
## 本driverの実行そのものが構造的に破ってしまうことが分かった(実際に
## 発生: v6追記後の再走でv4/v5のwall_ms_total・script_sha256が変化し、
## 司令塔/Sol便103が引用したv4のsha256 a6b412845adf119c80ebf77ab33d118cd47b40d84370f58d8c081d073d6f8b4c
## と一致しなくなった -- git commit 4ebe384(裁定461)の内容へ復元し直し、
## 差分はcommit後の再走によるtiming/self-hashの変化のみであることを確認
## 済み)。よってv6以降のsupplementは、本driverを再実行せず、既存の
## v4/v5/tuples-v3ファイルを読むだけの別ツール(search/probe/wac_v1/
## nf972_sourcemap_b_v6_gen.py)で生成する(新規の数学計算はゼロ -- 既存
## JSONの再構造化とsha256再計算のみのため、GAP再実行によるmutationリスク
## を避けてpythonで実装する判断)。
#############################################################################
Print("\nNF972_SOURCEMAP_B_DRIVER_DONE\n");
QUIT;
