#############################################################################
# search/gaplib_common.g — 影工房 GAP 共通ヘッダ(最小版 gaplib/v1)
# 2026-07-26 ツール総点検で新設(司令塔発注・事例4「既知罠を各実装者が個別に
# 踏み直している」)。
#
# ── 仕様(仕様書優先の原則・docs/体制と道具.md「質問の免許」3)──────────────
# 入力:  なし(Read するだけ)。グローバルに以下を定義する:
#        JStr / JB / JoinC / JArr / JPair        … JSON 文字列ヘルパー
#        WriteFile                                … 整形抑止つきファイル書き出し
#        GAPLIB_VERSION / GAPLIB_DefaultCapSec    … 定数
#        GAPLIB_ElapsedMs / GAPLIB_WallElapsedMs  … 経過時間(CPU / 壁時計)
#        GAPLIB_CheckCap                          … cap 超過検査(超過時に印字)
# 使い方: リポジトリ直下から `.\gap.ps1 search\<script>.g` で実行するスクリプト
#        の冒頭に  Read("search/gaplib_common.g");  を置く(相対パスは直下基準)。
# 適用範囲: **新規スクリプト専用**(2026-07-26 発注条件)。既存スクリプト
#        (証明書ハッシュ台帳記録済み)は書き換えない。既存スクリプトは同名
#        ヘルパーを自前定義しているため、後から Read を足すと定義順で上書きに
#        なる — 足さないこと。
# 互換性: JStr/JB/JoinC/JArr/JPair/WriteFile は既存の逐語コピー群
#        (week3-battery-common.g ほか 15 ファイル)と**出力バイト同一**。
#        JoinC のみ線形時間版(下記罠(2)) — LEDGER 2026-07-19 で証明書ハッシュ
#        2/2 MATCH によりバイト同一性を実測済みの実装と同方式。
# 較正:  scratchpad のセルフテスト(総点検時に PASS)で旧実装との一致を確認。
#        新規スクリプト側の fixture 設計はこれに依存せず従来どおり行うこと。
#############################################################################

GAPLIB_VERSION := "gaplib/v1";;

# ================= 経過時間と cap =================
# 罠(3): この環境のスクリプト実行 cap は**壁時計 600 秒**(harness の上限
#   600000ms・事前登録 cap も「GAP 1 実行 <= 600 秒」— LEDGER 2026-07-18/19)。
#   Runtime() は CPU ms であり壁時計と乖離する(shard-b1 実測: 壁 612.0s vs
#   GAP 内部 596625ms — LEDGER 2026-07-19)。cap 判定は壁時計側で行い、超過が
#   見えたら対象集合の shard 分割で対処する(cap 例外の後付けは不可 — 同日裁定)。
GAPLIB_StartCpuMs := Runtime();;
GAPLIB_ElapsedMs := function() return Runtime() - GAPLIB_StartCpuMs; end;;
if IsBoundGlobal("NanosecondsSinceEpoch") then
  GAPLIB_StartWallNs := NanosecondsSinceEpoch();;
  GAPLIB_WallElapsedMs := function()
    return Int((NanosecondsSinceEpoch() - GAPLIB_StartWallNs) / 1000000);
  end;;
else
  GAPLIB_StartWallNs := fail;;
  GAPLIB_WallElapsedMs := GAPLIB_ElapsedMs;;   # fallback: CPU ms(近似)
fi;

GAPLIB_DefaultCapSec := 600.0;;

# 超過なら "[CAP EXCEEDED] <label> ..." を印字して true を返す(継続判断は呼び手)。
# 既存の書式慣行(week3-psl-S1.g「[CAP EXCEEDED] S1」・e19.g)に合わせている。
GAPLIB_CheckCap := function(capSec, label)
  local wallSec;
  wallSec := GAPLIB_WallElapsedMs() / 1000.0;
  if wallSec > capSec then
    Print("[CAP EXCEEDED] ", label, " wall=", wallSec, "s cap=", capSec, "s\n");
    return true;
  fi;
  return false;
end;;

# ================= JSON 出力ヘルパー(既存コピー群とバイト互換) =================
JStr := function(s) return Concatenation("\"", s, "\""); end;;
JB := function(b) if b then return "true"; else return "false"; fi; end;;

# 罠(2): JoinC を「逐次 Concatenation」で書くと O(合計長²) — n=13 の証明書
#   直列化単独で 437.5 秒を要した実測あり(LEDGER 2026-07-19)。以下は部品を
#   list に Add し最後に Concatenation を 1 回だけ呼ぶ線形時間版。出力は旧版と
#   区切り位置・内容とも同一(同 LEDGER でハッシュ一致 2/2 を実測)。
JoinC := function(strs, sep)
  local parts, i;
  if Length(strs) = 0 then return ""; fi;
  parts := [ strs[1] ];
  for i in [2..Length(strs)] do
    Add(parts, sep);
    Add(parts, strs[i]);
  od;
  return Concatenation(parts);
end;;

JArr := function(items) return Concatenation("[", JoinC(items, ","), "]"); end;;
JPair := function(a,b) return Concatenation("[", String(a), ",", String(b), "]"); end;;

# 罠(4): PrintTo は既定で長い行に整形改行を挿入する。証明書 JSON はバイト厳密
#   (ハッシュ台帳照合)なので SetPrintFormattingStatus(f, false) が必須。
WriteFile := function(path, content)
  local f;
  f := OutputTextFile(path, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, content);
  CloseStream(f);
end;;

#############################################################################
# ── 罠のコメント集(実測済み・出典は provenance/LEDGER.md)────────────────
# (1) Concatenation の単一引数呼びは「リストのリストの連結」— 文字列(=文字の
#     リスト)を 1 個だけ渡すとクラッシュする。複数引数なら文字列連結。
#     Concatenation("a","b") は "ab" / Concatenation(["a","b"]) も "ab" だが
#     Concatenation("ab") は誤り(LEDGER 2026-07-26・A5 dessin 証明書組立で実害)。
# (2) JoinC の逐次 Concatenation は O(n²) — 上記 JoinC の線形版を使う。
# (3) cap は壁時計 600 秒。超過見込みは対象集合の shard 分割(n=13 のような
#     単一対象が支配的な場合は直列化コスト側を疑う)。GAPLIB_CheckCap を
#     節目に挟み、超過時は「[CAP EXCEEDED]+残り UNKNOWN」で正直に止める。
# (4) PrintTo の整形改行 → WriteFile(上記)を使う。
# (5) GAP の `^` は右作用で自己完結(i^(g*h) = (i^g)^h・g^h = h^-1*g*h)。
#     標準数学の共役 v∘q∘v⁻¹(左作用の記法)を点作用で再現する GAP 式は
#     `q^v` であり、素朴な `q^(v^-1)` は誤り(LEDGER 2026-07-26・実測確認済み)。
# (6) 語規約の正本は prepend: 論文語 "AB" ↔ GAP 積 "B*A"(工房規約として恒久化
#     — LEDGER 2026-07-26 バッテリー完走)。評価器を書くとき必ず manifest の
#     規約欄と突き合わせる(1b で natural 12 vs prepend 24 の実測差あり)。
# (7) 実行は必ず `.\gap.ps1 <script>`(gap.bat は別窓で自動実行不可)。heap は
#     -o 2g 固定(8GB 機・gap.ps1 が付与)。大きな列挙の前に pkg/ の棚を確認
#     (twistedconjugacy・lins・repsn 等 約190 本 — 2026-07-26 Opus 棚卸し)。
#############################################################################
