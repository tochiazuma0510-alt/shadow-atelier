# search/probe/wac_v1/ihnec_r4b_conventions_v3_20260802_gen.py
# 便100 検収(裁定422) — W100-4.1差戻しの現物修理(P100-4.1)。
#
# 経緯: v2 (search/certs/ihnec_r4b_conventions_v2_20260802.json) は
# effective_source_chain[1].superseded_by.sha256 と effective_source.sha256 に
# "SEE_MANIFEST(...)" という非64-hexのbare stringプレースホルダを入れており、
# 台帳v1.3/v1.4のCV-10 sha256欄の型(64-hex文字列)に適合しない(W100-4.1・MALFORMED)。
# さらにplaceholderの参照先注記が実在しない .sha256 拡張子のファイルを指していた
# (実在する外部holderは .json)。
#
# 本スクリプトはv2の数値・conventions_used内容を一切変更せず、自己参照2箇所
# (effective_source_chain の current entry / effective_source)だけを
# P100-4.1指定のtyped object (sha256_ref: {holder_path, json_pointer, resolution})
# に差し替えたv3 supplementを新設する。v2ファイル自体はbyte不変のまま残す
# (「逸脱を正直に申告した record」として保存・編集禁止)。
#
# 自己言及不能性の解消: v3は自分自身のsha256を内容に含まない(pointerで外部
# manifestを指すだけ)。したがってv3の書き出しに二段階のchicken-egg問題は
# 生じない — v3を確定して書き出した後、そのbytesのsha256を計算し、
# MANIFESTへ追記するだけでよい。
#
# MANIFESTへの追記は json.dump によるファイル全体の再整形ではなく、
# 既存bytesへの最小限のテキスト挿入(サージカル編集)で行う
# (指示: 過去entryは不改変・追記のみ -- json.dump による再インデントは
# 意味的に無害でも byte-level には「全行書き換え」に見えるため避ける)。
import json, hashlib, os, sys, platform

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

def relpath(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

OLD_V1_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_run_20260801.json")
OLD_V2_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v2_20260802.json")
V3_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v3_20260802.json")
MANIFEST_PATH = os.path.join(ROOT, "search", "certs", "MANIFEST_sol99_w99_2_1_20260802.json")

v1_sha = sha(OLD_V1_PATH)
v2_sha = sha(OLD_V2_PATH)
v1 = json.load(open(OLD_V1_PATH, encoding="utf-8"))
v2 = json.load(open(OLD_V2_PATH, encoding="utf-8"))

V3_RELPATH = relpath(V3_PATH)
MANIFEST_RELPATH = relpath(MANIFEST_PATH)
# JSON Pointer (RFC 6901): '/' in a path component must be escaped as '~1',
# '~' as '~0'. V3_RELPATH has no '~', only '/'.
V3_KEY_ESCAPED = V3_RELPATH.replace("~", "~0").replace("/", "~1")
JSON_POINTER = "/self_reference_resolution/%s/final_sha256" % V3_KEY_ESCAPED

SELF_REF = {
    "holder_path": MANIFEST_RELPATH,
    "json_pointer": JSON_POINTER,
    "resolution": "external-postwrite"
}

# conventions_used は v2 と同一内容を引き継ぐ(自己参照2箇所のみ差し替え)。
conventions_used_v3 = json.loads(json.dumps(v2["conventions_used"]))  # deep copy

conventions_used_v3["effective_source_chain"] = [
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
        "superseded_by": {
            "path": relpath(OLD_V2_PATH),
            "sha256": v2_sha
        }
    },
    {
        "role": "erratum",
        "path": relpath(OLD_V2_PATH),
        "sha256": v2_sha,
        "scope": "W100-4.1(sol/sol_reply_100_math27.md §4): 自己参照2箇所(effective_source_chain[1].superseded_by.sha256 / effective_source.sha256)に非64-hexのbare stringプレースホルダ SEE_MANIFEST(...) が入っており台帳CV-10 sha256欄の型に不適合(MALFORMED)。加えてplaceholder注記の参照先拡張子が実在しない .sha256 だった(実在holderは .json)。conventions_used の他の内容・数値は不変。v2ファイル自体は編集せず保存する。",
        "superseded_by": {
            "path": V3_RELPATH,
            "sha256_ref": SELF_REF
        }
    },
    {
        "role": "current",
        "path": V3_RELPATH,
        "sha256_ref": SELF_REF
    }
]
conventions_used_v3["effective_source"] = {
    "path": V3_RELPATH,
    "sha256_ref": SELF_REF
}
conventions_used_v3["ledger_version"] = "conventions_ledger_v1_4"

supplement = {
    "schema": "ihnec-r4b-conventions-supplement/v3",
    "generated_by": {
        "tool": "python (schema-conformance supplement generator; does not re-run GAP, does not alter measured values)",
        "script": relpath(os.path.abspath(__file__)),
        "date": "2026-08-02"
    },
    "task_ref": "便100 検収(裁定422) W100-4.1差戻し(sol/sol_reply_100_math27.md §4・P100-4.1)の現物修理。",
    "supersedes": {
        "path": relpath(OLD_V2_PATH),
        "sha256": v2_sha,
        "reason": "v2のself-hash placeholder(SEE_MANIFEST(...)・非64-hex・参照先拡張子誤り)をP100-4.1指定のtyped sha256_refへ差し替える。v2はbyte不変のまま『逸脱を正直に申告した record』として保存(編集禁止)。"
    },
    "supplements_cert": {"path": relpath(OLD_V1_PATH), "sha256": v1_sha},
    "note": "本certはv2のconventions_usedブロックのうちeffective_source_chain/effective_sourceの自己参照2箇所のみをtyped sha256_ref (P100-4.1) に差し替える。scan/anchors/p_ihn_*/shadows_sample等の実測値・その他conventions_used欄はv2から不変(値はすべて旧certからの参照のみ)。v1/v2ファイル自体はbyte不変のまま残る。",
    "self_hash_mechanism": {
        "design": "P100-4.1(sol_reply_100_math27.md §4)準拠。sha256をunion型の自由文字列にしない。通常entryはpathと64 lowercase hexのsha256を持つ。自己参照時だけ、sha256の代わりにsha256_ref={holder_path,json_pointer,resolution:'external-postwrite'}を持つ。",
        "why_no_fixed_point_problem": "v3は自分自身のsha256をv3の内容に一切含まない(pointerが指す先は外部artifact=MANIFESTの追記entryであり、v3自身のbytesではない)。したがってv3を確定・書き出した後にそのsha256を計算しMANIFESTへ追記する片方向の手順で完結し、自己言及の循環は生じない。",
        "self_ref_object": SELF_REF,
        "checker": "search/probe/wac_v1/ihnec_r4b_v3_selfhash_checker.py(P100-4.1の5検査を実装・実走してPASS/負例STOPを確認)"
    },
    "referenced_old_values": v2["referenced_old_values"],
    "malformed_findings_fixed": v2["malformed_findings_fixed"] + [
        {
            "id": "MF-W100-4.1-a",
            "rule": "台帳v1.3 CV-10四原則②(ハッシュキー名はsha256)+ P100-4.1(sha256はunion型自由文字列にしない)",
            "field": "conventions_used.effective_source_chain[1].superseded_by.sha256 (v2)",
            "observed_old_value": "SEE_MANIFEST(自己参照digestは書き出し後にsearch/certs/MANIFEST_sol99_w99_2_1_20260802.sha256へ記録・W99-2.1納品報告で申告)",
            "issue": "sha256欄に64-hexでないbare stringプレースホルダが入っておりMALFORMED。加えて参照注記の拡張子が実在しない .sha256(実在holderは .json)。v3ではsha256_ref typed objectへ差し替え。"
        },
        {
            "id": "MF-W100-4.1-b",
            "rule": "同上",
            "field": "conventions_used.effective_source.sha256 (v2)",
            "observed_old_value": "SEE_MANIFEST(同上)",
            "issue": "同上。v3ではsha256_ref typed objectへ差し替え。"
        }
    ],
    "conventions_used": conventions_used_v3,
    "cross_checked_status": v2["cross_checked_status"],
    "provenance": {
        "python_version": sys.version,
        "platform": platform.platform(),
        "v1_cert_sha256_reconfirmed": v1_sha,
        "v2_cert_sha256_reconfirmed": v2_sha,
        "note": "v3自身はself-hashを内容に含まない(sha256_refで外部manifestを指すのみ)。書き出し後、本スクリプトの後半でv3のsha256を計算しMANIFESTへ追記する(MANIFESTの過去entryは不改変・追記のみ・サージカル編集)。"
    }
}

with open(V3_PATH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(supplement, f, ensure_ascii=False, indent=2)
    f.write("\n")

v3_sha = sha(V3_PATH)
print("Wrote", V3_RELPATH)
print("v1_sha256:", v1_sha)
print("v2_sha256:", v2_sha)
print("v3_sha256:", v3_sha)

# --- MANIFESTへの追記(サージカル編集: 既存bytesは一切書き換えず、
#     2箇所にのみ新規テキストを挿入する。json.dumpによる全体再整形はしない) ---
raw = open(MANIFEST_PATH, "rb").read().decode("utf-8")
assert V3_RELPATH not in raw, "already present -- would need edit, not append; refusing"

anchor_a = '"final_sha256": "%s"\n    }\n  },\n' % v2["provenance"]["python_version"] if False else None
# Anchor A: insert a new self_reference_resolution entry right after the v2
# entry's closing "}" (before the "}," that closes self_reference_resolution).
v2_entry_close = (
    '      "final_sha256": "%s"\n'
    '    }\n'
    '  },\n'
) % v2_sha
if raw.count(v2_entry_close) != 1:
    raise SystemExit("anchor A not found exactly once -- refusing surgical edit (found %d)" % raw.count(v2_entry_close))

new_self_ref_entry = (
    '      "final_sha256": "%s"\n'
    '    },\n'
    '    "%s": {\n'
    '      "path": "%s",\n'
    '      "note": "P100-4.1(sol_reply_100_math27.md §4)のtyped sha256_ref正形。v2のSEE_MANIFEST(...) placeholder（非64-hex・MALFORMED・参照先拡張子誤り）を差し替えるv3 supplementの自己参照digestをここに確定する（裁定422）。",\n'
    '      "final_sha256": "%s"\n'
    '    }\n'
    '  },\n'
) % (v2_sha, V3_RELPATH, V3_RELPATH, v3_sha)

raw2 = raw.replace(v2_entry_close, new_self_ref_entry, 1)

# Anchor B: insert a new top-level key right before the final closing "}".
tail_anchor = raw2.rstrip("\n")
if not tail_anchor.endswith("}"):
    raise SystemExit("anchor B: file does not end with '}' -- refusing surgical edit")
# locate the known_deviation_disclosed value's closing quote+newline+"}" at EOF
known_dev_key = '"known_deviation_disclosed": "'
idx = raw2.index(known_dev_key)
# find end of that string value: the JSON string ends at the last '"' before
# the trailing '\n}\n' (there is no escaped trailing quote in that value).
close_brace_pos = raw2.rfind("}")
segment = raw2[idx:close_brace_pos]
# segment looks like: '"known_deviation_disclosed": "....."\n'
if not segment.rstrip().endswith('"'):
    raise SystemExit("anchor B: unexpected tail shape -- refusing surgical edit")
new_val_str = segment.rstrip()[:-1] + '",\n'  # drop trailing quote, reopen with comma
new_top_key = (
    '  "w100_4_1_addendum": {\n'
    '    "task_ref": "便100 検収（裁定422）W100-4.1差戻しの現物修理",\n'
    '    "note": "search/certs/ihnec_r4b_conventions_v2_20260802.json は self-hash placeholderの型不備（MALFORMED）により search/certs/ihnec_r4b_conventions_v3_20260802.json が supersede した。v2ファイル自体・本 manifest の既存 entry は不改変（追記のみ）。",\n'
    '    "v3_path": "%s",\n'
    '    "v3_sha256": "%s"\n'
    '  }\n'
) % (V3_RELPATH, v3_sha)

raw3 = raw2[:idx] + new_val_str + new_top_key + raw2[close_brace_pos:]

with open(MANIFEST_PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write(raw3)

print("Patched (surgical append-only)", relpath(MANIFEST_PATH))
