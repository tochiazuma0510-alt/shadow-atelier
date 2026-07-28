#!/usr/bin/env python3
# bundle-selfaudit.py -- N_infty stage2 freeze bundle self-audit (9 checks)
# usage: python search/bundle-selfaudit.py
# covers Sol blocker classes from 便 65-68 (B65-*, B66-*, B67-*, B68-*)
import os, re, sys, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {"spec":     "docs/week4-NInfty_stage2_spec_v10.md",
     "contract": "docs/mb_ninfty_verifier_contract_v5.md",
     "manifest": "docs/mb_dependency_manifest_v5.md"}
CUR = {"spec": "v10", "contract": "v5", "manifest": "v5"}
T = {k: open(os.path.join(D, p), encoding='utf-8').read() for k, p in F.items()}
B = {k: open(os.path.join(D, p), 'rb').read() for k, p in F.items()}
DG = {k: hashlib.sha256(v).hexdigest() for k, v in B.items()}
fails = []
def report(n, name, ok, detail):
    print(("PASS" if ok else "FAIL"), "|", n, name, "|", detail)
    if not ok: fails.append(n)

# ---------- 1. version-token sweep (B68-1) ----------
PAT = [("spec", r"mb/ninfty-stage2-predicate/v(\d+)"), ("spec", r"spec v(\d+)"),
       ("contract", r"mb/ninfty-verifier-contract/v(\d+)"), ("contract", r"contract v(\d+)"),
       ("manifest", r"mb/dependency-manifest/v(\d+)"), ("manifest", r"manifest v(\d+)"),
       ("s5", r"S5[-/ ]v(\d+)")]
def excluded_ranges(txt):
    """live_authority_refs / historical_quotation_refs blocks + diff tables + §8 record"""
    lines = txt.split("\n"); ex = set(); indiff = False
    for i, l in enumerate(lines, 1):
        if re.match(r"^## .*(差分|erratum 差分|版履歴)", l): indiff = True
        elif l.startswith("## ") and indiff: indiff = False
        if indiff and (l.startswith("| ") or l.startswith("> ")): ex.add(i)
        if l.lstrip().startswith(">") and ("版履歴" in l or "自認" in l or "欠陥" in l): ex.add(i)
    for key in ("live_authority_refs[]", "historical_quotation_refs[]"):
        p = txt.find(key)
        while p >= 0:
            s0 = txt[:p].count("\n") + 1
            for k in range(s0, s0 + 14): ex.add(k)
            p = txt.find(key, p + 1)
    for m in re.finditer(r"^\| \*\*LA-3\*\*.*$", txt, re.M): ex.add(txt[:m.start()].count("\n") + 1)
    for m in re.finditer(r"^\| \*\*CR-[0-9]\*\*.*$", txt, re.M): ex.add(txt[:m.start()].count("\n") + 1)
    for m in re.finditer(r"^supersedes[^\n]*$", txt, re.M): ex.add(txt[:m.start()].count("\n") + 1)
    return ex
HIST = ("版履歴", "差分", "supersedes", "自認", "監査 FAIL", "historical", "記録", "旧版",
        "でも不変", "継承", "note:", "要請時の原文", "発行済み", "欠陥", "撤回")
stale = []
for name, txt in T.items():
    ex = excluded_ranges(txt)
    for i, l in enumerate(txt.split("\n"), 1):
        if i in ex: continue
        if any(h in l for h in HIST): continue
        for series, pat in PAT:
            for m in re.finditer(pat, l):
                if series in CUR and "v" + m.group(1) == CUR[series]: continue
                stale.append((name, i, series, "v" + m.group(1), l.strip()[:70]))
report(1, "version-token sweep (B68-1)", len(stale) == 0,
       "対象=3 系列 x {mb/...形式, '<name> vN' 形式} + S5 = 7 pattern / 除外域=diff table, 版履歴, "
       "live_authority_refs, historical_quotation_refs, LA-3, CR-*, supersedes / LIVE-STALE=%d" % len(stale))
for s in stale: print("      ", s)

# ---------- 2. conformance set equality (B68-2 / F13.3) ----------
REG_RE = r"^\| \*\*([A-Z][A-Za-z0-9\-\.]*[′″‴]?)\*\* \|"
ok2 = True; det = []
for name in ("contract", "manifest"):
    txt = T[name]
    reg = set(m.group(1) for m in re.finditer(REG_RE, txt, re.M))
    mc = re.search(r"covered_clauses = \[(.*?)\]", txt, re.S)
    cov = set(x.strip() for x in mc.group(1).replace(chr(10), " ").split(",") if x.strip())
    mu = re.search(r"uncovered_clauses = \[(.*?)\]", txt, re.S)
    unc = set(x.strip() for x in mu.group(1).replace(chr(10), " ").split(",") if x.strip())
    ranges = [c for c in (cov | unc) if ".." in c]
    inter_ok = (cov & unc) == set()
    union_ok = (cov | unc) == reg
    det.append("%s: registry=%d covered=%d uncovered=%d range=%d cap=%s cup=%s"
               % (name, len(reg), len(cov), len(unc), len(ranges), inter_ok, union_ok))
    if ranges or not inter_ok or not union_ok:
        ok2 = False
        det.append("   %s reg-cov=%s cov-reg=%s" % (name, sorted(reg - cov)[:10], sorted(cov - reg)[:10]))
report(2, "conformance set equality (B68-2/F13.3)", ok2, " ; ".join(det))

# ---------- 3. derived-digest preimage completeness (B68-3) ----------
PRE = {  # digest name -> (binding target that MUST appear in preimage, preimage fields)
 "source_closure_digest":         ("source_artifact_digests[]", ["source_artifact_digests[]"]),
 "implementation_lineage_digest": ("source+toolchain+steps", ["source_artifact_digests[]", "toolchain_digest", "build_step_digests[]"]),
 "build_root_id":                 ("build_definition+pinned_inputs", ["build_definition_blob_digest", "pinned_input_digests[]"]),
 "subject_build_binding_digest":  ("subject_code_digest", ["subject_code_digest", "build_definition_blob_digest", "pinned_input_digests[]"]),
}
mtxt = T["manifest"]; ok3 = True; rows3 = []
for dn, (target, fields) in PRE.items():
    blk = re.search(r"D-\d\s+" + re.escape(dn) + r"\s*=(.{0,400})", mtxt, re.S)
    body = blk.group(1) if blk else ""
    present = all(f.replace("[]", "") in body for f in fields)
    rows3.append("%s: target=%s preimage_ok=%s" % (dn, target, present))
    if not present: ok3 = False
sbd_recalc = "I-0c" in mtxt and "subject_build_binding_digest" in mtxt
report(3, "derived-digest preimage completeness (B68-3)", ok3 and sbd_recalc,
       " ; ".join(rows3) + " ; I-0c'(受領側再計算)=%s" % sbd_recalc)

# ---------- 4. TCB arity (B68-4) ----------
HISTM = ("版履歴", "差分", "自認", "typo", "historical", "記録", "旧版", "Q2(F9)", "v4 の")
def live_lines(t): return [l for l in t.split(chr(10)) if not any(h in l for h in HISTM)]
decl = re.findall(r"^allowed_shared_\w+\[\]", mtxt, re.M)
decl_n = len(set(decl))
init = len(re.findall(r"^allowed_shared_\w+\s*=\s*\[\]", mtxt, re.M))
words = [w for l in live_lines(mtxt) for w in re.findall(r"(五欄|四欄|三欄)", l)]
ctr = [w for l in live_lines(T["contract"]) for w in re.findall(r"(五欄|四欄|三欄)", l)]
rcp = [w for l in live_lines(T["spec"]) for w in re.findall(r"(五欄|四欄|三欄)", l)]
ok4 = decl_n == 4 and init == 4 and set(words) <= {"四欄"} and set(ctr) <= {"四欄"} and set(rcp) <= {"四欄"}
report(4, "TCB arity (B68-4)", ok4,
       "manifest 宣言=%d 初期値[]=%d live 語=%s / contract live 語=%s / spec live 語=%s (historical 行は除外域)"
       % (decl_n, init, sorted(set(words)), sorted(set(ctr)), sorted(set(rcp))))

# ---------- 5. anchor existence + binding direction (v7 false-binding class) ----------
stxt = T["spec"]; ok5 = True; rows5 = []
for m in re.finditer(r'schema_id\(\s*([\w\-]+)\s*\)\s*=\s*(\w+)\s*\+\s*"#([\w\-]+)"', stxt):
    nm, owner, anc = m.group(1), m.group(2), m.group(3)
    tgt = {"predicate_spec_id": "spec", "verifier_contract_id": "contract",
           "dependency_manifest_schema_id": "manifest"}.get(owner)
    exists = ("{#" + anc + "}") in T.get(tgt, "")
    bm = re.search(r"bound_blob_digest\(\s*" + re.escape(nm) + r"\s*\)\s*=\s*(\w+)", stxt)
    bound = bm.group(1) if bm else "(grouped)"
    expect = {"spec": "predicate_spec_digest", "contract": "verifier_contract_digest",
              "manifest": "dependency_manifest_schema_digest"}[tgt]
    dir_ok = (bound == expect) or (bound == "(grouped)" and tgt == "spec")
    rows5.append("%s->%s#%s exists=%s bound=%s ok=%s" % (nm, tgt, anc, exists, bound, dir_ok))
    if not (exists and dir_ok): ok5 = False
report(5, "anchor existence + binding direction", ok5, " ; ".join(rows5))

# ---------- 6. pin topology (便 66 F7) ----------
t6 = (DG["contract"] in stxt and DG["manifest"] in stxt and DG["manifest"] in T["contract"]
      and DG["spec"] not in T["contract"] and DG["spec"] not in T["manifest"]
      and DG["contract"] not in T["manifest"])
gov = all(('"mb/ninfty-stage2-predicate/v10"' in T[k] and "receipt が記入" in T[k]) for k in ("contract", "manifest"))
report(6, "pin topology (manifest->contract->spec, 循環 0)", t6 and gov,
       "spec pins C/M=%s,%s ; contract pins M=%s ; upstream pins downstream=None ; governing=ID+receipt=%s"
       % (DG["contract"] in stxt, DG["manifest"] in stxt, DG["manifest"] in T["contract"], gov))

# ---------- 7. byte hygiene ----------
ok7 = True; rows7 = []
for k in F:
    raw = B[k]; t = T[k]; L = t.split("\n")
    c0 = sum(1 for l in L for ch in l if ord(ch) < 32)
    odd = len([i for i, l in enumerate(L, 1) if l.count("$") % 2 == 1])
    bad = raw.count(b"\r") + t.count(chr(9)) + c0 + odd + (1 if raw[:3] == b"\xef\xbb\xbf" else 0)
    rows7.append("%s LF=%d CR=%d TAB=%d C0=%d odd$=%d BOM=%s" %
                 (k, raw.count(b"\n"), raw.count(b"\r"), t.count(chr(9)), c0, odd, raw[:3] == b"\xef\xbb\xbf"))
    if bad: ok7 = False
report(7, "byte hygiene", ok7, " ; ".join(rows7))

# ---------- 8. lifecycle tense ----------
ok8 = True; rows8 = []
for k in ("contract", "manifest"):
    t = T[k]
    has_emb = "embedded_state_at_candidate_creation" in t and "live_status_authority" in t
    fc = "receipt がその実在と digest を束縛するまで、本稿を operative として扱ってはならない" in t
    noverpin = "v8 発行前に本稿を operative" not in t and "v9 の実在" not in t
    rows8.append("%s embedded/authority=%s fail-closed=%s 旧版要求残存=%s" % (k, has_emb, fc, not noverpin))
    if not (has_emb and fc and noverpin): ok8 = False
gate = ("exact_freeze_bundle" in T["spec"] and "mb/ninfty-stage2-predicate/v10" in T["spec"]
        and "v6 の Sol 監査 PASS}" not in T["spec"])
rows8.append("spec §9 gate=exact_freeze_bundle(v10 束)=%s" % gate)
report(8, "lifecycle tense (§0.1 型)", ok8 and gate, " ; ".join(rows8))

# ---------- 9. invariant mutual contradiction (B67-1) ----------
inv = re.findall(r"^invariant \d[^\n]*", stxt, re.M)
old = [l for l in stxt.split("\n")
       if "public は primary_reason_code のみを出す" in l and "invariant 2 が逐語" not in l and not l.startswith("| **D**")]
sec_norm = "secondary_reason_codes[]" in stxt and "P-S3" in stxt
ok9 = (len(old) == 0) and sec_norm and any("canonical_sort" in l for l in inv + stxt.split("\n"))
report(9, "invariant mutual contradiction (B67-1)", ok9,
       "invariant 行数=%d / 旧文『public は primary のみ』live 残存=%d / secondary normative=%s" %
       (len(inv), len(old), sec_norm))

print("\nsha256:")
for k, p in F.items(): print("  %-9s %s  %s" % (k, DG[k], p))
print("\nRESULT:", "ALL PASS" if not fails else "FAIL at " + str(fails))
sys.exit(0 if not fails else 1)
