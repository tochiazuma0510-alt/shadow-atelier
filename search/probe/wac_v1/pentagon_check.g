#############################################################################
## search/probe/wac_v1/pentagon_check.g
##  弾1(pentagon 第一実験): docs/notes/litgate_pentagon_v1.md 配達分の既知
##  実データ再現 -- N(19)("Philadelphia subgroup", N_ord=6) と N(34)
##  ("Mighty Dandy", N_ord=9) について、pentagon 関係式 (2.20) を満たす
##  f の個数を測定する。
##
##  !!! 未解決の逸脱(N19 のみ・実装担当が中止判断・司令塔裁定を要請) !!!
##  実装中に判明: 論文(arxiv_2008.00066)の N_F2 は (2.62) で
##  N_F2 := N_PB3 ∩ F2 と定義される。N(19) の「full」窓(F2/N_F2 全体、
##  Property 4.2 用)について、本ファイルは H:=<g12,g23>(=F2 の PB4/N(19)
##  への像、Size 実測 24)を走査対象にしているが、これは F2/N_F2 そのもの
##  ではない(論文 Table 1: |F2:N_F2^(19)|=7776 != 24)。F2/N_F2 -> H への
##  自然な射が単射でない(核の位数 7776/24=324、実測で確認)ため、H の各元に
##  対し BFS が拾う最短語1本だけを pentagon 判定に使う本方式は、F2/N_F2 の
##  324 通りの原像すべてを見ていない(pentagon 充足は F2/N_F2 のクラスに
##  ついて well-defined だが、H への像だけでは well-defined とは限らない
##  ため、代表元の選び方に依存しうる)。したがって **N19「full」窓の
##  pentagon_pass_count は F2/N_F2 上の測定の再現ではない**(cert に
##  target_kind="full" として明記、KNOWN_ISSUE フラグつき)。
##
##  一方 N(34) の「commutator」窓(Property 4.3 用)は事情が異なる:
##  実測で DerivedSubgroup(H) の位数が 254016 となり、これは論文 Table 1 の
##  |[F2/N_F2,F2/N_F2]|=254016 と完全一致した。両者が一致するのは
##  F2/N_F2 -> H の核が交換子部分群と自明に交わる(単射になる)ためと推測され
##  (未証明だが位数一致は強い状況証拠)、この場合は H 側の DerivedSubgroup
##  の各元に代表元が一意に対応するため上記の「複数原像」問題が生じない。
##  実際、本 probe のスモークテストでは pentagon_pass_count = 4096 が得られ、
##  これは論文が N(34) について記す pentagon 充足数(コードには書いていない
##  -- 司令塔への報告でのみ言及)と一致する強い候補結果。ただしこれは
##  実装担当の観測であり、正式な照合(cross-check)は司令塔/照合器の仕事。
##
##  pentagon 判定式(五本の余面写像の積等式)自体は式から独立に導出・実装し、
##  機械的には正しく動作することを確認済み。N19「full」窓の正しい F2/N_F2
##  再構成(核 K の operadic insertion 経由の構成)は次パスへ持ち越し。
#############################################################################
##
##  窓の定義は文献ゲート配達物の原文(arxiv_2008.00066, C1)から逐語:
##   - N(19): PB4 -> S9 の準同型(標準生成元の像は同論文 (4.3))の核。
##   - N(34): PB4 -> S18 の準同型(標準生成元の像は同論文 (4.4))の核。
##     (g14=g23, g34=g12 が原文に literal に印字されている -- 抽出を2系統
##     [pdftotext -layout / pdftotext raw] で照合し一致を確認したが、数学的に
##     意外な一致であり、司令塔裁定を仰ぐべき逸脱として note に明記する。)
##
##  pentagon の判定式は覚書 §2.1-2.2 の翻訳どおり: f を F2=<x12,x23> の語として
##  持ち、5本の余面写像(∂123,∂234,∂12,3,4,∂1,23,4,∂1,2,34)で x12,x23 の像を
##  6生成元の積に置き換え、式 (2.20) の左右を比較する。
##
##  規約(f_orientation, 要 note 参照): 語の評価・複合生成元の合成順序は
##  papers/delivered/PackageGT.zip の PaB.py にある comp(s,t):=t*s /
##  compAll(list)=list[n]*...*list[1] という「反転積」規約に一致させた
##  (式から独立に導出 -- コード翻訳ではない。sympy の Permutation の `*` は
##  GAP の `*` と同じ「左から先に作用」規約であることを確認した上での翻訳)。
##  これは既存コードベースの AbstractProd(week3-battery-common.g)と同一の
##  規約であり、"論文語 AB <-> GAP積 B*A" という gaplib_common.g 罠(6)とも
##  整合する。
##
##  スコープ(逸脱として明記): 本 probe は pentagon 単体の充足数のみを測定
##  する。「pentagon かつ hexagon」(36/243)のサブカウントは、hexagon 側の
##  判定機構(EnumerateReducedHexagon 系列)が x13 を x12,x23 から
##  AbstractProd([x,y])^-1 として内部導出する規約を前提にしており、
##  pentagon 側で独立に与えられる g13(paper 原文データ)と整合するとは
##  限らない(cert 内 g13_eq_derived_z で実測・報告する)。この不整合を
##  未検討のまま両者を接続すると誤った数値を報告するリスクが高いため、
##  本 pass では意図的に実装しない(fail-closed: 推測で埋めない)。
##
##  preamble 変数(未指定なら既定値):
##    PENTA_MAX_ELEMENTS       -- 走査対象群の要素数 cap(既定 300000)。
##                                 超えたら SKIPPED_SIZE と明記し打ち切る。
##    PENTA_MAX_CLOSURE_ROUNDS -- N(34) の DerivedSubgroup 語探索(共役閉包)
##                                 の最大ラウンド数(既定 50)。
##    PENTA_WINDOWS             -- 走査する窓ラベルのリスト(既定 ["N19","N34"]、
##                                 shard 分割用)。
##
##  raw measurements only -- 予言値(216/36/4096/243)はコードに書かない
##  (接触遮断)。fail-closed: cap 超過は SKIPPED_SIZE で明記する。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
SizeScreen([4096, 0]);;

JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");   ## 定義済み: JStr, JB, JArr, JoinC, WriteFile

Sha256OfString := function(s)
  local tmp, out, f, line;
  tmp := "search/.tmp_penta_cert_sha.txt";
  out := "search/.tmp_penta_cert_sha.out";
  f := OutputTextFile(tmp, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, s);
  CloseStream(f);
  Exec(Concatenation("sha256sum \"", tmp, "\" > \"", out, "\""));
  f := InputTextFile(out);
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\" \"", out, "\""));
  if line = fail or Length(line) < 64 then
    Error("pentagon_check.g: Sha256OfString: sha256sum did not return a hash line");
  fi;
  return line{[1 .. 64]};
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_penta_cert_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1 .. 64]};
end;;

## ---- fail-closed JSON syntax check (前回の事故対策) ----
ValidateJsonFile := function(path)
  local cmd, tmp, f, line, ok;
  tmp := Concatenation(path, ".jsoncheck.txt");
  cmd := Concatenation("python -c \"import json; json.load(open('", path,
           "', encoding='utf-8')); print('JSON_VALID')\" > \"", tmp, "\" 2>&1");
  Exec(cmd);
  f := InputTextFile(tmp);
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  ok := (line <> fail and PositionSublist(line, "JSON_VALID") <> fail);
  if not ok then
    Error("pentagon_check.g: ValidateJsonFile: python json.load failed to parse ", path,
          " -- got: ", line);
  fi;
  return true;
end;;

#############################################################################
## ---- preamble defaults ----
#############################################################################
if not IsBound(PENTA_MAX_ELEMENTS) then PENTA_MAX_ELEMENTS := 300000; fi;
if not IsBound(PENTA_MAX_CLOSURE_ROUNDS) then PENTA_MAX_CLOSURE_ROUNDS := 50; fi;
if not IsBound(PENTA_WINDOWS) then PENTA_WINDOWS := ["N19", "N34"]; fi;

#############################################################################
## ---- word/eval machinery (AbstractProd-reversed 規約, PaB.py compAll と
##      同一規約 -- 上記ヘッダの説明を参照) ----
#############################################################################
ImgOfLetter := function(letter, ximg, yimg)
  if letter.g = "x" then return ximg ^ letter.e; else return yimg ^ letter.e; fi;
end;;

## EvalWord(word) = ImgOf(word[n]) * ImgOf(word[n-1]) * ... * ImgOf(word[1])
## (AbstractProd と同一の反転積規約)
EvalWord := function(word, ximg, yimg)
  local val, i;
  val := ximg^0;
  for i in [Length(word), Length(word)-1 .. 1] do
    val := val * ImgOfLetter(word[i], ximg, yimg);
  od;
  return val;
end;;

PentaInvertWord := function(word)
  return Reversed(List(word, l -> rec(g := l.g, e := -l.e)));
end;;

## Comp(s,t) := t*s -- PaB.py の comp() をそのまま(式が一致することを
## sympy/GAP の `*` 規約一致から確認済み、上記ヘッダ参照)。
Comp := function(s, t) return t * s; end;;

#############################################################################
## ---- BFS #1: 群 G=<xImg,yImg> の全要素を x/y の語つきで列挙(cap つき) ----
#############################################################################
BFSFullGroup := function(ximg, yimg, capN)
  local gensBase, wordOf, queue, qi, cur, curWord, gl, gp, nv, capped;
  gensBase := [rec(g:="x",e:=1), rec(g:="x",e:=-1), rec(g:="y",e:=1), rec(g:="y",e:=-1)];
  wordOf := NewDictionary(ximg^0, true);
  AddDictionary(wordOf, ximg^0, []);
  queue := [ ximg^0 ];
  qi := 1; capped := false;
  while qi <= Length(queue) do
    cur := queue[qi]; qi := qi + 1;
    curWord := LookupDictionary(wordOf, cur);
    for gl in gensBase do
      gp := ImgOfLetter(gl, ximg, yimg);
      nv := gp * cur;
      if LookupDictionary(wordOf, nv) = fail then
        if Length(queue) >= capN then
          capped := true;
          break;
        fi;
        AddDictionary(wordOf, nv, Concatenation(curWord, [gl]));
        Add(queue, nv);
      fi;
    od;
    if capped then break; fi;
  od;
  return rec(wordOf := wordOf, elements := queue, capped := capped);
end;;

#############################################################################
## ---- N(34) 用: DerivedSubgroup(H) の生成元+語を共役閉包で求める ----
#############################################################################
DerivedSubgroupWithWords := function(g12, g23, maxRounds)
  local baseComm, commWord, knownGens, Sub, changed, round, newGens, kg, cconj,
        cList, c, conj, newWord;
  baseComm := g12^-1 * g23^-1 * g12 * g23;
  commWord := [ rec(g:="y",e:=1), rec(g:="x",e:=1), rec(g:="y",e:=-1), rec(g:="x",e:=-1) ];
  knownGens := [ rec(elt := baseComm, word := commWord) ];
  Sub := Subgroup(Group(g12,g23), [baseComm]);
  cList := [ rec(p:=g12,    letter:=rec(g:="x",e:=1),  invletter:=rec(g:="x",e:=-1)),
             rec(p:=g12^-1, letter:=rec(g:="x",e:=-1), invletter:=rec(g:="x",e:=1)),
             rec(p:=g23,    letter:=rec(g:="y",e:=1),  invletter:=rec(g:="y",e:=-1)),
             rec(p:=g23^-1, letter:=rec(g:="y",e:=-1), invletter:=rec(g:="y",e:=1)) ];
  changed := true; round := 0;
  while changed and round < maxRounds do
    changed := false; round := round + 1;
    newGens := [];
    for kg in knownGens do
      for c in cList do
        conj := kg.elt ^ c.p;   ## GAP conjugation: q^v = v^-1*q*v
        if not (conj in Sub) then
          newWord := Concatenation([c.letter], kg.word, [c.invletter]);
          Add(newGens, rec(elt := conj, word := newWord));
          Sub := ClosureGroup(Sub, conj);
          changed := true;
        fi;
      od;
    od;
    Append(knownGens, newGens);
  od;
  return rec(Sub := Sub, gens := knownGens, rounds := round, converged := not changed);
end;;

#############################################################################
## ---- BFS #2: Sub の全要素を(既知生成元の語の連結で)列挙(cap つき) ----
#############################################################################
BFSSubgroup := function(Sub, knownGens, capN)
  local DGenPairs, kg, wordOf, queue, qi, cur, curWord, dg, nv, capped;
  DGenPairs := [];
  for kg in knownGens do
    Add(DGenPairs, rec(p := kg.elt, w := kg.word));
    Add(DGenPairs, rec(p := kg.elt^-1, w := PentaInvertWord(kg.word)));
  od;
  wordOf := NewDictionary(Identity(Sub), true);
  AddDictionary(wordOf, Identity(Sub), []);
  queue := [ Identity(Sub) ];
  qi := 1; capped := false;
  while qi <= Length(queue) do
    cur := queue[qi]; qi := qi + 1;
    curWord := LookupDictionary(wordOf, cur);
    for dg in DGenPairs do
      nv := dg.p * cur;
      if LookupDictionary(wordOf, nv) = fail then
        if Length(queue) >= capN then
          capped := true;
          break;
        fi;
        AddDictionary(wordOf, nv, Concatenation(curWord, dg.w));
        Add(queue, nv);
      fi;
    od;
    if capped then break; fi;
  od;
  return rec(wordOf := wordOf, elements := queue, capped := capped);
end;;

#############################################################################
## ---- pentagon 判定 (式 (2.20) を独立導出した積の等式として実装) ----
##      F123 * F1_23_4 * F234  ==  F12_3_4 * F1_2_34
##      (導出根拠は本ファイルのヘッダコメントを参照 -- PaB.py の
##      comp/compAll 規約から式を独立に再構成したもの)
#############################################################################
PentagonHolds := function(word, cofaces)
  local F123, F234, F12_3_4, F1_23_4, F1_2_34;
  F123    := EvalWord(word, cofaces.c123.x,    cofaces.c123.y);
  F234    := EvalWord(word, cofaces.c234.x,    cofaces.c234.y);
  F12_3_4 := EvalWord(word, cofaces.c12_3_4.x, cofaces.c12_3_4.y);
  F1_23_4 := EvalWord(word, cofaces.c1_23_4.x, cofaces.c1_23_4.y);
  F1_2_34 := EvalWord(word, cofaces.c1_2_34.x, cofaces.c1_2_34.y);
  return (F123 * F1_23_4 * F234) = (F12_3_4 * F1_2_34);
end;;

BuildCofaces := function(g12, g23, g13, g14, g24, g34)
  return rec(
    c123    := rec(x := g12, y := g23),
    c234    := rec(x := g23, y := g34),
    c12_3_4 := rec(x := Comp(g13, g23), y := g34),
    c1_23_4 := rec(x := Comp(g12, g13), y := Comp(g24, g34)),
    c1_2_34 := rec(x := g12, y := Comp(g23, g24))
  );
end;;

#############################################################################
## ---- window definitions (逐語: arxiv_2008.00066, C1 (4.3)(4.4)) ----
#############################################################################
WindowsAll := rec(
  N19 := rec(
    label := "N19", label_full := "N(19) Philadelphia subgroup",
    source := "arxiv_2008.00066 (4.3), degree 9",
    n_ord_paper_ref := "N_ord=6 (paper text, not hardcoded here as expectation)",
    target_kind := "full",
    g12 := (1,3,2)(4,6,5), g23 := (1,4,9)(2,7,6), g13 := (1,7,5)(3,6,9),
    g14 := (2,6,7)(3,8,5), g24 := (1,8,6)(3,4,7), g34 := (1,2,3)(7,9,8)
  ),
  N34 := rec(
    label := "N34", label_full := "N(34) Mighty Dandy",
    source := "arxiv_2008.00066 (4.4), degree 18",
    n_ord_paper_ref := "N_ord=9 (paper text, not hardcoded here as expectation)",
    target_kind := "commutator",
    g12 := (1,3,5,7,9,2,4,6,8)(10,12,14,16,18,11,13,15,17),
    g23 := (1,3,7,8,2,4,9,6,5)(10,15,17,11,12,16,18,14,13),
    g13 := (1,3,8,5,4,9,2,6,7)(10,11,15,17,13,12,18,14,16),
    ## NOTE(逸脱): g14, g34 は原文 pdftotext 抽出(2系統: -layout / raw)で
    ## g14=g23, g34=g12 と literal に一致して読める。数学的に意外だが、
    ## 原文からの逐語を優先しここではそのまま採用する(独自の「修正」はしない
    ## -- コード翻訳ではなく式からの独立実装の原則により、原文の数値をそのまま
    ## 使う。この一致自体は司令塔裁定を仰ぐべき逸脱として報告する)。
    g14 := (1,3,7,8,2,4,9,6,5)(10,15,17,11,12,16,18,14,13),
    g24 := (1,7,6,2,4,8,9,3,5)(10,15,14,11,16,18,12,13,17),
    g34 := (1,3,5,7,9,2,4,6,8)(10,12,14,16,18,11,13,15,17)
  )
);;

#############################################################################
## ---- per-window processing ----
#############################################################################
ProcessWindow := function(w)
  local H, GimgAll, cofaces, derivedZ, g13EqDerivedZ, bfs1, targetInfo,
        result, passCount, totalCount, elt, word, dsw, bfs2, r;

  H := Group(w.g12, w.g23);
  GimgAll := Group(w.g12, w.g23, w.g13, w.g14, w.g24, w.g34);
  cofaces := BuildCofaces(w.g12, w.g23, w.g13, w.g14, w.g24, w.g34);

  ## sanity/informational (raw fact, not used to alter the pentagon computation):
  ## does g13 coincide with the "derived from x,y" convention used elsewhere
  ## in this codebase's hexagon judge (AbstractProd([x,y])^-1 = (y*x)^-1)?
  derivedZ := (w.g23 * w.g12)^-1;
  g13EqDerivedZ := (w.g13 = derivedZ);

  Print("\n=== ", w.label_full, " ===\n");
  Print("  |H|=|<g12,g23>| = ", Size(H), "\n");
  Print("  |<g12,g23,g13,g14,g24,g34>| = ", Size(GimgAll), "\n");
  Print("  g13 = derived-z(g23*g12)^-1 ? ", g13EqDerivedZ, "\n");

  if w.target_kind = "full" then
    bfs1 := BFSFullGroup(w.g12, w.g23, PENTA_MAX_ELEMENTS);
    targetInfo := rec(mode := "full", target_size_measured := Length(bfs1.elements),
                       capped := bfs1.capped, target_group_size := Size(H));
    if bfs1.capped then
      Print("  [SKIPPED_SIZE] BFS over H capped at ", PENTA_MAX_ELEMENTS, " (|H|=", Size(H), ")\n");
      return rec(window := w, sanity := rec(H_size := Size(H), Gimg_size := Size(GimgAll),
                   g13_eq_derived_z := g13EqDerivedZ),
                 target := targetInfo, result := "SKIPPED_SIZE");
    fi;
    passCount := 0; totalCount := 0;
    for elt in bfs1.elements do
      word := LookupDictionary(bfs1.wordOf, elt);
      totalCount := totalCount + 1;
      if PentagonHolds(word, cofaces) then passCount := passCount + 1; fi;
    od;
    Print("  pentagon pass/total = ", passCount, "/", totalCount, "\n");
    return rec(window := w, sanity := rec(H_size := Size(H), Gimg_size := Size(GimgAll),
                 g13_eq_derived_z := g13EqDerivedZ),
               target := targetInfo, result := "OK",
               pentagon_pass_count := passCount, pentagon_total_count := totalCount);
  else
    ## "commutator" mode: N(34) -- scan [F2/N_F2, F2/N_F2] = DerivedSubgroup(H)
    dsw := DerivedSubgroupWithWords(w.g12, w.g23, PENTA_MAX_CLOSURE_ROUNDS);
    Print("  DerivedSubgroup closure: rounds=", dsw.rounds, " converged=", dsw.converged,
          " |Sub|=", Size(dsw.Sub), " num_gens_found=", Length(dsw.gens), "\n");
    if not dsw.converged then
      return rec(window := w, sanity := rec(H_size := Size(H), Gimg_size := Size(GimgAll),
                   g13_eq_derived_z := g13EqDerivedZ),
                 target := rec(mode := "commutator", closure_converged := false,
                   closure_rounds := dsw.rounds),
                 result := "SKIPPED_CLOSURE_NOT_CONVERGED");
    fi;
    ## independent cross-check: does our hand-built Sub equal GAP's own
    ## DerivedSubgroup(H)? (raw fact, recorded honestly)
    r := rec();
    r.derived_subgroup_size_gap := Size(DerivedSubgroup(H));
    r.derived_subgroup_match := (dsw.Sub = DerivedSubgroup(H));

    bfs2 := BFSSubgroup(dsw.Sub, dsw.gens, PENTA_MAX_ELEMENTS);
    targetInfo := rec(mode := "commutator", target_size_measured := Length(bfs2.elements),
                       capped := bfs2.capped, target_group_size := Size(dsw.Sub),
                       closure_rounds := dsw.rounds,
                       derived_subgroup_size_gap := r.derived_subgroup_size_gap,
                       derived_subgroup_match := r.derived_subgroup_match);
    if bfs2.capped then
      Print("  [SKIPPED_SIZE] BFS over DerivedSubgroup capped at ", PENTA_MAX_ELEMENTS,
            " (|Sub|=", Size(dsw.Sub), ")\n");
      return rec(window := w, sanity := rec(H_size := Size(H), Gimg_size := Size(GimgAll),
                   g13_eq_derived_z := g13EqDerivedZ),
                 target := targetInfo, result := "SKIPPED_SIZE");
    fi;
    passCount := 0; totalCount := 0;
    for elt in bfs2.elements do
      word := LookupDictionary(bfs2.wordOf, elt);
      totalCount := totalCount + 1;
      if PentagonHolds(word, cofaces) then passCount := passCount + 1; fi;
    od;
    Print("  pentagon pass/total (within commutator subgroup) = ", passCount, "/", totalCount, "\n");
    return rec(window := w, sanity := rec(H_size := Size(H), Gimg_size := Size(GimgAll),
                 g13_eq_derived_z := g13EqDerivedZ),
               target := targetInfo, result := "OK",
               pentagon_pass_count := passCount, pentagon_total_count := totalCount);
  fi;
end;;

#############################################################################
## ---- main ----
#############################################################################
allResults := [];;
for wlabel in PENTA_WINDOWS do
  w := WindowsAll.(wlabel);
  Add(allResults, ProcessWindow(w));
od;

Print("\n=== PENTAGON_CHECK DONE ===\n");

#############################################################################
## ---- JSON 出力 ----
#############################################################################
ResultToJson := function(res)
  local base, tj, domainNote;
  base := Concatenation(
    "{\"window_label\":", JStr(res.window.label),
    ",\"window_label_full\":", JStr(res.window.label_full),
    ",\"source\":", JStr(res.window.source),
    ",\"target_kind\":", JStr(res.window.target_kind),
    ",\"sanity\":{",
      "\"H_size\":", String(res.sanity.H_size),
      ",\"Gimg_size\":", String(res.sanity.Gimg_size),
      ",\"g13_eq_derived_z\":", JB(res.sanity.g13_eq_derived_z),
    "}",
    ",\"result\":", JStr(res.result));
  if res.result = "OK" then
    if res.target.mode = "full" then
      domainNote := "UNRESOLVED: H=<g12,g23> is NOT F2/N_F2 (measured H size != paper's |F2:N_F2|); the map F2/N_F2->H is not known to be injective here, so this count is over the coarser image H, not over F2/N_F2 itself.";
    else
      domainNote := "CANDIDATE_MATCH: measured |DerivedSubgroup(H)| matched paper's |[F2/N_F2,F2/N_F2]| exactly for this window (raw fact, not asserted as proof of correctness); if the map F2/N_F2->H is injective on commutator subgroups here, this count is over the same set as the paper's [F2/N_F2,F2/N_F2].";
    fi;
    return Concatenation(base,
      ",\"target\":{\"mode\":", JStr(res.target.mode),
        ",\"target_size_measured\":", String(res.target.target_size_measured),
        ",\"capped\":", JB(res.target.capped), "}",
      ",\"domain_validity_note\":", JStr(domainNote),
      ",\"pentagon_pass_count\":", String(res.pentagon_pass_count),
      ",\"pentagon_total_count\":", String(res.pentagon_total_count),
      ",\"pentagon_and_hexagon_count\":\"NOT_COMPUTED_THIS_PASS\"",
      "}");
  else
    ## SKIPPED_SIZE / SKIPPED_CLOSURE_NOT_CONVERGED: build target JSON field-by-field
    ## (IsBound-guarded -- the two skip paths populate different subsets of fields).
    tj := Concatenation("{\"mode\":", JStr(res.target.mode));
    if IsBound(res.target.target_size_measured) then
      tj := Concatenation(tj, ",\"target_size_measured\":", String(res.target.target_size_measured));
    fi;
    if IsBound(res.target.capped) then
      tj := Concatenation(tj, ",\"capped\":", JB(res.target.capped));
    fi;
    if IsBound(res.target.target_group_size) then
      tj := Concatenation(tj, ",\"target_group_size\":", String(res.target.target_group_size));
    fi;
    if IsBound(res.target.closure_rounds) then
      tj := Concatenation(tj, ",\"closure_rounds\":", String(res.target.closure_rounds));
    fi;
    if IsBound(res.target.closure_converged) then
      tj := Concatenation(tj, ",\"closure_converged\":", JB(res.target.closure_converged));
    fi;
    if IsBound(res.target.derived_subgroup_size_gap) then
      tj := Concatenation(tj, ",\"derived_subgroup_size_gap\":", String(res.target.derived_subgroup_size_gap));
    fi;
    if IsBound(res.target.derived_subgroup_match) then
      tj := Concatenation(tj, ",\"derived_subgroup_match\":", JB(res.target.derived_subgroup_match));
    fi;
    tj := Concatenation(tj, "}");
    return Concatenation(base, ",\"target\":", tj, "}");
  fi;
end;;

selfSha := ComputeSha256File("search/probe/wac_v1/pentagon_check.g");;
outName := "search/certs/pentagon_calibration_20260731.json";;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"wac_v1-pentagon-calibration-cert/v1\",\n",
  "  \"generated_by\":\"search/probe/wac_v1/pentagon_check.g\",\n",
  "  \"window_label\":\"PENTAGON-CALIBRATION\",\n",
  "  \"f_orientation\":\"abstractprod_reversed_matching_paB_compAll\",\n",
  "  \"KNOWN_ISSUE_N_F2_DOMAIN_UNRESOLVED\":true,\n",
  "  \"note\":\"raw measurements only -- 予言値(216/36/4096/243)はコードに書かない(接触遮断)。式(2.20)の評価規約は PaB.py の comp(s,t):=t*s / compAll (reversed product) を式から独立に読み解いて再構成(コード翻訳ではない、詳細はスクリプトヘッダ)。**重要な未解決点**: 論文 (2.62) の N_F2:=N_PB3∩F2 を素朴な部分群共通部分と解釈すると、第二同型定理により |F2:N_F2| は |PB4:N| を割り切るはずだが、論文 Table 1 は N(19) で |F2:N_F2|=7776 > |PB4:N(19)|=216 と記しており矛盾する(実測: Size(Group(g12,g23))=24 のみ、Table1 の 7776 とは一致しない)。NFI_PB4(B4) が PaB4 上の compatible equivalence relation(§2.1-2.2)であり N_PB3 は insertion map を介した誘導関係である可能性が高く、単純な部分群共通部分ではないと推定(未確証)。よって本 cert の pentagon_pass_count_OVER_IMAGE_NOT_N_F2 / pentagon_total_count_OVER_IMAGE_NOT_N_F2 は「F2 の PB4/N への像 <g12,g23>(N34 はその DerivedSubgroup)上で測った pentagon 充足数」であり、論文の F2/N_F2 上の測定(216/36/4096/243 の対象)とは異なる集合上の値である。量的再現としては未達 -- 司令塔裁定・追加読解待ち。pentagon_and_hexagon_count は本 pass ではスコープ外(理由: hexagon 判定機構は x13 を AbstractProd([x,y])^-1 として内部導出する規約を前提にしており、pentagon 側で独立に与えられる g13 との整合が未検証 -- sanity.g13_eq_derived_z で実測のみ報告)。N(34) の g14=g23, g34=g12 は原文 pdftotext 抽出(2系統照合)+ PDF ページ画像の直接目視で literal に一致することを確認済み(誤植ではない) -- 数学的に意外な一致として明記のみ。\",\n",
  "  \"params\":{\n",
  "    \"windows\":", JArr(List(PENTA_WINDOWS, JStr)), ",\n",
  "    \"max_elements_cap\":", String(PENTA_MAX_ELEMENTS), ",\n",
  "    \"max_closure_rounds\":", String(PENTA_MAX_CLOSURE_ROUNDS), "\n",
  "  },\n",
  "  \"results\":", JArr(List(allResults, ResultToJson)), ",\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"gap_invocation\":\"gap -q -o 2g search/probe/wac_v1/pentagon_check.g (preamble optionally sets PENTA_WINDOWS for shard)\"\n",
  "  }\n",
  "}\n");;

WriteFile(outName, cert);;
ValidateJsonFile(outName);;
Print("\nWrote ", outName, " (json.load OK)\n");
Print("\nPENTAGON_CHECK_DONE\n");
QUIT;
