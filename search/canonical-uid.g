#############################################################################
## search/canonical-uid.g -- P81-F: window canonical UID (judge v1.4)
##
## 司令塔裁定(2026-07-29/30, W7 発注訂正込み)に基づく実装:
##
##   窓 = (n, a1, b1)(候補A: search/w62-windows.g の a1,b1 -- strike-a{16,18,20}.g
##   から逐語)。ここから作る対象は「抽象群 G=<a1,b1> の Cayley グラフ」ではなく
##   **domain [1..n] 上の生成元ラベル付き作用グラフ**: 頂点 i(色1)から
##   頂点 i^a1 への辺を色2、頂点 i^b1 への辺を色3で表す。多重辺を避けるため
##   標準の頂点分割手法を使う: 各 i につき「a-辺頂点」m_{i,a}(色2)・
##   「b-辺頂点」m_{i,b}(色3)を新設し、i -> m_{i,a} -> i^a1、i -> m_{i,b} -> i^b1
##   という 2 段の弧に置き換える(3n 頂点・4n 弧、多重辺は構造的に発生しない)。
##
##   この構成は docs/notes/a13_prediction_v1.md S1.0 の補題(2つの生成対が
##   S_n-共役 <=> 同一 C-軌道 <=> 同一窓 N)が要求する不変量と一致する:
##   (a1,b1) を (a1^g, b1^g) に同時共役で取り替えても、頂点の再ラベル付け
##   i |-> i^g がこの作用グラフの同型を与える(下の証明メモ参照)ので、
##   bliss の canonical form は不変。逆に (a1,b1) を独立に(非対称に)取り替え
##   たり swap したりすれば一般に別の UID になる -- これは意図された挙動
##   (裁定: 「不変量は対の同時共役のみ」「(a,b)は ordered pair なので swap
##   不変性は要求しない」)。
##
##   [同時共役で同型になることの直接検算]
##   sigma: i |-> i^g とする。graph1 の弧 i -> i^h (h=a1 or b1) は sigma で
##   i^g -> (i^h)^g に写る。graph2(生成元 h^g := g^-1*h*g)の弧は
##   j -> j^(h^g) = j -> j^(g^-1 h g)。j := i^g を代入すると
##   j^(h^g) = i^(g * g^-1 h g) = i^(h g) = (i^h)^g。graph1 の像の終点と一致
##   するので sigma は graph1 -> graph2 の同型。
##
## UID = 上記グラフを BlissCanonicalLabelling(digraph, colours) で正準化し、
##   正準表現(色つき隣接構造、各頂点の出隣接をソート)を決定的に直列化して
##   SHA-256 したもの(sha256sum に shell out -- search/w62-splitting.g の
##   ComputeSha256File と同じ方式、GAP に SHA-256 のネイティブ実装がないため)。
##
## LID-1(裁定171 / docs/notes/a13_prediction_v1.md S1.1 に倣う「literal な
##   生成元語の SHA-256」)も併記する。UID とは別の ID(表示依存 = LID-1、
##   窓の同一性 = UID)であり、両者は一致する義務がない -- 実際、同時共役
##   だけで LID-1 は変わるが UID は変わらないことを回帰スイートで示す。
##
## 入力の出所(provenance): search/w62-windows.g の W62_WINDOWS(a1,b1,n は
##   search/strike-a{16,18,20}.g の各66-67/57-58/57-58行からの逐語 -- 司令塔
##   裁定どおり、生成対は cert ではなく driver ソースから取る)。
#############################################################################

Read("search/gaplib_common.g");
Read("search/w62-windows.g");   # W62_WINDOWS, W62_MakeW

if LoadPackage("digraphs") <> true then
  Error("canonical-uid.g: LoadPackage(\"digraphs\") failed -- fail-closed, ",
        "bliss canonical labelling is unavailable without it");
fi;

CANONICAL_UID_VERSION := "canonical-uid/v1";;
CANONICAL_UID_INPUT_SOURCE := "search/w62-windows.g:W62_WINDOWS (verbatim from search/strike-a{16,18,20}.g driver literals, per W7/P81-F ruling 2026-07-30)";;

#############################################################################
## ---------------------- SHA-256 (shell out; w62-splitting.g pattern) ------
#############################################################################
CANONICAL_UID_TMP_COUNTER := 0;;
Sha256OfString := function(s)
  local tmp, out, f, line;
  CANONICAL_UID_TMP_COUNTER := CANONICAL_UID_TMP_COUNTER + 1;
  tmp := Concatenation("search/.tmp_uid_sha_", String(Runtime()), "_",
                        String(CANONICAL_UID_TMP_COUNTER), ".txt");
  out := Concatenation(tmp, ".sha");
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
    Error("canonical-uid.g: Sha256OfString: sha256sum did not return a hash line");
  fi;
  return line{[1 .. 64]};
end;;

#############################################################################
## ---------------------- domain action graph + canonical form --------------
#############################################################################
# BuildWindowActionDigraph(n, a1, b1): returns rec(digraph, colours, n).
# Vertex layout (3n vertices total):
#   [1 .. n]        domain points, colour 1
#   [n+1 .. 2n]     a-edge subdivision vertices, colour 2 (m_{i,a} = n+i)
#   [2n+1 .. 3n]    b-edge subdivision vertices, colour 3 (m_{i,b} = 2n+i)
BuildWindowActionDigraph := function(n, a1, b1)
  local out, colours, i;
  out := [];
  colours := [];
  for i in [1 .. n] do
    out[i] := [n + i, 2*n + i];
    colours[i] := 1;
  od;
  for i in [1 .. n] do
    out[n + i] := [ i^a1 ];
    colours[n + i] := 2;
  od;
  for i in [1 .. n] do
    out[2*n + i] := [ i^b1 ];
    colours[2*n + i] := 3;
  od;
  return rec(digraph := Digraph(out), colours := colours, n := n);
end;;

# CanonicalFormOfActionGraph(ag): applies BlissCanonicalLabelling with the
# colour partition, then produces a deterministic string serialization of
# the canonical (digraph, colouring) pair (sorted out-neighbours per vertex,
# vertices visited in canonical-index order 1..3n -- this order is itself
# canonical because it IS the vertex set of the canonical representative).
CanonicalFormOfActionGraph := function(ag)
  local p, canon, canonColours, i, totalV, nbrs, vertexParts;
  if IsMultiDigraph(ag.digraph) then
    Error("canonical-uid.g: action digraph has multiple edges -- ",
          "construction invariant violated (should be structurally impossible)");
  fi;
  p := BlissCanonicalLabelling(ag.digraph, ag.colours);
  canon := OnDigraphs(ag.digraph, p);
  # per Digraphs manual S7.2-8: colour of vertex v (in original) survives at
  # v^p in the canonical representative, so the canonical colouring is:
  canonColours := List(DigraphVertices(ag.digraph), i -> ag.colours[i / p]);
  totalV := DigraphNrVertices(canon);
  vertexParts := [];
  for i in [1 .. totalV] do
    nbrs := ShallowCopy(OutNeighboursOfVertex(canon, i));
    Sort(nbrs);
    Add(vertexParts, Concatenation("v", String(i), ":c", String(canonColours[i]),
                                    ":o", JArr(List(nbrs, String))));
  od;
  return rec(p := p, canon := canon, canonColours := canonColours,
             serialized := Concatenation("windowactiongraph/v1|n=", String(ag.n),
               "|V=", String(totalV), "|", JoinC(vertexParts, ";")));
end;;

#############################################################################
## ---------------------- top-level: UID + LID-1 for one (n,a1,b1) ----------
#############################################################################
# WindowCanonicalUID(id, n, a1, b1): returns a record with both IDs.
#   uid_sha256  -- the P81-F canonical UID (invariant under simultaneous
#                  conjugation of (a1,b1); this is the "identity of the
#                  window" per the coordinator's ruling).
#   lid1_sha256 -- LID-1-style literal-word hash (representation-dependent;
#                  "identity of the display", per docs/notes/a13_prediction_v1.md
#                  S1.1 convention, adapted to this window family which has
#                  no "t" parameter).
# S1S2FromA1B1: reproduces search/w62-windows.g's W62_MakeW arithmetic for
# s1 = b^-1*a, s2 = a^-1*b^2 inside A_n x S_3 (the B3-image generators),
# WITHOUT pulling in kerchi-judge.g/MakeWindow (which would also build
# Bq=Group(s1,s2) and PN=Group(x,y) as lazy group objects -- harmless in
# principle, but this script has no other use for kerchi-judge.g's much
# larger dependency surface, so the small arithmetic is inlined instead).
S1S2FromA1B1 := function(n, a1, b1)
  local An, S3, D, embA, embS, agen, bgen;
  An := AlternatingGroup(n);
  S3 := SymmetricGroup(3);
  D := DirectProduct(An, S3);
  embA := Embedding(D, 1);  embS := Embedding(D, 2);
  agen := Image(embA, a1) * Image(embS, (1,3));
  bgen := Image(embA, b1) * Image(embS, (1,3,2));
  return rec(s1 := bgen^-1 * agen, s2 := agen^-1 * bgen^2);
end;;

WindowCanonicalUID := function(id, n, a1, b1)
  local ag, cf, uid, ss, lid1Str, lid1;
  ag := BuildWindowActionDigraph(n, a1, b1);
  cf := CanonicalFormOfActionGraph(ag);
  uid := Sha256OfString(cf.serialized);
  ss := S1S2FromA1B1(n, a1, b1);
  lid1Str := Concatenation("LID1/v1|id=", id, "|n=", String(n),
               "|a1=", String(a1), "|b1=", String(b1),
               "|S1=", String(ss.s1), "|S2=", String(ss.s2));
  lid1 := Sha256OfString(lid1Str);
  return rec(id := id, n := n, uid_sha256 := uid, uid_serialized_preview := cf.serialized,
             lid1_sha256 := lid1, lid1_serialized := lid1Str);
end;;

Print("canonical-uid.g loaded (", CANONICAL_UID_VERSION, ")\n");
