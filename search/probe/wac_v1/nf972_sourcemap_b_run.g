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

s4CertRaw := ParseS4PassingFWords(S4_CERT_PATH);;
Print("  S4.v2.json generation_detail pass:true parsed = ", Length(s4CertRaw), " (expect 54)\n");
S4CertTupleStrings := Set(List(s4CertRaw, r -> Concatenation("(", String(r.m mod Pord), ";",
  JoinC(List(Can4OfPerm9(WordEval(r.fword, Xperm, Yperm)), String), ","), ")")));;

dictK9OK := (K9CertTupleStrings = Proj9Strings);;
dictS4OK := (S4CertTupleStrings = Proj4Strings);;
Print("  辞書適用後 q9射影 = K9.v1.json f_triple 逐語一致 ? ", dictK9OK, "\n");
Print("  辞書適用後 q4射影 = S4.v2.json witness 逐語一致 ? ", dictS4OK, "\n");

if not (dictK9OK and dictS4OK) then
  # fail-closed: 保存して即停止(補正しない)。差分の一部を記録してから Error。
  k9OnlyMine := Difference(Proj9Strings, K9CertTupleStrings);;
  k9OnlyCert := Difference(K9CertTupleStrings, Proj9Strings);;
  s4OnlyMine := Difference(Proj4Strings, S4CertTupleStrings);;
  s4OnlyCert := Difference(S4CertTupleStrings, Proj4Strings);;
  Print("  [INTEGRITY_STOP diag] k9OnlyMine=", Length(k9OnlyMine), " k9OnlyCert=", Length(k9OnlyCert),
        " s4OnlyMine=", Length(s4OnlyMine), " s4OnlyCert=", Length(s4OnlyCert), "\n");
  Error("nf972_sourcemap_b_run: INTEGRITY_STOP -- dictionary self-check failed (K9 match=",
        dictK9OK, " S4 match=", dictS4OK, "). Refusing to write v2 cert. Report to commander.");
fi;
Print("  辞書自己検査 PASS -- 辞書は恒等(自構成の marked 生成元 = cert 側 marked 生成元)。\n");

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
  "  \"supersedes\":\"search/certs/superseded/nf972_sourcemap_b_tuples_20260804_PRE_PREDICATE_FIX.json(canonical_sha256=", JStr(PRE_FIX_CANONICAL_SHA), ")\",\n",
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
## ---- v1.1追補 出力(裁定442 §6 指示4): 辞書経由 tuple v2 + supplement ----
## 辞書=恒等と機械検査済みなので、v2の座標はv1と同一(可能な範囲で明示)。
## supplementに辞書の定義・自己検査結果を記録する。
#############################################################################
Print("\n=== v2出力: 辞書supplement + tuple v2 ===\n");
TUPLES_V2_OUT_PATH := "search/certs/nf972_sourcemap_b_tuples_v2_20260804.json";;

tuplesV2Json := Concatenation(
  "{\n",
  "  \"schema\":\"nf972-sourcemap-b-tuples-v2/v1_1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/nf972_sourcemap_b_run.g\",\n",
  "  \"design_doc\":\"docs/notes/nf972_freeze_v1.md v1.1追補(裁定442)SS6\",\n",
  "  \"note\":\"canonical marking = factor cert座標系(K9.v1.json f_triple・S4.v2.json witness)。辞書は自構成marked生成元(g9.x,g9.y / Xperm,Yperm)とcert側marked生成元の恒等対応(week3-battery-common.gのMakeGn / week3-psl-common.gのRunPSLWindowの生成元構成式がK9.v1.json/S4.v2.jsonの生成スクリプトと同一であることをソースコード比較で確認)。A側の実装・出力は一切参照していない。\",\n",
  "  \"root_cause_note\":\"第1回突合の交わり9/972は座標系未宣言ではなく、本実装のNF972HexagonOK乗算規約バグ(修正はこのスクリプトの冒頭コメントと ops/express/20260804_implementer_nf972b_predicate_bug_found.md に記録)が原因だった。バグ修正後の本走で辞書=恒等の自己検査がPASSした。\",\n",
  "  \"dictionary\":{\n",
  "    \"type\":\"identity\",\n",
  "    \"generator_correspondence\":\"my g9.x<->cert x, my g9.y<->cert y (K9); my Xperm<->cert x, my Yperm<->cert y (S4)\",\n",
  "    \"k9_cert_path\":", JStr(K9_CERT_PATH), ",\n",
  "    \"s4_cert_path\":", JStr(S4_CERT_PATH), ",\n",
  "    \"k9_cert_shadow_count_parsed\":", String(Length(k9CertRaw)), ",\"k9_cert_expected\":108,\n",
  "    \"s4_cert_shadow_count_parsed\":", String(Length(s4CertRaw)), ",\"s4_cert_expected\":54\n",
  "  },\n",
  "  \"dictionary_selfcheck\":{\n",
  "    \"q9_projection_matches_k9_cert_f_triple_verbatim\":", JB(dictK9OK), ",\n",
  "    \"q4_projection_matches_s4_cert_witness_verbatim\":", JB(dictS4OK), ",\n",
  "    \"both_pass\":", JB(dictK9OK and dictS4OK), "\n",
  "  },\n",
  "  \"serialization_format\":\"(m0;a1,eps1,a2,eps2,a3,eps3;i1,...,i9)\",\n",
  "  \"sort_order\":\"gap_String_sort_of_serialized_tuple\",\n",
  "  \"count\":", String(Length(SortedNFStrings)), ",\n",
  "  \"canonical_bytes_sha256\":", JStr(CanonicalSha256), ",\n",
  "  \"tuples\":", JArr(List(SortedNFStrings, JStr)), "\n",
  "}\n");;
WriteFile(TUPLES_V2_OUT_PATH, tuplesV2Json);;
Print("  Wrote ", TUPLES_V2_OUT_PATH, " (", Length(SortedNFStrings), " tuples, dictionary self-check pass=",
      (dictK9OK and dictS4OK), ")\n");

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
  "    \"design_doc\":\"docs/notes/nf972_freeze_v1.md v1.1追補(裁定442)SS6\",\n",
  "    \"dictionary_type\":\"identity(marked生成元対応がcert生成スクリプトと同一構成式であることを確認済み)\",\n",
  "    \"q9_projection_matches_k9_cert_f_triple_verbatim\":", JB(dictK9OK), ",\n",
  "    \"q4_projection_matches_s4_cert_witness_verbatim\":", JB(dictS4OK), "\n",
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
Print("\nNF972_SOURCEMAP_B_DRIVER_DONE\n");
QUIT;
