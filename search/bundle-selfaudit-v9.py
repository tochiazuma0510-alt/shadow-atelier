#!/usr/bin/env python3
# bundle-selfaudit-v9.py -- N_infty stage2 freeze bundle self-audit (16 checks + M70/M71/M72/M74 変異試験)
# usage: python search/bundle-selfaudit-v9.py [--mutate]   (exit 0 = ALL PASS)
# v9 (実装係・便95 W95-2.3 修理バンドル item 1・司令塔検問1 束縛条項(b)):
#   points at spec v19 / contract v14 / manifest v14. (Two corrections to
#   earlier drafts of this header, both recorded rather than absorbed:
#   (i) "manifest unchanged at v13" was wrong -- the manifest's own §0 header
#   ID-binds governing_spec, which v18->v19 made stale, and check #1's
#   version-token sweep is what detected it; (ii) "the manifest bump is a
#   PURE SYNC version" was then also wrong -- the 司令塔裁定 2026-08-01
#   added substantive clause Y-3a (registry receipt must pin the docs trio
#   digests). See manifest v14 §0.-0.5.)
#   ADDITIVE ONLY over v8: none of
#   v8's 15 checks or its M69-1..5/M70/M72-1/M74 mutation fixtures are
#   removed or weakened -- new check #16 verifies the [27] semantic-axis S2
#   band is stated as the SAME explicit set in both spec and contract (司令塔
#   検問1 束縛条項(a): 非連続集合は範囲記法でなく明示集合で書く、という要求
#   の機械照合).
#
# v8 (自動ループ 2 巡 / Sol 便 74 FAIL B74-1..4):
#   B74-1 canonicality を [branch-contract] から読む(build_step は順序保存列)
#   B74-2 check #4 を block 由来の期待と QD kind の実比較へ
#   B74-3 causal-use の正方向強制 + consumer 三集合 exact equality
#   B74-4 M72-1 が production consumer_buildface / projection を直接呼ぶ
#
# v4 (裁定 87 / Sol 便 69 FAIL B69-1..4 + F11):
#   B69-1: operative の定義を厳格化 -- 除外するのは明示型付き `> **[historical]**` blockquote と
#          [sweep-def]/[registry-definition]/[typed-registry]/authblock の fence だけ。
#          通常 blockquote と machine schema fence は operative として走査する。
#   B69-2: clause/check の regex を **文書の [registry-definition] block から読む**(checker 内に
#          手書きしない)。起動時にその block の自己 digest を表示する。
#   B69-3: alternation は長 token 先行(W-2′ を W-[0-9] の前)。fixture を固定。
#   B69-4: build_record_present の四象限 fixture を機械検査。
#   F11 : M69-1..5 の変異試験を内蔵(--mutate で実行)。
#
import os, re, sys, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {"spec":     "docs/week4-NInfty_stage2_spec_v19.md",
     "contract": "docs/mb_ninfty_verifier_contract_v14.md",
     "manifest": "docs/mb_dependency_manifest_v14.md"}
CUR = {"spec": "v19", "contract": "v14", "manifest": "v14"}
ORD = {"manifest": 0, "contract": 1, "spec": 2}
T = {k: open(os.path.join(D, p), encoding='utf-8').read() for k, p in F.items()}
Bb = {k: open(os.path.join(D, p), 'rb').read() for k, p in F.items()}
DG = {k: hashlib.sha256(v).hexdigest() for k, v in Bb.items()}
fails = []
def report(n, name, ok, detail):
    print(("PASS" if ok else "FAIL"), "|", n, name, "|", detail)
    if not ok: fails.append(n)

# ============ 文書から regex 正本を読む(B69-2 / F11 末尾) ============
def regblock(txt):
    m = re.search(r"\[registry-definition\](.*?)```", txt, re.S)
    return m.group(1) if m else None
def regexes(txt):
    b = regblock(txt)
    if b is None: return None, None, None
    cl = re.search(r"clause_id_regex = (.+)", b).group(1).strip()
    ck = re.search(r"check_id_regex  = (.+)", b).group(1).strip()
    dg = hashlib.sha256(b.encode()).hexdigest()
    return cl, ck, dg
CL_RE, CK_RE, REG_DG = regexes(T["contract"])
CL_RE_M, CK_RE_M, REG_DG_M = regexes(T["manifest"])
print("regex source = document [registry-definition] block")
print("  contract block digest =", REG_DG)
print("  manifest block digest =", REG_DG_M)
print("  clause_id_regex =", CL_RE)
print("  check_id_regex  =", CK_RE)
print()

# ============ 構造分類器(B69-1 で operative を厳格化) ============
EXCLUDED_FENCE = ("[sweep-def]", "sweep_definition", "[registry-definition]",
                  "[typed-registry]", "live_authority_refs[]", "historical_quotation_refs[]")
def classify(txt):
    cls = {}; lines = txt.split("\n"); fence = False; fkind = None; in_diff = False
    for i, l in enumerate(lines, 1):
        st = l.strip()
        if st.startswith("```"):
            if not fence:
                fence = True; fkind = "code"
                nxt = "\n".join(lines[i:i+3])
                if any(k in nxt for k in EXCLUDED_FENCE): fkind = "authblock"
            else:
                fence = False; fkind = None
            cls[i] = "fence-delim"; continue
        if fence:
            cls[i] = "supersedes" if st.startswith("supersedes") else fkind
            continue
        if re.match(r"^#{2,4} ", l):
            in_diff = bool(re.search(r"(差分|版履歴)", l)); cls[i] = "diffhead" if in_diff else "heading"; continue
        if st.startswith(">"):
            # 明示型付き historical blockquote だけを除外(B69-1)
            cls[i] = "hist-bq" if st.startswith("> **[historical]") else "blockquote"; continue
        if st.startswith("|"): cls[i] = "difftable" if in_diff else "table"; continue
        if st.startswith("supersedes"): cls[i] = "supersedes"; continue
        cls[i] = "prose"
    # blockquote の継続行(> なしの折返し)は直前クラスを継承
    return cls
OPERATIVE = {"prose", "table", "heading", "fence-delim", "blockquote", "code"}

# ===== [branch-contract] 由来の値(全 check が参照するので先に解決する)=====
def parse_branch_contract(txt):
    """[branch-contract] block を bracket-aware に parse する。
       list 要素に `foo[]` のような角括弧が入るので、非貪欲 regex では途中で切れる。"""
    # 行頭の [branch-contract] だけを block 開始とみなす(本文の言及に食いつかない)
    m = re.search(r"^\[branch-contract\][^\n]*\n(.*?)```", txt, re.S | re.M)
    if not m: return None
    b = m.group(1)
    def section(name):
        sm = re.search(r"\n\s*" + name + r"\s*:\s*\{", b)
        if not sm: return None
        k = sm.end(); depth = 1
        while k < len(b) and depth:
            if b[k] == "{": depth += 1
            elif b[k] == "}": depth -= 1
            k += 1
        return b[sm.end():k-1]
    def field(sec, name):
        if sec is None: return []
        fm = re.search(name + r"\s*=\s*\[", sec)
        if not fm: return []
        k = fm.end(); depth = 1; start = k
        while k < len(sec) and depth:
            if sec[k] == "[": depth += 1
            elif sec[k] == "]":
                depth -= 1
                if depth == 0: break
            k += 1
        body = sec[start:k]
        return [x.strip() for x in body.replace(chr(10), " ").split(",") if x.strip()]
    st, sf = section("true"), section("false")
    if st is None or sf is None: return None
    def scalar(sec, name):
        if sec is None: return None
        mm = re.search(name + r"\s*=\s*([A-Za-z_][A-Za-z0-9_\-]*)", sec)
        return mm.group(1) if mm else None
    def canon(b):
        cm = re.search(r"canonicality\s*=\s*\{(.*?)\n\}", b, re.S)
        out = {}
        if cm:
            for line in cm.group(1).split(chr(10)):
                mm = re.match(r"\s*([A-Za-z_]+\[\])\s*:\s*([a-z\-]+)", line)
                if mm: out[mm.group(1)] = mm.group(2)
        return out
    def consumers(b):
        cm = re.search(r"^# consumer = \{(.*?)\}", b, re.M)
        return [] if not cm else [x.strip() for x in cm.group(1).split(",") if x.strip()]
    CANON = canon(b); CONSUMER_LITERAL = consumers(b)
    return {"canonicality": CANON, "consumer_literal": CONSUMER_LITERAL,
            "true":  {"required": field(st, "required_keys"), "recompute": field(st, "recompute"),
                      "forbidden": [], "closure_policy": scalar(st, "closure_policy")},
            "false": {"required": field(sf, "required_keys"), "forbidden": field(sf, "forbidden_keys"),
                      "recompute": field(sf, "recompute"), "closure_policy": scalar(sf, "closure_policy")}}

BC = parse_branch_contract(T["manifest"])
HEX = re.compile(r"^[0-9a-f]{64}$")

# --- 判定リストは [branch-contract] block から導出する(hardcode しない) ---
# BASE  = false.required_keys - {build_record_present}   (= 全 record で必須の provenance 欄)
# FOUR  = false.forbidden_keys                            (= true でのみ必須の build 欄)
def derive_keysets(bc):
    if bc is None: return None, None, None
    base = [k for k in bc["false"]["required"] if k != "build_record_present"]
    four = list(bc["false"]["forbidden"])
    rec  = {"true": list(bc["true"]["recompute"]), "false": list(bc["false"]["recompute"])}
    return base, four, rec
def derive_policy(bc):
    return None if bc is None else {"true": bc["true"]["closure_policy"], "false": bc["false"]["closure_policy"]}
BASE, FOUR, RECOMPUTE = derive_keysets(BC)
CANON = (BC or {}).get("canonicality", {})
CONSUMER_LITERAL = (BC or {}).get("consumer_literal", [])

def parse_bc_use_map(txt):
    """[bc-use-map] block を読む(F12.1: reference/causal-use gate の正本)"""
    m = re.search(r"^\[bc-use-map\][^\n]*\n(.*?)```", txt, re.S | re.M)
    if not m: return None
    out = {}
    for line in m.group(1).split(chr(10)):
        mm = re.match(r"\s*([A-Za-z0-9\-_\u2032\u2033\u2034\u2057]+)\s*:\s*\[(.*?)\]", line)
        if mm: out[mm.group(1)] = [x.strip() for x in mm.group(2).split(",") if x.strip()]
    return out or None
POLICY = derive_policy(BC)
BC_USE = parse_bc_use_map(T["manifest"])

# ===== branch evaluator(check 4 / 14 / 15 と変異 lane が共有する)=====
def _has(rec, k): return k.replace("[]", "") in rec
def _get(rec, k): return rec.get(k.replace("[]", ""))
def _valid_hex(v):  return isinstance(v, str) and bool(HEX.match(v))
def _valid_list(v): return isinstance(v, list)
def validate_branch(rec):
    """全 consumer が最初に適用する共有ゲート([branch-contract] が唯一正本)。
       BC-1: consumer は独自の分岐記述を持たず、この関数だけを分岐判断に使う。"""
    # B71-5: typed branch domain -- schema validity を両分岐で先に確定する
    if "build_record_present" not in rec: return "[12]"
    if not isinstance(rec["build_record_present"], bool): return "[12]"      # non-boolean
    for k in BASE:
        if not _has(rec, k): return "[11]"
        v = _get(rec, k)
        if v is None: return "[12]"                                          # null 不可
        if k.endswith("[]"):
            if not _valid_list(v): return "[12]"                             # list 型
            # B72-4/B74-1: 要素は非 null の 64-hex。順序/重複の扱いは
            # [branch-contract] の canonicality 宣言に従う(hardcode しない)。
            for e in v:
                if e is None or not _valid_hex(e): return "[12]"
            if CANON.get(k) == "sorted-dedup-set" and list(v) != sorted(set(v)): return "[12]"
        elif k == "toolchain_digest":
            if not _valid_hex(v): return "[12]"                              # 64-hex
    if rec["build_record_present"] is True:
        v = _get(rec, "pinned_input_digests[]")
        if not _valid_list(v): return "[12]"
        for e in v:
            if e is None or not _valid_hex(e): return "[12]"                 # B72-4 要素レベル
        if CANON.get("pinned_input_digests[]") == "sorted-dedup-set" and list(v) != sorted(set(v)):
            return "[12]"
    if rec["build_record_present"] is True:
        for k in FOUR:
            if not _has(rec, k): return "[12]"
            v = _get(rec, k)
            if k.endswith("[]"):
                if not isinstance(v, list): return "[12]"
            elif not (isinstance(v, str) and HEX.match(v)): return "[12]"
        return "PASS"
    for k in FOUR:
        if _has(rec, k): return "[12]"      # QD-4: forbidden key present
    return "PASS"

def consumer_DR2(rec):
    """D-R2⁗: D-1/D-2 は全 record・D-3/D-4′ は present=true のみ"""
    g = validate_branch(rec)
    if g != "PASS": return g
    for k in BASE:
        if not _has(rec, k): return "[11]"
    # recompute リスト(BC 由来)に D-3/D-4′ が含まれる分岐だけ build 欄を検査する
    want = RECOMPUTE["true" if rec.get("build_record_present") is True else "false"]
    if any(x.startswith("D-3") or x.startswith("D-4") for x in want):
        for k in FOUR:
            if not _has(rec, k): return "[12]"
    return "PASS"
def consumer_I0c(rec):
    """I-0c″(4): present=true/top-level のみ binding 欠落 [12]・false は ABSENT が唯一の PASS"""
    g = validate_branch(rec)
    if g != "PASS": return g
    if "build_record_present" not in rec: return "[12]"
    # recompute に D-4′ が含まれる分岐でだけ subject binding を要求する(BC 由来)
    want = RECOMPUTE["true" if rec.get("build_record_present") is True else "false"]
    if any(x.startswith("D-4") for x in want):
        if not _has(rec, "subject_build_binding_digest"): return "[12]"
        v = _get(rec, "subject_build_binding_digest")
        return "PASS" if isinstance(v, str) and HEX.match(v) else "[12]"
    for k in FOUR:
        if _has(rec, k): return "[12]"
    return "PASS"
def build_face_projection(rec):
    """production の build-face 射影(B74-4: 試験はこの関数を直接呼ぶ)。
       [branch-contract] の forbidden/required に従い、false leaf でも
       申告済み toolchain / build step は射影に残す。"""
    proj = set()
    if _has(rec, "toolchain_digest"): proj.add(_get(rec, "toolchain_digest"))
    proj |= set(_get(rec, "build_step_digests[]") or [])
    if rec.get("build_record_present") is True:
        if _has(rec, "build_definition_blob_digest"): proj.add(_get(rec, "build_definition_blob_digest"))
        proj |= set(_get(rec, "pinned_input_digests[]") or [])
    return proj
def i3d_decision(projA, projB, tcb):
    """I-3d: build face 交差から TCB を差し引いて [11] か PASS を返す"""
    return "[11]" if ((projA & projB) - set(tcb)) else "PASS"
def consumer_buildface(rec):
    """build_artifact_set 射影: false の forbidden_keys は要素にしない・ABSENT は非混入"""
    g = validate_branch(rec)
    if g != "PASS": return g
    if rec.get("build_record_present") is True:
        if not _has(rec, "build_definition_blob_digest"): return "[12]"
    else:
        for k in FOUR:
            if _has(rec, k): return "[12]"
    proj = build_face_projection(rec)
    if any(x in (None, "", 0) for x in proj): return "[12]"
    return "PASS"
def consumer_R6(rec, policy=None):
    """R-6/H-1a″: closure_policy が bootstrap_leaf のときだけ再帰昇格を免除する。
       policy は [branch-contract] 由来(B72-3: hardcode しない)。"""
    g = validate_branch(rec)
    if g != "PASS": return g
    if not _has(rec, "toolchain_digest"): return "[11]"
    pol = (policy or POLICY or {}).get("false")
    if rec.get("build_record_present") is True:
        return "PASS" if _has(rec, "build_definition_blob_digest") else "[12]"
    # false 側の policy が bootstrap_leaf でなければ再帰昇格が要求され、leaf は不備になる
    return "PASS" if pol == "bootstrap_leaf" else "[11]"
def consumer_I0(rec):
    """I-0″: required_keys の存在と recompute リストに従う再計算(D-3/D-4′ は true のみ)"""
    g = validate_branch(rec)
    if g != "PASS": return g
    want = RECOMPUTE["true" if rec.get("build_record_present") is True else "false"]
    need = list(BASE)
    if any(x.startswith("D-3") or x.startswith("D-4") for x in want): need = need + list(FOUR)
    for k in need:
        if not _has(rec, k): return "[12]"
    return "PASS"
def consumer_H1a(rec, policy=None):
    """H-1a″: fixpoint 再計算。closure_policy が bootstrap_leaf のときだけ leaf を許す"""
    g = validate_branch(rec)
    if g != "PASS": return g
    pol = (policy or POLICY or {}).get("false")
    if rec.get("build_record_present") is True: return "PASS"
    return "PASS" if pol == "bootstrap_leaf" else "[12]"
def consumer_C6(rec):
    """contract C-6⁗: required_keys 提出 + forbidden_keys の ABSENT + recompute に従う再計算"""
    g = validate_branch(rec)
    if g != "PASS": return g
    br = "true" if rec.get("build_record_present") is True else "false"
    for k in (BC[br]["required"] if BC else []):
        if not _has(rec, k): return "[12]"
    for k in (BC["false"]["forbidden"] if (BC and br == "false") else []):
        if _has(rec, k): return "[12]"
    want = RECOMPUTE[br]
    if any(x.startswith("D-3") or x.startswith("D-4") for x in want):
        for k in FOUR:
            if not _has(rec, k): return "[12]"
    return "PASS"
CONSUMERS = [("D-R2" + chr(0x2057), consumer_DR2), ("I-0" + chr(0x2033), consumer_I0),
             ("I-0c" + chr(0x2033), consumer_I0c), ("build_artifact_set", consumer_buildface),
             ("R-6", consumer_R6), ("H-1a" + chr(0x2033), consumer_H1a),
             ("C-6" + chr(0x2057), consumer_C6)]

# ---------- 1. version-token sweep ----------
PAT = [("spec", r"mb/ninfty-stage2-predicate/v(\d+)"), ("spec", r"spec v(\d+)"),
       ("contract", r"mb/ninfty-verifier-contract/v(\d+)"), ("contract", r"contract v(\d+)"),
       ("manifest", r"mb/dependency-manifest/v(\d+)"), ("manifest", r"manifest v(\d+)"),
       (None, r"【v(\d+)[^】]*】"),
       (None, r"(?<!spec )(?<!contract )(?<!manifest )\bv(\d+) (?:で|から|は|新設|更新|訂正|修正)")]
def sweep(Tx):
    out = []
    for name, txt in Tx.items():
        cls = classify(txt)
        for i, l in enumerate(txt.split("\n"), 1):
            if cls.get(i) not in OPERATIVE: continue
            def _mask(mm):
                span = mm.group(0)
                v = int(re.search(r"chg v(\d+)", span).group(1))
                if "mb/" in span: return span
                if v > int(CUR[name][1:]) - 1: return span
                return ""
            masked = re.sub(r"【chg v\d+[^】]*】", _mask, l)
            for series, pat in PAT:
                for m in re.finditer(pat, masked):
                    tgt = series if series else name
                    if "v" + m.group(1) == CUR.get(tgt): continue
                    out.append((name, i, cls[i], tgt, "v" + m.group(1), l.strip()[:60]))
    return out
stale = sweep(T)
report(1, "version-token sweep (operative = 通常 blockquote と schema fence を含む)", len(stale) == 0,
       "除外域 = 明示型 `> **[historical]**` bq / [sweep-def]・[registry-definition]・[typed-registry]・authblock fence / 差分表 / supersedes"
       " / LIVE-STALE=%d" % len(stale))
for s_ in stale[:10]: print("      ", s_)

# ---------- 2/3. registry 集合等式(文書 regex + scope 限定) ----------
def extract_clauses(txt, cl_re):
    cls = classify(txt)
    return set(m.group(1) for i, l in enumerate(txt.split("\n"), 1) if cls.get(i) == "table"
               for m in [re.match(cl_re, l)] if m)
META_FENCE = ("covered_clauses", "covered_procedure_checks", "uncovered_checks",
              "uncovered_clauses", "[registry-definition]", "[branch-contract]",
              "conformance_record")
def _fence_spans(txt):
    """(start,end,header) の list。header はフェンス直後 3 行。"""
    lines = txt.split("\n"); out = []; st = None
    for i, l in enumerate(lines, 1):
        if l.strip().startswith("```"):
            if st is None: st = i
            else: out.append((st, i, "\n".join(lines[st:st+4]))); st = None
    return out
OWN = {"manifest": ("D-", "R-", "U-"), "contract": ("P-", "W-", "S1", "S2", "S3", "C1")}
def own_filter(name, ids):
    """CR-8b(per-document scope): その文書に normative 定義がある check だけを残す。
       相互の義務は clause 散文(contract C-6⁗ 等)で表現する。"""
    pre = OWN.get(name)
    if not pre: return set(ids)
    return set(x for x in ids if x.startswith(pre))
def _tagged_table_rows(txt):
    """[normative-check-table] marker 直後の table 区間だけを返す(F12.3: 構造推測の廃止)"""
    lines = txt.split(chr(10)); out = set(); i = 0
    while i < len(lines):
        if lines[i].strip() == "[normative-check-table]":
            j = i + 1
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                out.add(j + 1); j += 1
            i = j
        else: i += 1
    return out
def extract_checks(txt, ck_re):
    """CR-8: defined_procedure_checks は明示タグ block と normative table 行だけから抽出。
       covered/uncovered/registry-definition/branch-contract/conformance の meta fence は母体から除く。"""
    cls = classify(txt); lines = txt.split("\n")
    banned = set()
    for a, b, head in _fence_spans(txt):
        if any(k in head for k in META_FENCE) or "[normative-check-block]" not in head:
            for k in range(a, b + 1): banned.add(k)
    tagged_fence = set()
    for x, y, head in _fence_spans(txt):
        if "[normative-check-block]" in head and not any(k in head for k in META_FENCE):
            for k in range(x, y + 1): tagged_fence.add(k)
    corpus = (tagged_fence | _tagged_table_rows(txt)) - banned
    out = set()
    for i, l in enumerate(lines, 1):
        if i in corpus:
            for m in re.finditer(ck_re, l): out.add(m.group(1))
    return out
def setof(txt, key):
    m = re.search(key + r" = \[(.*?)\]", txt, re.S)
    return None if not m else set(x.strip() for x in m.group(1).replace(chr(10), " ").split(",") if x.strip())
ok2 = True; ok3 = True; d2 = []; d3 = []
for name, cl, ck in (("contract", CL_RE, CK_RE), ("manifest", CL_RE_M, CK_RE_M)):
    txt = T[name]
    reg = extract_clauses(txt, cl); cov = setof(txt, "covered_clauses") or set(); unc = setof(txt, "uncovered_clauses") or set()
    good = (not [c for c in cov | unc if ".." in c]) and (cov & unc == set()) and (cov | unc == reg)
    d2.append("%s: reg=%d cov=%d eq=%s" % (name, len(reg), len(cov), good))
    if not good: ok2 = False; d2.append("  reg-cov=%s cov-reg=%s" % (sorted(reg - cov)[:8], sorted(cov - reg)[:8]))
    creg = own_filter(name, extract_checks(txt, ck)); ccov = setof(txt, "covered_procedure_checks") or set(); cunc = setof(txt, "uncovered_checks") or set()
    cgood = (ccov & cunc == set()) and (ccov | cunc == creg)
    d3.append("%s: reg=%d cov=%d eq=%s" % (name, len(creg), len(ccov), cgood))
    if not cgood: ok3 = False; d3.append("  reg-cov=%s cov-reg=%s" % (sorted(creg - ccov)[:8], sorted(ccov - creg)[:8]))
report(2, "clause registry 集合等式(文書 regex)", ok2, " ; ".join(d2))
BADPRIME = (chr(0x27), chr(0x2019), chr(0xB4), chr(0x2035))
tokbad = [(k, i, l.strip()[:40]) for k in F for i, l in enumerate(T[k].split(chr(10)), 1)
          for bp in BADPRIME if ("W-2" + bp) in l]
if tokbad: ok3 = False
report(3, "check registry 集合等式 + W-2′ token 一貫性(U+2032 exact)", ok3,
       " ; ".join(d3) + " ; 非 U+2032 prime の W-2 変種=%d %s" % (len(tokbad), tokbad[:3]))

# ---------- 4. block <-> QD 表 semantic equality (B72-1 / B74-2) ----------
mt = T["manifest"]
def parse_qd_table(txt):
    rows = {}
    for m in re.finditer(r"^\| \*\*(QD-[1-4])\*\* \| `(true|false)` \| (.*?) \| (.*?) \|$", txt, re.M):
        qid, pres, fields, exp = m.group(1), m.group(2), m.group(3), m.group(4)
        kind = ("complete" if "complete" in fields else
                "missing" if "missing" in fields else
                "canonical" if "canonical" in fields else
                "nonempty" if "nonempty" in fields else "?")
        rows[qid] = {"present": pres == "true", "kind": kind,
                     "verdict": "[12]" if "[12]" in exp else "PASS",
                     "exempt_D34": ("免除" in exp),
                     "recompute_D34": ("D-3" in exp and "D-4" in exp and "免除" not in exp),
                     "mentions_schema": ("schema-valid" in fields or "schema-invalid" in fields)}
    return rows
QD = parse_qd_table(mt)

def synth_record(present, kind):
    """block の required/forbidden/canonicality から、その kind の代表 record を合成する。
       期待 verdict は hardcode せず、production validator を実際に走らせて得る。"""
    HX = "a" * 64
    r = {"build_record_present": present}
    for k in BASE:
        r[k.replace("[]", "")] = [HX] if k.endswith("[]") else HX
    if present:
        for k in FOUR:
            r[k.replace("[]", "")] = [] if k.endswith("[]") else HX
    if kind == "missing" and present:
        r.pop(FOUR[0].replace("[]", ""), None)          # required の 1 欄を落とす
    if kind == "nonempty" and not present:
        r[FOUR[2].replace("[]", "")] = ""               # forbidden を空文字で置く
    return r
KIND_OF = {"QD-1": (True, "complete"), "QD-2": (True, "missing"),
           "QD-3": (False, "canonical"), "QD-4": (False, "nonempty")}
ok4 = (BC is not None and len(QD) == 4); d4 = []
if ok4:
    blk_D34 = {True: any(x.startswith(("D-3", "D-4")) for x in RECOMPUTE["true"]),
               False: any(x.startswith(("D-3", "D-4")) for x in RECOMPUTE["false"])}
    for qid, (pres, kind) in KIND_OF.items():
        r = QD.get(qid)
        if r is None: ok4 = False; d4.append("%s 行が無い" % qid); continue
        # (a) kind を実比較(B74-2: 捨てない)
        if r["kind"] != kind:
            ok4 = False; d4.append("%s: kind=%s(block 由来の期待 %s)" % (qid, r["kind"], kind))
        # (b) verdict は production validator を走らせて導く(hardcode なし)
        want_verdict = validate_branch(synth_record(pres, kind))
        if r["present"] != pres or r["verdict"] != want_verdict:
            ok4 = False
            d4.append("%s: 表(present=%s verdict=%s) / validator 由来(present=%s verdict=%s)"
                      % (qid, r["present"], r["verdict"], pres, want_verdict))
        # (c) D-3/D-4′ の再計算 or 免除
        if want_verdict == "PASS":
            wd = blk_D34[pres]
            if not (r["recompute_D34"] == wd or (not wd and r["exempt_D34"])):
                ok4 = False; d4.append("%s: D34 描画が block と不一致(期待 %s)" % (qid, wd))
        # (d) schema validity が描画に反映されているか(便 74 F5.2)
        if kind in ("missing", "canonical") and not r["mentions_schema"]:
            ok4 = False; d4.append("%s: schema validity が描画に無い" % qid)
    selfclaim = [i for i, l in enumerate(mt.split(chr(10)), 1)
                 if ("四象限" in l or "本表" in l) and "正本" in l and "rendered-nonnormative" not in l
                 and "[branch-contract]" not in l and not l.lstrip().startswith(">")]
    if selfclaim: ok4 = False; d4.append("表が正本を自称する行 %s" % selfclaim)
report(4, "block <-> QD 表 semantic equality (B74-2)", ok4,
       "QD 行 %d / kind 実比較 + validator 由来 verdict / %s" % (len(QD), "; ".join(d4) if d4 else "不一致なし"))

# ---------- 5. certificate 未定義欄 ----------
st = T["spec"]
cert = re.search(r"divisor_equality_certificate = \{.*?\n\}", st, re.S).group(0)
report(5, "certificate schema の未定義欄", "verifier_evidence" not in cert, "cert block 内 verifier_evidence=%s" % ("verifier_evidence" in cert))

# ---------- 6. anchor ----------
ok6 = True; ng = []
for m in re.finditer(r'schema_id\(\s*([\w\-]+)\s*\)\s*=\s*(\w+)\s*\+\s*"#([\w\-]+)"', st):
    nm, owner, anc = m.group(1), m.group(2), m.group(3)
    tgt = {"predicate_spec_id": "spec", "verifier_contract_id": "contract", "dependency_manifest_schema_id": "manifest"}.get(owner)
    ex = ("{#" + anc + "}") in T.get(tgt, "")
    bm = re.search(r"bound_blob_digest\(\s*" + re.escape(nm) + r"\s*\)\s*=\s*(\w+)", st)
    bound = bm.group(1) if bm else "(grouped)"
    exp = {"spec": "predicate_spec_digest", "contract": "verifier_contract_digest", "manifest": "dependency_manifest_schema_digest"}[tgt]
    if not (ex and (bound == exp or (bound == "(grouped)" and tgt == "spec"))): ok6 = False; ng.append(nm)
report(6, "anchor 実在 + binding 方向", ok6, "NG=%s" % (ng if ng else 0))

# ---------- 7. pin topology ----------
t7 = (DG["contract"] in st and DG["manifest"] in st and DG["manifest"] in T["contract"]
      and DG["spec"] not in T["contract"] and DG["spec"] not in T["manifest"] and DG["contract"] not in T["manifest"])
gov = all(('"mb/ninfty-stage2-predicate/' + CUR["spec"] + '"' in T[k] and "receipt が記入" in T[k]) for k in ("contract", "manifest"))
report(7, "pin topology (manifest->contract->spec)", t7 and gov, "one-way=%s governing=%s" % (t7, gov))

# ---------- 8. byte hygiene ----------
ok8 = True; r8 = []
for k in F:
    raw = Bb[k]; t = T[k]; L = t.split("\n")
    c0 = sum(1 for l in L for ch in l if ord(ch) < 32)
    odd = len([i for i, l in enumerate(L, 1) if l.count("$") % 2 == 1])
    ast = len([i for i, l in enumerate(L, 1) if l.startswith("| **") and l.count("**") % 2 == 1])
    r8.append("%s LF=%d CR=%d TAB=%d C0=%d odd$=%d 未閉鎖**=%d" % (k, raw.count(b"\n"), raw.count(b"\r"), t.count(chr(9)), c0, odd, ast))
    if raw.count(b"\r") + t.count(chr(9)) + c0 + odd + ast: ok8 = False
report(8, "byte hygiene + Markdown 閉じ", ok8, " ; ".join(r8))

# ---------- 9. lifecycle ----------
ok9 = all(("embedded_state_at_candidate_creation" in T[k] and "live_status_authority" in T[k]) for k in ("contract", "manifest"))
gate = "exact_freeze_bundle" in st and "mb/ninfty-stage2-predicate/" + CUR["spec"] in st
report(9, "lifecycle tense", ok9 and gate, "embedded/authority=%s gate(%s)=%s" % (ok9, CUR["spec"], gate))

# ---------- 10. TCB arity ----------
decl = len(set(re.findall(r"^allowed_shared_\w+\[\]", mt, re.M)))
init = len(re.findall(r"^allowed_shared_\w+\s*=\s*\[\]", mt, re.M))
cm = classify(mt); cc = classify(T["contract"])
w = [x for i, l in enumerate(mt.split("\n"), 1) if cm.get(i) in ("table", "prose") for x in re.findall(r"(五欄|四欄|三欄)", l)]
wc = [x for i, l in enumerate(T["contract"].split("\n"), 1) if cc.get(i) in ("table", "prose") for x in re.findall(r"(五欄|四欄|三欄)", l)]
report(10, "TCB arity", decl == 4 and init == 4 and set(w) <= {"四欄"} and set(wc) <= {"四欄"},
       "宣言=%d 初期値=%d m=%s c=%s" % (decl, init, sorted(set(w)), sorted(set(wc))))

# ---------- 11. invariant ----------
old = [l for l in st.split("\n") if "public は primary_reason_code のみを出す" in l and "canonical_sort" not in l and "更新" not in l and not l.startswith("| ")]
report(11, "invariant 矛盾", len(old) == 0 and "canonical_sort( ({[26]}" in st, "旧文 live=%d" % len(old))

# ---------- 12. cross-doc clause-ID 同期 ----------
MALL = extract_clauses(T["manifest"], CL_RE_M) | extract_checks(T["manifest"], CK_RE_M)
CALL = extract_clauses(T["contract"], CL_RE) | extract_checks(T["contract"], CK_RE)
XREF = r"(?<![A-Za-z0-9])((?:D-R|D-|I-0c|I-0|I-|SB-|QD-|E-|R-|H-|M-|FA-|BA-|Y-|U-|T-|CR-|LA-)[A-Za-z0-9\-\.]*[′″‴⁗]?)(?![A-Za-z0-9])"
cc2 = classify(T["contract"]); refs = set(); inside = False
for i, l in enumerate(T["contract"].split("\n"), 1):
    if l.startswith("## 7."): inside = True
    elif l.startswith("## ") and inside: inside = False
    if inside and cc2.get(i) in ("table", "prose", "heading"):
        for m in re.finditer(XREF, l):
            if not m.group(1).startswith("C-"): refs.add(m.group(1))
missing = sorted(x for x in refs if x not in MALL and x not in CALL)
report(12, "cross-doc clause-ID 同期", not missing, "§7 参照=%d / manifest registry=%d / 不在=%s" % (len(refs), len(MALL), missing if missing else "なし"))

# ---------- 13. authblock label<->digest + sweep-def ----------
SLUG = {"mb/ninfty-stage2-predicate": "spec", "mb/ninfty-verifier-contract": "contract", "mb/dependency-manifest": "manifest"}
ok13 = True; r13 = []
for name in F:
    blk = re.search(r"live_authority_refs\[\] = \[(.*?)\n\]", T[name], re.S)
    if not blk: ok13 = False; r13.append("%s: block なし" % name); continue
    for e in re.finditer(r'artifact_id: "([^"]+)/(v\d+)",\s*\n\s*digest_or_receipt_slot: "([^"]+)"', blk.group(1)):
        slug, ver, dg = e.group(1), e.group(2), e.group(3)
        tgt = SLUG.get(slug)
        dok = (tgt == name or ORD[tgt] > ORD[name]) if dg.startswith("receipt:") else (dg == DG[tgt])
        if not (ver == CUR[tgt] and dok): ok13 = False; r13.append("%s->%s label=%s dok=%s" % (name, tgt, ver, dok))
    hb = re.search(r"historical_quotation_refs\[\] = \[(.*?)\n\]", T[name], re.S)
    if hb:
        for e in re.finditer(r'artifact_id: "([^"]+)/v(\d+)\.\.v(\d+)"', hb.group(1)):
            slug, lo, hi = e.group(1), int(e.group(2)), int(e.group(3))
            tgt = SLUG.get(slug)
            top = int(CUR[tgt][1:]) - (1 if tgt == name else 0)
            if not (lo >= 1 and hi <= int(CUR[tgt][1:]) and hi >= lo):
                ok13 = False; r13.append("%s historical %s v%d..v%d 範囲不正" % (name, tgt, lo, hi))
        if re.search(r'historical_quotation_refs.*?artifact_id: "[^"]+/v\d+", digest', hb.group(0), re.S):
            ok13 = False; r13.append("%s: historical に単一版 label + digest(誤記型)" % name)
    sd = re.search(r'current_version\s*=\s*"v(\d+)".*?historical_upper_bound\s*=\s*"v(\d+)"', T[name], re.S)
    if not sd or int(sd.group(2)) != int(sd.group(1)) - 1 or "v" + sd.group(1) != CUR[name]:
        ok13 = False; r13.append("%s: sweep-def 版不整合" % name)
report(13, "authblock label<->digest + sweep-def 上限", ok13, "NG=%s" % (r13 if r13 else 0))

# ---------- 14. branch evaluator + consumer matrix (B70-1 / B70-4) ----------
# block 自身の内部整合(true.required = base + four + present)
BC_SELF_OK = (BC is not None and
              set(BC["true"]["required"]) == set(BASE) | set(FOUR) | {"build_record_present"})
# fidelity gate: 導出値が空/欠損なら checker 自身を FAIL させる
BC_FIDELITY = (BC is not None and len(BASE) == 3 and len(FOUR) == 4 and BC_SELF_OK
               and RECOMPUTE["true"] and RECOMPUTE["false"]
               and len(RECOMPUTE["true"]) == 4 and len(RECOMPUTE["false"]) == 2)

H = "a" * 64
SRC = "c" * 64
REC = {
 "QD-1 true/complete": ({"build_record_present": True, "source_artifact_digests": [SRC], "toolchain_digest": H,
                          "build_step_digests": [H], "build_definition_blob_digest": H,
                          "pinned_input_digests": [], "build_root_id": H, "subject_build_binding_digest": H}, "PASS"),
 "QD-2 true/missing":  ({"build_record_present": True, "source_artifact_digests": [SRC], "toolchain_digest": H,
                          "build_step_digests": [H], "build_definition_blob_digest": H,
                          "pinned_input_digests": [], "build_root_id": H}, "[12]"),
 "QD-3 false/canon":   ({"build_record_present": False, "source_artifact_digests": [SRC], "toolchain_digest": H,
                          "build_step_digests": [H]}, "PASS"),
 "QD-4 false/nonempty":({"build_record_present": False, "source_artifact_digests": [SRC], "toolchain_digest": H,
                          "build_step_digests": [H], "build_root_id": ""}, "[12]"),
}
ok14 = BC is not None and BC_FIDELITY; rows14 = []
if not BC_FIDELITY:
    rows14.append("BC fidelity gate FAIL: BASE=%s FOUR=%s RECOMPUTE=%s self_ok=%s"
                  % (BASE, FOUR, RECOMPUTE, BC_SELF_OK))
for label, (rec, exp) in REC.items():
    verdicts = {n: f(rec) for n, f in CONSUMERS}
    same = len(set(verdicts.values())) == 1
    match = same and list(verdicts.values())[0] == exp
    rows14.append("%s -> %s (期待 %s, 一致 %s)" % (label, verdicts, exp, same))
    if not match: ok14 = False
report(14, "branch evaluator + consumer matrix equality (B70-1/4)", ok14,
       "[branch-contract] parsed=%s fidelity=%s / BASE(%d)=%s / FOUR(%d)=%s / recompute=%s / %s"
       % (BC is not None, BC_FIDELITY, len(BASE or []), BASE, len(FOUR or []), FOUR, RECOMPUTE, " ; ".join(rows14)))

# ================= M70 変異試験 =================
mutation_fails = []
def mreport(name, ok, detail):
    print(("PASS" if ok else "FAIL"), "|", name, "|", detail)
    if not ok: mutation_fails.append(name)

if "--mutate" in sys.argv:
    print("\n--- M70/M71 変異試験(fail-closed・実 record 評価)---")
    ct = T["contract"]
    # M70-1 covered へ未知 W-9 -> extra-covered FAIL
    t1 = ct.replace("covered_procedure_checks = [", "covered_procedure_checks = [W-9, ", 1)
    d1 = own_filter("contract", extract_checks(t1, CK_RE)); c1 = setof(t1, "covered_procedure_checks")
    mreport("M70-1", ("W-9" in c1 and "W-9" not in d1),
          "covered に W-9=%s / defined に W-9=%s(定義母体に混入しない)" % ("W-9" in c1, "W-9" in d1))
    # M70-2 normative W-2′ 定義削除・covered 維持 -> undefined-covered FAIL
    def _corpus_lines(txt):
        """defined の抽出母体になる行番号(タグ付き block + normative table)"""
        cls = classify(txt); banned = set()
        for x, y, head in _fence_spans(txt):
            if any(k in head for k in META_FENCE) or "[normative-check-block]" not in head:
                for k in range(x, y + 1): banned.add(k)
        return [i for i in range(1, len(txt.split(chr(10))) + 1)
                if i not in banned and cls.get(i) in ("table", "prose", "code", "blockquote")]
    lines = ct.split(chr(10)); corpus = set(_corpus_lines(ct))
    L2 = list(lines)
    for i in corpus:
        L2[i-1] = L2[i-1].replace("W-2" + chr(0x2032), "W-2X")
    t2 = chr(10).join(L2)
    d2 = own_filter("contract", extract_checks(t2, CK_RE)); c2 = setof(t2, "covered_procedure_checks")
    mreport("M70-2", ("W-2" + chr(0x2032) in c2 and "W-2" + chr(0x2032) not in d2),
          "covered=%s defined=%s (母体行 %d 本を改変)" % ("W-2" + chr(0x2032) in c2, "W-2" + chr(0x2032) in d2, len(corpus)))
    # M70-3 covered enumeration を母体から除いても registry 不変
    t3 = re.sub(r"covered_procedure_checks = \[.*?\]", "covered_procedure_checks = []", ct, flags=re.S)
    d3a = own_filter("contract", extract_checks(ct, CK_RE)); d3b = own_filter("contract", extract_checks(t3, CK_RE))
    mreport("M70-3", d3a == d3b,
          "defined=%d -> %d 差分=%s" % (len(d3a), len(d3b), sorted(d3a ^ d3b)))
    # M70-4 W-2′ token 一貫性: 全て U+2032 / 母体へ U+0027 を一件注入 -> FAIL
    def tokscan(txt):
        return [i for i, l in enumerate(txt.split(chr(10)), 1) for bp in BADPRIME if ("W-2" + bp) in l]
    clean = all(len(tokscan(T[k])) == 0 for k in F)
    L4 = list(lines); injected = None
    for i in sorted(corpus):
        if "W-2" + chr(0x2032) in L4[i-1]:
            L4[i-1] = L4[i-1].replace("W-2" + chr(0x2032), "W-2" + chr(0x27), 1); injected = i; break
    t4 = chr(10).join(L4)
    caught = len(tokscan(t4)) > 0
    d4 = own_filter("contract", extract_checks(t4, CK_RE)); c4 = setof(t4, "covered_procedure_checks")
    mreport("M70-4", (clean and caught),
          "三文書とも非 U+2032 変種=0 -> %s / 注入行=%s -> token gate 検出=%s / 注入後 registry equality=%s"
          % (clean, injected, caught, d4 == c4))
    # M70-5 QD-1..4 concrete record で全 consumer 同一 verdict
    allsame = True; detail = []
    for label, (rec, exp) in REC.items():
        vs = {n: f(rec) for n, f in CONSUMERS}
        s_ = len(set(vs.values())) == 1 and list(vs.values())[0] == exp
        allsame &= s_; detail.append("%s=%s" % (label.split()[0], list(vs.values())[0]))
    mreport("M70-5", allsame,
          " ".join(detail))
    # M70-6 true record の四欄を一欄ずつ欠落 -> 各 [12] / pinned=[] は PASS
    base = dict(REC["QD-1 true/complete"][0]); rows = []; ok6 = True
    for k in ["build_definition_blob_digest", "pinned_input_digests", "build_root_id", "subject_build_binding_digest"]:
        r = dict(base); r.pop(k)
        vs = set(f(r) for _, f in CONSUMERS)
        hit = (vs == {"[12]"})
        rows.append("%s欠落->%s" % (k.split("_")[0], sorted(vs)))
        ok6 &= hit
    vs0 = set(f(base) for _, f in CONSUMERS)
    ok6 &= (vs0 == {"PASS"})
    mreport("M70-6", ok6,
          " ".join(rows) + " || pinned=[] base=%s" % sorted(vs0))

    # M70-7 [branch-contract] の required_keys を一欄削除
    #   B71-4: production と同一の bracket-aware parser が返す span を使って変異する。
    #   (前版は regex で list を切っており、本体で直した「非貪欲 regex が foo[] で切れる」bug を
    #    試験側で再導入していた -- 自認)
    mt_orig = T["manifest"]
    bm = re.search(r"^\[branch-contract\][^\n]*\n(.*?)```", mt_orig, re.S | re.M)
    blk = bm.group(1); base_off = bm.start(1)
    def _span(sec_name, field_name, b):
        sm = re.search(r"\n\s*" + sec_name + r"\s*:\s*\{", b)
        k = sm.end(); depth = 1
        while k < len(b) and depth:
            if b[k] == "{": depth += 1
            elif b[k] == "}": depth -= 1
            k += 1
        sec_lo, sec_hi = sm.end(), k - 1
        fm = re.search(field_name + r"\s*=\s*\[", b[sec_lo:sec_hi])
        s0 = sec_lo + fm.end(); p = s0; depth = 1
        while p < sec_hi and depth:
            if b[p] == "[": depth += 1
            elif b[p] == "]":
                depth -= 1
                if depth == 0: break
            p += 1
        return s0, p
    lo, hi = _span("false", "required_keys", blk)
    items = [x.strip() for x in blk[lo:hi].replace(chr(10), " ").split(",") if x.strip()]
    dropped = items[-1]
    blk2 = blk[:lo] + ", ".join(items[:-1]) + blk[hi:]
    mut = mt_orig[:base_off] + blk2 + mt_orig[base_off + len(blk):]
    changed = (mut != mt_orig)
    bc2 = parse_branch_contract(mut)
    base2, four2, rec2 = derive_keysets(bc2)
    fid2 = (bc2 is not None and base2 is not None and len(base2) == 3 and len(four2) == 4
            and set(bc2["true"]["required"]) == set(base2) | set(four2) | {"build_record_present"})
    behav = (base2 != BASE)
    mreport("M70-7", (changed and behav and not fid2),
            "削除欄=%s / block 改変=%s / 導出 BASE %d -> %d(変化=%s)/ fidelity=%s(要求: changed and behav and not fid2)"
            % (dropped, changed, len(BASE), len(base2 or []), behav, fid2))

    # ---- M71-1 typed branch domain の negative record(B71-5)----
    H2 = "b" * 64
    NEG = [
      ("present=non-boolean",            {"build_record_present": "yes", "source_artifact_digests": [SRC],
                                          "toolchain_digest": H2, "build_step_digests": [H2]}, "[12]"),
      ("false+toolchain=null",           {"build_record_present": False, "source_artifact_digests": [SRC],
                                          "toolchain_digest": None, "build_step_digests": [H2]}, "[12]"),
      ("false+toolchain=non-64hex",      {"build_record_present": False, "source_artifact_digests": [SRC],
                                          "toolchain_digest": "deadbeef", "build_step_digests": [H2]}, "[12]"),
      ("false+build_steps=non-list",     {"build_record_present": False, "source_artifact_digests": [SRC],
                                          "toolchain_digest": H2, "build_step_digests": H2}, "[12]"),
      ("true+pinned=non-list",           {"build_record_present": True, "source_artifact_digests": [SRC],
                                          "toolchain_digest": H2, "build_step_digests": [H2],
                                          "build_definition_blob_digest": H2, "pinned_input_digests": H2,
                                          "build_root_id": H2, "subject_build_binding_digest": H2}, "[12]"),
      ("true+pinned=[]",                 {"build_record_present": True, "source_artifact_digests": [SRC],
                                          "toolchain_digest": H2, "build_step_digests": [H2],
                                          "build_definition_blob_digest": H2, "pinned_input_digests": [],
                                          "build_root_id": H2, "subject_build_binding_digest": H2}, "PASS"),
    ]
    rows = []; okneg = True
    for label, rec, exp in NEG:
        vs = set(f(rec) for _, f in CONSUMERS)
        good = (vs == {exp})
        okneg &= good
        rows.append("%s->%s%s" % (label, sorted(vs), "" if good else "(期待 %s)" % exp))
    mreport("M71-1", okneg, "typed domain negative 6 本(全 consumer 一致を要求): " + " ".join(rows))

    # ---- M71-2 通常 prose + covered の双方へ W-9(F10.2 の別本回帰)----
    t9 = ct.replace("## 1. 役割と非役割", "本文中に W-9 という語を置く(通常 prose)。\n\n## 1. 役割と非役割", 1)
    t9 = t9.replace("covered_procedure_checks = [", "covered_procedure_checks = [W-9, ", 1)
    d9 = own_filter("contract", extract_checks(t9, CK_RE)); c9 = setof(t9, "covered_procedure_checks")
    mreport("M71-2", ("W-9" in c9 and "W-9" not in d9),
            "通常 prose と covered の双方へ W-9 -> defined=%s covered=%s(extra-covered を検出)" % ("W-9" in d9, "W-9" in c9))

    # ---- M71-3 BC_USE_MAP causal-use gate(B74-3: 正方向も強制・probe 集合の verdict vector で判定)----
    def bc_mutate(field):
        bm2 = re.search(r"^\[branch-contract\][^\n]*\n(.*?)```", T["manifest"], re.S | re.M)
        b = bm2.group(1)
        def span(sec, fld):
            sm = re.search(r"\n\s*" + sec + r"\s*:\s*\{", b); k2 = sm.end(); dep = 1
            while k2 < len(b) and dep:
                if b[k2] == "{": dep += 1
                elif b[k2] == "}": dep -= 1
                k2 += 1
            lo0, hi0 = sm.end(), k2 - 1
            fm2 = re.search(fld + r"\s*=\s*\[", b[lo0:hi0])
            if not fm2: return None, None
            s0 = lo0 + fm2.end(); p = s0; dep = 1
            while p < hi0 and dep:
                if b[p] == "[": dep += 1
                elif b[p] == "]":
                    dep -= 1
                    if dep == 0: break
                p += 1
            return s0, p
        if field == "recompute":
            b2 = b.replace("recompute      = [D-1, D-2]", "recompute      = [D-1, D-2, D-3, D-4" + chr(0x2032) + "]", 1)
        elif field == "closure_policy":
            b2 = b.replace("closure_policy = bootstrap_leaf", "closure_policy = recursive", 1)
        elif field in ("forbidden_keys", "required_keys"):
            lo, hi = span("false", field)
            if lo is None: return None
            items = [x.strip() for x in b[lo:hi].replace(chr(10), " ").split(",") if x.strip()]
            b2 = b[:lo] + ", ".join(items[:-1]) + b[hi:]      # bracket-aware に末尾 1 欄を削除
        else:
            b2 = b
        if b2 == b: return None
        return parse_branch_contract(T["manifest"].replace(b, b2, 1))
    HX = "a" * 64
    PROBES = [dict(REC["QD-1 true/complete"][0]), dict(REC["QD-3 false/canon"][0])]
    PROBES.append({"build_record_present": False, "source_artifact_digests": [SRC],
                   "toolchain_digest": HX, "build_step_digests": [HX],
                   "subject_build_binding_digest": HX})            # forbidden 感応 probe
    PROBES.append({"build_record_present": False, "source_artifact_digests": [SRC],
                   "toolchain_digest": HX})                        # required 感応 probe
    CONSF = dict(CONSUMERS)
    def vec(fn, policy=None):
        out = []
        for r in PROBES:
            try: out.append(fn(r, policy) if fn in (consumer_R6, consumer_H1a) else fn(r))
            except TypeError: out.append(fn(r))
        return tuple(out)
    okmap = (BC_USE is not None); det = []
    if BC_USE is not None:
        for field in ("recompute", "closure_policy", "forbidden_keys", "required_keys"):
            bc2 = bc_mutate(field)
            if bc2 is None: okmap = False; det.append("%s: 変異不能" % field); continue
            b2, f2, r2 = derive_keysets(bc2); p2 = derive_policy(bc2)
            for cname, fn in CONSF.items():
                deps = BC_USE.get(cname, [])
                base_vec = vec(fn, POLICY)
                sv = (BASE, FOUR, RECOMPUTE, BC)
                globals()["BASE"], globals()["FOUR"], globals()["RECOMPUTE"], globals()["BC"] = b2, f2, r2, bc2
                mut_vec = vec(fn, p2)
                globals()["BASE"], globals()["FOUR"], globals()["RECOMPUTE"], globals()["BC"] = sv
                changed_v = (base_vec != mut_vec)
                if field not in deps and changed_v:
                    okmap = False; det.append("%s は %s に非依存と宣言だが変化" % (cname, field))
                if field in deps and not changed_v:
                    okmap = False; det.append("%s は %s に依存と宣言だが不変(causal-use 不成立)" % (cname, field))
            det.append("%s 変異 OK" % field)
        bc_pol = bc_mutate("closure_policy"); p_pol = derive_policy(bc_pol)
        LEAF = dict(REC["QD-3 false/canon"][0])
        r6b, r6a = consumer_R6(LEAF, POLICY), consumer_R6(LEAF, p_pol)
        okmap &= (r6b == "PASS" and r6a == "[11]")
        det.append("closure_policy 負例: R-6 %s -> %s(要求 PASS->[11])" % (r6b, r6a))
    mreport("M71-3", okmap, "causal-use gate(正逆双方向・probe 4 本の verdict vector): " + " ; ".join(det))

    # ---- M72-1 production path の build face 回帰(B74-4)----
    #   別実装の clone を使わず production の build_face_projection() / i3d_decision() を呼ぶ。
    #   TCB subtraction と I-3d の [11] decision まで実行し、
    #   production から toolchain append を外す変異で FAIL することを確認する。
    TOOL = "a" * 64
    LEAF_A = {"build_record_present": False, "source_artifact_digests": ["1" * 64],
              "toolchain_digest": TOOL, "build_step_digests": ["d" * 64]}
    LEAF_B = {"build_record_present": False, "source_artifact_digests": ["2" * 64],
              "toolchain_digest": TOOL, "build_step_digests": ["f" * 64]}
    pA, pB = build_face_projection(LEAF_A), build_face_projection(LEAF_B)
    dec_empty_tcb = i3d_decision(pA, pB, [])          # 初期 TCB は四欄とも空
    dec_with_tcb  = i3d_decision(pA, pB, [TOOL])      # toolchain を TCB に入れれば PASS
    # production を変異: projection から toolchain を外す
    _orig_proj = build_face_projection
    def _mutated_proj(rec):
        p = set(_orig_proj(rec))
        p.discard(rec.get("toolchain_digest"))
        return p
    globals()["build_face_projection"] = _mutated_proj
    mut_dec = i3d_decision(build_face_projection(LEAF_A), build_face_projection(LEAF_B), [])
    globals()["build_face_projection"] = _orig_proj
    doc_expr = re.search(r"^build_artifact_set\(X\)[^\n]*", T["manifest"], re.M)
    doc_ok = bool(doc_expr) and "entry.toolchain_digest" in doc_expr.group(0) and "#" not in doc_expr.group(0)
    mreport("M72-1", (dec_empty_tcb == "[11]" and dec_with_tcb == "PASS" and mut_dec == "PASS" and doc_ok),
            "production projection + I-3d decision: 空 TCB=%s / TCB={toolchain}=%s / "
            "production から toolchain を外す変異=%s(PASS へ退行 -> 検出)/ 文書式 operand=%s"
            % (dec_empty_tcb, dec_with_tcb, mut_dec, doc_ok))

    # ---- M72-2 要素レベル negative(B72-4)----
    NEG2 = [
      ("build_steps=[非 64hex]", {"build_record_present": False, "source_artifact_digests": [SRC],
                                   "toolchain_digest": H, "build_step_digests": ["deadbeef"]}, "[12]"),
      ("pinned=[非 64hex]",      {"build_record_present": True, "source_artifact_digests": [SRC],
                                   "toolchain_digest": H, "build_step_digests": [H],
                                   "build_definition_blob_digest": H, "pinned_input_digests": ["deadbeef"],
                                   "build_root_id": H, "subject_build_binding_digest": H}, "[12]"),
      ("source=[非 64hex]",      {"build_record_present": False, "source_artifact_digests": ["s"],
                                   "toolchain_digest": H, "build_step_digests": [H]}, "[12]"),
      ("build_steps=[null]",     {"build_record_present": False, "source_artifact_digests": [SRC],
                                   "toolchain_digest": H, "build_step_digests": [None]}, "[12]"),
    ]
    rows2 = []; ok2n = True
    for label, rec, exp in NEG2:
        vs = set(f(rec) for _, f in CONSUMERS)
        g = (vs == {exp}); ok2n &= g
        rows2.append("%s->%s%s" % (label, sorted(vs), "" if g else "(期待 %s)" % exp))
    mreport("M72-2", ok2n, "要素レベル negative 4 本(全 consumer 一致を要求): " + " ".join(rows2))

    # ---- M74-1 順序保存列 vs 集合表現(B74-1 の accepted universe 回帰)----
    HB, HA = "b" * 64, "a" * 64
    ORD_OK = {"build_record_present": False, "source_artifact_digests": [SRC],
              "toolchain_digest": HA, "build_step_digests": [HB, HA]}      # 非辞書順の有効な build 手順
    SRC_BAD = {"build_record_present": False, "source_artifact_digests": [HB, HA],
               "toolchain_digest": HA, "build_step_digests": [HA]}          # set 表現欄の未 sort
    DUP_STEP = {"build_record_present": False, "source_artifact_digests": [SRC],
                "toolchain_digest": HA, "build_step_digests": [HA, HA]}     # 手順の重複(順序列なので可)
    v_ord = set(f(ORD_OK) for _, f in CONSUMERS)
    v_src = set(f(SRC_BAD) for _, f in CONSUMERS)
    v_dup = set(f(DUP_STEP) for _, f in CONSUMERS)
    canon_ok = (CANON.get("build_step_digests[]") == "order-preserving-seq"
                and CANON.get("source_artifact_digests[]") == "sorted-dedup-set")
    mreport("M74-1", (v_ord == {"PASS"} and v_src == {"[12]"} and v_dup == {"PASS"} and canon_ok),
            "非辞書順 build 手順 [b,a] -> %s(要求 PASS)/ 手順の重複 -> %s(要求 PASS)/ "
            "source の未 sort -> %s(要求 [12])/ canonicality を block から取得=%s"
            % (sorted(v_ord), sorted(v_dup), sorted(v_src), canon_ok))

    # ---- meta-fixture: regression 自身を故意に false 化 -> nonzero exit を確認 ----
    _saved = list(mutation_fails)
    mreport("META-1(意図的 false)", False, "meta-fixture: この行は必ず FAIL し、footer と exit code に伝播することを確認する")
    meta_ok = (len(mutation_fails) == len(_saved) + 1)
    mutation_fails[:] = _saved          # 検査後に取り消す(本番 verdict を汚さない)
    # META-3: 同じ exit contract を持つ子プロセスで、意図的 FAIL が非 0 exit になることを実測する
    import subprocess as _sp
    _probe = os.path.join(D, "search", "_meta_exit_probe.py")
    with open(_probe, "w", encoding="utf-8") as _f:
        _f.write("import sys\nfails=[]\nmutation_fails=['META-INTENTIONAL']\nALLF=list(fails)+list(mutation_fails)\nsys.exit(0 if not ALLF else 1)\n")
    _r = _sp.run([sys.executable, _probe], capture_output=True)
    try: os.remove(_probe)
    except OSError: pass
    mreport("META-2", meta_ok and _r.returncode == 1,
            "意図的 FAIL が mutation_fails[] に伝播=%s / 同じ exit contract の子プロセス exit code=%d(要求 1)"
            % (meta_ok, _r.returncode))

    # ---- F12.2 machine-readable footer ----
    MTOTAL = 14   # M70-1..7 + M71-1..3 + M72-1..2 + META-2
    print()
    print("[mutation-footer]")
    print("mutation_total  = %d" % MTOTAL)
    print("mutation_passed = %d" % (MTOTAL - len(mutation_fails)))
    print("mutation_failed = %s" % (mutation_fails if mutation_fails else "[]"))
    print("normal_failed   = %s" % (fails if fails else "[]"))
    print("overall_exit_contract = (normal_failed union mutation_failed == empty)")

# ---------- 15. consumer 三集合 exact equality (B74-3 / F6.3) ----------
lit = set(CONSUMER_LITERAL)
mapk = set((BC_USE or {}).keys())
exe = set(n for n, _ in CONSUMERS)
ok15 = (lit == mapk == exe) and len(lit) > 0
report(15, "consumer 三集合 exact equality ([branch-contract] literal / BC_USE_MAP / executable)", ok15,
       "literal %d / map %d / executable %d ; literal-map=%s map-exe=%s exe-literal=%s"
       % (len(lit), len(mapk), len(exe), sorted(lit - mapk), sorted(mapk - exe), sorted(exe - lit)))

# ---------- 16. [27] semantic-axis S2 帯 = 明示集合、spec/contract 一致 (v9・便95 W95-2.3) ----------
def _s2_set(txt):
    m = re.search(r"S2_CODES\s*=\s*\{([^}]*)\}", txt)
    if not m: return None
    return set(int(x) for x in re.findall(r"\d+", m.group(1)))
def _s2_routing_line(txt):
    # the SINGLE normative routing line itself (not surrounding prose/comments,
    # which may legitimately quote the old "[13]..[24]" notation to explain why
    # it was replaced -- see the S2_CODES rationale comment)
    m = re.search(r"^.*S2  native cross-check.*$", txt, re.M)
    return m.group(0) if m else ""
s2_spec = _s2_set(T["spec"])
s2_contract = _s2_set(T["contract"])
S2_EXPECTED = {13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 27}
range_notation_gone = ("[13]..[24]" not in _s2_routing_line(T["spec"])
                        and "[13]..[24]" not in _s2_routing_line(T["contract"]))
ok16 = (s2_spec == S2_EXPECTED) and (s2_contract == S2_EXPECTED) and range_notation_gone
report(16, "S2 帯 = 明示集合(range 表記でない)・spec/contract 一致・{27} を含む", ok16,
       "spec S2_CODES=%s contract S2_CODES=%s expected=%s range_notation_gone=%s"
       % (s2_spec, s2_contract, sorted(S2_EXPECTED), range_notation_gone))

def _readf(path):
    with open(path, encoding="utf-8", errors="replace") as _f:
        return _f.read()


# ---------- 17. S2 帯内累積 (v9 additive・便96 W96-2.1 / R96-1) ----------
# ADDITIVE: no existing check is weakened or removed. This one fixes the
# repair Sol demanded -- spec sec.5.3.2's worked example ([24]+[27] together)
# and X-1 must not contradict each other again -- and it also asserts the
# lane-side consequence (X-1a), because a document-only repair would leave
# the implementations free to drift back.
_lane_b = _readf(os.path.join(D, "search", "ninfty-checker.py"))
_lane_a = _readf(os.path.join(D, "search", "ninfty-searcher-v2.mjs"))
_cum_declared = all("S2 帯内は累積" in T[k] for k in ("spec", "contract"))
_pairs_declared = all("S2_EQUIVALENT_CAUSE_PAIRS" in T[k] for k in ("spec", "contract"))
# the OLD, self-contradicting formulation must be gone from the LIVE X-1 rows
_x1_rows = [ln for k in ("spec", "contract") for ln in T[k].splitlines()
            if ln.startswith("| **X-1**")]
_old_gone = len(_x1_rows) == 2 and not any("semantic axis は軸内で排他" in ln for ln in _x1_rows)
# X-1a must exist in both documents
_x1a = all("X-1a" in T[k] for k in ("spec", "contract"))
# lane B: the [27] site must NOT early-return, and primary must be machine-computed
_b_site = _lane_b.split("INTEGRITY_DIVISOR_ORIENTATION_MISMATCH)", 1)
_b_no_early = (len(_b_site) == 2
               and "return result" not in _b_site[1].split("t1_stage", 1)[0]
               and "_resolve_stage_and_primary" in _lane_b)
# lane A was already cumulative: it must keep using a SET, never an early return
_a_cumulative = ("const I = new Set()" in _lane_a) and ("I.add('divisor-orientation-attestation-mismatch')" in _lane_a)
ok17 = _cum_declared and _pairs_declared and _old_gone and _x1a and _b_no_early and _a_cumulative
report(17, "S2 帯内は累積(spec/contract 同期・X-1a・両 lane に early-return 無し)", ok17,
       "declared=%s pairs=%s old_exclusivity_gone=%s X-1a=%s laneB_no_early_return=%s laneA_set=%s"
       % (_cum_declared, _pairs_declared, _old_gone, _x1a, _b_no_early, _a_cumulative))

# ---------- 18. payload-era matrix (v9 additive・便96 W96-2.2 / R96-2) ----------
_full = _readf(os.path.join(D, "search", "ninfty-evidence-union-full.py"))
_PLANES = ("frozen_route_verifier", "native_payload_schema", "nf_route",
           "decision_lane_predicate", "control_plane")
_planes_in_spec = all(pl in T["spec"] for pl in _PLANES)
_planes_in_code = all(('"%s"' % pl) in _full for pl in _PLANES)
_matrix_declared = "PAYLOAD_ERA_MATRIX" in T["spec"] and "PAYLOAD_ERA_MATRIX" in _full
_y3b = "Y-3b" in T["manifest"]
# the renamed consumer field, and the banned old name, as EMITTED keys
_renamed = '"control_plane_docs_receipt_binding"' in _full and '"payload_era_matrix"' in _full
_old_name_gone = '"docs_era_binding"' not in _full
# every live plane source must actually carry its marker
_markers_ok = True
_marker_detail = {}
for _rel, _want in (("search/ninfty-checker.py", ["decision_lane_predicate"]),
                    ("search/ninfty-verifier-w6-r3nf.py", ["nf_route"]),
                    ("search/ninfty-searcher-v2.mjs", ["native_payload_schema", "decision_lane_predicate"])):
    _src = _readf(os.path.join(D, *_rel.split("/")))
    _got = re.findall(r"\[ep-era-declaration\] plane=([a-z_]+)", _src)
    _marker_detail[_rel] = sorted(_got)
    if sorted(_got) != sorted(_want):
        _markers_ok = False
# the BYTE-FROZEN verifier must NOT have been given a marker
_frozen_untouched = "[ep-era-declaration]" not in _readf(os.path.join(D, "search", "ninfty-verifier-b.py"))
ok18 = (_planes_in_spec and _planes_in_code and _matrix_declared and _y3b
        and _renamed and _old_name_gone and _markers_ok and _frozen_untouched)
report(18, "payload-era matrix(5 plane・Y-3b・欄名分離・marker 実在・frozen 無改変)", ok18,
       "spec=%s code=%s matrix=%s Y-3b=%s renamed=%s old_name_gone=%s markers=%s frozen_untouched=%s"
       % (_planes_in_spec, _planes_in_code, _matrix_declared, _y3b, _renamed,
          _old_name_gone, _marker_detail, _frozen_untouched))

# ---------- 19. W-6 option (a) と UNKNOWN W6-KEY (v9 additive・便96 W96-2.3 / R96-3) ----------
_w6_clauses = ["W6-C%d" % i for i in range(1, 8)]
_w6_spec = all(c in T["spec"] for c in _w6_clauses)
_w6_con = all(c in T["contract"] for c in _w6_clauses)
_w6_unknown = "UNKNOWN W6-KEY" in T["spec"] and "UNKNOWN W6-KEY" in T["contract"]
# the non-implication must be stated, not merely implied
_w6_noimply = "R3-NF PASS は W-6 を含意しない" in T["spec"]
ok19 = _w6_spec and _w6_con and _w6_unknown and _w6_noimply
report(19, "W-6 = option (a)・R3-NF 非含意・UNKNOWN W6-KEY 登録(spec/contract 同期)", ok19,
       "spec_clauses=%s contract_clauses=%s unknown_registered=%s non_implication_stated=%s"
       % (_w6_spec, _w6_con, _w6_unknown, _w6_noimply))

print("\nsha256:")
for k, p in F.items(): print("  %-9s %s  %s" % (k, DG[k], p))
ALLF = list(fails) + list(mutation_fails)
print("\nRESULT:", "ALL PASS" if not ALLF else "FAIL at " + str(ALLF))
sys.exit(0 if not ALLF else 1)
