# search/probe/wac_v1/ihnec_r4b_conventions_v5_20260805_gen.py
# 便102 F102-4.1 差戻し(sol/sol_reply_102_math29.md §4)の現物修理 — 指摘1。
#
# 指摘1(逐語): 「新 version の cert が実際に使う live ledger 版を宣言する。」
#   v4 は conventions_used.ledger_version = "conventions_ledger_v1_5" を宣言した
#   まま、納品束の申告は「台帳 v1.6」だった(宣言と申告の齟齬)。
#
# 本 v5 の措置:
#   (1) live 台帳 artifact = docs/notes/conventions_ledger_v1.md(H1 = 規約台帳 v1.6)
#       を実際に読み、その版名 "conventions_ledger_v1_6" を宣言する。
#   (2) ★ 宣言を散文にせず digest で束縛する: 新欄 ledger_artifact_pin
#       {path, sha256, declared_version} を top-level に置く。checker v3 の
#       (xi) がこの束縛を強制し、(x) が pin の bytes 一致を再計算検査する。
#       ⟹ 「台帳版を宣言したが実物と食い違う」型は、次からは機械が止める。
#   (3) 台帳 v1.7 は**草案・未発効**(docs/notes/conventions_ledger_v1_7_draft.md)
#       につき**宣言しない**。発効判定は司令塔 + Sol の専権であり、cert が
#       先走って未発効版を名乗ることはしない(fail-closed)。
#
# 凍結境界: v1/v2/v3/v4 の cert ファイルは byte 不変(編集しない)。MANIFEST は
# 追記のみのサージカル編集(既存 bytes を書き換えない)。checker v1/v2 も不改変。
#
# v4 は既に書き出し済みで bytes 確定済みなので、v5 の連鎖が v4 を指す箇所は
# **plain sha256** で書ける(sha256_ref indirection が要るのは v5 自身を指す
# 3 箇所 = erratum(v4->v5).superseded_by / role=current / effective_source のみ)。
import json, hashlib, os, sys, platform

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def relpath(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


OLD_V1_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_run_20260801.json")
OLD_V2_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v2_20260802.json")
OLD_V3_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v3_20260802.json")
OLD_V4_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v4_20260804.json")
V5_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v5_20260805.json")
MANIFEST_PATH = os.path.join(ROOT, "search", "certs", "MANIFEST_sol99_w99_2_1_20260802.json")
LEDGER_PATH = os.path.join(ROOT, "docs", "notes", "conventions_ledger_v1.md")

v1_sha = sha(OLD_V1_PATH)
v2_sha = sha(OLD_V2_PATH)
v3_sha = sha(OLD_V3_PATH)
v4_sha = sha(OLD_V4_PATH)
ledger_sha = sha(LEDGER_PATH)
v4 = json.load(open(OLD_V4_PATH, encoding="utf-8"))

# --- live 台帳版の機械読み取り(手写し禁止・machine-piped) ---
# H1 行から版番号を抽出し、"conventions_ledger_vX_Y" 形へ機械変換する。
ledger_head = open(LEDGER_PATH, encoding="utf-8").readline().strip()
import re
m = re.search(r"規約台帳\s*v(\d+)\.(\d+)", ledger_head)
if not m:
    raise SystemExit("live 台帳の H1 から版番号を読めない: %r" % ledger_head)
LIVE_LEDGER_VERSION = "conventions_ledger_v%s_%s" % (m.group(1), m.group(2))
print("live ledger H1     :", ledger_head)
print("live ledger version:", LIVE_LEDGER_VERSION)
if LIVE_LEDGER_VERSION == v4["conventions_used"]["ledger_version"]:
    raise SystemExit("v4 と同じ版を宣言することになる — F102-4.1 指摘1 の前提が崩れている")

# v4 の自己参照 digest(MANIFEST に記録済み)と、たった今再計算した v4_sha が
# 一致することを確認する(v4 は不改変のはず)。
manifest_now = json.load(open(MANIFEST_PATH, encoding="utf-8"))
recorded_v4_sha = manifest_now["self_reference_resolution"][relpath(OLD_V4_PATH)]["final_sha256"]
assert recorded_v4_sha == v4_sha, "v4 self-hash mismatch: MANIFEST says %s, recomputed %s" % (recorded_v4_sha, v4_sha)

V5_RELPATH = relpath(V5_PATH)
MANIFEST_RELPATH = relpath(MANIFEST_PATH)
# JSON Pointer (RFC 6901): '/' -> '~1', '~' -> '~0'.
V5_KEY_ESCAPED = V5_RELPATH.replace("~", "~0").replace("/", "~1")
JSON_POINTER = "/self_reference_resolution/%s/final_sha256" % V5_KEY_ESCAPED

SELF_REF_V5 = {
    "holder_path": MANIFEST_RELPATH,
    "json_pointer": JSON_POINTER,
    "resolution": "external-postwrite"
}

# conventions_used は v4 と同一内容を引き継ぐ(ledger_version と
# effective_source_chain / effective_source だけ差し替え)。
conventions_used_v5 = json.loads(json.dumps(v4["conventions_used"]))  # deep copy
conventions_used_v5["ledger_version"] = LIVE_LEDGER_VERSION

conventions_used_v5["effective_source_chain"] = [
    {
        "role": "original",
        "path": relpath(OLD_V1_PATH),
        "sha256": v1_sha
    },
    {
        "role": "erratum",
        "path": relpath(OLD_V1_PATH),
        "sha256": v1_sha,
        "scope": "conventions_used ブロックのMALFORMED 12箇所(comparison_targetのbare string・chi_P_criterion欠落・roundtrip_witness/separation/effective_source_chain/level等の欠落)を訂正。scan/anchors/p_ihn_*等の実測値(972/108/54を含む)は不変(旧certは無罪・遡及不要・CL-2)。",
        "superseded_by": {"path": relpath(OLD_V2_PATH), "sha256": v2_sha}
    },
    {
        "role": "erratum",
        "path": relpath(OLD_V2_PATH),
        "sha256": v2_sha,
        "scope": "W100-4.1(sol/sol_reply_100_math27.md §4): 自己参照2箇所に非64-hexのbare stringプレースホルダ SEE_MANIFEST(...) が入っておりMALFORMED。v3ではsha256_ref typed objectへ差し替えた。conventions_used の他の内容・数値は不変。v2ファイル自体は編集せず保存する。",
        "superseded_by": {"path": relpath(OLD_V3_PATH), "sha256": v3_sha}
    },
    {
        "role": "erratum",
        "path": relpath(OLD_V3_PATH),
        "sha256": v3_sha,
        "scope": "W101-3.1(sol_reply_101_math28.md §3・裁定428): v3のledger_versionが\"conventions_ledger_v1_4\"のまま v1.5新設のsha256_ref typed objectを使っていた(ledger_version drift)。v4がこれを訂正。v3ファイル自体は編集せず保存する。",
        "superseded_by": {"path": relpath(OLD_V4_PATH), "sha256": v4_sha}
    },
    {
        "role": "erratum",
        "path": relpath(OLD_V4_PATH),
        "sha256": v4_sha,
        "scope": "F102-4.1(sol/sol_reply_102_math29.md §4・便102)の指摘1: v4のconventions_used.ledger_versionは\"conventions_ledger_v1_5\"を宣言しているのに、納品束の申告は台帳v1.6だった(宣言と申告の齟齬)。加えて当時のchecker v2のEXPECTED_LEDGER_VERSIONもv1_5であり、束全体が一貫して古い版を見ていた。v5では live台帳artifact(docs/notes/conventions_ledger_v1.md・H1=規約台帳v1.6)を機械読み取りして宣言し、その bytes を ledger_artifact_pin で束縛する。v4のconventions_used内容・実測値は不変。v4ファイル自体は編集せず保存する。",
        "superseded_by": {"path": V5_RELPATH, "sha256_ref": SELF_REF_V5}
    },
    {
        "role": "current",
        "path": V5_RELPATH,
        "sha256_ref": SELF_REF_V5
    }
]
conventions_used_v5["effective_source"] = {"path": V5_RELPATH, "sha256_ref": SELF_REF_V5}

CHECKER_V3_RELPATH = "search/probe/wac_v1/ihnec_r4b_selfhash_checker_v3.py"

supplement = {
    "schema": "ihnec-r4b-conventions-supplement/v5",
    "generated_by": {
        "tool": "python (schema-conformance supplement generator; does not re-run GAP, does not alter measured values)",
        "script": relpath(os.path.abspath(__file__)),
        "date": "2026-08-05"
    },
    "task_ref": "便102 F102-4.1差戻し(sol/sol_reply_102_math29.md §4)の現物修理・指摘1。ledger_version宣言を live台帳artifact(v1.6)へ同期し、宣言をdigestで束縛する。",
    "supersedes": {
        "path": relpath(OLD_V4_PATH),
        "sha256": v4_sha,
        "reason": "v4はconventions_used.ledger_version=\"conventions_ledger_v1_5\"を宣言したまま、納品束では台帳v1.6準拠と申告していた(F102-4.1 指摘1・宣言と申告の齟齬)。v4はbyte不変のまま保存(編集禁止)。v5はledger_version宣言を live台帳(v1.6)へ同期し、ledger_artifact_pinでdigest束縛する。他のconventions_used内容・実測値はv4から不変。"
    },
    "supplements_cert": {"path": relpath(OLD_V1_PATH), "sha256": v1_sha},
    "ledger_artifact_pin": {
        "path": relpath(LEDGER_PATH),
        "sha256": ledger_sha,
        "declared_version": LIVE_LEDGER_VERSION,
        "h1_verbatim": ledger_head,
        "note": "★ v5新設欄(便102 F102-4.1 指摘1の構造的修理)。conventions_used.ledger_version は『どの台帳版に準拠して書かれた cert か』の宣言だが、v4までは散文の宣言でしかなく、実物の台帳artifactと突合できなかった。本欄は宣言をlive artifactのbytesへ束縛する。checker v3 の (xi) が declared_version == conventions_used.ledger_version を強制し、(x) が本欄の sha256 を実bytesと再計算突合する。⟹ 台帳が改版されれば本certは自動的にINTEGRITY_STOPし、cert側の再版を強制する(これは意図した fail-closed 挙動である)。なお台帳v1.7はdocs/notes/conventions_ledger_v1_7_draft.mdに草案として存在するが未発効につき宣言しない(発効判定は司令塔+Solの専権)。"
    },
    "note": "本certはv4のconventions_usedブロックのうちledger_versionと、v5自身を指すよう更新したeffective_source_chain/effective_sourceの自己参照のみを差し替え、top-levelにledger_artifact_pinを新設する。scan/anchors/p_ihn_*/shadows_sample等の実測値・その他conventions_used欄はv4から不変(値はすべて旧certからの参照のみ)。v1/v2/v3/v4ファイル自体はbyte不変のまま残る。",
    "self_hash_mechanism": {
        "design": "P100-4.1(sol_reply_100_math27.md §4)準拠。sha256をunion型の自由文字列にしない。通常entryはpathと64 lowercase hexのsha256を持つ。自己参照時(=v5自身を指す箇所)だけ、sha256の代わりにsha256_ref={holder_path,json_pointer,resolution:'external-postwrite'}を持つ。v1〜v4を指す箇所は、それらのbytesが既に確定しているため plain sha256 で書く(fixed-point問題が生じるのはv5自身を指す3箇所: erratum(v4->v5).superseded_by / role=current entry / effective_source のみ)。",
        "why_no_fixed_point_problem": "v5は自分自身のsha256をv5の内容に一切含まない(pointerが指す先は外部artifact=MANIFESTの追記entryであり、v5自身のbytesではない)。したがってv5を確定・書き出した後にそのsha256を計算しMANIFESTへ追記する片方向の手順で完結し、自己言及の循環は生じない。",
        "self_ref_object": SELF_REF_V5,
        "self_ref_occurrence_count": 3,
        "checker": CHECKER_V3_RELPATH + "(便102 F102-4.1準拠。走査を『既にdigestを持つdictの発見』から『schema上digest必須の位置の構造的列挙』へ反転し、各必須位置で sha256 XOR sha256_ref を検査する — 両方ある側に加え、★どちらも無い側(missing-both)を検出する。加えて(x)plain sha256のbytes再計算・(xi)ledger_artifact_pinの束縛を新設。checker v1(ihnec_r4b_v3_selfhash_checker.py)およびv2(ihnec_r4b_selfhash_checker_v2.py)は不改変で保存)",
        "checker_history": [
            {"version": "v1", "path": "search/probe/wac_v1/ihnec_r4b_v3_selfhash_checker.py", "status": "frozen_record"},
            {"version": "v2", "path": "search/probe/wac_v1/ihnec_r4b_selfhash_checker_v2.py", "status": "frozen_record",
             "known_hole": "便102 F102-4.1: 走査が『既にsha256/sha256_refを持つdictの列挙』だったため、digest必須entryから双方を消すとentry自体が走査から消えた(Solの実証: v4のeffective_source_chain[0]からsha256を除去 -> PASS, scanned 8)。台帳規範11のXORのうちmissing-both側が未実装。"},
            {"version": "v3", "path": CHECKER_V3_RELPATH, "status": "current"}
        ]
    },
    "referenced_old_values": v4["referenced_old_values"],
    "malformed_findings_fixed": v4["malformed_findings_fixed"] + [
        {
            "id": "MF-F102-4.1-a",
            "rule": "台帳v1.6 §0/§1.7(ledger_versionは実際に使用しているlive台帳版と一致させる)",
            "field": "conventions_used.ledger_version (v4)",
            "observed_old_value": "conventions_ledger_v1_5",
            "issue": "v4は台帳v1.5を宣言したまま、納品束では台帳v1.6準拠と申告していた(F102-4.1 指摘1)。v5ではlive台帳artifactを機械読み取りして conventions_ledger_v1_6 を宣言し、ledger_artifact_pin でそのbytesへ束縛する。"
        },
        {
            "id": "MF-F102-4.1-b",
            "rule": "台帳v1.6 §2 規範11(digest必須欄は sha256 と sha256_ref のちょうど一方を持つ)+ §1.7.3′ (viii)",
            "field": "checker v2 の走査方式(cert欄そのものではなく検査器の欠陥)",
            "observed_old_value": "walk_sha_containers(): 既にsha256/sha256_refを持つdictのみを列挙",
            "issue": "digest必須entryから双方を消すとentryが走査対象から消え、missing-bothが検出されなかった(Solの変異注入で実証: PASS, scanned 8)。checker v3 で走査を構造的必須位置列挙へ反転し、missing-both fixtureをmutant matrixへ追加した。cert側の欄は無罪(v4のdigest欄自体は正しい)。"
        }
    ],
    "conventions_used": conventions_used_v5,
    "cross_checked_status": v4["cross_checked_status"],
    "provenance": {
        "python_version": sys.version,
        "platform": platform.platform(),
        "v1_cert_sha256_reconfirmed": v1_sha,
        "v2_cert_sha256_reconfirmed": v2_sha,
        "v3_cert_sha256_reconfirmed": v3_sha,
        "v4_cert_sha256_reconfirmed": v4_sha,
        "ledger_artifact_sha256_reconfirmed": ledger_sha,
        "note": "v5自身はself-hashを内容に含まない(sha256_refで外部manifestを指すのみ)。書き出し後、本スクリプトの後半でv5のsha256を計算しMANIFESTへ追記する(MANIFESTの過去entryは不改変・追記のみ・サージカル編集)。v1〜v4を指す箇所はそれらのbytesが既に確定しているためplain sha256で書いている。"
    }
}

with open(V5_PATH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(supplement, f, ensure_ascii=False, indent=2)
    f.write("\n")

v5_sha = sha(V5_PATH)
print("Wrote", V5_RELPATH)
print("v1_sha256:", v1_sha)
print("v2_sha256:", v2_sha)
print("v3_sha256:", v3_sha)
print("v4_sha256:", v4_sha)
print("ledger_sha256:", ledger_sha)
print("v5_sha256:", v5_sha)

# --- MANIFESTへの追記(サージカル編集: 既存bytesは一切書き換えず、新規テキストのみ挿入) ---
raw = open(MANIFEST_PATH, "rb").read().decode("utf-8")
assert V5_RELPATH not in raw, "already present -- would need edit, not append; refusing"

v4_entry_close = (
    '      "final_sha256": "%s"\n'
    '    }\n'
    '  },\n'
) % v4_sha
if raw.count(v4_entry_close) != 1:
    raise SystemExit("anchor A not found exactly once -- refusing surgical edit (found %d)" % raw.count(v4_entry_close))

NOTE_V5 = (
    "便102 F102-4.1(sol/sol_reply_102_math29.md §4)指摘1のledger_version齟齬修理。"
    "v4はconventions_used.ledger_version=\\\"conventions_ledger_v1_5\\\"を宣言したまま"
    "納品束では台帳v1.6準拠と申告していた。v5はlive台帳artifactを機械読み取りして"
    "conventions_ledger_v1_6を宣言し、ledger_artifact_pinでそのbytesへ束縛する。"
    "v4ファイル自体は不改変。"
)

new_self_ref_entry = (
    '      "final_sha256": "%s"\n'
    '    },\n'
    '    "%s": {\n'
    '      "path": "%s",\n'
    '      "note": "%s",\n'
    '      "final_sha256": "%s"\n'
    '    }\n'
    '  },\n'
) % (v4_sha, V5_RELPATH, V5_RELPATH, NOTE_V5, v5_sha)

raw2 = raw.replace(v4_entry_close, new_self_ref_entry, 1)

# Anchor B: append one new top-level key after the w101_3_4_addendum block.
old_tail = (
    '  }\n'
    '}\n'
)
if not raw2.endswith(old_tail):
    raise SystemExit("anchor B: unexpected manifest tail -- refusing surgical edit")

F1024_NOTE = (
    "便102 F102-4.1(sol/sol_reply_102_math29.md §4)差戻しの現物修理。"
    "(1) cert: v5がlive台帳版conventions_ledger_v1_6を宣言しledger_artifact_pinでbytes束縛。"
    "(2) checker v3: 走査を『digestを既に持つdictの発見』から『schema上digest必須位置の構造的列挙』へ反転し、"
    "sha256 XOR sha256_ref のmissing-both側を新規に検出する(Solが変異注入で実証した穴)。"
    "(3) missing-both fixtureをmutant matrixへ追加(既存selftestは全維持)。"
    "(4) CL-12の『閉』の訂正とCL-13条文案は次版台帳v1.7の草案 docs/notes/conventions_ledger_v1_7_draft.md へ。"
    "過去cert(v1-v4)・過去checker(v1/v2)・本manifestの既存entryはいずれも不改変(追記のみ)。"
)

new_top_key = (
    '  },\n'
    '  "f102_4_1_addendum": {\n'
    '    "task_ref": "便102 F102-4.1差戻しの現物修理",\n'
    '    "note": "%s",\n'
    '    "v5_path": "%s",\n'
    '    "v5_sha256": "%s",\n'
    '    "checker_v3_path": "%s",\n'
    '    "ledger_artifact_path": "%s",\n'
    '    "ledger_artifact_sha256": "%s",\n'
    '    "ledger_v1_7_draft_path": "docs/notes/conventions_ledger_v1_7_draft.md",\n'
    '    "ratification_status": "UNRATIFIED -- 発効判定は司令塔 + Sol(便103)。本addendumは納品記録であって発効記録ではない"\n'
    '  }\n'
    '}\n'
) % (F1024_NOTE, V5_RELPATH, v5_sha, CHECKER_V3_RELPATH, relpath(LEDGER_PATH), ledger_sha)

raw3 = raw2[: -len(old_tail)] + new_top_key

with open(MANIFEST_PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write(raw3)

print("Patched (surgical append-only)", relpath(MANIFEST_PATH))
print("checker_v3_sha256:", sha(os.path.join(ROOT, CHECKER_V3_RELPATH.replace("/", os.sep))))
