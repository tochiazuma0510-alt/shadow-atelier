# search/probe/wac_v1/ihnec_r4b_selfhash_checker_v2.py
# 便101 検収(裁定428)P101-3.2〜3.4(sol_reply_101_math28.md §3 W101-3.2/3.3・
# 台帳CL-9)の現物修理。
#
# 旧checker search/probe/wac_v1/ihnec_r4b_v3_selfhash_checker.py(便100 検収・
# 裁定422)は不改変(記録として保存)。本ファイルは別名の v2 として新設する。
#
# 旧checker(v1)の穴(W101-3.3, sol_reply_101_math28.md §3):
#   (1) cert内のsha256_refのうち role="current" と effective_source の2箇所しか
#       解決しない -- nested な superseded_by.sha256_ref は走査されない。
#   (2) current.path == effective_source.path しか見ず、両方が「実際に入力
#       されたcert path」と一致することを見ない(pathを両方とも同じ偽値へ
#       変えればholderを正しく保ったまま通ってしまう)。
#   (3) 同一entryにsha256とsha256_refを併記した排他型違反を拒否しない。
#   (4) selftestの負例が(1)(2)(3)や64-hex型違反を発火させていない。
#
# 本v2は次を実装する:
#   (a) conventions_used 以下を再帰的に走査し、"sha256" または "sha256_ref" を
#       持つ全dict(nested superseded_by含む)を列挙する。
#   (b) 各dictについて:
#       - "sha256" と "sha256_ref" の両方を持てば XOR違反としてSTOP。
#       - "sha256_ref" を持てば、そのdictの兄弟 "path" 欄が指すファイルを対象に
#         P100-4.1の(i)-(iv)を適用する(holder存在・target path一致・64-hex・
#         bytes再計算一致)。
#       - "sha256" のみを持てば、64-hex型を検査する(型検査のみ・bytes再計算は
#         P100-4.1の対象外なので行わない -- 過去certは編集不可のため)。
#   (c) effective_source_chain の role="current" entry と conventions_used.
#       effective_source の双方について、.path が「実際に入力されたcertの
#       repo相対path」と一致することを強制する(current.path==effective_source.path
#       だけでは不十分 -- 両方を実cert pathへ束縛する)。
#   (d) conventions_used.ledger_version が本checkerの対応版
#       (EXPECTED_LEDGER_VERSION)と一致することを要求する。不一致は
#       ledger_version drift としてSTOP(旧v3のように新型sha256_refを使いながら
#       旧版ledger_versionを宣言する食い違いをfail-openで見逃さない)。
#
# 照合器としての注意(CLAUDE.md鉄則2): 本checkerはGAP探索器のコード・中間結果を
# importしない。証明書(cert JSON)のbytesだけを入力に、上記検査を独立に
# 再計算する。sha256計算はPython標準ライブラリhashlibのみ使用。
import json, hashlib, os, sys, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
HEX64 = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_LEDGER_VERSION = "conventions_ledger_v1_5"


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


def check_sha256_ref(entry_label, sha256_ref, expected_cert_relpath, expected_cert_abspath):
    """
    P100-4.1's (i)-(iv) applied to a single sha256_ref, authenticating the
    file at expected_cert_relpath/expected_cert_abspath.
    Returns the resolved 64-hex sha256 string on success; raises CheckStop
    otherwise.
    """
    if not isinstance(sha256_ref, dict):
        raise CheckStop("%s: sha256_ref must be an object" % entry_label)
    for k in ("holder_path", "json_pointer", "resolution"):
        if k not in sha256_ref:
            raise CheckStop("%s: sha256_ref missing key %r" % (entry_label, k))
    if sha256_ref["resolution"] != "external-postwrite":
        raise CheckStop("%s: unexpected resolution %r" % (entry_label, sha256_ref["resolution"]))

    holder_relpath = sha256_ref["holder_path"]
    holder_abspath = abspath(holder_relpath)

    # (i) holder の存在
    if not os.path.isfile(holder_abspath):
        raise CheckStop("%s: (i) holder does not exist: %s" % (entry_label, holder_relpath))

    try:
        holder_doc = json.load(open(holder_abspath, encoding="utf-8"))
    except Exception as e:
        raise CheckStop("%s: (i) holder is not valid JSON: %s (%s)" % (entry_label, holder_relpath, e))

    value, parent, key = resolve_json_pointer(holder_doc, sha256_ref["json_pointer"])

    # (ii) target path の一致
    if not isinstance(parent, dict) or "path" not in parent:
        raise CheckStop("%s: (ii) holder record at pointer parent has no 'path' field to cross-check against" % entry_label)
    record_path = parent["path"]
    if record_path != expected_cert_relpath:
        raise CheckStop("%s: (ii) target path mismatch: holder record path=%r != expected cert path=%r" % (entry_label, record_path, expected_cert_relpath))

    # (iii) そこにある値が64 lowercase hex
    if not isinstance(value, str) or not HEX64.match(value):
        raise CheckStop("%s: (iii) resolved value is not 64 lowercase hex: %r" % (entry_label, value))

    # (iv) target bytes の再計算一致
    if not os.path.isfile(expected_cert_abspath):
        raise CheckStop("%s: (iv) target cert file does not exist: %s" % (entry_label, expected_cert_relpath))
    actual = sha_bytes(expected_cert_abspath)
    if actual != value:
        raise CheckStop("%s: (iv) recomputed sha256 mismatch: holder says %s, actual bytes give %s" % (entry_label, value, actual))

    return value


def walk_sha_containers(node, label):
    """
    Recursively yield (label, dict) for every dict in the tree that carries a
    "sha256" and/or "sha256_ref" key -- including dicts nested inside
    "superseded_by" or any other structure (this is the fix for W101-3.3(1):
    the v1 checker only looked at two hardcoded locations).
    """
    if isinstance(node, dict):
        if "sha256" in node or "sha256_ref" in node:
            yield (label, node)
        for k, v in node.items():
            yield from walk_sha_containers(v, "%s.%s" % (label, k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_sha_containers(v, "%s[%d]" % (label, i))


def run_checks_on_cert(cert_relpath, cert_abspath, cert):
    """
    Core logic, parameterized on an explicit (cert_relpath, cert_abspath) pair
    identifying the "actual input cert" (used both by run_checks(path), which
    derives these from the file it loads, and by the selftest fixtures, which
    pass a mutated in-memory copy of the real v4 cert while still binding to
    the real v4 file's identity).
    """
    cu = cert["conventions_used"]

    # (d) ledger_version must match the schema version this checker targets.
    # A cert that declares an older ledger_version while using the newer
    # typed sha256_ref schema (W101-3.1's v3 drift) must not silently pass.
    lv = cu.get("ledger_version")
    if lv != EXPECTED_LEDGER_VERSION:
        raise CheckStop(
            "ledger_version drift: cert declares ledger_version=%r but this checker "
            "(checker v2) requires %r -- the sha256_ref typed-object schema this cert "
            "uses was only defined starting %s (P100-4.1); a cert claiming an older "
            "ledger_version is MALFORMED / INTEGRITY_STOP, not fail-open"
            % (lv, EXPECTED_LEDGER_VERSION, EXPECTED_LEDGER_VERSION)
        )

    # (a)+(b): enumerate every sha256/sha256_ref-bearing dict under
    # conventions_used, reject XOR co-presence, apply (i)-(iv) to every
    # sha256_ref, type-check every plain sha256.
    containers = list(walk_sha_containers(cu, "conventions_used"))
    if not containers:
        raise CheckStop("no sha256/sha256_ref-bearing object found under conventions_used")

    scanned = []
    for label, obj in containers:
        has_plain = "sha256" in obj
        has_ref = "sha256_ref" in obj
        if has_plain and has_ref:
            raise CheckStop("%s: XOR violation -- both 'sha256' and 'sha256_ref' present in the same entry" % label)
        if has_ref:
            claimed_path = obj.get("path")
            if not claimed_path:
                raise CheckStop("%s: sha256_ref present but no sibling 'path' field to authenticate against" % label)
            v = check_sha256_ref(label, obj["sha256_ref"], expected_cert_relpath=claimed_path, expected_cert_abspath=abspath(claimed_path))
        else:
            v = obj.get("sha256")
            if not (isinstance(v, str) and HEX64.match(v)):
                raise CheckStop("%s: (iii) plain sha256 is not 64 lowercase hex: %r" % (label, v))
        scanned.append({"label": label, "path": obj.get("path"), "resolved_sha256": v, "kind": "sha256_ref" if has_ref else "sha256"})

    # (c) current entry / effective_source / actual input cert: three-way
    # path identity (W101-3.3(2) fix -- checking current.path==effective_source.path
    # alone lets both be tampered to the same wrong value while the holder
    # stays technically "correct").
    chain = cu["effective_source_chain"]
    current_entries = [e for e in chain if e.get("role") == "current"]
    if len(current_entries) != 1:
        raise CheckStop("expected exactly 1 role:current entry in effective_source_chain, found %d" % len(current_entries))
    current = current_entries[0]
    es = cu["effective_source"]

    if current.get("path") != cert_relpath:
        raise CheckStop("(c) effective_source_chain[role=current].path (%r) != actual input cert path (%r)" % (current.get("path"), cert_relpath))
    if es.get("path") != cert_relpath:
        raise CheckStop("(c) effective_source.path (%r) != actual input cert path (%r)" % (es.get("path"), cert_relpath))

    if "sha256_ref" not in current:
        raise CheckStop("role:current entry has no sha256_ref (not a self-referencing cert; nothing for this checker to do)")
    if "sha256_ref" not in es:
        raise CheckStop("effective_source has no sha256_ref")

    v_current = check_sha256_ref(
        "effective_source_chain[role=current]",
        current["sha256_ref"],
        expected_cert_relpath=cert_relpath,
        expected_cert_abspath=cert_abspath,
    )
    v_es = check_sha256_ref(
        "effective_source",
        es["sha256_ref"],
        expected_cert_relpath=cert_relpath,
        expected_cert_abspath=cert_abspath,
    )
    if current["sha256_ref"] != es["sha256_ref"]:
        raise CheckStop("(v) current.sha256_ref != effective_source.sha256_ref (not identical typed objects)")
    if v_current != v_es:
        raise CheckStop("(v) resolved sha256 differs between current entry and effective_source: %s vs %s" % (v_current, v_es))

    return {
        "cert": cert_relpath,
        "ledger_version": lv,
        "resolved_sha256": v_current,
        "sha256_ref_and_sha256_locations_scanned": len(scanned),
        "scanned": scanned,
        "checks": [
            "d_ledger_version_match",
            "a_all_sha256_ref_enumerated_including_nested_superseded_by",
            "b3_xor_sha256_vs_sha256_ref",
            "i_holder_exists",
            "ii_target_path_match",
            "iii_64hex",
            "iv_bytes_match",
            "c_current_eq_effective_source_eq_actual_input_path",
            "v_current_eq_effective_source_resolved_value",
        ],
        "verdict": "PASS",
    }


def run_checks(cert_path):
    cert_relpath = relpath(cert_path)
    cert = json.load(open(cert_path, encoding="utf-8"))
    return run_checks_on_cert(cert_relpath, cert_path, cert)


def deepcopy(obj):
    return json.loads(json.dumps(obj))


def main_selftest():
    V4_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v4_20260804.json")
    V4_RELPATH = relpath(V4_PATH)
    V3_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v3_20260802.json")

    real_v4 = json.load(open(V4_PATH, encoding="utf-8"))

    n_pass = 0
    n_stop = 0

    def expect_pass(label, fn):
        nonlocal n_pass
        print("=== %s ===" % label)
        report = fn()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        assert report["verdict"] == "PASS"
        n_pass += 1
        print()

    def expect_stop(label, fn, must_contain=None):
        nonlocal n_stop
        print("=== %s ===" % label)
        try:
            fn()
            print("UNEXPECTED: did not raise -- FAIL")
            sys.exit(1)
        except CheckStop as e:
            msg = str(e)
            if must_contain and must_contain not in msg:
                print("UNEXPECTED: STOP fired but message did not mention %r: %s" % (must_contain, msg))
                sys.exit(1)
            print("STOP (expected):", msg)
            n_stop += 1
        print()

    # --- positive case: the real v4 cert (all 3 sha256_ref locations, nested
    # superseded_by included, must resolve and match) ---
    expect_pass("positive case: real v4 cert", lambda: run_checks(V4_PATH))

    # --- regression: real v3 cert must be flagged for ledger_version drift
    # (fail-closed, not fail-open -- this is the exact case W101-3.1 raised) ---
    expect_stop(
        "regression: real v3 cert flagged for ledger_version drift",
        lambda: run_checks(V3_PATH),
        must_contain="ledger_version drift",
    )

    # --- old negative fixture (a): holder missing ---
    def fixture_a():
        bad_ref = {
            "holder_path": "search/certs/DOES_NOT_EXIST_MANIFEST.json",
            "json_pointer": "/self_reference_resolution/x/final_sha256",
            "resolution": "external-postwrite"
        }
        check_sha256_ref("fixture-a", bad_ref, V4_RELPATH, V4_PATH)
    expect_stop("negative (a): holder missing", fixture_a, must_contain="(i)")

    # --- old negative fixture (b): json_pointer resolves to a record whose
    # 'path' disagrees with the cert being authenticated ---
    def fixture_b():
        good_pointer_ref = {
            "holder_path": "search/certs/MANIFEST_sol99_w99_2_1_20260802.json",
            "json_pointer": "/self_reference_resolution/search~1certs~1ihnec_r4b_conventions_v4_20260804.json/final_sha256",
            "resolution": "external-postwrite"
        }
        check_sha256_ref("fixture-b", good_pointer_ref, "search/certs/ihnec_r4b_run_20260801.json", V4_PATH)
    expect_stop("negative (b): json_pointer target path mismatch", fixture_b, must_contain="(ii)")

    # --- old negative fixture (c): target bytes tampered (simulated via wrong
    # expected_cert_abspath) ---
    def fixture_c():
        good_ref = {
            "holder_path": "search/certs/MANIFEST_sol99_w99_2_1_20260802.json",
            "json_pointer": "/self_reference_resolution/search~1certs~1ihnec_r4b_conventions_v4_20260804.json/final_sha256",
            "resolution": "external-postwrite"
        }
        wrong_bytes_path = os.path.join(ROOT, "search", "certs", "ihnec_r4b_run_20260801.json")
        check_sha256_ref("fixture-c", good_ref, V4_RELPATH, wrong_bytes_path)
    expect_stop("negative (c): target bytes tampered", fixture_c, must_contain="(iv)")

    # --- new negative fixture (d): 64-hex type violation (mutate a plain
    # sha256 field to a non-hex value) ---
    def fixture_d():
        cert = deepcopy(real_v4)
        cert["conventions_used"]["effective_source_chain"][0]["sha256"] = "NOT-A-VALID-HEX-DIGEST"
        run_checks_on_cert(V4_RELPATH, V4_PATH, cert)
    expect_stop("negative (d): 64-hex type violation on a plain sha256 field", fixture_d, must_contain="(iii)")

    # --- new negative fixture (e): the "current" entry is changed to an
    # internally-consistent lie -- its path + sha256_ref are BOTH swapped
    # (together) to authenticate a different real cert (v3) instead of the
    # file actually being checked (v4). This passes the generic per-entry
    # (i)-(iv) scan (v3's real bytes really do match), so only the explicit
    # (c) three-way path-identity check against the actual input file catches
    # it. ---
    V3_REF = {
        "holder_path": "search/certs/MANIFEST_sol99_w99_2_1_20260802.json",
        "json_pointer": "/self_reference_resolution/search~1certs~1ihnec_r4b_conventions_v3_20260802.json/final_sha256",
        "resolution": "external-postwrite"
    }
    V3_RELPATH_FOR_FIXTURES = "search/certs/ihnec_r4b_conventions_v3_20260802.json"

    def fixture_e():
        cert = deepcopy(real_v4)
        current_entry = [e for e in cert["conventions_used"]["effective_source_chain"] if e.get("role") == "current"][0]
        current_entry["path"] = V3_RELPATH_FOR_FIXTURES
        current_entry["sha256_ref"] = V3_REF
        run_checks_on_cert(V4_RELPATH, V4_PATH, cert)
    expect_stop(
        "negative (e): current entry internally-consistently claims to be a different real cert (v3), not the actual input (v4)",
        fixture_e, must_contain="(c)"
    )

    # --- new negative fixture (f): a previously-unscanned nested
    # superseded_by.sha256_ref is corrupted (points at the wrong holder) ---
    def fixture_f():
        cert = deepcopy(real_v4)
        chain = cert["conventions_used"]["effective_source_chain"]
        # entry[3] is role="erratum", path=v3, whose superseded_by.sha256_ref
        # points at v4 -- this exact nested location was NOT scanned by the
        # v1 checker (W101-3.3(1)).
        assert "superseded_by" in chain[3] and "sha256_ref" in chain[3]["superseded_by"]
        chain[3]["superseded_by"]["sha256_ref"]["holder_path"] = "search/certs/DOES_NOT_EXIST_MANIFEST.json"
        run_checks_on_cert(V4_RELPATH, V4_PATH, cert)
    expect_stop("negative (f): previously-unscanned nested superseded_by.sha256_ref corrupted", fixture_f, must_contain="(i)")

    # --- new negative fixture (g): XOR violation (sha256 and sha256_ref both
    # present on the same entry) ---
    def fixture_g():
        cert = deepcopy(real_v4)
        current_entry = [e for e in cert["conventions_used"]["effective_source_chain"] if e.get("role") == "current"][0]
        current_entry["sha256"] = "0" * 64
        run_checks_on_cert(V4_RELPATH, V4_PATH, cert)
    expect_stop("negative (g): XOR violation -- sha256 and sha256_ref co-present", fixture_g, must_contain="XOR")

    # --- new negative fixture (h): path spoofing, exactly per W101-3.3(2) --
    # current.path AND effective_source.path are BOTH changed (together, with
    # matching sha256_ref) to the SAME different-but-real cert (v3). This
    # means current==effective_source still holds (old check (v) would pass),
    # and each individually is internally consistent with the holder (generic
    # (i)-(iv) scan passes), so ONLY the explicit (c) check -- binding both to
    # the actual input file's own path -- catches the spoof. ---
    def fixture_h():
        cert = deepcopy(real_v4)
        cu = cert["conventions_used"]
        current_entry = [e for e in cu["effective_source_chain"] if e.get("role") == "current"][0]
        current_entry["path"] = V3_RELPATH_FOR_FIXTURES
        current_entry["sha256_ref"] = V3_REF
        cu["effective_source"]["path"] = V3_RELPATH_FOR_FIXTURES
        cu["effective_source"]["sha256_ref"] = V3_REF
        run_checks_on_cert(V4_RELPATH, V4_PATH, cert)
    expect_stop(
        "negative (h): path spoofing -- current.path==effective_source.path (both consistently claim v3) but neither == actual input path (v4)",
        fixture_h, must_contain="(c)"
    )

    print("=" * 70)
    print("ALL SELFTEST CASES BEHAVED AS EXPECTED (%d PASS + %d STOP)" % (n_pass, n_stop))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        main_selftest()
    else:
        target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v4_20260804.json")
        try:
            report = run_checks(target)
            print(json.dumps(report, ensure_ascii=False, indent=2))
        except CheckStop as e:
            print("INTEGRITY_STOP / MALFORMED:", e)
            sys.exit(1)
