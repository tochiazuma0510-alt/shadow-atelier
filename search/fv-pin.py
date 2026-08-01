#!/usr/bin/env python3
"""FAKE-VOID 母集団台帳 — cert pin 生成器 兼 検証器(machine-piped)

  python search/fv-pin.py           # 台帳の pin 表を再生成(標準出力)
  python search/fv-pin.py --verify  # pin 表 + プローブ述語の再検査(VERDICT 行を出す)

規律:
  - 本器は docs/notes/fake_void_v1.md の台帳欄を**生成**するためのもの。
    台帳の値を人手で写してはならない(machine-piped 規律)。
  - 本器は「fake witness ゼロ」を主張しない。主張するのは
    「pin した cert が実在し、その reduction 欄が surjective=true である」だけ。
    その帰結の解釈(= どの層のどの量化子に効くか)は台帳本文の責任。
"""

import hashlib, glob, json, os, sys

# (行ID, パス or "GLOB:<pattern>")
ROWS = [
    ("A-1",  "certificates/K3.v1.json"),
    ("A-1d", "docs/week4-K3飽和_opus_v3.md"),
    ("A-2",  "certificates/A1.v2.2.json"),
    ("A-2d", "docs/week4-A5算術飽和_v4.md"),
    ("A-3a", "certificates/K4.v1.json"),
    ("A-3b", "certificates/K8.v1.json"),
    ("A-3c", "certificates/K16.v1.json"),
    ("B-1",  "certificates/L01.v1.json"),
    ("B-2",  "certificates/M01.v1.json"),
    ("B-3",  "certificates/1b.v2.json"),
    ("B-4",  "certificates/2b.v2.json"),
    ("B-5",  "certificates/3.v2.json"),
    ("B-6a", "certificates/A1.v2.2.json"),
    ("B-6b", "certificates/A2.v2.json"),
    ("B-7",  "provenance/cert-hashes-wp2.txt"),
    ("B-V1", "crosscheck/verdicts/L01.v1.verdict.json"),
    ("B-V2", "crosscheck/verdicts/M01.v1.verdict.json"),
    ("B-V3", "crosscheck/verdicts/K3.v1.verdict.json"),
    ("B-V4", "GLOB:crosscheck/verdicts/[123][ab]*.v2.verdict.json"),
    ("B-V5", "GLOB:crosscheck/verdicts/A[12]*.verdict.json"),
    ("C-1",  "GLOB:certificates/e2c6/m6_j2_m*.json"),
    ("C-2",  "GLOB:certificates/e2c6j3/*.json"),
    ("D-0",  "docs/notes/gtpi_cv9_freeze_v1.md"),
    ("D-1",  "search/certs/gtpi_closure_20260801.json"),
    # E-* = 帯 W(GTSh 非可解)の既知 4 窓
    ("E-1",  "search/certs/wall2_cert_20260731.json"),
    ("E-2",  "search/certs/wall28_cert_20260731.json"),
    ("E-3",  "search/certs/wall36_cert_20260731_r2.json"),
    ("E-4",  "search/certs/wall37_cert_20260731_r2.json"),
    # S-* = 「壁族」の名で括られているが GTSh は可解 = 帯 D の元(cert が solvable:true)
    ("S-1",  "search/certs/wall40_cert_20260801.json"),
    ("S-2",  "search/certs/wall45_cert_20260801.json"),
    ("S-3",  "search/certs/dl3_cert_20260731.json"),
    ("S-4",  "search/certs/centb_cert_20260731.json"),
    ("F-1",  "search/certs/wall_miner_v5_20260729.json"),
    ("F-1b", "search/certs/wall_probe_20260728.json"),
    ("F-2",  "search/certs/wall_census_192_360_20260730.json"),
    ("F-3",  "search/certs/a13_ladder_manifest_20260730.json"),
    ("F-4",  "GLOB:certificates/S[1-7].v2.json"),
    ("G-1",  "search/certs/ep_sweep744_20260801.json"),
    ("G-2",  "GLOB:certificates/mb/actions/30289323147/ninfty-b5-*.json"),
    ("G-3",  "docs/notes/p52_deathcause_v1.md"),
    ("G-3a", "docs/notes/p52_deathcause_v1_addendum_novelty.md"),
    ("G-4",  "certificates/mb/actions/30289323147/RETRACTED_AS_CANDIDATE.md"),
    # 追記 A(erratum)の出所
    ("H-1",  "docs/scout/覚書_fvl1_20260801.md"),
    ("H-2",  "papers/txt/2008.00066-what-are-gt-shadows.txt"),
    ("H-3",  "certificates/N5.v1.json"),
]

# (プローブID, cert パス, 標的名, 期待 image_size)
#   None = image_size 欄を持たない cert(surjective 欄のみ検査)
PROBES = [
    ("P/K3<-L",    "certificates/L01.v1.json", "K3",  None),
    ("P/K3<-M5",   "certificates/M01.v1.json", "K3",  None),
    ("P/K3<-1b",   "certificates/1b.v2.json",  "K3",  12),
    ("P/NQ<-1b",   "certificates/1b.v2.json",  "N_Q", None),
    ("P/N2<-2b",   "certificates/2b.v2.json",  "N2",  4),
    ("P/NQ<-2b",   "certificates/2b.v2.json",  "N_Q", 4),
    ("P/K3<-M3",   "certificates/3.v2.json",   "K3",  12),
    ("P/N3<-M3",   "certificates/3.v2.json",   "N3",  8),
    ("P/NA<-MA5",  "certificates/A2.v2.json",  "N_A", 20),
]


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 16), b""):
            h.update(blk)
    return h.hexdigest()


def emit_pins():
    missing = 0
    print("# rowid\tpath\tstatus\tsha256\tnfiles")
    for rid, spec in ROWS:
        if spec.startswith("GLOB:"):
            pat = spec[5:]
            files = sorted(glob.glob(pat))
            if not files:
                print(f"{rid}\t{pat}\tMISSING\t-\t0"); missing += 1; continue
            agg = hashlib.sha256()
            for p in files:
                agg.update(sha_file(p).encode())
            print(f"{rid}\t{pat}\tOK\t{agg.hexdigest()}\t{len(files)}")
        else:
            if not os.path.exists(spec):
                print(f"{rid}\t{spec}\tMISSING\t-\t0"); missing += 1; continue
            print(f"{rid}\t{spec}\tOK\t{sha_file(spec)}\t1")
    return missing


def verify_probes():
    fails = 0
    print("\n# probeid\tcert\ttarget\tsurjective\timage_size\tresult")
    for pid, path, target, want in PROBES:
        if not os.path.exists(path):
            print(f"{pid}\t{path}\t{target}\t-\t-\tMISSING"); fails += 1; continue
        d = json.load(open(path, encoding="utf-8"))
        red = d.get("reductions", d.get("reduction"))
        hit = None
        for e in (red or []):
            if e.get("target") == target or e.get("to") == target:
                hit = e; break
        if hit is None:
            print(f"{pid}\t{path}\t{target}\t-\t-\tNO_ENTRY"); fails += 1; continue
        surj = hit.get("surjective")
        isz = hit.get("image_size")
        ok = (surj is True) and (want is None or isz == want)
        if not ok:
            fails += 1
        print(f"{pid}\t{path}\t{target}\t{surj}\t{isz}\t{'PASS' if ok else 'FAIL'}")
    return fails


def census():
    """cert 樹全体を走査し、reduction/survival プローブを**悉皆**列挙する。
    台帳の『どの窓に fake プローブが存在するか / しないか』欄はこの出力が正本。
    ここに現れない窓は、fake プローブ 0 本(= 構造測定のみ)である。"""
    import collections
    rows, bad = [], 0
    pats = ["certificates/**/*.json", "search/certs/**/*.json"]
    seen = set()
    for pat in pats:
        for p in glob.glob(pat, recursive=True):
            p = p.replace("\\", "/")
            if p in seen:
                continue
            seen.add(p)
            try:
                d = json.load(open(p, encoding="utf-8"))
            except Exception:
                bad += 1
                continue
            if not isinstance(d, dict):
                continue
            r = d.get("reductions", d.get("reduction"))
            if not r or not isinstance(r, list):
                continue
            for e in r:
                if not isinstance(e, dict):
                    continue
                tgt = e.get("target") or e.get("to")
                img = e.get("image_size")
                if img is None and isinstance(e.get("image"), list):
                    img = len(set(e["image"]))
                rows.append((str(tgt), p, e.get("surjective"), img, e.get("kernel_order")))
    rows.sort()
    print("\n# target\tsource_cert\tsurjective\timage_size\tkernel_order")
    for t in rows:
        print("\t".join(str(x) for x in t))
    c = collections.Counter(t[0] for t in rows)
    print(f"\n# PROBE_ENTRIES={len(rows)} DISTINCT_BASE_WINDOWS={len(c)} "
          f"UNPARSABLE_JSON={bad}")
    print("# BY_BASE_WINDOW=" + str(dict(sorted(c.items()))))
    print("# ALL_SURJECTIVE=" + str(all(t[2] is True for t in rows)))
    return 0 if all(t[2] is True for t in rows) else 1


def bands():
    """C-WALL-FAM の各窓を帯 D(GTSh 可解)/ 帯 W(非可解)へ機械的に振り分ける。
    根拠は cert 自身の solvable 欄(工房の分類語ではなく cert の値が正本)。"""
    import re
    fam = [
        ("n=24", "search/certs/wall2_cert_20260731.json"),
        ("n=28", "search/certs/wall28_cert_20260731.json"),
        ("n=36", "search/certs/wall36_cert_20260731_r2.json"),
        ("n=37", "search/certs/wall37_cert_20260731_r2.json"),
        ("n=40", "search/certs/wall40_cert_20260801.json"),
        ("n=45", "search/certs/wall45_cert_20260801.json"),
        ("n=21 (T5-dl3)", "search/certs/dl3_cert_20260731.json"),
        ("n=18 (W-CENT-B)", "search/certs/centb_cert_20260731.json"),
    ]
    print("\n# window\tcert\tsolvable\tderived_length\tband")
    nW = nD = 0
    for lab, p in fam:
        if not os.path.exists(p):
            print(f"{lab}\t{p}\t-\t-\tMISSING"); continue
        s = open(p, encoding="utf-8", errors="replace").read()
        sv = re.search(r'"solvable"\s*:\s*(true|false)', s)
        dl = re.search(r'"derived_length"\s*:\s*(-?\d+)', s)
        sv = sv.group(1) if sv else "?"
        band = "W(non-solvable)" if sv == "false" else ("D(solvable)" if sv == "true" else "?")
        if sv == "false":
            nW += 1
        elif sv == "true":
            nD += 1
        print(f"{lab}\t{p}\t{sv}\t{dl.group(1) if dl else '-'}\t{band}")
    print(f"\n# BAND_W_COUNT={nW} BAND_D_COUNT={nD}")
    return 0


if __name__ == "__main__":
    m = emit_pins()
    rc = 0
    if "--bands" in sys.argv:
        rc += bands()
    if "--verify" in sys.argv:
        rc += verify_probes()
    if "--census" in sys.argv:
        rc += census()
    if any(a.startswith("--") for a in sys.argv[1:]):
        print(f"\nVERDICT: pins_missing={m} failures={rc} "
              f"{'ALL PASS' if (m == 0 and rc == 0) else 'ATTENTION'}")
    elif m:
        print(f"\n# WARNING: {m} pinned path(s) missing", file=sys.stderr)
