#############################################################################
## search/probe/wac_v1/ent1_search_20260801.g
## 標的 ENT-1(docs/notes/roof2_cv9_freeze_v1.md SS7.4・裁定400起票承認)。
##
## 何をするか: N' <| B3, N' subseteq K^(3), [K^(3):N']=3, PB3/N' が G_3 の
## 非分裂 chi_i-拡大(位数324)であるものを、`lins`(low index normal
## subgroups)で B3 の指数 1944(=6*324)の正規部分群を悉皆列挙し、その中から
## K^(3) の下に落ちるものへ絞り込むことで探す。見つかれば
##   M_ENT := K^(9) cap N',  |PB3/M_ENT| = 8748
## が「工房初の本質的entangled屋根」の候補になる(freeze SS7.4)。見つからなければ
## 「この宇宙(index<=1944・lins v0.9・Firth-Holt法)でbounded陰性」として正直に
## 記帳する(silent cap禁止)。
##
## 宇宙の事前登録: 指数上限 = 1944(freeze SS7.4が名指しした値。B3の指数6・324)。
## これより広い宇宙は探索しない(指示範囲を勝手に広げない)。もし1944が重すぎる
## ことが判明したら実装せず司令塔へ報告する設計だったが、実測ではB3(2生成子
## 1関係子のfp群)へのLowIndexNormalSubgroupsSearchForIndexは指数1944まで
## 約25秒で完走した(予備計測 scratchpad/ent1_lins_timing.g)ので上限は下げていない。
##
## 手法(freeze SS7.4 が名指しした方法をそのまま実装):
##  (1) B3 = <s1,s2 | s1s2s1=s2s1s2> をfp群として構成。
##  (2) LowIndexNormalSubgroupsSearchForIndex(B3, 1944, infinity) で指数
##      ちょうど1944のB3-正規部分群を悉皆列挙(lins v0.9・Firth-Holt法)。
##  (3) 各候補 N' について:
##      (3a) N' subseteq PB3 か(= 商 B3/N' が rho: B3->S3(s1->(12),s2->(23))
##           を経由するか)を GroupHomomorphismByImages の well-defined性で判定。
##      (3b) PB3 の像 H := <xbar,ybar,cbar>(xbar=s1bar^2, ybar=s2bar^2,
##           cbar=(s1bar s2bar s1bar)^2 -- week1-定義ノート SS(x:=sigma1^2,
##           y:=sigma2^2, c:=Delta^2, Delta:=sigma1sigma2sigma1) の位数が
##           ちょうど324か。
##      (3c) H から G_3(=MakeGn(3)、|G_3|=108)への
##           GroupHomomorphismByImages(H, G3, [xbar,ybar,cbar],
##             [g3.x, g3.y, Identity(G3)]) が well-defined かつ全射かつ核の
##           位数が3か(= N' subseteq K^(3) かつ [K^(3):N']=3 の必要十分条件 --
##           K^(3)は「xbar->g3.x, ybar->g3.y, cbar->1」という特定の写像の核として
##           定義されるので、この写像がH上well-definedであること自体がN'がK^(3)
##           に含まれることの証拠になる。裏付け: 同一パイプラインで指数648を
##           走査すると K^(3) 自身(核位数1の場合)がちょうど1件だけ一意に
##           再現される -- scratchpad/ent1_probe8_anchor.g・下記 anchor 節)。
##      (3d) 通過したものについて、核 B0(位数3)がHの中で分裂するか
##           (=B0を補う位数108の部分群がHにあるか)を
##           ConjugacyClassesSubgroups(H) の悉皆走査で機械判定。
##           非分裂ならENT-1の実物候補。
##
## 自己検査アンカー(本探索の前に必須): 指数648での同一パイプラインが
## K^(3)自身(H->G3が同型・核位数1)をちょうど1件だけ再現することを
## fail-closedにassertする(scratchpad/ent1_probe8_anchor.gで確認済みの結果を
## 本driver内でも再現・cert同梱)。
##
## 独立性・分離の注意: 本probeはsearch側(探索器)。MakeGn(3)はG_3の生成器の
## 「定義」(week1-定義ノート.md記載の閉じた式)であって、既存の照合済み証明書
## を読んでいるわけではない -- 生成器から新規にGAPで構築している。照合器
## (crosscheck/)は別途本certだけを入力に独立実装で再計算すること(本probeの
## コード・中間結果はimportしない)。
##
## 罠の回避(Sol警告6件・裁定的12件): 指数一致(|PB3img|=324など)だけをsettled
## 証明に使わない -- 判定は必ず(3c)の写像well-definedness+核位数+(3d)の
## 分裂検査まで通す。PB3/Nを安易にA(x,x,x)⊗Qへ直積分解しない(ここでは
## H全体でConjugacyClassesSubgroupsするだけで、A/Qへの分解は一切使わない)。
## m の法とuの法は本探索では未使用(この標的はhexagon/charming集合を扱わない)。
## GAPの部分群比較(IsSubgroup)でなくmarked factor map(3c の具体的生成子対応)
## で判定している。
##
## 実行: .\gap.ps1 search\probe\wac_v1\ent1_search_20260801.g
## commitしない(実装係の作業指示どおり)。
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

LoadPackage("lins");;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_ent1_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then
    Error("ent1_search: ComputeSha256File: sha256sum did not return a hash line for ", relpath);
  fi;
  return line{[1 .. 64]};
end;;

#############################################################################
## ---- B3, PB3 generators, G_3 target (all newly constructed -- no certs read) ----
#############################################################################
Print("=== B3 = <s1,s2 | s1s2s1=s2s1s2> ===\n");
F := FreeGroup("s1","s2");;
s1f := F.1;; s2f := F.2;;
B3 := F / [ s1f*s2f*s1f*(s2f*s1f*s2f)^-1 ];;
s1 := B3.1;; s2 := B3.2;;
S3 := SymmetricGroup(3);;

g3 := MakeGn(3);;
Print("|G_3| = ", Size(g3.G), " (expect 108)  ord(x)=", Order(g3.x),
      "  ord(y)=", Order(g3.y), " (both expect 6)\n");
if Size(g3.G) <> 108 or Order(g3.x) <> 6 or Order(g3.y) <> 6 then
  Error("ent1_search: G_3 construction mismatch -- refusing to proceed");
fi;

#############################################################################
## ---- factor-map helper: given a B3-normal subgroup H (index n), build
##      B3/H and test whether it factors through rho:B3->S3 and (if the PB3
##      image has order 324) through the K^(3)-defining map on generators ----
#############################################################################
## PB3-image generators from an ambient quotient's images of s1,s2:
PB3ImageGens := function(b1, b2)
  local xb, yb, cb;
  xb := b1^2;
  yb := b2^2;
  cb := (b1*b2*b1)^2;
  return [xb, yb, cb];
end;;

## Classify one LinsNode's subgroup H <| B3 against the K^(3)-factor test.
## Returns a record with diagnostic fields.
ClassifyCandidate := function(H, expectQuotientOrder)
  local nat, Q, b1, b2, rhoHom, gens, xb, yb, cb, PB3img, ord, k3hom, ker, onto, rec_out;
  nat := NaturalHomomorphismByNormalSubgroup(B3, H);;
  Q := Image(nat);;
  b1 := Image(nat, s1);;
  b2 := Image(nat, s2);;
  rec_out := rec(quotient_order := Size(Q), rho_ok := false, pb3img_order := 0,
                  k3hom_ok := false, k3ker_order := 0, k3_onto := false,
                  matches_k3_window := false);;
  if Size(Q) <> expectQuotientOrder then
    Error("ClassifyCandidate: quotient order mismatch -- universe drift guard");
  fi;
  rhoHom := GroupHomomorphismByImages(Q, S3, [b1,b2], [(1,2),(2,3)]);;
  if rhoHom = fail then
    return rec_out;
  fi;
  rec_out.rho_ok := true;
  gens := PB3ImageGens(b1, b2);;
  xb := gens[1];; yb := gens[2];; cb := gens[3];;
  PB3img := Group(xb, yb, cb);;
  ord := Size(PB3img);;
  rec_out.pb3img_order := ord;;
  k3hom := GroupHomomorphismByImages(PB3img, g3.G, [xb,yb,cb], [g3.x, g3.y, Identity(g3.G)]);;
  if k3hom = fail then
    return rec_out;
  fi;
  rec_out.k3hom_ok := true;;
  ker := Kernel(k3hom);;
  onto := (Image(k3hom) = g3.G);;
  rec_out.k3ker_order := Size(ker);;
  rec_out.k3_onto := onto;;
  rec_out.matches_k3_window := onto;;  # well-defined+onto <=> N' subseteq K^(3)
  rec_out.PB3img := PB3img;;
  rec_out.ker := ker;;
  return rec_out;
end;;

#############################################################################
## ---- self-check anchor: index 648, expect exactly 1 candidate reproducing
##      K^(3) itself (kernel order 1, PB3img order 108, isomorphic to G_3) ----
#############################################################################
Print("\n=== 自己検査アンカー: 指数648でK^(3)自身が一意に再現されるか ===\n");
t0 := Runtime();;
grAnchor := LowIndexNormalSubgroupsSearchForIndex(B3, 648, infinity);;
subsAnchor := ComputedNormalSubgroups(grAnchor);;
t1 := Runtime();;
Print("  index=648 total candidates = ", Length(subsAnchor), "  time_ms=", t1-t0, "\n");

anchorHits := 0;;
for i in [1 .. Length(subsAnchor)] do
  cl := ClassifyCandidate(Grp(subsAnchor[i]), 648);;
  if cl.rho_ok and cl.pb3img_order = 108 and cl.k3hom_ok and cl.k3_onto and cl.k3ker_order = 1 then
    anchorHits := anchorHits + 1;;
  fi;
od;
Print("  K^(3)-matching candidates at index 648 = ", anchorHits, " (expect exactly 1)\n");
anchorOK := (anchorHits = 1);;
if not anchorOK then
  Error("ent1_search: ANCHOR FAILURE -- expected exactly 1 K^(3)-matching candidate at ",
        "index 648, got ", anchorHits, ". Refusing to proceed to the index-1944 search ",
        "with an unverified filter pipeline.");
fi;

#############################################################################
## ---- main search: index 1944 exact, filter for N' subseteq K^(3),
##      [K^(3):N']=3, then split/non-split classification ----
#############################################################################
Print("\n=== 主探索: 指数1944(=6*324)のB3-正規部分群を悉皆列挙(lins) ===\n");
t0 := Runtime();;
gr := LowIndexNormalSubgroupsSearchForIndex(B3, 1944, infinity);;
subs := ComputedNormalSubgroups(gr);;
t1 := Runtime();;
totalCandidates := Length(subs);;
Print("  index=1944 total B3-normal candidates = ", totalCandidates, "  time_ms=", t1-t0, "\n");

rhoOkCount := 0;;      # N' subseteq PB3
pb3img324Count := 0;;  # |PB3img| = 324 (necessary size)
k3windowCount := 0;;   # N' subseteq K^(3), [K^(3):N']=3 (the actual target family)
ent1Hits := [];;       # non-split members of that family

for i in [1 .. Length(subs)] do
  cl := ClassifyCandidate(Grp(subs[i]), 1944);;
  if cl.rho_ok then rhoOkCount := rhoOkCount + 1; fi;
  if cl.rho_ok and cl.pb3img_order = 324 then pb3img324Count := pb3img324Count + 1; fi;
  if cl.rho_ok and cl.pb3img_order = 324 and cl.k3hom_ok and cl.k3_onto and cl.k3ker_order = 3 then
    k3windowCount := k3windowCount + 1;;
    # split/non-split test: does a subgroup of order 108 in PB3img meet ker trivially?
    ccs := ConjugacyClassesSubgroups(cl.PB3img);;
    splitFound := false;;
    for cc in ccs do
      repH := Representative(cc);;
      if Size(repH) = 108 and Size(Intersection(repH, cl.ker)) = 1 then
        splitFound := true;
        break;
      fi;
    od;
    Add(ent1Hits, rec(candidate_index := i, split := splitFound));;
    Print("  K^(3)-window candidate #", i, ": split=", splitFound, "\n");
  fi;
od;

Print("\n=== 集計 ===\n");
Print("  総候補数(index=1944, B3-normal) = ", totalCandidates, "\n");
Print("  N' subseteq PB3(rho経由) = ", rhoOkCount, "\n");
Print("  |PB3像|=324 のもの = ", pb3img324Count, "\n");
Print("  N' subseteq K^(3) かつ [K^(3):N']=3(ENT-1の対象族) = ", k3windowCount, "\n");
nonSplitHits := Filtered(ent1Hits, r -> not r.split);;
Print("  うち非分裂(ENT-1が求める実物) = ", Length(nonSplitHits), "\n");

ent1Exists := (Length(nonSplitHits) > 0);;
Print("\nENT-1 exists (within index<=1944 universe) = ", ent1Exists, "\n");
if ent1Exists then
  VerdictStatus := "exists";;
else
  VerdictStatus := "bounded_negative";;
fi;

#############################################################################
## ---- JSON cert ----
#############################################################################
selfSha := ComputeSha256File("search/probe/wac_v1/ent1_search_20260801.g");;

HitsJson := function(r)
  return Concatenation("{\"candidate_index\":", String(r.candidate_index),
                        ",\"split\":", JB(r.split), "}");
end;;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"ent1-search/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/ent1_search_20260801.g\",\n",
  "  \"card_label\":\"ENT-1(docs/notes/roof2_cv9_freeze_v1.md SS7.4・裁定400起票承認・実装係)\",\n",
  "  \"design_doc\":\"docs/notes/roof2_cv9_freeze_v1.md SS7(IHNEC-GAP-5)・SS7.4 標的ENT-1\",\n",
  "  \"target\":\"N' <| B3, N' subseteq K^(3), [K^(3):N']=3, PB3/N' が G_3 の非分裂 chi_i-拡大(位数324)\",\n",
  "  \"universe\":{\n",
  "    \"note\":\"事前登録: 指数上限=1944(=6*324)。freeze SS7.4が名指しした値そのまま。予備計測(scratchpad/ent1_lins_timing.g)で index<=1944 まで約25秒で完走することを確認済みのため、指定より狭めていない。\",\n",
  "    \"ambient_group\":\"B3 = <s1,s2 | s1s2s1=s2s1s2>(fp群として新規構築)\",\n",
  "    \"index_bound\":1944,\n",
  "    \"index_exact\":true,\n",
  "    \"search_backend\":\"lins package v0.9 (Firth-Holt algorithm), LowIndexNormalSubgroupsSearchForIndex(B3,1944,infinity)\",\n",
  "    \"completeness_caveat\":\"lins v0.9 は Firth-Holt法の実装。本driverはGAPパッケージが返す結果を『指数1944のB3-正規部分群の悉皆列挙』として扱っているが、これはlinsの実装が完全であることへの依存であり、本driver自身がlinsのアルゴリズム完全性を独立に証明したわけではない。\"\n",
  "  },\n",
  "  \"anchor_selfcheck\":{\n",
  "    \"note\":\"指数648でK^(3)自身(核位数1の同型ケース)がちょうど1件だけ再現されることをfail-closedにassert(本探索の分類パイプラインの健全性確認)\",\n",
  "    \"index\":648,\n",
  "    \"total_candidates\":", String(Length(subsAnchor)), ",\n",
  "    \"k3_matching_candidates\":", String(anchorHits), ",\n",
  "    \"expected\":1,\n",
  "    \"pass\":", JB(anchorOK), "\n",
  "  },\n",
  "  \"main_search\":{\n",
  "    \"index\":1944,\n",
  "    \"total_b3_normal_candidates\":", String(totalCandidates), ",\n",
  "    \"factors_through_pb3_rho\":", String(rhoOkCount), ",\n",
  "    \"pb3_image_order_324\":", String(pb3img324Count), ",\n",
  "    \"k3_window_family_count\":", String(k3windowCount), ",\n",
  "    \"k3_window_family_note\":\"N' subseteq K^(3) かつ [K^(3):N']=3 を満たす候補数(=判定式(3c)がwell-defined+全射+核位数3)\",\n",
  "    \"hits\":", JArr(List(ent1Hits, HitsJson)), ",\n",
  "    \"non_split_count\":", String(Length(nonSplitHits)), ",\n",
  "    \"ent1_exists_within_universe\":", JB(ent1Exists), "\n",
  "  },\n",
  "  \"verdict\":{\n",
  "    \"status\":", JStr(VerdictStatus), ",\n",
  "    \"note\":\"status=exists なら non_split_count>0 の候補あり。status=bounded_negative なら index<=1944 の宇宙内では非分裂ENT-1窓は見つからなかった(非存在の証明ではない -- UNKNOWN扱いの陰性)\"\n",
  "  },\n",
  "  \"conventions_used\":{\n",
  "    \"ledger_version\":\"conventions_ledger_v1_3\",\n",
  "    \"perm_composition\":\"gap_native_right_action\",\n",
  "    \"b3_presentation\":\"s1,s2 with relator s1*s2*s1*(s2*s1*s2)^-1 (docs/week1-定義ノート.md: sigma1,sigma2)\",\n",
  "    \"pb3_generators\":\"x:=sigma1^2, y:=sigma2^2, Delta:=sigma1sigma2sigma1, c:=Delta^2 (docs/week1-定義ノート.md 逐語)\",\n",
  "    \"g3_construction\":\"MakeGn(3)(search/week3-battery-common.g、既存 -- ここでは生成器から新規構築、証明書は読まない)\",\n",
  "    \"k3_membership_test\":\"marked factor map: GroupHomomorphismByImages(PB3img, G3, [xbar,ybar,cbar],[g3.x,g3.y,1]) がwell-defined+全射+核位数3であることでN' subseteq K^(3)かつ[K^(3):N']=3を判定(GAPの単純な部分群比較IsSubgroupは使っていない -- 裁定の罠12件『marked factor mapを使う』に対応)\",\n",
  "    \"split_test\":\"ConjugacyClassesSubgroups(PB3img)を悉皆走査し、位数108かつ核と自明交叉の部分群の有無で分裂性を機械判定(ANDの直積分解には依らない)\"\n",
  "  },\n",
  "  \"cross_checked_status\":{\"status\":\"n/a\",\"reason\":\"単系統GAP探索(lins低指数正規部分群探索+marked factor map判定)。cross-checkedを主張しない。照合器(独立実装)による再計算は別途必要\"},\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"lins_version\":", JStr(InstalledPackageVersion("lins")), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"wall_ms_total\":", String(GAPLIB_WallElapsedMs()), "\n",
  "  }\n",
  "}\n");;

WriteFile("search/certs/ent1_search_20260801.json", cert);;
Print("\nWrote search/certs/ent1_search_20260801.json\n");
Print("\nENT1_SEARCH_DONE\n");
QUIT;
