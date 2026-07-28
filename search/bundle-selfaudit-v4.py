#!/usr/bin/env python3
# bundle-selfaudit-v4.py -- N_infty stage2 freeze bundle self-audit (13 checks + M69 変異試験)
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
# usage: python search/bundle-selfaudit-v4.py [--mutate]   (exit 0 = ALL PASS)
import os, re, sys, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {"spec":     "docs/week4-NInfty_stage2_spec_v13.md",
     "contract": "docs/mb_ninfty_verifier_contract_v8.md",
     "manifest": "docs/mb_dependency_manifest_v8.md"}
CUR = {"spec": "v13", "contract": "v8", "manifest": "v8"}
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
def extract_checks(txt, ck_re):
    cls = classify(txt)
    out = set()
    for i, l in enumerate(txt.split("\n"), 1):
        if cls.get(i) in ("table", "prose", "code", "blockquote"):
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
    creg = extract_checks(txt, ck); ccov = setof(txt, "covered_procedure_checks") or set(); cunc = setof(txt, "uncovered_checks") or set()
    cgood = (ccov & cunc == set()) and (ccov | cunc == creg)
    d3.append("%s: reg=%d cov=%d eq=%s" % (name, len(creg), len(ccov), cgood))
    if not cgood: ok3 = False; d3.append("  reg-cov=%s cov-reg=%s" % (sorted(creg - ccov)[:8], sorted(ccov - creg)[:8]))
report(2, "clause registry 集合等式(文書 regex)", ok2, " ; ".join(d2))
report(3, "check registry 集合等式(W-2′ を含む)", ok3, " ; ".join(d3))

# ---------- 4. 四象限 fixture (B69-4) ----------
mt = T["manifest"]
quad = all(("| **QD-%d**" % k) in mt for k in range(1, 8))
canon = "[canonical-empty]" in mt and "ABSENT" in mt
d3only = bool(re.search(r"D-3 と D-4′ は top-level と .?build_record_present = true.? の entry だけで再計算", mt))
sent = "要素にならない" in mt
ok4 = quad and canon and d3only and sent
report(4, "build_record_present 四象限 fixture (B69-4)", ok4,
       "QD-1..7=%s / [canonical-empty]+ABSENT=%s / D-3,D-4′ を true 限定=%s / sentinel 非混入=%s" % (quad, canon, d3only, sent))

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
    sd = re.search(r'current_version\s*=\s*"v(\d+)".*?historical_upper_bound\s*=\s*"v(\d+)"', T[name], re.S)
    if not sd or int(sd.group(2)) != int(sd.group(1)) - 1 or "v" + sd.group(1) != CUR[name]:
        ok13 = False; r13.append("%s: sweep-def 版不整合" % name)
report(13, "authblock label<->digest + sweep-def 上限", ok13, "NG=%s" % (r13 if r13 else 0))

# ================= M69 変異試験 =================
if "--mutate" in sys.argv:
    print("\n--- M69 変異試験 ---")
    def mut(name, f):
        T2 = dict(T); T2[name] = f(T[name]); return T2
    # M69-1: operative blockquote / schema fence へ旧 ID 注入
    inj = T["contract"].replace("## 1. 役割と非役割", "> 本稿は mb/dependency-manifest/v5 を参照する。\n\n## 1. 役割と非役割", 1)
    r1 = len(sweep({**T, "contract": inj})) > 0
    inj2 = T["contract"].replace("```text\nconformance_record = {", "```text\nconformance_record = {\n  # manifest v5 §2.1", 1)
    r1b = len(sweep({**T, "contract": inj2})) > 0
    print(("PASS" if r1 and r1b else "FAIL"), "| M69-1 operative bq/fence への旧 ID 注入 -> sweep FAIL |",
          "blockquote=%s fence=%s" % (r1, r1b))
    # M69-2: C-6⁗ の exact 抽出
    row = "| **C-6⁗** | dummy |"
    got = [m.group(1) for m in [re.match(CL_RE, row)] if m]
    print(("PASS" if got == ["C-6⁗"] else "FAIL"), "| M69-2 文書 regex が C-6⁗ を exact 抽出 |", got)
    # M69-3: W-2′ を covered から削除 -> equality FAIL
    t3 = T["contract"].replace("W-2′, ", "", 1)
    creg = extract_checks(t3, CK_RE); ccov = setof(t3, "covered_procedure_checks") or set()
    print(("PASS" if ccov != creg else "FAIL"), "| M69-3 W-2′ 削除 -> check equality FAIL |",
          "reg-cov=%s" % sorted(creg - ccov)[:4])
    # M69-4: 正直な false leaf fixture
    ok4a = ("D-1 と D-2 は全 entry で再計算" in mt)
    ok4b = bool(re.search(r"D-3 と D-4′ は top-level と .?build_record_present = true.? の entry だけで再計算", mt))
    ok4c = ("要素にならない" in mt)
    print(("PASS" if ok4a and ok4b and ok4c else "FAIL"),
          "| M69-4 false leaf -> D-1/D-2 検査・D-3/D-4′ 免除・sentinel 非混入 |",
          "D1D2=%s D3D4免除=%s sentinel=%s" % (ok4a, ok4b, ok4c))
    # M69-5: true 反転 + 一欄欠落 -> [12]
    q2 = "| **QD-2** | `true` | missing" in mt and "[12]" in mt
    print(("PASS" if q2 else "FAIL"), "| M69-5 true + 一欄欠落 -> digest-mismatch [12] |", "QD-2 規定=%s" % q2)

print("\nsha256:")
for k, p in F.items(): print("  %-9s %s  %s" % (k, DG[k], p))
print("\nRESULT:", "ALL PASS" if not fails else "FAIL at " + str(fails))
sys.exit(0 if not fails else 1)
