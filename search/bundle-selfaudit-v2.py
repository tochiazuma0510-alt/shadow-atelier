#!/usr/bin/env python3
# bundle-selfaudit-v2.py -- N_infty stage2 freeze bundle self-audit (11 checks)
# v2 (裁定 84 / 内部前哨ゲート FINDING-4):
#   - 除外域を **構造ベース** に変更(コードフェンス境界・明示ブロック・表行・blockquote)
#     v1 の HIST 15 語の行内部分一致は廃止した。
#   - 裸 v トークン(【v4 新設】型)も sweep 対象に含める。
#   - check registry の完全性(CR-5..7)を追加。
#   - subject binding が record 粒度で自己完結しているか(FINDING-1)を追加。
# usage: python search/bundle-selfaudit-v2.py   (exit 0 = ALL PASS)
import os, re, sys, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {"spec":     "docs/week4-NInfty_stage2_spec_v11.md",
     "contract": "docs/mb_ninfty_verifier_contract_v6.md",
     "manifest": "docs/mb_dependency_manifest_v6.md"}
CUR = {"spec": "v11", "contract": "v6", "manifest": "v6"}
T = {k: open(os.path.join(D, p), encoding='utf-8').read() for k, p in F.items()}
Bb = {k: open(os.path.join(D, p), 'rb').read() for k, p in F.items()}
DG = {k: hashlib.sha256(v).hexdigest() for k, v in Bb.items()}
fails = []
def report(n, name, ok, detail):
    print(("PASS" if ok else "FAIL"), "|", n, name, "|", detail)
    if not ok: fails.append(n)

# ================= 構造分類器(v2 の核) =================
def classify(txt):
    """行番号 -> 構造クラス。語の部分一致は使わない。"""
    cls = {}
    lines = txt.split("\n")
    fence = False; fence_kind = None
    in_diff = False        # '## ... 差分' 見出し配下の表
    for i, l in enumerate(lines, 1):
        st = l.strip()
        if st.startswith("```"):
            fence = not fence
            if fence:
                fence_kind = "authblock" if False else "code"
            cls[i] = "fence-delim"
            continue
        if fence:
            cls[i] = "code"
            continue
        if re.match(r"^#{2,4} ", l):
            in_diff = bool(re.search(r"(差分|版履歴)", l))
            cls[i] = "heading"; continue
        if st.startswith(">"):
            cls[i] = "blockquote"; continue
        if st.startswith("|"):
            cls[i] = "difftable" if in_diff else "table"; continue
        if st.startswith("supersedes"):
            cls[i] = "supersedes"; continue
        cls[i] = "prose"
    # 明示ブロック(live_authority_refs / historical_quotation_refs)は
    # 直後のコードフェンス内に限り authblock に格上げ
    for m in re.finditer(r"^(live_authority_refs|historical_quotation_refs)\[\]", txt, re.M):
        ln = txt[:m.start()].count("\n") + 1
        j = ln
        while j <= len(lines) and cls.get(j) == "code":
            cls[j] = "authblock"; j += 1
        j = ln - 1
        while j >= 1 and cls.get(j) in ("code", "authblock"):
            cls[j] = "authblock"; j -= 1
    return cls
# operative(= 除外しない)クラス
OPERATIVE = {"prose", "table", "heading", "fence-delim"}

# ---------- 1. version-token sweep (B68-1 / FINDING-4) ----------
PAT = [("spec", r"mb/ninfty-stage2-predicate/v(\d+)"), ("spec", r"spec v(\d+)"),
       ("contract", r"mb/ninfty-verifier-contract/v(\d+)"), ("contract", r"contract v(\d+)"),
       ("manifest", r"mb/dependency-manifest/v(\d+)"), ("manifest", r"manifest v(\d+)"),
       (None, r"【v(\d+)[^】]*】"), (None, r"(?<!spec )(?<!contract )(?<!manifest )(?<!predicate/)\bv(\d+) (?:で|から|は|新設|更新|訂正|修正)")]
stale = []
for name, txt in T.items():
    cls = classify(txt)
    for i, l in enumerate(txt.split("\n"), 1):
        if cls.get(i) not in OPERATIVE: continue
        for series, pat in PAT:
            masked = re.sub(r"\u3010chg [^\u3011]*\u3011", "", l)
            for m in re.finditer(pat, masked):
                ver = "v" + m.group(1)
                tgt = series if series else name
                if ver == CUR.get(tgt): continue
                stale.append((name, i, cls[i], tgt, ver, l.strip()[:64]))
report(1, "version-token sweep (構造除外/裸 v 込み)", len(stale) == 0,
       "pattern=8(3 系列 x 2 形式 + 【vN …】 + 裸 vN 助詞) / 除外域=code, authblock, blockquote, difftable, supersedes "
       "(語の部分一致は不使用) / LIVE-STALE=%d" % len(stale))
for s_ in stale[:12]: print("      ", s_)

# ---------- 2. clause registry set equality ----------
REG_RE = r"^\| \*\*([A-Z][A-Za-z0-9\-\.]*[′″‴]?)\*\* \|"
def setof(txt, key):
    m = re.search(key + r" = \[(.*?)\]", txt, re.S)
    if not m: return None
    return set(x.strip() for x in m.group(1).replace(chr(10), " ").split(",") if x.strip())
ok2 = True; det = []
for name in ("contract", "manifest"):
    txt = T[name]
    reg = set(m.group(1) for m in re.finditer(REG_RE, txt, re.M))
    cov = setof(txt, "covered_clauses") or set()
    unc = setof(txt, "uncovered_clauses") or set()
    rng = [c for c in (cov | unc) if ".." in c]
    ok = (not rng) and (cov & unc == set()) and (cov | unc == reg)
    det.append("%s clause: reg=%d cov=%d unc=%d range=%d eq=%s" % (name, len(reg), len(cov), len(unc), len(rng), ok))
    if not ok:
        ok2 = False
        det.append("   reg-cov=%s cov-reg=%s" % (sorted(reg - cov)[:8], sorted(cov - reg)[:8]))
report(2, "clause registry set equality (F13.3)", ok2, " ; ".join(det))

# ---------- 3. check registry set equality (FINDING-3 / CR-5..7) ----------
CHK_RE = r"(?<![A-Za-z0-9])(D-[0-9]′?|U-[0-9]|P-[0-9]\.[0-9]|W-[0-9]|W-2′|S[123]|C1)(?![A-Za-z0-9])"
ok3 = True; det3 = []
for name in ("contract", "manifest"):
    txt = T[name]
    body = re.sub(r"covered_procedure_checks = \[.*?\]", "", txt, flags=re.S)
    body = re.sub(r"covered_clauses = \[.*?\]", "", body, flags=re.S)
    reg = set(m.group(1) for m in re.finditer(CHK_RE, body))
    cov = setof(txt, "covered_procedure_checks")
    unc = setof(txt, "uncovered_checks")
    if cov is None:
        ok3 = False; det3.append("%s: covered_procedure_checks 欄なし" % name); continue
    unc = unc or set()
    rng = [c for c in (cov | unc) if ".." in c]
    ok = (not rng) and (cov & unc == set()) and (cov | unc == reg)
    det3.append("%s check: reg=%d cov=%d unc=%d eq=%s" % (name, len(reg), len(cov), len(unc), ok))
    if not ok:
        ok3 = False
        det3.append("   reg-cov=%s cov-reg=%s" % (sorted(reg - cov)[:8], sorted(cov - reg)[:8]))
report(3, "check registry set equality (FINDING-3)", ok3, " ; ".join(det3))

# ---------- 4. subject binding が record 粒度で自己完結 (FINDING-1) ----------
mt = T["manifest"]
d4 = re.search(r"D-4′?\s+subject_build_binding_digest\s*=(.{0,700})", mt, re.S)
body4 = d4.group(1) if d4 else ""
per_record = ("top-level record" in body4 and "content_digest" in body4)
cls_m0 = classify(mt)
no_cross = not any("相互照合" in l for i, l in enumerate(mt.split(chr(10)), 1)
                   if cls_m0.get(i) in OPERATIVE)
absent_decl = "build_record_present" in mt
i0 = "I-0c″" in mt
ok4 = per_record and no_cross and absent_decl and i0
report(4, "subject binding の record 粒度自己完結 (FINDING-1)", ok4,
       "D-4' に record 別 subject 出所=%s / live '相互照合' 残存=%s / build_record_present 宣言=%s / I-0c''=%s"
       % (per_record, not no_cross, absent_decl, i0))

# ---------- 5. certificate schema の欄がすべて定義済み (FINDING-2) ----------
st = T["spec"]
cs = re.search(r"divisor_equality_certificate = \{(.*?)\n\}", st, re.S).group(1)
fields = set()
for l in cs.split("\n"):
    l = l.split("#")[0].strip().rstrip(",")
    if not l or l.startswith("#"): continue
    for tok in re.findall(r"^([a-z_]+[a-z0-9_]*)", l): fields.add(tok)
undef = [f for f in sorted(fields)
         if st.count(f) < 2 and T["contract"].count(f) == 0]
cls_s0 = classify(st)
cert_block = re.search(r"divisor_equality_certificate = \{.*?\n\}", st, re.S).group(0)
ve_operative = any("verifier_evidence" in l for i, l in enumerate(st.split(chr(10)), 1)
                   if cls_s0.get(i) == "table")
ok5 = ("verifier_evidence" not in cert_block) and (not ve_operative) and not undef
report(5, "certificate schema の未定義欄 (FINDING-2)", ok5,
       "cert schema 内 verifier_evidence=%s / operative table 内=%s / 定義参照が spec 内 1 回のみかつ contract 不参照の欄=%s"
       % ("verifier_evidence" in cert_block, ve_operative, undef))

# ---------- 6. anchor existence + binding direction ----------
ok6 = True; rows6 = []
for m in re.finditer(r'schema_id\(\s*([\w\-]+)\s*\)\s*=\s*(\w+)\s*\+\s*"#([\w\-]+)"', st):
    nm, owner, anc = m.group(1), m.group(2), m.group(3)
    tgt = {"predicate_spec_id": "spec", "verifier_contract_id": "contract",
           "dependency_manifest_schema_id": "manifest"}.get(owner)
    exists = ("{#" + anc + "}") in T.get(tgt, "")
    bm = re.search(r"bound_blob_digest\(\s*" + re.escape(nm) + r"\s*\)\s*=\s*(\w+)", st)
    bound = bm.group(1) if bm else "(grouped)"
    expect = {"spec": "predicate_spec_digest", "contract": "verifier_contract_digest",
              "manifest": "dependency_manifest_schema_digest"}[tgt]
    good = exists and (bound == expect or (bound == "(grouped)" and tgt == "spec"))
    if not good: ok6 = False; rows6.append("%s->%s#%s exists=%s bound=%s" % (nm, tgt, anc, exists, bound))
report(6, "anchor existence + binding direction", ok6, "NG=%d (全 %d anchor)" % (len(rows6), len(re.findall(r'schema_id\(', st))) + ("" if ok6 else " " + str(rows6)))

# ---------- 7. pin topology ----------
t7 = (DG["contract"] in st and DG["manifest"] in st and DG["manifest"] in T["contract"]
      and DG["spec"] not in T["contract"] and DG["spec"] not in T["manifest"]
      and DG["contract"] not in T["manifest"])
gov = all(('"mb/ninfty-stage2-predicate/v11"' in T[k] and "receipt が記入" in T[k]) for k in ("contract", "manifest"))
report(7, "pin topology (manifest->contract->spec, 循環 0)", t7 and gov,
       "spec pins C=%s M=%s / contract pins M=%s / 上流->下流 pin=None / governing=ID+receipt=%s"
       % (DG["contract"] in st, DG["manifest"] in st, DG["manifest"] in T["contract"], gov))

# ---------- 8. byte hygiene ----------
ok8 = True; rows8 = []
for k in F:
    raw = Bb[k]; t = T[k]; L = t.split("\n")
    c0 = sum(1 for l in L for ch in l if ord(ch) < 32)
    odd = len([i for i, l in enumerate(L, 1) if l.count("$") % 2 == 1])
    bad = raw.count(b"\r") + t.count(chr(9)) + c0 + odd + (1 if raw[:3] == b"\xef\xbb\xbf" else 0)
    rows8.append("%s LF=%d CR=%d TAB=%d C0=%d odd$=%d" % (k, raw.count(b"\n"), raw.count(b"\r"), t.count(chr(9)), c0, odd))
    if bad: ok8 = False
report(8, "byte hygiene", ok8, " ; ".join(rows8))

# ---------- 9. lifecycle tense ----------
ok9 = True; rows9 = []
for k in ("contract", "manifest"):
    t = T[k]
    a = "embedded_state_at_candidate_creation" in t and "live_status_authority" in t
    b = "receipt がその実在と digest を束縛するまで、本稿を operative として扱ってはならない" in t
    rows9.append("%s embedded/authority=%s fail-closed=%s" % (k, a, b))
    if not (a and b): ok9 = False
gate = "exact_freeze_bundle" in st and "mb/ninfty-stage2-predicate/v11" in st
report(9, "lifecycle tense", ok9 and gate, " ; ".join(rows9) + " ; spec gate(v11 束)=%s" % gate)

# ---------- 10. TCB arity ----------
decl = len(set(re.findall(r"^allowed_shared_\w+\[\]", mt, re.M)))
init = len(re.findall(r"^allowed_shared_\w+\s*=\s*\[\]", mt, re.M))
cls_m = classify(mt); cls_c = classify(T["contract"])
w = [w for i, l in enumerate(mt.split("\n"), 1) if cls_m.get(i) in OPERATIVE for w in re.findall(r"(五欄|四欄|三欄)", l)]
wc = [w for i, l in enumerate(T["contract"].split("\n"), 1) if cls_c.get(i) in OPERATIVE for w in re.findall(r"(五欄|四欄|三欄)", l)]
ok10 = decl == 4 and init == 4 and set(w) <= {"四欄"} and set(wc) <= {"四欄"}
report(10, "TCB arity", ok10, "宣言=%d 初期値[]=%d operative 語 manifest=%s contract=%s" % (decl, init, sorted(set(w)), sorted(set(wc))))

# ---------- 11. invariant contradiction ----------
old = [l for i, l in enumerate(st.split("\n"), 1)
       if "public は primary_reason_code のみを出す" in l and classify(st).get(i) in OPERATIVE | {"code"}]
old = [l for l in old if "canonical_sort" not in l and "更新" not in l]
ok11 = len(old) == 0 and "secondary_reason_codes[]" in st and "canonical_sort( ({[26]}" in st
report(11, "invariant mutual contradiction", ok11, "旧文 live 残存=%d / secondary normative=%s" % (len(old), "secondary_reason_codes[]" in st))

print("\nsha256:")
for k, p in F.items(): print("  %-9s %s  %s" % (k, DG[k], p))
print("\nRESULT:", "ALL PASS" if not fails else "FAIL at " + str(fails))
sys.exit(0 if not fails else 1)
