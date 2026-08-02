# search/probe/wac_v1/ihnec_r4b_v3_selfhash_checker.py
# 便100 検収(裁定422)P100-4.1準拠checker。
#
# P100-4.1指定の5検査:
#   (i)   holderの存在
#   (ii)  target pathの一致 (holder内でjson_pointerが指す記録が、確かに
#         「このcertのpath」の記録であること -- pointer先の兄弟欄 "path" と照合)
#   (iii) そこにある値が64 lowercase hex
#   (iv)  target bytesの再計算一致(実ファイルのsha256を再計算し(iii)と比較)
#   (v)   current entryとeffective_sourceの同一性(cert内部で
#         effective_source_chainの最終entryとconventions_used.effective_source
#         が同じsha256_refを指すこと)
#
# 1つでも欠ければ MALFORMED / INTEGRITY_STOP。
#
# 照合器としての注意(CLAUDE.md鉄則2): 本checkerはGAP探索器のコード・中間結果を
# importしない。証明書(cert JSON)のbytesだけを入力に、上記5検査を独立に
# 再計算する。GAP側 generator (ihnec_r4b_conventions_v3_20260802_gen.py) とは
# helperを共有しない(sha256計算はPython標準ライブラリhashlibのみ使用)。
import json, hashlib, os, sys, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
HEX64 = re.compile(r"^[0-9a-f]{64}$")

class CheckStop(Exception):
    pass

def relpath(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")

def abspath(relp):
    return os.path.join(ROOT, relp.replace("/", os.sep))

def sha_bytes(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def resolve_json_pointer(doc, pointer):
    """RFC 6901 JSON pointer resolution. Returns (value, parent, last_key)."""
    if pointer == "":
        return doc, None, None
    if not pointer.startswith("/"):
        raise CheckStop("json_pointer must start with '/': %r" % pointer)
    parts = pointer[1:].split("/")
    parts = [p.replace("~1", "/").replace("~0", "~") for p in parts]
    cur = doc
    parent = None
    key = None
    for part in parts:
        parent = cur
        key = part
        if isinstance(cur, list):
            idx = int(part)
            cur = cur[idx]
        elif isinstance(cur, dict):
            if part not in cur:
                raise CheckStop("json_pointer segment not found: %r (full=%r)" % (part, pointer))
            cur = cur[part]
        else:
            raise CheckStop("json_pointer descends into non-container at %r" % part)
    return cur, parent, key

def check_sha256_ref(entry_path_label, sha256_ref, expected_cert_relpath, expected_cert_abspath, holder_root=ROOT):
    """
    entry_path_label: human label for error messages (e.g. "effective_source")
    sha256_ref: dict with holder_path, json_pointer, resolution
    expected_cert_relpath: repo-relative path of the cert that this sha256_ref
        is supposed to authenticate (i.e. the file the reference is ABOUT).
    expected_cert_abspath: absolute path to that same file, for bytes recomputation.
    Returns the resolved 64-hex sha256 string on success; raises CheckStop otherwise.
    """
    if not isinstance(sha256_ref, dict):
        raise CheckStop("%s: sha256_ref must be an object" % entry_path_label)
    for k in ("holder_path", "json_pointer", "resolution"):
        if k not in sha256_ref:
            raise CheckStop("%s: sha256_ref missing key %r" % (entry_path_label, k))
    if sha256_ref["resolution"] != "external-postwrite":
        raise CheckStop("%s: unexpected resolution %r" % (entry_path_label, sha256_ref["resolution"]))

    holder_relpath = sha256_ref["holder_path"]
    holder_abspath = os.path.join(holder_root, holder_relpath.replace("/", os.sep))

    # (i) holder の存在
    if not os.path.isfile(holder_abspath):
        raise CheckStop("%s: (i) holder does not exist: %s" % (entry_path_label, holder_relpath))

    try:
        holder_doc = json.load(open(holder_abspath, encoding="utf-8"))
    except Exception as e:
        raise CheckStop("%s: (i) holder is not valid JSON: %s (%s)" % (entry_path_label, holder_relpath, e))

    # resolve pointer -> (value, parent_of_value, key_of_value)
    value, parent, key = resolve_json_pointer(holder_doc, sha256_ref["json_pointer"])

    # (ii) target path の一致: pointer先の兄弟 "path" 欄が、このsha256_refが
    # 認証しようとしているcertのpathと一致すること(pointerが別recordを
    # 指してしまっていないことの確認)
    if not isinstance(parent, dict) or "path" not in parent:
        raise CheckStop("%s: (ii) holder record at pointer parent has no 'path' field to cross-check against" % entry_path_label)
    record_path = parent["path"]
    if record_path != expected_cert_relpath:
        raise CheckStop("%s: (ii) target path mismatch: holder record path=%r != expected cert path=%r" % (entry_path_label, record_path, expected_cert_relpath))

    # (iii) そこにある値が64 lowercase hex
    if not isinstance(value, str) or not HEX64.match(value):
        raise CheckStop("%s: (iii) resolved value is not 64 lowercase hex: %r" % (entry_path_label, value))

    # (iv) target bytes の再計算一致
    if not os.path.isfile(expected_cert_abspath):
        raise CheckStop("%s: (iv) target cert file does not exist: %s" % (entry_path_label, expected_cert_relpath))
    actual = sha_bytes(expected_cert_abspath)
    if actual != value:
        raise CheckStop("%s: (iv) recomputed sha256 mismatch: holder says %s, actual bytes give %s" % (entry_path_label, value, actual))

    return value

def run_checks(cert_path):
    """
    Runs P100-4.1's 5 checks against the given v3-style cert.
    Returns a dict report; raises CheckStop on the first failed mandatory check
    (fail-closed: 1つでも欠ければ MALFORMED/INTEGRITY_STOP).
    """
    cert_relpath = relpath(cert_path)
    cert = json.load(open(cert_path, encoding="utf-8"))
    cu = cert["conventions_used"]

    chain = cu["effective_source_chain"]
    current_entries = [e for e in chain if e.get("role") == "current"]
    if len(current_entries) != 1:
        raise CheckStop("expected exactly 1 role:current entry in effective_source_chain, found %d" % len(current_entries))
    current = current_entries[0]

    if "sha256_ref" not in current:
        raise CheckStop("role:current entry has no sha256_ref (not a self-referencing cert; nothing for this checker to do)")

    v_chain = check_sha256_ref(
        "effective_source_chain[role=current]",
        current["sha256_ref"],
        expected_cert_relpath=cert_relpath,
        expected_cert_abspath=cert_path,
    )

    es = cu["effective_source"]
    if "sha256_ref" not in es:
        raise CheckStop("effective_source has no sha256_ref")
    v_es = check_sha256_ref(
        "effective_source",
        es["sha256_ref"],
        expected_cert_relpath=cert_relpath,
        expected_cert_abspath=cert_path,
    )

    # (v) current entry と effective_source の同一性
    if current.get("path") != es.get("path"):
        raise CheckStop("(v) current.path (%r) != effective_source.path (%r)" % (current.get("path"), es.get("path")))
    if current["sha256_ref"] != es["sha256_ref"]:
        raise CheckStop("(v) current.sha256_ref != effective_source.sha256_ref (not identical typed objects)")
    if v_chain != v_es:
        raise CheckStop("(v) resolved sha256 differs between current entry and effective_source: %s vs %s" % (v_chain, v_es))

    return {
        "cert": cert_relpath,
        "resolved_sha256": v_chain,
        "checks": ["i_holder_exists", "ii_target_path_match", "iii_64hex", "iv_bytes_match", "v_current_eq_effective_source"],
        "verdict": "PASS"
    }

def main_selftest():
    """
    Positive case: the real v3 cert.
    Negative fixtures (in-memory, no extra files written to search/certs/):
      (a) holder missing -> STOP
      (b) json_pointer wrong (points at unrelated record) -> STOP
    """
    v3_path = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v3_20260802.json")

    print("=== positive case: real v3 cert ===")
    report = run_checks(v3_path)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    assert report["verdict"] == "PASS"

    print()
    print("=== negative fixture (a): holder missing ===")
    try:
        bad_ref = {
            "holder_path": "search/certs/DOES_NOT_EXIST_MANIFEST.json",
            "json_pointer": "/self_reference_resolution/x/final_sha256",
            "resolution": "external-postwrite"
        }
        check_sha256_ref("fixture-a", bad_ref, "search/certs/ihnec_r4b_conventions_v3_20260802.json", v3_path)
        print("UNEXPECTED: fixture (a) did not raise -- FAIL")
        sys.exit(1)
    except CheckStop as e:
        print("STOP (expected):", e)

    print()
    print("=== negative fixture (b): json_pointer resolves to a record whose 'path' disagrees with the cert being authenticated ===")
    try:
        # the pointer itself is well-formed and resolves to a real 64-hex value
        # (the v3 record in the real manifest), but we ask check_sha256_ref to
        # authenticate a DIFFERENT cert (v1's path) with it -- (ii) must catch
        # the path disagreement between the resolved record and the claimed cert.
        good_pointer_ref = {
            "holder_path": "search/certs/MANIFEST_sol99_w99_2_1_20260802.json",
            "json_pointer": "/self_reference_resolution/search~1certs~1ihnec_r4b_conventions_v3_20260802.json/final_sha256",
            "resolution": "external-postwrite"
        }
        check_sha256_ref("fixture-b", good_pointer_ref, "search/certs/ihnec_r4b_run_20260801.json", v3_path)
        print("UNEXPECTED: fixture (b) did not raise -- FAIL")
        sys.exit(1)
    except CheckStop as e:
        print("STOP (expected):", e)

    print()
    print("=== negative fixture (c): target bytes tampered (simulated via wrong expected_cert_abspath) ===")
    try:
        good_ref = {
            "holder_path": "search/certs/MANIFEST_sol99_w99_2_1_20260802.json",
            "json_pointer": "/self_reference_resolution/search~1certs~1ihnec_r4b_conventions_v3_20260802.json/final_sha256",
            "resolution": "external-postwrite"
        }
        # point (iv) recomputation at a different, unrelated file's bytes
        wrong_bytes_path = os.path.join(ROOT, "search", "certs", "ihnec_r4b_run_20260801.json")
        check_sha256_ref("fixture-c", good_ref, "search/certs/ihnec_r4b_conventions_v3_20260802.json", wrong_bytes_path)
        print("UNEXPECTED: fixture (c) did not raise -- FAIL")
        sys.exit(1)
    except CheckStop as e:
        print("STOP (expected):", e)

    print()
    print("ALL SELFTEST CASES BEHAVED AS EXPECTED (1 PASS + 3 STOP)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        main_selftest()
    else:
        target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v3_20260802.json")
        try:
            report = run_checks(target)
            print(json.dumps(report, ensure_ascii=False, indent=2))
        except CheckStop as e:
            print("INTEGRITY_STOP / MALFORMED:", e)
            sys.exit(1)
