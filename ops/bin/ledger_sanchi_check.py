#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三致検査 checker — 誤り台帳の「ヘッダ加法式 / 名前付き行数 / フッタ」照合。

規律(裁定 881 + Sol 便 118 W5):
  * 納品ファイルを **絶対パスで再オープンして読む**。
  * メモリ上の生成文字列を検査する checker は禁止(B117-2 の直接原因)。
  * ヘッダは数値の目視でなく **加法式そのものを parse して評価**する。

使い方: python ops/bin/ledger_sanchi_check.py <納品ファイルの絶対パス> <期待累計>
"""
import hashlib
import os
import re
import sys

try:                                   # Windows cp932 コンソール対策(表示のみ)
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

PRIOR = 23  # 前代 = v1.1 の 11 + Sol 便 114 の 12(§2.4 の表に行を持たない分)

ROW_RE = re.compile(r'^\|\s*(?:★\s*)?\*\*([EBMm][0-9]*-[0-9]+)\*\*\s*\|')
ID_RE = re.compile(r'[EBMm][0-9]*-[0-9]+')
FORMULA_RE = re.compile(r'\*\*(v1\.1 の .*?)\*\*')
HEADER_RE = re.compile(r'^\*\*v1\.1 の [0-9]+ \+ Sol 便 114')
FOOT24_RE = re.compile(r'\*\*⟹ 累計 ([0-9]+) 件\*\*')
FOOT9_RE = re.compile(r'\*\*誤り ([0-9]+) 件\*\*')


def eval_formula(text):
    """加法式を区間ごとに評価して (最終値, 各区間のトレース) を返す。"""
    running, trace = 0, []
    for seg in text.split('/'):
        if '=' not in seg:
            continue
        lhs, rhs = seg.rsplit('=', 1)
        totals = re.findall(r'[0-9]+', rhs)
        if not totals:
            continue
        declared = int(totals[-1])
        lhs = re.sub(r'[(（][^)）]*[)）]', ' ', lhs)   # 説明的な括弧は addend でない
        lhs = lhs.replace('v1.1', ' ')
        lhs = re.sub(r'便\s*[0-9]+', ' ', lhs)          # 便番号は addend でない
        n_ids = len(ID_RE.findall(lhs))                  # 列挙された ID は各 1 件
        lhs = ID_RE.sub(' ', lhs)
        nums = [int(x) for x in re.findall(r'[0-9]+', lhs)]
        delta = sum(nums) + n_ids
        running += delta
        trace.append((seg.strip(), nums, n_ids, delta, running, declared, running == declared))
    return running, trace


def main():
    path = os.path.abspath(sys.argv[1])
    expect = int(sys.argv[2])
    with open(path, 'rb') as fh:
        raw = fh.read()
    sha = hashlib.sha256(raw).hexdigest()
    lines = raw.decode('utf-8').split('\n')

    print('READ (absolute path) : %s' % path)
    print('EXISTS               : %s' % os.path.isfile(path))
    print('SHA-256              : %s' % sha)
    print('LINES                : %d' % len(lines))
    print('EXPECTED TOTAL       : %d' % expect)
    print('')

    fails = []

    # ---- §2.4 の範囲 ----
    start = next(i for i, l in enumerate(lines) if l.startswith('## 2.4'))
    end = next(i for i in range(start + 1, len(lines))
               if lines[i].startswith('---') or lines[i].startswith('# '))
    print('[span] §2.4 = line %d .. %d  | %s' % (start + 1, end, lines[start][:40]))
    print('')

    # ---- (a) ヘッダ加法式 ----
    hi = next(i for i in range(start, end) if HEADER_RE.match(lines[i]))
    hf = FORMULA_RE.search(lines[hi]).group(1)
    hv, htrace = eval_formula(hf)
    print('[a] HEADER additive formula  @ line %d' % (hi + 1))
    for seg, nums, nid, delta, run, dec, ok in htrace:
        print('      %-52s nums=%-12s ids=%d  +%-3d -> %-3d  declared=%-3d %s'
              % (seg[:52], nums, nid, delta, run, dec, 'OK' if ok else 'MISMATCH'))
        if not ok:
            fails.append('header segment mismatch @ line %d: %s' % (hi + 1, seg))
    print('      evaluated total = %d   (expect %d) : %s'
          % (hv, expect, 'PASS' if hv == expect else 'FAIL'))
    if hv != expect:
        fails.append('header evaluates to %d, expected %d' % (hv, expect))
    m = re.search(r'累計\s*([0-9]+)', hf)
    print('      literal "累計 N"  = %s : %s'
          % (m.group(1), 'PASS' if m and int(m.group(1)) == expect else 'FAIL'))
    if not m or int(m.group(1)) != expect:
        fails.append('header literal 累計 != %d' % expect)
    print('')

    # ---- (b) 名前付き行数 ----
    rows = [(i + 1, ROW_RE.match(lines[i]).group(1)) for i in range(start, end)
            if ROW_RE.match(lines[i])]
    print('[b] NAMED ROWS in §2.4 : %d' % len(rows))
    print('      first @ line %d = %s   last @ line %d = %s'
          % (rows[0][0], rows[0][1], rows[-1][0], rows[-1][1]))
    print('      ids = %s' % ', '.join(r[1] for r in rows))
    print('      %d rows + %d 前代 = %d  (expect %d) : %s'
          % (len(rows), PRIOR, len(rows) + PRIOR, expect,
             'PASS' if len(rows) + PRIOR == expect else 'FAIL'))
    if len(rows) + PRIOR != expect:
        fails.append('named rows %d + %d != %d' % (len(rows), PRIOR, expect))
    dup = [r for r in rows if [x[1] for x in rows].count(r[1]) > 1]
    print('      duplicate ids  : %s' % (dup if dup else 'none'))
    if dup:
        fails.append('duplicate ledger ids: %s' % dup)
    e40 = [r for r in rows if r[1] == 'E-40']
    print('      E-40 present   : %s  (must be absent — 便 118 W5) : %s'
          % (bool(e40), 'FAIL' if e40 else 'PASS'))
    if e40:
        fails.append('E-40 was numbered (duplicate of B117-2)')
    print('')

    # ---- (c) §2.4 フッタ ----
    fi = next(i for i in range(start, end) if FOOT24_RE.search(lines[i]))
    fv = int(FOOT24_RE.search(lines[fi]).group(1))
    ff = FORMULA_RE.search(lines[fi])
    fev = eval_formula(ff.group(1))[0] if ff else None
    print('[c] §2.4 FOOTER              @ line %d' % (fi + 1))
    print('      declared 累計 = %d  (expect %d) : %s'
          % (fv, expect, 'PASS' if fv == expect else 'FAIL'))
    print('      embedded formula evaluates to %s : %s'
          % (fev, 'PASS' if fev == expect else 'FAIL'))
    if fv != expect:
        fails.append('§2.4 footer = %d' % fv)
    if fev != expect:
        fails.append('§2.4 footer formula = %s' % fev)
    print('')

    # ---- (d) §9 フッタ ----
    gi = [i for i, l in enumerate(lines) if FOOT9_RE.search(l)]
    print('[d] §9 FOOTER "誤り N 件"    : %d hit(s)' % len(gi))
    for i in gi:
        v = int(FOOT9_RE.search(lines[i]).group(1))
        print('      @ line %d : %d  : %s' % (i + 1, v, 'PASS' if v == expect else 'FAIL'))
        if v != expect:
            fails.append('§9 footer @ line %d = %d' % (i + 1, v))
    if not gi:
        fails.append('§9 footer not found')
    print('')

    # ---- (e) stale 値 ----
    print('[e] STALE VALUES')
    for pat in ('累計 51', '誤り 51 件', '累計 45', '誤り 45 件'):
        hits = [i + 1 for i, l in enumerate(lines) if pat in l]
        print('      "%s" : %s' % (pat, hits if hits else 'absent (PASS)'))
        if hits:
            fails.append('stale "%s" @ lines %s' % (pat, hits))
    print('')

    print('=' * 62)
    if fails:
        print('RESULT: FAIL (%d)' % len(fails))
        for f in fails:
            print('  - %s' % f)
        sys.exit(1)
    print('RESULT: ALL PASS — header formula / named rows / footers agree at %d' % expect)
    sys.exit(0)


if __name__ == '__main__':
    main()
