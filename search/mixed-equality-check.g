# mixed-equality-check.g -- I-3 先行手(等号検査)
#
# 実行: .\gap.ps1 search\mixed-equality-check.g
#
# 事前登録: provenance/registered/universe_I1_I3.md 「I-3 先行手(等号検査)」節。
# 出典: arXiv 2405.11725(dihedral poset; Prop 3.5)。ψ_n の生成元像は
#       docs/week1-定義ノート.md §3(2405 (3.1))から逐語転記(下記 MakeGn 内コメント参照)。
#
# 主張候補: K^(12) = K^(4) ∩ K^(3)(⊆ は Prop 3.5 系で既知・等号が未検算)。
# 判定法(事前登録どおり・固定): B3 の対写像 (psi_4, psi_3) の像を D4^3 x D3^3 内に
#   生成元 x, y (c は両写像で (1,1,1) に落ちるため寄与なし)から直接構成し、
#   Size を計算して事前登録済みの比較値 6912 = 4*12^3 と照合する。
#   指数の偶然一致に頼らず、像そのものを構成する(事前登録の指示どおり)。
#
# 判定: EQUAL(6912と一致) / NOT_EQUAL(不一致) / UNKNOWN(計算不能)。
#
# 規律: 宇宙は事前登録どおり固定(n=4, n=3 のみ)。u・c 平方類・ĉ_μ には触れない。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;   # JB/WriteFile 等の共通ヘルパー(gaplib/v1・新規スクリプト規約)

PF := function(b)
  if b then return "PASS"; else return "FAIL"; fi;
end;;

# ------------------------------------------------------------------
# MakeDn -- search/week1-kn-spotcheck.g / search/suite-wp1.g より再利用(無変更でコピー)
# D_n の置換表現(論文 2405 §5.3 の慣例): r(j) = j+1 mod n, s(j) = -j mod n
# ------------------------------------------------------------------
MakeDn := function(n)
  local r, s;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  if not (Order(r) = n and Order(s) = 2 and s*r*s^-1 = r^-1) then
    Error("D_n relations failed for n = ", n);
  fi;
  return [r, s];
end;;

# D_n^3 の元を「3n 点上の置換」として実装(suite-wp1.g の MakeGn と同一だが、
# ここでは複数の n を「非交和の点集合」上に同時実装するため offset 付きに一般化する)
# tr(p, i, n, offset): D_n の元 p を、offset だけずらした 3n 点中の第 i ブロックへ移送
trOffset := function(p, i, n, offset)
  local l, j, total;
  # l は「offset..offset+3n」の外側全体を恒等に保つため、呼び出し側で合成する設計とする
  l := List([1..offset + 3*n], k -> k);
  for j in [1..n] do
    l[j + (i-1)*n + offset] := (j^p) + (i-1)*n + offset;
  od;
  return PermList(l);
end;;

# MakeGn(n) -- suite-wp1.g と同一実装(較正済み・無変更でコピー)。回帰対象ではないが
# セクション 2(WP1 既知値 |G_12| との比較)で参照するために保持する。
MakeGn := function(n)
  local rs, r, s, x, y, tr;
  rs := MakeDn(n);  r := rs[1];  s := rs[2];
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do
      l[j + (i-1)*n] := (j^p) + (i-1)*n;
    od;
    return PermList(l);
  end;
  # x̄ = (r, s, s), ȳ = (rs, r, rs)  ※ rs は「s のち r」= GAP では s*r
  x := tr(r,1) * tr(s,2) * tr(s,3);
  y := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  return rec(x := x, y := y, G := Group(x, y));
end;;

expectedSize := function(n)
  if n mod 2 = 1 then return 4*n^3; else return 4*(n/2)^3; fi;
end;;

t0 := Runtime();;

# ####################################################################
# セクション 1: 対写像 (psi_4, psi_3) の像を D4^3 x D3^3 (12+9=21 点) 内に直接構成
# ####################################################################
Print("############################################################\n");
Print("# セクション 1: (psi_4, psi_3) の像の直接構成\n");
Print("############################################################\n");

d4 := MakeDn(4);;  r4 := d4[1];;  s4 := d4[2];;
d3 := MakeDn(3);;  r3 := d3[1];;  s3 := d3[2];;

# D4^3 は点 1..12、D3^3 は点 13..21(offset=12)
tr4 := function(p, i) return trOffset(p, i, 4, 0); end;;
tr3 := function(p, i) return trOffset(p, i, 3, 12); end;;

# x̄ = (r,s,s), ȳ = (rs,r,rs) を D4^3 成分・D3^3 成分それぞれで構成し、21 点上の
# 単一の置換として積を取る(直積の元は「両側の作用を同時に行う置換」として実現できる)
xPair := tr4(r4,1) * tr4(s4,2) * tr4(s4,3) * tr3(r3,1) * tr3(s3,2) * tr3(s3,3);;
yPair := tr4(s4*r4,1) * tr4(r4,2) * tr4(s4*r4,3) * tr3(s3*r3,1) * tr3(r3,2) * tr3(s3*r3,3);;

GPair := Group(xPair, yPair);;
imageSize := Size(GPair);;

Print("生成元像(21 点上の置換、点 1-12=D4^3, 13-21=D3^3):\n");
Print("  x_pair = ", xPair, "\n");
Print("  y_pair = ", yPair, "\n");
Print("像の位数 |Im(psi_4,psi_3)| = ", imageSize, "\n");

# ####################################################################
# セクション 2: 事前登録済み比較値 6912 との照合 + WP1 既知値 |G_12| との参考照合
# ####################################################################
Print("\n############################################################\n");
Print("# セクション 2: 判定\n");
Print("############################################################\n");

registeredTarget := 6912;;   # provenance/registered/universe_I1_I3.md 記載の比較値 = 4*12^3
Print("事前登録済み比較値(4*12^3, universe_I1_I3.md 記載どおり) = ", registeredTarget, "\n");

verdict := "";;
if imageSize = registeredTarget then
  verdict := "EQUAL";
elif imageSize > 0 then
  verdict := "NOT_EQUAL";
else
  verdict := "UNKNOWN";
fi;
Print("[判定(事前登録比較値 ", registeredTarget, " に対して)] ", verdict, "\n");

# 参考観測(判定には使わない・解釈は司令塔/数学者の仕事):
# WP1 (search/suite-wp1.g) で n=12 は「偶数」扱いで |G_12| = 4*(12/2)^3 = 864 が
# ALL PASSED 済みの既知値である。この場に限り同一セッション内で MakeGn(12) を
# 参考として再構成し、独立に得た imageSize と比較記録する(判定基準は上記の
# registeredTarget=6912 のみ・以下は事実の並記)。
g12 := MakeGn(12);;
g12Size := Size(g12.G);;
Print("\n参考観測: このセッション内で MakeGn(12) を再構成した場合 |G_12| = ", g12Size,
      " (WP1 既知値 864 に一致するか: ", PF(g12Size = 864), ")\n");
Print("参考観測: imageSize (", imageSize, ") と g12Size (", g12Size, ") の一致: ",
      PF(imageSize = g12Size), "\n");
Print("(解釈はしない。事前登録比較値 6912 と g12Size=", g12Size,
      " 自体が異なることも含め、事実として記録する。)\n");

t1 := Runtime();;
elapsedMs := t1 - t0;;

# ####################################################################
# 証明書 JSON
# ####################################################################
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_i3.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/mixed-equality-check.g");;
universeDocSha256 := ComputeSha256File("provenance/registered/universe_I1_I3.md");;

cert := Concatenation(
  "{\"schema\":\"i3-equality-check/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/mixed-equality-check.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"claim\":\"K^(12) = K^(4) intersect K^(3)\"",
  ",\"method\":\"直接構成: (psi_4,psi_3) の像を D4^3 x D3^3 (21点) 内に生成元 x,y から構成し Size を計算\"",
  ",\"generators\":{\"x_pair\":\"", String(xPair), "\",\"y_pair\":\"", String(yPair), "\"}",
  ",\"image_size\":", String(imageSize),
  ",\"registered_target\":", String(registeredTarget),
  ",\"verdict_vs_registered_target\":\"", verdict, "\"",
  ",\"reference_observation\":{\"g12_size_this_session\":", String(g12Size),
  ",\"g12_matches_wp1_known_864\":", JB(g12Size = 864),
  ",\"image_size_matches_g12_size\":", JB(imageSize = g12Size), "}",
  ",\"elapsed_cpu_ms\":", String(elapsedMs),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"",
  ",\"universe_doc_sha256\":\"", universeDocSha256, "\"",
  ",\"universe_doc_path\":\"provenance/registered/universe_I1_I3.md\"}",
  "}"
);;

outPath := "search/certs/i3_equality_20260728.json";;
WriteFile(outPath, cert);;   # WriteFile は生バイト書出し(PrintTo/OutputTextFile は
                              # 長い行を "\<改行>" で折り返し JSON を破壊するため不使用)
Print("\n証明書を書き出した: ", outPath, "\n");

Print("\n############################################################\n");
Print("I3 VERDICT: ", verdict, "\n");
QUIT;
