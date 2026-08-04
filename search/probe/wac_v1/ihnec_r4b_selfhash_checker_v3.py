# search/probe/wac_v1/ihnec_r4b_selfhash_checker_v3.py
# 便102 F102-4.1 差戻し(sol/sol_reply_102_math29.md §4)の現物修理。
#
# 旧checker は不改変で保存する(記録):
#   - v1: search/probe/wac_v1/ihnec_r4b_v3_selfhash_checker.py (便100検収・裁定422)
#   - v2: search/probe/wac_v1/ihnec_r4b_selfhash_checker_v2.py (便101検収・裁定428/431/433)
# 本ファイルは別名の v3 として新設する(versioned supersede・既存検査は
# 一つも削らず・弱めず、追加のみ = additive only)。
#
# ---------------------------------------------------------------------------
# v2 の穴(便102 F102-4.1・Sol が変異注入で実証)
# ---------------------------------------------------------------------------
# v2 の走査 walk_sha_containers() は「**既に** sha256 または sha256_ref を持つ
# dict」を列挙する。したがって本来 digest を持つべき entry から**双方を消す**と、
# その entry 自体が走査対象から消える。Sol の再現:
#
#     v4 の effective_source_chain[0] から sha256 をメモリ上で除去 -> PASS, scanned 8
#
# これは台帳規範11(§2・v1.6新設)の XOR = 「ちょうど一方を持つ」のうち、
# 「両方持つ」側しか実装しておらず、「**どちらも持たない**」側(missing-both)を
# 実装していなかったということである。文書(§1.7.3′ (viii))は既に
# 「両方書いたもの・どちらも無いものを MALFORMED」と書いていたので、
# これは規範の欠落ではなく **実装の欠落**である。
#
# ---------------------------------------------------------------------------
# v3 の設計変更(核心)
# ---------------------------------------------------------------------------
# 走査を「値の発見(discovery)」から「**構造からの必須位置列挙**」へ反転する。
#
#   enumerate_required_digest_positions(cert)
#       = schema 上 digest が必須である位置を、**その位置に digest があるか
#         どうかとは無関係に**、cert の構造だけから列挙する。
#         (top-level supersedes / supplements_cert / ledger_artifact_pin,
#          conventions_used.effective_source,
#          conventions_used.effective_source_chain[i] の各 entry,
#          その入れ子 superseded_by(再帰的に何段でも))
#
# 各必須位置で **sha256 XOR sha256_ref**(規範11)を検査する。
#   - 両方ある  -> STOP "XOR violation (both)"
#   - どちらも無い -> STOP "XOR violation (missing-both)"   <-- ★ v3 の新規検出
#
# さらに v2 の discovery walk も**belt として残す**(削らない)。必須位置集合に
# 入っていない場所に digest が現れた場合も、XOR と (i)-(iv)/(iii) を適用する。
# discovery 側は原理上 missing-both を検出できない(存在しない値は発見できない)
# ので、missing-both の検出責任は必須位置列挙側が単独で負う。
#
# 追加検査(v2 に無かったもの・additive):
#   (x)   plain sha256 の **bytes 再計算一致**。v2 は plain sha256 を 64-hex の
#         型検査だけで通していた。v5 の連鎖に載る過去 artifact は全て bytes 確定
#         済みなので、実際に再計算して突合できる(合わなければ STOP)。
#   (xi)  ledger_artifact_pin: cert が宣言する ledger_version が、pin された
#         台帳 artifact の bytes(sha256)と declared_version に束縛されること。
#         「宣言だけして実物と食い違う」型(= F102-4.1 の指摘1そのもの)を、
#         宣言文の照合ではなく **digest 照合**で塞ぐ。
#
# 既存検査は全て維持: (d) ledger_version 一致 / (i) holder 実在 / (ii) target
# path 一致 / (iii) 64-hex / (iv) bytes 再計算 / (c) current=effective_source=
# 実入力 path の三者一致 / (v) current と effective_source の解決値一致 /
# XOR(both 側)/ nested superseded_by の走査。
#
# 照合器としての注意(CLAUDE.md鉄則2): 本checkerはGAP探索器のコード・中間結果を
# importしない。証明書(cert JSON)のbytesだけを入力に上記検査を独立に再計算する。
# sha256計算はPython標準ライブラリhashlibのみ使用。
import json, hashlib, os, sys, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
HEX64 = re.compile(r"^[0-9a-f]{64}$")

# 本 checker が対応する live 台帳版。cert の conventions_used.ledger_version が
# これと一致しない場合は fail-closed で STOP(推測して PASS にしない)。
# 便102 F102-4.1 の指摘1: v4 は v1_5 を宣言したまま束の申告は v1.6 だった。
# v5 は live 台帳 artifact(docs/notes/conventions_ledger_v1.md = v1.6)を宣言し、
# その bytes を ledger_artifact_pin で pin する。
# (台帳 v1.7 は**草案・未発効**につき宣言しない — 発効判定は司令塔+Sol の専権。)
EXPECTED_LEDGER_VERSION = "conventions_ledger_v1_6"

DEFAULT_CERT = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v5_20260805.json")


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
    otherwise.  (Unchanged from checker v2.)
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


# ---------------------------------------------------------------------------
# ★ v3 の核心: 構造からの必須位置列挙(値の有無に依存しない)
# ---------------------------------------------------------------------------
TOP_LEVEL_REQUIRED_DIGEST_KEYS = ("supersedes", "supplements_cert", "ledger_artifact_pin")


def _collect_superseded_chain(label, entry, out):
    """entry.superseded_by を再帰的に(何段でも)必須位置として積む。"""
    node = entry
    lbl = label
    seen = 0
    while isinstance(node, dict) and "superseded_by" in node:
        node = node["superseded_by"]
        lbl = lbl + ".superseded_by"
        seen += 1
        if seen > 64:
            raise CheckStop("%s: superseded_by nesting too deep (>64) -- refusing" % lbl)
        if not isinstance(node, dict):
            raise CheckStop("%s: superseded_by must be an object, got %r" % (lbl, type(node).__name__))
        out.append((lbl, node))


def enumerate_required_digest_positions(cert):
    """
    Enumerate every position where the schema REQUIRES a digest, derived from
    the document STRUCTURE -- independently of whether a digest is actually
    present there.  This is the fix for 便102 F102-4.1: checker v2 enumerated
    "dicts that already carry a digest", so deleting both digest fields from a
    digest-bearing entry also deleted the entry from the scan.

    Returns [(label, dict), ...].
    """
    out = []

    if not isinstance(cert, dict):
        raise CheckStop("cert root must be an object")

    # 1. top-level pins required by the ihnec-r4b-conventions-supplement schema.
    for k in TOP_LEVEL_REQUIRED_DIGEST_KEYS:
        if k not in cert:
            raise CheckStop(
                "schema requires top-level %r (digest-bearing pin) -- missing field is "
                "MALFORMED, not 'not applicable' (規範1)" % k
            )
        if not isinstance(cert[k], dict):
            raise CheckStop("top-level %r must be an object" % k)
        out.append((k, cert[k]))

    cu = cert.get("conventions_used")
    if not isinstance(cu, dict):
        raise CheckStop("conventions_used missing or not an object")

    # 2. effective_source (CV-10).
    if "effective_source" not in cu:
        raise CheckStop("conventions_used.effective_source is required (CV-10) -- missing is MALFORMED")
    es = cu["effective_source"]
    if not isinstance(es, dict):
        raise CheckStop("conventions_used.effective_source must be an object (CV-10 原則③)")
    out.append(("conventions_used.effective_source", es))
    _collect_superseded_chain("conventions_used.effective_source", es, out)

    # 3. effective_source_chain: EVERY entry is a digest-bearing position,
    #    plus every nested superseded_by.
    if "effective_source_chain" not in cu:
        raise CheckStop("conventions_used.effective_source_chain is required (CV-10) -- missing is MALFORMED")
    chain = cu["effective_source_chain"]
    if not isinstance(chain, list) or not chain:
        raise CheckStop("conventions_used.effective_source_chain must be a non-empty array")
    for i, e in enumerate(chain):
        lbl = "conventions_used.effective_source_chain[%d]" % i
        if not isinstance(e, dict):
            raise CheckStop("%s must be an object" % lbl)
        out.append((lbl, e))
        _collect_superseded_chain(lbl, e, out)

    return out


def walk_sha_containers(node, label):
    """
    (Retained from checker v2 -- NOT removed.)  Recursively yield (label, dict)
    for every dict in the tree that carries a "sha256" and/or "sha256_ref" key.
    In v3 this is a *belt*: it catches digests appearing in positions the
    structural enumerator does not know about.  By construction it can never
    detect missing-both (an absent value cannot be discovered); that duty is
    carried solely by enumerate_required_digest_positions().
    """
    if isinstance(node, dict):
        if "sha256" in node or "sha256_ref" in node:
            yield (label, node)
        for k, v in node.items():
            yield from walk_sha_containers(v, "%s.%s" % (label, k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_sha_containers(v, "%s[%d]" % (label, i))


def check_xor(label, obj, required):
    """
    台帳規範11(v1.6 §2): digest を持つ全ての欄は sha256 と sha256_ref の
    **ちょうど一方**を持つ。
      - 両方  -> STOP (v2 も検出していた)
      - 皆無  -> STOP (★ v3 で新規に検出。required=True の位置でのみ意味を持つ)
    Returns ("sha256"|"sha256_ref").
    """
    has_plain = "sha256" in obj
    has_ref = "sha256_ref" in obj
    if has_plain and has_ref:
        raise CheckStop(
            "%s: XOR violation (both) -- 'sha256' and 'sha256_ref' are both present "
            "in the same entry (規範11)" % label
        )
    if not has_plain and not has_ref:
        if not required:
            raise CheckStop("%s: internal -- check_xor(required=False) called on a digest-free dict" % label)
        raise CheckStop(
            "%s: XOR violation (missing-both) -- this position is digest-REQUIRED by the "
            "schema but carries neither 'sha256' nor 'sha256_ref' (規範11: ちょうど一方). "
            "欠品は『非該当』ではなく MALFORMED / INTEGRITY_STOP" % label
        )
    return "sha256" if has_plain else "sha256_ref"


def validate_digest_position(label, obj, kind):
    """
    Apply the per-position digest checks and return the resolved 64-hex value.
      sha256_ref -> (i)-(iv) against the sibling 'path'.
      sha256     -> (iii) 64-hex type check, plus ★ (x) bytes recomputation
                    against the sibling 'path' (new in v3; v2 stopped at type).
    """
    claimed_path = obj.get("path")
    if not claimed_path:
        raise CheckStop("%s: digest-bearing entry has no sibling 'path' field to authenticate against" % label)
    if kind == "sha256_ref":
        return check_sha256_ref(label, obj["sha256_ref"], expected_cert_relpath=claimed_path,
                                expected_cert_abspath=abspath(claimed_path))
    v = obj.get("sha256")
    if not (isinstance(v, str) and HEX64.match(v)):
        raise CheckStop("%s: (iii) plain sha256 is not 64 lowercase hex: %r" % (label, v))
    # ★ (x) plain digest bytes verification (additive; v2 did type-check only).
    target_abs = abspath(claimed_path)
    if not os.path.isfile(target_abs):
        raise CheckStop("%s: (x) target file for plain sha256 does not exist: %s" % (label, claimed_path))
    actual = sha_bytes(target_abs)
    if actual != v:
        raise CheckStop("%s: (x) plain sha256 does not match target bytes: cert says %s, actual bytes give %s (%s)"
                        % (label, v, actual, claimed_path))
    return v


def check_ledger_pin(cert, declared_ledger_version):
    """
    ★ (xi) v3 新設.  The cert's declared ledger_version must be bound to the
    actual bytes of the live ledger artifact, not merely asserted in prose.
    便102 F102-4.1 の指摘1(宣言 v1_5 / 申告 v1.6 の齟齬)を digest で塞ぐ。
    The digest itself is validated by validate_digest_position(); here we only
    bind the version strings.
    """
    pin = cert["ledger_artifact_pin"]
    for k in ("path", "sha256", "declared_version"):
        if k not in pin:
            raise CheckStop("ledger_artifact_pin missing key %r" % k)
    if pin["declared_version"] != declared_ledger_version:
        raise CheckStop(
            "(xi) ledger pin drift: ledger_artifact_pin.declared_version=%r != "
            "conventions_used.ledger_version=%r" % (pin["declared_version"], declared_ledger_version)
        )
    return {"path": pin["path"], "sha256": pin["sha256"], "declared_version": pin["declared_version"]}


def run_checks_on_cert(cert_relpath, cert_abspath, cert):
    """
    Core logic, parameterized on an explicit (cert_relpath, cert_abspath) pair
    identifying the "actual input cert" (used both by run_checks(path) and by
    the selftest fixtures, which pass a mutated in-memory copy of the real v5
    cert while still binding to the real v5 file's identity).
    """
    cu = cert.get("conventions_used")
    if not isinstance(cu, dict):
        raise CheckStop("conventions_used missing or not an object")

    # (d) ledger_version must match the live ledger version this checker targets.
    lv = cu.get("ledger_version")
    if lv != EXPECTED_LEDGER_VERSION:
        raise CheckStop(
            "ledger_version drift: cert declares ledger_version=%r but this checker "
            "(checker v3) requires %r -- a cert must declare the live ledger version it "
            "actually uses (便102 F102-4.1 指摘1); mismatch is MALFORMED / INTEGRITY_STOP, "
            "not fail-open" % (lv, EXPECTED_LEDGER_VERSION)
        )

    # ---- ★ structural enumeration of digest-REQUIRED positions ----
    required = enumerate_required_digest_positions(cert)
    required_ids = set(id(obj) for _, obj in required)

    scanned = []
    for label, obj in required:
        kind = check_xor(label, obj, required=True)          # both / missing-both
        v = validate_digest_position(label, obj, kind)
        scanned.append({"label": label, "path": obj.get("path"), "resolved_sha256": v,
                        "kind": kind, "position": "required"})

    # ---- belt: discovery walk (retained from v2) over the WHOLE cert ----
    discovered = 0
    for label, obj in walk_sha_containers(cert, "cert"):
        if id(obj) in required_ids:
            continue
        kind = check_xor(label, obj, required=True)
        v = validate_digest_position(label, obj, kind)
        discovered += 1
        scanned.append({"label": label, "path": obj.get("path"), "resolved_sha256": v,
                        "kind": kind, "position": "discovered"})

    # ---- (xi) ledger artifact pin <-> declared ledger_version ----
    ledger_pin = check_ledger_pin(cert, lv)

    # ---- (c) current entry / effective_source / actual input cert: three-way
    # path identity (retained from v2, W101-3.3(2) fix) ----
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
        "checker": "ihnec_r4b_selfhash_checker_v3",
        "ledger_version": lv,
        "ledger_artifact_pin": ledger_pin,
        "resolved_sha256": v_current,
        "required_digest_positions": len(required),
        "discovered_extra_digest_positions": discovered,
        "sha256_ref_and_sha256_locations_scanned": len(scanned),
        "scanned": scanned,
        "checks": [
            "d_ledger_version_match",
            "structural_enumeration_of_digest_required_positions",
            "xor_both_present",
            "xor_missing_both",
            "belt_discovery_walk_whole_cert",
            "i_holder_exists",
            "ii_target_path_match",
            "iii_64hex",
            "iv_bytes_match",
            "x_plain_sha256_bytes_match",
            "xi_ledger_artifact_pin_binding",
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


# ---------------------------------------------------------------------------
# selftest / mutant matrix
# ---------------------------------------------------------------------------
def main_selftest():
    V5_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v5_20260805.json")
    V5_RELPATH = relpath(V5_PATH)
    V4_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v4_20260804.json")
    V4_RELPATH = relpath(V4_PATH)
    V3_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v3_20260802.json")

    real_v5 = json.load(open(V5_PATH, encoding="utf-8"))
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

    def current_of(cert):
        return [e for e in cert["conventions_used"]["effective_source_chain"] if e.get("role") == "current"][0]

    # === positive ===============================================
    expect_pass("P1 positive: real v5 cert", lambda: run_checks(V5_PATH))

    # === regression: earlier certs must be flagged, not fail-open ==========
    expect_stop("R1 regression: real v4 cert flagged for ledger_version drift",
                lambda: run_checks(V4_PATH), must_contain="ledger_version drift")
    expect_stop("R2 regression: real v3 cert flagged for ledger_version drift",
                lambda: run_checks(V3_PATH), must_contain="ledger_version drift")

    # === negative fixtures retained from checker v2 (all kept) ============
    def fixture_a():
        bad_ref = {"holder_path": "search/certs/DOES_NOT_EXIST_MANIFEST.json",
                   "json_pointer": "/self_reference_resolution/x/final_sha256",
                   "resolution": "external-postwrite"}
        check_sha256_ref("fixture-a", bad_ref, V5_RELPATH, V5_PATH)
    expect_stop("N-a: holder missing", fixture_a, must_contain="(i)")

    V5_KEY = V5_RELPATH.replace("~", "~0").replace("/", "~1")
    GOOD_V5_REF = {"holder_path": "search/certs/MANIFEST_sol99_w99_2_1_20260802.json",
                   "json_pointer": "/self_reference_resolution/%s/final_sha256" % V5_KEY,
                   "resolution": "external-postwrite"}

    def fixture_b():
        check_sha256_ref("fixture-b", GOOD_V5_REF, "search/certs/ihnec_r4b_run_20260801.json", V5_PATH)
    expect_stop("N-b: json_pointer target path mismatch", fixture_b, must_contain="(ii)")

    def fixture_c():
        wrong_bytes_path = os.path.join(ROOT, "search", "certs", "ihnec_r4b_run_20260801.json")
        check_sha256_ref("fixture-c", GOOD_V5_REF, V5_RELPATH, wrong_bytes_path)
    expect_stop("N-c: target bytes tampered", fixture_c, must_contain="(iv)")

    def fixture_d():
        cert = deepcopy(real_v5)
        cert["conventions_used"]["effective_source_chain"][0]["sha256"] = "NOT-A-VALID-HEX-DIGEST"
        run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_stop("N-d: 64-hex type violation on a plain sha256 field", fixture_d, must_contain="(iii)")

    V4_KEY = V4_RELPATH.replace("~", "~0").replace("/", "~1")
    V4_REF = {"holder_path": "search/certs/MANIFEST_sol99_w99_2_1_20260802.json",
              "json_pointer": "/self_reference_resolution/%s/final_sha256" % V4_KEY,
              "resolution": "external-postwrite"}

    def fixture_e():
        cert = deepcopy(real_v5)
        ce = current_of(cert)
        ce["path"] = V4_RELPATH
        ce["sha256_ref"] = V4_REF
        run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_stop("N-e: current entry internally-consistently claims a different real cert (v4)",
                fixture_e, must_contain="(c)")

    def fixture_f():
        cert = deepcopy(real_v5)
        chain = cert["conventions_used"]["effective_source_chain"]
        tgt = [e for e in chain if "superseded_by" in e and "sha256_ref" in e["superseded_by"]]
        assert tgt, "no nested superseded_by.sha256_ref found -- fixture premise broken"
        tgt[0]["superseded_by"]["sha256_ref"]["holder_path"] = "search/certs/DOES_NOT_EXIST_MANIFEST.json"
        run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_stop("N-f: nested superseded_by.sha256_ref corrupted", fixture_f, must_contain="(i)")

    def fixture_g():
        cert = deepcopy(real_v5)
        current_of(cert)["sha256"] = "0" * 64
        run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_stop("N-g: XOR violation (both) -- sha256 and sha256_ref co-present",
                fixture_g, must_contain="XOR violation (both)")

    def fixture_h():
        cert = deepcopy(real_v5)
        cu = cert["conventions_used"]
        ce = current_of(cert)
        ce["path"] = V4_RELPATH
        ce["sha256_ref"] = V4_REF
        cu["effective_source"]["path"] = V4_RELPATH
        cu["effective_source"]["sha256_ref"] = V4_REF
        run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_stop("N-h: path spoofing -- current.path==effective_source.path but neither == actual input",
                fixture_h, must_contain="(c)")

    # === ★ NEW in v3: missing-both (便102 F102-4.1 / Sol の実証した変異) ====
    def fixture_i():
        cert = deepcopy(real_v5)
        e0 = cert["conventions_used"]["effective_source_chain"][0]
        assert "sha256" in e0
        del e0["sha256"]          # <- Sol's exact mutation, transposed to v5
        run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_stop("N-i ★: missing-both on effective_source_chain[0] (Sol 便102 §4 の変異そのもの)",
                fixture_i, must_contain="XOR violation (missing-both)")

    def fixture_j():
        cert = deepcopy(real_v5)
        chain = cert["conventions_used"]["effective_source_chain"]
        tgt = [e for e in chain if "superseded_by" in e and "sha256" in e["superseded_by"]]
        assert tgt, "fixture premise broken"
        del tgt[0]["superseded_by"]["sha256"]
        run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_stop("N-j ★: missing-both on a nested superseded_by",
                fixture_j, must_contain="XOR violation (missing-both)")

    def fixture_k():
        cert = deepcopy(real_v5)
        del cert["conventions_used"]["effective_source"]["sha256_ref"]
        run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_stop("N-k ★: missing-both on conventions_used.effective_source",
                fixture_k, must_contain="XOR violation (missing-both)")

    def fixture_l():
        cert = deepcopy(real_v5)
        del cert["supersedes"]["sha256"]
        run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_stop("N-l ★: missing-both on top-level supersedes",
                fixture_l, must_contain="XOR violation (missing-both)")

    def fixture_m():
        cert = deepcopy(real_v5)
        del cert["supplements_cert"]
        run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_stop("N-m ★: a digest-required top-level pin deleted wholesale",
                fixture_m, must_contain="schema requires top-level")

    # === ★ NEW in v3: (x) plain sha256 bytes verification ==================
    def fixture_n():
        cert = deepcopy(real_v5)
        # well-formed 64-hex but wrong value: v2 would have accepted it.
        cert["conventions_used"]["effective_source_chain"][0]["sha256"] = "a" * 64
        run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_stop("N-n ★: plain sha256 is valid 64-hex but does not match target bytes",
                fixture_n, must_contain="(x)")

    # === ★ NEW in v3: (xi) ledger pin binding =============================
    def fixture_o():
        cert = deepcopy(real_v5)
        cert["ledger_artifact_pin"]["declared_version"] = "conventions_ledger_v1_7"
        run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_stop("N-o ★: ledger_artifact_pin.declared_version != conventions_used.ledger_version",
                fixture_o, must_contain="(xi)")

    def fixture_p():
        cert = deepcopy(real_v5)
        cert["ledger_artifact_pin"]["sha256"] = "b" * 64
        run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_stop("N-p ★: ledger artifact digest does not match the live ledger bytes",
                fixture_p, must_contain="(x)")

    # === 非発火側の縁(鉄則2: 述語の両縁を張る)============================
    # 「digest 位置でない欄が欠けても missing-both は発火しない」ことを示す。
    # これがないと『何を消しても止まる』過剰発火と区別できない。
    def nonfire_1():
        cert = deepcopy(real_v5)
        chain = cert["conventions_used"]["effective_source_chain"]
        tgt = [e for e in chain if "scope" in e]
        assert tgt, "fixture premise broken"
        del tgt[0]["scope"]          # optional prose field, NOT a digest position
        return run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_pass("P2 non-firing edge: deleting a non-digest optional field ('scope') does NOT fire missing-both",
                nonfire_1)

    def nonfire_2():
        cert = deepcopy(real_v5)
        # an entry legitimately carrying ONLY sha256 must not fire; and one
        # carrying ONLY sha256_ref must not fire.  Assert both shapes exist in
        # the real cert, then re-run.
        chain = cert["conventions_used"]["effective_source_chain"]
        assert any("sha256" in e and "sha256_ref" not in e for e in chain)
        assert any("sha256_ref" in e and "sha256" not in e for e in chain)
        return run_checks_on_cert(V5_RELPATH, V5_PATH, cert)
    expect_pass("P3 non-firing edge: both legal one-sided shapes (sha256-only / sha256_ref-only) coexist and PASS",
                nonfire_2)

    # === ★ 便102 §4 の再現テスト: Sol が変異させた現物(v4)そのもの ========
    # checker v3 の必須位置列挙 + XOR 述語を、Sol が用いた v4 の変異体へ直接
    # 適用する。(v4 は ledger_version drift で先に止まるので、ここでは
    # 構造述語だけを単独で走らせ、Sol の変異が確かに捕捉されることを示す。)
    def reproduce_sol():
        cert = deepcopy(real_v4)
        e0 = cert["conventions_used"]["effective_source_chain"][0]
        assert "sha256" in e0, "premise broken: v4 chain[0] has no sha256"
        del e0["sha256"]
        # v4 は v5 schema の top-level pin を持たないので、構造列挙のうち
        # conventions_used 部分だけを直接適用する(検査の弱体化ではなく、
        # 過去 artifact に対する診断的適用)。
        cu = cert["conventions_used"]
        positions = []
        es = cu["effective_source"]
        positions.append(("conventions_used.effective_source", es))
        _collect_superseded_chain("conventions_used.effective_source", es, positions)
        for i, e in enumerate(cu["effective_source_chain"]):
            lbl = "conventions_used.effective_source_chain[%d]" % i
            positions.append((lbl, e))
            _collect_superseded_chain(lbl, e, positions)
        print("   [reproduction] v4 の必須 digest 位置 = %d(v2 の discovery walk は変異後 8 しか見なかった)" % len(positions))
        for lbl, obj in positions:
            check_xor(lbl, obj, required=True)
    expect_stop("REPRO ★ 便102 §4: v4 の effective_source_chain[0] から sha256 を除去 -> v3 の述語は STOP",
                reproduce_sol, must_contain="XOR violation (missing-both)")

    print("=" * 70)
    print("ALL SELFTEST CASES BEHAVED AS EXPECTED (%d PASS + %d STOP)" % (n_pass, n_stop))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        main_selftest()
    else:
        target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CERT
        try:
            report = run_checks(target)
            print(json.dumps(report, ensure_ascii=False, indent=2))
        except CheckStop as e:
            print("INTEGRITY_STOP / MALFORMED:", e)
            sys.exit(1)
