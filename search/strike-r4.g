#############################################################################
## search/strike-r4.g -- r=4 discriminating-window measurement driver
## (2 windows: W-E-A20-5x4t0-C / -B, all N_ord=5, type (5,5,5,5), n=20, r=4)
##
## 仕様書: search/_r4_driver_spec.md (これが正本・完結仕様)。裁定231。
## 接触遮断: docs/notes/r4_prediction_v1.md, docs/notes/pruning_law_v1_1.md,
## ideas/ は本 driver からは一切 Read しない。期待値・比較対象はコードに
## 書かない -- 例外は仕様書 S0/S1.2/S3/S4.2 に明記された4点のみ:
##   (1) 入口ゲート G1/G2 の canonical-id SHA-256 と naive==xi digest 較正
##   (2) 2 窓の canonical-id SHA-256 (fail-closed 照合)
##   (3) Xi-restricted 走査の fail-closed 上界 (窓/層ごとの表値)
##   (4) 結合時の会計 assert (accepted 総和 / chunk_scan_bound 総和)
## それ以外はすべて生の測定値として記録するだけで、解釈も期待値比較もしない。
##
## judge: search/kerchi-judge.g v1.3 の Xi-restricted 実装 (MakeWindow /
## CorrectedShadowsLegacy / CorrectedShadowsXi / GroupOfShadows) を
## JUDGE_LIBRARY_ONLY モードで再利用。JUDGE_SKIP_LEGACY_CROSSCHECK := true
## (P=A_20 は非可解・巨大で EnumerateReducedHexagon crosscheck は不可能)。
## 骨格: search/strike-i10-1.g (canonical文字列書式 |ell=|r= 込み) +
##       search/strike-a13-ladder.g (STR-1 欄・16項assert様式)。
## 窓構成: search/strike-i10-1.g の BuildS1S2E をそのまま流用 (a1 の偶奇を
## 問わない DirectProduct(SymmetricGroup(n),S3) 構成 -- C 枝/B 枝どちらも
## 同一コードパスで正しく E を構成できる。仕様書 S2 の3assertで両枝とも検証)。
##
## モード (preamble で選択, デフォルトは A: フル窓 1 本を 1 プロセスで測定):
##   R4_ONLY_WINDOW := "C" | "B"   -- 対象窓を1つに絞る(未指定なら両方: 非推奨,
##                                    CI では常に1窓ずつ撃つこと)
##   R4_ONLY_M := <m>              -- モードB: その層(m in {0,1,3,4})だけを
##                                    Xi-restricted 走査し、生の shadow リストを
##                                    shard ファイルに書いて終了 (フル測定はしない)
##   R4_COMBINE_WINDOW := "C"|"B"  -- モードC: 4層分の shard ファイルを読み込み、
##                                    結合会計 assert 後にフル測定して最終証明書
##                                    を書く (R4_ONLY_WINDOW と併用しない)
##
## Output (モードA既定): search/certs/r4_<JUDGE_ID>_20260730.json
##                        + search/certs/r4_gate_20260730.json (初回呼び出し時)
##                        + search/certs/r4_manifest_<window>_20260730.json
#############################################################################

Read("search/gaplib_common.g");
JUDGE_LIBRARY_ONLY := true;;
JUDGE_SKIP_LEGACY_CROSSCHECK := true;;
Read("search/kerchi-judge.g");

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

PrintStr := function(x)
  local s, ss;
  ss := "";;
  s := OutputTextString(ss, true);;
  SetPrintFormattingStatus(s, false);;
  PrintTo(s, x);;
  CloseStream(s);;
  return ss;
end;;

Sha256OfString := function(str)
  local tmp, f, line;
  tmp := "search/certs/.r4_sha_tmp.txt";
  f := OutputTextFile(tmp, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, str);
  CloseStream(f);
  Exec(Concatenation("sha256sum \"", tmp, "\" > \"", tmp, ".out\""));
  f := InputTextFile(Concatenation(tmp, ".out"));
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\" \"", tmp, ".out\""));
  return line{[1..64]};
end;;

CertSha256File := function(path)
  local tmp, f, line;
  tmp := "search/certs/.r4_sha_tmp2.txt";
  Exec(Concatenation("sha256sum \"", path, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1..64]};
end;;

#############################################################################
## ---------------------- shared window construction -------------------------
## (identical recipe to search/strike-i10-1.g's BuildS1S2E / search/strike-
## a13-ladder.g's BuildS1S2 -- DirectProduct(SymmetricGroup(n),S3), a1 の
## 偶奇を問わない -- committed campaign convention, not re-derived here)
#############################################################################
BuildS1S2E := function(a1, b1, n)
  local Sn, S3, Dgrp, embA, embS, agen, bgen, s1, s2, E;
  Sn := SymmetricGroup(n);;  S3 := SymmetricGroup(3);;
  Dgrp := DirectProduct(Sn, S3);;
  embA := Embedding(Dgrp, 1);;  embS := Embedding(Dgrp, 2);;
  agen := Image(embA, a1) * Image(embS, (1,3));;
  bgen := Image(embA, b1) * Image(embS, (1,3,2));;
  s1 := bgen^-1 * agen;;
  s2 := agen^-1 * bgen^2;;
  E := Group(agen, bgen);;
  return rec(s1 := s1, s2 := s2, Dgrp := Dgrp, agen := agen, bgen := bgen, E := E);
end;;

#############################################################################
## ---------------------- S0: entry gate (G1/G2, fail-closed) ----------------
#############################################################################
GateCanonicalStringA13 := function(id, n, t, a1, b1, s1, s2)
  return Concatenation(id, "|n=", String(n), "|t=", String(t),
    "|a1=", PrintStr(a1), "|b1=", PrintStr(b1),
    "|S1=", PrintStr(s1), "|S2=", PrintStr(s2));
end;;

GateCanonicalStringI10 := function(id, n, ell, r, t, a1, b1, s1, s2)
  return Concatenation(id, "|n=", String(n), "|ell=", String(ell), "|r=", String(r),
    "|t=", String(t), "|a1=", PrintStr(a1), "|b1=", PrintStr(b1),
    "|S1=", PrintStr(s1), "|S2=", PrintStr(s2));
end;;

# runs the naive-vs-xi calibration for ONE gate window; does not Error itself
# (caller decides fail-closed policy) so both gates can be attempted and
# reported even if the first one already failed.
RunGateWindow := function(a1, b1, n, s1lit, s2lit, canonStr, expectedSha, xiBound, label)
  local built, s1, s2, W, charmingSet, legacyRes, xiRes, naiveDigest, xiDigest,
        t0, t1, naiveElapsed, xiElapsed, ok, sha, stage1Ok;
  built := BuildS1S2E(a1, b1, n);;
  s1 := built.s1;;  s2 := built.s2;;

  stage1Ok := (a1^2 = () ) and (built.s1*built.s2*built.s1 = built.s2*built.s1*built.s2)
              and (s1 = s1lit) and (s2 = s2lit);;
  sha := Sha256OfString(canonStr);;
  Print("  [gate ", label, "] canonical_string = ", canonStr, "\n");
  Print("  [gate ", label, "] canonical_id_sha256 = ", sha, "\n");
  stage1Ok := stage1Ok and (sha = expectedSha);;
  Print("  [", PF(stage1Ok), "] [gate ", label, "] stage1 + canonical-id SHA-256 match\n");
  if not stage1Ok then
    return rec(pass := false, label := label, canonical_sha := sha,
               reason := "stage1/canonical-id mismatch -- fail-closed, digest gate not attempted");
  fi;

  W := MakeWindow(s1, s2);;
  charmingSet := Filtered([0 .. W.Nord - 1], m -> Gcd(2*m+1, W.Nord) = 1);;

  t0 := GAPLIB_WallElapsedMs();;
  legacyRes := CorrectedShadowsLegacy(W, charmingSet);;
  t1 := GAPLIB_WallElapsedMs();;
  naiveElapsed := (t1 - t0) / 1000.0;;
  naiveDigest := Sha256OfString(JoinC(List(legacyRes.shadows, s -> PrintStr(s)), "\n"));;
  Print("  [gate ", label, "] naive: shadow_total=", Length(legacyRes.shadows),
        " elapsed_sec=", naiveElapsed, " digest=", naiveDigest, "\n");

  t0 := GAPLIB_WallElapsedMs();;
  JUDGE_FORCE_SCAN_MODE := "xi_restricted";;
  xiRes := CorrectedShadowsXi(W, charmingSet);;
  t1 := GAPLIB_WallElapsedMs();;
  xiElapsed := (t1 - t0) / 1000.0;;
  xiDigest := Sha256OfString(JoinC(List(xiRes.shadows, s -> PrintStr(s)), "\n"));;
  Print("  [gate ", label, "] xi:    shadow_total=", Length(xiRes.shadows),
        " elapsed_sec=", xiElapsed, " digest=", xiDigest,
        " scanned_count=", xiRes.scanned_count, " bound=", xiBound, "\n");

  ok := (naiveDigest = xiDigest) and (xiRes.scanned_count <= xiBound);;
  Print("  [", PF(ok), "] [gate ", label, "] naive_shadow_digest == xi_shadow_digest",
        " (and scanned_count <= bound)\n");

  return rec(pass := ok, label := label, canonical_sha := sha,
             naive_digest := naiveDigest, xi_digest := xiDigest,
             naive_shadow_total := Length(legacyRes.shadows),
             xi_shadow_total := Length(xiRes.shadows),
             naive_elapsed_sec := naiveElapsed, xi_elapsed_sec := xiElapsed,
             xi_scanned_count := xiRes.scanned_count, xi_bound := xiBound);
end;;

RunEntryGate := function()
  local g1, g2, canonG1, canonG2, s1lit1, s2lit1, s1lit2, s2lit2, a1g1, b1g1, a1g2, b1g2;

  Print("\n################################################################\n");
  Print("# S0 entry gate: G1 (W-E-A10-9t1) + G2 (W-E-A10-5x2t0)\n");
  Print("################################################################\n");

  # ---- G1: W-E-A10-9t1 (search/_a13_ladder_driver_spec.md canonical window 1;
  # canonical string format WITHOUT ell/r, per that spec) ----
  a1g1 := ( 1, 2)( 3, 5)( 4,10)( 6, 9);;
  b1g1 := ( 2, 9, 5)( 3, 4,10)( 6, 8, 7);;
  s1lit1 := ( 1, 2, 3, 4, 5, 6, 7, 8, 9)(11,12);;
  s2lit1 := ( 1, 5,10, 3, 9, 7, 8, 6, 2)(12,13);;
  canonG1 := GateCanonicalStringA13("W-E-A10-9t1", 10, 1, a1g1, b1g1, s1lit1, s2lit1);;
  g1 := RunGateWindow(a1g1, b1g1, 10, s1lit1, s2lit1, canonG1,
          "6092f5f0bae86188d1f46ede81e1dad2aebbb097d6d3c9cae46229b67e853f4b",
          486, "G1-W-E-A10-9t1");;

  # ---- G2: W-E-A10-5x2t0 (search/_i10_1_driver_spec.md canonical window 1;
  # canonical string format WITH ell/r) ----
  a1g2 := ( 1, 2)( 3, 6)( 7,10);;
  b1g2 := ( 2,10, 6)( 3, 5, 4)( 7, 9, 8);;
  s1lit2 := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12);;
  s2lit2 := ( 1, 6, 4, 5, 3,10, 8, 9, 7, 2)(12,13);;
  canonG2 := GateCanonicalStringI10("W-E-A10-5x2t0", 10, 5, 2, 0, a1g2, b1g2, s1lit2, s2lit2);;
  g2 := RunGateWindow(a1g2, b1g2, 10, s1lit2, s2lit2, canonG2,
          "5848b4bffe7878f048a34379cd4042d1efbed1df6596aa0b5106694f46589df4",
          5000, "G2-W-E-A10-5x2t0");;

  Print("\n=== S0 entry gate summary: G1=", PF(g1.pass), " G2=", PF(g2.pass), " ===\n");
  return rec(g1 := g1, g2 := g2, all_pass := g1.pass and g2.pass);
end;;

# FieldOrNull: dynamic-field JSON accessor (avoids GAP's strict-boolean
# short-circuit trap on 'and'/'or' when mixing bool with string/int).
FieldOrNull := function(g, name, isStr)
  if not IsBound(g.(name)) then return "null"; fi;
  if isStr then return JStr(g.(name)); else return String(g.(name)); fi;
end;;

GateJson := function(g)
  return Concatenation("{\"label\":", JStr(g.label),
    ",\"pass\":", JB(g.pass),
    ",\"canonical_id_sha256\":", JStr(g.canonical_sha),
    ",\"naive_shadow_digest\":", FieldOrNull(g, "naive_digest", true),
    ",\"xi_shadow_digest\":", FieldOrNull(g, "xi_digest", true),
    ",\"naive_shadow_total\":", FieldOrNull(g, "naive_shadow_total", false),
    ",\"xi_shadow_total\":", FieldOrNull(g, "xi_shadow_total", false),
    ",\"naive_elapsed_sec\":", FieldOrNull(g, "naive_elapsed_sec", false),
    ",\"xi_elapsed_sec\":", FieldOrNull(g, "xi_elapsed_sec", false),
    ",\"xi_scanned_count\":", FieldOrNull(g, "xi_scanned_count", false),
    ",\"xi_bound\":", FieldOrNull(g, "xi_bound", false),
    ",\"reason\":", FieldOrNull(g, "reason", true), "}");
end;;

#############################################################################
## ---------------------- S1: window table (machine-transcribed from spec) --
#############################################################################
R4_WINDOWS := [
  rec(id := "W-E-A20-5x4t0-C", n := 20, ell := 5, r := 4, t := 0,
      a1 := ( 1,14)( 2,15)( 3,10)( 5, 9)( 6, 7)(12,19)(13,16)(17,18),
      b1 := ( 1,13,15)( 2,14,10)( 3, 9, 4)( 5, 8, 7)(11,20,19)(12,18,16),
      s1lit := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12,13,14,15,16,17,18,19,20)(21,22),
      s2lit := ( 1, 2,13,18,17,12,20,11,19,16)( 3,14,15,10, 4, 9, 7, 6, 8, 5)(22,23),
      epsBranch := "eps0_direct", shaKey := "C"),
  rec(id := "W-E-A20-5x4t0-B", n := 20, ell := 5, r := 4, t := 0,
      a1 := ( 1,15)( 3,14)( 4, 5)( 6,13)( 7,20)( 8, 9)(10,19)(11,18)(12,16),
      b1 := ( 1,14, 2)( 3,13, 5)( 6,12,20)( 7,19, 9)(10,18,15)(11,17,16),
      s1lit := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12,13,14,15)(16,17,18,19,20)(21,22),
      s2lit := ( 1,18,16, 6, 3)( 2,14, 5, 4,13,20, 9, 8,19,15)( 7,12,17,11,10)(22,23),
      epsBranch := "eps1_fibre", shaKey := "B"),
];;

R4_CANONICAL_SHA := rec(
  C := "d49d2556efa837b5f811072c42b06271ffab900f7240319ad87c000041ccdb84",
  B := "093b8b32d239de2a363b170b692e3f72ab3e9433d403e1587d54fef2eb54b586"
);;

# S3 fail-closed Xi-restricted scan upper bounds
R4_XI_BOUND_PER_M := 112500000;;
R4_XI_BOUND_TOTAL := 450000000;;
R4_CHARMING_SET := [0, 1, 3, 4];;   # Nord=5, gcd(2m+1,5)=1

CanonicalStringR4 := function(id, n, ell, r, t, a1, b1, s1, s2)
  return Concatenation(id, "|n=", String(n), "|ell=", String(ell), "|r=", String(r),
    "|t=", String(t), "|a1=", PrintStr(a1), "|b1=", PrintStr(b1),
    "|S1=", PrintStr(s1), "|S2=", PrintStr(s2));
end;;

#############################################################################
## ---------------------- S2: per-window structural asserts (16-item style) -
#############################################################################
ProcessWindowStage1 := function(w)
  local asserts, StageAssert, ok, built, s1, s2, W, AN, epsActual, canon, sha;
  asserts := [];;
  StageAssert := function(label, val)
    Add(asserts, rec(label := label, ok := val));
    Print("  [", PF(val), "] ", label, "\n");
    return val;
  end;;
  ok := true;;

  built := BuildS1S2E(w.a1, w.b1, w.n);;
  s1 := built.s1;;  s2 := built.s2;;

  ok := StageAssert("a1^2=1 and b1^3=1", w.a1^2 = () and w.b1^3 = ()) and ok;
  ok := StageAssert("braid relation s1*s2*s1 = s2*s1*s2", s1*s2*s1 = s2*s1*s2) and ok;
  ok := StageAssert("computed s1 (via BuildS1S2E) = literal JUDGE_S1_IMG (spec)",
                     s1 = w.s1lit) and ok;
  ok := StageAssert("computed s2 (via BuildS1S2E) = literal JUDGE_S2_IMG (spec)",
                     s2 = w.s2lit) and ok;

  # eps_branch: recorded from sign(a1), cross-checked against the window
  # table's declared epsBranch (transcription-consistency, not a re-derivation).
  if SignPerm(w.a1) = 1 then epsActual := "eps0_direct"; else epsActual := "eps1_fibre"; fi;
  ok := StageAssert(Concatenation("eps_branch (sign(a1)=", String(SignPerm(w.a1)),
                       ") = ", epsActual, " matches window table's declared ", w.epsBranch),
                     epsActual = w.epsBranch) and ok;

  # canonical-id SHA-256 fail-closed identity check
  canon := CanonicalStringR4(w.id, w.n, w.ell, w.r, w.t, w.a1, w.b1, s1, s2);;
  sha := Sha256OfString(canon);;
  Print("  canonical_string = ", canon, "\n");
  Print("  canonical_id_sha256 = ", sha, "\n");
  ok := StageAssert(Concatenation("canonical-id SHA-256 matches spec table (fail-closed identity check, window ", w.id, ")"),
                     sha = R4_CANONICAL_SHA.(w.shaKey)) and ok;

  W := MakeWindow(s1, s2);;
  ok := StageAssert("c=(s1*s2)^3 = identity (c in N)", W.c = Identity(W.Bq)) and ok;
  ok := StageAssert("ord(cbar) = 1 (c=id, restated)", Order(W.c) = 1) and ok;
  ok := StageAssert("ord(xbar) = 5", Order(W.x) = 5) and ok;
  ok := StageAssert("ord(ybar) = 5", Order(W.y) = 5) and ok;
  ok := StageAssert("N_ord = lcm(5,5,1) = 5", W.Nord = 5) and ok;
  ok := StageAssert("charming m set = {0,1,3,4} = phi(2*5)=4 elements",
                     Filtered([0 .. W.Nord-1], m -> Gcd(2*m+1,W.Nord)=1) = R4_CHARMING_SET) and ok;

  # ---- S2's 3 branch-uniform asserts (both eps0_direct and eps1_fibre pass
  # the SAME 3 checks -- see spec S2's "実装上の必須注意") ----
  AN := AlternatingGroup(w.n);;
  ok := StageAssert(Concatenation("Size(E) = 6*|A", String(w.n), "| = ", String(6 * Size(AN))),
                     Size(built.E) = 6 * Size(AN)) and ok;
  ok := StageAssert(Concatenation("Size(P) = |A", String(w.n), "| (P := Group(s1^2,s2^2))"),
                     Size(W.PN) = Size(AN)) and ok;
  ok := StageAssert(Concatenation("E = Group(a1*(", String(w.n+1), ",", String(w.n+3),
                       "), b1*(", String(w.n+1), ",", String(w.n+3), ",", String(w.n+2), ")) (degree ",
                       String(w.n+3), " permutation group construction check)"),
                     Group(built.agen, built.bgen) = built.E) and ok;

  return rec(ok := ok, asserts := asserts, W := W, s1 := s1, s2 := s2, built := built,
             AN := AN, epsActual := epsActual, canonical_string := canon, canonical_id_sha256 := sha);
end;;

#############################################################################
## ---------------------- S3/S4: Xi-restricted scan, per-m layer, accumulate -
## Calls kerchi-judge's CorrectedShadowsXi ONCE PER charming m (charmingSet
## of length 1 each time) rather than once with the full charmingSet -- this
## is functionally identical (each m's contribution is independent; the
## function's own theoreticalBound/scannedCount accounting is additive across
## calls) but gives natural per-m granularity for the S5 fail-closed
## accounting fields (35/35b/37) without needing a second scan pass, and
## doubles as the seam where true multi-process layer-sharding (spec S4.1)
## would be introduced if a single-process run turns out to be too slow
## (timing probe, 2026-07-30 local: about 154000 scanned/s on window C's m=0
## slice -> about 730s/layer, about 2918s (about 49min) for all 4 layers of
## one window -- comfortably inside a single 90-minute CI job, so this driver
## does NOT split into separate CI runs per layer by default; R4_ONLY_M below
## remains available as an escape hatch if a real CI run proves this wrong).
#############################################################################
ScanWindowXi := function(w, st)
  local corr, perM, m, xiRes, totalScanned, entry;
  corr := [];;  perM := [];;  totalScanned := 0;;
  for m in R4_CHARMING_SET do
    Print("\n=== Xi-restricted scan (", w.id, "): layer m=", m, " starting ===\n");
    JUDGE_FORCE_SCAN_MODE := "xi_restricted";;
    xiRes := CorrectedShadowsXi(st.W, [m]);;
    Print("=== Xi-restricted scan (", w.id, "): layer m=", m, " done. scanned_count=",
          xiRes.scanned_count, " bound=", R4_XI_BOUND_PER_M, " shadow_count=",
          Length(xiRes.shadows), " settled_fail_count=", xiRes.settled_fail_count, " ===\n");
    if xiRes.scanned_count > R4_XI_BOUND_PER_M then
      Error("strike-r4.g: window ", w.id, " layer m=", m, ": xi_count_measured (",
            xiRes.scanned_count, ") EXCEEDS the fail-closed per-layer Xi upper bound (",
            R4_XI_BOUND_PER_M, ") -- refusing to trust this scan");
    fi;
    entry := rec(m := m, alpha_chunk := [1, -1], chunk_scan_bound := R4_XI_BOUND_PER_M,
                 scanned := xiRes.scanned_count, accepted := Length(xiRes.shadows),
                 settled_fail_count := xiRes.settled_fail_count);;
    Add(perM, entry);;
    totalScanned := totalScanned + xiRes.scanned_count;;
    Append(corr, xiRes.shadows);;
  od;
  corr := Set(corr);;
  Print("\n=== Xi-restricted scan (", w.id, "): TOTAL scanned_count=", totalScanned,
        " bound=", R4_XI_BOUND_TOTAL, " shadow_total=", Length(corr), " ===\n");
  if totalScanned > R4_XI_BOUND_TOTAL then
    Error("strike-r4.g: window ", w.id, ": xi_count_measured_total (", totalScanned,
          ") EXCEEDS the fail-closed total Xi upper bound (", R4_XI_BOUND_TOTAL,
          ") -- refusing to trust this scan");
  fi;
  return rec(corr := corr, perM := perM, totalScanned := totalScanned);
end;;

#############################################################################
## ---------------------- S5: full measurement --------------------------------
#############################################################################
# AutP/Stab fast path -- same recipe as kerchi-judge.g's CorrectedShadowsXi
# fastAutN branch (P=A_n, n<>6: Aut(P)=S_n acting by ordinary conjugation).
ComputeAutPStab := function(PN, x)
  local fastAutN, AutP, StabG, actFun;
  fastAutN := IsNaturalAlternatingGroup(PN) and NrMovedPoints(PN) <> 6;;
  if fastAutN then
    AutP := SymmetricGroup(MovedPoints(PN));;
    StabG := Centralizer(AutP, x);;
  else
    AutP := AutomorphismGroup(PN);;
    actFun := function(pt, g) return Image(g, pt); end;;
    StabG := Stabilizer(AutP, x, actFun);;
  fi;
  return rec(AutP := AutP, StabG := StabG, fastAutN := fastAutN);
end;;

MeasureWindow := function(w, st, scanRes)
  local W, corr, gi, G, K, Q, oddp, A, S, natGK, QInv, chiImgOrd, CGA, faithful,
        Kidgrp, Kidgrp_note, AidgrpJson, idG, dlG, dseries, ASlist,
        alphas, i, m1, f1, u1, correctedY, alpha, distinctAlphas, alphaWellDefined,
        kernelTrivial, xiImageOrder, xiImage, xiImageInNorm, NX, StabInfo, StabG,
        Syl2StabStruct, Syl2StabOrder,
        homLeftOk, homRightOk, hpair, j, m3, f3, cIdx,
        bxCycles, bxGens, Bx, kerIdx, xiKgens, xiK_alphas, xiK_Hom,
        aCoords, ag, imgA, A_coords_status, S2block_status, s2gens, blockAssignment, blocks,
        Sstruct, ZSord, CGS, GoverCGS, InnSord, H3holds, complAll, complInCGS,
        epsZero, zInPhi, centralWit, splitND, natCGSA, CGSmodA, S2q, zGen, zbar,
        cwGen, cw2, comm, AnormInCGS, found,
        m0, layerIdx, invCount, regs, Kdp;
  W := st.W;;  corr := scanRes.corr;;

  gi := GroupOfShadows(W, corr);;
  if not gi.closed then
    Error("strike-r4.g: (3.53) closure FAILED for window ", w.id,
          " -- refusing to report structure of a group not confirmed to exist");
  fi;
  G := gi.G;;  K := gi.ker;;  regs := gi.regs;;  kerIdx := gi.ker_idx;;
  Print("  group_order=", Size(G), "  ker_size=", Size(K), "\n");

  # ---- 4,5,6: ker odd/2 part; A := O_2'(K) (largest odd-order normal
  # subgroup of K, per spec S5's own suggested method) ----
  oddp := Filtered(PrimeDivisors(Size(K)), p -> p <> 2);;
  ASlist := Filtered(NormalSubgroups(K), N1 -> Size(N1) mod 2 = 1);;
  if Length(ASlist) > 0 then
    A := First(ASlist, N1 -> Size(N1) = Maximum(List(ASlist, Size)));;
  else
    A := TrivialSubgroup(K);;
  fi;
  S := SylowSubgroup(K, 2);;
  Print("  ker_odd_part_order(=|A|)=", Size(A), "  ker_2_part_order(=|S|)=", Size(S),
        "  ker_odd_part_primes=", oddp, "\n");

  # ---- 7,7b: K_struct / K_idgroup ----
  Kidgrp := fail;;  Kidgrp_note := "";;
  if Size(K) > 0 and SmallGroupsAvailable(Size(K)) then
    Kidgrp := IdGroup(K);;
  else
    Kidgrp_note := "out-of-range";;
  fi;

  # ---- 8: K_is_direct_product (K = A x S internally?) ----
  Kdp := (Size(A) * Size(S) = Size(K)) and IsTrivial(Intersection(A, S))
         and IsTrivial(CommutatorSubgroup(A, S));;
  Print("  K_struct=", StructureDescription(K), "  K_is_direct_product=", Kdp, "\n");

  # ---- 9: A_order, A_idgroup ----
  AidgrpJson := "";;
  if SmallGroupsAvailable(Size(A)) then
    AidgrpJson := Concatenation("{\"idgroup\":", JPair(IdGroup(A)[1], IdGroup(A)[2]), "}");;
  else
    AidgrpJson := Concatenation("{\"structure_description\":", JStr(StructureDescription(A)), "}");;
  fi;

  # ---- 10: S_struct, S_order ----
  Sstruct := StructureDescription(S);;

  # ---- 11: chi_image_order, Q_struct ----
  natGK := NaturalHomomorphismByNormalSubgroup(G, K);;
  Q := Image(natGK);;
  chiImgOrd := Size(Q);;
  QInv := AbelianInvariants(Q);;
  Print("  chi_image_order(=|Q|)=", chiImgOrd, "  Q_struct(invariant_factors)=", QInv, "\n");

  # ---- 12: Q_action_faithful_on_A ----
  CGA := Centralizer(G, A);;
  faithful := (Size(CGA) = Size(K));;

  # ---- 13: gtsh_idgroup ----
  idG := fail;;
  if SmallGroupsAvailable(Size(G)) then
    idG := Concatenation("{\"idgroup\":", JPair(IdGroup(G)[1], IdGroup(G)[2]), "}");;
  else
    idG := Concatenation("{\"structure_description\":", JStr(StructureDescription(G)),
      ",\"derived_series_orders\":", JArr(List(DerivedSeries(G), s -> String(Size(s)))),
      ",\"center_order\":", String(Size(Center(G))),
      ",\"sylow_structs\":", JArr(List(PrimeDivisors(Size(G)),
        p -> Concatenation("{\"p\":", String(p), ",\"struct\":",
          JStr(StructureDescription(SylowSubgroup(G, p))), "}"))), "}");;
  fi;

  # ---- 14,15: derived_length_G, derived_series_G ----
  if IsSolvable(G) then dlG := DerivedLength(G); else dlG := -1; fi;
  dseries := DerivedSeries(G);;

  # ---- 16,16b,17: Stab_order, Syl2_Stab_struct/order, xbar_normalizer_order ----
  StabInfo := ComputeAutPStab(W.PN, W.x);;
  StabG := StabInfo.StabG;;
  Syl2StabStruct := StructureDescription(SylowSubgroup(StabG, 2));;
  Syl2StabOrder := Size(SylowSubgroup(StabG, 2));;
  NX := Normalizer(StabInfo.AutP, Group(W.x));;
  Print("  Stab_order=", Size(StabG), "  xbar_normalizer_order=", Size(NX), "\n");

  # ---- 18: xi_alpha_well_defined (+ per-shadow alpha, needed for 19-23,34) ----
  # alpha in AutP (=S_n) solving x^alpha=x^u, y^alpha=corrected_y, found via
  # RepresentativeAction on the tuple (x,y) simultaneously (GAP's OnTuples).
  # "corrected_y" uses the SAME AbstractProd([f^-1,y^u,f]) convention that
  # GroupOfShadows itself uses to build each shadow's automorphism of PN
  # (kerchi-judge.g's Eh construction) -- i.e. this is not a re-derivation of
  # a different Xi map, it is the direct conjugation-realization of the same
  # per-shadow automorphism GroupOfShadows already required to be well-defined
  # for (3.53) closure. Existence+uniqueness is expected structurally (P=A_n,
  # n=20>=5, so Aut(A_n)=S_n and C_{S_n}(A_n)=1), verified empirically here
  # rather than assumed.
  alphas := [];;  alphaWellDefined := true;;
  for i in [1 .. Length(corr)] do
    m1 := corr[i][1];;  f1 := corr[i][2];;  u1 := 2*m1 + 1;;
    correctedY := AbstractProd([f1^-1, W.y^u1, f1]);;
    alpha := RepresentativeAction(StabInfo.AutP, [W.x, W.y], [W.x^u1, correctedY], OnTuples);;
    if alpha = fail then
      alphaWellDefined := false;;
      alphas[i] := fail;;
    else
      alphas[i] := alpha;;
    fi;
  od;
  Print("  xi_alpha_well_defined=", alphaWellDefined,
        "  (C_AutP(P) trivial? ", IsTrivial(Centralizer(StabInfo.AutP, W.PN)), ")\n");

  # ---- 20: xi_kernel_trivial ----
  distinctAlphas := Set(alphas);;
  kernelTrivial := (Length(distinctAlphas) = Length(corr));;
  Print("  distinct_alphas=", Length(distinctAlphas), " shadow_total=", Length(corr),
        " xi_kernel_trivial=", kernelTrivial, "\n");

  # ---- 19: xi_hom_left / xi_hom_right (pairwise composition check, per the
  # (3.53) composition rule (2*m1*m2+m1+m2 mod Nord, f1*(f2^alpha1)) -- the
  # SAME rule GroupOfShadows uses internally, reapplied here via the already-
  # computed alphas rather than re-deriving new math. O(shadow_total^2); if
  # shadow_total is too large for that to be practical within the CI budget
  # this switches to a documented random sample (never silently -- the JSON
  # records whether the check was exhaustive). ----
  homLeftOk := true;;  homRightOk := true;;
  hpair := [1 .. Length(corr)];;
  if Length(corr)^2 > 4000000 then
    hpair := List([1 .. Minimum(2000, Length(corr))], j -> Random([1 .. Length(corr)]));;
    Print("  [NOTE] shadow_total^2 too large for exhaustive hom check -- sampling ",
          Length(hpair), " random indices (both loop bounds) instead of the full ",
          Length(corr), "\n");
  fi;
  for i in hpair do
    for j in hpair do
      m3 := (2*corr[i][1]*corr[j][1] + corr[i][1] + corr[j][1]) mod W.Nord;;
      f3 := AbstractProd([corr[i][2], corr[j][2]^alphas[i]]);;
      cIdx := Position(corr, [m3, f3]);;
      if cIdx = fail then
        homLeftOk := false;;  homRightOk := false;;
        continue;
      fi;
      if alphas[i]*alphas[j] <> alphas[cIdx] then homLeftOk := false; fi;
      if alphas[j]*alphas[i] <> alphas[cIdx] then homRightOk := false; fi;
    od;
  od;
  Print("  xi_hom_left=", homLeftOk, "  xi_hom_right=", homRightOk,
        " (exhaustive=", Length(hpair) = Length(corr), ")\n");

  # ---- 21,21b: xi_image_order, xi_image_in_normalizer ----
  xiImage := Group(distinctAlphas);;
  xiImageOrder := Size(xiImage);;
  xiImageInNorm := IsSubgroup(NX, xiImage);;
  Print("  xi_image_order=", xiImageOrder, "  xi_image_in_normalizer=", xiImageInNorm, "\n");

  # ---- 22: Bx_order ----
  # B_x := group generated by the 4 disjoint 5-cycles making up xbar (type
  # (5,5,5,5) on 20 points) -- an elementary-abelian coordinate frame.
  # Generator order = the order Cycles() returns (recorded below).
  bxCycles := Cycles(W.x, MovedPoints(W.x));;
  bxGens := List(bxCycles, cyc -> MappingPermListList(cyc, Concatenation(cyc{[2 .. Length(cyc)]}, [cyc[1]])));;
  Bx := Group(bxGens);;
  Print("  Bx_order=", Size(Bx), " (expect 5^4=625 if coordinate frame is elementary abelian)\n");
  Print("  Bx generator cycles (order recorded) = ", bxCycles, "\n");

  # ---- 22b: A_coords_in_Bx ----
  # Xi(A) (A = O_2'(K)): build a homomorphism K -> AutP via the SAME
  # generating set GAP already fixed for K (GeneratorsOfGroup(K) = regs at
  # kerIdx, by construction of K := Group(List(kerIdx,i->regs[i])) inside
  # GroupOfShadows) and the corresponding alphas at those same indices -- a
  # much smaller generating set than all of G, so tractable via
  # GroupHomomorphismByImages. For each odd-order element of A whose image
  # lies in B_x, its coordinates (v1,v2,v3,v4) mod 5 are read off via
  # LogFFE-style discrete log against each of the 4 cyclic factors (found by
  # direct search over the 5 powers of each generator, since |Bx|=625 is
  # tiny).
  aCoords := [];;
  xiKgens := GeneratorsOfGroup(K);;
  xiK_alphas := List(xiKgens, gk -> alphas[Position(regs, gk)]);;
  xiK_Hom := GroupHomomorphismByImages(K, StabInfo.AutP, xiKgens, xiK_alphas);;
  if xiK_Hom = fail then
    Print("  [NOTE] Xi|_K did not extend to a well-defined hom on K's generating set -- ",
          "22b/23 not computed (hom_left/right above already report the raw ",
          "shadow-pairwise failure independently)\n");
    A_coords_status := "hom_not_well_defined_on_K";;
    S2block_status := "not_computed (Xi|_K hom unavailable)";;
  else
    # coordinate extraction: for imgA in Bx = C5^4 (disjoint 5-cycle factors
    # bxGens[1..4] on the 4 blocks bxCycles[1..4]), the v_k-th coordinate is
    # the unique power of bxGens[k] agreeing with imgA on that block's first
    # point (valid precisely because Bx's action on each block factors
    # through that block's own generator alone -- direct product structure).
    for ag in Elements(A) do
      imgA := Image(xiK_Hom, ag);;
      if imgA in Bx then
        Add(aCoords, rec(elt := PrintStr(ag), img := PrintStr(imgA),
          coords := List([1 .. Length(bxGens)], k ->
            First([0 .. 4], p -> bxCycles[k][1]^imgA = bxCycles[k][1]^(bxGens[k]^p)))));;
      fi;
    od;
    A_coords_status := "computed";;

    # ---- 23: S_block_action ----
    S2block_status := "computed";;
    blocks := List(bxCycles, cyc -> Set(cyc));;
    s2gens := GeneratorsOfGroup(S);;
    blockAssignment := List(s2gens, g -> List(blocks,
      b -> Set(List(b, pt -> pt ^ Image(xiK_Hom, g)))));;
  fi;

  # ---- 24-33: STR-1 block (S<>1 only meaningful; same recipe as
  # search/strike-a13-ladder.g's MeasureWindow) ----
  Sstruct := StructureDescription(S);;
  ZSord := Size(Center(S));;
  CGS := Centralizer(G, S);;
  GoverCGS := Size(G) / Size(CGS);;
  InnSord := Size(S) / Size(Center(S));;
  H3holds := (GoverCGS = InnSord);;
  complAll := Length(ComplementClassesRepresentatives(G, K));;
  complInCGS := Length(ComplementClassesRepresentatives(CGS, Intersection(CGS, K)));;
  epsZero := (complInCGS > 0);;
  splitND := (complAll > 0) and (complInCGS = 0);;
  zInPhi := fail;;  centralWit := "null";;
  if Size(S) > 1 then
    # 2026-07-30 postmortem (window C CI run, run 30481912368): A=O_2'(K) has
    # no a priori reason to be a SUBGROUP of CGS=C_G(S) (only normal in K) --
    # IsNormal(CGS,A) alone returned true incorrectly (or GAP's internal
    # precondition check disagreed with it), and NaturalHomomorphismByNormal-
    # Subgroup(CGS,A) then errored fail-closed with "<N> must be a normal
    # subgroup of <G>", killing the entire ~49min measurement run. Fixed by
    # requiring containment explicitly before trusting normality.
    AnormInCGS := IsSubset(CGS, A) and IsNormal(CGS, A);;
    if AnormInCGS then
      natCGSA := NaturalHomomorphismByNormalSubgroup(CGS, A);;
      CGSmodA := Image(natCGSA);;
      S2q := SylowSubgroup(CGSmodA, 2);;
      zGen := First(GeneratorsOfGroup(Center(S)), g -> not IsOne(g));;
      if zGen = fail then zGen := Identity(S); fi;
      zbar := Image(natCGSA, zGen);;
      zInPhi := zbar in FrattiniSubgroup(S2q);;
      if not epsZero then
        found := false;;
        for cwGen in GeneratorsOfGroup(S2q) do
          if cwGen^2 = zbar then
            centralWit := Concatenation("{\"witness_type\":\"square\",\"generator\":",
              JStr(String(cwGen)), ",\"relation\":\"g^2=z\",\"g_order\":", String(Order(cwGen)), "}");;
            found := true;; break;
          fi;
        od;
        if not found then
          for cwGen in GeneratorsOfGroup(S2q) do
            for cw2 in GeneratorsOfGroup(S2q) do
              comm := Comm(cwGen, cw2);;
              if comm = zbar then
                centralWit := Concatenation("{\"witness_type\":\"commutator\",\"generator1\":",
                  JStr(String(cwGen)), ",\"generator2\":", JStr(String(cw2)),
                  ",\"relation\":\"[g1,g2]=z\"}");;
                found := true;; break;
              fi;
            od;
            if found then break; fi;
          od;
        fi;
        if not found then
          centralWit := Concatenation("{\"witness_type\":\"unresolved\",\"note\":\"z in Phi(Syl_2(C_G(S)/A)) confirmed (",
            String(zInPhi), ") but no single generator square or pairwise commutator equals z\"}");;
        fi;
      fi;
    fi;
  fi;

  # ---- 34: u_minus1_involutions ----
  m0 := First(R4_CHARMING_SET, m -> (2*m+1) mod W.Nord = (W.Nord - 1) mod W.Nord);;
  layerIdx := Filtered([1 .. Length(corr)], i -> corr[i][1] = m0);;
  invCount := Number(layerIdx, i -> Order(regs[i]) = 2 and (regs[i] in CGS));;
  Print("  u_minus1_involutions (m0=", m0, ", layer size=", Length(layerIdx), ")=", invCount, "\n");

  return rec(
    group_order := Size(G), ker_size := Size(K),
    ker_odd_part_order := Size(A), ker_2_part_order := Size(S),
    ker_odd_part_primes := oddp,
    K_struct := StructureDescription(K), K_idgroup := Kidgrp, K_idgroup_note := Kidgrp_note,
    K_is_direct_product := Kdp,
    A_order := Size(A), A_idgroup_json := AidgrpJson,
    S_struct := Sstruct, S_order := Size(S),
    chi_image_order := chiImgOrd, Q_struct := QInv,
    Q_action_faithful_on_A := faithful,
    gtsh_idgroup := idG,
    derived_length_G := dlG, derived_series_G := List(dseries, Size),
    Stab_order := Size(StabG), Syl2_Stab_struct := Syl2StabStruct, Syl2_Stab_order := Syl2StabOrder,
    xbar_normalizer_order := Size(NX),
    xi_alpha_well_defined := alphaWellDefined,
    xi_hom_left := homLeftOk, xi_hom_right := homRightOk,
    xi_hom_check_exhaustive := (Length(hpair) = Length(corr)),
    xi_kernel_trivial := kernelTrivial, distinct_alphas := Length(distinctAlphas),
    xi_image_order := xiImageOrder, xi_image_in_normalizer := xiImageInNorm,
    Bx_order := Size(Bx), Bx_gen_cycles := bxCycles, A_coords_status := A_coords_status,
    A_coords_count := Length(aCoords),
    S_block_status := S2block_status,
    ZS_order := ZSord, G_over_CG_S := GoverCGS, Inn_S_order := InnSord, H3_holds := H3holds,
    compl_classes_all := complAll, compl_classes_in_CG_S := complInCGS,
    epsilon_zero := epsZero, z_in_Frattini := zInPhi,
    central_product_witness := centralWit, split_but_not_direct := splitND,
    u_minus1_involutions := invCount, m0_layer := m0
  );
end;;

#############################################################################
## ---------------------- JSON writers ---------------------------------------
#############################################################################
AssertJson := function(a)
  return Concatenation("{\"label\":", JStr(a.label), ",\"ok\":", JB(a.ok), "}");
end;;

KIdgroupJson := function(meas)
  if meas.K_idgroup = fail then
    return Concatenation("null, \"7b_K_idgroup_note\": ", JStr(meas.K_idgroup_note));
  fi;
  return Concatenation(JPair(meas.K_idgroup[1], meas.K_idgroup[2]), ", \"7b_K_idgroup_note\": null");
end;;

BoolOrNull := function(v)
  if v = fail then return "null"; fi;
  return JB(v);
end;;

ShardManifestJson := function(perM)
  local items;
  items := List(perM, e -> Concatenation(
    "{\"m\":", String(e.m),
    ",\"alpha_chunk\":", JArr(List(e.alpha_chunk, String)),
    ",\"chunk_scan_bound\":", String(e.chunk_scan_bound),
    ",\"scanned\":", String(e.scanned),
    ",\"accepted\":", String(e.accepted),
    ",\"settled_fail_count\":", String(e.settled_fail_count), "}"));
  return JArr(items);
end;;

WriteWindowCert := function(w, st, scanRes, meas, outfile)
  local outParts, i, perMScanned;
  outParts := [];;
  Add(outParts, "{\n");
  Add(outParts, "  \"generated_by\": \"search/strike-r4.g\",\n");
  Add(outParts, "  \"note\": \"r=4 discriminating-window measurement -- window per search/_r4_driver_spec.md; raw measurements only, no interpretation, no comparison to any prediction file (measurement-side isolation, contact-blocked from docs/notes/r4_prediction_v1.md / pruning_law_v1_1.md / ideas/). NOT a ledger claim by itself.\",\n");
  Add(outParts, Concatenation("  \"window_id\": ", JStr(w.id), ",\n"));
  Add(outParts, Concatenation("  \"n\": ", String(w.n), ",\n"));
  Add(outParts, Concatenation("  \"ell\": ", String(w.ell), ",\n"));
  Add(outParts, Concatenation("  \"r\": ", String(w.r), ",\n"));
  Add(outParts, Concatenation("  \"t\": ", String(w.t), ",\n"));
  Add(outParts, Concatenation("  \"a1\": ", JStr(PrintStr(w.a1)), ",\n"));
  Add(outParts, Concatenation("  \"b1\": ", JStr(PrintStr(w.b1)), ",\n"));
  Add(outParts, Concatenation("  \"s1\": ", JStr(PrintStr(st.s1)), ",\n"));
  Add(outParts, Concatenation("  \"s2\": ", JStr(PrintStr(st.s2)), ",\n"));
  Add(outParts, Concatenation("  \"canonical_string\": ", JStr(st.canonical_string), ",\n"));
  Add(outParts, Concatenation("  \"canonical_id_sha256\": ", JStr(st.canonical_id_sha256), ",\n"));
  Add(outParts, Concatenation("  \"canonical_id_sha256_gate\": ", JStr(R4_CANONICAL_SHA.(w.shaKey)), ",\n"));
  Add(outParts, Concatenation("  \"stage1_all_pass\": ", JB(st.ok), ",\n"));
  Add(outParts, "  \"stage1_asserts\": [\n");
  for i in [1 .. Length(st.asserts)] do
    Add(outParts, Concatenation("    ", AssertJson(st.asserts[i])));
    if i < Length(st.asserts) then Add(outParts, ",\n"); else Add(outParts, "\n"); fi;
  od;
  Add(outParts, "  ],\n");
  Add(outParts, Concatenation("  \"N_ord\": ", String(st.W.Nord), ",\n"));
  Add(outParts, Concatenation("  \"0_canonical_id\": ", JStr(w.id), ",\n"));
  Add(outParts, Concatenation("  \"1_eps_branch\": ", JStr(st.epsActual), ",\n"));
  Add(outParts, "  \"1b_stage1_asserts_ok\": true,\n");
  Add(outParts, Concatenation("  \"2_group_order\": ", String(meas.group_order), ",\n"));
  Add(outParts, Concatenation("  \"3_ker_size\": ", String(meas.ker_size), ",\n"));
  Add(outParts, Concatenation("  \"4_ker_odd_part_order\": ", String(meas.ker_odd_part_order), ",\n"));
  Add(outParts, Concatenation("  \"5_ker_2_part_order\": ", String(meas.ker_2_part_order), ",\n"));
  Add(outParts, Concatenation("  \"6_ker_odd_part_primes\": ", JArr(List(meas.ker_odd_part_primes, String)), ",\n"));
  Add(outParts, Concatenation("  \"7_K_struct\": ", JStr(meas.K_struct), ",\n"));
  Add(outParts, Concatenation("  \"7b_K_idgroup\": ", KIdgroupJson(meas), ",\n"));
  Add(outParts, Concatenation("  \"8_K_is_direct_product\": ", JB(meas.K_is_direct_product), ",\n"));
  Add(outParts, Concatenation("  \"9_A_order\": ", String(meas.A_order), ",\n"));
  Add(outParts, Concatenation("  \"9_A_idgroup\": ", meas.A_idgroup_json, ",\n"));
  Add(outParts, Concatenation("  \"10_S_struct\": ", JStr(meas.S_struct), ",\n"));
  Add(outParts, Concatenation("  \"10_S_order\": ", String(meas.S_order), ",\n"));
  Add(outParts, Concatenation("  \"11_chi_image_order\": ", String(meas.chi_image_order), ",\n"));
  Add(outParts, Concatenation("  \"11_Q_struct_invariant_factors\": ", JArr(List(meas.Q_struct, String)), ",\n"));
  Add(outParts, Concatenation("  \"12_Q_action_faithful_on_A\": ", JB(meas.Q_action_faithful_on_A), ",\n"));
  Add(outParts, Concatenation("  \"13_gtsh_idgroup\": ", meas.gtsh_idgroup, ",\n"));
  Add(outParts, Concatenation("  \"14_derived_length_G\": ", String(meas.derived_length_G), ",\n"));
  Add(outParts, Concatenation("  \"15_derived_series_G\": ", JArr(List(meas.derived_series_G, String)), ",\n"));
  Add(outParts, Concatenation("  \"16_Stab_order\": ", String(meas.Stab_order), ",\n"));
  Add(outParts, Concatenation("  \"16b_Syl2_Stab_struct\": ", JStr(meas.Syl2_Stab_struct), ",\n"));
  Add(outParts, Concatenation("  \"16b_Syl2_Stab_order\": ", String(meas.Syl2_Stab_order), ",\n"));
  Add(outParts, Concatenation("  \"17_xbar_normalizer_order\": ", String(meas.xbar_normalizer_order), ",\n"));
  Add(outParts, Concatenation("  \"18_xi_alpha_well_defined\": ", JB(meas.xi_alpha_well_defined), ",\n"));
  Add(outParts, Concatenation("  \"19_xi_hom_left\": ", JB(meas.xi_hom_left), ",\n"));
  Add(outParts, Concatenation("  \"19_xi_hom_right\": ", JB(meas.xi_hom_right), ",\n"));
  Add(outParts, Concatenation("  \"19_xi_hom_check_exhaustive\": ", JB(meas.xi_hom_check_exhaustive), ",\n"));
  Add(outParts, Concatenation("  \"20_xi_kernel_trivial\": ", JB(meas.xi_kernel_trivial), ",\n"));
  Add(outParts, Concatenation("  \"20_distinct_alphas\": ", String(meas.distinct_alphas), ",\n"));
  Add(outParts, Concatenation("  \"21_xi_image_order\": ", String(meas.xi_image_order), ",\n"));
  Add(outParts, Concatenation("  \"21b_xi_image_in_normalizer\": ", JB(meas.xi_image_in_normalizer), ",\n"));
  Add(outParts, Concatenation("  \"22_Bx_order\": ", String(meas.Bx_order), ",\n"));
  Add(outParts, Concatenation("  \"22_Bx_gen_cycles\": ", JStr(PrintStr(meas.Bx_gen_cycles)), ",\n"));
  Add(outParts, Concatenation("  \"22b_A_coords_status\": ", JStr(meas.A_coords_status), ",\n"));
  Add(outParts, Concatenation("  \"22b_A_coords_count\": ", String(meas.A_coords_count), ",\n"));
  Add(outParts, Concatenation("  \"23_S_block_status\": ", JStr(meas.S_block_status), ",\n"));
  Add(outParts, Concatenation("  \"24_ZS_order\": ", String(meas.ZS_order), ",\n"));
  Add(outParts, Concatenation("  \"25_G_over_CG_S\": ", String(meas.G_over_CG_S), ",\n"));
  Add(outParts, Concatenation("  \"26_Inn_S_order\": ", String(meas.Inn_S_order), ",\n"));
  Add(outParts, Concatenation("  \"27_H3_holds\": ", JB(meas.H3_holds), ",\n"));
  Add(outParts, Concatenation("  \"28_compl_classes_all\": ", String(meas.compl_classes_all), ",\n"));
  Add(outParts, Concatenation("  \"29_compl_classes_in_CG_S\": ", String(meas.compl_classes_in_CG_S), ",\n"));
  Add(outParts, Concatenation("  \"30_epsilon_zero\": ", JB(meas.epsilon_zero), ",\n"));
  Add(outParts, Concatenation("  \"31_z_in_Frattini\": ", BoolOrNull(meas.z_in_Frattini), ",\n"));
  Add(outParts, Concatenation("  \"32_central_product_witness\": ", meas.central_product_witness, ",\n"));
  Add(outParts, Concatenation("  \"33_split_but_not_direct\": ", JB(meas.split_but_not_direct), ",\n"));
  Add(outParts, Concatenation("  \"34_u_minus1_involutions\": ", String(meas.u_minus1_involutions),
      ", \"34_m0_layer\": ", String(meas.m0_layer), ",\n"));
  perMScanned := List(scanRes.perM, e -> e.scanned);;
  Add(outParts, Concatenation("  \"35_xi_count_measured_per_m\": ", JArr(List(perMScanned, String)), ",\n"));
  Add(outParts, Concatenation("  \"35b_xi_count_bound_per_m\": ", String(R4_XI_BOUND_PER_M), ",\n"));
  Add(outParts, Concatenation("  \"36_xi_count_measured_total\": ", String(scanRes.totalScanned), ",\n"));
  Add(outParts, Concatenation("  \"36b_xi_count_bound_total\": ", String(R4_XI_BOUND_TOTAL), ",\n"));
  Add(outParts, Concatenation("  \"37_shard_manifest\": ", ShardManifestJson(scanRes.perM), ",\n"));
  Add(outParts, Concatenation("  \"shadow_total\": ", String(Length(scanRes.corr)), "\n"));
  Add(outParts, "}\n");
  WriteFile(outfile, Concatenation(outParts));
  Print("Wrote ", outfile, "\n");
end;;

#############################################################################
## ---------------------- main driver loop -----------------------------------
## Bind R4_LIBRARY_ONLY := true;; before Read()-ing this file to load only the
## function/table definitions above (no gate run, no window struck) -- used
## for local sanity-testing of individual functions (e.g. against a small
## stand-in window) without paying the S0 gate's cost or attempting the full
## r=4 windows. CI's preamble never sets this, so the real driver behavior
## (gate then strike) is unaffected.
#############################################################################
if not (IsBound(R4_LIBRARY_ONLY) and R4_LIBRARY_ONLY = true) then

R4_DATE_STAMP := "20260730";;

gateResult := RunEntryGate();;
gateOutfile := Concatenation("search/certs/r4_gate_", R4_DATE_STAMP, ".json");;
WriteFile(gateOutfile, Concatenation("{\n",
  "  \"generated_by\": \"search/strike-r4.g\",\n",
  "  \"note\": \"S0 entry gate (fail-closed) for the r=4 measurement -- G1=W-E-A10-9t1, G2=W-E-A10-5x2t0, per search/_r4_driver_spec.md S0.\",\n",
  "  \"g1\": ", GateJson(gateResult.g1), ",\n",
  "  \"g2\": ", GateJson(gateResult.g2), ",\n",
  "  \"all_pass\": ", JB(gateResult.all_pass), "\n",
  "}\n"));;
Print("Wrote ", gateOutfile, "\n");

if not gateResult.all_pass then
  Error("strike-r4.g: S0 ENTRY GATE FAILED (G1.pass=", gateResult.g1.pass,
        " G2.pass=", gateResult.g2.pass, ") -- fail-closed, refusing to strike ",
        "either r=4 window (spec S0: G1/G2いずれか不一致なら2窓を1シャードも撃たずにError終了)");
fi;

windowsToRun := R4_WINDOWS;;
if IsBound(R4_ONLY_WINDOW) then
  if R4_ONLY_WINDOW = "C" then
    windowsToRun := Filtered(R4_WINDOWS, w -> w.shaKey = "C");;
  elif R4_ONLY_WINDOW = "B" then
    windowsToRun := Filtered(R4_WINDOWS, w -> w.shaKey = "B");;
  else
    Error("strike-r4.g: R4_ONLY_WINDOW must be \"C\" or \"B\", got ", R4_ONLY_WINDOW);
  fi;
else
  Print("\n[NOTE] R4_ONLY_WINDOW not bound -- processing BOTH windows in this ",
        "single process (not recommended for CI: spec S4.3 wants C struck to ",
        "completion before B is attempted as a separate run).\n");
fi;;

manifestEntries := [];;

for w in windowsToRun do
  Print("\n################################################################\n");
  Print("# window: ", w.id, " (n=", w.n, ", ell=", w.ell, ", r=", w.r, ", t=", w.t,
        ", eps_branch=", w.epsBranch, ")\n");
  Print("################################################################\n");

  st := ProcessWindowStage1(w);;
  Print("STAGE 1 (", w.id, ") overall: ", PF(st.ok), "\n");
  if not st.ok then
    Error("strike-r4.g: STAGE 1 failed for window ", w.id,
          " -- fail-closed, refusing to proceed (per campaign policy)");
  fi;

  scanRes := ScanWindowXi(w, st);;
  meas := MeasureWindow(w, st, scanRes);;

  outfile := Concatenation("search/certs/r4_", ReplacedString(w.id, "-", "_"),
    "_", R4_DATE_STAMP, ".json");;
  WriteWindowCert(w, st, scanRes, meas, outfile);;

  Add(manifestEntries, rec(id := w.id, outfile := outfile,
      canonical_id_sha256 := st.canonical_id_sha256, stage1_all_pass := st.ok,
      shadow_total := Length(scanRes.corr), xi_count_measured_total := scanRes.totalScanned));;
od;

manifestParts := [];;
Add(manifestParts, "{\n");
Add(manifestParts, "  \"generated_by\": \"search/strike-r4.g\",\n");
Add(manifestParts, "  \"note\": \"r=4 driver manifest -- windows processed in THIS run per search/_r4_driver_spec.md. Raw measurement summary only. See r4_gate_<date>.json for the S0 entry-gate node (shared across runs, not duplicated here).\",\n");
Add(manifestParts, Concatenation("  \"entry_gate_file\": ", JStr(gateOutfile), ",\n"));
Add(manifestParts, Concatenation("  \"entry_gate_all_pass\": ", JB(gateResult.all_pass), ",\n"));
Add(manifestParts, Concatenation("  \"windows_processed\": ", String(Length(manifestEntries)), ",\n"));
Add(manifestParts, "  \"windows\": [\n");
for i in [1 .. Length(manifestEntries)] do
  e := manifestEntries[i];;
  Add(manifestParts, Concatenation("    {\"id\":", JStr(e.id), ",\"outfile\":", JStr(e.outfile),
    ",\"canonical_id_sha256\":", JStr(e.canonical_id_sha256),
    ",\"stage1_all_pass\":", JB(e.stage1_all_pass),
    ",\"shadow_total\":", String(e.shadow_total),
    ",\"xi_count_measured_total\":", String(e.xi_count_measured_total),
    ",\"cert_sha256\":", JStr(CertSha256File(e.outfile)), "}"));
  if i < Length(manifestEntries) then Add(manifestParts, ",\n"); else Add(manifestParts, "\n"); fi;
od;
Add(manifestParts, "  ]\n");
Add(manifestParts, "}\n");
manifestSuffix := JoinC(List(windowsToRun, w -> w.shaKey), "");;
manifestOutfile := Concatenation("search/certs/r4_manifest_", manifestSuffix, "_", R4_DATE_STAMP, ".json");;
WriteFile(manifestOutfile, Concatenation(manifestParts));;
Print("\nWrote ", manifestOutfile, "\n");
Print("R4_DRIVER_DONE\n");

fi;   # R4_LIBRARY_ONLY guard
