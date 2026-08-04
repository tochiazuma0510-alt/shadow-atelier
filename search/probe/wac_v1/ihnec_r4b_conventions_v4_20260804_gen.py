# search/probe/wac_v1/ihnec_r4b_conventions_v4_20260804_gen.py
# 便101 検収(裁定428) -- P101-3.1(sol_reply_101_math28.md W101-3.1)の現物修理。
#
# 経緯: v3 (search/certs/ihnec_r4b_conventions_v3_20260802.json) は
# conventions_used.ledger_version に "conventions_ledger_v1_4" を宣言したまま、
# v1.5 で新設された sha256_ref typed object を使っている(schema versionの型不一致
# -- W101-3.1)。本スクリプトはv3の数値・conventions_used内容を一切変更せず、
# v3ファイル自体もbyte不変のまま残す。新設するv4 supplementだけが
# ledger_version = "conventions_ledger_v1_5" を正しく宣言する。
#
# 自己言及不能性の設計(v3から一歩進める): v3は既に書き出し済みでbytesが確定して
# いるので、v3自身のsha256は「今」計算できる(chicken-eggではない)。したがって
# v4のeffective_source_chain中でv3を指す箇所(旧supersededされたerratum entry
# および過去のv2->v3遷移を記録するsuperseded_by)は、v3の実digestを **plain
# sha256** として書いてよい -- typed sha256_ref に頼る必要があるのはv4自身を
# 指す3箇所(erratum(v3->v4).superseded_by / role=current entry / effective_source)
# だけである(いずれもv4自身の内容にv4自身のdigestを含められないという真の
# fixed-point問題を抱える)。
#
# MANIFESTへの追記は json.dump によるファイル全体の再整形ではなく、
# 既存bytesへの最小限のテキスト挿入(サージカル編集)で行う(過去entry不改変)。
import json, hashlib, os, sys, platform

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def relpath(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


OLD_V1_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_run_20260801.json")
OLD_V2_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v2_20260802.json")
OLD_V3_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v3_20260802.json")
V4_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v4_20260804.json")
MANIFEST_PATH = os.path.join(ROOT, "search", "certs", "MANIFEST_sol99_w99_2_1_20260802.json")

v1_sha = sha(OLD_V1_PATH)
v2_sha = sha(OLD_V2_PATH)
v3_sha = sha(OLD_V3_PATH)
v1 = json.load(open(OLD_V1_PATH, encoding="utf-8"))
v2 = json.load(open(OLD_V2_PATH, encoding="utf-8"))
v3 = json.load(open(OLD_V3_PATH, encoding="utf-8"))

# v3の自己参照digest(MANIFESTに既に記録済み)と、たった今再計算したv3_shaが
# 一致することを確認する(v3は不改変のはずなので、ここが食い違えば設計の前提が壊れている)。
manifest_now = json.load(open(MANIFEST_PATH, encoding="utf-8"))
recorded_v3_sha = manifest_now["self_reference_resolution"][relpath(OLD_V3_PATH)]["final_sha256"]
assert recorded_v3_sha == v3_sha, "v3 self-hash mismatch: MANIFEST says %s, recomputed %s" % (recorded_v3_sha, v3_sha)

V4_RELPATH = relpath(V4_PATH)
MANIFEST_RELPATH = relpath(MANIFEST_PATH)
# JSON Pointer (RFC 6901): '/' -> '~1', '~' -> '~0'.
V4_KEY_ESCAPED = V4_RELPATH.replace("~", "~0").replace("/", "~1")
JSON_POINTER = "/self_reference_resolution/%s/final_sha256" % V4_KEY_ESCAPED

SELF_REF_V4 = {
    "holder_path": MANIFEST_RELPATH,
    "json_pointer": JSON_POINTER,
    "resolution": "external-postwrite"
}

# conventions_used は v3 と同一内容を引き継ぐ(ledger_versionとeffective_source_chain/
# effective_sourceだけ差し替え)。
conventions_used_v4 = json.loads(json.dumps(v3["conventions_used"]))  # deep copy

conventions_used_v4["ledger_version"] = "conventions_ledger_v1_5"

conventions_used_v4["effective_source_chain"] = [
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
        "scope": "W100-4.1(sol/sol_reply_100_math27.md §4): 自己参照2箇所に非64-hexのbare stringプレースホルダ SEE_MANIFEST(...) が入っておりMALFORMED。v3ではsha256_ref typed objectへ差し替えた。conventions_used の他の内容・数値は不変。v2ファイル自体は編集せず保存する。",
        "superseded_by": {
            # v3は既に書き出し済み・bytes確定済みなので、ここは plain sha256 でよい
            # (v3自身のsha256_ref indirectionは v3自身の書き出し時にのみ必要だった)。
            "path": relpath(OLD_V3_PATH),
            "sha256": v3_sha
        }
    },
    {
        "role": "erratum",
        "path": relpath(OLD_V3_PATH),
        "sha256": v3_sha,
        "scope": "W101-3.1(sol_reply_101_math28.md §3・裁定428): v3のconventions_used.ledger_versionが\"conventions_ledger_v1_4\"を宣言したまま、v1.5で新設されたsha256_ref typed objectを使っており、schema versionの型が実際の内容と食い違う(ledger_version drift)。v3のconventions_used内容・実測値は不変。v3ファイル自体は編集せず保存する。v4ではledger_versionを\"conventions_ledger_v1_5\"へ正しく宣言する。",
        "superseded_by": {
            "path": V4_RELPATH,
            "sha256_ref": SELF_REF_V4
        }
    },
    {
        "role": "current",
        "path": V4_RELPATH,
        "sha256_ref": SELF_REF_V4
    }
]
conventions_used_v4["effective_source"] = {
    "path": V4_RELPATH,
    "sha256_ref": SELF_REF_V4
}

supplement = {
    "schema": "ihnec-r4b-conventions-supplement/v4",
    "generated_by": {
        "tool": "python (schema-conformance supplement generator; does not re-run GAP, does not alter measured values)",
        "script": relpath(os.path.abspath(__file__)),
        "date": "2026-08-04"
    },
    "task_ref": "便101 検収(裁定428) W101-3.1差戻し(sol_reply_101_math28.md §3・P101-3.1)の現物修理。ledger_version宣言のみをv1.5へ同期する。",
    "supersedes": {
        "path": relpath(OLD_V3_PATH),
        "sha256": v3_sha,
        "reason": "v3のconventions_used.ledger_versionが\"conventions_ledger_v1_4\"のまま、v1.5新設のsha256_ref typed objectを使っていた(W101-3.1・schema version drift)。v3はbyte不変のまま『逸脱を正直に申告した record』として保存(編集禁止)。v4はledger_version宣言のみを訂正し、他のconventions_used内容・実測値はv3から不変。"
    },
    "supplements_cert": {"path": relpath(OLD_V1_PATH), "sha256": v1_sha},
    "note": "本certはv3のconventions_usedブロックのうちledger_versionと、v4自身を指すよう更新したeffective_source_chain/effective_sourceの自己参照のみを差し替える。scan/anchors/p_ihn_*/shadows_sample等の実測値・その他conventions_used欄はv3から不変(値はすべて旧certからの参照のみ)。v1/v2/v3ファイル自体はbyte不変のまま残る。",
    "self_hash_mechanism": {
        "design": "P100-4.1(sol_reply_100_math27.md §4)準拠。sha256をunion型の自由文字列にしない。通常entryはpathと64 lowercase hexのsha256を持つ。自己参照時(=v4自身を指す箇所)だけ、sha256の代わりにsha256_ref={holder_path,json_pointer,resolution:'external-postwrite'}を持つ。v1/v2/v3を指す箇所は、それらのbytesが既に確定しているため plain sha256 で書く(fixed-point問題が生じるのはv4自身を指す3箇所: erratum(v3->v4).superseded_by / role=current entry / effective_source のみ)。",
        "why_no_fixed_point_problem": "v4は自分自身のsha256をv4の内容に一切含まない(pointerが指す先は外部artifact=MANIFESTの追記entryであり、v4自身のbytesではない)。したがってv4を確定・書き出した後にそのsha256を計算しMANIFESTへ追記する片方向の手順で完結し、自己言及の循環は生じない。",
        "self_ref_object": SELF_REF_V4,
        "self_ref_occurrence_count": 3,
        "checker": "search/probe/wac_v1/ihnec_r4b_selfhash_checker_v2.py(便101 P101-3.2〜3.4準拠。cert内の全sha256_ref(nested superseded_by含む)を列挙して(i)-(iv)を適用し、current.path=effective_source.path=実入力cert pathの三者一致とsha256/sha256_refのXOR排他を強制する。v1の検収済みihnec_r4b_v3_selfhash_checker.pyは不改変で別名v2として新設)"
    },
    "referenced_old_values": v3["referenced_old_values"],
    "malformed_findings_fixed": v3["malformed_findings_fixed"] + [
        {
            "id": "MF-W101-3.1",
            "rule": "台帳v1.5 §0/§1.7(ledger_versionは実際に使用しているschema版と一致させる)",
            "field": "conventions_used.ledger_version (v3)",
            "observed_old_value": "conventions_ledger_v1_4",
            "issue": "v3のconventions_usedはv1.5で新設されたsha256_ref typed objectを使っているにもかかわらず、ledger_versionはv1.4を宣言していた(schema version drift・W101-3.1)。v4ではconventions_ledger_v1_5へ訂正する。"
        }
    ],
    "conventions_used": conventions_used_v4,
    "cross_checked_status": v3["cross_checked_status"],
    "provenance": {
        "python_version": sys.version,
        "platform": platform.platform(),
        "v1_cert_sha256_reconfirmed": v1_sha,
        "v2_cert_sha256_reconfirmed": v2_sha,
        "v3_cert_sha256_reconfirmed": v3_sha,
        "note": "v4自身はself-hashを内容に含まない(sha256_refで外部manifestを指すのみ)。書き出し後、本スクリプトの後半でv4のsha256を計算しMANIFESTへ追記する(MANIFESTの過去entryは不改変・追記のみ・サージカル編集)。v1/v2/v3を指す箇所はそれらのbytesが既に確定しているためplain sha256で書いている(この点はv3からの変更点)。"
    }
}

with open(V4_PATH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(supplement, f, ensure_ascii=False, indent=2)
    f.write("\n")

v4_sha = sha(V4_PATH)
print("Wrote", V4_RELPATH)
print("v1_sha256:", v1_sha)
print("v2_sha256:", v2_sha)
print("v3_sha256:", v3_sha)
print("v4_sha256:", v4_sha)

# --- MANIFESTへの追記(サージカル編集: 既存bytesは一切書き換えず、新規テキストのみ挿入) ---
raw = open(MANIFEST_PATH, "rb").read().decode("utf-8")
assert V4_RELPATH not in raw, "already present -- would need edit, not append; refusing"

# Anchor A: insert a new self_reference_resolution entry right after the v3
# entry's closing "}" (before the "}," that closes self_reference_resolution).
v3_entry_close = (
    '      "final_sha256": "%s"\n'
    '    }\n'
    '  },\n'
) % v3_sha
if raw.count(v3_entry_close) != 1:
    raise SystemExit("anchor A not found exactly once -- refusing surgical edit (found %d)" % raw.count(v3_entry_close))

new_self_ref_entry = (
    '      "final_sha256": "%s"\n'
    '    },\n'
    '    "%s": {\n'
    '      "path": "%s",\n'
    '      "note": "便101 P101-3.1(sol_reply_101_math28.md §3・W101-3.1・裁定428)のledger_version drift修理。v3のconventions_used.ledger_versionが\\"conventions_ledger_v1_4\\"のまま新型sha256_refを使っていた食い違いを、v4がconventions_ledger_v1_5を正しく宣言することで閉じる。v3ファイル自体は不改変。",\n'
    '      "final_sha256": "%s"\n'
    '    }\n'
    '  },\n'
) % (v3_sha, V4_RELPATH, V4_RELPATH, v4_sha)

raw2 = raw.replace(v3_entry_close, new_self_ref_entry, 1)

# Anchor B: insert two new top-level keys right after the existing
# w100_4_1_addendum block's closing "}" (i.e. right before the file's final
# closing "}"). Anchored on the exact known tail bytes so a byte-identical
# match is required before any edit (refuses silently-wrong insertion points).
old_tail = (
    '    "v3_sha256": "%s"\n'
    '  }\n'
    '}\n'
) % v3_sha
if raw2.count(old_tail) != 1:
    raise SystemExit("anchor B not found exactly once -- refusing surgical edit (found %d)" % raw2.count(old_tail))

# We append TWO new top-level keys: (1) the plain v4 deliverable pointer
# (mirrors w100_4_1_addendum's shape), and (2) the W101-3.4 fixed-point
# over-claim correction (marks the old known_deviation_disclosed text as a
# historical claim and supplies the corrected current erratum, WITHOUT
# touching the old string byte-for-byte).
new_tail_head = (
    '    "v3_sha256": "%s"\n'
    '  },\n'
) % v3_sha

W1013_ADDENDUM_NOTE = (
    "便101 検収(裁定428)P101-3.1(sol_reply_101_math28.md W101-3.1)の現物修理。"
    "search/certs/ihnec_r4b_conventions_v3_20260802.json は "
    "conventions_used.ledger_version=\\\"conventions_ledger_v1_4\\\" を宣言したまま "
    "v1.5新設のsha256_ref typed objectを使っており(schema version drift)、"
    "search/certs/ihnec_r4b_conventions_v4_20260804.json がこれを訂正して supersede した。"
    "v3ファイル自体・本 manifest の既存 entry は不改変(追記のみ)。"
)

W1014_ADDENDUM_NOTE = (
    "便101 検収(裁定428)P101-3.6(sol_reply_101_math28.md W101-3.4)の現物修理。"
    "本manifestの既存 known_deviation_disclosed の一文(下記 status.original_text_verbatim に"
    "byte保存)は「後継artifactが自己SHA-256を自己bytesに含むことは構造的に不可能」という"
    "数学的過剰主張(W100-4.1で既に指摘済み・sol_reply_100_math27.md §4)である。"
    "この過剰主張はここで historical_claim と指定し、正しい限定文を current erratum として置く。"
)

new_top_keys = (
    '  "w101_3_1_addendum": {\n'
    '    "task_ref": "便101 検収（裁定428）W101-3.1差戻しの現物修理",\n'
    '    "note": "%s",\n'
    '    "v4_path": "%s",\n'
    '    "v4_sha256": "%s"\n'
    '  },\n'
    '  "w101_3_4_addendum": {\n'
    '    "task_ref": "便101 検収（裁定428）W101-3.4差戻しの現物修理",\n'
    '    "note": "%s",\n'
    '    "target_field": "known_deviation_disclosed",\n'
    '    "status": "historical_claim",\n'
    '    "original_text_verbatim": "CV-10(規約台帳v1.4 §2)は superseded_by.sha256 に後継artifact自身のsha256を書くことを要求するが、後継artifactが自分自身の内容のsha256を自分の内容に含むことは構造的に不可能(ハッシュのfixed-point問題)。本納品では、自己参照箇所には明示プレースホルダ文字列を書き、実際の最終sha256は本manifestへ記録する2段階方式を採った。これは規約台帳が明記していない状況への実務判断であり、司令塔裁定を仰ぐ余地を残す(疑問点として報告)。",\n'
    '    "current_erratum": "『構造的に不可能』は過剰主張であり撤回する。正しい限定文は次の通り: 通常の単一書き出しパス(ファイルを一度で確定・保存する生成手順)では、そのファイルが自分自身の最終sha256を内容に含むことを直接には解けない自己参照であり、これを運用schemaとして禁止する(sha256をunion型の自由文字列にせず、自己参照時のみ typed sha256_ref で外部holderをpostwrite解決する -- 台帳v1.5 §1.7 / P100-4.1)。これは実装上・運用上の禁止規約であって、数学的な不可能性の主張ではない(例えば同一ファイルへの複数パス書き出しや外部fixed-point反復解法などの代替は本規約が禁止しているだけで、数学的に不可能とまでは言えない)。"\n'
    '  }\n'
) % (W1013_ADDENDUM_NOTE, V4_RELPATH, v4_sha, W1014_ADDENDUM_NOTE)

new_tail = new_tail_head + new_top_keys + '}\n'
raw3 = raw2.replace(old_tail, new_tail, 1)

with open(MANIFEST_PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write(raw3)

print("Patched (surgical append-only)", relpath(MANIFEST_PATH))
